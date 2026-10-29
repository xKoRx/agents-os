---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Prospective Metadata Quality W1-e 2026-10-28]]"
  - "[[Research — Public Market Capture W1-d 2026-10-28]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-f preregistration H1"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Preregistration — First Hypothesis W1-f 2026-10-29

## Propósito

- Preregistro **congelado antes de medir** de la primera hipótesis objetiva y falsable del programa offline (shot W1-f, sesión one-shot GLM-5.3-Flash Max vía ZCode CLI en `sqx-ulab-hefesto-0`). No busca rentabilidad ni optimiza nada: es un **ensayo técnico de falsación de disponibilidad** sobre la cadena real de calidad prospectiva del Engine, y el diagnóstico reproducible de si los datos autorizados (capture-v6) alcanzan.
- Estado del checkout al congelar: `w0/offline-causal-replay-20261027` @ `7d519eb712a6a4ec9f369c92d9ee2c735454678b`, árbol limpio. Copia de máquina en OUT: `/home/kor/Documents/Codex/2026-10-27/task-2/validated-baseline/w1-f-first-hypothesis-20261029/w1f-preregistration-h1.json` (SHA256 `9c56acfad029b6d3a69de75feb1e1234d65df5182abb5af5d6023fe8da7a817b`). El harness Go verifica la existencia/hashing del prereg y falla cerrado si falta: el orden preregistro→medición queda test-enforced.
- Al congelar NO se había leído contenido del journal (ningún precio, libro ni frame). Entradas del autor: continuidad canónica (W1-c/W1-d/W1-e), los 6 manifests de capture-v6 (sólo metadata), la tabla de 12 SHAs en `.private-execution/w1f/inputs.json` y el código fuente en el checkout.

## Contenido

### Selección de candidata (inventario y admisibilidad, sin medir desempeño)

Candidatas existentes evaluadas por contratos/esquema:

| Candidata | Veredicto | Razón contractiva |
|---|---|---|
| PE-002 NegRisk (S01) | Inadmisible | Requiere canastas multi-mercado con fee certificada; v6 son 4 moneylines no emparentados, fee INTERVAL [0,1000]/UNRESOLVED, `REAL_FEE_READY=false`. |
| PE-005-R1 Sports Reversion (S02) | Inadmisible económicamente | Edge/taker sin fee certificada; ventana de 5 min lejos de kickoff sin episodios; requisito de muestra (≥100 frames elegibles por ventana T-90min) no alcanzado por construcción. Se documenta como **candidata condicional** (ver abajo). |
| PE-001 Combinatorial (S03) | Inadmisible estructuralmente | Necesita pares ML+SP del mismo evento; v6 sólo trae moneylines. |
| PE-030 Weather (S04) | Inadmisible | Sin mercados/clima ni vintages en v6. |
| PE-004 Maturation O/B (S05) | Inadmisible | No nace mercado nuevo en la ventana de 5 min; cohorte ausente. |
| **Gate de calidad prospectiva (W1-e) como objeto de falsación** | **ELEGIDA** | Única compatible con los contratos vigentes y los datos autorizados: los contratos existen (`regimes.EvaluateTickConstraint`, `AssetConstraintAsOf`, gate real de books, replay read-only), la muestra contiene exactamente las clases de evidencia requeridas (observaciones init seqs 4–15, libros WS seqs 16–90, metadata final seqs 92–103) y la pregunta es objetiva, falsable y sin claim económico. |

Candidata condicional documentada (NO ejecutada aquí): S02-style spread-reversion en SHADOW sobre capturas futuras, admitible sólo cuando: (1) fee certificada (mapeo documentado base_fee↔feeRate o evidencia trade convergente), (2) hecho real de cambio de tick con libro posterior, (3) ventanas > TTL con re-polls, (4) ≥100 frames elegibles por ventana preregistrada.

### Hipótesis W1-F-H1 (congelada)

**Enunciado:** sobre capture-v6 (4 moneylines, 8 assets, una ventana WS de 5 minutos + metadata CLOB init/final), el gate REAL de calidad prospectiva del Engine (`regimes.AssetConstraintAsOf`, TTL 15 min política congelada, causalidad PIT acotada por admisión) es demostrablemente causal de extremo a extremo: cada snapshot completo de libro queda OBSERVED_USABLE en su propia pared de recepción y secuencia de journal con cero lookahead; la elegibilidad es invariante bajo cortes negativos; la metadata final no habilita decisiones pasadas; el eje fee permanece honestamente sin resolver (ningún POINT inventado); y la ventana de 5 minutos es estructuralmente insuficiente para ejercer las ramas stale y tick-change a nivel libro, lo cual se declara como déficit cuantificado, no ocultado.

### Predicciones y criterios de falsación

