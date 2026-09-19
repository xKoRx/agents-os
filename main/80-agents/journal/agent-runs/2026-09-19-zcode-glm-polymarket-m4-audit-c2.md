---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: run
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-09-19-zcode-glm-polymarket-m4-audit-c2

## Trabajo

- **Objetivo:** mandato M4-AUDIT-C2 — resolver los hallazgos del M4 FINAL ACCEPTANCE AUDIT sobre el baseline ratificado `879886f`: cerrar G-11 con fixtures propias, incorporar G-07 con tres schedules explícitos, endurecer cobertura con tests de falla útiles, reconstruir el harness `certify` con identidad completa + receipts reales + baseline pinning + STALE_CERTIFICATION + matriz negativa, y re-certificar no-live.
- **Alcance atribuible a esta combinación superficie×modelo:** preflight (SHA `879886f`, árbol limpio, sin writers, suite baseline verde 25 paquetes); P1 G-11 — nuevo `internal/account/reconcile.go` dentro del ownership Account (observaciones de orden/settlement con ejes frozen monótonos, contradicciones → casos durables migración 0036, settlement FAILED sin liberar saldo/reserva/confirmación con escalado HUMAN_REVIEW_REQUIRED, transferencias EXTERNAL_IN/OUT/INSTANCE_MOVE exactly-once con UNATTRIBUTED bloqueante, scan REST paginado con re-lectura de estabilidad), fixtures versionadas `testdata/account/fixtures/g11/` con manifest sha256 + provenance, 15 escenarios expected/actual con evidencia `testdata/account/evidence/g11.json` (patrón emit/re-check), regresión G-02/G-02b/G-10c/G-11b/G-12/G-12b verde con race (checkpoint `17cc207`); P2 G-07 — evidencia formal `testdata/replay/evidence/g07.json` con schedules {32}/{1}/{7,3,1} explícitos, digests idénticos y delivery verdicts (checkpoint `5fbeec5`); P3 cobertura por orden de prioridad con tests de falla útiles (sin borrar código, sin excluir paquetes): supervisor 64.7→79.5 con **corrección de defecto real** (Boot no copiaba dataDir a cfg ⇒ el diagnóstico de watermark de disco siempre hacía statfs sobre path vacío y nunca podía salir de OK — corregido y mapeo OK/LOW/CRITICAL probado), frames 82.4→87.6 (inbox-full con semántica de consumo de seq, aborto de reservación con rollback, fencing de generaciones), account 77.7→80.5 (atomicidad ante storage failure, bordes del classifier, EXTERNAL_OUT idempotente), risk 82.9→91.4, replay 79.7→80.7, strategy 75.9→78.5, simulator 79.8→85.4, cmd 50.3→68.0 (matriz de runners in-process con códigos de salida) (checkpoint `4381884`); P4 harness reconstruido — 32 filas (27 no-live sobre los 26 identificadores del plan + 5 live diferidos), identidad por fila (evidence path + SHA-256 + verify command + timestamp + baseline), receipts reales ejecutados al certificar (comando/baseline/exit/packages/patrón/estado; recibo vacío = FAIL; sin suites = NOT_RUN, jamás PASS), PARTIAL rechazado fail-closed, `M4_STALE_CERTIFICATION` ante baseline incorrecto, matriz negativa pineada + test de integración sobre el árbol real (checkpoint `1c4f123`); regresión final build/vet/test/race/tidy/diff-check verde; E2E físicos sobre el journal vivo `/tmp/pm-ws2` (verify NO_INTEGRITY_FAILURES frontier 6464, manifest 11 segmentos, replay digest `7f24c081…` idéntico en schedules {1}/{32} — igual al registrado en la auditoría previa, SHADOW INCONCLUSIVE honesto, backup→restore 16/16 sin degradación + verify restaurado, boot LIVE_DISABLED/NO_LEASE/readiness_live false); certificado final re-emitido en HEAD `1c4f123` con pin de baseline: `M4_CERTIFIED_NON_LIVE` 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 diferidos; higiene vault aparte (36 residuos `*.md.tmp.*` eliminados con prueba por archivo, entrada en [[2026-09-19-md-tmp-residue-cleanup]]); actualización de [[Polymarket Engine — MVP]] (bitácora + estado `M4_ACCEPTANCE_PENDING` por piso de cobertura).

## Verificación

- `go build ./...`, `go vet ./...`, `go test ./...`, `go test -race ./...`, `go mod tidy`, `git diff --check`: verdes en `1c4f123`, árbol limpio.
- `engine experiment certify --repo-root . --baseline <HEAD>`: exit 0, `M4_CERTIFIED_NON_LIVE`, 32 filas; negativos demostrados por CLI (baseline incorrecto → `M4_STALE_CERTIFICATION`; `--skip-suites` → `M4_PARTIAL` 14 in-scope NOT_RUN sin recibos inventados).
- E2E: comandos físicos listados arriba con exits verificados; digest de replay coincide con la evidencia de la auditoría previa (sin recaptura).
- Cobertura reproducible final (`go test -cover ./...`): módulo ~87%; ≥95: catalog 95.0, protocol 94.8, config 97.8, archtest 97.1, gamma 97.5; resto entre 78–91 — **el piso 95 por paquete sigue sin cumplirse** (bloqueador declarado de aceptación, sin excepciones auto-aprobadas).

## Rework

- Ninguno por ahora; pendiente de decisión owner/manager: piso de cobertura 95 por paquete (elevar o aprobar excepciones por líneas concretas con la clasificación entregada) y resolución final `M4_MANAGER_ACCEPTED_NON_LIVE`.
