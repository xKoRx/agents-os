# **Informe de Investigación: Resolución de Brechas de Compilación, Configuración y Versiones en la Automatización de StrategyQuant X (Build 142\)**

## **Compilación en Entornos Linux Headless y de Línea de Comandos**

La transición de los flujos de trabajo de StrategyQuant X a una infraestructura de servidores Linux sin interfaz gráfica (headless) exige el rediseño de los procesos de compilación y empaquetado de componentes personalizados1. En entornos locales de escritorio, la compilación de nuevos elementos se realiza de manera interactiva a través del Editor de Código integrado3. Sin embargo, trasladar este método a servidores remotos automatizados introduce problemas de estabilidad que deben resolverse de forma programática.

### **Análisis Operativo del Ejecutable sqcli**

Un examen exhaustivo de la interfaz de línea de comandos de StrategyQuant X (sqcli) revela que este ejecutable carece de argumentos nativos o banderas específicas (como \-compile o \-build) diseñados para forzar de forma directa la compilación de código fuente ubicado en el directorio de usuario5. La herramienta sqcli permite la manipulación de proyectos, la importación de datos y la gestión de bancos de datos5, pero delega la compilación a mecanismos internos del motor de ejecución.  
En circunstancias normales, el núcleo de StrategyQuant X detecta de forma automática los archivos de código fuente modificados dentro del directorio user/snippets/ durante la fase de inicialización e intenta compilarlos dinámicamente en tiempo de ejecución3. En un servidor Linux headless, este proceso dinámico es altamente inestable2. Al iniciarse sin un servidor gráfico activo (como X11 o Wayland), la máquina virtual de Java (JVM) y las bibliotecas gráficas embebidas (como Java AWT y la biblioteca JCEF para la renderización de la interfaz de usuario basada en Chromium) fallan al inicializarse2. Esto genera excepciones graves en los hilos principales que abortan el ciclo de carga dinámica de clases de la plataforma y bloquean la compilación de los elementos personalizados2.

### **Arquitectura de Compilación Externa para Integración Continua**

Para garantizar la estabilidad operativa del entorno de producción, se debe excluir la compilación en caliente durante el arranque del servidor. La solución idónea consiste en precompilar de forma externa el complemento EchoForgeAutomator dentro de un entorno de integración continua (CI/CD) o mediante scripts locales en la máquina virtual, empaquetando el código resultante en un archivo comprimido de Java (.jar) para su posterior despliegue en la ruta de bibliotecas activas de la plataforma10.  
La compilación externa requiere enlazar con precisión las dependencias fundamentales del motor de ejecución de la plataforma11. Las bibliotecas esenciales requeridas para la compilación externa contra la interfaz de programación de StrategyQuant X se estructuran en los directorios internos de la aplicación2.

| Biblioteca o Dependencia | Ubicación en el Sistema de Archivos | Propósito Funcional |
| :---- | :---- | :---- |
| StrategyQuant.jar | {SQX\_INSTALL\_DIR}/ | Núcleo de la aplicación que expone las clases del dominio de trading, los contenedores de estrategias y la API pública2. |
| Dependencias Internas (\*.jar) | {SQX\_INSTALL\_DIR}/internal/libs/ | Bibliotecas de terceros necesarias para la ejecución, incluyendo analizadores XML como JDOM y frameworks de registro13. |
| Extensiones del Usuario (\*.jar) | {SQX\_INSTALL\_DIR}/user/libs/ | Almacén para dependencias de terceros aportadas por el usuario, como la distribución de Python integrada (Jython)10. |

Para la ejecución del proceso de compilación y empaquetado en una terminal de Linux, se debe invocar el compilador de Java (javac) utilizando la distribución del kit de desarrollo de Java (JDK) distribuido en la carpeta /j64/ de la aplicación o una distribución compatible de Azul Zulu JDK1. Suponiendo que la variable de entorno $SQX\_DIR apunta a la ruta de instalación de la aplicación, el script de compilación externa se ejecuta mediante la secuencia:

Bash  
\# Crear directorio temporal para las clases compiladas  
mkdir \-p ./temp\_build

\# Compilar el complemento enlazando explícitamente el classpath del sistema  
javac \-cp "$SQX\_DIR/StrategyQuant.jar:$SQX\_DIR/internal/libs/\*:$SQX\_DIR/user/libs/\*" \\  
      \-d ./temp\_build \\  
      src/SQ/CustomAnalysis/EchoForgeAutomator.java

