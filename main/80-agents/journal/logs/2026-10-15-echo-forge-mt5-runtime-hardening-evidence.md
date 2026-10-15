---
type: change_log
schema_version: 1
scope: session
created: "2026-10-15"
updated: "2026-10-15"
area: "[[Aranea]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
application:
entities:
  - "[[Echo Forge — Robust Run Selection V2]]"
related:
  - "[[WINDOWS-RUNTIME-HARDENING-20261015]]"
  - "[[WINDOWS-HANDOFF-KRONOS-20261015]]"
  - "[[2026-10-15-zcode-glm53-echo-forge-mt5-runtime-hardening]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-10-15-forge-mt5-runtime-hardening-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-15-echo-forge-mt5-runtime-hardening-evidence

Cambios de la sesión one-shot "ECHO FORGE — WINDOWS MT5 RUNTIME HARDENING" (ZCode/GLM-5.3-Flash, manager GPT-6). Veredicto: `MT5_OPERATIONAL_CERTIFIED_WITH_CONSTRAINTS`.

## Repo `xKoRx/symphony` (commit `b5d65b9`, pusheado a origin/master sobre `eab4302`)

- Nuevo `deploy/windows/session-worker/` (supervisor interactivo + instalador + README): mecanismo canónico de arranque/supervisión/update del worker MT5 en worker-kronos; reemplaza `C:\Temp\session_worker.ps1`. Sin cambios Go: la release 0.2.141 y su binario certificado no se tocaron (sin nueva release).
- `.agents/skills/worker-troubleshooting/SKILL.md`: §10 nueva (causa de la degradación session 0 con línea temporal y RADAR_PRE_LEAK, mecanismo canónico, certificación de ciclo de vida A–E, límites) + nota de actualización en §9.
- `AGENTS.md`: línea obsoleta "MT5 no escribe .htm bajo LocalSystem" reemplazada por el estado vigente (sesión interactiva + supervisor; StagerRuntime Disabled por recurrencia de degradación, no por imposibilidad).

## Host worker-kronos (via aranea-ssh `mt5-kronos-admin`)

- Instalado `C:\ProgramData\Stager\bin\Start-EchoForgeSessionWorker.ps1` (SHA256 `08BD7361…4D94`; backups v1 `A8F2AF6E…` y v2 `13AF5E88…` como `.bak-*`); tarea `\EchoForgeMT5WorkerSession` re-registrada (At logon + repetición 15 min, sin límite 72h, Interactive only, Run As KoR); `C:\Temp\session_worker.ps1` eliminado; staging en `C:\ProgramData\Stager\install\session-worker-20261015\`.
- Pruebas físicas acotadas (todas revertidas/limpias): probe session-0 SYSTEM (tarea `ForgeS0Probe` borrada), singleton probe KoR (tarea `ForgeSingletonProbe` borrada), update por CURRENT con release de prueba `0.2.141-supvtest` (copia byte-idéntica de 0.2.141, directorio eliminado; `StagerReconcile` pausado ~3 min y re-habilitado; CURRENT restaurado a `0.2.141`).
- Backtest de aceptación: `smoke-hardening-01-20261015` success, evidencias durables en `07_smoke_runtime_hardening_20261015/` (prefijo nuevo).

## Vault

- Nuevo `10-projects/Echo Forge — Robust Run Selection V2/artifacts/mt5-serial-recovery-20261014/WINDOWS-RUNTIME-HARDENING-20261015.md` (evidencia canónica de esta sesión).
- Nuevo agent-run `80-agents/journal/agent-runs/2026-10-15-zcode-glm53-echo-forge-mt5-runtime-hardening.md` y feedback `80-agents/journal/feedback/session/2026-10-15-forge-mt5-runtime-hardening-feedback.md`.
- `WINDOWS-HANDOFF-KRONOS-20261015.md`: se añade cross-referencia al documento nuevo (estado parcialmente superado en mecanismo de arranque).

## Pendientes owner (no aprobados por esta sesión)

1. Autologon/arranque desatendido post-reboot: decisión de seguridad; gate NO aprobado.
2. LiveUpdate MT5 (6182→6230 descargado en slot-2): decidir bloqueo verificado vs aceptar drift; NO se mutó `Config\common.ini` a ciegas.
3. Re-evaluación de `StagerRuntime`/SCM sólo tras reboot de mantenimiento + probe session-0 PASS.
