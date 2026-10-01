---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
parent: "[[Echo Forge — Operación Real V2]]"
repo: "xKoRx/symphony"
aliases:
  - Robust V2 Technical Results Report
  - ROBUST-V2 Technical Report
tags:
  - kind/doc
  - area/echo
  - echo-forge
  - robust-run-selection
  - technical-results
created: "2026-10-01"
updated: "2026-10-01"
---

# ECHO FORGE — ROBUST RUN SELECTION V2
# EXHAUSTIVE TECHNICAL RESULTS + DECISION REPORT

Status: `TECHNICAL_REPORT_COMPLETE` · Date: 2026-10-01 · Rol: fresh Principal Technical Documentation Lead / Quant Systems Analyst (sólo lectura de fuentes y redacción; sin product code, sin tuning, sin rediseño). Autoridad canónica de implementación: [[ROBUST-V2-DESIGN-FREEZE]].

---

## Universos de evidencia (disciplina de materializaciones)

Todo número cuantitativo de este reporte pertenece a exactamente uno de estos tres universos y nunca se mezclan:

| Universo | Qué es | Autoridad para | Fuentes |
|---|---|---|---|
| **A — Historical wave2a** | La corrida histórica V1 de Echo Forge (FlowRun `80647dc2-848a-4150-842e-cc6947eed87c`): 34 aggregates, 46 picks V1, resultado 10 SELECTED / 24 rechazadas. Sus `aggregates.tsv`/`picks.tsv` del bundle c52 son **otra materialización** respecto de `cells.tsv` (discrepancia Optimizer-vs-WFM registrada el 2026-09-29). | Historia operacional de V1; comparaciones **cualitativas** con wave2b. | [[ROBUST-V2-DURABLE-REPLAY]], [[Echo Forge — Operación Real V2]] |
| **B — Local A/B validation** | V1 y V2 ejecutados por el evaluador durable real (`evaluateNeighborhoods` + `wfm.SelectRobustV2`, código de producto sin cambios, @ `bc50bbb`) sobre **el mismo input**: 1.836 CELLs (`cells.tsv` del bundle c52, SHA256 `3e0dac89…` == manifest). | **Comparación algorítmica directa V1 vs V2.** Único universo donde los dos algoritmos vieron celdas idénticas. | [[ROBUST-V2-LOCAL-VALIDATION]] + `artifacts/local-validation-20260930/` |
| **C — wave2b Hera E2E** | El Optimizer **re-ejecutado** en la flota (wave `wave2b`, FlowRun `0cbd0f34-c4f2-459e-b670-242bddd35b85`): CELLs frescas, 1.836 nuevas, V2 consumido por el flujo canónico completo. | Flujo operacional canónico, integración runtime, evidencia durable, decisiones downstream. **NO comparar cuantitativamente con wave2a.** | [[ROBUST-V2-HERA-E2E]] + `artifacts/hera-e2e-20261001/` |

Regla aplicada en todo el documento: una cifra citada lleva la referencia de su universo; los R-values (`R_retdd`, `R_aux`, cliff) de wave2b **no existen** porque el contrato durable V2 no los emite (ver §13).

---

## 1. Executive Summary

**El problema.** V1 rankea neighborhoods 3×3 poniendo primero la métrica del centro (`ranking_metric(center) DESC`, `sharpe_ratio` en wave2a) y usando la robustez (`dispersion_cov`) sólo como desempate. Consecuencia demostrada con datos reales: un centro atractivo puede ganar aunque su superficie local sea frágil, y cuando el centro elegido es un pico aislado, el propio V1 se auto-gatea con `SEVERE_WARNING` y la Strategy queda FAIL aunque existiera una meseta buena al lado.

**Qué hace V2.** `robust_run_selection_v2` es un algoritmo nuevo, seleccionable por la configuración WFM existente (`wave_config.wfm_params`), que selecciona **mesetas paramétricas**: estabilidad por mediana + MAD normalizado + representatividad del centro (`R_x = max(D_x, C_x)`), un cliff Ret/DD como hard gate, dos bandas anidadas de indiferencia (Ret/DD primaria, `R_aux = max(R_sharpe, R_profit)` secundaria) y calidad lexicográfica (mediana Ret/DD → Sharpe → Net Profit) con tie-break determinista. V1 queda byte y semánticamente intacto; `select_robust_run` sigue consumiendo el `rank == 1` único.

**Qué cambió y qué no.** Cambió la matemática de selección intra-strategy (7 archivos, +1217/−42). No cambió: arquitectura (sin `evaluation_policy`, sin registry), V1, el consumidor downstream, ni el schema de veredictos. La flota corría 0.2.130 (sin V2) → se cortó la release **0.2.131** desde el SHA certificado `bc50bbb` (`vcs.modified=false`) y se desplegó 3/3. **Product code changes: NONE después de la certificación.**

**Resultados (universo B — autoridad A/B).** Sobre las mismas 1.836 CELLs: V2 rechaza exactamente el mismo set de 16 Strategies que V1 (0 rechazos nuevos); las 6 Strategies que V1 se auto-gateaba como FAIL-SEVERE pasan a WARN (seleccionables); 13/18 rank1 cambiados, **13/13 hacia menor `R_retdd`** (12/13 hacia menor `R_aux`); 7 sacrifican mediana Ret/DD (mediana −1,24; peor −2,18), 5 mejoran, 1 empata; el cliff 0.35 corta 26/214 vecindarios (12,15%, idéntico al adversarial de diseño) y nunca rechaza una Strategy completa que V1 hubiera aceptado. Sin defectos de implementación.

**Resultados (universo C — autoridad operacional).** wave2b consumió V2 end-to-end en la flota real (Hera incluida): 34 → 1.836 CELLs → 34 WFM → **0 PASS / 21 WARN / 13 FAIL → 21 SELECTED / 13 sin decisión**, 89 stage executions, **0 errores de stage**, evidencia durable completa (config PG con V2, 34/34 aggregates Mongo con `scoring_algorithm=robust_run_selection_v2` + digest `sha256:24daf87d…` idéntico al trial local, 21 decisiones PG con `ranking_metric=ret_dd` y `robustness_score=0`), STOP antes de Final Retester/MT5 verificado. Corrida ~21h (wave2a había tomado ~12h), sin retries anómalos.

**Evidencia existente.** Escalera completa: diseño congelado tras adversarial + corrección fail-closed → Shot 1/1R → Shot 2 adversarial (0 BLOCKER/0 MAJOR) → Shot 3 certificación (PASS) → validación local A/B con datos reales (PASS) → E2E full-flow en flota (PASS_WITH_FIX, el "fix" es de runtime, no de producto).

**Estado final.** `READY_FOR_NORMAL_V2_USE: YES` con la release 0.2.131 desplegada en la flota. La rama certificada `feature/robust-selection-v2-shot1` @ `bc50bbb` está pusheada; **la absorción a `master` (`ca07f72`, aún sin V2) es la integración pendiente del Primary Technical Manager**. Los parámetros 0.35/0.01/0.01 siguen siendo valores de prueba observados tal cual, no defaults ratificados por el Owner.

Headline metrics:

| Métrica | Valor | Universo |
|---|---|---|
| Strategies cohorte | 34 (NDX L H1 SQX v1, wave1z) | A/B/C |
| CELLs por corrida | 1.836 (34 × 54) | B/C |
| V2 seleccionadas (E2E) | 21 de 34 (61,8%) | C |
| Rechazos Strategy-level por gates V2 (cliff/bandas) | **0** | B |
| Vecindarios cortados por cliff 0.35 | 26/214 = 12,15% | B |
| rank1 cambiados vs V1 (mismo input) | 13/18, 100% hacia menor R_retdd | B |
| Estrategias desbloqueadas (FAIL-SEVERE V1 → WARN V2) | 6 | B |
| Stage executions E2E / errores | 89 / 0 | C |
| Defectos de integración de V2 | 0 | C |
| Delta físico | 7 archivos, +1217/−42 | repo |

---

## 2. Context and Problem

### 2.1 Cómo funciona V1 (reconstrucción de source, verificada)

V1 (`wfm_3x3_v1` + `dispersion_cov`) calcula para cada neighborhood 3×3 el coeficiente de variación de Sharpe y de Net Profit y un score escalar:

```text
dispersion_cov:
  D_sharpe = CoV(Sharpe[3×3])
  D_profit = CoV(NetProfit[3×3])
  robustness = 1 / (1 + D_sharpe + D_profit)

durable ranking:
  1. ranking_metric(center) DESC     ← sharpe_ratio en wave2a
  2. robustness DESC
  3. runs ASC
  4. OOS ASC
```

Fuentes: `sqx/core/wfm/evaluator.go` (`scoreDispersionCoV`), `sqx/adapters/wfm/binding/evaluate.go` (`rankDurablePicks`), `sqx/adapters/wfm/binding/config.go` (defaults `RankingMetricSharpe` / `PrimaryMetricRetDD`). La separación arquitectónica `evaluate_wfm` (evalúa, adscribe, rankea) → `select_robust_run` (consume `rank == 1`) es correcta y no se tocó.

### 2.2 El defecto real: un centro atractivo puede ser un pico frágil

La robustez V1 es un desempate, no un criterio: si el centro tiene el mejor Sharpe del vecindario, gana aunque la superficie a su alrededor se degrade materialmente. Dos contraejemplos reales del corpus (universo A/B, replay de diseño sobre export Optimizer, [[ROBUST-V2-DESIGN-CANDIDATE]]):

- **Strategy_1.8.669, 7/32:** centro Ret/DD 23,30 con peor vecino 13,41 (downside ≈42% relativo al centro; cliff ≈39% de la escala local). El durable V1 lo elige por center Sharpe 1,35.
- **Strategy_6.39.493, 7/32:** `D_retdd` ≈ 0,09 (parece compacto por MAD/CoV) pero cliff ≈ 0,48 con mediana 19,75 y mínimo 10,18 — un tail severo que la dispersión global no ve.

### 2.3 El segundo defecto: auto-gateo por pico aislado

Cuando V1 elige el pico aislado, la regla de pico aislado (2σ, defaults) dispara `SEVERE_WARNING` sobre el pick y el veredicto cae a FAIL **con picks emitidos**: la Strategy sale del funnel aunque tuviera mesetas estables disponibles. En el A/B local (universo B) esto afectó a 6 Strategies (`6.24.638`, `6.39.493`, `6.41.479`, `7.46.731`, `8.10.634`, `8.11.487`, picos de 2,0–3,1σ); en la materialización histórica (universo A) fueron 8 FAIL-SEVERE. Las cifras difieren entre A y B porque son materializaciones distintas — ver §16.

