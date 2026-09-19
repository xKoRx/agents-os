---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-17"
updated: "2026-09-17"
aliases:
  - "Daedalus — Development Agents MCP Access & Gaps"
tags:
  - area/aranea
  - tech/mcp
  - kind/access-matrix
---

# Daedalus — Development Agents MCP Access & Gaps

> Corte documental 2026-09-17. Alcance EXCLUSIVO: MCP Access Plane consumido por coding agents de Daedalus en Echo/Echo Forge. Router: [[aranea-mcps-expert]]; arquitectura/inventario: [[AGENT-PLATFORM - MCP Access Plane - Architecture]]; procedimientos: runbooks de familia. Esta nota reconcilia evidencia existente: NO realiza nuevos smokes y NO redefine roadmaps de producto.

## Veredicto ejecutivo: bloqueo REAL por falta de MCP

**NINGUNO DEMOSTRADO en los estados vigentes revisados de Echo y Echo Forge.** No crear nuevos MCP para desbloquear una tarea sin identificar primero una operación concreta detenida, el perfil exacto y su `POLICY_DENIED`/`Access denied`/ausencia de herramienta, y descartar el camino autorizado existente.

- **Forge:** el bloqueo real de `CERT-F04-01` fue `persistence_deadline_required` en `mt5_compile`, un defecto de SOURCE, NO del MCP. Fix `49fce32…` verificado; release `0.2.99` publicada y desplegada en flota Linux/Windows con proof de source/manifest/worker y evidence publisher. Estado documental: `CERT-F04-01 = BLOCKED / READY TO RERUN`; próximo paso RERUN físico desde cero. No volver a pedir MCP de Windows/MinIO/Temporal para explicar ese bloqueo. Autoridad: [[Echo + Echo Forge — Deferred Certification Backlog]] § estado de entrada y delta C1/C2 2026-09-17.
- **Echo:** E-04 T21/AC-37 depende del golden Forge auténtico y cross-lane real; NO hay un fallo de permisos MCP documentado como causa inmediata. E-06 sigue su propio desarrollo/validación física, no se clasifica como bloqueo MCP por inferencia. Autoridad: [[Echo + Echo Forge — Deferred Certification Backlog]].
- **Windows evidence:** resuelto `ACTIVE/CERTIFIED` para inspección privilegiada de `worker-kronos` mediante publisher SYSTEM y lectura no-admin; ya permitió certificar el rollout de la release `0.2.99`. El publisher NO otorga admin ni certifica automáticamente el flujo F-04; no solicitar otro seed por inercia. Autoridad: [[aranea-ssh-mcp]], backlog de certificación.

No volver a mezclar "no existe la tool X" con "la fase Y está bloqueada por X". Una limitación de autoridad es un contrato de seguridad, NO un bloqueo real sin misión detenida que la requiera. Telegram, Jaeger MCP, Temporal ops, etcd RW y Kafka/Flink PROD **NO SON BLOQUEOS DE ECHO/FORGE DEMOSTRADOS A ESTE CORTE**. No convertirlos en lista de tareas ni proponer implementarlos preventivamente. **MinIO RW dejó de ser pendiente el 2026-09-18 (noche):** existe como `aranea-minio-rw` (:3011, identidad = key owner full, certificado 4/4 server + 6/6 chain) por decisión owner — la herramienta NO debe volver a citarse como "MinIO RW pendiente".

## Semántica de evidencia

- `SERVER CERTIFIED`: backend/proxy/superficie certificada en `mcps`.
- `CONSUMER CERTIFIED`: cliente específico de Daedalus (`Cursor`, `ZCode`, `Codex`) pasó config/env/handshake/tools/call; PASS de un cliente no certifica a otro.
- `ACCESS BLOCKER PROVEN`: misión vigente con operación exacta requerida, ruta/perfil autorizado, fallo efectivo demostrado, sin alternativa autorizada disponible y estado formal BLOCKED por ese fallo.
- `PENDING SMOKE`: evidencia incompleta del cliente, no equivale a misión de producto bloqueada.

## Inventario MCP registrado: 13 capabilities (2026-09-17)

