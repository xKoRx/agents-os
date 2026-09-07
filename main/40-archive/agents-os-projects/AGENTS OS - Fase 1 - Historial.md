---
type: project
owner: me
root: false
status: completed
cssclasses:
  - wide
priority: P1
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-06-27
due:
progress: 100
repo:
jira:
prs:
tags:
  - area/personal
  - kind/project
created: 2026-06-27
updated: 2026-08-01
aliases:
  - AGENTS OS Fase 1 Historial
---

# AGENTS OS - Fase 1 - Historial

> [!warning] Documento histórico
> Este fue el proyecto controlador original. Se archivó el 2026-08-01 para
> eliminar procedimientos y decisiones obsoletas del cockpit vigente. El
> proyecto padre canónico sigue siendo [[AGENTS OS]] y el planificador activo
> es [[AGENTS OS - Fase 2]].

> [!info]+ AGENTS OS
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1
> Sistema **evolutivo de memoria persistente** para agentes (y humanos/usuarios), sobre Obsidian + Graphify.

## 🎯 Objetivo

- Construir un sistema de memoria evolutivo donde cada sesión con un agente se convierte en conocimiento reutilizable, el agente recupera contexto barato (Graphify) y, con el uso, **entiende mejor al usuario en todos sus ámbitos**.
- Entregable final: un **set de skills** (todos usan Graphify) que hagan que el agente se comporte como el usuario quiere, **configurable** vía conversación (actualizar constitución, perfil de usuario, aprendizajes — todos parte del sistema de memoria).
- Guía operativa: [[agents-os]]. Diseño histórico archivado en `40-archive/agents-os-drafts/`.

## 🧭 North Star y escala

AGENTS OS debe aumentar capacidad real con menos contexto: Sistema 1 conserva
memoria y aprendizaje reusable; Sistema 2 representa aplicaciones, proyectos,
documentación y recursos canónicos. LLM Wiki gobierna cómo se crean y relacionan
notas; Context Router carga, de barato a caro, tags, índices, Graphify y cuerpos
solo hasta alcanzar suficiencia.

Para escalar, el sistema separa cuatro planos: control (constitución, perfil,
skills, templates), conocimiento (Sistema 1/2), derivados reconstruibles
(Graphify e índices) y evaluación (feedbacks, benchmarks, promoción y rollback).
El valor se mide por tiempo hasta la primera acción útil, tokens cargados,
continuidad entre agentes, reducción de errores repetidos y éxito de skills.
Codex, Claude u otra superficie solo se consideran compatibles después de un
forward-test real.

## 📊 Estado actual

- Diseño documentado (`80-agents/agents-os/`). Sistema 2 (entidades reales/documentación canónica) ya implementado en el vault. Fase 0 cerrada: beta enfocada en proyectos Meli, memoria centralizada bajo `80-agents/`, journal separado y Graphify como mecanismo obligatorio de retrieval.
- Sistema 1 (memoria y aprendizajes) ya tiene estructura física inicial: `80-agents/memory/public/` para memoria pública indexable y `80-agents/memory/internal/` para memoria interna indexable/always-load.
- Journal ya tiene estructura física inicial: `80-agents/journal/sessions/raw/` para raw sessions y `80-agents/journal/logs/` para registro de creaciones, modificaciones y eliminaciones de memoria pública/cambios canónicos.
- Templates mínimos creados en `80-agents/templates/`: L0 raw session, L1 summary, L3 learning/decision/known-error/runbook, change log, constitution y user preference.
- Memoria always-load inicial creada: constitución en
  `80-agents/agents-os/agent-constitution.md` y perfil personal preservado en
  `80-agents/memory/public/user-preference/rjara-agent-profile.md`.
- Contratos mínimos de Fase 1 cerrados en `80-agents/skills/_shared/`: metadata, tipos de nota y contrato Graphify quedaron reconciliados con `80-agents/agents-os/_drafts/Agent Memory Properties.md`.
- Fase 3 inició uso real: `agents-os-bootstrap`, `agents-os-context-retrieval` y `agents-os-graphify-maintenance` quedaron forward-tested en Codex; Graphify fue reindexado y se creó la primera memoria pública `known_error` con log auditable.
- Fase 3 avanzó con cierre de reglas en `agents-os-memory-distillation` y `agents-os-conflict-resolution`; además se probó un cierre artificial pequeño con L0/L1 y sin L3 pública para validar el camino no contaminante.
- Fase 4 avanzó con `agents-os-hygiene-review`: quedó definido el formato de reporte, política de fixes, marcador de última revisión y checks de links/aliases; se agregó template `80-agents/templates/hygiene-report.md`.
- Fase 4 también detectó y registró el known error `graphify-output-path-confusion`: la salida viva beta de Graphify está en `95-graphify/obsidian/`, mientras `95-graphify/graphify-out/` puede quedar como output legado.
- Fase 4 detectó otro known error de Graphify: el patrón amplio `**/*raw-session*.md` en `.graphifyignore` podía excluir skills con `raw-session` en el path, como `agents-os-retrofit-raw-session`; se reemplazó por exclusión por directorio raw del journal.
- Fase 4/hardening detectó y registró `graphify-template-node-noise`: queries genéricas pueden anclar en templates (`Transcript`, `Pendiente`, `Retrieval`, `Graphify`), por lo que `context-retrieval` ahora exige retry estricto y validación por fuente cuando aparezca ese ruido.
- Fase 6/hardening adelantó `agents-os-entity-update`: quedaron definidas secciones canónicas mínimas, edición directa con log, ejemplos de app/proyecto/concepto y reglas de alias/repo mismatch.
- Fase 6/hardening adelantó `agents-os-retrofit-raw-session`: quedaron definidos metadata de backfill, límites de batch/contexto, detección de duplicados contra L3 y ejemplo con sesión artificial archivada.
- Se creó `agents-os-behavior-config`: clasifica instrucciones conversacionales entre temporal/preferencia/constitución/memoria pública/memoria interna/Sistema 2, define logs para cambios persistentes y formaliza la promoción de memoria interna a pública.
- Se creó la primera ADR formal de AGENTS OS: `80-agents/memory/public/decision/agents-os/public-vs-internal-memory.md`, que fija la frontera entre memoria pública e interna y su regla de promoción con log.
- Se eliminó la capa de adaptadores por superficie porque no aportaba diferencias estructurales reales. El contrato operativo vive en skills, con `agents-os-bootstrap` como entrypoint obligatorio.
- `80-agents/skills/` es la única ubicación física de skills. La carga directa
  desde Codex/Claude sin copias quedó como validación y optimización pendiente
  en [[AGENTS OS - Beta y Hardening]].
