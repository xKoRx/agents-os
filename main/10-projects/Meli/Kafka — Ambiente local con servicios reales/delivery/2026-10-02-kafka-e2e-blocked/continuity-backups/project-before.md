---
type: project
schema_version: 1
owner: "me"
root: true
status: "active"
priority: "P2"
area: "[[Meli]]"
parent:
sprint:
start: "2026-09-30"
due:
progress: 25
repo: "https://github.com/melisource/fury_rio-controlplane-kafka"
jira:
prs:
aliases: ["Kafka local real", "Ambiente local Kafka", "Control plane Kafka — Desarrollo local"]
tags: ["kind/project", "area/meli", "app/rio-controlplane-kafka"]
created: "2026-09-30"
updated: "2026-10-01"
---

# Kafka — Ambiente local con servicios reales

> [!info]+ Kafka — Ambiente local con servicios reales
> **Área:** [[Meli]] · **Estado:** active · **Owner:** Rodrigo · **Fase:** ejecución E2E; implementación multiagente y gates externos pendientes.

## 🎯 Objetivo

Levantar [[rio-controlplane-kafka]] y [[rio-playmaker]] en un ambiente de desarrollo que ejecute PROVISION, UPDATE, DEPROVISION y PEEK contra Kafka real, use KVS real de Fury Sandbox y muestre el resultado real en Playmaker. Automatizar la comprobación de esas capacidades para desarrollo y CI. Mantener los contratos y la lógica de negocio utilizados por las aplicaciones, con una matriz verificable de cobertura y de dependencias externas.

El resultado esperado es un comando de inicio documentado, configuración reproducible, servicios saludables y escenarios que demuestren el efecto físico sobre topics, mensajes y estado de orquestación. La comparación de implementaciones ya terminó y vive en [[Ambientes locales RIO — Comparativa de implementaciones]]; este proyecto conduce el cambio que se desprende de esa evidencia.

## 📊 Estado actual

- **Gate de implementación:** SPEC funcional → SPEC técnica → tareas guardadas en `rio-controlplane-kafka/meli/features/20261001-real-e2e/`; autorización autónoma del owner aplicada, publicación SIG todavía bloqueada por sesión expirada. Matriz versionada de 351 filas, todas NOT_EXECUTED; 299 FULL preparadas, 24 PARTIAL y 28 NONE (7 defensivas sin estímulo físico conocido, 11 SDK/managed y 10 joins Kafka/Playmaker con preparación pendiente). FULL significa código preparado, sin certificación de ejecución. Decisión: suites dentro del CP, extensión del local-integration real de Playmaker, cinco brokers por RF AWS1–5/GCP1–3.
- **Evidencia ejecutada:** Kafka5/RF1–5/ISR y MySQL37 migraciones comprobados físicamente, con cleanup independiente. El contexto propio ahora tiene cero contenedores/redes/volúmenes Compose. CP fuente f80: full722 tests/0fallos/0errores/0skips Java25; las tres familias compilan y bootJar existe. Schema0/−1 reprodujo4 fallos normativos antes y25 tests verdes después, repetidos desde430 limpio por agente distinto. PM4386 PASS/2 skips históricos y SDK708 PASS/0 skips independientes. No se acredita CP/KVS/Playmaker E2E físico. KL actual691 IDs/194Markdown estructural/histórico PASS; formal937 byte-idéntico baseline, sin weakening del validator. Las pruebas fuente/unitarias no certifican esas capacidades completas.
- **Lifecycle/controles:** Sandbox por corrida implementado con comparación exacta de exports/API, credenciales almacenadas sin SSO, outcomes antes de mutación y cleanup incierto rojo. Regresiones independientes localizaron y resolvieron P1/P2; gate Gradle9 en verificación. Proxy Kafka de frames con listener advertised y ADMIN independiente reproduce APIs19/20/32/75/37/44/0/2 contra broker3.9.1; primer cleanupFAIL preservado, segundo run PASS con cleanup certificado. Escenarios CP consumidores preparados, todavía sin KVS real. Full Application managed en SPEC T14, publicación/callback/cleanup/SDK-adopción siguen gates.
- **Código candidato:** CP real-e2e con publishers Kafka, bridge Kafka→HTTP, guard Toolkit real y seam GCP conectiva; launchers de cinco brokers y MySQL/Playmaker propio; suites físicas de CRUD/PEEK/KVS/publicación/restart en preparación. Se implementa fail-closed MSK y seam GCP actions; estado WORK_BRANCH_PENDING, no producción. Infra incorpora adapters PM de acciones/KVS/peek preservando Tiger/ACME.
- **Continuidad:** proyecto y SPECs son control único; evidencia compacta temporal en `/private/tmp/kafka-e2e-discovery/` y física en `rio-controlplane-kafka-e2e/build/real-e2e/`. Próximo paso: obtener permiso clone-service KVS propio (Fury ya autenticado), generar exports y ejecutar/reproducir las dos familias locales; después completar adapters administrados y diez joins nuevos con contratos/servicios propios. La revisión formal y el job corporativo permanecen gates separados. Tokens/coste desconocidos. Ledger mínimo versionado en CP `meli/features/20261001-real-e2e/evidence/verification-ledger.json`, con fallos iniciales y árboles independientes.

