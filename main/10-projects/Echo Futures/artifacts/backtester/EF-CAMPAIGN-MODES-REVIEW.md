---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
related:
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---

# EF-CAMPAIGN-MODES-REVIEW

## Propósito

Revisión documental independiente C02 del diseño candidato [[EF-CAMPAIGN-MODES-DESIGN]] frente al mandato [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]], sus decisiones Owner y el baseline Platform/S04. No se edita el diseño autor ni se ejecuta producto.

**DICTAMEN: FINDINGS. OWNER_ACCEPTANCE: REVIEW. VERIFICATION: NOT_EXECUTED. ROLE: TOP. SURFACE: CLOUD. WORK FUNCTION: revisor documental adversarial. CURRENT_TASK_STATE: REVIEW. Fecha 2026-10-28.**

**Admisión: DESPACHADO.** C01 existe y está publicado en agents-os/master, blob eea8f96b6eba02309990d30d06d9825d0ebe43c7, commit 8c79805ef5a558369f83fd6f55c82835d7e778ad. No se redacta sustituto ni se acepta C01 automáticamente.

## Contenido

### 1. Conclusión ejecutiva

El diseño C01 conserva la economía Owner y propone correctamente la medición por CHALLENGE y FUNDED separados, la composición SIMULATION con USD 4.000 y una caja, la reinversión exclusiva de cobros netos recibidos, MM por etapa, NQ, cero aportes y la admisión G0–G5 sin relajaciones. No exige esperanza por trade positiva ni impone preservación prudencial de cada cuenta. E1–E4 concilian aritméticamente como casos hipotéticos, no como backtests.

**FINDINGS se justifica por F01 y F02 (P1) y F03 (P2).** F01 es contradicción de cardinalidad/denominador ante compra cobrada no provisionada. F02 es ausencia de un KPI longitudinal obligatorio para verificar el objetivo de primer retiro por compra. F03 acopla innecesariamente FUNDED aislada a la implementación CHALLENGE. Son correcciones del contrato/plan; no requieren otro motor.

D01–D06 de C01 siguen pendientes en su alcance declarado. El conflicto G4 para FUNDED está expresado como decisión Owner, NO como excepción ya autorizada. El master Echo observado aún carece de los modos S04; esa incertidumbre está bien reconocida y afecta implementación, no la posibilidad de revisar el diseño.

### 2. Evidencia, límites e independencia

