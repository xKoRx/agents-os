---
type: doc
schema_version: 1
status: archived
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[signals-context-flow]]"
aliases:
  - SPEC Funcional Context IO
  - SIG-573 funcional
tags:
  - kind/doc
  - project/crear-context
created: "2026-08-19"
updated: "2026-08-24"
---

# Spec Funcional: entidad Context de componente

**Estado:** draft · **Fecha:** 2026-08-19 · **Dueño:** rjara (Signals) · **Apps:** rio-playmaker, rio-sdk-events

---

## Propósito

Spec funcional de la entidad `Context`: define **qué** tiene que ser verdad cuando esté lista y **por qué**, sin entrar en el cómo. Este archivo es el mirror local de [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573). El contrato de datos y la regla de derivación viven en [[SPEC Tecnica — Context IO]]; [[Guía de implementación — Component Context]] documenta únicamente la entrega abandonada y no es una guía vigente.

> [!warning] Mirror histórico — no implementar desde esta nota
> La fuente de desarrollo vigente es `rio-playmaker` → `.sdd/features/new-component-context/1-functional/spec.md`; SIG-590 registra las enmiendas que todavía requiere SIG-573. Este archivo queda archivado para conservar trazabilidad y no debe competir como fuente canónica.

## Contenido

Problema y root cause · objetivo y alcance v1 · historias de usuario (US-N) · requisitos funcionales (RF-N) · criterios de aceptación (CA-N) · escenarios E2E · fuera de alcance · dependencias e impacto cross-app · decisiones cerradas.

## Problema

Un control plane recibe, en el mensaje de deployment, identificadores, tipo de componente, criticidad y `params` — un mapa de variables ya resueltas por Playmaker, opaco por contrato. Recibe `"broker:9092"` sin saber que vino del `topic_name` de un Kafka vecino: no sabe qué componentes lo rodean, qué publica cada uno, ni en qué versión quedó su propio último deploy.

**Root cause:** el mensaje de deployment transporta valores, no contexto. La información que los explica existe — vive en Playmaker, en las relaciones y en los outputs que los propios CP publicaron — pero nunca cruza hacia el CP.

Consecuencia directa: el diagnóstico de un deploy roto exige reconstruir a mano, desde tres sistemas, algo que Playmaker ya sabe. El CP no puede validar coherencia ni reaccionar a su entorno porque no tiene con qué comparar, y el criterio de qué información consume cada componente vive en el front en vez de viajar con el request.

## Objetivo

`Context` es una entidad de primer nivel en Playmaker: el contenedor de la información de contexto que un componente necesita para desplegarse, calculado por request y transportado en el mensaje de deployment. Es deliberadamente extensible — nace con información de I/O y admite después otras clases (estado anterior del componente, historial de intentos) sobre el mismo canal, sin renegociar el mecanismo. Este spec fija la **entidad y su canal**; lo que transporta hoy es su primer caso de uso.

**Primer caso de uso (v1) — contrato:** Playmaker despacha un mensaje batch con un contrato de deployment por componente; cada uno de esos contratos lleva su propio `Context`:

```
Context (por componente)
├─ dataProduct       → DataProduct { id, name, teamName, environment }
├─ component         → Component { id, name, type, lastDeployedVersion }
│                       └─ LastDeployedVersion { version, outputs }
├─ sources[]         → RelatedComponent   (lo que alimenta a este componente)
└─ destinations[]    → RelatedComponent   (lo que este componente alimenta)

RelatedComponent
├─ id
├─ name
├─ type
└─ outputs           — Map<String, String>, valores ya resueltos
```

Con esto, un valor deja de ser una cadena anónima y pasa a tener procedencia. **Alcance v1:** construir este `Context` y enviarlo, uno por componente, dentro del mensaje batch; que los CP lo lean y actúen es la iniciativa siguiente.

## Historias de Usuario

- **US-1** — **Como** dueño de un control plane, **quiero** recibir, junto al deployment, mi propio Data Product y mi última versión deployada, más qué componentes me rodean y qué publica cada uno, **para** explicar un fallo sin reconstruir el mapeo desde tres sistemas.
- **US-2** — **Como** dueño de un control plane, **quiero** ver los outputs de cada componente vecino ya resueltos, **para** reconocer de cuál de ellos salió cada valor que recibo en `params` sin tener que interpretar estructuras intermedias.
- **US-3** — **Como** desarrollador de Signals, **quiero** que la información de contexto se agregue al mensaje sin cambiar `params`, **para** adoptarla progresivamente sin coordinar un cutover con todos los CP.
- **US-4** — **Como** desarrollador de Signals, **quiero** que la entidad admita nuevas clases de contexto, **para** no rediseñar el canal cada vez que un CP necesite otra información.

## Requisitos Funcionales

| # | Requisito | Prioridad |
|---|---|---|
| RF-1 | Cada componente del mensaje batch de deployment lleva su propio `Context`, como campo adicional y opcional que no altera `params` ni rompe a un consumidor que lo desconoce. | Debe |
| RF-2 | Los `outputs` de un `RelatedComponent` llegan con el valor **ya resuelto** —el mismo valor efectivo que Playmaker sustituye en `params`—, sin wrappers ni estructuras que el CP tenga que desenvolver. Nunca se infieren por igualdad de nombre o valor. | Debe |
| RF-3 | Un `RelatedComponent` que aún no publicó outputs se informa igual —nunca se omite— con `outputs` vacío. | Debe |
| RF-4 | Un `RelatedComponent` importado de otro Data Product resuelve sus outputs contra el componente original; si su importación no está autorizada, sus `outputs` van vacíos. | Debe |
| RF-5 | `Component.lastDeployedVersion` representa el último deploy completado del componente en el ambiente destino y contiene su versión y outputs; si no existe un deploy completado, el objeto completo va ausente. | Debe |
| RF-6 | La identidad de un `RelatedComponent` siempre corresponde a la entidad relacionada dentro del Data Product actual; para una copia importada, su `id` y nombre son los de la copia aunque los outputs provengan del original. | Debe |
| RF-7 | Un fallo interno al construir el Context nunca bloquea el deployment: el mensaje se publica sin `context`. | Debe |

