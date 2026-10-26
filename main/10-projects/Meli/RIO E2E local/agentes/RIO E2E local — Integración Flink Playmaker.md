---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[RIO E2E local]]"
sprint:
start: "2026-10-22"
due: "2026-10-23"
progress: 78
repo:
jira:
prs:
aliases: ["rio-e2e-local-flink-playmaker", "Integración PM + CP Flink E2E local", "F3 Flink Playmaker"]
tags:
  - kind/project
  - area/meli
  - project/rio-e2e-local
created: "2026-10-22"
updated: "2026-10-22"
entities: ["[[rio-playmaker]]", "[[rio-controlplane-flink]]", "[[ads-signals-frontend]]", "[[lore]]"]
related: ["[[CP Flink local]]", "[[RIO E2E local — SPEC F2 ClickHouse]]", "[[RIO E2E local — Diseño revisado]]"]
---

# RIO E2E local — Integración Flink Playmaker

> [!info]+ RIO E2E local — Integración Flink Playmaker
> **Área:** [[Meli]] · **Owner:** agente · **Padre:** [[RIO E2E local]] · **Estado:** `backend_review_front_blocked` · **Prioridad:** P1 (demo viernes 23/10)
> Esta nota es el planificador único: diseño, decisiones, fases, gates y despachos. Ningún plan paralelo sobrevive fuera de ella.

## 🎯 Objetivo

Demostrar el recorrido completo **APIs de Playmaker → Kafka local → CP Flink → Flink real → resultados y runtime status → estado de Playmaker**, primero por backend y después desde [[ads-signals-frontend]] con journeys verificados por [[lore]], sobre la misma VM `colima-rio` donde ya corren Kafka y ClickHouse.

Fuera de alcance: lógica de negocio de cualquier repo (`src/main` queda intacto en PM y CP Flink), UPDATE literal desde PM (PM no lo emite), GCP, fixes de bugs de develop (se reportan aparte), journeys de entidades/entity-service, generalizar `local/rio_e2e.py` a N CPs y cualquier framework E2E nuevo.

## 📊 Estado actual

- **2026-10-23 — backlog cubierto: 13 casos certificados.** Agregados `clickhouse-run-query`, `clickhouse-refreshable-view`, `kafka-clickhouse-connector` y `cross-cp-pipeline` (tópico → Flink SQL → tópico → conector → tabla en un solo deploy), todos PASS al primer intento. Certificación `rio-ecosystem all` desde cero en PM `53a3a929a`: 12 corridas Lore PASS (una por caso, con smoke), 48/48 oráculos backend, teardown 0/0. El conector usa la forma explícita (`source`/`outputs`): la forma derivada de relaciones que arma la UI no tiene productor de `cluster`/`database`/`table` en la salida del CP de MergeTree.
- **2026-10-23 — ecosistema reutilizable con un comando: 9 casos certificados.** En PM `feature/rio-e2e-local-flink` @ `4a71b5dde`: `.lore/ecosystem/rio-ecosystem` (`doctor`, `up`, `seed`, `run`, `verify`, `down`, `all`) levanta Colima, los tres CP, Playmaker, el front y Lore, siembra cada caso por API, corre una corrida Lore por caso y verifica oráculos de backend. Casos (carpeta `cases/<id>/` con escenarios, `case.json` de seed, relaciones y oráculos): smoke, kafka-topic, kafka-topic-update, clickhouse-mergetree, clickhouse-mv, flink-sql, flink-sql-invalid, flink-jar y flink-python. Certificación desde cero: 8 corridas Lore PASS, 28/28 oráculos PASS, teardown 0/0. Skills `rio-ecosystem-e2e` y `rio-ecosystem-scenario-authoring` en `.lore/ecosystem/skills/`, enlazadas desde `AGENTS.md`; runbook en `.lore/ecosystem/README.md`. Backlog del catastro: conector Kafka→ClickHouse por UI, pipeline cruzado entre CPs, acción Run Query y refreshable view.
- **2026-10-23 — escenarios de ecosistema alineados con `.lore/`.** Movidos de `local/lore/` a `.lore/ecosystem/` (`d287dd2cb`) con `environments: [ecosystem]`, fuera del `scenario_directory` de Cleric de #1327; manifiesto actualizado (`bbe14b2c8`), contrato agentic completo PASS y push. Import en Lore desde la ruta nueva OK (5/5 escenarios, proyecto `rio-e2e-ecosystem`); los journeys no se re-ejecutaron tras el movimiento.
- **2026-10-23 — rama PM sincronizada con develop.** `feature/rio-e2e-local-flink` @ `c0c4371a6` (`merge develop` sobre `ca4fe6bef`, push normal), 0 commits atrás. Conflicto único `.testing/impact.json` resuelto por unión de selectores. Gates del árbol fusionado: `test` 5184/0/3 skips heredados, `localTest` 55/0, aislamiento, contrato de repositorio y contrato agentic PASS (incluye `AT-000-S01` y `AT-180-S18` `L0-LOCAL_STACK`). Queda como único bloqueante el PR hermano de CP Flink sin mergear.
- **2026-10-23 — ramas publicadas y descripciones de PR listas.** PM `feature/rio-e2e-local-flink` @ `3cb35aaef` y CP Flink `feature/rio-e2e-local-flink-playmaker` @ `da3e33c6` pusheadas (PRs sin abrir). Descripciones: [[Descripción PR — rio-playmaker (E2E local Flink)]] y [[Descripción PR — rio-controlplane-flink (E2E local Playmaker)]]. Bloqueante de PM: base 19 commits atrás de `develop`, conflicto sólo en `.testing/impact.json`.
- **2026-10-22 — F5 completo: Lore 5/5 PASS (Claude Code).** Primer PASS de navegador certificado: `run_mvkbbsbnec16b25105`, compliance 100%, 0 failed/blocked, sobre `ads-signals-frontend` → Playmaker → Kafka → CP Flink/Kafka/ClickHouse reales. Lore sin cambios de código: binario nativo del Claude Agent SDK instalado con `--no-save` desde el registry del lockfile, Chromium vía wrapper (`--host-resolver-rules`, certificado ignorado) en `LORE_CHROMIUM_PATH`, web en 8444 por fallback automático. El agente de Lore no puede arrastrar al canvas, así que los componentes se siembran por API PM con las formas de las suites y Lore despliega y opera; el ciclo Flink se separó en `b3-flink-lifecycle` por el presupuesto de 40 llamadas por escenario. Escenarios y procedimiento en PM `local/lore/` (`3cb35aaef`). Todos los commits siguen locales, sin push. Pendiente del owner: aceptar G4/G5 y decidir push/PRs.
- **2026-10-22 — F4 completo: journeys de navegador B1–B3 PASS (Claude Code).** El front `ads-signals-frontend` sin cambios de código opera contra Playmaker y los tres CP reales: Flink SQL deploy → stop → start con jobs reales y datos transformados, tópico Kafka con RF 2 y peek, tabla MergeTree en una base creada desde la UI. Correcciones: identidad única `example` (Kraken con mocks grabados), segundo broker para RF 2 y runner SQL emulado en `src/local` del CP Flink (`da3e33c6`, sin `src/main`). Hub de PM documenta el procedimiento (`3e76158bf`). Commits locales sin push. Pendiente: F5 (Lore), que debe lanzar Chromium con el mismo `--host-resolver-rules`.
- **2026-10-22 — G4 review con journeys BLOCKED y VM limpia.** Commit local PM `471e845a2` (`Document local frontend integration`), sólo `local/RIO_E2E.md` cambió en esta sesión; contra `f1a4b246d`, 9 archivos +2011/−261 y `src/main`/`src/test` vacíos. Seed de los tres DP/staging e identidad backend PASS; hooks WebSec/DataSec PASS, Java/Checkstyle/PMD no aplican al Markdown, contrato PASS y localTest 55/0. S4.1 no obtuvo home autenticada; B1–B3 bloqueados antes de crear/deploy/acciones por fallo de autorización del front, sin causa raíz afirmada ni URL habilitada para Lore. Sol verificó 0 contenedores, 0 redes rio-*, 12 puertos libres y PM/front sin procesos propios; PM/CP Flink/front/Lore/Kafka/CH limpios. T4.4/T4.5 en review de evidencia del bloqueo, no de journeys completados.

- **2026-10-22 — S4.1/S4.4 BLOCKED; B1–B3 sin mutaciones.** Front Node 24.16 arrancó en TTY y compiló sin errores, pero `GET http://localhost:8080/data-products` terminó el proceso con `TypeError: The "path" argument must be of type string. Received function UnauthorizedView`, en `@kraken/static` → `authorizationMiddlewareFn`; no hubo status HTTP fiable. Raíz HTTP observada `Cannot GET /`; después del crash, navegación 8080 `ERR_CONNECTION_REFUSED` y HTTPS solicitado `Timeout 30000ms exceeded`. MOCK presente, tres segmentos, no expirado; no se determinó la causa del rechazo de autorización. Ninguna home autenticada ni URL lista para Lore; no se cambió host/config/código/token. Sol verificó componentes vacíos en DP 1/2/3 y JobManager sin jobs; no hay líneas BFF/example en el log seguro tras restart. Capturas diagnósticas y logs saneados sólo en el directorio temporal de sesión; T4.6 en validación, teardown en curso.

- **2026-10-22 — T4.3 review, stack listo para navegador.** PM, Kafka, ClickHouse y Flink arrancados; Sol verificó por API los tres data products y `project_code: rio-e2e-local`, environment staging (IDs DP/env 1/1, 2/2, 3/3). Identidad verificada por Sol en el mismo GET `/v2/reference/grants`: MOCK 200/dos grants; default 502 que propaga el 403 del fixture. El header debe conservar minúscula como `callLocal`; urllib lo capitalizaba y explicó la discrepancia del probe, sin PLAN_CONFLICT. Front y S4.1 delegados a Luna separado; B1–B3 aún sin resultado.

- **2026-10-22 — F4 en ejecución autónoma.** Coordinación GPT 6.1 Sol y operación GPT Luna; se inicia preflight y extracción de identidad pública en memoria, sin CA, comandos del owner ni cambios productivos. T4.3 en curso; T3.7/T4.2 permanecen validadas.

- **2026-10-22 — F4 ya no depende del owner.** El owner aclaró que las pruebas no deben requerir que ejecute comandos. Se elimina la precondición de CA devcert (T4.0 cancelada): el navegador automatizado ignora el certificado en 8443 o usa HTTP 8080, y Lore usa 8080 loopback. G4 vuelve a `pending`; F4 (T4.3–T4.6) puede ejecutarse completo por el agente.
- **2026-10-22 — T3.7 y T4.2 validados; F4 sigue bloqueado sólo por la CA.** PM `356dc49e1` (limpieza) y `2528f23d5` (token del fixture) y CP Flink `ff0e8d10` (README) revisados: cambios correctos y acotados, `localTest` 55/0 y `verifyLocalArtifactIsolation` PASS re-ejecutados sin cache. Reservas menores para el PR: `@SuppressWarnings("PMD.GodClass")` agregado al fixture y reformateo completo impuesto por hooks; un "P1/P2" residual en el hub. La primera reinstalación de la CA reinstaló la vencida desde la cache (ver T4.0).
- **2026-10-22 — T3.7 y fixture T4.2 en review; G4 blocked por CA.** Commits locales PM `356dc49e1` y `2528f23d5`, CP Flink `ff0e8d10`. Regresión PM 4927/0 fallos/2 skips heredados; locales 55/0, aislamiento PASS y cinco hooks PASS; fixture 98,1% líneas/98,5% ramas, configuración 100% líneas sin ramas. CA rc1 `Certificate will expire`; por instrucción del owner se detiene F4 antes de extraer el MOCK_TOKEN, seed, stack y navegador. T4.3–T4.6 pendientes; G0–G3 siguen accepted. Auditoría final: 0 contenedores, 0 redes rio-* y 12 puertos libres; PM/CP/front/Lore limpios.

- **2026-10-22 — DD-8 corregido; listo para T3.7 + F4.** El owner autorizó el token configurable del fixture en `src/local` de PM. El rediseño usa el `MOCK_TOKEN` público de Tiger como identidad única de front y PM, sin token real. Pendientes: T4.0 (CA, owner) antes de levantar el front, y T3.7 antes de cualquier PR. En la revisión se retiró el hallazgo sobre `KafkaE2EContext`: su cambio es necesario (`DEADLINE` y tópicos del probe) y el reformateo lo imponen los hooks sobre el archivo completo.
- **2026-10-22 — validación independiente F0–F3 (Claude Code):** G0–G3 `accepted`, G4/G5 `blocked`. CP Flink `ac019e17` aprobado sin reservas. PM `a66ae3871` aprobado con reservas: funcional y sin código productivo, pero antes de abrir PR hay que limpiar la suite, el hub y `.testing/impact.json` (T3.7). **Defecto del plan en DD-8:** `RIO_LOCAL_TIGER_TOKEN` sólo existe en el cliente de los tests; `LocalAcmeGrantsFixtureServer` fija `Bearer local-e2e` y el front necesita un JWT Tiger para resolver identidad, así que F4 no funciona sólo con variables de entorno aunque se renueve la CA. Falta decisión del owner (T4.0) además de la CA vencida.

- **2026-10-22 — G0–G3 review; G4/G5 blocked; sesión cerrada con backend completo.** CP `ac019e17d482` (ocho archivos), PM F2 `aaef4d4e6fd4` y F3 `a66ae3871db9` (seis archivos propios autorizados); protected trees vacíos contra pins. P1/P2 PASS×3; P3–P8 PASS; R1 Kafka7+CH5 PASS con JM29EMPTY. P5 caché JAR0→5→5 y P6 ZIP0→1→1, SQL/Python con asserts de datos transformados; excepción JAR DD-7 autorizada. P9 FAIL esperado: develop-gap vigente, CP COMPLETED/jobs CANCELED/output0 pero PM requested/slot running por terminal_component_run; sin fix ni rerun. Contrato final30/0/0/0 y cinco hooks PASS. Front Node24/npmci PASS, cero cambios propios; CA vencida/sudo sin privilegios bloquean navegador y Lore, sin run id ni JWT real. Máximo VM observado4,30GiB/7,74GiB fits; Sol confirmó0 contenedores/0 redes rio-* y12 puertos libres. Sin push/PR/merge; revisión independiente pendiente.

## 🧱 Entrega de desarrollo

La SPEC funcional y técnica de esta integración es esta nota (§ Diseño y § Paquetes). `$FUENTES` es la raíz externa de checkouts Meli registrada en el workspace; los originales tienen cambios de otras tareas y no se tocan.

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-controlplane-flink]] · fury_rio-controlplane-flink | `feature/rio-e2e-local-flink-playmaker` (creada en F0), worktree `$FUENTES/rio-controlplane-flink-rio-e2e-pm` | `origin/develop` @ `920a7075` | § Objetivo y matriz E2E | § Diseño DD-1, DD-2, DD-6 | G1 review; commit `ac019e17` |
| [[rio-playmaker]] · fury_rio-playmaker | `feature/rio-e2e-local-flink` (creada en F0), worktree `$FUENTES/rio-playmaker-rio-e2e-flink` | `origin/develop` @ `f1a4b246d` | § Objetivo y matriz E2E | § Diseño DD-3 a DD-5, DD-7, DD-9 | F2 review (`aaef4d4e6`); F3 review; F4 review con journeys BLOCKED |
| [[ads-signals-frontend]] · fury_ads-signals-frontend | sin rama: sólo configuración por variables de entorno; worktree detached `$FUENTES/ads-signals-frontend-rio-e2e` | `origin/develop` @ `9a70723c9` | § Journeys B1–B3 | § Diseño DD-8 | G4 review: BLOCKED por autorización del front |
| [[lore]] · lore | sin rama: herramienta de verificación | `develop` @ `e906b95` | § Journeys B1–B3 | § Diseño DD-8 | G5 blocked por G4 |
| [[rio-controlplane-kafka]] / [[rio-controlplane-clickhouse]] | sin cambios; checkouts detached de `origin/develop` para regresión | Kafka `f4b5701`, CH `4b16f7c2` | — | — | regresión en F3 |

