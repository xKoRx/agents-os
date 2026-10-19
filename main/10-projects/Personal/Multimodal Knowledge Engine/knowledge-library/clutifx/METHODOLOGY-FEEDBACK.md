# METHODOLOGY-FEEDBACK — Clutifx (Course Intelligence)

Feedback de método del curso Clutifx. Objetivo: mejorar los videos siguientes,
no justificar decisiones pasadas. Estado tras Chapter 04 (2026-10-19), que
incluyó el preflight de continuidad (supersession safety + remediation DOL/DXY
de ch02 + hardening SOURCE-FIRST). Los bloques OBSERVED/REPAIRED de Chapters
02/03 se conservan abajo (§Ch03, §Ch02). La skill canónica quedó en v1.2 con
hardening ch03+ch04; NO se toca aquí la decisión de Owner sobre ASR.

## PREFLIGHT (2026-10-19, obligatorio antes de Chapter 04 — PASS 5/5)

- **Supersession safety**: los 6 históricos de ch03 mantenían `verdict: SUPPORTED` y la proyección CLAIMS.md los mostraba como vigentes → contaminación de consultas. Contrato nuevo: GROUNDING_VERDICT (SUPPORTED/…) ≠ LIFECYCLE_STATUS (activo/superseded derivable de `superseded_by`; SIN propiedad redundante). Renderer marca `SUPERSEDED — HISTORICAL, NOT ACTIVE` + `Replacement:` navegable; validador V14 (superseded_by/supersedes bidireccional, sin ciclos), V15 (proyección con lifecycle), V16 (docs pedagógicos sin WIKILINKS a reemplazados — la mención histórica en texto plano es rastro de auditoría permitido), V10 (fila `Claims activos / superseded` obligatoria con reemplazos). Contract tests: `lifecycle_selftest.py` (10 casos). ch03 aplicado: 211/6, VALIDATION PASS.
- **DOL/DXY en ch02**: la remediation de ch03 dejó ch02 intacta "para no tocar sin evidencia"; el preflight la adjudicó con la fuente de ch02: c-0066 y c-0089 publicaban DXY donde la fuente dice "el doble"/"dol" (s-001005/s-001010) y "a por tu dol, perdón, a por tu objetivo" (s-001401) → DOL_CONFIRMED ×2, 2 supersessions (c-0099/c-0100), amend-0003/0004, docs/glosario/índice actualizados. ch03 semánticamente intacto; ch01 intacto.
- **SOURCE-FIRST hardening**: `check_term_sources.py` ahora es case-insensitive en el lado fuente (un "dol" minúscula del ASR cuenta como canónico) y trata los garbles ambiguos ("el doble", "doll", "dole", "dolls") como aliases de grupo: canónico en statement + alias en fuente sin marca `[ASR]` ⇒ `TERM_DISAMBIGUATION_REQUIRED` (REVIEW; el chequeo no decide el término). Selftest 10 casos con los casos REALES de ch03 y ch02. La verificación determinista detecta la necesidad de revisión; el reviewer adjudica.

## CH04 OBSERVED (medido en Chapter 04, sin corregir)

| Métrica | Valor |
|---|---|
| Video | ep04-entradas.mp4 · 27:35.4 · SHA `f69f7d62…` |
| ASR_WALL | **4h10m** (0,11× realtime; máquina compartida con jobs de backtest ~400 % CPU — el rate canónico era 0,21–0,38×; la carga externa dominó el total) |
| EXTRACT_WALL | 15,3 min (6 EXTRACTORs paralelos, 119 claims) |
| REVIEW_WALL | 91,9 min (28 MINUTE_REVIEWERs, 4 olas de 5/7/7/9; verificación visual frame-a-frame) |
| AGENT_WALL | 107,2 min / 27,6 min video ≈ **233 min/h-video** (objetivo ≤120; banda 2× = 240 → continúa; igual que ch03) |
| Claims | 119 (111 SUPPORTED / 8 UNCERTAIN / 0 UNVERIFIED) · 109 instructor_statement (incluye c-0016 adjudicada) + 9 visual_observation · 0 model_inference · 33 con preguntas sin resolver |
| Frames | 28 base + 77 bajo demanda = 105; 97 citados en evidence |
| Revisión independiente (DOCVERIFY) | ver handoff; ejecutada sobre la biblioteca publicada con puntos de contraste SOURCE-FIRST obligatorios |
| Checkpoint 5 min | PASS (21/21 VALID; proyección 152 min/h-video; real 233 — dentro de banda) |

