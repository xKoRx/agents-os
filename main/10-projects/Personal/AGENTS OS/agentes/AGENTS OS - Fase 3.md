---
type: project
schema_version: 1
owner: agent
root: false
status: completed
cssclasses:
  - wide
priority: P0
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-08-08
due:
progress: 100
repo:
jira:
prs:
aliases:
  - AGENTS OS Fase 3
  - AGENTS OS Executable Schema
  - AGENTS OS Metadata Retrieval
related:
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
tags:
  - area/personal
  - kind/project
  - project/agents-os
created: 2026-08-08
updated: 2026-08-11
---

# AGENTS OS - Fase 3

> [!info]+ Schema ejecutable y retrieval por metadata
> **Padre:** [[AGENTS OS]] · **Owner:** agent · **Estado:** completed · **Prioridad:** P0 · **Gate actual:** G6 `accepted` · **Fase actual:** F6 completa; T6.1–T6.6 Done
>
> Esta iteración convierte templates, frontmatter, tags y Graphify en un
> contrato coherente y ejecutable. Hereda sólo la deuda explícita de
> [[AGENTS OS - Fase 2]]; no repite sus baselines, decisiones ni pruebas ya
> aceptadas.

## Motivación

Fase 2 dejó autoridades únicas, schemas S1/S2, lint all-vault, Graphify
vault-aware, skills federadas y un piloto de layout validado. El sistema ya es
operable, pero todavía depende demasiado de disciplina manual:

- una nota puede crearse sin template o con un frontmatter incompleto;
- el lint conoce reglas codificadas que pueden divergir de templates y schema;
- no existe una versión de contrato que permita evolucionar un template sin
  confundir notas antiguas con notas nuevas;
- los tags no tienen una política suficientemente verificable para servir de
  filtro confiable;
- las skills portables viven en `30-resources/agents/skills/`, mientras prompts
  y otros assets de agentes no tienen una topología común;
- Graphify relaciona wikilinks y usa aliases para resolverlos, pero no proyecta
  el frontmatter general ni ofrece filtros por metadata/tags;
- el Context Router usa metadata como Layer 0 fuera del grafo, por lo que la
  selección determinística todavía está fragmentada;
- la deuda heredada mantiene el gate global en `warn-first`.

La meta no es agregar otra capa semántica opaca. Es construir retrieval local,
explicable y agnóstico al modelo: metadata confiable reduce candidatos, el
grafo explica relaciones y el cuerpo Markdown se abre sólo al final.

## Descripción y contexto

### Punto de partida aceptado

- [[AGENTS OS - Fase 2]] terminó con G7 `accepted`, doctor estricto `0/0/0`,
  Graphify funcional y rescan path-based validado por el owner.
- Lint heredado: `41 ERROR / 84 WARN` sobre el corpus live.
  - 35 `unknown-type`.
  - 3 `bad-status`.
  - 2 `missing-field`.
  - 1 `bad-owner`.
  - 81 notas sin frontmatter y 3 con frontmatter sin `type`.
- De los 41 errores, 37 están en Aranea; los cuatro restantes están en Echo
  Forge, Destaques de Precio y dashboards Echo Forge.
- Skills app-owned pendientes de mover al repo `xKoRx/symphony`:
  `echo-forge-wfm-troubleshooting` y `sqx-temporal-failure-audit`.
- El layout `10-projects/Personal/AGENTS OS/` ya pasó un piloto real. Falta un
  segundo piloto antes de generalizar movimientos por área.
- El gate all-vault permanece `warn-first`; el flip estricto sólo es válido con
  `ERROR=0` y warnings resueltos o excluidos por contrato.

### Lo que se entiende por “usar template”

No es posible demostrar retrospectivamente que un archivo fue creado mediante
un botón o comando de template. El contrato verificable será **conformidad**:

1. cada `type` creable tiene exactamente un template canónico;
2. cada nota nueva declara el tipo y la versión de schema aplicable;
3. el lint compara su frontmatter y estructura contra ese contrato;
4. cambios de versión requieren migración explícita, no drift silencioso.

### Envelope común y extensión por tipo

Todos los tipos nuevos compartirán un envelope mínimo. No se copiarán campos
vacíos que no cambian routing, lifecycle o retrieval.

```yaml
type: <canonical-type>
schema_version: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
aliases: []
tags:
  - kind/<canonical-type>
```

- Sistema 1 extiende con `scope`, `load_policy`, `indexable`, prioridad y
  routing de memoria cuando corresponda.
- Sistema 2 extiende con `status`, `area`, `parent`, `owner`, `project`,
  `application`, `entities`, `related` u otros campos sólo cuando tienen
  semántica definida.
- `type` y links canónicos contienen semántica; tags son slugs técnicos para
  filtros. Un tag no reemplaza un campo canónico.

### Topología objetivo de recursos para agentes

```text
30-resources/
└── agents/
    ├── 00-index.md
    ├── skills/
    ├── prompts/
    ├── references/
    └── examples/
```

Fronteras de ownership:

- `80-agents/skills/`: runtime core y vault-ops de AGENTS OS.
- `30-resources/agents/skills/`: skills portables/transversales del Second Brain.
- `<repo>/.agents/skills/`: skills propiedad de una aplicación.
- `30-resources/agents/prompts/`: prompts reusables; los procedimientos con
  decisiones, validación o lifecycle siguen siendo skills.

Resources seguirá organizado por dominio estable, no como espejo obligatorio
de Areas. El routing de área vive en frontmatter y links. Sólo se permite una
subcarpeta por área cuando existe ownership exclusivo, estable y documentado.

### Modelo Graphify objetivo

Graphify seguirá siendo índice derivado. Markdown, templates y contratos son
la fuente de verdad.

- Proyectar en el nodo de archivo metadata seleccionada: `type`,
  `schema_version`, `status`, `scope`, `area`, `project`, `application`,
  `entities`, `tags`, `confidence`, `load_policy`, `index_priority`, `updated`.
- Usar tags como facets/filtros invertidos; no crear indiscriminadamente un
  nodo/edge por tag que produzca supernodos.
- Convertir links canónicos del frontmatter en edges tipados determinísticos:
  `in_area`, `child_of`, `in_project`, `for_application`, `about`,
  `related_to`, `supersedes`.
- Reutilizar las exclusiones reales de `.graphifyignore`; ningún extractor
  auxiliar debe volver a introducir trash, outputs, fixtures o journal.
- Exponer filtrado local por metadata antes de búsqueda lexical o traversal.
- Mantener compatibilidad con `query`, `explain`, `path`, `affected` y
  `references`.

### Context Router objetivo

```text
intent + entidad
      ↓
metadata/type/tags (filtro local determinístico)
      ↓
índice curado + aliases
      ↓
Graphify: links y edges tipados
      ↓
búsqueda lexical sobre candidatos
      ↓
cuerpo Markdown de las pocas fuentes seleccionadas
```

Esto sustituye la dependencia de una API semántica para la mayoría de los
casos de retrieval conocidos. No pretende inferir equivalencia semántica
arbitraria: las preguntas difusas siguen usando búsqueda lexical y juicio del
agente sobre un conjunto ya reducido.

## 🎯 Objetivo

- Garantizar que toda nota nueva o modificada sea conforme a un template y a
  un schema versionado.
- Tener una fuente canónica por contrato de tipo y evitar drift entre schema,
  templates y lint.
- Hacer del lint un gate preventivo: no entra deuda nueva aunque exista deuda
  legacy explícita durante la migración.
- Normalizar `30-resources/agents/` para skills portables, prompts y assets
  reusables sin mezclar runtime core ni ownership de aplicaciones.
- Definir una política PARA/CODE para Resources: dominio físico estable,
  routing por área en metadata y excepciones justificadas.
- Extender Graphify con metadata, facets y relaciones de frontmatter.
- Hacer que Context Router use esa capa local como selección primaria sin
  convertir Graphify en fuente de verdad.
- Absorber y cerrar la deuda heredada de Fase 2 sin repetir trabajo aceptado.
- Llegar a un gate all-vault estricto sólo con evidencia `ERROR=0` y sin
  ocultar residuos mediante exclusiones genéricas.

## Resultados verificables

1. Cada tipo live/creable tiene contrato y template canónico, o una exención
   explícita como fragmento/derivado.
2. Notas nuevas/modificadas fallan si falta frontmatter, `type`, versión,
   campos o tags requeridos.
3. Fixtures prueban tipos válidos, inválidos, versiones, tags, paths y
   estructura mínima.
4. `30-resources/agents/` contiene índice, skills portables y contrato de
   prompts; no quedan copias en el path anterior.