- **Ejecución activa 2026-10-01:** coordinador más roles acotados de dominio, infraestructura y knowledge. Checkouts originales preservados. Refs remotos actualizados mediante `fetch origin`; bases limpias actualizadas con `pull --ff-only`. Control durable de ejecución en esta nota; inventario y matriz341 en `rio-controlplane-kafka/meli/features/20261001-real-e2e/`, con mapping executable y NOT_EXECUTED explícito.
- **Fuentes vigentes y bases preservadas:** Kafka master `f74e856ef3de881e2d504c6cb1ced573681c1058`, develop `4302481c69300074a85ea5eb051a27bbd505cdce`; Playmaker master focal `0c83575c54cb198d238be7d83f3b4d8de27abbc8` (corte inicial histórico `3cd0daf6e17841ab79381f1eb5e2bd014ad68bd1`), develop `7673f4bffc286f0f24d4214938df53c4c5eb9c38`; SDK Events master `ad2c98b806cffb88b23513f87785932aa1707ea4`; knowledge master `de7cde85f7dd83a673c918e22ae9f08a0f7e05bd`. El ensayo anterior se conserva como evidencia histórica parcial, no certificación.
- **Fronteras y bloqueos comprobados:** Spellbook `Session expired`; Fury almacenado ahora PASS sin SSO; inventarios y templates BigQueue HTTP200. Dos BC propios creados/observados y retirados; clone-service KVS CP devolvió403, permiso puntual pedido al owner. ACME grant exacto verificado200; caller privado0600 preparado desde Tiger válido, sin bypass. KVS create/CAS/TTL sigue bloqueado y no hubo escrituras. GCP OAuth/BigQueue propios/cleanup y runner corporativo todavía no verificados. GitHub runners API respondió404 (no demuestra ausencia). Zord preparado sobre diffs congelados; auto-review rechazó envío a reviewers externos/configurados y cursor persistente hasta autorización explícita, solicitada. Trabajo independiente continúa.
- **Asignación de escritores:** root: SPEC/build/suite Playmaker/launcher PM/fix SDK; domain: matrix/inventario/suite física y fixes de provisioning; infra: Compose/launcher CP/adapters CP+PM/CI; knowledge: documentación KL entregada, ahora correcciones por root en fase posterior. Fault Controls: proxy transparente y brokers/ACLs propios con soporte Java, domain escribe escenarios consumidores. Infra congeló26 archivosCP/21PM; reviewer reproduce SDK/deltas y coexistencia Kafka+MySQL. Reviewer independiente sólo inspecciona/reproduce; no certifica su propio código. El brief por archivos y evidencia vive en las SPECs y artefactos compactos.

- **Investigación terminada el 2026-09-30:** se contrastaron los siete control planes, Playmaker, Materializer y SDK Events con commits identificados. Fuentes y límites en [[Repositorios RIO — Ambientes locales (2026-09-30)]].
- **Base encontrada:** Playmaker ya tiene MySQL real y transporte Kafka real en `local,local-integration`. Su propia arquitectura declara pendiente un control plane real conectado. Kafka ya tiene Compose con un broker, pero su publicación local usa archivos y su KVS sin configuración funciona en modo degradado.
- **Recomendación histórica (30/09, superada por decisión RF1–5):** extender esa base con tres brokers Apache Kafka en KRaft, el control plane real y KVS real de Fury en sandbox. Usar adaptadores locales de transporte y conexión que deleguen a los procesadores productivos. La configuración del SDK Toolkit con el sandbox debe demostrarse antes de dar por cubierta la idempotencia.
- **Alcance confirmado por el owner:** el CP debe funcionar completo localmente, incluido KVS, con pruebas automáticas. KVS real de Fury Sandbox está aceptado; el ambiente puede depender de conectividad corporativa. El backend KVS queda definido, y su configuración con el cliente Toolkit actual sigue por comprobar.
- **Estado histórico previo al encargo:** propuesta documental, implementación 0%. Estado vigente: ramas/SPEC/tareas/código candidato presentes; verificación real E2E todavía pendiente, sin declarar entrega completa.
- **Actualización de repos:** diez bases locales actualizadas con `git pull`: siete control planes, Playmaker, Materializer y SDK Events. Kafka y Playmaker se actualizaron desde worktrees limpios de sus ramas `develop` existentes, preservando ramas y cambios de los checkouts originales. ClickHouse volvió a su rama original después de actualizar su base. Las fuentes remotas examinadas coincidieron con los SHAs finales de esas bases.
- **Validación realizada:** investigación estática el 2026-09-30; prueba runtime parcial el 2026-10-01. La copia limpia falla en este Mac ARM por SIGILL del broker y falta de routing del CP. Con `JAVA_TOOL_OPTIONS=-XX:UseSVE=0` en el broker y routing AWS a localhost, ambos arrancan: `/ping` responde y PEEK devuelve cinco mensajes reales. Los resultados siguen a archivos y KVS sigue no-op. No se probaron deployments ni integración con Playmaker. Evidencia: [[Kafka local — Historia y prueba de arranque (2026-10-01)]].

- **Checkpoint SDK/controles:** nuevo worktree `rio-sdk-events-kafka-e2e`, rama `feature/kafka-e2e-publisher-fix`, base master `ad2c98b806cffb88b23513f87785932aa1707ea4`, sólo cinco archivos de publisher/tests; no release ni sustitución del artifact CP. Authbroker aislado confirmó TopicAuthorizationException y RF insuficiente real, luego restauró ACLs/create/ISR y cleanup certificado; no certifica CP/KVS. Evidencia `build/real-e2e/30a63cdea70b492ca357f1643f799194/fault-controls/ledger.json`. Suite Playmaker se amplía con redeploy PROVISION/reconcile, errores Actions, Service PEEK y DLT local neutral; ejecución aún pendiente.

