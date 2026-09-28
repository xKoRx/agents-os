---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures Architecture Candidate V1]]"
aliases: []
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-review
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D3 Astra Architecture Review

## Propósito

Revisión adversarial independiente de la arquitectura congelada D2 de Echo Futures. Fecha de referencia: **28 de septiembre de 2026**. Reviewer único: **Astra**, en esta sesión. El objetivo es evaluar si los contratos congelados bastan para construir el sistema correctamente; este informe no diseña sus correcciones ni modifica autoridades D2.

## Contenido

### 1. Alcance y baselines realmente utilizados

**Vault:** árbol limpio al inicio, commit `abc030d91cb69ff2907474b929af6397dbef9ed6`. Se leyó Architecture Candidate V1, el proyecto canónico y los seis workstreams D2-04..09; se siguieron secciones relevantes de sus children cuando definían el mecanismo cuestionado. Del D1 Analysis Pack se consultaron las decisiones de dominio y las referencias pertinentes de capacidades. Los cierres vigentes prevalecen sobre wording histórico expresamente superseded.

| Autoridad principal | Git blob del contenido revisado |
|---|---|
| [[Echo Futures]] | `8792b61ad4dc` |
| [[Echo Futures Architecture Candidate V1]] | `983b2ca0ad53` |
| [[Echo Futures — D2-04 Operation Order Fill Position]] | `2ca3abcd7f4e` |
| [[Echo Futures — D2-05 Instrument Session Provider]] | `c40a4cac90e6` |
| [[Echo Futures — D2-06 Market Runtime]] | `8bbf97f9c511` |
| [[Echo Futures — D2-07 Execution Runtime]] | `29561e6ac675` |
| [[Echo Futures — D2-08 Strategy Runtime]] | `ae736caf27cb` |
| [[Echo Futures — D2-09 Blocking Refactors]] | `8447a00e730a` |

**Echo source:** exclusivamente objetos de `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`, leídos mediante `git show <SHA>:<path>`. Se inspeccionaron puntualmente `v3/core/deploy/flink-statefun/develop/module.yaml`, `v3/sdk/kache/README.md` y `v3/sdk/kache/account_configs.go`. El checkout encontrado estaba en una rama feature con otro HEAD; no se utilizó ese contenido ni se auditó su delta. No se hizo fetch ni se afirma una nueva certificación de `master` remoto. El baseline solicitado sí existe localmente y fue el utilizado.

**Infraestructura:** se contrastaron las garantías pertinentes con documentación oficial de StateFun **3.2**, no con una versión actual asumida. No se accedió a DEV/PROD, no se enviaron órdenes y no se ejecutó una certificación física. Los escenarios siguientes son contraejemplos de contratos, no incidentes observados ni resultados de un simulador implementado.

**Independencia:** no se abrió el artifact D3 invalidado, no se recuperó desde Git ni se utilizó su contenido. La revisión fue realizada por un solo reviewer, sin delegación. No se modificaron D2 ni Echo source.

En este informe, **FACT** identifica lo escrito o demostrado por una fuente; **INFERENCE** identifica una conclusión derivada de esos hechos; **HYPOTHESIS** identifica una posibilidad pendiente de evidencia. Las cifras de los escenarios son ilustrativas y no representan parámetros de una prop concreta.

### 2. Veredicto ejecutivo

**La arquitectura D2 no es todavía un contrato suficiente para construir V1 con las garantías que declara.** Se identificaron **cinco findings HIGH y uno MEDIUM**, sin findings CRITICAL.

Los problemas materiales están en la composición de contratos: una identidad de mercado checkpointeada puede sobrevivir externamente a su rollback; las órdenes de reducción no tienen una cota conjunta demostrada; NET_ABS no trata correctamente salidas de Operations opuestas; la revalidación provider confunde una comprobación local con un punto de decisión account-keyed; y el replay no captura las versiones realmente observadas mediante lecturas pull. Además, el lifecycle de una apertura esperando admission no está cerrado frente a Signals posteriores.

No se demostró que Echo necesite un rewrite, que los boundaries Strategy/MM/Operation deban desaparecer, ni que 100–200 cuentas sean estructuralmente imposibles. La separación M1/M2, las capacidades obligatorias del adapter y el aislamiento del legacy son bases coherentes. Los findings tampoco se resuelven simplemente configurando correctamente EXACTLY_ONCE o certificando un venue: varios ocurren con Kafka, StateFun y venue funcionando conforme a sus contratos.

**No hay impedimento técnico para pasar a D4 como fase de corrección y adjudicación de estos findings. Sí hay impedimento para llevar D2 intacto a un freeze implementable o a V1.** Esta conclusión técnica no emite ni sustituye un gate del Primary Manager.

### 3. Findings ordenados por severidad

#### D3-01 — La identidad canónica de mercado puede reutilizarse después de un rollback

