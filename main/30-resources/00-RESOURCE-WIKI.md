---
type: doc
schema_version: 1
status: active
icon: 📚
slug: resource-wiki-schema
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-09-03
aliases:
  - Resource Wiki
  - reglas de la resource wiki
  - LLM Wiki de recursos
  - resource wiki schema
tags:
  - kind/doc
  - kind/system
  - area/personal
  - project/agents-os
---

# 📚 Resource Wiki — Reglas y esquema

Este documento es el **contrato humano** de la wiki compilada que vive en
`30-resources/`: define estructura, autoridad, provenance, freshness y
lifecycle. La **ejecución con criterio** vive únicamente en la skill
`agents-os-resource-wiki`; el reindex y los checks mecánicos viven en su
runbook.

> Origen del patrón: `30-resources/LLM Wiki.md` (idea abstracta). Este doc es la
> instanciación concreta para AGENTS OS. La prueba de concepto viva es
> `30-resources/aranea/` (ya operaba así antes de formalizarlo).

## Propósito

`30-resources/` no es una carpeta de archivos sueltos: es una **wiki que el agente
compila y mantiene incrementalmente**. Cada fuente que entra se lee una vez, se
integra al contenido existente (se actualizan páginas, se cruzan referencias, se
marcan contradicciones) y queda *mantenida*, no re-derivada en cada query.

## Contenido

El contrato cubre capas de autoridad, estructura de dominios, creación de páginas, provenance, freshness, lifecycle, índices, logs, operaciones y fronteras.

## Las tres capas (y por qué Graphify NO compite)

1. **Evidencia fuente** — origen externo resoluble mediante una nota
   `type: source` y, opcionalmente, una captura inmutable bajo `_sources/`. La
   evidencia respalda afirmaciones; no es la síntesis vigente del vault.
2. **La wiki** — páginas Markdown canónicas de Sistema 2 que integran la
   evidencia y mantienen el estado vigente. **Esta es la autoridad para
   responder qué sostiene hoy el vault**, siempre conservando provenance.
3. **Selección curada** — `00-index.md` elige qué páginas abrir y `log.md`
   audita operaciones del dominio. Ninguno reemplaza a las páginas canónicas;
   los logs operacionales quedan fuera de Graphify.
4. **El índice derivado** — Graphify. Grafo reconstruible sobre la wiki para
   navegación, paths y detección de huérfanos/god-nodes. **No es verdad**;
   se puede borrar y regenerar.

> **Modo de operación (decisión 2026-07-03): se trabaja con ÍNDICES, no con capa
> semántica.** El retrieval primario es el `00-index.md` curado. Graphify
> se corre solo en modo `update` (AST, sin LLM, gratis) como índice estructural de
> apoyo. La extracción semántica (`extract --mode deep`) quedó **parqueada** (free
> tier de Gemini insuficiente; solo para proyectos de código vía API cuando se justifique).
>
> **¿Graphify solo-índices aporta o estorba?** APORTA y no estorba, **siempre que** el
> corpus esté limpio (`.graphifyignore`) y se use para lo suyo: lint/auditoría del grafo
> completo (huérfanos, god-nodes), `affected`/`path` y descubrimiento cross-dominio.
> ESTORBA solo si se ensucia o si se usa como capa de retrieval/semántica de markdown
> (ahí ganan tags + índice curado). Arquitectura completa de 4 capas y roles en el ADR
> [[token-economy-indexing-architecture]].

> ⚠️ **Dos "wikis", una sola verdad.** La wiki curada (capa 2, en `30-resources/`,
> fuente de verdad) NO es lo mismo que el modo `--wiki` de Graphify (derivado,
> desechable, en `graphify-out/`). Nunca editar la segunda como si fuera la primera.

### Cómo se potencian (no se pisan)

| | `00-index.md` (wiki) | Grafo (Graphify) |
|---|---|---|
| Resuelve | "¿qué página abro?" | "¿qué se conecta con qué / paths / huérfanos" |
| Naturaleza | curado, determinístico, `grep`-able | derivado, probabilístico |
| A escala de recursos | gana para elegir qué leer | gana para relaciones y lint |

El `00-index.md` da entrada barata y precisa; Graphify da la topología y el
*lint*.

## Estructura de un dominio de wiki

Una subcarpeta temática de `30-resources/` es un **dominio activo** sólo cuando
su raíz cumple este contrato:

```text
30-resources/<dominio>/
├── 00-index.md      # catálogo curado (type: index, desde 70-templates/index.md)
├── log.md           # bitácora cronológica append-only del dominio
├── <páginas>.md     # páginas canónicas (Sistema 2, desde su template)
└── _sources/        # opcional: capturas crudas inmutables, fuera de Graphify
```

- El nombre exacto del entrypoint es `00-index.md`, en minúsculas. No se acepta
  `index.md`, `00-INDEX.md`, `INDEX.md` ni un segundo catálogo raíz.
- El índice raíz declara `type: index` y `status: active`; `log.md` existe desde
  la activación. Un directorio sin ese par sigue siendo una colección, no un
  dominio activo, y el doctor no debe exigirle lifecycle de wiki.
- Dominios activos al 2026-09-13: `agents/`, `applications/` (con `applications/echo/` como subdominio activo desde 2026-09-13, sub-índice propio y bitácora compartida `applications/log.md`), `aranea/`, `grids/`, `knowledges/`, `methodologies/` (con `methodologies/sdd/` como subdominio activo), `rio-atlas/`, `runbooks/` (activado explícitamente 2026-09-12; los runbooks de AGENTS OS viven en `80-agents/memory/public/runbook/`), `tools/` y `vibe-coding/`. `ideas/`, `meetings/`, `sqx/`, `storage/`, `dashboards/` y `agents-os/` mantienen su función propia; no se promueven implícitamente.

## Convenciones de páginas

- **Toda página es Sistema 2 → nace de template** (`70-templates/`). Si falta el
  template, se crea antes o en el mismo cambio (regla dura de la constitución).
- `00-index.md` usa `type: index` y el template `70-templates/index.md`.
- Naming canónico, aliases y slugs según `90-system/convenciones.md`. Los links
  internos apuntan siempre al nombre canónico.
- Una página = una entidad/concepto. No mezclar runbook + skill + memoria en una
  página (ver "Diferenciación de artefactos" en la constitución).
- **Corte estable vs volátil (regla dura para apps/servicios).** Separar en secciones distintas la información *persistente* (responsabilidad, rol, límites de dominio, contratos: cambia solo si cambia el propósito) de la *volátil* (stack, librerías, versiones, infra concreta: se puede cambiar mañana). La sección volátil lleva su propio `last_verified`. Motivo: economía de tokens y freshness — lo volátil se re-verifica sin re-derivar lo estable. Los templates `application.md` y `service.md` ya nacen con este corte.

## Provenance, freshness y confianza

La provenance se modela con links, no con texto ambiguo ni paths de máquina:

1. Cada origen externo relevante tiene una nota desde
   `70-templates/source.md` (`type: source`) con `source_url` o `repo` + `path`.
2. Una página creada o materialmente reescrita por ingest enlaza esas notas en
   `sources`. `type: methodology` y `type: resource` usan sus templates S2.
3. Una captura pesada o literal puede vivir bajo `_sources/`; es inmutable y
   queda fuera del corpus Graphify. Su nota `source` conserva el locator y, si
   aporta, checksum/licencia.
4. Una cita de query apunta a la página canónica consultada; desde allí debe
   poder seguirse la provenance hasta la fuente.

Semántica temporal:

- `updated`: fecha del último cambio material de la página.
- `last_verified`: última fecha en que sus afirmaciones fueron contrastadas
  con las fuentes enlazadas; no se actualiza por formato o backlinks.
- `confidence`: `verified`, `high`, `medium` o `low`. `verified` exige contraste
  directo con una fuente resoluble; las demás expresan fuerza de evidencia, no
  certeza subjetiva.

Freshness es **event-driven**: se verifica al ingerir una fuente que pueda
afectar la página, al responder una query sensible a vigencia o cuando el
dominio declara una cadencia propia. No existe una cadencia global inventada.
Una página sin `last_verified` no está automáticamente inválida; la query debe
declarar el gap si la vigencia cambia la respuesta.

## Reemplazo, deprecación y contradicciones

- La misma entidad se actualiza en su página canónica; una fuente nueva no crea
  una copia `-v2` ni borra evidencia en silencio.
- Una fuente reemplazada pasa a `status: superseded` y enlaza
  `superseded_by`; la nueva puede enlazar `supersedes`. Archivar significa
  retención histórica, no autoridad vigente.
