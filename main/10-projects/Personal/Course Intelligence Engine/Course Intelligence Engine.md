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
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P2 · **Repo:** no asignado · **Implementación:** no autorizada. Este proyecto es independiente de Hermes, Echo y Echo Forge; Aranea es infraestructura opcional, no dependencia. Las decisiones de este documento son propuestas para validación experimental, no resultados certificados.

## 🎯 Objetivo

- Transformar cursos de trading heterogéneos de 1–2 horas (teoría, diapositivas, gráficos, StrategyQuant X, parámetros, procedimientos y backtests) en una biblioteca de conocimiento verificable, no en un resumen narrativo.
- POC: procesar **un video real con derechos suficientes**, recuperar conocimiento visual y hablado, identificar omisiones e incertidumbres y publicar Markdown con vínculos a evidencia de origen y timestamps reales.
- Go como dueño del dominio; KISS, YAGNI, SOLID. Sin frontend, Kafka, base vectorial, microservicios ni modificaciones a Echo/Echo Forge. No usar GLM Pro destinado al desarrollo como inferencia recurrente del corpus.

## 📊 Estado actual

- **2026-09-17 — Arquitectura candidate, NOT ACCEPTED / NOT IMPLEMENTED.** Debate adversarial de dos posiciones simulado secuencialmente; no hubo dos agentes externos reales. Propuesta C: inspección visual determinista independiente del audio + adquisición multimodal adaptativa limitada + verificación externa de evidencias. La superioridad de C no está demostrada.
- **Contexto:** la primera propuesta `Raw → Extracted → Aligned → Interpreted → Verified → Published` se conserva solo como hitos; no puede ser un pipeline irreversible. Las ventanas de 5–10 minutos son valores configurables ilustrativos y unidades de procesamiento, no unidades semánticas.
- **Infraestructura:** Mac M4 con 24 GB; candidato `Qwen/Qwen3.5-27B` con conversión `mlx-community/Qwen3.5-27B-4bit`. Compatibilidad operativa, memoria máxima, calidad de texto pequeño, múltiples imágenes y soporte de clips en el backend seleccionado **NO PROBADOS físicamente**. Ver SPEC-00.
- **Precondiciones:** confirmar ruta/repositorio de implementación y worktree; confirmar video con derechos, material representativo y golden humano. Ninguna SPEC de código está autorizada automáticamente por este diseño.
- **Estado Agents-OS:** documento persistido por instrucción explícita de escritura; la sesión no se cierra sin pedido explícito.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Course Intelligence Engine / repo pendiente de definir | pendiente | pendiente de preflight Git | [[Course Intelligence Engine#1. Contrato funcional y resultado]] | [[Course Intelligence Engine#9. Roadmap de SPECs]] | BLOCKED para implementación hasta decisión del owner, preflight y autorización de SPEC-00 |

## 1. Contrato funcional y resultado

**Entrada:** video original autorizado e inmutable, perfil de ejecución y configuración de presupuestos/versiones. **Salida:** Markdown técnico con conceptos, definiciones, procedimientos, estrategias, parámetros, afirmaciones del instructor, observaciones visuales, hipótesis, contradicciones y preguntas abiertas. Cada elemento material debe enlazar fuentes temporales verificables o declarar `INCOMPLETE`/`UNREADABLE`/`UNVERIFIED` según corresponda. El resultado debe permitir navegar al timestamp exacto y consultar la captura original; no prometer comprensión exhaustiva no demostrada.

**Identidades separadas:** unidad de procesamiento (ventana temporal), evento audiovisual (intervalo y región) y unidad de conocimiento (Claim/Concept/Procedure/Strategy). Una explicación que comienza al minuto 8 y termina al 17 puede tener varias ventanas de procesamiento pero un único procedimiento consolidado con referencias múltiples. Cada instante pertenece a un único intervalo principal; las ventanas de contexto pueden solaparse sin duplicar afirmaciones.

**Mapa global:** transcribir el video completo y producir un índice visual independiente de ASR; construir la planificación temática con ambos canales, silencios y anclas visuales. El ASR nunca es la única fuente para decidir dónde hay conocimiento. Conservar relaciones entre fragmentos y consolidar reglas/excepciones globalmente antes de publicar.

## 2. Debate adversarial cerrado

**Agente A — Deterministic Pipeline Architect (posición simulada):** decodificar y analizar económicamente toda la duración, generar métricas globales/regionales, agrupar actividad, seleccionar anclas y evidencia reproduciblemente y después interpretar. A admite que una selección cerrada no resuelve todas las ambigüedades.

**Agente B — Agentic Visual Intelligence Architect (posición simulada):** entregar transcripción, contexto, inventario visual mínimo y evidencia inicial; formular preguntas, solicitar frames/ROI/pares/secuencias, investigar iterativamente y detenerse mediante límites externos. B admite que un agente guiado solo por audio nunca solicitará eventos silenciosos que desconoce.

### Ronda 1 — Cinco ataques por posición

| A cuestiona B | Riesgo | B cuestiona A | Riesgo |
|---|---|---|---|
| A1. Dependencia del contexto inicial | Ignora demostraciones silenciosas | B1. Relevancia basada en píxeles | Cambios pequeños pueden ser decisivos |
| A2. Decisiones no deterministas | Selecciones distintas entre corridas | B2. Umbrales rígidos | Escenas y resoluciones heterogéneas |
| A3. Costo impredecible | Agota tokens y tiempo | B3. Frames estáticos | Pierde orden y causalidad |
| A4. Autoevaluación del agente | Falsa completitud | B4. Exceso de candidatos | Movimiento genera evidencia irrelevante |
| A5. Complejidad operacional | Cola/agentes se convierten en workflow engine | B5. Selección cerrada | No puede aclarar imágenes borrosas o contradictorias |

### Ronda 2 — Defensas operacionales

- **A responde B1–B5:** análisis regional además del global; umbrales y configuración versionados/calibrados; eventos con inicio/durante/final y secuencias; agrupamiento de actividad y deduplicación con identidad temporal conservada; admitir profundización dirigida sin delegar la cobertura inicial.
- **B responde A1–A5:** inventario visual independiente del audio y anclas de intervalos estables; persistir prompt/modelo/entradas/decisiones para auditoría sin prometer determinismo perfecto; presupuestos aplicados en Go; matriz de cobertura y criterio de terminación externos; bucle local de solicitudes tipadas sin cola ni framework distribuido.

### Ronda 3 — Síntesis y desacuerdo falsable

- **Acuerdo:** detección determinista para descubrir candidatos; investigador adaptativo para interpretar/solicitar más; verificador independiente para procedencia y referencias; presupuesto y gates para terminar. Son responsabilidades de un monolito, no servicios ni agentes desplegados separados.
- **Pendiente empírico:** A espera que un índice denso alcance los eventos relevantes; B espera que muchas escenas sigan requiriendo investigación. Comparar A (índice + selección fija), B (audio + anclas visuales mínimas + adaptación) y C (índice + selección inicial + adaptación) con el mismo video, ASR, modelo y validador. Hipótesis candidata: C; si no aporta calidad correcta adicional frente a A, quitar adaptación por KISS.

## 3. Comparación de arquitecturas (hipótesis, no benchmarks)

| Criterio | A: determinista | B: agéntica | C: híbrida |
|---|---|---|---|
| Cobertura visual | Sistemática según detectores | Depende de anclas y preguntas | Inspección sistemática más profundización |
| Falsos negativos | Límites de detectores | Puntos ciegos de contexto | Riesgos de ambos; requiere golden |
| Fidelidad temporal | PTS bajo control del extractor | Depende de validador externo | Validador común obligatorio |
| Inferencia y costo | Predecible, potencial redundancia | Variable pero acotable | Costo inicial más adquisición incremental |
| Complejidad | Menor | Mayor control de ciclos | Mayor que A, sin distribución |
| Reproducibilidad | Reglas versionables | Trazas auditables, no idénticas necesariamente | Índice reproducible + trazas auditables |
| Reintentos | Por etapa | Por solicitud/decisión | Journal único y artefactos idempotentes |
| Escalabilidad | Segmentos y videos independientes | Escala según presupuesto | Particionable luego de validar |
| Calidad final | Limitada por evidencia inicial | Limitada por observabilidad e inferencia | Mejora potencial todavía no probada |

## 4. Diseño visual: inspección, selección y profundización

### 4.1. Dos operaciones y tres contadores

**Inspección** calcula métricas económicas y registra actividad; **adquisición** recupera evidencia interpretable. Medir por separado frames decodificados, artefactos guardados e imágenes efectivamente enviadas al VLM. Candidato POC: inspeccionar secuencialmente todos los frames con buffers pequeños y métricas sobre representaciones reducidas; NO almacenar ni inferir sobre todos. Comparar contra densidad reducida en E2: decodificar todo no es un dogma de producción.

### 4.2. Señales complementarias

| Detector | Mecanismo candidato | Qué descubre | Limitación |
|---|---|---|---|
| Cambio global | Luminancia, histograma, bordes | Slide/ventana | Cambios pequeños |
| Diferencia regional | Tiles parcialmente solapados, señal por región | Parámetros, anotaciones | No conoce relevancia |
| Persistencia temporal | STABLE→CHANGING→STABILIZING→STABLE | Antes/durante/después, transitorios | No conoce intención |
| OCR diferencial selectivo | ROI original, texto y posición antes/después | Etiquetas/valores | Lectura falible; jamás certifica solo |
| SSIM / hash perceptual | Deduplicación contextual | Redundancia | No fusionar momentos/instrumentos distintos |
| Movimiento temporal | Diferencias; optical flow solo cuando aporte | Scroll/dibujos | Movimiento ≠ conocimiento |
| Anclas de cobertura | Capturas distribuidas incluso en escenas estables | Inventario fuera de eventos | No sustituyen detección densa |

**Multirresolución:** frame reducido para cambios globales, regiones a detalle suficiente para parámetros pequeños y extracción original para verificar. Mantener ROI como coordenadas del frame original. No asumir que downsampling, OCR o upscale reconstruyen valores ilegibles. PySceneDetect puede ser candidato para cortes; no es un reconocedor de interfaces SQX. OpenCV puede resolver diferencias; el VLM no debe calcular píxeles innecesariamente.

**Estados, no frames sueltos:** editar Population Size 100→200 exige capturas de ambos estados, etiqueta, unidad y contexto; OCR produce un candidato, no un hecho. Una tabla de backtest exige encabezados y configuración. Un gráfico que se desplaza se agrupa como actividad continua y conserva estado inicial/final e hitos; no crear eventos por cada vela/cursor. Dibujar líneas, modificar parámetros y aceptar un diálogo puede exigir secuencia ordenada. El clip nativo se difiere hasta demostrar que las secuencias con PTS pierden información indispensable.

**Evento de dos segundos:** una ancla cada 10 s puede omitirlo; no usar anclas como único detector ni desechar indiscriminadamente eventos por duración mínima. Exigir evidencia durante el intervalo real más contexto antes/después. Distinguir detección, adquisición e interpretación: detectar algo sin capturar su contenido cuenta como omisión E2E.

### 4.3. Selección inicial

Cuatro canales: (A) anclas de cobertura de escenas estables, (B) antes/durante/después de eventos visuales, (C) anclas vinculadas a referencias del audio como «este parámetro», (D) adquisiciones solicitadas al investigar. Separación de anclas 30–60 s **solo ilustrativa para experimentar**, no configuración certificada. Priorizar diversidad de tiempos y ROI; agrupar actividad continua y deduplicar sin perder identidad temporal ni la evidencia candidata original. Registrar candidatos descartados por presupuesto.

### 4.4. Qué recibe el investigador y cómo trabaja

Contexto de entrada: transcripción del fragmento + vecinos, mapa global con posibles excepciones, inventario de eventos silenciosos, miniaturas/capturas iniciales, evidencia ya adquirida, preguntas abiertas y presupuesto restante. No recibe anotaciones golden ni respuestas esperadas. El modelo emite `InvestigationDecision` con preguntas y `EvidenceRequest` tipadas, nunca comandos shell arbitrarios. Un ejecutor en Go valida rangos, permisos, presupuesto y duplicación; recupera la evidencia; el modelo la interpreta y pide otra observación solo si una pregunta material sigue abierta. Un evaluador de cobertura externo al modelo autoriza terminación.

**Contrato mínimo de solicitud:** `video_id`, `segment_id`, `question_id`, `time_range` y `mode` (`FRAME`, `ROI`, `PAIR`, `SEQUENCE`), `reason`; ROI opcional/requerido según modo; resolución y máximo de frames normalizados por Go. `request_id` identifica la pregunta; `acquisition_key` identifica el trabajo deduplicable a partir de fuente, stream, intervalo, modo, ROI, resolución y versión del extractor. Estado/errores/artefactos son resultado separado; prioridad efectiva y costos son política de Go. `CLIP` deshabilitado inicialmente. Distintas preguntas pueden reutilizar evidencia idéntica sin borrar sus motivos.

**Terminación:** cada pregunta queda `SUPPORTED`, `CONTRADICTED`, `UNREADABLE` o `INCOMPLETE`; el orquestador comprueba eventos de riesgo sin revisar, referencias y presupuesto. El modelo puede proponer `DONE` pero jamás certifica cobertura semántica. Al agotarse un límite, publicar explícitamente `INCOMPLETE` o no publicar cuando corresponda; nunca inventar valores ni declarar comprensión total.

### 4.5. Tiempo real y evidencia inmutable

Identidad de fuente mediante SHA-256. Guardar stream, time base racional, PTS de presentación original, ordinal, requested timestamp, actual timestamp, intervalo/ROI, hash de artefacto y versión de extractor. No derivar tiempos suponiendo FPS constante; gestionar VFR, start_time, discontinuidades y offset audio/video. En seek decodificar y seleccionar el frame según política temporal explícita; verificar que su PTS real cumple tolerancia basada en separación entre frames vecinos. Un frame solicitado a 03:42 no constituye prueba de que el extraído corresponde a 03:42. Ante tiempos ambiguos, fallar cerrado para referencias certificadas.

### 4.6. Cobertura y costo

Tres métricas distintas: cobertura temporal inspeccionada (computable), recuperación de eventos relevantes y recuperación de conocimiento (ambas requieren golden humano). Los frames no observados, eventos no adquiridos, valores ilegibles y preguntas abiertas permanecen registradas. Presupuestos codificados por video/fragmento/solicitud para rondas, requests, frames extraídos, imágenes inferidas, secuencias, memoria, tokens, deadlines, reintentos y disco. Ejemplo exclusivamente experimental: 3 rondas, 4 solicitudes por ronda, 6 imágenes por solicitud, 32 imágenes inferidas por fragmento; los límites simultáneos prevalecen. Registrar presupuesto, consumo real, caché, fallos consumidos y calidad por separado. Tokens reales solo cuando los informa el backend; de lo contrario, estimados explícitos. Sin fallback silencioso a APIs pagadas.

## 5. Arquitectura lógica y persistencia

**Monolito CLI Go:** `ingest`, `run`, `resume`, `inspect`, `publish`. Responsabilidades internas: orquestador (estados/presupuesto), media/tiempo (ffprobe/ffmpeg), ASR/segmentos (whisper.cpp candidato), índice visual, adquisición, investigador VLM, knowledge builder, validador y publicador. Herramientas externas realizan multimedia/inferencia; Go conserva dominio, decisión de publicación, referencias y control de recursos. Sin UI ni API pública. WhisperX, OpenCV/PySceneDetect y soporte nativo de clips son opcionales sujetos a necesidad medida.

**Persistencia candidata:** filesystem local para original y derivados, SQLite para journal, IDs, índice, estados y referencias. Ejecución secuencial con diario durable: no hace falta una cola dedicada. PostgreSQL/MinIO/Argus no son dependencias de la POC; migración futura mediante límites de dominio, no abstracciones genéricas anticipadas. Hermes/Agents-OS gobiernan agentes de desarrollo y documentación, no son runtime del CIE.

**Estados de solicitudes:** `PENDING → RUNNING → SUCCEEDED | FAILED_RETRYABLE | FAILED_FINAL`; reconciliar `RUNNING` tras crash contra procesos/artefactos antes de reintentar. Rechazar solicitudes inválidas sin retry; acotar retries recuperables; OOM produce stop explícito. Un solo ejecutor activo por workspace o lock verificable. Guardar salidas temporales, comprobar integridad, publicar atómicamente cuando el filesystem lo permita y registrar commit durable; al reiniciar reconciliar archivo y journal. No prometer ejecución exactly-once; exigir un solo resultado lógico válido por acquisition_key después de pruebas de crash/concurrencia.

**DAG pequeño de datos:** Original→{Transcript,VisualIndex}→SegmentMap→Evidence/Investigation→Knowledge→Validation→Publication. Cada artefacto registra esquema, hashes de entradas/configuración, modelo/extractor, hash de salida y dependencias. Cambiar VLM invalida interpretación y descendientes, no ASR/índice; cambiar detector visual regenera índice y descendientes pertinentes, no ASR; cambiar video invalida sus derivados; cambiar template regenera Markdown. No workflow engine genérico.

**Estructura Go tentativa:** `cmd/cie`, `internal/domain`, `media`, `transcript`, `visual`, `evidence`, `investigation`, `knowledge`, `store`, `publish`, `testdata`. Crear paquetes cuando haya necesidad concreta. Interfaces solo para fronteras realmente sustituibles (ASR/VLM/almacenamiento), no para cada struct. Logs JSON y manifiesto de corrida con run/video/segment/request/stage/attempt/duration/outcome/error/resource_usage; sin dumps de transcripciones, videos ni secretos.

**Seguridad:** video con derechos como gate previo; material del curso no confiable, sus textos no pueden controlar prompts de sistema, permisos o ejecutar comandos. El investigador solo emite solicitudes estructuradas; Go crea rutas dentro del workspace y controla límites. No enviar medios a endpoints remotos por defecto.

## 6. Ingeniería de conocimiento y publicación

**Entidades mínimas:** `Claim` atómica (alcance y condiciones), `Concept`, `Procedure` ordenado (precondiciones/pasos), `Strategy` (reglas/parámetros/excepciones), `Evidence`, `Question`, `Relation` y `Conflict`. Una estrategia o procedimiento puede enlazar evidencias de distintos fragmentos. Consolidar globalmente y comprobar que excepciones posteriores modifican reglas previas.

**Clases epistemológicas separadas:** `INSTRUCTOR_SAID`, `VISUALLY_OBSERVED`, `MODEL_INFERRED`, `EXTERNAL_CORROBORATED`, `EMPIRICALLY_TESTED`. No confundir «el instructor dijo 80% de win rate», «la pantalla muestra 80%» y «el rendimiento fue reproducido». Estado de soporte, contradicción, ilegibilidad e incompletitud se mantiene por afirmación/procedimiento, no por documento entero. El modelo solo cita IDs de evidencia otorgados por Go. El validador comprueba ID, fuente, tiempo, versión y hash; la correspondencia semántica entre claim y evidencia se evalúa con golden/revisión independiente, no se da por probada porque el enlace existe.

**Markdown de salida:** índice de temas, conceptos, procedimientos, estrategias, parámetros con origen, afirmaciones atribuidas, evidencias timestamp/ROI, conflictos y preguntas abiertas, informe de cobertura, procedencia y presupuesto. Enlaces navegables al original y artefactos locales; sin documentos que oculten incertidumbres ni relaciones duplicadas por solapamiento.

## 7. Siete escenarios de validación

| Caso | Recuperación candidata C | Riesgo/alarma de cobertura insuficiente |
|---|---|---|
| Teoría con diapositivas | Cortes + anclas + audio + lectura original | Definición o diapositiva relevante sin evidencia |
| SQX silencioso | Cambio regional sin pista ASR + before/after + ROI | Parámetro anotado ausente o mal leído; no dar pista de respuesta al agente |
| Gráfico complejo | Agrupar pan/scroll/dibujos; secuencia y audio | Orden causal, vela o línea no reconstruible |
| Demostración de 2 s | Barrido denso, frame dentro del intervalo y contexto | Solo frames anterior/posterior: NO cuenta como recuperación |
| Regla y excepción +15 min | Segmentos con contexto + consolidación global | Regla publicada como absoluta pese a excepción |
| Contradicción audio/pantalla | Evidencias independientes y `Conflict` explícito | Valor único falsamente confirmado |
| Parámetro ilegible | Original/ROI y abstención `UNREADABLE` | Inventar valor o declarar PASS sin detalle recuperable |

El material real quizá no contiene todos los casos: cubrir los ausentes con fixtures claramente separados del benchmark principal. No afirmar validación real cuando solo existe diseño.

## 8. Experimentos y quality gates

**Golden humano independiente:** anotar directamente el video original ANTES de ver salidas de A/B/C: `id`, tipo, intervalo real, ROI, contenido, criticidad fijada previamente, canal, legibilidad, dependencias y observaciones. Incluir explícitamente eventos visuales sin mención en ASR; separar recuperables de genuinamente ilegibles. Idealmente dos revisores adjudican críticos; con uno declarar limitación. Golden oculto a los investigadores. Congelar la referencia antes de medir; no ajustar umbrales y presentar la misma corrida como validación independiente.

**Experimentos:** E1 comparar A/B/C con mismo video, ASR, VLM y validador: (i) presupuesto equivalente, (ii) presupuesto operacional propio, reportes separados. E2 barrido denso vs muestreo reducido. E3 global vs regional vs regional+OCR (medir falsos positivos y negativos). E4 frame vs par vs secuencia; clip solo con preflight. E5 identidad exacta de modelo/backend, imágenes SQX/gráficos, salida estructurada, pico de RAM y velocidad. E6 crash, retry, duplicación, actualización de extractor, reconciliación y reanudación.

**Métricas con denominador explícito:** recall de eventos relevantes recuperables, omisiones críticas por etapa (detección/adquisición/interpretación/publicación), error de PTS/pertenencia al evento, exactitud de etiqueta+valor+unidad de parámetros, fidelidad de afirmaciones por revisión humana, integridad de referencias, cobertura temporal/eventos/conocimiento separadas, frames decodificados/adquiridos/inferidos, duración, RAM, tokens reales o estimados y costo incremental de C sobre A. No medir calidad por cantidad de páginas.

**Gates G0–G9:** G0 derechos y runtime real; G1 referencias temporales reales; G2 recuperar todos los eventos críticos declarados recuperables en el golden del video evaluado; G3 cero valores críticos falsamente confirmados; G4 cero referencias inválidas; G5 ninguna afirmación material inventada ni excepción conocida oculta; G6 incertidumbres visibles; G7 crash/retry/idempotencia coherentes; G8 presupuesto respetado o `INCOMPLETE`; G9 revisor reconstruye unidades críticas desde Markdown y evidencias. El alcance de un único video NO prueba recuperación universal. El código nuevo debe cubrir primero caminos críticos y alcanzar mínimo 95% coverage según perfil global; coverage porcentual no sustituye e2e.

**Decisión:** `GO` solo con gates críticos superados y beneficio incremental de los componentes añadidos; `CORRECT` si falla un caso con causa aislada y corrección acotada; `NO_GO` si persisten omisiones críticas recuperables, alucinaciones materiales, referencias inválidas o presupuesto descontrolado. Si A satisface gates y C no añade recuperación correcta, retirar la adaptación para ese alcance; si ninguna variante pasa, ninguna queda aprobada.

## 9. Roadmap de SPECs

| SPEC | Objetivo y alcance | Dependencias | Contrato / pruebas obligatorias | Aceptación y bloqueo; evidencia |
|---|---|---|---|---|
| 00 Runtime & Feasibility | Verificar herramientas, Qwen candidato, imágenes múltiples, memoria, ASR representativo, sin motor | Autorización de video/workspace | RuntimeCapabilityReport, ModelIdentity, ResourceMeasurement; inferencia física, fallos/OOM | PASS solo con identidad y resultados reales; BLOCKED si incompatible o sin autorización; versiones, hashes, logs y mediciones |
| 01 Media & Temporal | Ingesta, ffprobe, hash, streams, PTS y seek verificable | 00 | VideoAsset, MediaTime, FrameReference; VFR/offset/corrupción | Sin referencias ficticias; bloquear timeline incoherente; manifiesto y tests |
| 02 Transcript & Segmentation | ASR completo, offsets, ventanas y contexto vecino | 01 | TranscriptSegment, SegmentContext; silencios/fronteras/reanudar | Tiempos estables y revisión humana; bloquear ASR inutilizable |
| 03 Visual Index | Barrido, diferencias globales/regionales, agrupación, cobertura sin VLM | 01 | VisualEvent, VisualCoverage; slides, ROI mínima, 2 s, silencio, gráfico | Índice auditable; bloquear pérdida sistemática de candidatos; contact sheet y métricas |
| 04 Evidence & Journal | Solicitudes tipadas, extracción ROI/par/secuencia, hashes, idempotencia/crash | 01,03 | EvidenceRequest, EvidenceArtifact, AcquisitionResult; duplicados, rangos, crash, lock | Artefactos durables coherentes o BLOCKED; journal, hashes, pruebas de fallos |
| 05 Golden humano | Anotar, clasificar críticos y congelar criterios independientemente | Video elegido, 01 | GoldenAnnotation, EvaluationResult; recuperabilidad, silencios, adjudicación | Baseline congelado; BLOCKED si anotaciones críticas ambiguas o material insuficiente |
| 06 Baseline A E2E | Reconstruir conocimiento, validar evidencia, publicar Markdown mínimo y medir A | 02–05 | KnowledgeClaim, ValidationResult, PublicationManifest; excepciones/conflictos/hallucinations | A evaluable end-to-end y omisiones clasificadas; bloquear afirmaciones sin sustento |
| 07 Investigator B/C | Preguntas y adquisición adaptativa bajo límites; misma capa de validación | 06 | InvestigationDecision, BudgetAccount; bucle infinito, gasto, referencia inventada, evento silencioso | Auditoría/reinicio/budgets PASS; BLOCKED si modelo se autocertifica |
| 08 Evaluation & ADR | Comparativa A/B/C, ablations, fallos, Markdown final y decisión | 07 | BenchmarkReport; presupuesto equivalente y operacional separado | Gates + GO/CORRECT/NO_GO sustentado, sin contaminación de golden |

**Disciplina:** SPEC pequeña, baseline Git/worktree, rutas permitidas, versiones, pruebas críticas, evidencia física y error explícito. No abrir infra nueva ni modificar Echo/Echo Forge. La SPEC-06 antes de la adaptación corrige un defecto del orden anterior: el baseline debe ser E2E para poder medir calidad y publicación, no solo detectar frames.

## 10. ADR-001 — Bounded Hybrid Evidence Acquisition (PROPOSED)

**Contexto:** audio y video contienen conocimiento complementario; un pipeline fijo cerrado no profundiza y un agente guiado solo por texto no sabe qué ocurrió silenciosamente.

**Decisión propuesta:** evaluar C con índice visual independiente, selección inicial sistemática, investigación dirigida acotada, verificación por evidencia y benchmark humano. No aprobar superioridad sin experimentos.

**Alternativas:** A determinista sigue como baseline y puede quedar en producción del alcance si satisface gates; B audio+anclas tiene riesgo de eventos invisibles; enviar videos completos a VLM carece de control de timestamp/costo y queda diferido; clips, Kafka, PostgreSQL obligatorio, MinIO obligatorio, búsqueda vectorial y workflow engine no están justificados en el MVP.

**Consecuencias:** mayor complejidad que A y posible inferencia adicional; índice que requiere calibración; resultados del VLM no necesariamente deterministas; no puede certificarse conocimiento total automáticamente. Contrapartida: evidencia auditable, posibilidad de profundizar y capacidad de retirar adaptación sin reescribir contratos.

**Incertidumbres:** U01 modelo/backend en M4 24 GB y calidad SQX, resolver SPEC-00; U02 clips versus secuencias, solo E4 si necesario; U03 densidad visual/eventos de 2 s, E2/SPEC-03; U04 sensibilidad regional/OCR, E3; U05 costo/calidad incremental de C, E1; U06 fidelidad de procedimientos y contradicciones, golden/SPEC-06–08.

**Estado:** PROPOSED, no ACCEPTED, no implementación. Autorización de SPEC-00 no está implícita en este documento.

## 11. Próximo mandato para agente de desarrollo (condicionado)

> **Mandato SPEC-00 — Runtime & Feasibility:** Ejecuta bootstrap canónico de Agents-OS, identifica `VAULT_ROOT`, lee exclusivamente este proyecto y la SPEC-00. Primero confirma autorización expresa de SPEC-00, video con derechos, ruta/repositorio/workspace autorizados, branch/base/estado de Git y hardware/herramientas reales. Sin esos preconditions devuelve `BLOCKED` exacto y no modifiques archivos. Comprueba identidad del modelo `Qwen/Qwen3.5-27B` y de la conversión `mlx-community/Qwen3.5-27B-4bit` o registra variante exacta realmente disponible; prueba en el Mac M4 24 GB una imagen SQX de texto pequeño, un gráfico, múltiples imágenes y JSON estructurado; mide RAM máxima, tiempo, fallos, calidad de lectura y residuos de contexto. Verifica FFmpeg/ffprobe y ASR representativo. No declares PASS por instalar el modelo ni extrapoles soporte de clips de otro backend. Entrega RuntimeCapabilityReport, matriz documentado versus probado, mediciones, comandos/evidencia, incertidumbres y PASS/BLOCKED/NO_GO. No abras SPEC-01 por iniciativa propia, no montes servicios y no cierres Agents-OS.

## 🧩 Subproyectos

- Ninguno creado; no se ha autorizado delegación de implementación.

## ✅ Tareas

- [ ] Aprobar o rechazar ADR-001 como hipótesis de la POC y designar repo/workspace/video autorizado #owner/me #type/admin #area/personal
- [ ] Autorizar explícitamente SPEC-00 después del preflight de alcance #owner/me #type/supervision #area/personal
- [ ] Preparar anotaciones humanas independientes y decidir quién adjudica eventos críticos #owner/me #type/research #area/personal
- [ ] Revisar resultados del benchmark A/B/C antes de aceptar arquitectura operativa #owner/me #type/supervision #area/personal

## 📆 Bitácora

- **2026-09-17** — Debate A/B/C finalizado en esta conversación y propuesta técnica escrita en la nota canónica del proyecto por instrucción explícita. No se ejecutó código ni pruebas físicas; pendiente autorización del MVP y SPEC-00. Sin cierre de sesión.

## 🧭 Decisiones

- **2026-09-17:** C es candidato experimental, A baseline obligatorio, B comparador; no hay benchmark favorable certificado.
- **2026-09-17:** una sola CLI Go, herramientas especializadas externas, SQLite + filesystem en POC; sin infraestructura distribuida ni acoplamiento Echo/Hermes.
- **2026-09-17:** integridad de fuente, PTS real, separación hecho/observación/inferencia y golden humano son requisitos transversales; límites producen INCOMPLETE, nunca certeza falsa.

## 🔗 Docs / Links

- [[agents-os]] — mapa operativo de Agents-OS; fuente de verdad para startup en [[agents-os-bootstrap]].
- Fuentes técnicas candidatas a verificar/medir en SPEC-00: https://huggingface.co/Qwen/Qwen3.5-27B ; https://huggingface.co/mlx-community/Qwen3.5-27B-4bit ; https://ffmpeg.org/ffprobe.html ; https://github.com/ggml-org/whisper.cpp .
- El diseño anterior está en la conversación del 17-09-2026; esta nota es la referencia canónica actual para implementación futura, no debe tratarse como una SPEC aceptada.

## 💡 Ideas

### Backlog de ideas

- Al demostrar necesidad: clips nativos, almacenamiento MinIO, jobs PostgreSQL, observabilidad Argus, corpus completo, deduplicación entre cursos y búsqueda semántica.

### Motivos / principios

- La evidencia es la unidad de verdad operacional; inferencia produce interpretaciones, nunca certifica sola. Elegir el mínimo sistema que entregue conocimiento correcto, medible y trazable.