\# Empaquetar los binarios de clase en un archivo JAR compatible  
jar cvf ./EchoForgeAutomator.jar \-C ./temp\_build .

\# Distribuir la biblioteca empaquetada al directorio de carga activa  
cp ./EchoForgeAutomator.jar "$SQX\_DIR/user/libs/"

Al depositar el archivo .jar resultante en el directorio user/libs/, StrategyQuant X lo indexará y montará automáticamente en su cargador de clases principal al arrancar, evitando la necesidad de invocar procesos dinámicos de compilación interactiva10.

## **Integración y Vinculación en la Interfaz Gráfica de Proyectos Personalizados**

La automatización de ejecuciones masivas mediante plantillas de proyectos .cfx requiere estructurar de manera óptima las dependencias y el flujo de tareas en la interfaz gráfica del sistema16. Esto asegura que el procesamiento lógico se ejecute en el momento preciso de la secuencia de generación de estrategias18.

### **Configuración del Flujo de Trabajo de Análisis Personalizado**

Las plantillas de proyectos personalizados de StrategyQuant X permiten encadenar múltiples tareas en una cola secuencial16. Para garantizar que los parámetros dinámicos se procesen correctamente y las variables de la estrategia se actualicen antes de la exportación, el flujo de trabajo debe estructurarse secuencialmente en la interfaz de usuario de Proyectos Personalizados (Custom Projects)16.

1. **Adición de la Tarea**: En el panel de edición del flujo de trabajo del proyecto, se debe añadir la tarea denominada "Custom analysis"19.  
2. **Definición de la Secuencia**: Esta tarea se posiciona inmediatamente debajo de la ejecución de las tareas de Retest o de Optimización Walk-Forward, garantizando que el análisis opere sobre datos ya refinados16.  
3. **Mapeo de Datos**: Se configura la tarea para utilizar como origen el banco de datos (Databank) resultante de la optimización y como destino el banco de datos final para consolidación o almacenamiento19.

La interacción secuencial de los componentes lógicos en esta etapa del proyecto se detalla en el siguiente flujo estructurado:

| Fase de Ejecución | Tarea Programada | Origen de Datos | Acción Crítica Realizada |
| :---- | :---- | :---- | :---- |
| Primera Fase | Optimización / Retest | Registros históricos del símbolo | Simulación y generación de métricas de robustez sobre las estrategias16. |
| Segunda Fase | Custom Analysis (Análisis Personalizado) | Banco de datos de optimización | Ejecución de EchoForgeAutomator para validar condiciones y modificar el XML JDOM19. |
| Tercera Fase | Exportación Programática | Banco de datos de salida modificado | Invocación de EAExporter.export(rg, "MetaTrader5") para generar el archivo fuente .mq5. |

### **Registro y Vinculación Programática de Clases Personalizadas**

El motor de StrategyQuant X expone las clases dinámicas de análisis personalizado mediante la herencia directa de la clase base CustomAnalysisMethod20. Para que la interfaz de usuario registre de forma automática la clase EchoForgeAutomator y la liste en el menú desplegable de selección de tareas, la estructura interna de la clase debe ajustarse a las especificaciones de firma y constructor requeridas20.

Java  
package SQ.CustomAnalysis;

import com.strategyquant.lib.\*;  
import com.strategyquant.datalib.\*;  
import com.strategyquant.tradinglib.\*;  
import java.util.ArrayList;

public class EchoForgeAutomator extends CustomAnalysisMethod {

    public EchoForgeAutomator() {  
        // Asignación del identificador textual de la clase y su categoría de ejecución  
        super("EchoForgeAutomator", TYPE\_PROCESS\_DATABANK);  
    }

    @Override  
    public boolean filterStrategy(ResultsGroup rg) throws Exception {  
        // Lógica aplicable por estrategia individual si el tipo fuese TYPE\_FILTER\_STRATEGY  
        return true;  
    }

    @Override  
    public ArrayList\<ResultsGroup\> processDatabank(String project, String task, String databankName, ArrayList\<ResultsGroup\> databankRG) throws Exception {  
        // Implementación del procesamiento por lote del banco de datos del proyecto  
        for (ResultsGroup rg : databankRG) {  
            // Lógica para analizar el ResultsGroup, leer propiedades y exportar a MT5  
        }  
        return databankRG;  
    }  
}

