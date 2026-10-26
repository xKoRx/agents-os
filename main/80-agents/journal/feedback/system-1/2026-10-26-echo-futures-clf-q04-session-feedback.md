---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: ["[[Echo Futures]]"]
related: []
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# Feedback — CLF-Q04 (fricciones reales)

1. **MCP aranea-ssh con sesión de transporte expirada durante todo el shot** (`Session not found or expired. Re-initialize` en todas las llamadas a `mcp__aranea-ssh__*`). Trabajé por Bash local porque la máquina local ES Hefesto (`~/echo-work` existe localmente), pero el canal MCP quedó inservible y sin forma de reinicializarlo desde la sesión. Si la auditoría hubiera requerido otro host, habría bloqueado el shot.
2. **El catálogo canónico `STRATEGIES-CATALOG.md` no existe en el vault** pese a que el master de investigación lo declara re-domiciliado (2026-10-24) y el QA dice haberlo verificado "cuando vivía en este directorio". La migración nunca dejó el archivo; la auditoría tuvo que reconstruir la autoridad desde la capa por capítulo (rules/CLAIMS). Riesgo de trazabilidad si el archivo compilado nunca existió fuera de un directorio de trabajo.
3. **Ambigüedad de nombres en los CSV Q03R1** (`CLF-Q03R1-LASTCONTRACT-ALL-VARIANTS.csv` suma 69 round-trips de NQZ6 mientras `CLF-Q03R1-G4-QUALIFICATION.csv` suma 54 de NQU6) provocó una revisión externa que leyó "54 atribuidos al último contrato". Sugerencia: renombrar a `...NQZ6-...`/`...NQU6-...` o añadir columna `contract` a ambos.
4. **El campo `profile.provider_fee $50 (FACT)` del plan no es consumido por el modelo de cash** (que cobra $120 en compra y renovación, config declarada en `campaign.go`). Dos verdades de costeo conviven en el mismo plan sellado; conviene unificar o documentar la semántica.
5. Positivo: los streams `economic.ndjson.gz` + `result.json` sellados permitieron una reconstrucción económica independiente completa (fill-a-fill, céntimo exacto) sin re-ejecutar nada — el formato de recibos demostró ser auditable de verdad.
