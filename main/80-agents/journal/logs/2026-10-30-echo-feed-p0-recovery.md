---
type: change_log
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities: []
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-30-echo-feed-p0-recovery

## Cambio

Actualización de [[Echo Futures — Runtime Pools]] con mandato P0, baseline preservado, ownership Sol/Luna, gates pendientes y cuota confirmada. El proyecto sigue como único planificador.

## Evidencia y motivo

Mandato Owner 2026-10-30; lectura source de workers y estado local systemd/journal. Feed reconectado tras acción física Owner a las 13:58:42 Chile, sin certificación inferida. Se corrige la inferencia histórica que comparaba items del relay con records Kafka: no demuestra estancamiento por sí sola.

## Validación y límites

Rama fuente inicial limpia en 3eaed4d2; nueva rama de misión conserva baseline. Go freeze3 y S2 pasan suites focales/race/vet y revisión independiente. C#165+4asserts/0fallos tras cap pending; revisión independiente cap/drain/resume y crash→SOURCE_GAP PASS. Integrado87c85a5e en codex/echo-feed-p0; paquete Windows validado y staged C:\Temp\EchoFeedP0. Relay87c85a5e desplegado17:38:40Z PID149253 porhash23960992…b78c9, core/gateway yFlink intactos; S2guard solo staged. Instalación/compilaciónNT Owner pendiente. Baseline físico reproduce NACKED tras drain desde14:09:39 Chile; causa inicial de presión no demostrada. Solo relay DEV actualizado; certificaciones pendientes. Cuenta de cuota: 64% inicial y59% restante último corte; reserva5%. Sin secretos ni dumps persistidos.

## Rollback

Revertir únicamente el delta documental de este hito; conservar historia y cambios concurrentes.

## Corrección del instalador tras intento Owner

El paquete original confundió símbolo configurado con Instrument.FullName y falló antes de mutar addon/identity. El fixture inicial reflejaba esa misma suposición y no cubría el límite real. Reparación: preservar única clave durable existente y mantener validación de fingerprint productiva. Windows confirmó nombres distintos, helper positivo sobre copia temporal, fingerprint incompatible sin mutación, multistream/missing identity rechazados; paquete reemplazado (Install SHA791fc1b5…caf40f). Instalación física sigue pendiente del reintento Owner.

## Segunda corrección: identidad legacy confirmada por Owner

El segundo Apply también falló antes de mutar. Diagnose.ps1 confirmó schema/session/fingerprint/last_seq/updated_utc, cursor28576, sin epoch/data_seq. La causa de ambos preflight puede ser la enumeración de propiedad ausente en PS5.1; no quedó demostrada diferencia real de alias. Source b440776d4b154fbb91e29ce2c522fd1e1a28ebbb pusheada: marcador de gap de perfil en misma identidad, materializado usando la clave real del primer callback; sesión, cursor y outbox preservados, sin floor inventado. Revisión independiente detectó y cerró bypass STORAGE_FAILED por reconnect; Windows206asserts/0fallos +11checks adversariales PASS. Installer Apply+Rollback QA7 sobre forma exacta/cursor28576 PASS; helper idempotente, negativos sin mutación, rollback byte-exacto. Staging final C:\Temp\EchoFeedP0 y readback Windows11/11 hashes PASS; manifest7c7cfc69d16ab013bad5374f5dd731be96b6db495b5877dcabe6c45c559d8a7d, Installb2a8c1b1fd781202c27b3fffb95e42615f55ea0b732077a858a6962b9bf83bed. Fuente del manifest b440776d verificada con remoto. Paquete final preflight legacy PASS; instalación NT Owner aún NOT_RUN. Relay permanece87c85a5e; C#-only no exige rebuild Go, core/FX no tocados. Cuota último corte56% restante.

## Instalación física y defecto de reconexión

