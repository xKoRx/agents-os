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
progress: 55
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
updated: "2026-09-10"
---

# AGENT-PLATFORM - MCP Access Plane

> [!info]+ Access plane compartido para agentes
> **Padre:** [[AGENT-PLATFORM-OWNER-PROJECT]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1

## 🎯 Objetivo

- Convertir el host MCP existente de Aranea en un access plane reutilizable para Hermes, Daedalus y agentes futuros, centralizando sesiones, credenciales reales, perfiles de acceso, auditoría y políticas sin repartir secretos de los servicios destino entre máquinas o runtimes.
- Adoptar MCPs existentes antes de construir; modificar o forkear sólo cuando un gap real de seguridad, persistencia o caso de uso quede demostrado.

## 📊 Estado actual

- T0 cerrado. `mcps` es un LXC dedicado con Docker + Portainer; IP actual `192.168.31.219`, considerada mutable y no parte del contrato estable.
- El stack PostgreSQL MCP anterior fue retirado completamente. Sólo `portainer` queda ejecutándose.
- DNS de `mcps` fue corregido para usar Pi-hole `192.168.31.31` y search domain `lab.aranea.cl`; `mcps.lab.aranea.cl` es el endpoint estable usado por consumidores.
- T1 sigue WIP y T2 está WIP, pero el SSH MCP ya está operacionalmente usable desde Cursor/Daedalus con cuatro perfiles read-only: `sqx-zeus`, `sqx-hera`, `sqx-kronos` y `mt5-kronos`.
- Las host keys ED25519 de todos los targets están pinneadas y validadas. Hera y Kronos regeneraron keys únicas porque las VMs clonadas compartían originalmente la misma identidad SSH que Zeus.
- La identidad SSH dedicada `echo-dev@mcps`, fingerprint `SHA256:2Qv9f2AREQyse50bGYaTLc1PHK43gvuf3xgv5TTJ+I0`, se reutiliza para los cuatro targets. La key genérica `mcp-access@mcps` queda fuera del diseño y no debe autorizarse.
- En los Linux SQX existe usuario remoto dedicado `echo-dev`, password bloqueado, sin sudo ni grupos extra. En `mt5-kronos` existe `echo-dev` como usuario local no-admin con autenticación OpenSSH por public key.
- `tufantunc/ssh-mcp` quedó validado preliminarmente en v2.8.0, source tag `v2.8.0` / commit `d2d769684701e0939c1d8e56cbdde3d77fed53ef`, imagen local `local/ssh-mcp:2.8.0-d2d7696`, ejecutando como usuario no-root.
- El servidor MCP HTTP está activo en `mcps`, con bearer obligatorio, rate limit, protección de Host y `hostKeyMode=strict`; endpoint estable actual `http://mcps.lab.aranea.cl:3000/`.
- Gate cliente cerrado desde Daedalus: resolución DNS + `/health` + `/status` autenticado + handshake MCP + `tools/call read-command`; Cursor consume el MCP como herramienta real sin recibir private keys SSH.
- Diagnóstico útil validado en Zeus: `echo-dev` puede leer `/home/kor/sqx/user/log/...` mediante ACL mínima de traversal en `/home/kor`, sin poder enumerar el home completo.
- Validación multi-target desde Cursor PASS: `read-command` devolvió `echo-dev`/`sqx-ulab-zeus-0`, `echo-dev`/`sqx-ulab-hera-0`, `echo-dev`/`sqx-ulab-kron-0` y `worker-kronos\\echo-dev`/`worker-kronos` respectivamente. `run-command` fue rechazado por diseño al estar todos los perfiles en `viewer` + `readOnly=true`.
- T2 aún no se cierra formalmente: faltan validar sesión persistente/background, timeout, auditoría y el perfil operator/least-privilege antes de declarar el SSH MCP completamente aprobado.

## 🧱 Entrega de desarrollo

_No aplica por ahora — la primera etapa es discovery y configuración operativa sobre infraestructura existente. Si una tarea requiere cambiar código, configuración versionada, schemas o infraestructura mediante repositorio, se registrarán repo/branch/base y SPECs antes de implementar ese cambio._

## 🧩 Subproyectos

- Ninguno.

## ✅ Tareas

> [!note]+ Fuente única de planificación
> Estas tareas `#owner/agent` viven sólo en este proyecto. Cada tarea debe poder cerrarse y validarse de forma independiente antes de avanzar a la siguiente.

> [!example]- Roadmap incremental
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] T0 Inventariar el host MCP existente: runtime, MCPs instalados, versiones, transporte, puertos, autenticación, persistencia, secretos, usuarios de servicio, red, logs y forma de despliegue #owner/agent #type/research #area/aranea
> - [/] T1 Definir y congelar el contrato mínimo de acceso: consumidores, aliases/profiles, least privilege, ubicación de secretos, autenticación cliente→MCP, auditoría, política de red y separación entre credenciales del MCP y credenciales del servicio destino #owner/agent #type/research #area/aranea
> - [/] T2 Seleccionar y validar SSH MCP con un solo host de laboratorio: sesión persistente, host-key verification, perfiles read/operator, timeout, auditoría y cero private keys entregadas al agente #owner/agent #type/admin #area/aranea
> - [ ] T3 Seleccionar y validar PostgreSQL MCP con una sola base de desarrollo: perfiles RO/RW, credencial centralizada, límites de query/timeout y convivencia con `psql` nativo #owner/agent #type/admin #area/aranea
> - [ ] T4 Seleccionar y validar MongoDB MCP con una sola base de desarrollo: perfiles RO/RW, `readOnly`/protecciones equivalentes, límites de consulta y convivencia con `mongosh` nativo #owner/agent #type/admin #area/aranea
> - [ ] T5 Seleccionar y validar Temporal MCP: comenzar read-only con allowlist de namespaces; evaluar `signal/start/cancel` sólo después de demostrar la necesidad y el modelo de policy correspondiente #owner/agent #type/admin #area/aranea
> - [ ] T6 Consolidar los cuatro MCP aprobados en el host central, integrar al menos Hermes y Daedalus, demostrar que ambos consumen capabilities sin recibir credenciales reales de los servicios destino, y dejar health checks, logs, rotación/rollback y runbook operativo mínimo #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-10** — SSH MCP expandido a cuatro targets en una sola instancia/puerto: `sqx-zeus`, `sqx-hera`, `sqx-kronos` y `mt5-kronos`. Cursor/Daedalus ejecutó `read-command` sobre los cuatro perfiles y obtuvo las identidades/hostnames esperados. Todos permanecen `viewer` + `readOnly=true`; `run-command` es rechazado por diseño.
- **2026-09-10** — En Hera y Kronos se regeneraron host keys ED25519 únicas porque las VMs clonadas compartían la misma key de Zeus. `mt5-kronos` quedó autenticando por public key con usuario local no-admin `echo-dev`; se corrigió `AuthorizedKeysFile` porque OpenSSH Windows resolvía erróneamente la ruta relativa bajo `C:\\WINDOWS`.
- **2026-09-10** — Primer circuito MCP completo validado: Daedalus resuelve y alcanza `mcps.lab.aranea.cl`, autentica con bearer, inicializa una sesión MCP Streamable HTTP y ejecuta `read-command("whoami")` sobre el target SQX; `ssh-mcp` conecta mediante la private key centralizada y retorna `echo-dev`. La private key SSH nunca se entrega a Daedalus.
- **2026-09-10** — `ssh-mcp` v2.8.0 se construyó desde source pinneado (`v2.8.0`, commit `d2d769684701e0939c1d8e56cbdde3d77fed53ef`) como `local/ssh-mcp:2.8.0-d2d7696`. Smoke test stdio PASS; luego transporte HTTP PASS con health, bearer auth, allowed Host, rate limit y host-key strict.
- **2026-09-08** — Primer acceso SSH real validado para `echo-dev`: `mcps` conecta a `sqx-zeus.lab.aranea.cl` mediante identidad dedicada, trust store dedicado y host-key strict; la sesión remota ejecuta como `echo-dev` en `sqx-ulab-zeus-0`. El usuario remoto no tiene sudo ni grupos adicionales.
- **2026-09-08** — El perfil inicialmente llamado `sqx-dev` se renombra a `echo-dev` porque representa capacidad de desarrollo/diagnóstico de Echo/Echo Forge y no debe quedar acoplado al runtime SQX. La key mantiene la misma fingerprint y cambia su comentario a `echo-dev@mcps`.
- **2026-09-08** — T2 iniciado con `sqx-zeus.lab.aranea.cl` (`192.168.31.101`) como primer target. Host key ED25519 validada local/remotamente y agregada al trust store dedicado. El POC se centra primero en acceso dev/diagnóstico desde agentes Daedalus; `hermes-admin` se implementará después como perfil separado de mayor privilegio.
- **2026-09-08** — DNS de `mcps` corregido: resolver directo Pi-hole `192.168.31.31`, search domain `lab.aranea.cl`. Se comprobó resolución de `daedalus` y `sqx-zeus`.
- **2026-09-07** — T0 cerrado. Se confirmó `mcps` como LXC dedicado con Docker + Portainer, IP actual `192.168.31.219`. El stack PostgreSQL anterior se bajó con `docker compose down`; fueron removidos sus 9 contenedores y la red `postgres_mcp_net`. Verificación posterior: sólo `portainer` permanece activo. Se decide conservar el LXC/Portainer y reconstruir limpio.
- **2026-09-07** — Proyecto creado para materializar incrementalmente el Capability Plane ya definido en [[AGENT-PLATFORM-ARCHITECTURE]]. Scope inicial congelado a SSH, PostgreSQL, MongoDB y Temporal; MinIO, Kafka y observabilidad quedan fuera hasta estabilizar este patrón.

