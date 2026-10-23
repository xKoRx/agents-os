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

v1.1 (2026-10-18): hardening tras Chapter 02 — evidencia visual estructurada,
contexto de frontera, naming determinista de frames, glosario como input,
checkpoint total vs agentes y validación final obligatoria (ver §Hardening v1.1).
v1.2 (2026-10-18): navegación Obsidian y conocimiento iterativo — CLAIMS.md/FRAMES.md
como proyecciones deterministas, anchors de bloque en transcript, wikilinks con
ruta completa desde vault root, identidad permanente de claims, AMENDMENTS/
OPEN-QUESTIONS, protocolo de aclaración acotada y contrato de consulta para
agentes (ver §Navegación e iteración).

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

El HHMMSS se genera SIEMPRE por fórmula desde los segundos reales (jamás
concatenado a mano — 2/18 workers de ch02 escribieron horas en vez de minutos):

```python
filename = f"f-{seconds // 3600:02d}{(seconds % 3600) // 60:02d}{seconds % 60:02d}.png"
```

Frames bajo demanda: SOLO cuando el transcript dice "esto de aquí / pinto esto
/ miren el gráfico / nombra un nivel numérico / cambia de timeframe" y el frame
de minuto no despeja la referencia. Presupuesto orientativo: ≤1 frame/minuto
obligatorio + ~0,5-1 bajo demanda (un video de 1 h ⇒ 60-120 frames), SIN tope
rígido cuando el instructor cambia de gráfico/temporalidad o dibuja estructuras:
se registra el exceso y su justificación en review-notes. En cursos con recorrido
de gráfico continuo (ch02: 2,6/min) el presupuesto se declara por bloque, no global.

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
   ids `s-<HHMMSS>`. Guardar sha256 del video en el README. Cargar el
   `GLOSSARY.md` del curso y su tabla de garbles ASR conocidos como input de
   extractores y revisores (contexto, no permiso para sustituir palabras
   parecidas sin respaldo).
2. **Frames base** (minutos): 1 frame por minuto SIEMPRE (fin de minuto,
   `-ss MM:59.5`) → `frames/f-<HHMMSS>.png`. No deduplicar agresivamente: 60
   frames/h pesan poco y son la red de re-consulta.
3. **CHECKPOINT TEMPRANO** (obligatorio): procesar los primeros 5 minutos de
   video completos (pasos 4-5). Medir tiempo real POR SEPARADO: throughput de
   subagentes (extracción+revisión) y tiempo total del proceso (ASR,
   orquestación, integración y publicación NO se esconden — ch02: pipeline
   99 min/h-video ✓ pero total observado por el owner 2h06 para 17 min,
   dominado por ASR). Reportar ambos al owner. Si el proyectado se desvía >2×
   del objetivo (≤2 h subagentes / ~15 min API por hora de video), PARAR y
   re-decidir. Este control existe porque el run caro se detectó 12 horas tarde.
4. **Knowledge desde transcript** (el corazón): en bloques de ~5-10 min,
   extraer claims atómicos pero sensatos (separar reglas de parámetros y de
   observaciones; NO micro-fragmentar: ~10-25 claims/minuto de clase densa,
   mucho menos en pausas). Cada claim cita sus `s-<HHMMSS>`. Los deícticos
   ("esto", "este rango") se marcan para el paso 5 si el contexto textual no
   los resuelve.
5. **Frames bajo demanda + revisión POR MINUTO** (una llamada por minuto): un
   solo llamado recibe el transcript del minuto UNIÓN todos los segmentos
   citados por sus claims (contexto de frontera: jamás truncar evidencia en el
   límite del minuto — en ch02 produjo 4 UNCERTAIN artificiales; usar
   `scripts/make_minute_payload.py`) + el frame de ese minuto + los claims
   propuestos, extrae los frames específicos que necesite, y emite UN
   veredicto por claim: SUPPORTED / UNCERTAIN (dudoso, no adivinar) — y
   CORRIGE causalidad inventada y deícticos sin resolver. El integrador
   verifica cardinalidad entrada=salida (`scripts/validate_review.py`); si no
   coincide, `MINUTE_REVIEW = INVALID`. Con API/modelo local es una llamada
   estructurada; con subagentes, un subagente por minuto (5-10 en vuelo).
