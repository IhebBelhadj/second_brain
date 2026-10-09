---
type: subtopic
created: <% tp.date.now("YYYY-MM-DD") %>
topic: 
tags: [subtopic]
---
# <% tp.file.title %>

> What this covers:

Part of [[]]. Same reading order as the full index; each note assumes the ones above it.

## Notes, in reading order
- 

## Weakest first
```dataview
TABLE WITHOUT ID file.link AS Note, type AS Type, confidence AS Conf
FROM ""
WHERE subtopic = this.file.name AND confidence
SORT confidence ASC
```
