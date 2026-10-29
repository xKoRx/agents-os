---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v2 W1-h 2026-10-29]]"
  - "[[Research — Economic Pilot Corrections W1-h 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-h preregistration v2 PE-005-R1"
  - "PE-005-R1-E1 v2"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29

## Propósito

- Preregistro **v2 correctivo** de `PE-005-R1-E1` ("pre-match spread reversion", engine `poc-sports` v1 @ `853c0e4`). Reemplaza en alcance a la v1 ([[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]], preservada como historia) resolviendo las siete correcciones W1-h **antes** de adquirir cualquier dato nuevo. Congelado el 2026-10-29: cero datos nuevos, cero requests de mercado, checkout intacto @ `853c0e46c9be2de4e84201e240e9cf8366b1036e`, árbol limpio salvo el fixture untracked de este shot.
- Este documento **no ejecuta nada** y no promete beneficio. El piloto que materializa (UN episodio) es **descriptivo**: no valida ni falsifica rentabilidad. La ejecución requiere adjudicación previa de Metis sobre (i) esta especificación, (ii) el plan v2 y (iii) la decisión de delta productor de §4.
- Parámetros numéricos de la hipótesis: **idénticos al set congelado 2026-09-21** (`window_ms=300000, ref_frames=10, widen_min_bps=50, entry_budget=25, min_net_edge_bps=50, taker=true`). Ninguna constante se elige mirando datos; las constantes nuevas del piloto se derivan de constantes ya congeladas (§5, §6).

## Contenido

### 1. Diff conceptual v1 → v2 (razones a priori, sin ajuste a resultados)

| # | Corrección W1-h | Qué afirmaba la v1 | Qué fija la v2 | Razón a priori |
|---|---|---|---|---|
| 1 | Frescura + writer | Re-polls cada ≤15–30 min "para que el gate no degrade a stale"; `clob observe` re-invocado **durante** el `record` de 90 min | El re-poll con contenido idéntico **no renueva** frescura (dedup por contenido); TTL anclado a la primera recepción del contenido vigente; invocaciones **estrictamente seriales** (sin solaparse) | Semántica del código @ `853c0e4` demostrada por fixture offline `TestW1HMetadataFreshnessRecipe` / `TestW1HConcurrentWritersUnsupported` (§4). No es ajustable por frecuencia: es física del reducer |
| 2 | Resultado económico | Endpoint primario = toque de B\* en 300 s (diagnóstico tratado como salida) | Endpoint primario = **round trip virtual a horizonte fijo H=300 s** con entrada sobre profundidad, liquidación full-size a bids y costes de ambas patas; el toque de B\* queda **sólo diagnóstico** | "Toque ≠ fill" es regla congelada del paquete economics; la contabilidad requiere liquidez de salida para TODO el tamaño (§5) |
| 3 | Fee | `fee_high=500` presentado como bound dominante del escenario | 500 bps = **sensibilidad CONDICIONAL** del escenario A (fórmula documentada, deportes 0,05); 1000 bps = **estrés separado** del cap legacy; `REAL_FEE_READY=false` intacto | La incertidumbre real es el INTERVAL [0,1000] sin mapeo verificado; elegir 500 como "vigente" inventaría certeza inexistente (§6) |
| 4 | Estadística | n=90 señales / ≥30 episodios con IC de Wilson e inflación ×1,3 | Piloto = UN episodio, **descriptivo por partido** (1 cluster); fase inferencial POSTERIOR prospectiva con unidad/estimador/dependencia/reglas fijadas (§7) | Las señales intra-partido están correlacionadas; Wilson i.i.d. y el factor 1,3 no son IC por cluster; el piloto no tiene potencia para nada y no la anuncia |
| 5 | Presupuesto | "0,9 MB/min"; "campaña ~25 ventanas bajo el techo 10 GB" | 447.016 B/5 min = **0,0894 MB/min decimal**; 25 ventanas de estrés = 40 GB ⇒ **no cabe**: campaña NO programada; piloto 1 episodio con proyección total ≤3,1 GB ≪ stop-line 8 GB (§8) | Aritmética corregida con unidades; separación medido/hipotético; prohibido borrar datos para caber |
| 6 | Selección | v6 (kickoffs 2026-11-18) asumida sirviendo "hoy" | Reglas de descubrimiento para kickoffs próximos con presupuesto acotado y desenlace honesto `NO_ELIGIBLES_EN_LOTE` si no los hay (§3) | El descubrimiento es sólo diseño; sin consultar mercados en este shot; jamás inferir kickoff de `startDate`/`endDate` |
| 7 | Supervisión | "sin background" junto a record bloqueante de 90 min + re-polls | Receta serial de pasos foreground con outcome durable por paso, checkpoint duro 02:00 GMT-3 y pausa completa 02–08 sin gracia; sin daemon/cron (§9) | El escritor único obliga a serializar; la supervisión es una secuencia de comandos con recibos, no un proceso residente |

