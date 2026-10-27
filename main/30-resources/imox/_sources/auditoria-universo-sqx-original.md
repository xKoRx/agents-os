---
name: "auditoria-universo-sqx"
description: "Auditoría quant de un universo o databank de estrategias SQX (mq4 + trades + sqx) en cualquier mercado: clustering, cobertura de regímenes, gaps, robustez y qué minar después, con informe PDF."
---

# Auditoría de universo de estrategias SQX (cobertura de regímenes y gaps)

Actúa como Quant Portfolio Researcher senior. La pregunta central que debe responder el informe es siempre esta:

> «Si estas N estrategias fueran mi universo actual en <MERCADO> <TF>, ¿qué partes del comportamiento del mercado estoy cubriendo, dónde estoy excesivamente concentrado, qué regímenes tengo poco o nada cubiertos y qué debería investigar o minar a continuación?»

**Cuándo usarla:** el usuario pide analizar un databank o carpeta de estrategias SQX *como universo* (diversificación real, clustering, regímenes, gaps, próximos minados, qué estrategias sobran).
**Cuándo NO:** para cuentas o carteras ya operando.

## Requisitos y adaptación al entorno
Esta skill se escribió sobre un montaje con SQX en una máquina remota y análisis pesado en la nube. Si tu entorno es distinto, adapta estas piezas antes de usarla:

- **Herramientas de equipo remoto** (`device_bash`, `device_stage_files`, `device_commit_files`, `SendUserFile`): si trabajas todo en local, sustitúyelas por `Bash` y por la entrega de ficheros que use tu cliente. Todo lo demás funciona igual.
- **MCP de SQX** (`mcp__*__sqx__*`): opcional. Sin él, el inventario se hace solo desde los ficheros (pasos 3-5); pierdes la reconciliación con el databank del paso 1.
- **Skills auxiliares** del paso 12 (`dataviz`, `pdf`): si no las tienes, genera los gráficos con matplotlib y el PDF con reportlab siguiendo las indicaciones de ese paso, que son autosuficientes.
- **Versión de SQX**: los extractores están validados con Build 136 (.mq4) y el formato SQStats puede cambiar entre builds. Recalibra siempre como se indica en el paso 4.
- **Python**: en la nube hacen falta numpy, pandas, scipy, matplotlib y reportlab. En el equipo basta la librería estándar.

## Entregables
1. Informe PDF de tipo research report (17 secciones + anexo, en español, coma decimal).
2. CSV `<MERCADO>_<TF>_universe_classification.csv` (separador `;`, decimal `,`, utf-8-sig) con la familia, las métricas, la clasificación CORE/SATELLITE/BENCH/REDUNDANT y el motivo de cada estrategia.
3. Los dos ficheros se entregan al usuario y se guardan en la carpeta de salida que tenga configurada.
4. Mensaje final breve: respuesta a la pregunta central, las discrepancias de datos que bloquean el despliegue y las limitaciones del método.

## Principios no negociables
- **Tres tipos de evidencia, siempre etiquetados:** A = backtest; B = diversificación entre estrategias; C = fuera de muestra o live (holdout post-generación, WF OOS, demo o real). No mezclarlos. Un buen backtest nunca es evidencia live.
- **DESCONOCIDO ≠ no cubierto.** Si no hay muestra suficiente, se dice. Hay que distinguir entre la cobertura *empírica* y la cobertura *de diseño* (si existe alguna estrategia construida para ese comportamiento).
- **No inventar datos, métricas ni parámetros.** Si falta algo (el número de pruebas de la minería, datos de precio, evidencia live), se declara y se muestra la sensibilidad.
- **Valor incremental > rentabilidad individual.** Una estrategia mediocre que cubre un régimen ausente vale más que un clon excelente.
- **Nada está validado para live** por tener buenas métricas. Las estrategias REDUNDANT se *archivan*, no se borran (sirven como alternativas, como lista de exclusión para SQX y para contar las pruebas del DSR).
- Etiquetar la confianza (alta, media o baja) cuando la muestra sea pequeña.

