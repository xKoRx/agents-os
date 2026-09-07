---
type: project
owner: agent
root: false
status: completed
priority: P0
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start: 2026-07-25
due:
progress: 100
repo:
jira:
prs:
aliases:
  - AGENTS OS Hot Path
  - AGENTS OS Cierre Silencioso
  - AGENTS OS Token Economy Iteration
  - AGENTS OS - Hot Path Iteration
tags:
  - area/personal
  - kind/project
  - project/agents-os
created: 2026-07-25
updated: 2026-08-01
---

# AGENTS OS - Hot Path y Cierre Silencioso

> [!info]+ AGENTS OS - Hot Path y Cierre Silencioso
> **Padre:** [[AGENTS OS]] · **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P0
> Iteración para recuperar la economía de tokens original de AGENTS OS mediante
> un arranque único e incremental, cierre silencioso por defecto y documentación
> core verificablemente consistente.

## 🎯 Objetivo

- Reducir de forma material el contexto cargado antes de la primera acción útil,
  sin perder información que cambie decisiones.
- Establecer un único procedimiento de bootstrap, con rutas cold/warm/cambio de
  entidad y memoria interna seleccionada por metadata.
- Separar la persistencia interna del cierre de su reporte al usuario: el sistema
  puede guardar continuidad, pero no debe enumerar memorias o artefactos salvo
  solicitud explícita, conflicto o error.
- Eliminar drift entre constitución, guía, skills, proyecto controlador,
  configuración de superficies, snapshots e índice Graphify.
- Validar el resultado con benchmarks comparables y agentes frescos.

## 📊 Estado actual

- **Cerrado administrativamente el 2026-08-01.** La implementación lograda se
  conserva como evidencia histórica; el gate E2E y toda iteración estructural
  restante fueron migrados a [[AGENTS OS - Fase 2]], que pasa a ser el único
  planificador activo.
- **Implementación consolidada y en Review.** P0–P4 están aplicados y el doctor
  estructural pasa. Resta el gate E2E con agente fresco para cerrar el proyecto.
- La implementación paralela que creó `AGENTS OS - Hot Path Iteration` fue
  fusionada aquí el 2026-07-27; su nota quedó en archivo histórico.
- El camino potencial de arranque carga aproximadamente **21–24 mil tokens**
  antes del contexto específico de la tarea. Es una estimación por tamaño de
  archivos, no un cap ni una métrica final.
- La causa principal es acumulativa: reglas de superficie + guía completa +
  constitución + perfil + bootstrap + retrieval + memorias internas `always`;
  `session-close` también está modelada como core/always-load.
- Existen al menos tres recetas de inicio que compiten y una selección no
  ejecutable llamada “memoria interna compacta”.
- El cierre mezcla persistencia con UX: su contrato obliga a reportar un
  inventario de raw, summary, feedback, learnings, ADRs, known errors, runbooks,
  entity updates, conflictos, logs, Graphify y tareas.
- El journal contiene **153 feedbacks** (`110` general + `43` de Graphify), con
  aproximadamente **75 mil palabras**. Las dos plantillas de feedback suman
  unas **663 palabras antes de ser llenadas**.
- Graphify devolvió en la auditoría fuentes live y copias bajo
  `outputs/agents-os-chatgpt/`, señal de que el corpus derivado no está
  efectivamente excluido.
- No se implementó ninguna corrección de comportamiento en la sesión que creó
  este proyecto. Las decisiones de abajo son dirección propuesta y deben
  convertirse en cambios pequeños, validados y auditables.

## 🔬 Hallazgos verificados

### P0 — Seguridad y portabilidad

1. `AGENTS.md` contenía una ruta absoluta dependiente de máquina. Las
   referencias de guía, constitución, perfil y skills podían fallar antes de
   que bootstrap tuviera oportunidad de resolver el vault.
2. Una memoria interna específica de Symphony está marcada
   `load_policy: always` y contiene una credencial en texto plano. No copiarla
   ni reproducirla. Retirarla del vault y rotarla antes de cualquier benchmark.
3. El instalador genera rutas absolutas en reglas project-scoped. Una mudanza del
   vault o cambio de usuario deja las reglas inválidas.

