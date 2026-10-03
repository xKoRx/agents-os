# Change Log — 2026-10-03 — D6 Real Execution Lane post-owner-install (FAIL: AddOn ejecución no cargó en NT)

- **Fecha:** 2026-10-03
- **Entidad:** [[Echo Futures]]
- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` (nuevo, esquema A–N del despacho: verificación owner install, runtime NT, bridge enable, runbooks M/N, final safety state G-EGRESS-0, handoff /close completo)
  - `10-projects/Echo Futures/Echo Futures.md` (nueva entrada de bitácora D6: REAL EXECUTION LANE POST-OWNER-INSTALL — FAIL)
  - `80-agents/journal/agent-runs/2026-10-03-zcode-glm53-d6-real-execution-lane-post-install.md` (nuevo)
  - `80-agents/journal/sessions/raw/2026-10-03-d6-real-execution-lane-post-install-raw.md` (nuevo L0 compacto)

## Motivo

- Owner ejecutó el ciclo W1 (copiado de AddOns + config al perfil KoR + reinicio de NinjaTrader) y despachó la certificación física del execution lane sin egress sobre la instalación realizada (mandato A–N, one-shot).

## Resolución aplicada

- `D6_REAL_EXECUTION_LANE_NO_EGRESS = FAIL` — la certificación no se completó: el EchoExecutionAddOn real nunca se cargó en NT. Evidencia runtime multiplicada: NT reiniciado (PID 1876→8700; feed AddOn compiló y publica), **0 intentos de conexión a :9771 en ~40 min** con cadencia de diseño ≤10 s, 0 hellos, netstat vacío, bridge LISTENING + `Test-NetConnection=True` desde el host NT, PID sin cambio en re-verificación final. `OWNER_W1_VERIFIED = FAIL`: bytes instalados no verificables (ACL estructural del perfil KoR, 5.ª deny; short-path 8.3 no resuelve) y el `FILE_NOT_FOUND` de certutil refutado como evidencia por contra-prueba (quoting del transporte). No es REMEDIATION_REQUIRED: los mismos bytes pasaron shadow-compile físico en Shot 3 ⇒ sin candidato de defecto de producto.
- Ejecutado agent-side: bundle staged re-verificado ×3 (b2a29a36…/581a7087…/9ca3fddc… == HEAD); escritura guardada ETCD `futures-bridge/accounts=E2T-GAU50-01` + bridge start (PID 1737260, release 40102ea5, listener *:9771) → barrier fail-closed temprano (`no authenticated AddOn session`); readiness fail-closed 8 blockers 0/0/0 toda la corrida; binding feed-side vivo (id "3" == hint, 5.ª sesión); STALE ≈22 h confirmado; runbooks M (Sunday G-REALTIME, ya probado con la misma llamada) y N (Monday ladder) listos.
- Teardown a **G-EGRESS-0 probado**: unidad inactive+disabled, `:9771` FREE, clave de sesión eliminada con ciclo guardado (lectura exacta, 21 claves). Delta infra neto CERO; cero commits (`40102ea5a44b…`). `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`; topic de comandos inexistente; journal M2 vacío; 0 frames de comando.

## Validación

- Evidencia física cross-verificada (SSH dev-win netstat/certutil/Test-NetConnection + journalctl bridge/relay + evidence.jsonl sin máscara + ETCD crudo con lecturas exactas + Kafka MCP). La verificación de instalados quedó documentada como estructuralmente imposible para el agente (ACL) con la contra-prueba de quoting que invalida el falso FILE_NOT_FOUND. MCP RO ETCD repitió fuzzy-read (2.ª vez) — cliente crudo como autoridad. Sin secretos persistidos. OD-D6-1 AUTHORIZED vigente sin consumir.

## Compartibilidad

- Owner: repetir W1 CON VERIFICACIÓN (checklist en artifact §A/§9) — verificar targets + hashes, re-copiar `-Force` desde `C:\Temp`, reiniciar NT DESPUÉS de copiar, `compile-errors.txt` si NinjaScript falla. Señal de éxito observable: dial `:9771` cada ≤10 s.
- Manager: FAIL ⇒ no certificar lane ni ejecutar ladder hasta el fix. Con la señal de éxito: re-despachar pasos C–K del artifact → domingo G-REALTIME (runbook §M) → ladder congelado §N en lun 2026-10-05 00:00–15:50 CT. No emitir `EF_D6_E2E_PASS`.
