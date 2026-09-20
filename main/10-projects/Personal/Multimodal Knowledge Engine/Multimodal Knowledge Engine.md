---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Personal]]"
parent:
sprint:
start: 2026-09-17
due:
progress: 5
repo: xKoRx/multimodal-knowledge-engine
jira:
prs:
aliases:
  - Course Intelligence Engine
  - Course Intelligence
  - Multimodal Knowledge
  - Motor de conocimiento multimodal
  - Motor de conocimiento de cursos
  - Procesamiento de cursos de trading
tags:
  - kind/project
  - area/personal
created: "2026-09-17"
updated: "2026-09-17"
---

# Multimodal Knowledge Engine

> [!info]+ Proyecto
> **Estado:** active · **Repo:** `xKoRx/multimodal-knowledge-engine` · **Arquitectura:** ADR-001 cerrada para POC y M0 SPEC Freeze completado · **Ejecución:** lista para iniciar SPEC-00A desde el baseline congelado del repo; implementación y runtime todavía no certificados. Esta nota es autoridad de producto/decisiones; el detalle ejecutable vive en `docs/architecture/` y `docs/specs/` del repo. Proyecto independiente de Hermes, Echo y Echo Forge.

## 🎯 Objetivo

**Objetivo único e invariable:** transformar fuentes multimodales heterogéneas en documentación técnica de alta calidad y una base de conocimiento explotable para derivar conceptos, reglas, procedimientos, estrategias, ideas, contradicciones e hipótesis. La POC usa cursos de trading en video, pero `curso` y `video` son casos de entrada, no el dominio del producto. Futuras fuentes pueden incluir entrevistas, podcasts, conferencias, webinars, screencasts, audio, imágenes, presentaciones y documentos. El procesamiento multimedia es un medio, no el producto final. No construir motores de trading, backtesting, frontend ni infraestructura por anticipación.

- **M0 — Source → Knowledge:** POC funcional sobre UN video real autorizado de 1–2 h, comenzando con fragmento configurable de 5–10 min. Audio, demostraciones visuales silenciosas, gráficos, SQX, presentaciones y parámetros deben producir Markdown técnico y JSONL estructurado, con evidencia y tiempos reales. El fragmento de procesamiento NO es frontera semántica.
- **M1 — Corpus → Documentation:** procesar múltiples fuentes de manera incremental y consolidarlas en documentación coherente por unidad lógica/corpus, evitando duplicados y manteniendo cobertura/procedencia. La primera expansión será por videos y cursos.
- **M2 — Knowledge → Intelligence:** cruzar fuentes/corpus, reconstruir reglas y estrategias con condiciones y excepciones, identificar equivalencias, desacuerdos contextualizados, ideas e hipótesis falsables. Ninguna idea se presenta como rentable o verdadera sin evidencia independiente suficiente.

**Función objetivo:** fidelidad, cobertura de contenido recuperable, trazabilidad, utilidad y calidad documental. Tokens, cantidad de frames, tamaño de Markdown y complejidad no son objetivos. El backend multimodal inicial de desarrollo para M0 es `GLM-5.3-Flash`; es una implementación de `VLMProvider`, no parte del dominio ni autoridad de conocimiento.

## 📊 Estado actual

