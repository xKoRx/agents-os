# Automatización robusta de StrategyQuant X Build 142 con Custom Analysis Java y SQCLI nativo

## Resumen ejecutivo

La ruta **oficial y verificable** para automatizar StrategyQuant X Build 142 sin tocar `.cfx` por fuera ni hacer “cirugía ZIP con bisturí oxidado” es esta: **ejecutar un Custom Analysis dentro de un Custom Project**, trabajar sobre `ResultsGroup`, `StrategyBase`, `WalkForwardMatrixResult`, `WalkForwardResult` y `Databank`, y disparar el proyecto por `sqcli` con `-project action=start`. La API pública documenta claramente el ciclo de vida de `CustomAnalysisMethod`, el acceso a estrategias vía `ResultsGroup`, la lectura/escritura de `lastSettings`, la conversión de XML de estrategia a `StrategyBase`, y la actualización del registro en databank. También documenta que las estrategias conservan `OptimizationProfile` y `OutOfSample` como metadatos del `ResultsGroup`. citeturn17view0turn24view0turn27view3turn26view4turn25view3turn25view4

Lo que **sí pude verificar y dejarte copy-pasteable** es: el esqueleto exacto del CA, cómo acceder al databank y a cada estrategia, cómo cargar/modificar parámetros de la estrategia y `MagicNumber`, y cómo persistir esos cambios de vuelta al databank usando API oficial. Lo que **no pude verificar en la API pública accesible** es una clase/documentación pública equivalente a `EAExporter` para exportar `.mq5` directamente por Java en Build 142; la documentación oficial que sí encontré para exportación MT muestra el flujo GUI “Source code tab → Save to file”, pero no expone una clase pública Java ni un comando `sqcli` específico para exportar EAs MT5. En otras palabras: para exportación MT5 programática, la documentación pública quedó coja; muerto el perro no, pero sí quedó medio cojo. citeturn41search1turn41search3turn14view0turn36view0turn36view1

## Arquitectura oficial soportada

`CustomAnalysisMethod` es una clase abstracta pública del paquete `com.strategyquant.tradinglib`. Su constructor documentado es `CustomAnalysisMethod(String name, int type)`, y los hooks oficiales son `filterStrategy(String project, String task, String databankName, ResultsGroup rg)` y `processDatabank(String project, String task, String databankName, ArrayList<ResultsGroup> databankRG)`. Los tipos documentados son `TYPE_FILTER_STRATEGY`, `TYPE_PROCESS_DATABANK` y `TYPE_BOTH`. No hay anotaciones obligatorias en esta clase base; el patrón oficial es declarar la clase en paquetes tipo `SQ.CustomAnalysis`, llamar a `super(...)` en el constructor y sobrescribir uno de los dos métodos. citeturn17view0

La propia documentación oficial del ejemplo `CAApplyOptimParams` usa exactamente ese patrón: `package SQ.CustomAnalysis;`, clase que extiende `CustomAnalysisMethod`, constructor `super("CAApplyOptimParams", TYPE_FILTER_STRATEGY)`, y override de `filterStrategy(...)`. El mismo artículo la define explícitamente como un **Custom Analysis snippet** que corre después del Walk-Forward Optimization. citeturn28view0

Además, la documentación de Custom Analysis en Custom Projects indica que el modo “per databank” corre sobre el databank completo y que este tipo de análisis se usa **dentro de un Custom Project** en la tarea “Custom analysis”. Eso calza perfecto con `sqcli -project action=start`, porque `sqcli` puede arrancar un proyecto existente, no inyectar lógica externa a mitad del vuelo. citeturn41search4turn40view0

## Acceso a databanks, estrategias y objetos Java

En el flujo oficial tienes dos niveles de acceso:

Primero, **durante el loop natural del task**, SQX te pasa el `ResultsGroup` directamente al `filterStrategy(...)` o el `ArrayList<ResultsGroup>` completo al `processDatabank(...)`. Eso es lo más limpio cuando tu pipeline necesita transformar cada estrategia y dejarla seguir al siguiente task. citeturn17view0turn28view0

