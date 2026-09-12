---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[Echo Forge]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[echo-forge-workers-shared-access]]"
aliases:
  - runbook SSH MCP Aranea
  - aranea-ssh
  - mcp ssh
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

Ejecutar inspección y operación remota sobre workers autorizados de Aranea mediante la capability canónica `aranea-ssh`. Este runbook posee hechos operativos de SSH MCP. La selección de capability y autoridad mínima pertenece a [[aranea-mcps-expert]]. Las skills de dominio deciden cuándo se necesita evidencia de host/runtime.

## Precondiciones

- El target es infraestructura Aranea; si es MELI/corporativo, abortar y no usar este runbook.
- `aranea-mcps-expert` ya eligió `aranea-ssh` y el perfil mínimo.
- La capability `aranea-ssh` aparece conectada en el cliente.
- Las credenciales/keys SSH finales permanecen en `mcps`; el agente no las pide, imprime, copia ni persiste.
- Este camino MCP no se sustituye por [[echo-forge-workers-shared-access]] mientras `aranea-ssh` cubra la acción.

## Procedimiento

1. **Fijar perfil y autoridad.** Default: perfil `viewer` y `read-command`. No usar `run-command` contra perfiles viewer. Usar `mt5-kronos-operator` sólo cuando la tarea exija escribir, compilar o ejecutar. No invocar operaciones privileged/admin ni alterar ACLs salvo autorización explícita de esa acción administrativa exacta.

| Profile | Target | Authority | Uso normal |
|---|---|---|---|
| `sqx-zeus` | Linux SQX Zeus | viewer / read-only | procesos, logs, archivos, evidencia de runtime |
| `sqx-hera` | Linux SQX Hera | viewer / read-only | procesos, logs, archivos, evidencia de runtime |
| `sqx-kronos` | Linux SQX Kronos | viewer / read-only | procesos, logs, archivos, evidencia de runtime |
| `mt5-kronos` | Windows worker-kronos | viewer / read-only | inspección MT4/MT5, procesos, logs, paths |
| `mt5-kronos-operator` | Windows worker-kronos | operator / writable | upload, compile y ejecución explícitamente autorizados |

2. **Usar el endpoint canónico.** MCP: `aranea-ssh`. Endpoint: `http://mcps.lab.aranea.cl:3000/`. No inferir otro puerto, host o transporte si este runbook está disponible.
3. **Reducir lecturas viewer al allowlist.** Las policies viewer pueden rechazar comandos compuestos, pipelines o constructos de shell aunque cada pieza sea inofensiva por separado. Si un diagnóstico es denegado: reducir a una sola operación de lectura allowlisted; partir lecturas compuestas en llamadas separadas; no cambiar a un perfil writable sólo para facilitar el diagnóstico; reportar `POLICY_DENIED` si la evidencia no cabe en autoridad viewer.
4. **Transferir archivos por el canal autorizado.** Para texto/código/config pequeños (`.mq4`, `.mqh`, `.mq5`, `.txt`, `.json`, `.ini`, scripts) usar `sftp-upload` / `sftp-download` a través de `aranea-ssh`. No crear servidores HTTP temporales, listeners netcat ni otros side channels. Para artefactos grandes/binarios, preferir el staging autorizado. Si no existe path autorizado, detener y reportar el blocker.
5. **Respetar semántica Windows.** `mt5-kronos-operator` está validado con identidad `worker-kronos\echo-dev`, hostname `worker-kronos` y home efectivo `C:\Users\echo-dev.WORKER-KRONOS`. El shell remoto es PowerShell: no asumir POSIX ni usar `&&` como separador genérico; usar sintaxis compatible como `;` cuando corresponda.
6. **Aplicar el hecho conocido de includes MT4.** En `master_test_001`, compilar un EA como `echo-dev` puede resolver `#include <...>` globales desde el árbol AppData de `echo-dev` aunque el `.mq4` principal viva en el árbol del terminal KoR. Mirror validado: `C:\Users\echo-dev.WORKER-KRONOS\AppData\Roaming\MetaQuotes\Terminal\8819D02A34F64665EDC6BEA4A390310C\MQL4\Include\`. Si MetaEditor emite una cascada `can't open include`, verificar este mirror antes de cambiar lógica del EA o ampliar ACLs.
7. **Tratar fallos como boundary.** `POLICY_DENIED` → reducir/partir la lectura; no escalar automáticamente. `Access Denied` en un path → registrar path exacto y operación requerida; no mutar ACLs automáticamente. Error de sintaxis Windows → verificar PowerShell antes de diagnosticar la aplicación destino. Acción writable requerida con sólo viewer disponible → detener y reportar operator. Transferencia imposible por SFTP/staging → detener; no inventar side channel.

## Certificación 2026-09-11

Se verificó end-to-end `run-command` con el perfil operator autorizado sobre `worker-kronos` y la identidad `worker-kronos\echo-dev`. También se verificaron `sftp-upload` y `sftp-download` con un probe reversible en `C:/Windows/Temp`, incluyendo eliminación posterior. Un intento de `run-command` contra el perfil viewer `sqx-zeus` devolvió `POLICY_DENIED: Profile "sqx-zeus" is read-only, so "safe" commands are refused.`; este rechazo es comportamiento esperado y confirma el boundary, no un fallo del MCP.

## Validación

```text
Capability:          aranea-ssh
Profile:             <viewer o operator justificado>
Authority match:     PASS
Target:              <host/profile>
Operation:           <read-command|sftp-*|run-command justificado>
Mutation:            none | target + post-condition + verification
Boundary:            none | POLICY_DENIED/Access Denied registrado sin bypass
Secrets:             none persisted
```

## Rollback / recuperación

Abortar sin mutar cuando el cliente no tiene `aranea-ssh`, la policy viewer rechaza la evidencia y no hay autorización operator, la transferencia no cabe en SFTP/staging o el único workaround sería publicar puertos/alterar ACLs. Ante fallo, conservar evidencia de boundary, no rotar secretos preventivamente y handoff a [[aranea-mcp-capability-plane]] si el problema es el plano MCP.

## Evidencia

Reportar profile, target host, operación ejecutada, output/file path relevante, si hubo mutación y cualquier boundary de policy/ACL.
