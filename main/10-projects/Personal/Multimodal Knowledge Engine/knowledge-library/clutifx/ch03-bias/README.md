# ch03-bias — Clutifx · Capítulo 3

Biblioteca de conocimiento del tercer video del curso Clutifx, extraída con la
metodología `course-knowledge-extraction` (skill canónica del vault, NO el
pipeline MKE V2).

## Identidad de la fuente

| Campo | Valor |
|---|---|
| Archivo | `/home/kor/mke/course/ep03-bias.mp4` |
| SHA-256 | `c52dafa80388fcd89bb9b8f99e71caa6ae27c38eda760c2733baa0a1ff366b37` |
| Duración | 41:50.8 (2.510,8 s), h264 + aac |
| Tema real del capítulo | Cómo se saca el BIAS (la dirección) desde la temporalidad más alta hacia la baja; entradas explícitamente excluidas (capítulo siguiente) |
| Tema | El nombre de carpeta `ch03-bias` replica el nombre del archivo (`ep03-bias`); el instructor anuncia al inicio: "cómo saco el BIAS" [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-000006|s-000006]] |

## Provenance de la extracción

| Campo | Valor |
|---|---|
| Fecha | 2026-10-18 (sesión 15:39–22:00 aprox.) |
| ASR | faster-whisper `large-v3`, int8 CPU, language=es (p=1,00), 506 segmentos, 96 % habla, ligado al SHA; wall 3h18m (0,21× realtime) |
| Preflight | scripts generalizados antes de ejecutar (manifiesto de frames base, renderers deterministas sin fecha, anchors de transcript como bloques Obsidian independientes, checks W05/W09/W10 del validador); `REUSABLE_SCRIPT_PREFLIGHT = PASS` |
| Extracción | 5 subagentes GLM ONE-SHOT en paralelo (bloques 0–8, 8–16, 16–24, 24–32, 32–41:51 min), 211 claims propuestos en ~10,9 min |
| Revisión | 42 subagentes ONE-SHOT — UNA revisión por minuto de video (olas de 5–8 workers), 42/42 `MINUTE_REVIEW = VALID` (cardinalidad exacta) |
| Modelo | GLM (subagentes locales de agente; sin API pagada, sin cambio de modelo) |
| Remediation | 2026-10-18: auditoría DOL/DXY (104 ocurrencias en 20 claims, 0 DXY genuinos), 6 supersessions + 5 correcciones de notas/glosas, q-ch03-001 RESUELTA; ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/AMENDMENTS|AMENDMENTS]] |
| Run dir | `/home/kor/mke/clutifx-ch03-20261018/` |

## Métricas

| Métrica | Valor |
|---|---|
| Claims totales | 217 (211 originales + 6 de la remediation terminológica 2026-10-18) |
| SUPPORTED / UNCERTAIN / UNVERIFIED | 211 / 0 / 0 vigentes (2 UNCERTAIN del review —c-0061 y c-0154— adjudicados en integración; ver las notas de ambos claims) **+ 6 SUPERSEDED** (c-0089, c-0093, c-0116, c-0121, c-0122, c-0123: normalización incorrecta DXY donde la fuente dice DOL — reemplazados por c-0212..c-0217, ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/AMENDMENTS|AMENDMENTS]]) |
| Epistemic | 182 instructor_statement (176 + 6 nuevos) · 35 visual_observation (todas con frame verificado en `evidence`) · 0 model_inference |
| Contradicciones marcadas | 0 |
| Frames base (fin de minuto) | 42 (minutos 0–40 en MM:59.5 + fin del minuto parcial f-004150; manifiesto `frames/.base_frames`) |
| Frames bajo demanda | 79 (extraídos y verificados visualmente por los MINUTE_REVIEWERs, nombres por fórmula desde segundos reales) |
| Referencias visuales sin resolver | ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/OPEN-QUESTIONS|OPEN-QUESTIONS]] (4 preguntas abiertas) |
| Rules / concepts / examples documentados | 18 / 13 / 15 |
| Coverage | 42/42 minutos de video con claims y revisión |
| Checkpoint 5 min | PASS (VALID 5/5; continuar automático) |

## Throughput (reporte separado tramos vs total)

| Tramo | Valor |
|---|---|
| ASR wall | 3h18m (0,21× realtime; partida dominante del total, igual que en ch02) |
| Extracción wall | ~10,9 min (5 subagentes paralelos) |
| Revisión wall | ~146 min (42 revisores, 6 olas de 5–8; incluye verificación visual frame-a-frame del contrato v1.1+) |
| Integración + biblioteca + validación | ~1h (integración por olas, documentación, proyecciones, wikilinks) |
| Agent wall (extracción+revisión) | ~157 min para 41,8 min de video ≈ **225 min/h-video** (objetivo ≤120; banda 2× = 240 → continúa; el exceso viene de la verificación visual por claim y de 42 minutos vs 18 en ch02) |

## Estructura

- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/documentation|documentation]] — síntesis por conceptos, todo citado
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS|CLAIMS]] — proyección navegable por claim (autoridad: `claims.jsonl`)
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript|transcript]] — recurso citable con anchors `^s-HHMMSS`
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/FRAMES|FRAMES]] — inventario de frames
- [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/rules|rules]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/concepts|concepts]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/examples|examples]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/study-guide|study-guide]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/review-notes|review-notes]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/OPEN-QUESTIONS|OPEN-QUESTIONS]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/AMENDMENTS|AMENDMENTS]]
