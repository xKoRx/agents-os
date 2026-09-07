---
type: learning
scope: project
created: 2026-08-08
updated: 2026-08-08
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Fase 2]]"
aliases:
  - lint all-vault canónico
  - explicit lint paths bypass exclusions
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - project/agents-os
  - tech/agents-os
  - priority/high
---

# Paths explícitos en lint omiten las exclusiones del corpus

El baseline all-vault comparable se ejecuta sin paths posicionales:

```bash
python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --check
```

Al pasar cualquier path explícito —incluido `.`— el lint omite sus exclusiones
normales e incorpora trash, outputs, derivados y fixtures. Ese modo sirve para
una validación dirigida, pero sus conteos no representan el corpus canónico ni
deben compararse con el gate `warn-first` de Graphify.
