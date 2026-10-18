---
type: skill
schema_version: 1
name: course-knowledge-extraction
description: >
  Extrae el conocimiento de un video de curso (clase hablada sobre material
  visual mayormente estático) y lo publica como biblioteca por capítulo:
  transcripción ordenada como recurso citable, 1 frame por minuto + frames
  específicos bajo demanda, claims con cita de evidencia y una revisión POR
  MINUTO (nunca por claim). Diseñada para ser escalable a campañas de cientos
  de videos con API, modelo local o subagentes. Prohíbe explícitamente el
  pipeline MKE V2 completo con revisión por claim (costo real medido: 44 h por
  un video de 34 min).
scope: global
created: "2026-10-18"
updated: "2026-10-18"
entities: []
related:
  - "[[Multimodal Knowledge Engine]]"
aliases:
  - extraccion de conocimiento de cursos
  - course video knowledge
  - knowledge library de cursos
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/extract
  - domain/knowledge
---

# course-knowledge-extraction

## Purpose

Convertir un video de curso en una **biblioteca de conocimiento auditable y
re-consultable**, por capítulo. El diseño está validado empíricamente contra el
run ch01 de Clutifx (2026-10-14/16): el transcript es el 85-90% del
conocimiento; las imágenes aportan en dos casos acotados — resolver deícticos
("este rango" = cuál rectángulo) y capturar datos visuales (niveles, esquemas,
timeframe en pantalla) — y la verificación por claim con llamada individual es
el error de diseño que mató ese run.

## Minimal Read

1. Esta skill completa (es autocontenida).
2. Post-mortem del run caro: `mke/multimodal-knowledge-engine/docs/runbooks/video-knowledge-exploitation.md` §10 (fuera del vault; opcional).
3. Biblioteca de referencia ya publicada: `10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/clutifx/ch01-introduccion/` (estructura a imitar).

## REGLAS DURAS — prohibiciones (no negociables)

1. **PROHIBIDO ejecutar el pipeline MKE V2 completo** (`mke plan/acquire/windows/pipeline`) sobre videos de curso con proveedor de subagentes. Su contrato exige UNA llamada VLM por claim → ~1.200 llamadas seriales por video de 30-60 min → 2+ días. Medido, no especulado.
2. **PROHIBIDO revisar claim por claim** (una llamada de verificación por cada afirmación). La revisión es POR MINUTO: una llamada valida todos los claims de ese minuto juntos.
3. **PROHIBIDO inspección 1 fps** y ventanas de 15 s. El 87% de los frames son el mismo chart quieto; la sobre-fragmentación multiplica llamadas sin aumentar conocimiento.
4. **PROHIBIDO continuar un grind serial que se desvía >2× del tiempo estimado sin checkpoint con el owner.** Se mide throughput tras procesar los primeros ~5 minutos de video y se reporta el ETA real antes de seguir.
5. **PROHIBIDO inventar relaciones causales** que el transcript no enuncia (error dominante del run caro: 38 INSUFFICIENT, casi todos "X, y después, Y" convertidos en "X PORQUE Y"). Relación solo si hay nexo explícito (porque, para, si, habilita, requiere).
6. **PROHIBIDO un claim sin cita de evidencia** (segmento de transcript; frame solo si es visual).
7. Si existe API con saldo (<1 USD/video estimado), es el proveedor preferido; el flujo es idéntico y solo cambia la velocidad. Subagentes/modelo local son válidos con este flujo simple.

## Contrato de recursos y citas

Toda referencia es textual y reversible: cualquier documento puede citar, y
cualquier agente posterior puede re-consultar el recurso citado.

| Recurso | Nombre/formato | Ejemplo |
|---|---|---|
| Frame de minuto | `frames/f-<HHMMSS>.png` (siempre fin de minuto: acumula los dibujos) | `frames/f-001259.png` = minuto 12:59 |
| Frame bajo demanda | `frames/f-<HHMMSS>.png` (segundo exacto de la cita) | `frames/f-001234.png` = 00:12:34 |
| Segmento de transcript | `transcript.md` ordenado, cada segmento con id `s-<HHMMSS>` | `s-001234: "esto de aquí es un rango"` |
| Claim | `claims.jsonl`, id `c-<NNN>` | `c-0042` |
| Cita de evidencia | `[mm:ss]` en prose; `{"evidence": ["s-001234","f-001234"]}` en JSONL | `[12:34]`, `[f-001234]` |

Extracción de frame puntual (determinística, sin herramientas pesadas):

```bash
ffmpeg -ss <HH:MM:SS[.ms]> -i <video.mp4> -frames:v 1 -q:v 2 frames/f-<HHMMSS>.png
```

Frames bajo demanda: SOLO cuando el transcript dice "esto de aquí / pinto esto
/ miren el gráfico / nombra un nivel numérico / cambia de timeframe" y el frame
de minuto no despeja la referencia. Presupuesto orientativo: ≤1 frame/minuto
obligatorio + ~0,5-1 bajo demanda. Un video de 1 h ⇒ 60-120 frames total.

## Estructura de la biblioteca (por capítulo)