- **P1 elegibilidad:** replay del manifest ORIGINAL de v6 (cutoff 103) con schedule `32,7,1` → exactamente 8 assets de libros, todos OBSERVED_USABLE al cierre, ninguno SYNCING/SUSPECT.
- **P2 sin lookahead por libro:** para CADA evento de snapshot completo (asset a, pared t, seq s) enumerado del journal: veredicto `AssetConstraintAsOf(a,t,s)` = `constraint_ok` con TickKnown=true, Suspect=false, y KnownAt del ganador ≤ t. Sondas negativas: veredicto en (pared del primer libro, seq=0) no cuenta ningún candidato (cota de admisión); veredicto en (pared estrictamente anterior al primer known_at del asset, seq=103) = `no_observation_yet` (cota de recepción).
- **P3 negativa postcut:** digests de replay: cut-91 == cut-103 == manifest original (los tres iguales); la metadata final (seqs 92–103) no cambia ningún estado de libro anterior; `regime_digest` distingue prefijos consumidos (cut-20 ≠ cut-91 ≠ cut-103).
- **P4 determinismo:** dos `RunObservation` con schedules distintos (`32,7,1` y `7,32,1`) → mismo digest y mismos estados; dos pasadas independientes del harness → mismo digest de contenido de evidencia (excluyendo IDs/paredes locales).
- **P5 frontera stale a nivel política:** con las observaciones init reales: decisión en `first_known_at+TTL` exacto = `constraint_ok` (borde inclusivo); en `+1ns` = `observation_stale`. La rama stale se ejercita a nivel política sobre datos reales; a nivel LIBRO no existe veredicto stale en ventana (ver P7).
- **P6 honestidad de fee:** con la proyección cut-103: las 4 condiciones resuelven fee INTERVAL [0,1000] bps con PointBps ausente (caso 3, supuesto U-02); los 8 assets resuelven UNRESOLVED con cero observaciones de fee; ningún POINT; los campos legacy mbf/tbf 1000/1000 nunca son tasa certificada.
- **P7 déficit cuantificado:** cero eventos `tick_size_change` del WS y cero cambios de lexema de tick en la ventana; para todo libro, lag(known_at→pared) < TTL(15 min) (el gate jamás pasa a stale en ventana); cada asset y condición lleva exactamente 1 revisión proyectada (contenido init; final deduplica por contenido). Veredicto: las ramas stale y tick-change son INEJERCIBLES a nivel libro en una ventana de 5 minutos — déficit estructural de los datos autorizados, cuantificado por el harness.

**Regla de veredicto (congelada):** si ninguna falsación dispara → `DATA_SUFFICIENT_FOR_GATE_AVAILABILITY_TRIAL` con ramas stale/change INCONCLUSIVE (P7). Si alguna dispara → `HYPOTHESIS_FALSIFIED` con el artefacto violador exacto e INCONCLUSIVE general. Si faltan inputs o falla integridad → NOT_RUN/INCONCLUSIVE con causa. Ningún resultado aquí es claim de rentabilidad, edge ni live.

### Corroboraciones esperadas de registros previos (no selección)

Prefijos 16-hex registrados por la continuidad W1-d/W1-e, usados como corroboración (la repetición del digest de observación de W1-d NO prueba la integración W1-e; la prueba es código+tests+`regime_digest`): digest de observación cut-91/cut-103/original = `b8c5854e797fcc3a…`; `regime_digest` cut-103 = `e66dfb8c…`; frontier durable 103; 8 assets; 74 frames admitidos.

### Señal, entradas, salida, límites

- **Señal:** veredictos point-in-time del gate real sobre snapshots de libros reconstruidos (sin estrategia, sin órdenes).
- **Entradas:** journal de capture-v6 vía APIs existentes read-only (`capture.OpenView/Verify`, `replay.BuildManifest/NewReplayer/RunObservation`, store temporal, reducer+servicio de regimes). Los 12 inputs con SHA de `.private-execution/w1f/inputs.json` se verifican in-process por el test; mismatch → fallo de cadena de custodia.
- **Salida:** evidence JSON + manifests derivados SOLO en OUT (`/home/kor/Documents/Codex/2026-10-27/task-2/validated-baseline/w1-f-first-hypothesis-20261029`), IDs únicos, jamás sobrescribir; inputs jamás escritos.
- **Tamaño virtual:** N/A (no corre estrategia, no se consume bankroll virtual; 0 órdenes, 0 fills, 0 fills simulados). **Latencia:** sólo observacional (distribución de lag known_at→pared del libro). **Fill:** ninguno (no confundir libros reconstruidos, trades observados y fills simulados). **Costes:** escenarios fee INTERVAL [0,1000] bps de campos LEGACY declarados; nunca certificados ni aplicados a PnL.
- **Requisitos de muestra:** los de CUALQUIER hipótesis económica futura NO se alcanzan con v6 y NO se intentan aquí (ver candidata condicional). **Split exploratorio/OOS:** no aplica (ventana única totalmente preregistrada; sin tuning ni selección de modelos); OOS 3901955/3901953 permanece SELLADO y no leído.
- **Límites de ejecución:** CPU 2 / RAM 2 GiB; comandos preflight del perfil; sin red nueva, sin capturas, sin Parquet, sin raw; gofmt sólo sobre los 2 archivos propios.

### Harness autorizado (tests del repo, no plataforma paralela)

- `internal/experiment/w1f_hypothesis_test.go` — oráculos sintéticos independientes (futuro/postcut, empate wall+seq, stale, unknownfee, metadata final no habilita pasado), expectativas calculadas a mano.
- `internal/experiment/w1f_hypothesis_integration_test.go` — evidencia REAL: consume el journal de v6 por APIs existentes, extrae resumen mínimo y escribe evidence/manifests SOLO en OUT; falla cerrado si el prereg falta.

## Fuentes

- [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §§18 (W0…W1-e, bullets 1–17) y "Siguiente paso concreto".
- [[Research — Prospective Metadata Quality W1-e 2026-10-28]]; [[Research — Public Market Capture W1-d 2026-10-28]].
- Manifests v6 (sólo metadata): `selection-manifest-v6.json`, `capture-manifest-v6.json`, `preregister-v6.json`, `observe-init-v6.json`, `observe-final-v6.json`, `capture-status-v6.json`.
- `.private-execution/w1f/inputs.json` (12 SHAs autorizados).
- Código real leído en el checkout @ `7d519eb`: `internal/regimes/{prospect,service,reducer,feeresolver}.go`, `internal/books/reducer.go`, `internal/replay/{replay,manifest}.go`, `internal/experiment/experiment.go`, `cmd/engine/replay.go`.
