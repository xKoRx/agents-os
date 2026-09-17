---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-17"
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
  - "[[Daedalus — Development Agents MCP Access & Gaps]]"
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

## Propósito y precondiciones

Inspección y operación remota de hosts Aranea por `aranea-ssh` (endpoint `http://mcps.lab.aranea.cl:3000/`). El router [[aranea-mcps-expert]] elige ambiente/capability/autoridad; aquí vive la mecánica. El estado transversal de accesos de los coding agents Daedalus y sus gaps está en [[Daedalus — Development Agents MCP Access & Gaps]]. Sólo Aranea; para MELI/corporativo STOP. El cliente debe exponer `aranea-ssh`. Private keys/credenciales SSH permanecen en `mcps`; no pedirlas, imprimirlas ni copiarlas. No sustituir MCP por [[echo-forge-workers-shared-access]] si MCP cubre la operación.

## Perfiles y autoridad efectiva

| Profile | Target | Usuario remoto | Autoridad / uso |
|---|---|---|---|
| `sqx-zeus` | Linux SQX Zeus | `echo-dev` | operator writable no-root; runtime SQX dentro de sus permisos |
| `sqx-hera` | Linux SQX Hera | `echo-dev` | operator writable no-root |
| `sqx-kronos` | Linux SQX Kronos | `echo-dev` | operator writable no-root |
| `mt5-kronos` | Windows worker-kronos | `echo-dev` | viewer RO, tool allowlist limitada; **NO `sftp-download` Windows** (POLICY_DENIED comprobado) |
| `mt5-kronos-operator` | Windows worker-kronos | `worker-kronos\echo-dev` | operator writable **no-admin**; upload/compile y lectura del evidence JSON de SYSTEM |
| `docker-echo-dev-operator` | Linux `docker-echo-dev`, `.75` | `root` | root-equivalent únicamente DEV; filesystem/Docker/lifecycle, seguir runbook Flink |
| `echo-runtime-prod` | Echo PROD `.71` | `echo-dev` | viewer RO, sin sudo; procesos/listeners/fs-meta, no restart/deploy |

`operator` es autoridad del MCP, NO privilegio OS adicional. `privileged-command` no eleva si el usuario no dispone ya de sudo/admin y acción autorizada. `approvalPolicy="auto"` puede autoejecutar una tool: no equivale a aprobación humana. Antes de mutación, target exacto, blast radius, rollback/post-condición y verificación. No convertir una lectura en `run-command` por comodidad.

## Tool surface y procedimiento

Surface `ssh-mcp` v2.8.0: `list-connections`, `list-sessions`, `open-session`, `close-session`, `read-session-output`, `read-command`, `run-command`, `privileged-command`, `signal-process`, `sftp-upload`, `sftp-download` (disponibilidad efectiva por policy/profile; listado no equivale a permiso).

1. Descubrir conexión exacta por `list-connections`; confirmar identidad remota (`whoami`/`id`) con lectura autorizada y no inferir root.
2. Inspección: `read-command`, preferentemente comando único allowlisted (`ls`, `cat`, `grep`, `find`, `stat`, `df`, etc. según profile). Compuestos/pipelines/clases 'safe' pueden ser denegados: dividir, no cambiar a operator o saltarse policy.
3. Mutación: sólo operator/identidad con permiso OS real, `run-command` y target delimitado + rollback/post-condición. `signal-process` exige PID identificado.
4. Sesión stateful/background sólo si CWD/env o proceso largo aporta valor; `open-session` + tool adecuada; leer output y cerrar con `close-session`. Reutilizar una sesión MCP en probes para no saturar pool (ver más abajo).
5. Transferencia pequeña por `sftp-upload`/`sftp-download` cuando tool y profile lo permitan; para binarios/grandes staging autorizado. No HTTP improvisado/netcat/side channel. **En viewer `mt5-kronos`, `sftp-download` responde POLICY_DENIED ANTES del filesystem**: usar `mt5-kronos-operator`+`Get-Content` read-only para evidence JSON, no relajar viewer.
6. Windows usa PowerShell, identidad validada `worker-kronos\echo-dev`, home `C:\Users\echo-dev.WORKER-KRONOS`; no asumir POSIX ni `&&` universal. Para MT4 compilación `master_test_001`, includes globales pueden resolver en AppData `echo-dev` aunque fuente viva en árbol KoR; mirror validado `C:\Users\echo-dev.WORKER-KRONOS\AppData\Roaming\MetaQuotes\Terminal\8819D02A34F64665EDC6BEA4A390310C\MQL4\Include\`. Antes de cambiar EA/ACL por `can't open include`, verificar ese mirror.
7. `docker-echo-dev-operator` es root sólo en `.75` DEV; Flink control REST por `aranea-flink-dev-admin`, host/Docker/lifecycle por SSH. Portainer stack 1 es declarativo; `/data/compose/1/docker-compose.yml` interno equivale a host `/var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml`. No crear Compose paralelo ni `docker compose up -d` rutinario por hash drift.
8. `POLICY_DENIED` y Access Denied son boundaries. No ampliar ACL/policy ni credenciales automáticamente. Si requiere admin inexistente, reportar la capability exacta faltante y alternativa autorizada; no 'privileged-command' improvisado.

