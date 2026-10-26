---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - IA y Building Blocks - Cambio de enfoque de Aritz]]'
- '[[IMOX - Fuente - SQX 144 - Builders cortos y filtros baratos]]'
- '[[IMOX - Fuente - SQX - Point value y comprobación monetaria]]'
- '[[IMOX - Fuente - Ventanas móviles de 24 meses y estabilidad temporal]]'
- '[[IMOX - Fuente - SQX automatizado - Hipótesis, sondas y ejecución]]'
- '[[IMOX - Fuente - Building Blocks Skill]]'
- '[[IMOX - Fuente - Actualizar Broker Profiles en SQX]]'
- '[[IMOX - Fuente - Guía SQX 144 - Conocimiento de Telegram]]'
last_verified: '2026-10-24'
confidence: high
aliases: []
tags:
- kind/resource
- area/trading
- topic/imox
- topic/sqx144
created: '2026-10-24'
updated: '2026-10-26'
source_url: https://comunidad.imoxtrading.com/c/aportes-ia/ia-building-blocks
related:
- '[[IMOX]]'
- '[[30-resources/applications/echo/echo-forge]]'
---

# IMOX - Empezar con SQX 144 - Metodología y primera campaña

## Síntesis vigente

**El primer cambio es diseñar qué ventaja se busca y acotar su búsqueda antes de gastar máquina.** En las respuestas escritas de Aritz consultadas en Circle recomienda calibrar y acotar builders por hipótesis, usar Random en ese flujo y generar tandas pequeñas de minutos. La skill sirve para producir esa especificación y sus presets; no sustituye investigar la hipótesis ni validar lo generado.

Esta revisión amplía la biblioteca anterior con cinco posts. Se consultaron las listas de Strategy Quant 144 y Aportes IA y se seleccionaron las publicaciones relevantes; no se auditó toda la comunidad ni se revisaron todas sus grabaciones oficiales.

## Punto de partida de Rodrigo

Declarado el 24 de octubre de 2026: pasó de SQX 136 a 142 hace aproximadamente dos meses, recientemente a 144, mantiene su metodología anterior y todavía no construyó en esta nueva etapa. No se deduce de eso qué filtros exactos, datos o parámetros tiene configurados hoy. El objetivo inmediato es preparar nuevas campañas y una skill de SQX; no cambiar sistemas en producción.

## Qué está haciendo la comunidad ahora

| Evidencia | Qué muestra | Cómo usarla |
|---|---|---|
| [[IMOX - IA y Building Blocks - Cambio de enfoque de Aritz]] | Aritz propone Random, calibración, hipótesis acotadas y minutos por builder; critica perseguir volumen. | Referencia principal escrita para orientar el cambio metodológico. |
| [[IMOX - Building Blocks Skill]] | Carlos convierte activo/TF/dirección/familia en preset `.sqb` y explicación usando un catálogo real. | Herramienta de preparación, no prueba de rentabilidad. |
| [[IMOX - SQX 144 - Builders cortos y filtros baratos]] | Xavi usa una hora/15–30 aceptadas y genética con 120 generaciones. | Alternativa personal; no mezclar sus cifras con la receta de Aritz. |
| [[IMOX - Builder - Minería de estrategias]] | Edgar combina múltiples builders, firmas de bloques y análisis temporal. | Aprender a medir variedad y coste de selección. |
| [[IMOX - Claude en CustomProjects para analizar databanks]] | Jose2ms inserta un selector IA con validación determinista antes de robustez. | Automatización adicional cuando ya existe una cadena funcional. |
| [[IMOX - SQX automatizado - Hipótesis, sondas y ejecución]] | Francisco prueba hipótesis con criterios previos y separa razonamiento de vigilancia por scripts. | Evitar gastar campañas en tesis no contrastadas o confundir proceso vivo con progreso. |

No toda la comunidad migró al mismo método. La propuesta de Aritz y las variantes genéticas coexisten. El audio del administrador y los módulos de formación mencionados no se revisaron en esta comprobación, por lo que no se presenta una reconstrucción completa del curso nuevo.

## Qué cambia respecto de seguir igual tras la migración

