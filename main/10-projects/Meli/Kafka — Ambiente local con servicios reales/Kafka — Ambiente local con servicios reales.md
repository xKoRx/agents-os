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
updated: "2026-10-07"
---

# Kafka — Ambiente local con servicios reales

> [!info]+ Kafka — Ambiente local con servicios reales
> **Área:** [[Meli]] · **Estado:** active · **Owner:** Rodrigo · **Fase:** extracción pequeña CP local verificada físicamente dos veces y reproducida desde clon limpio; rama lista para revisión.

## 🎯 Objetivo

Ejecutar E2E del [[rio-controlplane-kafka]] contra Kafka real usando un mapa simple en memoria para la idempotencia local, conforme a la decisión explícita del owner del 2026-10-05. Fury KVS Sandbox deja de ser requisito para esta familia. Primero CP Kafka; Playmaker y el resto del ecosistema quedan para una fase posterior.

Mantener controllers, validadores, handlers, procesadores, provisioners y guard reales del CP. Comprobar efectos Kafka, resultados correlacionados y estado del mapa de la misma aplicación. El mapa no certifica persistencia tras reinicio, exclusión entre JVMs ni el cliente/servicio Toolkit productivo. La producción conserva su backend. La comparación histórica de implementaciones vive en [[Ambientes locales RIO — Comparativa de implementaciones]].

## 📊 Estado actual

- **Entrega pequeña 07/10 — objetivo vigente:** `rio-controlplane-kafka-local-small`, rama `feature/kafka-local-small`, commit `eb16f5f1ef63466bcdb8ee1266eabb7ea3f21d10`, desde develop remoto verificado `4302481c69300074a85ea5eb051a27bbd505cdce`. PROVISION, UPDATE, DEPROVISION y PEEK acción/REST más errores contractuales: dos corridas finales **9/0/0/0 PASS** desde ambientes vacíos y reproducción independiente **9/0/0/0 PASS**. CP real, un broker Kafka real RF1, KVS mapa por JVM y resultados Kafka reales; cleanup físico y packaging productivo PASS. Diff 14 archivos (11 añadidos, 3 modificados); sólo dos anotaciones de perfil en configuración productiva, sin cambios de negocio. `local/README.md` contiene start/test/stop. Original y congelado íntegros; sin PR, push, CI ni integraciones del ecosistema. Revisión independiente sin findings materiales; Zord formal no ejecutado por rechazo automático de envío de diff privado, consulta de autorización/omisión pendiente. Registro breve y SPECs proporcionales en el control externo de esta ejecución; atribución en los agent runs `kafka-small-local-*`.

- **Ejecución funcional activa 06/10 (supersede el recheck de sólo lectura):** runtime propio `colima-rio-kafka-e2e-01a0f8e0` disponible con 6.198.423.552 bytes; handshake Kafka real desde host39092–39096 verificado, shared default intacto. Baseline unfiltered `cc21725628c84592b64113606ff072e7`: **348 tests,261 PASS,87 FAIL,0errors/skips,cleanup PASS**. 845 unit+compile PASS hoy. Fixes exclusivos GPT-6 Luna: prefijo Compose corregido; binding action envelope `publish_time` opcional según OpenAPI; fixtures RF/metadatos y cobertura childrouting en curso. No certificación completa todavía. El SIGKILL previo conserva causa desconocida; el runtime actual no depende de Fury/VPN. Continuación: fixes→fullunfiltered→freeze→replay independiente desde clone limpio→evidencia/knowledge. Control activo `/private/tmp/kafka-e2e-validate-20261006/execution-control.json`.

