---
type: session
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — E1 Fee Model Conformance W1-q 2026-10-31]]"
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-31-polymarket-w1q-e1-conformance-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Cerrar W1-q: conformidad **offline** del modelo documentado de fee (`fee = C × rate × p × (1 − p)`, sólo `e = 1`) con fixtures sintéticos, reutilizando `FeeSchedule`/economics y sin framework paralelo. Sin piloto, gate, capturas, OOS, L ni dinero.

## Contexto cargado

- Bootstrap AGENTS OS en cold start (constitución, perfil global, memoria interna global, índice de skills, registro de routers) y entidad [[Polymarket Engine — MVP]]; el registro de routers no tiene fila para el área Personal, así que el resultado es DEFAULT sin router de dominio.
- Fuentes heredadas ya aceptadas: [[Research — Fee Formula Documentary W1-p 2026-10-31]] (fórmula, unidades, precisión no adjudicada, cobro por lado, roles, límites del gap U-02) y [[Research — Target Fee Inventory W1-o 2026-10-31]].
- Code scout en modo `inline-fallback` (`dispatch_id=w1q-e1-fees`): mapa de `FeeSchedule`/economics, efectos laterales de tests y límites de redondeo y elegibilidad, sin añadir framework.

## Trabajo realizado

- **Hallazgo de partida**: la semántica existente **ya coincidía** con el modelo documentado en `e = 1` (`rate·p^e·(1−p)^e·take`); el desajuste estaba en tres propiedades que el encargo exigía separadas: exactitud, elegibilidad y roles/lados de cobro.
- **Seam mínimo**: `exactCost` compartido + `DocumentedE1Cost` (exacto, `e ≠ 1` falla cerrado con `KindUnsupported`) en `internal/regimes/schedule.go`; `DocumentedRole`, `DocumentedE1Quote` y `BuildQuoteDocumentedE1` en `internal/economics/scheduled.go` (premisa `takerOnly` explícita, débito BUY `notional + fee`, neto SELL `notional − fee`). El legacy (`LevelCost`, `TRUNCATE_6DP`, `BuildQuoteScheduled`) queda intacto.
- **Finding real de la revisión de fuente**: la rama MAKER no validaba el dominio de precio de los takes consumidos (`WalkSideDetailed` no valida precios), así que un book fuera de `(0,1)` podía volver como quote MAKER resuelto. Corregido moviendo la validación antes de la rama de rol, reutilizando la aritmética del `FeeSchedule`, con el rechazo clasificado `KindInvalidInput`; regresión MAKER × 3 premisas × 4 precios × BUY/SELL añadida.
- **Ajuste de honestidad**: el helper `w1qVenueBand` pasó a `w1qHypotheticalBand` y el intervalo `[floor5, ceil5]` dejó de presentarse como lo que el venue podría cobrar: es banda **hipotética** de modelado.
- **Verificación y cierre**: preflight `safe: true`; focal `-run '^TestW1Q'` verde en los dos paquetes; suite de los dos paquetes verde; build exit 0; `gofmt -l` vacío; `diff --check` limpio; commit local `dee7a97` (4 archivos, sin push).

## Artifacts creados o modificados

- Informe canónico: [[Research — E1 Fee Model Conformance W1-q 2026-10-31]].
- Código: `internal/regimes/schedule.go`, `internal/regimes/w1q_documented_e1_test.go`, `internal/economics/scheduled.go`, `internal/economics/w1q_documented_e1_test.go` (commit `dee7a97`).
- Journal: este resumen, el feedback de sesión, el agent run, el change log de entidad y el feedback del code scout (`dispatch_id=w1q-e1-fees`).
- Artefactos del shot: `validated-baseline/w1-q-e1-conformance-20261031/` (`implementation-ready.json`, `conformance.md`, `run-receipt.json`, `prereg-draft.md`, `scout-pack.json`).

## Memoria propuesta o creada

- No se creó memoria interna nueva: el delta durable de esta sesión es estado de proyecto y evidencia ya persistidos en el informe canónico, el agent run y el feedback; la única señal transferible (el hook que deniega lecturas de runbook y comandos inline) quedó en el feedback, que es donde debe vivir.

## Decisiones

- El modelo documentado se expone como **vía separada** (exactitud + `e = 1` + roles) y **no** se conecta a piloto, gate ni estrategia.
- `e ≠ 1` falla cerrado **sólo** en la vía documentada: el contrato legacy conserva su exponente general y sus pruebas.
- El redondeo del venue se trata como **no adjudicado**: se conserva el valor exacto y, en tests, una banda hipotética declarada; `TRUNCATE_6DP` no se renombra como regla del venue.
- El maker paga `0` **sólo** con la premisa `takerOnly` establecida; sin ella su fee queda desconocido, nunca `0`.

## Pendiente

- Recepción point-in-time de versión y fuente del parámetro antes de cada decisión; precisión, unidad y premisas con fuente fechada; clasificación exploratoria frente a OOS antes de que exista contenido; criterios dados sin tuneo.
- **L** la elige el Owner de forma explícita —incluido si el código actual la incluye o la excluye como literal v1— y no puede derivarse de resultados; la referencia de detección existente no se cambia.
- Aprobación de piloto o gate: aparte. Para seguir offline no hacen falta cuenta, micros, tokens ni fondos.
