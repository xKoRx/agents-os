---
type: change_log
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities: ["[[AGENTS OS]]"]
related: ["[[MiniMax M3.1 Flash]]", "[[80-agents/crew/INDEX.md|Registro de la Tripulación]]"]
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

# Registro del agente MiniMax M3.1 Flash en la tripulación

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/crew/MiniMax M3.1 Flash.md` (created, `type: agent`, Sistema 2)
  - `80-agents/journal/logs/2026-10-30-minimax-m31-flash-crew-registration.md` (created, este log)
  - `80-agents/crew/INDEX.md` (updated: `related` y lista de superficies registradas, más una regla de superficies con modelo fijo)

## Motivo

- El owner pidió registrar MiniMax M3.1 Flash como otro agente de AGENTS OS. La tripulación de `80-agents/crew/` es el registro canónico de agentes y superficies del vault, y el precedente más cercano es el alta de [[ChatGPT]] (commits `2a77ca02` y `c4a36d49`), que creó el perfil y luego actualizó el índice.
- Identificador exacto reportado por el host en esta ejecución: `minimax/MiniMax-M3.1-Flash`. No se infirió desde capacidades ni desde la superficie.

## Fuentes usadas

- `80-agents/crew/INDEX.md` (contrato de identidad de la tripulación), `80-agents/crew/ChatGPT.md`, `80-agents/crew/ZCode.md`, `80-agents/crew/Ariadna.md` (precedente de superficie con modelo fijo).
- `80-agents/skills/_shared/schema-contract.md` (tipo `agent`: plantilla `70-templates/agent-profile.md`, secciones obligatorias) y `80-agents/skills/_shared/scripts/materialize_schema_note.py`.
- `80-agents/skills/agents-os-agent-run-register/SKILL.md` (clave de comparación superficie×modelo) y `80-agents/agents-os/agent-constitution.md` (reglas 6 y 13).
- Evidencia de fricción ya registrada en el vault sobre el plan de tokens de MiniMax: `80-agents/journal/feedback/system-1/2026-09-10-echo-forge-f04-normal-implementation-session-feedback.md` (F-03/F-04) y `80-agents/journal/feedback/system-1/2026-09-06-echo-forge-mt5-ownership-b1b-session-feedback.md`.

## Resolución aplicada

- El perfil se materializó con el contrato ejecutable (`materialize_schema_note.py agent`), no con frontmatter escrito a mano, y luego se completaron especialidades, modelo, alias y secciones obligatorias.
- El modelo queda fijo en el perfil (`model: MiniMax-M3.1-Flash`), como en [[Ariadna]], y el índice lo explicita para que no se confunda con las superficies de `model: dynamic`.
- La atribución de identidad queda sin ambigüedad: un modelo ejecutado dentro de otra superficie sigue registrándose a esa superficie (`agent_surface: [[ZCode]]`, `agent_model: minimax/MiniMax-M3.1-Flash`); la entrada del modelo aplica cuando se usa como superficie propia.
- La fricción del plan de tokens se documenta como riesgo conocido de la familia MiniMax, marcando que la evidencia disponible proviene de MiniMax-M3 y no está verificada para M3.1 Flash.
- No se tocó el bootstrap, el perfil global ni la constitución. No se creó `agent_run` porque este trabajo fue documental y no un segmento material de código (regla de `agents-os-agent-run-register`).

## Validación

- Contrato de tipo `agent` en verde: `materialize_schema_note.py agent "80-agents/crew/MiniMax M3.1 Flash.md" --dry-run` resolvió sistema s2 y plantilla `70-templates/agent-profile.md`; la materialización real confirmó el mismo contrato.
- Frontmatter del perfil y del log validados contra el contrato (`schema_version: 1`, `status: active`, `share_scope`, `load_policy`, `indexable`, `index_priority`, secciones `## 📜 Directivas y Reglas de Comportamiento` y `## 🛠️ Limitaciones Técnicas y Operativas`).
- Enlaces verificados: `[[MiniMax M3.1 Flash]]` resuelve al archivo creado y las referencias a superficies existentes (`[[ZCode]]`, `[[Codex]]`, `[[Claude Code]]`, `[[Cursor]]`, `[[Antigravity]]`, `[[Copilot CLI]]`, `[[ChatGPT]]`, `[[Ariadna]]`) son canónicas.
- `agents-os-doctor` ejecutado sobre el vault: sin veredictos nuevos atribuibles a este cambio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar `80-agents/crew/MiniMax M3.1 Flash.md` y este log, y revertir en `80-agents/crew/INDEX.md` las tres líneas agregadas (`related`, superficie registrada y regla de superficies con modelo fijo). No hay estado derivado ni migraciones que revertir.
