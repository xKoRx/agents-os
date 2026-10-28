---
type: prompt
schema_version: 1
status: active
area: "[[Trading]]"
target: "Manager técnico existente; C01 GOD Cloud; C02 TOP Cloud condicional"
prompt_version: 1
inputs:
  - "Decisiones Owner del 2026-10-28"
  - "Retornos A/B y baseline real de integración S04"
  - "Contratos, código y receipts vigentes del Backtester"
outputs:
  - "Diseño de campañas CHALLENGE, FUNDED y SIMULATION"
  - "KPI, caja, reutilización y plan incremental revisables"
  - "Mandatos de diseño, revisión y coordinación"
project: "[[Echo I+D — Futures]]"
aliases:
  - "FUT-R01 — Frente C de campañas"
related:
  - "[[Echo Futures — Optimización de Campañas]]"
  - "[[FUT-R01-ITERACION-01]]"
  - "[[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]]"
tags:
  - kind/prompt
  - area/trading
  - project/echo-rnd
created: "2026-10-28"
updated: "2026-10-28"
---

# FUT-R01 — Campañas Challenge, Funded y Simulation

## Propósito

Registrar el cambio Owner del 28-10-2026 y preparar el desarrollo incremental de una capacidad económica del Backtester. **Frente C** designa este nuevo trabajo; no debe confundirse con el antiguo **I01-C**, que era un mandato read-only de datos/recibos.

**Estado:** requisitos Owner aceptados y prompts preparados; diseño técnico C01 pendiente. No se han ejecutado nuevas campañas ni implementado estas capacidades por esta entrega. El Owner informa que la integración S04 completa y sus variantes a master está en curso. Ese reporte sustituye la pausa anterior, sin certificar merge, tests, aceptación o despliegue.

El Backtester es parte de la responsabilidad funcional de I+D Futures: una carencia necesaria se transforma en desarrollo priorizado, con evidencia de salida. [[Echo Futures — Optimización de Campañas]] conserva el planner técnico de entrega; [[Echo Futures]] y Runtime Pools mantienen arquitectura, contratos y gates. El manager de investigación sigue dueño de prioridad, KPI y decisión económica. No se crea otro manager permanente, proyecto, motor ni scheduler.

## Contrato de entrada

### Decisiones Owner vigentes

| Decisión aceptada | Consecuencia concreta |
|---|---|
| USD 4.000 destinados a comprar challenges, sin futuros operados con capital propio | Separar bankroll comercial de saldo nominal/equity prop. Forex permanece separado; no inventar aportes. Si un programa exige otro desembolso, registrar su fuente o dependencia antes de declarar financiable el escenario. |
| Retiro sin objetivo fijo de USD 3.000 | Evaluar importe, momento y continuidad de retiro dentro de reglas, costes y horizonte. USD 500/2.000/5.000 son ejemplos Owner, no lista autorizada ni búsqueda congelada. |
| Challenge: pasar o perder rápido dentro de lo permitido | No añadir caps prudenciales de lotes/riesgo/pérdida acumulada por costumbre. El espacio admisible lo delimitan reglas de programa, broker/mercado y controles técnicos. El tamaño concreto necesita evidencia; no se presume que el máximo maximiza pases. |
| Umbral aceptable challenge 1/3; mejorar por encima | Es criterio Owner para futuras campañas, no promedio del mercado ni resultado Echo. Antes de aplicarlo se fija unidad (compra/cuenta/intento y resets), cohorte y horizonte; reportar ambas vistas, sin elegir el denominador más favorable. Informar muestra, incertidumbre, pendientes y tiempo; no cambiar G0–G5. El 25% anterior queda histórico. |
| Dos campañas aisladas, CHALLENGE y FUNDED, para la misma Strategy o conjuntos diferentes | Cada etapa usa MM, reglas, condiciones iniciales, ledger y KPI propios. Una solicitud puede pedir ambas en paralelo lógico, con ejecución física sujeta a capacidad. |
| FUNDED cuenta todas las cuentas usadas, incluidas las quemadas | Promedio por iniciada, no sólo por pagadora; separar pagos repetidos y pérdida posterior a un cobro. |
| Todo cash neto recibido vuelve al bankroll | Reinversión 100%; no modelar extracción personal ni reservar capital unilateralmente. Un pago solicitado o aprobado aún no financia nuevas compras. |
| SIMULATION compone después compras, etapas, cuentas/pools, varias estrategias y props con un único bankroll | Debe reconstruir causalmente caja, coste, split, demoras, reglas, restricciones de concurrencia y pérdidas. Primer incremento de simulación puede ser 1×1; capacidad multi-Strategy/multi-prop sigue siendo alcance posterior requerido. |
| Desarrollo por iteraciones cortas y reutilización | Diseñar el primer incremento hasta poder implementarlo; siguientes sólo outcome/dependencia/gate. Preservar S04 y sus recibos válidos. |

