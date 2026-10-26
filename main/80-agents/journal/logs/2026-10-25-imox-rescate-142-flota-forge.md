---
type: change_log
schema_version: 1
scope: "session"
created: "2026-10-25"
updated: "2026-10-25"
area: "[[Trading]]"
project: "[[Estrategias IMOX — Forex y CFD con Echo Forge]]"
application:
entities: ["[[Estrategias IMOX — Forex y CFD con Echo Forge]]"]
related: ["[[IMOX — Rescate 142 en flota Forge (2026-10-25)]]", "[[Echo Forge — Operación Real V2]]"]
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: "local"
load_policy: "manual"
indexable: false
index_priority: "never"
tags: ["kind/change-log", "scope/session"]
---

# Rescate 142 en flota Forge y registro en el proyecto IMOX

## Cambio

Se ejecutó la recuperación forense del material NDX SQX 142 en Zeus/Hera/Kronos (solo lectura de orígenes) y se creó [[IMOX — Rescate 142 en flota Forge (2026-10-25)]] como registro canónico del inventario, clasificación y preservación. El proyecto actualizó estado actual, bitácora (entrada 2026-10-25), tarea de inventario marcada DONE y campo `updated`. Hallazgos: tres pools disjuntos (Zeus 727 G1 ya ingestado por Forge; Hera 555 G2 y Kronos 1091 NDX_W3/G4 nunca ingestado), marca «highprecision» = `CrossCheck_HigherPrecision` embebida, y ausencia de evidencia de G3/G5/G6. Preservación en MinIO `sqx-strategies/recovery-imox-142/20261025/` (15 tars ~1,71 GB verificados por tamaño+ETag/MD5 15/15, 10 manifiestos con SHA256 por archivo) y staging de import para Forge sin despachar.

## Validación

Clasificación por contenido (bloques `key=` de `strategy_Portfolio.xml` contra universos `use=true` extraídos de los `.cfx` reales de flota; universos G1/G2/G4 idénticos entre hosts, G1 y G4 byte-idénticos). Integridad de preservación verificada listando el prefijo en destino (25 objetos) y comparando tamaño+ETag contra MD5/SHA256 calculados en cada host. Echo PROD consultado RO (0 promotions, 0 strategy versions). Orígenes SQX intactos; temporales de sesión eliminados de los 3 hosts; sin cambios en Forge/Echo/workers ni despachos de ningún tipo.

## Rollback

Eliminar el prefijo MinIO `recovery-imox-142/20261025/` (25 objetos), la nota [[IMOX — Rescate 142 en flota Forge (2026-10-25)]], la entrada de bitácora 2026-10-25 y revertir estado/tarea/frontmatter del proyecto. Los orígenes nunca se modificaron, por lo que no hay rollback del lado flota.