Owner Apply PASS con4archivos outbox y5fuentes; backup20261030T184231959Z-3c39ce21 fuera Custom. Log físico último inicio15:49:03Chile carga P0 MVID450b806a-641f-4c47-a0d8-b1c635b2bb22/assemblySHA0e81df1d12bf13d53a8ff8d725e924090c3f980aeccc5cf2e6423222d2528a1d. Sesión preservada ycursor30145. TCP conecta; relay rechaza hello0 duplicado antes de negociar contra highwater30169, source confirmado Accept antes handleHello. A15:51:54 callbacks32570 pero batches0/cursor30145/LEGACY. Se autoriza corrección estrecha Go: control handshake en nuevo socket autenticado, pin sesión/socket, sin reset ni dataACK prematuro. Owner no debe reinstalar; mantiene NT abierto/desarmado. Evidence sanitizada local echo-feed-p0-reconnect-evidence/before-fix.json. Sol implementa, Luna revisa semántica C#, runtime_evidence verifica independiente; root integra/deploy sólo relay tras QA. Cuota55% restante confirmada.

## Recuperación de transporte tras fix de handshake

Sol integró corrección por root en44502831 (remoto confirmado): hello control separado de datahighwater, auth/sessionpin/socketowner ycursor preservado. Regresión socket roja→verde, suitesfocales completas-race/vet yQAindependiente PASS;2fixturesTCR sólo ConnectionClosed entre hellos. Build limpio vcs.modified=false; relay único desplegado18:57:35Z PID187477 SHA44d7ec421452b17031ef317e984e211559aaf3e99b06754a4d4a814b3ab1323d. Primera comprobación inmediata deexe falló antes de lectura estable; readback/proc posterior PASS sin otrorestart. Rollback conserva dropin87c85a5e ybinario. Core/gateway/current/Flink intactos. NT reconecta automáticamente18:57:43Z conP0/MVID esperado, config1 ACTIVE. A18:58:35Z ACK30867,497recordsKafka/14030items confirmados, sinerrors/rejects/stall. Transporte recuperado; aún falta prueba física exacta contra highwater retenido: Owner reiniciaNT una vez, sin reiniciarrelay ni reinstalarAddon. Gate sigue desarmado; gap/30min/S2 pendientes. FuenteNTb440776d yrelay44502831 explícitos porcomponente.

## Retorno Owner y defecto concurrente de persistencia

Owner respondió continua tras restart físico. RelayPID187477 sigue sin restartdesde18:57:35Z; feedACTIVE ycursor43519→45061. Nuevo reason visible: IDENTITY_PERSIST sharing failure feed-identity.json.tmp; repetición de reason no equivale a nuevosfallos porheartbeat. Source confirma snapshots bajo gate pero I/O compartido fuera, persistedSeq=lastSeq actual no snapshot, dirtyflagscleared tras posiblemutación. Luna autorizada fixmínimo+reprosdeterministas; Solcrossreview; runtimereviewer updater source-only conbackup/fuentehash youtboxintacto, sin re-ejecutargapmigration. Conteoactual procesosNT noverificado; mensajeWindows no prueba otroproceso.

Journal retenido sólo19:08:57Z enlectura19:33Z, sinhello/sessionopened/configapplied delrestart; no certificar handshake exacto porregistroausente. EvidenciaSol RELAY-STABILITY-1933Z:30publishfail acumulados,19logsretenidos sobre14seq; ACK44778 supera todofailedseq(max43572), queue0/64, saturation0/stalled0. Retries recuperados, no exactamenteonce ni30mincert (persistencia pendiente+huecoretención). No más investigaciónKafkainfra ni mutacionesruntime. Cuota53% restante.

## Persistencia corregida y actualizador separado

Fuente e8f699b693b788094c52710d2138d06dd81dbc32 integrada y pusheada. EchoFeedV1 SHA e99d9e25df5af44955b89b3a26cfed68e720a5d109bc7d8923b256c8f0d6ae0b; tests 8dae0e05…89b91. Windows baseline rojo 215/5; final 230/0 + F05 70/0. Revisión independiente PASS: serialización del temporal, avance concurrente no falsamente persistido, gap durable, retry y SOURCE_GAP/estado STORAGE_FAILED conservados. No cambios Go ni redeploy de relay.