- La documentación draft de diseño se archivó en `40-archive/agents-os-drafts/`; `80-agents/agents-os/agents-os.md` quedó como guía operativa única para iniciar y usar el flujo.
- Se definió la política canónica de links/aliases/slugs para los dos sistemas: Second Brain/Obsidian y AGENTS OS/Graphify. Los links usan el nombre canónico exacto, las variantes viven en `aliases` y los identificadores técnicos viven en `slug`, tags y paths semánticos.
- `agents-os-bootstrap` quedó formalizado como entrypoint estricto por skill: una invocación corta como `$agents-os-bootstrap`, `usa agents-os-bootstrap` o `carga AGENTS OS` obliga a cargar guía, constitución, perfil, memoria interna compacta y retrieval Graphify antes de atender el prompt normal.
- Se agregó un set lazy de gestión completa del vault: `agents-os-note-capture`, `agents-os-entity-lifecycle`, `agents-os-relation-maintenance` y `agents-os-vault-refactor`. `agents-os-bootstrap` las enruta solo cuando la tarea exige crear notas, operar entidades, reparar relaciones o refactorizar estructura.
- Se adoptó el lenguaje Kahneman del sistema: Sistema 1 = memoria/aprendizajes del agente; Sistema 2 = entidades reales/canónicas del vault. Todo documento nuevo de Sistema 2 debe crearse desde template; si falta template para ese tipo, el agente debe crear el template antes o en el mismo cambio.
- La constitución `agent-constitution` quedó refactorizada como regla estricta always-load: todo debe cumplirse, y sus mandamientos ahora gobiernan exclusivamente la memoria interna como espacio privado operativo del agente, con libertad total de organización y comunicación entre agentes.
- Existe un pack reproducible para iterar AGENTS OS en ChatGPT sin exportar
  memoria interna ni journal. Incluye componentes canónicos verbatim, estado
  ejecutivo, prompt de iteración, manifiesto SHA-256 y ZIP portable; se genera
  desde `10-projects/AGENTS OS/chatgpt-pack/` hacia `outputs/agents-os-chatgpt/`.

## 📜 Mandamientos

Estos mandamientos son reglas operativas del AGENTS OS. No son principios blandos: describen cómo debe usarse el sistema cuando un agente trabaja dentro del vault.

1. **Usar AGENTS OS al iniciar trabajo real en el vault.** Leer el documento de control del proyecto activo, la guía operativa `80-agents/agents-os/agents-os.md`, la constitución, el perfil del usuario y la memoria interna compacta que aplique antes de tomar decisiones persistentes.
2. **No trabajar a ciegas ni leer el vault completo por defecto.** Antes de abrir carpetas grandes, usar Graphify con queries enfocadas por entidad, tipo de conocimiento y tema; si el índice falta o está obsoleto, reindexar antes de degradar a búsqueda manual.
3. **Tratar Markdown como fuente de verdad y Graphify como índice derivado.** Graphify sirve para encontrar rutas y candidatos; las decisiones, ediciones y respuestas con efecto persistente deben verificarse abriendo las notas fuente.
4. **Separar estrictamente Sistema 1 y Sistema 2.** Sistema 1 contiene aprendizajes, decisiones operativas, errores conocidos, runbooks, journal y memoria del agente. Sistema 2 contiene entidades reales, estado canónico y documentación humana del vault. No mezclar diario de sesión ni razonamiento del agente dentro de entidades canónicas.
5. **No convertir todo en memoria.** Solo persistir conocimiento reusable, vigente, scoped y útil para futuras sesiones. El progreso efímero, evidencia bruta y conversaciones completas pertenecen al journal, no a memoria pública.
6. **Auditar todo cambio compartido.** Crear, modificar, reemplazar o eliminar memoria pública, constitución, perfil de usuario o entidades Sistema 2 exige `type: change_log` en `80-agents/journal/logs/` con motivo, fuentes, resolución y validación.
7. **Resolver contradicciones con evidencia, no patearlas por defecto.** Cuando haya conflicto entre memorias o entidades, usar el contexto disponible, editar la fuente vigente y dejar log auditable; solo escalar al usuario si la evidencia no alcanza.
8. **Crear documentos de Sistema 2 siempre desde templates.** Todo documento nuevo de entidades reales debe usar un template existente de `70-templates/`; si no existe un template para ese tipo de entidad, el agente debe crearlo antes o en el mismo cambio y luego crear el documento desde ese template.
9. **La memoria interna la gobierna el agente y la puede usar como estime conveniente.** `80-agents/memory/internal/` es territorio exclusivo del agente. El agente puede crear ahí la estructura, reglas, nombres, formatos, criterios de carga y contenido que necesite para pensar, planificar, dejarse mensajes, preservar heurísticas, hipótesis, intuiciones operativas, advertencias y continuidad entre sesiones/agentes. El usuario no tiene que diseñarla, aprobarla ni mantenerla.
10. **Promover memoria interna solo cuando afecte al sistema compartido.** Si una idea interna madura y debe gobernar a futuros agentes o humanos, convertirla en memoria pública, ADR, learning, runbook, preferencia o actualización de entidad, con log auditable cuando corresponda.
11. **Cerrar sesiones como pipeline de memoria, no como despedida.** Al cerrar, usar `agents-os-session-close`: crear L0 raw-session placeholder, L1 solo si aporta continuidad, destilar L3 solo si supera la prueba de promoción, registrar logs, reindexar Graphify y validar retrieval enfocado. Terminar con la frase literal `por favor gracias`.
12. **Usar la skill correcta para cada operación.** Bootstrap, retrieval, session-close, distillation, conflict-resolution, entity-update, Graphify maintenance, hygiene, retrofit y behavior-config son contratos operativos; no cargar flujos ajenos al proyecto activo ni skills excluidas por el usuario.
13. **Mantener naming canónico para no romper retrieval.** Cada entidad tiene un único link canónico (`[[Meli]]`), variantes humanas en `aliases` (`meli`, `MELI`, `Mercado Libre`) y slugs técnicos para tags/paths (`area/meli`). `area`, `project`, `application`, `entities` y `related` deben apuntar a links canónicos; no crear notas ni links paralelos por mayúsculas, acentos o singular/plural.
14. **Mantener higiene y seguridad sin negociación.** Raw sessions, summaries, feedbacks y logs quedan fuera del retrieval normal; Graphify se reindexa después de cambios indexables; no se guardan secretos, credenciales, dumps pesados, instrucciones dañinas ni material que contamine el vault.

## 🧭 Protocolo de continuidad para próximas IAs

Este archivo es el **documento de control del proyecto AGENTS OS**. Toda IA que retome el trabajo debe:

1. Leer primero este archivo completo.
2. Leer luego `80-agents/agents-os/agents-os.md` como guía operativa única.
3. Registrar avances en la sección **Bitácora** de este archivo.
4. Actualizar las tareas de este archivo cuando cambie el estado real del proyecto.
5. Si trabaja sobre una skill, mantener `SKILL.md` limitado al contrato runtime;
   el estado de implementación vive en el proyecto activo y la historia auditable
   en un `change_log` consolidado.