5. Las dos skills app-owned pendientes viven sólo en `xKoRx/symphony` y el
   registry federado las resuelve.
6. Graphify almacena metadata seleccionada en nodos de archivo y filtra por
   ella sin leer cuerpos.
7. Frontmatter con links canónicos produce edges tipados verificables; tags
   funcionan como facets y no como supernodos.
8. Context Router recupera casos fact/relation/domain con metadata→grafo→body
   y conserva fallback degradado.
9. Un agente fresco resuelve el proyecto, una skill, un prompt, una memoria y
   una entidad usando el nuevo pipeline.
10. El corpus acordado llega a `ERROR=0`; warnings quedan corregidos o
    excluidos con regla específica y auditable antes del flip estricto.

## Alcance

- Contrato común, versionado y ejecutable de templates S1/S2.
- Templates actuales y futuros bajo `70-templates/` y `80-agents/templates/`.
- Lint all-vault y gate de notas nuevas/modificadas.
- Reorganización acotada de recursos de agentes.
- Migración de las dos skills Echo Forge/SQX pendientes a su repo owner.
- Fork y wrapper `graphify-obsidian`.
- Context Router, contrato Graphify y pruebas multisuperficie.
- Deuda residual exacta heredada desde Fase 2.
- Segundo piloto de layout por área.

## Fuera de alcance

- Embeddings, vector DB o APIs semánticas pagadas.
- Reescribir cuerpos de notas sólo para uniformar estilo.
- Reorganizar todo `30-resources/` por área en un único movimiento.
- Convertir cada tag en un nodo del grafo.
- Inferir owners, estados, tipos o fechas sin evidencia.
- Mover runtime core fuera de `80-agents/skills/`.
- Copiar skills app-owned al vault para facilitar discovery.
- Sustituir Markdown por Graphify, JSON o una base de datos como autoridad.
- Repetir gates F0–F7 ya aceptados en [[AGENTS OS - Fase 2]].

## Requerimientos

| ID | Requerimiento | Evidencia de aceptación |
|---|---|---|
| R1 | Envelope común para todo tipo nuevo | contrato versionado + fixtures |
| R2 | Extensiones por tipo sin YAML ceremonial | matriz de campos required/optional/forbidden |
| R3 | Exactamente un template canónico por tipo creable | auditoría template↔type sin duplicados |
| R4 | Versionar schema/template | upgrade y nota legacy probados |
| R5 | Lint derivado del contrato, no tabla paralela informal | tests detectan drift template/schema/lint |
| R6 | Gate duro para notas nuevas/modificadas | fixture/archivo nuevo inválido bloquea |
| R7 | Baseline legacy no permite findings nuevos | comparación reproducible y fail-on-new |
| R8 | Tags mínimos, permitidos y coherentes | lint de `kind/`, routing y duplicados |
| R9 | Topología `30-resources/agents/` | move map, rollback y refs verdes |
| R10 | Ownership de skills respetado | core/vault-portable/app-owned sin copias |
| R11 | Contrato y template para prompts reusables | prompt fixture + índice |
| R12 | Resources domain-first con routing de área | convención y piloto, sin árbol espejo masivo |
| R13 | Metadata proyectada en file nodes Graphify | asserts sobre graph.json/API local |
| R14 | Tags como facets, no edges globales | filtros correctos y sin supernodos |
| R15 | Links de frontmatter como edges tipados | path/affected sobre fixtures y vault |
| R16 | Exclusiones únicas y consistentes | trash/outputs/journal ausentes del corpus |
| R17 | Context Router consume metadata→graph→body | E2E fact/relation/domain |
| R18 | Operación sin API semántica | cold run offline/local reproducible |
| R19 | Compatibilidad de comandos Graphify | query/explain/path/affected sin regresión |
| R20 | Cierre de deuda heredada | lint final y ledger por decisión |
| R21 | Segundo piloto de layout | identidad, links, caches y rollback validados |
| R22 | Flip estricto sólo con corpus limpio | gate bloquea fixture real y update sano pasa |
| R23 | Deduplicación de links preserva relación tipada | un `references` previo no suprime `depende_de` |
| R24 | Operaciones Graphify resuelven aliases de frontmatter | canonical y alias seleccionan el mismo file node |
| R25 | Templates y fixtures no forman parte del corpus live | reindex con 0 nodos bajo sus paths y contrato/materializador verdes |
| R26 | Materialización fail-closed sin acoplamiento global | drift ajeno aislado; drift del tipo pedido bloquea |

## Decisiones vigentes

| ID | Decisión | Estado |
|---|---|---|
| D1 | Conformidad verificable importa más que probar el acto histórico de usar template | accepted |
| D2 | Envelope común + extensión por tipo; no frontmatter idéntico lleno de vacíos | accepted |
| D3 | `type` + `schema_version` identifican el contrato aplicable | accepted |
| D4 | Markdown/templates son autoridad; lint y Graphify son implementaciones derivadas | accepted |
| D5 | New/changed strict primero; legacy se migra sin permitir deuda nueva | accepted |
| D6 | `30-resources/agents/{skills,prompts,references,examples}` es la topología objetivo | accepted |
| D7 | Resources se organiza domain-first; área viaja en metadata/links salvo ownership exclusivo | accepted |
| D8 | Runtime core queda en `80-agents/skills/`; app-owned vive en el repo | accepted |
| D9 | Tags son facets; sólo campos con links canónicos generan edges | accepted |
| D10 | Graphify no se convierte en autoridad ni semantic DB | accepted |
| D11 | Retrieval local metadata+grafo+lexical reemplaza la dependencia de API, no toda inferencia semántica | accepted |
| D12 | No hay flip estricto ni exclusión amplia mientras persista deuda no clasificada | accepted |
| D13 | La deduplicación Graphify es relation-aware o da precedencia al edge tipado sobre `references` | accepted |
| D14 | Economía de Tokens es invariante: contrato/lint filtran programáticamente y no agregan lecturas amplias ni cuerpos al hot path | accepted |
| D15 | Templates y fixtures son inputs de creación/validación por filesystem, no evidencia ni nodos Graphify | accepted |
| D16 | Create valida envelope + tipo/template solicitado; el auditor global corre en cambios de contrato, Doctor y release | accepted |

## Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Schema, template y lint vuelven a divergir | deuda silenciosa | contrato machine-readable único + contract tests |
| Actualizar template invalida notas antiguas | migración masiva accidental | `schema_version` y migradores explícitos |
| Gate estricto bloquea por deuda legacy | pérdida de operabilidad | strict en new/changed + baseline exacto temporal |
| Baseline se vuelve allowlist eterna | deuda congelada | ledger decreciente; ningún finding nuevo; gate final G6 |
| Tags crean supernodos Graphify | paths ruidosos | facets invertidos, no edges genéricos |
| Frontmatter genera relaciones falsas | retrieval incorrecto | sólo campos tipados con links canónicos |
| Un link genérico previo suprime el edge tipado al mismo target | relación real invisible | deduplicar por target+relation o promover el edge tipado |
| `explain` no resuelve aliases aunque wikilinks sí | routing inconsistente | índice de aliases compartido por resolución y consultas |
| Graphify reintroduce paths ignorados | ruido/alias collisions | un solo corpus resolver honrando `.graphifyignore` |
| Move de `agents-skills` rompe discovery | skills invisibles | move map, checksums, registry update y forward-test |
| Duplicar skill app-owned en vault/repo | dos autoridades | move sin copia + checksum + assert de source único |
| Organizar Resources por área duplica dominios | moves y ambigüedad | domain-first; excepción explícita y estable |
| Metadata excesiva aumenta tokens | hot path más caro | proyección selectiva; filtros antes de cuerpos |
| Fork Graphify difícil de mantener | deuda operacional | tests aislados, changelog de fork y rollback de wheel |
| Drift de un template bloquea cierres no relacionados | pérdida de continuidad | validación scoped en create + auditor global separado |

## Roadmap dependency-ordered

| Fase | Resultado | Gate |
|---|---|---|
| 0 | Plan, baseline heredado y decisiones cerradas | G0 |
| 1 | Contrato versionado + cobertura de templates | G1 |
| 2 | Lint preventivo, fixtures y no-new-debt gate | G2 |
| 3 | Topología Resources/agents + skills/prompts | G3 |
| 4 | Graphify con metadata, facets y edges tipados | G4 |
| 5 | Context Router integrado y E2E local | G5 |
| 6 | Retrofit residual, segundo piloto y gate estricto | G6 |

## Paquetes autónomos

### Fase 0 — Handoff y contrato de ejecución

**Misión:** crear el planner único, transferir sólo deuda viva de Fase 2 y
congelar las decisiones que evitan retrabajo.