## Paso 0 · Preparación
Crea una lista de tareas. Si el usuario está presente, confirma con AskUserQuestion solo lo que no se pueda deducir de los ficheros:
- Carpeta y proyecto/databank de SQX (por ejemplo, proyecto «Builder», databank «Results»: comprueba cuáles usa el usuario).
- Riesgo fijo por trade (1R). Normalmente es `mmRiskedMoney` en el .mq4. Verifícalo: la mediana de P&L de los cierres por `SL` debe rondar −1R.
- Zona horaria del servidor del bróker y sesiones del mercado (ver el paso 7).
- Si tiene un fichero de precios del instrumento (export de SQX o MT4). Si no lo tiene, se usa un proxy (paso 7).
Si el usuario no está presente, asume lo razonable y decláralo al principio del informe.

## Paso 1 · Inventario
- Contar tipos de fichero. Patrón habitual de un pipeline SQX con WF Matrix: `EA_<MKT>_<TF>_<runs>.<oos%>_<id>.mq4`, `BT_SINGLE_WF_<MKT>_<TF>_<runs>.<oos>_<id>.csv`, `ORIG_<MKT>_<TF>_<id>.sqx`, `WF_<...>_<runs>.<oos>_<id>.sqx` y `SINGLE_WF_<...>.sqx`. El prefijo `<runs>.<oos>` (por ejemplo `7.26`) es la celda elegida de la WF Matrix. Adáptalo a la convención de nombres del usuario.
- Cruzar los IDs entre tipos: diff de las listas sin prefijos. Buscar ficheros que falten, IDs que no casen y sufijos «(1)» (reimportaciones).
- **SQX por MCP** (si están disponibles las herramientas `sqx__*`): `list_projects` → `list_databanks` → `list_strategies`. Para `get_strategy_stats` de muchas estrategias, delega en un subagente que las pida en paralelo y escriba un CSV. OJO: `values[0]` es el nombre de la estrategia, así que `values[i+1]` ↔ `columns[i]`. Descarta las columnas «Mini equity chart».
- Reconciliar el databank con los CSV (neto y nº de trades) y comprobar si las columnas OOS están a cero. Caso real visto: el «IS» del databank era todo el backtest, holdout incluido.

## Paso 2 · Mover datos entre el equipo y la nube
Solo aplica si el análisis se hace en un entorno distinto al de SQX. Si trabajas en local, sáltate este paso.

- La python del equipo puede no tener scipy ni sklearn. El análisis pesado se hace en la nube y la extracción, en el equipo con la librería estándar.
- Trade lists: `device_stage_files` (máximo 50 por llamada).
- .mq4 y .sqx: extrae en el equipo y saca el resultado por stdout. Si la salida es grande se guarda en el directorio de resultados de herramienta del cliente (legible con Bash en la nube), pero **se trunca a 262.144 caracteres**. Para ficheros grandes: `tar cJf - a.csv b.csv | base64 -w0 > bundle.b64; split -b 200000 bundle.b64 part_`; imprime cada parte en una llamada, reensambla en la nube, comprueba el md5 y descomprime.
- Para bucles largos en el equipo usa `nohup python3 script.py > log 2>&1 &` y consulta el log.