Segundo, si necesitas **acceso aleatorio** al databank y actualización explícita, la API pública documenta `ResultsGroup.getDatabank()`, `Databank.getLocked(...)`, `Databank.update(...)`, `Databank.add(...)`, `Databank.loadStrategies(...)` y `Databank.getName()`. En cristiano: puedes bloquear una estrategia por nombre, modificarla y hacer `update(...)` para persistir el cambio. citeturn18view3turn26view4turn26view6turn26view7

Para cargar la estrategia como objeto Java editable, la ruta pública documentada es:

1. `rg.getStrategyXml()` para obtener el XML de estrategia desde `ResultsGroup`.  
2. `StrategyBase.createXmlStrategy(rg.getStrategyXml())` para convertir ese XML a `StrategyBase`.  
3. `transformToVariables(boolean symmetric)` para pasar a modo editable por variables.  
4. `variables()` para iterar o buscar parámetros por nombre.  
5. `transformToNumbers()` para volver al formato numérico.  
6. `rg.portfolio().addStrategyXml(strategyBase.getStrategyXml())` para escribir el XML modificado de vuelta en el `ResultsGroup`. citeturn18view6turn27view3turn31view0

Si lo que quieres es partir desde los `settings` y no desde el XML, la API pública también expone `StrategyBase.getStrategy(SettingsMap settings)` y `StrategyBase.getSettings()/setSettings(SettingsMap)`, aunque en los ejemplos oficiales de mutación de parámetros StrategyQuant usa la ruta XML→`StrategyBase`, no la ruta `SettingsMap`→`StrategyBase`. citeturn27view2turn18view7

## Modificación de parámetros robustos y `MagicNumber`

### Lo que está verificado al cien

El ejemplo oficial `CAApplyOptimParams` demuestra cómo tomar el resultado WFM desde la estrategia actual:

- `WalkForwardMatrixResult mwfResult = (WalkForwardMatrixResult) rg.mainResult().get(SettingsKeys.WalkForwardResult);`
- `WalkForwardResult bestWFResult = mwfResult.getWFResult(rg.getBestWFResultKey(), false);`
- `WalkForwardPeriod lastPeriod = bestWFResult.wfPeriods.get(bestWFResult.wfPeriods.size()-1);`
- `String lastParameters = lastPeriod.testParameters;`

Luego ese string de parámetros se aplica a la estrategia mediante un helper oficial de ejemplo. citeturn28view0

La versión mejorada del helper, `StrategyParametersHelperV2`, sigue siendo documentación oficial y su método `setParameters(...)` está completo: transforma la estrategia a variables, recorre `variables()`, compara por nombre, ejecuta `variable.setFromString(...)`, vuelve con `transformToNumbers()`, y reescribe el XML en `ResultsGroup` con `rg.portfolio().addStrategyXml(...)`. Además, si `modifyLastSettings=true`, intenta sincronizar `rg.getLastSettings()` usando `XMLUtil` y termina con `rg.setLastSettings(...)`. citeturn31view0

Importante: `StrategyParametersHelperV2.getParameterValues(...)` **omite** `MagicNumber` al listar parámetros, pero `setParameters(...)` **no lo excluye** al escribir. O sea: si tu estrategia tiene una variable llamada exactamente `MagicNumber`, puedes fijarla con el mismo helper enviando `MagicNumber=123456` en el string de parámetros. citeturn31view0

También encontré respaldo histórico del propio Mark Fric en foro oficial: la recomendación de SQ para magic numbers editables es **crear variables** para esos magic numbers y cambiarlas cuando se aplica el EA al gráfico; además recomienda usar un magic number único por par. Eso refuerza que `MagicNumber` como input variable es un patrón soportado por SQ, no un invento de laboratorio. citeturn33view1