- **2026-09-17 — M0 SPEC Freeze COMPLETADO:** el repo contiene arquitectura M0 y SPECs congeladas `00A → 00B → 01 → 02 → 03-A → 03-C → 04`; no hay decisiones arquitectónicas materiales abiertas para comenzar 00A. El baseline exacto es el HEAD final de `master` posterior al freeze y debe quedar fijado en el mandato de implementación.
- **2026-09-17 — Product-first:** SPEC-00A reemplaza el antiguo runtime-first. El primer desarrollo debe producir cuanto antes `mke process video.mp4 --transcript transcript.json --vlm glm` → `source.json`, `evidence/`, `knowledge.jsonl`, `documentation.md`. SQLite/resume no entran hasta SPEC-02.
- **2026-09-17 — Local runtime desacoplado:** SPEC-00B valida Whisper/Qwen/Ollama/LM Studio/M4/Kronos contra los mismos contratos externos. Un backend local `NO_GO` no rediseña el core ni bloquea por sí solo SPEC-01 mientras exista un VLM aceptado; una insuficiencia del contrato vuelve a manager como `PLAN_CONFLICT`.
- **2026-09-17 — Diseño CERRADO para ejecución experimental:** ADR-001 se mantiene: interpretación de gráficos, cierre verificable de preguntas, benchmark emparejado A/C y dos gates internos de SPEC-03. No reiniciar debate arquitectónico sin evidencia física contradictoria.
- **Delegación autorizada:** futuro mandato `Manager → Implementer → QA`, cada SPEC `IMPLEMENT → TEST → QA`; `PASS` autoavanza, `CORRECT` corrige y revalida, `BLOCKED` detiene dependientes mientras manager busca solución en scope, `NO_GO` detiene la vía afectada. Solo escalar humano por permisos, gasto nuevo, cambio de scope, otros sistemas o decisión irreversible.
- **Sin implementación física todavía:** repo y branch remotos están verificados, pero video autorizado, credenciales/runtime GLM, runtimes locales, memoria/rendimiento y calidad real se verifican durante ejecución. No inventar métricas ni disponibilidad.
- **Agents-OS:** proyecto principal `owner: me`; subproyecto ejecutor [[M0 Execution]] materializado el 2026-09-17 con tarea puente única en WIP. Workspace del repo: `~/mke/` (fuera del vault). Cierre de sesión solo por solicitud explícita.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Multimodal Knowledge Engine / `xKoRx/multimodal-knowledge-engine` | `master` verificada | HEAD final del SPEC Freeze; fijar SHA exacto al despachar 00A | esta nota + ADR-001 | `docs/architecture/architecture.md` + `docs/specs/SPEC-00A-product-spike.md` … `SPEC-04-integration-benchmark.md` | `READY_FOR_IMPLEMENTATION`; comenzar por 00A |

## 1. Contrato funcional

**Entrada M0:** video procesable con derechos suficientes; original inmutable SHA-256; streams/PTS, configuración, versión y presupuesto. **Salida M0:** `Evidence`, `KnowledgeItem`, `Procedure` y `Relation`, JSONL reproducible, Markdown navegable, reporte de cobertura/incertidumbre/QA y referencias que llevan al origen y tiempo real. Cada afirmación material tiene identidad, evidencia, clase epistémica y estado; cada paso de un procedimiento tiene evidencia POR PASO.

**Documentación DE VALOR:** debe recuperar conceptos, condiciones, reglas, valores legibles, procedimientos SQX y ejemplos de gráficos sin tener que rever el video completo, con referencias para auditar. No aprobar un resumen narrativo bonito. Declarar expresamente dudas, ilegibilidad, omisiones y contradicciones. El motor no certifica exhaustividad ni verdad empírica.

Ventana, evento y conocimiento tienen identidades separadas; un instante tiene ventana principal y contexto vecino solapado sin duplicar conocimiento. Una explicación puede cruzar muchas ventanas y una excepción posterior debe actualizar y revalidar la regla. `Raw → Extracted → Aligned → Interpreted → Verified → Published` son hitos y checkpoints, NO flujo irreversible.

## 2. ADR-001 — Bounded Hybrid Evidence Acquisition (ACCEPTED FOR POC DESIGN)

Monolito CLI Go. Cobertura visual independiente del ASR, densidad configurable y reproducible; investigador opcional pide evidencia adicional con protocolo cerrado. El código gobierna procedencia, límites, estados, tiempos, publicación e idempotencia. El modelo propone preguntas e interpretaciones; no controla shell, fuente externa ni política de verdad.