## Paso 3 · Lógica estructural de los .mq4 (SQX Build 136)
Extractor (`python3 ext.py 0 999 > salida`):
```python
import glob, re, sys
fs=sorted(glob.glob('EA_*.mq4')); lo,hi=int(sys.argv[1]),int(sys.argv[2])
for f in fs[lo:hi]:
    s=open(f,encoding='utf-8',errors='replace').read(); L=s.split('\n'); out=['#####FILE '+f]
    out+=[l.strip() for l in L[:8] if 'Generated' in l or 'Backtested' in l or 'Strategy' in l]
    a=s.find('// -- Variables'); b=s.find('// Money Management variables')
    out+=[l.strip() for l in s[a:b].split('\n') if l.strip().startswith('extern') and 'CustomComment' not in l]
    a=s.find('extern double mmRiskedMoney'); out.append(s[a:a+60].split('\n')[0])
    a=s.find('extern string sdtw'); b=s.find('extern string slts')
    out+=[re.sub(r'\s*//.*','',l.strip()).replace('extern ','') for l in s[a:b].split('\n') if l.strip().startswith('extern') and 'extern string s' not in l[:16]]
    a=s.find('// Rule: Trading signals'); b=s.find('return;',a)
    out.append('\n'.join(l.strip() for l in s[a:b].split('\n') if l.strip() and not l.strip().startswith('//') and l.strip() not in ('{','}')))
    print('\n'.join(out))
```
Qué extraer y cómo interpretarlo:
- Cabecera `WF Matrix - Strategy <ID> EA`: **comprueba que el ID coincide con el nombre del fichero** (caso real: un .mq4 contenía otra estrategia distinta). `Backtested on <SYMBOL> / <TF>, <desde> - <hasta>`: el `<hasta>` es el fin de datos de generación y marca el inicio del holdout de esa estrategia.
- Señales: `LongEntrySignal = (...);` y `ShortEntrySignal = (...);` (si es `false`, no hay lógica corta).
- Entrada: `sqOpenOrder(OP_BUYSTOP|OP_SELLSTOP|OP_BUYLIMIT|OP_BUY...)`. El nivel de precio se saca con `sqMMFixedAmount("Current",OP_x,(PRECIO),sqGetSLLevel`, no partiendo por comas, porque hay argumentos anidados. También: `sqSetOrderExpiration(_ticket, N)`, SL y PT (`k·sqATR(NULL,0,P,1)`), `"TrailingStop"`, `"TrailingActivation"`, `"MoveSL2BE"` y las opciones de trading (LimitTimeRange con horas, ExitOnFriday con hora, ExitAtEndOfDay).
- Rasgos por estrategia: **dirección**, **anclaje de entrada** (pivote SqPivots(startH,startM,line,shift), máximo de N barras, nivel de sesión, MA ± k·vol, bandas, HA, Keltner, cierre diario…), **etiquetas de filtros** (BB por encima de la superior / por debajo de la media, ADX bajo o al alza, giro de BullsPower, SAR, expansión de ATR, estructura diaria, etc.), **firma de salida** (tupla de periodos de ATR y coeficientes de SL/PT/TS) y **expiración**.
- Semántica de SQX: `sqBands(..., mode, shift)` con mode 0 = media, 1 = superior, 2 = inferior. Una orden stop con expiración larga que se reemplaza en cada señal hace que el filtro pese poco: compruébalo con el solape de trades del paso 6.
- Marca las anomalías: condiciones siempre verdaderas (`X <= X`), condiciones duplicadas (`A && A`) y la dirección del código frente a la del backtest (¿hay cortos en el CSV sin lógica corta, o al revés?).
- Clase declarada (taxonomía sugerida: Trend Following / Momentum / Breakout / Pullback / Mean Reversion / Range / Volatility / Market Structure / Hybrid / Other). Recuerda que, si todas entran con órdenes stop, a nivel de ejecución todas son breakout.

## Paso 4 · Decodificar los .sqx (son zip)
- `SINGLE_WF_*.sqx`: `Results/Main: <SYM>_LOM_<TF>/MonteCarloManipulation_Results.xml` y `MonteCarloRetest_Results.xml`, con `<RobustnessOriginalResults>` y `<LevelStat level="50..100">`.
- `WF_*.sqx`: el `settings.xml` (hasta 90 MB) tiene un `<Result resultKey="WF: N runs : P % OOS">` por celda más el base `Strategy <ID>`. Las estadísticas van en `<stats_LQ1_direction_DD_0_L1_pl_DD_10_L1_sample_DD_{S}_L1__RQ1_ ...><SQStats version="2" e="b64">…`, donde S = 10 es el IS (solo la **ventana IS inicial**), 20 el OOS concatenado y 127 el total.
- Decodificador SQStats (formato binario propietario, validado con Build 136):
```python
import base64, struct
def decode(b64):
    b=base64.b64decode(b64); i=0; out={}
    while i<len(b):
        t=b[i]
        if t in (1,2,3):
            k=b[i+1]
            if t==1: v=struct.unpack('>i',b[i+2:i+6])[0]; i+=6
            elif t==3: v=struct.unpack('>f',b[i+2:i+6])[0]; i+=6
            else: v=struct.unpack('>q',b[i+2:i+10])[0]; i+=10
            out[(t,k)]=v
        elif t in (0x65,0x66,0x67):
            L=struct.unpack('>H',b[i+1:i+3])[0]; name=b[i+3:i+3+L].decode(); j=i+3+L
            if t==0x65: v=struct.unpack('>i',b[j:j+4])[0]; j+=4
            elif t==0x67: v=struct.unpack('>f',b[j:j+4])[0]; j+=4
            else: v=struct.unpack('>q',b[j:j+8])[0]; j+=8
            out[name]=v; i=j
        else: raise ValueError('type %d'%t)
    return out
KEYS={'net':(3,10),'dd':(3,9),'trades':(1,9),'pf':(3,27),'sharpe':(3,1),'retdd':(3,25),'stability':(3,11),'annual_pct':(3,24),'r_expectancy':(3,34),'avg_trade':(3,17),'avg_win':(3,31),'avg_loss':(3,32),'exposure':(3,46),'avg_bars':(3,30)}
```
  **Recalibra siempre** con una estrategia conocida (los valores de `get_strategy_stats` o su CSV) antes de fiarte del mapa de claves: puede cambiar entre builds.
