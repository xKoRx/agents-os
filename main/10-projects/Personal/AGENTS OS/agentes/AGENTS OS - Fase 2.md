---
type: project
owner: agent
root: false
status: completed
cssclasses:
  - wide
priority: P0
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-08-01
due:
progress: 100
repo:
jira:
prs:
aliases:
  - AGENTS OS Fase 2
  - AGENTS OS Architecture Phase 2
  - AGENTS OS Vault Curation
tags:
  - area/personal
  - kind/project
  - project/agents-os
created: 2026-08-01
updated: 2026-08-08
---

# AGENTS OS - Fase 2

> [!info]+ Planificador único de la iteración
> **Padre:** [[AGENTS OS]] · **Owner:** agent · **Estado:** completed ·
> **Prioridad:** P0 · **Gate final:** G7 `accepted` · **Handoff:** [[AGENTS OS - Fase 3]]
>
> Este proyecto organiza la segunda iteración de AGENTS OS: autoridades
> únicas, carga incremental, skills por ownership, schema consistente,
> documentación LLM Wiki curada y una migración retomable del vault.

## Resumen ejecutivo

AGENTS OS ya aporta valor como sistema de contexto persistente, pero su primera
iteración acumuló procedimientos repetidos, proyectos controladores extensos,
skills de distinto scope en una carpeta plana y dos schemas que compiten. Fase
2 conserva el valor comprobado y reduce las fuentes de drift.

El resultado buscado no es sólo ahorrar tokens: es que un agente fresco pueda
entender qué leer, dónde está la autoridad, qué puede modificar y cómo dejar
continuidad verificable. El sistema debe seguir siendo redefinible: decisiones,
gates y evidencia quedan en este proyecto, no congeladas en reglas implícitas.

## 🎯 Objetivo

- Diseñar y ejecutar una arquitectura de conocimiento curado para humanos y
  agentes, con una fuente canónica por hecho o procedimiento.
- Hacer que `AGENTS.md` sea un hook mínimo y que `agents-os-bootstrap` sea la
  única máquina de startup.
- Separar skills globales del vault, metodologías transversales y skills
  propiedad de aplicaciones/repositorios.
- Separar el schema de Sistema 1 del schema de Sistema 2 y validarlos de forma
  determinística.
- Integrar LLM Wiki como lifecycle de conocimiento, no como otro entrypoint ni
  como una copia de documentación canónica.
- Dejar una ruta gradual para reorganizar proyectos por área sin romper links,
  Graphify ni entrypoints.
- Validar continuidad, utilidad y portabilidad con agentes frescos.

## 📊 Estado actual

- **Proyecto completado; backlog residual transferido a [[AGENTS OS - Fase 3]]
  (2026-08-08).** El owner ordenó cerrar Fase 2 y continuar sin retrabajo en una
  nueva iteración. Fase 3 hereda los `41 ERROR / 84 WARN`, las dos skills
  app-owned pendientes, el segundo piloto de layout y el eventual gate
  estricto, junto con el nuevo alcance de templates versionados, Resources/
  agents y Graphify metadata-aware. Los entregables y gates aceptados aquí no
  se reabren ni se duplican.
- **G7 `accepted`; Fase 2 completa y lista para cierre owner (2026-08-08).**
  El owner confirmó T7.4 en una vista real de Obsidian: el rescan completo de
  Task Board muestra el nuevo path `10-projects/Personal/AGENTS OS/` y no el
  path antiguo `10-projects/AGENTS OS/`. El piloto path-based queda validado.
  Se conserva `warn-first`: los 41 ERROR residuales siguen scoped y el cambio
  a gate estricto continúa en NO-GO. No hay una F8 automática; cualquier lote
  adicional requiere decisión explícita del owner o una nueva iteración.
- **F7 entregada; G7 en `review` (2026-08-08).** El retrofit P1 seguro redujo
  el lint global de `237 ERROR / 84 WARN` a `41 ERROR / 84 WARN`: las 26 skills
  core, skills federadas/app, 64 memorias internas y fuentes S1 verificables
  quedaron regularizadas. Los 41 errores restantes están scoped: 35 tipos
  legacy, 3 estados legacy, 2 campos de proyecto y 1 owner; se concentran en
  Aranea (37), Echo Forge (1), Destaques (1) y dashboards Echo (2). No se
  reinterpretaron estados ni ownership sin evidencia. Doctor estricto
  `0/0/0` (startup≈5006) y Graphify `5474/6296` están verdes. Decisión:
  mantener `warn-first`; el gate estricto es **NO-GO** mientras haya 41 ERROR.
  Todo el trabajo del agente está cerrado. Falta únicamente T7.4, prueba
  humana del rescan path-based en una vista real de Obsidian.
- **G6 `accepted`; F7 iniciada (2026-08-08).** El owner autorizó aceptar G6
  si la revalidación resultaba verde. Se reprodujo doctor estricto
  `HIGH=0 MEDIUM=0 LOW=0`, Graphify resolvió el planificador vigente y la
  evidencia multisuperficie/smoke CLI sigue trazable; G6 queda aceptado. Se
  corrigió drift documental de R11/R12/R14 y del despacho F6. F7 abre el
  cierre gradual de la deuda restante: T7.1/T7.2 cerradas con baseline lint
  `237 ERROR / 84 WARN` sobre 485 notas; la mayor concentración está en
  Sistema 1 (`182` findings), seguida por resources (`32`), proyectos (`21`)
  y sistema (`2`). Próximo paso exacto: T7.3, retrofit P1 de fuentes
  canónicas con metadata verificable. El primer lote P1 regularizó las 26
  skills core `agents-os-*`, reduciendo el lint a `159 ERROR / 84 WARN`; quedan
  fuera de este lote los tipos, ownership y fechas que no pueden inferirse.
  El owner elevó el target blando de cold startup a 6k; doctor vuelve a
  `0/0/0` con startup≈5006 y el lote P1 conserva su validez.
  El gate continúa `warn-first`; no se
  hace un retrofit masivo ni un flip estricto sin evidencia.
- **G5 aceptado por el owner; Fase 6 iniciada (2026-08-08).** La revisión
  actual confirmó el piloto: doctor estricto `0/0/0`, fuentes canónicas y
  rollback íntegros. Se conserva el **NO-GO temporal** para retrofit masivo
  hasta probar un rescan real de caches de plugins path-based. T6.1 queda en
  WIP para ejecutar la matriz cold/warm/swap/Graphify.
- **Fase 6 parcialmente validada (2026-08-08).** T6.1, T6.4 y T6.6 cerradas:
  cold/warm/swap y Graphify disponible/degradado preservan la autoridad y el
  fallback; doctor estricto `0/0/0`; reindex completó con 5471 nodos/6291
  aristas. El query log registra 279 operaciones, 2.9% de misses proxy y
  p95 de 598 ms; no se justifica watcher. T6.2/T6.3 siguen WIP: el proceso
  fresco de Codex alcanzó bootstrap pero sus hooks/plugins fallaron antes del
  cierre, y Claude CLI sólo emitió errores de reglas de permisos. G6 no pasa
  a review hasta repetir ambos smokes en superficies sanas.
- **Fase 5 ejecutada; G5 en `review` (2026-08-08).** T5.1–T5.4 cerradas.
  `[[AGENTS OS]]` vive en `10-projects/Personal/AGENTS OS/` con identidad,
  parent, task bridge y `area: [[Personal]]` preservados. Evidencia: lint
  dirigido `0/0`; doctor estricto `0/0/0`; pack 145 archivos con hashes/ZIP
  PASS; Graphify 5465/6284 y `explain` al nuevo path con backlinks. Rollback
  exacto y checklist reusable registrados en
  `80-agents/journal/logs/2026-08-08-agents-os-fase5-project-layout-pilot.md`.
  Recomendación: **GO** para conservar el piloto; **NO-GO temporal** para un
  retrofit masivo hasta verificar/automatizar el rescan de caches de plugins
  path-based en una vista real. La caché derivada de Task Board quedó stale
  tras el move externo; las fuentes canónicas no. F6 no se inicia sin
  aceptación humana de G5.
- **Fase 5 iniciada; T5.1 en WIP (2026-08-08).** G4 está `accepted` y
  habilita el piloto. Se inventarían referencias físicas a
  `10-projects/AGENTS OS/` y se prepara un move map/rollback exacto antes de
  mover archivos. Alcance acotado al árbol AGENTS OS; otros proyectos,
  archive, journal y outputs generados quedan fuera del lote.
- **T5.1 cerrada; T5.2 en WIP (2026-08-08).** Inventario: 8 archivos físicos
  (2 entidades project, 5 archivos del builder/pack y 1 prompt), sin symlinks;
  destino `10-projects/Personal/AGENTS OS/` inexistente. Referencias operativas
  seleccionadas: `.graphifyignore`, README raíz, mapa `agents-os.md`, skill
  `agents-os-install` y cuatro archivos del pack. Historia, archive, journal,
  `.trash`, outputs y cachés Graphify quedan intactos. El baseline del pack
  falló antes del move por una referencia obsoleta a
  `AGENTS OS - Beta y Hardening`; se reemplaza por el planificador activo.
  Rollback exacto: mover el árbol destino al path origen y revertir el mismo
  set de referencias; checksums SHA-256 pre-move capturados para los 8 archivos.
- **T5.2 cerrada; T5.3 en WIP (2026-08-08).** El árbol completo fue movido a
  `10-projects/Personal/AGENTS OS/`; el origen ya no existe y no cambió ningún
  título canónico. Se actualizaron `.graphifyignore`, README raíz, mapa
  `agents-os.md`, `agents-os-install` y el builder/selección del pack. El pack
  ahora selecciona el parent y `[[AGENTS OS - Fase 2]]`, no el proyecto
  archivado Beta/Hardening. Se inicia validación funcional y de rollback.
- **T5.3 cerrada; T5.4 en WIP (2026-08-08).** Lint dirigido del parent y
  planificador `ERROR=0 WARN=0` (2 notas); doctor estricto
  `HIGH=0 MEDIUM=0 LOW=0`; pack regenerado (145 archivos, hashes y ZIP PASS);
  Graphify reindex exit 0 (5465 nodos/6284 edges) y `explain "AGENTS OS"`
  resuelve de forma única al nuevo path con backlinks vigentes. El pack está
  fuera del grafo y no existen Bases activas. Parent bridge y tareas internas
  se leen desde el nuevo path. Limitación de superficie: la caché derivada del
  plugin Task Board conserva rutas anteriores y requiere rescan desde Obsidian;
  no se editó manualmente como fuente canónica.
