---
type: change_log
scope: session
created: "2026-07-25"
updated: "2026-07-25"
area: "[[Personal]]"
project: "[[AGENTS OS - Hot Path y Cierre Silencioso]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-operating-continuity]]"
  - "[[agents-os-operating-continuity-archive]]"
  - "[[agents-os-session-feedback]]"
  - "[[agents-os-doctor]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/personal
  - project/agents-os
  - change/updated
  - change/created
---

# Hot Path Iteration — P4 Compactación y alineación aplicados

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - EDITADO `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
    — compactado de 270 a ~75 líneas.
  - CREADO `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity-archive.md`
    — contenido histórico movido, `load_policy: manual`.
  - EDITADO `80-agents/skills/agents-os-session-feedback/SKILL.md` — alineado
    con event-driven (P2).
  - EDITADO `80-agents/skills/agents-os-doctor/SKILL.md` — ajuste del
    umbral de leanness de 250 a 400 líneas (baseline medido).

## Motivo

- La global interna siempre-load pesaba 270 líneas con secciones que eran
  historia auditable (Kaizen runs, wikilinks chronicle, Economía de Tokens,
  TP creation attempts, MCP catalogs, Grid publicaciones). El brief de
  Hot Path recomendaba ~200-500 tokens para esta nota; la estábamos
  pagando completa en cada cold start.
- `agents-os-session-feedback` aún decía en su procedimiento que se creara
  feedback "siempre" al cerrar y un segundo feedback de Graphify si
  Graphify se usó — contradicción directa con el Silent Close de P2.
- El umbral "250 líneas" para dividir SKILL.md era arbitrario. Medición
  real: las skills más largas (268 líneas) tienen Progress Logs de 6-21
  líneas — el peso está en el contrato, no en la historia. Umbral subido
  a 400 para no generar ruido.

## Fuentes usadas

- Brief de ChatGPT `agents-os-hot-path-brief.md` (sección "Memoria interna
  enrutable", "Exactamente una nota global de startup, idealmente 200-500
  tokens").
- `agents-os-operating-continuity.md` (estado pre-P4).
- `agents-os-session-feedback/SKILL.md` (estado pre-P4).
- Mediciones `wc -l` sobre todas las skills.

## Resolución aplicada

- **Global interna split:** lo que cambia decisiones operativas (current
  stance, Hot Path summary, Graphify estado actual, Resource Wiki &
  Context Router, gotchas operativos) quedó en la nota always-load. Lo
  que es crónica fechada (setup inicial, clean install, higiene passes,
  Resource Wiki chronicle, MCP catalogs, TP chronicle, evaluación de
  adopción, ChatGPT pack) se movió a `agents-os-operating-continuity-archive.md`
  con `load_policy: manual` — cargar solo cuando se depura una decisión
  específica del pasado.
- **Feedback alineado con event-driven:** Purpose ahora lista 4
  condiciones de trigger (fricción / degradación / gap / sampling).
  Procedure pide decidir primero si aplica; si no, skip. Hard Rules
  explícito: clean session → no feedback. Graphify feedback NO automático,
  solo ante algo notable.
- **Umbral doctor ajustado:** el check 6 (leanness) ahora usa 400 líneas
  en vez de 250, con nota sobre el baseline medido.

## Validación

- Global interna: 270 → ~75 líneas (~70% reducción del costo en cold start).
- Archive incluye el link `[[agents-os-operating-continuity]]` para que un
  agente fresco pueda encontrarlo si lo necesita.
- `session-feedback` ya no se contradice con `session-close` (P2).
- Doctor check 6 ahora tiene un umbral basado en medición real, no inventado.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin identidad ni secretos. La credencial
  redactada en P0 no aparece en ninguna de las notas tocadas.

## Pendiente (no crítico)

- Forward-test real: medir el cold start post-P4 vs baseline pre-Hot-Path
  (~21-24k → esperado ≤8-10k) cuando se corra el gate E2E.
- Si los targets no se cumplen tras P4, los sospechosos son: (a) `agents-os.md`
  aún pesado (chequear si quedó procedimiento duplicado), (b) constitución
  o perfil demasiado largos, (c) entity pack por proyecto demasiado densos.

## Rollback

- Para la global interna: revertir el diff de
  `agents-os-operating-continuity.md` (volver a las 270 líneas) y borrar
  el archivo `...-archive.md`.
- Para feedback: revertir los 4 edits de `agents-os-session-feedback/SKILL.md`.
- Para doctor: revertir el cambio del check 6 a `~250 líneas`.
- Independiente entre sí.
