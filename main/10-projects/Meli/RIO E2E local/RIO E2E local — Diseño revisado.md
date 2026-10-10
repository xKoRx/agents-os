---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: ["[[RIO E2E local]]", "[[Kafka — Ambiente local con servicios reales]]", "[[rio-playmaker]]", "[[rio-controlplane-kafka]]", "[[rio-controlplane-clickhouse]]", "[[rio-controlplane-flink]]", "[[ads-signals-frontend]]"]
aliases: ["rio-e2e-local-diseno", "Diseño RIO E2E local"]
tags:
  - kind/doc
  - area/meli
  - project/rio-e2e-local
created: "2026-10-09"
updated: "2026-10-09"
---

# RIO E2E local — Diseño revisado

## Propósito

Diseño objetivo del ambiente local con cinco aplicaciones reales (Playmaker, ads-signals-frontend, CP Kafka, CP ClickHouse, CP Flink) donde triggers y resultados de deployment viajan por Kafka mediante consumers/producers embebidos, sin bridge ni relay HTTP. Describe estado objetivo, contratos, cambios mínimos por repo, plan de verificación y bloqueos. La autorización vigente y la entrega certificada F1 se registran en [[RIO E2E local]].

## Contenido

### Veredicto

Viable para Playmaker, CP Kafka y CP ClickHouse con efectos físicos reales y cero o casi cero cambio en `src/main`. CP Flink tiene hoy transporte, guards y FAILED real alcanzables; su despliegue físico está **BLOCKED** hasta demostrar el seam mínimo hacia un job Flink real. Front con journeys alcanzables una vez integrados los fixtures de referencia (templates/grants) y las actions que usan esos journeys. La certificación final conserva el alcance completo: efectos reales en Kafka, ClickHouse y Flink, más journeys browser por CP. Las fases intermedias pueden entregar menos, pero no redefinen el criterio de cierre: si un seam no se demuestra, el resultado final es BLOCKED, no un PASS reducido. El inventario y el challenge siguientes conservan el snapshot de discovery anterior a la implementación. F1 Playmaker + Kafka fue implementada y certificada el 09/10; su matriz vigente se actualiza abajo y su evidencia completa vive en [[RIO E2E local]]. CH/Flink/front no adquieren certificación por esa entrega parcial del proyecto.

**Snapshot previo a implementación/publicación:** base leída PM `origin/develop` 44c2905 y CP Kafka 6a91937 (iguales al remoto por `ls-remote` el 09/10); CH c8b20b6, Flink 7c645ea, front a3f82ab y rio-frontend 6d644ec, cuyos `develop` remotos avanzaron a ac4662a, 579a6ce, 01e19bc y d977028 sin poder leerse sin fetch.

### Tabla por aplicación — snapshot previo a ejecución

| App | Capacidad / seam observado | Frontera sustituida | Cambio mínimo | Riesgo | Estado |
|---|---|---|---|---|---|
| rio-playmaker | `LocalKafkaDeploymentTriggerProducer` (key=deploymentId, `acks=all`, idempotente, `.get(10s)`) y `LocalKafkaDeploymentResultListener` → mismo `DeploymentResultConsumerService.consume` que el controller productivo; DLT `rio-deployment-result-local-dlt` | BigQueue→Kafka; Tiger mock local; Entity/Approvals/Materializer stubs; KVS de actions NoOp | Config (puerto, timeouts productivos por tipo) y modo broker externo del launcher; fix DEPROVISION por PR propio | Medio: timeouts 10s y undeploy | NO_EJECUTADO (sólo `LocalKafkaDeploymentTransportTest` con mocks) |
| rio-controlplane-kafka | Entrada sólo HTTP con guards inline en `DeploymentTriggerController.handleEvent`; resultados Kafka ya existen (`LocalKafkaBigQueueClient`, sin key, tópico fijo `local-deployment-result`) | BigQueue→Kafka; KVS mapa por JVM con CAS; auth GCP deshabilitada | Listener en `src/local`; tópicos como propiedad; key; init de tópicos en Compose. 0 líneas en `src/main` | Bajo | NO_EJECUTADO (standalone25 PASS 08/10 es HTTP→resultados Kafka) |
| rio-controlplane-clickhouse | Entrada HTTP inline en `DeploymentEventController.receiveEvent(@Valid envelope, BindingResult)`; resultados locales a archivo (`BigQueueClientFactory`→`LocalFileBigQueueClient`); motor single-node suficiente para MergeTree/MV | BigQueue→Kafka; KVS/lock/KMS locales existentes | Source set local, listener, factory Kafka `@Primary`, Compose CP+ClickHouse fijado | Medio: versión ClickHouse, ownership local no-op | NO_EJECUTADO |
| rio-controlplane-flink | Entrada HTTP inline en `handleDeploymentTrigger(BigQueueMessage)`; publisher local = logger (`LocalBigQueueDeploymentPublisher`, `@Profile("local")`); despliegue vía AWS KDA SDK (us-east-1, sin `endpointOverride`) o Fury Cloud Controller + Dataproc | BigQueue→Kafka | Listener y publisher Kafka en `src/local`; 1 anotación de perfil en `src/main`; seam físico mínimo por demostrar | Alto: arranque local GCP no verificado; seam físico desconocido | Transporte NO_EJECUTADO; físico BLOCKED |
| ads-signals-frontend | BFF Nordic→PM con `PLAYMAKER_BASE_URL` (debe empezar con `http://localhost`); polling 2–5 s; journeys kafka-topic, clickhouse-mergetree/matview, flink-sql/job; `list-warehouse/list-database` son actions asíncronas (`action_id` + polling) | Tiger dev token; IAM bypass y mocks de desarrollo existentes | Sin código en el front; fixtures de referencia y actions del lado PM/CP | Alto: templates ULID de PM test, grants ACME, actions | NO_EJECUTADO; depende de fixtures y actions |

