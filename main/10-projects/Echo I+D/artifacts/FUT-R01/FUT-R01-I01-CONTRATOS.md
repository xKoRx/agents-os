# FUT-R01 — I01-B: contrato Rapid EOD 50K, caja finita y dos MM comparables

**Estado de entrega:** \`PARTIAL_DOCUMENTAL / BLOCKED_EXECUTABLE\` · **Fecha de consulta:** 2026-10-28 (America/Santiago) · **Responsable de aceptación:** manager Echo I+D — Futures / Owner · **Intervenciones físicas:** ninguna · **G0–G5:** sin cambios, NOT_EXECUTED.

**Autoridad y corte:** xKoRx/agents-os, rama \`master\`, \`main/AGENTS.md\`; [[Echo I+D — Futures]], [[FUT-R01-ITERACION-01]], [[FUT-R01-RV-01-CONSOLIDADO]] §§5,7,9,10, [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]] y DR-02 del mandato v4. Se verificó que \`FUT-R01-I01-SPEC.md\` no estaba presente en master al preparar este informe. S04→master sigue siendo integración informada por Owner, no una certificación realizada aquí. \`I01-C\` histórico read-only no es el nuevo frente C de campañas.

> **Alcance y límite:** candidato **My Funded Futures / Rapid EOD / 50K** exclusivamente documental, NO firma elegida, compra, autorización operativa ni RuleSet certificado. El saldo nominal USD 50.000 no financia la negociación desde los USD 4.000: estos últimos son exclusivamente bankroll externo de compras y cargos efectivamente financiables, sin aportes y sin respaldo Forex. Una Strategy NQ de tres bloques y su geometría técnica se mantienen idénticas entre MM. No se ejecutaron pruebas, simulaciones, backtests ni inspección de Echo, Hefesto o servidores.

## 1. Dictamen y refutadores

**Resultado:** el perfil comercial es suficientemente identificable para preparar la contabilidad y la interfaz de dos MM, pero **no es elegible para ejecución certificada**: falta la ruta exacta y permitida de órdenes Echo→bridge/API→plataforma→cuenta por etapa, y quedan ambiguos el enforcement del DD, el saldo debitado en payout, los costes obligatorios de ruta/transferencia, la cohorte contractual y un conflicto de límite funded. Las fuentes oficiales [S01–S12] corresponden a páginas consultadas el 28-10-2026; la fecha mostrada por el sitio no equivale a vigencia garantizada de un contrato individual.

**Incompatibilidad documentada:** este programa permite como máximo **3 SIM funded Rapid EOD 50K simultáneas**, aunque el límite general entre cuentas 25K/50K pudiera ser 5 [S02]. Por lo tanto, la meta Owner de 5 funded simultáneas **no se puede cubrir íntegramente con esta única combinación**. No invalida estudiar una cuenta candidata ni descarta la meta con dos firmas distintas.

**Contradicción documental oficial:** el Help Center específico fija **3 NQ / 30 MNQ** en SIM funded [S01]; una tabla de marketing del mismo proveedor presenta **4 minis / 40 micros** en una fila de funded 50K [S12]. No se promueve 4 como permiso, ni se disimula la divergencia: \`RULE_CONFLICT\` y confirmación de condiciones efectivas por cohorte antes de congelar límites. NQ es el único instrumento del encargo; MNQ figura en fuentes sólo como equivalencia comercial, no como reemplazo permitido por el Owner.

**Otros refutadores/paradas:** una prohibición contractual concreta del origen real de órdenes o del patrón elegido vuelve \`INCOMPATIBLE\` esa ruta; un dato esencial ausente produce \`UNKNOWN\`, no permiso; si la transición a live suspende SIM y nuevas compras, la simulación debe cambiar de estado y no prolongar ficticiamente la SIM [S03]. No se buscará otra firma para rescatar esta entrega.

## 2. Vector de identidad por fase, plataforma y cohorte

| Vector | Estado inicial / identidad | Estado documental |
|---|---|---|
| \`MFFU / Rapid EOD / 50K / EVALUATION / Tradovate / NEW-2026-10-28\` | Cuenta de evaluación nominal 50K; precio y términos de contratación por confirmar al checkout; Tradovate figura entre plataformas soportadas [S10]. | \`CONDITIONED\` — no API/bridge Echo certificado. |
| \`MFFU / Rapid EOD / 50K / SIM_FUNDED / Tradovate / PASS_FROM_EVAL\` | Inicio contable funded de **USD 0 de PnL relativo** después de pase/revisión/upgrade, no cuenta bancaria con 50K [S01,S02]. | \`CONDITIONED\` — límite 3 funded y conflicto de máximo de contratos. |
| \`MFFU / Rapid EOD / 50K / LIVE / PLATFORM_UNKNOWN / TRANSITION_DATE_UNKNOWN\` | Transición discrecional o por disparador contractual; al iniciar live saldo relativo USD 0 y reglas distintas [S03]. | \`CONDITIONED\` — nueva plataforma/cuenta, origen y obligaciones no acreditados. |
| Cohortes anteriores / promos / otros tamaños / Rapid estándar | No extrapolar retrospectivamente; Rapid estándar usa otra consistencia, días mínimos y DD intradía en funded. | \`EXCLUDED\` para esta ficha. |

\`NEW-2026-10-28\` identifica una **cohorte prospectiva hipotética**, no una compra realizada. Cada futuro intento necesita fecha de compra, modalidad comercial efectiva, URL/términos aceptados, plataforma, ID de cuenta, ID de compra, ID de reset/renovación, versión de reglas y fechas de modificación. No se presupone que el precio promocional esté vigente cuando ocurra la compra.

## 3. Matriz contractual por fase — fuente, estado e impacto

| Campo | EVALUATION — Rapid EOD 50K | SIM_FUNDED — Rapid EOD 50K | LIVE — Rapid 50K | Estado / fuente y efecto |
|---|---|---|---|---|
| Objetivo/resultado | Target +USD 3.000; pase sujeto a revisión y requisitos. | Sin target equivalente para “pasar”; producir solicitudes/cobros elegibles. | Operativa live y cobros según reglas live. | \`RESUELTO\` base [S01,S02,S03]. |
| Balance reportado | Nominal 50K con PnL de evaluación; no bankroll. | PnL inicial relativo USD 0, no depósito real de 50K al operador. | Balance relativo inicial USD 0. | \`RESUELTO\` distinción [S01,S03]; composición exacta balance/equity ante DD \`UNKNOWN\`. |
| Max DD y actualización | MLL USD 2.000 EOD; evaluar su HWM, floor y lock según términos exactos. | MLL USD 2.000; suelo móvil actualiza al nuevo máximo **de cierre diario**, nunca baja; al alcanzar +USD 100 se bloquea [S01]. | MLL USD 2.000 EOD; suelo se bloquea en USD 0 [S03]. | \`RESUELTO\` frecuencia/base cualitativa; \`UNKNOWN\` instante de enforcement intradía, mark utilizado, igualdad/toque, costes, liquidación y pending orders. **EOD de actualización no demuestra enforcement sólo EOD.** |
| Daily loss limit | Ninguno separado. | Ninguno separado. | No se encontró afirmación inequívoca en las fuentes incluidas. | \`RESUELTO\` Eval/SIM [S01]; Live \`UNKNOWN\`. |
| Consistencia / días | 30% del beneficio total atribuible como máximo a un día; mínimo **4 días operados**. Reglas de igualdad/día ganador aún pendientes. | Sin regla de consistencia para payout; calendario desde primer trade y nuevos beneficios. | Live sin regla específica verificada aquí. | \`RESUELTO\` Eval/SIM [S01,S04]; detalle de cálculo \`UNKNOWN\`. |
| Noticias Tier 1 | Permitidas en evaluación según plan específico. | Prohibidas. Franja exacta, órdenes existentes y clasificación de evento \`UNKNOWN\`. | No extrapolar permiso de SIM ni evaluación. | \`RESUELTO\` prohibición por fase [S01]; precisión \`UNKNOWN\`; Fair Play mantiene restricciones amplias [S05]. |
| Horario y cierre | Fuente expresa 18:00 EST apertura Globex y liquidación automática 16:10 EST en sesiones ordinarias; en feriados no confiar en auto-liquidación [S06]. | Mismo horario general documentado por firma, salvo anexo de fase. | Horario general con excepción live que requiere corroboración por cohorte. | \`RESUELTO\` regla general; \`UNKNOWN\` manejo DST de la etiqueta “EST”, calendarios y notificaciones de feriados. |
| Contratos, escalado | Hasta 3 mini / 30 micros según plan [S01]; NQ entero 1–3 dentro de esta investigación. | Help Center: 3 mini / 30 micro; marketing: 4 mini / 40 micro. | 3 mini / 30 micro [S03]. | \`RULE_CONFLICT\` funded; límites **provisionales** más restrictivos a efectos documentales, no certificados [S01,S12]. Escalado intrafase no documentado. |
| Inactividad | 7 días (unidad de calendario y excepción \`UNKNOWN\`). | 7 días (unidad y enforcement \`UNKNOWN\`). | No extrapolar regla. | \`RESUELTO\` cifra Eval/SIM [S01]; detalles \`UNKNOWN\`. |
| Simultaneidad | Máximo general 10 evaluaciones activas [S02]. | Límite específico 3 Rapid EOD 50K [S02]. | Live unifica parámetros de múltiples Rapid convertidas y detiene SIM/compras [S03]. | \`RESUELTO\` restricción explícita; no implica autorización de 5 funded en esta firma. |
| Conductas | HFT y explotación del simulador prohibidos; uso automatizado propio permitido condicionado; hedge de direcciones opuestas sobre NQ/MNQ prohibido [S05]. | Idem; noticias T1 prohibidas [S01,S05]. | Bots sujetos además a reglas CME; nuevas condiciones de cuenta [S05,S03]. | \`RESUELTO\` marco de conducta; definición granular de “HFT”, “gaming” o políticas de riesgo extremo \`UNKNOWN\`. |

**Enforcement — regla para el futuro simulador:** separar \`EOD_HWM_UPDATE\`, \`BREACH_CHECK\`, \`FORCED_FLATTEN\`, \`BREACH_FINAL\` y tratamiento de órdenes pendientes. El suelo teórico de SIM puede representarse como \`floor_eod=min(+100, HWM_eod−2000)\` sólo como **operacionalización a validar**, no regla completa de ejecución; además debe determinarse qué variable (balance, equity, realización) se compara con ese suelo y cuándo. Los gaps/slippage pueden producir overshoot y no se inventa un fill en el límite.

## 4. Origen de órdenes y autorización por fase

\`Strategy NQ determinista [I01-A]\` → \`generador de señal/proceso Echo (ubicación UNKNOWN)\` → \`propietario y ubicación de órdenes/cancelaciones UNKNOWN\` → \`bridge/API autenticado UNKNOWN\` → \`Tradovate / NinjaTrader / TradingView disponibles como plataformas nombradas, pero ruta exacta no elegida [S10]\` → \`cuenta MFFU de fase determinada\`.

- **Automatización propia:** MFFU permite algoritmos propios adaptados a configuraciones del trader, salvo HFT, explotación de fills simulados, brackets deliberadamente abusivos y prácticas prohibidas [S05]. Esto NO autoriza cualquier bridge, VPS, cloud origin o identidad de credenciales.
- **Copy trading:** MFFU documenta copy trading entre cuentas de la firma, Tradovate group copier y herramientas externas; la responsabilidad contractual permanece en el trader [S07]. Su política prohíbe copiar **a otro trader** y la colaboración para estrategias idénticas/opuestas entre cuentas no relacionadas [S05]. Autorización multi-prop cross-firm, identidad del titular y tratamiento hedge \`UNKNOWN\`; no convertir “copia permitida” en permiso cruzado universal.
- **Integración API:** [S10] acredita conexión de plataformas y aceptación de acuerdo de datos, **no API programática de una cuenta MFFU** ni alta de claves, permisos de órdenes, servidor que las origina o continuidad en live. Por tanto la ruta Echo es \`UNKNOWN\`, **no \`COMPATIBLE\` ni \`INCOMPATIBLE\` todavía**.
- **Live:** [S03] dispone que al transicionar una Rapid SIM pasa a \`DORMANT\`, se suspenden otras cuentas SIM y nuevas compras mientras opere live, y varias Rapid pueden consolidarse en una sola live. Un bridge SIM no acredita bridge live. Es una transición terminal obligatoria de esa trayectoria SIM, con contratos nuevos o continuidad verificable.
- **TopstepX:** antecedente de ruta de RV-01 únicamente. No corresponde transferir esa prohibición específica al proveedor MFFU ni rediseñar Echo en este I01-B.
- **Elegibilidad/KYC:** primer payout exige verificación KYC y medio de recepción Riseworks [S09]. Residencia/país del titular, cuentas familiares y la aceptación contractual real de una ruta por etapa quedan \`UNKNOWN\`; sin contacto externo en este mandato.

## 5. Costes por evento y fuente de financiación

| Evento | Importe/documentación para Rapid EOD 50K | Base económica, lugar del cargo y vigencia |
|---|---|---|
| Compra \`PURCHASE\` | Web comercial muestra **USD 135 promocional** / **USD 225 referencia sin promoción** en vista 50K [S11]; **no precio confirmado de checkout**. | Externo al bankroll en fecha de pago. Registrar total realmente debitado, impuesto/FX si corresponde y cohorte; condiciones/promoción cambian. |
| Reset \`RESET\` | \`UNKNOWN\` coste, disponibilidad, nueva identidad e impacto sobre la cohorte. | Pago sólo si realizado; puede crear nuevo intento vinculado a compra anterior. No inventar USD 0. |
| Renovación \`RENEWAL\` | Comercial Rapid EOD afirma compra única sin renovación [S12]; alcance efectivo y acuerdos legacy no confirmados. | No crear cargos mensuales ficticios; registrar explícitamente valor \`0\` sólo si la contratación concreta confirma modalidad de un pago. |
| Activación \`ACTIVATION\` | **USD 0** para Rapid EOD [S01,S12]. | Evento de transición con coste 0, contabilizado exactamente una vez. |
| Market data / plataforma | Requiere acuerdo de datos para activar acceso en plataformas [S10]; cargos propios aplicables \`UNKNOWN\`. | Si se paga desde bankroll, gasto externo real; si incluido o bonificado, sin débito adicional. |
| API / bridge / copier / operación | Permiso y tarifario particular \`UNKNOWN\`; que Tradesyncer sea preferido no implica que sea gratuito [S07]. | No declarar financiable una ruta con coste obligatorio sin fuente ni monto; no añadir una plataforma imaginaria. |
| NQ comisiones | **USD 4,68 round trip por NQ**, tick 0,25 = USD 5, luego USD 20 por punto, según lista MFFU [S08]. | Coste transaccional que afecta PnL de evaluación/SIM si está incluido; **no restar nuevamente del bankroll** si ya llegó neteado. Slippage no está incluido como certeza. |
| Solicitud/transferencia/FX | Split SIM 90/10 [S01]; costo de Riseworks, banco, cripto, FX/impuestos \`UNKNOWN\` [S09]. | Restar una vez desde efectivo recibido o desde débito externo según factura real, nunca ambos. |
| Live / reserva / costes adicionales | Nueva cuenta y hasta USD 5.000 de beneficios SIM asignables a \`Reserve\` [S03], no equivalentes a desembolso propio. Comisiones/fees live \`UNKNOWN\`. | Reserva contractual ≠ cash recibido. No inventar financiación ni continuidad de caja. |

**Lectura del objetivo histórico Owner de USD 400/funded:** tres compras a USD 135, dos fallidas y una pasada, sumarían **USD 405** de adquisición **únicamente como aritmética condicional**, sin resets ni otros costes y sin probabilidades estimadas. Una sola trayectoria ganadora costaría USD 135; la adquisición de una funded **agregada** debe cargar todas las compras fallidas de la cohorte, no sólo esa trayectoria. El ratio 1/3 Owner no es medición de esta firma ni valida el ejemplo.

## 6. Payout — máquina de estados e incertidumbre que altera cash

**SIM RAPID EOD 50K [S01,S04,S09]:** beneficios realizados acumulados al menos USD 2.100 para habilitar primer payout, primera elegibilidad no antes de 24 horas desde primer trade según política general Rapid; ninguna consistencia funded; frecuencia diaria; mínimo solicitado USD 500; unlock posterior cuando beneficio neto desde último pago llegue a USD 500; split 90% trader / 10% firma; sin máximo por solicitud publicado en artículo específico. “No cap por solicitud” no significa cobros ilimitados ni duración SIM ilimitada: transición live automática/discrecional puede cortarla [S03].

**Estados distintos, con timestamps:** \`PROFIT_REALIZED\` → \`ELIGIBLE\` → \`REQUESTED\` → \`UNDER_REVIEW\` → \`APPROVED / REJECTED\` → \`PROVIDER_SENT\` → \`TRANSFER_PENDING\` → \`CASH_RECEIVED_USABLE\`. Requiere KYC, Riseworks, acuerdos de primer pago y transferencia [S09]. Una página anuncia aprobación casi inmediata o 6–12 horas hábiles si requiere revisión [S04], otra describe un procesamiento de 6–12 horas hábiles [S09]; **no hay promesa verificable de plazo hasta abono efectivo**, menos aún en banco chileno.

Para solicitud bruta contractual \`A\` que sea efectivamente admitida, el neto **antes de cargos de transferencia y FX** es \`0,90×A\`. Ejemplo unitario, sin fijar objetivo: \`A=USD 500\` ⇒ \`USD 450\` antes de otros cargos, una vez recibido. La política de retiro aún debe resolver **monto que puede solicitarse tras el buffer, si éste debe permanecer, monto debitado de balance (A vs neto), saldo posterior, si pago afecta el lock y eventos de revisión**. Ni \`A=PnL−2100\` ni \`A=PnL−100\` se adoptan como fórmula contractual sin evidencia. La cota de mantenimiento de +USD 100 no resuelve por sí sola la retención permitida.

**LIVE [S03]:** transición automática al lograr USD 10.000 de beneficio neto en un solo día o discrecional por Risk Team; exceso sobre USD 10.000 de esa sesión se pierde según el documento, hasta USD 5.000 de SIM se asignan a Reserve y el resto puede quedar elegible para retirada sujeto a protocolos. Se suspende SIM y nueva compra durante live. La cuenta live inicia USD 0 relativo, MLL 2.000 EOD con suelo bloqueado en 0, hasta 3 NQ, split 90/10 y frecuencia diaria; sin buffer live en la página. No prolongar la secuencia SIM más allá del evento efectivo de transición. El Reserve no entra en bankroll hasta una entrega real admisible.

**Política de retiro — escenarios, NO decisión:** primer mínimo elegible; solicitud parcial que preserve capacidad de cobros posteriores; solicitud mayor dentro de \`A_max\` acreditado; secuencia de solicitudes y pérdida posterior; salto a live. Horizonte, demora, costes, política seleccionada y post-balance se registran por separado. USD 3.000 como meta fija ha sido superseded.

## 7. Ledger del bankroll — contrato común CHALLENGE/FUNDED/SIMULATION

Para cada evento único y fecha:
\`B(t)=USD 4.000 + Σ CASH_RECEIVED_USABLE_NET(t) − Σ OUTLAY_EXTERNAL_PAID(t)\`.

- \`CASH_RECEIVED_USABLE_NET\`: sólo cobro **neto ya disponible para financiar compras**, luego de split y cargos efectivamente detraídos; no sumar dos veces un cobro que pasa de Riseworks a banco. Solicitud, aprobación, transferencia pendiente, PnL SIM y Reserve se informan en un registro aparte.
- \`OUTLAY_EXTERNAL_PAID\`: compra, reset, renovación si aplica, activación, plataformas, datos, API, copiloto, operación o transferencia **sólo cuando se paguen externamente**. El registro conserva destinatario, ID único del evento, moneda, FX observado, fecha/estado y su relación con cuenta/compra. Si el coste ya redujo el PnL nominal o el neto recibido, no debitarlo aquí nuevamente.
- \`OBLIGATIONS_PENDING\` y \`CASH_COMMITTED\` son saldos separados para calcular caja libre; no se restan prematuramente de \`B(t)\` y tampoco se ignoran al admitir una nueva compra.
- \`PROPFIRM_PNL\` permanece separado: la quema de un challenge/funded **no resta de nuevo USD 2.000 del bankroll**; su pérdida económica ya comprende los pagos externos necesarios, salvo nuevo cargo contractual real.
- **Invariante de admisión de compra:** no adquirir/activar/resetear cuando el importe efectivamente exigible no puede pagarse con \`B(t)\` libre y sin aportes. Con cargos obligatorios \`UNKNOWN\`, escenario marcado \`NOT_FULLY_FINANCEABLE\`, no “USD 0 por defecto”.
- **Idempotencia documental:** cada compra, reset, comisión externamente pagada y cobro usa ID de evento/recibo; un retry de simulación no duplica flujos. Sin mezclar cohorte por precio, regla, contrato, plataforma, fecha o fase.

**Dos vistas de coste no intercambiables:**
1. \`winning_path_cost\` = cargos externos efectivamente ligados a la compra/intento que llegó a pase/activación, sin imputarle otros fallos; descriptivo de una trayectoria.
2. \`aggregate_acquisition_cost_per_activated\` = costes de **toda la cohorte** de compras, intentos, resets y activaciones atribuibles / funded efectivamente iniciadas, también fallidos y pendientes; N=0 ⇒ N/A, no cero.
3. \`cost_per_paying\` = adquisición y costes externos atribuibles totales / cuentas que **recibieron cash** a H, con la cohorte y exclusiones explícitas. N=0 ⇒ N/A.

Se conservarán vistas de **intentos iniciados**, **evaluaciones comerciales compradas**, **pases**, **funded activadas**, **funded quemadas**, **pagadoras únicas** y **pagos recibidos**. Una cuenta con dos cobros y pérdida posterior suma una funded iniciada, una pagadora, dos pagos y una pérdida; la funded sin pagos permanece en el denominador. Se reportan escenarios de horizonte por inicio de cohorte y fecha de corte, con pendientes/censura; no se atribuye a todas el mismo seguimiento si compraron en fechas distintas.

## 8. Dos MM candidatos comparables — NO congelados

**Precondición externa compartida:** una sola \`StrategyID + VariantID + ConfigID\` (setup, filtro, stop/objetivo técnicos y salida temporal fijados por I01-A), NQ puro; las mismas oportunidades exógenas y datos/calendarios, pero **cuentas y estados independientes**. No se multiplica una curva cerrada por contratos para inferir vetos, slippage, payouts o resultados. \`I01-SPEC\` ausente, por tanto ninguna política queda \`FINAL\`.

El riesgo técnico de una unidad NQ de stop conocido es \`r_1 = d_ticks×USD 5 + USD 4,68 roundtrip + slippage_modelado\`; equivalente \`d_puntos×USD 20\` antes de costes. El stop y objetivo en ticks los fija Strategy, **nunca MM**. Para \`q\` contratos enteros: \`r_q\` debe incorporar tamaños, comisiones, slippage, posiciones simultáneas y coste de liquidación; un stop presupuestado no garantiza una pérdida máxima ante gap. La referencia es **headroom de DD prop por etapa**, no 1%/2% de USD 4.000 ni porcentaje del nominal 50K.

| Parámetro | \`MM-CTRL-NQ\` — control de mínimo tamaño | \`MM-MAX-NQ\` — exposición contractual alta |
|---|---|---|
| CHALLENGE sizing | \`q=1 NQ\` si cuenta, sesión, contrato y estado admiten; si no, veto. Es control experimental, no nuevo límite prudencial impuesto al resto. | \`q=max entero admisible dentro del máximo contractual de NQ\`, provisionalmente rango 1..3, sujeto a no activar una infracción **ya demostrable** con la información causal del momento. No asumir que q=3 es legal por sí mismo. |
| FUNDED sizing | \`q=1 NQ\` si elegible con DD/saldo/payout/horario actualizados; vetar de lo contrario. | \`q=max entero admisible\` con reevaluación después de PnL, payout, lock y cambio de fase. Conflicto 3 vs 4 queda abierto; no elegir 4 por marketing. |
| Objetivo comparado | Control de menor lote entero para medir pase/primera recepción y supervivencia condicionada. | Acortar potencialmente pase y cobro, a costa de mayor discontinuidad de quema y dependencia del MLL. No se afirma que domine. |
| Salidas Strategy | Exactamente el mismo stop, target y cierre técnico que \`MM-MAX-NQ\`. | Exactamente el mismo stop, target y cierre técnico que \`MM-CTRL-NQ\`. |
| Salidas MM/económicas | Liquidación contractual, protección para no mantener órdenes ilegales, y política de retiro propia aún no seleccionada, **identificadas como razón MM**. | Idem; eventuales salidas económicas adicionales requieren criterio explícito y otra identidad/configuración, sin llamarlas stop de Strategy. |
| Reentrada/continuidad | Oportunidades y límites de la etapa; no inventar límite de trades al día, rescate, reserva ni porcentaje por costumbre. | Idem; consumir riesgo disponible puede quemar cuenta rápido; no abrir cuando el contrato veta, y no reutilizar estados de otra cuenta. |
| Estado | \`PROPOSED_REQUIREMENTS\`, no aprobado. | \`PROPOSED_REQUIREMENTS\`, no aprobado. |

**Admisión común pendiente de operacionalizar:** \`instrument=NQ\`, calendario/DST, cierre obligado, prohibición noticias por fase, contrato máximo confirmado, máximo de cuentas, no hedge prohibido, posición actual y órdenes vivas, reglas HFT/fills/abuso, inactividad, consistencia/días, DD real y enforcement, disponibilidad de señales, fill y stop; además rastro de \`SIGNAL → VETO_REASON/ORDER → FILL/EXIT\`. Con incertidumbre material de DD/API, no inferir automáticamente permiso de entrada por comparar \`r_q\` con el floor. La política agresiva **no** autoriza incumplir ni convierte pérdida estimada hasta stop en techo garantizado.

**Diseño de comparación causal:** misma serie de oportunidades; ambas ven señales de calendario original, pero cada cuenta aplica su propio estado. Guardar señales sin orden, denegadas, canceladas, fills, comisiones, excursión de mark/equity necesaria, terminal de cuenta y fuente del cierre (Strategy/MM/firm). Validación de geografía del stop e igualdad/overshoot queda con I01-A, datos y owner técnico. El contraste no es 1% vs 2% arbitrario; son extremos enteros definidos por capacidad y reglas efectivas, propuestos para que el Owner juzgue el trade-off, no para certificar óptimo.

## 9. KPI de las tres campañas y decisión económica posterior

| Modo | Denominadores y salidas exigidas | Lo que no puede inferirse |
|---|---|---|
| \`CHALLENGE\` | Compras comerciales, intentos (resets asociados), pases/fallos/pendientes; pase por compra y por intento a H; coste por pase y por funded activada; tiempo a pase o quema; motivo de veto; coste de todos los fallos. Umbral 1/3 es **Owner** y debe fijar denominador/horizonte antes de contrastar. | Probabilidad de pase de la firma, por el nombre de la MM, ni 1/3 observado. |
| \`FUNDED\` | Todas las funded iniciadas, incluso quemadas y sin pago; fracción con primer cobro, \`cash_neto_recibido/N_funded\`, margen posterior a gastos funded (sin recomputar activación), pagos repetidos, primer cobro, pérdida posterior y pendientes por H. | Iniciar funded de la nada no valida adquisición desde evaluaciones. |
| \`SIMULATION\` | Encadenar compras→intentos→pases→activación→operativa funded→solicitud→aprobación→abono→reinvierte; \`B(H)\`, mínimo de caja libre, agotamiento/no poder comprar, tiempo hasta primer efectivo, coste por activada/pagadora, pagos posteriores y obligaciones/cuentas pendientes. | No presuponer independencia de varias cuentas sobre NQ, ni financiarse con PnL de SIM o cobros por aprobar. |

**Selección aún abierta:** horizontes/cortes (p.ej. 30/60 días sólo como escenarios, corte táctico 31-12-2026 sin prometer cumplimiento); priorización de cobro temprano vs caja neta al corte vs riesgo de agotamiento vs ciclos posteriores; importes/tiempos/política de retiro; máximo desembolso comprometible y resets; fuente de financiación de cargos obligatorios. No imponer score, cutoff universal PF/Sharpe o esperanza de trade positiva. Una señal con media por trade no positiva no queda universalmente descartada como campaña, pero tampoco el split contractual garantiza utilidad.

**Ejemplos contables de aceptación futuros, no pruebas corridas:** si 12 intentos externos consumen USD 1.200 y tres pasan, coste por pase USD 400 incluyendo nueve fallos; si una funded recibe dos pagos y después se quema, ambos flujos permanecen y la cuenta no se excluye; un pago aprobado y no disponible no autoriza compra; evento de activación USD 0 se representa una vez; si un payout queda duplicado por retry, el ledger rechaza el doble crédito. Estos son requisitos de una verificación posterior de C01, no ejecución de I01-B.

## 10. Dependencias exactas y preguntas para manager/Owner

| Prioridad | Dependencia y pregunta exacta | Impacto actual |
|---|---|---|
| D1 — \`RULE_CONFLICT\` | ¿Para **Rapid EOD 50K SIM FUNDED** de nueva cohorte 2026, el contrato vinculante admite **3** o **4** NQ, y cuáles son máximo total y reglas de escalado? [S01 vs S12] | No congelar \`q_max\` funded. |
| D2 — \`UNKNOWN\` | ¿Qué **serie de balance/equity/mark y costes**, momento de breach, comparación toca/cruza, liquidación y órdenes pendientes aplica al DD EOD de Eval/SIM/Live? | No modelo causal de quema ni validación de agresividad. |
| D3 — \`UNKNOWN\` | ¿Cuál es el **bridge/API específico autorizado** para cuenta MFFU Rapid EOD por fase, plataforma, origen/dispositivo del proceso que envía/modifica/cancela, credenciales, VPS/cloud y continuidad live? ¿Es el mismo titular en todas las cuentas? | Automatización documental genérica no acredita ejecución de Echo. |
| D4 — \`UNKNOWN\` | ¿Qué reglas exactas determinan \`A_max\`, retención del buffer 2.100, **débito en cuenta tras solicitar/recibir**, lock DD y condiciones de rechazo/abono, incluidos cargos de Riseworks/banco/FX para titular en Chile? | No existe todavía payout neto causal utilizable para optimización. |
| D5 — \`UNKNOWN\` | ¿Cuánto costará realmente **checkout 50K** en esa cohorte, reset, datos, API/copy, transferencia y cualquier cargo obligatorio? ¿Existen excepciones por plataforma/plan/contrato firmado? | No declarar financiable una cadena con USD 4.000 sin los costos vinculantes. |
| D6 — \`UNKNOWN\` | ¿Qué franja exacta restringe noticias T1 en SIM, qué criterio de “7 días” de inactividad y qué interpretaciones HFT/riesgo extremo afectan la Strategy y la MM? ¿Qué horario ET/DST oficial aplica cada sesión y feriado? | Regla de admisión incompleta; no presumir permiso por silencio. |
| D7 — \`DEPENDENCY_I01_A\` | ¿Cuál es la ficha I01-A única de señal, stop/objetivo y salida temporal, con datos y precedencia causal? | Dos MM quedan propuestas, sin parametrización ejecutable. |
| D8 — \`OWNER_DECISION\` | ¿Qué horizontes, prioridad de caja/rapidez/agostamiento, política de compras/resets y pérdidas comprometibles se usarán en la comparación **después de completar requisitos**? | No adjudicar una política ganadora ni escoger retiro por conjetura. |
| D9 — \`COORDINATION\` | ¿Cuál es el corte S04 efectivamente aceptado y quién resolverá recepción de A/B y diseño C01 sin writers concurrentes? | I01-B no interviene runtime ni altera G0–G5. |
| D10 — \`UNKNOWN\` | ¿Está admitido el **titular y su medio de retiro** bajo términos vigentes y existe un contrato de SIM→live que mantenga el origen de órdenes y la estrategia elegidos? | No declarar compra ni continuidad live aptas. |

**Estado de admisibilidad:** \`DOCUMENTAL_CONDITIONED\`, con al menos D1–D5 indispensables antes de un RuleSet y valoración de caja aceptables. **Integración física:** \`NOT_INSPECTED / NOT_CERTIFIED\`. **Alternativa LucidFlex 50K:** no ampliada: la cuota de fuentes se destinó a la fase primaria y subsisten bloqueos materiales. El cap histórico RV-01 (USD 2.000 de solicitud / 90% split) es antecedente, no nuevo perfil verificado. **DR-05:** no abierto. **Method delta:** \`NO_DELTA\`.

## 11. Registro de doce páginas oficiales decisivas

Todos los URL siguientes son **del emisor del programa**, consultados el **2026-10-28**. Se preserva fecha visible en la página; “sin fecha” significa que no fue posible establecer una fecha de publicación desde la página consultada. No equivalen a aceptación de términos por una cuenta real.

| ID | Fuente oficial, URL y fecha visible | Alcance aportado |
|---|---|---|
| S01 | [Rapid EOD 50K — A Comprehensive Look](https://help.myfundedfutures.com/en/articles/16158363-rapid-eod-50k-a-comprehensive-look) — 2026-08-24 | Target, DD, consistencia, news, 3 minis, buffer, split, live link y funded inicial 0. |
| S02 | [Moving from Evaluation to Sim-Funded](https://help.myfundedfutures.com/en/articles/16498635-moving-from-evaluation-to-sim-funded-account) — 2026-09-04 | Revisión/upgrade, límites 10 evaluaciones/3 Rapid EOD funded y cuenta SIM. |
| S03 | [Understanding Rapid Live](https://help.myfundedfutures.com/en/articles/13134718-understanding-rapid-live) — 2026-09-08 | Gatillos, reserva, transferencia, suspensión SIM/compras, consolidación y parámetros live. |
| S04 | [Payout Policy Overview](https://help.myfundedfutures.com/en/articles/13745661-payout-policy-overview-best-and-fastest-prop-firm-payouts) — 2026-08-25 | Primera elegibilidad 24 h, buffer, mínimo, aprobación y revisión. |
| S05 | [Fair Play and Prohibited Trading Practices](https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices) — 2026-08-24 | Automatización condicionada, HFT, fills, no hedging, no copiar terceros. |
| S06 | [Permitted Times to Trade](https://help.myfundedfutures.com/en/articles/9558251-permitted-times-to-trade) — 2026-08-24 | Horarios, autoliquidación diaria y excepción de feriados. |
| S07 | [Copy Trading at MyFundedFutures](https://help.myfundedfutures.com/en/articles/10771500-copy-trading-at-myfundedfutures) — 2026-08-24 | Copia bajo responsabilidad, plataformas y servicios terceros. |
| S08 | [Futures Instrument List](https://help.myfundedfutures.com/en/articles/9735811-futures-instrument-list) — 2026-08-24 | Tick/valor de NQ y comisión total roundtrip. |
| S09 | [Guide to Your First Payout](https://help.myfundedfutures.com/en/articles/11542406-guide-to-your-first-payout-quick-and-easy-process) — 2026-08-26 | KYC, Riseworks, acuerdos, aprobación y transferencia. |
| S10 | [Connecting to Different Platforms at MFFU](https://help.myfundedfutures.com/en/articles/8528337-connecting-to-different-platforms-at-mffu) — 2026-08-24 | Plataformas soportadas/acuerdo de market data, NO API Echo. |
| S11 | [MyFundedFutures — selector de planes 50K](https://myfundedfutures.com/) — sin fecha de publicación | Precio comercial mostrado USD 135 promo / USD 225 sin descuento, no checkout firmado. |
| S12 | [Rapid EOD Plan — marketing y tabla de reglas](https://marketing.myfundedfutures.com/plans/rapid-eod) — comparación comercial fechada 2026-07-31; actualización de página no informada | Compra única/activación 0 y discrepancia oficial de 4 minis funded 50K frente a Help Center 3. |

**Retorno para el manager:** \`I01-B | PARTIAL_DOCUMENTAL | MFFU/Rapid EOD/50K con Eval/SIM/Live separados | DD/Payout/fees con UNKNOWN explícitos | 3 funded máximo: incompatibilidad con 5 en una firma | ruta Echo UNKNOWN | MM-CTRL-NQ vs MM-MAX-NQ propuestos sin congelar | caja B(t) y métricas por cohorte definidos | I01-SPEC ausente | sin alternativa nueva | no ejecución ni selección | pendiente Owner y confirmación contractual\`.