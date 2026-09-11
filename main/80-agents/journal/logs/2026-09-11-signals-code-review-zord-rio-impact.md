---
type: change_log
schema_version: 1
scope: session
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Meli]]"
project:
application:
entities:
  - "[[RIO]]"
  - "[[local-agents-pipeline-cli]]"
  - "[[ads-signals-knowledge-library]]"
related:
  - "[[signals-code-review]]"
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

# 2026-09-11-signals-code-review-zord-rio-impact

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/skills/signals-code-review/SKILL.md` — skill personal canónica creada.
  - `80-agents/memory/public/runbook/signals-code-review-runbook.md` — runbook mecánico creado.
  - `80-agents/skills/INDEX.md` — registro de la skill actualizado.
  - `80-agents/memory/public/user-preference/rjara-meli-work-preferences.md` — referencia legacy a la copia Claude reemplazada por las skills canónicas.
  - `30-resources/tools/local-agents-pipeline-cli.md` — reviewer personal RIO y reglas de activación registrados.
  - `~/.config/zords/agents/rjara-rio-impact.md` — Zord global local, manual y deshabilitado por defecto creado.

## Motivo

- Consolidar el criterio personal de code review de Rodrigo dentro de AGENTS OS y extenderlo con revisión multiagente mediante Zord, contraste de PR/specs y detección de impacto transversal entre aplicaciones de RIO usando la knowledge library oficial y el RIO Atlas.

## Fuentes usadas

- Contratos de autoría: `80-agents/skills/agents-os-skill-authoring/SKILL.md`, `80-agents/skills/_shared/skill-contract.md`, `80-agents/skills/_shared/note-types.md`, `80-agents/skills/_shared/schema-contract.md` y `80-agents/memory/public/runbook/agents-os-skill-authoring.md`.
- Criterio previo: copia legacy `~/.claude/skills/signals-code-review/SKILL.md`, [[rjara-agent-profile]], [[rjara-meli-work-preferences]] y learnings de review enlazados.
- RIO: [[ads-signals-knowledge-library]], su `AGENTS.md`, startup, context packs, source manifest y ledger bilateral; [[RIO Atlas]], [[integration-map]], [[Fuentes — Workspace de repositorios]] y fichas de aplicaciones.
- Zord: [[local-agents-pipeline-cli]], sus prompts `io-boundaries`/`cross-repo-validation` y README del checkout documentado.
- Redacción y publicación: [[human-first-technical-writing]] y documentación oficial de GitHub para crear una Pull Request review con comentarios inline mediante `line`/`side`.

## Resolución aplicada

- La skill conserva decisiones contextuales: alcance, frontera transversal, priorización, criterios personales, reconciliación de evidencia y veredicto. El runbook posee baseline Git, recuperación progressive-disclosure, comandos Zord, evidencia cross-repo, validación, estados degradados y recuperación.
- Se fijó la jerarquía código owner > knowledge library > Atlas/fichas, con chequeo de frescura y prohibición de convertir documentación stale o findings de Zord en verdad sin contraste.
- La revisión permanece read-only; descripción de PR y fixes tienen handoffs separados.
- La validación de tests parte por una matriz de comportamientos críticos del PR y sus resultados observables; coverage sigue permitido como complemento, pero no acredita por sí solo los comportamientos materiales.
- Zord se resuelve exclusivamente como la tool canónica [[local-agents-pipeline-cli]], primero por binario y luego por su checkout owner registrado; queda prohibido hacer discovery abierto, recrearlo o usar `zord add` durante un review.
- El workflow quedó semiautomático con un único gate humano: el agente investiga, verifica y presenta comentarios Human First con su porqué; Rodrigo aprueba todos, algunos IDs o ninguno; tras aceptación se publica una sola review breve y se verifica por read-back.
- Se agregó un gate fail-closed: la skill sólo opera cuando la pertenencia a Meli está demostrada. En proyectos no Meli o de identidad incierta devuelve `NOT_APPLICABLE` antes de invocar Zord y no cae a un review genérico.
- Para todo proyecto Meli, Zord es obligatorio. Los proyectos Meli fuera de Signals/RIO usan el set estándar; Signals/RIO agrega `rjara-rio-impact` con `--include`, manteniéndolo global, manual y disabled para que nunca se active accidentalmente.
- `rjara-rio-impact` revisa el diff y fuentes oficiales por separado. El coordinador no le entrega briefs, prioridades, sospechas ni findings anteriores; sólo activa el revisor y proporciona el diff o diffs relacionados, evitando sesgar su foco.

## Validación

- `validate_schema_contract.py --type skill|runbook|change_log|user_preference`: `errors=0` en los cuatro slices.
- `lint.py --strict` sobre los cinco archivos canónicos creados/modificados: `ERROR=0 WARN=0`; parse YAML estricto: PASS.
- `quick_validate.py` se ejecutó como diagnóstico portable y rechazó, según lo esperado por `skill-contract.md`, las keys locales `aliases`, `created`, `entities`, `index_priority`, `indexable`, `load_policy`, `related`, `schema_version`, `scope`, `tags`, `type` y `updated`; no se alteró el contrato AGENTS OS para fabricar un PASS.
- Activación positiva: “revisa la branch de rio-playmaker y sus impactos en RIO” → PASS, aplica `signals-code-review`.
- Activación negativa: “revisa un PR de Echo Forge” → PASS, no aplica esta skill scoped a Meli/Signals.
- Activación adyacente: “arma la descripción del PR de rio-playmaker” → PASS, handoff a [[pr-description]].
- Forward-test sobre el checkout actual de `rio-playmaker`: el baseline detectó `scripts/inactivate-probe/` funcional sin trackear y por contrato la revisión completa debe quedar `BLOCKED` hasta resolver su ownership; smoke independiente de Zord listó 8 reviewers, seleccionó 7 habilitados y completó `assemble --scope branch --dry-run` sin ejecutar agentes ni cambiar el working tree. Resultado del forward-test: PASS.
- Draft→Ready: PASS; skill/runbook separados, fuentes canónicas enlazadas, output explícito y failure modes de base incorrecta, documentación stale, falsos positivos de Zord, búsquedas negativas parciales y scope creep cubiertos.
- `graphify-obsidian update` intentado: bloqueado por dos findings nuevos fuera de este delta (`Sin título.md` sin frontmatter y un proyecto Echo con `status: closed`); el wrapper conservó el último índice válido. Los cinco archivos de esta operación mantienen lint estricto `0/0`.
- Refinamiento solicitado por el owner: validación comportamiento→test, resolución canónica de Zord y ciclo preview→aprobación→publicación agregados. Revalidación posterior: lint estricto `ERROR=0 WARN=0`, schemas `skill|runbook|change_log` con `errors=0`, YAML PASS y forward checks `behavior-over-coverage`, `canonical-zord-resolution`, `owner-gated-publication` y `human-first-comments` en PASS.
- Segundo refinamiento solicitado por el owner: piloto local de reviewer RIO independiente y exclusión absoluta de proyectos no Meli. Pendiente registrar aquí los resultados del check, list, dry-run, lint y schemas posteriores al cambio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** contiene preferencias personales y referencias internas de RIO; no incluye secretos, payloads, credenciales ni dumps.

## Rollback

- Eliminar los dos artefactos canónicos nuevos, retirar la entrada del índice, restaurar la referencia previa en preferencias Meli, quitar la sección personal de [[local-agents-pipeline-cli]] y mover a respaldo o eliminar `~/.config/zords/agents/rjara-rio-impact.md`. La copia legacy bajo Claude no fue modificada.