rio-frontend queda fuera: su listado está fijado a `environment = 'legacy'`, la base URL de Playmaker está hardcodeada y despliega con el modelo antiguo de definitions/services.

### Challenge priorizado

| # | Supuesto | Evidencia (observado) | Fallo / impacto | Decisión | Corrección menor |
|---|---|---|---|---|---|
| 1 | Existe una entrada compartible bajo HTTP en cada CP | Los tres CP tienen guards (tipo, schema, context, routing, métricas, async) dentro del método del controller; ninguno tiene ingress reutilizable | Llamar al processor salta guards; llamar al controller no reproduce binding, `@Valid`, filtros ni exception handlers MVC | Cambiar | Adapter local pequeño que invoca el handler (opción A) sólo con pruebas de paridad HTTP↔Kafka; B donde A no conserve limpiamente la capa MVC (candidato: CH por `@Valid` + `BindingResult`) |
| 2 | CP Kafka ya publica al tópico que PM escucha | CPK publica a `local-deployment-result` (fijo en `LocalFunctionalAdaptersConfiguration`); PM escucha `rio-deployment-result-local` | Resultados nunca llegan a PM | Cambiar | Nombre de tópico como propiedad con default actual; el modo ecosistema usa `rio-deployment-result-local`; standalone25 intacta |
| 3 | Un broker compartido sin fricción | PM develop trae su propio broker (`docker-compose.kafka.yaml`, host 39092) y `LocalKafkaBootstrapGuard` exige `127.0.0.1:<port>` | Dos brokers colisionan en 39092; PM no puede ir en contenedor sin tocar `src/main` | Mantener broker dueño CPK | PM en host contra `127.0.0.1:39092`; launcher PM con modo broker externo; tópicos creados por el init del Compose CPK |
| 4 | CH y Flink ya pueden publicar resultados reales | CH local escribe archivos; Flink local reemplaza el publisher real por un logger y el real es `@Profile("!local")`; ninguno tiene `kafka-clients` | Sin resultados en PM | Cambiar | CH: `BigQueueClientFactory` local `@Primary` que entrega cliente Kafka. Flink: subclase local del publisher real con factory Kafka y `LocalBigQueueDeploymentPublisher` a `local & !local-kafka` |
| 5 | El payload cruza sin pérdida | SDK PM 1.5.0 y CH 1.6.1 tienen `context`; CPK y Flink 1.3.1 no. CH exige `context` salvo DEPROVISION | Si el listener tipa y re-serializa, pierde campos; CH rechazaría con FAILED | Cambiar | Listener nunca tipa: árbol JSON → `{"msg": árbol}`; un value que ya trae `msg` es poison (DLT), nunca doble envelope |
| 6 | Una imagen Flink + CP = E2E físico | KDA SDK fija `US_EAST_1` sin override; GCP usa Fury Cloud Controller (IaC/Terraform) + Dataproc; `FlinkCloudAdapter` sólo monitorea | No hay runtime local alcanzable con código existente | Mantener en el criterio final | BLOCKED documentado y spike para demostrar el seam mínimo hacia un job real; tamaño del cambio y RAM son estimaciones a medir |
| 7 | El front cubre los tres CP con deployments | PM local: actions producer no-op, KVS de resultados NoOp, PEEK sintético. El front usa actions para PEEK Kafka y para `list-warehouse/list-database` de ClickHouse (`api/technologies/clickhouse-mergetree/action-databases.ts`) | Journey UI ClickHouse no completa sin actions | Cambiar | Incluir las actions que usan los journeys iniciales: transporte Kafka de actions en PM y CPs y KVS local de resultados con semántica CAS/TTL declarada |
| 8 | El undeploy funciona con transporte real | Fix DEPROVISION sólo en rama HTTP (staged): guard terminal por operación y publish `afterCommit` en `UndeployServiceImpl` | Undeploy E2E FAIL con cualquier transporte | Mantener fuera del transporte | Rama propia del fix como dependencia explícita de la rama E2E; verificar si `InactivationResultHandler` (camino del front) está afectado |
| 9 | Timeouts locales no influyen | `deployment-result.timeout` local = 10 s para todos los tipos | `DeploymentTimeoutJob` marca FAILED y descarta el terminal tardío | Cambiar | Valores productivos por tipo en `application-local-integration.yml`; nunca delays |
| 10 | Auth/datos del front se resuelven solos | Tiger local es mock con identidad sintética (`KAFKA_HTTP.md`); `acmeClient.base-url` local apunta a ACME real; templates del front son ULIDs de PM test no sembrados en develop | 403/404 en grants y templates inexistentes | Cambiar | Fixtures mínimos de templates y grants en `src/local` de PM (fixture ACME de la rama HTTP), validaciones activas |
| 11 | Kafka mejora la fiabilidad del resultado CPK | `DeploymentResultPublisher.publish` captura y loguea; `finalizeOutcome` antes de publicar; replay → `Drop(TERMINAL)` sin re-emitir; GCP con `operation` null publica FAILED sin claim | Resultado perdido no se recupera | Conservar | Caso de prueba que evidencia el gap: PM termina FAILED por timeout con tópico físico creado. Corrección productiva fuera de alcance |
| 12 | Compartir tópico es seguro | Los tres CP responden 200 sin publicar ante `component_type` ajeno | Con group compartido, un CP recibe el trigger de otro, lo ignora y nadie lo procesa | Mantener tópico, cambiar groups | Un group por CP; observer con `assign()` sin group |
| 13 | ACK Kafka = procesado | En los tres CP el 2xx es recepción y el proceso es async | Crash entre commit y proceso pierde el trigger (igual que BigQueue) | Mantener paridad | Commit tras 2xx. El timeout de PM sólo hace visible el fallo: no recupera la operación y el motor puede haber cambiado. No prometer más |
| 14 | ClickHouse `latest` sirve | Compose HEAD usa `latest`; cambio ajeno sostiene que 25.8 rechaza `format=` del cliente on-prem; ownership local no-op; connector Kafka exige ON CLUSTER/Keeper/S3; UPDATE de MV no soportado | Resultado depende de la imagen; algunos FAILED son de negocio | Cambiar | Releer develop vigente y preservar cambios ajenos; fijar la versión on-prem productiva si se obtiene, si no una versión elegida por pruebas físicas y declarada sin paridad productiva; connector fuera; MV UPDATE se registra como FAILED de negocio |
| 15 | Bases vigentes conocidas | `develop` local ≠ `origin/develop` en PM, CPK y front; remotos CH/Flink/front avanzaron | Diseño de CH/Flink/front puede estar desfasado | Cambiar | Fetch autorizado y relectura del delta antes de las SPEC |
| 16 | "standalone25" es Java 25 | Es la suite de 25 tests `LocalKafkaFlowsTest`; CPK compila a Java 21; PM, CH y Flink usan toolchain 25 | Homogeneizar rompería builds | Mantener | Cada imagen con su JDK; sin downgrade |

