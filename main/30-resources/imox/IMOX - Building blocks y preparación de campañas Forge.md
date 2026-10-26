---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - Building Blocks Skill]]'
- '[[IMOX - Fuente - Guía de Building Blocks SQX 145]]'
- '[[IMOX - Fuente - Tipos de estrategia en trading algorítmico]]'
- '[[IMOX - Fuente - Builder - Minería de estrategias]]'
- '[[IMOX - Fuente - AnchoredVWAP - Exportación y compatibilidad por versión]]'
- '[[IMOX - Fuente - IA y Building Blocks - Cambio de enfoque de Aritz]]'
last_verified: '2026-10-24'
confidence: high
aliases: []
tags:
- kind/resource
- area/trading
- topic/imox
- topic/building-blocks
created: '2026-10-24'
updated: '2026-10-26'
related:
- '[[IMOX]]'
- '[[30-resources/applications/echo/echo-forge]]'
source_url: https://comunidad.imoxtrading.com/c/aportes-ia/building-blocks-skill
---

# IMOX - Building blocks y preparación de campañas Forge

## Síntesis vigente

Rodrigo declara que la metodología implementada por [[30-resources/applications/echo/echo-forge|Forge]] es la aprendida en [[IMOX]]. Para las próximas campañas necesita definir building blocks que permitan crear estrategias nuevas y variadas. Esta síntesis organiza las fuentes revisadas; no certifica equivalencia entre el código actual de Forge y toda recomendación comunitaria.

El post buscado es [[IMOX - Building Blocks Skill]], de Carlos K. Genera una **selección de bloques en `.sqb`**, no necesariamente nuevos indicadores ni plugins Java. Esa distinción debe resolverse antes de pedir que un agente «cree bloques».

## Ruta de lectura

1. [[IMOX - Tipos de estrategia en trading algorítmico]]: qué mecanismos se quiere diversificar.
2. [[IMOX - Guía de Building Blocks SQX 145]]: qué hace realmente cada pieza y qué puede imponer un preset.
3. [[IMOX - Building Blocks Skill]]: contrato para que un agente proponga selecciones importables.
4. [[IMOX - AnchoredVWAP - Exportación y compatibilidad por versión]]: comprobar que se puede llegar al motor de ejecución.
5. [[IMOX - Builder - Minería de estrategias]] y [[IMOX - Claude en CustomProjects para analizar databanks]]: coste, variedad y selección antes de robustez.
6. [[IMOX - Actualizar Broker Profiles en SQX]] y [[IMOX - Misma EA entre brokers - Nasdaq y productos distintos]]: producto, datos y condiciones reales.

## Contrato propuesto para un generador de presets

Esto es **análisis propio basado en las fuentes**, aún sin implementar:

| Entrada | Motivo |
|---|---|
| Build y motor objetivo de SQX, destino MT4/MT5 y parches relevantes | Un catálogo 145 no certifica importación/exportación de una instalación 144. |
| `.sqb` completo exportado por la instalación objetivo | Plantilla y allowlist de IDs reales, parámetros y estructura. |
| Familia/hipótesis, activo, broker/ticker, dirección y timeframe | Acotar la búsqueda por comportamiento, no solo nombres de indicadores. |
| Tipo de orden, nivel, margen/signo, disparador, filtro y salidas | La lógica nace de su combinación; un `.sqb` no garantiza fijar todo. |
| Catálogo de presets y estrategias anteriores | Detectar repetición de firmas y huecos de cobertura. |
| Rangos de parámetros, sesiones, costes y política de evaluación | Mantener comparables las variantes y evitar cambiar el criterio mirando resultados. |

Salida esperada: preset importable, manifiesto de bloques y versión, explicación de roles, diferencias frente a variantes previas y advertencia cuando haga falta template `.cfx`/AlgoWizard u otra pieza. Conservar identidad/hash del preset y relación campaña→builder→candidata→evaluación para poder comparar.

La guía de taxonomía descargada añade cinco decisiones —lógica, orden, horizonte, disparador y salida— y pide comprobar también el solapamiento de drawdowns. Esto amplía los cuatro ejes de campaña, sin asumir que cambiar de indicador diversifica.

### Gates propuestos

1. Ningún identificador fuera del catálogo permitido; parámetros compatibles y sin confundir comodines con números.
2. Importación real en SQX y revisión de bloques/órdenes activados.
3. Ejemplo mínimo exportado y compilado para el motor objetivo, antes de un minado largo.
4. Build corto con presupuesto de tiempo/candidatos, conservando también descartes y motivos.
5. Medir diversidad de firmas y lógica, candidatos aceptados por hora y coste de validación, además de las métricas finales.
6. Retest/optimización y contraste SQX→MT5 según metodología vigente; selección validada por código determinista, no solo respuesta del agente.
7. Evaluación independiente que no se haya usado para seleccionar, ajustar prompts, familias o parámetros de generaciones anteriores.

