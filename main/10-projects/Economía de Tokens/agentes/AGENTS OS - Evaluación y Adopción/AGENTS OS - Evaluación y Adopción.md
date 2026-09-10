---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P2
area: "[[Personal]]"
parent: "[[Economía de Tokens]]"
sprint:
start: 2026-07-10
due:
progress: 100
repo:
jira:
prs:
aliases:
  - AGENTS OS Evaluación y Adopción
  - AGENTS OS team adoption review
tags:
  - kind/project
  - area/personal
  - project/agents-os
  - project/economia-de-tokens
created: 2026-07-10
updated: 2026-09-09
---

# AGENTS OS - Evaluación y Adopción

%% Naming: AGENTS OS - Evaluación y Adopción es el link canónico; aliases guarda variantes humanas. %%

> [!info]+ AGENTS OS - Evaluación y Adopción
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P2 · **Padre:** [[Economía de Tokens]]
> Subproyecto de agente para convertir la arquitectura y la evidencia de AGENTS OS en material profesional de evaluación y adopción para un equipo técnico.

## 🎯 Objetivo

- Explicar en una sola visualización la promesa completa de AGENTS OS: gobernanza, routing de contexto, memoria, aprendizaje, conocimiento real y bucles de mejora.
- Presentar a continuación una evaluación crítica y basada en evidencia: ventajas, desventajas, casos de uso, gaps, riesgos y recomendaciones.
- Mantener el entregable en local y listo para revisión humana antes de cualquier publicación.

## 📊 Estado actual

- **Review:** versión 4 publicada y verificada en Grid remoto privado, reconciliada con el estado real del 2026-09-09.
- El entregable dejó de ser una evaluación con score y pasó a ser un contraste **promesa vs. evidencia**: siete promesas con veredicto cumplida/parcial/no cumplida, cada una con su evidencia y su salvedad. No hay cifra estimada; todo sale del agregado de 340 feedbacks de sesión (2026-07-05 → 2026-09-09) o de un gate ejecutable.
- Veredicto vigente: **el arranque y la memoria cumplen; el bucle de mejora y la delegación a subagentes no.** Sigue siendo piloto controlado.
- El generador es autocontenido: `build-grid.py` renderiza desde `agents-os-grid.source.json` sin depender de ningún generador externo. Los datos viajan embebidos como JSON y el layout se construye desde ahí, así que reordenar el reporte no puede cambiar un número.
- Verificación remota: el payload JSON descargado desde Grid es idéntico al local; la diferencia de bytes es sólo la inyección estándar del runtime de Grid.
- **El documento está compartido con una persona además del owner.** Cualquier publicación cambia lo que esa persona ve.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Ver [[convenciones]]. %%
> - [x] Consolidar evaluación completa y profesional de AGENTS OS #owner/agent #type/research #area/personal
> - [x] Incorporar casos de uso concretos y límites de uso #owner/agent #type/research #area/personal
> - [x] Diseñar el mapa de componentes y relaciones de AGENTS OS #owner/agent #type/dev #area/personal
> - [x] Integrar la arquitectura como portada del Grid local #owner/agent #type/dev #area/personal
> - [x] Incorporar LLM Wiki como capa de conocimiento canónico y declarar su cobertura parcial #owner/agent #type/research #area/personal
> - [x] Ajustar portada y firma final para publicación Baticoders · vis-nexus #owner/agent #type/dev #area/personal
> - [x] Verificar visualmente el Grid y el diagrama en local #owner/agent #type/dev #area/personal
> - [x] Publicar evaluación en Grid de Meli #owner/agent #type/admin #area/personal — doc_id `01KXGAY6QKSZWEBR5SCY5JSWCE`, versión 1, privado.
> - [x] Revisar, corregir, verificar y publicar la versión 2 con el estado real del 2026-07-14 #owner/agent #type/research #area/personal — Grid v2 verificado.
> - [x] Rehacer el entregable como contraste promesa vs. evidencia y publicar la versión 4 #owner/agent #type/research #area/personal — Grid v4 verificado contra el payload local.
> - [x] Reemplazar el builder por uno autocontenido, sin generador externo #owner/agent #type/dev #area/personal

## 📆 Bitácora

- **2026-09-09** — Versión 4 publicada y verificada. El entregable se rehízo como contraste promesa vs. evidencia con el agregado de 340 feedbacks del período; el score global y el conteo de skills de julio salieron porque ya no representaban nada verificable. El builder anterior dependía de un generador externo que no existe en el vault, así que era irreproducible: se reemplazó por uno autocontenido con los datos embebidos como JSON. Los dos artefactos generados de julio se eliminaron.
- **2026-07-14** — Versión 2 publicada y verificada en Grid: score 7,0,
  scaffolding/onboarding/higiene/skills canónicas incorporados, evidencia
  Graphify actualizada y cifra histórica no vigente retirada. Se descartó el
  botón ZIP por decisión del owner; el paquete se compartirá aparte por Slack.