Strategy conserva setup, filtro opcional y objetivo/riesgo técnico o RR. MM por prop/programa/etapa es otra entidad. Política de retiro/compras debe quedar identificada en los contratos económicos existentes; su ubicación técnica final es parte del diseño, no una nueva entidad impuesta por este documento.

El Owner no seleccionó proveedor ni autorizó compras/operaciones por este cambio. La prioridad agresiva no permite infringir reglas comerciales, restricciones de automatización, integridad de órdenes o controles técnicos. Tampoco convierte esperanza positiva por trade o supervivencia indefinida en gates universales.

### Evidencia existente y vigencia

- Agents-OS leído al comienzo: `837db281b78bc3d5f28834cf5e6ad539217696d5`.
- Echo master observado en revisión read-only: `347eee8bdab7f7628629af6383d1e45520815abd`. Es snapshot remoto, no baseline de implementación aceptado ni prueba física. En ese árbol aún no se observaba campaign-lab/research_lab.py; la integración puede seguir avanzando.
- Platform/SDK ya contienen lifecycle, MM/Strategy/Provider, cobros diferidos, economía y replay/identidad. La capacidad completa de los tres tipos no está certificada.
- En ese corte, Platform conserva caja inicial 5.000, compra 120 y perfil histórico E2T/GAU50. `PlatformProfile` valida targets 2250/2300/2500/3000 y `PayoutNet` emplea split histórico específico. Es reutilización parcial, no soporte genérico de proveedores/retiros.
- El controlador Platform conserva cuentas pero selecciona un turno físico; ello no acredita concurrencia de varias estrategias/props con caja común.
- S04 documenta catálogo, 26 nativas/78 SG, runner, preparación, reanudación, conciliación y bundles. Es evidencia histórica que se debe reconciliar con la entrega integrada; no reinstalar otro laboratorio.
- RV-01 conserva NO_APTO_AUN para una campaña definida/reproducible; no bloquea diseñar esta capacidad. A/B no han retornado a este manager. Los DR y RV originales se preservan sin edición.

### Definiciones de KPI propuestas para revisión

Las decisiones anteriores son Owner; estas definiciones operacionalizan el requerimiento y deben formar parte de C01 revisado.

**CHALLENGE.** Congelar cohorte, horizonte y seguimiento. Distinguir cuentas comerciales, compras e intentos/resets. Cada intento iniciado termina en pase, fallo comercial, otro terminal identificado o pendiente. Los errores técnicos del experimento se registran aparte; no son automáticamente fracaso de trading ni se eliminan silenciosamente.

- Reportar tasa por intentos = intentos aprobados / intentos iniciados, y tasa por adquisición/compras comerciales = unidades compradas que consiguieron pase / unidades compradas de la cohorte. Vincular resets gratuitos/pagados, renovaciones e intentos a su compra sin duplicar éxitos. **La unidad a la que se aplicará 1/3, tratamiento de resets y horizonte se fijan explícitamente antes de adjudicar**; no quedan aceptados por una fórmula candidata. Para hablar de probabilidad a H hace falta seguimiento comparable; un cierre con inicios escalonados es una fotografía con censura.
- Mostrar también pase entre resueltos, claramente separado; no ocultar pendientes para alcanzar 1/3.
- Coste por pase = costes de evaluación de toda la cohorte / pases.
- Coste por funded disponible = costes de adquisición y activación atribuibles a toda la cohorte / funded efectivamente activadas. Aprobar no equivale a activar.
- Coste de todas las perdidas, resets y renovaciones entra una sola vez. Cero pases/activaciones: N/A sin éxito observable, nunca coste cero. Con pendientes, los ratios al corte son provisionales.
- Tiempo hasta pase/fallo, distribución de costes, causas, oportunidades/vetos y dependencia por período acompañan el KPI principal.

**FUNDED.** Sea N el número de cuentas funded iniciadas, W el total neto efectivamente recibido y F los desembolsos operativos funded externos **no incluidos ni en W ni en adquisición**. Para la fórmula combinada, los cargos se particionan por evento: adquisición incluye compras, resets/renovaciones de evaluación y activación hasta disponibilidad; F sólo costes posteriores distintos. La activación se asigna una vez a adquisición, nunca también a F. Otra vista de costes puede mostrarse, pero no sumarse duplicada al resultado.

- Fracción con primer cobro = cuentas con al menos un pago recibido / N.
- Cobro medio por funded iniciada = W / N.
- Margen funded antes de adquisición = (W − F) / N.
- Contribución combinada aproximada por funded = margen anterior − coste de adquisición por funded disponible, sólo con cohortes/fechas/perfiles compatibles. No es por sí sola una simulación integral.
- Una cuenta que cobra dos veces y después se quema cuenta una vez en N, una pagadora, dos pagos y una pérdida. Quemadas/sin pago aportan cero cobros, no desaparecen.
- Reportar pagadoras/quemadas/activas/pendientes, cobros por ciclo, tiempo, importes y horizonte. Cobro medio entre pagadoras se rotula aparte.
- Funded aislada declara origen: estado estandarizado, estado/fecha derivado de pases concretos o distribución modelada. No transferir resultados entre orígenes sin justificarlo.

