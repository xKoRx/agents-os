---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM-OWNER-PROJECT]]"
sprint:
start: 2026-09-07
due:
progress: 5
repo:
jira:
prs:
aliases:
  - MCP Access Plane
  - Centralización MCP
  - MCP Gateway
tags:
  - kind/project
  - area/aranea
  - project/aranea-agent-platform
  - tech/mcp
created: "2026-09-07"
updated: "2026-09-07"
---

# AGENT-PLATFORM - MCP Access Plane

> [!info]+ Access plane compartido para agentes
> **Padre:** [[AGENT-PLATFORM-OWNER-PROJECT]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1

## 🎯 Objetivo

- Convertir el host MCP existente de Aranea en un access plane reutilizable para Hermes, Daedalus y agentes futuros, centralizando sesiones, credenciales reales, perfiles de acceso, auditoría y políticas sin repartir secretos de los servicios destino entre máquinas o runtimes.
- Adoptar MCPs existentes antes de construir; modificar o forkear sólo cuando un gap real de seguridad, persistencia o caso de uso quede demostrado.

## 📊 Estado actual

- T0 está WIP. El host MCP existente tiene sólo PostgreSQL MCP; no existe aún un access plane multi-capability.
- La implementación actual usa Docker Compose con `crystaldba/postgres-mcp:latest` para SSE y una imagen local `local/postgres-mcp-streamable:latest` para Streamable HTTP. Hay tres perfiles lógicos (`echo` prod RO, `echo-develop` RO y `echo_mcp` RW sandbox) duplicados entre ambos transportes y tres proxies Nginx adicionales para compatibilidad con Antigravity.
- La configuración muestra hardening de contenedor útil (`read_only`, `/tmp` tmpfs, `no-new-privileges`, `cap_drop: ALL`, límites de PID/memoria), pero también deuda de diseño: tags `latest`, imagen local no versionada, duplicación 3×2 de backends, proxies de compatibilidad, credenciales por variables de entorno y ninguna autenticación cliente→MCP visible en el Compose entregado.
- La implementación está actualmente sin uso y el owner autoriza retirarla si conviene. No se reutilizará como arquitectura objetivo por defecto; primero se completa T0 y luego se decide entre migración mínima o reemplazo limpio.
- La arquitectura [[AGENT-PLATFORM-ARCHITECTURE]] ya define MCP como denominador común del Capability Plane y registra que existen servicios MCP en Aranea; este proyecto materializa esa capacidad de forma incremental.

## 🧱 Entrega de desarrollo

_No aplica por ahora — la primera etapa es discovery y configuración operativa sobre infraestructura existente. Si una tarea requiere cambiar código, configuración versionada, schemas o infraestructura mediante repositorio, se registrarán repo/branch/base y SPECs antes de implementar ese cambio._

## 🧩 Subproyectos

- Ninguno.

## ✅ Tareas

> [!note]+ Fuente única de planificación
> Estas tareas `#owner/agent` viven sólo en este proyecto. Cada tarea debe poder cerrarse y validarse de forma independiente antes de avanzar a la siguiente.

> [!example]- Roadmap incremental
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [/] T0 Inventariar el host MCP existente: runtime, MCPs instalados, versiones, transporte, puertos, autenticación, persistencia, secretos, usuarios de servicio, red, logs y forma de despliegue #owner/agent #type/research #area/aranea
> - [ ] T1 Definir y congelar el contrato mínimo de acceso: consumidores, aliases/profiles, least privilege, ubicación de secretos, autenticación cliente→MCP, auditoría, política de red y separación entre credenciales del MCP y credenciales del servicio destino #owner/agent #type/research #area/aranea
> - [ ] T2 Seleccionar y validar SSH MCP con un solo host de laboratorio: sesión persistente, host-key verification, perfiles read/operator, timeout, auditoría y cero private keys entregadas al agente #owner/agent #type/admin #area/aranea
> - [ ] T3 Seleccionar y validar PostgreSQL MCP con una sola base de desarrollo: perfiles RO/RW, credencial centralizada, límites de query/timeout y convivencia con `psql` nativo #owner/agent #type/admin #area/aranea
> - [ ] T4 Seleccionar y validar MongoDB MCP con una sola base de desarrollo: perfiles RO/RW, `readOnly`/protecciones equivalentes, límites de consulta y convivencia con `mongosh` nativo #owner/agent #type/admin #area/aranea
> - [ ] T5 Seleccionar y validar Temporal MCP: comenzar read-only con allowlist de namespaces; evaluar `signal/start/cancel` sólo después de demostrar la necesidad y el modelo de policy correspondiente #owner/agent #type/admin #area/aranea
> - [ ] T6 Consolidar los cuatro MCP aprobados en el host central, integrar al menos Hermes y Daedalus, demostrar que ambos consumen capabilities sin recibir credenciales reales de los servicios destino, y dejar health checks, logs, rotación/rollback y runbook operativo mínimo #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-07** — T0 iniciado con inventario real del Compose existente. Sólo hay PostgreSQL MCP. La solución rápida actual materializa 9 contenedores para 3 perfiles lógicos: 3 SSE con `crystaldba/postgres-mcp:latest`, 3 Streamable HTTP desde una imagen local y 3 Nginx para compatibilidad de Host/Antigravity. La implementación está sin uso; se preserva sólo hasta completar el inventario y no se toma como arquitectura objetivo.
- **2026-09-07** — Proyecto creado para materializar incrementalmente el Capability Plane ya definido en [[AGENT-PLATFORM-ARCHITECTURE]]. Scope inicial congelado a SSH, PostgreSQL, MongoDB y Temporal; MinIO, Kafka y observabilidad quedan fuera hasta estabilizar este patrón. No se crea una VM nueva ni se migra el host MCP existente antes de completar T0-T1.

## 🧭 Decisiones

- D1: centralizar credenciales y sesiones MCP en un host dedicado es la dirección preferida; los agentes consumen capabilities y perfiles, no secretos de los servicios destino.
- D2: el host/contenedor MCP existente es el baseline de discovery, no una arquitectura a preservar. Reutilizarlo, limpiarlo o reemplazarlo se decide después de T0-T1; una VM nueva requiere evidencia material de que el host actual no cumple aislamiento, mantenimiento, red o disponibilidad.
- D3: un host central no implica una identidad omnipotente. Cada MCP/perfil debe usar credenciales finales separadas y least-privilege en SSH, PostgreSQL, MongoDB y Temporal.
- D4: mantener clientes nativos (`ssh`, `psql`, `mongosh`, Temporal CLI) donde aporten valor; MCP es la capa reusable para agentes, no una prohibición del acceso nativo.

## 🔗 Docs / Links

- [[AGENT-PLATFORM-ARCHITECTURE]] — arquitectura v1 y definición del Capability Plane.
- [[AGENT-PLATFORM-OWNER-PROJECT]] — cockpit humano padre.

## 💡 Ideas

### Backlog de ideas

- Extender el access plane a MinIO/S3, Kafka y observabilidad sólo después de cerrar T6 y demostrar que el patrón reduce credenciales distribuidas y fricción operacional.

### Motivos / principios

- KISS/YAGNI: reutilizar el host MCP y software existente antes de crear infraestructura o código nuevo.
- Seguridad por capas: restricción de red + autenticación MCP + policy/profile + credencial final least-privilege.

### Memoria pública / interna

- **Memoria pública:** este proyecto conserva decisiones y estado durable; los contratos operativos estables podrán promoverse a runbook/documentación cuando queden verificados.
- **Memoria interna:** no se crea memoria adicional mientras el planificador contenga todo el estado necesario.
- **Motivo:** evitar duplicar el roadmap o la autoridad de acceso fuera del proyecto.
