# L0 — 2026-10-03 — D6 real execution lane retry post owner fix (raw)

**Sesión:** ZCode/GLM-5.3-Flash — despacho TOP one-shot (retry), NO-EGRESS, tras el fix owner del NinjaScript duplicado. Entidad: [[Echo Futures]].

## Hilo de evidencia (compacto, el detalle vive en el artifact §R0–R9)

- Insumo owner: fuente NinjaScript duplicada corregida + restart NT; log visible con AMBOS AddOns cargando; línea crítica `EchoExecutionAddOn config loaded: ntx=****.161:0` (precheck obligatorio A/B).
- R0 precheck RESUELTO = opción B (puerto real 0): format string imprime el puerto parseado sin máscara (MaskId sólo host/cuenta, `EchoExecutionAddOn.cs:134-137`); host parseó OK (`****.161` ⇒ archivo existe, `ntx_host` correcto) ⇒ defecto aislado a `ntx_port` (ausente/string ⇒ `GetNumber` default 0, `:127`); guards `ntxPort<=0 ⇒ return` (`:271`/`:407`) = lanes inertes silenciosas; bundle correcto (`9ca3fddc…`, `"ntx_port": 9771` numérico) re-verificado en C:\Temp ⇒ el instalado difiere; ACL 6.ª deny (instalado no agent-verificable).
- R2 físico decisivo: escritura guardada `futures-bridge/accounts=E2T-GAU50-01` (4 pasos + MCP RO) + bridge PID 1798251 release `40102ea5` (SHA `484b550b…`) listener `*:9771` activo >2.5 min ⇒ **cero conexiones, cero `[ntx]`**, ≥7 fases de retry cubiertas (contra LISTEN un dial = ESTABLISHED persistente).
- R3 barrier fail-closed a los 10.0 s exactos (`no authenticated AddOn session on the execution lane`, 2.ª demostración); readiness 8 blockers exactos, ambiguous/mismatches/dropped = 0/0/0; binding ETCD 12/12 por lectura cruda; topic de comandos inexistente.
- R1/R4/R6: NT reiniciado ≈21:25Z (PID 8700→11412); feed AddOn físico PASS (sesión `2e031cd2…`, frames 10 s, sink sin máscara: `resolved id "3"` == hint, 6.ª sesión consecutiva; positions/orders `[]`; balances demo 50000/50000); exec AddOn cargado PASS (supersede del FAIL previo); exec-side D/E/G/H NOT_RUN (endpoint no resuelto; probe no usado).
- R7/R8: STALE ≈24 h (replay estático de la sesión nueva a las 21:25:21Z, offsets p4 5476462→5476468, no refresca evidencia — F-S2-02); G_HORIZON PARTIAL_NEEDS_CREATED_ORDER; residual de producto no elevado: LoadConfig acepta `ntx_port` inválida con default 0 + log "config loaded" (contradice disciplina fail-closed declarada `:104-106`) — clase robustez AddOn, Manager adjudica.

## Salidas

- Artifact: `10-projects/Echo Futures/artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` (intento 1 preservado + §POST OWNER FIX / RETRY R0–R9 + /close)
- Project note D6 (sección RETRY) · change log `80-agents/journal/logs/2026-10-03-d6-real-execution-lane-retry.md` · agent-run mismo día.

## Fricciones/notas

- Ninguna nueva: read-command del MCP SSH sigue policy-denied (perfil viewer) ⇒ dev-win-operator; netstat/tasklist y ACL perfil KoR igual que en sesiones previas.
- ETCD crudo con cliente repo sdk/etcd (receta de memoria) funcionó a la primera; keys sin slash inicial; layout real: sesión = clave `futures-bridge/accounts`, binding = `accounts/E2T-GAU50-01/*`.

## Próximo paso

Owner: fix config §R9 (reemplazar JSON con copia íntegra de C:\Temp + reiniciar NT; señal observable ESTABLISHED→:9771 + hello ≤10 s). Dom ≥17:00 CT G-REALTIME (feed-lane-only, NO depende del fix). Con la señal: re-despacho C–K → lun 2026-10-05 ladder congelado.
