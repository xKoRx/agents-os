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
repo:
jira:
prs:
aliases:
  - Course Intelligence
  - Motor de conocimiento de cursos
  - Procesamiento de cursos de trading
tags:
  - kind/project
  - area/personal
created: "2026-09-17"
updated: "2026-09-17"
---

# Course Intelligence Engine

> [!info]+ Proyecto
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P2 · **Repo:** no asignado · **Arquitectura:** acordada para implementar y falsar mediante una POC, NO certificada experimentalmente · **Implementación:** no autorizada. Proyecto independiente de Hermes, Echo y Echo Forge; Aranea es infraestructura opcional. Esta nota es la única arquitectura vigente para el proyecto.

## 🎯 Objetivo

- Convertir cursos de trading heterogéneos de 1–2 horas (teoría, diapositivas, gráficos, StrategyQuant X, parámetros, procedimientos y backtests) en conocimiento técnico estructurado, verificable y reutilizable, no en resúmenes narrativos.
- POC: procesar UN video real autorizado, recuperar información hablada y visual —incluidas demostraciones silenciosas—, registrar ambigüedades y omisiones, y generar Markdown técnico y JSONL estructurado con evidencia verificable y timestamps reales.
- Go es dueño del dominio; KISS, YAGNI, SOLID. Sin frontend, Kafka, base vectorial, microservicios, scheduler distribuido ni modificaciones a Echo/Echo Forge. No usar GLM Pro destinado al desarrollo como inferencia recurrente del corpus.

## 📊 Estado actual

