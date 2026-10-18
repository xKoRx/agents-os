# A. Resumen ejecutivo

La invocación actual de SQX 144 vía CLI (ejecutando directamente `/.../sqx/144/sqcli -project action=start name=custom`) **es correcta** según la documentación oficial. Los comandos CLI soportados en SQX incluyen categorías como `-data`, `-instrument`, `-symbol`, `-project`, `-tools`, `-databank`, `-extindicators`, `-run`, `-exit`, entre otros. En ninguno de estos comandos existe un parámetro explícito para controlar hilos o núcleos (no hay argumentos `threads`, `workers`, etc. en la documentación). 

No se han encontrado cambios significativos en el CLI de StrategyQuant X entre la versión 142 y 144. El changelog de 144 sólo menciona mejoras en el CLI de *Data Manager*, pero nada específico para el lanzador de SQX. La funcionalidad de la CLI (por ejemplo, arranque de proyecto con `-project action=start name=<proyecto>`) permanece igual. 

En cuanto a ejecutar mediante script o directamente, no hay en la documentación oficial un guión “oficial” (`run_sqcli.sh`) obligatorio. Por defecto se muestra `sqcli.exe` (o `sqcli` en Linux) ubicado en la carpeta de instalación. En Linux no hay mención de un wrapper proporcionado por el proveedor; cualquier `run_sqcli.sh` observado es probablemente creado por usuarios. Para verificarlo conviene inspeccionar cada host (buscando archivos por nombre, revisando timestamps y permisos) y comparar con la fecha de instalación o actualización oficial, en lugar de suponer que existe en todas las versiones.

**Conclusión:** La forma de invocar SQX 144 es correcta y completa según la guía oficial. No parece faltar ningún parámetro CLI documentado ni hay evidencia de diferencias de lanzamiento entre 142 y 144 que afecten paralelismo. Por lo tanto, la baja utilización de CPU observada **no se debe a la forma de invocar** el CLI, sino probablemente a cómo SQX distribuye internamente las tareas (p. ej. _CustomAnalysis_ secuencial). 

# B. Contrato de la CLI

La CLI de StrategyQuant X se usa lanzando el ejecutable `sqcli` (en Windows `sqcli.exe`, en Linux `sqcli`) desde la carpeta de instalación. Por ejemplo:

- **Modo no interactivo:** `sqcli -data action=update` actualiza todos los datos y termina.
- **Modo interactivo:** ejecutar `sqcli` sin parámetros abre un prompt interactivo en línea de comandos.
- **Sin encabezado:** todos los comandos internos se prefijan con guión. Por ejemplo, listar proyectos: `sqcli -project action=list`, listar símbolos: `sqcli -symbol action=list`, etc.

Los comandos principales documentados son:

- **`-data`**: gestiona datos (update, import, export, clone, timezones).
- **`-instrument`**: gestiona instrumentos (list/add/edit/delete).
- **`-symbol`**: gestiona símbolos (list/add/edit/delete, etc.).
- **`-databank`**: gestiona Databanks (list, save, load, copy, etc.).
- **`-project`**: gestiona proyectos internos (list/start/stop/pause/resume/status, etc.). Ejemplo: `sqcli -project action=start name=Builder` inicia el proyecto “Builder”.
- **`-tools`**: ejecuta utilidades (por ejemplo, exportar órdenes a CSV).
- **`-extindicators`**: a partir de Build 142 permite gestionar indicadores externos con múltiples valores (list/add/import).
- **`-gui`**: inicia un servidor web para la GUI (sin otros argumentos).
- **`-run`**: ejecuta varios comandos en lote cargándolos de un archivo.
- **Otros comandos**: `-execute`, `-deletefile`, `-waitfor`, `-exit`, etc. según la documentación CLI general.

**Argumentos de paralelismo:** Ninguna de las opciones `-data`, `-project`, `-builder`, etc., incluye parámetros para ajustar hilos o núcleos. Por ejemplo, en la documentación de `-project` sólo aparecen `action`, `name`, `file`; en `-data` aparecen acciones de import/export, rango de fechas, etc. pero nada relativo a threads. No existe, en los manuales oficiales, flags tipo `threads=`, `workers=`, ni modos alternativos que modifiquen el paralelismo interno. 

