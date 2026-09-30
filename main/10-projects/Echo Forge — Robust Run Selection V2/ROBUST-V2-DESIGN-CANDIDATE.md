# ROBUST-V2-DESIGN-CANDIDATE

Status: `DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW`

Date: 2026-09-29

Scope: diseño pre-implementación de robust run selection intra-strategy para Echo Forge. No product code, no SPEC final, no implementación autorizada.

## 1. Problem statement

V1 calcula una noción de dispersión local para cada neighborhood 3×3, pero el durable ranking no usa esa robustez como criterio principal. La reconstrucción del source muestra:

```text
dispersion_cov:
  D_sharpe = CoV(Sharpe[3×3])
  D_profit = CoV(NetProfit[3×3])
  robustness = 1 / (1 + D_sharpe + D_profit)

durable ranking:
  1. ranking_metric(center) DESC
  2. robustness DESC
  3. runs ASC
  4. OOS ASC
```

En wave2a el ranking metric durable es `sharpe_ratio`.

Consecuencia: un center atractivo puede ganar aunque exista otro neighborhood cuya superficie sea más estable. La robustez queda reducida a desempate y no gobierna realmente la selección.

El objetivo V2 no es "elegir el menor cliff" ni "maximizar robustness". Es seleccionar una **meseta paramétrica de buena calidad**, evitando tanto peaks frágiles como plateaus mediocres.

## 2. V1 source reconstruction

Autoridades verificadas en `xKoRx/symphony`:

- `sqx/core/wfm/evaluator.go`: `scoreDispersionCoV`, CoV de Sharpe/Net Profit y score escalar.
- `sqx/adapters/wfm/binding/evaluate.go`: `rankDurablePicks` ordena primero por `ranking_metric(center)`, después por `score`, después por `runs` y `OOS`.
- `sqx/adapters/wfm/binding/config.go`: default durable `RankingMetricSharpe`, `PrimaryMetricRetDD`.
- `specs/FEAT-SQX-DURABLE-ROBUST-SELECTION/SPEC.md`: `select_robust_run` consume exactamente un `rank == 1`; no recalcula ranking.

No se encontró defecto material en la separación arquitectónica actual:

```text
evaluate_wfm
  -> construye neighborhoods
  -> decide eligibility / warnings
  -> rankea picks

select_robust_run
  -> consume aggregate
  -> materializa rank == 1
```

V2 debe modificar la semántica del ranking/evaluation upstream, no convertir `select_robust_run` en un segundo evaluator.

## 3. Desired invariants

### I1 — Intra-strategy only

Cada Strategy se evalúa contra sus propios neighborhoods. No existe score Strategy-vs-Strategy.

### I2 — Stability != performance level

La policy debe producir dos conceptos separados:

- **stability**: cuánto cambia el comportamiento dentro del 3×3.
- **quality**: nivel de performance de la meseta.

Ninguna transformación debe ocultar uno dentro del otro.

### I3 — Peak resistance

Un center alto rodeado por degradaciones materiales no puede ganar sólo por su center metric.

### I4 — Bad plateau resistance

Una superficie muy estable pero consistentemente mediocre no puede ganar sólo porque su dispersión es mínima.

### I5 — Tail awareness

Un único vecino extremadamente malo debe ser visible aunque MAD sea pequeño.

### I6 — Broad-instability awareness

Varias degradaciones moderadas deben ser visibles aunque no exista un único cliff extremo.

### I7 — Determinism

Mismo conjunto de CELLs, independiente del input order, produce mismo ranking exacto.

### I8 — Fail closed on invalid required evidence

Required metrics missing/NaN/Inf, duplicate cells o neighborhood incompleto no se imputan ni se convierten en cero.

### I9 — Small policy perturbation should not cause chaotic rank1 churn

Cambios pequeños de threshold o de un score diagnóstico deben generar churn limitado y explicable.

### I10 — No historical-profit optimization

La policy no se selecciona por cuál habría producido más profit en wave2a.

## 4. Operational taxonomy

Para un neighborhood 3×3 elegible:

