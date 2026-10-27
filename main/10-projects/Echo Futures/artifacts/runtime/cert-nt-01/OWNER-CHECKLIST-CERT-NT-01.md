---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
aliases:
  - CERT-NT-01 owner checklist
tags:
  - kind/doc
  - area/echo
created: "2026-10-19"
updated: "2026-10-23"
---

# OWNER CHECKLIST — CERT-NT-01 (desbloqueo de gates C2/C3/C4)

## Manager 2026-10-27 — Cierre PRE `5a0cf62f`, G0 y rollback legacy pendientes

**SOURCE ACCEPTED para continuar CERT-NT-01; G0=BLOCKED_EXTERNAL, R1_LEGACY=NOT_PROVEN, OWNER_WINDOW_REQUEST=NOT_READY.** Runtime DEV, FX, NT y PROD NO se han tocado por este dictamen. El `expected-roster` configura 8 keys ACTIVE pero el split 5 `present`/3 `absent` es todavía hipótesis hasta la sonda real de las ValueSpecs; `seal --cut-kind savepoint` está desarrollado/testeado y la lectura física queda bloqueante **antes de detener el job**.

El MCP SSH externo `aranea-ssh` debe re-inicializarse en el host del agente; después el MISMO Submanager sólo ejecuta G0 preflight RO (relay SFTP staging + mounts JM/TM) y certifica el camino R1 antiguo SIN fresh-submit. El Compose legacy `ac0621a1` no llevaba recovery gate ni restore args; no se puede recomendar volver a ese Compose y arrancarlo sin `-s/--fromSavepoint` explícito. Sin G0 y rollback probado, NO SOLICITAR ventana Owner. Referencia [[WINDOW-CARD-PRD6]] «Veredicto Primary Manager post cierre 5a0cf62f». No nuevo Flink, no restart FX, sin armado, PROD/SIM bloqueados.

## Manager 2026-10-26 — FASE 0 ACEPTADA, PERO VENTANA OWNER AÚN NO SOLICITABLE

Release `4a041e6c` reconstruido/readback OK; DEV Flink `flink` .75 mantiene job 38/38, 17 ingress, FX consumiendo, cuentas Futures desarmadas, PROD intacto. Fase 0 sin restart ACEPTADA. **No autoriza reinicio, savepoint real, despliegue ni ARMADO.**

El Submanager GLM, dentro de esta MISMA CERT-NT-01 y sin otro PRD, debe cerrar las condiciones PRE-01..05 vinculantes al inicio de [[WINDOW-CARD-PRD6]]: roster proyectado mediante `Runtime.ExpectedRoster()` y validado contra estado materializado; prueba de relay SFTP para posterior copia de estado off-host; source de restauración coherente (P1 checkpoint vs P2 savepoint: el artefacto RESTAURADO ha de ser el MISMO sellado y portable), path del savepoint dentro de JM/TM, rollback condicionado a efectos FX. Topic attest = provisioning en la ventana. **Si el savepoint falla, NO ejecutar fallback incremental no validado**; STOP antes del restart. Única acción Owner futura: aprobar explícitamente la ventana una vez presentado GO/NO-GO completo. No nuevo Flink/Compose, no tocar PROD ni cuenta comercial.



## PRD.6 adjudicada por Manager 2026-10-26 — DEV solo observación, ventana Owner pendiente