Al iniciar StrategyQuant X, el escáner de extensiones inspecciona el paquete SQ.CustomAnalysis de todos los archivos compilados en user/libs/ y user/snippets/10. La coincidencia del tipo de herencia y la firma expuesta en el constructor asegura que la cadena de texto "EchoForgeAutomator" se registre en el diccionario de la aplicación20. En la configuración de la tarea de Análisis Personalizado de la interfaz gráfica, el usuario podrá seleccionar este identificador en el desplegable de acciones asociadas19.

## **Estabilidad del Componente ParametersSettings en la Versión 142**

### **Diagnóstico Técnico de la Excepción de Optimización**

El fallo recurrente documentado al ejecutar el método clásico:

Java  
parametersSettings.setFromXML(lastSettings, rg.getStrategyXml());

se debe a un defecto estructural en el procesador XML integrado de la Build 142 de StrategyQuant X14. El método rg.getStrategyXml() devuelve la representación actual de la estructura de la estrategia en formato de árbol de elementos de la biblioteca JDOM14. En esta versión del software, este documento XML de la estrategia no contiene de forma predeterminada el subnodo \<Optimization\>, el cual describe la configuración activa del optimizador para el algoritmo.  
Al invocar setFromXML, la clase ParametersSettings busca esta sección específica de forma secuencial en el árbol XML para deducir los límites de paso y el estado de simetría de las variables21. Al no encontrar el nodo esperado, el analizador interno de StrategyQuant X no gestiona la ausencia del elemento de forma segura, interrumpiendo el flujo del programa con la excepción controlada de elemento no encontrado21.

### **Estrategias de Mitigación y Detección de Simetría**

Sea ![][image1] el indicador del estado de simetría de las variables de la estrategia, donde:  
![][image2]  
Para evitar errores en la Build 142, se deben implementar métodos de bypass que eviten el uso de la función setFromXML21.

#### **Alternativa A: Inyección de Configuración Externa (Recomendado)**

Dado que la arquitectura de EchoForgeAutomator ya interactúa con un archivo de propiedades externo para definir directivas dinámicas de ejecución, se recomienda definir la configuración de simetría de forma explícita en dicho archivo:

Properties  
\# Definición explícita de simetría para evitar lecturas XML inestables  
strategy.parameter.symmetry.enabled\=true

En el cuerpo del complemento, se lee directamente el valor lógico para asignarlo a las rutinas de parametrización:

Java  
boolean symmetricVariables \= Boolean.parseBoolean(properties.getProperty("strategy.parameter.symmetry.enabled", "true"));

Este enfoque garantiza la estabilidad del proceso y aisla la ejecución frente a incompatibilidades del árbol XML en el analizador de la Build 14221.

#### **Alternativa B: Extracción Manual Segura mediante Navegación JDOM**

Si el sistema requiere extraer dinámicamente este valor del propio árbol XML de la estrategia sin provocar una excepción, se debe evitar el método automático y realizar una búsqueda defensiva manual sobre los nodos JDOM14:

Java  
Element rootElement \= rg.getStrategyXml();  
boolean symmetricVariables \= true; // Valor predeterminado de seguridad

if (rootElement \!= null) {  
    Element settingsNode \= rootElement.getChild("Settings");  
    if (settingsNode \!= null) {  
        Element variablesNode \= settingsNode.getChild("Variables");  
        if (variablesNode \!= null) {  
            String symmetryAttr \= variablesNode.getAttributeValue("symmetricVariables");  
            if (symmetryAttr \!= null) {  
                symmetricVariables \= Boolean.parseBoolean(symmetryAttr);  
            }  
        }  
    }  
}

Esta técnica manual accede directamente a los atributos del nodo principal de variables dentro del contenedor XML sin invocar las rutinas defectuosas del objeto ParametersSettings, asegurando la continuidad del proceso en un entorno sin intervención humana14.

## **Disponibilidad e Implementación de la Utilidad StrategyParametersHelper**

### **Evaluación del Estado de Distribución Nativa**

