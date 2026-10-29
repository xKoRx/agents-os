---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo I+D — Futures]]"
  - "[[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---

# EF-CAMPAIGN-MODES-DESIGN

## Propósito

Mantener el diseño único de CHALLENGE, FUNDED y SIMULATION sobre el Backtester existente. Esta revisión C03 corrige F01–F03 de C02, reconcilia SOURCE S04 y prepara el incremento I0 autorizado por la instrucción Owner «diseña y comencemos la implementación». C01 original permanece recuperable en `8c79805ef5a558369f83fd6f55c82835d7e778ad`; C02 conserva su informe sin edición. Este documento no acredita código ejecutado, aceptación económica, campañas, compras ni despliegues.

**Revisión vigente: C03, 2026-10-28 America/Santiago. Rol: GOD; superficie: CLOUD; función: manager técnico existente. CURRENT_TASK_STATE: CONTINUATION. DELIVERY_STATE: READY_FOR_AUTHORIZED_IMPLEMENTATION sólo para I0 descriptivo/no-spawn. IMPLEMENTATION: NOT_STARTED / LOCAL_HANDOFF_READY. OWNER_ACCEPTANCE: REVIEW. S04_SEMANTIC_ACCEPTANCE: BLOCKED_EVIDENCE (S04-F01). PROD: FROZEN_BY_OWNER.**

I0 usa el source observado `xKoRx/echo@2baf319ddcba622d9557bc9f23a13787b44c58a7` para una proyección opt-in, sin alterar ni certificar sus políticas de trading. La orden Owner permite preparar y comenzar este slice acotado; no acepta por anticipado S04, D01–D06, un gate ni el resultado del código. El mandato LOCAL incluye reconciliación focal y parada de la parte afectada si aparece una contradicción. La admisión de campañas continúa cerrada mientras falten su paquete propio, la cualificación aplicable y la reconciliación de guards. Planner único: [[Echo Futures — Optimización de Campañas]]. Paquete: [[EF-CAMPAIGN-MODES-I0-LOCAL]].

## Contenido

### 1. Dictamen ejecutivo y límites de autoridad

1. Se amplían los modos existentes de Platform: CHALLENGE corresponde a `CHALLENGE_ONLY`, FUNDED a `FUNDED_ONLY` y SIMULATION a una revisión explícita del recorrido `FULL_JOURNEY`. No se crea un cuarto modo “dual”, otra fábrica ni otro motor.
2. Una petición dual se expresa mediante dos ítems del batch existente, relacionados por identidad de comparación; cada etapa conserva MM, RuleSet, estado inicial, cuentas y ledger propios. Ejecutarlos secuencialmente sigue cumpliendo el paralelismo lógico.
3. La cohorte primaria descriptiva cuenta unidades comerciales de evaluación efectivamente cobradas con cantidad conocida, incluso pendientes de provisión. Factura, unidad, derecho, cuenta, intento y retry son distintos. D01/H deben estar explícitos antes de adjudicar 1/3; I0 no adjudica.
4. FUNDED informa cobros por todas las cuentas iniciadas, incluidas las que nunca cobraron; una pagadora puede perderse después. La conversión compra→primer cobro se calcula directamente por linaje, nunca multiplicando tasas de etapas aisladas. FUNDED aislada depende de I0 y de su origen/perfil, sin esperar la implementación CHALLENGE.
5. SIMULATION conduce una trayectoria temporal completa con USD 4.000 y un solo bankroll. El saldo nominal, los pases y las solicitudes/aprobaciones de pago no crean caja.
6. Activación pertenece al coste de adquisición; los costes operativos funded posteriores la excluyen. Cada evento financiero tiene una única imputación y una identidad idempotente.
7. El stock de obligaciones se conserva al horizonte. La selección propuesta usa caja neta de campaña a un horizonte fijo, acompañada de liquidez, pendientes y dispersión; no maximiza por defecto el primer cheque.
8. El G4 actual requiere un pase challenge por identidad. FUNDED aislada y un MM funded distinto necesitan decisión focal del Owner; no reciben PASS heredado ni un permiso automático para histórico.
9. S04 está integrado en SOURCE a `2baf319d`; ancestry y catálogo están comprobados. BUILD/TEST son EXECUTOR_REPORTED y falta recuperar el informe completo del verificador. El catálogo/materializador de las 26 nativas usa V1 y su intérprete cambió: equivalencia histórica queda UNKNOWN hasta resolver S04-F01. El launcher pre-ClutiFX no contiene `qualification_guard.py`; no asumir admisión mecánica vigente. [[EF-S04-INTEGRATION-RECONCILIATION]] contiene evidencia y límites.
10. Primer incremento propuesto: contrato económico versionado y proyección de KPI conciliados sobre artefactos existentes y casos documentales. No requiere reejecutar S04 ni elegir una prop para definir el esquema.

**Invariantes heredadas.** NQ exclusivo; Strategy = setup + filtro opcional + objetivo/riesgo técnico o RR; MM separado por prop/programa/etapa; sin modificar señal/geometría para resolver tamaño; Forex separado; cero aportes; reinversión del 100% del payout neto recibido; sin objetivo fijo de USD 3.000; sin caps prudenciales adicionales por costumbre; reglas de prop/broker/mercado y controles técnicos obligatorios. 1/3 es umbral Owner para futuras campañas, no probabilidad empírica; USD 400/funded y aspiraciones de cobro no son parámetros calibrados. Una esperanza por trade no positiva no descarta universalmente una campaña; la asimetría contractual tampoco demuestra utilidad. [S01–S02]

**Autoridad.** I+D Futures conserva requisitos y prioridad económica. Optimización de Campañas conserva el planner técnico. Runtime/SDK conservan contratos y owners; retester/runbook conservan G0–G5. El manager mantiene este diseño y el planner técnico por delta; I+D integra su planner central. C01/C02 originales son evidencia histórica. C03 no modifica gates, skills, runbooks, reglas económicas aceptadas ni la cuota compartida. [S01–S06; R03–R05]

### 2. Baseline, entradas y clasificación de evidencia

#### 2.1 Cortes recuperados y reconciliación C03

| Superficie | Corte | Estado observado y límite |
|---|---|---|
| Agents-OS al inicio de C03 | `844e777f95e01e5268f8f7cd98de5299765ce0f2` | Autoridades leídas; HEAD se reconcilia de nuevo antes de publicar con lease, sin force |
| Echo master | `2baf319ddcba622d9557bc9f23a13787b44c58a7` | SOURCE demostrado; no certificación de runtime |
| S04 integrado | `ae1b09bc10370806f7648f076c5fa0825c9efa4e` | Ancestro verificado; 26 nativas + 63 SG = 89 identidades, 15 alias fuera del censo ejecutable |
| Merge | `2188ac3e23d4e4a73ca0edb9aad952029deec951` | Padres `347eee8b` y `ae1b09bc`; no repetir merge |
| BUILD / TEST | Retorno Owner + agent-run del ejecutor | EXECUTOR_REPORTED; logs/digests y verificación independiente completa por recuperar |
| S04 semántico | S04-F01 | Contradicción del recibo: catálogo nativo V1 y materializador explícito frente a afirmación «vacío»; efecto en corridas reales UNKNOWN |
| Guards de lanzamiento | S04-F02 | `qualification_guard.py` ausente del árbol master; no transportar el PASS documental de ClutiFX al launcher pre-ClutiFX |
| A/B | WAITING_RETURN para este manager | La selección económica específica continúa en I+D; C03 no repite los DR ni el research A/B |
| C01 / C02 | `8c79805...` / `844e777...` | C01 corregido por delta; C02 mantiene su identidad y veredicto histórico FINDINGS |

“SOURCE demostrado” sólo acredita fuente/linaje. La igualdad de nombres de tests fallidos no demuestra causa ambiental ni paridad semántica. La baseline está admitida como fuente de un reporte derivado aislado, sin convertirla en baseline de campañas aceptada. Ver [[EF-S04-INTEGRATION-RECONCILIATION]] para el registro SOURCE / BUILD / TEST / ACCEPTANCE / DEPLOY.

#### 2.2 Clasificación de artefactos previos

| Entrada | Clasificación C01 | Uso permitido |
|---|---|---|
| Decisiones Owner de tipos y economía | ACCEPTED_INPUT | Restricciones funcionales del diseño |
| R6 y enmiendas GOD-05 | ACCEPTED_INPUT para sus contratos vigentes | Fronteras de dominio, causalidad, claims, afinidad y drenaje; no certificación física |
| S04, Platform y fixtures | ACCEPTED_INPUT sólo como fuente inspeccionada para I0; UNREVIEWED como equivalencia de ejecución | Reutilización localizada; no trasladar resultados históricos a master sin resolver S04-F01 |
| Recibos R03 89/89 | RECEIPT_HISTORICO, OWNER_ACCEPTANCE=REVIEW | Evidencia histórica de corrección/campañas bajo sus políticas; no resultados funded nuevos |
| Antiguo 25%, capital 5.000 y retiro fijo | HISTORICAL o SUPERSEDED según fuente | Reproducir identidades históricas, nunca nuevos defaults |
| Retorno de integración y agent-run | ACCEPTED_INPUT como declaración del ejecutor; UNREVIEWED como certificación | SOURCE corroborado; BUILD/TEST/independencia completa requieren sus receipts |
| C02 F01–F03 | ACCEPTED_INPUT para reparación documental | Correcciones integradas en C03; no se reescribe el review original |
| Foto C01 de master 347eee8 / IN_PROGRESS | SUPERSEDED para estado presente | Se conserva como procedencia de C01; nuevo corte observado 2baf319d |

El planner consigna 89/89 filas COMPLETE_RECONCILED, 3.037 compras y 328 pases para el perfil histórico; también indica que combina evidencia reutilizada y reejecuciones. No se atribuyen todas las filas a un único binario ni se convierten en tasa esperada del programa nuevo. [S01, S03]

#### 2.3 Presupuesto de discovery y contradicción cerrada

Se utilizaron diez fuentes técnicas principales, S01–S10, además del routing mínimo nombrado en el mandato y las reglas de creación/cierre. No se abrió una nueva investigación externa ni se eligió proveedor.

Se justifican dos lecturas acotadas adicionales sobre una contradicción concreta: el plan previo describía FUNDED_ONLY/CHALLENGE_ONLY, mientras Platform en master no contiene esos campos. Se inspeccionó `campaign.go` para distinguir el driver CAMPAIGN legacy (X01) y el mismo `platform_campaign.go` en el corte S04 (S07b), donde los modos sí están implementados. Resultado histórico de C01: los modos eran reutilización de S04 pendiente de reconciliación. En C03 su presencia en master está verificada; eso no resuelve la paridad ni certifica ejecuciones. La lectura del README fue routing exigido por AGENTS.md. No se amplió a otras estrategias, a los cuatro DR ni a un inventario exhaustivo del repositorio.

### 3. Capacidad existente y delta mínimo

| Requisito | Capacidad y símbolo observado/documentado | Delta candidato | Aceptación futura discriminante |
|---|---|---|---|
| Tipos de campaña | Master 2baf319d: `CampaignModeFullJourney`, `CampaignModeChallengeOnly`, `CampaignModeFundedOnly` integrados desde S04 | Conservar nombres e identidad; versionar semántica económica nueva | Un request legacy reproduce su significado; uno nuevo incompleto se rechaza |
| Continuidad challenge | S04: `ChallengePolicyContinuous = CONTINUOUS_V1`, `PassEvents` y `FirstPassAt` | Mantener campaña hasta horizonte; separar cuenta, compra e intento | Primer pase termina esa evaluación, no la campaña; ningún pase duplicado |
| FUNDED aislada | S04: `seedFundedAccount` instala transición canónica; una seed; no compras/setup/compliance posterior | Origen/estado/fecha explícitos y cohortes de seeds; declarar exclusiones, nunca coste cero implícito | Denominador incluye seeds quemadas; fechas y floors iniciales sellados |
| Petición dual | CLI: `PlatformBatchPlan.Items`, `RunPlatformBatch`; runner S04 plan/prepare/run/resume/reconcile | Dos ítems vinculados por comparación, salida separada por etapa | Alterar MM funded no muta estado/ledger challenge |
| Caja finita | `cashBook`, `CashEvents`, purchase/renew/setup/tickPayment y conciliación | Caja inicial 4.000 explícita; cargos versionados; obligaciones; fuentes de financiación | Cero sobregiro/creditación anticipada; ecuación de caja exacta |
| Caja de investigación | S04: `ResearchCashPolicy`; `researchCashEnabled` evita bloqueo de compra/renovación y ruina | Prohibida en SIMULATION de cero aportes; sólo evidencia analítica etiquetada | Plan SIMULATION con financiación virtual se rechaza antes del motor |
| Perfil contractual | `PlatformProfile`, `ScenarioCharge`, RuleSet por fase | Ampliar perfil/config existente con términos soportados y fuente; no defaults de E2T | Regla/cargo obligatorio desconocido impide declarar financiabilidad |
| Payout | `PlatformPayment`; request/approved/processed/credit; `PayoutNet` | Política de retiro finita y referencia separada de reglas comerciales; cargos/split exactos | Solicitar/aprobar no suma caja; split y fees una sola vez |
| Cuatro payouts | Constante S04 `MaxPayoutsPerAccount = 4` y terminal propio | Preservar legacy; en nuevo perfil resolver si límite es contractual o política elegida | No heredar “4” a otra prop; continuidad postcobro identificada |
| Identidad | `CanonicalJSONDigest(req)`, Spec.Build, DataHashes; CLI exige binary SHA | Añadir tipo/etapa/políticas/origen/horizonte/selección; diferenciar experimento de attempt físico | Cambiar una semántica material cambia identidad y bloquea resume incompatible |
| Reporting | `PlatformCampaignResult`, Accounts/Payments/CashEvents; S04 characterize/adjudicate | Proyección económica por cohorte y cuentas, con desconocidos y censura | Agregado reproduce eventos; coste unitario con cero éxitos no vale cero |
| Estado financiero | Compartimentos conservados; `AccountContextTransition`, `AccountCashflow`, accounting SDK | Reusar controles y autoridades; evento comercial no recalcula PnL | Transición requiere precondiciones/digest; nominal separado de bankroll |
| Runtime común | R6: Strategy única, fanout, pool reducer, Provider/Operation/MM; GOD-05 M01–M07 | Driver simulado consume esos contratos; no importar Core/internal | Misma causalidad y mismas decisiones de dominio dentro del alcance declarado |
| Varias props simultáneas | R6 permite asociaciones separadas y exclusividad por cuenta; Platform actual selecciona un turno | Conducir varios compartimentos/asociaciones sobre un reloj común y un bankroll | Dos props compiten por la última compra sin doble gasto y reciben señales coincidentes |
| Recursos | Supervisor único y guard S04 documentados | Reusar cola; paralelismo lógico no altera techo físico | Global ≤6 motores incluido oráculo, sujeto a recursos y mandato vigente |
| Replay | CAMPAIGN legacy sella petición; Platform conserva identidad y trazas | Replay del driver completo de tipos nuevos, no sólo RunState | Mismos eventos comerciales, transiciones y caja; primera divergencia localizada |

