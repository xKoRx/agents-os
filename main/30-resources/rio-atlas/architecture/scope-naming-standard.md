---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
sources:
  - "[[scope-inventory]]"
  - "[[scope-compatibility-matrix]]"
  - "[[fury-segmentation-model]]"
last_verified: 2026-08-12
confidence: high
aliases:
  - RIO Scope Inventory Functional Specification
  - spec funcional de scopes RIO
  - estándar de nomenclatura de scopes RIO
tags:
  - kind/resource
  - tech/rio
  - project/scopes-rio
created: 2026-08-12
updated: 2026-08-12
cssclasses:
  - wide
---

# RIO Scope Inventory — Functional Specification

> [!summary] Decisión
> Construir el inventario como una fuente de verdad normalizada obtenida de Fury y generar desde ella la documentación y el reporte visual. Registrar hechos tipados por runtime y binding; no existe una categoría genérica de uso, no se infiere el segmento desde el nombre y no hay score compuesto.

## Síntesis vigente

Spec funcional del inventario real de scopes RIO. Define la fuente JSON, el collector Fury, las reglas tipadas para BigQueue/Streams/Work Queues/Web, la carga de configuración, el reporte derivado y los gates de publicación. El baseline se mantiene separado de la propuesta, pero el reporte ya expone los candidatos que alimentan la normalización de nomenclatura.

## Problem Statement

RIO opera hoy **88 scopes runtime en 9 aplicaciones** con seis tipos de compute y tres infra-segments. El inventario anterior partía de superficies parciales: `fury list-infra` ocultaba 21 runtimes administrados y no exponía `metadata.segment`; el grid convertía ausencias de evidencia en una clasificación dominante y colapsaba segmentos de runtime, recurso y binding en una sola etiqueta. El resultado era visualmente fuerte, pero llevaba a conclusiones incorrectas, como presentar `rio-controlplane-observability/consumer-prod-nonsite` como `legacy` cuando Fury lo registra directamente en `nonsite`.

El grafo read-only que usa Fury contiene los hechos necesarios para resolver el baseline: runtime, build, environment, lifecycle, segmento, consumers BigQueue, sinks Streams y worker groups de Work Queues. Esos hechos tienen semánticas distintas. Un consumer `running`, un sink pausado, un worker group `ready` y un runtime `Healthy` no son una misma métrica y tampoco prueban tráfico o necesidad de negocio.

## Objectives

1. Mantener una fuente de verdad estructurada y reproducible con una fila única por `application/scope`.
2. Registrar el segmento efectivo del runtime desde `metadata.segment` y conservar por separado los segmentos observados en recursos y bindings.
3. Mostrar relaciones operacionales sólo donde Fury entrega evidencia tipada: consumers BigQueue, sinks HTTP de Streams y worker groups de Work Queues.
4. Generar el inventario Markdown y el reporte HTML exclusivamente desde la fuente normalizada, sin conteos escritos a mano.
5. Hacer que una audiencia sin contexto previo entienda el problema, el estado real y los gaps en menos de dos minutos.
6. Fallar la generación si faltan aplicaciones, aparecen scopes duplicados, quedan bindings sin resolver o el listado de activos no reconcilia con `scopes status`.
7. Registrar por scope la Fury route Web y contrastar la versión de configuración desplegada por Fury con el latest release `APPROVED` de Config Orchestrator; la resolución del profile en código queda como evidencia independiente.
8. Traducir los hechos a una lista explícita de cambios candidatos por aplicación para conducir la nomenclatura de todos los componentes Fury.
9. Exigir que toda aplicación desplegable represente los scopes lógicos `prod`, `stage` y `alpha`; `beta/gamma` son extensiones opcionales.
10. Definir un routing escalable desde el ambiente solicitado hasta el consumer del scope efectivo, separado del segmento físico Fury.

## Scope

**In scope:** extracción read-only de Fury y Config Orchestrator; normalización allowlisted; snapshot JSON; segmentos, lifecycle, health, bindings y routes; comparación deployed/latest-approved por scope; resolución de profiles/archivos del checkout con commit; propuesta curada por aplicación; grupos `alpha/beta/gamma/stage`; contrato extensible para Secrets/KVS; reporte visual e inventario Markdown generado.

**Out of scope:** tráfico, último mensaje, owner humano, ejecución de renombres, migración de recursos, compatibilidad semántica de schemas, sinks `target_type=TP/STREAM` sin join directo a un runtime HTTP e implementación productiva del routing propuesto.

## Users

- **Signals / RIO:** necesita responder qué existe y cómo está conectado sin reinterpretar cada nombre.
- **Owners de control planes:** necesitan ubicar sus runtimes, segmento y bindings verificables.
- **Fury / plataforma:** necesita distinguir datos expuestos por la plataforma de inferencias hechas en documentación.
- **Liderazgo técnico:** necesita una vista llamativa y breve que explique el problema antes de entrar al detalle.

