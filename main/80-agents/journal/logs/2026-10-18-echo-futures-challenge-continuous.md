---
type: journal
schema_version: 1
created: "2026-10-18"
entities:
  - "[[Echo Futures]]"
tags:
  - kind/journal
---

# 2026-10-18 (v2) — Echo Futures: CHALLENGE CONTINUOUS — FIRST_PASS revocado y lote re-ejecutado

- Mandato ONE-SHOT v2.0 del Owner: revocatoria del corte FIRST_PASS (decisión del Manager CLOUD, no del Owner); campaña CHALLENGE_ONLY CONTINUA con el lote completo re-ejecutado bajo una sola versión final sellada.
- Rama de producto `experiment/challenge-first-20261018` @ `2b467ad5` (pulsado y verificado en remoto `ce09ba4f..2b467ad5`; sin merge a master). Delta de continuidad del motor: `02980b82`; RED capturado @ `cf5909c6`; tooling oráculo/analizador: `52c3cbd5`, `d111e6b0`; resultados: `2b467ad5`.
- Identidad nueva `challenge_policy=CONTINUOUS_V1` obligatoria en preset→spec→plan→request (rechazos nombrados; FIRST_PASS ya no es valor aceptado; artefactos históricos intactos con etiqueta `SUPERSEDED_FOR_CONTINUOUS_OBJECTIVE`).
- Reparaciones §2.1 RED→GREEN: USD de ciclo con point_value del instrumento (la versión anterior restaba 4.98 a puntos×contratos), ciclos por Operation+cuenta, defecto de signo en SHORT (cazado por igualdad FIFO↔Operación), oráculo con veredicto estructurado + exit codes (negativo sembrado → exit 2), FIFO preserva base en cierres parciales.
- Lote CONTINUO: 49/49 campañas `CONTINUOUS_HORIZON_COMPLETE` reconciled, oráculo 49 OK / 0 FAIL. 114 compras, 7 pases (6,1% observado; W0 6/80, W1 1/34), 57 perdidas por presupuesto, 0 FAILED_RULE, 50 pendientes al corte, gasto 14.880 USD, costo/pase 2.125,71 USD. Séptimo pase invisible para FIRST_PASS: segundo pase de TG-F0/W0 el 14-nov.
- Run root físico nuevo: `/srv/echo-work/runs/challenge-first-continuous-20261018/` (binario sellado sha256 `2ae5807a…`; el lote FIRST_PASS no se tocó).
- Regresión completa del paquete backtester: 6 fallos TODOS pre-existentes contrastados en `ce09ba4f` (5×BTG-S05 + matrix-preset).
- Delta en [[TRADESGERARD-CONTROL]] (corte 2026-10-18 v2). Entregables: `RESULTS-CONTINUOUS.md`, `executive-table.md`, `executive-rows.csv`, `pass-sequence.csv`, `accounts-detail.csv`, `oracle-receipts.json`, `rankings.py`, `oracle/test_cycle_usd.py`.
- Sin LIVE, sin merge a master, sin matriz funded, sin aceptación del Owner. Cierre de ESTA sesión local autorizado por el mandato.
