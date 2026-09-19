---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-17"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[Daedalus — Development Agents MCP Access & Gaps]]"
  - "[[aranea-mcps-expert]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-hasura-mcp]]"
  - "[[aranea-kafka-mcp]]"
  - "[[aranea-flink-mcp]]"
  - "[[aranea-observability-mcp]]"
  - "[[aranea-temporal-mcp]]"
  - "[[aranea-minio-mcp]]"
  - "[[aranea-etcd-mcp]]"
aliases:
  - runbook capability plane MCP Aranea
  - aranea mcp plane
  - troubleshooting MCP Aranea
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - action/mcp-plane
---

# aranea-mcp-capability-plane

## Propósito

Diagnosticar discovery, configuración del cliente, env, auth, proxy, transporte, sesiones o policy antes de culpar al backend de datos/servicio. Router agent-facing: [[aranea-mcps-expert]]. Arquitectura y puertos: [[AGENT-PLATFORM - MCP Access Plane - Architecture]]. Procedimientos de cada familia: sus runbooks. Matriz por consumidor Daedalus y gaps Echo/Forge de acceso exclusivamente: [[Daedalus — Development Agents MCP Access & Gaps]]. No usar esta nota como SPEC de producto.

## Estado normal (registrado al 2026-09-17)

**13 capabilities**; listado de registros certificados por familia, no sustituto de `tools/list` efectivo en el cliente:

```text
3000  aranea-ssh
3001  aranea-postgres-ro
3002  aranea-postgres-rw
3003  aranea-mongo-forge-ro
3004  aranea-mongo-forge-rw
3005  aranea-hasura-prod-ro
3006  aranea-hasura-dev-admin
3007  aranea-kafka-dev-admin
3008  aranea-flink-dev-admin
3009  aranea-observability-ro
3010  aranea-temporal-ro
3011  aranea-minio-rw   (ex aranea-minio-ro; RW full desde 2026-09-18, identidad = key owner)
3012  aranea-etcd-ro
```

La fotografía histórica con sólo 10/11 capabilities precede la incorporación de Temporal/MinIO/etcd. MinIO y etcd están ACTIVE y certificados server + Cursor desde 2026-09-17; **MinIO es RW full con rename a `aranea-minio-rw` desde 2026-09-18** (identidad = key owner; detalle en [[aranea-minio-mcp]]) y etcd mantiene sus limitaciones de prefix en [[aranea-etcd-mcp]]. **Cursor PASS no implica ZCode/Codex PASS**: el patcher del trío kor corrió el 2026-09-17 (shape) y el runtime funcional se certificó por chain el 2026-09-18; el rename minio en ZCode/Codex queda pendiente del patcher kor stageado (`/tmp/minio-rw-rename-zcode-codex.py`, 2026-09-18). No deducir éxito de que existan las entries ni requerir owner cuando un operador ya autorizado pueda aplicar una corrección dentro de ACL/contrato.

## Consumer onboarding managed (B2 2026-09-14, B4 2026-09-15)

Hermes puede onboardear/remover capabilities en el consumer real Daedalus/Cursor sin edición manual del owner bajo un permiso scoped:

```text
Authority:   hermes-ops@daedalus (key-only, password locked, SIN sudo)
             ACLs scoped sobre /home/kor/.cursor/mcp.json (rw),
             /home/kor/.cursor + /home/kor/.config/mcp (-wx, backups),
             /home/kor/.config/aranea/secrets/hermes-managed/ (rwx)
Operator:    /home/kor/.config/aranea/secrets/hermes-managed/bin/
             mcp-onboard.py {add|remove|status}
             consumer-smoke.py (bearer por stdin, nunca argv/env persistido)
Config real: /home/kor/.cursor/mcp.json (refs ${env:VAR}; nunca bearer literal)
Env chain:   plasma-workspace/env/aranea-mcp.sh -> .config/mcp/aranea-env.sh
             -> archivos de secreto 0600 de kor (NO accesibles para hermes-ops)
Onboarding:  clon de entry existente, ref ${env:} idéntica; sin duplicar bearer
Smoke:       initialize (clientInfo requiere version) / tools/list / tools/call inocuo
             usando mcp.json + env chain real del consumer
Rollback:    remove + hash byte-identical vs backup anterior
Quirk:       scripts con ${...}/regex por heredoc-through-ssh se corrompen;
             distribuir por scp/base64-file
```

