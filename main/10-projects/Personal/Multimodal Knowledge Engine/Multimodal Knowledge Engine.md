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
updated: "2026-09-28"
---

# Multimodal Knowledge Engine

> [!important]+ Estado canónico al cerrar · 2026-09-28
> **CERTIFICACIÓN M0 REAL EJECUTADA: `M0_NO_GO`.** El producto y la ruta física quedaron probados de punta a punta; el fallo está acotado a acreditación/evaluación, no a media/evidence foundation. Corrida formal reportada: 26/26 ventanas, 348 llamadas, ~5.2M tokens, G1/G3/G4/G8 PASS; G2 falló con 7/7 reglas críticas sin acreditar y G5 con 6 excepciones ocultas. QA posterior verificó que las 7 reglas estaban presentes en el material recuperado.
>
> **Workstream vigente: `M0-R1 — Bounded Remediation + Local Runtime Completion`.** Scope autorizado por Owner: corregir grounding audio-only, evaluación cross-language y robustez de verdicts/runbook; además dejar Whisper local operativo detrás de `ASRProvider` y recertificar G0–G9 sobre el mismo source/golden cuando sea válido. No reabrir arquitectura, no M1/M2, no usar C para esconder un baseline A roto.
>
> Repo de continuidad: `fix/m0-live-readiness` @ `974f74818d1a298497fff77e297f64b1dd327f61` es el último HEAD remoto verificado. El ejecutor anterior reportó cambios locales no commiteados de OpenRouter/runbook; un nuevo agente debe inspeccionar worktree/HEAD reales antes de tocar nada.

## 🎯 Objetivo

Transformar **fuentes multimodales heterogéneas** en conocimiento estructurado y documentación técnica útil, auditable y trazable (`source → evidence → knowledge.jsonl → documentation.md`) para extraer conceptos, reglas, parámetros, procedimientos con evidencia por paso, contradicciones contextualizadas e hipótesis. Videos, cursos, trading, entrevistas y podcasts son modalidades/casos, NO dominio fijo.

- **M0 — Source → Knowledge:** primer caso un video de curso de trading autorizado (fragmento 5–10 min → video completo 1–2 h); publicar Markdown + JSONL, QA y benchmark real, incertidumbres visibles. NO basta compilar ni aprobar recorded fixtures.
- **M1 — Corpus → Documentation:** procesar fuentes múltiples e incrementalmente; consolidación por corpus, referencias, cobertura, deduplicación. Solo tras M0 PASS.
- **M2 — Knowledge → Intelligence:** conocimiento cruzado, reglas/condiciones/contradicciones e hipótesis falsables. Sin afirmaciones de rentabilidad sin pruebas independientes.

**Éxito del producto:** biblioteca documental explotable y fiel, no resumen narrativo ni CLI por sí sola. Priorizar fidelidad, cobertura recuperable, trazabilidad, utilidad y calidad; no volumen de texto, frames ni tokens.

## 📊 Estado actual — autoridad temporal más reciente

1. **2026-09-17 — Freeze:** ADR-001 y arquitectura + seis SPECs congeladas en repo, base `e5f9e9757d0e42b00c831e57920174428397d3b5`.
2. **2026-09-20 — implementación/recovery/readiness:** rama de continuidad llegó a `fix/m0-live-readiness @ 974f74818d1a298497fff77e297f64b1dd327f61`; ruta `media → plan → acquire → windows → pipeline` y holdout recorded quedaron listos, todavía sin certificación física.
3. **2026-09-28 — certificación física real:** source autorizado y credencial VLM estuvieron disponibles y se ejecutó el pipeline real completo. Resultado formal `M0_NO_GO`, no `BLOCKED`. G1/G3/G4/G8 pasaron; G2/G5 fallaron.
4. **Diagnóstico aceptado R1:** (a) grounding reviewer recibe referencias de transcript sin texto suficiente: 0/147 audio-only soportados vs 65/176 con imagen; (b) golden español vs publicación mayormente inglesa hace fallar equivalencia lexical; (c) ~15.7% verdicts malformados fallan cerrado correctamente pero erosionan recall/costo; (d) runbook/budget tuvo erratas físicas detectadas al ejecutar.
5. **Producto demostrado:** frames/PTS/provenance, multimodalidad visual y honestidad del grounding quedaron físicamente evidenciados; QA reportó 10/10 afirmaciones soportadas honestas y cero alucinaciones publicadas como soportadas en la muestra.
6. **Objetivo operacional refinado por Owner:** Whisper/local ASR deja de ser opcional para este workstream. M0-R1 debe dejar ASR local funcional detrás de `ASRProvider`, sin acoplar dominio ni abrir routing/infra nueva.
7. **Siguiente gate único:** ejecutar el prompt/mandato M0-R1 ya definido, preservar source/golden/baseline, aplicar invalidation mínima y volver a certificar G0–G9. Sólo `M0_R1_PASS` habilita cierre M0 y planificación M1.

