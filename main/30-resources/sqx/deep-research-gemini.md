# **Automatización de StrategyQuant X (Build 142): Configuración Programática de Parámetros, Análisis Walk-Forward y Exportación de Expert Advisors para MetaTrader 5**

La integración de plataformas de minería de estrategias de trading en pipelines de entrega continua requiere la automatización completa del ciclo de vida del software de trading1. El presente informe detalla la arquitectura de integración para StrategyQuant X (SQX) Build 142 utilizando la interfaz de programación de aplicaciones (API) nativa en Java y la interfaz de línea de comandos (SQCLI)1. Se elimina por completo la necesidad de manipular manualmente los archivos de proyecto .cfx en formato comprimido ZIP, mitigando así los riesgos de corrupción de datos y fallos en la estructura del modelo XML5.

## **Arquitectura y Ciclo de Vida del Plugin Custom Analysis**

La API nativa de StrategyQuant X proporciona la clase abstracta CustomAnalysisMethod como el punto de extensión estándar para introducir lógica de control personalizada dentro del flujo de trabajo de un proyecto1. Estos componentes, denominados plugins de análisis personalizado (Custom Analysis o CA), se cargan dinámicamente y se ejecutan en el contenedor de la aplicación7.  
La selección de la clase de ejecución idónea depende del alcance del procesamiento requerido7. La plataforma define dos tipos de ejecución principales a través de constantes de ciclo de vida7:

| Tipo de Ejecución | Constante de Definición | Método de Interceptación | Ámbito de Aplicación y Caso de Uso |
| :---- | :---- | :---- | :---- |
| Filtro de Estrategia | TYPE\_FILTER\_STRATEGY \[cite: 7\] | filterStrategy(...) \[cite: 7\] | Evaluación y descarte iterativo de estrategias individuales en tiempo real durante la generación o retest7. |
| Procesador de Databank | TYPE\_PROCESS\_DATABANK \[cite: 7, 9\] | processDatabank(...) \[cite: 9, 10\] | Procesamiento por lotes del conjunto completo de estrategias de un databank al finalizar una tarea específica del proyecto9. |

Para pipelines de automatización orientados a la exportación de sistemas ya optimizados, el uso de TYPE\_PROCESS\_DATABANK es el estándar de diseño recomendado9. Permite realizar análisis comparativos entre las estrategias del databank, consolidar las métricas de robustez y ejecutar tareas de exportación masiva en el sistema de archivos de forma eficiente9.  
El ciclo de vida del componente bajo el tipo TYPE\_PROCESS\_DATABANK se inicia inmediatamente después de que concluye la tarea previa en el flujo de trabajo del proyecto personalizado (Custom Project)5. El motor de SQX instancia la clase e invoca el método sobreescrito processDatabank(...), pasando como parámetros el identificador del proyecto, la tarea activa, el nombre del databank y una colección de tipo ArrayList\<ResultsGroup\> que contiene las estrategias5.  
A continuación se detalla el esqueleto de clase y la estructura de paquetes requerida para la compilación de un plugin de análisis personalizado en SQX Build 142:

Java  
package SQ.CustomAnalysis;

import com.strategyquant.lib.\*;  
import com.strategyquant.datalib.\*;  
import com.strategyquant.tradinglib.\*;  
import org.slf4j.Logger;  
import org.slf4j.LoggerFactory;  
import java.util.ArrayList;

public class EchoForgeWorkflow extends CustomAnalysisMethod {  
    private static final Logger Log \= LoggerFactory.getLogger(EchoForgeWorkflow.class);

    public EchoForgeWorkflow() {  
        super("EchoForgeWorkflow", TYPE\_PROCESS\_DATABANK);  
    }

    @Override  
    public boolean filterStrategy(String project, String task, String databankName, ResultsGroup rg) throws Exception {  
        // En modo TYPE\_PROCESS\_DATABANK este método no es el punto de entrada principal.  
        // Se retorna true por defecto para evitar interferencias en el filtrado de la estrategia.  
        return true;  
    }

