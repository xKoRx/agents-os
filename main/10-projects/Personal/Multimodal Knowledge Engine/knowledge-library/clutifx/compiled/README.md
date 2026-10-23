# Clutifx — Biblioteca compilada (Knowledge Compilation V1)

Recompilación integral del conocimiento certificado de los 12 capítulos del curso Clutifx en una biblioteca integrada, coherente, navegable y utilizable. **Este artefacto es derivado: la autoridad sigue siendo la biblioteca por capítulos** ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/COURSE-INDEX|COURSE-INDEX]]), sus `claims.jsonl` y sus transcripciones/frames.

Estado de la fuente: snapshot certificado `7fdaac6b` (CLUTIFX_GOD_FINAL_HARDING → READY_FOR_COMPILATION = PASS; ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/COMPILATION-READINESS|COMPILATION-READINESS]]). Preflight de esta compilación: 4/4 validadores PASS, métricas idénticas al baseline (12 capítulos, 1.599 activos, 1.584 SUPPORTED, 15 UNCERTAIN, 9 superseded, 1.033 frames, 3 claims con duda material, 1 grupo de contradicción). Provenance completa: [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/PROVENANCE|PROVENANCE]].

## 1. Qué puedes hacer con esta biblioteca

- **Estudiar** la metodología completa del instructor en orden progresivo ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/guia-estudio|guía de estudio]]).
- **Consultar** conceptos, reglas, condiciones, excepciones y ejemplos por tema (documentos 01–12).
- **Decidir** con el [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/playbook-decisiones|playbook]]: prerrequisitos, señales, invalidaciones, red flags, excepciones y acciones de gestión.
- **Ver los ejemplos** originales indexados ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/atlas-ejemplos|atlas]]).
- **Saber qué NO está resuelto**: contradicciones, garbles y huecos ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/dudas-y-discrepancias|dudas-y-discrepancias]]).
- **Trazar** cualquier afirmación hasta su claim, su segmento de transcript y su frame.

## 2. Mapa de la compilación

| Documento | Responsabilidad | Fuente principal |
|---|---|---|
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/guia-estudio|guia-estudio]] | Entrada de estudio y consulta; rutas por tipo de pregunta | transversal |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/01-rangos-y-estructura|01-rangos-y-estructura]] | Rango, cadena, pendiente/reiniciado, a favor/en contra, invalidación, HTF manda, rangos enfrentados | ch01, ch02, ch03, ch07, ch08 |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/02-tiempo-y-power-of-3|02-tiempo-y-power-of-3]] | Temporalidades, horario NY, aperturas, horas clave, sesiones, Power of 3 | ch02, ch01, ch03, ch07, ch09 |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/03-bias|03-bias]] | Procedimiento del bias, DOL, jerarquía de TFs, anti "solo time-based" | ch03 (+ch04/ch05) |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/04-turtle-soup|04-turtle-soup]] | Turtle Soup, intra-Turtle Soup, stop, no esperar cierre | ch01, ch02, ch04, ch11 |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/05-failure-swing|05-failure-swing]] | Definición, 3 motivos, identificación, rango activado, usos | ch06, ch01, ch07, ch08 |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/06-smt-y-dxy|06-smt-y-dxy]] | SMT clásica vs estrategia, 3 casos, DXY −1 | ch05, ch01, ch06, ch09, ch10 |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/07-entradas|07-entradas]] | Esquema y orden de entradas, refinado, reglas, invalidaciones, salidas | ch04 (+ch02/ch07/ch08) |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/08-setups-london-ny|08-setups-london-ny]] | Escenarios de London, setups de NY, checklist de 4 preguntas | ch07 |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/09-red-flags|09-red-flags]] | Las 4 red flags con su fuerza dicha | ch09 (+ch07/ch10) |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/10-noticias|10-noticias]] | Excel de noticias, doctrina, horarios, confirmaciones, red flags de noticias | ch10 (+ch02/ch03/ch07) |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/11-riesgo-y-gestion|11-riesgo-y-gestion]] | Riesgo por etapa, cobro, BE, parciales, stop, pirámides | ch11 (+ch04/ch08/ch09) |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/12-psicotrading|12-psicotrading]] | Parte mental como relato de experiencia | ch12 |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/playbook-decisiones|playbook-decisiones]] | Condiciones y decisiones consultables | transversal |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/atlas-ejemplos|atlas-ejemplos]] | Índice de ejemplos con claims y frames | los 12 examples.md |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/dudas-y-discrepancias|dudas-y-discrepancias]] | Contradicción MATERIAL, UNCERTAIN, garbles, huecos | los 12 OPEN-QUESTIONS |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/COVERAGE|COVERAGE]] | Matriz de cobertura claims → secciones | generado |
| [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/PROVENANCE|PROVENANCE]] | Snapshot, SHAs, validaciones, auditoría | generado |

