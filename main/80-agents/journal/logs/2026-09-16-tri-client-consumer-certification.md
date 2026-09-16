---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
entities:
  - "[[HERMES — Agent Access Operations]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "80-agents/journal/feedback/system-1/2026-09-16-tri-client-consumer-cert-session-feedback.md"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-16-tri-client-consumer-certification

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** corrección config consumer demostrada (Cursor) + stage de instrumento owner-side (Codex) + deuda nueva documentada. Sin mutación del Access Plane, sin rotación de credenciales, sin smokes funcionales en la fase final (re-brief owner: validación estática; la certificación funcional la ejecuta el owner desde los 3 IDEs).
- **Archivo(s) Sistema 2:**
  - `/home/kor/.cursor/mcp.json` en Daedalus (updated: refs Mongo RO/RW; in-place vía ACL, owner/modo/ACL preservados; `4a8222d505a52ccd`→`8302719f9fe0e7cc`; backup `~kor/.config/aranea/secrets/hermes-managed/mcp.json.bak-tri-20260916-151924`).
  - `10-projects/Aranea/agentes/HERMES — Agent Access Operations.md` (bitácora 2026-09-16c).
  - `10-projects/Aranea/AGENT-PLATFORM/agentes/AGENT-PLATFORM - MCP Access Plane.md` (bitácora 2026-09-16: deuda bearer compartido Mongo/PG).
  - Daedalus:`/tmp/codex-config-normalize.py` (created, stage; sha16 `024c69bc62181a1a` verificado local↔Daedalus; ejecución kor pendiente del owner).
- **Este change log + feedback** (la sesión de recovery paralela ya dejó `2026-09-16-tri-client-mcp-config-normalization.md` con el estado intermedio; este lo cierra).

## Motivo

- Workload owner: certificación tri-client del consumo MCP real en Daedalus; re-brief posterior lo re-enmarca a normalización de configuración (consistencia semántica, mecanismo nativo por cliente, sin pruebas desde los clientes; el owner hará los smokes).

## Fuentes leídas

- Inventario canónico del plane ([[AGENT-PLATFORM - MCP Access Plane]]) + `docker ps`/bearer listing vía `mcps-ops` (sólo nombres/sha).
- Configs efectivas: `~/.cursor/mcp.json` (lectura directa por ACL), `~/.zcode/cli/config.json` (denegada por diseño), `~/.codex/config.toml` (denegada por diseño), chain `/home/kor/.config/mcp/aranea-env.sh` (nombres de variables + sha16, jamás valores).
- Docs oficiales: zcode.z.ai MCP (config paths `mcp.servers`, headers HTTP literales, env para stdio, sin interpolación documentada) y developers.openai.com/codex/mcp (`bearer_token_env_var`, `env_http_headers`, config compartida ChatGPT desktop/CLI/extensión).
- Operadores B2 certificados (`mcp-onboard.py`, `consumer-smoke.py`) y logs B4/B3.3.

## Resultado

- **Cursor: READY (CONFIG_READY).** 11 entradas = 10 capabilities + clon gestionado B2 (RETAINED por decisión owner). Fix demostrado: `aranea-mongo-forge-ro/rw` referenciaban `ARANEA_POSTGRES_MCP_*` (envs correctas `ARANEA_MONGO_FORGE_MCP_*` presentes en el chain). Pre-fix: sweep consumer 11/11 con ciclo MCP completo (initialize→list→call inocua→DELETE) por entrada — Mongo 18/27 tools exactas; post-fix refs validadas estáticamente. Negativos: 401 sin bearer ×10 endpoints.
- **ZCode: CONFIG_READY con caveat (DEFERRED literal credentials).** v3.11.2-6792; config `~/.zcode/cli/config.json` clave `mcp.servers` (docs), `600 kor` sin ACL; smoke 10/10 heredado del baseline owner (config no modificada); no existe soporte documentado de `${env:}` en headers HTTP ⇒ se conserva lo funcional.
- **Codex: OWNER_ACTION_REQUIRED.** codex-cli 0.153.4 (ChatGPT desktop 26.901.51231, config compartida); `~/.codex/config.toml` `600 kor` sin ACL ilegible para `hermes-ops`; mecanismo nativo correcto = `bearer_token_env_var` por entrada. Patcher determinista stageado (backup `.bak-tri-<ts>` 600, atomic replace, round-trip TOML, idempotente, fail-closed, cero secretos).
- **Deuda nueva: bearers Mongo/PG comparten VALOR** (postgres `daedalus-ro.bearer` == mongo `daedalus-ro.bearer` sha16 `5416e5d26b9b75ad`; postgres `daedalus.bearer` == mongo `daedalus-rw.bearer` sha16 `aeca359b4e853f49`). Separación actual por NOMBRE, no por material. Rotación coordinada 4 proxies = owner action posterior (prohibida aquí).
- **Anomalía 13:26:41 resuelta:** edición owner de ambos configs kor esta mañana (backups `.bak-mcp-20260916-132641` + brief "configuración declarada alineada por el owner"); sin tercer implicado.

## Validación

- Fix Cursor: diff exacto de refs; re-parse JSON OK; owner 1000:1000, 660, ACL `u:hermes-ops:rw-` preservados; rollback = restore byte-identical del `.bak-tri-20260916-151924` (sha `4a8222d505a52ccd`).
- Chain: 10/10 variables `ARANEA_*_BEARER` presentes; sha16 OBS chain == proxy-secrets (`aa6aa30fa94c75b4` exact, sin newline).
- Plane intacto: `docker ps` sin drift, cero cambios server-side, cero secretos impresos (sólo nombres/len/sha16), `/tmp` de Daedalus limpio salvo instrumentos stageados declarados.
- Cero uso de sudo; cero ampliación de ACLs; cero ejecución de MCP en la fase final.

## Pendiente

- Owner: ejecutar `python3 /tmp/codex-config-normalize.py` como kor (única acción), luego certificación funcional desde los 3 IDEs (Cursor ya está en condiciones; ZCode sin cambios; Codex tras el patcher).
- Owner (posterior, decisión aparte): rotación coordinada de bearers Mongo/PG compartidos.
- Actualizar `mcp-access-plane-operations` (perfil Hermes) con el mecanismo `bearer_token_env_var` de Codex y la ruta de config ZCode cuando el owner certifique.
