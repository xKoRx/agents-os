# WINDOWS-RUNTIME-HARDENING-KRONOS — Evidencia física (2026-10-15)

**STATUS: MT5_OPERATIONAL_CERTIFIED_WITH_CONSTRAINTS**

Sesión one-shot ZCode/GLM-5.3-Flash sobre el mandato "ECHO FORGE — WINDOWS MT5
RUNTIME HARDENING" (manager GPT-6). Base: WINDOWS-HANDOFF-KRONOS-20261015.md
(mismo directorio). Host: `WORKER-KRONOS` (VM 135, `mt5-kronos.lab.aranea.cl`),
ambiente operacional único de Forge (production, contrato §0). No se repitió la
campaña wave3t; la release 0.2.141 y su binario certificado no cambiaron.

## Resultado

`MT5_OPERATIONAL_CERTIFIED_WITH_CONSTRAINTS`: mecanismo operacional regularizado,
versionado y probado físicamente (crash-restart, singleton fail-closed, update
controlado por CURRENT, 1 backtest MT5 real con HTM + journals durables), con dos
límites declarados: (1) arranque desatendido post-reboot sigue sin garantía (gate
owner, sin autologon) y (2) hallazgo nuevo de drift de build MT5 por LiveUpdate.

## 1. Causa de la degradación de session 0 (mandato 1)

La sesión 0 NO es incapaz de MT5 — sufre una **degradación transitoria y
recurrente del presupuesto gráfico**, con recuperación:

- Línea temporal real del 14-oct (log `C:\MT5\slots\slot-2\logs\20261014.log.pre-smoke.bak`):
  los launches session-0 de 03:06–09:50 (smokes + wave3n/o) funcionaron; desde
  **10:36** (wave3p) TODOS los launches session-0 mostraron `Window MDI create
  failed` / `Document create frame from resource 131 failed` (10:36, 15:18,
  20:44, 20:49, 20:54, 21:08, 21:21). La ventana 16:42→20:44 reportada en el
  cierre anterior era la detección, no el inicio. La sesión interactiva
  materializó HTM todo el día.
- Windows Error Reporting (Application log): `RADAR_PRE_LEAK_64` de
  `metatester64.exe` build 6182 a las **09:07**, minutos antes del boundary;
  histórico del mismo evento: 03-jul, 06-ago, 01-oct, 13-oct (presión
  recurrente del tester). Event 1001 único del día.
- System log sin eventos en el boundary; única instalación de Windows Update
  ese día: Defender 19:54 (posterior al inicio). **Uptime del host 5.264.033 s
  (~61 días)** a las 12:00 del 14-oct: la degradación no vino de reboot ni de
  parches.
- **Probe físico 2026-10-15 11:03 local (session 0 sana hoy):** tarea efímera
  SYSTEM (`ForgeS0Probe`, borrada tras la prueba) lanzó
  `C:\MT5\slots\slot-2\terminal64.exe /portable /config:...\smoke\s0probe\tester.ini`
  (Expert SmokeProbe.ex5): `last test passed "successfully finished"`, exit 0,
  **HTM (23.028 B) + 5 PNGs materializados, cero `MDI create failed`** (evidencia
  en `C:\MT5\slots\slot-2\logs\20261015.log` 11:03).
