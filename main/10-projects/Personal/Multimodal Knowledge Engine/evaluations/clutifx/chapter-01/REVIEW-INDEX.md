# REVIEW-INDEX — Clutifx Chapter 01 (run BLOCKED en L1)

Source SHA-256: `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b` · duración 34:03.9 · MKE `cc13a121` · live `openrouter`/`stealth/space-bunny-alpha`

**Estado: no existe conocimiento publicado.** El pipeline live terminó FATAL (exit 5) durante el commit de candidatos de la ventana w0003, por el contrato de identidad de registro (S2-B-01): `cl-chart-instrument-eurusd@1` propuesto por w0002 y w0003 con contenido divergente. Este índice documenta lo que el run produjo físicamente: 3 reconstrucciones VALIDATED con sus proposals **no committeados** (no son knowledge canónico), y el par divergente exacto.

## Cronología física del run L1

| Ventana | Invocación | Estado | Claims prop. | Rel. prop. | Tokens |
|---|---|---|---|---|---|
| `w0001` | `2a411cc4f1706926…` | VALIDATED (proposal no committeado) | 11 | 1 | 28162 |
| `w0002` | `d166a548bd273d4c…` | VALIDATED (proposal no committeado) | 31 | 2 | 39922 |
| `w0003` | `e05318c662138cd1…` | VALIDATED (proposal no committeado) | 14 | 1 | 32639 |

## El par divergente (causa del FATAL)

Mismo `id@version` propuesto por dos ventanas consecutivas; la igualdad de contenido incluye `evidence_ids`, que son window-locales:

**w0002 (frame t=00:12):**
```json
{
 "id": "cl-chart-instrument-eurusd",
 "kind": "parameter",
 "statement": "The displayed chart instrument is EUR/USD.",
 "epistemic": "VIDEO_OBSERVED",
 "evidence_ids": [
  "frame-4de8f12d4841c630-s0-p1080000-canonical-v1"
 ]
}
```
**w0003 (frame t=00:37):**
```json
{
 "id": "cl-chart-instrument-eurusd",
 "kind": "parameter",
 "statement": "The displayed chart instrument is EURUSD.",
 "epistemic": "VIDEO_OBSERVED",
 "evidence_ids": [
  "frame-4de8f12d4841c630-s0-p3330000-canonical-v1"
 ]
}
```
Error textual del engine: `record cl-chart-instrument-eurusd@1 was committed twice with divergent content (window w0002, then window w0003): same id/version with different content is corruption, never a silent replacement` (exit 5, ClassFatal, sticky).

## Proposals por ventana (contexto de revisión; NO son canonical claims)

Las respuestas completas están en `provider-requests.jsonl` (task `claims.reconstruction`) y en el journal del run local. Distribución agregada de los 56 claims propuestos:

- kinds: {'claim': 20, 'parameter': 16, 'procedure_step': 3, 'observation': 14, 'rule': 3}
- epistemic: {'INSTRUCTOR_SAID': 26, 'VIDEO_OBSERVED': 30}
- idioma de statements (heurística): {'other': 1, 'es-like': 10, 'en': 45} — el modelo escribió mayoritariamente en inglés sobre contenido en español; el prompt congelado no declara política de idioma
- evidencia citada: {'asr': 26, 'frame': 54}
