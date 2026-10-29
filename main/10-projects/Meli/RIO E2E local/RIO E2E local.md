---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Meli]]"
parent:
sprint:
start: "2026-10-08"
due:
progress: 75
repo:
jira:
prs: ["https://github.com/melisource/fury_rio-playmaker/pull/1286", "https://github.com/melisource/fury_rio-controlplane-kafka/pull/86", "https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/342", "https://github.com/melisource/fury_rio-playmaker/pull/1288", "https://github.com/melisource/fury_rio-controlplane-flink/pull/209", "https://github.com/melisource/fury_rio-controlplane-flink/pull/211", "https://github.com/melisource/fury_rio-controlplane-flink/pull/213"]
aliases: ["rio-e2e-local", "RIO local E2E", "Ecosistema RIO E2E local"]
tags:
  - kind/project
  - area/meli
  - project/rio-e2e-local
created: "2026-10-08"
updated: "2026-10-28"
slug: rio-e2e-local
entities: ["[[rio-playmaker]]", "[[rio-controlplane-kafka]]", "[[rio-controlplane-clickhouse]]", "[[rio-controlplane-flink]]"]
related: ["[[ads-signals-frontend]]", "[[rio-frontend]]", "[[Kafka — Ambiente local con servicios reales]]", "[[Ambientes locales RIO — Comparativa de implementaciones]]"]
---

# RIO E2E local

> [!info]+ RIO E2E local
> **Área:** [[Meli]] · **Owner:** Rodrigo · **Estado:** active · **Fase:** ver «Estado vigente»; sesión one-shot cerrada.

## 🎯 Objetivo

Diseñar y luego implementar un entorno local reproducible con cinco aplicaciones reales: Playmaker, un front RIO vigente y los CP de Kafka, ClickHouse y Flink. Front/Postman entran por las APIs Playmaker; triggers y resultados viajan por Kafka mediante producers/consumers embebidos en cada aplicación. Verificar efectos físicos en motores y estado final de Playmaker/CP. Posteriormente ampliar al resto del ecosistema, sin construir hoy un framework general.

Base fijada por el owner: rio-deployment-trigger-local y rio-deployment-result-local, sin bridge Kafka→HTTP externo ni embebido. Minimizar cambios productivos, conservar contratos y usar Clean, SOLID, KISS y YAGNI para justificar cada pieza nueva. El challenge y el consenso están completos; en el HEAD actual de PM #1286, los siete E2E del stack local pasan. Los flujos de undeploy/DEPROVISION que dependen del comportamiento defectuoso de develop permanecen etiquetados develop-gap (ver bitácora). El alcance posterior conserva CH/Flink/front.

## Estado vigente

- **2026-10-28 — Refview sincronizado y versiones para test:** [[Import de Refreshable Materialized Views externas]] publica los tres merges de develop. CP y front `0.0.4-import-ref-view-ch`, PM `0.0.3-import-ref-view-ch`: las tres FINISHED, CI PASS y registry disponible para el deploy del owner en `test`. Suites locales PASS; sin despliegues ni nueva E2E Lore. [[2026-10-28-refreshable-testing-versions-entity-updated]].

