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
related: []
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

# 2026-09-16-f05i-t7-close-declarative-closure

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - Repo `xKoRx/symphony` (branch `codex/f05-release-prep`, commit `3d0e8c958765da23840e00bf1a0ac017fc47597a`, push fast-forward `0ddd4db..3d0e8c9`): `sqx/core/releasematrix/release-matrix.json` — fila `f05i-read-surface`: `implementation_sha` → `0ddd4db5435151c6bbbcc1550f3dfb35d708807e` (source aprobado, no el commit de cierre), `implemented` OPEN→DONE (`evidence_kind git`), `source_verified` OPEN→DONE (`evidence_kind tests`); released/deployed OPEN, physically_certified DEFERRED `CERT-F05-02` y cross_lane NOT_APPLICABLE intactos; otras 16 filas byte-intactas. `sqx/core/releasematrix/releasematrix_test.go` — `TestGuardF05INotDeclaredDone` reemplazado por `TestGuardF05ISourceVerifiedDeclaration` (13 invariantes); resto de tests íntegro.
  - [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]: párrafo de estado con el cierre (manager approval T7-A, commit de cierre `3d0e8c9`, veredicto, NOT PERFORMED/NOT RUN explícitos, gates CERT intactos, sin golden inventado) y nota de actualización en la descripción frozen de la fila `f05i`. Esta SPEC no congela comandos de test: la receta de persistencia vive en el proyecto.
  - [[Echo Forge — F-05-I Cohesive release and read surfaces]]: regex de persistencia del freeze T7 corregida `TestForgeCampaignResult|TestFlowRunResult` → `TestLoadForgeCampaignResult|TestLoadFlowRunResult` (familias reales; corrección de la receta de verificación, NO del source; T7-A recuperó la cobertura con ejecución suplementaria reportada PASS); T7 `[r]`→`[x]` Done; bullet de cierre T7-CLOSE en estado actual; tabla de entrega con veredicto final; progress 100; entrada de bitácora.
  - [[80-agents/journal/agent-runs/2026-09-16-zcode-glm-5.3-flash-f05i-t7-close.md]] (nuevo, materializado vía `materialize_schema_note.py`).
  - Este change_log (nuevo).

## Motivo

- El manager emitió `PASS — T7-A SOURCE / CONTRACT REVIEW APPROVED`; la misión F05I-T7-CLOSE ordena cerrar F-05-I sólo a nivel declarativo: convertir la evidencia aprobada en una declaración versionada y verificable de la matriz de release, sin re-auditar, sin features, sin certificación física, sin release ni deploy.
- La regex frozen de persistencia nombraba `TestForgeCampaignResult|TestFlowRunResult`, pero las familias reales son `TestLoadForgeCampaignResult*`/`TestLoadFlowRunResult*` (hallazgo menor T7-A); se corrige la receta documental para que futuras ejecuciones del gate cubran de facto esas familias.

## Fuentes usadas

- Mandato F05I-T7-CLOSE (baseline `0ddd4db`, allowed files, contenido exacto de evidencias, guard nuevo, validaciones, corrección de receta, STOP conditions).
- Evidencia T7-A: agent-run `2026-09-16-zcode-glm-5.3-flash-f05i-t7a-verification` y change_log `2026-09-16-f05i-t7a-verification-evidence`.
- Source del paquete `sqx/core/releasematrix` @ HEAD (`releasematrix.go`: tabla C1.5 de evidencia admisible, reglas DONE/DEFERRED) y estado del repo verificado con `git fetch`/`rev-parse`/`status`.

## Resolución aplicada

- implemented/source_verified de `f05i-read-surface` pasan a DONE con las autoridades de evidencia correctas por dimensión (git/tests), citando T1–T6 + F05I-PAGINATION-C2 + SHA `0ddd4db` + aprobación manager (implemented) y el agent-run T7-A con la lista completa de gates PASS incluidos los fallos honestos (build global `sqx/tools` FAIL/BASELINE_KNOWN; unshare no demostrado) (source_verified). Sin `certification_record` como sustituto de tests.
- Dimensiones físicas y las otras 16 capabilities sin ningún cambio (verificado por diff de nombres/orden y de campos no-state contra HEAD anterior).
- Guard temporal sustituido por el guard positivo de cierre que mecaniza las 13 invariantes de la declaración.

## Validación

- `go test ./sqx/core/releasematrix/... -count=1` exit 0 · `go test ./sqx/cmd/sqx-flowkit/... -count=1` exit 0 · `go test -race ./sqx/core/releasematrix/... -count=1` exit 0 · `go vet ./sqx/core/releasematrix/...` exit 0 · `go build ./sqx/cmd/sqx-flowkit/...` exit 0 · `git diff --check` exit 0 · gofmt limpio · guards 7/7 PASS en verbose.
- Round-trip canónico: `TestCanonicalRoundTripByteIdentity` PASS (artefacto committed == `MarshalCanonical(Parse(artifact))`); `TestEmbeddedMatchesRepoFile` PASS (embedded == repo file).
- Smoke de portabilidad: binario nuevo en `/tmp`, `release-matrix` desde CWD temporal vacío exit 0, byte-idéntico (`cmp` OK), stderr vacío, 17 capabilities.
- Git: `git diff --name-status 0ddd4db..HEAD` == exactamente los 2 allowed files; push fast-forward confirmado (SHA remoto == local `3d0e8c9`); dirty ajeno `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` intacto y excluido del stage; sin tag/release/merge/PR/deploy.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Repo: `git revert 3d0e8c958765da23840e00bf1a0ac017fc47597a` en `codex/f05-release-prep` (restaura la fila OPEN y el guard temporal; sin force).
- Vault: revertir las ediciones listadas en Cambio (SPEC/proyecto/agent-run/este log) — sin dependencias externas.