### Plateau

Neighborhood con dispersión local baja en las métricas relevantes y sin tail Ret/DD incompatible con la meseta. No implica buen nivel de performance.

### Peak

Center materialmente mejor que el entorno, con superficie local peor. Puede existir incluso cuando el MAD global del 3×3 parece bajo.

### Cliff

Una caída local extrema de Ret/DD respecto del nivel representativo del neighborhood. Es un problema de tail/local downside, no de dispersión global.

### Unstable neighborhood

Neighborhood con dispersión amplia en una o más métricas, aunque no tenga un único punto extremo.

### Robust-but-bad plateau

Stability alta pero nivel mediano de performance claramente inferior a otros plateaus comparables de la misma Strategy.

### High-quality robust plateau

Neighborhood sin cliff inadmisible, no dominado en estabilidad y con nivel mediano fuerte dentro del conjunto comparable de esa misma Strategy.

## 5. Candidate mathematical contract

### 5.1 Required neighborhood metrics

Para V2, cada una de las 9 CELLs del neighborhood debe tener observaciones finitas de:

```text
Ret/DD
Sharpe
Net Profit
```

Si cualquiera falta o es NaN/Inf, el neighborhood es ineligible.

Esta exigencia es más estricta que V1 `dispersion_cov`, porque Ret/DD pasa a ser parte explícita de la policy.

### 5.2 Robust location

Para cada métrica `x`:

```text
L_x = median(x_1 ... x_9)
```

La mediana representa el nivel del plateau y evita que el center o un outlier único definan el neighborhood.

### 5.3 Robust dispersion

Candidate:

```text
MAD_x = median(|x_i - median(x)|)
scale_x = median(|x_i|)

D_x =
  0                if scale_x == 0 and MAD_x == 0
  +Inf             if scale_x == 0 and MAD_x > 0
  MAD_x / scale_x  otherwise
```

Aplicar a:

```text
D_retdd
D_sharpe
D_profit
```

Razón para usar `median(abs(x))` como denominador y no `abs(median(x))`:

- tolera mejor signos mixtos;
- evita singularidades artificiales cuando la mediana cruza cero pero la magnitud típica no;
- mantiene escala relativa;
- sigue siendo KISS y robusto a outliers.

### 5.4 Optional diagnostic stability score

Para observabilidad y sensitivity, no como ranking authority:

```text
S_x = 1 / (1 + D_x)
S_diag = exp(
  w_retdd * ln(S_retdd) +
  w_sharpe * ln(S_sharpe) +
  w_profit * ln(S_profit)
)
```

con pesos exploratorios solamente:

```text
40/30/30
50/25/25
60/20/20
```

La geometric mean es razonable como diagnóstico porque una dimensión muy mala no queda totalmente compensada por otras dos buenas. Sin embargo, convertir `S_diag` en autoridad de ranking introduce una scalarización arbitraria y reabre una pelea de weights que no es necesaria para V2.

**Recommendation:** conservar `S_diag` sólo para audit/sensitivity y no usarlo como primer sort key.

### 5.5 Stability authority: Pareto layers

Representar la estabilidad de cada candidate como vector:

```text
D = (D_retdd, D_sharpe, D_profit)
```

Candidate A domina a B si:

```text
A.D_retdd <= B.D_retdd
A.D_sharpe <= B.D_sharpe
A.D_profit <= B.D_profit
```

y al menos una desigualdad es estricta más allá de epsilon determinístico.

Construir capas no-dominadas:

```text
layer 1 = candidates no dominados
layer 2 = no dominados después de remover layer 1
...
```

Esto elimina weights del camino crítico y preserva el concepto de stability como vector, no como performance.

## 6. Ret/DD design

### 6.1 Why Ret/DD needs two independent views

Ret/DD debe aportar:

1. **broad stability** mediante `D_retdd`;
2. **tail downside** mediante cliff guard.

MAD y cliff no son duplicados:

- MAD detecta múltiples degradaciones moderadas / superficie amplia.
- Cliff detecta un punto extremo que MAD puede ocultar.

