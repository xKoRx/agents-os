---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - Mi base de datos para analizar resultados]]'
last_verified: 2026-10-24
confidence: verified
aliases: []
tags:
- kind/resource
- area/trading
- topic/imox
created: '2026-10-24'
updated: '2026-10-26'
---

# IMOX - Base de datos para analizar resultados

## Síntesis vigente

Jorge PF presenta una aplicación personal que centraliza el trabajo posterior a StrategyQuant X (SQX): catálogo de minados y estrategias, ejecución e importación de backtests MT5, seguimiento demo y comparación demo versus backtest del mismo periodo. Su valor principal es la trazabilidad entre esas etapas y la reducción de carga manual. El autor la considera operativa, con comparadores y portfolio todavía en evolución.

**Advertencia de interpretación:** todas las cifras y estrategias de las siete capturas proceden de una copia con datos aleatorios generados para mostrar la interfaz. No representan resultados reales. La revisión verifica lo que se publicó, no el funcionamiento del software ni su rentabilidad.

## Contexto y problema que resuelve

El autor llevaba meses registrando minados y EAs seleccionados manualmente en Access. El trabajo era tedioso, se aplazaba y su conocimiento de bases de datos no le permitía construir una interfaz cómoda. Con ayuda de Claude construyó una app para editar la base, importar información automáticamente y analizar demos y backtests. Bromea con llamarla «Jorghub»; no se presenta un nombre definitivo ni un producto distribuido.

La plataforma cubre la actividad posterior a SQX, no sustituye el minado. Los paneles comparten una base de datos; no son listas aisladas.

## Modelo de información y trazabilidad

| Entidad o catálogo | Información descrita u observada | Relación o uso |
|---|---|---|
| Minados | Código, fecha, símbolo, temporalidad, dirección, estados Builder/Retester/Optimizer/Revisión/Backtesteado, fuente de datos, terminal, comentarios | Origen de las estrategias; es la tabla que el autor edita habitualmente. |
| Estrategias | Identificador propio, minado de origen y nombre asociado a los archivos `.mq5` | Une backtests, clasificación y seguimiento. |
| Backtests | Resultados MT5, periodo y configuración | Permite selección, detalle y comparación. |
| Demos | Historial enviado desde terminales MT5 a una VDS mediante un EA | Seguimiento actualizado de estrategias por broker y terminal. |
| Backtests «WF» | Backtests del periodo demo, con el mismo broker y configuración | Contraste entre ejecución demo y simulación del mismo intervalo. |
| Catálogos auxiliares | Brokers, símbolos, tipos de estrategia, tipos de entrada, temporalidades y direcciones | Evitan que los paneles interpreten de forma distinta las mismas entidades. |

La captura de tablas muestra pestañas Minados, Estrategias, Brokers, Símbolos y Tipos y listas. No publica el esquema físico, claves, restricciones, motor de base de datos ni modelo de sincronización. Access es el antecedente; no está confirmado como motor actual.

## Flujo de backtests e importación

1. Exportar o disponer de las EAs de SQX en una carpeta.
2. Pulsar «Nuevo backtest» y seleccionar carpeta, minado, terminal MT5 y otras variables que el post no detalla.
3. La app ejecuta los backtests y muestra una tabla para decidir qué estrategias conservar o descartar.
4. Al importar, registra las estrategias, asigna ID, crea sus registros de backtest y edita los `.mq5` para alinear su nombre con la base.
5. Abrir una estrategia para ver curva, información adicional y rendimientos mensuales.
6. Enviar una selección al comparador para superponer curvas, calcular correlaciones y explorar el comportamiento conjunto.

El horizonte habitual de backtest es el mismo cubierto por la estrategia en SQX, generalmente cinco u ocho años según el autor. La interfaz llama al panel inicial «backtests en bruto (solo backtest, sin comparación SQX)»: no debe interpretarse como una conciliación automática SQX versus MT5.

## Paneles y evidencia visual