- **2026-10-28 — follow-up de Ale en Flink:** nuevo PR [#221](https://github.com/melisource/fury_rio-controlplane-flink/pull/221), `feature/local-kafka-dlt-readiness` @ `06e073bd` desde `develop` @ `e8755055`. Readiness exige metadata de ambas DLT con límite de dos segundos; fixtures usan los nombres reales. Tests productivos1969/locales101 y hooks PASS, coverage readiness100% líneas/ramas y configuración100% líneas. E2E SQL/invalid/JAR/Python/cross-CP PASS con PM develop `20e0a9109`: Lore13/13 y oráculos23/23; teardown0, sin contenedores/redes RIO ni servidores en los puertos usados. CI, coverage, dependencies, static analyzer, CodeQL y workflow SUCCESS. PR listo para review. [[Descripción PR — rio-controlplane-flink (DLT readiness)]].

- **2026-10-23 — import refview alineado; certificación pendiente:** PM `85f5bad67` sobre base E2E, CP `686d8f7a8` y front `8eaa15827` sobre develop, publicados y drafts conservados. Suites PM5190, CP3973 y front11745 PASS; typecheck heredado123 sigue rojo. Runner y skill incorporan ocho screens y espera del grupo completo con regresiones RED/GREEN; candidatos a #1332. Spellbook vencido y un nuevo `down --volumes` del stack concurrente rechazado automáticamente: autenticación y autorización específicas pendientes. Lore0/12; no hay certificado de import ni teardown final. [[Import de Refreshable Materialized Views externas]], [[2026-10-23-refreshable-import-e2e-alignment]].

- **2026-10-23 — import de refreshable externa, intento detenido en F0:** [[Import de Refreshable Materialized Views externas]] conserva PM `74bcdde08`, CP CH `b2386223` y front `027d9f10c`; puerto 8443 ocupado por un Lore ajeno (PID 62677), preservado. Sin merges, stack ni corridas (0/12); caso y certificación pendientes. [[2026-10-23-refreshable-import-e2e-preflight-entity-updated]].

- **2026-10-23 — PRs de la ronda Flink/front/Lore abiertos, listos para review:** CP Flink [#218](https://github.com/melisource/fury_rio-controlplane-flink/pull/218) (mergear primero) · Playmaker [#1332](https://github.com/melisource/fury_rio-playmaker/pull/1332) · front docs [#824](https://github.com/melisource/fury_ads-signals-frontend/pull/824). Descripciones: [[Descripción PR — rio-controlplane-flink (E2E local Playmaker)]], [[Descripción PR — rio-playmaker (E2E local Flink)]], [[Descripción PR — ads-signals-frontend (RIO ecosistema local)]].

- **2026-10-23 — Ambiente desde cero con un comando:** `.lore/ecosystem/rio-ecosystem setup` clona e instala las seis apps (manifiesto `apps.json` con git path y rama) y `all` corre los 13 casos; validado con workspace vacío: 12 corridas Lore PASS, 48/48 oráculos (PM `bc5e283fe`). El front no cambia código; su README apunta al runbook (rama docs sin push).

- **2026-10-23 — 13 casos de ecosistema certificados:** se suman Run Query, refreshable view, conector Kafka→ClickHouse y un pipeline que cruza Kafka, Flink y ClickHouse en un solo deploy. `rio-ecosystem all` desde cero: 12 corridas Lore PASS y 48/48 oráculos backend (PM `53a3a929a`).

- **2026-10-23 — "corre todos los escenarios de RIO" listo para el equipo:** `.lore/ecosystem/rio-ecosystem all` en el repo de Playmaker levanta el ecosistema local y corre 9 casos (Kafka, ClickHouse con vista materializada, Flink SQL/JAR/Python e inválido), certificados desde cero: Lore 8/8 corridas, 28/28 oráculos backend. Agentes: skills en `.lore/ecosystem/skills/` vía `AGENTS.md`. Detalle en [[RIO E2E local — Integración Flink Playmaker]].

- **2026-10-22 — Lore 5/5 PASS (primer PASS de navegador):** `run_mvkbbsbnec16b25105`, compliance 100%: smoke, Flink SQL deploy y stop/start, tópico Kafka con peek y tabla ClickHouse, contrastados con backend real. Lore sin cambios de código; escenarios y procedimiento en PM `local/lore/` (`3cb35aaef`). Commits locales sin push en PM y CP Flink. Detalle en [[RIO E2E local — Integración Flink Playmaker]].

- **2026-10-22 — journeys de navegador B1–B3 PASS:** `ads-signals-frontend` sin cambios de código opera contra Playmaker local y los tres CP reales (Flink SQL deploy/stop/start con jobs y datos reales, tópico Kafka RF 2 con peek, MergeTree en base creada desde la UI), verificado contra backend. Procedimiento en el hub de PM (`3e76158bf`) y runner SQL local del CP Flink (`da3e33c6`); commits locales sin push. Falta F5 (Lore). Detalle en [[RIO E2E local — Integración Flink Playmaker]].

- **2026-10-22 — integración PM + CP Flink validada por backend:** [[RIO E2E local — Integración Flink Playmaker]] G0–G3 aceptados tras code review independiente (CP Flink `ac019e17`, PM `a66ae3871`, commits locales sin push). Flink entra por APIs de PM con SQL, stop/start, redeploy, JAR, Python y errores; regresión Kafka/ClickHouse PASS; undeploy sigue `develop-gap`. Front y Lore bloqueados por la CA devcert vencida y por un defecto de identidad del diseño (DD-8), pendiente de decisión.

- **2026-10-22 — diseño y plan de la integración PM + CP Flink listos:** [[RIO E2E local — Integración Flink Playmaker]] (proyecto de agente, `ready_for_phase_0`) fija bases frescas CP Flink `920a7075` (#213, con #211/#214) y PM `f1a4b246d` (#1318). El único faltante de transporte es el intake Kafka de actions en el CP Flink; PM no requiere código productivo ni `src/local`. Seis fases con gates: bases/memoria → actions CP Flink → vertical SQL desde APIs PM → matriz + regresión → front → Lore y ensayo de demo. Ruta crítica para la demo: G0 → G1 → G2 → G4 → G5. Sin código ni uso de la VM en esta sesión.

- **2026-10-22 — retoma para demo del 23/10:** owner confirma los tres PRs Flink mergeados; GitHub confirma #211 (`74cc6f96`) y #213 (`920a7075`). Kafka #86 y ClickHouse #342 también mergeados. #214 Flink y #1318 PM mergeados: usar bases develop frescas con esos fixes. La integración PM + Flink sigue pendiente: la guía de develop la excluye y Flink standalone recibe actions por HTTP, mientras PM las publica en Kafka. Completar adapter local de actions y composición con broker compartido; luego certificar APIs PM y efectos físicos, levantar ads-signals-frontend y ejecutar Lore. No se ejecutaron suites en esta retoma. Preflight read-only: colima-rio accesible, sin contenedores activos, 4 CPU/~8 GB RAM; host ~32 GiB libres; shell Node22, Node24 instalado. Front/Kafka/CH originales tienen cambios de otras tareas: aislar checkouts. Lore/browser y TLS siguen pendientes de prueba real.

- **2026-10-21 — CP Flink #213 sincronizado y comentarios corregidos:** `438d2b9b` incorpora #211 @ `6847ab66` y los tres comentarios de revisión de Python/ZIP. 1937 productivos + 53 locales, hooks y E2E físico completo PASS; CI, CodeQL, cobertura, dependencias, análisis estático y workflow SUCCESS. Cleanup 0 contenedores/0 redes rio-*, worktree limpio. #213 listo para revisión y MERGEABLE; detalle en [[CP Flink local]] y [[2026-10-21-flink-pr213-review-comments]].

- **2026-10-20 — CP Flink standalone completo; sigue integración Playmaker:** #209 mergeado (squash `0b60e64b`); #211 @ `91cdd5f8` listo para review y #213 draft @ `e7e12bff`, ambos con E2E físico completo PASS y descripciones publicadas como serie. PM #1286 y #1288 ya están mergeados, así que la integración Playmaker + Flink parte de `develop` con el patrón de ClickHouse. Detalle y contrato en [[CP Flink local]] («Próxima sesión»). [[2026-10-20-flink-pr211-pr213-sync-updated]].

- **2026-10-19 — PM #1288, pipeline verde:** el owner exige pipeline verde. `e0c91cb8e` corrige una carrera de verificación asíncrona en `DeploymentFlowAcceptanceCriteria` que hizo fallar x86 en CI 6321 sobre `5be401023`; ARM había pasado. Fix test-only, mismas aserciones y sin cambio productivo. Hooks PASS; regresión fresca 4889 casos, 0 fallos/errores y 2 skips heredados. [Pipeline 6324](https://rp-ci-java.furycloud.io/blue/organizations/jenkins/rio-playmaker/detail/rio-playmaker/6324/pipeline/) SUCCESS sobre ese SHA; CI, coverage, dependencias, análisis estático y workflow verificados en verde. El comentario de MV resuelto y su evidencia física se conservan; src/main/src/local/src/localIntegrationTest son idénticos a `5be401023`. [[2026-10-19-codex-unknown-rio-e2e-pr1288-mv-actions]].

- **2026-10-19 — PM #1288, comentario de MV atendido:** `feature/rio-e2e-local-clickhouse-kiss` @ `5be401023`, base `develop`. El E2E usa `stop`/`start` y `schema_name`, conserva SQL/estado persistido y no modifica lógica productiva. Sobre el SHA final: ClickHouse 5/5 y subset Kafka 5/5 PASS; cleanup de proyectos/volúmenes/redes/JVM/credenciales certificado. LocalTest 53 y aislamiento PASS; 113 selectores y tres checks L0 PASS. El runner agregado falló en el preflight del cuarto check por puerto ocupado; el check de ecosistema Kafka aislado pasó después de verificar los puertos libres. Formato/Checkstyle/PMD mantienen hallazgos heredados, sin nuevos. [Hilo respondido y resuelto](https://github.com/melisource/fury_rio-playmaker/pull/1288#discussion_r4318283767). [[2026-10-19-codex-unknown-rio-e2e-pr1288-mv-actions]].

- **2026-10-14 — CP Flink #211, alineación y comentarios publicados:** `feature/rio-e2e-local-flink-pr2` @ `39937680`, base `feature/rio-e2e-local-flink-kiss` @ `c0cabe72`. Dos merges normales; SQL UPDATE/CRUD/JAR conservan las regresiones del #209. Gates 1937 productivos + 19 locales y hooks PASS; src/main/src/test vacíos contra base y develop. Tres hilos corregidos, respondidos en español y resueltos. E2E completo PASS en 278b4a1a y cleanup sin contenedores/redes rio-*; el fix final de adjuntos reemplazados 39937680 tiene tests locales verdes y queda pendiente de recertificación física por el límite de tres iteraciones. Descripción del vault/GitHub actualizada. [[CP Flink local]] · [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]] · [[2026-10-14-rio-flink-pr211-alignment-close]].

- **2026-10-14 — verificación navegador con Lore: BLOCKED por ambiente local.** Run `run_mv8ffvfka5316a27a4`: 12 escenarios, 0 passed/0 failed/3 blocked/9 skipped; compliance 0%, gate release=false. Lore arrancó con Node 24.19.0 y Chromium completo; el SDK Claude falló antes de navegar por binario darwin-arm64 ausente. Front develop `66464bfc1` exportado intacto: npm install falló ENOSPC y no inició runtime; checkout original con cinco cambios ajenos preservado. PM/CP Kafka/CP CH iniciaron HTTP 200 sin BeanCurrentlyInCreationException; luego el broker terminó por SyncFailedException. SQL CH 25.8.33.6 confirmó cero tablas/MVs de usuario; PM sin servicios, componentes PENDING_CONFIG. No se certifica ningún journey ni falla de la app. CA MeliDev vencida; alternativa gateway rechazada por revisión automática, no ejecutada. Teardown propio completo y diez puertos cerrados; primera comprobación sin contenedores/redes rio-*. Luego otra sesión creó seis contenedores Flink/Kafka y red rio-local, preservados; limpieza global de la VM no certificada tras espera acotada de cinco minutos (FINAL_GLOBAL_CLEANUP_CHECK_FAILED); debe terminar el teardown de la otra sesión. Bases PM `0dcf4ac8e`, Kafka `ebebb406`, CH `22120ed1`, Lore `e906b959`. [Reporte completo y comandos](/private/tmp/rio-lore-qa-20261014/report.md). [[2026-10-14-codex-unknown-rio-lore-verification]] · [[2026-10-14-rio-lore-verification-session-feedback]]. Próximo: liberar espacio, resolver checkout del front, renovar CA y reparar opcionales de Lore; después repetir E2E. No commits/push/ramas/PR ni cambios de código de esta sesión. Conflicto concurrente en PM local/RIO_E2E.md y cambio local/rio_e2e.py preservados.
- **2026-10-14 — documentation published in five PRs; physical documentation checks pending:** PM #1286 `feature/rio-e2e-local-kafka` @ `1d9ceefd5`; PM #1288 `feature/rio-e2e-local-clickhouse-kiss` @ `35b525454`; Kafka #86 `feature/rio-e2e-local-kafka` @ `aae17bc4b`; ClickHouse #342 `feature/rio-e2e-local-clickhouse-kiss` @ `dc956a081`; Flink #209 `feature/rio-e2e-local-flink-kiss` @ `c0cabe721`. Playmaker `local/RIO_E2E.md` is the integration hub; CP READMEs separate standalone scope from integration and link to it; Spanish general docs retain AT-180-S20/S21 as short pointers, and Kafka specs retain Spanish. Local checks PASS: Kafka62, ClickHouse57, Flink11; Playmaker24/36 cached local tests and executed artifact isolation PASS. Repository validators and Markdown hooks PASS. Literal Kafka startup failed on a broker-name conflict; corrected startup, Flink startup and manual ClickHouse startup fail before mutation with `rio-local is occupied; wait for its owner to finish`. Physical suites/readiness/teardown therefore remain pending; no owned containers or private credentials remain, and other-session resources are preserved. Launcher validation also needs clarification because existing test/stop write automatic receipts/results despite the no-receipts instruction. The testing plan fails because it requires `.testing/impact.json`; that JSON is outside this task. Authored commits change only Markdown; the mandatory stacked merge inherits #1286's existing `local/rio_e2e.py` fix (+2/−1 against #1288's session baseline), with no script delta against the stacked base. All five descriptions are published and all review threads resolved; Flink's new job-ID lookup failure is documented, with code reconciliation pending. Flink #211 is untouched by this session. Next: release the shared VM, resolve the launcher-output constraint, run standalone suites followed by launcher/manual integrations in series, and verify owned teardown. [[2026-10-14-rio-e2e-local-documentation-session-feedback]] · [[2026-10-14-rio-e2e-local-documentation]].
- [[CP Flink local]] concentra el estado y la planificación de los tres PRs del CP Flink local.
- F1 Kafka y F2 ClickHouse KISS mantienen su alcance vigente; integración Playmaker/front posterior según sus entregas.

## 📊 Estado actual

- **2026-10-14 — PR #1286 sincronizado y decoder aislado:** `feature/rio-e2e-local-kafka` @ `2658c298e` incorpora `develop` @ `024564e6d`; GitHub confirma `mergeable=true`. Conflicto en `.testing/impact.json` resuelto conservando ambas ramas. Decoder, listener y configuración se empaquetan sólo en el jar local; regresión 4.807 casos (2 omitidos), localTest 41 y controles LINE/BRANCH ≥95% PASS. Checks de stack pendientes: Docker no disponible en esta ejecución. [Comentario respondido](https://github.com/melisource/fury_rio-playmaker/pull/1286#discussion_r4276204075).

- **Review F1 — 2026-10-13, sesión cerrada:** cinco comentarios aplicables corregidos/publicados/respondidos. PM159ad1fa0 (Java354f9d) corrige lock del primer lookup caller/delegate y save tardío del ledger; CP0b9fa60/fuente65f472f corrige readiness de todos los tópicos e IDs antes de intake. FullPM4820/local23, CP691/62 ycoverage/isolation PASS. Launcher26 con señales/child reales yRED8/10; nuevo contrato26selectors+3L0 PASS ymandatoryL1 reanudado MySQL33308 después de bindpreflight sin recursos: normal2×11/gap2×1, restart real, cleanup exacto0containers/vols/3redes/24images/9ports/statePIDgroupabsent. Challenge fuente/receipts QUALIFIED PASS sin corrida propia. CI6193PM fallóx86 porverify prematuro de@Async; fix test-only903 publicado, focused/full4820local23PASS y CI6196/coverage/deps/static/workflow SUCCESS. Recheckbotd16 agregó4263876597: fixACME sin drain, HEADbody abortantesheaders/EOF, bodylessHEAD405; RED2timeouts yHEAD1timeout, GREENlocal26, sourcepeerQUALIFIEDPASS.Final159: contrato completo outerexit0,27selectors+3L0+launcher26+local26 y nueva física34dc87fd12cf24/24/cleanup exacto;PMjar382139d3/CP7e,source/index/receipts QUALIFIEDPASS. CI6197/coverage/deps/static/workflow SUCCESS; bot final NEUTRAL sin nuevos comentarios/bloqueantes; revisión humana por complejidad. CP553/CodeQLSUCCESS. CodeScanningPMstartup/0jobs separado; patchCIae4 sólo en pending/rio-e2e-local-codeql-runner, sin excepción enviada. CH/Flink preservados. [[2026-10-13-codex-unknown-rio-e2e-local-pr-comments]] · [[2026-10-13-rio-e2e-local-pr-comments-session-feedback]].
- **Continuidad F1:** completar revisión humana de PM1286/CP86 y tomar estos fixes publicados como base al continuar las integraciones locales; PM1288 apilado debe incorporar F1 de forma explícita. Conservar los gates/evidencia por fuente y las entregas ClickHouse/Flink vigentes. [[playmaker-undeploy-lock-first-managed-read]] · [[kafka-local-spring-retry-ack-evidence]] · [[playmaker-local-ledger-publication-signals]] · [[playmaker-local-acme-request-body-drain]].

## 🧱 Entrega de desarrollo

Entrega multirrepo por fases. F1 tiene ramas/bases y SPEC funcional→técnica→tareas antes de código; las otras aplicaciones conservan su estado de discovery. No trasladar cambios sucios.

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] · fury_rio-playmaker | feature/rio-e2e-local-kafka; fix separado feature/rio-e2e-local-deprovision-fix | origin/develop vigente `67cc44792`; merge del transporte resuelto sin commit | repo + meli/features/20261009-rio-e2e-local/1-functional/spec.md | repo + meli/features/20261009-rio-e2e-local/2-technical/spec.md | PR HEAD159ad1fa0 intacto; candidato stageado 50 archivos y siete Java permitidos, test4810/local26/isolation PASS. Fix f21b0a2e0 publicado, sólo nueve Java/test4821 PASS. E2E STOP: rio-local existente; faltan gates físicos, commit/push del PR, respuestas y descripción |
| [[ads-signals-frontend]] · fury_ads-signals-frontend | Integración no creada | origin/develop local a3f82abd8a4756d750b8d3ec86e9065df1fec9a4; remoto 01e19bc sin leer | Journeys B1–B3 en el diseño revisado | Sin código si D4 se resuelve por seed | BLOCKED (D4) |
| [[rio-controlplane-kafka]] · fury_rio-controlplane-kafka | feature/rio-e2e-local-kafka | 6a91937c0664d83f907dec222af8a96b4042c6ae | repo + meli/features/20261009-rio-e2e-local/1-functional/spec.md | repo + meli/features/20261009-rio-e2e-local/2-technical/spec.md | HEAD4e19959: PR #86 publicado, 19 archivos/+1708/−16; `src/main`/`src/test` vacíos; 691+62 `check` PASS, 25/25 `localFunctionalTest` PASS, cleanup completo; ocho hilos respondidos sin resolver; descripción actualizada. [[Descripción PR — rio-controlplane-kafka]] |
| [[rio-controlplane-clickhouse]] · fury_rio-controlplane-clickhouse | feature/rio-e2e-local-clickhouse, worktreeaislado | fetcheddevelop cf17797ef9bc1eb9b9bdb3329e6c70bfc8231386; originaldirty intacto | SPEC F2 C1–C6/A1/X1–X4 abajo | SharedintakeMVC mínimo/Kafkaembebido/motor25.8.33.6/SQLcliente físico | E2E backend soportado y cleanup PASS; C6 API PM/capabilities externas BLOCKED, F4 NO_EJECUTADO |
| [[rio-controlplane-flink]] · fury_rio-controlplane-flink | Standalone listo (#209 mergeado, #211, #213); integración Playmaker no creada | origin/develop local7c645ea92f86650744a3c5ee1bad0012633ef0e9;1 cambio ajeno | Escenarios a descubrir | Cloud Controller/runtime a verificar | Seam local por demostrar |

### Entregables F2 ClickHouse vigentes

SPEC consolidada de revisión: [[RIO E2E local — SPEC F2 ClickHouse]]. Incluye referencias recuperadas, contrato por caso, PLAN técnico y TASKS READY por repo; las SPEC enlazadas en la tabla conservan la autoridad y deltas de implementación.

SDD funcional → técnica/PLAN → TASKS READY precedió la implementación en los tres repos. Estas SPEC concretas son la autoridad del alcance F2; el borrador posterior corresponde al macroproyecto de cinco apps.

| Repo | Rama / candidato | SPEC funcional | SPEC técnica y PLAN | TASKS |
|---|---|---|---|---|
| PM | feature/rio-e2e-local-clickhouse · HEADf0cac94f (fuente c5cc53e0; E2E/cleanup PASS) | [spec](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md) | [plan](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md) | [ready](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |
| ClickHouse | feature/rio-e2e-local-clickhouse · HEAD61b63808 (fuente 8ab2961d; E2E/cleanup PASS) | [spec](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md) | [plan](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md) | [ready](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |
| Kafka | feature/rio-e2e-local-clickhouse-regression · HEADf8fe7671 (fuente 28428ff4; F1+F2/standalone PASS) | [spec](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md) | [plan](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md) | [ready](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |

Gates root: contrato canónico, ocho matrices físicas, fault9/native52/critical7 y Kafka standalone PASS; collectors privados con FAIL preservados y reconciliaciones independientes. Cleanup root y del primer clone bootstrap fallido conservan baseline exacto. Reproducción limpia660431b713e7: FAIL unhealthy antes de tests, causa NO_AISLADA. Corrección mínima8ab2961d incluye init público en imagen del motor (dos archivos CH, CPstage intacto); VERIFY estático PASS. Reproducción independiente del nuevo Compose PASS: cuatro normales y cuatro gaps en cuatro stacks nuevos, 104 ejecuciones exactas/0FES. Manifest ebb133f2 conserva3136files; matrices independientes56993045, motores/cleanup45fbb366, baseline actualfullmetadata6430d371 y externalsb151d252 PASS. 2808PID/1116PGID originales+observadores ausentes inclZ/0SIG;14IDs propios retirados/23rmi exactos,24baselineRootFS/3redes intactos,0containersvolumes/puertos libres/statecredsausentes. SOURCE_RELEASE es aditivo, resultado sellado intacto. Commits finales f0cac94f/61b63808/f8fe7671 sólo ocho archivos existentes; clones exactos limpios y fuentes/jars invariantes. [Reproducir](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/local/RIO_E2E.md); [matriz actual](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/4-implementation/VERIFICATION.md). C6 PM UPDATE literal BLOCKED_no_API, capabilities externas ausentes y Code Scanning remoto startup_failure conservados. No PR/merge/deploy ni certificación browser implícitos.

### SPEC funcional — borrador

1. Levantar simultáneamente las cinco aplicaciones y los motores/dependencias locales necesarios. Cinco aplicaciones no significa cinco contenedores: Kafka, MySQL, ClickHouse y runtime Flink son infraestructura adicional.
2. Requests desde APIs Playmaker y journeys del front elegido, con triggers SDK reales, procesamiento CP real y resultados reales. No fabricar COMPLETED ni sustituir provisioning/SQL/jobs/lifecycle por fixtures.
3. Matriz por CP/caso: endpoint vigente, tipo de componente, operación/action soportada, trigger, resultado CP, estado PM, efecto físico y fronteras sustituidas. No asumir que los tres CP soportan las mismas operaciones.
4. Errores iniciales/propagados, duplicados/replays/orden y deadlines según contratos. Separar PASS/FAIL/BLOCKED/NO_EJECUTADO y E2E backend de browser. HTTP200 y ACK Kafka son recepción, no estado terminal.
5. Comandos pequeños de arranque/pruebas/limpieza, rutas arbitrarias/con espacios, recursos propios identificados y aislamiento. Repetir dos veces sobre ambiente vivo, recrear vacío y reproducir desde clones limpios. No suites concurrentes contra el mismo ambiente.

### SPEC técnica — estado objetivo

Estado objetivo, contratos, inventario por repo, secuencias ACK/error/replay, matriz E2E y decisiones abiertas en [[RIO E2E local — Diseño revisado]]. Resumen:

- Un broker, dueño Compose CP Kafka, red `rio-local`; Playmaker y front en host (PM contra `127.0.0.1:39092` por `LocalKafkaBootstrapGuard`), CPs/ClickHouse/MySQL en la VM. Puertos: PM39080, CP Kafka39081, CP ClickHouse39082, CP Flink39083, broker39092, ClickHouse HTTP39123, MySQL33306, front8443.
- Tópicos `rio-deployment-trigger-local` y `rio-deployment-result-local`, una partición, key `deployment_id`, payload SDK crudo; un group por CP; DLT por CP con la política de reintento ya usada por PM; observer con `assign()` sin group.
- Entrada CP: adapter local A que invoca el handler del controller sólo si demuestra paridad HTTP↔Kafka, incluidos binding, validación, filtros y errores; B con refactor estructural mínimo donde A no los conserve limpiamente. Commit tras aceptación; no equivale a operación terminada. Salida CP: `BigQueueClient` Kafka bajo el publisher productivo.
- Se conservan contratos, guards, idempotencia y gaps productivos (publisher CP Kafka, GCP PEEK). Sin bridge, librería común ni broker de PM. Runtime Flink, seam y dimensionamiento por demostrar; Flink físico permanece en el criterio final.

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

No se crearon subproyectos persistentes de ejecución delegada. SDD delegó implementación y revisión independiente de F1 con bases/SPEC antes de código; la entrega y continuidad permanecen en este proyecto.

## ✅ Tareas

- [r] [[RIO E2E local — Integración Flink Playmaker]] arrancar + seguimiento #owner/me #type/supervision #area/meli
- [x] Publicar dos PRs con descripciones técnicas y nueva recertificación de auth upstream #owner/agent #type/dev #area/meli
- [ ] Resolver CodeQL Playmaker y acreditar ambos PRs verdes sin bypass #owner/agent #type/test #area/meli
- [x] Preparar dos prompts maestros alineados con F1 y decisión N CPs #owner/agent #type/dev #area/meli

- [x] Simplificar F1 según review Claude, documentar contra-challenges y verificar por otro agente #owner/agent #type/dev #area/meli
- [x] Recertificar fuentes simplificadas: regresiones/cobertura, normal con presupuesto productivo, matriz completa repetida y reproducción limpia independiente #owner/agent #type/test #area/meli

- [x] Implementar F1 Playmaker + CP Kafka con transporte Kafka embebido; conservar originales y extraer fix DEPROVISION en rama propia #owner/agent #type/dev #area/meli
- [x] Verificar K1–K6/X2–X4/A2, standalone25, regresiones y limpieza propia; repetir ambiente vivo y recreación vacía #owner/agent #type/test #area/meli
- [x] Verificación independiente y corrección/gate final de F1 #owner/agent #type/test #area/meli

- [x] Ejecutar [[Prompt — Challenge del diseño RIO E2E local]] y revisar findings #owner/me #type/research #area/meli
- [x] Acordar D1–D6 de [[RIO E2E local — Diseño revisado]] #owner/me #type/dev #area/meli
- [ ] Autorizar fetch y releer deltas remotos de CH, Flink y front #owner/me #type/research #area/meli
- [ ] Spike de sólo lectura del seam físico mínimo de Flink #owner/me #type/research #area/meli
- [x] Preparar rama propia del fix DEPROVISION como dependencia explícita de la integración #owner/me #type/dev #area/meli
- [x] Aprobar diseño revisado y registrar ramas/bases/SPEC/tareas por repo F1 #owner/me #type/dev #area/meli

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

- **2026-10-23 — refview certificado:** cinco casos ClickHouse, 13 escenarios Lore y 23 oráculos PASS desde cero; teardown cero. Nuevo import externo, fixes CP/front y Lore #21; screens/fixtures/oráculos candidatos a #1332. PM 0cec5e7c5, CP 1a39e420, front cdcb115e6. [[Import de Refreshable Materialized Views externas]].



- **2026-10-14 — CP Flink #211:** fixes y alineación publicados en 39937680; física final del último fix pendiente, continuidad en [[CP Flink local]] y [[2026-10-14-rio-flink-pr211-alignment-close]].

- **2026-10-14 — verificación final (Claude Code):** reviews de los agentes contrastadas contra repo y GitHub; 48 hilos resueltos, últimos fixes de docs/launcher publicados, cinco suites físicas PASS en serie, rama del fix de undeploy borrada, nota [[lore]] creada. [[2026-10-14-rio-e2e-local-final-verification-session-feedback]].

- **2026-10-14 — cierre de comentarios de los cinco PRs:** cuatro ramas publicadas, diez hilos respondidos/resueltos, cinco descripciones y re-review CH; gates Java verdes, fuentes productivas preservadas. Física pendiente por preflight real de recursos ajenos; cierre y feedback por delta. [[2026-10-14-rio-e2e-local-five-pr-comments-close]] · [[2026-10-14-rio-e2e-local-five-pr-comments-session-feedback]].

- **2026-10-14 — CP Flink #209:** merge y fixes publicados en la rama existente; cierre/serialización, suite reducida, docs en inglés y E2E normal/error PASS; seis respuestas y descripción publicados. [[2026-10-14-rio-flink-kiss-pr209-close]] · [[2026-10-14-rio-flink-kiss-pr209-session-feedback]].

- **2026-10-14 — CP Kafka #86, feedback publicado:** `4e1995907f79acc921ba50fbd2066ac459f89b03` en `feature/rio-e2e-local-kafka`; diff 19/+1708/−16 vs `develop`, `src/main`/`src/test` vacíos. `check` 691+62 y físico 25/25 PASS; cleanup Compose completo. Ocho hilos de dmuena respondidos, otros hilos permanecen abiertos y sin resolver, descripción del PR actualizada. [[Descripción PR — rio-controlplane-kafka]] · [[2026-10-14-rio-controlplane-kafka-review-change-log]] · [[2026-10-14-rio-controlplane-kafka-review-session-feedback]].

- **2026-10-14 — PM #1288, alineación local y fixture ClickHouse:** merge normal `b533e1d39` sobre base corregida `b3554c7f0`, cero delta productivo propio, 4811+33 tests y E2E ClickHouse 5/5 PASS. Runtime MV stop/start verificado; cleanup completo. README CH `16f3e575`; ambos commits publicados con push normal después de los rechazos iniciales por allowlist. Dos respuestas y descripción publicadas; cierre y feedback por delta. [[Descripción PR — rio-playmaker (E2E local ClickHouse)]].

- **2026-10-14 — CH #342, cierre local sin delta productivo:** reverts 8444e4ad/c82658f2/525fc806 integrados con develop y publicados con merge a0be8288; proxy y README publicados en d064c280. Gates Java 2549+57 PASS; E2E final 5/5 con PM 312963ba0, con límites de baseline y runtime status documentados; cleanup del stack completo. Cinco respuestas en cuatro hilos y cuerpo del PR actualizados. [[2026-10-14-rio-clickhouse-kiss-pr342-close]] · [[2026-10-14-rio-clickhouse-kiss-pr342-session-feedback]].

- **2026-10-14 — PM #1286, E2E y simplificaciones de review:** commit b3554c7f054553270151970e72154f34f2efbd15 en feature/rio-e2e-local-kafka, push normal exitoso. Diff neto 50 archivos/+4540/−83; src/main y src/test conservan exactamente los mismos siete archivos. ./gradlew test y ./gradlew localTest verifyLocalArtifactIsolation PASS; launcher 27/27 y E2E local 7/7 PASS con teardown CLEANUP_CERTIFIED. Cuatro hilos de dmuena respondidos con el SHA nuevo; descripción del PR actualizada. Hallazgo: en develop, undeploy por bus no completa; DeploymentResultHandlerImpl descarta resultados DEPROVISION con already_terminal o terminal_component_run. Fuera del PR y pendiente de ticket del owner; la clase de undeploy y los dos casos de DEPROVISION quedan develop-gap. [[RIO Playmaker — develop descarta resultados de DEPROVISION por bus]] · [[Descripción PR — rio-playmaker]] · Feedback: [[2026-10-14-rio-e2e-local-pr1286-session-feedback]].

- **2026-10-14 — PM #1286, implementación local y review:** merge con `develop` y correcciones locales publicados en la rama existente `feature/rio-e2e-local-kafka`; HEAD `d73200b3f4787bdc80f7abecc39a1e89e5681ba2`, diff `50 files, +4759/-82`, exactamente siete archivos distintos en `src/main`/`src/test`; lógica de negocio coincide con `develop`. `./gradlew test` (4811 tests; 0 failures/errors, 2 skips heredados) y `./gradlew localTest verifyLocalArtifactIsolation` (25 tests; aislamiento PASS) verdes. 26 hilos inspeccionados/respondidos, sin resolver hilos ajenos; descripción del PR actualizada. L1 físico: 11 tests, 1 PASS/10 FAIL (resultados de deploy siguen `requested`, errores de fixture cleanup y timeout DLT); `stop` certificó cleanup. No se aplicó `develop-gap` porque no falló únicamente undeploy. Feedback: [[2026-10-14-rio-e2e-local-pr1286-session-feedback]].

- **2026-10-13 — PM #1286, separación de lógica productiva:** fix publicado en rama propia `f21b0a2e0`; candidato reducido a 50 archivos stageado y gates Java verdes. E2E rechazado por red `rio-local` existente; STOP, merge del PR sin commit y publicación/hilos/descripción pendientes.

- **2026-10-13 — CH #342, implementación local sin cambios productivos:** detenida en fetch por IP allow list, también en el reintento posterior a la conexión de VPN informada por el owner. Sin reverts, commits, push, respuestas, edición del PR ni ejecución del stack; cierre por delta en esta nota y log existente.

- **2026-10-13 — cierre de review F1:** PM1286@159ad1fa0 y CP86@0b9fa60: cinco comentarios corregidos/publicados/respondidos; CI6197/553 verde, CPCodeQLSUCCESS, bot final sin nuevos hallazgos/revisión humana. Nuevo contrato27+3L0+launcher26+local26 y física24/24/cleanup exacto PASS. CodeScanning PM separado; sin excepción enviada. Feedback/continuidad en [[2026-10-13-rio-e2e-local-pr-comments-session-feedback]] y [[2026-10-13-codex-unknown-rio-e2e-local-pr-comments]].

- **2026-10-13 — PR CP Flink local:** descripción de `feature/rio-e2e-local-flink-kiss` contra `develop` en [[Descripción PR — rio-controlplane-flink (E2E local)]]; [PR #209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209) listo para revisión. Comparación sin multicaster y cleanup completos; cierre [[2026-10-13-rio-flink-local-pr-session-close]].

- **2026-10-09 — publicación solicitada:** PR Kafka86 verde y PM1286 publicado; fuente PM integrada con auth vigente, gates y nueva reproducción física independiente PASS. CodeQL PMstartup_failure pendiente de diagnóstico/aprobación de patch acotado. Dos prompts y feedback/continuidad persistidos; registro [[2026-10-09-codex-unknown-rio-e2e-local-pr-publication]].

- **2026-10-09 — iteración posterior:** review Claude challengeada, simplificación y regresiones permanentes implementadas; fuentes90df/b0 y nueva recertificación root+independiente completa en contexto saludable. Normal11/gap1 separadas, cada una cuatro corridas nuevas PASS; jars reconstruidos idénticos, cobertura independiente y limpieza de nuevos stacks PASS. VM original offline/cleanup36868 no certificado y ledger privado preservado explícitamente. Sesión y macroproyecto siguen activos. [[2026-10-09-rio-e2e-local-f1-implementation]] y [[2026-10-09-codex-unknown-rio-e2e-local-f1-simplification]].

- **2026-10-09** — F1 implementada y certificada siguiendo el diseño: transporte Kafka embebido reemplaza el camino HTTP; dependencia DEPROVISION separada, originales preservados. Gates productivos/locales/contrato y standalone25 PASS; seis suites físicas 12/12 en repetición, recreación vacía y reproducción independiente. Findings de ownership/interrupción/bytes/fixture corregidos y promovidos a regresiones. Fuentes PM 2f4a0a2 / CP 581e234; entregas Markdown PM c03b950 / CP 6832c70. Jars coinciden por hash; limpieza certificada sin afectar recursos ajenos ni filtrar credenciales. Checkouts permanentes en fuentes; sesión/proyecto activos para fases posteriores. [[2026-10-09-rio-e2e-local-f1-implementation]] y [[2026-10-09-codex-unknown-rio-e2e-local-f1]].

- **2026-10-09** — Review cruzada de F1 por Claude Code (Opus 5.5) y refactor de simplificación de Codex (PM `ccc43d0d5`, CPK `90710a5`): listener CP sobre Spring Kafka, `LocalClusterMapping` eliminado, tópicos desde el runner, transporte PM unificado, suite E2E dividida y caso K6 como `test-gap`. Claude aprueba F1. Para F4 (front) quedan pendientes: token `local-e2e`, team del fixture, entity-service y el payload `aws-msk-topic` del front. [[2026-10-09-claude-code-claude-opus-5-5-rio-e2e-local-f1-review]].
- **2026-10-08** — Proyecto y prompt creados desde templates canónicos. Identidad local de repos leída sin fetch. Challenge e implementación pendientes. [[2026-10-08-rio-e2e-local-created]].
- **2026-10-09** — Challenge ejecutado con discovery de sólo lectura sobre refs git de los cinco repos; diseño revisado entregado, front elegido y seis decisiones abiertas. Sin código, fetch, Docker ni VM. [[2026-10-09-rio-e2e-local-design-challenge]].
- **2026-10-09** — Segunda revisión cruzada aceptada: alcance final completo (Flink físico y journeys con actions), A condicionada a demostrar paridad por pruebas, timeout como detección y readiness explícita. Mismo change log.
- **2026-10-09** — Sesión cerrada por pedido explícito. Continuidad guardada en esta nota, feedback propio en [[2026-10-09-rio-e2e-local-consenso-session-feedback]] y revisión atribuible en [[2026-10-09-codex-unknown-rio-e2e-local-design-review]]. [[2026-10-09-rio-e2e-local-session-close]].

## 🧭 Decisiones

- **2026-10-14 — Hallazgo para el owner:** `OnPremiseClickHouseClient` de develop envía `format=`, rechazado por ClickHouse con `UNKNOWN_SETTING` en todas las versiones probadas (22.8, 23.3, 23.8, 24.3, 24.8 y 25.8). La URL productiva se resuelve desde `endpoint-pattern`; existe un posible bug productivo si ese endpoint no pasa por un gateway que traduzca el parámetro. Verificar la topología productiva y tratarlo en un cambio aparte; este PR conserva el código productivo.

- Owner fija cinco apps iniciales y crecimiento posterior. Producers/consumers Kafka sin bridge es requisito; producción se toca sólo ante necesidad demostrada y mediante cambio mínimo que conserve contratos.
- Front del alcance: [[ads-signals-frontend]]; [[rio-frontend]] fuera por estar acotado a ambientes legacy.
- D1–D6 acordadas en [[RIO E2E local — Diseño revisado]]: A condicionada a paridad HTTP↔Kafka (B donde no alcance), Flink físico en el criterio final, actions de los journeys dentro del alcance, fixtures mínimos de referencia, extracción selectiva desde LOCAL-HTTP-2 y versión ClickHouse fijada por pruebas físicas. F1 autorizada por el pedido actual del owner; CH/Flink/front permanecen posteriores.
- Iniciativa raíz independiente de [[Kafka — Ambiente local con servicios reales]], que conserva evidencias y ramas específicas. El cierre anterior del 09/10 se conserva como antecedente; revisión F1 del13/10 cerrada con cinco comentarios corregidos/respondidos, CI y nueva física certificadas; fases posteriores conservadas.

- **2026-10-09 — Owner tras review cruzada Claude↔Codex de F1:** prioridad única = todo funcionando local para E2E desde el front, KISS/YAGNI y sin tocar código productivo en lo posible. La versión de librerías en classpath locales (p. ej. `kafka-clients` 4.2.1 del CP vs 3.9.2 productivo) es irrelevante mientras levante. Regla F2: el runner se generaliza a N CPs al sumar ClickHouse, no se copia.

## 🔗 Docs / Links

- [[Descripción PR — rio-playmaker (E2E local Flink)]] — PM `feature/rio-e2e-local-flink` @ `bbe14b2c8`, base `develop` @ `ca4fe6bef` (sincronizada; escenarios Lore en `.lore/ecosystem/`).
- [[Descripción PR — rio-controlplane-flink (E2E local Playmaker)]] — CP Flink `feature/rio-e2e-local-flink-playmaker` @ `da3e33c6`, base `develop` @ `920a7075`.
- [[Descripción PR — rio-controlplane-kafka]] — CP Kafka #86, HEAD `4e19959`, rama `feature/rio-e2e-local-kafka`, base `develop`.
- [[Descripción PR — rio-controlplane-clickhouse (E2E local)]] — entrega local vigente, CH #342, HEAD `d064c280`; sin diferencias en `src/main`/`src/test` respecto de develop.
- [[Descripción PR — rio-playmaker (E2E local ClickHouse)]] — PM #1288 sobre #1286; HEAD publicado y verificado `b533e1d39`.
- [[Descripción PR — rio-controlplane-flink (E2E local)]] — cuerpo publicado en PR #209.

- [[RIO E2E local — Diseño revisado]] — estado objetivo, contratos, inventario, matriz E2E y decisiones abiertas.
- [[Prompt — Challenge del diseño RIO E2E local]] — prompt autocontenido, sólo diseño.
- [[Kafka — Ambiente local con servicios reales]] — antecedente técnico/evidencia de alcance anterior.
- [[Ambientes locales RIO — Comparativa de implementaciones]] — investigación histórica, no contratos vigentes sin reverificar.
- [[rio-playmaker]], [[ads-signals-frontend]], [[rio-frontend]], [[rio-controlplane-kafka]], [[rio-controlplane-clickhouse]], [[rio-controlplane-flink]].

## 💡 Ideas

### Backlog de ideas

- Incorporar otros CP/materializer/servicios después de demostrar el patrón con estas cinco apps; no construir ahora un framework E2E general.

### Motivos / principios

- Clean/SOLID para separar transporte y negocio; KISS para operación local; YAGNI para limitar dependencias/abstracciones. Cada pieza nueva debe resolver una necesidad comprobada.

### Memoria pública / interna

- **Memoria pública:** contratos y decisiones verificadas enlazados desde esta nota.
- **Memoria interna:** journal de creation/discovery, sin duplicar el estado operativo en memorias generales.
- **Motivo:** separar propuesta vigente, evidencia histórica e implementación futura.


## F2 FULL local — ampliación vigente del owner (2026-10-10)

El owner pidió terminar todos los flujos ClickHouse que existen en RIO, con implementación local transparente. La aceptación anterior de104ejecuciones conserva su subset y cleanup; no acredita este nuevo catálogo completo. Trabajo actual: transporte de runtime-status/eventos/cleanup scheduled bajo publishers productivos, routing local del conector, autorización fixture con project/grants reales y motor25.8.33.6 con Keeper/ON CLUSTER y backend de objetos local compatible. Se reutilizan las SPEC/PLAN/TASKS/VERIFICATION existentes; ningún nuevo reporte permanente ni framework. Operaciones inexistentes, callbacks exitosos ficticios y desactivar guards siguen fuera.

Bases de trabajo PMf0cac94f / CH61b63808 / Kafka f8fe7671, ramas existentes aisladas. Fetch nuevo de los tres repos terminó128 por IP allowlist de GitHub; el gate de refs remotas frescas está BLOCKED, siguiente paso concreto habilitar acceso corporativo autorizado y recuperar/leer delta antes de certificar vigencia remota. No usar ls-remote como lectura ni evadir la restricción.

Root mantiene autoridad exclusiva del contexto sano colima-rio-kafka-e2e-01a0f8e0. Baseline nuevo leído: daemon273d8c36,24imágenes/3redes/0containers/0volúmenes; evidencia privada /private/tmp/rio-clickhouse-full-20261010/baseline.json SHA02efa44b5a8945e411bbe500815e9d7c8b83d0a31aa9ffe02dd5023d2ba03fda. No runtime FULL iniciado todavía. Implementadores CH/PM tienen límites de escritura y builddir separados; verificador sólo lectura/candidato congelado. F1 y sus límites se conservan; KVS por JVM/KMS local/corporateauth/version parity/externalAOC-security-SDD tienen sus fronteras explícitas. F4/cincoapps y VM originaloffline36868 no se recalifican; AGENTS OS permanece abierto.


## F2 FULL local — continuidad vigente 2026-10-11

La ampliación FULL todavía no está certificada. El transporte local usa handlers, validaciones, guards y publishers productivos para las operaciones soportadas por Rio. La última suite física FULL13f93f2d092d terminó exit1: catálogo31 exacto,24PASS/7FAIL/0errors/skips. Las correcciones posteriores de oráculo SHOW CREATE y parser compartido tienen VERIFY Java independiente; no convierten esa ejecución en PASS ni reemplazan la física pendiente.

VERIFY actual: CP ClickHouse2753producto fresh+108local fresh/0FES, receipt5d2375e6 y30classIDs/exec/XML exactos, cada clase crítica definida>=95líneas/ramas; PM toolkit47 fresh/0FES y producto4873(2skips heredados)/local36 UP_TO_DATE exactos, receipt8b373f75. Jars congelados: PMprod9c933696/local895171c9, CHprodde87e687/local8c4ba179; Kafka sin cambios del delta FULL. Gates normal/repetición/recreación, gap15separado, fault9/helperswhole95 actuales, contrato canónico S20/S21 y reproducción exclusiva de clones limpios con espacios siguen BLOCKED/NO_EJECUTADO. Los tres contratos estáticos/plan PM sí terminaron0; --plan no es ejecución del E2E.

Bloqueo inmediato: revisión automática rechazó dos veces la ampliación de TABLE ENGINE Kafka/S3/IcebergS3 y READ ON REMOTE al usuario efímero CP propio y exige autorización humana específica, todavía pendiente. [Propuesta concreta de dos archivos](/private/tmp/rio-clickhouse-full-20261010/bootstrap-owned-engine-capability-review/candidate.patch) SHAcae7cdbd preparada, no aplicada; bootstrap2f75d195/teste8c90df6 intactos. READ ON REMOTE permite consultas distribuidas; su suficiencia conjunta requiere prueba física. No usar grants globales de datos, credenciales admin, stubs de negocio o desactivar validaciones.

Cleanup del trabajo actual terminado: stop propio13f93/credenciales-state ausentes y17buildimages retiradas; las dos descargas propias también fueron retiradas por IDs capturados. Receipta31b8195 en `/private/tmp/rio-clickhouse-full-20261010/final-permission-block-exact-owned-pulls-cleanup.json`:24imágenes baseline original con sus campos/RootFS y3redes preservados,0containers/volumes/23barebinds libres. Comparación por esquema: un Variant originalmente ausente se normaliza a null, sin pérdida de campos originales; no claim JSON byteidéntico. Cierre externo114c238b: cuatro originales/grupos de cleanup/contratos ausentes incluyendoZ/0SIG. Contexto global colima intacto; daemon sano273d8c36 explícito. Freshstart posterior NO_EJECUTADO: siguiente run necesita pulls propios nuevos acreditados y preflight actualizado. VM originaloffline yledger36868 intocados/cleanup originalNO_CERTIFICADO.

Ramas aisladas reviewables con delta staged, sin commits FULL nuevos: PMfeature/rio-e2e-local-clickhouse HEADf0cac94f/tree8a2f3f91 (36archivosvsHEAD), CHmisma rama HEAD61b63808/treec2330ef8 (35vsHEAD), Kafkafeature/rio-e2e-local-clickhouse-regression HEADf8fe7671 limpio/0delta. No commit sin contrato canónico real exigido por AGENTS; no bypass. Refs actuales GitHub siguen BLOCKED allowlistIP, CodeQL remoto startup_failure y capacidades externas/SDDcanónicas ausentes conservan estado. No PR/push/merge/deploy, F4 ni certificación de cincoapps. AGENTS OS permanece abierto.

Detalle actual: [VERIFICATION PM](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/4-implementation/VERIFICATION.md), [VERIFICATION CH](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/4-implementation/VERIFICATION.md) y [[2026-10-10-codex-unknown-rio-e2e-f2-clickhouse]]. Próximo paso concreto: respuesta humana a las cuatro capacidades→aplicar propuesta/VERIFY afectado→fresh preflight→gates físicos completos y reproducción independiente→cleanup final propio.

## F2 ClickHouse KISS — vigente (2026-10-12)

Reinicio KISS sobre el patrón del F1 Kafka (16 archivos). E2E físico PASS con PM + CP Kafka + CP ClickHouse + motor 25.8.33.6 en VM `colima-rio`: deploy MergeTree, action de lectura, MV describe/stop/start, refreshable PROVISION, conector Kafka→ClickHouse con filas reales, undeploy/cleanup; regresión CP Kafka 25 tests y PM F1 9 tests.

- **CH — actualizado 2026-10-14:** `feature/rio-e2e-local-clickhouse-kiss` HEAD `d064c280`: 14 archivos/+2002/−0 vs `origin/develop` 6ad1d574, sin delta en `src/main`/`src/test`. Compatibilidad HTTP sólo mediante proxy local `nginx:1.28-alpine`, motor `25.8.33.6` y usuario SQL `rio_cp`; validación y límites en «Estado vigente». https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/342 · [[Descripción PR — rio-controlplane-clickhouse (E2E local)]]
- **PM** `feature/rio-e2e-local-clickhouse-kiss`: HEAD publicado `b533e1d39` sobre base corregida `b3554c7f0`; 11 archivos/+867/−6 y cero delta en `src/main`/`src/test`; Java/local/E2E ClickHouse PASS; push normal confirmado. PR apilado sobre #1286. https://github.com/melisource/fury_rio-playmaker/pull/1288 · [[Descripción PR — rio-playmaker (E2E local ClickHouse)]]
- **CP Kafka:** sin cambios.
- **Alcance aceptado por el owner:** refreshable sólo PROVISION (es lo desarrollado en develop); destinos S3/Iceberg del conector fuera (están en master pero el front no los expone; requerirían MinIO); bug latente de develop `CredentialGenerator` sin dígito garantizado vs `PasswordValidator` (~0,4% de creaciones read-only) no se toca.
- **Próximo paso:** probar `ads-signals-frontend` con `PLAYMAKER_BASE_URL=http://localhost:8081` (riesgos: grants del fixture ACME para el usuario real, entity-service remoto, catálogo sembrado).
