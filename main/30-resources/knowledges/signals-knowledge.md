---
type: resource
schema_version: 1
status: deprecated
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
sources:
  - "[[signals-knowledge-repo]]"
related:
  - "[[RIO]]"
  - "[[Onboarding Signals]]"
  - "[[Signals Knowledge Harness]]"
  - "[[ads-signals-catalog]]"
  - "[[ads-signals-frontend]]"
last_verified: 2026-08-18
confidence: low
aliases:
  - signals-knowledge
  - Signals Platform Knowledge Bundle
  - Signals Knowledge Bundle
  - knowledge bundle de Signals
tags:
  - kind/resource
  - area/meli
  - tech/okf
created: "2026-08-18"
updated: "2026-09-01"
---

# signals-knowledge

## Síntesis vigente

- **Lifecycle:** knowledge reemplazada el 2026-09-01 por [[ads-signals-knowledge-library]]. Esta nota se conserva como registro histórico y ya no debe usarse como punto de entrada vigente.
- **Qué es:** repositorio externo de **conocimiento curado** del equipo Signals (Ads, MercadoLibre), en formato **OKF** (Open Knowledge Format): un árbol de Markdown con frontmatter YAML y links relativos, navegable por humanos y agentes. Es una **aplicación Fury** (`.fury` → `application_name: signals-knowledge`), no un servicio en runtime: su producto es el conocimiento mismo.
- **Autor / dueño:** **Carlos Montecinos** (`cmontecinos`, Software Expert — Advertising); escribió el bundle inicial (2026-08-18).
- **Rol dentro de mi vault:** es un **external-resource**, la extensión externa de mi Resource Wiki (`30-resources/`). Es el **espejo canónico del equipo** de lo que yo documento por mi cuenta en el onboarding — por lo tanto es la referencia contra la cual **validar** lo que tengo en `30-resources/applications/`, `30-resources/rio-atlas/`, etc. Cuando mi entendimiento avanza, el destino de ese conocimiento es este repo (vía PR); esta nota es el **puntero canónico** al repo, no una copia de su contenido (evitar drift).
- **Decisión histórica 2026-08-18:** este repo fue la fuente canónica del equipo hasta ser sustituido por [[ads-signals-knowledge-library]] el 2026-09-01.
- **Dominio que cubre (áreas OKF del bundle):** `rio/` (Playmaker + Control Planes, el core técnico), `signals-catalog/` (fuente de verdad de señales), `signals-collector/` (ingesta/recolección de eventos), `signals-sdk-go/` (SDK Go), `signals-cli/`, `signals-migrator/` (migración desde Melidata) y `signals-frontend/` (UI). Taxonomía de `type` en frontmatter OKF: `Bundle Index` · `Service` · `Concept` · `SDK`.
- **Mi rol como contribuidor:** entro por **backend**, luego reviso **frontend** y probablemente más adelante **ingesta (collector)**. Toda iniciativa de Signals debería terminar con un PR acá — tanto el resultado de la iniciativa como el conocimiento nuevo descubierto en el camino.
- **Cómo se contribuye:** editar/agregar `.md` respetando OKF (frontmatter + links relativos) y abrir PR. El repo tiene hook de `pre-commit` **sin** `.pre-commit-config.yaml`, así que los commits requieren `PRE_COMMIT_ALLOW_NO_CONFIG=1 git commit -m "..."`.
- **Gobierno y harness:** el trabajo de proponer una **harness de contribución para agentes** (AGENTS.md + skills, gobernada por LLM Wiki, portable a agentes de otros devs sin AGENTS OS) vive en el proyecto [[Signals Knowledge Harness]].
- **Futuro:** este es el primer external-resource de tipo *knowledge bundle*; el dominio `30-resources/knowledges/` queda listo para referenciar otras knowledges cuando aparezcan (ver `00-index.md`).

## Evidencia y provenance

- **Fuente:** [[signals-knowledge-repo]] — `repo: signals-knowledge` · `path: signals-knowledge` (relativo a [[Fuentes — Workspace de repositorios]] = `~/fuentes`). Invariante 12: el repo vive fuera del vault; acá solo el puntero.
- **Archivos leídos (2026-08-18):** `README.md`, `index.md` (`type: Bundle Index`, `timestamp: 2026-07-30`), `.fury`, y el árbol de dominios (`find -maxdepth 2`).
- `last_verified: 2026-08-18` · `confidence: high` (contrastado directo contra el repo en `~/fuentes/signals-knowledge`).

## Límites y contradicciones

- **Estado del bundle:** el propio README lo marca como **versión inicial, en construcción**; falta contenido en varias áreas (los `index.md` de cada dominio existen, el detalle profundo aún no).
- **Solapamiento con mi Resource Wiki (a reconciliar, no a duplicar):** el bundle cubre el mismo dominio que mis notas de `30-resources/applications/` (rio-*, [[ads-signals-catalog]], [[ads-signals-frontend]]) y `30-resources/rio-atlas/`. La tarea de *validar lo del repo vs lo que investigué* es de contraste; los hallazgos que corrijan el bundle salen como PR allá, y los que corrijan mi vault se actualizan acá siguiendo la Resource Wiki. Ninguna de las dos wikis es copia de la otra.
- **`signals-collector`:** el bundle lo trata como área de primer nivel (ingesta), pero **no tengo aún nota de app propia** para el collector en `30-resources/applications/` — gap conocido de mi onboarding (mi entrada futura por ingesta).
- **Taxonomía distinta:** los `type` OKF (`Bundle Index/Service/Concept/SDK`) no mapean 1:1 a los tipos S2 de mi vault (`application/service/concept/...`); al contrastar, traducir en vez de asumir equivalencia.
