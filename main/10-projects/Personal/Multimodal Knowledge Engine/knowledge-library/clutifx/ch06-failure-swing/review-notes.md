# review-notes — Clutifx Chapter 06 (Failure Swing)

Notas de la revisión por minuto (14/14 `MINUTE_REVIEW = VALID`) y del proceso. Estado final: **64 claims: 64 SUPPORTED / 0 UNCERTAIN / 0 UNVERIFIED** · 62 instructor_statement + 2 visual_observation · 0 model_inference.

## ASR y provenance

- ASR: faster-whisper large-v3 int8 CPU (beam 5, es p=1,00), 167 segmentos, 97 % habla, ligado al SHA. Wall **59,5 min (0,23× realtime)** — rate canónico, con el grind r5 de Echo en la máquina (load ~10/24 cores) sin degradar el rate.
- Preflight corrigió el contador de normalización `f-.png` de `integrate_reviews.py` (contaba toda ref f- añadida; ahora sólo las que traían sufijo) con `integrator_selftest.py` **6/6** (caso nuevo 6). En producción el contador reportó **6 refs normalizadas reales** (los reviewers citaron 6 refs con `.png`).

## Decisiones de revisión notables

- **El término se dice literal y garbleado a la vez**: "failure swing" literal ×16 (s-000000 apertura, s-000249, s-000627, s-000937/945/948, s-001058, s-001247, s-001258, s-001301…) y garbles "fellow swing" ×13 + variantes "felo", "celu", "pelo(s)", "Fearless", "Finishing", "pelos wings". La lectura failure swing de TODOS los garbles está respaldada por literales del mismo capítulo; los statements preservan la palabra dicha con [ASR] y la adjudicación vive en `reason`/notas (contrato v1.2). Esto resuelve q-ch05-009 ("Felux Swing" = failure swing) por evidencia directa.
- **Garbles de SMT**: "es sentir", "S&T", "ahí sentí", "sentir" → lectura probable SMT, respaldada por "SMT" literal en s-000547; el deíctico de c-0018 ('ahí sentí') no confirmable por frame → queda en unresolved (q-ch06 — ver OPEN-QUESTIONS).
- **Brokers resueltos con fuente visual**: "PPR" [ASR] → 'Pepper' (Pepperstone) por la anotación FOREXCOM/FXCM/PEPPER/OANDA en f-000459 y la entrada PEPPERSTONE del diálogo de símbolos; "forex con" [ASR] → Forex.com y "fxm" [ASR] → FXCM por la misma lista (confirmación parcial: lista en pantalla, no audio). "bloque" [ASR] → ¿broker? queda ABIERTO (q-ch06-005).
- **"logo"/"load" [ASR] → low**: el propio transcript usa "low" literal en s-000923/s-000926; en c-0039 el reviewer restauró la marca [ASR] en la segunda aparición que el extractor había normalizado sin marca.
- **c-0011 (negación clave capturada)**: "que veas un alto al final de la hora NO significa que tenga que pasar un failure swing. No" — el extractor la enunció como warning y el reviewer la confirmó; es la contrapartida de la regla R8 y evita la lectura causal inversa.
- **Corrección de visual_hint (c-0008)**: el hint apuntaba a 159 s donde la etiqueta 'SMT' ya no es visible; el reviewer la verificó en ~124–132 s y el integrador fijó `second: 128` (f-000204/f-000212). La medición "0.00017/0.01%" que dictó el ASR no es legible en ningún frame → eliminada del hint y registrada como no verificada (q-ch06-012).
- **Hedge restaurado (c-0040)**: "El instructor cree que…" — el extractor había publicado la creencia como hecho; el reviewer exigió el hedge dicho.
- **Deícticos preservados**: c-0029/c-0030/c-0050 pasaron de glosas interpretativas a la deixis literal con bracket [deíctico…]; los deícticos del trade final de c-0058 (726–746 s) quedaron sin frame (hueco entre bases) → q-ch06-010.
- **Frames descartados/no citados**: f-001327 es el fade negro del cierre (base de minuto 13, no citable como contenido); ningún reviewer lo citó como evidencia.

## Correcciones aplicadas en integración (reviewer propone, integrador aplica)

10 `corrections_suggested` revisadas y aplicadas: c-0008 (visual_hint.second 159→128 + medición no verificada fuera del hint), c-0012 (nota de atribución del garble a s-000300; s-000249–253 dicen "failure" literal), c-0020 (texto literal de la unresolved PPR→Pepper con respaldo visual), c-0029 y c-0030 (deixis literal), c-0033 (s-000713 añadido — ya fusionado por verified_evidence), c-0035 (glosa "(en esa temporalidad)" fuera + "vais a ver" literal), c-0039 ('logo' [ASR] en su 2.ª aparición), c-0040 (hedge "El instructor cree que"), c-0050 (deixis + 'a pistas' [ASR] + cita textual).

## Cobertura y presupuesto de frames

- Coverage: **14/14 minutos** con claims y revisión; 64 claims (4,6/min; máx 8 en min 5).
- Frames: 19 (14 base: minutos 0–12 en MM:59.5 + fin del parcial f-001327, negro; 5 bajo demanda: f-000204, f-000212, f-000239, f-000419, f-001002 — nombres por fórmula, verificados visualmente). 17 frames citados por claims. Presupuesto declarado por bloque: capítulo de pizarra con esquemas rotulados (FINAL DE VELA, lista de brokers) — demanda concentrada en min 2 y min 10.

## Throughput

| Tramo | Valor |
|---|---|
| Extracción wall | 10,6 min (3 EXTRACTORs paralelos: 20+28+16 claims) |
| Revisión wall | ~11,5 min (ola 1: minutos 0–4, 5 revisores, 5,3 min; ola 2: minutos 5–13, 9 revisores en paralelo, ~8,5 min) |
| Agent wall (extracción+revisión) | ≈22 min para 13,5 min de video ≈ **98 min/h-video** (objetivo ≤120 → PASS; mejor capítulo del curso; ch05: 143) |
| Checkpoint 5 min | PASS (20/20 VALID; proyección ~140 min/h-video con olas de 5 → mejorada con ola única de 9) |
