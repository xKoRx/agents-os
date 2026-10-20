---
type: change_log
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area: "[[Personal]]"
project: "[[Multimodal Knowledge Engine]]"
entities:
  - "[[Multimodal Knowledge Engine]]"
related:
  - "[[course-knowledge-extraction]]"
  - "[[course-knowledge-worker]]"
aliases: []
confidence: high
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change Log — Clutifx Chapter 05 (SMT) publicado + skills endurecidas

- **Entidad actualizada:** `10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/` — nuevo capítulo `ch05-smt/` (biblioteca completa: 100 claims 99 SUPPORTED / 1 UNCERTAIN / 0 superseded, 81 frames, 18 rules / 10 concepts / 7 examples, 10 preguntas abiertas) + `COURSE-INDEX.md`, `GLOSSARY.md` (DXY documentado como término literal de ch05; SMT redefinida) y `METHODOLOGY-FEEDBACK.md` (bloque CH05 OBSERVED/LEARNED).
- **Motivo:** mandato ONE-SHOT de continuar la biblioteca del curso con ep05-smt.mp4 (SHA `072f669d…`, 18:29.7), metodología `course-knowledge-extraction` v1.2+hardening.
- **Delta skills (por delta, sin nueva metodología):** (1) `scripts/integrate_reviews.py` generalizado desde el run ch04 (paths por argumento + normalización de refs `f-XXXXXX.png`, defecto real ch04) + `scripts/tests/integrator_selftest.py` (5 casos; cazó un bug de índice antes de producción); (2) `validate_library.py` V08 extendido: `visual_hint.second` fuera de la duración de la fuente = finding (defecto real ch05: HHMMSS pegado como segundos crudos, 5 casos) + caso red-green G en `fixtures_selftest.py` (11/11); (3) `course-knowledge-worker/SKILL.md`: contrato EXTRACTOR fija `second` en segundos reales por fórmula.
- **Verificación:** probe ASR preflight 0,21× (GO, sin contención); checkpoint 5 min PASS (26/26 VALID); 19/19 `MINUTE_REVIEW = VALID`; `LIBRARY_VALIDATION = PASS` (V+W completos) en ch05 y sin regresión en ch02/ch03/ch04; `TERM_SOURCE_CHECK = PASS` (100 vivos / 0 findings); DOCVERIFY independiente ONE-SHOT: 2 MATERIAL + 3 MENOR, los 5 corregidos in-mission y re-validados. 7/7 selftests PASS.
- **Handoff:** agente wall 143 min/h-video (mejor del curso); ASR 92,5 min sigue siendo la partida dominante (decisión Owner GPU/modelo abierta). Ep06 anunciado ("Felux Swing" [ASR] = failure swing, q-ch05-009). NO se ejecuta Chapter 06.