- **Fase 4 ACEPTADA; G4 `accepted` por el owner (2026-08-08).** T4.1–T4.5
  cerradas. El owner aceptó el re-review sin observaciones pendientes tras
  corregir los dos bloqueantes: (1) Resource Wiki rechaza sólo variantes legacy
  y enumera `methodologies/` + `methodologies/sdd/`; (2) el contrato federado
  separa `quick_validate.py` portable del frontmatter S1 extendido. El
  validador se ejecutó con Python 3.10.16 y 3.12.9: ambos dieron exit 1 esperado
  por `created, scope, tags, type, updated`. La validación federada equivalente
  quedó verde: lint exacto de la skill `0/0` (1 nota), parse YAML skill/UI PASS
  y `$sdd-workflow` consistente. URL Kiro canónica:
  `https://kiro.dev/docs/specs/`. Contrato Resource Wiki y dominio activo
  `methodologies/sdd` con seis páginas, cinco notas source, provenance y
  lifecycle; skill transversal federada `sdd-workflow`; ingest/query/lint
  verificados. La query SDD recuperó como top results `SDD — Lifecycle`, el
  índice y las fuentes GitHub/Kiro. Evidencia: templates 19 `0/0`; dominio SDD
  13 `0/0`; skill `0/0`; doctor estricto `HIGH=0 MEDIUM=0 LOW=0`; gate global
  warn-first `ERROR=237 WARN=84`; reindex exit 0 (5465 nodos/6284 edges); cero
  specs concretas copiadas. **F5 quedó habilitada, pero F5/T5.1 no fue
  iniciada.** Próximo paso exacto: T5.1, inventariar referencias y preparar
  move/rollback del piloto antes de cualquier movimiento. Evidencia consolidada:
  `80-agents/journal/logs/2026-08-08-agents-os-fase4-resource-wiki-sdd.md`.
- **Fase 3 ACEPTADA; G3 accepted por el owner (2026-08-08).** Cerrados los tres
  bloqueantes de la revisión: (1) `methodology/source` definidos en schema S2,
  lint y templates para el handoff F4; (2) lint ampliado a campos base/core,
  frontera de templates y reglas duras S1 (`status` ahora ERROR); (3) templates
  S1/S2 y routing de lifecycle/update/capture reconciliados. Evidencia vigente:
  templates `ERROR=0 WARN=0` (31), fixtures válidas `0/0` (6), fixtures
  inválidas `ERROR=8 WARN=0` (8, un assert aislado por archivo), hash read-only
  PASS. El baseline estricto ahora expone el drift real: `ERROR=237 WARN=87`
  sobre 471 notas; el gate warn-first lo reporta y **no bloquea**
  `graphify-obsidian update` (exit 0, 5320 nodos/6095 edges). Doctor estricto
  verde `HIGH=0 MEDIUM=0 LOW=0` startup≈4979. El owner revisó y aceptó G3;
  F4 queda habilitada e **iniciada** con T4.1 en WIP. Evidencia consolidada de
  G3:
  `80-agents/journal/logs/2026-08-07-agents-os-fase3-schema-lint-gate.md`.
  Próxima tarea exacta: T4.1 normalizar contrato resource wiki.
- **Fase 2 ejecutada; G2 aceptado por el owner (2026-08-07).** G1 aceptado por
  owner. Registry federado
  construido (INDEX con core + sección federada), ownership de las 32 skills
  clasificado, transversales extraídas a `30-resources/agents-skills/` (D14,
  in-vault). Doctor federation-aware y estricto en verde (`HIGH=0 MEDIUM=0
  LOW=0`, startup ≈4979, exit 0). Nesting físico del core descartado (D14).
  **Gaps cerrados:** (1) **forward-test** ejecutado en superficie Claude Code
  (proceso fresco): discovery HIT de skill core `agents-os-doctor` y federadas
  `sync-local-branch`/`fury-lib-consumer-deploy` vía registry federado; limitación
  de superficie registrada (el registro nativo de Claude Code solo expone
  bootstrap; el resto se descubre por el registry leído con file-tools).
  (2) **repo owner Echo Forge/SQX HALLADO**: `xKoRx/symphony`
  (`~/go/src/github.com/xKoRx/symphony`, no en `~/fuentes/`); **piloto
  `sqx-plugin-lifecycle` migrada** (sin copia) a su `.agents/skills/`; INDEX
  actualizado; las otras 2 quedan pendientes (repo hallado, ya no bloqueadas).
  Tras `G2 accepted`: Fase 3 (T3.1), donde vive el lint de frontmatter + gate
  warn-first.
- El cockpit padre [[AGENTS OS]] fue compactado y contiene una sola tarea
  puente WIP hacia este proyecto.
- Los proyectos [[AGENTS OS - Hot Path y Cierre Silencioso]] y
  [[AGENTS OS - Beta y Hardening]] fueron archivados; sus pendientes relevantes
  están incorporados en Fase 2.
- Se retiraron `Finish Tasks` y `Progress Log` de 22 skills. No se creó memoria
  redundante porque los hechos durables ya vivían en procedimientos, contratos
  o proyectos. El gate runtime de SQX fue conservado con nombre correcto.
- El doctor actual reporta una referencia de skill rota, `.obsidian/` ausente
  de `.graphifyignore` y dos falsos positivos de portabilidad sobre paths
  remotos válidos. Estos hallazgos entran en Fase 1.
- El vault está respaldado a nivel de infraestructura; no se requiere snapshot
  ni mecanismo de recuperación adicional.

## Resultado del cierre

1. Deuda metadata reducida `237→41 ERROR`; residuo ambiguo scoped, sin inventar
   semántica.
2. Rescan de caches path-based validado por el owner en una vista real.
3. Gate estricto en NO-GO; `warn-first` permanece vigente hasta limpiar o
   excluir contractualmente el residuo.

## Baseline y clases de evidencia

| Evidencia | Estado | Fuente |
|---|---|---|
| Runtime core | HEAD Markdown del vault | `VAULT_ROOT/80-agents/agents-os/agents-os.md` |
| Bootstrap | HEAD Markdown del vault | `VAULT_ROOT/80-agents/skills/agents-os-bootstrap/SKILL.md` |
| Retrieval | HEAD Markdown del vault | `VAULT_ROOT/80-agents/skills/agents-os-context-retrieval/SKILL.md` |
| Schema S1 | CONTRACT | `VAULT_ROOT/80-agents/skills/_shared/metadata-schema.md` |
| Convenciones S2 | CONTRACT parcial | `VAULT_ROOT/90-system/convenciones.md` |
| Templates S2 | IMPLEMENTATION parcial | `VAULT_ROOT/70-templates/project.md` |
| LLM Wiki | CONTRACT parcial | `VAULT_ROOT/30-resources/00-RESOURCE-WIKI.md` |
| Auditoría | TEST/lint | `VAULT_ROOT/80-agents/skills/agents-os-doctor/scripts/doctor.py` |
| Historia Fase 1 | REPORT/ROADMAP | `VAULT_ROOT/40-archive/agents-os-projects/AGENTS OS - Fase 1 - Historial.md` |

## Matriz requerimiento → evidencia

| ID | Requerimiento | Estado | Evidencia/gap | Fase |
|---|---|---|---|---|
| R1 | Un entrypoint universal y mínimo | done | `AGENTS.md` mínimo resuelve `VAULT_ROOT` e invoca bootstrap | F1 |
| R2 | Una autoridad por procedimiento | done | bootstrap/retrieval/cierre tienen una fuente canónica cada uno | F1 |
| R3 | Skills sin historia runtime | done | 22 skills limpiadas; change log 2026-08-01 | F0 |
| R4 | Skills organizadas por ownership | done | core en `80-agents`, transversales federadas y skill piloto en repo owner | F2 |
| R5 | App skills junto a su aplicación | done | registry federado resuelve repo owner y evita copias en el vault | F2 |
| R6 | Schema S1 y S2 no competitivo | done | metadata-schema=autoridad S1, convenciones=autoridad S2; lint aplica ambos | F3 |
| R7 | Frontmatter consistente y validable | partial | lint all-vault operativo + templates verdes; retrofit de notas live pendiente (plan por área en el log F3) | F3 |
| R8 | LLM Wiki armónica | done | contrato, índices activos, provenance y lifecycle validados | F4 |
| R9 | SDD documentado y ejecutable sin duplicar | done | dominio methodology + skill federada; cero specs concretas copiadas | F4 |
| R10 | Proyectos subdivididos por área | partial | piloto `10-projects/Personal/AGENTS OS/` verde; retrofit masivo condicionado al rescan de plugins path-based | F5 |
| R11 | Continuidad con otro agente | done | Desktop + proceso fresco CLI recuperaron bootstrap, planner y registry sin reexplicación material | F6 |
| R12 | Valor medido más allá de tokens | done | cold/warm/swap, reexplicación, calidad y proxy hit/miss registrados | F6 |
| R13 | Lint de frontmatter all-vault + gate pre-execute graphify | done | `lint.py` all-vault read-only + gate warn-first cableado en `graphify-obsidian update` (probado: no bloquea, `update` exit 0). Flip a bloqueante condicionado al retrofit (D12) | F3 |
| R14 | Uso y utilidad de graphify-obsidian medidos | done | 279 operaciones analizadas; miss proxy 2.9% y p95 598 ms; watcher descartado | F6 |

## Alcance

- Runtime y documentación canónica de AGENTS OS.
- Estructura y discovery de skills del vault.
- Schema, templates y lint de Sistema 1/Sistema 2.
- LLM Wiki sobre `30-resources/` y metodologías.
- Piloto de reorganización física usando AGENTS OS/Personal.
- Validación Graphify y forward-tests con agentes frescos.

## Fuera de alcance

- Reorganizar masivamente todo el vault antes del piloto.
- Copiar skills de aplicaciones al vault cuando el repositorio es su owner.
- Convertir cada proyecto en una wiki.
- Instalar embeddings, vector DB o Graphify semántico sin evidencia de necesidad.
- Reescribir documentación histórica archivada.
- Cambiar metodologías o reglas de negocio de aplicaciones concretas.

## Registro de decisiones

| ID | status | resolución | fuente/evidencia | fase |
|---|---|---|---|---|
| D1 | CONFIRMED | El agente entra por `AGENTS.md` y éste invoca directamente bootstrap; no encadena `agents-os.md` | decisión del owner 2026-08-01 | F1 |
| D2 | CONFIRMED | Se permite repetir un recordatorio/puntero, nunca el procedimiento completo | decisión del owner 2026-08-01 | F1 |
| D3 | CONFIRMED | `context-router.md` será doc humano; la skill retrieval conserva el algoritmo | owner: "no duplicar" | F1 |
| D4 | TECHNICAL_RESOLUTION | El schema es documento; templates lo instancian; skill+script lo aplican | separación de responsabilidades | F3 |
| D5 | CONFIRMED | Skills AGENTS OS gobiernan el vault; skills de app viven con la app/repositorio | decisión del owner 2026-08-01 | F2 |
| D6 | TECHNICAL_RESOLUTION | `80-agents/skills/` será registry root federado, no carpeta plana ni copia universal | ownership + anti-drift | F2 |
| D7 | CONFIRMED | SDD reusable vive como knowledge domain en resources; ejecución en skill; specs concretas en proyecto/repo | decisión del owner 2026-08-01 | F4 |
| D8 | CONFIRMED | LLM Wiki se implementa con una skill global, no dentro del proyecto | decisión del owner 2026-08-01 | F4 |
| D9 | TECHNICAL_RESOLUTION | `area:` es autoridad semántica; carpetas por área son navegación validable | evita depender del path | F5 |
| D10 | TECHNICAL_RESOLUTION | Proyectos anteriores se archivan y Fase 2 queda como planificador único | contrato de proyecto de agente | F0 |
| D11 | TECHNICAL_RESOLUTION | Referencias de planes usan el prefijo simbólico `VAULT_ROOT/` con una ruta relativa; nunca una URI absoluta ni un path de máquina | constitución de portabilidad | F0 |
| D12 | CONFIRMED | El lint de frontmatter corre como gate pre-execute de `graphify-obsidian update` en modo warn-first (reporta+cuenta, no bloquea); pasa a estricto tras el retrofit | decisión del owner 2026-08-06 | F3 |
| D13 | CONFIRMED | La medición de uso/utilidad de `graphify-obsidian` (sobre `query-log.jsonl` + proxy hit/miss) se hace en Fase 6; no se instrumenta nada nuevo antes | decisión del owner 2026-08-06 | F6 |
| D14 | CONFIRMED | Las skills transversales (ni core AGENTS OS ni de una app) viven **in-vault** bajo `30-resources/agents-skills/`, registradas en el INDEX federado (enlaza, no copia). El conocimiento de metodologías (SDD/RFC/PM, Fury deploy) va como knowledge domain en `30-resources/methodologies/` (F4). Refina D6 y la topología: `80-agents/skills/` queda solo con core agents-os (+ vault-ops); NO se usa repo externo | decisión del owner 2026-08-06 | F2 |

