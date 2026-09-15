---
type: change_log
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
entities:
  - "[[HERMES — Agent Access Operations]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[Echo]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
  - "[[Echo — Access & Physical Capability Matrix]]"
  - "[[mcp-access-plane-operations]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-15-gap-echo-004-closed

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/ACCESS-CERTIFICATION.md` (updated: veredicto RESUELTO; owner gate CUMPLIDO; nueva sección "GAP-ECHO-004 CLOSED"; superficie sin capacidad → CERTIFIED; conclusión)
  - `10-projects/Echo/agentes/Echo — Access & Physical Capability Matrix.md` (updated: reconciliación; filas Gateway/Core-Bridge RECERTIFICADAS; GAP-ECHO-004 CERRADO; gate E-02 Gateway physical TARGET+CERT)
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (updated: delta de readiness 2026-09-15b; trigger de reactivación abierto)
  - `10-projects/Echo/agentes/Echo — E-02 Control Safety, Auth and Journal Recovery.md` (updated: bitácora 2026-09-15b sin cambio de gates)
  - `10-projects/Aranea/agentes/HERMES — Agent Access Operations.md` (updated: Bitácora 2026-09-15b; decisión A-D08)
  - `30-resources/runbooks/aranea-ssh-mcp.md` (updated: fila perfil CERTIFICADO; PENDING_OWNER_GATE → RESUELTO con lección de preflight; cobertura real del viewer; rollback de seed; gotcha pool de sesiones)
  - `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` (updated: fila viewer `echo-runtime-prod` CERTIFICADO en tabla de ambientes)
  - skill local `mcp-access-plane-operations` (updated: recert post-seed, preflight de identidad, sesión única, bearer ssh family)

## Motivo

- Cierre formal de GAP-ECHO-004: owner seed instalado en `.71` y recertificación completa del viewer `echo-runtime-prod` desde el consumer real Daedalus/cursor (workload A0.1 de [[HERMES — Agent Access Operations]], parte 2). Sin tocar Echo productivamente, sin restart de Gateway/Core/Bridge, sin rotar host keys, sin iniciar etcd/Temporal.

## Resultado

- **Owner seed CUMPLIDO (GATED → hecho por el owner):** `mcps:/opt/mcp/ssh/keys/echo-dev.pub` (fingerprint `SHA256:2Qv9f2AREQyse50bGYaTLc1PHK43gvuf3xgv5TTJ+I0`, leído de disco antes del bundle) instalada append-only en `authorized_keys` de `echo-dev` en `192.168.31.71`. Corrección de runtime del owner: la identidad `echo-dev` NO preexistía — fue creada como identidad dedicada (uid/gid 1001, grupos sólo `echo-dev`, sudo DENIED, home 750, `.ssh` 700, archivo 600, `sshd -t` PASS). Lección: el bundle asumía la identidad preexistente; preflight obligatorio `id -u <user>` en futuros seed bundles (registrado en runbook + skill + A-D08).
- **Recertificación consumer PASS (Daedalus real, probe server-side en mcps, bearer por stdin, sesión MCP única):** initialize PASS (SSH MCP Server 2.8.0); 11 tools exactos; perfil visible (7 perfiles); identity `whoami=echo-dev` / `hostname=echo` / `id uid=1001(echo-dev)… ` sin sudo ni grupos operator; **Gateway RUNNING** (`echo-gateway` PID 713, desde ago09, como `kor`), **Core RUNNING** (`echo-core` PID 110701, desde ago20), `echo-functions` (StateFun) RUNNING (PID 320982), **Bridge NOT_DEPLOYED** (sin proceso — registrado, no se levanta); listeners 80/9080/9090/8080/8090 (+22/53); negative `run-command echo cert-negative-probe` → `POLICY_DENIED … read-only` MUST DENY (H2 observable post-seed); leak check CLEAN.
- **Boundary viewer confirmado:** `docker ps`, `curl`, `systemctl`, `dmesg`, `pgrep` → POLICY_DENIED (el enforcement rechaza también la clase `safe`, no sólo el tool); `journalctl` acotado al user journal de `echo-dev`; `ss -tlnp` sin atribución de proceso de otros usuarios. Logs productivos siguen por `aranea-observability-ro` (correlación: Loki `service=echo-core` vivo en sesión anterior; health `/health` 200 re-verificado desde mcps en esta sesión).
- **GAP-ECHO-004 → CLOSED.** Prerrequisito de observación runtime de CERT-E04-01 cubierto por vía directa (viewer) + observabilidad. Deuda separada NO bloqueante: host key `.71` idéntica a `sqx-zeus` (rotación owner opcional).
- **Intervención en mcps (AUTO, sin cambio de config):** `docker restart ssh-mcp` único, tras agotar el pool de 64 sesiones con probes init-only por llamada; container healthy; config intacto. Gotcha + prevención (sesión única por probe) registrados en runbook y skill.

## Validación

- Probe de certificación con aserciones duras derivadas del schema vivo (`tools/list` → `inputSchema.required`/`properties`; argumento de selección de perfil = `profile` top-level) — RESULT: PASS, EXIT=0.
- Salud del plane post-restart: `docker ps` healthy + certificación completa posterior PASS.
- Sin mutación en `.71` (sólo owner seed); sin restart de Gateway/Core/Bridge; sin secrets en chat/vault (key pública + fingerprint sólo por referencia/stdin).
- Drift: único delta en mcps = restart de ssh-mcp (estado expected post-restart); `/tmp` de mcps y local con scripts de probe eliminados; sesión MCP cerrada implícitamente al terminar el proceso del probe.

## Pendiente

- Backlog reactivo: capabilities todas operacionales; siguiente trabajo pertenece a los gates propios de E-02 (ejecutar verificaciones Hasura/Kafka/Flink contra capabilities certificadas) — fuera del scope de esta sesión.
- Deuda abierta no bloqueante: rotación de host key de `.71` (owner, opcional; actualizar `trustedHostKey` del perfil en el mismo cambio).