### Arquitectura revisada

```text
 host macOS                                    VM colima-rio · red rio-local
 ┌──────────────────────┐                      ┌───────────────────────────────────────────────┐
 │ ads-signals-frontend │                      │ rio-kafka (dueño: Compose CP Kafka)           │
 │ nordic dev :8443     │                      │   rio-deployment-trigger-local  (P=1)         │
 └─────────┬────────────┘                      │   rio-deployment-result-local   (P=1)         │
           │ BFF HTTP                          │   DLTs · tópicos de negocio prefijados por CPK│
           ▼                                   │        ▲ 127.0.0.1:39092   ▲ rio-kafka:19092  │
 Postman/JUnit ─HTTP─► Playmaker :39080 ───────┼────────┘                   │                  │
                       bootRun local,          │  CP Kafka      :39081 ◄────┤ rio-cp-kafka-local       │
                       local-integration       │  CP ClickHouse :39082 ◄────┤ rio-cp-clickhouse-local  │
                       MySQL :33306 (VM)       │  CP Flink      :39083 ◄────┘ rio-cp-flink-local       │
                                               │  ClickHouse (versión on-prem fijada) :39123   │
                                               └───────────────────────────────────────────────┘
```

**Responsabilidades.** PM: única entrada HTTP de negocio, persistencia, publish del trigger y consumo de resultados. Cada CP: un listener local que sólo traduce transporte (record → envelope → handler del controller) y un `BigQueueClient` Kafka bajo el publisher productivo; negocio, guards, idempotencia y publicación siguen siendo los productivos. Compose CP Kafka: broker y red `rio-local`; la topología de tópicos del ecosistema pertenece al runner PM. Cada otro repo: su Compose une la red externa y nunca crea ni borra broker o red.

