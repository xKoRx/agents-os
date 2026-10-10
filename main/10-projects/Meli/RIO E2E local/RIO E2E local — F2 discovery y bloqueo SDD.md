---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: ["[[RIO E2E local]]", "[[RIO E2E local — Diseño revisado]]", "[[rio-playmaker]]", "[[rio-controlplane-kafka]]", "[[rio-controlplane-clickhouse]]"]
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-09"
updated: "2026-10-09"
---

# RIO E2E local — F2 discovery y bloqueo SDD

## Propósito

Registrar el discovery autorizado de F2 al 09/10/2026, su identidad recuperada por fetch y el bloqueo previo a SPEC. Este documento es evidencia de lectura, no SPEC READY, implementación ni aceptación física. El proyecto permanece activo; AGENTS OS no se cierra.

## Contenido

**Checkpoint histórico:** el bloqueo de autoridad quedó resuelto por la instrucción posterior del owner de escribir SPEC y continuar de inmediato. Se usa el catálogo SDD vigente, sin copiar/migrar skills. Las SPEC funcional/técnica/tasks READY de F2 ya existen por repo en `meli/features/20261009-rio-e2e-local-clickhouse/`; la ejecución actual vive en [[RIO E2E local]]. Los estados BLOCKED/NO_EJECUTADO siguientes describen el discovery previo, no el gate actual de implementación.

### Gate previo a SPEC: BLOCKED

El prompt exige que las únicas skills canónicas vivan en `80-agents/skills/` y ordena: «Si falta una skill necesaria, registra el bloqueo concreto sin inventar una ubicación». El bootstrap canónico fue leído/ejecutado una sola vez. Su catálogo [[80-agents/skills/INDEX|AGENTS OS Skills — Índice]] enlaza `sdd-workflow` y `sdd-developer` en `30-resources/agents/skills/`; ambas carpetas existen allí, pero ninguna existe bajo la raíz que exige el pedido. El router Meli también está enlazado fuera de esa raíz. No se invocaron esas copias, no se copiaron ni migraron skills y no se sustituyó SDD por un procedimiento inventado.

Se presentó al owner una aclaración de autoridad: usar las skills federadas que declara el catálogo vigente o conservar el bloqueo hasta disponer de las canónicas exigidas. No hay respuesta al registrar este checkpoint. La falta de respuesta no es autorización. Discovery de sólo lectura continúa dentro del alcance ya autorizado; SPEC/PLAN/TASKS READY e implementación dependen de resolver esta discrepancia.

### Identidad vigente antes de SPEC

| Repo | Origin | Checkout / rama actual | HEAD actual | Base remota recuperada | Estado inicial y final |
|---|---|---|---|---|---|
| Playmaker | `git@github.com:melisource/fury_rio-playmaker.git` | `rio-playmaker-rio-e2e-local`, `feature/rio-e2e-local-kafka` | `c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f` | `origin/develop = 1ba12db957576db04eca686c16e6afac7564edd1` | limpio; sin cambios fuente |
| CP Kafka | `git@github.com:melisource/fury_rio-controlplane-kafka.git` | `rio-controlplane-kafka-rio-e2e-local`, `feature/rio-e2e-local-kafka` | `90710a590794e8a35b39f420013b24e2367ea4c1` | `origin/develop = 6a91937c0664d83f907dec222af8a96b4042c6ae` | limpio; sin cambios fuente |
| CP ClickHouse | `git@github.com:melisource/fury_rio-controlplane-clickhouse.git` | checkout de su entidad `rio-controlplane-clickhouse`, `develop` | `c8b20b6531a73348314587fc14f43e0ad8ce76ae` | `origin/develop = cf17797ef9bc1eb9b9bdb3329e6c70bfc8231386` | las mismas ocho modificaciones tracked y dos entradas untracked ajenas |

