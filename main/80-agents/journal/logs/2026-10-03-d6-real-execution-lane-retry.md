# Change Log — 2026-10-03 — D6 Real Execution Lane RETRY post owner fix (FAIL: config JSON parsea ntx_port=0)

- **Fecha:** 2026-10-03
- **Entidad:** [[Echo Futures]]
- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` (append §POST OWNER FIX / RETRY R0–R9: precheck `:0` resuelto, C/F con listener activo, owner action §R9, handoff /close; intento 1 preservado íntegro)
  - `10-projects/Echo Futures/Echo Futures.md` (nueva entrada de bitácora D6: REAL EXECUTION LANE RETRY POST OWNER FIX — FAIL raíz única)
  - `80-agents/journal/agent-runs/2026-10-03-zcode-glm53-d6-real-execution-lane-retry.md` (nuevo)
  - `80-agents/journal/sessions/raw/2026-10-03-d6-real-execution-lane-retry-raw.md` (nuevo L0 compacto)

## Motivo

- El Owner corrigió la fuente NinjaScript duplicada y reinició NinjaTrader: evidencia visible de ambos AddOns cargando (supersede del hallazgo de instalación del intento 1). Despacho de re-certificación one-shot NO-EGRESS con precheck crítico obligatorio sobre `ntx=****.161:0`.

## Resolución aplicada

- **Precheck resuelto = opción B (puerto real 0):** el format string del AddOn @ HEAD imprime el puerto parseado sin máscara (`EchoExecutionAddOn.cs:134-137`; MaskId sólo host/cuenta); host parseó OK ⇒ el archivo existe con `ntx_host` correcto y el defecto queda aislado a `ntx_port` (ausente/string ⇒ `GetNumber` default 0); guards `ntxPort<=0 ⇒ return` (`:271`/`:407`) dejan ambos lanes inertes sin log; bundle correcto (`9ca3fddc…`, 9771 numérico) re-verificado en `C:\Temp` ⇒ el instalado difiere; ACL 6.ª deny. Confirmación física: bridge release `40102ea5` (PID 1798251, SHA `484b550b…`) con listener `*:9771` activo >2.5 min ⇒ cero conexiones y cero líneas `[ntx]` cubriendo ≥7 fases de retry. Clasificado **config-only** (no defecto de parser: entrada válida ⇒ 9771).
- **Ejecutado con listener activo:** escritura guardada `futures-bridge/accounts=E2T-GAU50-01` (pre-read → put → read-back → cross-check MCP RO) → `account session built` 1.0 s → barrier fail-closed a los 10.0 s exactos (`no authenticated AddOn session on the execution lane`, 2.ª demostración); readiness `ready_new_risk=false` con los 8 blockers exactos 0/0/0; binding ETCD 12/12 re-verificado por lectura cruda; topic de comandos inexistente (0 replayables).
- **Evidencia complementaria:** NT reiniciado ≈21:25Z (PID 8700→11412); feed AddOn físico PASS (sesión `2e031cd2…`, sink sin máscara `resolved id "3"` == hint ETCD, 6.ª sesión consecutiva; positions/orders `[]`; balances demo 50000/50000); exec AddOn cargado PASS; exec-side D/E/G/H NOT_RUN (mandato: endpoint no resuelto ⇒ no ejecutar; probe no usado); STALE ≈24 h (replay estático de la sesión nueva NO refresca evidencia, F-S2-02); residual de producto no elevado: LoadConfig acepta `ntx_port` inválida con default silencioso 0 + log "config loaded" (§R8, adjudicación Manager).
- **Teardown a G-EGRESS-0 probado:** unidad inactive+disabled, `:9771` FREE, clave de sesión eliminada con ciclo guardado (cross-check MCP RO 21 claves == baseline), journal M2 0 registros, herramienta efímera ETCD eliminada, worktree limpio. Delta infra neto CERO; cero commits (`40102ea5a44b…`); `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`.

## Validación

- Evidencia triple capa (fuente byte-verificada + bundle + TCP físico contra LISTEN activo) cross-verificada con SSH dev-win-operator, ETCD crudo (cliente repo), journalctl bridge/relay, sink evidence.jsonl sin máscara y Kafka MCP. `NTX_PORT_ZERO_LOG_EXPLAINED = YES`; `EXECUTION_ADDON_LOADED = PASS` (supersede); `OWNER_W1 = PASS` con excepción de config registrada aparte. OD-D6-1 AUTHORIZED vigente sin consumir. Sin secretos persistidos.

## Compartibilidad

- Owner: única acción exacta (§R9, ciclo standing OD-D6-4) — reemplazar `echo-execution-addon.json` del perfil KoR con la copia íntegra de `C:\Temp` (hash `9ca3fddc…`; `"ntx_port": 9771` numérico; NO editar a mano) y reiniciar NinjaTrader. Señal observable por el agente sin intervención owner: ESTABLISHED→:9771 + hello `[ntx]` autenticado ≤10 s tras el arranque de NT con el bridge en marcha.
- Manager: FAIL ⇒ no certificar lane ni ejecutar ladder hasta el fix. Domingo 2026-10-04 ≥17:00 CT: G-REALTIME certificable (feed-lane-only, NO depende del fix, runbook §M). Con la señal: re-despachar C–K (~5 min en ventana) → ladder congelado §N en lun 2026-10-05 00:00–15:50 CT. No emitir `EF_D6_E2E_PASS`.
