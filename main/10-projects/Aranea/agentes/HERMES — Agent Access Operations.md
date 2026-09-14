---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P0
area: "[[Aranea]]"
parent: "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
sprint:
start: 2026-09-14
due:
progress: 0
repo:
jira:
prs:
slug: hermes-agent-access-operations
aliases:
  - Hermes Agent Access Operations
  - Hermes MCP Operations
  - Hermes Capability Operations
  - Hermes Access Plane Operations
tags:
  - kind/project
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - agent/hermes
  - tech/mcp
  - domain/agent-access
created: "2026-09-14"
updated: "2026-09-14"
---

# HERMES — Agent Access Operations

> [!info]+ Agent Access Operations
> **Padre:** [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] · **Owner:** agent · **Estado:** active · **Prioridad:** P0

## 🎯 Objetivo

Convertir a Hermes en el operador autónomo del **Agent Access Plane** de Aranea: recibir necesidades funcionales de Echo, Echo Forge y futuros agentes, descubrir la superficie real del servicio, reutilizar/reparar/extender/desplegar la capability necesaria, certificarla desde el consumidor real y registrar el resultado sin depender de intervención shell humana rutinaria.

Este workstream **no reemplaza** [[AGENT-PLATFORM - MCP Access Plane]]. Ese proyecto sigue siendo el source of truth del plano MCP existente. Aquí se gobierna la autonomía de Hermes para operarlo y hacerlo crecer.

## 🧠 Contexto

Echo y Echo Forge ya han demostrado un patrón repetido: el desarrollo queda bloqueado no necesariamente por código, sino porque los agentes carecen de una capability operativa concreta sobre un servicio real.

Ejemplos recientes de necesidades:

- Hasura DEV data-plane/control-plane;
- Kafka DEV produce/consume/admin scoped;
- Flink/StateFun control plane;
- etcd scoped access;
- PostgreSQL DEV migration/DDL surface;
- Temporal DEV workflow/history/task-queue visibility;
- MinIO artifact resolution/read/hash;
- runtime operations para Gateway/Core/Bridge/MT4/MT5;
- observabilidad read-only.

Atacar cada ítem manualmente no escala. La meta es que Hermes pueda resolver el patrón de forma reusable.

## 🏛️ Boundary

### Este workstream SÍ gobierna

- recibir capability requests desde agentes/proyectos;
- discovery del servicio y entorno real;
- decidir si reutilizar/reparar/extender/wrap/deploy;
- administrar configuración del MCP Access Plane necesaria para esa capability;
- crear/ajustar perfiles, scopes y grants dentro de DEV/test autorizado;
- usar credenciales por referencia sin exponer valores;
- smoke server-side;
- smoke desde consumidor real;
- publish/register/revoke de capabilities;
- actualizar Agents-OS y cerrar blockers con evidencia.

### Este workstream NO gobierna

- administrar físicamente Proxmox/TrueNAS/hosts como responsabilidad principal: eso vive en [[HERMES — Infrastructure Operations]];
- duplicar endpoints, permisos o estado detallado ya canónico en [[AGENT-PLATFORM - MCP Access Plane]];
- entregar acceso root-equivalent a agentes consumidores;
- habilitar mutaciones PROD automáticamente.

## 🔁 Regla de dependencia

El Access Plane Operator puede necesitar que un servicio, VM, Docker runtime o MCP backend sea reparado. Esa reparación debe poder escalar a [[HERMES — Infrastructure Operations]] o a un service operator con management path nativo.

```text
consumer necesita capability
        │
        ▼
Agent Access Operations
        │
        ├── capability sana → publicar/certificar
        │
        ├── capability insuficiente → extender/configurar
        │
        └── runtime/servicio roto
                   │
                   ▼
       Infrastructure / Service Operator
                   │
                   ▼
       reparar por management plane nativo
                   │
                   ▼
       Agent Access Operations recertifica
```

Hermes nunca debe quedar atrapado intentando arreglar un MCP usando exclusivamente ese mismo MCP.

## 📥 Capability Request — contrato conceptual v1

El consumidor expresa **qué necesita**, no cómo implementarlo.

Campos mínimos:

- `consumer` — agente/proyecto que lo requiere;
- `service` — servicio lógico;
- `environment` — DEV/test/PROD;
- `surface` — data / event / control / artifact / runtime / observability;
- `actions` — operaciones funcionales requeridas;
- `scope` — recursos/datos/namespace/DB/topic/etc. permitidos;
- `mutability` — observe / write / operate;
- `reason` — qué validación o flujo desbloquea;
- `evidence_required` — evidencia necesaria para considerar la capability lista.

Ejemplo:

```text
consumer: Echo verifier
service: Kafka
environment: DEV
surface: event
actions: produce + bounded consume + inspect groups/offsets
scope: sandbox resources used by the verifier
mutability: write
reason: certify redelivery semantics
evidence_required: server smoke + consumer smoke
```

## 📤 Capability Grant — resultado conceptual v1

El resultado durable debe poder indicar, sin secretos:

- capability/profile id;
- target lógico y environment;
- transport/surface;
- acciones permitidas;
- scope permitido;
- mutability;
- credential reference;
- evidence de certificación;
- consumer certificado;
- rollback/revoke path;
- status.

No se exige todavía una base de datos o schema ejecutable propio. Agents-OS y la configuración existente son suficientes para v1.

## 🔄 Ciclo autónomo objetivo

```text
REQUESTED
→ DISCOVERED
→ PLANNED
→ PROVISIONED
→ VERIFIED_SERVER
→ VERIFIED_CONSUMER
→ PUBLISHED
→ CONSUMED
```

Estados excepcionales:

- `BLOCKED` — falta authority real o dependencia externa precisa;
- `REVOKED` — capability retirada;
- `DEFERRED` — fuera del scope actual, por ejemplo PROD no autorizado.

## 🧠 Decision tree de provisión

Siempre en este orden:

1. **Reuse** — ya existe capability suficiente y sana.
2. **Repair** — existe pero está rota.
3. **Extend/Configure** — existe pero falta scope/action concreta.
4. **Wrap native surface** — no hay MCP adecuado, pero existe API/CLI segura reutilizable.
5. **Deploy existing MCP/integration** — adoptar upstream existente, pinneado y scoped.
6. **Build/fork** — sólo si un gap material demostrado no puede resolverse de otro modo.

La estrategia evita que cada blocker termine creando otro servicio custom.

## 🚦 Roadmap A0 → A5

### A0 — Inspect

**Objetivo:** Hermes entiende el Access Plane actual y puede localizar el source of truth.

- reconciliar [[AGENT-PLATFORM - MCP Access Plane]];
- enumerar capabilities vigentes y consumers reales;
- identificar runtime/host/config source of truth del MCP plane;
- identificar management paths de recovery independientes;
- clasificar authority faltante de Hermes.

**Gate:** Hermes puede explicar y localizar una capability existente sin pedir al owner información ya documentada.

### A1 — Repair

**Objetivo:** Hermes recupera capabilities existentes rotas.

- health/initialize/tools/list;
- logs/runtime/config;
- restart/repair por management plane;
- recertificación server + consumer;
- incident evidence y causa cuando sea posible.

**Gate:** una capability rota se recupera end-to-end sin intervención shell humana rutinaria.

### A2 — Configure / Extend

**Objetivo:** modificar capabilities existentes sin rediseñar el plano.

- scopes;
- profiles;
- tool allow/deny;
- target/environment config;
- bearer/credential refs;
- consumer registration.

**Gate:** cambio scoped certificado y revocable.

### A3 — Deploy

**Objetivo:** Hermes instala una capability nueva cuando no existe superficie reusable.

- discovery upstream/native APIs;
- selection con KISS/YAGNI;
- pin de versión/source;
- backend privado cuando aplique;
- auth boundary;
- stable endpoint/profile;
- server smoke;
- consumer smoke;
- runbook/update source of truth.

**Gate:** nuevo MCP/capability DEV/test deployado reproduciblemente sin intervención humana manual habitual.

### A4 — Grant / Revoke

**Objetivo:** administrar consumo por agente/surface.

- crear grant scoped;
- secret refs;
- publish config al consumidor;
- verify from consumer;
- revoke/rollback probado.

**Gate:** Hermes puede otorgar y retirar una capability sin exponer secretos ni ampliar permisos accidentalmente.

### A5 — Autonomous Enablement

**Objetivo:** cerrar la cadena completa desde blocker funcional.