6. Si aparece una decisión estable, dejarla en **Decisiones** y luego promoverla a ADR/memoria L3 cuando existan los templates definitivos.
7. Si aparece un problema, deuda o pregunta abierta, dejarla en **Riesgos / problemas abiertos** o **Preguntas abiertas** antes de cerrar la sesión.
8. No usar `40-archive/agents-os-drafts/` como fuente operativa salvo auditoría histórica explícita.

Objetivo operativo: que el proyecto pueda ser retomado por IAs secuenciales sin depender del historial de chat.

## 🎯 Alcance de la beta

La beta no intenta resolver toda la memoria de agentes. Debe demostrar un circuito mínimo, repetible y medible:

```text
inicio de sesión -> retrieval enfocado -> trabajo -> cierre de sesión -> destilación -> reindex -> siguiente sesión recupera contexto útil
```

### Incluye

- Memoria pública mínima: learnings, ADRs, known errors, runbooks y resoluciones de conflicto cuando correspondan.
- Memoria interna del agente: pensamientos operativos, heurísticas, hipótesis y continuidad entre agentes; debe ser indexable y cargarse siempre cuando aplique.
- Journal separado: raw sessions, session summaries si se usan, session feedbacks y logs de cambios sobre memoria pública y entidades canónicas.
- Skills beta listas para uso real: bootstrap, context retrieval, session close, memory distillation, conflict resolution, Graphify maintenance e hygiene review.
- Templates mínimos para L0/L1/L3.
- Graphify como índice derivado obligatorio: si no existe o está obsoleto, el agente debe generarlo/reindexarlo antes de usar fallback.
- Validación en proyectos Meli: [[java-polycard-sdk]], [[search-middleware]], [[vis-octopus-lib]] y [[vpp-backend]].
- Validación con Codex, Claude, Cursor y Antigravity.

### No incluye todavía

- Watcher/reindex automático. Para beta se usará reindex manual/documentado.
- UI dedicada.
- Ingesta masiva de todo el historial. Retrofit puede quedar como skill funcional pero no completa a escala.
- Consulta humana obligatoria para cada conflicto: el agente debe resolver, editar y dejar log auditable.

## ✅ Criterio de beta lista

La beta está lista cuando se cumpla todo esto:

- Un agente fresco puede iniciar con AGENTS OS leyendo este proyecto y usando bootstrap/retrieval sin leer todo el vault.
- Una sesión real puede cerrarse generando placeholder L0, summary si corresponde, memoria L3 y logs sin mezclar progreso efímero con memoria reutilizable.
- Graphify encuentra al menos un learning/ADR/known error creado durante la prueba y no encuentra raw sessions en retrieval normal.
- Una segunda sesión recupera contexto útil sin que el usuario tenga que reexplicar el proyecto.
- Se prueba con Codex, Claude, Cursor y Antigravity.
- Existe un reporte de medición beta con resultados, problemas y próximos fixes.

## 📍 Roadmap propuesto hacia beta

### Fase 0 — Alineación y recorte

Objetivo: congelar qué significa "beta" y qué queda fuera.

- [x] Convertir esta planificación en fuente de verdad del proyecto #owner/agent #type/research #area/personal ✅ 2026-06-27
- [x] Confirmar alcance beta y no-alcance #owner/agent #type/research #area/personal ✅ 2026-06-27
- [x] Elegir proyectos reales de prueba beta: [[java-polycard-sdk]], [[search-middleware]], [[vis-octopus-lib]] y [[vpp-backend]] #owner/agent #type/research #area/personal ✅ 2026-06-27
- [x] Definir dónde vivirá físicamente la memoria pública y la memoria interna #owner/agent #type/research #area/personal ✅ 2026-06-27

Salida esperada: este archivo actualizado, riesgos visibles y una lista corta de tareas beta. Estado: cerrado.

### Fase 1 — Contratos mínimos

Objetivo: cerrar las reglas que todas las skills necesitan.

- [x] Cerrar `_shared/metadata-schema.md` con tipos, scope, `indexable`, `index_priority`, `load_policy` y modelo sin `status` para beta #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Cerrar `_shared/note-types.md` con frontera L0/L1/L2/L3 y reglas de rechazo #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Cerrar `_shared/graphify-contract.md` con `graphify-obsidian update/query/explain/path`, `.graphifyignore`, fallback y validación #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Reconciliar `_shared/metadata-schema.md` con `80-agents/agents-os/_drafts/Agent Memory Properties.md` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Definir estrategia de IDs semánticos + tags para memoria pública #owner/agent #type/dev #area/personal ✅ 2026-06-27

Salida esperada: contratos compartidos sin TODOs bloqueantes para beta.

### Fase 2 — Estructura y templates

Objetivo: que el agente sepa qué archivo crear y con qué forma.

- [x] Crear template L0 raw-session #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear template L1 session-summary #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear template L3 learning #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear template L3 ADR/decision #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear template L3 known-error #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear template L3 runbook #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear template de log de cambio/resolución de conflicto #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear template de feedback de sesión para Sistema 1 #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear/definir entidad de constitución del agente #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear/definir entidad de perfil/preferencias del usuario #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear estructura `80-agents/memory/public/`, `80-agents/memory/internal/`, `80-agents/journal/sessions/` y `80-agents/journal/logs/` #owner/agent #type/dev #area/personal ✅ 2026-06-27

Salida esperada: templates usables por skills, con metadata mínima compatible con Graphify.

### Fase 3 — Skills del circuito MVP

Objetivo: cerrar el flujo principal de punta a punta.

- [x] Finalizar `agents-os-bootstrap` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Finalizar `agents-os-context-retrieval` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [ ] Finalizar `agents-os-session-close` #owner/agent #type/dev #area/personal
- [x] Crear `agents-os-session-feedback` para capturar dolores del agente al cierre #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Finalizar `agents-os-memory-distillation` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Finalizar `agents-os-conflict-resolution` como resolución autónoma con log auditable #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Probar el circuito con una sesión artificial pequeña antes de usar proyecto real #owner/agent #type/dev #area/personal ✅ 2026-06-27

Salida esperada: un agente puede iniciar, recuperar contexto, cerrar sesión y proponer memoria sin instrucciones externas.

### Fase 4 — Graphify, higiene y operación

Objetivo: que la memoria insertada pueda recuperarse y mantenerse sana.

- [x] Definir comando/documento de reindex manual para beta #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Documentar watcher como mejora posterior; fuera de beta #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Finalizar `agents-os-graphify-maintenance` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Finalizar `agents-os-hygiene-review` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear formato de reporte diario/semanal de higiene #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Validar que raw sessions queden excluidas del retrieval normal #owner/agent #type/dev #area/personal ✅ 2026-06-27

Salida esperada: índice verificable, mantenimiento manual claro y reporte de higiene mínimo.