Los objetos fueron recuperados mediante `git fetch --no-tags`, no inferidos de `ls-remote`. Referencias adicionales locales de lectura: PM `refs/rio-e2e-f2/reference/pm-pr-1286`; CP Kafka `refs/rio-e2e-f2/reference/cpk-pr-86`. Coinciden con los HEAD publicados y con sus checkouts. No se creó rama F2, worktree, commit de producto ni PR.

Dependencia F1: ambos PRs siguen OPEN y ready. El fix DEPROVISION `b6030980501139723338390a70458f111e5d2a7f` es ancestro del HEAD PM actual; no requiere cherry-pick duplicado ni merge previo. Las bases remotas PM/CP Kafka no tienen nuevos commits fuera de los deltas ya integrados en F1. Se releyeron las SPECs/tareas/VERIFICATION F1, guía PM `local/RIO_E2E.md`, aceptación `PR_INTEGRATION_REVIEW.md` y revisión `PM_UPSTREAM_AUTH_MERGE_REVIEW.md`; `SIMPLIFICATION_REVIEW.md` conserva carácter histórico.

Cambios ajenos CH preservados: `README.md`, `docker-compose.yml`, `KvsOwnershipService.java`, `OnPremiseClickHouseClient.java`, `CredentialGenerator.java` y sus tres tests; además `.graphifyignore` y `local/`. Fetch sólo actualizó refs/objetos. No reset, clean, stash, merge, checkout ni extracción de esos cambios.

### Checks remotos F1 observados de nuevo