## Certificaciones por fecha (no equiparar historia con estado vigente)

### SQX operators — 2026-09-13 PASS

`SQX-zeus/hera/kronos` promovidos viewer→operator sin cambiar host, puerto, `echo-dev`, key, pin ED25519, `tty=false`, timeout ni `approvalPolicy=auto`. Reiniciado sólo ssh-mcp, `running/healthy`, status perfiles operator. MCP Streamable HTTP initialize protocolo `2025-03-26`, notifications/initialized `202`, tools/list PASS; los tres targets `run-command` create `/tmp/aranea-mcp-write-smoke` → `read-command` readback → remove PASS/CLEAN. Eso prueba circuito real cliente→HTTP MCP→SSH→FS; no root.

### worker-kronos operator — 2026-09-11 y corrección 2026-09-17

`run-command`, `sftp-upload`, `sftp-download` en **operator** `worker-kronos\echo-dev` probados con fixture reversible bajo `C:/Windows/Temp`. La nota H2 2026-09-15 de SFTP viewer se certificó en profile **Linux efímero `linux-viewer-smoke`**, NO en `mt5-kronos`. En Windows `mt5-kronos` viewer + `sftp-download` = `POLICY_DENIED` 3/3 incluso con `echo-dev:R`: enforcement de profile antes del filesystem. Esta es la autoridad factual final; nunca reusar el claim incorrecto.

### H2 viewer enforcement — 2026-09-15 PASS

Defecto anterior: `run-command echo/whoami` pasaba sobre viewer porque sólo se chequeaba clase `read-only`. Fix server-side tool-level `read-only-tool-boundary`, imagen `local/ssh-mcp:2.8.0-d2d7696-h2fix`; `run-command` en viewer DENIED y `read-command` permitido. Allowlist nominal de tools viewer upstream incluye `read-command`, `list-connections`, `list-sessions`, `read-session-output`, `sftp-download`, `close-session`, `open-session`; **la presencia nominal de `sftp-download` NO certifica ejecución por el profile Windows concreto**. Desde Daedalus: `mt5-kronos` read `whoami` PASS/run `echo` DENIED; Linux viewer smoke idem; `mt5-kronos-operator` run PASS; Docker DEV run PASS; SQX operator read+run PASS.

### echo-runtime-prod — CERTIFIED 2026-09-15 / GAP-ECHO-004 CLOSED

Perfil `.71` `echo-dev`, viewer/RO, keyRef plane existente, host-key pinning. Owner seed creó identidad `echo-dev` uid/gid 1001 sin sudo y authorized key 600 (`.ssh` 700); `sshd -t` PASS. Consumer Daedalus 7 profiles, identity `echo-dev@echo` PASS, Core/Gateway/echo-functions RUNNING al corte, Bridge NOT_DEPLOYED, listeners 80/9080/9090/8080/8090. Viewer `run-command` MUST DENY, `read-command` allowlist `whoami`, `hostname`, `id`, `ps aux`, `ss -tlnp`, `cat`, `ls`, `journalctl`; `docker ps`, `curl`, `systemctl`, `dmesg`, `pgrep` son POLICY_DENIED aun si parecen 'safe'. Journal sólo propio de `echo-dev`; logs PROD por `aranea-observability-ro`. No atribuir PID de otros usuarios desde `ss` sin root. Host key de `.71` idéntica a `sqx-zeus` (clon): rotación controlada pendiente como higiene, con actualización simultánea de `trustedHostKey`. Revoke owner-side: quitar línea `echo-dev@mcps` de authorized_keys en `.71`; opcional retirar profile.

### Evidence publisher worker-kronos — 2026-09-17 ACTIVE / CERTIFIED (owner seed COMPLETED)

**Contrato:** Task Scheduler `AraneaEvidencePublish` como SYSTEM, cada 5 minutos, guard anti-solapamiento (skip sin efectos) ejecuta inspector PowerShell protegido de superficie fija: cero inputs/rutas dinámicas/red. Publica atómicamente tmp+rename JSON sanitizado a `C:\ProgramData\Aranea\evidence\stager-evidence-latest.json`; dirs `Aranea`/`evidence` sin herencia, Administrators+SYSTEM write; `worker-kronos\echo-dev:R` sólo reporte. Contenido: `generated_at_utc`, `publish_interval_minutes=5`, `deployment_stale_after_minutes=15`, `health_stale_after_hours=8`, `partial`, `errors`, self-hash y evidencia worker/Stager/CURRENT/reconciliación/poller.