**SEVERITY:** HIGH · **AREA:** Market runtime / crash recovery / deduplication.

**CLAIM:** `stream_seq` generado en estado checkpointeado no basta para hacer idempotente un egress AT_LEAST_ONCE cuando una ejecución abortada ya publicó eventos y el orden de admisión puede cambiar al restaurar. El contrato no garantiza que un mismo `(stream_id, stream_seq)` conserve el mismo contenido a través de esa ventana.

**WHY IT IS A PROBLEM:** El guard downstream descarta cualquier `seq ≤ last_applied_stream_seq`, sin demostrar igualdad del evento. Kafka no elimina los records publicados por un egress no transaccional cuando Flink restaura su contador. Restaurar estado y mensajes internos no restaura un topic externo a su estado previo. Tampoco el journal transaccional conserva necesariamente la ejecución abortada que produjo esos records.

**BROKEN INVARIANT:** D2-06 I5/I6/I16: dedup sin pérdida de eventos legítimos, identidad canónica suficiente y contenido inequívoco para replay.

**CONCRETE FAILURE SCENARIO:**

1. El checkpoint conserva `stream_seq=100` y los guards downstream en 100.
2. Dos eventos físicos distintos, X e Y, pueden llegar desde candidates/control con orden de admisión no fijado por un único log recuperable. En el primer intento se admite X y se publica `X/101`.
3. El job falla antes de completar el checkpoint. `X/101` permanece en Kafka; el contador y el arbitraje vuelven al checkpoint.
4. En la restauración se admite Y antes que X y se publican `Y/101`, `X/102`. D2 no congela un orden total recuperable entre los inputs que concurren en esa isla.
5. El consumidor restaurado lee `X/101`, descarta `Y/101` por el guard y aplica `X/102`: pierde Y y cuenta X dos veces. El journal transaccional del intento exitoso puede referenciar 101 como Y, mientras el topic también contiene X con esa identidad.

El caso no exige que todo restart cambie de orden. Basta que un orden distinto esté permitido. Producer idempotence y orden de la partición de salida no comparan la identidad semántica de X/Y ni impiden reutilizar un contador restaurado.

**EVIDENCE:**

