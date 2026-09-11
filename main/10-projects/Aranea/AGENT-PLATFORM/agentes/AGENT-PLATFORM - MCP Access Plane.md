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
progress: 70
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
updated: "2026-09-11"
---

# AGENT-PLATFORM - MCP Access Plane

> [!info]+ Access plane compartido para agentes
> **Padre:** [[AGENT-PLATFORM-OWNER-PROJECT]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1

## 🎯 Objetivo

- Convertir el host MCP existente de Aranea en un access plane reutilizable para Hermes, Daedalus y agentes futuros, centralizando sesiones, credenciales reales, perfiles de acceso, auditoría y políticas sin repartir secretos de los servicios destino entre máquinas o runtimes.
- Adoptar MCPs existentes antes de construir; modificar o forkear sólo cuando un gap real de seguridad, persistencia o caso de uso quede demostrado.

## 📊 Estado actual

- T0 y T2 cerrados. T1 continúa WIP como contrato transversal; T3 PostgreSQL sigue WIP con POC autenticada de desarrollo ya funcional.
- `mcps` es un LXC dedicado con Docker + Portainer; IP actual `192.168.31.219`, considerada mutable y no parte del contrato estable. `mcps.lab.aranea.cl` es el endpoint estable usado por consumidores.
- SSH MCP operativo en una sola instancia/puerto con cinco perfiles: read-only `sqx-zeus`, `sqx-hera`, `sqx-kronos`, `mt5-kronos`; writable/operator `mt5-kronos-operator`.
- Las host keys ED25519 de todos los targets están pinneadas y validadas. Hera y Kronos regeneraron keys únicas porque las VMs clonadas compartían originalmente la identidad SSH de Zeus.
- La identidad SSH dedicada `echo-dev@mcps`, fingerprint `SHA256:2Qv9f2AREQyse50bGYaTLc1PHK43gvuf3xgv5TTJ+I0`, se mantiene centralizada. La key genérica `mcp-access@mcps` queda fuera del diseño y no debe autorizarse.
- En Linux SQX existe usuario remoto dedicado `echo-dev`, password bloqueado, sin sudo ni grupos extra. En `mt5-kronos` existe usuario local Windows `echo-dev`, no-admin, autenticado por public key.
- `tufantunc/ssh-mcp` v2.8.0 está pinneado a tag `v2.8.0` / commit `d2d769684701e0939c1d8e56cbdde3d77fed53ef`, imagen local `local/ssh-mcp:2.8.0-d2d7696`, ejecutando como usuario no-root.
- Transporte HTTP activo con bearer obligatorio, rate limit, protección de Host y `hostKeyMode=strict`; endpoint estable `http://mcps.lab.aranea.cl:3000/`.
- Cursor/Daedalus consume `aranea-ssh` de forma persistente: bearer cargado automáticamente por el entorno de KDE, sin `export` manual ni lanzamiento de Cursor desde consola.
- Multi-target PASS desde Cursor: `read-command` validado en los cuatro perfiles viewer; `run-command` rechazado por diseño en viewer y validado en `mt5-kronos-operator` como `worker-kronos\\echo-dev`.
- Golden path MT4 PASS vía MCP: transferencia/copia de fuentes, compilación con MetaEditor en `master_test_001`, resolución del mirror de includes bajo el AppData de `echo-dev` y generación de `reference_v3.ex4` con 0 errors / 0 warnings.
- PostgreSQL MCP POC: `crystaldba/postgres-mcp` pinneado a commit `15c8e33353546148acc2d8bd784551cf3905d1e2`, imagen local `local/postgres-mcp:0.3.0-15c8e33`, runtime no-root `999:999`, Streamable HTTP funcional contra `echo-develop` con identidad `mcp_echo_rw`.
- El PostgreSQL MCP no trae bearer auth nativo; se validó un proxy Nginx 1.29.8 pinneado por digest, en red Docker privada, con bearer separado del SSH MCP. Sin token devuelve `401`; con token inicializa MCP, preserva `Mcp-Session-Id` y ejecuta `execute_sql` a través del proxy.
- El camino PostgreSQL validado hasta ahora es RW/dev: discovery de schemas/objetos, `current_user=mcp_echo_rw`, `current_database=echo-develop`, SELECT y permiso DELETE comprobado mediante `EXPLAIN ... WHERE false` sin mutar datos. T3 no se cierra aún: falta perfil RO sobre la misma base de desarrollo, límites/timeout y materializar el despliegue persistente/consumo real sin reemplazar `psql` nativo.
- La skill canónica `xKoRx/symphony/.agents/skills/echo-forge-wfm-troubleshooting/SKILL.md` quedó actualizada con profiles MCP, reglas de transferencia, PowerShell/Windows, golden path MT4 y guards explícitos para impedir servidores HTTP ad-hoc o cambios de ACL no autorizados.
- Hardening genérico no necesario para desbloquear el uso actual — validación explícita de sesiones background, timeout extremo y revisión operativa de audit trail — se difiere a T6, donde se consolidarán health/logs/rotación/rollback y runbook transversal.

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
> - [x] T2 Seleccionar y validar SSH MCP para uso real de agentes: host-key strict, perfiles read/operator, bearer cliente→MCP, least privilege por target, acceso multi-host, transferencia de archivos, ejecución controlada y cero private keys entregadas al agente. Hardening transversal de background/timeout/audit pasa a T6 #owner/agent #type/admin #area/aranea
> - [/] T3 Seleccionar y validar PostgreSQL MCP con una sola base de desarrollo: perfiles RO/RW, credencial centralizada, límites de query/timeout y convivencia con `psql` nativo #owner/agent #type/admin #area/aranea
> - [ ] T4 Seleccionar y validar MongoDB MCP con una sola base de desarrollo: perfiles RO/RW, `readOnly`/protecciones equivalentes, límites de consulta y convivencia con `mongosh` nativo #owner/agent #type/admin #area/aranea
> - [ ] T5 Seleccionar y validar Temporal MCP: comenzar read-only con allowlist de namespaces; evaluar `signal/start/cancel` sólo después de demostrar la necesidad y el modelo de policy correspondiente #owner/agent #type/admin #area/aranea
> - [ ] T6 Consolidar los cuatro MCP aprobados en el host central, integrar al menos Hermes y Daedalus, demostrar que ambos consumen capabilities sin recibir credenciales reales de los servicios destino, y dejar health checks, logs/audit, background/timeout si aportan valor, rotación/rollback y runbook operativo mínimo #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-11** — PostgreSQL MCP POC autenticada PASS en `mcps`: source `crystaldba/postgres-mcp` pinneado a `15c8e33353546148acc2d8bd784551cf3905d1e2`, imagen local no-root `local/postgres-mcp:0.3.0-15c8e33`, Streamable HTTP conectado como `mcp_echo_rw` a `echo-develop`. Discovery, sesión MCP y RW se validaron sin mutación real. Como el upstream no aporta bearer auth, se validó Nginx 1.29.8 pinneado por digest como proxy en red privada: `401` sin bearer y `200 + Mcp-Session-Id + tools/call` con bearer dedicado. T3 permanece WIP hasta completar RO sobre la misma DB de desarrollo, límites/timeout y despliegue persistente/consumo real.
- **2026-09-10** — T2 SSH MCP cerrado para uso real de agentes. Se validó `mt5-kronos-operator` con `run-command` como usuario Windows no-admin y el golden path MT4 `upload/copy → compile` sobre `master_test_001`; `reference_v3.mq4` compiló a `.ex4` con 0 errors / 0 warnings. La resolución de `#include` de MetaEditor ejecutado como `echo-dev` usa el AppData de ese usuario y requiere mirror del mismo hash de terminal. La skill Echo Forge WFM Troubleshooting documenta este contrato y prohíbe servidores HTTP ad-hoc para mover texto cuando `sftp-upload` es suficiente.
- **2026-09-10** — Cursor/Daedalus quedó con autoload persistente de `ARANEA_SSH_MCP_BEARER` mediante entorno de usuario/KDE; `aranea-ssh` conecta verde al abrir Cursor normalmente, sin launcher de consola.
- **2026-09-10** — SSH MCP expandido a cuatro targets read-only en una sola instancia/puerto: `sqx-zeus`, `sqx-hera`, `sqx-kronos` y `mt5-kronos`; se añadió `mt5-kronos-operator` para mutación/ejecución controlada.
- **2026-09-10** — En Hera y Kronos se regeneraron host keys ED25519 únicas porque las VMs clonadas compartían la misma key de Zeus. `mt5-kronos` quedó autenticando por public key con usuario local no-admin `echo-dev`; se corrigió `AuthorizedKeysFile` porque OpenSSH Windows resolvía la ruta relativa bajo `C:\\WINDOWS`.
- **2026-09-10** — Primer circuito MCP completo validado: Daedalus resuelve y alcanza `mcps.lab.aranea.cl`, autentica con bearer, inicializa MCP Streamable HTTP y ejecuta `read-command("whoami")`; la private key SSH nunca se entrega a Daedalus.
- **2026-09-10** — `ssh-mcp` v2.8.0 se construyó desde source pinneado (`v2.8.0`, commit `d2d769684701e0939c1d8e56cbdde3d77fed53ef`) como `local/ssh-mcp:2.8.0-d2d7696`. Smoke test stdio PASS; transporte HTTP PASS con health, bearer auth, allowed Host, rate limit y host-key strict.
- **2026-09-08** — Primer acceso SSH real validado para `echo-dev`: `mcps` conecta a `sqx-zeus.lab.aranea.cl` mediante identidad dedicada, trust store dedicado y host-key strict; la sesión remota ejecuta como `echo-dev` en `sqx-ulab-zeus-0`.
- **2026-09-08** — El perfil inicialmente llamado `sqx-dev` se renombra a `echo-dev` porque representa capacidad de desarrollo/diagnóstico de Echo/Echo Forge y no debe quedar acoplado al runtime SQX.
- **2026-09-08** — T2 iniciado con `sqx-zeus.lab.aranea.cl` (`192.168.31.101`) como primer target. Host key ED25519 validada local/remotamente y agregada al trust store dedicado.
- **2026-09-08** — DNS de `mcps` corregido: resolver directo Pi-hole `192.168.31.31`, search domain `lab.aranea.cl`.
- **2026-09-07** — T0 cerrado. Se confirmó `mcps` como LXC dedicado con Docker + Portainer, IP actual `192.168.31.219`. El stack PostgreSQL anterior se bajó con `docker compose down`; fueron removidos sus 9 contenedores y la red `postgres_mcp_net`. Verificación posterior: sólo `portainer` permanecía activo.
- **2026-09-07** — Proyecto creado para materializar incrementalmente el Capability Plane ya definido en [[AGENT-PLATFORM-ARCHITECTURE]]. Scope inicial congelado a SSH, PostgreSQL, MongoDB y Temporal; MinIO, Kafka y observabilidad quedan fuera hasta estabilizar este patrón.

## 🧭 Decisiones

- D1: centralizar credenciales y sesiones MCP en un host dedicado; los agentes consumen capabilities y perfiles, no secretos de los servicios destino.
- D2: se conserva el LXC `mcps` y Portainer como baseline operativo; una VM nueva sólo se justifica con evidencia material.
- D3: un host central no implica una identidad omnipotente. Cada MCP/perfil usa credenciales finales separadas y least-privilege.
- D4: mantener clientes nativos (`ssh`, `psql`, `mongosh`, Temporal CLI`) donde aporten valor; MCP es la capa reusable para agentes.
- D5: la IP `192.168.31.219` es ubicación actual, no identidad estable. Consumidores usan DNS `mcps.lab.aranea.cl`.
- D6: las private keys SSH permanecen en el access plane; los agentes no reciben las credenciales finales.
- D7: `echo-dev` es identidad limitada para desarrollo/diagnóstico Echo/Echo Forge; perfiles de mayor privilegio se diseñan aparte y sólo cuando existe necesidad demostrada.
- D8: permisos remotos se agregan sólo cuando una necesidad concreta falle y pueda expresarse con least privilege; no ampliar ACLs preventivamente.
- D9: consumidores acceden al SSH MCP mediante Streamable HTTP autenticado con bearer; el bearer es independiente de la identidad SSH final.
- D10: múltiples targets SSH se concentran en una sola instancia/puerto de `ssh-mcp`; la separación se realiza mediante perfiles.
- D11: para archivos de texto/código hacia targets SSH se usa `sftp-upload`; no se levantan servidores HTTP temporales ad-hoc. Binarios/grandes deben usar staging autorizado.
- D12: T2 se considera cerrado cuando el camino real de agentes queda validado con perfiles RO/operator, strict host keys, auth MCP, least privilege, transferencia y ejecución. Hardening transversal no bloqueante (background/timeout/audit operacional) se concentra en T6 para evitar sobrediseñar cada capability.
- D13: PostgreSQL MCP se adopta desde `crystaldba/postgres-mcp` pinneado por commit e imagen local; las credenciales DB permanecen sólo en `mcps` y el runtime usa identidad PostgreSQL dedicada least-privilege.
- D14: como PostgreSQL MCP no ofrece bearer auth nativo, el endpoint remoto se protege mediante proxy Nginx pinneado, bearer dedicado y red Docker privada; el backend MCP no se publica directamente a consumidores.

## 🔗 Docs / Links

- [[AGENT-PLATFORM-ARCHITECTURE]] — arquitectura v1 y definición del Capability Plane.
- [[AGENT-PLATFORM-OWNER-PROJECT]] — cockpit humano padre.
- `xKoRx/symphony/.agents/skills/echo-forge-wfm-troubleshooting/SKILL.md` — contrato operativo Echo Forge para acceso remoto SQX/MT4/MT5 por MCP.

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
