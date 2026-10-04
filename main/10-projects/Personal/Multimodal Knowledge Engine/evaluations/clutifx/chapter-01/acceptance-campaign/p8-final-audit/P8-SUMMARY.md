# P8 — EXHAUSTIVE OLD-vs-NEW ACCEPTANCE · SUMMARY

**Fase:** P8 del programa de aceptación MKE V2 · Clutifx Chapter 01.
**Candidato:** `19b44c193e6ac5b9cd3be26c03792e43113fbe08` (branch `feature/v2-layered-knowledge-model`, binary sha256 `e5e4fcbe…`, config sha256 `02f5f7ad…`, config_fingerprint run `21278b86…`, fuente `4de8f12d…` verificada).
**Run P7:** `~/mke/clutifx-ch01-rerun-20261003/run-rerun/` — 130/130 ventanas live, 2026-10-04T01:51Z→16:33Z, **14h48m52s unattended**, exit 4 INCOMPLETE ordenado. Cero intervención manual (verificada por 6 vías independientes).
**Método:** 10 workers ONE-SHOT fresh-context + Manager. Cobertura física completa SIN muestreo: 1043/1043 claims, 146/146 relations, 19/19 ventanas rechazadas, 64/64 non-supported, 78/78 casos identidad (71 reviews + 17 colisiones −solapes), 1 composition + journal provider completo, replay recorded del journal durable.

## Cobertura de auditoría (P8 COVERAGE REQUIREMENTS)

| Población | Requerido | Auditado | Artefacto |
|---|---|---|---|
| ventanas | 130/130 | 130/130 | `results/FULL-WINDOW-AUDIT.md` |
| claims | todos (1043) | 1043/1043 | `results/FULL-CLAIM-AUDIT.jsonl` (+A1–A4) |
| relations | todas (146) | 146/146 | `results/FULL-RELATION-AUDIT.jsonl` |
| ventanas rechazadas | 19/19 | 19/19 | `results/REJECTED-WINDOW-AUDIT.md` |
| non-supported | 64/64 | 64/64 + muestra distribuida 61 supported | `results/GROUNDING-AUDIT.md` |
| identidad | todas | 78/78 + fragmentación + acumulaciones 38/38 | `results/IDENTITY-AUDIT.md` |
| provider | todos los eventos | 1618 calls, 244 eventos | `results/PROVIDER-RESILIENCE-AUDIT.md` |
| L2 | composition + SKOs | 1 invocación + 23 objetos/164 refs | `results/L2-SKO-AUDIT.md` |
| replay | PASS | export 1391 fixtures → run recorded → compare | `../REPLAY-AUDIT.md` |

## Resultado por gate congelado P2

Ver `../OLD-VS-NEW.md` (delta completo 40+ métricas) y `../RESIDUAL-FINDINGS.md` (adjudicación findings).

- **PASS:** wrong_claim_rate (3 publicados = 0.27% ≤0.5%; ~0.5% material ≤1%; sin WRONG nuevo en reglas centrales) · material precision 98.2% ≥97% · identity false merges 0 (invariante) · 0 corrupción · atomicity PASS · replay PASS (0 divergencia de conocimiento) · non-supported 64 < 80 · residuo ventanas rechazadas 10 < 19 · falsos positivos 0 (safety rule) · manual resumes 0 · run fatals 0.
- **FAIL:** L2_REACHED (0 SKOs — B-08) · MISSING_MATERIAL = 4 en aceptadas (M-08; umbral 0) · grounding FN rate 25% semántico / 46.9% con causa-provider (M-07; umbral ≤10%).
- **Mejora con deuda:** inestabilidad clasificación 16→6 deterministas (no eliminada) · falsos splits 2→0 · fragmentación 13→77 pares (MI-05, peor) · bad-refs 4→2 (transientes de ventanas distintas).

## Erratas P6

Resueltas contra journal durable y persistidas en `../P6-ERRATA.md` (A: 8 equivalence reviews semánticos ≠ 0 colisiones deterministas — métricas distintas; B: bad-ref defect FIXED 3/3, w0003 = rechazo nuevo no relacionado NO recovered).

## Regression watch (4 wrong baseline)

1. `cl-vela-negativa-mayoria` → **ABSENT_AND_MISSING** (corrección ausente; parte de M-08).
2. `cl-entradas-sirven-para-encontrar-bias` → **FIXED** (`cl-los-rangos-son-importantes-para-encontrar-entradas/bias` + relación).
3. `cl-objetivo-hoy-rango-bullish-libra` → **STILL_WRONG** (`cl-gbpusd-today-target-137489` publicado SUPPORTED con el mismo nivel equivocado; M-09).
4. `cl-cambio-oferta-demanda-termino-ingles` → **FIXED** (`cl-change-of-delivery-similar-to-trend-change` + relación; verificado contra asr-00233/234).

## Adjudicación

```text
PHASE = P8
STATUS = FINDINGS
CHAPTER_THRESHOLDS_MET = NO        (3 gates: B-08 L2, M-07 FN, M-08 MISSING_MATERIAL)
OWNER_DECISION_REQUIRED = NO       (reparaciones técnicas acotadas; sin choice semántica genuina)
NEXT_PHASE_AUTHORIZED = YES        (remediation loop R1→R6)
```

**Plan de remediación (loop):**
1. **R1** diseño ONE-SHOT del bundle: adoptar R-M05 (composition por-objeto) + R-M06 (reissue recon), tolerancia de formato del validador grounding (recupera 9 records con veredicto SUPPORTED en journal), reviewer v3 (causal/deixis/garble), recon v4 (negaciones/excepciones + forward-refs + verificación de niveles reforzada).
2. **R2/R3** implementación + adversarial independiente (incluye falsificar R-M05/R-M06 adoptados).
3. **R5** full rerun (los cambios de prompt alteran materialmente el output → rerun justificado; R-M05/R-M06 viajan en el mismo bundle).
4. **R6** P8 otra vez sobre el nuevo run (tooling y corpus builder reutilizables).
5. **R4** targeted live queda absorbido por el full rerun (las 5 parse-fatal y el L2 se ejercitan en el rerun remediado).
