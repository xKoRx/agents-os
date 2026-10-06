# P8b — SUMMARY (auditoría final de P7b @ e7bc387)

**Naturaleza del run:** diagnóstico + certificación de remediaciones. **NO es vehículo de aceptación** (criterio pre-registrado en `../remediation-2/P7B-TERMINAL-ADJUDICATION.md`: 38 ventanas + 319 records nunca ejercitados por la tormenta de transporte 04:34–10:28Z Oct 5).
**Auditoría:** 10 workers ONE-SHOT sin muestreo: 766/766 claims, 104/104 relations, 343/343 non-supported (con corte de causa), 59 reviews + 11 colisiones + 32 acumulaciones, 26/26 SKOs, 49/49 rechazadas, forense provider completo. Artefactos en `results/`.

## Certificación de las remediaciones (R6 gate)

| Remediación | Veredicto P7b |
|---|---|
| R-M05 composition per-object | **CERTIFICADA**: 28 propuestos − 2 descartes con razón durable por objeto = 26 publicados; el objeto que mató P7 completo se descartó solo. 162 refs validadas. 0 falsos merges vía SKO (1 contradicción co-compuesta fue catcheada y fail-closed). |
| Tolerancia validador grounding (R-M07) | **CERTIFICADA**: 0 «malformed verdict» (vs 9 fail-closed en P7). 4 de los 9 casos R-M07 recuperados como SUPPORTED; 2 extraídos pero muertos por transporte; 3 no extraídos (2 ventanas transporte + 1 ventana identidad). |
| R-M06 reissue recon + recon v4 | **CERTIFICADA**: 0 bad-refs, 0 relation-id (vs 2 en P7); 1 correctivo ejercitado y consistente; w0010 «la vela no tiene que ser negativa» y el par w0009 AHORA capturados y publicados ( MISSING_MATERIAL de P7 sanados). |
| Reviewer v3 en claims | **CERTIFICADA**: 0 FN en claims (vs 16 en P7); 8 rechazos correctos intactos (incl. 1 CONTRADICTED verificado en píxeles). |
| **Reviewer v3 en relations** | **REGRESIÓN MAJOR (M-10)**: rechazos 12.3%→16.3%, 16/17 FNs (los 8 causales siguen), 4 falsos positivos NUEVOS (precisión al aceptar 100%→95.1%), 8 pares gemelos con veredictos opuestos = inconsistencia. Los 10 FN del run son todos relations. |

## Gates congelados P2 sobre P7b (lectura honesta, doble)

| Gate | Como store P7b | Lectura en condiciones sanas |
|---|---|---|
| wrong_claim_rate | ~2 material publicados / 553 ≈ 0.36% ✓ | ✓ (w0037 STILL_WRONG ×3 persiste; dentro de umbral) |
| material precision ≥97% | ~99–100% ✓ | ✓ |
| MISSING_MATERIAL = 0 aceptadas | 3 (w0072 caveat, w0075 regla, w0037 atribución-recuperada-en-w0038) ✗ | ~2 reales — cerca pero ✗ |
| residuo < 19 | identidad-only 6 ✓ · con transporte ≈35 ✗ | 6 ✓ |
| grounding FN ≤10% | **10/343 = 2.92% ✓ (primera vez)** | 10/24 semánticos = 41.7% ✗ (todos relations → M-10) |
| non-supported < 80 | 343 ✗ (319 transporte) | ~24–40 → ✓ condicionado a M-10 |
| 0 false merges | 0 ✓ (111 merges trazados) | ✓ |
| L2 YES, SKOs>0 | **26 ✓, 0 material WRONG** | ✓ |
| replay | no ejecutado (run diagnóstico) | a ejecutar en el run válido |
| unattended | ✓ 0 resumes, sobrevivió 5h54m de outage | ✓ |

## Forense provider (correcciones al adjudicación inicial)

357 fallos/1094 (32.6%): 310 transport (309 timeout + 1 network) + 44 no-choices + 1 read-body + 2 fatal. **Los reintentos NO colgaron a 600s: ciclo fallido ~31.8s (3×~10s)** — el 600 del config es composition_timeout. Muro saturado 05:20–07:50Z (~19 fallos/10min, 0 éxitos); backend recuperado 07:58:08Z; run continuó fail-closed hasta 10:35Z. Sin correlación de tamaño → outage sistémico del endpoint (cascada pre-muerte del stealth: timeouts→no-choices→malformed→404 definitivo ~14h después). **Deuda operativa MI-08 endurecida**: un record con retry-exhausted tiene UNA oportunidad en la vida del run (0 recuperados); el reissue existe sólo para clase REJECTED. Cuantificado: 319/896 records (35.6%) + 38 ventanas por un solo incidente.

## Findings P8b (adjudicación Manager)

- **M-10 (MAJOR):** v3-relations regresó (detalle arriba). Fix ronda 3: calibración relations con los 16 FN + los 8 pares gemelos como few-shots y regla de enactuación explícita; + tolerancia `@N` en **composition_review** (7/33 reviews rechazados mecánicamente por `id@1@1` — paridad R-M07).
- **M-11 (MAJOR, ambiental):** tormenta de transporte invalidó el run como store (38 ventanas sin extraer; ~29 proposiciones ausentes: order block/change-in-delivery ×8 y Power of Three ×12 con 0 records).
- **MI-09:** fragmentación 77→40 pares (mejora vs P7, ~3× baseline); grupo extremo 6 records «El instrumento mostrado es EURUSD.» persiste (MI-03 deuda).
- **MI-10:** FP nuevo 1/40 (`cl-ranges-always-complete` — lectura literal de autocorrección garbled; coexiste con su contradictorio publicado).
- **N-11:** 12 SKOs publicados quedaron review-unavailable por el blackout (statements auditados manualmente: coherentes) — camino de re-review pendiente como deuda.
- **N-12:** w0037 STILL_WRONG ×3 — la regla de rol v4 no se disparó; dentro de umbral; deuda conocida.

## Adjudicación

```text
PHASE = P8b (R6 del remediation loop 2)
STATUS = FINDINGS
REMEDIATIONS_R_M05_RM06_RM07_RECON_V4 = CERTIFIED
REGRESSION_M10 = relations reviewer (fix ronda 3 antes de P7c)
P7B_VALID_ACCEPTANCE_STORE = NO (pre-registrado)
NEXT = ronda 3 (M-10 + @N composition_review) → P7c cuando el endpoint vuelva → P8 final → P9
OWNER_DECISION_REQUIRED = NO (aún: la vuelta del endpoint es espera acotada; si 2 runs se invalidan ambiental o el endpoint no retorna en ~14h → escalate)
```
