---
type: runbook
schema_version: 1
scope: graphify
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[agents-os-graphify-maintenance]]"
  - "[[graphify-markdown-wikilink-and-backend-gaps]]"
aliases:
  - reindex bloqueado por deuda global
  - lint gate all-or-nothing
  - desbloquear update de Graphify
confidence: verified
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/graphify
  - project/agents-os
  - tech/agents-os
---

# reindex-bloqueado-por-deuda-global

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

- Reindexar Graphify cuando el gate de lint rechaza la corrida por findings que no pertenecen al delta de la sesión. Acredita el delta, congela la deuda ajena en el baseline y deja el índice fresco sin relajar el contrato.

## Precondiciones

- Los archivos que la sesión creó o modificó están escritos y son indexables.
- Se conoce la lista exacta de esos paths; el procedimiento no adivina el delta.
- `graphify-obsidian` está instalado y su caché es escribible; si el sandbox lo impide, resolver eso primero.

## Procedimiento

1. Acreditar el delta: `python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --strict <paths-del-delta>`. Debe salir `0/0`. Si falla, el problema es el delta y el gate está haciendo su trabajo: corregir y volver al paso 1.
2. Medir la deuda total: `lint.py --check`. Anotar `ERROR`/`WARN`.
3. Correr el gate: `lint.py --gate`. Si sale `GO`, saltar al paso 6.
4. Si el gate reporta `new=0` pero igual bloquea, el baseline está desactualizado o vacío: regenerarlo con `lint.py --emit-baseline > 80-agents/skills/agents-os-entity-lifecycle/lint-baseline-v1.json`. El baseline congela deuda **preexistente**; nunca se regenera para tapar un finding introducido por el delta, que ya quedó descartado en el paso 1.
5. Reconfirmar `lint.py --gate`: debe salir `GO` con `new=0`.
6. Reindexar con `graphify-obsidian update`.
7. Verificar descubribilidad por título exacto: `graphify-obsidian explain "<título creado o cambiado>"`.

## Validación

- `lint.py --strict <delta>` en `0/0` y `lint.py --gate` con `new=0`.
- `explain` por título exacto devuelve el nodo del delta.
- La cuenta de `ERROR` del baseline no creció respecto del paso 2.

## Rollback / recuperación

- El baseline anterior se recupera con `--emit-baseline` sobre el estado previo, o restaurándolo desde el journal del cambio que lo instaló. El índice es derivado: si queda inconsistente, se reconstruye con otro `update`; nunca se edita a mano ni se borra el grafo.

## Evidencia

- Seis sesiones con el mismo diagnóstico y deuda creciente (10 → 136 findings): [[2026-08-24-rio-component-context-graphify-feedback]], [[2026-08-26-skill-reindex-gate-graphify-feedback]], [[2026-09-01-crear-context-reindex-blocked-graphify-feedback]], [[2026-09-02-playmaker-graphify-gate-feedback]], [[2026-09-03-vpn-routing-reindex-gate-feedback]], [[2026-09-04-forge-campaign-schema-boundary-fix-graphify-feedback]].
- El mecanismo de baseline existía desde 2026-08-11 con cero fingerprints, así que el gate seguía fail-closed contra deuda ajena; se pobló el 2026-09-09 tras bajar la deuda de 32 a 9 errores.
