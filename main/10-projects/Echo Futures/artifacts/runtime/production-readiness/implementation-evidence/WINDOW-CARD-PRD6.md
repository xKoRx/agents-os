---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]]"
  - "[[EF-PROD-PRD6-RECOVERY-MIGRATION-CLOSURE-20261026]]"
  - "[[Echo Futures — Runtime Pools]]"
  - "[[OWNER-CHECKLIST-CERT-NT-01]]"
aliases:
  - WINDOW-CARD-PRD6
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# WINDOW-CARD-PRD6 — tarjeta de ventana Owner (final, materializada)

## Decisión Primary Manager post Fase 0 — 2026-10-26 (PRE-VENTANA, vinculante)

**Fase 0 ACCEPTED. El Owner NO debe autorizar aún el restart.** Los puntos P4 son preparación técnica del submanager, no tres decisiones personales del Owner. Seguir el mismo plan CERT-NT-01; no nueva etapa de arquitectura, ni nuevo Flink, Docker Compose project, Kafka/ETCD, VM/LXC o servicios. Sólo la ventana que interrumpa FX compartido requiere aprobación expresa del Owner, cuando todos los bloqueos previos estén cerrados.

**PRE-01 / Roster:** existe `v3/core/internal/futuresruntime/recovery_gate.go::Runtime.ExpectedRoster()` en el SHA `4a041e6c`, que deriva los 7 tipos de owner de la composición/configuración sellada (stream, strategies, pool bindings y operation composite key, accounts, pools). **Usarlo como proyección canónica de claves CONFIGURADAS** en vez de inventar otro enumerador. Pero no demuestra por sí mismo las claves y estados realmente MATERIALIZADOS en Flink/legacy: cruzar las keys ACTIVE y RETIRED contra el snapshot real/journal/identidad y el roster del manifest; detectar claves ausentes, huérfanas, estado no inicializado y conflicto. `RECOVER_MIGRATE` actualmente estampa el marker a un `RosterActive` sin lectura explícita de otra ValueSpec económica dentro de `initializeContinuity`; no aceptar una proyección de configuración como prueba de estado preexistente. Si no puede acreditarse la clasificación, STOP sin reinicio. No declarar BIRTH sobre estado histórico para silenciar el guard.

**PRE-02 / Copia:** recomendar **relay SFTP existente del agente**, cifrado hacia `.161:/srv/echo-work/ef-recovery/prd6-20261026/` y sha256 en origen+destino; no requiere instalar rsync ni claves entre hosts. Probar la capacidad con archivo no económico de staging ahora si ya está permitido; copiar savepoint/estado real sólo bajo ventana Owner. Verificar capacidad/espacio real justo antes de copia. Ningún snapshot se envía por el contexto del LLM/chat.

**PRE-03 / Topic:** `echo.futures.recovery-attest.v1` se aprovisiona exclusivamente en Kafka DEV, con identidad/config/control adecuados dentro de la ventana permitida. No es un bloqueo previo para solicitarla si el plan es determinista. NO auto-create silencioso.

**PRE-04 / Corte CONSISTENTE P1/P2/P6 (bloqueante):** la tarjeta histórica P1 sella el último CHECKPOINT; P2 genera un SAVEPOINT posterior; P6 restaura el CHECKPOINT de P1. **Crear un savepoint seguro no hace portable ese checkpoint incremental anterior.** Flink 1.14: `savepoint` normalmente portable, checkpoint puede tener paths absolutos. El corte realmente restaurado DEBE ser el MISMO cuyo manifest certifica todas las identidades y offsets, y su copia debe sobrevivir sin depender de ficheros del host original. `runSeal` del SHA actual exige Flink `latest.completed` y `--checkpoint-dir`; no se asume que pueda sellar un savepoint P2. Probar y resolver en el mismo mandato la compatibilidad mínima savepoint→seal/attest, o demostrar con evidencia fuerte que el checkpoint P1 incremental es AUTÓNOMO al perder el origen (incluye toda dependencia y las URIs que Flink realmente abrirá). Si ninguna ruta está demostrada, STOP antes de P5; no usar un P2 verde como permiso de restaurar P1.

