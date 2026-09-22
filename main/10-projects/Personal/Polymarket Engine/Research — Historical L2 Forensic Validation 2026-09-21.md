---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Historical Data Acquisition ADDENDUM 2026-09-21]]"
aliases:
  - "Historical L2 Forensic Validation 2026-09-21"
  - "HISTORICAL_L2_FORENSIC_RESULT"
tags:
  - kind/doc
  - scope/project
  - area/personal
  - project/polymarket-engine
created: "2026-09-21"
updated: "2026-09-21"
---

# Research — Historical L2 Forensic Validation 2026-09-21

## Propósito

Validación forense one-shot del hallazgo #6 del ADDENDUM (reconstrucción L2 por deltas no confiable, BBA mismatch 66-85%). Verifica la causa del drift sin asumir que el reconstructor previo es correcto, determina la resolución utilizable del histórico gratuito y cierra la decisión de adquisición: `HISTORICAL_L2_FORENSIC_RESULT` = **`L2_RECONSTRUCTIBLE`** (con caveats declarados). El drift declarado fue un artefacto del modelo de reconstrucción del cert, no de los datos.

## Contenido

### 1. Causa demostrada del drift

- El generador de `results/reconstruction_cert.json` no fue persistido (sólo el JSON hasheado); la reproducción se hizo con reconstructor propio desde los parquets crudos verificados (sha256 = publicador, re-verificado 2026-09-21).
- Con semántica correcta (upsert: `price_change.size` = tamaño nuevo del nivel, 0 = borrar; 6.134 eventos size=0 en la cohorte, 0 negativos), estado por asset, orden arrival o venue: **BBO mismatch 0/628 intervalos (horas completas) y 0/536 (ventana 21:10-22:40Z)**. El drift de precio del cert NO es reproducible con ningún modelo per-asset correcto.
- El modelo del cert queda identificado como **aditivo-sin-borrado** (delta suma sobre el nivel, nada se elimina): reproduce los `levels_diff` del cert (1.242-2.148 por mercado vs 1.191-2.072 declarados, Δ≤8%) y en ese modelo el BBO y los tamaños derivan monótonamente (sólo pueden mejorar), lo que genera exactamente la clase de drift que el cert midió. El SQL P2 de `bench_driver.py` codifica el mismo modelo defectuoso (`max(snap_bb, d_bb)` + suma de tamaños).
- Mezcla cross-asset (estado por mercado) descartada como causa: produce ~100% de mismatch, no 66-85%.
- Hallazgo paralelo: `SHA256SUMS.txt` del dataset tiene 3 entradas stale (ruta `benchmark/results/reconstruction_cert.json` inexistente; el archivo real vive en `results/` con hash `fa8977fe…` que sí corresponde). Integridad del resto: 18/18 OK.

### 2. Categorías de discrepancia con ejemplos reproducibles

- **Defecto del reconstructor (causa del 66-85%):** variante `addnodelete` en `hist-l2-forensic-20260922/scripts/recon.py`; cert vs correcto: 117/138 vs 0/69 (19a016da).
- **Eventos ausentes reales (huecos de captura, ~0,1% de deltas):** 50/628 intervalos (7,96%) tienen ≥1 nivel con tamaño divergente al snapshot siguiente; 66 niveles en 2h; **BBO jamás afectado**. Ejemplo reproducible: asset `1fc6d5c6` nivel BUY 0.02 pasa 15.290,55 → 30,55 entre snapshots 21:45:38Z → 21:49:36Z sin ningún delta en el archive (`scripts/drill.py`). Los huecos se autodetectan y autocuran en el snapshot siguiente.
- **Mezcla de recolectores:** `sequence` es collector-local (rangos 2,81e14 vs 5,3e16 entre witnesses); merge de estas horas conserva copia del último dominio activo `e`; books de otros witnesses llegan hasta 674 s tarde (skew p50 43-44 ms, p99 ~3-4 s) → el replay físico debe ordenar por tiempo venue, no por arrival. Con cualquiera de los dos órdenes el resultado de BBO es idéntico (0 mismatch).
- **Limitaciones inevitables del archivo:** timestamps venue en ms empatan (orden intra-ms no exacto); sin queue position (touch-is-not-fill, upper bound); incidente venue `2026-09-01-db-replica-lag` con restart CLOB 22:30→23:54Z intersecta los últimos 10 min de la ventana congelada (2 de 7 residuos caen ahí; no hay concentración anómala); `boundary_dropped` documentado por el propio archive (944 price_change T21, 5.276 T22 en fronteras de hora). Dedup: 0 filas duplicadas exactas, 0 secuencias duplicadas por hora.

### 3. Resolución utilizable (cohorte 4 mercados MLB, 2h completas + ventana congelada)