**SIMULATION.** Con cero aportes y reinversión total:

`bankroll(t) = 4000 + cash neto recibido(t) − desembolsos efectivos del bankroll(t)`.

Descomponer desembolsos por compras, resets, renovaciones, activación y otros cargos aplicables, sin doble conteo. Si algún cargo obligatorio no tiene fuente de financiación resuelta, el escenario no está acreditado como financiable. **Pérdida nominal de la cuenta prop no se debita otra vez del bankroll**: ya se perdió la posibilidad financiada por su adquisición, salvo cargo contractual externo verificable.

Conservar orden y fecha de compra, pase, activación, operativa, elegibilidad, solicitud, aprobación, cobro y reinversión. Ningún saldo nominal, PnL no cobrado ni pago pendiente compra otra cuenta. Distinguir caja disponible, compromisos, cuentas activas y pagos pendientes al horizonte; no atribuirles cash residual inventado.

Resultados: bankroll final/mínimo, cambio neto B(H)−4000, compras/pases/activaciones/pérdidas, pagos recibidos/pendientes/denegados, costes, tiempo sin liquidez para comprar, concentración y atribución por Strategy/prop. Varias cuentas sobre la misma trayectoria no son réplicas independientes. No dividir días/cuentas dependientes y sumar curvas como si no compartieran caja.

**Retiro y escalabilidad.** Se elegirá el mejor retiro/política dentro del conjunto y horizonte evaluados, con separación real selección/evaluación. El objetivo candidato es caja neta de campaña al horizonte; acompañar por tiempo/dispersión/agotamiento. Horizonte, pesos o desempates materiales no quedan inventados por esta nota. Maximizar el primer cheque puede empeorar el total posterior. Una contribución media positiva merece evaluación de escalado; no demuestra crecimiento infinito con caja finita, cuentas correlacionadas, demoras y límites comerciales.

### Casos de aceptación que discriminan errores

Son ejemplos de contrato, **no tests ejecutados ni resultados de estrategias**.

| Caso | Resultado exigido |
|---|---|
| 12 intentos cuestan 1.200 y pasan 3 | Coste/pase 400; nunca 100 por cargar sólo la ganadora. |
| De esos 3 pases se activan 2 a coste 100 cada una | Coste agregado por funded disponible 1.400/2 = 700; el tercer pase sigue identificado. |
| Cero pases | Mostrar gasto y ausencia de coste unitario finito estimable. |
| 10 pases, 20 fallos, 70 pendientes | 10% sobre iniciadas al corte; 33,3% entre resueltas, rotulado aparte. |
| 10 funded, 3 reciben 1.000 netos cada una | Cobro medio 300 por funded iniciada; 1.000 sólo entre pagadoras. |
| Dos pagos y posterior pérdida de una cuenta | Preservar ambos cobros; una cuenta iniciada y una perdida. |
| Pago bruto 1.000, split 80%, deducción única 20 | Cash recibido 780. Comisiones ya en PnL no vuelven a restarse. |
| Activación incluida en adquisición y vista de costes funded | El resultado combinado la resta una sola vez; F la excluye expresamente. |
| Compra con reset gratuito y/o reset pagado | Conservar unidad comercial e intentos vinculados, tasas por ambas unidades y costes; no sustituir silenciosamente el denominador del 1/3. |
| Pago solicitado/aprobado pero aún no recibido | No habilita nuevas compras; respetar días hábiles/fecha efectiva. |
| PnL nominal positivo o pérdida de equity prop | No entra ni sale directamente del bankroll comercial. |
| Funded inicia antes del pase que supuestamente la financió | Rechazar esa composición causal, aunque la media aislada sea favorable. |
| Diez cuentas replican señal y pérdidas simultáneas | Conservar dependencia; no diez réplicas IID. |
| Retry/reanudación reproduce un evento de pago | No duplicar cash, compras ni identidad; recibo trazable. |
| Dos etapas analíticas simultáneas | Aislar estado/ledger/MM; misma Strategy no implica mismos fills ni riesgo. |
| Política de retiro seleccionada con una ventana | Congelarla antes de evaluación temporal; no afinar usando esa evaluación. |

### Admisión y alcance incremental

G0–G5 se conservan. **El G4 actual exige CHALLENGE_PASSED por identidad Strategy×variante×MM; su aplicabilidad a una campaña FUNDED independiente requiere decisión explícita.** C01 debe proponer la resolución focal si es necesaria. No transferir PASS del MM challenge a funded ni llamar SIMULATION a un histórico para saltar el guard. La discusión no impide diseñar contratos o casos deterministas del motor.

Orden de entrega propuesto, coordinado con S04:

1. Reconciliar baseline aceptado y contratos/KPI comunes.
2. CHALLENGE aislada con reporte completo.
3. FUNDED aislada y solicitud dual comparable para una Strategy.
4. SIMULATION 1 Strategy/1 prop con caja causal de 4.000.
5. Varias estrategias, pools y al menos dos props concurrentes con una caja común y asignación explícita.