Owner confirmó cierre de NT y el guard real devolvió cero procesos. Actualizador separado EchoFeedP0Update reemplaza sólo una fuente, con respaldo, hash esperado previo y comprobación de outbox idéntico. QA Windows Apply/idempotencia/rollback PASS; rechazos por outbox avanzado y fuentes alteradas sin mutar datos. Paquete local verificado: manifest 2026277924f35866784f00b79aa77211b07cf4095aca1b9e459e304dd7ad3cd8, Update.ps1 dc0ad739…900f9. Readback Windows final 4/4 hashes PASS y fixture preflight final PASS. Paquete entregable C:\Temp\EchoFeedP0Update; QA resumen /tmp/echo-feed-p0-update-qa/summary.md, hash2a8cd518…ace5. Gate pendiente: Owner Update.ps1 -Apply, F5 y reinicio limpio/conexión feed desarmada. No Apply al perfil Owner desde herramientas.

Para conservar evidencia del siguiente arranque antes de la rotación del journal, se inició un colector local de sólo lectura durante una hora (exec session13672), con campos permitidos y sin payloads de cuenta/tokens: echo-feed-p0-reconnect-evidence/identity-update-live.jsonl. No reinicia servicios ni cambia configuración. No equivale a una certificación ni a una automatización recurrente.

## Actualización física aceptada y observación

Owner Apply source-only PASS con outbox/identidad intactos y backup20261030T194722320Z-424343b0. Aclara que reinicia NT tras compilar: AddOn inicia automáticamente, no hay switch adicional de feed. Colector preservó hello de misma sesión seq0 a16:50:25 (assembly anterior),16:51:35 (nueva compilación) y16:52:51 Chile (última MVID0a6ba618-2bf3-44e0-bad5-bcbc52c53006, SHA67102f47f1b2436ab5a58cec66042c4a82b7c5e2a18e5f338d230ab5a227ea6a). RelayPID187477 desde15:57 intacto yconfig1 aplicada: rehandshake físico contra sesión retenida demostrado. Composite proof por fuente instalada/verificada+compilación Owner+MVID cargado, no sourceSHA inferida del assembly.

Heartbeats posteriores ACTIVE yreason vacío; cursor47242→47400. Observación30min desde16:52:51 hasta17:22:51, no PASS anticipado. /ready19:56:07Z mantiene market_fresh BLOCKED EVENT_TS_AGE_EXCEEDS_FRESHNESS_BOUND y ejecución sin permisos; investigar continuidad/analytics/proveedor antes de certificar. Sol B2/continuidad RO, runtime_evidence ventana/ready RO, Luna bindingSIM/PoolMM RO; sin mutaciones económicas ni sharedcore/Flink. Cuota51% restante confirmada.


## Diagnóstico B2 posterior al update

Provider confirmado actual por candidatos QUOTE/TRADE19:59:42Z, stampedseq719726..720339; no falta conexiónNT. Estado canónico comprometido aún02:00Z/LEGACY_DEGRADED; grupoFlink drena45146621→45151726, lag43373→39298. Iniciojob19:54:03Z requiere verificar causa/restore antes de inferir continuidad; no mutacionesruntime. Publicaciónrelay registra9fallosTCP sobre4seq y ACKposterior49468; progreso recuperado, no prueba porpayload de exactlyonce. Observación continúa hasta20:22:51Z. SIMreview debe distinguir selectorlegacyfeed de bindings ejecuciónCERTNT01-SIM01 ya documentados; no concluirausenciaSIM buscando sólo prefijosSIM/Sim101.


## Delta físico y guard de continuidad