- Si cambia la identidad del concepto, la página anterior usa un estado
  `deprecated` permitido por su tipo y enlaza la reemplazante. El índice raíz
  deja una sola entrada vigente.
- Una contradicción no resuelta conserva ambas afirmaciones con fuente/fecha,
  baja `confidence` cuando corresponda y queda visible en el índice/log hasta
  resolverse.

## `00-index.md` (catálogo)

- Content-oriented: una fila por página vigente, con link + resumen de **una
  línea** + meta útil (`last_verified`, `confidence` o source count cuando
  cambie la selección).
- Se actualiza en **cada ingest**. Un índice desactualizado es deuda, no adorno.
- Debe ser `grep`-able y legible de un vistazo. Es lo primero que lee el agente
  antes de abrir páginas.

## Escalado del índice (plano → jerárquico)

Un `00-index.md` plano (una fila por página) es lo correcto **mientras siga siendo
`grep`-able y legible de un vistazo**. Cuando un dominio crece, un índice plano deja de
filtrar barato (capa 1) y empieza a entrar entero al contexto — el opuesto de la economía
de tokens. Ahí se **escala a sub-índices jerárquicos**, como ya hace `aranea/`
(`01-topologia/`, `02-servicios/`, `03-storage/`…), cada uno con su propio `00-index.md`.

Umbral (smell-test, no regla dura):

- **Plano** hasta ~15–20 páginas o mientras el índice quepa cómodo en una lectura.
- **Escalar** cuando: (a) el índice supera ~20 filas o deja de leerse de un vistazo;
  (b) emergen sub-dominios naturales (agrupaciones que se consultan juntas); o
  (c) el `00-index.md` por sí solo ya no cabe en un presupuesto de capa 1 razonable.

Cómo escalar:

1. `00-index.md` raíz del dominio pasa a ser un **índice de índices**: una fila por
   sub-dominio con link a su `00-index.md` + una línea de qué agrupa.
2. Cada sub-dominio es una subcarpeta con su `00-index.md`; comparte el
   `log.md` raíz salvo que se active explícitamente como dominio independiente.
3. La navegación sigue siendo cheapest-first: raíz → sub-índice → página → cuerpo.
   Nunca se salta un nivel (misma disciplina que las 4 capas del [[context-router]]).

Regla anti-drift: escalar el índice **no** duplica contenido — mueve filas a su
sub-índice y deja en la raíz solo el puntero. Un dominio nunca debe tener dos catálogos
que compitan (ver frontera "una fuente por hecho").

## `log.md` (bitácora)

- Append-only, cronológico. Prefijo consistente para parsear con unix:
  `## [YYYY-MM-DD] <op> | <detalle>` donde `<op>` ∈ `ingest | query | lint`.
- `grep "^## \[" log.md | tail -5` → últimas 5 operaciones.
- Registra qué fuente entró, qué páginas tocó y qué se decidió. No es el
  `change_log` público (eso vive en `80-agents/journal/logs/` para cambios canónicos).
- No impone actividad por calendario. Registra eventos reales; un dominio sin
  operaciones recientes puede seguir sano.

## Operaciones (detalle en la skill)

- **Ingest** — entra una fuente → leer → integrar en páginas → actualizar
  `00-index.md` → append a `log.md`.
- **Query** — responder desde la wiki (index → páginas → síntesis con citas).
  Las buenas respuestas se archivan como nuevas páginas (compounding).
- **Lint** — salud periódica: huérfanos, contradicciones, stale, conceptos sin
  página. Se apoya en Graphify. Parte mecánica en el runbook
  `resource-wiki-lint-reindex`.

## Fronteras (qué NO hacer)

- No dejar que las páginas wiki se vuelvan **fuente paralela** que driftea de los
  docs canónicos ya existentes: la página *es* el doc canónico, no una copia.
- No meter secretos, credenciales ni dumps pesados (constitución).
- No indexar `_sources/`, `trash/`, `*.json` ni salidas de Graphify (ver
  `.graphifyignore`).
- No confundir la wiki curada con el `--wiki` derivado de Graphify.

## Links

- [[LLM Wiki]] — idea original del patrón.
- [[graphify]] — índice derivado.
- [[agents-os]] — guía operativa.
- [[agent-constitution]] — regla canónica de la resource wiki y de templates.
- `30-resources/aranea/00-index.md` — implementación de referencia.
- [AGENTS OS y estructura del vault](agents-os/README.md) — instalación,
  packaging y distribución portable.
