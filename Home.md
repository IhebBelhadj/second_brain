---
type: home
tags: []
---
# Home

## Weakest — study these next
```dataview
TABLE WITHOUT ID file.link AS Note, topic AS Topic, confidence AS Conf
FROM ""
WHERE confidence <= 2
SORT confidence ASC
LIMIT 15
```

## Unresolved mistakes
```dataview
LIST
FROM ""
WHERE type = "mistake" AND resolved != true
SORT file.ctime DESC
```

## Inbox
```dataview
LIST
FROM "Inbox"
SORT file.ctime ASC
```

## Active projects
```dataview
TABLE WITHOUT ID file.link AS Project, due AS Due
FROM "Projects"
WHERE status = "active"
SORT due ASC
```

## Reading now
```dataview
TABLE WITHOUT ID file.link AS Source, medium AS Type
FROM "Resources"
WHERE status = "reading"
```

## Recent practice
```dataview
TABLE WITHOUT ID file.link AS Session, topic AS Topic, score AS Score
FROM ""
WHERE type = "practice"
SORT date DESC
LIMIT 5
```

## Topics
```dataview
LIST
FROM #topic
SORT file.name ASC
```

## Orphans — link these or delete them
```dataview
LIST
FROM "Notes" OR "Areas"
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
LIMIT 10
```