Revoke de esta autoridad: `userdel -r hermes-ops` + `setfacl -x` sólo sobre las entradas u:hermes-ops autorizadas en `/home/kor`, `.config`, `.cursor`, `.config/mcp`, `.config/aranea`, `.config/aranea/secrets`, `mcp.json`, `aranea-env.sh` (detalle en change_log `2026-09-14-b2-real-consumer-onboarding-closed`).

Provisioning B4: un env nuevo se persiste en `~kor/.config/aranea/secrets/hermes-managed/<cap>.bearer` (640, ACL `u:kor:r--`); `aranea-env.sh` se edita con bloque idempotente `if [ -r ... ]; then export VAR="$(cat ...)"; fi` con backup sha y `bash -n`/auto-restore. Certificar sourceando el chain con `HOME=/home/kor` y comprobando la entry real. HOME incorrecto produce falsos NOT_SET. Esto se demostró con observabilidad. Secret files originales de kor fuera del alcance hermes-ops permanecen así; no ampliar ACL para Codex/ZCode por comodidad.

El proxy Nginx histórico admite un solo bearer por su `map`; B3.3 demostró generar bearer nuevo server-side sobre proxy existente sin recrear el container, salvo cambio estructural del map. Bearer nunca en docs/logs/argv. ZCode mantiene literal en config 600 por decisión documentada 2026-09-16 (`${env:}` en headers no validado); Codex usa `bearer_token_env_var` tras normalización 2026-09-16. NO copiar tokens entre clientes o notas; ejecutar nueva certificación del trío 3010–3012 antes de declararlos completamente onboarded.

## Procedimiento de diagnóstico

1. Inventariar `tools/list` real del cliente concreto (`Cursor`, `ZCode`, `Codex`); distingir config presente, env heredada, handshake, tools expuestas y llamada inocua. Un `Up` o HTTP sin payload no prueba MCP.
2. Verificar URL, variable y autorización **sin revelar secreto** (`SET/NOT_SET`). Una shell con variable SET no implica que Cursor ya abierto la haya heredado.
3. Ante missing capability: discovery/config/environment antes de culpar al backend. Ante 401: bearer cliente/proxy; no rotar credenciales upstream por intuición. Ante 400/406: GET `/mcp` manual puede no ser request Streamable HTTP válido; comprobar initialize y headers MCP reales.
4. Ante `POLICY_DENIED` o Access Denied, cargar router/runbook de familia y respetar boundary. No ir al servicio directo, ampliar ACL ni cambiar de ambiente. Para timeout reducir scope/limit/query antes de ampliar policy.
5. Ante change de capability: cargar Architecture; comparar imagen/mounts/red/puerto y tool surface real, preparar backup/revert, añadir sólo el backend/proxy autorizado, test positivo+negativo 401/no-write y E2E en cliente real. Sin cert no cambiar estado de skills.
6. Hasura PROD authority: server tools/list EXACTAMENTE 3 (`get_inconsistent_metadata`, `get_schema`, `get_version`); sin `export_metadata`/`run_sql`/`reload_metadata` (H1). `mcp_auth` del cliente Cursor no cuenta si ausente en tools/list server-side. DEV 9 tools. `get_schema` históricamente grande (~11MB) podía matar hijo stdio; evitar queries masivas sin límite.
7. GAP-ECHO-010 Hasura: `initialize` 200+sid pero tools `-32603 Not connected` era hijo compartido muerto mcp-proxy 6.7.16, fix `-g010fix` respawnea con sesión nueva; ssh-mcp (pool 64, init-per-call) y flink-mcp (SDK Java) NO comparten esta causa. `-32001` sid inexistente; `-32000` sid ausente; `202` sin sid en notificaciones no es respuesta positiva a initialize.
8. Kafka DEV: 19 tools, `alter_configs` incremental Aranea para no revertir propiedades no objetivo; detener mutaciones ante drift. Kafka PROD no certificado.
9. Flink DEV: 22 tools y NO SQL. REST/control por `aranea-flink-dev-admin`; filesystem/Docker/lifecycle sólo por `aranea-ssh` + `docker-echo-dev-operator`. Declarativo Portainer stack 1; no `docker compose up -d` indiscriminado.
10. Temporal 3010: 28 tools RO `hardReadOnly`, allowlist namespaces; iniciar/cancelar no está cubierto. MinIO 3011: 9 tools listadas, put/copy/delete denegados e IAM sólo prefixes del runbook. etcd 3012: 4 tools RO, prefijos/secret keys filtrados; acceso directo al cluster sin auth/TLS NO es workaround.
11. Windows privileged evidence: `AraneaEvidencePublish` SYSTEM -> JSON -> `mt5-kronos-operator` `echo-dev` read-only. El viewer `sftp-download` está `POLICY_DENIED` en Windows; no inferirlo desde viewer Linux histórico. Filtros y frescura en [[aranea-ssh-mcp]].
12. Distinguir reparación `mcps` de consumer onboarding: para operaciones appliance usar management path `mcps-ops` vía [[aranea-mcp-plane-operator]], nunca usar un MCP del mismo appliance para reiniciarlo. Un smoke por stdin no equivale a demostrar env-chain persistente; exigir ambas pruebas cuando corresponde.

