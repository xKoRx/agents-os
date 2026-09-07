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

# 04 — Principios y decisiones

[[agents-os|← Volver al índice]]

## Principios duros (acordados)

1. **Dos sistemas, un vault.** Documentación (entidades reales = fuente de verdad) y Memoria del agente (cómo se ha trabajado). La memoria cuelga de las entidades, no las duplica.
2. **Cross-ámbito.** Hoy sesgado a TI, pero el objetivo es cubrir todo lo que hace el usuario.
3. **Agnóstico al agente.** Codex, Claude, Cursor, Antigravity, MiniMax, etc.: todos usan el mismo sistema y **Graphify de la misma manera**. Si cada agente lo usa distinto, el sistema se degrada con el tiempo.
4. **Cero gestión manual para el usuario.** Todo lo hace el agente; el usuario **consume y valida**.
5. **Markdown como fuente de verdad.** Graphify es índice derivado y reconstruible.
6. **Retrocompatibilidad por raw.** Se guarda la sesión completa (L0) para poder **reprocesar** y extraer nuevos tipos de conocimiento a futuro (retrofit), sin sobrecargar la metadata de hoy.
7. **No ensuciar el vault ni el root.** Respetar la estructura existente; ubicar artefactos en carpetas existentes.
8. **No guardar evidencia pesada.** Logs, dumps, exports grandes van a su sistema (MinIO, repo, storage); en Obsidian solo **referencias**.
9. **Conflicto de conocimiento → resolver y registrar.** El agente debe resolver la contradicción con el contexto disponible, editar lo necesario y dejar log auditable; no debe bloquear por consulta humana en beta.
10. **El grafo explota estructura, no la inventa.** La utilidad de Graphify depende de notas bien modeladas (nombres consistentes, links, tags y properties limpias).

## Decisiones tomadas

- **Raw session**: el **agente** crea el placeholder L0 y el **usuario** pega la sesión completa; el agente genera el resto (summary si aplica, learnings, ADRs, known errors, updates y logs).
- **Graphify uniforme** entre agentes, con **documentación base** de uso obligatoria.
- **Reindex manual documentado para beta**; watcher queda como mejora post-beta.
- **Higienización manual al cierre del día**, como proceso aparte (validar/corregir/reportar por fecha y nuevas sesiones).
- **La base del sistema es a nivel de skills + reglas** (un documento tipo system-prompt / convención), no MCP ni servicio en el MVP.
- **Conflicto de aprendizaje** se resuelve por el agente, partiendo de la premisa de **contexto enriquecido**, y deja registro en `80-agents/journal/logs/`.
- **Memoria centralizada:** `80-agents/memory/public/` para memoria pública y `80-agents/memory/internal/` para memoria interna.
- **Journal separado:** `80-agents/journal/sessions/` para sesiones y `80-agents/journal/logs/` para cambios auditables.
- **Modelo sin `status` para memorias:** una memoria vigente existe; una memoria obsoleta se elimina o reemplaza y se registra el cambio.
- **Graphify beta:** usar `graphify-obsidian`; si falta índice, generarlo/reindexarlo antes de hacer retrieval degradado.
- **Outputs Graphify objetivo:** migrar a `graphify-out/` en root con `.graphifyignore`; no borrar `95-graphify/` sin tarea explícita.

## Decisiones descartadas (para el MVP)

- **Vector DB / embeddings como base principal.** Motivos: menos control humano, más infraestructura, menos auditabilidad, no modela vigencia de decisiones ni resuelve contradicciones, menos portable que Markdown + Git. Posible como **acelerador auxiliar** más adelante, no como base.
- **Context packs manuales persistentes** como índice paralelo. Graphify ya cumple el rol de índice; mantener uno a mano duplicaría información y generaría deuda documental.
- **Guardar logs/evidencia pesada en Obsidian.** Solo referencias.
- **Watcher como requisito beta.** Queda fuera para evitar bloquear el circuito mínimo.

## Tensión de diseño a vigilar

- **Costo de metadata vs adopción.** Como todo lo gestionan agentes (el usuario solo valida), el costo de llenar metadata recae en el agente; aun así conviene **mínima metadata** que mueva el retrieval y crecer por retrofit, para no fragilizar la consistencia.
- **Enforcement de comportamiento.** Una convención en Markdown solo se cumple si el harness del agente la inyecta (skill/rules/system-prompt). De ahí que la base sea "skills + reglas" y Graphify uniforme.
