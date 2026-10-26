---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Coste de IA - Traspasos y selección de modelo]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-ia/como-baje-un-78-lo-que-me-costaba-usar-la-ia-por-dia-con-mis-numeros-reales-y-en-lenguaje-de-trader"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Coste de IA - Traspasos y selección de modelo

## Síntesis vigente

El autor afirma haber reducido 78 % su coste diario mediante un sistema de traspasos y uso más eficiente de modelos. El método y medición completos están en un PDF enlazado.

## Conocimiento extraído

El cuerpo describe la frustración de agotar créditos y remite al artículo. Los comentarios explican una skill de traspaso que prepara continuidad para otra sesión y una selección de modelo según flujo y complejidad.

El valor transferible es separar trabajo que requiere más capacidad, continuidad compacta y contexto necesario. No se verificaron las tarifas, modelos, caché ni posibilidad de cambiar automáticamente defaults. Tampoco se atribuye a esta técnica eludir límites de cuenta.

## Comentarios y matices

Asier pide aclarar resumen versus traspaso y modelo potente versus ligero. Ricardo propone que la IA analice el flujo y cree la skill; comenta que deja de agotar cupos, pero no presenta en Circle un experimento controlado. Se desplegó la respuesta adicional, que solo agradece y anuncia prueba.

## Contraste con el PDF descargado

Se leyó `Claude_eficiente_para_traders.pdf`, cuatro páginas, especialmente la tabla de resultados de la página 3 y las limitaciones de la 4. La medición corresponde a registros de Claude Code entre 29 de septiembre y 10 de octubre de 2026; excluye el chat web.

**El 78 % del título no es el ahorro con el mismo trabajo.** El equivalente API diario reportado baja de 138 a 30 USD, pero el autor separa menor actividad de eficiencia. Para las mismas 1.699 requests estima 392 USD con hábitos anteriores frente a 150 efectivos: aproximadamente 60–62 % de ahorro modelado. No son dólares facturados en una suscripción.

Cinco cambios del autor: sesiones por tema/día, aviso de contexto grande o pausa larga, modelo por complejidad, lecturas/salidas acotadas e instrucciones persistentes más cortas. Su `/traspaso` propio escribe un archivo breve con estado y pendientes para una sesión nueva; `/compact` resume dentro de la misma sesión.

Umbrales de 300k tokens, una hora y precios/modelos son configuración y supuestos del artículo, no garantías del producto. No se verificaron los logs originales ni tarifas; tampoco hay medición independiente de calidad antes/después. Las contribuciones monetarias se reportan redondeadas.

## Adjuntos y cobertura

Post y nueve comentarios revisados. PDF: https://academia.imoxtrading.com/documento/t3u8qhv7aADn. PDF recibido y leído localmente con autorización; no se conserva una copia literal en la wiki.

## Interés para Forge

Prioridad de consulta: **Media**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-ia/como-baje-un-78-lo-que-me-costaba-usar-la-ia-por-dia-con-mis-numeros-reales-y-en-lenguaje-de-trader).
- Autor: Ricardo Exequiel Esposito Laine. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Coste de IA - Traspasos y selección de modelo]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

El 78 % mezcla menor uso y eficiencia; el propio PDF reduce la conclusión a alrededor de 60 % para cantidad equivalente de requests. No es ahorro generalizable ni prueba de igualdad de trabajo o calidad. Nombres de modelos y comportamientos del producto citados por miembros no se validaron como estado actual.
