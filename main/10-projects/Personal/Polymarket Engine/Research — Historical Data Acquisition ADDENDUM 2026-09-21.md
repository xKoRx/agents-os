---
type: research
schema_version: 1
scope: project
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[2026-09-21-historical-research-m0]]"
  - "[[2026-09-21-historical-backtest-readiness]]"
aliases:
  - "Historical Data Acquisition Addendum 2026-09-21"
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: normal
tags:
  - kind/research
  - scope/session
  - area/personal
  - project/polymarket-engine
  - kind/addendum
---

# Research — Historical Data Acquisition ADDENDUM (2026-09-21)

ADDENDUM correctivo one-shot de adquisición y persistencia de datos históricos para Polymarket Engine. Verifica físicamente los proveedores, cierra las brechas de los informes [[2026-09-21-historical-research-m0]] (`HISTORICAL_DATA_PARTIAL`) y [[2026-09-21-historical-backtest-readiness]] (`DESCRIPTIVE_ONLY`) y deja una cohorte histórica durable y verificable. El documento original queda como registro histórico; las conclusiones que este addendum superseda se marcan en la tabla. Dataset durable: repo `xKoRx/polymarket-engine-datasets` → `hist-acq-20260921/` (manifest + SHA256SUMS). Baseline engine: `master` @ `09e8c76` (código `66486ac`). OOS 22:45Z sellado, no tocado. Sports Week intacto (sólo probe read-only de estado).

## Resultado en una línea

`HISTORICAL_DATA_ACQUISITION_RESULT` = adquisición verificada de extremo a extremo (hashes locales = publicador, extracción independiente = multiset idéntico, replay digests 4/4 = COHORT), arquitectura de persistencia seleccionada (Parquet + DuckDB) con equivalencia demostrada contra ClickHouse, y sin compra necesaria hoy: PendulumFlow cubre el dato L2 del cohort a costo $0 bajo CC BY 4.0. Hallazgo certificador nuevo: la reconstrucción del libro por deltas NO es confiable; sólo los snapshots periódicos son estado L2 admisible.

## Tabla correctiva — afirmación → evidencia → corrección → impacto