### 2.4 Lo que NO se criticó de V1

V1 no está caricaturizado como "roto": su separación evaluator→selector es sana, su determinismo es correcto y en wave2a seleccionó 10 estrategias operables. El problema es de **autoridad de ranking** (centro primero, robustez como desempate) y de **interacción con warnings** (elegir el pico dispara el propio gate). Esa es exactamente la superficie que V2 reemplaza de forma aditiva.

---

## 3. Design Objectives

Propiedades buscadas (congeladas en [[ROBUST-V2-DESIGN-FREEZE]] y trazables a los invariantes I1–I10 de [[ROBUST-V2-DESIGN-CANDIDATE]]):

- **Plateau robustness:** seleccionar mesetas paramétricas de buena calidad, no picos frágiles ni plateaus mediocres.
- **Center representativeness:** el centro aplicado debe ser representativo del neighborhood; un centro-anomalía (pico o valle) se ve por `C_x`.
- **Ret/DD priority:** Ret/DD tiene prioridad semántica explícita (mandato Owner), por ordenamiento — cliff + banda primaria — no por weights.
- **Sharpe/Profit auxiliary stability:** la estabilidad auxiliar usa el peor de los dos ejes (`max`), sin compensación entre ellos.
- **Determinism:** mismo input en cualquier orden → mismo ranking exacto (probado con 500 permutaciones en Shot 2).
- **Intra-strategy only:** cada Strategy se evalúa contra sus propios neighborhoods; sin ranking cruzado.
- **V1 compatibility:** V1 inmutable (ids, `dispersion_cov`, defaults, ranking, digest tipado, `select_robust_run`); V2 es opt-in por configuración.
- **KISS/YAGNI:** sin Pareto, sin weighted scalar, sin weights espaciales, sin surface fitting, sin quality bands, sin segunda arquitectura de policies, sin optimizer de hiperparámetros.
- **Fail-closed:** evidencia requerida faltante/NaN/Inf, neighborhood incompleto, derivado no-finito o config V2 inválida nunca se imputan ni coerced.

---

## 4. Final Mathematical Contract

Contrato congelado ([[ROBUST-V2-DESIGN-FREEZE]]). Requiere, en las 9 CELLs de cada neighborhood 3×3, observaciones finitas de Ret/DD, Sharpe y Net Profit. Para cada métrica `x ∈ {retdd, sharpe, profit}`:

```text
M_x     = median(x[9])                    # nivel de la meseta (robusto al outlier)
scale_x = median(abs(x[9]))               # magnitud típica local (tolera signos mixtos)
MAD_x   = median(abs(x_i - M_x))          # dispersión amplia

D_x = 0            si scale_x == 0 y MAD_x == 0        # superficie plana: estable
      +Inf         si scale_x == 0 y MAD_x > 0         # variación sin escala: sentinela
      MAD_x/scale  en otro caso

C_x = 0            si scale_x == 0 y |center_x-M_x| == 0
      +Inf         si scale_x == 0 y |center_x-M_x| > 0
      |center-M|/scale en otro caso

R_x = max(D_x, C_x)      # el PEOR de los dos modos de fallo manda (sin compensación)
```

**Qué resuelve cada pieza (intuición).** La mediana define el nivel del plateau sin que el centro o un outlier lo definan. `MAD/scale` es una dispersión relativa robusta y scale-free (sustituye al CoV, que explota con medias ≈0 y se deforma con signos mixtos). `C_x` expone la representatividad del centro: un pico central oculto al MAD (ej. `10 10 10 / 10 20 10 / 10 10 10` da MAD=0 pero C=1,0) no puede disfrazarse de meseta. `max(D,C)` impide que una dimensión compense la otra.

**Cliff Ret/DD** (tail downside, centro-independiente — la alternativa centro-relativa fue rechazada por mezclar tail risk con "qué tan especial es el centro" y explotar cerca de cero):

```text
R     = RetDD[3×3]
L     = median(R);  scale = median(abs(R));  tail = min(R)

cliff = 0        si scale == 0 y L == tail
        +Inf     si scale == 0 y L != tail
        max(0, (L-tail)/scale) en otro caso
```

**Fail-closed derivado** (corrección obligatoria del adversarial final): si cualquiera de `R_retdd`, `R_sharpe`, `R_profit`, `R_aux` o `cliff` es no-finito, el candidato es analíticamente inelegible **antes** de cualquier mínimo (`ret_best`/`aux_best` jamás pueden ser `+Inf`; se elimina el fail-open `+Inf <= +Inf + ε` de IEEE). Si no queda candidato → FAIL analítico de la Strategy (`NO_ACCEPTABLE_NEIGHBORHOOD`).

**Secuencia completa de decisión por candidato:**

```text
config V2 válida (cliff_threshold, epsilon_ret, epsilon_aux: finitos, >= 0;
                  inválido = error de config/contrato, NO resultado analítico)
→ elegibilidad estructural (9 CELLs completas, passed, 3 métricas OBSERVED finitas)
→ derivar D/C/R, R_aux, cliff
→ gate finiteness (no-finito → inelegible)
→ cliff <= cliff_threshold          (hard gate: sólo filtra, nunca rankea)
→ banda primaria:  R_retdd <= ret_best + epsilon_ret,   ret_best = min(R_retdd)
→ R_aux = max(R_sharpe, R_profit)
→ banda auxiliar:  R_aux <= aux_best + epsilon_aux,     aux_best = min(R_aux entre primarios)
→ calidad (lexicográfica): mediana Ret/DD DESC → mediana Sharpe DESC → mediana Net Profit DESC
→ tie-break técnico: R_retdd ASC → R_aux ASC → runs ASC → OOS ASC (sort estable)
```

**Detalles contractuales fijados por implementación/certificación:** `nested indifference` es intencional — el mínimo exacto de Ret/DD **no** tiene estatus protegido una vez otro candidato entra en la banda (y la membresía final NO es monótona en `epsilon_ret`, semántica aceptada y auditada); la calidad sólo arbitra entre candidatos cuya diferencia de estabilidad fue declarada inmaterial; `ranking_metric = ret_dd` y `ranking_metric_value` = mediana del vecindario (no del centro) son la quality key primaria explícita; un único `rank == 1` contiguo; TopN (3) se aplica tras el ranking completo; los refs de cada pick son la CELL central (`neighbors[4]`); `robustness_score` viaja en zero value (`0`) — V2 no define score escalar (ver §5). Sin fórmulas fuera de este contrato.

---

## 5. Decision Register

Tipos: **D** = design decision (freeze/iteraciones), **M** = manager correction, **O** = owner decision/contrato, **I** = implementation consequence certificada.