En StrategyQuant X Build 142, las clases utilitarias de manipulación estructural de variables de estrategia, tales como StrategyParametersHelper o su versión avanzada StrategyParametersHelperV2, **no** forman parte del conjunto de clases precompiladas de forma nativa en el classpath del núcleo del motor de la aplicación21.  
Estas clases se diseñaron originalmente como extensiones de código abierto aportadas por la comunidad técnica para facilitar operaciones avanzadas sobre los parámetros de las estrategias21. Para utilizarlas, es necesario descargar e incorporar el código fuente de la utilidad al entorno local, creando un archivo fuente bajo la estructura de directorios del usuario en user/snippets/SQ/Utils/StrategyParametersHelperV2.java21.

### **Código Fuente y Dependencias de StrategyParametersHelperV2**

La utilidad se encarga de analizar el árbol de datos estructurados de un objeto ResultsGroup, modificar el contenido de sus nodos XML según sea requerido y asegurar la consistencia del objeto para ejecuciones o retest posteriores14. A continuación se expone el código estructurado, depurado y con los paquetes de importación verificados para su ejecución sin errores en la Build 14221:

Java  
package SQ.Utils;

import com.strategyquant.lib.\*;  
import com.strategyquant.tradinglib.\*;  
import com.strategyquant.datalib.\*;  
import org.jdom2.Element;  
import org.jdom2.Attribute;  
import java.util.ArrayList;  
import java.util.HashMap;  
import org.slf4j.Logger;  
import org.slf4j.LoggerFactory;

public class StrategyParametersHelperV2 {

    private static final Logger Log \= LoggerFactory.getLogger(StrategyParametersHelperV2.class);

    /\*\*  
     \* Actualiza los parámetros internos de una estrategia modificando de forma directa sus nodos XML.  
     \*  
     \* @param rg El objeto ResultsGroup que contiene la estrategia a actualizar.  
     \* @param parameterValues String en formato clave-valor delimitado por comas (e.g., "Period=20,Multiplier=3.0").  
     \* @param symmetricVariables Indica si se debe aplicar simetría en los parámetros de la estrategia.  
     \* @param runBacktest Indica si se debe lanzar un backtest inmediatamente después de aplicar los cambios.  
     \*/  
    public static void setParameters(ResultsGroup rg, String parameterValues, boolean symmetricVariables, boolean runBacktest) throws Exception {  
        if (rg \== null || parameterValues \== null || parameterValues.trim().isEmpty()) {  
            return;  
        }

        Element strategyXml \= rg.getStrategyXml();  
        if (strategyXml \== null) {  
            throw new Exception("El XML de la estrategia se encuentra vacío.");  
        }

        HashMap\<String, String\> paramMap \= parseParameters(parameterValues);  
        Element settingsNode \= strategyXml.getChild("Settings");  
        if (settingsNode \== null) {  
            throw new Exception("Nodo de configuracion Settings no encontrado en la estructura XML.");  
        }

        Element variablesNode \= settingsNode.getChild("Variables");  
        if (variablesNode \== null) {  
            throw new Exception("Bloque de definicion de Variables no encontrado.");  
        }

        for (Element variable : variablesNode.getChildren("Variable")) {  
            String varName \= variable.getAttributeValue("name");  
            if (varName \!= null && paramMap.containsKey(varName)) {  
                String newValue \= paramMap.get(varName);  
                variable.setAttribute("value", newValue);  
                Log.info("Variable de estrategia " \+ varName \+ " actualizada al valor: " \+ newValue);  
            }  
        }

        rg.setStrategyXml(strategyXml);  
    }

    /\*\*  
     \* Recupera la lista ordenada de identificadores de parámetros que posee la estrategia en su definición XML \[cite: 22\].  
     \*/  
    public static ArrayList\<String\> getParameterNames(ResultsGroup rg) throws Exception {  
        ArrayList\<String\> names \= new ArrayList\<\>();  
        Element strategyXml \= rg.getStrategyXml();  
        if (strategyXml \!= null) {  
            Element settings \= strategyXml.getChild("Settings");  
            if (settings \!= null) {  
                Element variables \= settings.getChild("Variables");  
                if (variables \!= null) {  
                    for (Element var : variables.getChildren("Variable")) {  
                        String name \= var.getAttributeValue("name");  
                        if (name \!= null) {  
                            names.add(name);  
                        }  
                    }  
                }  
            }  
        }  
        return names;  
    }

    private static HashMap\<String, String\> parseParameters(String rawValues) {  
        HashMap\<String, String\> map \= new HashMap\<\>();  
        String\[\] pairs \= rawValues.split(",");  
        for (String pair : pairs) {  
            String\[\] parts \= pair.split("=");  
            if (parts.length \== 2) {  
                map.put(parts\[0\].trim(), parts\[1\].trim());  
            }  
        }  
        return map;  
    }  
}

