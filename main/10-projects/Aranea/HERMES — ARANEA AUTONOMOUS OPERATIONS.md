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
updated: "2026-09-18"
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

[[HERMES — Bootstrap & Self-Sufficiency]] es un proyecto **transitorio**, no un tercer workstream. Existe sólo para sacar al owner del loop antes de comenzar la operación repetitiva.

## 🏛️ Modelo de agentes / autoridad

Hermes actúa como **orquestador**. La ejecución concreta debe poder separarse en operadores especializados con system prompt, credenciales, herramientas y scope propios.

Roles lógicos iniciales — no implican todavía un framework ni procesos separados obligatorios:

```text
Hermes / Ariadna
├── backup / storage operator
├── proxmox operator
├── linux / container operator
├── windows operator
├── service operator
└── access-plane operator
```

La implementación puede consolidar o separar estos roles según evidencia real. La separación de autoridad importa más que el número de agentes. En v1 se prefieren **skills + connections/credentials separadas**; un perfil/subagente nuevo sólo aparece cuando agrega aislamiento real.

### Niveles conceptuales

- **Consumer:** Echo, Forge y futuros agentes. Consumen capabilities publicadas; no administran Aranea.
- **Operator:** skills/perfiles/subagentes Hermes con acceso nativo scoped para una responsabilidad concreta.
- **Orchestrator:** Ariadna/Hermes decide qué operador usar, coordina, valida evidencia, escala bloqueos y actualiza Agents-OS.

## 🔐 Principios frozen para v1

1. **Management plane != MCP Access Plane.** Hermes debe conservar un path administrativo independiente.
2. **Privilegios progresivos.** No entregar autoridad total al inicio; cada etapa se certifica antes de ampliar la siguiente.
3. **Separación por responsabilidad.** Prompts, credentials y tools se asignan al operador que las necesita.
4. **Secrets por referencia.** Nunca persistir valores secretos en Agents-OS, prompts o handoffs.
5. **Target proof antes de mutar.** Toda mutación debe demostrar host/servicio/entorno real antes de ejecutarse.
6. **DEV/test primero.** La autonomía de mutación se certifica primero fuera de PROD.
7. **PROD no es autónomo por defecto.** Mutaciones PROD requieren un gate explícito hasta que el owner cambie esta política.
8. **Consumer-side verification.** Una capability agent-facing no está lista sólo porque el servidor responde; debe pasar desde el consumidor real o harness equivalente certificado.
9. **Reuse > repair > extend > wrap > build.** No construir MCPs o tooling nuevo si una superficie existente puede servir de forma segura.
10. **Agents-OS es el estado durable.** Los proyectos de agente deben permitir que un agente fresco continúe sin depender del chat anterior.
11. **Rollback/revoke obligatorio para cambios de autoridad.** Toda ampliación operativa debe poder revertirse o revocarse.
12. **KISS/YAGNI.** No crear dashboard, policy DSL, capability database ni provider framework genérico antes de demostrar repetición real.
13. **Human actions are bootstrap debt.** Toda acción manual repetida del owner debe eliminarse, automatizarse o quedar clasificada como gate excepcional.
14. **Batch owner intervention.** Hermes acumula necesidades de bootstrap en un único `OWNER ACTION BUNDLE`; no dirige al owner comando por comando salvo dependencia secuencial real.

## 🛣️ Orden de implementación operativo

Aunque existen dos workstreams permanentes, **la ejecución inicial es deliberadamente serial** para maximizar independencia y minimizar intervención humana.

### Fase 0 — B0/B4: sacar al owner del loop

Proyecto: [[HERMES — Bootstrap & Self-Sufficiency]].

Objetivo:

```text
perfil/autonomía
→ direct management path a mcps
→ consumer onboarding path
→ operator skill
→ golden repair/deploy
→ HUMAN EXIT
```

El owner acepta trabajo manual sólo aquí para instalar las primeras identities/keys/configs que Hermes aún no pueda auto-provisionar.

**Gate:** Hermes puede administrar el MCP Access Plane y publicar una capability DEV/test sin shell/config manual rutinaria del owner.

### Fase 1 — A0/A5: autonomía del Agent Access Plane

