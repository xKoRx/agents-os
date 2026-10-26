---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
  - "[[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]]"
  - "[[EF-PROD-GI2-CONTINUITY-CLOSURE-EVIDENCE]]"
  - "[[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# EF-PROD PRD.5 — Preflight DEV read-only + campaña de cobertura (2026-10-25/26)

## Propósito

Evidencia consolidada de la ejecución PRD.5 (mandato Owner 2026-10-25, decisión Primary Manager 2026-10-25 addendum [[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]]): Trabajo A preflight READ-ONLY del Flink DEV existente, Trabajo B QA de cobertura, preparación del release inmutable `0e17c4d3` y tarjeta de despliegue observation-only. **Ninguna mutación de servicios; PROD intacto; el despliegue DEV queda PENDIENTE DE VENTANA OWNER** (reinicio compartido FX+Futures). Ejecutado por Submanager GLM-5.3-Flash LOCAL; el Manager no reejecutó estas mediciones.

## Veredicto

```text
STATUS: DEV_READY_FOR_OWNER_WINDOW
SOURCE_SHA: 0e17c4d3f1179cde709f923c8dd28e8cd853afc9 (+ QA c2d71357: 11 *_test.go + 1 script de tooling, cero producto)
DEV_FLINK_EXISTING: stack Compose `flink` @ .75 (/data/compose/1, Portainer) — statefun-master+worker apache/flink-statefun:3.2.0-java11; job StatefulFunctions jid 0f6901a3 RUNNING 43h, chk-1286 COMPLETED (restored:0), checkpoints en disco host, savepoints VACÍOS
PROD_UNTOUCHED: SÍ — Echo PROD nativo en .71 (sin Docker/Flink), Kafka PROD .247-249, ETCD /echo/production/ separado; sólo lecturas RO
DEPLOYMENT_METHOD: actualizar archivos del MISMO deployment (module.yaml + flink-conf en /root/statefun, edit mínimo del compose con gate+restore-args+bind /opt/echo, recreate del master; Core: repoint release + systemctl --user restart echo-core-dev)
CHECKPOINT_RESTORE: compatible demostrado por diseño (ValueSpecs: sólo añade estado `Continuity`; 17 tuplas de ingress idénticas; GI-2 L3 aislado S1 PASS) — la demostración física en DEV real es el PASO 5-6 de la ventana
STATE_CONTINUITY: offsets FX committed=HWM (lag≈0, fin de semana); binding único DESARMADO (enabled=false); sin órdenes
FX_IMPACT: sólo la pausa del restart compartido en la ventana (datos retenidos en Kafka, offsets por checkpoint); sin exposición económica
M1: hoy at-least-once EFECTIVO (módulo desplegable sin deliverySemantic); el release lo sube a EXACTLY_ONCE transaccional (7 de 8 egress; system-events queda at-least-once por diseño GI-01)
MARKET_FRESHNESS: key ETCD ausente hoy; el release añade el productor real (GI-RDY-P1)
NINJA_FEED: NO_INICIADO — requiere ventana + control Owner (mandato paso 10, después del deploy)
COVERAGE_NEW: 2532/2734 = 92.61% (GI-2: 82.92%) — BAJO piso GOD-03
COVERAGE_DIFF: 409/518 = 78.96% observado (GI-2: 76.45%), exit 1 SIN fallo de método; 9 archivos RESUELTOS DECLARATION_ONLY — BAJO piso GOD-03
ROLLBACK: R1/R2 definidos, ambos con restore SIEMPRE (checkpoint host-retained); jamás arranque fresco
NEXT_PHYSICAL_GATE: ventana Owner (reinicio compartido job DEV) → pasos 0-8 de la tarjeta → luego feed Ninja observación (paso 10, control Owner)
AGENTS_OS_READBACK: planner PRD.5 actualizado + este documento + agent-run + change_log (commit documental verificado por Git)
```

## 1. Preflight DEV AS-BUILT (read-only, 2026-10-25)