| Puerto | Capability | Autoridad / límite certificado |
|---:|---|---|
| 3000 | `aranea-ssh` | perfiles por host: SQX `echo-dev` no-root; MT5 viewer u operator `echo-dev` no-admin; Docker DEV root; Echo PROD viewer; publisher SYSTEM Windows sólo evidencia publicada |
| 3001 | `aranea-postgres-ro` | Echo PROD RO |
| 3002 | `aranea-postgres-rw` | Echo DEV data RW; no inferir CREATE de esquema |
| 3003 | `aranea-mongo-forge-ro` | Mongo Forge PROD RO, 18 tools |
| 3004 | `aranea-mongo-forge-rw` | Mongo Forge DEV RW, 27 tools |
| 3005 | `aranea-hasura-prod-ro` | PROD strict RO, exactamente 3 tools post-H1; sin export_metadata, SQL ni mutaciones |
| 3006 | `aranea-hasura-dev-admin` | DEV admin, 9 tools incluido `run_sql`; E-05 usó este camino para migración 063 DEV |
| 3007 | `aranea-kafka-dev-admin` | Kafka DEV, 19 tools; no PROD |
| 3008 | `aranea-flink-dev-admin` | Flink DEV REST, 22 tools sin SQL; runtime Docker DEV usa SSH separado |
| 3009 | `aranea-observability-ro` | Grafana/Prometheus/Loki ARGUS, 22 tools RO; sin Jaeger toolset |
| 3010 | `aranea-temporal-ro` | 28 tools RO namespaces `sqx-dev`,`sqx`,`sqx-prop`; sin start/signal/cancel/terminate |
| 3011 | `aranea-minio-rw` | **RW full** (2026-09-18 noche): identidad = key owner, todos los buckets (put/get/delete/copy/presign); certificado server 4/4 + smoke chain kor 6/6. Ex `aranea-minio-ro` (lectura IAM acotada) — histórico |
| 3012 | `aranea-etcd-ro` | cuatro tools RO; ocho prefixes allowlisted, nombres de secretos filtrados; sin mutadores; cluster sin TLS/auth requiere hardening separado |

Los inventarios históricos de 9/10/11 capacidades no sustituyen este corte; comprobar runtime ante cambios posteriores. Los límites por capability se consultan en los runbooks, no se transforman en tickets sin uso probado.

## Estado de consumidores: deuda propia del plano, NO blocker de proyecto probado

- **Cursor:** las 10 capacidades base certificadas anteriormente, Temporal añadida y smoke del trío Temporal/MinIO/etcd `3/3 PASS` el 2026-09-17. No confundir con un nuevo re-smoke total 13/13. **2026-09-18 noche:** entry renombrada a `aranea-minio-rw` (misma URL, bearer sin cambio de valor; smoke funcional RW 6/6 vía chain kor).
- **ZCode:** baseline 10/10 al 2026-09-16; altas 3010–3012 aplicadas por patcher kor 2026-09-17 (shape) y runtime funcional certificado 2026-09-18 vía chain kor. **Rename minio → `aranea-minio-rw` pendiente de patcher kor** (stageado 2026-09-18 noche en `/tmp`; el valor del bearer no cambia, sólo nombre de entry/var).
- **Codex:** baseline nativo 10/10 al 2026-09-16, `bearer_token_env_var`; runtime funcional 2026-09-18 vía chain kor. **Rename minio → `aranea-minio-rw` pendiente del mismo patcher kor.**

Completar esos smokes si una sesión de ZCode/Codex requiere las tools nuevas. No declarar bloqueo Echo/Forge sólo por el pendiente documental; no afirmar PASS sin prueba individual. El patcher tri-client stageado se opera con autoridad autorizada sobre los archivos de `kor`; sin ampliar ACL ni imprimir bearer.

## Windows: acceso de evidencia ya resuelto

`AraneaEvidencePublish` ejecuta SYSTEM cada cinco minutos y publica JSON sanitizado en `C:\ProgramData\Aranea\evidence\stager-evidence-latest.json`. El coding agent lo consume RO por `aranea-ssh` + `mt5-kronos-operator` (identidad `echo-dev` no-admin, `Get-Content`/`Get-Item`). Certificación 2026-09-17: identidad, self-hash, dos publicaciones, lectura real, ACE write-denied y negativos viewer. `mt5-kronos+sftp-download` = `POLICY_DENIED` 3/3; no recomendarlo. Requisitos de evidencia runtime: edad `generated_at_utc` <=15 min y `partial=false`; stale/ausente => UNKNOWN, diagnosticar publisher. El backlog CERT-F04-01 C2 documenta su uso posterior para observar Windows `0.2.99` y SHA del worker exacto al manifest. No confundir con habilitación de admin Windows o certificación física de la campaña.

## Regla de apertura de un nuevo MCP o ampliación

Abrir sólo ante: (1) tarea ID/SPEC vigente y verbo requerido; (2) target/ambiente; (3) caller Daedalus concreto; (4) evidencia de fallo de acceso real; (5) inexistencia demostrada de ruta autorizada existente; (6) mínimo permiso necesario y controles de seguridad/rollback; (7) smoke de servidor y consumidor. Si una operación existente como `deploy_release.sh`/Stager ya publica y despliega artefactos, no inventar `MinIO RW` para el mismo objetivo. Si F-04 falla por código o por falta de golden físico, no inventar un problema de permisos.

## Fuentes canónicas

[[Echo + Echo Forge — Deferred Certification Backlog]], [[AGENT-PLATFORM - MCP Access Plane - Architecture]], [[aranea-mcps-expert]], [[aranea-ssh-mcp]], [[aranea-temporal-mcp]], [[aranea-minio-mcp]], [[aranea-etcd-mcp]], [[aranea-observability-mcp]], [[aranea-mcp-capability-plane]], [[ACCESS-CERTIFICATION]]. Esta nota no contiene secretos ni sustituye un probe del runtime vivo.