### P1 — Arranque y retrieval

1. `80-agents/agents-os/agents-os.md` define un contrato de inicio y enseguida
   repite otro flujo con distinto orden.
2. `agents-os-bootstrap/SKILL.md` vuelve a implementar el startup y
   `agents-os-context-retrieval/SKILL.md` vuelve a priorizar material que ya
   debía estar cargado.
3. La guía y bootstrap dicen “cargar memoria interna compacta bajo
   `80-agents/memory/internal/`”, pero no definen selector, scope, límite,
   prioridad ni resolución de múltiples notas `always`.
4. El perfil está hardcodeado como `rjara-agent-profile.md` en guía,
   constitución y bootstrap, pero `agents-os-install` puede resolver o crear
   `user-profile.md`. Una instalación portable puede crear un perfil que el
   runtime no encuentre.
5. El Context Router prohíbe saltar capas, mientras su tabla comienza las
   consultas de relación/código en Layer 2 y las síntesis en Layer 1.
6. Bootstrap exige emitir una nota de orientación visible aunque la preferencia
   del usuario pide evitar updates intermedios y el dato no agrega valor en el
   caso exitoso.
7. El routing de skills está duplicado y no coincide: la guía lista skills que
   no aparecen en el catálogo del bootstrap.
8. Los `SKILL.md` mezclan el contrato ejecutable con `Finish Tasks` y
   `Progress Log`; como el agente debe leerlos completos, paga contexto por
   historial de desarrollo.

### P1 — Cierre

1. `agents-os-session-close` está marcado `load_policy: always` y
   `agent/alwaysload`, pese a que la constitución y la propia skill exigen un
   pedido explícito.
2. La salida fija del cierre enumera doce categorías de artefactos, aunque el
   usuario no quiere conocer cuáles memorias se guardaron.
3. El L0 placeholder se crea siempre, incluso cuando no hay transcript
   disponible ni intención de pegarlo.
4. El mandamiento “toda sesión toca memoria interna” fuerza escrituras sin
   probar que exista un delta durable.
5. El feedback general es obligatorio en cierre normal y, dado que Graphify es
   retrieval primario, la mayoría de los cierres puede generar también un
   feedback específico de Graphify.
6. El cierre táctico dice que el feedback es solo por fricción, mientras
   constitución y `agents-os-session-feedback` lo hacen obligatorio salvo
   cierre mínimo.

### P1 — Consistencia documental e índice

1. La constitución live está correctamente en
   `80-agents/agents-os/agent-constitution.md`, y guía/bootstrap live apuntan a
   esa ruta.
2. `10-projects/AGENTS OS/chatgpt-pack/PROJECT-STATE.md` conserva una referencia
   antigua a `sources/80-agents/memory/public/constitution/agent-constitution.md`.
3. El proyecto [[AGENTS OS]] mantiene `agents-os-session-close` como pendiente
   aunque la skill existe, se usa y tiene forward-tests parciales.
4. El mismo proyecto conserva el objetivo histórico de contexto inicial cercano
   a 3.000 tokens junto con reglas posteriores de techo blando por suficiencia.
5. El proyecto afirma que todas las skills usan Graphify, lo que no describe la
   arquitectura híbrida vigente.
6. `agents-os-skill-authoring/SKILL.md` contiene rutas relativas incorrectas
   hacia `_shared/`; desde su carpeta deberían subir a `../_shared/`.
7. `.graphifyignore` excluye `95-graphify/` y `graphify-out/`, pero no
   `outputs/agents-os-chatgpt/`; el índice observó esas copias.
8. El proyecto controlador referencia material histórico bajo
   `80-agents/agents-os/_drafts/` que ya no forma parte de la estructura live.
9. El wrapper `/usr/local/bin/graphify-obsidian` intenta escribir su query log
   bajo `~/.config/graphify-obsidian/query-log.jsonl`; en superficies
   sandboxed genera `Operation not permitted`, aunque `explain/query` continúa.

## 🧭 Arquitectura objetivo

### Matriz de autoridad