**GUI vs CLI headless:** El modo `-gui` abre la interfaz web/visual; en cambio, el uso de `-project` (o cualquier otro comando sin `-gui`) corre headless en línea de comandos. No hay indicación de que `-project` cambie políticas internas de paralelismo: la ejecución sin GUI es idéntica lógicamente a la ruta gráfica, solo sin ventanas. No existe tampoco un flag especial documentado para “modo headless” aparte de usar directamente estos comandos en consola.

**Cambios 142 vs 144:** Los reléases oficiales no mencionan cambios en los parámetros de CLI para SQX entre la 142 y la 144. La nota de versión de la 144 habla de mejoras en CLI de Data Manager pero no indica cambios en SQX CLI. El único cambio relevante en 142 fue la introducción del comando `-extindicators` para indicadores externos. No hay pruebas documentadas de que el CLI requiera ahora ejecutarse desde un directorio específico; en Windows se indica usar `sqcli.exe` en la carpeta de instalación, lo cual implica que cualquier ruta completa válida debería funcionar siempre que las rutas relativas (configuración, licencia) se mantengan.

# C. Contrato de lanzamiento de la JVM

En Linux, `sqcli` es un lanzador nativo que inicia la JVM interna de SQX. Este lanzador lee archivos de configuración (`sqcli.config`, `StrategyQuantX.config`) y también respeta variables de entorno de Java. En Echo Forge se inyecta via systemd `JAVA_TOOL_OPTIONS` con opciones de memoria y GC: 

```
JAVA_TOOL_OPTIONS="-Xms34g -Xmx55g -XX:MaxDirectMemorySize=1g -XX:MaxMetaspaceSize=512m -XX:ReservedCodeCacheSize=256m -Xss1m -XX:+ExitOnOutOfMemoryError"
```

El archivo `sqcli.config` de SQX 144 añade internamente `-Xms4g` y `-XX:+UseParallelGC`. En la práctica observamos que la JVM arrancó con `Xms=4g` (el valor menor) y `Xmx=55g` (el mayor de las variables). Esto indica que **los parámetros explícitos en la configuración (`-Xms4g`) anulan al `-Xms34g` de `JAVA_TOOL_OPTIONS`**, a pesar de aparecer después (el lanzador suele aplicar sus propias flags de memoria en tiempo de inicialización). Por contra, el `-Xmx` quedó en 55g, por lo que el límite superior vino de la variable de entorno. 

Respecto al orden de precedencia de opciones JVM: Oracle/OpenJDK especifican que en Java 9+ los entornos `JDK_JAVA_OPTIONS` tienen prioridad sobre `JAVA_TOOL_OPTIONS`, y estos a su vez sobre `_JAVA_OPTIONS`. En nuestro caso usamos Zulu 25 (Java 25) donde `_JAVA_OPTIONS` ya está obsoleto. Según la documentación, `JAVA_TOOL_OPTIONS` (y _JAVA_OPTIONS) se *prepended* al inicio de los argumentos JVM. Sin embargo, `JDK_JAVA_OPTIONS` (introducido en Java 9) sobrescribe opciones idénticas en `JAVA_TOOL_OPTIONS`. Dado que no usamos `JDK_JAVA_OPTIONS` en el servicio, efectivamente las opciones de `JAVA_TOOL_OPTIONS` se aplican, excepto cuando el lanzador propio de SQX vuelve a especificar un valor (como con Xms).

Sobre paralelismo: el parámetro `-XX:ActiveProcessorCount=N` fija lo que `Runtime.getRuntime().availableProcessors()` reporta. Según pruebas públicas, esto *afecta el tamaño de los pools internos* (GC, ForkJoin, etc.) pero **no impide físicamente usar más cores** si el código genera más hilos. En nuestro caso SQX ya “reconoció” 76 cores y preparó 76 hilos ejecutores, por lo que no se usaría a menos que se limite con este flag (lo cual reduciría la concurrencia de JVM sin necesariamente mejorar la ejecución del workload). 

El `-XX:+UseParallelGC` habilita el recolector paralelo tradicional (throughput GC). En Java 8 era el predeterminado en modo servidor; en Java 11+ el predeterminado cambió a G1GC. Por tanto, forzar ParallelGC en Java 25 sacrifica los beneficios de G1 (menores pausas) a cambio de throughput masivo. No tenemos evidencia concreta de que esto empeore el rendimiento de SQX en este workload, pero en sistemas de 76 núcleos suele favorecer procesamiento intensivo si el GC no es el cuello. Dada la complejidad del modelo de SQX, lo razonable es no recomendar cambios de GC sin pruebas: **usar las que vienen por defecto** o el ParallelGC actual no es intrínsecamente erróneo, solo una alternativa. 