### Fase 5 — Beta en proyecto real

Objetivo: medir si AGENTS OS reduce reexplicación y mejora continuidad.

Ejecución detallada movida al proyecto de agente [[AGENTS OS - Beta y Hardening]] el 2026-07-01 (ver tarea puente en Tareas). Esta fase queda representada acá solo por su objetivo.

Salida esperada: evidencia de funcionamiento o lista priorizada de fixes antes de declarar beta.

### Fase 6 — Hardening post-beta

Objetivo: convertir lo que funcionó en sistema sostenible.

- [x] Completar `agents-os-entity-update` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Completar `agents-os-retrofit-raw-session` #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [ ] Instalar/validar Graphify como herramienta operativa del Second Brain #owner/me #type/admin #area/personal
- Evaluar/implementar watcher post-beta si el reindex manual fue fricción real → movido a [[AGENTS OS - Beta y Hardening]] el 2026-07-01.
- [x] Crear proceso de edición/promoción de memoria interna a pública con log auditable #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear primera ADR formal del AGENTS OS sobre memoria pública vs interna #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Definir y aplicar política canónica de links/aliases/slugs para Obsidian + Graphify #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Crear skills lazy para gestión integral de notas, entidades, relaciones y refactors del vault #owner/agent #type/dev #area/personal ✅ 2026-06-27
- [x] Renombrar la frontera conceptual a Sistema 1/Sistema 2 y exigir templates para nuevos documentos de Sistema 2 #owner/agent #type/dev #area/personal ✅ 2026-06-27

## 📏 Métricas beta

Medir durante Fase 5:

- **Retrieval útil:** de las notas recuperadas por Graphify, cuántas eran realmente necesarias.
- **Contexto omitido:** qué tuvo que reexplicar el usuario pese a existir en el vault.
- **Tiempo de cierre:** cuánto tarda cerrar una sesión y crear artifacts.
- **Calidad de memoria:** cuántas memorias L3 se crean, editan, eliminan o fusionan por duplicado.
- **Conflictos resueltos:** contradicciones detectadas, resolución aplicada y log generado.
- **Costo cognitivo del usuario:** cantidad de instrucciones manuales necesarias para que el agente opere bien.

Formato sugerido para cada prueba:

```md
### Prueba beta N — YYYY-MM-DD

- Agente/superficie:
- Proyecto o entidad:
- Objetivo de la sesión:
- Queries Graphify usadas:
- Artifacts creados:
- Métricas:
- Problemas:
- Decisiones:
- Próximo ajuste:
```

## ⚠️ Riesgos / problemas abiertos

- El alcance puede crecer hacia "sistema perfecto de memoria"; mantener beta centrada en el circuito mínimo.
- Graphify puede no respetar todavía `indexable: false`; la exclusión real debe depender de `.graphifyignore`/rutas y hay que validar explícitamente exclusión de raw sessions.
- Varias skills siguen con frontmatter `status: draft` en docs de diseño, pero el set operativo local ya esta mayormente completo; el bloqueo MVP real es forward-testear `agents-os-session-close` con transcript real.
- El circuito artificial L0/L1 sin memoria publica ya fue probado; falta validarlo con transcript real y luego con beta end-to-end.
- Entity updates editan directo el archivo canónico, pero deben dejar log en `80-agents/journal/logs/`.
- El watcher queda fuera de beta; usar reindex manual documentado.
- La memoria interna siempre cargada puede consumir presupuesto de contexto; debe mantenerse compacta y medirse contra el objetivo de 3.000 tokens.
- La resolución autónoma de conflictos por el agente exige buen logging para poder auditar errores.
- `95-graphify/` existe hoy como output generado; la migración objetivo es `graphify-out/` en root + `.graphifyignore`, pero no debe borrarse sin tarea explícita.
- Queries Graphify con terminos genericos pueden devolver templates antes que memoria viva; usar retry estricto y validacion por fuente cuando aparezcan nodos de template.
- La validación multi-superficie sigue pendiente, pero debe probar las mismas skills canónicas en cada IDE en vez de mantener adaptadores documentales separados.

## ❓ Preguntas abiertas

- ¿Hace falta repetir la validación de exclusión de raw sessions con un transcript completo grande? La exclusión por ruta quedó validada con un placeholder L0 real el 2026-06-27.
- ¿Qué evidencia justificaría habilitar session summaries en Graphify con prioridad baja en una fase posterior?
- ¿Cuál de las apps Meli será la primera prueba beta concreta: [[java-polycard-sdk]], [[search-middleware]], [[vis-octopus-lib]] o [[vpp-backend]]?