## Source of Truth Contract

El artefacto canónico es `~/fuentes/rio-inspector/rio-scopes.json`, generado por `~/fuentes/rio-inspector/scope_inventory.py`. El payload completo del backend no se persiste porque puede contener endpoints y referencias internas; sólo se guarda una allowlist funcional.

```yaml
schema_version: 3
collected_at: timestamp
collector_versions:
  furycli: version
  cli-services: version
  cli-scopes: version
scopes:
  - id: application/scope
    application: app
    scope: scope
    fury_service_id: number
    service_type_raw: Fury service type
    runtime_type: web | bigqueue | stream | work_queue | template_processing | job
    version: build
    runtime_segment: legacy | nonprod | nonsite | null
    fury:
      deployment_status: finished | inactive
      lifecycle: Active | Inactive
      health: Healthy | Desired | null
      environment: Productive | Test | Unknown
      criticality: value
      observed_at: timestamp
    resource_segments: []
    bindings: []
    binding_summary: typed state | null
    route:
      applicable: boolean
      reported: boolean | null
      source: Fury metadata.loadbalancer_id
    fury_config:
      deployed_version: value | null
      latest_approved_version: value | null
      latest_approved_found: boolean
      comparison: current | different | deployed_version_not_exposed | not_reported
    code_config:
      resolved_profiles: []
      selected_files: []
      missing_profile_files: []
      code_revision:
        commit: git sha | null
        branch: local branch | null
    resource_inventory:
      secret: {collection_status: not_collected, items: []}
      kvs: {collection_status: not_collected, items: []}
    derived:
      operational:
        state: active | inactive | not_evaluated
        reason: typed reason
      naming_flags: []
      change_tracks: []
    provenance:
      collector: furycli.furyapi.FuryApi.get_scopes
      captured_at: timestamp
validation:
  duplicate_scope_ids: []
  runtime_bindings_unresolved: 0
  active_status_missing: []
  unexpected_status_rows: []
```

## User Stories & Acceptance Criteria

### US-1 — Inventario completo desde Fury

Como maintainer de RIO, quiero que todos los runtimes live aparezcan una sola vez para no perder tipos que `list-infra` filtra.

- El collector usa `FuryApi(app).get_scopes()` sobre `applications/<app>/services` con las 10 aplicaciones RIO explícitas.
- Sólo entran como scopes los tipos runtime allowlisted: Web, BigQueue, Streams, Work Queues, Template Processing y Job.
- Cada identidad `application/scope` es única.
- El corte generado reconcilia runtimes activos con `fury -a <app> scopes status -j`.
- Un error al leer el service graph, un duplicado o una diferencia de reconciliación detiene la publicación.

### US-2 — Segmento runtime real

Como owner de un control plane, quiero ver el infra-segment que Fury registra para cada runtime, sin deducirlo del nombre.

- `runtime_segment` proviene únicamente de `service.metadata.segment`.
- `consumer-prod-nonsite` aparece como `nonsite` porque Fury lo entrega así, no por el sufijo.
- Si Fury entrega `null`, la UI muestra `no expuesto`; nunca completa `legacy` por defecto.
- Segmentos de consumer, sink o worker group viven en `resource_segments`/`bindings` y no sobreescriben el segmento runtime.
- Cuando runtime y recurso difieren, ambos valores quedan visibles en el detalle.

### US-3 — Binding BigQueue observable

Como owner de un runtime BigQueue, quiero ver si tiene consumers asignados y su estado exacto.

- Cada nodo `bigqueue_consumer_new` se une al runtime sólo por `service_id` y se valida que el target sea BigQueue.
- `consumer activo` aparece sólo si al menos un consumer asignado está `running`.
- `consumer pausado` aparece si ninguno está `running` y al menos uno está `paused`.
- `sin consumer` aparece sólo después de consultar el grafo completo y encontrar cero asignaciones.
- Web, Jobs, Template Processing y otros runtimes no reciben esta pill.

### US-4 — Binding Streams observable

Como owner de un runtime Streams, quiero distinguir un sink asignado activo, pausado o la ausencia de un enlace HTTP directo.

- Sólo se unen sinks con `target_type=HTTP` mediante `metadata.scope`; `sink_app_name/sink_scope_name` puede ser fallback validado.
- `sink activo` exige `enabled=true` y `user_status=RUNNING`.
- `sink pausado` exige `enabled=false` o `user_status` con prefijo `PAUSED`.
- `sin sink HTTP directo` significa que no existe ese join en el grafo; no significa ausencia de tráfico o necesidad.
- Sinks `target_type=TP/STREAM` no se adjudican por similitud de nombre.

