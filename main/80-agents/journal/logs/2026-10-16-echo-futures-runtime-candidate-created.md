---
type: change_log
schema_version: 1
scope: session
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Futures — candidato runtime creado y actualizado

## Cambio

Nota afectada: `10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md`. Estado vigente **CANDIDATO_R5 / LISTO_PARA_REVISIÓN_DEL_OWNER**. R1–R4 conservados en Git como historia, no políticas alternativas vigentes. Escrituras en master de Agents-OS; no ramas/PRs de documentación, no implementación ni cierre.

## Motivo

El asistente confundió afinidad permanente con turno diario y en R4 impidió rotar cuentas pausadas. El Owner corrigió explícitamente: daily DD/daily target pausa UNA cuenta; la MISMA Strategy continúa en otra en la MISMA sesión. Al siguiente día se vuelve a la cuenta elegible más antigua ya asignada a esa Strategy. La generación de señales nunca se pausa por el estado de las cuentas. La interpretación R4 era incorrecta y no debe implementarse.

## Fuentes usadas

Mandato inicial PROMPT_VERSION1 y aclaraciones del Owner de esta conversación del2026-10-16. El mandato inicial ya describía el paso a otra cuenta en la misma sesión al pausar la anterior y la independencia de analytics.

R5 no vuelve a inspeccionar producto ni WIP. Conserva evidencia anterior: Echo@95e9d105182af99d03700f4b5def24bf9fc6b5fd; Signal en domain/signal.go blob9cb6d0810fdf5437d5972804e3f015c7514be6f6; fanout.go blob100a9e72b32158d8b87e2521b265d1d4428ead8c; Architecture V2 blobbfccbb8289d8a8896ecbdb921f61cacd5506e95f; Technical SPEC bloba37ba7c2666ecb35ec59da2a8ca9ac48e190e77b; D2-08 blobae736caf27cb028b69a1260de8e35cc3fcd03a16.

Antecedentes económicos R3: TGMM blobeb2824a470d27d63d93c856f4a0829d4526d367b; platform_operability blob52710c0494dd375745aeb8c3dce85386ec36265e; minimum_policy blob9ace5fdbff3f6b2d506c9e769cc29236de9d54cf; TG-FLOW blob7af1b9a9fe1a471ebe0f5e048379c8c0400dd7fb. No nuevas conclusiones sobre esos cortes ni bloqueos al trabajo paralelo.

## Resolución aplicada

### R5 vigente

- Afinidad cuenta→Strategy permanece a través de pausas/días/reinicio: cuenta de A nunca pasa a B.
- Turno termina también por daily DD/daily target. Tras resolver órdenes/exposición salientes, otra cuenta propia elegible o libre compatible más antigua continúa ESA Strategy en la misma sesión.
- Nueva jornada: se vuelve a la propia elegible más antigua y se repite la secuencia diaria; no conservar la última de ayer por inercia. Reset de selección no resetea economía, pisos ni afinidad.
- Strategy y analytics continúan evaluando/publicando independientemente de cuentas. No destino elegible es falta de ejecución física, no pausa de Strategy ni permiso para fabricar señales/fills.
- La nota maestra reemplaza las restricciones incorrectas de R4 en tabla, modelo, protocolo, lifecycle y pruebas, no sólo en un addendum contradictorio. La prueba crítica incluye C01→pausa→C04 el mismo día y retorno a C01 al día siguiente.
- Cinco cuentas es soporte/cohorte, no garantía de utilización. Runtime y backtester mantienen sus ramas independientes y adaptación gradual posterior.

### Historia relevante

R2 introdujo pool–Strategy–MM, FIFO, concurrencia y AccountStrategy automático; R3 confirmó afinidad permanente, retiró contexto de cuenta de Strategy y fijó presupuesto completo pese al remanente. R4 recuperó correctamente Signal/SignalDelivery/strategy_cycle_seq existentes y el antecedente ReferenceEvent→Signal, pero interpretó MAL permanencia como ausencia de rotación diaria. R5 conserva la recuperación canónica y corrige esa interpretación.

En R4 una búsqueda ReferenceEvent sin resultados y un path supuesto signal_delivery.go con404 no se usaron como prueba de ausencia: las fuentes reales fueron D2-08, Signal, fanout y SPEC. Tampoco se certificó el adaptador Forex.

No se modifican controles TradesGerard, ramas de producto, infraestructura ni campañas. No dispatch ni cierre de sesión. No promesa de plazo o rentabilidad.

## Validación

**Límite R1 conservado:** creación vía conector, sin ejecutar materializador/lint. La primera versión del registro atribuyó por error validaciones y equivalencia byte-identical no realizadas; fue corregida en la misma sesión. Materialización canónica, gate por tipo y lint automatizado siguen NOT_RUN; readback documental no los sustituye.

Historial:

- R1 diseño commit b9eb613dcb5cb6c33408bff5e72f4dfa2c295f9e, blob015e02a29ee96d88f8c907da2772ad1060411d92. Registro inicial commit9b0839c2ed22167daeb0429ddf9f63ad2f7c5276, blobe70598bdce6a68283f82350b930ef7c65dd5557c, leído antes de corregir validaciones.
- R2 diseño e076fdeb5231f50ce74481cf1459191ac94ff50c /09f66b257d9d176960af8d8a0e04a4df3c4dfa7d. Registro c5643616b0326ed3ad7a348489e86a9e4e193e8b /e40314245fc69bbd2aa5a2b0496b4c98f356afc1.
- R3 diseño3dc493ecbe38c6738c6737720922df8d24d244a7 /deca8de9c5555285c884f66d5cdd96890a8652fa. Registro55341fc52c055205c49cac1485482f99dd853f8c /a6129be701636109cb6d6abcdc647b5eb8af70bc.
- R4 diseñob063ceb218779dd3c8e81310590d0557b6354558 /17caab4ec25f38aea1eea9a8d325617fc4c8371a. Registrodb8e5e1e1e86df2d81abf57b14b1152452b648c2 /2b6565888200790865af85ad2b2bb4abe3b55474, leído en R4 antes de esta actualización por su SHA.
- R5: lectura actual de nota confirma blob R4 sin cambios concurrentes. Actualización con ese SHA: commit7d2535e7f69e9201ce13e61d5a804e1b68005f32 /blob4b2855e8c365b16241a2759a65cd6f3962b60a43. Readback17–46 confirma R5, rotación por daily pause, vuelta diaria a más antigua propia e independencia de Strategy; SHA coincide con escritura. Este registro se actualiza por su SHA previamente leído y con control de concurrencia.

No producto/scripts/tests/campañas/órdenes/deploy ejecutados; las pruebas de la nota son requisitos, no PASS. No verificación byte a byte local ni lint.

## Compartibilidad

Scope local; sin secretos, tokens, endpoints operativos ni razonamiento privado. C01..C05 son alias de ejemplo, no un inventario descubierto.

## Rollback

Conservar R5 como autoridad de la aclaración del Owner. Una restauración documental técnica debe preservar esta corrección y cambios concurrentes, nunca volver a introducir como vigente la retención incorrecta R4. No revertir producto ni modificar controles backtester. No cierre/feedback automático.