- WF, por estrategia: las estadísticas OOS de la celda elegida, la **WF Efficiency** = % anual OOS / % anual IS (umbrales orientativos: < 50 % sobreajuste, 60-80 % bien, **> 100 % sospechoso**) y la tasa de celdas «aprobadas» (OOS > 0, PF ≥ 1,2, eficiencia ≥ 0,5). Si aprueba el 100 % de las celdas, la matriz no discrimina: dilo. Una eficiencia > 1 suele reflejar que el tramo OOS fue mejor que la ventana IS inicial (asimetría temporal), no robustez.
- MC, por estrategia: neto P95 / original y DD P95 / DD original, por separado para Manipulación (orden de trades y saltos) y para Retest (ruido en datos, spread y parámetros).

## Paso 5 · Métricas por estrategia (trade lists)
- CSV de SQX: separador `;`, columnas `Ticket;Symbol;Type;Open time;Open price;Size;Close time;Close price;Profit/Loss;Balance;Sample type;Close type;MAE ($);MFE ($);Time in trade;Comment`; fechas `%Y.%m.%d %H:%M:%S`.
- **pandas 3 usa `datetime64[us]`.** Nunca hagas `astype('int64')//10**9`; para la hora usa `.values.astype('datetime64[h]')`.
- R = P&L / 1R. P&L diario realizado (por fecha de cierre) sobre días hábiles.
- Por estrategia: n, PF, win rate, E[R], SQN (√N) y SQN100, Sharpe (media/σ diaria · √252), max DD, Ret/DD, skew de R, cuota de beneficio del 1 % de mejores días, duración mediana, % de tiempo en mercado, tipos de cierre, reparto por sesión, años y meses, cociente segunda/primera mitad. Además, **pre y post holdout** según el `gen_end` de cada estrategia: E[R], Sharpe y nº de trades.

## Paso 6 · Similitud, duplicados y familias
- ρ de Pearson y Spearman del P&L diario, ρ semanal y distribución de pares (> 0,5 / > 0,7 / > 0,9 y mínimo). Autovalores: cuota de PC1 y **nº efectivo de apuestas** = (Σλ)²/Σλ².
- Solape de entradas: Jaccard de (hora de entrada, dirección) y Jaccard de timestamps idénticos. Simultaneidad: cuántas estrategias entran en la misma hora y dirección (y el % de trades en eventos con ≥ 10, ≥ 20 y ≥ 40). Concurrencia horaria de posiciones abiertas (máximo y % de horas con más de la mitad del universo dentro).
- Clustering jerárquico de enlace medio sobre `0.5·(1−ρ) + 0.5·(1−Jaccard_hora)`, con corte ≈ 0,55. Grupos de casi-duplicados: enlace completo sobre 1−ρ con corte 0,10 (ρ ≥ 0,90).
- Nombra las **familias** por estructura (anclaje, motor de salida, dirección) y comprueba que coinciden con el clustering. Subfamilias por etiquetas de filtros: mide su ρ interno y entre subfamilias. Si subfamilias con filtros opuestos correlacionan alto, los filtros son decorativos.
- **Fuentes independientes**: agrupa en S1, S2… las familias con ρ ≥ ~0,6 a nivel de familia. Son la unidad de la regla de cobertura.