- **Checkpoint de revisión adicional:** Protocol proxy Kafka reprodujo13 assertions físicas desde snapshot limpio; SIGSTOP/interrupt del cierre expuso dos defectos reales de cleanup (down omitido y descendiente vivo), FAIL original conservado y retiro propio certificado por revisor. Autor corrige; revisor distinto repetirá. Managed Application/CRUD RF1–3/PEEK/error/redelivery compila, pero registry sigue cerrado por SDK/lifecycle/observer no verificados; peer detectó que KVS terminal no prueba quiescencia ni exhaustividad de resultados. Launcher managed carga Sandbox completo, iguala run IDs y aísla SCP;8 controles L0 PASS. FuenteSet duplicaba recursos al invocar task real: setSrcDirs corrige y gate missingconfig produce nonzero exacto; baselineFAIL preservado. Root añade observación pasiva local del executor real antes de cleanup; unit/gates pendientes.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-controlplane-kafka]] · `melisource/fury_rio-controlplane-kafka` | `feature/kafka-real-e2e` · worktree hermano `rio-controlplane-kafka-e2e` | `develop@4302481c69300074a85ea5eb051a27bbd505cdce` | `meli/features/20261001-real-e2e/1-functional/spec.md` lista; publicación SIG bloqueada por sesión | `meli/features/20261001-real-e2e/2-technical/spec.md` lista | Implementación/suites compiladas; real E2E pendiente |
| [[rio-playmaker]] · `melisource/fury_rio-playmaker` | `feature/kafka-real-e2e` · worktree hermano `rio-playmaker-kafka-e2e` | `develop@7673f4bffc286f0f24d4214938df53c4c5eb9c38` | Funcional E2E del CP compartido, lista | Técnica E2E del CP compartida, lista | Adapters acciones/peek/KVS y launcher propios implementados; gates de ejecución pendientes |
| [[ads-signals-knowledge-library]] · `melisource/fury_ads-signals-knowledge-library` | `docs/kafka-real-e2e` · worktree hermano `ads-signals-knowledge-library-kafka-e2e` | `master@de7cde85f7dd83a673c918e22ae9f08a0f7e05bd` | Contrato de auditoría del prompt maestro | Correcciones canónicas y documentación pendiente de E2E | Auditoría y correcciones verificadas en curso |
| [[rio-sdk-events]] · `melisource/fury_rio-sdk-events` | `feature/kafka-e2e-publisher-fix` · worktree `rio-sdk-events-kafka-e2e` | `master@ad2c98b806cffb88b23513f87785932aa1707ea4` | Delta funcional compartido del CP | Delta técnico SDK en SPEC del CP | Corrección segment/buffering, regressions red→green708 reproducidos independientemente; release/backport y delivery real pendientes |

El flujo de entrega sigue Spellbook: SPEC funcional → SPEC técnica → tasks → implementación. Completar ramas y ambas SPEC antes de modificar código. Incluir otro repositorio en esta tabla sólo si el diseño demuestra que necesita un cambio.

## 🧩 Alcance propuesto