Proyecto: [[HERMES — Agent Access Operations]].

Hermes convierte el bootstrap en operación reusable:

```text
request funcional
→ discover
→ reuse/repair/extend/deploy
→ certify server
→ certify consumer
→ publish
→ register
```

**Gate:** un request nuevo DEV/test puede resolverse end-to-end sin intervención humana, salvo authority realmente ausente.

### Fase 2 — Echo + Echo Forge: cerrar blockers reales

Con A0-A5 operativo, Hermes toma la cola real de Echo/Forge. Primero reconcilia el blocker report contra el plano vigente para no rehacer capabilities ya existentes.

Prioridad de ejecución:

1. marcar `PASS` todo requirement ya cubierto por capabilities certificadas;
2. extender/configurar capabilities existentes antes de desplegar nuevas;
3. desplegar capabilities faltantes;
4. devolver evidencia consumible a los carriles Echo/Forge;
5. cerrar sólo blockers de infraestructura/capability; no invadir decisiones de producto/código de esos proyectos.

**Gate:** Echo y Forge dejan de depender del owner para obtener acceso operativo a servicios DEV/test.

### Fase 3 — H1: habilitación administrativa de Backup & Storage

Proyecto: [[HERMES — Infrastructure Operations]], reutilizando [[BACKUP-DR-OWNER-PROJECT]].

**Alcance corregido (decisión owner 2026-09-18):** H1 es **habilitación** — Ariadna certifica identidades, permisos efectivos, rutas nativas de administración y recuperación independiente, y las entrega como capacidades listas para consumir. La **ejecución** (jobs, backups, restores, drills, retención) pertenece al proyecto Backup/DR, no a este carril.

```text
inventory H0 (DONE 2026-09-18)
→ reconciliación de accesos administrativos
→ certificación read-only por familia (matriz de autoridad)
→ verificación del consumidor real en sesión fresca
→ handoff de capacidades a Backup/DR (R2 las consume)
```

**Gate:** las capacidades administrativas necesarias están certificadas y el proyecto Backup/DR puede consumirlas sin bootstrap manual rutinario. H1 no implica backups/jobs/retención/restores existentes ni certificados.

### Fase 4 — H2/H6: administración completa de Aranea

Expansión progresiva después de H1:

```text
H2 Proxmox lifecycle
→ H3 guest/service operations
→ H4 provisioning
→ H5 high-impact infra
→ H6 integrated autonomy
```

La meta H4 incluye que Hermes pueda **instalar servicios nuevos, configurarlos, levantarlos, integrarlos con observabilidad/backups y destruirlos cuando corresponda**, dentro de authority aprobada y con rollback/evidencia.

H5/H6 agregan networking, storage/cluster de mayor blast radius y recoveries multi-capa sólo después de demostrar seguridad operacional en etapas anteriores.

## 🚦 Rollout de Infrastructure Operations

La madurez de infraestructura se versiona de forma independiente de la madurez del access plane.

| Nivel | Alcance | Gate de salida |
|---|---|---|
| **H0 — Observe** | inventario, topología, health, configuración no secreta, relaciones host/VM/LXC/service | Hermes puede reconstruir el estado real sin mutar y detectar drift básico |
| **H1 — Backup & Storage Administrative Enablement** *(corregido 2026-09-18)* | habilitación administrativa: identidades, permisos efectivos, rutas nativas y recuperación para TrueNAS/PBS/targets, certificadas read-only; la ejecución de backups/restores es del proyecto [[BACKUP-DR-OWNER-PROJECT]] | capacidades certificadas consumibles por R2 sin bootstrap manual rutinario — **H1 ENABLEMENT PASS 2026-09-18** |
| **H2 — Proxmox Lifecycle** | inspect/start/stop/reboot/create/clone/configurar VMs/LXC dentro de scopes definidos | habilitación cerrada 2026-09-18 (`H2 ENABLEMENT PASS`): matriz de autoridad clasificada read-only + contrato del operador ([[proxmox-lifecycle-operator-contract]]); la certificación operativa (lifecycle ejecutado con target proof y rollback) la demuestra el proyecto ejecutor |
| **H3 — Guest & Service Operations** | Linux, Windows, Docker, systemd, filesystem/config y restart de servicios | diagnóstico + reparación de un servicio DEV/test sin intervención humana |
| **H4 — Provisioning** | levantar VMs/LXC/containers, instalar/configurar software, onboarding backup/observability y teardown controlado | servicio DEV/test provisionado y retirado reproduciblemente con evidencia |
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

