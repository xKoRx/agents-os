# OPERATIONAL-SAFETY — Safe release adoption + canary reuse guard (2026-10-16)

**STATUS: FORGE_OPERATIONAL_SAFETY_PASS**

Sesión one-shot ZCode/GLM-5.3-Flash sobre el mandato "ECHO FORGE — FINAL
OPERATIONAL SAFETY — SAFE RELEASE ADOPTION + CANARY REUSE GUARD" (manager
GPT-6). Base: `WINDOWS-RUNTIME-HARDENING-20261015.md` (mismo directorio) y
release 0.2.143 operacional con stager driver `windows-session-supervisor`. No
se repitió wave3t; no se cambió Fidelity, ranking ni selección; cero
integración Echo; sin reboot del host; sin autologon.

## Resultado

`FORGE_OPERATIONAL_SAFETY_PASS`: (A) ningún update ordinario vuelve a matar
activities en vuelo — el supervisor adopta releases por **drain** del lifecycle
existente del worker y sólo lanza la release nueva con el cierre probado;
(B) un canario (`smoke_canary=true`) con SourceKey de evidencia ya existente se
rechaza con error tipado pidiendo SourceKey nuevo — jamás responde con evidencia
reutilizada como si fuera ejecución nueva.

## 1. Safe release adoption (riesgo A)

**Antes:** el supervisor (v2.1, `taskkill /T /F` en update) mataba el worker al
avanzar `CURRENT` — los logs de worker-kronos muestran los taskkill de las
adopciones 0.2.141→0.2.142 (19:21Z) y 0.2.142→0.2.143 (23:43Z) del 15-oct.

**Mecanismo nuevo (dos extremos):**

- Worker (`sqx/cmd/sqx-mt5-worker/drain_windows.go`, nuevo): observa el evento
  nombrado `Global\echo-forge-sqx-mt5-worker-drain` (crear-o-abrir, manual-reset,
  **reseteado al arrancar** para descartar señales perdidas entre dos vidas). El
  disparo alimenta el MISMO shutdown de siempre: cancel → `serveMT5Lifecycle`
  (`BeginDrain` → admisión cerrada → activities en vuelo terminan →
  `worker.Stop` → `MarkStopped` → `singleton.Release`). Sin trigger el worker
  arranca igual (fail-open documentado, telemetría ERROR).
- Supervisor (`deploy/windows/session-worker/Start-EchoForgeSessionWorker.ps1`):
  ante `CURRENT` avanzado hace `OpenEventW`+`SetEvent`, re-señala cada ciclo
  (idempotente) y lanza la release nueva **sólo** al observar el worker ausente
  (`worker previo pid X ya no esta (cierre probado): adoptando release Y`). Sin
  evento accesible o sin cierre: `activación pendiente`, worker vivo se
  conserva. El `taskkill` del worker quedó eliminado del script (el único
  taskkill restante es el sweep de huérfanos GUI de `C:\MT5`, previo).
- Crash recovery, backoff, singleton y el barrido de huérfanos quedaron
  intactos (harness S4e lo certifica).

**Tests obligatorios del mandato, certificación física en worker-kronos:**

- Trigger 5/5 (`sqx/cmd/sqx-mt5-worker/drain_windows_test.go`, binario
  GOOS=windows compilado en host, SHA256 `2c6cd9b7…d98`): señal dispara drain,
  señal perdida descartada, doble señal = un drain, Close sin inventar drain, e
  integración con el shutdown del lifecycle hasta `StateStopped`.
- Harness 33/33 PASS (`deploy/windows/session-worker/tests/
  Test-SessionWorkerUpdate.ps1` + `tests/worker-stub/main.go`, corrida limpia
  `run3e`, 01:58:35Z): S1 update con worker idle; S2 update con worker ocupado
  (activity en vuelo preservada 20s, luego salida limpia, sin kill); S3 crash
  durante la actualización (adopción con cierre probado exit=1);
  S4a binario ausente = pendiente conservando worker; S4b re-señal idempotente
  (una sola línea de drain por pid); S4c supervisor único (mutex); S4d señal
  perdida descartada + señal fresca drena (manual-reset); S4e muerte del worker
  sin drain = observación + backoff + relanzamiento.
