# PROVENANCE — Compilación Clutifx V1

## Identidad

- Misión: CLUTIFX KNOWLEDGE COMPILATION V1 (ONE-SHOT, 2026-10-23).
- Snapshot fuente certificado: `7fdaac6bbe22dbc4cee7aa795c2baef3d99aa472` ( ancestro del HEAD de publicación; delta intermedio verificado sin archivos Clutifx).
- Preflight de la compilación: PASS 4/4 (`check_consumption_contract.py` PASS [12 capítulos, 1.608 registros = 1.599 activos + 9 superseded; 1.584 consumibles = 1.581 + 3 con duda material; 1 grupo de contradicción], `consumption_contract_selftest.py` PASS, `validate_library.py` PASS 12/12 con duraciones reales de los 12 videos, `check_term_sources.py` PASS 12/12). Evidencia: run `/home/kor/mke/clutifx-compilation-v1-20261023/preflight/PREFLIGHT.txt`.

## Bibliotecas fuente (las 12, sin modificaciones)

| # | Capítulo | SHA-256 video (prefijo) | Claims activos | SUPPORTED | UNCERTAIN | Superseded | Frames |
|---|---|---|---|---|---|---|---|
| 01 | ch01-introduccion | `4de8f12d` | 132 | 132 | 0 | 0 | 93 |
| 02 | ch02-time | `fb8b3de4` | 98 | 98 | 0 | 2 | 65 |
| 03 | ch03-bias | `c52dafa8` | 211 | 211 | 0 | 6 | 121 |
| 04 | ch04-entradas | `f69f7d62` | 119 | 111 | 8 | 0 | 105 |
| 05 | ch05-smt | `072f669d` | 100 | 99 | 1 | 0 | 81 |
| 06 | ch06-failure-swing | `470ff3c0` | 64 | 64 | 0 | 0 | 31 |
| 07 | ch07-setups | `b20ce8f7` | 238 | 238 | 0 | 0 | 126 |
| 08 | ch08-proceso | `5495798b` | 86 | 86 | 0 | 0 | 93 |
| 09 | ch09-red-flags | `e4c22102` | 137 | 135 | 2 | 0 | 73 |
| 10 | ch10-noticias | `cdd6ee7b` | 199 | 196 | 3 | 1 | 105 |
| 11 | ch11-riesgo | `590e4c3c` | 80 | 79 | 1 | 0 | 87 |
| 12 | ch12-psicotrading | `b9fc83c5` | 135 | 135 | 0 | 0 | 53 |
| Σ | | | 1.599 | 1.584 | 15 | 9 | 1.033 |

Restricciones respetadas: no se ejecutó ASR ni extracción; no se re-procesaron videos; no se modificó ningún claim original; no se normalizaron garbles sin evidencia; no se consumió legado MKE V2 como conocimiento activo.

## Proceso de la compilación

1. PREFLIGHT bloqueante (4 validadores + concordancia con el baseline certificado) → PASS persistido.
2. Digest completo de las 12 bibliotecas (documentation, OPEN-QUESTIONS, examples, rules, CLAIMS vía glosario e índice del curso).
3. Síntesis transversal en 17 documentos (12 temáticos + playbook + atlas + dudas + guía + README), construida sólo sobre claims consumibles con sus dudas adjuntas.
4. Verificación mecánica propia: script `check_compiled.py` (wikilinks resolubles; cobertura claim a claim con expansión de rangos; auditoría de citas no consumibles; control de los 3 claims guardados) — correcciones aplicadas hasta 0 errores de enlace y auditoría limpia.
5. Revisión residual claim a claim: 44 claims sin cita directa clasificados (21 EQUIV, 18 META, 3 VISUAL, 1 GARBLE, 1 ANUNCIO) — ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/COVERAGE|COVERAGE]].
6. DOCUMENTATION_VERIFIER independiente (worker sin acceso de autor) sobre el draft: ver informe enlazado desde aquí tras su ejecución.
7. QA práctica adversarial: 10 consultas canónicas + 5 adversariales ejecutadas contra la compilación y auditadas contra claims.
8. Publicación: esta carpeta `compiled/` bajo `knowledge-library/clutifx/`, navegación añadida a COURSE-INDEX y a la nota principal del proyecto MKE, validaciones re-ejecutadas, commit y push a `master` (respetando el autosync).

## Contrato de consumo aplicado

`CONSUMIBLE = ACTIVE ∧ SUPPORTED ∧ evidencia resuelta`, con dudas materiales adjuntas (q-ch07-019 para los 3 claims guardados), dudas auxiliares como nota, exclusiones SUPERSEDED/UNCERTAIN/legacy. Detalle en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/README|README §3]] y [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/COMPILATION-READINESS|COMPILATION-READINESS §C3]].

## Auditoría de esta compilación

- Enlaces: 0 errores (script del run; los destinos se resuelven contra el árbol del vault tras publicar).
- Cobertura: 1.388/1.584 citados directos (87,6%) + 152 vía examples.md/atlas (9,6%) + 44 clasificados (2,8%) = 1.584; ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/COVERAGE|COVERAGE]].
- DOCVERIFY independiente (worker sin acceso de autor, 2026-10-23): **PASS_WITH_FINDINGS — 0 MATERIAL + 7 MENOR**; los 7 corregidos y la corrección verificada. Informe: `/home/kor/mke/clutifx-compilation-v1-20261023/qa/DOCVERIFY.md`.
- QA práctica adversarial: 10 consultas canónicas + 5 adversariales ejecutadas y auditadas contra claims; informe: `/home/kor/mke/clutifx-compilation-v1-20261023/qa/PRACTICAL-QA.md`.
