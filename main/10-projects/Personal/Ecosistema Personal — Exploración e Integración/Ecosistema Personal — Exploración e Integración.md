---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Personal]]"
parent:
sprint:
start: 2026-09-20
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Mejora de sistemas
  - Mejora Aranea
  - Exploración de nuevas ideas
  - Radar de herramientas
  - Ecosystem Improvement
  - Tech Adoption Radar
tags:
  - kind/project
  - area/personal
created: "2026-09-20"
updated: "2026-09-20"
---

# Ecosistema Personal — Exploración e Integración

> [!info]+ Cockpit humano · investigación transversal
> **Área:** [[Personal]] · **Owner:** me · **Estado:** active · **Prioridad:** P2 · **Progreso:** 0% de evaluaciones ejecutadas. Recoge mejoras aplicables a Aranea, agentes, proyectos y vida cotidiana; no es un mandato de instalar todo. **Candidato ≠ decisión de adopción.**

## 🎯 Objetivo

Mantener un radar accionable de proyectos, herramientas, patrones y oportunidades externas para mejorar el ecosistema personal: homelab [[Aranea]], [[AGENTS OS]], Agents Hub, Hermes/Ariadna, [[Echo]], [[Echo Forge]], [[Polymarket Engine]], [[Multimodal Knowledge Engine]], [[Loom]], Backup/DR, Argus, productividad, investigación y creación de contenido. Poder dejar una idea en espera y retomarla semanas después con cualquier agente sin depender del historial del chat.

**Resultado buscado:** experimentos pequeños, métricas comparables y decisiones explícitas `ADOPT / ADAPT / PARK / REJECT` por candidato y por sistema; implementación solamente en los proyectos propietarios con sus propias SPECs y autorizaciones. Identificar también qué no vale la pena integrar, conservando el porqué y la condición de reapertura.

## 📊 Estado actual

- **2026-09-20:** iniciativa y backlog creados a partir de la investigación GitHub Trending diaria/semanal/mensual y de todos los repositorios discutidos en la conversación. El ranking diario se contrastó directamente; semanal/mensual por recopilatorios externos, por lo que la presencia exacta o posición en esos períodos NO debe tratarse como dato oficial ni duradero.
- **Ejecución:** 0 pruebas de adopción; ningún paquete instalado; ningún ambiente, permiso, memoria ni repositorio de productos modificado por este proyecto. Las prioridades son propuestas de evaluación, no autorizaciones operativas.
- **Catálogo completo y candidatos aplazados/rechazados provisionalmente:** [[Radar de Herramientas — 2026-09-20]]. **Retoma en sesión limpia:** [[Ecosistema Personal — Continuidad]]. Esta nota es la única fuente de planificación y estado; el catálogo conserva el detalle de cada candidato y la continuidad indica cómo reabrirla.
- **Verificación pendiente del entorno:** creación vía GitHub API, sin checkout local ni ejecución de `materialize_schema_note.py`, lint, Graphify o revisión de índice. No declarar `SCHEMA_PASS`, `INDEX_FRESH` ni `WORKTREE_CLEAN` hasta ejecutar sus verificadores sobre `origin/master`. La desviación está registrada en feedback.

## 🧭 Alcance, fuentes y límites

- **Sí:** descubrir/revaluar repositorios; verificar README, licencia, mantenimiento, interfaces, seguridad, costos, requisitos y duplicidad; diseñar POC read-only; medir resultados; documentar ADOPT/ADAPT/PARK/REJECT, owner, rollback y enlaces a evidencia; proponer tareas en proyectos existentes bajo sus procedimientos.
- **No:** forks o clones completos dentro del vault, instalación masiva de skills/MCP, acceso nuevo a secretos, comandos `curl | sh` sin revisión, hooks globales no aprobados, despliegues a producción, migración de MinIO/Ceph, trading real ni creación de múltiples fuentes de verdad.
- **Confidencialidad:** MELI/RIO/Project Lens permanece en herramientas corporativas autorizadas. No indexar código, documentos ni datos internos en servicios externos o instancias personales sin autorización; reutilizar ideas genéricas de UX sin copiar datos empresariales.
- **Aranea:** política cero servicios publicados; acceso privado. Cualquier experimento con permisos o navegador autenticado usa identidad y máquina aisladas y principio de mínimo privilegio. Ceph/Backup-DR conservan sus gates reales; esta iniciativa no los redefine ni los cierra.
- **Trading:** Polymarket investigación read-only sin credenciales de negociación, órdenes ni capital real; Echo/Forge no pasan a PROD por adopción de una herramienta. Forecasting no equivale a edge probado; validar licencia de pesos de modelos.
- **Agents-OS:** Markdown canónico; motores de memoria, embeddings, grafos y resúmenes son derivados. Un candidato externo jamás decide estado, SPEC, gate o cierre de proyecto. Referenciar los estados actuales de sus respectivas notas, no copiar snapshots aquí.
- **Fuente técnica:** repo y README oficiales enlazados por candidato; benchmark del autor = claim por reproducir, no PASS. GitHub Trending es una fuente efímera de descubrimiento, no un gate de arquitectura.