Checkpoints2605/2606/2607 completados tras restore2604, avance durabledelstream19721→82081 facts yLSO14721518→14783885; diagnóstico inicial sano se limita a ese corte. A20:04:49Z apareció RequestTimeoutException NQmarket_stream, checkpoint2608 falló Coordinator suspending yrestore2607@20:04:54Z; no atribución aC# ni mutaciónmanual. Lagposterior35603 sigue descendiendo; no fullCERTPASS.

Sol/Luna demuestran fuente EchoNativeBars sinlookbackconfig (cursor→now o1día), insuficienteparademostrar51H4/20×5m ni rehidratartrasrestoredownstream. Recovery porOHLCtickssynthetic noadmitida. Root adjudica P0 de seguridad: BAR_COVERAGE puedehacerREADYaunqueSourceGapOpen; Sol autorizadofixmínimoSDKmarket/readiness+red/green, Lunaverificaciónindependiente; sourceonly, sinruntimewrites. Contracto de rebootstrap/epochcontinúadesignonly: no resets, nodeletionsgap, noREADYmanual. Cuota49% restante.


## Guard integrado y diagnóstico sin hipótesis promovidas

Root integra/pushea d49648e83a8db79e7f62de2dd6772229335a4930 tras red6casos/green SDKmarket+ctx+analytics+S2 race, corefuncionesfocal yvet; Luna3probesindependientes overlay/racePASS. Root detectócausabarspuria conOpenGapsvacío, Sol corrigióantesfreeze. Corebuildlimpio Go1.27.1/vcs.modified=false SHA9fe03c835e28c4289009650037a557b63e3a48084fb4154f9838f319a42d4f62 staged echo-feed-p0-release-d49648e8; nodeploy.

A20:12:33 CP2607últimocompleto,2608/2609/2610fallidos,restorecount4; committed45156750 sinavancedurable desde20:06:53,lag35603→37303. Fuentequote/tradeactualinnerEpoch1 distintoouterrelayepoch. HeadKafka45156750es4QUOTElegacy event02:19Z,no70itemsactuales. Perfhermético bounded16invocations×70items431ms,response4.01MB;16×256771ms,response9.10MB. No explica2minfísico, noRCAporamplificaciónniaprobarcaparbitrario. Sólolectura/perfaislado; runtimeintacto. RebuildSegment existecomo tipo sinrutaoperativa: gapirrecuperable+51H4/20×5m requierecontratorevalidaciónnativaauditable aúnnoimplementado; no usartickssynthetic niresetcursor.


## Ventana30min completada, sin certificación end-to-end

19:52:51.799→20:22:51.799Z. ÚltimoheartbeatACTIVE/cursor57378,9781/9780sealed/sent,pending2,reconnects1. RelayACK57349/440ms,queue4/64,saturation/stall0; publishfail54→84/rejected22→45. Progreso de transporte yassemblyrehandshake demostrados; noPASScontinuidad/frescura/S2 porloopFlink ydatosnoacreditados. Reporte preservado echo-feed-p0-reconnect-evidence/post-update-window-20261030.md SHA98eeb6fb…ec732; colectorROstoppedtrasventana, sinserviciosafectados.

Root autorizó observabilidad focal source-only aSol (HTTPbytes/status/duration/cancel +contador/time marketstream, sinpayloads/identidades, memoriaacotada ysinsemánticacambiada), Lunaverificará; prepararpaquetecoreyrollback antesdepedirúnicaventanaFX. NuevodeploytodavíaNO autorizado. CorePID78126 ybaselineSHA0dc3ca7f…26de9 re-verificados. FXgroup echo-core-v3 STABLE (configcache sincommittedoffset, nointerpretarlagcomoatraso); FXreferenceevents lag9 enlecturaRO. Noorders/armado/offsetreset.


## Candidato de diagnóstico listo; espera de ventana FX

