# P8 Final Audit — A3 (w0067–w0099, run rerun @ 19b44c1)

Auditoría fuente-grounded de la población COMPLETA de claims del candidato para las
ventanas w0067–w0099. Sin muestreo: cada claim se verificó contra el transcript del
corpus y, para claims visuales (niveles de precio, colores, rectángulos, etiquetas de
UI, temporalidad/instrumento), leyendo el PNG citado (~65 frames leídos).

Ámbito: 28 ventanas aceptadas (w0075, w0081, w0088, w0093, w0098 sin claims → excluidas).

## Cifras

- **Claims auditados: 279** (una fila por claim en `FULL-CLAIM-AUDIT-A3.jsonl`).
- **Distribución de labels:**
  - CORRECT: **243**
  - DUPLICATE: **35**
  - WRONG: **1**
  - PARTIAL / OVERGENERALIZED / UNVERIFIABLE_FROM_AVAILABLE_EVIDENCE: 0
- **Material precision parcial:** MATERIAL=YES = 177; aceptables (CORRECT+DUPLICATE) =
  176 → **99,4 %** (176/177).
- **MISSING_MATERIAL: 1** (`MISSING-KNOWLEDGE-A3.jsonl`); MISSING_NON_MATERIAL: 0.

## Hallazgo WRONG (1)

- `w0094 / cl-chart-symbol-gbpusd` — «El gráfico muestra el símbolo GBPUSD».
  El frame citado (p129240000) muestra la cabecera «**EURUSD** · 8h · FOREX.com».
  GBPUSD sólo aparece como rótulo del diagrama dibujado, no como símbolo del gráfico.
  MATERIAL=YES (identidad de instrumento). Es el único defecto factual del rango.

## Patrones notables

1. **Duplicates (35) concentrados y legítimos:** casi todos provienen de utterances de
   ASR compartidas entre ventanas adyacentes (asr-00134, 00136, 00141, 00156, 00168,
   00169, 00174, 00190, 00193, 00194), que se re-minan en cada ventana solapada. Cada
   DUPLICATE referencia el claim canónico previo. Grupo típico: w0076→w0079 (reglas de
   «cierra afuera / esperar nueva vela / tomar low / formar rango») y w0091→w0092
   (definición SMT euro/correlacionado/reversal).
2. **Garbles ASR citados fielmente no degradan el claim** (según criterio del encargo):
   «Tartle Sup/Tartel Sub» ≡ Turtle Soup, «intertartel sub», «DXI» (≈DXY), «JP» (≈JPY),
   «GIP» (≈GBP), «S&T» (≡SMT). Caso especial: `cl-smt-desarrollo-capitulo` (w0085) tiene
   el garble **en el statement** («se Osborneá» ≈ se desarrollará); la proposición es
   correcta y verificable (asr-00188) → CORRECT con nota.
3. **Discrepancia instructor vs pantalla (no engendra error):** en w0097 el instructor
   dice «gráfico de 4 horas» pero la cabecera muestra 8h; los claims VIDEO_OBSERVED
   reportan fielmente la cabecera (8h) y la regla queda como condicional, tal como fue
   enunciada.
4. **Cobertura de parámetros numéricos excelente:** todos los niveles de la herramienta
   de posición (apertura 1,14487; stop 1,14229; objetivo 1,15321; R:R 3,23; cantidad
   1550387) y los deltas de w0069 (stop 0,00209→0,00258; objetivo 0,00209→0,00835;
   R:R 0,81→3,24) verificados contra píxeles de los frames. El rectángulo de la SMT de
   la estrategia propia queda clavado (1,15239 / 1,14592→1,14493).
5. **MISSING (1):** identidad EURUSD/15M del gráfico de demostración visible en cabecera
   desde w0067 pero no canónica hasta w0073/w0077 (15M) y w0084 (EURUSD, ya en 8h);
   w0067 sólo capturó la plataforma (FOREX.com).

## Cobertura de verificación

- 279/279 claims con veredicto y cita de fuente.
- Lectura visual de frames en 26 de 28 ventanas (todas las que tenían claims visuales).
- Frames con `exists=true` en todo el rango; ningún evidence roto detectado.

## FEEDBACK (Agents-OS)

- **Friction menor — omisión casi-commitida de w0074:** al agrupar por rangos contiguos
  de ventanas aceptadas, w0074 quedó fuera de mi primer lote (la recuperé en el chequeo
  de totales: 279). Un manifiesto `accepted_windows` o un índice por-worker en el corpus
   evitaría este riesgo.
- **Frames fuera de ventana:** el corpus cita frames muy fuera de la ventana temporal del
  claim (p.ej. w0077 usa p158040000, pts 29:16, para justificar la temporalidad 15M).
  Funciona, pero confunde la auditoría; mejor acotar evidence a la ventana o anotar el
  motivo.
- **Duplicados sistemáticos por solape de transcript:** ~12,5 % del store del rango son
  re-canonizaciones de la misma utterance en ventanas adyacentes. Un pase de dedup
  (candidato a duplicado si comparte `evidence_ids` de ASR con un claim canonical
  previo) lo detectaría automáticamente.
- **Garbles en statements:** los garbles de ASR dentro del statement (no sólo en la
  evidencia) precisan siempre re-lectura humana; un campo `normalized_terms` en el
  claim ayudaría a búsqueda y a auditoría.
- **Lo que fue bien:** el formato P1 del corpus (transcript con ids + frames con
  `cited_by_claim` + `exists` + grounding reasons) permitió auditoría exhaustiva
  one-shot sin re-lecturas; agrupar lecturas de frames por ventana mantuvo el coste bajo
  (~65 Reads para 279 claims).
