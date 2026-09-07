---
type: change_log
schema_version: 1
scope: session
created: "2026-08-20"
updated: "2026-08-20"
area: "[[Echo]]"
project: "[[Echo - Discovery y Estado]]"
application: "[[echo-core]]"
entities:
  - "[[Echo]]"
  - "[[echo-core]]"
  - "[[Echo - Discovery y Estado]]"
related:
  - "[[2026-08-20-echo-hotfix-merged-and-prod-audit]]"
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

# Echo: síntesis de OPEN nativo implementada, testeada y deployada en prod

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated (repo externo + prod + notas de vault)
- **Repo `xKoRx/echo`:** commit `e25165ba` en master (pusheado a origin): constructor `NewTradeJournalOpenFromCloseResult` en `v3/sdk/domain/trade_journal.go` (+tests) y síntesis en `handleExecutionCloseWithTelemetry` (`v3/core/internal/functions/trade_journal.go`, +tests). Rama `fix/native-open-synthesis` eliminada tras el merge ff.
- **Prod `192.168.31.71`:** deploy de `echo-core` 20-08 22:26 vía `build_v3.sh core` + `deploy-prod.sh core` (reemplazo atómico + restart). Backup previo en el host: `echo-core.bak-20260820-pre-synthesis` (md5 del binario anterior registrado).
- **Archivo(s) vault:**
  - `10-projects/Echo/Echo - Discovery y Estado.md` (causa raíz cerrada, tareas, bitácora)
  - `30-resources/applications/echo-core-changelog.md` (entradas 2026-08-20 y 2026-08-19)

## Motivo

- El owner ordenó corregir el bug de nativas, asegurar con tests y desplegar. Investigación con evidencia: los EAs de los terminales son pre-05-07 y no envían `lot_size` en opens nativos → core rechazaba opens → closes caían en `close_without_open` → 0 filas NATIVE desde el 1-jun. Se eligió la mitigación core-only (síntesis del OPEN desde el CloseResult) por ser deployable desde Linux, segura con EAs viejos y nuevos, y con fuente durable (sin la carrera de `active_positions`).

## Fuentes usadas

- Investigación de subagente sobre cadena EA→bridge→core + logs/BD de prod (read-only).
- Implementación de subagente (branch + tests) revisada y aceptada por el parent antes del merge.

## Resolución aplicada

- Síntesis solo ante `ErrCloseWithoutOpen` + NATIVE; ante payload incompleto o fallo de persistencia se conserva el rechazo original. Idempotente ante reentregas. Path ECHO intacto. No se tocaron migraciones, matview, gateway, bridge ni front.
- Post-deploy: servicio active, md5 del binario nuevo verificado en host, arranque limpio (únicos ERROR son del proceso anterior cerrándose), pipeline ECHO insertando. Sin actividad nativa aún (mercado calmo): la síntesis se manifestará con el próximo close nativo real.

## Validación

- `go build ./v3/sdk/... ./v3/core/...` OK; `go test` core PASS; sdk PASS salvo 3 fallos preexistentes que requieren infra real (verificados idénticos en master vía worktree).
- `systemctl is-active echo-core` = active; `journalctl` post-restart sin errores nuevos; `trade_journal` con inserts ECHO posteriores al audit (2540→2558).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Prod: `ssh kor@192.168.31.71` → `cp /home/kor/echo/echo-core.bak-20260820-pre-synthesis /home/kor/echo/echo-core && sudo systemctl restart echo-core`.
- Repo: `git revert e25165ba` en master + push.
- Vault: revertir ediciones listadas y borrar este log.