## Paso 7 · Precio, sesiones y regímenes
- Datos de precio: prefiere un fichero real (export de SQX o MT4). La web puede estar bloqueada por la política de red del entorno (caso real: Yahoo y Stooq devolvían 403): no intentes saltártela. **Alternativa validada**: un proxy de cierre diario con los precios de apertura y cierre de todos los trades (último precio observado cada día, forward-fill en los días sin observación). Contrástalo con drawdowns conocidos del mercado e informa del % de días rellenados.
- Sesiones en **hora de servidor** (comprueba la de tu bróker; muchos operan en GMT+2/+3). Adáptalas al mercado: índices de EE. UU. (apertura del contado a las 16:30 de servidor si el servidor va en GMT+2), DAX o Euro Stoxx (09:00-17:30 CET), oro y FX (Asia, Londres, NY). Declara siempre la convención usada.
- Regímenes (se etiquetan con los datos disponibles hasta t y se aplican a los trades con **1 día hábil de retardo**):
```python
lr=np.log(c).diff()
R['trend']=np.log(c/c.shift(50))/(lr.rolling(50).std()*np.sqrt(50))   # Strong Bull >=1.2 | Weak Bull 0.4-1.2 | Neutral ±0.4 | Weak Bear -1.2..-0.4 | Strong Bear <=-1.2
R['vol20']=lr.rolling(20).std()*np.sqrt(252)                           # terciles de la muestra -> Low / Normal / High (informa los umbrales)
R['vr']=lr.rolling(10).std()/lr.rolling(60).std()                      # expansión >=1.2, contracción <=0.7
R['er20']=(c-c.shift(20)).abs()/c.diff().abs().rolling(20).sum()      # tendencial >=0.35, mean-reverting <=0.16
rng=(c.rolling(20).max()-c.rolling(20).min())/c; R['compression']=rng<=rng.expanding(250).quantile(0.2)
R['bo_up']=c>c.rolling(20).max().shift(1); R['bo_dn']=c<c.rolling(20).min().shift(1)
R['reversal']=(np.sign(np.log(c/c.shift(10)))!=np.sign(np.log(c/c.shift(50))))&(R.trend.abs()>=0.4)&((np.log(c/c.shift(10)).abs()/(lr.rolling(50).std()*np.sqrt(10)))>1)
R['dd']=c/c.cummax()-1; R['stress']=(R.dd<=-0.10)|(R.vol20>=R.vol20.quantile(0.9)); R['crash']=R.dd<=-0.15
```
- Evidencia por celda (tendencia × vol, y cada indicador de comportamiento): para cada fuente, la serie diaria (por fecha de entrada) de ΣR / nº de estrategias de la fuente; **t = media/σ·√n_días**. Añade la E[R] mediana por estrategia de cada familia y subfamilia.
- Regla de estado:
```python
def status(days, med_trades, t_src):            # t_src: {fuente: t}
    if days<40 or med_trades<30: return 'UNKNOWN'
    ts={k:v for k,v in t_src.items() if v==v}
    sig=[k for k,t in ts.items() if t>=2]; weak=[k for k,t in ts.items() if t>=1]; neg=[k for k,t in ts.items() if t<=-1]
    if sig and len(weak)>=2: return 'COVERED'
    if sig: return 'UNDER-COVERED'
    if ts and max(ts.values())>=1 and not neg: return 'UNDER-COVERED'
    return 'MISSING'
```
  Con una sola fuente independiente, el máximo posible es UNDER-COVERED (punto único de fallo). Las correcciones del analista se permiten, pero se marcan con * y se justifican: por ejemplo, un régimen en el que la familia dominante pierde la mayor parte de su edge, o un «Strong Bear» con pocos días en episodios en V → UNKNOWN.

## Paso 8 · Estrés, tiempo y contribución
- ρ medio entre pares en días tranquilos, estrés, crash, vol alta y vol baja. ρ entre familias en esos mismos estados. Coexcedencia de colas (peor 5 %). Jaccard de estados de drawdown (bajo el agua más del 25 % del DD propio). P&L de cada familia en los días de drawdown profundo de la familia dominante y en su peor 5 % de días.
- R por año y familia (heatmap), rentabilidad anual del subyacente, peores episodios de drawdown de la cartera equiponderada (¿en qué régimen ocurren?).
- Contribución por estrategia: ρ con la familia dominante, ρ medio y máximo (y su vecino más cercano), ganancia de Sharpe al combinarla al 50 % con el núcleo, P&L en los peores días del núcleo, E[R] en vol alta, en rupturas bajistas y en la celda más infra-cubierta, holdout, MC y WF.