## Política de repetición

1. **Autoridad:** regla/procedimiento completo en una sola fuente.
2. **Recordatorio:** una línea y un link a la autoridad; puede repetirse en un
   boundary como `AGENTS.md`.
3. **Derivado:** índice, pack o snapshot generado; nunca se edita como verdad.
4. **Prohibido:** copiar algoritmos, listas de skills, thresholds o secuencias
   entre guía, constitución, proyecto y skills.

## Arquitectura actual

```text
AGENTS.md (hook + reglas repetidas)
  → bootstrap
  → agents-os.md / constitución / router con zonas solapadas
  → 80-agents/skills/* plano
  → schemas S1/S2 parcialmente mezclados
  → resources wiki parcial + Graphify derivado
```

## Arquitectura objetivo

```text
AGENTS.md
  └── agents-os-bootstrap
      ├── base cold/warm/swap
      ├── context retrieval
      │   ├── entidad/proyecto canónico
      │   ├── 00-index.md / LLM Wiki
      │   └── Graphify para relaciones
      └── una skill especializada por ownership

Sistema 1: 80-agents/{agents-os,memory,skills,journal,templates}
Sistema 2: 10-projects, 20-areas, 30-resources, apps/repos
Derivados: 95-graphify, graphify-out, outputs
Gobierno S2: 90-system/convenciones.md + 70-templates + lint
```

## Matriz de autoridad objetivo

| Fuente | Responsabilidad única | No contiene |
|---|---|---|
| `AGENTS.md` | Resolver root e invocar bootstrap | cold/warm, Graphify, cierre, skill list |
| bootstrap | Startup y routing | rationale, historia, estado de proyecto |
| `agents-os.md` | Mapa humano de autoridades | procedimiento ejecutable |
| constitución | Invariantes duras | ejemplos y secuencias extensas |
| Context Retrieval skill | Algoritmo de selección/carga | evangelización y roadmap |
| `context-router.md` | Concepto, valor y ejemplos humanos | algoritmo duplicado |
| skills | Procedimiento runtime | `Finish Tasks`, progress logs |
| proyecto | Estado, plan, gates y decisiones | reglas runtime duplicadas |
| journal | Historia y evidencia | autoridad vigente |

## Topología de skills objetivo

```text
80-agents/skills/
├── INDEX.md                    # registry federado
├── _shared/                   # contratos compartidos
├── agents-os/                 # gobierna el vault
├── methodologies/             # SDD/RFC/PM transversales
└── shared/                    # workflows realmente generales

<application-repo>/
├── AGENTS.md                   # entrypoint local fino
└── .agents/skills/            # skills propiedad de la app
```

Reglas:

- El registry puede apuntar a skills externas; no copia su contenido.
- La entidad `application` registra `repo`, `path`, `agent_entrypoint` y
  `skills_root` cuando corresponda.
- Una skill cross-app queda en `shared/` o `methodologies/` sólo si ningún repo
  es claramente su owner.
- Discovery específico de una superficie puede usar un shim/pointer mínimo,
  nunca una segunda fuente semántica.

## Matriz de ownership de skills (T2.1)

Clasificación de las 32 skills en disco (2026-08-06). Repos owner verificados en
`~/fuentes/` cuando aplica.

| Clase | Skills | Target de ownership (D14) |
|---|---|---|
| **core agents-os + vault-ops** (27) | 26 `agents-os-*` + `operational-healthcheck-policy` (reclasificada: es sobre la salud del propio Second Brain, no transversal; `status: draft`) | vault `80-agents/skills/` |
| **transversal → agents-skills** (1) | `sync-local-branch` (git genérico; dev-workflow) | ✅ `30-resources/agents-skills/sync-local-branch/`, federada en INDEX |
| **metodología cross-app** (1) | `fury-lib-consumer-deploy` (Fury deploy `java-polycard-sdk`→consumers) | ✅ skill en `30-resources/agents-skills/fury-lib-consumer-deploy/`; conocimiento → `30-resources/methodologies/` (F4) |
| **app-owned Echo Forge/SQX** (3) | `echo-forge-wfm-troubleshooting` · `sqx-temporal-failure-audit` · `sqx-plugin-lifecycle` | repo owner **hallado**: `xKoRx/symphony` `.agents/skills/` (2026-08-07). **`sqx-plugin-lifecycle` migrada (piloto)**; las otras 2 pendientes (ya no bloqueadas) |

Estado actual verificado: **cada skill tiene una sola fuente física** (no hay
copias en `.agents/`/`.claude/`); el assert "un solo source path" ya se cumple.

### Implicación de D14 (de-risking del nesting)

El problema original de la "carpeta plana" (D6: mezcla core + dominio + app) se
resuelve **extrayendo** las skills no-core, no anidando las 26 core:

- ✅ transversal (1) y metodología cross-app (1) → `30-resources/agents-skills/` (hecho); app-owned Echo Forge/SQX (3) → repo owner (bloqueado, repo no hallado).
- Al quedar `80-agents/skills/` solo con core agents-os (+ vault-ops + 3 app bloqueadas), **el nesting físico de las 26 core en `agents-os/` deja de ser necesario para separar ownership** (era la parte de mayor blast radius: refs `../_shared/`, doctor path-math, paths de bootstrap/retrieval, adapters de superficie que asumen layout plano). Queda como sub-decisión opcional/cosmética, no como requisito de G2.
- La federación real la da el **INDEX apuntando a fuentes fuera del core** (`30-resources/agents-skills/` + repos de app), no el movimiento de core. El doctor ahora valida los targets federados.

## Schema y frontmatter objetivo

| Capa | Autoridad | Enforcement |
|---|---|---|
| Sistema 1 | `_shared/metadata-schema.md` | doctor + templates 80-agents |
| Sistema 2 | `90-system/convenciones.md` | templates 70 + entity lifecycle |
| Tags | vocabulario S2 + campos semánticos | lint determinístico |
| Identidad | title canónico + aliases + slug | duplicate/link lint |

El schema no es una skill. `agents-os-entity-lifecycle` orquesta creación,
rename, move, merge y validación; un script determinístico valida campos,
tipos, estados y templates. No se crea otra skill antes de consolidar las
fronteras de `entity-lifecycle`, `entity-update` y `note-capture`.

## LLM Wiki armónica

```text
fuentes crudas inmutables
  → ingest
  → páginas Markdown canónicas
  → 00-index.md curado
  → links/provenance/freshness
  → Graphify derivado
```

- La skill global `agents-os-resource-wiki` implementa ingest/query/lint.
- `30-resources/00-RESOURCE-WIKI.md` explica el schema humano.
- Un proyecto conserva estado en su nota; sólo usa `docs/00-index.md` si su
  documentación crece como dominio de conocimiento.
- Cada dominio curado define provenance, `last_verified` cuando aplique,
  confianza respaldada y lifecycle de reemplazo/deprecación.
- Un índice existe para seleccionar qué abrir; si no reduce lectura, se divide
  o se elimina.

## SDD y metodologías

```text
30-resources/methodologies/sdd/
├── 00-index.md
├── overview.md
├── lifecycle.md
├── artifact-model.md
├── quality-gates.md
├── roles.md
├── anti-patterns.md
├── log.md
└── _sources/

80-agents/skills/methodologies/sdd-workflow/SKILL.md
<project-or-repo>/specs/
```

- Resources contiene conocimiento reusable y curado.
- La skill contiene el procedimiento ejecutable.
- `specs/` contiene instancias concretas y estado real.
- Learnings/known errors reusables se promueven a memoria sólo si cambian una
  acción futura; no se duplica la metodología completa en memoria.

## Layout de proyectos objetivo

```text
10-projects/
├── Meli/<Proyecto>/<Proyecto>.md
├── Personal/<Proyecto>/<Proyecto>.md
├── Echo/<Proyecto>/<Proyecto>.md
├── Aranea/<Proyecto>/<Proyecto>.md
└── _planning/
```

- Una carpeta por proyecto.
- La nota principal comparte nombre con la carpeta.
- `area:` sigue siendo la autoridad; el path sólo refleja navegación.
- `parent:` expresa jerarquía; no se infiere de nesting.
- `agentes/`, `docs/`, `specs/` y `sources/` aparecen sólo cuando aplican.
- El piloto es AGENTS OS; el retrofit masivo requiere gate posterior.

## Estrategia de carga

| Intención | Entrada | Escala a |
|---|---|---|
| Startup | bootstrap | base scoped + entidad |
| Estado de proyecto | nota controladora | docs/evidencia seleccionada |
| Hecho de dominio | metadata/00-index | una página canónica |
| Relación/impacto | Graphify | cuerpos involucrados |
| Metodología | índice methodology | skill si se ejecutará |
| Operación app | entity → repo entrypoint | skill canónica del repo |

## Calidad y métricas

- Tiempo hasta primera acción útil.
- Tokens nuevos en cold, warm y cambio de entidad.
- Reexplicación que el usuario debió aportar.
- Errores prevenidos por memoria/documentación recuperada.
- Respuestas respaldadas por fuentes canónicas.
- Precisión del selector de skills y tasa de fallback.
- Drift detectado por lint estructural vs auditoría semántica.
- Costo de mantener índices frente a su utilidad real.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Registry federado no descubierto por una superficie | forward-test fresco + shim pointer mínimo si es necesario |
| Over-engineering del schema | piloto por tipos area/project/application antes de retrofit |
| LLM Wiki se vuelve copia | canonical-home check y provenance obligatoria |
| Proyecto Fase 2 se vuelve otra constitución | no cargar en startup; sólo estado/plan/evidencia |
| Índices crecen demasiado | subíndices por smell-test y métrica de selección |
| Doctor genera falsos positivos | clasificar vault paths vs runtime paths externos |
| Skills app quedan huérfanas | entidad application + registry federado + repo AGENTS |

## Roadmap dependency-ordered

