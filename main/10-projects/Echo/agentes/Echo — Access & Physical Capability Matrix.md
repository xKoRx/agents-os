---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
project: "[[Echo — Live Platform V1]]"
related:
  - "[[Echo — E-02 Control Safety, Auth and Journal Recovery]]"
  - "[[Echo — E-05 Analytics Convergence A0]]"
aliases: []
tags:
  - kind/doc
  - area/echo
  - project/echo
created: "2026-09-14"
updated: "2026-09-14"
---

# Echo — Access & Physical Capability Matrix

## Propósito

Certificación independiente de mínimo privilegio y capacidad física para desarrollar, verificar, integrar y certificar Echo Live Platform V1. Autoridad: contrato/spec actual > source actual > documentación histórica. Corte: 2026-09-14. Resultado global: ACCESS_CERTIFICATION_BLOCKED porque el carril inmediato E-02 carece de superficies físicas Kafka, Hasura DEV y control Flink/Gateway.

## Contenido

### Estado global

`ACCESS_CERTIFICATION_BLOCKED`. E-02 no puede reabrir su certificación física de cierre: PG17/062 y observabilidad READ están disponibles, pero faltan Hasura DEV data/metadata, Kafka producer/consumer para PublishSync/redelivery, control Flink restart/recovery y un target físico Gateway/Core/Bridge. E-05 queda `PARTIAL`; no se modificó ni reconcilió.

### Inventario MCP/tool físicamente descubierto

| Superficie | Tool/MCP real | Entorno | Privilegio declarado/observado | Evidencia | Estado |
|---|---|---|---|---|---|
| SSH | `mcp__aranea_ssh__*` | DEV/SQX, Docker DEV, MT5 | operator, Docker operator, MT5 viewer/operator | `list_connections`, `hostname`, `id`, `run_command`, temp-file create/read/remove | PASS acotado; no restart/deploy probado |
| PostgreSQL RO | `mcp__aranea_postgres_ro__*` | PROD Echo | read-only | identidad PG17.6; SELECT/catalog; write privileges false; CREATE TEMP rechazado por validator | PROD_READ PASS; PROD_WRITE DENIED |
| PostgreSQL RW | `mcp__aranea_postgres_rw__*` | DEV Echo | data RW, sin app-schema CREATE | SELECT; reversible INSERT/ROLLBACK; temp DDL; `has_schema_privilege(echo,CREATE)=false` | DATA_RW PASS; DDL_MIGRATION FAIL |
| Mongo Forge | `mcp__aranea_mongo_forge_ro/rw__*` | Forge | Forge-only | tool inventory; no Echo source dependency proven | LEGACY_OR_UNUSED for Echo |
| GitHub | `mcp__codex_apps__github_*` | `xKoRx/echo` | read plus admin/write tools exposed | login, repo permissions, branches, commit/diff/file reads; no write called | READ PASS; write authority NOT_TESTED |
| Hasura/Kafka/Flink/StateFun/etcd/observability MCP | ninguno con esos namespaces en `ALL_TOOLS` | — | no callable agent surface | inventory real de tools + endpoint auth checks | ACCESS GAP |

### Surface Matrix

