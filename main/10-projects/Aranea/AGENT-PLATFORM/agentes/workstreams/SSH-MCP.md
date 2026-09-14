---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-13"
updated: "2026-09-13"
tags:
  - area/aranea
  - tech/mcp
  - tech/ssh
---

# SSH MCP — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]]. **No es un proyecto paralelo.**
>
> Estado vigente certificado el 2026-09-13. Ante conflicto con entradas históricas del proyecto, la autoridad agent-facing es [[aranea-mcps-expert]] y el procedimiento canónico es [[aranea-ssh-mcp]].

## Objetivo

Dar a los agentes acceso SSH centralizado a hosts Aranea sin entregar private keys ni credenciales finales, separando identidad remota, autoridad MCP y privilegio real del sistema operativo.

## Estado certificado

```text
aranea-ssh endpoint           http://mcps.lab.aranea.cl:3000/
ssh-mcp                       v2.8.0 / healthy
sqx-zeus                      operator / writable / echo-dev / non-root
sqx-hera                      operator / writable / echo-dev / non-root
sqx-kronos                    operator / writable / echo-dev / non-root
mt5-kronos                    viewer / read-only / echo-dev
mt5-kronos-operator           operator / writable / echo-dev
 docker-echo-dev-operator      operator / writable / root / DEV-only
```

Los tres profiles SQX fueron promovidos el 2026-09-13 desde `viewer/readOnly=true` a `operator/readOnly=false`. Host, puerto, identidad `echo-dev`, key, host-key pinning, TTY y timeout no cambiaron.

## Cómo deben usarlo los agentes

- Para inspección, incluso en SQX operator, preferir `read-command`.
- Para escritura/ejecución necesaria usar `run-command` con profile exacto y target acotado.
- Para archivos pequeños usar `sftp-upload` / `sftp-download`; no inventar side channels.
- Usar sesiones interactivas/background sólo si el estado persistente o proceso largo aporta valor; cerrarlas al terminar.
- `signal-process` requiere PID identificado.
- `privileged-command` no crea privilegios: sólo sirve si la identidad remota tiene sudo/admin y la tarea autoriza esa elevación.
- `operator` describe la superficie MCP, no significa `root`.
- `approvalPolicy="auto"` no equivale a human-in-the-loop. Antes de toda mutación: target exacto, blast radius, rollback/post-condición y verificación posterior.

## Tool surface certificada

```text
list-connections
list-sessions
open-session
close-session
read-session-output
read-command
run-command
privileged-command
signal-process
sftp-upload
sftp-download
```

## Certificación E2E 2026-09-13

Se validó el camino MCP real, no SSH directo:

```text
initialize                 PASS / protocol 2025-03-26
notifications/initialized  PASS / 202 Accepted
tools/list                 PASS
sqx-zeus                   write -> read -> delete PASS / CLEAN
sqx-hera                   write -> read -> delete PASS / CLEAN
sqx-kronos                 write -> read -> delete PASS / CLEAN
```

Probe reversible usado: `/tmp/aranea-mcp-write-smoke`, eliminado en los tres hosts.

## Boundaries

- SQX opera como `echo-dev`, actualmente sin sudo ni grupos extra: writable dentro de sus permisos, no root-equivalent.
- `mt5-kronos` sigue read-only; usar `mt5-kronos-operator` sólo cuando se necesite mutación.
- `docker-echo-dev-operator` sí es root-equivalent, pero sólo para ese host DEV.
- No usar esta capability para MELI/corporativo.
- No ampliar ACLs ni privilegios como workaround automático.

## Autoridad

Routing y selección de capability: [[aranea-mcps-expert]].

Procedimiento, recovery, tool semantics y smokes: [[aranea-ssh-mcp]].