- Defectos encontrados y corregidos durante la certificación (commit
  `7d70f46`): `CreateEvent` no aceptaba `ERROR_ALREADY_EXISTS` (handle válido
  sobre objeto preexistente) ni en el trigger ni en el stub; dos carreras de
  assert del propio harness (contar adopción/relanzamiento antes de que el
  supervisor escribiera la línea) y cierre prematuro del handle del evento en
  S4d (destruía el objeto y perdía la señal fresca).

## 2. Canary reuse guard (riesgo B)

**Antes:** la primera pasada del canario 0.2.143 (mismo SourceKey que el smoke
previo) fue respondida por el gate §14 con la evidencia reutilizada en <1s, sin
backtest físico.

**Ahora (commit `4b55ec4`):** `reuseBacktestArtifact` retorna el error tipado
no-reintentable `smoke_canary_source_reused`
(`domain.ErrSmokeCanarySourceReused`, clasificado con tipo Temporal dedicado)
cuando un request `smoke_canary=true` encuentra HTM durable de su SourceKey —
el mensaje exige despachar con SourceKey nuevo. No sobreescribe artefactos (no
hay path de escritura en el guard), no rompe el reuso ordinario (misma
SourceKey sin marca canaria reutiliza igual) y no crea otro mecanismo de
despacho (el canario sin HTM corre físico por el mismo flujo de siempre y
re-certifica PASS). Regresiones: reuse rechazado (caso exacto 0.2.143), reuso
normal emparejado intacto, canario sin HTM corre físico y certifica
(`TestMT5ArtifactBacktest_SmokeCanaryReuseRejected`,
`_RegularReuseUnaffectedByCanaryGuard`, `_SmokeCanaryWithoutHTMRunsPhysical`).

## 3. Despliegue y handover (worker-kronos)

- Script nuevo instalado en `C:\ProgramData\Stager\bin\` con backup
  `Start-EchoForgeSessionWorker.ps1.bak-20261015-230055`; SHA256
  `8DD1824038A3FA99B9EDF001D7D383CC0036BC00B666B887DE7DB7D837B827EB`; parse
  PowerShell 0 errores.
- Handover en ventana idle verificada (~83 min sin actividad; último evento del
  worker = canario r2 `activity.ok` 00:12:12Z): `schtasks /end` + `/run`.
  Hallazgo favorable: **el worker productivo pid 29292 NO murió** (el job de la
  tarea no mata al hijo); el nuevo supervisor lo adoptó por la ruta feliz.
- Postcondición verificada: un solo supervisor (pid 6292, script drain); un
  solo worker (pid 29292, `Path` bajo `releases\0.2.143`, vivo continuo desde
  23:44Z); `StagerReconcile` Last Result 0; stager status
  `activation b6a3a8e2 phase=committed`, current=running=0.2.143; 0 líneas
  taskkill fechadas post-handover.

## 4. Límites y pendientes

- **Transición de una sola vez:** el worker 0.2.143 en producción NO incluye el
  trigger (binario pre-cambio). La primera adopción de release con el
  supervisor nuevo quedará pendiente (`evento de drain ... inaccesible` en el
  log) mientras el worker vivo sea pre-trigger; se resuelve sola cuando la
  release stageada incluya el trigger y se ejecute el handover idle
  (`/end`+`/run`) — documentado en worker-troubleshooting §10. A partir de esa
  release, toda adopción posterior es drain automático.
- El camino drain del binario productivo (no del stub) se ejercitará con esa
  primera adopción real; el contrato está cubierto por los 5/5 tests del
  trigger compilados del mismo código.
- Pendientes owner pre-existentes intactos: autologon post-reboot, LiveUpdate
  6230, re-evaluación SCM.

## 5. Commits y trazabilidad

- symphony master (pusheado, `c82f27f..e4d37ff`): `4b55ec4` (trigger drain +
  guard canario + regresiones + supervisor drain + harness/stub + README),
  `7d70f46` (hallazgos del harness físico), `e4d37ff` (docs
  worker-troubleshooting §10/§11).
- Evidencia cruda en host: `C:\Users\ariadna-win\sw-harness\` (scripts,
  stub, binario de test, logs `run2/`, `run3e.out.log` con el RESUMEN 33/33).
- Vault: agent-run `80-agents/journal/agent-runs/
  2026-10-16-zcode-glm53-echo-forge-operational-safety.md`; este documento.
