# AMENDMENTS — ch03-bias

Historial **append-only** de correcciones materiales y decisiones semánticas
sobre los claims del capítulo DESPUÉS de su publicación. Formato por entrada:
`amendment_id` · `claim_id` · fecha · motivo · anotación anterior · anotación
nueva · evidencia revisada · resultado. Los IDs de claim NUNCA se renumeran; si
una corrección cambia materialmente la proposición, se crea un claim nuevo y el
anterior queda superseded (ver contrato en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS|CLAIMS]] y en la skill principal).
Regeneraciones cosméticas de proyecciones NO se registran aquí (para eso está
git).

---

## amend-ch03-01

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0121|c-0121]] → **SUPERSEDED por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0215|c-0215]]**
- **Fecha:** 2026-10-18
- **Motivo:** normalización semántica incorrecta — el statement publicaba "se llegue **al DXY**" pero la fuente dice "**al DOL**" (s-002201, literal en ASR). DOL (objetivo de liquidez) y DXY (índice del dólar, lectura de ch02) son conceptos distintos; el referente de la proposición cambió → supersession (mecanismo V1.2).
- **Anotación anterior:** "es muy normal que se llegue al DXY utilizando esa volatilidad" + note "ASR 'al DOL' = 'al DXY' (garble conocido)".
- **Anotación nueva:** c-0215: "es muy normal que se llegue al DOL utilizando esa volatilidad" (palabra literal de la fuente); note documenta la remediation.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-002201|s-002201]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001229|s-001229]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** c-0121 preservado sin renumerar, marcado `superseded_by: c-0215`; c-0215 = SUPPORTED. Resuelve la parte accionable de [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/OPEN-QUESTIONS#q-ch03-001|q-ch03-001]].

## amend-ch03-02

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0122|c-0122]] → **SUPERSEDED por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0216|c-0216]]**
- **Fecha:** 2026-10-18
- **Motivo:** misma clase de defecto — "llegar al DXY… llegar hacia el DXY" publicado donde la fuente dice "al doll… hacia el doll" (s-002207, s-002215), dos frases después del "al DOL" literal (s-002201): mismo referente, DOL.
- **Anotación anterior:** statement con "al DXY"/"hacia el DXY" + note "'el doll' = 'el DXY'".
- **Anotación nueva:** c-0216 con "al DOL [ASR: 'doll']… hacia el DOL (el lunes)".
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-002207|s-002207]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-002215|s-002215]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** c-0122 `superseded_by: c-0216`; c-0216 = SUPPORTED.

## amend-ch03-03

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0123|c-0123]] → **SUPERSEDED por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0217|c-0217]]**
- **Fecha:** 2026-10-18
- **Motivo:** la aposición explícita del integrador "(La llegada al DXY)" fija un referente incorrecto para "Fue en FB"; el referente de la llegada es el DOL (continuación inmediata del pasaje DOL de s-002201–s-002215).
- **Anotación anterior:** "(La llegada al DXY) fue en FB y, por lo tanto, no es muy limpia."
- **Anotación nueva:** c-0217: "(La llegada al DOL [ASR: 'doll']) fue en FB…". La pregunta por "FB" queda abierta en [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/OPEN-QUESTIONS#q-ch03-003|q-ch03-003]] (ahora apuntando a c-0217).
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-002217|s-002217]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** c-0123 `superseded_by: c-0217`; c-0217 = SUPPORTED.

## amend-ch03-04

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0089|c-0089]] → **SUPERSEDED por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0212|c-0212]]**
- **Fecha:** 2026-10-18
- **Motivo:** statement publicaba "Aunque se tenga **el DXY** ahí abajo" donde la fuente dice "tenéis **el doble** aquí abajo" (s-001625/s-001627). "El doble" = el DOL (nivel/objetivo del gráfico "ahí abajo"; el índice DXY no es un nivel del chart EURUSD). Cambio material de referente → supersession.
- **Anotación anterior:** "…el DXY ahí abajo…" + note "'El doble' = el DXY (garble conocido del curso)".
- **Anotación nueva:** c-0212: "Aunque se tenga el DOL [ASR: 'el doble'] ahí abajo…".
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001625|s-001625]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001627|s-001627]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** c-0089 `superseded_by: c-0212`; c-0212 = SUPPORTED.

## amend-ch03-05

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0093|c-0093]] → **SUPERSEDED por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0213|c-0213]]**
- **Fecha:** 2026-10-18
- **Motivo:** statement publicaba "por mucho que **tu DXY** esté ahí abajo" donde la fuente dice "tu **doble**" (s-001719) = tu DOL. Mismo mecanismo: sustitución publicada con referente equivocado.
- **Anotación anterior:** "…tu DXY esté ahí abajo…" + note "ASR 'tu doble' = tu DXY".
- **Anotación nueva:** c-0213: "…por mucho que tu DOL [ASR: 'tu doble'] esté ahí abajo, no vas a poder vender ahí."
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001719|s-001719]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** c-0093 `superseded_by: c-0213`; c-0213 = SUPPORTED (la regla PDM no cambia).

## amend-ch03-06

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0116|c-0116]] → **SUPERSEDED por [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0214|c-0214]]**
- **Fecha:** 2026-10-18
- **Motivo:** statement publicaba "**el DXY** sigue intacto ahí abajo" donde la fuente dice "**el doble** sigue intacto ahí abajo" (s-002108) = el DOL bajista sin alcanzar. El "intacto ahí abajo" sólo tiene sentido de nivel de precio del chart.
- **Anotación anterior:** "…el DXY sigue intacto ahí abajo" + note "'el doble' = el DXY".
- **Anotación nueva:** c-0214: "…el DOL [ASR: 'el doble'] sigue intacto ahí abajo."
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-002108|s-002108]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** c-0116 `superseded_by: c-0214`; c-0214 = SUPPORTED.