Puede agruparse 2–3 si reduce trabajo y permite verificar ambos resultados por separado. Diseño C01 puede avanzar mientras se integra S04; implementación nueva parte del corte aceptado y de un mandato autorizado. No es permiso para detener ni rehacer la integración actual.

## Contrato de salida

- Requisitos aceptados separados de decisiones técnicas candidatas y UNKNOWNs.
- Matriz de reutilización/migración por fuente y evidencia.
- SPEC funcional, propuesta técnica, PLAN/TASKS del primer incremento y aceptación separadas.
- Algoritmos de medición y casos que reconcilien costes, estados, cobros y caja.
- Brecha de admisión funded-only resuelta para revisión, sin cambios de gates ejecutados.
- Un único planner técnico existente; el manager Futures integra prioridades y resultados.
- Prompts siguientes preparados, no despachados por esta publicación.

## Prompt

### C01 — GOD Cloud, diseño cuantitativo y técnico ONE-SHOT

```text
# ECHO FUTURES — C01: DISEÑO DE CAMPAÑAS CHALLENGE, FUNDED Y SIMULATION
ROLE: GOD · SURFACE: CLOUD · WORK FUNCTION: diseño cuantitativo y técnico.
ONE-SHOT de contexto fresco. Eres el worker, no el manager ni quien acepta el diseño.

/goal
Entregar un diseño candidato completo y revisable que amplíe el Backtester existente para medir CHALLENGE y FUNDED por separado y componer después SIMULATION con caja finita compartida. Cerrar requisitos económicos, estados, KPI, reutilización, límites de admisión y primer incremento implementable. Estados finales: READY_FOR_OWNER_REVIEW, PARTIAL o BLOCKED con dependencia exacta. No implementar ni certificar.

/authorities
Bootstrap canónico xKoRx/agents-os, master, vault main/, entrada main/AGENTS.md. Cargar echo-futures-research-manager, technical-project-manager y sdd-workflow mediante su routing vigente; echo-rnd-cycle-runbook; echo-retester-master y echo-futures-strategy-qualification-runbook para los límites de admisión.
Leer primero:
- main/10-projects/Echo I+D/Echo I+D — Futures.md
- main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION.md
- main/10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md, sólo estado, contratos y recibos pertinentes.
- EF-BACKTEST-RUNTIME-INTEGRATION-PLAN y autoridades R6/GOD-05 referenciadas, sólo delta que afecte el diseño.
Leer A/B cuando estén publicados; su ausencia no bloquea contratos genéricos, sí conclusiones específicas de Strategy/prop.

/baseline
CURRENT_TASK_STATE: CONTINUATION. El Owner informa S04 completa y variantes en integración a master; la certificación del corte todavía debe recuperarse. No duplicar ni alterar ese merge.
PRIOR_ARTIFACTS:
- Decisiones Owner de tres campañas y economía: ACCEPTED_INPUT.
- S04/lab, Platform y diseño anterior: REFERENCE_ONLY hasta comprobar vigencia y alcance por símbolo/receipt.
- RV-01: dictamen documental vigente NO_APTO_AUN para campaña definida, no veto universal al diseño.
- A/B: WAITING_RETURN o estado documentado actual; no inferir finalización.
El snapshot remoto Echo 347eee8bdab7f7628629af6383d1e45520815abd sólo orienta; NO es baseline certificado para implementar. Reconciliar contra el corte que devuelva la integración.

/frozen
NQ exclusivo; Strategy = setup + filtro opcional + objetivo/riesgo técnico o RR. MM por prop/programa/etapa separado. No cambiar la señal ni geometría para resolver sizing.
USD 4.000 son caja para comprar challenges, no equity de futuros propios; Forex separado, sin aportes adicionales. Todo payout neto efectivamente recibido se reinvierte.
No existe objetivo fijo de retiro USD 3.000: importe, momento y continuidad se evaluarán como política económica identificada.
Challenge: resolver pase/pérdida lo más rápido permitido. No imponer caps prudenciales adicionales de lotes/riesgo/pérdida acumulada por costumbre; obedecer todas las reglas de prop, broker, mercado y controles técnicos. El sizing exacto debe justificarse; máximo tamaño no prueba optimalidad.
1/3 es umbral de aceptación Owner para challenge futuro, no promedio empírico ni modificación de G0–G5.
FUNDED mide cobros netos por TODAS las cuentas iniciadas, incluidas quemadas y sin pago. SIMULATION encadena etapas, costes y cobros reales en el tiempo.
Backtester es capacidad funcional bajo responsabilidad de I+D Futures; owners técnicos existentes conservan contratos, implementación y gates. No crear otro programa, planner, scheduler, DSL o motor.

/scope
Diseño de capacidad y delta mínimo, sin código/producto, tests ejecutados, campañas, compras, hosts, mensajes a terceros ni operación real.
Presupuesto: un worker, una entrega; hasta 10 fuentes internas técnicas decisivas además del routing mínimo, más los retornos A/B si están. Fuentes adicionales sólo si cierran una contradicción concreta y explicando el delta. Consultas oficiales puntuales, sin nuevo Deep Research ni elección comercial.
No sustituir un dato físico faltante por inferencia. Proponer una única cápsula read-only para Hefesto sólo si resulta indispensable, sin despacharla.

/execute
1. Mapear requisitos→capacidad existente→delta→prueba de aceptación. Distinguir código observado, receipt histórico, integración actual y capacidad certificada. Recuperar modos/runner/cash/identity/account lifecycle/reportes reales antes de proponer nombres o APIs.
2. Definir CHALLENGE y FUNDED como experimentos separados sobre el dominio compartido. Una solicitud puede pedir ambas etapas para la misma Strategy, con MM/RuleSet/estado/ledger propios y resultados comparables. Resolver como trabajos independientes mediante infraestructura existente; paralelismo lógico no obliga a concurrencia física.
3. Formalizar cohortes, intentos/compras/resets, pases, fallos comerciales, fallos técnicos, pendientes y activaciones. Reportar tasas por compras/cuentas y por intentos, vinculando resets pagados/gratuitos sin duplicar éxitos. Fijar explícitamente unidad, horizonte y tratamiento de resets antes de aplicar 1/3. Iniciadas/resueltas separadas, seguimiento/censura y coste agregado por pase/funded disponible. Cero éxitos no devuelve coste cero.
4. FUNDED: declarar origen/fecha/estado inicial; medir cuentas que cobraron, importe neto total y medio por todas, costes externos, tiempo al cobro, pagos repetidos y pérdida antes/después de cobrar. Una pagadora puede quemarse después. Particionar cada coste por evento entre adquisición (incluida activación) y operación funded posterior: no restar activación en ambos lados ni descontar de nuevo cargos ya en cash neto/PnL.
5. SIMULATION: definir flujo causal compras→pase→activación→funded→solicitud→aprobación→cobro→nueva compra. Un ledger de bankroll común; saldos nominales y payouts pendientes no son caja. Conservar obligaciones, fechas y atribución. Empezar con una Strategy/prop y extender después a varias estrategias, pools y al menos dos props simultáneas.
6. Proponer política de compra/asignación/reemplazo predeclarada y política de retiro finita, no una búsqueda cartesiana. Si hay costes obligatorios fuera de compra, identificar fuente de financiación; no inventar fondos ni ocultarlos. Optimizar por caja de campaña a horizonte fijado; resolver como propuesta cualquier criterio material no aceptado.
7. Conservar dependencia temporal, señales coincidentes y estados generados por pases. No componer campañas mediante multiplicación independiente de ratios ni reutilizar trades cerrados escalados si el MM cambia admisión/estado/fills.
8. Resolver causalidad/datos/replay del runtime común y diferencias del adaptador simulado. M1 no inventa trayectorias/fills/bounds. Versionar tipo, etapa, MM, RuleSet, retiro, compras, datos, build, selección y estado inicial.
9. Tratar expresamente G4 basado en CHALLENGE_PASSED frente a FUNDED aislada o MM distinto. Conservar gates vigentes; cualquier cambio requerido se entrega como decisión focal para Owner, no excepción ya aplicada ni PASS heredado.
10. Proponer incrementos: contratos/KPI → CHALLENGE → FUNDED/comparación dual → SIMULATION mínima → varias estrategias/props/caja común. Reutilizar S04 sin reejecutar evidencia válida. Detallar sólo el primer incremento y las dependencias/pruebas de los siguientes.

/verify
Revisar documentalmente, no ejecutar, los casos del mandato: costes de todas las compras, cero pases, pendientes, pase sin activación, quemadas sin cobro, varios payouts y pérdida posterior, split/cargos, cobro diferido, ausencia de compra sin liquidez, pérdidas nominales separadas de caja, estados funded condicionados, correlación simultánea, retry sin doble pago y compatibilidad legacy.
Demostrar con ejemplos contables pequeños que bankroll final reconcilia con flujos y que cambiar el objetivo de retiro sólo altera la identidad económica pertinente. No llamar pruebas físicas a esos ejemplos.
Revisar que ventaja media positiva no se convierta en escala infinita, y que selección de MM/retiro conserva evaluación temporal separada.

/reuse
Inventariar componentes/recibos de S04, Platform, SDK, supervisor, reporting, fixtures y contratos reutilizables. No crear utilidades universales sin segundo uso concreto. Identificar invalidación selectiva cuando cambie una semántica.

/improve
Informar METHOD_DELTA y REUSABLE_BEHAVIOR_CANDIDATES con evidencia o NONE. No editar skills, gates o runbooks como efecto lateral.

/close
Persistir el informe completo, con fuentes, tablas, decisiones abiertas y SPEC/PLAN/TASKS claramente separados, en:
main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-DESIGN.md
Si ya existe, clasificar y continuar por delta; no sobrescribir trabajo concurrente. El manager integra planner y autoridades compartidas; no escribirlas.
Cargar y aplicar:
main/80-agents/skills/agents-os-agent-run-register/SKILL.md (registrar sólo si aplica; explicar omisión documental),
main/80-agents/skills/agents-os-session-feedback/SKILL.md,
main/80-agents/skills/agents-os-session-close/SKILL.md.
Esta ONE-SHOT incluye feedback y cierre de SU sesión, no del programa ni del manager. Publicar Agents-OS en master sin ramas/PR/force, reconciliar HEAD y verificar. Si falta acceso, entregar artefacto completo y bloqueo explícito; nunca fingir publicación.
Retorno Owner-mediated al manager: estado, path/commit, 8–12 líneas ejecutivas, decisiones requeridas, primer incremento y verificación pendiente. PRO_CHAT_POOL_DELTA sólo confirmado o UNKNOWN.
No depender de micro-followups para decisiones técnicas rutinarias; parar únicamente por contradicción material, autoridad faltante o límite del encargo.
```

