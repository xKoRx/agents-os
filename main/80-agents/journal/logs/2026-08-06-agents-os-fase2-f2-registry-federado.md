---
type: change_log
scope: public
created: 2026-08-06
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Fase 2]]"
  - "[[agents-os-doctor]]"
confidence: verified
load_policy: manual
indexable: false
tags:
  - kind/changelog
  - action/refactor
  - project/agents-os
  - scope/public
---

# Change log — AGENTS OS Fase 2 · Skills por ownership (registry federado)

Ejecución de Fase 2 (T2.1–T2.4). Objetivo: registry federado + ownership sin
duplicar skills ni romper discovery. Doctor estricto verde
(`HIGH=0 MEDIUM=0 LOW=0`, startup ≈4948).

## Decisión rectora

**D14** (owner): las skills transversales (ni core AGENTS OS ni de una app)
viven **in-vault** en `30-resources/agents-skills/`, registradas en el INDEX
federado (enlaza, no copia). Conocimiento de metodologías → `30-resources/methodologies/`
(F4). El vault `80-agents/skills/` queda solo con core agents-os (+ vault-ops).
Corrige una lectura previa que asumía un repo externo `agent-skills`.

## Cambios

1. **Ownership (T2.1)** — clasificadas 32 skills: 26 core `agents-os-*`;
   `operational-healthcheck-policy` reclasificada a **vault-ops core** (es sobre
   la salud del propio Second Brain, no transversal); `sync-local-branch`
   transversal; `fury-lib-consumer-deploy` metodología Fury cross-app; 3 de
   Echo Forge/SQX app-owned.

2. **Extracción de transversales (T2.3, D14)** — movidas sin copia:
   - `80-agents/skills/sync-local-branch/` → `30-resources/agents-skills/sync-local-branch/`
   - `80-agents/skills/fury-lib-consumer-deploy/` → `30-resources/agents-skills/fury-lib-consumer-deploy/`
   Ambas usan paths vault-root (no `../`), así que sus refs internas no se rompen.

3. **INDEX federado (T2.2)** — `80-agents/skills/INDEX.md` reorganizado: catálogo
   core arriba + sección "Registro federado" con (a) transversales en
   `30-resources/agents-skills/` y (b) app-owned Echo Forge/SQX con owner destino
   marcado como bloqueado. Los 2 links movidos apuntan a la nueva ruta.

4. **Doctor federation-aware** — `agents-os-doctor/scripts/doctor.py`:
   - `check_skill_index`: regex de skills del core anclado a
     `80-agents/skills/([^/]+)/SKILL.md` (antes `skills/...`, que capturaba por
     error `agents-skills/`).
   - Nuevo check: los targets federados `30-resources/agents-skills/*/SKILL.md`
     del INDEX deben resolver en disco.

5. **Refs vivas actualizadas** (assert "sin romper refs"):
   - `10-projects/Automatización despliegue FURY.md` (2 wikilinks) → nueva ruta.
   - `80-agents/memory/internal/agent-memory/2026-07-15-local-branch-sync-continuity.md`
     (puntero "Skill canónica") → nueva ruta.
   - Journal logs históricos y `outputs/` (pack derivado) se dejan como están
     (historia/derivados; el pack se regenera).

## No ejecutado / gaps para aceptar G2

- **Forward-test multisuperficie** (assert G2 "Codex + otra superficie
  descubren core y piloto"): no ejecutable en esta sesión no-interactiva
  (no puedo lanzar un proceso fresco de Codex/Claude). Gap documentado.
- **Migración de 3 skills app** (`echo-forge-wfm-troubleshooting`,
  `sqx-temporal-failure-audit`, `sqx-plugin-lifecycle`) a su repo owner:
  bloqueada — repo owner de Echo Forge/SQX no hallado en `~/fuentes/`.
- **Nesting físico del core** descartado (D14): innecesario para separar
  ownership; era la parte de mayor blast radius.

## Verificación

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py --strict
# → HIGH=0 MEDIUM=0 LOW=0 startup_tokens≈4948 ; exit 0
# 32 targets del INDEX resuelven (incl. 2 en 30-resources/agents-skills/)
```