Los símbolos nombrados son observados en S07–S10/X01 o documentados expresamente por S03/R05; esa distinción es parte de la tabla. No se afirma haber ejecutado sus fixtures.

**Hallazgos con impacto obligatorio.** Platform/master fija 5.000 de caja, compra 120, saldo nominal 50.000, objetivo de evaluación 3.000, Provider E2T/GAU50 y pausas internas. PlatformProfile valida targets 2250/2300/2500/3000 y calcula split histórico 50% u 80% según monto. Esas constantes no implementan el nuevo universo contractual ni justifican un tamaño óptimo. El nuevo diseño no copia esas pausas/caps como prudencia universal y tampoco modifica un RuleSet para admitir riesgo. Cada restricción se clasifica: contractual, técnica, política elegida o legacy. [S07a, S08]

**Reuso concreto del lab.** Catálogo 26, 78 variantes SG y deduplicación de 15 ADD→CH300 son inventario histórico documentado, no 104 estrategias independientes. Se preservan `campaign_lab.py`, `research_lab.py`, preparación de fuente/analytics, export/validate-bundle y reportes. `project` BINARY_DIAGNOSTIC/SESSION_BLOCKS sigue marcado PROJECTED_ONLY; no se convierte en SIMULATION causal por cambiar la etiqueta. [S03]

## SPEC — Contrato funcional candidato

### 4. Unidad experimental, tiempo e identidades

Una campaña congela una pregunta económica, Strategy/config, MM por etapa, Provider/Program/RuleSet, ventanas, datos, estado inicial y políticas. No cambia esos valores para mejorar un resultado observado. Los nombres de campos nuevos de esta sección son semánticos candidatos a encajar en los contratos existentes; no son APIs ni flags ya disponibles.

| Identidad | Unidad y relación |
|---|---|
| Experimento/campaña | Petición semántica inmutable; contiene uno o varios ítems de etapa o un recorrido completo |
| Comparación dual | Relación entre ítems con la misma Strategy/config y diseño de ventanas; no fusiona cuentas ni crea caja común |
| Cohorte | Conjunto de unidades incluidas por regla de entrada previa: compras dentro de una ventana o estados funded de origen definido |
| Compra/transacción | Un evento monetario comercial. Una factura puede comprar varias unidades; contar facturas no equivale a contar cuentas |
| Unidad de adquisición pagada | Una unidad comercial inicial de evaluación con pago capturado y cantidad evidenciada; existe antes de su provisión y mantiene raíz aunque cambie account_id tras reset |
| Derecho/provisión | Entrega comercial vinculada a la unidad: pendiente, entregada, fallida o refund/cierre; no determina si existió la compra cobrada |
| Cuenta/contexto | Identidad canónica de ejecución y su fase/contexto; conserva la relación con su adquisición y todos sus intentos |
| Intento económico | Recorrido challenge entre inicio y pase, fallo, expiración o cierre por política; un reset inicia otro intento |
| Attempt técnico | Ejecución/retry del job existente. No es otra compra ni otro intento económico |
| Activación funded | Instalación efectiva de contexto funded disponible; enlaza el pase/origen y los cargos de adquisición |
| Payout | Solicitud individual con lifecycle propio; una cuenta puede producir varios |
| Evento financiero | Identidad estable de un cargo, abono, obligación, refund o liquidación; no cambia al hacer retry |

Las cardinalidades anteriores evitan dos errores: llamar “compra” a cada retry y llamar “cuenta nueva” a cada transacción de renovación. Si la prop vende un reset como otro derecho independiente, el perfil declara esa semántica; no se decide por el nombre del endpoint. Un lote de K derechos produce K unidades de adquisición y un evento de pago, con asignación de coste verificable que suma exactamente la factura.

#### 4.1 Horizontes que deben declararse

- **Ventana de ingreso:** cuándo se compran evaluaciones o se incluyen estados funded en la cohorte.
- **Horizonte por unidad H:** seguimiento desde inicio económico; declarar si usa tiempo calendario, sesiones elegibles o ambos. Los cargos y vencimientos siempre siguen sus relojes comerciales.
- **Corte administrativo T:** fecha final observada del conjunto, distinta de H cuando hay inicios escalonados.
- **Horizonte de campaña Hc:** período de la simulación desde t0, común a todas sus compras/cobros.
- **Ventanas de selección y evaluación:** qué datos ya influyeron en MM/retiro/compra; no se solapan causalmente por escoger una seed cuyo pase ocurrió después del inicio evaluado.

No se fija un número de días como si lo hubiese aprobado el Owner. La propuesta es declarar seguimiento por edad de unidad para comparar tasas y un horizonte calendario fijo para comparar caja. El período y la política de cierre al horizonte son decisiones D02/D04.

### 5. CHALLENGE: cohortes, estados y KPI

#### 5.1 Compra, provisión e intento: estados separados

Una unidad entra a la cohorte pagada cuando su pago fue efectivamente capturado y existe evidencia de la cantidad comercial comprada. No exige que ya estén entregados el derecho, las credenciales o la cuenta. Una autorización/reserva sin cargo, una solicitud nunca cobrada y un retry técnico no crean adquisiciones pagadas. La compra cobrada pendiente de provisión conserva coste y denominador; su estado comercial no se clasifica como pérdida de trading.

Separar: solicitud/pago; raíz de adquisición; provisión del derecho; cuenta instalada; intento económico; attempt técnico. Factura por K unidades conocidas crea K raíces y un solo cargo. Un cargo duplicado no crea otra raíz sin otra adquisición comercial. Si K es desconocido, conservar importe, unidades conocidas e ítems de cardinalidad desconocida, y publicar U=UNKNOWN. No deducir cantidad dividiendo por un precio supuesto.

Cada intento iniciado conserva un estado mutuamente excluyente: activo/pausado, aprobado, fallo por regla, expirado/cerrado por contrato, cerrado por política o no observable por técnica. Reset gratuito/pagado termina/vincula el intento anterior e inicia otro bajo la misma raíz, salvo que el contrato venda explícitamente un nuevo derecho inicial independiente. Renovación que sólo extiende vigencia no crea raíz ni intento. Un retry del job no altera compras, intentos ni dinero.

La raíz termina en pase, fallo final/expiración/abandono comercial declarado, refund/cierre comercial o continúa pendiente. La pérdida de un intento no es fallo final de la raíz si aún cabe un reset contractual. El pase cuenta una vez por raíz; no se duplica tras repetir su evento. Varias funded por compra requieren cardinalidad contractual soportada; no se deduce por nombres.

En la vista descriptiva de cohorte pagada bruta, un refund posterior es contra-coste y desenlace de la raíz, sin borrarla retrospectivamente de U. Una vista alternativa que excluya refunds requiere identidad y regla de selección explícitas; no sustituye silenciosamente el denominador del 1/3. Esta propuesta de D01 se implementa descriptivamente en I0, sin adjudicar el umbral.

Pase, revisión, credenciales, activación pagada, instalación y disponibilidad funded son hechos distintos. Aprobar no demuestra financiación ni cobro. COMPLETE_RECONCILED / INTERRUPTED / ENGINE_FAILED / DATA_BLOCKED / UNRECONCILED son calidad de ejecución, no BURNED. Conservar último estado económico válido y porción desconocida.

#### 5.2 Denominadores y costes

U es el número de unidades comerciales inicialmente cobradas con cardinalidad conocida, también las no provisionadas. A son intentos económicos iniciados; P_U raíces con al menos un pase; P_A intentos con pase; F funded efectivamente disponibles. Identificar U_known y los ítems de cardinalidad desconocida; no publicar U exacto ni ratios que lo necesitan si existen esos ítems.

| KPI | Definición | Alcance |
|---|---|---|
| Pase por adquisición pagada al corte | P_U / U | Todas las unidades cobradas de la cohorte; conserva provisión pendiente, pérdidas, refunds y pendientes |
| Pase por intento | P_A / A | Incluye intentos sin fills; excluye retries técnicos |
| Pase entre resueltos | P_U / U_resueltas; P_A / A_resueltos | Vista secundaria con desenlaces declarados |
| Activación por pase | F / P_U | Separar espera, rechazo, falta de liquidez y corte |
| Funded disponible por adquisición | F / U | Unidades disponibles según cardinalidad declarada; no confundir con éxito binario por compra |
| Coste por pase | C_eval_pagado_neto / P_U | Costes de toda la cohorte, no sólo ganadoras |
| Coste por funded disponible | C_adq_pagado_neto / F | Evaluación más activación, incluyendo adquisiciones fallidas |
| Coste por intento | C_eval_pagado_neto / A | Descriptivo; no reemplaza coste por pase |
| Tiempo a provisión/resolución/pase/fallo | Desde compra y desde inicio del intento | Ambos relojes; pausas y pendientes visibles |

El reporte publica además facturas/cargos, cantidades por factura, derechos provisionados, cuentas instaladas, resets pagados/gratuitos, renovaciones, refunds e intentos técnicos. Una cuenta que no se instaló permanece en U. La tasa por cuenta iniciada es secundaria porque excluye provisión pendiente. Sólo declarar compra=derecho=cuenta cuando su cardinalidad 1:1 esté probada.

C_eval incluye compras/resets/renovaciones y cargos de evaluación pagados, menos refunds recibidos vinculados. C_adq añade revisión/credenciales/activación hasta disponibilidad. Repartir un cargo de bundle sólo con regla explicitada que conserve exactamente el total; si no existe, el total común es conocido y la atribución individual queda UNKNOWN. No duplicar activación en F_op.

Cero éxitos produce coste unitario ausente con NO_SUCCESSES y gasto visible; no cero ni infinito ficticio. U=0 produce NO_PAID_ACQUISITIONS; cardinalidad incompleta produce UNKNOWN_CARDINALITY. Un numerador afectado por evidencia técnica incompleta no se convierte en cero: publicar conteo observado/límite y estado de completitud. Dinero y fracciones exactos; redondeo sólo de presentación.

#### 5.3 Aplicación futura del 1/3

Propuesta D01: P_U(H)/U sobre unidades comerciales pagadas, resets vinculados y éxito único por raíz. Antes de adjudicar deben fijarse explícitamente unidad, reglas de resets/refunds, cohorte y H. I0 sólo calcula vistas descriptivas y devuelve THRESHOLD_NOT_ADJUDICATED si esa decisión no existe. No reescribe el adjudicador histórico 25%.

Con U y P_U exactos y seguimiento aplicable, comparar 3×P_U ≥ U. No redondear 32,9% a un tercio. El umbral Owner no reemplaza G4 ni demuestra suficiencia estadística; no se agrega un N mínimo universal ni otro cap prudencial.

#### 5.4 Seguimiento, pendientes y censura

Una foto de 10 pases, 20 fallos y 70 pendientes informa 10% sobre 100, y 33,3% entre 30 resueltos como otra vista. No elimina pendientes para aprobar. El reloj de adquisición empieza en el cargo; los relojes de provisión/inicio de trading/funded se conservan aparte.

Para pase antes de H, una unidad observada hasta H sin pase aporta indicador cero a esa pregunta, aunque siga activa; no se etiqueta quemada. Una unidad observada sólo hasta h<H está censurada. Publicar incorporación, edad, seguimiento, maduras, censuradas y técnica incompleta; no comparar cortes de edades distintas como si fueran iguales.

Si U es conocido, los límites P/U y (P+potencialmente_exitosas_no_observadas)/U describen completitud, no confianza ni una estimación de probabilidad. No agregar fallos terminales al límite superior. No usar censura no informativa, Kaplan–Meier o IID por cuenta sin justificar los supuestos; conservar eventos competitivos y dependencia temporal.

### 6. FUNDED: origen, seguimiento y cobros

#### 6.1 Orígenes admitidos como experimentos, no equivalentes

| Origen | Datos iniciales exigidos | Conclusión válida |
|---|---|---|
| Estado estandarizado | Balance/equity, floor/trailing, límites, días, target/contador de payout, elegibilidad, obligaciones, fase comercial exacta y fecha | Respuesta de ese estado hipotético; coste de adquisición excluido/UNKNOWN, no cero |
| Estado derivado de un pase | purchase/attempt/pass IDs, instante de pase y activación, contexto instalado, cargo y receipt, estado de Strategy/analytics a esa fecha | Trayectoria condicionada al pase y a su tiempo real |
| Estado observado importado | Snapshot y hechos verificables, instante, productor y alcance; pendientes abiertos | Continuación desde ese corte, sin reconstrucción ficticia previa |
| Distribución modelada de estados | Fuente/ventana de calibración, variables conjuntas, semilla y límites | Sensibilidad modelada, sin llamarla evidencia de cuentas reales |

No copiar saldo/floor de un seed estándar a todos los pases. El contrato puede resetear balance y riesgo en la activación, pero se aplica su transformación exacta; no se heredan mecánicamente los máximos/minimos challenge ni se borran los que el contrato conserva. La historia de mercado/Strategy continúa causalmente mientras se resuelven revisión y credenciales. Una funded no empieza antes del pase que la originó.