### La pieza sensible en Build 142

Aquí hay una pifia importante, así que te la digo de frente. El ejemplo original de 2021 usa `ParametersSettings.setFromXML(lastSettings, rg.getStrategyXml())` para detectar si la estrategia usa variables simétricas (`parametersSettings.symmetry`). Pero en un comentario oficial de 2025, un usuario reporta explícitamente en **version 142** el error `Cannot load Parameters settings. Element ‘Optimization’ not found`. Por eso, para Build 142 yo **no confiaría ciegamente** en esa detección automática. citeturn28view0

La V2 mejora el helper porque desacopla la lectura/escritura de parámetros de esa detección; aun así, en enero de 2026 otro usuario reportó que el helper V2 “ya no es compatible con 143” y que corrompe datos de stop loss, mientras un admin respondió que lo revisarían. La lectura práctica es: **Build 142 parece ser el último rango donde esta familia de helpers todavía era razonable**, pero debes testear bien SL/PT y parametrización simétrica antes de subirlo a producción. citeturn31view0

### Código recomendado del helper

El siguiente helper está basado en la versión oficial V2, pero lo dejé reducido al caso que te importa: aplicar un string de parámetros arbitrario, incluyendo `MagicNumber`.

```java
package SQ.Utils;

import com.strategyquant.lib.SQTime;
import com.strategyquant.lib.XMLUtil;
import com.strategyquant.tradinglib.*;
import com.strategyquant.tradinglib.options.TradingOptionsList;
import com.strategyquant.tradinglib.propertygrid.IPGParameter;
import com.strategyquant.tradinglib.propertygrid.ParametersTableItemProperties;
import org.jdom2.Element;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class StrategyParametersHelperV2Safe {

    public static final Logger Log = LoggerFactory.getLogger(StrategyParametersHelperV2Safe.class);

    public static final String VALUE_DELIMITER = "=";
    public static final String PARAM_DELIMITER = ",";

    public static void setParameters(ResultsGroup rg,
                                     String parameters,
                                     boolean symmetricVariables,
                                     boolean modifyLastSettings) throws Exception {

        StrategyBase strategyBase = getStrategyBase(rg, symmetricVariables);
        Variables variables = strategyBase.variables();

        String[] params = parameters.split(PARAM_DELIMITER);
        HashMap<String, String> paramMap = new HashMap<>();

        for (String p : params) {
            String[] values = p.split(VALUE_DELIMITER, 2);
            if (values.length == 2) {
                paramMap.put(values[0].trim(), values[1].trim());
            }
        }

        for (int i = 0; i < variables.size(); i++) {
            Variable variable = variables.get(i);
            String newValue = paramMap.get(variable.getName());
            if (newValue != null) {
                variable.setFromString(newValue);
            }
        }

        strategyBase.transformToNumbers();
        rg.portfolio().addStrategyXml(strategyBase.getStrategyXml());
        rg.specialValues().setString(StatsKey.OPTIMIZATION_PARAMETERS, parameters);

        if (modifyLastSettings) {
            try {
                Element lastSettings = XMLUtil.stringToElement(rg.getLastSettings());
                Element elParams = lastSettings.getChild("Options")
                                              .getChild("BuildTradingOptions")
                                              .getChild("Params");

                List<Element> paramElems = elParams.getChildren("Param");
                List<TradingOption> tradingOptions = TradingOptionsList.getInstance().getAvailableClasses();

                for (String paramName : paramMap.keySet()) {
                    boolean processed = false;

                    for (TradingOption option : tradingOptions) {
                        if (processed) break;

                        String optionClass = option.getClass().getSimpleName();
                        ArrayList<IPGParameter> optionParams = option.getParams();

                        for (IPGParameter optionParam : optionParams) {
                            if (processed) break;
                            if (!optionParam.getName().equals(paramName)) continue;

                            String paramKey = optionParam.getKey();

                            for (Element elParam : paramElems) {
                                String elParamClass = elParam.getAttributeValue("className");
                                String elParamKey = elParam.getAttributeValue("key");

                                if (elParamClass != null
                                        && elParamKey != null
                                        && elParamClass.equals(optionClass)
                                        && elParamKey.equals(paramKey)) {

                                    String value = paramMap.get(paramName);

                                    if (optionParam.getType() == ParametersTableItemProperties.TYPE_TIME) {
                                        value = "" + SQTime.HHMMToMinutes(Integer.parseInt(value)) * 60;
                                    }

                                    elParam.setText(value);
                                    processed = true;
                                    break;
                                }
                            }
                        }
                    }
                }

                rg.setLastSettings(XMLUtil.elementToString(lastSettings));
            } catch (Exception e) {
                Log.error("Cannot apply trading-options params to last settings", e);
            }
        }
    }

    private static StrategyBase getStrategyBase(ResultsGroup rg, boolean symmetricVariables) throws Exception {
        StrategyBase xmlS = StrategyBase.createXmlStrategy(rg.getStrategyXml());
        xmlS.transformToVariables(symmetricVariables);
        return xmlS;
    }
}
```

