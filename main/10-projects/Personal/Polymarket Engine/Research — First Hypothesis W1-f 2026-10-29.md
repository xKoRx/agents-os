---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Preregistration — First Hypothesis W1-f 2026-10-29]]"
  - "[[Research — Prospective Metadata Quality W1-e 2026-10-28]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-f first hypothesis report"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Research — First Hypothesis W1-f 2026-10-29

## Propósito

- Informe canónico del shot W1-f (sesión one-shot, GLM-5.3-Flash Max vía ZCode CLI en `sqx-ulab-hefesto-0`): completar UNA primera hipótesis objetiva preregistrada y evaluable con el Engine real, y entregar el diagnóstico reproducible de si los datos autorizados (capture-v6) alcanzan. Sin búsqueda de rentabilidad ni optimización.
- **Estado vigente (al cierre): HIPÓTESIS W1-F-H1 COMPLETADA — `NO_FALSATION_FIRED_IN_RUN`; veredicto congelado aplicado: `DATA_SUFFICIENT_FOR_GATE_AVAILABILITY_TRIAL`, con las ramas stale y tick-change declaradas INCONCLUSIVE a nivel libro (déficit estructural cuantificado) y economía NO afirmada.** La infraestructura científica quedó probada de extremo a extremo: preregistro congelado antes de medir (test-enforced), oráculos independientes, doble pasada determinista, evidencia con hashes.
- No se tocó: capture-v6 y los 12 inputs (jamás escritos; 12/12 SHA verificados in-process dos veces por corrida), OOS 3901955/3901953 (sellados, jamás leídos), raw/w1b8, código de producción (sólo se añadieron 2 archivos de test; commit local `853c0e4`, sin push).

## Contenido

### ESTADO VIGENTE — cierre W1-f (2026-10-29)

- **Secuencia científica ejecutada en orden:** (1) inventario conceptual y admisibilidad por contratos SIN medir desempeño; (2) elección de la candidata existente más simple compatible con descartes; (3) preregistro fechado+hash congelado en AgentsOS y copia de máquina en OUT ANTES de cualquier medición; (4) harness mínimo en los 2 archivos autorizados; (5) corridas con bugs ordinarios corregidos en-shot hasta ensayo útil; (6) evidencia con hashes y cierre canónico.
- **Selección de candidata (descartes contractivos, sin búsqueda masiva):** PE-002 NegRisk (requiere canastas + fee certificada; v6 no la tiene), PE-005-R1 Sports Reversion (edge indefinible sin fee certificada; 5 min lejos de kickoff sin episodios; requisito de muestra ≥100 frames elegibles por ventana no alcanzado), PE-001 Combinatorial (sin pares ML+SP en v6 — sólo moneylines), PE-030 Weather (sin mercados ni vintages en v6), PE-004 Maturation (no nace mercado nuevo en la ventana). **Elegida:** la falsación del gate de calidad prospectiva W1-e — única compatible con los contratos vigentes y los datos autorizados; candidata económica condicional (S02-style) documentada con sus gates en el preregistro.
- **Preregistro W1-F-H1 (congelado):** MD canónico [[Preregistration — First Hypothesis W1-f 2026-10-29]] + JSON de máquina en OUT (SHA256 `9c56acfad029b6d3a69de75feb1e1234d65df5182abb5af5d6023fe8da7a817b`). Predicciones P1–P7, criterios de falsación y regla de veredicto congelados; al congelar NO se había leído contenido del journal (ningún precio, libro ni frame). El harness de integración **falla cerrado si el prereg falta**: el orden prereg→medición queda test-enforced.
- **Harness (tests del repo, no plataforma paralela; cero cambios de producción):** `internal/experiment/w1f_hypothesis_test.go` (SHA `ec901049…`) — oráculos sintéticos con expectativas calculadas a mano sobre los contratos públicos (`EvaluateTickConstraint`, `ResolveFee`): futuro/postcut por wall y por seq, empate wall+seq, missing capture_seq fail-closed, frontera TTL inclusiva/stale, cuarentena point-in-time, receive time ilegible, y honestidad de fee (ningún POINT inventado; INTERVAL [0,1000] con supuesto U-02; los únicos POINT documentados). `internal/experiment/w1f_hypothesis_integration_test.go` (SHA `18d6fdb9…`) — consume capture-v6 EXCLUSIVAMENTE por APIs read-only existentes (`capture.Verify/OpenView`, `replay.BuildManifest/NewReplayer/RunObservation`, store local de corrida para el reducer+servicio de regimes) y escribe evidencia/manifests SÓLO en OUT con IDs únicos de corrida.
- **Resultado medido (corrida autoritativa 14:45:03Z, ambas pasadas idénticas):**
  - **P1 elegibilidad ✓:** 8/8 assets de libros `OBSERVED_USABLE` al corte 103 (y en cortes 20 y 91); ninguno SYNCING/SUSPECT.
  - **P2 sin lookahead ✓:** los 8 snapshots de libro (uno por asset, todos en seq 17, pared `2026-10-28T19:24:36.967923223Z`) reciben veredicto `constraint_ok` en su propia (pared, seq) con `known_at` del ganador ANTERIOR a la pared del libro; 0 violaciones; sondas negativas: seq=0 no cuenta candidatos y la pared pre-observación (con admisión completa 103) da `no_observation_yet`.
  - **P3 negativa postcut ✓:** digest de observación IDÉNTICO entre cut-20, cut-91, cut-103 y el manifest original (`b8c5854e797fcc3a340bf76554417a9370391c3a58e359e244e4e333a6887715` — byte a byte el registrado por W1-d/W1-e); la metadata final (seqs 92–103) no cambia ningún estado anterior; `regime_digest` pairwise distinto (`8aec29ec…` / `f668990f…` / `e66dfb8c…`, corroborando los valores de continuidad).
  - **P4 determinismo ✓:** schedules `32,7,1` vs `7,32,1` → mismo digest y estados; dos pasadas completas del harness → mismo content digest de evidencia.
  - **P5 frontera stale ✓ (a nivel política, sobre observaciones reales):** decisión en `known_at+TTL` exacto → `constraint_ok` (borde inclusivo); en `+1ns` → `observation_stale`.
  - **P6 honestidad de fee ✓:** 4 condiciones → INTERVAL [0,1000] bps con supuesto U-02 y PointBps ausente; 8 assets → UNRESOLVED con 0 fee observations; 0 POINT en toda la proyección; mbf/tbf 1000/1000 permanecen campos LEGACY, no tasa certificada (`REAL_FEE_READY=false` intacto).
  - **P7 déficit cuantificado ✓:** 0 eventos `tick_size_change`, 0 trades con fee (y 0 trades de cualquier tipo en la enumeración), lag known_at→libro 43,8–47,0 s ≪ TTL 900 s → **las ramas stale y tick-change son INEJERCIBLES a nivel libro dentro de la ventana de 5 minutos**; 1 revisión por entidad (init; final deduplica por contenido); 1 cuarentena record-kind (referencia de página gamma, fuera de alcance), 0 cuarentenas de mercado/asset.
