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

- **ESTADO VIGENTE — pasada 6 (2026-10-28, misma sesión): selector v4 científicamente defendible; demostración por CONTRASTE de que las páginas vacías de v2/v3 eran causadas por `start_date_min`; SIN MUESTRA — presupuesto de candidatos agotado en objetos no deportivos.** Corrección ordinaria aplicada: `start_date_min` RETIRADO de la consulta (campo filtrado no documentado; retirar un filtro de semántica desconocida es conservador, no optimiza resultados); descubrimiento solo con parámetros documentados (`closed=false&active=true&limit=100&offset`); elegibilidad client-side por `gameStartTime` (intacto); gate OOS honesto = SOLO el gate id pre-interpretación (sin garantía server-side; sin start_date_min la capa estructural desaparece — registrado así en preregistro/manifiesto). BUILD exit 0; TEST verde (gamma 2.334s / clob 0.016s / cmd-engine 35.408s). Preregistro v4 congelado antes de red (binding `3587ff3f…`). Ejecución REAL 18:29:41Z: 1 request (1/2 restantes), HTTP 200, **100 objetos reales inspeccionados (549 KB journalizados; sha `1f43a5a8…`), 0 sellados, 0 elegibles** — todos sin `gameId`/`gameStartTime` (no deportivos; ids 559651+ bajo ordenamiento por defecto de Gamma, no documentado). Presupuesto de candidatos 100/100 agotado ⇒ 2ª request imposible sin violar el tope. `journal verify` capture-v4: NO_INTEGRITY_FAILURES (frontier 2). Observe/record/manifest/replay NOT_RUN con causa (sin assets). OOS jamás consultado; gate no activado pero test-enforced.
- [HISTORIA — pasada 5] Corrección a gameStartTime + descubrimiento v3 con `start_date_min`: página `[]` (mismo sha que v2); su conclusión «bloqueo de datos/universo vacío» EXCEDÍA la evidencia (solo dos consultas bajo ESE filtro) — corregida por el contraste v4. Detalle: doc W1-d (sección SUPERSEDED) y change_log (13).
- [HISTORIA — pasadas 1-4] Ingeniería de la extensión W1-d (transportes, `catalog select`, `clob observe`, tests offline; TEST 3/3 PASS), denegación de pasada 3 (causa real: flag `--preregister`), selección v2 (limit=4, `[]`).

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