Para Infrastructure Operations, el equivalente es que Hermes pueda recibir un objetivo operativo —por ejemplo proteger un nuevo servicio, crear una VM DEV, instalar/configurar una aplicación o recuperar un daemon— y completar la operación dentro de su authority vigente con target proof, rollback y evidencia.

## 📊 Estado actual

- **Proyecto creado:** 2026-09-14.
- **Plan de implementación reordenado:** Bootstrap/Human Exit → Agent Access autonomy → Echo/Forge blockers → Backup/Storage → full Infrastructure autonomy.
- **Bootstrap:** activo como [[HERMES — Bootstrap & Self-Sufficiency]].
- **Infrastructure Operations:** authority incremental aún por bootstrap; ejecución H0/H1 queda después del cierre del P0 Echo/Forge.
- **Agent Access Operations:** existe un MCP Access Plane funcional y en evolución bajo [[AGENT-PLATFORM - MCP Access Plane]], pero Hermes todavía no dispone del ciclo autónomo completo A0→A5.
- **Dependencias ya existentes:** [[BACKUP-DR-OWNER-PROJECT]] para Backup/DR y [[AGENT-PLATFORM - MCP Access Plane]] para la implementación MCP actual.
- **Prioridad inmediata:** completar B0-B4 y sacar al owner del loop antes de resolver más MCPs manualmente.

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
> Los dos workstreams son permanentes. Bootstrap es transitorio y debe cerrarse primero. El detalle operativo vive en cada proyecto `owner: agent`.

- [x] [[HERMES — Bootstrap & Self-Sufficiency]] sacar al owner del loop — B4 Human Exit Gate PASS 2026-09-15; proyecto en Review, owner fuera de la configuración MCP rutinaria #owner/me #type/supervision #area/aranea
- [ ] [[HERMES — Agent Access Operations]] autonomía MCP + desbloqueo Echo/Forge #owner/me #type/supervision #area/aranea
- [/] [[HERMES — Infrastructure Operations]] backups → administración integral #owner/me #type/supervision #area/aranea

## 📆 Bitácora

- **2026-09-18 — H2 ENABLEMENT PASS (mandato owner):** [[HERMES — Infrastructure Operations]] certificó read-only la capacidad administrativa Proxmox lifecycle (familias A–G, 34 operaciones: 9 verificadas en lectura, 24 autorizadas-no-ejercidas vía SSH root-equivalent, destroy owner-gated), creó el contrato del futuro operador ([[proxmox-lifecycle-operator-contract]]) y verificó el consumidor en sesión fresca. Cero mutaciones; sin owner bundle. La ejecución lifecycle queda para el proyecto ejecutor que la consuma. Detalle: `80-agents/journal/logs/2026-09-18-h2-proxmox-enablement.md`.
- **2026-09-18 — H1 ENABLEMENT PASS (mandato owner; corrección de alcance):** la Fase 3 queda como habilitación administrativa (no ejecución de backups): [[HERMES — Infrastructure Operations]] certificó read-only PVE/TrueNAS/PBS (SSH `ariadna`+sudo en 7/7 targets, API/WS funcionales, matriz de autoridad en esa nota), verificó el consumidor en sesión fresca y entregó handoff a R2. La ejecución de PBS/jobs/restores sigue en [[BACKUP-DR-OWNER-PROJECT]] (su R2 discovery ya corrió hoy con bundle owner propio). Propuesta de cambio contractual (gate por-acción → gates por clase) preparada y NO aplicada. Detalle: `80-agents/journal/logs/2026-09-18-h1-enablement.md`.
- **2026-09-14** — Se reordena la implementación para minimizar intervención humana: bootstrap transitorio primero; luego autonomía MCP; después blockers Echo/Forge; luego Backup/DR; finalmente expansión H2-H6.
- **2026-09-14** — Proyecto creado. Se separan formalmente las responsabilidades de administración integral del homelab y habilitación MCP para agentes. Se congela el principio de management path independiente y el rollout dual H0→H6 / A0→A5.
- **2026-09-15** — **Bootstrap B4 PASS: Human Exit Gate cerrado.** Residual B3.3 (env del chain de kor) eliminado por Hermes sin owner — chain-cert PASS, rollback byte-identical y re-aplicación convergente demostrados. Las 9 condiciones del gate certificadas con evidencia runtime/durable (detalle: `80-agents/journal/logs/2026-09-15-b4-human-exit-gate-pass.md`). [[HERMES — Bootstrap & Self-Sufficiency]] pasa a **Review**: el bootstrap transitorio terminó. [[HERMES — Agent Access Operations]] asume la continuidad; los blockers reales de Echo/Forge son su primer workload A0-A5. El owner deja de hacer configuración MCP rutinaria.

