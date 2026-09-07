---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Presentación deployments en RIO]]"
  - "[[ads-signals-knowledge-library]]"
  - "[[RIO]]"
aliases:
  - Auditoría ads-signals-knowledge-library
  - Review RIO knowledge library
tags:
  - kind/doc
  - area/meli
  - project/presentacion-deployments-rio
created: "2026-09-01"
updated: "2026-09-01"
---

# Revisión de ads-signals-knowledge-library

## Propósito

Determinar si `ads-signals-knowledge-library` puede reemplazar a `signals-knowledge` como knowledge canónica del vault y si su contenido es suficientemente confiable para explicar deployments en RIO el 2026-09-02.

## Veredicto

**Sí reemplaza al repo anterior como punto de entrada canónico, pero todavía no puede tratarse como verdad operacional autosuficiente.** La librería tiene una arquitectura documental muy superior: límites de verdad, contratos, flujos, fichas por servicio, troubleshooting, catálogo de features, freshness, sensitivity, context packs y evaluaciones reproducibles. Sin embargo, en `master@c2e83fdbd` falla su propio validador con 17 errores y su snapshot del código, verificado el 2026-08-28, quedó materialmente atrás de varios `origin/master`.

Para la presentación, la librería se usó como mapa de navegación; cada afirmación sensible se contrastó con el código actual. No se modificó el repo externo durante esta revisión.

## Contenido

### Cobertura revisada

- Superficie completa inventariada y validada: 148 archivos fuera de `.git`, 138 Markdown, 129 documentos bajo `docs/`, 5 scripts y 5 templates.
- Startup y gobierno: `AGENTS.md`, `README.md`, navegación, límites de verdad, source manifest, freshness/confidence, sensitivity e ingestion strategy.
- Arquitectura y contratos: plataforma, control/data plane, interacciones, pipeline deployment, materialization, identifiers, routing, messages/delivery y status models.
- Servicios: Playmaker, SDK Events, Materializer, Kafka, Flink, ClickHouse, Fury, Signals, Observability, KMS y servicios adyacentes.
- Operación: troubleshooting, capability maps, feature catalog, coverage ledger, context packs y las evaluaciones/runs congeladas.
- Contraste primario: `origin/master` de nueve repos del camino de deployment, sin alterar sus worktrees.

### Integridad mecánica

`ruby scripts/validate_library.rb` termina en `LIBRARY_VALIDATION_FAIL errors=17`:

- 3 freeze JSON apuntan al commit inexistente `a1b787419aeef34a7d7ea74fbeb7085ac1dc6185`.
- Cada freeze reporta 4 archivos del harness que no existen en ese snapshot: 12 errores adicionales.
- `docs/10-evaluations/cross-app-feature-prospects-review-2026-08-28.md` contiene 2 links locales rotos hacia `.sdd/.../cleric.md#iteración-3` y `.sdd/.../paladin.md`.

Resultado: la librería no pasa hoy su gate declarado de reproducibilidad e integridad.

### Drift material encontrado

| La librería afirma o implica | Código actual verificado | Impacto |
|---|---|---|
| Signals CP es template/placeholder y no implementa deployments. | `rio-controlplane-signals@26ec78392` implementa `catalog-signal`, `bigqueue-signal` y `stream-signal`, `PROVISION`/`UPDATE`/`DEPROVISION`, idempotencia KVS con CAS, Catalog/Collector y resultados. | El mapa de CP y routing queda incompleto si se usa la librería sola. |
| Fury cubre sólo Kafka↔Streams; BigQueue/KVS están ausentes. | `rio-controlplane-fury@27786b9cc` agrega `kafka-fury-bigqueue` y `kafka-fury-kvs`, desired/observed state durable y marcadores de publicación terminal. | Se pierde el CP con el patrón de confiabilidad más fuerte del sistema. |
| Observability no sincroniza tags OTel y no cubre `aws-flink-job`. | `rio-controlplane-observability@486e063dd` implementa ambos. | La cobertura de governance aparece menor que la real. |
| Playmaker tiene 8 tipos BigQueue y orden “topological-ish”. | `rio-playmaker@6cb4c5668` declara 11 rutas explícitas BigQueue más catch-all REST; `FORCE_CONFIG_ORDER = true` ignora el grafo y fuerza no-engines/engines. | Routing y causalidad de batches quedan descritos incorrectamente. |
| No existe endpoint moderno de logs de execution. | Playmaker actual contiene `PipelineExecutionLogsService` y su controller; el frontend actual lo consume. | Troubleshooting y API surface quedan atrás. |
| El source manifest representa el código vigente. | Desde sus SHAs cambiaron Playmaker, Flink, Fury, Observability, Signals y frontend; sólo Materializer, SDK Events, Kafka y ClickHouse coinciden con la revisión. | `last_verified` no garantiza frescura por servicio. |
| El README dice que el repo no tiene remote configurado. | El checkout revisado tiene `origin/master` y está alineado en `c2e83fdbd`. | El bloque “Estado del repositorio” también necesita refresco. |

