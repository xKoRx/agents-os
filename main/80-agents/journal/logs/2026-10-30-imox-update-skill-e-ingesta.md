---
type: "change_log"
schema_version: 1
scope: "session"
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Trading]]"
project: 
application: 
entities: ["[[IMOX]]"]
related: ["[[IMOX — Revisión 2026-10-30 - Actualización incremental]]", "[[30-resources/agents/skills/imox-update/SKILL.md]]"]
aliases: []
confidence: "verified"
source_session: 
source_feedbacks: []
share_scope: "local"
load_policy: "manual"
indexable: false
index_priority: "never"
tags: ["kind/change-log", "scope/session"]
---

# IMOX — Skill de actualización y lote 30 de octubre

## Cambio

Creación de skill federada `imox-update`, registro/handoff y manifiesto durable de descargas; cuatro parejas fuente/recurso nuevas (tres recientes, una histórica), nueve pares revisitados, source de evento y de documento, más síntesis/índices/registros/cobertura/logs. **128 posts únicos: 5 procesados, 13 excluidos con motivo y 110 parciales.**

## Motivo

Rodrigo pidió actualizar hasta hoy y repetir con «actualiza imox» en sesiones nuevas, exclusivamente Codex/Hefesto y Chrome del owner. Si no se pueden descargar documentos, solicita lista clicable y posterior carga de Descargas por pedido. La limitación de superficie/host viene del owner; permanece scoped a esta skill.

## Fuentes usadas

[[IMOX — Revisión 2026-10-30 - Actualización incremental]], fuentes enlazadas y pedido directo del owner del 2026-10-30. Materialización por contrato; skill-creator y agents-os-skill-authoring/runbook consultados.

## Resolución aplicada

Una skill específica posee ejecución/continuación IMOX y delega identidad/ingesta al contrato genérico. Registro del bootstrap garantiza descubrimiento en sesiones nuevas del vault; no se crearon copias/symlinks en carpetas cliente. No se cambió el bootstrap ni el perfil global. Se preservan desconocidos y frontera parcial; evento y adjunto no inflan posts.

## Validación

Forward-test real: pedido actual en Codex/Hefesto, Chrome KoR, fuentes nuevas/delta, Academia pide login, se persiste manifiesto con URL sin repetir descargas ni transmitir credenciales. Casos de activación revisados: «actualiza imox» aplica; «explica qué es IMOX» sólo consulta wiki; «ejecuta campaña Forge» deriva al owner de investigación y no inicia ingesta/operación por esta skill. Caso host distinto: la instrucción detiene ingesta y no propone otro navegador/máquina.

Lint estricto del SKILL ya pasó sin errores/advertencias; validación final del lote: 41 notas sin errores/advertencias, enlaces de las 42 rutas resolubles, 128 IDs únicos y manifiesto retomable. Parse YAML estricto aplicable al frontmatter. `quick_validate.py` se ejecutó: incompatibilidad esperada del perfil portable, rechaza `aliases, area, created, entities, index_priority, indexable, load_policy, related, schema_version, scope, tags, type, updated`. Se conserva metadata federada por el contrato canónico, no se suprime para fabricar PASS. No hay `agents/openai.yaml` adicional que validar.

## Compartibilidad

Local. Sin secretos, credenciales, tokens ni URLs privadas de acceso al evento. Los recursos de miembros son para investigación personal, sin redistribución.

## Rollback

Retirar sólo el lote nuevo identificado en la revisión y la skill/filas/handoff introducidos; restaurar del historial las revisitas y vistas derivadas si se requiere. No borrar ni duplicar fuentes previas ni descargas originales.
