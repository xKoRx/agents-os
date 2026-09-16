---
type: session-feedback
schema_version: 1
created: "2026-09-16"
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
related: []
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
---

# 2026-09-16 — Access Ops reconciliation session feedback

- **Fricción (menor):** `search_files` vía kernel hermes_tools falló con JSONDecodeError "Extra data" en múltiples resultados multi-file; workaround estable = `find`/`grep` por terminal. Patrón ya observado antes en salidas multi-JSON.
- **Observación:** los archivos de resultado de execute_code con stdout >50KB requieren re-paginación por `read_file` del spill path — flujo funcional pero costoso en llamadas para notas grandes (matrices Echo >100k chars).
- **Pain pattern candidate:** extracción de entidades vault grandes (notas proyecto 400–900 líneas) consume la mayor parte del presupuesto de la sesión; un resumen/índice por nota canónica (frontmatter `summary:` o extracto de bitácora reciente) reduciría lecturas completas.