Distinguir programa simulated funded, LiveSim y live con su fase real; el rótulo FUNDED es la pregunta económica, no una garantía comercial universal. Esta entrega no decide prop ni ruta de automatización.

#### 6.2 Estados independientes

La cuenta conserva su lifecycle: pendiente de instalación, disponible/operativa, pausada, drenando, perdida por reglas, cerrada por política, transición comercial o abierta al horizonte. El payout conserva solicitado, aprobado, procesado/débito nominal pendiente, cobro pendiente, recibido, denegado/cancelado y, si el contrato lo permite, reversado.

“Pagadora” es un atributo histórico: haber recibido al menos un pago. No es un estado excluyente de “quemada”. Un cobro ya recibido no se borra al perder después la cuenta. Un cobro pendiente después de una pérdida se liquida/deniega conforme al contrato, no por un if genérico que asume siempre pago o siempre cancelación.

La retirada de una cuenta exige drenaje y correlación de sus órdenes/fills. El cierre económico no habilita reutilizar su estado ni liberar un claim incierto.

#### 6.3 KPI

N es el número de cuentas funded cuyo contexto inicial fue instalado y comenzó su seguimiento económico, incluidas las que tuvieron cero señales o cero pagos. Las activaciones/instalaciones fallidas se reportan aparte y no se eliminan de la cohorte de adquisición. Una cuenta no necesita un primer fill para integrar N.

W es la suma neta de pagos efectivamente recibidos; W puede distinguir abonos y reversos identificados. F_op son desembolsos externos de operación funded posteriores a disponibilidad, excluidos de adquisición y no descontados ya de W ni del PnL nominal.

| KPI | Fórmula / contenido |
|---|---|
| Fracción de pagadoras | N_con_al_menos_un_cobro / N |
| Cobro neto medio por iniciada | W / N |
| Margen funded antes de adquisición | (W − F_op) / N |
| Cobro medio entre pagadoras | W / N_pagadoras, rotulado secundario |
| Pagos repetidos | Número total, ordinal por cuenta, montos y tiempos; sin multiplicar N |
| Pérdida antes/después de cobro | Dos conteos y tiempos, manteniendo el total de cuentas |
| Estado al horizonte | Activas, pausadas, perdidas, cerradas, transiciones y pendientes, por dimensiones separadas |
| Tiempo al primer cobro | Desde disponibilidad funded; además desde compra si existe origen trazable |
| Importe/tiempo pendiente | Solicitudes y obligaciones, con estado y vencimientos; valor en caja = 0 hasta cobro |
| Costes | Adquisición referenciada, operación y descuentos incluidos en payout, particionados |
| Seguimiento | N iniciadas, completas a H, censuradas, técnica incompleta y duración por cuenta |

Con N=0 no se informa promedio cero. La media sólo entre pagadoras no sirve como media funded. Las medias monetarias se calculan con dinero exacto; el redondeo de presentación no modifica el ledger.

**Composición aritmética limitada.** Si adquisición y funded pertenecen a la misma cohorte trazable, perfil y período compatible, la contribución por funded disponible puede mostrarse como (W−F_op−C_adq)/N, siendo N=F y usando el mismo conjunto. Si las cohortes difieren, se muestran separadas o como proyección condicionada explícita. No se multiplica tasa de pase × tasa de cobro × payout medio para afirmar caja o supervivencia de USD 4.000.

#### 6.4 Conversión longitudinal compra → primer cobro (C02-F02)

Q(H) cuenta raíces distintas de U con al menos un payout de trading positivo efectivamente recibido antes del corte declarado, a través del linaje verificado compra→intento→pase→activación→payout. **q(H)=Q(H)/U**. Cada raíz aporta a Q como máximo una vez, aunque tenga varios cobros o descendientes funded permitidos. Refunds, retiros nominales y pagos sólo solicitados/aprobados/procesados no satisfacen el primer cobro.

Acompañar q con U/Q, número de pagos, W neto recibido, W/U, contribución neta por adquisición cuando la atribución de todos los costes sea completa, tiempo compra→primer cobro y funded→primer cobro, origen, pendientes, reversos y censura. Conservar fecha de primer crédito y efectivo neto retenido por separado: una pagadora luego quemada o con reverso mantiene el hecho histórico del crédito; el reverso resta dinero y queda visible.

CHALLENGE aislada sin seguimiento funded produce NOT_OBSERVED para q, no cero. FUNDED exógena o cohortes sin relación causal producen UNKNOWN/NO_LINKAGE. CHALLENGE 10 compras/3 pases más FUNDED exógena 3 iniciadas/1 pagadora no demuestra 1/10. En una trayectoria linked y completamente observada al corte, Q=0 sí es un resultado válido. Si parte del linaje es desconocida, informar éxitos observados y faltantes sin inventar una tasa completa.

La aspiración Owner de un cobro por cada diez compras no es una estimación ni un nuevo gate. El KPI existe para medirla directamente cuando exista evidencia compatible.

### 7. Costes, ledger y financiación

#### 7.1 Tres vistas, una sola contabilización por efecto

1. **Ledger nominal por cuenta:** fills, comisiones de trading, ajustes, balance, equity y cashflows de prop. Lo posee accounting/Provider/Operation según sus contratos.
2. **Ledger comercial de bankroll:** dinero externo recibido/pagado, independiente del saldo nominal. Lo extiende Campaign usando la infraestructura de caja existente.
3. **Registro de obligaciones/pagos:** compromisos, fechas, condición, acreedor/origen y relación con el efectivo. No es otro motor contable ni autoriza gasto por sí solo.

| Evento | Clase económica | Efecto en bankroll | Exclusión obligatoria |
|---|---|---:|---|
| Compra inicial | Adquisición/evaluación | −cargo pagado | No debitar otra vez al crear el account_id |
| Reset pagado/gratuito | Adquisición/evaluación | −cargo pagado / 0 | Nuevo intento no implica nueva compra automática |
| Renovación evaluación | Adquisición/evaluación | −cargo pagado | No duplicar por cada trade/día |
| Activación/credenciales/setup exigido | Adquisición hasta disponible | −cargo pagado | F_op excluye el mismo evento |
| Fee de datos/plataforma posterior externo | Operación funded o coste común | −cargo pagado | Excluir si ya fue retenido del payout |
| Fee de trading debitado al saldo prop | PnL nominal | 0 directo | No restarlo otra vez de W ni de B |
| Retiro bruto debitado a la cuenta prop | Transferencia nominal a proceso de payout | 0 directo | No restarlo también del bankroll |
| Payout neto recibido | Cobro | +neto recibido | No aplicar split ni fee otra vez |
| Refund comercial recibido | Contra-coste de adquisición/operación | +refund | No contarlo como payout de trading |
| Pérdida nominal/floor breach | Resultado de cuenta | 0 directo | No volver a cobrar la pérdida de equity al Owner |
| Clawback/cargo contractual externo | Reverso/cargo, sólo si existe autoridad | ±efectivo real | No inventarlo como regla universal |

La descomposición de un pago conserva bruto solicitado/aprobado, trader share según regla versionada, retenciones y neto recibido. La ubicación temporal del débito nominal, elegibilidad durante revisión, uso de fondos solicitados y consecuencias de una pérdida antes del cobro son términos del perfil. Si afectan caja y faltan, el escenario queda CONTRACT_INCOMPLETE; no se rellenan con el comportamiento histórico de Platform.

#### 7.2 Ecuaciones e invariantes

Con B0=4.000, cero aportes, W(t) cobros netos, R(t) refunds recibidos y D(t) todos los desembolsos externos pagados:

**B_liquidado(t) = 4.000 + W(t) + R(t) − D(t).**

De forma equivalente, B=4.000+W−costes_netos_pagados, cuando refunds ya están incluidos como contra-coste. Usar una forma u otra, nunca ambas a la vez.

**Caja disponible** es B_liquidado menos importes ya comprometidos/reservados que no pueden gastarse dos veces. Una reserva no es otro desembolso y se libera contra el cargo o contra una cancelación legítima. La propuesta protege obligaciones contractuales conocidas/aceptadas, no una reserva prudencial inventada. Los costes futuros opcionales se deciden con su política; los compromisos irrevocables se conservan con su vencimiento.

Cada evento propuesto añade al registro existente: identificador estable, tipo, importe/moneda, momento de ocurrencia y de disponibilidad, cuenta/adquisición/intento/payout afectados cuando aplique, regla y fuente, referencia causal, signo y estado. Mismo ID+mismos términos ⇒ sin segundo efecto; mismo ID+términos distintos ⇒ conflicto visible y no mutación silenciosa. Se conservan fallos y reversos con nuevas referencias, no reescribiendo historia.

Una compra requiere liquidez suficiente en el instante de compromiso y cumplimiento de obligaciones/admisión; ninguna aprobación pendiente aporta efectivo. Si dos candidatos compiten por USD 100 disponibles, la decisión serializada admite uno y el segundo vuelve a leer la caja. La cuenta nominal no garantiza ese pago.

#### 7.3 Fuente de financiación todavía material

La decisión aceptada dice “USD 4.000 para comprar challenges”. No especifica cómo se financian cargos obligatorios adicionales. **D03 propone** que activaciones, resets, renovaciones y costes operativos externos autorizados debiten el mismo bankroll de 4.000 y sus cobros, sin aportes ni uso de Forex. Es la interpretación mínima que permite cerrar SIMULATION, pero requiere aceptación económica cuando esos cargos existan.

Hasta resolver D03 y los importes del perfil comercial, puede calcularse un experimento de medición de costes; no puede rotularse como campaña financiable. Si un cargo se retiene realmente del payout, se modela esa retención. Si es prepago, no se paga con un cobro futuro. Si el perfil exige una fuente externa no autorizada, esa ruta no es admisible con “cero aportes”.

Un experimento aislado CHALLENGE/FUNDED puede medir una cohorte finita sin representar solvencia conjunta: debe declarar MEASUREMENT_ONLY, el coste observado y exclusiones. No inventa crédito para el Owner, no oculta el gasto y no satisface la aceptación de SIMULATION.

### 8. SIMULATION: composición causal con caja común

#### 8.1 Recorrido 1 Strategy × 1 prop

El recorrido conserva compras → evaluación → pase → revisión/activación → funded → elegibilidad → solicitud → aprobación/procesamiento → cobro → disponibilidad para nuevas compras. No todas las transiciones son instantáneas ni todas terminan con éxito.

1. Inicializar B0=4.000, inventario vacío y obligaciones iniciales declaradas. Toda cuenta precargada requeriría origen y financiación; la SIMULATION mínima comienza sin funded gratuitas.
2. Consumir mercado, calendarios y hechos comerciales mediante el reloj/driver existente. Strategy y analytics conservan su historia técnica incluso sin cuenta habilitada.
3. Evaluar la política de compra con la información disponible. Comprometer/debitar el coste una vez y registrar el derecho. Aplicar la demora real de provisión de la evaluación; comprar no garantiza operar inmediatamente.
4. Instalar contexto/RuleSet/MM cuando se cumplen precondiciones. Provider/Operation/MM conducen las operaciones; Campaign observa desenlaces, sin recalcular trading PnL ni declarar pases por saldo leído fuera de la autoridad.
5. Un pase crea la obligación/opción de activar y un estado pendiente con fecha. Funded empieza sólo tras activación pagada cuando corresponda e instalación efectiva, con la transformación contractual de estado.
6. La política de retiro decide solicitud/monto/continuidad usando estado causal. El perfil conduce revisión, aprobación, débito nominal, demora y eventual cobro/denegación.
7. Un cobro efectivo acredita el bankroll una vez y habilita el siguiente ciclo de decisión de compra. Los pagos pendientes siguen con su cuenta y reloj aunque la cuenta deje de operar.
8. Al horizonte, cerrar observación y reportar posiciones/órdenes/obligaciones/pendientes conforme a la política de cierre predeclarada. No liquidar ficticiamente derechos/cuentas a valor nominal ni sumar cheques futuros.

El programa puede perder todas las cuentas sin consumir otros USD 50.000/100.000 por cuenta del bankroll. Las funded quemadas reducen las oportunidades futuras de cobrar y requieren nuevas adquisiciones si la política lo permite; la pérdida nominal no es una factura adicional.

#### 8.2 Orden temporal y situaciones simultáneas

Se reutiliza el scheduler/reloj del motor. Los eventos comerciales entran como controles/timers de Campaign, con instante efectivo y secuencia causal. No se crea un servicio de scheduling.

Para compras competitivas, la propuesta serializa en el owner del bankroll: aplicar hechos ya efectivos y obligaciones exigibles, conciliar cash recibido y reservar el coste de la decisión admitida antes de examinar la siguiente. Esta secuencia no reordena los fills ni reemplaza la prioridad de matching del venue. Un empate entre candidatos comerciales se resuelve por la política de asignación predeclarada, no por el hash de una orden.

Si la compra se dispara por una señal, registrar esa señal como causa de demanda comercial. No asegurar su fill después de obtener credenciales: R6 fija el destino o NO_TARGET al admitir la señal, y una cuenta que aparece después recibe señales futuras. Sólo una activación realmente previa al corte de admisión puede recibir la señal conforme al contrato. El comportamiento histórico ON_DEMAND de Platform no demuestra latencia comercial cero. [S05, S07a–S07b]

#### 8.3 Liquidez, compromisos y ruina

Distinguir tres resultados:

- **Bloqueo de liquidez:** hoy no se puede comprar/activar/pagar, pero existen cuentas utilizables, derechos recuperables o cobros pendientes. Registrar duración y motivo; no llamarlo ruina definitiva.
- **Insolvencia/impago contractual:** obligación exigible sin fuente; aplicar gracia/expiración del perfil, nunca inventar préstamo o condonación. Si falta el tratamiento contractual, bloquear la interpretación financiable.
- **Agotamiento absorbente dentro del escenario:** no existe compra/reanudación legal financiable, cuenta capaz de continuar ni derecho/cobro pendiente que pueda cambiar el estado según la política y términos. No requiere adivinar beneficios futuros; describe el conjunto de acciones legales que queda.

