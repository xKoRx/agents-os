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
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Prospective Metadata Quality W1-e 2026-10-28]]"
  - "[[Research — Public Market Capture W1-d 2026-10-28]]"
aliases: []
confidence: high
source_session: "sess W1-e one-shot ZCode×GLM-5.3-Flash (Hefesto, 2026-10-28)"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-10-28-polymarket-w1e-metadata-quality-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- W1-e: integrar el tick/fee prospectivo observado en capture-v6 al camino REAL de calidad del Polymarket Engine, estrictamente offline, sin nueva captura/selección/red, sin raw histórico ni OOS, con causalidad PIT (recepción real, vigencia/TTL explícita, unknown honesto, fail-closed).

## Contexto cargado

- Bootstrap Agents-OS completo (constitución, perfil rjara, nota interna global, índice de skills, registro de routers → DEFAULT sin router, context-retrieval); continuidad Five-POC §§1–18 completa (incluida la nota del lanzador sobre el corte 1310, preservada y atribuida); informe W1-d original; código real del engine (capture/protocol/regimes/books/replay/record/histimport/experiment) leído por rutas canónicas; resúmenes v6 autorizados (12 entradas inmutables, nunca cuerpos crudos al modelo).

## Trabajo realizado

- Implementación mínima modular (17 archivos, sin tocar los 3 protegidos W1-c ni el código W1-d): parser `ParseClobTickSize` + kind protocolar; reducer de regimes interpreta observaciones W1-d (`clob-<op>:<phase>:<key>`) y proyecta revisiones tick con known_at=recepción; política prospectiva pura con TTL congelado 15m, lazos por orden del journal, guard de regresión de reloj y veredictos con provenance; `AssetConstraintAsOf` point-in-time (tick por wall, cuarentenas por seq); `books.ConstraintSource` con `(at, seq)`; replay enruta books por el gate real con store temporal propio (jamás escribe junto al journal) + `regime_digest` nuevo; `histimport.Qualities` y `experiment.shadowConstraints` migrados al mismo contrato.
- Regresiones: 7 paquetes PASS (`protocol/histimport/experiment/books/regimes/replay/cmd-engine`), con oráculos causales (pre-observación unknown, TTL inclusivo→stale, cambio por recepción, cuarentena PIT, wall-regression, fail-closed de body inválido, negativa postcut) y sustitución del antiguo test de lookahead por `TestFutureTickRevisionIsPointInTime`.
- Integración nativa capture-v6: 4 manifests derivados (cut-16/20/91/103) + replay del manifiesto original y de cut-103, schedule 32,7,1 — 8/8 assets OBSERVED_USABLE por el gate real; negativa postcut demostrada (cut-91 ≡ cut-103, digest `b8c5854e…`); comparabilidad original ≡ derivado; regime_digest distingue prefijos.
- Correcciones documentales W1-d in place (2 sobreafirmaciones → límites; unidades/tamaños distinguidos), con marcadores fechados y historia preservada.

## Artifacts creados o modificados

- Checkout: delta W1-e sin commit (SHAs por archivo en el informe W1-e); binario `validated-baseline/w1-e-prospective-metadata-quality-20261028/engine` SHA256 `54ca3b29…`; manifests derivados cut-16/20/91/103 con SHAs.
- Vault: informe W1-e nuevo; correcciones in place en informe W1-d; esta sesión, feedback y agent_run; change_log [[2026-10-27-polymarket-engine-entity-updated]] (16); continuidad §18 bullet W1-e.

## Memoria propuesta o creada

- Ninguna interna: el delta durable quedó en informe W1-e + continuidad; sin hipótesis pendientes que ameriten nota interna adicional.

## Decisiones

- TTL = constante de política congelada (15 m, borde inclusivo), no inferida de datos; PIT de tick por receive-wall con lazo por admisión y cuarentenas por seq exacta; replay con store temporal en vez de proyección por cursor para eliminar lookahead interno sin cambiar la semántica del gate.
- No re-emitir la evidencia G-07 (denegado el env por hook, 1 intento): resultó innecesario, el digest comprometido no driftó porque el fixture G-07 ahora llega a los mismos estados por el gate real.

## Pendiente

- Elección de UNA primera hipótesis falsable (lanzador/Owner, con preregistro); observación futura de un `tick_size_change` real / re-poll fuera de ventana para ejercer los caminos de cambio y stale con datos.
- Estrechar el INTERVAL de fee exige la autoridad documental del mapeo base_fee↔feeRate o trades reales con `fee_rate_bps` en ventana (hoy: 0 observaciones); fee sigue sin certificar (`REAL_FEE_READY=false`).
- Sin push (commit solo local); live sigue cerrado; freeze de producto intacto.

## Continuación misma sesión (tras cortes ECONNRESET 20:57:27Z y project_token_request_failed; reanudada por el lanzador, sin retry automático)

- **Fee/tick real por inspección nativa** (copia derivada autorizada `capture-v6-derived`, `engine.db.pre-w1e` preservado, proyección desde cero): 4 condiciones con tick `0.01`, min-size `5`, mbf/tbf `1000/1000` bps, `fd{r:0.05,e:1,to:true}`, 0 fee observations, sin cuarentenas; 8 assets con tick `0.01` y 0 fee observations. Todas las `known_at` son recepciones reales 19:23:49.63–53.13Z (seqs 4–15); la fase final dedup por contenido idéntico. Resolución honesta: condición = INTERVAL [0,1000] bps (caso 3 del FeeResolverV1, fórmula U-02 no documentada, mbf==tbf no es convergencia), asset = UNRESOLVED (set vacío); 1000 es campo legacy declarado, no comisión certificada.
- **Negativa causal same-wall/seq:** bug detectado por lectura (el filtro asof usaba solo wall; una revisión admitida después con misma wall habría ganado por orden de revisión) — corregido: candidatos cuentan solo con `capture_seq ≤ seq` decisión (desde `capture_ref` durable; seq ilegible = 0 = nunca cuenta, nunca inventado) Y `known_at ≤ at`. Regresiones: `TestSameWallLaterAdmissionCannotWin`, `TestMissingCaptureSeqFailsClosed`, `TestW1DSameWallAdmissionBound`; replay cut-103 post-fix con digest `b8c5854e…` y `regime_digest e66dfb8c…` idénticos al pre-fix.
- **Checkpoint local:** commit `7d519eb712a6a4ec9f369c92d9ee2c735454678b` (29 archivos, +3648/−134, diff --check limpio, 3 W1-c verificados por SHAs exactos del certificado W1-c), árbol final limpio, sin push; binario `eb459241…`; TEST 3/3 PASS (regimes/replay/cmd-engine) + BUILD exit 0 post-gofmt; gofmt normalizó prospect.go (re-add + re-test).
- **Fricción:** `sha256sum` inputs, `mv` wal/shm y `git diff --cached --stat` denegados por el hook (1 intento c/u, documentados); dos cortes de transporte reanudados por el lanzador sin pérdida de trabajo.