- **Composición real del journal (medida, no inferida):** 103 registros = 1 gamma/data (página de selección) + 24 clobrest/data (12 init + 12 final) + 74 marketws/data (8 book snapshots + 73 eventos que el harness NO clasifica — no son contenido de libro para los reducers del engine) + 4 engine/control. La calidad SYNCING del `capture-status-v6` era la etiqueta del colector W1-d ANTES de W1-e; con el gate real todos los libros quedan OBSERVED_USABLE.
- **Diagnóstico de suficiencia (la pregunta del mandato):** los datos autorizados ALCANZAN para demostrar el gate causal de extremo a extremo (elegibilidad, no-lookahead, postcut, determinismo, frontera TTL a nivel política, honestidad de fee) y NO ALCANZAN para: (a) ejercer stale o cambio de tick a nivel libro (ventana de 5 min ≪ TTL; sin hecho de cambio) — INCONCLUSIVE con déficit exacto: se requiere ventana > 15 min con re-poll fuera de ventana, o un `tick_size_change` real del WS con libro posterior (el modelo ya lo consumiría sin código nuevo); (b) CUALQUIER claim económico (fee sin certificar, muestra de conveniencia de 5 min, 4 mercados/8 assets, sin fill ni liquidez calibrada). Requisitos mínimos para la candidata económica condicional: fee certificada (mapeo documental base_fee↔feeRate o trades convergentes), ≥100 frames elegibles por ventana preregistrada, ventanas > TTL.
- **Calidad del proceso (historia de corridas preservada):** corrida 1 NOT_RUN (bug de ruta: `capture.Verify` espera el data-dir padre); corrida 2 (14:39) con defecto de determinismo propio (el número de pasada entraba al content digest — corregido); corrida 3 (14:40/14:42) con dos defectos menores de evidencia (comparación de prefijos de corroboration con longitudes distintas; 66 registros WS sin clasificar → añadidos buckets honestos); corrida 4 (14:45) AUTORITATIVA. **Incidente registrado:** las corridas 2–3 escribieron manifests derivados con nombres SIN run-id y se sobrescribieron entre sí (los SHA de los bytes perdidos quedaron dentro de las evidencias de esas corridas; desde la corrida 4 todo nombre lleva run-id). Inputs jamás afectados.
- **Recibo de reproducibilidad:** HEAD inicial `7d519eb712a6a4ec9f369c92d9ee2c735454678b` → commit `853c0e46c9be2de4e84201e240e9cf8366b1036e` «Preregister and exercise first offline Polymarket hypothesis» (2 archivos, +1043 líneas, árbol limpio, sin push). Suite completa `go test -p 1 -count=1 -timeout 15m ./internal/experiment` PASS final 13.875s; BUILD exit 0 con binario byte-idéntico entre rebuilds (`engine` SHA `3d8b83f5605f3ee9cf11478326f41163b5093363709b73c70e74348bd5ec2197`; el código de producción no cambió). go.mod `b3a5f56b…`, go.sum `7d442ddd…`, go1.27.1. Recibo maestro: `W1-F-MANIFEST.json` en OUT con todos los hashes (evidencias `0d305e7a…`/`f844d11c…`).
- **Denegaciones registradas (sin reintentos ni variantes):** `find`/`ls` sobre el repo (incluso rutas propias del scope) → descubrimiento de paths vía continuidad canónica + Read directo; `sha256sum` multi-path y sobre el MD canónico del vault → recibo canónico sin hash del MD (binding = copia de máquina); `mkdir`/`date` (Write creó los padres; los muros de tiempo los estampa el harness Go); `git diff --cached --stat/--check` combinados (formas separadas permitidas). TodoWrite bloqueado por el perfil del shot (como en W1-e).

