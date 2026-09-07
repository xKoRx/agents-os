# Control Panel

## Sync

![[obsidian-sync]]

## Graphify

![[graphify-echo-forge]]

## Monitores

```dataview
TABLE status, last_check, service
FROM "90-system"
WHERE type = "monitor"
SORT last_check DESC
```
