---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: 
  - "[[Playmaker — Context en emisores existentes]]"
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
aliases: 
  - Estandarización de Context en flujos RIO
  - SPEC funcional Context en retry, deprovision y desactivación
  - SIG-645 — Context transversal en RIO
tags: 
  - kind/doc
  - area/meli
  - project/playmaker-context-retry-deprovision-desactivacion
created: 2026-09-30
updated: 2026-10-01
project: "[[Playmaker — Context en emisores existentes]]"
application: "[[rio-playmaker]]"
---

# Spec Funcional: Context transversal en RIO — emisores existentes

**Estado:** en revisión · **Fecha:** 2026-10-01 · **Dueño:** rjara (Signals) · **Aplicación:** rio-playmaker

**Spellbook:** [SIG-645](https://spellbook.adminml.com/projects/SIG/specs/SIG-645) · **ID:** `b3b0fb05-d64f-4119-b98e-6aac9b36ca3c`

## Propósito

Estandarizar Context como capacidad transversal de RIO para aportar información adicional a las operaciones existentes que la necesitan. Esta entrega extiende su publicación a undeploy/deprovision, desactivación y a la republicación interna de mensajes de deployment que Playmaker ya contempla.

## Contenido

Contrato funcional para enriquecer mensajes existentes sin cambiar las operaciones ni su elegibilidad.

## Problema

El deployment por batches entrega Context al control plane, mientras otros emisores de `DeploymentTriggerMessage` omiten esa información. Esto produce diferencias de identidad, versión conocida, relaciones y outputs entre mensajes del mismo contrato.

**Causa raíz:** el enriquecimiento con Context está conectado a un camino de envío de deployment, sin un criterio común para los emisores existentes de operaciones RIO.

## Objetivo y alcance

Context acompaña los mensajes que las rutas existentes deciden publicar. Los flujos funcionales incluidos son **undeploy/deprovision** y **desactivación**. La republicación por timeout pertenece al deployment y vuelve a emitir `PROVISION` con su política vigente.

| Ruta existente | Operación | Alcance |
|---|---|---|
| Undeploy/deprovision | `DEPROVISION` | Emisores BigQueue genérico, Fury→Kafka y Kafka→Fury. |
| Desactivación | `DEPROVISION` | Envío asociado a su ejecución de desactivación. |
| Republicación interna por timeout | `PROVISION` | Enriquecer sólo el envío que ya permite la política vigente. |

La republicación requiere un deployment activo `DEPLOY/REQUESTED`, timeout vencido, transporte `BIG_QUEUE`, antigüedad e intentos admitidos, y servicio/grupo/ejecución resolubles. `STARTED`, `UNDEPLOY` y los demás casos no elegibles mantienen su tratamiento. La entrega no agrega un endpoint ni una operación `RETRY`.

```text
Undeploy / desactivacion ---> DEPROVISION --+
Timeout elegible -----------> PROVISION ---+
                                          |
                                          v
                    Context construible y tamaño permitido?
                      | SI: mensaje con Context ---> CP
                      | NO: mensaje sin Context ---> CP
                            + causa registrada
```

## Historias de Usuario

- **US-1** — **Como** responsable de un control plane, **quiero** recibir Context en los mensajes existentes de provisión y retiro incluidos, **para** interpretar la operación con información del componente y su entorno.
- **US-2** — **Como** equipo de RIO, **quiero** un criterio común de disponibilidad y degradación de Context, **para** reutilizar esta capacidad entre emisores.
- **US-3** — **Como** operador, **quiero** reconocer cuándo se envió una operación sin Context y por qué, **para** diagnosticar la degradación sin exponer datos sensibles.

## Requisitos Funcionales

| # | Requisito | Prioridad |
|---|---|---|
| RF-1 | Los mensajes de las rutas incluidas incorporan `context` cuando puede construirse y cumplen el límite de tamaño, para los tipos y transportes ya admitidos. | Debe |
| RF-2 | Context corresponde al componente, data product, definición y ambiente de la operación; conserva al usuario de origen cuando está disponible. | Debe |
| RF-3 | Se preserva cuándo se publica o no: estado, timeout, antigüedad, intentos, routing, permisos y elegibilidad. | Debe |
| RF-4 | Se conserva el contrato y su degradación parcial: historia, relaciones u outputs faltantes no inventan valores ni descartan la identidad resoluble. | Debe |
| RF-5 | Se preservan `params`, operación, identidades, correlación y ciclo de vida, incluidos parámetros Fury y publicación de desactivación. | Debe |
| RF-6 | Un fallo de construcción publica sin Context. Los fallos de publicación mantienen su tratamiento propio. | Debe |
| RF-7 | El mensaje completo con Context admite hasta 200 KiB inclusive. Exceso o medición fallida omiten Context completo y preservan los otros campos. | Debe |
| RF-8 | Se observan resultado/duración de construcción, tamaño y descarte, con correlación y sin valores crudos de Context/params ni datos sensibles. | Debe |
| RF-9 | Se conserva la compatibilidad de consumidores que ignoran Context o admiten su ausencia. Su adopción tiene alcance propio. | Debe |

### Coherencia por ruta

En la republicación, `component.version` identifica la definición asociada al deployment; estado y relaciones se consultan al nuevo envío, sin snapshot inmutable. `latestVersion`, si existe, es la última versión completada del mismo servicio y ambiente y no reemplaza `params`. En deprovision se conserva ese estado conocido antes de la transición al retiro. En desactivación, identidad/definición corresponden al servicio objetivo; las relaciones pueden estar vacías y la correlación pertenece a su ejecución.

## Criterios de Aceptación

- **CA-1** — **Dado** Context resoluble y tamaño permitido, **cuando** publica cada ruta incluida, **entonces** llega Context coherente. Se cubren las tres variantes de deprovision.
- **CA-2** — **Dado** un timeout elegible `DEPLOY/REQUESTED`, **cuando** la política vigente decide republicar, **entonces** llega `PROVISION` con Context de su definición. `STARTED`, `UNDEPLOY`, intentos agotados, transporte no admitido o antigüedad excedida no generan envíos adicionales por el enriquecimiento.
- **CA-3** — **Dado** un recurso con versión completada y outputs conocidos, **cuando** se construye Context para retirarlo, **entonces** conserva esa información del servicio y ambiente objetivo.
- **CA-4** — **Dado** historia, relaciones u outputs ausentes, **cuando** se construye Context, **entonces** conserva la identidad disponible según el contrato parcial.
- **CA-5** — **Dado** un fallo de construcción, **cuando** se publica, **entonces** llega sin Context, con causa registrada y los otros campos preservados.
- **CA-6** — **Dado** tamaño exacto de 200 KiB, exceso y medición fallida, **cuando** se aplica la protección, **entonces** sólo el primero conserva Context y los descartes tienen causas distinguibles.
- **CA-7** — **Dado** un escenario con y sin Context, **cuando** se comparan efectos, **entonces** se conservan RF-3/RF-5, incluido after-commit y bloqueo/resultado de desactivación.
- **CA-8** — **Dado** un consumidor que ignora Context o admite su ausencia, **cuando** recibe ambos mensajes, **entonces** procesa sin migración obligatoria.
- **CA-9** — **Dado** envíos completo/degradado y batches de referencia, **cuando** se revisa la evidencia, **entonces** se distinguen construcción/descarte sin datos sensibles y batches conserva su comportamiento.

## Escenarios E2E

- **E2E-1 — Republicación interna de `PROVISION`:** **Dado** un entorno configurado y un timeout elegible, **cuando** Playmaker decide republicar, **entonces** el consumidor recibe `PROVISION` con Context y correlación vigente.
- **E2E-2 — Deprovision:** **Dado** un recurso con retiro BigQueue, **cuando** se solicita cada variante admitida, **entonces** llega `DEPROVISION` con Context, params originales y correlación correcta.
- **E2E-3 — Desactivación:** **Dado** un componente elegible sin conexiones activas, **cuando** se desactiva, **entonces** llega `DEPROVISION` con Context, ejecución visible y ciclo de resultado vigente.
- **E2E-4 — Degradación común (RF-6/RF-7):** **Dado** construcción o medición fallidas, o exceso de tamaño, **cuando** se publica un envío incluido, **entonces** llega sin Context, con causa observable y seguimiento preservado.

## Fuera de Alcance

- Crear un flujo funcional de retry, un endpoint para reintentar o una nueva operación de mensaje; cambiar la política existente de timeouts o habilitar republicaciones donde hoy no corresponden.
- Agregar Context al deploy individual, actions, materializer u otros emisores adicionales.
- Corregir los `params` vacíos de la republicación interna, cambiar el contrato de Context, retirar `params` o migrar consumidores.
- Persistir un snapshot inmutable del primer envío, agregar APIs/UI de Context o resolver otros hallazgos preexistentes.

## Dependencias e impacto cross-app

Playmaker usa el contrato existente de `rio-sdk-events:1.5.0`. Los control planes reciben información aditiva. La prueba de republicación requiere una configuración y un caso que cumplan la elegibilidad vigente; no se modifica la configuración productiva como parte de esta entrega. Deprovision se valida con ClickHouse y las variantes aplicables; desactivación, con un consumidor o entorno que soporte ese flujo.

## Fuentes

- Iniciativa de origen: [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573) y [SIG-590](https://spellbook.adminml.com/projects/SIG/specs/SIG-590). [Operaciones del SDK 1.5.0](https://github.com/melisource/fury_rio-sdk-events/blob/1.5.0/src/main/java/com/mercadolibre/rio/sdk/events/deployment/DeploymentOperation.java).
- [Timeout job: invocación, guards y publicación](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/DeploymentTimeoutJob.java#L124-L360); [invocación desde historia](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/impl/PipelineHistoryServiceImpl.java#L87-L104).
- [Deprovision: emisores existentes](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/impl/UndeployServiceImpl.java#L562-L673); [desactivación: publicación y mensaje](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/java/com/mercadolibre/rio/playmaker/service/impl/ComponentInactivationServiceImpl.java#L383-L471).
- [Política base](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/resources/application.yml#L264-L294); [local: cero intentos](https://github.com/melisource/fury_rio-playmaker/blob/f087e4b7cc185d93618de4bdeaeb76b53486ac47/src/main/resources/application-local.yml#L68-L82).
