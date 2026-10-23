# COMPILATION-READINESS — Clutifx (2026-10-23, certificación GOD + contrato de consumo)

Documento mínimo de preparación para la futura recompilación integral del curso. **Este documento NO ejecuta la recompilación** (mandato: COMPILATION_EXECUTED = NO). Autoridades canónicas: COURSE-INDEX.md, GLOSSARY.md, los claims.jsonl por capítulo y los validadores de la skill `course-knowledge-extraction` v1.2.

Historial: la certificación anterior (CLUTIFX_FINAL_REGULARIZATION, 2026-10-22, baseline `85369dba`) se emitió con defectos que una auditoría independiente detectó; esta versión la sustituye tras corregirlos (misión GOD 2026-10-22/23; ver FRAME-RECONCILIATION-2026-10-22.md §cierre, AMENDMENTS ch01-006/007 y ch07-005/006, y el HANDOFF del run `~/mke/clutifx-god-cert-20261022/`). Ampliación 2026-10-23 (misión KNOWLEDGE_CONSUMPTION_HARDENING, am-ch07-007): la última brecha abierta —q-ch07-019 señalizada sólo en documentación narrativa— quedó cerrada con vínculo estructural en los claims y el contrato de consumo de §C3 endurecido con preflight determinista y casos negativos (`~/mke/clutifx-contract-hardening-20261023/`). Efecto secundario de la misma misión: proyectar las dudas en CLAIMS.md sometió las notas a V11 y sacó a la luz 8 notas de duda con referencias colgantes latentes (IDs de frames hipotéticos o de frames de revisión nunca publicados, y una cita de segmento inexistente), todas re-ancladas sin tocar statements (am-ch03-001, am-ch07-008, am-ch10-003/004).

## Identidad certificada

| Campo | Valor |
|---|---|
| Misión | CLUTIFX_GOD_FINAL_HARDENING (2026-10-22/23) |
| Baseline de partida | `85369dba` (ancestro verificado; delta Clutifx previo vacío) |
| HEAD del artefacto | ver §Commit de compilación al final (se cierra con el push de este archivo) |

## Inventario y estado por capítulo (12/12)

| # | Capítulo | SHA-256 (prefijo) | Claims activos | SUPPORTED | UNCERTAIN | Superseded | Frames físicos/indexados | LIBRARY_VALIDATION | SOURCE_FIRST |
|---|---|---|---|---|---|---|---|---|---|
| 01 | ch01-introduccion | `4de8f12d…` | 132 | 132 | 0 | 0 | 93/93 | PASS (0) | PASS |
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
| **Σ** | | | **1.599** | **1.584** | **15** | **9** | **1.033/1.033** | **12/12 PASS** | **12/12 PASS** |

Identidades de fuente verificadas por SHA-256 completo de los 12 videos (los 12 coinciden con los README por capítulo). Delta de inventario vs la certificación anterior: CH01 frames 89→93 (+4 publicados por la corrección de grounding visual, am-ch01-006; total 1.029→1.033). Claims, veredictos y supersession SIN cambios (1.599/1.584/15/9 idénticos).

## QA y verificación