- **Consulta/recheck 06/10 (sólo lectura):** CP4c66d0d limpio. Docker actual `colima`27.4.0/aarch64 tiene2054631424bytes (~2GiB), menor que el gate5GiB. No se repitieron pruebas de negocio hoy. Último E2E sigue343/309fallos y objetivo físico incompleto. Patrones de perfil/adapters contrastados con KMSdevelop7fe7745, ClickHouserama7de630c y Playmakerrelease5abe5c2; no estándar E2E común ni pruebas físicas de otrosCP certificadas. [Recibo actual](delivery/2026-10-06-kafka-e2e-status/status.json).
- **Decisión aplicada 05/10:** `LocalInMemoryKvsClient` por instancia con create exclusivo, CAS, versión local, TTL y copia de bytes; perfil `local,real-e2e,memory-e2e`. No requiere Fury, VPN ni Sandbox para este backend. El runtime/CI usa Kafka real y transporte de resultados Kafka. Ecosistema después.
- **Código entregado:** implementación CP `7615b210e5b70667912b956c2f27cc0d1ebc80eb`; cierre documental `4c66d0d5ca77e1de4aef5b08c9e601921eb60a9b`, rama `feature/kafka-e2e-memory`, worktree limpio `/Users/rjara/fuentes/rio-controlplane-kafka-memory-e2e`. Base `7f1720d950446638ff9b15a0e4e167f3e8e26e43` y checkout anterior preservados. SPEC funcional→técnica→tareas: delta `LOCAL-MEMORY-1` en `meli/features/20261001-real-e2e/`. Rama pendiente; no producción/push/release.
- **Verificación independiente PASS:** clon nuevo detached de `7615b21`, Java25/Gradle9.3.1 offline, `test compileRealIntegrationTestJava`:65 clases/845 pruebas/0 fallos/0 errores/0 skips;33 fuentes sin drift. Los49 controles de launcher/verificador también PASS. GenerateDocTest cambió su Swagger generado en el clon propio; diff preservado. Ninguno de estos controles acredita E2E Kafka.
- **E2E físico FAIL/BLOCKED:** corrida `48711a6c7ffa43dc88c44b2d4b1db4b1`:343 invocaciones,309 fallidas,34 PASS,0 skips. Cinco brokers internos saludables, pero host `127.0.0.1:39092` rechazó conexión y el primer fixture agotó el timeout. Tres assertions del adapter comparaban enum contra string; corregidas sin cambiar oráculos CAS y con replay pendiente. La corrida fallida original sigue conservada.
- **Bloqueo vigente preciso:** forwarding SSH del Colima propio recibió SIGKILL (PID41272,exit-9); causa desconocida. Sin fix causal demostrado. VM propia detenida y recursos de corrida retirados; Colima compartido tiene2GiB y no fue modificado. Hace falta un runtime Docker propio con≥5GiB y listeners host39092–39096 accesibles. No se necesita login Fury ni un alias KVS.
- **Reproducción:** en el nuevo worktree, `DOCKER_CONTEXT=<contexto-propio-operativo> JAVA_HOME=<jdk25> ./e2e/local.sh` (opcional `--offline`). El default `./e2e/run.sh` selecciona la misma familia. Un comando realiza startup/test/teardown; faltantes o fallos retornan nonzero. Retiene recursos propios si la reconciliación es UNKNOWN o queda trabajo pendiente. Reportes por corrida en `build/local-e2e/<run>/`. CI `.github/workflows/local-kafka-e2e.yml` implementado, job externo NOT_EXECUTED.
- **Cobertura honesta:** matriz local356:5 PASS únicamente a nivel adapter/config unitario,226 BLOCKED por Kafka host y125 NOT_EXECUTED fuera de la selección local. Matriz remota351 intacta. GCP plaintext no certifica OAuth; Kafka local no certifica BigQueue. Las fronteras y escenarios excluidos están en `e2e/LOCAL.md` y la matriz. No se declara completo el E2E.
- **Knowledge y continuidad:** `docs/kafka-e2e-memory@0feee7b5fad32c8c7dc3dcc252d65166b15c0cd9`, worktree limpio `/Users/rjara/fuentes/ads-signals-knowledge-library-kafka-memory-e2e`; delta5docs de la biblioteca con contratos/capas/gates actuales; master canónico auditado permanece separado de la rama pendiente. Paquete durable [handoff, parches y evidencia](delivery/2026-10-05-kafka-memory-e2e/HANDOFF.md). Próximo: restaurar el runtime propio→suite local completa→repetición independiente limpia y fallas críticas→job CI con runner elegido. Sesión AGENTS OS activa/parcial; tokens/coste desconocidos.

### Corte histórico previo a la decisión de mapa (superado para la familia local)

