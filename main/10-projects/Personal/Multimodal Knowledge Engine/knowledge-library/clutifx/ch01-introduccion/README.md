# ch01-introduccion — Clutifx · Capítulo 1

Biblioteca de conocimiento del primer video del curso Clutifx, extraída con MKE V2.

| Campo | Valor |
|---|---|
| Fuente | `/home/kor/mke/course/ep01-intro.mp4` (sha256 `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b`) |
| Audio→texto | faster-whisper, 323 segmentos, `transcript.json` en el run dir |
| Motor | MKE V2, branch `feature/agent-vlm-provider` @ `5ebc066`, fingerprint `94e44674f03a1b34e6d53ab5198afbdee9ed5001609f9baf56af7429589d66dd` |
| VLM | proveedor de buzón `agent:` (subagentes locales, sin API pagada) |
| Run dir | `/home/kor/mke/clutifx-ch01-agent-20261015/` |
| Fecha | 2026-10-15/16 (run iniciado 2026-10-14) |

## Archivos

- `documentation.md` — síntesis del capítulo por conceptos (rango, pendiente/reiniciado, Turtle Soup, SMT, failure swing, order block, Power of 3), construida SOLO sobre claims con grounding SUPPORTED.
- `claims.jsonl` — 1.894 registros (1.527 claims + 367 relaciones) con su veredicto de grounding (`GROUNDING_SUPPORTED` / `INSUFFICIENT` / `CONTRADICTED` / `UNREVIEWED`), razones y evidencia citada (`evidence_ids` → frames/transcript del run dir).

## Estado del pipeline

RECONSTRUCTION completa (130/130 ventanas). GROUNDING REVIEW al 63% (1.200/1.894) cuando el owner abortó el run. Fases SKO composition y publication NO ejecutadas: `documentation.md` se sintetizó directamente del subconjunto validado. Ver la sección "Estado de la extracción" en `documentation.md` para los números exactos.

## Para regenerar/ampliar

1. El run dir conserva `run-agent/run.db` (journal con las 1.219 invocaciones validadas — replayable) y `spool/` (bundles).
2. Relanzar el pipeline con el mismo comando hace resume por journal y continúa donde quedó (las respuestas del spool se re-consumen por identidad de contenido).
3. Metodología completa: `mke/multimodal-knowledge-engine/docs/runbooks/video-knowledge-exploitation.md`.