La certificación y los artefactos físicos fueron reportados en Daedalus bajo `~/mke/m0-20260928/`; esa ruta es evidencia local y debe revalidarse en el host antes de asumir persistencia. Los cambios no commiteados reportados por el ejecutor no son autoridad Git hasta ser inspeccionados y committeados.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch activo de continuidad | Base verificable | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| MKE / `xKoRx/multimodal-knowledge-engine` | `fix/m0-live-readiness` @ `974f74818d1a298497fff77e297f64b1dd327f61` (último HEAD remoto verificado; inspeccionar posibles cambios locales antes de modificar) | freeze `e5f9e97` → implementación `77b8d6f` → recovery `b48822d` → readiness `974f748` | esta nota + [[M0 Execution]] | `docs/architecture/architecture.md`; SPEC-00A/00B/01/02/03/04; `docs/runbooks/m0-live-certification.md` | certificación real ejecutada: `M0_NO_GO`; remediation M0-R1 + Whisper local pendientes |

## 1. Contrato funcional y boundaries vigentes

**Entrada M0:** video con derechos suficientes, original inmutable SHA-256, streams/PTSes, transcript ligado a hash o ASR aceptado, config/model/presupuesto versionados. **Salida:** `Evidence`, `KnowledgeItem`, `Procedure` y `Relation`, JSONL canónico + Markdown derivado, reporte de QA/cobertura/incertidumbre y enlaces al original/tiempo real. Cada afirmación material y cada paso de procedimiento requiere evidencia propia; si es ilegible `UNKNOWN/UNREADABLE/INSUFFICIENT`, nunca inventar valor. Se preservan condiciones, negaciones y excepciones distantes.

ADR-001 **Bounded Hybrid Evidence Acquisition**: A baseline fijo primero, C investigator opcional que solo emite preguntas y solicitudes tipadas para volver al MISMO pipeline A. Un toggle `adaptive_investigation`. C se descarta por reglas SPEC-04 si no agrega conocimiento correcto útil sin regresiones/costo injustificado; el 0/3 sintético no es conclusión universal sobre C.

```text
original/hash/PTS
 ├─ ASR + transcript normalizado
 └─ cobertura visual independiente + activity index
       → planning context no autoritativo
       → selección inicial determinista `mke plan`
       → adquisición tipada `mke acquire` + evidencia SQLite/FS
       → ventanas desde evidencia comprometida `mke windows`
       → reconstruction → integrity → grounding → consolidación/revalidación
       → JSONL canónico → documentación Markdown + interpretación/QA
```

`FRAME|REGION|COMPARE|SEQUENCE|FIND_CHANGE`, presupuestos finitos, dedupe lógico `request_id ≠ acquisition_key`, reintento/crash/resume, tiempo PTS efectivo ≠ tiempo solicitado. Nunca confundir evento inspeccionado/adquirido con contenido interpretado. `interpretation.jsonl` expone evidencia sin referencias en conocimiento. Hints deterministas de conflicto NO son relaciones CONTRADICTS soportadas y no eligen verdad; las relaciones provienen de reconstruction con grounding. Taxonomía de `KnowledgeItem.kind` solo `claim|concept|rule|parameter|observation` (`event` inválido se rechaza auditablemente, nunca publica).