- **Revalidación 05/10:** Fury Tiger presente/vencido;0API remotas. Clone403 del02/10 no reintentado. Fix auth-before-SDK preparado con27PASS+10peer/74harness y patch5paths portable; aplicación original no ejecutada por fallo de capacidad del reviewer automático. CP7f1720d/KL5c4cb45 permanecen limpios. [Continuidad actual](delivery/2026-10-05-kafka-kvs-resume/HANDOFF.md).
- **Veredicto: BLOCKED; objetivo incompleto.** [Handoff durable](delivery/2026-10-02-kafka-e2e-blocked/HANDOFF.md) y [cinco parches/índice](delivery/2026-10-02-kafka-e2e-blocked/delivery-index.json) conservados en el vault. El ensayo físico completo CP/KVS/Playmaker/managed y el job CI siguen NOT_EXECUTED. No cierre de sesión ni certificación final.
- **Fuente guardada:** CP `7f1720d950446638ff9b15a0e4e167f3e8e26e43`, Playmaker candidato `acbda2f1e68ae7672de6f9571cd739da972ca07a`, overlay master `47df54fe1e341be6b1c2304a2c098b0c01d626e1`, SDK `97146e9fde6cb2d947b7978ba2ba2491d11f06b5`, knowledge `5c4cb45d9fa8c3e4a95d73542ecd58c04c7c1530`. Cinco worktrees limpios; originales y cambios previos preservados. Sin push/PR/release/despliegue. WORK_BRANCH_PENDING, no producción. Bases/ramas/SPECs exactas en el índice.
- **Matriz:** 351 capacidades/22 columnas; 304 FULL preparadas, 29 PARTIAL, 18 NONE; **351 NOT_EXECUTED** en su contrato físico completo. FULL significa preparación revisada. Matriz SHA `2f0d813088fe8b6d2e88a8c39bc5d850edebc2a860bc0d3dbd34040111b2c50e`. Decisión implementada: source sets en CP, extensión aislada del harness Playmaker, cinco brokers para AWS RF1–5/GCP RF1–3.
- **Validación real y límites:** CP822 PASS/0skip; PM4384 PASS de4386/2 skips baseline; SDK708 PASS/0skip. Compilación de tres familias y ambos jars PM PASS. Kafka real5/RF1–5/ISR, MySQL37 y controles físicos propios PASS; reproducción independiente de ownership/journals/taskproof y cinco parches sobre bases limpias PASS. Esos scopes no certifican negocio Sandbox. CI all-missing intentó cuatro gates: status2 cada uno/agregado1; no job externo ejecutado. Último inventario Docker propio:0 contenedores/volúmenes/redes de corrida.
- **Knowledge concreta:** 17 documentos actualizados contrastando master GitHub fechado y evidencia runtime. Estructura691 IDs/194 Markdown, histórico y diff PASS. Formal FAIL937, bytes idénticos al baseline/0 errores nuevos. Sin repin global ni weakening del validador. Ledger95 conserva REDs y peers; fuente final29 paths sin drift, SHA `23409c2bc593f8373a419255e4c00b08747f8d01f2499a95e17755795f50b0b1`.
- **Siguiente paso (prioridad CP):** resolver el403 de clonación Sandbox del KVS propio CP, reproducido con VPN/auth válidos, o indicar otro alias propio autorizado; preparar sólo su Sandbox con `--scope cp`. Ejecutar Toolkit real y `realIntegrationTest`; el ecosistema y proveedores quedan para después. Sus aliases/targets/grants/recibos/runner permanecen registrados como gates de esas familias posteriores. Ejecutar Toolkit create/versión/CAS/TTL → CP completa → ambos Playmaker → managed → job CI → reproducción independiente limpia/casos críticos. Zord necesita autorización explícita de destinos/acción y Spellbook renovación privada. Auto-review rechazó el envío externo del diff privado y la actualización persistente del cursor. Tokens/coste desconocidos. El handoff detalla acciones, comandos, cleanup y evidencia.

