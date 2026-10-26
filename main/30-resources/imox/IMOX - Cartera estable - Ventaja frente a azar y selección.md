---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - Cartera estable - Ventaja frente a azar y selección]]'
- '[[IMOX - Fuente adjunta - PDF Cartera estable]]'
last_verified: '2026-10-26'
confidence: high
aliases: []
tags:
- kind/resource
- area/trading
- topic/imox
created: '2026-10-26'
updated: '2026-10-26'
related:
- '[[IMOX]]'
---

# IMOX - Cartera estable - Ventaja frente a azar y selección

## Síntesis vigente

Hipótesis abierta: distinguir ventaja propia de exposición al mercado y sesgo de selección. Compara cada trade con 200 entradas del mismo lado y duración, sorteadas a ±180 días y excluyendo 45 días previos a la entrada hasta 7 días posteriores a la salida. El test local ±15 días favorecía artificialmente comprar caídas en paseos aleatorios. El autor reporta calibración con 1.000 paseos y 3% de falsos positivos para la versión corregida. Son resultados declarados, no reproducidos aquí.

## Evidencia y provenance

[[IMOX - Fuente - Cartera estable - Ventaja frente a azar y selección]] · [Circle](https://comunidad.imoxtrading.com/c/laboratorio-a51b70/en-busca-de-la-cartera-estable-dos-pruebas-para-separar-ventaja-de-suerte) · Xavi Lorente; revisión 2026-10-26. Afirmaciones atribuidas al autor o a miembros; no comprobación independiente de resultados, código o condiciones comerciales.

## Límites y contradicciones

Respuestas adicionales pendientes; no se ejecutó el experimento ni se validó código/dataset.

Decisión de ingesta: `useful`. Estado de lectura: `partial`; el recurso conserva conocimiento útil incluso si quedan medios o respuestas pendientes.

## Detalles contrastados en el PDF

El documento de siete páginas agrega `sin datos` para menos de diez operaciones fuera y distingue falta de potencia de contradicción con la ventaja previa. Replica estrategia original con parámetros, MM, costes y TF secundarios; separa 2015-01-05→2018-06-26 de referencia 2018-06-27→2025-07-31 y descarta trades que cruzan el corte. Con réplica inferior al 60% clasifica no fiable; bajo 80% avisa. Los umbrales son diseño del autor. Controlar timezone/DST y sesiones cambió sustancialmente la réplica reportada de índices europeos. Las figuras representan simulaciones y esquema de cadena, no resultados reales de EAs. La t supone trades independientes; el autor admite posible inflación por episodios compartidos y propone remuestreo temporal. No hay evidencia todavía de cartera más estable: necesita forward.

## Comentarios observados

Se discute beta frente a alfa, Sharpe deflactado y PBO. Un miembro plantea PBO sobre selección por mercado/TF/dirección, no sólo una EA; Xavi reporta que sólo dos EAs de oro de unas 200 superan dos ventanas antiguas. Son declaraciones no reproducidas. Otro miembro considera válido explotar beta y pide no filtrar hasta volver imposible generar; no convertir el debate en consenso ni en prohibición de beta.