### C-MANAGER — coordinación en el manager técnico existente

```text
# ECHO FUTURES — MANAGER DE ENTREGA: S04 + NUEVOS TIPOS DE CAMPAÑA
ROLE: GOD · SURFACE: CLOUD · WORK FUNCTION: manager técnico del entregable existente.
Continuidad coordinadora, no worker ONE-SHOT. Usar preferentemente en el manager que ya conduce frente 1; no abrir un coordinador competidor.

/goal
Coordinar la integración S04→master que ya está en marcha y la entrega incremental de CHALLENGE, FUNDED y SIMULATION, conservando paridad semántica y evidencia. Estado inicial: RECONCILING; siguientes estados: DESIGN_REVIEW, READY_FOR_AUTHORIZED_IMPLEMENTATION, VERIFYING, READY_FOR_OWNER_REVIEW o BLOCKED con causa.

/authorities
Bootstrap xKoRx/agents-os/master, vault main/, main/AGENTS.md. Aplicar technical-project-manager, echo-futures-research-manager, sdd-workflow, echo-retester-master y runbook de cualificación según alcance.
Planner técnico único: main/10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md.
Mandato funcional vigente:
main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION.md.
I+D Futures conserva prioridad/decisiones económicas; Echo Futures/Runtime Pools mantienen autoridades técnicas, R6 y freezes pertinentes.

/baseline
CURRENT_TASK_STATE: CONTINUATION. Integración S04/variantes IN_PROGRESS_OWNER_REPORTED; recuperar commit, alcance y receipts actuales del ejecutor existente. No duplicar merge, resetear, recrear trabajo ni aceptar resultado por estar en master.
A/B están pendientes de retorno al manager de I+D. C01 diseño puede avanzar en paralelo a la integración; diff final depende del corte aceptado.
Clasificar todo artefacto ACCEPTED_INPUT / REFERENCE_ONLY / UNREVIEWED / SUPERSEDED antes de reutilizarlo.

/frozen
Tres tipos de campaña; USD 4.000 para compras, cero capital propio de trading y Forex separado; reinversión completa del cash neto recibido; payout variable; MM de resolución rápida sujeto a reglas; umbral Owner 1/3 para challenge; Strategy/MM/Provider separados; NQ exclusivo.
No imponer topes prudenciales no pedidos, prometer escala infinita, relajar reglas ni gates. La nueva capacidad de simulación no autoriza gasto o trading.
Los 25% históricos, USD 5.000 y perfiles antiguos se conservan con su identidad; no son defaults nuevos.
Un funded aislado no demuestra adquisición ni acceso financiado a ese estado.

/scope
Gobierno, recuperación read-only y diseño documental ahora. No duplicar autoridades/planners; no programar ni ejecutar campañas como efecto lateral.
Este prompt no amplía permisos del trabajo de integración ya autorizado. Cualquier implementación nueva requiere paquete concreto con base, scope, presupuesto y autorización aplicable; las decisiones técnicas rutinarias quedan con el ejecutor senior.
Presupuesto inicial: una reconciliación de estado y una devolución; después iteraciones por retorno verificable, sin vigilancia/polling indefinido.

/execute
1. Leer estado/receipts del frente activo y obtener la lista exacta de variantes, MM y capacidades S04 migradas. Separar SOURCE, BUILD, TEST, ACCEPTANCE, DEPLOY; resolver discrepancias sin intervenir trabajo ajeno.
2. Recibir C01 o entregar su prompt completo al Owner. Adjudicar diseño contra requisitos; si falta evidencia crítica, un único encargo focal, no rehacer cuatro DR.
3. Mantener una sola cola técnica en el planner existente. Orden propuesto: baseline S04 aceptado; contratos/KPI comunes; CHALLENGE; FUNDED y comparación dual; SIMULATION 1×1; extensión multi-Strategy/multi-prop con bankroll único. Agrupar sólo si reduce esfuerzo sin perder verificabilidad.
4. Detallar el incremento activo: resultado, SPEC funcional/técnica, base/branch reales, responsables, recursos, aceptación, rollback y condición de parada. Las futuras iteraciones mantienen sólo resultado/dependencias.
5. Reconciliar G4 challenge con funded-only mediante decisión expresa si hace falta; no cambiar guards por interpretación.
6. Cuando exista autorización de implementación, emitir los mandatos LOCAL con el ciclo vigente: implementación, verificador adversarial independiente en contexto fresco, corrección/gate final. Un review Cloud no reemplaza E2E local. No inventar comandos ni afirmar ejecución.
7. No promover a LIVE políticas marcadas HISTORICAL_ONLY. La integración de variantes y la nueva economía no certifican runtime-ready ni producción.
8. Devolver a I+D la evidencia mínima, capacidad pendiente, decisión económica y siguiente pregunta; no bloquear research A/B por tareas de producto que no cambien su decisión.

/verify
Para cada incremento, distinguir requisitos demostrados de NOT_EXECUTED/UNKNOWN. Exigir reconciliación contable, causalidad, aislamiento de etapas, reproducibilidad/reanudación, conservación legacy y ausencia de doble gasto/cobro. Medir capacidad antes de afirmar throughput.
Concentración temporal/correlación entre cuentas permanece en las simulaciones; no financiar compras con beneficios nominales ni pagos pendientes.

/reuse
Usar SDK/runner/supervisor/receipts del lab y componentes existentes. Reusar datos/analytics sólo con identidad y causalidad compatibles. Preservar fixtures del verificador que capturen invariantes durables.

/improve
Cada worker retorna activos reutilizables y feedback concreto o NONE; no crear más skills/managers como resultado rutinario.

/close
Actualizar por delta el planner técnico existente y sus artefactos propios; evitar writers concurrentes. I+D integra su planner central. Publicar Agents-OS en master, sin ramas/PR/force, con HEAD reconciliado, change_log y lectura de verificación.
Todos los workers que despaches deben cargar agents-os-agent-run-register (cuando aplique), agents-os-session-feedback y agents-os-session-close: son ONE-SHOT con persistencia, feedback, cierre y retorno con paths/SHA/estado. Registrar consumo Pro sólo confirmado.
Tú eres coordinador: NO cierres automáticamente tu sesión ni el programa. Cierre formal sólo cuando el Owner lo pida. No vigilancia autónoma.
Primera respuesta: estado observado vs informado, qué falta para aceptar S04, incremento activo de campañas y el prompt exacto que corresponde ejecutar ahora.
```

