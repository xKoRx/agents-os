---
type: session_feedback
schema_version: 1
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Aranea]]"
project: "[[The Lab]]"
entities:
  - "[[Echo]]"
related:
  - "[[K — Final Correction and Gate D1 (Shot 3)]]"
severity: low
category: environment
load_policy: manual
indexable: false
tags:
  - kind/feedback
  - scope/session
---

# Feedback — D1 Echo Foundation Shot 3 (2026-09-23)

## Observaciones

1. **PG embebido requiere LD_LIBRARY_PATH no documentado.** El binario del PG desechable (`/tmp/echo-e08-pg/postgresql-17.11.0-…/bin`) falla con `libxml2.so.2: cannot open shared object file` salvo que se exporte `LD_LIBRARY_PATH=/tmp/echo-e08-pg/libs`. Ese requisito vive sólo en el entorno de los procesos que ya lo arrancaron (descubierto vía `/proc/<pid>/environ`). Costó un arranque fallido del PG del Shot 3. Sugerencia: anotar el par binario+libs en el Environment Contract o en un runbook de PG desechable (quizá ya cubierto por la memoria de suite sqx; no estaba visible para este flujo).
2. **Layout de módulos Go de v3 no es uniforme.** `v3/sdk/contracts` es módulo propio, `v3/sdk/postgres` pertenece al módulo `v3/sdk`, y `go build ./...` desde la raíz del repo no funciona con `go.work` ("directory prefix . does not contain modules"). Cada shot re-deriva esto por ensayo y error; un mapá de módulos (5 líneas) en el Environment Contract ahorraría el redescubrimiento.
3. **`gofmt -l v3/` reporta 5 archivos lab-worker preexistentes** (formatting noise en master). No es de D1 y no se tocó (scope congelado), pero cualquier gate futuro que use `gofmt -l` como aserción dura va a tropezar con ello; moverlo a su propio fix de higiene.

## Lo que funcionó bien

- Mandato con scope congelado explícito + reproducers físicos del Shot 2: la corrección fue quirúrgica (diff de 4 archivos) y la demostración rojo/verde fue directa.
- Continuidad de evidencia A→K en la carpeta D1: cada shot pudo verificar el anterior sin confiar en sus claims.