**PRE-05 / Paths y rollback:** la ruta de `target-directory` del REST savepoint debe existir y ser accesible en el espacio de archivos **dentro del JobManager y TaskManagers**; el bind inventariado expone `/opt/flink/savepoints` en contenedor, no necesariamente `/data/compose/1/...` del host. Confirmar antes de disparar. P1/P2 con ingresses activos pueden tener fronteras distintas; hacer un corte coordinado, con interrupción/efectos FX comprendidos y plan rollback por frontera de efectos. El rollback R1 **nunca** debe hacer bootstrap por ausencia de manifest ni reponer un snapshot anterior si FX ya confirmó efectos posteriores sin reconciliación; en ese caso sólo forward-recovery conservador. Mantener el historial R1/R2 con esta prioridad.

**Restricción de autoridad:** hasta que PRE-01, PRE-02 (mecanismo probado), PRE-04 y PRE-05 estén documentados con evidencia, `OWNER_WINDOW_REQUEST=NOT_READY`; no instruir al Owner a fijar fecha para un procedimiento incapaz de restaurar el mismo corte. El Manager puede aceptar el preflight sin aprobar el reinicio. Próximo actor: **mismo Submanager GLM, cierre P4 técnico pre-ventana**, una sola entrega de tarjeta corregida/readback y luego solicitar una vez la autorización Owner. PROD, Ninja ejecución, SIM y cuentas reales siguen intocables.

## Propósito

Tarjeta GO/NO-GO y procedimiento 0-10 para la ÚNICA ventana Owner del commissioning DEV observation-only de Echo Futures sobre el MISMO Flink DEV existente (Compose `flink` @ .75), según la adjudicación [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]]. Versión final materializada en vault con el release del SHA exacto `4a041e6c` (reemplaza al borrador del workspace que referenciaba el release intermedio `63f241c0`); estado PRE-VENTANA verificado físicamente el 2026-10-26T23:30Z por el Submanager sin restart ni mutación del job compartido. La ventana NO arranca sin aprobación expresa del Owner; PROD, cuentas y SIM siguen intocables.

## Contenido

### 1. Regla rectora

El primer paso de la ventana es obtener y verificar el corte de estado completo ANTES de detener nada. Ante cualquier fallo: rollback ANTES de reintentar; jamás arranque fresco (sin restore args) para "salir del bloqueo"; jamás borrar el checkpoint original. Un solo deployment (proyecto Compose `flink` @ .75); PROD intacto; ninguna cuenta armada.

### 2. Identidad del release (fase 0, 2026-10-26T23:30Z)

Reconstruido desde worktree limpio `wt-main` del workspace `~/aranea/work/ef-prd6-20261026/` con `evidence/build-release.sh`; `origin/feature/ef-runtime-pools` verificado por `git ls-remote` = `4a041e6cf17b27a023a1a693a48be1034c35e7dd`. Layout inmutable: `/home/kor/opt/echo-dev/releases/4a041e6cf17b27a023a1a693a48be1034c35e7dd/` (BUILD.md con sha256 por archivo; `vcs.revision=4a041e6c…` y `vcs.modified=false` en ambos binarios Go; go1.27.1 linux/amd64).

| archivo | sha256 |
|---|---|
| `echo-core` | `10624fd0750a90a14fd8da479b0823751efd65d2e3d683dce322204ca04de3f8` |
| `echo-runtime-control` | `1e8c2c0817a0cebea2db9903b0c6c52a691fa7ccf27b7d9617f60b504f0f6b9e` |
| `probe/…/CheckpointFrontierProbe.class` | `c84ca49568737c4f6564240634024854fbfa6874793356be6022e57bdc5cfdc9` |