No se fijaron activos, presupuestos, umbrales ni recetas de campaña para Rodrigo. No se ejecutó ni se lanzó minado alguno.

## Matriz inicial de hipótesis

Es una lista de investigación, no una selección rentable ni un preset implementado:

| Hipótesis | Estructura a especificar | Riesgo de confusión |
|---|---|---|
| Breakout | Nivel y disparador de ruptura, orden stop y salida | Llenar toda la cartera de variantes de la misma exposición. |
| Mean reversion | Alejamiento extremo, condición de vuelta, orden y salida coherentes | Un oscilador por sí solo no define reversión. |
| Pullback | Estado de tendencia y retroceso contra ella | Confundirlo con comprar una caída sin filtro de régimen. |
| Momentum/trend | Evento de aceleración o estado de tendencia | Distinguir cruce de permanencia y no duplicar breakout con otro nombre. |
| Squeeze/expansión | Compresión previa y evento de expansión | Filtro de volatilidad sin disparador no identifica la hipótesis. |
| Fade/false breakout | Ruptura fallida y reingreso | Signo de nivel/margen puede requerir plantilla adicional. |
| Sesión/calendario | Rango/horario y racional del efecto | Pocos eventos, costes de sesión y validación mal adaptada. |

Añadir short o H4 es un eje distinto; no reemplaza comprobar el mecanismo y la contribución conjunta al portfolio.

## Actualización: evidencia directa del administrador

La revisión adicional de [[IMOX - IA y Building Blocks - Cambio de enfoque de Aritz]] encontró instrucciones escritas de IMOX para Random, bloques calibrados/acotados y tandas de minutos. Esto es una referencia más directa de la orientación del administrador que la guía comunitaria o ejemplos genéticos personales. No prueba que el curso completo nuevo se haya revisado ni que genética no pueda funcionar. Ruta práctica actual: [[IMOX - Empezar con SQX 144 - Metodología y primera campaña]].

## Contradicciones y decisiones pendientes

- **Todos los bloques frente a familias:** Builder y la guía 144 contienen ambos enfoques; la adenda de la guía recomienda familias. Comparar alternativas con presupuesto equivalente, en lugar de declarar resuelto el debate.
- **Filtrar correlación pronto:** reduce coste, pero puede eliminar una variante robusta antes de saberlo. Separar duplicado exacto, misma firma y parecido estadístico; conservar razones y medir falsos descartes.
- **Compatibilidad de volumen:** el fallo de exportación de AnchoredVWAP tiene corrección reportada; la calidad/semántica del volumen CFD es otra pregunta y no queda arreglada por compilar.
- **OOS y año oculto:** cuando alimentan decisiones o iteraciones del agente pasan a formar parte de selección. El siguiente experimento necesita una evaluación realmente independiente.
- **Catálogo y capacidades:** falta export actual de la instalación de Rodrigo para producir presets fiables; este recurso no lo inventa a partir de PDFs.

## Evidencia y provenance

- [Skill de selección de Building Blocks en Circle](https://comunidad.imoxtrading.com/c/aportes-ia/building-blocks-skill).
- [Guía de piezas SQX 145 en Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/guia-de-building-blocks-de-sqx-145).
- [Tipos de estrategia en Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/tipos-de-estrategia-en-trading-algoritmico).
- Los enlaces a fichas anteriores resuelven a sus notas source, con la URL de cada post.
- Relación metodológica IMOX→Forge y objetivo de nuevas campañas: instrucción expresa de Rodrigo en esta conversación, 2026-10-24.

## Límites y contradicciones

Investigación documental y propuesta de contrato. La auditoría de Forge, la creación de la skill propia y la ejecución de campañas son trabajos posteriores que requieren definir el experimento y verificar el estado actual del sistema. Los umbrales y resultados de miembros no se convierten en policy de Rodrigo.

## Actualización documental 2026-10-26

[[IMOX - Metodología para investigación Forex y CFD]] integra los estudios nuevos de octubre, distingue orientación de Aritz de experimentos de miembros y conserva decisiones aún no resueltas para Forge. [[IMOX — Revisión 2026-10-26 - Actualización de octubre]] documenta inventario y límites. Esta ampliación no revalida todos los datos antiguos ni modifica el pipeline técnico.