## CH04 LEARNED (para ep05+)

1. **La corrección de statement por el reviewer funciona**: 7 corrections_suggested aplicadas en integración (marcas [ASR], género literal, niveles leídos con zoom); el flujo "reviewer propone, integrador aplica al pool, validate_review por minuto" evitó toda edición manual canónica.
2. **El reviewer puede RECHAZAR evidencia del extractor** (c-0083: frame mostraba 4h, no 1h): la regla "no aceptar un frame que no muestre lo afirmado" operó de verdad; los visual_hints erróneos del extractor (3) quedaron documentados en reasons sin contaminar statements.
3. **Los UNCERTAIN son productivos**: 8/119 (6,7 %) por garbles/deícticos, todos con pregunta abierta trazada (19 q-ch04-*). Mejor dudoso visible que falso SUPPORTED.
4. **Las colas de las olas dominan el makespan**: la ola de 9 tardó ~31 min (los reviewers pesados ~1,5-1,9 h de subagente con muchas lecturas de frames). Para ep05+ considerar despacho por tamaño de payload ya probado en ch03.
5. **El ASR sigue siendo el cuello absoluto** (4h10m para 28 min por carga externa): la decisión Owner (GPU/modelo menor) sigue abierta; con la máquina despejada el rate vuelve a ~0,2-0,38×.
6. **Normalizar refs `f-` en el integrador**: los reviewers escribieron 6 evidencias como `f-XXXXXX.png` (con sufijo); el integrador ahora las normaliza (el fix se hizo post-integración; incorporarlo a integrate_reviews.py).


## REMEDIATION (2026-10-18 noche — DOL/DXY + probe ASR, mandato Primary Manager)

- **Defecto MATERIAL que la verificación documental dejó pasar**: c-0121 publicaba "al DXY" donde la fuente dice "al DOL" (s-002201 literal). Causa raíz: el glosario mapeaba el garble "el doble/dol" a DXY globalmente y extractores/revisores lo trataron como permiso de sustitución. Auditoría completa: 104 ocurrencias en 20 claims — **0 menciones genuinas de DXY en ch03**; el término del capítulo es DOL (s-001229 "el tema DOL" literal, pizarra f-004059).
- **Corrección con contrato de identidad V1.2**: 6 supersessions (c-0089→c-0212, c-0093→c-0213, c-0116→c-0214, c-0121→c-0215, c-0122→c-0216, c-0123→c-0217 — el statement publicado cambió de referente ⇒ claim nuevo + anterior superseded sin renumerar), 2 glosas inline retiradas in-place (c-0144, c-0184), notas corregidas (c-0055, c-0074, c-0080, c-0142, c-0146, c-0208, c-0031), q-ch03-001 RESUELTA, 12 amendments. ch02 NO se toca (sus lecturas DXY quedan como publicadas; el glosario queda desambiguado).
- **Contrato nuevo (skills)**: TERM_DISAMBIGUATION_REQUIRED — el statement publica la palabra dicha ([ASR]), la interpretación vive en notes; que el glosario liste una equivalencia NO la respalda. Chequeo SOURCE-FIRST determinista `check_term_sources.py` + `source_first_selftest.py` (el caso 1 es el defecto real) + obligación SOURCE-FIRST en DOCUMENTATION_VERIFIER (docs↔claims no basta: ambos pueden contener el mismo error).
- **Verificación independiente post-remediation**: 2 MATERIAL (c-0116 citado como vivo en documentation; c-0080 con nota DXY no cubierta) + 6 MENOR (numeración de amendments intercambiada en notes, FRAMES.md desincronizada, rangos de examples, remanentes DXY en review_reasons, evidence de c-0217 sin s-002215, q-ch03-001 con claim inexistente) — los 8 corregidos in-mission; re-validado (LIBRARY_VALIDATION PASS, TERM_SOURCE_CHECK PASS 211 vivos / 0 findings).
- **Lección de proceso**: el DOCVERIFY del run original contrastó docs↔claims (coherencia interna) pero no claims↔fuente (verdad). El SOURCE-FIRST es ahora mandatorio; el caso real quedó como contract test.

