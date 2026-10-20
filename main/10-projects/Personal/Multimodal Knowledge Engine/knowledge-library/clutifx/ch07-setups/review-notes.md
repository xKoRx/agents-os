# review-notes — Clutifx Chapter 07 (Setups)

Notas de revisión y decisiones del run. Autoridad de claims: `claims.jsonl` ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS|CLAIMS]]).

## ASR y provenance

- faster-whisper large-v3 int8, es (p=1,00), beam 5, **480 segmentos, 98 % de habla** (el capítulo más denso del curso), ligado al SHA `b20ce8f7…`.
- **ASR interrumpido por doble reboot del host** (intento 1, 09:51–~15:10, murió sin transcript); relanzado 17:01, **68,3 min (0,68× realtime — el rate más rápido del curso; máquina despejada post-reboot)**. Sin duplicación de proceso (verificado: sin transcript.json + log cortado antes de relanzar).
- Garbles nuevos del capítulo registrados en el context-pack y el GLOSSARY (pablo frida/PowerCity, load/logo/lobo/bajo→low, "el todo claro", vela del circo, Felucion, pechazo, trailer, "durante el hondo", veris, TAS del SUPE…).

## Ejecución híbrida por agotamiento de cuota del proveedor (FALLBACK REGISTRADO)

- Ola 1 (min 0–4, checkpoint) y ola 2 (min 5–14) + minutos 16–18 y 21–24: **23 minutos revisados por subagentes ONE-SHOT** (general-purpose con prompt de MINUTE_REVIEWER), 46 frames verificados visualmente por ellos.
- A las ~19:00 el proveedor devolvió `[1310] Weekly/Monthly Limit Exhausted` (reset 2026-10-25) en los reintentos de los minutos 15/19/20; se aplicó el **fallback documentado**: el integrador (este agente, que no fue extractor) ejecutó el rol MINUTE_REVIEWER inline para los 23 minutos restantes (15, 19, 20, 25–45) con el mismo contrato: SOURCE-FIRST contra transcript, extracción de frames bajo demanda por fórmula, verificación visual vía análisis VLM de imagen, cardinalidad validada por `validate_review.py`. Independencia extractor/revisor preservada (el integrador jamás extrajo claims).
- El DOCVERIFY también corre en modo fallback (ver sección final) por la misma causa.

## Decisiones de revisión notables

- **c-0170 (frame de transición)**: el revisor cazó que f-003302 (33:02) muestra GBPUSD 15M — el instructor aún no cambiaba a EUR; se citó f-003328/f-003336 en su lugar y el visual_hint se movió a 2008s. Regla "no aceptar un frame que no muestre lo afirmado" operando (tercera vez en el curso).
- **Re-adjudicación honesta de epistemic**: c-0167 (visual_observation→instructor_statement, sustancia hablada + frame corroborativo) — patrón P1 de ch02/ch05.
- **s-000331** ("más claro"/"menos claro"): el revisor lo dejó ABIERTO (q-ch07-009) en vez de resolver por contexto — correcto: la palabra hablada no es verificable por frame.
- **Defecto de naming cazado in-flight**: el integrador generó 5 frames con nombre concatenado a mano (f-00321935.png…), detectados y eliminados inmediatamente, regenerados por fórmula Python. Nunca citados ⇒ sin entrada en `.deprecated_frame_names` (no son citas históricas, fueron archivos efímeros de un mismo cambio).

## Correcciones aplicadas en integración (reviewer propone, integrador aplica)

28 `corrections_suggested` de los revisores aplicadas vía pool: 8 adiciones de evidence (frases que cruzan segmentos: c-0004, c-0028, c-0061, c-0064, c-0067, c-0068, c-0117, c-0126), 12 ajustes de literalidad de statement (persona gramatical c-0003/c-0036/c-0037, deícticos c-0006, hedges c-0009, marcas [ASR] c-0021/c-0096/c-0129, truncamiento con candidato c-0035, aparte reorganizado c-0063, matiz del cierre-fuera c-0064, literales c-0047/c-0048), 7 refinamientos de visual_hint (c-0004, c-0025, c-0029, c-0033, c-0034, c-0045, c-0170) y 1 re-adjudicación de epistemic (c-0167). Sin edición manual de `claims.jsonl` fuera del integrador.

## Cobertura y presupuesto de frames

- 46 frames base (minuto 0–44 en MM:59.5 + parcial f-004535) reutilizados del intento original (manifiesto `frames/.base_frames`).
- **80 frames bajo demanda** extraídos y verificados visualmente (46 por revisores subagente, 34 por el integrador-revisor); **64 citados** en `claims.jsonl.evidence`; total 126 PNG. Densidad 2,8/min (capítulo con recorrido de gráfico continuo y esquemas — presupuesto por bloque declarado, exceso justificado: el instructor cambia de TF/gráfico constantemente).
- 12 visual_observation con frame verificado en evidence (V07/V08 satisfecho).

## Throughput (epochs reales)

| Tramo | Valor |
|---|---|
| ASR_WALL | 68,3 min (0,68× realtime; intento 1 perdido por reboot no contado) |
| EXTRACTION_WALL | 11 min (6 EXTRACTORs paralelos, 238 claims) |
| REVIEW_WALL | 45 min (18:27→19:12): ola 1 checkpoint 9 min (5 revisores), ola 2 ~15 min (10 revisores), resto híbrido subagente+integrador tras el agotamiento de cuota |
| INTEGRATION_WALL | ~20 min (correcciones vía pool + integrador + proyecciones) |
| AGENT_WALL (extracción+revisión) | ≈56 min para 45,6 min de video ≈ **74 min/h-video** (objetivo ≤120 → PASS; el mejor del curso) |

## Verificación documental independiente (DOCVERIFY) — fallback

El agente documentation-verifier no está disponible (provider ausente) y los subagentes general-purpose quedaron fuera por cuota agotada. Ejecutado por el integrador en modo adversarial: (1) `check_term_sources.py` = PASS (238 vivos / 0 MATERIAL / 0 TERM_DISAMBIGUATION_REQUIRED — todos los términos normalizados del statement están dichos en la fuente o preservados con [ASR]); (2) contraste SOURCE-FIRST puntual de los términos de la familia DOL contra sus segmentos (los canónicos publicados sin [ASR] — "dol" s-000518, "DOL" s-002110 — son literales); (3) validación de navegación completa `validate_library.py` = PASS (0 findings) incluyendo checks W (links a archivos/headings/blocks, proyecciones sincronizadas, FRAMES.md). Limitación registrada: la revisión semántica docs↔claims corrió sin contraparte subagente independiente; el Owner puede pedir un DOCVERIFY subagente cuando la cuota se restablezca (2026-10-25).