Reportar B final/mínima, disponible mínima, tiempo sin liquidez, obligaciones vencidas/no vencidas, cobros pendientes, compras/pases/activaciones, pérdidas y concentración. Un saldo positivo menor al coste de compra no implica ruina si todavía existe una cuenta operativa; una gran cartera nominal tampoco prueba liquidez.

Un seguimiento de liquidación posterior a Hc puede publicarse como cola separada, sin trading nuevo y con fecha límite identificada. Sus pagos no se agregan retrospectivamente a B(Hc). Si se quiere elegir con ese horizonte ampliado, debe fijarse antes de evaluar.

#### 8.4 Extensión a varias estrategias, pools y dos props

El mismo bankroll arbitra las decisiones comerciales de varias asociaciones. Cada cuenta mantiene Provider/Program/RuleSet, MM, ledger nominal, fase y payout propios. Cada compra/cargo/cobro tiene atribución a prop/estrategia/cohorte; un coste común tiene una regla de reparto cuya suma concilia con el total.

Se preserva R6: una cuenta activa como máximo por asociación, claim exclusivo global por cuenta, afinidad por Strategy, estado MM por Operation/cuenta y drenaje antes de liberar. Dos props simultáneas se representan mediante cuentas/asociaciones diferentes. No habilita múltiples Strategies en una cuenta ni múltiples activas por asociación. La asignación comercial no reemplaza FIFO/afinidad del pool. [S05]

Todas las asociaciones consumen la misma trayectoria de mercado y el orden causal relevante. Una misma Strategy en varios pools se evalúa una vez y produce decisiones de delivery separadas. Varias estrategias distintas conservan sus propios estados. Una cuenta sin destino en un evento no recupera esa oportunidad al conseguir caja después.

El reporte por prop es atribución de flujos, no un bankroll independiente que pueda gastar los mismos USD 4.000. Sumar dos simulaciones aisladas de USD 4.000 daría USD 8.000 implícitos y no cumple esta capacidad.

### 9. Políticas predeclaradas y selección económica

#### 9.1 Registro mínimo dentro de configuración existente

Cada candidato fija un tuple de versiones: MM challenge, MM funded, retiro, compra, asignación, reset/renovación/reemplazo, origen funded y cierre de horizonte. Se usan enums/structs/configuraciones tipadas en los owners existentes; no se introduce un lenguaje de políticas ni un optimizador universal.

| Política | Propuesta inicial para revisión | Alternativa finita con pregunta concreta |
|---|---|---|
| Compra | ON_DEMAND cuando falta cuenta elegible y existe liquidez/entitlement, respetando provisión | Compra anticipada a frontera comercial declarada para medir coste/latencia de estar listo |
| Asignación entre props/estrategias | Orden estable predeclarado; dentro de cada pool manda R6 | Round-robin por decisión comercial elegible, sin cambiar claims ni afinidad |
| Reemplazo | Tras terminalidad y drenaje, comprar sucesora si financiable | Comparar reset contractual con recompra sólo cuando ambos existen; no “rescatar” pérdidas cambiando señal |
| Renovación | Decisión antes del vencimiento, con coste/derecho identificado | Cerrar en esa frontera si el valor de continuar es la hipótesis que se evalúa |
| Retiro | Primer instante elegible, monto legal máximo compatible con continuidad definida | Esperar un evento/umbral legal declarado; o monto legal menor para comparar caja futura |
| Continuidad postpayout | Continuar mientras regla/política permita y haya elegibilidad | Retirar cuenta tras un número de cobros si se declara como política experimental, no como regla universal |

Todos los parámetros materiales se fijan antes de mirar evaluación. Los importes 500/2.000/5.000 mencionados por el Owner no se convierten en una lista de búsqueda. Reglas de monto mínimo/máximo, buffer obligatorio, split, consistencia y frecuencia vienen del contrato B; los objetivos voluntarios vienen de la política candidata. “Pedir máximo legal” tampoco se presume óptimo.

#### 9.2 Sizing sin alterar Strategy

La Strategy entrega geometría técnica y dirección. El MM decide la cantidad sobre esa geometría, con datos y costes disponibles en el instante. La discretización, lot_step, tick/point value, costes estimados y caps físicos provienen de metadatos/contratos exactos.

Para un MM de presupuesto fijo que ya soporte ese modelo, el candidato usa cantidad entera admisible derivada de presupuesto dividido por riesgo monetario por contrato más costes, con redondeo según su kernel; conserva riesgo solicitado, riesgo ejecutable, cantidad y presupuesto no utilizado. Otros MMs conservan sus fórmulas propias. Una propuesta de 100 de riesgo y 60 por contrato admite 1 contrato bajo ese presupuesto y ejecuta 60, no “usa 100” moviendo el stop; cifras ilustrativas sin correspondencia a un perfil seleccionado.

En pools con `MM_ENTRY_BUDGET_UNCLIPPED_V1`, R6 prohíbe convertir R>remanente positivo en retirada/clamp por defecto. Se mantienen breaches efectivos y límites reales de prop/broker/mercado, sizing mínimo y controles técnicos. No se reintroduce el recorte histórico bajo un nuevo nombre. [S05]

Comparar tamaño máximo legal con otro perfil necesita una hipótesis: rapidez de resolución, sobrepaso de target, mínimos de días/consistencia, probabilidad de perder antes del pase y cash esperado a Hc. Mayor tamaño no prueba óptimo. No se propone un “riesgo conservador” adicional como requisito de admisión.

#### 9.3 Espacio finito sin producto cartesiano

Propuesta de método, pendiente de presupuesto del manager:

1. Congelar un control ya soportado/compatible y, como máximo, dos alternativas MM challenge justificadas por una pregunta de resolución rápida. No crear otra familia Strategy por cambiar MM.
2. Con un perfil funded justificado, comparar como máximo tres políticas completas de retiro/continuidad. El diseño de la etapa conserva todas las iniciadas y no selecciona sólo estados de pases rentables.
3. Llevar como máximo dos tuplas completas a SIMULATION mínima; variar compra/asignación sólo si su latencia o liquidez explica una diferencia material.
4. Un refinamiento adicional requiere una pregunta nueva y presupuesto explícito. Si el mejor candidato está en un borde, reportar “mejor entre los evaluados”, no óptimo global.
5. Registrar también candidatos inválidos/no ejecutables y negativos. No rellenar una cuota de estrategias ni abrir todas las combinaciones de lotes × retiro × días × props.

Los números anteriores son límites candidatos de búsqueda de C01, no autorización de ocho corridas ni modificación del supervisor. Los valores de MM y las fechas no se inventan sin A/B/corte aceptado.

#### 9.4 Objetivo propuesto a horizonte fijo

Proponer como score primario **J(Hc)=B_liquidado(Hc)−O_irrevocable_no_pagado(Hc)**, donde O incluye sólo obligaciones contractuales ya contraídas que siguen a cargo del bankroll y no están descontadas de W/D. La reserva de esas obligaciones no se resta una segunda vez. Mostrar también B bruto liquidado y caja disponible para que el lector vea la diferencia.

La finalidad es que atrasar un cargo debido no haga parecer mejor una política. No se valora como cash un payout pendiente, una cuenta nominal ni un supuesto valor de reventa. La regla y el horizonte de comparación son D04, aún propuestos.

Con múltiples trayectorias temporales, reportar media/mediana/dispersión de J y delta frente a B0, probabilidad empírica de agotamiento bajo el diseño, tiempos de cobro y concentración. No imponer un máximo aceptable de ruina ni pesos de utilidad sin Owner. Si sólo existe una trayectoria, informar un resultado condicionado a ella; no inventar una distribución.

Challenge informa rapidez de pase/pérdida y funded informa cobro por iniciada; el criterio final de campaña valora ambos junto con financiación y tiempo. No seleccionar el primer cheque más alto como proxy suficiente del total recibido.

#### 9.5 Separación temporal e incertidumbre

Congelar MM/retiro/compra en una ventana de desarrollo; evaluar la tupla cerrada en datos posteriores no usados. Estados funded derivados de pases se generan dentro de la trayectoria admisible y en su fecha, sin lookahead. Excluir del calificativo OOS los períodos ya usados para gates, selección manual o ajustes de agentes; el 60/20/20 retrospectivo de S04 mantiene su etiqueta histórica. [S01, S03, R04–R05]

Las réplicas de una señal en diez cuentas no aportan diez experimentos independientes. Sensibilidades/bootstrap, si se usan, remuestrean bloques temporales conjuntos entre estrategias/props y reconstruyen estados/calendarios con warmup y contratos compatibles. No se juntan bloques como si los máximos trailing, elegibilidad y obligaciones se resetearan solos. Si no puede justificarse la reconstrucción, se usan ventanas contiguas y el alcance queda limitado.

No escalar trades ya cerrados para otro MM si cambia cantidad admisible, fills, estado, trailing, pausas, duración, resets o compras. Se puede reutilizar fuente/preparación causal; la trayectoria dependiente se vuelve a conducir sólo cuando la identidad cambia y los gates lo permiten.

Una media positiva con demora de pagos, dependencias y caja finita no demuestra escala infinita. El incremento multi-prop mide capacidad y sensibilidad bajo límites reales, no una extrapolación geométrica de medias aisladas.

### 10. Causalidad, datos y replay del runtime común

#### 10.1 Contrato de datos mínimo

Cada ítem sella instrumento NQ y contratos físicos, fuente/manifiesto/hash, cobertura y gaps, warmup, trade_start/end_exclusive, calendario/timezone/DST, rollover, resolución, precio/volumen, disponibilidad y modelo de ejecución. Sin dato indispensable, DATA_REQUIRED; no sustituir ausencia por cero ni por una serie “equivalente” sin identidad.

Una tabla preparada puede compartirse únicamente cuando su key completa, kernel, parámetros, prefijo y disponibilidad coinciden. El CLI observado ya prepara fuente y analytics TG por identidad y abre cursores aislados. El reuso no permite acceder al final de una barra antes de decision_time ni perder el estado de una Strategy al comprar otra cuenta. [S10]

OHLC M1 no observa el orden real H/L, bid/ask, cola o latencia. Un recorrido intrabar versionado es un supuesto del modelo y no una cota conservadora universal. Marcar el resultado MODEL_CONDITIONAL; si la decisión depende de ese orden, comparar supuestos admisibles o requerir evidencia más fina, sin llamarla fill observado. [R06]

Los fees, slippage, order types y restricciones del venue simulado son parte de la identidad. Una limitación no soportada se rechaza; un fixture de fills/latencia no prueba que el mercado histórico siguió esa secuencia.

#### 10.2 Tres alcances de replay

| Alcance | Entradas | Comparación y límite |
|---|---|---|
| Dominio | Estado inicial, config exacta, eventos causalmente disponibles, orden por owner/lane y reloj | Señales, observaciones, decisiones MM/Provider, claims y órdenes; no prueba fill real |
| Sesión con ejecución observada | Además ACK/reject/fill/cancel/finality, fees y ajustes auténticos | Ledger reconstruido y decisiones; detener equivalencia en primera orden divergente |
| Backtest simulado | Mismo dominio, fuente y modelo de venue explícito | Traza del modelo y lifecycle comercial; no certifica infraestructura/broker |

Si sólo se inyectan revisiones contables originales, el replay prueba decisiones sobre esa economía suministrada, no la corrección del productor de PnL. Para conciliar contabilidad hay que reconstruir desde hechos primarios y estado inicial. GOD-05 conserva la separación de garantías de Flink/M1, M2 y venue; C01 no promete atomicidad entre sistemas. [S04, S06]

El paquete sellado incluye cambios de config/control, generaciones, observaciones consumidas y disponibilidad, eventos comerciales y obligaciones. Resume también conserva provisión/activaciones pendientes, reservas, pagos/timers y cursor comercial; los IDs de efectos sobreviven a reintentos. Snapshot de RunState por sí solo no acredita que no haya doble cargo/cobro. Un hash de archivos no demuestra captura completa. La ejecución de tipos nuevos debe reproducirse a través del driver de campaña con su petición, no arrancando un RunState sin compras/cobros.

#### 10.3 Identidad e invalidación selectiva

Mantener dos identidades: experimento semántico y ejecución física. La primera incluye tipo/modo, etapa comercial, Strategy/config/filtros, MM y política presupuestaria, Provider/Program/RuleSet/terms, retiro/compras/asignación/reemplazo, financiación, horizonte/cohorte, estado inicial/origen, datos/calendario/modelo, build y método de selección. La segunda añade attempt/run y localizador de evidencia sin reescribir la primera.

| Cambio | Invalidación exigida | Reuso permitido |
|---|---|---|
| Etiqueta/formato de reporte sin semántica | Derivados y comprobación de agregados | Eventos y campañas selladas |
| Fórmula de KPI/denominador | Versión del reporte y decisión económica | Eventos íntegros; nunca reetiquetar aceptación anterior |
| Compra/retiro/financiación | Trayectoria de cuentas/caja y decisiones dependientes | Datos/analytics causales; señales sólo si independencia demostrada |
| MM, RuleSet, ejecución, estado inicial | Gates/resultados afectados y nueva identidad | Casos no afectados con correspondencia documentada |
| Señal/filtro/calendario/roll/datos | Cadena causal dependiente y selección | Receipts antiguos como historia, no como PASS nuevo |
| Build cambiado | Verificar diferencia semántica y contrato de receipts | Sólo cuando el owner del gate acepta la equivalencia; no falsificar build hash |
| Mayor concurrencia lógica | Replay, claims, aislamiento, orden y liquidez compartida | Kernels/fixtures unitarios válidos; no heredar economía 1×1 |

No se alteran artefactos históricos para satisfacer un schema nuevo. Si falta un campo de coste/origen/event_id, el migrador/proyector sólo lo recupera cuando existe una relación inequívoca en la evidencia; en otro caso emite UNKNOWN y limita el KPI.

### 11. Admisión y conflicto G4