| Fuente | Responsabilidad única | No debe contener |
|---|---|---|
| `AGENTS.md` | Hook mínimo para arrancar AGENTS OS | Constitución duplicada, listas de skills, procedimiento completo |
| `agents-os-bootstrap/SKILL.md` | Única máquina de estados de startup | Historia de desarrollo, rationale extenso |
| `agents-os.md` | Mapa conceptual y routing hacia fuentes canónicas | Receta de startup, receta de retrieval o cierre duplicadas |
| `agent-constitution.md` | Invariantes duras y breves | Procedimientos, ejemplos extensos, bitácora |
| Perfil resuelto | Preferencias globales y módulos por scope | Reglas de dominio irrelevantes al inicio |
| Skills | Trigger + procedimiento + output + hard rules | `Finish Tasks`, `Progress Log`, rationale humano |
| `_shared/` | Schemas y semántica común | Flujos completos de una skill |
| Proyecto [[AGENTS OS]] | Estado, roadmap, decisiones de producto | Reglas ejecutables |
| Journal/snapshots | Auditoría e historia | Autoridad vigente o corpus normal |

### Bootstrap único e incremental

1. **Clasificar el turno:** cold start, warm turn, cambio de entidad o
   invalidación de reglas.
2. **Cold start:** cargar una cápsula corta de invariantes y preferencias
   globales.
3. **Resolver objetivo, entidad e intención antes de memoria de dominio.**
4. **Memoria interna:** cargar únicamente
   `type: agent_memory + load_policy: always + scope: global`.
5. **Context Router:** partir en la capa más barata relevante para la intención;
   nunca abrir cuerpos sin selección previa; escalar por insuficiencia.
6. **Verificación:** abrir solo las fuentes Markdown que puedan cambiar la
   respuesta o una escritura persistente.
7. **Skill específica:** cargar una sola skill principal y dependencias
   estrictamente necesarias.
8. **Salida:** no mostrar orientation/context-pack cuando todo funciona; reportar
   solo degradación, gaps o supuestos que afecten al usuario.
9. **Warm turn:** reutilizar base y contexto de entidad; recuperar únicamente el
   delta del nuevo prompt.
10. **Cambio de entidad:** conservar invariantes y reemplazar solo el pack de
    entidad.

### Memoria interna enrutable

- Mantener una única nota global always-load de 200–500 tokens como señal de
  startup.
- Mover memorias de proyecto/app a `when_project_loaded`,
  `when_application_loaded` u otra política concreta ya soportada por el schema.
- Prohibir `always` en memoria de dominio.
- Reemplazar “toda sesión escribe” por “toda sesión con delta durable deja
  continuidad”.
- No crear otra fuente de verdad: el índice interno es un pointer compacto a
  memorias scoped.

### Cierre silencioso por delta

| Delta observado | Persistencia |
|---|---|
| Ningún conocimiento ni estado nuevo | Ningún artefacto |
| Solo continuidad operacional | Actualizar proyecto/control **o** checkpoint interno |
| Conocimiento reusable | L3 + log + reindex dirigido |
| Transcript disponible o solicitado | L0; L1 solo si agrega navegación |
| Fricción real del sistema | Feedback compacto |
| Auditoría solicitada | Inventario completo visible |

Reporte predeterminado:

```text
Sesión cerrada. Continuidad lista. Próximo paso: <acción>.
```

No listar memorias creadas, actualizadas, descartadas o duplicadas. Mostrar
detalle solo con `cierre con detalle`, ante conflicto que requiera decisión o
si el pipeline falló.

### Feedback event-driven

- Crear feedback solo ante fricción, retrieval degradado, gap o pedido
  explícito.
- Agregar telemetría de Graphify en higiene periódica en vez de una nota por
  sesión.
- Conservar muestreo opcional para medir salud sin producir dos plantillas
  completas en cada cierre.

## 📦 Archivos candidatos

### Runtime y autoridad

- `AGENTS.md`
- `80-agents/agents-os/agents-os.md`
- `80-agents/agents-os/agent-constitution.md`
- `80-agents/agents-os/context-router.md`
- `80-agents/memory/public/user-preference/rjara-agent-profile.md`
- `80-agents/skills/agents-os-bootstrap/SKILL.md`
- `80-agents/skills/agents-os-context-retrieval/SKILL.md`
- `80-agents/skills/agents-os-session-close/SKILL.md`
- `80-agents/skills/agents-os-session-feedback/SKILL.md`
- `80-agents/skills/_shared/metadata-schema.md`
- `80-agents/skills/_shared/note-types.md`
- `80-agents/skills/_shared/skill-contract.md`

