# Tasks — kafka-real-e2e

La planificación/estado vive en el proyecto Kafka — Ambiente local con servicios reales de AGENTS OS. Esta tabla define slices y gate por archivo; no es un segundo planner.

| ID | RF/CA | Owner | Scope | Gate |
|---|---|---|---|---|
| T1 | RF-1,CA-1 | Dominio | coverage-matrix.tsv + domain-inventory.md | inventario exhaustivo con SHA y scenarios OK/falla |
| T2 | RF-2–5/8/10 | Infraestructura | e2e/ + adapters reale2e + seams GCP/KVS/BigQ | cinco brokers saludables, cliente real, no fallback, conexiones sin mocks |
| T3 | RF-2–5,CA-2/3 | Dominio | src/realIntegrationTest scenarios + bugs provisioner | efecto Kafka, eventos, KVS y fallas controladas con cleanup |
| T4 | RF-6,CA-4 | Infraestructura/coordinador | adapters Playmaker + src/e2eTest | solicitud y estado MySQL real, DTO wire compatibles |
| T5 | RF-7/8/10,CA-6 | Infraestructura/coordinador | managed suite/CI | runner real o bloqueo explícito; falta dependencia falla |
| T6 | RF-9,CA-7 | Knowledge | KL docs/contratos/manifest/runbook | claims canónicos auditados y validadores verdes |
| T7 | CA-1–7 | Verificador independiente | clean checkout sin editar durante review | suite completa y fallas críticas, repetición y cleanup |
| T8 | CA-1 | Coordinador | evidencia/matriz + proyecto | informe PASS/FAIL/BLOCKED/NOT_EXECUTED y continuidad |

Gates externos pendientes: sesión Spellbook para SPEC/tareas SIG; permiso de clonación KVS Sandbox propio (HTTP403 con auth200); credenciales/recursos administrados; runner Docker/red corporativa. Ninguno se cuenta éxito por código escrito.

- T9 · RF-5/7: root único escritor SDK ProducerFactory/BigQueueClientImpl/regressions; reviewer distinto verifica. Nueva rama master ad2c98b8; sin publicar releases. Registrar artifact efectivo y bloqueo de adopción/BigQueue hasta ejecución real.

- T10 · RF-2/4/5/8: fault_controls implementa infra propia de denegación Kafka, brokers reducidos y proxy HTTP/TCP real; domain implementa escenarios. Root integra SPEC/build, reviewer reproduce sin editar. Ningún mock/no-op ni servicio compartido como fallback.

- T11 [IN_PROGRESS] Coordinator src/e2eTest/playmaker: redeploy PROVISION/reconcile, Service PEEK real/validación, propagación de errores Action y malformed-input DLT Kafka real. Domain actualiza mappings preparados; reviewer independiente reproduce tras gates reales. No ampliar certifiación managed.

- T12 [IN_PROGRESS] Coordinator e2e/sandbox.py + integración launcher: lifecycle Fury Sandbox propio por corrida, exports0600, provenance y cleanup verificado; evita claves globales en sandbox compartido. Basado en rutas CLI primarias; auth200 y BC create/delete parciales ejecutados, clone403 bloquea instancia/config/KVS de ambas apps.

- T13 [IN_PROGRESS] Fault_controls: proxy de frames Kafka y broker propio con advertised listener proxy; domain: carreras/deadlines por API/topic exactos. Reviewer separado reproduce. Root: SPEC y gate de ownership Sandbox estricto (findings P1/P2).

- T14 [READY] Infra: Application real managed, escenarios OAuth Kafka→KVS→BigQueue y observer estricto; callback CP/PM separado. Root registra APIs/templates200 y SDKcleanup primario; las ejecuciones y lifecycle real siguen gates externos.

- T15 [IN_PROGRESS] Domain: timeout físico de reassignment mediante throttling en cinco brokers propios, snapshot/restauración exactos y mensajes reales16MiB; regression oracle Kafka/KVS/result, peer reproduce.

- T16 [IN_PROGRESS] Domain:6 interrupciones físicas de worker propio, focused-service PARTIAL y frontera HTTP/guard/publishing explícita; no normalizar flags ni errores.

- T17 [READY_SOURCE_NOT_EXECUTED] Domain: cleanup KVS selectivo real y grupo explícito UUID para JVM hija; todos los retiros independientes conservan FAIL.
- T18 [SOURCE_L0_PASS] Root: launcher managed/Sandbox full exports/exclusive run/SCP/gates, regressions5+10+8; peer reprodujo clean y detectó duplicate resources, corregido por setSrcDirs. Quiescence managed sigue en corrección.
- T19 [PASS_PARTIAL_CONFIGDATA_ONLY] Domain: ConfigData/Binder reales para8 mappings; root task profileConfigDataTest separada, no certificado de arranque/clientes.
- T20 [SOURCE_L0_PASS_RUNTIME_BLOCKED] Root/domain: observación pasiva local del executor productivo y commit offsets del bridge real antes de cleanup; unit5+4 independent PASS; journal/namespace source+11 gate controls peer PASS; parent46/UNKNOWN negatives independent PASS; all-family compile+ConfigData15 PASS; CP/KVS física pendiente.

