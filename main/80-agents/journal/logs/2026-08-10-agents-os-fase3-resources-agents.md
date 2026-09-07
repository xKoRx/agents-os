---
type: change_log
schema_version: 1
scope: session
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 3]]"
application:
entities: []
related: []
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

# 2026-08-10 — AGENTS OS F3 Resources/agents

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / moved
- **Archivo(s):** `30-resources/agents/`, `70-templates/prompt.md`, `80-agents/skills/_shared/schema-contract.md`, `80-agents/skills/INDEX.md`, pack ChatGPT y `xKoRx/symphony/.agents/skills/`.

## Motivo

Se ejecutó el lote local de Fase 3 para normalizar assets portables bajo la topología aprobada y hacer verificable el tipo `prompt`.

## Fuentes usadas

- [[AGENTS OS - Fase 3]]
- [[F3 — Migración de skills]]

## Resolución aplicada

Se creó el dominio `30-resources/agents/` con índice, bitácora, referencias, prompts, examples y skills. Las tres skills portables se movieron sin copias y con hashes preservados. Se añadió el tipo S2 `prompt`, su template y fixture válida. El registry federado y Doctor consumen el nuevo path. `echo-forge-wfm-troubleshooting` y `sqx-temporal-failure-audit` se migraron sin copia a `xKoRx/symphony/.agents/skills/`; se adaptaron al contrato de discovery del repo y sus dependencias relativas resuelven. El pack incluye Fase 3, schema contract y `30-resources/agents/`. La piloto `sqx-plugin-lifecycle` se restauró desde `ea03696` al checkout activo para corregir el target faltante del registry. El owner aceptó G3 el 2026-08-10; F4 quedó habilitada sin iniciar y T4.1 es el próximo paso.

## Validación

- `validate_schema_contract.py`: `errors=0`.
- Lint estricto de las notas canónicas modificadas: `ERROR=0 WARN=0`; gate no-new-debt `new=0`.
- Doctor estricto: `HIGH=0 MEDIUM=0 LOW=0`.
- Pack ChatGPT: `182` archivos, hashes y ZIP válidos.
- Forward-test core/portable/prompt/app-owned: `forward_test_failures=0`; source único y contratos nativos verdes.
- Reindex Graphify correcto; `explain` resuelve el proyecto y el prompt.
- Checksums y rollback registrados en [[F3 — Migración de skills]]; paths anteriores ausentes.
- Aceptación owner: G3 `review→accepted`; cockpit y snapshot externo sincronizados; F4 habilitada con T4.1 pendiente.
- Cierre de aceptación: schema `errors=0`, strict de los seis artefactos tocados `ERROR=0 WARN=0`, Doctor `0/0/0` y pack de 182 archivos válido. El gate global y el reindex final quedaron bloqueados por dos notas concurrentes ajenas a F3 en `30-resources/rio-atlas/architecture/` con `type: reference` no contratado; no se modificaron ni se absorbieron al baseline.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

Mover los tres directorios portables de `30-resources/agents/skills/` de vuelta a `30-resources/agents-skills/`; mover las dos skills app-owned desde el repo owner a sus paths anteriores del vault; restaurar registry, Doctor, memoria interna y pack; retirar la piloto restaurada sólo si el target sigue disponible en la rama autorizada; ejecutar hashes, strict, Doctor, pack, Graphify y forward-test.
