# COMPILATION-READINESS — Clutifx (2026-10-23, certificación GOD)

Documento mínimo de preparación para la futura recompilación integral del curso. **Este documento NO ejecuta la recompilación** (mandato: COMPILATION_EXECUTED = NO). Autoridades canónicas: COURSE-INDEX.md, GLOSSARY.md, los claims.jsonl por capítulo y los validadores de la skill `course-knowledge-extraction` v1.2.

Historial: la certificación anterior (CLUTIFX_FINAL_REGULARIZATION, 2026-10-22, baseline `85369dba`) se emitió con defectos que una auditoría independiente detectó; esta versión la sustituye tras corregirlos (misión GOD 2026-10-22/23; ver FRAME-RECONCILIATION-2026-10-22.md §cierre, AMENDMENTS ch01-006/007 y ch07-005/006, y el HANDOFF del run `~/mke/clutifx-god-cert-20261022/`).

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
- **Preguntas abiertas materiales**: visibles, con IDs estables y ahora con dos nuevas (q-ch07-019 hora de noticia; q-ch01 ninguna nueva). Ninguna afirmación dudosa es consumible como hecho.

## Control de sincronización (Fase C — fix en la causa)

- **Causa raíz** (histórica): doble sync sin tumbas compartidas — cron git (`sync.sh`, cada minuto) + Obsidian Self-hosted LiveSync (v1.0.26, liveSync=true, CouchDB E2EE). LiveSync re-descargaba borrados locales; el cron commiteaba lo restaurado. Detalle: FRAME-RECONCILIATION-2026-10-22.md.
- **Fix aplicado (2026-10-22 21:53)**: exclusión soportada del árbol Clutifx en LiveSync mediante `syncIgnoreRegEx = "knowledge-library/clutifx/"` (predicado de sync-target del plugin: excluye de propagación Y reflexión), aplicada con reinicio controlado de Obsidian (systemd --user; config verificada en disco tras apagado y arranque). LiveSync NO desactivado; CouchDB/E2EE intactos. Se descartó `useIgnoreFiles/.gitignore` por romper el git.
- **Convergencia demostrada (21:53→07:0x, ~9 h)**: 0/55 nombres retirados reaparecidos; 1.033/1.033 PNG en 12/12 (conteos exactos); 0 adds de frames en git; 0 borrados nuevos; LiveSync vivo con el filtro activo durante todo el período, con ~9 h de ciclos reales de autosync (cron, cada minuto) y replicación continua.
- **Residual**: (a) otros dispositivos con LiveSync sobre el mismo CouchDB remoto NO quedan protegidos (alcance local a este vault; decisión del Owner); (b) revertir la config reintroduce el riesgo; (c) los validadores W06/V11/V04/V05 siguen como red de detección.

## Política de consumo para la recompilación (C3)

El compilador sólo tratará como conocimiento fundamentado:

```text
ACTIVE (sin superseded_by) AND verdict = SUPPORTED AND evidencia resuelta (s-/f- existentes)
```

Excluir de afirmaciones factuales: SUPERSEDED (9), UNCERTAIN (15), UNVERIFIED (0), y todo el contenido de `ch01-introduccion/legacy-mke-v2/` (1.894 registros MKE V2 — historia, no conocimiento). Los elementos inciertos se conservan como preguntas/limitaciones identificadas (OPEN-QUESTIONS por capítulo, incluida la nueva q-ch07-019); los superseded navegan a su reemplazo. Dependencias de duda material que NO deben entrar como conocimiento confirmado: q-ch01-002 ("doble"→DOL/DXY) y sus análogas por capítulo listadas en OPEN-QUESTIONS.

## Resultado

```text
READY_FOR_COMPILATION = PASS
COMPILATION_EXECUTED = NO
```

Sin defectos materiales conocidos abiertos. Recomendaciones no bloqueantes al Owner: (1) decidir si otros dispositivos con LiveSync deben replicar la exclusión `syncIgnoreRegEx`; (2) la decisión ASR (GPU/modelo) sigue abierta y no afecta a la recompilación.

## Commit de compilación

El commit autoritativo para la futura recompilación es el que contiene este archivo tras el push final de la misión GOD (ver HANDOFF del run; HEAD verificado contra origin/master después del último ciclo de autosync).
