---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - IA y Building Blocks - Cambio de enfoque de Aritz]]", "[[IMOX - Fuente - Building Blocks Skill]]", "[[IMOX - Fuente - Tipos de estrategia en trading algorítmico]]", "[[IMOX - Fuente - Actualizar Broker Profiles en SQX]]", "[[IMOX - Fuente - SQX - Point value y comprobación monetaria]]", "[[IMOX - Fuente - Claude en CustomProjects para analizar databanks]]", "[[IMOX - Fuente - Builder - Minería de estrategias]]", "[[IMOX - Fuente - Acceso VDS por WireGuard]]", "[[IMOX - Fuente - Manual de psicología para traders]]", "[[IMOX - Fuente - Seminario 30 de octubre - Repaso 136 a 144]]", "[[IMOX - Fuente - Cartera estable - Ventaja frente a azar y selección]]", "[[IMOX - Fuente - Gestión variable - Martingala H1 de Ramon]]", "[[IMOX - Fuente - Piramidación - Comparación a igual riesgo]]", "[[IMOX - Fuente - FOMO - Plan y decisiones trazables]]", "[[IMOX - Fuente - Gestión variable - Error de timeframe y límite de lotes]]", "[[IMOX - Fuente - MetaTrader móvil - Observar sin intervenir]]", "[[IMOX - Fuente - Robustez entre brokers - Estudio de 189 estrategias]]", "[[IMOX - Fuente - Axi por etapas - Sizing y exposición conjunta]]", "[[IMOX - Fuente - Capacidad SQX - Comparar bloques equivalentes]]", "[[IMOX - Fuente - FTMO - Recuperación con escalera de riesgo]]", "[[IMOX - Fuente - Incubación masiva - Experimento de Tony]]", "[[IMOX - Fuente - Tailscale sin login - Recuperación por IPMI]]", "[[IMOX - Fuente - Índice general de Zona de Aportes]]", "[[IMOX - Fuente - Automatizar SQX con sqcli - Experimento 143]]", "[[IMOX - Fuente - Panel de EAs - Comparación del custom con MT5]]", "[[IMOX - Fuente - Evento Repaso 136 a 144 del 30 de octubre]]"]
last_verified: "2026-10-26"
confidence: "high"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox", "topic/methodology"]
created: "2026-10-26"
updated: "2026-10-30"
related: ["[[IMOX]]", "[[Estrategias IMOX — Forex y CFD con Echo Forge]]"]
---

# IMOX - Metodología para investigación Forex y CFD

## Síntesis vigente

La definición de trabajo para [[Estrategias IMOX — Forex y CFD con Echo Forge]] es un proceso de investigación: formular hipótesis acotadas, construir búsquedas compatibles con el instrumento real, generar candidatas, someterlas a selección y robustez, comprobar ejecución, y evaluar su contribución a una cartera con seguimiento trazable. Esta es una síntesis documental personal con fuentes iniciales al 26 de octubre de 2026 y delta explícito al 30 de octubre; no una transcripción certificada de toda la formación oficial ni una validación de Forge.

La orientación escrita de Aritz en [[IMOX - IA y Building Blocks - Cambio de enfoque de Aritz]] prioriza Random, indicadores calibrados, builders acotados y tandas de minutos. La incubación masiva 142, la genética amplia, la selección IA y los esquemas de riesgo de otros miembros son variantes con objetivos y evidencias diferentes. La comunidad contiene desacuerdos; no hay una única receta inferible de sumar sus parámetros.

## Autoridad de las fuentes

| Capa | Evidencia | Alcance |
|---|---|---|
| Orientación directa de IMOX/Aritz | Comentarios escritos sobre builders Random; anuncio de repaso 136→144 y opinión sobre observación móvil. | Atribuir exactamente lo escrito; audio, curso y seminario no revisados íntegramente. |
| Investigación de miembros | Estudios multibroker, azar/selección, piramidación, incubación y MM. | Hipótesis y resultados declarados en sus muestras; no política de Rodrigo. |
| Propuesta de esta síntesis | Secuencia y preguntas para preparar una investigación trazable con Forge. | Requiere decisión y verificación técnica al empezar el proyecto; aquí no se ejecuta. |

## Secuencia de trabajo propuesta

### 1. Especificar la hipótesis y el instrumento