6. **Composición**: `documentation.md` — síntesis por conceptos del capítulo,
   cada afirmación con su cita `[mm:ss]` y `[f-<HHMMSS>]` cuando es visual.
   Construida SOLO sobre claims SUPPORTED; los UNCERTAIN pueden mencionarse
   explícitamente como dudosos, nunca como hechos. La síntesis tampoco puede
   resolver categóricamente una ambigüedad material que el claim citado
   mantiene abierta (garble [ASR], TERM_DISAMBIGUATION_REQUIRED, q-\<curso\>-NNN
   OPEN) salvo que aporte evidencia adicional adjudicada: preserva la palabra
   dicha y declara la interpretación como candidata no confirmada (regresión
   real ch09 DV09-001: «mover el stop a break even» publicado sobre el garble
   abierto «tarjeta breakable» de c-0015/q-ch09-002).
7. **Publicación + validación final**: README con provenance (video sha256,
   herramienta, modelo, fecha, conteos RECONCILIADOS contra los artefactos) +
   claim counts por veredicto. DONE exige: evidencia estructurada válida,
   provenance visual válida (todo visual_observation con frame verificado en
   `evidence`; una nota textual no sustituye la cita), conteos reconciliados,
   revisión semántica ejecutada y `scripts/validate_library.py` = PASS.
   "Todo SUPPORTED" NO basta para declarar DONE. La biblioteca se considera
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

## Términos especializados — normalización y desambiguación (hardening ch03, 2026-10-18)

1. **Una normalización de términos especializados NO está soportada por el hecho de aparecer en el glosario.** El glosario es contexto, no regla de sustitución ciega. Defecto real (ch03 c-0121): el ASR dice "al DOL" y el claim publicó "al DXY" "porque el glosario lo decía" — MATERIAL, corregido por supersession.
2. **TERM_DISAMBIGUATION_REQUIRED**: cuando un mismo garble del ASR admite dos o más términos con significados distintos (p.ej. "el doble" → DOL objetivo de liquidez vs DXY índice del dólar), el EXTRACTOR preserva la palabra dicha en el statement (con marca `[ASR]`) y anota los candidatos; el MINUTE_REVIEWER los contrasta contra el segmento citado, frames y contexto (¿es un nivel del gráfico? ¿un índice externo?); si no puede decidir, devuelve incertidumbre — jamás publica la interpretación como término.
3. **El statement publica la palabra dicha; la interpretación vive en notes/unresolved_questions.** Sustituir el término en el statement cambia materialmente la proposición → supersession (contrato v1.2).
4. **Chequeo SOURCE-FIRST determinista**: `scripts/check_term_sources.py <lib>` — por claim vivo, si el statement publica un término canónico de un grupo crítico (default: DOL/DXY con los garbles ambiguos "el doble/doll/dole/dolls" como aliases de grupo; extensible con `--groups`) y la evidencia citada no lo contiene: si la fuente dice otro CANÓNICO del grupo (case-insensitive: un "dol" minúscula del ASR cuenta) → MATERIAL FINDING; si la fuente sólo contiene un GARBLE AMBIGUO sin marca de adjudicación `[ASR]` en el statement → `TERM_DISAMBIGUATION_REQUIRED` (REVIEW). El chequeo detecta la necesidad de revisión; no decide el término — el reviewer SOURCE-FIRST adjudica con transcript, audio puntual, contexto y frames. Verificar con `scripts/tests/source_first_selftest.py` (casos 1 y 6/7 son los defectos reales de ch03 y ch02).
5. La verificación documental (DOCUMENTATION_VERIFIER) debe incluir este chequeo: que documentation.md concuerde con claims.jsonl NO basta, porque ambos pueden contener el mismo error.

## Hardening v1.1 — contratos añadidos tras Chapter 02 (2026-10-18)

1. **Contrato de evidencia**: toda observación visual material lleva frame
   DENTRO de `claims.jsonl.evidence` (además del s-id). `visual_hint` señala
   dónde mirar; el frame verificado es la cita. Chequeos V07/V08 del validador.
2. **Contexto de frontera**: payload del minuto = segmentos del minuto ∪
   segmentos citados por sus claims (contract test C de ch02 lo demuestra con
   los casos reales c-0067/c-0072).