- **Revisión por minuto**: válida por contrato en los 12 (cardinalidad verificada por `validate_review.py`/integrador en sus runs originales; detalle en METHODOLOGY-FEEDBACK).
- **DOCVERIFY CH01**: independiente ONE-SHOT original (0 MATERIAL + 11 MENOR) re-adjudicado contra el árbol (fase D): DV01-006 estaba declarado y NO aplicado (reglas R27) → aplicado; los 7 MENOR residuales corregidos o resueltos con fundamento (am-ch01-007). 0 abiertos.
- **DOCVERIFY CH07**: independiente ONE-SHOT REAL ejecutado en esta misión (DV-CH07-GOD-20261022-R2, worker sin acceso de autor): PASS_WITH_FINDINGS (1 MATERIAL + 5 MENOR). MATERIAL = f-000545 con nombre de segundos crudos (contenido real 09:05; MAD 0.00 verificado) → renombrado f-000905 y referencias actualizadas; MENOR corregidos (am-ch07-005). RE-VERIFICACIÓN independiente posterior sobre el árbol físico: PASS 7/7. 0 MATERIAL abiertos.
- **Grounding visual CH01 (fase A)**: forense de píxeles ffmpeg de los 93 PNG contra el MP4 (SHA verificado): 3 frames renombrados por nomenclatura raw-seconds, 6 timestamps de justificación corregidos (2 mecanismos: nombre concatenado y lectura raw del nombre), 4 frames citados-no-publicados extraídos, contrastados y publicados. 0 casos restantes (barrido completo). am-ch01-006.
- **Barrido semántico cross-chapter (fase E)**: 3 auditores independientes (E1 rango/pendiente/TS/DOL-DXY; E2 SMT/failure-swing/OB/Po3; E3 London-NY/noticias/riesgo/psicotrading/superficie): núcleo semántico coherente; 0 MATERIAL abiertos tras corrección — el único MATERIAL (XE3-04: dos horas dichas para la noticia del ejemplo NY-EUR) quedó registrado como duda abierta q-ch07-019 con flags en síntesis (no-armonización sin evidencia, contrato SOURCE-FIRST); 15 MENOR corregidos (hedges preservados en GLOSSARY/COURSE-INDEX, citas realineadas, punteros legacy→V1.2, cabeceras ch11, [ASR] faltantes).
- **Semántica targeted**: `check_term_sources.py` 12/12 PASS (1.584 claims vivos, 0 MATERIAL, 0 TERM_DISAMBIGUATION_REQUIRED). Claims refutados en ACTIVE KNOWLEDGE: 0 (los 9 superseded son historia navegable, V14 ×12).
- **Contrato de consumo (preflight F1)**: 1.584 claims consumibles (ACTIVE ∧ SUPPORTED ∧ evidencia s-*/f-* resuelta), 0 con evidencia rota; exclusiones activas (SUPERSEDED 9, UNCERTAIN 15, UNVERIFIED 0, legacy-mke-v2 fuera).
- **Preguntas abiertas materiales**: visibles, con IDs estables y ahora con dos nuevas (q-ch07-019 hora de noticia; q-ch01 ninguna nueva). Ninguna afirmación dudosa es consumible como hecho. Desde 2026-10-23 la duda material tiene además **vínculo estructural**: q-ch07-019 declara `Materialidad: MATERIAL` y está referenciada en el `unresolved_questions` de los tres claims que afecta (am-ch07-007); el preflight del contrato verifica la bidireccionalidad.

## Control de sincronización (Fase C — fix en la causa)

- **Causa raíz** (histórica): doble sync sin tumbas compartidas — cron git (`sync.sh`, cada minuto) + Obsidian Self-hosted LiveSync (v1.0.26, liveSync=true, CouchDB E2EE). LiveSync re-descargaba borrados locales; el cron commiteaba lo restaurado. Detalle: FRAME-RECONCILIATION-2026-10-22.md.
- **Fix aplicado (2026-10-22 21:53)**: exclusión soportada del árbol Clutifx en LiveSync mediante `syncIgnoreRegEx = "knowledge-library/clutifx/"` (predicado de sync-target del plugin: excluye de propagación Y reflexión), aplicada con reinicio controlado de Obsidian (systemd --user; config verificada en disco tras apagado y arranque). LiveSync NO desactivado; CouchDB/E2EE intactos. Se descartó `useIgnoreFiles/.gitignore` por romper el git.
- **Convergencia demostrada (21:53→07:0x, ~9 h)**: 0/55 nombres retirados reaparecidos; 1.033/1.033 PNG en 12/12 (conteos exactos); 0 adds de frames en git; 0 borrados nuevos; LiveSync vivo con el filtro activo durante todo el período, con ~9 h de ciclos reales de autosync (cron, cada minuto) y replicación continua.
- **Residual**: (a) otros dispositivos con LiveSync sobre el mismo CouchDB remoto NO quedan protegidos (alcance local a este vault; decisión del Owner); (b) revertir la config reintroduce el riesgo; (c) los validadores W06/V11/V04/V05 siguen como red de detección.

## Política de consumo para la recompilación (C3, endurecida 2026-10-23)