- Host .75 (perfil `docker-echo-dev-operator`): contenedores `statefun-master` (43 h, REST host 8082→8081) y `statefun-worker` (3 d), imagen `apache/flink-statefun:3.2.0-java11`; proyecto Compose `flink` en `/data/compose/1` (Portainer); mismo host aloja `hasura-graphql` DEV y Portainer.
- Entrypoint efectivo del master: `/docker-entry-point.sh` OFICIAL **sin argumentos** (auto-deploy por módulo; sin gate ni restore — el estado GI-REC-P0 confirmado en source está presente en el runtime). `RestartPolicy: unless-stopped`.
- Binds: `flink-conf.yaml` ro (`/root/statefun/conf/`), `modules` ro (`/root/statefun/modules/`), checkpoints/savepoints **rw en disco del host** (`/data/compose/1/statefun/{checkpoints,savepoints}`). Flink 1.14.3, 1 TM/2 slots, HA none, restart fixed-delay 3×5s, checkpoint interval 120s **AT_LEAST_ONCE**, RocksDB incremental, `num-retained=1`.
- Módulo desplegado: `/root/statefun/modules/application/module.yaml` (20.768 B, mtime 2026-10-22 21:01, corte FEFB S2) con backups CERT-NT-01 en el mismo dir. 17 ingresses (FX + futures) → endpoint `http://dev.echo.core.lab.aranea:9090/statefun`; 7 egress **sin `deliverySemantic`** ⇒ M1 at-least-once efectivo hoy.
- Job vigente `0f6901a3…` RUNNING desde 2026-10-24 ~04:42 UTC: 19 vértices × 2 = 38/38 tasks, 0 excepciones; checkpoints 1286+ COMPLETED / 0 failed / **0 restored**; `chk-1286` ~2.9 MB en disco host; **directorio de savepoints VACÍO**.
- Consumo sano: grupos `echo-statefun-*` EMPTY en admin (StateFun usa assign sin membresía clásica) con offsets committed al día (lag≈0): account-snapshots lag 120/10 particiones; market-feed committed=HWM=45.142.540 (p4); trade-closes lag 4; pool-config y strategy-config 9/9.
- Core DEV (Daedalus .161, este host): `echo-core-dev` ACTIVE desde 2026-10-23 (release `ac0621a1`, deploy CERT-NT-01-F1); registra los 7 owners futures (market_stream 11 states, market_analytics 14, strategy_engine 3, signal_fanout 1, operation 1, provider_rules 1, pool_manager 1) y publica bootstrap idempotente `certnt01-pool` config_version=1. Gateway/front ACTIVE.
- ETCD DEV `/echo/development/`: 78 keys; `futures/enabled=true`; **`futures-bridge/accounts/E2T-GAU50-01/binding/enabled=false` ⇒ DESARMADO** (único binding); `futures/config_snapshot` y nt-feed configurados; `futures/market/freshness` ausente (llega con el release).
- Kafka DEV `.44:19091-96`: todos los topics del módulo vigente existen; **falta `echo.futures.recovery-attest.v1`** (ingress nuevo del release) — pre-crear en ventana o verificar auto-create.

## 2. Separación PROD (comprobación read-only)

PROD Echo corre **nativo** en .71 (perfil viewer): `/home/kor/echo/echo-core|echo-functions|echo-gateway` desde 2026-10-20, sin Docker ni procesos Flink; `echo-lab-worker` (cron del owner) ajeno a esta sesión. Kafka PROD `.247-249:9092` (ETCD `/echo/production/kafka/brokers`) ≠ Kafka DEV; namespace ETCD `/echo/production/` (37 keys) separado de `/echo/development/` (78). Ninguna escritura PROD.

## 3. Delta del release `0e17c4d3` vs desplegado + compatibilidad