| Fase | Resultado | Carga relativa | Gate |
|---|---|---|---|
| 0 | Baseline medible del sistema actual | baja | G0 |
| 1 | Autoridades y doctor coherentes | media | G1 |
| 2 | Skills por ownership + discovery federado | alta | G2 |
| 3 | Schema S1/S2 + templates + lint | alta | G3 |
| 4 | LLM Wiki + SDD/metodologías | media-alta | G4 |
| 5 | Piloto de layout por área con AGENTS OS | alta | G5 |
| 6 | Forward-tests, métricas y decisión de adopción | alta | G6 |
| 7 | Retrofit gradual de metadata + caches path-based + decisión de gate estricto | alta | G7 |

## Paquetes autónomos

### Paquete autónomo Fase 0 — Baseline

**Misión exacta**

Capturar una fotografía reproducible del sistema actual antes de modificar
autoridades, paths o topología. El vault está respaldado a nivel de
infraestructura; esta fase solo mide, no protege.

**Precondiciones verificables**

- Proyecto Fase 2 validado.
- Tarea puente WIP en [[AGENTS OS]].
- Ningún movimiento estructural adicional iniciado.

**Lectura obligatoria**

- Secciones `Estado actual`, `Baseline` y `Registro de decisiones` de esta nota.
- `VAULT_ROOT/80-agents/skills/agents-os-doctor/SKILL.md`
- `VAULT_ROOT/.graphifyignore`

**Decisiones cerradas**

- El vault está respaldado por infraestructura; no se requiere snapshot ni
  mecanismo de recuperación adicional.
- El baseline es medición, no fuente canónica ni corpus Graphify.

**Implementación paso a paso**

1. Ejecutar doctor y registrar su output completo (errores, warnings, conteos).
2. Contar skills, notas por tipo, variantes de frontmatter detectadas.
3. Medir tiempo de startup cold (archivos leídos, tokens estimados).
4. Registrar dominios Graphify activos y estado de `.graphifyignore`.
5. Actualizar esta nota y dejar G0 en `review`.

**Archivos esperados**

- modify: esta nota (progreso, estado actual, bitácora).
- create: log de baseline bajo `VAULT_ROOT/80-agents/journal/hygiene/`.

**No tocar**

- Runtime core, topología de skills, templates y paths de proyectos.

**Spikes permitidos**

- Ninguno. La medición no exige exploración nueva.

**Tests y asserts**

- Doctor output registrado con fecha y conteos reproducibles.
- Startup baseline incluye archivos core leídos y tokens estimados.
- Log de baseline no aparece en el corpus Graphify normal.

**Entregables/Gate G0**

- Log de baseline con doctor output, conteos y startup measurement en `review`.

**Handoff a Fase 1**

- Fase 1 recibe rutas core verificadas, baseline y rollback probado.

### Paquete autónomo Fase 1 — Autoridades y doctor

**Misión exacta**

Eliminar duplicación procedural y hacer que el doctor represente correctamente
el contrato vigente.

**Precondiciones verificables**

- G0 `accepted` por el owner.

**Lectura obligatoria**

- Matriz de autoridad y política de repetición de esta nota.
- `VAULT_ROOT/AGENTS.md`
- `VAULT_ROOT/80-agents/skills/agents-os-bootstrap/SKILL.md`
- `VAULT_ROOT/80-agents/agents-os/context-router.md`
- `VAULT_ROOT/80-agents/skills/agents-os-context-retrieval/SKILL.md`

**Decisiones cerradas**

- `AGENTS.md` apunta directo a bootstrap.
- `agents-os.md` no es always-read.
- Context Router humano no duplica el algoritmo.
- Paths remotos de un runtime no son automáticamente paths locales no portables.

**Implementación paso a paso**

1. Adelgazar `AGENTS.md` a resolver root + invocar bootstrap.
2. Compactar `context-router.md` a concepto/rationale/ejemplos.
3. Eliminar instrucciones startup/cierre obsoletas fuera de autoridades.
4. Reparar la referencia relativa rota de SQX.
5. Agregar `.obsidian/` a `.graphifyignore`.
6. Reubicar la nota rogue `agents-os/agent-memory` según su tipo.
7. Refinar doctor para distinguir vault paths de paths operacionales remotos.
8. Ejecutar doctor estricto y actualizar G1.

**Archivos esperados**

- modify: AGENTS, context-router, doctor, graphifyignore, skill SQX.
- move: nota rogue hacia memoria pública/interna canónica.
- modify only if needed: mapa `agents-os.md` y constitución.

**No tocar**

- Topología física de skills y schema S2.

**Spikes permitidos**

- Ninguno; una contradicción nueva produce `PLAN_CONFLICT`.

**Tests y asserts**

- Una sola receta executable de startup.
- Doctor sin falso positivo para paths remotos conocidos.
- Cero refs rotas core; `.obsidian/` excluido.
- Startup estimado no aumenta.

**Entregables/Gate G1**

- Patch atómico, change log, doctor estricto y diff de autoridad en `review`.

**Handoff a Fase 2**

- Fase 2 recibe un runtime estable y un doctor confiable.

### Paquete autónomo Fase 2 — Skills por ownership

**Misión exacta**

Transformar la carpeta plana en un registry federado sin duplicar skills ni
romper discovery.

**Precondiciones verificables**

- G1 `accepted`.

**Lectura obligatoria**

- Topología objetivo y D5/D6 de esta nota.
- `VAULT_ROOT/80-agents/skills/INDEX.md`
- `VAULT_ROOT/80-agents/skills/_shared/skill-contract.md`
- `VAULT_ROOT/80-agents/skills/agents-os-install/SKILL.md`

**Decisiones cerradas**

- Core AGENTS OS queda bajo el registry del vault.
- Skills app-specific quedan en el repo owner cuando sea posible.
- El registry enlaza; nunca copia.

**Implementación paso a paso**

1. Clasificar cada skill: agents-os, methodology, shared, domain o app-owned.
2. Resolver owner/repo de las app-specific mediante entidades application.
3. Definir manifest/registry portable con ubicación canónica y trigger.
4. Mover core a subcarpetas sin romper refs relativas ni tooling.
5. Migrar una skill app piloto a su repo owner o registrar bloqueo explícito.
6. Adaptar bootstrap/install/doctor al registry recursivo/federado.
7. Forward-test discovery desde proceso fresco.

**Archivos esperados**

- modify: INDEX, bootstrap, install, doctor y skill refs.
- create: estructura agents-os/methodologies/shared.
- conditional move: skill app piloto al repo owner.

**No tocar**

- Schema S2, templates y estructura física de proyectos.

**Spikes permitidos**

- Discovery multisuperficie: comparar registry, path explícito y shim pointer;
  salida: tokens, latencia, tasa de éxito y limitación por superficie.

**Tests y asserts**

- Cada skill tiene un solo source path.
- Todos los registry targets resuelven.
- Codex y al menos otra superficie descubren una skill core y la piloto.
- Ningún adapter contiene reglas semánticas duplicadas.

**Entregables/Gate G2**

- Registry federado, matriz de ownership y forward-test en `review`.

**Handoff a Fase 3**

- Fase 3 recibe lifecycle/doctor con paths definitivos.

### Paquete autónomo Fase 3 — Schema S1/S2

**Misión exacta**

Separar contratos de metadata, alinear templates y crear lint determinístico
antes de migrar notas.

**Precondiciones verificables**

- G2 `accepted`.

**Lectura obligatoria**

- Schema objetivo de esta nota.
- `VAULT_ROOT/80-agents/skills/_shared/metadata-schema.md`
- `VAULT_ROOT/90-system/convenciones.md`
- `VAULT_ROOT/70-templates/project.md`
- `VAULT_ROOT/70-templates/area.md`

**Decisiones cerradas**

- S1 y S2 tienen autoridades separadas.
- Schema es documento; skill+script lo aplica.
- No se hace retrofit masivo en esta fase.

**Implementación paso a paso**

1. Restringir metadata-schema a memoria/journal/runtime S1.
2. Expandir convenciones S2 con tipos, campos base y estados por tipo.
3. Definir campos core vs opcionales; eliminar YAML ceremonial.
4. Alinear templates area/project/application/index/idea/tool.
5. Consolidar frontera lifecycle/update/capture sin crear otra skill.
6. Crear lint read-only all-vault y fixtures de notas válidas/inválidas (D4:
   el schema es documento; el script lo aplica).
7. Auditar tipos reales y producir plan de retrofit por área.
8. (R13/D12) Cablear el lint como gate **pre-execute** de `graphify-obsidian
   update`, en el branch `update` del wrapper portable
   `VAULT_ROOT/95-graphify/dist/graphify-obsidian`, justo antes de invocar el
   extractor. Modo **warn-first**: reporta y cuenta violaciones sin bloquear
   `update`; los subcomandos query/path/explain/affected no se tocan (no
   reindexan). El flip a bloqueante queda condicionado al retrofit (post-G3).

**Archivos esperados**

- modify: metadata-schema, convenciones y templates seleccionados.
- create: script de lint + fixtures bajo la skill lifecycle.
- create: reporte de divergencia fuera del corpus normal.
- modify: wrapper `95-graphify/dist/graphify-obsidian` (invocación warn-first
  del lint en el branch `update`). Nota: la copia instalada en `~/bin` es
  derivada; la fuente canónica portable es la del vault.

**No tocar**

- Notas live en masa; sólo fixtures y un piloto explícito.
- La lógica de indexación del wrapper; sólo se añade el gate no bloqueante.

**Spikes permitidos**

- Parser YAML/Templater para decidir enforcement sin reescritura accidental.

**Tests y asserts**

- Templates pasan lint.
- Tipos/status no definidos fallan con mensaje accionable.
- S1 no exige `status`; S2 define status por lifecycle.
- El lint no modifica archivos en modo check.
- El gate warn-first **no** bloquea `graphify-obsidian update` con el drift
  actual (141 sin type + 63 variantes); emite reporte/conteo y `update` completa.
- El lint recorre todas las notas del vault (excluye lo de `.graphifyignore`).

**Entregables/Gate G3**

- Contratos separados, templates verdes, lint all-vault + gate warn-first
  integrado y reporte de retrofit en `review`.

**Handoff a Fase 4**

- Fase 4 recibe tipos `resource/index/methodology/source` definidos.

### Paquete autónomo Fase 4 — LLM Wiki y SDD

**Misión exacta**

Convertir LLM Wiki en un lifecycle de conocimiento coherente y demostrarlo con
el dominio SDD, sin duplicar specs concretas.

**Precondiciones verificables**

- G3 `accepted`.

**Lectura obligatoria**

- Secciones LLM Wiki y SDD de esta nota.
- `VAULT_ROOT/30-resources/00-RESOURCE-WIKI.md`
- `VAULT_ROOT/30-resources/LLM Wiki.md`
- `VAULT_ROOT/80-agents/skills/agents-os-resource-wiki/SKILL.md`

**Decisiones cerradas**

- Una skill global implementa wiki.
- Resources contiene metodología reusable; specs concretas quedan con proyecto/repo.
- Graphify es derivado; `00-index.md` es selección curada.

**Implementación paso a paso**

