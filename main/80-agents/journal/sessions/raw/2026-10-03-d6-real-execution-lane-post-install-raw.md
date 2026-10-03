# L0 — 2026-10-03 — D6 real execution lane post-owner-install (raw)

**Sesión:** ZCode/GLM-5.3-Flash — despacho TOP one-shot A–N, NO-EGRESS, post-instalación owner del EchoExecutionAddOn. Entidad: [[Echo Futures]].

## Hilo de evidencia (compacto, el detalle vive en el artifact)

- Mandato: verificar instalación owner sobre la realidad y certificar el lane (A–N). Insumo owner: copiado de AddOns+config al perfil KoR + restart NT (INPUT a verificar, no prueba).
- A: staged ×3 == HEAD (certutil sin espacios, método probado); instalados NO agent-verificables (ACL 5.ª deny; short-path 8.3 no resuelve); FILE_NOT_FOUND de certutil refutado por contra-prueba (quoting del transporte).
- B: NT PID 1876→8700; feed `64803b9b` hello 19:38:33Z seq 0 (feed AddOn compiló y corre); exec AddOn: 0 dials a :9771 en ~40 min con cadencia ≤10 s, 0 hellos, netstat vacío; Test-NetConnection True; PID sin cambio al cierre.
- C/D: ETCD `accounts=E2T-GAU50-01` guardado (pre-read→put→read-back→MCP RO) + bridge PID 1737260 release `40102ea5` listener :9771 → barrier fail-closed `no authenticated AddOn session`; readiness 8 blockers 0/0/0.
- E–K: binding feed-side vivo id "3" (5.ª sesión); exec-side/Barrier/Reconnect/Fencing/Restart NOT_RUN (probe prohibido y no usado); G_HORIZON PARTIAL_NEEDS_CREATED_ORDER.
- L/M/N: STALE ≈22 h (p4 5476461 replay estático); NEW_RISK NO; runbooks Sunday/Monday READY.
- Cierre: G-EGRESS-0 probado (unidad inactive+disabled, :9771 FREE, clave eliminada, 21 claves exactas); cero commits `40102ea5a44b…`; 0 órdenes; OD-D6-1 vigente.

## Salidas

- Artifact: `10-projects/Echo Futures/artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` (A–N + /close)
- Project note D6 · change log `80-agents/journal/logs/2026-10-03-d6-real-execution-lane-post-install.md` · agent-run mismo día.

## Fricciones/notas

- MCP RO ETCD fuzzy-read 2.ª vez ("17:00" para clave borrada) — cliente crudo = autoridad.
- Transporte SSH dev-win: comillas de paths con espacio se strippean; PowerShell remoto; tasklist/Get-Process StartTime denegados por ACL; netstat ok.

## Próximo paso

Owner re-ciclo W1 con verificación → señal dial :9771 cada ≤10 s → re-despacho C–K → dom G-REALTIME (runbook §M) → lun 2026-10-05 ladder (§N).
