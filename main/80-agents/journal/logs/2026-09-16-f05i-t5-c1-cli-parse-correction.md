---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]"
  - "[[Echo Forge — Factory V2 Completion]]"
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

# 2026-09-16-f05i-t5-c1-cli-parse-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - [[Echo Forge — F-05-I Cohesive release and read surfaces]]: `## 📊 Estado actual` con la entrada de la corrección manager C1 de T5 (causas, fix, SHA `cbf520b`); tabla `## 🧱 Entrega de desarrollo` y tarea F05I-T5 actualizadas con la corrección (T5 permanece `[r]` Review, manager review pending de `cbf520b`); nueva entrada en `## 📆 Bitácora`.
  - [[80-agents/journal/agent-runs/2026-09-16-zcode-glm-5.3-flash-f05i-t5-c1-cli-parse-fix.md]] (nuevo, materializado vía `materialize_schema_note.py`): agent_run [[ZCode]] × GLM-5.3-Flash del segmento de corrección F05I-T5-C1.
  - Repo `xKoRx/symphony` (fuera del vault): commit `cbf520b9663fa3c1a3a927c27bd7240b521446bf` con `sqx/cmd/sqx-flowkit/inspect.go` e `inspect_test.go` (369 inserciones / 31 deletions).

## Motivo

- Corrección manager F05I-T5-C1 (SOURCE REVIEW de T5 @ `eed8000`): (1) `flag.ExitOnError` en los FlagSets inspect ejecutaba `os.Exit` dentro de `flag.Parse`, saltándose writers inyectados y el stderr contractual `2:INVALID_ARGUMENT:`; (2) la sintaxis frozen `run get <FlowRunRef> --ranking name` fallaba porque el paquete flag deja de parsear tras el primer positional; (3) help de grupos y leaves incoherente (exit 2, o usage default del paquete flag por stderr).

## Fuentes usadas

- Misión manager F05I-T5-C1 (defectos y tests obligatorios 1–8).
- SPEC [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]] (§Read surface contract, §Exit codes, §C1.6).
- Estado vigente de [[Echo Forge — F-05-I Cohesive release and read surfaces]] y repro local contra el binario de `eed8000`.

## Resolución aplicada

- En `inspect.go`: helper `newInspectFlagSet` (ContinueOnError + salida del paquete flag suprimida) para los seis FlagSets inspect; `exitForFlagError` traduce `flag.ErrHelp` a usage stdout exit 0 y el resto a `emitError` 2:INVALID_ARGUMENT; parser puro `parseRunGetArgs`/`firstContractualPositional` implementa el orden frozen de `run get` (ref contractual aislado, tail de flags, positional extra rechazado, validación de ref pre-boot); constantes de uso contractual; grupos campaign/run/strategy responden `-h`/`--help` en stdout exit 0. push-output conserva su `ExitOnError` brownfield.
- En `inspect_test.go`: 7 funciones de test nuevas (contrato unknown-flag por superficie, parsing C2 por helper puro, pre-DI `latest --ranking`, `--ranking` sin valor, help grupos, help leaves, guard AST sin `flag.ExitOnError`/`os.Exit` en inspect.go); verificado que FALLAN contra `eed8000` en worktree del baseline y PASS post-fix.

## Validación

- gofmt OK · `go test ./sqx/cmd/sqx-flowkit/...` PASS · `-race` PASS · `go vet` PASS · `go build` paquete PASS · `go test ./sqx/core/releasematrix/... ./sqx/core/forge/...` PASS · `git diff --check` OK · smoke binario (unknown flag contractual, 12 superficies help exit 0 stdout/stderr limpio, `release-matrix` byte-idéntico) · `go build ./sqx/...` global falla sólo en `sqx/tools` (BASELINE_KNOWN preexistente).
- Commit atómico `cbf520b` push normal fast-forward `eed8000..cbf520b`; HEAD remoto == local; `eed8000` y baseline `b57bfb2` ancestros; dirty ajeno `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` preservado; T1–T4 Done sin cambios; T5 Review; T6/T7 pendientes; F-05-I abierta; ningún gate físico marcado.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert cbf520b` en `xKoRx/symphony` restaura el comportamiento de `eed8000`; las notas del vault se reverten eliminando la entrada de bitácora/estado añadidas y este log.