**Código fuente `4a041e6cf17b27a023a1a693a48be1034c35e7dd` aceptado COMO CANDIDATO a certificar DEV con excepciones limitadas**, no G-IMPL pleno ni PROD. La cobertura sigue bajo GOD-03 (nuevos 89.94%; diff-aware 82.71%); excepción sólo para DEV sin órdenes. La rama incremental RocksDB no quedó probada en el lab: la copia actual de `_metadata`+dependencias no demuestra portabilidad si hay rutas absolutas. **Antes de un reinicio compartido FX/Futures, obtener savepoint/backup completo y portable usando servicios ya existentes, demostrar identidad/checkpoint/17 ingress y rollback y conseguir AUTORIZACIÓN EXPRESA DEL OWNER de la ventana.** Si el snapshot no es verificable, STOP SIN RESTART. La tarjeta WINDOW-CARD-PRD6 debe materializarse y verificarse en vault antes de la ventana. No tercer Flink, nuevo Compose project, cuentas, Sim101 ni PROD. Ver [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]] y planner [[Echo Futures — Runtime Pools]].

## EF-PROD 2026-10-26 — PRD.5 RO aceptado; SIN VENTANA DEV todavía

El Manager verificó `c2d71357` (sólo pruebas/tooling) y aceptó el inventario, pero detectó incompatibilidad de migración en `seal.go`: sólo 1 ingress frente a 17 FX/Futures, offsets desde HWM en vez del checkpoint, copia sólo de `_metadata` sin SST/dependencias y campos de identidad sintéticos; `owner_continuity.go` rechaza keys legacy ACTIVE sin su nuevo marker. Sin snapshot/savepoint completo recuperable ni migración comprobada, **NO reiniciar/recrear Flink DEV ni declarar segura la tarjeta Owner**. PRD.6 es un único cierre GLM sobre source y pruebas aisladas, no otro GOD ni otro Flink. Cobertura también continúa bajo 95% (92.61% archivos nuevos, 78.96% diff-aware observado). PROD y SIM/órdenes siguen intactos/desarmados. Autoridades [[EF-PROD-PRD5-MANAGER-REVIEW-20261026]] y [[Echo Futures — Runtime Pools]].

## EF-PROD 2026-10-25 — Código GI-2 listo para preflight DEV existente; PROD NO-GO

**Decisión Owner:** Aranea ya tiene dos Flink/StateFun (DEV y PROD). NO desplegar otro Flink ni nuevos proyectos Docker. Fuente candidata `0e17c4d3`; L3 restore probado sólo en laboratorio aislado. G-IMPL queda BLOCKED por cobertura insuficiente 82.92% archivos Go nuevos / 76.45% subset diff-aware observado (9 archivos sin datos). Se permite preflight sólo lectura sobre Flink DEV existente y preparar actualización observation-only; **no reiniciar jobs FX compartidos ni aplicar Compose source automáticamente**. Despliegue DEV depende de checkpoint/rollback/impacto FX comprobados y ventana Owner cuando corresponda. PROD/Ninja ejecución/Sim101 continúan DESARMADOS hasta autorización y certificación separadas. Referencia [[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]] y [[Echo Futures — Runtime Pools]] PRD.5.

## EF-PROD 2026-10-24 — G-IMPL BLOCKED por integración source; certificación física NO-GO

El Primary Manager volvió a revisar `9daa57cb` después del cierre GI-01..04. **M1 schema objeto está corregido y el JAR real lo aceptó**, y los negativos de Kafka/ETCD funcionan en su capa. **G-IMPL permanece BLOCKED** porque `gate` no obliga al master de StateFun a restaurar el snapshot, `attest` no tiene readers efectivos; Kafka topic identity y frescura completa/edad de documento no están demostrados, y 96.68% cubre archivos Go nuevos pero no código añadido a existentes. Ver addendum de [[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]], PRD.4 en [[Echo Futures — Runtime Pools]]. Un solo correctivo B3, sin GOD nuevo. No desplegar, instalar con nuevo scope, armar SIM/LIVE, tocar cuentas comerciales ni ejecutar este checklist hasta autorización posterior de G-IMPL/G-ENV/G-REC/G-FEED y Owner.

## Diseño GOD 2026-10-23 — G-DOC ACCEPTED, implementación GLM autorizada, certificación NO-GO