- **FACT:** D2-06A §17, líneas 422–445: candidates keyeados por `stream_id|source_id`, asignación de `stream_seq` en `echo/market_stream`, estado checkpointeado y egress canónico deliberadamente AT_LEAST_ONCE. Su §1, línea 51, justifica esa elección por latencia.
- **FACT:** D2-06 §6, líneas 209–223: el guard downstream usa `last_applied_stream_seq`; §18, líneas 633–641: journal transaccional; §22, líneas 767–790: contadores/estado checkpointeados y recording separado.
- **FACT:** StateFun distingue AT_LEAST_ONCE, que permite duplicados, de egress transaccional; su recovery restaura estado y mensajes. Véanse [Kafka egress, StateFun 3.2](https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/docs/modules/io/apache-kafka/#kafka-egress-and-fault-tolerance) y [fault tolerance, StateFun 3.2](https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/docs/concepts/application-building-blocks/#fault-tolerance).
- **INFERENCE:** no hay una prueba de identidad estable entre intentos abortados y recuperados; el contraejemplo invalida la suficiencia del guard, no AT_LEAST_ONCE como técnica general.

**AFFECTED AUTHORITY:** [[Echo Futures — D2-06 Market Runtime]] §§6, 18, 21–22; [[Echo Futures — D2-06A Market Feed Authority]] §17; [[Echo Futures — D2-09 Blocking Refactors]] §4.1, clasificación replay-stable de `stream_seq`.

**D2 DECISION CHALLENGED:** «AT_LEAST_ONCE + contador `stream_seq` checkpointeado = idempotencia canónica suficiente». Esto cuestiona una decisión deliberada de diseño, no la falta de configurar EXACTLY_ONCE en el deployment existente.

**BLOCKS V1?** YES · **CONFIDENCE:** alta sobre la insuficiencia del contrato; no validado mediante fault injection. · **TYPE:** INFERENCE.

#### D3-02 — La validación individual de reducciones permite invertir una Operation con órdenes válidas

**SEVERITY:** HIGH · **AREA:** Operation / MM / ForceClose / órdenes concurrentes.

**CLAIM:** Verificar `qty ≤ logical_exposure` para cada REDUCE/EXIT no evita que varias órdenes vivas consuman la misma exposición. D2 permite múltiples Orders vivas y atribuye al dedup/terminal guards una convergencia de cierres que esas técnicas no garantizan.

**WHY IT IS A PROBLEM:** Serializar la construcción no serializa la ejecución física. La primera reducción pendiente no disminuye la exposición hasta su Fill, por lo que la segunda puede aprobarse sobre el mismo saldo. `client_order_id` distintos representan dos órdenes legítimas para M2; ejecutar cada una exactamente una vez puede producir precisamente el exceso. Detectar el breach después conserva la verdad, pero no demuestra el invariante preventivo.

**BROKEN INVARIANT:** D2-04 I3 y §3.1: las Orders construidas por Echo no cruzan la dirección de la Operation. La excepción fail-visible para anomalías físicas no cubre dos órdenes correctamente ejecutadas que Echo emitió sin exclusión suficiente.

**CONCRETE FAILURE SCENARIO:** Una Operation LONG tiene exposición +1. MM ya emitió una EXIT SELL 1, todavía viva. Llega ForceClose: registra terminación, solicita cancelar la EXIT y produce otra SELL 1 para cerrar la exposición que aún observa. Ambas pasan la guard individual. La EXIT original gana la carrera al cancel; la nueva SELL también ejecuta. Resultado: `+1 −1 −1 = −1`. El venue no sobrellenó ninguna orden y no hubo redelivery duplicado. La Operation conserva dirección LONG y exposición negativa real; los guards terminales no deshacen el short.

La misma insuficiencia aparece con reducciones superpuestas de MM sin ForceClose. Un adapter con protección adicional podría evitar ciertos casos, pero D2 no exige una semántica de exclusión/reducción conjunta para todas las clases soportadas; MARKET/LIMIT/STOP y M2 no la implican.

**EVIDENCE:**

- **FACT:** D2-04 §2.2, líneas 77–78: validación individual y múltiples Orders vivas; I3, línea 168, repite la guard.
- **FACT:** D2-04 §3.1, líneas 133–135: ForceClose cancela Orders y emite cierres; afirma ausencia de cruce por construcción.
- **FACT:** D2-04 §11-R5, línea 368, sostiene que intents de cierre concurrentes convergen mediante idempotencia, dedup por client tag y terminal guards.
- **FACT:** D2-07 §7 y §§9–11 garantizan identidad/finality de cada comando; no establecen exclusión económica entre dos Orders distintas. El gate de close degradado de §12 no es una regla conjunta para cierres normales.
- **INFERENCE:** no existe en esos mecanismos una cota de reducciones ejecutables pendientes que haga verdadera la afirmación preventiva.

**AFFECTED AUTHORITY:** [[Echo Futures — D2-04 Operation Order Fill Position]] §§2.2, 3.1, 4, 11-R5; [[Echo Futures Architecture Candidate V1]] §4; [[Echo Futures — D2-08 Strategy Runtime]] §§10–11.

**D2 DECISION CHALLENGED:** suficiencia de `qty ≤ exposure` por Order y del dedup por identidad para asegurar convergencia de MM/safety. No se cuestiona conservar Fills reales ni se solicita auto-repair de Position.

**BLOCKS V1?** YES · **CONFIDENCE:** alta. · **TYPE:** INFERENCE.

#### D3-03 — Una salida por Operation puede aumentar NET_ABS y romper el cap reservado

**SEVERITY:** HIGH · **AREA:** Provider caps / exposición neta / múltiples AccountStrategies.

**CLAIM:** El diseño combina NET_ABS account-scoped con salidas que no reservan y nunca se bloquean por provider. Reducir una Operation no es monotónicamente reductor del neto absoluto de la cuenta. Por tanto, el envelope de reservas no acota todos los fills permitidos.

**WHY IT IS A PROBLEM:** `firm_by_operation` corrige la contabilidad después del Fill, pero no representa una salida en vuelo en el intervalo alcanzable. Además, un update retrasado de una salida puede subestimar NET_ABS; el skew no es siempre conservador como afirma D2. Este problema existe con exposición íntegramente atribuible a Echo y Position perfectamente conciliada.

**BROKEN INVARIANT:** D2-05C I-C2 y R2.5: cap seguro bajo cualquier ordering permitido y skew que sólo deniega de más. La contradicción es entre la métrica account-scoped y la clasificación local REDUCE/EXIT como reducción de riesgo universal.

**CONCRETE FAILURE SCENARIO:** Cap NET_ABS de 5 contratos en un mismo scope; inicialmente A tiene +4 y B tiene −4, neto 0. No se parte de un breach.

| Paso | Decisión/hecho | Neto / envelope |
|---|---|---|
| 1 | C solicita BUY 5; no hay otras reservas | `n=0, R+=5, R−=0`: GRANTED, extremo 5 |
| 2 | B cierra su short mediante EXIT BUY 4 | Salida sin reserva, permitida; C sigue autorizado |
| 3 | Ejecutan ambas BUY, en cualquier orden | A +4, B 0, C +5: neto +9 > cap 5 |

Los fills son exactos y normales. Si el Fill de B llega antes, su update puede revelar el problema, pero no elimina automáticamente la orden C ya ejecutable. Si llega después, el breach ya existe. `PHYSICAL_STATE_UNTRUSTED` por mismatch no previene el caso: el neto físico y el lógico pueden coincidir durante toda la secuencia.

**EVIDENCE:**

- **FACT:** D2-05 §§15–16, líneas 299–305 y 311–320: updates por Fill, métricas y releases; §12, línea 136: salidas nunca bloqueadas.
- **FACT:** D2-05C R2.3, líneas 129–135: intervalo NET_ABS basado en net firme y reservas vivas; §9, línea 326: reducciones no reservan y liberan capacidad sólo por sus fills; §6, línea 304: gates sólo sobre nuevo riesgo.
- **FACT:** D2-05C R2.5, línea 150, afirma skew exclusivamente fail-safe; D2-05 §1, línea 49, integra ese claim.
- **INFERENCE:** el contraejemplo conserva todos los invariantes locales de cantidad y dedup, pero rompe la cota account-wide.

**AFFECTED AUTHORITY:** [[Echo Futures — D2-05 Instrument Session Provider]] §§12, 15, 20, 23; [[Echo Futures — D2-05C Provider Program Rules]] R2.3/R2.5 y §9; [[Echo Futures Architecture Candidate V1]] §7.

**D2 DECISION CHALLENGED:** «salida de Operation = liberación conservadora de capacidad» para todas las métricas. No afecta la validez de sumar absolutos por Operation para GROSS; sí invalida la garantía universal para NET_ABS y GROUP_WEIGHTED cuando utiliza netos.

**BLOCKS V1?** YES · **CONFIDENCE:** alta; contraejemplo aritmético directo. · **TYPE:** INFERENCE.

#### D3-04 — La revalidación pre-egress no tiene el punto de autoridad que declara

**SEVERITY:** HIGH · **AREA:** Provider hot updates / grants / autoridad distribuida.

**CLAIM:** El egress guard corre en `echo/operation` y sólo solicita `ReservationRevalidate` si detecta un cambio de epoch. La autoridad corriente vive en otra key, `echo/provider_rules(account_id)`. El contrato no demuestra cómo la rama «epoch no cambió» conoce el estado vigente de ese owner; sin ese conocimiento, puede omitir precisamente la revalidación necesaria.

**WHY IT IS A PROBLEM:** Una comparación contra un snapshot local prueba lo observado por Operation, no lo ya procesado por provider_rules. D2-05C afirma que detección y decisión ocurren en el mismo punto serializado account-keyed, mientras el flujo integrado coloca la detección en otro owner. El mismo riesgo existe para suspensión/entitlement usando el admission snapshot del guard.

**BROKEN INVARIANT:** D2-05C I-C7 y C-R3: un grant todavía no emitido debe satisfacer la autoridad vigente en el punto de linearización account-keyed; kache no sustituye aceptación autoritativa.

**CONCRETE FAILURE SCENARIO:**

1. `provider_rules` concede qty 5 bajo v5/cap 10; el result va hacia Operation.
2. `provider_rules` procesa v6/cap 3 antes del egress-check. La publicación/entrega de v6 hacia la vista local de Operation va atrasada.
3. Operation recibe el grant v5 y compara con su vista v5: «no cambió», por lo que no envía `ReservationRevalidate`.
4. Emite qty 5. Esto no es el caso tolerado de «v6 aún no llegó al authority owner»: en el escenario sí fue procesada allí.

No se exige simultaneidad global ni revocar retrospectivamente una orden ya física. El problema es que la arquitectura afirma un punto de decisión que su protocolo no obliga a atravesar para grants sin cambio local visible.

**EVIDENCE:**

- **FACT:** D2-05 §15, líneas 242–256: Stage-2 y egress guard en Operation; revalidación condicional por epoch.
- **FACT:** D2-05C, líneas 176–177: guard con admission snapshot kache-fed y revalidación sólo si cambia authority/epoch.
- **FACT:** D2-05C C-R3.6 y «Linearization point», líneas 220–227: exige que si v6 ya fue procesada por provider_rules, el egress-check use v6; afirma detección y decisión en el mismo punto serializado.
- **FACT:** D2-05 R15 y §14 eliminaron kache como autoridad de Stage-1, pero no aportan una barrera equivalente para la rama condicional de Stage-2.
- **INFERENCE:** el flujo admite el tercer caso omitido por la demostración C-R3: owner actualizado, consumidor del grant aún desactualizado.

**AFFECTED AUTHORITY:** [[Echo Futures — D2-05 Instrument Session Provider]] §§14–15, 17; [[Echo Futures — D2-05C Provider Program Rules]] C-R3.6; [[Echo Futures — D2-09 Blocking Refactors]] §13; [[Echo Futures Architecture Candidate V1]] §7.

**D2 DECISION CHALLENGED:** detección local de epoch como condición suficiente para decidir si se consulta la autoridad serializada. El hallazgo no cuestiona el Stage-1 request/response ya reparado.

**BLOCKS V1?** YES · **CONFIDENCE:** alta sobre la contradicción de ownership/protocolo. · **TYPE:** INFERENCE.

#### D3-05 — El journal por isla no identifica las vistas pull observadas por Strategy

**SEVERITY:** HIGH · **AREA:** EXACT_REPLAY / MarketContext / read models compartidos.

**CLAIM:** Grabar el orden de inputs y la posición del emisor de cada delivery no determina qué versión de otro read model compartido leyó una evaluación. D2 permite lecturas pull de current-state/bars y afirma que su fidelidad se obtiene automáticamente del journal por isla; esa afirmación es falsa sin un vínculo entre lectura y versión observada.

**WHY IT IS A PROBLEM:** El orden del producer no fija cuándo su snapshot llega a la caché de un consumidor. `source_ref` identifica el evento que disparó la evaluación, no necesariamente las versiones de todos los streams/timeframes leídos durante ella. Dos ejecuciones con iguales journals de dominio pueden diferir sólo en propagación de caché y producir Signals distintas. Conocer el digest de la decisión permite detectar divergencia, pero no reconstruye el input ausente.

**BROKEN INVARIANT:** D2-06 I16/I19 y §19; D2-08 §17: manifest + anchor + journals + contenido + mismo código deben reproducir las mismas Signals, dentro del boundary de mercado V1.

**CONCRETE FAILURE SCENARIO:** Una Strategy bars-only evalúa al cierre NQ y consulta como contexto la última barra de ES. Analytics ES produjo X y después su corrección X′, ambos reconstruibles y con el mismo orden journalado. En el run live, X′ ya existe en el producer pero todavía no llegó al kache utilizado por Strategy: la evaluación lee X. En otro schedule de propagación, con los mismos inputs admitidos, el mismo trigger NQ y el mismo `source_ref`, lee X′. Esa lectura no es otra delivery a Strategy. El replay sabe reconstruir X y X′, pero el contrato grabado no permite escoger cuál observó la evaluación original.

Esto tampoco se limita al replay de ejecución que D2 difirió: el ejemplo cambia la **Signal de Strategy**, expresamente incluida en EXACT_REPLAY V1. La notificación ligera de MM seguida de lectura de «estado actual» reproduce la misma clase de dependencia, aunque el replay completo de MM permanezca fuera de scope.

**EVIDENCE:**

- **FACT:** D2-06B §§14/22/25, líneas 244, 329 y 402–403: lectura de current-state/otros timeframes mediante snapshots/kache; los cierres son triggers push.
- **FACT:** D2-06C §10, líneas 203–207: journal de delivery con posición del emisor; afirma que las lecturas pull cross-stream son exactas «sin trabajo adicional». §15, líneas 277–282, define referencias al evento y emisor, no un read-set de versiones observadas.
- **FACT:** D2-08 §12, línea 245: la notificación de MM sólo porta identidad; la decisión lee el estado actual desde el read model compartido.
- **FACT SOURCE:** `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`, `v3/sdk/kache/account_configs.go:38–54, 98–132`: caché en memoria con consumer propio en background; su README describe latest-value por key. Esto verifica el patrón reutilizado, no afirma que el futuro market cache ya exista.
- **INFERENCE:** serialización de cada owner y reproducibilidad del producer no equivalen a reproducibilidad de una observación eventual del consumidor.

**AFFECTED AUTHORITY:** [[Echo Futures — D2-06 Market Runtime]] §§14, 17–19; [[Echo Futures — D2-06B Bars Hot State Warmup]] §§14, 22–25; [[Echo Futures — D2-06C Live Replay Market Boundary]] §10; [[Echo Futures — D2-08 Strategy Runtime]] §§12, 17.

**D2 DECISION CHALLENGED:** suficiencia del journal de orden y `source_ref` de deliveries para reproducir lecturas pull arbitrarias. No se cuestiona compartir market state ni se exige un orden global.

**BLOCKS V1?** YES, para la garantía EXACT_REPLAY de Strategy declarada en V1. · **CONFIDENCE:** alta. · **TYPE:** INFERENCE.

#### D3-06 — Falta el lifecycle de una OPEN que espera AdmissionResult

**SEVERITY:** MEDIUM · **AREA:** Signal ordering / pre-materialización / continuaciones asíncronas.

**CLAIM:** Stage-1 introduce una continuación asíncrona antes de crear Operation, pero las reglas de ciclo sólo cubren Operations existentes y un ciclo futuro diferido mientras otra termina. No queda definido cómo CLOSE/CLOSE_ALL y OPENs posteriores afectan una apertura cuyo AdmissionRequest está en vuelo.

**WHY IT IS A PROBLEM:** Preservar el orden de llegada de las Signals no preserva automáticamente el orden de sus efectos cuando una de ellas espera respuesta de otro owner. El no-op de gestión sin Operation puede consumir un CLOSE mientras el OPEN previo sigue pendiente, y las guards enumeradas al recibir ALLOW no incluyen la invalidación por ese cierre. Es una brecha de contrato resoluble sin cambiar los boundaries generales; no demuestra que toda implementación vaya a elegir el comportamiento inseguro.

**BROKEN INVARIANT:** D2-08 §§5/7/16: aplicación determinística y ordenada del ciclo técnico en AccountStrategy; un CLOSE posterior no debe quedar neutralizado por materialización tardía de su OPEN anterior.

**CONCRETE FAILURE SCENARIO:**

1. `OPEN(k)` llega a una key vacía, pasa guards y envía AdmissionRequest; todavía no existe Operation.
2. `CLOSE_ALL(k)` llega después, respetando el orden de Signals. La regla de gestión sin Operation produce no-op/fail-visible.
3. Llega ALLOW del OPEN original. La Signal sigue vigente, el binding sigue enabled y nunca se materializó k.
4. Si se aplican sólo las guards enumeradas, nace Operation(k) y puede abrir exposición después de haber procesado su cierre. `last_materialized_cycle_seq` no lo impide porque k aún no se materializaba.

La otra interpretación posible —retener las Signals posteriores o invalidar la continuación— no está especificada como transición obligatoria para esta fase. Esa ambigüedad debe resolverse antes de implementar el lifecycle, no mediante una suposición del adapter.

**EVIDENCE:**

- **FACT:** D2-05 §14, líneas 194–222: request/response pre-materialización y re-chequeo de valid_until/binding después de ALLOW.
- **FACT:** D2-04 §3.1, línea 137; D2-08 §7, línea 184: gestión de un ciclo sin Operation es no-op/fail-visible.
- **FACT:** D2-08 §7, líneas 175–180: `last_materialized_cycle_seq` y buffer futuro definidos alrededor de una Operation existente, sin fase de admission pendiente equivalente.
- **FACT:** D2-08 §16, línea 285: Signals y responses de provider participan de owners/colas distintas. La serialización de una invocación no declara una transacción lógica que dure hasta recibir una respuesta.
- **INFERENCE:** el contrato admite interpretaciones con efectos diferentes ante la misma secuencia. No se encontró una regla vigente que cierre el caso pre-Operation.

**AFFECTED AUTHORITY:** [[Echo Futures — D2-05 Instrument Session Provider]] §14; [[Echo Futures — D2-04 Operation Order Fill Position]] §3.1; [[Echo Futures — D2-08 Strategy Runtime]] §§7, 16.

**D2 DECISION CHALLENGED:** considerar completo el orden de lifecycle mediante FIFO de Signals + buffer de un ciclo futuro, sin definir la continuación de Stage-1 ante gestión posterior.

**BLOCKS V1?** YES, hasta cerrar la ambigüedad de lifecycle. · **CONFIDENCE:** alta sobre el contrato incompleto; media-alta sobre la traza si se implementan literalmente las guards enumeradas. · **TYPE:** INFERENCE.

### 4. Contradicciones entre artifacts

| Cruce | Contradicción o insuficiencia | Resultado de revisión |
|---|---|---|
| D2-06A §17 / D2-06 §6 ↔ D2-09 §4.1 | Secuencia restaurable publicada AT_LEAST_ONCE se clasifica como identidad suficientemente estable | D3-01 |
| D2-04 I3/§3.1 ↔ §2.2/§11-R5 | No reversal por construcción frente a múltiples reducciones vivas y dedup por Order | D3-02 |
| D2-05C R2.3/I-C2 ↔ §9/I-C6 | Envelope NET_ABS universal frente a salidas sin reserva | D3-03 |
| D2-05 §15 ↔ D2-05C C-R3, linearization point | Egress-check local condicional descrito como decisión account-keyed | D3-04 |
| D2-06C §10 ↔ D2-06B lecturas kache / D2-08 §12 | Journal de deliveries se considera suficiente para lecturas pull independientes | D3-05 |
| D2-05 Stage-1 ↔ D2-04/D2-08 ciclo sin Operation | Continuación ALLOW sin transición definida frente a CLOSE ya recibido | D3-06 |

Se descartaron como defectos nuevos varios desalineamientos históricos que sí tienen autoridad posterior suficiente:

- D2-04 enumera guards terminales sin explicitar finality en todos sus resúmenes, pero **D2-07 §11 y D2-07A §16 sí exigen `TERMINAL_EXECUTION_FINAL` para terminalizar Operation**. No se reporta «cancel ACK equivale a terminalidad» como finding vigente.
- El child D2-07C tiene wording antiguo sobre retorno de cinco familias. D2-07 integrado §§8/17 lo corrige expresamente mediante tres caminos. No se atribuyó Position ni readiness a Operation.
- Las referencias históricas a `orderId:seq` y a implementar Reference→Signal en V1 están corregidas por los cierres D2-08/D2-09 y Candidate. No se reabren.
- Entitlement revocado tiene suspensión explícita de automatización y operador; el principio general de no bloquear salidas no se interpretó como autorización para operar sin entitlement.

### 5. Invariantes relevantes que fueron desafiados

| Invariante | Evaluación |
|---|---|
| Un solo writer de estado por owner/key | Coherente localmente; no demuestra por sí solo corrección entre owners. D3-04/D3-06 identifican las brechas concretas. |
| Una Operation no terminal por AccountStrategy | Coherente para el lifecycle materializado y el ciclo futuro diferido; admission pendiente requiere precisión adicional. |
| Dirección inmutable y Fills sin clamp | La representación es correcta; la prevención de reversal por Orders propias es insuficiente: D3-02. |
| Position no atribuye Operations | Conservado. No se propuso netear ni reparar Operations mediante Position. |
| M1 separada de M2 | Coherente bajo sus condiciones declaradas. No se equiparó Kafka exactly-once con ejecución física exactly-once. |
| No blind retry; ambiguity fail-closed | Boundary viable por contrato; la selección real debe demostrar sus capacidades en D6. |
| Finality antes de liberar/terminalizar | Existe obligación explícita vigente en D2-07. El caso de un venue que contradiga evidencia final queda residual. |
| Caps account-wide seguros con múltiples Strategies | Refutado para NET_ABS por D3-03; hot revalidation insuficiente por D3-04. |
| Fuente/Contract separados; rollover sin retarget | Pin del Contract de Operation coherente; se mantienen los límites de divergencia de mappings y los gaps indicados abajo. |
| Barra cerrada observada X no se reevalúa por corrección X′ | Coherente para la delivery push de cierre; no resuelve las lecturas laterales de D3-05. |
| Calendario separado de DayBoundary y provider windows | Coherente conceptualmente. No se detectó contradicción material que obligue a fusionarlos. |
| Misma lógica de dominio LIVE/BACKTEST | Paquetes puros y clock inyectable permiten reutilización; la equivalencia exacta del run live tiene las limitaciones D3-01/D3-05. |
| Market/Strategy no se multiplican por cuenta | Se conserva estructuralmente; el costo N de MM y ejecución está reconocido. No se certificó throughput. |
| Incrementalidad y KISS/YAGNI | No se encontró necesidad demostrada de event sourcing global, portfolio engine, saga global, DSL ni framework adicional. |

### 6. Evidence gaps reales

**Los seis findings cuentan con evidencia contractual; los siguientes puntos no se elevan a defectos confirmados.**

1. **Hot rebind y exposición que sobrevive a una Order terminal.** D2-07 §18 y D2-07C §16 pinnean Orders físicas al binding anterior, mientras nuevas submissions van al nuevo. No queda suficientemente explícito si se prohíbe cambiar la identidad de la cuenta física subyacente durante una Operation, ni cómo se enruta una EXIT nueva de exposición abierta por una ENTRY ya terminal. Si el rebind puede cambiar de cuenta física, hay una hipótesis material de cierre en el destino equivocado; si sólo cambia el acceso a la misma cuenta física, ese escenario no se sigue. Falta esa restricción de identidad para decidir. **TYPE: HYPOTHESIS.**
2. **Precios técnicos durante divergencia feed/execution de Contract.** D2-05A §5/§13-R-A admite explícitamente distintos vencimientos y lo declara riesgo operacional; D2-03 permite niveles absolutos en `Signal.details`. No se dispone todavía del contrato concreto Strategy↔MM que demuestre cómo una Strategy basada en un vencimiento evita interpretar sus niveles como precios del otro. No se rechaza la decisión owner ni se impone una conversión: la compatibilidad debe quedar demostrada en el caso concreto. **TYPE: HYPOTHESIS**, adicional al riesgo aceptado de mapping divergente.
3. **Capacidad real de transport.** Ningún resultado obtenido en esta revisión certifica negative lookup, native idempotency, scope de execution identity, horizonte de history, finality o entitlement de un transport. Son pruebas D6 ya declaradas, no nuevos findings. El adapter real puede quedar legítimamente excluido si no las cumple.
4. **Certificación física del runtime.** Faltan las pruebas ya previstas de deployment EXACTLY_ONCE/read_committed, retención, fsync/corrupción, fallos de projector, clock/calendar release y carga de 200 cuentas. El source inspeccionado sólo confirma el patrón/baseline, no su comportamiento futuro. Esos gaps no invalidan por sí solos D2, pero tampoco corrigen los contraejemplos contractuales.

### 7. Riesgos residuales que no constituyen findings

- **Disponibilidad de M2:** fail-closed ante ambigüedad puede mantener una cuenta suspendida hasta intervención; es una elección explícita, no falso HA. La regla de no takeover automático limita split-brain dentro del scope operacional aceptado.
- **DR sin checkpoint:** `COLD_RECOVERY_REQUIRED` reconoce que PG no reconstruye MM. No se exigió recovery exacto desde una proyección eventual.
- **Fuentes clase C y backup:** no siempre existe historia suficiente para reconstruir; `ANALYTICAL_REBUILD_UNPROVABLE` y bloqueo del switch incapaz de servir Contracts demandados son comportamientos reconocidos.
- **Latencia y escala:** checkpoints de comandos, hops admission/reservation, notificaciones MM opt-in, consumer-per-account, journal I/O y reconnect storm requieren medición. El requisito de 200 cuentas no se convierte en prueba por contar keys, pero tampoco se refuta sin carga o un límite estructural concreto.
- **Finality y actividad externa:** un venue que contradice su evidencia final o actividad manual no correlacionable pueden producir mismatch. D2 preserva hechos y falla visible; esta revisión no reabre la política avanzada de reconciliation.
- **Retención y tzdata:** exact replay depende del corpus y de las mismas semánticas de código/calendario conservadas durante el horizonte declarado. No se exige replay después de purgar sus fuentes ni igualdad entre reglas civiles de releases diferentes.
- **Deudas owner:** permanecen fuera de esta revisión como blockers por sí solas Reference→Signal completo, props Forex, reutilización cross-market, Trade/The Lab, Q12/Q13 y la política avanzada de Position mismatch.

### 8. Tabla resumen de findings

| ID | Severidad | Problema | Tipo | Confianza | ¿Bloquea V1 sin resolver? |
|---|---|---|---|---|---|
| D3-01 | HIGH | Identidad `stream_seq` reutilizable tras rollback con egress AT_LEAST_ONCE | INFERENCE | Alta | YES |
| D3-02 | HIGH | Reducciones concurrentes pueden invertir la exposición | INFERENCE | Alta | YES |
| D3-03 | HIGH | Salidas por Operation rompen la cota NET_ABS | INFERENCE | Alta | YES |
| D3-04 | HIGH | Egress-check local puede omitir revalidación contra autoridad actual | INFERENCE | Alta | YES |
| D3-05 | HIGH | Replay no identifica las versiones de read models observadas por Strategy | INFERENCE | Alta | YES |
| D3-06 | MEDIUM | OPEN pendiente de admission sin semántica completa frente a CLOSE posterior | INFERENCE | Alta en el gap; media-alta en la traza | YES |

**Conteo:** CRITICAL 0 · HIGH 5 · MEDIUM 1 · LOW 0. No se usaron hipótesis para aumentar el conteo de findings.

### 9. Conclusión sobre continuidad hacia D4

**Se puede continuar técnicamente hacia D4 para corregir y resolver los findings. No se puede considerar D2 congelado suficiente para construir V1 sin cambios.**

Los defectos identificados no requieren por sí mismos un rewrite ni justifican introducir los frameworks excluidos por el proyecto. Sí impiden conservar, sin revisión, las garantías actuales de deduplicación de mercado, no reversal por Orders propias, caps NET_ABS, revalidación provider y EXACT_REPLAY de Strategy. D3-06 requiere cerrar una ambigüedad antes de que decisiones de implementación definan accidentalmente el lifecycle.

La adjudicación de cada finding y cualquier decisión de gate corresponden al Primary Manager. Este informe termina en la evaluación técnica y no abre ni ejecuta D4.

## Fuentes

- Corpus principal y blobs: §1. Las referencias `§` y líneas de findings corresponden a esas versiones, no a artifacts futuros corregidos.
- Children consultados: [[Echo Futures — D2-05A Instrument Contract]] (`6eb671f2466c`), [[Echo Futures — D2-05B Session Calendar]] (`8058aec0edbf`), [[Echo Futures — D2-05C Provider Program Rules]] (`637c62b810ec`), [[Echo Futures — D2-06A Market Feed Authority]] (`3bd67eaa67a7`), [[Echo Futures — D2-06B Bars Hot State Warmup]] (`72ce7ac45f43`), [[Echo Futures — D2-06C Live Replay Market Boundary]] (`e803fa2ef290`), [[Echo Futures — D2-07A Execution Adapter Contract]] (`ab978a389714`), [[Echo Futures — D2-07C Execution Runtime Topology]] (`75ee930dc0f0`).
- D1 consultado de forma puntual: [[Echo Futures — D1 Analysis Pack]] (`77ea051cdcf3`). Los SPECs históricos Simulator/Topstep no se usaron como arquitectura vigente.
- Source físico: `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360`, paths y alcance descritos en §1 y D3-05. No se atribuyen capacidades Futures implementadas al source legacy.
- Documentación primaria consultada el 2026-09-28: [Apache Kafka I/O — StateFun 3.2](https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/docs/modules/io/apache-kafka/) y [Application Building Blocks — StateFun 3.2](https://nightlies.apache.org/flink/flink-statefun-docs-release-3.2/docs/concepts/application-building-blocks/). No se derivaron conclusiones de los enlaces Javadoc que no fueron accesibles durante la revisión.