| # | Delta | Impacto |
|---|---|---|
| 1 | `deliverySemantic: {type: exactly-once, transactionTimeout: 15 min}` en 7 de 8 egress (`system-events` queda at-least-once por diseño GI-01/C-KAFKA-1) | M1 EXACTLY_ONCE transaccional |
| 2 | Ingress nuevo `echo/futures-recovery-attest-ingress` → topic `echo.futures.recovery-attest.v1` (NO existe aún), grupo `echo-statefun-recovery-attest`, latest, target `echo/recovery_attestor` | Topic a pre-crear en ventana |
| 3 | Egress nuevo `echo/futures-recovery-attest-report-egress` (exactly-once) | Evidencia de recovery firmada |
| 4 | flink-conf: EXACTLY_ONCE, interval 10s, timeout 60s, min-pause 200ms, `RETAIN_ON_CANCELLATION` | Compatibles con restore del checkpoint vigente |
| 5 | Compose: gate `echo-runtime-control` + `master-restore-args` obligatorio + exec entrypoint oficial; env ECHO_* obligatorios; bind `/opt/echo` (binario + storage recovery) | Requiere binario del release montado al master |
| 6 | ValueSpecs: nombres/tipos vigentes SIN cambios; ADITIVO (cada owner añade `Continuity` al final; market_stream preserva su lista congelada) | **Restore desde chk-1286 compatible**; nuevos owners empiezan vacíos |

## 4. Tarjeta de despliegue (archivo-por-archivo) y ventana

Regla rectora: **un solo deployment (proyecto Compose `flink` @ .75); PROD intacto; ninguna cuenta armada; ante fallo, rollback antes de reintentar; jamás arranque sin restore args.**

Comando de descubrimiento: `ssh root@192.168.31.75 'docker ps --format "{{.Names}} {{.Label \"com.docker.compose.project\"}}"; ls -la /root/statefun/modules/application/ /data/compose/1/statefun/checkpoints/0f6901a3a9aee496b408cbb5e4d0afeb/ | tail -5'`

| Archivo (host .75) | Hoy | Acción | Origen |
|---|---|---|---|
| `/root/statefun/modules/application/module.yaml` | 20.768 B FEFB | BACKUP → REPLACE por `develop/module.yaml` de `c2d71357` (wiring idéntico al de `0e17c4d3`: los tests QA no cambian manifiestos) | repo `c2d71357` |
| `/root/statefun/conf/flink-conf.yaml` | AT_LEAST_ONCE/120s | BACKUP → REPLACE por `develop/flink-conf.yaml` | repo `c2d71357` |
| `/data/compose/1/docker-compose.yml` | sin gate | BACKUP → EDIT mínimo: entrypoint gate + env ECHO_* + bind `/opt/echo` ro | tarjeta del workspace §4-5 |
| `/opt/echo/bin/echo-runtime-control` | no existe | ADD binario release sha256 `2e9f4034…` | release local `0e17c4d3` |
| `/opt/echo/recovery/` | no existe | ADD storage (manifest + roster + master-restore-args) generado por `seal`/`bootstrap-token` en ventana | gate CLI |
| topic `echo.futures.recovery-attest.v1` | no existe | ADD (pre-crear) o verificar auto-create | MCP Kafka DEV |
| Core `current` (Daedalus) | → ac0621a1 | REPOINT → `releases/0e17c4d3…` + restart `echo-core-dev` (unidad única) | release local BUILD.md |
| PROD (todo) | intacto | KEEP — NO TOCAR | — |

Procedimiento (0-8) y rollback R1/R2 completos en el workspace `~/aranea/work/ef-prd5-20261025/evidence/PREFLIGHT-AND-DEPLOY-CARD.md` §5-6 (insumos también en `briefs/` y `evidence/{A,B}-REPORT.md`). Release inmutable local: `/home/kor/opt/echo-dev/releases/0e17c4d3f1179cde709f923c8dd28e8cd853afc9/` (echo-core `f13ae3a8…`, echo-runtime-control `2e9f4034…`, `vcs.modified=false`; gateway `3751227d…`/relay `98ed260b…` verbatim con cadena de hashes íntegra). `current` NO fue repointeado.

## 5. Trabajo B — campaña de cobertura (resultado honesto)

**Base del delta `ac0621a1`; tip medido `c2d71357`** (= `0e17c4d3` + 11 `*_test.go` +3.021 líneas + 1 script de tooling; merges `--no-ff` `20b653b9`+`c2d71357`, ownership disjunto, push FF REMOTE_VERIFIED; build/vet/tests del tip PASS con los skips heredados declarados). Workflow ZCode secuencial (2 workers one-shot + gates deterministas; runs `dwfrun-e95d77dd`→`dwfrun-6ab38093`).