### Historial de ejecución (cortes anteriores)

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
| [[rio-controlplane-kafka]] · extracción pequeña vigente | `feature/kafka-local-small` · `rio-controlplane-kafka-local-small` | develop remoto `4302481c69300074a85ea5eb051a27bbd505cdce` | Encargo 07/10 y SPEC funcional breve del control de ejecución | SPEC técnica/tareas breves del mismo control; adapters y perfil aislados | Commit `eb16f5f`; dos suites 9/0/0/0 y replay limpio 9/0/0/0 PASS; revisión independiente PASS; Zord pendiente |
| [[rio-controlplane-kafka]] · CP local memoria actual | `feature/kafka-e2e-memory` · `rio-controlplane-kafka-memory-e2e` | Candidato `7f1720d950446638ff9b15a0e4e167f3e8e26e43` sobre develop previo | Delta `LOCAL-MEMORY-1` en funcional | Delta `LOCAL-MEMORY-1` en técnica y tareas | Implementación7615b21/docs4c66d0d;845 unit/compile peer PASS; físico BLOCKED |
| [[ads-signals-knowledge-library]] · memoria local actual | `docs/kafka-e2e-memory` · `ads-signals-knowledge-library-kafka-memory-e2e` | Candidato `5c4cb45d9fa8c3e4a95d73542ecd58c04c7c1530` | Decisión owner05/10 y auditoría |5docs delta fuentes/capas/runbook | Commit0feee7b; estructura/histórico PASS; formal937 preexistentes idénticos |
| [[rio-controlplane-kafka]] · `melisource/fury_rio-controlplane-kafka` | `feature/kafka-real-e2e` · worktree hermano `rio-controlplane-kafka-e2e` | `develop@4302481c69300074a85ea5eb051a27bbd505cdce` | `meli/features/20261001-real-e2e/1-functional/spec.md` lista; publicación SIG bloqueada por sesión | `meli/features/20261001-real-e2e/2-technical/spec.md` lista | Implementación/suites compiladas; real E2E pendiente |
| [[rio-playmaker]] · `melisource/fury_rio-playmaker` | `feature/kafka-real-e2e` · worktree hermano `rio-playmaker-kafka-e2e` | `develop@7673f4bffc286f0f24d4214938df53c4c5eb9c38` | Funcional E2E del CP compartido, lista | Técnica E2E del CP compartida, lista | Adapters acciones/peek/KVS y launcher propios implementados; gates de ejecución pendientes |
| [[ads-signals-knowledge-library]] · `melisource/fury_ads-signals-knowledge-library` | `docs/kafka-real-e2e` · worktree hermano `ads-signals-knowledge-library-kafka-e2e` | `master@de7cde85f7dd83a673c918e22ae9f08a0f7e05bd` | Contrato de auditoría del prompt maestro | Correcciones canónicas y documentación pendiente de E2E | Auditoría y correcciones verificadas en curso |
| [[rio-sdk-events]] · `melisource/fury_rio-sdk-events` | `feature/kafka-e2e-publisher-fix` · worktree `rio-sdk-events-kafka-e2e` | `master@ad2c98b806cffb88b23513f87785932aa1707ea4` | Delta funcional compartido del CP | Delta técnico SDK en SPEC del CP | Corrección segment/buffering, regressions red→green708 reproducidos independientemente; release/backport y delivery real pendientes |

El flujo de entrega sigue Spellbook: SPEC funcional → SPEC técnica → tasks → implementación. Completar ramas y ambas SPEC antes de modificar código. Incluir otro repositorio en esta tabla sólo si el diseño demuestra que necesita un cambio.

## 🧩 Alcance histórico anterior (Sandbox/ecosistema; superado para CP local)