### US-5 — Binding Work Queues observable

Como owner de Work Queues, quiero ver el worker group realmente unido al runtime y cualquier contradicción de configuración.

- El join primario usa cada `worker_group.metadata.data.worker_group_segments[].scope`; `metadata.data.scope` queda como fallback cuando no existe la lista y `metadata.scope_id` no se usa para resolver el runtime.
- `worker group activo` exige `worker_group_status=ready` y `paused=false`.
- `worker group pausado` y `sin worker group directo` son estados separados.
- Si el campo general y `worker_group_segments[].scope` discrepan, `mapping_conflict=true` queda persistido y visible; no se corrige desde el nombre.

### US-6 — Reporte derivado y comprensible

Como lector sin contexto previo, quiero entender rápidamente el tamaño, la segmentación y los bindings antes de explorar scopes individuales.

- El hero explica en una frase qué se registró y cuándo.
- Los KPIs muestran sólo conteos reconciliables: scopes, lifecycle, split prod/test, BigQueue con consumer activo y cobertura de segmento runtime.
- No existe score, ranking de riesgo ni indicador genérico de uso.
- Hay búsqueda y filtros por ambiente, runtime, segmento y binding.
- Cada scope abre un detalle con Fury, segmento runtime, segmentos de recurso, bindings, source y timestamp.
- La ayuda `?` funciona con click, teclado, Escape y touch; ningún dato depende sólo del color o del hover.

### US-7 — Documentación generada desde la base

Como maintainer, quiero eliminar drift entre la base y los entregables.

- `scope-inventory.md` y `rio-scope-inventory.html` se escriben desde el mismo JSON en una ejecución.
- Ningún KPI del HTML está hardcodeado.
- La nota generada identifica comando, fuente, límites y timestamp.
- El collector persiste las versiones `furycli`, `cli-services` y `cli-scopes`.

### US-8 — Fury routes Web observables

Como owner de un runtime Web, quiero saber si Fury reporta una route para no tratar Web como una caja negra.

- `route.reported=true` sólo cuando el runtime Web expone `metadata.loadbalancer_id`; el ID interno no se persiste.
- Un Web sin route reportada se clasifica `operational.state=inactive` en la capa reporte, sin alterar su lifecycle Fury.
- Web no recibe consumer, sink ni worker group artificial.
- El panorama por aplicación lista de forma explícita los Web sin route.

### US-9 — Fury Config por scope

Como maintainer de RIO, quiero contrastar para cada scope la configuración que Fury reporta como desplegada con el último release aprobado.

- `deployed_version` proviene únicamente de `metadata.application_config_version` del runtime Fury.
- `latest_approved_version` proviene del endpoint batch de Config Orchestrator usado por Fury Deployments para `--auto-config-version`.
- `current` exige igualdad exacta; `different` sólo informa desigualdad, no afirma cuál versión es más nueva.
- La ausencia de release aprobado queda `not_reported`; nunca se traduce a “carga default”.
- Profile y archivo Spring del repo viven en `code_config`, con commit/branch, y no se presentan como Fury config.

### US-10 — Panorama accionable para normalización

Como equipo RIO, quiero pasar de un conteo a una lista concreta de infraestructura y nombres que requieren decisión.

- Cada app muestra composición por tipo y segmento.
- BigQueue lista scopes sin consumer activo; Streams separa sink pausado de ausencia de sink HTTP; Work Queues lista ausencia de worker group; Web lista ausencia de route.
- Config lista diferencias concretas deployed/latest approved y conserva los dos valores.
- Cada tarjeta puede alternar entre situación actual y propuesta target-state.
- Un click sobre un scope del panorama lo lleva al detalle filtrado del inventario.

### US-11 — Propuesta comparable en todas las aplicaciones

Como equipo RIO, quiero ver el delta completo actual→propuesta para saber qué se retira, qué conserva identidad y qué debe crearse.

- Toda aplicación y repositorio aparece con `prod`, `stage` y `alpha`; `beta/gamma` sólo aparecen como ambientes adicionales.
- Los scopes actuales que desaparecen del target se renderizan primero y con borde rojo.
- Los scopes cuyo nombre y tipo se conservan usan borde gris; si cambia el segmento, indican `migrar segmento`.
- Los scopes nuevos usan borde verde.
- Después de los retiros, la lista se ordena `prod`, `stage`, `alpha`, `beta`, `gamma`.
- Un punto amarillo aparece únicamente en scopes Stream objetivo que necesitan decisión de sink.
- `rio-sdk-events` participa mediante contrato por ambiente, sin inventar runtimes Fury para una librería.

### US-12 — Routing por scope efectivo

Como owner de una aplicación RIO, quiero que una operación destinada a `alpha` llegue sólo al consumer `alpha` de cada control plane.