- C01 diseño: commit [8c79805ef5a558369f83fd6f55c82835d7e778ad](https://github.com/xKoRx/agents-os/commit/8c79805ef5a558369f83fd6f55c82835d7e778ad); §§4–21, E1–E5, V01–V24; autoría reportada GOD/CLOUD. Se comprobó el contenido publicado.
- Mandato obligatorio FUT-R01: blob 479806d5c742b7b19693dc69dc4ed2d5a0b1df22, incluidos Owner, prioridades, KPI y C02.
- **Seis fuentes internas decisivas adicionales**: S01 [[Echo I+D — Futures]] (blob 1eb3b808dc37eff5f091ccb6ba73fbbe38a09e6c); S02 [[Echo Futures — Optimización de Campañas]] (b7aa3010c58c568c183e4147ee2ca3dc1ae192c8); S03 [[echo-futures-strategy-qualification-runbook]] (5b40ec8ae69c195ffd84d85a046cc835031eeccb); S04 Echo S04 v3/backtester/platform_campaign.go (862263302b0172f070c226c0e5e942c18a960832); S05 Echo master v3/backtester/platform_campaign.go (24a86ff8fd23825ec1ec597e90e698f7b7ede620); S06 Echo master v3/backtester/platform_profile.go (b60daa689839bc6d04e83d3333d208b2cda68c31).
- Se cargaron como *routing/procedimiento*, fuera del presupuesto investigativo de seis, main/AGENTS.md, bootstrap/constitución, technical-project-manager, SDD, retester, I+D cycle, feedback y session-close. No se hizo investigación externa ni acceso a hosts.
- Echo/master inspeccionado: 347eee8bdab7f7628629af6383d1e45520815abd. Corte S04 de referencia: ae1b09bc10370806f7648f076c5fa0825c9efa4e. Un símbolo en S04 no prueba que el master, binario o tests de integración estén certificados.
- **Independencia:** tarea C02 y revisión lógica separadas del documento C01, sin edición ni coautoría sobre ese archivo en esta sesión. No hay recibo independiente que pruebe la identidad/modelo efectivos del autor original o que descarte influencias históricas comunes. Contexto fresco no prueba independencia histórica. GitHub atribuye publicación a una identidad de cuenta, no la autoría intelectual del texto. INDEPENDENCE_HISTORY: UNKNOWN.

### 3. Hallazgos demostrados (esperado / defecto / impacto / reparación mínima)

#### F01 — P1 / contradicción de denominador para compra cobrada sin derecho confirmado

**Soporte:** C01 §5.1 exige cargo **y** derecho confirmados para que una unidad pase a «comprada», pero afirma que un cargo debitado sin cuenta utilizable y cuyo derecho/refund sigue pendiente no desaparece del denominador de compras. §5.2 define U como unidades adquiridas y P_U/U como KPI principal del 1/3.

**Contraejemplo documental:** dos facturas pagadas de USD 100, cada una por un derecho comercial; A ya fue entregado y pasó, B sigue cobrado sin derecho provisionado ni reembolso al corte. P=1, dinero pagado=200, una compra pendiente. **Esperado** si el denominador mide compras efectivamente pagadas: 1/2=50%, gasto 200, costo/pase 200 y B pendiente, no fallida. **Defecto con lectura literal de U como sólo derechos confirmados:** U=1, 1/1=100%, aunque el mismo diseño exige no excluir B de «compras». Si una factura no permite conocer cuántas unidades cubre, el denominador es UNKNOWN y no se adjudica 1/3.

**Impacto:** una prop con problemas de provisión puede aparentar superar el umbral Owner por exclusión de compras cobradas. **Reparación mínima:** modelar cargo/compra pagada, derecho provisionado, solicitud no cobrada, fulfillment pendiente y refund recibido como dimensiones distintas; definir U del 1/3 con D01 o bloquear adjudicación donde falte cardinalidad. Mantener las partidas pagadas en costos y cohortes, sin reclasificar técnica como trading loss. Añadir V25/RC01.

**Clasificación:** contradicción documental demostrada; no se acusa un bug de ejecución observado.

#### F02 — P1 / contrato no obliga a reportar primer payout recibido por unidad comprada

**Soporte:** Owner S01 y FUT-R01 fijan aspiración de al menos una cuenta con retiro por cada diez compradas. C01 define P_U/U, F/U, pagadoras/N, W/N y un linaje causal correcto, pero su tabla KPI y el contrato de salida I0/I3 no exigen explícitamente el ratio longitudinal «compras iniciales con al menos un payout realmente acreditado / todas las compras iniciales de la cohorte».

**Contraejemplo documental:** CHALLENGE aislada compra 10, pasa 3. FUNDED aislada tiene tres seeds estandarizadas; una seed cobra USD 1.000. Sus porcentajes separados son 3/10 y 1/3, pero ninguna funded es descendiente causal de esas diez compras. **Esperado:** conversión compra→primer cobro = UNKNOWN/NO_LINKAGE, no 1/10 probado. En una SIMULATION de compras→funded realmente enlazadas, contar directamente derechos comprados con al menos un primer efectivo recibido antes de Hc, independientemente de pagos repetidos. **Defecto:** se puede completar la tabla propuesta sin informar la métrica que adjudica 1/10.

**Impacto:** etapas reportadas correctamente pero aspiración comercial central no evaluable, o posterior tentación de multiplicar tasas de cohortes distintas. C01 sí prohíbe esa multiplicación; no es el fallo alegado. **Reparación mínima:** especificar KPI causal de primer cobro por adquisición y cash neto por adquisición con fechas, censura, pendientes, origen y denominador declarados. Sólo para SIMULATION real/condicionada; funded exógena no recibe un coste de adquisición inventado. Añadir V26/RC03 al contrato futuro.

**Clasificación:** omisión demostrada del reporte requerido; ningún cálculo físico ha sido declarado fallido.

#### F03 — P2 / plan acopla FUNDED aislada a CHALLENGE sin necesidad explícita

**Soporte:** C01 §16 pone I2 FUNDED + dual como dependiente de I0/I1. S04 ya tiene FUNDED_ONLY con seed que instala contexto funded mediante transición canónica sin compra challenge ni activación simulada. Owner pidió etapas aisladas primero y SIMULATION integrada después.

**Contraejemplo documental:** I0 está listo y S04 reconciliado; I1 se demora por la definición de resets de una prop. Una cohorte FUNDED exógena con snapshot, MM/RuleSet y términos propios puede medir N/W/F_op sin ninguna adquisición de I1. **Esperado:** desarrollo FUNDED aislado sin bloquearse por I1, sujeto a sus propios requisitos de estado, términos, admisión y datos; dual sí depende de ambas etapas; SIMULATION integra posteriormente. **Defecto:** el plan I2 bloquea ambos outcomes como unidad.

**Impacto:** camino crítico artificial que retrasa medición funded. **Reparación mínima:** I2a FUNDED aislada desde I0 + evidencia S04; I2b comparación dual desde I1+I2a. D05 se mantiene obligatorio para histórico funded no admitido; no se crea otra vía de spawn ni motor.

**Clasificación:** defecto de secuenciación/documentación; no bug del producto ni permiso de saltar G4.

### 4. Riesgos y decisiones abiertas (no errores demostrados)

- **R01 / G4 FUNDED — DECISION_REQUIRED:** S03 exige ≥1 CHALLENGE_PASSED en el quarter para G4 histórico; una FUNDED_ONLY seeded no puede fabricar ese pase. C01 D05 correctamente conserva bloqueo y propone revisión por Owner/autoridad de gates. La opción «al menos un payout neto recibido en quarter» puede sesgar por delay/censura, por ejemplo funded activada cerca del fin con crédito legítimo posterior. Definir horizonte/seguimiento y quién acepta la regla antes del histórico. NO es bypass ni bloquea I0 de reporting.
- **R02 / reuso multi-asociación — I4_DEPENDENCY:** S04 Platform selectTurn controla una cuenta seleccionada por turno; ello no acredita simultaneidad de fanout multi-Strategy/multi-prop en una instancia. C01 cita R6 y propone el bridge posterior, pero no tiene aún receipt integrado, owner del seam ni prueba del reloj/caja común. No justificar un segundo engine, scheduler o cola; mantenerlo como dependencia de I4, no adelantarlo a I0.
- **R03 / selección J(Hc) — OWNER_UNSET:** C01 propone descontar una vez obligaciones irrevocables en la selección; eso evita premiar cargos atrasados. Sin D02/D04 (horizonte y cola de liquidación), no puede adjudicarse un «óptimo» por primer cobro o capital final. El riesgo es comparar ventanas disparejas, no un error de la ecuación documentada.
- **R04 / términos comerciales — CONTRACT_UNSET:** E2 asume 80% de split con bruto 1.000/600 como ejemplo explícitamente hipotético. S06 PlatformProfile legacy tiene otra tabla y fees; por tanto no es contradicción contable de E2. Antes de medir una prop específica se requieren versión comercial, split, fees, activación, frecuencia, elegibilidad, máximos y fecha de crédito. Cuatro payouts S04 y constantes 5.000/120 no son defaults autorizados.
- **R05 / tiempo y correlación — TO_VERIFY_LATER:** La propuesta preserva fechas de provisión/pase/activación, señales simultáneas y compra tras crédito efectivo. El batch de dos experimentos aislados no demuestra el resultado conjunto en caja finita. Verificar más adelante mediante el mismo driver y source, sin IID por replicación de cuentas.

### 5. Comprobaciones positivas contra los ejemplos C01

| Aspecto | Resultado de revisión documental |
|---|---|
| E1 compras/resets | 4 derechos, 6 intentos, 2 pases, 3 fallos de intento y 1 pendiente; 4×100+50+20=470, 470/2=235. Correcto para derechos provisionados del ejemplo. |
| E1 activación | Un pase no activado, F=1; adquisición 470+80=550, B=3.450. Activación no se duplica en F_op. Correcto. |
| E2 funded | N=3, una pagadora, dos cobros por 780+460=1.240, F_op=30, promedio bruto de cash por iniciada 413,33..., margen 403,33...; funded quemada tras cobrar sigue pagadora. Correcto. |
| E3 cash real | 4.000+780−200−80−10−100=4.390; antes del crédito B=3.710, aprobación=0 cash, pérdida nominal no se debita de nuevo. Correcto. |
| E4 liquidez | B=150−obligación comprometida 80 deja disponible 70; pagar obligación lleva liquidado a 70 sin restar dos veces. Correcto. |
| Cero pases | Costo unitario N/A con gasto visible, sin infinito ni 0 ficticio. Correcto. |
| Cohortes/seguimiento | C01 separa total, resueltos, maduros y censurados; advierte eventos competitivos e IID. Correcto salvo F01 de provisión. |
| Causalidad | Exógena, derivada de pase y observada no se presentan equivalentes. Simulación no compone ratios independientes. Correcto. |
| Estrategia/MM | Setup, filtro opcional, objetivo/riesgo técnico y MM aislado; no se cambia stop por sizing ni se impone prudencia de cuenta propia. Correcto. |
| Gates | G4 funded identificado como D05; ninguna excepción operativa aplicada. Correcto. |
| Reutilización | Modos existen en S04 pero no en Echo/master inspeccionado. C01 admite esa diferencia y opt-in legacy; no propone segundo motor. Correcto como dependencia. |

### 6. Casos candidatos de regresión para LOCAL (NO EJECUTADOS)

| ID | Escenario | Oráculo esperado |
|---|---|---|
| RC01 | Dos compras pagadas, una entregada/pasada, otra cobrada sin derecho ni refund | Denominador pagado 2 o UNKNOWN según cardinalidad; gasto 200; sin 100% espurio. |
| RC02 | Reset gratis + reset cobrado + renovación + falla técnica + cero pases | Intentos vinculados, costos una vez, fallo técnico no equivale a pérdida, costo/pase N/A. |
| RC03 | CHALLENGE 10/3 y FUNDED 3/1 exógenas; luego linaje real desde compras | q inicial UNKNOWN; q ligado cuenta primeros créditos, no cuentas pagadoras duplicadas. |
| RC04 | Funded cobra dos veces, pierde después, tercero aprobado pero pendiente | N fijo, W sólo recibido, pagadora histórica y cash sin aprobación adelantada. |
| RC05 | Dos props buscan gastar últimos USD 100 al mismo instante | Una compra financiada, compromiso único, attribution suma a cash real. |
| RC06 | Crédito en T+2; compra en T; obligación pendiente y pago posterior | Sin cash anticipado, sin doble resta de reserva. |
| RC07 | Funded activada tarde en quarter y payout posterior por términos | D05 pendiente mantiene guard cerrado; no se inventa pase ni se asume observación completa. |
| RC08 | Reproyección I0 de artefacto legacy sin origen/cargo identificable | UNKNOWN localizado, mismo input byte-intacto, cero launch de motores. |

**Todos son casos sugeridos, no tests ejecutados.** C02 no realizó código, tests, compras, backtests ni visitas a hosts. Las conciliaciones de E1–E4 son sólo razonamiento documental sobre importes ilustrativos.

### 7. Primer incremento: bloqueo y deuda

**I0 contratos + reporting es una opción KISS suficiente, pero su implementación está condicionada** a receipt de integración con SHA aceptado, mapa exacto S04/Platform/lab, archivos/fixtures y verificación del nuevo corte. No usar Echo/master antiguo como baseline por comodidad. **Antes de escribir sus fórmulas, corregir F01; incluir F02 desde el contrato para I3.** F03 se resuelve en el plan sin código. El histórico funded requiere D05 aparte.

**Deuda diferible:** I4 multi-Strategy/multi-prop y bridge R6, optimización/políticas después de datos, liquidación post-Hc, pruebas físicas. No invertir el orden de I0 por esas deudas ni garantizar que la composición ya funciona.

### 8. Siguiente decisión Owner y cierre

1. Devolver el documento C01 al autor para una corrección acotada F01–F03 y luego revisión de su delta, sin cambiar el planner por parte del reviewer.
2. Mantener D01–D04 y D06 explícitas hasta aceptar sus semánticas y contratos. Resolver D05 a través de la autoridad del retester antes de histórico FUNDED/dual afectado, no con un bypass.
3. Pedir al manager de integración el receipt del corte aceptado antes de I0 en producto. No encargar un nuevo frente de integración sin examinar el retorno existente.

**REUSABLE_BEHAVIOR_CANDIDATES:**
- RB01: chequeo documental «cargado vs derecho entregado vs pendiente» antes de ratios de adquisición. Evidencia F01/RC01. Uso futuro: campañas por cohortes con fulfillment diferido. NO_PROMOTED.
- RB02: prueba negativa «ratios marginales de etapas aisladas no son q longitudinal» antes de declarar conversión monetaria. Evidencia F02/RC03. Uso futuro: campañas, embudos de retención/payout. NO_PROMOTED.
No modificar skills, runbooks ni gates. **Agent run: NOT_APPLICABLE** a review de SPEC documental, sin segmento material de revisión formal del código implementado.

**Session feedback:** invocado por fricción real del remote fallback; nota C02 separada, no promoción L3. **Session close:** explícito, sólo esta ONE-SHOT; programa y manager permanecen abiertos; no L0/L1 ni checkpoint interno nuevo. **PRO_CHAT_POOL_DELTA: UNKNOWN** (no inferir por rol/modelo).

## Fuentes

- [C01 diseño en commit de publicación](https://github.com/xKoRx/agents-os/blob/8c79805ef5a558369f83fd6f55c82835d7e778ad/main/10-projects/Echo%20Futures/artifacts/backtester/EF-CAMPAIGN-MODES-DESIGN.md).
- [Mandato FUT-R01](https://github.com/xKoRx/agents-os/blob/8c79805ef5a558369f83fd6f55c82835d7e778ad/main/10-projects/Echo%20I%2BD/artifacts/FUT-R01/FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION.md).
- [S01 I+D Futures](https://github.com/xKoRx/agents-os/blob/8c79805ef5a558369f83fd6f55c82835d7e778ad/main/10-projects/Echo%20I%2BD/Echo%20I%2BD%20%E2%80%94%20Futures.md); [S02 planner de campañas](https://github.com/xKoRx/agents-os/blob/8c79805ef5a558369f83fd6f55c82835d7e778ad/main/10-projects/Echo%20Futures/agentes/Echo%20Futures%20%E2%80%94%20Optimizaci%C3%B3n%20de%20Campa%C3%B1as.md); [S03 runbook](https://github.com/xKoRx/agents-os/blob/8c79805ef5a558369f83fd6f55c82835d7e778ad/main/30-resources/runbooks/echo-futures-strategy-qualification-runbook.md).
- [S04 Platform en S04](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/platform_campaign.go); [S05 Platform en master](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_campaign.go); [S06 PlatformProfile en master](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_profile.go).