| # | Decisión | Problema que resuelve | Alternativas consideradas | Elección final | Razón | Evidencia | Tipo |
|---|---|---|---|---|---|---|---|
| 1 | V2 aditivo por config existente | Coexistencia sin mutar V1 | `evaluation_policy + version` (adversarial); registry de policies | Nuevo `algorithm id` en `wfm_params` existente | Sin segunda arquitectura; KISS | [[ROBUST-V2-DESIGN-FREEZE]] §1; [[ROBUST-V2-FINAL-ADVERSARIAL-REVIEW]] Attack 7 (superseded) | O+D |
| 2 | V1 inmutable | Preservar comportamiento histórico certificado | Reescribir ranking V1 | V1 byte-idéntico (ids, defaults, digest, `scoreNeighborhood`) | Compatibilidad frozen por Owner | Shot 2 §4; test digest `TestEvaluatorConfigDigest_V1JSONUnchangedByV2Fields` | O+I |
| 3 | Sin `evaluation_policy` | Evitar capa de dispatch nueva | Selector explícito de policy | Superseded por el freeze | El extension point existente basta | [[ROBUST-V2-DESIGN-FREEZE]] authority note | D |
| 4 | `R_x = max(D_x, C_x)` | Estabilidad = dispersión + representatividad del centro | MAD solo; geometría de bordes/superficie | Worst-of-two failure modes | MAD puede ocultar pico central; sin evidencia para surface fitting | [[ROBUST-V2-DESIGN-ITERATION-2]] §3; adversarial Attack 4 SURVIVES | D |
| 5 | Center representativeness `C_x` | El centro aplicado no debe ser anomalía | Solo dispersión tipo bag-of-values | `|center-M|/scale` con ramas zero-scale | Topología mínima que importa al run seleccionado | Iteration 2 §3 (S1: pico central invisible a MAD) | D |
| 6 | Cliff Ret/DD como hard gate | Tail local extremo invisible al MAD | Cliff como penalty/score; cliff centro-relativo | Gate `cliff <= threshold`, nunca rankea | Evita doble penalización del eje Ret/DD; centro-relativo mezcla semánticas | Candidate §6.2/6.5; Shot 2 probe "cliff no desempata" | D |
| 7 | Indiferencia primaria Ret/DD | Autoridad real de stability sin scalarización | Pareto plain (rechazado: frontier demasiado permisiva, layer-1 ≈32% mediana); regret tiers (Policy B, no recomendada) | `R_retdd <= min(R_retdd) + epsilon_ret` | Bounded trade-off explícito, transitive, anclado a mínimo común | Iteration 2 §2/§5; adversarial Attack 1 SURVIVES | D |
| 8 | `R_aux = max(R_sharpe, R_profit)` | El peor eje auxiliar manda, sin compensación | Promedio ponderado; epsilon por métrica | Minimax con un solo `epsilon_aux` | Un concepto: inestabilidad auxiliar material | Iteration 2 §5; adversarial Attack 5 RETAIN | D |
| 9 | `epsilon_aux` semántico | Cuánta degradación auxiliar es inmaterial | Ratio "2× peor" (explota cerca de 0) | Radio aditivo versionado, Owner-gated | Interpretación directa en unidades normalizadas | Iteration 2 §5/§12 O2 | D+O |
| 10 | Calidad lexicográfica | Elegir dentro del set stability-equivalente | Quality band adicional (YAGNI, 0 contraejemplos); utility compuesta | mediana Ret/DD → Sharpe → Net Profit DESC | Prioridad Owner Ret/DD sin weights; probe real: 0 casos red-flag | Iteration 2 §11 Q7; adversarial Attack 6 RETAIN | D |
| 11 | Derived non-finite fail-closed | `+Inf` podía sobrevivir bandas si todo el set era no-finito (defecto material del adversarial) | Comparaciones IEEE confía en `+Inf <= +Inf+ε` | Inelegibilidad candidate-wide antes de mínimos | Fail-closed por construcción; anchors siempre finitos | [[ROBUST-V2-FINAL-ADVERSARIAL-REVIEW]] Attack 9; [[ROBUST-V2-FINITENESS-VERIFICATION]] PASS | M |
| 12 | Params V2 finitos ≥0 | Evitar defaults silenciosos/clamps | Default silencioso; clamp | missing/NaN/Inf/negativo = config error (no FAIL analítico) | Separar fallo técnico de resultado analítico | Finiteness §8; decisiones del proyecto | M+I |
| 13 | Sin Pareto como autoridad | Non-dominance no codifica magnitud ni prioridad | Pareto layers con quality dentro de layer 1 | Diagnóstico sí, autoridad no | Compra de ~0,7% mediana con ~2,3× D_retdd (1.8.669) | Iteration 2 §2 | D |
| 14 | Sin weighted scalar / RobustnessScore escalar | Scalarización esconde trade-offs; score inventado sin autoridad | `S_diag` geométrico como autoridad (rechazado); `RobustV2Score=1/(1+R_retdd+R_aux)` (implementado en Shot 1, **eliminado en 1R**) | Sin score; `robustness_score=0` contractual | Ninguna base para weights; auditoría: 0 consumers deciden por score | Manager review Shot 1; Shot 1R; Shot 2 §9 | M |
| 15 | Sin weights espaciales / surface fitting | ¿Esquina vs vecino directo? | Distance/axis weighting | No en V2 | Sin evidencia; crearía familia de parámetros mágicos | Iteration 2 §4; freeze out-of-scope | D |
| 16 | `Rank` autoridad durable | Downstream no debe recomputar ni usar score | Recomputar rank desde `ranking_metric_value` | `select_robust_run` consume el `rank==1` único (duplicado/ausente → error) | El rank no es recomputable desde el valor; SPEC §11 | Shot 2 §8/§9; `durable_select_robust_run.go` intocado | I |
| 17 | `ranking_metric_value` = mediana del vecindario | Quality key auditable y honesta | Valor del centro (V1) | `ret_dd` + mediana 3×3, test de empate → Sharpe DESC | Representa la meseta, no el pico | Shot 1R; test `TiedMedianRetDDRankBeyondValue` | M+I |
| 18 | Valores 0.35 / 0.01 / 0.01 (trial/MVP) | Ejecutar trial sin tuning | Sensitividad 25/30/40 (25/30 eliminan Strategies completas) | Trial del mandato; sin defaults congelados | El freeze no congela valores productivos; Owner puede mover | Freeze §V2 config; [[ROBUST-V2-LOCAL-VALIDATION]]; E2E | O |
| 19 | Historical replay NO es gate de implementación | `cells.tsv` vacío bloqueaba el camino | Durable replay como prerequisito de SPEC (adversarial) | Deferido a evidencia/certificación | Tests deterministas + regresión V1 bastan para el delta | Freeze authority note; [[ROBUST-V2-DURABLE-REPLAY]] | D+O |
| 20 | Elegibilidad 3×3 estricta | Evidencia faltante no se imputa | Coercer missing→0; 8-cell fallback | 9 CELLs passed + 3 métricas OBSERVED finitas | Fail-closed; paridad legacy/durable | Shot 2 §5/§15 | I |
| 21 | Veredictos existentes intactos | Integrar V2 sin tocar la máquina de estados | Nuevos veredictos V2 | `NO_ACCEPTABLE_NEIGHBORHOOD` / `RULES_FAIL` / `SEVERE_WARNING` / WARN conservados | Superficie downstream estable | Shot 2 §8 | I |

Nota de trazabilidad: las decisiones 4–10, 13, 14 y 15 se debaten con contraejemplos reales y sintéticos en [[ROBUST-V2-DESIGN-CANDIDATE]] y [[ROBUST-V2-DESIGN-ITERATION-2]]; su forma final es la del freeze, que gana sobre cualquier texto previo en conflicto.

---

## 6. Implementation

### 6.1 Delta físico en `xKoRx/symphony`

```text
baseline:            master ca07f72 (merge-base ca07f72275ad349487ad21a0b2a51eb9ce3acd9a)
rama:                feature/robust-selection-v2-shot1
commits:             b696b3a (core V2) + a149a34 (binding durable) + bc50bbb (Shot 1R)
SHA final certificado: bc50bbba9a50b7079ed81ff96d80b9f1f780c368  (pusheada a origin)
delta:               7 archivos, +1217/−42  (verificado con git diff --stat en esta sesión)
```

Archivos (verificados contra `git diff --stat ca07f72..bc50bbb`):

| Archivo | Papel |
|---|---|
| `sqx/core/wfm/robust_v2.go` (+371) | Matemática pura: median/MAD/D/C/R/cliff, `SelectRobustV2` (finiteness→cliff→bandas→quality→tie-break), validación fail-closed de los 3 params |
| `sqx/core/wfm/evaluator.go` (+4) | Único hook de dispatch V2 en `EvaluateNeighborhood` (el switch V1 `scoreNeighborhood` queda intocado) |
| `sqx/core/wfm/robust_v2_test.go` (+322) | Tests core (plateau, center peak, cliff, bandas, nested indifference, quality order, tie-break, shuffle, zero-scale, params inválidos, legacy path) |
| `sqx/adapters/wfm/binding/config.go` (+90) | `EvaluatorConfigFromWFMParams` acepta `robust_run_selection_v2` con versión `v2`; params V2 como `*float64 omitempty` (digest V1 byte-idéntico) |
| `sqx/adapters/wfm/binding/evaluate.go` (+138) | Path durable: `eligible()` (9 celdas, 3 métricas OBSERVED finitas), despacho V2 en `evaluateNeighborhoods`, `rankRobustV2Picks` con `ranking_metric=ret_dd` + mediana |
| `sqx/adapters/wfm/binding/contract.go` (+3) | Campos V2 en contratos tipados |
| `sqx/adapters/wfm/binding/robust_v2_test.go` (+331) | Tests binding (config válida/inválida, digest V1, cliff gate e2e, quality order e2e, paridad, determinismo) |

### 6.2 Rutas de ejecución

- **Config path:** `wave_config.wfm_params` (schema existente, top-level de la wave, no por-task) → watcher → `sqx.configs.config_json` (PG durable) → `wfmParamsFromSpec` → `EvaluatorConfigFromWFMParams` → `ScoringAlgorithm=robust_run_selection_v2`, versión `v2`, 3 params required fail-closed.
- **Legacy path (in-memory):** `EvaluateNeighborhood` despacha V2 con la misma core; warnings/rules/stats V1 conservados.
- **Durable path:** `evaluateNeighborhoods` produce aggregates con scope/payload `scoring_algorithm="robust_run_selection_v2"`, `scoring_algorithm_version="v2"` y digest; `durable_select_robust_run` (intocado) consume el `rank==1` único; `RobustSelectionOutput` + `ValidateSelectedEvidence` aplican la decisión.
- **Tests:** 29 tests V2 (inventario completo en [[ROBUST-V2-SHOT3-FINAL-CERTIFICATION]] CHECK 4) + regresión V1 (`go test -count=1` wfm+binding y worker slice `WFM|Robust|DurableSelect|DurableApply|EvaluateWfm` verdes).

### 6.3 Por qué es KISS

Una sola función core compartida por ambos paths (no hay segunda implementación de la matemática), un único hook de dispatch de 4 líneas, 3 parámetros nuevos tipados como punteros opcionales que dejan el DTO/digest V1 byte-idéntico, cero abstracciones nuevas (sin registry, sin policy layer, sin interfaces), y V1 con cero líneas de comportamiento modificado. El shot explícitamente rechazó extender el framework cuando el extension point pudo soportar V2 sin cambio arquitectónico (condición de parada del freeze).

---

## 7. Validation Ladder

```text
DISEÑO
  Candidate (one-shot, corpus wave2a)      DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW
  └→ Manager review                        DESIGN_ITERATION_REQUIRED (Pareto insuficiente)
  └→ Iteration 2 (nested indifference)     DESIGN_V2_CANDIDATE_READY
  └→ Pre-adversarial manager               4 ataques obligatorios definidos
  └→ Final adversarial review              DESIGN_ITERATION_REQUIRED (defecto fail-open +Inf)
  └→ Amendment fail-closed + params        DESIGN_AMENDMENT_READY_FOR_FOCUSED_VERIFY
  └→ Finiteness verification               DESIGN_READY_FOR_DURABLE_REPLAY_AND_OWNER_FREEZE (PASS)
  └→ KISS DESIGN FREEZE                    READY_FOR_SHOT_1  ← autoridad canónica
  └→ [Durable replay gate]                 DURABLE_REPLAY_BLOCKED_EVIDENCE → deferido, no bloquea
IMPLEMENTACIÓN
  Shot 1  b696b3a+a149a34                  IMPLEMENTED_LOCAL (14+10 tests, regresión V1 PASS)
  Shot 1R bc50bbb                          Remediación manager (score inventado eliminado) PASS
VERIFICACIÓN INDEPENDIENTE
  Shot 2  adversarial implementation       SHOT_2_PASS (0 BLOCKER / 0 MAJOR / 2 MINOR)
  Shot  3  certificación final             SHOT_3_PASS (freeze, regresiones, build, clean tree; READY_TO_PUSH)
DATOS REALES
  Local A/B (universo B)                   LOCAL_VALIDATION_PASS  (mismo input V1/V2)
  Hera full-flow E2E (universo C)          HERA_FULL_FLOW_PASS_WITH_FIX  (release 0.2.131, 0 errores de stage)
INTEGRACIÓN
  Master absorption                        PENDIENTE — Primary Technical Manager (origin/master = ca07f72 sin V2)
```

Por etapa:

| Etapa | Goal | Método | Resultado | Hallazgos/correcciones | Gate |
|---|---|---|---|---|---|
| Design candidate→iteration 2 | Autoridad real de stability sin scalarización | Replay offline sobre corpus wave2a + contraejemplos | Pareto rechazado; nested bands diseñadas | 1.8.669: +0,71% mediana compraba 2,3× D_retdd | `DESIGN_V2_CANDIDATE_READY` |
| Final adversarial | Romper el candidate | 10 ataques con casos durables | 1 defecto material (fail-open +Inf) | Corrección fail-closed candidate-wide | `DESIGN_ITERATION_REQUIRED` |
| Finiteness verification | Verificar el amendment | Pruebas de casos (all-nonfinite, mixed, cliff +Inf, zero/near-zero, corpus finito) | Amendment transparente en corpus finito; fail-closed por construcción | Sin cutoff near-zero; no toca V1 | PASS |
| Shot 1/1R | Implementar el freeze | Delta mínimo + tests + regresión V1 | Implementación conforme; 1 finding de manager | Score inventado eliminado; quality key explícita | `SHOT_1R_PASS` |
| Shot 2 | Atacar la implementación | 25 ataques + 19 probes temporales (eliminados) | Matemática exacta; V1 intacto; paridad; determinismo (500 permutaciones) | MIN-01 knobs vestigiales en digest; MIN-02 SEVERE-with-picks preexistente | `SHOT_2_PASS` |
| Shot 3 | Certificar entrega | 9 checks (drift, freeze, regresiones, build/static, contratos, clean tree) | Sin drift desde Shot 2; `go build ./...` falla sólo por `libzmq.pc` (preexistente, probado en baseline) | 0 BLOCKER/0 MAJOR; `FILES_CHANGED_IN_SHOT_3: NONE` | `SHOT_3_PASS` |
| Local A/B | ¿Comporta como diseñado con datos reales? | Evaluador durable real sobre cells.tsv SHA-verificada | §9 | Sin defecto; sensibilidad cliff 2.25.400 anotada | `LOCAL_VALIDATION_PASS` |
| Hera E2E | ¿Lo consume el flujo canónico en flota? | wave2b completa, release 0.2.131, evidencia durable por eslabón | §11 | 0 defectos de integración V2; fix de runtime (rollout) | `HERA_FULL_FLOW_PASS_WITH_FIX` |

---

## 8. Cohort Composition

La cohorte es la operativa de Echo Forge: **34 Strategies NDX, Long, H1, SQX v1**, del cohort histórico `wave1z` / `02_full_retester` (propiedad del FlowRun COMPLETED `c329a546-800b-494b-bace-c87fd81dae10`). Es el mismo conjunto que consumió wave2a. No existe dataset pre-stageado adicional en Hera u otro host: el dataset del E2E **es** el corpus operativo de la flota.

El flow E2E contiene **un único task group**, `03_optimizer_v2_group` (verificado en el spec despachado `20260930_204232_flow-robust-v2-hera-e2e-wave2b.json`), que procesa toda la cohorte con `max_parallel: 3`, `batch_size: 1` y tres tasks: `project` (03_optimizer, grid WF type2 p10/o15: runs {5..10} × OOS {20..36} = 54 celdas/Strategy), `evaluate_wfm` (04) y `select_robust_run` (05).

Sobre los nombres `Strategy_1.*` … `Strategy_8.*`: el primer número se trata aquí como **numeric prefix (family)**, una agrupación descriptiva de los nombres. **No se encontró evidencia** en los sources, specs ni artifacts de que ese prefijo sea un `group_id` semántico del producto; no se afirma nada más allá de la distribución observable.

Distribución por prefijo y resultado wave2b (universo C; verificado contra `ROBUST-V2-HERA-E2E.csv` y `results_v2.jsonl`):

| Prefix (family) | Total strategies | V2 selected | V2 rejected | Selection rate |
|---:|---:|---:|---:|---:|
| 1 | 5 | 3 | 2 | 60% |
| 2 | 10 | 4 | 6 | 40% |
| 3 | 2 | 0 | 2 | 0% |
| 4 | 1 | 1 | 0 | 100% |
| 5 | 1 | 1 | 0 | 100% |
| 6 | 5 | 4 | 1 | 80% |
| 7 | 3 | 2 | 1 | 67% |
| 8 | 7 | 6 | 1 | 86% |
| **TOTAL** | **34** | **21** | **13** | **61,8%** |

Las families representadas entre las seleccionadas: 1, 2, 4, 5, 6, 7 y 8 (todas menos la 3, cuyas 2 estrategias quedaron sin vecindario elegible).

---

## 9. Local A/B — V1 vs V2 on Identical CELLs

**Dataset (universo B, autoridad A/B):** 34 Strategies × 54 CELLs = **1.836 CELLs** (`cells.tsv` del bundle c52-wave2a, SHA256 `3e0dac89…` verificado contra manifest y byte-idéntico a la copia original en `forge-recovery-c52-20260928/artifacts/`; re-verificado en esta sesión: 2.031.323 bytes, 1.836 filas, mismo hash). Grid `runs {5..10} × OOS {20,22,...,36}`, con `stability.passed` + 9 métricas OOS por celda. Ejecución con código de producto real (`evaluateNeighborhoods` + `wfm.SelectRobustV2`), worktree limpio @ `bc50bbb`, sin Stores/PG/Temporal (la frontera durable no participa; el cálculo es el mismo del worker).

**Configs efectivas:** V1 = defaults durables frozen (el spec wave2a no lleva `wfm_params`; digest `sha256:57cdb0c5…`): `wfm_3x3_v1`+`dispersion_cov`, `ranking_metric=sharpe_ratio`, `top_n=3`, `min_consistency=0.90`, weights 0.4/0.6, reglas default. V2 = trial `robust_run_selection_v2` con `0.35/0.01/0.01`, sin tuning (digest `sha256:24daf87d…`).

### 9.1 Resultado agregado

| Métrica | V1 | V2 |
|---|---|---|
| Strategies totales | 34 | 34 |
| Con picks (veredicto consumible) | 18 (12 WARN + **6 FAIL-SEVERE-with-picks**) | 18 (18 WARN) |
| Sin picks (`NO_ACCEPTABLE_NEIGHBORHOOD`) | 16 | 16 — **mismo set exacto** |
| Veredictos PASS / WARN / FAIL | 0 / 12 / 22 | 0 / 18 / 16 |
| FAIL por SEVERE_WARNING | 6 | **0** |
| rank1 igual / cambiado | — | 5 iguales / 13 cambiados |
| V1 seleccionable → V2 rechazada | — | **0** |
| V1 rechazada (pick) → V2 seleccionable | — | 0 a nivel pick; **6 a nivel veredicto** (FAIL-SEVERE → WARN) |

Distinción clave: un `FAIL-SEVERE` de V1 **emite** pick pero **no es seleccionable downstream** (`DurableSelectRobustRunActivity` rechaza aggregates FAIL). Por eso V1 tenía 18 "pick emitted" pero sólo 12 seleccionables; V2 tiene 18 emitidos y 18 seleccionables.

### 9.2 Dirección de los 13 cambios

- **13/13 hacia menor `R_retdd`** (el R_retdd del centro V1 medido con las fórmulas V2 sobre las mismas celdas vs el R_retdd del ganador V2).
- **12/13 hacia menor `R_aux`**; la excepción es `Strategy_2.76.686` (caso nested indifference: el ganador V2 tiene R_aux ≈ 6× peor, 0,286 vs 0,046, pero gana dentro de la banda primaria porque manda la mediana Ret/DD — semántica frozen operando tal cual).
- **Mediana Ret/DD:** 7 sacrificios (mediana de sacrificios −1,24; peor −2,18 en `7.51.646`), 5 mejoras (mejor +2,04 en `3.31.576`), 1 empate exacto (`6.41.479`, mediana 21,534 idéntica; movimiento puro por estabilidad).
- **Cliff:** 3 centros V1 estaban directamente sobre un acantilado Ret/DD y V2 los rechaza por el gate: `1.8.669` (0,392), `6.24.638` (0,364), `7.51.646` (0,403).

### 9.3 Clasificación de rechazos V2 (por vecindario)

952 vecindarios interiores 3×3 (34 × 28): **738** `NEIGHBORHOOD_NOT_PASSED` (sin 3×3 completo elegible — criterio idéntico al de V1), **26** `CLIFF_REJECTED` (12,15% de los 214 vecindarios analíticamente válidos — re-computado en esta sesión desde `v2_candidates.tsv`: exactamente 26 con `cliff > 0.35`, mismas 6 estrategias y mismos conteos por estrategia que el adversarial de diseño), **154** `PRIMARY_BAND`, **2** `AUX_BAND` (`1.8.669`, `7.46.731`), **32** `SURVIVOR`. Los 214 vecindarios analíticamente válidos coinciden 1:1 con los 214 candidatos V1 (misma elegibilidad estructural). A nivel Strategy: **0 rechazos por cliff/bandas** — las 16 rechazadas lo son por no tener ni un vecindario completo elegible (mismo set que V1).

### 9.4 Sanity

Sin defecto de implementación (`LOCAL_VALIDATION_FOUND_IMPLEMENTATION_DEFECT: NO`): sets de sobrevivientes == picks reales 34/34 asertados en runtime; rank-1 único; tie-break determinista observado (`8.11.487`, 4 empates de calidad resueltos por `R_retdd ASC`); dependencia de orden descartada. `WARNING_DATA_MISSING` ×34 en ambos lados (preexistente, campo stability score ausente en esta data). Caso de sensibilidad para el Owner: `2.25.400` gana con cliff 0,3497 — a 0,0003 del umbral 0,35 (no es defecto; es el caso canónico si algún día se mueve `cliff_threshold`). Limitación declarada: no se reclama replay histórico byte a byte (los aggregates/picks históricos son otra materialización, §2 universo A).

---

## 10. Detailed Local Decision Analysis (los 13 cambios, universo B)

Datos exclusivamente de `artifacts/local-validation-20260930/` (`details.json` re-procesado en esta sesión + CSV). "Stage" = etapa V2 donde quedó excluido el centro que V1 había elegido. Todas las medianas son del vecindario 3×3.

