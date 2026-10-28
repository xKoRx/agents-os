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

- **Pasada 4 (misma sesión, retry único autorizado): selección ejecutada REAL — cero candidatos elegibles.** Causa real de la denegación de la pasada 3 corregida con fecha: era el argumento `--preregister` (no incluido en el perfil del hook), NO el sufijo — `catalog select` siempre estuvo permitido. El comando exacto validado por el hook corrió: página Gamma acotada HTTP 200 = `[]` (3 bytes) a las 17:47:02Z, `page_sha256 37517e5f…`, preregistro v2 vinculado (`9611b9b1…`), `selected_markets=[]` + blocker medido. `journal verify`: NO_INTEGRITY_FAILURES (2 registros, frontier 2, página durable). Regla aplicada sin desviación: 0 elegibles ⇒ sin ampliar universo, sin WS; observe/record/manifest/replay NOT_RUN con causa (sin assets reales que observar). OOS intacto; sin órdenes; sin claims (una página vacía no observa nada).
- Aplicada al checkout la extensión mínima W1-d: `start_date_min` en gamma (sin `order`, no documentado), `FetchTickSize` en clob, TLS-forzado-salvo-loopback y redirects rechazados en ambos transportes, `catalog select` y `clob observe` nuevos, dispatch, y 3 archivos de tests offline (httptest loopback, sin red real).
- TEST exacta del lanzador: 3/3 paquetes PASS (gamma 2.336s, clob 0.015s, cmd/engine 35.484s), primera corrida. BUILD exacta: binario W1-d construido (exit 0).
- Preregistro v2 escrito antes de red (revisión vinculada de la v1: retira `order=startDate` no documentado; historia preservada).
- Intento de selección en pasada 3 con prefijo Engine exacto: DENEGADO por el hook — causa real precisada después: flag `--preregister` fuera del perfil (corrección registrada en doc/feedback/agent_run/change_log; historia de la denegación preservada). Cero variantes en su momento.
- Cierre canónico en vault con el materializador (4 notas creadas + este log + §18).

## Artifacts creados o modificados

- **Pasada 4:** `capture/` (journal real: 2 registros, frontier 2 — boot + página `[]`), `selection-manifest.json` (binding preregistro `9611b9b1…`, page sha `37517e5f…`, blocker). Sin cambios de código ni binario.
- Checkout (sin commit, HEAD intacto, 3 archivos W1-c intactos): 2 transportes editados, 2 comandos nuevos, 2 dispatches, 3 archivos de tests.
- `validated-baseline/w1-d-public-capture-20261028/`: preregister-v2.json (nuevo), engine (binario), implementation/ y close/ preservados como historia de las pasadas 1-2.
- Vault: doc W1-d, esta summary, feedback, agent_run, change_log (secciones (11) y (12)), §18 de la continuidad.

## Memoria propuesta o creada

- Ninguna L3 nueva (el patrón preflight-vs-encargo ya está registrado como feedback; la promoción sigue defer hasta tercera observación).

## Decisiones

- **Pasada 4:** con `[]` en la página acotada, aplicar la regla sin desviación: cero elegibles ⇒ sin muestra, sin ampliar universo, sin WS; bloqueo medido y entregado con el colector probado (mandato explícito).
- **Pasada 3:** no usar `policy-a/policy-b` ni fabricar manifiesto: la captura se detiene en selección (BLOCKED medido) antes que inventar identidad de mercados.
- No reintentar variantes tras la denegación única de la pasada 3 (regla explícita del mandato).

## Pendiente

- Decisión lanzador/Owner sobre la regla ex ante: re-verificar la semántica documentada de `start_date_min` (la página vino vacía con 200, no 422) y, si procede, re-preregistro v3 ANTES de cualquier nuevo request; el colector, binario y preregistro v2 quedan como evidencia probada.
- Con selección real: observe init → record 5m humo (tope 90m) → observe final → verify → manifest build → replay → cierre canónico del resultado.