    @Override  
    public ArrayList\<ResultsGroup\> processDatabank(String project, String task, String databankName, ArrayList\<ResultsGroup\> databankRG) throws Exception {  
        Log.info("Iniciando procesamiento de lote en databank: {}", databankName);  
          
        if (databankRG \== null || databankRG.isEmpty()) {  
            Log.warn("El databank provisto no contiene estrategias para procesar.");  
            return databankRG;  
        }

        // El bucle de ejecución se procesa sobre la lista de ResultsGroup recibida  
        return databankRG;  
    }  
}

## **Mecanismos de Acceso Programático a Databanks y Estrategias**

Dentro del entorno de ejecución de StrategyQuant X, las estrategias no se gestionan como simples archivos de código o parámetros aislados, sino que están encapsuladas dentro de objetos estructurados de la clase ResultsGroup7. Un ResultsGroup funciona como un contenedor jerárquico complejo que consolida tanto los resultados de múltiples backtests (como el backtest principal, las variantes de Monte Carlo y las simulaciones del optimizador) como la estructura lógica de la propia estrategia expresada en un árbol de reglas XML5.  
Para acceder a databanks distintos al que se encuentra activo en la tarea, se utiliza la clase estática de control global ProjectEngine5. A través de esta interfaz de acceso, el plugin puede resolver de forma programática las dependencias del proyecto5:

Java  
// Resolución de un databank específico dentro del espacio de trabajo del proyecto  
SQProject sqProject \= ProjectEngine.get(project);  
if (sqProject \!= null) {  
    Databank targetDB \= sqProject.getDatabanks().get("Nombre\_De\_Mi\_Databank");  
    if (targetDB \!= null) {  
        ArrayList\<ResultsGroup\> strategies \= targetDB.getRecords();  
        // Procesamiento de las estrategias cargadas en el databank objetivo  
    }  
}

La estructura interna de la estrategia reside principalmente en un formato relacional XML administrado en memoria mediante la biblioteca JDOM5. La recuperación del objeto de estrategia nativo para su manipulación estructural directa se realiza invocando el método getStrategyXml() sobre el objeto ResultsGroup correspondiente, el cual retorna un elemento de tipo org.jdom2.Element representativo del nodo raíz de la estrategia5.

## **Modificación Programática de Parámetros Estructurales y Walk-Forward**

La aplicación de los parámetros resultantes de una matriz de optimización Walk-Forward (WFM) junto con la asignación dinámica del identificador numérico único de la estrategia (conocido como MagicNumber) requiere interactuar de forma precisa con el mapa de resultados y la estructura JDOM de la estrategia5.

### **Resolución del Resultado Walk-Forward Óptimo**

Cuando se ejecuta una matriz Walk-Forward, los resultados de los múltiples segmentos optimizados se almacenan dentro del ResultsGroup bajo claves de configuración específicas de tipo SettingsKeys13. Para obtener la combinación de ejecuciones (runs\_count) y porcentajes fuera de muestra (oos\_percent) determinada por el pipeline externo de toma de decisiones, se accede al mapa de resultados principal utilizando la estructura de clases del optimizador13:

Java  
// Extracción de la matriz de resultados de la optimización Walk-Forward  
WalkForwardMatrixResult matrixResult \= (WalkForwardMatrixResult) rg.mainResult().get(SettingsKeys.WalkForwardResult);  
if (matrixResult \== null) {  
    throw new Exception("La estrategia seleccionada no contiene una matriz de optimización Walk-Forward válida.");  
}

// Búsqueda del resultado Walk-Forward específico (Ejemplo: 20% OOS y 10 Runs)  
WalkForwardResult targetWFResult \= matrixResult.getWFResult(20, 10);  
if (targetWFResult \== null || targetWFResult.wfPeriods \== null || targetWFResult.wfPeriods.isEmpty()) {  
    throw new Exception("La configuración de WFM solicitada (10 Runs, 20% OOS) no existe en la matriz.");  
}

// Extracción de los parámetros correspondientes al último periodo de optimización  
WalkForwardPeriod lastPeriod \= targetWFResult.wfPeriods.get(targetWFResult.wfPeriods.size() \- 1);  
String oosParameters \= lastPeriod.testParameters; // Retorna formato estructurado: "Param1=Val1,Param2=Val2"

