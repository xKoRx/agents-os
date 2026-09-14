---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P0
area: "[[Aranea]]"
parent:
sprint:
start: 2026-09-14
due:
progress: 0
repo:
jira:
prs:
slug: hermes-aranea-autonomous-operations
aliases:
  - Hermes Autonomous Operations
  - Aranea Autonomous Operations
  - Hermes Homelab Operations
  - Hermes Aranea
tags:
  - kind/project
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - agent/hermes
created: "2026-09-14"
updated: "2026-09-14"
---

# HERMES — ARANEA AUTONOMOUS OPERATIONS

> [!info]+ HERMES — ARANEA AUTONOMOUS OPERATIONS
> **Área:** [[Aranea]] · **Owner:** me · **Estado:** active · **Prioridad:** P0 · **Inicio:** 2026-09-14
>
> Programa para convertir a **Hermes** en el operador autónomo de Aranea sin mezclar su autoridad administrativa del homelab con el plano MCP consumido por agentes de desarrollo.

## 🎯 Objetivo

Construir de forma incremental una capacidad operativa en la que Hermes pueda:

1. **Administrar Aranea como infraestructura real**: storage, backups, TrueNAS, Proxmox, nodos, VMs, LXC, Docker, Linux, Windows, lifecycle de servicios, provisioning y recuperación.
2. **Administrar el Agent Access Plane**: descubrir, instalar, configurar, reparar, certificar y publicar capabilities MCP para Echo, Echo Forge y futuros agentes de desarrollo.
3. Mantener ambos dominios **operacionalmente independientes**, de modo que una falla del MCP Access Plane nunca deje a Hermes sin capacidad para reparar el propio access plane o el servicio subyacente.
4. Reducir progresivamente la intervención humana hasta que tareas DEV/test habituales puedan resolverse end-to-end por Hermes con evidencia durable en Agents-OS.

## 🧠 Contexto del problema

Hermes tendrá dos responsabilidades diferentes que comparten infraestructura pero **no deben compartir el mismo mecanismo de control**.

### Responsabilidad A — Administrador del homelab

El objetivo final es que Hermes pueda operar el clúster completo de Aranea:

- TrueNAS y storage;
- estrategia y ejecución de backups/restore;
- clúster Proxmox y sus nodos;
- lifecycle de VMs y LXC;
- Docker/Compose y contenedores;
- acceso a Linux y Windows;
- instalación/configuración de software dentro de VMs;
- despliegue y recuperación de servicios;
- networking y componentes de infraestructura cuando su nivel de autoridad lo permita;
- diagnóstico y reparación de fallas operativas.

La autoridad **no se entrega de una vez**. El rollout parte por inventario/read-only, luego storage/backups y avanza por etapas hasta administración integral.

### Responsabilidad B — Habilitación de servicios para agentes

Echo, Echo Forge y otros agentes necesitan superficies controladas para consultar u operar servicios como PostgreSQL, MongoDB, Hasura, Kafka, Flink, Temporal, MinIO, etcd, runtimes, observabilidad y futuros componentes.

El MCP Access Plane existente es la superficie correcta para los **consumidores de desarrollo**, pero no puede ser el único mecanismo de administración de Hermes. Si Hermes dependiera exclusivamente de un MCP para reparar el MCP, reiniciar su runtime o recuperar el servicio destino, se produciría una dependencia circular.

Los bloqueos actuales de Echo/Echo Forge se consideran **workload de aceptación** de este programa, no el diseño del programa.

## 🧭 Decisión arquitectónica principal

> **Ningún operador puede depender exclusivamente de la superficie que administra.**

Hermes tendrá un **management path independiente del MCP Access Plane**.

```text
                           HERMES
                    Orchestrator / Manager
                           │
          ┌────────────────┴─────────────────┐
          │                                  │
          ▼                                  ▼
 INFRASTRUCTURE OPERATIONS            AGENT ACCESS OPERATIONS
 native management plane              agent capability plane
          │                                  │
 SSH / APIs / WinRM /                   MCP Access Plane
 Proxmox / TrueNAS /                    profiles / grants /
 Docker / systemd /                     certification
 service admin APIs                           │
          │                                  ▼
          └──────────────► SERVICES ◄── Echo / Forge / agents
```