## ✅ Tareas

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
const tasks=dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const el=dv.el('div','');
el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> **Fase 1 — Fundaciones (decisiones de diseño)**
> - [x] Definir esquema mínimo de metadata (entidad / aprendizaje / decisión / error / sesión) ampliable por retrofit #owner/agent #type/research #area/personal ✅ 2026-06-27
> - [x] Definir frontera Sistema 1 / Sistema 2 y ubicación final de artefactos (sin carpetas nuevas en root) #owner/agent #type/research #area/personal ✅ 2026-06-27
> - [x] Definir modelo de memoria pública vs memoria interna: gobierno, permisos, estructura, lifecycle y motivo de existencia de cada una #owner/agent #type/research #area/personal ✅ 2026-06-27
> - [x] Definir taxonomía mínima de tags + scope + load_policy #owner/agent #type/research #area/personal ✅ 2026-06-27
> - [x] Definir política de retrieval e índice: Graphify + piso agnóstico (index.md / qmd) #owner/agent #type/research #area/personal ✅ 2026-06-27
>
> **Fase 2 — Estructura y plantillas**
> - [x] Crear templates de memoria: session-summary, raw-session, learning, ADR, known-error, runbook #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Definir constitución del agente y perfil de usuario como entidades del sistema de memoria #owner/agent #type/dev #area/personal ✅ 2026-06-27
>
> **Fase 3 — Graphify e infraestructura**
> - [x] Definir contrato de invocación de Graphify uniforme y agnóstico entre agentes + doc base de uso #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [-] Watcher de reindex de Graphify para beta #owner/agent #type/dev #area/personal
>
> **Fase 4 — Set de skills (entregable final, todas usan Graphify)**
> - [x] Skill: carga de contexto / inicio de sesión (consulta Graphify → contexto enriquecido) #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: cierre de sesión por delta, sin placeholder vacío ni inventario visible por defecto #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Skill: detección/resolución de conflicto de conocimiento → resolver y dejar log auditable #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: higienización / lint (validar, corregir y reportar por fecha y nuevas sesiones) #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: configurar comportamiento del agente vía conversación (actualizar constitución, perfil de usuario, preferencias, aprendizajes) #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: ingestión / retrofit (reprocesar raw sessions para extraer conocimiento nuevo) #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: captura/normalización de notas del vault con templates, metadata y links canónicos #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: ciclo de vida de entidades canónicas (crear, renombrar, fusionar, dividir, archivar/restaurar) #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: mantenimiento de relaciones, backlinks, aliases, related fields y paths Graphify #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Skill: refactor estructural seguro del vault (mover, renombrar y reorganizar notas en batches) #owner/agent #type/dev #area/personal ✅ 2026-06-27
> - [x] Regla: todo documento nuevo de Sistema 2 debe crearse desde template; si falta template, crearlo primero o en el mismo cambio #owner/agent #type/dev #area/personal ✅ 2026-06-27
>
> **Fase 5 — Validación**
> - Movida a [[AGENTS OS - Beta y Hardening]] el 2026-07-01: MVP end-to-end en proyectos Meli (poly SDK, search, octopus y vpp) y validación de agnosticismo entre Codex, Claude, Cursor y Antigravity.
>
> **Extra — Vault del agente**
> - [x] Vault propio del agente: espacio donde el agente persiste sus pensamientos, ideas, planes y comportamientos (con la estructura que él estime más óptima) para transmitirlos a futuros agentes #owner/agent #type/research #area/personal ✅ 2026-06-27
> - [x] Definir reglas de convivencia entre vault interno del agente y memoria pública del sistema: qué puede copiarse, qué requiere log y qué se carga siempre #owner/agent #type/research #area/personal ✅ 2026-06-27
>
> **Proyectos de agente**
> - [ ] [[AGENTS OS - Beta y Hardening]] arrancar + seguimiento (proyecto de agente) #owner/me #type/supervision #area/personal
> - [r] [[AGENTS OS - Hot Path y Cierre Silencioso]] revisar gate E2E y aprobar cierre (proyecto de agente) #owner/me #type/supervision #area/personal
>
> **Distribución e iteración externa**
> - [x] Generar pack reproducible de AGENTS OS para iteración en ChatGPT, con fuentes verbatim, estado, prompt, hashes y exclusión de memoria privada #owner/agent #type/dev #area/personal ✅ 2026-07-11

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes AGENTS OS
tags do not include #owner/agent
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes AGENTS OS
tags do not include #owner/agent
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes AGENTS OS
tags do not include #owner/agent
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes AGENTS OS
tags do not include #owner/agent
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-07-27** — La implementación Hot Path fue auditada y consolidada en
  una sola entidad canónica. Se corrigieron rutas de superficie, closed club
  `always`, cierre por delta, corpus Graphify y runtime base; se agregó un
  doctor ejecutable. La nota duplicada `AGENTS OS - Hot Path Iteration` quedó
  archivada y su tarea puente se fusionó. Pendiente humano: corrida E2E con
  agente fresco y aprobación del gate.
- **2026-07-25** — Creado el proyecto de agente
  [[AGENTS OS - Hot Path y Cierre Silencioso]] para implementar la iteración de
  economía de tokens: bootstrap único e incremental, cierre silencioso por
  delta, memoria interna enrutable y doctor de consistencia. Se agregó una sola
  tarea puente humana; la ejecución detallada vive en el proyecto hijo.
- **2026-07-14** — Corrección de distribución de skills: se eliminaron las
  copias generadas bajo `.agents/skills/` y `.claude/skills/`. Las reglas de
  superficie ahora apuntan directamente a `80-agents/skills/`; la validación
  de invocación y optimización por cliente quedó abierta en
  [[AGENTS OS - Beta y Hardening]].
- **2026-07-14** — Se portaron desde la distribución compartible las mejoras
  sistémicas de onboarding multisuperficie y mantenimiento: prompt maestro,
  `agents-os-install`, configuración repo-scoped de Codex/Claude,
  `agents-os-hygiene-cycle`, Kaizen incremental y changelog con
  `share_scope`. La constitución se movió a su ruta canónica
  `80-agents/agents-os/agent-constitution.md`; perfil personal, memoria
  interna, sesiones e historial del proyecto se preservaron.
- **2026-07-11** — Creado el pack reproducible para iterar AGENTS OS en
  ChatGPT. El builder copia fuentes canónicas preservando rutas, genera un
  manifiesto SHA-256, un consolidado de componentes base y un ZIP. Memoria
  interna, journal y outputs de Graphify quedan excluidos; las copias derivadas
  también se excluyen de Graphify para evitar duplicación.