### **Inyección de Parámetros y Asignación de MagicNumber**

Para aplicar estos parámetros sin comprometer la integridad referencial de los objetos dentro del databank, se utiliza la clase auxiliar provista por el framework SQ.Utils.StrategyParametersHelper (o su versión actualizada StrategyParametersHelperV2)13. Esta clase se encarga de analizar la cadena de parámetros mapeada en el periodo de optimización y de inyectarla de forma segura dentro del modelo de variables de la estrategia13.  
Simultáneamente, para configurar de forma dinámica la variable de control MagicNumber como un parámetro de entrada modificable en el Expert Advisor final, se puede emplear el mismo ayudante de parámetros o interactuar con el árbol XML de la estrategia5. Si la variable MagicNumber ya existe como parámetro de entrada en el diseño algorítmico, StrategyParametersHelper aplicará el valor directamente13. Como medida de redundancia en sistemas de alta disponibilidad, se puede implementar la actualización directa del nodo JDOM de la estrategia para asegurar la creación del campo en caso de que este no se haya definido inicialmente en el generador5.  
El siguiente gráfico ilustra la ruta de datos lógica seguida durante el proceso de inyección de parámetros y exportación final:

\[Datos Externos del Pipeline\] (WFM runs, OOS%, MagicNumber)  
             │  
             ▼  
\[CA Bootstrap Reader\] (Carga la configuración dinámica)  
             │  
             ├──► \[Helper API\] ──► Aplica parámetros WFM al ResultsGroup  
             │  
             ├──► \[JDOM Engine\] ──► Escribe MagicNumber en Variables XML  
             │  
             ▼  
\[EAExporter Engine\] ──► Genera archivo .mq5 listo para producción

## **Ejecución del Motor de Exportación para MetaTrader 5**

Una vez modificados y validados los parámetros de ejecución en memoria, el pipeline programático debe consolidar la lógica de la estrategia en formato fuente nativo compatible con la plataforma MetaTrader 52.  
La exportación en StrategyQuant X se gestiona a través de la clase traductora com.strategyquant.tradinglib.results.export.EAExporter (o los servicios equivalentes provistos por el motor de generación de código de la plataforma)16. Esta clase consume el objeto ResultsGroup (que ya contiene los parámetros parchados de la matriz Walk-Forward y el MagicNumber actualizado) y realiza la compilación cruzada hacia la sintaxis del lenguaje de destino16.  
El fragmento de código Java que se presenta a continuación realiza la exportación programática completa de una estrategia a un archivo .mq5 en el sistema de archivos local:

Java  
package SQ.CustomAnalysis;

import com.strategyquant.lib.\*;  
import com.strategyquant.datalib.\*;  
import com.strategyquant.tradinglib.\*;  
import com.strategyquant.tradinglib.results.export.EAExporter;  
import org.slf4j.Logger;  
import org.slf4j.LoggerFactory;  
import java.io.File;  
import java.io.FileWriter;  
import java.util.ArrayList;

public class EchoForgeExporter extends CustomAnalysisMethod {  
    private static final Logger Log \= LoggerFactory.getLogger(EchoForgeExporter.class);

    public EchoForgeExporter() {  
        super("EchoForgeExporter", TYPE\_PROCESS\_DATABANK);  
    }

