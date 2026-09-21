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
updated: "2026-09-20"
---

# Multimodal Knowledge Engine

> [!important]+ Estado canónico al pausar · 2026-09-20
> **PAUSA OPERATIVA / LIVE_READY_WITH_LIMITATIONS. M0 = BLOCKED físico, NO certificado.** Implementación y recovery sintético desarrollados; la última rama dev verificada es `fix/m0-live-readiness` @ `974f74818d1a298497fff77e297f64b1dd327f61` (**NO hay merge a `master` confirmado**). NO hubo GLM live, video autorizado certificado ni SPEC-04 G0–G9 real. El owner retomará posiblemente en semanas; su «listoooo» no certifica recursos ni M0.
>
> **Entrada obligatoria para cualquier agente nuevo:** [[M0 Execution]] es el planificador único de ejecución; [[MKE — Handoff técnico y certificación M0]] reúne SHAs, resultados, evidencia, límites, seguridad y protocolo de reinicio. No utilizar entradas históricas anteriores como estado presente. No reiniciar implementación desde SPEC-00A, reabrir arquitectura ni diseñar M1.

## 🎯 Objetivo

Transformar **fuentes multimodales heterogéneas** en conocimiento estructurado y documentación técnica útil, auditable y trazable (`source → evidence → knowledge.jsonl → documentation.md`) para extraer conceptos, reglas, parámetros, procedimientos con evidencia por paso, contradicciones contextualizadas e hipótesis. Videos, cursos, trading, entrevistas y podcasts son modalidades/casos, NO dominio fijo.

- **M0 — Source → Knowledge:** primer caso un video de curso de trading autorizado (fragmento 5–10 min → video completo 1–2 h); publicar Markdown + JSONL, QA y benchmark real, incertidumbres visibles. NO basta compilar ni aprobar recorded fixtures.
- **M1 — Corpus → Documentation:** procesar fuentes múltiples e incrementalmente; consolidación por corpus, referencias, cobertura, deduplicación. Solo tras M0 PASS.
- **M2 — Knowledge → Intelligence:** conocimiento cruzado, reglas/condiciones/contradicciones e hipótesis falsables. Sin afirmaciones de rentabilidad sin pruebas independientes.

**Éxito del producto:** biblioteca documental explotable y fiel, no resumen narrativo ni CLI por sí sola. Priorizar fidelidad, cobertura recuperable, trazabilidad, utilidad y calidad; no volumen de texto, frames ni tokens.

## 📊 Estado actual — autoridad temporal más reciente

1. **2026-09-17 — Freeze:** ADR-001 y arquitectura + seis SPECs en repo de código, base `e5f9e9757d0e42b00c831e57920174428397d3b5`. Scope y gates congelados.
2. **2026-09-20 — implementación:** siete etapas implementadas, `m0-implementation` @ `77b8d6f21ca3496457c523840d62c9eb105f158e`; 16/16 paquetes y QA reportados; benchmark sintético inicial detectó fallos materiales, certificación real no ejecutada.
3. **2026-09-20 — recovery sintético:** `fix/m0-synthetic-recovery` @ `b48822d5a2be1c805bc8eff52457cea71a7d708e`. `mke plan`, cobertura de interpretación, hints de contradicciones, evaluador v2 con errata del matcher. Tres benchmarks ejecutables corrigieron omisiones y A pasa sobre recorded scripts corregidos; **C aportó 0 conocimiento correcto incremental en 3/3 con más costo**. No extrapolar a inferencia live.
4. **2026-09-20 — live readiness:** `fix/m0-live-readiness` @ `974f74818d1a298497fff77e297f64b1dd327f61` (seis commits sobre recovery; commit comprobado en GitHub). Se descubrió que benchmark de recovery NO usaba `mke plan`: requests y ventanas eran manuales. Se integró `media → plan → acquire → windows → pipeline → documentación`; E2E prueba trazabilidad desde mp4 original. Holdout nuevo con golden separado 6/6 A usando recorded provider; contrato GLM probado con servidor HTTP simulado, **sin llamada real**. Último agente reporta suite 16/16 verde y `LIVE_READY_WITH_LIMITATIONS`.
5. **Estado final M0:** `BLOCKED` para certificación física. SPEC-00A criterio 8 GLM live y SPEC-04 video real + golden ciego + G0–G9 NO certificados. Video/credencial/transcript no confirmados en este handoff. Pausado por decisión de calendario del owner, no por fallo nuevo de arquitectura. No cambiar `status` a done.