1. **Infraestructura compartida:** reutilizar el Compose de Playmaker y agregar un perfil o archivo para tres brokers, volúmenes, healthchecks y listeners internos/externos. Un comando levanta infraestructura y arranca las dos aplicaciones con versiones y puertos explícitos.
2. **Control plane real:** consumir los triggers locales con los DTO y validadores vigentes; delegar a los procesadores existentes; crear, actualizar y borrar topics mediante `AdminClient` real; publicar resultados a Kafka local con confirmación del broker.
3. **Conexión de datos:** habilitar una configuración local explícita hacia los brokers del Compose. El flujo GCP necesita desacoplar la obtención de `AdminClient` de la autenticación OAuth para ejecutar su provisioner real contra el cluster local. AWS ya tiene una fábrica plaintext. El perfil de integración debe evitar exigir una SA GCP sólo para administrar Kafka local.
4. **Acciones y PEEK:** extender el transporte local de Playmaker para acciones y conectar su cliente HTTP de PEEK al control plane. En `local` hoy siguen seleccionándose un productor de acciones no-op y un cliente PEEK que devuelve un mensaje sintético.
5. **Idempotencia real:** configurar un contenedor aislado de KVS Fury Sandbox con el SDK actual y probar create/CAS, versión, TTL, redelivery y reinicios. Validar primero la versión asignada por el servidor después de create, el conflicto de versiones y el incremento tras un update válido: el guard depende de esos comportamientos. No copiar identificadores de sandbox de KMS.
6. **Verificación automática:** escenarios de ciclo de vida, datos, replicación, routing y errores con evidencia en Kafka, KVS y MySQL, ejecutables mediante Gradle y en CI. Reservar una validación de integración con servicios reales no productivos para OAuth de GCP, transporte BigQueue y otras dependencias que Compose no reproduce.
7. **Disponibilidad verificable:** el launcher del perfil de integración debe comprobar Kafka y KVS real, rechazar wiring no-op/archivos y explicar qué configuración falta. Una dependencia corporativa ausente debe producir un fallo visible en las suites que la requieren. Las pruebas de caída posterior de un KVS real verificarán la política de degradación vigente del producto.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] Confirmar KVS real de Fury Sandbox y permitir la dependencia de conectividad corporativa #owner/me #type/research #area/meli
> - [x] Preparar [[Prompt maestro — E2E completo de CP Kafka]] con cobertura exhaustiva, subagentes, pruebas reales y actualización de la knowledge library #owner/me #type/research #area/meli
> - [/] Ejecutar el prompt maestro con un agente y completar el sistema E2E, la auditoría documental y la evidencia de cada capacidad #owner/me #type/dev #area/meli
> - [ ] Comprobar el cliente Toolkit contra un sandbox propio y verificar create/CAS, versiones y TTL #owner/me #type/dev #area/meli
> - [ ] Identificar un runner de CI con Docker y acceso al KVS sandbox; documentar configuración y aislamiento por corrida #owner/me #type/dev #area/meli
> - [ ] Crear la SPEC funcional en Spellbook con la matriz de capacidades y los criterios de aceptación de esta nota #owner/me #type/dev #area/meli
> - [ ] Crear la SPEC técnica y verificar compatibilidad serializada entre `rio-sdk-events:1.5.0` de Playmaker y `1.3.1` de Kafka #owner/me #type/dev #area/meli
> - [ ] Definir las ramas y completar la tabla de entrega antes de implementar #owner/me #type/dev #area/meli
> - [ ] Implementar arranque compartido y configuración del control plane con Kafka real #owner/me #type/dev #area/meli
> - [ ] Conectar deployments completos y comprobar estado físico y resultado en Playmaker #owner/me #type/dev #area/meli
> - [ ] Conectar acciones/PEEK e idempotencia con KVS real #owner/me #type/dev #area/meli
> - [ ] Implementar suites Gradle de integración y E2E con servicios reales, reportes y cleanup #owner/me #type/dev #area/meli
> - [ ] Integrar la ejecución automática en PRs y verificar que una dependencia ausente produce fallo visible #owner/me #type/dev #area/meli
> - [ ] Ejecutar la matriz de aceptación, documentar brechas y entregar el comando reproducible #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-10-01 — gates y reproducción:** runtime propio creado sin activar ni reiniciar Colima compartido; Kafka RF1–5 físico PASS/cleanup. OOM detectado y corregido. CP701 tests PASS. Revisión independiente arregló precisión P/U/D GCP y fallo GCP null operation sin claim; harness corregido para claves, routing, cleanup y evidencia. Configuración sandbox/auth/runner aún bloquea suites completas.

- **2026-10-01 — implementación:** SPECs y tareas listas; writers aislados. Dominio incorporó inventario/matriz y candidato de fix MSK fail-closed con regresiones pendientes. Infra implementa adapters sólo conexión/transporte y launcher propio. Verificador independiente activado para docs congelados y luego código/checkout limpio. Playmaker develop avanzó a7673f4bff durante pull; congelado ese nuevo baseline y master canónico separado.

- **2026-10-01 — ejecución:** bootstrap y reglas scoped leídos; tres subagentes en discovery. Kafka develop avanzó respecto al ensayo. Ramas limpias creadas; cambios ajenos no copiados ni staged. Claims/publicación de deployments, errores MSK, seam GCP PEEK y validación de envelopes se investigan como riesgos críticos antes de fijar los escenarios. Spellbook requiere login del owner; trabajo independiente continúa.

- **2026-09-30** — Búsqueda y contraste de implementaciones vigentes completados; diez bases actualizadas; los checkouts originales de Kafka y Playmaker se preservaron usando worktrees limpios. Se creó esta iniciativa con la recomendación de extender `local-integration`, tres brokers y KVS sandbox real. Implementación pendiente de las SPEC y ramas.
- **2026-10-01** — Historia verificada: Compose creado el 25 de febrero y mergeado a develop el 2 de marzo de 2026. Arranque y PEEK reales comprobados con dos ajustes temporales de configuración. El warmup GCP sin credenciales avisa y permite arrancar; operaciones GCP pendientes. La prueba se hizo sin modificar los repos y sus procesos se retiraron. El ambiente completo sin mocks continúa pendiente.
- **2026-10-01** — El owner confirmó el requisito de CP completo localmente, incluido KVS y automatización, y eligió KVS real de Fury Sandbox. Se concretó una propuesta de suites JUnit/Testcontainers/Awaitility, cobertura y fases de entrega; configuración del SDK y disponibilidad del runner quedan como primeras comprobaciones técnicas.
- **2026-10-01** — Se entregó [[Prompt maestro — E2E completo de CP Kafka]] para ejecución futura multiagente y actualización obligatoria de [[ads-signals-knowledge-library]]. Cierre de AGENTS OS solicitado; feedback y ejecución de depuración registrados. Próximo paso: ejecutar el encargo desde baselines limpios y actuales. Implementación E2E sigue pendiente.

## 🧭 Decisiones vigentes