- **Métrica global (archivos nuevos): 2532/2734 = 92.61%** (GI-2: 2267/2734 = 82.92%) — +265 bloques reales. Aportó A: runtime-control 437→665/783 (665 = máximo alcanzable sin broker Kafka wire/ETCD/señales); aportó B: recovery attestation/manifest/digest a 100%, freshness producer 62→68/102, attestor wiring 4→9/10, permit freshness 100%.
- **Métrica diff-aware (observado): 409/518 = 78.96%** (GI-2: 396/518 = 76.45%), **exit 1 sin fallo de método**.
- **Los 9 archivos "sin observación" RESUELTOS por método**: clasificación `DECLARATION_ONLY` con clasificador go/parser (fail-closed: cualquier línea stmt/other o parse-error ⇒ exit 2 en fresh) y evidencia por archivo (p.ej. `interfaces.go added=9 comment=5 decl=4 stmt=0 other=0`) — son comentarios/campos/consts/imports sin una sola sentencia ejecutable: no había nada que observar y ahora el método lo demuestra, sin exclusión silenciosa.
- **AMBAS cifras siguen BAJO el piso GOD-03 ≥95%** — no se declara PASS. Brecha restante clasificada en los reportes de workers: (a) **no ejercitable en unit sin mutar producto** (dial `sarama.NewClient` sin seam, ETCD client real, entry-points `main()` con señales/dial, marshals defensivos, `os.Hostname`): ~150 bloques; (b) **alcanzable, fuera de presupuesto de este ciclo** (ninjatrader/adapter 15, bridge/internal 22, futures-projector producer 7, attest_report 4, functions default-legs 10, market engine 5, varios 1-3): ~68 bloques — ruta de cierre recomendada si el Manager ordena otra ronda.
- Perfiles: 101 por corrida, 0 FAIL, mismos skips heredados declarados (ACCEPTANCE-MATRIX). Reportes: `/tmp/ef-prd5-cov-new/coverage-report.md` y `/tmp/ef-prd5-cov-diff/diff-coverage-report.md` (efímeros; cifras embebidas aquí y en los reportes de workspace `evidence/{A,B}-REPORT.md`).

**Defectos del orquestador divulgados (no de los workers):** (1) gate `go build ./v3/...` estructuralmente inviable en el go.work multi-módulo (falla también en BASE puro) — Worker A lo escaló sin tocar go.work; corregido a `github.com/xKoRx/echo/v3/...` vía AmendWorkflow con cache. (2) Gate B corrió el script con cwd del vault (`world.run` no fija cwd ⇒ denominador 0 y "bad object ac0621a1") — la verificación válida fue re-ejecutada por el integrador desde dentro del worktree (exit 1, 9/9 DECLARATION_ONLY). El commit `2f4e522e` de B endureció el script ante repo ajeno (fallback emparejado sólo en `--use-profiles`; fresh sigue exit 2): revisado, no debilita el método.

## 6. Incidentes divulgados de esta sesión

(1) Verificación de versión vía ejecución del binario (`echo-core --version`): segundo core ~1 s que republicó bootstrap idempotente v1 (absorbido, verificado 9/9 consumido), rebalance transitorio `echo-core-v3`, salida por puerto ocupado; sin impacto FX ni del job. Lección: `go version -m`. (2) MCP SSH expiró tras el inventario (requiere reinicialización antes de la ventana); Kafka/Flink/ETCD MCP operativos toda la sesión.

## Fuentes

- Addendum «Re-review y decisión operativa 2026-10-25» en [[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]]; [[EF-PROD-GI2-CONTINUITY-CLOSURE-EVIDENCE]]; [[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]; planificador [[Echo Futures — Runtime Pools]] (PRD.5).
- Workspace externo `~/aranea/work/ef-prd5-20261025/`: `evidence/PREFLIGHT-AND-DEPLOY-CARD.md` (tarjeta completa), `evidence/{A,B}-REPORT.md` (adjudicaciones bloque a bloque), `briefs/{A,B}.md`.
- Release local `/home/kor/opt/echo-dev/releases/0e17c4d3…/BUILD.md`; repo `xKoRx/echo` `feature/ef-runtime-pools@c2d71357` (REMOTE_VERIFIED).