### C02 — revisión TOP Cloud condicional

Despachar después de C01 si el manager determina que una revisión independiente añade evidencia frente a riesgos materiales del diseño. No es revisión física ni un pase obligatorio para producir documentos.

```text
# ECHO FUTURES — C02: REVISIÓN ADVERSARIAL DEL DISEÑO DE CAMPAÑAS
ROLE: TOP · SURFACE: CLOUD · WORK FUNCTION: revisor documental independiente.
ONE-SHOT, contexto fresco. No eres el autor del diseño, manager ni verificador físico.

/goal
Refutar o sostener EF-CAMPAIGN-MODES-DESIGN contra el mandato Owner, fuentes y ejemplos contables. Salida READY_FOR_OWNER_REVIEW, FINDINGS o BLOCKED. No convertir review en aprobación.

/authorities
Bootstrap xKoRx/agents-os/master desde main/AGENTS.md. Leer el planner I+D Futures, FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION, el diseño C01 y las autoridades técnicas enlazadas que sean decisivas. Cargar technical-project-manager y gates vigentes.

/baseline
CURRENT_TASK_STATE: REVIEW. Requiere diseño C01 publicado con commit. Si falta, NO_DESPACHADO; no redactar un sustituto. Registrar autoría y límites reales de independencia; contexto fresco por sí solo no prueba independencia histórica.

/frozen
Preservar decisiones Owner de tres modos, reinversión, capital de compras, MM agresivo permitido, umbral 1/3, NQ y entidades separadas. No imponer prudencia de cuenta propia ni ignorar reglas comerciales.

/scope
Una revisión, hasta seis fuentes internas decisivas adicionales al diseño/mandato. Sin código, pruebas físicas, backtests, gastos, hosts ni cambios del diseño autor. No abrir investigación general.

/execute
Buscar contradicciones en cohortes, resets, activación, costes medios, pending/censura, pagos repetidos, split, dinero cobrado vs aprobado y bankroll real. Examinar funded exógena vs condicionada al pase, concurrencia causal, correlación, selección de retiro/MM y falsas extrapolaciones de escala. Verificar que G4/funded sea resuelto como decisión, no bypass.
Contrastar el delta con lo ya existente en S04/Platform; detectar otro motor/scheduler, cambios de runtime encubiertos o una abstracción sin uso concreto. Identificar bloqueos del primer incremento y deuda realmente diferible.

/verify
Presentar contraejemplos documentales con esperado/defecto/impacto/reparación mínima. Separar errores demostrados de riesgos o preguntas. No exigir rentabilidad antes de desarrollar una capacidad de medición ni usar una media positiva como prueba económica.

/reuse
Clasificar casos útiles como candidatos de regresión contable/temporal para el futuro verificador LOCAL; no decir que se ejecutaron.

/improve
REUSABLE_BEHAVIOR_CANDIDATES con evidencia o NONE; sin editar skills ni gates.

/close
Persistir revisión detallada exclusivamente en:
main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-REVIEW.md.
Conservar diseño y planner para su owner. Cargar agents-os-agent-run-register (si aplica), agents-os-session-feedback y agents-os-session-close; feedback y cierre de esta ONE-SHOT explícitos. Agents-OS master, sin ramas/PR/force; reconciliar HEAD y verificar publicación.
Retorno Owner-mediated: dictamen, hallazgos priorizados, path/SHA, límites de independencia, verificación NOT_EXECUTED y siguiente decisión. PRO_CHAT_POOL_DELTA confirmado o UNKNOWN.
```

