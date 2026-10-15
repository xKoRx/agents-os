---
type: session_feedback
schema_version: 1
created: "2026-10-15"
updated: "2026-10-15"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[aranea-agent-dev]]"
severity: low
category: environment
load_policy: manual
indexable: false
tags:
  - kind/feedback
  - scope/session
---

# Feedback — MT5 version-agnostic: allow-list eliminada, release 0.2.142 y smoke físico del build 6230 (2026-10-15)

## Observaciones

1. **El cierre del ítem 3 del feedback de la mañana (LiveUpdate drift) ya tiene implementación**: la decisión del owner ("compatibilidad por contrato observado, no por número de versión") quedó implementada en symphony `8b9a2db` + release 0.2.142 (Gate A preflight + Gate B report-smoke por instalación efectiva) y el build 6230 de slot-1 quedó validado físicamente end-to-end (HTM auténtico, parser 7/7, normalize OK, evidencia Gate B PASS). La "re-validación pre-campaña" recomendada esta mañana es ahora automática: el primer backtest tras cualquier cambio de ejecutable actúa de smoke y el resultado bloquea o habilita el despacho.
2. **La sesión MCP `aranea-ssh` expiró a mitad de sesión y ZCode no la re-inicializa automáticamente** (`Session not found or expired` en cada llamada). El fallback paramiko (credenciales de la skill app-owned worker-ssh) funcionó completo, pero duplica el transporte. Sugerencia: reciclar la sesión MCP (initialize HTTP) o documentar el fallback como vía primaria para hosts Windows de esta flota.
3. **El helper de despacho directo de `MT5BacktestArtifactWorkflow` se reimplementó por tercera vez** (r3 14-oct, hardening 15-oct mañana, y esta sesión lo volvió a necesitar). La sugerencia del feedback de la mañana sigue vigente y hoy tiene más argumento: el tool efímero de esta sesión (`di.InitSelective("sqx-mt5-worker", ENV=production)` + upload MinIO + `ExecuteWorkflow`) funcionó a la primera; canarizarlo como `sqx/tools/dispatch_mt5_smoke` (con la config XAUUSD H1 julio-2026 certificada de este smoke como default) lo convierte en un comando.
4. **Higiene de tests del repo symphony (dos hallazgos de la suite completa)**: (a) `sqx/activities/worker/phase4_performance_test.go` reescribe el fixture trackeado `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` al correr la suite — pollution de árbol que obliga a `git checkout --` después; (b) `sqx/adapters/registry-postgres` es flaky bajo suites paralelas pesadas (FAIL 199s en paralelo, PASS 239s/278s solo, con y sin el cambio). Ninguno bloquea; conviene wingate o temp dir para (a) y un retry/orden para (b).
5. **El flujo de release Windows canónico funcionó de punta a punta sin intervención** (`deploy_release.sh --release-only 0.2.142` → stager stageó con SHA verificado → supervisor hizo swap ≤35 s → worker en `releases\0.2.142` con `env=production`): la inversión del hardening de la mañana se pagó sola en el primer rollout real, que además era exactamente la prueba que faltaba (update con release real nueva).

## Lo que funcionó bien

- La regla de ambiente del contrato (Forge = un solo ambiente operacional) evitó toda tentativa de DEV paralelo: el smoke corrió en la flota real con prefijo nuevo (`smoke-version-agnostic-20261015/`) sin tocar wave3t.
- El EX5 local del finalista (`~/aranea/work/mt5-runtime-hardening-20261015/ex5_89171ea6.bin`, SHA verificado contra la memoria de la sesión de la mañana) evitó re-descubrir el artefacto del smoke.
- MinIO GET + hash + parse con el parser productivo (`-fetch` del tool efímero) dio la verificación end-to-end del HTM 6230 en un solo comando, con la identidad byte-exacta contra la evidencia Gate B.