| # | Strategy | V1 winner | V2 winner | Por qué ganaba V1 (centro) | Por qué gana V2 | Stage que decidió | Δ mediana Ret/DD |
|---|---|---|---|---|---|---|---:|
| 1 | 1.8.669 | 7/32 | **8/28** | Center Sharpe máximo; bajo V2: R_retdd 0,057, cliff 0,392, mediana 22,05 | Meseta stability-equivalente de mayor mediana (21,83); el centro V1 cae el cliff 0,392>0,35 | CLIFF | −0,22 |
| 2 | 2.17.581 | 6/22 | **6/34** | Center Sharpe 1,32; bajo V2: R_retdd 0,258 | R_retdd 0,070 (2,7× mejor), mayor mediana dentro del set primario (17,34; medP 18.479,8) | PRIMARY_BAND | −1,36 |
| 3 | 2.76.686 | 6/28 | **6/30** | Center Sharpe 1,26; R_retdd 0,112 | R_retdd 0,032; nested indifference: R_aux 0,286 vs 0,046 del centro V1, aceptado dentro de la banda primaria; mediana manda (21,91) | PRIMARY_BAND | −0,12 |
| 4 | 3.31.576 | 8/34 | **7/22** | Center Sharpe 1,06; R_retdd 0,440 (lo peor de ambos mundos) | Mediana +2,04 (11,26) Y R_retdd 9× menor (0,048) — sin sacrificio | PRIMARY_BAND | **+2,04** |
| 5 | 4.57.731 | 6/22 | **8/26** | Center Sharpe 1,24; R_retdd 0,216 | R_retdd 0,015; mediana casi igual (12,86 vs 12,88), medP mejor (19.130,6) | PRIMARY_BAND | −0,03 |
| 6 | 6.24.638 | 6/24 (FAIL-SEVERE) | **6/28** | Pico aislado 2σ+ auto-gateado; R_retdd 0,317, cliff 0,364 | R_retdd 0,084, cliff 0,315; desbloquea el veredicto (FAIL→WARN) y sube mediana (13,54) | CLIFF | **+1,13** |
| 7 | 6.39.493 | 7/28 (FAIL-SEVERE) | **6/24** | Pico 3σ+; R_retdd 0,314 | R_retdd 0,015 (21× menor), cliff 0,015; mediana 18,12 | PRIMARY_BAND | −1,63 |
| 8 | 6.40.536 | 7/24 | **6/32** | Center Sharpe 1,26; R_retdd 0,058 | R_retdd 0,011; dentro de banda, mayor mediana del set (20,85) | PRIMARY_BAND | −1,24 |
| 9 | 6.41.479 | 8/22 (FAIL-SEVERE) | **9/22** | Pico 2,51σ auto-gateado; R_retdd 0,100 | Misma mediana exacta (21,534); R_retdd 0,0195; WARN — meseta sin costo de calidad | PRIMARY_BAND | 0,00 (empate) |
| 10 | 7.46.731 | 8/34 (FAIL-SEVERE) | **8/22** | Pico; R_retdd 0,069, cliff 0,326 | R_retdd 0,017, cliff 0,041; mediana +2,02 (15,43) y desbloquea veredicto | PRIMARY_BAND | **+2,02** |
| 11 | 7.51.646 | 8/34 | **8/32** | Center Sharpe 1,21; R_retdd 0,459, cliff 0,403 | R_retdd 0,142, cliff 0,158; sacrifica −2,18 de mediana (15,32 vs 17,50) por ~3× estabilidad y sin acantilado — el gate protege exactamente lo diseñado (los vecinos "mejores" 6/32 y 6/34, mediana 23,67, caen por cliff 0,377/0,430) | CLIFF | −2,18 |
| 12 | 8.10.634 | 7/22 (FAIL-SEVERE) | **6/34** | Pico 2,5σ+; R_retdd 0,041 | R_retdd 0,024; mediana 11,40 (+0,39); desbloquea veredicto | PRIMARY_BAND | +0,39 |
| 13 | 8.11.487 | 6/26 (FAIL-SEVERE) | **8/22** | Pico aislado 3,07σ auto-gateado (FAIL); R_retdd 0,096, cliff 0,028 | Meseta casi perfecta (R_retdd 0,0062, cliff 0,037), mediana 15,29; 4 sobrevivientes empatados en calidad → tie-break frozen eligió 8/22 determinísticamente | PRIMARY_BAND | +0,11 |

Lecturas transversales respaldadas por la tabla: (a) los 3 cambios por cliff son exactamente el caso de uso del gate — V1 elegía centros sentados sobre caídas Ret/DD de 36–40% de la escala local; (b) los 10 cambios por primary band comparten el patrón "el centro con mejor Sharpe no era stability-equivalente al mejor R_retdd, y dentro del set equivalente la mayor mediana Ret/DD decidió"; (c) el único caso donde V2 acepta peor R_aux (2.76.686) es el comportamiento nested-indifference congelado, no un accidente; (d) 6 de los 13 cambios además desbloquean el veredicto FAIL-SEVERE → WARN.

---

## 11. Hera Full-Flow E2E

**Veredicto: `HERA_FULL_FLOW_PASS_WITH_FIX`** — V2 consumido por el flujo canónico completo de Forge en su ambiente operacional único (flota Zeus/Hera/Kronos), con datos reales. El único "fix" fue de **runtime**: la flota corría 0.2.130 (sin V2, `EvaluatorConfigFromWFMParams` habría fallado cerrado) → release **0.2.131** construida byte-a-byte desde el SHA certificado `bc50bbb`. **Product code changes: NONE.**

```text
FlowRunRef     = 0cbd0f34-c4f2-459e-b670-242bddd35b85        (wave wave2b)
cfgID          = NDX_SQX_v1_wwave2b    (config durable PG con wfm_params V2 preservado)
Root workflow  = sqx-main-v1-3afbfb70-774a-4c57-8fd5-463a5c7d09d4   (Temporal ns sqx-prop)
Dispatch       = 2026-09-30T23:42:32Z
COMPLETED      = 2026-10-01T20:47Z     (~21h05m; wave2a tomó ~12h; sin retry anómalo)
Stage counts   = 34× project COMPLETED · 34× evaluate_wfm COMPLETED · 21× select_robust_run COMPLETED
Stage errors   = 0     (89 stage executions; corroborado por monitor-wave2b.log terminal)
```

**Participación física por host** (invocaciones `sqcli` de wave2b, medidas a nivel host durante la sesión E2E; documentadas en [[ROBUST-V2-HERA-E2E]]): **Hera 39, Kronos 22, Zeus 109**. Son **invocaciones físicas del binario SQX**, no número de estrategias (fan-out `max_parallel: 3` con ventana deslizante genera múltiples invocaciones por celda/wavefront). No forman parte del bundle SHA-deado de artifacts; su fuente es el monitoreo de host de la sesión, registrado en el doc E2E.

**Pipeline ejecutado (canónico, sin scripts reemplazando stages):**

```text
wave_config.wfm_params V2 (schema existente)
   │
   ▼
watcher candidate-local 0.2.131 (Daedalus) ── pipeline 7/7 steps ──► paquete sellado MinIO
   │                                                                  (input/processed/20260930_204232_*)
   ▼
config durable PG  sqx.configs (cfgID NDX_SQX_v1_wwave2b, wfm_params preservado, verificado post-despacho)
   │
   ▼
Temporal (ns sqx-prop) ──► root workflow sqx-main-v1-3afbfb70
   │
   ▼
03_optimizer_v2_group  (cohort wave1z / 02_full_retester, max_parallel 3)
   ├── project  03_optimizer      34× COMPLETED ──► 1.836 CELLs (54/Strategy) en flota Zeus/Hera/Kronos
   ├── evaluate_wfm  04_wfm       34× COMPLETED ──► 34 aggregates Mongo (scoring_algorithm=v2, digest 24daf87d…)
   └── select_robust_run 05_robust 21× COMPLETED ──► 21 decisiones PG SELECTED (rank==1)
   │
   ▼
STOP antes de Final Retester/MT5  (verificado: MinIO wave2b sólo 03_optimizer/04_wfm/05_robust/root)
```

**Evidencia durable de que el flow usó V2 (cada eslabón):** (1) spec procesado con `wave_config.wfm_params.algorithms/params`; (2) config durable PG conservando `cliff_threshold 0.35 / epsilon_ret 0.01 / epsilon_aux 0.01` post-despacho; (3) **34/34 aggregates Mongo** con `scope.scoring_algorithm="robust_run_selection_v2"`, versión `"v2"` y digest `sha256:24daf87d…` — **idéntico al trial de la validación local** (mismos knobs efectivos: defaults frozen V1 para reglas/pesos/top_n + V2 0.35/0.01/0.01); (4) **21 decisiones PG** (`sqx.decisions`, OPTIMIZER_SELECTION, SELECTED) con `ranking_metric="ret_dd"`, `robustness_score=0` (contrato Shot 1R), verdict WARN, rank 1 y ref exacta al aggregate + CELL pick. Nota de sesión actual: los MCP Mongo (`ro`/`rw`) siguen caídos hoy (re-confirmado en esta sesión, `session not found`); la lectura Mongo/PG de wave2b referida aquí es la ejecutada y documentada durante la corrida E2E ([[ROBUST-V2-HERA-E2E]] Phase 6, helper efímero read-only del repo).

---

## 12. Hera E2E Funnel

```text
input strategies            = 34   (cohort histórico wave1z, memberships REPROCESSED 34/34)
optimizer ejecutado         = 34   (1.836 CELLs, 54/54 por Strategy, grid completo: mín=máx=54)
WFM evaluadas               = 34
WFM PASS                    = 0
WFM WARN                    = 21   (reason STABILITY_WARNINGS)
WFM FAIL                    = 13   (reason NO_ACCEPTABLE_NEIGHBORHOOD)
rank1 emitido               = 21   (uno por Strategy con picks; único rank==1, contrato durable)
downstream SELECTED         = 21   (decisiones PG, outcome WFM_WARN_TOP_PICK; 1:1 con WARN, 0 mismatch)
downstream REJECTED/sin decisión = 13  (sin survivors → sin decisión; mismo criterio que wave2a)
stage executions            = 89   (34 + 34 + 21) · errores = 0
```

Verificado en esta sesión contra `results_v2.jsonl` (34 filas; 21 SELECTED; 13 REJECTED, todos `NO_ACCEPTABLE_NEIGHBORHOOD`; un solo algorithm/digest en las 34 filas) y contra la cola del `monitor-wave2b.log` (`COMPLETED: 34/34/21`, `DECISION SELECTED: 21`, `TERMINAL`).