### 2. Identidad, universo y unidad

- **ID:** `PE-005-R1-E1` (revisión v2 del mismo enunciado falsable v1; la traza padre PE-005 → PE-005-R1 no cambia). El enunciado v1 se mantiene: ensanchamiento del spread vs mediana propia seguido de recuperación dentro de `window_ms`; la **medición** del éxito cambia a §5.
- **Unidad de decisión:** un outcome asset de un mercado moneyline con `gameStartTime` explícito. **Unidad estadística:** el **partido (episodio) = 1 cluster**; todos los mercados/outcomes del mismo partido (mismo `gameStartTime`) pertenecen a UN cluster.
- **Exclusiones duras (idénticas a v1):** OOS históricos `3901955`/`3901953` jamás consultados (gate id-only pre-interpretación); no-moneyline/combos; ventana que intersecte la pausa 02:00–08:00 GMT-3 (censurada ex ante); kickoff no disponible como hecho capturado (jamás `startDate`/`endDate`/`createdAt`).
- **Ventana por episodio:** `[K−90 min, K)` en recepción; post-kickoff el strategy bloquea.

### 3. Selección por reglas (corrección 6) — sólo diseño

- **Descubrimiento (design-only, presupuestado):** `GET /markets` con parámetros documentados `closed=false&active=true&sports_market_types=moneyline&limit=100&offset=0&order=gameStartTime&ascending=false`, tope **3 requests / 100 candidatos por lote**, reintentos desactivados. La aceptación server-side de `order` se observó UNA vez (W1-d pasada 8): se trata como **priorización**, no contrato; el orden real de la página se re-verifica client-side (monotonía de kickoffs; si falla, se ordena client-side la página adquirida — jamás segunda página para "arreglar" orden).
- **Filtros client-side ex ante** (aplicados antes de leer precios/cualquier contenido económico): `gameStartTime` parseable por el parser del selector (RFC3339 + wire), kickoff en `[now+30 min, now+26 h]`, ventana `[K−90m,K)` sin intersección con la pausa, `conditionId` y exactamente 2 `clobTokenIds`, gate OOS id-only **antes** de cualquier otra lectura.
- **Grupo seleccionado:** preferencia por UN partido (los ≤4 mercados del mismo `gameStartTime`); si el partido tiene un solo moneyline, se capturan sus 2 assets. Máximo 4 mercados/8 assets.
- **Desenlace honesto:** 0 elegibles en el lote acotado ⇒ resultado `NO_ELIGIBLES_EN_LOTE` registrado (con página journalizada y contadores); **prohibido** ampliar familia, paginar sin fin, relajar filtros o re-consultar en el mismo despacho. La decisión de re-despacho es de Metis/lanzador.
- Los costes de `clob observe` (re-polls) y del WS **no** cuentan contra el presupuesto de descubrimiento; se reportan por separado (§8).

### 4. Frescura de metadata y escritura del journal (corrección 1)

Hechos demostrados por el fixture offline de este shot (`internal/experiment/w1h_acquisition_recipe_test.go`, suite `^TestW1H` **PASS** exit 0, SHA `f7c03a4829cae2d31e77bd68be80f1f2c389a18143182dce44d24152f3c0fa17`):

