---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Personal]]"
project: "[[Loom]]"
application:
entities:
  - "[[Loom]]"
related:
  - "[[2026-09-20-zcode-glm-5.3-flash-loom-f3-ux-lab]]"
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

# 2026-09-20-loom-f3-ux-lab-g3

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Loom/Loom.md` — entrada en Estado actual: G3 LAB READY (Today interactivo sobre vault sintético, rama `feature/f3-ux-lab` publicada en origin @ `47cbadb`, veredicto auditor PASS, habilitación de producto sigue pendiente del owner).
- **Artefactos fuera del vault:** repo `xKoRx/loom` rama `feature/f3-ux-lab` (17 commits sobre `62943d4`): `poc/f3ux/` (comando demo, scaffold, UI Vue, ledger), `poc/f3lab/serve/{projection,sanitize}.go`, `poc/f3ux/{e2e,audit}/`, `specs/FEAT-F3-UX-LAB/RESULTS.md` + 12 capturas + evidencia de gates.

## Motivo

- Mandato "Today Interactive Lab" (G3 de laboratorio): convertir el lab F3 certificado (G1 watcher real + G2 HTTP) en una experiencia Today funcional en navegador, con escrituras reales exclusivamente sobre un vault sintético desechable, sin habilitar nada en producto.

## Fuentes usadas

- `specs/FEAT-F3-INTEGRATION/{INTEGRATION-CONTRACT,RESULTS}.md`, `specs/FEAT-F3-HARDENING/RESULTS.md`, `specs/FEAT-LOOM-V04/DAILY-PLAN-FORMAT.md`, `specs/FEAT-LOOM-V06/CONTRACT-DECISIONS.md` (rama lab).

## Resolución aplicada

- Fix G3-M1: "reprogramar" vive sólo en el picker de origen para tareas ausentes del plan (el writer certificado exige unicidad de block ID por plan; el control sobre referencias ya comprometidas jamás podía tener éxito). El writer no se debilitó.
- Hallazgos del auditor B1-01/B1-02 (LOW) CERRADOS: rechazo de forma 422 de `originNote` con `..`; redacción de rutas físicas en todo `detail` HTTP (`serve/sanitize.go`).
- Residual §9.B convertido en requisito bloqueante de habilitación (G4/G5): ledger durable de requestIds del lado servidor/caller.

## Validación

- Gates sobre SHA final `47cbadb` (evidencia en `specs/FEAT-F3-UX-LAB/evidence/gates-final.txt` del repo): gofmt/gofumpt/vet limpios; `go test -count=1 ./...` 14/14 ok (incluye matriz F3, H1–H10, R01–R09, G1, G2, auditoría ATK); race `-count=1` limpio; aislamiento `go list -deps ./cmd/loom` = 0 referencias f3*; sin rutas POST ni `allow-write-plan` en cmd/+internal; v0.6 `36c760c` intacta; secret scan 0; build desde árbol limpio OK; E2E Chromium E01–E12 12/12 PASS (tres capas) con veredicto PASS del auditor.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- La rama `feature/f3-ux-lab` es autónoma y jamás se fusiona a master/v0.6; eliminar la rama remota y los worktrees (`loom-f3ux*`) revierte todo. Ningún cambio de producto en master/v0.6.