## 🧭 Decisiones

- **D-01 — Dos workstreams independientes.** Infrastructure Operations y Agent Access Operations tienen authority, herramientas, credenciales y criterios de madurez distintos.
- **D-02 — Ariadna/Hermes orquesta; operadores ejecutan.** Skills/connections separadas son el default inicial; perfiles/subagentes adicionales sólo con beneficio material de aislamiento.
- **D-03 — MCP es consumer plane, no recovery plane.** El MCP Access Plane sirve a agentes de desarrollo; Hermes conserva interfaces administrativas nativas para operar/recuperar servicios.
- **D-04 — Secuencia inicial serial.** Primero Human Exit, luego Access Plane, luego Echo/Forge, luego Backup/DR y después infraestructura completa. No se paraleliza mientras el owner siga siendo dependencia operativa.
- **D-05 — Existing systems remain canonical.** Backup/DR y MCP Access Plane existentes se reutilizan; este proyecto no duplica su source of truth.
- **D-06 — Owner Action Bundle.** El trabajo manual de bootstrap debe pedirse batcheado y minimizarse; cada repetición futura se trata como deuda de automatización.

## 🔗 Docs / Links

- [[HERMES — Bootstrap & Self-Sufficiency]] — bootstrap transitorio CERRADO: Human Exit Gate PASS 2026-09-15, en Review.
- [[HERMES — Agent Access Operations]] — autonomía del capability plane y desbloqueo de Echo/Forge.
- [[HERMES — Infrastructure Operations]] — Backup/Storage y expansión a administración integral.
- [[Ariadna]] — identidad operativa existente sobre Hermes Agent.
- [[Aranea]] — área del homelab.
- [[BACKUP-DR-OWNER-PROJECT]] — diseño/proyecto canónico de Backup/DR usado por H1.
- [[AGENT-PLATFORM-OWNER-PROJECT]] — iniciativa donde vive el MCP Access Plane existente.
- [[AGENT-PLATFORM - MCP Access Plane]] — source of truth operativo del capability plane MCP.
- [[aranea-mcps-expert]] — skill agent-facing canónica del MCP plane; no se convierte en operador privilegiado.

## 💡 Ideas

### Backlog de ideas

- Extraer skills/provider archetypes sólo cuando varios servicios demuestren el mismo patrón repetible.
- Evaluar break-glass formal, policy engine o JIT credentials únicamente cuando la autonomía real haga insuficientes los gates simples de v1.

### Motivos / principios

- La prioridad inmediata no es darle más herramientas al owner: es eliminar al owner como relay técnico.
- La autonomía se expande por authority certificada y escenarios reales, no por entregar root global anticipadamente.
- Una capability sólo agrega valor cuando el consumidor real puede usarla y Hermes puede recuperarla si falla.

### Memoria pública / interna

- **Memoria pública:** este proyecto, Bootstrap y sus dos workstreams son la fuente durable de estado, decisiones, etapas y blockers del programa.
- **Memoria interna:** conocimiento efímero del agente sólo se conserva si cambia el plan, una decisión o un procedimiento reusable.
- **Motivo:** permitir continuidad entre sesiones y agentes sin depender del chat ni duplicar facts de Backup/DR o MCP Access Plane.