| Panel | Capacidad descrita y observada | Límites |
|---|---|---|
| 1. Backtests | Tabla con código, estrategia, símbolo, TF, dirección, valoración, desempeño en bajista, tipo, entrada, trades anuales, beneficio neto, drawdown máximo y Calmar; detalle con curva y tabla mensual. Se ven filtro por nombre/minado, exportación CSV y envío al comparador. | La valoración y «En bajista» son manuales y subjetivas. |
| 2. Comparador | Superposición de curvas, correlaciones y pestaña Portfolio. Se ven selección/importación por minado o símbolo, rango de fechas y sesiones guardadas. | El portfolio está especialmente inmaduro; no se detallan ponderación ni agregación de riesgo. |
| 3. Demo | Resultados por estrategia con broker, símbolo, temporalidad, curva, operaciones y métricas; detalle de curva y rendimientos mensuales. Se ven filtros por broker/terminal, exportación CSV y carga de backtest. | El autor quiere revisar qué columnas mostrar, incluido el magic number. |
| 4. Backtests WF | Lanza pruebas de las EAs en demo con igual configuración, broker e intervalo registrado. | Descrito en texto; no hay una captura independiente de este panel entre las siete imágenes. |
| 5. Demo vs WF | Curvas superpuestas y comparación de número de operaciones, beneficio neto, drawdown máximo, profit factor y winrate; columnas Demo, Backtest y diferencia; indicadores de concordancia y correlación. | La fórmula de concordancia no está publicada y al autor no le satisface todavía. |
| 6. Comparador demo | Compara varias demos con curvas, cálculo de correlaciones y pestaña Portfolio; selección por estrategia, fechas y sesiones. | Las demos del autor tienen como máximo cuatro meses desde su paso a MT5. |
| Estadísticas | Previsto: contar minados y estrategias por símbolo, distribución de tipos y resultados por tipo. | Pendiente de construcción; la pestaña visible no demuestra implementación. |

### Qué añaden las siete imágenes

1. Vista general de backtests: confirma navegación por seis paneles, estadísticas y tablas; permite ver campos y controles que el texto no enumera.
2. Tablas de fondo: revela los estados de las etapas del minado y su fuente de datos/terminal. Los activos, fechas y registros son ejemplos ficticios.
3. Detalle de backtest: curva de equity, señalización de drawdown/estancamiento, métricas complementarias y rendimientos mensuales con resumen anual.
4. Comparador de backtests: curvas superpuestas, fechas, gestión de sesiones y zona para correlaciones.
5. Seguimiento demo: filtros por broker/terminal, métricas y detalle desplegado con curva y tabla mensual.
6. Demo vs WF: aporta el desglose concreto de métricas y diferencias junto a concordancia y correlación. Sus porcentajes son ilustrativos, no objetivos de aceptación.
7. Comparador demo: confirma el esquema de selección, curvas y correlaciones aplicado al historial demo.

Las capturas se revisaron visualmente ampliadas. Los textos pequeños no permiten una transcripción exhaustiva y fiable de cada celda; se extraen controles y campos legibles, sin inventar fórmulas ni convertir cifras ficticias en evidencia.

## Criterios del autor y límites metodológicos

- «Valoración» expresa si una estrategia le gusta; «En bajista» valora cómo se comportó durante 2022. Esa etiqueta se refiere al periodo elegido por el autor, no a una clasificación objetiva de todos los mercados bajistas.
- La hipótesis del autor es que una buena coincidencia demo/backtest del mismo periodo da confianza sobre la fidelidad del backtest histórico largo. El post no demuestra esa extrapolación.
- «WF» es el nombre usado por el autor para este backtest de seguimiento. No describe ventanas móviles, reoptimización ni separación de entrenamiento y prueba; no se puede afirmar que implemente una metodología walk-forward completa.
- No hay definición de concordancia, serie usada para correlacionar, frecuencia de muestreo, tratamiento de posiciones abiertas, comisiones, swaps, spread, slippage, zona horaria, huecos o ticks. Son preguntas abiertas, no fallas comprobadas.
- No se comparte código, instalador, repositorio, esquema de datos, guía de despliegue ni enlace de descarga de la app. Los adjuntos revisados son imágenes.

## Comentarios y respuestas

Se desplegaron las respuestas y el comentario con «Ver más». Quedaron visibles los ocho comentarios que anuncia Circle. Había 18 reacciones al post al revisar; es una señal de recepción, no una validación técnica.