Por último, la prioridad de proceso (`High Priority` activado) tiene poco impacto si el servidor está ocioso (no hay contención). En Linux, cambiarla a “alta” básicamente hace que el scheduler favorezca a SQX si hay alguna otra carga mínima, pero en un servidor dedicado suele ser irrelevante; no incrementa el throughput por sí misma. Ejecutar desde un script *shell* en lugar de invocar el binario directamente no debería cambiar el comportamiento de la JVM: salvo que el script ajuste el `$PATH`, el directorio de trabajo, o capture señales, la JVM recibe los mismos argumentos. En resumen, no hay flags mágicos de la JVM necesarios (sí conviene proveer `-Djava.awt.headless=true` si el sistema carece de X11, pero SQX headless debería ignorar UI de todas formas). 

# D. Comportamiento multicore de SQX

SQX detecta los núcleos disponibles (p.ej. “Using: 76 cores, core usage configuration: ‘100%’” en logs) y crea un *pool* con 76 *thread executors*. Cada ejecutor es esencialmente un hilo de trabajo para distribuir tareas internas. Sin embargo, **crear 76 hilos no garantiza que todas las fases del cálculo sean paralelas**. Por ejemplo, en el *Builder* varias tareas (como backtests, evaluación y cruce de estrategias) suelen ejecutarse en paralelo, pero el plugin **CustomAnalysis** parece **procesar secuencialmente** cada estrategia. En el ejemplo dado, casi todo el tiempo de builder (69 minutos) fue consumido por CustomAnalysis (~60 minutos) usando solo ~1 CPU, lo cual indica que esa etapa no estaba paralelizada. 

No hay opción de CLI que cambie esto: el plugin de CustomAnalysis define internamente cómo recorre las estrategias. A falta de documentación oficial, inferimos que SQX distribuye las tareas de simulación básica (por ejemplo, evaluación o retesteo) en el pool, pero invoca el CustomAnalysis estrategia por estrategia, uno tras otro. Las políticas de paralelismo en `-project` (modo CLI) coincidirían con las de la GUI; es decir, no hay un “modo CLI especial” que altere el uso de threads. Por tanto, aunque SQX reconoció 76 hilos disponibles (según el log “Preparing thread executors: 76”), la **utilización real del CPU depende de cada fase**. Builder/Retester pueden aprovechar varios hilos, pero CustomAnalysis puede quedarse en un solo hilo. No hay ajustes documentados en settings o CLI de SQX 144 para paralelizar automáticamente esa fase.

En suma, la baja utilización de CPU en CustomAnalysis no proviene de la forma de lanzamiento de SQX, sino de la lógica interna del plugin (aparentemente secuencial). No se encontró evidencia de cambios en este aspecto entre 142 y 144. 

# E. Recomendación de arquitectura

Comparando las tres opciones:

| Criterio           | Ejecutar *directo*                 | Wrapper de Forge                  | Script oficial SQX         |
|--------------------|------------------------------------|-----------------------------------|----------------------------|
| **Compatibilidad 144**     | **Alta**: usa `sqcli` estándar.    | **Alta** (depende de implementación). | Indeterminada (no hay docs sobre un script oficial para 144). |
| **Multi-versión**  | Manejo actual de `<SQX_ROOT>/<ver>/sqcli` sirve. | Se puede implementar también. | Si existe, debería admitir rutas `<version>`. |
| **Control JVM**    | Medio: se apoya en `sqcli.config` y env vars. | Alto: podríamos añadir flags u opciones explícitas. | Bajo/Medio: el script oficial probablemente solo llame a `sqcli`. |
| **CPU / Hilos**    | Medio: no hay ajuste especial, usa lo configurado. | Alto: un wrapper puede fijar `-XX:ActiveProcessorCount` o variables. | Bajo: ¿script oficial?, presumiblemente similar al binario directo. |
| **Propagar errores**| Bueno: `sqcli` devuelve código de error,  Systemd lo captura. | Riesgo si no se maneja bien el código de salida en el wrapper. | Bueno (si lo provee SQX, debe pasar el código). |
| **Señales/Cancelación** | Directo: Syslog/systemd señalizan al proceso Java. | Complejo: el wrapper debe reenviar SIGTERM al hijo Java. | Indeterminado, pero asumiendo que sería `exec`, similar a directo. |
| **Mantenibilidad** | Simple: sin código extra.              | Más complejo: hay que mantener el wrapper. | Nulo (si está oficial, no lo mantenemos). |
| **Riesgo op.**    | Bajo: sin cambios de arquitectura.  | Mayor: introduce una capa nueva que puede fallar. | Medio: si existe y no está testeado, puede tener bugs propios. |