## Diseño

### Qué falta realmente

| Requisito | Evidencia en `origin/develop` | Estado |
|---|---|---|
| PM despacha deployments `flink-sql` y `aws-flink-job` a Kafka local | PM `src/local/resources/application-local-kafka.yml` enruta ambos tipos a `BIG_QUEUE`; en perfil `local-integration` ese transporte es `LocalKafkaDeploymentTriggerProducer` → `rio-deployment-trigger-local`, key `deployment_id` | done |
| CP Flink consume deployments por Kafka | CP `src/local/.../local/LocalKafkaTriggerListener` (id `local-kafka-triggers`, group `rio-cp-flink-local`) → `LocalKafkaTriggerAdapter` → `DeploymentTriggerController.handleDeploymentTrigger` | done |
| PM publica actions por Kafka | PM `src/local/.../localkafka/LocalKafkaActionsTriggerProducer` → `rio-action-trigger-local`, key `action_id`, JSON SDK crudo | done |
| **CP Flink consume actions por Kafka** | no existe; `local/README.md` declara que las actions entran por `POST /triggers/actions` y `local/e2e.py` las manda por HTTP | **missing** |
| CP Flink publica resultados y runtime status a Kafka | `LocalKafkaBigQueueClientFactory`: `rio-deployment-result-local`, `rio-action-result-local`, `rio-component-runtime-status-local` (key `component_name`) | done |
| PM consume los tres flujos de resultado | `LocalKafkaDeploymentResultListener`, `LocalKafkaActionResultListener`, `LocalKafkaRuntimeStatusListener` (este último habilitado por `local.integration.clickhouse.enabled: true`, ya presente en `application-local-kafka.yml`) | done |
| Broker compartido | Compose del CP Kafka es dueño de `rio-kafka` en red `rio-local`; el compose Flink ya declara `rio-local` externa y `rio-kafka:19092` | partial: falta modo integrado documentado y tópicos Flink en `RIO_LOCAL_TOPICS` |
| Suite PM que entra por APIs y verifica Flink físico | no existe; patrón `PlaymakerClickHouseE2ETest` + task `localClickHouseIntegrationTest` | **missing** |
| Front local y Lore | front configurable por env; Lore sin PASS de navegador (corrida 14/10 BLOCKED) | **missing** |

### Arquitectura objetivo

```text
host (macOS, 24 GiB)                                   VM colima-rio (4 CPU / 8 GiB) · red rio-local
───────────────────────────                            ─────────────────────────────────────────────────────────
Lore (Node 24, otro puerto) ──► ads-signals-frontend    rio-kafka (compose CP Kafka) 19092 / 127.0.0.1:39092
                                 https :8443               ├─ rio-deployment-trigger-local ──┬─► CP Kafka      39081
                                   │ x-tiger-token          │                                 ├─► CP ClickHouse 39082
                                   ▼                        │                                 └─► CP Flink      39083
                               Playmaker :39080 ───────────►├─ rio-action-trigger-local ──────┬─► CP Kafka
                               (perfiles local,             │                                 ├─► CP ClickHouse
                                local-integration,          │                                 └─► CP Flink [NEW intake]
                                local-kafka)                ├─ rio-deployment-result-local ◄──── los tres CP
                                   ▲                        ├─ rio-action-result-local ◄───────── los tres CP
                                   └── listeners PM ◄───────└─ rio-component-runtime-status-local ◄ CP Flink (POLL 60 s)
                                                          CP Flink ──► SQL Gateway 39183 / JobManager 39184 / TaskManager
                                                                       nexus-local (stub JAR/ZIP)
                                                          MySQL PM 33306 · ACME fixture 18081 (host, embebido en PM)

[NEW]      CP Flink: rama de actions en el intake Kafka local; DLT rio-action-trigger-local-dlt-flink
[MODIFIED] CP Flink: local/e2e.py publica actions por Kafka; README con modo integrado
[NEW]      PM: PlaymakerFlinkE2ETest (@Tag flink) + task localFlinkIntegrationTest
[MODIFIED] PM: local/RIO_E2E.md con stack completo de tres CP y lista de tópicos
```

### Decisiones de diseño

