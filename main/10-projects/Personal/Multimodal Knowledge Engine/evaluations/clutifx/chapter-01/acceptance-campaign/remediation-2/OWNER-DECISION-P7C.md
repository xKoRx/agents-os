# OWNER DECISION REQUIRED — Bloqueo ambiental del acceptance run (Clutifx Ch01)

**Fecha:** 2026-10-06 ~16:00Z · **De:** Primary Technical Manager / Acceptance Lead (campaña P1–P9)
**Estado:** `OWNER_DECISION_REQUIRED = YES` — condición pre-registrada por ambos tracks (`remediation-2/P7B-TERMINAL-ADJUDICATION.md`, memoria compartida).

## Qué está bloqueado y por qué es irreducible

El único paso que falta para `CHAPTER_01_ACCEPTED` es el **acceptance run (P7c)** con el bundle completo `20ad4de` (todas las remediaciones R-M05/M06/M07/M10 + prompts recon v4 + ground v3-claims/v4-relations). El backend VLM `openrouter/stealth/space-bunny-alpha` — el modelo con el que se extrajeron el baseline (ef53530), run-1 (19b44c1) y P7b (e7bc387) — **está 404 «No endpoints found» desde ~Oct 5 14:00Z (~24h)**. Los endpoints stealth son efímeros: murieron tras una degradación de 6h (timeouts → no-choices → malformed → retiro).

No es reparable por técnica: reintentar es lo único que podemos hacer (2 vigilantes activos, tope ~19:00Z), y **elegir un modelo sucesor cambia la semántica y la provenance de extracción** — es una decisión de producto, no del acceptance lead.

## Las opciones (con coste y consecuencia)

| Opción | Qué implica | Coste / riesgo |
|---|---|---|
| **A. Esperar el retorno del endpoint** (recomendada si el stealth vuelve) | Los vigilantes lanzan `run-rerun3c` automáticamente con `20ad4de` (checklist en `~/mke/clutifx-ch01-rerun3-20261005/README-P7C-COORDINATION.md`). ~15h de run + ~4h de P8 final. | Sin coste si no vuelve; comparabilidad 1:1 con baseline y todos los runs previos; riesgo: el endpoint puede no volver nunca. |
| **B. Re-certificar contra un modelo sucesor** (elegir id en `MKE_OPENROUTER_MODEL`) | Probe-runtime del nuevo modelo + P7c + P8 final. | ~20h + re-baseline: la comparación old-vs-new pasa a ser entre modelos distintos → los umbrales P2 miden producto+modelo; la provenance del capítulo cambia de modelo. Requiere aceptación explícita de esa política. |
| **C. Congelar Chapter 01 con el store de P7b** (`e7bc387`: 553 supported / 343 non-supported, 26 SKOs, 82/130 ventanas) | Requiere **waiver del owner** de 3 umbrales congelados (MISSING_MATERIAL=0 → 2–3; non-supported<80 → 343 por transporte; residuo<19 → ~35 con el bloque w0093–w0130 sin extraer: order block/change-of-delivery y Power of Three con 0 records). | El store pierde ~8m12s de material del capítulo (29 proposiciones); exactitud de lo publicado es excelente (~99% material precision, 2 wrong publicados). Congelar esto es un capítulo incompleto. |

**Recomendación del manager:** A (esperar al stealth, vigilantes ya en pie) con B como plan B si el owner prefiere no depender de endpoints efímeros a escala. C sólo si el owner decide que el capítulo no vale otro ciclo — en contra: el contenido faltante (order block + Power of Three) es material central de la estrategia del curso.

## Evidencia de soporte (todo persistido)

- Auditoría run-1: `acceptance-campaign/p8-final-audit/` · Auditoría P7b: `acceptance-campaign/p8-final-audit2/` (+`P8b-SUMMARY.md`)
- Criterio de validez del run pre-registrado: `acceptance-campaign/remediation-2/P7B-TERMINAL-ADJUDICATION.md`
- Remediaciones ronda 2 y 3 con adversariales: `acceptance-campaign/remediation-2/` (R1…R3c-ADJUDICATION) · origin = `20ad4de`
- Tormenta de transporte (forense): `p8-final-audit2/results/PROVIDER-RESILIENCE-AUDIT.md`
- Checklist de relanzamiento: `~/mke/clutifx-ch01-rerun3-20261005/README-P7C-COORDINATION.md`

## Estado terminal de la misión (interino, bloqueado por owner)

```text
P8_EXHAUSTIVE_ACCEPTANCE (run-1) = FINDINGS → remediated (rondas 2-3, certificadas en P7b)
P9_FREEZE = NOT_EXECUTED (no hay run válido para congelar)
CHAPTER_01_ACCEPTED = NO (pendiente del acceptance run)
READY_TO_SCALE_CORPUS = NO (mismo bloqueo; el resto de gates de escala ya pasó: 0 babysitting, replay PASS, L2 fiable)
OWNER_DECISION_REQUIRED = YES (opciones A/B/C arriba)
Vigilantes: track-A waiter EXPIRADO (96/96, 15:55Z) · watcher P8/P9 activo hasta ~19:00Z (probe 78/96, auto-lanza run-rerun3c si el modelo vuelve)
```

Si el modelo retorna tras este handoff: relanzar con el checklist de coordinación y ejecutar P8 final + P9 (todo el tooling y los workers están preparados y reutilizados con éxito dos veces).