1. **Infraestructura compartida:** reutilizar el Compose de Playmaker y agregar un perfil o archivo para tres brokers, volúmenes, healthchecks y listeners internos/externos. Un comando levanta infraestructura y arranca las dos aplicaciones con versiones y puertos explícitos.
2. **Control plane real:** consumir los triggers locales con los DTO y validadores vigentes; delegar a los procesadores existentes; crear, actualizar y borrar topics mediante `AdminClient` real; publicar resultados a Kafka local con confirmación del broker.
3. **Conexión de datos:** habilitar una configuración local explícita hacia los brokers del Compose. El flujo GCP necesita desacoplar la obtención de `AdminClient` de la autenticación OAuth para ejecutar su provisioner real contra el cluster local. AWS ya tiene una fábrica plaintext. El perfil de integración debe evitar exigir una SA GCP sólo para administrar Kafka local.
4. **Acciones y PEEK:** extender el transporte local de Playmaker para acciones y conectar su cliente HTTP de PEEK al control plane. En `local` hoy siguen seleccionándose un productor de acciones no-op y un cliente PEEK que devuelve un mensaje sintético.
5. **Idempotencia real:** configurar un contenedor aislado de KVS Fury Sandbox con el SDK actual y probar create/CAS, versión, TTL, redelivery y reinicios. Validar primero la versión asignada por el servidor después de create, el conflicto de versiones y el incremento tras un update válido: el guard depende de esos comportamientos. No copiar identificadores de sandbox de KMS.
6. **Verificación automática:** escenarios de ciclo de vida, datos, replicación, routing y errores con evidencia en Kafka, KVS y MySQL, ejecutables mediante Gradle y en CI. Reservar una validación de integración con servicios reales no productivos para OAuth de GCP, transporte BigQueue y otras dependencias que Compose no reproduce.
7. **Disponibilidad verificable:** el launcher del perfil de integración debe comprobar Kafka y KVS real, rechazar wiring no-op/archivos y explicar qué configuración falta. Una dependencia corporativa ausente debe producir un fallo visible en las suites que la requieren. Las pruebas de caída posterior de un KVS real verificarán la política de degradación vigente del producto.

## ✅ Tareas

### Extracción pequeña vigente — 07/10

- [x] Verificar develop remoto y preservar checkouts original/congelado.
- [x] Entregar wiring local aislado, broker único, KVS efímero y transporte de resultados reales.
- [x] Verificar cuatro flujos y errores mediante endpoints, resultados terminales y efectos Kafka.
- [x] Repetir suite completa desde dos ambientes vacíos y reproducir en clon independiente limpio.
- [x] Confirmar limpieza exclusiva, packaging productivo y conservación de negocio.
- [ ] Revisión humana de la rama; decidir autorización u omisión de Zord formal.

## Tareas históricas — desarrollo congelado, fuera del candidato

- [x] Registrar decisión del owner y delta SPEC funcional→técnica→tareas `LOCAL-MEMORY-1`.
- [x] Implementar mapa y selección explícita del perfil local; conservar lógica del CP.
- [x] Implementar launcher, task Gradle local, selección, informes y workflow CI.
- [x] Reproducir unit/compilación desde clon independiente y revisar controles de resultado/cleanup.
- [x] Actualizar la knowledge library con alcance local en memoria y evidencia sin afirmar producción.
- [ ] Resolver runtime Docker propio/forwarding host con≥5GiB y puertos39092–39096.
- [ ] Ejecutar toda la suite local y casos críticos de falla; verificar repetibilidad y cleanup.
- [ ] Reproducir ruta completa desde checkout limpio con revisor distinto.
- [ ] Ejecutar job CI local en runner autorizado; adjuntar resultado real.
- [ ] Cerrar objetivo y sesión con feedback AGENTS OS sólo cuando los gates físicos estén satisfechos.

## ✅ Tareas históricas — anteriores a la decisión de mapa

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


## Checkpoint final de fuente 2026-10-02 — continuidad BLOCKED

Cinco commits locales finales y originales preservados; parches durables en `delivery/2026-10-02-kafka-e2e-blocked`. Peer independiente aplicó los cinco sobre clones limpios de bases exactas y comparó árboles con los HEAD exportados: PASS5/5, refs originales intactas y clones retirados. Root V4.1 r2 cerró typed owner PID y races del driver sin cambiar expectativas; peer PASS,0 findings. Matriz final351/304 FULL preparadas/29 PARTIAL/18 NONE/all351 NOT_EXECUTED; sourcefreeze29 SHA23409c2bc593f8373a419255e4c00b08747f8d01f2499a95e17755795f50b0b1,0 drift. Peer documental228 checks y tareas37 PASS sólo fuente; aceptación física/formal abierta. KL691/194 estructural/histórico/diff PASS, formal937 baseline idéntico.