**Autoridad vigente, sin cambio.** G0 identidad/implementación → G1 correctness → G2A readiness + G2B sesión + G2C operación completa propia → G3 rollover → G4 contrato trimestral calificado con al menos un CHALLENGE_PASSED → G5 histórico. El runbook exige mínimo 45 sesiones elegibles para el contrato G4, guard en la vía real run/resume y receipts de identidad exacta. Los tests/fixtures del motor no sustituyen esta evidencia. [R04–R05]

En C03 se comprueba que el master pre-ClutiFX no trae `qualification_guard.py`. Antes de habilitar motores nuevos, el incremento correspondiente debe portar/adaptar únicamente la admisión vigente y demostrar negativos en run y resume, sin integrar ClutiFX entero ni alterar G4. I0 sin spawn no depende de ese port. [[EF-S04-INTEGRATION-RECONCILIATION]]

El campo heredado QUARTER_FUNDED describe pases de CHALLENGE_ONLY; no acredita funded ni retiros. El propósito efectivo de una ejecución depende de ventana, contratos físicos y horizonte sellados. Un estudio multicontrato corto sigue siendo HISTORICAL; rotularlo FUNDED, SIMULATION o diagnóstico no evita el guard. La protección documentada cubre el entrypoint autorizado del lab, no cualquier invocación directa del binario. [R04–R05]

| Trabajo | Admisión bajo autoridad vigente |
|---|---|
| Contratos, proyecciones desde receipts existentes y ejemplos contables | No lanzan motores ni crean PASS; permitidos como diseño/derivación |
| Nueva identidad CHALLENGE | Requiere cadena propia G0–G4 antes de histórico |
| FUNDED con el mismo nombre de Strategy pero otro MM/RuleSet/estado | No hereda G4 challenge; registrar incompatibilidad de alcance |
| FUNDED aislada que nunca ejecuta challenge | No puede producir CHALLENGE_PASSED en esa fase; histórico bloqueado por autoridad pendiente |
| Petición dual | Evaluar admisión de cada ítem; el autorizado no transmite permiso al otro; bloquear explícitamente el ítem incompatible |
| SIMULATION completa | Requiere admisión de identidades/etapas y composición; no crea un atajo a G5 |
| S04 bit-idéntica con receipt válido | Reutilizar evidencia, sin relanzarla para obtener otro receipt |

#### 11.1 D05: decisión focal propuesta al Owner

**Pregunta:** ¿se mantiene la exigencia de pase challenge como única admisión económica para todo histórico, o se autoriza al dueño de la metodología a establecer un criterio específico de etapa para FUNDED?

**Recomendación candidata, NO VIGENTE:** conservar la secuencia G0–G5 y los requisitos técnicos propios; encomendar al owner del retester una enmienda acotada de admisión funded que exija, en el contrato trimestral calificado y con origen declarado, al menos un payout neto efectivamente recibido, ledger/cohortes completos y ausencia de bloqueos técnicos. El criterio sería filtro de coste de cómputo para esa etapa, sin afirmar robustez y sin transferir PASS de otro MM. Sus detalles de fase/origen/identidad y tratamiento de seed deben quedar aceptados antes de cualquier motor afectado.

La propuesta cambia un criterio material del G4 actual y por eso vuelve al Owner: **C01 no lo aplica, no crea un gate alternativo en código y no actualiza la skill/runbook.** Si el Owner conserva el criterio actual, FUNDED histórica queda pendiente salvo que exista un mandato y evidencia que cumplan íntegramente esa autoridad; no se ejecuta un challenge artificial sólo para maquillar el perfil funded.

Para SIMULATION, la aceptación futura debe fijar cómo se refiere la cadena de ambas etapas y qué canario conjunto demuestra compras/activación/payout/caja antes del histórico. No basta unir dos PASS aislados si la interacción de fondos/tiempos cambia el resultado. Esta definición vuelve al mismo owner de gates, sin crear otra metodología paralela.

### 12. Casos documentales de aceptación y oráculos

Las filas siguientes son criterios y revisiones de coherencia del diseño, **no tests físicos ejecutados**.

| ID | Caso | Oráculo / resultado exigido |
|---|---|---|
| V01 | Costes de todas las compras | C_eval suma compras ganadoras, perdedoras y pendientes; jamás sólo la cuenta que pasa |
| V02 | Cero pases/activaciones | Gasto visible, P/F=0, coste unitario N/A con razón; ninguna división que produzca 0 exitoso |
| V03 | Pendientes al corte | Tasas sobre todas y entre resueltas separadas; seguimiento/censura explícitos |
| V04 | Reset gratuito y pagado | Dos nuevos intentos vinculados si ambos ocurrieron; sólo el pagado debita; no se duplica el derecho ni el pase |
| V05 | Renovación sin reset | Un coste y extensión; mismo intento salvo autoridad contractual contraria |
| V06 | Pase sin activación | P aumenta; F no; se conserva fecha/causa/coste y eventual obligación |
| V07 | Funded quemada sin cobrar | Cuenta permanece en N; W=0 para ella; fallo económico separado del técnico |
| V08 | Dos payouts y pérdida posterior | Una iniciada, una pagadora, dos cobros, una pérdida; no borrar cash ni reabrir la cuenta |
| V09 | Split y cargos | Bruto→share→retención→neto una vez; fees ya en PnL no vuelven a salir de B |
| V10 | Activación en dos vistas | Puede mostrarse como información funded, pero sólo C_adq la descuenta |
| V11 | Cobro diferido/denegado | Solicitud y aprobación no financian compra; sólo fecha de crédito aumenta B |
| V12 | Liquidez insuficiente | No compra, no sobregiro, motivo visible; exactamente el coste permite una compra si no está comprometido |
| V13 | Pérdida nominal | No débito comercial adicional sin cargo contractual real |
| V14 | Estado funded condicionado | t_funded ≥ t_pass/activación y transformación de estado conforme al perfil; rechazo de origen futuro |
| V15 | Correlación simultánea | Misma señal/pérdida afecta cuentas a la vez; no IID por cuenta ni suma de cajas aisladas |
| V16 | Retry/cash idempotente | Mismo payout/cargo ya aplicado no cambia B otra vez; conflicto de payload bloquea |
| V17 | Compatibilidad legacy | Campo nuevo ausente conserva semántica histórica; no reinterpreta 5.000/120/4 payouts como 4.000/nuevo perfil |
| V18 | Fallo técnico | Mantener intento/evidencia/costes conocidos; no convertirlo en trading loss ni borrarlo del análisis |
| V19 | Final del horizonte | Cash recibido sólo hasta H, obligaciones/pendientes separadas; sin valoración nominal residual |
| V20 | Dos props y última liquidez | Un owner serializa compromiso; suma atribuida=total; no doble compra |
| V21 | Nuevo MM o retiro | Nueva identidad y gates afectados; no reescalar trade tape dependiente |
| V22 | Control de admisión | FUNDED/SIMULATION no eluden G4 por etiqueta; cada rechazo demuestra cero spawn |
| V23 | Cuenta recién comprada tras señal | Provisión y watermark respetados; no backfill de una oportunidad ya decidida NO_TARGET |
| V24 | Retiro y cuenta quemada con pago pendiente | Se aplica la regla contractual de elegibilidad/liquidación; no cancelación/cobro universal inventado |
| V25 | Compra cobrada sin provisión | U incluye la unidad y el gasto; provisión pendiente no produce 100% espurio |
| V26 | Bundle y cantidad desconocida | K conocido cuenta K raíces/1 cargo; K desconocido conserva coste y UNKNOWN_CARDINALITY |
| V27 | Refund posterior | Cohorte pagada bruta intacta; contra-coste una vez; no se clasifica como trading loss |
| V28 | Compra→primer cobro | Q cuenta raíces únicas con linaje completo; pagos repetidos no multiplican Q |
| V29 | CHALLENGE sin funded observada y seeds exógenas | q NOT_OBSERVED o UNKNOWN/NO_LINKAGE; nunca cero inventado ni producto de tasas |
| V30 | Crédito seguido de reverso | Primer cobro histórico visible; cash retenido neto/reverso visibles y conciliados |

La conciliación tiene tres oráculos: conservación del bankroll por eventos, partición no duplicada de costes y reconstrucción de métricas desde las unidades incluidas. Un cuarto oráculo causal rechaza funded antes del pase, cash antes del crédito y datos posteriores al cut. Replay idéntico por sí solo no sustituye estos oráculos.



### 13. Ejemplos contables pequeños

Todos los importes, fechas relativas, splits y reglas de esta sección son **ilustrativos**. No representan una prop seleccionada, tasas empíricas, métricas de S04 ni pruebas ejecutadas.

#### E0. Compras cobradas, provisión y conversión (corrección C03)

Casos ilustrativos, NOT_EXECUTED: dos compras de USD 100 con una unidad cada una, A entregada/pasada y B aún no provisionada ⇒ U=2, P_U=1, ratio=1/2, C_eval=200, coste/pase=200, provisioning_pending=1. Si B recibe refund=100, U bruta sigue en 2, coste neto=100; no se inventa una pérdida de trading. Una factura por dos unidades a USD 180 conserva U=2/cargos=1/coste=180; sin evidencia de cantidad, U=UNKNOWN y coste conocido=180.

CHALLENGE U=10/P=3 y FUNDED exógena N=3/pagadoras=1 no prueban q=1/10. Con linaje real, raíz A cobra 780 y 460, luego pierde la cuenta: Q=1, payout_count=2, W=1.240; un tercer pago aprobado sin recibir aporta cero a caja. Refund no cuenta como payout de trading. Un reverso posterior conserva el primer crédito y reduce W neto.

#### E1. Compras, resets, pendientes y pase sin activación

Cuatro derechos A1–A4 cuestan USD 100 cada uno. A1 tiene tres intentos: pierde el primero, usa reset gratuito, pierde el segundo, paga reset de 50 y pasa el tercero. A2 pasa en su primer intento; A3 pierde definitivamente; A4 sigue pendiente y pagó renovación de 20. Sólo A1 está activada funded mediante cargo de 80; A2 permanece pendiente de activación.

| Concepto | Resultado |
|---|---:|
| Derechos comprados / intentos iniciados | 4 / 6 |
| Intentos pasados / perdidos / pendientes | 2 / 3 / 1 |
| Derechos con pase / fallo final / pendientes challenge | 2 / 1 / 1 |
| Pase por adquisición al corte | 2/4 = 50% |
| Pase por intento al corte | 2/6 = 33,33…% |
| Pase entre derechos resueltos | 2/3 = 66,66…%, vista secundaria |
| Coste evaluación | 4×100 + 50 + 20 = 470 |
| Coste por pase | 470/2 = 235 |
| Funded disponibles | 1 |
| Coste agregado de adquisición | 470 + 80 = 550 |
| Coste por funded disponible | 550/1 = 550 |
| Bankroll después de pagos | 4.000 − 550 = 3.450 |

La unidad A1 no se cuenta tres veces como compra y su pase no se repite. El coste por funded al corte incluye los otros derechos, incluido el pase aún no activado y el pendiente; por eso se declara provisional. No se ha asumido obligación irrevocable de activar A2 en este ejemplo.

Si se hubieran gastado 200 con cero pases, el reporte conservaría B=3.800, gasto=200, pases=0 y coste/pase=N/A—NO_SUCCESSES.

#### E2. Todas las funded, pagos repetidos y pérdida posterior

Hay tres funded iniciadas A/B/C. A cobra dos veces: bruto 1.000 con share 80% y retención 20 produce 780 netos; bruto 600 con share 80% y retención 20 produce 460 netos. Luego A se quema. B se quema sin cobrar. C sigue activa y tiene pago aprobado de neto 380 aún sin recibir. Los costes operativos externos posteriores suman 30, no incluidos en payouts.

| KPI | Resultado |
|---|---:|
| Iniciadas / pagadoras | 3 / 1 |
| Quemadas antes de cobro / después | 1 / 1 |
| Pagos efectivamente recibidos | 2 |
| W | 780 + 460 = 1.240 |
| Cobro por toda iniciada | 1.240/3 = 413,33… |
| Margen funded antes de adquisición | (1.240−30)/3 = 403,33… |
| Media sólo entre pagadoras | 1.240, secundaria |
| Payout neto pendiente | 380, sin caja acreditada |

Si esas mismas tres cuentas tienen una adquisición trazable conjunta de 900, incluida toda activación y desafíos fallidos atribuibles, la contribución observada total es 1.240−30−900=310; por iniciada, 103,33…. Si provienen de seeds hipotéticas sin adquisición, ese 900 no puede inventarse ni sustituirse por cero.

#### E3. Recorrido completo, crédito demorado y recompra

| Momento | Evento | Cambio de cash | B liquidado |
|---|---|---:|---:|
| D0 | Caja inicial | +4.000 inicial | 4.000 |
| D1 | Dos compras de 100 | −200 | 3.800 |
| D2 | A pierde nominalmente 2.000; B pasa | 0 | 3.800 |
| D3 | Activación de B | −80 | 3.720 |
| D4 | Coste funded externo | −10 | 3.710 |
| D5 | Solicitud bruta de 1.000 | 0 | 3.710 |
| D6 | Aprobación de pago neto 780 | 0 | 3.710 |
| D7 | Débito nominal del retiro aplicado | 0 comercial | 3.710 |
| D8 | Crédito efectivo de 780 | +780 | 4.490 |
| D8 posterior | Compra sucesora | −100 | 4.390 |
| Retry | Reentrega del mismo crédito/compra | 0 | 4.390 |

Conciliación: **4.000+780−200−80−10−100=4.390**. Los 2.000 de pérdida nominal no se restan; el split/retención están dentro de 780 y no vuelven a cobrarse. La activación 80 sólo aparece en adquisición. Si H termina D6, B(H)=3.710 y payout pendiente=780, no B=4.490.

#### E4. Liquidez y obligaciones sin reserva prudencial

En otro corte ya conciliado, B=90 y existe payout aprobado de 780 pendiente. Una nueva compra cuesta 100: se rechaza por liquidez. Tras crédito efectivo, B=870; comprar una cuenta deja 770.

