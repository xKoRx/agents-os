# Change Log — 2026-10-03 — D6 Real Execution Lane post-owner-install (BLOCKED_OWNER_ACTION: AddOn ejecución no activo en NT)

- **Fecha:** 2026-10-03
- **Entidad:** [[Echo Futures]]
- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` (nuevo: artifact de certificación del lane post-instalación owner — verificación B, hallazgo físico, readiness fail-closed, teardown G-EGRESS-0, checklist owner §9, handoff completo)
  - `10-projects/Echo Futures/Echo Futures.md` (nueva entrada de bitácora D6: REAL EXECUTION LANE POST-OWNER-INSTALL — BLOCKED_OWNER_ACTION)

## Motivo

- Owner ejecutó el ciclo W1 (copiado de `EchoExecutionAddOn.cs` + `EchoFeedAddOn.cs` + `echo-execution-addon.json` al perfil KoR + reinicio de NinjaTrader) y se despachó la certificación física del execution lane sin egress sobre la instalación ya realizada.

## Resolución aplicada

- `D6_REAL_EXECUTION_LANE_NO_EGRESS = BLOCKED_OWNER_ACTION` — la instalación del AddOn de ejecución **no tomó efecto físicamente**: NT reiniciado OK (PID 1876→8700; feed sesión `2f6a4d53`→`64803b9b`, hello 19:38:33Z) pero **0 intentos de conexión a :9771 en ~30 min** con cadencia de diseño ≤10 s, 0 hellos `[ntx]`, netstat dev-win vacío; transporte descartado (LISTEN `*:9771` + `Test-NetConnection = True` desde el host NT). Barrier fail-closed temprano certificado (`no authenticated AddOn session on the execution lane`); readiness fail-closed cada 30 s (8 blockers, ambiguous/mismatches/dropped = 0/0/0) — la conjunción frozen jamás abre sin AddOn autenticado.
- Binding feed-side vivo: `RJARA114411201551` = NT `Account.Id "3"` == hint ETCD (5.ª sesión consecutiva). Balances 50000/50000 (variante demo 01-oct, documentada).
- D–G (binding exec-side, account observation exec lane, barrier completo, fencing/reconnect F-S2-01/04, restart recovery) = NOT_RUN con AddOn real; el lado transporte permanece certificado por weekend §3/§5/§8. G_HORIZON sigue PARTIAL_NEEDS_CREATED_ORDER.
- Teardown a **G-EGRESS-0**: unidad `echo-futures-bridge` inactive+disabled, `:9771` FREE, clave ETCD `futures-bridge/accounts` eliminada con ciclo guardado (pre-read exacta → delete → read-back → listing exacto 21 claves). Delta de infraestructura neto CERO; repo @ `40102ea5a44b…` sin commits (BASELINE=FINAL).
- `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`; topic `echo.order-commands.E2T-GAU50-01.v1` inexistente; `session-observations.v1` sin registros nuevos hoy; journal M2 vacío.

## Validación

- Evidencia física cross-verificada (SSH dev-win netstat/Test-NetConnection + journalctl bridge/relay + evidence.jsonl sin máscara + ETCD crudo con lecturas exactas + Kafka MCP). ACL del perfil owner re-probada (5.ª deny) ⇒ la verificación de instalados es conductual; el `FILE_NOT_FOUND` de certutil se documentó como artefacto de quoting (lo dio también sobre el feed AddOn que SÍ corre). El MCP RO ETCD repitió el matching difuso ("17:00" para la clave borrada, 2.ª vez) — cliente crudo como autoridad. Sin secretos persistidos. OD-D6-1 queda AUTHORIZED sin consumir.

## Compartibilidad

- Owner: repetir W1 con verificación (checklist §9 del artifact) — verificar targets/bytes desde su sesión, re-copiar con `-Force` desde `C:\Temp`, reiniciar NT DESPUÉS de copiar, `compile-errors.txt` si NinjaScript falla. Señal de éxito observable por el agente: dial `:9771` cada ≤10 s.
- Manager: con la señal de éxito, re-despachar el lane pasos C–K (enable sesión + bridge + barrier con AddOn real + D–I) y luego el ladder físico congelado lun 2026-10-05 00:00–15:50 CT. No emitir `EF_D6_E2E_PASS` hasta ladder completo.