- **F1 (re-poll idéntico no renueva):** el reducer dedup revisions por `content_hash` (`internal/regimes/reducer.go`, `upsertRegimeRevision`: duplicado ⇒ sólo mueve `last_observed_at`); el `known_at` del hecho de tick vigente queda en la **primera** recepción de ese contenido. Consecuencia: con tick estático, la elegibilidad de un asset vive en `[primera recepción del contenido, +15 min]` y **ninguna frecuencia de re-polls la extiende**; los frames fuera de esa ventana quedan `SYNCING`/inelegibles y se cuentan (`frames_ineligible`), jamás excluidos favorablemente. Primeros 15 min: antes de la primera observación ⇒ `no_observation_yet` (SYNCING); el borde inclusive a +TTL y stale a +1 ns quedaron fijados por fixture.
- **F2 (cambio de contenido re-ancla):** un lexema nuevo crea revisión nueva y re-ancla el TTL en su propia recepción (fixture).
- **F3 (first_seen ≠ observación):** `known_at` (primera vista) y `last_observed_at`/recepción del re-poll son hechos distintos y separados; el veredicto conserva el `known_at` de primera vista (fixture).
- **F4 (epoch/reconexión):** la reconexión WS es epoch nuevo con gap declarado; **no** renueva frescura de tick (sólo observaciones REST con contenido nuevo o `tick_size_change` del WS lo hacen); la calidad de libro por shard reinicia hasta el primer book del epoch.
- **F5 (writer único):** `capture.Open` no tiene exclusión entre procesos; un segundo writer vivo adopta el boot activo, ambos asignan los mismos `seq`, y al reabrir el journal **se lee limpio mientras un registro ACKed-duradero queda silenciado sin discontinuidad declarada** (fixture `TestW1HConcurrentWritersUnsupported`). Por lo tanto **ninguna receta puede prometer escritura concurrente**: `record` y `clob observe` se ejecutan estrictamente en secuencia sobre un mismo data-dir.

**Receta ejecutable HOY (opción A, sin código nuevo):** episodio en 6 tramos seriales de 15 min (`record --duration 15m` → `clob observe --phase final` entre tramos; §Plan). El tamaño 15 min es la constante `ProspectiveTickTTL` ya congelada, no un parámetro ajustado. **Expectativa preregistrada E1:** con metadata estática, la fracción elegible de frames será ≈15/90 salvo cambios reales de contenido; el piloto MIDE ese perfil (es desenlace, no fracaso). Los re-polls intermedios siguen valiendo para capturar cambios de contenido si ocurren y para la cadena de custodia.

**Delta productor propuesto (opción B, decisión de Metis ANTES de capturar; NO implementado):** extensión mínima para **renovación de recepción**: en el branch de duplicado de `upsertRegimeRevision` (`internal/regimes/reducer.go`) registrar por entidad+contenido un hecho de renovación `(observed_at, capture_seq)`; que la evaluación del TTL (`internal/regimes/prospect.go` / service) ancle la vigencia en la última renovación admitida `capture_seq ≤ seq` de la decisión, manteniendo `known_at`/first_seen intactos y sin inferir estabilidad entre polls (la igualdad de hashes **no** es evidencia de continuidad; la renovación declara "lo observé de nuevo ahora"). Aceptación: re-poll idéntico en t extiende elegibilidad a `t+TTL`; first_seen invariante; sondas W1-e (pre-observación, seq=0, same-wall, wall-regression, cuarentena PIT) invariantes; `regime_digest` cambia (declarado). Si Metis no adjudica B, la opción A es la receta vinculante con su coste de elegibilidad preregistrado.

### 5. Resultado económico observable a horizonte fijo (corrección 2)

- **Endpoint primario del piloto:** para cada señal ACCEPT (gate económico v0.1 intacto: `net_bps ≥ 50` con fees al bound del escenario en ambos tramos), el resultado del **round trip virtual**:
  1. **Entrada:** en el primer frame `OBSERVED_USABLE` con wall **≥ señal + 1 frame** (latencia conservadora de un frame, el supuesto mínimo que no asume fill mismo-frame); BUY taker del tamaño `floor2(min(entry_budget/bestAsk, profundidadAsk))`; sin profundidad observable ⇒ `sufficiency_deficit`.
  2. **Salida a H = señal + 300 s** (el `window_ms` congelado; sin grado de libertad nuevo): SELL del **tamaño íntegro** retenido a los bids del último frame con wall ≤ H; ejecutable sólo si los bids cubren **todo** el tamaño (`WalkSide`, `remaining=0`); falta de profundidad/dato ⇒ `exit_non_executable` (estado **desconocido**, permanece en el denominador, jamás se cuenta como salida ni se excluye).
  3. **Contabilidad:** `net = proceeds − notionalEntrada − feeEntrada − feeSalida` con fees al bound del escenario (§6); **pérdidas con signo**; `net < 0` ⇒ `loss_at_horizon`; `net ≥ 0` ⇒ `entry_fill_exit_executed`.
