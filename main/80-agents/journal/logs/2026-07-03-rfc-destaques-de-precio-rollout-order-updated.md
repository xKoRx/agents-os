---
type: change_log
scope: project
created: 2026-07-03
updated: 2026-07-03
entities:
  - "[[Bajo y Muy Bajo Precio]]"
  - "[[RFC Destaques de Precio - Hito 2]]"
related:
  - "[[Destaques de Precio]]"
confidence: high
tags:
  - kind/log
  - area/meli
  - project/destaques-de-precio
---

# RFC Destaques de Precio - Rollout Order Updated

## Contexto

El usuario pidió mejorar el RFC de Hito 2 para reflejar el orden de despliegue vigente:

- primero **MLA + MLM**, porque la nueva versión del Sugeridor ya corre hace tiempo en ambos sites;
- después el **resto de sites no-MLB** en paralelo;
- **MLB** se trabaja después de MLA/MLM como carril separado basado en precio FIPE;
- la implementación base es común para todos los sites y sólo cambian las condiciones de tageo por site.

## Cambios

- `sb-main/01_Projects/previous-price-motors/rfc.md`: actualizado resumen, alcance por señal, estado/madurez por site, principios de diseño, proceso masivo, rollout propuesto y pendientes de definición.
- `10-projects/Destaques de Precio/agentes/RFC Destaques de Precio - Hito 2.md`: actualizado estado, tareas, bitácora y decisiones del proyecto de agente.
- `10-projects/Destaques de Precio/Bajo y Muy Bajo Precio.md`: actualizado estado actual, bitácora y decisiones del Hito 2.

### Iteración técnica posterior

El usuario corrigió y completó definiciones técnicas del RFC:

- Atributos de item aún no definidos: deben ser mínimos, idealmente booleanos (`true`/`false`) y filtrables en Search.
- Queda pendiente definir/crear atributos, agregarlos a caché Search API Go e iniciar conversación para filtrabilidad en Search.
- Hito 2 es una iteración de **Bajó de Precio**: se debe escalar el consumer/procesamiento existente, no diseñar una línea paralela.
- El consumer de procesamiento debe ser único y recibir cambios de precio + cambios de atributos.
- Ya existe consumer de cambios de precio para Bajó de Precio; se debe agregar consumer de cambios de atributos.
- Prioridad funcional: primero Bajo/Muy Bajo de Precio, luego Bajó de Precio.
- El proceso masivo debe paginar y encolar items al tópico/consumer común de procesamiento.
- Trigger del proceso masivo queda pendiente tanto para no-MLB como para MLB.
- Observabilidad, experimentos y rollout operativo quedan `TBD`.

## Validación

- Lectura puntual del RFC actualizado confirmó que el orden de rollout ya aparece como MLA+MLM primero, resto de sites no-MLB después en paralelo, y MLB como carril FIPE posterior.
- Se corrigió el pendiente antiguo que hablaba del criterio de entrada de MLB como deploy del nuevo Sugeridor; ahora queda expresado como criterio FIPE.
- Lectura puntual posterior confirmó que el RFC ya contiene contrato de atributos como pendiente, consumer común escalado desde Bajó de Precio, consumer de atributos, proceso masivo paginado y secciones Observabilidad/Experimentos/Rollout como `TBD`.

## Corrección de target

El usuario corrigió que el documento a actualizar no era el `rfc.md` legacy sino el RFC específico:

- `sb-main/01_Projects/previous-price-motors/RFC Destaque de precio — Hito 2.md`

Se aplicó la iteración técnica a ese archivo. El seguimiento del proyecto se actualizó para apuntar a ese RFC como fuente principal del Hito 2.