Fronteras externas justificadas: `VLMProvider` y `ASRProvider`; GLM-5.3-Flash backend inicial; Qwen/Ollama/LM Studio/Whisper futuros opcionales. Monolito Go CLI, FFmpeg/ffprobe, SQLite+FS, sin Kafka/Temporal/vector DB/frontend/microservicios/MinIO/Postgres obligatorios. No modificar Echo/Forge/Hermes productivos. Fuente es entrada NO CONFIABLE; nada en video/transcript manda herramientas, permisos ni secretos.

Determinismo = replay y orquestación/IDs/publicación para salidas de provider grabadas, nunca inferencia live determinista. JSONL es la fuente estructurada canónica; Markdown no se reparsea para reconstruir conocimiento. Grounding reviewer stateless con separación de contexto, estados explícitos y `SUPPORTED_BY_AUTOMATED_REVIEW` no significa verdad externa/humana. `EXTERNALLY_CHECKED` y `EMPIRICALLY_VALIDATED` requieren evidencia independiente real.

## 2. QA y decisión del producto

- Roles separados: manager / implementer / evaluador golden desde ORIGINAL / QA adversarial. Golden se congela ANTES de que su evaluador vea outputs 00A/A/C; jamás alimentar golden al engine, ajustar evaluación y llamarla independiente ni usar texto del modelo como fuente primaria.
- Paired A/C: mismos source bytes, transcript, índice/evidencia inicial, VLM/config común, reconstruction/reviewer/publisher; única diferencia intencional adaptive acquisition. Registrar ambos aciertos, solo A, solo C, ambos fallan, errores extra de C, primera frontera de pérdida y costo real/ceiling comparable. La existencia de C no justifica elegirlo.
- Gates reales SPEC-04: G0 precondiciones físicas/derechos/modelo; G1 PTS real; G2 cero omisiones recuperables críticas en golden; G3 cero valores críticos erróneos soportados; G4 refs íntegras; G5 no perder excepciones/claims sin fuente; G6 honestidad de grounding/conflictos; G7 crash/resume/dedup; G8 budget o INCOMPLETE explícito; G9 otro agente reconstruye ítems/pasos críticos desde docs + evidencia. Un A que falla gates no se salva con C. `AGENT_GOLDEN`/`AGENT_REVIEWED` no es verificación humana.
- SPEC-00A criterio 8 exige fragmento autorizado inferido con GLM live y knowledge real rastreable; SPEC-04 exige video completo y benchmark independiente. Ambos siguen pendientes a fecha corte.
- Exit codes congelados: `0=complete`, `2=invalid-input`, `3=unsupported`, `4=incomplete`, `5=fatal`, `6=retry-exhausted`. No maquillar terminales.

## 3. Roadmap ejecutado y siguiente gate

| Etapa | Implementación reportada | Certificación pendiente |
|---|---|---|
| 00A Product Spike | CLI/recorded E2E PASS parcial | criterio-8 GLM live sobre clip autorizado |
| 00B Runtime | adapters/contract probes con fakes | targets locales opcionales no certificados; GLM remoto requiere prueba live |
| 01 Media | media/PTS/coverage fixtures PASS | corroborar con video físico |
| 02 Evidence | typed acquisition/SQLite/resume fixtures PASS | corroborar en run real |
| 03-A Baseline | replay determinista/grounding/publicación PASS | calidad/grounding sobre video real |
| 03-C Investigator | implementado/replay PASS | valor comparativo real puede ser NO_GO sin bloquear A |
| 04 Integration | harness, golden, recovery y benchmark recorded | SPEC-04 G0–G9 físico integral, resultado M0_PASS/NO_GO/BLOCKED |