Si el MCP de Kafka, Hasura, Temporal o cualquier otro servicio deja de responder, Hermes debe seguir pudiendo acceder por el management plane autorizado para diagnosticar y reparar el servicio o el propio access plane.

## 🧩 Dos workstreams

| Workstream | Propósito | Boundary |
|---|---|---|
| [[HERMES — Infrastructure Operations]] | Dar a Hermes autoridad operativa progresiva sobre Aranea | Administra infraestructura y servicios mediante interfaces nativas; no usa el MCP como dependencia exclusiva de recovery |
| [[HERMES — Agent Access Operations]] | Hacer autónoma la habilitación de capabilities para agentes | Orquesta el MCP Access Plane existente; no reemplaza la administración física del servicio |

Los dos workstreams son coordinados por este proyecto, pero mantienen tareas, autoridad, credenciales, prompts y criterios de aceptación independientes.

## 🏛️ Modelo de agentes / autoridad

Hermes actúa como **orquestador**. La ejecución concreta debe poder separarse en operadores especializados con system prompt, credenciales, herramientas y scope propios.

Roles lógicos iniciales — no implican todavía un framework ni procesos separados obligatorios:

```text
Hermes
├── backup / storage operator
├── proxmox operator
├── linux / container operator
├── windows operator
├── service operator
└── access-plane operator
```

La implementación puede consolidar o separar estos roles según evidencia real. La separación de autoridad importa más que el número de agentes.

### Niveles conceptuales

- **Consumer:** Echo, Forge y futuros agentes. Consumen capabilities publicadas; no administran Aranea.
- **Operator:** subagentes/perfiles Hermes con acceso nativo scoped para una responsabilidad concreta.
- **Orchestrator:** Hermes decide qué operador usar, coordina, valida evidencia, escala bloqueos y actualiza Agents-OS.

## 🔐 Principios frozen para v1

1. **Management plane != MCP Access Plane.** Hermes debe conservar un path administrativo independiente.
2. **Privilegios progresivos.** No entregar autoridad total al inicio; cada etapa se certifica antes de ampliar la siguiente.
3. **Separación por responsabilidad.** Prompts, credentials y tools se asignan al operador que las necesita.
4. **Secrets por referencia.** Nunca persistir valores secretos en Agents-OS, prompts o handoffs.
5. **Target proof antes de mutar.** Toda mutación debe demostrar host/servicio/entorno real antes de ejecutarse.
6. **DEV/test primero.** La autonomía de mutación se certifica primero fuera de PROD.
7. **PROD no es autónomo por defecto.** Mutaciones PROD requieren un gate explícito hasta que el owner cambie esta política.
8. **Consumer-side verification.** Una capability agent-facing no está lista sólo porque el servidor responde; debe pasar desde el consumidor real.
9. **Reuse > repair > extend > wrap > build.** No construir MCPs o tooling nuevo si una superficie existente puede servir de forma segura.
10. **Agents-OS es el estado durable.** Los proyectos de agente deben permitir que un agente fresco continúe sin depender del chat anterior.
11. **Rollback/revoke obligatorio para cambios de autoridad.** Toda ampliación operativa debe poder revertirse o revocarse.
12. **KISS/YAGNI.** No crear dashboard, policy DSL, capability database ni provider framework genérico antes de demostrar repetición real.

## 🚦 Rollout de Infrastructure Operations

La madurez de infraestructura se versiona de forma independiente de la madurez del access plane.

| Nivel | Alcance | Gate de salida |
|---|---|---|
| **H0 — Observe** | inventario, topología, health, configuración no secreta, relaciones host/VM/LXC/service | Hermes puede reconstruir el estado real sin mutar y detectar drift básico |
| **H1 — Backup & Storage** | backups, restore evidence, storage health, TrueNAS/PBS/targets relacionados según diseño vigente | backups verificables + restore drill + operación sin intervención shell humana habitual |
| **H2 — Proxmox Lifecycle** | inspect/start/stop/reboot/create/clone/configurar VMs/LXC dentro de scopes definidos | lifecycle completo certificado con target proof y rollback |
| **H3 — Guest & Service Operations** | Linux, Windows, Docker, systemd, filesystem/config y restart de servicios | diagnóstico + reparación de un servicio DEV/test sin intervención humana |
| **H4 — Provisioning** | levantar nuevas VMs/LXC/containers y software requerido desde cero | provisioning reproducible + evidencia + registro durable |
| **H5 — High-impact Infrastructure** | networking, cluster/storage de alto impacto y operaciones con blast radius mayor | gates específicos, recovery probado y autoridad explícitamente habilitada |
| **H6 — Integrated Autonomy** | coordinación end-to-end entre capas y recovery de incidentes | runbooks/skills maduros + ejercicios de recovery + intervención humana excepcional |