El paquete [[EF-PROD-GOD-01-SOURCE-FORENSICS]], [[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]], [[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]] y [[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]] quedó **G-DOC ACCEPTED con enmiendas vinculantes M01–M07** registradas en [[EF-PROD-GOD-05-MANAGER-ADJUDICATION]] por Primary Manager el 2026-10-23. Se autorizó sólo implementación GLM B1→B2→B3 en source/entornos aislados; **no** despliegue operativo, listener, cuentas, armado SIM/LIVE, ni ejecución de esta checklist histórica. Estado/gates exclusivamente en [[Echo Futures — Runtime Pools]]. Instalación feed-only mantiene controles Owner de antes sin ampliación. F1 no repara restore y la RCA original del resubmit sigue sin demostrarse. G-IMPL y certificación físicos permanecen pendientes.

## ACTUALIZACIÓN MANAGER 2026-10-23 — F1 LIVE reparado; cert física y PROD BLOQUEADAS por restore Flink

**SHA Core DEV actual reportado:** `ac0621a1917a9ecbed50b3daed4add1518ffc71d` (reemplaza la identidad `2ee61791` en la sección histórica FINAL). El reloj LIVE funciona; sin embargo, Flink falló y re-sometió job NUEVO sin restaurar estado (`restored:0`, reset sequencer Futures, replay FX). La RCA/garantía de recuperación y 30 min reales de frescura STAMPED/NATIVE están pendientes. **NO autorizar listener de ejecución `:9771`, `futures-bridge/accounts` ni ningún armado, incluso Sim101, por completar solamente esta tarjeta**.

**Acción Owner permitida de forma independiente, SIN órdenes:** comprobar que no haya operaciones ajenas abiertas que hagan inseguro un reinicio de NinjaTrader; respaldo del perfil; instalar SOLO la versión integrada staged `EchoExecutionAddOn.cs`, `EchoFeedV1.cs`, `EchoNativeBars.cs` y retirar el anterior `EchoFeedAddOn.cs`/duplicados; instalar JSON TARGET con binding exclusivo Sim101 y secreto local (no publicar auth_token); verificar identidad real de Sim101 con `Account.Id` en el terminal y que NO aparezca RJARA comercial en ningún binding de ejecución; reiniciar NT únicamente bajo control Owner y validar handshake/feed sin activar ejecución. **No asumir que plataforma ID `2` es invariable:** revalidarlo en el terminal. Si no es posible demostrar identidad y feed único, STOP y rollback del perfil NT. La certificación operativa continúa bajo el ledger [[Echo Futures — Runtime Pools]], no bajo la sección FINAL histórica inferior.

## FINAL 2026-10-23 (SHA 2ee61791 desplegado) — UN solo ciclo Owner: AddOn integrado + JSON Sim101 + reinicio NT

Runtime ya desplegado y verificado por el submanager: core/gateway/relay DEV en release `2ee61791` (binarios buildvcs limpios), module Flink verbatim en .75 (job RUNNING 38/38), perfil de feed ETCD provisionado (ticks ALL, flush 50ms, NATIVE 1m..1d, NQ 12-26), backlog histórico drenado. Falta SOLO el ciclo físico del AddOn en .132.