1. Normalizar casing `00-index.md`, log y dominio activo.
2. Definir provenance, freshness, confidence y lifecycle de reemplazo.
3. Ajustar la skill resource-wiki al schema S2 sin duplicar reglas.
4. Crear `methodologies/sdd/` desde templates.
5. Ingerir fuentes SDD existentes de forma incremental y trazable.
6. Crear/ajustar skill ejecutable SDD que referencie el dominio.
7. Lint del dominio y query de prueba con citas.

**Archivos esperados**

- modify: resource wiki schema/skill.
- create: dominio methodologies/sdd, índice, log, fuentes y páginas.
- create or modify: skill methodology SDD.

**No tocar**

- Specs concretas de proyectos/apps salvo links de autoridad.
- Otros dominios resource en masa.

**Spikes permitidos**

- Umbral de subíndices basado en tamaño/selección; no embeddings.

**Tests y asserts**

- Query SDD entra por index y abre sólo fuentes seleccionadas.
- Ninguna spec concreta se duplica en methodologies.
- Provenance resuelve; log registra ingest/query/lint.
- Graphify no indexa `_sources` pesadas ni outputs.

**Entregables/Gate G4**

- Dominio SDD operativo, skill y prueba de retrieval en `review`.

**Handoff a Fase 5**

- Fase 5 recibe schema/lifecycle e índices listos para el piloto físico.

### Paquete autónomo Fase 5 — Piloto de proyectos por área

**Misión exacta**

Probar el layout `10-projects/Personal/AGENTS OS/` sin romper identidad,
entrypoints, packs ni retrieval.

**Precondiciones verificables**

- G4 `accepted` y backup probado.

**Lectura obligatoria**

- Layout objetivo y riesgos de esta nota.
- `VAULT_ROOT/10-projects/Personal/AGENTS OS/AGENTS OS.md`
- `VAULT_ROOT/90-system/convenciones.md`
- `VAULT_ROOT/80-agents/skills/agents-os-vault-refactor/SKILL.md`

**Decisiones cerradas**

- `area:` manda; carpeta refleja navegación.
- Una carpeta por proyecto; nota principal con mismo nombre.
- AGENTS OS es el único piloto antes del retrofit amplio.

**Implementación paso a paso**

1. Inventariar refs físicas a `10-projects/AGENTS OS`.
2. Diseñar move map y rollback exacto.
3. Mover a `10-projects/Personal/AGENTS OS/`.
4. Reparar scripts, packs, ignores y refs path-based.
5. Validar wikilinks, Dataview, tasks y Graphify.
6. Medir fricción y decidir si el layout escala al resto.

**Archivos esperados**

- move: proyecto AGENTS OS completo.
- modify: referencias path-based verificadas.
- create: reporte/plantilla de migración por área.

**No tocar**

- Otros proyectos o áreas.

**Spikes permitidos**

- Compatibilidad de Obsidian Bases/Tasks con el nuevo path.

**Tests y asserts**

- `[[AGENTS OS]]` resuelve una sola nota.
- Bootstrap marker y root continúan funcionando.
- ChatGPT pack se genera; Graphify ignora outputs.
- Cero links/path refs rotos del piloto.
- Rollback probado o verificable.

**Entregables/Gate G5**

- Piloto, reporte de migración y recomendación go/no-go en `review`.

**Handoff a Fase 6**

- Fase 6 recibe layout final o rollback aceptado con evidencia.

### Paquete autónomo Fase 6 — Validación y adopción

**Misión exacta**

Probar que Fase 2 aporta continuidad y utilidad real, cerrar gates y dejar el
siguiente ciclo definido sin depender de esta conversación.

**Precondiciones verificables**

- G5 `accepted`.

**Lectura obligatoria**

- Calidad/métricas, DoD y dispatches de esta nota.
- `VAULT_ROOT/80-agents/skills/agents-os-bootstrap/SKILL.md`
- `VAULT_ROOT/80-agents/skills/agents-os-context-retrieval/SKILL.md`
- `VAULT_ROOT/80-agents/skills/agents-os-doctor/BENCHMARK.md`

**Decisiones cerradas**

- Se mide valor y reexplicación, no sólo tokens.
- Compatibilidad de superficie exige proceso/agente fresco.
- Watcher se adopta sólo ante fricción medida del reindex manual.

**Implementación paso a paso**

1. Ejecutar cold fact/relation/synthesis/code.
2. Ejecutar warm turn y cambio de entidad.
3. Probar Graphify available/stale/unavailable.
4. Ejecutar ciclo E2E de conocimiento: ingest, query, trabajo, delta durable,
   reindex y recuperación por agente fresco.
5. Repetir discovery core/app en dos superficies como mínimo.
6. (R14/D13) Medir uso y utilidad de `graphify-obsidian` sobre
   `~/.config/graphify-obsidian/query-log.jsonl`: frecuencia por `kind`,
   entidades/temas consultados, distribución de `token_budget` y latencia; y un
   **proxy de utilidad hit/miss** (`nodes_returned==0` o `result_chars` bajo =
   miss). Contrastar costo de mantener el índice vs. su utilidad real.
7. Comparar baseline, registrar regresiones y decidir watcher.
8. Entregar go/no-go, deuda residual y propuesta Fase 3 si corresponde.

**Archivos esperados**

- modify: esta nota, parent y benchmark.
- create: reporte final/feedbacks sólo ante evidencia material.
- conditional modify: watcher/automation sólo con decisión respaldada.

**No tocar**

- Retrofit masivo de otras áreas.

**Spikes permitidos**

- Ninguno fuera de la matriz; una capacidad no disponible queda como gap.

**Tests y asserts**

- Agente fresco retoma sin pedir reexplicación material.
- Fuentes cargadas son suficientes y canónicas.
- Cero procedimientos duplicados detectados.
- Cold/warm/swap cumplen benchmark blando sin perder calidad.
- Skills app/core resuelven a una sola fuente.

**Entregables/Gate G6**

- Reporte go/no-go, debt register y entrega para aceptación humana.

**Handoff a Fase 7**

- El owner aceptó G6 y autorizó abrir F7. El foco se deriva exclusivamente de
  la deuda residual verificada: metadata live, caches path-based y transición
  segura del gate `warn-first`.

### Paquete autónomo Fase 7 — Retrofit y endurecimiento gradual

**Misión exacta**

Reducir la deuda live que impide volver estricto el lint all-vault, validar el
rescan de caches path-based antes de escalar el layout por área y dejar una
decisión G7 basada en evidencia, sin normalizar metadata semántica a ciegas.

**Precondiciones verificables**

- G6 `accepted`.
- Doctor estricto `0/0/0` y Graphify funcional.

**Lectura obligatoria**

- Estado, matriz, tareas y gates de esta nota.
- `VAULT_ROOT/80-agents/skills/_shared/metadata-schema.md`.
- `VAULT_ROOT/90-system/convenciones.md`.
- `VAULT_ROOT/80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py`.
- `VAULT_ROOT/80-agents/memory/public/learning/agents-os/external-vault-moves-require-plugin-cache-rescan.md`.

**Decisiones cerradas**

- El baseline canónico excluye trash, derivados, outputs y fixtures según el
  contrato del lint; pasar paths explícitos sólo sirve para diagnósticos
  dirigidos porque omite esas exclusiones.
- Se corrigen primero fuentes P1 cuya metadata puede verificarse. Tipos,
  ownership o fechas ambiguas se inventarían: quedan en backlog scoped.
- El gate permanece `warn-first` hasta que el corpus activo esté limpio o cada
  residuo tenga una exclusión contractual justificada.
- El layout no escala a otros proyectos hasta probar rescan nativo y una vista
  real del consumidor path-based.

**Implementación paso a paso**

1. Aceptar G6 y reconciliar Estado, matriz, tareas, gates y dispatches.
2. Capturar baseline residual por regla y top-level path.
3. Ejecutar retrofit P1 de fuentes canónicas con valores verificables; validar
   cada lote con lint dirigido y doctor.
4. Probar rescan de Task Board/consumidor path-based en Obsidian y decidir si
   se habilita otro piloto de layout.
5. Repetir lint all-vault, doctor y Graphify; decidir mantener `warn-first` o
   proponer el flip estricto.
6. Entregar go/no-go y dejar G7 en `review`.

**Archivos esperados**

- modify: esta nota y el parent.
- conditional modify: fuentes live incluidas en un lote P1 cuya metadata sea
  verificable.
- create: un change log consolidado por lote material.

**No tocar**

- Trash, archive, outputs, derivados Graphify y fixtures.
- Metadata con semántica no verificable desde su propia fuente.
- Movimientos masivos de proyectos antes del rescan real.

**Spikes permitidos**

- Sólo inspección read-only de consumidores/caches path-based y lint dirigido;
  ninguna edición manual de caches derivados.

**Tests y asserts**

- Cada lote reduce findings sin aumentar doctor ni romper Graphify.
- Ninguna fecha, owner, scope o type se infiere sin evidencia.
- El rescan path-based se valida en una vista real o queda gap explícito.
- El gate sólo cambia a estricto con `ERROR=0` en el corpus acordado.

**Entregables/Gate G7**

- Reporte de reducción por lote, evidencia del rescan, decisión del gate y
  deuda residual scoped.

**Handoff**

- G7 queda en `review`. No se crea F8 automáticamente; el owner decide cierre,
  siguiente lote o una nueva iteración según la deuda residual.

## ✅ Tareas

> [!example]- Fuente canónica de tareas
> **Fase 0**
> - [x] T0.1 Crear [[AGENTS OS - Fase 2]] como planificador único #owner/agent #type/dev #area/personal
> - [x] T0.2 Compactar parent y archivar planificadores anteriores #owner/agent #type/dev #area/personal
 > - [x] T0.3 Limpiar historia runtime de 22 skills #owner/agent #type/dev #area/personal
