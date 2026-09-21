---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Loom]]"
  - "[[Loom — Continuidad y próximos pasos]]"
aliases: []
tags:
  - kind/doc
  - area/personal
created: "2026-09-20"
updated: "2026-09-21"
---

# Loom — Banco de ideas de producto

## Propósito

Preservar **íntegramente las ideas útiles** discutidas al pausar Loom, con estado real y dependencias, para no repetir discovery ni perderlas durante la pausa. Este documento es un **backlog de producto propuesto**, no una SPEC congelada, mandato ejecutable ni autorización para iniciar agentes. Proyecto canónico: [[Loom]]. Punto de reentrada y riesgos: [[Loom — Continuidad y próximos pasos]].

## Contenido

### Visión y experiencia diaria

- **Notion para presentación + Obsidian para conocimiento + Agents-OS para continuidad y supervisión**, sin intentar clonar sus plataformas.
- Al abrir Loom, responder en unos segundos: **¿qué necesita mi atención?, ¿en qué punto quedó cada proyecto?, ¿cómo retomo?**. Home es una superficie de foco, no un inventario del vault ni 20 widgets. Proyectos completos en `/projects`; evidencia y Markdown fuente siempre accesibles.
- Markdown de Agents-OS sigue como autoridad; vistas, índice, colecciones, grafo e indicadores son proyecciones derivadas. No duplicar tareas/documentos ni inventar estados, KPIs o actividad de procesos.

### Catálogo completo de las 13 propuestas originales (reconciliadas con v0.6 + F3)

| Idea original | Estado al pausar | Conservación / acción futura |
| --- | --- | --- |
| Human Action Center | **Implementada en v0.5** | Preservar la semántica: aprobaciones humanas solo desde tarea puente `#owner/me #type/supervision` en `[r]` y referencia verificable; review genérica de agente ≠ aprobación; no reconstruir. |
| Project Command Center | **Implementada en v0.5** | Mejorar solo con casos reales; estado/progreso/hito/bloqueo desde fuentes documentales, no señales de procesos ficticias. |
| Resume Context | **Implementada en v0.5** | Ampliar con última ejecución documentada (mandato, SHA, gates, evidencia, próximo paso y residuales), sin crear otro orquestador ni inventar agentes activos. |
| Portfolio Insights | **Pendiente; candidato v0.7** | Vista transversal por proyecto: foco, progreso documentado, blockers, puentes humanos pendientes, proyectos sin próximo paso; procedencia, denominador y sin puntuaciones arbitrarias. |
| Change Feed | **Pendiente; candidato v0.8** | Mostrar cambios con antes/después y fuente identificable; exige contrato de historial persistente, identidad y límites de cobertura. No inferir cambio semántico solo desde mtime. |
| Smart Collections | **MVP implementado v0.6** | Ya existen Architecture, Runbooks, Decisions y Project Knowledge; no rehacer. `Recently Updated` permanece diferido hasta tener timestamps con procedencia. Custom collections diferidas hasta demanda verificable. |
| Knowledge Explorer | **Pendiente; candidato v0.7** | Panel contextual nota↔proyecto: backlinks, relaciones, recursos, ADR/decisiones y documentación; reusar índice/grafo y filtros Smart Collections, preservar ambigüedad explícita. No otra Graphify/vector DB/LLM. |
| Weekly Review | **Pendiente; candidato v0.8 junto a Change Feed** | Resumen semanal documental de avances, bloqueos, decisiones y compromisos arrastrados; enlazar evidencia, aclarar huecos de historial, evitar fabricar actividades. |
| Saved Workspaces | **Diferido UX** | Layout/preferencias browser-local; sin escribir preferencias en el vault ni activar sincronización entre máquinas por defecto (F1 diferido). |
| Focus Reading | **Diferido UX** | Lectura sin sidebar/panel contextual, ancho de lectura, back/forward y persistencia local; cambio pequeño sin nueva arquitectura. |
| Decision Explorer | **Condicional** | Abrir solo si Knowledge Explorer + colección Decisions no resuelven usos reales; no duplicar otra vista por nombre. |
| Agent Run Explorer | **Pendiente, incremental** | Historial documental de mandatos, agentes, SHAs, gates, evidencias y revisiones. `[/]` en Markdown significa estado declarado, jamás prueba de proceso vivo. Primera sección puede nacer en Resume Context v0.7. |
| Safe Capture | **Fuera de F3 / diferido** | Capturar nuevas ideas/notas requiere nuevo contrato de escritura, allowlist, backups, concurrencia, auditoría, revisión y permiso específicos. F3 solo puede escribir planes diarios, no editor genérico. |