El patrón anterior sale directamente del helper V2 oficial: `StrategyBase.createXmlStrategy(...)`, `transformToVariables(...)`, `variables()`, `variable.setFromString(...)`, `transformToNumbers()`, `rg.portfolio().addStrategyXml(...)` y `rg.setLastSettings(...)`. citeturn31view0

### Código recomendado del Custom Analysis

Este CA toma la mejor celda WFM elegida por SQX, aplica sus parámetros al strategy, añade `MagicNumber`, y deja el `ResultsGroup` mutado para el siguiente task. Para Build 142, te recomiendo **pasar la simetría como constante de proyecto** o dejarla configurable por `inputArgs`; no me casaría con la detección automática antigua. citeturn28view0turn31view0

```java
package SQ.CustomAnalysis;

import SQ.Utils.StrategyParametersHelperV2Safe;
import com.strategyquant.tradinglib.*;
import com.strategyquant.tradinglib.optimization.WalkForwardMatrixResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CAApplyRobustParamsAndMagic extends CustomAnalysisMethod {

    public static final Logger Log = LoggerFactory.getLogger(CAApplyRobustParamsAndMagic.class);

    public CAApplyRobustParamsAndMagic() {
        super("CAApplyRobustParamsAndMagic", TYPE_FILTER_STRATEGY);
    }

    @Override
    public boolean filterStrategy(String project, String task, String databankName, ResultsGroup rg) throws Exception {

        // Ajusta esto según tu template/proyecto.
        // En Build 142 es más seguro fijarlo explícitamente que depender del helper antiguo.
        boolean symmetricVariables = true;

        WalkForwardMatrixResult wfm =
                (WalkForwardMatrixResult) rg.mainResult().get(SettingsKeys.WalkForwardResult);

        if (wfm == null) {
            Log.warn("No WalkForwardMatrixResult found for {}", rg.getName());
            return true;
        }

        WalkForwardResult bestWFResult = wfm.getWFResult(rg.getBestWFResultKey(), false);
        if (bestWFResult == null || bestWFResult.wfPeriods == null || bestWFResult.wfPeriods.isEmpty()) {
            Log.warn("No best WF result/period found for {}", rg.getName());
            return true;
        }

        WalkForwardPeriod lastPeriod = bestWFResult.wfPeriods.get(bestWFResult.wfPeriods.size() - 1);

        String robustParamsFromWF = lastPeriod.testParameters;   // p.ej. "Fast=21,Slow=55"
        int robustRunsCount = bestWFResult.param1;               // matriz WFM param1
        int robustOosPercent = bestWFResult.param2;              // matriz WFM param2

        // Obtén tu magic number desde Echo Forge.
        // Opciones:
        // 1) pasarlo en inputArgs
        // 2) dejarlo fijo para test
        // 3) leerlo de un archivo/servicio invocado antes del proyecto
        String inputArgs = getInputArgs(); // ejemplo esperado: "magic=123456"
        int magicNumber = parseMagic(inputArgs, 123456);

        String finalParamPatch = robustParamsFromWF + ",MagicNumber=" + magicNumber;

        Log.info("Applying final patch to {} -> {}", rg.getName(), finalParamPatch);
        Log.info("Selected WFM cell: runs_count={}, oos_percent={}", robustRunsCount, robustOosPercent);

        StrategyParametersHelperV2Safe.setParameters(
                rg,
                finalParamPatch,
                symmetricVariables,
                true
        );

        // Si quieres dejar trazabilidad explícita en notas:
        rg.setNote("runs_count=" + robustRunsCount
                + ";oos_percent=" + robustOosPercent
                + ";magic=" + magicNumber);

        return true;
        // El ResultsGroup queda mutado y sigue al siguiente task del custom project.
    }

    private int parseMagic(String inputArgs, int fallback) {
        if (inputArgs == null || inputArgs.isBlank()) return fallback;

        String[] tokens = inputArgs.split(",");
        for (String token : tokens) {
            String[] kv = token.split("=", 2);
            if (kv.length == 2 && kv[0].trim().equalsIgnoreCase("magic")) {
                try {
                    return Integer.parseInt(kv[1].trim());
                } catch (Exception ignored) {
                    return fallback;
                }
            }
        }
        return fallback;
    }
}
```