Por principio KISS/YAGNI, **mantener la ejecución directa** con `sqcli` es suficiente. La ventaja de un wrapper propio sería **controlar explícitamente el entorno JVM** (paths, opciones, working dir), pero en este caso no es indispensable: Systemd e `sqcli.config` ya manejan la mayoría de los parámetros. No hay evidencia de que un wrapper mejore el paralelismo por sí solo. 

El único caso para considerar un script sería si existiera un guión oficial del proveedor en 144 que debiera usarse (no se halló información pública de ello). Dado que los lanzamientos oficiales no mencionan uno, asumimos que no es requerido. Si existiera, usarlo debería ser compatible con 142/144 (p.ej. tomando `<version>` dinámicamente), pero no hay confirmación.

**Recomendación:** **KEEP_DIRECT_CLI**. Seguir invocando `sqcli` directamente, asegurando que **working directory** y variables estén correctas en systemd. Mantener el selector de versión `<SQX_ROOT>/<VERSION>/sqcli` funciona con ambas versiones. No vale la pena introducir un wrapper propio a menos que en el futuro salga un script oficial o se identifique una necesidad concreta no cubiertas por la invocación directa. 

# F. Propuesta mínima de implementación

Para mejorar sin romper el modelo actual:

- **Comando Headless:** Añadir `-Djava.awt.headless=true` en la configuración de JVM (por ejemplo, en `sqcli.config` o en `JAVA_TOOL_OPTIONS`) para servidores sin interfaz gráfica. Esto evita cargar librerías de UI innecesarias. Es una buena práctica cuando se corre en modo consola, aunque SQX suele ignorar GUI de todos modos.  
- **Directorio de trabajo:** Asegurar que el proceso arranca en el directorio de instalación de SQX (o usar rutas absolutas para config/licencia), para que `sqcli` encuentre todos los archivos relativos. Systemd puede usar `WorkingDirectory=/home/kor/sqx/144` para evitar confusiones.
- **Variables de entorno:** Revisar que `JAVA_TOOL_OPTIONS` y similares contengan valores razonables (ya inyectados) y que no haya variables conflictivas (`_JAVA_OPTIONS` idealmente vacío).
- **Preservar multiversión:** Todo cambio debe respetar que se invoca usando la ruta completa a `sqcli` según la versión, sin hardcodear v142 o v144. Por ejemplo, si se utilizara un script, que reciba la ruta de instalación dinámica.
- **Gestión de señales:** Si por ejemplo se usara un *wrapper* futuro, tendría que usar `exec sqcli "$@"` para que la JVM reciba SIGTERM y no queden procesos huérfanos.

**Básicamente**, no se requieren desarrollos complejos. El entorno actual se basa en KISS: configuraciones en systemd y archivos `.config` gestionan la JVM. Agregar un pequeño script *solo si hace falta* (por ejemplo para `cd` al directorio correcto o distinguir versiones) puede ser YAGNI mientras todo funcione con el binario. 

# G. Protocolo de prueba controlada

Para validar cualquier cambio en la invocación, se recomienda un benchmark reproducible:

**Configuración inicial (constante):** misma instalación de SQX (v142 o v144 según prueba), mismo proyecto de prueba, mismo corpus de datos, idénticas configuraciones de `sqcli.config` y `settings.xml` (coreUsage=100%, highPriority=true, etc.), mismo usuario y hardware, misma versión de JVM, mismas condiciones de carga del sistema.

**Variantes a probar:**  
A) *CLI Directo actual:* Ejecutar `sqcli -project action=start name=<proyecto>` como se hace hoy (entrada a systemd).  
B) *CLI con flags recomendados:* Mismo que A, pero agregando ajustes (p.ej. `-Djava.awt.headless=true` o configuraciones JVM oficiales si se encuentran).  
C) *Wrapper propuesto (si se implementa):* Una alternativa con script: p.ej. `run_sqcli.sh` que haga `cd` al directorio y luego `exec sqcli ...`. 