```
10-projects/Personal/Multimodal Knowledge Engine/knowledge-library/<curso>/<capitulo>/
├── README.md          # provenance: sha256 del video, herramientas, fecha, estado
├── documentation.md   # la síntesis por conceptos, todo citado
├── claims.jsonl       # los claims atómicos con veredicto y evidencia
├── transcript.md      # recurso: transcript ordenado con ids s-<HHMMSS>
└── frames/            # recurso: f-<HHMMSS>.png
```

`claims.jsonl` — un JSON por línea:

```json
{"id":"c-0042","minute":12,"kind":"rule|parameter|observation|procedure",
 "statement":"El stop loss va seguro por debajo del low del Turtle Soup",
 "evidence":["s-001156","f-001199"],"verdict":"SUPPORTED|UNCERTAIN|UNVERIFIED","notes":""}
```

## Procedure

1. **Setup** (minutos): crear el directorio del capítulo. Extraer transcript
   (faster-whisper o equivalente; el MKE repo tiene `asr/` reutilizable en
   `/home/kor/mke/multimodal-knowledge-engine`) → escribir `transcript.md` con
   ids `s-<HHMMSS>`. Guardar sha256 del video en el README.
2. **Frames base** (minutos): 1 frame por minuto SIEMPRE (fin de minuto,
   `-ss MM:59.5`) → `frames/f-<HHMMSS>.png`. No deduplicar agresivamente: 60
   frames/h pesan poco y son la red de re-consulta.
3. **CHECKPOINT TEMPRANO** (obligatorio): procesar los primeros 5 minutos de
   video completos (pasos 4-5). Medir tiempo real. Reportar al owner el ETA
   para el video completo. Si se desvía >2× del objetivo (≤2 h subagentes /
   ~15 min API por hora de video), PARAR y re-decidir. Este control existe
   porque el run caro se detectó 12 horas tarde.
4. **Knowledge desde transcript** (el corazón): en bloques de ~5-10 min,
   extraer claims atómicos pero sensatos (separar reglas de parámetros y de
   observaciones; NO micro-fragmentar: ~10-25 claims/minuto de clase densa,
   mucho menos en pausas). Cada claim cita sus `s-<HHMMSS>`. Los deícticos
   ("esto", "este rango") se marcan para el paso 5 si el contexto textual no
   los resuelve.
5. **Frames bajo demanda + revisión POR MINUTO** (una llamada por minuto): un
   solo llamado recibe el transcript del minuto + el frame de ese minuto + los
   claims propuestos, extrae los frames específicos que necesite, y emite el
   veredicto por claim: SUPPORTED / UNCERTAIN (dudoso, no adivinar) — y
   CORRIGE causalidad inventada y deícticos sin resolver. Con API/modelo local
   es una llamada estructurada; con subagentes, un subagente por minuto
   (paralelizables 5-10 en vuelo).
6. **Composición**: `documentation.md` — síntesis por conceptos del capítulo,
   cada afirmación con su cita `[mm:ss]` y `[f-<HHMMSS>]` cuando es visual.
   Construida SOLO sobre claims SUPPORTED; los UNCERTAIN pueden mencionarse
   explícitamente como dudosos, nunca como hechos.
7. **Publicación**: README con provenance (video sha256, herramienta, modelo,
   fecha, conteos) + claim counts por veredicto. La biblioteca se considera
   entregable con UNCERTAINs visibles; NO se re-trabaja sin pedido del owner.

Costo objetivo verificado: video de 1 h ⇒ **≤2 h con subagentes, ~10-15 min y
<1 USD con API**. (El run caro: 44 h para 34 min.)

## Complement / corrección posterior (el punto de todo el contrato)

Como TODOS los recursos quedan en la biblioteca y toda afirmación cita
recursos, corregir o ampliar es determinista: se le pide a un agente
"completa/corrige el claim `c-0042` revisando `f-001234` y el transcript
`12:30-13:00`" y el agente re-consulta los recursos exactos sin re-procesar
nada. Prohibido re-procesar el video completo para corregir un punto: siempre
se opera sobre los recursos citados. Si falta un frame para resolver una duda
nueva, se extrae con el mismo comando de ffmpeg y se nombra con el mismo
esquema (queda documentado para la próxima consulta).

## Output

```text
COURSE_KNOWLEDGE: <curso>/<capitulo> => DONE|PARTIAL
claims: N (SUPPORTED n / UNCERTAIN n)
frames: n obligatorios + n bajo demanda
throughput: <min de video>/min real vs objetivo
biblioteca: <ruta absoluta>
```

## Anti-patrones (leitmotiv del run ch01 caro)

- "Mientras respondo bundles avanzo" — NO: responder bundles sin medir ETA es
  cómo se quemaron 44 h. Checkpoint temprano, siempre.
- "El motor exige X" — el motor (MKE V2) exige lo que exige SU contrato; este
  flujo NO corre ese contrato. No mezclar.
- "Mejor más granular para más precisión" — NO: el 5% de errores lo captura la
  revisión por minuto; la granularidad por claim solo compró 40× costo.
