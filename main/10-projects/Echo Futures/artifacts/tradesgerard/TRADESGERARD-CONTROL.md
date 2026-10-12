---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-CONTROL

## Propósito

Fuente única de estado de la preparación TradesGerard, etapa A del mandato GOD LOCAL del Owner, recibido el 2026-10-12. Estado técnico inicial: IN_PROGRESS; no READY_FOR_GLM, aceptación final Owner pendiente. Etapa B corresponde a GLM-5.3-Flash y no se lanza automáticamente.

## Contenido

### Autoridad y límites

El mandato vigente autoriza diseño técnico ordinario, desarrollo offline por TOPs, verificación independiente y corrección. El manager coordina y documenta; no escribe ni integra código, scripts, indicadores ni tests. Sin merges productivos, deploy, servicios, egress trading, compras/resets reales ni reconstrucción de cuentas personales. La aceptación final pertenece al Owner. BTG-PLAN, BTX-PERF y D1–D6 conservan sus gates históricos.

Inputs inmutables: caja inicial USD 5.000; compra individual USD 120 a demanda; reinversión sólo de efectivo acreditado; una cuenta operando y un ciclo agregado; turno persistente hasta target/límite/fallo/bloqueo/sesión; target ordinario evaluación USD 870 netos; pausa interna −USD 1.000 sin reset; NY flat/cancelado al cierre; funded sin heredar 870 ni consistencia de evaluación. Retiros brutos candidatos 2.250/2.300/2.500/3.000.

### Trabajo y evidencia vigente

| Entrega | Estado | Responsable / siguiente acción |
|---|---|---|
| Inventario real y diseño acotado por propietarios | IN_PROGRESS | TOP inventory, lectura física; devolución pendiente. |
| Perfil GAU50 versionado con fuentes oficiales | IN_PROGRESS | TOP prop_profile; separar hechos/supuestos/UNKNOWN. |
| Catálogo finito con todos los IDs | IN_PROGRESS | TOP catalog; original adjunto es snapshot de autoridad, catálogo de trabajo pendiente. |
| Motor/composición/campaña/lote compacto | NOT_IMPLEMENTED_THIS_INITIATIVE | Un integrador posterior al diseño; capacidades heredadas aún bajo inspección. |
| Verificación independiente del delta exacto | NOT_RUN | TOP adversarial fresh-context tras freeze. |
| Manual actualizado, evidencia A y prompt GLM | PENDING | Después de implementación y prueba, sin inventar flags ni rutas. |

Harness local: tres despachos físicos aceptados por collaboration.spawn_agent, TOPs fresh-context ONE-SHOT con modelo solicitado `gpt-6.1-sol`; modelo servido UNKNOWN. No se asume GLM disponible en el mismo harness. No se consume CLOUD Pro.

Baseline de source informado por inspección TOP: repo `xKoRx/echo`, checkout relativo a workspace Aranea `work/btx-perf-last-20261010/integrator/echo`, rama `codex/btx-perf-last`, HEAD `873f5f1c7df25086271af1de1896095f1cade2a9`, limpio; origin apunta a clon local. Es identidad source, no build nuevo ni certificación actual. Inventario completo pendiente. Ningún componente no inspeccionado se considera ausente.

### Recursos y gates

Preflight disco del workspace: filesystem 146G, usado 127G, disponible aproximadamente 12G (2026-10-12). Antes de ejecutar: reservar al menos 8 GiB libres, un escritor de producto y una campaña a la vez; TOP debe fijar límites medibles de temporales, outputs y logs según preflight de su ruta real. No limpieza de corpus/caches/releases/trabajo ajeno. Sin barrido de investigación completo en A.

El gate READY_FOR_GLM exige demostrar cada fila de §10 del mandato, no sólo interfaces o pruebas unitarias del autor. Fixtures deterministas deben etiquetarse; smoke real sólo con corpus válido y ventanas explícitas. Cobros pendientes no son caja, datos truncados no son checkpoints, hashes no reemplazan replay detallado. El coverage nuevo mínimo es 95% sin cambiar denominadores heredados.

### Siguiente acción

Revisar las tres devoluciones, fijar diseño acotado y perfil con UNKNOWN visibles, despachar un único TOP integrador; verificar luego sobre commit/build exactos mediante otro TOP independiente. Corregir gaps materiales antes de readiness; si existe bloqueo real, conservar causa, evidencia y continuidad.

## Fuentes

- Mandato Owner: `ECHO FUTURES — GOD LOCAL: BACKTESTER PARA TRADESGERARD`, PROMPT_VERSION 1, snapshot de entrada adjunto a la conversación de 2026-10-12.
- [[Echo Futures]] y `xKoRx/echo:v3/backtester/README.md` (manual existente, inspección TOP).
- `80-agents/skills/technical-project-manager` se resuelve en `30-resources/agents/skills/technical-project-manager/SKILL.md`; el mandato actual prevalece en modelo Sol 6.1, autonomía interna, alcance y ausencia de cuota de shots.
