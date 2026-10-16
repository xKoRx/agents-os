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

Creación y actualizaciones de `10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` por mandato Owner del 2026-10-16. Versiones históricas R1–R3 no aceptadas; estado vigente **CANDIDATO_R4 / LISTO_PARA_REVISIÓN_DEL_OWNER**. No aceptación propia, implementación, cierre de proyecto ni de sesión. Escrituras documentales directamente sobre master de Agents-OS; sin ramas ni PRs.

## Motivo

Mantener una autoridad runtime separada de los controles de backtester. El cuarto turno exige recuperar el nombre canónico ya definido, conservar la cuenta hasta pérdida/pase (no rotar por pausa), retirar el objetivo inventado de utilización de cinco cuentas y permitir evolución paralela en dos ramas de producto con adaptación posterior del backtester.

## Fuentes usadas

Mandato adjunto PROMPT_VERSION 1 y cuatro turnos explícitos del Owner. R1/R2 leyeron Echo `0c4aae552176fda005c44766e24dd70e8c48e589`; R3 resolvió `95e9d105182af99d03700f4b5def24bf9fc6b5fd`, dos commits adelante, y examinó sólo cambios de presupuesto/operabilidad. R4 vuelve a resolver master en ese mismo SHA.

Lecturas R4 adicionales:

- `v3/sdk/futures/domain/signal.go`: Signal, SignalDetails, SignalProvenance, StrategyCycleSeq, DeriveSignalID; blob `9cb6d0810fdf5437d5972804e3f015c7514be6f6`.
- `v3/sdk/futures/strategy/fanout.go`: AccountStrategyTarget, ApplyTargetSet, Linearize y llamada DeliveryFromSignal; blob `100a9e72b32158d8b87e2521b265d1d4428ead8c`.
- Architecture Candidate V2 §1–2.5, blob `bfccbb8289d8a8896ecbdb921f61cacd5506e95f`; Technical SPEC V1 §3 y §9–11, blob `a37ba7c2666ecb35ec59da2a8ca9ac48e190e77b`; D2-08 Strategy Runtime, sección inicial del documento del 2026-09-28, blob `ae736caf27cb028b69a1260de8e35cc3fcd03a16`.

Las búsquedas lexicales de ReferenceEvent no devolvieron resultados; eso no se trató como prueba de ausencia. El nombre y su antecedente se recuperaron directamente de D2-08. Un intento de abrir un path supuesto signal_delivery.go retornó404; la evidencia real de deliveries es fanout.go y la SPEC, no ese path.

Antecedentes R3 conservados: TGMM blob `eb2824a470d27d63d93c856f4a0829d4526d367b`, platform_operability blob `52710c0494dd375745aeb8c3dce85386ec36265e`, minimum_policy blob `9ace5fdbff3f6b2d506c9e769cc29236de9d54cf`, TG-FLOW blob `7af1b9a9fe1a471ebe0f5e048379c8c0400dd7fb`. No reauditoría ni ejecución de campañas en R4. La investigación comercial retirada por el Owner no se repitió; referencias públicas previas no se presentan como nueva verificación.

## Resolución aplicada

### Estado vigente R4

- La entidad es **Signal**, el delivery es **SignalDelivery** y el ciclo técnico es **strategy_cycle_seq**. Están en source y documentación; no se perdieron. D2-08 ya descartaba StrategyTrade/operation_key y documentaba el seam legacy ReferenceEvent→Signal. La imprecisión fue del análisis, que trató un contrato existente como pendiente. No se afirma haber ejecutado/verificado el adaptador Forex.
- Cuenta que operó A conserva afinidad A; ahora se precisa además que la asignación activa permanece durante pausas/días y sólo rota automáticamente por pérdida/pase de challenge tras drenaje. Se elimina la recomendación anterior de cambiar de cuenta por pausa diaria o cierre de sesión.
- Cinco cuentas es capacidad/cohorte, no obligación de cinco trades. Se retiran pools/asociaciones adicionales propuestos sólo para garantizar utilización. El usuario puede gestionar manualmente cuentas no utilizadas, sin coexistencia con autoridad automática activa implícita.
- Runtime y backtester avanzan en ramas de producto distintas. Runtime puede cambiar el SDK en su rama; backtester adapta después, sin detener validación actual ni exigir equivalencia temporal. Se mantiene un dominio objetivo único, sin duplicación permanente de paquetes Live/Backtest. No se crearon ramas en esta sesión.
- Se entrega diseño candidato por propietarios, configuración conceptual, permanencia, serving analytics, routing/dedup y pruebas acotadas. Las adiciones técnicas están rotuladas como propuestas, no como código implementado. Se identifica la necesidad de dedup por asociación al cambiar AccountStrategy y de un único versionador del target-set por Strategy para no perder targets de otros pools.