## Paso 9 · Robustez y sobreajuste
- Holdout post-generación: E[R] y Sharpe antes y después por estrategia y familia, cuántas quedan ≤ 0, y el error estándar ≈ σR/√n_post. **Persistencia del ranking**: Spearman de E[R] y del Sharpe entre el periodo de generación y el holdout. Avisa si el databank incluye el holdout (selección contaminada) o si ha cambiado el feed.
- Deflated Sharpe (el nº real de pruebas no suele constar: muestra una rejilla):
```python
from scipy import stats
X=DP/capital; T=len(X); sr=X.mean()/X.std(); sk=X.apply(stats.skew); ku=X.apply(lambda s: stats.kurtosis(s,fisher=False))
g=0.5772156649; V=1.0/T
emax=lambda N: np.sqrt(V)*((1-g)*stats.norm.ppf(1-1/N)+g*stats.norm.ppf(1-1/(N*np.e)))
dsr=lambda N: stats.norm.cdf((sr-emax(N))*np.sqrt(T-1)/np.sqrt(1-sk*sr+(ku-1)/4*sr**2))   # N en [n_univ,1e3,1e4,1e5,1e6]
```
- PBO por CSCV (S = 16 bloques contiguos, todas las combinaciones de 8):
```python
blocks=np.array_split(np.arange(T),16); logits=[]
for cmb in itertools.combinations(range(16),8):
    a=Xv[np.concatenate([blocks[i] for i in cmb])]; b=Xv[np.concatenate([blocks[i] for i in range(16) if i not in cmb])]
    best=np.argmax(a.mean(0)/a.std(0)); r=stats.rankdata(b.mean(0)/b.std(0))[best]/(Xv.shape[1]+1); logits.append(np.log(r/(1-r)))
PBO=(np.array(logits)<=0).mean()
```
  Aclara que se aplica sobre supervivientes: mide la inestabilidad del ranking, no todo el sobreajuste de la minería.
- Señales adicionales: parámetros y motores de salida repetidos (evolución genética de pocos padres), dependencia de un periodo (WF Efficiency > 1, mitades desiguales, año récord) y beta común (ρ con los retornos del subyacente).

## Paso 10 · Clasificación y cartera ilustrativa
- **CORE** (1-2 por fuente dominante): representante de su grupo de duplicados con el mejor holdout, MC y SQN100, y a poder ser la variante menos correlacionada con el núcleo.
- **SATELLITE**: aporta otra fuente u otro régimen (ρ baja con el núcleo, buen comportamiento en sus peores días o en celdas infra-cubiertas) y se sostiene razonablemente en el holdout.
- **BENCH / RESERVE**: el mejor representante de cada subfamilia no elegido, diversificadores con holdout débil o muestra pequeña y **cualquier estrategia con problemas de integridad de datos** (código ≠ backtest, WF ausente): esas nunca pasan de BENCH.
- **REDUNDANT / LOW PRIORITY**: todo lo demás, con el motivo (ρ máx. y vecino). Se archivan, no se borran.
- Carteras ilustrativas equiponderadas (universo, solo familia dominante, igual riesgo por familia y CORE+SATELLITE): Sharpe del backtest y del holdout, ρ con el subyacente, peor año y Ret/DD. **Avisa de que CORE+SATELLITE está sesgada por la selección**; la comparación limpia es la de igual riesgo por familia.

## Paso 11 · Gaps y prioridades de minado
- Tabla de gaps con columnas Dimensión · Estado · Evidencia · Diseño · Por qué importa. Dimensiones mínimas: dirección corta, rupturas bajistas, Strong y Weak Bear, vol alta y baja, Strong Bull con vol alta, Weak Bull, rango, mean reversion (entrada contra el movimiento), breakout y compresión, expansión, reversión, swing de varios días, scalping, cada sesión, frecuencia y market structure.
- Arquitectura objetivo por bloques (función, régimen objetivo, cobertura actual, candidatas), sin pesos si no hay evidencia OOS suficiente. Principios: presupuestar riesgo por familia, limitar la concurrencia y medir la diversificación en estrés.
- Prioridades de minado P1-P5 con el formato **Gap → Por qué importa → Qué buscar → Cómo en SQX**: dirección y tipo de orden, bloques y niveles a incluir o excluir, rangos horarios y Exit on Friday, validación por sub-periodos o regímenes, correlación con el databank «Existing portfolio», OOS reservado, registro del nº de pruebas y eliminación de duplicados con ρ ≥ 0,9 antes de la WF Matrix. **No inventes valores de parámetros.** La P5 siempre trata de cambiar el criterio de selección si PBO o DSR son malos.
- Plan de acción en 4 bloques (Immediate · Next Research Cycle · Medium Term · Validation Before Live), con columnas Qué hacer · Por qué · Problema que resuelve · Resultado esperado · Prioridad.