Wave2a muestra ambos tipos de contraejemplo.

### 6.2 Center-relative cliff hypothesis — rejected as primary definition

Hipótesis:

```text
(center_retdd - min_retdd) / abs(center_retdd)
```

Problemas:

- mezcla tail risk con qué tan especial es el center;
- castiga más a centers altos aun cuando el resto del plateau tenga buen nivel;
- explota cerca de center=0;
- center negativo produce semántica difícil de interpretar;
- no describe "caída desde la meseta", describe "caída desde un punto particular".

### 6.3 Candidate cliff definition

Usar el nivel representativo del neighborhood:

```text
R = RetDD[3×3]
L = median(R)
scale = median(abs(R))
tail = min(R)

cliff =
  0                if scale == 0 and L == tail
  +Inf             if scale == 0 and L != tail
  max(0, (L - tail) / scale) otherwise
```

Propiedades:

- center-independent;
- funciona con center positivo, cero o negativo;
- escala por magnitud típica local;
- signos mixtos no rompen el denominador;
- un único tail malo queda visible aunque MAD sea bajo.

### 6.4 Edge semantics for Ret/DD

- **center positivo:** no recibe tratamiento especial.
- **center cercano a cero / cero:** no existe división por center.
- **center negativo:** permitido matemáticamente; la quality posterior decidirá si el plateau es malo. No se considera robusto sólo por ser plano.
- **vecinos negativos / signos mixtos:** el cliff aumenta naturalmente cuando el tail cae bajo el nivel local; no hay singularidad por mediana cercana a cero mientras `median(abs(R))` sea material.
- **todos los valores cero:** `D_retdd=0`, `cliff=0`; quality = 0, por lo que no debería superar un plateau positivo salvo que no exista alternativa.
- **un vecino extremadamente malo:** cliff alto; MAD puede permanecer bajo.
- **varios vecinos moderadamente malos:** `D_retdd` sube aunque cliff no sea extremo.

### 6.5 Cliff as gate, not score component

Recommendation: **hard eligibility gate** con threshold policy-versioned, y no volver a incluir cliff dentro de stability score.

Razón:

- cliff expresa un límite semántico de downside local;
- `D_retdd` ya captura dispersión;
- meter cliff además como penalty/score genera doble penalización del mismo eje Ret/DD.

Puede auditarse el valor continuo de cliff, pero una vez pasado el gate no debería seguir alterando el ranking salvo como dato de diagnóstico.

## 7. Sharpe and Net Profit

### 7.1 Why CoV is not ideal for V2

`sigma / |mean|` falla semánticamente cuando:

- mean ≈ 0 → score explota;
- signos mixtos → el mean puede cancelar magnitudes y crear gran CoV artificial;
- valores negativos → el CoV es matemáticamente computable pero difícil de interpretar como estabilidad;
- un outlier mueve tanto mean como sigma;
- aunque sea scale-free, depende de mean, que no es robusto.

Wave2a no contiene valores negativos o cercanos a cero en estas métricas dentro del export analizado, pero V2 debe definir semántica general y no depender de esa casualidad.

### 7.2 Candidate replacement

Usar el mismo normalized MAD robusto para Sharpe y Net Profit:

```text
D_sharpe = MAD(Sharpe) / median(abs(Sharpe))
D_profit = MAD(NetProfit) / median(abs(NetProfit))
```

con las reglas de zero-scale definidas arriba.

Ventajas:

- una sola familia matemática para las tres métricas;
- robusta a un outlier;
- scale-free;
- tolera negativos y signos mixtos;
- fácil de explicar y replayear.

Limitación deliberada: un outlier extremo puede ser ocultado por MAD. Eso se acepta para Sharpe/Net Profit en V2; el único hard-tail guard propuesto es Ret/DD porque el Owner pidió darle mayor importancia paramétrica y porque duplicar cliff guards por cada métrica inflaría la policy sin evidencia.

## 8. Failure modes and alternatives considered

### A. Keep V1 CoV and only add Ret/DD cliff — rejected

Corrige un tail específico pero mantiene la fragilidad de CoV y el center-first ranking.

