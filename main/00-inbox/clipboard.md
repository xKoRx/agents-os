La semana quedó armada y el reloj de siete días todavía no partió. El servicio está activo y abre la primera captura solo en la ventana T−90.

## SPORTS_WEEKLY_CAMPAIGN_ACTIVATION

| | |
|---|---|
| Estado | `ARMED_WAITING_NEXT_WINDOW` |
| Publicado | `origin/master` = `origin/main` = `bfa6eaf` |
| Código | `c3b1aa1` |
| Binario | `vcs.revision=bfa6eaf`, `vcs.modified=false` |
| Certificado | `M4_CERTIFIED_NON_LIVE`, pin `c3b1aa1`, 27 PASS / 0 FAIL / 5 diferidos live (G-16, G-17, G-18, G-19, G-14b) |
| `started_at` | null |
| Próxima ventana | 2026-09-21T21:05:00Z, mercado 4584879, kickoff 22:35Z |
| En espera | 91 moneylines MLB (`series_id=3`) |

**Fee.** El tope publicado (Gamma/CLOB, en sports 1000 bps) y la fee del trade son identidades distintas. Si el trade cae dentro del tope, la resolución es INTERVAL `[0, cap]`. Si se sale del tope, o si dos trades de la misma identidad no convergen, sigue SUSPECT. Un trade convergente sin tope declarado sigue siendo POINT de ese trade. `REAL_FEE_READY=false`. `LIVE_DISABLED`. El parche U-02 `d5ce263` no se integró.

**Canary (90 s, mercado 4584879).** 45 frames recibidos, 36 admitidos, frontera durable 39. Los dos libros quedaron `OBSERVED_USABLE`. La observación de trade `"0"` quedó en el seq 29. `suspect=false`, cuarentena 0, cap declarado 1000/1000. Replay de los schedules `1` y `32,7,1` con el mismo digest `844a9392eaea0eccf3555d3eb0eda0b329c5d10c3cfecde86e729b47f6ee8e86`. `journal verify` en 0.

**Gates.** `go vet`, `go test ./... -count=1` y `go test ./... -race -count=1` verdes. `feeresolver.go` al 100%.

**Servicio.** Unidad user `sports-week-capture` activa. Timers `sports-week-health` (5 min) y `sports-week-analyze` (1 h) habilitados. Linger del usuario ya estaba en yes. Health ahora: `NO_GAMES_SCHEDULED`, proceso de grabación ausente, 91 mercados en espera. Dataset `sports-week-pe005`. Disco libre al armar: 18.8%. Bajo 15% no abre sesión nueva; bajo 5% cierra el journal y se detiene. No borra evidencia.

**Experimentos congelados antes de capturar.** `window_ms=300000`, `ref_frames=10`, `widen_min_bps=50`, `entry_budget=25`, `min_net_edge_bps=50`, `taker=true`, `cuts=30`. Universo por identidad y kickoff. Economía `NOT_CERTIFIED`. Una ventana sin señales se conserva. SHADOW corre solo sobre copia de un journal ya cerrado.

**Alertas.** No hay canal externo. El health deja el reporte en el dataset y, si la captura se rompe, un JSON en `alerts/`.

El reloj de siete días se escribe en `started_at` cuando parta la primera captura T−90, y un reinicio del servicio no lo pone de nuevo en cero.s