**Camino agent-facing CERTIFICADO:** `AraneaEvidencePublish SYSTEM -> JSON -> aranea-ssh / mt5-kronos-operator -> Get-Content/Get-Item read-only como echo-dev -> agente Daedalus`. El operator MCP permite ejecutar la lectura, pero NO eleva identidad ni autoriza modificar publicación. Para deployment/runtime certification: `generated_at_utc` ≤15 min, `partial=false`, `evidence.inspector_sha256` igual al hash canónico, `run_identity=SYSTEM`; consultar además publish task `last_run_utc/last_result`, comparar con reloj cliente. Umbral 8 h es sólo salud general, NO deploy. Ausencia/STALE => evidencia UNKNOWN/no certificable; diagnosticar publisher con authority existente, no volver al one-shot owner sin demostrar nuevo gap.

**Pruebas materiales 2026-09-17:** task SYSTEM, primera publicación 18:43Z y segunda 18:53Z (cadencia constatada), `partial=false`, self-hash inspector `28d782b78ebf1374…83e4a07` igual al esperado, lectura RO efectiva `echo-dev`; Write/Create DENIED sobre reporte, inspector, rollback, dir evidence; viewer `sftp-download` POLICY_DENIED; Stager/worker intactos. Reporte incluye worker PID `1700`, `C:\ProgramData\Stager\releases\0.2.98\bin\sqx-mt5-worker.exe`, SHA256 `0bceda4badd982b25b01f13ec40a23eb95c8179e28d8a6d955036b30fc7aa474` exacto con release 0.2.98. Esta capability resuelve inspección Windows; **NO certifica por sí sola la campaña F05C/F04 ni habilita acciones administrativas**.

**Owner seed/verifier histórico:** intento 1 abortó por `EXPECT_RB` stale tras parchear rollback; copia de bytes era íntegra. Intento 2 creó task/publicó JSON, pero self-verify consultó `$j.inspector_sha256` en vez de `$j.evidence.inspector_sha256` y devolvió falso `exit 4`. El agente certificó materialmente consumer/publisher; instalador v6 corregido canónico `aranea-evidence-install2.bat` SHA256 `2c32361f6fc213cf82a19b867531fbdd309b3b59e2bb77b778dea794a62a20fb`, stageado para posibles reinstalaciones. Rollback `aranea-evidence-rollback2.bat` está materializado y su SHA verificado: elimina task y `C:\ProgramData\Aranea` únicamente si se ejecuta elevado por owner autorizado. No ejecutarlo rutinariamente. Residuo benigno ACL `C:\Windows\Temp\sim-aranea` requiere owner sólo si decide higiene, no bloquea.

**Staging byte exact:** `sftp-upload` transporta `content` string, normaliza saltos de línea y NO reemplaza fiable un path existente (puede reportar éxito dejando bytes previos); para scripts/binaries byte-exactos: base64 sin newlines→`certutil -decode` target→comparar sha256 local/remoto completo. Evitar ensayos ACL en Temp que quiten herencia al directorio y bloqueen después al propio `echo-dev`.

## Operación, validación y rollback del plano SSH

- Pool ssh-mcp de 64 sesiones: probes init-per-call agotan pool ⇒ 503 `Server is at its session limit`; prevenir abriendo UNA sesión por probe y reutilizando `Mcp-Session-Id`, cerrándola. Recovery management-path sólo cuando confirmado: `docker restart ssh-mcp`, después health/consumer smoke; nunca reiniciar producto por fallo MCP. No atribuir defectos Hasura mcp-proxy a SSH.
- Config bind-mounted `ssh-mcp` debe ser mode `600`, owner uid/gid `65532:65532`; con `644 root` server rechaza world-accessible y con `600 root:root` falla EACCES. Restaurar config y verificar before restart si hubo drift.
- Rollback promoción SQX: revertir profiles a `viewer`+`readOnly=true`, reiniciar sólo ssh-mcp y certificar status/read-command, backup original cuando se requiera byte equality. Rollback profile `echo-runtime-prod` desde backup `/tmp/config.toml.pre-echo-runtime-prod` en mcps con owner/mode `65532:65532/600`, reiniciar ssh-mcp y revalidar perfiles/health. Rollback Windows publisher: procedimiento elevado y bundle owner descritos arriba. Docker DEV lifecycle: seguir runbook Flink, no usar `compose up -d` como rollback implícito.

```text
Capability:         aranea-ssh
Profile:            <nombre exacto>
Target / identity:  <host + usuario OS real>
Authority:          <viewer|operator + permisos OS>
Operation:          <tool exacta + lectura/mutación>
Evidence:           <salida material + fecha/frescura si aplica>
Mutation:           none | target + rollback/post-condición + verificación
Boundary:           none | POLICY_DENIED/Access Denied, sin bypass
Secrets:            none persisted
```

Ante transport/auth/session fallidos, primero [[aranea-mcp-capability-plane]]; ante elección de authority, [[aranea-mcps-expert]]. No imprimir secretos, no acceder a MELI y no publicar servicios extra.