Fijar activo, broker/símbolo/producto, timeframe, dirección, régimen esperado, mecanismo de entrada, orden y salida. Distinguir familia de lógica de tipo de orden: cambiar indicadores o añadir short no prueba diversificación. Utilizar catálogo/export real de la instalación objetivo; una guía 145 no acredita IDs, parámetros ni exportador de 144. Registrar contrato, tick/pip/point value, costes, sesiones, timezone y DST antes de interpretar métricas.

### 2. Generar para aprender, con presupuesto previo

Usar como punto de partida la orientación escrita de Aritz: búsquedas pequeñas y calibradas por hipótesis, Random y presupuesto acotado. Registrar preset/configuración, candidatos, rechazos y coste. Los máximos de 100 o ejemplos de menos de diez minutos explican escala; no se convierten en umbrales universales. La productividad se compara con el mismo bloque y carga entre máquinas, como propone [[IMOX - Capacidad SQX - Comparar bloques equivalentes]]. Una búsqueda vacía pide diagnóstico, no relajar automáticamente criterios hasta obtener un resultado agradable.

### 3. Seleccionar y probar sin ocultar el uso de datos

Separar dato usado para construir, filtrar, ajustar y evaluar. OOS y año oculto dejan de ser examen independiente cuando sus resultados deciden supervivencia o futuras propuestas del agente. La selección IA de [[IMOX - Claude en CustomProjects para analizar databanks]] consulta OOS: sirve como filtro, con validación determinista e identidad completa, pero participa en selección. Los costes de retest y falsos descartes tempranos deben medirse; la correlación antes de robustez sigue siendo un tradeoff abierto.

[[IMOX - Cartera estable - Ventaja frente a azar y selección]] agrega una propuesta experimental: contrastar contra azar con exposición comparable y ensayar en historia no usada. El PDF distingue cinco resultados: pasa, no pasa, no concluyente, no fiable y sin datos. Falta de potencia no equivale a refutación. Sus ventanas, t, réplica mínima y Bonferroni son parámetros de ese estudio, no gates adoptados por Rodrigo. La t presupone independencia y el propio autor pide contrastar dependencia temporal; el tramo limpio también se consume si guía nuevas decisiones.

### 4. Comprobar reproducción y condiciones de ejecución

Contrastar SQX→MT5 con mismo código, parámetros, producto, fechas, sesiones, dinero y costes. Investigar discrepancias trade a trade; una media global de concordancia no certifica equivalencia. [[IMOX - Robustez entre brokers - Estudio de 189 estrategias]] propone repetir con el broker de destino y controlar barras/horarios/calidad del feed; su referencia está favorecida por la selección original. Copiar señales puede reducir diferencia de señal, pero conserva costes y ejecución del destino.

El caso [[IMOX - Gestión variable - Error de timeframe y límite de lotes]] muestra que una curva no detecta EA en TF equivocado ni órdenes rechazadas por volumen. La supervisión debe comprobar que los EAs operan realmente y que rechazos, instancias detenidas o falta de margen no se confundan con ausencia de señal.

### 5. Evaluar cartera y gestión monetaria como preguntas distintas

Medir solapamiento de exposición, pérdidas simultáneas, drawdown conjunto y comportamiento en distintos tramos, además de correlación y métricas globales. Una mezcla de buenas curvas no prueba estabilidad, y muchas EAs beta pueden concentrar la misma apuesta. Comparar contra benchmarks adecuados al tiempo expuesto y al riesgo; un control con duración conocida a posteriori sirve para diagnóstico, no es una estrategia operable.

[[IMOX - Piramidación - Comparación a igual riesgo]] exige comparar variantes con el mismo presupuesto de riesgo y entradas emparejadas. Sus resultados negativos tienen alcance CFD, mercados, fechas, reglas y costes concretos; no prohíben universalmente otra piramidación. Igual riesgo inicial tampoco asegura igual exposición temporal ni drawdown.

No mezclar tres mecanismos: la martingala ×1,40 de [[IMOX - Gestión variable - Martingala H1 de Ramon]], la duplicación tras perder del caso de errores y la escalera por saldo de [[IMOX - FTMO - Recuperación con escalera de riesgo]]. Ninguno fue aprobado aquí. Evaluar riesgo flotante, límites de broker, dependencia entre cuentas, fallbacks y órdenes ya colocadas forma parte de cualquier estudio de MM; cifras de recuperación de una muestra no son pronósticos.

### 6. Seguir el proceso sin intervenir por impulso