### Delta para I01-B en curso

Aplicar al mismo encargo, sin reiniciarlo ni abrir otro DR. I01-A conserva su pregunta de señal; ambos recuperan decisiones Owner vigentes al retornar.

```text
ACTUALIZACIÓN OWNER PARA I01-B — mantener el encargo original y aplicar sólo este delta:
1. USD 3.000 queda superseded como meta fija. Documenta restricciones de importe/momento/split y costes para evaluar después una política de retiro; no elijas un número sin experimentos.
2. USD 4.000 es caja para comprar challenges; no capital propio con que operar NQ. Forex separado y sin reposición. Identifica cualquier fee obligatorio adicional y su fuente de pago; no inventes financiación.
3. Challenge busca pasar o quemar rápido dentro de TODAS las reglas aplicables. No introduzcas límites prudenciales extra por costumbre. 1/3 es umbral Owner para futuras campañas, no promedio del mercado.
4. Todo cash neto efectivamente recibido se reinvierte. Solicitud/aprobación/PnL nominal no son caja.
5. Se diseñarán campañas CHALLENGE y FUNDED separadas y después SIMULATION causal; entrega perfiles por etapa, denominadores/cohortes/costes y requisitos compatibles. Funded incluye todas las cuentas iniciadas, también quemadas.
6. La integración S04→master está en curso según Owner, no pausada; tu encargo continúa documental, sin intervenirla. El nuevo frente C de campañas no es el antiguo I01-C read-only de datos.
Recupera la autoridad actual en Echo I+D — Futures y FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION. No reinicies A/B ni repitas los DR.
```