- Modelo consistente: fuga/acumulación de recursos GUI de la sesión 0
  (compilaciones MetaEditor + tester) que agota el presupuesto gráfico del
  escritorio de servicios dentro de una jornada; se libera al terminar a los
  residentes (el zombie MetaEditor64 del 12-oct fue matado en el fix del
  14-oct) o con reboot. Dos incidentes con el mismo patrón: 14-ago ("ventana
  temprana del día", §8 de worker-troubleshooting) y 14-oct.

**Decisión (mandato 2):** restaurar `StagerRuntime`/SCM hoy NO conserva el
comportamiento certificado (una wave de 21 backtests ~5h no cabe en la garantía
de sesión 0; la sesión interactiva entregó 21/21 con HTM). El runner interactivo
supervisado queda formalizado como mecanismo canónico; `StagerRuntime` sigue
Stopped+Disabled y `target.yaml` mantiene `runtime.driver: windows-scm` como
declaración nominal (divergencia intencional documentada — el repo stager no es
local y no se mutó su schema a ciegas). Criterios de re-evaluación: reboot de
mantenimiento + probe session-0 PASS + decisión owner.

## 2. Mecanismo versionado (mandatos 3 y 4)

Nuevo paquete en el repo `xKoRx/symphony` `deploy/windows/session-worker/`:

- `Start-EchoForgeSessionWorker.ps1` — supervisor interactivo: relee
  `C:\ProgramData\Stager\CURRENT` en cada ciclo (~15s); lanza
  `releases\<CURRENT>\bin\sqx-mt5-worker.exe` con `ENV=production`; relanza ante
  crash con backoff exponencial 30s→10m (reset tras 600s estable); ante CURRENT
  avanzado termina el árbol del worker (`taskkill /T /F`) y ejecuta la release
  nueva; barre huérfanos GUI de `C:\MT5` sólo con el worker ausente; log de
  eventos `session-worker.supervisor.log`; logs por arranque
  `session-worker.{out,err}-<stamp>.log` (retención 20/14d).
  **Defecto corregido en la propia sesión:** la v1 esperaba al hijo con un loop
  bloqueante interno que dejaba la detección de CURRENT inalcanzable mientras el
  worker vivía (detectado en la prueba D; v2 con un único loop, instalada).
- `Install-EchoForgeSessionWorker.ps1` — instalación como administrador: copia a
  `C:\ProgramData\Stager\bin\` con backup + verificación SHA256, re-registra
  `\EchoForgeMT5WorkerSession` (Run As KoR, Interactive only, At logon +
  repetición 15 min, `ExecutionTimeLimit=0` — elimina el límite 72h que
  huérfanaba el worker, `MultipleInstances=IgnoreNew`) y elimina el launcher
  efímero `C:\Temp\session_worker.ps1`.
- `README.md` — procedimiento, rollback, verificación física y límites.

**Instalación física:** supervisor v2 SHA256
`13AF5E88FF36C45CD3CB0ED55006E8A369C96A5E3196BF493908D9F6A0C6F43F` en
`C:\ProgramData\Stager\bin\` (v1 `A8F2AF6E…F790` reemplazada, backup
`.bak-20261015-113628`); tarea re-registrada; `C:\Temp\session_worker.ps1`
ELIMINADO; staging de instalación conservado en
`C:\ProgramData\Stager\install\session-worker-20261015\`.

- **Singleton (mandato 4):** dos capas — supervisor único por sesión (mutex +
  `IgnoreNew`); el worker rechaza un segundo proceso fail-closed
  (`Global\echo-forge-sqx-mt5-worker`, `sqx/cmd/sqx-mt5-worker/singleton_windows.go`).
  La recuperación de leases/owners same-host la hace el propio binario
  (`previous_local_worker_dead_proven=true` tras muerte probada).
- **Staging de releases sin cambio:** `StagerReconcile` (SYSTEM, 1 min) sigue
  stageando desde el manifest de MinIO. **Hallazgo operacional: CURRENT es
  propiedad del stager** — repara divergencias manuales en ≤60s (observado en
  la prueba D). El update real (nueva release publicada) hace el swap vía
  supervisor en ≤30s tras el staging.

## 3. Pruebas físicas acotadas (mandato 7) — 2026-10-15

Sin nueva wave de 21; sin reboot del host; sin nueva release del worker.

- **A — Idempotencia:** `schtasks /run` con tarea viva → rechazada por
  `IgnoreNew` ("is currently running"); un solo supervisor, worker adoptado sin
  reinicio (PID 35616 intacto).
- **B — Crash → auto-restart:** `taskkill /F /PID 35616` → supervisor relanzó
  en <60s (PID 2256) desde `releases\0.2.141`; log del worker: singleton
  adquirido con `previous_local_worker_dead_proven=true`, recuperación
  same-host de owners habilitada, `env=production`.
- **C — Singleton fail-closed:** tarea efímera KoR /IT lanzando el exe por
  fuera → exit 1 (ruta única posible: rechazo del singleton), sin segundo
  proceso, canónico intacto. Tarea borrada.
- **D — Update controlado por CURRENT:** `StagerReconcile` pausado; release de
  prueba `0.2.141-supvtest` = **copia byte-idéntica del binario certificado**
  (SHA256 `BF247D61…EFC96` verificado en ambas rutas, NO es una release); swap
  de CURRENT → supervisor terminó el árbol del worker vivo (incl. hijo) y
  relanzó desde la ruta nueva en ≤30s; reversión idéntica; release de prueba
  eliminada; reconcile re-habilitado y CURRENT en `0.2.141`.
- **E — Backtest MT5 real de aceptación:** workflow `MT5BacktestArtifactWorkflow`
  `smoke-hardening-01-20261015` (run `01a14007-7ef7-78d1-8419-a0cff55427d1`,
  namespace `sqx-prop`, cola `sqx-main-queue` → activity `sqx-mt5-queue`)
  despachado con EX5 durable auténtico del finalista 89171ea6 (cohort wave2b,
  key `durable/mt5-export/v1/cd697133-…/06_mt5_ex5/final-89171ea6-….ex5`,
  220.836 B, SHA256 `92b025f2642b894e00c15fc7686a730be2238591d190dec378d04a4d538b7f20`
  verificado por descarga+hash local — coincide byte-exacto con SMOKE-SERIAL-3OF3.md).
  Ejecutado por el worker relanzado por el supervisor (PID 30840,
  `releases\0.2.141`). Resultado: `Tester last test passed "successfully
  finished" in 0:01:02.231` (12:28:11 local), `exit with code 0`, terminal en
  build 6182, **`activity.ok status=success` 15:28:23Z**; 5/5 evidencias
  durables publicadas 15:28:21–23Z bajo el prefijo nuevo
  `…/07_smoke_runtime_hardening_20261015/` (sin tocar `07_mt5_backtest/` de
  wave3t): `.htm` 787.084 B + `.tester.ini` 454 B + `.terminal.log` 7.164 B +
  `.tester.log` 4.429.154 B + `.agent.log` 5.531.638 B. El helper efímero de
  despacho (`sqx/tools/dispatchmt5smoke`, patrón `di.InitSelective("sqx-watcher")`)
  fue borrado tras la corrida; el repo quedó sin delta de herramientas. Nota:
  el ini del smoke usó `Symbol=NDX` con rango 2024-H1 (no la config certificada
  `NDX_SQX` 2025.07–2026.10): prueba de ciclo de vida, no de fidelidad; la
  descarga de historia completa (~40 min) no afecta la validez del ciclo
  worker→HTM→journals.
- NO probado físicamente: reboot del host (gate owner, ventana de
  mantenimiento) y update con una release real nueva (la ruta de swap es la
  misma probada en D; el primer rollout real la ejercita end-to-end).

## 4. Hallazgo nuevo: LiveUpdate de MT5 puede cambiar el build certificado

Durante la prueba E el terminal de slot-2 registró `LiveUpdate new version
build 6230 is available` y descargó los paquetes (11:49 local). El build vigente
en ejecución siguió siendo 6182 (el update se aplica al próximo arranque del
terminal). **Riesgo:** el próximo ciclo de backtests puede correr sobre build
6230 sin decisión explícita — drift del runtime físico que produjo la
certificación wave3t (21/21 sobre 6182). `Config\common.ini` del slot no tiene
clave de bloqueo; NO se mutó a ciegas. Opciones para el owner/próxima sesión:
(1) verificar y aplicar bloqueo de LiveUpdate por slot (clave en
`Config\common.ini` o switch del binario — requiere verificación física), (2)
bloqueo de red a los endpoints de MetaQuotes en las VMs de slots, (3) aceptar
el drift re-validando. Evidencia: `C:\MT5\slots\slot-2\logs\20261015.log` 11:49.

## 5. Límites declarados (mandato 5) — NO aprobados como gates

- **Arranque desatendido post-reboot:** sin garantía. La tarea es
  Interactive-only y no existe autologon (`AutoAdminLogon` ausente, verificado
  en el handoff previo). Tras un reboot una persona debe iniciar sesión KoR en
  la consola; el trigger At logon levanta supervisor+worker solos. Habilitar
  autologon o mecanismos equivalentes con credenciales es decisión de seguridad
  del owner; mientras no exista, este gate queda documentado como NO aprobado.
- **LiveUpdate (§4):** drift de build MT5 pendiente de decisión owner.
- `tscon 2 /dest:console` sigue siendo el remedio si la sesión de consola pasa a
  Disc (degradación gráfica de RDP documentada).

## 6. Sin cambios en lo certificado (mandato de alcance)

- Binario vivo = release 0.2.141 (`BF247D61…EFC96`), byte-idéntico al manifest
  de `xKoRx/symphony` @ `eab4302`; sin nueva release del worker.
- Sin cambios en Robust V2, Fidelity, ranking, promoción `finalist_promotion@1.0.0`
  ni integración con Echo. El backtest de aceptación publica bajo el prefijo
  nuevo `07_smoke_runtime_hardening_20261015/` (no toca `07_mt5_backtest/` de
  wave3t).
- Docs: `.agents/skills/worker-troubleshooting/SKILL.md` §10 (nueva) + nota en
  §9; `AGENTS.md` del repo actualizado (línea LocalSystem obsoleta); commit en
  master de symphony con los hashes de esta evidencia.
