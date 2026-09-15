---
type: change_log
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
entities:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
  - "[[HERMES — Agent Access Operations]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[mcp-access-plane-operations]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-15-b4-human-exit-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-15-b4-human-exit-gate-pass

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `30-resources/runbooks/aranea-mcp-capability-plane.md` (updated: § Consumer onboarding managed — mecanismo de provisioning del secret del chain certificado en B4; limitación single-bearer acotada con evidencia B3.3)
  - `30-resources/runbooks/aranea-observability-mcp.md` (updated: residual owner-side CERRADO; sección Cliente Daedalus/Cursor sin paso pendiente)
  - `30-resources/agents/skills/aranea-mcp-plane-operator/SKILL.md` (updated: paso 7 consumer smoke — validar probe contra superficie real antes de congelar aserciones; chain-cert como gate de persistencia)
  - `80-agents/journal/feedback/system-1/2026-09-15-b4-human-exit-session-feedback.md` (created)
  - `80-agents/journal/sessions/2026-09-15-b4-human-exit-summary.md` (created)
  - `10-projects/Aranea/agentes/HERMES — Bootstrap & Self-Sufficiency.md` (updated: status review, progress 100, B4 PASS, bitácora, tareas B4.1-B4.4)
  - `10-projects/Aranea/agentes/HERMES — Agent Access Operations.md` (updated: callout de handoff; frontmatter updated)
  - `10-projects/Aranea/HERMES — ARANEA AUTONOMOUS OPERATIONS.md` (updated: tarea puente Bootstrap cerrada, bitácora, link)
  - Hermes skill perfil `mcp-access-plane-operations` (updated: header chain-secret B4-certified)

## Motivo

- Cerrar el residual B3.3 (alta de `ARANEA_OBSERVABILITY_MCP_RO_BEARER` en el chain KDE de kor) sin owner, usando la authority B2 existente, y ejecutar el B4 Human Exit Gate contra evidencia runtime/durable.

## Cierre del residual B3.3 (cero intervención owner)

- **Discovery:** `hermes-ops` en Daedalus tiene ACL `rw` sobre `/home/kor/.config/mcp/aranea-env.sh` (archivo REAL del chain) y `rwx` sgid-kor + default ACL `u:kor:r-x` sobre `hermes-managed/`; sin sudo (verificado denegado pre y post). El chain son bloques `if [ -r file ]; then export VAR="$(cat file)"; fi` con guards `$HOME`-relativos.
- **Mutación (AUTO, rollback probado):** bearer transferido stdin-only `mcps`→Daedalus (sha16 `1433fe4157d2825d` íntegro, jamás impreso ni en argv) → `hermes-managed/observability-mcp-ro.bearer` (`640` + ACL `u:kor:r--`) → bloque canónico añadido a `aranea-env.sh` (in-place `r+` vía ACL, owner/mode/ACLs kor preservados; chain `1693→1914B`, sha `35098e152999cea9→0cddf55ec4761ff3`). Patch idempotente por marker, `bash -n` gate con auto-restore.
- **Certificación REAL (config persistente, no stdin):** RED honesta antes de mutar (chain `NOT_SET`); stdin-cert PASS (superficie 22 congelada, probes RO reales, negatives -32602, leak clean); **chain-cert PASS** sourceando `aranea-env.sh` con `HOME=/home/kor` y resolviendo la entry real `aranea-observability-ro` de `mcp.json` (initialize/tools-22/list_datasources/query_prometheus up instant/health/negatives/leak). Rollback materializado: restore sha `35098e15…` byte-identical + secret removed + chain inerte (`rc=2` esperado). Re-aplicación convergente: mismo sha final `0cddf55e…`, mismo bearer, chain-cert final PASS. `mcp.json` intacto `4a8222d505a52ccd` (drift cero).
- **Hallazgos de sonda (probe bugs, no del sistema, corregidos y documentados en la skill operador):** `list_datasources` devuelve `{"datasources":[...]}`; `query_prometheus` sin `queryType` explícito exige `stepSeconds` (usar `instant`+`endTime`); una sonda con `HOME` equivocado reporta falsos NOT_SET.

## B4 Human Exit Gate — PASS

| Condición | Evidencia |
|---|---|
| AUTO/GATED operativo | B0 aplicado (SOUL.md §8.1); esta sesión ejecutó mutaciones AUTO sin pedir OK y no cruzó ningún GATED |
| `mcps-ops` independiente del MCP plane | ssh key-only hermes-ops@mcps, sudo passwordless scoped; ningún MCP de `mcps` usado (B1 PASS + uso real en esta sesión) |
| root-equivalent sólo sobre `mcps` | `sudo -n` sin password en mcps; sudo DENEGADO en Daedalus re-verificado post-cambios |
| repair/config/redeploy sin owner | B3.2 golden repair `aranea-postgres-rw` PASS; B3.3 golden deploy `aranea-observability-ro` PASS; residual chain cerrado en esta sesión sin owner |
| consumer onboarding sin edición owner por capability | B2 PASS (Daedalus/Cursor, entry + smoke + rollback byte-identical); B4 añade provisioning del secret del chain sin owner |
| `aranea-mcp-plane-operator` reusable | 3 ejecuciones end-to-end (repair, deploy, residual-chain) con el mismo patrón baseline→intervención→smoke→post-condición→SoT |
| secrets ausentes de outputs/Agents-OS | bearer sólo stdin/pipe/file; en vault sólo paths/sha16/lengths; wrapper argv-log respetado; leak check CLEAN |
| golden repair PASS | B3.2 (2026-09-15, drift cero, recovery re-smoke) |
| golden deploy PASS | B3.3 (2026-09-15, cert 12/12, rollback byte-identical, drift cero 3000-3008) |
| remaining owner intervention = gates excepcionales | credenciales nuevas de servicios externos (ej. SA Grafana nuevo), PROD mutation, high-blast-radius network, trading (echo): GATED. Configuración MCP rutinaria: cero intervención owner desde B2/B3.3/B4 |

## Evidencia runtime fresca (2026-09-15)

- Plane completo Up (19 containers, familias 3001-3009 + ssh-mcp + portainer); unauth spot 3002/3005/3009 → 401.
- Chain consumer exporta exactamente `ARANEA_OBSERVABILITY_MCP_RO_BEARER` como usuario autorizado; secret files kor originales siguen inaccesibles para `hermes-ops` (least-privilege intacto, demostrado en vivo por los guards `-r`).
- Health ARGUS upstream: Prometheus/Loki/Grafana responses reales en los probes RO (series `up` con job otelcol, 3/3 datasources OK).

## Compartibilidad

- Mecanismo de provisioning del secret del chain (hermes-managed dir + bloque `if [ -r ]` + chain-cert con HOME correcto) es el patrón B4 replicable para toda capability futura: onboarding completo de una capability = entry `mcp.json` + secret del chain, ambos sin owner.
- Transferencia de continuidad: [[HERMES — Agent Access Operations]] (callout de handoff en la nota); primer workload A0-A5 = cola real de blockers Echo/Forge.