| # | Afirmación original | Evidencia obtenida 2026-09-21 | Corrección | Impacto en la decisión |
|---|---|---|---|---|
| 1 | `local_full_object_sha256: NOT_RECOMPUTED` (los objetos v3 nunca se verificaron byte a byte en local) | Descarga completa de ambos parquets (866,445,402 y 595,930,005 bytes). SHA-256 local `ee4c5add…` y `5cd4e6b1…` = hashes del publicador en COHORT | Cerrada: `RECOMPUTED_MATCHES_PUBLISHER` para 2026-09-01T21 y T22 | Los journals históricos m0 quedan anclados a bytes verificados; la cadena de custodia es completa |
| 2 | La extracción previa era reproducible en principio, pero sin prueba | Extracción independiente (DuckDB + proyección canónica, código distinto) sobre los bytes frescos: recuentos idénticos (15487/13204/13027/9166) y **multiset de filas idéntico** al explore previo por mercado | Confirmada con prueba fuerte; el hash de archivo difiere sólo por orden/serialización, no por contenido | La ventana congelada 21:10Z→22:40Z es determinista y auditable; ninguna fila fue inventada |
| 3 | Replay digests eran comparables sólo contra sí mismos (misma sesión) | Import fresco en dataset scratch con binario master `66486ac`: digest replay `{1}` == `{32,7,1}` == COHORT en 4/4 mercados (67fdba7b, 701d30b0, 873d0fb2, 04…) | El pipeline journal→replay es reproducible entre sesiones, máquinas y orden de import | `histimport` queda certificado como canal histórico determinista (dentro del alcance no-live M4) |
| 4 | Kickoff con autoridad `SCHEDULE_CORROBORATED_POSTHOC` (sólo statsapi) | CLOB `GET /markets/{condition}`: `game_start_time: 2026-09-01T22:40:00Z` en los 4 mercados + statsapi `gameDate` 22:40:00Z ×4 (status Final) | Autoridad doble fuente venue-declarada: `KICKOFF_VENUE_DECLARED_POSTHOC`. Sigue sin ser captura point-in-time de listing | El gate de kickoff de PE-005-R1 puede consumir campo venue; la variante PIT de listing sigue abierta |
| 5 | Fee `UNRESOLVED` / `REAL_FEE_READY=false` sin dato de fee efectiva | En v3, `last_trade_price` trae `fee_rate_bps`: todas las 256 fills del cohort tienen `fee_rate_bps=0`; CLOB declara `maker_base_fee=taker_base_fee=1000` (parámetro de contrato, sin fee efectiva observada) | Fee efectiva observada en el cohort = 0 bps (dato, no suposición). La certificación económica del engine sigue pendiente owner-side | `REAL_FEE_OBSERVED_0BPS` habilita certificar economía del cohort si el owner congela esa fee en el config |
| 6 | El libro L2 del cohort era reconstruible con snapshots + deltas (implícito en el import y en `describe`) | Certificación directa: reconstrucción snapshot→snapshot vs snapshot real: 66–85% de los intervalos tienen mismatch de BBA (142/216, 117/138, 82/98, 63/84) y ~1,2–2,1k niveles divergentes por mercado por mercado | **Supersedido**: los deltas NO bastan para reconstruir el libro. Sólo el snapshot-as-of (cada ~2–3 min) es verdad L2; el libro extendido por deltas es aproximación no certificada | Los gates de estrategia deben consumir `book` snapshots (marca SYNCING correcta) o declarar aproximación. El sweep del benchmark es metodología, no evidencia de edge |
| 7 | PendulumFlow como fuente de L2 histórico (afirmación comercial/documental) | Verificación física: v3 hourly parquet desde 2026-08-18T06 (probe de límite inferior), 7 tipos de evento con esquema publicado, HTTP Range por byte-range de evento, `timestamp_received` µs, secuencia collector-local, witness multi-máquina; 318B filas, +2,4B/día; licencia CC BY 4.0 (v3 y pmxt); espejo AG6 **sin licencia** (no redistribuir) | Confirmada con caveats de captura (llms.txt del propio archivo advierte 9 falacias de cómputo; coincide con el hallazgo #6) | Fuente primaria $0 para todo el era v3; caution legal sólo en el prefijo third-party/ag6 |
| 8 | PMData: Free / Plus / Enterprise-PIT (afirmación de investigación previa) | Auditoría de pmdata.dev: L2 + price_change + trades + on-chain fills + Chainlink desde 2026-02 (banner: todos los mercados desde 2026-05-01), parquet por mercado/fecha vía API key. Free 600 descargas → 50/mes; Plus $49/mes 1M descargas **uso personal**; Enterprise precio a medida + "Point-in-Time (PIT) Accuracy" + licencia comercial + keys ilimitadas | Los tres planes existen. **PIT no es demostrable como dato adicional**: la documentación pública no distingue si PIT Accuracy añade campos/capturas nuevas o es garantía contractual de captura sin correcciones retroactivas | Compra NO necesaria hoy. Si se necesita PIT comercial: pregunta directa al vendor (¿qué cambia en el esquema?) antes de pagar; Plus es inútil para uso comercial por su licencia |
| 9 | polymarketdata.co como alternativa con L2 "desde 2025-08, resolución 1m" | Sitio audita REST + S3 dumps + SDK; sin precios publicados; endpoints anónimos de muestra no existen (404/redirect verificado); sólo contacto enterprise | **No verificada físicamente**. No usar como supuesto de disponibilidad ni de granularidad | Queda fuera de cualquier decisión hasta que entregue muestra firmada o API de prueba |
| 10 | "Varios proveedores se complementan / se contradicen" (comparación cruzada pedida) | Ejecutable sólo con datos realmente accesibles: PendulumFlow es la única fuente L2 histórica accesible anónimamente. PMData requiere API key (creación de cuenta = acción owner); polymarketdata.co cerrado. Comparación intra-fuente multi-witness: `witness_stats.json` por hora (p50/p90/p99 por máquina) disponible en horas recientes | La comparación entre proveedores **no es ejecutable hoy sin una cuenta PMData**; la comprobación de consistencia interna del archivo sí (manifests + witnesses + sha256) | Para comparar proveedores el owner debe crear la key Free (600 descargas $0) — único pendiente accionable de adquisición |
| 11 | Wayback CDX 503 ⇒ no hay snapshot PIT de Gamma del listing | No reintentado a fondo en esta pasada (prioridad a adquisición física); sigue abierto | Sin corrección: `LISTING_PIT_METADATA` sigue siendo brecha | El único camino demostrado a metadata de listing PIT es un proveedor comercial con PIT verificado |

## Certificación de la muestra por nivel

- **Historia descriptiva (precios, trades, secuencias):** CERTIFICADA — 50.884 eventos, ventanas congeladas, hashes y digests reproducidos 4/4.
- **Libro L2 reconstruible:** PARCIAL — snapshots periódicos como estado as-of (544 snapshots, ~56 niveles promedio); extensión por deltas NO confiable (hallazgo #6). Etiqueta honesta: `L2_SNAPSHOT_ONLY`.
- **Estado point-in-time admisible:** PARCIAL — evento-a-evento con `timestamp_received` µs y `timestamp` venue ms; sin correcciones retroactivas conocidas; clock drift entre witnesses existe (usar `source_witness` único si se comparan arribos — llms.txt).
- **Simulación de ejecución bajo supuestos:** METODOLOGÍA demostrada (benchmark P2–P4 en dos motores con digests idénticos); NO constituye backtest elegible: fee de config pendiente, libro aproximado entre snapshots, `SCREEN_BLOCKED_INBOX` históricos ya resueltos en `66486ac` pero no re-ejecutados aquí.
- **Economía certificada:** NO — `fee_rate_bps=0` observado en datos, pero la decisión de congelar esa fee y certificar economía es owner-side (M4 live-gated).

## Benchmark de almacenamiento orientado a backtesting

Dataset: `events.parquet` 50.884 filas + `book_levels.parquet` 30.424 niveles (cohorte, zstd) + escala de referencia hora llena 80.010.651 filas (mismos objetos v3, sha256 verificados). Fases idénticas en semántica, digests canónicos enteros/decimales; 3 corridas por fase (1 fría-no-cebada, 2 tibias); RSS por `/usr/bin/time -v`; resultados y driver en `hist-acq-20260921/benchmark/`.

| Métrica (cohorte) | A Parquet+DuckDB 1.4.1 | C ClickHouse 25.8.4 (efímero) | B TimescaleDB |
|---|---|---|---|
| Ingesta | 0 s (attach zero-copy al Parquet) | 0,39 s events + 0,16 s levels (CSV→MergeTree) | no ejecutable |
| P1 scan completo | 0,033–0,041 s | 0,087–0,112 s | — |
| P2 reconstrucción de libros (30 cortes ×8 assets) | 0,22–0,34 s | 0,69–0,76 s | — |
| P3 frames 300s ×30 | 0,05–0,10 s | 0,16–0,26 s | — |
| P4 sweep 3 umbrales | 0,04–0,07 s | 0,09–0,15 s | — |
| Escala hora llena (80M filas, P1) | 0,34–0,53 s | 1,35–1,69 s | — |
| RSS máx (proceso consulta) | 38–79 MB | 132–138 MB (cliente; server aparte) | — |
| Espacio | parquet 0,42 MB (cohorte, zstd) | MergeTree ≈ 3–6 MB + TTL n/a | — |
| Complejidad operativa | binario único embebido, cero servicios | server + cliente + config; puerto; lifecycle | server PG + extensión TimescaleDB |
| Equivalencia de resultados | digest `8c6c5554` / `72e62aec` / `67efe361` / `30d78294` | **idénticos** fase por fase | n/a |

**Decisión: A (MinIO/SSD + Parquet + DuckDB) es la arquitectura de persistencia para backtesting del engine.** Gana en cada fase medida, en ingesta (costo cero: el Parquet verificado ES el dataset), en memoria y en complejidad operativa (embebido, sin servicio). Los Parquet originales quedan como fuente durable hash-vinculada; todo derivado (cut_states, índices) es regenerable desde `raw/` con los scripts persistidos. C (ClickHouse) queda documentado como alternativa válida si se pasa a serving concurrente multi-usuario o a escala de archivo completo; la equivalencia ya está demostrada y el costo de migración es bajo porque los digests fijan la semántica. **B no es decidible con evidencia física en esta máquina**: sin sudo, sin docker/podman, sin binarios PG/TimescaleDB; lo que falta exactamente para decidir B: (1) root o runtime de contenedores, (2) imagen/binario `timescaledb-ha` o `timescaledb-2-postgresql-17`, (3) repetir las mismas 5 fases; su perfil row-store + ingesta alta lo orienta a captura viva, no a replay batch, pero eso es hipótesis, no medición.

## Proveedor de pago recomendado

**Ninguno hoy.** El dato del cohort y de toda el era v3 está disponible gratis con licencia CC BY 4.0. Disparadores futuros de compra: (a) necesidad comercial de fills on-chain o Chainlink histórico → PMData (preguntar antes qué agrega Enterprise-PIT en el esquema, y exigir muestra firmada del cohort 2026-09-01 21:00–23:00Z para comparar contra PendulumFlow antes de pagar); (b) era pre-2026-08 con metadata PIT de listing → ninguno la ofrece verificadamente hoy.

## Próxima cohorte ya investigable

La hora completa 2026-09-01T21 ya está en `raw/` (80M filas, sha256 verificado): cualquier mercado del día es extraíble con el mismo pipeline sin costo. Sugerencia no-OOS: repetir cohorte con los kickoffs 23:10Z (ATL/SEA están sellados — NO usar) usando mercados de la ventana 2026-09-02T00+ para no rozar el OOS. Las horas v3 disponibles: 2026-08-18T06 → presente.

## Bloqueos que requieren decisión del owner

1. Crear API key PMData Free (600 descargas, $0, requiere cuenta/email) — desbloquea comparación PMData vs PendulumFlow y evaluación de on-chain fills.
2. Preguntar a PMData qué significa Enterprise "Point-in-Time (PIT) Accuracy" en el esquema (dato nuevo vs garantía contractual).
3. Decidir si se congela `fee_rate_bps=0` observado como fee de certificación económica del cohort.
4. Si se quiere medir B (TimescaleDB): habilitar docker o sudo en la máquina de benchmark.
5. Deuda conocida no tocada aquí: journal sin `account_fact` (DEGRADED) es esperado en investigación; el gate de cobertura de `histimport` (87,8% en ramas IO/parse) sigue en el informe previo.
