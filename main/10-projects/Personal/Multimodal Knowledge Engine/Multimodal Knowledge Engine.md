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
progress: 0
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
> **Estado:** active · **Repo:** `xKoRx/multimodal-knowledge-engine` · **Arquitectura:** ADR-001 cerrada para POC, pendiente de validación física · **Ejecución:** delegación por agentes autorizada dentro de los gates; no hay implementación certificada. Esta nota es la única autoridad vigente. Proyecto independiente de Hermes, Echo y Echo Forge.

## 🎯 Objetivo

**Objetivo único e invariable:** transformar fuentes multimodales heterogéneas en documentación técnica de alta calidad y una base de conocimiento explotable para derivar conceptos, reglas, procedimientos, estrategias, ideas, contradicciones e hipótesis. La POC usa cursos de trading en video, pero `curso` y `video` son casos de entrada, no el dominio del producto. Futuras fuentes pueden incluir entrevistas, podcasts, conferencias, webinars, screencasts, audio, imágenes, presentaciones y documentos. El procesamiento multimedia es un medio, no el producto final. No construir motores de trading, backtesting, frontend ni infraestructura por anticipación.

- **M0 — Source → Knowledge:** POC funcional sobre UN video real autorizado de 1–2 h, comenzando con fragmento configurable de 5–10 min. Audio, demostraciones visuales silenciosas, gráficos, SQX, presentaciones y parámetros deben producir Markdown técnico y JSONL estructurado, con evidencia y tiempos reales. El fragmento de procesamiento NO es frontera semántica.
- **M1 — Corpus → Documentation:** procesar múltiples fuentes de manera incremental y consolidarlas en documentación coherente por unidad lógica/corpus, evitando duplicados y manteniendo cobertura/procedencia. La primera expansión será por videos y cursos.
- **M2 — Knowledge → Intelligence:** cruzar fuentes/corpus, reconstruir reglas y estrategias con condiciones y excepciones, identificar equivalencias, desacuerdos contextualizados, ideas e hipótesis falsables. Ninguna idea se presenta como rentable o verdadera sin evidencia independiente suficiente.

**Función objetivo:** fidelidad, cobertura de contenido recuperable, trazabilidad, utilidad y calidad documental. Tokens, cantidad de frames, tamaño de Markdown y complejidad no son objetivos. GLM Pro se utiliza para DESARROLLO por agentes, no inferencia masiva del corpus.

## 📊 Estado actual