**Experimento A/C:** `adaptive_investigation=false` versus `true`, mismo ejecutable, source/hash, ASR, índice, evidencia inicial, modelos/backend, grounding, consolidación y publisher. Única diferencia controlada: adquisición adaptativa. Comparar techo común de recursos y separadamente costos operativos reales. Medir conocimiento correcto incremental, errores/regresiones y costo, NO longitud documental. Si A pasa y C no aporta calidad correcta útil, retirar C por KISS; si ninguna pasa, NO_GO. B no se implementa por puntos ciegos visuales. Cobertura visual no exige decodificación exhaustiva permanente: barrido denso versus densidad reducida es experimento, no decisión fija.

No Kafka, Temporal, base vectorial, frontend, API pública, microservicios, Postgres/MinIO obligatorios ni cluster en POC. No fijar umbrales/fps/paquetes o estrategias distribuidas antes de medir. Clips nativos solo si el backend exacto acredita soporte; secuencias de frames primero.

## 3. Arquitectura y persistencia

```text
Fuente original / identidad / reloj
   ├── ASR completo y timestamps
   └── cobertura visual independiente + índice de actividad
          → Planning Context NO autoritativo
          → selección inicial reproducible
          → Investigator opcional ↔ solicitudes tipadas + Evidence Acquisition
          → Knowledge Reconstruction
          → Integrity Validator + Grounding Reviewer
          → consolidación global y revalidación
          → JSONL + Markdown + QA/benchmark
```

Go posee dominio/estados, presupuestos, request validation, dependencias, idempotencia, referencias y política de publicación. FFmpeg/ffprobe, ASR, análisis visual y VLM son ejecutores especializados, no autoridad de conocimiento. `hint → question → evidence → claim → review → publication`; no publicar sugerencias del planning context como hechos.

Persistencia evoluciona por necesidad: SPEC-00A usa filesystem simple para demostrar producto; SPEC-02 introduce SQLite + filesystem, journal/reconciliación y `request_id ≠ acquisition_key`. Original/evidencia inmutables, hash de inputs y versiones de configuraciones/prompts/extractores/modelos, escritura temporal → validar/hash → rename atómico mismo FS → estado durable. Invalidar descendientes afectados, no repetir ASR/media si cambia solo reviewer. No interfaces por struct, logs con secretos/media/transcripción ni ejecución de instrucciones encontradas dentro de la fuente.

## 4. Extracción visual, gráficos y tiempo

Inspección barata de toda la cobertura declarada, independiente del habla, produce activity timeline; adquisición recupera evidencia de resolución original a demanda. Registrar frames inspeccionados, artefactos adquiridos, imágenes inferidas, intervalos sin observar y candidatos descartados por separado. Cobertura temporal ≠ de eventos ≠ semántica.

Señales candidatas: histogramas/bordes/luminancia, diferencias por tiles/ROI, persistencia antes-durante-después, transitorios, anclas incluso en escenas estables, actividad continua en gráficos, OCR diferencial selectivo y deduplicación perceptual contextual. PySceneDetect/OpenCV/optical flow son opciones, no obligaciones. Anclas 30–60 s y densidades son hipótesis experimentales. Evento de 2 s se recupera solo si el frame contiene contenido realmente dentro de ese intervalo. No inferir cifras de OCR/upscale ambiguo.

**Gráficos financieros:** conservar frame completo, ROI con coordenadas originales y secuencia temporal ordenada/PTS cuando la interpretación requiera movimiento. Registrar instrumento/timeframe, vela/región, anotaciones, valores y condiciones SOLO cuando legibles; en otro caso `UNKNOWN`/`UNREADABLE`. Diferenciar cursor, zoom/pan y actualización real del gráfico; nunca interpretar desplazamiento visual como cambio de mercado sin evidencia. Dos gráficos parecidos conservan identidad temporal. Golden incluye interpretación de gráfico, no solo captura correcta.

