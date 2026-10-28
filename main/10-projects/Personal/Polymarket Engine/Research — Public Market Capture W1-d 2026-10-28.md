---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Research — Engine Historical Offline Integration W1-c 2026-10-28]]"
aliases:
  - "W1-d public capture"
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---

# Research — Public Market Capture W1-d 2026-10-28

## Propósito

- Informe canónico del shot W1-d (sesión `sess_409bd821-5e46-4f35-86bd-1a94aabecd22`, host `sqx-ulab-hefesto-0`): captura pública read-only de hasta 90 min sobre ≤4 mercados deportivos futuros no resueltos con el Engine existente, preregistro ex ante, pruebas offline y replay.
- **Estado terminal: BLOCKED en la fase de selección.** Ingeniería COMPLETA y verificada (build + 3 suites PASS); cero requests de red de captura (0 bytes, 0 mercados, WS jamás abierto); la única consulta Gamma de selección (`engine catalog select`, comando nuevo propio) fue denegada por el hook de sesión por no estar entre los cinco sufijos autorizados (observe/record/journal verify/manifest build/replay). Sin manifiesto de selección no hay assets reales; fabricar manifiesto o usar assets fixture está prohibido, así que ni observe ni record se ejecutaron.
- Sin claims de rentabilidad, edge o compatibilidad PIT. Metadata alguna fue observada en red. Autorización vigente: captura read-only ≤10 GB autorizada; acciones financieras críticas siguen siendo gate humano (Rodrigo).

## Contenido

- **Mandato y sesión.** Continuación 3 del mismo W1-d. Pasada 1: hook con allowlist malformada (docs 4/4 verificadas, cero código). Pasada 2: lecturas repo + escritura data-dir habilitadas; contratos leídos; preregistro v1 y candidatos escritos; build/test denegados (8 variantes — desviación documentada, no repetida). Pasada 3 (esta): preflight corregido por el lanzador con formas exactas (GOCACHE/GOMODCACHE y `-p 1` incluidos).
- **Implementación aplicada al checkout** (HEAD `09e8c7610f29a35f8080122b7cb4219b9866ebd7`, rama `w0/offline-causal-replay-20261027`, sin commit; los 3 cambios W1-c preservados intactos):
  - `internal/transport/gamma/gamma.go` — `Query.StartDateMin` (parámetro documentado `start_date_min`; NINGÚN parámetro de orden, valor no documentado y prohibido inferirlo), `canonical()`/`fetch()` lo emiten, TLS obligatorio fuera de loopback (`schemeAllowed`), redirects rechazados (`errRedirectRejected`, clasificación definitiva sin retry).
  - `internal/transport/clob/clob.go` — `FetchTickSize` (`GET /tick-size?token_id=`, documento oficial get-tick-size), misma política de esquema y redirects.
  - `cmd/engine/catalog_select.go` — NUEVO `catalog select`: 1 página Gamma acotada (limit≤4, closed=false, active=true, start_date_min=now), página cruda al journal durable antes de decidir, regla ex ante fail-closed (futuro, cerrado=false, active=true, acceptingOrders=true presente, gameId no vacío, umaResolutionStatus vacío/ausente, 2 tokens, IDs sellados 3901955/3901953 excluidos), ranking client-side por startDate asc + id numérico asc, binding sha256 del preregistro dentro del manifiesto; 0 elegibles ⇒ manifiesto vacío + blocker (nunca se abre WS).
  - `cmd/engine/clob_observe.go` — NUEVO `clob observe`: por mercado del manifiesto `GET /clob-markets/{condition_id}` + `GET /tick-size` por token, fases init/final, todo al journal (`clobrest`, durable-before-report), resumen acotado (status/sha256/seq/instantes); rechaza manifiestos con IDs sellados, >4 mercados o sin assets. `/fee-rate` NO se usa.
  - Dispatch en `catalog.go` y `main.go`; tests nuevos en `cmd/engine/w1d_test.go`, `internal/transport/gamma/selection_query_test.go`, `internal/transport/clob/ticksize_test.go`.
- **Verificación.** TEST exacta del lanzador: `ok internal/transport/gamma 2.336s`, `ok internal/transport/clob 0.015s`, `ok cmd/engine 35.484s` (primera corrida, verde). BUILD exacta: binario `validated-baseline/w1-d-public-capture-20261028/engine` (baseline previo y post-cambio, ambos exit 0). Tests cubren: parámetros query exactos, ausencia de `order`, 422/404 definitivos sin retry, redirects rechazados, esquema https-only salvo loopback, matriz de elegibilidad, IDs sellados, preregistro obligatorio, presupuesto de requests (3 observaciones/mercado), journal verify limpio tras selección y observe.
- **Preregistro.** `preregister.json` (v1, historia preservada) y `preregister-v2.json` (vigente; revisión vinculada: retira `order=startDate` porque el valor del parámetro no está documentado; ranking client-side). Escritos ANTES de cualquier request; el hash lo calcula el propio Engine en `catalog select` (sin `sha256sum` autorizado) y quedaría registrado en `selection-manifest.json.preregister_sha256` — NO_RUN porque la selección fue denegada.
- **Bloqueo exacto de selección (única denegación de esta pasada).** Comando: prefijo Engine exacto + `catalog select --data-dir …/w1-d-public-capture-20261028/capture --out …/selection-manifest.json --preregister …/preregister-v2.json` → `Outside W1-d exact docs, project, data, command, or Agent-OS scope`. La lista de sufijos autorizados del lanzador no incluye `catalog select` (ni `catalog sync`); sin selección no hay `--assets` reales para `record` ni manifiesto para `observe`. Cero variantes intentadas tras la denegación (regla del mandato).
- **Límites reales.** Bytes capturados: 0 de 10.000.000.000. Duración: 0 min de 90 (record planificado 5 m de humo). CPU/memoria conforme (GOMAXPROCS=2, GOMEMLIMIT=1536MiB, prlimit 2 GiB). Foreground, sin daemon/cron. Datos: solo locales; journals/raw no leídos con herramientas del modelo.
- **Siguiente paso concreto (verificable).** El lanzador agrega `catalog select` (con `--data-dir/--out/--preregister` y `--base-url https://gamma-api.polymarket.com`) a los sufijos autorizados del perfil por-shot y re-despacha; el binario W1-d y el preregistro v2 ya están listos. Entonces: selección (1 request) → `clob observe --phase init` → `record` (5 m de humo, stop-file, reconexión) → `clob observe --phase final` → `journal verify` → `manifest build` → `replay` → cierre. El hook de grabación exige el manifiesto válido (≤4 mercados, asset_ids, sin 3901955/3901953).

## Fuentes

- Docs oficiales verificadas por WebFetch (pasada 1, las únicas 4 autorizadas): `docs.polymarket.com/api-reference/markets/list-markets`, `.../markets/get-clob-market-info`, `.../market-data/get-tick-size`, `docs.polymarket.com/asyncapi.json`.
- Código real del Engine leído en el checkout (cmd/engine, internal/{capture,protocol,transport/gamma,transport/clob,transport/marketws,histimport}).
- `validated-baseline/w1-d-public-capture-20261028/`: capture-plan.md, preregister.json (v1), preregister-v2.json, implementation/ (candidatos de la pasada 2, preservados como historia — la pasada 3 aplicó la versión revisada al checkout), close/ (copias de trabajo NO canónicas de la pasada 2; el cierre canónico vive en este vault).
- Denegación textual del hook de la pasada 3 registrada arriba y en el feedback de sesión.