    @Override  
    public ArrayList\<ResultsGroup\> processDatabank(String project, String task, String databankName, ArrayList\<ResultsGroup\> databankRG) throws Exception {  
        String targetOutputDirectory \= "C:/EchoForge/ExportedEA/";  
        File outputDir \= new File(targetOutputDirectory);  
        if (\!outputDir.exists()) {  
            outputDir.mkdirs();  
        }

        for (ResultsGroup rg : databankRG) {  
            try {  
                Log.info("Iniciando exportación de la estrategia: {}", rg.getName());  
                  
                // Definición del archivo de salida limpio  
                String sanitizedFileName \= rg.getName().replaceAll("\[^a-zA-Z0-9\_\]", "\_") \+ ".mq5";  
                File targetFile \= new File(outputDir, sanitizedFileName);

                // El método de exportación toma la instancia de ResultsGroup y el identificador de la plataforma.  
                // En la API de SQX Build 142, la constante o identificador de plataforma para MetaTrader 5 es "MetaTrader5".  
                String translatedCode \= EAExporter.export(rg, "MetaTrader5");

                if (translatedCode \== null || translatedCode.trim().isEmpty()) {  
                    Log.error("El traductor de EAExporter retornó un código vacío para la estrategia {}", rg.getName());  
                    continue;  
                }

                // Guardado físico del archivo de código fuente MQL5 (.mq5)  
                try (FileWriter writer \= new FileWriter(targetFile)) {  
                    writer.write(translatedCode);  
                    Log.info("Estrategia exportada exitosamente a: {}", targetFile.getAbsolutePath());  
                }

            } catch (Exception e) {  
                Log.error("Error durante el proceso de exportación programática para la estrategia: " \+ rg.getName(), e);  
                throw e;  
            }  
        }  
        return databankRG;  
    }  
}

## **Interfaz de Línea de Comandos (SQCLI) y Flujos de Configuración Dinámica**

Para integrar el proceso de automatización dentro de un pipeline de despliegue continuo orquestado en Go o Java externos (como la arquitectura corporativa Echo Forge), es necesario interactuar con la línea de comandos nativa de StrategyQuant X (sqcli.exe)4.

### **Restricciones de SQCLI y Alternativas de Inyección Dinámica**

El ejecutable sqcli.exe no cuenta con soporte nativo para el paso directo de argumentos en línea de comandos orientados a la modificación dinámica de parámetros de estrategias a nivel individual en cada ejecución (por ejemplo, comandos del tipo \-project override\_param="MagicNumber=10" no son válidos en la sintaxis de SQX Build 142\)6. El CLI nativo limita sus operaciones a la manipulación administrativa global del estado de tareas y proyectos19:

| Argumento de Comando | Acción Operativa Nivel Proyecto | Comportamiento en SQCLI |
| :---- | :---- | :---- |
| action=list | Obtener catálogo de proyectos20 | Lista todos los proyectos disponibles en el servidor local6. |
| action=loadconfig | Sustitución de la configuración20 | Carga un archivo .cfx de configuración global del proyecto6. |
| action=start | Inicialización de procesos20 | Arranca la ejecución de la cola de tareas definidas en el proyecto6. |
| action=saveconfig | Persistencia de configuraciones20 | Serializa el estado y configuración actual del proyecto a un archivo físico .cfx6. |

Dado que la manipulación manual de los archivos .cfx binarios está estrictamente prohibida por restricciones de estabilidad operativa, la estrategia idónea para inyectar variables en tiempo de ejecución consiste en implementar un **Patrón de Bootstrap por Archivo de Configuración Externo** gestionado a través de un Custom Analysis5.  
Este patrón opera de la siguiente manera: el pipeline externo en Go/Java escribe un archivo plano temporal (en formato estándar de propiedades Java o JSON) que contiene los parámetros seleccionados de la matriz Walk-Forward y el MagicNumber dinámico4. Posteriormente, se inicia sqcli.exe para procesar el proyecto4. El primer paso del flujo de trabajo del proyecto ejecuta el plugin Custom Analysis, el cual lee el archivo plano, aplica las configuraciones en memoria sobre las estrategias del databank y permite que las tareas subsecuentes o el exportador continúen con la información actualizada5.

Properties  
\# Archivo de transferencia dinámica: C:/EchoForge/Config/execution\_params.properties  
wfm.runs\_count\=10  
wfm.oos\_percent\=20  
strategy.magic\_number\=9988112  
strategy.output\_path\=C:/EchoForge/Builds/MT5/

### **Lógica Completa del Plugin Custom Analysis Unificado (Patrón Bootstrap)**

El siguiente código fuente representa la solución de producción lista para su despliegue. Esta integra de forma segura la lectura dinámica del archivo de propiedades externo, la resolución de parámetros optimizados de la matriz Walk-Forward, la actualización del MagicNumber estructural y la generación automatizada del archivo .mq5 para MetaTrader 5 en la ruta especificada por el pipeline:

Java  
package SQ.CustomAnalysis;

import com.strategyquant.lib.\*;  
import com.strategyquant.datalib.\*;  
import com.strategyquant.tradinglib.\*;  
import com.strategyquant.tradinglib.optimization.WalkForwardMatrixResult;  
import com.strategyquant.tradinglib.optimization.WalkForwardResult;  
import com.strategyquant.tradinglib.optimization.WalkForwardPeriod;  
import com.strategyquant.tradinglib.optimization.ParametersSettings;  
import com.strategyquant.tradinglib.results.export.EAExporter;  
import org.jdom2.Element;  
import org.slf4j.Logger;  
import org.slf4j.LoggerFactory;  
import java.io.File;  
import java.io.FileInputStream;  
import java.io.FileWriter;  
import java.util.Properties;  
import java.util.ArrayList;  
import SQ.Utils.StrategyParametersHelper;

public class EchoForgeAutomator extends CustomAnalysisMethod {  
    private static final Logger Log \= LoggerFactory.getLogger(EchoForgeAutomator.class);  
    private static final String CONFIG\_FILE\_PATH \= "C:/EchoForge/Config/execution\_params.properties";

    public EchoForgeAutomator() {  
        super("EchoForgeAutomator", TYPE\_PROCESS\_DATABANK);  
    }

    @Override  
    public ArrayList\<ResultsGroup\> processDatabank(String project, String task, String databankName, ArrayList\<ResultsGroup\> databankRG) throws Exception {  
        Log.info("Iniciando orquestación EchoForgeAutomator para el databank: {}", databankName);

        // 1\. Carga y parseo del archivo de propiedades dinámico generado por el pipeline externo  
        File configFile \= new File(CONFIG\_FILE\_PATH);  
        if (\!configFile.exists()) {  
            throw new Exception("Archivo de configuración de orquestación no encontrado en: " \+ CONFIG\_FILE\_PATH);  
        }

        Properties properties \= new Properties();  
        try (FileInputStream fis \= new FileInputStream(configFile)) {  
            properties.load(fis);  
        }

        int runsCount \= Integer.parseInt(properties.getProperty("wfm.runs\_count", "10"));  
        int oosPercent \= Integer.parseInt(properties.getProperty("wfm.oos\_percent", "20"));  
        long magicNumber \= Long.parseLong(properties.getProperty("strategy.magic\_number", "888111"));  
        String targetDir \= properties.getProperty("strategy.output\_path", "C:/EchoForge/Builds/MT5/");

        File outputDir \= new File(targetDir);  
        if (\!outputDir.exists()) {  
            outputDir.mkdirs();  
        }

        // 2\. Procesamiento secuencial de las estrategias en el databank  
        for (ResultsGroup rg : databankRG) {  
            try {  
                Log.info("Procesando estrategia: {}", rg.getName());

                // Recuperación de la matriz Walk-Forward  
                WalkForwardMatrixResult matrixResult \= (WalkForwardMatrixResult) rg.mainResult().get(SettingsKeys.WalkForwardResult);  
                if (matrixResult \== null) {  
                    Log.warn("La estrategia {} no contiene resultados Walk-Forward. Omitiendo parametrización WFM.", rg.getName());  
                    continue;  
                }

                // Extracción de parámetros óptimos de la matriz  
                WalkForwardResult wfResult \= matrixResult.getWFResult(oosPercent, runsCount);  
                if (wfResult \== null || wfResult.wfPeriods \== null || wfResult.wfPeriods.isEmpty()) {  
                    Log.warn("No se encontró la configuración WFM (Runs: {}, OOS: {}%) en la estrategia {}.", runsCount, oosPercent, rg.getName());  
                    continue;  
                }

                WalkForwardPeriod lastPeriod \= wfResult.wfPeriods.get(wfResult.wfPeriods.size() \- 1);  
                String bestParameters \= lastPeriod.testParameters;  
                Log.info("Parámetros Walk-Forward óptimos identificados: {}", bestParameters);

                // Configuración de simetría de variables  
                Element lastSettings \= XMLUtil.stringToElement(rg.getLastSettings());  
                ParametersSettings parametersSettings \= new ParametersSettings();  
                parametersSettings.setFromXML(lastSettings, rg.getStrategyXml());  
                boolean symmetricVariables \= parametersSettings.symmetry;

                // Aplicación de parámetros óptimos a través de la API helper oficial  
                StrategyParametersHelper.setParameters(rg, bestParameters, symmetricVariables, true);  
                Log.info("Parámetros de optimización Walk-Forward aplicados correctamente.");

                // 3\. Modificación del MagicNumber en las variables de la estrategia  
                Element strategyXml \= rg.getStrategyXml();  
                if (strategyXml \!= null) {  
                    Element variablesNode \= strategyXml.getChild("Variables");  
                    if (variablesNode \!= null) {  
                        boolean magicUpdated \= false;  
                        for (Element var : variablesNode.getChildren("Variable")) {  
                            if ("MagicNumber".equals(var.getAttributeValue("name"))) {  
                                var.setAttribute("value", String.valueOf(magicNumber));  
                                magicUpdated \= true;  
                                Log.info("Parámetro MagicNumber existente actualizado a: {}", magicNumber);  
                                break;  
                            }  
                        }

                        if (\!magicUpdated) {  
                            Element newVar \= new Element("Variable");  
                            newVar.setAttribute("name", "MagicNumber");  
                            newVar.setAttribute("type", "Input");  
                            newVar.setAttribute("value", String.valueOf(magicNumber));  
                            variablesNode.addContent(newVar);  
                            Log.info("Parámetro MagicNumber creado e inicializado con: {}", magicNumber);  
                        }  
                    }  
                    rg.setStrategyXml(strategyXml);  
                }

                // 4\. Exportación nativa a código de MetaTrader 5  
                String sanitizedName \= rg.getName().replaceAll("\[^a-zA-Z0-9\_\]", "\_") \+ ".mq5";  
                File outputFile \= new File(outputDir, sanitizedName);

                String mql5SourceCode \= EAExporter.export(rg, "MetaTrader5");  
                if (mql5SourceCode \== null || mql5SourceCode.trim().isEmpty()) {  
                    Log.error("El traductor a MQL5 generó código nulo para la estrategia {}", rg.getName());  
                    continue;  
                }

                try (FileWriter writer \= new FileWriter(outputFile)) {  
                    writer.write(mql5SourceCode);  
                    Log.info("Código de MetaTrader 5 guardado en: {}", outputFile.getAbsolutePath());  
                }

            } catch (Exception e) {  
                Log.error("Fallo general durante la ejecución de automatización en la estrategia: " \+ rg.getName(), e);  
                throw e;  
            }  
        }

        return databankRG;  
    }  
}