CP3bea4809; PM candidatoacbda2f1/canónico overlay47df54fe; SDK97146e9f; KL65bcbb97. No publicación ni adopción SDK. La revisión formal Zord continúa bloqueada por auto-review y autorización externa pendiente. KVS clone403, target/grants Entity/Tiger/ACME/Odin, BigQueue/OAuth/MSK propios y runner CI impiden completar contratos físicos. Handoff durable conserva acciones exactas y comandos efectivos. Outcome partial; sesión activa. No feedback final de éxito ni cierre hasta cumplir encargo. Tokens/coste desconocidos.


Handoff final revisado: dos frases corregidas para declarar preparación de autorización y limitar MySQL a37 migraciones; peer delta8 checks PASS, findings cerrados. Cinco parches portables PASS5/5 desde bases limpias; último recheck confirma cinco heads limpios, source29/patches/matriz sin drift, cuatro originales sin cambios y Docker propio vacío. Paquete durable `delivery/2026-10-02-kafka-e2e-blocked/HANDOFF.md`/`delivery-index.json`/`SHA256SUMS`. El gate físico completo sigue BLOCKED/351 NOT_EXECUTED; sesión activa y feedback parcial registrado, sin cierre ni éxito final.


## Prioridad del owner 2026-10-02 — Kafka CP primero

El owner precisó que necesita ejecutar E2E propios del CP Kafka; ecosistema queda para después. CP-SCOPE-1 registrado en SPEC funcional→técnica→tareas antes de código. Se detectó acoplamiento del helper Sandbox a dos apps aun en `realIntegrationTest`: nuevo `up --scope cp --cp-service <alias-propio>` prepara sólo CP y no pide servicios/aliases Playmaker. Gates CP vs ecosystem explícitos; default/legacy ecosystem preservados. Fuente9 paths congelada para peer Fault; root compileCP PASS y61 controles harness PASS; forwarding real launcher/Gradle cp/cp/ecosystem PASS sólo metadata, stops antes de negocio. Infra25 controles incluye2 RED baseline conservados. No suite física ejecutada ni capacidad promovida.

Read-only auth guard del SDK el 2026-10-02T15:31:37Z devolvió SANDBOX_FURY_LOGIN_REQUIRED; sesión Fury actual vencida. Cero llamadas remotas/valores de credenciales publicados/renovación. Se pidió al owner renovar Fury en el equipo; después revalidar clone del alias propioCP `triggers-status-nonprod`. El403 anterior con auth vigente es evidencia histórica, no refresh actual exitoso. CP local no depende de Entity/Tiger/ACME/Odin/Playmaker/BigQueue/OAuth administrados; esos gates sólo quedan en alcances posteriores. Próximo: peer de setup → commit/checkpointCP y runbookKL → auth renovada → provisión CP-only propia → contrato Toolkit real → suite `realIntegrationTest` completa/repetida. Sesión activa/outcome parcial.

## Checkpoint CP-only fuente revisada — 2026-10-02

Owner mantiene Kafka CP primero; ecosistema posterior. CP commit local `5b038f52a8bf4c11deabb86143ff4d4decaefc60` y KL `0c3448a14f3d8f2318a1c34d964ab57561917a20`, ambos checkouts limpios. Sourcefreeze13 SHA65393ccb8af0fbce63938431d7741e7fcbdc42dc296c6e2357e8c2759ff4027a; freeze9 inicial queda histórico. Compile CP PASS; `validateRealE2eHarness`72 controles source/metadata PASS (25 Sandbox +8 managed +11 CI +5 cleanup +16 retención +7 filesystem). Fault v2 SHA48483269a3ae0f8c1a62cf9b3739e85697d16005cd1ec9c1cd18ba5f27df5e38 PASS,0 drift/0 findings; P2 trap EXIT preexistente y bare-variable nuevo cerrados, todos los RED previos conservados. Domain doc delta SHAfbf4aba8f9022459cadd1d4a919a8e1af3fd74a96fce1bd0142d57abf7f5e74a PASS, tres contradicciones cerradas. KL estructural691/194 e histórico/diff PASS; formal FAIL rawSHA268be6f39a764e42569d5deafe535299f01bc5be000245779e9bd2e18bb9cdf5 idéntico baseline,0 nuevos.

