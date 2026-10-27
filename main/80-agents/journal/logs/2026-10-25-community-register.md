---
type: change_log
schema_version: 1
scope: session
created: "2026-10-25"
updated: "2026-10-25"
area: "[[Personal]]"
project:
application:
entities: ["[[IMOX]]", "[[AGENTS OS]]"]
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: "local"
load_policy: "manual"
indexable: false
index_priority: "never"
tags: ["kind/change-log", "scope/session"]
---

# Registro de conocimiento de comunidades

## Cambio

Se ampliaron los 23 sources IMOX existentes con seguimiento operacional (22 posts únicos y un adjunto no contado como post), preservando su provenance, contenido y fechas de lectura originales. Se crearon registro, cobertura, revisión local fechada, contrato portable y skill federada; navegación en índices de IMOX/agents/skills. No se migra este conocimiento a memoria de agente por defecto.

## Validación

Aplicación al caso real: deduplicación por identidad, separación del PDF adicional de su URL de contexto, conservación de horas desconocidas y cero fronteras históricas atribuidas. Resultado de clasificación conservadora: 2 posts procesados dentro del alcance previo y 20 parciales. No se ejecutó lectura web ni se movió una fecha last_verified de conocimiento por registrar metadata. Revisión a pedido por elección explícita del usuario; cero automatizaciones. Casos de frontera: fechas recientes dispersas no cierran meses anteriores; un post viejo con comentarios nuevos reabre cola de actividad; inaccesible no equivale a irrelevante. Gate federado dirigido: cero errores/avisos; YAML con rechazo de claves duplicadas en 56 notas, 22 identidades de post únicas, un adjunto separado, cero fronteras históricas falsas y cero enlaces rotos. Diagnóstico portable `quick_validate.py` rechaza las claves locales esperadas aliases, area, created, entities, index_priority, indexable, load_policy, related, schema_version, scope, tags, type, updated, según el perfil federado; no se retiraron para forzar compatibilidad. Aplicación manual real a migración local: no se navega a Circle ni se programa revisión. Activación negativa consulta general sin registro; adyacente publicación requiere pedido concreto. Validación final 00:18:06 America/Santiago. La clasificación procesado/parcial no certifica corrección de las afirmaciones.

## Rollback

Retirar únicamente los campos de seguimiento añadidos a sources y las notas/skill nuevas, revertir enlaces/entradas de este cambio y preservar todas las extracciones previas. No hubo cambios en Circle ni fuentes externas.
