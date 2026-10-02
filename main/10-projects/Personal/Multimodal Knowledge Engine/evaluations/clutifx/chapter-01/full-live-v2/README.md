# CLUTIFX CH01 — FULL LIVE EXTRACTION (MKE V2 @ ef53530)

**Veredicto del operador: `CLUTIFX_CH01_FULL_LIVE = INCOMPLETE_USEFUL`.** El capítulo 01 completo (130 ventanas canónicas, 34:04) fue extraído live con el producto certificado `ef53530756a27009517030a1bd29f0472bb3ad48` y terminó en INCOMPLETE ordenado (exit 4) con **803 claims + 130 relations canónicas en español (853 supported / 80 non-supported)**, ladder de identidad ejercitado a escala por primera vez (12 acumulaciones aplicadas y auditadas físicamente), replay recorded PASS, y L2 no alcanzado por un fallo de transporte de composition (razón durable). La extracción es útil y auditable: cada omisión y rechazo está explícito.

## Qué contiene este bundle

| Archivo | Contenido |
|---|---|
| RUN.md | Ejecución completa: precondiciones, 3 tramos (2 crashes + resume contractual), terminal state, replay |
| SOURCE.md | Source, transcript, L0 reutilizado con verificación física |
| METRICS.json | Todos los contadores + REQUIRED HANDOFF |
| WINDOWS.md | Disposición de las 130 ventanas + razones durables de rechazo |
| COVERAGE.md | Mapa temporal 00:00→34:04 por bloques |
| REVIEW-INDEX.md | **Índice principal para el Owner**: video ↔ conocimiento, una fila por ventana |
| OWNER-VALIDATION.md | Checklist de validación humana (13 intervalos + muestra de 5 tramos) — sin rellenar |
| OMISSIONS.md | Rechazado-explícito vs nunca-observado; omisiones L2/budget/provider |
| EQUIVALENCE-DECISIONS.md | Las 38 colisiones de identidad: statements, veredictos, clasificación humana, aplicados |
| MANAGER-REVIEW.md | Facts para adjudicación del Primary Manager (sin decisión) |
| PROVENANCE.md | Cadena de custodia SHA/fingerprints, inmutabilidad del producto, crash/resume |
| REQUEST-AUDIT.md | Métricas del provider: llamadas, errores, tokens, budget |
| claims.jsonl / skos.jsonl / documentation.md | Salidas canónicas del run (byte-a-byte) |
| transcript.json | Transcript ligado al source (para mapear evidence refs asr-*) |
| window-coverage.json / accumulation-audit.json / atomicity-audit.json / replay-comparison.json / replay-script.json | Proyecciones de auditoría máquina |

## Números clave

```text
CLUTIFX_CH01_FULL_LIVE = INCOMPLETE_USEFUL
WINDOWS: 130 intentadas / 104 aceptadas / 26 rechazadas / 0 unavailable
L0_REUSED = YES (binding físico completo)
Claims: 1039 propuestas → 803 canónicas (741 supported) · Relations: 168 → 130 (112 supported)
Idioma: 803 es / 0 en / 0 other · Integrity 933/933 PASS
Ladder: 38 colisiones · 21 adjudicaciones semánticas (17 live) · 11 EQUIVALENT / 6 DIVERGENT
Acumulaciones aplicadas live: 12 (7 records) · LIVE_ACCUMULATION_AUDIT = PASS
WHOLE_WINDOW_ATOMICITY = PASS · POTENTIAL_FALSE_SEMANTIC_MERGE = NO
L2_REACHED = NO (composition_unavailable por transporte; 0 SKOs)
Bad evidence refs: 4/130 ventanas (3.1%) · 0 JSON malformado · 115 correctivos de grounding
Provider: 1196 llamadas · 8,600,403 tokens · costo no expuesto (null)
Wall: 9h27m17s (3 tramos, 2 crashes recuperados por crash/resume contractual)
REPLAY = PASS (outcome idéntico; deltas enumerados en RUN.md)
```

## Cómo revisar (Owner)

1. Abrir **REVIEW-INDEX.md**, reproducir el video en cualquier intervalo y comparar contra los records listados.
2. Calificar con **OWNER-VALIDATION.md** (13 bloques + 5 muestras detalladas).
3. Revisar omisiones en **OMISSIONS.md** y las decisiones de identidad en **EQUIVALENCE-DECISIONS.md**.

Runtime local completo (run.db con journal íntegro, snapshots de crashes, replay run, tooling de análisis): `~/mke/clutifx-ch01-full-live-20261001/`. No se subió video, frames pesados ni secretos.