### Evolución histórica conservada

R2 estableció pool–Strategy–MM, una cuenta por asociación y varias asociaciones concurrentes, FIFO, gateway-only y binding AccountStrategy automático. Afinidad multiday era entonces propuesta. R3 la confirmó, retiró el contexto económico de Strategy, exigió presupuesto completo pese a remanente positivo inferior y mantuvo cinco cuentas en alcance. La divergencia económica publicada (rechazo por headroom/retirada anticipada) sigue documentada como antecedente; R4 no la usa como gate para parar runtime o backtester.

Las propuestas R1–R3 contradichas quedan en Git, no como recomendaciones paralelas vigentes. No se modifica el control de TradesGerard ni se despachan agentes. La fecha objetivo Owner domingo2026-10-18 noche no es promesa ni estimación.

## Validación

**Límite R1 conservado:** creación mediante conector GitHub, no ejecución del materializador canónico. Se leyeron skill de entity-update, contrato, templates y scripts, pero materialización, gate por tipo y lint automatizado = NOT_RUN. La primera versión atribuía por error validaciones/equivalencia byte-identical no realizadas; se corrigió en la misma sesión. No se oculta ni se da por subsanada esa limitación.

Historial de readback:

- R1 diseño: commit `b9eb613dcb5cb6c33408bff5e72f4dfa2c295f9e`, blob `015e02a29ee96d88f8c907da2772ad1060411d92`; encabezado/estado leído. Registro inicial: commit `9b0839c2ed22167daeb0429ddf9f63ad2f7c5276`, blob `e70598bdce6a68283f82350b930ef7c65dd5557c`, leído antes de corregirlo.
- R2 diseño: commit `e076fdeb5231f50ce74481cf1459191ac94ff50c`, blob `09f66b257d9d176960af8d8a0e04a4df3c4dfa7d`; readback inicial. Registro R2: commit `c5643616b0326ed3ad7a348489e86a9e4e193e8b`, blob `e40314245fc69bbd2aa5a2b0496b4c98f356afc1`, leído nuevamente en R3.
- R3 diseño: commit `3dc493ecbe38c6738c6737720922df8d24d244a7`, blob `deca8de9c5555285c884f66d5cdd96890a8652fa`; readback1–50. Registro R3: commit `55341fc52c055205c49cac1485482f99dd853f8c`, blob `a6129be701636109cb6d6abcdc647b5eb8af70bc`, leído completo en R4 antes de modificarlo.
- R4 diseño: leído el documento previo por rangos; actualización usando su SHA de concurrencia. Commit `b063ceb218779dd3c8e81310590d0557b6354558`, blob `17caab4ec25f38aea1eea9a8d325617fc4c8371a`. Readback1–76 confirma encabezado R4, permanencia hasta desenlace, ausencia de objetivo de utilización, dos ramas y recuperación canónica de Signal; el blob coincide con la respuesta de escritura. Este registro se actualiza usando su propio SHA leído.

No se ejecutaron materializador, lint, producto, scripts, campañas, tests, infraestructura ni órdenes. Readback es verificación documental, no comparación local byte a byte ni certificación de runtime. Las pruebas listadas son criterios de aceptación futuros, no resultados PASS.

## Compartibilidad

Scope local. Sin credenciales/tokens/endpoints operativos ni transcript de razonamiento. C01..C05 son alias ilustrativos; no inventario físico descubierto. Se preserva el conteo de cinco aportado por el Owner.

## Rollback

Restaurar sólo contenido anterior de nota/registro con una actualización conservadora que preserve cambios concurrentes. Versiones previas en Git. No revertir producto ni modificar controles de backtester. No cerrar sesión ni generar feedback de cierre automáticamente.