- **D1 — Arquitectura implementada:** suites Gradle separadas dentro del CP y extensión del transporte `local-integration` de Playmaker. Los contratos, escenarios y matriz se versionan con el CP; Playmaker conserva su orquestación y persistencia. Un repositorio E2E separado duplicaría coordinación de versiones sin un harness completo que reutilizar.
- **D2 — Kafka físico:** cinco brokers Apache Kafka KRaft por Compose propio cubren AWS RF1–5 y GCP RF1–3/default2. Imagen, listeners, heap y workaround ARM quedan fijados. La recomendación histórica de tres brokers no cubría RF4/5.
- **D3 — Persistencia:** KVS real de Fury Sandbox propio con el Toolkit productivo. La identidad Fury almacenada funciona; el permiso de clone-service devolvió HTTP403. BC create/delete sí se verificó. Create exclusivo, versión del servidor, CAS y TTL siguen pendientes; no se usa el container compartido ni un sustituto no-op.
- **D4 — Familias distintas:** la suite funcional local emplea Kafka real y no acredita OAuth GCP ni BigQueue administrada. Esas fronteras requieren recursos no productivos propios, observación de mensajes y cleanup verificado.
- **D5 — Automatización:** JUnit/Awaitility y Gradle existentes, Compose para el cluster de cinco nodos y los controles de procesos/red por corrida. Se mantienen las dependencias existentes de Testcontainers, sin incorporar otra librería. Launchers, suites y CI existen en las ramas candidatas; una dependencia obligatoria ausente deja el gate rojo.

## 🧪 Criterios de aceptación propuestos

| Capacidad | Evidencia requerida |
|---|---|
| Arranque | Un comando reproducible inicia las aplicaciones e infraestructura, espera disponibilidad y expone healthchecks útiles; reinicio conserva datos según la política elegida. |
| PROVISION | El topic aparece en Kafka con particiones, replicación y configuración solicitadas; Playmaker recibe el resultado correspondiente al mismo deployment. |
| UPDATE | Cambian particiones/configuración y replicación permitida; los campos omitidos se conservan; errores inválidos se reflejan como fallas reales. |
| DEPROVISION | El topic desaparece; repetir la operación conserva la semántica del handler vigente. |
| PEEK | Lee mensajes producidos realmente, por REST y por acción cuando corresponda; no altera offsets de un consumer group existente. |
| Redelivery y concurrencia | KVS real demuestra claim/CAS y deduplicación, incluido redelivery tras reinicio; no hay éxito sintético. |
| Routing y contratos | Se ejercitan los templates AWS/GCP y reglas vigentes de selección de cluster, usando fixtures locales explícitas; los DTO serializados de ambos repos son compatibles. |
| Fallas | Se ejercitan broker caído, publicación fallida, timeout, payload inválido y DLT; las brechas heredadas de ACK/asíncrono se documentan con resultado observable. |
| Automatización | Suites ejecutables localmente y en un runner de CI habilitado; cada corrida usa IDs/recursos aislados, espera condiciones observables, genera reportes y limpia sus recursos. La ausencia de Kafka o KVS requerido produce fallo explícito. |
| Autenticación/transporte administrados | OAuth GCP y BigQueue se validan contra servicios reales no productivos; la prueba local por sí sola no los certifica. |

### Automatización candidata (WORK_BRANCH_PENDING)

| Suite | Servicios y cobertura | Momento de ejecución |
|---|---|---|
| Unitarias existentes | Reglas y casos aislados en JUnit; conservar la ejecución rápida actual | Desarrollo y cada PR |
| `realIntegrationTest` — implementada, runtime BLOCKED | Cinco brokers Kafka reales por Compose propio y KVS Fury Sandbox; CP real, PROVISION/UPDATE/DEPROVISION, PEEK REST/acción, AWS RF1–5/GCP RF1–3, create/CAS/TTL, redelivery, concurrencia, errores y resultados publicados al broker | Comando local y cada PR en runner con Docker y acceso al sandbox |
| `e2eTest` — implementada, runtime BLOCKED | Playmaker + MySQL + CP + cluster Kafka real + KVS sandbox; request de deployment, efecto físico, evento de resultado y estado final de Playmaker; reinicios y fallas de integración | Comando local y cambios que afecten esos contratos; gate automático antes de entrega |

Cada escenario debe comprobar el efecto físico y el resultado correlacionado por IDs de la corrida. Un HTTP 200 de recepción asíncrona no basta para aprobar un deployment. Las suites reales deben ejecutar los handlers/provisioners de la aplicación, sin reemplazarlos por Mockito ni usar resultados sintéticos. Awaitility espera estados reales con timeout; se conservan logs y reportes JUnit/Gradle al fallar.

El sandbox se aísla por contenedor dedicado al ambiente y claves/IDs por corrida, según lo que soporte Fury. La limpieza se limita a los recursos creados por esa corrida. Ningún test debe borrar contenedores globales o datos de otro desarrollador. En CI, validar acceso a Docker y al sandbox antes de ejecutar; no marcar la suite como aprobada por un skip de infraestructura.

**Comandos candidatos implementados:** `e2e/sandbox.py up/verify/down` administra el Sandbox remoto propio; `e2e/run.sh realIntegrationTest|e2eTest` inicia, prueba y limpia runtime local; `e2e/managed.sh all|journey|gcp|bigqueue` ejecuta gates administrados; `e2e/ci.sh` agrega todos sin skips. KVS clone403 y contratos administrados pendientes impiden ejecutar las familias completas. No crear targets make vacíos.

### BigQueue para desarrollo local

La documentación oficial de Sandbox Services lista BigQueue mediante comandos mock de Fury CLI. `fury services bigq mock send-msg` entrega un mensaje con formato BigQueue a un endpoint local; no demuestra una cola sandbox real con topics, consumers y redelivery. No cumple por sí solo el requisito de transporte real.

También está documentado `fury services bigq mock send-msg-consumer`, que reenvía mensajes desde un consumer BigQueue real de test hacia un endpoint local. Su paso `init` pausa el consumer de test. No se usa como evidencia del E2E real ni se pausa un consumer compartido; no se ejecutó ni se modificó ningún consumer durante esta consulta. La documentación revisada no demuestra un BigQueue sandbox provisionable equivalente a KVS.

