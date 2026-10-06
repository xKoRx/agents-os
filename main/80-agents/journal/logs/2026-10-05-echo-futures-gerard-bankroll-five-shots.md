---
type: change_log
schema_version: 1
scope: session
created: "2026-10-05"
updated: "2026-10-05"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities: []
related:
  - "[[Echo Futures]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-05 — Echo Futures: programa Gerard y bankroll en cinco shots

## Cambio

- Tipo: actualización de alcance y creación de plan/mandato.
- Entidad: [[Echo Futures]].
- Artefactos: [[BTG-PLAN]] y [[BTG-S01-SUBMANAGER-PROMPT]].
- Estado anterior: Backtester V1 cerrado/certificado; Stage 2 real Gerard siguiente; Stage 3 campaña económica como etapa futura separada.
- Estado actual: Owner encarga resultado combinado en máximo cinco shots: S01 submanager LOCAL persistente hasta hacer funcionar lo existente; S02 diseño económico; S03 implementación; S04 adversarial LOCAL independiente; S05 corrección/certificación. Se mantiene la dependencia de validar histórico real antes de campaña.

## Motivo

Registrar el mandato explícito Owner y dejar el primer despacho completo sin modificar producto ni interferir con D6. El bankroll, la moneda y el precio por cuenta conservan la ambigüedad literal; USD 5.000 / USD 120 es un supuesto explicativo y no un dato confirmado.

## Fuentes usadas

- Mensaje Owner 2026-10-05 America/Santiago y mandato adjunto Stage 2.
- Refs GitHub consultados: Agents-OS 7435fa519b54c3601fb5f8e8f440cb8f54ad3d1c; Echo master 372af59a7b83604781346613da01e3d510ea1360; Backtester cd451972b242c8933321e03001decd4b6d778c61; D6 d08a30ce9815f820fda7132e20dc42cc345eb8e8.
- Cierre BT-S04, SPEC S1, SPEC GerardMM, Technical Project Manager y contrato de ambientes.

## Resolución aplicada

- El mandato nuevo reúne Stage 2/3 sin iniciar prematuramente la implementación de campaña.
- Retiros cobrados y PnL se distinguen; cuatro retiros máximos y reinversión son requisitos Owner.
- Identidad Gerard exacta, configuración efectiva y dataset físico permanecen por probar LOCAL.
- El plan y prompt no equivalen a una ejecución o gate aceptado. La sesión Primary Manager permanece abierta.

## Validación

- Materialización mediante materialize_schema_note.py vigente para doc, prompt y change_log.
- Revisión de referencias, secciones obligatorias y secuencia exacta de cinco shots.
- Inspección de HEADs GitHub y autoridades documentales; no ejecutados Go tests, backtests ni acciones de infraestructura.
- Revisión de diff limitada a documentación. La revisión automática rechazó actualizar master: solicitó una rama/PR revisable porque no había autorización explícita para mover la rama predeterminada. No se reintenta por otra vía; publicación acotada a docs/backtester-gerard-bankroll-five-shots-20261005 e integración a master pendiente.

## Compartibilidad

- Scope: local.
- Sin secretos, credenciales, dumps ni instrucciones para egress físico.

## Rollback

Revertir exclusivamente el commit documental de este cambio si el Owner reemplaza el mandato; conservar intactos Backtester certificado y D6.