Root integra/pushea7db3e1692de550162833b24d7ee13782d4fdeab0: instrumentación numérica del RPC real con límites y guardias previamente revisadas. QA Sol focal race/vet y Luna independiente PASS. Último defecto reproducido por root/worker: emit bajo mutex bloqueaba otros submits; corregido con emit/after fuera del lock, máximo1callback activo, agregado fijo y1timer máximo. Probe independiente100000updates+64concurrentes con sink retenido demuestra retorno concurrente y flush al liberar. No nuevos goroutines por request ni cambios al contexto de procesamiento.

Build limpio/vcs.modified=false; SHA580ff43a6b41c52d6310bbdb6d8f01e3f86fbf0620e83a07e3b3596ed1781418. Binario staged inmutable en opt/echo-dev/releases/7db3e1692de550162833b24d7ee13782d4fdeab0/echo-core, sin drop-in activo ni restart. Tarjeta concreta+manifiesto+proposed drop-in+rollback en /home/kor/aranea/work/echo-feed-p0-core-window. Único gate humano: mandato§11 prohíbe interrumpirFX; pedir autorización de reinicio exclusivo coreDEV compartido, dejandoNT abierto. Riesgo explícito: caída endpoint puede disparar recuperación automáticaFlink; ningún stop/restore/resetFlink autorizado. Baseline binario rollback0dc3ca7f…26de9 preservado.

SnapshotFlink20:28:34–35Z instancia iniciada20:13:46.962Z,2608completo20:26:46Z/restaurado20:28:10Z. No mezclar checkpointIDs con instancia previa. Root adjudica que el mismo bucle conocido no obliga a diferir indefinidamente la medición; recapturarpreflight y detener ante divergencia inesperada. Ninguna causa física del timeout demostrada todavía. B2/S2/SIM pendientes; sin armado/órdenes. Cuota45% restante, misión activa esperandoOwner, no cierre de sesión.


## Ventana core autorizada y ejecutada

Owner autorizó explícitamente reiniciar coreDEV y repararDEV, sin volver a pedir el gateFX. Baseline previa coincidió; readyfalse/noexecutionpermits, FXcacheSTABLE y Flink ya en recuperación antes de mutar. Se instaló únicamente drop-in90-feed-p0-core.conf y reinició echo-core-dev20:59:54Z. PID253760 carga7db3e169 SHA580ff43a…81418 por /proc/exe; /healthok. Gateway79000/relay187477/current3eaed4d2 intactos, sin intervenciónmanualFlink. Runtime sigue bloqueado y frescura pendiente. Core-window/deployment-result.json y owner-authorization.txt preservan evidencia. Sol observa RPCdiag y runtime_evidence investiga recuperaciones rápidasJM/TM (anteriores y posteriores alrestart); noRCAanticipada.


## Direct memory OOM físico y recuperación worker

Nuevo fallo21:01Z: Direct buffer memory en Kafka NetworkReceive y Nettycliente; workerJVMactual Directcap1744830464bytes, RSS10.2GiB, sinOOMcgroup/Docker. Workeractivo11:14:59Z mientras master28restarts. Root comprobó8/8objects del inventariochk2604 y5/5shareddepsoriginales presentes/hashmatch; manifest-2metadata/annexdigest divergen debytesactuales inventariados, driftpreexistente, noCLEANnuevo. No cambiarestoreargs: masterexistente reusa corteconfigurado; no seleccionarcheckpointantiguo manualmente.

AutorizaciónOwnerDEV vigente: root ejecutó una vez dockerrestartstatefun-worker,StartedAt21:05:33.137Z, sin config/state/offsetchanges ni manualJMrestart. Post21:06RUNNING40/40, RSS~3.43GiB vs10.2previo,mismocap; primeraRPC146batches/988items/5.526s/HTTP200. Disponibilidad recuperada, causa de acumulaciónaúnnoresuelta ni certificación. Observarcheckpoint/progresoFX y Futures; nodeclararSTABLEcache comoavanceporoffset=-1001. Evidencia post-deploy-ro-evidence.json en core-window.


## RCA física RPC y corrección puntual desplegada