La clase de la sonda es byte-idéntica a la certificada en el laboratorio PRD.6 (compilada contra `flink-dist_2.12-1.14.3` de la misma versión que la imagen `apache/flink-statefun:3.2.0-java11` del master DEV); en ventana re-verificar hash contra el `flink-dist` del contenedor antes de sellar (G2). El delta `63f241c0..4a041e6c` es higiene de repo (retiro del binario commiteado); ninguna ruta económica cambia.

### 3. Estado PRE-VENTANA verificado (read-only, 2026-10-26T23:30Z)

- Flink DEV .75: job `StatefulFunctions` `0f6901a3a9aee496b408cbb5e4d0afeb` RUNNING 38/38 (≈66,7 h desde 2026-10-24T04:42Z); checkpoints 1970 COMPLETED / 0 failed / 0 restored; último `chk-1970` en `file:/opt/flink/checkpoints/<jid>/chk-1970` (host: `/data/compose/1/statefun/checkpoints/<jid>/`); state ≈6,8 MB; contenedores `statefun-master`/`statefun-worker` imagen `apache/flink-statefun:3.2.0-java11` desde el inicio del job.
- `module.yaml` desplegado: 20 768 B, mtime 2026-10-22 21:01 (corte FEFB S2, idéntico al inventario PRD.5); 17 ingresses + 7 egress sin `deliverySemantic` (M1 at-least-once efectivo hoy); backups CERT-NT-01 en el mismo directorio.
- Savepoints: directorio `/data/compose/1/statefun/savepoints/` VACÍO ⇒ no existe aún corte portable; `num-retained=1` ⇒ los checkpoints originales se ROTAN (los previos quedan `discarded=true`): la defensa EX-STORAGE del Manager sigue siendo operativa y P2 (savepoint relocatable) es obligatorio para el corte #2.
- Kafka DEV `.44:19091-96`: los 17 grupos `echo-statefun-*` presentes y EMPTY (asignación StateFun sin membresía clásica); `echo.futures.recovery-attest.v1` AUSENTE (pre-crear en ventana, P3/G3).
- ETCD DEV `/echo/development/`: `futures/enabled=true` (observación), `futures-bridge/accounts/E2T-GAU50-01/binding/enabled=false` (único binding, DESARMADO), `futures/config_snapshot` presente (11 991 B; certnt01-r1, NQZ6, provider SIM caps 2/2, estrategia certnt01-s2), `futures/market/freshness` ausente (llega con el release).
- Core DEV (.161 Daedalus): `echo-core-dev` ACTIVE en release `ac0621a1` (`vcs.modified=false`); gateway y front ACTIVE; sin listener `:9771` (sólo `:9770` lane de feed, observación); sin proceso `futures-bridge`; repoint a `4a041e6c` pendiente (P9).
- NT (.132): última autoridad PRD.5 (2026-10-25): feed NO_INICIADO, sin binding de ejecución armado; el perfil `dev-win` viewer rechazó la lectura remota en esta fase ⇒ re-verificar la capa NT en ventana (capa 4 del desarme).
- Almacenamiento: `.161:/srv/echo-work/ef-recovery/prd6-20261026/` pre-creado (sdb 147G, 12G libres — suficiente para el corte de ~MB); `.75` alcanza `.161:22`; disco raíz de .75 con 2,3G libres (88% usado) — suficiente para el savepoint pero sin holgura amplia: documentar headroom.
- PROD: intacto (sólo lecturas DEV en toda la fase; cero escrituras).

### 4. Inventario de los 17 ingresses (del module.yaml desplegado; offsets muestreados 2026-10-26T23:30Z)

Lane FX (11): la frontier authoritative por ingress la captura el `seal` en P1 (offset = frontier real del checkpoint, NUNCA HWM); la muestra RO de Kafka acredita consumo sano.