**Implementación:**

1. Cerrar [[AGENTS OS - Fase 2]] como proyecto completado.
2. Registrar baseline heredado `41/84`, dos skills y segundo piloto.
3. Crear tarea puente única en [[AGENTS OS]].
4. Validar título, parent, frontmatter y ausencia de duplicados.
5. Dejar G0 en review sin iniciar implementación estructural.

**Tests:** lint dirigido `0/0`; Graphify resuelve título y alias después del
reindex; parent contiene una sola tarea puente Fase 3.

**Rollback:** borrar sólo la entidad Fase 3 recién creada y restaurar los
punteros del parent/continuidad; no revertir entregables Fase 2.

### Fase 1 — Contrato versionado y templates

**Misión:** convertir la política de templates en un contrato verificable y
versionado sin duplicar reglas.

**Precondición:** G0 accepted.

**Implementación:**

1. Diseñar el formato machine-readable dentro de la autoridad Markdown.
2. Definir envelope común, tipos de datos y extensiones required/optional/
   forbidden por tipo.
3. Definir semántica de `schema_version`, compatibilidad y migradores.
4. Auditar todos los tipos S1/S2 contra templates existentes.
5. Crear templates faltantes y eliminar duplicados por decisión explícita.
6. Definir contrato de tags y secciones mínimas por tipo.
7. Actualizar lifecycle/create para rechazar notas sin template.

**Tests:** mapa type→template total y único; fixtures de dos versiones;
templates S1/S2 respetan frontera; ninguna nota live se modifica aún por
inferencia.

**Gate G1:** contrato y cobertura en review, con estrategia de migración y
rollback aceptable.

### Fase 2 — Lint preventivo y no-new-debt

**Misión:** hacer que el contrato se ejecute automáticamente y detener deuda
nueva antes de limpiar la existente.

**Precondición:** G1 accepted.

**Implementación:**

1. Refactorizar lint para consumir el contrato canónico.
2. Validar frontmatter, tipos, versiones, campos, valores, contenedores,
   formatos, tags, routing, path y secciones mínimas.
3. Agregar modo strict para notas nuevas/modificadas.
4. Crear baseline exacto de findings legacy y fallar ante cualquier finding
   nuevo; el baseline sólo puede disminuir.
5. Mantener `graphify-obsidian update` operativo durante la migración.
6. Crear fixtures unitarias por regla y asserts de read-only.
7. Integrar el gate a las superficies disponibles sin asumir Git.

**Tests:** notas inválidas fallan de a una regla; nota válida por cada familia;
hash del corpus no cambia al lint; un finding nuevo bloquea; un finding legacy
no se oculta.

**Gate G2:** no puede entrar deuda nueva y el baseline es reproducible.

### Fase 3 — Resources/agents, skills y prompts

**Misión:** establecer una home reusable para assets de agentes respetando
ownership y sin reorganizar todo Resources.

**Precondición:** G2 accepted.

**Implementación:**

1. Inventariar referencias a `30-resources/agents/skills/` y al path histórico que será retirado.
2. Preparar move map y rollback con checksums.
3. Crear `30-resources/agents/00-index.md`, `skills/`, `prompts/`,
   `references/` y `examples/` desde contratos/templates válidos.
4. Mover las tres skills portables actuales a `agents/skills/` sin copias.
5. Definir `type: prompt`, template, campos de inputs/output/target/version y
   frontera prompt-vs-skill.
6. Migrar `echo-forge-wfm-troubleshooting` y `sqx-temporal-failure-audit` al
   repo `xKoRx/symphony/.agents/skills/` sin duplicarlas.
7. Actualizar INDEX federado, referencias, packs y discovery.
8. Piloto domain-first: no mover otros dominios de Resources.

**Tests:** source único por skill; INDEX resuelve todos los targets; smoke core,
portable y app-owned; prompt fixture pasa lint; rollback reproduce hashes.

**Gate G3:** topología y ownership en review, sin paths rotos ni copias.

### Fase 4 — Graphify metadata-aware

**Misión:** incorporar metadata confiable al índice local sin cambiar la fuente
de verdad ni romper operaciones existentes.

**Precondición:** G3 accepted y lint preventivo verde.

**Implementación:**

1. Definir schema de metadata proyectada y límites de tamaño/sanitización.
2. Parsear frontmatter con fixtures compartidas del contrato.
3. Guardar metadata sólo en file nodes; headings heredan por pertenencia.
4. Crear índice invertido/filtros para type, tags, scope, status y routing.
5. Crear edges tipados sólo desde campos linkables definidos y hacer la
   deduplicación relation-aware, sin que un `references` previo los suprima.
6. Honrar `.graphifyignore` en extracción, aliases, facets y relaciones.
7. Añadir operación/flags de filter compatibles con query existente.
8. Reindexar y comparar nodos, edges, componentes, tiempo y tamaño.

**Tests:** filtros exactos; `explain`/filter por título y alias; ausencia de ignored paths;
frontmatter malformado no forja metadata; tags no crean supernodos; comandos
legacy conservan resultados; link genérico + tipado al mismo target conserva
la relación tipada.

**Rollback:** restaurar wheel/wrapper anterior y reconstruir índice derivado;
Markdown no cambia.

**Gate G4:** metadata/facets/edges en review con compatibilidad y métricas.

#### Diseño cerrado T4.1

- **Envelope derivado:** cada nodo de archivo Markdown puede llevar `metadata_schema: obsidian-v1`, `metadata` con la proyección allowlisted y `aliases`; headings no copian metadata y sólo conservan pertenencia estructural.
- **Proyección:** `type`, `schema_version`, `status`, `scope`, `area`, `project`, `application`, `entities`, `tags`, `confidence`, `load_policy`, `index_priority` y `updated`; valores desconocidos o estructuras anidadas no se proyectan.
- **Límites fail-closed:** frontmatter máximo de 32 KiB, 64 ítems por lista, 512 caracteres por escalar, sin controles ni saltos de línea; un bloque malformado no produce metadata, aliases ni relaciones.
- **Facets:** el grafo exporta postings exactos `facet -> valor normalizado -> file node ids`; `tags` son postings y nunca nodos ni edges. Routing usa `area`, `project`, `application` y `entities` sobre la misma proyección.
- **Relaciones allowlisted:** `area→in_area`, `parent→child_of`, `project→in_project`, `application→for_application`, `entities→about`, `related→related_to` y `supersedes→supersedes`; sólo se materializan valores con wikilinks canónicos y la identidad de deduplicación es `(source,target,relation)`.
- **CLI compatible:** se agrega `filter` para selección exacta por metadata/title/alias y `query --filter key=value` como extensión aditiva; `query`, `explain`, `path` y `affected` existentes conservan sintaxis y pasan a compartir resolución de aliases.
- **Exclusiones:** discovery, índice de aliases, metadata, facets y relaciones usan el mismo corpus filtrado por `.graphifyignore`; ningún escáner auxiliar puede reintroducir paths ignorados.

### Fase 5 — Context Router y retrieval local

**Misión:** hacer que el router consuma la nueva capa y probar que reduce
lecturas sin API semántica.

**Precondición:** G4 accepted.

**Implementación:**

1. Actualizar contrato Graphify y Context Router sin duplicar algoritmos.
2. Resolver fact por type/entity/tag antes de abrir índice/cuerpo.
3. Resolver relation/impact por edges de frontmatter + wikilinks.
4. Resolver domain synthesis con facets, índice curado y búsqueda lexical.
5. Conservar fallback `rg`/Markdown cuando Graphify esté ausente o stale.
6. Probar cold/warm/swap con agente fresco y dos superficies.
7. Comparar candidatos, precisión proxy, misses, latencia y cuerpos abiertos
   contra baseline Fase 2.

**Tests:** casos project, skill, prompt, known_error, resource y aplicación;
ningún resultado usa template/derivado como evidencia live; degradación
declarada y recuperable.

**Gate G5:** router metadata→grafo→body en review con mejora verificable.

### Fase 6 — Retrofit, segundo piloto y strict gate

**Misión:** cerrar la deuda heredada usando el nuevo contrato, validar adopción
y decidir el gate estricto.

**Precondición:** G5 accepted.

**Implementación:**

1. Resolver con evidencia los 35 tipos desconocidos; mapear, formalizar o archivar, nunca renombrar en masa a ciegas.
2. Resolver 32 campos requeridos, 12 tags, 11 secciones, tres estados y un owner inválidos expuestos por el lint contractual.
3. Clasificar las 81 warnings: migrar 78 notas sin frontmatter y tres sin type, o excluir fragmentos/derivados mediante reglas específicas.
4. Retirar findings del baseline a medida que se corrigen.
5. Ejecutar segundo piloto de layout por área con move map, rollback, Obsidian,
   caches, Graphify y links.
