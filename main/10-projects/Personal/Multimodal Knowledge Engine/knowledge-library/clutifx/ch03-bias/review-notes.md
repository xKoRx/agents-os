# ch03-bias — Particularidades de la revisión

Notas del integrador sobre lo preservado, los garbles de ASR y el uso de
frames. Citas: `[mm:ss]` → transcript; `c-NNNN` → [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS|CLAIMS]]/`claims.jsonl`.

## Particularidades del transcript preservadas

- **El capítulo no da una definición verbal única de "bias"**: el concepto se enseña por procedimiento (derivar la dirección desde TFs altas hacia las bajas) y por la pizarra final de m40 (f-004059). Ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/concepts|concepts]] §BIAS.
- **c-0061**: el review lo marcó UNCERTAIN porque el statement fundía dos dichos ("un poco feo" y "muy difícil de operar") con una atribución deíctica; adjudicado en integración separando ambas citas literales ([[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/CLAIMS#c-0061|c-0061]]).
- **c-0131/c-0132**: frase truncada por corte de bloque (m23→m24); el claim cruza la frontera con la continuación en s-002402 (contexto de frontera del payload).
- **c-0154**: statement corregido al dicho literal "Estoy emitiendo la temporada más alta" [ASR]; la lectura ("empezando por/eliminando la temporalidad más alta") es interpretación en notes, jamás en el statement.
- **c-0181**: "Ahora no me acuerdo si fue stop loss o no... vale, sí fue stop loss" — la autocorrección del instructor se preserva tal cual (fidelidad al dicho, no "limpieza").
- **c-0183/c-0184**: mea culpa del instructor (operó contra los rangos bullish de 8h/12h/6h y le saltó el stop) preservado completo: es warning didáctico del propio curso.
- **Gestión c-0106**: "completa esto" queda con referente abierto (ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/OPEN-QUESTIONS#q-ch03-002|q-ch03-002]]); f-001935 se extrajo e inspeccionó y NO desambigua sin inferencia — no se citó como evidencia.

## Garbles de ASR (preservados tal cual en statements; interpretación en notes o aquí)

| ASR | Real |
|---|---|
| "GDP" / "GVP" | GBP (libra esterlina; confirmado por el par en pantalla en f-000042/f-000659) |
| "el doble" / "dole" / "dolls" / "el dol" | el DOL (draw on liquidity; ver [[10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch03-bias/OPEN-QUESTIONS#q-ch03-001|q-ch03-001]] sobre DOL vs DXY) |
| "vallas" / "el vayas" / "bayas" | bias |
| "power free" / "Pablo III" | Power of 3 |
| "load" / "logo" | low |
| "loan" | long (s-000549) |
| "veris" | bearish |
| "bullies" / "rango bullies" | rango bullish |
| "fellow swing" | failure swing (c-0136) |
| "target sub" / "tartle sub" | Turtle Soup (contexto) |
| "la vela de estrés" | la vela de las tres (s-003511) |
| "rango a jabón" / "rangos de favor" | rango a favor / rangos a favor |
| "temporadas" / "temporales" | temporalidades |
| "NCP" | NFP |
| "stop los" | stop loss |
| "en lo don" | en London (con tensión interna: "porque no es London" en s-003053) |
| "un red más baja" | una temporalidad más baja (s-003030) |
| "comprate" | ¿"completó"? (s-003157) — sin lectura confirmada |
| "emitiendo la temporada más alta" | ¿"empezando por/eliminando la temporalidad más alta"? (s-002948) — sin lectura confirmada |
| "me curso intermedio" | (en) el curso intermedio (s-002348) |
| "te cuentas" | te encuentras (s-003745) |
| "lleve esto" | probablemente "tome/toque esto" (s-003101) — preservado literal |
| "sentí" | ¿semanal? (s-000188 aprox.) — sin lectura confirmada |
| "el turn" | ¿target? (s-000749) — sin lectura confirmada |
| "en chip" (s-002509) / "FB" (s-002217) / "es después de la vez" (s-002319) / "ahí es en ti con libro de" (s-001902) | sin recuperación fiable |
| "para doble ya la sesión" (s-004056) | la pizarra de m40 (f-004059) resuelve el sentido: "12h–8h–6h–4h = DOL sesión" |

## Uso de frames

- 42 frames base (fin de minuto; manifiesto `frames/.base_frames`) + 79 bajo demanda extraídos y verificados visualmente por los MINUTE_REVIEWERs (presupuesto 1–3/min respetado; exceso puntual justificado por recorrido de gráfico continuo — p. ej. minuto 33 usó 5).
- 74 frames citados en `claims.jsonl.evidence`; los 35 claims `visual_observation` tienen frame verificado (check V07).
- Frames extraídos e inspeccionados pero NO citados por no resolver el deíctico: f-000103 (c-0007), f-000135, f-001450/f-002238, f-001935 (c-0106), f-002145, f-003059/3005/3009/3014, f-003501. Registro honesto: un frame que no muestra lo afirmado no se cita.
- "Cambiar intervalo" (diálogo del replay) tapa parte del gráfico en algunos stills de 30:05–30:14; los claims de ese tramo quedan soportados por transcript.

## Decisiones de integración

- **Unión de evidencia**: `evidence` = s-ids del extractor ∪ `verified_evidence` del revisor (ordenado, sin duplicados). Las adiciones puntuales del revisor (p. ej. s-000148 en c-0011, s-003355 en c-0174, s-003920 en c-0202, s-004014 en c-0205) cerraban frases citadas.
- **Correcciones de statement aplicadas** (12): garbles restaurados o interpretados a notes (c-0014, c-0034, c-0154, c-0161, c-0183), deícticos literales (c-0125, c-0133, c-0196, c-0202), modalidad/restauración literal (c-0015, c-0023, c-0124, c-0131, c-0205). Ninguna cambió la proposición; sólo fidelidad al dicho.
- **Reclassificaciones epistemic** (35 claims a visual_observation): todas con frame verificado dentro de `verified_evidence`; el revisor del minuto las propuso explícitamente. c-0043 se revirtió a instructor_statement (el revisor lo mandó mantener; el frame es corroboración de contexto).
- **1 UNCERTAIN adjudicado** (c-0154) con nota en el claim; 0 UNVERIFIED; 0 contradicciones.
