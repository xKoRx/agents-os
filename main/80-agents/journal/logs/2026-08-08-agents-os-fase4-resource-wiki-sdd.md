---
type: change_log
scope: session
created: 2026-08-08
updated: 2026-08-08
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 2]]"
application:
entities:
  - "[[AGENTS OS - Fase 2]]"
  - "[[30-resources/methodologies/sdd/overview|SDD — Overview]]"
related:
  - "[[30-resources/methodologies/sdd/00-index|Spec-Driven Development — Índice]]"
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
  - project/agents-os
  - change/created
---

# Fase 4 — Resource Wiki + dominio y workflow SDD

## Cambio

- **Tipo:** created / updated / conflict-resolution
- **Contrato y schema:** `30-resources/00-RESOURCE-WIKI.md`,
  `90-system/convenciones.md`, `.graphifyignore`, templates `resource.md` y
  `source.md`, skills `agents-os-resource-wiki` y `agents-os-doctor`.
- **Dominio:** `30-resources/methodologies/` y
  `30-resources/methodologies/sdd/` (índices, logs, seis metodologías y cinco
  notas source).
- **Skill:** `30-resources/agents-skills/sdd-workflow/` + registro federado en
  `80-agents/skills/INDEX.md`.
- **Casing/lifecycle:** `vibe-coding/00-index.md` y
  `aranea/03-storage/backup-dr/00-index.md`, referencias vivas asociadas,
  `aranea/log.md` y normalización del dominio Vibe Coding a [[Personal]].
- **Control:** [[AGENTS OS - Fase 2]].

## Motivo

- Ejecutar F4 con una fuente canónica por responsabilidad: contrato humano,
  skill de Resource Wiki, metodología SDD reusable, skill ejecutable transversal
  y specs concretas en sus repositorios.
- Cerrar ambigüedad entre fuente cruda y síntesis vigente, y hacer provenance,
  freshness/confidence y reemplazo verificables.

## Fuentes usadas

- [[AGENTS OS - Fase 2]] (D7, D8, D14 y paquete F4).
- [[LLM Wiki]] y `30-resources/00-RESOURCE-WIKI.md`.
- GitHub Spec Kit oficial:
  `https://github.com/github/spec-kit/blob/main/docs/reference/agentic-sdd.md`.
- Kiro Specs oficial: `https://kiro.dev/docs/specs/`.
- Repo `xKoRx/symphony`: `CONSTITUTION.md`, `.agents/rules/08-10`,
  `.agents/skills/sdd-*`, `vibe-coding/SDD.md` y `docs/sdd/`.

## Resolución aplicada

- Evidencia fuente respalda; páginas wiki mantienen la síntesis vigente;
  `00-index.md` selecciona; Graphify deriva relaciones.
- Dominio activo = `00-index.md` lowercase + `log.md`; logs y `_sources/`
  quedan fuera de Graphify.
- Freshness es event-driven y `last_verified` sólo cambia tras contraste real.
- `docs/sdd/` de Symphony quedó `superseded`: declara bootstrap pendiente,
  mientras el runtime vivo ya contiene constitution, reglas, skills y specs.
- `sdd-workflow` vive como transversal federada bajo
  `30-resources/agents-skills/` (D14); no duplica las páginas metodológicas.
- El contrato Resource Wiki exige `00-index.md`, rechaza las variantes legacy
  `index.md`, `00-INDEX.md` e `INDEX.md`, y registra `methodologies/` con su
  subdominio activo `methodologies/sdd/`.
- `_shared/skill-contract.md` separa el perfil OpenAI portable del perfil
  federado AGENTS OS: las claves S1 extendidas se conservan y se validan con el
  gate federado equivalente.
- No se copiaron specs concretas de Symphony al vault.

## Validación

- Templates S2: `ERROR=0 WARN=0 notes_scanned=19`.
- Dominio SDD seleccionado: `ERROR=0 WARN=0 notes_scanned=13`.
- Skill federada: lint exacto `ERROR=0 WARN=0 notes_scanned=1`; frontmatter y
  UI YAML parseables; `default_prompt` referencia `$sdd-workflow`; 112 líneas.
- `quick_validate.py` ejecutado con Python 3.10.16 y 3.12.9: exit 1 esperado en
  ambos por `created, scope, tags, type, updated`. Es el perfil portable
  estándar y no aplica como gate a la skill federada canónica; la
  incompatibilidad y el gate equivalente están formalizados en
  `_shared/skill-contract.md`.
- Contrato Resource Wiki: seis dominios/subdominios activos verificados con
  `00-index.md + log.md`; casing e inventario canónico consistentes.
- Doctor estricto: `HIGH=0 MEDIUM=0 LOW=0 startup_tokens≈4979`.
- Gate all-vault warn-first: `ERROR=237 WARN=84 notes_scanned=484`; deuda
  preexistente, no bloquea update.
- Graphify update: exit 0, `5465 nodes / 6284 edges`.
- Query SDD recuperó lifecycle, índice y notas source GitHub/Kiro entre los
  primeros resultados.
- Assert de no duplicación: ninguna ruta concreta
  `specs/FEAT-*/(SPEC|PLAN|TASKS|VERIFICATION).md` en el dominio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin paths locales persistidos ni secretos; los repos
  externos usan `repo + path` y las fuentes públicas usan URL resoluble.

## Rollback

- Eliminar `30-resources/methodologies/` y
  `30-resources/agents-skills/sdd-workflow/`; retirar su fila del registry.
- Revertir contrato/templates/ignore/skills a la versión previa y restaurar el
  casing legacy de índices sólo si un consumidor no reparable lo exige.
- Quitar `aranea/log.md` y revertir las referencias mecánicas asociadas.
- Reindexar Graphify y devolver G4 a `pending`.
