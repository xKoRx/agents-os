# Validación funcional CP Kafka — activa

Backend autorizado: mapa por instancia, Kafka real. Fury Sandbox retirado del alcance local por el owner. Playmaker/ecosistema y transportes/proveedores administrados se verifican aparte.

- PASS de prerrequisitos: 68 clases/880 unitarios, cero FAIL/error/skip; compilación E2E, harness,20 controles de evidencia y bootJar. No es PASS E2E.
- FAIL conservado: baseline `cc21725628c84592b64113606ff072e7`,348/87 FAIL/0 error/skip,cleanup PASS.
- FAIL conservado: candidato3661388 corrida `ba6f97e381c24319961fa0e36dfc1bd0`,360/211 FAIL/0 error/skip,cleanup RETAINED. Retiro manual separado de recursos propios, sin cambiar el veredicto.
- FAIL conservado: candidato4df8822 corrida `d01cf0fbd82442fd80158dfc898e75ff`,359/349 PASS/10 FAIL/0 error/skip,cleanup PASS.
- FAIL más reciente: candidato db7f279, corrida `7bbf862d57d648d0b3ca6ecafc9abcd1`, 359/350 PASS/9 FAIL/0 error/skip, cleanup PASS; Docker propio confirmado vacío.
- Corrección implementada por GPT-6 Luna, congelada en b791048: precondición PEEK visible al CP, dos causas distintas de repetición DELETE, cuatro matchers de interrupción y dos precondiciones de config para deadline RF real. Contratos canónicos y oráculos conservados; SPEC antes de código.
- Pendiente obligatorio: nueva corrida física completa sin filtros y reproducción independiente completa desde clone limpio.
- CI NOT_EXECUTED: workflow en rama de trabajo fuera de default develop; acceso repo pull/push confirmado, API runners404. Falta integración y runner calificado Docker≥5GiB/Java25/Maven interno; no inferir ausencia de runners ni falta VPN.

Fuentes canónicas revalidadas2026-10-06: CPmaster `f74e856ef3de881e2d504c6cb1ced573681c1058`, develop `4302481c69300074a85ea5eb051a27bbd505cdce` (ancestro del candidato), KLmaster `de7cde85f7dd83a673c918e22ae9f08a0f7e05bd`. Master leído confirma routing ambiguo first-match. Cambios nuevos WORK_BRANCH_PENDING. Coste/tokens desconocidos.

Sesión activa, sin cierre ni declaración de entrega completa. Paquetes baseline/,candidate-red-1/,candidate-red-2/,candidate-red-3/ conservan evidencia sanitizada y hashes.

Cuarto intento de suite: `b791048`, run `2d88001ba3e04d3495494415896328b2`, FAIL antes de ejecutar (0 tests): cinco brokers saludables dentro de Docker, host ports unreachable30s; cleanup PASS. No es FAIL de negocio ni PASS. Infra recuperó sólo Colima propio mediante gRPC soportado por Lima1.0.5; ApiVersions5/5 y cleanup probes PASS. Causa SIGKILL SSH desconocida. Sin tocar VPN/default. El quinto intento completo está activo desde mismas fuentes congeladas.


Quinto intento EN_EJECUCION, no certificado: `b7910487c6a5336e128f9452b96f1e1641aa1740`, run `c6e8062a5de64da7af9663e7f6cfa128`, sesión32754. Readiness Kafka PASS y pruebas nativas activas sin filtros. Revisión source/schema independiente PASS, clean-v4 497 archivos/15pins listo para replay después de terminar y limpiar root. `runtime-grpc-readiness/` conserva límites/comandos/hash; sólo acredita conectividad.


Quinto intento terminado FAIL: `c6e8062a5de64da7af9663e7f6cfa128`,359/349PASS/10FAIL/0error/skip,cleanupRETAINED. Dos raíces GCP DescribeConfigs Unknown antesmutation y ClusterFault read metadata Timeout; ocho cascadas bloqueadas por journal retenido. `candidate-red-5/` conserva380 artefactos sanitizados/hash. RFnative, bridge/publicación no acreditados por este intento. Nueva corrección acotada con SPEC/review/Luna pendiente; no cierre ni full PASS.


Sexto intento EN_EJECUCION, aún no PASS final: b1a017adfc8d7c2139be808d042ddea29a581bf6, run19d659a642814618a2f97e10fa93d5b5, sesión90288. SPEC dbf5f8c/89696bc precedió cambios Luna acotados a tres archivos de tests; sin cambios productivos. Prerrequisitos10 PASS compilación/harness/20evidence/bootJar/266hashes0drift; revisión independiente source/schema19pins/6negativos PASS. Unit880@b791 reuso ligado a197 archivos main/unit/build idénticos. Limpieza manual run5 PASS por separado, original FAIL/RETAINED intacto. Root dueño exclusivo Gradle/Docker; peer-clean-v5 en preparación, replay físico pendiente.


