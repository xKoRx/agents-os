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
source_session: "2026-09-16 E-06 TOP transport contract correction"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-16-echo-e06-transport-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md`
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md`
  - `xKoRx/echo` `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/{SPEC,PLAN,TASKS,VERIFICATION}.md` (docs-only; SPEC v1.2.1)

## Motivo

- **Sistema 2 update:** v1.2.0 exigía escribir `{program_name, chart_ref, magic}` en una `GlobalVariableSet` irrealizable (`name`≤63, `value` double; `GlobalVariableTime` no es publicación; int64 magic no cabe en double). El estado vigente pasa a encoding v1 lossless con CASE B intacto.

## Fuentes usadas

- SPEC v1.2.0 @ `e8fba410347f6c60d036f9d03b2d0b1946d53e28`
- MQL5 `GlobalVariableSet`/`GlobalVariableTime` contract
- Forge READ ONLY `xKoRx/symphony` @ `0ddd4db` (`codex/f05-release-prep`); exporter blob `cfbd5b78`; WINDOWS-CONTRACT §4.1 (`OnInit critical error`)
- Freeze Manager CASE B (sin reabrir)

## Resolución aplicada

- SPEC v1.2.1: encoding `echo.attest.v1.<acct16>.<chart16>.<field>`; magic `mh`/`ml`; commit par; `ts` escrito; `chart_ref` obligatorio; inyección estructural post-`generate`+`assertNonZeroLots`
- Verdict: `E06_TRANSPORT_CONTRACT_READY_FOR_MANAGER_REVIEW`
- Echo HEAD: `336c723ba46a7c04a1a6cc4390c6d5a4f15b56d7` (contrato `662c0dcef9fb17a5308ddcb974eabb6074c748aa`; old `e8fba410347f6c60d036f9d03b2d0b1946d53e28`)
- Product source `v3/**` delta vs master = 0; Forge bytes = 0

## Validación

- Diff `5dd998f1...HEAD` names: sólo `specs/`
- Push FF `e8fba410..336c723b` a `origin/feature/e06-reference-enrollment-binding`
- `origin/master` intacto `5dd998f1`

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina como contrato, sin memoria interna

## Rollback

- Revertir las notas del vault y los dos commits docs-only de Echo si el Manager rechaza el encoding v1.