### Nueva idea (2026-09-21): Prompt Context Inspector — validación y contexto antes de ejecutar

**Pedido del owner:** desde Loom, ingresar un prompt, validarlo y obtener una vista previa del contexto que se cargaría en función de ese prompt, considerando **todas las herramientas e integraciones disponibles, incluida Graphify**. El objetivo es poder inspeccionar qué información recibiría efectivamente el agente, no solo ver una lista genérica de documentos.

**Experiencia deseada (propuesta, no SPEC):** mostrar el contexto ensamblado y su procedencia: documentos de Agents-OS, referencias de proyecto, memoria, resultados de búsqueda/grafo de Graphify y las demás herramientas habilitadas que correspondan. Distinguir herramientas **disponibles**, **seleccionadas/invocadas** y **no aplicables o no disponibles**, con razones cuando sea posible. Mostrar fuentes y fragmentos incorporados, orden de carga, estimación de tokens/presupuesto, duplicados, referencias rotas y truncamientos; reportar errores de validación y permisos sin inventar resultados.

**Condición de veracidad y seguridad:** una simulación o estimación de contexto debe identificarse como tal. Para afirmar «contexto realmente cargado», se necesita evidencia del ensamblador/runtime y trazas de las herramientas; no presentar una predicción como ejecución confirmada. Preferir inspección *dry-run* / solo lectura sin acciones con efectos secundarios. Reutilizar las integraciones e índices existentes, especialmente Graphify, sin crear otro motor de grafo, memoria u orquestador.

**Estado:** idea de producto capturada para discovery y priorización futura. No implica desarrollo, SPEC congelada, cambio de roadmap, inicio de agentes ni autorización de escritura o ejecución.

### Oportunidad distintiva: operaciones de agentes SIN un nuevo orquestador

Una bandeja **Needs your attention** debe llevar de entrega→puente humana→SPEC→evidencia→bitácora→decisión; separar **bloqueos documentados**, **reviews genéricas** y **aceptaciones de owner**. Retomar un proyecto debe enseñar último hito verificable, último `agent_run` documentado, última entrega SHA, gates y próxima acción; ausencia de datos ⇒ «no disponible». Beads/Gas Town/Superpowers son inspiración para vistas de dependencia/gates, no autorización para ejecutar agentes desde Loom ni para declarar actividad en vivo.

### Secuencia propuesta, supeditada a reanudación del owner

**Primero: F3 Product Integration RC (bloquea la expansión).** Baseline `feature/f3-idempotency-gate @ 04a3ae80b9eaacd4165e1989a21246c9bc2d8898` y referencia completa en [[Loom — Continuidad y próximos pasos]]. Integrar writer+ledger+watcher+API+Today en rama aparte, modo read-only default, certificación solo fixtures, HTTP Host/Origin/CSRF y modelo de amenazas StateDir. No G4 ni vault real sin nuevo permiso. Después hacer aceptación UX humana **read-only** antes de seguir.

**v0.7 propuesta — Knowledge & Portfolio:** Knowledge Explorer + Portfolio Insights + continuidad de la última ejecución en Resume Context. Criterios: navegar Home→proyecto→documento/evidencia en ≤2–3 interacciones habituales; resolver backlinks duplicados y referencias ambiguas sin inventar vínculos; métricas con población/fecha/denominador; pruebas de vacíos, stale y dark/light; datos procedentes del mismo snapshot. No implementar otra Home ni reescribir las cuatro Smart Collections.