- **2026-09-17 — Arquitectura de la POC acordada por dos interlocutores; validación física pendiente.** ADR-001 acepta ensayar una cobertura visual independiente del audio y una investigación multimodal adaptativa opcional. A es baseline end-to-end obligatorio; C usa el mismo ejecutable con `adaptive_investigation=true`. B queda documentada como alternativa, no se implementa ni evalúa en la POC. No existen métricas reales de superioridad.
- **Diseño anterior superseded dentro de esta misma nota:** las nueve SPECs y comparación A/B/C de la versión anterior no están vigentes. Se conservan sus invariantes útiles (tiempo real, golden humano, recuperación tras fallos y baseline A E2E). No existe una segunda arquitectura activa.
- **Contexto:** `Raw → Extracted → Aligned → Interpreted → Verified → Published` describe hitos, no un flujo irreversible. Ventanas de 5–10 minutos son parámetros ilustrativos de procesamiento, nunca unidades semánticas obligatorias.
- **Runtime candidato, NO verificado físicamente:** Mac Apple Silicon M4, 24 GB; `Qwen/Qwen3.5-27B` / conversión `mlx-community/Qwen3.5-27B-4bit`, FFmpeg/FFprobe y ASR local candidato whisper.cpp. Compatibilidad, memoria, lectura de texto pequeño, múltiples imágenes y formato estructurado requieren SPEC-00. No inferir soporte de clips de un backend diferente. Un modelo menor es una variante experimental etiquetada, nunca fallback silencioso.
- **Precondiciones pendientes:** video autorizado y representativo, repo/workspace y baseline Git, autorización expresa de SPEC-00, identidad y recursos reales del runtime, anotación humana independiente y presupuesto experimental. Diseñar la POC NO autoriza escribir código.
- **Agents-OS:** proyecto canónico localizado y actualizado por instrucción explícita; sesión abierta, sin cierre.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Course Intelligence Engine / repo pendiente | pendiente | preflight Git pendiente | [[Course Intelligence Engine#1. Contrato funcional y resultado]] | [[Course Intelligence Engine#9. Roadmap de SPECs]] | Diseño acordado; implementación BLOCKED hasta autorización y precondiciones de SPEC-00 |

## 1. Contrato funcional y resultado

**Entrada:** video autorizado, original inmutable identificado por SHA-256, streams y tiempo canónico, configuración efectiva versionada y presupuesto por video. **Salida:** `KnowledgeItem`, `Procedure`, `Relation` y `Evidence` persistidos como conocimiento estructurado, exportación JSONL reproducible y Markdown técnico navegable; reporte de cobertura, limitaciones y evaluación. Cada afirmación material conserva identidad, clase epistemológica, estado de validación y referencias a audio/video con timestamps reales. La publicación explicita incertidumbres; nunca promete comprensión exhaustiva ni verdad empírica automáticamente certificada.

**Tres identidades distintas:** ventana de procesamiento, evento temporal/espacial y conocimiento. Cada instante pertenece a una ventana principal; el contexto vecino puede solaparse, sin duplicar conocimiento. Una regla o procedimiento puede abarcar varias ventanas, enlazar excepciones posteriores y consolidarse globalmente.

**Golden temprano:** seleccionar video y comenzar anotación humana sobre el ORIGINAL desde el inicio; definir criticidad y congelar el golden antes de evaluar resultados, idealmente antes de mostrar cualquier salida A/C al anotador. El golden jamás alimenta prompts, selección, calibración encubierta ni conocimiento publicado. Con un solo video no se puede generalizar exactitud al corpus completo.

## 2. ADR-001 — Bounded Hybrid Evidence Acquisition (ACCEPTED FOR POC DESIGN)

**Contexto:** audio, diapositivas, interfaces, gráficos y demostraciones contienen información complementaria; ASR solo deja ciegos visuales, y selección rígida puede no resolver configuraciones o secuencias ambiguas.

**Decisión:** construir un monolito CLI Go con cobertura visual independiente de ASR, densidad configurable, selección inicial reproducible y un investigador que puede solicitar evidencia adicional mediante protocolo cerrado. Comparar el baseline A end-to-end frente a C con adquisición adaptativa activada. Mantener como autoridad operacional evidencia íntegra, identidad temporal, límites y estados, no el juicio del modelo.

**Experimento controlado:** A (`adaptive_investigation=false`) y C (`true`) comparten video/hash, transcripción, índice, evidencia inicial, modelo/revisión/backend, reconstrucción, grounding, consolidación, publisher y configuración relevante. La única diferencia funcional del experimento principal es la adquisición adaptativa. Ejecutar una comparación con límites iguales de imágenes/inferencia y reportar consumo real; ejecutar por separado otra con presupuestos operacionales propios. Igual techo no implica igual consumo. La mejora se expresa como conocimiento correcto incremental y errores/costo introducidos, nunca longitud del documento.

**No decisiones:** cobertura visual no significa decodificar todos los frames permanentemente: barrido exhaustivo económico versus densidad reducida es ablación experimental. No se congelan paquetes Go, umbrales, intervalos de anclas, modelos alternativos ni estrategia distribuida. B (transcripción + anclas mínimas + agente) no se implementa: riesgo de eventos visuales desconocidos y sin pregunta incremental imprescindible para esta POC. Envío de video completo a VLM, clips nativos, Kafka/Temporal, Postgres/MinIO obligatorios, base vectorial, múltiples modelos y cluster quedan diferidos hasta justificación empírica.

**Consecuencia:** C añade complejidad y costo potencial; se retira la adaptación por KISS si A alcanza gates y C no recupera conocimiento relevante adicional bajo condiciones comparables. Si ninguna variante alcanza gates, no se aprueba ninguna por sofisticación.

## 3. Arquitectura lógica y responsabilidades

```text
Video original + identidad / reloj canónico
       ├── Transcripción completa + timestamps
       └── Cobertura visual independiente + índice de actividad
                   ↓
          Planning Context (NO AUTORITATIVO)
                   ↓
          Selección determinista inicial
                   ↓
      Interpretación / Investigator opcional
                   ↕ preguntas y solicitudes acotadas
          Evidence Acquisition + journal
                   ↓
          Knowledge Reconstruction
                   ↓
      Integrity Validator + Grounding Reviewer
                   ↓
      Global Consolidation → revalidar cambios
                   ↓
          JSONL + Markdown + evaluación golden
```

- **Go:** estados, reglas de adquisición, presupuesto, idempotencia, referencias, dependencias y política de publicación. FFmpeg/FFprobe, ASR y VLM son ejecutores especializados, no autoridad de negocio.
- **Planning Context:** combina transcripción, inventario visual, actividad silenciosa, contexto vecino y preguntas pendientes; solo orienta preguntas. Ningún dato del mapa global se convierte directamente en conocimiento publicado: `hint → question → evidence → claim → review → publication`.
- **Separación de fases:** `Raw/Extracted/Aligned/Interpreted/Verified/Published` son checkpoints auditables; el investigator puede solicitar adquisición nueva y retroceder localmente de forma acotada.
- **Persistencia:** un solo proceso local secuencial, filesystem de originales/derivados y SQLite para estado, solicitudes, índice y journal. Un propietario/bloqueo verificable por ejecución; no cola externa ni motor de workflows. Una ejecución aislada por video (`video_id`, espacio de artefactos, presupuesto y dependencias); particionable más adelante sin implementar distribución ahora.
- **Artefactos:** original y evidencia inmutables; hashes y versión de entradas, configuración y extractores/modelos; escritura temporal → validar/hash → publicación atómica en el mismo filesystem → journal; reconciliación ante crash. Duplicados equivalentes reutilizan evidencia por `acquisition_key`, conservan identidad de cada pregunta. No prometer exactly-once físico.
- **Invalidación:** cambios de modelo/grounding invalidan sus salidas descendientes, no la extracción independiente; cambio de índice visual conserva ASR; cambio de plantilla solo regenera proyección cuando no modifica el conocimiento. Versionar prompts, modelos, parámetros, resultados y fallos.
- **Go packages:** implementar fronteras reales, sin congelar layout ni interfaces por cada struct. Una CLI operativa capaz de correr, inspeccionar y reanudar; logs estructurados mínimos y manifiesto por corrida. Medios, transcript y secretos no van a logs ni endpoints remotos por defecto. Texto dentro del curso es entrada no confiable; jamás comandos ni instrucciones de sistema.

## 4. Extracción visual, tiempo y adquisición

**Inspección versus adquisición:** inspección calcula señales baratas sobre toda la cobertura declarada; adquisición recupera material a resolución original para responder preguntas. Medir frames inspeccionados, artefactos adquiridos e imágenes efectivamente inferidas por separado. Barrido exhaustivo con buffers pequeños es una variante inicial a probar contra muestreo menos denso, NO contrato de producción. Guardar intervalos no observados y candidatos descartados.

**Señales candidatas:** cambios globales (luminancia/bordes/histograma), diferencias por tiles/regiones a resolución suficiente, persistencia temporal (antes/durante/después/transitorios), anclas estables y auditables, agrupación de actividad continua de gráficos, OCR diferencial únicamente selectivo y deduplicación perceptual contextual. OCR, downsampling y upscale no prueban por sí solos valores; dos gráficos visualmente similares conservan identidades temporales separadas. PySceneDetect/OpenCV/optical flow son opciones, no dependencias arquitectónicas obligatorias.

**Selección inicial:** anclas distribuidas incluso en escenas estables, capturas antes/durante/después de eventos, capturas vinculadas a expresiones de audio y actividad visual silenciosa. La separación de anclas de 30–60 s es ilustrativa y debe medirse. Un evento de 2 s solo se considera recuperado si la evidencia contiene realmente el contenido dentro de su intervalo; anclas anterior/posterior no bastan. Gráficos y secuencias deben conservar orden y estados, sin inferir intención a partir de movimiento. Una captura que no permite leer un parámetro produce `UNREADABLE`, nunca una cifra inventada.

**Solicitudes permitidas:** `FRAME`, `REGION`, `COMPARE`, `SEQUENCE`, `FIND_CHANGE`; clip nativo diferido. Cada solicitud tiene `request_id`, `video_id`, `segment_id` o evento referenciado, `question_id`, `kind`, intervalo concreto, justificación, límites y ROI cuando corresponda. `FIND_CHANGE` usa detectores deterministas en ventana local, no un VLM recorriendo videos enteros. Go valida identidad, permiso, límites de duración y búsqueda local, timestamps/ROI, duplicados y cuotas ANTES de ejecutar; el investigador nunca recibe shell, paths ni acceso a otros videos. Presupuesto acota rondas, solicitudes, frames, imágenes inferidas, secuencias, tokens reportados/estimados, RAM, tiempos, reintentos y disco. Agotamiento ⇒ `INCOMPLETE`, no loop ilimitado.

**Tiempo canónico:** preservar stream, PTS original, time base racional, ordinal, tiempo normalizado, tiempo solicitado y tiempo REAL del frame recuperado, intervalos y hash. Gestionar VFR, start_time, offset audio/video y discontinuidades. El seek es una petición: decodificar, seleccionar según política, verificar PTS efectivo y tolerancia fundada en frames vecinos; si no se puede, la referencia no pasa integridad. ROI conserva coordenadas del frame original y origen del recorte.

## 5. Contratos de conocimiento y verificación

**Modelo canónico mínimo:** `KnowledgeItem` (`kind=claim|concept|rule|parameter|observation`, alcance, condiciones, clase epistemológica, estado y evidencia), `Procedure` (pasos ordenados, precondiciones, excepciones, estado y evidencia POR PASO), `Relation` (incluye dependencias, excepciones y contradicciones entre fragmentos) y `Evidence` (identidad, tiempo, contenido/ROI, hash y procedencia). Contradicción e incertidumbre son estados/relaciones, no agregados separados para la POC. Las preguntas y solicitudes son estado operacional, no nuevas entidades ontológicas.

**Clases epistemológicas distintas de validación:** `INSTRUCTOR_SAID`, `VIDEO_OBSERVED`, `MODEL_INFERRED`, `EXTERNALLY_CHECKED`, `EMPIRICALLY_VALIDATED`. Una afirmación del instructor, una cifra en pantalla, una inferencia y un backtest reproducido no son equivalentes. No usar la etiqueta `EMPIRICALLY_VALIDATED` sin prueba externa reproducible.

**Integrity Validator (determinista):** verifica evidencia existente, video correcto, hash, versión, fuente, timestamps reales, ROI y correspondencia formal de intervalos. `INTEGRITY_PASS` NO demuestra semántica.

**Claim Grounding Reviewer (stateless):** recibe únicamente la versión concreta del claim/paso, referencias de evidencia, fragmento de transcripción necesario y clase epistemológica, sin la conversación ni razonamiento del investigator. Responde `GROUNDING_SUPPORTED | GROUNDING_CONTRADICTED | GROUNDING_INSUFFICIENT` con IDs y motivo auditables. Puede usar el mismo VLM con contexto separado: esto no garantiza independencia de errores. JSON inválido, reviewer ausente o fallo ⇒ no se marca SUPPORTED. La pareja `INTEGRITY_PASS && GROUNDING_SUPPORTED` autoriza mostrar `SUPPORTED_BY_AUTOMATED_REVIEW`, **nunca VERIFIED_TRUE / verdad certificada**. Falsos `SUPPORTED`, especialmente críticos, se miden contra golden humano.

**Consolidación y revalidación:** reconciliar conocimientos de todas las ventanas, reglas/excepciones posteriores, pasos y contradicciones antes de publicar. Modificar una afirmación invalida grounding de esa versión; revalidar la nueva versión Y cualquier paso o elemento dependiente afectado. Preservar ambos canales cuando audio y video discrepan, sin atribuir automáticamente el error al instructor. `CONTRADICTED`, `INSUFFICIENT`, `UNREADABLE` e `INCOMPLETE` se muestran como tales; no publicar hechos materiales huérfanos ni ocultar conflictos.

**Publicación:** JSONL versionado, con orden estable/IDs y referencias completas, es intercambio estructurado reproducible; SQLite conserva estado operacional. Markdown es proyección de lectura (índice, conceptos, reglas, pasos, parámetros, contradicciones, preguntas, cobertura y evidencia). No reconstruir JSONL a partir de Markdown. Toda referencia material resuelve al original o artefacto íntegro y timestamp real; usar paths relativos, no `file://` como única referencia.

## 6. Benchmark, escenarios y límites de verdad

**Golden independiente:** anotación humana directamente desde el video original con ID, clase, timestamp/intervalo, ROI si existe, contenido esperado, criticidad fijada antes, canal, legibilidad, dependencias y adjudicación. Incluir demostraciones sin pista en ASR y distinguir recuperable de ilegible. Preferible doble revisión para críticos; si solo hay una, registrar limitación. Congelar antes de analizar resultados A/C; no recalibrar el sistema sobre ese golden y presentar la misma ejecución como test independiente.

**Casos críticos:** (1) teoría y slides; (2) parámetro SQX silencioso sin pista textual; (3) gráfico con orden temporal; (4) evento breve cuya evidencia debe caer en el intervalo; (5) regla con excepción distante; (6) contradicción audio/pantalla; (7) valor genuinamente ilegible con abstención correcta. Los ausentes en el video real se prueban con fixtures claramente segregados y NO se contabilizan como recuperación del video principal.

**Experimentos:** E1 A vs C con misma evidencia inicial y modelo/validador/publisher, en comparación de igual techo de inferencia y comparación operacional separadas; E2 inspección densa vs temporal reducida; E3 global vs regional y OCR selectivo solo si aporta; E4 frame/par/secuencia, clips solo si las secuencias fallan y el backend acredita soporte; E5 modelo/backends y memoria físicamente; E6 fallos, reintentos, crash, hashes e invalidación. No construir B como tercer pipeline.

**Métricas:** eventos recuperados / eventos recuperables del golden, omisiones críticas clasificadas por primer punto de pérdida (`detección → adquisición → interpretación → validación/consolidación → publicación`), parámetros exactos (etiqueta/valor/unidad/condición), grounding falso positivo humano, referencias íntegras, cobertura temporal/eventos/conocimiento por separado, utilidad humana del procedimiento y costo marginal. Registrar tiempo total, RAM pico, decodificación, imágenes entregadas, tokens reales o estimados y fallos; la cantidad de páginas no mide calidad.

**Gates:** G0 video/derechos y runtime real; G1 línea temporal verificable; G2 cero omisiones críticas recuperables en el golden evaluado; G3 cero valores críticos incorrectos publicados como respaldados; G4 100% referencias materialmente válidas; G5 cero afirmaciones materiales inventadas o excepciones conocidas ocultadas; G6 incertidumbres/conflictos visibles y reviewer sin falsos `SUPPORTED` críticos en golden; G7 resume, deduplicación y reconciliación comprobados; G8 límites respetados o resultado `INCOMPLETE`; G9 un revisor humano reconstruye unidades críticas desde documentación y evidencias. Coverage de código: priorizar funcionalidades críticas y alcanzar al menos 95% según perfil global; porcentaje no sustituye pruebas E2E. Un video no demuestra precisión generalizable.

**Decisión experimental:** `GO` cuando gates críticos pasan y los componentes adicionales prueban utilidad; `CORRECT` si hay causa y reparación acotadas; `NO_GO` si persisten errores críticos, referencias falsas o consumo fuera de control. Si A pasa y C no aporta calidad correcta adicional, retirar adaptación para ese alcance. Si ninguna pasa, detener sin certificar.

## 7. Persistencia, seguridad y escalamiento

**SQLite + filesystem:** journal transaccional de solicitudes/etapas, archivos temporales validados con hash, publicación atómica local y reconciliación tras crash. `request_id` ≠ `acquisition_key`; operaciones físicas pueden repetirse, solo un resultado lógico válido. Sin promesa exactly-once. Al reiniciar inspeccionar estado durable y efectos físicos antes de reintentar. Cache y DAG tipado permiten reprocesar descendientes únicamente, sin construir motor genérico.

**Runtime local condicionado:** Mac M4 24 GB es target inicial, no capacidad certificada. Medir simultaneidad ASR/VLM en SPEC-00; no ejecutarlos en paralelo hasta validar memoria. Sin API remota por defecto ni fallback de pago. Video y transcript son potencialmente sensibles; instrucciones dentro del video no tienen autoridad sobre herramientas ni sistema.

**Escalamiento futuro:** unidad independiente por video; agregar coordinación multi-video, distribución Zeus/Hera/Kronos, almacenamiento remoto, modelos de clasificación de menor tamaño o búsqueda semántica solo con demanda y baseline de calidad. Un antecedente denominado Trading Course Intelligence (julio, 10 cursos/100–150 h, ASR/visual periódico/JSONL/Markdown/distribución) fue reportado durante el debate, pero su fuente original NO se verificó en el vault; no tratar cifras, frecuencia ni topología como decisiones vigentes. Se rescata únicamente exportación JSONL, semántica escalonada como opción futura y aislamiento por video.

## 8. Secuencia de ejecución y gates

**Antes de desarrollar:** identificar repo/workspace autorizados, derechos del video y presupuesto; iniciar golden humano y preservar separación del investigador. Cada SPEC se aprueba por prueba de funciones críticas, evidencia física, versiones y límites, no por compilar o autovalidarse. No anticipar tareas de Echo, Echo Forge, Hermes ni instalación de servicios nuevos.

**Baseline E2E obligatorio:** SPEC-03 primero debe producir A con selección fija, conocimiento completo, integrity + grounding, consolidación/revalidación y Markdown/JSONL mínimo. Solo con A evaluable se habilita el investigator C. La publicación base no puede esperar a SPEC-04; SPEC-04 finaliza reportes y comparación. Ambas variantes comparten contrato de conocimiento y publisher.

## 9. Roadmap de SPECs

| SPEC | Alcance y dependencia | Prueba/entregable y gate |
|---|---|---|
| **00 — Runtime & Feasibility** | Verificar herramientas, modelo exacto/backend, ASR, imágenes y memoria con material autorizado; NO construir el motor. Requiere autorización explícita y preflight. | `RuntimeCapabilityReport`; imagen SQX legible, gráfico, comparación multiimagen, JSON estructurado y RAM pico medidos. BLOCKED ante falta de permisos/material/workspace; OOM no implica retry ilimitado. |
| **01 — Media Intelligence Foundation** | Después de 00: fuente/hash, PTS/offsets, ASR completo, segmentos+contexto, cobertura visual independiente, índice y anclas. | `VideoAsset`, `TranscriptSegment`, `VisualEvent`, `VisualCoverage`, manifiesto temporal. Pruebas VFR, seek, silencios, parámetro pequeño, evento 2 s, gráfico, fallos y densidad. |
| **02 — Evidence Acquisition** | Después de 01: solicitudes tipadas locales, ROI/pares/secuencias, timestamps efectivos, SQLite/FS, presupuestos e idempotencia. | `EvidenceRequest`, `EvidenceArtifact`, `AcquisitionResult`. Pruebas rango/ROI inválidos, deduplicación, crash, archivo parcial, hashes, lock, reanudación. |
| **03 — Investigator & Knowledge** | Después de 02: construir PRIMERO A end-to-end (reconstrucción, integrity, grounding, consolidación, revalidación, publicación JSONL/Markdown mínimo). Solo después activar C con investigator acotado. Golden ya iniciado y congelado antes de evaluar resultados. | `KnowledgeItem`, `Procedure`, `Relation`, `InvestigationDecision`, `ValidationResult`, `PublicationManifest`; A E2E funcional y C con límites/errores controlados. Gating: no autocertificación, false support ni hechos sin evidencia. |
| **04 — Publication & Experiment** | Después de 03: publicar documentación final, comprobar golden previamente congelado y comparar A/C (presupuesto común vs operacional separado), ablaciones, costos y decisión. | `BenchmarkReport`, documentación navegable, JSONL válido, métricas por causa, pruebas de recovery y decisión GO/CORRECT/NO_GO. No atribuir los siete escenarios al video si se cubrieron con fixtures. |

**Disciplina:** scope y baseline Git fijados por SPEC, sin código fuera de archivos permitidos, pruebas de funciones críticas antes que cobertura superficial, evidencia física, errores cerrados y handoff claro. Las cinco SPECs son slices de entrega, no cinco servicios ni packages forzados.

## 10. Autorización y próximo mandato

**Arquitectura:** ADR-001 aceptada únicamente como diseño para implementar y falsar en la POC. No existe validación experimental de C, del backend ni de detección exhaustiva. El usuario debe autorizar SPEC-00 y definir video/repo/workspace antes de ejecutar código; no abrir SPEC-01 por iniciativa propia.

> **Mandato SPEC-00 (condicionado):** ejecutar bootstrap canónico, recuperar esta nota, comprobar autorización de SPEC-00, repo/workspace/branch/base/worktree y video autorizado, verificar FFmpeg/ffprobe/ASR y identidad exacta de `Qwen/Qwen3.5-27B` + conversión `mlx-community/Qwen3.5-27B-4bit` o variante declarada. Probar inferencia sobre SQX de texto pequeño, gráfico, multiimagen y salida estructurada; medir memoria, duración, errores y contexto residual. Diferenciar DOCUMENTED, SOURCE_VERIFIED y PHYSICALLY_VERIFIED. Reportar `RuntimeCapabilityReport`, mediciones/evidencia, incertidumbres y PASS/BLOCKED/NO_GO. Si 27B falla, documentar causa y proponer prueba separada con modelo menor, sin sustitución silenciosa. No implementar motor, levantar infraestructura, modificar Echo/Forge ni cerrar Agents-OS.

## 🧩 Subproyectos

- Ninguno creado; no se ha autorizado delegación de implementación.

## ✅ Tareas

- [x] Converger arquitectura de la POC y reemplazar arquitectura anterior en proyecto canónico #owner/me #type/admin #area/personal
- [ ] Designar repo/workspace, video con derechos y presupuesto; confirmar autorización de SPEC-00 #owner/me #type/admin #area/personal
- [ ] Iniciar y congelar golden independiente antes de evaluar A/C; definir adjudicación de críticos #owner/me #type/research #area/personal
- [ ] Ejecutar SPEC-00 solo tras autorización explícita y revisar su reporte de runtime #owner/me #type/supervision #area/personal
- [ ] Revisar benchmark A/C y decisiones de adaptación después de SPEC-04 #owner/me #type/supervision #area/personal

## 📆 Bitácora

- **2026-09-17:** la versión inicial de esta nota contenía nueve SPECs y A/B/C. Debate posterior entre interlocutores acordó A vs C, cinco SPECs, Grounding Reviewer con alcance limitado, golden temprano, baseline A E2E, JSONL y aislamiento por video. Se actualiza la misma entidad canónica; no se ejecutaron pruebas ni código y no se autoriza implementación. Sesión Agents-OS abierta.

## 🧭 Decisiones

- **2026-09-17 / ADR-001 ACCEPTED FOR POC DESIGN:** cobertura visual independiente del audio con densidad experimental; baseline A E2E y C opcional mismo ejecutable/único toggle; B no implementada.
- **2026-09-17:** evidence integrity y grounding son controles distintos. `SUPPORTED_BY_AUTOMATED_REVIEW` no significa verdad; cambios tras consolidación invalidan revisiones afectadas.
- **2026-09-17:** SQLite + filesystem + monolito Go; knowledge mínimo + JSONL exportable + Markdown proyección; golden humano independiente desde selección del video.
- **2026-09-17:** ninguna SPEC ni despliegue autorizados por este acuerdo; resultados de runtime y superioridad de C siguen NO PROBADOS.

## 🔗 Docs / Links

- [[agents-os]] — mapa operativo; bootstrap ejecutable en [[agents-os-bootstrap]].
- Fuentes técnicas candidatas a verificar durante SPEC-00: https://huggingface.co/Qwen/Qwen3.5-27B ; https://huggingface.co/mlx-community/Qwen3.5-27B-4bit ; https://ffmpeg.org/ffprobe.html ; https://github.com/ggml-org/whisper.cpp .
- Historial del diseño inicial: revisión anterior de esta misma nota en Git; las decisiones antiguas A/B/C y SPEC-00..08 se consideran superseded, no arquitectura alternativa vigente.

## 💡 Ideas

- Evaluar únicamente después de los resultados: clips nativos, clasificación preliminar con modelo pequeño, almacenamiento MinIO, jobs PostgreSQL, observabilidad Argus, corpus completo, deduplicación entre cursos, distribución entre nodos y búsqueda semántica.
- Principio: el código controla procedencia, recursos, temporalidad y qué puede publicarse; el modelo pregunta e interpreta; solo un golden humano permite medir fidelidad semántica en un video y no puede garantizar exhaustividad universal.