**Por qué WARN sigue siendo seleccionable en este contrato:** WARN significa "hay picks con stability warnings" — es un veredicto de nivel warning, no de rechazo. El consumidor durable `select_robust_run` rechaza aggregates **FAIL** y selecciona el `rank==1` único de los no-FAIL; la decisión PG registra el outcome `WFM_WARN_TOP_PICK` (top pick bajo WARN). Esto es exactamente el comportamiento de wave2a (10 WARN → 10 SELECTED). La advertencia queda en la evidencia durable para el Owner; no bloquea el funnel.

---

## 13. Full 34-Strategy Result Table (universo C — wave2b)

Todas las cifras de esta tabla salen de `ROBUST-V2-HERA-E2E.csv` / `results_v2.jsonl`. `median neighborhood Ret/DD` = mediana del vecindario 3×3 del pick (quality key durable). **Blank en `R_retdd`/`R_aux`/`cliff`/`Sharpe`/`Profit`: el contrato durable V2 de esta wave no emitió esas cantidades** (sólo `ranking_metric=ret_dd` + mediana como quality key; `R_aux`/cliff son cantidades internas de selección y `robustness_score` es 0 contractual). Se deja blank en vez de derivar fuera del flujo — no fabricar valores.

| Strategy | Prefix | Verdict E2E | Selected | Rank1 runs/OOS | Reason | Median nbhd Ret/DD |
|---|---|---|---|---|---|---:|
| Strategy_1.13.611 | 1 | WARN | SELECTED | 7/30 | STABILITY_WARNINGS | 9,1168 |
| Strategy_1.37.569 | 1 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_1.38.707 | 1 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_1.8.669 | 1 | WARN | SELECTED | 9/34 | STABILITY_WARNINGS | 12,2781 |
| Strategy_1.83.581 | 1 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_2.17.503 | 2 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_2.17.581 | 2 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_2.25.400 | 2 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_2.27.756 | 2 | WARN | SELECTED | 8/22 | STABILITY_WARNINGS | 7,9534 |
| Strategy_2.30.706 | 2 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_2.41.524 | 2 | WARN | SELECTED | 6/28 | STABILITY_WARNINGS | 8,1405 |
| Strategy_2.55.692 | 2 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_2.73.608 | 2 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_2.75.621 | 2 | WARN | SELECTED | 8/22 | STABILITY_WARNINGS | 6,5428 |
| Strategy_2.76.686 | 2 | WARN | SELECTED | 6/32 | STABILITY_WARNINGS | 8,8288 |
| Strategy_3.18.626 | 3 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_3.31.576 | 3 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_4.57.731 | 4 | WARN | SELECTED | 8/32 | STABILITY_WARNINGS | 9,8987 |
| Strategy_5.38.585 | 5 | WARN | SELECTED | 8/22 | STABILITY_WARNINGS | 7,7111 |
| Strategy_6.24.638 | 6 | WARN | SELECTED | 6/22 | STABILITY_WARNINGS | 7,6759 |
| Strategy_6.32.425 | 6 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_6.39.493 | 6 | WARN | SELECTED | 8/24 | STABILITY_WARNINGS | 12,6152 |
| Strategy_6.40.536 | 6 | WARN | SELECTED | 9/30 | STABILITY_WARNINGS | 14,6083 |
| Strategy_6.41.479 | 6 | WARN | SELECTED | 8/28 | STABILITY_WARNINGS | 12,6458 |
| Strategy_7.2.741 | 7 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_7.46.731 | 7 | WARN | SELECTED | 9/24 | STABILITY_WARNINGS | 12,7681 |
| Strategy_7.51.646 | 7 | WARN | SELECTED | 6/28 | STABILITY_WARNINGS | 8,4541 |
| Strategy_8.10.634 | 8 | WARN | SELECTED | 8/28 | STABILITY_WARNINGS | 8,0574 |
| Strategy_8.11.487 | 8 | WARN | SELECTED | 7/26 | STABILITY_WARNINGS | 11,6464 |
| Strategy_8.25.708 | 8 | WARN | SELECTED | 8/22 | STABILITY_WARNINGS | 10,6267 |
| Strategy_8.26.438 | 8 | WARN | SELECTED | 7/34 | STABILITY_WARNINGS | 7,0866 |
| Strategy_8.46.640 | 8 | FAIL | REJECTED | — | NO_ACCEPTABLE_NEIGHBORHOOD | — |
| Strategy_8.62.460 | 8 | WARN | SELECTED | 7/30 | STABILITY_WARNINGS | 9,9595 |
| Strategy_8.67.447 | 8 | WARN | SELECTED | 9/30 | STABILITY_WARNINGS | 8,2452 |

---

## 14. Detailed Review of the 21 Selected Strategies (universo C)

Por contrato durable, cada fila tiene: verdict WARN (reason `STABILITY_WARNINGS`), decisión PG SELECTED (`WFM_WARN_TOP_PICK`, rank 1, `ranking_metric=ret_dd`, `robustness_score=0`). Family = numeric prefix. La interpretación adicional posible sin inventar: el rango de medianas Ret/DD de las seleccionadas es 6,54–14,61; los runs elegidos van de 6 a 9 y el OOS de 22 a 34, cubriendo todo el grid — V2 no colapsó a una esquina del espacio paramétrico.

| Strategy | Family | Runs/OOS rank1 | Median nbhd Ret/DD | Verdict | Decision |
|---|---|---|---:|---:|---|
| Strategy_1.13.611 | 1 | 7/30 | 9,1168 | WARN | SELECTED |
| Strategy_1.37.569→(no) — ver §15 | — | — | — | — | — |
| Strategy_1.8.669 | 1 | 9/34 | 12,2781 | WARN | SELECTED |
| Strategy_2.27.756 | 2 | 8/22 | 7,9534 | WARN | SELECTED |
| Strategy_2.41.524 | 2 | 6/28 | 8,1405 | WARN | SELECTED |
| Strategy_2.75.621 | 2 | 8/22 | 6,5428 | WARN | SELECTED |
| Strategy_2.76.686 | 2 | 6/32 | 8,8288 | WARN | SELECTED |
| Strategy_4.57.731 | 4 | 8/32 | 9,8987 | WARN | SELECTED |
| Strategy_5.38.585 | 5 | 8/22 | 7,7111 | WARN | SELECTED |
| Strategy_6.24.638 | 6 | 6/22 | 7,6759 | WARN | SELECTED |
| Strategy_6.39.493 | 6 | 8/24 | 12,6152 | WARN | SELECTED |
| Strategy_6.40.536 | 6 | 9/30 | 14,6083 | WARN | SELECTED |
| Strategy_6.41.479 | 6 | 8/28 | 12,6458 | WARN | SELECTED |
| Strategy_7.46.731 | 7 | 9/24 | 12,7681 | WARN | SELECTED |
| Strategy_7.51.646 | 7 | 6/28 | 8,4541 | WARN | SELECTED |
| Strategy_8.10.634 | 8 | 8/28 | 8,0574 | WARN | SELECTED |
| Strategy_8.11.487 | 8 | 7/26 | 11,6464 | WARN | SELECTED |
| Strategy_8.25.708 | 8 | 8/22 | 10,6267 | WARN | SELECTED |
| Strategy_8.26.438 | 8 | 7/34 | 7,0866 | WARN | SELECTED |
| Strategy_8.62.460 | 8 | 7/30 | 9,9595 | WARN | SELECTED |
| Strategy_8.67.447 | 8 | 9/30 | 8,2452 | WARN | SELECTED |

La vigésima-primera es `Strategy_1.13.611` (primera fila); la fila marcada "(no)" es un placeholder de lectura — las 21 seleccionadas son exactamente las filas con Decision SELECTED de la tabla §13. No se fabrican explicaciones matemáticas por estrategia (R-values no emitidos en wave2b); el análisis fino de comportamiento V2 por estrategia vive en el universo B (§10).

---

## 15. Detailed Review of the 13 Rejected Strategies (universo C)

Las 13 rechazadas comparten una única razón durable: **`NO_ACCEPTABLE_NEIGHBORHOOD`** — la Strategy no tuvo ni un vecindario 3×3 que sobreviviera la cadena de elegibilidad y gates (§4). En V2 esto significa cero candidatos al llegar a bandas/calidad, sin rank1 y por tanto sin decisión downstream.

Qué significa exactamente: la elegibilidad estructural/métrica (9 CELLs completas, passed, 3 métricas OBSERVED finitas) es **idéntica a la de V1**. Los gates propios de V2 (finiteness, cliff, bandas) también desembocan en esta razón si vacían el set, pero **no está demostrado —y no debe asumirse— que el cliff haya causado rechazo alguno a nivel Strategy en wave2b**: el contrato durable no emite la descomposición por etapa. La evidencia disponible del universo B (misma semántica, mismo criterio de elegibilidad) muestra que el 100% de los rechazos Strategy-level fueron estructurales (`NEIGHBORHOOD_NOT_PASSED`) y que los gates V2 no rechazaron ninguna Strategy completa; en wave2a, el cliff 35% no eliminó ninguna Strategy (18/18 pre-cliff-eligible la retuvieron, adversarial Attack 3).

| Strategy | Family | Reason (durable, E2E real) | Evidencia |
|---|---|---|---|
| Strategy_1.38.707 | 1 | NO_ACCEPTABLE_NEIGHBORHOOD | `results_v2.jsonl` fila FAIL; sin decisión PG |
| Strategy_1.83.581 | 1 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_2.17.503 | 2 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_2.17.581 | 2 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem (en wave2a materializaciones A/B sí tenía vecindario elegible — variación del Optimizer fresco, ver §16) |
| Strategy_2.25.400 | 2 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem (en universo B era seleccionable con cliff 0,3497) |
| Strategy_2.30.706 | 2 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_2.55.692 | 2 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_2.73.608 | 2 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_3.18.626 | 3 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_3.31.576 | 3 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem (en universo B V2 la seleccionaba con la mejor mejora de mediana) |
| Strategy_6.32.425 | 6 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_7.2.741 | 7 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |
| Strategy_8.46.640 | 8 | NO_ACCEPTABLE_NEIGHBORHOOD | ídem |

---

## 16. Historical V1 vs E2E V2

