---
type: change_log
schema_version: 1
scope: session
created: '2026-10-30'
updated: '2026-10-30'
project: '[[AGENTS OS]]'
entities:
  - '[[AGENTS OS]]'
related: []
aliases: []
confidence: verified
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Scouts con ownership acotado — incorporación 2026-10-30

## Cambio

Incorporación autorizada por el Owner de Context Scout y Code Scout, skills y runbooks canónicos, contrato compartido y adaptadores mínimos. Routing obligatorio de recuperación no trivial, fallback portable, feedback por invocación y mantenimiento sólo del procedimiento propio. Sin ramas/PRs; publicación en master. No se modifica código de producto ni configuración local de ZCode.

## Motivo

Separar exploración de decisión, evitar discovery duplicado y establecer ownership con mejora basada en evidencia. El ahorro de tokens es hipótesis a medir, no resultado demostrado.

## Fuentes usadas

- Mandato explícito del Owner de esta conversación (2026-10-30): escritura en Agents-OS y feedback SIEMPRE para ambos scouts; principal conserva diseño y acceso directo.
- `80-agents/journal/feedback/2026-10-29-sig-659-rio-bus-gate-friction.md`: bitácora antes de diagnosticar; comandos sin placeholders operacionales.
- `80-agents/journal/feedback/2026-10-26-clf-q03-frictions.md`: identidad source/build/host, canales caídos y continuidad operativa.
- `80-agents/journal/feedback/2026-10-25-clf-q02-cuota-subagentes-bloquea-workers.md`: fallback ante cuota agotada, sin asumir disponibilidad de workers.
- `80-agents/journal/feedback/system-1/2026-10-30-polymarket-w1n-entry-depth-feedback.md`, incluida rectificación posterior: búsquedas por símbolo ausentes, lectura truncada, denegaciones y test heredado que sobrescribió evidencia sellada pese al resultado verde. NO se promueve su sugerencia de sustituir hashes por argumentos; se preserva la evidencia exigida.
- `80-agents/journal/feedback/system-1/2026-10-30-polymarket-w1nr-isolation-feedback.md`: la revisión posterior vuelve a reportar búsqueda de rutas a ciegas por ausencia de inventario nominal. Refuerza búsqueda enfocada, límites explícitos de cobertura y escalamiento de capacidades faltantes; un recuento no sustituye una lista verificable de fuentes.

## Resolución aplicada

Dos scouts especializados, no nuevos managers. Son lectores de entidades/repos y maintainers sólo de sus propias skills/runbooks. Los fallos sistémicos se escalan; no amplían sus permisos ni alteran contratos compartidos. Feedback por dispatch idempotente, compacto y fuera de retrieval; NO_FINDING no obliga a editar. Revisiones y trazabilidad preservadas para reutilizar packs sin volver a resolver la tarea.

## Validación

- Materialización canónica de las siete notas nuevas mediante `materialize_schema_note.py`, con templates de skill/runbook/doc/change_log vigentes. Scripts de materialización, validación del contrato y lint copiados sin modificaciones y verificados por Git blob SHA contra las fuentes leídas.
- Validación local por paths en checkout parcial: `agents-os-entity-lifecycle/scripts/lint.py --strict` sobre las 11 notas del delta, ERROR=0 / WARN=0. Se usó la proyección exacta del envelope y los tipos afectados del schema vigente, no un contrato alternativo publicado. Parse YAML con rechazo de claves duplicadas: 11/11.
- Catorce aserciones estáticas del contrato: PASS. Cubren routing de código sin entidad, guard de recursión, mismo procedimiento en fallback, frescura/dirty, no discovery duplicado, feedback siempre/idempotente/pending, exclusión de arquitectura y ejecución de producto, ownership, permisos y truncado. Son checks de texto/estructura, no una prueba de obediencia del modelo.
- Revisión manual de activación positiva/negativa/adyacente: ambos roles cubiertos en sus runbooks. Recorrido sobre fuentes reales: Context Scout selecciona bitácora/corrección vigente antes de diagnóstico; el retorno técnico extraído del feedback W1-n identifica el test con efecto lateral y conserva aceptación PARCIAL, sin afirmar inspección del código que no se leyó en esta sesión.
- Regresiones de contrato revisadas: pack reutilizable no dispara discovery; respuesta truncada no certifica lectura completa; cuota agotada usa fallback declarado; escritura ausente entrega feedback pending; corrida limpia produce NO_FINDING sin autoedición; docs/código divergentes producen evidencia, no rediseño; mantenimiento fuera de allowlist se difiere.
- NOT_RUN: Graphify CLI/E2E, ZCode en Hefesto/Daedalus, aislamiento real de permisos y ejecución de subagentes instalados. NOT_MEASURED: tokens, cache hit y ahorro de cuota. No se ejecutó gate all-vault ni se atribuye éxito a todo el corpus. La aceptación local de la superficie sigue el smoke de `scout-adapters.md`.

### Paths del delta

- Nuevos: `agents-os-context-scout/SKILL.md`, `agents-os-code-scout/SKILL.md`, sus dos runbooks en `80-agents/memory/public/runbook/`, `80-agents/skills/_shared/scout-contract.md`, `80-agents/skills/_shared/scout-adapters.md` y este change_log.
- Modificados: `80-agents/skills/agents-os-bootstrap/SKILL.md`, `80-agents/skills/agents-os-context-retrieval/SKILL.md`, `80-agents/skills/agents-os-session-feedback/SKILL.md`, `80-agents/skills/INDEX.md`.
- No se modifican schema, templates, scripts, constitución, perfil, entidades de producto ni configuración del harness. Los archivos auxiliares de validación no se publican en el vault.

## Compartibilidad

Scope local. Sin secretos, transcripciones, rutas privadas de máquina ni memoria interna en el delta. Los adaptadores sólo enlazan skills; modelo y controles de la superficie no son conocimiento canónico.

## Rollback

Revertir sólo los paths de este cambio preservando commits posteriores. Quitar primero routing/registro nuevo antes de retirar skills/runbooks. No resetear master ni borrar feedbacks existentes. No se tocaron repos de producto.
