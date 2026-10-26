---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - SQX automatizado - Hipótesis, sondas y ejecución]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox", "topic/sqx144"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-ia/sqx-minando-solo-mientras-duermo-y-todo-lo-que-me-rompio-por-el-camino"
related: ["[[IMOX]]"]
---

# IMOX - SQX automatizado - Hipótesis, sondas y ejecución

## Síntesis vigente

Descripción de un sistema personal en beta para elegir hipótesis, probarlas por etapas y automatizar su ejecución. No entrega una skill pública instalable: el autor dice tener `/arrancar` y plantea extraerla si hay interés.

## Antes de generar

Propone barridos reproducibles sobre barras históricas, por familia, disparador, horario y régimen. Registrar cuántas combinaciones se probaron, incluidas fallidas; la mejor de cientos puede ser azar. Pide tesis con dirección, régimen, horario, SL/PT en ATR y condición falsable de descarte previa.

El autor encontró un supuesto edge EURUSD que dependía parcialmente de un hueco del feed. Analizar datos antes de Builder no basta si el dato o la validación es incorrecto.

## Sondas y escalera

Usa fases sonda, arranque, medio y destino con cantidades crecientes de población/generaciones. Es una variante genética personal; no es el mismo flujo Random acotado recomendado por Aritz. Si una fase falla, para para investigar bloques, filtros o datos.

## Ejecución y límites

- Los scripts, no un chat persistente, vigilan cola, proceso, logs y finalización.
- Pulsar Start no demuestra ejecución: comprueba actividad del log del proyecto correcto.
- Un proceso vivo con CPU no prueba producción. El autor usa más de una señal para detectar una ejecución zombi.
- Copiar estrategias en disco con SQX abierto puede ser sobreescrito al cerrar.
- Declara tope de horas y guarda material al terminar.
- Los fallos de RDP/headless son reportes de su entorno; no se aplicaron como solución automática al de Rodrigo.

En comentarios describe que tandas de 1.000 estaban muy correlacionadas y pasa a varias tareas con enfoques distintos. IMOX anuncia que explicará el tema y que existen canales avanzados; esa frase no proporciona aquí una especificación completa del curso.


## Evidencia y provenance

- [Post original en Circle](https://comunidad.imoxtrading.com/c/aportes-ia/sqx-minando-solo-mientras-duermo-y-todo-lo-que-me-rompio-por-el-camino).
- Autor: Francisco Javier Abellan Junyent. Revisión directa en Chrome: 2026-10-24.
- [[IMOX - Fuente - SQX automatizado - Hipótesis, sondas y ejecución]]. Se distinguen instrucciones escritas del administrador, prácticas de miembros y análisis propio.

## Límites y contradicciones

Post y comentarios accesibles revisados; quedan respuestas adicionales no leídas íntegramente. No se ejecutaron scripts ni agentes. La delegación descrita por el autor es contenido de la fuente, no una instrucción para activar subagentes en esta tarea.