## Criterios de Aceptación

- **CA-1** — Dado cualquier deploy soportado, cuando se publica el mensaje batch, entonces cada componente incluye su `Context` con `dataProduct` y `component` propios, y `params` permanece idéntico al de antes del cambio.
- **CA-2** — Dado un consumidor que desconoce el campo Context, cuando recibe el mensaje, entonces lo procesa sin error.
- **CA-3** — Dado un componente con dos relaciones entrantes y una saliente, cuando se construye su Context, entonces `sources` tiene 2 `RelatedComponent` y `destinations` 1, cada uno con id, nombre, tipo y outputs.
- **CA-4** — Dado un `RelatedComponent` sin deployment previo en el ambiente, cuando se construye el Context, entonces se informa con `outputs` vacío.
- **CA-5** — Dado un `RelatedComponent` importado, cuando se construye el Context, entonces con importación autorizada sus outputs son los del componente original; sin autorización, sus `outputs` van vacíos.
- **CA-6** — Dado un output que el CP publicó como wrapper (`type`/`value`/`sensitive`), cuando viaja en el Context, entonces llega como el valor resuelto y el CP no recibe el wrapper.
- **CA-7** — Dado un fallo interno al construir el Context, cuando se despacha el deployment, entonces el deploy procede igual y el mensaje se publica sin Context.
- **CA-8** — Dado un componente sin deploy completado en el ambiente destino, cuando se construye su Context, entonces `component.lastDeployedVersion` va ausente; si existe, contiene el semver y los outputs del mismo slot.

## Escenarios E2E

- **E2E-1** — **Dado** un pipeline `kafka-topic → flink-sql` donde el topic ya desplegó, **cuando** se despliega el componente Flink, **entonces** su Context incluye `dataProduct`/`lastVersion` propios y el topic en `sources` con sus outputs.
- **E2E-2** — **Dado** el mismo pipeline con el topic aún sin desplegar, **cuando** se despliega el componente Flink, **entonces** `sources` informa el topic con `outputs` vacío.
- **E2E-3** — **Dado** un `flink-sql` que escribe a un `clickhouse-mergetree`, **cuando** se construye el Context, **entonces** ClickHouse aparece en `destinations` con los outputs que publicó.
- **E2E-4** — **Dado** un `kafka-topic` importado desde otro Data Product con importación autorizada, **cuando** se despliega el componente que lo consume, **entonces** `sources` informa los outputs del topic original.

## Fuera de Alcance

- **Que los control planes lean y actúen sobre el Context.** Esta iteración habilita el canal y garantiza que la información llegue; la adopción por cada CP es una iniciativa separada.
- Persistir el Context: no habrá tabla, snapshot, backfill ni lifecycle. Se calcula por request.
- Reemplazar, migrar o eliminar `parameters`/`properties_map`; el front seguirá escribiendo su mapeo hasta que los CP consuman el Context.
- Nuevas clases de información de contexto más allá de las de este contrato.
- Los paths legacy/componente y materializer directo, que hoy no comparten el objeto de dispatch del pipeline.
- Cambiar la operación que Playmaker declara en el mensaje de deployment. El Context viaja con la operación que el pipeline ya emite hoy; revisarla es trabajo aparte y con impacto en los CP.
- Corregir los mismatches de keys ya identificados. El Context los vuelve observables; corregirlos es trabajo posterior.

## Dependencias / Impacto Cross-App

- **rio-playmaker** — app eje. Construye el Context y lo agrega al mensaje.
- **rio-sdk-events** — dueño del contrato del Context y del mensaje de deployment. Requiere una versión nueva.
- **Control planes (kafka, flink, clickhouse, fury, collector)** — reciben el campo y lo ignoran. No requieren cambios para que este spec se cumpla.
- **ads-signals-frontend** — sin cambios en esta iteración.
- **Prerequisito de rama:** el trabajo va montado sobre el fix de resolución de parámetros que mueve la resolución al deploy y despacha el batch siguiente recién tras el commit de los outputs del anterior. Sin ese fix, el Context leería outputs no commiteados.

## Decisiones cerradas

- El Context es efímero y create-only: se calcula por request y no se persiste.
- Se envía en el mensaje de deployment como campo aditivo y opcional. Eso no contradice postergar la adopción: enviar la información y que el CP la consuma son dos pasos distintos.
- Se conserva la nomenclatura `sources`/`destinations`, ya presente en la base de datos y en el contrato del SDK.
- Al CP le llega data resuelta, no material para que la extraiga. Los `outputs` se exponen como `Map<String, String>` de valores efectivos, reutilizando la misma resolución que ya aplica el fix de parámetros sobre `service.values` (que desenvuelve el wrapper `{type, value, sensitive}`). El Context no traslada wrappers ni obliga al CP a replicar esa lógica.
- El SDK trata `params` y `context` como potencialmente sensibles y no garantiza cifrado: productores y consumidores no deben loguear ni persistir valores crudos. La política de si Playmaker emite `outputs` detrás de un flag permanece como decisión bloqueante de rollout, no como responsabilidad del DTO.
- Un `RelatedComponent` importado no declara su origen: al CP le basta con recibir los outputs correctos, que se resuelven contra el componente original.