Conservar identidad hipótesis→campaña→configuración→EA→retest→ejecución→observación y motivos de descarte. Revisar resultados y estados operacionales según un plan previo. El post de [[IMOX - MetaTrader móvil - Observar sin intervenir]] conserva el matiz de Aritz: observar puede enseñar; acceso inversor permite observar sin modificar órdenes. No convertir quitar el móvil en doctrina. [[IMOX - FOMO - Plan y decisiones trazables]] y [[IMOX - Manual de psicología para traders]] aportan disciplina, no nuevos umbrales estadísticos.

## Qué queda por definir antes de ejecutar con Forge

| Decisión o evidencia | Qué falta resolver en el proyecto |
|---|---|
| Base técnica | Build real SQX, motor MT4/MT5, catálogo `.sqb`, configuración `.cfx`, datos, producto y costes vigentes. |
| Cadena oficial | Formación nueva y umbrales completos de retester/MC/optimización; no reconstruirlos desde comentarios o capturas de miembros. |
| Protocolo experimental | Presupuesto, criterios previos, rol de cada split, control de pruebas múltiples y evaluación que no guíe iteraciones. |
| Equivalencia con Forge | Verificar qué implementa hoy y qué sólo es propuesta documental. Esta ingesta no inspeccionó repos, workers ni runtime. |
| Criterio de cartera/MM | Objetivo y restricciones propias por vehículo, con evidencia de ejecución y exposición conjunta; no copiar porcentajes comunitarios. |

Ruta detallada de arranque: [[IMOX - Empezar con SQX 144 - Metodología y primera campaña]]. Contrato de presets: [[IMOX - Building blocks y preparación de campañas Forge]]. [[IMOX - Seminario 30 de octubre - Repaso 136 a 144]] es una oportunidad futura de completar formación, no evidencia ya disponible al corte.

## Evidencia y provenance

Las notas `source` del frontmatter resuelven a Circle y a sus PDF adjuntos. Revisión incremental: [[IMOX — Revisión 2026-10-26 - Actualización de octubre]]. Las fuentes históricas conservan su fecha real anterior; leer una síntesis hoy no equivale a revisitar todos sus posts.

## Límites y contradicciones

No existe cobertura global certificada de Circle, sus chats, clubes privados o Academia. Las fuentes nuevas conservan medios y respuestas pendientes; el manual MPPT se revisó de forma dirigida. Los PDFs son copias personales de acceso restringido, sin redistribución. No se ejecutaron minados, pruebas de rentabilidad, cambios de software, riesgo ni operaciones de trading. Las propuestas de esta página son material de investigación para el proyecto, sin aprobación implícita de estrategia o MM.

## Actualización de fuentes — 2026-10-30

La ruta oficial ahora incorpora [[IMOX - Índice general de Zona de Aportes]] y cuatro índices fijados actualizados en sus locators originales. Son herramientas de descubrimiento, con curaduría por interacción; no validan cada afirmación que destacan ni sustituyen la formación.

[[IMOX - Automatizar SQX con sqcli - Experimento 143]] añade una propuesta personal para build 143. Los comentarios de Aritz remiten explícitamente a los fallos de GUI sqcli y a la automatización nocturna ya documentados. El documento adjunto está pendiente de login/descarga; no se puede certificar su receta ni adaptarla a 144 desde el título.

La discusión de [[IMOX - Cartera estable - Ventaja frente a azar y selección]] amplía el control de calidad del test: además de no detectar ventaja donde no existe, comprobar su capacidad para detectar una ventaja conocida. Hay desacuerdo sobre construir ese control sintético de forma independiente; no es un método ya implementado. No convertir popularidad o nuevos comentarios en validación experimental.

[[IMOX - Seminario 30 de octubre - Repaso 136 a 144]] pasó de futuro a finalizado según Circle. Aritz afirma que queda grabado; no se observó locator ni se revisó el contenido. La cadena oficial y sus umbrales continúan pendientes de contraste.

El hallazgo histórico [[IMOX - Panel de EAs - Comparación del custom con MT5]] refuerza la pregunta de equivalencia entre motores y selección para demo, pero sus cuatro imágenes siguen pendientes de lectura completa. [[IMOX - Tailscale sin login - Recuperación por IPMI]] es continuidad operacional atribuida a un miembro, sin adopción de sus cambios de seguridad.

Revisión: [[IMOX — Revisión 2026-10-30 - Actualización incremental]]. Descargas: [[IMOX — Descargas pendientes]].
