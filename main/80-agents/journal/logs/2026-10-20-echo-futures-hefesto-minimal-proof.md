---
type: journal
schema_version: 1
created: "2026-10-20"
entities:
  - "[[Echo Futures]]"
tags:
  - kind/journal
---

# 2026-10-20 — Echo Futures: hefesto nuevo host oficial del backtest + prueba mínima de máquina

- El Owner declara hefesto (192.168.31.164, 16 GB RAM) host oficial del backtest Echo Futures en reemplazo del host anterior de 96 GB (daedalus 192.168.31.141), hoy sin ruta. El estado 13/26 y el cierre final quedaron descritos en [[TRADESGERARD-CONTROL]] (corte 2026-10-20).
- Recuperación de continuidad vía RUNBOOK-CONTINUIDAD-20261019 del repo `xKoRx/echo` rama `experiment/challenge-history-20261018` @ `48aaf5f7`: 13 filas COMPLETE_RECONCILED (12 r4 + MR-03 r5); r5 con las 13 restantes se perdió con el host; recuperación por copia de `/srv/echo-work` (host encendido) o RUTA B (asset r4 del release GitHub, requiere gh+token; repo privado verificado).
- Prueba mínima en hefesto PASS: build `-p 1` de echo-backtest/ntdigest/planfix exit0; suite Go del gate `ok v3/backtester 8.563s`; tests Python challenge-history 37/37 OK.
- Hallazgo ambiental nuevo: `/tmp` tmpfs de 7 GiB < reserva de plataforma 8 GiB (`platform_search.go:213`); mitigado con `TMPDIR` en disco. patrón candidato para memoria L3 si se repite en otra máquina.
- Entidad afectada: [[Echo Futures]]. Delta en [[TRADESGERARD-CONTROL]] corte 2026-10-20. Sin LIVE, sin merge, sin corridas con datos reales (preparación sellada no disponible en esta máquina aún).
