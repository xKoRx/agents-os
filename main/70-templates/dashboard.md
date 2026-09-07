---
type: dashboard
schema_version: 1
status: active
icon: 📊
tags:
  - kind/dashboard
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

> [!tip] Panel de control. Vistas derivadas del vault; la fuente de verdad vive en cada nota.

## Sección

```base
filters:
  and:
    - 'type == "project"'
views:
  - type: cards
    name: Vista
    order:
      - file.name
```