El primer dominio práctico es **storage/backups**, reutilizando el conocimiento y decisiones canónicas de [[BACKUP-DR-OWNER-PROJECT]] en vez de duplicarlas.

## 🚦 Rollout de Agent Access Operations

| Nivel | Alcance | Gate de salida |
|---|---|---|
| **A0 — Inspect** | descubrir el MCP Access Plane real, targets, perfiles, tools, credenciales por referencia y consumidores | mapa operativo actual reconciliado con evidencia |
| **A1 — Repair** | diagnosticar y reparar capabilities MCP existentes | Hermes recupera una capability rota sin depender de esa misma capability |
| **A2 — Configure / Extend** | modificar scope, perfiles, permisos y configuración existente | cambio scoped + smoke server-side + consumer-side |
| **A3 — Deploy** | instalar y publicar un MCP/capability nuevo cuando no exista superficie reusable | deployment repetible, autenticado, scoped y certificado |
| **A4 — Grant / Revoke** | otorgar o retirar capabilities a consumidores concretos | grants trazables, secretos no expuestos, revoke probado |
| **A5 — Autonomous Enablement** | recibir necesidad funcional y resolver discovery→provision→certify→publish | nuevos blockers DEV/test se resuelven sin shell humano salvo autoridad realmente ausente |

## 🔄 Contrato operativo objetivo

Los consumidores deben pedir **qué capacidad necesitan**, no cómo implementarla.

Ejemplo conceptual:

```text
consumer: Echo verifier
service: Kafka
environment: DEV
need: bounded produce/consume with key + headers to certify redelivery
mutability: write scoped to sandbox resources
required evidence: server smoke + consumer smoke
```

Hermes decide:

```text
reuse existing capability
→ repair if broken
→ extend if insufficient
→ wrap native surface if needed
→ build new integration only as last option
```

Resultado esperado:

```text
REQUESTED
→ DISCOVERED
→ PLANNED
→ PROVISIONED
→ VERIFIED
→ PUBLISHED
→ CONSUMED
```

Estados excepcionales: `BLOCKED` y `REVOKED`.

## 🧪 Workload de aceptación inicial

Los bloqueos de Echo/Echo Forge no se copian como diseño permanente; se usan para probar familias de capabilities:

- **DATA:** PostgreSQL, MongoDB, Hasura y futuras superficies data-plane/control-plane.
- **EVENT:** Kafka y semántica de produce/consume/groups/redelivery.
- **CONTROL:** Temporal, Flink/StateFun, etcd y operaciones de lifecycle/control.
- **ARTIFACT:** MinIO y resolución/lectura/verificación de artifacts.
- **RUNTIME:** Gateway/Core/Bridge, Docker, MT4/MT5 y otros runtimes operativos.
- **OBSERVABILITY:** ARGUS/Jaeger/telemetría agent-facing cuando corresponda.

La fuente canónica del MCP plane actual sigue siendo [[AGENT-PLATFORM - MCP Access Plane]]. Este proyecto gobierna la **autonomía de Hermes sobre ese plano**, no duplica endpoints, credenciales ni estado detallado de cada MCP.

## ✅ Definition of Done del programa

El programa alcanza su objetivo cuando, dentro del nivel de autoridad aprobado, el owner puede expresar una necesidad como:

> “Echo está bloqueado porque necesita X en el servicio Y de DEV para validar Z.”

Y Hermes puede, sin intervención shell humana rutinaria:

```text
descubrir el target real
→ escoger el operador correcto
→ provisionar/reparar/configurar
→ verificar server-side
→ verificar desde el consumer real
→ publicar/registrar la capability
→ devolver evidencia
→ actualizar Agents-OS
```

Para Infrastructure Operations, el equivalente es que Hermes pueda recibir un objetivo operativo —por ejemplo proteger un nuevo servicio, crear una VM DEV o recuperar un daemon— y completar la operación dentro de su autoridad vigente con target proof, rollback y evidencia.

