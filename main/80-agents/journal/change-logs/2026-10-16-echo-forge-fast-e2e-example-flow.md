---
type: change_log
schema_version: 1
scope: session
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[2026-10-16-zcode-glm53-echo-forge-fast-e2e-example-flow]]"
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
confidence: high
source_session:
source_feedbacks:
---

# Change Log — Fast E2E SQX144 example_flow (2026-10-16, sesión de corrección)

## Cambios en repositorios (pusheados a origin/master `5a66bb6→f30ed1d`)

- `xKoRx/symphony` `4b46b5e` — fix(worker): fallback `matchRetesterUpstreamByCarrier` en db_register del retester durable (outputs decorados por SQX `.k0/.z0` + prefijo job vs tokens compactos del Builder; fail-closed 0/>1 candidatos) + test focalizado.
- `xKoRx/symphony` `e1405d1` — fix(worker): mismo fallback en `persistRetesterEvidence` (upstream + fila de overview por carrier embebido con unicidad estricta).
- `xKoRx/symphony` `c2b234a` — chore(release): manifest 0.2.145 (linux `c3ba2a86`; rollout Zeus+Kronos verificado; Hera pending por host caído).
- `xKoRx/symphony` `f30ed1d` — chore(release): manifest 0.2.146 (linux `e94c38d3`; rollout Zeus+Kronos verificado; Hera pending).

## Cambios operacionales (sin commit; owner-canon)

- CFX nuevo `Build_BR_G1_H1_144_fast.cfx` sha `07321f99` (delta sobre `507507c5`: Build Output databank `Results`→`output` — el CustomAnalysis inyectado lee `output`; MaxStrategies 1000→24; databank-full 24/restart 0). Los otros 4 CFX reutilizados byte-exactos (`2cd587f0`, `14d55e98`, `d4d9c0aa`, `a51c1cc3`).
- Limpieza manual de databanks del staging custom 144 en Zeus/Kronos entre re-despachos (residuos de waves propias; la limpieza pre-pipeline del worker no siempre limpia Results).
- Watcher candidate-local `forge-watcher-fast144` en `~/aranea/work/fast-e2e-sqx144-example-flow-20261016/watcher` — eliminado al cierre (screen quit; sin procesos).
- Helpers efímeros en `sqx/tools/` eliminados antes del push; repo limpio en `f30ed1d`.
- FlowRuns wave 1-7 bajo identidad `NDX_example_flow_fast_v1_w*`: FAILED_ATTEMPT_KEEP (prefijos MinIO `wave_1..7/ndx/l_h1/example_flow_fast/` y filas PG/Mongo preservados sin borrado).
- Campaña errónea `569c152c` CANCELLED durable 15:24:46Z; artefactos preservados.

## Cambios en vault

- Nuevo: `10-projects/Echo Forge — Operación Real V2/artifacts/FAST-E2E-SQX144-EXAMPLE-FLOW-20261016/` (REPORT FAIL honesto, STAGES-MATRIX.csv, WORKERS-144-MATRIX.csv, CONFIG-ORIGINAL-AND-ADAPTED.md, SHA256SUMS, CFX, specs).
- Actualizado: `10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md` (sección sesión 2026-10-16 Fast E2E + estado flota 0.2.146 + hallazgos de defectos).
- Nuevo: `80-agents/journal/agent-runs/2026-10-16-zcode-glm53-echo-forge-fast-e2e-example-flow.md`; `80-agents/journal/feedback/session/2026-10-16-forge-fast-e2e-budget-control-feedback.md`.

## No cambiado (explícito)

- Thresholds frozen (robust V2 0.35/0.01/0.01; ranking 40/30/30), contratos congelados, Echo (cero ingress/deployments), flota Hera (caída ambiental, sin intervención), worker Windows (sin ejercicio), artefactos de campañas previas.