- **Estados taxonómicos exhaustivos (7):** `no_signal`, `signal_no_fill`, `entry_fill_exit_executed`, `entry_fill_exit_non_executable`, `invalid_gap`, `loss_at_horizon`, `sufficiency_deficit`. Clasificación por señal; agregación **por partido** (descriptiva). La aritmética quedó demostrada sobre el paquete economics real (`TestW1HEconomicsVirtualExitAtHorizon`: barrido de entrada, FeeHigh exactos, pérdida −5.055 conservada, stress 1000 bps volviendo pérdida la misma recuperación, salida insuficiente clasificada).
- **Toque de B\* (strategy `reverted`):** métrica **diagnóstica** que se reporta junto al endpoint; jamás sustituye la salida ejecutada (toque ≠ fill).
- **Gaps y pausa:** señal cuya ventana `[señal, H]` cruza un gap declarado (reconexión, corte de tramo, pausa) ⇒ `invalid_gap`; evaluación dentro de gap prohibida; continuidad jamás inventada. Ventana que intersecta la pausa 02:00–08:00 GMT-3 ⇒ episodio censurado ex ante.
- **Sin datos futuros:** señal, elegibilidad y referencia usan sólo frames recibidos ≤ instante de decisión; la liquidación usa frames ≤ H; la elegibilidad del episodio se decide con metadata de selección (kickoff) previa a la ventana.
- **Exposición virtual:** presupuesto total USD 500 futuro (estado TESTING, sin cuenta ni fondos), entrada ≤ USD 25, exposición abierta simultánea ≤ USD 100, sin reentrada sobre señal abierta del mismo asset; cero órdenes reales.

### 6. Fee (corrección 3)

- **Escenario A (sensibilidad CONDICIONAL):** `fee_low=0 / fee_high=500` bps — bound que domina la fórmula documentada `fee = C·rate·p·(1−p)` con rate 0,05 deportes (docs 2026-10-29, vigencia desconocida para nuestros mercados). No se certifica tarifa alguna y **no** se afirma que 500 bps sea el intervalo vigente.
- **Escenario S (estrés separado):** 1000 bps (bound del cap legacy `mbf/tbf`, supuesto U-02). Ambos escenarios se reportan; la correspondencia oficial por mercado exige evidencia ya existente pertinente (nueva lectura documental permitida; **ningún** request a mercados ni `fee-rate`/trades nuevos).
- **Gate:** `REAL_FEE_READY=false` inalterado; sin certificación por trades sin semántica; sin fee 0 ni POINT inventado; si los escenarios no sostienen un claim, el gate es explícito (bloqueo), no una cifra de conveniencia. Límites as-of/históricos y fuente/versión de docs/código se citan en cada uso.

### 7. Estadística: piloto descriptivo y fase inferencial posterior (corrección 4)

- **Piloto (UN episodio):** sólo descriptivo **por partido**; ambos outcomes y mercados del mismo partido = **1 cluster**; tabla de los 7 estados + fracción elegible (E1) + frames/bytes medidos. **El piloto no valida ni falsifica rentabilidad** y no se presentará como tal.
- **Prohibido en el piloto:** IC de Wilson sobre señales correlacionadas, factor de inflación ×1,3 como corrección de cluster, mezclar la parada de 90 señales con horizontes de 60 episodios, potencia anunciada sin base.
- **Fase inferencial POSTERIOR (prospectiva, sellada hasta su apertura):** se activa sólo si Metis adjudica campaña. Diseño fijado ahora, sin datos: unidad = episodio-partido; estimando = fracción de señales ACCEPT con `entry_fill_exit_executed` a nivel cluster, con intervalo por cluster (bootstrap de clusters pre-registrado en su apertura) y sensibilidad por supuestos de ICC declarados no garantizados; enrollment = kickoffs elegibles en orden ascendente bajo esta spec; split = primeros 60 episodios exploratorios, resto OOS-nuevo sellado (regla v1 intacta, sin IDs inventados); regla de rechazo = la que se congele en la apertura con su umbral explícito; tamaño de muestra = decisión por **precisión/presupuesto** con supuestos declarados (o diseño fijo defendible), jamás "80 % potencia" sin fundamento. Criterios de suficiencia/insuficiencia/`NOT_RUN`/no-admisión/abandono: la taxonomía de §5 clasifica **todos** los casos (incluidos `sufficiency_deficit` y `invalid_gap`), y el cierre sin claim es desenlace válido.

### 8. Presupuesto y aritmética (corrección 5)

