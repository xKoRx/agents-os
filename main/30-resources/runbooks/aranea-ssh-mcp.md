---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-13"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-flink-mcp]]"
  - "[[echo-forge-workers-shared-access]]"
aliases:
  - runbook SSH MCP Aranea
  - aranea-ssh
  - mcp ssh
  - docker-echo-dev-operator
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
  - tech/ssh
  - action/mcp-ssh
---

# aranea-ssh-mcp

## Propósito

Ejecutar inspección y operación remota sobre workers/hosts autorizados de Aranea mediante la capability canónica `aranea-ssh`. Este runbook posee hechos operativos de SSH MCP. La selección de capability y autoridad mínima pertenece a [[aranea-mcps-expert]]. Las skills/runbooks de dominio deciden cuándo se necesita evidencia o mutación de host/runtime.

## Precondiciones

- El target es infraestructura Aranea; si es MELI/corporativo, abortar y no usar este runbook.
- `aranea-mcps-expert` ya eligió `aranea-ssh` y el perfil mínimo.
- La capability `aranea-ssh` aparece conectada en el cliente.
- Las credenciales/keys SSH finales permanecen en `mcps`; el agente no las pide, imprime, copia ni persiste.
- Este camino MCP no se sustituye por [[echo-forge-workers-shared-access]] mientras `aranea-ssh` cubra la acción.

## Procedimiento

1. **Fijar perfil y autoridad.** Elegir el profile que corresponde al host real. `operator` habilita operaciones mutables en el MCP, pero **no convierte al usuario remoto en root**: la autoridad efectiva sigue limitada por el usuario SSH y sus permisos del sistema operativo. No invocar operaciones privileged/admin ni alterar ACLs salvo autorización explícita de esa acción administrativa exacta.

| Profile | Target | Remote identity | Authority | Uso normal |
|---|---|---|---|---|
| `sqx-zeus` | Linux SQX Zeus | `echo-dev` | operator / writable | procesos, logs, archivos, ejecución y mutaciones necesarias del runtime SQX dentro de permisos `echo-dev` |
| `sqx-hera` | Linux SQX Hera | `echo-dev` | operator / writable | procesos, logs, archivos, ejecución y mutaciones necesarias del runtime SQX dentro de permisos `echo-dev` |
| `sqx-kronos` | Linux SQX Kronos | `echo-dev` | operator / writable | procesos, logs, archivos, ejecución y mutaciones necesarias del runtime SQX dentro de permisos `echo-dev` |
| `mt5-kronos` | Windows worker-kronos | `echo-dev` | viewer / read-only | inspección MT4/MT5, procesos, logs, paths |
| `mt5-kronos-operator` | Windows worker-kronos | `echo-dev` | operator / writable | upload, compile y ejecución explícitamente autorizados |
| `docker-echo-dev-operator` | Linux `docker-echo-dev` / `192.168.31.75` | `root` | operator / writable / root | config/filesystem, Docker/Compose, logs, exec y lifecycle DEV |

2. **Elegir el tool por intención, no por comodidad.** La superficie certificada de `ssh-mcp` v2.8.0 incluye:

| Intención | Tool | Regla |
|---|---|---|
| descubrir perfiles/conexiones | `list-connections` | read-only; usar para confirmar profile/estado |
| lectura puntual | `read-command` | preferido para `ls`, `cat`, `grep`, `find`, `stat`, `df` y demás allowlist de lectura |
| comando que puede mutar | `run-command` | usar sólo con profile operator y target/scope explícitos |
| sesión shell stateful | `open-session` + `run-command` con `session` | sólo cuando CWD/env persistente aporta valor; cerrar con `close-session` |
| proceso largo/background | `open-session` tipo `background` + `read-session-output` | cerrar la sesión al terminar; `signal-process` sólo sobre PID identificado |
| transferencia de archivo | `sftp-upload` / `sftp-download` | upload es escritura; download es lectura |
| elevación sudo | `privileged-command` | sólo si la tarea requiere sudo y el usuario remoto realmente tiene esa autoridad |

`approvalPolicy = "auto"` significa que un profile operator **no garantiza un prompt humano** antes de un comando que el servidor clasifique como write/destructive/privileged. El agente debe aplicar el gate antes de invocar: target exacto, blast radius, rollback/post-condición cuando haya mutación y verificación posterior. No usar el approval gate del servidor como sustituto del razonamiento de seguridad.

