---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-13"
updated: "2026-09-17"
tags:
  - area/aranea
  - tech/mcp
  - tech/ssh
---

# SSH MCP — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]], no proyecto paralelo. Estado de SSH y del publisher Windows reconciliado al 2026-09-17. Router agent-facing: [[aranea-mcps-expert]]; procedimiento y evidencia detallada: [[aranea-ssh-mcp]]. No utilizar esta nota como inventario general de todas las capabilities; ver [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

## Objetivo

Acceso SSH centralizado de agentes Aranea sin compartir private keys ni credenciales upstream. Separar autoridad del profile MCP, identidad remota y permisos OS. El acceso a evidencia privilegiada Windows se implementa por publicación SYSTEM de datos acotados, no elevando `echo-dev`.

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

Los profiles SQX fueron promovidos el 2026-09-13 sin cambiar identidad ni host-key pinning. `echo-runtime-prod` está certificado desde 2026-09-15; observación sí, restart/control PROD no. Todos los permisos se limitan al host y usuario de cada profile.

## Windows: camino final certificado

```text
AraneaEvidencePublish (Task Scheduler, SYSTEM, cada 5 min)
  -> C:\ProgramData\Aranea\evidence\stager-evidence-latest.json
  -> aranea-ssh / mt5-kronos-operator / worker-kronos\echo-dev
  -> Get-Content o Get-Item estrictamente read-only -> agente Daedalus
```

- `mt5-kronos` viewer + `sftp-download` fue denegado físicamente `POLICY_DENIED` 3/3, antes del filesystem; NO usarlo ni ampliar permisos para este caso. La certificación viewer `sftp-download` del 2026-09-15 correspondió a un viewer Linux efímero y no prueba acceso en Windows.
- Consumer PASS 2026-09-17: lectura como `echo-dev` no-admin; task SYSTEM; inspector self-hash canónico; `partial=false`; segunda publicación autónoma demostrada; Write/Create DENIED en JSON/inspector/rollback/evidence; Stager/worker no modificados. Worker observado PID 1700, release 0.2.98, SHA256 `0bceda4badd982b25b01f13ec40a23eb95c8179e28d8a6d955036b30fc7aa474`.
- Validez para certificar despliegue: `generated_at_utc` no mayor a 15 min, `partial=false`, `run_identity=SYSTEM`, `evidence.inspector_sha256` coincide con registro. Ocho horas es umbral de health general, NO certificación de deploy. Si falta o está STALE: diagnosticar la tarea/publicación dentro de la autoridad ya disponible y marcar UNKNOWN; no pedir owner por inercia ni usar un inspector elevado improvisado.
- El instalador tuvo dos falsos negativos de self-verify (EXPECT_RB stale y propiedad JSON equivocada). Instalador canónico corregido v6 SHA256 `2c32361f6fc213cf82a19b867531fbdd309b3b59e2bb77b778dea794a62a20fb`; ver detalles/rollback en [[aranea-ssh-mcp]]. El estado certificado se basó en pruebas consumer materiales, no en el exit del instalador. La formalización de convergencia F05C sigue siendo responsabilidad de esa misión, no del workstream MCP.

## Uso y límites

- Inspección SQX: preferir `read-command` aunque el profile sea operator. Mutación: `run-command` sólo con target, scope, rollback/post-condición y verificación. `approvalPolicy="auto"` no representa aprobación humana.
- SFTP upload/download y sesiones/background sólo donde el profile y tool lo permitan; cerrar sesiones; `signal-process` sólo sobre PID identificado. En Windows el shell remoto es PowerShell.
- `privileged-command` no crea privilegios OS. `mt5-kronos-operator` es writable como `echo-dev`, NO admin Windows. `docker-echo-dev-operator` sí es root-equivalent exclusivamente en el host DEV correspondiente.
- No instalar, detener o administrar servicios/release Windows por el hecho de disponer de evidencia SYSTEM. No usar Echo PROD para mutaciones ni capabilities Aranea sobre MELI. No abrir ACLs, extender viewer o crear side channels como workaround.

## Certificación histórica y autoridad

E2E 2026-09-13 por MCP real: initialize, notifications/initialized, tools/list y create/read/delete en `/tmp/aranea-mcp-write-smoke` PASS/CLEAN para SQX Zeus/Hera/Kronos. H2 viewer tool-level corregido el 2026-09-15; Windows evidence añadido y certificado el 2026-09-17. Detalles de tool surface, pruebas, recovery y rollback en [[aranea-ssh-mcp]]. Routing y elección de ambiente/capability en [[aranea-mcps-expert]].