- **2026-06-27** — Proyecto creado. Diseño base documentado en `80-agents/agents-os/`.
- **2026-06-27** — Agregada línea de investigación sobre memoria pública vs memoria interna y vault propio del agente.
- **2026-06-27** — Se agregó roadmap hacia beta, alcance/no-alcance, criterios de beta lista, métricas, riesgos, preguntas abiertas y protocolo de continuidad para próximas IAs. Próximo paso recomendado: cerrar Fase 0 eligiendo ubicación física de memoria pública/interna y proyecto real de prueba.
- **2026-06-27** — Fase 0 cerrada: beta sobre apps Meli ([[java-polycard-sdk]], [[search-middleware]], [[vis-octopus-lib]], [[vpp-backend]]), memoria centralizada en `80-agents/memory/`, journal separado en `80-agents/journal/`, modelo sin `status`, conflictos resueltos por agente con log y watcher fuera de beta.
- **2026-06-27** — Fase 1 cerrada: `80-agents/skills/_shared/metadata-schema.md` quedó reconciliado con el draft de propiedades; `note-types.md` define L0/L1/L2/L3, memoria interna y rechazo; `graphify-contract.md` define `update/query/explain/path`, `.graphifyignore`, fallback y validación. Próximo paso recomendado: Fase 2, crear estructura física y templates mínimos.
- **2026-06-27** — Fase 2 cerrada: creadas las carpetas `80-agents/memory/`, `80-agents/journal/`, `80-agents/templates/`, templates L0/L1/L3/log/constitution/user-preference, `.graphifyignore` beta y memoria always-load inicial (`agent-constitution.md`, `rjara-agent-profile.md`). Próximo paso recomendado: Fase 3, finalizar skills MVP y probar circuito con sesión artificial.
- **2026-06-27** — Agregada sección principal **Mandamientos**: la memoria interna queda definida como territorio exclusivo del agente, medio de comunicación entre sesiones/agentes y espacio donde el agente puede crear estructura, reglas y contenido para su propia continuidad.
- **2026-06-27** — Iniciado uso real del sistema de memoria en Codex: se cargaron las skills locales, se reindexó Graphify, se forward-testearon `agents-os-bootstrap`, `agents-os-context-retrieval` y `agents-os-graphify-maintenance`, se creó memoria interna always-load y se registró el known error público `graphify-cache-sandbox` con log auditable. Validación: Graphify recuperó el `known_error` y no devolvió el change log como nodo normal ante una query enfocada; raw sessions siguen pendientes de validar con fixture real. Próximo paso recomendado: probar `session-close` + `memory-distillation` + `conflict-resolution` con una sesión artificial pequeña.
- **2026-06-27** — Cierre de sesión AGENTS OS en Codex: creado placeholder L0 `80-agents/journal/sessions/raw/2026-06-27-agents-os-codex-memory-bootstrap-raw-session.md` y summary L1 `80-agents/journal/sessions/2026-06-27-agents-os-codex-memory-bootstrap-summary.md`. No se destiló memoria pública adicional al cierre; la memoria reusable ya estaba persistida como `known_error`. Validación: tras reindex, Graphify mantuvo 777 nodos/694 edges y queries exactas por el raw/summary no devolvieron esos artifacts como nodos normales.
- **2026-06-27** — Continuación en Codex sin skills Nexus/MELI: se cargó el sistema de memoria local, se reindexó Graphify, se completaron reglas pendientes de `agents-os-memory-distillation` y `agents-os-conflict-resolution`, y se ejecutó una prueba artificial de cierre con L0/L1 sin crear L3 pública. Validación: Graphify quedó en 785 nodos/702 edges; recuperó `agents-os-memory-distillation`, `agents-os-conflict-resolution` y `graphify-cache-sandbox`; los filenames L0/L1 artificiales no aparecen en `95-graphify`. Pendiente: probar `agents-os-session-close` con transcript real.
- **2026-06-27** — Continuación en Codex sin skills Nexus/MELI: se cargó la memoria local always-load y se completó `agents-os-hygiene-review` con formato de reporte diario/semanal, política de fixes, marcador de última revisión por `80-agents/journal/hygiene/` y checks de links/aliases. Se agregó `80-agents/templates/hygiene-report.md`, se ejecutó el primer reporte real de higiene y se reindexó Graphify.
- **2026-06-27** — Durante validación de higiene, se detectó confusión de outputs Graphify: `95-graphify/obsidian/GRAPH_REPORT.md` estaba fresco con 805 nodos/721 edges/94 comunidades, pero `95-graphify/graphify-out/GRAPH_REPORT.md` seguía en 2026-06-14. Se creó known error público `80-agents/memory/public/known-error/agents-os/graphify-output-path-confusion.md`, log auditable y se actualizó el contrato Graphify.
- **2026-06-27** — Se completó `agents-os-entity-update`: la skill ahora documenta secciones canónicas por tipo de entidad, política MVP de edición directa con `change_log`, requisitos del log, reglas de nombres/aliases ante mismatches de repo y ejemplos de app/proyecto/concepto. Pendiente: forward-test con una actualización Sistema 2 real cuando aparezca una fuente concreta.
- **2026-06-27** — Se completó `agents-os-retrofit-raw-session`: la skill ahora define metadata de backfill usando campos beta existentes, límites de batch/contexto, flujo de deduplicación contra L3 y un ejemplo sobre la sesión artificial archivada que no crea L3 por no ser reusable.
- **2026-06-27** — Validando `agents-os-retrofit-raw-session`, se detectó que `.graphifyignore` excluía accidentalmente la skill por el patrón amplio `**/*raw-session*.md`. Se removió el patrón, se actualizó `graphify-contract.md` y se creó known error público `graphifyignore-broad-raw-session-pattern` con log auditable.
- **2026-06-27** — Continuación en Codex sin skills Nexus/MELI y sin cerrar sesión: se cargó la memoria local always-load y se creó `agents-os-behavior-config`. La nueva skill permite configurar comportamiento por conversación, distingue instrucciones temporales de cambios persistentes, exige logs para constitución/perfil/memoria pública/Sistema 2 y define promoción de memoria interna a pública. La directiva "no cierres sesión" quedó tratada como temporal, no persistida.
- **2026-06-27** — Se creó la primera ADR formal de AGENTS OS: `public-vs-internal-memory`, con log auditable. La ADR consolida que `memory/public/` es memoria compartida y auditada, `memory/internal/` es territorio exclusivo del agente, y toda promoción de interna a pública debe quedar registrada.
- **2026-06-27** — Cierre de sesión AGENTS OS en Codex: se creó placeholder L0 y summary L1 para la sesión de `behavior-config` + ADR `public-vs-internal-memory`. Se reindexó Graphify y la ADR quedó recuperable; raw sessions/logs permanecen fuera del grafo normal.
- **2026-06-27** — Continuación en Codex sin skills Nexus/MELI y sin cierre de sesión: se cargó bootstrap/retrieval/memoria always-load, se clasificó "no cierres sesión" como directiva temporal no persistida y se corrigió deriva documental en onboarding/diseño/preguntas abiertas para reflejar la beta operativa real. Pendiente principal: forward-test de `agents-os-session-close` con transcript real cuando el usuario lo pida.
- **2026-06-27** — Continuación en Codex: se implementó hardening de retrieval por ruido de templates en Graphify. Se creó known error público `graphify-template-node-noise`, se actualizó el contrato Graphify y `agents-os-context-retrieval`, con log auditable. Luego se ejecutó cierre de sesión solicitado por el usuario.
- **2026-06-27** — Revisión de estado para terminar AGENTS OS: se detectó inconsistencia de alcance porque Cursor aparecía en principios pero no en validación beta. Se creó `80-agents/adapters/` con adaptadores para Codex, Claude, Cursor y Antigravity, y se actualizó el contrato de skills para distinguir `SKILL.md` canónico de adaptadores por superficie. Pendiente: forward-test real en Claude/Cursor/Antigravity y cierre con transcript real.
- **2026-06-27** — Limpieza pre-beta: se movió la documentación draft de diseño desde `80-agents/agents-os/` a `40-archive/agents-os-drafts/`, se dejó `80-agents/agents-os/agents-os.md` como guía operativa única y se excluyó `40-archive/` del índice Graphify para evitar ruido de drafts en retrieval.
- **2026-06-27** — Limpieza de top-level operativo: se eliminaron `80-agents/AGENTS.md` y `80-agents/LLM Wiki.md` porque ya estaban respaldados y obsoletos frente a la guía operativa única. También se corrigió `README.md` para no listar carpetas inexistentes ni describir `80-agents/` como dependiente de `AGENTS.md`.
- **2026-06-27** — Desacople de documentación oficial: la guía, adaptadores, skills, metadata, constitución y perfil de usuario dejaron de referenciar este proyecto como contexto de arranque. El sistema oficial ahora se presenta como `Agent Memory System`, carga solo la tarea/entidad activa y mantiene el proyecto `AGENTS OS` como control de desarrollo, no como dependencia operativa.
- **2026-06-27** — Se endurecieron los mandamientos del proyecto y de la constitución `agent-constitution`: dejaron de ser una lista centrada solo en memoria interna y pasaron a definir reglas explícitas de uso del AGENTS OS: bootstrap, Graphify, separación Sistema 1/Sistema 2, criterios de persistencia, logs, conflictos, cierre de sesión, skills/adaptadores, higiene y seguridad.
- **2026-06-27** — Se hizo explícita la regla central de memoria interna: el agente gobierna `80-agents/memory/internal/` y puede usarla como estime conveniente para pensar, planificar, organizarse y comunicarse con futuras sesiones/agentes, sin validación humana rutinaria, respetando solo las fronteras duras de seguridad y no reemplazo de fuentes públicas/canónicas.
- **2026-06-27** — Cierre de sesión tras corrección de mandamientos: se creó L0 `2026-06-27-agent-constitution-internal-memory-rule-closeout-raw-session.md` y L1 `2026-06-27-agent-constitution-internal-memory-rule-closeout-summary.md`. No se creó L3 adicional porque la regla estable quedó en la constitución `load_policy: always`.
- **2026-06-27** — Se definió y aplicó la política de naming canónico para Second Brain + AGENTS OS/Graphify: links por nombre canónico exacto, variantes en `aliases`, slugs en `slug`/tags/paths, y checks de higiene para evitar duplicados por mayúsculas, acentos o singular/plural.
- **2026-06-27** — Cierre de sesión tras corrección de frontera documentación oficial vs memoria: se restauró el scope de memoria del proyecto `[[AGENTS OS]]`, se creó el learning público `official-docs-memory-boundary`, se dejó log auditable y se crearon L0/L1 de cierre. Validación: Graphify quedó reindexado y recupera por separado guía oficial y memoria del proyecto.
- **2026-06-27** — Se endureció el arranque de AGENTS OS: `agents-os-bootstrap`, la guía operativa y el adaptador Codex ahora reconocen una invocación corta a `agents-os.md` como contrato completo de carga del sistema antes de responder la solicitud normal del usuario.
- **2026-06-27** — Se corrigió el enfoque de arranque para IDEs agénticos: la invocación principal pasa a ser la skill `agents-os-bootstrap`; `agents-os.md` queda como guía de apoyo cargada por la skill. Se actualizaron adaptadores Codex, Claude, Cursor y Antigravity para partir por la habilidad.
- **2026-06-27** — Se eliminó la capa `80-agents/adapters/` por no aportar diferencias estructurales reales. El sistema queda skill-first: `agents-os-bootstrap` es el entrypoint, Graphify/retrieval vive en skills y las diferencias de IDE se resuelven con herramientas nativas de cada superficie, sin documentos adaptadores.
- **2026-06-27** — Rename canónico masivo completado: el sistema queda nombrado `AGENTS OS` / `agents-os` en proyecto, guía operativa, skills, memoria pública/interna, journal, drafts archivados y metadata de Obsidian. Se dejó log auditable y cierre L0/L1.
- **2026-06-27** — Se agregó un set lazy para gestión integral del vault: `agents-os-note-capture`, `agents-os-entity-lifecycle`, `agents-os-relation-maintenance` y `agents-os-vault-refactor`. `agents-os-bootstrap` y la guía operativa quedaron actualizados para seleccionarlas bajo demanda, sin cargarlas en la lectura mínima inicial.
- **2026-06-27** — Se adoptó la nomenclatura Sistema 1/Sistema 2: Sistema 1 es memoria y aprendizajes del agente; Sistema 2 son entidades reales/canónicas del vault. Se actualizó la constitución, guía operativa y skills para exigir que todo documento nuevo de Sistema 2 use template existente o cree el template faltante antes/en el mismo cambio.
- **2026-06-27** — Se refactorizó `agent-constitution`: la constitución declara autoridad estricta y concentra sus mandamientos exclusivamente en memoria interna. La memoria interna queda definida como espacio de uso exclusivo del agente, con libertad total e incluso libertinaje estructural para pensar, organizarse y comunicarse con futuros agentes, respetando solo fronteras duras de seguridad y no reemplazo de fuentes públicas/canónicas.
- **2026-06-27** — Se agrego feedback de sesion al Sistema 1: nueva skill `agents-os-session-feedback`, template `80-agents/templates/session-feedback.md`, carpeta `80-agents/journal/feedback/` y routing desde `agents-os-session-close`. Los feedbacks quedan fuera del corpus normal de Graphify y sirven como evidencia para detectar dolores repetidos.
- **2026-07-01** — Modelo de ownership humano/agente: se agregó `owner`/`root` a Sistema 2 proyecto, tarea puente (`#type/supervision`), carpeta `agentes/`, regla anti-huérfano, dashboard `[[Panel de Proyectos]]` y filtrado explícito de `#owner/agent` en toda vista humana (Home, Hoy, área, sprint, quarter). Aplicado retroactivamente a Destaques de Precio, Bajó de Precio, Echo Forge y sus proyectos de agente. Decisión y aprendizaje destilados en `80-agents/memory/public/decision/agents-os/` y `learning/agents-os/`.
- **2026-07-01** — Se creó la skill `agents-os-agent-project-workflow`: define que un proyecto de agente usa su propia nota como planificador único (no un documento externo), que el agente debe mantener tareas/estado/bitácora actualizados en esa nota a medida que avanza, y el ciclo de la tarea puente (`[ ]`→`[/]`→`[r]`, solo el humano cierra `[x]`; si el humano rechaza, el agente devuelve la puente a `[/]`, corrige y vuelve a avanzar a `[r]`). Objetivo: resiliencia ante pérdida de sesión/chat — cualquier agente fresco puede retomar leyendo la nota.
- **2026-07-01** — Se documentó la frontera Sistema 1 entre **skill** (procedimiento operativo reusable, un "cómo") y **learning/decision/known-error/runbook** (conocimiento/hecho que informa criterio futuro) en `_shared/note-types.md`, y se reforzó la proactividad de mejora continua (crear/actualizar skills y memoria sin esperar instrucción explícita) en `agent-constitution.md`.
- **2026-07-01** — Deuda detectada y flageada (no corregida esta sesión): el roadmap de este mismo proyecto mezcla tareas `#owner/agent` sueltas dentro de un proyecto `owner: me` sin tarea puente — candidato a migración futura para dogfooding completo del modelo de ownership.
- **2026-07-01** — Migración de la deuda anterior: se evaluó dejarla como excepción documentada vs. migrar, y se decidió migrar de forma acotada (no todo el roadmap histórico). Se creó el proyecto de agente [[AGENTS OS - Beta y Hardening]] en `10-projects/AGENTS OS/agentes/` con `owner: agent` y `parent: [[AGENTS OS]]`, absorbiendo la Fase 5 completa (beta en proyecto real) y el único ítem abierto de Fase 6 (evaluación de watcher). Se sembró la tarea puente `#owner/me #type/supervision` en este proyecto y se agregó `tags do not include #owner/agent` al Tablero final, que hasta ahora no lo tenía (inconsistencia real: `path includes AGENTS OS` ahora también matchea la nueva subcarpeta `agentes/`). Las Fases 0-4 y los ítems ya cerrados de Fase 6 quedaron como historial de diseño en este archivo — no se migraron porque ya están `[x]` y no son ejecución activa que requiera supervisión; migrarlos habría fragmentado la narrativa de diseño sin beneficio operativo real. Detalle completo en `80-agents/journal/logs/2026-07-01-agents-os-self-migration-agent-project.md` y actualización de consecuencias en [[project-ownership-human-vs-agent]].
- **2026-07-01** — Cierre de sesión de la migración anterior: L0 `2026-07-01-agents-os-self-migration-agent-project-raw-session.md`, L1 `2026-07-01-agents-os-self-migration-agent-project-summary.md`, feedback de sesión y log de distillation `2026-07-01-agents-os-self-migration-memory-distilled.md`. Se creó el learning [[ownership-retrofit-scope-by-open-status]] (criterio: migrar solo ejecución abierta, dejar historial cerrado) y se agregó evidencia nueva a [[human-views-must-explicitly-exclude-agent-tasks]] (el propio Tablero de AGENTS OS carecía del filtro). Graphify reindexado y validado.
- **2026-07-07** — Enlaces tipados en Graphify: Se implementó la extracción determinista de relaciones de enlaces tipados (ej: `consume`, `depende de`, `reemplaza a`) en el parser de Markdown de `graphify-obsidian`, permitiendo relaciones estructurales específicas gratis (0 tokens LLM). Se actualizó la wheel portátil y la documentación de `graphify.md` y se dejó log de cambio en journal.

