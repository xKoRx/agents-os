---
type: doc
schema_version: 1
status: "active"
area: "[[Personal]]"
related: ["[[IMOX]]", "[[AGENTS OS]]"]
aliases: ["Contrato de registro de foros"]
tags: ["kind/doc", "tech/agents-os", "topic/communities"]
created: "2026-10-25"
updated: "2026-10-25"
---

# Registro de conocimiento de comunidades

## Propósito

Contrato portable para convertir un foro en conocimiento mantenido de AGENTS OS: preservar procedencia, decisiones y cobertura verificable. IMOX/Circle es la primera aplicación; Reddit podrá usar el mismo contrato con su adaptador de identidad y navegación, sin asumir equivalencia entre plataformas.

## Contenido

### Autoridad y ubicación

- El `source` existente de cada publicación conserva identidad, lectura, decisión, destinos y pendientes. No crear otro registro por cada lectura ni por cambiar el título.
- Recursos de dominio mantienen síntesis; ideas, lecciones, decisiones, recordatorios o proyectos reciben enlaces de provenance. No guardar todo como memoria de agente ni promover un comentario a regla por su tono convincente.
- El índice de conocimiento elige qué consultar; el registro operativo indica qué se procesó; la revisión por lote demuestra qué cambió y la cobertura registra qué universo se recorrió.
- Capturas pesadas opcionales bajo `_sources/`; no credenciales, tokens, volcados masivos ni datos personales innecesarios.

### Identidad

Preferir ID nativo del post cuando esté visible/disponible. Sin él, clave provisional de plataforma+host+path canónico; quitar fragmentos de comentarios y parámetros de seguimiento. Preservar aliases/redirecciones comprobadas si cambia la URL. Dos comentarios no son dos posts; un PDF sin locator original es adjunto/suministro del usuario, no otro post de su URL de contexto.

Para Reddit, usar su ID de submission cuando se verifique; no inferirlo antes de revisar la fuente. Este contrato no activa ni conecta Reddit.

### Campos de seguimiento sobre `type: source`

| Campo | Significado |
|---|---|
| `platform`, `community_key`, `record_kind` | Origen y clase (`post`, `attachment`, eventualmente `comment`). |
| `post_key`, `source_post_id`, `canonical_post_url`, `space_key` | Identidad y scope; IDs desconocidos permanecen null. |
| `published_at`, `source_updated_at` | Tiempos de la plataforma, solo si están contrastados. |
| `registered_at` | Registro en el vault con offset. No es fecha de publicación o de lectura. |
| `last_reviewed_on`, `last_reviewed_at`, `review_time_precision` | Fecha/hora real de revisión y precisión disponible. Una fecha histórica sin hora se mantiene como fecha. |
| `processing_state` | `discovered`, `partial`, `processed`, `excluded`, `inaccessible`. |
| `reading_scope`, `body_coverage`, `comments_coverage`, `attachments_coverage` | Qué se leyó y qué falta. Un resumen generado no prueba lectura exhaustiva. |
| `relevance_decision`, `decision_reason` | `useful`, `not_useful`, `deferred`, `duplicate`, `undecided`, con razón específica. Un caso nuevo no puede cerrarse con «no sirve» sin explicar por qué. |
| `knowledge_destinations` | Enlaces a conocimiento/idea/lección/proyecto donde se integró; para un duplicado, enlace al registro canónico. |
| `pending_reason`, `last_registration_review` | Próximo paso y revisión/lote que dejó ese estado. |
| `contribution_state`, `contribution_reason` | `not_planned`, `idea`, `draft`, `published`; identidad/permalink del aporte si realmente se publica. |

`status` del tipo source conserva su lifecycle documental (`active`, etc.) y **no** se reutiliza para el workflow de lectura.

### Evidencia de ausencia

«No registrado», «no encontrado en este recorrido», «no accesible» y «no existe en el scope enumerado» son estados distintos. Solo un inventario completo acotado permite afirmar ausencia en ese intervalo/espacio; no extenderla a toda la comunidad ni a contenido borrado, privado o no visible.

### Cierre de procesamiento

`processed`: lectura suficiente para el scope explícito, integración terminada y provenance resoluble. No certifica que las afirmaciones sean verdad ni que estén implementadas. `excluded`: clasificación motivada terminal para el scope vigente, conservando el nivel real de lectura y la condición que justificaría reconsiderarla. `inaccessible` o `partial` no se convierten en `not_useful` para cerrar una cola.

Descartes posibles: fuera del interés definido, duplicado con destino canónico, promoción sin evidencia utilizable, versión obsoleta sustituida, contexto insuficiente para aplicarlo o investigación que no responde al objetivo actual. Distinguir «no útil ahora», «falso contrastado», «incierto» e «inaccesible». Una nueva evidencia o cambio de interés puede reabrir la decisión.

### Ingesta y extracción

Clasificar salida: conocimiento estable de la entidad; idea a evaluar; lección reusable; decisión contextual; recordatorio/tarea; propuesta de aporte. Crear solo el destino que aporte valor y tenga contrato/template; enlazar en vez de duplicar. No copiar manuales enteros ni ejecutar adjuntos por aparecer en el foro.

En cambios de un post, comparar con lo capturado previamente y actualizar las notas afectadas, conservando contradicciones y versión anterior relevante. No releer automáticamente todo el histórico si una identidad y revisión ya cubren el mismo contenido sin señales de cambio.

### Tiempo y revisiones

Una nota `doc` por lote de revisión puede agrupar día/hora, alcance, enumeración, decisiones, destinos, pendientes y checkpoint. Si hay varias corridas en un día, registrar horas exactas verificadas y IDs distintos; no crear una fuente duplicada por corrida. `log.md` conserva un resumen cronológico con link a la revisión.

No confundir `último post visto`, `última lectura`, `última actualización`, `inventario completo` y `procesamiento completo`. La semántica de intervalos contiguos y las tres colas de sincronización están en [[IMOX — Cobertura de revisión]] para la primera implementación. Al incorporar otra comunidad, instanciar ese control con sus capacidades comprobadas.

### Aplicación inicial

[[IMOX — Registro de publicaciones]] · [[IMOX — Cobertura de revisión]] · [[IMOX — Revisión 2026-10-25 - Inicialización del registro]]. Seguimiento a pedido. La portabilidad del contrato no significa que Reddit ya esté conectado o inventariado.

## Fuentes

- Solicitud expresa de Rodrigo, 25 de octubre de 2026; incluyendo conservar descartes, intervalos de cobertura y futuro interés en Reddit.
- [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] y las notas source de IMOX como evidencia de la migración local.