6. Ejecutar lint global, doctor, Graphify, pack y E2E fresco.
7. Activar gate estricto sólo con `ERROR=0` y residuo contractual explícito.
8. Entregar decisión de adopción y dejar G6 en review.

**Tests:** no-new-debt baseline vacío; strict bloquea fixture y permite update
real; doctor `0/0/0`; Graphify/Context Router verdes; rollback del piloto
probado.

**Gate G6:** owner acepta cierre, siguiente lote o rollback puntual.

#### Ledger T6.1 — unknown-type

| Tipo legacy | Casos | Evidencia de clasificación | Ruta de resolución | Estado |
|---|---:|---|---|---|
| `agent-project` | 10 | planes bajo `10-projects/Aranea/agentes/` con objetivo, scope y ejecución delegada | migrados integralmente a `project`; nueve quedan paused/0% y el rollout documental paused/10% | aplicado |
| `owner-task` | 5 | notas de acción humana con contexto y tarea del owner | migradas integralmente a `action`; `open→todo`, `paused→todo` con reactivación explícita | aplicado |
| `ticket` | 6 | tickets operacionales con goal/contexto, scope y estados open/closed/superseded | migrados integralmente a `action`; `open→todo`, `closed→done`, `superseded→canceled` | aplicado |
| `spec-alignment` | 1 | entregable documental de alineación y closeout | migrado a `doc`; gate/review preservado en metadata legacy y cuerpo | aplicado |
| `design-proposal` | 3 | propuestas documentales, dos marcadas deprecated | migradas a `doc`; sólo las dos fuentes deprecated quedaron `archived` | aplicado |
| `audit` | 1 | auditoría documental con findings | migrada a `doc` conservando findings y provenance | aplicado |
| `design` | 1 | diseño Backup/DR congelado | migrado a `doc/active`; rol canónico y congelamiento preservados explícitamente | aplicado |
| `contract-proposal` | 1 | propuesta de contrato, no contrato vigente | migrada a `doc/active` con autoridad no canónica y draft preservados | aplicado |
| `contract` | 1 | contrato Backup/DR vigente | migrado a `doc/active` preservando aprobación y rule-of-record | aplicado |
| `form` | 2 | formularios de decisión operativa | migrados a `doc/active` conservando workflow de decisión | aplicado |
| `request-changes` | 1 | documento de cambios propuestos | migrado a `doc/active` sin confundirlo con `change_log` | aplicado |
| `drill-template` | 1 | plantilla operacional legacy dentro de Resources | migrada a `doc/active` y marcada como artefacto legacy, no template canónico ni runbook | aplicado |
| `strategy_evaluation` | 2 | persistencia generada de matrices Walk-Forward bajo `dashboards/echo-forge/bases/` | excluir por rutas exactas del corpus canónico | aplicado |

## ✅ Tareas

> [!example]- Fuente canónica de tareas
> **Fase 0 — Handoff**
> - [x] T0.1 Verificar ausencia de duplicado y crear [[AGENTS OS - Fase 3]] desde template #owner/agent #type/admin #area/personal
> - [x] T0.2 Transferir baseline y backlog residual de Fase 2 sin duplicar historia #owner/agent #type/research #area/personal
> - [x] T0.3 Definir motivación, alcance, decisiones, riesgos, roadmap y gates #owner/agent #type/research #area/personal
> - [x] T0.4 Crear tarea puente y dejar G0 en Review #owner/agent #type/admin #area/personal
>
> **Fase 1 — Contrato y templates**
> - [x] T1.1 Diseñar contrato machine-readable y `schema_version` #owner/agent #type/dev #area/personal
> - [x] T1.2 Definir envelope común y extensiones S1/S2 #owner/agent #type/dev #area/personal
> - [x] T1.3 Auditar cobertura type→template y crear faltantes #owner/agent #type/research #area/personal
> - [x] T1.4 Definir contrato de tags y estructura mínima #owner/agent #type/dev #area/personal
> - [x] T1.5 Actualizar lifecycle/create y dejar G1 en Review #owner/agent #type/admin #area/personal
> - [x] T1.6 Centralizar materialización y cubrir todas las superficies de creación canónica #owner/agent #type/dev #area/personal
> - [x] T1.7 Aislar validación por tipo y probar que drift ajeno no bloquea cierres S1 #owner/agent #type/dev #area/personal
>
> **Fase 2 — Lint preventivo**
> - [x] T2.1 Refactorizar lint para consumir contrato canónico #owner/agent #type/dev #area/personal
> - [x] T2.2 Validar versiones, campos, tags, routing, paths y estructura #owner/agent #type/dev #area/personal
> - [x] T2.3 Implementar strict new/changed y baseline decreciente #owner/agent #type/dev #area/personal
> - [x] T2.4 Ampliar fixtures y asserts read-only #owner/agent #type/research #area/personal
> - [x] T2.5 Integrar gate sin asumir Git y dejar G2 en Review #owner/agent #type/admin #area/personal
>
> **Fase 3 — Resources/agents**
> - [x] T3.1 Inventariar refs y preparar move/rollback #owner/agent #type/research #area/personal
> - [x] T3.2 Crear topología `agents/{skills,prompts,references,examples}` #owner/agent #type/dev #area/personal
> - [x] T3.3 Mover skills portables y definir contrato/template de prompts #owner/agent #type/dev #area/personal
> - [x] T3.4 Migrar dos skills app-owned pendientes a `xKoRx/symphony` #owner/agent #type/dev #area/personal
> - [x] T3.5 Actualizar registry/packs, forward-test y dejar G3 en Review #owner/agent #type/research #area/personal
>
> **Fase 4 — Graphify metadata-aware**
> - [x] T4.1 Diseñar proyección de metadata y facets #owner/agent #type/research #area/personal
> - [x] T4.2 Implementar parser/proyección en file nodes #owner/agent #type/dev #area/personal
> - [x] T4.3 Implementar filtros y edges tipados de frontmatter #owner/agent #type/dev #area/personal
> - [x] T4.4 Unificar exclusiones y preservar compatibilidad CLI #owner/agent #type/dev #area/personal
> - [x] T4.5 Ejecutar fixtures, reindex, métricas y dejar G4 en Review #owner/agent #type/research #area/personal
>
> **Fase 5 — Context Router**
> - [x] T5.1 Actualizar contrato/router a metadata→grafo→body #owner/agent #type/dev #area/personal
> - [x] T5.2 Implementar rutas fact/relation/domain y fallback #owner/agent #type/dev #area/personal
> - [x] T5.3 Ejecutar E2E fresco multisuperficie sin API #owner/agent #type/research #area/personal
> - [x] T5.4 Comparar métricas y dejar G5 en Review #owner/agent #type/research #area/personal
>
> **Fase 6 — Retrofit y adopción**
> - [x] T6.1 Resolver 35 unknown-type con evidencia #owner/agent #type/research #area/personal
> - [x] T6.2 Resolver 32 missing-field, 12 missing-tag, 11 missing-section, 3 status y 1 owner inválidos #owner/agent #type/dev #area/personal
> - [x] T6.3 Resolver/clasificar 81 warnings y vaciar baseline #owner/agent #type/dev #area/personal
> - [x] T6.4 Ejecutar segundo piloto de layout por área #owner/agent #type/dev #area/personal
> - [x] T6.5 Revalidar lint, doctor, Graphify, pack y E2E #owner/agent #type/research #area/personal
> - [x] T6.6 Decidir flip estricto, entregar y dejar G6 en Review #owner/agent #type/admin #area/personal

## Control de gates

| Gate | Estado | Evidencia requerida | Habilita |
|---|---|---|---|
| G0 | accepted | owner aceptó planner, handoff, bridge, lint y Graphify el 2026-08-08 | F1 |
| G1 | accepted | owner aceptó contrato, cobertura y materialización scoped fail-closed el 2026-08-10 | F2 |
| G2 | accepted | owner aceptó baseline `94/81`, `new=0`, strict/fixtures/read-only y Graphify `5041/5890` el 2026-08-10 | F3 |
| G3 | accepted | owner aceptó topología, ownership, prompts, packs y discovery verdes el 2026-08-10 | F4 |
| G4 | accepted | owner aceptó metadata/facets/edges + compatibilidad, wheel `0.9.6.post1`, suite `2840/28`, reindex y comparación rollback el 2026-08-10 | F5 |
| G5 | accepted | owner aceptó E2E no-API cold/warm/swap en CLI+fallback, 5×14 operaciones con 0 misses, precisión proxy 100%, gates y reindex verdes el 2026-08-10 | F6 |
| G6 | accepted | owner aceptó corpus `0/0`, segundo piloto, baseline vacío, gate estricto y matriz final verde el 2026-08-11 | cierre completado |