| Tópico | Productor | Consumidores (group) | Key | Value |
|---|---|---|---|---|
| `rio-deployment-trigger-local` | PM `LocalKafkaDeploymentTriggerProducer` | `rio-cp-kafka-local`, `rio-cp-clickhouse-local`, `rio-cp-flink-local` | `deployment_id` | `DeploymentTriggerMessage` SDK crudo, snake_case |
| `rio-deployment-result-local` | Publisher productivo de cada CP vía `BigQueueClient` Kafka | `rio-playmaker-local-integration` (existente) | `deployment_id` | `DeploymentResultMessage` SDK crudo |
| `rio-deployment-result-local-dlt` | `DefaultErrorHandler` de PM | observer | original | original |
| `rio-deployment-trigger-local-dlt-<cp>` | listener del CP tras reintentos o poison | observer | original | original |

Una partición por tópico ordena los registros, y la key queda correcta si luego crecen las particiones. El orden de registros no ordena la ejecución: cada CP acepta y despacha async (virtual threads), así que dos triggers del mismo componente pueden ejecutarse solapados igual que con BigQueue. La suite espera el terminal de una operación antes de lanzar la siguiente y sólo exige orden STARTED→terminal dentro de una operación. `auto.offset.reset=earliest` con group estable evita perder registros, pero no elimina carreras. Readiness explícita antes del primer caso: tópicos existentes (`auto.create` está apagado y un send previo falla), cada group `Stable` con su partición asignada (AdminClient `describeConsumerGroups`), healthchecks de apps y motores y PM consumiendo resultados. No se usan delays. El observer E2E usa `assign()` sin `group.id`, así nunca participa en un group.

**Secuencia normal, ACK y errores**

```text
Front/Postman → PM API → tx persiste ejecución/deployment → commit
PM AFTER_COMMIT (pipeline) / commit previo (deploy v2) → send(key).get(10s), acks=all
   └ timeout/error → QueueException → PM marca FAILED (paridad con BigQueue)
CP listener poll(1) → árbol JSON → {"msg": árbol} → handler del controller in-process
   ├ 2xx → commitSync (≡ ACK BigQueue: recepción, no fin de proceso)
   ├ excepción o no-2xx → sin commit → seek → backoff 1s ×2 → DLT-<cp> → commit
   └ no JSON / trae "msg" / > 256 KiB → DLT-<cp> sin reintento → commit
CP async (productivo): claim → STARTED → efecto físico → COMPLETED | FAILED
CP publisher productivo → BigQueueClient Kafka send(key).get(15s), acks=all
   └ error → absorbido por el publisher (gap productivo) → PM DeploymentTimeoutJob → FAILED
     (detección, no recuperación: el efecto físico puede existir con el resultado perdido)
PM listener → consume() con lock pesimista y guards → ack record
   └ inválido → DLT PM sin reintento; transitorio → 1s ×2 → DLT PM
```

La política de reintento/DLT del listener CP copia la que PM ya tiene en `LocalKafkaConfiguration` (`FixedBackOff(1000, 2)`); no es política de negocio nueva. FAILED de negocio viaja como resultado normal y nunca se reintenta; payload inválido va a DLT; fallo de transporte se reintenta acotado.

