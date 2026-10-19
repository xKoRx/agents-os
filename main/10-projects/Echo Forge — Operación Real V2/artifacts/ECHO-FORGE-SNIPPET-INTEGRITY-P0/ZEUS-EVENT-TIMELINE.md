# ZEUS-EVENT-TIMELINE — Snippet Integrity P0 (2026-10-19)

Zona horaria: horas locales de Zeus = UTC-3; todos los eventos abaixo en UTC (Z). Anclaje: `date`/`date -u` en Zeus 22:04:35Z = 19:04:35 local.

## Antes del incidente

| Momento (Z) | Evento | Evidencia |
|---|---|---|
| 2026-09-06 10:13:10 | Instalación inicial del plugin EchoForge en Zeus: snippet `EchoForgeOverviewExporter.java` (73.993 B, SHA `03106b81…`) + resto de snippets del dir, owner `echo-dev:echo-dev` 664 | mtimes sep-6 idénticos en todo `CustomAnalysis`; copias gemelas en `sqx/142` y `sqx/user` |
| 2026-10-18 01:21 / 09:46 | Rollout S01 (18-oct) actualizó en Zeus SOLO los JARs (`EchoForgeAutomator.jar` 143.407 B, `Snippets.jar` 1.459.151 B) — **el snippet fuente quedó en sep-6** | mtimes de los JARs respaldados en `backup/plugin-s02-20261019T180331Z/`; hallazgo S01 "snippets.txt hash-keyed / jar stale" |
| 2026-10-19 16:31:22 | Bundle S02 subido a Zeus (`/tmp/s02-rollout/src/...java`, 87.157 B `b5f85c4e…`, mtime preservado por `cp -a`) | stat de `/tmp/s02-rollout/src` |
| 2026-10-19 ~16:53 | Worker symphony 0.3.2 activo en Zeus (PID 2933209) | `ps aux` |

## Incidente (deploy S02)

| Momento (Z) | Evento | Evidencia física |
|---|---|---|
| 18:03:31.749 | `deploy-plugin-s02.sh` (SHA `b52addbe…`, como kor vía SSH exec sin pty — no deja wtmp) inicia; backup de estado previo | `SHA256SUMS.before` mtime 18:03:31.761Z: snippet `03106b81…` + JARs oct-18 |
| 18:03:32.86–.89 | Compilación OK contra SDK local (8 clases, main `3ec6e112…`) | mtimes `target-prod/classes` |
| 18:03:33.4 → 34.425 | Swap `user/libs/EchoForgeAutomator.jar` aplicado (kor-writable) | mtime 18:03:33.401Z, ctime (rename) 18:03:34.425Z; dir `user/libs` ctime 18:03:34.425Z |
| 18:03:34.429 | Swap `internal/libs/Snippets.jar` aplicado | dir `internal/libs` ctime 18:03:34.429Z |
| 18:03:34.43x | **Línea 95 (swap del snippet): `cp` → EACCES silencioso, `mv` no ejecuta, script continúa** | kor no tiene w en el dir (`775 echo-dev:echo-dev`); ctime del dir demuestra que jamás hubo chmod |
| 18:03:34.439 | Sello `SHA256SUMS.after` escrito: **src `b5f85c4e…` / live `03106b81…`** — la prueba física del swap omitido | backup `plugin-s02-20261019T180331Z/` |
| 18:03:34.440 | `rollback.sh` generado; script reporta `DEPLOY OK` | mtime rollback.sh |
| 18:03:57 → 18:04:28 | **Canary 1** (`ef-canary-s02-180357`, 3 estrategias): ejecuta exporter **v1.2** (0 markers `Parallel workers`, recompila desde el fuente sep-6), rc=0 | `canary-run.log`, `overview_databank_20261019_180412.log` (header v1.2, `processed 3/3`) |
| 18:04:05–18:08:54 | Estado previo del cache `internal/tmp/compiled` respaldado manualmente (clases viejas 50.876 B) | `backup/.../tmp-compiled-cache/` |
| 18:09:24 → ~18:09:5x | **Canary 2** (`ef-canary-s02-180924`): también código viejo (0 markers) | `canary-run.log` (147.521 B) |
| 18:22:43.495992 | **Corrección real**: fuente S02 instalado como `echo-dev:echo-dev` 664 (canal echo-dev operator — sin sudo; chown a propio uid es no-op válido) | mtime/ctime del snippet y ctime del dir, todos 18:22:43.495992274Z |
| 18:23:02 → ~18:23:4x | **Canary 3** (`ef-canary-s02-182302`): PASS, marker `Parallel workers: 3`, 3/3 filas | `canary-run.log`, `.s02-canary-last` |

## Post-incidente (estabilidad observada)

| Momento (Z) | Evento | Evidencia |
|---|---|---|
| 18:47–18:49 | E2E w11: CustomAnalysis del builder con ruta paralela S02 (doc 2m10s) | PLUGIN-ROLLOUT-3OF3 / E2E-CPU-PERFORMANCE |
| 19:02–19:17 | Sesión interactiva `echo-dev` desde `192.168.31.219` (post-incidente, sin relación causal) | `last -a` |
| 19:05:38–19:27:27 | 10 runs del proyecto flota `EchoForgeOverviewExporter` (cert CPU REAL_COMPUTATION) — cada run recompila desde el fuente S02 | `log/global_log_20261019_19*.log` |
| 19:35–19:49:41 | 10 runs proyecto `custom` (cert CPU); **el último reescribe TODO el cache + `Snippets.jar` desde el fuente S02** (mecanismo per-run de Build 144) — coherente, benigno | cache + jar mtime uniforme 19:49:41Z; clase extraída = `3ec6e112…` |
| 22:3x–23:0x | Gates de integridad read-only de esta investigación: PASS 3/3 hosts (ver matriz) | `RUNTIME-IDENTITY-MATRIX.csv` |

## No-intervenciones

Se mantiene el contrato de la investigación: cero reinicios, cero caches vaciados, cero ownership tocado, cero campañas interrumpidas (el sqcli activo durante la sesión se respetó; la reproducción fue candidate-local sin sqcli y los gates son de sólo lectura).