En un corte distinto con B=150 y una obligación irrevocable pendiente de 80, la caja libre propuesta es 70. No se admite una compra de 100 que utilice esos mismos 80 comprometidos. Al pagar la obligación, B pasa a 70 y el compromiso se extingue: no queda B=−10 por restar reserva y pago dos veces. Son compromisos existentes; no se añade un colchón de seguridad.

#### E5. Simultaneidad y causalidad

Dos props reciben la misma señal mediante asociaciones distintas y ambas cuentas sufren su stop en la misma trayectoria. El experimento conserva dos resultados económicos y una causa de mercado coincidente; no declara dos observaciones independientes.

Una política compra una evaluación el lunes y pasa el miércoles; las credenciales funded llegan el viernes. Usar un seed funded desde el lunes mide otra pregunta. No se le atribuyen los cobros lunes–jueves al recorrido de esa compra, aunque la suma de medias parezca favorable.

## PLAN — Impacto, reutilización y entrega incremental

### 14. Arquitectura propuesta y fronteras

**Se extiende Campaign/Platform alrededor del dominio SDK compartido.** Strategy no compra cuentas; MM no adjudica presupuesto común entre props; PoolManager no lleva balances ni calcula PnL; Provider conserva reglas/admisión/riesgo; accounting conserva ledger nominal. El owner comercial de Campaign mantiene caja, obligaciones y políticas de adquisición/retiro. No existe otra autoridad financiera en reporting.

La versión nueva debe ser opt-in y explícita. Los campos legacy ausentes conservan legacy; los campos nuevos obligatorios ausentes producen rechazo. No convertir por defecto FULL_JOURNEY histórico en la SIMULATION de 4.000. La implementación elige una revisión de schema compatible con el mecanismo vigente; no redefine silenciosamente PlatformCampaignSchemaV1.

**Ubicación mínima de los cambios:**

| Superficie existente | Cambio propuesto | Exclusión |
|---|---|---|
| Catálogo/manifiesto/preset del lab | Tuple completo y vinculación dual; políticas/origen/financiación/cohortes sellados | Sin DSL ni nueva base de catálogo |
| PlatformCampaignRequest/Profile/result | Extensiones versionadas de contratos y eventos necesarios | Sin prop hardcodeada nueva ni cambio global de defaults |
| Driver Platform y controles de cuenta | Recorrido por etapa, obligaciones/pagos, inicialización explícita | Sin fórmulas paralelas de MM, riesgo o PnL |
| SDK existente | Sólo un seam mínimo compartido si el baseline demuestra que falta | No import de backtester a SDK ni de Core/internal a backtester |
| Reporting lab | Proyecciones derivadas y comparaciones por etapa/campaña | No modifica decisiones, fills o estado |
| Runner/supervisor | Admission y ejecución de ítems por infraestructura existente | No otra cola/scheduler/daemon |
| Adapter simulado | Hechos/modelo de venue y driver temporal | No emula una certificación de broker/NT |

Una utilidad común sólo se extrae si tiene consumidores concretos. Aquí, la partición de costes y la agregación por cohorte tienen dos usos inmediatos CHALLENGE/FUNDED y un tercero SIMULATION; pueden vivir junto al reporting actual. No se justifica un framework financiero universal ni un language de estrategia.

#### 14.1 Partición mínima y extensibilidad

| Dueño existente | Responsabilidad única | Extensión aditiva |
|---|---|---|
| SDK Strategy + analytics | Setup/filtro/objetivo técnico y observaciones causales | Un módulo/archivo por implementación y registro explícito en la factory compartida |
| SDK MM | Cantidad y gestión monetaria por cuenta/Operation/etapa | Un paquete/config por MM; no recibe del lab una fórmula alternativa |
| Provider + accounting + pool reducer | Reglas, límites, fills, PnL nominal, claims/afinidad/drain | Contratos del runtime como autoridad; no duplicarlos en Campaign |
| Platform Campaign | Lifecycle comercial, contexto por etapa, obligaciones/pagos y único owner de bankroll | Configuración tipada versionada sobre modos existentes; sin otra cola ni motor |
| Lab reporting | Proyección pura de eventos a cohortes/KPI, completitud y comparación | Adaptador legacy + reporte económico opt-in; no decide operaciones |
| Runner/supervisor | Jobs, intentos físicos, admisión y receipts | Cola existente y recursos medidos; paralelismo lógico independiente de concurrencia física |

La relación de dependencias sigue siendo backtester→SDK y lab→artefactos de ejecución, nunca SDK→lab ni backtester→Core/internal. Una factory explícita y módulos concretos permiten agregar estrategias/MM sin modificar scheduler/ledger/venue. No crear una interfaz por tipo ni un catálogo dinámico universal anticipando cientos de estrategias; extraer sólo una costura con consumidores concretos. El tamaño futuro se maneja con módulos pequeños, identidades y pruebas propias.

La interpretación pública CHALLENGE/FUNDED/SIMULATION se materializa sobre CHALLENGE_ONLY/FUNDED_ONLY/FULL_JOURNEY con revisión económica explícita. La comparación dual es un vínculo de batch: mismo input técnico cuando corresponda, estados económicos independientes y ningún dinero compartido. SIMULATION sí necesita un reloj comercial y una caja comunes. La inmutabilidad/digest sella semántica; no usar IDs de intento o el orden de workers como lógica económica.

### 15. Inventario de reutilización y límite del receipt

| Activo | Evidencia disponible | Reutilización propuesta | Condición de vigencia |
|---|---|---|---|
| S04 catálogo26/variantes/derive | Planner C01, C04 y cierre documentados | Identidades y generación finita | Mapa a blobs integrados y config efectiva |
| Runner plan/prepare/run/resume/reconcile | Planner C02; CLI Platform inspeccionada | Transporte único de jobs y attempts | Verificar seam integrado y guard activo |
| Characterize/reconcile/adjudicate | Planner C03/C07 y R03 | Eventos→operaciones→cohortes/reportes | Nuevo KPI versionado; datos originales íntegros |
| Export/validate-bundle | Planner C08, DRAFT_DISABLED | Pin de MM/filtros y provenance | No heredar RUNTIME_READY |
| Preparación datasets/TG | CLI inspeccionada, cache por key completa | Compartir bytes/analytics puros | Demandas y cut causal equivalentes |
| Cash/PlatformPayment/controls | Código observado en S07–S10 | Dinero exacto, lifecycle y trazabilidad | Ampliar cargo/event ID y obligaciones donde falten |
| Compartimentos/SDK accounting/provider/operation | Código de llamadas y R6 | Estado aislado, transición y autoridad | Paridad contra el baseline aceptado |
| Pool/fanout/afinidad/drain | R6 y GOD-05 | Composición multi-asociación posterior | Evidencia de reducer/adapter integrado, no sólo existencia de tipos |
| Supervisor R02/R03 y resource receipt | Planner/runbook | Techo global y admisión por recursos | Comprobar único supervisor al despacho futuro |
| Fixtures S04/F1–F4, RGMM/EntryFilters | Planner registra cobertura y recibos | Conservar oráculos que cubren semántica no cambiada | Ejecutar sólo afectados al implementar |
| R03 protected-close y censo 89/89 | Receipt resumido por planner, exactos commits históricos | Regresión de finality/cierre y evidencia económica histórica | No extrapolar a nuevas reglas/fees/MM |
| CAMPAIGN legacy/replay | X01 y README | Compatibilidad de sealed request, evento de cash y delimitación de driver | No mezclar con Platform como si fuese el mismo formato |

Esta tabla no certifica que los tests estén presentes/verde en el binario integrado. La cápsula condicional y el manager de integración deben devolver esa correspondencia. La presencia de un test en el árbol o un porcentaje histórico no equivale a ejecución actual.

### 16. Incrementos y dependencias

| Incremento | Outcome verificable | Dependencias | Aceptación |
|---|---|---|---|
| I0 — contratos/KPI, activo | Proyección económica opt-in desde evidencia existente, F01/F02 y UNKNOWN explícitos | Source 2baf319d y paquete LOCAL acotado; ninguna decisión económica abierta se adjudica | Casos contables y legacy exactos; entrada intacta; cero motores |
| I1 — CHALLENGE | Cohortes continuas, compra/provisión/intento/reset, pase/fallo/pendiente y costes | I0; perfil declarado; S04-F01 resuelto para identidad consumida; guard vigente antes de campañas | Campaña no termina al primer pase; todos los costes/pendientes; cadena propia |
| I2a — FUNDED aislada | Origen/estado/fecha, todas las iniciadas y lifecycle de múltiples pagos | I0 + perfil y origen funded; no depende de I1; D05 condiciona histórico afectado | N/W/F_op y primer cobro conciliados; aislamiento; pérdidas/reversos visibles |
| I2b — comparación dual | Dos resultados por etapa ligados por identidad, comparables con sus límites | I1 + I2a | MM/RuleSet/ledger aislados; no multiplicar tasas ni sumar cajas como simulación |
| I3 — SIMULATION 1×1 | Compra→pase→activación→cash→recompra con B0=4.000 | I1 + I2a; términos/financiación y admisión conjunta; no depende de una UI dual | Reserva/cargo/cobro únicos, liquidez y resume deterministas, cero aportes |
| I4 — multi-Strategy/multi-prop | Varias asociaciones sobre mercado común y una caja | I3; segundo perfil; adapter R6 y capacidad medida | Contención real por caja, fanout simultáneo, claims/drain y atribución exactos |

I1 e I2a pueden desarrollarse en paralelo sólo con ownership de archivos disjunto y contrato I0 estable; si pisan el mismo driver, un único writer las entrega secuencialmente. FUNDED aislada no espera resets challenge. Las próximas iteraciones se mantienen como outcome/dependencias, sin preimplementar I3/I4 en I0. El gate de baseline S04 y la admisión de campañas se resuelven antes de consumir esas capacidades en ejecuciones; no bloquean la proyección pura y honesta del slice I0.

### 17. Incremento activo: I0 — contrato y proyección económica

**Resultado:** leer un artefacto existente y explicar exactamente qué compra/cuenta/intento observó, cuánto pagó/cobró, qué denominadores conoce y qué no puede adjudicar. Extender el lab con contrato/reporting opt-in, sin cambiar decisiones de trading ni ejecutar campañas.

**Autorización y estado:** el Owner solicita diseñar y comenzar implementación. El paquete concreto está en [[EF-CAMPAIGN-MODES-I0-LOCAL]], para el ejecutor LOCAL existente; no se crea otro manager. READY_FOR_AUTHORIZED_IMPLEMENTATION significa permiso del slice documentado, no código ya ejecutado, aceptación de S04 ni aprobación automática del resultado.

#### 17.1 Base, branch, responsables y recursos

- Repo producto: `xKoRx/echo`. Base SOURCE comprobada: `2baf319ddcba622d9557bc9f23a13787b44c58a7`. La aceptación semántica de S04 está abierta; I0 no depende de atribuir equivalencia económica a sus 89 filas.
- Branch: resolver primero el WIP del ejecutor. Reusar la rama propia de I0 si existe y cumple base; de lo contrario crear `feature/ef-campaign-modes-i0` desde ese SHA. Rama propuesta, NO creada por CLOUD. Un descendiente requiere reconciliación de delta y evidencia de alcance, sin reset ni overwrite.
- Responsable implementación: ejecutor NORMAL/GLM-5.3-Flash LOCAL vigente en Hefesto. Verificador independiente: TOP LOCAL, contexto fresco, después del SHA candidato. Corrección final: NORMAL LOCAL; manager adjudica retorno sin autoaceptar gates.
- Presupuesto I0-S1: máximo 150 minutos, incluyendo hasta 30 de reconciliación focal y 20 finales de evidencia/cierre; un writer, cero motores de campaña, cero compras/trading/deploy. Presupuesto técnico del encargo, no un cap financiero del modelo.
- Control documental: Agents-OS master, único writer con HEAD reconciliado, sin ramas/PR/force. I+D conserva su planner central.

#### 17.2 SPEC funcional y técnica del slice

Aplican §§4–7 y §6.4 corregidos. F01: compra cobrada anterior a provisión, bundles conocidos/desconocidos, resets/renovaciones/retries y refund separado. F02: conversión directa por linaje, q ausente por alcance o evidencia incompletos. Cada métrica conserva numerador/denominador exactos, estado/razón y evidencia; no usar valor cero como ausencia. Contrato/report schema nuevo opt-in; los reports/receipts/catalog-v1 y la adjudicación 25% permanecen íntegros.

Separar un adaptador de evidencia legacy, proyección pura e integración CLI/report dentro del lab existente. El adaptador sólo recupera relaciones inequívocas; un importe conocido sin relación a cuenta permite total, pero no atribución inventada. No rellenar event_id, fechas, financiación ni origen. Un nuevo contrato puede validarse como completo; el reporte legacy parcial sigue siendo útil sin pretender que sirve para SIMULATION.

La evidencia de dinero usa valores exactos ya disponibles (decimal/racional); redondear únicamente al presentar. El reducer de reporte deduplica efectos con identidad estable y falla ante mismo ID/términos incompatibles. No simula que ya existe un nuevo ledger/driver: sólo proyecta eventos/fixtures identificados y verifica su reconciliación.

#### 17.3 Superficie real y límites

| Archivo/superficie existente | Uso en I0 |
|---|---|
| `v3/backtester/tools/tradesgerard/campaign-lab/campaign_lab.py` | Validación/materialización y digest; extensión opt-in |
| `.../research_lab.py` | Lectura de `_census`, `characterize`, `row_from_char`, `adjudicate`; integración aditiva del reporte |
| Tests y documentación del mismo directorio | Regresiones nuevas; tests existentes sólo con TCR si la policy lo exige |
| `specs/FEAT-CHALLENGE-HISTORY/` | Leer feature existente y registrar change SDD del slice conforme al catálogo, sin segunda SPEC contradictoria |
| `platform_campaign.go`, `platform_research.go`, SDK | READ_ONLY para contrato de entrada y reconciliación S04; no cambios Go en I0 |
| Artefactos/planes/catálogos/receipts sellados | READ_ONLY; reporte derivado en destino nuevo y checksums de entrada |