## 🧭 Decisiones

- D1: centralizar credenciales y sesiones MCP en un host dedicado es la dirección preferida; los agentes consumen capabilities y perfiles, no secretos de los servicios destino.
- D2: se conserva el LXC `mcps` y Portainer como baseline operativo; una VM nueva sólo se justifica con evidencia material de aislamiento, mantenimiento, red o disponibilidad insuficientes.
- D3: un host central no implica una identidad omnipotente. Cada MCP/perfil usa credenciales finales separadas y least-privilege.
- D4: mantener clientes nativos (`ssh`, `psql`, `mongosh`, Temporal CLI) donde aporten valor; MCP es la capa reusable para agentes, no una prohibición del acceso nativo.
- D5: la IP `192.168.31.219` es ubicación actual, no identidad estable. Los consumidores usan el access plane por alias/DNS, actualmente `mcps.lab.aranea.cl`.
- D6: SSH es el primer capability a implementar porque desbloquea el mayor gap operativo inmediato para Hermes y Daedalus. Las private keys permanecen en el access plane; los agentes no reciben las credenciales finales.
- D7: identidades SSH separadas por perfil de capacidad. `echo-dev` es la identidad limitada para agentes de desarrollo sobre infraestructura Echo/Echo Forge; `hermes-admin` se diseñará y desplegará aparte, con mayor privilegio sólo donde sea necesario.
- D8: el perfil remoto se prueba primero sin sudo ni grupos adicionales. Los permisos operativos se agregan sólo cuando una necesidad concreta de diagnóstico falle y pueda expresarse con least privilege.
- D9: el acceso remoto de consumidores al SSH MCP usa Streamable HTTP autenticado con bearer sobre DNS estable; el bearer autentica el acceso al capability plane y es independiente de la identidad SSH final mantenida en `mcps`.
- D10: múltiples targets SSH se concentran en una sola instancia/puerto de `ssh-mcp`; la separación se realiza mediante perfiles, no mediante servicios o puertos por máquina.

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