- **Ancla medida:** 447.016 B de payload WS / 5 min / 8 assets = **89.403,2 B/min = 0,0894 MB/min decimal** (la cifra v1 "0,9" era un error de unidad ×10, retirado). Estrés cerca de kickoff 3–20×: hipótesis conservadora **no medida**.
- **Piloto UN episodio (≤90 min, ≤4 mercados/8 assets):** peor caso 20× ⇒ 160.925.760 B ≈ **0,16 GB** de captura nueva; proyección total workspace = 2.931.394.683 B (preflight del lanzador, metadata de filesystem, no ciencia) + captura + ledger/manifests (≈ MB) ≈ **≤3,1 GB** ≪ stop-line **8.000.000.000 B** < techo **10.000.000.000 B**. Parada obligatoria **antes** del techo; prohibido borrar datos para caber; compresión no asumida; cada estimación declara medido vs hipotético.
- **Campaña de 25 ventanas:** 25 × 1,6 GB = **40 GB > techo** ⇒ **NO se programa ahora** (corrige a la v1); cualquier campaña se re-presupuesta por episodio con tasas medidas. No releer raw ni inventar distribuciones.
- **Contadores 81/74:** 81 eventos − 74 registros = 7 eventos extra ⇒ por palomar **≥1** registro multi-evento; **NO implica ≥7 registros multi-evento** (73×1 + 1×8 = 81 lo reproduce con uno solo) — corrige la errata de confluencia; el desconocido exacto queda nombrado sin releer frames.
- **Requests:** descubrimiento ≤3/lote (§3); `clob observe` = 12 lecturas REST por invocación × 7 invocaciones por episodio (§Plan) reportadas aparte; sin reintentos; `retry_after_seconds`/429 ⇒ registro y fin.

### 9. Supervisión, pausa y cortes (corrección 7)

- **Forma:** secuencia **serial** de comandos foreground pre-escritos (el Plan v2), ejecutada por el lanzador/operador con **outcome durable por paso** (status-file del `record`, recibos de `observe`, verify del journal). Sin daemon, cron ni procesos residentes; si el paso falla, el paso muere y deja recibo — el siguiente paso no arranca sin decisión.
- **Checkpoint duro:** ningún paso inicia o continúa dentro de 02:00–08:00 GMT-3 (pausa COMPLETA, sin gracia). El stop-file se pre-coloca 15 min antes de las 02:00; el episodio cuya ventana intersecte la pausa queda censurado ex ante (§3). No hay captura nocturna ni señal cruzando la pausa.
- **Estado incierto:** tras fallo de transporte (ECONNRESET, 1310) se preservan logs/exit/heartbeats, se corre `journal verify` antes de cualquier relanzamiento y el estado incierto se declara; sin retry automático, sin cambio de proveedor, sin login.
- **Cortes de verificación causal** (idénticos a v1): T−75/T−45/T−15 por replay de manifiestos derivados; invariancia de schedule; corte negativo postcutoff.

### 10. Qué NO es este preregistro

No es promesa de beneficio ni estimación de alpha; el piloto es descriptivo; no certifica fees ni ticks; no habilita live, órdenes, cuentas ni fondos; no reabre `PROJECT_FROZEN_OWNER_2026_09_23`; no reinterpreta tests técnicos como hipótesis económicas; el gate técnico (suite `^TestW1H`) demuestra semántica de receta, jamás un resultado económico.

## Fuentes

- Semántica leída @ `853c0e4`: `internal/regimes/reducer.go` (dedup por contenido), `internal/regimes/prospect.go` (TTL inclusive/stale, adquisición acotada por seq), `internal/capture/capture.go` + `internal/capture/recover.go` (boot único sin exclusión, adopción de boots vivos), `cmd/engine/record.go` / `cmd/engine/clob_observe.go` (serial, journal+store por proceso), `internal/strategy/pocs/sports/sports.go` (B\*, FeeHigh, WalkSide), `internal/economics/economics.go` (sweep/quotes/interval).
- Fixture offline: `internal/experiment/w1h_acquisition_recipe_test.go` (SHA `f7c03a48…fa17`), comando exacto autorizado, **PASS** exit 0 (recibo en OUT `w1-h-economic-pilot-v2-20261029`).
- [[Plan — Single Episode Pilot v2 W1-h 2026-10-29]] (receta), [[Research — Economic Pilot Corrections W1-h 2026-10-29]] (evidencia por corrección), [[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]] (v1, historia), [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §§18–19.
- `.private-execution/w1h/inputs.json` (12 hashes) y `.private-execution/w1h/workspace-preflight.json` (metadata filesystem).
