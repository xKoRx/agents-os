---
type: session_feedback
schema_version: 1
created: "2026-10-15"
updated: "2026-10-15"
area: "[[Aranea]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
entities:
  - "[[Echo Forge — Robust Run Selection V2]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[aranea-agent-dev]]"
severity: medium
category: environment
load_policy: manual
indexable: false
tags:
  - kind/feedback
  - scope/session
---

# Feedback — Runtime hardening worker-kronos: transporte SSH Windows, Ownership de CURRENT y LiveUpdate (2026-10-15)

## Observaciones

1. **El transporte aranea-ssh hacia hosts Windows degrada comandos PowerShell no triviales**: elimina `$_` (rompe cualquier pipeline con bloque de script), rechaza `&&` (PowerShell 5.1 ya lo rechaza solo) y rompe el quoting con comillas dobles anidadas. Todo el trabajo real requirió subir `.ps1` por SFTP y ejecutarlos con comandos cortos. Sugerencia: codificar esta regla (ya registrada en memoria del agente) en el runbook de la familia ssh del MCP, para que no se redescubra en cada sesión Windows.
2. **`CURRENT` del stager Windows es propiedad exclusiva de `StagerReconcile`**: un swap manual se revierte en ≤60s (reparación de divergencia, no reescritura periódica — el mtime no cambia si no hay drift). Es el diseño correcto, pero ningún doc lo declaraba: la prueba D de esta sesión lo descubrió por ensayo. Documentado ahora en worker-troubleshooting §10; conviene que el repo stager (no local en esta máquina) lo declare en su README.
3. **LiveUpdate de MT5 es un drift silencioso del runtime certificado**: el terminal de slot-2 descargó el build 6230 en plena prueba (11:49 local) sin ningún gate; se aplicará en el próximo arranque del terminal. La certificación wave3t (21/21) corre sobre build 6182. No existe clave de bloqueo verificada en `Config\common.ini` ni switch cableado en el worker. Riesgo real para la próxima campaña: resultados sobre un build distinto al certificado. Recomendación: decisión owner (bloqueo verificado por slot, bloqueo de red a endpoints MetaQuotes, o aceptar drift + re-validación pre-campaña).
4. **La sesión 0 del host es un recurso que se agota, no un booleano roto/sano**: dos incidentes (14-ago, 14-oct) con el mismo patrón "funciona temprano, falla después de N launches GUI", RADAR_PRE_LEAK de metatester64 como precursor, y recuperación al matar residentes GUI. El probe session-0 (tarea efímera SYSTEM + ini mínimo + grep MDI) es barato y debería ejecutarse ANTES de cualquier decisión de volver al SCM o de despachar una wave larga en session 0. Quedó codificado en worker-troubleshooting §10.
5. **El helper de despacho directo de `MT5BacktestArtifactWorkflow` es reutilizable y no está canarizado**: los smokes r3 (14-oct) y esta sesión lo reimplementaron a mano (patrón `di.InitSelective("sqx-watcher", …)` + `ExecuteWorkflow("MT5BacktestArtifactWorkflow")`). Sugerencia: promover un `sqx/tools/dispatch_mt5_smoke` canónico (fuera de releases) con la config certificada por defecto (`NDX_SQX`, rango vigente) para que el smoke de aceptación post-recuperación sea un comando, no un ejercicio de 40 min de descarga de historia como esta vez (usé `Symbol=NDX` 2024-H1 por defecto y pagué ~40 min de descarga).

## Lo que funcionó bien

- El handoff WINDOWS-HANDOFF-KRONOS-20261015 fue una base exacta: cada afirmación suya se re-verificó sin sorpresas (worker, tarea, servicio, layout, ACLs), lo que permitió ir directo a la investigación causal.
- La combinación MCP MinIO presign + hash local dio verificación byte-exacta del EX5 durable sin descargar por el canal MCP truncado.
- El binario worker resultó tener ya todo lo difícil (singleton fail-closed, recuperación de leases condicionada a muerte probada): el hardening correcto fue 100% fuera del binario, sin tocar la release certificada.
