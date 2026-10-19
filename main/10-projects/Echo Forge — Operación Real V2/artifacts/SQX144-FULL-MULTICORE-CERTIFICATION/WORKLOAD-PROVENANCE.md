---
type: evidence
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# WORKLOAD-PROVENANCE — identidad, procedencia y sellos de la certificación

## Baseline de código y release

- Repositorio `xKoRx/symphony`, HEAD verificado `492a271e84f1faa1d4050b7ab35255863b2992e5` (release 0.3.1, master) — clones locales verificados en `~/aranea/work/sqx144-supply-remediation-20261018/symphony` y `~/aranea/work/sqx144-cpu-20261018/symphony`.
- El harness de certificación corre sqcli DIRECTAMENTE (candidate-local); no usa workers productivos ni despliega releases. `PRODUCT_MUTATIONS: NONE`.
- Fuente del builder certificado: `input/00_configs/builder_test.cfx` del repo @ 492a271e (el builder de los flujos E2E). SHA del cfx fuente: `cc4b0abfb931410b…`; cfx desplegado fc-build v5 (símbolo 2 → XAUUSD_dukascopy por datos del host): `812dc3cb9c3d0c93…` — idéntico en los 3 hosts.
- Fuente del retester: proyecto real de campaña w10 (`/tmp/cpx/project.cfx` en Kronos, SHA `de8b3ac8…` — idéntico en los 3 hosts).
- Fuente del optimizer: task WFO de campaña (`/tmp/cpopt/Optimize-Task1.xml`, SHA `79d5d9dd…`); builder maratón: Builder_G1 (`/tmp/bg1/config.xml`, SHA `e661d258…`).

## Instalación SQX y licencia

- Instalación productiva de referencia por host: `/home/kor/sqx/144` (SQX 144.2953). Candidate-local LEAN en `/home/echo-dev/forge-cert-20261018/sqx144-cert/` (copia de `user` sin History/logs/projects + symlinks a j64/internal/History productivos) — construida por `fc-workspace.sh`, instalación productiva intacta.
- **Binario sqcli idéntico en los 3 hosts**: SHA256 `7d312106112c07fad5b49e55079f50854e87ea3af2a86b54ebf4bd306e030702`.
- settings.xml por host (sellados en `state/install.sha256`): coreUsage=100%, highPriority=true, threadAffinity=false.
- Licencia: verificada en runtime por cada smoke en los 3 hosts (bloque `Verifying license ...` OK + runs completando; hardware ID estable por host).
- Cores reconocidos por SQX (consola): Kronos "Using: 72 cores", Hera "Using: 60 cores", Zeus "Using: 24-27 cores" (ajuste propio del coreUsage sobre 28 vCPU).

## Corpora (auténticos, congelados, separados por prueba)

| Corpus | Procedencia | SHA manifiesto |
|---|---|---|
| `overview1117` (823 .sqx) | estrategias auténticas de campaña (subset de la campaña overview, congelado desde P0) | `rec/fc-retest-n*-input.sha256` por run/host |
| `corpus-pristine` (24 .sqx) | corpus pristine w10 (S02), grupo del optimizer independiente | `rec/opt-XX-source.sha256` por run/host |
| Output del builder (20 .sqx) | generadas EN esta certificación (builder_test) | `state/builder-output.sha256` |
| Cohort integrado (10 .sqx) | subset determinista (uniforme 10/20 ordenado) del output del builder | `state/cohort.sha256` + `state/cohort-list.txt` |

El corpus se transportó Kronos→Hera/Zeus por HTTP LAN con verificación SHA256 del tarball (`19b9a8bf…` en destino) — byte-idéntico.

## Harness y sellos de ejecución

- Harness `fc-*` (v driver `a06e6cce…`, analyzer `fc-analyze.py` final): instalado byte-exacto por HTTP+SHA en los 3 hosts.
- Timeline por host en `logs/campaign.log` (marcadores `== S1…S6`, `FC_PREP_OK`, sellos `continuity seal … = 0`, `CAMPAIGN_COMPLETE`).
- Campaña: smoke DONE → ladder DONE → optimizer group DONE → builder DONE → cohort DONE → analyze DONE, en los 3 hosts (2026-10-19 04:45-04:56Z).
- Guard de instancia única: `FC_PREFLIGHT_FAIL` count = 0 en los 3 logs (nunca hubo 2 SQX por VM).
- Cruces con productivo: cero. El workflow ajeno `sqx-main-v1-ab32f685` (wave3f NDX) quedó intacto y sin actividades; ningún CFX del Owner modificado; ETCD/PG/MinIO/servicios intactos.

## Instrumentación

- CPU del grupo de procesos (pgid del sqcli) cada 200 ms vía `/proc/*/stat` (utime+stime, CLK_TCK=100 verificado).
- CPU por thread (per-tid) cada 1 s + contador RUNNABLE + hasta 8 snapshots `jcmd Thread.print` en fases calientes.
- Poller de bytes de consola cada 2 s (datación de fases por offset→timestamp).
- `/usr/bin/time -v` por run (wall + MaxRSS).
- Estado intermedio del builder vía HTTP API local de SQX (`-project action=status`).
- Análisis por run: `fc-analyze.py` → `analysis/<label>.json` (fases boot/calc/save con medias integrales jiffies, pico5, fracción hot, threads).

## Raw en hosts (no copiado al vault, ~1-2 GB total)

`/home/echo-dev/forge-cert-20261018/{rec,analysis,state,logs}` en sqx-zeus, sqx-hera y sqx-kronos (usuario echo-dev). Los CSV de CPU/threads, consolas completas, sellos SHA y JSON de análisis permanecen allí; el vault lleva las matrices y resúmenes derivados.