Sexto intento final FAIL:19d659a642814618a2f97e10fa93d5b5/b1a017;354 nativos/348PASS/6FAIL/0error-skip,cleanupPASS;359 seleccionados no completados por6 interrupciones ausentes y1initerror. Nativeproof/casereceiptsfalse correctamente. Cuatro frentes:PEEK REST404 antes acciones; protocol Composeupnozero/salida helperborrada; ClusterFaultDescribeTopicsnativeTimeoutnode4 antesrestore yDescribeCluster local30s antesdispatch; RFdeadline2casosConfigEntrySET noobservable inmediatamente, sin alcanzartrigger. Bridge2/publication3 ahoraPASS físico, no fullcertificación. candidate-red-6 preserva artefactos sanitizados/hash; rawXML privadofreeze382. Diagnósticoindependiente, SPEC y nuevascorreccionesLuna siguen antes repetirfull+peer.

2026-10-06 candidate7 infrastructure diagnostic: actual owned Docker CLI negative controls PASS (320dd137d0134119accb4c703b6c0efc, Java25 compile0/control0/source drift0). Both nonzero exit and interruption preserve private hashed output and safe receipt; owned child reaped, interrupt restored. This is infrastructure proof only, not CP business PASS. Candidate6 remains FAIL354/6/cleanupPASS. Root review required ScenarioLuna to remove stale Admin observations, check native advertised endpoints, move receipts outside reconciliation intents and preserve original deadlines. Next: frozen review/inventory/compile → focused physical → full → clean peer.

2026-10-06 focused diagnostic13 @19eab8f (3cc97f825838411b802def07d42449cc) FAIL: native8=3PASS5FAIL/0errors-skips; cleanupRETAINED; sixInterruptedmethods not reached (initError1 instead). PEEK+twoActiontimeouts passed; independentADMIN/listNodes port56547 cannotconnect atOwnedProtocol233. Clusterfirstcase reached4nativephase receipts includingRF5ISR5/newIDCOMPLETED/guard, then cleanupDeleteTopics get30 localTimeout +suppressedDeleteGroup localTimeout; actualcause UNKNOWN (no nativecall/node instack). RemainingCluster/RF3 failures constructionjournalcascade beforemutations. Original28runfiles and497sourcehashes0drift archived; manualcleanup separate underway with ownedPID/resourcechecks. GPT6Luna prepares fresh cleanup mutationclient SPEC outsideCP; protocolprobe compares exact9094 hostbinding own resources. Full359+cleanpeer still mandatory, nofullPASS.

2026-10-06 candidate8 checkpoint: focused7 original FAIL/RETAINED intact. Own manualcleanup PASS separately (1fb2d3b8), ports/resources absent. Two exact9094 hostbind probes each TCP/ApiVersions3/3 PASS, prior JavaAdmin.listNodes failure NOT_REPRODUCED; gRPC unchanged. SPEC36ae21a precedes fresh cleanupAdmin and post-TCP Protocolobserver. Protocolf0db68frozen, Fixture under source review for full setupfailure caching and strictdecimal port parsing; CI exporter outsideCP gets five root review corrections. No Gradle/Docker active; full359 and independent cleanpeer still mandatory.

2026-10-06 focused8 @789c4e6/e15ad99b53a94cc7ba25260288d0d166 finalFAIL13=12PASS1FAIL/0errors-skips cleanupPASS. AllInterrupted6,Cluster2(+8actualphases),Boundary2,Control1PASS. RF1AWS failedAwaitilitypending30 atline99 BEFOREassignment; actualproductAdmin3DescribeCluster node4 hung60001ms thenFAILED, underlyingcauseUNKNOWN; GCPRF2 physicalTIMEOUTguard/recoveryPASS. Dynamicquota visibilitypassedall5, oldnullcauseclosed. Originals46files/497source0drift frozen, archivecritical-diagnostic-red-8/. Samefrozen-source RF2isolateddiagnostic9 launched to distinguish precedingchaos context from independentAWSbehaviour. Fullsuite remainsNOT_CERTIFIED; CIab97outsideCP review/sourceonly.