## 3. Autoridades y contrato de consumo

**Autoridades** (en orden): (1) `claims.jsonl` por capítulo (autoridad máquina-legible), (2) `transcript.md` + `frames/` (evidencia primaria), (3) documentación por capítulo, (4) esta compilación (derivada). El legado `ch01-introduccion/legacy-mke-v2/` NO es conocimiento activo.

**Contrato de consumo aplicado**: sólo `ACTIVE ∧ SUPPORTED ∧ evidencia resuelta`, con estas reglas (C3 de COMPILATION-READINESS):

1. **Fidelidad, no verdad**: SUPPORTED acredita que el instructor dijo/observó eso con evidencia verificada; NO acredita verdad objetiva ni rentabilidad. El estado epistémico lo dan `epistemic` y `kind` — ninguna inferencia del extractor se atribuye al instructor.
2. **Dudas materiales adjuntas**: los 3 claims del grupo de contradicción (q-ch07-019: la noticia del ejemplo NY-EUR dicha «a las 10» [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0143|c-0143]] y «a las 8» [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0181|c-0181]], [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/CLAIMS#c-0182|c-0182]]) se consumen sólo con su duda abierta [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch07-setups/OPEN-QUESTIONS#q-ch07-019|q-ch07-019]] visible — **prohibido afirmar una hora confirmada**. Las dudas auxiliares (garbles, deícticos) acompañan como nota sin bloquear.
3. **Exclusiones**: SUPERSEDED (9, navegan a su reemplazo), UNCERTAIN (15, se describen como dudosos), UNVERIFIED (0), legacy MKE V2, evidencia inexistente.
4. **Hedges preservados**: «puede», «normalmente», «a veces», «yo creo», «no siempre», «en este ejemplo», «en mi experiencia» son parte del contenido; la compilación no aumenta la certeza de la fuente.
5. **Sin garantías de rentabilidad**: la extracción certifica lo enseñado; MKE no valida la estrategia ni sus resultados.

**Navegación**: toda afirmación operativa material tiene cadena de trazabilidad con wikilinks completos → claim (`[[…/CLAIMS#c-XXXX]]`), segmento (`[[…/transcript#^s-HHMMSS]]` cuando se cita el segmento crudo), frame (`[[…/frames/f-HHMMSS.png]]`) y OPEN-QUESTIONS cuando corresponde.

## 4. Qué NO es esta compilación

- No es una segunda fuente de verdad: donde haya duda, manda el claim y su evidencia.
- No convierte descripciones de ejemplos en reglas generales.
- No inventa reglas para cubrir huecos (los huecos están declarados en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/dudas-y-discrepancias#6-huecos-de-contenido-declarados-ausencia-es-ausencia|dudas §6]]).
- No implementa estrategias automáticas ni sistemas de trading.
- No presenta la metodología como rentable o validada empíricamente.

## 5. Historia

Compilada el 2026-10-23 (misión CLUTIFX KNOWLEDGE COMPILATION V1, ONE-SHOT) desde el snapshot certificado `7fdaac6b`. Preflight, QA independiente, prueba práctica adversarial y validaciones de publicación documentadas en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/compiled/PROVENANCE|PROVENANCE]]. Las correcciones futuras se hacen por el mecanismo de complemento de la skill (re-consultar los recursos citados, nunca re-procesar videos).