## ASR PROBE (2026-10-18, acotado — 36,9 min de presupuesto 45)

- 6 fragmentos × 28 s (168 s) con términos/garbles, negaciones, números/TFs y DOL/doble. A = large-v3 beam5: 1161s (0,14× fragmento) · B = beam1: 970s (0,17×) · C = medium NO EJECUTADO (no cacheado; descarga prohibida por mandato).
- Calidad: aciertos idénticos 72 % (31/43) con las MISMAS ausencias en A y B; "DOL" 3/6 en ambos; "DXY" 0/6 en ambos (correcto). Las ausencias se explican por cortes de ventana/VAD, no por beam.
- **ASR_RECOMMENDATION = KEEP_LARGE_V3_BEAM5**: beam1 sólo 1,20× más rápido (≈3 min/h de audio) — nada del 2-5× esperado — y sin medición de comportamiento full-audio. Nota: los benchmarks por fragmentos subestiman el throughput (0,14-0,17× vs 0,21× full-run) por reinicios de VAD/contexto. La palanca real sigue siendo modelo/GPU (decisión Owner).
- Detalle: `/home/kor/mke/clutifx-ch03-20261018/asr-probe/` (RECOMMENDATION.md, verdict.json, probe-report.json).

## CH03 OBSERVED (medido en Chapter 03, sin corregir)

