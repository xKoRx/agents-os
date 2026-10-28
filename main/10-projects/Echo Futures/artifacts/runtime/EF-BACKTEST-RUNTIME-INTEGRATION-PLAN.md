---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — Runtime Pools]]"
  - "[[Echo I+D — Futures]]"
  - "[[FUT-R01-RESEARCH-MANDATE]]"
  - "[[ECHO-FUTURES-RUNTIME-POOL-DESIGN]]"
  - "[[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]"
aliases:
  - "Echo Futures — Plan de integración Backtester y runtime"
tags:
  - kind/doc
  - area/echo
created: "2026-10-28"
updated: "2026-10-28"
---

# EF-BACKTEST-RUNTIME-INTEGRATION-PLAN

## Propósito

Preparar la convergencia de los experimentos del Backtester con el modelo vigente del runtime, de forma que una sesión registrada pueda reproducirse y contrastarse con la misma lógica de Strategy, MM, cuenta y ejecución. Mandato directo Owner del 2026-10-28: **planificación y diseño**, sin implementación ni pruebas nuevas.

**Estado: DESIGN_CANDIDATE / READY_FOR_REVIEW; no implementation-ready ni autorización de merge, despliegue u órdenes.** Este artefacto pertenece a [[Echo Futures]], owner de producto, enlazado desde FUT-R01 para coordinar necesidades de investigación. No crea otro proyecto, planner, motor, skill ni SPEC congelado. El siguiente retorno es una recuperación read-only acotada de Hefesto.

## Contenido

### 1. Decisiones, alcance y autoridades