## Casos históricos relevantes, sin tratarlos como estado actual

- 2026-09-11 Mongo Forge ausente del cliente por bearers env `NOT_SET`; backend no era culpable.
- 2026-09-12 Hasura DEV PASS: :3006 401 sin bearer, init 200+sid, tools/list 9, Cursor `get_version`/consistency PASS; admin secret server-side.
- 2026-09-12 Hasura PROD certificación inicial 4 tools incl. `export_metadata`: **SUPERSEDED 2026-09-15** H1 elimina export, 3 vigentes; cualquier rebuild que lo reintroduzca queda fuera de contrato.
- 2026-09-13 Kafka DEV :3007 401, 19 tools, 6 brokers, golden admin smoke create/alter incremental/increase/produce/consume/group/delete PASS con recursos temporales. `ARANEA_KAFKA_MCP_DEV_ADMIN_BEARER` se carga vía chain KDE; clientes abiertos necesitan reheredar env.
- 2026-09-13 Flink DEV :3008 401 wrong bearer, init, 22 tools, no SQL, `get_cluster_info`/`list_jobs` PASS, host operator root DEV; su Java MCP puede usar SSE `data:` en tools/call. Portainer stack 1 es autoridad del runtime.
- 2026-09-15 observabilidad 22 tools viewer RO, Prometheus/Loki queries reales; Jaeger datasource visible pero sin toolset Jaeger.
- 2026-09-16 GAP-ECHO-010 Hasura `-g010fix` validado 50/50 DEV + 30/30 PROD server+Daedalus. El diagnóstico anterior que atribuía lo mismo a SSH/Flink está SUPERSEDED.
- 2026-09-17 Windows evidence publisher ACTIVE/CERTIFIED por consumer; dos fallos anteriores del self-verifier del instalador eran metadata, no fallo de la publicación. MinIO/etcd certificados, Cursor 3/3 sobre el trío nuevo; ZCode/Codex aún requieren su propio smoke posterior.

## Validación / rollback

```text
Plane symptom:      missing|401|POLICY_DENIED|timeout|invalid request
Config present:     yes|no
Required env:       SET|NOT_SET (value never shown)
Capability exposed: yes|no (tools/list del cliente específico)
Client vs backend:  distinguished
Tool surface:       expected exact set|unexpected
Architecture drift: none|material
Mutation:           none | scope + rollback + postcondition
Bypass:             none
Secrets in docs:    none
```

No publicar backend, abrir puertos, pedir secretos o modificar ACL para resolver discovery. Config/env que empeore el cliente ⇒ restore de backup y reinicio/re-smoke sólo del cliente. Hasura PROD expone mutadores/export ⇒ restore strict-RO; Kafka pierde patch incremental ⇒ restore imagen `local/kafka-mcp:2.0.0-0b3bf47-inc1-fm3.0.1`; Flink pierde pin/patch o añade SQL ⇒ restore `local/flink-mcp:0.3.1-981bbef-aranea2-flink1.14`. Nuevas familias: seguir runbook específico y rollback propio; no inventar rollback genérico.

## Evidencia

Registrar capability, fecha, consumer exacto, discovery/env por nombre sin valor, handshake/tool surface, auth/policy, target, acciones y rollback, y efecto material. Server cert, Cursor cert y ZCode/Codex cert son dimensiones distintas.