- **2026-09-17 — Nombre y alcance generalizados:** `Course Intelligence Engine` pasa a ser **Multimodal Knowledge Engine**. El repo dedicado ya existe como `xKoRx/multimodal-knowledge-engine`. La POC sigue siendo un video de curso de trading; no ampliar M0 a otras fuentes antes de certificarlo.
- **2026-09-17 — Diseño CERRADO para ejecución experimental:** convergencia de dos IAs sobre ADR-001. Los cuatro hallazgos posteriores están incorporados: interpretación de gráficos, cierre verificable de preguntas, benchmark emparejado A/C y dos gates internos para SPEC-03. No reiniciar debate arquitectónico sin un fallo físico que lo justifique.
- **Delegación autorizada:** agentes hacen discovery, SPEC-00 y continúan por gates PASS dentro de scope efectivamente autorizado; revisor separado valida cada fase. No requieren aprobación humana para cada paso rutinario. Solo escalar permisos/derechos, presupuesto nuevo, scope externo o bloqueo irreparable. No prometer ejecución persistente si el entorno no la permite.
- **Sin validación física:** repo identificado, pero branch/base/workspace local, video/runtime y métricas todavía deben verificarse por preflight. No hay pruebas de modelo, memoria, rendimiento, código o calidad. No inventar ruta, permisos, SHA ni métricas.
- **Diseño superseded:** las nueve SPECs y variante B de la primera versión ya no aplican. Se conserva su historia en Git, no una segunda arquitectura vigente.
- **Agents-OS:** proyecto principal `owner: me`; proyecto ejecutor `owner: agent` se creará con materializador canónico y `parent: [[Multimodal Knowledge Engine]]` cuando exista entorno apto. Una tarea puente humana, planificador único en el subproyecto. No fingir que se creó ya. Cierre de esta sesión exclusivamente por solicitud explícita.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Multimodal Knowledge Engine / `xKoRx/multimodal-knowledge-engine` | `master` declarada por GitHub; verificar localmente | SHA por verificar | [[Multimodal Knowledge Engine#1. Contrato funcional]] | [[Multimodal Knowledge Engine#9. Roadmap de SPECs]] | Discovery autorizado; desarrollo bloqueado hasta preflight y SPEC-00 PASS |

## 1. Contrato funcional

**Entrada M0:** video procesable con derechos suficientes; original inmutable SHA-256; streams/PTS, configuración, versión y presupuesto. **Salida M0:** `Evidence`, `KnowledgeItem`, `Procedure` y `Relation`, JSONL reproducible, Markdown navegable, reporte de cobertura/incertidumbre/QA y referencias que llevan al origen y tiempo real. Cada afirmación material tiene identidad, evidencia, clase epistémica y estado; cada paso de un procedimiento tiene evidencia POR PASO.

**Documentación DE VALOR:** debe recuperar conceptos, condiciones, reglas, valores legibles, procedimientos SQX y ejemplos de gráficos sin tener que rever el video completo, con referencias para auditar. No aprobar un resumen narrativo bonito. Declarar expresamente dudas, ilegibilidad, omisiones y contradicciones. El motor no certifica exhaustividad ni verdad empírica.

Ventana, evento y conocimiento tienen identidades separadas; un instante tiene ventana principal y contexto vecino solapado sin duplicar conocimiento. Una explicación puede cruzar muchas ventanas y una excepción posterior debe actualizar y revalidar la regla. `Raw → Extracted → Aligned → Interpreted → Verified → Published` son hitos y checkpoints, NO flujo irreversible.

## 2. ADR-001 — Bounded Hybrid Evidence Acquisition (ACCEPTED FOR POC DESIGN)

Monolito CLI Go. Cobertura visual independiente del ASR, densidad configurable y reproducible; investigador opcional pide evidencia adicional con protocolo cerrado. El código gobierna procedencia, límites, estados, tiempos, publicación e idempotencia. El modelo propone preguntas e interpretaciones; no controla shell, fuente externa ni política de verdad.

**Experimento A/C:** `adaptive_investigation=false` versus `true`, mismo ejecutable, source/hash, ASR, índice, evidencia inicial, modelos/backend, grounding, consolidación y publisher. Única diferencia controlada: adquisición adaptativa. Comparar techo común de recursos y separadamente costos operativos reales. Medir conocimiento correcto incremental, errores/regresiones y costo, NO longitud documental. Si A pasa y C no aporta calidad correcta útil, retirar C por KISS; si ninguna pasa, NO_GO. B (ASR+anclas mínimas+agente) no se implementa por puntos ciegos visuales. Cobertura visual no exige decodificación exhaustiva permanente: barrido denso versus densidad reducida es experimento, no decisión fija.

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

Go: dominio/estados, presupuestos, request validation, dependencias, idempotencia, referencias y política de publicación. FFmpeg/ffprobe, ASR, análisis visual y VLM son ejecutores especializados, no autoridad de conocimiento. `hint → question → evidence → claim → review → publication`; no publicar sugerencias del planning context como hechos.

Ejecución local secuencial, SQLite + filesystem y CLI con run/inspect/resume. Bloqueo verificable por run/source. Original/evidencia inmutables, hash de inputs y versiones de configuraciones/prompts/extractores/modelos, escritura temporal → validar/hash → rename atómico mismo FS → journal; reconciliación tras crash. `request_id` ≠ `acquisition_key`; deduplicar efecto lógico sin prometer exactly-once físico. Invalidar descendientes afectados, no repetir ASR si cambia reviewer. No interfaces por struct, logs con secretos/media/transcripción ni ejecución de instrucciones encontradas dentro de la fuente.

## 4. Extracción visual, gráficos y tiempo

Inspección barata de toda la cobertura declarada, independiente del habla, produce activity timeline; adquisición recupera evidencia de resolución original a demanda. Registrar frames inspeccionados, artefactos adquiridos, imágenes inferidas, intervalos sin observar y candidatos descartados por separado. Cobertura temporal ≠ de eventos ≠ semántica.

Señales candidatas: histogramas/bordes/luminancia, diferencias por tiles/ROI, persistencia antes-durante-después, transitorios, anclas incluso en escenas estables, actividad continua en gráficos, OCR diferencial selectivo y deduplicación perceptual contextual. PySceneDetect/OpenCV/optical flow son opciones, no obligaciones. Anclas 30–60 s y densidades son hipótesis experimentales. Evento de 2 s se recupera solo si el frame contiene contenido realmente dentro de ese intervalo. No inferir cifras de OCR/upscale ambiguo.

**Gráficos financieros:** conservar frame completo, ROI con coordenadas originales y secuencia temporal ordenada/PTS cuando la interpretación requiera movimiento. Registrar instrumento/timeframe, vela/región, anotaciones, valores y condiciones SOLO cuando legibles; en otro caso `UNKNOWN`/`UNREADABLE`. Diferenciar cursor, zoom/pan y actualización real del gráfico; nunca interpretar desplazamiento visual como cambio de mercado sin evidencia. Dos gráficos parecidos conservan identidad temporal. Golden incluye interpretación de gráfico, no solo captura correcta.

Solicitudes `FRAME`, `REGION`, `COMPARE`, `SEQUENCE`, `FIND_CHANGE`; `FIND_CHANGE` usa detector determinista en intervalo local. Cada solicitud contiene ID de pregunta/source/segmento o evento, tipo, intervalo, justificación, límites y ROI opcional. Go valida identidad, intervalo, geometría, permisos, presupuesto y dedup ANTES del extractor. Acotar rondas, solicitudes, frames, imágenes efectivamente inferidas, secuencias, tokens, memoria, tiempo, disco y reintentos; agotamiento ⇒ `INCOMPLETE`.

**Cierre del investigator:** cada pregunta relevante termina `ANSWERED` (evidencia concreta y grounding suficiente), `UNRESOLVED`, `UNREADABLE` o `BUDGET_EXHAUSTED`. Go valida estados terminales, no acepta solo «ya entendí» del LLM. Las incertidumbres se publican; no alegar comprensión completa por falta de preguntas nuevas.

**Tiempo canónico:** stream, PTS real, time base racional, ordinal, tiempo normalizado, instante solicitado y realmente recuperado, intervalos, hash y geometría original de ROI. Gestionar VFR, offset audio/video, start_time y discontinuidades. Un seek solicitado no es una referencia válida hasta verificar PTS efectivo y tolerancia fundada en frames vecinos.

## 5. Conocimiento y revisión

Modelo mínimo: `Evidence` (fuente/tiempo/ROI/hash), `KnowledgeItem` (`claim|concept|rule|parameter|observation`, alcance, condiciones, evidencia, estado), `Procedure` (pasos ordenados, condiciones, excepciones, evidencia POR PASO) y `Relation` (dependencia, excepción, equivalencia, contradicción). Preguntas/requests son journal, no entidades ontológicas nuevas.

Clases epistémicas: `INSTRUCTOR_SAID`, `VIDEO_OBSERVED`, `MODEL_INFERRED`, `EXTERNALLY_CHECKED`, `EMPIRICALLY_VALIDATED`; no usar validación empírica sin prueba reproducible externa. Integrity Validator determinista: IDs, original/hash, tiempos reales, ROI, versiones/artefactos. Integrity PASS no prueba que un claim esté semánticamente soportado. Grounding Reviewer stateless: solo claim/paso versionado, evidencia/transcripción necesaria y clase, SIN historial/razonamiento del generador; devuelve `GROUNDING_SUPPORTED|GROUNDING_CONTRADICTED|GROUNDING_INSUFFICIENT` con motivo/IDs. Mismo VLM con contexto separado NO garantiza independencia de errores. Error, JSON inválido o reviewer ausente nunca equivale a SUPPORTED. Solo `INTEGRITY_PASS && GROUNDING_SUPPORTED` permite `SUPPORTED_BY_AUTOMATED_REVIEW`, nunca `VERIFIED_TRUE`.

Consolidación entre ventanas y revisión posterior de cambios/dependientes; preservar diferencias entre audio y pantalla sin decidir automáticamente cuál es cierto. Mostrar `CONTRADICTED`, `INSUFFICIENT`, `UNREADABLE`, `INCOMPLETE`. JSONL ordenado/versionado es intercambio estructurado; Markdown es proyección legible con índice, procedimientos, gráficos, reglas, excepciones, preguntas, cobertura y enlaces relativos a evidencias; nunca reconstruir JSONL desde Markdown.

## 6. QA por agentes y benchmark

**El usuario no valida manualmente cada SPEC.** Un agente implementador entrega; un agente QA separado verifica contra fuente ORIGINAL, artefactos y contratos, jamás solo contra el Markdown generado. Un agente evaluador prepara `GoldenManifest` desde ORIGINAL ANTES de ver A/C, anota hechos/eventos, condiciones, valores, timestamps/ROI, criticidad y legibilidad; otro agente revisa críticos cuando sea posible. Congelar golden antes de evaluación, no introducirlo en prompts del engine ni recalibrar sobre él y presentar el mismo run como test independiente. Separar roles y contextos; distintos modelos si disponibles, pero no dependencia obligatoria.

**Honestidad del benchmark:** etiquetar `AGENT_GOLDEN`, `AGENT_REVIEWED`, jamás `HUMAN_VERIFIED`. Agentes pueden compartir sesgos: PASS significa que pasaron las pruebas y revisión automatizada en ese material, NO calidad humana certificada ni generalización a todos los corpus. El gold humano queda como evaluación externa optativa posterior, no gate cotidiano.

**E1 A/C emparejado por elemento:** ambos recuperan / solo C recupera / solo A recupera (regresión) / ambos fallan / C agrega error. Registrar primer punto de pérdida: detección→adquisición→interpretación→grounding/consolidación→publicación. Métrica primaria: conocimiento CORRECTO incremental, regresiones y costo marginal; nunca páginas. Comparación bajo techo de inferencia común y segunda operacional por consumo real. Experimentos complementarios: E2 denso/reducido; E3 global/ROI + OCR; E4 frame/par/secuencia; E5 backend y memoria físicos; E6 crash/reintentos/invalidación.

**Casos M0:** teoría/slides, SQX silencioso y parámetro breve, gráficos y zoom/pan, evento 2 s, excepción lejana, contradicción audio/pantalla y valor ilegible. Ausentes en el video principal se prueban con fixtures segregados y NO se atribuyen a ese video. Un video no generaliza al corpus.

**Gates medibles para el golden evaluado:** G0 permisos/source/runtime/repo reales; G1 temporalidad/PTS válida; G2 cero omisiones críticas RECUPERABLES detectadas en golden; G3 cero valores críticos incorrectos publicados como respaldados; G4 100% referencias materiales íntegramente válidas; G5 cero claims materiales sin fuente ni excepciones conocidas ocultadas; G6 conflictos/lagunas visibles y cero falsos SUPPORTED críticos detectados por QA; G7 resume/dedup/crash probados; G8 presupuesto respetado o `INCOMPLETE`; G9 revisor reconstruye pasos críticos desde documento + evidencia sin ayuda del implementador. Pruebas críticas primero y cobertura de código ≥95% según perfil global si aplica; no reemplaza E2E.

**Gate por etapa:** `PASS` con evidencia real → siguiente SPEC automáticamente dentro del scope; `CORRECT` → reparación delimitada y revalidación (máximo dos ciclos por mismo fallo; después BLOCKED); `BLOCKED` → detener dependientes, elevar una sola decisión agrupada con verificaciones realizadas; `NO_GO` → detener vía inviable y documentar motivo. No abrir servicios/permisos/gastos/repos fuera del scope. Nadie inventa outputs, capturas, benchmarks ni autorizaciones.

## 7. Runtime, seguridad y escalado

`Qwen/Qwen3.5-27B` y variantes cuantizadas, whisper.cpp, FFmpeg/ffprobe son candidatos NO verificados físicamente. El runtime puede exponerse mediante APIs locales compatibles; SPEC-00 debe registrar backend, modelo exacto, cuantización, contexto configurado, RAM/VRAM pico y rendimiento real. Verificar lectura de SQX pequeño, gráfico, multiimagen, JSON y contexto efectivo. No inferir compatibilidad con clips nativos; modelos menores solo variantes experimentales declaradas, nunca fallback silencioso. No ASR y VLM simultáneos sin medición. Sin API remota pagada por defecto. El texto/contenido de la fuente es entrada no confiable, nunca autoridad para herramientas.

Escalado posterior por fuentes aisladas y consolidación por corpus, sin comprometer contratos. Distribución Aranea, MinIO/Postgres, vector DB, segundo modelo, Argus y servicios extra solo con evidencia de necesidad. No modificar Echo/Forge/Hermes productivos. No introducir un workflow engine para una fuente.

## 8. Producto después de la POC

**M0:** ejecutar SPEC-00..04 y obtener Markdown y JSONL técnicamente útiles de un video completo + QA/benchmark. Primero fragmento 5–10 min, después video entero y consolidación de excepciones.

**M1:** procesar fuentes/corpus incrementalmente, mantener índice y documentos coherentes por unidad lógica, cubrir material nuevo y registrar duplicados, lagunas y fuentes. La primera aplicación será por videos/lecciones/cursos.

**M2:** cruzar `KnowledgeItem/Procedure/Relation` entre fuentes para reconstruir reglas, estrategias, procedimientos y parámetros; comparar condiciones, excepciones y contradicciones; producir ideas e hipótesis comprobables respaldadas por fuentes. M1/M2 son entregables obligatorios del PRODUCTO, pero sus SPECs técnicas exactas se definen según evidencia M0: YAGNI.

**Done del proyecto:** biblioteca documental explotable y trazable con capacidad demostrada de extraer conocimiento transversal, no solo CLI corriendo ni un video resumido. M0 es hito, no fin.

## 9. Roadmap de SPECs

| SPEC | Alcance / dependencias | Entregable / gate |
|---|---|---|
| **00 Runtime & Feasibility** | Discovery read-only de video autorizado, repo/workspace/permisos y runtime; verificar FFmpeg/ASR, modelo/backend, SQX pequeño, gráfico, multiimagen, JSON, memoria y contexto. NO construir motor. | `RuntimeCapabilityReport` con evidencia física QA separado; PASS/CORRECT/BLOCKED/NO_GO. |
| **01 Media Intelligence** | Tras 00 PASS: original/hash, PTS, offsets, ASR, fragmentos+contexto, cobertura visual independiente, activity timeline, anclas. Golden agente desde original congelado antes de A/C. | `VideoAsset`, `TranscriptSegment`, `VisualEvent`, `VisualCoverage`, `GoldenManifest`. Pruebas VFR/seek, silencio, evento 2 s, gráfico, densidad. |
| **02 Evidence Acquisition** | Tras 01 PASS: requests tipadas, ROI/pares/secuencias, PTS real, SQLite/FS, límites, dedup, crash/resume. | `EvidenceRequest`, `EvidenceArtifact`, `AcquisitionResult` y pruebas negativas/recovery QA. |
| **03-A Baseline E2E** | Tras 02 PASS: interpretación, Knowledge, integrity, grounding, consolidación y revalidación, JSONL y Markdown mínimo, SIN investigator C. | Documento REAL y QA PASS antes de habilitar 03-C. |
| **03-C Investigator acotado** | Tras 03-A PASS: bucle de preguntas/requests y estados terminales bajo límites; mismo pipeline y publisher con toggle. | QA de decisiones, límites, errores y regresión; no reimplementar A. |
| **04 Publication & Experiment** | Tras A, C si 03-C PASS: documentación completa, benchmark golden congelado, A/C emparejado, ablaciones, costo y decisión. | `BenchmarkReport`, conocimiento/documentos, GO/CORRECT/NO_GO por variante con evidencia. |

Son **cinco SPECs numeradas**, con dos gates internos en 03; NO seis servicios. Cada SPEC fija repo, branch, SHA base, allowed files, presupuesto, tests, errores y evidencia antes de codificar. Agent manager coordina implementador y QA en contextos separados. La aprobación de este mandato AUTORIZA discovery read-only, SPEC-00 y encadenamiento de SPEC-01..04 dentro de los permisos verificados, solo tras PASS. No autoriza crear repo público, contratar servicios, editar otros proyectos ni inventar Git baseline. Un video sin derechos o runtime inaccesible son BLOCKED con una sola solicitud concreta al usuario.

## 10. Próximo mandato ejecutable

> Hermes/manager: bootstrap canónico; cargar SOLO esta arquitectura y skill `agents-os-agent-project-workflow`. Resolver recursos y permisos reales de video, repo/workspace `xKoRx/multimodal-knowledge-engine` y runtime; efectuar Git preflight. Crear subproyecto `owner: agent` mediante materializador y una sola tarea puente en este proyecto, sin inventar status. Preparar golden agente ciego y lanzar SPEC-00 con QA separado. Tras PASS documentado, avanzar 01→02→03-A→03-C→04 dentro del mismo alcance; registrar tareas/estado/bitácora y pruebas en el planificador canónico. Entregar Markdown y JSONL DE VALOR, evidencia exacta y benchmark sobre UN video. Si algo material falta, emitir un único BLOCKED preciso: verificado, dato faltante, decisión mínima. No cerrar sesión Agents-OS automáticamente; cierre solo por solicitud explícita.

## 🧩 Subproyectos

- Proyecto de ejecución `owner: agent` autorizado pero todavía NO creado ni verificado; materializar en entorno con contrato vigente y enlazar tras creación efectiva.

## ✅ Tareas

- [x] Convergencia arquitectónica ADR-001 A/C; versiones previas superseded. #owner/me #type/admin #area/personal
- [x] Fijar objetivo único, QA delegado, contratos visual/gráficos, gates y milestones M0/M1/M2. #owner/me #type/admin #area/personal
- [x] Renombrar proyecto a Multimodal Knowledge Engine y vincular repo `xKoRx/multimodal-knowledge-engine`; mantener nombre anterior como alias histórico. #owner/me #type/admin #area/personal
- [ ] Tarea puente de ejecución: discovery, subproyecto de agente, SPEC-00..04 y entrega M0 validada. #owner/me #type/supervision #area/personal
- [ ] Tras M0 PASS, delegar M1/M2 con SPECs basadas en evidencia, hasta biblioteca transversal. #owner/me #type/supervision #area/personal

## 📆 Bitácora

- **2026-09-17:** debate de dos IAs convergió en ADR-001 y cinco SPECs; implementación y runtime sin verificar. Arquitectura inicial A/B/C y nueve SPECs superseded en historia Git.
- **2026-09-17 — cierre operativo:** usuario fija objetivo documental y explotación de cursos; delega QA de etapas a agentes y solo interviene por excepción. Integrados cuatro findings de review, dos gates 03, golden de agente etiquetado, M0/M1/M2 y mandato SPEC-00. No hay ejecución física ni creación de subproyecto confirmada.
- **2026-09-17 — rename:** usuario generaliza el dominio más allá de cursos (entrevistas, podcasts y otras fuentes). Se adopta **Multimodal Knowledge Engine**, se fija repo `xKoRx/multimodal-knowledge-engine` y `Course Intelligence Engine` queda como alias histórico. M0 no cambia de alcance: sigue validándose con un video de curso de trading.

## 🧭 Decisiones

- Nombre canónico: **Multimodal Knowledge Engine**; `Course Intelligence Engine` queda como alias histórico.
- ADR-001: híbrido fijo/adaptativo falsable, A obligatorio antes de C, un único toggle, B no implementada.
- Documentación de calidad y explotación de conocimiento son la autoridad del producto; M0 no equivale a Done.
- QA por agentes sin falsa certificación humana; gates PASS autoavanzan, scope/permisos bloquean, modelo/costo no se inventa.
- Go + SQLite/FS en POC, ASR y cobertura visual independientes, timestamps reales, integrity + grounding, JSONL canónico y Markdown proyección.

## 🔗 Docs / Links

- Repo: `xKoRx/multimodal-knowledge-engine`.
- [[agents-os]], [[agents-os-bootstrap]], [[agents-os-agent-project-workflow]], [[agents-os-session-close]].
- Candidatos SPEC-00: https://huggingface.co/Qwen/Qwen3.5-27B ; https://huggingface.co/mlx-community/Qwen3.5-27B-4bit ; https://ffmpeg.org/ffprobe.html ; https://github.com/ggml-org/whisper.cpp .
- Historia de versiones previas: Git de esta misma entidad; `Course Intelligence Engine` permanece como alias, no arquitectura alternativa.

## 💡 Ideas diferidas

- Clips nativos, modelos pequeños de clasificación, Postgres/MinIO, Argus, cluster, corpus masivo y búsqueda vectorial solo con pruebas de necesidad. No desviar M0.
