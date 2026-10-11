---
type: weekly
created: <% tp.date.now("YYYY-MM-DD") %>
tags: []
---
# Week <% tp.date.now("gggg-[W]ww") %>

## Clear
- [ ] Inbox empty
- [ ] Daily captures filed

## Numbers
| | This week |
|---|---|
| Hours studied |  |
| New notes |  |
| Practice score |  |

## Weakest right now
```dataview
TABLE WITHOUT ID file.link AS Note, topic, confidence AS Conf
FROM ""
WHERE confidence AND confidence <= 2 AND file.name != "AGENTS" AND file.name != "CLAUDE"
SORT confidence ASC
LIMIT 10
```

## Reflection
- Worked:
- Didn't:
- Change next week:

## Next week
- [ ] 