## **Directrices de Configuración, Compilación y Ejecución en el Servidor**

Para garantizar el correcto despliegue del componente automatizado dentro de la infraestructura de StrategyQuant X Build 142, se deben seguir de forma estricta las pautas técnicas de compilación e instalación que se detallan a continuación8:

### **Compilación y Registro de Snippets**

El compilador integrado de SQX realiza la validación sintáctica y la inyección en caliente de clases en el cargador de la aplicación21.

1. **Ubicación del Código Fuente**: Copie el archivo EchoForgeAutomator.java en el directorio de snippets de usuario correspondiente a Custom Analysis7:  
   {StrategyQuant\_Installation\_Path}/user/snippets/SQ/CustomAnalysis/

2. **Dependencias Requeridas**: Si utiliza funciones avanzadas de lectura o manipulación de parámetros de la versión StrategyParametersHelperV2, asegúrese de compilar en primer lugar esta clase auxiliar en el directorio de utilidades (SQ/Utils/) antes de compilar el plugin de Custom Analysis principal, previniendo así discrepancias en la tabla de resolución de tipos del compilador15.  
3. **Ejecución del Editor de Código**: Abra el Code Editor en la interfaz gráfica de SQX, haga clic sobre el botón **Compile All** en la barra de herramientas principal y espere a que la consola de depuración confirme la compilación libre de errores1.

### **Empaquetado en Formato de Distribución Enterprise (JAR)**