| Surface / env | Required verbs | Actual tool / positive probe | Negative/safety probe | Resultado / Echo lanes |
|---|---|---|---|---|
| SSH SQX DEV | READ, EXEC_DIAGNOSTIC | `hostname`, `id`, `ps`, `ss`, `systemctl`, bounded journal, temp file lifecycle en `sqx-zeus/hera/kronos` | `sudo -n -l` fue `POLICY_DENIED`; no restart/deploy ejecutado | READ/EXEC_DIAGNOSTIC PASS; RESTART/DEPLOY NOT_TESTED; E-02…E-13 diagnóstico |
| SSH Docker DEV | READ, EXEC_DIAGNOSTIC, controlled DEV container operations | `whoami=root`, `docker ps`, compose list, Docker service status, Hasura/Flink health, PG17 disposable | scope es DEV; no product/production restart; no secret values impresos | READ/EXEC_DIAGNOSTIC PASS; DEV container authority AVAILABLE; E-02/E-05 physical support parcial |
| SSH MT5 viewer/operator | READ, EXEC_DIAGNOSTIC, test filesystem | operator process/filesystem probes y temp file create/read/remove; viewer safe/destructive commands rechazados | Windows operator no Administrators/Medium Integrity; no terminal process, no matching pipe | operator READ/diagnostic partial; viewer READ only; E-06…E-09 gaps |
| PostgreSQL PROD | SELECT, catalog, views/functions, read-only tx | `current_database=echo`, user `mcp_echo_prod_ro`, PG17.6, tx read-only on, schemas/objects/privileges | write privileges INSERT/UPDATE/DELETE false; CREATE TEMP rejected | PROD_READ PASS; PROD_WRITE/DDL DENIED; E-02/E-05/E-06…E-13 read evidence |
| PostgreSQL DEV data plane | SELECT, controlled DML, rollback, constraints | user `mcp_echo_dev_rw`, tx read-only off; SELECT; INSERT `MANUAL_FIXTURE` inside ROLLBACK; zero residual rows | rollback verified by follow-up count 0 | DATA_RW PASS; E-02/E-05…E-13 |
| PostgreSQL DEV migration plane | CREATE/ALTER/DROP app schema, migration up/down | temp table create/alter succeeded; DB/schema CREATE privileges false | no app-schema migration attempted | DDL_MIGRATION FAIL via PG MCP; E-02 blocked until authorized migration workflow |
| Disposable PostgreSQL | destructive PG17 migration harness | Docker DEV pulled `postgres:17`; PG17.11 ready; E-02 062 up/down/up physically applied in disposable container; table/index and drop verified; container/temp files removed | no production DB touched | PASS; E-02 PG17 062 READY; E-05 PG17 environment READY |
| Hasura PROD | query/export/read metadata | direct health/version 200; metadata without secret 401 | no-secret metadata mutation/read rejected; no mutation called | HASURA_PROD_READ NOT_CERTIFIED (health only); mutation boundary observed; E-02/E-05 gaps |
| Hasura DEV data | GraphQL query/mutation with required role/header | health/version 200; `__typename` 200; protected `accounts` query returned auth error without header | admin secret not printed; no data mutation | DEV data READ/WRITE BLOCKED: no callable MCP, no bearer, no CLI; E-02/E-05/E-06/E-10/E-13 |
| Hasura DEV metadata | export, consistency, apply/reload, track/permissions/hooks | `/v1/metadata` without secret 401; `hasura` CLI absent on Docker host | no metadata mutation | READ/WRITE BLOCKED; exact missing MCP/authorized CLI; E-02/E-05/E-06/E-13 |
| Kafka DEV/test | broker read, bounded consume, produce, key/headers/group behavior | TCP reachability from Docker DEV to `192.168.31.44:19091..19096`; `kcat` and Kafka CLI absent | no PROD write; no admin action | READ/WRITE NOT_TESTED; E-02 PublishSync/redelivery BLOCKED; E-07…E-09 blocked |
| Flink/StateFun DEV | health, jobs, task managers, checkpoints, logs | REST `/overview`, `/jobs`, `/taskmanagers`, current job RUNNING, 2 slots, checkpoint 499 completed, bounded logs | cancel/stop/restart/resubmit not executed; no production job touched | READ/status/checkpoints PASS; control verbs NOT_TESTED; E-02 recovery BLOCKED |
| etcd | scoped READ, DEV prefix WRITE, secret rotation path | no etcd MCP/profile; probes to candidate ports closed; endpoint not resolved from current source/runtime | no config write; no secret value exposed | NOT_TESTED/BLOCKED; E-06/E-11/E-12 |
| Observability ARGUS | query traces/logs/metrics, health | `.60`: Prometheus `up` success 5 results; Jaeger services 5 and `echo-core` trace query 1; Loki labels success and query_range 200; Grafana health 200; OTLP 4317 reachable | no write/admin; no secrets | READ PASS on ARGUS; E-02/E-05/E-06…E-13 evidence |
| Observability DEV candidate | query traces/logs/metrics | `.45`: Loki 3100 open only; Prometheus 9090, Jaeger 16686, OTLP 4317 closed | no changes | PARTIAL; canonical DEV route unresolved |
| Gateway | health, logs, config, DEV/test restart, test HTTP | source/config identify `.211:8090`; curl `/health` failed; no container/profile found | `/close` and trading commands not invoked | BLOCKED; E-02/E-06…E-13 |
| Core / Bridge | health, logs, listeners, Kafka/PG reachability, safe restart | no live Echo core/bridge target/container/profile found; Docker compose only Flink/Hasura | no restart | NOT_TESTED/BLOCKED; E-07…E-13 |
| MT4/MT5 physical | terminal, logs, EA, pipes, demo account, start/stop, controlled operation | C:\MT4/C:\MT5 roots and EA/build files readable; no terminal/EA process; no matching named pipes; operator temp write works | no trading, no terminal start/stop, no account operation | filesystem READ PARTIAL; future physical gate MISSING/MANUAL; E-06…E-09 |
| GitHub Echo | branches, commits/diffs/files, feature push, master integration separation | `xKoRx/echo` default master; exact master `7e628bf5`; E05 `3bc5dca9`; branches and compare read; repo permission admin | no push/merge/update_ref/delete invoked | READ PASS; push/integration authority NOT_TESTED; least-privilege separation finding |

