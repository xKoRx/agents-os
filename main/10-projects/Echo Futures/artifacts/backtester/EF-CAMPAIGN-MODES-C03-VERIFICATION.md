---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[EF-CAMPAIGN-MODES-DESIGN]]", "[[EF-CAMPAIGN-MODES-I0-LOCAL]]", "[[EF-S04-INTEGRATION-RECONCILIATION]]", "[[EF-CAMPAIGN-MODES-REVIEW]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---

# EF-CAMPAIGN-MODES-C03-VERIFICATION

## Propósito

Persistir el retorno del apoyo ONE-SHOT documental C03 y la adjudicación focal del manager. Este recibo conserva el alcance exacto de la revisión; no certifica producto, aceptación S04 ni cualificación.

## Contenido

**PASS_DOCUMENTAL** para I0 descriptivo/opt-in/no-spawn. El reviewer independiente de la redacción en esta pasada leyó los candidatos y volvió a comprobar la corrección de F-C03-01. Independencia histórica UNKNOWN. Pruebas físicas NOT_EXECUTED. Owner REVIEW. El manager y el programa continúan abiertos.

### Adjudicación del manager después del retorno

- F-C03-01 cerrado por corrección y lectura focal del reviewer: pérdida nominal no debita caja; un reverso efectivo sí reduce neto, conservando el primer crédito y Q.
- Se incorporaron también las dos aclaraciones opcionales: bundle de 180 separado del caso compras100+100/refund100; I0.T2 nombra schema/reporte opt-in y catálogos históricos read-only. Son cambios de redacción y aritmética expresamente solicitados por el reviewer. El manager comprobó la delta; no se afirma una nueva revisión independiente sobre esos dos cambios finales.
- Los hashes del memo siguiente identifican exactamente los candidatos revisados. Los hashes de la tabla final identifican los archivos publicados tras esas dos aclaraciones. No se atribuye prueba física ni ejecución LOCAL a ninguna tabla.

### Retorno íntegro del reviewer

# C03 — Revisión documental independiente del delta y del paquete I0

ROLE: GOD  
SURFACE: CLOUD  
WORK FUNCTION: revisor documental ONE-SHOT; no manager ni implementador  
DICTAMEN: PASS_DOCUMENTAL  
OWNER_ACCEPTANCE: REVIEW  
PHYSICAL_VERIFICATION: NOT_EXECUTED  
INDEPENDENCE_HISTORY: UNKNOWN  
PRO_CHAT_POOL_DELTA: UNKNOWN  
REMOTE_WRITES: NONE

## Resultado y alcance

F01–F03 de C02 quedaron corregidos de forma sustantiva. El paquete delimita suficientemente la independencia del reporter I0: fuente 2baf319d inspeccionada, reporte opt-in derivado, ausencia de motores y mutación de recibos, runtime/SDK/launchers read-only, salida conservadora con UNKNOWN y verificación LOCAL posterior. No hace falta aceptar la paridad S04 ni portar qualification_guard.py para implementar esa proyección. Esas dependencias permanecen exigibles antes de las ejecuciones afectadas.

El dictamen inicial FINDINGS se debió a **un P2 documental en el oráculo de reversos**. El manager corrigió esa frase; la lectura focal posterior verificó su coherencia y cierra F-C03-01. **Dictamen final: PASS_DOCUMENTAL** para el delta y el paquete I0 no-spawn. No es aceptación de S04, del Owner ni prueba física. Dos aclaraciones opcionales eliminan ambigüedades del handoff, sin ampliar alcance ni bloquear el reporter.

Lectura de esta revisión: candidatos EF-CAMPAIGN-MODES-DESIGN, EF-CAMPAIGN-MODES-I0-LOCAL, EF-S04-INTEGRATION-RECONCILIATION y bloque vigente C03 del planner; contraste con C01 original, C02, mandato funcional y campaign-contract-delta. No se auditó nuevamente el repositorio producto ni se ejecutaron tests/builds/campañas/hosts. Las coordenadas siguientes corresponden a los textos candidatos leídos en esta pasada.

## F-C03-01 — P2 CERRADO: el criterio de aceptación del reverso contradecía el neto

**Fuente exacta:** EF-CAMPAIGN-MODES-DESIGN §17.4, criterio 5, línea 705:

> Dos pagos de una raíz cuentan Q=1; approved-only no cuenta; pérdida posterior y reverso no borran historia ni efectivo.

**Contraste:** §6.4, línea 248, dice que el reverso resta dinero y conserva el primer crédito; E0, línea 523, exige reducir W neto; V30, línea 509, exige cash retenido neto/reverso visibles y conciliados. El paquete LOCAL, líneas 125–128, también distingue primer crédito y reversos/cash retenido.

**Caso discriminante, sólo documental:** una raíz causal recibe +780 y luego un reverso efectivo de −780, ambos anteriores al corte. Q sigue siendo 1 y el primer crédito no desaparece del historial. W neto retenido y el efecto acumulado en caja son 0. La pérdida posterior de la cuenta, por sí sola, no resta los 780. Seguir literalmente «reverso no borra … efectivo» permite conservar indebidamente +780 netos o rechazar el reducer correcto.

**Impacto:** dos instrucciones distintas para el mismo oráculo de aceptación. El resto del contrato ya tiene la semántica correcta; no se alega que el modelo económico completo esté errado.

**Corrección mínima:** sustituir el final del criterio por:

> La pérdida posterior no borra los cobros recibidos. El reverso conserva la historia del primer crédito y Q, y reduce W/caja netos mediante su propio evento identificado.

No requiere decisión económica nueva: explicita la semántica ya escrita en §6.4/E0/V30.

**Disposición verificada:** el manager sustituyó el criterio por la separación explícita entre pérdida nominal y reverso financiero. La lectura focal confirmó: «Un reverso financiero preserva el historial del primer crédito y Q, pero resta el importe efectivamente revertido de W/cash neto; +780 y reverso −780 dejan Q=1 y cash neto=0». Esto satisface el caso y elimina la contradicción. No se ejecutó test físico ni se editó el candidato por parte de este reviewer.

## Aclaraciones opcionales, no bloqueantes

1. **I0-S1 /verify, línea 141:** «Bundle K=2 por180 frente a cardinalidad ausente; refund100 mantiene U bruta2 y coste neto100». El neto 100 corresponde al caso anterior de dos compras por 100, no al bundle de 180. Los ejemplos canónicos E0 son correctos. Separar en dos bullets o escribir «En el caso anterior de coste 200, refund 100 deja coste neto 100; el bundle de 180 conserva su propio total». Si se aplica refund 100 al bundle de 180, su neto es 80. No hay que crear un caso nuevo ni cambiar fórmulas.
2. **DESIGN I0.T2, línea 727:** «Fijar schema del contrato económico en catálogo/manifiesto del lab» conserva una formulación amplia de C01. §17.2–17.3 y Allowed Files de I0 mantienen catalog-v1.json y R02-HISTORICAL-MANIFEST.json read-only. Para evitar interpretación expansiva, escribir «Fijar schema/validación del reporte económico opt-in dentro del lab y artefactos SDD; catálogos/manifiestos históricos read-only». La lectura conjunta actual ya limita el permiso; esto no exige una nueva superficie ni bloquea el reporter.

## Comprobaciones positivas del delta

| Eje | Resultado documental y soporte |
|---|---|
| F01 / denominador | §5.1–5.2 hace entrar U por pago capturado y cantidad comercial conocida, antes de provisión. Dos compras de 100 con una pendiente conservan U=2, P=1, coste 200. Cuenta, factura, cargo, raíz e intento no son intercambiables. |
| Bundles y faltantes | K conocido produce K raíces y un cargo. K desconocido conserva gasto y subtotal conocido, pero U/ratios dependientes son UNKNOWN. No se infiere cantidad por precio ni se usa sólo el conjunto provisionado. |
| Refunds y retries | Refund es contra-coste recibido y desenlace de la raíz, sin borrar la cohorte pagada bruta. Reset contractual vincula nuevo intento salvo derecho independiente documentado; renovación ordinaria y retry no fabrican compras. Mismo ID/payload es idempotente; ID con términos incompatibles produce conflicto. |
| F02 / q longitudinal | §6.4 exige raíz→intento→pase→activación→payout efectivamente recibido. Cada raíz cuenta una vez; pagos repetidos conservan todo W. Refund no es payout. CHALLENGE 10/3 y FUNDED exógena 3/1 no prueban q=1/10. |
| UNKNOWN frente a cero | §5.2/6.4 y I0-S1 distinguen numerador incompleto, cardinalidad desconocida, NOT_OBSERVED y NO_LINKAGE. Q=0 requiere trayectoria enlazada y observada al corte. Cero éxito no produce coste unitario cero; semillas exógenas no reciben adquisición inventada. |
| Cortes y censura | §4.1/5.4 separan ingreso, seguimiento H, corte administrativo T y Hc. §8.3 y V19 conservan cobros posteriores como cola separada. Reversos y pagos deben seguir el mismo cutoff; no se adelantan créditos ni datos. |
| Costes y caja | §7 mantiene adquisición/activación, F_op, nominal y cash separados. Refunds se suman como R o restan de coste neto, una sola vez. Reservas y pagos no se duplican. Pérdida nominal no debita bankroll sin cargo externo real. |
| F03 / dependencias | §16 separa I2a FUNDED desde I0+perfil/origen, I2b dual desde I1+I2a e I3 desde capacidades de ambas etapas. No condiciona FUNDED aislada a resets de CHALLENGE. |
| Capas | §14.1 deja Strategy/MM/Provider/accounting/Platform/runner en sus owners. El reporter sólo proyecta eventos; no decide operaciones, financiación, lifecycle comercial ni PnL. No hay motor, DSL, DB o scheduler nuevo. |
| Pruebas causales | §12/17.4 y I0-S2 exigen oráculos independientes, command real, input intacto y sentinel no-spawn/egress. RC05/RC06/RC07 con scheduler/guard real y resume comercial no se declaran ejecutados por fixtures de proyección. |
| Legacy | §14/17 y I0-S1 protegen schema opt-in, 25%, 5.000/120/4 payouts e identidad de recibos. El nuevo reporte no alimenta silenciosamente el selector antiguo. Nuevos campos obligatorios faltantes no adquieren defaults legacy. |
| S04 | La reconciliación separa SOURCE demostrado de BUILD/TEST reportados, review completo no recuperado y aceptación semántica abierta. V1 catálogo/materializador no equivale a planes históricos efectivos ni a mismo intérprete. No se afirma que las 89 corridas cambiaron. |
| Permisos | I0-S1 tiene base, rama/WIP, presupuesto, Allowed Files, rollback y STOP. Sólo S1 está activo. Cero campañas/compras/trading/deploy; no promoción HISTORICAL_ONLY→LIVE ni autoaceptación. D01–D06/G0–G5 siguen explícitos. |

## Independencia del reporter y dependencias no bloqueantes

I0 no usa la paridad histórica como supuesto de verdad para calcular compras o payouts: recibe evidencia y conserva su procedencia/completitud. Una fila legacy recuperable puede proyectarse sin afirmar que un binario distinto produciría esa fila. Por ello S04-F01 limita el claim de equivalencia y las ejecuciones posteriores, no la posibilidad de escribir el adaptador/report.

S04-F02 no se declara resuelto por prohibir motores: el package exige no tocar run/resume y demostrar que el comando real no llega a ellos. El port/adaptación del guard sigue siendo trabajo explícito previo al lanzamiento. D05 tampoco se reemplaza por un payout ni por el nombre FUNDED/SIMULATION.

La ausencia de una evidencia S04 dentro de la pasada focal debe retornar UNKNOWN con dependencia exacta, tal como prescribe §17.5, y no detener la parte del reporter que tiene datos/contrato suficientes. Del mismo modo, un E2E sin artefacto recuperable queda no demostrado, nunca PASS. Ninguno de estos límites exige resolver I3/I4 para I0.

## Cierre de este apoyo

Hashes SHA-256 de los cuatro textos candidatos después de verificar la corrección del manager; prueban identidad de los archivos leídos, no pruebas físicas ni publicación remota:

| Archivo | SHA-256 |
|---|---|
| EF-CAMPAIGN-MODES-DESIGN.md | `f58d0b35454239e021b42d9e70f94a38984388d908b442a0f14234fe2b662862` |
| EF-CAMPAIGN-MODES-I0-LOCAL.md | `10c1638d9404a94f956e34a06b3b50f934719250b5264cc622e67eb45dc236b6` |
| EF-S04-INTEGRATION-RECONCILIATION.md | `d071ee9bca4b1d23d32876877e689a0f745654f2952ed9e7debc071e6e143bfe` |
| Echo Futures — Optimización de Campañas.md | `8f5be6963ed58983b1c06a044a7dd21ae7451b7f90d1365e542ce079cce2c8b2` |

- No edición de los candidatos, producto, remotos, gates ni planner. Único artefacto local: este memo temporal para disposición/persistencia del manager.
- Agent run: NOT_APPLICABLE según agents-os-agent-run-register; revisión de SPEC documental, sin segmento material de código implementado.
- Feedback: las primeras lecturas agrupadas generaron truncación de salida; se recuperaron las secciones decisivas mediante lecturas acotadas. Evidencia final suficiente para el alcance; sin nueva política ni promoción L3. El manager decide si ese feedback justifica persistencia de apoyo.
- Skills leídas: agents-os-agent-run-register, agents-os-session-feedback, agents-os-session-close. Cierre limitado a este worker ONE-SHOT; no cierre del manager/programa.
- Independencia: revisión de los textos candidatos sin coautoría ni edición sobre ellos en esta pasada; no prueba independencia histórica respecto de autores/revisores previos. INDEPENDENCE_HISTORY: UNKNOWN.
- PHYSICAL_VERIFICATION: NOT_EXECUTED. PRO_CHAT_POOL_DELTA: UNKNOWN. No SHA remoto propio.
- Siguiente acción mínima: entregar I0-S1 bajo los límites existentes; el writer puede desambiguar los dos puntos opcionales al persistir el handoff. No requiere otra revisión amplia ni resolver I3/I4. Este memo no concede OWNER_ACCEPTANCE ni un PASS físico.

### Identidad final tras aclaraciones del manager

| Archivo | SHA-256 final |
|---|---|
| EF-CAMPAIGN-MODES-DESIGN.md | `9e674f5f3f24ddb77095767cc184cd9571cbc7c485026ecf3d68241b37bde763` |
| EF-CAMPAIGN-MODES-I0-LOCAL.md | `a325afa72354d4f7368ce55a9c26d2f03fa5fbbc71f01bfdc3b0185c02369da9` |
| EF-S04-INTEGRATION-RECONCILIATION.md | `d071ee9bca4b1d23d32876877e689a0f745654f2952ed9e7debc071e6e143bfe` |
| Echo Futures — Optimización de Campañas.md | `8f5be6963ed58983b1c06a044a7dd21ae7451b7f90d1365e542ce079cce2c8b2` |

## Fuentes

- C01 original y C02 recuperados de Agents-OS; mandato funcional FUT-R01 vigente.
- Candidatos C03 y contraste económico del worker campaign_contract, referenciados en el memo con su alcance.
- Memo fuente del reviewer SHA256 `db8e1007eef8d8d237cd11d4726b1343eea1e77525c12430821002f827efa63d`; publicación por el manager como único writer, sin edición retrospectiva de su dictamen.
- [[2026-10-28-echo-campaigns-c03-manager-session-feedback]] y [[2026-10-28-echo-campaigns-c03-manager]].
