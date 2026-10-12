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
| Inventario real y diseño acotado por propietarios | REVIEWED_FOR_IMPLEMENTATION | TOP inventory completo; mapa y decisiones en [[TRADESGERARD-CONTRACT]]. |
| Perfil GAU50 versionado con fuentes oficiales | RESEARCH_COMPLETE_SCENARIO_REQUIRED | [[TRADESGERARD-PROP-PROFILE]] distingue hechos, supuestos y UNKNOWN; no certificación comercial. |
| Catálogo finito con todos los IDs | DESIGN_AUDIT_RUNNING | `catalog.json` conserva53 IDs; TOP independiente revisa equivalencias antes del freeze. |
| Motor/composición/campaña/lote compacto | IMPLEMENTATION_RUNNING | TOP integrator_a, único escritor de source en rama aislada `codex/tradesgerard-platform-a`. |
| Verificación independiente del delta exacto | NOT_RUN | TOP adversarial fresh-context tras freeze. |
| Manual actualizado, evidencia A y prompt GLM | PENDING | Después de implementación y prueba, sin inventar flags ni rutas. |

Harness local: TOP inventory/prop_profile/catalog retornaron artefactos físicos; integrator_a implementa y contract_audit verifica el catálogo en ámbitos disjuntos. Todos fresh-context ONE-SHOT, modelo solicitado `gpt-6.1-sol`; modelo servido UNKNOWN. No se asume GLM disponible en el mismo harness. No se consume CLOUD Pro.

Baseline de source informado por inspección TOP: repo `xKoRx/echo`, checkout relativo a workspace Aranea `work/btx-perf-last-20261010/integrator/echo`, rama `codex/btx-perf-last`, HEAD `873f5f1c7df25086271af1de1896095f1cade2a9`, limpio; origin apunta a clon local. Es identidad source, no build nuevo ni certificación actual. Inventario completo pendiente. Ningún componente no inspeccionado se considera ausente.

### Recursos y gates

Preflight disco del workspace: filesystem 146G, usado 127G, disponible aproximadamente 12G (2026-10-12). Antes de ejecutar: reservar al menos 8 GiB libres, un escritor de producto y una campaña a la vez; TOP debe fijar límites medibles de temporales, outputs y logs según preflight de su ruta real. No limpieza de corpus/caches/releases/trabajo ajeno. Sin barrido de investigación completo en A.

El gate READY_FOR_GLM exige demostrar cada fila de §10 del mandato, no sólo interfaces o pruebas unitarias del autor. Fixtures deterministas deben etiquetarse; smoke real sólo con corpus válido y ventanas explícitas. Cobros pendientes no son caja, datos truncados no son checkpoints, hashes no reemplazan replay detallado. El coverage nuevo mínimo es 95% sin cambiar denominadores heredados.

### Siguiente acción

Recoger candidato del integrador y findings de auditoría del catálogo, verificar luego source/build exactos mediante TOP independiente del producto. Corregir gaps materiales antes de readiness; si existe bloqueo real, conservar causa, evidencia y continuidad. SDD source: `xKoRx/echo:specs/FEAT-TRADESGERARD-PLATFORM-A/`; nuevo worktree relativo a Aranea `work/tradesgerard-platform-a-20261012/echo`. Documentación Agents-OS en master con sincronización automática observada; no atribuir commits sync al manager ni afirmar push sin verificar.

## Fuentes

- Mandato Owner: `ECHO FUTURES — GOD LOCAL: BACKTESTER PARA TRADESGERARD`, PROMPT_VERSION 1, snapshot de entrada adjunto a la conversación de 2026-10-12.
- [[Echo Futures]] y `xKoRx/echo:v3/backtester/README.md` (manual existente, inspección TOP).
- `80-agents/skills/technical-project-manager` se resuelve en `30-resources/agents/skills/technical-project-manager/SKILL.md`; el mandato actual prevalece en modelo Sol 6.1, autonomía interna, alcance y ausencia de cuota de shots.
