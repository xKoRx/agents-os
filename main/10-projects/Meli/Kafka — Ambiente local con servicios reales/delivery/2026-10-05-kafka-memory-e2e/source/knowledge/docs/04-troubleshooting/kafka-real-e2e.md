---
title: Verificar el E2E real de Kafka CP
layer: L3
audience: [engineering, quality, support, agents]
last_verified: 2026-10-05
confidence: medium
sensitivity: internal
---

# Verificar el E2E real de Kafka CP

## Corte local de trabajo — 05/10

**WORK_BRANCH_PENDING; gate físico BLOCKED.** La última decisión del owner retira Fury Sandbox del E2E local del CP y prioriza un mapa en memoria; el ecosistema queda para después. El candidato `feature/kafka-e2e-memory@7615b210e5b70667912b956c2f27cc0d1ebc80eb` parte de `7f1720d950446638ff9b15a0e4e167f3e8e26e43`. Este corte no reemplaza el master canónico `f74e856e` ni declara disponibilidad en producción. La primera corrida física falló; no hay una familia de negocio completa PASS ni un replay limpio del launcher final.

El perfil `memory-e2e`, junto con `local,real-e2e`, usa un `ConcurrentHashMap` por instancia mediante la interfaz nativa `KvsClient`. Las versiones son asignadas localmente. El estado se pierde al reiniciar y dos JVMs mantienen mapas independientes: esta familia no acredita persistencia, exclusión entre procesos, recovery durable ni semántica del servidor Fury KVS. `RealKvsIntegrationTest` ejecuta el mapa en esta task; sus nombres legacy no prueban que se consultó un servidor.

La selección de `localKafkaE2eTest` está fijada en `build.gradle` y `e2e/LOCAL.md`: diez clases funcionales, con tres escenarios child de routing/config explícitamente excluidos. Usa cinco brokers propios para AWS RF1–5 y GCP RF1–3/default2, controllers/processors/provisioners del CP y resultados sobre Kafka. No deshabilita escenarios para dar verde; los contratos fuera de selección conservan su estado separado. Los tests directos de provisioner/interrupción mantienen su capa más acotada. GCP sobre brokers plaintext locales no acredita OAuth y Kafka local no acredita delivery BigQueue. Playmaker/MySQL/EntityService, identidad y proveedores administrados conservan su alcance posterior.

### Capacidades del mapa verificadas en la capa unitaria

| Capacidad local | Comportamiento preparado y probado | Evidencia fijada al candidato |
|---|---|---|
| Create/version/CAS | Create exclusivo asigna 1; update exige la versión exacta e incrementa 1; concurrencia y reserva del guard dentro de la instancia | `LocalInMemoryKvsClientTest`, `IdempotencyGuardTest` |
| TTL | -1 conserva, 0 expira inmediatamente, positivo expira en segundos del reloj local; update exitoso renueva el TTL | `LocalInMemoryKvsClientTest` |
| Aislamiento y bytes | Instancias independientes; reads/writes copian bytes; otra instancia o restart no recupera el estado | `LocalInMemoryKvsClientTest` |
| Close y APIs no soportadas | Close borra el mapa y rechaza operaciones posteriores; typed/batch/bulk fallan explícitamente | `LocalInMemoryKvsClientTest` |
| Selección de perfil | Memoria exige `local,real-e2e,memory-e2e`; builder remoto y fallback conservan sus perfiles | `KvsConfigTest` |