**Próxima acción NO es implementar otra SPEC ni buscar más ideas.** Reanudar con [[MKE — Handoff técnico y certificación M0]] §9, corregir las cuatro erratas operativas del runbook original y ejecutar certificación física de fuente real bajo QA separado. No afirmar disponibilidad de video/key/transcript por el «listo» del owner; verificar sin exponer secretos. Si faltan, BLOCKED y solicitud única mínima. Guardar resultados verificables en [[M0 Execution]]. Solo si M0 PASS, planificar M1 basándose en resultados físicos.

## 4. Roadmap posterior — CANDIDATOS, sin aprobación M0

Repo: `docs/roadmap/post-m0-opportunities.md` (`master`, commit de alta `c9c0d3cd703c4f18e2f4439e3263f7a8a17e21b3`; verificar HEAD al retomar). Secuencia propuesta: R0 certificación, R0-FIX por fallos reales; R1 video-use VU-01 planning context compacto y VU-02 evidence timeline para QA como experimentos aislados; M1 corpus incremental; opcionales MarkItDown (documentos) y Agent Reach (adquisición autorizada); WeKnora como índice derivado para consulta, nunca autoridad; M2 análisis transversal; OpenMAIC/HyperFrames publicación opcional fuera del core. Ninguna dependencia nueva entra a M0 por inspiración. Código después de M0 PASS y aprobación de scope; research read-only posible sin desviar QA.

## 🧩 Subproyectos

- [[M0 Execution]] — proyecto `owner: agent`, planificador durable único; implementación, recovery y readiness entregados, certificación física pendiente de reanudar. No crear otro proyecto paralelo para el MISMO M0 ni marcarlo done.

## ✅ Tareas

- [x] Convergencia arquitectónica ADR-001 y SPECs M0 freeze. #owner/me #type/admin #area/personal
- [x] Fijar objetivo de conocimiento, QA delegado, contratos visuales y milestones. #owner/me #type/admin #area/personal
- [x] Renombrar Course Intelligence Engine → MKE, vincular repo y alias histórico. #owner/me #type/admin #area/personal
- [x] Autorizar y despachar implementación M0 con gates; recovery y live readiness quedaron entregados por el agente (NO certificación física). #owner/me #type/admin #area/personal
- [r] [[M0 Execution]] seguimiento — certificación física original ejecutada con `M0_NO_GO`; planificador ahora conduce M0-R1 hasta recertificación. Mantener en Review; no Done antes de `M0_R1_PASS` y aceptación humana. #owner/me #type/supervision #area/personal
- [x] Inputs físicos de certificación original disponibles: source autorizado + credencial VLM + transcript/ASR aceptado permitieron corrida real; secretos/material privado permanecen fuera del vault. ✅2026-09-28 #owner/me #type/admin #area/personal
- [ ] Ejecutar `M0-R1 — Bounded Remediation + Local Runtime Completion`: corregir R1-01..04, dejar Whisper local funcional vía `ASRProvider`, revalidar contra source/golden preservados y cerrar G0–G9. #owner/agent #type/dev #area/personal
- [ ] Tras `M0_R1_PASS`, decidir alcance y delegar SPECs M1 (luego M2) con evidencia; no anticipar. #owner/me #type/supervision #area/personal #blocked

## 📆 Bitácora

- **2026-09-17:** objetivo y ADR-001 acordados, cambio de Course Intelligence Engine a Multimodal Knowledge Engine; M0 SPEC freeze en código `e5f9e97`; subproyecto [[M0 Execution]] creado. Diseño inicial anterior superseded, recuperable en historia Git.
- **2026-09-20 — primera entrega:** implementación 7/7 SPECs @ `77b8d6f`; QA fixtures, error sintético material y BLOCKED físico. Nunca fue M0 PASS.
- **2026-09-20 — recovery:** `b48822d`, 3 benchmarks A PASS sobre recorded corregido y golden congelado; C 0/3 incremental. Hints/errata/evidencia de interpretación incorporados, NO prueba de GLM real.
- **2026-09-20 — readiness:** `974f748`, ruta planificador integrada `media→plan→acquire→windows→pipeline`, holdout 6/6 recorded, HTTP GLM simulado, runbook añadido, 16/16 suites reportadas verdes; LIVE_READY_WITH_LIMITATIONS, M0 BLOCKED físico.
- **2026-09-20 — pausa y handoff intersesión:** owner pide conservar absolutamente todo para retomarlo posiblemente en semanas con nuevos agentes. Se crea [[MKE — Handoff técnico y certificación M0]] en recursos: autoridades, SHAs, pruebas y limitaciones, mapa de evidencia, four runbook erratas, dependencias físicas y protocolo exacto. Tarea puente en Review, nunca Done. No se ejecuta nuevo M0 E2E en esta documentación. Fecha de próxima sesión NO fijada.

