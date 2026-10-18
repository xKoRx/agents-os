# METHODOLOGY-FEEDBACK — Clutifx (Course Intelligence)

Feedback de método del curso Clutifx. Objetivo: mejorar Chapter 03 y los ~200
videos siguientes, no justificar decisiones pasadas. Estado tras la extracción
de Chapter 02 (2026-10-18) y su remediación autorizada por el Owner el mismo
día. La skill canónica quedó en v1.1; NO se toca aquí la decisión de.Owner sobre
ASR.

## OBSERVED (lo medido en Chapter 02, sin corregir)

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

## PROPOSED_FOR_NEXT_CHAPTER (ep03-bias y sucesivos)

1. **Ejecutar el pipeline v1.1 tal cual**: paquetes de worker con
   `course-knowledge-worker/SKILL.md` + ROLE; payload por
   `make_minute_payload.py`; integración con `validate_review.py`; cierre con
   `validate_library.py` = PASS + conteos reconciliados. Nada de esto requiere
   nueva construcción.
2. **Decidir ASR** con un test de 2 minutos (large-v3 beam 5 vs beam 1 vs
   medium) comparado contra el transcript actual de ch02. Ahorro potencial
   ~30–40 min/video. (Decisión Owner.)
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