### Tecnología no provisionada sin source proof

Current Echo source/runtime proof no estableció MinIO, Temporal, MongoDB Forge, ni Echo Forge como dependencias de este lane. Se clasifican `LEGACY_OR_UNUSED` y no se solicitaron permisos. Shared artifacts sólo tienen soporte temporal DEV probado; cualquier storage adicional queda `UNKNOWN_NEEDS_SOURCE_PROOF`.

### Roadmap Matrix

| Task | Required surfaces / tested capability | Missing capability | Readiness |
|---|---|---|---|
| E-02 | PG17 disposable/062 READY; PG DEV data RW; observability ARGUS READ | Hasura DEV data+metadata, Kafka producer/consumer, Flink control/recovery, Gateway target | BLOCKED |
| E-03 | Existing closed state; no new gate claimed | No new certification evidence in this session | Existing closed; unchanged |
| E-04 | Integrated source; physical golden is separate | final Forge golden/join out of scope | PARTIAL; unchanged |
| E-05 | PG17 environment READY; Git/source READ PASS | Hasura T19, BWC active terminal/demo environment | PARTIAL |
| E-06 | PG, Hasura, etcd/config, Gateway, Bridge, Reference EA | Hasura metadata/data, etcd, Gateway/Bridge, Reference terminal/account | BLOCKED |
| E-07 | Kafka, Core/Flink, PG, Bridge/EA facts, observability | Kafka read/write, Core/Bridge, EA facts | BLOCKED |
| E-08 | Kafka command plane, Core/Flink, PG reservation, Execution Agent test env | Kafka write, Flink control, Core, Execution test env | BLOCKED |
| E-09 | Reference+Execution EA, Kafka, Core/Flink, PG, traces/logs, demo broker | terminal/demo account, Kafka write, Flink control, Core | BLOCKED |
| E-10 | PG analytics, Reference facts, Hasura read | Hasura authenticated read and Reference physical facts | PARTIAL |
| E-11 | PG control plane, config, Gateway/Core, later execution test | etcd/config, Gateway/Core | PARTIAL |
| E-12 | PG portfolio/control, config, Gateway/Core, execution authority later | etcd/config, Gateway/Core, safe execution test | PARTIAL |
| E-13 | Hasura READ, frontend env, observability, operational endpoints | authenticated Hasura read, Gateway/ops target; dashboard write is later-only | PARTIAL |

### Gaps