No existe `research_campaign.py` en el corte inspeccionado; no referenciarlo como fuente. Si conviene extraer una función pura a un módulo pequeño junto al lab, registrarlo como archivo create en PLAN/Allowed Files antes de IMPLEMENT. No instalar framework, DB, servicio, scheduler, DSL ni un nuevo motor financiero.

#### 17.4 Aceptación

1. Dos unidades cobradas, una pasada y otra no provisionada, conservan U=2 y tasa 1/2, con gasto 200 en el caso ilustrativo.
2. Bundle conocido cuenta unidades una vez; cantidad desconocida conserva gasto y bloquea sólo ratios dependientes.
3. Reset gratis/pagado, renovación, retry y refund producen identidades/costes exactos; el refund no borra la cohorte pagada bruta descriptiva.
4. P=0/F=0/N=0/UNKNOWN/NOT_OBSERVED son distinguibles; ningún coste unitario de éxito cero es 0.
5. Dos pagos de una raíz cuentan Q=1; approved-only no cuenta. Una pérdida nominal posterior no borra el historial ni debita cash comercial ya recibido. Un reverso financiero preserva el historial del primer crédito y Q, pero resta el importe efectivamente revertido de W/cash neto; +780 y reverso −780 dejan Q=1 y cash neto=0.
6. CHALLENGE sin observación funded y FUNDED exógena no fabrican q=0 ni q como producto de tasas; linaje incompleto tiene razón explícita.
7. Activación, fees retenidos, refunds y PnL nominal no se descuentan o acreditan dos veces; sumas por asignación concilian con cash total.
8. Eventos duplicados son idempotentes; mismo ID/términos distintos produce conflicto. Cortes temporales y eventos posteriores al cutoff no se adelantan.
9. Input y receipts quedan byte-intactos; salida determinista; sentinel independiente demuestra cero spawn/egress; legacy 25%/5.000/perfiles originales permanece igual.
10. Smoke E2E LOCAL del comando de reporting real sobre al menos un artefacto recuperable y fixtures explícitos para huecos. E2E del reporte no es backtest ni certificación financiera.
11. Pruebas afectadas y ≥95% de coverage del desarrollo nuevo, con invariantes críticas primero; no limpiar deuda ajena ni maquillar fallos ambientales.
12. Devolver candidato/SHA/commands/receipts y baseline observations separados. Gate final REVIEW.

**Rollback:** no consumir el reporte opt-in y revertir sólo commits propios si corresponde; inputs/receipts anteriores siguen disponibles. **Parada:** presupuesto, WIP ajeno en conflicto, fuente/contrato imprescindible ilegible o necesidad de tocar runtime/gates. Un gap de equivalencia histórica no se rellena: el reporte preserva UNKNOWN y se bloquea sólo la aceptación afectada.

#### 17.5 Reconciliación focal incluida, sin rehacer S04

Recuperar build/logs/failure sets/retorno completo del verificador existente. Para S04-F01, censar planes efectivos sellados de las 26 nativas por policy y hash; demostrar la frontera V1 con fixtures acotados de los dos cortes, sin campañas ni modificación del runtime. Si falta evidencia, retornar dependencia exacta y continuar el reporte independiente. S04-F02 queda requisito previo de I1/I2a que lanzaran motores: portar/adaptar guard vigente por cambio explícito, nunca un bypass desde el reporte.

## TASKS — Secuencia derivada para I0

Las tareas siguientes están preparadas para I0-S1 bajo el único manager. Código/test: NOT_EXECUTED por CLOUD. El paquete LOCAL fija permisos, recursos y retorno; no inicia I1.

| Task | Trabajo y superficie | Dependencia | Evidencia de aceptación |
|---|---|---|---|
| I0.T1 | Reconciliar WIP/base y S04-F01/F02 de forma focal | Fuente 2baf319d + retorno existente | Matriz SOURCE/BUILD/TEST/ACCEPTANCE/DEPLOY; planes/policies/receipts o UNKNOWN; ninguna reejecución S04 |
| I0.T2 | Fijar schema/validación del contrato y reporte opt-in dentro del lab y del change SDD; catálogos/manifiestos históricos read-only | T1 + revisión de C01 | Identidad incluye modo/etapa/políticas/origen; campos UNSET no se completan tácitamente |
| I0.T3 | Mapear evidencia legacy por capacidad de derivación | T2 | Dos ejemplos reales recuperables o ausencia explícita; tabla recuperable/UNKNOWN |
| I0.T4 | Extender proyección económica en reporting existente | T3 | U pagada antes de provisión; Q/q longitudinales; costes/payouts/censura y ausencia localizada |
| I0.T5 | Implementar conciliación y negativos de doble conteo/identidad | T4 | Casos E1/E2/E3; duplicado mismo ID sin doble cash; conflicto bloqueado |
| I0.T6 | Verificar no mutación/no spawn/compatibilidad legacy y regresiones afectadas | T4–T5 | Entrada byte-intacta, salida determinista, cero motores y semántica anterior conservada |
| I0.T7 | Documentar comandos realmente disponibles y límites | T6 | Uso reproducible desde el checkout aceptado; sin flags inventados |
| I0.T8 | Entregar diff/receipt y revisión independiente del slice según manager | T7 | Source exacto, pruebas ejecutadas por el futuro worker, pendientes y OWNER_ACCEPTANCE=REVIEW |

**Acción vigente C03: ejecutar únicamente I0-S1 del paquete [[EF-CAMPAIGN-MODES-I0-LOCAL]].** El Owner ya pidió comenzar implementación; no se vuelve a pedir permiso por decisiones rutinarias de código dentro del slice. El reporte describe y valida; no decide D01–D06 ni financia un cargo. Si aparece una contradicción de autoridad, devolverla sin alterar runtime/gates.

### 18. Retorno focal esperado de Hefesto

La cápsula C01-BASELINE-READONLY queda SUPERSEDED por I0.T1: ya se recibieron el retorno de integración y la inspección SOURCE. No abrir otro preflight general ni otro merge.

Un solo retorno local debe distinguir: (a) planes/configs realmente ejecutados y evidencia de V1, (b) build/tests e informe independiente recuperados, (c) ubicación del guard y delta necesario para lanzamientos posteriores, (d) candidato de contrato/reporting I0 con pruebas propias. Persistir los artefactos faltantes en un bundle de recibos del ejecutor, con checksums y rutas relativas, sin copiar logs pesados al vault.

S04-F01 no autoriza cambiar V1 a Unclipped en bloque ni alterar el runtime. Si se requiere migración prospectiva, devolver propuesta con identidad/compatibilidad y evidencia de frontera; los receipts históricos conservan el intérprete original. S04-F02 no autoriza portar toda la rama ClutiFX. Ambos hallazgos se resuelven en su autoridad antes de afirmar equivalencia o ejecutar nuevas campañas.

## Decisiones abiertas, verificación y cierre

### 19. Decisiones focales para Owner y dependencias

Las decisiones aceptadas del mandato no se vuelven a someter a votación. Esta tabla contiene sólo material nuevo o todavía no fijado; la propuesta permite revisar un diseño completo sin presentar esas elecciones como autorizadas.

| ID | Decisión pendiente | Propuesta concreta de C01 | Efecto hasta resolver |
|---|---|---|---|
| D01 | Unidad primaria del umbral 1/3, refunds, resets y horizonte | Propuesta corregida: cohorte bruta de unidades comerciales inicialmente cobradas, éxito único, resets vinculados; vistas de provisión/cuenta/intento separadas | I0 implementa descripción de esas vistas; no adjudica 1/3 sin decisión aplicable y H explícitos |
| D02 | Ventana de incorporación, horizonte H por unidad y horizonte Hc de campaña | Predeclarar fechas/cutoff y seguimiento común; distinguir seguimiento completo, censura y cola de cobros | No seleccionar un ganador económico ni declarar comparación homogénea sin esos valores |
| D03 | Fuente de financiación de activación, renovaciones y demás cargos obligatorios | Todos los cargos externos salen de los mismos 4.000 USD más cobros netos recibidos, con obligaciones y liquidez explícitas; ningún aporte/Forex | La simulación finita no es admisible mientras haya cargos obligatorios sin financiador autorizado; las proyecciones aisladas pueden declarar MEASUREMENT_ONLY |
| D04 | Función de selección y políticas económicas candidatas | Seleccionar por J(Hc), caja liquidada al horizonte menos obligaciones irrevocables no pagadas, mostrando caja bruta/disponible, incertidumbre y censura; comparar un conjunto pequeño de tuples completos según sección 9 | Es criterio propuesto, no objetivo aceptado ni permiso para buscar combinaciones; se conserva la separación selección/evaluación |
| D05 | Admisión histórica de FUNDED aislada o MM distinto frente a G4 | Solicitar decisión focal al Owner y traducción por el owner de gates; propuesta de evidencia funded específica en sección 11, manteniendo el resto de requisitos | G4 vigente continúa exigiendo CHALLENGE_PASSED de la identidad aplicable; no se hereda PASS, no se aplica excepción ni se corre el histórico afectado |
| D06 | Instancias concretas de Strategy/prop/origen funded y términos económicos | Consumir retornos A/B y reglas oficiales versionadas cuando estén disponibles; empezar por una pareja ya admisible sin elegir proveedor comercial aquí | Contratos genéricos listos; sizing exacto, reglas comerciales, fees, calendario y conclusiones por prop/Strategy quedan UNKNOWN |

**Decisiones técnicas rutinarias ya resueltas como parte del candidato:** reutilizar los modos de etapa S04 y el batch existente; dos ítems independientes para comparación dual; identidad por semántica; costes atribuidos por evento; compras/intentos separados; idempotencia de cobro; ausencia de éxito como N/A del coste unitario; una caja en la composición; simulación causal conjunta; legacy opt-in y UNKNOWN granular. No requieren crear otro programa ni obtener permiso para cada nombre de campo.

El modo de ejecución BASIC/CAMPAIGN del backtester y el modo de etapa Platform son ejes distintos. La comparación dual tampoco es un tercer motor: enlaza dos experimentos de etapa mediante el identificador de comparación. La propuesta no cambia la señal, geometría o autoridad de cálculo para resolver esos ejes. [R06, S07a–b, X01]

### 20. UNKNOWNs y bloqueo exacto de la siguiente acción

| Evidencia no recuperada | Dependencia exacta | Acción afectada | Acción que sigue disponible |
|---|---|---|---|
| Equivalencia semántica de S04 y planes nativos efectivos | S04-F01 en reconciliación; fuente 2baf319d sí demostrada | Aceptar equivalencia de las 89 o usar sus resultados como PASS del runtime integrado | Implementar I0 descriptivo opt-in/no-spawn sobre source verificado, con límites explícitos |
| Guard vigente ausente del master pre-ClutiFX | S04-F02; adaptación explícita por owner del launcher antes de ejecutar | Nuevas campañas/quarter/histórico o resume que lance motores | Contratos, reporter, fixtures deterministas sin campañas |
| Binario/build, fixture/test receipt y aceptación física del integrado | Artefactos sellados del owner técnico existente | Declarar capacidad certificada o desplegable | Distinguir código observado y receipt histórico |
| Retornos A/B publicados | A/B del ciclo FUT-R01 o estado documental actualizado | Conclusión específica de Strategy/prop y selección comercial | Diseño genérico por contratos |
| Reglas oficiales vigentes, costes, activación, payout/denegación y clock de cada perfil | Snapshot oficial fechado y decisiones de perfil por prop/programa/etapa | Ejecutar escenario FACT y sizing exacto | Definir campos y escenarios DESIGN_SCENARIO inequívocos |
| Dataset/eventos suficientes para fills y replay exactos | Receipt de datos/modelo y ledger requerido según sección 10 | Reclamar exactitud física, cotas conservadoras o paridad integral | Simulación declarada y paridad limitada al nivel soportado |
| Admisión G4 funded o identidad con MM distinto | Decisión D05, aplicada por autoridad de gates antes de despacho | Histórico funded afectado y composición no admitida | I0 documental/reporting y desarrollo futuro dentro de sus permisos |
| Fuente autorizada de todos los costes obligatorios | D03 y contrato completo de obligaciones | SIMULATION finita ejecutable | Exponer coste y déficit sin inventar fondos |
| Consumo de pool Pro | Medición/receipt de cuota atribuible a esta sesión | Confirmar delta de PRO_CHAT_POOL | Declarar UNKNOWN; no modificar contadores compartidos |

Los UNKNOWNs limitan exactamente el claim o acción de su fila. **Diseño C03 listo para revisión; paquete I0 READY_FOR_AUTHORIZED_IMPLEMENTATION; código NOT_STARTED.** La orden Owner autoriza ese slice acotado, no la aceptación de los gates ni campañas posteriores. SOURCE S04 es conocido; su equivalencia semántica permanece en revisión.

### 21. Verificación documental original C01 y límites del resultado

Se inspeccionaron las autoridades y el código citado contra refs fijadas, se comparó la presencia de los modos de etapa en master y en la referencia S04, y se revisó cada caso V01–V24 contra las definiciones del SPEC. Los ejemplos E1–E4 se reconciliaron aritméticamente; E5 revisa dependencia temporal. Son revisiones documentales realizadas por este worker, sin revisor independiente ni aceptación del Owner.

La verificación separa cuatro afirmaciones: **el símbolo fue leído**, **un planner refiere un receipt**, **una integración informa un corte** y **ese corte recibió aceptación/certificación**. C01 sólo afirma las dos primeras cuando tiene su soporte, y conserva UNKNOWN en las demás. No transforma una captura de fuente en resultado de ejecución.

| Control del mandato | Resultado documental |
|---|---|
| Costes de todas las compras, cero pases, resets y pendientes | Definidos en secciones 5/7 y E1; sin coste unitario cero ficticio |
| Pase sin activación, origen funded y estados derivados del pase | Separados en secciones 4/6/8; E1/E5 no crean funded disponible anticipada |
| Quemadas sin cobro, varios pagos y pérdida posterior | Denominador de todas las iniciadas; atributo pagadora acumulativo; E2 |
| Split/cargos una vez y cobro diferido | Ledger y partición por evento; solicitud/aprobación no son caja; E2/E3 |
| Compra sin liquidez, pérdidas nominales y obligaciones | Rechazo causal de compra y libros separados; E3/E4 |
| Dependencia temporal y correlación simultánea | Recorrido conjunto, mismos datos/señales y cohortes; E5 y sección 8 |
| Retry y compatibilidad legacy | Claves de idempotencia propuestas y opt-in semántico; V16–V19 y PLAN |
| Selección/evaluación, sizing y gates | Predeclaración, separación temporal y G4 sin excepción; secciones 9–11 |

