# STEALTH-WATCHERS-CLOSED

Fecha de cierre: 2026-10-06 (~19:30 local). Mandato: STEP 0 de la migración Z.AI (`zai-rebaseline`). El Owner seleccionó OPTION_B (migrar a Z.AI/glm-5.3-flash); un retorno del endpoint stealth NO debe relanzar una corrida de aceptación obsoleta. Evidencia histórica preservada, nada borrado.

## Watchers localizados y estado final

| Watcher | Script | Dir de ejecución | Ventana de sondeo | Probes | Último probe | Estado final | Acción de shutdown |
|---|---|---|---|---|---|---|---|
| Track A resume (P7c) | `wait-and-resume.sh` | `~/mke/clutifx-ch01-rerun3-20261005/` | 2026-10-05 16:10Z → 2026-10-06 16:10Z (cada 15 min, tope 96 ≈ 24h) | 96/96 HTTP 404 | 2026-10-06T15:55:58Z | **Agotó tope y salió solo** ("TOPE 24h alcanzado sin retorno del modelo") ANTES del cierre | Renombrado a `wait-and-resume.sh.DISABLED-by-zai-migration` + `chmod -x` |
| Manager P8/P9 fresh-launch | `watch_fresh_launch.sh` | cd `~/mke/clutifx-ch01-rerun3-20261005/` (script creado en staging `…20261006/`) | 2026-10-06 03:05Z → 2026-10-06 19:06Z (cada 10 min, tope 96 ≈ 16h) | 96/96 HTTP 404 | 2026-10-06T18:56:17Z | **Agotó tope y salió solo** ("TOPE 16h sin retorno del modelo") ANTES del cierre | Renombrado a `watch_fresh_launch.sh.DISABLED-by-zai-migration` + `chmod -x` |
| Launcher staging (track A, día 05) | `probe_and_launch.sh` (ya `.DISABLED` previo) | `~/mke/clutifx-ch01-rerun3-20261006/` | 8 probes "probe dead" hasta 2026-10-06T02:59:51Z | 8 | 2026-10-06T02:59:51Z | Ya inert antes de esta migración | Sin acción adicional (evidencia preservada) |

## Verificación de procesos vivos al cierre

- `ps -u kor` filtrado por `mke|clutifx|rerun|openrouter|watch|resume`: **0 procesos de vigilancia stealth vivos** al momento del cierre (solo `deployer-watcher` PID 4185897/4186093 de otro repo, bucket `./deploy`, ajeno a MKE/stealth — no tocado).
- `crontab -l`: solo `sync.sh` del vault (sin watchers MKE). `/etc/cron.d/`: solo `e2scrub_all` (sistema). `atq`: vacío. `tmux ls`: sin sesiones. systemd user: sin unidades MKE/stealth.

## Consecuencia operacional

- Ningún watcher relanzará `run-rerun3c`/`run-rerun3` con el provider stealth aunque el endpoint vuelva. La campaña continúa exclusivamente por la migración Z.AI re-baseline (nuevo modelo = nuevo baseline semántico; el resume P7c con fingerprint stealth quedará obsoleto por diseño).
- Errores del endpoint: 404 "No endpoints found for stealth/space-bunny-alpha" durante toda la ventana sondeada (coincide con la retirada del endpoint del 2026-10-05).
- Los 3 watchers consultaban OpenRouter con la credencial del env `~/mke/.secrets/openrouter.env`; ese env NO fue modificado ni leído en contenido para este artefacto.