| GAP-ID | Severity | Exact missing permission/tool | Affected tasks | Minimal remedy |
|---|---|---|---|---|
| GAP-ECHO-001 | CRITICAL | Callable Hasura DEV data+metadata surface; current `ALL_TOOLS` has none and SSH host has no `hasura` CLI | E-02, E-05, E-06, E-10, E-13 | expose scoped DEV Hasura MCP/CLI workflow; keep admin secret MCP-internal and redacted |
| GAP-ECHO-002 | CRITICAL | Kafka DEV/test list/consume/produce client; only TCP reachability proved, no `kcat`/CLI/MCP | E-02, E-07, E-08, E-09 | expose safe producer/consumer for dedicated test topic; no Kafka admin or PROD write |
| GAP-ECHO-003 | CRITICAL | Flink/StateFun DEV cancel/stop/restart/resubmit authority; only REST READ via SSH | E-02, E-07, E-08, E-09, E-13 | expose scoped DEV control MCP/operator workflow with recovery observation |
| GAP-ECHO-004 | HIGH | Live DEV Gateway/Core/Bridge host/service profile and health/log path; `.211:8090` unreachable | E-02, E-06…E-13 | publish exact DEV/test target and operator health/log/restart path |
| GAP-ECHO-005 | HIGH | etcd endpoint plus scoped READ and DEV sandbox-prefix WRITE | E-06, E-11, E-12 | provide prefix-scoped tool/path; keep PROD secrets unreadable |
| GAP-ECHO-006 | HIGH | Running MT4/MT5 test terminal, Reference/Execution demo accounts, EA attach and named-pipe/controlled-operation path | E-06…E-09 | provide manual operator gate or safe test host; never use PROD account |
| GAP-ECHO-007 | MEDIUM | DEV observability canonical route `.45` incomplete; ARGUS `.60` is queryable | E-02, E-05…E-13 | choose/restore DEV query route; READ only is sufficient now |
| GAP-ECHO-008 | MEDIUM / SECURITY | GitHub connector exposes admin/write operations beyond this lane; push/integration not separately exercised | all integration work | separate read + feature-push from controlled master integration authority |
| GAP-ECHO-009 | MEDIUM / SECURITY | Docker DEV SSH profile is root-equivalent | DEV operations | retain only if host is isolated DEV and commands are audited; do not extend to PROD |

### Required explicit gates

| Gate | Result |
|---|---|
| E-02 PG17 062 physical gate | READY: disposable PG17.11 up/down/up applied and verified; no PROD migration |
| E-02 Hasura DEV roles/hook | BLOCKED: no callable DEV data/metadata surface; direct unauthenticated probes rejected |
| E-02 Kafka PublishSync/redelivery | BLOCKED: TCP only; no produce/consume/key/header/group probe |
| E-02 Flink restart/recovery | BLOCKED: REST read/checkpoints PASS; control authority not available/tested |
| E-02 Gateway physical | BLOCKED: `.211:8090` health unreachable; no live target/profile |
| E-02 observability | PASS for ARGUS READ; DEV candidate `.45` PARTIAL |
| E-02 result | `E02_PHYSICAL_CERTIFICATION_BLOCKED` |
| E-05 PG17 physical | PASS for disposable PG17 mechanism; E05 063 product migration not executed |
| E-05 Hasura T19 | BLOCKED: no callable metadata/data authority or CLI |
| E-05 source/Git | PASS: master/E05 commits, branches, diffs/files read; no write |
| E-05 BWC environment | BLOCKED/PARTIAL: MT5 filesystem/operator exists, but no running terminal/demo account/pipe |
| E-05 result | `E05_PHYSICAL_SURFACES_NOT_READY`; exact gaps GAP-ECHO-001 and GAP-ECHO-006 |

### Safety Boundaries

Not executed: real trading, position close, productive Flink cancel/stop/restart, productive Bridge/Gateway/Core restart, Kafka PROD write, PROD migration, Hasura PROD metadata/data mutation, etcd PROD write or secret rotation, firewall changes, Echo source/E-05/master changes, Echo Forge changes, deployment, and E-02 physical gates. Secret handling probe found no cleartext secret: Hasura admin-secret presence was inspected only as `<redacted-present>`; no credential entered Agents OS, logs, handoff, or this matrix.

### Evidence and reproducibility

Physical evidence was collected in session probes on 2026-09-14 using the tools listed above. Positive results include exact identities, privilege checks, HTTP status/GraphQL error behavior, PG rollback residual count zero, disposable PG17 migration lifecycle, Flink job/checkpoint responses, ARGUS query responses, GitHub object reads, and policy-denied negative probes. Large outputs and secrets were intentionally not persisted; the change log and session feedback identify the evidence class and limitations.

## Fuentes

- [[Echo — Live Platform V1]]; [[Echo — E-02 Control Safety, Auth and Journal Recovery]]; [[Echo — E-05 Analytics Convergence A0]]; `xKoRx/echo` current source/specs at master `7e628bf5fcadd92dc5398663d9b99a239a95ef7a` and feature refs `f7ddea18`, `3bc5dca9`; Agents OS MCP/tool inventory captured during this session.