Este código usa únicamente superficies verificadas en la documentación pública: `CustomAnalysisMethod`, `filterStrategy(...)`, `ResultsGroup.mainResult()`, `SettingsKeys.WalkForwardResult`, `WalkForwardResult.param1/param2`, `WalkForwardPeriod.testParameters`, `ResultsGroup.getBestWFResultKey()`, `ResultsGroup.setNote(...)` y el patrón oficial de aplicar parámetros por `StrategyBase`. citeturn17view0turn21view1turn25view3turn31view0

### Persistencia explícita en databank

Si en tu flujo necesitas mutar una estrategia específica **fuera** del iterator natural del task, puedes usar `Databank.getLocked(...)` y `Databank.update(...)`. Ese patrón está documentado por la API pública. citeturn26view7turn18view3

```java
Databank db = rg.getDatabank();
ResultsGroup locked = db.getLocked(rg.getName(), task);

// ... mutas "locked" con el helper ...

db.update(locked.getName(), locked, true, task);
locked.releaseLock(task);
```

## Lo que sí y lo que no pude verificar sobre `runs_count`, `oos_percent` y exportación MT5

### `runs_count` y `oos_percent`

La API pública confirma que `WalkForwardResult` expone `param1` y `param2`, y que `ResultsGroup` expone `getOOS()/setOOSSettings(...)` y `getOptimizationProfile()/setOptimizationProfile(...)`. Eso demuestra que el `ResultsGroup` tiene superficies oficiales para guardar metadatos de OOS y optimización. citeturn21view1turn25view3turn25view4

Pero no pude verificar, en la Javadoc pública accesible, los **setters internos concretos** de `com.strategyquant.tradinglib.strategy.OutOfSample` ni de `com.strategyquant.tradinglib.optimization.OptimizationProfile`. Por eso no te voy a vender humo con un `profile.setRunsCount(...)` inventado, porque eso sería pasarte un cacho disfrazado de solución. La conclusión honesta es: hoy puedes **leer** ese par desde `bestWFResult.param1/param2` y dejarlo trazado en `note` o en metadatos de proyecto; lo que no pude dejar validado es la mutación copy-pasteable de esos objetos internos sin entrar en API no documentada. citeturn21view1turn25view3turn25view4

### Exportación `.mq5`