## Paso 12 · Informe PDF
- Termina la investigación antes de maquetar. Si dispones de skills auxiliares de visualización y PDF, cárgalas ahora; si no, las indicaciones de abajo son suficientes con matplotlib y reportlab.
- Secciones: 1 Executive Summary (respuesta corta + qué tengo / qué cubro / robustez / qué hacer) · 2 Data & Methodology (fuentes, método, tabla de discrepancias) · 3 Databank Overview · 4 Strategy Quality Analysis · 5 Strategy Clustering · 6 Diversification Analysis (lógica, dirección, horizonte y sesiones, volatilidad, tendencia, correlación y estrés, temporal) · 7 Market Regime Coverage · 8 Strategy Coverage Matrix · 9 Hidden Concentration Risks (tabla de diversificación aparente frente a real) · 10 Portfolio Contribution Analysis · 11 Strategy Gaps · 12 Robustness / Overfitting Risks · 13 Ideal Portfolio Architecture · 14 StrategyQuant Next Mining Priorities · 15 Action Plan · 16 Limitations · 17 Final Research Conclusions · Anexo con la ficha de todas las estrategias. Portada con 4 KPIs y la pregunta central.
- Gráficos (matplotlib, 200 dpi, fuente Carlito): distribuciones de métricas; composición; heatmap de correlación ordenado por clustering, con franja de familia (escala secuencial si todas las ρ son positivas, divergente si hay negativas); espectro de autovalores y simultaneidad; equity por familia y precio en un panel aparte (**nunca doble eje**); underwater por familia; R por año y familia; sesiones; matriz tendencia × vol con estados; barras de comportamiento por familia; estrés; holdout; DSR/PBO; WF/MC; dispersión de ρ con el núcleo frente al Sharpe de holdout, coloreada por clase.
- Paleta de familias (validada): `#2a78d6, #eb6834, #1baf7a, #eda100`, más marcadores distintos. Estados: cubierto `#0ca30c`, infra-cubierto `#fab219`, ausente `#d03b3b`, desconocido `#c9c8c2`, siempre con texto. Clases: CORE `#4a3aa7`, SATELLITE `#e87ba4`, BENCH `#008300`, REDUNDANT gris.
- Trucos de reportlab: la fuente Carlito tiene ρ ≥ ≤ × → ≈ ●, pero **no** ■ ◆ ▲ ✓. Escapa `&`, `<` y `>` en los Paragraph. Evita los `%` literales dentro de cadenas con formato `%`. Pon keepWithNext en los estilos H2 y H3 y mete cada figura y su pie en una **Table de una celda**: KeepTogether rompe keepWithNext y los títulos quedan huérfanos. Formato español: `f'{x:,.2f}'` → intercambia `,` y `.`.
- Revisión visual obligatoria: `pdftoppm -r 60` → hojas de contacto de 8 páginas → mira solapes de texto, títulos huérfanos y cabeceras de tabla partidas; repite a 100 dpi las páginas densas.

## Paso 13 · Verificación y entrega
- Recalcula de forma independiente, directamente desde los CSV crudos, las cifras titulares: nº de trades y de cortos, cuota larga del P&L, ρ media y mínima, pares con ρ > 0,95, PC1 y nº efectivo de apuestas, % de simultaneidad y E[R] pre y post. Todas deben casar con el informe.
- Comprueba cada número del texto frente a su fuente mientras redactas; corrige en lugar de redondear hacia la narrativa.
- Entrega el PDF y el CSV al usuario y guárdalos en su carpeta de salida. Respuesta final breve.

## Errores ya vistos (evítalos)
- Confiar en el ID del nombre de fichero sin mirar la cabecera del .mq4 (puede haber un EA de otra estrategia dentro).
- Dar por hecho que la dirección del código coincide con la del backtest.
- Tomar el «IS» del databank SQX como in-sample puro (puede incluir el holdout).
- Leer la WF Efficiency > 1 como robustez.
- Rankear las estrategias por métricas de backtest dentro de un universo con PBO alto.
- Afirmar que una estrategia «es la única que…» basándose en celdas con 1-3 trades (comprueba siempre n).
- Contar filtros o clases declaradas como diversificación sin comprobar el solape real de trades.