Fuentes oficiales verificadas el 2026-10-01: [Sandbox Services, servicios soportados](https://github.com/melisource/fury_sandbox-services-docs/blob/961c80339f0b12cd0a88610f5af9edf79d58385f/docs/guide/sandbox_service.md) y [BigQueue CLI, Mock Message](https://github.com/melisource/fury_cli-services-docs/blob/2ae4d44d8750497cb36e1fa6f85aff62b03fa583/docs/guide/services/bigq.md#bigqueue-mock-message). Se contrastó el comando `send-msg` con la ayuda del CLI instalado.

### Orden de entrega propuesto

1. **Dependencias comprobadas:** configurar KVS sandbox con el Toolkit actual, demostrar su contrato y confirmar el runner de CI. La falta de acceso/configuración deja la suite real como no ejecutada y el pipeline falla con diagnóstico.
2. **CP local completo:** resolver arranque/routing/compatibilidad ARM, conexión real de ambos flujos Kafka, resultados al broker, acciones e idempotencia. Entregar el launcher y `realIntegrationTest` juntos.
3. **Playmaker y CI:** conectar el flujo completo con MySQL, crear `e2eTest`, comprobar contratos entre SDK 1.3.1/1.5.0 y automatizar los gates.
4. **Fallas y reinicios:** completar la matriz de recuperación, redelivery, concurrencia y persistencia, y documentar la validación adicional de OAuth/BigQueue en servicios no productivos.

## 🔗 Docs / Links

- [[Ambientes locales RIO — Comparativa de implementaciones]] — evidencia comparada, herramientas comunes, alternativas y recomendación.
- [[Repositorios RIO — Ambientes locales (2026-09-30)]] — commits y archivos fuente verificables.
- [[Kafka local — Historia y prueba de arranque (2026-10-01)]] — fecha de incorporación, fallas originales y prueba real de arranque/PEEK con configuración temporal.
- [[Prompt maestro — E2E completo de CP Kafka]] — encargo completo para el agente ejecutor.
- [Testcontainers — Kafka](https://java.testcontainers.org/modules/kafka/) — soporte oficial de contenedores Apache Kafka y listeners adicionales.
- [Gradle — Testing](https://docs.gradle.org/current/userguide/java_testing.html) — suites separadas y reportes de ejecución.
- [[RIO]] · [[rio-controlplane-kafka]] · [[rio-playmaker]] · [[rio-controlplane-kms]] · [[rio-sdk-events]].

## 💡 Ideas

- Si la operación diaria requiere trabajar sin VPN, evaluar después un backend local real para persistencia y locks, con su propio contrato de CAS/TTL. Esa alternativa requiere diseño adicional y no certifica las semánticas de Fury KVS.

- **Checkpoint T20 (2026-10-01):** CP candidato Java25 full unit712 PASS/0skip; observer5+4 independent PASS. ConfigData15 real YAML/Binder independent PASS únicamente parcial. Proxy v2 independiente13assert +STOP/interruption cleanup físico PASS; FAIL previo preservado. Parentretention4actualfunctions+4mutantes independent PASS y5+10+8controls. Journal durable/predispatch y teardown de namespaces auxiliares en revisión, no runtime CP/KVS certificado. SDK checkpoint97146e9fde6cb2d947b7978ba2ba2491d11f06b5; PM1b4b8e1554c37357e4b39e1860be6ad43f9aa640 (full4386/2baseline skips; stagedcontractfocused8PASS, ecosystemL1redsin Sandbox generado). KVS own clone403 sigue gate principal.

## Checkpoint T21/T22 — continuidad activa, sin cierre

- **CP fuente:** `f80ea19421518251515aae768d020f574ad255bb`, rama `feature/kafka-real-e2e`, base develop430. Schema0/−1 se ignora antes del executor según OpenAPI/SDK mínimo1; no se aplica Validator global que altere el grupo nulo legacy. Autor4 casos rojos y25 verdes; verificador independiente repite4 rojos→25 verdes desde430 limpio, sólo dos archivos. Root ejecuta full722 tests/0fallos/0errores/0skips Java25, compila las tres familias y genera `application.jar`. Escenarios físicos siguen NOT_EXECUTED.
- **Canonical PM:** nuevo master GitHub0c83575 incorpora transporte local de deployments y herencia de entidades. La rama1b4 basada en develop767 conserva adapters de acciones/peek/KVS y autorización aún no canónica. Fuentes/objetos Git y diferencias están versionados en evidence/pm-current-master-*. Matriz351:299FULL preparadas/24PARTIAL/28NONE; las diez filas nuevas carecen de fixtures/cuerpos completos y no se promueven por igualdad de fuente.
- **Limpieza:** inventario final en el contexto Docker propio: cero contenedores (incluidos detenidos), redes y volúmenes Compose. Sin escrituras KVS por clone403; BCs propios retirados con ausencia verificada. No se pausó consumer ni se alteró servicio compartido.
- **Biblioteca:** revalidación focal de master0c sin repin global ni cambiar el validator; dos capacidades nuevas verificadas en fuente (herencia y deploymentKafka local), total vigente691 IDs/194Markdown. Cortes históricos689/3cd quedan explícitos. Validadores estructural/histórico PASS y formal937 byte-idéntico al baseline; peer final y commit documental en curso.
- **Estado:** BLOCKED/entrega incompleta. Managed registry/observer y nuevos joins tienen trabajo de implementación pendiente, además de recursos reales y CI no disponibles. Ledger y DELIVERY mantienen la evidencia versionada, sin capacidades físicas completas certificadas. El permiso Sandbox puntual y las preguntas de destinos Zord/servicios/runner siguen pendientes. No cierre AGENTS OS ni declaración de éxito; tokens/coste desconocidos.

## Fase activa T23/T24 — oráculos y fronteras reales

T23 contrasta las anotaciones del SDK1.3.1 realmente resuelto y productores master0c: el éxito con metadata requerida ausente es un defecto, no un contrato válido. Autor reprodujo64 casos rojos con binding real contra los controllers previos; guard acotado ACK/ignore antes de dispatch en curso, preservando grupo nulo legacy y component/environment nulos de acción precreación. Revisión independiente cleanf80 y validación completa pendientes. Los null-ID no otorgan autoridad para borrar claves globales; observación inesperada exige UNKNOWN y retención durable.

T24 prepara fixtures/cuerpos de los diez joins PM-KAFKA sin reducir alcance por KVS403. Discovery encontró que EntityServiceClientImplLocal responde sintéticamente con revisiones1–100: el perfil real-e2e debe seleccionar el cliente productivo y exigir inputs/revisiones propias verificadas. Aún sin cambios ni ejecución de esos joins. Auditoría de limpieza PM examina borrar KVS/SQL antes de detener todos los workers; no se certifica seguridad por estado terminal aislado. Writers por archivos y Gradle serial: Domain T23, Infra discovery T24, Fault revisión independiente. Gates externos y sesión permanecen abiertos.

## Checkpoint T23 y fases T24/T25/T26 — sesión activa

CP commit `eee5b9091b332a975c78823679a1e99b517632bc`: guards acotados de metadata requerida antes de executor, preservando grupo nulo legacy y component/environment nulos de acción. RED64→GREEN113 controllers+10 HTTP positivos con binding real; peer cleanf80 repitió sin hallazgos abiertos. Root full804/0fallos/0errores/0skips y tres familias compiladas+bootJar. Primer full804/4FAIL por fixtures positivos sin metadata quedó conservado; sólo se completaron esos fixtures, sin cambiar sus aserciones. Jar construido con overlay T23 congelado sobre f80, código guardado después en eee. No evidencia física de contratos CP/KVS/PM. Matriz351:297FULL preparadas/26PARTIAL/28NONE, todos NOT_EXECUTED.

SPEC funcional→técnica→tareas aprobada antes de implementación para T24 joins/EntityService y T25/T26 lifecycle/observación KVS. Writers exclusivos: Infra8Java+2seams Entity, Fault guardian+runner+6paths tests/fixture, Domain4Java journals/wrappers+testFS; root wiring/build/config/evidencia. Revisión cruzada y Gradle serial. Canonical PM checkout limpio `rio-playmaker-kafka-e2e-canonical`, base master GitHub0c83575, overlay restringido sin alterar auth/services/config canónicos. Toolkit resuelto CP1.0.5/PM0.7.4; observación de intentos no implica retries internos ni exactly-once. EntityService master25b34c73 evidencia fuente; target/grants reales aún no conocidos. ImportAPPROVED necesita Odin/notificación real autorizada y contrato de limpieza: no SQL sintético.

KVS clone403, servicios administrados/EntityService/Odin propios, CI y revisión formal Zord siguen gates; trabajo independiente continúa. Sesión/outcome partial, no cierre ni feedback final hasta cumplir encargo; tokens/coste desconocidos. Evidencias file-backed y comandos en CP verification-ledger/DELIVERY.


## Checkpoint 2026-10-02 — integración T24–T26 y revisión Root V4

CP `eee5b909` + overlays: full unit **822 PASS/0skip/64classes** y bootJar; PM candidate full **4386 PASS/2 skips baseline/382classes**, ambos jars canonical0c/candidate1b compilados. Seis arranques reales de los jars PM sin lease válido fallaron antes del puerto HTTP (control de proceso/configuración, no backend). CP guardian dos archivos recibió peer cleanEEE **22 casos/271 checks PASS**, con reap/PID+nacimiento/puertos+temporales verificados; no contrato de negocio certificado.

T24 peer detectó cuatro P2 de orden UNKNOWN/retención Entity/inventario actionLock/row-lock ajeno; fix T24R tres archivos congelado y revisión Domain activa. T25 neutral13/131 peer reproducido; underscore-run corregido en integración posterior. T26 cinco journals/wrappers y testsFS18 reproducidos por otro agente, sin hallazgos de ese scope. RootV1/V2/V3 reviews preservadas: V3 parser21+selection7+nativeJava4 controles satisfechos, dos P2 confirmados (worker plainJUnit sin clienteKVS y exención del cuerpo de clientes canónicos). RootV4 ahora preparado para registrar worker nativo antes de fixture con intent del daemon Gradle y restringir exactamente siete deltas de perfil, más UNKNOWN final durable. Autor de worker separado; Gradle serial. No certificar un autor solo ni convertir controles sintéticos de harness en negocio.

CI cuatro gates obligatorios CP/canonicalPM/candidatePM/managed: ejecución real all-missing intentó cuatro (status2 cadauno), overall1 y artefacto público sanitizado; binding/publication55 y retention16 PASS. Freeze final seis paths pendiente. KL17 docs congelados88+/32: estructura691IDs/194MarkdownPASS; formal937 idéntico baseline/0 nuevos. Peer pendiente y delta de evidencia822 aún no integrado. KVS clone403, Entity scopes ZeroTrustUnauthorized/activeDeployments400, managed/Odin/runner propios y Zord externo continúan abiertos. Último refresh GitHub oficial falló por allowlistIP403; snapshot canónico previamente verificado permanece fechado, no se presenta como latest.

Siguiente paso: integrar RootV4, ejecutar worker normal/fallo79 con Gradle9.3.1 real privado y revisión independiente; recibir T24R/KL/CI peers, compilar tres familias estables, actualizar matriz/evidencia/README y commits/patches. Sesión activa; no cierre ni feedback de éxito. Tokens/coste desconocidos.


## Checkpoint V4 2026-10-02 — cierre de integración todavía pendiente

RootV4 congelado28 paths, SHAJSON `d6da7a6257222b0a28b82bd23212d399f5943bdda3abd7500c4bf7afb8b1e0f3`; writer cerrado para Domain peer. Gradle9.3.1 real propio: plainJUnit1/noSkip/zeroKvsGenerations→command0 con workers[] nativos y taskproof; ownWorkerhalt79→command1 sin successproof, ambos workers ausentes. Domain reprodujo ambas rutas en freshprivatecopies/nativebirth y liberó slot; revisión28/parser aún activa. Worker2 SPI/BeforeAll+PreConstruct ya peer19/224+2SPI/autodetection negativos PASS. Sourceguard7 exactprofiledeltas: dosbaselinesaceptadas/14bodymutantsrechazados; CP snapshot ata Gradle/script/testJava/SPI. UNKNOWNfinalhelperFS7PASS y fallback guardianownCONT/TERM condeadline siemprefalloretained. Comando inicial de escritura fue rechazado auto-review por sobrescritura sin respaldo visible; se guardaron/verificaron backups durables exactos antes de aplicar, sin pérdida ni bypass.

CI6 peerRoot `a4b5446d...`:55binding/publication+7removals/5inputs+actualcleanallmissing4status2overall1/harness0PASS, no findings; job real externo NOT_EXECUTED. T24R3 Domain peer `301a1d0e...` cerrócuatroP2source/FS; no negocio. KL17 Domain peer `7c13417b...`:937formal igualbaseline/estructura691/194PASS; unP2operacional confirmado stop/reapPM versusdrain, delta1sentence privado aúnnoaplicado. READMEefectivo4familias/inputCI/cleanup gates stagedparaInfra peer, no fuente28tocada.

Infra cerró preparaciónretentionUPDATE yphysicalparamsCONCURRENT enunTestFile `0bb0e21e...`; privatejavac8PASS/51sourcecontrols/same22methods36invocations, Fault peer activo. Matrizdelta privado propuesto7FULL/3PARTIAL de10 IDs, global304/29/18; matrizactiva todavía351/297/26/28 y todoscontratosfísicosNOT_EXECUTED. TresfamiliasGradlecompile+bootJar Root activo sólotrasreleaseDomain, source estable porfases. Siguiente: recibirpeers28/testfile/docs, incorporar README/KLP2/matriz/evidencias/ledger, validar biblioteca ycommits/patches, conservar gates externos precisos. Sesión/outcome partial; no cierre hasta entrega independiente completa. Tokens/coste desconocidos.


V4 compile correction checkpoint: actual stable3 command failed at compileRealIntegrationTestJava (frozenRealControlplaneProcess.java:77 local `java` hidespackageUUID), preserving log/hash in root-wiring-v4-compiler-delta/first-compile-failure.json. The two-identifier fix is staged private;28freeze intactpendingDomainreport. Domain actualGradle normal/fatal79 repeatedPASS but explicitly not a whole-suite compile certificate. all-final independent Taskproof missing validation is accepted audit criterion/potentialP2 under neutralcontrol. InfraOneTest oracle seed/mismatch SQL paths missing immediate UNKNOWN found byFaultpeer; no FULLpromotion until repaired. READMEpeer found obsolete old3gate/1SHAsection; stageddocsnotappliedyet. Continue independent corrections; no closure/completeclaim.


### Checkpoint 02/10 — RootV4.1, source peer y gates externos

Root corrigió el package-shadow `java` y registró compile de las tres familias PASS48/42/16clases, sin ejecutar negocio. Los21controles previos y29nuevos typed task/collector metadata PASS; siete false-accepts independientes anteriores conservados. RootV4.1 freeze29 SHA2be8b9deead072c1d8b8373ed8e4b7052b5073deb263d0965a12c2dbdafd2944, peer Domain en curso. PMneutral Root14/159PASS; peer detectó carreras del driver de readiness y leaseSTOPPED, conserva dos fallos y diagnostica waits sin cambiar outcomes. README corregido aplicado tras peer Fault38checks; KLdelta stop/reapANDCPdrain estructural691/194PASS/formal937baselineexact0nuevos. OneTest ef816/P2closed peer c981; matrizpropuesta304/29/18/all351NOT_EXECUTED pendiente peerFault.

Siguiente concreto: cerrar delta readiness driver con reproducción independiente; aplicar matriz/doc/evidence guardados, validar KL y sourcefreeze, commits locales/patches/handoff. NingúnbackendKVS/PM/managed/job ejecutado. Sandbox403,EntityZT/targets/grants,BigQueue/OAuth/SDK/Odin/runner/Spellbook/Zord siguen gates. Sesión AGENTS OS activa; no cierre ni feedback final todavía. Tokens/coste desconocidos.