### B. Cliff only — rejected

Un neighborhood con varios valores moderadamente malos puede no presentar un cliff aislado y seguir siendo inestable.

### C. Normalized MAD only — rejected

MAD puede ignorar un único tail severo.

Wave2a example from the offline replay using Optimizer-export values:

```text
Strategy_1.8.669, neighborhood 6/30
D_retdd ≈ 0.032
cliff ≈ 0.425
median Ret/DD ≈ 23.303
min Ret/DD = 13.412
```

MAD diría "muy estable" mientras existe una caída local fuerte.

### D. Robustness DESC strict -> quality — rejected

También puede convertir la nueva stability score en una tiranía.

Counterexample:

```text
Strategy_8.10.634
top stability candidate: 9/30
  S_diag ≈ 0.9790
  median Ret/DD ≈ 9.4101

higher-quality robust candidate: 6/22
  S_diag ≈ 0.9672
  median Ret/DD ≈ 11.7347
```

Una ganancia ≈0.0118 de stability sacrificaría ≈19.8% de Ret/DD mediano. No existe base conceptual para afirmar que esa pequeña diferencia de scalar score debe dominar siempre.

### E. Weighted geometric mean as ranking authority — not recommended

Es interpretable, pero obliga a congelar weights sin necesidad y hace que pequeños cambios de weight puedan cambiar authority. Mejor dejarla como audit metric.

### F. Pure quality medians after cliff — rejected

Volvería encubiertamente a "best performance wins", sólo que usando medianas.

### G. Pareto stability layers + quality — candidate

Mantiene stability y quality separados, no necesita weights y permite que quality decida sólo entre candidates que no son claramente peores en stability.

## 9. Candidate ranking contract

Input: neighborhoods 3×3 estructuralmente completos y con required evidence válida.

### Stage 1 — structural/metric eligibility

Neighborhood ineligible si:

- falta cualquiera de las 9 CELLs;
- existe duplicate `(runs,OOS)`;
- cualquier CELL required no es `Passed=true`;
- Ret/DD, Sharpe o Net Profit missing/NaN/Inf.

### Stage 2 — cliff gate

```text
keep iff cliff_retdd <= CLIFF_MAX
```

`CLIFF_MAX` es policy parameter Owner-gated.

### Stage 3 — stability layers

Calcular `D_retdd, D_sharpe, D_profit` y asignar `pareto_layer` ascendente.

### Stage 4 — quality of plateau

Dentro de la mejor layer disponible, ordenar:

```text
1. median neighborhood Ret/DD DESC
2. median neighborhood Sharpe DESC
3. median neighborhood Net Profit DESC
```

Esto define **quality of plateau** mediante el nivel típico de todo el neighborhood, no el center.

Ret/DD va primero porque el Owner explícitamente quiere mayor importancia a esta métrica. Sharpe y Net Profit quedan secundarios.

### Stage 5 — deterministic technical tie-break

Sólo si los valores anteriores son iguales dentro de epsilon canónico:

```text
1. D_retdd ASC
2. D_sharpe ASC
3. D_profit ASC
4. runs ASC
5. OOS ASC
```

No usar center metric como tie-break.

### Output audit fields recommended

V2 aggregate pick debería poder auditar al menos:

```text
rank
runs_count
oos_percent
pareto_layer
cliff_retdd
d_retdd
d_sharpe
d_net_profit
median_retdd
median_sharpe
median_net_profit
stability_score_diag?   # optional
```

El exacto schema pertenece a SPEC posterior, no se congela aquí.

## 10. Cliff threshold sensitivity

Thresholds exploratorios solicitados: 25%, 30%, 35%, 40%.

Offline design replay sobre el export `OPTIMIZER-CANDIDATES.csv`:

```text
25% -> 14 Strategies con al menos un candidate
30% -> 15
35% -> 18
40% -> 18
```

Tomando 35% como referencia y ranking diagnóstico 50/25/25:

```text
35 -> 25: 4 Strategies pierden todos sus candidates; 1 rank1 cambia entre las restantes
35 -> 30: 3 pierden todos; 1 rank1 cambia
35 -> 40: ninguna gana candidate adicional; 2 rank1 cambian
```

Interpretación:

- el threshold importa más que pequeños cambios de weights;
- 25/30 parecen materialmente más agresivos sobre este corpus;
- 40 no amplía cobertura respecto de 35 pero sí permite algunos neighborhoods adicionales y cambia decisiones.

**Design recommendation:** llevar `35%` como **review candidate**, no frozen. La decisión final pertenece al Owner y debe verificarse nuevamente con el corpus WFM durable exacto.

## 11. Weight sensitivity

Con cliff fijo, el score diagnóstico bajo 40/30/30, 50/25/25 y 60/20/20 muestra churn limitado pero no cero.

Ejemplo a threshold 35%:

```text
40/30/30 -> 50/25/25: 2 rank1 cambian
50/25/25 -> 60/20/20: 2 rank1 cambian
40/30/30 -> 60/20/20: 4 rank1 cambian
```

Esto no justifica un optimizer de weights. Al contrario, refuerza sacar los weights de la autoridad de ranking.

## 12. Concrete wave2a examples

### 12.1 MAD hides a single bad tail

```text
Strategy_6.39.493, 7/32
D_retdd ≈ 0.0895
cliff ≈ 0.4848
median Ret/DD ≈ 19.7525
min Ret/DD ≈ 10.1772
```

El neighborhood parece compacto por MAD pero tiene tail severo.

### 12.2 Broad instability without isolated tail

```text
Strategy_3.31.576, 8/34
D_retdd ≈ 0.239
cliff ≈ 0.239
tail-gap entre peor y segundo peor ≈ 0.011 del scale local
```

No existe un único outlier dominante; varios puntos están degradados. Cliff solo no basta.

### 12.3 Stability-vs-quality tradeoff

```text
Strategy_6.40.536

candidate 9/24:
  S_diag ≈ 0.9784
  median Ret/DD ≈ 18.5207
  cliff ≈ 0.1105

candidate 7/22:
  S_diag ≈ 0.9735
  median Ret/DD ≈ 22.2366
  cliff ≈ 0.1470
```

Diferencia mínima de scalar stability pero ≈16.7% de diferencia de median Ret/DD. Una regla `robustness DESC` estricta elegiría el primero sin una justificación proporcional.

### 12.4 Near-threshold neighborhoods exist

Wave2a contiene numerosos neighborhoods alrededor de 25%, 30%, 35% y 40%; por lo tanto el threshold no es una decisión inocua y debe ser versionado/auditable.

## 13. Strategy_1.8.669 walkthrough

Evidencia owner/Optimizer:

```text
current durable rank1: runs=7, OOS=32
Optimizer export center:
  Ret/DD = 23.3026
  Sharpe = 1.33
  Net Profit = 14618.9004
worst Ret/DD in 3×3:
  runs=6, OOS=30
  Ret/DD=13.4117
center-relative downside ≈ 42.45%
```

Durable aggregate/pick reporta para el mismo CELL:

```text
ranking_metric = sharpe_ratio
ranking_metric_value = 1.35
robustness_score = 0.8595
```

Esto confirma que el valor de selección WFM puede diferir del Optimizer export.

Replay de diseño sobre el Optimizer export sugiere:

```text
current neighborhood 7/32:
  median Ret/DD ≈ 22.0546
  min Ret/DD = 13.4117
  candidate median-relative cliff ≈ 39.2%
```

Con un cliff candidate 35%, este neighborhood no pasaría.

Otros neighborhoods de la misma Strategy presentan mejor comportamiento local en el replay; por ejemplo 8/28 mostró aproximadamente:

```text
S_diag ≈ 0.9845
median Ret/DD ≈ 21.8314
cliff ≈ 12.2%
```

y el Pareto-layer replay con threshold 35% encontró candidates no dominados distintos del rank1 V1.

**Important:** esto no autoriza cambiar el rank1 hoy. El replay exacto debe usar las observaciones WFM durable, no sólo el Optimizer export.

