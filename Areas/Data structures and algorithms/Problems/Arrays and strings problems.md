---
type: concept
created: 2026-10-02
topic: Data structures and algorithms
confidence: 1
tags: [dsa, problems, strings, ctci]
aliases: [Check permutation, URLify, Palindrome permutation, One away, CtCI chapter 1]
---
# Arrays and strings problems

> [!abstract] In one sentence
> The problems from *Cracking the Coding Interview* chapter 1 that I solved, each with the idea that cracks it, a clean solution, its cost, and what my own version gets wrong. Most of them reduce to three tools: **counting characters with a [[Hash table]]**, **comparing with two indexes** instead of building new strings, and **bit vectors** as a tiny set.

## The recurring patterns

| Pattern | Idea | Problems below |
|---|---|---|
| **Frequency count** | Count each character in a dict (or a fixed array of 26/128), then reason about the counts | Check permutation, palindrome permutation |
| **Bit vector** | One integer, one bit per possible character: a set in a single number. Toggle with XOR | Palindrome permutation |
| **Two indexes / one pass** | Walk both strings with indexes, allow one difference, don't build substrings | One away |
| **Work from the end** | When the output is longer than the input in the same buffer, fill it from the back so nothing gets overwritten | URLify |

Before coding any of them: **clarify the input** (case-sensitive? spaces count? ASCII or Unicode?). Half of my bugs below are an unasked question about the input.

## 1.2 Check permutation

> Given two strings, decide if one is a permutation of the other. `"listen"`, `"silent"` → true.

**Idea:** same length and same character counts.

My solution is correct:

```python
def check_permutation(s1, s2):
    if len(s1) != len(s2):
        return False
    freq = {}
    for ch in s1:
        freq[ch] = freq.get(ch, 0) + 1
    for ch in s2:
        if freq.get(ch, 0) == 0:     # more of ch in s2 than in s1
            return False
        freq[ch] -= 1
    return True
```

| Approach | Time | Extra space |
|---|---|---|
| Count with a dict (above), or `Counter(s1) == Counter(s2)` | O(n) | O(k), k = distinct characters |
| Sort both and compare: `sorted(s1) == sorted(s2)` | O(n log n) | O(n) |

The length check isn't just an optimization: without it, `"ab"` vs `"abc"` would pass the loop (the second loop never sees a missing character).

## 1.3 URLify

> Replace every space with `%20`. The book's version: a character array with enough free space at the end, and the "true length" of the string. `"Mr John Smith    ", 13` → `"Mr%20John%20Smith"`.

**Idea (in place, from the end):** count the spaces in the true length, compute the final length (`true_length + 2 × spaces`), then copy characters **from the back**, writing `0`, `2`, `%` for each space. Going backwards means I never overwrite a character I haven't copied yet.

```python
def urlify(chars, true_length):          # chars: list with free space at the end
    spaces = chars[:true_length].count(" ")
    write = true_length + 2 * spaces - 1
    for read in range(true_length - 1, -1, -1):
        if chars[read] == " ":
            chars[write - 2:write + 1] = ["%", "2", "0"]
            write -= 3
        else:
            chars[write] = chars[read]
            write -= 1
    return chars[:true_length + 2 * spaces]
```

In Python, strings are immutable, so the idiomatic answer is `s[:true_length].replace(" ", "%20")`. The in-place version is what the interview is about (C, Java char arrays).

**What my version does:** splits into words, then joins them with `%20`, adding one **after every word**. Run results:

| Input | Mine | Expected |
|---|---|---|
| `"Mr John Smith"` | `Mr%20John%20Smith%20` | `Mr%20John%20Smith` |
| `"Mr John Smith    "` | `Mr%20John%20Smith%20%20` | `Mr%20John%20Smith` (true length 13) |
| `"a  b"` | `a%20b%20` | `a%20%20b` (each space replaced) |

Three issues: a trailing `%20` after the last word, `if buffer != ' '` should be `!= ''` (an empty last word gets added, giving the extra `%20%20`), and consecutive spaces are collapsed instead of each one replaced. Building `res += word + '%20'` in a loop also copies the string each time (O(n²) worst case, `"".join` avoids it).

## 1.4 Palindrome permutation

> Is the string a permutation of a palindrome? `"Tact Coa"` → true (`"taco cat"`). Spaces and case are ignored.

**Idea:** a palindrome reads the same both ways, so every character appears an **even** number of times, except **at most one** (the middle one, for odd lengths). The order doesn't matter, only the counts.

**With a dict** (my `is_palandrome`): count, then count how many characters have an odd count. Correct logic, but it doesn't ignore spaces or case: `"Tact Coa"` returns **False** (the space appears once, `T` and `t` are different).

```python
def palindrome_permutation(s):
    odd = set()
    for ch in s.lower():
        if not ch.isalpha():
            continue
        odd ^= {ch}                  # toggle: in the set = odd count so far
    return len(odd) <= 1
```

**With a bit vector** (my `is_palandrome_binary`): one integer, bit k = "letter k has been seen an odd number of times". XOR toggles it. At the end, at most one bit may be set, and a number with at most one bit set satisfies `x & (x - 1) == 0`:

```
x      = 0b0010000   (one bit set)
x - 1  = 0b0001111
x & (x - 1) = 0      → true

x      = 0b0010100   (two bits set)
x - 1  = 0b0010011
x & (x - 1) = 0b0010000 ≠ 0 → false
```

My version computes `bit = ord(char) - ord('a')` for **every** character. For a space or an uppercase letter, that's negative, and `1 << -65` raises `ValueError: negative shift count` (that's what `"Tact Coa"` does). Fix: lowercase first and skip anything outside `a`–`z`.

| Approach | Time | Space |
|---|---|---|
| Dict / set of odd characters | O(n) | O(k) |
| Bit vector | O(n) | O(1): one integer (only works for a small fixed alphabet) |

## 1.5 One away

> Edits are: insert a character, remove a character, replace a character. Are two strings at most one edit apart? `pale, ple` → true. `pales, pale` → true. `pale, bale` → true. `pale, bake` → false.

**Idea:** insert and remove are the same check seen from the other string. So:
- Lengths differ by more than 1 → false
- Same length → at most **one position** differs (replace)
- Lengths differ by 1 → skipping **one** character in the longer string makes them equal (insert/remove)

My **first attempt** (`one_away`, which I marked `# wrong` myself) tries to repair the strings while scanning. Running it confirms it fails both ways:

| Input | First attempt | Correct |
|---|---|---|
| `pale, ple` | False | **True** |
| `baller, baler` | False | **True** |
| `ab, ba` | True | **False** (two replaces) |
| `pale, pa` | True | **False** (two removals) |

The last two show a structural problem: the loop only runs to the length of the **shorter** string, so extra characters at the end of the longer one are never examined.

My **refined version** (`one_away_refined`) passes all of these. It swaps so `s1` is the shorter, finds the **first** difference, and decides there: same length → the rest after `i` must match (`s1[i+1:] == s2[i+1:]`), different length → `s1[i:] == s2[i+1:]` (skip one character in the longer). No difference found → equal, or one extra character at the end: true.

It's O(n) time, but the slices copy the rest of the strings (O(n) memory). The two-index version avoids copies:

```python
def one_away(a, b):
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) > len(b):
        a, b = b, a                       # a is the shorter (or equal)
    i = j = 0
    found_diff = False
    while i < len(a) and j < len(b):
        if a[i] != b[j]:
            if found_diff:
                return False
            found_diff = True
            if len(a) == len(b):
                i += 1                    # replace: move both
        else:
            i += 1                        # match: move the shorter
        j += 1                            # the longer always moves
    return True
```

## Practice

> [!example]- Is `"aabbccd"` a permutation of a palindrome? And `"aabbcd"`?
> `"aabbccd"`: only `d` has an odd count → yes (`abcdcba`). `"aabbcd"`: `c` and `d` odd → no.

> [!example]- What is `0b1011000 & (0b1011000 - 1)`, and what does it say?
> `0b1011000 - 1 = 0b1010111`, AND = `0b1010000` ≠ 0: more than one bit set.

> [!example]- `one_away("apple", "aple")`: trace the two-index version.
> Lengths 4 and 5, a = "aple", b = "apple". a,a match; p,p match; l vs p differ → found_diff, lengths differ so only j moves; l vs l match; e vs e match. Returns True.

> [!example]- Why does URLify fill the buffer from the end?
> The output is longer than the input in the same array. Writing from the front would overwrite characters not copied yet. From the back, the write index is always ahead of (or equal to) the read index.

## Easy to get wrong
- Not asking: case-sensitive? spaces count? which alphabet?
- Forgetting the length check in check permutation
- Bit tricks on characters outside the expected range (negative shifts)
- Only scanning up to the shorter string's length and missing trailing differences
- Building strings with `+=` in a loop instead of `"".join`
- Slicing in a loop (`s[i+1:]`) when two indexes would do

## Related
- Data structures:: [[Hash table]] (frequency counts)
- Techniques:: *[[Two pointers]]*, *[[Bit manipulation]]*
- Number representation:: [[Number base conversion]]
- Area:: [[Data structures and algorithms]]

## Flashcards
#flashcards

How to check if two strings are permutations of each other? :: Same length and same character counts (dict/Counter), O(n)
Condition for a string to be a permutation of a palindrome? :: At most one character has an odd count
How to track odd/even counts with a bit vector? :: XOR toggles one bit per character
How to test that at most one bit is set in x? :: x & (x - 1) == 0
Why does URLify fill from the end? :: The output is longer than the input in the same buffer, so writing backwards never overwrites unread characters
Idiomatic Python URLify? :: s[:true_length].replace(" ", "%20")
One away: the three cases? :: Length difference > 1 false. Same length: at most one differing position. Length differs by 1: skip one character in the longer string
Why are insert and remove the same check in one away? :: Inserting into one string is removing from the other
Why is `res += word` in a loop slow in Python? :: Strings are immutable, each += copies: use "".join
What question should I ask before solving a string problem? :: Case sensitivity, whether spaces count, and the character set (ASCII/Unicode)