## Definición de Done

- Toda nota nueva/modificada se valida contra un template/contrato versionado.
- No existe un tipo creable sin template ni dos templates canónicos para el
  mismo tipo/versión.
- Lint, templates y autoridades no mantienen listas paralelas divergentes.
- El gate evita findings nuevos durante toda la migración.
- `30-resources/agents/` concentra assets portables; runtime y app-owned
  conservan sus homes correctas.
- Resources no replica Areas sin ownership exclusivo demostrado.
- Graphify filtra metadata/tags y recorre relaciones de frontmatter sin
  convertir tags genéricos en supernodos.
- Context Router usa metadata→grafo→body y conserva fallback.
- El baseline contractual F2 de 94 errores y 81 warnings está resuelto o excluido por contrato específico.
- Las dos skills SQX pendientes tienen source único en el repo owner.
- Segundo piloto de layout validado con rollback.
- Gate estricto activado sólo con evidencia de corpus limpio.
- Doctor, Graphify, pack y E2E fresco están verdes.
- G6 queda en Review; sólo el owner cierra la tarea puente.

## Política de repetición y handoff

- Esta nota es el único planificador durable de Fase 3.
- Fase 2 es evidencia histórica aceptada; enlazarla, no copiar sus bitácoras.
- Cada gate requiere aceptación owner antes de iniciar la fase siguiente.
- Cada lote actualiza tareas, progreso, Estado actual y Bitácora en el mismo
  cambio material.
- Cambios canónicos dejan un change log consolidado.
- Todo move tiene inventario, checksums, rollback y validación de referencias.
- Ningún baseline permite deuda nueva; sólo puede decrecer.
- La próxima tarea exacta siempre queda escrita en Estado actual.

## 📊 Estado actual

- **Proyecto completado; T6.1–T6.6 Done; G6 accepted.** El owner aceptó la entrega el 2026-08-11 y cerró la tarea puente. El segundo piloto quedó validado por scanner nativo sobre 1560 archivos: Task Board `old=0`, `new=139`, once paths nuevos y 117 tareas pendientes del lote. El corpus live y el baseline contractual están `0 ERROR / 0 WARN`; `--gate` opera como gate estricto all-vault y bloquea cualquier finding. La matriz final pasó contrato `errors=0`; fixtures/read-only/no-new-debt/strict gate; strict dirigido `0/0`; Doctor `0/0/0` con startup≈5956; pack de 183 archivos; Graphify final `5125/6116`; Context Router E2E `14/14`, 0 misses, precisión proxy 100% y sin API. No quedan tareas abiertas en esta iteración.

## 🧩 Subproyectos

- Ninguno. Los paquetes F0–F6 viven en este planificador único.

## 📆 Bitácora

- **2026-08-11 (G6 accepted · proyecto completado)** — El owner aceptó explícitamente G6 y autorizó cerrar la tarea puente. El proyecto pasa `active→completed`; G6 `review→accepted`; la tarea puente Review→Done. Todas las tareas T0.1–T6.6 están Done y no quedan pendientes de implementación en Fase 3.

- **2026-08-11 (F6 completa · G6 Review)** — T6.6 activó el gate estricto: el baseline persistido quedó `0 ERROR / 0 WARN` y vacío de fingerprints; el wrapper canónico y la instalación local ejecutan `Gate frontmatter (strict)` antes de Graphify. La regresión agregó prueba explícita de baseline vacío que permite corpus sano y bloquea una nota sin frontmatter. La matriz final quedó verde: contrato `errors=0`; lint/gate `0/0`, `new=0`, `resolved=0`; strict dirigido `0/0`; Doctor `0/0/0`, startup≈5941; pack 183; Graphify `5123/6114`; E2E `14/14`, 0 misses, precisión proxy 100%, p95 Graphify 202.95 ms y fallback 18.72 ms. T6.6 pasa `[/]→[x]`, progress `98→100`, G6 `pending→review` y la tarea puente WIP→Review. Evidencia: [[2026-08-11-agents-os-fase3-t66-strict-gate]].

- **2026-08-11 (T6.4 completa · T6.6 WIP)** — El owner ejecutó el scanner nativo de Task Board sobre 1560 archivos. La verificación read-only posterior confirmó JSON válido, `old=0`, `new=139`, once paths nuevos bajo el subárbol piloto y 117 tareas pendientes asociadas; T6.4 pasa `[/]→[x]`. Se inició T6.6: el baseline contractual pasó de `94/81` histórico vacío en runtime a `0/0` persistido, por lo que `--gate` ahora bloquea cualquier finding; wrapper canónico e instalación local muestran `Gate frontmatter (strict)`. La suite del lint pasó fixtures, strict, read-only, no-new-debt y strict gate; corpus y gate live quedaron `0/0`. T6.6 pasa `[ ]→[/]`, progress `96→98` y la tarea puente permanece WIP hasta la matriz final.

- **2026-08-11 (T6.4 bloqueada por permiso de Accesibilidad)** — Se comprobó que Obsidian está abierto como proceso `Electron`; se invocó el flujo nativo de Task Board, pero macOS rechazó el envío de teclas de `osascript` con error `1002` (“no tiene permitido enviar presiones de tecla”). La cache read-only permanece `old=28/new=0`. No se editó el derivado ni se inició T6.6; se requiere permiso de Accesibilidad o ejecución manual del scanner para generar la evidencia de cierre. Evidencia: [[2026-08-11-agents-os-fase3-native-scanner-blocker]].

- **2026-08-11 (T6.5 completa · T6.4 sigue WIP)** — Se ejecutó la matriz técnica posterior al segundo piloto: contrato `errors=0`; lint/gate `0/0`, `new=0`, `resolved=175`; strict permitió fixture v1 y bloqueó fixture inválida; Doctor `0/0/0` con startup≈5942; pack de 183 archivos con hashes y ZIP válidos; Graphify `5118/6101`; E2E `14/14`, 0 misses, precisión proxy 100%, p95 Graphify 210.4 ms y fallback 19.59 ms. La advertencia de skill Graphify 0.8.39 frente al paquete 0.9.6.post1 es ruido cosmético ya documentado y no afectó el indexado. T6.5 pasa `[/]→[x]`, progress `93→96`. T6.4 no se cierra: cache Task Board `old=28/new=0`, Apple Events sin respuesta y CLI Obsidian deshabilitada; no se modificó el derivado. Evidencia: [[2026-08-11-agents-os-fase3-t65-validation]].

- **2026-08-11 (T6.4 sigue WIP · scanner nativo pendiente)** — La lectura read-only de `.obsidian/plugins/task-board/tasks.json` confirmó JSON válido pero cache stale: `28` valores string con el path viejo `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT.md` y `0` bajo el subárbol nuevo. No se alteró el derivado. La automatización de eventos macOS sigue indisponible y no permite ejecutar ni comprobar visualmente el scanner; la tarea y la puente se mantienen WIP. Próximo paso: scanner completo de Task Board en Obsidian y verificación `old=0` + paths nuevos + tablero operativo.

- **2026-08-10 (T6.4 WIP · move y rollback verdes; cache nativa pendiente)** — El segundo piloto seleccionó `BACKUP-DR-OWNER-PROJECT` porque el lote humano de once notas cumplía schema v1, tenía relaciones parent/children y estaba consumido por Task Board. El move agrupó owner, contrato y nueve subproyectos bajo `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/`; se repararon tres referencias path-based vigentes y el índice Aranea se migró a schema v1, tags namespaced, headings contractuales y paths `VAULT_ROOT`. El rollback real restauró los once hashes y el file-node origen con 33 conexiones; el forward definitivo dejó once file-nodes nuevos, backlinks y relaciones verdes, lint global `0/0`, gate `new=0 resolved=175`, contrato verde y Graphify `5118/6101`. Task Board reprodujo el riesgo conocido: cache stale `old=130/new=0`; no se editó el derivado porque el scanner nativo no pudo automatizarse sin acceso de eventos macOS. T6.4 pasa `[ ]→[/]`, progress sigue `93` y queda bloqueada sólo por el scan completo y verificación visual en Obsidian. Evidencia: [[AGENTS OS Fase 3 T6.4 — Segundo piloto de layout por área]].

