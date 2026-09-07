---
type: doc
status: draft
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
created: 2026-06-27
updated: 2026-06-27
---

# 06 — Glosario

[[agents-os|← Volver al índice]]

- **AGENTS OS** — el sistema operativo de memoria/aprendizaje para agentes que define este proyecto (la Capa 2 + sus reglas y procesos).
- **Capa 1 / Documentación** — entidades reales (proyectos, apps, áreas, servicios, conceptos). Fuente de verdad para humano y agente.
- **Capa 2 / Memoria del agente** — conocimiento sobre cómo se ha interactuado con las entidades: aprendizajes, decisiones, errores conocidos, preferencias.
- **Memoria pública** — memoria Capa 2 auditable y legible por humanos/agentes. Vive en `80-agents/memory/public/`.
- **Memoria interna** — memoria Capa 2 gobernada por el agente para persistir hipótesis, heurísticas, planes internos y continuidad cognitiva. Vive en `80-agents/memory/internal/`, es indexable y se carga siempre cuando aplique.
- **Journal** — espacio operativo no canónico para sesiones y logs. Vive en `80-agents/journal/`.
- **Log de cambios** — registro auditable de creaciones, modificaciones y eliminaciones de memoria pública o entidades canónicas.
- **Entidad** — nota que representa una cosa real; responde "qué es y cómo funciona hoy".
- **Aprendizaje (learning)** — conclusión reutilizable que debería afectar sesiones futuras; necesita scope.
- **ADR / Decisión** — registro de una decisión y su justificación.
- **Known error** — falla conocida, su causa, impacto y mitigación.
- **Runbook** — procedimiento operativo validado.
- **Raw session (L0)** — conversación completa de una sesión en Markdown; respaldo y base de retrofit; sin evidencia pesada; no se indexa. El agente crea el placeholder y el usuario pega la conversación.
- **Session summary (L1)** — resumen destilado y enlazado de la sesión. Para beta vive en journal y no es la fuente principal de retrieval.
- **Niveles L0–L4** — roles del conocimiento (raw, summary, entidades, operacional, índice Graphify); no son carpetas.
- **Graphify** — indexador/CLI del usuario (macOS) que genera un grafo navegable del conocimiento; índice **derivado**, no fuente de verdad. Variantes: `graphify` (repos `~/fuentes`), `graphify-personal`, `graphify-obsidian`.
- **Retrieval** — recuperar contexto relevante (vía Graphify) sin leer todo el vault.
- **Retrofit** — reprocesar raw sessions guardadas para extraer nuevos tipos de conocimiento a futuro.
- **Watcher** — proceso futuro que reindexaría Graphify al insertar/modificar archivos. Queda fuera de beta.
- **Higienización** — proceso manual (fin del día) que valida, corrige y reporta el estado del conocimiento.
- **Contexto enriquecido** — premisa de que, al inicio de sesión, el agente ya cargó el conocimiento relevante de la entidad, lo que le permite detectar contradicciones.
- **Scope** — alcance de un aprendizaje (global / usuario / proyecto / app / tecnología / integración / error / workflow): determina cuándo cargarlo.
- **Load policy** — cuándo debe cargarse una nota (siempre / al cargar proyecto / app / etc.).
- **Indexable** — si una nota entra al índice de Graphify.
- **Constitución del agente** — reglas globales de comportamiento que el agente considera siempre (documento separado; **no** es este set de diseño).
- **Sin status** — regla del modelo beta: las memorias no usan `status`; si dejan de servir, se eliminan o reemplazan y el cambio se registra en journal.