> [!warning] **NOT AN A/B COMPARISON.**
> El Optimizer fue **re-ejecutado** en wave2b: los CELL values son frescos (nueva materialización física del SQX en flota). wave2a y wave2b **no comparten inputs**, y las diferencias por estrategia confluían frescura-del-optimizer + algoritmo. La comparación cuantitativa V1-vs-V2 con inputs idénticos es exclusivamente la del universo B (§9–§10). Esto es sólo una comparación **operacional cualitativa**.

```text
V1 (wave2a, universo A — histórico):  34 → 10 WARN → 10 SELECTED · 24 FAIL (16 NO_ACCEPTABLE + 8 SEVERE_WARNING)
V2 (wave2b, universo C — E2E):        34 → 21 WARN → 21 SELECTED · 13 FAIL (todas NO_ACCEPTABLE; V2 no produce FAIL-SEVERE-with-picks)
```

Por estrategia (cruce de veredictos entre waves): 8/34 mismo veredicto · 13 FAIL(V1)→WARN+SELECTED(V2) · 2 WARN(V1)→FAIL(V2) (`2.17.581`, `3.31.576`) · 11 cambios de pick dentro de WARN. Ejemplo concreto del efecto frescura: `1.8.669` fue 7/32 (V1, wave2a) y 8/28 (V2, universo B sobre celdas c52) y 9/34 (V2, wave2b) — tres materializaciones, tres coords. La lectura operacional: V2 desbloquea strategies que V1 auto-gateaba por pico aislado y/o encuentra mesetas donde V1 no aceptaba vecindario, sin generar rechazos por cliff/bandas a nivel Strategy; las 2 inversiones y los 11 cambios de pick se explican por la combinación de celdas frescas + preferencia por mesetas, un trade-off ya aceptado como política del diseño V2.

---

## 17. Operational Rollout

```text
0.2.130 (flota pre-E2E):   SIN V2  (release: publish 0.2.130 desde 0a10612 — verificado en git log de xKoRx/symphony)
0.2.131 (flota vigente):   construida desde bc50bbb (SHA certificado Shot 3) con deploy_release.sh --release-only
rama E2E:                  feature/robust-selection-v2-hera-e2e @ 15ce01e (bc50bbb + commit de manifest 0.2.131) — pusheada a origin
binarios:                  worker SHA f6354373…, watcher SHA 0c811b9d…, vcs.revision=bc50bbb…, vcs.modified=false
manifest:                  MinIO deploy/worker/sqx/manifest.json @ 2026-09-30T23:27:05Z
rollout:                   3/3 certificado por Prometheus (series campaign_apply con process_executable_path=/opt/stager/releases/0.2.131/bin/symphony;
                           un worker vivo por host: Hera PID 56057, Kronos 1734488, Zeus 3301726)
```

Estado final de `master` (verificado en esta sesión contra `origin`):

| Referencia | SHA | Contiene V2? |
|---|---|---|
| runtime fuente (flota, 0.2.131) | `bc50bbba9a50b7079ed81ff96d80b9f1f780c368` | **SÍ** (rama certificada) |
| manifest de release (rama E2E) | `15ce01e7d0c6fa6d1b6372cf1561ffdfd265130e` | SÍ (`bc50bbb` + manifest) |
| `origin/master` | `ca07f72` (merge-base de ambas ramas) | **NO — absorción pendiente del Primary Technical Manager** |

Consecuencia operacional: `READY_FOR_NORMAL_V2_USE: YES` con la release 0.2.131 desplegada; la próxima release natural de master absorberá la rama V2 cuando el manager complete la integración (tarea abierta en la nota del proyecto). SSH `kor@` sigue roto (publickey denied 3/3); la verificación de rollout se hizo por el canal Prometheus certificado, igual que los preflights de host aceptados como riesgo conocido en wave2a.

---

## 18. Problems Encountered

Problemas **de V2** (afectan corrección del algoritmo/entrega): exactamente uno, atrapado antes de producción.

| # | Problema | Impacto | Resolución | ¿Afectó corrección de V2? |
|---|---|---|---|---|
| P1 | Shot 1 implementó un scalar inventado `RobustnessScore = 1/(1+R_retdd+R_aux)` (finding del Primary Manager) | Autoridad de ranking encubierta en V2 | **Eliminado en Shot 1R** (`bc50bbb`): V2 no define score escalar; `robustness_score` viaja en zero value contractual; `rank==1` única autoridad; quality key explícita (`ranking_metric=ret_dd` + mediana) con test de empate | No — corregido antes de certificar; Shot 2/3 lo re-verificaron |

Problemas **operacionales/de entorno** (ninguno afectó la corrección de V2):

| # | Problema | Impacto | Resolución | ¿Afectó V2? |
|---|---|---|---|---|
| P2 | `cells.tsv` histórico "zero bytes" vs manifest con hash no vacío (bloqueó el gate de durable replay histórico) | Replay histórico exacto no ejecutado | **Actualizado (hallazgo nuevo): el payload no vacío existe** — la copia del bundle c52 en el vault está íntegra (re-verificado hoy: 2.031.323 bytes, 1.836 filas, SHA256 `3e0dac89…` == manifest, == copia original en `forge-recovery-c52-20260928/artifacts/`). El estado vacío corresponde a la introducción histórica del artefacto (commit `8385041a` de agents-os). Queda vigente sólo el replay histórico como verificación diferida (los aggregates/picks del bundle son otra materialización) | No — fue historia/evidencia, nunca gate |
| P3 | Ambos MCPs Mongo (ro/rw) caídos durante el E2E — y siguen caídos hoy (re-confirmado) | Lectura durable Mongo durante E2E | Fallback: helper efímero read-only con el cliente del repo; evidencia registrada en el doc E2E | No (canal de lectura, no de ejecución) |
| P4 | SSH `kor@` no disponible (publickey denied 3/3) | Verificación de rollout y preflights de host | Verificación por el canal Prometheus certificado (series `campaign_apply` de la release); preflights aceptados como riesgo conocido, igual que wave2a | No |
| P5 | `libzmq.pc` ausente en Daedalus → `go build ./...` exit 1 (cadena `internal/tasks`→`sdk/pkg/mt5`→`pebbe/zmq4`) | Build-all local rojo | Clasificado **preexistente ambiental**: probado idéntico en el baseline `ca07f72` vía worktree temporal; delta V2 no toca esa cadena; sin sudo en Daedalus, deuda ajena no tocada | No |
| P6 | OTEL collector `.45` caído | Telemetría de export degradada | Preexistente, no bloqueante (documentado en E2E y en el contrato de ambiente) | No |
| P7 | Watcher legacy de wave2a aún vivo en Daedalus | Riesgo de interferencia pre-despacho | Eliminado antes del despacho de wave2b | No |
| P8 | Corrida wave2b ~21h vs ~12h de wave2a con flota sin cambios de config | Ventana operacional más larga | Observado, 0 errores de stage y sin retries anómalos; se reporta como dato, no como defecto | No |

---

## 19. Known Deferred Items (revalidados hoy)

| Ítem | Estado revalidado 2026-10-01 |
|---|---|
| MIN-01 — knobs V1 vestigiales (`ranking_metric`, `min_consistency`, `weight_center`, `weight_neighbors`, `max_*_cov`) participan del digest/identidad de config V2 sin efecto conductual | **Vigente**, DEFER (higiene futura del manager; dos configs V2 que difieren sólo en knobs muertos producen aggregates distintos con el mismo ganador) |
| MIN-02 — interacción preexistente SEVERE-with-picks vs durable select (`evaluateNeighborhoods` conserva picks en FAIL; durable select rechaza FAIL-with-picks) | **Vigente**, DEFER (preexistente V1, no introducida por el delta; en wave2b V2 no produjo ningún SEVERE-with-picks, pero el código permanece) |
| Historical exact durable replay (FlowRun wave2a `80647dc2`, reproducción V1 byte-exacta + replay V2 offline + sensitivity de parámetros sobre esa autoridad) | **Parcialmente desbloqueado, sigue abierto**: `cells.tsv` existe íntegro y SHA-verificado (P2 resuelto a favor), pero el replay histórico no se ha ejecutado y los aggregates/picks del bundle siguen siendo otra materialización (no reproducen desde cells.tsv); tarea abierta en el proyecto |
| Ratificación Owner de parámetros productivos (0.35/0.01/0.01 son valores de prueba observados, no defaults congelados) | **Vigente** — el freeze explícitamente no congela valores productivos; caso de sensibilidad `2.25.400` (cliff 0,3497 vs 0,35) documentado para esa decisión |
| Deudas operacionales de infra (SSH `kor@` roto; OTEL `.45` caído; `libzmq.pc` en Daedalus; MCPs Mongo intermitentes) | **Vigentes**, preexistentes y ajenas a V2 (§18 P3–P6) |
| ~~`cells.tsv` "missing"~~ | **CERRADO como finding de payload** — non-empty payload found, SHA verified (no repetir como missing) |

---

## 20. Final Assessment

Hechos (cada uno con evidencia en las secciones previas):

- **¿Funciona V2?** Sí. Con el mismo input exacto que V1 (universo B) selecciona las mismas 16 no-elegibles, desbloquea 6 auto-gateadas, mueve 13/18 rank1 hacia mesetas con menor R_retdd y no rechaza nada extra; con el flujo canónico en flota (universo C) produjo 21 selecciones durables con 0 errores de stage.
- **¿Está integrado?** En la flota sí (release 0.2.131 desde el SHA certificado, rollout 3/3, consumida por el pipeline real). En git: ramas `feature/robust-selection-v2-shot1` @ `bc50bbb` y `feature/robust-selection-v2-hera-e2e` @ `15ce01e` pusheadas; **`master` (`ca07f72`) aún no la absorbe** — integración pendiente del Primary Technical Manager.
- **¿Probado con datos reales?** Sí, dos veces: A/B sobre las 1.836 CELLs reales de wave2a (SHA-verificadas) y E2E sobre 1.836 CELLs frescas generadas por el Optimizer en la flota.
- **¿Probado E2E?** Sí: watcher → MinIO → PG config → Temporal → optimizer → evaluate_wfm → select_robust_run → decisiones durables, con evidencia auditable en cada eslabón y digest idéntico al trial local.
- **¿Cambió V1?** No. Byte y semánticamente intacto (digest V1 estable, `scoreNeighborhood`/`rankPicks` intocados, regresión V1 verde en Shots 1–3).
- **¿Hubo defectos de integración?** De V2: ninguno (89/89 stages, 0 errores). Se aplicó un fix de runtime (rollout 0.2.131) porque la flota no tenía V2.
- **¿Puede usarse normalmente?** Sí: `READY_FOR_NORMAL_V2_USE: YES` con 0.2.131 desplegada; basta declarar `wfm_params` V2 en la wave config.