Checkpoint: CP712unit PASS/0skip; PM4386 con2 skips baseline independientes, stagedfocused8PASS/L1BLOCKED; SDK708/0skip independiente y fix97146e9; KL5d832e0 estructural/historicalPASS y formal937 baseline idéntico. Todos los341 contratos completos siguenNOT_EXECUTED. Source main / adapters / helpers y controles compilados/revisados no sustituyen gate realSandbox403 ni managedSDK/lifecycle/observer pendientes.


- T21 [SOURCE_UNIT_PASS_REAL_NOT_EXECUTED] Domain, exclusive writer: document the schema minimum contract; save a red regression for 0/-1 × AWS MSK/GCP using actual SDK/parser binding and unit dispatch controls; add the lower-bound controller guard; prepare real HTTP/Kafka/KVS no-effect regression; run targeted unit tests and compile during the granted exclusive Gradle slot; freeze exact sources for independent peer review. Physical execution remains blocked by the actual Sandbox gate.

T21 validation: previous controller failed four schema lower-bound invocations because it scheduled the executor. Candidate controller suite passed25/0fail/0skip and real-suite compilation passed. Exact red/green XML/logs are saved in /private/tmp/kafka-e2e-discovery/t21-schema-*. Independent review remains pending. The four physical variants use real services and are NOT_EXECUTED; no invalid-input provisioning outcome is certified as success.

## T22 — auditoría focal y preparación pendiente

- T22 [SOURCE_AUDIT_ONLY / PREPARATION_OPEN]: root integra diez fronteras PM Kafka verificadas contra master0c83575; Domain proporciona contratos/objetos primarios; Infra corrige biblioteca; Fault revisa de forma independiente. Diez filas nuevas NONE/NOT_EXECUTED. Preparar fixtures y cuerpos físicos de entidades/pipeline cuando se resuelvan recursos/revisiones Entity Service y contratos de template/routing; probar ambas versiones de autorización sin extrapolar develop a master. Ninguna fila se considera lista por la sola auditoría.
- Conteo vigente después de T21/T22: 351 filas, 299 FULL preparadas, 24 PARTIAL, 28 NONE; no capacidades E2E físicas certificadas.


- T23 [SOURCE_UNIT_PASS_REAL_NOT_EXECUTED] Domain: append functional/technical/tasks before implementation; add real SDK binding RED regressions and valid positive unit metadata; implement only two bounded controller guards; replace invalid-metadata physical success oracles and separate three compatibility conflicts; eliminate null-ID global-key ownership/deletion; targeted GREEN/compile in exclusive Gradle slot; freeze exact authorized paths for independent peer review. Existing28 NONE rows remain visible. All full physical contracts stay NOT_EXECUTED.

T23 author validation: RED36 Deployment+28 Action invocations failed specifically because the old controllers scheduled execute(Runnable); no errors/skips. GREEN67 Deployment+46 Action=113 PASS/0fail/0error/0skip, with real SDK binding, schema/compatibility/processor-delegation preservation. compileRealIntegrationTestJava, compileE2eTestJava and compileManagedIntegrationTestJava PASS after manual OpenAPI additions. Required-metadata rows explicitly separate normative guards from CURRENT legacy compatibility; compound rows stay PARTIAL for unresolved SDK/PM declared-contract conflicts. No actual CP/KVS/managed business runtime is certified.

T23 full-unit follow-up: coordinator run804 tests found4 failures/0errors/0skips, all ProvisioningEventsIntegrationTest positive JSON missing newly required metadata. Authorized only its three payload builders to supply valid IDs/names/criticality without changing assertions, business mocks or layer classification. Existing receipt remains failure evidence; focused rerun then coordinator full rerun are separate. Unit constructors/literal HTTP fixtures are audited to distinguish direct-processor tests from inbound controller fixtures.

T23 fixture follow-up GREEN: controller113 + ProvisioningEventsIntegrationTest6 + ActionEventsIntegrationTest4 =123 PASS/0failure/0error/0skip. All three suites compile. Only positive Provisioning JSON metadata changed; original assertions and mocked-business layer remain intact. Root full804/4-failure receipt is preserved as pre-fixture-correction evidence. Independent clean f80 red/green and final coordinator full rerun remain separate.


## Final source checkpoint — 2026-10-02

