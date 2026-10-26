---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Ventanas móviles de 24 meses y estabilidad temporal]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox", "topic/sqx144"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/ventanas-moviles-de-2-anos-y-si-la-metrica-global-nos-esta-escondiendo-lo-importante"
related: ["[[IMOX]]"]
---

# IMOX - Ventanas móviles de 24 meses y estabilidad temporal

## Síntesis vigente

El post propone mirar cuándo se obtuvo el beneficio y no solo el total global. Agrupa P/L mensual y calcula, para cada ventana de 24 meses, beneficio de esa ventana dividido por **MaxDD global de la estrategia**. Desplaza un mes y resume peor, mediana y última ventana.

## Interpretación

Con 48 meses hay 25 ventanas solapadas; no son 25 observaciones independientes. El denominador no es el drawdown local de cada ventana. El autor usa 24 meses para equilibrar muestra y capacidad de detectar estancamiento, especialmente con H4/D1 de baja frecuencia.

Sus zonas —negativo, de cero a una vez MaxDD y por encima— son criterios de investigación del autor, no gates universales. Peor y última ventana deben interpretarse juntas. No garantiza estabilidad futura.

## Debate

Cristobal propone Stability; otros, R² y Recovery Factor. Xavi los considera complementarios. Se discuten degradación IS/OOS y comparación SQX/MT5 año a año, porque discrepancias de años distintos pueden compensarse en el total.

Luis describe otro camino: condiciones con edge definidas antes del filtrado SQX, en lugar de generación libre. Esto refuerza separar hipótesis previa y búsqueda posterior, sin demostrar que su edge esté replicado.

## Uso propuesto

Añadir análisis temporal como diagnóstico y comparador antes de convertirlo en un filtro. Adaptar ventana y muestra a la frecuencia de la hipótesis; fijar el criterio antes de examinar candidatos nuevos.


## Evidencia y provenance

- [Post original en Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/ventanas-moviles-de-2-anos-y-si-la-metrica-global-nos-esta-escondiendo-lo-importante).
- Autor: Xavi Lorente. Revisión directa en Chrome: 2026-10-24.
- [[IMOX - Fuente - Ventanas móviles de 24 meses y estabilidad temporal]]. Se distinguen instrucciones escritas del administrador, prácticas de miembros y análisis propio.

## Límites y contradicciones

Cuerpo y comentarios accesibles leídos; hay imagen ilustrativa y adjunto no auditados en detalle, y respuestas adicionales no revisadas íntegramente. No se validaron correlaciones entre métricas ni se reprodujeron resultados.
