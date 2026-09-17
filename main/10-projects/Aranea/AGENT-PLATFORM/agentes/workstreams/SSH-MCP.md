---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-13"
updated: "2026-09-17"
aliases:
  - "SSH MCP — workstream del MCP Access Plane"
tags:
  - area/aranea
  - tech/mcp
  - tech/ssh
---

# SSH MCP — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]], no proyecto paralelo. Estado SSH y publisher Windows reconciliado 2026-09-17. Autoridad agent-facing: [[aranea-mcps-expert]]; procedimiento/evidencia detallada: [[aranea-ssh-mcp]]. Inventario transversal: [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

## Objetivo

Acceso SSH centralizado de agentes Aranea sin compartir private keys ni credenciales upstream. Separar autoridad del profile MCP, identidad remota y permisos OS. Para evidencia privilegiada Windows se publica un JSON acotado desde SYSTEM; NO se eleva `echo-dev`.

## Estado certificado

```text
aranea-ssh                    http://mcps.lab.aranea.cl:3000/; ssh-mcp v2.8.0 + H2
sqx-zeus                      operator / writable / echo-dev / non-root
sqx-hera                      operator / writable / echo-dev / non-root
sqx-kronos                    operator / writable / echo-dev / non-root
mt5-kronos                    viewer / read-only / echo-dev
mt5-kronos-operator           operator / writable / echo-dev / non-admin
docker-echo-dev-operator      operator / writable / root / DEV-only
echo-runtime-prod             viewer / read-only / echo-dev / non-root
Windows evidence publisher    ACTIVE/CERTIFIED 2026-09-17; owner seed completed
```

Los profiles SQX fueron promovidos el 2026-09-13 sin cambiar identidad ni host-key pinning. `echo-runtime-prod` certificado desde 2026-09-15: observación sí, control/restart PROD no. Scope limitado al host/identidad de cada profile.

## Windows: camino agent-facing certificado

```text
AraneaEvidencePublish (Task Scheduler, SYSTEM, cada 5 min)
  -> C:\ProgramData\Aranea\evidence\stager-evidence-latest.json
  -> aranea-ssh / mt5-kronos-operator / worker-kronos\echo-dev
  -> Get-Content/Get-Item estrictamente read-only -> agente Daedalus
```

- `mt5-kronos` viewer + `sftp-download` fue `POLICY_DENIED` 3/3 antes del filesystem. La certificación viewer `sftp-download` del 2026-09-15 era sobre viewer Linux efímero; no extrapolar a Windows ni ampliar permisos.
- Consumer PASS: `echo-dev` no-admin leyó reporte; publisher SYSTEM, self-hash correcto, `partial=false`, segunda publicación periódica, Write/Create DENIED en reporte/inspector/rollback/evidence, viewer negativo; Stager y worker intactos. Worker observado PID 1700, release 0.2.98, SHA256 `0bceda4badd982b25b01f13ec40a23eb95c8179e28d8a6d955036b30fc7aa474`.
- Certificación de deploy: edad `generated_at_utc` ≤15 min, `partial=false`, `run_identity=SYSTEM`, `evidence.inspector_sha256` igual al registro. Health 8 h NO aplica a deploy. Reporte ausente/STALE ⇒ UNKNOWN y diagnóstico por agente con capabilities existentes; no owner ni one-shot por inercia.
- Owner seed tuvo dos falsos negativos del instalador (EXPECT_RB stale y propiedad JSON equivocada), pero el publisher se certificó con pruebas consumer. Instalador v6 canónico SHA256 `2c32361f6fc213cf82a19b867531fbdd309b3b59e2bb77b778dea794a62a20fb`; rollback/contrato en [[aranea-ssh-mcp]]. Veredicto formal de convergencia Forge es gate del producto separado de la capacidad MCP.

## Uso y límites

- Inspecciones SQX con `read-command`, aunque operator; mutaciones `run-command` sólo con scope, rollback/post-condición. `approvalPolicy="auto"` NO es consentimiento humano.
- Transferencia SFTP/sesiones sólo cuando tool y profile permiten; cerrar sesiones, `signal-process` requiere PID identificado. Windows usa PowerShell.
- `privileged-command` no concede autoridad OS. `mt5-kronos-operator` no-admin. `docker-echo-dev-operator` es root exclusivamente DEV en su host.
- El evidence publisher no autoriza administrar releases, servicios, tareas ni ACL. Echo PROD viewer no permite mutación. Prohibidos ACL ampliadas, bypass, side channels y cualquier uso Aranea MCP para MELI.

## Certificación histórica y autoridad

E2E 2026-09-13: initialize protocolo 2025-03-26, initialized 202, tools/list; en Zeus/Hera/Kronos prueba reversible create/read/delete en `/tmp/aranea-mcp-write-smoke` PASS/CLEAN. H2 viewer tool-level 2026-09-15; Echo PROD viewer certificado 2026-09-15; Windows publisher ACTIVE/CERTIFIED 2026-09-17. Tools, recovery, pruebas completas y rollback: [[aranea-ssh-mcp]]. Selección de perfil/authority: [[aranea-mcps-expert]].