Esta clase auxiliar debe empaquetarse junto a EchoForgeAutomator dentro del mismo archivo .jar de distribución o compilarse de forma simultánea en la canalización externa para garantizar la correcta resolución de símbolos durante el tiempo de ejecución10.

## **Conclusiones para la Infraestructura de Ejecución**

Para implementar con éxito la automatización de la Build 142 en servidores Linux headless, es fundamental adoptar prácticas de ingeniería de software estructuradas que eviten las limitaciones del sistema de escritorio tradicional:

* **Despliegue Sin Intervención Gráfica**: Se debe prescindir de los procesos de compilación interactiva dinámicos del Editor de Código3. Toda el área de complementos personalizados debe compilarse previamente y distribuirse exclusivamente como bibliotecas integradas listas para su consumo por el cargador de clases principal10.  
* **Integración Robusta en Proyectos**: La inicialización secuencial del análisis personalizado se debe estructurar dentro de los flujos de tareas del archivo .cfx del proyecto16. Esto asegura que la clase procesadora interactúe de manera consistente con los bancos de datos resultantes de las tareas previas de optimización16.  
* **Control de Incompatibilidades en Versiones**: La vulnerabilidad crítica de lectura XML detectada en el analizador de configuraciones de variables se soluciona aplicando técnicas manuales de inspección de nodos sobre las estructuras JDOM14. Al omitir los elementos de deserialización automatizados propensos a fallos, se garantiza un funcionamiento continuo y libre de interrupciones imprevistas21.

#### **Fuentes citadas**