Paquete durable separado `delivery/2026-10-02-kafka-cp-only-source/HANDOFF.md`, index y parches delta/completos; anterior paquete bloqueado intacto. Originales4 refs/status read-only coinciden con baseline; no auditoría nueva de bytes originales. Matriz351/SHA2f0d813088fe8b6d2e88a8c39bc5d850edebc2a860bc0d3dbd34040111b2c50e sin cambios y todas NOT_EXECUTED para capacidad física completa. No CP/KVS/SDK negocio en estos controles. CI dispatcher aún agrega4 familias y no acredita job CP-only separado; pipeline real NOT_EXECUTED. Próximo concreto: owner renueva Fury (pregunta pendiente), read-only guard/login válido → clone propioCP recheck (403 histórico, no refresh actual) → Toolkit server create/version/CAS/TTL → `realIntegrationTest` completa/repetida desde checkout limpio. No depende de permisos del ecosistema para ejecutar CP local. Sesión activa/outcome parcial; cierre y feedback final sólo al completar objetivo. Tokens/coste desconocidos.

Replay portable del delta CP-only completado: PASS4/4 (CP y KL delta/completos aplicados desde bases exactas, árboles==HEAD). Receipt SHA4d6171a221a3eeef25f730b3f36ab13b059e9983d2f68695db0ba66a5cfc86a2, summary SHA8886323583ddc73a9146f5cd7b0d953ec05a84b09cabd61c6e7c57b83129ad48. Dos WTs/four originales refs/Git-visible estado sin drift; cuatro clones retirados. Import/tree-only, no negocio. Suplemento final-checkpoint.json y SHA256SUMS verificados; se mantienen auth requerida, full CP NOT_EXECUTED y sesión activa.

## Recheck real CP después de VPN — 2026-10-02

Owner confirmó VPN conectada. Auth almacenada PASS; API Sandbox alcanzado y lifecycle CP-only real create200→clone403→delete200→GET404. BC/run propio f76a79f1799a420ebfe7d3dfa9b0f670, ausencia corroborada mediante GET independiente (peer73b97249cf871907267497fc886c529dc16606f838c6be219c076a8e24bd80d3). No instancia/KVSwrites,0 mutaciones UNKNOWN, cleanupCERTIFIED_API_ABSENCE. Inventario ownCP vía ServicesApi primario GET200; coincidencia exacta `triggers-status-nonprod`, statusapproved/container_type database/test_containertrue. Alias visible no implica Sandboxability;403 no permite decidir entre elegibilidad y autorización. Login/VPN dejan de ser el bloqueo actual.

Runtime local READY (JDK25, Docker propio4CPU/~5.77GiB, imagenARM64 pinned cacheada,0containers); no se inició negocio. Root actualizó dos docs y receipt CP; Domain peer de3paths PASS/0findings SHA7e6a169a442888dae3a2372894e601a1e396d0cd74f98e4574b0af7d27ca248b. KL estructura/histórico/diffPASS y formalFAIL baselineidéntico268be6.../0nuevos. Commits locales CP45ff4504cadeb3b8271a0c9020e610edad11ab77 y KLe89a2a58b7ff06b368f2820b60ed0ec4f0b7e28d, limpios. Fuente del runtime al ejecutar5b038f, cambios posteriores sólo documentación/evidencia. Paquete durable `delivery/2026-10-02-kafka-cp-vpn-check` con index/handoff/SHA256SUMS; anteriores cortes intactos.

Pregunta puntual pendiente: habilitar/confirmar clonación Sandbox del alias propio para identidad actual o indicar otro alias propio CP autorizado. Después ownSandboxCP→contratoToolkitserver→suiteCPcompleta→repetición limpia independiente. FullCP NOT_EXECUTED/BLOCKED; ecosistema posterior, sin no-op/mock/skip. No cierre AGENTS OS ni feedback final todavía; sesión activa/parcial. Tokens/coste desconocidos.