## 🧱 Entrega de desarrollo

_No aplica en esta etapa: proyecto de exploración/portafolio, no implementa código ni infraestructura. Antes de cada experimento que cambie código, configuración ejecutable, esquema o infraestructura, crear o enlazar un subproyecto `owner: agent` bajo su proyecto responsable con repo, branch, base SHA, SPEC funcional y técnica, gates, rollback y tarea puente humana. No inventar HEAD ni estados de otros repos._

## 🧩 Subproyectos

Todavía ninguno. Crear uno solamente al aprobar un experimento que requiera varias tareas o un delivery técnico. Este cockpit conserva una sola tarea puente por subproyecto, que un agente puede llevar como máximo a `[r]`; el owner acepta y cierra.

## ✅ Tareas

### M0 — Preparar el radar y fijar controles
- [x] Definir iniciativa transversal, fuentes, candidatos directos, inspiración, alternativas aplazadas y descartes provisionales #owner/me #type/research #area/personal
- [ ] Ejecutar materializador/validador del proyecto, `scripts/lint.py --strict` sobre notas nuevas, comprobación de Graphify y `git status` desde un checkout autorizado; registrar evidencia real #owner/agent #type/admin #area/personal #blocked
- [ ] Revisar el catálogo completo y seleccionar **una sola POC por categoría**; no abrir iniciativas por cada repositorio #owner/me #type/research #area/personal

### M1 — POC de valor inmediato, aisladas y reversibles
- [ ] Auditoría read-only de un repo autorizado usando Cloudflare Security Audit; registrar superficies, hallazgos confirmados/pendientes/rechazados y evidencia #owner/me #type/research #area/personal
- [ ] Comparar Alibaba Open Code Review vs reviewer actual en un PR autorizado de Echo Forge o Polymarket; medir errores reales, falsos positivos, costo y cobertura #owner/me #type/research #area/personal
- [ ] Probar Worktrunk en sandbox: cuatro worktrees y agentes sin colisiones, sin merges/push autónomos #owner/me #type/research #area/personal
- [ ] Benchmark de memoria: Agents-OS retrieval actual vs **un solo candidato** (Supermemory u OpenViking), corpus congelado y preguntas con decisiones contradictorias/obsoletas, trazabilidad y costo #owner/me #type/research #area/personal
- [ ] Medir llmfit en equipos de inferencia autorizados; fit, cuantización, latencia, RAM/VRAM, tokens/s y carga paralela #owner/me #type/research #area/personal

### M2 — Investigación aplicada sin romper roadmaps
- [ ] MKE: estudiar video-use (timeline/visual bajo demanda), MarkItDown (documentos) y Agent Reach (adquisición) como candidatos futuros; conservar M0 audiovisual y cobertura visual independiente #owner/me #type/research #area/personal
- [ ] Loom: evaluar UX read-only v0.4/vigente antes de plantear Human Action Center, Project Command Center y Resume Context; Archify/Diagram Design/Hister solo como referencias #owner/me #type/research #area/personal
- [ ] Hermes/Ariadna: contrastar continuidad, tools web y navegador autenticado en entorno separado sin ampliar credenciales operativas #owner/me #type/research #area/personal
- [ ] Aranea: evaluar Coder/RustFS/llmfit sin intervenir Ceph/MinIO/PBS vigentes; seguridad y DR mantienen sus proyectos autorizantes #owner/me #type/research #area/personal
- [ ] Vida y creatividad: probar, solo si surge necesidad real, Hister, Humanizer o No AI Slop (elegir uno), HyperFrames/OpenMAIC/VoiceStudio y God's Eye View bajo permisos y licencias verificados #owner/me #type/research #area/personal