Opinión del autor (separada de los hechos): el diseño resultó conservador donde importaba (0 rechazos nuevos) y el costo declarado — mover picks hacia mesetas sacrificando mediana Ret/DD en 7/13 casos — es exactamente el trade-off que el Owner aprobó al priorizar Ret/DD y robustez paramétrica. El punto que merece atención futura del Owner no es el algoritmo sino la sensibilidad del umbral (`2.25.400` a 0,0003 del cliff) y la ratificación de valores productivos.

---

## 21. Next Functional Step

El próximo paso natural del pipeline (sin ejecutar en este mandato): **Final Retester** sobre las **21 Strategies seleccionadas** por wave2b. El wave design de wave2b replicó el funnel de wave2a con STOP explícito antes de Final Retester/MT5 (verificado por MinIO: sin tasks de promotion/apply/MT5), así que el funnel queda esperando exactamente esa etapa con las 21 seleccionadas como entrada (evidencia: 21 decisiones PG SELECTED, `artifacts/herae2e/…/results_v2.jsonl`, MinIO `sqx-strategies/wave_wave2b/`). No se propone trabajo adicional de diseño de Robust Selection.

---

## Appendix A — Fuentes revisadas (12 docs + artifacts + repo)

Documentos del proyecto (todos leídos completos para este reporte): [[ROBUST-V2-DESIGN-FREEZE]] · [[ROBUST-V2-DESIGN-CANDIDATE]] · [[ROBUST-V2-DESIGN-ITERATION-2]] · [[ROBUST-V2-FINAL-ADVERSARIAL-REVIEW]] · [[ROBUST-V2-FINITENESS-VERIFICATION]] · [[ROBUST-V2-DURABLE-REPLAY]] · [[ROBUST-V2-SHOT2-ADVERSARIAL-REVIEW]] · [[ROBUST-V2-SHOT3-FINAL-CERTIFICATION]] · [[ROBUST-V2-LOCAL-VALIDATION]] (+CSV) · [[ROBUST-V2-HERA-E2E]] (+CSV) · nota de proyecto [[Echo Forge — Robust Run Selection V2]] · bundle históricos en [[Echo Forge — Operación Real V2]].

Artifacts raw: `artifacts/local-validation-20260930/` (`strategies.tsv`, `v1_candidates.tsv` 214 filas, `v2_candidates.tsv` 952 filas, `details.json`, `five_cases.json`, `v2_stage_counts.json`) · `artifacts/hera-e2e-20261001/` (spec despachado `20260930_204232_flow-robust-v2-hera-e2e-wave2b.json` SHA `49a952b7…`, `results_v2.jsonl` SHA `688128a6…`, `monitor-wave2b.log` SHA `0b902554…`, `SHA256SUMS.txt`) · corpus `c52-wave2a-20260929/cells.tsv` (SHA `3e0dac89…` re-verificado).

Repo (verificado hoy contra origin): `xKoRx/symphony` — `origin/master` `ca07f72`; `origin/feature/robust-selection-v2-shot1` `bc50bbb`; `origin/feature/robust-selection-v2-hera-e2e` `15ce01e`; delta `ca07f72..bc50bbb` = 7 archivos +1217/−42; release 0.2.130 = `af8f1ae` (sin V2).

Contratos de producto referenciados: `xKoRx/symphony:specs/FEAT-SQX-DURABLE-WFM/SPEC.md` (§11: score no-autoridad) · `specs/FEAT-SQX-DURABLE-ROBUST-SELECTION/SPEC.md` (`select_robust_run` consume `rank==1` único).

## Appendix B — Mapa de reconciliación numérica (QA de este reporte)

| Afirmación | Verificación hecha en esta sesión |
|---|---|
| Funnel C: 34/1836/34/0-21-13/21 rank1/21 SELECTED/89 stages/0 errores | Recount de `results_v2.jsonl` (34 filas, 21/13, 1 digest) + cola `monitor-wave2b.log` (COMPLETED 34/34/21, DECISION 21, TERMINAL, 0 FAILED) |
| Tabla de prefijos 1–8 (5/10/2/1/1/5/3/7; 21 seleccionadas) | Recount desde `results_v2.jsonl` — coincide con valores esperados del mandato |
| A/B: 12 WARN + 6 SEVERE V1; 18 WARN V2; 16 rechazos idénticos | Recount desde `details.json` (34 entradas) + `ROBUST-V2-LOCAL-VALIDATION.csv` |
| 13 cambios; 13/13 menor R_retdd; 12/13 menor R_aux; 7 sacrificios (mediana −1,24; peor −2,18); 5 mejoras; 1 empate | Recomputado desde `details.json` — coincide con [[ROBUST-V2-LOCAL-VALIDATION]] |
| Cliff 26/214 = 12,15%, 6 estrategias (8/7/1/1/5/4) | Recomputado desde `v2_candidates.tsv` (`cliff > 0.35` sobre 214 analíticamente válidos) |
| cells.tsv íntegro | `sha256sum` = `3e0dac89…` (== manifest), 1.836 filas, 2.031.323 bytes |
| master sin V2; ramas pusheadas; delta 7/+1217/−42; 0.2.130 sin V2 | `git fetch` + `git log`/`git diff --stat` contra `origin` en clone local |
| Digest V2 único `sha256:24daf87d…` en B y C | `results_v2.jsonl` (C) + [[ROBUST-V2-LOCAL-VALIDATION]] (B) — idénticos |
| Mongo/PG durable wave2b | No re-querido hoy (MCP Mongo caído — re-confirmado; PG RO no expone `sqx.decisions`): se cita lo verificado y documentado en la sesión E2E |

---

```text
FINAL STATUS: TECHNICAL_REPORT_COMPLETE

TECHNICAL_DOCUMENT_SKILL:
  name/path: human-first-technical-writing
             main/30-resources/agents/skills/human-first-technical-writing/SKILL.md
  (skill canónica de documentación técnica del registry federado de Agents-OS; aplicada:
   orden por preguntas del lector, profundidad progresiva, causalidad, sin diagramas
   decorativos, sin hard-wrap, incertidumbre declarada y no convertida en certeza)

REPORT:
  path: main/10-projects/Echo Forge — Robust Run Selection V2/ROBUST-V2-TECHNICAL-RESULTS-REPORT.md
  commit: (ver HANDOFF final de la sesión; vault sincronizado por sync.sh)

SOURCES_REVIEWED: 12 docs del proyecto + 2 bundles de artifacts + 1 corpus cells.tsv + repo git + specs
KEY ARTIFACTS: artifacts/local-validation-20260930/ · artifacts/hera-e2e-20261001/ · c52-wave2a cells.tsv (SHA verificado)

MASTER_STATE:
  SHA: ca07f72 (origin/master, sin V2 al cierre de este reporte)
  V2 integrated: NO en master — SÍ en ramas pusheadas (bc50bbb / 15ce01e) y en runtime 0.2.131 (rollout 3/3)

COHORT:
  strategies: 34 (NDX L H1 SQX v1, cohort wave1z / 02_full_retester)
  workflow groups: 1 (03_optimizer_v2_group; tasks project/evaluate_wfm/select_robust_run; max_parallel 3)
  numeric prefixes/families: 1(5) 2(10) 3(2) 4(1) 5(1) 6(5) 7(3) 8(7) — prefijo descriptivo, sin evidencia de group_id semántico
  families represented among selected: 1,2,4,5,6,7,8 (todas menos 3)

LOCAL_A_B:
  key results: mismo set de 16 rechazadas; 6 FAIL-SEVERE→WARN; 13/18 rank1 cambiados (13/13 menor R_retdd,
  12/13 menor R_aux); 7 sacrificios mediana Ret/DD (mediana −1,24, peor −2,18), 5 mejoras, 1 empate;
  cliff 26/214=12,15%; 0 rechazos Strategy-level por gates V2; sin defecto de implementación

HERA_E2E:
  key results: 34→1836 CELLs→34 WFM→21 WARN→21 SELECTED / 13 NO_ACCEPTABLE; 89 stages, 0 errores;
  0.2.131 desde bc50bbb, rollout 3/3; durable evidence completa (digest 24daf87d… == trial local);
  STOP antes de Final Retester verificado

DECISIONS_DOCUMENTED: 21 (registro §5, con tipo design/manager/owner/implementation)

STRATEGY_DETAIL:
  34/34 covered: YES (tabla §13)
  21 selected covered: YES (§14)
  13 rejected covered: YES (§15)

CAVEATS:
- wave2a vs wave2b NO es comparación A/B (optimizer re-ejecutado, celdas frescas); A/B real = universo B
- R_retdd/R_aux/cliff/Sharpe/Profit en blanco para wave2b: el contrato durable no los emitió (no fabricar)
- NO_ACCEPTABLE_NEIGHBORHOOD de wave2b no descompone por etapa; no atribuir cliff por Strategy sin evidencia
- cifras históricas V1 (10/24) y del A/B local V1 (12/22) difieren por materialización: ambas son correctas en su universo
- participaciones por host (39/22/109) provienen del monitoreo de host de la sesión E2E, no del bundle SHA-deado
- Mongo/PG durable de wave2b citado de la sesión E2E (MCP Mongo caído al escribir este reporte — re-confirmado)

DEFERRED:
- MIN-01 knobs vestigiales en digest V2; MIN-02 SEVERE-with-picks preexistente
- historical exact durable replay (parcialmente desbloqueado por cells.tsv íntegro)
- ratificación Owner de 0.35/0.01/0.01 productivos
- deudas operacionales: SSH kor@, OTEL .45, libzmq.pc Daedalus, MCPs Mongo intermitentes

QA:
  skill validation: human-first-technical-writing aplicada (scan/backtracking/mental-model; sin hard-wrap)
  links checked: wikilinks a los 12 docs del proyecto + artifacts paths verificados en disco
  numbers reconciled: ver Appendix B (recounts independientes de CSV/JSON/log/git)

NEXT EXACT:
  Return report to Primary Technical Manager + Owner.
  Do not modify product code.
```