Solicitudes `FRAME`, `REGION`, `COMPARE`, `SEQUENCE`, `FIND_CHANGE`; `FIND_CHANGE` usa detector determinista en intervalo local. Cada solicitud contiene ID de pregunta/source/segmento o evento, tipo, intervalo, justificación, límites y ROI opcional. Go valida identidad, intervalo, geometría, permisos, presupuesto y dedup ANTES del extractor. Acotar rondas, solicitudes, frames, imágenes efectivamente inferidas, secuencias, tokens, memoria, tiempo, disco y reintentos; agotamiento ⇒ `INCOMPLETE`.

**Cierre del investigator:** cada pregunta relevante termina `ANSWERED` (evidencia concreta y grounding suficiente), `UNRESOLVED`, `UNREADABLE` o `BUDGET_EXHAUSTED`. Go valida estados terminales, no acepta solo «ya entendí» del LLM. Las incertidumbres se publican; no alegar comprensión completa por falta de preguntas nuevas.

**Tiempo canónico:** stream, PTS real, time base racional, ordinal, tiempo normalizado, instante solicitado y realmente recuperado, intervalos, hash y geometría original de ROI. Gestionar VFR, offset audio/video, start_time y discontinuidades. Un seek solicitado no es una referencia válida hasta verificar PTS efectivo y tolerancia fundada en frames vecinos.

## 5. Conocimiento y revisión

Modelo mínimo: `Evidence` (fuente/tiempo/ROI/hash), `KnowledgeItem` (`claim|concept|rule|parameter|observation`, alcance, condiciones, evidencia, estado), `Procedure` (pasos ordenados, condiciones, excepciones, evidencia POR PASO) y `Relation` (dependencia, excepción, equivalencia, contradicción). Preguntas/requests son journal, no entidades ontológicas nuevas.

Clases epistémicas: `INSTRUCTOR_SAID`, `VIDEO_OBSERVED`, `MODEL_INFERRED`, `EXTERNALLY_CHECKED`, `EMPIRICALLY_VALIDATED`; no usar validación empírica sin prueba reproducible externa. Integrity Validator determinista: IDs, original/hash, tiempos reales, ROI, versiones/artefactos. Integrity PASS no prueba que un claim esté semánticamente soportado. Grounding Reviewer stateless: solo claim/paso versionado, evidencia/transcripción necesaria y clase, SIN historial/razonamiento del generador; devuelve `GROUNDING_SUPPORTED|GROUNDING_CONTRADICTED|GROUNDING_INSUFFICIENT`. Error, JSON inválido o reviewer ausente nunca equivale a SUPPORTED. Solo `INTEGRITY_PASS && GROUNDING_SUPPORTED` permite `SUPPORTED_BY_AUTOMATED_REVIEW`, nunca `VERIFIED_TRUE`.

Consolidación entre ventanas y revisión posterior de cambios/dependientes; preservar diferencias entre audio y pantalla sin decidir automáticamente cuál es cierto. Mostrar `CONTRADICTED`, `INSUFFICIENT`, `UNREADABLE`, `INCOMPLETE`. JSONL ordenado/versionado es intercambio estructurado canónico; Markdown es proyección legible y nunca fuente de reconstrucción estructurada.

## 6. QA por agentes y benchmark

**El usuario no valida manualmente cada SPEC.** Un agente implementador entrega; un agente QA separado verifica contra fuente ORIGINAL, artefactos y contratos, jamás solo contra el Markdown generado. Un agente evaluador prepara `GoldenManifest` desde ORIGINAL ANTES de ver A/C; otro agente revisa críticos cuando sea posible. Congelar golden antes de evaluación, no introducirlo en prompts del engine ni recalibrar sobre él y presentar el mismo run como test independiente.

**Honestidad del benchmark:** etiquetar `AGENT_GOLDEN`, `AGENT_REVIEWED`, jamás `HUMAN_VERIFIED`. PASS significa pruebas/revisión automatizada sobre ese material, NO calidad humana certificada ni generalización a todos los corpus.