- **L2 continuo verificable:** 92,04% de los intervalos (628) reconstruyen la profundidad completa exacta; 7,96% con 1-2 niveles de tamaño divergentes (detectables al snapshot siguiente); ventana congelada: 97,39% exactos. Verificabilidad: cada snapshot certifica la reconstrucción previa.
- **BBO continuo verificable:** 0% de error en 628 intervalos + 99,61% de acuerdo (514/516) contra la traza independiente `best_bid_ask` del venue (las 2 discrepancias = 1 tick en 1 instante, tokens complementarios del mismo mercado).
- **L2 sólo snapshots:** cadencia mediana 13,5-67,4 s por mercado; huecos máximos 7,8-13,7 min; 2 de 4 mercados con snapshots densos en la ventana de kickoff (40-52 books en 22:35-22:45Z) y 2 con books escasos (2 books; `9f9a19e8` sin book en 22:40-22:45Z) — pero deltas densos (748-3.896 en 10 min) y BBO por deltas validado.
- **Inválido/censurado:** 22:30→22:40Z de la ventana (restart CLOB venue); fronteras de hora con drops documentados; nada más.

### 4. PE-005-R1 (Sports Reversion, horizonte 5 min)

Investigable con el dato gratuito a nivel BBO: reconstrucción snapshot+deltas con semántica upsert anclada por snapshots, con la cobertura de deltas pre-kickoff demostrada (los 4 mercados tienen game_start_time venue-declarado y delta flow grueso en los 10 min previos). La simulación de ejecución con profundidad sigue limitada a snapshot-as-of y a upper bound (touch-fill), y el flujo pre-kickoff de books escasos en 2 mercados exige consumir BBO reconstruido, no snapshots crudos. Sin introducir sesgo incompatible con el horizonte: el sesgo sería consumir el modelo aditivo (ya refutado).

### 5. Benchmark mínimo posterior (cadena completa, DuckDB baseline, sin nuevas bases)

Parquet verificado (sha=publicador) → extracción determinista (89.718 eventos) → reconstrucción correcta 0,335 s para 8 assets × 2h + 30 cortes (`results/cut_states_upsert.json`, digest `c5f3b52b…`, 240 filas) → frames p3 del bench A (digest `67efe361…`) → engine Go `09e8c761` replay digests 4/4 = COHORT con journal sin huecos → múltiples backtests p4 sweep 3 umbrales (digest `30d78294…`, metodología, no evidencia de edge).

### 6. Almacenamiento

Dataset `hist-acq-20260921/` (2,1 GB): integridad completa (raw = hashes del publicador; 18/18 archivos OK + cert con ruta stale), destino físico único local `/home/kor/go/src/github.com/xKoRx/polymarket-engine-datasets/` (SIN git ni remote: los derivados y manifests no tienen segunda copia; el raw es re-descargable del archive por sha). Disco local 88% usado (13G libres). **MinIO homelab operativo (12 buckets) pero NO autorizado para este dataset** (sin bucket ni policy polymarket; freeze `STORAGE-ORGANIZATION-FREEZE` de BACKUP-DR activo, gate `STORAGE_ORGANIZATION_COMPLETE` pendiente) → bloqueo exacto: autorización owner de bucket/uso + cierre del freeze. Sports Week intacto (`sports-week-capture.service` running, no se tocó `sports-week-pe005/`). Sin borrado de evidencia.

### 7. Proveedores alternativos

Sin brecha que justifique compra para el era v3: el L2 gratuito es reconstruible. Brechas residuales que una muestra ajena sí ayudaría a acotar: cuantificar si los huecos ~0,1% son del archivo o del venue; resolución intra-ms; calidad pre-2026-08-18. Solicitudes concretas de muestra (mismos 4 condition ids, 2026-09-01 21:00-23:00Z, tipos book/price_change/best_bid_ask) preparadas en `hist-l2-forensic-20260922/results/SAMPLE_REQUESTS.md` — PMData requiere cuenta+key (acción owner, plan Free $0) y polymarketdata.co contacto enterprise. Sin compras ni aceptación de condiciones (esperando autorización).

## Decisión

`L2_RECONSTRUCTIBLE` para el era v3 (2026-08-18→presente) bajo protocolo obligado: semántica upsert, orden venue-time (o arrival con curado por snapshot), separación estricta por asset, BBO siempre con verificación por snapshot, ventana de incidente venue marcada. El veredicto `SNAPSHOT_ONLY` del ADDENDUM queda **supersado** en su fundamentación (era consecuencia del modelo aditivo); la cadencia snapshot sigue siendo el único estado certificado sin reconstrucción. Siguiente experimento históricamente ejecutable: cohorte no-OOS con kickoffs 23:10Z del 2026-09-02 (ventana 2026-09-02T00+) reconstruida con este protocolo para PE-005-R1 a nivel BBO.

## Fuentes

- Workspace forense: `~/aranea/work/hist-l2-forensic-20260922/` (scripts `recon.py`/`drill.py`/`bba_check.py`/`cut_states.py`, data `cohort_full.ndjson`, resultados JSON).
- Dataset: repo `xKoRx/polymarket-engine-datasets` → `hist-acq-20260921/` (raw parquets sha=publicador, MANIFEST, SHA256SUMS, `results/reconstruction_cert.json`).
- [[Research — Historical Data Acquisition ADDENDUM 2026-09-21]] (hallazgo #6 corregido por esta validación).
- Manifests del archive: `archive.pendulumflow.com/v3/2026-09-01/{21,22}/manifest.json` + página `/audit` (incidente db-replica-lag) + `providers/pf-llms.txt` (falacias de cómputo).
