---
type: change_log
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities: []
related:
  - "[[meli-agent-dev]]"
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

# observability-metrics-standard — skill creada + plugin sentinels instalado en Claude

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `30-resources/agents/skills/observability-metrics-standard/SKILL.md` (creado)
  - `80-agents/skills/INDEX.md` (fila + conteo federadas transversales 12→13, `updated`)
  - `30-resources/agents/00-index.md` (fila + conteo páginas curadas 22→23, `updated`/`reviewed`)
  - `30-resources/agents/log.md` (entrada de ingesta)
  - Fuera del vault: marketplace `sentinels-commands` agregado y plugin `sentinels@sentinels-commands` (v0.1.0) instalado y habilitado en Claude Code (`~/.claude/plugins/`), espejando la instalación que ya existía en Codex (`~/.codex/plugins/`).

## Motivo

- El usuario evaluó el plugin corporativo `sentinels@rio-observability-standard` (repo `melisource/fury_rio-observability-standard`, instalado previamente en Codex) para decidir si podía independizarse de él escribiendo una skill propia.
- Lectura del contrato real (`docs/guide/metrics-standard.md`, v1.0.0, Status: Proposed) y de las tres skills del plugin (`scan`/`migrate`/`pr-review`) mostró que el método (checklist de límites de ciclo de vida, principios counter/histogram/gauge, tags acotados, emisión terminal post-commit, triage scan/migrate/review) es portable, pero la gramática `signals.rio.<domain>.<entity>.<event>`, el tag `fury_app` y el catálogo de entidades son un contrato Meli/RIO todavía evolucionando — forkearlo lo habría desincronizado del estándar real.
- Decisión acordada con el usuario: extraer solo el método a una skill transversal propia (uso Aranea/personal), y para Meli/RIO seguir dependiendo del plugin real — pero instalado también en Claude Code, no solo en Codex, para que la referencia sea utilizable en ambas superficies.

## Fuentes usadas

- `~/.codex/.tmp/marketplaces/rio-observability-standard/docs/guide/metrics-standard.md` (contrato v1.0.0).
- `~/.codex/.tmp/marketplaces/rio-observability-standard/sentinels/skills/{scan,migrate,pr-review}/SKILL.md`.
- `~/.codex/.tmp/marketplaces/rio-observability-standard/.claude-plugin/marketplace.json` (nombre real de marketplace para Claude: `sentinels-commands`).
- `80-agents/skills/agents-os-skill-authoring/SKILL.md`, `_shared/note-types.md`, `_shared/skill-contract.md`, `80-agents/templates/skill.md`, `memory/public/runbook/agents-os-skill-authoring.md`.
- `30-resources/agents/skills/meli-agent-dev/SKILL.md` y `aranea-agent-dev/SKILL.md` para confirmar que esta skill no pertenece a ninguno de los dos dominios (es transversal, no toca acceso MCP ni repos corporativos).

## Resolución aplicada

- Clasificación: skill (procedimiento repetible multi-juicio), no runbook ni memoria.
- Materializada con `materialize_schema_note.py skill 30-resources/agents/skills/observability-metrics-standard/SKILL.md` (sin copiar frontmatter a mano).
- Trigger boundary explícito: sí para Aranea/homelab y proyectos personales sin contrato corporativo mandatado; no para Meli/RIO/Signals/Ads (handoff a `meli-agent-dev` → plugin `sentinels`); adyacente: acceso MCP Aranea sigue siendo exclusivo de `aranea-mcps-expert`.
- Se registró la skill en ambos índices federados (`80-agents/skills/INDEX.md` y `30-resources/agents/00-index.md`) y en `30-resources/agents/log.md`.
- Se agregó el marketplace `git@github.com:melisource/fury_rio-observability-standard.git` a Claude Code (`claude plugin marketplace add`) y se instaló/habilitó `sentinels@sentinels-commands` (`claude plugin install`); requiere una sesión nueva de Claude Code para que las skills `scan`/`migrate`/`pr-review` aparezcan en contexto.
- No se tocó `meli-agent-dev` en este cambio: el usuario no pidió agregar el binding de routing todavía, solo instalar el plugin y extraer la skill genérica.

## Validación

- `doctor.py --component structural`: PASS, 0 findings.
- `doctor.py --component conformance`: FAIL preexistente en el corpus (SCHEMA-VALIDATOR-GREEN, LOAD-POLICY-VOCABULARY, NO-SECRETS-IN-MARKDOWN — drift previo no introducido por este cambio) más un finding propio de REGISTRY-DISK-PARITY (`observability-metrics-standard` ausente del índice) que se corrigió en el mismo cambio agregando la fila a `30-resources/agents/00-index.md`. El otro finding de esa misma regla (`aranea-mcp-plane-operator` ausente) es drift preexistente fuera de este alcance.
- Activación: positivo (proyecto Aranea/personal sin estándar propio) → aplica; negativo (repo Meli/RIO/Signals) → no aplica, handoff a `meli-agent-dev`; adyacente (elegir ambiente/conectar MCP Aranea) → handoff a `aranea-mcps-expert`.
- `claude plugin list` confirma `sentinels@sentinels-commands` versión 0.1.0, scope user, estado enabled.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni credenciales; solo rutas de vault y de configuración local de Claude Code.

## Rollback

- Eliminar `30-resources/agents/skills/observability-metrics-standard/`, revertir las filas agregadas en `80-agents/skills/INDEX.md`, `30-resources/agents/00-index.md` y `30-resources/agents/log.md`.
- `claude plugin uninstall sentinels@sentinels-commands` y `claude plugin marketplace remove sentinels-commands` para deshacer la instalación en Claude Code; Codex no se ve afectado.