Son cinco capacidades locales de la matriz, no nuevos feature IDs ni garantías del servidor. Fuente al SHA candidato: `src/main/java/com/mercadolibre/rio_controlplane_kafka/reale2e/LocalInMemoryKvsClient.java`, `src/main/java/com/mercadolibre/rio_controlplane_kafka/config/KvsConfig.java` y sus tests bajo `src/test/java/com/mercadolibre/rio_controlplane_kafka/`; [diff fijado por commit](https://github.com/melisource/fury_rio-controlplane-kafka/compare/7f1720d950446638ff9b15a0e4e167f3e8e26e43...7615b210e5b70667912b956c2f27cc0d1ebc80eb).

### Ejecutar y conservar evidencia

```sh
DOCKER_CONTEXT=<contexto-Docker-propio> JAVA_HOME=<JDK25-verificado> ./e2e/local.sh
# Con las dependencias ya disponibles en cache:
DOCKER_CONTEXT=<contexto-Docker-propio> JAVA_HOME=<JDK25-verificado> ./e2e/local.sh --offline
```

`./e2e/local.sh` y `./e2e/run.sh` sin argumentos seleccionan `localKafkaE2eTest`; no necesitan login, alias KVS, BC, instancia ni configuración Fury Sandbox. Sí requieren Docker/Compose propio con al menos 5 GiB, JDK 25, cinco puertos loopback 39092–39096 disponibles y dependencias Maven internas por red o cache. Una invocación filtrada con `--tests` acredita sólo su selección.

Los reportes viven en `build/local-e2e/<RUN_ID>/`: hashes de fuente, readiness, JUnit sanitizado, prueba de finalización del worker nativo y `result.json`. `e2e/verify-local-result.py` exige test count positivo, cero fallos/errores/skips, tuple exacta de run/task/owner/worker y cleanup PASS; un HTTP200, un broker saludable o compilación no sustituyen ese resultado. Logs crudos de Gradle/brokers permanecen privados. Trabajo retenido UNKNOWN impide el `down`; no borrar journals ni resources para obtener PASS.

### Evidencia de ejecución y límites actuales

| Comprobación del 05/10 | Estado observado | Límite |
|---|---|---|
| Adapter/config/guard focal | PASS: 59 tests (17+14+28), cero fallos/errores/skips | Capa unitaria; no efecto Kafka ni servidor KVS |
| Regresión CP y compilación | PASS: 845 unitarios, cero fallos/errores/skips; `compileRealIntegrationTestJava` PASS | No certifica negocio Kafka |
| Reproducción independiente del SHA candidato desde clon limpio inicial | PASS: 845 unitarios/65 clases, cero fallos/errores/skips; Java25/offline `test` + `compileRealIntegrationTestJava` | Sin Docker/backend ni variables Fury/AWS/MELI/KVS; sólo unit/compilación, no E2E físico |
| Primera corrida física `48711a6c7ffa43dc88c44b2d4b1db4b1` | FAIL: 343 invocaciones: 309 fallaron, 34 pasaron, 0 skips | Cinco brokers healthy y metadata interna con cinco IDs; host 127.0.0.1:39092 rechazó conexión. Primer describeCluster agotó deadline y el journal FAILED bloqueó fixtures posteriores. Ninguna familia completa PASS |
| Assertions KVS de esa corrida | Tres comparaciones enum/string fallaron; corregidas a `ErrorCode.CONFLICT.getCode()` | Oracles de operaciones/CAS preservados; replay físico posterior pendiente |
| Cleanup/native proof/UNKNOWN retention | V1 retiró recursos propios tras el fallo; controles endurecidos después. Peer independiente V5 PASS: 49 controles, 0 findings | Certifica fuente/metadata/proceso, no una corrida Kafka limpia del código final |
| Matriz local 356 | 5 PASS unit/config; 226 BLOCKED por Kafka host; 125 NOT_EXECUTED fuera de selección | La matriz remota histórica 351 permanece intacta; no sumar PASS de capas distintas |
| Workflow corporativo | `.github/workflows/local-kafka-e2e.yml` implementado, NOT_EXECUTED | Requiere runner del owner con Docker/JDK 25/Maven interno; no exige auth Fury |

El recibo de la rama en el suplemento documental `4c66d0d5ca77e1de4aef5b08c9e601921eb60a9b` es `meli/features/20261001-real-e2e/evidence/local-memory-2026-10-05.md` (SHA256 `27d51ae2e4ecc8aa513344fad79f647bdc5c6e8f83a4f718b0d884944292cd61`); la selección/status por capacidad está en `local-coverage-matrix.tsv`. Conserva el fallo original anterior al endurecimiento del launcher y separa controles unitarios de los efectos físicos. No reemplazar efectos ni resultados Kafka por mocks o archivos. La reproducción independiente conserva `review.json` SHA256 `2c66dc4ea7a8cdc7040434ff6a4aa8d469681dc7b4a0f333b313c3671c11f033` y `unit-and-compile.log` SHA256 `11b5532664724e9202d30c138537c2d833b34e357743fd5caf275f9d3fa5c9f5`; 33 paths candidatos sin drift. Su verdict es unit/compilación únicamente.

### Fuentes y escalamiento del alcance local

Fuente del candidato `7615b210e5b70667912b956c2f27cc0d1ebc80eb`: `e2e/local.sh`, `e2e/run.sh`, `e2e/verify-local-result.py`, `build.gradle`, `src/main/resources/application-memory-e2e.yml`, cliente/config/tests del mapa, workflow local y SPECs bajo `meli/features/20261001-real-e2e/`; [diff de la rama de trabajo](https://github.com/melisource/fury_rio-controlplane-kafka/compare/7f1720d950446638ff9b15a0e4e167f3e8e26e43...7615b210e5b70667912b956c2f27cc0d1ebc80eb). La biblioteca no afirma que el commit esté publicado o integrado. El [suplemento documental](https://github.com/melisource/fury_rio-controlplane-kafka/compare/7615b210e5b70667912b956c2f27cc0d1ebc80eb...4c66d0d5ca77e1de4aef5b08c9e601921eb60a9b) actualiza sólo `e2e/LOCAL.md` y el recibo de evidencia: cleanup retiene recursos ante UNKNOWN y agrega la reproducción independiente unitaria. El core sigue fijado a `7615b21`. La fecha verifica esos deltas, no un nuevo master.

El runtime propio Colima 0.8.1/Lima 1.0.5 falló readiness tras 603 s de restart/foreground/gRPC. SSH nativo funciona; el child de forwarding recibió SIGKILL, sin causa establecida en los controles del intervalo. No atribuirlo a VPN, auth, permisos o AMFI. La VM propia quedó detenida, sin containers del run; el runtime compartido de 2 GiB no se modificó y Docker default está indisponible.

El siguiente gate es restaurar un runtime propio con al menos 5 GiB y listeners host funcionales, repetir toda la suite local y completar un replay limpio independiente, incluidos los fallos Kafka/publicación/proceso esperados. El launcher final verifica los cinco listeners host con deadline de 30 s. El 403 histórico Sandbox no bloquea este comando; las familias remotas permanecen separadas. Estado físico completo: BLOCKED.

## Referencia histórica — 01/10–02/10

Los apartados siguientes conservan sin reescribir el diseño y los ensayos de `feature/kafka-real-e2e` con Fury Sandbox. Sus comandos, gates KVS y prohibición de memoria corresponden a aquella familia remota, no al alcance local autorizado el 05/10.

## Impacto y alcance

**WORK_BRANCH_PENDING.** El sistema se implementa en `feature/kafka-real-e2e`, sobre CP develop `4302481c69300074a85ea5eb051a27bbd505cdce` y Playmaker develop `7673f4bffc286f0f24d4214938df53c4c5eb9c38`. Los masters canónicos siguen en el [manifiesto](../08-governance/source-manifest.md); este runbook no afirma disponibilidad en producción. La decisión, SPECs, tareas, inventario y matriz se guardan en el CP bajo `meli/features/20261001-real-e2e/`.

Los alcances se ejecutan por separado. La suite propia del CP (`realIntegrationTest`) usa únicamente Kafka real, el CP y su KVS Fury Sandbox exclusivo, con resultados observables sobre Kafka. El ecosistema agrega Playmaker/MySQL/EntityService e identidad; el proveedor/transporte administrado usa recursos no productivos propios. El owner priorizó primero la suite propia del CP el 2026-10-02. Ejecutar el provisioner GCP sobre Kafka plaintext local no acredita OAuth GCP. Los adapters Kafka de triggers/resultados no acreditan BigQueue. No hay certificación completa de ninguna de esas familias todavía.

La arquitectura reutiliza Gradle/JUnit/Awaitility del CP y el transporte Kafka `local-integration` de Playmaker. Cinco brokers cubren AWS RF1–5 y GCP RF1–3/default2. Las conexiones y el transporte varían por perfil; validadores, processors, provisioners, guard y consumidores de estado son los reales. Las suites no pueden acreditar éxito usando el fallback KVS, archivos de resultados o respuestas sintéticas del negocio.

El [master Playmaker `0c83575`](../08-governance/kafka-canonical-audit-2026-10-01.md#transporte-local-y-service-peek) ya contiene ese transporte local de deployments, idéntico a develop `7673f4b`. Los adapters locales de acciones, clientes Toolkit KVS dedicados y selección HTTP real de Service PEEK siguen sólo en checkpoint `1b4b8e1`. El master local conserva Service PEEK sintético; el harness completo continúa WORK_BRANCH_PENDING. La auth configured-only+Tiger del master difiere de las reglas más estrictas de develop/work; un recorrido sobre `1b4b8e1` no certifica esa auth canónica.

## Evidencia mínima segura

| Comprobación del 01/10 | Estado observado | Límite |
|---|---|---|
| Cinco brokers KRaft, topics de 3 particiones RF1–5 | PASS, réplicas/ISR y cinco IDs observados; cleanup certificado | Infraestructura únicamente, sin CP/KVS/Playmaker |
| Heap192MiB por broker | FAIL, OOM real al iniciar LogManager | Se corrigió a heap512MiB/límite768MiB; no esconder el primer ensayo |
| Compilación CP y regresión existente más regresiones acotadas | PASS unit T23: 804 tests/0 fallos/0 errores/0 skips Java25 (63 clases), compile de tres familias y bootJar; cortes anteriores 722/712 y primer full de 804 tests con 4 fixtures incompletos preservados | No equivale a suite real |
| MySQL8.0.32, 37 migraciones y fixture SQL del harness | PASS por reproducción independiente; cleanup certificado | No acredita Tiger/ACME, CP ni despliegue Playmaker |
| SDK publisher: segment/buffering explícitos | PASS unitario708/0 skips, regresión inicial3 fallos reproducida; factory corregida en rama SDK | CP sigue artifact1.3.1; no release ni delivery BigQueue acreditada |
| Broker propio con ACLs y RF insuficiente | PASS, denial real, topic ausente, restauración/create/ISR y cleanup certificado | Controles físicos únicamente; casos CP/KVS consumidores pendientes |
| KVS Toolkit exclusivo/create/versión/CAS/TTL | BLOCKED: recheck del 02/10 con VPN y auth Fury válidos creó BC200, clone propio403, delete200/ausencia404 | Alias visible aprobado/test; no instancia ni escrituras.403 no distingue elegibilidad Sandbox de autorización; contrato servidor NOT_EXECUTED |
| Recorrido Playmaker completo y acciones | NOT_EXECUTED, KVS403 bloquea; input de identidad/grant preparado | Compilar y aceptar HTTP no son estado final |
| OAuth GCP / BigQueue administrada / job corporativo completo | NOT_EXECUTED, recursos/credenciales/runner y cleanup por confirmar | Sin sustitución por pruebas locales |

El ledger por corrida debe contener SHA y manifiesto del candidato, namespace propio, correladores, particiones/RF/config/offsets verificados, terminal recibido, KVS real y estado MySQL cuando aplica. Conserva JUnit y limpieza tanto en éxito como en fallo. El payload sintético permitido es un fixture de entrada; un resultado observado nunca se reemplaza por un fixture.

El lifecycle remoto se intentó con dos BC nuevos propios. `POST bc` y ownership metadata fueron observados; `POST bc/<run>/services` devolvió403 al clonar el KVS de test del CP. Se retiró cada BC (`DELETE200`, lectura posterior404); no se asignó instancia ni se escribió KVS. El guard read-only del 2026-10-02T15:31:37Z devolvió `SANDBOX_FURY_LOGIN_REQUIRED`, sin API remota ni renovación implícita. Una comprobación posterior con VPN conectada encontró auth válida y repitió el lifecycle CP-only: BC propio create200, clone de `triggers-status-nonprod`403, delete200 y ausencia404 confirmada además por GET independiente. El catálogo KVS propio respondió200 y contiene una coincidencia exacta, `status=approved`, `container_type=database`, `test_container=true`; eso acredita visibilidad, no clonabilidad. La CLI instalada no ofrece un catálogo de elegibilidad Sandbox y403 no distingue esa causa de autorización. Acción inmediata: habilitar/confirmar la clonación Sandbox del alias propio para la identidad Fury actual o indicar otro alias CP propio autorizado. No se asignó instancia ni se escribió KVS. El ledger versionado candidato vive en `meli/features/20261001-real-e2e/evidence/verification-ledger.json`; conserva IDs mínimos, árboles independientes y hashes, sin endpoints ni credenciales.

La documentación oficial revisada el 02/10 sirve Sandbox1.3.12, KVS2.0.43 y Fury CLI5.24.0. [KVS documenta servicios reales mediante Sandbox](https://furydocs.io/kvs-docs/2.0.43/guide/#/kvs_sandbox?id=sandbox-key-value-store); [Notes exige Commiter o superior](https://furydocs.io/sandbox-services-docs/1.3.12/guide/#/notes) y [la guía excluye KVS Vault](https://furydocs.io/sandbox-services-docs/1.3.12/guide/#/). [Agregar al BC](https://furydocs.io/sandbox-services-docs/1.3.12/guide/#/commands/bc?id=add) requiere un servicio existente de la misma app y nombre case-sensitive, sin flag beta documentado. No apareció etiqueta beta en las páginas revisadas ni resultados al buscar beta en ambas guías; eso no acredita GA. El rol efectivo, la condición Vault y la elegibilidad Sandbox del alias concreto siguen sin verificar: `database` no descarta Vault. No atribuyas403 a rol, Vault o `test=true` sin la razón del backend. El recibo candidato `meli/features/20261001-real-e2e/evidence/sandbox-documentation-2026-10-02.json` identifica fuentes, límites y revisión de inferencias. No hubo mutaciones remotas ni ejecución de negocio durante esta búsqueda.

La matriz versionada del checkpoint CP `3bea4809a5372d5acca3d86a6181ed2c60137f22` contiene **351 filas** (319 CP +20 Playmaker +2 controles de cleanup/workers +10 fronteras Kafka/entities/context/auth), todas NOT_EXECUTED para la capacidad completa:304 FULL preparados,29 PARTIAL y18 NONE. FULL mide preparación, no ejecución. El corte `eee5b909` conservaba297/26/28; los anteriores siguen como evidencia histórica. T24 prepara22 métodos/36 invocaciones por política para las diez fronteras PM, con revisión de fuente independiente; siete joins completos preparados y tres fronteras parciales. Ninguno acredita negocio físico. Templates BigQueue200 y ACME grant preparado no acreditan delivery, token efectivo, EntityService desplegado ni negocio. [Fuentes y límites de esta preparación](../08-governance/kafka-canonical-audit-2026-10-01.md#preparación-t23t26-y-límites-de-la-evidencia).

El control del parent pasó reproducción independiente desde copia limpia:46 controles (5 cleanup,10 Sandbox,8 parser/gates,16 retención y7 filesystem), además de los cuatro negativos originales de enumeración; el fixture de permisos fue reproducido bajo umask077. Los fallos iniciales permanecen en el ledger. ConfigData/Binder real tuvo15 invocaciones PASS; el proxy físico tuvo13 aserciones independientes y cleanup tras STOP/interrupción. Todos son evidencia de controles o componentes, no aprobación del recorrido CP/KVS/Playmaker.

El delta CP-only del 02/10 agrega scope explícito `cp`/`ecosystem` y corrige el contexto del EXIT trap del wrapper CI en Bash3.2. `validateRealE2eHarness` ejecutó72 controles locales PASS (25 Sandbox,8 managed launcher,11 CI,5 cleanup,16 retención y7 filesystem); `compileRealIntegrationTestJava` PASS. Estos controles usan metadata/procesos privados antes del SDK y no certifican KVS, CP ni un job corporativo real. Los RED previos del trap y de una asignación incorrecta se conservan.

## Máquina de estados esperada

Usa el [contrato canónico](../05-contracts/status-models.md#idempotencia-cp) y la [ficha del CP](../03-services/rio-controlplane-kafka.md). Deployments con operación válida finalizan antes de publish best-effort; una pérdida del terminal puede dejar efecto Kafka sin convergencia Playmaker. GCP `operation=null` falla antes del claim. Actions reservan publicación dentro de `IN_PROGRESS`, publican y finalizan. No prometer exactly-once. Las correcciones candidatas (describe MSK fail-closed, números exactos y seam GCP peek) aún no son comportamiento master.

## Árbol de decisión

1. Verifica branch/base/SPEC y que el checkout original con cambios ajenos siga intacto. Usa los worktrees dedicados del proyecto.
2. Selecciona un Docker runtime propio con al menos5GiB; el ensayo usó6GiB/4CPU ARM. No reinicies el runtime compartido para ganar memoria.
3. Autentica Fury y configura un sandbox KVS propio con el cliente Toolkit vigente. El archivo privado modo0600 contiene sólo exports generados y metadatos de ownership. Un directorio de artifacts SCP propio impide heredar configuraciones de otra aplicación.
4. Para Playmaker prepara identidad Tiger, equipo/proyecto ACME y containers KVS propios de resultados/locks. La auth productiva permanece activa.
5. Ejecuta la familia y espera efectos/terminales con deadlines. Si el preflight falla, registra BLOCKED y capacidades NOT_EXECUTED; no uses skip ni un perfil más débil.
6. Ejecuta la familia administrada sólo después de verificar recursos propios, callback/observer real y API de cleanup. Nunca pausas un consumer compartido.

Comandos implementados en la rama candidata; el arranque completo sigue pendiente de esos gates externos:

```sh
export DOCKER_CONTEXT=<contexto-Docker-propio> JAVA_HOME=<JDK25-verificado>
export E2E_FURY_PYTHON=<Python-del-Fury-autenticado>
# CP solo: un alias/BC propio; no exige servicios Playmaker.
"$E2E_FURY_PYTHON" e2e/sandbox.py up --scope cp --cp-service <alias-KVS-propio-CP>
export E2E_KVS_ENV_FILE=<directorio-privado-impreso>/sandbox.env
./e2e/run.sh realIntegrationTest
# Ecosistema posterior: otro run con --scope ecosystem y sus tres aliases.
# No reutilizar instancias/run IDs ni usar receipt CP-only para esas familias.
# Cada familia PM exige repo/SHA40, caller0600, Entity bundle y denied identity propios.
./e2e/run.sh e2eCanonicalPlaymakerTest
./e2e/run.sh e2eCandidatePlaymakerTest
# Managed usa configuración propia con su run fijo y KVS separado.
./e2e/managed.sh all
./e2e/ci.sh
```

En Application completo configura/verifica `credentials.secret-segment` y el SecretClient `@Primary`; el probe import-onlySDK usa `fury-secrets.segment-id`. Mantén ambas rutas explícitas en el journey OAuth; no deduzcas el wrapper CP sólo desde bytecode de auto-config. El comando candidato `E2E_KVS_ENV_FILE=<archivo-generado> ./e2e/managed.sh journey` ejecuta `managedControlplaneJourneyTest`; `all` incluye journey y probes. Carga todos los exports Sandbox, exige el mismo run ID y un artifact-root fresco0700; el registry de SDK/lifecycle/observer sigue bloqueado antes de beans. Exige identidad de mensajes y ventana completa del consumer; pedir64 o leer peek10 no acredita redelivery.

El helper crea BCs nuevos separados de CP/Playmaker por UUID y usa sólo rutas del CLI vigente. El lifecycle tuvo **ejecución parcial contra el API remoto**: BC create/ownership y retiro por DELETE200→GET404; clone-service403. Start, asignación de instancia, configuraciones KVS y el cleanup de esas asignaciones permanecen NOT_EXECUTED. Antes de escenarios, el launcher y Gradle directo contrastan todos los exports consumidos, aliases, segmentos, run/BC/instancia con configuración API fresca; rechazan mappings Toolkit heredados adicionales. Sólo admite credenciales almacenadas válidas, sin iniciar SSO implícito. Una ausencia inicial tras `create` incierto es cleanup fallido y conserva receipt para reconciliación; no acredita ausencia definitiva.

El archivo de identidad contiene `E2E_PLAYMAKER_TIGER_TOKEN`, `E2E_OWNER_TEAM` y `E2E_OWNER_PROJECT`; no publiques sus valores. Los containers de results/locks y su segment van en la configuración privada del sandbox. El launcher crea MySQL propio, aplica las migraciones canónicas y activa `local,local-integration,real-e2e` en Playmaker. El wrapper de integración y la CI requieren el mismo alcance real; una task vacía no puede dar verde.

El commit candidato SDK `97146e9fde6cb2d947b7978ba2ba2491d11f06b5` en `feature/kafka-e2e-publisher-fix` parte de master `ad2c98b806cffb88b23513f87785932aa1707ea4`. Conserva el builder configurado al crear el Producer; el [hallazgo canónico](../03-services/rio-controlplane-kafka.md) describe las opciones descartadas sin inventar una respuesta del servicio. El CP mantiene1.3.1: el gate managed exige decisión de adopción/backport y verificación física además de callback/cleanup propios.

## Hipótesis y cómo falsarlas

| Feature/capacidad | Escenario candidato | Evidencia exigida |
|---|---|---|
| `kafka.topic-provision`, `kafka.topic-update`, `kafka.topic-deprovision` | `RealControlplaneIntegrationTest#allSupportedReplicationFactorsCompletePhysicalCrud` y escenarios reconcile/config/error | AdminClient independiente + evento UUID + guard KVS; ausencia final real |
| `kafka.deploy-msk`, `kafka.deploy-gcp`, routing y validación | Casos por provider/aliases/defaults, envelopes ignorados y parámetros inválidos | Sin efecto/claim/evento donde el contrato lo exige; terminal real cuando acepta |
| `kafka.actions-peek`, `kafka.topic-peek-http` | Mensajes reales/formats/EARLIEST/LATEST, límite y errores; grupo preexistente | Keys/valores/offsets exactos y offsets comprometidos sin cambios |
| `kafka.actions-publication-idempotency` y guard | `RealKvsIntegrationTest`, `RealPublicationFailureIntegrationTest`, `RealProcessRecoveryIntegrationTest` | Exclusividad/versiones/TTL/CAS reales, fallo del producer y JVMs reiniciadas; sin garantías extra |
| `edge.deploy.grouped.playmaker-kafka`, `edge.action.result.kafka-playmaker` | `PlaymakerKafkaE2ETest`: CRUD, redeploy PROVISION/reconcile, PEEK acción/error y Service PEEK | Solicitud autenticada→trigger→efecto→resultado→KVS/MySQL correlacionados |
| OAuth/BigQueue/perímetro | Familia administrada separada | Credenciales/binding reales no productivos, delivery observado, errores y cleanup propio |

Los nombres son implementaciones pendientes en la work branch. La matriz exhaustiva del CP decide qué escenario está preparado, PASS, FAIL, BLOCKED o NOT_EXECUTED; esta tabla no convierte una familia escrita en cobertura ejecutada.

La [herencia/entities y contexto Kafka canónicos](../08-governance/kafka-canonical-audit-2026-10-01.md#entities-y-contexto-en-la-frontera-kafka) ya tienen cuerpos T24 posteriores al checkpoint: `PlaymakerKafkaEntityE2ETest`, `PlaymakerKafkaEntityDeploymentE2ETest`, `PlaymakerPipelineContextE2ETest` y `PlaymakerKafkaAuthorizationVersionE2ETest`. Requieren SQL/HTTP/wire/Kafka/KVS y EntityService productivos, artefactos separados master 0c/candidate 767, grants reales y cleanup probado. Siguen NOT_EXECUTED; imported APPROVED/Odin y excepciones defensivas permanecen parciales. T21/schema<1 y T23/metadata wire son guards candidatos anteriores al executor/claim, no master ni Validator global. El checkpoint CP `3bea4809` conserva siete de esas fronteras FULL preparadas y tres PARTIAL, con revisión de fuente independiente; los cuerpos nuevos por sí solos no certifican esos joins físicos. [Mapeo y límites T23–T26](../08-governance/kafka-canonical-audit-2026-10-01.md#preparación-t23t26-y-límites-de-la-evidencia).

## Recuperación segura

La integración T24/T25/T26 y root posterior cerró revisión independiente de fuente/componentes en el checkpoint CP `3bea4809`; el recorrido físico sigue NOT_EXECUTED. T25 reportó controles filesystem/process y offsets Kafka reales por separado; T26 pasó 18 tests unitarios sin Sandbox. El protocolo exigido debe demostrar PM/CP quiescentes, todas las correlaciones/offsets y receipts de cada client/generación antes de borrar KVS/SQL/config. Hasta verificación conjunta y runtime, no asumir que un permiso emitido, proceso muerto, terminal KVS o archivo SEALED ya cumplen ese protocolo. UNKNOWN exige retención y fallo. [Límites de evidencia](../08-governance/kafka-canonical-audit-2026-10-01.md#t25t26-controles-acotados-y-diseño-pendiente).

Los traps detienen sólo los procesos propios. Retiran recursos de la corrida únicamente cuando los gates de trabajo y limpieza permiten hacerlo. El diseño del checkpoint histórico CP `f80ea19421518251515aae768d020f574ad255bb`, previo a la integración nueva, conserva un journal0600 de intención en `E2E_RECONCILIATION_DIR`0700, escrito antes de efectos/envíos, y inventario ausente, permisos incorrectos o symlink producen UNKNOWN y un marker pendiente impide destruir Kafka/MySQL/Sandbox o borrar configuración privada. El endpoint local pasivo `/internal/e2e/workers` exige run y PID propios; commits del bridge, ingress y procesos/threads propios se comprueban aparte. No usa un terminal KVS como prueba de quiescencia. No borres el journal ni ejecutes `sandbox.py down` antes de reconciliar ese inventario y los workers. Un fallo de cleanup hace fallar el run; cada intento de limpieza se ejecuta aunque otro falle. Sandbox remoto y runtime Docker propio tienen lifecycle explícito separado. `sandbox.py down` verificó ownership y ausencia de los dos BC creados para el intento fallido. Stop de instancias y cleanup de KVS asignado permanecen NOT_EXECUTED porque el clone-service403 impidió su creación. CI prepara BCs exclusivos por job y conserva directorio privado ante cleanup incierto/fallido, con receipt sanitizado en el reporte. La familia CI CP consume `RIO_E2E_FURY_PYTHON` y `RIO_E2E_CP_KVS_SERVICE`; las familias ecosystem agregan `RIO_E2E_PM_RESULTS_KVS_SERVICE` y `RIO_E2E_PM_LOCKS_KVS_SERVICE`. El dispatcher `ci.sh` vigente sigue agregando las cuatro familias, por lo que no certifica un job CP-only aislado; permisos y schemas reales siguen gates. La preparación para continuar conserva el candidato y la evidencia sanitizada.

## No hacer

- No habilitar mocks, KVS no-op, almacenamiento en memoria o resultados a archivos para dar verde a una suite real.
- No usar BigQueue mock/forward como prueba de delivery administrada ni pausar consumers compartidos.
- No interpretar un `200`, un topic creado, STARTED o código compilado como despliegue completado.
- No copiar configuración de KMS, credenciales ni mensajes reales a la biblioteca o los reportes.

## Escalamiento

Para ejecutar CP local, resolver el403 de la clonación Sandbox del KVS propio, reproducido con VPN y auth válidos. Habilitar/confirmar clonabilidad y autorización de ese alias/identidad o indicar otro alias CP propio autorizado. No volver a atribuir el bloqueo actual a VPN o login. Los gates de ecosistema, identidad/ACME, OAuth/BigQueue y renovación Spellbook quedan separados de esa ejecución local. El administrador debe identificar runner corporativo con Docker/acceso a Sandbox para ejecutar el job real. La revisión formal Zord requiere autorización explícita de sus destinos externos configurados y escritura del cursor: el auto-review la rechazó antes de ejecutar reviewers. Esa revisión/publicación pendiente no se presenta como una dependencia del launcher CP local; tampoco se declaró revisión completa ni éxito total.

## Fuentes

- [Auditoría canónica y distinción de ramas](../08-governance/kafka-canonical-audit-2026-10-01.md).
- [Catálogo Kafka y anchors por SHA](../09-feature-catalog/rio-controlplane-kafka.md).
- [Contratos de entrega](../05-contracts/messages-and-delivery.md) y [ledger de fronteras](../05-contracts/upstream-downstream-ledger.md).
- Candidato local: CP `meli/features/20261001-real-e2e/`, `e2e/README.md`, suites Gradle y reportes `build/real-e2e/`; no commit de implementación canónica declarado.


## Comandos y evidencia del corte posterior

El [suplemento posterior](../08-governance/kafka-canonical-audit-2026-10-01.md#corte-posterior-de-implementación-y-verificación-acotada--0210) separa los822tests CP y las nuevas preparaciones de los cortes históricos804/722/712. Preparación revisada304FULL/29PARTIAL/18NONE,351NOT_EXECUTED; PASS_PREPARATION_PEER_ONLY. El README candidato CP `e2e/README.md` fija los comandos actuales y inputs verificables. No sustituye el contrato canonical.

CI intenta cuatro familias, exige los dos SHAs40 de PM y configura var `RIO_E2E_ENTITY_SERVICE_BASE_URL` → env `E2E_ENTITY_SERVICE_BASE_URL`; secretos `RIO_E2E_CHECKOUT_TOKEN`, `RIO_E2E_PLAYMAKER_CALLER_CONFIG`, `RIO_E2E_MANAGED_CONFIG`, `RIO_E2E_MANAGED_KVS_CONFIG`, `RIO_E2E_ENTITY_SERVICE_TEMPLATE_BUNDLE`, `RIO_E2E_PLAYMAKER_DENIED_IDENTITY_TEMPLATE`. Sólo publica evidencia desde su whitelist fija; logs/identidades/endpoints quedan privados. Un preflight que termina2 y un gate overall1 son fail-closed observados, no un job real ni un PASS de negocio. La disponibilidad del runner/protected environment permanece sin verificar.

No ejecutar `sandbox.py down` automáticamente después de un fallo. Primero exigir stop/reap PM exacto más drain/quiescencia CP vivo, offsets completos, quiescencia SQL, registry/clients/ACK completos y task/process exits reales. UNKNOWN/missing/partial retiene journal/recursos y falla. Cleanup Entity exige draft ausente y entidad DEACTIVATED; conserva revisiones activadas/audit. Un400 de deployments no prueba ausencia, y flags/config/hash por sí solos no verifican un target desplegado.