**v0.8 propuesta — Temporal & Review:** Change Feed + Weekly Review unidos, solo después de congelar contrato para snapshots/eventos históricos (identidad, retención, timestamps, coverage, deduplicación, reconstrucción y vacíos). Una lista ordenada por mtime/bitácora por sí sola no prueba qué cambió. `Recently Updated` puede desbloquearse únicamente al validar la procedencia de tiempos.

**Backlog UX posterior:** Focus Reading, Saved Workspaces; Decision Explorer si existe caso real; Agent Run Explorer expandido si la continuidad mínima resulta insuficiente; Safe Capture con contrato y autorización independiente. F2 `daily_plan` es propuesta de esquema no aplicada; F4 vocabulario de tipos diferido. No planificar F1 sync cross-machine durante la pausa.

### Criterios de calidad que deben sobrevivir al handoff

1. Fuente y estado separados: *documentado*, *calculado*, *confirmado por ejecución* y *desconocido* no son intercambiables.
2. No cerrar puentes `[r]` ni cambiar el estado del proyecto en nombre del owner. Una entrega RC no significa aceptación humana.
3. Filtrar y enlazar al Markdown original, no mantener copias de conocimiento ni inventar relaciones de proyecto.
4. Un solo snapshot por respuesta; secuencia de solicitudes y cancelación en UI; fixtures adversariales, E2E y evidencia visual antes de liberar nuevas vistas.
5. Corporate/personal: mantener separados vaults/instancias; validar la política de MELI antes de uso laboral, sin asumir autorización.
6. Una pausa no es un cierre de proyecto: sin fecha comprometida, sin agentes automáticos, sin merge ni escritor en vault real por inferencia.

### Preguntas a resolver únicamente cuando se retome

- ¿Está ya implementada la RC F3? Descubrir HEAD, no asumir que `feature/f3-product-integration` existe.
- ¿Qué hallazgos de seguridad del StateDir siguen abiertos? ¿Qué actor debe cubrirse realmente? ¿Está definida la ventana de retries/retención?
- ¿Qué pantallas de v0.6 resultan útiles en una prueba UX real read-only y cuáles sobran?
- ¿Qué metadatos temporales son fiables para Change Feed/Weekly Review? Si no existen, definir captura antes de presentar métricas.
- ¿Qué decisión del owner autoriza cada gate? Nunca interpretar esta nota como autorización para G4.

## Fuentes

- Idea del owner del 2026-09-21: validar un prompt desde Loom e inspeccionar el contexto cargado según el prompt con todas las herramientas, incluida Graphify. Capturada como idea nueva, no incluida entre las 13 propuestas originales.
- Investigación de producto compartida por el owner el 2026-09-20: «Loom — convertir Agents-OS en tu centro de operaciones» (13 propuestas; investigación basada originalmente en v0.4). Se preserva aquí su inventario reconciliado con el estado posterior; las prioridades v0.7/v0.8 son propuestas, no decisiones de implementación ya aprobadas.
- `xKoRx/loom`, `feature/loom-v06 @ 36c760cc9d124ef8522aa10ab91852e1fcac334b`, `specs/FEAT-LOOM-V06/SPEC.md`.
- `xKoRx/loom`, `feature/f3-ux-lab @ 47cbadb8e3e46cda85ccac776fc6de767338bc44`, `specs/FEAT-F3-UX-LAB/RESULTS.md`.
- `xKoRx/loom`, `feature/f3-idempotency-gate @ 04a3ae80b9eaacd4165e1989a21246c9bc2d8898`, `specs/FEAT-F3-IDEMPOTENCY/RESULTS.md`.
- [[Loom — Continuidad y próximos pasos]] (gate siguiente y condiciones de reentrada).