- **2026-07-14** — El owner pidió revisar el Grid con el contexto posterior al
  scaffolding de equipo. Se reabre la revisión local: la versión remota sigue
  siendo v1 hasta que la versión 2 sea revisada y publicada explícitamente.
- **2026-07-10** — Proyecto creado como hijo de [[Economía de Tokens]]. Se migraron el Grid y su fuente desde `outputs/` para que el entregable tenga ownership, continuidad y trazabilidad.
- **2026-07-10** — Se agregó la portada arquitectónica “promesa del sistema” y se mantuvo el reporte crítico como segundo acto. Artefactos listos para revisión humana.
- **2026-07-10** — Ajuste tras revisión del owner: LLM Wiki pasa a ser explícita en Sistema 2 y en la Capa 1 del Context Router. Se declara como implementada parcialmente, no como capacidad homogénea del vault.
- **2026-07-10** — Ajuste prepublicación: retirada la pill visual de cobertura parcial y firma final reemplazada por `Baticoders · vis-nexus`.
- **2026-07-10** — Publicación iniciada. Grid redirigió a Google/IAP y requiere login del owner; pestaña dejada visible para continuar sin rehacer el flujo.
- **2026-07-14** — Publicación completada en Grid remoto privado: [AGENTS OS — evaluación crítica para adopción en equipo](https://grid.adminml.com/d/01KXGAY6QKSZWEBR5SCY5JSWCE/view), versión 1. El contenido descargado coincide con el HTML local salvo la inyección estándar del runtime seguro de Grid.

## 🧭 Decisiones

- El entregable contrasta promesa contra evidencia, no asigna un score global: un número agregado ocultaba que dos promesas están cumplidas y dos no lo están.
- Ninguna cifra del reporte es estimada. Si algo no se puede medir con el corpus, el reporte dice que no se puede medir.
- El builder no depende de un generador externo. Un entregable que no se puede regenerar en la máquina donde vive no es reproducible.
- Vivir bajo [[Economía de Tokens]] porque el Context Router y la recuperación progresiva nacen de esa iniciativa, y el destino declarado es evangelización técnica.
- Separar narrativa en dos actos: **promesa/venta** primero; **estado real, evidencia y gaps** después.
- Usar SVG vectorial editable para que componentes, relaciones y wording puedan iterarse sin regenerar una imagen raster.
- Representar Graphify como **índice derivado**, nunca como fuente de verdad.
- Publicar solo tras revisión explícita del owner; la condición se cumplió y la versión 1 quedó publicada de forma privada en Grid de Meli.

## 🔗 Docs / Links

- [[Economía de Tokens]] — iniciativa padre y tarea puente humana.
- [[AGENTS OS]] — proyecto/sistema evaluado.
- [[context-router]] — protocolo de recuperación por capas.
- [[token-economy-indexing-architecture]] — arquitectura de indexación.
- [Grid local](agents-os-grid.html) — vista generada, autocontenida.
- [Fuente del Grid](agents-os-grid.source.json) — única fuente de los datos del reporte.
- [Builder](build-grid.py) — `python3 build-grid.py`, sin dependencias externas.
- [Diagrama editable](assets/agents-os-componentes.svg) — portada arquitectónica de julio; no se embebe en la versión 4.
- [Grid remoto privado](https://grid.adminml.com/d/01KXGAY6QKSZWEBR5SCY5JSWCE/view) — versión 4.

## 💡 Ideas

### Backlog de ideas

- Convertir la visual en una versión “actual vs target” si el equipo necesita discutir roadmap por componente.
- Añadir métricas de una beta controlada cuando exista evidencia comparativa.

### Motivos / principios

- Vender la tesis sin esconder la deuda: la arquitectura puede ser buena y la madurez de adopción todavía insuficiente.
- Una fuente canónica por hecho; los índices y visualizaciones son proyecciones derivadas.

### Memoria pública / interna

- **Memoria pública:** decisiones, known errors, runbooks y learnings reutilizables que explican la evaluación.
- **Memoria interna:** continuidad operativa del agente durante la preparación e iteración del material.
- **Motivo:** distinguir conocimiento compartible de contexto de ejecución privado evita mezclar evidencia con seguimiento de sesión.
