# COMPILATION-READINESS — Clutifx (2026-10-22)

Documento mínimo de preparación para la futura recompilación integral del curso. **Este documento NO ejecuta la recompilación** (mandato: COMPILATION_EXECUTED = NO). Autoridades canónicas: COURSE-INDEX.md, GLOSSARY.md, los claims.jsonl por capítulo y los validadores de la skill `course-knowledge-extraction` v1.2.

## Identidad certificada

| Campo | Valor |
|---|---|
| Misión | CLUTIFX_FINAL_REGULARIZATION (2026-10-22) |
| HEAD del artefacto | ver §Commit de compilación al final (se cierra con el push de este archivo) |
| Baseline auditado externamente | `a05186a7` (55 huérfanos, CH01 legacy) — reproducido 1:1 al iniciar |

## Inventario y estado por capítulo (12/12)

| # | Capítulo | SHA-256 (prefijo) | Claims activos | SUPPORTED | UNCERTAIN | Superseded | Frames físicos/indexados | LIBRARY_VALIDATION | SOURCE_FIRST |
|---|---|---|---|---|---|---|---|---|---|
| 01 | ch01-introduccion | `4de8f12d…` | 132 | 132 | 0 | 0 | 89/89 | PASS (0) | PASS |
| 02 | ch02-time | `fb8b3de4…` | 98 | 98 | 0 | 2 | 65/65 | PASS (0) | PASS |
| 03 | ch03-bias | `c52dafa8…` | 211 | 211 | 0 | 6 | 121/121 | PASS (0) | PASS |
| 04 | ch04-entradas | `f69f7d62…` | 119 | 111 | 8 | 0 | 105/105 | PASS (0) | PASS |
| 05 | ch05-smt | `072f669d…` | 100 | 99 | 1 | 0 | 81/81 | PASS (0) | PASS |
| 06 | ch06-failure-swing | `470ff3c0…` | 64 | 64 | 0 | 0 | 31/31 | PASS (0) | PASS |
| 07 | ch07-setups | `b20ce8f7…` | 238 | 238 | 0 | 0 | 126/126 | PASS (0) | PASS |
| 08 | ch08-proceso | `5495798b…` | 86 | 86 | 0 | 0 | 93/93 | PASS (0) | PASS |
| 09 | ch09-red-flags | `e4c22102…` | 137 | 135 | 2 | 0 | 73/73 | PASS (0) | PASS |
| 10 | ch10-noticias | `cdd6ee7b…` | 199 | 196 | 3 | 1 | 105/105 | PASS (0) | PASS |
| 11 | ch11-riesgo | `590e4c3c…` | 80 | 79 | 1 | 0 | 87/87 | PASS (0) | PASS |
| 12 | ch12-psicotrading | `b9fc83c5…` | 135 | 135 | 0 | 0 | 53/53 | PASS (0) | PASS |
| **Σ** | | | **1.599** | **1.584** | **15** | **9** | **1.029/1.029** | **12/12 PASS** | **12/12 PASS** |

Identidades de fuente verificadas por SHA-256 completo de los 12 videos el 2026-10-22 (los 12 coinciden con los README por capítulo).

## QA y verificación

- **Revisión por minuto**: válida por contrato en los 12 (cardinalidad verificada por `validate_review.py`/integrador; CH01: 34/34 minutos, 132/132 claims). CH02–CH12: válidos en sus runs originales (detalle por capítulo en METHODOLOGY-FEEDBACK).
- **DOCVERIFY**: CH01 independiente ONE-SHOT 2026-10-22 = PASS_WITH_FINDINGS (0 MATERIAL + 11 MENOR; los 4 recomendados corregidos, am-ch01-005). CH02–CH12: ejecutados en sus cierres (MATERIAL corregidos entonces; detalle en METHODOLOGY-FEEDBACK/AMENDMENTS por capítulo).
- **Semántica targeted (C2)**: definiciones fundacionales contrastadas en CH01 (DOCVERIFY punto 4) y cross-capítulo vía `check_term_sources.py` 12/12 PASS (DOL/DXY y grupos críticos, 1.584 claims vivos, 0 MATERIAL, 0 TERM_DISAMBIGUATION_REQUIRED). Claims refutados en ACTIVE KNOWLEDGE: 0 (los 9 superseded son historia navegable con `superseded_by` bidireccional, validado por V14 en los 12).
- **Preguntas abiertas materiales**: visibles y con IDs estables por capítulo (OPEN-QUESTIONS). Ninguna afirmación dudosa es consumible como hecho: UNCERTAIN (15) excluidos de las síntesis y marcados; garbles con [ASR] preservados en statements.

## Control de sincronización (Fase A)

- **Causa raíz de la resurrección de PNGs**: doble sync sin tumbas compartidas — cron git (`sync.sh`, cada minuto) + Obsidian Self-hosted LiveSync (liveSync=true, E2EE CouchDB, replicación periódica) sobre el mismo árbol. LiveSync re-descargaba archivos borrados localmente (inodos nuevos, mtime original preservado, blobs idénticos); el cron commiteaba lo restaurado. Detalle y evidencia: FRAME-RECONCILIATION-2026-10-22.md.
- **Reconciliación**: 55/55 residuos retirados (48 nombre inválido + 4 fuera de duración + 3 históricos), todos byte-idénticos a frames indexados; 0 VALID_UNINDEXED; manifiesto `.deprecated_frame_names` completado (ch03).
- **Persistencia verificada**: 0 huérfanos en los 12 capítulos tras ~3 horas y múltiples ciclos reales de sincronización git+LiveSync (retiro 16:35 → verificación 19:5x; evento inverso observado y repuesto durante CH01, ver review-notes de ch01). El riesgo residual del plugin queda documentado como recomendación al Owner (no bloquea: los validadores W06/V11/V04/V05 cazan cualquier re-aparición).

## Política de consumo para la recompilación (C3)

El compilador sólo tratará como conocimiento fundamentado:

```text
ACTIVE (sin superseded_by) AND verdict = SUPPORTED AND evidencia resuelta (s-/f- existentes)
```

Excluir de afirmaciones factuales: SUPERSEDED (9), UNCERTAIN (15), UNVERIFIED (0), y todo el contenido de `ch01-introduccion/legacy-mke-v2/` (1.894 registros MKE V2 — historia, no conocimiento). Los elementos inciertos se conservan como preguntas/limitaciones identificadas (OPEN-QUESTIONS de cada capítulo); los superseded navegan a su reemplazo. Dependencias de duda material que NO deben entrar como conocimiento confirmado: q-ch01-002 ("doble"→DOL/DXY) y sus análogas por capítulo listadas en OPEN-QUESTIONS.

## Resultado

```text
READY_FOR_COMPILATION = PASS
COMPILATION_EXECUTED = NO
```

Sin defectos materiales conocidos abiertos. Recomendaciones no bloqueantes al Owner: (1) desactivar o reconfigurar Obsidian LiveSync para este árbol (o excluirlo) para eliminar el riesgo de resurrección/borrado fuera de git; (2) la decisión ASR (GPU/modelo) sigue abierta y no afecta a la recompilación.

## Commit de compilación

El commit autoritativo para la futura recompilación es el que contiene este archivo tras el push final de la misión (ver HANDOFF del run; HEAD verificado contra origin/master después del último ciclo de autosync).