2026-10-06 RF2isolated9 @789c/245a0a2c298f4bbaa2f2dc4a2c08a78d native2/0fails cleanupPASS with actualAWS+GCP physicalpendingTIMEOUT/recovery. Gradlecompletion genuinelyFAIL REAL_E2E_PRIVATE_WORKER_FILE_REQUIRED; enumeration source includes cases directory among workerJSON inputs, independent diagnosis pending. Not an expected filtered-onlyfailure and no fullPASS. Boundary/RF sharetestcontext andnativeAWSdefault60s vslocalGCP10s; priorClusterdistinctcontext stoppedsamephysicalbrokers. UnderlyingconnectioncauseUNKNOWN; fresh context controls passed, isolation decision SPEConly beingreviewed. New gate scope: preciseprivatecases directory separation +same normalexit/PIDbirth/failclosedchecks. CIab97/source25neutral independentPASS, realfullgreenexport/tamper pending. Original18runfiles/497sources0drift frozen. No active Docker/Gradle; full359+peerremainmandatory.


## Candidate9 committed — 2026-10-06

CP isolated HEAD `dfa3d62` includes native worker layout selector correction, 12 private-filesystem controls and RF test context isolation. SPEC `060fcc5`, CI implementation `6777248`. Source review v1 P2 preserved; v2 PASS_SOURCE_ONLY, SHA `6f245c8eb759b05e13f46592bd65716cb7ac77991161f927c99a9187ed27f6d9`. Root actual combined validation13 running (880 unit expectation, E2E compile and neutral controls); full359 and independent clean replay pending. No physical full PASS. Fury not required; own memory map per context is the owner choice. Own Docker context remains `colima-rio-kafka-e2e-01a0f8e0`.


## Focused diagnostic10 — original RED preserved

Actual CP `dfa3d62cc36f867a747a06602d1cfe89dcf4b917`, run `a8b0a7bb26d9450fb05e405ce5cc52ec`: native13/12PASS/1FAIL/0errors/skips, cleanupPASS. Both AWS/GCP RF deadline recovery, both cluster-fault cases/eight physical phases and six interrupt cases PASS. Sole failure `HttpTimeoutException` owned-empty PEEK readiness helper `RealE2eFixture.java:1106`, before Action dispatch; underlying slow phase UNKNOWN. Native completion proof absent because actual failed Test task; filtered completeness independently false. Original46 run files and source499 zero drift frozen SHA `f2b64826a6694912dfdf7404baad5b56b034662d853cc84920eb7116d5c9ade1`; raw five XML private. SPEC10 being reviewed: remove independent2s readiness request cap while preserving overall20s deadline and404/not_found-only retry. No product/API/business changes or fullPASS claim.


## Native critical13 PASS — full attempt8 running

CP `e003906fd2c22af1370dcc90b7832dd4b51481ba`: actualcombined14 880/0fail/error/skip + compile/harness/12FS/20verifier/25CI/bootJar PASS, source499 zero drift. Focused13 run `5f9c95c7fef14f8396acb13c4e494ca4`: native13/0fail/error/skip, Gradle BUILD SUCCESSFUL, nativeTaskProofTRUE, cleanupPASS. Filtered aggregate correctly FAIL/caseCompletenessFALSE (13 is not359); no full-pass claim. Original47files frozen, both RF/cluster fault/eightphases/interrupt6/nativeActionTimeout/PEEK PASS. Full attempt7 `d14bc34be55b4d688b9eb508a6704291` rejected beforetests: ports unavailable diagnostic,0tests/noresult; original causeUNKNOWN/noerrno. Later authorized probe5/5 binds free/no LISTEN. Full attempt8 run `682f0e2bc5d749c88b0463f81a239263` now RUNNING unfiltered. Peer clean-v7 prepared exacte003 source499 clean/nohardlinks, no runtime yet. ProtectedownerWTs unchanged clean CP4c66/KL0fee.

## Full attempt8 — final FAIL conservado

Commit `e003906fd2c22af1370dcc90b7832dd4b51481ba`, run `682f0e2bc5d749c88b0463f81a239263`: **359 /358 PASS /1 FAIL /0 errors /0 skipped; cleanup PASS**. El único fallo es `RealFixtureCleanupIntegrationTest` línea58, “nothing was thrown”: la prueba cierra el Admin de lectura mientras la limpieza usa un nuevo Admin nativo. Revisión independiente confirma el objetivo de falla obsoleto; no se relaja el oráculo negativo. Originales congelados:712 archivos de corrida y499 fuentes sin drift, SHA `e4b247217f012384b753fe64a86d40731ae3c27b5e42f1ef9fc0ed5e1b691378`. Candidate11 SPEC propone provocar la falla en el mutador nativo real y añadir recuperación positiva (360 casos), todavía no implementado ni validado. Runtime/Gradle libres.