```text
need
→ discovery
→ strategy
→ provision/repair
→ certify
→ publish
→ consumer PASS
→ Agents-OS update
```

**Gate:** nuevos blockers DEV/test de Echo/Forge se resuelven sin shell humana salvo falta real de authority o decisión de producto/seguridad.

## 🧪 Familias de aceptación

Los blockers actuales sirven como aceptación por familia, no como arquitectura fija.

### DATA

Ejemplos: PostgreSQL, MongoDB, Hasura.

Debe probar:

- read/write scoped;
- metadata/control plane cuando corresponda;
- roles/permissions;
- DDL/migration authority sólo cuando sea necesaria;
- no superuser/global admin por defecto.

### EVENT

Ejemplo: Kafka.

Debe probar:

- list/introspection;
- bounded consume;
- produce sandbox;
- key/headers;
- groups/offsets/redelivery;
- admin sólo en el scope demostrado necesario.

### CONTROL

Ejemplos: Temporal, Flink/StateFun, etcd.

Debe probar:

- inspect status/history/config;
- scoped lifecycle operations;
- retry/recovery observability;
- mutación separada de observación cuando convenga.

### ARTIFACT

Ejemplo: MinIO.

Debe probar:

- resolve exact artifact;
- existence/size/metadata/hash;
- read/download surface scoped;
- write sólo si aparece un caso real.

### RUNTIME

Ejemplos: Gateway/Core/Bridge, Docker, MT4/MT5.

Debe probar:

- status/logs/listeners/config/dependencies;
- restart sólo en DEV/test autorizado;
- viewer != operator;
- execution boundary explícito.

### OBSERVABILITY

Ejemplos: ARGUS/Jaeger.

Debe probar query/inspection read-only primero, manteniendo cambios operativos fuera del consumer plane.

## 🧪 Acceptance workload inicial conocido

### Echo

El programa debe ser capaz de resolver o demostrar ya resueltas necesidades del tipo:

- Hasura DEV data-plane + metadata/control plane;
- Kafka DEV produce/consume scoped;
- Flink/StateFun control operations;
- etcd scoped access;
- Gateway/Core/Bridge operations;
- PostgreSQL DEV migration/DDL authority;
- MT4/MT5 test/demo cuando el roadmap lo requiera.

### Echo Forge

El programa debe cubrir necesidades del tipo:

- PostgreSQL DEV `sqx` SELECT / RW sólo si se demuestra;
- Temporal DEV workflow/history/task-queue/poller inspection;
- MinIO artifacts RO con hash/metadata/read;
- separación real viewer/operator en `mt5-kronos`.

El estado exacto de cada capability se verifica contra el source of truth vigente antes de trabajar; esta lista es acceptance context, no inventario operativo canónico.

## 📊 Estado actual

- Workstream creado 2026-09-14.
- [[AGENT-PLATFORM - MCP Access Plane]] ya posee múltiples capabilities certificadas y una arquitectura real que debe reutilizarse.
- Kafka DEV, Flink DEV, Hasura, PostgreSQL y Mongo ya tienen trabajo previo importante; no deben reinstalarse por reflejo.
- El gap principal es pasar de **operación manual/orquestada por el owner** a **operación autónoma por Hermes**.
- **Nivel inicial declarado:** A0 pendiente de certificación específica desde Hermes; partes de A1-A3 existen operacionalmente pero no se consideran autonomía Hermes hasta probarse desde su runtime/authority.
- Este workstream es P0 porque Echo/Echo Forge están encontrando blockers de capability que frenan desarrollo.

## 🧱 Entrega de desarrollo

_No existe un único repo. La mayoría de cambios serán configuración/infraestructura del MCP Access Plane. Antes de modificar source/versioned config o crear/forkear una integración, registrar repo/branch/base y SPECs en la tarea correspondiente. No implementar código custom sin gap demostrado._

## ✅ Tareas

### A0 — Reconciliar y bootstrap

- [ ] A0.1 Cargar [[AGENT-PLATFORM - MCP Access Plane]] y reconciliar estado real desde Hermes #owner/agent #type/admin #area/aranea
- [ ] A0.2 Identificar management path real de `mcps` y demostrar que no depende de sus MCP #owner/agent #type/admin #area/aranea
- [ ] A0.3 Clasificar authority Hermes para inspect/repair/configure/deploy/grant #owner/agent #type/admin #area/aranea
- [ ] A0.4 Congelar Capability Request/Grant v1 en forma mínima, sin crear plataforma adicional #owner/agent #type/admin #area/aranea