> - ~~[ ] T0.4 Establecer y probar punto de recuperación del vault~~ (cancelada — vault respaldado por infra)
> - [x] T0.5 Capturar baseline reproducible de doctor, Graphify, schemas y skills #owner/agent #type/research #area/personal
> - [x] T0.6 Dejar G0 en Review con evidencia #owner/agent #type/admin #area/personal
>
> **Fase 1**
> - [x] T1.1 Adelgazar AGENTS.md y reconciliar autoridades #owner/agent #type/dev #area/personal
> - [x] T1.2 Compactar context-router humano sin duplicar retrieval #owner/agent #type/dev #area/personal
> - [x] T1.3 Reparar doctor, ref SQX, graphifyignore y nota rogue #owner/agent #type/dev #area/personal
> - [x] T1.4 Validar doctor estricto y dejar G1 en Review #owner/agent #type/research #area/personal
>
> **Fase 2**
> - [x] T2.1 Clasificar ownership de todas las skills #owner/agent #type/research #area/personal
> - [x] T2.2 Diseñar registry federado y discovery portable #owner/agent #type/dev #area/personal
> - [x] T2.3 Migrar transversales a 30-resources/agents-skills (D14); repo owner Echo Forge/SQX hallado (`xKoRx/symphony`) y piloto `sqx-plugin-lifecycle` migrada (2 restantes pendientes, ya no bloqueadas) #owner/agent #type/dev #area/personal
> - [x] T2.4 Forward-test de resolución (core + federadas) ejecutado en superficie Claude Code con métricas y limitación de superficie; G2 en Review con los 2 gaps cerrados #owner/agent #type/research #area/personal
>
> **Fase 3**
> - [x] T3.1 Separar contratos metadata S1/S2 #owner/agent #type/dev #area/personal
> - [x] T3.2 Alinear templates prioritarios #owner/agent #type/dev #area/personal
> - [x] T3.3 Crear lint all-vault y fixtures read-only #owner/agent #type/dev #area/personal
> - [x] T3.5 Cablear lint como gate pre-execute warn-first de graphify-obsidian update #owner/agent #type/dev #area/personal
> - [x] T3.4 Auditar retrofit y dejar G3 en Review #owner/agent #type/research #area/personal
> - [x] T3.6 Completar handoff F4 con tipos methodology/source en schema y lint #owner/agent #type/dev #area/personal
> - [x] T3.7 Fortalecer lint de campos base/core, reglas duras y fixtures unitarias #owner/agent #type/dev #area/personal
> - [x] T3.8 Reconciliar templates S1/S2 y routing lifecycle/update/capture #owner/agent #type/dev #area/personal
> - [x] T3.9 Reproducir evidencia completa y devolver G3 a Review #owner/agent #type/research #area/personal
>
> **Fase 4**
> - [x] T4.1 Normalizar contrato resource wiki #owner/agent #type/dev #area/personal
> - [x] T4.2 Crear dominio methodologies/sdd con provenance #owner/agent #type/dev #area/personal
> - [x] T4.3 Crear/ajustar skill ejecutable SDD sin duplicar docs #owner/agent #type/dev #area/personal
> - [x] T4.4 Ejecutar ingest/query/lint y dejar G4 en Review #owner/agent #type/research #area/personal
> - [x] T4.5 Corregir bloqueantes del review G4 y regenerar evidencia #owner/agent #type/dev #area/personal
>
> **Fase 5**
> - [x] T5.1 Inventariar refs y preparar move/rollback del piloto #owner/agent #type/research #area/personal
> - [x] T5.2 Mover AGENTS OS bajo Personal y reparar refs #owner/agent #type/dev #area/personal
> - [x] T5.3 Validar Obsidian, packs, Graphify y links #owner/agent #type/research #area/personal
> - [x] T5.4 Emitir recomendación de retrofit y dejar G5 en Review #owner/agent #type/research #area/personal
>
> **Fase 6**
> - [x] T6.1 Ejecutar matriz cold/warm/swap/Graphify #owner/agent #type/research #area/personal
> - [x] T6.2 Ejecutar E2E con agente fresco (Codex CLI aislado recuperó bootstrap, planner y registry) #owner/agent #type/research #area/personal
> - [x] T6.3 Validar discovery en al menos dos superficies (Codex Desktop + Codex CLI) #owner/agent #type/research #area/personal
> - [x] T6.6 Medir uso y utilidad de graphify-obsidian (query-log + proxy hit/miss) #owner/agent #type/research #area/personal
> - [x] T6.4 Comparar métricas y decidir watcher (no adoptar: no hubo fricción medida) #owner/agent #type/research #area/personal
> - [x] T6.5 Entregar GO y dejar G6 en Review #owner/agent #type/admin #area/personal
>
> **Fase 7**
> - [x] T7.1 Aceptar G6 y reconciliar el planificador con la evidencia F6 #owner/agent #type/admin #area/personal
> - [x] T7.2 Capturar baseline residual por regla y top-level path #owner/agent #type/research #area/personal
> - [x] T7.3 Ejecutar retrofit P1 de fuentes canónicas con metadata verificable (237→41 ERROR; residuo ambiguo scoped) #owner/agent #type/dev #area/personal
> - [x] T7.4 Validar rescan de cache path-based: Obsidian `Cmd+P` → `Task Board: Open vault scanner` → scan completo; owner confirmó nuevo path y ausencia del antiguo #owner/me #type/research #area/personal
> - [x] T7.5 Revalidar lint, doctor y Graphify; decisión NO-GO gate estricto, mantener warn-first #owner/agent #type/research #area/personal
> - [x] T7.6 Entregar go/no-go y dejar G7 en Review #owner/agent #type/admin #area/personal

## Control de gates

| Gate | current state | responsabilidad agente | evidencia de aceptación owner | enables |
|---|---|---|---|---|
| G0 | accepted | baseline aceptado por owner 2026-08-06 | doctor output y startup measurement aceptados | F1 |
| G1 | accepted | autoridades/doctor aceptados por owner 2026-08-06 | doctor y matriz sin contradicción | F2 |
| G2 | accepted | aceptado por owner 2026-08-07; registry federado + ownership + forward-test; 2 gaps cerrados (forward-test superficie Claude Code + repo owner `xKoRx/symphony` con piloto `sqx-plugin-lifecycle` migrada). Doctor estricto verde | fuente única y forward-test aceptados | F3 |
| G3 | accepted | aceptado por owner 2026-08-08 tras correcciones: `methodology/source` definidos; lint aplica campos base/core, frontera templates y hard rules; templates 31 en verde; fixtures válidas 6 verdes e inválidas 8/8 rojas; read-only PASS; gate warn-first reporta ERROR=237/WARN=87 y `update` completa exit 0; doctor estricto verde | owner aceptó contratos, templates, fixtures y gate el 2026-08-08 | F4 |
| G4 | accepted | T4.5 cerró los dos bloqueantes: contrato Resource Wiki consistente/inventario vigente y perfil de validación federada formalizado con evidencia real de `quick_validate.py`; lint/YAML/doctor verdes | owner aceptó el re-review sin observaciones pendientes el 2026-08-08 | F5 |
| G5 | accepted | owner aceptó el piloto tras revalidar doctor, fuentes canónicas, rollback y recomendación; se conserva NO-GO temporal para retrofit masivo hasta validar rescan de plugins path-based | aceptación owner 2026-08-08 | F6 |
| G6 | accepted | doctor estricto `0/0/0`; Graphify y el smoke fresco CLI resolvieron fuentes canónicas y registry; debt de hooks/plugins aislada y no bloqueante | owner autorizó aceptar si la revalidación estaba verde; confirmada el 2026-08-08 | F7 |
| G7 | accepted | T7.1–T7.6 cerradas; `237→41 ERROR`, `84 WARN`; doctor `0/0/0`; Graphify `5474/6296`; gate estricto NO-GO, se mantiene warn-first | owner confirmó T7.4: rescan completo muestra el nuevo path y ausencia del antiguo (2026-08-08) | cierre/iteración siguiente |

## Definición de Done

- Un agente que sólo recibe el workspace entra por `AGENTS.md` y ejecuta
  bootstrap sin que el usuario enumere documentos.
- No existe más de una receta runtime para startup, retrieval, cierre o ingest.
- Cada skill tiene owner y source canónico resoluble.
- Schemas S1/S2 y templates pasan lint.
- SDD demuestra LLM Wiki sin duplicar specs concretas.
- El piloto por área mantiene identidad, links y rollback.
- Doctor estricto y Graphify están verdes o tienen gaps aceptados.
- Un agente fresco recupera suficiente contexto con menor reexplicación.
- G7 fue aceptado por el owner tras validar T7.4. La tarea puente permanece en
  Review hasta que el owner la marque Done; el agente no la cierra.

## Prompt común de ejecución

Trabaja exclusivamente la fase asignada de [[AGENTS OS - Fase 2]]. Lee su
paquete autónomo, verifica el gate previo y trata esta nota como planificador
único. Preserva cambios ajenos. No inventes decisiones ni amplíes scope. Usa
Markdown como verdad y Graphify como derivado. Actualiza tareas, progreso,
estado y Bitácora a medida que avances. Si la evidencia contradice el plan,
detente con `PLAN_CONFLICT`. Deja el gate actual en `review`; nunca aceptes tu
propio gate ni comiences la fase siguiente.

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Baseline
GATE_REQUERIDO=none
TAREAS=T0.5, T0.6
SALIDA=log de baseline con doctor output + startup measurement + G0 review
STOP=G0 review; prohibido iniciar F1
```

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Autoridades y doctor
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1-T1.4
SALIDA=autoridades reconciliadas + doctor estricto + G1 review
STOP=G1 review; prohibido iniciar F2
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — Skills por ownership
GATE_REQUERIDO=G1 accepted
TAREAS=T2.1-T2.4
SALIDA=registry federado + piloto app + G2 review
STOP=G2 review; prohibido iniciar F3
```

**Despacho Fase 3**

```text
FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3 — Schema S1/S2
GATE_REQUERIDO=G2 accepted
TAREAS=T3.1, T3.2, T3.3, T3.5, T3.4
SALIDA=schemas + templates + lint all-vault + gate warn-first graphify + G3 review
STOP=G3 review; prohibido iniciar F4
```

**Despacho Fase 4**

```text
FASE_ASIGNADA=4
PAQUETE_CANONICO=Paquete autónomo Fase 4 — LLM Wiki y SDD
GATE_REQUERIDO=G3 accepted
TAREAS=T4.1-T4.4
SALIDA=dominio SDD + skill + query/lint + G4 review
STOP=G4 review; prohibido iniciar F5
```

**Despacho Fase 5**

```text
FASE_ASIGNADA=5
PAQUETE_CANONICO=Paquete autónomo Fase 5 — Piloto de proyectos por área
GATE_REQUERIDO=G4 accepted
TAREAS=T5.1-T5.4
SALIDA=piloto AGENTS OS + rollback + recomendación + G5 review
STOP=G5 review; prohibido iniciar F6
```

**Despacho Fase 6**

```text
FASE_ASIGNADA=6
PAQUETE_CANONICO=Paquete autónomo Fase 6 — Validación y adopción
GATE_REQUERIDO=G5 accepted
TAREAS=T6.1, T6.2, T6.3, T6.6, T6.4, T6.5
SALIDA=reporte go/no-go + medición de uso/utilidad graphify + deuda residual + G6 review
STOP=G6 review; prohibido crear una fase siguiente
```

**Despacho Fase 7**

```text
FASE_ASIGNADA=7
PAQUETE_CANONICO=Paquete autónomo Fase 7 — Retrofit y endurecimiento gradual
GATE_REQUERIDO=G6 accepted
TAREAS=T7.1-T7.6
SALIDA=reducción por lote + rescan path-based + decisión gate + G7 review
STOP=G7 review; prohibido iniciar una fase posterior
```

## Contrato de handoff

Al finalizar una sesión normal:

1. Actualizar tareas, `progress`, Estado actual y Bitácora.
2. Dejar evidencia exacta de comandos/tests y archivos tocados.
3. Registrar nuevos hechos reusables sólo si superan la prueba de memoria.
4. No crear otro planner ni guardar progreso dentro de una skill.
5. Indicar la próxima tarea exacta y el gate vigente.

## 📆 Bitácora

- **2026-08-08 (cierre y handoff)** — Por decisión explícita del owner, Fase 2
  pasa a `completed`. La deuda residual se transfiere a
  [[AGENTS OS - Fase 3]] sin copiar historia ni repetir validaciones aceptadas.
  El proyecto queda como evidencia canónica de F0–F7 y G0–G7.