- **Identidad de la búsqueda:** pasar de pedir muchas EAs a declarar familias y configuraciones concretas. Acumular EAs parecidas no garantiza diversificación.
- **Uso de IA:** aprovecharla para especificar y generar configuraciones compatibles, procesar datos mediante código y conservar evidencia; no creer una justificación de indicador sin medirla.
- **Presupuesto:** limitar cada prueba, aceptar que una hipótesis no produzca y cambiar de prueba. No relajar filtros repetidamente para fabricar un éxito.
- **Evaluación:** mirar IS/OOS, distribución temporal, degradación y contribución conjunta además del ranking global.
- **Automatización:** encadenar tareas después de comprobar una ejecución pequeña completa. La vigilancia de Forge/scripts no necesita un chat consumiendo tokens todo el día.
- **Migración técnica:** revisar ATR, instrumento, costes, sesiones y exportadores en el build real. Las diferencias 136→144 de una guía no dicen qué cambió justo en el salto 142→144 de Rodrigo.

## Orden concreto para empezar

### 1. Dejar una base 144 confiable

Registrar build exacto, motor destino, broker/servidor y símbolo. Mantener una configuración antigua de referencia antes de editar. Actualizar instrumentos y sesiones con el procedimiento de [[IMOX - Actualizar Broker Profiles en SQX]]. Revisar contrato, tick/pip, point value, lote mínimo/paso, moneda, horario, timezone/DST, comisión, spread y swap.

Control de salida: una operación conocida produce el P/L esperado para su dirección y costes, y puede reconciliarse con MT5. Ver [[IMOX - SQX - Point value y comprobación monetaria]]. Un PF bonito no detecta necesariamente escala monetaria errónea.

La guía comunitaria indica que en 144 ya no corresponde el multiplicador histórico ×10 del ATR. Revisar la configuración heredada y comprobar el comportamiento del indicador en el build actual; no cambiar todos los ATR a un mismo número por esta afirmación.

### 2. Preparar entradas reales para la skill

Exportar desde **esa instalación 144**:

- Un `.sqb` con todos los bloques activados como catálogo y plantilla estructural. Es un insumo de documentación; **no** significa minar con todos activos.
- Un `.cfx` de referencia si se quiere que la skill configure todo el Builder/Custom Project. No se asume que ya existe uno validado.
- Configuración del instrumento, split de datos y criterios de validación que se van a utilizar.

No hace falta ese export para comprender la metodología; sí hace falta para entregar un preset importable de la instalación de Rodrigo sin inventar IDs.

### 3. Definir una primera comparación pequeña

Propuesta de esta revisión: un instrumento, una temporalidad y una dirección, con pocas hipótesis diferenciadas. Elegir por interés y huecos de cobertura, no porque un indicador esté de moda. Ejemplos de hipótesis: ruptura, reversión y pullback; son ilustrativos, no una selección aprobada de campañas.

Por cada hipótesis escribir: comportamiento esperado, régimen donde tiene sentido, orden/disparador, filtro, horizonte, salidas, rangos a explorar y qué resultado hará descartarla. Presupuesto, máximo de candidatas y criterios se fijan antes de ver resultados. El modo Random acotado es el punto de partida recomendado aquí por cercanía a la indicación escrita de Aritz; una comparación con genética es otro experimento.

No convertir máximo 100 o menos de diez minutos del comentario en un gate universal. Son referencias de escala. El presupuesto real depende de máquina, activo, frecuencia y objetivo y debe quedar registrado.

### 4. Probar que la configuración hace lo que dice

Importar y revisar los bloques seleccionados, su semántica y parámetros. Verificar orden y signo de nivel/margen; la guía 145 advierte que el `.sqb` no fija toda la lógica de órdenes pendientes. Si hace falta plantilla, declararlo y usar una compatible con 144.

Generar un ejemplo mínimo exportable y compilarlo en el motor destino. Revisar compatibilidad AnchoredVWAP/parches por build y significado del volumen del feed. No habilitar todos los bloques de 145 porque un PDF los enumera.

### 5. Ejecutar una sonda y recién después ampliar