| Métrica | Valor |
|---|---|
| Video | ep03-bias.mp4 · 41:50.8 · SHA `c52dafa8…` |
| ASR_WALL | **3h18m** (0,21× realtime; más lento que ch02's 0,38× — 96 % de habla y 506 segmentos) — partida dominante |
| EXTRACT_WALL | 10,9 min (5 EXTRACTORs paralelos, 211 claims) |
| REVIEW_WALL | ~146 min (42 MINUTE_REVIEWERs, 6 olas de 5–8; cada revisor extrae y verifica visualmente sus frames) |
| AGENT_WALL (extracción+revisión) | ~157 min / 41,8 min video ≈ **225 min/h-video** (objetivo ≤120; banda 2× = 240 → continúa; el exceso viene de la verificación visual frame-a-frame del contrato v1.1+) |
| Claims | 211 (todos SUPPORTED; 2 UNCERTAIN del review adjudicados en integración con nota) · 176 instructor_statement + 35 visual_observation · 0 model_inference |
| Frames | 42 base + 79 bajo demanda = 121; 74 citados en evidence |
| Revisión independiente (DOCVERIFY) | 0 MATERIAL + 5 MENOR (conteos y citas cruzadas), todos corregidos in-mission |
| Checkpoint 5 min | PASS (30/30 VALID; proyección inicial ~80 min/h-video subestimó las olas reales de ~13 min) |

## CH03 REPAIRED (defectos de contrato encontrados en vuelo, con prueba)

- **`make_minute_payload.py` emitía `id` pero `validate_review.py` esperaba `key`** (y los reviewers v1.2 devuelven `claim_key`): el checkpoint lo cazó antes de dañar nada. Fix en ambos helpers + test de regresión nuevo `scripts/tests/review_pipeline_selftest.py` (5 casos, rojo-verde).
- **Frame base del minuto parcial**: la captura usa el fin real del video (f-004150 a 41:50.5); sin regla de nombre: lo decide el manifiesto.
- **Naming de frames a mano falla**: el integrador generó `f-00059` (5 dígitos) por concatenación manual en el primer lote; re-hecho con la fórmula. Confirma el contrato: SIEMPRE fórmula desde segundos reales, jamás printf a mano.
- **V11 es chapter-local**: los refs `s-` de OTRO capítulo en los docs disparan V11 falso-positivo. Los W-checks sí los resuelven (cross-file). Para ch04: citar cross-chapter con enlace a archivo + timestamp en la etiqueta (o extender V11 si Owner lo quiere).
- **5 MENOR del DOCVERIFY** corregidos: conteos README (preguntas abiertas 3→4; UNCERTAIN adjudicados 1→2), cita de ch02 atribuida a claim inexistente (→ segmentos reales sin claim, declarado), 4 frames listados en examples sin citación real (→ quitados), fórmula de rango atribuida al claim equivocado (→ c-0118/c-0100).

## CH03 LEARNED (para Chapter 04)

1. **ASR sigue siendo el cuello** (3h18m para 42 min de video): el test de 2 min (beam 1/medium vs large-v3) sigue en PROPOSED-2 esperando decisión Owner. Con ep04 (~similar duración) el ahorro potencial es >1 h/video.
2. **La verificación visual frame-a-frame es el nuevo centro de costo del review** (146 min vs 19,8 en ch02 por 2,3× video): es el precio del provenance visual v1.1+ y compró 35 visual_observation con frame verificado y 0 MATERIAL en el DOCVERIFY. Alternativa a proponer a Owner: reviewers SIN extracción propia (sólo transcript + base frame) + una sola pasada visual del integrador sobre los visual_hints; medir calidad antes de adoptar.
3. **Olas de 8 con colas de 14–16 min desperdician paralelismo**: despachar por tamaño de payload (claims×segmentos) en vez de por minuto reduces el makespan.
4. **El glosario de garbles por capítulo funciona**: ~10 garbles nuevos de ch03 ya están en review-notes para reutilizar en ch04 (ep04-entradas reutilizará el vocabulario DOL/bias/rangos).
5. **Integración por olas en background** (reviewers async + integración del integrador entre olas) funcionó sin bloquear: mantener.

## Ch02 OBSERVED (medido en Chapter 02, sin corregir)

| Métrica | Valor |
|---|---|
| Video | ep02-time.mp4 · 17:09 · SHA `fb8b3de4…` |
| OWNER_OBSERVED_ELAPSED | **2h06m** (medida del Owner; autoridad para el total end-to-end) |
| AGENT_RECONSTRUCTED_ELAPSED | ≈1h40–1h50 (02:54–04:35, mtimes/epoch) — la diferencia es ventana de observación + overhead de orquestación; se reportan ambas |
| ASR_WALL_TIME | 45,1 min (faster-whisper large-v3 int8 CPU, 0,38× realtime) — partida dominante |
| EXTRACTION_WALL_TIME | 8,6 min (3 subagentes ONE-SHOT paralelos) |
| REVIEW_WALL_TIME | 19,8 min (18 subagentes, olas 5/7/6) |
| INTEGRATION_WALL_TIME | ~20 min (primera publicación) + ~35 min (remediación P1–P10) |
| Subagentes | 21 (extracción+revisión) + 3 auditores visuales + 1 revisión independiente + 1 verificación documental |
| Claims | 98 (4–9/min) · frames 18 base + 47 demanda · 65 archivos |
| Throughput subagentes (extracción+revisión) | ~28,4 min / 17,2 min video ≈ 99 min/h-video (objetivo ≤120 ✓) — NO es el tiempo end-to-end |
| Hallazgos del Owner sobre la primera publicación | 6 (provenance visual, naming, conteos README, wall time, c-0066, c-0056) — todos reproducidos 1:1 desde los archivos |

## REPAIRED (verificado, con prueba)

- **Provenance visual estructurada**: los claims visuales citaban solo transcript;
  tras auditar físicamente 41 claims (27 visual_observation ∪ 38 visual_hint),
  `claims.jsonl.evidence` contiene 48 refs a frames verificados (antes 0).
  23/23 visual_observation con frame; epistemic realmente cambiada en 5 claims
  (4 visual_observation→instructor_statement + 1 model_inference→instructor_statement;
  41 auditadas, 36 con frames — errata B3 en repair/REPAIR-LOG).
- **Naming de frames**: f-170903→f-001703 + 5 históricos declarados en
  `.deprecated_frame_names` (el validador distingue `historical_invalid_name`
  de cita vigente). 65/65 nombres canónicos y dentro de duración.
- **Conteos reconciliados**: README (14/13) vs artefactos (16/17) resuelto —
  README = artefactos en claims/veredictos/rules/concepts/examples/frames.
- **Wall time**: el reporting distingue OBSERVED (owner, 2h06) de tramos del
  agente; el README ya no presenta los 28,4 min como tiempo total.
- **c-0066**: adjudicación A — el condicional DXY es textual del instructor →
  `instructor_statement` (era `model_inference`+SUPPORTED, inaceptable tal cual).
- **c-0056**: deíctico de 8h resuelto con comparación de estados
  (f-000758/f-000806, rango válido 1,4748–1,5803); matiz del borde inferior del
  rectángulo descartado conservado en la nota.
- **Validador determinista** (`scripts/validate_library.py`, V01–V13) +
  cardinalidad de reviews (`validate_review.py`, R01–R04) + payload builder con
  contexto de frontera (`make_minute_payload.py`) + selftest 10/10. RED capturado
  antes de reparar; `LIBRARY_VALIDATION = PASS` después.
- **Skills**: principal en **v1.2** (v1.1: 7 contratos; v1.2 mismo día: navegación
  Obsidian, proyecciones deterministas CLAIMS/FRAMES, identidad permanente,
  AMENDMENTS/OPEN-QUESTIONS, aclaración acotada, consulta por agentes, checks W);
  `course-knowledge-worker` (EXTRACTOR / MINUTE_REVIEWER / DOCUMENTATION_VERIFIER,
  spool-only, cardinalidad obligatoria, unresolved_questions, modalidad targeted)
  registrada en el INDEX federado.
- **Revisión independiente (P10)**: 10/10 puntos sustantivos PASS; 3 findings de
  registro (1 MATERIAL de libro de conteos, 2 MENOR editoriales) corregidos
  in-mission y re-validados.

## REMAINING (abierto, honesto)

1. **ASR local lento** (45 min/video en CPU): sin decidir. Opciones ya
   identificadas (beam 1, modelo menor, GPU); requiere decisión Owner porque
   cambia la herramienta de transcripción.
2. **c-0056**: el borde inferior del rectángulo descartado (~zona 1,52) se lee
   de un still en pleno dibujo — consistente, no probado como caja completa.
3. **c-0059 y c-0070**: visual_hints sin frame (sustancia hablada; los frames
   candidatos se inspeccionaron y no muestran lo afirmado). Aceptables como
   contexto; si el Owner los quiere visuales, habría que redibujar/demostrar en
   el video — no hecho.
4. **Epistemic en extracción**: las 5 reclasificaciones post-hoc eran evitables si
   los extractores aplicaran la distinción instructor/visual/inferencia con más
   rigor al proponer (el glosario y la v1.1 lo piden; no verificado en un run
   nuevo).
5. **`documentation-verifier` agent type no disponible en esta cuenta**
   (provider zai-start-plan ausente): las verificaciones se ejecutaron con
   `general-purpose` + prompt adversarial. Gap de plataforma, no de método.

## PROPOSED_FOR_NEXT_CHAPTER (ep04-entradas y sucesivos)

1. **Ejecutar el pipeline v1.2+hardening ch03 tal cual**: paquetes de worker con
   `course-knowledge-worker/SKILL.md` + ROLE; payload por
   `make_minute_payload.py`; integración con `validate_review.py`; cierre con
   `validate_library.py` = PASS + conteos reconciliados. Nada de esto requiere
   nueva construcción.
2. **Decidir ASR** con un test de 2 minutos (large-v3 beam 5 vs beam 1 vs
   medium) comparado contra el transcript actual de ch02/ch03. Ahorro potencial
   >1 h/video (ch03: 3h18m de ASR para 42 min). (Decisión Owner, sigue abierta.)
3. **Presupuesto de frames por bloque** declarado en el paquete según densidad
   visual estimada (recorrido de gráfico ⇒ más que 1/min), con exceso
   justificado en review-notes (ya es contrato v1.1; aplicar el presupuesto
   inicial desde la planificación).
4. **Epistemic estricta en EXTRACTOR**: si el statement se sostiene con citar al
   instructor, es `instructor_statement`; `visual_observation` sólo si la
   sustancia requiere mirar el gráfico; `model_inference` nunca llega a
   SUPPORTED sin adjudicación explícita (V13 lo bloquea).
5. **MINUTE_REVIEWER devuelve `verified_evidence` completo** (s- y f-), de modo
   que la integración de evidencia sea mecánica y no requiera segunda auditoría
   visual (en ch02 hizo falta una ronda P1 completa).
6. **Mantener**: checkpoint doble a los 5 min (subagentes vs total), revisión
   POR MINUTO (nunca por claim), adjudicaciones documentadas en el claim,
   `repair/` con baseline+log por capítulo.