### M3 — Decisiones y promoción
- [ ] Registrar para cada candidato seleccionado decisión ADOPT/ADAPT/PARK/REJECT, evidencia, costo, dueño, fecha de reevaluación condicionada y rollback; actualizar catálogo, NO duplicar en proyectos destinatarios #owner/me #type/research #area/personal
- [ ] Si ADOPT/ADAPT exige implementación, preparar subproyecto con SPECs, branch/base, permisos, gates y tarea puente en proyecto propietario antes de tocar código #owner/me #type/supervision #area/personal

## 🧪 Contrato de evaluación por candidato

1. **Problema existente:** evidencia concreta, sistema receptor y baseline actual; si no hay problema medible, `PARK`.
2. **Autoridades:** repo oficial, documentación, licencia, límites, mantenimiento, dependencia, versión/pin, TOS si usa terceros; claims no verificados quedan explícitos.
3. **Fronteras:** datos que salen, secretos, privilegios, hooks, red, escritura, CI, APIs no documentadas y compatibilidad MELI/proyectos. Fallo de seguridad/licencia ⇒ `NO_GO`.
4. **POC:** alcance mínimo, infraestructura aislada, permisos read-only por defecto, fixtures/corpus congelado, salida reproducible; no mutate PROD.
5. **Métricas:** precisión/cobertura/falsos positivos, tokens, costo, latencia, recursos, UX y esfuerzo de mantenimiento según la clase de herramienta. Comparar contra baseline, no contra marketing.
6. **Decisión:** `ADOPT` = usar con gates aprobados; `ADAPT` = incorporar patrón específico; `PARK` = posponer con trigger; `REJECT` = descartar por causa precisa, nunca borrarlo de la historia. Decisión del owner cuando impacta arquitectura/seguridad/costos.
7. **Promoción:** link hacia proyecto propietario, una sola fuente de verdad; rollback y verificación registrados antes de integrar.

## 📆 Bitácora

- **2026-09-20:** usuario solicita proyecto persistido, radar íntegro incluyendo descartes, actualización documental, feedback y cierre de sesión. Proyecto raíz humano creado; la verificación local de schema/lint/Graphify queda expresamente `NOT_RUN` por limitación de ejecución del checkout. Siguiente agente comienza por el gate M0 y la elección de UNA POC.

## 🧭 Decisiones

- Nombre canónico: **Ecosistema Personal — Exploración e Integración**; alias para mejora de sistemas/Aranea e ideas. Se conserva fuera de un solo proyecto de Aranea porque atraviesa vida personal, agentes y varios repositorios.
- Iniciativa `owner: me`, `root: true`; no tiene un agente autónomo que adopte herramientas por su cuenta. Futuros deliveries técnicos son subproyectos separados con autoridad propia.
- Estado inicial de los candidatos = **no adoptado**. «Desechado» en la conversación se representa `PARK`/`REJECT provisional` con razón y trigger de reapertura; no se pierde la idea ni se reinterpreta como rechazo definitivo del usuario.
- No crear una memoria adicional como fuente de verdad del portafolio: proyecto = estado, radar = ficha técnica, handoff = instrucción de recuperación.

## 🔗 Docs / Links

- [[Radar de Herramientas — 2026-09-20]] — inventario exhaustivo por sistema y por repositorio, candidatos descartados incluidos.
- [[Ecosistema Personal — Continuidad]] — punto de entrada de sesión nueva, limitaciones y mandato de siguiente agente.
- [[AGENTS OS]] · [[Loom]] · [[Multimodal Knowledge Engine]] · [[Polymarket Engine]] · [[Echo]] · [[Echo Forge]]; Aranea, Hermes, Agents Hub, Backup/DR y Argus: resolver sus títulos canónicos desde el índice antes de escribir allí.
- `xKoRx/agents-os`, branch `master`: guía `main/80-agents/agents-os/agents-os.md`, constitución, bootstrap y session-close son autoridades de operación.

## 💡 Ideas

- **Backlog:** dashboards de salud de agentes y proyectos, recuperación de contexto con procedencia, revisores independientes, workspaces aislados, archivo de investigación personal, generación audiovisual basada en conocimiento, medición local de modelos; todas las ideas tienen trazabilidad en el radar.
- **Principio:** integrar capacidades pequeñas y demostradas, no otro framework entero por popularidad.
- **Memoria pública:** proyecto/radar son fuentes compartidas; **memoria interna:** no requerida mientras el handoff canónico cubra continuidad.