- **2026-08-10 (T6.3 completa · warnings legacy resueltos)** — Se clasificaron los 80 warnings remanentes por evidencia. Aranea preserva páginas canónicas migradas a `doc`, procedimientos a `runbook` y tickets históricos a `action`; la decisión pública y tres memorias internas quedaron conformes al schema vigente. Se eliminaron credenciales expuestas de `APIs.md`. Diecinueve artefactos no canónicos (evidencia de investigación sin provenance, ejemplos, instrucciones de host, borradores, panel derivado y dibujo de plugin) se excluyeron por rutas exactas en `.graphifyignore`, sin regla amplia. Validación: lint/gate `0 ERROR / 0 WARN`, contrato `0`, Graphify `5118/6101`; Doctor `0/0/0` y E2E `14/14`, 0 misses como evidencia anticipada que se repetirá después del piloto T6.4. T6.3 pasa `[x]`, progress `90→93`; T6.4 queda como próximo paso.

- **2026-08-10 (T6.2 completa · normalización de findings contractuales)** — Se resolvieron todos los 56 ERROR vigentes: 32 campos requeridos, 12 tags, 11 secciones y los estados S2 restantes. El lote incorporó metadata de retrieval en nueve skills, `scope/global` en doce, headings contractuales preservando el contenido, `sources` en Data Mesh y lifecycle/tags correctos en dos índices históricos. Los tres legacy modificados declararon `schema_version: 1` y se completaron sus secciones/tipos para pasar strict. Validación: contrato `0` errores, strict de 19 notas `0/0`, lint global `0 ERROR / 80 WARN`; `unknown-type=0`, `new=0`, `resolved=95`. T6.2 pasa `[x]`, progress `86→90`; T6.3 queda como próximo paso.