3. **Naming determinista**: fórmula sobre segundos reales; los nombres
   históricos inválidos se declaran en `<biblioteca>/.deprecated_frame_names`
   (un `historical_invalid_name` es registro de auditoría, no cita vigente).
4. **Densidad visual**: sin tope rígido por minuto cuando el contenido lo pide;
   exceso registrado y justificado.
5. **Glosario como input**: GLOSSARY.md del curso + garbles conocidos entran en
   cada paquete de extractor y revisor.
6. **Checkpoint doble**: throughput de subagentes Y tiempo total, por separado,
   desde el checkpoint de 5 minutos.
7. **Validación final**: validate_library.py PASS + conteos reconciliados +
   revisión semántica antes de DONE.

### Scripts auxiliares (deterministas, stdlib-only)

```text
scripts/validate_library.py <lib> [--duration-seconds N]  # V01-V13; PASS|FAIL
                                                          # V11 exime los tokens dentro de wikilinks
                                                          # cross-chapter ([[…/CLAIMS#c-…]] o [[…/transcript#^s-…]]:
                                                          # su destino lo validan los checks W) — el token
                                                          # desnudo de otro capítulo sigue fallando
                                                          # (aclaraciones targeted am-ch09-*, regresión en
                                                          # fixtures_selftest caso I)
scripts/validate_review.py <payload.json> <review.json>   # cardinalidad R01-R04
scripts/integrate_reviews.py --run <run> --lib <lib> [minutos...]
                                                          # aplica reviews al pool y escribe
                                                          # claims.jsonl; el canónico SOLO se
                                                          # escribe con integración COMPLETA
                                                          # (todos los reviews del run + cobertura
                                                          # total del pool); una ejecución parcial
                                                          # escribe sólo claims.jsonl.partial y
                                                          # sale 1 (defecto real ch08: un run de un
                                                          # minuto sobrescribió el canónico desde
                                                          # el pool). Evidencia visual por clases:
                                                          # las f-* del pool sin verificar NO entran
                                                          # al canónico; entran las de
                                                          # verified_evidence del revisor y las
                                                          # targeted-adjudicadas con prueba en
                                                          # <run>/evidence-adjudications.json
                                                          # (defecto real ch10: refs f- adjudicadas
                                                          # se perdían en la fusión)
scripts/make_minute_payload.py <transcript.md> <claims> <min> <out>
scripts/tests/fixtures_selftest.py                        # red-green del validador
scripts/add_block_anchors.py <transcript.md>              # anchors ^s- idempotentes
                                                          # + bloques Obsidian independientes
scripts/render_claims_md.py <vault> <lib>                 # proyección CLAIMS.md (sin fecha)
scripts/render_frames_md.py <vault> <lib>                 # inventario FRAMES.md (clase base
                                                          # = frames/.base_frames, sin fecha)
scripts/wikilink_docs.py <vault> <lib> <doc.md>           # enlaza docs (--all-tokens|--bracketed)
scripts/tests/wikilink_selftest.py                        # red-green de checks W (11 casos)
scripts/tests/wikilinker_selftest.py                      # red-green del script wikilink_docs:
                                                          # absorción de citas, sin [[[, idempotencia
scripts/tests/anchors_selftest.py                         # red-green de anchors/bloques (7 casos)
scripts/tests/review_pipeline_selftest.py                 # payload emite key; validate_review
                                                          # acepta claim_key|key (5 casos)
scripts/tests/lifecycle_selftest.py                       # red-green de supersession safety
                                                          # (V14/V15/V16; 10 casos)
scripts/tests/evidence_safety_selftest.py                 # red-green de la seguridad de evidencia
                                                          # visual del integrador (5 casos; ch10)
scripts/check_term_sources.py <lib> [--groups JSON]       # SOURCE-FIRST: normalización de términos
                                                          # sin respaldo en la fuente = MATERIAL
scripts/tests/source_first_selftest.py                    # red-green del chequeo (caso real DOL/DXY)
```

Checks W (desde v1.2 + hardening ch03): links a archivos/headings/blocks
existentes (W01–W03), anchors únicos Y en bloques propios (W05), FRAMES.md
cubre frames (W06), PNG sin ruta completa inválido (W07), proyección CLAIMS.md
sincronizada en heading + statement + epistemic + verdict (W04/W09), wikilinks
equilibrados sin Markdown mal formado (W10).