**Métricas a medir:**  
- **Procesadores reconocidos:** `Runtime.getRuntime().availableProcessors()`. Verificar que es 76 en todos.  
- **Hilos ejecutores preparados:** Buscar en logs “Preparing thread executors”. Debe ser 76 en todas las variantes (sin ActiveProcessorCount).  
- **Hilos activos reales:** por ejemplo usando `jps/jstack` durante ejecución o herramientas OS (top).  
- **Uso de CPU promedio/pico:** %, en total y por hilo.  
- **Tiempos de cada fase:** cronometrar builder, CustomAnalysis, Retester/Optimizer.  
- **Throughput:** estrategias procesadas por minuto (o similar).  
- **Uso de memoria/GC:** ver logs GC, uso de heap, pausas.  
- **Exit code y logs:** asegurarse que sea 0 y que la salida funcional sea la misma (p.ej. resultados estadísticos).

**Criterios de éxito/fracaso:**  
- Si el launcher era problema, esperamos ver *diferencias claras*: p.ej. variante B (con ajustes) reduce el tiempo de CustomAnalysis o aumenta concurrentemente los hilos activos, sin cambiar los resultados funcionales.  
- Si todas las variantes rinden prácticamente igual, el launcher no afecta el cuello de botella. Por ejemplo, si CPU sigue ~1 core en CustomAnalysis en B y C, entonces el script no cambia el comportamiento.  
- No basta con ver CPU alto: se debe verificar estabilidad de resultados y tiempos por fase. Una diferencia en tiempos del builder/CustomAnalysis confirmaría un efecto del launcher. Si solo cambia Xms/Xmx, podría afectar GC, pero probablemente poco.

En resumen: un launcher *no* tendrá éxito solo porque use más CPU; el criterio real es reducir el tiempo de procesamiento sin alterar la carga de trabajo. Si tras pruebas A, B, C los tiempos de CustomAnalysis o el número de hilos activos no mejoran, se descarta la hipótesis del launcher.

# H. Fuentes

- Manual oficial StrategyQuant X (CLI commands). Estos documentos listan los comandos y argumentos del CLI de SQX (v127+, aplicable a v144), donde se observa que *no* hay flags de hilos/CPU.  
- Notas de la versión SQX 144 (sitio StrategyQuant). Mencionan mejoras en CLI de Data Manager, sin referencia al CLI del Builder o CustomAnalysis.  
- Documentación “Introduction to CLI” de SQX: ejemplos de ejecución vía `sqcli.exe` para datos y modo batch.  
- Documentación específica de comandos: *Manage data*, *Manage projects*, *Manage instruments*, *Manage symbols*, *Manage databanks*, *Tools*, *Web GUI*, etc. Todo actualizado hasta abril 2020 (válido para v144).  
- Soporte Java/JVM: Blog de Baeldung sobre `JDK_JAVA_OPTIONS` vs `JAVA_TOOL_OPTIONS`; StackOverflow sobre `_JAVA_OPTIONS`; StackOverflow sobre `-XX:ActiveProcessorCount`. Estos confirman el orden de precedencia de variables de entorno JVM y el efecto de ActiveProcessorCount.  
- Observaciones propias (logs citados en el enunciado) indican *“Using: 76 cores... preparing 76 thread executors”* durante el arranque de SQX (demostrando reconocimiento de núcleos, settings coreUsage=100%).  

**Niveles de confianza:** Alta en lo documentado oficialmente (CLI y variables JVM); media-baja en inferencias no documentadas (comportamiento interno de CustomAnalysis), pues no hay fuente pública aparte de logs locales. Limitaciones: no se accedió al código fuente cerrado de SQX, por lo que algunas conclusiones (como si CustomAnalysis puede paralelizar) son deducidas indirectamente, no confirmadas internamente.

**Veredicto final:** El diagnóstico mejor sustentado es `SQX144_CLI_INVOCATION_CORRECT`. La ejecución actual *no adolece* de parámetros faltantes ni de requerimientos especiales de lanzamiento. Cualquier mejora en rendimiento debe buscarse a nivel del paralelismo interno de SQX (p. ej. en el plugin CustomAnalysis), no en cambiar la forma de invocar el CLI.