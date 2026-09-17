---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-17-f05c-cert-f04-01-runtime-evidence-close

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (delta fechado `2026-09-17 — Cierre de evidencia runtime (veredicto READY FOR CERT-F04-01-EXEC; WINDOWS CONVERGED PASS persistido y re-verificado vivo)` + reemplazo de la sección "Próxima tarea única recomendada" con el estado vigente; sin cambio de clases A/B/C y sin cambio de estados de gates físicos)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-runtime-evidence-close.md` (creado)

## Motivo

- Misión NORMAL F05C-F04-01-RUNTIME-EVIDENCE-CLOSE del manager: cerrar únicamente el deployment/runtime evidence set previo a CERT-F04-01-EXEC, sin reabrir la conclusión WINDOWS CONVERGED (cerrada por owner con paso 0 elevado: PID 1700, PPID 30700, ejecutable `C:\ProgramData\Stager\releases\0.2.98\bin\sqx-mt5-worker.exe`, SHA256 == `0bceda4b…` MATCH EXACTO, `StagerRuntime` PID 30700 como `.\kor`). Read-only: sin reinstalar, sin reiniciar, sin detener procesos, sin publicar, sin campañas, sin modificar CERT.

## Fuentes usadas

- Encabezado de la misión (estado owner-cerrado) y [[Echo + Echo Forge — Deferred Certification Backlog]] (deltas convergencia/access-recovery/R1/preexec-lock del mismo día).
- SSH `aranea-ssh`: `mt5-kronos` viewer (identity) + `mt5-kronos-operator` (sólo lecturas: `Get-Process`, barrido por nombre, `Get-CimInstance`, `wmic`, `wevtutil`, `schtasks /TN`, `Test-Path`/`Get-Content` sobre `C:\ProgramData\Stager`, `Get-ChildItem C:\stager -Force`, `netstat -ano`).
- SSH `sqx-zeus`/`sqx-hera`/`sqx-kronos` (lecturas: `cat /opt/stager/CURRENT`, `ps aux`, `ls -l /proc/*/exe`, `cat /proc/<pid>/cmdline`, `ss -tnp`).
- Observabilidad `aranea-observability-ro`: `list_datasources` (Loki), `list_loki_label_names/values` 24h — verificó que el worker Windows no ingiere a Loki.

## Resolución aplicada

- Delta en el backlog que persiste **WINDOWS CONVERGED PASS** (owner, paso 0 elevado) con re-verificación viva a 2026-09-17T17:12Z: (1) parent/child — vivo confirma 1×`sqx-mt5-worker` PID 1700 + 1×`stager-runtime` PID 30700 (mismos PIDs del cierre ⇒ sin restart; PPID y hash con autoridad owner); CreationDate por canal INDETERMINABLE con boundaries exactos re-confirmados (`Get-CimInstance` 0x80041003, `wmic` ausente, `wevtutil` System Access denied, StartTime/Path ocultos); (2) stager release state — `C:\ProgramData\Stager` ACL-bloqueado por diseño (CURRENT/PENDING/target.yaml/hash por autoridad owner; corroboración viva: worker corriendo desde `releases\0.2.98\bin`); (3) `StagerReconcile` UNKNOWN — `schtasks /TN` "cannot find the path specified", CIM denegado, instalador la declara; no convertido a ABSENT; (4) poller — netstat PID 1700 con 2 ESTABLISHED (Temporal `192.168.31.46:7233` + OTel `192.168.31.60:14317`), cero workers duplicados, TaskQueue `sqx-mt5-queue` soportada por contrato de servicio @ baseline (no demostrable viva: Loki no ingiere el worker Windows, sin log legible); drain no declarado; (5) flota Linux 0.2.98 viva — Zeus PID 2633855 (ps), Hera PID 1231842 y Kronos PID 1203622 (cmdline `/opt/stager/releases/0.2.98/bin/symphony`), CURRENT `0.2.98` en los tres, PIDs estables desde sep13 03:21Z.
- Veredicto **READY FOR CERT-F04-01-EXEC**: A PASS (preexec), B PASS (convergencia cerrada + evidence close), C PASS (input frozen), D PASS (canales re-demostrados), E PASS (sin blockers nuevos). Observación registrada no bloqueante: artefacto F-03 legacy vivo en Hera (`/tmp/f03-cert`, ENV=`f03cert`, con conexión Temporal `:7233` adicional vista por `ss -tnp`), pre-existente a todas las auditorías y separado por ambiente; higiene opcional de drenaje pre-EXEC.
- Sección "Próxima tarea única recomendada" actualizada: prompt maestro `F05C-CERT-F04-01-EXEC` redactado y entregado (NO ejecutado); próximo paso = manager despacha EXEC.

## Validación

- Windows: todas las operaciones fueron lecturas; cero stop/start de procesos o servicios, cero instalación, cero writes de archivos, cero mutación de ACL/registry/scheduled tasks; `StagerReconcile` no tocada.
- Linux: sólo `cat`/`ps aux`/`ls -l`/`ss -tnp` allowlist; cero writes.
- Observabilidad: sólo discovery de labels (read-only estricto).
- Ningún estado de gate cambiado en vault; sin secretos leídos ni registrados; sin MCP nuevo; `C:\ProgramData\Stager` no ByPass-eado.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el delta fechado y la sección de recomendación en el backlog y borrar este log + el agent-run; ningún otro artefacto tocado.
