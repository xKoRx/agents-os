# P8 Final Audit — A4 (worker FULL-CLAIM-AUDIT, ventanas w0100–w0130)

Candidato auditado: run **rerun @ 19b44c1** (`/home/kor/mke/clutifx-ch01-rerun-20261003/run-rerun/claims.jsonl`).
Alcance: **todas** las ventanas aceptadas del rango w0100–w0130. Excluidas por rechazo (otro worker): w0111, w0122, w0127, w0128.

## Cobertura
- Ventanas aceptadas auditadas: **27** (w0100–w0110, w0112–w0121, w0123–w0126, w0129, w0130).
- Claims auditados: **261 / 261** (100%, sin muestreo). Un row por claim en `FULL-CLAIM-AUDIT-A4.jsonl`.
- Verificación visual: **~60 frames PNG leídos** con Read (todos los claims visuales y todos los de nivel de precio fino), además del transcript completo de las 27 ventanas.

## Distribución de labels
| Label | n |
|---|---|
| CORRECT | 233 |
| DUPLICATE | 22 |
| PARTIAL | 5 |
| WRONG | 1 |
| OVERGENERALIZED | 0 |
| UNVERIFIABLE_FROM_AVAILABLE_EVIDENCE | 0 |
| **Total** | **261** |

## Precisión material parcial
- Claims MATERIAL=YES: **172**.
- CORRECT+DUPLICATE sobre MATERIAL=YES: **168/172 = 97.7%**.
- Desglose del 2.3% restante: 1 WRONG material, 3 PARTIAL material (3 PARTIAL más son material=NO, por terminología ASR «Felur Swing» en meta de curso).

## MISSING-KNOWLEDGE
- **MISSING_MATERIAL: 0** (`MISSING-KNOWLEDGE-A4.jsonl` vacío). El transcript+frames de las 27 ventanas está representado en el store: failure swing (definición y causas), order block (identidad, usos, entradas long/short tras cierre por fuera), divergencia de lows entre brokers (FOREX.com vs FXCM/otro broker), change of delivery, Power 3 (apertura-manipulación-distribución-cierre, vela 4H, 0100/0500 NY, compras ideales en manipulación, rango alcista durante el Power 3) y la lógica de las herramientas de posición con todos sus niveles.

## REGRESSION WATCH (obligatorio)
Claim viejo WRONG material: `cl-cambio-oferta-demanda-termino-ingles` (w0106, «change instead of delivery» → falso término «cambio de oferta y demanda» en inglés; contaminaba 2 records como PARTIAL).

**Veredicto: FIXED.**
- El claim viejo **no existe** en el rerun (verificado contra `claims.jsonl` completo: 0 hits por id; 0 hits de la cadena «oferta y demanda» en todo el store).
- El conocimiento está representado y publicado en dos records candidatos de w0106, ambos verificados contra transcript+frames por este auditor:
  - `cl-change-of-delivery-similar-to-trend-change` (w0106, SUPPORTED_BY_AUTOMATED_REVIEW): normaliza el garble ASR «change instead of delivery» al término real **«change of delivery»** y conserva la glosa «sería como el cambio de tendencia un poco» (asr-00233/00234).
  - `cl-order-block-important-for-change-of-delivery` (w0106, SUPPORTED_BY_AUTOMATED_REVIEW): asociación order block ↔ change of delivery (asr-00230–00233).
- No se aceptó un mero borrado: el par de records cubre la proposición errónea original y su contexto.