Netty21:18:36Z rechazó HTTP200 por respuesta35183940B >33554432B; reintentos agotaron120s y masterauto-restart29 a21:20:16Z desde2604configurado. DirectOOM previo es hecho separado; acumulación causal no demostrada. Sol implementó exactendpointmarket_stream16 preservando wildcard1000 ytransport, más taskmanager.jvm-exit-on-oom:true; Luna verificó precedencia y recarga realmoduleenFunctionGroupOperator.openTM contra fuenteApache3.2. SDKreal-race17×256items PASS43.681s, response10062264B,4352facts/egress intactos y17C2+17origin forwards; vetPASS. Root integró/pusheó7d2106ea.

Savepoint previo completo /opt/flink/savepoints/echo-feed-p0-20261030/savepoint-0f6901-bf5a646f5f8d; archivehost SHAa1b659dc…baac. Copiaoffhost no completada porlímiteherramienta, noportabilidadcertificada. No era necesarioresubmitJM. Cirugía sobreconfigreal21:32:15Z preserva8192m/4slots; backup /root/statefun/p0-backup-20261030T213215Z. Host/TM moduleSHA04c1d59cbfa7d436c3380cadfb6cff4c68057d7559fb9a92e67e232a90e83afb yconfSHA3ceb20d2d2feffb291784095f9548e50e3a58fc929724b8ca1ac73edd635aba6 iguales. Worker-onlyrestart21:32:20.401Z; JM21:20:16.500/29sinrestart;40/40RUNNING, restore2610 a21:32:39Z. OOMtrue confirmadoenlogdecarga. No cambiosstate/cursor/restoreargs/epoch/órdenes. Nuevointervaloobservaciónservidor; mercado cerró21:00Z, livecert esperaeventoauténtico. Cuota41%restante.


## Confirmación cap real, identidad Owner y fuente-gap moderno

RPCs nuevas16C1 confirmadas21:37–21:40,respuesta4.49–7.50MB,HTTP200/zeroerrors; grandes1000/72postrestore erantrabajopersistido, semánticaStateFunverificada. Root/Sol/Luna SDKreprolegacy→DATA2/prev1 rechazacorrectamentemissing1 inclusoJSONrestore/BAR_COVERAGE. Búsqueda17lecturasRO acotada encontróúltimolegacyoffset45171596yprimerstamped45171597receive18:57:44Z DATA1/prev0 BAR_CLOSED. No defectoadmisióncore demostrado.

Owner ejecutóDiagnoseGap share-delete/samesnapshotSHA,4fixtures+atomicreplaceWindows5.1PASS. Identidad epoch1,lastframe68313,floor991264,profilegapnull, streamgapNOT_NEGOTIATED missing550237/onset19:51:32.9255795Z unknowncount. Source/helperstage1031779457… ambossoportanprofilegap, tambiénupdatee99d9e25…; noRCAinventada sobreausenciadelmarkerpreupgrade.21:59read_committedconfirma CURSOR/frontier550236/source_gaptrue/NOT_READY SOURCE_GAP_UNRESOLVED. Mercado cerradoackOwner; nofrescuraen vivo niSIMclaim.

CoreobservabilidadS2mínima7archivos+docsb9a5ca20 integrado/pusheado, QA Solfocal+fullS2race/vetPASS yLunaoverlayadversarialscalar/read-onlyPASS. InterfazopcionalWarmupDiagnostics reutilizaeligibilidadcausal, logpostupdateevaluated5m separaowner/evaluation/warmup; sinestado/decisión/efecto/API nuevo. Buildclean SHA dadaac7b…267a3, core-onlyrestart21:55:19Z PID285883,/procverified/healthok; gateway/relay/current/JM/TM intactos. /readyruntime/recoverableREADY peroSTAL ypermisosausentes. plannedcorebounceimpideclaimuninterrupted30min; serverconfigobservaciónhasta22:04.