### Instalación, validación e índice

- `80-agents/skills/agents-os-install/SKILL.md`
- `80-agents/skills/agents-os-install/scripts/configure-agent-surfaces.py`
- `80-agents/skills/agents-os-hygiene-review/SKILL.md`
- `80-agents/skills/agents-os-skill-authoring/SKILL.md`
- `.graphifyignore`

### Estado y derivados

- `10-projects/AGENTS OS/AGENTS OS.md`
- `10-projects/AGENTS OS/agentes/AGENTS OS - Beta y Hardening.md`
- `10-projects/AGENTS OS/chatgpt-pack/PROJECT-STATE.md`
- builder/manifiesto de `outputs/agents-os-chatgpt/`

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> **Fase 0 — Seguridad y reparaciones mecánicas**
> - [x] Retirar del vault la credencial detectada sin copiarla a logs #owner/agent #type/admin #area/personal #urgent ✅ 2026-07-27
> - [x] Corregir rutas project-scoped para resolver desde `VAULT_ROOT`, sin paths absolutos #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Corregir referencias relativas rotas de `agents-os-skill-authoring` #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Excluir `outputs/agents-os-chatgpt/` y `.obsidian/` del corpus Graphify #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [ ] Hacer portable/escribible el query log del wrapper Graphify en superficies sandboxed #owner/agent #type/dev #area/personal
>
> **Fase 1 — Autoridad y adelgazamiento**
> - [x] Congelar la matriz de autoridad y declarar una sola fuente por procedimiento #owner/agent #type/research #area/personal ✅ 2026-07-27
> - [x] Adelgazar `agents-os.md` a mapa conceptual y punteros #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Adelgazar la constitución a invariantes runtime #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Mover `Finish Tasks` y `Progress Log` fuera de todas las skills runtime; conservar sólo gates de ejecución reales #owner/agent #type/dev #area/personal ✅ 2026-08-01
> - [ ] Implementar resolución canónica portable del perfil always-load #owner/agent #type/dev #area/personal
> - [x] Consolidar el registry de skills/triggers sin duplicar listas #owner/agent #type/dev #area/personal ✅ 2026-07-27
>
> **Fase 2 — Hot Path de contexto**
> - [x] Reescribir bootstrap como máquina cold/warm/entity-switch/invalidation #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Corregir el Router a “capa más barata aplicable” y eliminar la contradicción de no-skip #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Crear/compactar un único índice interno global always-load y enrutar el resto por scope #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Eliminar orientation/context-pack visible en el camino exitoso #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Validar fallback Graphify sin relecturas amplias #owner/agent #type/dev #area/personal ✅ 2026-07-27
>
> **Fase 3 — Cierre silencioso**
> - [x] Remover `session-close` del set always-load y dejarla trigger-only #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Implementar clasificador de delta para decidir persistencia mínima #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Hacer L0 condicionado a transcript disponible/solicitado #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Cambiar el reporte default a resultado + próximo paso, sin inventario de memorias #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Hacer feedback general y Graphify event-driven/agrupado #owner/agent #type/dev #area/personal ✅ 2026-07-25
> - [x] Reconciliar el mandamiento de huella interna con persistencia basada en delta durable #owner/agent #type/research #area/personal ✅ 2026-07-27
>
> **Fase 4 — Doctor y consistencia**
> - [x] Implementar lint ejecutable de paths físicos, always-load, secrets, índice y proyectos #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Implementar medición estimada del startup base #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Eliminar procedimientos duplicados del hot path core #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Detectar/excluir snapshots, outputs y runtime Obsidian del corpus Graphify #owner/agent #type/dev #area/personal ✅ 2026-07-27
> - [x] Reconciliar proyecto controlador y proyecto duplicado con estado live #owner/agent #type/dev #area/personal ✅ 2026-07-27
>
> **Fase 5 — Benchmark y gates**
> - [x] Medir baseline pre-iteración y cold base post-iteración #owner/agent #type/research #area/personal ✅ 2026-07-27
> - [ ] Probar cold start en fact, relation, synthesis y code #owner/agent #type/research #area/personal
> - [ ] Probar warm turn y cambio de entidad con agente fresco #owner/agent #type/research #area/personal
> - [ ] Probar Graphify disponible, stale y degradado #owner/agent #type/research #area/personal
> - [ ] Probar cierre sin delta, continuidad, L3, transcript y auditoría #owner/agent #type/research #area/personal
> - [ ] Comparar contra baseline y entregar decisión go/no-go #owner/agent #type/research #area/personal