Source preparation and independent receipts are integrated in `meli/features/20261001-real-e2e/evidence/DELIVERY.md` and the common `meli/features/20261001-real-e2e/evidence/` ledger. T24/T24R3, T26 and owner-process source/component reviews are recorded separately. Root aggregate29 SHA23409c2bc593f8373a419255e4c00b08747f8d01f2499a95e17755795f50b0b1 plus independent r2 peer dd28a38d2419f35ec5a8aa2f19b01d78b6e0233b0e087f944564d4c598d6c30d closes typed-worker and neutral-readiness findings at their actual layer. Four neutral replays14/159 preserve all47 assertions/deadlines; prior failures remain.

Matrix351:304 FULL prepared,29 PARTIAL,18 NONE; every complete capacity is NOT_EXECUTED.22 T24 methods/36 invocations per PM policy; seven complete prepared joins and three partial frontiers. CP822 unit/0skip; PM4386 total/4384PASS/2 unchanged baseline skips; SDK708 unit/0skip. Three-family compile48/42/16classes. These checks do not complete the unchecked physical acceptance tasks.

Full correlated CP/Kafka/KVS/results/canonical and candidate PM suites, current Toolkit server create/version/CAS/TTL, managed OAuth/BigQueue/Odin, repeated clean business reproduction and actual corporate job remain BLOCKED. Formal Meli/Zord gate remains blocked by the recorded auto-review rejection; no reviewer publication or release occurred. See exact external actions and retained-failure rules in DELIVERY.md.

Checked implementation/review tasks above denote source or explicitly named unit/component controls only. Full physical acceptance and formal review tasks stay open; no checkmark certifies backend or a completed E2E family.


## CP-SCOPE-1 — prioridad CP del owner (2026-10-02)

- [x] Agregar scope CP-only a lifecycle/provenance de Sandbox con regression controls y mantener defaults ecosystem/legacy.
- [x] Rechazar recibos CP-only en familias ecosystem y documentar comando CP independiente.
- [x] Revisión independiente de aislamiento, ownership/cleanup y regresiones; ejecutar controles y task discovery/preflight real sin falsificar negocio.
- [ ] Guardar checkpoint/knowledge/commits CP-only y recibos de revisión de fuente.
- [ ] Ejecutar la suite física CP completa y repetirla desde checkout limpio: primero renovar Fury (`SANDBOX_FURY_LOGIN_REQUIRED` actual), después revalidar el clone propio que históricamente devolvió403; resolver permiso si persiste. Fuente/controles no cierran esta aceptación.

- [x] Corregir P2 preexistente de contexto del EXIT trap CI en Bash3.2 y agregar regresión de funciones reales sin backend; conservar retención UNKNOWN e independencia del parent.

CP-SCOPE-1 source controls: coordinator `validateRealE2eHarness`72 PASS and CP compile PASS; independent source/metadata v2 PASS,0 drift/0 findings after preserving baseline and bare-variable REDs. These checkmarks certify only the named source/neutral controls. Full business run, current Toolkit server contract, clean repeated reproduction and actual corporate CI job remain NOT_EXECUTED. Current auth gate is Fury login required; the former clone403 must be rechecked after renewal.


## LOCAL-MEMORY-1 — reemplaza gates Sandbox del scope local, 2026-10-05

- Domain: adapter por instancia, KvsConfig y regresiones CRUD/CAS/TTL/copias/close/profiles; único escritor de esos4paths.
- Infra: resolver de perfiles y fixtures/scenarios compatibles por contexto; manifiesto de selección/exclusiones.
- Root: perfiles/preflight/observer, Gradle, launcher/CI, SPEC y evidencia; sin negocio mock.
- Knowledge: runbook/ficha/manifest de rama pendiente, sin cambiar claims canónicos de producción.
- Revisor distinto: checkout limpio, controles de falla y reproducción Kafka real; limpieza/repetición.

Gates actuales: ejecución física y revisión independiente pendientes. Auth/Fury/Sandbox deja de ser dependencia del CP local; no se solicitará login para esa familia. CI corporativo remoto y familias ecosistema/managed no forman el gate inmediato solicitado.

LOCAL-MEMORY-1 checkpoint: adapter/config/guard59 and fullunit845 PASS/0skip, real-suite compile PASS; independent launcher/source/metadata/process49 PASS/0findings after retained REDs. Full physical attempt343/309fail/34pass/0skip hit refused host Kafka, with internal5broker health. SIGKILL forwarding cause UNKNOWN; own runtime stopped after failed restart, shared2GiB runtime untouched. Local full/repeated clean physical and CI job remain BLOCKED/NOT_EXECUTED. Local matrix356 distinguishes5 unitPASS,226BLOCKED and125NOT_EXECUTED; none is a productive KVS certification.