| Comentario | Información relevante | Tratamiento |
|---|---|---|
| [Luciano]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118110103 ) | Felicita al autor y destaca utilidad para acompañar métricas. | Recepción positiva, sin detalle técnico adicional. |
| [Ricardo]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118112962 ) | Cuenta su migración de MT4 a MT5, conversión de biblioteca de EAs y reinicio de Darwins; describe mejor interacción con SQX/IA e inconsistencias que experimentaba en MT4. | Experiencia personal; no benchmark ni prueba de superioridad universal. |
| [Miguel, pregunta]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118173279 ) | Pregunta cómo se reinicia un Darwin y qué ocurre con asignaciones compradas. | Abre un tema lateral de condiciones de cuenta. |
| [Ricardo, respuesta]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118173437 ) | Afirma que el reinicio pierde antigüedad/track record, crea otro Darwin en calibración y cobra un mes; expresa duda sobre asignaciones compradas. | Afirmaciones comunitarias sin verificación oficial en esta ingesta. |
| [Miguel, réplica]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118174397 ) | Decide seguir con MT4 por sus asignaciones existentes. | Muestra una restricción práctica de migración; se omiten montos personales innecesarios. |
| [Ricardo, adjunto]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118175242 ) | Aporta una foto de una conversación con «Darwinex Zero AI». La respuesta del chatbot dice que reiniciar elimina asignaciones permanentes compradas, activadas o no, y que para conservarlas debe mantenerse el Darwin correspondiente. | Se leyó la foto. Es evidencia de una respuesta de chatbot, no confirmación de política contractual vigente. |
| [Asier]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118126507 ) | Quiere hacer algo similar y señala que priorizará ideas. | Señal de interés en construir herramientas propias. |
| [José Matías]( https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados#comment_wrapper_118152742 ) | Agradece y comenta que le dio ideas. | Recepción positiva, sin información técnica nueva. |

El hilo lateral de Darwinex se conserva por relevancia contextual. Sus condiciones requieren consulta oficial antes de tomar una decisión; aquí no se adoptan como reglas verificadas.

## Valor para Rodrigo y posibles aportes

Evaluación de esta ingesta: **alto valor como referencia de organización y trazabilidad; valor insuficiente como software reutilizable o validación estadística**. No contiene una estrategia lista para operar.

Ideas derivadas para evaluar, sin asumir una implementación propia:

- Mantener una identidad estable desde el minado hasta cada versión del EA, ejecución de backtest y demo.
- Automatizar captura/importación para evitar que el catálogo quede abandonado por carga manual.
- Comparar demo y simulación con broker, configuración y periodo alineados; conservar las diferencias por métrica para investigarlas.
- Separar clasificación subjetiva de métricas calculadas y documentar las fórmulas antes de usar umbrales.
- Priorizar catálogo/trazabilidad y contraste demo/backtest antes de invertir en un portfolio completo. Esta prioridad es análisis propio, no una instrucción del autor.

Preguntas que podrían aportar valor al hilo:

1. ¿Cómo define concordancia y sobre qué serie/frecuencia calcula la correlación?
2. ¿Cómo identifica un EA entre terminales y brokers, y cómo distingue versiones del mismo código?
3. ¿Qué condiciones fija para que demo y backtest sean comparables: costes, horario, ticks y posiciones abiertas?
4. ¿Cómo evita duplicados al importar historial y cómo maneja reinicios o terminales desconectadas?
5. ¿Planea compartir el esquema, una versión mínima o el EA de sincronización?

No se publicó ningún comentario. Estas preguntas son material para preparar un aporte posterior cuando Rodrigo lo solicite.

## Evidencia y provenance

- Fuente canónica: [[IMOX - Fuente - Mi base de datos para analizar resultados]].
- [Publicación de Jorge PF](https://comunidad.imoxtrading.com/c/plugins-627f40/mi-base-de-datos-para-analizar-resultados), espacio Herramientas/Plugins/Eas de IMOX en Circle.
- Revisión directa: 2026-10-24, mediante Chrome autenticado; cuerpo completo, siete imágenes del post y ocho comentarios, incluida la imagen de una respuesta.
- La interfaz mostraba «2 días» como antigüedad del post; no se convirtió a una fecha absoluta porque no se verificó el timestamp exacto.

## Límites y contradicciones

No se ejecutó ni auditó la app. No se comprobó el estado actual de políticas Darwinex ni se inspeccionaron otras publicaciones. Las capacidades se atribuyen al autor o a la interfaz observada; las sugerencias se distinguen como análisis propio. La duda del autor sobre concordancia permanece abierta.

## Delta observado el 2026-10-26

El cuerpo conserva la advertencia de datos ficticios. Ahora se observan 14 comentarios frente a ocho de la captura anterior; hay respuestas anidadas adicionales pendientes. No se certifican condiciones de reinicio de Darwinex desde testimonios de miembros. La revisita textual no renueva la verificación de todos los materiales previos.