B2actualnative5msnapshot96barsnoequivaleaH4Seen/BBSeen/S2readiness; nopublicreadmodelS2. ConfigSnapshotleadingobjects completosconfirmanrunpin certnt01-r1/modeLIVE (marketmode,noautorizacióncuentaeconómica) ystratcertnt01-s2s2NQ:NQZ6. Manifest/journaltopics p0oldest=HWM=LSO0: recordingnoacreditado. RebuildSegmenttipoexistesinruta; contrato3puntosproponeC5nativo/segmentodurable/stagingtechnical/ownerreceipts, peroRUN_STARTmarketnoactualfanoutStrategy. Rootpideamendmentmínimoexistingowners/noservice antesadoptarimplementación. B2nofingeinitialanchor/historia niresetcursor. Cuota40%restante.


## Ventana servidor terminada y continuidad pendiente

Corte22:04:55Z: mismosJM/TM,40/40tasks, checkpoint2625/0failed, restore2610. Futurescommitted=HWM45207224/lag0; FX152805/lag0.14RPCsnuevas16C1, max7503497B/1852.50ms/HTTP200/0errors, sinrecurrenciaTooLongFrame/OOM/timeout. Memoriadirecta~1.367GB. Corebounceplanificado21:55 impideclaim30minE2Eininterrumpido. Collectoresfinitosdetenidos. post-cap-observation.json SHAefb81ee12e4bb2389b609cb46408f4feabf861830de99ffb174c7d50a4e44530. Readcommittedfrontier550236/sourcegaptrue/NOT_READY confirmaOwnergap550237; lag0noequivalea continuidad. Ambosmarkersdepérdida sepreservan, RCA históricaausenciaoriginaldesconocida. Sol/LunaretomancontratoB2mínimo yreviewantesimplementación, sinmáspesquisasgenerales. Cuota37%restanteconfirmada; reserva5%.


## B2 contrato congelado e implementación disjunta

Root integró/pusheó7082d27c (B2-CONTRACT+goldenbytevectors); no producto implementado porroot. Solwire/market/core/runtime; LunaC#capture/intent; runtime_evidenceSDKbars/analytics/strategy. RawC5array exactUTF8/base64/SHA; corpuscodec5bars deliberadamenteinsuficientepara51/20. Singleactivestream/lane, capabilitypositiva, pausacapture/drainoldoutboxACK, immutablecapsuleartifact→identityPREPARED→exactoutboxframe→durableACK→atomicepoch/floorrollforward, gapsauditados. NewnativeprojectionyS2technicalstate seinstalanlocalmente sólo trasvalidarcorpus/causalReadyFromState; config/economía/counters/live dedupconservados; allconfiguredreceiptsjoinenmarketmantieneNOT_READYhastaresultado. Ledger16bounded yúltimobundleacotadopermitido. Corefirstdeploy, no downgradepreB2trasadmisiónrebuild; ningún protocolo parcialdesplegado.

Prerequisitocursor: Solreprored yfixverifiedidentityduplicatenextcursor sincanonicalseq/forward. QAindependienteruntime detectóreadinessstrandedalhealgapconduplicate; SolcorrigióEnginecompose ytestsforeignbar+restore/freshnesssinavance. RealSDKoldcoreunknownREBUILD_SEGMENT abortaRPCenteraantesDATAepoch2, -racePASS. Revisiónfinalcruzadadelconjunto pendiente. Windowscsc4.8.9232 yNTCore/Gui8.1.8.4disponibles; ninguna lecturaKoR/process ni solicitudhistóricareal. Cuota35%confirmada; reserva5%.


## B2 integración en curso, corte 22:55Z

Helpers SDK bars/analytics/strategy pasan suites focales con race y suites completas; la prueba S2 de fidelidad tenía un fallo preexistente reproducido en archive limpio7082 (control sin READY). Se corrigió sólo la precondición del control; warmup permanece NOT_READY y conserva paridad/ausencia de señales. Sol revisa independientemente los helpers. QA independiente wire/relay confirmó golden/negativos y bloqueo de ACK/DATA hasta publicar control durable. Vertical real SDK 51H4+20×5m con3targets funcional; falta freeze y medición máxima256/respuesta32MiB.