**Replay, duplicados, restart y shutdown.** Trigger reentregado: CPK descarta por KVS (`Drop(TERMINAL)`, sin re-emitir), CH por `isAlreadyCompleted`, Flink AWS por claim y Flink GCP sin claim. Resultado duplicado o tardío: PM descarta por `terminal_state` o `stale_after_terminal`. Restart de un CP: la memoria KVS se pierde pero los offsets comprometidos viven en el broker, así que no relee lo ya aceptado. Rebalance sólo ocurre en restart (un consumer por group); el listener hace `commitSync` en revocación. Shutdown: el listener deja de hacer poll, comete y cierra antes de que Spring cierre el executor; el trabajo async en curso se pierde igual que en producción, por eso la suite espera estados terminales en PM y efectos físicos antes de bajar contenedores.

### Alternativas sin bridge

| Criterio | A · listener invoca el handler del controller | B · extraer `*TriggerIntake` en `src/main` |
|---|---|---|
| Cambio productivo | 0 en CPK y CH; 1 anotación en Flink | 3 clases nuevas + 3 controllers + tests (actions duplica) |
| Paridad | Mismo método de negocio, pero la capa MVC (binding, `@Valid`, filtros, exception handlers) no se reproduce: se demuestra con pruebas | Refactor mecánico verificado por los tests existentes del controller |
| Diferencias | Salta `CorrelationIdFilter` (CPK) y `RoutingFilter` (CH); CH necesita reproducir `@Valid` + `BindingResult`; las excepciones no pasan por `ControllerExceptionHandler` | Ninguna en negocio |
| Acoplamiento | Adapter local depende de una clase web; un cambio de firma rompe `compileLocalJava` en `check` | Adapters dependen de un puerto de aplicación |
| Coste | ~80 LOC locales por CP, sin PR productivo | PR productivo por CP, review y release del equipo |

Elegida **A por CP, condicionada a paridad demostrada**. Prueba de paridad obligatoria por CP: la misma matriz de entradas (válida, tipo ajeno, schema futuro, sin `deploymentId`, context inválido, JSON malformado, binding inválido) por MockMvc y por el listener debe producir las mismas invocaciones al processor, resultados publicados y métricas; las entradas que por HTTP dan 4xx/5xx deben terminar en DLT o reintento según la tabla de errores. Se usa **B** en el CP donde A no conserve limpiamente esa capa: el handler exige objetos servlet, `RoutingFilter` afecta negocio aguas abajo, o reproducir `@Valid`/`BindingResult` obliga a reimplementar MVC. CH es el primer candidato a B y se decide con esa prueba, no por preferencia.

**Se elimina de la propuesta:** bridge/relay de cualquier tipo; broker propio de PM en modo ecosistema; extracción de handlers por defecto; librería común o soporte Kafka en el SDK; mapas KVS nuevos en PM para deployments (no los usan); segundo front; tópicos de trigger por CP; envelope dentro de Kafka; puertos ClickHouse 8123/9000 publicados en host; imágenes `latest`; delays.

### Inventario de cambios por repo

| Repo | `src/main` | Local / build / Compose | Pruebas de paridad |
|---|---|---|---|
| rio-playmaker | 0 por transporte. Fix DEPROVISION en rama propia (`UndeployServiceImpl`, `DeploymentResultHandlerImpl`, `DeploymentLogRepository`), extraído selectivamente de LOCAL-HTTP-2 | `application-local-integration.yml` (timeouts productivos); `local/00-integration-pipeline.sh` modo broker externo; transporte Kafka local de actions (producer + listener de `/events/actions/result` equivalente, extraídos de `kafka-real-e2e` sin gate Sandbox); KVS local de resultados de actions con CAS/TTL declarados; fixtures mínimos de referencia (templates con los ULIDs del front y grants ACME) sin desactivar validaciones; suite E2E en source set de prueba local; `.testing/impact.json` y `execution-plans.json` con el runner declarado | Suite completa + `LocalKafkaDeploymentTransportTest`; tests de adapters de actions; jar productivo sin cambios |
| rio-controlplane-kafka | 0 | `src/local`: `LocalKafkaTriggerListener`; `LocalFunctionalAdaptersConfiguration` con nombres de tópico como propiedad y key; listener de actions para PEEK; `docker-compose.yml` init de tópicos y DLT; `local/README.md` | standalone25 25/25; paridad HTTP↔Kafka; `localTest` del listener (mismo árbol al controller, commit sólo tras 2xx, poison→DLT, tipo ajeno sin resultado); `bootJar` sin clases locales |
| rio-controlplane-clickhouse | 0, salvo que `BigQueueClientFactory` no sea sustituible por bean (1 anotación) | `build.gradle` source sets `local`/`localTest`, `localImplementation kafka-clients`, `localBootJar`; listeners de deployments y de actions (`list-warehouse`, `list-database`), `LocalKafkaBigQueueClient`, factory `@Primary`; Compose con CP y ClickHouse fijado; `Dockerfile.local`. Si la paridad de A falla: intake extraído en `src/main` (B) | Tests existentes; paridad HTTP↔Kafka incluido `@Valid`/`BindingResult`; `bootJar` sin clases locales |
| rio-controlplane-flink | 1 anotación: `LocalBigQueueDeploymentPublisher` → `local & !local-kafka` | Igual patrón que CH; `LocalKafkaDeploymentPublisher extends BigQueueDeploymentPublisher` sin overrides; config local si el arranque exige containers KVS | Tests existentes; listener; arranque `local,local-kafka` |
| ads-signals-frontend | 0 | Env local (`PLAYMAKER_BASE_URL=http://localhost:39080`, `TIGER_DEV_TOKEN`); datos de referencia vía fixtures de PM; pruebas browser con `nordic-e2e-toolkit` si soporta el journey (por verificar) | Journey browser por CP disponible |