## Límites

- Cinco minutos y una ventana NO prueban estabilidad entre polls, edge ni rentabilidad; el veredicto es de DISPONIBILIDAD técnica, no de valor económico. `ProspectiveTickTTL=15m` sigue siendo política de investigación. El fee INTERVAL [0,1000] bps es un escenario acotado por campos declarados LEGACY, nunca una tarifa certificada. El freeze de producto sigue vigente; live sigue cerrado; Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real.

## Fuentes

- [[Preregistration — First Hypothesis W1-f 2026-10-29]] y su copia de máquina hasheada en OUT.
- [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §§18 (W0…W1-e) y [[Research — Prospective Metadata Quality W1-e 2026-10-28]], [[Research — Public Market Capture W1-d 2026-10-28]].
- Código real leído: `internal/regimes/{prospect,service,reducer,feeresolver}.go`, `internal/books/reducer.go`, `internal/replay/{replay,manifest}.go`, `internal/experiment/experiment.go`, `cmd/engine/{replay}.go` @ `7d519eb`.
- Evidencia: OUT `validated-baseline/w1-f-first-hypothesis-20261029/` (recibo maestro `W1-F-MANIFEST.json`).

## Erratas y alcance de la evidencia (añadido 2026-10-29, shot W1-g; el texto original de arriba se preserva íntegro)

- **(a) Orden prereg→medición:** la existencia y el hash del prereg al correr (y el fail-closed del harness si faltara) demuestran **artefacto disponible e íntegro al momento de medir**, NO que la escritura del prereg precedió a toda inspección previa de código/manifests. La evidencia de orden queda limitada al registro observable de la sesión (transcripción + artefactos); `frozen_before_measurement` y "test-enforced" deben leerse como declaración registrada + control de integridad, no como prueba independiente de autoría previa por missing-file-gate.
- **(b) P1–P7 son regresiones técnicas, no evidencia económica:** esas predicciones restate semántica ya establecida por W1-e (gate prospectivo, TTL inclusivo/stale, cuarentenas PIT, fee honesta). Su confirmación en W1-f verifica que la cadena se comporta como documentada; NO constituye nueva evidencia económica. `DATA_SUFFICIENT_FOR_GATE_AVAILABILITY_TRIAL` es un veredicto de disponibilidad técnica.
- **(c) Composición del journal — unidades distintas, no conciliación inventada:** "74 marketws" son **registros** de journal (`surface_histogram[marketws/data]`; capture-status-v6: 103 frames WS recibidos / 74 admitidos / 0 rechazados), mientras que "8 book + 0 + 0 + 0 + 0 + 73 = 81" son **eventos** enumerados parseando los payloads de esos 74 registros con `ParseMarketWSFrame` (cada registro puede traer múltiples eventos array-wrapped; código de contadores en `internal/experiment/w1f_hypothesis_integration_test.go`, bucle de enumeración). La ecuación "74 = 8 + 73" del párrafo de composición (y de `W1-F-MANIFEST.json`) es una errata de confluencia de unidades: lo medido es 74 registros → 81 eventos clasificados. **No conciliado (se nombra el desconocido exacto, sin releer frames):** qué registros traían >1 evento y si alguno rindió 0 eventos; 81−74=7 sólo acota que al menos 7 registros llevaron eventos múltiples. Los artifacts OUT de W1-f permanecen inmutables como evidencia; esta fe de erratas vive en esta nota, en la nota PREREG W1-f y en el paquete W1-g.
- Los manifests derivados sobrescritos por las corridas 2–3 se mantienen como historia (SHAs de los bytes perdidos dentro de las evidencias de esas corridas); no se recrearon bytes ni se certificaron intermedios por hash.
