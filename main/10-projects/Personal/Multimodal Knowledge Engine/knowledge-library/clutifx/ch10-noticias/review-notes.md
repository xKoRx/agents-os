# review-notes — ch10-noticias (Clutifx · Chapter 10)

Notas de revisión del run del 2026-10-21 (Manager local GLM, ONE-SHOT). Contrato: `course-knowledge-extraction` v1.2 + hardening ch03–ch09 (incluida la regla anti-resolución-de-ambigüedades añadida en el cierre de ch09).

## Condiciones del run

- **Contención del host durante TODO el capítulo**: echo-core (157 % permanente) + go tests de otra sesión (lab-v4-shot4, churn intermitente ~100-220 %) sobre 8 cores. Load 8,9-17,4 según el momento; PSI «some» hasta 36 %. Ningún proceso ajeno fue tocado. El ASR rindió 0,24× (pronóstico del preflight: 0,25-0,30× — cumplido).
- **[1210] transitorios del proveedor**: 5 muertes de worker (extractor bloque 6; revisores min 5, 8, 21, 25), TODAS recuperadas con un retry del worker completo (protocolo ch08). 0 [1310].
- **Checkpoint 5 min**: PASS — bloque 1 + ola min 0-4 VALID; proyección registrada ~269 min/h-video (1,22× del baseline ch09 aceptado; OVER >2× del objetivo 120 → continuado con registro, mismo criterio ratificado por el Owner en ch09). Real final 284 min/h-video (ver README).

## Defecto de naming cazado y corregido en vuelo (clase «95 s → f-000095»)

1. El prompt del extractor de bloque 1 listó frames base con nombres decimales incorrectos (f-000119 por «1:59»); los archivos en disco SÍ estaban correctos por fórmula (1:59 = f-000159). El worker detectó el desajuste contra `ls`, leyó los reales y citó sólo los existentes. Lección ya registrada en CH09 LEARNED #1 se re-confirma: los ejemplos de naming en prompts deben generarse por la fórmula.
2. El frame final del video lo extraje a mano como `f-002148` (segundos crudos 2148) — el revisor de min35 lo cazó («2148 s → f-003548») y se renombró antes de publicar. Dos ocurrencias del mismo defecto de clase en un run: la fórmula es la única autoridad.

## Correcciones aplicadas en integración (antes de publicar; ~50 adjudicadas)

- **Evidencia completada** (12): segmentos de frontera que las citas requerían (s-000100, s-000238, s-000551, s-000722, s-001246, s-001506, s-001645, s-001725 movido de b3-28 a b3-29, s-001905, s-001925, s-002519/s-002639, s-003050, s-003533 ×2).
- **Literalidad restaurada** (12): «Stop los [ASR]», «la noticia que pasaba», «stop loss por ahí», «fijaos qué ratio nos podía dar aquí» (glosa inferencial fuera), «estaríamos posicionados», «día bastante consolidación [ASR]», «este PI [ASR] (= CPI)», «la noticia de las 8» (literal) + nota 8:15, «por lo tanto» en orden causal, «otro long aquí», «por aquí a las cuatro y media» (04:30 del eje, no 16:30), «dos, tres ratios [ASR]», «pero ya se haya sacado unos toplos [ASR]», «si la noticia fuera una vez [ASR]».
- **Kinds ajustados por hedges** (6): rule→observation (b3-09, b5-08), procedure→example (b3-14, b4-02), rule→warning (b5-30); b4-02 también por ser operación de UN día.
- **visual_hints falsos corregidos/anulados** (6): b1-23 (calendario Forex Factory, NO gráfico), b2-17 (tarjeta PMI del Excel, NO gráfico), b2-24 (anulado: diálogo de intervalo tapa el gráfico), b2-25/b3-25 matizados, b5-16 (8h/480M en pantalla, no «9 horas»).
- **Adjudicaciones visuales con palabra dicha preservada** (6): «My Forex»→Myfxbook (c-0020; URL+sitio verificados por el Manager en f-000350/f-000359), «DXI»→DXY (f-002459/f-002504/s-003344; NO DOL), «GDP»→GBP (f-002504), «USDCAT/USDCHEF»→USDCAD/USDCHF (f-000600); «USDJPI» queda SIN confirmar; «target sub» marcado [ASR; candidato Turtle Soup].
- **Frame refs mal anotadas** (3): b1-15/b1-16 (f-000159→f-000239/f-000248) y b1-28/b1-29 (f-000359→f-000559) — herencia del prompt con nombres decimales.

## Contradicciones documentadas (sin armonizar)

- **8:15 vs 8:30/8:45** (ch02/ch07): c-0069 y c-0165 UNCERTAIN con CONTRADICTION; el ejemplo del 4-jun dice «ocho y cuarto» y el frame muestra 08:15. Puede ser noticia distinta — requiere audio (q-ch10-001).
- **Vela de las 7 vs de las 8**: c-0164 UNCERTAIN; resolución visual de min28 documentada en q-ch10-002 (misma vela, etiqueta por temporalidad).
- **«en 6h no hay nada» vs «teníamos un primer rango»**: c-0113 UNCERTAIN; lecturas de ambos revisores en q-ch10-003.
- c-0032 (condición «misma dirección» sobre garble) y c-0030 (observación visual del extractor refutada por pantalla) completan los 6 UNCERTAIN, todos visibles y sin resolución artificial.

## Verificación visual independiente del Manager

El Manager leyó directamente f-000350 y f-000359 (3:50/3:59) para adjudicar la aparente contradicción entre revisores de min3 y min5 (resultaron mirar minutos distintos; ambos tenían razón). Lección: ante desacuerdo entre revisores sobre contenido de pantalla, leer el frame directamente cuesta menos que una revisión nueva.

## Proyecciones y validación

- CLAIMS.md 199 filas; FRAMES.md 98 frames (36 base por manifiesto + 62 bajo demanda; 91 citados, 7 contextuales sin claims — inventariados, patrón ch09).
- Veredicto final: 199 claims = 193 SUPPORTED + 6 UNCERTAIN + 0 UNVERIFIED; 0 superseded; epistemic 197 instructor_statement + 2 visual_observation.

## CIERRE (closeout 2026-10-21 — anotación append-only; el registro histórico de arriba no se reescribe)

Tras la publicación, el closeout targeted corrigió: am-ch10-001 (c-0030 superseded por c-0200 — la observación Myfxbook-min5 refutada ya no está activa) y am-ch10-002 (adjudicación de las horas «8 y cuarto»: c-0165 y c-0164 SUPPORTED, c-0069 UNCERTAIN con contradicción retirada, q-ch10-001/002 RESUELTAS, q-ch10-015 nueva). Métricas vigentes en el README (200 claims: 196 S + 3 U activos + 1 superseded; AGENT_WALL 266 min/h-video conciliado por epochs — la cifra 284 de arriba era la estimación de cierre del run). Ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch10-noticias/AMENDMENTS|AMENDMENTS]].