Tres copias pequeñas del listener y del cliente Kafka son aceptables: viven en código local, difieren en el handler invocado y un SDK compartido exigiría release desde master. Se reevalúa al sumar el cuarto CP con copias idénticas.

**Límites productivos que se conservan:** endpoints, DTOs, validaciones, routing, defaults, handlers, estados, errores, publishers (incluido el gap CPK), idempotencia y capacidades. GCP PEEK sigue FAILED/INVALID_PARAMS/`unmapped` sin STARTED. Kafka local no certifica BigQueue; Tiger mock no certifica JWT/OAuth; fixtures ACME no certifican ACME; mapas KVS no certifican persistencia tras restart ni coordinación entre JVMs.

### Recursos y operación

| Proceso | Dónde | Memoria estimada (inferencia) |
|---|---|---|
| Broker + CP Kafka | VM | ~0,5 GiB (medido 08/10) |
| CP ClickHouse + ClickHouse server | VM | 0,6–0,8 + 1,0–1,5 GiB con `max_server_memory_usage` |
| CP Flink | VM | 0,5–0,8 GiB |
| MySQL PM | VM | ~0,4 GiB |
| Overhead VM | VM | ~0,6 GiB |
| Playmaker + front | host | ~1,5–2 GiB fuera de la VM |

Total VM estimado 3,6–4,9 GiB de 8 GiB: alcanza con `mem_limit` y `-Xmx` explícitos. Un runtime Flink real se estimó en 4–6 GiB (JobManager + TaskManager); es una estimación por medir, no un descarte: si no cabe, se dimensiona al demostrar el seam. Todo se mide con `docker stats` en la primera ejecución.

Compose por repo con nombres de proyecto únicos (`rio-kafka-local` existente, `rio-clickhouse-local`, `rio-flink-local`); jar copiado en `Dockerfile.local`, sin bind mount; healthchecks (`/ping`, `SELECT 1`, `mysqladmin ping`, listado de tópicos) y `depends_on: service_healthy`. Comandos con `-f "<repo>/docker-compose.yml" --project-directory "<repo>"` y `DOCKER_CONTEXT=colima-rio` por comando, sin cambiar el contexto activo. Limpieza en orden: front, PM, Compose CH y Flink (consumers salen del group), MySQL, Compose CPK (broker y red al final); sólo proyectos propios; la VM no se opera.

**Desviación operacional registrada09/10:** host ENOSPC seguido de I/O del perfil original impidió continuar. Se intentó stop/start y finalmente force-stop al fallar SSH, preservando disco/perfil y sin prune. Recertificación F1 usa el contexto existente saludable `colima-rio-kafka-e2e-01a0f8e0`, explícito y con baseline vacío; no cambia el contexto activo. `colima-rio` permanece offline y cleanup del run36868 NO CERTIFICADO; ledger privado íntegro en `fuentes + .rio-e2e-interrupted-state/36868d2dbe3d`. Esto no redefine la política normal ni acredita reparación/limpieza del perfil original. Verificación y contra-challenges vigentes en `rio-playmaker + meli/features/20261009-rio-e2e-local/4-implementation/SIMPLIFICATION_REVIEW.md`.

### Plan gradual y criterios de aceptación