| # | ingress id | topic | consumer group | startup | target owner | muestra 2026-10-26 |
|---|---|---|---|---|---|---|
| 1 | echo/execution-policies-ingress | echo.execution-policies.v1 | echo-statefun-execution-policies-v3 | earliest | echo/strategy_config | grupo EMPTY, consumiendo |
| 2 | echo/reference-events-ingress | echo.reference-events.v1 | echo-statefun-reference-events-v3 | latest | echo/execution_planner | grupo EMPTY, consumiendo |
| 3 | echo/account-snapshots-ingress | echo.account-snapshots.v1 | echo-statefun-account-snapshots | latest | echo/acc_snapshot, echo/account_sync | lag 136 (p3), resto 0 |
| 4 | echo/instrument-snapshots-ingress | echo.instrument-snapshots.v1 | echo-statefun-instrument-snapshots | latest | echo/inst_snapshot | grupo EMPTY, consumiendo |
| 5 | echo/trade-closes-ingress | echo.trade-closes.v1 | echo-statefun-trade-closes | latest | echo/close_handler | grupo EMPTY, consumiendo |
| 6 | echo/execution-results-ingress | echo.execution-results.v1 | echo-statefun-execution-results | latest | echo/execution_store | grupo EMPTY, consumiendo |
| 7 | echo/close-results-ingress | echo.close-results.v1 | echo-statefun-close-results | latest | echo/execution_store | grupo EMPTY, consumiendo |
| 8 | echo/trade-closes-journal-ingress | echo.trade-closes.v1 | echo-statefun-trade-journal-master | earliest | echo/trade_journal | lag 1 (p5), committed≈HWM |
| 9 | echo/close-results-journal-ingress | echo.close-results.v1 | echo-statefun-trade-journal-slave | earliest | echo/trade_journal | grupo EMPTY, consumiendo |
| 10 | echo/reference-events-journal-ingress | echo.reference-events.v1 | echo-statefun-trade-journal-ref-open | earliest | echo/trade_journal | grupo EMPTY, consumiendo |
| 11 | echo/execution-results-journal-ingress | echo.execution-results.v1 | echo-statefun-trade-journal-exec-open | earliest | echo/trade_journal | grupo EMPTY, consumiendo |

Lane Futures (6): carriles económicos en silencio (execution-events y physical-drain con HWM 0 ⇒ cero actividad); bootstraps idempotentes consumidos al frontier.

| # | ingress id | topic | consumer group | startup | target owner | muestra 2026-10-26 |
|---|---|---|---|---|---|---|
| 12 | echo/futures-market-feed-ingress | echo.futures.market-feed-candidates.v1 | echo-statefun-futures-market-feed | latest | echo/market_stream | committed=HWM=45.142.540 (p4), lag 0 |
| 13 | echo/futures-execution-events-ingress | echo.execution-events.v1 | echo-statefun-futures-execution-events | latest | echo/operation | topic vacío (HWM 0) — desarmado |
| 14 | echo/futures-strategy-config-ingress | echo.futures.strategy-config.v1 | echo-statefun-futures-strategy-config | latest | echo/strategy_engine | committed=HWM=9 (p0) |
| 15 | echo/futures-pool-config-ingress | echo.futures.pool-config.v1 | echo-statefun-futures-pool-config | latest | echo/pool_manager | committed=HWM=9 (p1) |
| 16 | echo/futures-physical-drain-ingress | echo.futures.physical-drain.v1 | echo-statefun-futures-physical-drain | earliest | echo/provider_rules | topic vacío (HWM 0) — sin drain pendiente |
| 17 | echo/position-snapshots-ingress | echo.position-snapshots.v1 | echo-statefun-position-sync | latest | echo/position_sync | grupo EMPTY, consumiendo |

Topic IDs (KIP-516): los captura el `seal` por topic en P1 y los estampa en el manifest; los 7 owners futures con `HandleContinuityProbe` (market_stream, market_analytics, strategy_engine, signal_fanout, operation, provider_rules, pool_manager) son el universo de la migración ONE-SHOT.

### 5. Requisitos P4 pendientes ANTES de la ventana (huecos de preparación, fail-closed documentados)