- **2026-09-28 — certificación física M0:** corrida real completa reportada sobre source autorizado: 26/26 ventanas, 348 VLM calls, ~5.2M tokens, costo reportado 0. Resultado `M0_NO_GO`: G1/G3/G4/G8 PASS; G2 7/7 critical recoverable sin acreditar; G5 6 excepciones ocultas. QA determinó que los 7 ítems estaban presentes en material recuperado, apuntando a grounding/evaluación y no a acquisition.
- **2026-09-28 — remediation owner:** se autoriza workstream acotado `M0-R1` y se eleva Whisper/local ASR a requisito operacional. Mandato entregado para IMPLEMENT→TEST→QA→recertificación, sin M1/M2 ni rediseño general.

## 🧭 Decisiones

- `Course Intelligence Engine` solo alias histórico; nombre MKE generalista, POC video trading sin types de trading en core.
- ADR-001 A antes de C y C opcional, B no implementada por puntos ciegos visuales. No vender C por el trabajo invertido; recuperar conocimiento correcto incremental es la medida.
- GLM tras VLMProvider, Whisper tras ASRProvider; Qwen/M4/Kronos no bloquean M0 con backend aceptado. Modelo/endpoint/compatibilidad reales no presumidos.
- Product-first 00A, SQLite+FS cuando necesario 02; nada de infraestructura por anticipación.
- QA no auto-certificado, golden blind, replay ≠ live, no afirmaciones falsas de verdad humana/externa, JSONL canónico.
- Historial sintético anterior NO_GO conservado; recovery PASS sobre tres casos y holdout 6/6 no son certificación M0. Gate definitivo físico/spec basado en evidencia.
- Roadmap de oportunidades diferido y ya persistido, sin scope creep M0.
- Para M0-R1, el golden existente se preserva hash-identical; corregir evaluación cross-language NO autoriza traducir/regenerar golden ni relajar valores/condiciones/negaciones/excepciones.
- Whisper/local ASR es ahora requisito operacional del Owner para cerrar M0-R1, pero sigue detrás de `ASRProvider`; este refinement no autoriza acoplar media/pipeline a Whisper ni crear routing/infra adicional.

## 🔗 Docs / Links

- **Punto de entrada para nuevo agente:** [[MKE — Handoff técnico y certificación M0]].
- **Planificador:** [[M0 Execution]].
- [Rama de código de continuidad](https://github.com/xKoRx/multimodal-knowledge-engine/tree/fix/m0-live-readiness) y [commit verificable `974f748`](https://github.com/xKoRx/multimodal-knowledge-engine/commit/974f74818d1a298497fff77e297f64b1dd327f61).
- [Arquitectura congelada](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/architecture/architecture.md); [SPEC-00A](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-00A-product-spike.md); [SPEC-04](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-04-integration-benchmark.md).
- [Runbook físico (leer erratas en recurso antes de usar)](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/runbooks/m0-live-certification.md).
- [Roadmap posterior](https://github.com/xKoRx/multimodal-knowledge-engine/blob/master/docs/roadmap/post-m0-opportunities.md).
- [[agents-os]], [[agents-os-bootstrap]], [[agents-os-agent-project-workflow]], [[agents-os-session-close]].

## 💡 Ideas diferidas

- Video-use, MarkItDown, Agent Reach, WeKnora, OpenMAIC/HyperFrames: solo experimentos futuros; ver roadmap. Postgres/MinIO/vector DB/cluster/Argus/otros modelos solo por evidencia de necesidad; sin desviar M0.