La documentación oficial de usuario para exportar a MetaTrader dice que debes abrir la estrategia, ir a la pestaña **Source code**, cambiar a **MetaTrader Expert Advisor** y usar **Save to file**. La documentación de “Results – Source code” también explica que esa pestaña genera el source code del strategy para la plataforma seleccionada. citeturn41search1turn41search3

Lo que **no** encontré en la API pública accesible fue una clase pública documentada tipo `EAExporter`, `Mql5Exporter`, `SourceCodeExporter` o similar. La overview de la Public API solo lista paquetes públicos como `com.strategyquant.datalib`, `com.strategyquant.lib`, `com.strategyquant.tradinglib`, `com.strategyquant.tradinglib.project`, `...results`, `...task.settings` y `...taskImpl`; y en los índices públicos que pude revisar no apareció una clase exportadora de EAs. Por tanto, **no puedo validar** una exportación MT5 programática pura por Java apoyada en API pública documentada. citeturn14view0turn36view0turn36view1

Mi recomendación práctica para Echo Forge en Build 142 es esta:

- **Sí**: usar CA para aplicar parámetros y `MagicNumber` dentro del proyecto.  
- **Sí**: dejar el strategy mutado en el databank final.  
- **No vendido como verificado**: una llamada Java pública oficial a export `.mq5`.  
- **Si necesitas exportar sin UI sí o sí**: la extensión oficial más prometedora es un **Custom Task plugin** que interactúe con internals no expuestos públicamente, pero esa parte ya sale de la API pública documentada y exige inspección local del build/SDK. citeturn8view3turn14view0

## Instalación, empaquetado y ejecución por `sqcli`

### Opción recomendada para tu caso

Para un **Custom Analysis snippet**, la vía estándar no es empaquetar un JAR de plugin tipo task, sino usar el **Code Editor** de SQX. StrategyQuant documenta que el programa se extiende con snippets desde el Code Editor, y que esos snippets pueden exportarse/importarse como archivos `.sxp` mediante **Import/Export → Import extensions**. También documenta que las librerías Java externas se copian a `/user/libs` y requieren reinicio. citeturn43search3turn43search0turn42search14

La receta operativa que mejor encaja con Echo Forge es:

1. Crear dos clases en Code Editor:  
   `SQ.Utils.StrategyParametersHelperV2Safe` y `SQ.CustomAnalysis.CAApplyRobustParamsAndMagic`. citeturn28view0turn31view0

2. Compilarlas dentro de SQX. Si además usas librerías propias, copiarlas a `/user/libs` y reiniciar SQX. citeturn42search14

3. Añadir al Custom Project una tarea **Custom analysis** que use tu snippet. El tipo per-strategy/per-databank está soportado por `CustomAnalysisMethod`. citeturn17view0turn41search4

4. Si necesitas pasar datos dinámicos desde Echo Forge, usar `inputArgs` del snippet o un paso previo del proyecto que deje esos datos donde el snippet los pueda leer. `CustomAnalysisMethod` expone `getInputArgs()/setInputArgs()`. citeturn17view0

### Si necesitas un task nativo completo

SQX también soporta **plugins de task completos**. El ejemplo oficial dice que todo custom task se compone de dos plugins: un Task plugin y un Settings plugin, con paquetes obligatorios:

- `com.strategyquant.plugin.Task.impl.XXXXXX`
- `com.strategyquant.plugin.Settings.impl.XXXXX`

El propio ejemplo recomienda importar ambos `.sxp` por Code Editor y reiniciar SQX para ver el task disponible en Custom Projects. citeturn8view3

Eso es relevante para ti porque, si más adelante quieres encapsular “patch + export + audit trail” como un task nativo de proyecto, **esa** es la extensión oficial de mayor nivel dentro de SQX. citeturn8view3

### Disparo por `sqcli`

La CLI oficial documenta:

- `-project action=start name=...`
- `-project action=loadconfig name=... file=...`
- `-run file=...` para ejecutar varias líneas de comandos CLI
- `-execute file=...` para llamar un script externo desde el flujo CLI. citeturn40view0turn39search11turn39search8

