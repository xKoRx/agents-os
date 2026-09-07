---
type: doc
status: draft
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
created: 2026-06-27
updated: 2026-06-27
aliases:
  - Primer para IA
---

# 00 — Onboarding para otra IA

[[agents-os|← Índice]]

> [!info] Si eres una IA y vas a trabajar en este proyecto, lee este documento primero. Es el contexto mínimo para entender el **AGENTS OS** sin huecos. Detalle en los documentos `01`–`06`.

## En 60 segundos

- Esto es el diseño de un **sistema de memoria/aprendizaje para agentes** (AGENTS OS) sobre un vault de **Obsidian** + el indexador **Graphify**.
- Conviven **dos capas** en el mismo vault:
  - **Capa 1 — Documentación**: entidades reales (proyectos, apps, áreas…). **Fuente de verdad**. Ya implementada.
  - **Capa 2 — Memoria del agente**: aprendizajes/decisiones/errores/preferencias sobre **cómo se ha trabajado** con esas entidades. En diseño. **Cuelga de la Capa 1 vía links; no la duplica.**
- **Graphify** = índice derivado para recuperar contexto barato; **Markdown = verdad**.
- Objetivo: que el agente recupere lo importante sin leer todo el vault y, con el uso, entienda mejor al usuario en **todos sus ámbitos**.
- Decisión beta: memoria pública e interna viven en `80-agents/memory/`; sesiones y logs viven en `80-agents/journal/`.

## Reglas que debes respetar

1. **No dupliques entidades.** La memoria referencia la entidad real con `[[link]]`.
2. **Markdown es la verdad**; Graphify es reconstruible.
3. **No guardes logs/dumps/evidencia pesada** en el vault: solo referencias (rutas s3, commit, job id).
4. **No ensucies el root** del vault; usa la estructura existente.
5. **Conflicto de conocimiento → resuelve y registra.** Usa contexto enriquecido, edita lo necesario y deja log auditable en journal.
6. **Consulta Graphify antes de leer notas**; si el índice no existe o está obsoleto, genera/reindexa con `graphify-obsidian`.
7. **Puedes editar conocimiento canónico directo** cuando el cambio sea necesario, pero debes dejar log del cambio.
8. El usuario **consume y valida**; tú haces el trabajo. No le generes carga de gestión.
9. Las memorias no usan `status`; si una memoria ya no sirve, se elimina o reemplaza y se registra el cambio.

## Estado actual

- Capa 1 implementada (ver [[agents-os]] -> "Avances").
- Capa 2 beta ya tiene estructura operativa en `80-agents/memory/`, `80-agents/journal/`, `80-agents/templates/` y `80-agents/skills/`.
- Skills listas o forward-testeadas: bootstrap, context retrieval, memory distillation, conflict resolution, Graphify maintenance, hygiene review, entity update, retrofit raw session y behavior config.
- Pendiente central del MVP: `agents-os-session-close` todavia necesita forward-test con un transcript real provisto por el usuario.
- Pendiente beta: ejecutar el circuito en proyecto real y validar con Codex, Claude, Cursor y Antigravity.
- Watcher queda fuera de beta.
- Hay decisiones tomadas y puntos pendientes: ver [[05-preguntas-abiertas]]. **No inventes** resoluciones donde dice "pendiente"; si necesitas una decisión que no está, **pregunta al usuario**.

## Mapa de lectura

1. [[01-problema-y-vision]]
2. [[02-arquitectura]]
3. [[03-flujos]]
4. [[04-principios-y-decisiones]]
5. [[05-preguntas-abiertas]]
6. [[06-glosario]]