- Paquete staged verificado por hash en `.132`: `C:\Users\echo-dev\certnt01-final\` (4 archivos; tarjeta `OWNER-INSTALL-CARD-FINAL.md` con pasos exactos, backup, rollback y hashes; fuente daedalus `/home/kor/opt/echo-dev/var/nt-feed/owner-install/final-2ee61791/`).
- Acción: cerrar NT → respaldar → RETIRAR `EchoFeedAddOn.cs` (una sola autoridad de feed; D5) y duplicados → copiar `EchoExecutionAddOn.cs` + `EchoFeedV1.cs` + `EchoNativeBars.cs` (sha256 en la tarjeta) a `Custom\AddOns\EchoFeed\` → reemplazar COMPLETO `echo-execution-addon.json` por el TARGET sustituyendo sólo el `auth_token` (binding CERTNT01-SIM01 → .161:9771 → Sim101 id "2"; config_version 1; feed ticks ALL/flush 50/NATIVE 1m..1d) → iniciar NT.
- Verificación esperada (submanager por canal del relay): hello con capabilities `feed.ticks.v1/feed.bars.v1/feed.batch.v1`, `feed_state ACTIVE`, `market_batch` en Kafka con `bars_origin` estampado, y binding RESOLVED = Sim101 id "2" (cero RJARA…551).
- Este ciclo desbloquea C2 (ventana stampada de 30 min), C3 y la elegibilidad de armado C5. El armado C5 lo ejecuta el submanager con despacho propio tras verificar el ciclo.

---

Actualizado 2026-10-20 (RESUME-05): la sección «RESUME-05» de abajo es la vigente para el arming C3.

## RESUME-05 (2026-10-20) — timeout CORREGIDO y demostrado; JSON COMPLETO; acción Owner única para arming C3

- Estado runtime vigente: core `112ccccd` (fix del timeout, release `~/opt/echo-dev/releases/112ccccd…`, MainPID 2936052) + module verbatim `aa7a019c` en .75 ACTIVOS; job Flink `faf27ca3` RUNNING 38/38. Prueba sostenida real 31,7 min con feed vivo: **ESTABILIDAD PASS** (0 timeouts/restarts/excepciones, 14 checkpoints COMPLETED, FX lag 0, ETCD intacto, entorno DESARMADO). Hallazgo abierto que NO bloquea el arming: servicio 20,5 rec/s vs ingress 46,1 rec/s ⇒ la edad del evento procesado crece por sobre la cota `FreshnessBound=30s` (FreshnessStale; la admisión continúa por diseño D6); la paridad de ingress requiere palanca arquitectural (estado shardado/incremental del sequencer — shot futuro). Detalle: `~/aranea/work/cert-nt-01-c-resume5/HANDOFF-C-RESUME5.md`.
- JSON a instalar: `RESUME05-ADDON-JSON-SIM101-COMPLETO.json` (en este directorio; sha256 `7a06d643fa6d98679ecb429ea1d38b16d14b4f7922e72de330b4435fd28501c9`, 510 B). El ID de plataforma de Sim101 **ya está resuelto: "2"** — obtenido del evidence-log del relay de feed (`~/opt/echo-dev/var/nt-feed/evidence.jsonl`, frame `account` con `discovered[{"id":"2","name":"Sim101"}]`) y verificado contra el source byte-exacto de ambos AddOns (`EchoFeedAddOn.cs:615` y el drift-check `EchoExecutionAddOn.cs:1037` comparan el mismo `Account.Id`). El ÚNICO dato que el Owner sustituye al instalar es el `auth_token` (el vigente del perfil; jamás transita por chat).
- Validación con el parser REAL del AddOn (lógica verbatim de `EchoExecutionAddOn.cs` sha `a93a6a1e…` compilada con csc .NET 4.8 en .132): `config loaded: bindings=1 contracts=1`, account_id=2/Sim101, ntx_port=0 deshabilita la lane sin invalidar — **ALL_PASS 7/7** + test negativo fail-closed (port=0 → INVALID). La confirmación definitiva es la carga en vivo (log `bindings=1 RESOLVED` tras reiniciar NT).
- **Acción Owner EXACTA (arming C3):** (1) cerrar NinjaTrader 8; (2) reemplazar por completo `C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json` con el contenido del JSON COMPLETO sustituyendo el placeholder del `auth_token` por el token vigente (copiarlo del archivo actual antes de sobrescribir); (3) iniciar NT. Verificación esperada: log `config loaded: bindings=1 contracts=1` + binding RESOLVED (Sim101, id "2"); CERO intentos de dial hacia :9770 (ntx_port=0); dial hacia :9771 sólo cuando exista el listener del bridge. Después de este ciclo, el arming C3 lo ejecuta el submanager en un despacho nuevo. Referencia completa: `~/aranea/work/cert-nt-01-mgr-resume5/OWNER-CHECKLIST-RESUME5-DELTA.md`.

Actualizado 2026-10-19 noche (RESUME-03): el defecto P1 del typename fue **CORREGIDO, publicado (`c37d1351`) y demostrado en vivo** (el job con el fix registró los 10 specs de `market_stream` y consumió ~375K mensajes frescos sin ninguna `IllegalArgumentException`). El module volvió a PRE por un defecto NUEVO distinto (timeout del transporte StateFun→core bajo burst del feed, RESUELTO en RESUME-05 — ver arriba). El feed de las 21:00Z resultó ser la **pausa ordinaria de NQ (16:00 CT)**: reanudó solo a las 22:00Z. El contenido del JSON fue confirmado por el Owner y **NO es armable** (apunta a una cuenta comercial real). Ninguna acción pendiente arma ejecución.

## Estado de las acciones originales (2026-10-19 RESUME-01)

- **Acción 1 (reconectar «Simulación»): RESUELTA — la caída de 21:00Z era la pausa diaria ordinaria de NQ (16:00–17:00 CT).** El feed reanudó SOLO a las 22:00Z con la reapertura de Globex (verificado: QUOTE NQ:NQZ6 con `event_ts` <2 s a las 22:27Z; burst ~170 ev/s). La reconexión GUI del Owner ya NO es una espera activa: re-verificar frescura del feed justo antes de cada ventana de certificación y reclasificar sólo si una congelación ocurre FUERA de la pausa 21:00–22:00Z.
- **Acción 2 (cargar AddOn de ejecución): HECHA por el Owner** (RESUME-01/02, PID 8556). Matiz UNKNOWN V8 opcional sigue abierto: `Get-FileHash "C:\Users\KoR\Documents\NinjaTrader 8\bin\Custom\AddOns\**\EchoExecutionAddOn.cs"` (esperado `a93a6a1e…` del release, una sola copia).

## RESUME-03 — typename P1 CORREGIDO y demostrado; defecto NUEVO: timeout del transporte

- **Fix publicado:** rama `feature/ef-runtime-pools` @ `c37d1351` (fix `be3c35e4` + regresión gramática `c37d1351`, verificación independiente VERIFIED, release desplegada en `~/opt/echo-dev/releases/c37d1351…`). El core DEV corre `c37d1351` (owners:7). La gramática se pinneó contra el runtime Java REAL desplegado (clase `TypeName` del jar, md5 `9a7bf01c`).
- **Demostración en vivo (23:14–23:44Z):** module verbatim re-aplicado → job 38/38 → `echo/market_stream/NQ:NQZ6` registró sus 10 estados con `echo.types/futures_*` y consumió committed 21.848.991 → 23.223.863 (~375K mensajes frescos, 0 duplicados/conflictos, journal egress emitiendo) **sin ninguna excepción de typename**. El P1 de RESUME-01 quedó cerrado con evidencia de producción.
- **Defecto NUEVO (bloquea la estabilidad de C2):** a los 12 min bajo burst del feed, 3× `RequestTimeoutException` del cliente netty de StateFun invocando `echo/market_stream` (batch acumulado 1001 mensajes / 2,5 MB), "Checkpoint Coordinator suspending", FixedDelay 5s×3 agotado → job FAILED. Rollback del module ejecutado íntegro (PRE 28/28 estable, FX lag 0). El core sano responde; el análisis del call-timeout/capacidad del clúster StateFun (worker 2048 MB, async max-per-task 8) es el SIGUIENTE paso antes de reintentar el verbatim — fuera del alcance de RESUME-03. Evidencia: `~/aranea/work/cert-nt-01-c-resume3/HANDOFF-C-RESUME3.md`.
- **Nota ETCD:** las claves `futures/enabled` + `futures/config_snapshot` fueron borradas por un actor externo a las 22:31Z (rev 61252) y re-provisionadas byte-exacto por el submanager (22:39Z). Si al armar no están, re-provisionar desde `~/aranea/work/cert-nt-01-a/config_snapshot.json` (validar con el parser del release) antes de cualquier restart del core.

## JSON de configuración del AddOn — CONTENIDO CONFIRMADO por el Owner y NO CONFORME (SUPERSEDED 2026-10-20 por el JSON COMPLETO de RESUME-05, sección arriba)

El JSON provisto (token enmascarado) usa la forma legacy plana, que el AddOn (`ParseBindings`, source `a93a6a1e…`) convierte en **UNA asociación de EJECUCIÓN** con `account_name="RJARA114411201551"` — **cuenta comercial real del Owner** — en `.161:9771`, y apunta además la lane de mercado al mismo 9771. Con ese JSON el armado queda PROHIBIDO (Sim101 exclusivamente; resolución de cuenta Name-primary; los comandos Sim101 serían RECHAZADOS fail-closed, pero la configuración no es la autorizada).

**Acción Owner exacta (referencia completa: `~/aranea/work/cert-nt-01-mgr/RESUME03-ADDON-JSON-SIM101.md`):** editar `C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json` a la forma multi-binding con `bindings:[{physical_binding:"CERTNT01-SIM01", host:"192.168.31.161", port:9771, account_id:"<id de plataforma de Sim101>", account_name:"Sim101"}]` y `ntx_host:"192.168.31.161", ntx_port:9770, account_id:"<id Sim101>", account_name:"Sim101"` (token SIN cambios; contratos/intervalos SIN cambios). Resolución Name-primary: el nombre debe ser exactamente `Sim101` y el id de plataforma debe coincidir (contradicción = drift fail-closed). Tras guardar: reiniciar NT. Pendiente de decisión al armar: la lane de mercado del AddOn de ejecución hacia `:9770` conviviría con el AddOn D6 de feed (doble productor) — el submanager lo reconcilia en el despacho de armado.

## Qué queda PROHIBIDO para cualquiera (vigente)

- Habilitar `futures-bridge/accounts` (clave de armado), iniciar `futures-bridge`, o poner `enabled=true` en la asociación `certnt01-a1` sin un despacho explícito del Manager (eso ES armar ejecución).
- Ejecutar/cancelar órdenes en cuentas RJARA\*/E2T del Owner. SIM autorizada para esta certificación: **Sim101** exclusivamente.
- Mergear `feature/ef-runtime-pools` a master o tocar Echo PROD.

## Reanudación de la certificación

Orden de desbloqueo actualizado (RESUME-03): (1) análisis y corrección del timeout del transporte StateFun→core bajo burst (call-timeout/capacidad del clúster: worker 2048 MB, `statefun.async.max-per-task=8`; decidir configuración o remedio de producto con despacho nuevo — evidencia en HANDOFF-C-RESUME3) y re-aplicación del module verbatim; política del backlog (~1,36M mensajes históricos 18:53–21:00Z NO consumidos: con `startupPosition: latest` del release se saltan por diseño; cambiar a earliest/grupo requiere decisión del Manager); (2) Owner aplica el JSON corregido (Sim101, multi-binding, ntx_port 9770) + reinicio NT; (3) submanager arma la sesión SIM: token + binding + `futures-bridge/accounts` SOLO con la cuenta de certificación, verificación de binding Sim101 y de `RESOLVED` (no DRIFT) en el AddOn; (4) smoke del gateway y recorrido Strategy→MM→NT/SIM (C3); (5) rotación/recuperación/economía (C4, con `MULTIACCOUNT_NT_NOT_EXECUTED`); (6) verificación independiente (C5) y estado final seguro (ejecución automática deshabilitada).
