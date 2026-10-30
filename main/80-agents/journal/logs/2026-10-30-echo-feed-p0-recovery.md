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
