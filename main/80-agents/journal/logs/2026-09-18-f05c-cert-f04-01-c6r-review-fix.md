---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
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

# 2026-09-18-f05c-cert-f04-01-c6r-review-fix

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-18 — Corrección de revisión C6R` con veredicto `SOURCE_READY` + actualización de `Estado de entrada` + actualización de `Próxima tarea única recomendada para NORMAL`; el source queda listo para Release Authority)
  - `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-f05c-cert-f04-01-c6r-review-fix.md` (creado)
  - Repo `xKoRx/symphony` — rama `codex/f05-build6182-parser-cert` @ `c1d24c1…` en origin (5 archivos, commit adicional sobre `bcf67be…` sin reescritura; cambio de repo documentado aquí, no en el vault)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C6R`: la revisión independiente del manager sobre el source fix C6 (`bcf67be…`) identificó cuatro pendientes (R1 diagnóstico incorrecto con allow-list stale inline en `parse.go:158`, R2 SPEC-PARSER §3.2 sin 6182, R3 falta de modo obligatorio de release para el fixture externo, R4 coverage 81.6% < 95% de política) y el mandato ordenó cerrarlos exclusivamente, sin repetir certificación física, compatibilidad ni adquisición, y sin campañas, releases ni deployments. Prohibiciones respetadas: sin tocar `types.go`, `crosscheck.go`, `CORPUS.md`, reconcile, Temporal ni fixtures existentes; sin descargar de MinIO, sin credenciales, sin copiar los 13 MB al vault; sin merge, sin release, sin rollout, sin RERUN-4.

## Fuentes usadas

- Mandato maestro F05C-CERT-F04-01-C6R (texto de la misión con hallazgos R1–R4).
- Registro C6 (`~/aranea/work/f04-cert-f04-01-c6/certification-record.md`) y estado vigente del backlog (delta C6).
- `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/SPEC-PARSER.md` §3.2/§3.3 y `CORPUS.md` §5.6 @ `bcf67be…`.
- Fixture auténtico re-verificado: copia privada de `daedalus` con 13074872 B y SHA256 `21917e14…8b5c` == durable.
- Perfil de coverage del paquete (`go test -coverprofile`) para dirigir los tests enfocados a los bloques descubiertos.

## Resolución aplicada

- R1: diagnóstico de build ausente en `parseTable0` pasa a `"server row with a build from the certified matrix"` (sin duplicar la allow-list; única autoridad `isSupportedBuild` en `types.go`); test nuevo `TestParse_MissingBuildRowFailsClosed` congela el error tipado, el observado `missing build row` y la ausencia de cualquier build inline; política de aceptación sin cambios.
- R2: SPEC-PARSER §3.2 incorpora 6182 a los builds certificados (único cambio contractual; CORPUS y semánticas congeladas intactos).
- R3: modo obligatorio de release `SQX_MT5_REQUIRE_B6182_FIXTURE=1` en `build6182_test.go` — variable ausente, archivo inexistente, size incorrecto, SHA256 incorrecto y test omitido → FAIL (nunca skip); skip explícito conservado en desarrollo; sin descargas automáticas ni credenciales; bytes consumidos sólo de la ruta provista; tabla de decisión congelada por `TestBuild6182_ReleaseModeDecisionTable`; el release runner debe ejecutar el paquete completo sin filtros `-run` exigiendo 0 skips.
- R4: coverage medida en condiciones comparables (worktree temporal del baseline, eliminado sin residuo): `a440ac4` = 81.5% / `bcf67be` = 81.6% — déficit preexistente del paquete; cerrado con 18 tests de contrato enfocados en `contract_test.go` (diagnósticos tipados, MISSING/INVALID por label, flags degenerados, gramáticas y overflow fail-closed, errores por celda de orders/deals, gaps estructurales T0/T1, payload UTF-16 impar, desbalance in/out bidireccional, timezone inválida); residual ~1% documentado como ramas defensivas inalcanzables, sin tests artificiales ni excepciones inventadas.
- Delta C6R en el backlog con resultado, evidencia, commit, tests, coverage y próximo gate (Release Authority).

## Validación

- Suite enfocada 6182 con bytes auténticos: 11/11 PASS (6182 aceptado; 6181/6183 → `ErrBuildNotSupported` con build observado; 7/7 crosschecks PASS; encoding/estructura nunca parciales).
- Paquete completo modo release con fixture auténtico: 53 PASS / 0 SKIP / 0 FAIL, coverage **99.1%**; modo release sin fixture: exit 1 con 7 FAILs tipados y 0 skips; modo release con SHA incorrecto: exit 1 con diagnóstico got/want; modo dev sin fixture: 46 PASS + 7 skips explícitos (sólo auténticos) + 0 FAIL (regresión histórica limpia).
- `gofmt -l` limpio en `sqx/adapters/mt5/`; `go vet ./sqx/adapters/mt5/... ./sqx/core/...` OK; `go build ./sqx/adapters/... ./sqx/core/...` OK; fallos preexistentes de `sqx/tools` (main redeclarado) y gofmt de `sqx/activities/worker/` demostrados idénticos en HEAD pristine vía stash (fuera del allow-list).
- Git: commit adicional único `c1d24c1bbfb1819739e173d16593eb15f1afae49` sobre `bcf67be…` (sin reescritura, sin force-push, sin merge); push a origin con read-back verificado (`git ls-remote` == HEAD local); diff limitado a los 5 archivos permitidos; sin secretos ni URLs firmadas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Repo: el commit C6R es aditivo sobre la rama de certificación no mergeada; revertir = `git revert c1d24c1` o ignorar la rama remota (sin efecto sobre `codex/f05-release-prep` ni releases). Vault: el delta C6R es append-only sobre el backlog; revertir = eliminar el delta C6R y restaurar el párrafo de estado y la sección de próxima tarea previos (historial C6 intacto). El modo release es opt-in por variable de entorno: sin `SQX_MT5_REQUIRE_B6182_FIXTURE=1` el comportamiento de desarrollo (skip explícito) queda exactamente como en C6.