## 14. Edge-case semantics

### missing

Required metric missing en cualquiera de las 9 CELLs -> neighborhood ineligible.

### NaN / Inf

Required metric NaN/Inf -> neighborhood ineligible. No filtrar silenciosamente el valor y continuar con 8 CELLs.

### zero denominator

Para normalized MAD / cliff:

```text
scale = median(abs(values))
scale == 0 and numerator == 0 -> 0
scale == 0 and numerator > 0 -> +Inf
```

`+Inf` hace fallar el cliff gate o deja el candidate dominado/ineligible según el componente.

### negative values

Permitidos como números finitos. Stability mide dispersión; quality conserva el signo mediante la mediana.

### mixed signs

Permitidos. La normalización por `median(abs(x))` evita cancelación del denominador.

### duplicate cell

Dos CELLs con mismo `(runs,OOS)` -> contract conflict / error, nunca last-write-wins.

El binding durable actual ya falla cerrado para duplicate cell pairs y esa semántica debe preservarse.

### incomplete 3×3

Neighborhood ineligible. No interpolar, imputar ni achicar a 8/7 CELLs.

### ties

Comparar con epsilon canónico y seguir la cadena determinística. El epsilon exacto debe quedar en SPEC/code contract; no usar tolerancias dependientes del runtime.

### input shuffle

Canonicalizar CELLs por `runs ASC, OOS ASC` antes de construir grid y usar comparadores totales. Shuffle debe ser una regresión obligatoria.

## 15. Sensitivity strategy

No ajustar threshold/weights para maximizar cuántos winners "se ven buenos".

Reportar por cada variante deliberada:

```text
- Strategies con 0 candidates
- Strategies con >=1 candidate
- rank1 churn count
- churn rate sólo entre Strategies comparables
- qué Strategies cambiaron
- razón exacta del cambio:
    cliff eligibility
    pareto layer
    median Ret/DD
    median Sharpe
    median Net Profit
    technical tie-break
- distance to threshold de cada cambio
```

### Red flags

- +/-5 pp de cliff cambia una fracción grande de rank1 sin explicar por qué.
- un tiny weight change cambia gran parte del universo.
- rank1 cambia por input shuffle.
- quality medians casi iguales pero un epsilon floating decide de forma no reproducible.
- policy favorece consistentemente plateaus peores sólo por minúsculas diferencias de scalar stability.
- varias Strategies quedan sin candidate exclusivamente por un threshold elegido mirando outcomes.
- Owner case mejora pero aparecen degradaciones conceptuales claras en otras Strategies.

## 16. Evidence required before implementation

Antes de escribir product code:

1. Replay read-only exacto usando `cells.tsv` o MetricSets WFM durable que alimentaron los aggregates, no sólo `OPTIMIZER-CANDIDATES.csv`.
2. Reproducir V1 rank1 exacto para las 10 selected Strategies a partir de esa evidencia.
3. Confirmar las 34 Strategies y clasificar qué neighborhoods son structurally/metric eligible bajo V2.
4. Generar tabla V1 vs V2 candidate para cada Strategy con componentes separados.
5. Ejecutar sensitivity determinística de cliff 25/30/35/40 y, sólo como diagnóstico, weights 40/30/30, 50/25/25, 60/20/20.
6. Probar shuffle determinism.
7. Incluir fixtures sintéticos de signs/zero/missing/NaN/Inf/duplicates/incomplete-grid.
8. Primary Technical Manager debe revisar que el cambio cabe upstream en evaluator/binding sin alterar `select_robust_run`.

## 17. Decisions already technical

Estas decisiones pueden considerarse suficientemente técnicas para la siguiente iteración de Manager:

- preservar arquitectura evaluator -> aggregate rank -> selector rank1;
- selección exclusivamente intra-strategy;
- separar stability de quality;
- reemplazar CoV como candidato V2 por normalized MAD robusto;
- cliff Ret/DD definido contra nivel local, no contra center;
- no usar cliff simultáneamente como hard gate y penalty/score;
- usar medianas del neighborhood para quality;
- no usar center metric en quality ni tie-break;
- fail closed para invalid/missing/duplicate/incomplete;
- no usar weight optimization;
- preferir Pareto stability layers sobre un scalar score como ranking authority.

