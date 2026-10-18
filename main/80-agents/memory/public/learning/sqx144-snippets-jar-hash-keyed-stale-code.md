---
type: learning
schema_version: 1
scope: area
area: "[[Echo]]"
created: "2026-10-18"
updated: "2026-10-18"
confidence: verified
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
load_policy: manual
indexable: true
index_priority: normal
tags:
  - kind/learning
  - area/echo
  - tech/deployment
  - tech/sqx
---

# SQX 144 snippets: cache hash-keyed — actualizar fuente+hash a la vez ejecuta código stale

En Build 144, el plugin Forge (CustomAnalysis exporters) ejecuta las clases de `internal/libs/Snippets.jar`; `user/settings/snippets.txt` es el manifiesto `<fuente>|<md5>` y SQX solo recompila un snippet cuando el md5 listado DIFIERE del md5 de la fuente en disco. Demostrado físicamente el 2026-10-18 con 5 runs trampa en Kronos (verificado por firma JFR): reemplazar solo `user/libs/EchoForgeAutomator.jar` no cambia el código ejecutado, y actualizar fuente+hash simultáneamente deja el jar stale corriendo en silencio (los timings "candidato" eran baseline). Una clase nueva no se descubre desde user/libs ("Class ... doesn't exist").

**Por qué importa:** cualquier prueba A/B de código del plugin en flota puede medir el baseline sin saberlo; el ruido JIT de la tarea (17–31 s para el mismo trabajo) además lo disimula.

**Cómo aplicar:** para deploy manual en copia candidate-local, cambiar SOLO la fuente (hash stale dispara recompile en boot) o actualizar fuente+hash+Snippets.jar juntos como hace el pipeline deployer; verificar que el código nuevo corre con un canario de firma JFR (p.ej. "0 Pattern.compile bajo frames del exporter") en lugar de confiar en timings. Detalle completo: `10-projects/Echo Forge — Operación Real V2/artifacts/ECHO-FORGE-OVERVIEW-PERF-S01/DEPLOYMENT-MECHANISM.md`.
