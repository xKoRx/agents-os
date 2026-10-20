# change_log — 2026-10-19 · course-knowledge-extraction: fix del contador de normalización `f-.png` en `integrate_reviews.py` (run ch06)

## Cambio

- Skill afectada: `30-resources/agents/skills/course-knowledge-extraction/` (script `scripts/integrate_reviews.py` + test `scripts/tests/integrator_selftest.py`).
- Defecto: el contador "refs f-.png normalizadas" se incrementaba dentro del bucle de merge para toda ref `f-NNNNNN` añadida — ya después de `_normalize_ref()` — por lo que contaba refs ya canónicas como si hubieran sido normalizadas (sobreenumeración sistemática desde su generalización en el run ch05).
- Fix: el conteo se realiza en el punto donde ocurre la normalización (comparación raw→normalizada por `zip`); la lógica de merge queda idéntica (mismo orden, mismos dedups, mismos writes). Sin cambio funcional del comportamiento de integración.
- Test: caso 6 nuevo en `integrator_selftest.py` (un review con `f-000123.png` + `f-000456` canónica ⇒ el stdout debe reportar exactamente `1`). Red verificado contra el código anterior (reportaba 2); green tras el fix. Suite completa: **6/6 PASS**.

## Evidencia (resumen)

- En producción (run ch06, 2026-10-19): `integrate_reviews.py` reportó `refs f-.png normalizadas: 6` sobre 14 reviews — refs con sufijo reales citadas por reviewers.
- `validate_library.py` = PASS y `check_term_sources.py` = PASS sobre la biblioteca `ch06-failure-swing` publicada con el script corregido.

## Notas

- Detectado por el mandato de preflight del run ch06 ("corregir el contador de normalización `f-.png` del integrador mediante un test acotado, sin modificar su comportamiento funcional").
- El defecto afectaba sólo al reporte por stdout (auditoría), nunca a los datos escritos en `claims.jsonl`.