El compilador sólo tratará como conocimiento fundamentado:

```text
CONSUMIBLE = ACTIVE (sin superseded_by) AND verdict = SUPPORTED AND evidencia resuelta (s-/f- existentes)
```

con este significado y estas reglas de consumo:

1. **Fidelidad, no verdad**: SUPPORTED acredita que el instructor dijo/observó eso con evidencia verificada (eje A); NO acredita verdad objetiva ni ausencia de contradicciones con otras declaraciones. El estado epistémico (eje B) lo dan `epistemic` (instructor_statement / visual_observation / model_inference) y `kind` — las inferencias del extractor no se atribuyen a la fuente.
2. **Dudas materiales adjuntas** (eje C): todo consumible que referencia en `unresolved_questions` una q-* con Estado OPEN y `Materialidad: MATERIAL` se consume como **CONSUMIBLE_CON_DUDA_MATERIAL** — acompañado siempre por su pregunta abierta, preservando TODAS las versiones dichas. Las dudas AUXILIARES (garbles, deícticos; sin marcador MATERIAL) acompañan como nota sin bloquear el claim: proporcionalidad, no degradación masiva.
3. **Contradicciones materiales** (eje E): ≥2 consumibles ligados a la misma q-* MATERIAL forman un grupo de contradicción (único vigente: q-ch07-019 = {c-0143, c-0181, c-0182}, noticia «a las 10» vs «a las 8» del ejemplo NY-EUR de ch07). Ninguno de sus claims puede sostener un hecho definitivo («la noticia fue a las X») ni una regla operativa universal basada en ese dato; el compilador conserva ambas declaraciones como evidencia histórica del instructor.
4. **Exclusiones del conocimiento factual** (eje D): SUPERSEDED (9), UNCERTAIN (15), UNVERIFIED (0), todo `ch01-introduccion/legacy-mke-v2/` (historia, no conocimiento) y evidencia inexistente. Los superseded navegan a su reemplazo; las inciertas quedan como preguntas/limitaciones identificadas (incluida q-ch01-002 «doble»→DOL/DXY y sus análogas en OPEN-QUESTIONS).

Verificación determinista: `scripts/check_consumption_contract.py <clutifx>/` (PASS: 12 capítulos, 1.608 registros = 1.599 activos + 9 superseded; 1.584 consumibles = 1.581 + 3 con duda material; 1 grupo de contradicción; 0 evidencia rota) con casos negativos en `scripts/tests/consumption_contract_selftest.py` (14/14: contradicción sin señalizar → detectada; hecho definitivo «a las 8»/«a las 10» y regla universal sobre claims guardados → RECHAZADOS; reporte de contradicción con ambas horas → ACEPTADO). La interpretación libre de síntesis en texto libre es trabajo del compilador futuro; el contrato aquí fijado es su especificación mínima.

## Resultado

```text
KNOWLEDGE_LIBRARY_READY = PASS
CONSUMPTION_CONTRACT = PASS
READY_FOR_COMPILATION = PASS
COMPILATION_EXECUTED = YES (2026-10-23)
```

Sin defectos materiales conocidos abiertos. **Compilación ejecutada (2026-10-23, misión CLUTIFX KNOWLEDGE COMPILATION V1)**: la superficie derivada vive en `compiled/` ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/README|entrada]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/PROVENANCE|provenance completa]]); preflight 4/4 PASS contra este snapshot, DOCVERIFY independiente PASS_WITH_FINDINGS (0 MATERIAL), QA práctica adversarial PASS, cobertura 1.584/1.584 conciliada ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/COVERAGE|COVERAGE]]). Este documento de preparación queda como registro del estado que la compilación consumió. Recomendaciones no bloqueantes al Owner: (1) decidir si otros dispositivos con LiveSync deben replicar la exclusión `syncIgnoreRegEx`; (2) la decisión ASR (GPU/modelo) sigue abierta y no afecta a la recompilación.

## Commit de compilación

El commit autoritativo para la futura recompilación es el que contiene este archivo tras el push final de la misión GOD (ver HANDOFF del run; HEAD verificado contra origin/master después del último ciclo de autosync).
