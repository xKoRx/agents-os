---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - SQX 144 - Builders cortos y filtros baratos]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox", "topic/sqx144"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/generando-estrategias-en-sqx-v144-sin-que-cada-bloque-dure-dias"
related: ["[[IMOX]]"]
---

# IMOX - SQX 144 - Builders cortos y filtros baratos

## Síntesis vigente

Xavi describe un flujo personal para evitar gastar días en tandas que no entregan estrategias: Builder con tope habitual de una hora y banco de 15–30 aceptadas; Custom Projects encadenados.

## Cribado y secuencia

- Filtra en Build por criterios que ya usaría al final: CAGR/MaxDD y un snippet de años cuyo Net Profit supera el MaxDD con margen.
- Tras Builder y Monte Carlo Manipulation, retest rápido 1M slow del último año reservado, con Net Profit positivo como filtro. Luego las fases caras.
- Aclara que pedir último año positivo puede eliminar lógicas legítimas con años negativos naturales: no es regla universal.
- Declara que una tanda sin material termina cerca del tiempo de Build; una con supervivientes puede tardar 3–15 horas.

## Genética: ejemplo, no preset para copiar

En un comentario usa población 140, 120 generaciones, cuatro islas, migración cada 13 y reinicio por estancamiento en 25. Otro miembro usa cinco islas y población 20. Estos números no coinciden con la adenda de la guía 144 que recomienda 15 generaciones ni con Random de Aritz. Son caminos diferentes y no una configuración consensuada.

## Interés

Aplicar antes las comprobaciones baratas, medir coste hasta finalista y declarar un presupuesto por hipótesis. Un año llamado holdout que filtra candidatos ya participa en selección; reservar otra evaluación independiente si se quiere medir el proceso adaptativo.


## Evidencia y provenance

- [Post original en Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/generando-estrategias-en-sqx-v144-sin-que-cada-bloque-dure-dias).
- Autor: Xavi Lorente. Revisión directa en Chrome: 2026-10-24.
- [[IMOX - Fuente - SQX 144 - Builders cortos y filtros baratos]]. Se distinguen instrucciones escritas del administrador, prácticas de miembros y análisis propio.

## Límites y contradicciones

Cuerpo y nueve comentarios accesibles leídos. El autor dice explícitamente que no es una metodología cerrada. Sus resultados no fueron reproducidos y los ejemplos no se adoptan como parámetros de Rodrigo.
