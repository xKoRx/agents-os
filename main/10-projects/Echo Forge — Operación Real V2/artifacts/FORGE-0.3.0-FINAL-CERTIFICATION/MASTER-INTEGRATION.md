# MASTER-INTEGRATION — Echo Forge 0.3.x (2026-10-18)

## Veredicto

**MASTER_INTEGRATION_PASS** — HEAD `492a271` (master == origin/master, push FF sin force), árbol limpio al construir la release canónica 0.3.1, `vcs.modified=false` verificado en los 3 binarios.

## Revisión de ramas contra el HEAD autorizado `4bb1ca0c`

Refresh físico 2026-10-18 (`git fetch` + `rev-list --count master..<branch>`):

| Rama | Exclusivas | Detrás | Decisión |
|---|---|---|---|
| feat/retester-producer-snapshots | 0 | 105 | Contenida: sin acción |
| feat/sqx-version-selector | 0 | 37 | Contenida: sin acción |
| feature/robust-selection-v2-hera-e2e | 0 | 43 | Contenida: sin acción |
| feature/robust-selection-v2-shot1 | 0 | 44 | Contenida: sin acción |
| fix/group-chaining-artifact-cohort | 0 | 49 | Contenida: sin acción |
| fix/ndx-canonical-instrument | 0 | 107 | Contenida: sin acción |
| fix/watcher-import-intake-deadline | 2 (a95ef2c, 509a10f) | 111 | **NO MERGE** (abajo) |

**NO se hizo merge masivo de ramas históricas.**

## Rama divergente del watcher — análisis de los 2 commits exclusivos

- `509a10f` (SQX_WATCHER_INTAKE_DEADLINE): **YA ESTÁ EN MASTER** — `sqx/activities/watcher/import_intake.go` contiene `intakeDeadline()` con la misma env y default 2m intacto. Verificado por grep en HEAD.
- `a95ef2c` (SQX_WATCHER_DISABLE_AUTO_UPGRADE): **NO está en master y NO es necesaria** — el patrón certificado del watcher candidate-local corre el binario desde `Temp/sqx-watcher` y la condición existente `strings.Contains(execPath, "/Temp/")` ya desactiva el watchdog (demostrado en producción: el watcher w9 corrió 2h+ y el w10 igual). Mergear traería 111 commits de base antigua sin contenido material nuevo.

## Commits efectivos incorporados (fix Magic Number + cableado warnings)

- `d67244b` fix(mt5): identidad MagicNumber 64-bit de punta a punta — exporter-plugin `enforceMagicWidth` (int→long, fail-closed 0/>1 declaraciones, idempotente; 5 regresiones simulador), `magicreadback.FromHTMInputs` (mágica EFECTIVA del HTM), gate `mt5_reconcile_v1` (HTM==sqx.strategy_magic, CONTRACT_CONFLICT non-retryable en asignación ausente/input ausente/mismatch; corre ANTES de cualquier escritura durable), puerto `capabilities.MagicAllocationReader` + wiring `durable.Magic`, registro de la activity `evaluate_strategy` (deep_warnings_shadow.v1, loader/wfm nil por contrato congelado, camino standalone, veredicto informativo). 9 archivos, +405/−11.
- `66dd8cd` chore: gitignore `sqx/exporter-plugin/target/` (Go buildvcs cuenta untracked como `vcs.modified=true`; causa del stamp defectuoso de 0.3.0).
- `492a271` chore(release): manifest 0.3.1.

## Regresiones

- Suite completa `go test` de sqx (74 paquetes): PASS excepto el conjunto de fallos PREEXISTENTES idéntico al baseline histórico documentado (2026-09-23, "16 preexistentes, 0 nuevos"): gate `TestFromSQX_AuthenticRERUN5SQX` exige env `SQX_AUTHENTIC_FIXTURE` (fixture RERUN-5 no disponible en Daedalus; FAIL-por-diseño), y `TestDecisionStore_ListFlowRunSelectionDecisions` + 4 tests de workflows que fallan idénticos en master limpio (contaminación de suite paralela; en aislamiento pasan con y sin el cambio). go vet limpio. gofmt en archivos tocados.
- Simulador del plugin: 11/11 checks OK (6 previos + 5 nuevos de enforceMagicWidth).
- Build producción del plugin contra SDK SQX local Build 144: OK, JAR 52 clases, `unzip -t` OK.

## Contratos congelados

Intactos: allocator de mágicas (sin tocar), Money Management (sin tocar), robust selection (sin tocar), schema durable, flujos del funnel. El único cambio de comportamiento: (1) el MQ5 publicado declara `input long MagicNumber` (mismo valor durable), (2) el reconcile exige igualdad HTM-efectiva==durable antes de persistir, (3) `evaluate_strategy` queda registrada y ejecuta en shadow sin tocar la selección.