- **Roster DEV (`--roster-file`):** no existe hoy un enumerador autoritativo de las keys ACTIVE de los 7 owners futures desde el checkpoint; el sweep valida contra el roster sellado y es fail-closed en AMBAS direcciones (key faltante ⇒ owner queda bloqueado en runtime tras la migración; key sobrante ⇒ sweep NO-GO). Método de generación debe definirse y su lista congelarse ANTES de la ventana (recomendación: derivarla de `futures/config_snapshot` + perfil nt-feed y validarla contra el inventario PRD.5 de 32 keys; cualquier drift ⇒ NO-GO documentado, no ajuste ad-hoc).
- **Ruta de copia G5:** `.75` NO tiene `rsync` y NINGUNA dirección tiene clave SSH instalada (.75→.161 ni .161→.75); el target `/srv/echo-work/ef-recovery/prd6-20261026/` ya existe. El Owner decide ANTES de la ventana: instalar clave SSH (push o pull, con `tar`+ssh o instalando rsync) o autorizar explícitamente el relay SFTP del agente como mecanismo de copia (viable: corte de ~MB; exige MCP SSH vivo durante P1-P2).
- **Topic `echo.futures.recovery-attest.v1`:** pre-crear en ventana (P3) vía MCP Kafka DEV o verificar auto-create (G3).
- **Defecto cosmético P3 (D-5):** el `--help` de `echo-runtime-control` no lista `seal` ni `bootstrap-token`; ambos subcommands existen y funcionan (`cli_run.go:93/111`). No bloquea; registrar en el reporte de ventana.

### 6. GO / NO-GO (condiciones exactas)

GO exige TODAS:

| # | Condición | Verificación en ventana |
|---|---|---|
| G1 | Manager aprobó el cierre PRD.6 | HECHO — [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]] ACCEPTED_WITH_LIMITED_DEV_EXCEPTIONS |
| G2 | Release por SHA `4a041e6c`: `echo-runtime-control`, `echo-core`, sonda contra el `flink-dist` del contenedor | hashes §2; `go version -m` y sha256 por binario; hash del `.class` contra la lib del contenedor |
| G3 | Topic `echo.futures.recovery-attest.v1` existe (o auto-create verificado) | MCP Kafka DEV `describe_topic` |
| G4 | ETCD `/echo/development/futures/config_snapshot` existe (revisión real para el seal) | HECHO — presente 11 991 B; read-back en P0 |
| G5 | Copia COMPLETA off-host del corte a `.161:/srv/echo-work/ef-recovery/prd6-20261026/` + sha256 verificado en destino | `sha256sum -c` en .161; mecanismo según §5 (clave o relay autorizado) |
| G6 | Sonda sobre el corte: 17 operadores con frontier legible; 0 `unreadable`; 0 partición ambigua | salida JSON de la sonda archivada |
| G7 | `seal` SEALED con 17 ingresses, offsets = frontier del checkpoint (NO HWM), topic_id KIP-516 por topic, manifest+anexos digest-verified | stdout del seal + `LoadManifest` |
| G8 | (Migración) sweep `continuity-migrate` MIGRATION_COMPLETE: roster completo, 0 MISSING/ERROR, evidencia CAS instalada | stdout + key ETCD `futures/recovery/continuity_migration/<lineage>` |
| G9 | Restore con restore-args hacia la COPIA; Flink `latest.restored` == checkpoint sellado y external_path == copia; attest EXTERNAL CLEAN | REST + `echo-runtime-control attest` |
| G10 | Post-restore: FX consumiendo (grupos `echo-statefun-*` avanzando, lag drenando), Futures desarmado (`binding/enabled=false` intacto), 0 excepciones del job | Kafka admin + Flink REST + ETCD |
| G11 | Checkpoint POST-restore COMPLETED (con markers MIGRATED_LEGACY) + seal gen N+1 SIN migración (STRICT) | REST + seal |

NO-GO inmediato (cualquiera): sonda falla o deja operadores ilegibles; seal refuse por cualquier brecha (publicarla, no saltarla); sweep con timeout o un solo outcome ≠ MIGRATED/ALREADY; restore sin `latest.restored` o desde otro snapshot; attest ≠ CLEAN; FX sin consumir tras el restore; cualquier excepción del job no explicada. En NO-GO: R1 rollback y la ventana termina en el estado previo.

