---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
application:
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
  - "[[Echo — Live Platform V1]]"
related: []
aliases: []
confidence: verified
source_session: "2026-09-16 E-06 TOP refresh liveness erratum"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-16-echo-e06-refresh-liveness-erratum

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md`
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md`
  - `xKoRx/echo` `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/{SPEC,PLAN,TASKS,VERIFICATION}.md` (docs-only; SPEC v1.2.2)

## Motivo

- **Sistema 2 update:** §7.2a.4 v1.2.1 exigía «MUST republicar al menos cada 5 s» con el sitio de refresh en `OnTick`; MQL5 no garantiza ticks cada cinco segundos ⇒ el contrato contenía una garantía temporal irrealizable. El estado vigente congela la semántica de refresh del Manager con CASE B y encoding v1 intactos.

## Fuentes usadas

- SPEC v1.2.1 @ `336c723ba46a7c04a1a6cc4390c6d5a4f15b56d7` (contrato `662c0dcef9fb17a5308ddcb974eabb6074c748aa`)
- Decisión Manager 2026-09-16 (erratum liveness, frozen, 7 puntos)
- MQL5 `OnTick`/`OnTimer`/`EventSetTimer` contract (sin garantía de frecuencia de ticks)

## Resolución aplicada

- SPEC v1.2.2 §7.2a.4: `OnTimer` existente realmente activado con período ≤5 s preferido; prohibido modificar `EventSetTimer`/crear timer; `OnTick` oportunista con 5 s como intervalo mínimo entre publicaciones (no frecuencia); sin tick ni timer compatible sin promesa de liveness continua; expiración 15 s fail-closed `SUSPENDED + UNKNOWN`; recovery §6 con nueva atestación matching; ninguna actualización de `ts` desde Echo/Bridge/Gateway/config; cero cambios de trading
- Scanner §7.2a.5: ausencia de sitio de refresh deja de ser fail-closed en export
- Tests AC-37a…d (contractual + físico; PHYSICAL gated por Version con inyección §7.2a.5)
- Verdict: `E06_PLANNING_READY_FOR_IMPLEMENTATION_REVIEW`
- Echo HEAD: `acf996ad043f87d6bbe6ae7b6190d1eb801e908a` (contrato `28afc47faf72b70e67b141b39224b8674f98458b`; old `336c723ba46a7c04a1a6cc4390c6d5a4f15b56d7`)
- Product source `v3/**` delta vs master = 0; Forge bytes = 0

## Validación

- Diff `5dd998f1...acf996ad` names: sólo `specs/` (4 docs E-06 + fila catálogo SPECS.md previa)
- Push FF `336c723b..acf996ad` a `origin/feature/e06-reference-enrollment-binding`
- `origin/master` intacto `5dd998f1`; merge-base sin rebase

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina como contrato, sin memoria interna

## Rollback

- Revertir las notas del vault y los dos commits docs-only de Echo si el Manager rechaza el erratum de liveness.