## Límites

- Esta entrega publica decisiones y preparación. No ejecuta C01/C02, integra S04, compra cuentas ni modifica código/runtime/gates.
- A/B siguen pendientes de recepción; no se invalida su trabajo válido por el delta económico.
- I01-C de datos conserva alcance read-only, por coordinar con el owner técnico; el nuevo frente C no lo despacha automáticamente.
- No se modifica el significado de receipts históricos ni se exige volver a correr una campaña válida por cambiar de chat.
- La capacidad nueva no añade cobertura de mecanismos ni cuenta como estrategia. NQ, independencia demostrable y condiciones de evidencia siguen vigentes.
- El manager permanece abierto. Los workers futuros ONE-SHOT incluyen cierre/feedback por mandato expreso, sin cerrar el programa.

## Fuentes y revisión

- Owner: instrucciones del 2026-10-28 en esta continuidad, fuente de las decisiones aceptadas; no contienen resultados simulados/operados.
- [Planner del laboratorio al corte leído](https://github.com/xKoRx/agents-os/blob/837db281b78bc3d5f28834cf5e6ad539217696d5/main/10-projects/Echo%20Futures/agentes/Echo%20Futures%20%E2%80%94%20Optimizaci%C3%B3n%20de%20Campa%C3%B1as.md): objetivos/receipts históricos, C01–C10 y límites.
- [Platform campaign](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_campaign.go), [perfil](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_profile.go), [economía](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/platform_economics.go), [identidad](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/identity.go), [README](https://github.com/xKoRx/echo/blob/347eee8bdab7f7628629af6383d1e45520815abd/v3/backtester/README.md): código/documentación observados; no certificación física.
- [Rapid EOD 50K oficial](https://help.myfundedfutures.com/en/articles/16158363-rapid-eod-50k-a-comprehensive-look), fecha visible 24-08-2026; [LucidFlex payouts oficial](https://support.lucidtrading.com/en/articles/12945796-lucidflex-payouts), fecha visible 28-07-2026; consultados 28-10-2026. Sus diferentes mínimos/caps/splits/días ejemplifican por qué el retiro es una política sujeta al programa. No son una selección de prop ni perfiles completos acreditados.
- Dos apoyos read-only revisaron matemática y reutilización; un tercer apoyo TOP revisó el mandato y detectó doble conteo potencial de activación y ambigüedad compra/intento/reset. Reparaciones incorporadas: partición única de cargos y denominadores explícitos antes de aplicar 1/3. Sin código/tests/campañas/publicación propios; no son certificación física ni votos. Consumo de cuota Pro no confirmado: UNKNOWN, sin incremento inventado.