**Prueba de verdad:** resultados reported por agentes y commits Git no equivalen a reejecución de tests ni disponibilidad del entorno en esta sesión de documentación. Revalidar al reiniciar. Los artefactos bajo `~/mke/evidence/` y `artifacts/` son locales reportados, no respaldos Git confirmados.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch activo de continuidad | Base verificable | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| MKE / `xKoRx/multimodal-knowledge-engine` | `fix/m0-live-readiness` @ `974f74818d1a298497fff77e297f64b1dd327f61` (remote commit comprobado; re-fetch obligatorio) | freeze `e5f9e97` → implementación `77b8d6f` → recovery `b48822d` → readiness `974f748` | esta nota y [[MKE — Handoff técnico y certificación M0]] | `docs/architecture/architecture.md`; SPEC-00A/00B/01/02/03/04; `docs/runbooks/m0-live-certification.md` | dev listo según reports, QA real BLOCKED; no merge a master verificado |

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
- [r] [[M0 Execution]] arrancar + seguimiento — implementación/recovery/readiness entregados; en REVIEW del owner, certificación M0 real pendiente; no marcar Done antes de aceptación final. #owner/me #type/supervision #area/personal
- [ ] Disponer o identificar legítimamente video autorizado, transcript SHA-bound o ASR aceptado y GLM API key por canal seguro; no guardar credenciales/material privado en vault. #owner/me #type/admin #area/personal #blocked
- [ ] Tras M0 PASS físico, decidir alcance y delegar SPECs M1 (luego M2) con evidencia; no anticipar. #owner/me #type/supervision #area/personal #blocked

## 📆 Bitácora

- **2026-09-17:** objetivo y ADR-001 acordados, cambio de Course Intelligence Engine a Multimodal Knowledge Engine; M0 SPEC freeze en código `e5f9e97`; subproyecto [[M0 Execution]] creado. Diseño inicial anterior superseded, recuperable en historia Git.
- **2026-09-20 — primera entrega:** implementación 7/7 SPECs @ `77b8d6f`; QA fixtures, error sintético material y BLOCKED físico. Nunca fue M0 PASS.
- **2026-09-20 — recovery:** `b48822d`, 3 benchmarks A PASS sobre recorded corregido y golden congelado; C 0/3 incremental. Hints/errata/evidencia de interpretación incorporados, NO prueba de GLM real.
- **2026-09-20 — readiness:** `974f748`, ruta planificador integrada `media→plan→acquire→windows→pipeline`, holdout 6/6 recorded, HTTP GLM simulado, runbook añadido, 16/16 suites reportadas verdes; LIVE_READY_WITH_LIMITATIONS, M0 BLOCKED físico.
- **2026-09-20 — pausa y handoff intersesión:** owner pide conservar absolutamente todo para retomarlo posiblemente en semanas con nuevos agentes. Se crea [[MKE — Handoff técnico y certificación M0]] en recursos: autoridades, SHAs, pruebas y limitaciones, mapa de evidencia, four runbook erratas, dependencias físicas y protocolo exacto. Tarea puente en Review, nunca Done. No se ejecuta nuevo M0 E2E en esta documentación. Fecha de próxima sesión NO fijada.

## 🧭 Decisiones

- `Course Intelligence Engine` solo alias histórico; nombre MKE generalista, POC video trading sin types de trading en core.
- ADR-001 A antes de C y C opcional, B no implementada por puntos ciegos visuales. No vender C por el trabajo invertido; recuperar conocimiento correcto incremental es la medida.
- GLM tras VLMProvider, Whisper tras ASRProvider; Qwen/M4/Kronos no bloquean M0 con backend aceptado. Modelo/endpoint/compatibilidad reales no presumidos.
- Product-first 00A, SQLite+FS cuando necesario 02; nada de infraestructura por anticipación.
- QA no auto-certificado, golden blind, replay ≠ live, no afirmaciones falsas de verdad humana/externa, JSONL canónico.
- Historial sintético anterior NO_GO conservado; recovery PASS sobre tres casos y holdout 6/6 no son certificación M0. Gate definitivo físico/spec basado en evidencia.
- Roadmap de oportunidades diferido y ya persistido, sin scope creep M0.

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
