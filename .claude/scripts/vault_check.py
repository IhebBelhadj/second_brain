#!/usr/bin/env python3
"""Health check for the vault. Run from anywhere: python3 .claude/scripts/vault_check.py

Checks:
  - wikilinks that resolve to no note (by file name or alias). Italic links *[[X]]* are
    treated as planned notes and listed separately, not as errors
  - [[Note#Heading]] links whose heading doesn't exist
  - duplicate note names and aliases that collide with other notes
  - notes under Areas/ missing frontmatter their template defines (type, and topic/confidence
    when the template for that type has them)
  - notes under Areas/<Area>/ not linked from the topic index Areas/<Area>/<Area>.md
  - notes under Areas/<Area>/ not listed in the area guide Areas/<Area>/AGENTS.md

Exit code 1 if anything other than planned notes is reported.
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKIP_DIRS = {".git", ".obsidian", ".trash", ".claude", "Templates"}
GUIDE_FILES = {"AGENTS.md", "CLAUDE.md"}
LINK_RE = re.compile(r"(\*?)(!?)\[\[([^\]]+?)\]\](\*?)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*$")


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".md") and f not in GUIDE_FILES:
                yield os.path.join(dirpath, f)


def frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def parse_list(value):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [x.strip().strip("\"'") for x in value[1:-1].split(",") if x.strip()]
    return [value] if value else []


def headings(text):
    out = set()
    in_code = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            m = HEADING_RE.match(line)
            if m:
                out.add(m.group(1).strip().lower())
    return out


def main():
    notes = {}  # lowercase name -> path
    texts = {}
    problems = defaultdict(list)
    planned = defaultdict(set)

    for path in md_files():
        name = os.path.basename(path)[:-3]
        if name.lower() in notes:
            problems["duplicate note names"].append(f"{name}: {rel(notes[name.lower()])} / {rel(path)}")
        notes[name.lower()] = path
        with open(path, encoding="utf-8") as fh:
            texts[path] = fh.read()

    aliases = {}
    for path, text in texts.items():
        for a in parse_list(frontmatter(text).get("aliases", "")):
            key = a.lower()
            if key in notes and notes[key] != path:
                problems["alias collides with a note name"].append(f"'{a}' in {rel(path)} vs {rel(notes[key])}")
            elif key in aliases and aliases[key] != path:
                problems["alias used twice"].append(f"'{a}': {rel(path)} / {rel(aliases[key])}")
            aliases.setdefault(key, path)

    def resolve(target):
        return notes.get(target.lower()) or aliases.get(target.lower())

    heading_cache = {}
    for path, text in texts.items():
        body = re.sub(r"```.*?```", "", text, flags=re.S)
        for star1, bang, inner, star2 in LINK_RE.findall(body):
            target = inner.replace("\\|", "|").split("|")[0]
            target, _, heading = target.partition("#")
            target = target.strip()
            if not target:
                continue
            if bang and os.path.splitext(target)[1] not in ("", ".md"):
                continue  # embedded image / attachment
            dest = resolve(target)
            if not dest:
                if star1 and star2:
                    planned[target].add(rel(path))
                else:
                    problems["unresolved links"].append(f"[[{target}]] in {rel(path)}")
                continue
            if heading:
                hs = heading_cache.setdefault(dest, headings(texts[dest]))
                if heading.strip().lower() not in hs:
                    problems["broken heading links"].append(f"[[{target}#{heading}]] in {rel(path)}")

    # which fields each note type must have = what its template defines
    template_fields = {}
    tdir = os.path.join(ROOT, "Templates")
    for f in os.listdir(tdir):
        if f.endswith(".md"):
            fm = frontmatter(open(os.path.join(tdir, f), encoding="utf-8").read())
            if fm.get("type"):
                template_fields[fm["type"]] = set(fm)

    areas_dir = os.path.join(ROOT, "Areas")
    for area in sorted(os.listdir(areas_dir)):
        area_path = os.path.join(areas_dir, area)
        if not os.path.isdir(area_path):
            continue
        index = os.path.join(area_path, f"{area}.md")
        guide = os.path.join(area_path, "AGENTS.md")
        index_text = texts.get(index, "")
        guide_text = open(guide, encoding="utf-8").read() if os.path.exists(guide) else ""
        if not os.path.exists(guide):
            problems["missing area guide"].append(rel(guide))
        linked = {m[2].replace("\\|", "|").split("|")[0].split("#")[0].strip().lower()
                  for m in LINK_RE.findall(index_text)}
        for path in texts:
            if not path.startswith(area_path + os.sep) or path == index:
                continue
            name = os.path.basename(path)[:-3]
            fm = frontmatter(texts[path])
            expected = {"type"} | ({"topic", "confidence"} & template_fields.get(fm.get("type", ""), set()))
            missing = sorted(k for k in expected if not fm.get(k))
            if missing:
                problems["missing frontmatter"].append(f"{rel(path)}: {', '.join(missing)}")
            if name.lower() not in linked:
                problems[f"not linked from the {area} index"].append(rel(path))
            if guide_text and f"{name}.md" not in guide_text:
                problems[f"not listed in Areas/{area}/AGENTS.md"].append(rel(path))

    for kind, items in problems.items():
        print(f"\n✗ {kind} ({len(items)})")
        for i in sorted(set(items)):
            print(f"   {i}")
    if planned:
        print(f"\n· planned notes, linked in italics ({len(planned)})")
        for t in sorted(planned):
            print(f"   {t}  ← {', '.join(sorted(planned[t]))}")
    if not problems:
        print(f"\n✓ {len(texts)} notes, no problems")
    sys.exit(1 if problems else 0)


def rel(p):
    return os.path.relpath(p, ROOT)


if __name__ == "__main__":
    main()