## ✅ Criterios de aceptación

- Una sola receta ejecutable de startup.
- Ninguna ruta project-scoped depende del nombre del usuario o ubicación
  absoluta del vault.
- Exactamente una memoria interna global `always`; ninguna memoria de dominio
  `always`.
- `session-close` no entra al startup y solo se carga tras trigger explícito.
- El cierre exitoso default tiene máximo tres líneas y no enumera memorias.
- Ningún L0 vacío se crea sin transcript disponible/solicitado.
- Feedback solo aparece por evento o muestreo definido.
- Cero copias de `outputs/` en el grafo live.
- Cero referencias físicas rotas en el core.
- El proyecto controlador y snapshots declaran su autoridad y frescura.
- Cold start objetivo de **3–5 mil tokens** y warm turn de **menos de mil tokens
  nuevos**, usados como benchmark blando. La suficiencia manda sobre el número.
- La reducción de tokens no empeora recuperación útil, confianza ni tasa de
  éxito frente al baseline.

## 🧪 Matriz mínima de pruebas

| Caso | Esperado |
|---|---|
| Cold fact | Base mínima + entidad + una fuente verificada |
| Cold relation | Grafo primero cuando sea la capa más barata aplicable |
| Domain synthesis | Índice curado + top-N fuentes; sin lectura amplia |
| Code question | Grafo de código + símbolos puntuales |
| Warm same entity | Solo delta; no releer constitución/guía |
| Entity switch | Mantener base y reemplazar pack scoped |
| Graphify stale | Reindex una vez y continuar |
| Graphify unavailable | Fallback enfocado con degradación explícita |
| Close no delta | Sin artefactos; reporte breve |
| Close continuity | Un único checkpoint durable |
| Close reusable | L3/log/reindex sin inventario visible |
| Close audit | Inventario completo solo por solicitud |

## ⚠️ Riesgos y mitigaciones

- **Sobrecompactación:** un cap rígido puede cortar la línea importante.
  Mitigación: presupuestos blandos y escalado por miss.
- **Nuevo documento paralelo:** un manifest manual podría transformarse en otra
  fuente de verdad. Mitigación: que sea generado o solo pointer.
- **Pérdida de continuidad:** eliminar escrituras obligatorias puede ocultar
  estado. Mitigación: persistir ante delta material y medir reexplicación.
- **Drift por generación:** `AGENTS.md` y packs pueden quedar obsoletos.
  Mitigación: `doctor` compara derivados contra fuentes y falla la validación.
- **Reescritura demasiado amplia:** cambios simultáneos a archivos de alta
  autoridad son difíciles de auditar. Mitigación: PRs/parches por fase, logs y
  rollback explícito.
- **Benchmark sesgado:** agentes familiarizados con el sistema pueden rendir
  mejor. Mitigación: usar agentes frescos y control sin AGENTS OS.

## 🚫 Fuera de alcance

- Crear otro índice paralelo a Markdown/Graphify.
- Aplicar límites duros de tokens.
- Reescribir masivamente memoria histórica sin juicio por nota.
- Exponer memoria interna o detalles de artefactos de cierre al usuario.
- Resolver en esta iteración todos los objetivos de adopción multisuperficie de
  [[AGENTS OS - Beta y Hardening]].

## 📆 Bitácora

- **2026-08-01 (cierre)** — Proyecto archivado tras crear
  [[AGENTS OS - Fase 2]]. Sus pendientes E2E y de consistencia quedaron
  migrados al nuevo planificador; no debe usarse como autoridad vigente.
