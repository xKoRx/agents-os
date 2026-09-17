---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Personal]]"
project: "[[Course Intelligence Engine]]"
application:
entities:
  - "[[Course Intelligence Engine]]"
related: []
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
---

# 2026-09-17 Course Intelligence Engine — Architecture Convergence

## Cambio

- **Tipo:** updated.
- **Archivo(s):** `10-projects/Personal/Course Intelligence Engine/Course Intelligence Engine.md`.
- **Commit:** `74ced7e6d703157410af78e75734fe4b5adc8c3a`.

## Motivo

- El debate entre dos interlocutores acordó cinco correcciones de diseño y ajustó el contrato de grounding y el orden del baseline/golden. La nota canónica aún contenía nueve SPECs, benchmark A/B/C y validación semántica insuficientemente delimitada.
- Se actualizó la misma entidad Sistema 2 para que futuras tareas tengan un único diseño vigente; no corresponde crear otro proyecto ni memoria duplicada.

## Fuentes usadas

- Texto de convergencia aportado por el usuario en la conversación del 17-09-2026, con aceptación explícita de ambos interlocutores y mandato de actualizar el proyecto al acordar.
- Nota canónica previa del proyecto en GitHub `master`, blob SHA `8c39cd6d794f13170f62b435bb431d2b50bee42d`.
- `80-agents/agents-os/agent-constitution.md`, `80-agents/skills/agents-os-entity-update/SKILL.md` y `80-agents/skills/_shared/note-types.md`.
- El documento exacto de Trading Course Intelligence de julio no se localizó; sus aportes quedan atribuidos al relato del debate, no verificados como contenido del vault.

## Resolución aplicada

- ADR-001 pasa a ACCEPTED FOR POC DESIGN, sin autorización de implementación ni certificación experimental.
- A y C comparten ejecutable y componentes; únicamente cambia `adaptive_investigation`. B se descarta provisionalmente para el MVP.
- Cobertura visual independiente de ASR y densidad configurable; barrido exhaustivo es una variante experimental.
- Validación de integridad determinista separada de grounding stateless; `SUPPORTED_BY_AUTOMATED_REVIEW` no implica verdad. Cambios por consolidación invalidan revisiones dependientes.
- Contratos de conocimiento reducidos a KnowledgeItem, Procedure, Relation, Evidence; SQLite operacional, JSONL exportable y Markdown como proyección.
- Roadmap comprimido de nueve a cinco SPECs, con golden humano temprano y congelado antes de evaluar; baseline A E2E completo antes de activar C.
- Mantener aislamiento por video y diferir infraestructura, modelos adicionales y procesamiento distribuido.

## Validación

- GitHub confirmó escritura del archivo del proyecto en `master`: commit `74ced7e6d703157410af78e75734fe4b5adc8c3a`, blob `6f701b7139a5a5e42ec29aa585b738980f49e451`.
- Pendiente: verificación de lectura de la nota actualizada y de este log. No se ejecutaron pruebas físicas, lint local ni código de la aplicación: repositorio local/VAULT_ROOT no montado en la sesión.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos, datos privados de memoria interna ni paths absolutos específicos de máquina.

## Rollback

- Recuperar el blob anterior `8c39cd6d794f13170f62b435bb431d2b50bee42d` de la nota, conservando trazabilidad de la reversión. No revertir automáticamente sin examinar cambios posteriores.