## amend-ch03-07

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0144|c-0144]] (ID preservado)
- **Fecha:** 2026-10-18
- **Motivo:** la glosa inline "(DXY)" del statement era una interpretación incorrecta adosada a la palabra dicha ("del doll"); el statement preservaba la palabra pero publicaba el referente equivocado dentro del texto.
- **Anotación anterior:** "hay que añadir el componente del doll (DXY), del bias".
- **Anotación nueva:** "hay que añadir el componente del doll [ASR], del bias" + note con la interpretación correcta (DOL; s-001229 literal + f-004059). La proposición (añadir el componente direccional) se preserva → corrección in-place con amendment, sin supersession.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-002721|s-002721]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001229|s-001229]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** statement corregido; verdict/epistemic intactos.

## amend-ch03-08

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0184|c-0184]] (ID preservado)
- **Fecha:** 2026-10-18
- **Motivo:** glosa bracket "[DXY]" incorrecta sobre la palabra dicha "mi doble" (s-003541).
- **Anotación anterior:** "…se completa mi doble [DXY]…" + note "'Mi doble' = 'mi DXY'".
- **Anotación nueva:** "…se completa mi doble [ASR]…" + note: "mi doble" = mi DOL (el objetivo cuya finalización daba por segura el instructor).
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-003541|s-003541]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** corrección in-place; warning didáctico intacto.

## amend-ch03-09

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0208|c-0208]] (ID preservado)
- **Fecha:** 2026-10-18
- **Motivo:** la note interpretaba "'Doble' = DXY (glosario). Interpretación probable: bias para el DXY y la sesión", cuando la pizarra del propio minuto (f-004059: "12h - 8h - 6h - 4h = DOL sesión") resuelve el referente como DOL.
- **Anotación anterior:** interpretación DXY en notes.
- **Anotación nueva:** "para doble ya la sesión" = "para el DOL ya, la sesión" (pizarra); interpretación DXY descartada.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-004056|s-004056]]
- **Resultado:** notes corregidas; statement (preserva "para doble ya la sesión") y verdict intactos.

## amend-ch03-10

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0074|c-0074]] (ID preservado)
- **Fecha:** 2026-10-18
- **Motivo:** la note decía "«el doble» = el DXY según el glosario"; el referente correcto es DOL (destino del movimiento "hasta el doble"; s-001229 + f-004059).
- **Anotación anterior / nueva:** note corregida; statement (garble preservado) intacto.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001316|s-001316]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** note corregida.

## amend-ch03-11

- **Claims:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0055|c-0055]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0142|c-0142]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0146|c-0146]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0031|c-0031]] (IDs preservados)
- **Fecha:** 2026-10-18
- **Motivo:** notas que citaban la lectura antigua del glosario (DXY) o dejaban el referente sin adjudicar cuando la evidencia existente (s-001229 literal, f-004059) permite adjudicar DOL.
- **Anotación nueva:** «Dole»/«doll»/«el doble» = DOL en los cinco casos; garbles preservados en statements.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001229|s-001229]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** notes alineadas; statements intactos.

## amend-ch03-12

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0080|c-0080]] (ID preservado)
- **Fecha:** 2026-10-18
- **Motivo:** la note y el review_reason interpretaban "el doble está bearish = el DXY está bearish (glosario)"; el referente correcto es DOL (el objetivo/liquidez apunta abajo; contexto s-001405–s-001417 — depende de dónde están los objetivos de TF alta; s-001229 + f-004059). Hallado por la verificación independiente post-remediation (DVR-02).
- **Anotación anterior:** notes con equivalencia DXY.
- **Anotación nueva:** notes con lectura DOL + marcador de corrección en review_reason; statement (garble preservado) intacto.
- **Evidencia revisada:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001411|s-001411]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/transcript#^s-001229|s-001229]] · [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/frames/f-004059.png|f-004059]]
- **Resultado:** notes corregidas; verdict/epistemic intactos.

---

Nota de contexto: las correcciones de fidelidad hechas durante la integración
previa a la publicación (pre-remediation) están documentadas en
[[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/review-notes|review-notes]] §Decisiones de integración y en las notas de cada claim.
## am-ch03-001

- **Claim:** [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0018|c-0018]]
- **Fecha:** 2026-10-23
- **Motivo:** hardening del contrato de consumo — la proyección de `unresolved_questions` en CLAIMS.md (renderer 2026-10-23) sometió las dudas al chequeo V11 y reveló que la nota usaba sintaxis de ID (`f-000249`) para un frame HIPOTÉTICO nunca extraído (sugerencia de extracción, no referencia).
- **Antes:** «…si el integrador la quiere, extraer [ID de frame hipotético para 00:02:49]» (nunca extraído; ver nota).
- **Después:** «…si el integrador la quiere, extraer el frame de 00:02:49 si hace falta.» (el texto original queda en el historial git de claims.jsonl y en el run `~/mke/clutifx-contract-hardening-20261023/`)
- **Evidencia:** no aplica (nota de duda; statement, evidence y veredicto intactos).
- **Resultado:** CORREGIDO — misma instrucción sin pseudo-referencia; validate_library PASS.