## Navegación e iteración (v1.2)

**Wikilinks reales**: la biblioteca vive en un vault Obsidian. Todo enlace usa
ruta completa relativa al vault root ([[curso/capitulo/CLAIMS#c-0048|c-0048]],
[[…/transcript#^s-000716|07:16]], [[…/frames/f-000716.png|f-000716]]) — nunca
basenames ambiguos (cada capítulo tendrá transcript.md, CLAIMS.md y frames con
los mismos nombres). Los embeds ![[…]] se reservan para donde la imagen aporta
comprensión (principalmente examples/documentation); nunca masivos.

**Proyecciones deterministas** (no son segunda fuente de verdad; claims.jsonl
sigue siendo la autoridad máquina-legible y NO lleva sintaxis Obsidian):
- `transcript.md` con block id ` ^s-HHMMSS` por segmento (`add_block_anchors.py`,
  idempotente; parte del setup). Cada segmento debe ser un BLOQUE Obsidian
  independiente (línea en blanco/heading antes y después del anchor): un block
  id a mitad de párrafo es texto literal, no anchor — el validador lo exige (W05)
  y el script separa párrafos automáticamente.
- `CLAIMS.md` por claim (`render_claims_md.py`): heading estable `### c-XXXX`,
  verdict/epistemic/tiempo derivado de evidencia real, links a segmentos y frames.
  Sin fecha dinámica: misma entrada => mismos bytes cualquier día.
- `FRAMES.md` por frame (`render_frames_md.py`): timestamp + claims que lo citan;
  los frames contextuales no fuerzan relaciones. La clase base/bajo demanda es
  autoridad del manifiesto `frames/.base_frames` (capturas realmente ejecutadas),
  nunca una regla sobre nombres — sin manifiesto el renderer falla cerrado.

**Identidad permanente**: un `c-NNNN` publicado jamás se renumera por agregar
claims; los nuevos toman IDs nuevos. Correcciones que preservan la proposición
actualizan el claim (nota enmendada); si cambian materialmente la proposición,
el Manager adjudica claim nuevo y el anterior queda superseded sin romper
backlinks.

**Supersession safety y contrato de consulta** (hardening ch04, 2026-10-19):
distinguir GROUNDING_VERDICT (SUPPORTED/UNCERTAIN/UNVERIFIED — cómo se sostiene
el claim con la fuente) de LIFECYCLE_STATUS (activo vs reemplazado — si es
conocimiento vigente). No hay propiedad redundante: `superseded_by` presente
⇒ el claim es SUPERSEDED (historia preservada: conserva ID, evidencia y
adjudicación original, y siempre navega a su reemplazo). El reemplazo es
bidireccional (`superseded_by` ↔ `supersedes`, validado). **ACTIVE KNOWLEDGE =
claims WITHOUT `superseded_by`**: consultas, síntesis y documentación por
defecto usan sólo claims activos; los históricos se recuperan sólo para
auditoría o cuando el usuario pide expresamente versiones anteriores. El
renderer marca los reemplazados (`SUPERSEDED — HISTORICAL, NOT ACTIVE` +
`Replacement:` navegable) y el validador lo exige (V14 integridad, V15
proyección, V16 docs pedagógicos sin citas de reemplazados como vigentes,
V10 fila `Claims activos / superseded` en el README). Contract tests:
`scripts/tests/lifecycle_selftest.py`.

**Correcciones y dudas**: `AMENDMENTS.md` por capítulo (append-only:
amendment_id, claim_id, fecha, motivo, antes/después, evidencia, resultado —
sólo correcciones materiales, no regeneraciones cosméticas) y
`OPEN-QUESTIONS.md` por capítulo (ID estable `q-<curso>-NNN`, claim, pregunta,
evidencia, estado OPEN|RESOLVED). Una pregunta abierta NO degrada una regla
correctamente sustentada.

**Dudas materiales con vínculo estructural** (hardening 2026-10-23, defecto
real q-ch07-019): una contradicción entre claims activos SUPPORTED —dos
versiones dichas incompatibles del mismo hecho— es incompatible con consumir
cualquiera de ellas como confirmada, aunque cada claim sea fiel a su fuente.
Por eso: (a) toda pregunta OPEN **material** (afecta la verdad de lo afirmado,
no un garble/deíctico auxiliar) declara `**Materialidad: MATERIAL**` en su
entrada de OPEN-QUESTIONS — sin marcador es AUXILIAR y no bloquea; (b) los
claims que su entrada enlaza DEBEN referenciarla en su campo
`unresolved_questions` (vínculo estructural bidireccional, verificable), no
basta mencionarla en la documentación narrativa; (c) el preflight
`scripts/check_consumption_contract.py` valida la estructura del contrato por
curso (consumibles, guardados con duda material, grupos de contradicción) con
selftest rojo/verde en `scripts/tests/consumption_contract_selftest.py`. El
renderer proyecta `unresolved_questions` en CLAIMS.md (`**Dudas abiertas:**`),
así la superficie navegable muestra la duda donde se lee el claim. Aplicarlo
ANTES de declarar DONE del capítulo.

**Aclaración acotada** (sin reprocesar el capítulo): resolver claim por ID →
abrir statement y provenance ([[CLAIMS]]) → consultar segmentos citados →
inspeccionar frames citados → extraer sólo frames puntuales nuevos si hacen
falta → proponer aclaración → revisión acotada (worker MINUTE_REVIEWER targeted)
→ actualizar claims.jsonl → regenerar proyecciones afectadas → registrar
amendment → validar (validate_library.py). Nunca 18 revisiones de minuto por una
duda.

**Consulta por agentes** ("¿Qué enseña el curso sobre X?"): recorrer
COURSE-INDEX → GLOSSARY → documentación del capítulo → CLAIMS.md/claim exacto →
transcript/frame. Distinguir SUPPORTED / UNCERTAIN / UNVERIFIED / OPEN QUESTION /
instructor_statement / visual_observation. Si falta conocimiento, decirlo: los
vacíos NO se rellenan con conocimiento general; el contexto externo se etiqueta
explícitamente como no del curso.

**Contrato de consumo** (hardening 2026-10-23): SUPPORTED acredita **fidelidad
a la fuente** (segmentos/frames verificados), NO verdad objetiva ni ausencia
de contradicciones. El estado epistémico lo dan `epistemic`
(instructor_statement / visual_observation / model_inference) y `kind`; las
inferencias propias del extractor nunca se atribuyen a la fuente. El consumible
factual es `ACTIVE ∧ SUPPORTED ∧ evidencia resuelta` **con sus dudas
materiales adjuntas**: todo claim con referencia a una q-* OPEN MATERIAL
(`unresolved_questions`) se consume como CONSUMIBLE_CON_DUDA_MATERIAL — se
preservan TODAS las versiones dichas, se cita la pregunta abierta y NO se
elige arbitrariamente entre lecturas en contradicción (los claims de un grupo
de contradicción nunca sostienen un hecho definitivo ni una regla universal).
Las dudas auxiliares (garbles, deícticos sin q-* MATERIAL) acompañan como nota
sin bloquear el claim. Excluidos del conocimiento factual: SUPERSEDED,
UNCERTAIN, UNVERIFIED, legacy MKE V2, evidencia inexistente.

**Validación de navegación**: validate_library.py incluye checks W (links a
archivos/headings/blocks existentes, anchors únicos, proyecciones sincronizadas,
PNG sin ambigüedad, índices de curso resolubles) — PASS antes de publicar.

### Subagentes

Antes de despachar workers: cargar
`30-resources/agents/skills/course-knowledge-worker/SKILL.md` e incluirlo en
cada paquete con `ROLE = EXTRACTOR|MINUTE_REVIEWER|DOCUMENTATION_VERIFIER`,
ONE-SHOT, FRESH CONTEXT. El Manager pasa skill + rol + recursos concretos +
contrato de salida; no duplica las reglas largas en cada subprompt. Los workers
escriben a su spool; sólo el integrador toca los archivos canónicos.

## Anti-patrones (leitmotiv del run ch01 caro)

- "Mientras respondo bundles avanzo" — NO: responder bundles sin medir ETA es
  cómo se quemaron 44 h. Checkpoint temprano, siempre.
- "El motor exige X" — el motor (MKE V2) exige lo que exige SU contrato; este
  flujo NO corre ese contrato. No mezclar.
- "Mejor más granular para más precisión" — NO: el 5% de errores lo captura la
  revisión por minuto; la granularidad por claim solo compró 40× costo.
