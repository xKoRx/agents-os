---
type: change_log
schema_version: 1
scope: session
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Meli]]"
project: "[[Crear Context]]"
application:
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
related:
  - "[[pr-description]]"
  - "[[signals-code-review]]"
  - "[[Descripciones de PR — recurso del proyecto en el vault]]"
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
  - project/crear-context
---

# 2026-08-24 — Procedimiento de descripciones de PR + PRs de Crear Context

## Qué cambió

**Procedimiento promovido a skill propia.** La mecánica de descripciones de PR vivía como `references/pr-description.md` dentro de `signals-code-review`, una skill de *code review*: para escribir una descripción había que cargar el protocolo de revisión completo. Se promovió a skill independiente.

- Nuevo canónico: `80-agents/skills/pr-description/SKILL.md` (`scope: global`, agent-facing, con Inputs/Procedure/Output/Hard Rules).
- Cara humana nueva: `30-resources/runbooks/Descripciones de PR — recurso del proyecto en el vault.md` — el *por qué* (no en la raíz del repo, template del repo como autoridad, una nota por repo, bloqueantes arriba). No repite el procedimiento.
- Router de cliente: `~/.claude/skills/pr-description/SKILL.md` — puntero al canónico, no copia, siguiendo el patrón de `agents-os-bootstrap` y respetando el skill-contract ("no copiar skills bajo carpetas de cliente").
- `signals-code-review`: su `references/pr-description.md` quedó reducido a puntero; se actualizaron su `description`, su intro y el paso 8.1 para invocar `pr-description` en vez de reimplementar.
- `80-agents/skills/INDEX.md` registró la fila de `pr-description`.

**Descripciones de PR de la iniciativa.** Escritas contra las branches vigentes, con suites corridas en la sesión.

- `10-projects/Meli/Crear Context/Descripción PR — rio-sdk-events.md` — `feature/new-component-context @ aac690d`, base `master @ 9d86eb8`, 2 commits, +463/-10. Suite 696 tests / 0 fallas + `jacocoTestCoverageVerification` PASS.
- `10-projects/Meli/Crear Context/Descripción PR — rio-playmaker.md` — `feature/new-component-context`, base `develop @ 0524ce49e`, **0 commits** (working tree), 13 modificados +288/-11 más 6 nuevos sin trackear. Suite 3.144 tests / 0 fallas / 2 skipped.
- Las dos notas previas, que describían la entrega descartada, se renombraron a `Descripción PR — <repo> (entrega descartada).md`. No se borró nada.

**Nota del proyecto** [[Crear Context]]: tabla de branches vigentes reescrita con estado real, diffstat, suites y enlace a cada descripción; orden de merge explícito (SDK → release `1.4.0` → Playmaker); tabla de entrega de desarrollo corregida (`0.0.2` → `0.0.3-component-context`, Playmaker ya no figura "sin implementación"); estado actual y bitácora actualizados.

## Bloqueantes levantados (no corregidos — son del usuario)

- **rio-playmaker sin commits** y con seis archivos de la feature sin trackear.
- `develop` local **14 commits detrás** de `origin/develop`.
- `build.gradle` de Playmaker pinneado a la versión de prueba `0.0.3-component-context`; el merge exige `1.4.0` publicada desde `master`.
- `docs/specs/swagger.yaml` modificado solo por un newline final: ruido ajeno al cambio.
- SDK: commit HEAD con sujeto `versión`, español y sin conventional commit, contra su propio `CODING_GUIDELINES.md`; `build.gradle` pierde el newline final.
- Enmienda pendiente de SIG-573 pedida por §13 de SIG-590.

## Verificación

- `./gradlew test jacocoTestCoverageVerification` en `rio-sdk-events` — exit 0, 696 tests, 0 fallas, 0 skipped.
- `./gradlew test` en `rio-playmaker` — exit 0, 3.144 tests, 0 fallas, 2 skipped.
- `git status` posterior en ambos repos: sin daño colateral de los builds; el único no trackeado ajeno es `graphify-out/`, preexistente.
- `validate_schema_contract.py` — 0 errores.

## Deuda detectada, no tocada

- `80-agents/skills/signals-spec-authoring` y `~/.claude/skills/signals-spec-authoring` **divergieron**: difieren `SKILL.md` y dos referencias, y la copia de cliente tiene dos archivos que el vault no tiene. Es exactamente el problema que el patrón de router evita; conviene convertir esa skill al mismo patrón.
- `signals-code-review` existe solo en `~/.claude/skills/`, sin canónico en el vault.