- El front resuelve `frontend` y `backend` por eje con `queryParam ?? cookieMeliLab ?? prod`; el queryParam pisa MeliLab sólo en su eje.
- nginx sirve el scope/build de frontend y el front traduce `backend` al header estándar de scope que Fury routes usa para dirigir a Playmaker.
- Playmaker valida el scope solicitado, lo normaliza como `environment_scope` y estampa un tag `scope:<x>` server-side.
- Un topic compartido transporta los mensajes y el consumer Fury filtra por el tag `scope:<x>`; el endpoint vuelve a validar como defensa en profundidad.
- `mqclient Filters`/Fury `filters.modified_fields` transporta tags de negocio arbitrarios; `scope:<x>` sigue el patrón productivo verificado en VIS. Falta confirmar si Fury aplica el filtro server-side.
- Si el filtro no es server-side, prod usa un topic separado y los ambientes nonprod comparten topic+filtro para evitar entrega física de mensajes productivos a consumers no productivos.
- `ProducerBuilder.withSegmentID` conserva su responsabilidad física nonprod/nonsite y no selecciona alpha/stage/prod.

## Business Rules

1. No existe un campo o categoría genérica de uso.
2. `running`, `ready`, `Healthy` y `Active` conservan su semántica original; ninguno se traduce a tráfico o necesidad.
3. El segmento runtime es `metadata.segment`; el nombre es sólo identidad y puede estar desactualizado.
4. Un scope puede relacionarse con recursos en otro segmento; no se colapsan los valores.
5. Web no recibe clasificación de binding; recibe una señal independiente de Fury route y una lectura operacional derivada de esa señal.
6. Rojo se reserva para un estado negativo verificado; gris representa no aplica/no expuesto y ámbar una relación pausada, ausente o contradictoria.
7. Las aplicaciones se ordenan alfabéticamente o por volumen explícito, nunca por suma de señales heterogéneas.
8. La capa factual no decide retiros. La propuesta curada sí recomienda consolidar, agregar o retirar, pero todo elemento `decision_required` permanece sujeto a aprobación del equipo.
9. `legacy` significa que Fury reporta `metadata.segment=legacy`; `segmented` significa `nonprod` o `nonsite` explícito.
10. RIO define el nombre base `<environment>-<role>[-<qualifier>]` y Fury agrega siempre el segmento efectivo como último token del nombre materializado (`alpha-api` → `alpha-api-nonprod`); el equipo no lo escribe ni lo infiere.
11. `prod` vive en `nonsite`; `alpha`, `beta`, `gamma` y `stage` viven en `nonprod`.
12. Todo scope lleva los tres tokens `<environment>-<role>-<segment>`, sin nombres pelados: con un único runtime del tipo, `<role>` toma el valor canónico del tipo (`api`, `consumer`, `events`, ...). Más de un scope del mismo tipo+ambiente sólo se permite bajo los criterios de excepción de [[#Estándar de Nomenclatura]].
13. Toda aplicación desplegable implementa como mínimo `prod`, `stage` y `alpha`; `beta/gamma` no sustituyen ese mínimo.
14. Todo Stream sin sink activo lleva punto amarillo: antes de migrarlo se decide retiro o se documenta/reconecta su binding.
15. El ambiente lógico viaja como dato semántico validado; el segmento Fury nunca se usa como sustituto de `environment_scope`.

## Current Verified Baseline

| Dimensión | Corte live |
|---|---:|
| Runtimes | 88 |
| Lifecycle | 85 activos · 3 inactivos |
| Ambiente | 32 prod · 56 test/stage |
| Tipos | 42 Web · 23 BigQueue · 15 Streams · 3 Work Queues · 3 Template Processing · 2 Jobs |
| Segmento runtime | 50 legacy · 26 nonprod · 12 nonsite |
| BigQueue | 22 scopes con consumer activo · 1 con consumer pausado · 39 consumers running · 1 paused |
| Streams | 0 scopes con sink HTTP activo · 12 con sink pausado · 3 sin sink HTTP directo |
| Work Queues | 3 scopes con worker group activo · 0 pausados · 0 sin worker group directo |
| Web routes | 42 reportadas · 0 sin route |
| Fury Config Orchestrator | 42/88 con latest approved · 39 current · 2 diferentes · 1 latest con deployed no expuesta · 46 sin release aprobado reportado |
| Lectura operacional | 64 activos · 19 inactivos · 5 no evaluados |
| Normalización | 50 scopes legacy · 53 con al menos un flag de naming |

El scope nuevo respecto del baseline anterior es `rio-controlplane-signals/bq-consumer-nonprod`: Fury lo entrega `Active`, `Healthy`, `nonprod`, con `deployment-consumer--nonprod` en `running`. El repositorio local no era una autoridad suficiente para decidir que Signals no tenía scopes.

## Target State de scopes

La propuesta versionada vive en `~/fuentes/rio-inspector/rio-scope-policy.json`; no está embebida en el HTML. Define por aplicación el descriptor del cambio, cada scope objetivo, su tipo, segmento, scopes de origen y si requiere decisión.

### Estándar de Nomenclatura

> [!important] Convención canónica — base RIO `<environment>-<role>`, visible Fury `<environment>-<role>-<segment>`
> RIO gobierna `<environment>-<role>[-<qualifier>]`; Fury agrega siempre `-<segment>` desde el placement efectivo. El resultado visible tiene los tres tokens, pero ambiente/rol y segmento pertenecen a autoridades distintas.

```text
<environment>-<role>[-<qualifier>]-<segment>

environment : prod | stage | alpha | beta | gamma   · ambiente lógico real
role        : token funcional del servicio          · vocabulario canónico abajo
qualifier   : opcional                              · SÓLO si hay >1 scope del mismo tipo+ambiente
segment     : nonsite | nonprod                     · metadata.segment de Fury (real)

prod -> nonsite        stage | alpha | beta | gamma -> nonprod
```

Reglas duras:
- RIO define el nombre base `<environment>-<role>[-<qualifier>]`; `<segment>` lo agrega Fury como último token y nunca se inventa ni se escribe a mano.
- Sin nombres base pelados: el web principal parte como `prod-api` y Fury lo materializa `prod-api-nonsite`, nunca `prod`.
- El ambiente lógico y el profile/config se resuelven explícitamente; nunca desde el último token `nonprod/nonsite` agregado por Fury.
- Con un único runtime del tipo, `<role>` toma el valor canónico del tipo; no se omiten tokens.
- `<environment>` ≠ `<segment>`: un runtime `nonprod` puede ser `stage` o `alpha`; el primer token los distingue.
- `legacy` no es segmento objetivo: todo runtime `legacy` se migra (`prod→nonsite`, resto→`nonprod`) y recién ahí toma nombre canónico.
- `prod`, `stage` y `alpha` obligatorios por app desplegable; `staging` se normaliza a `stage`; `beta/gamma` sólo con la lane end-to-end.

Vocabulario canónico de `role`:

| Runtime Fury | role canónico | Split permitido |
|---|---|---|
| web | `api` | `inbound` / `outbound` |
| bigqueue | `consumer` | `<qualifier>` |
| stream | `events` | `<qualifier>` |
| template_processing | `processor` | `<qualifier>` |
| work_queue | `worker` | `<qualifier>` |
| job | `job` | `<qualifier>` |

Tokens sucios (`bq`, `jobs1`, `test2`, `develop`, `--tp`, segmento intercalado) se normalizan a este vocabulario.

### Criterios para más de un scope del mismo tipo en el mismo ambiente

> **Baseline: 1 scope por (ambiente × tipo de runtime).** Un segundo scope del mismo tipo es una excepción que **se justifica y se documenta**, nunca el default.

Se permite un scope adicional del mismo tipo+ambiente sólo si aplica ≥1 criterio, registrado:

1. **Criticidad / blast radius distinto** — exigen escalado, cadencia de deploy o aislamiento de fallas independientes (ej. consumer real-time crítico vs consumer de backfill/bulk).
2. **Alertas / observabilidad divergentes** — umbrales, on-call o dashboards genuinamente distintos porque el comportamiento *normal* difiere, no por cosmética.
3. **Endpoints / contrato divergentes** — web o stream con dirección, forma de tráfico o contrato público materialmente distinto (ej. `inbound` gateway vs `outbound` webhook).
4. **Aislamiento mandado** — plataforma o compliance exige separación física.

Sin ningún criterio → **colapsar** a un único scope del tipo. El scope extra se nombra con `role` alterno (`inbound`/`outbound`) o `qualifier` (`prod-consumer-bulk-nonsite`), jamás dos nombres iguales.

### Regla "cortar o mantener" para apps con scopes redundantes

Toda app con >1 scope del mismo tipo+ambiente, o con tokens fuera del vocabulario, se marca en `rio-scope-policy.json` con un bloque `consolidation_decision`:

```text
consolidation_decision:
  type: <runtime type>
  environment: <prod|stage|alpha|...>
  candidates: [<scopes actuales + from>]
  proposed_action: collapse | keep_split
  justification: <criterio 1–4 que lo sostiene | "sin particularidad → colapsar">
```

Ni cortar ni mantener se aprueba sin justificación explícita contra los criterios. El estándar sólo obliga a que la decisión **exista y sea trazable**; el equipo la ratifica en la fase de Alineación.

### Ejemplos aplicados

- **rio-controlplane-clickhouse / prod** → `prod-api-nonsite` · `prod-consumer-nonsite` · `prod-events-nonsite` *(Stream con `decision_required`)*.
- **rio-controlplane-clickhouse / alpha** → `alpha-api-nonprod` · `alpha-consumer-nonprod` · `alpha-events-nonprod` · `alpha-job-nonprod` *(job sin función clara → `consolidation_decision`)*.
- **rio-controlplane-fury / prod** → hoy 6, mínimo **4**: `prod-api-nonsite` · `prod-consumer-nonsite` · `prod-events-nonsite` · `prod-processor-nonsite`. `inbound`/`outbound` entran a `consolidation_decision`: se conservan como `prod-inbound-nonsite` / `prod-outbound-nonsite` sólo si justifican el criterio 3; si no, colapsan en `prod-api-nonsite`.

### Recomendación de consolidación

- Consolidar consumers BigQueue duplicados en **un runtime por aplicación y grupo**, salvo aislamiento documentado de escala, criticidad o contrato.
- Migrar runtimes productivos `legacy` a `nonsite` y runtimes de test/stage a `nonprod` antes de retirar sus equivalentes antiguos.
- Consolidar variantes `test`, `test2`, `test3`, `develop`, `api-test` bajo lanes `alpha/beta/gamma` sólo cuando su propósito sea equivalente; si el workload difiere, conservarlo como role/workload explícito.
- No migrar automáticamente los 15 Streams: ninguno tiene sink activo. Los 12 pausados y 3 sin enlace HTTP llevan punto amarillo para decidir retiro o mantener con binding explícito.
- Jobs y Template Processing requieren role/workload explícito; no se consideran runtime principal genérico.

### Arquitectura de ambientes

El header y el filtro resuelven tramos distintos. El front traduce el selector `backend` al header estándar de scope para Fury routes; Playmaker convierte el scope validado en `environment_scope` y estampa el tag `scope:<x>`. `modified_fields` es la clave de transporte del SDK y acepta tags de negocio arbitrarios; falta confirmar si Fury aplica el filtro antes de entregar el mensaje.

```text
?frontend=alpha&backend=beta / cookie MeliLab
  --> nginx sirve front alpha
  --> header de scope --> Fury route --> Playmaker beta
  --> tag scope:beta --> topic compartido
  --> consumer Fury beta --> guard scope == beta
```

Decisión recomendada:

1. Mantener un vocabulario cerrado `prod|stage|alpha|beta|gamma` en el SDK.
2. Validar el header contra el ambiente persistido; si no coincide, rechazar la solicitud.
3. Agregar `environment_scope` a triggers, results y estados relacionados para preservar correlación.
4. Publicar en un topic compartido y estampar `scope:<environment_scope>` como tag de filtro server-side; el consumer revalida el scope como defensa en profundidad.
5. Separar prod en su propio topic sólo si Fury confirma que el filtro por tag no se aplica antes de la entrega.
6. Mantener el mapping físico independiente: `prod→nonsite`, resto→`nonprod`.

El alta de `beta` o `gamma` se vuelve mecánica: registrar el ambiente en Playmaker, aprovisionar scopes/consumers de ese ambiente, enlazar el filtro `scope:<x>` y ejecutar la matriz E2E. No exige inventar `nonprod-beta`: Fury agrega `nonprod` al nombre base materializado.

### Piloto de migración — `rio-controlplane-kms`

- **Propuesta:** usar la segmentación obligatoria de `test` antes del 2026-09-09 como primer slice vertical: base RIO `alpha-api`, visible Fury `alpha-api-nonprod`; `test-nonprod` queda como bridge sólo si la remediación lo exige.
- **Qué ganamos:** cumplimiento, salida verificable de `legacy`, naming canónico, canary/rollback y una plantilla reusable para el resto de RIO.
- **Qué implica:** confirmar el nombre aceptado y la señal de cumplimiento; desacoplar Spring profile del último token `nonprod/nonsite`; crear scope+routes; desplegar, probar y mover tráfico gradualmente.

### Extensión a Secrets y KVS

La base reserva identidad `application/scope/resource_type/resource_name` y los tipos `secret` y `kvs`. Hasta implementar sus collectors, cada scope guarda `collection_status=not_collected`; el reporte no puede afirmar que esos recursos no existen.

## Edge Cases

- Un runtime `Desired` puede estar sano en scale-to-zero; la vista no lo presenta como inactivo.
- Un runtime Streams puede estar `Healthy` y, a la vez, su sink asignado estar pausado; compute y binding se muestran por separado.
- `pusher-sink-*` usa nombres de sink, pero es un runtime Streams sin join HTTP directo en el grafo consultado.
- El worker group de stage tiene un campo general stale que apunta a test, pero su registro segmentado y efectivo apunta a `work-queues-stage`; la edge se une a stage y la contradicción queda registrada.
- `runtime_segment=nonsite` puede coexistir con un recurso Stream en `physical_segment=legacy`; ambos son hechos distintos.
- Un scope inactivo puede no aparecer en `scopes status -j`; lifecycle se conserva desde el service graph.
- Dos versiones de config con formatos distintos se marcan `different`; no se ordenan ni se llama a una “behind” sin evidencia adicional.
- Que Config Orchestrator no entregue latest approved no demuestra ausencia de configuración runtime.

## Non-Functional Requirements

- Collector read-only; no crea, actualiza ni elimina recursos Fury.
- Persistencia allowlisted; no guarda el payload raw, endpoints internos, ARNs ni nombres de secretos.
- Salida determinística para un mismo snapshot: orden por aplicación, ambiente y scope.
- Generación fatal ante pérdida de una aplicación, duplicados o bindings runtime sin resolver.
- HTML responsive, accesible por teclado y sin dependencias externas.
- El reporte abre localmente sin servidor ni acceso adicional a red.

## Dependencies

- Fury CLI `5.20.0` y método core `furycli.furyapi.FuryApi.get_scopes`.
- Plugins observados: `cli-services 1.51.0` y `cli-scopes 0.1.0`.
- `mqclient 3.4.9`: `Producer.send(message, Filters)` existe, pero `Filters` sólo modela `modified_fields`.
- Contratos de `rio-sdk-events` para incorporar `environment_scope` de manera compatible.
- Sesión autenticada de Fury con acceso read-only a las 10 aplicaciones.
- Python del entorno Fury; el comando reproducible actual es `cd ~/fuentes && pyenv exec python rio-inspector/scope_inventory.py collect`.

## Evidencia y provenance

- Baseline y bindings: `~/fuentes/rio-inspector/rio-scopes.json`, generado desde el service graph Fury y reconciliado con `scopes status`.
- Collector: `~/fuentes/rio-inspector/scope_inventory.py`, con versiones de Fury persistidas y allowlist explícita.
- Estructura funcional: espejo local de SIG-257 y specs comparables de Signals; los links SIG-72/SIG-347 quedaron bloqueados por SSO en esta sesión.
- Documentación derivada: [[scope-inventory]] y `30-resources/grids/rio-scope-inventory.html` salen del mismo JSON.

## Risks and Mitigations

| Riesgo | Mitigación |
|---|---|
| El service graph no es un contrato CLI público estable | Adapter único, allowlist de campos, versiones persistidas y validaciones fatales. |
| `list-infra` y repo local omiten runtimes | Autoridad primaria en el service graph; reconciliación contra `scopes status`. |
| Un nombre sugiere un segmento incorrecto | Nunca usar naming para poblar `runtime_segment`; mostrar nombre y facts por separado. |
| Confundir binding configurado con tráfico | Copy explícito “relación observable, no tráfico”; no hay categoría genérica. |
| Payload raw contiene referencias internas | No persistir raw; normalización in-memory con allowlist. |
| Un join cambia o queda ambiguo | Validar tipo target y detener publicación si queda unresolved. |
| El checkout local difiere del build desplegado | Persistir commit/branch junto al resultado, mostrarlo como “resoluble en código inspeccionado” y validar contra el build antes de ejecutar cambios. |
| Un caller falsifica el header de ambiente | Playmaker valida el valor contra ambiente persistido y autorización; no acepta un scope Fury libre. |
| Alpha y stage comparten segmento nonprod | Separar por topic lógico y consumer; el segmento sólo controla placement físico. |
| Un mensaje llega al topic equivocado | Guard obligatorio de `environment_scope` en el consumer, métrica de mismatch y DLQ/ACK según contrato acordado. |
| Crear todos los ambientes multiplica infraestructura | Prod/stage/alpha son baseline; beta/gamma se activan mediante plantilla/manifiesto y sólo cuando la lane existe end-to-end. |

## Success Metrics

- 100% de los runtimes del service graph representados una vez.
- 100% de los runtimes activos reconciliados con `scopes status -j`.
- 0 bindings runtime sin resolver y 0 IDs duplicados al publicar.
- 100% de los scopes con `source` y `observed_at`.
- 100% de los conteos del reporte derivados desde el JSON.
- 100% de los Web con route reportada o ausencia explícita.
- 100% de los scopes con profile/archivo local resuelto y artifact Fury registrados por separado.
- 0 clasificaciones genéricas de uso y 0 segmentos efectivos inferidos desde nombres.
- 100% de las aplicaciones con propuesta `prod`, `stage` y `alpha`.
- 100% de las filas de propuesta clasificadas como retirar/mantener/agregar y ordenadas de forma determinística.
- 0 mensajes procesados por un consumer cuyo `environment_scope` no coincide con su scope efectivo.

## End-to-End Acceptance Scenarios

### E2E-1 — Caso nonsite verificado

1. Ejecutar el collector.
2. Buscar `rio-controlplane-observability/consumer-prod-nonsite`.
3. Verificar runtime segment `nonsite` desde `metadata.segment`.
4. Verificar consumer `rio-deployment-consumer--nonsite`, estado `running`, topic `rio-deployment-trigger--nonsite.rio-playmaker` y segmento de binding `nonsite`.
5. Verificar pill `consumer activo · 1` y ausencia de una etiqueta genérica.

### E2E-2 — Stream compute sano con binding pausado

1. Buscar `rio-materializer/stream-test`.
2. Verificar runtime segment `legacy` y health Fury independiente.
3. Verificar sink HTTP `sink-test-controlplane-events` unido por ID.
4. Verificar `enabled=false`, `user_status=PAUSED_LOOSING_DATA` y pill `sink pausado · 1`.

### E2E-3 — Contradicción Work Queues stage

1. Buscar `rio-materializer/work-queues-stage`.
2. Verificar que `wg-materialize-request-stage` se une por `worker_group_segments[].scope=work-queues-stage`, no por similitud de nombre.
3. Verificar que el binding conserva `declared_scope=work-queues-test` y `mapping_conflict=true` para no esconder el campo stale.

### E2E-4 — Web sin clasificación artificial

1. Filtrar runtime `web`.
2. Verificar que no aparece pill de consumer, sink, worker group o binding genérico.
3. Verificar lifecycle, health, ambiente y segmento runtime sin penalización por ausencia de binding.

### E2E-5 — Diff de propuesta

1. Abrir la propuesta de una aplicación.
2. Verificar que todos los scopes retirados aparecen primero con borde rojo.
3. Verificar que los mantenidos tienen borde gris y los agregados borde verde.
4. Verificar el orden posterior `prod`, `stage`, `alpha`, `beta`, `gamma`.
5. Verificar que sólo los Stream objetivo llevan punto amarillo.

### E2E-6 — Routing alpha

1. Abrir una sesión interna con `?frontend=alpha&backend=beta` y verificar que ambos ejes persisten independientemente.
2. Verificar que nginx sirve el front alpha y que Fury routes dirige el header de scope al Playmaker beta.
3. Verificar que Playmaker estampa `scope:beta` y que sólo el consumer beta recibe el mensaje.
4. Alterar el tag o payload para producir mismatch y verificar que el guard del consumer no ejecuta la operación.
5. Repetir para prod y stage; beta/gamma se prueban sólo cuando estén habilitados y un usuario no interno siempre falla cerrado a prod.

## Rollout

1. Ejecutar collector y gates de reconciliación.
2. Revisar el JSON normalizado y los casos E2E de nonsite, Streams y Work Queues.
3. Renderizar Markdown y HTML desde el snapshot aprobado.
4. Aprobar el diff retirar/mantener/agregar por aplicación; resolver los 15 puntos amarillos de Streams.
5. Ejecutar primero el piloto KMS: corregir la resolución de profile, crear scope+routes, validar tráfico NONPROD y mantener `test` como rollback.
6. Implementar el contrato `environment_scope`/tag `scope:<x>` en SDK, Playmaker y consumers, con compatibilidad de payload.
7. Aprovisionar scopes prod/stage/alpha mediante plantilla; ejecutar E2E y sólo entonces extender al resto y retirar nombres antiguos.

## Open Decisions

1. ¿El collector vivirá en `rio-inspector` o debe migrarse a un repo Signals con CI y ownership formal?
2. ¿Qué canal publicará el snapshot y con qué cadencia?
3. ¿Se agregará una superficie oficial de Fury para Streams/Work Queues o se mantendrá el adapter sobre el service graph?
4. ¿Cómo se mostrarán en una próxima iteración los recursos no runtime, como topics, streams físicos y KVS, sin colapsarlos al scope?
5. ¿Cuál será la política de compatibilidad para mensajes antiguos sin `environment_scope` durante el rollout?
6. ¿Fury acepta `alpha-api-nonprod` para remediar `rio-controlplane-kms/test` o exige el bridge `test-nonprod`, y qué señal levanta la restricción de deploy?
7. ¿El filtro `scope:<x>` se aplica server-side en la definición Fury del consumer o después de la entrega?

## Relaciones

- Fuente generada: [[scope-inventory]]
- Routing: [[scope-compatibility-matrix]]
- Segmentación: [[fury-segmentation-model]]
- Entregable visual: `30-resources/grids/rio-scope-inventory.html`
- Proyecto: [[Estandarización de Scopes RIO]]
- Atlas: [[00-index|RIO Atlas]]