3. **Usar el endpoint canónico.** MCP: `aranea-ssh`. Endpoint: `http://mcps.lab.aranea.cl:3000/`. No inferir otro puerto, host o transporte si este runbook está disponible.
4. **Reducir lecturas al tool de lectura.** Aunque `sqx-*` ahora sean operator, las inspecciones normales deben seguir usando `read-command`; no usar `run-command` para una lectura sólo porque el profile lo permite. Las policies de lectura pueden rechazar comandos compuestos, pipelines o constructos de shell; si ocurre, reducir a una sola operación allowlisted o partir la evidencia en llamadas separadas.
5. **Transferir archivos por el canal autorizado.** Para texto/código/config pequeños (`.mq4`, `.mqh`, `.mq5`, `.txt`, `.json`, `.ini`, scripts) usar `sftp-upload` / `sftp-download` a través de `aranea-ssh`. No crear servidores HTTP temporales, listeners netcat ni otros side channels. Para artefactos grandes/binarios, preferir el staging autorizado. Si no existe path autorizado, detener y reportar el blocker.
6. **Respetar semántica Windows.** `mt5-kronos-operator` está validado con identidad `worker-kronos\echo-dev`, hostname `worker-kronos` y home efectivo `C:\Users\echo-dev.WORKER-KRONOS`. El shell remoto es PowerShell: no asumir POSIX ni usar `&&` como separador genérico; usar sintaxis compatible como `;` cuando corresponda.
7. **Aplicar el hecho conocido de includes MT4.** En `master_test_001`, compilar un EA como `echo-dev` puede resolver `#include <...>` globales desde el árbol AppData de `echo-dev` aunque el `.mq4` principal viva en el árbol del terminal KoR. Mirror validado: `C:\Users\echo-dev.WORKER-KRONOS\AppData\Roaming\MetaQuotes\Terminal\8819D02A34F64665EDC6BEA4A390310C\MQL4\Include\`. Si MetaEditor emite una cascada `can't open include`, verificar este mirror antes de cambiar lógica del EA o ampliar ACLs.
8. **Tratar `docker-echo-dev-operator` como root-equivalent.** El profile entra como `root@192.168.31.75` con key dedicada y `readOnly=false`. Está autorizado para el host DEV completo, pero no es permiso genérico sobre otros hosts ni PROD. Para Flink/StateFun, seguir [[aranea-flink-mcp]]: control plane por `aranea-flink-dev-admin`; filesystem/Docker/lifecycle por este profile.
9. **No inventar source-of-truth de Compose.** En `docker-echo-dev`, el stack Flink vive en Portainer stack `1`; `/data/compose/1/docker-compose.yml` es path interno de Portainer y corresponde en el host a `/var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml`. No crear otra definición paralela ni ejecutar lifecycle rutinario desde un compose reconstruido.
10. **Tratar fallos como boundary.** `POLICY_DENIED` → revisar profile/tool/scope; no escalar automáticamente. `Access Denied` en un path → registrar path exacto y operación requerida; no mutar ACLs automáticamente. Error de sintaxis Windows → verificar PowerShell antes de diagnosticar la aplicación destino. Elevación requerida pero el usuario remoto no tiene sudo/admin → detener y reportar boundary. Transferencia imposible por SFTP/staging → detener; no inventar side channel.

## Certificación

### SQX operators — 2026-09-13

Los profiles `sqx-zeus`, `sqx-hera` y `sqx-kronos` fueron promovidos desde `viewer/readOnly=true` a `operator/readOnly=false`, conservando host, puerto, usuario `echo-dev`, key, host-key pinning, `tty=false`, timeout y `approvalPolicy="auto"`.

Se reinició únicamente `ssh-mcp`; el container volvió `running/healthy` y `GET /status` autenticado reportó los tres profiles como `role=operator`, `readOnly=false`.

Certificación E2E por MCP Streamable HTTP, no por SSH directo:

```text
initialize -> protocolVersion 2025-03-26
notifications/initialized -> 202 Accepted
tools/list -> PASS
sqx-zeus   -> run-command create /tmp probe -> read-command verify -> rm -> PASS/CLEAN
sqx-hera   -> run-command create /tmp probe -> read-command verify -> rm -> PASS/CLEAN
sqx-kronos -> run-command create /tmp probe -> read-command verify -> rm -> PASS/CLEAN
```

El probe fue `/tmp/aranea-mcp-write-smoke` con contenido `aranea-mcp-write-smoke`; quedó eliminado en los tres hosts. Esta certificación prueba el circuito `agent/client → HTTP MCP → operator profile → SSH → filesystem remoto`.

Boundary operativo: estos tres profiles siguen entrando como `echo-dev`; no son root-equivalent. `privileged-command` sólo es útil si el usuario remoto posee sudo y la acción está autorizada. `approvalPolicy="auto"` permanece vigente y debe tratarse como capacidad de auto-ejecución, no como human-in-the-loop.

### worker-kronos operator — 2026-09-11

Se verificó end-to-end `run-command` con el perfil operator autorizado sobre `worker-kronos` y la identidad `worker-kronos\echo-dev`. También se verificaron `sftp-upload` y `sftp-download` con un probe reversible en `C:/Windows/Temp`, incluyendo eliminación posterior.

El perfil `mt5-kronos` sigue siendo viewer/read-only; para mutaciones usar únicamente `mt5-kronos-operator` cuando la tarea las requiera.

### docker-echo-dev operator — 2026-09-13

Profile certificado:

```text
name:      docker-echo-dev-operator
target:    root@192.168.31.75
authority: operator / writable / root
key:       dedicada al profile
host key:  strict / fingerprint pinneado
```

Certificación E2E a través de `aranea-ssh` / `run-command`:

```text
host=docker-echo-dev
user=root
Docker client/server=29.1.3
Docker Compose=v5.0.1
statefun-master=running
statefun-worker=running
isError=false
```

La key privada queda montada read-only dentro de `ssh-mcp`; no se comparte con Daedalus/Cursor ni se reutiliza para SQX/MT5.

## Validación

```text
Capability:          aranea-ssh
Profile:             <profile exacto>
Remote identity:     <usuario efectivo>
Authority match:     PASS
Target:              <host/profile>
Operation:           <read-command|run-command|sftp-*|session|privileged-command justificado>
Mutation:            none | target + rollback/post-condition + verification
Boundary:            none | POLICY_DENIED/Access Denied registrado sin bypass
Secrets:             none persisted
```

Para `sqx-zeus`, `sqx-hera` y `sqx-kronos`, además:

```text
Remote identity:      echo-dev
Authority:            operator / writable
Root-equivalent:      no
Preferred read tool:  read-command
Write tool:           run-command / sftp-upload según intención
Approval policy:      auto; no asumir prompt humano
```

Para `docker-echo-dev-operator`, además:

```text
Target host:          192.168.31.75
Remote identity:      root
Root-equivalent:      yes / intentional DEV boundary
Domain runbook:       aranea-flink-mcp cuando la tarea es Flink/StateFun
PROD authority:       none
```

## Rollback / recuperación

Abortar sin mutar cuando el cliente no tiene `aranea-ssh`, el profile/tool no cubre la acción, la transferencia no cabe en SFTP/staging o el único workaround sería publicar puertos/alterar ACLs. Ante fallo, conservar evidencia de boundary, no rotar secretos preventivamente y handoff a [[aranea-mcp-capability-plane]] si el problema es el plano MCP.

Para revertir específicamente la promoción SQX si aparece un problema de policy, volver cada profile `sqx-zeus`, `sqx-hera`, `sqx-kronos` a `role="viewer"` + `readOnly=true`, reiniciar sólo `ssh-mcp` y revalidar `/status` + `read-command`; usar el backup runtime creado antes del cambio si se necesita restauración exacta.

Para `docker-echo-dev-operator`, no asumir que un `docker compose up -d` es reversible o no disruptivo: seguir el runbook de dominio, preparar rollback y verificar el servicio después de cualquier lifecycle mutation.

## Evidencia

Reportar profile, target host, identidad remota, tool/operación ejecutada, output/file path relevante, si hubo mutación y cualquier boundary de policy/ACL. Para operators root-equivalent o acciones privileged, incluir rollback/post-condición cuando exista mutación.