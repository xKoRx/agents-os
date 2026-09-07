---
type: feedback
scope: session
status: open
created: "2026-06-30"
updated: "2026-06-30"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[Ariadna]]"
  - "[[Aranea]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-06-30-1636-aranea-docs-storage-batch-summary]]"
  - "[[2026-06-30-1636-aranea-docs-storage-batch-raw]]"
aliases: []
confidence: high
source_session: "[[2026-06-30-1636-aranea-docs-storage-batch-summary]]"
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - kind/feedback
  - scope/session
---

# Feedback sistema 1 — Sesión 2026-06-30 batch Aranea

> Sesión batch (3 entregas en una noche). Recogido para Kaizen.

## Qué complicó más la sesión y cómo se mejoraría

- **Bloqueo SSH+sudo NOPASSWD** descubierto al probar la cadena de
  inventario. Mejorable: validar `agent-read` antes de delegar, no
  después. Costo: ~30 min de latency en arrancar el subagente T1 con
  brief correcto.
- **MEMORY.md en estado de drift** detectado por el memory tool. No
  teníamos ritual explícito para resolverlo. Aprendido en caliente:
  rewrite `§-delimited`.
- **Sibling subagent warning** durante T2 (`sa-0-bf42550b` reportó que
  modificó AUDIT.md/BACKUP-SYSTEM.md simultáneamente). Verificado en
  disco con `wc -l` después: contenido completo. Probable falso
  positivo del tracker. Sin acción correctiva.

## Qué parte de Sistema 1 fue más útil

- **MEMORY consolidada** con bug del dashboard incluido — el
  side-note quedó visible para la próxima sesión, que es exactamente
  lo que sirve.
- **Tickets 010/011 en `~/aranea/tickets/`** siguiendo la convención
  existente — consistent con prácticas del owner.
- **Decisión sobre ubicación `30-resources/aranea/`** documentada
  como ADR formal antes de ejecutar — el owner explícito manda sobre
  AGENTS OS.

## Qué parte fue menos útil, redundante o ruidosa

- **3 placeholders intencionales** ("Pendiente Task 2") en T1: pequeño
  ruido pero era necesario como contrato explícito de qué llenaría T2.
  OK mantener en futuras cadenas de delegación.
- **El wiki-link `[[Ariadna.md]]` y otros** apuntan a notas que no
  existen en el vault (como `[[30-resources/aranea/00-index]]` no
  resuelve perfecto en Obsidian graph mode, hay que pasar links
  canónicos con extensión `.md`). Trabajable pero no crítico.

## Qué problema apareció que Sistema 1 no resuelve pero podría ayudar

- **Validación de wiki-links cross-task**: T2 generó docs que apuntan
  a T1 docs. Tuve que validar manualmente con `grep` + `wc` que los
  targets existen. Podría haber una skill `agents-os-link-validation`
  o invocación Graphify que lo automatice.
- **Drift tracking entre tareas**: si T1 hubiera escrito `2026-06-30`
  y T2 hubiera partido de `2026-06-28` sin saberlo, habría quedado
  inconsistente. El brief del padre debe reforzar explícitamente la
  fecha de captura (sí lo hice esta vez).

## Qué feedback deja sobre retrieval, skills y templates

- **El template `decision.md` no se aplicaba explícitamente para
  decisiones de ubicación**, lo armé ad-hoc siguiendo estructura
  observada en otros ADRs del vault. Evaluar formalización.
- **El template `raw-session.md` está perfecto** — fácil de llenar,
  rápido de cerrar. Cero fricción.

## Qué dolor parece repetible y debería evaluarse para promoción a L3

- **Patrón "chain de subagentes T1→T2 sobre output pre-existente"**:
  funcionó muy bien esta vez (T2 leyó T1 en lugar de empezar de
  cero). Vale la pena un **skill `agents-os-delegation-chain`** que
  estandarice: brief con paths absolutos esperados, slots a llenar,
  cross-validation de wiki-links al cierre.
- **Drift de datos por refresh manual faltante** (caso NOPASSWD):
  promover a **runbook/known-error** consolidado. Ya está hecho en
  parte como `known-error/aranea-agent-ro-sudo-nopasswd-blocked.md`.
