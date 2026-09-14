---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Aranea]]"
parent: "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
sprint:
start: 2026-09-14
due:
progress: 0
repo:
jira:
prs:
slug: hermes-infrastructure-operations
aliases:
  - Hermes Infrastructure Operations
  - Hermes Homelab Administration
  - Hermes Infra Ops
tags:
  - kind/project
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - agent/hermes
  - domain/infrastructure
created: "2026-09-14"
updated: "2026-09-14"
---

# HERMES — Infrastructure Operations

> [!info]+ Infrastructure Operations
> **Padre:** [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1

## 🎯 Objetivo

Dar a Hermes autoridad operativa **paulatina, verificable y recuperable** sobre Aranea hasta poder administrar de extremo a extremo el homelab: storage, backups, TrueNAS, Proxmox, nodos, VMs/LXC, Linux/Windows, Docker, lifecycle de servicios, provisioning y componentes de mayor impacto cuando sean habilitados explícitamente.

Este workstream define el **management plane nativo** de Hermes. No depende del MCP Access Plane para reparar o administrar el mismo plano MCP ni los servicios subyacentes.

## 🧠 Contexto

Hermes será el administrador general del homelab, pero entregar root-equivalent sobre todo Aranea desde el primer día generaría demasiado blast radius y dificultaría saber qué autoridad está realmente certificada.

La estrategia es progresiva:

```text
observe
→ protect storage/backups
→ operate Proxmox lifecycle
→ operate guests/services
→ provision new infrastructure
→ enable high-impact infrastructure
→ integrated autonomy
```

El conocimiento existente de Backup/DR se reutiliza desde [[BACKUP-DR-OWNER-PROJECT]]. Este workstream **no rediseña Backup/DR**; lo usa como primer dominio real para certificar el modelo de autonomía.

## 🏛️ Boundary

### Este workstream SÍ gobierna

- authority/bootstrap de Hermes sobre interfaces administrativas nativas;
- inventario y discovery de infraestructura;
- administración de Proxmox/TrueNAS/hosts/guests según etapa activa;
- acceso Linux/Windows para operación;
- Docker/systemd/filesystem/configuración no secreta;
- service lifecycle y recovery;
- provisioning de infraestructura cuando H4 quede habilitado;
- gates, rollback, revoke y evidencia de cada nivel.

### Este workstream NO gobierna

- capabilities MCP entregadas a Echo/Forge/agentes: eso vive en [[HERMES — Agent Access Operations]];
- endpoints/permisos exactos del MCP Access Plane: source of truth [[AGENT-PLATFORM - MCP Access Plane]];
- redefinir la estrategia Backup/DR: source of truth [[BACKUP-DR-OWNER-PROJECT]];
- mutaciones PROD no autorizadas explícitamente.

## 🔐 Principios de autoridad

1. Hermes recibe sólo la autoridad necesaria para el nivel H actualmente certificado.
2. Un operador especializado recibe tools/credentials sólo para su responsibility boundary.
3. Los valores secretos nunca se escriben en Agents-OS; sólo referencias.
4. Antes de cualquier mutación se demuestra target, entorno y blast radius.
5. Toda nueva autoridad debe tener revoke/rollback viable.
6. Un management path no puede depender exclusivamente del servicio/plano que debe recuperar.
7. PROD/high-impact permanece gated hasta decisión explícita del owner.

## 🚦 Roadmap H0 → H6

### H0 — Observe / Inventory

**Objetivo:** Hermes puede reconstruir el estado real de Aranea sin mutar.

- inventario de nodos físicos/virtualizados;
- Proxmox cluster resources;
- TrueNAS/storage topology y health;
- VMs/LXC, host placement y estado;
- services/runtimes relevantes;
- interfaces administrativas disponibles;
- relaciones service → guest → host → storage;
- identificación de gaps de autoridad/credenciales por referencia.

**Gate:** un agente fresco puede diagnosticar dónde vive un servicio y qué management path usar sin preguntar al owner por datos ya documentados.

### H1 — Backup & Storage

**Objetivo:** Hermes opera protección y recovery básico usando el diseño vigente.

- leer y reconciliar [[BACKUP-DR-OWNER-PROJECT]];
- ejecutar/verificar backups dentro del scope aprobado;
- health de targets/storage;
- detectar jobs fallidos o cobertura incompleta;
- validar evidencia de restore;
- ejecutar restore drill acotado;
- registrar findings y drift en Agents-OS.

**Gate:** la operación normal de backup/restore evidence no requiere shell humana habitual.

### H2 — Proxmox Lifecycle

**Objetivo:** Hermes administra lifecycle de VMs/LXC con scopes explícitos.

- inspect/config/status;
- start/stop/reboot;
- create/clone cuando el scope esté aprobado;
- resource/config changes acotados;
- validación post-change;
- rollback/recovery.

**Gate:** lifecycle completo certificado sobre workloads no críticos antes de ampliar scope.

### H3 — Guest & Service Operations

**Objetivo:** Hermes diagnostica y repara servicios dentro de guests.

- Linux SSH;
- Windows management path;
- Docker/Compose;
- systemd/services;
- filesystem/configuración;
- logs/health;
- restart/recovery;
- verificación funcional post-repair.

**Gate:** reparar un servicio DEV/test roto end-to-end sin intervención humana.

### H4 — Provisioning

**Objetivo:** Hermes puede levantar infraestructura nueva reproducible.

- VM/LXC/containers;
- OS/bootstrap;
- instalación/configuración de software;
- networking/config necesaria dentro del scope;
- observabilidad y backup onboarding;
- documentation/state registration.

**Gate:** nuevo servicio DEV/test provisionado desde objetivo funcional hasta health/backup/documentación.

### H5 — High-impact Infrastructure

**Objetivo:** habilitar progresivamente operaciones de mayor blast radius.

Ejemplos potenciales: networking, cluster/storage operations, quorum-sensitive services, cambios host-level críticos.

**Gate:** cada familia tiene recovery demostrado, authority específica y criterios de abort/rollback.

### H6 — Integrated Autonomy

**Objetivo:** Hermes coordina incidentes y cambios multi-capa usando operadores especializados.

**Gate:** tareas habituales y recoveries previstos requieren intervención humana excepcional, no como paso normal del procedimiento.

## 🤖 Operadores lógicos previstos

La separación exacta se ajustará por evidencia; punto de partida:

- `backup/storage operator`
- `proxmox operator`
- `linux/container operator`
- `windows operator`
- `service operator`

No se crea un framework genérico de operadores por anticipación. Primero se certifican paths reales; después se extraen skills/prompts reutilizables.

## 🧪 Acceptance scenarios

Este workstream debe demostrar progresivamente escenarios reales, no sólo acceso técnico:

- identificar host/guest de un servicio desde nombre lógico;
- detectar backup faltante o job fallido;
- validar un backup y restaurar una muestra acotada;
- reiniciar de forma segura un servicio DEV/test;
- recuperar un MCP/runtime caído usando el management path nativo;
- crear/provisionar un workload no crítico cuando H4 esté activo;
- registrar evidencia suficiente para que otro agente continúe.

## 📊 Estado actual

- Workstream creado 2026-09-14.
- **Nivel actual:** pre-H0 / bootstrap de authority aún no certificado de forma integral.
- Existen capacidades operativas parciales distribuidas en el homelab, pero no deben asumirse como authority Hermes hasta reconciliarlas y probarlas desde su runtime real.
- Primer dominio propuesto: **H0 inventory + H1 Backup & Storage**.
- [[BACKUP-DR-OWNER-PROJECT]] permanece como autoridad del diseño Backup/DR; este proyecto opera la autonomía alrededor de ese diseño.

## 🧱 Entrega de desarrollo

_No aplica como repo único. Este workstream puede cambiar configuración ejecutable e infraestructura; antes de cada implementación se debe registrar el target real, source of truth, baseline, scope y rollback en la tarea correspondiente. Si aparece código/versioned config, se agrega repo/branch/base/SPEC antes de modificarlo._

## ✅ Tareas

### I0 — Bootstrap del management plane

- [ ] I0.1 Inventariar interfaces administrativas realmente disponibles para Hermes #owner/agent #type/research #area/aranea
- [ ] I0.2 Clasificar authority actual por target: observe / operate / provision / absent #owner/agent #type/admin #area/aranea
- [ ] I0.3 Definir referencias de credenciales y boundaries sin persistir secretos #owner/agent #type/admin #area/aranea
- [ ] I0.4 Certificar que Hermes conserva recovery path independiente del MCP Access Plane #owner/agent #type/admin #area/aranea

### I1 — H0 Observe

- [ ] I1.1 Reconciliar inventario real de nodes/hosts/VMs/LXC/storage/services #owner/agent #type/admin #area/aranea
- [ ] I1.2 Construir mapa service → guest → host → management path #owner/agent #type/admin #area/aranea
- [ ] I1.3 Definir evidence contract mínimo para operations #owner/agent #type/admin #area/aranea
- [ ] I1.4 Certificar H0 desde runtime Hermes #owner/agent #type/admin #area/aranea

### I2 — H1 Backup & Storage

- [ ] I2.1 Cargar y reconciliar [[BACKUP-DR-OWNER-PROJECT]] sin rediseñarlo #owner/agent #type/admin #area/aranea
- [ ] I2.2 Identificar authority faltante para backups/storage/restore #owner/agent #type/admin #area/aranea
- [ ] I2.3 Certificar operación de backup/health dentro de scope aprobado #owner/agent #type/admin #area/aranea
- [ ] I2.4 Ejecutar restore drill acotado y registrar evidencia #owner/agent #type/admin #area/aranea
- [ ] I2.5 Declarar H1 PASS o blockers precisos #owner/agent #type/admin #area/aranea

### I3 — Expansión H2→H6

- [ ] I3.1 Planificar H2 Proxmox lifecycle sólo después de H1 #owner/agent #type/admin #area/aranea
- [ ] I3.2 Planificar H3 guest/service operations sólo con management paths certificados #owner/agent #type/admin #area/aranea
- [ ] I3.3 Planificar H4 provisioning con onboarding a backup/observability/documentación #owner/agent #type/admin #area/aranea
- [ ] I3.4 Mantener H5 high-impact gated hasta aprobación explícita del owner #owner/agent #type/admin #area/aranea
- [ ] I3.5 Definir criterio medible de H6 sólo después de escenarios reales repetidos #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-14** — Workstream creado. Se fija rollout H0→H6 y se define H0/H1 como primer tramo. Backup/DR existente será reutilizado como primer dominio de autonomía, no duplicado.

## 🧭 Decisiones

- **I-D01:** management path nativo es obligatorio para recovery del MCP Access Plane y servicios administrados.
- **I-D02:** autoridad progresiva por nivel; no root-equivalent global inicial.
- **I-D03:** storage/backups es el primer dominio operativo por prioridad y porque permite certificar el patrón de seguridad/recovery antes de Proxmox completo.
- **I-D04:** operadores especializados son boundaries de autoridad; su implementación concreta se difiere hasta ver las interfaces reales.

## 🔗 Docs / Links

- [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] — programa padre.
- [[BACKUP-DR-OWNER-PROJECT]] — source of truth de Backup/DR.
- [[HERMES — Agent Access Operations]] — workstream paralelo del capability plane.
- [[AGENT-PLATFORM - MCP Access Plane]] — plano que Infrastructure Operations debe poder recuperar sin depender de él.

## 💡 Ideas

### Backlog de ideas

- Detectar cuáles operators merecen perfil/agent separado después del primer ciclo H0/H1.
- Incorporar drills periódicos de recovery cuando el management plane sea estable.

### Motivos / principios

- La autonomía vale sólo si Hermes puede recuperarse de la falla de las superficies que administra.
- El blast radius debe aumentar más lento que la evidencia de operación segura.