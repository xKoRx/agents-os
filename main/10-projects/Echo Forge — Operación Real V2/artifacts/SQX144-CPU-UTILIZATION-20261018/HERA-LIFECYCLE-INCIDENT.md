---
type: incident_report
schema_version: 1
status: final
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
severity: low (sin pérdida durable; E2E completó por retry)
tags:
  - kind/incident
  - area/echo
---

# HERA-LIFECYCLE-INCIDENT — 2026-10-18T05:05:43Z "Stopping stager-runtime.service"

## Dictamen independiente

**El host Hera fue reiniciado por acción humana del owner** (no OOM, no despliegue, no crash, no CPU): sesión SSH de `kor` desde 192.168.31.162 a las 05:05 local emitió el reboot; systemd ejecutó el shutdown limpio (línea "Stopping stager-runtime.service" 05:05:43Z); boot 05:07:02Z. La actividad builder en vuelo murió con el host; el primer retry falló rápido por el estado dejado; el segundo retry (Kronos) completó y el E2E terminó COMPLETED sin intervención.

## Timeline (UTC)

| Hora | Evento | Evidencia |
|---|---|---|
| 04:08–04:10 | Rollout 0.3.1: workers Zeus/Kronos reiniciados con release nueva | `/opt/stager/releases/0.3.0` (04:01) y `0.3.1` (04:09) en Hera; PIDs worker Zeus 04:08, Kronos 04:10 |
| 04:36:24–25 | Activity builder (task 01_builder, proyecto custom) inicia en Hera; sqcli corriendo | worker log Hera "activity.start" + "Iniciando ejecución de comando" 04:36:25Z |
| 05:05:xx | `kor` abre sesión SSH pts/0 desde 192.168.31.162 (sesión de 0 s) y lanza reboot | `last -x` Hera: "kor pts/0 192.168.31.162 Sun Oct 18 02:05 - 02:05 (00:00)" (hora local) |
| 05:05:43 | Worker recibe **quiesce** por canal ETCD+archivo y systemd detiene la unidad (shutdown) | worker log: "Recibida señal: quiesce solicitado" file_quiesce_watcher.go:85 + etcd_quiesce_watcher.go:105, 05:05:43Z |
| 05:07:02 | Boot de Hera completo (LINUX RESTART 02:07:08 local en sysstat) | `uptime -s` = 02:07:02 local; `last -x` "reboot system boot … 02:07"; sar sa18 "LINUX RESTART"; `/var/crash` vacío |
| 05:07:09 | Worker nuevo arranca; error TRANSITORIO de activación SQX: `/home/kor/sqx/144` "no such file or directory" (disco SQXDATA aún sin montar al arrancar el worker); se auto-recupera | worker log Hera main.go:118 VersionNotFound 05:07:09Z; runs sqcli normales desde 05:09 |
| 05:09:25→27 | Retry del builder en Hera: sqcli exit 0 en 2105 ms con "Project stopped" en output → error marker → "success markers not found" → activity.error | worker log Hera sqx_executor.go:89/173 |
| 05:11:27 | Retry siguiente despachado a Kronos: builder inicia | worker log Kronos 01_builder |
| 06:20:42 | Builder completa en Kronos: 4154640 ms | worker log Kronos "Comando ejecutado exitosamente" |
| 06:21→06:58 | Resto del flujo (retests 649→22, exporters) distribuido Hera/Kronos/Zeus | worker logs 3 hosts |
| 07:39:44 | Última actividad del E2E (MT5 reconcile wave 10); flujo COMPLETED | worker log Hera tail; FlowRun 79385c32 COMPLETED 3h03m |

## Preguntas del mandato

- **Quién ordenó detener stager-runtime**: el shutdown del host (reboot emitido desde sesión SSH kor@192.168.31.162). El quiesce previo por ETCD/file llegó en el mismo segundo — mecanismo de drenaje de Forge; `/sqx-worker/production/maintenance/control` está hoy en `{}` (sin quiesce residual) y `maintenance/state/h0` en `completed` (14-oct).
- **¿Reinicio de sistema o contenedor?**: reinicio completo del host (sysstat "LINUX RESTART", `last -x` reboot, qemu-guest-agent 05:07:08Z). No hay apt/updates en la ventana, `/var/crash` vacío, dmesg no legible como echo-dev (innecesario: el patrón de last/auth apunta a acción manual).
- **¿OOM?**: no. `MemoryMax=infinity`, 98 GB RAM con ~1 GB usado en la ventana, sin marcadores OOM en logs accesibles, shutdown limpio con secuencia systemd completa.
- **Propagación a sqcli**: el JVM hijo (process-group propio del Execute) murió con el host sin llegar a escribir estado final del proyecto.
- **Por qué el siguiente intento falló sin success markers**: el retry 05:09:25Z re-ejecutó `sqcli -project action=start name=custom` sobre el proyecto cuyo run previo fue interrumpido; sqcli retornó en 2,1 s con "Project stopped" en la salida (error marker configurado) y sin "All tasks completed" ⇒ validación de markers falló (hipótesis respaldada por evidencia: el output efectivamente contuvo "Project stopped"; la lectura exacta del estado interno de sqcli no es observable). El retry posterior partió el proyecto desde cero (hooks limpian databanks, log Kronos 05:11:27Z) y completó.
- **Riesgo de repetición**: el riesgo real es "host reiniciado con actividad en vuelo" (operacional, no de software); la política de retries ilimitada de Forge lo absorbió (attempt 3 exitoso en otro host). Riesgo puntual conocido y de bajo costo: un retry inmediato tras un kill puede quemar un intento en el fast-fail "Project stopped"; candidato a mejora de producto (REMEDIATION-PLAN ítem 5).

## Nota de reconciliación

El agent-run del E2E 0.3.1 había registrado la causa como "churn systemd"; esta forense la precisa: el churn fue consecuencia del **reboot del host iniciado por el owner**, no un reinicio espontáneo del servicio.