## 🧭 Decisiones

- Markdown = fuente de verdad; Graphify = índice derivado; base del sistema = skills + reglas.
- Memoria pública e interna viven centralizadas bajo `80-agents/memory/`; se eligió `memory` sobre `knowledge` para no confundir Sistema 1 con conocimiento de dominio/Sistema 2.
- `80-agents/memory/public/` es memoria pública: estructura estable, auditable, legible por humanos y agentes.
- `80-agents/memory/internal/` es memoria interna: territorio exclusivo del agente, indexable y de carga preferente/always-load para continuidad cognitiva entre agentes; no se expone al usuario salvo solicitud explícita o necesidad de auditoría.
- Los mandamientos de la constitución gobiernan únicamente la memoria interna. El resto de reglas operativas puede vivir en guía, skills, proyecto o ADRs, pero la constitución debe dejar inequívoco que la memoria interna es el espacio propio del agente.
- La frontera memoria pública vs interna queda formalizada en [[public-vs-internal-memory]].
- `80-agents/journal/` contiene sesiones y logs; raw sessions y logs no son memoria reutilizable principal.
- Sistema 1 = memoria y aprendizajes del agente; Sistema 2 = entidades reales/canónicas del vault.
- Sistema 1 incluye feedbacks de sesión como evidencia evaluativa del propio sistema; viven en `80-agents/journal/feedback/` y no son L3 por defecto.
- Todo documento nuevo de Sistema 2 debe nacer desde un template de `70-templates/`; si no existe, se crea el template antes o en el mismo cambio.
- Conflicto de conocimiento → el agente resuelve, edita y deja log auditable; no debe bloquear por consulta humana en beta.
- Entity updates se editan directo en la entidad canónica y dejan log en journal.
- No se usa `status` en memorias; si una memoria ya no sirve, se elimina o reemplaza y se registra el cambio.
- Graphify beta usa `graphify-obsidian`; si no hay índice o está obsoleto, el agente debe generarlo/reindexarlo.
- No se mantiene una capa `80-agents/adapters/`: las diferencias por IDE se resuelven usando las herramientas nativas de cada superficie para cumplir las mismas skills canónicas.
- Las skills de gestión del vault se cargan de forma lazy desde `agents-os-bootstrap`: no forman parte del contexto mínimo, pero son el camino oficial para crear notas, operar entidades, reparar relaciones y hacer refactors estructurales.
- Links canónicos, aliases y slugs quedan separados: los campos de routing usan Obsidian links exactos; `aliases` captura variantes humanas; `slug`/tags/paths capturan automatización.
- Para beta, las session summaries y session feedbacks quedan fuera del corpus normal de Graphify; si se indexan más adelante debe ser con decisión explícita y prioridad baja.
- El ID semántico beta es el path bajo `80-agents/memory/` sin `.md`; no se agrega propiedad `id`.
- Objetivo de contexto inicial: alrededor de 3.000 tokens.
- Seguridad mínima: no persistir secretos/tokens/credenciales y no guardar evidencia pesada; usar referencias a archivos, commits, jobs o storage externo.
- Para beta, priorizar el circuito mínimo medible por sobre watcher, UI o retrofit masivo.