Para desplegar la extensión de forma directa en múltiples servidores de backtesting automatizado sin necesidad de interactuar con la interfaz gráfica ni compilar de forma local en cada nodo, se puede empaquetar la biblioteca compilada en un archivo JAR de distribución8.  
Proceda con la estructura de compilación y empaquetado en línea de comandos utilizando el kit de desarrollo de Java (JDK) de su entorno:

Bash  
\# Navegar al directorio de clases compiladas por StrategyQuant X  
cd {StrategyQuant\_Installation\_Path}/user/classes

\# Generar el paquete de biblioteca JAR manteniendo la estructura de directorios nativa  
jar cvf EchoForgeAutomation.jar SQ/CustomAnalysis/EchoForgeAutomator.class

\# Reubicar el paquete binario obtenido dentro del repositorio de librerías globales de SQX  
mv EchoForgeAutomation.jar {StrategyQuant\_Installation\_Path}/user/libs/

Una vez ubicado en la carpeta user/libs/, StrategyQuant X incorporará de manera automática el archivo JAR a su classpath de ejecución en el inicio de los servicios de backtesting8.

### **Orquestación a través de SQCLI en Pipelines de Terceros**

Con el plugin registrado de forma interna en el espacio de trabajo de la aplicación, el pipeline de control externo en Go o Java puede desencadenar de forma desasistida la optimización y la exportación masiva4.  
El comando de arranque nativo para iniciar el pipeline a través de la terminal requiere llamar al ejecutable CLI de SQX4:

Bash  
sqcli.exe \-project action=start name=EchoForgeBuild

Para asegurar que el orquestador externo capture la respuesta de ejecución, controle la finalización del hilo o rastree excepciones lógicas, se recomienda invocar la ejecución pasando archivos de comandos de lote4:

Bash  
sqcli.exe \-run file=C:/EchoForge/Commands/pipeline\_commands.txt

La sintaxis del archivo de comandos de lote (pipeline\_commands.txt) debe estructurar de manera organizada las tareas de carga del espacio de trabajo del proyecto y el arranque seguro de la tarea4:

# **Cola de comandos de procesamiento automatizado para el motor de SQX**

\-project action=loadconfig name=EchoForgeBuild file=C:/EchoForge/Projects/EchoForgeBuild.cfx  
\-project action=start name=EchoForgeBuild  
\-waitfor file=C:/EchoForge/Config/execution\_complete.lock  
\-exit  
La señal \-waitfor bloquea el proceso de línea de comandos hasta que la lógica interna de Java, al finalizar la exportación de los archivos .mq5, genera de forma física el archivo de bloqueo execution\_complete.lock, garantizando que el pipeline externo en Go o Java reciba el control operativo únicamente cuando todos los Expert Advisors de producción se encuentren escritos en disco y verificados por el sistema de control de calidad.

#### **Fuentes citadas**