1. **F0 — precondiciones.** Fetch autorizado y relectura del delta de CH, Flink y front; spike de sólo lectura para el seam físico mínimo de Flink; rama del fix DEPROVISION como dependencia explícita (ramas apiladas, sin exigir merge previo); SPEC funcional → técnica → tareas en Spellbook por repo afectado.
2. **F1 — PM + CP Kafka.** CERTIFICACIÓN LOCAL vigente09/10 fuente PM642aa53 (auth develop1ba12 íntegra) / CPb0d4587, PRs1286/86. Contrato22 selectors+3L0+L1 PASS, root44941be9e81d2×11 normal+2×1 gap; clones independientes810238a329de2×11 productivo y9444d48eba3d2×1 gap15s, cero fallos/errores/skips, cleanup propio PASS calificado al contexto sano. PR Kafka verde; PM CodeQL startup_failure no queda aprobado por la evidencia local. [[RIO E2E local]] conserva estado/continuidad actual. **Historia anterior a publicación:** K1–K6/X2–X4 y A2 backend PASS; standalone25 PASS; jars productivos aislados; simplificación recertificada fuentes90df/b0: normal2×11 y gap2×1 root(runf4ec56bb0c47), repetidas independientemente con presupuesto productivo normal(rund566b230fa3b) y stack nuevo15s gap(run12e65ac4a701); contexto saludable con limpieza exclusiva PASS. Las seis12/12 anteriores sólo certifican sus fuentes históricas. K3 físico cubre undeploy; inactivate conserva regresiones y su journey browser permanece en F4.
3. **F2 — + CP ClickHouse.** C1–C6 PASS (C6 como FAILED de negocio esperado).
4. **F3 — + CP Flink.** F1–F2 y X1 con los tres CP PASS; F3 físico PASS si el seam se demostró, si no BLOCKED registrado con el cambio mínimo requerido.
5. **F4 — actions y front.** A1–A2 PASS; B1–B3 PASS en browser. Un gap de UI se registra aparte del caso API equivalente.
6. **F5 — certificación de cinco apps con alcance completo** (Kafka, ClickHouse y Flink físicos más journeys browser). Dos suites seguidas sobre el mismo ambiente vivo, recreación vacía y repetición, reproducción desde clones limpios por otro agente; sin suites concurrentes; limpieza exclusiva verificada.
7. **Expansión.** Sólo después de F5: un CP por vez: módulo Compose + listener + cliente Kafka, mismo tópico y group propio. Materializer y resto del ecosistema sólo después.

### Matriz E2E

| ID | Caso | Entrada | Resultado CP esperado | Estado PM | Efecto físico | Hoy |
|---|---|---|---|---|---|---|
| K1 | kafka-topic PROVISION | API pipeline deploy | STARTED→COMPLETED | run COMPLETED | tópico prefijado con particiones/config | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| K2 | kafka-topic cambio de configuración (redeploy emite PROVISION; CP UPDATE se prueba standalone) | redeploy con cambio | STARTED→COMPLETED | COMPLETED | config cambiada | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| K3 | kafka-topic DEPROVISION | undeploy / inactivate | STARTED→COMPLETED | inactivo/terminado | tópico ausente | PASS F1 undeploy físico; inactivate regresión PASS, browser posterior |
| K4 | FAILED de negocio | params o ambiente inválidos | FAILED sin STARTED | FAILED con error | sin tópico | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| K5 | replay de trigger | reinyectar value capturado | sin resultado nuevo | sin cambio | sin cambio | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| K6 | gap de publicación | tópico de resultado ausente durante el proceso | publish absorbido | FAILED por timeout | tópico creado (inconsistencia conocida) | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| C1 | mergetree PROVISION | API | STARTED→IN_PROGRESS×4→COMPLETED | COMPLETED | db, tabla, usuarios ro/rw y grants | NO_EJECUTADO |
| C2 | mergetree UPDATE | API | COMPLETED | COMPLETED | ALTER aplicado | NO_EJECUTADO |
| C3 | mergetree DEPROVISION | API | COMPLETED | inactivo | tabla y usuarios ausentes | NO_EJECUTADO; depende de la rama del fix |
| C4 | mat-view PROVISION/DEPROVISION | API | COMPLETED | COMPLETED/inactivo | vista y usuario | NO_EJECUTADO |
| C5 | context ausente o inválido | API | FAILED sin STARTED | FAILED | nada | NO_EJECUTADO |
| C6 | mat-view UPDATE | API | FAILED (gap de negocio) | FAILED | sin cambio | NO_EJECUTADO |
| F1 | flink-sql PROVISION | API | FAILED real por proveedor ausente | FAILED | — | NO_EJECUTADO; físico BLOCKED |
| F2 | tipo ajeno | trigger kafka-topic | ninguno desde Flink | — | — | NO_EJECUTADO |
| F3 | flink-sql PROVISION físico | API | STARTED→COMPLETED | COMPLETED | job real RUNNING; DEPROVISION lo cancela | BLOCKED (seam por demostrar) |
| A1 | ClickHouse `list-warehouse`/`list-database` | API actions + polling `/v2/actions/{id}` | resultado de action real | action completada con datos del motor | consulta real a ClickHouse | NO_EJECUTADO |
| A2 | Kafka PEEK | `POST /services/{id}/actions/peek` | mensajes reales del tópico | resultado visible | lectura real del broker | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| X1 | aislamiento del tópico | un trigger por tipo | resultados de un único CP por `deployment_id` | — | — | NO_EJECUTADO |
| X2 | poison | no JSON / con `msg` | DLT-<cp>, sin resultado | sin cambio | — | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| X3 | restart CP | reinicio con offsets comprometidos | sin reproceso | sin cambio | — | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| X4 | resultado inválido | value inválido en resultado | DLT PM | sin cambio | — | PASS F1 recertificada; normal11 + gap1, repetidas root/independiente |
| B1 | browser Kafka | crear → deploy → polling → peek → inactivate | como K1/A2/K3 | visible en UI | como K1/K3 | NO_EJECUTADO |
| B2 | browser ClickHouse | elegir warehouse/base → crear mergetree → deploy → inactivate | como A1/C1/C3 | visible en UI | como C1/C3 | NO_EJECUTADO |
| B3 | browser Flink | crear flink-sql → deploy → inactivate | como F3 | visible en UI | job real | BLOCKED (seam Flink) |