### 7. Procedimiento (pasos 0-10, en orden; nada se salta)

- **P0 — Congelar entrada.** Re-leer el job vigente (REST `/jobs/overview`), anotar jid, uptime, último checkpoint COMPLETED (id + external_path). Congelar cambios de config (ni ETCD ni module) hasta el fin de la ventana.
- **P1 — Corte ANTES de detener nada (regla rectora).** Con el job CORRIENDO: `echo-runtime-control seal --job-id <jid> --checkpoint-dir file:<external_path> --module-file /root/statefun/modules/application/module.yaml --roster-file <roster.json> --config-file <roster-config.json> --storage-root /opt/echo/recovery --env development --etcd-endpoints ... --kafka-brokers ... --flink-rest http://statefun-master:8081 --flink-libs /opt/flink/lib --probe-classes /opt/echo/probe --continuity-migration --migration-attest-owner echo/recovery_attestor --migration-request-topic echo.futures.recovery-attest.v1`. Verificar salida SEALED: `ingress_count: 17`, offsets por ingress (frontier real; `earliest_sentinel` listados), `completed_at` = REST. Copia off-host (G5) + `sha256sum -c` en .161.
- **P2 — Savepoint relocatable (corte portable candidato).** REST `POST /jobs/<jid>/savepoints` con `target-directory` en la **ruta del filesystem del contenedor accesible por JM+TM** (verificar el bind, p. ej. `file:///opt/flink/savepoints/`, NO asumir el path host `/data/compose/1/...`) → COMPLETED → verificar todas las dependencias → copia off-host. **P2 no autoriza P5** hasta que el propio savepoint quede ligado al manifest con frontier/roster/IDs y la ruta P6 RESTORE exactamente P2, o hasta que se demuestre el restore independiente del checkpoint incremental P1 sin el origen. Si no es sellable con el CLI actual: STOP y corrección mínima antes de ventana. NO cancela automáticamente el job; congelar frontera/efectos de forma coordinada.
- **P3 — Pre-crear `echo.futures.recovery-attest.v1` si falta (G3)** (MCP Kafka DEV; partitions 1; retention del módulo).
- **P4 — Preparar archivos (tarjeta archivo-por-archivo PRD.5 §4 vigente):** backup + replace `module.yaml` y `flink-conf.yaml` por los del release `4a041e6c`; edit mínimo del compose (gate + env ECHO_* + bind `/opt/echo` ro + restore-args); `/opt/echo/bin/echo-runtime-control` (hash `1e8c2c08…`) y `/opt/echo/probe/` (hash `c84ca495…`); roster/config congelados según §5; `num-retained` ≥ 10 en el flink-conf del release.
- **P5 — Paro coordinado.** Verificar que ningún binding está armado (pre-G10). `docker compose stop` del proyecto `flink` (master+worker juntos). Registrar hora UTC.
- **P6 — Restore.** `echo-runtime-control gate ...` → RESTORE → `master-restore-args` apunta **al MISMO corte portable/independiente certificado en P1/P2** (manifest + offsets + job identity). No asumir copia checkpoint P1 sólo porque P2 savepoint existe. Antes de arrancar, verificar integridad/accesibilidad sin ficheros del checkpoint original. Arrancar el MISMO Compose con `--fromSavepoint <artefacto-certificado> --job-id <jid>`; verificar `latest.restored` coincide EXACTAMENTE con el manifest (G9a). Si no se puede vincular el artefacto, STOP.
- **P7 — Migración.** `echo-runtime-control continuity-migrate ...` → MIGRATION_COMPLETE (G8); el job procesa con markers MIGRATED_LEGACY; FX sigue consumiendo (lag por grupo).
- **P8 — Attest.** `echo-runtime-control attest ...` → EXTERNAL CLEAN (G9b). Publicar evidencia (reporte firmado + digests).
- **P9 — Core repoint.** En .161: `releases/4a041e6c…/echo-core` + `systemctl --user restart echo-core-dev` (unidad única; Gateway/front intactos). Verificar journal (recovery authority leída, freshness producer activo, sin errores ETCD/PG).
- **P10 — Cierre.** Nuevo checkpoint COMPLETED sobre el release nuevo (G11a) → `seal` gen N+1 SIN flag de migración (STRICT para siempre; el seal rechaza re-abrir) → copia off-host del nuevo corte → monitoreo 30 min (G10: FX lag≈0, 0 restarts) → ventana cerrada. Estado final: `READY_DISARMED` (Futures sin armar; armado = gate Owner aparte).