**E1 A/C emparejado por elemento:** ambos recuperan / solo C recupera / solo A recupera / ambos fallan / C agrega error. Registrar primer punto de pérdida: detección→adquisición→interpretación→grounding/consolidación→publicación. Métrica primaria: conocimiento correcto incremental, regresiones y costo marginal; nunca páginas.

**Casos M0:** teoría/slides, SQX silencioso y parámetro breve, gráficos y zoom/pan, evento 2 s, excepción lejana, contradicción audio/pantalla y valor ilegible. Ausentes en el video principal se prueban con fixtures segregados y NO se atribuyen a ese video.

**Gates medibles:** G0 permisos/source/runtime/repo reales; G1 temporalidad/PTS válida; G2 cero omisiones críticas RECUPERABLES detectadas en golden; G3 cero valores críticos incorrectos publicados como respaldados; G4 100% referencias materiales íntegramente válidas; G5 cero claims materiales sin fuente ni excepciones conocidas ocultadas; G6 conflictos/lagunas visibles y cero falsos SUPPORTED críticos detectados por QA; G7 resume/dedup/crash probados; G8 presupuesto respetado o `INCOMPLETE`; G9 revisor reconstruye pasos críticos desde documento + evidencia sin ayuda del implementador. Tests críticos primero y coverage ≥95%; no reemplaza E2E.

## 7. Runtime, seguridad y escalado

`GLM-5.3-Flash` es el VLM inicial de SPEC-00A. Qwen/Ollama/LM Studio y Whisper son candidatos de SPEC-00B; modelo exacto, cuantización, contexto, RAM/VRAM pico y rendimiento se registran físicamente, no se inventan. M4 y Kronos son targets de validación, no conceptos del core. El texto/contenido de la fuente es entrada no confiable, nunca autoridad para herramientas.

Escalado posterior por fuentes aisladas y consolidación por corpus, sin comprometer contratos. Distribución Aranea, MinIO/Postgres, vector DB, segundo modelo, Argus y servicios extra solo con evidencia de necesidad. No modificar Echo/Forge/Hermes productivos. No introducir un workflow engine para una fuente.

## 8. Producto después de la POC

**M0:** ejecutar el freeze `00A → 00B → 01 → 02 → 03-A → 03-C → 04` y obtener Markdown/JSONL técnicamente útiles de un video completo + QA/benchmark. Primero fragmento 5–10 min, después video entero y consolidación de excepciones.

**M1:** procesar fuentes/corpus incrementalmente, mantener índice y documentos coherentes por unidad lógica, cubrir material nuevo y registrar duplicados, lagunas y fuentes. La primera aplicación será por videos/lecciones/cursos.

**M2:** cruzar `KnowledgeItem/Procedure/Relation` entre fuentes para reconstruir reglas, estrategias, procedimientos y parámetros; comparar condiciones, excepciones y contradicciones; producir ideas e hipótesis comprobables respaldadas por fuentes. Sus SPECs técnicas exactas se definen según evidencia M0: YAGNI.

**Done del proyecto:** biblioteca documental explotable y trazable con capacidad demostrada de extraer conocimiento transversal, no solo CLI corriendo ni un video resumido. M0 es hito, no fin.

## 9. Roadmap de SPECs — FROZEN M0