### Decisiones acordadas

- **D1 — entrada CP:** A como adapter local pequeño, sólo con prueba de paridad HTTP↔Kafka por CP; B donde A no conserve limpiamente binding, `@Valid`, filtros y manejo de errores.
- **D2 — Flink:** BLOCKED documentado mientras se busca el seam mínimo para un job real; Flink físico permanece en el criterio final. Tamaño del cambio y RAM se demuestran, no se suponen.
- **D3 — actions:** dentro del alcance las que usan los journeys iniciales (`list-warehouse`, `list-database`, PEEK).
- **D4 — datos del front:** fixtures locales mínimos de templates y grants, coherentes con la config del front y sin desactivar validaciones; se resuelven como parte de la integración.
- **D5 — rama LOCAL-HTTP-2:** extracción selectiva del fix DEPROVISION y de adapters reutilizables en ramas aisladas con dependencia explícita; el fix conserva su propia rama y ya está incluido en el PR Playmaker1286; no requiere un tercer PR ni merge previo.
- **D6 — ClickHouse:** releer develop vigente, preservar cambios ajenos y fijar versión por pruebas físicas, prefiriendo la versión on-prem productiva cuando se obtenga.

F1 ya autorizada, con SPEC antes de código e iteración posterior recertificada. Pendiente para fases siguientes: fetch/relectura de deltas CH/Flink/front y seam físico Flink; conservar criterios completos de F2–F5.

### Bloqueos

- Entrega PR F1: CodeQL Playmaker startup_failure sin jobs; propuesta de runner rechazada por auto-review y pendiente de autorización explícita, con causa aún no demostrada. No reduce la aceptación de código local ni acredita el green remoto.

- Flink físico: seam por demostrar (KDA sin override de endpoint; Cloud Controller + Dataproc sin equivalente local).
- Undeploy: fix DEPROVISION fuera de develop; se consume desde su rama propia.
- Delta remoto de CH, Flink y front sin leer: requiere fetch autorizado.
- Cliente on-prem de ClickHouse frente a la versión fijada: por verificar contra la versión productiva.

## Fuentes

- Lectura por ref git (sin checkout/fetch/build) de los cinco repos y de los worktrees `rio-playmaker-kafka-e2e`, `rio-controlplane-kafka-e2e`, `rio-controlplane-kafka-memory-e2e` y `*-http-lifecycle`; `ls-remote` de `develop` el 09/10.
- Jars `rio-sdk-events` 1.3.1, 1.5.0 y 1.6.1 inspeccionados con `javap` (campo `context`).
- `local/KAFKA_HTTP.md` de la rama HTTP de PM (Tiger mock, fixture ACME, fix DEPROVISION) y [[Kafka — Ambiente local con servicios reales]] (evidencias LOCAL-HTTP-2 y PR85).