### 8. NO-GO parciales declarados

- **P2 falla (savepoint no COMPLETED):** **STOP ANTES DE P5.** No continuar automáticamente con el checkpoint incremental P1: `num-retained >= 10` o mantener los SST del original NO demuestra portabilidad ni permite acreditar una recuperación independiente. Sólo una alternativa documentalmente equivalente, restaurable desde una copia sin depender de origen y sellada como EXACTAMENTE el corte restaurado puede volver a plantear GO al Manager/Owner.
- **P7 falla (sweep incompleto/timeout):** R1. NO reintentar la migración más de UNA vez sin dictamen del Manager (un fallo deja cero evidencia ETCD; segundo fallo = R1).
- **P9 falla (core no arranca con el release nuevo):** repoint al release anterior + restart core; el job DEV sigue con markers migrados y manifest gen 1 (compatibles con el core GI-2); cerrar en degradación documentada.

### 9. Rollbacks y cinco capas de desarme

- **R1 (pre-efecto, hasta P7 inclusive):** stop compose; restaurar `module.yaml` + `flink-conf.yaml` + compose desde los backups de P4; gate con el manifest ANTERIOR (o bootstrap-state previo si no había manifest) apuntando al checkpoint ORIGINAL (P1 nunca lo borra ni mueve); arrancar; verificar FX consumiendo + `latest.restored`.
- **R2 (post-efecto, después de P8):** NO se retrocede al snapshot anterior (ya hubo procesamiento): forward-fix con el estado actual; única excepción P9 (el job nunca dejó de ser autoridad). Jamás `--allow-bootstrap` ni arranque sin restore-args.
- **Cinco capas de desarme — estado PRE (2026-10-26T23:30Z) y verificación POST obligatoria:** (1) armado ETCD: `futures-bridge/accounts/E2T-GAU50-01/binding/enabled=false` verificado; (2) listener de ejecución: sin `:9771` en .161 (sólo `:9770` feed de observación); (3) proceso: sin `futures-bridge` corriendo en .161; (4) terminal NT .132: sin binding de ejecución armado según última autoridad PRD.5 (feed NO_INICIADO) — re-verificar en ventana; (5) autoridad económica: G-SIM=BLOCKED, Sim101 no armada, PROD intacto (cero escrituras). La ventana no cambia ninguna de las cinco: el POST debe leerlas IDÉNTICAS.

### 10. Evidencia a producir en ventana

`/opt/echo/recovery/manifest-<gen>.json` + anexos; stdout de seal/attest/continuity-migrate; salida de la sonda; sha256 manifiestos off-host; REST snapshots (jobs/checkpoints pre/post); journal del core; capturas de las cinco capas PRE/POST. Todo con fecha UTC y comando ejecutado.

## Fuentes

- [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]] (autoridad de la ventana) y [[EF-PROD-PRD6-RECOVERY-MIGRATION-CLOSURE-20261026]] (evidencia técnica).
- Borrador fuente: `~/aranea/work/ef-prd6-20261026/evidence/WINDOW-CARD-PRD6.md`; release construido: `/home/kor/opt/echo-dev/releases/4a041e6cf17b27a023a1a693a48be1034c35e7dd/BUILD.md`.
- Verificación física fase 0 (2026-10-26T23:30Z): Flink/Kafka/ETCD MCP, SSH `docker-echo-dev-operator` (.75), local .161; [[OWNER-CHECKLIST-CERT-NT-01]] y planner [[Echo Futures — Runtime Pools]].
