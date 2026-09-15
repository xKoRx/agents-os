---
type: skill
schema_version: 1
name: aranea-mcp-plane-operator
description: >-
  Opera el Access Plane MCP de Aranea (LXC `mcps`) por management path nativo
  (`mcps-ops`): discovery, baseline, backup mínimo, restart/redeploy/repair de
  una capability DEV, server smoke, consumer smoke, rollback y update del
  source of truth. Cargar al reparar/reiniciar/auditar una capability MCP o al
  operar el appliance `mcps`. No es para elegir capability como consumidor
  (usar [[aranea-mcps-expert]]) ni para onboardar consumers (usar
  [[mcp-access-plane-operations]] / runbook capability-plane).
scope: area
created: "2026-09-15"
updated: "2026-09-15"
entities:
  - "[[Aranea]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
aliases:
  - aranea-mcp-plane-operator
  - mcp plane operator
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - tech/mcp
  - tech/agents-os
  - action/mcp-plane-operations
---

# aranea-mcp-plane-operator

## Purpose

Reparar, reiniciar, reconfigurar y verificar capabilities del Access Plane MCP de Aranea operando el LXC `mcps` por su management path nativo — nunca a través de un MCP servido por `mcps` — dejando evidencia, rollback y source of truth actualizado.

Trigger: una capability MCP está caída/degradada, hay que aplicar un restart/redeploy controlado, hay que auditar drift del runtime del plane, o hay que demostrar repair end-to-end.

No trigger: elegir capability/ambiente como consumidor ([[aranea-mcps-expert]]), onboardar un consumer nuevo ([[mcp-access-plane-operations]]), diseñar el deployment de una capability nueva ([[AGENT-PLATFORM - MCP Access Plane - Architecture]]).

## Minimal Read

Read only:
1. `[[AGENT-PLATFORM - MCP Access Plane - Architecture]]` — topología, boundaries, inventario de puertos y Gate D de certificación.
2. El runbook de la familia de la capability objetivo (`30-resources/runbooks/aranea-<familia>-mcp.md`).
3. `[[mcp-access-plane-operations]]` (Hermes skill) sólo para mecánica del management path (scp vs heredoc, sudo/find, bearer-by-reference).

## Procedure

1. **Fijar target y clase.** Capability exacta (container backend + proxy), ambiente (DEV/PROD) y autoridad vigente. PROD queda read-only salvo gate explícito del owner; DEV restart/redeploy/repair es AUTO.
2. **Baseline antes de tocar.** Registrar por `mcps-ops`: `docker inspect` (image digest, restart policy, mounts, port bindings), sha256 del template de proxy en `/opt/mcp/<familia>/runtime/proxy/`, `ss -lntp` del puerto, y un server smoke autenticado PASS. Sin baseline no hay repair.
3. **Backup mínimo.** Copiar a `/tmp` en `mcps` (o leer y retener hashes) los archivos de config que la intervención pueda tocar. Un restart no cambia config; un redeploy/config-change exige copia previa + sha.
4. **Intervención controlada.** En orden creciente de blast radius: `docker restart <backend>` → `docker restart <proxy>` → recreate del container con los mismos mounts/imagen pinneada. Nunca rebuild que pierda pin/patch de la imagen certificada. Un solo container por paso; nada de operaciones masivas.
5. **Runtime health.** `docker ps` status + unauth request → 401 esperado en el proxy.
6. **Server smoke.** Desde `mcps` vía `mcps-ops`: initialize (con `clientInfo.version`) → `tools/list` → tools/call inocuo; bearer entra por stdin, jamás por argv/env persistido/chat. Script de smoke se sube por scp, no heredoc.
7. **Consumer smoke.** Desde un consumer real (Daedalus via `daedalus-ops`): resolver la entry real de `mcp.json` con su ref `${env:VAR}`, bearer por stdin, initialize/tools/list/tools/call. PASS sólo con el MCP client shape real del consumer.
8. **Post-condición y drift cero.** Comparar contra baseline: image digests, mounts, port bindings, template sha. Cualquier delta no intencional → revertir inmediatamente con el backup.
9. **Rollback path.** Config: restaurar backup (sha byte-identical) + restart del container afectado + re-smoke. Runtime: `docker stop/start` o recreate con los parámetros del baseline. El rollback se documenta aunque no se ejecute; se ejecuta y re-verifica cuando la post-condición falla.
10. **Source of truth.** Si el estado vigente cambió (puerto, imagen, tool surface, naming), actualizar la nota de arquitectura y/o el runbook de familia; si no cambió nada, no tocar canon. Registrar el cambio en `change_log` cuando altera archivos canónicos.

## Output

```text
Capability:      <aranea-*  ambiente  containers backend+proxy>
Baseline:        <digests + template sha + smoke PASS | FAIL — abortado si FAIL>
Intervention:    <restart | recreate | config-change + archivo tocado>
Server smoke:    PASS | FAIL — <serverInfo + tools count>
Consumer smoke:  PASS | FAIL — <consumer + entry + tools count>
Post-condition:  drift cero | delta intencional <detalle> | delta NO intencional <revertido>
Rollback:        <path documentado | ejecutado + resultado>
SoT update:      <nota/runbook actualizado | none>
```

## Hard Rules

- Administración de `mcps` sólo por `mcps-ops` (SSH nativo); nunca a través de un MCP servido por `mcps`.
- PROD: read-only; cualquier intervención PROD es GATED (owner). DEV restart/redeploy/repair es AUTO según SOUL.md §8.1.
- Nada de secretos por argv, env persistido, chat o vault: bearer/credenciales por stdin o archivo 0600; verificar presencia, nunca el valor.
- Prohibido rebuild que pierda el pin/patch de imagen certificada; recreate exige los mismos mounts/policy/ports del baseline.
- Scripts con `${...}`/regex van por scp/base64-file, nunca heredoc-through-ssh.
- Sin baseline previo no se interviene; sin server smoke no se declara repair.
- No introducir topología nueva ni Compose: la arquitectura canónica manda; desviación requiere decisión explícita en la nota de arquitectura.
- La evidencia runtime vigente (`tools/list`, health, mounts, digests reales) vence cualquier documentación histórica; ante contradicción, re-clasificar el estado antes de intervenir.
- Toda boundary de seguridad se certifica con probe positivo **y** negativo (auth vs unauth → 401, tool esperada vs tool rechazada/ausente); la prueba positiva sola no certifica.
- Todo cambio reusable exige rollback evidence (restauración probada o path documentado con verificación) y post-condición de drift cero: cualquier delta no intencional se revierte inmediatamente.
- Delegar procedimientos por familia a los runbooks; esta skill no duplica endpoints ni inventarios.