- **2026-08-08 (T7.4 confirmada · G7 accepted)** — El owner confirmó el
  rescan completo de Task Board en una vista real: el consumidor path-based
  muestra `10-projects/Personal/AGENTS OS/` y no el path antiguo
  `10-projects/AGENTS OS/`. T7.4 `[x]`, G7 `review→accepted`, progreso 100%.
  Fase 2 queda lista para cierre owner; no se crea F8 automáticamente. La
  deuda residual (`41 ERROR / 84 WARN`) permanece scoped y el gate sigue
  `warn-first`.
- **2026-08-08 (F7 entregada · G7 review)** — T7.3 cerrada por alcance seguro:
  26 skills core, skills federadas/app, 64 memorias internas, tres runbooks y
  fuentes S1 verificables regularizadas. Lint `237→41 ERROR` y `84 WARN`; deuda
  residual: unknown-type 35, bad-status 3, missing-field 2, bad-owner 1; por
  dominio: Aranea 37, Echo Forge 1, Destaques 1, dashboards Echo 2. No se
  normalizaron tipos, estados, progress ni ownership ambiguos. T7.5 cerrada:
  doctor `HIGH=0 MEDIUM=0 LOW=0`, startup≈5006; Graphify update exit 0,
  `5474` nodos / `6296` aristas. Decisión NO-GO al gate estricto; continúa
  `warn-first`. T7.6 cerrada y G7 `pending→review`. Único paso owner: T7.4,
  validar rescan path-based en una vista real de Obsidian.
- **2026-08-08 (F7 · T7.3 lote P1 core skills)** — Se regularizaron las 26
  fuentes canónicas `80-agents/skills/agents-os-*/SKILL.md`: `scope: global`,
  `created` desde la fecha de creación verificable del filesystem y `updated`
  al cambio. Lint de las skills core (sin fixtures intencionalmente inválidas)
  verde; baseline all-vault baja de `237 ERROR / 84 WARN` a `159 ERROR / 84
  WARN` (−78 errores). Se mantienen fuera tipos legacy, ownership/estados de
  entidades y fechas sin evidencia. Lint dirigido `0/0`; Graphify reindexó
  `5474` nodos / `6296` aristas. El owner elevó el target blando a 6k y el
  doctor vuelve a verde con startup≈5006; T7.3 queda WIP para el siguiente
  lote verificable; gate `warn-first`.
- **2026-08-08 (G6 accepted → F7)** — Revisión owner condicionada a evidencia
  verde: doctor estricto reproducido `HIGH=0 MEDIUM=0 LOW=0`; Graphify reindexó
  y `explain` resolvió `[[AGENTS OS - Fase 2]]`; el smoke CLI y la segunda
  superficie mantienen evidencia auditable. Se corrigió drift del planner:
  R1/R2/R4/R5/R8/R9/R11/R12/R14 reflejan sus entregables reales y el despacho
  de F6 conserva su identidad. G6 `review → accepted`. F7 creada por decisión
  del owner. T7.1/T7.2 `[x]`: baseline lint canónico `237 ERROR / 84 WARN`
  sobre 485 notas; reglas: missing-field 149, unknown-type 60, s1-status 24,
  bad-status 3, bad-owner 1; warnings: no-frontmatter 81 y no-type 3. Por raíz:
  80-agents 182, 30-resources 32, 10-projects 21 y 90-system 2. El gate sigue
  `warn-first`; próximo paso T7.3. La validación de rescan real T7.4 queda
  explícitamente humana/de superficie, no se falsifica desde shell.
- **2026-08-09 (G6 → review)** — T6.2/T6.3/T6.5 `[x]`. En Codex Desktop y
  un proceso fresco de Codex CLI read-only, AGENTS.md encaminó a bootstrap;
  el proceso fresco resolvió el planificador activo y las rutas federadas
  `agents-os-doctor` y `sync-local-branch`. Doctor estricto actual:
  `HIGH=0 MEDIUM=0 LOW=0`; Graphify `explain` resolvió la entidad. El CLI con
  configuración completa aún produjo fallas ruidosas de hooks/plugins, pero la
  corrida aislada finalizó las lecturas y demostró que no es un defecto del
  vault. Recomendación GO; sin Fase 7 automática. La tarea puente pasa a
  Review para decisión del owner.
- **2026-08-08 (Fase 6 · validación parcial)** — T6.1 `[x]`: cold/warm/swap
  y Graphify disponible/degradado conservaron bootstrap, entidad y fallback;
  reindex 5471/6291 y doctor `0/0/0`. T6.6 `[x]`: 279 consultas, 2.9% miss
  proxy, p95 598 ms. T6.4 `[x]`: no watcher. T6.2/T6.3 `[/]` por fallas de
  superficie: Codex fresco llegó a bootstrap pero hooks/plugins no cerraron;
  Claude CLI reportó reglas de permisos inválidas. G6 permanece `pending`.
- **2026-08-08 (G5 accepted → Fase 6)** — El owner aceptó G5 tras la
  revalidación actual: doctor estricto `0/0/0`; no se detectó drift en las
  fuentes canónicas ni en el rollback. La condición de rescan Task Board se
  mantiene como límite de escala, no como bloqueo del piloto. T6.1 `[/]`.
- **2026-08-08 (Fase 5 · G5 review)** — T5.4 cerrada. Recomendación emitida:
  GO para conservar `10-projects/Personal/AGENTS OS/`; NO-GO temporal para un
  retrofit masivo hasta probar rescan de plugins path-based con una vista real.
  Change log/checklist/rollback:
  `80-agents/journal/logs/2026-08-08-agents-os-fase5-project-layout-pilot.md`.
  G5 `pending → review`; F6 no iniciada y la tarea puente del parent permanece
  WIP porque el proyecto completo aún tiene F6 pendiente.
- **2026-08-08 (Fase 5 · T5.3 → T5.4)** — Validación del piloto: lint 2 notas
  `0/0`; doctor estricto `0/0/0`; pack 145 archivos + hashes + ZIP PASS;
  reindex 5465/6284 exit 0; `[[AGENTS OS]]` único y Graphify apunta al nuevo
  path con backlinks. No hay Bases activas ni selectores Dataview/Tasks vivos
  hardcodeados al path anterior. La caché derivada de Task Board sí quedó
  stale tras el move externo y requiere rescan desde la UI; se registra como
  condición para escalar, no se convierte en autoridad. T5.3 `[x]`; T5.4 `[/]`.
- **2026-08-08 (Fase 5 · T5.2 → T5.3)** — Movido el lote exacto de 8 archivos
  a `10-projects/Personal/AGENTS OS/`, sin rename canónico ni eliminación.
  Reparadas las referencias operativas y el pack pasó de seleccionar el
  proyecto archivado a seleccionar el planificador activo. Origen ausente,
  destino presente y rollback inverso disponible. T5.2 `[x]`; T5.3 `[/]`.
- **2026-08-08 (Fase 5 · T5.1 → T5.2)** — Inventario cerrado: 8 archivos,
  destino libre y referencias operativas acotadas. Excluidos historia,
  journal, archive, outputs y caches derivados. El pack tenía un fallo
  preexistente por exigir el proyecto archivado Beta/Hardening; su selección
  se corrige al parent + planificador activo. Rollback verificable definido
  como move inverso + reversión del set de paths, con checksums pre-move.
  T5.1 `[x]`; T5.2 `[/]`.
- **2026-08-08 (Fase 5 · inicio T5.1)** — G4 aceptado y precondición de gate
  satisfecha. Iniciado el inventario de referencias físicas y el diseño de
  move/rollback para el único piloto `10-projects/AGENTS OS/` →
  `10-projects/Personal/AGENTS OS/`; todavía no se movieron archivos.
- **2026-08-08 (Fase 4 · G4 accepted)** — El owner declaró que no quedan
  observaciones sobre G4 y aceptó el re-review. G4 `review → accepted`; F5 queda
  habilitada, pero F5/T5.1 no se inició. Próximo paso exacto: T5.1, inventariar
  referencias y preparar move/rollback del piloto; probar backup antes de todo
  movimiento físico.
- **2026-08-08 (Fase 4 · T4.5 · G4 re-review)** — El owner rechazó G4 y se
  registró `review → wip`. Corregido `00-RESOURCE-WIKI.md`: el entrypoint
  canónico sigue siendo `00-index.md`, las variantes legacy rechazadas son
  `index.md`, `00-INDEX.md` e `INDEX.md`, y el inventario incorpora
  `methodologies/` con `methodologies/sdd/`. La fuente Kiro usa la URL canónica
  `https://kiro.dev/docs/specs/`. `quick_validate.py` se ejecutó realmente en
  Python 3.10.16 y 3.12.9: exit 1 esperado en ambos por las claves S1
  `created, scope, tags, type, updated`; `_shared/skill-contract.md` formaliza
  que ese perfil portable no aplica como gate a skills federadas. Gate
  equivalente: lint exacto skill `ERROR=0 WARN=0 notes_scanned=1`, YAML
  skill/UI PASS y `$sdd-workflow` consistente. Dominio methodologies 13 `0/0`;
  seis dominios/subdominios activos con `index+log` PASS; doctor estricto
  `0/0/0`; reindex exit 0 (5465 nodos/6284 edges). T4.5 cerrada; G4
  `wip → review`; F5/T5.1 no iniciada.
- **2026-08-08 (Fase 4 · G4 review)** — T4.4 cerrada. Lint: templates 19
  `ERROR=0 WARN=0`; dominio SDD (sin logs operacionales) 13 `0/0`; skill
  `sdd-workflow` `0/0`; YAML de skill/UI parsea y referencia `$sdd-workflow`.
  La evidencia inicial declaró erróneamente `quick_validate.py` no disponible;
  T4.5 la reemplaza con ejecución real y el perfil federado formalizado. Query
  Graphify `SDD — Lifecycle brownfield backfill phase
  gap verification provenance` recuperó lifecycle + índice + fuentes GitHub y
  Kiro como top nodes. Gate all-vault warn-first `237/84`; doctor estricto
  `0/0/0`; reindex exit 0 (5464 nodos/6283 edges). Cero specs concretas en el
  dominio. G4 `pending → review`; F5 no iniciada. Próximo paso: revisión/aceptación
  humana de G4; sólo después T5.1.
- **2026-08-08 (Fase 4 · T4.2–T4.3)** — Creado el dominio activo
  `30-resources/methodologies/sdd/`: índice, log, seis páginas metodológicas y
  cinco notas `source`. Fuentes primarias: GitHub Spec Kit, Kiro Specs y el
  runtime/manual SDD de `xKoRx/symphony`. El antiguo `docs/sdd/` quedó
  `superseded` porque su README declara bootstrap pendiente mientras el runtime
  ya contiene constitution, rules, skills y specs. No se copiaron specs
  concretas. Creada la transversal federada `sdd-workflow` bajo
  `30-resources/agents-skills/` (D14), con core procedural lean y referencias al
  dominio; INDEX actualizado. T4.4 pasa a WIP para lint/query/reindex y G4.