En la sonda guardar configuración, presupuesto, intentos, aceptadas, tiempo y motivos de rechazo. Si no produce, diagnosticar datos, filtros y lógica por separado; registrar el cambio antes de repetir. Un databank vacío puede ser incompatibilidad o restricción imposible, no prueba automática de que el activo carece de edge.

La salida buscada de la primera sonda es saber si el experimento funciona y merece más presupuesto; no tener inmediatamente una EA para real.

### 6. Validar la cadena antes de multiplicar campañas

Con pocas candidatas completar la secuencia de robustez/retetests, optimización/estabilidad y contraste SQX→MT5 que se haya definido. La comunidad menciona MC1/MC2 y nuevos módulos, pero esta revisión no obtuvo una plantilla oficial completa de la nueva cadena ni sus umbrales: no se inventan como si fueran metodología verificada.

Toda consulta al OOS o año oculto que cambia selección o propuestas del agente participa en entrenamiento/selección del proceso. Separar una evaluación final que no lo haya guiado. Analizar ventanas y años evita que una cifra total esconda periodos enteros débiles; ver [[IMOX - Ventanas móviles de 24 meses y estabilidad temporal]].

### 7. Integrar con Forge y escalar

Cuando la sonda y la cadena pequeña funcionen, registrar presets/hipótesis con identidad estable y preparar la campaña de Forge. Esta revisión no audita si Forge ya soporta el modo/configuración nueva ni cambia su pipeline por inferencia. El mapeo concreto metodología→config→ejecución se verifica en su propio trabajo técnico.

## Skill entregada y alcance

[[30-resources/agents/skills/sqx144-campaign-design/SKILL.md|sqx144-campaign-design]] prepara la hipótesis, clasifica fuentes y devuelve especificación, faltantes y plan de sonda. Si recibe catálogo/config reales puede guiar la creación y revisión de presets. No contiene un export de Rodrigo, no se declara probada contra SQX y no inicia minados sin una instrucción concreta de ejecución.

## Qué falta ahora mismo

No constan todavía en esta conversación: build exacto de 144, instrumento/broker de la primera campaña, destino MT4/MT5, export `.sqb`, `.cfx` de referencia y plantilla oficial de la nueva cadena. Se pueden diseñar hipótesis mientras se obtienen, pero no certificar compatibilidad ni cerrar una campaña ejecutable.

El primer entregable práctico es un paquete pequeño: ficha de hipótesis + preset de esa instalación + configuración versionada + una sonda con evidencia. Dejar la construcción de hubs y automatizaciones adicionales para cuando ayuden a ese flujo.

## Evidencia y provenance

- [Aritz: builders acotados y evitar genética en ese flujo](https://comunidad.imoxtrading.com/c/aportes-ia/ia-building-blocks#comment_wrapper_115862100).
- [Aritz: Random y minados de minutos](https://comunidad.imoxtrading.com/c/aportes-ia/ia-building-blocks#comment_wrapper_115864322).
- [Xavi: alternativa de builders cortos con genética](https://comunidad.imoxtrading.com/c/aportes-y-recursos/generando-estrategias-en-sqx-v144-sin-que-cada-bloque-dure-dias).
- Las fichas enlazadas resuelven a las notas fuente de Circle. Lectura web exclusivamente en Chrome, 2026-10-24.
- Estado personal y objetivo: solicitud directa de Rodrigo en esta conversación.

## Límites y contradicciones

Se trata de investigación documental y una propuesta de arranque. No se ha inspeccionado ni ejecutado SQX de Rodrigo, escuchado el audio o completado la formación oficial nueva, y no se inventan umbrales faltantes. La recomendación de comenzar por Random se atribuye a evidencia escrita del administrador; no se presenta como superioridad estadística demostrada sobre genética.

## Actualización documental 2026-10-26

[[IMOX - Metodología para investigación Forex y CFD]] integra los estudios nuevos de octubre, distingue orientación de Aritz de experimentos de miembros y conserva decisiones aún no resueltas para Forge. [[IMOX — Revisión 2026-10-26 - Actualización de octubre]] documenta inventario y límites. Esta ampliación no revalida todos los datos antiguos ni modifica el pipeline técnico.