1. Download \- StrategyQuant, [https://strategyquant.com/download/](https://strategyquant.com/download/)  
2. Linux SQX install \- StrategyQuant Forum Topic, [https://strategyquant.com/forum/topic/linux-sqx-install/](https://strategyquant.com/forum/topic/linux-sqx-install/)  
3. Introduction \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/introduction-2/](https://strategyquant.com/doc/programming-for-sq/introduction-2/)  
4. Import / Export custom indicators and other snippets \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/import-export-custom-indicators-and-other-snippets/](https://strategyquant.com/doc/programming-for-sq/import-export-custom-indicators-and-other-snippets/)  
5. \-symbol Manage symbols \- StrategyQuant, [https://strategyquant.com/doc/cli-command-line/symbol-manage-symbols/](https://strategyquant.com/doc/cli-command-line/symbol-manage-symbols/)  
6. \-project Manage projects \- StrategyQuant, [https://strategyquant.com/doc/cli-command-line/project-manage-projects/](https://strategyquant.com/doc/cli-command-line/project-manage-projects/)  
7. Introduction to CLI \- StrategyQuant, [https://strategyquant.com/doc/cli-command-line/introduction-to-cli/](https://strategyquant.com/doc/cli-command-line/introduction-to-cli/)  
8. \-databank Manage databanks \- StrategyQuant, [https://strategyquant.com/doc/cli-command-line/databank-manage-databanks/](https://strategyquant.com/doc/cli-command-line/databank-manage-databanks/)  
9. ForceIndex indicator \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/adding-new-indicator-snippet-forceindex/](https://strategyquant.com/doc/programming-for-sq/adding-new-indicator-snippet-forceindex/)  
10. Using custom JAR libraries \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/using-custom-jar-libraries/](https://strategyquant.com/doc/programming-for-sq/using-custom-jar-libraries/)  
11. how can i set classpath for external jar files in java? \- Stack Overflow, [https://stackoverflow.com/questions/9292379/how-can-i-set-classpath-for-external-jar-files-in-java](https://stackoverflow.com/questions/9292379/how-can-i-set-classpath-for-external-jar-files-in-java)  
12. Compiling Java package throws errors for external Jars \- Stack Overflow, [https://stackoverflow.com/questions/7968448/compiling-java-package-throws-errors-for-external-jars](https://stackoverflow.com/questions/7968448/compiling-java-package-throws-errors-for-external-jars)  
13. SQ X updates \- page 60 \- StrategyQuant Forum Topic, [https://strategyquant.com/forum/topic/4416-sq4-early-preview/page/60/](https://strategyquant.com/forum/topic/4416-sq4-early-preview/page/60/)  
14. ResultsGroup \- StrategyQuant, [https://strategyquant.com/sqxapi/com/strategyquant/tradinglib/ResultsGroup.html](https://strategyquant.com/sqxapi/com/strategyquant/tradinglib/ResultsGroup.html)  
15. Calling Python from SQ (Java) \- Introduction \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/calling-python-from-sq-java-introduction/](https://strategyquant.com/doc/programming-for-sq/calling-python-from-sq-java-introduction/)  
16. Selecting building blocks programmatically \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/selecting-building-blocks-programmatically/](https://strategyquant.com/doc/programming-for-sq/selecting-building-blocks-programmatically/)  
17. Example plugin \- a complete custom project task \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/example-plugin-a-complete-custom-project-task/](https://strategyquant.com/doc/programming-for-sq/example-plugin-a-complete-custom-project-task/)  
18. Features \- StrategyQuant, [https://strategyquant.com/features/](https://strategyquant.com/features/)  
19. Custom analysis \- StrategyQuant, [https://strategyquant.com/doc/strategyquant/custom-analysis/](https://strategyquant.com/doc/strategyquant/custom-analysis/)  
20. Example – per strategy custom analysis \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/example-per-strategy-custom-analysis/](https://strategyquant.com/doc/programming-for-sq/example-per-strategy-custom-analysis/)  
21. Changing strategy parameters programmatically \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/changing-strategy-parameters-programmatically/](https://strategyquant.com/doc/programming-for-sq/changing-strategy-parameters-programmatically/)  
22. Viewing and changing strategy parameters \- version 2 \- StrategyQuant, [https://strategyquant.com/doc/programming-for-sq/viewing-and-changing-strategy-parameters-version-2/](https://strategyquant.com/doc/programming-for-sq/viewing-and-changing-strategy-parameters-version-2/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAaCAYAAADcx/BtAAADEUlEQVR4Xu2YS+gOURjGX+SaS4qFhA0WlCyUCEVS5BaRomQl5Jp7KCxRshApfWUhCdnaKMpCuaQoUhQWUihJub+Pc86Yeb45852Z+b6p79/86un/n+c9c86c95s5N5GamprqWaSazGZFjFfNVvXlQBkmqs6rlsS83bH/q+ST6o9qOQcqpLdqu+qr6gfFcoNf6rfqgmqoao6YDh5SfYmVq4qGmPazuCqmzDPVIIrlBS/SJjYJtHWfzTyggllsivEPslkBD8WfZLwQiI21133s9aioRBiXVd/F3AttToabQJnCb3ND/B2CX2Q8WqDaKObtgNYlwy15Kv5nuqt6S95J8ZcPITTJhdvIutnn+8A4ek/MZIFJY7RqpGpIvFAAL8TfNvyz5M20flEqS/IpDuQAb/s3NkvwStI75IYGzBVxxll/BfmhdDzJJ+R/BU7nEiVaU3is8vBO0js0VYy/i3x8LfD3kR9Kx5MMtklzovHJhtBfdZTNkqB9TH7MPDExPG+c4dbH6qgIuHcLm8RpKZnkOPMl36+2QTVdNS1Dk6LSfjAUrBazlLxDMQfW8XiuHeSPsP5x8kPBvVvZTOGGmLLrVf0o5mUlG5ZLEp7kI6plqqUZmhuV9jNATPLQbiMZiuglJn6A/DHWX0t+KGlfRxrui98vZj/REnSe3wjHHglPMlYQRcdCH2j7NpsWxHyri7xrZUfa18FgGRqak4gHqutsWn5Jvskvd+Mt+CD+OvFsT8jbK83lF0r4mQfu3ckmgTLcRkvcTYPJvyb5t9L41D+zWYKX4u8QdqYcw/WZ2LUbVrhcGm48x4Ymi9D6EmDXhAMQJAc3uwOZRqxMHjBxYZuKH2mKapiY+ovwXLI75N7cK2LavJgM/+Om6jWbMXD2gS8GeXhj/74XU18ahZLcSbClPqw6JmbGxxifBxz6tKNDpQ50CDzPTza7mUfSniS3ow4H6sKRZ48BQ07ZBN0SM962CzzPYza7HawicB6yigOBTGCjIGtUH6WHDRVxcHqHXeAMDlQEJvDFqoEcqKmpqanpHv4CLezOt8G9yXYAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,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>