- **2026-08-08 (Fase 4 · T4.1)** — Contrato Resource Wiki normalizado:
  autoridad por capas, dominio activo, casing `00-index.md`, provenance,
  freshness/confidence y reemplazo/deprecación. Nuevo template `resource`,
  template `source` extendido y `_sources/` excluida de Graphify. Índices
  legacy de `vibe-coding` y `aranea/backup-dr` renombrados; Aranea recibió
  `log.md` raíz y routing de Vibe Coding pasó a [[Personal]] sin inventar
  provenance retroactiva. Evidencia: templates 19 `0/0`; doctor estricto
  `0/0/0`; cuatro dominios activos con index+log; reindex exit 0 (5382/6166),
  gate warn-first `237/88`. T4.1 cerrada; T4.2 inicia.
- **2026-08-08 (Fase 4 · inicio)** — G3 aceptado y F4 habilitada. Se inicia
  T4.1 para normalizar el contrato Resource Wiki antes de crear el dominio
  `methodologies/sdd`; la tarea puente del parent permanece WIP.
- **2026-08-08 (G3 accepted · cierre de sesión)** — El owner aprobó G3
  explícitamente. Gate `review → accepted`; F4 queda habilitada pero no se
  inició. La tarea puente de [[AGENTS OS]] permanece WIP porque el proyecto
  completo sigue activo. Próxima tarea exacta: T4.1 normalizar contrato
  resource wiki.
- **2026-08-08 (G3 · correcciones de review)** — El owner solicitó corregir y
  dejar G3 listo para aceptar. G3 pasó `review → wip → review`; T3.6–T3.9
  cerradas. Se definieron `methodology/source` en schema, lint y templates; el
  lint ahora valida campos base/core, frontera 70/80, owner/parent de proyecto,
  locator de source y `status` S1 como ERROR; se agregaron fixtures unitarias.
  Se eliminó el decision template S1 duplicado de `70-templates`, el agent
  template S2 pasó a 70, se repararon action/monitor/skill y lifecycle/update/
  capture enrutan a la autoridad correcta. Evidencia: templates 31 `0/0`;
  válidas 6 `0/0`; inválidas 8 `ERROR=8 WARN=0`; S1-status aislada exit 1;
  read-only hash PASS; all-vault `ERROR=237 WARN=87`/471; doctor estricto verde;
  `graphify-obsidian update` mostró el gate y completó exit 0 (5320 nodos,
  6095 edges). F4 no se inició; G3 espera aceptación humana.
- **2026-08-07 (Fase 3 · Schema S1/S2 + lint + gate)** — Owner **aceptó G2**;
  arrancó F3. **T3.1:** `metadata-schema.md` restringido a Sistema 1 (enum `type`
  solo S1; puntero a convenciones; regla S1 sin status); `convenciones.md` con
  sección "Schema de Sistema 2" (tabla tipo→status por lifecycle + status
  requerido piloto area/project/application + campos base). **T3.2:**
  `decision.md` sin `status` ceremonial; `service-doc`/`agent`/`monitor`/`action`/
  `context_pack` bendecidos como tipos reales (tienen template+notas vivas) →
  **todos los templates pasan lint** (0 findings en 70-templates y
  80-agents/templates). **T3.3:** creado `agents-os-entity-lifecycle/scripts/
  lint.py` (read-only, all-vault, honra `.graphifyignore`+dot-dirs+`fixtures/`;
  modos `--check`/`--gate`) + fixtures (válidas ERROR=0; inválidas ERROR=3 WARN=1
  con mensajes accionables). **T3.5:** gate warn-first (D12) en el branch `update`
  del wrapper `95-graphify/dist/graphify-obsidian`, justo antes del extractor;
  query/path/explain/affected intactos; `~/bin` re-sincronizado desde la fuente
  canónica. Probado con `graphify-obsidian update` real: banner + conteo
  (ERROR=63 WARN=111 sobre 470 notas del corpus) y **update completó exit 0**
  (5300 nodos). **T3.4:** auditados los tipos reales y producido plan de retrofit
  por área (P1 core S1: internal_memory/agent-memory/memory→agent_memory,
  known-error→known_error; P2 proyectos: agent-project→project+owner:agent; P3
  Aranea/Echo: ticket/design-*/service-doc; ~60 páginas 30-resources se tipifican
  en F4). **No** se hizo retrofit masivo (fuera de scope). Doctor estricto verde
  `HIGH=0 MEDIUM=0 LOW=0` startup≈4979 exit 0. Sin cambios colaterales (solo
  derivados en `95-graphify/obsidian/`). **G3 → review; no se inició F4 ni se
  auto-aceptó el gate.** Evidencia:
  `80-agents/journal/logs/2026-08-07-agents-os-fase3-schema-lint-gate.md`.
  Próxima tarea: T4.1 (solo tras `G3 accepted`).
- **2026-08-07 (Fase 2 · cierre de gaps G2)** — Proceso fresco (superficie Claude
  Code). **Gap 2:** repo owner Echo Forge/SQX **hallado** en `xKoRx/symphony`
  (`~/go/src/github.com/xKoRx/symphony`, no en `~/fuentes/`), confirmado por
  `AGENTS.md`/`CONSTITUTION.md`/`deploy/manifest.json`/`sqx/`/`worker-ssh`.
  **Piloto `sqx-plugin-lifecycle` migrada** (sin copia; `cp -R` + checksums + `rm`)
  a `.agents/skills/` del repo; INDEX reescrito (`repo + path relativo`, inv. 11);
  las otras 2 pasan a "pendiente (repo hallado)". No se commiteó/pusheó (decisión
  del owner). **Gap 1:** forward-test ejecutado en Claude Code — HIT de core
  `agents-os-doctor` (~1161 tok, 0.30 ms), federadas `sync-local-branch` (~873 tok)
  y `fury-lib-consumer-deploy` (~2148 tok) por registry federado; MISS correcto de
  la piloto desde el vault, HIT en el repo. Limitación de superficie: el registro
  nativo de skills de Claude Code solo expone bootstrap (por diseño del
  skill-contract). **Higiene:** el doctor arrancó en `MEDIUM=1` (startup ≈5012,
  drift preexistente de la nota de continuidad global, +241 chars, no de este
  trabajo); compactada a puntero → `MEDIUM=0`, startup ≈4979. `graphify-obsidian
  update` OK (5272 nodos). Doctor estricto verde `HIGH=0 MEDIUM=0 LOW=0` exit 0.
  **G2 en review, listo para aceptación del owner; no se inició F3 ni se
  auto-aceptó el gate.** Evidencia: `80-agents/journal/logs/2026-08-07-agents-os-fase2-g2-gaps-closure.md`.
- **2026-08-06 (Fase 2)** — G1 aceptado por owner. T2.1–T2.4: matriz de ownership de las 32 skills; **D14** (corregida: transversales **in-vault** en `30-resources/agents-skills/`, no repo externo). Ejecutado: `sync-local-branch` y `fury-lib-consumer-deploy` movidas a `30-resources/agents-skills/`; INDEX convertido en registry federado (core + sección federada); doctor hecho federation-aware (regex anclado a `80-agents/skills/` + validación de targets federados); refs vivas actualizadas (`Automatización despliegue FURY.md`, memoria interna de continuidad). `operational-healthcheck-policy` reclasificada a vault-ops. Nesting físico del core **descartado** (D14: innecesario; la separación se logra por extracción). Doctor estricto verde `HIGH=0 MEDIUM=0 LOW=0`; 32 targets del INDEX resuelven. **Gaps para G2:** (1) forward-test multisuperficie no ejecutable aquí; (2) migración de 3 skills Echo Forge/SQX bloqueada (repo owner no hallado). G2 → review. Evidencia: `80-agents/journal/logs/2026-08-06-agents-os-fase2-f2-registry-federado.md`.
- **2026-08-06 (scope+)** — El owner amplió el scope: R13 (lint de frontmatter all-vault + gate pre-execute warn-first de `graphify-obsidian update`) y R14 (medir uso/utilidad de graphify sobre `query-log.jsonl`, ya con 269 entradas). Decisiones D12 (warn-first→estricto tras retrofit) y D13 (medición en F6). Tareas nuevas T3.5 (F3) y T6.6 (F6); despachos F3/F6 actualizados. Punto de pre-execute confirmado en el branch `update` del wrapper `95-graphify/dist/graphify-obsidian` (query/path/explain/affected no reindexan). No ejecutado aún; queda para F3/F6 tras sus gates.
- **2026-08-06 (Fase 1)** — G0 aceptado por owner. Ejecutadas T1.1–T1.4: AGENTS.md adelgazado a resolver-root+bootstrap; `context-router.md` compactado a doc humano (algoritmo único en `agents-os-context-retrieval`); ref rota SQX `../../`→`../`; `.obsidian/` agregado a `.graphifyignore`; nota rogue `agents-os/agent-memory` reubicada a `memory/public/known-error/` con frontmatter `known_error` (dir vacío eliminado); doctor refinado (portability por línea, exención de comandos remotos ssh/scp/rsync). Doctor estricto verde `HIGH=0 MEDIUM=0 LOW=0`, startup ≈4948 (sin aumentar). Evidencia: `80-agents/journal/logs/2026-08-06-agents-os-fase2-f1-autoridades-doctor.md`. **G1 → review.** Próxima tarea: T2.1 (solo tras `G1 accepted`).
- **2026-08-06 (Fase 0)** — Baseline capturado (T0.5, T0.6). Doctor: `HIGH=3 MEDIUM=1 LOW=0 startup≈4948`; 32 SKILL.md en disco (57 notas `type: skill`); 1311 notas `.md`, 63 variantes de `type`, 141 sin type; dominios Graphify `obsidian/personal/work`; startup cold 6 archivos ≈2973 words. Evidencia en `80-agents/journal/hygiene/2026-08-06-agents-os-fase2-baseline.md`. **G0 → review.** Próxima tarea: T1.1 (solo tras `G0 accepted`).
- **2026-08-06** — T0.4 cancelada: vault respaldado por infra, sin necesidad de snapshot adicional. Fase 0 simplificada a baseline puro (T0.5-T0.6). Riesgo "Mover paths sin Git" eliminado de la matriz. Paquete Fase 0 reescrito.
- **2026-08-01 (validación)** — El validador del plan confirmó 7 fases, 7
  gates, 7 dispatches y 22 referencias `VAULT_ROOT` resolubles, sin errores ni
  warnings. Ready state: `ready_for_phase_0`; próxima tarea T0.4.
- **2026-08-01** — Proyecto creado por decisión del owner. Se consolidaron la
  auditoría de autoridades, la política de repetición, skills por ownership,
  schema S1/S2, LLM Wiki, SDD, layout por área, provenance, freshness,
  lifecycle, validación y métricas. Parent compactado; proyectos anteriores
  archivados; ready phase F0.
- **2026-08-01 (preparación)** — Se limpiaron 22 skills y se preservó el gate
  runtime de SQX. El cambio está auditado en
  `80-agents/journal/logs/2026-08-01-agents-os-runtime-skill-history-cleanup.md`.

## 🔗 Fuentes y continuidad

- [[AGENTS OS]] — cockpit y tarea puente.
- [[agents-os]] — mapa conceptual.
- [[agent-constitution]] — invariantes.
- [[AGENTS OS - Fase 1 - Historial]] — historia del proyecto original.
- [[AGENTS OS - Hot Path y Cierre Silencioso]] — evidencia de la iteración hot path.
- [[AGENTS OS - Beta y Hardening]] — deuda beta/multisuperficie migrada.
