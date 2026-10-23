---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases:
  - clutifx source coverage
  - cobertura fuente clutifx
tags:
  - kind/doc
  - area/echo
  - tech/strategy-research
created: "2026-10-23"
updated: "2026-10-23"
---

# CLUTIFX-SOURCE-COVERAGE — Mapa claims → catálogo

FASE B4 de la misión GOD. Demuestra que todo claim operativo relevante tiene destino en el catálogo o exclusión justificada. El mapeo claim-a-claim fino vive certificado en la biblioteca (`compiled/COVERAGE.md`: 1.388 citas directas + 152 vía atlas + 44 clasificados = 1.584 consumibles); este documento mapea **capítulo → piezas del catálogo** y consolida las exclusiones propias de esta misión. Minería por capítulo (extractos con veredicto por claim) como evidencia de segunda capa.

| Capítulo (claims totales) | Consumibles | Destino principal en el catálogo | Observaciones |
|---|---|---|---|
| ch01 introducción (132) | 132 | CMP-001..006 (rango, cadena, pendiente, reiniciado, TS, intra-TS), CMP-019, CMP-010 (P3), glosario master §1 | 20 claims META omitidos como regla (lista en extracto ch01); ninguno operativo perdido |
| ch02 time (100) | 98 | CMP-010, CMP-020, horario §1 (pirámide de aperturas, horas clave, minuto 59), CMP-024 (HTF manda), STR-001 contexto | 2 claims superseded (DOL/DXY) excluidos por contrato |
| ch03 bias (217) | 211 | CMP-002/003/004/007/008/023, §7 procedimiento, red flag 1 | 8 UNCERTAIN/deícticos no consumibles; 6 superseded |
| ch04 entradas (119) | 111 | STR-005 (refinado), SET-002/003/004 (OB, PDM espejo, continuación), §5 gestión, jerarquía DOL>entrada | 8 UNCERTAIN marcados (lista en dudas-y-discrepancias) |
| ch05 smt (100) | 99 | CMP-012/013/014/015, STR-007, red flag 4 | 1 UNCERTAIN (c-0073 dibujo caso 2) |
| ch06 failure swing (64) | 64 | CMP-011, STR-006 | — |
| ch07 setups (238) | 238 | STR-001/002/003/004, SET-001, CMP-020/021/022, checklist 4 preguntas (§0), contradicción q-ch07-019 preservada (no consumible como hora) | mayor capítulo; 2 claims guardados como duda material |
| ch08 proceso (86) | 86 | §7 procedimiento completo, CMP-002, salidas §5 (reacción contraria, vela clave condicional SET-007), anti-regla de venta | — |
| ch09 red flags (137) | 135 | §6 completo (4 flags), CMP-016..019, secuencia 1-5-9 (CMP-020), consolidación 3 momentos | 2 UNCERTAIN (c-0063, c-0075) |
| ch10 noticias (200) | 196 | STR-008(+b), CMP-021, filtros de noticia §6, calendario/Excel fuente | 15 UNCERTAIN-adjacent (garbles de pares q-ch10-005; c-0069/c-0113/c-0032) |
| ch11 riesgo (80) | 79 | §5 gestión completa (BE estructural, parciales, pirámides, riesgo por etapa), STR-009 | 1 UNCERTAIN (c-0068); capital de referencia no dicho |
| ch12 psicotrading (135) | 135 | `NON_TRADING_CONTENT` (excluido del catálogo salvo solapes ya cubiertos en §5/§8 del master vía ch11) | sin reglas de entrada/salida |
| **Total 1.608** | **1.584 + 15 UNCERTAIN** | | 9 superseded excluidos por contrato |

**Cadena de trazabilidad completa**: claim → (a) doc compilado del capítulo (citas wikilink certificadas por COVERAGE.md + DOCVERIFY 2026-10-23 0 MATERIAL) → (b) pieza del catálogo master (§ de este run) → (c) detector objetivo (CLUTIFX-OBJECTIVE-DETECTORS.md) → (d) variante experimental (CLUTIFX-EXPERIMENT-MATRIX.md). Los extractos por capítulo (12 archivos, minería GLM-5.3-Flash con veredicto por claim) quedan como evidencia de que ningún regla operativa de rules.md/examples.md quedó fuera de (b).

## Exclusiones consolidadas (clasificación de la misión)

- `META` (19+1): transaccional del curso (aperturas/recaps/anuncios) — ya clasificados por COVERAGE; sin destino por diseño.
- `EXAMPLE_ONLY`: ratios y cifras de ejemplos (12,34R; −164/−100 pips; 0.00209 del stop) — se citan como [ejemplo] en master/detectores, nunca como parámetro.
- `DUPLICATE_SEMANTICS` (20): repetidos del instructor — un solo destino (regla de no-duplicación de FASE E).
- `INSUFFICIENT_SPECIFICATION`: "Entry Model" (ch04 c-0110); vídeo extras del reiniciado (ch03 c-0013); capital de referencia de % (q-ch11-001); límite de reentradas; distancia numérica del stop (mostrada 0.00209 no verbalizada). Ninguno rellenable.
- `UNCERTAIN` (15): lista nominal en `compiled/dudas-y-discrepancias.md` §3; ninguno consumido como hecho; los tocamientos del catálogo los marcan.
- `NOT_OBSERVABLE_WITH_AVAILABLE_DATA`: SMT multi-par, DXY, motivo FS-brokers, pares de confirmación de noticia (sin 2º instrumento/calendario).
- `NON_TRADING_CONTENT`: ch12 íntegro + psicología dispersa (notas de extractos).
- Contradicción MATERIAL vigente q-ch07-019 (hora 10 vs 8 de la noticia del ejemplo NY-EUR): ambas versiones preservadas en STR-008 como contexto; **ninguna hora adjudicada**; la regla operativa de ch07 (con noticia a las 8:30 operar la vela de las 5) queda como la regla general y la entrada en la 9 sólo como variante descrita, sin hora confirmada para ese ejemplo.