### A1 — Repair loop

- [ ] A1.1 Seleccionar una capability existente con recovery verificable como primer golden repair #owner/agent #type/admin #area/aranea
- [ ] A1.2 Ejecutar diagnóstico/recovery usando management plane independiente #owner/agent #type/admin #area/aranea
- [ ] A1.3 Recertificar server-side y desde consumer real #owner/agent #type/admin #area/aranea
- [ ] A1.4 Convertir sólo el patrón reusable demostrado en runbook/skill #owner/agent #type/admin #area/aranea

### A2 — Configure / Extend

- [ ] A2.1 Tomar un blocker real de Echo/Forge que requiera ampliar una capability existente #owner/agent #type/admin #area/aranea
- [ ] A2.2 Aplicar minimum-scope change + rollback #owner/agent #type/admin #area/aranea
- [ ] A2.3 Certificar consumer-side y cerrar blocker con evidencia #owner/agent #type/admin #area/aranea

### A3 — Deploy

- [ ] A3.1 Tomar un blocker real sin capability reusable #owner/agent #type/admin #area/aranea
- [ ] A3.2 Ejecutar decision tree reuse→repair→extend→wrap→deploy antes de construir #owner/agent #type/research #area/aranea
- [ ] A3.3 Desplegar/adoptar integración mínima y pinneada #owner/agent #type/admin #area/aranea
- [ ] A3.4 Publicar y certificar desde consumer #owner/agent #type/admin #area/aranea

### A4 — Grant / Revoke

- [ ] A4.1 Definir grant durable mínimo por consumer sin persistir secret values #owner/agent #type/admin #area/aranea
- [ ] A4.2 Certificar alta/baja de una capability real #owner/agent #type/admin #area/aranea

### A5 — Autonomous Enablement

- [ ] A5.1 Resolver un capability request nuevo de Echo end-to-end sin shell humana #owner/agent #type/admin #area/aranea
- [ ] A5.2 Resolver un capability request nuevo de Echo Forge end-to-end sin shell humana #owner/agent #type/admin #area/aranea
- [ ] A5.3 Medir intervención humana residual y convertir sólo gaps repetidos en mejoras del sistema #owner/agent #type/admin #area/aranea
- [ ] A5.4 Declarar A5 PASS cuando nuevos requests DEV/test sean rutina para Hermes #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-14** — Workstream creado. Los blockers de Echo/Forge pasan a ser acceptance workload. Se preserva [[AGENT-PLATFORM - MCP Access Plane]] como source of truth del plano MCP y se fija la meta A0→A5 de autonomía Hermes.

## 🧭 Decisiones

- **A-D01:** consumers piden capacidades funcionales, no mecanismos ni SSH.
- **A-D02:** capability no está READY hasta consumer-side PASS.
- **A-D03:** reuse > repair > extend > wrap > deploy > build/fork.
- **A-D04:** Hermes usa management plane independiente para reparar runtime/servicios del access plane.
- **A-D05:** PROD mutation no es autónoma en v1.
- **A-D06:** Agents-OS + configs actuales son registry suficiente para v1; no capability DB/dashboard/policy engine todavía.

## 🔗 Docs / Links

- [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] — programa padre.
- [[HERMES — Infrastructure Operations]] — management/recovery plane complementario.
- [[AGENT-PLATFORM-OWNER-PROJECT]] — iniciativa del Agent Platform.
- [[AGENT-PLATFORM - MCP Access Plane]] — source of truth operativo MCP.
- [[AGENT-PLATFORM - MCP Access Plane - Architecture]] — arquitectura existente.
- [[aranea-mcps-expert]] — skill canónica agent-facing referenciada por el proyecto MCP.

## 💡 Ideas

### Backlog de ideas

- Extraer provider archetypes tras varias capabilities nuevas/repair loops reales.
- Incorporar métricas simples: requests autónomos cerrados, intervenciones humanas, consumer-smoke pass rate.

### Motivos / principios

- El objetivo no es producir más MCPs; es hacer que el acceso necesario aparezca de forma segura cuando el desarrollo lo necesita.
- La capa de autonomía debe sobrevivir a la caída de la capa que administra.