### Hallazgos de arquitectura que la presentación debe mostrar

- Playmaker tiene dos continuaciones críticas no durables: dispatch inicial y avance de batch mediante eventos `AFTER_COMMIT` + `@Async` sin outbox/replayer.
- Kafka, Flink y ClickHouse ACKean el push antes de completar trabajo local en background; una caída puede consumir el mensaje y matar la operación.
- Kafka/ClickHouse y parte de Flink pueden persistir terminal local antes de una publicación de resultado best effort, dejando efecto real sin cierre en Playmaker.
- Fury persiste desired/observed state y distingue resultado reportado de publicado; permite reconciliar y reintentar, patrón preferible para los demás CP.
- Signals procesa dentro del request y hace fallar el push si no puede publicar el terminal, reduciendo la ventana de pérdida.
- Materializer conserva deuda legacy: futures descartados, timeout index en memoria, workqueue desprendida y un adapter stream que hoy convertiría `FAILED` en `COMPLETED` si se habilitara.
- La matriz de capacidad de CP y el routing base de Playmaker divergen para `gcp-*`, `kafka-fury-bigqueue` y `kafka-fury-kvs`.

El detalle causal y el modelo completo están en [[Deployments en RIO — flujo completo]].

### Qué está bien diseñado en la librería

- La jerarquía responde bien a preguntas humanas: empezar, entender plataforma, seguir flujos, bajar a servicios, operar, consultar contratos y evaluar calidad.
- Separa autoridad del código, confianza documental y evidencia segura; prohíbe inventar delivery semantics y recuerda que ACK no es business success.
- Los contratos de identifiers, status y mensajes son una buena columna vertebral transversal.
- Los context packs y feature catalog permiten retrieval focalizado sin releer todo el repositorio.
- El validador y los freezes son la dirección correcta; el problema actual es que el gate está rojo y no se ha actualizado con los repos.

### Plan de corrección recomendado para el repo

1. Actualizar `source-manifest.md` a los SHAs actuales y declarar freshness por servicio, no sólo por fecha global.
2. Regenerar las fichas y contratos afectados: Signals, Fury, Observability, Playmaker routing/order/logs y capability matrix.
3. Reparar los tres freezes para que referencien commits alcanzables o preserven el objeto necesario, y corregir los dos links `.sdd`.
4. Ejecutar `validate_library.rb` en CI y bloquear merge cuando el gate esté rojo.
5. Convertir capability↔routing↔timeout en una validación cruzada ejecutable: todo tipo implementado debe declarar owner, transport, operaciones, timeout e idempotencia.
6. Agregar un ledger explícito de riesgos de delivery por boundary: durable acceptance, ACK point, idempotency claim, terminal persistence, result publication y replay owner.

## Fuentes

- Repo `ads-signals-knowledge-library`, path `ads-signals-knowledge-library` relativo a `~/fuentes`, `master@c2e83fdbdc38cbc089328d0c67d7bf25e15f762a`, limpio y alineado con `origin/master` al revisar.
- `ruby scripts/validate_library.rb`, ejecutado el 2026-09-01: 17 errores reproducibles.
- Repos primarios y SHAs consignados en [[Deployments en RIO — flujo completo]].

## Separación de certeza

- **Hecho:** estructura, campos, routing, listeners, orden de persistencia/publicación y manejo de excepciones observados en el código.
- **Inferencia:** una caída en esas fronteras puede perder una continuación o separar estado local de estado orquestado; se deduce de la ausencia de una aceptación/outbox/replayer durable en el camino observado.
- **Pendiente:** incidencia real, frecuencia, configuración viva de scopes, filtros BigQueue y overrides de producción. Requiere telemetría operacional, no más lectura de repos.