## Lookup oficial Sandbox/KVS — 2026-10-02

Owner pidió comprobar beta. Guías live Sandbox1.3.12/KVS2.0.43/CLI5.24.0 documentan servicios reales/KVS soportado, Commiter+ y Vault excluido. Sin etiqueta beta en páginas revisadas; búsqueda beta NoResults no acredita GA. Rol efectivo/Vault/elegibilidad concreta/cause403 permanecen NOT_VERIFIED. Independent Fault review de inferencias y3paths PASS/0findings; no lectura browser independiente ni certificación E2E. CP `7f1720d950446638ff9b15a0e4e167f3e8e26e43` y KL `5c4cb45d9fa8c3e4a95d73542ecd58c04c7c1530` clean, sólo docs/evidencia. Validadores estructural691/194 e histórico PASS; formal937 byte-idéntico baseline268be6/0nuevos. [Handoff y fuentes](delivery/2026-10-02-kafka-sandbox-docs/HANDOFF.md). Gate CP sigue clone403, KVS writes0/fullCP NOT_EXECUTED. Próximo: confirmar rol y elegibilidad del alias propio/razónbackend; repetir lifecycle CP-only y suite completa al habilitarse. Sesión active/partial, tokens/coste desconocidos.

## Reanudación CP/KVS — 2026-10-05

Owner pidió continuar CP Kafka. Auth guard directo12:59/13:08Z devuelveLOGIN_REQUIRED;13:04 metadata confirma token/snapshot presentes, Tigerexpired y ZTausente, sin causar claims de permiso/backend. SDKconstructor local falló antesauth por logger ~/.fury/logs PermissionError; approval SDK y aplicación5paths rechazadas por reviewermodelcapacity,0execution/no unsafejudgment. Alternativa segura: authread-only y candidatecheckout propio en /private/tmp, nunca escritura protegida víaotrocanal. SPEC→tech→tasks CP-AUTH-1 preparados; baseline27FAIL3/candidate27PASS; Fault peer SHA166b95b94b656e2c17262e006a157ba0004c9ac5fb34a3392d9281b62aeca830 PASS+10controls, Domain3docdeltaPASS. Harnessmandatory74PASS sobreclone limpio; patch5paths replayPASS SHA9675d52dc71c84d6b5e565f1eefa6dce89ffde5e15a60aefc85550432aae846b. AggregationAssertion53vs74 preservada; añadióconteos reales5cleanup+16retention desde mismo log, sin rerun/expectationchange. Originales CP7f1720d/KL5c4cb45 unchanged/clean; no newcommit/push. [Packet/handoff](delivery/2026-10-05-kafka-kvs-resume/HANDOFF.md). Estado BLOCKED currentauth+approvalcapacity; clone403histórico/noAPI/KVSwrites0/fullCP NOT_EXECUTED. Ownerlogin solicitadoasync pendiente; después auth→ownCPprovision→contratoSDKserver→suite completa/repeat. Ecosistema posterior. Sesión active/partial sin cierre; tokens/coste desconocidos.


## Cierre explícito — extracción pequeña — 2026-10-07

El owner solicitó cerrar esta sesión y dejar feedback. La entrega vigente es `feature/kafka-local-small@eb16f5f1ef63466bcdb8ee1266eabb7ea3f21d10`: 11 archivos añadidos y 3 modificados; dos ejecuciones finales de 9 pruebas sin fallos desde ambientes vacíos, más reproducción independiente de 9 desde clon limpio. Guía operacional en `local/README.md`: `start` crea Kafka y arranca el CP; `test` crea, prueba y limpia; `stop` elimina exclusivamente recursos propios. Docker/Colima debe estar iniciado. `AGENTS.md` heredado quedó intacto; no referencia esta guía.

Sesión cerrada, rama limpia y sin infraestructura propia activa. Los checkpoints anteriores conservan el estado histórico del alcance congelado; no describen esta entrega pequeña. Siguiente acción: revisión humana del diff y decidir la revisión formal Zord, NO REVISADO porque auto-review rechazó exportar el diff privado sin autorización específica. No hay PR ni push. Feedback: [[2026-10-07-kafka-small-local-session-feedback]].
