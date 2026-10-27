---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
related: ["[[IMOX]]"]
aliases: []
tags: ["kind/doc", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-26"
project: "[[Estrategias IMOX — Forex y CFD con Echo Forge]]"
---

# IMOX — Registro de campañas

## Propósito

Definir una ficha canónica por campaña de [[Estrategias IMOX — Forex y CFD con Echo Forge]] y una vista derivada para distinguir lo propuesto, listo, ejecutado y aprendido. Esta nota es el contrato del registro, no un segundo historial de cada campaña.

## Contenido

### Unidad de investigación y de ejecución

- **Celda de cobertura:** carril/producto × activo/instrumento × lógica × dirección × timeframe/horizonte; sesión/régimen son dimensiones adicionales cuando cambian la tesis. El broker/feed es parte de la receta; NDX cash CFD y un futuro NQ no comparten validación por nombre.
- **Hipótesis:** comportamiento falsable que se busca explotar. Puede tener varias recetas/presets y varias campañas.
- **Familia de preset:** selección semántica de bloques, orden, filtros y salidas. La variante fija versión SQX, rangos, símbolo, sesiones y costes.
- **Campaña:** experimento con receta y criterios congelados. Agrupa ejecuciones y conserva cambios de versión como nueva campaña/receta cuando alteran la pregunta.
- **Run:** intento físico identificado por Forge. Retry técnico no es nuevo experimento; registrar el vínculo al original y outcome.
- **Cohort heredado:** material previo aún por inventariar. No fingir conocer la campaña original ni adjudicar fechas/versión/autoría no demostradas.

### Ficha mínima y campos para vistas

Materializar cada ficha como `type: doc` por el contrato del vault, en `campanas/`, con `project: [[Estrategias IMOX — Forex y CFD con Echo Forge]]`, `research_record: campaign`, `campaign_id`, `campaign_state` y rutas a evidencia. No crear un tipo paralelo de frontmatter sin contrato.

| Grupo | Contenido requerido |
|---|---|
| Identidad | ID estable propuesto `IMX-FX-AAAA-NNN`, título, hipótesis y vínculos de deriva/reutilización; reservarlo antes de ejecutarlo. |
| Cobertura | Carril, activo canónico, símbolo broker, producto, lógica, dirección, TF, horizonte y sesión/régimen. No rellenar desconocidos por inferencia. |
| Diseño | Tesis y criterio de descarte previos, receta/preset y revisión, IDs de bloques/roles, compatibilidad SQX/motor y delta respecto de su antecedente. |
| Datos | Dataset/versionado o hash, broker/feed, sesiones, costes, periodos IS/selección/evaluación y registro de qué datos vio el agente. |
| Presupuesto | Tiempo/candidatas/cómputo acordados y condición de parada. |
| Evaluación | Policy/revisión de gates, reglas congeladas, cobertura temporal, contraste de motores y qué constituye un candidato elegible. |
| Ejecución | Config/FlowRun/artefactos reales, fechas y outcome físico; por ahora no inventar un mapping a APIs de Forge. |
| Resultado | Candidatas por etapa, causas de rechazo, coste, errores, decisión y contribución al conjunto. Distinguir fallo operativo de tesis no apoyada. |
| Aprendizaje | Evidencia, límite de generalización y siguiente experimento; indicar si amerita cambiar el procedimiento de la skill. |

### Estados de campaña

`idea` → `designed` → `prepared` → `running` → `evaluating` → `closed`.

- `prepared` requiere paquete compatible y criterios previos completos; una selección de bloques en prosa todavía es `designed`.
- `blocked` puede interrumpir el ciclo con causa y condición de reanudación. `parked` es decisión de priorización.
- Al cerrar, registrar outcome separado: `candidate`, `no_edge_supported`, `inconclusive` o `execution_failed`. No cerrar como «sin edge» un error de datos/motor.
- Después de campaña, cada candidata tiene estado propio de validación/admisión/seguimiento. El estado de campaña no se recicla como estado live de la EA.
- El registro legado permanece `inventory_pending` en su frente, sin crear campañas históricas ficticias.

### Vista de campañas

```dataview
TABLE campaign_id AS ID, campaign_state AS Estado, instrument AS Activo, strategy_family AS Familia, direction AS Dirección, timeframe AS TF, recipe_revision AS Receta
FROM "10-projects/Estrategias IMOX — Forex y CFD con Echo Forge/campanas"
WHERE research_record = "campaign"
SORT campaign_id ASC
```

No hay campañas de este proyecto registradas aún. Las campañas históricas de los proyectos técnicos no se adoptan automáticamente; deben enlazarse cuando se compruebe que corresponden al material que Rodrigo quiere rescatar.

### Matriz de cobertura v0.1 — 2026-10-26

**Objetivo Owner:** registrar y estudiar al menos diez activos antes del 31-12-2026 mediante metodología genética IMOX; conservar por celda el avance hasta Forge, Echo y The Lab. Registrar diez activos no equivale a completar todas sus combinaciones ni a operar diez activos. Aquí se guardan referencias verificadas; los CFX/INI, EAs, operaciones y resultados privados se almacenan exclusivamente en sus sistemas autorizados (Forge, Echo o MinIO privado), no en el vault público.

#### Dimensiones fijas

| Eje | Valores/identidad | Regla |
|---|---|---|
| Activo | asset_id estable, p. ej. NDX o EURUSD | No inferir desde el nombre del archivo |
| Clase | INDEX, FX, METAL; catálogo ampliable | Clase económica no es producto negociable |
| Producto | product_id con contrato efectivo: CFD, FX, futuro, broker/símbolo | NDX CFD y NQ futuro son celdas distintas; sin contrato comprobado no se certifica |
| Temporalidad | timeframe explícito (H1 conocido; M15/H4 sólo posibles extensiones) | No considerar probada una escala por equivalencia visual |
| Dirección | L o S | LONG y SHORT tienen celdas distintas |
| Familia | BR; familias adicionales MR, PB, TF, FB y SE por definir | La familia económica es distinta de la firma de indicadores |
| Grupo | BR-G1 a BR-G6; otros grupos sólo tras diseñarlos | Un G1 sin prefijo de familia no es único |
| Variante | broker/feed, histórico/version, SQX build, costes, sesiones y DST | No trasladar validación entre brokers, versiones o datos |
| Firma | logical_type derivado de ClassificationSnapshot e indicator_signature.v1 | No equivale a BR-G1, ni hay firmas en casillas aún no pobladas |
| Receta | recipe_revision con refs y hashes de todas las tasks efectivas | Alterar un criterio crea revisión, no reescribe un run previo |

**Clave de celda:** IMX1 / product_id / asset_id / timeframe / direction / family_id / group_id. Ejemplo legible: IMX1/CFD-INDEX/NDX/H1/L/BR/BR-G1. La identidad real del producto se fija después de comprobar el perfil; no asignar IDs reales usando datos supuestos. Dentro de cada celda, las variantes de feed/receta preservan su evidencia y cada firma logical_type observada puede tener hasta cinco seleccionadas. La identidad/linaje durable sigue siendo StrategyRef/FlowRunRef/EvaluationRef de Forge.

**Semántica de celdas:** NR = no registrada/no probada (no es 0 ni fallo); DESIGN = familia/grupo diseñado sin ejecución certificada de esa combinación; H142(n) = cohorte SQX 142 recuperada, con n archivos (no finalistas); IMPORTED = ingesta Forge verificada; READY_IMPORT = staging sin despacho; TOP5 = 5/5 elegibles con refs de SelectionSnapshot; UNDERFILLED(n/5) = menos de cinco con agotamiento probado. Un fallo operativo no se convierte en UNDERFILLED. Un conteo 0 sólo puede registrarse con fuente que demuestre cero.

#### Catálogo inicial: seis activos + cuatro cupos vacíos

| Slot | Activo | Clase | Producto/feed | Estado |
|---|---|---|---|---|
| A01 | NDX | INDEX | USATECHIDXUSD_darwinex, CFD histórico 142 | Evidencia heredada |
| A02 | DAX | INDEX | Pendiente de verificar | Objetivo |
| A03 | USDJPY | FX | Pendiente de verificar | Objetivo |
| A04 | XAUUSD | METAL | Pendiente de verificar | Objetivo |
| A05 | GBPJPY | FX | Pendiente de verificar | Objetivo |
| A06 | EURUSD | FX | Pendiente de verificar | Objetivo |
| A07 | — | — | Por elegir | Slot reservado, no activo |
| A08 | — | — | Por elegir | Slot reservado, no activo |
| A09 | — | — | Por elegir | Slot reservado, no activo |
| A10 | — | — | Por elegir | Slot reservado, no activo |

DAX y NDX son índices, XAUUSD metal y los otros tres pares FX. No contarlos como diez pares Forex homogéneos. Para los A02–A06 se conoce el activo objetivo, pero todavía no la configuración del producto/feed/TF/dirección. Los slots vacíos no cuentan como activos procesados.

#### Proyección inicial — familia BR, H1 LONG

**Vista únicamente de la combinación H1/LONG/BR**, con G1–G6 como columnas. Las demás combinaciones y familias se mantienen NR hasta disponer de evidencia; no crear cientos de notas vacías.

| Activo | BR-G1 | BR-G2 | BR-G3 | BR-G4 | BR-G5 | BR-G6 |
|---|---|---|---|---|---|---|
| NDX | H142(727); IMPORTED | H142(555); READY_IMPORT | DESIGN | H142(1091); READY_IMPORT | DESIGN | DESIGN |
| DAX | NR | NR | NR | NR | NR | NR |
| USDJPY | NR | NR | NR | NR | NR | NR |
| XAUUSD | NR | NR | NR | NR | NR | NR |
| GBPJPY | NR | NR | NR | NR | NR | NR |
| EURUSD | NR | NR | NR | NR | NR | NR |
| A07–A10 | Sin activos asignados | — | — | — | — | — |

**Provenance:** [[IMOX — Rescate 142 en flota Forge (2026-10-25)]]. Los tres pools son distintos byte-a-byte; G4 es grupo dominante según universo de bloques, sin probar exclusividad económica. Todos son SQX 142.2399, NDX, H1, LONG. G1 pasó por Forge (TopProjection 34 y diez robust históricas) pero no hay evidencia de Top 5 definitivo **por logical_type**. G2 y G4 tienen manifiesto de import listo, sin ejecución de wave. G3/G5/G6 tienen diseño de Breakout sin pool materializado reconocido. No se declara ninguna estrategia admitida/operando en Echo por estos pools.

#### Qué registrar cuando una celda se procesa

La ficha de campaña y su vista de cobertura deben enlazar, nunca copiar desde sistemas externos: identificador y versión del Builder/config (hash), todos los configs originales y efectivos de tasks, workers, dataset y costes; pool/candidatas, ClassificationSnapshotRef, cantidad y cardinalidad de logical types, objetivo 5, RankingSnapshotRef/SelectionSnapshotRef por firma, supervivientes/UNDERFILLED/exhaustion; evaluación final SQX, contraste MT5, outcome del flujo; receipt de ingesta Echo, versión/definición operacional y ACK de aplicación; referencia de historia, trade journal, curvas/MetricSets y cortes de The Lab. Los valores no observados permanecen NULL/desconocidos, no ceros ni falsos.

**Gates independientes:** INVENTORIED → CONFIG_VERIFIED → BUILDER_OR_IMPORT_DONE → CLASSIFIED → TOP5_OR_UNDERFILLED → SQX_MT5_VALIDATED → ECHO_INGEST_ACCEPTED → ECHO_OPERATIONAL_READY → LAB_METRICS_READY. Ingesta recibida no prueba operación, ni la operación prueba que Lab calculó métricas. Distinguir error de contrato/infraestructura de rechazo económico demostrado.

#### Trabajo requerido para poblar y explotar la matriz

1. **Nuevas configuraciones de tasks SQX 144:** diseñar una receta de procesamiento única para G1/G2/G4, con CFX/INI y reglas específicas de Retester Light, rankeo, clasificación, Retester Full, WFM/Optimizer, Apply, Retester Full Precision tick, MT5, ranking de ambos motores, Top 5 por logical type, warnings e ingesta Echo. Conservar refs y hashes de configuración fuente/efectiva por ejecución. WorkflowSpec describe la orquestación y sus bindings, no sustituye las configs de las tasks. Los Builders 142 sólo aportan cohortes históricas y procedencia.
2. **Migración controlada 142→144:** conservar bytes originales y confirmar compatibilidad de templates/bloques y datos/point value/comisiones/spread/swap/DST; una conversión correcta debe demostrar import y cálculo monetario.
3. **Validación de la distribución de firmas:** contar los logical_type reales antes de dimensionar el trabajo; un Top 5 por firma puede producir más de cinco finalistas por grupo. En Dynamic Groups top_n=5, batch_size=Y, K global de concurrencia y límites de presupuesto se eligen aparte; acumular sobrevivientes de todas las iteraciones y re-rankear el acumulado íntegro por firma; exhaustion real produce UNDERFILLED.
4. **Calidad, comparabilidad y linaje:** congelar reglas IS/OOS/holdout; validar métricas procedentes de la task correcta, WFM IS seleccionado/Apply y Final Reretester de alta precisión; MT5 debe evaluar el mismo periodo y artifact lineage. No etiquetar una incompatibilidad SQX/MT5 como edge inexistente.
5. **Destino:** Forge selecciona, pero Echo es dueño de ingesta idempotente, StrategyDefinition/version, provisión y ACK runtime, señales/trade_journal. The Lab deriva historia concatenada y revisiones de curvas, métricas y rankings sin reescribir fuentes. Mantener hitos separados: finalista, ingestado, operativo, demo, real y métricas listas.
6. **Capacidad:** Hefesto ya figura integrado físicamente como worker Forge SQX 144 con guard intermitente y heap propio (journal 2026-10-26); política owner: Retester/Optimizer de hasta diez estrategias por tarea, no Builders. Verificar activo/dataset, memoria, compatibilidad y disponibilidad antes de cada dispatch. Zeus/Hera/Kronos siguen siendo Builders principales futuros.
7. **Cartera de experimentos:** diseño por hipótesis genética IMOX; no adoptar Random como default desde un comentario aislado. Priorizar huecos de familia, dirección, activo, TF y exposición; registrar descarte y diversidad estadística, no sólo conteos de EAs.

**Cobertura total versus objetivo anual:** si el owner aprobara tres TF (M15/H1/H4 como ejemplo), diez activos × seis grupos Breakout × dos direcciones × tres TF ya serían 360 celdas BR, antes de nuevas familias, productos/feed y múltiples logical types. La matriz puede representar todas como NR implícitas sin inventar campañas. Reportar separadamente activos registrados, activos con campaña, activos con candidato validado, activos en Echo, celdas con evidencia, celdas validadas y particiones Top 5/UNDERFILLED.

**Autoridades:** [[IMOX - Tipos de estrategia en trading algorítmico]], [[SQX — BR H1 LONG — Grupos, Builders y continuidad Forge-Echo]], [[IMOX — Rescate 142 en flota Forge (2026-10-25)]], [[Dynamic Groups — Shot 2 — Estado de implementación]], diseño privado de Dynamic Groups en Symphony. A 2026-10-26 la implementación de Dynamic Groups sigue candidata sin prueba física E2E, release ni deploy; Forge→Echo→The Lab tiene gates independientes aún por certificar.


### Cierre compartido de pools BR-G1/G2/G4 — receta propuesta EVAL-144 (2026-10-26)

**Secuencia exigida:** F0 = certificación física completa en TEST con fixtures y datos descartables, incluyendo MT5, Echo y analítica The Lab, antes de usar cualquier grupo histórico → F1 = cierre de los pools NDX H1 LONG BR-G1 727, BR-G2 555 y BR-G4 1091, con **configs de todas las tasks nuevas para SQX 144** → F2 = replanteo por familia/grupo y múltiples configs calibradas, criticando los seis grupos anteriores con GLM-5.3-Flash Max → F3 = campañas genéticas continuas para llenar la matriz. F0 no se certifica sobre pools históricos ni se declara PASS por tests parciales del motor.

**Estructura de investigación:** familia = mecanismo económico; grupo = hipótesis de subfamilia; config = variante genética calibrada y versionada de Builder; pipeline = cadena de evaluación versionada común; campaña = intención e hipótesis falsable aplicada a una celda/config; run = intento físico; logical type = clasificación observada de estrategias dentro de cada campaña/grupo. No equiparar grupo y logical type; no limitar a seis los nuevos grupos. Los grupos antiguos no se replicarán a otros activos hasta review y aprobación.

| Orden | Task EVAL-144 | Evidencia / gate |
|---|---|---|
| 00 | Preflight de cohorte + perfil | StrategyRefs y hashes congelados, SQX build/activo/datos/costes/DST válidos, selección de worker por capacidad |
| 01 | Retester Light | Evaluación rápida exacta, errores operativos separados de rechazos económicos |
| 02 | Ranking preliminar Retester | Score/policy explícita; preservar universo completo para clasificar por tipos sin sesgo del top global |
| 03 | Clasificación / group | ClassificationSnapshotRef; particiones por logical type; lotes iniciales Y=10, target X=5 por partición, reposición y EOF medibles |
| 04 | Retester Full | Métricas/evidencia por candidato, producto y ventana comparables |
| 05 | WFM / Optimizer | Fuente post-retest correcta, runs y sus ventanas IS/OOS identificadas |
| 06 | Selección run + Apply | Regla de selección aprobada pendiente; nuevo StrategyRef/version con parámetros elegidos y readback, original inmutable |
| 07 | Retester Full Precision tick | Backtest SQX tick real sobre el período del run elegido, sin falsificar modo ni fechas |
| 08 | MT5 | EX5/INI por instancia, mismo período/parámetros/estrategia aplicada, evidencia de backtest efectivo |
| 09 | Reconciliación SQX + MT5 y ranking final | Comparabilidad, tolerancias y pesos definidos antes de usar resultados; ranking de elegibilidad conjuntiva y ScoreRefs |
| 10 | Selección Top 5 | Rerank del acumulado completo de cada logical type y entrega 5/5 o UNDERFILLED(n/5) sólo con agotamiento demostrado |
| 11 | Warnings y reporte | Desde cualquier task: INFO / WARN / BLOCK (un BLOCK impide promoción); GLM-5.3-Flash Max genera reporte factual por campaña/grupo y revisión manual asistida de coherencia de familia de finalistas |
| 12 | Ingesta Echo | Intake idempotente autorizado, StrategyDefinition/version, ACK y provisioning diferenciado de activación |
| 13 | The Lab | Historia pre/post construcción y Echo, relación trade_journal, curvas/MetricSets, readiness analítica independiente |

**Brief previo GLM-5.3-Flash Max:** descripción de intención, ventaja y régimen buscados; familia/grupo/config, entrada/salida, exclusiones, activo/TF/dirección, presupuesto, falsación y criterios. **Reporte posterior:** funnel con conteos por etapa y logical type, métricas y períodos efectivos, resultados SQX/MT5, warnings, fallos operativos, ranking/Top5/UNDERFILLED, divergencias, diversidad/correlación, decisión y siguiente hipótesis, citando evidence refs. El modelo ayuda a revisar manualmente la pertenencia a familia, pero no sustituye la clasificación persistida ni las validaciones deterministas.

**Regla científica:** tick SQX y MT5 sobre el IS seleccionado demuestran concordancia de motores, no independencia del OOS. Conservar un holdout que no se use para ajustar configs ni scores. Ninguna conclusión de rentabilidad extrapolada por el modelo.

**Checkpoint de cierre por grupo:** G1 importado en Forge, G2/G4 READY_FOR_IMPORT; los tres siguen PENDIENTES de EVAL-144 completo. Los resultados para cada grupo quedan separados por refs y se agregan mediante la misma sección del proyecto. Echo ingestado, Echo operativo, demo/real y The Lab listo son hitos diferentes.

**Decisiones abiertas de Owner para congelar antes de F0:** ranking final combinando SQX Full Precision y MT5 (fórmula/pesos/tolerancias), política WFM de elección del run, split IS/OOS/holdout, criterios económicos de elegibilidad, límites de cómputo/reintentos, autorización de inyección y activación Echo. No inventar números.

### Reutilización y mejora

Mantener el padre reusable y su variante separados. Cambiar broker obliga a validar producto/costes/feed; cambiar TF obliga a revisar horizonte, frecuencia, rangos y muestra; cambiar long/short obliga a comprobar simetría económica y de bloques. Transferir una hipótesis no transfiere su resultado.

Las mejoras del procedimiento se aplican por delta durable, con fuente/fallo que lo justifique y comprobación en un caso concreto. Guardar `methodology_revision` en las campañas; conservar la evaluación original y reanalizar con una revisión nueva sin sobrescribirla.

## Fuentes

- [[Estrategias IMOX — Forex y CFD con Echo Forge]]; petición expresa de Rodrigo de planificar hasta fin de año y diferir rescate.
- [[IMOX - Building Blocks Skill]] · [[IMOX - Tipos de estrategia en trading algorítmico]] · [[IMOX - SQX automatizado - Hipótesis, sondas y ejecución]].