## Hallazgos notables
1. **Único WRONG material: `cl-rango-nivel-inferior-112695` (w0103)** — afirma que el nivel inferior del rango dibujado es 1,12695. Los frames muestran que la línea inferior se ancla en el low del rectángulo negro (~1,12634/1,12641; ver p143640000, y zoom p146520000 con eje 1,12634–1,12648); 1,12695 es un nivel distinto y superior. Cita además un solo frame cuya etiqueta cercana es otra. Requiere corrección del valor (p. ej. 1,12634) o reclasificación. Nivel superior hermano (`cl-rango-nivel-superior-113976`) sí es correcto.
2. **13 falsos negativos del reviewer automático**: claims que este auditor verifica como CORRECT/DUPLICATE contra fuente pero que quedaron sin publicar como SUPPORTED — 10×UNSUPPORTED_INSUFFICIENT (p.ej. `cl-entrada-posicion-corta-114697` w0115, con veredicto malformado schema v2/v1; `cl-stop-final-long-114521` w0115, soportado por la secuencia completa de frames; `cl-eurusd-impulso-114550-116200` w0119, soportado por p163260000 de la misma ventana), 1×UNSUPPORTED_CONTRADICTED (`cl-second-rectangle-color-change` w0102: la transición negro→blanco sí ocurre, p142650000→p142830000; el par citado solo mostraba el estado final), 1×UNSUPPORTED_REVIEW_UNAVAILABLE (fallo de infra del VLM). Coste: conocimiento correcto fuera de publicación, ~5% de las ventanas del rango.
3. **Terminología ASR inconsistente entre ventanas contiguas**: w0100 normaliza «failure swing», pero w0101 propaga el garble «Felur Swing» en 5 claims (3 materiales marcados PARTIAL: `cl-felur-swing-direct-up-move`, `cl-felur-swing-range-created`, más 2 meta). Mismo patrón que el error de regresión ya corregido en w0106. Menor: «25» como timeframe alternativo (w0116/w0117) es fiel al ASR pero sospechoso de ser garble de «15».
4. **Redundancia sistémica benigna**: 22 DUPLICATE, casi todas re-observaciones del mismo diagrama persistente (etiquetas 0100/0500/4 HORAS re-almacenadas en w0121→w0125→w0129→w0130) y re-emisiones de la misma regla desde segmentos ASR compartidos entre ventanas solapadas (p.ej. regla long-tras-cierre en w0113/w0114, compras-ideales en w0123/w0124, timeframes 10/25/30 en w0116/w0117).
5. **5 PARTIAL**: 3 por terminología «Felur Swing» (w0101), 1 inferencia sin respuesta en su ventana (`cl-lower-entry-better-for-long` w0124; la respuesta canónica sí está en w0125 `cl-entrada-preferida-power-3-nueva-vela`), 1 debilidad de citación con contenido correcto (`cl-apertura-0100` w0123).
6. **Artefactos de LLM en grounding reasons** (no en statements): caracteres corruptos tipo «密密麻麻_identifican», «俯xj», «expressionan», «Lasequentialidad» en varios records (w0101, w0106, w0112, w0114, w0118). Cosmético, pero sugiere retry/temperatura del reviewer.

## Veredicto de aceptación del rango
Con 1 WRONG material (nivel de precio específico), 0 omisiones de conocimiento material y la regresión w0106 FIXED, el rango w0100–w0130 queda en **97.7% de precisión material**. Acción recomendada: corregir `cl-rango-nivel-inferior-112695` y revisar la política de publicación del reviewer (falsos negativos) antes del cierre.

## FEEDBACK (Agents-OS)
- **Corpus bien diseñado**: el formato P1 con `frames[].path/exists/cited_by_claim` y asr ids estables hizo la auditoría source-grounded sin ambigüedad; el patrón de paths de frames (`media-run/evidence/objects/<evidence_id>.png`) funcionó siempre (0 frames inexistentes).
- **Fricción 1 — labels del reviewer como input de sesgo**: varios GROUNDING_INSUFFICIENT/CONTRADICTED se resuelven leyendo UN frame adyacente de la misma ventana. Sugerencia: en el corpus P1, incluir además del par citado el frame previo/posterior más cercano por pts_ms, o un campo `neighbor_frames`.
- **Fricción 2 — niveles de precio exigen lectura de píxeles**: las etiquetas del eje de TradingView mezclan labels de escala y de endpoints de objetos; en 2 casos (w0103 nivel inferior, w0116 línea PnG) hubo que verificar por aritmética entre niveles (entrada−distancia=objetivo). Sugerencia: añadir al corpus un campo `axis_labels` extraído por OCR por frame para auditorías sin visión.
- **Fricción 3 — detección de DUPLICATE es manual**: no hay índice de proposiciones canónicas entre ventanas; tuve que rastrear duplicados por memoria de sesión (asr ids compartidos ayudaron mucho). Sugerencia: exponer en el corpus un `related_canonical_claim_id` sugerido por similitud de asr-segments.
- **Gap — relación claims↔asr-segment implícita**: los `evidence_ids` no distinguen solapamiento de segmentos entre ventanas, que es la causa raíz de casi todos los DUPLICATE; hacerlo explícito abarataría esta auditoría.
- **Positivo**: la instrucción de agrupar lecturas de frames por ventana fue clave; 261 claims se auditaron con ~60 lecturas de imagen sin perder cobertura.