Un flujo mínimo sería:

```bash
sqcli.exe -project action=loadconfig name=EchoForge file=C:/SQ/projects/EchoForge.cfx
sqcli.exe -project action=start name=EchoForge
```

O, mejor, por archivo de comandos:

```text
-project action=loadconfig name=EchoForge file=C:/SQ/projects/EchoForge.cfx
-project action=start name=EchoForge
-exit
```

y luego:

```bash
sqcli.exe -run file=C:/SQ/cli/echoforge.txt
```

La CLI **no documenta** pasar `.properties`, `.json` ni overrides arbitrarios de task/strategy parameters al arrancar el proyecto. Lo que sí documenta es cargar una config `.cfx`, arrancar el proyecto, ejecutar scripts externos y exportar databanks a CSV/XLSX. Por lo tanto, la vía oficial para dinamismo en tiempo de ejecución no es un archivo de propiedades externo, sino **meter la lógica dinámica dentro del proyecto** mediante Custom Analysis / Custom Task plugin. citeturn40view0turn40view1turn39search11turn39search8

## Ruta recomendada para Echo Forge

Si tuviera que dejar esto listo para producción en Build 142, mi diseño sería:

Integrar el cálculo de robustez fuera de SQX como ya lo hacéis, pasar a SQX el `MagicNumber` y cualquier flag operativo que necesites por una entrada controlada del proyecto, ejecutar un **Custom Analysis per-strategy** que:

1. lea `WalkForwardMatrixResult`,  
2. obtenga la celda robusta elegida (`rg.getBestWFResultKey()`),  
3. aplique `lastPeriod.testParameters`,  
4. agregue `MagicNumber=...`,  
5. deje trazabilidad con `setNote(...)`,  
6. envíe la estrategia parchada al siguiente task/databank. citeturn28view0turn31view0turn25view3

Para la parte de exportación MT5, separaría dos escenarios. Si basta con dejar el strategy listo para exportar y que otro paso local/controlado abra SQX con UI o automatice la pestaña Source code, la estrategia ya queda preparada. Si necesitas exportación `.mq5` 100 % headless **dentro** de SQX, yo no la daría por resuelta hasta inspeccionar localmente Build 142, porque la API pública no la documenta. En ese caso el siguiente salto oficial es un **custom task plugin**, pero su capa exportadora concreta no quedó expuesta en la documentación pública que pude verificar. citeturn41search1turn41search3turn8view3turn14view0

## Preguntas abiertas y limitaciones

La principal limitación de esta investigación es que la **Javadoc pública accesible no expone una clase/exporter pública para MQL5** ni los setters internos concretos de `OutOfSample` y `OptimizationProfile`; por eso no sería serio inventarte una API de export o de mutación de `runs_count/oos_percent` que no pude corroborar. citeturn14view0turn25view3turn25view4

También hay una advertencia de compatibilidad: el ejemplo original de parámetros tiene un reporte específico de error en **v142** por `ParametersSettings`, y la V2 tiene reportes de problemas a partir de **v143**. La lectura sensata es que en Build 142 la solución viable es **usar el helper basado en `StrategyBase.createXmlStrategy(...)` y testear muy bien** stops, profit targets y simetría de variables con un set acotado antes de soltarlo al bullpen productivo. citeturn28view0turn31view0

Mi conclusión final, sin adornarlo de más, es esta: para Build 142 la automatización robusta de **patch de parámetros + `MagicNumber` + persistencia en databank + ejecución por `sqcli`** sí queda bien soportada por la API oficial/documentación pública. La pieza que **no** queda cerrada con evidencia pública suficiente es la **exportación `.mq5` completamente programática por Java**. Ahí, hoy por hoy, el camino verificado se corta justo antes del último metro. citeturn17view0turn28view0turn31view0turn40view0turn41search1turn14view0