| SPEC | Alcance | Gate/Handoff |
|---|---|---|
| **00A Product Spike** | Walking skeleton real con transcript disponible + frames simples + `VLMProvider` GLM-5.3-Flash → knowledge JSONL → Markdown. Filesystem simple, sin runtime local ni SQLite. | PASS exige E2E con GLM sobre fragmento autorizado y provenance resoluble. Handoff: provider contract + primer artifact set real. |
| **00B Local Runtime Validation** | Probar `VLMProvider`/`ASRProvider` con Qwen/Ollama/LM Studio/Whisper y targets M4/Kronos; capability matrix por target. | Cada target termina PASS/NO_GO/BLOCKED. Un local NO_GO no rediseña ni bloquea el core mientras exista VLM aceptado. |
| **01 Media Foundation** | Source/hash, ffprobe/ffmpeg, timeline/PTS real, transcript normalizado, frames, visual activity/anchors y coverage independiente del ASR. | QA de VFR/seek, silencio, evento corto, cobertura e identidad. |
| **02 Evidence Acquisition** | `FRAME/REGION/COMPARE/SEQUENCE/FIND_CHANGE`, budgets, `request_id ≠ acquisition_key`, SQLite+FS, dedupe, crash/resume/reconciliation. | QA física de artifacts + DB, dedupe y crash matrix. |
| **03-A Knowledge Baseline** | Evidence → reconstruction → integrity → grounding → consolidation/revalidation → JSONL → Markdown, sin investigator. “Determinista” = replay con outputs provider grabados + orquestación/serialización deterministas. | Documento real + QA PASS obligatorio antes de C. |
| **03-C Investigator** | Preguntas acotadas → requests tipadas → Evidence adicional → EXACTO pipeline 03-A, con estados terminales y hard budgets. | QA de límites, typed-only acquisition, regresión y reuse del pipeline. |
| **04 Integration & Benchmark** | Video completo, golden agente congelado antes de A/C, A/C emparejado, recovery, invalidation, calidad/costo, docs finales. | G0–G9 + decisión A/C basada en conocimiento correcto incremental/regresiones/costo; no diseñar M1/M2. |

Los contratos detallados, inputs/outputs, persistencia, errores, idempotencia, criterios binarios, tests, QA gates y handoffs son canónicos en el repo. Agents-OS conserva este resumen, estado y decisiones.

## 10. Próximo mandato ejecutable

> Manager: bootstrap canónico; verificar que `master` coincide con el baseline del SPEC Freeze; crear el subproyecto `owner: agent` mediante el materializador y enlazar una sola tarea puente; despachar SOLO SPEC-00A al Implementer con `docs/architecture/architecture.md` + `docs/specs/SPEC-00A-product-spike.md`; usar QA separado; tras PASS encadenar automáticamente 00B→01→02→03-A→03-C→04 dentro del scope. El primer objetivo físico es `mke process video.mp4 --transcript transcript.json --vlm glm` produciendo `source.json`, `evidence/`, `knowledge.jsonl`, `documentation.md`. El golden se crea recién en SPEC-04 desde ORIGINAL y antes de mostrar A/C al evaluador. Si faltan video autorizado, credenciales/runtime o permisos al llegar al gate físico correspondiente, emitir un único `BLOCKED` preciso. No cerrar Agents-OS automáticamente.

## 🧩 Subproyectos

- [[M0 Execution]] (`owner: agent`, en `agentes/`): ejecución del mandato M0 desde el freeze; planificador único de la implementación. Materializado el 2026-09-17 al iniciar el mandato.

## ✅ Tareas

- [x] Convergencia arquitectónica ADR-001 A/C; versiones previas superseded. #owner/me #type/admin #area/personal
- [x] Fijar objetivo único, QA delegado, contratos visual/gráficos, gates y milestones M0/M1/M2. #owner/me #type/admin #area/personal
- [x] Renombrar proyecto a Multimodal Knowledge Engine y vincular repo `xKoRx/multimodal-knowledge-engine`; mantener nombre anterior como alias histórico. #owner/me #type/admin #area/personal
- [x] Congelar arquitectura ejecutable M0 y SPEC-00A/00B/01/02/03/04 en el repo; product spike antes de infraestructura local. #owner/me #type/admin #area/personal
- [/] [[M0 Execution]] arrancar + seguimiento (subproyecto `owner: agent`; campaña 00A→04 COMPLETA 2026-09-20: rama `m0-implementation` pusheada @ `77b8d6f`, veredicto M0 **BLOCKED físico** — requiere video autorizado + credenciales GLM para la certificación de SPEC-04; hallazgos de capacidad documentados en [[M0 Execution]]) #owner/me #type/supervision #area/personal
- [ ] Tras M0 PASS, delegar M1/M2 con SPECs basadas en evidencia, hasta biblioteca transversal. #owner/me #type/supervision #area/personal

