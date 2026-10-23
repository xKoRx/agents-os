# COVERAGE — Matriz de cobertura de la compilación

Matriz derivada que mapea los claims consumibles (`ACTIVE ∧ SUPPORTED ∧ evidencia resuelta`, 1.584) a su representación en la compilación. Generada por el script del run (`check_compiled.py`) sobre los wikilinks reales de los documentos publicados —excluyendo este archivo y PROVENANCE del conteo para evitar circularidad— y revisada claim a claim por el compilador. **La omisión de un claim de esta prosa no es una omisión de conocimiento**: la clasificación de abajo hace reconstruible qué sección lo respalda o por qué no entra.

Método de cómputo: (1) *citado directo* = el claim aparece con wikilink (incluidos rangos explícitos `c-XXXX–c-YYYY`) en un documento compilado (los 12 temáticos, playbook, atlas, dudas, guía, README); (2) *vía atlas* = citado por el `examples.md` de su capítulo, al que el [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/atlas-ejemplos|atlas]] enlaza; (3) *sin cita directa* = clasificado abajo con código. Desglose total: **1.388 directos (87,6%) + 152 vía atlas (9,6%) + 44 clasificados (2,8%) = 1.584**.

## Tabla por capítulo

| Capítulo | Consumibles (ACTIVE∧SUPPORTED) | Citados directamente | Sin cita directa | Cobertura |
|---|---|---|---|---|
| ch01-introduccion | 132 | 108 | 19 | 81.8% |
| ch02-time | 98 | 94 | 2 | 95.9% |
| ch03-bias | 211 | 102 | 10 | 48.3% |
| ch04-entradas | 111 | 101 | 5 | 91.0% |
| ch05-smt | 99 | 97 | 0 | 98.0% |
| ch06-failure-swing | 64 | 48 | 4 | 75.0% |
| ch07-setups | 238 | 226 | 2 | 95.0% |
| ch08-proceso | 86 | 86 | 0 | 100.0% |
| ch09-red-flags | 135 | 128 | 0 | 94.8% |
| ch10-noticias | 196 | 193 | 0 | 98.5% |
| ch11-riesgo | 79 | 70 | 2 | 88.6% |
| ch12-psicotrading | 135 | 135 | 0 | 100.0% |
| **Total** | **1584** | **1388** | **196** | **87.6%** |

## Clasificación de los 44 claims sin cita directa

### META — Transaccional del capítulo (apertura, temario, recap, cierre, despedida, anuncios de vídeo siguiente): no es metodología. Se conserva en el transcript del capítulo.
- ch01-introduccion: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0001|c-0001]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0002|c-0002]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0003|c-0003]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0104|c-0104]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0114|c-0114]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0115|c-0115]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0130|c-0130]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0131|c-0131]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0132|c-0132]]
- ch02-time: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0005|c-0005]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch02-time/CLAIMS#c-0082|c-0082]]
- ch03-bias: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0130|c-0130]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0205|c-0205]]
- ch06-failure-swing: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/CLAIMS#c-0031|c-0031]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/CLAIMS#c-0043|c-0043]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/CLAIMS#c-0064|c-0064]]
- ch07-setups: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0238|c-0238]]
- ch11-riesgo: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS#c-0080|c-0080]]
### EQUIV — Equivalente temático: el contenido está enunciado por otro claim SUPPORTED ya citado en la misma sección del documento compilado (el instructor repite la idea con otras palabras) o es narración de ejemplo representada por su E del atlas.
- ch01-introduccion: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0014|c-0014]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0021|c-0021]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0027|c-0027]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0029|c-0029]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0032|c-0032]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0033|c-0033]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0038|c-0038]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0039|c-0039]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0040|c-0040]]
- ch03-bias: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0027|c-0027]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0081|c-0081]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0090|c-0090]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0103|c-0103]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0104|c-0104]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0110|c-0110]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0131|c-0131]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0132|c-0132]]
- ch04-entradas: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0012|c-0012]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0020|c-0020]]
- ch07-setups: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0042|c-0042]]
- ch11-riesgo: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch11-riesgo/CLAIMS#c-0042|c-0042]]
### VISUAL — Descripción de pantalla/dibujo sin sustancia reglada (anotaciones visuales del ejemplo).
- ch04-entradas: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0010|c-0010]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0022|c-0022]]
- ch06-failure-swing: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch06-failure-swing/CLAIMS#c-0022|c-0022]]
### GARBLE — Garble de ASR con lecturas candidatas registradas en el claim que no afecta ninguna regla (ch04 c-0008: «la entidad» [ASR]; candidatos: «entidad» literal / garble de «la entrada»).
- ch04-entradas: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch04-entradas/CLAIMS#c-0008|c-0008]]
### ANUNCIO — Anuncio de contenido no desarrollado en los 12 capítulos («más tipos de rangos… lo vais a ver» ch01 c-0015) — hueco declarado.
- ch01-introduccion: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/CLAIMS#c-0015|c-0015]]

## Notas de auditoría

- Citas a claims NO consumibles: exactamente los 15 UNCERTAIN, todos en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/dudas-y-discrepancias|dudas-y-discrepancias]] y marcados como dudosos donde aparecen. Cero citas a SUPERSEDED como vigentes (el rango del atlas de ch02 excluye explícitamente c-0089 SUPERSEDED, que navega a c-0100).
- Claims guardados (q-ch07-019: c-0143, c-0181, c-0182): citados únicamente en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/08-setups-london-ny|08-setups-london-ny]] (con ambas horas + duda visible), [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/README|README]] (contrato) y [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/dudas-y-discrepancias|dudas-y-discrepancias]] — nunca como hecho.
- Los walkthroughs completos (ch08 86/86, ch12 135/135) quedan representados por rangos explícitos del atlas + síntesis; el checker verifica los extremos de cada rango contra los claims reales del capítulo.
- Los rangos por minuto se derivan de los `claims.jsonl` de cada capítulo; cualquier disputa se resuelve contra la autoridad del capítulo.
- Verificación independiente (DOCVERIFY, 2026-10-23): PASS_WITH_FINDINGS, 0 MATERIAL; los 7 MENOR fueron corregidos (punteros c-0218/c-0219 y c-0002/c-0003, ancla de README, sincronización de esta tabla con la corrida final, encabezados «obligatorio/JAMÁS» devueltos a la fuerza dicha, ruta absoluta → wikilink). Informe completo en el run `/home/kor/mke/clutifx-compilation-v1-20261023/qa/DOCVERIFY.md`.