## 📊 Estado actual

- **Proyecto creado:** 2026-09-14.
- **Diseño macro:** frozen para iniciar ejecución: dos workstreams independientes, management plane nativo y MCP Access Plane separado.
- **Infrastructure Operations:** autoridad incremental aún por bootstrap; H0/H1 son el inicio previsto.
- **Agent Access Operations:** existe un MCP Access Plane funcional y en evolución bajo [[AGENT-PLATFORM - MCP Access Plane]], pero Hermes todavía no dispone del ciclo autónomo completo A0→A5.
- **Dependencias ya existentes:** [[BACKUP-DR-OWNER-PROJECT]] para Backup/DR y [[AGENT-PLATFORM - MCP Access Plane]] para la implementación MCP actual.
- **Prioridad inmediata del programa:** habilitar autonomía de Agent Access Operations para desbloquear desarrollo sin comprometer el diseño de administración integral de Aranea.

## 🧱 Entrega de desarrollo

_No aplica directamente al proyecto padre — es un programa de coordinación. Todo cambio de código, configuración ejecutable, schema o infraestructura se gatea y documenta en el subproyecto que lo ejecuta antes de implementar._

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Cockpit humano
> El detalle vive en los dos proyectos `owner: agent`. Este proyecto conserva sólo una tarea puente por workstream.

- [ ] [[HERMES — Infrastructure Operations]] arrancar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[HERMES — Agent Access Operations]] arrancar + seguimiento #owner/me #type/supervision #area/aranea

## 📆 Bitácora

- **2026-09-14** — Proyecto creado. Se separan formalmente las responsabilidades de administración integral del homelab y habilitación MCP para agentes. Se congela el principio de management path independiente y el rollout dual H0→H6 / A0→A5.

## 🧭 Decisiones

- **D-01 — Dos workstreams independientes.** Infrastructure Operations y Agent Access Operations tienen autoridad, herramientas, credenciales y criterios de madurez distintos.
- **D-02 — Hermes orquesta; operadores ejecutan.** Se prefieren perfiles/subagentes especializados sobre un agente único con todas las herramientas siempre disponibles.
- **D-03 — MCP es consumer plane, no recovery plane.** El MCP Access Plane sirve a agentes de desarrollo; Hermes conserva interfaces administrativas nativas para operar/recuperar servicios.
- **D-04 — Rollout gradual.** Storage/backups abre el carril de infraestructura; agent enablement puede avanzar en paralelo a mayor velocidad.
- **D-05 — Existing systems remain canonical.** Backup/DR y MCP Access Plane existentes se reutilizan; este proyecto no duplica su source of truth.

## 🔗 Docs / Links

- [[Aranea]] — área del homelab.
- [[BACKUP-DR-OWNER-PROJECT]] — diseño/proyecto canónico de Backup/DR usado por el rollout H1.
- [[AGENT-PLATFORM-OWNER-PROJECT]] — iniciativa donde vive el MCP Access Plane existente.
- [[AGENT-PLATFORM - MCP Access Plane]] — source of truth operativo del capability plane MCP.
- [[aranea-mcps-expert]] — skill agent-facing canónica del MCP plane, según el proyecto existente.

## 💡 Ideas

### Backlog de ideas

- Extraer skills/provider archetypes sólo cuando varios servicios demuestren el mismo patrón repetible.
- Evaluar break-glass formal, policy engine o JIT credentials únicamente cuando la autonomía real haga insuficientes los gates simples de v1.

### Motivos / principios

- La prioridad es **autonomía útil y recuperable**, no maximizar privilegios ni construir una plataforma genérica antes de tiempo.
- Una capability sólo agrega valor cuando el consumidor real puede usarla y Hermes puede recuperarla si falla.

### Memoria pública / interna

- **Memoria pública:** este proyecto y sus dos workstreams son la fuente durable de estado, decisiones, etapas y blockers del programa.
- **Memoria interna:** conocimiento efímero del agente sólo se conserva si cambia el plan, una decisión o un procedimiento reusable.
- **Motivo:** permitir continuidad entre sesiones y agentes sin depender del chat ni duplicar facts de Backup/DR o MCP Access Plane.