## 18. Decisions requiring Owner

### O1 — Cliff threshold

Elegir el policy threshold después del replay durable exacto.

Candidate para revisión: **35%**.

No frozen.

### O2 — Confirm ranking philosophy

Aceptar o rechazar explícitamente:

```text
cliff gate
-> best Pareto stability layer
-> median Ret/DD
-> median Sharpe
-> median Net Profit
-> deterministic technical tie-break
```

Esta es una decisión semántica de producto cuantitativo, no sólo implementación.

### O3 — Treatment when every neighborhood fails cliff gate

Candidate technical behavior: Strategy queda sin acceptable neighborhood y sigue la semántica FAIL upstream existente; no rescatar automáticamente por "least bad cliff".

Requiere ratificación porque afecta funnel.

## 19. Risks / unknowns

### R1 — Optimizer-vs-WFM metric discrepancy

Para `Strategy_1.8.669`, CELL 7/32:

```text
OPTIMIZER-CANDIDATES.csv Sharpe = 1.33
durable pick ranking_metric_value = 1.35
```

El workbook wave2a documenta explícitamente que el Sharpe del pick puede ser una re-evaluación WFM distinta del valor Optimizer.

Impacto: el corpus Optimizer es excelente para shape/counterexamples, pero no es suficiente para certificar el exact rank result de V2.

### R2 — Current wave2a only has 18 Strategies with replayable V2 candidate under the simplified Optimizer-based eligibility used here

Esto no significa que las otras 16 deban fallar V2; el durable WFM evidence y las reglas/warnings actuales deben reconstruirse antes de inferir el funnel final.

### R3 — Pareto layer sizes

Algunas Strategies tienen varias alternativas en layer 1. Esto es intencional: quality decide entre candidates sin dominancia clara. Debe auditarse que las layers no se vuelvan demasiado anchas por epsilon mal elegido.

### R4 — Median lexicographic quality is intentionally not a composite utility score

Ret/DD tiene prioridad semántica. Si el Owner quiere trade-offs continuos entre Ret/DD, Sharpe y Profit, eso sería otra policy y debe discutirse explícitamente; no esconderlo en weights.

## 20. Reuse

Potentially reusable assets:

- existing deterministic grid canonicalization / duplicate-cell contract in durable WFM binding;
- wave2a `OPTIMIZER-CANDIDATES.csv`, `picks.tsv`, `aggregates.tsv`, `ROBUST-SELECTION-AUDIT.csv`;
- `matrices/build_matrices_xlsx.py` as read-only visualization helper, not policy authority.

No promover automáticamente tooling nuevo.

`REUSE = NONE_REQUIRED_FOR_IMPLEMENTATION_DESIGN` beyond the existing evidence exports and evaluator structure.

## 21. Improve / gaps

- Large `cells.tsv` could not be consumed through the current GitHub connector path in this session; exact durable replay needs a local/read-only tooling path or a smaller canonical export.
- The wave2a artifacts mix Optimizer values and WFM re-evaluated pick values without one compact joined table containing the exact 9 WFM observations per candidate neighborhood.
- Recommended evidence improvement: create a deterministic **read-only replay export** from the existing durable WFM aggregate/CELL MetricSets with one row per candidate center and the 9 exact Ret/DD/Sharpe/NetProfit observations. This is tooling/evidence, not product behavior.

## 22. Recommendation for next design iteration

Primary Technical Manager should challenge only the remaining semantic choices, not re-open frozen architecture:

1. validate the Pareto-layer ranking contract against exact durable wave2a evidence;
2. present cliff 35% vs adjacent 30/40% with exact churn explanations;
3. confirm the behavior when every candidate fails cliff;
4. if accepted, freeze Functional/Technical SPECs and only then plan implementation.

No implementation should begin from this document alone.

---

Final status:

`DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW`