| Repo / HEAD | Resultado vigente de lectura |
|---|---|
| [Playmaker #1286](https://github.com/melisource/fury_rio-playmaker/pull/1286) / `c3ecf8c` | CI6144, cobertura, dependencias, static-analyzer y workflow SUCCESS; Code Reviewer terminó NEUTRAL. Code Scanning sigue `startup_failure`: [37975496615](https://github.com/melisource/fury_rio-playmaker/actions/runs/37975496615) y nueva ejecución [37976397528](https://github.com/melisource/fury_rio-playmaker/actions/runs/37976397528), ambas sobre este HEAD. No se modificó ni reintentó workflow. |
| [CP Kafka #86](https://github.com/melisource/fury_rio-controlplane-kafka/pull/86) / `90710a5` | CI551, cobertura, dependencias, static-analyzer, workflow y CodeQL SUCCESS; Code Reviewer NEUTRAL, empty SARIF SKIPPED. |

El resumen `statusCheckRollup` PM omite el fallo de arranque de Code Scanning; se verificó además la API de workflow runs. El verde local histórico no modifica este gate remoto. No se aplicó la propuesta de runner corporativo ni se trató su rechazo anterior como una aprobación. Las seis superficies PM inspeccionadas en este discovery (ActionController, ActionServiceImpl, PipelineHistoryServiceImpl, PipelineExecutionLogsServiceImpl, CustomAuthorizationFilter y TigerUsernameAuthentication) siguen byte por byte iguales a `origin/develop`. Esto es comprobación de fuente, no nueva certificación de auth.

### Delta ClickHouse recuperado

Desde `c8b20b65` hasta `cf17797e`: cuatro commits, 82 archivos, +5504/-231 líneas. Incluye `d0d6ef24` (política de mensajes Kafka inválidos), `668266b7` (diagnóstico sanitizado de campos inválidos), `ac4662af` (tooling/reconciliación) y `cf17797e` (refreshable materialized views). Se leyó el delta real y se delegó un discovery independiente sin permisos de escritura, Gradle ni Docker.

El stack declarado permanece Java25, Spring Boot4.1.1, SDK `rio-sdk-events:1.6.1` y ClickHouse `client-v2:0.9.6`. Son declaraciones de build leídas, todavía no resolución efectiva, bytecode ni inventario de jar del candidato F2.

Hallazgos que cambian la futura SPEC:

- MergeTree vigente despacha a `DeployTableDeployment` y `CreateTableDeploymentFlow`: publica tres `IN_PROGRESS` (schema, tabla y usuarios/grants), frente a los cuatro del camino legado que usa el snapshot. La aceptación debe documentar la secuencia productiva vigente sin inventar un progreso extra, conservando SQL, usuarios, grants y acceso físico.
- MergeTree `PROVISION` y `UPDATE` comparten reconciliación. El redeploy PM debe observar su operación real y su ALTER físico; el contrato CP literal se acredita separado si PM no lo emite.
- MV existente puede reconciliarse por `PROVISION` y modificar su query. `UPDATE` literal MV sigue ausente del dispatch y falla; no se puede equiparar automáticamente redeploy PM con ese `UPDATE`. C6 requiere separar ambos contratos antes de READY, preservar el FAILED de negocio donde aplique y comprobar ausencia de cambios físicos en ese caso.
- Tres fixes de la validación CH anterior permanecen sólo en el checkout sucio, ausentes de upstream: parámetro HTTP `format`→`default_format`, garantía de dígito/símbolo en credenciales y ownership local en memoria. Son dependencias a evaluar y probar en cambios separados; no se copiaron ni se asumieron disponibles en la base limpia.

Discovery independiente completado sin escrituras ni ejecución. Evidencia leída de `cf17797e`: `CreateTableDeploymentFlow.java:67,88,100` publica los tres progress; `ProcessDeploymentUseCase.java:126` sólo registra PROVISION/DEPROVISION para MV y su dispatch no comprueba el comando ausente. El test upstream `givenMvUpdate_throws_illegalArgument` afirma FAILED/no ejecución, sin comprobar una razón determinista. No se inventó esa razón ni se implementó UPDATE.

Actions vigentes: `ListWarehouseAction` exige `data.teamId`, acepta `data.environmentId` opcional y devuelve `data.warehouses` como lista de nombres desde el catálogo productivo WarehouseService/Properties, sin SQL. `ListSchemaAction` (`list-database`) usa `data.warehouseName`; `GetSchemasQuery.java:24` consulta `system.databases`, excluye `system`, `information_schema` e `INFORMATION_SCHEMA`, y devuelve `data.databases:[{name}]`. La futura SPEC debe acreditar catálogo vigente/correspondencia de endpoints y SQL real de list-database, sin fabricar warehouse SQL ni listas hardcodeadas. Estas actions CH no poseen locks/CAS/TTL propios; debe distinguirse ese hecho del contrato PM de actions/KVS.

La decisión A/B permanece pendiente de pruebas de paridad. `DeploymentEventController.java:96` requiere `@Valid` y `BindingResult`; envelope usa `@NotNull/@AssertTrue`, y `WebConfig.java:24` registra el RoutingFilter externo con orden1. El advice productivo distingue errores MVC. Intake estructural mínimo compartido (B) es candidato si A reconstruye MVC; no hay pruebas para declararlo elegido. Rutas CP actuales: deployments `/triggers/deployments`, actions `/events/actions/trigger`. Nunca usar MockMvc/HTTP en el runtime.

`BigQueueClientFactory.createClient` es overridable y permite estudiar un factory `@Primary` de perfil local bajo los publishers reales. Los beans lazy/qualified incluyen `deploymentResultClient`, `actionsResultClient`, `componentRuntimeStatusClient` y `connectorCleanupTriggerClient`; selección, serializer y cierre único pendientes de pruebas. BigQueueDeploymentPublisher absorbe errores de lifecycle normal y propaga rejected-result: conservar y probar el gap propio CH sin prometer recuperación.

`LocalDeploymentStateService.claimStart` reclama por deployment ID de forma atómica, descarta STARTED/COMPLETED y permite reintentar FAILED; no tiene TTL ni persistencia. Ownership local upstream es no-op; KMS local es sustituto reversible. El executor productivo usa virtual threads con propagación Meli/MDC y destroy shutdown, sin espera explícita de drenaje en su configuración. El futuro lifecycle debe probar drenaje real y esperar terminales, sin convertir shutdown en prueba de completion. La ruta on-prem usa `java.net.http.HttpClient`, aunque el build declare client-v2; compatibilidad de `format=` requiere ese cliente real y la imagen fijada.

### Runner y owner de pruebas encontrados

La autoridad de runtime sigue en PM `local/rio_e2e.py`, wrapper `local/rio-e2e.sh`; los casos físicos canónicos F1 viven en PM `src/localIntegrationTest/java/com/mercadolibre/rio/playmaker/localkafka/`, y los probes de launcher en `local/tests/test_rio_e2e_launcher.py`. CP Kafka mantiene `src/localTest` y `src/localFunctionalTest`. No se agregaron tests ejecutables a documentación.

El runner vigente tiene un único `cp_root`, owner file `cp-owner.json`, Compose project CP, readiness y restart fijo de `rio-cp-kafka`; generalizarlo a una pequeña lista/configuración N CPs es trabajo F2 autorizado pendiente de PLAN. Debe preservar defaults/CLI standalone F1, ledger/nonce/identidad de PID, señales, drain, test/stop lock, rendezvous, topología desde PM y broker/red propiedad CP Kafka. No existe aún ese cambio ni una promesa de compatibilidad probada.

### Baseline operacional leído, sin adoptar runtime

Contexto explícito `colima-rio-kafka-e2e-01a0f8e0`; daemon ID `273d8c36-e8c7-4ed6-8eb6-f12fdd7d174d`, Docker27.4.0, cuatro CPU y 6198427648 bytes de RAM (aprox.5,77GiB). Baseline: cero containers, cero volumes, tres redes estándar y 24 IDs únicos de imágenes incluyendo dangling. `docker image ls` repite un mismo ID por tags; el conteo corresponde a IDs únicos, no filas.

Redes baseline: bridge `dcf8b0beae0089205d3e0f6e1b53317f0290e656341dc443d98bb6a672e25c87`; host `7d68ac26a944efdf5656210f1e6eec9ffb06d8935b768e58f0c58dd6d800a49a`; none `36c5c478ea2f6e1444e890acc3a8e547a9c8c5e3cdcc0f80ce59ed0a273c16f5`. No red `rio-local` preexistente. Las carpetas de runtime `.local-rio-e2e` de los tres checkouts inspeccionados están ausentes; esto no constituye lease global ni autorización para otra integración concurrente.

`docker system df`: siete imágenes contabilizadas, 1,503GB; cero containers/volumes/build cache activos. Esta salida no acredita espacio libre del filesystem VM. Host `df -h`: 8,2GiB disponibles y99% de capacidad usada. Revalidar disco/RAM/exclusividad inmediatamente antes de adquirir runtime; no se inició build/pull/stack con este presupuesto. No se cambió docker context activo ni se operó ninguna VM. La VM original offline y su ledger privado quedaron intactos y su cleanup sigue NO CERTIFICADO.

Los primeros probes sandbox de socket Docker fallaron por permiso; la consulta de lectura autorizada fuera del sandbox acreditó los valores anteriores. Las salidas vacías/cero del probe fallido no se usaron como baseline. La segunda lectura GH se repitió con acceso autorizado al detectar error de red; sólo las respuestas válidas se usaron como evidencia.

### Gates y matriz de aceptación

| Gate / casos | Estado F2 | Evidencia / próximo paso |
|---|---|---|
| Bootstrap, refs y fetch | PASS de discovery | refs completas arriba; leer delta y contratos antes de SPEC |
| Autoridad de skills SDD | BLOCKED | resolver catálogo federado vs raíz exigida con el owner |
| SPEC funcional/técnica y TASKS READY por repo | BLOCKED | dependen de autoridad SDD y decisiones contractuales descritas; F1 READY no autoriza nuevas decisiones |
| C1–C6 y A1 backend | NO_EJECUTADO | ninguna API PM/evento/SQL F2 ejecutada; no hay prueba física de DB, tabla, vista, usuarios/grants o actions |
| X1 multi-CP, X2 poison, X3 restart CH, X4 resultados | NO_EJECUTADO | recuperar primero candidato y runtime propio; no reutilizar PASS F1 como aislamiento CH |
| Regresión F1/productiva/capabilities/cobertura/aislamiento F2 | NO_EJECUTADO | builds y ejecuciones nuevas pendientes; jars/conteos previos sólo acreditan su fuente histórica |
| Repeticiones vivas/recreación/reproducción independiente | NO_EJECUTADO | ninguna suite F2 iniciada; verificador no tiene permisos runtime |
| Cleanup F2 | NO_EJECUTADO | no se crearon recursos/procesos/credenciales F2; no se requiere teardown de recursos ajenos |
| Front/browser F4 | NO_EJECUTADO | fuera de este alcance backend; nunca PASS por F2 |

Artefacto de este discovery: DISPOSABLE_REPRODUCER documental. No hay PERMANENT_REGRESSION, E2E_CANDIDATE ni HARNESS_TOOLKIT_CANDIDATE nuevo en producto. Feedback reusable: discrepancia concreta del catálogo y prompt; se conserva aquí como bloqueo, sin fabricar una skill, migración o sesión de feedback. No se registra PASS parcial de F2.

### Continuación concreta

1. Resolver la autoridad de SDD mediante la respuesta del owner; cargar desde el routing aceptado las skills completas, sin volver a ejecutar bootstrap.
2. Revalidar PR heads/refs por delta y crear worktrees F2 aislados con base PM sobre PR1286, CP Kafka sobre PR86 y CH sobre `origin/develop` recuperado; registrar dependencia F1 y DEPROVISION ya integrada. No trasladar cambios ajenos.
3. Completar discovery/paridad y decisiones C1/C6/actions, dependencias físicas locales CH y versión de imagen antes de SPEC/PLAN/TASKS READY. Mantener guards PM/auth, SQL físico y semántica de negocio.
4. IMPLEMENT, freeze de commits/árbol/fuentes/jars, VERIFY independiente con probes propios y reproducción exacta, CORRECT/final gate. Adquirir una sola autoridad de runtime y serializar suites; revalidar espacio libre VM/host y memoria antes de iniciar recursos.

## Fuentes

- [[RIO E2E local]] y [[RIO E2E local — Diseño revisado]], leídos por delta; [[Descripción PR — rio-playmaker]] y [[Descripción PR — rio-controlplane-kafka]].
- Bootstrap `80-agents/skills/agents-os-bootstrap/SKILL.md`; registry `80-agents/skills/INDEX.md`; ausencia comprobada mediante búsqueda enfocada y `ls` de las dos carpetas SDD exigidas.
- Repos externos identificados desde las entidades y el pedido: `git remote -v`, `branch --show-current`, `rev-parse`, `status --short`, `worktree list --porcelain`; fetch PM develop+PR1286, CP Kafka develop+PR86 y CH develop; `git log/diff/show` de los objetos recuperados. Roots se resuelven desde entidades/checkouts indicados, no del vault.
- GitHub `gh pr view --json` de ambos PRs y `gh api` de workflow runs PM sobre HEAD exacto; comandos de lectura sin modificación remota.
- Docker `--context colima-rio-kafka-e2e-01a0f8e0` con `context inspect`, `info`, `container ls -a`, `network ls --no-trunc`, `volume ls`, `image ls -a --no-trunc` y `system df`; `df -h` host y `java_home -V` (Corretto25.0.4/21.0.6/17.0.14 instalados). Nada de estos probes equivale a readiness de aplicaciones o SQL físico.