- Strategy conserva la ficha simple aceptada: setup, filtro y objetivo/riesgo o RR. MM por prop/programa/etapa es otra entidad. La integración no mueve fórmulas ni salidas entre entidades para facilitar el portado.
- NQ es el instrumento autorizado. La reproducibilidad identifica el contrato negociado, calendario, roll y precios sin habilitar MNQ.
- Capital económico vigente: USD 4.000 Futures; Forex tiene aproximadamente USD 2.000 separados. La meta de dos props simultáneas exige medir concurrencia y caja conjunta, no sólo campañas individuales.
- Las cinco estrategias challenge y las cinco funded pueden ser las mismas, diferentes o una mezcla. Esta decisión no concede aptitud técnica/económica.
- Arquitectura vigente: R6 de [[ECHO-FUTURES-RUNTIME-POOL-DESIGN]], complementada por GOD-02 bajo las enmiendas M01–M07 de [[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]. Preservar los freezes, ownership y gates aplicables.
- GOD-05 excluyó la migración Backtester/Lab de su implementación anterior. Este **nuevo mandato documental** permite diseñarla; no amplía retroactivamente PRD ni certificaciones.
- La antigua fase S05/adopción runtime de [[Echo Futures — Optimización de Campañas]] quedó superseded por la rectificación Owner de cuatro shots del 21-10. Se reutilizan sus requisitos pertinentes, sin reactivar ese despacho.
- Los G0–G5 de cualificación de estrategias continúan vigentes. Los criterios de integración de este documento no los sustituyen ni redefinen.
- No se modifica el runtime en pruebas ni la infraestructura compartida con Forex/Echo Forge. No se ejecuta cierre formal de sesión.

### 2. Baseline observado y límites de evidencia

Cortes leídos en GitHub, no inspección física de Hefesto:

| Superficie | Identidad / estado observado | Alcance |
|---|---|---|
| Echo master | d74b652500e673fc2bf4289f9f195f11960ba26e | Ancestro común observado |
| Backtester/Lab | experiment/campaign-lab-s04 @ ae1b09bc10370806f7648f076c5fa0825c9efa4e | 77 commits sobre el ancestro común |
| Runtime | feature/ef-runtime-pools @ bcffcf310c5825cd7b1c434158ee160a93b45c47 | 172 commits sobre el ancestro común; ramas divergentes |
| Planner Runtime Pools | Encabezado todavía referido a 5a0cf62f | No usar ese encabezado para invalidar receipts posteriores |
| Último receipt recuperado | WINDOW-CARD-PRD6, ventana del 27-10: DEV_RO_OPERATIONAL | Observación DEV, NEW_RISK=BLOCKED, cero órdenes; no prueba PROD |
| Binarios consignados en ese receipt | Core dede64436a931d33f6ef44ee20f36204336f5fab; CLI 006857b8 (abreviado por la fuente) | Distintos del HEAD fuente bcffcf31 |
| Información posterior del Owner | El runtime nuevo está en pruebas PROD | Declaración aceptada como contexto operativo; falta vincular ambiente, binarios y alcance de esas pruebas |

El compare devuelve 300 archivos y está truncado: **no es inventario completo de conflictos**. Fuente, checkout, binario desplegado, configuración y certificación son identidades separadas. El receipt DEV previo no refuta la información posterior del Owner. La inspección de código tampoco acredita ejecución física. [S1–S4]

### 3. Hallazgos que determinan la integración

| Superficie | Evidencia concreta | Implicación de diseño |
|---|---|---|
| Dominio compartido | Backtester compone Strategy/MM, Operation, Provider, market/analytics y ledger mediante SDK; usa CompositionFactories | Conservar una implementación de dominio. Reconciliar composición, disponibilidad y drivers; compartir imports por sí solo no demuestra paridad |
| Registro de Strategy | El corte Lab resuelve FBC/ORB/MR además de S1/S2/fixture/TG; el runtime leído registra S1/S2/fixture/TG | Integrar registro/configuración/requisitos y su consumidor, no copiar sólo los archivos de señal |
| MM y AccountPolicy | Lab resuelve RGMM y una política RG sellada; runtime compone catálogo versionado y AccountPolicy para Gerard/TG | Portar de forma coherente los contratos requeridos; verificar snapshots/keys, política, unidades y ausencia de estado mutable compartido |
| Restricción RG | La composición RG de Lab rechaza LIVE explícitamente como HISTORICAL_POLICY_ONLY | No quitar la guarda para hacer funcionar un merge. Determinar qué semántica es reutilizable y diseñar soporte runtime explícito, con revisión de producto y validación propia |
| Analytics/filtros | Lab integra MR, TG preparado y filtros con vistas causales; R6 exige unión deduplicada de demandas Strategy+MM y observaciones por consumidores | Contrastar streaming/preparado, disponibilidad, calendarios, warmup y reinicio. No duplicar cálculo por cuenta ni introducir un acceso a estado futuro |
| Selección de cuentas | Platform conserva cuentas y rota un turno físico tras vaciado; R6 usa asociaciones, claims, afinidad y arbitraje por cuenta | Un selector de campaña no demuestra multipool concurrente. El runner offline debe consumir la misma semántica de pool/provider |
| Política de presupuesto | R6 prescribe MM_ENTRY_BUDGET_UNCLIPPED_V1 en pools; la semántica histórica STRATEGIC_ENTRY_BUDGET_V1 permanece identificada | Reproducir legacy con su política. Un experimento con nueva política tiene identidad y resultados nuevos; no exigir igualdad histórica artificial |
| Caja histórica | platform_campaign.go inicializa USD 5.000 y cobra compra fija USD 120; researchCashEnabled evita declarar ruina | No acredita supervivencia con USD 4.000 sin aportes. Diseñar caja finita y costes por perfil sin sobrescribir resultados anteriores |
| Funded aislado | FUNDED_ONLY omite adquisición/evaluación/setup fees; existe límite de cuatro payouts por política histórica de campaña | Útil para una fase, insuficiente para economía end-to-end. No convertir esas constantes en reglas universales de proveedor |
| Reproducción | ReproduceCampaign leído reconstituye SealedCampaignRequest y llama RunCampaign | No se ha acreditado un reproductor equivalente completo para Platform ni para sesiones físicas actuales; recuperar lo existente antes de construir |
| Ejecución simulada | README declara OHLC modelado y límites del venue: no cola, profundidad o latencia real observadas | Separar fidelidad de dominio, replay de hechos de ejecución y estimación de fills |

La evidencia de código corresponde sólo a los cortes y archivos citados. La ausencia de soporte en la composición observada no demuestra que no exista trabajo local posterior. [S5–S12]

### 4. Modelo objetivo propuesto: dominio único y adaptadores explícitos

**Conservar el SDK como dueño de reglas compartidas y reducers; runtime y Backtester componen las mismas autoridades con entradas/transporte propios.**

| Responsabilidad | Autoridad que se reutiliza | Diferencia legítima por entorno |
|---|---|---|
| Mercado y tiempo causal | Eventos normalizados, calendario/contrato, disponibilidad y reloj por transición | Feed vivo o registro histórico; reloj virtual reproduce los tiempos registrados |
| Analytics | Requisitos de Strategy+MM, kernels, observaciones, warmup/readiness | Transporte/caché/preparación, con equivalencia causal demostrada |
| Strategy | Una evaluación y estado técnico por strategy_id; Signal inmutable | Transporte del input y persistencia del estado |
| Asociación/pool | pool_id, strategy_id, MMConfigRef/version; selección, FIFO, claims, afinidad y drenaje | Adaptador StateFun o conductor offline de los mismos contratos/reducers |
| MM/Operation/Provider | MM sellado por Operation; política/admisión/reservas; ledger y reglas por cuenta | Hechos recibidos de la ejecución real, observada o simulada |
| Ejecución | Intenciones, correlación, ACK/reject/fill/cancel/finality y protección | Transporte físico, reproducción de hechos registrados o venue simulado versionado |
| Campañas e investigación | Orquestación de compras, activación, cobros, búsqueda y reportes | Laboratorio; no se incorpora al PoolManager |

Cardinalidades vigentes R6: máximo una cuenta activa por asociación; exclusividad de cuenta entre claims; varias asociaciones/pools pueden coexistir. No introducir múltiples estrategias en una cuenta ni varias cuentas activas por asociación sin decisión de producto. Para dos props simultáneas, representar asociaciones/cuentas separadas y medir su concurrencia efectiva.

Strategy y analytics siguen funcionando cuando una cuenta pausa o rota. El MM y estado financiero no se filtran de una cuenta a otra. Los fills tardíos conservan su cuenta, Operation y generación originales. La rotación no se justifica sólo porque una posición aparezca plana.

**Modularidad concreta:** agregar una Strategy/MM requiere su módulo, configuración, demandas analíticas y política compatible. No requiere otro scheduler, ledger ni venue. Backtester no importa Core/internal; si falta una función compartible, su extracción mínima al dueño SDK se propone y revisa antes de implementar. No se introduce DSL, motor universal, segundo bus ni nueva base de ticks por esta integración. [S3, S5–S9]

### 5. Qué significará “replicar una sesión”

| Comprobación | Entradas requeridas | Resultado exigido / límite |
|---|---|---|
| Decisiones de dominio | Mismo código/semántica, configuración, estado inicial, datos causalmente disponibles y orden relevante | Mismos setups/filtros, señales, rechazos, decisiones MM, claims/reservas e intenciones de orden |
| Sesión con ejecución observada | Lo anterior más ACK/rechazos/fills/cancel/finality, comisiones y revisiones contables reales | Mismas transiciones y ledger explicables. El replay consume hechos registrados y no envía órdenes a un venue |
| Backtest con fills simulados | Señal/dominio compartidos y modelo de ejecución explícito | Resultados del modelo versionado, con costes y supuestos soportados declarados; cualquier latencia utilizada requiere semántica implementada y explícita. No certifica fills históricos exactos |
| Histórico OHLCV 1m | Barras, calendario, disponibilidad y modelo intrabar declarado | Investigación al alcance de esos datos; no certifica secuencia real de ticks/BBO ni cola |

Para comprobar decisiones pueden readmitirse snapshots económicos autoritativos registrados. Para afirmar reproducción o validación contable, el ledger se reconstruye desde hechos primarios de ejecución, fees, ajustes y estado inicial, y se contrasta con las revisiones registradas. Si sólo se consumen revisiones originales, el resultado se limita a paridad de decisiones sobre economía suministrada; no certifica el productor contable.

El replay de la sesión real requiere **también el contexto que el motor vio**, no sólo descargar después precios del mismo día. Deben preservarse el warmup/estado inicial, los momentos de disponibilidad, las decisiones de control y los hechos de ejecución.

Si una intención de orden difiere, detener el dictamen de equivalencia en la **primera divergencia causal**. No introducir después los fills originales como si pertenecieran a una orden distinta. El informe clasifica la causa: código, config/política, dato/orden/disponibilidad, reloj, estado inicial, control o ejecución.

Comparar dinero en unidades exactas y precios/cantidades según instrumentos. La normalización de IDs o campos propios del modo debe documentar una correspondencia que conserve toda causalidad; no usar tolerancias para ocultar señales u órdenes diferentes. Cualquier tolerancia numérica debe justificarse antes del ensayo. La coincidencia de PnL agregado no sustituye estas comparaciones.

La paridad no prueba correctness: además se necesitan oráculos independientes de conservación de dinero, límites/protección, elegibilidad, no lookahead y finality. Reutilizar pruebas válidas existentes cuando su identidad/cobertura las hagan aplicables. [S5, S11, S12]

### 6. Paquete mínimo de captura y reproducción

Se propone reutilizar RunSpec/identidades/receipts, recording y journal existentes. El retorno read-only debe mapear cada campo a una superficie real antes de diseñar otra persistencia.

| Grupo | Contenido mínimo para decidir si una sesión es reproducible |
|---|---|
| Identidad | Commit/build digest de cada componente relevante; modo; versiones de esquema y modelo; Strategy/config/filtros; MM sellado; Provider/Program/RuleSet y política presupuestaria |
| Inicio | Estado/checkpoint verificable o prefijo causal suficiente; cuentas, fase, balances, reservas, órdenes/posiciones/Operations pendientes; afinidades/claims y generaciones; warmup/readiness |
| Mercado | Contrato real, catálogo, tick size/unidades, calendario/sesión/DST/roll; eventos que consumió el runtime; stream/epoch, secuencia, event time y tiempos efectivos de recepción/disponibilidad |
| Analytics | Demanda y versión, insumos y observaciones/vistas entregadas, completitud, frontier y cut causal; procedencia de datos preparados |
| Control y tiempo | Cambios de configuración, armado/pausa, timers/watermarks relevantes, desconexión/recovery, fencing/epochs y transiciones de día; reloj inmutable por transición |
| Ejecución/cuenta | Intenciones y correlaciones, ACK/reject, fills parciales, cancel/finality, fees, ajustes y transiciones de fase; revisiones contables originales como referencia de comparación y snapshots externos identificados cuando sean entradas de autoridad; identidad de hechos tardíos y deduplicación |
| Integridad | Manifiestos, digests, rango y gaps explícitos, orden por owner/lane y dependencias entre owners; comprobación de que el corte representa lo efectivamente procesado |
| Resultado | Traza y ledger por cuenta/Operation/Strategy/MM; primera divergencia, cobertura y limitaciones; localizadores durables de evidencia |

No se presupone que exista un orden global único de todos los mensajes: recuperar orden por lane/owner y relaciones causales necesarias. M1/checkpoints y M2/venue son garantías distintas; no inventar atomicidad entre Flink, PostgreSQL y broker. Un hash de archivos no acredita completitud de captura. Si faltan hechos, declarar el alcance recuperable y el faltante; no sintetizarlos como evidencia observada. [S3, S4, S10–S12]

### 7. Estrategia de reconciliación de ramas propuesta

1. Fijar SHAs reales y estado local, con inventario completo de cambios por propietario y unidades de dependencia. Clasificar: reutilizable, adaptador, sólo Lab, superseded o conflicto.
2. Usar **como candidato** un corte runtime aceptado por su owner como base de convergencia del SDK. El HEAD más nuevo no es automáticamente el corte aceptado/desplegado. La decisión se fija después del retorno de Hefesto.
3. Preservar el corte experimental y sus artefactos para reproducción histórica. Integrar unidades coherentes de Strategy/MM/analytics/config/política; no cherry-picks aislados que compilen con contratos incompatibles ni un merge total sin adjudicar conflictos.
4. Mantener drivers/reportes/campañas propios del laboratorio. Adaptar su composición a contratos actuales, sin traer infraestructura física ni compras al dominio de pool.
5. Construir un primer recorrido completo acotado: fixture existente para plumbing si aplica y **TG como candidato técnico por estar registrado en ambos cortes**, con configuración soportada y explícita. Esta selección no prioriza TG por rentabilidad. FBC/ORB/MR y RG se incorporan después de resolver sus requisitos.
6. Versionar todo cambio legítimo de política, modelo o input económico. No reetiquetar resultados legacy como runtime-ready.
7. Sólo cuando se autorice implementación: usar el flujo SDD vigente del repo Echo y checkout/worktree aislado, fronteras de archivos y revisión independiente. Este documento no crea rama ni entrega un AllowedFiles definitivo antes de conocer conflictos/WIP.

### 8. Hitos propuestos y aceptación

No se inventan fechas, capacidad de Hefesto ni throughput. El orden es por dependencias; cada fase ejecutable necesitará presupuesto acordado. La estimación se anclará en archivos/conflictos, disponibilidad de fixtures/datos y pruebas reutilizables.

| Hito | Resultado/evidencia de salida | Responsable y dependencias | Aceptación y condición de reconsideración | Coste / decisión |
|---|---|---|---|---|
| R0 — recuperar baseline físico | Manifest de ramas/binarios/config, diff completo por propietario, índice de receipts/fixtures/capturas; gaps presentes/ausentes/desconocidos | Worker local read-only en Hefesto; owners Runtime/Backtester, WIP compartido | Cada afirmación crítica tiene SHA/localizador o UNKNOWN. Parar ante falta de acceso/permiso o necesidad de mutación | Una recuperación acotada; sin tests/campañas. Confirmar capacidad local antes del despacho |
| D1 — cerrar diseño de convergencia | Corte candidato, matriz de conflictos/contratos, primer recorrido, política de presupuesto, alcance de replay y plan SDD | Owner producto + manager, con R0 y este diseño | No ambigüedad Strategy/MM, cuentas, autoridad temporal o RG-LIVE. Cambio material se eleva al Owner | Coste según conflictos reales; Owner revisa decisiones y autoriza implementación acotada |
| I1 — recorrido offline compartido | Composición que usa contratos SDK/R6, Strategy/MM sellado y driver offline; recibos de decisiones/ledger | Ejecutor autorizado; D1, fixtures reutilizables | Igualdad de dominio bajo entradas equivalentes y oráculos independientes. Parar ante dependencia de Core/internal o duplicación del motor | Estimar tras D1; no compras ni infraestructura física |
| I2 — módulos experimentales | Registro/config/filtros/analytics y MM/policy reconciliados para módulos seleccionados | Ejecutor + revisión independiente; I1 y requisitos por módulo | Sin deriva no declarada; TG/MR/preparado equivalentes cuando comparten insumos; RG conserva guarda hasta soporte explícito aceptado | Selección mínima por necesidad real; no obligar a portar todo el catálogo |
| V1 — sesión observada | Paquete de una sesión real disponible + comparación causal y contable; primer desvío o coincidencia | Verificador local independiente; I1, módulo incluido, captura completa | No órdenes externas; equivalencia sólo dentro del alcance demostrado. Si faltan datos, clasificar gaps y proponer captura futura autorizable | Coste dominado por captura/integridad, no horas ficticias. Nueva captura física requiere autorización propia |
| V2 — multipool y economía comparable | Evidencia de dos perfiles/props coexistiendo, aislamiento, pausa/rotación, tardíos y caja finita; legacy reproducible | Owners de producto/lab + verificador; contratos/policies y reglas identificados | Concurrencia demostrada, no dos runs seriales agregados; caja USD 4.000 sin aportes implícitos; costes completos en el ciclo apropiado | Presupuesto separado para pruebas/campañas. Programas comerciales y gasto siguen reservados al Owner |
| A1 — adopción del candidato | Paquete inmutable, veredicto independiente, documentación y clasificación de evidencia reutilizada/invalidada | Manager técnico + Owner; hitos anteriores según alcance | No deuda crítica oculta. Los gates de estrategias y de ejecución física mantienen su autoridad | Integración aceptada no habilita PROD. Rollout y operación requieren decisiones posteriores |

V1 puede preceder a incorporar módulos no necesarios para esa sesión. Las actividades que compartan archivos/SDK se serializan; investigación externa A/B/C puede continuar en paralelo. WIP/capacidad real se acuerdan con Hefesto/Echo Forge.

### 9. Casos de aceptación indispensables

Son criterios propuestos, no tests ejecutados:

- Igual input disponible y estado → igual señal y filtro; evitar lookahead en H1, VWAP, cierre RTH, warmup y cambio de contrato/DST.
- Igual señal/config/observaciones/estado de cuenta → igual decisión MM, elegibilidad, reserva y orden.
- Pausa, pérdida de elegibilidad, día nuevo, claims concurrentes y rotación respetan R6; no reinician Strategy ni contaminan otra cuenta.
- Reconexión, duplicados, parciales, cancelación tardía y fill del predecesor conservan identidad y protección; no se convierten en eventos de la cuenta sucesora.
- Nueva revisión MM no altera Operations selladas anteriores; módulo/política ausente falla explícitamente.
- Mismos hechos primarios de ejecución, fees, ajustes y estado inicial → mismo ledger; las revisiones originales sirven de referencia de comparación. PnL agregado coincidente con traza distinta falla equivalencia.
- Dos asociaciones de proveedores diferentes están activas simultáneamente en el ensayo que lo declara, con exposición agregada y caja compartida correctamente atribuida.
- El modo de caja finita no toma fondos de Forex ni aportes research; beneficios no cobrados no financian compras. FUNDED_ONLY identifica costes excluidos.
- Legacy conserva sus identidades/políticas; la nueva integración no modifica sus recibos ni reutiliza su PASS en otro SHA por inferencia.

Seleccionar del corpus existente los casos que ya prueban estos contratos. Ampliar pruebas sólo por riesgo concreto o gate requerido; no repetir campañas válidas por antigüedad de conversación.

### 10. Primer mandato ONE-SHOT — recuperación de Hefesto

**Pregunta:** ¿qué cortes, contratos, datos, receipts y estado operativo reales permiten fijar el primer recorrido Backtester→SDK/runtime sin tocar servicios ni repetir cómputo?

**Autoridad:** en sesión nueva ejecutar bootstrap de xKoRx/agents-os, master, main/AGENTS.md; recuperar este documento y las autoridades enlazadas. Usar el README canónico v3/backtester/README.md y el SDD/reglas del repo Echo. El alcance de este encargo es lectura; la instrucción Owner prevalece sobre automatismos de cierre. No asumir acceso por haber recibido el prompt.

**Entradas:** SHAs de §2, modelo R6/GOD-05, receipts PRD/FEFB y artefactos del Lab que ya existan. El Owner informa pruebas PROD; identificar su evidencia actual sin presumir que el receipt DEV sea el último hecho físico.

**Entregables:**

1. Branch/HEAD/worktree y dirty state, sólo nombres/estado necesarios, sin secretos; relación con los SHAs de §2. No reset, checkout destructivo ni cambio de rama de un worktree ajeno.
2. Diff completo por propietario entre cortes; matriz de módulos, configuración, MM sellado, AccountPolicy, analytics, pools/rotación, driver y replay. Separar evidencia de ausencia de ausencia de acceso.
3. Identidad de componentes desplegados en el entorno reportado, configuración/policy IDs, postura de riesgo y receipt existente; inspeccionar únicamente superficies de lectura autorizadas. No inferir permisos de operación desde nombres históricos de cuenta.
4. Índice de fixtures/tests/receipts existentes aplicables, con SHA, alcance y gate; **sin ejecutarlos**.
5. Índice de capturas/manifiestos disponibles para una sesión: warmup/inicio, mercado, disponibilidad/orden, control, ejecución y cuenta. Evaluar completitud documental, sin iniciar capture/replay ni afirmar equivalencia física.
6. Propuesta de primer recorrido y corte, bloqueos materiales, coste estimable con supuestos y próxima decisión del owner técnico.

**Presupuesto:** un worker ONE-SHOT, una pasada enfocada y como máximo una reparación de localizadores. Sin campañas, pruebas, modelos de optimización ni ampliación a otros mercados. Si el acceso no existe, devolver lo verificable y la dependencia concreta; no agotar tiempo probando accesos no autorizados.

**Refutadores/criterios:** hashes/localizadores verificables o UNKNOWN; no transformar un archivo existente en PASS ni un histórico en estado operativo actual. Sin diffs completos, captura suficiente o identidad binaria, no declarar implementation-ready ni replay certificado.

**Parada:** al entregar el paquete o encontrar un bloqueo de acceso/autoridad material. Prohibido compilar, ejecutar motores/tests/replays, instalar, reiniciar, migrar, desplegar, armar, comprar o enviar órdenes por este mandato.

**Retorno y persistencia:** informe en las superficies canónicas existentes, con fuente por hallazgo, estado, riesgos y siguiente acción. Si se autoriza la escritura documental local, un único responsable publica el retorno bajo este artefacto y reconcilia HEAD de Agents-OS/master sin ramas/PRs. Si el worker no puede publicar, devuelve contenido y localizadores al manager; no inventa publicación. Aplicar agent-run/feedback sólo cuando corresponda a su alcance y declarar recursos/consumos comprobados o UNKNOWN. No cierre formal de sesión del programa.

**Estado de despacho:** PREPARADO, no ejecutado en Hefesto. Esta sesión Cloud sólo leyó fuentes y prepara/persiste documentación.

### 11. Decisiones abiertas y continuidad

Antes de implementar: fijar corte de convergencia aceptado, alcance de soporte runtime para RG, primera sesión/módulo y fronteras de archivos, presupuesto local y dueño de cada cambio. La propuesta de arquitectura reutiliza R6; cualquier cambio de identidad/cardinalidad o política económica vuelve al Owner.

Antes de operación comercial: Provider/Program/RuleSet actuales, reserva/pérdida máxima/desembolsos, semántica bruto/neto del retiro objetivo y gates físicos aplicables. Esos puntos no impiden terminar este diseño ni el Deep Research.

Próximo paso técnico: revisar este candidato con el owner de producto y recuperar R0 mediante el mandato anterior. Próximo paso de investigación: ejecutar externamente [[FUT-R01-RESEARCH-MANDATE]] v3 y devolver informe/fuentes al manager. No cerrar FUT-R01 por entregar un prompt o plan.

## Fuentes

Las fuentes de Agents-OS se leyeron inicialmente en f844162d3305e6ce9441dd11598aa1a69e753164 y se reconciliaron para publicación; los enlaces congelados mantienen la procedencia de afirmaciones. Los commits de Echo son cortes de source, no certificaciones.

- **S1 — ramas:** [compare Lab→runtime](https://github.com/xKoRx/echo/compare/ae1b09bc10370806f7648f076c5fa0825c9efa4e...bcffcf310c5825cd7b1c434158ee160a93b45c47).
- **S2 — R6:** [ECHO-FUTURES-RUNTIME-POOL-DESIGN](https://github.com/xKoRx/agents-os/blob/f844162d3305e6ce9441dd11598aa1a69e753164/main/10-projects/Echo%20Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md), §§10,12–18.
- **S3 — producción:** [GOD-05](https://github.com/xKoRx/agents-os/blob/f844162d3305e6ce9441dd11598aa1a69e753164/main/10-projects/Echo%20Futures/artifacts/runtime/production-readiness/EF-PROD-GOD-05-MANAGER-ADJUDICATION.md), M01–M07.
- **S4 — receipt:** [WINDOW-CARD-PRD6](https://github.com/xKoRx/agents-os/blob/f844162d3305e6ce9441dd11598aa1a69e753164/main/10-projects/Echo%20Futures/artifacts/runtime/production-readiness/implementation-evidence/WINDOW-CARD-PRD6.md), veredicto del 27-10; [planner Lab](https://github.com/xKoRx/agents-os/blob/f844162d3305e6ce9441dd11598aa1a69e753164/main/10-projects/Echo%20Futures/agentes/Echo%20Futures%20%E2%80%94%20Optimizaci%C3%B3n%20de%20Campa%C3%B1as.md), rectificación Owner cuatro shots.
- **S5 — contrato Backtester:** [README](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/README.md), arquitectura/paridad, modos y límites.
- **S6 — composición Lab:** [SDK composition.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/sdk/futures/config/composition.go).
- **S7 — composición runtime:** [SDK composition.go](https://github.com/xKoRx/echo/blob/bcffcf310c5825cd7b1c434158ee160a93b45c47/v3/sdk/futures/config/composition.go).
- **S8 — runner:** [compose.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/compose.go) y [compose_account.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/compose_account.go).
- **S9 — analytics/filtros:** [mr_analytics.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/mr_analytics.go), [tg_compose.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/tg_compose.go), [compose_entryfilters.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/compose_entryfilters.go).
- **S10 — economía Platform:** [platform_campaign.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/platform_campaign.go) y [Challenge History SPEC](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/specs/FEAT-CHALLENGE-HISTORY/SPEC.md).
- **S11 — identidades:** [identity.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/identity.go).
- **S12 — reproducción:** [replay.go](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/replay.go).
