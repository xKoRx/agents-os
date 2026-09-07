---
type: known_error
scope: application
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Symphony]]"
  - "[[Stager]]"
  - "[[Echo Forge]]"
related:
  - "[[stager-go-requires-current-pending-bridge]]"
  - "[[symphony-zeus-troubleshooting]]"
aliases:
  - stager PENDING thrash en noop
  - worker draining cada minuto Zeus
  - pending_sync=1 sin cambio de versión
confidence: high
source_session: "echo-forge-apply-selected-run-1786366035"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - area/symphony
  - kind/knownerror
  - project/echo-forge
  - tech/stager
  - host/zeus
---

# Stager Go escribe PENDING en noop y reinicia el worker en loop

## Síntoma

- En Zeus, `apply_selected_run` (u otras activities con `sqcli`) arrancan, copian a `EchoForgeRobustRunExporter` y lanzan `sqcli`, pero no terminan: setup queda `READY`.
- Logs del worker: `Detectado PENDING` + `worker draining` cada ~30–60s.
- Stager log: `result=noop before=0.2.40 after=0.2.40 pending_sync=1` sin release nueva.
- Temporal UI puede mostrar activities “rotas” / reintentos; no es el mismo fallo que metadata missing.

## Causa

Tras cutover a Stager Go (`0.2.40`), el stager marca `PENDING` aunque el resultado sea **noop** (misma versión). El worker ve `/var/lib/symphony/PENDING`, hace shutdown gracioso y reinicia. Con `max_concurrent_activity=1`, cualquier `sqcli` en curso muere.

## Impacto

- Workflows Echo Forge quedan a medias (ej. 13/16 `APPLIED`, 3 eternamente `READY`).
- Cola `sqx-main-queue` degradada por churn de worker.
- Confunde troubleshooting de `apply_selected_run` con bugs de metadata.

## Detección

```bash
ssh kor@192.168.31.101 'tail -n 40 /var/log/symphony/stager.log'
# buscar: result=noop ... pending_sync=1
grep -c "Detectado PENDING" /var/log/symphony/symphony-worker.log
```

Workflow de referencia: `sqx-main-00_configs-v1-XAUUSD-H1-L-1786366035` (run_id `91e79e2be9a01d189970d8dbdae49c3d`).

## Mitigación

1. Cortar el thrash: stager no debe escribir `PENDING` en noop / `pending_sync` sin cambio real de release.
2. Mientras tanto: detener stager o inhibir escritura de `PENDING` en Zeus para dejar terminar activities.
3. No confundir con [[sqx-import-metadata-silent-fallback]] ni mismatch `run_id` en `databank_metadata` (otro defect: workflow `1786323448` / flow_75).

## Evidencia

- Zeus `/var/log/symphony/stager.log` 2026-08-10 ~14:30–14:47 UTC: noop + `pending_sync=1` en loop.
- Worker: >1000 `Detectado PENDING` en el log vigente; reinicios ~cada minuto.
- Mongo `robust_run_setups` del run `91e79e2b…`: 13 `APPLIED`, 3 `READY` con metadata presente.