- **DD-1 — Intake de actions en CP Flink = mismo listener, segunda rama.** `LocalKafkaTriggerListener` se suscribe también a `${local.kafka.action-trigger-topic}`; `LocalKafkaTriggerAdapter` enruta por tópico: deployments como hoy, actions envolviendo el JSON crudo en `{"publish_time":0,"msg":...}`, binding a `BigQueueMessage<ActionTriggerMessage>` y llamada directa a `ActionTriggerController.handleActionTrigger`. Es exactamente el patrón de los CP Kafka y ClickHouse. Mismo listener id ⇒ `LocalKafkaReadiness` cubre ambos tópicos sin cambios. Mismo group `rio-cp-flink-local`; cada CP lee todos los triggers y el controller productivo filtra por `rio.supported-component-types` (`flink-sql`, `aws-flink-job`), devolviendo 200 para tipos ajenos ⇒ offset confirmado como no-op. Cero cambios en `src/main`.
- **DD-2 — Semántica de ACK y DLT de actions = la de deployments.** `AckMode.RECORD`, auto-commit apagado, `max.poll.records=1`, `FixedBackOff(1000 ms, 2)`, `PoisonPayloadException` sin reintento (256 KiB, UTF-8 estricto, un objeto JSON, sin `msg`), DLT `rio-action-trigger-local-dlt-flink` con ack de 15 s. El controller productivo es asíncrono (`CompletableFuture.runAsync`): el commit marca aceptación, no término. El término se observa en `rio-action-result-local` y en `GET /v2/actions/{id}`.
- **DD-3 — PM no cambia código de producción; `src/local` sólo para el token del fixture ACME (DD-8).** El enrutamiento `BIG_QUEUE` de los tipos Flink, el productor de actions y los tres listeners de resultados ya existen en develop. El flag `local.integration.clickhouse.enabled` gobierna también el runtime status de Flink; renombrarlo no aporta a la demo (YAGNI) y se documenta en el hub. La única excepción en `src/local` es la de DD-8, autorizada por el owner el 2026-10-22.
- **DD-4 — Redeploy desde PM = PROVISION.** `DispatchRequestFactory.build` y `DeploymentServiceImpl` fijan `DeploymentOperation.PROVISION`. Sobre una app RUNNING, el CP la deriva a STOP_TO_UPDATE → update → start y reemplaza job IDs sin duplicarlos (comportamiento de develop, igual que KDA). La suite lo verifica así y nunca lo presenta como UPDATE literal; UPDATE literal sigue siendo capacidad standalone del CP (`local/e2e.py`).
- **DD-5 — Undeploy = `develop-gap` hasta probar lo contrario.** Los casos de DEPROVISION vía PM se etiquetan `develop-gap` y quedan fuera de la task por defecto. F3 los ejecuta una vez sobre `f1a4b246d` y reporta en una línea separada si el descarte por `already_terminal`/`terminal_component_run` persiste. No se corrige.
- **DD-6 — Broker único, modo integrado del CP Flink.** En integración no se usa el `docker run` manual del README Flink (su contenedor colisiona en nombre con el broker del compose Kafka). El broker lo levanta el compose del CP Kafka; el compose Flink se une a `rio-local` como ya declara. Tópicos agregados a `RIO_LOCAL_TOPICS`: `rio-deployment-trigger-local-dlt-flink`, `rio-action-trigger-local-dlt-flink`, `rio-flink-input-local`, `rio-flink-output-local`.
- **DD-7 — Oráculo físico Flink en la suite PM.** Excepción P5 autorizada por el owner el 22/10: TopSpeedWindowing se verifica por job real RUNNING, stop/start con reemplazo de IDs y caché Nexus; no publica Kafka y no se cambia el artefacto. SQL/Python conservan datos transformados en Kafka. Cada caso restante cruza cuatro capas: estado PM (deployment/pipeline/action COMPLETED o FAILED y `GET /data-products/{dp}/environments/{env}/services` para runtime), eventos (trigger y resultado con la key correcta, observer `assign()` sin group), Flink real (JobManager REST `127.0.0.1:39184/jobs/overview` y `/jobs/{id}`) y datos (filas producidas en `rio-flink-input-local` aparecen transformadas en `rio-flink-output-local`). HTTP 202 o ACK Kafka nunca cuentan como término.
- **DD-8 — Identidad local única = `MOCK_TOKEN` de la librería Tiger.** Con `USE_TIGER_MOCK=silent`, `TigerTokenValidation` de `tiger-java-helper` 2.3.0 ignora el token recibido y resuelve siempre los claims de su constante pública `Constants.MOCK_TOKEN` (usuario `example`, identidad `mrn:seginf:ad:user/example`), que es exactamente la identidad que espera `LocalAcmeGrantsFixtureServer`. El único acople es que `AcmeClientImpl` reenvía el header `x-tiger-token` entrante y el fixture lo compara contra un literal. Por eso: (1) el fixture lee el header esperado de `RIO_LOCAL_TIGER_TOKEN`, la misma variable que ya usa el cliente de los tests, con default `Bearer local-e2e` y rechazo de valor vacío al arrancar; (2) el front corre con `TIGER_DEV_TOKEN=<MOCK_TOKEN>` y PM con `RIO_LOCAL_TIGER_TOKEN="Bearer <MOCK_TOKEN>"`, de modo que front y PM ven el mismo usuario `example`. El valor se extrae en runtime de la clase `com.mercadolibre.tiger.java.helper.utils.Constants` del jar en la cache de Gradle; no se copia a archivos versionados ni al vault. No se usa ningún token real. Front sin código: `PLAYMAKER_BASE_URL=http://localhost:39080` (activa `callLocal` y el header en minúscula), sin depender de la CA devcert ni de ningún comando del owner: el navegador automatizado de F4 entra por `https://dev.mercadolibre.com.ar:8443` ignorando errores de certificado, o por `http://localhost:8080`; Lore (que no ignora certificados) usa `http://localhost:8080`, loopback. Los data products de los journeys se crean por API de PM con `project_code: rio-e2e-local` porque Puma local apunta a `127.0.0.1:9`. Lore corre en otro puerto que el front, con sesión de prueba `Services-Backoffice-Token=<MOCK_TOKEN>` sobre el host loopback del front. **Ajuste verificado 2026-10-22:** el front autoriza vía Kraken, así que corre con los mocks grabados del repo (`mocks/test` copiado a `mocks/development`, gitignored, más un registro de usuario Kraken para `example`) y `NODE_CONFIG` con `mocksEnabled` y la app Kraken `signals-rio`; se sirve como `https://local.adminml.com:8443` (cookie `.adminml.com` y lookup LDAP de Kraken) resuelto sólo en el navegador con `--host-resolver-rules`, certificado ignorado y user agent de Chrome. El formulario de tópicos exige RF ≥ 2, por lo que el journey Kafka suma un segundo broker sólo-broker al clúster KRaft (`rio-kafka-2`). Un `flink-sql` creado desde el front nombra el runner productivo `rio-flink-sql` 1.0.3: el stub Nexus del CP Flink sirve un placeholder y `src/local` ejecuta los archivos SQL por el SQL Gateway, que hace de runner.
- **DD-9 — Escenarios Lore de ecosistema en PM `.lore/ecosystem/`.** Siguen la convención `.lore/` de la suite propia de Playmaker ([#1327](https://github.com/melisource/fury_rio-playmaker/pull/1327)) pero quedan fuera de `.lore/scenarios/`, el `scenario_directory` que inventaría el gate Cleric, porque necesitan el ecosistema completo; cada escenario declara `environments: [ecosystem]` y corre en el proyecto Lore `rio-e2e-ecosystem`. Los journeys de demo terminan antes de inactivar mientras DD-5 siga en `develop-gap`.

### Contratos que se usan (sin cambios)

| Flujo | Tópico | Key | Productor → consumidor | DLT |
|---|---|---|---|---|
| Deployment trigger | `rio-deployment-trigger-local` | `deployment_id` | PM → CP Kafka, CH, Flink | `-dlt-kafka`, `-dlt-clickhouse`, `-dlt-flink` |
| Action trigger | `rio-action-trigger-local` | `action_id` | PM → CP Kafka, CH, Flink | `-dlt-kafka`, `-dlt-clickhouse`, `-dlt-flink` [NEW] |
| Deployment result | `rio-deployment-result-local` | `deployment_id` | CP → PM | `rio-deployment-result-local-dlt` |
| Action result | `rio-action-result-local` | `action_id` | CP → PM | `rio-action-result-local-dlt` |
| Runtime status | `rio-component-runtime-status-local` | `component_name` | CP Flink → PM | `rio-component-runtime-status-local-dlt` |

APIs PM que ejercita la suite (`{slot}` = `/data-products/{dp}/components/{c}/environments/{env}`): `POST /data-products`, `POST /data-products/{dp}/environments`, `POST /data-products/{dp}/components`, `POST .../components/{c}/definitions`; deploy por pipeline (`GET /data-products/{name}/environments/{env}/pipeline`, `POST .../pipeline/deploy`, `GET .../pipeline/history/{execution}`) y directo (`POST {slot}/deployments` con `definition_id`); actions `POST {slot}/actions/{start|stop}` con `{"data":{"flink_app_name":...}}` (más `snapshotOption` en start y `forceStop` en stop, como envía el front) y polling `GET /v2/actions/{id}`; undeploy `DELETE {slot}/deployments/{id}` (`develop-gap`). `start`/`stop` exigen `DEV_AND_UP` por familia `flink-sql`/`flink-job`; `flink-job` y `aws-flink-sql` están en `unsupported-action-component-types`, así que la suite usa los tipos concretos `flink-sql` y `aws-flink-job`.

### Matriz E2E

| ID | Entrada por PM | Oráculo | Fase | Resultado verificado |
|---|---|---|---|---|
| P1 SQL vertical | deploy `flink-sql` con dos INSERT | PROVISION COMPLETED en PM; dos jobs RUNNING; filas transformadas en `rio-flink-output-local`; runtime RUNNING en services | F2 | PASS ×3 |
| P2 stop/start | action `stop` y luego `start` | action COMPLETED en PM; jobs CANCELED y luego RUNNING con IDs nuevos; runtime READY → RUNNING por POLL sin falso FAILED (#214) | F2 | PASS ×3 |
| P3 redeploy | nuevo definition + deploy | PROVISION (no UPDATE); STOP_TO_UPDATE → update → start; job IDs reemplazados sin duplicados; datos siguen fluyendo | F3 | PASS |
| P4 SQL inválido | deploy con SQL roto | PM FAILED con causa del CP; ningún job RUNNING | F3 | PASS |
| P5 JAR | deploy `aws-flink-job` con JAR del stub Nexus + stop/start | COMPLETED; job TopSpeedWindowing RUNNING; cache hit en el access log del stub | F3 | PASS; JAR5→5 |
| P6 Python | deploy `aws-flink-job` con ZIP `py-upper` + stop/start | COMPLETED; job RUNNING; UDF transforma datos | F3 | PASS; ZIP1→1 |
| P7 tipo no soportado | action sobre `aws-flink-sql` | rechazo de PM antes del wire; nada en `rio-action-trigger-local` | F3 | PASS |
| P8 poison action | bytes inválidos en `rio-action-trigger-local` | DLT `-dlt-flink` conserva bytes/key; consumidor sigue sano | F1 (CP) | PASS |
| P9 undeploy | `DELETE {slot}/deployments/{id}` | `develop-gap`: reporte separado vigente/no vigente | F3 | FAIL esperado; develop-gap vigente |
| R1 regresión | suites Kafka (`localIntegrationTest`) y ClickHouse (`localClickHouseIntegrationTest`) con Flink vivo | sin fallas nuevas; ningún CP procesa tipos ajenos | F3 | PASS; Kafka7 + CH5 |
| B1–B3 | journeys de navegador Kafka, ClickHouse, Flink | ver F5 | F4–F5 | BLOCKED; CA/trust, sin ejecución |

### Capacidad de la VM

Límites declarados: compose Kafka ~1,5 GiB (broker 768 MiB, CP 512 MiB, init 256 MiB que termina), CH ~1,8 GiB (motor 1 GiB, CP 768 MiB, proxy nginx), Flink 5,7 GiB (JM 1400, TM 1800, SQL Gateway 1400, CP 1200, nexus 64 MiB), más MySQL. La suma de límites (~9–9,5 GiB) supera los 8 GiB de la VM, pero son topes, no consumo; lo medido del stack Kafka fue ~500 MB. F0 mide el consumo real con todo arriba. Si el pico supera 7 GiB, redimensionar `colima-rio` a 12 GiB (host de 24 GiB) es un punto de control del owner (cambia la VM compartida); mientras tanto la regresión CH y la demo Flink se ejecutan en serie.

## Plan de implementación

### Roadmap

| Fase | Resultado | Carga relativa | Depende de |
|---|---|---|---|
| F0 | Bases, worktrees, preflight y medición de capacidad | baja | — |
| F1 | CP Flink consume actions por Kafka; modo integrado documentado | media (código + tests) | G0 |
| F2 | Vertical PM → Flink SQL → datos → stop/start → estado PM | alta (stack completo) | G1 |
| F3 | Matriz completa, `develop-gap` y regresión Kafka/CH | alta (física) | G2 |
| F4 | Front local contra PM con los tres CP | media (identidad y datos) | G2 |
| F5 | Lore: smoke, journeys B1–B3 y ensayo de demo desde arranque limpio | media | G4 |

F3 y F4 son independientes en código y pueden prepararse en paralelo, pero comparten la VM: nunca dos suites ni una suite y una sesión de navegador al mismo tiempo sobre el mismo stack.

### Paquete autónomo Fase 0 — Bases y preflight

**Misión exacta** — Dejar dos worktrees limpios sobre develop fresco con sus ramas, un worktree detached del front, un baseline de la VM y la medición de memoria con los tres CP arriba; no escribir código.

**Precondiciones verificables** — GlobalProtect conectado (fetch a `melisource` sin rechazo de allowlist); `DOCKER_CONTEXT=colima-rio` responde; cero contenedores y cero redes `rio-*` de otra sesión (si existen, STOP sin tocarlos).

**Lectura obligatoria** — esta nota (§ Entrega de desarrollo, § Diseño DD-6, § Capacidad de la VM); `VAULT_ROOT/10-projects/Meli/RIO E2E local/CP Flink local.md` (§ Próxima sesión); PM `local/RIO_E2E.md` (§ ClickHouse integration with a manual stack); CP Flink `local/README.md`.

**Decisiones** — Ramas y bases de la tabla de entrega; originales intactos; DD-6 (broker del compose Kafka).

**Implementación paso a paso** — T0.1 fetch y worktrees; T0.2 baseline VM; T0.3 levantar stack completo sin PM (compose Kafka con `RIO_LOCAL_TOPICS` extendida, MySQL, compose CH, compose Flink con `localBootJar` de develop) y medir `docker stats` en reposo y con un job SQL standalone; T0.4 teardown propio y verificación de baseline.

**Archivos esperados** — ninguno en repos; evidencia en el directorio temporal de la sesión y resumen en § Bitácora.

**No tocar** — checkouts originales (`rio-controlplane-flink`, `rio-playmaker`, `rio-controlplane-kafka`, `rio-controlplane-clickhouse`, `ads-signals-frontend`); configuración de la VM (redimensionar es punto de control del owner).

**Spikes permitidos** — S0.1: confirmar si `FlinkControlPlaneClientImplLocal` (stub de PM para `ServiceActionsServiceImpl`) queda activo con los perfiles `local,local-integration,local-kafka`; sólo lectura, resultado una línea en la bitácora para F4.

**Tests y asserts** — `git rev-parse` de cada worktree igual a la base de la tabla; `git status --porcelain` vacío; readiness 200 de CP Kafka, CH y Flink; pico de memoria registrado por contenedor.

**Entregables/Gate G0** — tabla de SHAs y worktrees, pico de memoria con veredicto `fits` (≤ 7 GiB) o `needs_owner_resize`, baseline restaurado (0 contenedores/redes `rio-*` propios).

**Handoff** — F1 recibe el worktree CP Flink en su rama y la lista de tópicos integrada; no rediscute bases ni broker.

### Paquete autónomo Fase 1 — CP Flink: actions por Kafka

**Misión exacta** — Agregar la rama de actions al intake Kafka local del CP Flink según DD-1/DD-2, pasar `local/e2e.py` a publicar actions por Kafka y documentar el modo integrado, sin tocar `src/main`.

**Precondiciones verificables** — G0 `accepted`; worktree `rio-controlplane-flink-rio-e2e-pm` en `feature/rio-e2e-local-flink-playmaker` limpio.

**Lectura obligatoria** — § Diseño DD-1, DD-2, DD-6 y matriz P8; CP Flink `src/local/java/com/mercadolibre/rio/controlplaneflink/local/` (`LocalKafkaTriggerListener`, `LocalKafkaTriggerAdapter`, `LocalKafkaTriggerConfiguration`, `LocalKafkaReadiness`), `src/local/resources/application-local-kafka.yml`, `src/main/java/com/mercadolibre/rio/controlplaneflink/controller/ActionTriggerController.java`, `local/e2e.py` (función `action`), `local/README.md`; patrón de referencia CP Kafka `src/local/java/com/mercadolibre/rio_controlplane_kafka/local/LocalKafkaTriggerAdapter.java`. Contexto: `VAULT_ROOT/10-projects/Meli/RIO E2E local/CP Flink local.md`.

**Decisiones** — DD-1, DD-2, DD-6 cerradas; group `rio-cp-flink-local`; DLT `rio-action-trigger-local-dlt-flink`; claves nuevas `local.kafka.action-trigger-topic` y `local.kafka.action-trigger-dlt-topic`.

**Implementación paso a paso** — T1.1 config y listener; T1.2 adapter con rama de actions y DLT; T1.3 tests locales; T1.4 `e2e.py` por Kafka; T1.5 README modo integrado; T1.6 E2E standalone completo y gates.

**Archivos esperados** — modify: `LocalKafkaTriggerListener.java`, `LocalKafkaTriggerAdapter.java`, `LocalKafkaTriggerConfiguration.java`, `application-local-kafka.yml`, `local/e2e.py`, `local/README.md`; create o modify en `src/localTest`: tests del adapter/listener para actions. Condicional: `LocalKafkaReadiness` sólo si el listener id deja de ser único (no debería).

**No tocar** — `src/main`, `src/test`, `build.gradle` productivo, `Dockerfile` productivo, compose salvo variables de tópicos; ningún cambio a `ActionProcessor` ni a #214.

**Spikes permitidos** — ninguno; si el binding de `BigQueueMessage<ActionTriggerMessage>` no funciona con el wrapper usado en deployments, `PLAN_CONFLICT`.

**Tests y asserts** — action `flink-sql` válida invoca el controller con `action_id`, `action_name`, `component_template` y `data.flink_app_name` intactos; tipo ajeno (`clickhouse-mergetree`) → 200 y commit sin efecto; poison (> 256 KiB, UTF-8 inválido, JSON con `msg`, dos objetos) → DLT sin reintento conservando bytes y key; non-2xx → 3 intentos y DLT; deployments siguen pasando por su rama (regresión). Cobertura ≥ 95 % líneas y ramas del código local tocado, priorizando los casos críticos anteriores. `./gradlew test` productivo sin cambios en conteo (1966) y `localTest` verde.

**Entregables/Gate G1** — diff limitado a la lista de archivos; `git diff origin/develop -- src/main src/test` vacío; `localTest` + productivos verdes; `local/e2e.py` completo PASS (SQL, UPDATE, CRUD, JAR, Python, stop/start) con actions por Kafka; cleanup 0/0. Commit local en la rama; push y PR sólo con autorización del owner.

**Handoff** — F2 recibe `local-application.jar` del CP con intake de actions y la lista de tópicos/DLT; no reabre DD-1/DD-2.

### Paquete autónomo Fase 2 — PM: vertical Flink SQL

**Misión exacta** — Crear la suite PM `@Tag("flink")` y su task Gradle, y probar P1 y P2 entrando sólo por APIs de PM con el stack completo vivo.

**Precondiciones verificables** — G1 `accepted`; worktree `rio-playmaker-rio-e2e-flink` en `feature/rio-e2e-local-flink` limpio; VM sin stack ajeno.

**Lectura obligatoria** — § Diseño DD-3, DD-4, DD-7, § Contratos y matriz P1–P2; PM `src/localIntegrationTest/java/com/mercadolibre/rio/playmaker/localkafka/` (`PlaymakerClickHouseE2ETest`, `KafkaE2EContext`, `KafkaProbe`, `KafkaEventAssertions`, `PlaymakerApi`, `PlaymakerFixtures`), `build.gradle` (task `localClickHouseIntegrationTest`), `local/RIO_E2E.md`; CP Flink `local/e2e.py` (SQL de los dos INSERT, nombres de tópicos de datos y parámetros del definition). Contexto: `VAULT_ROOT/10-projects/Meli/RIO E2E local/RIO E2E local — SPEC F2 ClickHouse.md`.

**Decisiones** — DD-3 (sin cambios fuera de tests/build/docs locales), DD-7 (cuatro capas de oráculo), tipos concretos `flink-sql`/`aws-flink-job`, `project_code: rio-e2e-local`.

**Implementación paso a paso** — T2.1 task Gradle y exclusión del tag en `localIntegrationTest`; T2.2 helper JobManager REST y constantes Flink en el contexto E2E; T2.3 P1; T2.4 P2; T2.5 hub `local/RIO_E2E.md` con stack de tres CP; T2.6 corrida física dos veces seguidas y una sobre stack recreado.

**Archivos esperados** — create: `src/localIntegrationTest/java/com/mercadolibre/rio/playmaker/localkafka/PlaymakerFlinkE2ETest.java`, `.../localkafka/FlinkJobManagerClient.java`; modify: `build.gradle` (task `localFlinkIntegrationTest` con `includeTags 'flink'`, `excludeTags 'develop-gap'`; `localIntegrationTest` excluye `flink`), `KafkaE2EContext.java` (group `rio-cp-flink-local` Stable y readiness 39083 sólo en la suite Flink), `local/RIO_E2E.md`; excepción aprobada por el owner el 22/10: modify `.testing/impact.json` para contrato obligatorio, manteniendo máximo diez archivos PM y eliminando la opción de seed script.

**No tocar** — `src/main`, `src/test`, `src/local` (DD-3), `local/rio_e2e.py`, suites Kafka/CH existentes salvo el filtro de tags.

**Spikes permitidos** — S2.1: si el definition `flink-sql` requiere campos que `e2e.py` no muestra, leerlos de `DeploymentTriggerMapper` del CP; si exige lógica nueva en PM, `PLAN_CONFLICT`.

**Tests y asserts** — P1: pipeline COMPLETED, PROVISION observado con key `deployment_id`, resultado COMPLETED, dos jobs RUNNING, N filas de entrada → N filas transformadas, services RUNNING. P2: `stop` 202 + `action_id`, trigger en `rio-action-trigger-local` con key `action_id`, resultado COMPLETED, jobs CANCELED, runtime READY sin FAILED; `start` análogo con jobs RUNNING de IDs nuevos y datos fluyendo de nuevo. Fallo de cualquier capa = FAIL aunque PM diga COMPLETED.

**Entregables/Gate G2** — `localFlinkIntegrationTest` P1–P2 PASS tres veces (dos en vivo, una recreada); `./gradlew test localTest` sin regresión; diff acotado; cleanup propio; hub actualizado. Este gate habilita en paralelo F3 y F4.

**Handoff** — F3 recibe suite y helpers para extender; F4 recibe el comando de arranque del stack completo desde el hub.

### Paquete autónomo Fase 3 — Matriz completa y regresión

**Misión exacta** — Extender la suite con P3–P7 y P9, ejecutar la regresión Kafka y ClickHouse con Flink vivo y reportar el estado vigente del `develop-gap`.

**Precondiciones verificables** — G2 `accepted`; ninguna sesión de F4/F5 usando la VM durante las corridas.

**Lectura obligatoria** — § Diseño DD-4, DD-5, matriz P3–P9 y R1; suite y helpers creados en F2; CP Flink `local/e2e.py` (casos JAR TopSpeedWindowing, Python `py-upper`, SQL inválido); PM `application.yml` (`action-authorization`). Contexto: `VAULT_ROOT/10-projects/Meli/RIO E2E local/CP Flink local.md` (comportamientos de develop observables).

**Decisiones** — DD-4 (redeploy = PROVISION), DD-5 (undeploy `develop-gap`), sin fixes de develop.

**Implementación paso a paso** — T3.1 P3 y P4; T3.2 P5 y P6; T3.3 P7; T3.4 P9 con tag `develop-gap` y corrida aislada; T3.5 regresión `localIntegrationTest` y `localClickHouseIntegrationTest` con el compose Flink arriba (o en serie si G0 dio `needs_owner_resize` sin redimensión aprobada); T3.6 consolidar resultados.

**Archivos esperados** — modify: `PlaymakerFlinkE2ETest.java`, `local/RIO_E2E.md` (matriz y gap).

**No tocar** — `src/main`, `src/test`, `src/local` de PM; todo el repo CP Flink salvo `PLAN_CONFLICT` aceptado por el owner.

**Spikes permitidos** — S3.1: si P5/P6 requieren el stub Nexus con una ruta que PM no puede expresar en el definition, documentar BLOCKED con la evidencia; no adaptar el CP.

**Tests y asserts** — P3: un único PROVISION, job IDs reemplazados y conteo de jobs igual al previo; P4: FAILED con causa, cero jobs RUNNING; P5/P6: COMPLETED, job RUNNING, stop/start y cache hit; P7: 4xx de PM y ningún registro nuevo en el tópico; P9: veredicto `develop-gap vigente` o `no vigente` con eventos y estado PM; R1: mismos conteos que en develop y cero triggers procesados por el CP equivocado.

**Entregables/Gate G3** — matriz con PASS/FAIL/BLOCKED por caso y evidencia, reporte del gap en línea separada, regresión verde, cleanup propio.

**Handoff** — Owner recibe la matriz para decidir push/PR; F5 recibe confirmación de si los journeys pueden incluir inactivar.

### Paquete autónomo Fase 4 — Front local contra PM

**Misión exacta** — Hacer configurable el token del fixture ACME de PM según DD-8, levantar `ads-signals-frontend` sin cambios de código contra el stack completo con la identidad `MOCK_TOKEN`, y completar en un navegador automatizado los journeys B1–B3 hasta su último paso de demo, cada uno contrastado con backend.

**Precondiciones verificables** — G2 `accepted`; Node 24; worktree del front detached en `9a70723c9` con `npm ci` hecho (T4.1). Ninguna acción del owner: no se requiere CA de confianza ni sudo.

**Lectura obligatoria** — § Diseño DD-3, DD-8 y DD-9; PM `src/local/java/com/mercadolibre/rio/playmaker/localkafka/LocalAcmeGrantsFixtureServer.java` (constante `TOKEN`, método `responseStatus`), `LocalKafkaAdaptersConfiguration.java` (bean `localAcmeGrantsFixtureServer`), `src/localTest/java/com/mercadolibre/rio/playmaker/localkafka/LocalAcmeGrantsFixtureServerTest.java`, `src/main/java/com/mercadolibre/rio/playmaker/restclient/impl/AcmeClientImpl.java` (reenvío de headers); front `config/default-development.js`, `api/lib/playmaker.ts` (`callLocal`), `api/lib/tigerToken.ts`, `api/lib/resolveUserId.ts`, `app/server/index.ts` (bootstrap del cookie), `config/default.js` (`playmaker_component_templates`), `src/technologies/_base/flinkLifecycle.ts`. Contexto: `VAULT_ROOT/10-projects/Meli/RIO E2E local/RIO E2E local — Diseño revisado.md` (D4 y journeys).

**Decisiones** — DD-8 (token del fixture configurable por `RIO_LOCAL_TIGER_TOKEN`, identidad `MOCK_TOKEN`, sin token real), DD-3 (única excepción en `src/local`), entity-service fuera de alcance, front servido en 8080 (HTTP) y 8443 (HTTPS sin trust).

**Implementación paso a paso** — T4.2 fixture configurable con tests y arranque con `MOCK_TOKEN`; T4.3 seed de data products por API PM; T4.4 B3 Flink; T4.5 B1 Kafka y B2 ClickHouse; T4.6 sección front en el hub y commit.

**Archivos esperados** — modify PM: `LocalAcmeGrantsFixtureServer.java` (token por constructor, validación de no vacío), `LocalKafkaAdaptersConfiguration.java` (`@Value("${RIO_LOCAL_TIGER_TOKEN:Bearer local-e2e}")`), `LocalAcmeGrantsFixtureServerTest.java`, `local/RIO_E2E.md` (sección front). Front y Lore sin archivos versionados. Evidencia (capturas, requests) sólo en el directorio temporal de la sesión.

**No tocar** — `src/main`/`src/test` de PM, el resto de `src/local`, código del front y su checkout original, la identidad y los grants del fixture (`IDENTITY`, `TEAM`, proyectos), `KafkaE2EContext`.

**Spikes permitidos** — S4.1: si `http://localhost:8080` redirige a HTTPS o el login rechaza HTTP, usar `https://dev.mercadolibre.com.ar:8443` con el navegador ignorando errores de certificado y registrar el resultado para F5 (Lore necesita una de las dos vías sin trust; si ninguna sirve, BLOCKED con evidencia, sin pedir sudo). S4.2: si crear un componente desde el front devuelve 400/404 por template ULID o por `GET /v2/reference/component-types`, BLOCKED con el request exacto; sembrar templates exige `PLAN_CONFLICT`. S4.3: si un panel de entity-service impide completar el create, BLOCKED con evidencia. S4.4: si el bootstrap del front no acepta el `MOCK_TOKEN` (expiración o formato), BLOCKED con el log; no usar un token real sin autorización del owner.

**Tests y asserts** — fixture: el default sigue aceptando `Bearer local-e2e`; con token configurado acepta exactamente ese valor y rechaza `Bearer local-e2e` con 403; valor vacío o en blanco falla al construir; rutas y grants sin cambios. `./gradlew localTest verifyLocalArtifactIsolation` y la regresión `test` sin fallos nuevos. Journeys: cada paso verificado también por backend (componente en PM, trigger en el tópico, efecto físico: job RUNNING, tabla CH o tópico Kafka); pantalla sin error y estado final visible.

**Entregables/Gate G4** — commit local PM con el fixture y la sección front; capturas por paso de B1–B3; request/response de cualquier BLOCKED; comando de arranque del front reproducible desde el hub.

**Handoff** — F5 recibe host/puerto del front, el procedimiento de seed y de extracción del `MOCK_TOKEN`, y la lista de pasos por journey que pasaron.

### Paquete autónomo Fase 5 — Lore y ensayo de demo

**Misión exacta** — Obtener el primer PASS de navegador con Lore sobre B1–B3 y ensayar la demo completa desde un arranque limpio.

**Precondiciones verificables** — G4 `accepted`; Node 24; `npx playwright install chromium` hecho; puerto de Lore distinto al del front.

**Lectura obligatoria** — § Diseño DD-8, DD-9 y matriz B1–B3; Lore `docs/scenario-format.md`, `services/runner/claudeAgentDriver.ts`, `services/runner/browserSession.ts`, `scripts/dev-all.mjs`; nota `VAULT_ROOT/30-resources/applications/lore.md`; corrida bloqueada previa en `VAULT_ROOT/10-projects/Meli/RIO E2E local/RIO E2E local.md` (entrada 2026-10-14 verificación navegador).

**Decisiones** — DD-9 (escenarios en PM `local/lore/`), journeys terminan antes de inactivar salvo que G3 diga `develop-gap no vigente`; `blocked` de Lore nunca se cuenta como falla de la app.

**Implementación paso a paso** — T5.1 smoke: Lore arranca, SDK y Chromium navegan al front por HTTPS y abren la home autenticada; T5.2 escenarios B1–B3 en Markdown; T5.3 proyecto y entorno Lore con sesión de prueba; T5.4 corrida B1–B3 con reporte; T5.5 ensayo desde VM limpia siguiendo el hub al pie de la letra, Lore otra vez y teardown.

**Archivos esperados** — create: PM `local/lore/scenarios/b1-kafka.md`, `b2-clickhouse.md`, `b3-flink.md`, `local/lore/README.md`; modify: PM `local/RIO_E2E.md` (sección demo).

**No tocar** — código de Lore y del front; la sesión de prueba nunca se persiste en archivos.

**Spikes permitidos** — S5.1: configurar el puerto web de Lore por su config o variables existentes; si exige código, correr el front en otro host/puerto en lugar de tocar Lore. S5.2: si falta el binario del Claude Agent SDK para darwin-arm64 (causa del bloqueo del 14/10), reinstalar dependencias de Lore con Node 24; si persiste, BLOCKED con la traza.

**Tests y asserts** — smoke PASS; B1–B3 `passed` con captura y URL por paso; cada journey contrastado con la comprobación física de backend del mismo recurso; ensayo limpio sin intervención manual fuera del guion.

**Entregables/Gate G5** — run id de Lore y reporte, compliance de B1–B3, evidencia física cruzada, tiempo total del arranque limpio, cleanup propio.

**Handoff** — Owner recibe guion de demo verificado y estado de la VM; push/PR/merge quedan como decisiones suyas.

### Control de gates

| Gate | Estado | Responsabilidad del agente de fase | Evidencia de aceptación del owner | Habilita |
|---|---|---|---|---|
| G0 | accepted | Cinco pins y worktrees limpios; readiness tres CP; dos jobs SQL RUNNING y seis filas UPPER; VM usada 3,84 GiB, contenedores pico observado 3,32 GiB (`fits`); cleanup 0/0, nueve puertos libres | Validación 22/10 (Claude Code): pins y cleanup coherentes con la bitácora | F1 |
| G1 | accepted | `ac019e17`: ocho archivos; 1966 productivos y 85 locales PASS, coverage 100%, cinco hooks PASS; P8 bytes/key y E2E standalone completo PASS; cleanup 0/0 | Validación 22/10: diff de 8 archivos sin `src/main`/`src/test`; `test localTest` re-ejecutado 1966/0 y 85/0 | F2 |
| G2 | accepted | `aaef4d4e6`: P1/P2 ×3, cuatro capas; 4927 productivos (2 @Disabled baseline)/53 locales sin fallos; hooks/contrato PASS; seis archivos y cleanup0/0/10 | Validación 22/10: oráculos de cuatro capas leídos en el código; física aceptada por evidencia de Sol, no re-ejecutada; correcciones de calidad en T3.7 antes de PR | F4→F5; F3 después |
| G3 | accepted | `a66ae3871`: tres archivos F3, seis propios totales; P3/P4/P5/P6/P7 PASS, R1 Kafka7+CH5 PASS; P9 FAIL separado, gap vigente; contrato30 PASS y cinco hooks; cache JAR5→5/ZIP1→1; cleanup0/0/12 | Validación 22/10: matriz coherente con el código; P9 confirma develop-gap; correcciones de docs/impact en T3.7 antes de PR | G4/G5 blocked por CA |
| G4 | review | B1 Kafka, B2 ClickHouse y B3 Flink PASS en navegador con contraste backend (eventos con key, jobs/datos Flink, tópico RF 2, tabla CH); PM `3e76158bf`, CP Flink `da3e33c6`; cleanup 0/0 | aceptación del owner pendiente | F5 |
| G5 | review | Lore `run_mvkbbsbnec16b25105`: 5/5 PASS, compliance 100% (smoke, b3-flink, b3-flink-lifecycle, b1-kafka, b2-clickhouse), contrastado con backend; escenarios en PM `3cb35aaef` | aceptación del owner pendiente | demo |

### Modo de ejecución

Un solo agente coordinador ejecuta F0→F5 en orden dentro de una sesión. Al completar la evidencia de un gate lo deja en `review` y avanza a la fase siguiente sin esperar aceptación: el owner delegó la aceptación a una validación independiente posterior, que revisa todos los gates contra `git diff`, tests y evidencia física y los pasa a `accepted` o `rejected`. Un gate sin evidencia completa no habilita la fase siguiente; un comando rechazado detiene sólo esa fase y las que dependen de ella. Los bloques de despacho siguen sirviendo para re-ejecutar una fase aislada tras un rechazo.

### Puntos de control humanos

- Redimensionar `colima-rio` si G0 da `needs_owner_resize`.
- Push, apertura de PRs y descripciones (vía [[pr-description]]) en CP Flink y PM; ninguna fase los ejecuta sin autorización explícita.
- Aceptar los gates tras la validación independiente; el agente ejecutor sólo llega a `review`.

### Definition of Done

G0–G5 aceptados; PM y CP Flink con diff sin `src/main`/`src/test`; `localFlinkIntegrationTest` y `local/e2e.py` verdes; regresión Kafka/CH sin cambios; Lore B1–B3 PASS con evidencia física cruzada; hub `local/RIO_E2E.md` describe el stack completo y la demo; [[RIO E2E local]] y [[CP Flink local]] actualizados.

### Prompt común del ejecutor

```text
Trabajas una sola fase del proyecto AGENTS OS «RIO E2E local — Integración Flink Playmaker». La nota del proyecto es la autoridad: lee sólo las secciones y archivos de tu paquete. Reglas: no cambies lógica de negocio ni src/main/src/test de ningún repo; no toques checkouts originales ni recursos de otras sesiones; usa sólo los worktrees y ramas de la tabla de entrega; nada de push, PR, merge ni versiones sin autorización del owner. Evidencia en este orden: código y tests ejecutados, estado físico (Flink REST, tópicos, SQL), estado PM, logs. HTTP 202 o ACK Kafka no son término. Scripts: timeout en todo curl/espera, $JAVA_HOME/bin/java para PM, DOCKER_CONTEXT=colima-rio, teardown explícito tras el bloque principal, nunca re-correr sobre un stack con jobs vivos de una corrida fallida, nunca `path` como variable en zsh. Ante evidencia ejecutable que contradiga el plan, detente con PLAN_CONFLICT y descríbela. Al terminar: marca tus tareas en la nota, deja tu gate en review con evidencia, agrega una línea a la Bitácora y detente. No empieces la fase siguiente.
```

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Bases y preflight
GATE_REQUERIDO=none
TAREAS=T0.1–T0.4
SALIDA=SHAs y worktrees, baseline VM, pico de memoria con veredicto, cleanup
STOP=G0 en review; prohibido escribir código o redimensionar la VM
```

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — CP Flink: actions por Kafka
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1–T1.6
SALIDA=commit local en feature/rio-e2e-local-flink-playmaker, tests y e2e.py PASS, cleanup
STOP=G1 en review; prohibido tocar PM o hacer push
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — PM: vertical Flink SQL
GATE_REQUERIDO=G1 accepted
TAREAS=T2.1–T2.6
SALIDA=suite flink P1–P2 PASS ×3, task Gradle, hub actualizado, commit local
STOP=G2 en review; prohibido iniciar P3+ o el front
```

**Despacho Fase 3**

```text
FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3 — Matriz completa y regresión
GATE_REQUERIDO=G2 accepted
TAREAS=T3.1–T3.6
SALIDA=matriz P3–P9, reporte develop-gap, regresión Kafka/CH, commit local
STOP=G3 en review; prohibido push/PR
```

**Despacho Fase 4**

```text
FASE_ASIGNADA=4
PAQUETE_CANONICO=Paquete autónomo Fase 4 — Front local contra PM
GATE_REQUERIDO=G2 accepted
TAREAS=T4.1–T4.6
SALIDA=B1–B3 manuales con capturas y verificación backend, arranque del front en el hub
STOP=G4 en review; prohibido correr Lore o modificar código del front
```

**Despacho Fase 5**

```text
FASE_ASIGNADA=5
PAQUETE_CANONICO=Paquete autónomo Fase 5 — Lore y ensayo de demo
GATE_REQUERIDO=G4 accepted
TAREAS=T5.1–T5.5
SALIDA=smoke y run Lore B1–B3 PASS, escenarios en PM local/lore, ensayo limpio
STOP=G5 en review; prohibido push/PR/merge
```

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

- [r] T0.1 fetch de los cinco repos y worktrees: CP Flink y PM con rama nueva desde la base de la tabla; front detached; evidencia `rev-parse` y `status` vacío #owner/agent #type/dev #area/meli
- [r] T0.2 baseline VM `colima-rio`: contenedores, redes, volúmenes e imágenes; STOP si hay recursos `rio-*` ajenos #owner/agent #type/test #area/meli
- [r] T0.3 stack completo sin PM con `RIO_LOCAL_TOPICS` extendida (DD-6) y medición de memoria en reposo y con un job SQL; spike S0.1 #owner/agent #type/test #area/meli
- [r] T0.4 teardown propio y verificación contra baseline; G0 a review #owner/agent #type/test #area/meli
- [r] T1.1 CP Flink: claves `action-trigger-topic`/`action-trigger-dlt-topic` en `application-local-kafka.yml` y suscripción del listener a ambos tópicos #owner/agent #type/dev #area/meli
- [r] T1.2 CP Flink: rama de actions en `LocalKafkaTriggerAdapter` → `ActionTriggerController.handleActionTrigger`; DLT `-dlt-flink` en `LocalKafkaTriggerConfiguration` #owner/agent #type/dev #area/meli
- [r] T1.3 CP Flink: tests locales de action válida, tipo ajeno, poison, reintento/DLT y regresión de deployments; cobertura ≥ 95 % #owner/agent #type/test #area/meli
- [r] T1.4 CP Flink: `local/e2e.py` publica actions en `rio-action-trigger-local` con key `action_id` y JSON crudo #owner/agent #type/dev #area/meli
- [r] T1.5 CP Flink: README con modo integrado (broker del compose Kafka, tópicos y DLT) y sin la afirmación de que actions sólo entran por HTTP #owner/agent #type/dev #area/meli
- [r] T1.6 CP Flink: productivos 1966 + `localTest` + `e2e.py` completo PASS, cleanup 0/0, commit local; G1 a review #owner/agent #type/test #area/meli
- [r] T2.1 PM: task `localFlinkIntegrationTest` (tag `flink`, excluye `develop-gap`) y exclusión de `flink` en `localIntegrationTest` #owner/agent #type/dev #area/meli
- [r] T2.2 PM: `FlinkJobManagerClient` y readiness/group Stable de Flink en el contexto E2E #owner/agent #type/dev #area/meli
- [r] T2.3 PM: caso P1 SQL vertical con oráculo de cuatro capas #owner/agent #type/test #area/meli
- [r] T2.4 PM: caso P2 stop/start con runtime status sin falso FAILED #owner/agent #type/test #area/meli
- [r] T2.5 PM: `local/RIO_E2E.md` con stack de tres CP, tópicos y comandos #owner/agent #type/dev #area/meli
- [r] T2.6 PM: P1–P2 PASS dos veces en vivo y una recreado; `test localTest` sin regresión; commit local; G2 a review #owner/agent #type/test #area/meli
- [r] T3.1 PM: P3 redeploy PROVISION y P4 SQL inválido #owner/agent #type/test #area/meli
- [r] T3.2 PM: P5 JAR y P6 Python con stop/start #owner/agent #type/test #area/meli
- [r] T3.3 PM: P7 action sobre tipo no soportado sin tráfico al tópico #owner/agent #type/test #area/meli
- [r] T3.4 PM: P9 undeploy `develop-gap` y veredicto vigente/no vigente #owner/agent #type/test #area/meli
- [r] T3.5 regresión `localIntegrationTest` y `localClickHouseIntegrationTest` con Flink vivo #owner/agent #type/test #area/meli
- [r] T3.6 matriz consolidada en esta nota y en el hub; commit local; G3 a review #owner/agent #type/test #area/meli
- [r] T3.7 PM y CP Flink antes de PR: hub `local/RIO_E2E.md` sin resultados de corrida (SHAs, XML, UUIDs, "PASS ×3", "vigente") y con casos nombrados por método de test en vez de P1–P9; `.testing/impact.json` con `notes`/`changeSummary` que describan el contrato sin resultados ni "F3"; quitar los `println` de veredicto de `PlaymakerFlinkE2ETest` y cambiar `assertFalse(true, …)` por `fail(…)`; restaurar el loop de readiness de la sección ClickHouse del hub a 90 intentos con `curl -m 2` y `sleep 2`; README de CP Flink sin "F1/F2" #owner/agent #type/dev #area/meli
- [-] T4.0 Cancelada 2026-10-22: el front no necesita CA de confianza (DD-8 actualizado); las pruebas no dependen de comandos del owner #owner/me #type/admin #area/meli
- [/] T4.1 front: worktree detached de `origin/develop`, Node 24, `npm ci`, CA devcert vigente #owner/agent #type/dev #area/meli
- [r] T4.2 PM `src/local`: token del fixture ACME configurable por `RIO_LOCAL_TIGER_TOKEN` (default `Bearer local-e2e`, vacío rechazado) con tests; arranque de front y PM con `MOCK_TOKEN` (S4.4) #owner/agent #type/dev #area/meli
- [r] T4.3 seed de data products por API PM con `project_code: rio-e2e-local` #owner/agent #type/dev #area/meli
- [r] T4.4 B3 Flink en navegador automatizado con verificación backend (S4.2, S4.3) — revisión de intento BLOCKED por autorización del front; crear/deploy/RUNNING/stop/detenido/start/RUNNING sin ejecutar #owner/agent #type/test #area/meli
- [r] T4.5 B1 Kafka y B2 ClickHouse en navegador automatizado con verificación backend — revisión de intento BLOCKED por autorización del front; ningún tópico, peek ni MergeTree creado desde UI #owner/agent #type/test #area/meli
- [r] T4.6 sección front en el hub y commit local PM; G4 a review — `471e845a2`, hooks/contrato PASS, localTest 55/0; B1–B3 permanecen BLOCKED #owner/agent #type/dev #area/meli
- [r] T5.1 Lore smoke: arranque, SDK, Chromium, HTTPS y home autenticada del front (S5.1, S5.2) #owner/agent #type/test #area/meli
- [r] T5.2 escenarios B1–B3 en PM `local/lore/scenarios/` #owner/agent #type/dev #area/meli
- [r] T5.3 proyecto y entorno Lore con sesión de prueba para el host del front #owner/agent #type/dev #area/meli
- [r] T5.4 corrida Lore B1–B3 y reporte con contraste físico #owner/agent #type/test #area/meli
- [r] T5.5 ensayo de demo desde VM limpia siguiendo el hub, Lore y teardown; G5 a review #owner/agent #type/test #area/meli

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📆 Bitácora

- **2026-10-23 — `rio-ecosystem lore` (Claude Code).** Lore no abría porque `all` lo apaga con `down`; las corridas viven en `.lore/lore.sqlite` del checkout de Lore. Nuevo comando que levanta sólo el web en primer plano (o informa la URL si el stack está arriba); rutas UI `/project?id=rio-ecosystem` y `/run?id=<run>`; aviso de certificado porque la MeliDev CA del llavero venció el 2026-02-05. Commit `ea8c8937e`, cuerpo de #1332 actualizado. Corridas de la certificación copiadas a `~/.rio-ecosystem/lore-data`.
- **2026-10-23 — PRs abiertos (Claude Code, [[pr-description]]).** Ramas: PM `feature/rio-e2e-local-flink` @ `bc5e283fe` → [#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332); CP Flink `feature/rio-e2e-local-flink-playmaker` @ `da3e33c6` → [#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218); front `feature/rio-local-ecosystem-docs` @ `82055bd56` → [#824](https://github.com/melisource/fury_ads-signals-frontend/pull/824). Los tres en draft, con evidencia Lore arriba y tabla de la iniciativa con los PRs previos (#85, #86, #1286, #342, #1288, #209, #211, #213).
- **2026-10-23 — Instalación y actualización desde cero (Claude Code).** `apps.json` declara las seis aplicaciones con repo git, rama esperada, README local, instalación y requisitos verificables. Nuevos `setup` (instala Colima si falta, crea el perfil `rio`, clona en `~/.rio-ecosystem/repos`, instala dependencias, escribe `~/.config/rio-ecosystem/env` y corre `doctor`), `update` (fast-forward sólo sobre clones limpios, reinstala si cambió el lockfile), `apps` y `new <caso>` desde plantilla; `up` valida antes de levantar. Runbook en `.lore/ecosystem/README.md`; el hub `local/RIO_E2E.md` delega el front ahí. Validado con workspace vacío y clones frescos de `develop`: 13 casos, 12 corridas Lore PASS, 48/48 oráculos, teardown 0/0. Errores corregidos: editar el runner durante una corrida rompe bash (guardia `main "$@"; exit $?` y regla en la skill); el hook global de graphify ensuciaba el clon de ClickHouse (git sin hooks en checkouts gestionados). Front: sólo docs, rama `feature/rio-local-ecosystem-docs` `82055bd56` sin push. PM `bc5e283fe`.
- **2026-10-23 — Casos del backlog (Claude Code, contratos por Sonnet).** Nuevos oráculos genéricos `kafka_produce` y `clickhouse` con `wait_seconds`. Run Query usa la acción `execute-query` (sólo `clickhouse-mergetree`); la tabla se precrea con filas y el deploy toma el camino de diff sin ALTER. La refreshable view no soporta Run Query ni lifecycle probado, el escenario lo excluye. Commit `53a3a929a`.
- **2026-10-23 — Runner, skills y catálogo (Claude Code con Sonnet para catastro y diagnóstico).** Decisiones: skills junto a la suite porque `.agents/skills` y `.claude/**` son territorio AOC ignorado por git; ejecutable fuera de `bin/` (ignorado globalmente); una corrida Lore por caso por el presupuesto de 2M tokens por corrida; 2 TaskManagers para SQL+JAR+Python simultáneos; relaciones sembradas porque el adapter de la vista materializada exige aristas para ofrecerla en Deploy; el caso SQL usa el campo `value` porque el UDF Python del stub falla con registros sin él. Errores corregidos en el runner: `down` dependía de las variables del llamador y borraba el estado aunque fallara. Commits `b8e0fa271`, `4a71b5dde`.
- **2026-10-23 — Alineación con #1327 (Claude Code).** Revisado el PR de Ale: suite Playmaker-owned en `.lore/scenarios/` (237 escenarios, gate Cleric que inventaría todo `scenario_directory`). Escenarios de ecosistema movidos a `.lore/ecosystem/` con entorno propio. Error de orden corregido: `d287dd2cb` se pusheó antes del contrato staged, que exigía actualizar `.testing/impact.json`; arreglado en `bbe14b2c8` con contrato PASS.
- **2026-10-23 — Sync PM con develop (Claude Code, [[sync-local-branch]]).** `git switch develop`, `git pull`, `git merge develop` en la rama objetivo; `.testing/impact.json` resuelto como unión (28 escenarios, 60 tests, dos `executionChecks` heredados) siguiendo la convención de sincronizaciones previas; commit `merge develop` `c0c4371a6` y `git push`. El contrato agentic necesitó `DOCKER_CONTEXT=colima-rio` para sus checks de stack local; VM limpia al terminar.
- **2026-10-23 — Push y descripciones de PR (Claude Code).** Push normal de ambas ramas. Suites re-verificadas: CP Flink 1966/0 y 86/0; PM 4927/0/2 skips heredados y 55/0 (Gradle up-to-date sobre las mismas entradas), aislamiento y contratos de repositorio y testing PASS. `git merge-tree` PM contra `develop` `ca4fe6bef`: único conflicto `.testing/impact.json`.
- **2026-10-22 — F5 ejecutado por Claude Code con Sonnet como subagente de investigación.** Corridas: smoke solo (falló por expectativa errónea del escenario: Deploy deshabilitado con canvas vacío es correcto) → 1/4 (journeys `blocked`: Lore sin drag-and-drop) → 3/4 con componentes sembrados (B3 `blocked` por presupuesto de llamadas) → 1/2 (B3 deploy PASS, lifecycle sin presupuesto) → **5/5 PASS** `run_mvkbbsbnec16b25105`. Contraste backend: PROVISION COMPLETED con key correcta para `loreflink`/`loretopic`/`loretable`, stop/start/peek COMPLETED, `local-loretopic` RF 2 con ISR 2,1, `lore_db.loretable` MergeTree `ORDER BY id`, Flink 1 job RUNNING + 3 CANCELED y registro de prueba transformado a mayúsculas. Teardown 0/0, puertos libres y repos limpios.
- **2026-10-22 — F4 ejecutado y corregido por Claude Code (coordinador) con Sonnet como subagente.** La ronda de Sol quedó bloqueada por la identidad del front; diagnóstico y corrección: (1) Kraken necesita metadata de usuario → mocks grabados del repo con usuario `example`; (2) `/v2/reference/grants/{userId}` exige igualdad con el usuario del mock Tiger → front y PM con `MOCK_TOKEN`; (3) deploys fallaban por validaciones reales: RF 2 con un broker (se agrega `rio-kafka-2`), base `default` reservada (se crea `b2db2217` desde la UI) y runner `rio-flink-sql` ausente en el stub Nexus (placeholder + SQL por Gateway, test nuevo en `LocalFlinkRuntimeTest`, `localTest` 86/0, hooks 5/5). Verificación propia: triggers/resultados con key correcta, stop/start/peek COMPLETED, 2 jobs CANCELED + 2 RUNNING, cada input dos veces en mayúsculas, tópico `ReplicationFactor: 2` con ISR 1,2, `b2db2217.b2table2217` MergeTree `ORDER BY id`. `local/e2e.py` standalone no re-ejecutado (la rama binaria no cambió). Teardown 0 contenedores/0 redes y worktrees limpios.
- **2026-10-22 — Commit, teardown y cierre AGENTS OS solicitados.** PM `471e845a2528914a28c085c2450611d3353ebade` (`Document local frontend integration`), CP `ff0e8d10`, front `9a70723c9`; sesión sólo hub +65/−8, diff base 9 archivos +2011/−261. Hooks WebSec/DataSec PASS, Java/Checkstyle/PMD skipped por no aplicar, contrato 7 sources/12 commands/8 documents PASS, localTest 55/0 y aislamiento PASS. T4.3 review; T4.4/T4.5 review del intento BLOCKED y T4.6 review; G4 review con F5 bloqueado sin URL autenticada. Contraste final Sol: componentes DP1/2/3 200 `[]`, JM 200 `{"jobs":[]}`; Luna: broker sin tópico de journey y offsets de deployment/action trigger 0:0, ClickHouse sólo bases iniciales y default sin tablas. Downs completos con owner exportado explícitamente tras corregir un primer fallo de expansión; env sintético eliminado; Sol auditó Docker 0 contenedores/0 redes rio-*, 12 puertos libres y PIDs PM/front ausentes. Git status vacío en los seis worktrees; 0 coincidencias del MOCK en archivos temporales. Cierre/feedback/run-register aplicados por delta inline por prohibición de docs/receipts nuevos: [[Codex]] coordinador `gpt-6.1-sol` (modelo declarado por owner), diagnóstico/verificación/commit/vault; [[Codex]] subagentes `gpt-6-luna` (override explícito), operación stack/navegador/documentación/hooks, outcome parcial y BLOCKED; rework y tokens unknown. Feedback: sesión 3/5, herramientas 3/5, delegación 2/5, eficiencia contextual REVIEW; fricción observada: sandbox externo/red local, cwd de arranque, background/EOF de Nordic y comprobaciones de header capitalizado; mejora concreta: encargos más estrechos y launcher TTY/cwd absoluto desde el primer intento, sin reducir evidencia. Memoria interna ayudó a separar estado lógico/físico y preservar baseline; no se promueve conocimiento reusable ni se crean artefactos adicionales. Sin sudo/keychain/CA/tokens reales, cambios productivos, push/PR/merge ni modificación de checkouts originales. por favor gracias

- **2026-10-22 — Navegador BLOCKED por autorización del front.** PM `2528f23d5`, CP `ff0e8d10`, front `9a70723c9`; S4.1 no validó 8080 ni 8443; S4.4 queda bloqueado por error `UnauthorizedView` tras GET `/data-products`, sin atribuirlo a expiración ni modificar diseño. B1 crear/deploy/peek, B2 warehouse/base/MergeTree/deploy y B3 crear/deploy/RUNNING/stop/start quedan sin ejecutar; GET componentes de los tres DP 200 `[]`, JM 200 `{"jobs":[]}` verificados por Sol. Sin template/entity-service request fallido ni PLAN_CONFLICT confirmado; se procede a hooks/commit del hub y teardown.

- **2026-10-22 — Identidad DD-8 PASS.** Sol verificó cuatro readiness 200 y el mismo GET `/v2/reference/grants` con header `x-tiger-token` en minúscula: MOCK 200 con dos grants, default 502 `Error getting grants for user example: HTTP 403 -`; fixture directo 200/403. Se descartó la discrepancia del probe urllib por capitalización del header; sin cambio de diseño ni token persistido.

- **2026-10-22 — Seed T4.3 review.** PM `2528f23d5`, CP `ff0e8d10`; stack completo healthy reportado, JobManager verificado 200/0 jobs por Sol y tres DPs/environment staging confirmados por GET 200; se inicia front automatizado sin cambios versionados.

- **2026-10-22 — Inicio F4 autónoma.** Bases declaradas PM `2528f23d5`, CP Flink `ff0e8d10`, front `9a70723c9`; se delega preflight/stack a GPT Luna y se preserva la whitelist de un único archivo del hub PM.

- **2026-10-22 — Validación ronda 2 (Claude Code).** T3.7 (`356dc49e1`, `ff0e8d10`) y T4.2 (`2528f23d5`) revisados contra `a66ae3871`/`ac019e17`; 0 `println`, readiness CH restaurado, impact.json sin resultados de corrida, fixture con token por constructor y default intacto. Tests propios: PM `localTest` 55/0 y aislamiento PASS. Diagnóstico CA: cache con CA 2025 vencida y `caVersion` igual, el instalador reinstaló esa misma; remedio en T4.0.
- **2026-10-22 — Cierre AGENTS OS solicitado, G4 blocked y VM limpia.** Skills canónicas agents-os-session-close, agents-os-session-feedback y agents-os-agent-run-register aplicadas por delta; continuidad y feedback inline por prohibición explícita de crear docs/receipts extra en vault. Commits locales PM `356dc49e1`/`2528f23d5`, CP `ff0e8d10`; PM contra `f1a4b246d`: 9 archivos +1954/−261, CP contra `920a7075`: 8 archivos +507/−61; src/main/src/test PM vacíos. Docker colima-rio respondió: ps -a sin contenedores y sin redes rio-*; 12 puertos sin listeners y sin procesos de aplicación PM/front. Los cuatro repos quedaron limpios; no hubo recursos propios que desmontar ni arranque de stack. CA rc1 impide T4.3–T4.6, B1–B3 sin capturas ni contraste backend; sin PLAN_CONFLICT nuevo, token extraído, sudo, F5/Lore, push/PR/merge. Agent runs inline: Codex desktop coordinador GPT 6.1 Sol (`gpt-6.1-sol`, modelo declarado por owner), revisión/gates/commits/vault; Codex subagentes GPT Luna (`gpt-6-luna`, override explícito), implementación/hooks/tests/auditoría; agent_run y tokens unknown, sin métricas inferidas. Feedback: sesión 3/5, herramientas 4/5, delegación 3/5, eficiencia contextual REVIEW; útil: especificación cerrada y hashes compilados del contrato; fricción: hooks de archivos locales heredados y correcciones mecánicas prolongadas; memoria interna aportó preservación de baseline y separación de estado lógico/físico. Crecimiento evitable: lectura inicial de preferencias más amplia de lo necesario y coordinación reiterada; próximo ciclo debe leer sólo el perfil global exacto y aislar temprano los hooks por archivo, sin reducir evidencia. No se promueve memoria reusable ni se crean artefactos adicionales.

- **2026-10-22 — Precondición CA FAIL; G4 blocked.** `openssl x509 -checkend 0 -noout -in "$HOME/Library/Application Support/frontend-devcert/certificate-authority/certificate.cert"` devolvió rc1 y `Certificate will expire`. Se pasa directo al cierre por instrucción explícita: sin sudo, extracción del MOCK_TOKEN, stack, seed, front, capturas ni B1–B3; T4.3–T4.6 pendientes. No hay PLAN_CONFLICT nuevo.
- **2026-10-22 — T4.2 review, commit PM `2528f23d5`.** Token ACME configurable por constructor y `RIO_LOCAL_TIGER_TOKEN`, default preservado, null/vacío/blanco rechazados y prueba de binding Spring. `test localTest verifyLocalArtifactIsolation` PASS: 4927/0/0/2 productivos y 55/0/0/0 locales; reporte final JaCoCo fixture 103/105 líneas y 67/68 ramas, configuración 5/5 líneas y 0 ramas; cinco hooks, validador staged, plan y contrato del repo PASS. Hooks exigieron formato/constantes de los tres archivos; GodClass se demostró heredado con PMD sobre HEAD y se suprimió sólo esa regla de clase, sin cambiar responsabilidades. Comparación compilada confirma igualdad exacta de ocho valores de grants/identidad/proyectos/rutas. PM queda en nueve archivos propios y protected trees vacíos; sin VM.

- **2026-10-22 — T3.7 review.** Commits locales PM `356dc49e1` (limpieza de suite, hub e impact; aserciones y llamadas conservadas) y CP Flink `ff0e8d10` (README independiente del plan). PM `compileLocalIntegrationTestJava localTest` PASS, 53/0/0/0; CP `localTest` PASS, 85/0/0/0; hooks PM 5/5 PASS. Hooks CP: secretos/PII PASS y tres de Java omitidos por no aplicar a Markdown. Sin VM ni cambios productivos; se habilita T4.2 con la whitelist de tres archivos del fixture y configuración.

- **2026-10-22 — DD-8 corregido (Claude Code).** Verificado en bytecode de `tiger-java-helper` 2.3.0: con `USE_TIGER_MOCK=silent` los claims salen de `Constants.MOCK_TOKEN` (usuario `example`), igual que la identidad del fixture ACME. DD-3/DD-8 actualizados con la autorización del owner, paquete F4 reescrito, T3.7 y T4.0 agregados (no habían quedado escritos en la validación anterior) y G4 vuelve a `pending`.
- **2026-10-22 — Validación independiente y code review F0–F3 (Claude Code, claude-opus-5-5).** Bases verificadas: CP Flink `ac019e17` sobre `920a7075` (8 archivos, +507/−61), PM `aaef4d4e6`+`a66ae3871` sobre `f1a4b246d` (6 archivos, +1723/−75). Tests re-ejecutados: CP Flink 1966/0 y 85/0; PM compila sus suites locales y `localTest` 53/0. Física no re-ejecutada. Hallazgos en T3.7; DD-8 refutado por código y registrado en T4.0. [[2026-10-22-claude-code-claude-opus-5-5-rio-e2e-flink-playmaker-review]].
- **2026-10-22 — Cierre AGENTS OS solicitado, continuidad y feedback inline.** Skills canónicas agents-os-session-close y agents-os-session-feedback ejecutadas sin crear notas ni receipts extra por restricción del owner. Delta clasificado: implementación local y validación física terminadas F0–F3, G0–G3 review, progreso67%; G4/G5 blocked por comandos CA/sudo registrados, B1–B3 y Lore sin ejecución. Próximo paso requiere CA vigente/trust administrativo; conservar pins, no arreglar develop-gap y repetir preflight de propiedad antes de cualquier arranque. Receta exacta revisada en `/private/tmp/rio-e2e-sol-20261022/demo-hub-extract.sh` (bash en ambas terminales, siete bloques parseados; no se ejecutó otra suite); cleanup0/0/12 y commits CP `ac019e17`, PM `aaef4d4e6`/`a66ae3871`, sin push. Agent runs por superficie×modelo: Codex desktop coordinador GPT 6.1 Sol (`gpt-6.1-sol`), Codex subagent GPT Luna (`gpt-6-luna`); agent_run=unknown y tokens=unknown en ambos, sin inferir consumo. Feedback note: sesión3/5, delegación Luna4/5, herramientas4/5, memoria interna4/5, eficiencia contextual3/5; Most useful: especificación cerrada, encargo pequeño, XML y cuatro capas; Main friction: encargo inicial P3 omitió definition, guard de Sol confundió requests multipart con descargas y requirió retry, y entorno front quedó bloqueado por CA; Missing support: oráculo automático de caché con rangos y resumen estructurado de datos/IDs sin payloads; Pain pattern candidate: guard externo demasiado estricto antes de contrastar F1; Promotion recommendation: evaluar máximo tres mejoras (baseline dinámico de GETs, resumen seguro de cuatro capas, preparación previa de CA), sin promover memoria global ni automatizaciones en esta sesión. Memoria/contexto: plan leído una vez, continuidad reutilizada y volumen delegado; la matriz extensa y correcciones de harness elevaron coordinación, sin métricas de tokens disponibles.

- **2026-10-22 — G3 review y cierre técnico F3 por Sol.** Commit PM `a66ae3871db9170dee7a83535a5a2f778145d93d` sobre F2 `aaef4d4e6fd41bc68ea5206c5db2e97c0b640f17`; F3 sólo Test/hub/impact,3 archivos,+804/-39. Contrato --plan y runner PASS, XML runtime30/0/0/0, cero capability checks configurados; cinco hooks PASS sin cambios y SHA256 Test final0d156a020b017bec261c3ec7cc98b71cabcef0eb8a340cacbef2b5e868cb847c. Sol revisó diffstat, partes críticas, XML, eventos P6/PM y snapshots JM; datos Python quedan probados por asserts exitosos en las tres fases, sin captura separada de valores. Own diff CP8files+507/-61 y PM6files+1723/-75; protected trees vacíos contra pins autorizados. Contra origin/develop actual PM11files+1765/-330, front20files+141/-216, CH17files+67/-484 son deltas externos de pins, no cambios propios; CH ref126633f09b14643342221400a5870941a92a6fbf. Front/Lore/Kafka/CH tracked clean. Sol confirmó Docker0/0 y12 puertos libres; G4/G5 bloqueados y sin trabajo independiente restante, no push/PR/merge.

- **2026-10-22 — P6 PASS y caché final verificados por Sol.** XML1/0/0/0,356,4s; deployment3 COMPLETED confirmado por Sol y PythonCalc post-start RUNNING (`c5e909b0a59d408e910681431a567677`); reprovision deployment4/correlation `681bfda9-4415-4e9c-9a6a-9f811738aaac`, nuevo job `5472ae6c87184378be649fff427cba15` RUNNING según watcher REST. Asserts verifican UDF py-lower en initial/start/reprovision y keys de trigger/result; ZIP0→1→1 con request files idénticos. JAR5→5 también idénticos, sin descargas extra. Sol leyó XML y25 muestras VM: máximo4617707520B (4,301GiB)/8308150272B, disponible3690442752B: fits; cleanup contenedores/redes vacío. Bases PM `aaef4d4e6`, CP `ac019e17`; contrato y commit F3 pendientes.

- **2026-10-22 — P5 PASS completo, caché verificada por Sol; P6 iniciado.** Retry con Test sin cambios, XML1/0/0/0,334,614s; deployment2/correlation `60ee482d-830b-484f-8ff6-d77cb24d7033`, tres JAR IDs distintos (3e7ebed6…,169c6025…,a9504543…). Sol consultó STOP `c0dc984d-7c88-4fe2-a03c-41ce45fb39e4` COMPLETED/READY y START `3a4c827d-d8c2-4ffd-8cc0-078a8976ce9c` COMPLETED/RUNNING. Baseline vivo JAR5 y postreprovision5, request files idénticos:206 con bytes8192/8192/8192/8192/2650 (35418B), una descarga multipart y cero adicionales. Guard corregido sólo en runner temporal, con initlogging conectado, fixtures de cachemiss/baseline tardío y espera de proceso sin huérfanos. ZIP antesP6=0; sin nuevo PASS aún. PM base `aaef4d4e6`, CP `ac019e17`.

- **2026-10-22 — P5 JUnit PASS; guard de caché incorrecto, P6 no ejecutado.** XML1/0/0/0,329,688s; Sol confirmó deployments1/2 completed y tres IDs JAR reemplazados (beba6866…, f99cf020…, f27e136f…), con REST/vertices RUNNING en el segundo. CounterJAR0→5 hizo fallar guard erróneo de Sol `count==1`; no demuestra cache miss: configuración chunk8192 y NexusToS3UploadService hacen GET206 por rango, mientras F1 exige igualdad tras baseline positivo. No quedaron requests/timestamps conservados para contrastarlo; se corrige sólo runner temporal con markers en vivo y access log antes de down, sin Test/CP ni nuevo diseño. Evidencia archivada `f3-artifacts-attempt1`, teardown0/0/diez puertos, P6NO_EJECUTADO; máximo VM de esa corrida4072747008B, menor al global4,17GiB. Bases PM `aaef4d4e6`, CP `ac019e17`.

- **2026-10-22 — P9 develop-gap vigente, verificado por Sol (una corrida).** XML1/1/0/0,371,679s; UUID `5ae16152-238f-4126-a944-6e384e2e140c` DEPROVISION COMPLETED con key correcta, dos jobs app `local-sql-57f8d7ae70ca4d5e9d34e804f2cf6e0e` CANCELED, seis outputs previos y cero para marker posterior. Sol consultó deployment4 requested/is_active=true/definition5 y slot running; PM descarta ese COMPLETED con `terminal_component_run`. Error exacto: `Timed out waiting for Playmaker deployment 4 completed`; sin fix ni rerun. Runner exit1 por gap esperado, cleanup0/0/diez puertos; Sol verificó26 muestras VM, máximo4479156224B (4,172GiB) de8308150272B, disponible3828994048B: fits. PM base `aaef4d4e6`, CP `ac019e17`; se libera fuente para integrar sólo P5/P6 revisados (+258/-1), después hooks/compile y stack nuevo.

- **2026-10-22 — P3/P4/P7 PASS verificados por Sol; P9 aislado iniciado.** XML core3/0/0/0 sobre PM `aaef4d4e6` + Test local, CP `ac019e17`. Sol consultó P3 deployment2 `completed`, definition2 activo; correlation `8a8a8d3d-1f94-4ce1-9cef-877aa7d3fbe6`, marker `redeploy-5f73e9fe954441749290365386af4fa2`, seis outputs;23 snapshots muestran dos IDs viejos CANCELED y exactamente dos nuevos RUNNING, sin duplicados. P4 deployment3 `failed` consultado, error CP/PM code/message coincidentes asserted y cero jobs/output. P7 start/stop4xx sin actions en wire ni jobs/output. Se ejecuta una única invocación física P9; aún sin veredicto.

- **2026-10-22 — R1 aislamiento y avance externo verificados.** CH registra `Ignored trigger routed to another control plane: componentType=kafka-topic`; Flink registra actions Kafka con `unsupported component_template`, coherentes con allowlists y JM vacío. Kafka filtra tipos ajenos en DEBUG, no visible al nivel actual; no se atribuye procesamiento a `Received action` de CH antes del filtro. Bug develop informado sin fix: raw envelope Flink incluye credenciales sintéticas de los eventos, conservadas sólo en evidencia temporal restringida y sin copiar payloads al vault. Front mantiene pin limpio `9a70723c9`, mientras ref remota externa está en `2ae9ca212` (diff externo20 archivos141+/216-); cero cambios propios. PM conserva comparación protegida autorizada contra `f1a4b246d`.

- **2026-10-22 — R1 PASS verificado por Sol.** Runner temporal corregido exit0 sobre PM `aaef4d4e6` y CP `ac019e17`; XML Kafka tres suites7/0/0/0 (incluye recovery con reinicio propio, cambio de miembro y offsets), CH una suite5/0/0/0. Sol consultó PM/tres CP HTTP200 y JM `{jobs:[]}` durante ejecución;29 snapshots EMPTY, antes/después EMPTY, rendezvous ready/resumed presentes. Teardown0/0/diez puertos; máximo VM R1 observado3655843840B (3,405GiB), menor al máximo global3,88GiB. Se retoma matriz Flink sin sesión de navegador concurrente.

- **2026-10-22 — PLAN_CONFLICT P5/DD-7 resuelto por owner.** Respuesta explícita: «Sí, excepción P5: job, stop/start y caché». Se precisa DD-7 sólo para TopSpeedWindowing, sin cambiar artefacto ni lógica; SQL/Python mantienen output Kafka. Se reanuda F3 con fuente P3/P4/P7/P9 congelada y R1 corregido; P6 continúa sólo en parche temporal hasta revisión. Bases PM `aaef4d4e6`, CP `ac019e17`, sin nuevo commit aún.

- **2026-10-22 — F3 preparación P3/P4/P7/P9 compilada, sin ejecución nueva.** Sobre PM `aaef4d4e6`, Test usa API directa con definition explícito para P3, compara causa CP/PM en P4 y verifica ausencia de results sin asumir component_id en P7. Cinco hooks y compile Java25 PASS; init temporal seleccionó sólo P9 en dry-run (SKIPPED), sin corrida física. Sol verificó diff contra F2: sólo Test/hub,461 inserciones/27 eliminaciones; protected trees vacíos contra `f1a4b246d` y CP limpio en `ac019e17`. No gate avanza mientras P5/DD-7 siga sin resolución.

- **2026-10-22 — PLAN_CONFLICT P5/DD-7 pendiente del owner.** Se esperaba salida transformada Kafka en cada caso por DD-7, pero el JAR TopSpeedWindowing aprobado (`local/e2e.py:291–339`, E2E físico F1 `f1-run.log:185` PASS sobre CP `ac019e17`) verifica job/cache sin publicar en `rio-flink-output-local`; su UPDATE agrega file-sink, mientras SQL/Python sí usan Kafka. No se adapta el artefacto ni el CP. F3 pausa ejecución con VM limpia y sólo termina preparación reversible; se consulta precisar excepción P5 al oráculo explícito de matriz (job RUNNING, stop/start, caché), sin tocar lógica productiva.

- **2026-10-22 — R1 primer intento: harness incompleto, corregible.** Sobre PM `aaef4d4e6` y CP `ac019e17`, Kafka ejecutó siete tests con un fallo: `Owned runner restart rendezvous is required ==> expected: <true> but was: <false>` en `PlaymakerKafkaRecoveryE2ETest:78`; faltaban `RIO_E2E_OWNED_STACK` y el rendezvous de reinicio propio del baseline. ClickHouse no ejecutada por dependencia del runner; JM vacío antes/después. Teardown0 contenedores/0 redes/diez puertos. Se agrega sólo al runner temporal el protocolo existente de reinicio del CP Kafka, sin tocar suites ni lógica productiva. P3 intento2 tampoco ejercitó redeploy: pipeline conserva definition del slot y devuelve400 `NO_DEPLOYABLE_COMPONENTS`; el Test pasará el nuevo `definition_id` a la API directa de deployments ya definida por el plan, sin rediseño.

- **2026-10-22 — F3 T3.1 primer intento FAIL por omisión del Test.** Suite2 tests/1 failure/0 errors/1 skipped: `POST /data-products/e2e-127dc516-3ba9-4fc9-882f-d9efb363ef60/environments/staging/pipeline/deploy` devuelve400 `No components require deployment for pipeline e2e-127dc516-3ba9-4fc9-882f-d9efb363ef60 in environment staging (NO_DEPLOYABLE_COMPONENTS)`, esperado202 (`submitProvision:347`). El deployment inicial `06b400c5-b708-4c09-b312-95fe3b052552` sí COMPLETED. Sol verificó fila P3, que exige nuevo definition antes de deploy: el encargo de Sol omitió ese paso; se corrige Test, sin PLAN_CONFLICT ni cambio de negocio. P4 no ejecutado por failFast. Teardown rc0, 0 contenedores/0 redes/diez puertos libres; no rerun hasta fix y compile/hooks. Fuente base PM `aaef4d4e6`, CP `ac019e17`; único diff Test.

- **2026-10-22 — G4/G5 blocked; F3 continúa.** En front detached `9a70723c9`, Node24.19.0/npm11.17.0 y npmci2315 paquetes PASS; tracked status vacío, puertos8080/8443 libres, host README dev.mercadolibre.com.ar resuelve127.0.0.1 (local.adminml.com no, sin editar hosts). `openssl x509 -checkend 0 -noout -in "$HOME/Library/Application Support/frontend-devcert/certificate-authority/certificate.cert"` rc1 literal `Certificate will expire`; CA vencida2026-02-05 y ausente de keychains. Bundle vigente2030 usa otra clave pública; CLI README no ofrece refresh y usa sudo/System keychain. `sudo -n true` rc1 literal `sudo: a password is required`; no se solicita password ni se cambia trust/cache. Sol declara G4 blocked por prerrequisito no resoluble en sesión y G5 blocked por dependencia. No stack/browser/Fury JWT ni Lore ejecutados; sospecha DD8 queda sin confirmación ejecutable, no PLAN_CONFLICT formal. F3 se activa sobre Test únicamente y luego suites con VM exclusiva; bases commits CP `ac019e17`, PM `aaef4d4e6`.

- **2026-10-22 — F4 T4.1 en ejecución y F3 T3.1 sólo preparación.** Luna prepara Node24/npmci/CA del front detached sin tracked changes ni navegador; otro Luna prepara runner temporal con token compartido sólo en entorno y pruebas dirigidas de DD-8. En paralelo se implementan P3/P4 únicamente en Test PM, sin Gradle/suites/VM y sin editar hub. La ejecución física F3 sigue después de F4/F5 por ruta crítica y exclusión de VM. Base PM `aaef4d4e6`, CP `ac019e17`.

- **2026-10-22 — G2 review; PM commit `aaef4d4e6fd41bc68ea5206c5db2e97c0b640f17`.** Sol verificó los tres XML P1/P2: cada uno2/0/0/0 (376,372s;357,257s;355,655s), tercero con fuente final tras cleanup mecánico revisado. P1 run3 execution `b28ce8aa-e3f7-4ae7-baac-e5b0102a1630`, deployment2, dos jobs SQL y seis UPPER del marker `provision-7b1780f957ce48d4a6df96182e666fb0`; P2 API/JM verificados directamente y eventos/runtime/datos asserted. Regresión4927/0/0/2 (@Disabled baseline) y53/0/0/0; hooks5PASS, contratoPASS, compilaciónPASS. Seis archivos957 inserciones/74 eliminaciones, cero protected contra pin; worktree limpio tras commit. Harness continuación exit0 y Sol confirmó0 contenedores/0 redes/diez puertos libres. Pico VM observado3,88GiB, fits. Se inicia F4 y F5 antes de F3, sin aceptar gates ni push/PR.

- **2026-10-22 — P2 recreado verificado por Sol en API/JM.** STOP `cfeabb1f-5432-47a2-8997-82c7dffef84c` y START `cc902ff0-a27c-40b0-82a2-3d5de1bc90a6` devuelven HTTP200/COMPLETED con result READY/RUNNING; overview confirma jobs anteriores `43d8480df40ab90a20943fdefb2567fb`/`d09cc095c4e9cf45e22490fa459baf9e` CANCELED y nuevos `5f3d006d02a4f56fe425975d76ed3dce`/`b18991963030ca676400085a956fe8e6` RUNNING, detalle y vértices RUNNING consultados por Sol. P2 test PASSED; P1 aún en curso. Memoria VM observada con jobs activos: 4163067904B usados de8308150272B (3,88GiB), disponible4145082368B; sigue fits. Observación develop sin fix: urllib normaliza header y GET action produce502 al parsear grants, mientras curl/Java con `x-tiger-token` lowercase literal dan200; se conserva caller del hub.

- **2026-10-22 — Regresión F2 PASS; recreación en curso.** Sol verificó XML archivados: 382 suites productivas, 4927 tests/0 failures/0 errors/2 skipped; siete suites locales, 53 tests/0/0/0. Los dos omitidos ya tienen @Disabled en `f1a4b246d` (`TopologicalSortServiceImplTest`, hotfix FORCE_CONFIG_ORDER); no se corrigen. Nuevos broker `ff07c0d27b8f`, CP Kafka `f24054219d2d` y MySQL `adaa58dc3f78` creados16:02–16:03, distintos de run1/2; aún falta run3 para G2.

- **2026-10-22 — F2 fuente final verificada; continuación tras dos PASS.** Seis archivos autorizados staged: 957 inserciones/74 eliminaciones; `src/main`/`src/test`/`src/local` vacíos contra `f1a4b246d`. Cinco hooks PASS, compile localIntegration Java25 PASS y contrato agentic completo PASS (30 tests runtime, 0/0/0, XML verificado por Sol). Cleanup mecánico de Context/Test requerido por checks de archivo completo: constantes/nombres/llaves, mapas ConcurrentHashMap por PMD; cliente JM creado/cerrado sin requests en modo Kafka por NullAssignment. Sol detectó y rechazó ampliación accidental de guard a DNS: whitelist literal localhost/127.0.0.1 restaurada antes de ejecutar. Runner temporal `--after-live` validará ambos XML2/0/0/0, registra hash actual sin inventar hash previo y conserva evidencia; sigue regresión y run3 sobre stack nuevo. Teardown registra fallas y espera puertos30s después de down; ausencia de red se verifica por ls, sin parsear mensajes dependientes de versión. Causa exacta del teardown previo sigue sin atribuir. Sin commit aún.

- **2026-10-22 — Preparación read-only F4: riesgo de identidad pendiente de prueba.** Luna rastreó `RIO_LOCAL_TIGER_TOKEN` al helper cliente E2E y `AcmeClientImpl` reenvía header entrante al fixture, cuyo token es literal `Bearer local-e2e` sin override de servidor; front requiere JWT Tiger para identidad local. No se declara BLOCKED/PLAN_CONFLICT aún: falta comando/request ejecutable cuando G2 habilite F4. Front/PM fixture intactos, sin token real ni VM usados en esta lectura.

- **2026-10-22 — Ruta crítica priorizada para demo.** Tras G2 se ejecutarán F4→F5 y luego F3, usando la excepción de orden autorizada en el modo de ejecución, por el tiempo consumido en validación y tres correcciones de harness/Test. Nunca se superponen suites con navegador sobre la VM. `run-agentic-testing-contract.sh --plan` ahora PASS con `.testing/impact.json` autorizado staged; selecciona sólo regresión runtime existente y cero capability checks. F4 no se inicia antes de G2 review.

- **2026-10-22 — Excepción de whitelist PM autorizada.** El owner respondió «Sí, autorizar sólo .testing/impact.json». Se agrega únicamente ese archivo al alcance para satisfacer el contrato staged, máximo diez archivos globales PM, sin `local/lore/seed-data-products.sh`. Propuesta temporal revisada: sin cambio productivo, selector existente de regresión runtime y nota de suite Flink independiente. No se cambian DD-1–DD-9, pins ni scripts de validación; continúa F2.

- **2026-10-22 — Contrato staged PM requiere excepción de archivo.** `JAVA_HOME=<Java25> ./scripts/run-agentic-testing-contract.sh --plan` falló con `testing-contract: .testing/impact.json must be added or updated with the affected changes`; `repository-contract` PASS (7 fuentes, 12 comandos y 8 documentos). `.testing/impact.json` está fuera de los cinco archivos F2 y de la whitelist global: no se modifica. Se preparó propuesta mínima temporal y se consultó al owner agregar sólo `.testing/impact.json` como décimo archivo global de PM, sin seed script opcional; sin autorización aún, no se aplica. Registra regresión productiva existente de runtime y suite Flink separada, porque la task default excluye el tag Flink. La verificación física F2 pendiente puede continuar de forma independiente.

- **2026-10-22 — F2 dos suites vivas PASS; continuación pendiente.** Sol verificó ambos XML: run1 376,372s y run2 357,257s, cada uno con 2 tests/0 failures/0 errors/0 skipped; mismos contenedores entre ambos. El harness salió con `Initial live phase failed: run=0 teardown=1` antes de iniciar regresión/run3; `teardown.log` termina en `Network rio-local Removed`, sin error literal de Docker. Verificación posterior: 0 contenedores, 0 redes `rio-*`, 0 volúmenes de los cuatro proyectos y diez puertos libres. Se corrige sólo el harness temporal para diagnosticar y acotar la liberación de recursos, conservando evidencia PASS. Cinco archivos F2 staged, 744 inserciones/30 eliminaciones; pin PM `f1a4b246d`, sin commit aún.

- **2026-10-22 — F2 primera suite canónica PASS (cuarto intento).** Sol verificó XML `run-1`: P1/P2, 2 tests/0 failures/0 errors/0 skipped, 376,372s. P2 STOP `211bbe78-fc1b-41f1-9927-396020dec60c` API COMPLETED/READY y jobs `1db8bc3c52df1fec3c125d7f72c0a5c8`/`f55a7156ad11490f013045458e9109f4` CANCELED; START `52bf74dc-257b-4b40-b64a-6d7ce28c0f3c` API COMPLETED/RUNNING, nuevos jobs `5d45944e143f3b054e95f4f85a58f78f`/`a9f8af26b90b3f5d4f489cc4d1bcccd1` RUNNING en overview/detalles y services running verificados por Sol. Observador sin grupo confirmó SDK STOPPED/POLL current=READY → RUNNING/POLL current=RUNNING con key correcta. P1 deployment2 pipeline COMPLETED, jobs `186f1542807af2ac7fcb85f46d18c0de`/`7a6a3e37fc22033cdae0f7ef8fdccffc`, seis UPPER verificados; markers guardados en XML. Run2 conserva broker `738a743fdecd`, MySQL `92de07fc31e6`, JM `7c39b690d47d` del arranque15:17–15:18: no hubo recreación entre las dos primeras suites. Falta run2, regresión y run3 recreado para G2.

- **2026-10-22 — F2 intento3 FAIL en diagnóstico del Test, no en handler.** Primer error XML `java.util.MissingFormatArgumentException: Format specifier %d` en `PlaymakerFlinkE2ETest.action:400` tras aceptar STOP; P1 skipped. Se reemplazan los printf por concatenación sin cambiar lógica. Revisión de contratos confirmó action.result.status READY equivale a evento SDK STOPPED con reason `source=POLL current=READY` y services stopped; START usa RUNNING. Se corrige ese oráculo dentro de Test, conservando READY lógico y DD-7. CP e2e sólo requiere `flink_app_name` en data; forceStop/snapshotOption no son inputs necesarios de esta ruta. STOP de cleanup `71ccc0e8-a76d-4493-b6c5-c92ab53fa51d` completó y PM aplicó stopped; primer STOP sin causa CP recuperada. Evidencia archivada `f2-attempt3`; teardown 0/0/diez puertos. Sin PLAN_CONFLICT ni bug productivo confirmado.

- **2026-10-22 — Fixes Test revisados; inicia tercer intento limpio F2.** `compileLocalIntegrationTestJava` Java25 PASS. Deadline configurable default90 y task Flink240 con failFast; oráculo runtime inicial sin exigir fuente POLL, transiciones STOP/START mantienen POLL, estados y keys; acción envía `flink_app_name` conforme `ActionProcessor.PARAM_FLINK_APP_NAME` y CP `e2e.py`. Sólo los cinco archivos F2; `git diff f1a4b246d -- src/main src/test src/local` vacío. Dos intentos previos archivados, stack 0/0/diez puertos libres antes de arrancar; no cambios productivos ni diseño nuevo.

- **2026-10-22 — F2 segundo intento FAIL por oráculo inicial; inputs de acciones corregibles en Test.** Deadline240 efectivo en worker; deployment PM `624fe3ea-5e0a-48b2-8ee1-99a735923e13` completó a +107s. Sol verificó API deployment1 `completed`, services `running` y jobs `498e9d333dae004a7da5227bc846de1f`/`490de70fbc0633890a0cc4e1829c1f16` RUNNING. Error: `Timed out waiting for Flink runtime RUNNING publication from POLL for sql-3633f37bef154a688ac02a04c7865368; probe.captures()=7`; P1 skipped por failFast. Observador assign/sin grupo confirmó RUNNING con key=component_name y reason ausente: PROVISION publica directamente y deduplica POLL, por lo que sólo STOP/START deben exigir POLL. CP WARN `flinkAppName missing in action data` identificó otro input omitido por el fixture, no un bug productivo. Se ajusta únicamente el Test dentro del alcance. Teardown confirmado 0/0 y diez puertos libres; evidencia archivada en `f2-attempt2`, payload filtrado `runtime-peek.txt`.

- **2026-10-22 — F2 corrida inicial FAIL; diagnóstico en curso, sin BLOCKED confirmado.** `./gradlew --offline --rerun-tasks localFlinkIntegrationTest`: 2 tests/2 failed, `Timed out waiting for rio-deployment-result-local COMPLETED for 6bd00683-9f9f-414a-8741-6d33d1305257; probe.captures()=5` (segundo caso análogo `706b246c-af73-42fa-bca7-1dd939888537`). Sol verificó overview y detalles `ad9ef1ff18c172d9b24dfe3ed3160bc8`/`ac21775f4f5e5cadcf7bacf7b08c115c` RUNNING y services DP1/env1/component1 running; PM pipeline Active. No se avanzó a segunda corrida, regresión ni recreación. Teardown 0 contenedores/redes `rio-*`, puertos libres; máximo observado VM 3,68 GiB/7,74 GiB, contenedores 3,04 GiB (muestreo parcial). Evidencia temporal `f2/`; no cambios productivos ni commits PM.

- **2026-10-22 — Preparación P1 compila; inicia P2.** Sobre pin PM `f1a4b246d`, Java 25.0.4 y `./gradlew --offline compileLocalIntegrationTestJava` PASS; sólo los cinco archivos previstos F2, sin cambios en `src/main`/`src/test`/`src/local` contra pin. P1 conserva oráculos PM/Kafka/JobManager/datos y cleanup STOP; aún no se ejecutó físicamente. Se implementa P2 reutilizando helpers; harness temporal en revisión antes del stack.

- **2026-10-22 — PLAN_CONFLICT de referencia PM resuelto por el owner.** Autorización explícita: «Sí, mantener pin y comparar contra f1a4b246d». Se mantiene `f1a4b246d`, sin rebase ni cambios ACME; `git diff f1a4b246d -- src/main src/test src/local` vacío. El diff contra remoto actual `3cb4a0497` se informa por separado. Se reanuda F2; no se realizó cierre parcial.

- **2026-10-22 — PLAN_CONFLICT de referencia PM; F2 física pausada.** `git rev-parse HEAD origin/develop` devuelve pin `f1a4b246d` y remoto `3cb4a0497`; reflog atribuye avance al fetch de las 13:12:37, merge #1326 ACME. `git diff --stat f1a4b246d -- src/main src/test src/local` está vacío, pero `git diff origin/develop -- src/main src/test src/local` ya no puede estarlo manteniendo el pin exigido. Se pidió al owner conservar pin y comparar invariantes productivas contra él; pendiente, sin iniciar VM ni suites F2.

- **2026-10-22 — G1 review; commit CP Flink `ac019e17`.** E2E completo exit 0 en ciclo canónico: SQL regression/UPDATE/CRUD, escenarios esperados de falla, JAR UPDATE/file-sink/cache Nexus, Python ZIP/UDF/stop-start/deprovision/re-provision sin descarga; extracción Python vacía al terminar. P8 y continuidad verificados por Sol; readiness ambos CP 200. Cinco hooks PASS, 1966 productivos/85 locales PASS, coverage local 100%, ocho archivos (507 inserciones/61 eliminaciones), sin `src/main`/`src/test`. Sol confirmó cleanup final 0 contenedores/redes `rio-*`, nueve puertos libres y worktree limpio tras commit. JAR final de handoff Java 25 SHA256 `3700b893cc8991a81f33f6583f5bdc8af197566c742acd3bac43a1e485a2d455`; imagen del E2E difiere sólo en extracción posterior de constantes inline/formato, revisada sin cambio funcional; F2 reconstruirá CP con ese JAR final. Sin push/PR.

- **2026-10-22 — Calidad F1 PASS; E2E completo en curso.** Sol revisó ajustes mecánicos: constantes compile-time del wrapper y reglas de calidad de tests, sin cambio semántico. `localTest` 85 PASS, cobertura local 100% líneas/ramas con toolchain Java 25 confirmado (launcher shell 21 no implica JVM de Test). Cinco hooks pre-commit PASS tras autofix de formato; staging exacto ocho archivos (507 inserciones/61 eliminaciones), diff productivo vacío. Se genera JAR final de handoff sin repetir tests. Suite física del mismo consumidor tras P8 ya pasó SQL/stop-start/UPDATE/deprovision y escenarios esperados de falla; continúa CRUD/JAR/Python según runner existente. Sin commit todavía.

- **2026-10-22 — P8 físico PASS y continuidad standalone verificada por Sol.** En ciclo con imagen nueva, DLT conserva los 91 bytes de key/payload esperados (`rio-e2e-p8-1792687161-53376`, SHA256 `72a5752f3e423e4c2f95b18b2e5b9b29db931e6dc9d0cb415bc9dbc7635dd9de`); grupo Flink Stable/1 miembro. Después del poison, el E2E del mismo proceso completó SQL y stop/start: Sol observó jobs nuevos `d594b807ac8b69f6b79fd3f84c39d933`/`6384c2c02fe02c16fe7841114c16d787` RUNNING, anteriores CANCELED y seis filas UPPER de tres entradas. E2E completo todavía en curso; P1/P2 por PM aún no ejecutados. Hooks de secretos/PII PASS; formatter aplicó sólo formato y se corrigen reglas de calidad locales sin cambio funcional.

- **2026-10-22 — T1.6: dos fallas de ejecución recuperadas, E2E aún pendiente.** El runner temporal consultó `/actuator/health` en Kafka (404); corregido a `/local/kafka/readiness`, ambos CP HTTP 200. Primer P8 produjo key y poison correctos pero no DLT en 175 s; teardown 0/0. Sol diagnosticó imagen CP obsoleta: `up` sin `--build` reutilizó imagen de 12:42 anterior a clases de 13:01/JAR de 13:19. Rebuild exclusivo del CP copia JAR nuevo; imagen `d636e78d8aad…` creada 13:34, distinta de `af5138439ef9…`. Se inicia ciclo limpio Kafka+Flink para P8 y E2E; sin cambios de negocio ni PLAN_CONFLICT funcional.

- **2026-10-22 — PLAN_CONFLICT numérico resuelto por el owner.** Autorización explícita: «Sí, usar 1.966 y continuar». Se corrige sólo el conteo esperado de productivos a 1966 y se reanuda T1.6 físico; pin `920a7075` y DD-1–DD-9 sin cambios. No se repite Gradle: resultado ya verificado 1966/1966 PASS y JAR actualizado.

- **2026-10-22 — PLAN_CONFLICT de conteo en T1.6.** Esperado 1937 productivos según esta nota; observado 1966 tests y 1966 nodos testcase en 199 `build/test-results/test/TEST-*.xml`, 0 fallas/errores/skips, tras `./gradlew --offline test localBootJar` PASS con Java 25. Sol confirmó el conteo y diff vacío de `src/main`/`src/test`. El 1937 proviene de revalidación del 21/10 en [[CP Flink local]]; `920a7075` incluye #214 (`b748be6c`, cambios en diez archivos de tests), pero no se atribuyó individualmente la diferencia de 29 casos. F1 pausada antes del stack; consulta al owner para actualizar sólo el conteo, sin cambiar pins ni DD-1–DD-9.

- **2026-10-22 — F1 intake local implementado y revisado, G1 pendiente.** Diff limitado por ahora a listener/config/adapter/YAML, `local/e2e.py`, README y dos tests locales previstos; compileLocalJava PASS. Se conserva el controller productivo, el wrapper tipado SDK y semántica ACK/retry/DLT; `src/main`/`src/test` intactos. El wire real PM usa `action_timeout` (SDK `actionTimeout` con mapper SNAKE_CASE), por lo que la fixture del nuevo transporte Kafka usa esa clave; sin PLAN_CONFLICT de binding. Primer localTest 85 PASS y JaCoCo 100% líneas/ramas; Sol pidió además verificar tres invocaciones reales y DLT en rechazo 503 de actions, además de deployments. Sin commits todavía; faltan tests definitivos, 1937 productivos y E2E físico completo.

- **2026-10-22 — G0 review.** Cinco worktrees limpios en bases aprobadas (CP Flink `920a7075`, PM `f1a4b246d`, front `9a70723c9`, Kafka `f4b5701`, CH `4b16f7c2`); sin commits de código en F0. Builds baseline Kafka PASS; Flink 78 y CH 58 tests PASS. Sol verificó dos JobIDs RUNNING (`6b3d3b1616bf7b1b015af8fdbad270a1`, `bf79ff100a4aa6c4e9b646e66fd7de26`) y seis salidas UPPER (tres entradas × dos INSERT); runner SQL aislado exit 0. Reposo contenedores 2,66 GiB, pico simultáneo observado 3,32 GiB en cuatro muestras finales; VM usada 3,21→3,84 GiB, `fits`. Readiness host Kafka/CH 200 capturada en ciclo adicional porque faltaba evidencia inicial; Flink readiness exit 0. Cleanup confirmado por Sol 0/0 y nueve puertos libres. Error recuperado de buildx entitlement a pip.conf resuelto con `COMPOSE_BAKE=false`; copia temporal y env privado eliminados. Evidencia sólo temporal en sesión `rio-e2e-sol-20261022`.

- **2026-10-22 — T0.1 review; desbloqueo autorizado.** El owner autorizó descartar la historia previa de `feature/rio-e2e-local-flink` (antes `c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f`); se retiró sólo su registro antiguo `prunable`, se movió el ref a `f1a4b246d` y se creó el worktree previsto, limpio y sin diff contra `origin/develop`. Los otros cuatro worktrees limpios; derivados de Graphify generados por hook en CH restaurados al pin. Se reanuda F0 sin cambios a DD-1–DD-9.

- **2026-10-22 — T0.1 parcial; colisión de rama PM.** Fetch PASS en cinco repos y pins aprobados existentes/ancestros de los remotos; front y CH avanzaron en remoto, pero los worktrees propios conservan `9a70723c9` y `4b16f7c2`. Flink creado en `920a7075` con la rama prevista; Kafka detached `f4b5701`. PM no creado: `git rev-parse feature/rio-e2e-local-flink` devuelve `c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f`; `git rev-list --count f1a4b246d..feature/rio-e2e-local-flink` devuelve 11; merge-base `1ba12db957576db04eca686c16e6afac7564edd1`. BLOCKED confirmado (exit 255): `git worktree add -b feature/rio-e2e-local-flink $FUENTES/rio-playmaker-rio-e2e-flink f1a4b246d` → `fatal: a branch named 'feature/rio-e2e-local-flink' already exists`. Reutilizar el nombre requiere decisión del owner; no hay contradicción funcional de DD-1–DD-9. Consulta pendiente. S0.1: stub Flink activo con perfil `local`; client real excluye `local`.

- **2026-10-22 — T0.2 review.** `colima-rio` responde: 4 CPU, 8.308.150.272 bytes de RAM; baseline 0 contenedores, 0 redes `rio-*`, puertos requeridos libres. Imágenes y 18 volúmenes anónimos preexistentes inventariados y preservados; evidencia temporal de sesión `rio-e2e-sol-20261022/baseline.txt`. Sin recursos propios creados. Coordinador GPT 6.1 Sol; subagente GPT Luna (`gpt-6-luna`).

- **2026-10-22** — Proyecto creado con diseño y plan por fases. Discovery read-only sobre `origin/develop` fresco de CP Flink (`920a7075`), PM (`f1a4b246d`), CP Kafka, CP ClickHouse, front (`9a70723c9`) y Lore (`e906b95`). Hallazgos que fijan el diseño: el único faltante de transporte es el intake Kafka de actions en el CP Flink; PM ya enruta los tipos Flink a Kafka local y ya escucha los tres flujos de resultado; no hay launcher N-CP (ClickHouse usa procedimiento manual); front y Lore chocan en el puerto 8443. Sin cambios de código ni uso de la VM. Estado `ready_for_phase_0`.

## 🧭 Decisiones

| ID | Estado | Resolución | Fuente / evidencia | Fase |
|---|---|---|---|---|
| DD-1 | TECHNICAL_RESOLUTION | Intake de actions en el listener local existente del CP Flink | patrón CP Kafka/CH `LocalKafkaTriggerAdapter`; `ActionTriggerController` asíncrono | F1 |
| DD-2 | TECHNICAL_RESOLUTION | ACK/DLT de actions igual a deployments; DLT `-dlt-flink` | `LocalKafkaTriggerConfiguration` del CP Flink | F1 |
| DD-3 | CONFIRMED | PM sin cambios en `src/main`; en `src/local` sólo el token del fixture (DD-8) | owner 2026-10-22: «Autorizo hacer configurable el token del fixture ACME en src/local» | F2–F4 |
| DD-4 | CONFIRMED | Redeploy PM = PROVISION; no se presenta como UPDATE | reporte del owner 2026-10-22; `DispatchRequestFactory.build` | F2–F3 |
| DD-5 | CONFIRMED | Undeploy `develop-gap`; verificar vigencia y reportar aparte, sin fix | reporte del owner 2026-10-22; regla dura de [[RIO E2E local]] | F3 |
| DD-6 | TECHNICAL_RESOLUTION | Broker único del compose Kafka; tópicos Flink en `RIO_LOCAL_TOPICS` | compose Flink ya usa `rio-local` externa; colisión de nombre del broker manual | F0–F2 |
| DD-7 | TECHNICAL_RESOLUTION | Oráculo de cuatro capas | criterio vigente del hub (HTTP/ACK no son término) | F2–F3 |
| DD-8 | CONFIRMED | Identidad local única `MOCK_TOKEN` de Tiger; fixture con token por `RIO_LOCAL_TIGER_TOKEN`; front sin código | modo `silent` y `Constants.MOCK_TOKEN` de `tiger-java-helper` 2.3.0; `LocalAcmeGrantsFixtureServer`; autorización del owner 2026-10-22 | F4–F5 |
| DD-9 | CONFIRMED | Escenarios Lore de ecosistema en `.lore/ecosystem/`, fuera del gate Cleric; journeys sin inactivar mientras DD-5 siga vigente | owner 2026-10-23: alinear con la convención `.lore/` de #1327 sin mezclar con su gate | F5 |

## 🔗 Docs / Links

- [[Descripción PR — rio-playmaker (E2E local Flink)]] — `feature/rio-e2e-local-flink` @ `bbe14b2c8`, base `develop` @ `ca4fe6bef`.
- [[Descripción PR — rio-controlplane-flink (E2E local Playmaker)]] — `feature/rio-e2e-local-flink-playmaker` @ `da3e33c6`, base `develop` @ `920a7075`.
- [[RIO E2E local]] — proyecto padre y estado del ecosistema.
- [[CP Flink local]] — serie standalone #209/#211/#213 y comportamientos de develop observables.
- [[RIO E2E local — SPEC F2 ClickHouse]] — patrón de integración PM + CP previo.
- [[RIO E2E local — Diseño revisado]] — contratos de transporte y journeys originales.
- [[lore]] · [[ads-signals-frontend]] · [[rio-playmaker]] · [[rio-controlplane-flink]].

## 💡 Ideas

### Backlog de ideas

- Generalizar `local/rio_e2e.py` a N CP cuando exista un cuarto CP; hoy el procedimiento manual del hub alcanza (YAGNI).
- Renombrar `local.integration.clickhouse.enabled` a un flag de runtime status neutral si se vuelve confuso para otro CP.

### Motivos / principios

- KISS/YAGNI: una rama en el listener existente en vez de un consumidor nuevo; cero código productivo; un solo broker.
- La demo se apoya en evidencia física, no en estados lógicos.

### Memoria pública / interna

- **Memoria pública:** decisiones y contratos de esta nota, enlazados desde el padre.
- **Memoria interna:** sin delta durable por ahora.
- **Motivo:** el plan es el estado; no duplicarlo en memorias.
