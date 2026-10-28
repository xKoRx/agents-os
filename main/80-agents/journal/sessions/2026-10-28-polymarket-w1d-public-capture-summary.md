---
type: session
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
related:
  - "[[Research — Public Market Capture W1-d 2026-10-28]]"
aliases: []
confidence: high
source_session: sess_409bd821-5e46-4f35-86bd-1a94aabecd22
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-28-polymarket-w1d-public-capture-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- W1-d (misma sesión `sess_409bd821-…`, continuación 3): captura pública read-only ≤90 min de ≤4 mercados deportivos futuros no resueltos con preregistro ex ante, tests offline y replay sobre polymarket-engine. Sin estrategia/PnL/órdenes; IDs sellados 3901955/3901953 fuera.

## Contexto cargado

- Bootstrap de la pasada 1 reutilizado (sin re-bootstrap retroactivo): constitución, memoria interna global, skills INDEX, templates de session/feedback/agent-run, crew INDEX.
- Delta de esta pasada: formas exactas BUILD/TEST/prefijo Engine corregidas por el lanzador (GOCACHE/GOMODCACHE + `-p 1`); contratos del Engine ya leídos en pasada 2; candidatos de `implementation/` preservados como historia.

## Trabajo realizado

- **ESTADO VIGENTE — pasadas 7-8 (2026-10-28, misma sesión): MUESTRA PÚBLICA CAPTURADA — cadena completa exit 0.** Pasada 7 (cortada por cuota del proveedor 1310 a las 18:51:35Z, exit 1 — no guard; cierre incompleto): lote moneyline con parser RFC3339-estricto → 100 candidatos reales de la familia, 0 elegibles por formato (`kickoff unparsable`); diagnóstico auxiliar del LANZADOR sobre bytes locales (exclusión ID-only previa, sin cambio de bytes): 22/100 con formato `YYYY-MM-DD HH:MM:SS+00` (todos pasados, ene–ago 2026), 78 sin string utilizable. Pasada 8 (Rodrigo ordenó seguir GLM; único intento): (1) `parseKickoffInstant` — RFC3339/Nano + layout wire observado (`2006-01-02 15:04:05-07`), UTC exacta, fail-closed sin zona; regresión de equivalencia/inválidos/pasado/futuro-sintético; (2) ordenamiento fundado `order=gameStartTime&ascending=false` (parámetros documentados en list-markets sobre campo documentado; la guía discover-markets documenta CERO ordenamiento — priorización de presupuesto, no inferencia de kickoff); (3) preregistro v6 congelado (binding `5069f924…`); (4) **lote v6 REAL 19:23:10Z: 1 request, 100 inspeccionados, 100 ELEGIBLES, 0 sellados, 4 seleccionados** (kickoffs 2026-11-18T00:00/00:30Z; ids 6013297/6013337/6013387/6013310; sha de página `d8f59551…`); (5) **cadena de captura completa**: `clob observe init` 12/12 HTTP 200 → `record` 5 m (epoch 1 sin gaps, 103 frames/74 admitidos/0 rechazados, 8 libros de 20-22 niveles, durable_seq 90) → `clob observe final` 12/12 → `journal verify` NO_INTEGRITY_FAILURES (103 registros, 4 segmentos, frontier 103, cursores consistentes) → `manifest build` `85618e1a…` → **replay ×2 con digest idéntico `b8c5854e…`** (8 assets OBSERVED_USABLE en books; delivery 0 frames — sin RUNTIME records, honesto). TEST verde (gamma 2.330s / cmd-engine 30.750s) tras una iteración ordinaria (duplicación canonical+Add; aserciones viejas). Lecturas honestas: libros SYNCING en el camino de calidad (tick PIT ausente — OBSERVED_USABLE es de books, no el gate de calidad); fees/tick observados no certificados; 5 min sin claims de edge/PnL; la aceptación server-side de `order=gameStartTime` es observación de un instante, no contrato.
- [HISTORIA — pasada 6] Descubrimiento genérico sin `start_date_min` (100 no-deportivos; contraste que demostró el efecto del filtro) — no era descubrimiento dirigido.
- [HISTORIA — pasada 5] gameStartTime como kickoff + retiro de `order=startDate`; `[]` bajo `start_date_min` (conclusión «universo vacío» excedía evidencia, corregida en pasada 6).
- [HISTORIA — pasadas 1-4] Ingeniería de la extensión W1-d; denegación de pasada 3 (causa real: flag `--preregister`); selección v2 limit=4 `[]`.

## Artifacts creados o modificados

- **Pasada 6:** checkout — `catalog_select.go` v4 (retiro de `start_date_min`; regla/ids v4; OOSGate honesto sin capa estructural), test de regresión de queryparams (start_date_min NO debe enviarse); binario reconstruido. Data-dir — `preregister-v4.json`, `capture-v4/` (journal: 2 registros, 549 KB de página real, frontier 2), `selection-manifest-v4.json` (binding `3587ff3f…`; 1 request; 100 inspeccionados; 0 sellados; 0 elegibles). v1/v2/v3 preservados intactos.
- **Pasadas 3-5:** checkout — `catalog_select.go`, `clob_observe.go`, gamma/clob (StartDateMin/DisableRetry/TLS/redirects, FetchTickSize), dispatch, 3 archivos de tests; preregistros v1-v3; capture/, capture-v3/ y manifiestos v2/v3.
- Vault: doc W1-d, esta summary, feedback, agent_run, change_log (secciones (11)-(14)), §18 de la continuidad.

## Memoria propuesta o creada

- Ninguna L3 nueva (el patrón preflight-vs-encargo ya está registrado como feedback; la promoción sigue defer hasta tercera observación).

## Decisiones

- **Pasada 6:** retirar `start_date_min` (semántica desconocida) es corrección metodológica, no optimización; el gate OOS queda honestamente reducido al gate id-only real (registrado así, sin garantías server-side inventadas); con presupuesto de candidatos agotado NO se usa la 2ª request (inspeccionar más violaría el tope).
- **Pasadas 4-5:** con `[]`/vacío bajo el filtro, regla sin desviación: sin ampliar universo, sin WS.
- **Pasada 3:** no fabricar manifiesto ni usar assets fixture; no reintentar variantes tras denegaciones únicas.

## Pendiente

- Decisión lanzador/Owner: preregistro v5 para apuntar a deportivos — `sports_market_types`/`game_id`/`tag_id` están documentados como parámetros pero sus VALORES/semántica no: primero verificación documental enfocada; luego regla + presupuesto nuevos (p. ej. renunciar a inspección masiva y apuntar por filtro) y re-despacho con el mismo comando validado.
- Con selección real: observe init → record 5m humo (tope 90m) → observe final → verify → manifest build → replay → cierre canónico del resultado.