- **2026-08-10 (T6.1 completa · lote documental)** — Se migraron los doce tipos legacy restantes a `doc` v1 con tags y secciones contractuales. `DESIGN-PROPOSAL` y `PROPUESTA-COMPLETA-ITER4` quedaron `archived` porque ya declaraban deprecación; los otros diez quedaron `active` sin perder la semántica de review, findings, diseño congelado, draft, contrato aprobado, formularios, request changes ni plantilla operacional legacy. Strict del lote `0/0`; gate global `56/80`, `new=0`, `resolved=39`; `unknown-type` baja `12→0`. Graphify reconstruyó `5081/6011` y verificó los doce nodos `doc` con lifecycle `10/2`. T6.1 pasa `[x]`, progress `83→86` y T6.2 queda como próximo paso.
- **2026-08-10 (T6.1 · regresión Graphify tipada acotada)** — El reindex inicial encontró los diez proyectos por facets, pero `affected --relation child_of` omitió los proyectos 00 y 09 porque cada nota repetía su parent dentro de `related`; `path` devolvía sólo `related_to`. Se retiraron las dos relaciones genéricas redundantes y el segundo reindex restauró nueve hijos Backup/DR más uno Servicios Docs como `child_of`. El known error se actualizó: `0.9.6.post1` resolvió aliases y colisiones typed-vs-references, pero conserva un gap entre dos relaciones tipadas del mismo par; la causa en código queda pendiente.
- **2026-08-10 (T6.1 · lote agent-project completo)** — Se migraron diez `agent-project` a `project` v1 con `owner: agent`, parent, lifecycle, prioridad, progress, tags y secciones contractuales. Los proyectos 00–08 quedan `paused/0%` porque el parent prohibía ejecución pese al estado legacy `ready`; el proyecto 09 conserva la pausa y queda `10%` por tres acciones completadas de veintinueve. Para cumplir el workflow se migraron los dos parents legacy y se agregaron diez tareas puente `#owner/me #type/supervision`; esto resolvió además `bad-status`, `bad-owner` y `missing-progress` ya inventariados para T6.2. Strict de hijos y parents `0/0`; gate global `68/80`, `new=0`, `resolved=27`; `unknown-type` baja `22→12`. T6.1 sigue WIP con los doce documentos legacy del ledger.
- **2026-08-10 (T6.1 · dos lotes action completos)** — Se migraron integralmente cinco `owner-task` y seis `ticket` al contrato `action` v1, preservando el contenido histórico y normalizando owner, lifecycle, tags y secciones. Mappings aplicados: `open→todo`, `paused→todo` con reactivación explícita, `closed→done` y `superseded→canceled`. Ambos lotes pasan strict `0/0`; el gate global bajó `92→81 ERROR`, conservó `80 WARN`, quedó `new=0`, `resolved=14` y redujo `unknown-type` de `33→22`. T6.1 sigue WIP; el próximo lote son diez `agent-project`.
- **2026-08-10 (F6 iniciada · T6.1 WIP)** — Se inició el retrofit residual tras G5 accepted. El lint reprodujo `94 ERROR / 80 WARN`, incluidos `35 unknown-type` en `13` valores. La inspección de frontmatter, títulos, headings y paths permitió agrupar `10 agent-project→project`, `11 ticket/owner-task→action`, `12 entregables legacy→doc` y `2 strategy_evaluation` derivados; estos últimos se excluyeron por rutas exactas, sin regla genérica. El gate posterior pasó con `92/80`, `new=0`, `resolved=3`; el reindex quedó en `5009` nodos y `5939` edges sin los dos derivados. T6.1 permanece WIP hasta migrar y validar los otros `33` casos.
- **2026-08-10 (G5 accepted · cierre de sesión)** — El owner aceptó G5 y pidió cierre explícito. F6 queda habilitada sin iniciar; T6.1 permanece `[ ]`, progress continúa en `83` y la tarea puente vuelve Review→WIP. Próximo paso exacto: clasificar y resolver con evidencia los 35 `unknown-type`, sin renombrado masivo por inferencia.
- **2026-08-10 (F5 completa · G5 review)** — T5.2 cerró rutas fact/relation/domain, resolución de skill vía facet+registry y fallback Markdown; el primer E2E rechazó correctamente 29 candidatos extra al usar sólo `type=skill`, y la ruta final los redujo mediante `80-agents/skills/INDEX.md` sin ocultar el gap. T5.3 agregó `context_router_e2e.py` y validó desde un proceso aislado cold/warm/swap, dos superficies y siete clases de fuente sin API. T5.4 ejecutó cinco repeticiones (`70` operaciones): 0 misses, precisión proxy 100%, p95 CLI `203.60–214.47 ms`, fallback `11.09–13.23 ms`, cuatro cuerpos y un índice curado por corrida; el baseline F2 era 2.9% miss y p95 `598 ms` sobre 279 operaciones, por lo que la comparación es direccional y no reemplaza esa muestra histórica. El smoke post-reindex pasó con p95 `266.05/17.58 ms`; schema, strict, gate y Doctor verdes. Graphify reconstruyó `5014/5942`; las comunidades variaron `487→493` y se excluyen del gate. `graph.html` se omitió por el límite de 5000 nodos, manteniendo `graph.json` y `GRAPH_REPORT.md`. T5.2–T5.4 `[x]`, progress `75→83`, G5 `pending→review` y bridge WIP→Review. F6 permanece bloqueada hasta aceptación owner.
- **2026-08-10 (F5 · degradación externa durante T5.2)** — Un refresh posterior a la sincronización del planner activó correctamente el gate no-new-debt y fue rechazado por `bad-tag` en `10-projects/Meli/Crear Context/Crear Context.md` (`project` sin namespace), una edición concurrente fuera del scope de F5. La nota ya declara `root: true`, por lo que el lint dirigido actual reporta sólo ese finding. No se modificó la nota ajena; el índice válido de T5.1 (`4990/5899/498`) permanece disponible y T5.2 continúa WIP con esta degradación explícita.
- **2026-08-10 (F5 · T5.1 completa · T5.2 WIP)** — Se actualizaron `graphify-contract.md`, `agents-os-context-retrieval` y `context-router.md` sin duplicar el algoritmo: el contrato define capacidades, la skill ejecuta el routing y el doc explica el modelo. Los tres artefactos fueron migrados/conservados en schema v1 y pasan lint estricto `0/0`; validator `errors=0`. Las pruebas live confirmaron título con `.md`, alias sin sufijo, intersección type+tag, `query --filter`, `explain` y edge tipado `child_of`. El reindex pasó el gate `94/80 new=0 resolved=1` y produjo `4990` nodos, `5899` edges y `498` comunidades. T5.1 `[/]→[x]`, T5.2 `[ ]→[/]`, progress `73→75` y bridge permanece WIP.
- **2026-08-10 (G4 accepted · handoff F5)** — El owner confirmó que la garantía de conformidad usa materialización Python desde template más lint contractual, aceptó G4 e indicó comenzar F5. G4 `review→accepted`; T5.1 `[ ]→[/]`, F5 queda activa y la tarea puente vuelve Review→WIP. Próximo paso: actualizar el contrato Graphify y el Context Router a metadata/facets→grafo→body sin duplicar la lógica de routing.
- **2026-08-10 (F4 completa · G4 review)** — T4.5 construyó e instaló `graphifyy 0.9.6.post1` (wheel SHA-256 `ecdb3e67c4d3a31153ddb38b08c15c106c102844ce88503c99e23bd3971225d1`), amplió `.graphifyignore` a todas las fixtures, corrigió que un `references` inverso sobreescribiera relaciones de frontmatter y validó alias/filter/query/path/explain/affected. Suite final `2840 passed, 28 skipped`, Ruff verde, lint estricto `0/0`, gate `94/81 new=0` y Doctor `0/0/0`. Comparación controlada sobre el mismo corpus: rollback `0.9.6`=`4984/5889/497`, `12.60 s`, `4,634,091 bytes`; actual=`4984/5893/493`, `15.93 s`, `5,308,347 bytes` (`+0` nodos, `+4` edges, `-4` comunidades, `+3.33 s`, `+674,256 bytes`). El benchmark contiene `359` file nodes con metadata, 15 dimensiones facet, edges tipados `in_area=200`, `child_of=28`, `in_project=124`, `for_application=28`, `about=64`, `related_to=244`, `supersedes=1`, sin tag-nodes ni ignored paths; el refresh post-registro quedó `4985/5894` y no usa comunidades como gate por su variación entre reconstrucciones. T4.5 `[x]`, progress `70→73`, G4 `pending→review` y bridge WIP→Review; F5 espera aceptación owner.
- **2026-08-10 (F4 · T4.4 completa · T4.5 WIP)** — El índice auxiliar de stems/aliases ahora usa los mismos patrones `.graphifyignore` que discovery y el wrapper expone `filter` como consulta directa. La suite completa detectó que los postings dict rompían GraphML; se corrigió serializando atributos estructurados sólo para ese export, manteniendo graph.json tipado. Las fallas de hooks se aislaron con `GIT_CONFIG_GLOBAL=/dev/null` porque la máquina define `core.hooksPath`; resultado final `2839 passed, 28 skipped`, Ruff verde. T4.4 `[x]`, T4.5 `[/]`, progress `67→70`.
- **2026-08-10 (F4 · T4.3 completa · T4.4 WIP)** — Se incorporaron postings exactos persistidos, operación `filter`, flag aditivo `query --filter`, filtros type/tag/scope/status/routing/title/alias, resolución compartida de aliases y edges tipados desde siete campos de frontmatter. La deduplicación ahora distingue relación y tags siguen sin nodos/edges. Regresión CLI/unitaria: `167 passed, 2 skipped`; Ruff verde. T4.3 `[x]`, T4.4 `[/]`, progress `64→67`.
- **2026-08-10 (F4 · T4.2 completa · T4.3 WIP)** — Se implementó el parser Obsidian sin dependencia YAML, límites 32 KiB/64 ítems/512 caracteres, sanitización de escalares y proyección allowlisted sólo en nodos de archivo; aliases quedan separados y frontmatter malformado no produce metadata ni relaciones. Suite dirigida metadata/typed-links/Markdown: `24 passed`. T4.2 `[x]`, T4.3 `[/]`, progress `61→64`.
- **2026-08-10 (F4 · T4.1 completa · T4.2 WIP)** — Se cerró el diseño metadata-aware sin convertir Graphify en autoridad: metadata selectiva sólo en file nodes, aliases separados, facets como postings exactos, tags sin edges, siete relaciones allowlisted, deduplicación `(source,target,relation)`, límites fail-closed y `.graphifyignore` como filtro único. T4.1 `[x]`, T4.2 `[/]`, progress `58→61`; G4 y bridge permanecen pending/WIP.
- **2026-08-10 (G3 accepted · handoff F4)** — El owner aprobó G3 y pidió actualizar el proyecto y cerrar la sesión. G3 `review→accepted`; F4 queda habilitada sin iniciar, T4.1 permanece `[ ]`, progress continúa `58` y la tarea puente vuelve Review→WIP. Próximo paso exacto: diseñar la proyección de metadata y facets en T4.1.
- **2026-08-10 (F3 completa · G3 review)** — Se corrigió el falso bloqueo causado por buscar Symphony sólo bajo `~/fuentes`: la fuente canónica ya declaraba `~/go/src/github.com/xKoRx/symphony` y el remoto configurado usa `github.com-personal`. T3.4 movió sin copia `echo-forge-wfm-troubleshooting` y `sqx-temporal-failure-audit` al repo owner, adaptó metadata/secciones/referencias al contrato nativo y verificó source único. T3.5 actualizó registry y pack; el pack generó 182 archivos con hashes/ZIP válidos. El forward-test fresco pasó core, portable, prompt, las tres app-owned, contrato del repo, dependencias relativas, source único, registry y pack con `forward_test_failures=0`; también restauró `sqx-plugin-lifecycle` desde `ea03696` porque faltaba en la rama activa. Release-process MCP no estaba instalado, así que los gates se ejecutaron localmente con schema, strict, baseline, Doctor y Graphify. T3.4/T3.5 `[x]`, progress `54→58`, G3 `pending→review` y bridge WIP→Review.
- **2026-08-10 (F3 parcial · bloqueo de ownership externo)** — T3.1 inventarió referencias live, move map, hashes y rollback en [[F3 — Migración de skills]]. T3.2 creó el dominio `30-resources/agents/` con índice, prompts, references, examples, skills y log. T3.3 movió `sync-local-branch`, `fury-lib-consumer-deploy` y `sdd-workflow` sin copias; los hashes se conservaron y registry/Doctor se actualizaron. Se agregó `type: prompt`, template y fixture. Schema, strict de notas nuevas y Doctor quedaron verdes; Graphify reindexó `5066/5928/499` y resolvió el proyecto y prompt. T3.4 queda WIP bloqueada: falta checkout/acceso a `xKoRx/symphony`; remoto SSH respondió “Repository not found”. T3.5 permanece WIP y G3 `pending`; no se mueve la tarea puente a Review.
- **2026-08-10 (G2 accepted · handoff F3)** — El owner aceptó G2 y pidió cierre de sesión para continuar con un próximo agente. G2 `review→accepted`; F3 queda habilitada sin iniciar, T3.1 permanece `[ ]`, progress continúa `44` y bridge Review→WIP con foco F3/G3. Próximo paso exacto: inventario de referencias a `30-resources/agents-skills/`, move map, checksums y rollback.
- **2026-08-10 (G2 review · corrección materializador→strict)** — La validación del change log materializado detectó que un escalar opcional vacío era tratado como tipo inválido. El lint ahora permite opcionales vacíos y mantiene fail-closed para requeridos vacíos; fixture v1 y strict del change log quedan verdes sin alterar baseline `94/81` ni estado de G2.
- **2026-08-10 (F2 completa · G2 review)** — T2.5 integró el gate no-new-debt al wrapper canónico y a su copia instalada: falta de lint o fingerprint nuevo bloquea `update`; deuda incluida en baseline no bloquea. E2E real: `ERROR=94 WARN=81 baseline=94/81 new=0 resolved=0`, Graphify exit 0 con `5041/5890/499`, y `explain` resolvió Fase 3 y el contrato. T2.5 `[x]`, G2 `pending→review`, progress `42→44` y bridge WIP→Review. El owner debe aceptar G2 antes de F3.
- **2026-08-10 (F2 · T2.1–T2.4 completas)** — `lint.py` dejó de copiar constantes y consume `schema-contract.md`; valida versión, requeridos/prohibidos, tipos de datos, lifecycle, tags, wikilinks de routing, secciones, fronteras y reglas semánticas. `--strict <path...>` exige v1 y cero findings sin usar Git; `--gate` exige que el set actual sea subconjunto del baseline SHA-256 y permite sólo disminución. Fixtures contractuales y legacy, regresión read-only y prueba de deuda nueva pasan. El nuevo baseline reproducible es `94/81`, mayor que `41/81` porque expone deuda v1 que el lint legacy no veía; las autoridades tocadas por F2 fueron migradas y pasan strict. T2.1–T2.4 `[x]`, T2.5 `[/]`, progress `31→42`.
- **2026-08-10 (F2 iniciada · T2.1 WIP)** — El owner pidió sincronizar el cockpit y completar F2. Se corrigió el estado stale del parent, T2.1 pasó `[ ]→[/]` y comenzó la auditoría del lint legacy contra el contrato ejecutable; G2 permanece `pending` hasta demostrar no-new-debt, fixtures read-only e integración independiente de Git.
- **2026-08-10 (T1.7 · G1 accepted)** — La fricción real del cierre Stager
  demostró que `materialize_schema_note.py` validaba globalmente los 42
  templates antes de crear cualquier tipo: drift en `application` bloqueó
  `change_log`, L0 y feedback S1. Se separó create scoped de auditoría global.
  Regresión: `unrelated_drift=isolated`, `requested_type_drift=blocked`;
  validator global/scoped y dry-run `change_log` verdes. El owner ordenó
  terminar F1/G1: T1.7 `[x]`, G1 `review→accepted`, progress `29→31` y F2
  habilitada con T2.1 como próximo paso.
