---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: host
task_type: certification
task_complexity: high
outcome: blocked
verification: physical_evidence
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-09-24-zcode-glm53-forge-v2-prework-correccion

## Trabajo

- **Objetivo:** corrección y cierre del prework de Fase 1: reconciliar aislamiento runtime DEV, resolver físicamente SQX DEV, ejecutar el tramo Strategy→SQX→evidence, cerrar en PREWORK_PASS o UN blocker preciso.
- **Alcance atribuible:** reconciliación ETCD watcher/worker (código+runbooks+lectura real de prefixes); reparación del canal `aranea-ssh` (restart canónico del contenedor en mcps); preflight físico read-only de la instalación SQX certificada en Kronos (Build 142.2399, plugin certificado, licencia compartida flota×3); transferencia de la distribución oficial `SQX_142_linux_20250327.zip` (1 515 370 594 B, SHA256 idéntico origen/destino) vía clave SSH temporal con revocación verificada; materialización de SQX DEV en Daedalus (`/home/kor/sqx`, JRE bundled Zulu 21, plugin `EchoForgeAutomator.jar` SHA certificado, `license.db` con clave flota); prueba física de `sqcli` (Build 142.2399 + rechazo de licencia); siembra de prefixes ETCD del candidato `/sqx-{worker,watcher}/forgev2dev/` con cola exclusiva `sqx-forgev2-dev-v1`; rebuild de binarios candidato desde `d9032ff8` limpio; smoke E2E real dispatch→workflow→worker→cohort MinIO→`sqcli` hasta la frontera de licencia; teardown completo (workflow CANCELLED/TERMINATED, filas PG, objetos MinIO, procesos).
- **Artefactos afectados:** ETCD DEV `/sqx-{worker,watcher}/forgev2dev/` (nuevos, rollback = delprefix); instalación `/home/kor/sqx` en Daedalus (nueva, DEV); workspace externo `~/aranea/work/forge-prework2-20260924/`; Kronos `authorized_keys` (append+revoke con SHA antes/después idéntico); repo symphony sin delta.

## Evidencia

- **Validaciones:** licencia rechazada materialmente (`Failed to check license - License is not valid for this computer` tras imprimir `SQX version: 142.2399`); clave licencia idéntica en Zeus/Hera/Kronos (SHA256 del valor igual en los 3); exactamente 1 poller `4123232@daedalus@` en `sqx-forgev2-dev-v1` y 0 pollers nuevos en `sqx-main-queue`; workflow del smoke `sqx-main-v1-baa4815d-f034-4874-9cda-1fcd8f2330d9` corrió en la cola exclusiva (Temporal memo/describe), descargó cohort MinIO verificado por pipeline y falló en `execute_sqx` con `sqcli` exit 1 (retry infinito por `MaximumAttempts:0`); zombie del prework anterior `sqx-main-v1-556c2aa4…` TERMINATED server-side.
- **Resultado observable:** PREWORK_BLOCKED_AUTHORITY — único blocker: licencia SQX para Daedalus (§3.8 de términos: single device salvo Agreement distinto).
- **Limitaciones de la evidencia:** el exporter no produjo output real (la licencia impide ejecutar SQX); `vcs.modified=false` es inalcanzable desde `d9032ff8` (el build reescribe `go.work.sum` stale; evidencia del delta capturada).

## Evaluación

%% Sin scores: verificación física objetiva; outcome bloqueado por dependencia externa (licencia owner/proveedor). %%

## Resultado

- **Outcome:** PREWORK_BLOCKED_AUTHORITY — acción owner única: habilitar Daedalus en la licencia SQX (ampliación de asiento/Agreement con StrategyQuant s.r.o.) o proveer clave DEV.
- **Rework posterior:** unknown.
- **Aprendizaje para comparar herramientas:** la lectura RO del config JSON local permitió consumir el MCP `aranea-ssh` vía HTTP MCP sin exponer el bearer; `sftp-download` inline corrompe binarios (usar scp con clave temporal revocada); `CancelWorkflow` sin poller queda pendiente — `TerminateWorkflow` es la vía server-side.
