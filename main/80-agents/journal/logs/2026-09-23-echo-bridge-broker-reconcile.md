# Change Log — 2026-09-23 Echo bridge broker reconcile (diagnóstico + fix + testing + master)

Sesión: diagnóstico read-only PROD del incidente "WSF NEW! (183623) no recibe copias", implementación del fix de reconciliación de broker del echo-bridge, deploy/validación física en testing (dev-win) y fusión a master. Autorización owner explícita para implementar (Opción C), desplegar a testing y llevar a master.

## Repositorio Echo (fuera del vault)

- Commit `c99aee06` `fix(bridge): reconcilia broker de sesión/pipe con la config canónica` — 15 archivos (session: interfaces/execution_session/command_consumer/session_manager; internal: pipe_handler/reference_pipe_handler/pipe_manager/bridge/http_server) + tests nuevos y `TestHTTPServer_WithCallback` actualizado al nuevo contrato (callback también en re-registro).
- **Fusionado FF a `origin/master`** (`5dd998f1..c99aee06`) y rama `fix/bridge-session-broker-reconcile` publicada. Clon principal `~/go/src/github.com/xKoRx/echo` queda divergido (ahead 1 = front `3596fc48` de otra sesión sin destino decidido; behind 1 = c99aee06) — decisión owner.
- Build Windows `c99aee06` (go1.27.1, -trimpath -buildvcs, `vcs.modified=false`) SHA256 `452fae86…ccc51`.

## Testing (dev-win 192.168.31.132 / DEV-WIN)

- Desplegado `C:\aranea-dev\echo-bridge-fix\` (echo-bridge.exe + launcher detached) corriendo en **:8082** conectado a etcd/Kafka/PG DEV.
- Nueva key etcd DEV `/echo/development/bridge/http_port=8082` (el default 8081 lo ocupa el bridge DEV viejo `echo-bridge-v3` PID 5240, intocable por permisos del usuario SSH — pararlo/reasignar puerto = owner).
- E2E forzado PASS: registro sin config → pinned `WSFMARKETS` (bug reproducido); config canónica `WSF` por Kafka → reconciliación automática de sesión; comando → `broker=WSF broker_symbol=USDJPYc` (antes `USDJPY` plano → 999).
- Limpieza: mensajes de prueba tombstoneados en Kafka, schtasks de prueba eliminadas, http.server temporal detenido. Herramientas dejadas en `~/aranea/work/bridge-broker-reconcile-20260923/` (worktree, launcher, ktool productor sarama).

## Sistema 1

- Creado `80-agents/memory/public/known-errors/echo-bridge-session-broker-pinned-to-self-declared-broker.md` (L3): EA autodeclara broker con fallback a compañía normalizada; sesión pinned; detransform cae a identidad; falla silenciosa sin filas en journal; mitigación deploy ≥ c99aee06 o alias en symbol_mappings.
- Creado `80-agents/journal/agent-runs/2026-09-23-zcode-glm-5.3-flash-echo-bridge-broker-reconcile.md`.
- Creada `80-agents/journal/feedback/system-1/2026-09-23-echo-bridge-session-feedback.md` (gates MCP sin elicitation, MCPs con sesión perdida, patrón launcher-detached para procesos persistentes en hosts Windows vía MCP SSH).

## Pendiente (owner)

- Deploy del bridge `c99aee06` en PROD `mt4-real` + restart (auto-repara la sesión de la cuenta `183623`).
- Parar/reemplazar el bridge DEV viejo en dev-win y decidir puerto definitivo.
- Push/decisión del commit front `3596fc48` en el clon principal (master local divergido).
- Proponerse como mejora de skill de auditoría: discriminador Loki `|= "detransformed"` como paso estándar ante "cuenta no copia".