## 📆 Bitácora

- **2026-09-17:** debate de dos IAs convergió en ADR-001; implementación y runtime sin verificar. Arquitectura inicial A/B/C y nueve SPECs superseded en historia Git.
- **2026-09-17 — cierre operativo:** usuario fija objetivo documental/explotación de conocimiento, QA por agentes y dos gates 03; no hay ejecución física ni creación de subproyecto confirmada.
- **2026-09-17 — rename:** se adopta **Multimodal Knowledge Engine** y repo `xKoRx/multimodal-knowledge-engine`; `Course Intelligence Engine` queda como alias histórico; M0 sigue sobre un video de curso de trading.
- **2026-09-17 — M0 SPEC Freeze:** repo remoto `master` verificado; se reemplaza runtime-first por product-first `00A→00B→01→02→03-A→03-C→04`. Se persisten arquitectura y seis documentos SPEC. Review adversarial resuelve riesgos materiales: runtime local no bloquea el core por target, determinismo definido por replay/control determinista, SQLite diferido hasta SPEC-02, adapters GLM/Qwen/Whisper detrás de dos fronteras externas reales, provenance obligatorio y QA automatizable con fixtures/replay más E2E físico. Próximo paso: implementación 00A desde baseline exacto del freeze.
- **2026-09-17 — mandato de implementación iniciado:** subproyecto [[M0 Execution]] materializado (`owner: agent`), tarea puente en WIP, repo clonado en workspace externo `~/mke/`, baseline freeze `e5f9e97` verificado como HEAD de `master`, rama de desarrollo `m0-implementation` creada desde ese baseline. SPEC-00A despachada al Implementer con QA separado.

## 🧭 Decisiones

- Nombre canónico: **Multimodal Knowledge Engine**; `Course Intelligence Engine` queda como alias histórico.
- ADR-001: híbrido fijo/adaptativo falsable, A obligatorio antes de C, un único toggle, B no implementada.
- `GLM-5.3-Flash` es backend VLM inicial de desarrollo y NO entra al dominio; `VLMProvider` y `ASRProvider` son las únicas fronteras externas que justifican interfaces anticipadas.
- Product-first: 00A demuestra documentación real antes de construir runtime/persistencia completos; SQLite entra en 02 cuando existen resume/reconciliation reales.
- Determinismo 03-A significa pipeline/replay reproducible con respuestas grabadas, no promesa de inferencia LLM determinista.
- JSONL es publicación estructurada canónica; Markdown es proyección.
- QA por agentes sin falsa certificación humana; gates PASS autoavanzan, scope/permisos bloquean, modelo/costo no se inventa.
- Go + SQLite/FS en M0 maduro, ASR y cobertura visual independientes, timestamps reales, integrity + grounding.

## 🔗 Docs / Links

- Repo: `xKoRx/multimodal-knowledge-engine`.
- Repo canónico M0: `docs/architecture/architecture.md`, `docs/specs/SPEC-00A-product-spike.md`, `docs/specs/SPEC-00B-local-runtime.md`, `docs/specs/SPEC-01-media-foundation.md`, `docs/specs/SPEC-02-evidence-acquisition.md`, `docs/specs/SPEC-03-knowledge-pipeline.md`, `docs/specs/SPEC-04-integration-benchmark.md`.
- [[agents-os]], [[agents-os-bootstrap]], [[agents-os-agent-project-workflow]], [[agents-os-session-close]].
- Historia de versiones previas: Git de esta misma entidad; `Course Intelligence Engine` permanece como alias, no arquitectura alternativa.

## 💡 Ideas diferidas

- Clips nativos, modelos pequeños de clasificación, Postgres/MinIO, Argus, cluster, corpus masivo y búsqueda vectorial solo con pruebas de necesidad. No desviar M0.