C# compiló contra NT8.1.8.4 real y harness golden/crash/generation pasó. Se detectó por fuente que heartbeat/account positivo puede adelantar outbox durante negociación: se autorizó corrección mínima y repro antes de freeze. La pausa intencional queda auditada como discontinuidad UNKNOWN; no crea missing1 ficticio en época nueva. El actualizador multiarchivo pasó parser PS5.1, Apply/rollback con fixtures aún pendiente; no se entregó ni aplicó. Request exacto3835af8e-f281-4ffa-8d9a-03751569b349, SHA4a01e9be54660d15c143acc0124b99b9e673b4b06ed75dc8d54035178092b6b8. No cambio de identidad/outbox ni nueva intervención Owner.

LIVE checkpoint/restore es alcance B2; EXACT_REPLAY de C5 permanece explícitamente no soportado y debe rechazarse, sin trades sintéticos. Rechazo técnico/config invalida receipt durable sin bloquear CLOSE; cache lag conserva latch y no aborta RPC. Root verificó22:53:30Z healthOK/runtime+recoverableREADY, marketSTALE/executionBLOCKED. Restore args automático sigue2604: no reiniciar JM con ese pin ni usarlo tras B2; cierre operativo debe resolver referencia futura con corte nuevo verificado. Cuota32% restante, reserva5%.


## B2 fuente integrada y servicios desplegados 23:11Z

Commit463307945cf666b3df8dc444551a308fb105be5e, rama codex/echo-feed-p0, pushFF confirmado y checkout limpio.43archivos (40producto/tests y3docs), root sólo integración/docs/ops. QA cruzada cerró orden writer/legacy direct-drain, profileIDENTITY compatible, receipt caller común typed/raw y amplificación audit. Suitesrace/vet/composición y C#Framework64 contra NT8.1.8.4 PASS. RPCreal max256C5+3840DATA en16invocaciones, estado2,454,930B; respuesta12,533,314B <32MiB. Fanout completo>8MiB rechaza sin instalación parcial; audit summary32refs<512B con evidencia completa preservada. EXACT_REPLAY C5 explícitamente no soportado; no certificado de replay.

Builds Go1.27.1 exactSHA/vcs.modified=false. Core instalado/verificado23:11:10Z PID349117 SHA7ead79c6105517c6430320752e1c7f0f8496e1f79817d27abf280ad82b2327f2; healthOK/runtime+recoverableREADY, marketSTALE/executionBLOCKED. Relay verificado23:11:36Z PID349547 SHA7e6724b01e5960a321832a2095841bb4f620eba620b4e6f11a837481ee4c19b4, listener9770. Gateway79000/current intactos. Backups exactos preB2 son Coreb9a5ca20 y relay44502831; no usar rollback viejo7db/3eaed. Evidencia completa y manifiestos en /home/kor/aranea/work/echo-feed-b2-release/. Sol verifica postdeploy RO acotado.

Paquete /home/kor/aranea/work/echo-feed-b2-update-package está ligado a46330794 y cuatro fuentes congeladas; Update.ps1 SHA9c2c0b95cf59d462394160f4dc2cbe50ccfc6861f30d0b049da5fa025a055cbb. Compilación fuente/harness y parserPS5.1 PASS, pero Apply/idempotencia/rollback aún NO_RUN: solicitud Owner cerrarNT y respondercontinua está pendiente. No paquete final entregado, ninguna modificación KoR ni solicitudB2 aplicada. No repetir permisos; esperar confirmación. Cuota30% restante/reserva5%. Tras recuperación real persistida, aún debe actualizarse restoreargs2604 a savepoint fresco verificado sin reinicioJM. Mercado cerrado sigue bloqueando frescura/S2SIM.
