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

Creación y actualización documental de `10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` por mandato Owner del 2026-10-16. R1 CANDIDATO_INICIAL / NO_ACEPTADO; R2 CANDIDATO_R2 / DISEÑO_NO_ACEPTADO; vigente **CANDIDATO_R3 / DISEÑO_NO_ACEPTADO**. No cambia aceptación del proyecto, producto ni controles del carril local. Escrituras sobre master, sin rama ni PR.

## Motivo

Conservar AS-IS localizado y decisiones progresivas en la autoridad runtime, sin duplicar catálogo de cuentas ni estado de campañas. R2 eliminó asignación manual de Strategy/MM por cuenta y corrigió exclusividad por pool. R3 confirma afinidad permanente, retira cuenta/MM del contexto de Strategy, exige el intento con presupuesto completo pese a remanente menor y fija la entrega en cinco cuentas.

## Fuentes usadas

Mandato inicial adjunto PROMPT_VERSION 1 y los tres turnos explícitos del Owner del 2026-10-16. R1/R2: Echo `0c4aae552176fda005c44766e24dd70e8c48e589`, incluyendo platform_campaign.go blob `1bdbd20f4abf9aa89d4044fa77332d2a9801d04f` y TG-FLOW. Fuentes Apache sobre owners/direcciones citadas en R2 son fundamento histórico, no verificación del wiring de Echo. La investigación comercial R1 se retiró del alcance por el Owner; no se repitió en R2/R3.

R3: master resuelto en `95e9d105182af99d03700f4b5def24bf9fc6b5fd`, compare con base indica dos commits. Lecturas: `v3/sdk/futures/strategies/tgmm/tgmm.go` líneas1–305, blob `eb2824a470d27d63d93c856f4a0829d4526d367b`; `v3/backtester/platform_operability.go` líneas1–240, blob `52710c0494dd375745aeb8c3dce85386ec36265e`; minimum_policy.go completo, blob `9ace5fdbff3f6b2d506c9e769cc29236de9d54cf`; TG-FLOW.md, blob `7af1b9a9fe1a471ebe0f5e048379c8c0400dd7fb`. Documentación oficial NinjaTrader OnOrderUpdate consultada para distinguir Submitted/Accepted/Rejected/Filled y rechazo por riesgo, no para permisos ni para mover la Strategy a NinjaTrader.

## Resolución aplicada

R2 estableció pool–Strategy–MM, una cuenta por asociación y varias asociaciones concurrentes dentro del mismo pool, turno persistente, FIFO y gateway-only. AccountStrategy se mantiene propuesto como binding efectivo automático. R3 conserva esas decisiones y corrige las siguientes:

- Afinidad A→A a través de días/pausas confirmada expresamente; ya no es sólo interpretación propuesta. I1 no introduce migraciones entre asociaciones/pools.
- Strategy pasa a ser completamente agnóstica a cuenta y MM. La sugerencia R2 de contexto de cuenta para ambos consumidores se reemplaza por contexto económico sólo en MM/owners financieros; señales y ciclo técnico compartibles. No duplicar Operation financiera para llamar canónicas a las intenciones.
- El presupuesto solicitado no se reduce ni se rechaza/retira sólo porque el remanente positivo sea inferior. El piso y su breach real siguen observándose; se distinguen presupuesto, orden, fill y PnL. Cantidad/ticks/capacidad reales no se falsifican.
- Divergencia publicada observada: EntryBudgetV1 de TGMM rechaza por headroom y platform_operability retira por presupuesto. No cumple el nuevo mandato de entrar completo. Se registra como punto de integración con el delta local, sin cambiar producto, detener al GLM ni afirmar haber visto su WIP.
- Cohorte requerida CINCO cuentas, no entrega de una. Tres asociaciones sólo habilitan tres turnos simultáneos; cinco candidatas no garantizan cinco operaciones en una semana. Se propone configuración de cinco asociaciones con Strategies reutilizadas entre pools distintos para dar cinco turnos desde el inicio; propuesta, no cambio de configuración ejecutado. No se fabrican señales para completar uso.

El diseño permanece candidato. La fecha objetivo domingo2026-10-18 noche no se presenta como promesa ni estimación. No hay prompt de implementación, dispatch ni cierre.

## Validación

**Límite R1 conservado:** creación mediante conector GitHub, no mediante ejecución del materializador canónico. Se leyeron skill de entity-update, contrato, templates y scripts canónicos, pero materialización, gate por tipo y lint automatizado = NOT_RUN. No comparación local byte a byte ni reconstrucción local ejecutada del contrato. La primera versión del registro atribuía por error esas validaciones; se corrigió en la misma sesión y esta limitación no se oculta.

Readback R1: diseño creado en `b9eb613dcb5cb6c33408bff5e72f4dfa2c295f9e`, blob `015e02a29ee96d88f8c907da2772ad1060411d92`, encabezado/estado leído. Primera versión del registro creada en `9b0839c2ed22167daeb0429ddf9f63ad2f7c5276`, blob `e70598bdce6a68283f82350b930ef7c65dd5557c`, leída completa antes de su corrección.

Readback R2: diseño actualizado con SHA de concurrencia, commit `e076fdeb5231f50ce74481cf1459191ac94ff50c`, blob `09f66b257d9d176960af8d8a0e04a4df3c4dfa7d`; encabezado y rango inicial verificados. Registro R2 actualizado en `c5643616b0326ed3ad7a348489e86a9e4e193e8b`, blob `e40314245fc69bbd2aa5a2b0496b4c98f356afc1`; leído nuevamente completo en R3 antes de modificarlo.

R3: nota existente leída en dos rangos1–110 y111–230 con el mismo blob R2; actualización conservadora por ese SHA, commit `3dc493ecbe38c6738c6737720922df8d24d244a7`, blob `deca8de9c5555285c884f66d5cdd96890a8652fa`. Readback1–50 en master confirma encabezado R3 y decisiones de afinidad, Strategy, presupuesto y cinco cuentas; blob coincide con la respuesta de actualización. El registro existente se actualiza por su SHA leído. No se afirma comparación local byte a byte, lint ni ejecución de fixtures.

No se ejecutaron código de producto, scripts, campañas, tests de trading, infraestructura ni órdenes. La publicación documental no certifica el runtime físico ni acepta el diseño.

## Compartibilidad

Scope local. Sin credenciales, tokens, endpoints operativos, memoria interna privada ni transcript de razonamiento. Alias C01..C05 son ficticios; se conserva el conteo de cinco dado por el Owner, no un descubrimiento de sus identidades.

## Rollback

Restaurar sólo el contenido anterior de nota/registro por actualización conservadora que preserve cambios concurrentes. Las versiones R1/R2 quedan en Git. No afecta producto ni controles TradesGerard. No cerrar sesión ni generar feedback automáticamente.