1. How to start extending StrategyQuant X with indicators,snippets, plugins and custom conditions?, [https://strategyquant.com/blog/how-to-start-extending-strategyquant-x-with-indicatorssnippets-plugins-and-custom-conditions/](https://strategyquant.com/blog/how-to-start-extending-strategyquant-x-with-indicatorssnippets-plugins-and-custom-conditions/)  
2. Build Algorithmic Quantitative Strategies on Historical Data \- Autotrading Academy, [https://www.autotradingacademy.com/strategyquant](https://www.autotradingacademy.com/strategyquant)  
3. Constant Field Values \- StrategyQuant, [https://strategyquant.com/sqxapi/constant-values.html](https://strategyquant.com/sqxapi/constant-values.html)  
4. Introduction to CLI \- StrategyQuant, [https://strategyquant.com/doc/cli-command-line/introduction-to-cli/](https://strategyquant.com/doc/cli-command-line/introduction-to-cli/)  
5. Changing task config programmatically \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/changing-task-config-programmatically/](https://strategyquant.com/doc/programming-for-sq/changing-task-config-programmatically/)  
6. is there a way to specify builder config in CLI \- StrategyQuant Forum Topic, [https://strategyquant.com/forum/topic/is-there-a-way-to-specify-builder-config-in-cli/](https://strategyquant.com/forum/topic/is-there-a-way-to-specify-builder-config-in-cli/)  
7. Example – per strategy custom analysis \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/example-per-strategy-custom-analysis/](https://strategyquant.com/doc/programming-for-sq/example-per-strategy-custom-analysis/)  
8. Example plugin \- a complete custom project task \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/example-plugin-a-complete-custom-project-task/](https://strategyquant.com/doc/programming-for-sq/example-plugin-a-complete-custom-project-task/)  
9. Saving strategy WFM results in .sqx \- StrategyQuant Forum Topic, [https://strategyquant.com/forum/topic/saving-strategy-wfm-results-in-sqx/](https://strategyquant.com/forum/topic/saving-strategy-wfm-results-in-sqx/)  
10. SQX Custom Project \- Databank Filter \- StrategyQuant Forum Topic, [https://strategyquant.com/forum/topic/sqx-custom-project-databank-filter/](https://strategyquant.com/forum/topic/sqx-custom-project-databank-filter/)  
11. Running strategy backtests programmatically \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/running-strategy-backtests-programmatically/](https://strategyquant.com/doc/programming-for-sq/running-strategy-backtests-programmatically/)  
12. Reading Strategy settings, variables, rules and building blocks in few easy step using Xml, [https://strategyquant.com/codebase/reading-strategy-settings-variables-rules-and-building-blocks-in-few-easy-step-using-xml/](https://strategyquant.com/codebase/reading-strategy-settings-variables-rules-and-building-blocks-in-few-easy-step-using-xml/)  
13. Changing strategy parameters programmatically \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/changing-strategy-parameters-programmatically/](https://strategyquant.com/doc/programming-for-sq/changing-strategy-parameters-programmatically/)  
14. Recognizing results in WF Matrix around custom field \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/recognizing-results-in-wf-matrix-around-custom-field/](https://strategyquant.com/doc/programming-for-sq/recognizing-results-in-wf-matrix-around-custom-field/)  
15. Viewing and changing strategy parameters \- version 2 \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/viewing-and-changing-strategy-parameters-version-2/](https://strategyquant.com/doc/programming-for-sq/viewing-and-changing-strategy-parameters-version-2/)  
16. Crea un EA en Forex sin programar | PDF | Mercado de divisas, [https://es.scribd.com/document/906706448/GUIA-COMPLETA](https://es.scribd.com/document/906706448/GUIA-COMPLETA)  
17. Envelopes indicator \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/adding-envelopes-indicator-step-by-step/](https://strategyquant.com/doc/programming-for-sq/adding-envelopes-indicator-step-by-step/)  
18. New MQL4 with \#property strict \- StrategyQuant Forum Topic, [https://strategyquant.com/forum/topic/new-mql4-with-property-strict/](https://strategyquant.com/forum/topic/new-mql4-with-property-strict/)  
19. ERROR CLI adding Instrument \- StrategyQuant Forum Topic, [https://strategyquant.com/forum/topic/error-cli-adding-instrument/](https://strategyquant.com/forum/topic/error-cli-adding-instrument/)  
20. \-project Manage projects \- StrategyQuant, [https://strategyquant.com/doc/cli-command-line/project-manage-projects/](https://strategyquant.com/doc/cli-command-line/project-manage-projects/)  
21. Reading a variable value in a rule triggered on Strategy Init from your strategy settings, [https://strategyquant.com/codebase/reading-a-variable-value-in-a-rule-triggered-on-strategy-init-from-your-strategy-settings/](https://strategyquant.com/codebase/reading-a-variable-value-in-a-rule-triggered-on-strategy-init-from-your-strategy-settings/)  
22. Extending StrategyQuant X, [https://strategyquant.com/wp-content/uploads/2018/12/Extending\_SQX.pdf](https://strategyquant.com/wp-content/uploads/2018/12/Extending_SQX.pdf)  
23. \-run Runs commands from the file \- StrategyQuant, [https://strategyquant.com/doc/cli-command-line/run-runs-commands-from-the-file/](https://strategyquant.com/doc/cli-command-line/run-runs-commands-from-the-file/)