- **2026-08-01** — Se revisaron las 22 skills que contenían `Finish Tasks` o
  `Progress Log`. La historia duplicada fue retirada porque las reglas durables
  ya vivían en los procedimientos, contratos compartidos o proyectos. El
  checklist de `sqx-temporal-failure-audit` se conservó como
  `Evidence Completion Gate` porque sí gobierna cada ejecución.
- **2026-07-27** — Validación post-implementación: se corrigió el root físico
  de `AGENTS.md`; closed club `always` quedó en exactamente cinco archivos;
  el cold base bajó a ~4,9k tokens estimados; `.obsidian/` y `outputs/` quedaron
  fuera de Graphify; cierre y feedback quedaron realmente silenciosos por
  delta; preferencias Meli/Aranea salieron del perfil global; se implementó
  `agents-os-doctor/scripts/doctor.py`. Se fusionó el proyecto duplicado y el
  puente humano pasó a Review. Queda pendiente la corrida E2E con agente fresco.
- **2026-07-27 (portabilidad)** — Corrección posterior del diseño de paths:
  el hook, instalador, doctor, scripts de tagging, runbooks y wrapper Graphify
  dejaron de persistir rutas absolutas. Todo el core resuelve desde
  `VAULT_ROOT`, `cwd`, ubicación del wrapper o `AGENTS_OS_VAULT`.
- **2026-07-25** — Proyecto creado desde `70-templates/project.md` a petición
  explícita de Rodrigo. Consolidó la auditoría de arranque, cierre, economía de
  tokens, consistencia documental, Graphify y seguridad. No se aplicaron todavía
  cambios al runtime; todas las tareas quedan en To Do para ejecución
  verificable por fases.

## 🧭 Decisiones

- Esta iteración se modela como proyecto de agente hijo de [[AGENTS OS]], no
  como memoria ni como expansión de [[AGENTS OS - Beta y Hardening]].
- La nota del proyecto es el planificador único y conserva todo el contexto
  necesario para que un agente fresco continúe sin releer esta conversación.
- El diseño recomendado es **hot path incremental + cierre silencioso por
  delta + doctor de consistencia**.
- Los objetivos numéricos son benchmarks blandos; nunca justifican perder
  contexto relevante.
- El reporte de cierre y la persistencia interna son contratos separados.

## 🔗 Docs / Links

- [[AGENTS OS]] — proyecto padre.
- [[AGENTS OS - Beta y Hardening]] — beta y adopción; scope relacionado pero
  distinto.
- [[agents-os]] — guía operativa vigente.
- [[context-router]] — concepto de retrieval por capas.
- [[token-economy-indexing-architecture]] — arquitectura de economía de tokens.
- [[project-ownership-human-vs-agent]] — contrato de proyecto de agente y tarea
  puente.
- `80-agents/skills/agents-os-bootstrap/SKILL.md`
- `80-agents/skills/agents-os-context-retrieval/SKILL.md`
- `80-agents/skills/agents-os-session-close/SKILL.md`
- `80-agents/skills/agents-os-hygiene-review/SKILL.md`
- `80-agents/skills/agents-os-agent-project-workflow/SKILL.md`

## 💡 Ideas

### Backlog de ideas

- Generar un pequeño `runtime digest` desde fuentes marcadas, en vez de
  mantenerlo manualmente.
- Registrar hashes/mtime de fuentes base para invalidación warm.
- Exponer una operación única `context-pack` por intención sobre el contrato
  existente de Graphify, sin convertirla en otra fuente de verdad.

### Motivos / principios

- Una fuente canónica por hecho.
- Runtime agent-facing corto; rationale humano separado.
- Suficiencia primero, cheapest applicable layer, verificación quirúrgica.
- Persistir solo lo que cambia una decisión o permite continuidad real.

### Memoria pública / interna

- **Memoria pública:** no crear L3 por esta propuesta; las reglas cambian solo
  cuando una fase sea aprobada e implementada.
- **Memoria interna:** un pointer compacto a este proyecto basta para
  continuidad.
- **Motivo:** el diagnóstico y plan son estado de proyecto Sistema 2; duplicarlos
  como memoria inflaría retrieval.