- **2026-08-10 (auditoría anti-ruido · economía de tokens)** — La revisión del
  owner detectó que `.graphifyignore` aún permitía indexar inputs, aunque D9/R14
  ya prohibían supernodos. Se midieron `299` nodos de templates y `10` de
  fixtures. Se excluyeron `70-templates/`, `80-agents/templates/` y fixtures
  del contrato; validator siguió en `errors=0` y Graphify pasó de `5287/6076`
  a `4978/5774`, con `0` nodos residuales en esos paths. No existen nodos de
  facets `type`, `schema_version`, `project` o `kind/*`; contrato grado `4`,
  materializador grado `6`. Se fijaron R25 y D15. Una prueba de estabilidad
  posterior trazó el delta global a cambios concurrentes en dos notas RIO, no
  a acumulación incremental; el gate durable es el conteo por paths (`0`). La
  misma concurrencia cambió `application.md` sin actualizar el contrato y abrió
  `2` errores. Se actualizó atómicamente el perfil v1 de `application`, se
  versionaron las 10 notas RIO nuevas y validator/lint dirigido volvieron a
  `0/0`. El materializador renderiza la nueva forma v1 correctamente.
- **2026-08-10 (T1.6 completa · G1 review)** — Se agregó materializador
  canónico sin overwrite y auditoría de 13 creation entrypoints. Contrato,
  resolver y create path fallan ante tipo desconocido/exento o gate rojo.
  [[Economía de Tokens]] queda como D14 y relación estructural; todo ocurre
  programáticamente sin cargar cuerpos. T1.6 `[x]`, bridge WIP→Review y G1
  `pending→review` nuevamente. Lint dirigido `0/0`; el baseline global
  `41/81` incluye un nuevo `missing-field` en `data-mesh.md`, externo a F1.
- **2026-08-10 (G1 rechazado · gap de enforcement)** — El owner exigió
  comprobar que todas las notas canónicas nuevas usan implementación real y
  recordó que AGENTS OS deriva de [[Economía de Tokens]]. Se verificó que el
  contrato y resolver son reales, pero varias skills aún referencian templates
  directamente. G1 vuelve a `pending`, bridge a WIP y T1.6 queda abierta.
- **2026-08-10 (F1 completa · G1 review)** — T1.1–T1.5 `[x]`; lifecycle/create
  usa resolver fail-closed y el gate de contrato quedó verde. Validación final:
  schema `errors=0`, lint dirigido de 51 fuentes `0/0`, doctor estricto
  `0/0/0`, baseline global `40/81` sin deuda nueva y Graphify `5253/6010`.
  G1 `pending→review`; la tarea puente pasa WIP→Review. F2 no inicia sin
  aceptación humana.
- **2026-08-10 (F1 · T1.1–T1.4)** — Creado contrato ejecutable v1 con 43
  tipos y semántica legacy/future; templates versionados y cobertura canónica
  completa mediante 12 templates faltantes. Tags/secciones mínimas y tipos de
  datos quedaron contractuales. El auditor verifica mapping único, fronteras,
  campos, tags, headings, derivados, fragmentos y fixtures con `errors=0`.
  T1.5 pasa a WIP para cerrar lifecycle/create y gates.
- **2026-08-10 (F1 retomada)** — El owner solicitó ejecutar T1.1–T1.5 y cerrar
  sesión al terminar. T1.1 pasa a WIP; el planificador sigue siendo la fuente
  única y G1 no avanzará a Review sin contrato, auditoría y validación.
- **2026-08-08 (G0 accepted · cierre de sesión)** — El owner aceptó G0. F1
  queda habilitada pero no iniciada; ninguna tarea T1 cambió de estado. La
  próxima ejecución comienza en T1.1. Los gaps verificados de alias resolution
  y deduplicación de relaciones fueron promovidos a known error reusable y
  feedback Graphify.
- **2026-08-08 (validación G0)** — Lint dirigido de cinco fuentes `0/0`;
  doctor estricto `HIGH=0 MEDIUM=0 LOW=0`, startup≈5015; Graphify reindexó
  `5615` nodos / `6469` edges y resolvió el título canónico. El alias
  `AGENTS OS Executable Schema` no fue resuelto por `explain`, y el edge
  `depende_de` quedó suprimido porque un `references` al mismo target apareció
  antes. Ambos gaps quedaron incorporados como R23/R24 y tests de F4.
- **2026-08-08 (creación · G0 review)** — Fase 2 cerrada y su deuda viva
  transferida sin duplicar historia. Creado roadmap F0–F6 con contrato
  versionado de templates, lint preventivo, topología Resources/agents,
  Graphify metadata-aware, Context Router local, retrofit residual y segundo
  piloto. T0.1–T0.4 `[x]`; G0 `pending→review`.

## 🧭 Decisiones

- Ver tabla `Decisiones vigentes`; cualquier cambio exige actualizarla antes
  de implementar y dejar evidencia en Bitácora.

## Relaciones

- depende de [[AGENTS OS - Fase 2]]
- depende de [[AGENTS OS]]
- deriva de [[Economía de Tokens]]
- implementa [[token-economy-indexing-architecture]]
- consume [[agents-os-bootstrap]]
- consume [[agents-os-context-retrieval]]

## 🔗 Docs / Links

- [[AGENTS OS]] — cockpit y tarea puente.
- [[schema-contract]] — contrato ejecutable S1/S2.
- [[executable-schema-contract-versioning]] — ADR de formato, compatibilidad y
  migración.
- [[AGENTS OS - Fase 2]] — baseline, entregables y deuda transferida.
- [[agents-os]] — mapa conceptual.
- [[agent-constitution]] — invariantes.
- [[convenciones]] — schema Sistema 2 y PARA.
- [[metadata-schema]] — schema Sistema 1.
- [[graphify-contract]] — contrato derivado actual.
- `70-templates/` — templates Sistema 2.
- `80-agents/templates/` — templates Sistema 1.
- `80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py` — lint actual.
- `80-agents/skills/agents-os-graphify-install/` — wrapper canónico y provenance;
  binario, wheels e índice viven localmente fuera del vault.

## 💡 Ideas

### Backlog de ideas

- Evaluar autocompletado de frontmatter desde el contrato una vez que lint y
  creación determinística estén estables.
- Evaluar ranking por freshness/confidence después de validar filtros exactos;
  no incorporarlo antes de G4.
- **Shift-left del gate en flujos que generan Markdown (2026-08-10):** exigir `materialize_schema_note.py` + `lint.py --strict` DENTRO de las herramientas/agentes que emiten notas (p.ej. generadores como `rio-inspector` y el flujo que construye RIO Atlas), no sólo en el reindex. El contrato+gate de Fase 3 detecta el drift fail-closed y funcionó (frenó 3 notas del RIO Atlas creadas con frontmatter a mano y un `type: reference` inexistente antes de reindexar), pero su alcance no cubre integrar la validación en flujos de creación externos; sin eso un generador reintroduce frontmatter no conforme en cada corrida. `agents-os-entity-lifecycle` ya ordena el flujo correcto (clasificar → materializar desde `resource`/`index` → incorporar → `lint --strict` sobre las notas → pasar gate → recién reindexar); la mejora es hacerlo **obligatorio** en esos flujos. No requiere skill nueva ni un `type` extra para silenciar el lint. Origen: sesión de onboarding Signals; ver [[Onboarding Signals]].

### Motivos / principios

- Prevenir drift nuevo es más valioso que un retrofit masivo temprano.
- Metadata confiable habilita retrieval local explicable.
- Los paths expresan ownership estable; los links expresan semántica.
- Graphify se reconstruye; Markdown se preserva.

### Memoria pública / interna

- **Memoria pública:** contratos, decisiones y aprendizajes que gobiernan a
  todos los agentes.
- **Memoria interna:** continuidad compacta del agente hacia este planificador.
- **Motivo:** mantener historia y coordinación fuera del hot path sin perder
  retomabilidad.
