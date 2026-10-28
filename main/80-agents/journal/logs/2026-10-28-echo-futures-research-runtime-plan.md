---
type: change_log
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Echo]]"
project: "[[Echo I+D — Futures]]"
application:
entities:
  - "[[Echo Futures]]"
  - "[[Echo I+D — Futures]]"
related:
  - "[[FUT-R01-RESEARCH-MANDATE]]"
  - "[[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]]"
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

# Echo Futures — prompt de investigación y diseño de integración

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - Echo I+D — Futures.md y Echo I+D — Cobertura Futures.md.
  - FUT-R01-RESEARCH-MANDATE.md, versión 3.
  - Echo Futures.md y artifacts/runtime/EF-BACKTEST-RUNTIME-INTEGRATION-PLAN.md.

## Motivo

- Owner confirma USD 4.000 Futures / aproximadamente USD 2.000 Forex separados, ficha simple Strategy y superposición libre entre 5 challenge y 5 funded. Solicita el prompt completo corregido del frente 2 y avanzar planificación/diseño del frente 1 para integrar Backtester con el nuevo runtime y reproducir sesiones.
- Se conserva el contexto Owner de pruebas PROD; la última evidencia documental recuperada acredita una ventana DEV RO anterior. No se reemplaza una declaración por otra ni se adjudica readiness física.

## Fuentes usadas

- Mensaje Owner del 2026-10-28 y decisiones vigentes de FUT-R01.
- Agents-OS/master f844162d3305e6ce9441dd11598aa1a69e753164, reconciliado antes de publicación con 6dbd64d12a4818fe62f8bf947692bcc74cd8e0c6; autoridades R6, GOD-05, WINDOW-CARD-PRD6 y planner Lab.
- Echo Lab ae1b09bc10370806f7648f076c5fa0825c9efa4e y runtime bcffcf310c5825cd7b1c434158ee160a93b45c47; ancestro d74b652500e673fc2bf4289f9f195f11960ba26e. Fuentes concretas y alcance en el nuevo plan.
- Workers acotados de lectura fuente, autoridad y diseño de investigación; revisión documental técnica y de gobierno. No pruebas físicas; consumo Pro no comprobado = UNKNOWN.

## Resolución aplicada

- Prompt v3 autocontenido y orientado a evidencia externa: tres módulos, ficha Strategy de tres bloques, MM separado, ambos escenarios del payout USD 3.000 y límites de ejecución. Deep Research completo preparado, no ejecutado.
- Superposición 5+5 deja de ser pendiente. Retorno interno/read-only se separa del encargo externo.
- Plan candidato de integración bajo Echo Futures, sin nuevo planner ni reactivación de S05. Diferencia lógica compartida, replay de decisiones, reconstrucción contable y simulación de fills; identifica módulos/MM/policies, divergencia de ramas, caja histórica y simultaneidad no demostrada.
- Revisión independiente incorporada: evitar circularidad al usar revisiones contables como input y resultado; no atribuir al venue un modelo de latencia no acreditado.
- Se prepara mandato read-only de Hefesto y secuencia de hitos. No ejecución, implementación, compras, despliegue ni cierre formal.

## Validación

- Creación desde plantillas canónicas mediante materialize_schema_note.py; lint estricto de los seis documentos: ERROR=0, WARN=0, notes_scanned=6.
- Revisión de fuentes y de coherencia del plan. No se corrieron pruebas de producto, backtests, campañas ni replay.
- Publicación atómica en Agents-OS/master condicionada a reconciliar HEAD y verificar contenido remoto; no ramas/PRs ni force.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** documentación interna del proyecto, sin credenciales ni secretos. El prompt externo contiene únicamente la cápsula de contexto necesaria.

## Rollback

- Revertir sólo este cambio documental mediante un commit posterior sobre master, preservando trabajo concurrente. No modifica source, binarios, datos, cuentas ni resultados previos.