**No se ejecutaron tests de producto, campañas, compras, simulaciones de mercado, builds ni operaciones en hosts.** Tampoco se alteró el merge, el planner, las autoridades compartidas o los gates. La revisión de schema/Markdown y la conciliación aritmética de ejemplos son controles del documento, no evidencia física de Backtester. Los recibos previos conservan su propio alcance y no fueron reejecutados.

### 22. METHOD_DELTA y REUSABLE_BEHAVIOR_CANDIDATES

**METHOD_DELTA: PROPOSED — aplicado sólo como disciplina de esta entrega, sin cambio de método canónico.** Antes de decidir que una capacidad falta, comparar símbolo, ref, significado y receipt en una matriz corta. El caso comprobable es CampaignMode: falta en la versión master observada de PlatformCampaignRequest y aparece en la referencia S04; la conclusión correcta es “reutilización condicionada a integración”, no “crear modos desde cero”. La segunda mejora local es revisar denominadores y cargos por evento antes de componer resultados. [S07a–b, S03]

**REUSABLE_BEHAVIOR_CANDIDATES:**

| Candidato | Evidencia en esta sesión | Segundo uso concreto | Destino propuesto, sin promoción |
|---|---|---|---|
| Matriz source/receipt/integración/aceptación por capacidad | Discrepancia master/S04 en modos y financiación research | Integración runtime/lab y futuro incremento multi-prop | Evaluación por manager en el runbook existente; no skill nueva |
| Checklist de unidad, censura, coste y caja antes de KPI | E1–E4 evitan éxito duplicado, coste cero y pago pendiente como efectivo | CHALLENGE/FUNDED aislados y SIMULATION | Contrato/reporting de I0, no utilidad universal |
| Lectura selectiva del planner y ampliación sólo ante contradicción | Planner amplio con estados/contratos/receipts pertinentes; X01 y S07b resuelven un contraste concreto | Siguiente revisión de integración y reutilización S04 | Feedback de sesión; no ampliar el routing por defecto |

No se editaron skills, runbooks, gates, memoria compartida ni el sistema de admisión como efecto lateral. Estos candidatos no son instrucciones nuevas para el siguiente worker.

### 23. Cierre histórico exclusivo de C01 (no cierra C03 ni al manager)

- **Tipo de sesión:** diseño/documentación con inspección estática de fuentes. No fue implementación, ejecución de research ni code review formal de corrección del producto.
- **Agent run:** omitido según agents-os-agent-run-register: la sesión documental no activa un run de implementación/prueba/ejecución/revisión formal. No se fabricó un receipt de motor, host o binario.
- **Feedback:** materializado en [[2026-10-28-echo-futures-c01-campaign-modes-session-feedback]]; registra el contraste de cortes, el límite de evidencia y una mejora focal.
- **Change log:** [[2026-10-28-echo-futures-c01-campaign-modes]]; cambio documental limitado a informe, feedback y cierre. No se edita el planner del manager.
- **Continuidad:** este informe contiene estado, decisiones, tareas y dependencia exacta. No se creó transcripción L0/L1 ni se hizo promoción a L3; no había transcript literal aportado para archivar.
- **Publicación:** Agents-OS master mediante reconciliación de HEAD y actualización condicionada al SHA padre; el commit y su verificación se devuelven en el handoff. Ninguna rama/PR/force. Una colisión con trabajo concurrente exige relectura, no sobrescritura.
- **Graphify/índice local:** UNKNOWN en esta superficie CLOUD; la publicación remota no acredita sincronización o recuperación local. No se despachó mantenimiento de hosts.
- **PRO_CHAT_POOL_DELTA: UNKNOWN.** El nombre del modelo/superficie no es un receipt de cuota. No se aumenta ni corrige un contador por inferencia.
- **Cierre:** sólo esta ONE-SHOT. Owner revisa; manager integra; los owners técnicos conservan implementación y gates. El programa permanece abierto.

## Fuentes

### 24. Registro de fuentes y presupuesto

Las referencias siguientes son permalinks de lo leído, no una afirmación de que ese corte sea el baseline integrado certificado. Los diez grupos S01–S10 constituyen las fuentes técnicas decisivas previstas. X01 y la segunda versión S07b son ampliaciones focales para resolver la contradicción de modos y caja; el bootstrap/routing/templates de cierre se registran aparte. No se abrió otro Deep Research ni se hizo selección comercial.
#### Fuentes técnicas

- **S01 — [main/10-projects/Echo I+D/Echo I+D — Futures.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/10-projects/Echo%20I%2BD/Echo%20I%2BD%20%E2%80%94%20Futures.md)**. Blob `1eb3b808dc37eff5f091ccb6ba73fbbe38a09e6c`. Estado del programa, decisiones Owner y dependencias A/B; lectura focal de estado/economía/ciclo.
- **S02 — [main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/10-projects/Echo%20I%2BD/artifacts/FUT-R01/FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION.md)**. Blob `479806d5c742b7b19693dc69dc4ed2d5a0b1df22`. Mandato FUT-R01 de campañas; requisitos y límites, sin reabrir los DR.
- **S03 — [main/10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/10-projects/Echo%20Futures/agentes/Echo%20Futures%20%E2%80%94%20Optimizaci%C3%B3n%20de%20Campa%C3%B1as.md)**. Blob `b7aa3010c58c568c183e4147ee2ca3dc1ae192c8`. Planner técnico: sólo estados, contratos, S04/R03 y recibos pertinentes; no se tomó todo el planner como nuevo scope.
- **S04 — [main/10-projects/Echo Futures/artifacts/runtime/EF-BACKTEST-RUNTIME-INTEGRATION-PLAN.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/10-projects/Echo%20Futures/artifacts/runtime/EF-BACKTEST-RUNTIME-INTEGRATION-PLAN.md)**. Blob `30ecc22283c48b4f5b65b6f53f95054c5e88d226`. Plan de integración runtime/backtester: delta de arquitectura, replay, fase y caja.
- **S05 — [main/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/10-projects/Echo%20Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md)**. Blob `88e04100b242e99d2000494fa727043dd9b19a6d`. Autoridad R6: secciones de pools, afinidad, claims, fanout, drain y presupuesto MM.
- **S06 — [main/10-projects/Echo Futures/artifacts/runtime/production-readiness/EF-PROD-GOD-05-MANAGER-ADJUDICATION.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/10-projects/Echo%20Futures/artifacts/runtime/production-readiness/EF-PROD-GOD-05-MANAGER-ADJUDICATION.md)**. Blob `1e19c58fd8831317e8f341537447e7a958ead319`. GOD-05: adjudicación y enmiendas M01–M07; alcance DEV/documental y no certificación PROD.
- **S07a — [v3/backtester/platform_campaign.go](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_campaign.go)**. Blob `24a86ff8fd23825ec1ec597e90e698f7b7ede620`. Fuente Platform en master remoto: request/result, caja, runner, lifecycle y pagos.
- **S07b — [v3/backtester/platform_campaign.go · S04](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/platform_campaign.go)**. Blob `862263302b0172f070c226c0e5e942c18a960832`. Mismo archivo en la referencia S04: modos de etapa, continuidad, seed y research cash; lectura adicional para cerrar contradicción.
- **S08 — [v3/backtester/platform_profile.go](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_profile.go)**. Blob `b60daa689839bc6d04e83d3333d208b2cda68c31`. Fuente del perfil comercial y PayoutNet: observado como implementación histórica, no como términos oficiales actuales.
- **S09 — [v3/backtester/platform_economics.go](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_economics.go)**. Blob `e602caafbc4d810dd66b7b1914e07a3a38879edc`. Fuente de conciliación nominal/ciclo y reserva económica compartida.
- **S10 — [v3/backtester/cmd/echo-backtest/platform.go](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/cmd/echo-backtest/platform.go)**. Blob `2fbfab0905d76266f450208005140115ea4b38fd`. Fuente del CLI Platform/batch: entrypoints, preparación, reuse y provenance.
- **X01 — [v3/backtester/campaign.go](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/campaign.go)**. Blob `e3f0d27e8e970ad068800bb702df79b11519062c`. Driver CAMPAIGN legacy: identidad y cash separados de Platform; lectura adicional para desambiguar modos.

#### Routing mínimo y cierre

- **R01 — Bootstrap y routing de responsabilidad.** [main/AGENTS.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/AGENTS.md) (blob `8c38d41c16eed31746c0a2c0cd2395270a71efc9`); [main/80-agents/agents-os/agents-os.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/agents-os/agents-os.md) (blob `da66d662c0ebb87bd492013a7533bd45060eb111`); [main/80-agents/skills/agents-os-bootstrap/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/skills/agents-os-bootstrap/SKILL.md) (blob `85005f25d445756b30bb8bb43cff755367232220`); [main/30-resources/agents/skills/echo-futures-research-manager/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/30-resources/agents/skills/echo-futures-research-manager/SKILL.md) (blob `725a7c77100c94f35b847e407c4b34a6831f89e7`).
- **R02 — Gestión técnica y SDD.** [main/30-resources/agents/skills/technical-project-manager/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/30-resources/agents/skills/technical-project-manager/SKILL.md) (blob `c35f6765134a9e596de18d582cf730356b320f76`); [main/30-resources/agents/skills/sdd-workflow/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/30-resources/agents/skills/sdd-workflow/SKILL.md) (blob `189cb3466e854d093c9a120777b4e9418596d5ea`).
- **R03 — Ciclo I+D.** [main/30-resources/runbooks/echo-rnd-cycle-runbook.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/30-resources/runbooks/echo-rnd-cycle-runbook.md) (blob `ac120854ee42ba3dfcbaaf66382007d26f22ebf8`).
- **R04 — Retester y admisión.** [main/30-resources/agents/skills/echo-retester-master/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/30-resources/agents/skills/echo-retester-master/SKILL.md) (blob `6755affbe3c8337a618cd235fe34c451662b1b7a`).
- **R05 — Calificación Strategy.** [main/30-resources/runbooks/echo-futures-strategy-qualification-runbook.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/30-resources/runbooks/echo-futures-strategy-qualification-runbook.md) (blob `5b40ec8ae69c195ffd84d85a046cc835031eeccb`).
- **R06 — Routing técnico de Echo y contrato de modelos.** [AGENTS.md](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/AGENTS.md) (blob `2e4b7ad1146d639e18d3eed6c270bd47fb9855de`); [v3/backtester/README.md](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/README.md) (blob `66267be80dfc3f63ec44f5e7327ce4c40cdc3813`).
- **R07 — Registro, feedback y cierre de sesión.** [main/80-agents/skills/agents-os-agent-run-register/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/skills/agents-os-agent-run-register/SKILL.md) (blob `d0e7662fba8a8b23bd735cf120a2733ed3cb0080`); [main/80-agents/skills/agents-os-session-feedback/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/skills/agents-os-session-feedback/SKILL.md) (blob `8aded0addda1a47afe39e6f675b86bc101577e64`); [main/80-agents/skills/agents-os-session-close/SKILL.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/skills/agents-os-session-close/SKILL.md) (blob `1d1e3681fa7a787a9a7ff47a52ebc6c471c3fe95`).
- **R08 — Contrato y materialización documental.** [main/80-agents/skills/_shared/schema-contract.md](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/skills/_shared/schema-contract.md) (blob `27e59b8b1e9044ded50e5cfef4474c6e3ed59b95`); [main/80-agents/skills/_shared/scripts/materialize_schema_note.py](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/skills/_shared/scripts/materialize_schema_note.py) (blob `067dbef8afca0f3918b1435b83267f547f462bc4`); [main/80-agents/skills/_shared/scripts/validate_schema_contract.py](https://github.com/xKoRx/agents-os/blob/032095c6bbe1c6c5422d758b5540b023a89afd24/main/80-agents/skills/_shared/scripts/validate_schema_contract.py) (blob `7f6e9227ab11f2aac8a1bec135775bbd852d016c`).

Las plantillas canónicas doc, feedback y change_log fueron materializadas con el script publicado de R08. No se copió metadata de otra entidad. Las fechas documentales usan 2026-10-28, corroborada por reloj UTC.

Los enlaces de bootstrap fijados al SHA Agents-OS recuperado corresponden a los mismos blobs observados al arranque. No se incluyen logs pesados, prompts, transcripciones ni supuestas pruebas físicas. El retorno final añade el commit de esta entrega; el documento no pretende incluir recursivamente su propio hash.

### 25. Fuentes y disposición C03

- [[EF-CAMPAIGN-MODES-REVIEW]]: F01–F03 adoptados como reparación; C02 permanece intacto en commit `844e777f95e01e5268f8f7cd98de5299765ce0f2`.
- [[EF-S04-INTEGRATION-RECONCILIATION]]: source, catálogo exacto, S04-F01/F02, extractos y hashes; no certificación física.
- [[EF-CAMPAIGN-MODES-I0-LOCAL]]: único paquete activo I0-S1; I0-S2/S3 preparados y no ejecutados.
- Owner, mensaje de continuidad: «todo converge aquí, campañas… diseña y comencemos la implementación»; autoriza comenzar el desarrollo acotado, no gasto, campañas ni cambio de gates.
- Dos apoyos CLOUD ONE-SHOT de lectura/revisión aportaron evidencia separada de S04 y economía; el manager verificó los archivos decisivos y adjudicó el delta. Independencia física: NOT_EXECUTED; independencia histórica: UNKNOWN; PRO_CHAT_POOL_DELTA: UNKNOWN. No se modifica cuota por inferencia.
- Manager y programa permanecen abiertos; C03 no ejecuta session-close del coordinador.