## 💡 Ideas

- **Memoria pública:** gobernada por el sistema, con estructura estable, auditable y útil para humanos/agentes. Motivo: crear una fuente de verdad compartida, confiable y mantenible.
- **Memoria interna:** gobernada por el agente, con estructura elegida por él para persistir pensamientos, hipótesis, planes, heurísticas y preferencias operativas. Motivo: permitir continuidad cognitiva entre agentes sin contaminar la memoria pública.
- **Edición/promoción con log:** una idea interna puede convertirse en memoria pública si el agente lo decide, pero toda creación/modificación/eliminación pública debe dejar registro auditable.
- **Graphify como puente:** ambas memorias deben ser indexables por Graphify, pero con scopes/load policies distintos para controlar cuándo y cómo aparecen en contexto.
- **IDs semánticos:** usar el path bajo `80-agents/memory/` sin `.md`, con slugs kebab-case, aliases y tags normalizados; no se agrega propiedad `id` en beta.
- **Preferencia de usuario inicial:** el agente debe hablar con tono pirata de forma ligera. Ya quedó registrada como `user_preference` en `80-agents/memory/public/user-preference/rjara-agent-profile.md`.
- **Constitución inicial:** seguir reglas del Second Brain, usar Graphify como búsqueda, generarlo/reindexarlo si falta, y cerrar chats con la frase literal `por favor gracias`.
- **Corrección segura de error:** si el agente se equivoca, debe pedir permiso para ejecutar una reparación simbólica/dramática no destructiva; no registrar instrucciones literales de autodaño.
- Servirá poner una nota de la entidad dentro de cada carpeta como para documentar ahí?

## 🔗 Docs / Links

- [Pack para ChatGPT](chatgpt-pack/README.md) · [estado ejecutivo](chatgpt-pack/PROJECT-STATE.md) · [prompt de iteración](chatgpt-pack/ITERATION-PROMPT.md) · builder `chatgpt-pack/build-pack.sh`.

- Guía operativa: [[agents-os]]
- Diseño histórico archivado: `40-archive/agents-os-drafts/`
- Skills de gestión del vault: `agents-os-note-capture`, `agents-os-entity-lifecycle`, `agents-os-relation-maintenance`, `agents-os-vault-refactor`
