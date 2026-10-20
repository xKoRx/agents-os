---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-20"
updated: "2026-10-20"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities:
  - "[[Echo Futures — Runtime Pools]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
model_source: perfil autorizado por KoR
task_type: debugging
task_complexity: high
outcome: success
verification: partial
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

# Agent Run — CERT-NT-01 RESUME-04 (RCA timeout transporte + paquete JSON SIM, ventana acotada)

## Trabajo

- **Objetivo:** mandato CERT-NT-01 / RESUME-04 (Primary Manager GPT-6, Owner KoR): RCA del bloqueo de estabilidad StateFun→core, corrección, prueba sostenida y JSON SIM final. El Owner acotó la ventana a media sesión («cerrar todo urgente, mañana continuamos») ⇒ se ejecutó en modo read-only + preparación, sin redeploy ni prueba sostenida (fallback /close del mandato: rollback conocido + limitación explícita).
- **RCA DEMONSTRADA:** lote de 1001 envelopes a `echo/market_stream` ≈161 s al ritmo real del handler (4460 canónicos/720 s ≈ 6,2 ev/s, journal core verificado) > call timeout declarado 2min (`module.yaml:28`, netty async, `maxNumBatchRequests: 1000`); `RequestTimeoutException` attempt #0 con mailbox bloqueado ≥106 s (checkpoint barrier WARN; patrón 83 s previo bajo límite); 3 fallos idénticos → FAILED → rollback ya ejecutado en RESUME-03. Clasificación PRODUCT×CONFIG. Evidencia: docker logs .75 (`/tmp/w-r3.log` 23:30–23:50Z), journal echo-core-dev, module.yaml del worktree c37d1351.
- **Backlog contabilizado por partición** (Kafka MCP): p4 committed 23.223.863 congelado, HWM 23.524.736, lag 300.873, low_watermark 21.848.991 (tramo histórico bajo committed por diseño `latest` — no procesado).
- **ETCD PRE/POST:** intacto (enabled mod 61254, snapshot sha 5e59fb4c mod 61253); borrado 22:31Z refinado a revs 61251+61252 consecutivos; sin autoría demostrable (sin audit log; 0 tests del repo escriben las claves).
- **JSON SIM FINAL:** `~/aranea/work/cert-nt-01-mgr/RESUME04-ADDON-JSON-SIM101-FINAL.json` (sha256 4579fa32…) con `ntx_port: 0` (lane de mercado del AddOn de ejecución deshabilitada → única autoridad de feed = D6 :9770; verificado en source `:422` que port<=0 no invalida el JSON y `:184-188` que ntx_host vacío heredaría 9771); validación campo a campo contra `ParseBindings` (.cs byte-exacto a93a6a1e); pendiente UN dato Owner (ID de plataforma de Sim101).

## Evidencia

- Planner «RESUME-04» + bitácora 2026-10-20 + gate C2 actualizados (readback pendiente en cierre).
- Vault: `artifacts/runtime/cert-nt-01/RESUME04-ADDON-JSON-SIM101-FINAL.json` + `RESUME04-ADDON-JSON-SIM101.md`.
- Sin mutaciones al runtime: module PRE 74a3c72d, job 6ecfa30b 28/28 failed=0, core c37d1351 PID 2738096, FX lag 0, armado ausente, cero órdenes, cuentas reales intactas.

## Límites

- Estabilidad NO demostrada en esta ventana; fix (producto o config de un parámetro) y prueba sostenida 30 min pasan a RESUME-05 con dependencias en orden (planner).
- Verificación independiente B y despacho de especialistas C no ejecutados (ventana); la RCA fue ejecutada por el submanager con evidencia cruda referenciada.
