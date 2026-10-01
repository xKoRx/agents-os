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
updated: "2026-10-01"
reviewed: "2026-10-01"
---

# Multimodal Knowledge Engine

> [!important]+ Estado canónico · 2026-09-30
> **V1 / M0-R1 = CLOSED_AS_REMEDIATED** @ `fix/m0-live-readiness` `640d000eb6993de2e0181a64e7a693021f364a1a`. `M0_R1_REMEDIATION = PASS`, golden preservado, `M0 = NOT_RECERTIFIED` y la recertificación completa G0–G9 no se ejecutó.
>
> **D4 = DEFERRED_TO_V3.** El gap de scoring multi-record queda preservado como evidencia histórica; V2 no modifica el golden ni hace composition-aware benchmark scoring.
>
> **V2 = SHOT 3 COMPLETE / FINAL CERTIFICATION PASS.** `V2_DESIGN = ACCEPTED`, `ARCHITECTURE = FROZEN`, `SHOT2_REVIEW = FINDINGS (1C/6MA/10MI/12NOTE)` @ `8ad46c8`, `SHOT3_REMEDIATION = PASS`, `V2_FINAL_CERTIFICATION = PASS` @ `cc13a121cebbddf153f283a3df0f4197dfb92cc1` (push FF a origin). V1 baseline/golden intactos, `D4_TOUCHED = NO`, sin entrada a V3. Limitación real documentada: la certificación física corre sobre fuente real con adapter recorded (CLI `--vlm recorded:`); no hubo smoke live con modelo real en Shot 3 (sin credencial por-corrida; el intento live de Shot 1 con OpenRouter quedó como evidencia previa). Artefactos: `~/mke/v2-shot3-cert-20260930/`. Actualización 2026-10-01: el smoke live se ejecutó sobre Clutifx ep01 completo — `CLUTIFX_CH01_EXTRACTION = BLOCKED` (L0 PASS full-chapter; L1 FATAL contractual de identidad @ w0003; ver `evaluations/clutifx/chapter-01/` y bitácora). Actualización 2026-10-01 (identity remediation): design + implementación + suite `cc13a12..71b5a21` (3 commits, `docs/v2/remediation/CLUTIFX-LONG-SOURCE-CLAIM-IDENTITY-REMEDIATION.md` como autoridad); independent adversarial review = `FINDINGS` (0 CRITICAL / 0 MAJOR / 1 MINOR de instrumentación / 4 NOTE, `READY_FOR_MANAGER_ADJUDICATION = YES`, live no ejecutado; detalles en bitácora).

**Workstream vigente: MKE V2 — Layered Knowledge Model.** V1 queda como baseline preservada y evidencia del porqué existe V2; no reabrir findings M0-R1 salvo regresión concreta.
## 🎯 Objetivo

Transformar **fuentes multimodales heterogéneas** en conocimiento estructurado y documentación técnica útil, auditable y trazable (`source → evidence → knowledge.jsonl → documentation.md`) para extraer conceptos, reglas, parámetros, procedimientos con evidencia por paso, contradicciones contextualizadas e hipótesis. Videos, cursos, trading, entrevistas y podcasts son modalidades/casos, NO dominio fijo.

- **M0 — Source → Knowledge:** primer caso un video de curso de trading autorizado (fragmento 5–10 min → video completo 1–2 h); publicar Markdown + JSONL, QA y benchmark real, incertidumbres visibles. NO basta compilar ni aprobar recorded fixtures.
- **M1 — Corpus → Documentation:** procesar fuentes múltiples e incrementalmente; consolidación por corpus, referencias, cobertura, deduplicación. Solo tras M0 PASS.
- **M2 — Knowledge → Intelligence:** conocimiento cruzado, reglas/condiciones/contradicciones e hipótesis falsables. Sin afirmaciones de rentabilidad sin pruebas independientes.

**Éxito del producto:** biblioteca documental explotable y fiel, no resumen narrativo ni CLI por sí sola. Priorizar fidelidad, cobertura recuperable, trazabilidad, utilidad y calidad; no volumen de texto, frames ni tokens.

## 📊 Estado actual — autoridad temporal más reciente

1. **V1 cerrada como remediada:** `640d000` es la baseline congelada; Shot 3 fue aceptado adversarialmente y el golden permaneció intacto.
2. **M0 no fue recertificado:** la certificación física original terminó `M0_NO_GO`; la remediación quedó aceptada, pero no hubo rerun final G0–G9.
3. **D4 diferido:** el desacople entre records atómicos y reglas multi-cláusula del golden no se corrige en V2; queda para V3 junto con composition-aware evaluation.
4. **V2 Design aceptado:** L0 reutiliza source/media/evidence/coverage V1; L1 introduce claims explícitamente atómicos; L2 agrega SKOs compuestos sólo desde L1 válido.
5. **KISS/YAGNI preservado:** sin nueva DB, queue, graph/vector store, RAG, search, intent/questions, cross-source composition ni SKO nesting.
6. **Design Pack físico:** `docs/v2/V2-ARCHITECTURE.md`, `V2-FUNCTIONAL-CONTRACT.md`, `V2-TECHNICAL-CONTRACT.md`, `V2-ACCEPTANCE-PLAN.md`, `V2-IMPLEMENTATION-PLAN.md` sobre `feature/v2-layered-knowledge-model @ 618043e`.
7. **Shot 1 aceptado:** implementation + focused remediation `MGR-S1-01` cerrados @ `8ad46c8`.
8. **Shot 2 ejecutado:** review adversarial independiente `SHOT2_REVIEW = FINDINGS` @ `8ad46c8` (1 CRITICAL / 6 MAJOR / 10 MINOR / 12 NOTE, `READY_FOR_SHOT3 = YES`); repros físicos en harnesses `zz_shot2_*` de 5 worktrees de review.
9. **Shot 3 completado:** adjudicación + remediation + certificación final `PASS` @ `cc13a12`; 7 mandatorios cerrados (A-01, C-01, B-01, E-01, G-01, G-02, T-01), minors acotados cerrados (A-03, D-01, J-03, K-01, T-03), acceptance adversarial independiente PASS (0 defectos nuevos), replay físico byte-idéntico, provenance física resuelta a SHA real.
La certificación y los artefactos físicos fueron reportados en Daedalus bajo `~/mke/m0-20260928/`; esa ruta es evidencia local y debe revalidarse en el host antes de asumir persistencia. Los cambios no commiteados reportados por el ejecutor no son autoridad Git hasta ser inspeccionados y committeados.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch activo de continuidad | Base verificable | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| MKE / `xKoRx/multimodal-knowledge-engine` | V1: `fix/m0-live-readiness @ 640d000`; V2: `feature/v2-layered-knowledge-model @ cc13a12` | V2 parte exactamente de `640d000`; Design Freeze `618043e` | `docs/v2/V2-FUNCTIONAL-CONTRACT.md` | `docs/v2/V2-TECHNICAL-CONTRACT.md` + `V2-ARCHITECTURE.md` | `V2_FINAL_CERTIFICATION = PASS` (Shot 3 @ `cc13a12`) |

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

**Próxima acción:** implementar el mínimo V2 completo definido por el Design Pack sobre la branch V2, sin reabrir V1 ni introducir D4/V3. La secuencia está congelada en exactamente tres shots.

## 4. Roadmap posterior — CANDIDATOS, sin aprobación M0

Repo: `docs/roadmap/post-m0-opportunities.md` (`master`, commit de alta `c9c0d3cd703c4f18e2f4439e3263f7a8a17e21b3`; verificar HEAD al retomar). Secuencia propuesta: R0 certificación, R0-FIX por fallos reales; R1 video-use VU-01 planning context compacto y VU-02 evidence timeline para QA como experimentos aislados; M1 corpus incremental; opcionales MarkItDown (documentos) y Agent Reach (adquisición autorizada); WeKnora como índice derivado para consulta, nunca autoridad; M2 análisis transversal; OpenMAIC/HyperFrames publicación opcional fuera del core. Ninguna dependencia nueva entra a M0 por inspiración. Código después de M0 PASS y aprobación de scope; research read-only posible sin desviar QA.

## 🧩 Subproyectos

- [[M0 Execution]] — planificador histórico de V1/M0; cerrado como remediado @ `640d000`, sin recertificación final. Conservar como evidencia, no usar para conducir V2.

## ✅ Tareas

- [x] Convergencia arquitectónica ADR-001 y SPECs M0 freeze. #owner/me #type/admin #area/personal
- [x] Fijar objetivo de conocimiento, QA delegado, contratos visuales y milestones. #owner/me #type/admin #area/personal
- [x] Renombrar Course Intelligence Engine → MKE, vincular repo y alias histórico. #owner/me #type/admin #area/personal
- [x] Autorizar y despachar implementación M0 con gates; recovery y live readiness quedaron entregados por el agente (NO certificación física). #owner/me #type/admin #area/personal
- [r] [[M0 Execution]] seguimiento — V1/M0-R1 cerrado por decisión Owner como `CLOSED_AS_REMEDIATED`; M0 quedó `NOT_RECERTIFIED`. El bridge permanece en Review según workflow de proyecto de agente. #owner/me #type/supervision #area/personal
- [x] Inputs físicos de certificación original disponibles: source autorizado + credencial VLM + transcript/ASR aceptado permitieron corrida real; secretos/material privado permanecen fuera del vault. ✅2026-09-28 #owner/me #type/admin #area/personal
- [x] Cerrar V1/M0-R1 como `CLOSED_AS_REMEDIATED` @ `640d000`; preservar `M0 = NOT_RECERTIFIED` y diferir D4 a V3. ✅2026-09-29 #owner/me #type/admin #area/personal
- [x] Liderar y congelar MKE V2 Design Pack L0/L1/L2 sobre baseline `640d000`; `V2_DESIGN = ACCEPTED`. ✅2026-09-29 #owner/me #type/supervision #area/personal
- [x] Ejecutar V2 Shot 1 — minimum complete implementation según `docs/v2/V2-IMPLEMENTATION-PLAN.md`; manager recheck final PASS @ `8ad46c8`, `MGR-S1-01 = CLOSED`. ✅2026-09-30 #owner/agent #type/dev #area/personal
- [x] Ejecutar V2 Shot 2 — independent adversarial review, sin fixes de producto: `SHOT2_REVIEW = FINDINGS` @ `8ad46c8` (1C/6MA/10MI/12NOTE), repros físicos en worktrees de review. ✅2026-09-30 #owner/agent #type/testing #area/personal
- [x] Ejecutar V2 Shot 3 — adjudicación, remediation y final certification: `V2_FINAL_CERTIFICATION = PASS` @ `cc13a12`, acceptance independiente PASS, suites 20/20, físico completo sobre fuente real. ✅2026-09-30 #owner/agent #type/testing #area/personal
- [x] Ejecutar primera extracción full real live (Clutifx ch01) con V2 `cc13a12`: L0 COMPLETE, L1 `BLOCKED` por FATAL contractual de identidad (S2-B-01) @ w0003; review bundle en `evaluations/clutifx/chapter-01/`; decisión Owner+Manager pendiente. ✅2026-10-01 #owner/agent #type/testing #area/personal
- [x] Independent adversarial review de la identity remediation (`cc13a12..71b5a21`, frentes A–T): `IDENTITY_ADVERSARIAL_REVIEW = FINDINGS` (0C/0MA/1MI/4NOTE); sin product fixes, sin live; `READY_FOR_MANAGER_ADJUDICATION = YES`. ✅2026-10-01 #owner/agent #type/testing #area/personal

## 📆 Bitácora

- **2026-09-17:** objetivo y ADR-001 acordados, cambio de Course Intelligence Engine a Multimodal Knowledge Engine; M0 SPEC freeze en código `e5f9e97`; subproyecto [[M0 Execution]] creado. Diseño inicial anterior superseded, recuperable en historia Git.
- **2026-09-20 — primera entrega:** implementación 7/7 SPECs @ `77b8d6f`; QA fixtures, error sintético material y BLOCKED físico. Nunca fue M0 PASS.
- **2026-09-20 — recovery:** `b48822d`, 3 benchmarks A PASS sobre recorded corregido y golden congelado; C 0/3 incremental. Hints/errata/evidencia de interpretación incorporados, NO prueba de GLM real.
- **2026-09-20 — readiness:** `974f748`, ruta planificador integrada `media→plan→acquire→windows→pipeline`, holdout 6/6 recorded, HTTP GLM simulado, runbook añadido, 16/16 suites reportadas verdes; LIVE_READY_WITH_LIMITATIONS, M0 BLOCKED físico.
- **2026-09-20 — pausa y handoff intersesión:** owner pide conservar absolutamente todo para retomarlo posiblemente en semanas con nuevos agentes. Se crea [[MKE — Handoff técnico y certificación M0]] en recursos: autoridades, SHAs, pruebas y limitaciones, mapa de evidencia, four runbook erratas, dependencias físicas y protocolo exacto. Tarea puente en Review, nunca Done. No se ejecuta nuevo M0 E2E en esta documentación. Fecha de próxima sesión NO fijada.

- **2026-09-28 — certificación física M0:** corrida real completa reportada sobre source autorizado: 26/26 ventanas, 348 VLM calls, ~5.2M tokens, costo reportado 0. Resultado `M0_NO_GO`: G1/G3/G4/G8 PASS; G2 7/7 critical recoverable sin acreditar; G5 6 excepciones ocultas. QA determinó que los 7 ítems estaban presentes en material recuperado, apuntando a grounding/evaluación y no a acquisition.
- **2026-09-28 — remediation owner:** se autoriza workstream acotado `M0-R1` y se eleva Whisper/local ASR a requisito operacional. Mandato entregado para IMPLEMENT→TEST→QA→recertificación, sin M1/M2 ni rediseño general.
- **2026-09-29 — M0-R1 Shots 1–3:** Shot 1 implementación (`dad3891`), Shot 2 revisión adversarial (8 MAJOR/13 MINOR/12 NOTE, sin CRITICAL), Shot 3 remediación completa + aceptación adversarial independiente PASS @ `640d000` (8 commits). Golden intacto `91c3dd57…`. D4 = CONTRACT_DECISION_REQUIRED (composición multi-record); recertificación G0–G9 pendiente de decisión owner + credencial por-corrida + smoke live. Planificador: [[M0 Execution]].
- **2026-09-29 — cierre V1 + Design V2:** Owner congela V1/M0-R1 como `CLOSED_AS_REMEDIATED`, mantiene `M0 = NOT_RECERTIFIED` y difiere D4 a V3. Manager verifica `fix/m0-live-readiness @ 640d000`, inspecciona contracts/source V1 y concluye que L0 ya existe mayormente, mientras V1 knowledge mezcla atomicidad y composición. Se crea `feature/v2-layered-knowledge-model` desde `640d000` y se congela Design Pack L0/L1/L2 @ `618043e`, sin product code.
- **2026-09-29 — finalización Design V2:** review final cierra D-FIX-01..04: atomicidad operacional L1, bounded direct-relation closure L2, boundary de run journal preservada e invocación `mke pipeline` con config schema v1/v2 explícita. Adversarial read final verifica merge-base `640d000`, branch behind=0 y diff limitado a cinco `docs/v2/*`. Design Pack final @ `618043e`; `ARCHITECTURE = FROZEN`, `READY_FOR_V2_SHOT_1 = YES`.
- **2026-09-30 — manager recheck final Shot 1:** candidate `218875e` fue revisada y se detectó `MGR-S1-01` (claim→L0 dependency edges incompletos para multi-ref). Focused remediation `8ad46c8` persiste todos los refs L0 de forma sorted/deduplicated e idempotente; regression consulta `run.db` vía `ListDependencyEdges()` y cubre multi-ref, transcript+visual y crash/resume. Manager acepta Shot 1: `V2_SHOT1_IMPLEMENTATION = PASS`, `READY_FOR_V2_SHOT_2 = YES`.
- **2026-09-30 — V2 Shot 2 (review adversarial):** `SHOT2_REVIEW = FINDINGS` @ `8ad46c8`: 1 CRITICAL (S2-C-01: relation review sin statements de endpoints — relación invertida publicó SUPPORTED end-to-end), 6 MAJOR (S2-A-01 reconstruction sin texto de transcript citado; S2-B-01 identidad/versión divergente suprimida por orden; S2-E-01 phantom reasons no deterministas; S2-G-01 budget cuenta sólo claims; S2-G-02 reason over-budget imprime puntero; S2-T-01 provider requests sin test de contenido), 10 MINOR, 12 NOTE. `READY_FOR_SHOT3 = YES`. Repros físicos: harnesses `zz_shot2_*` sin commit en `~/aranea/work/mke-v2-shot2-review-20260930/wt-{A..E}`.
- **2026-09-30 — V2 Shot 3 (adjudicación + remediation + certificación final):** `SHOT3_REMEDIATION = PASS` y `V2_FINAL_CERTIFICATION = PASS` @ `cc13a121cebbddf153f283a3df0f4197dfb92cc1` (4 commits FF pusheados sobre `8ad46c8`). Mandatorios cerrados con regresión permanente y repro refutado físicamente: S2-C-01 (endpoints exactos id@versión+statement+orientación en el request durable; endpoints irresolubles fail-closed), S2-A-01 (todo segmento citado viaja con su texto, transcript-only/visual/multimodal, sin duplicación), S2-B-01 (idéntico=dedup idempotente; divergente=ClassFatal corruption en ambos órdenes de ventana; duplicate relation ids rechazados uniformes), S2-E-01 (phantom reasons en orden canónico; replay byte-estable), S2-G-01 (budget acota catálogo completo claims+relations; one-below rechaza sin composer call), S2-G-02 (reason con "budget (N)" literal, documentation.md byte-idéntico entre corridas), S2-T-01 (probe de captura con 8 tests permanentes sobre las 5 boundaries + corrective reissue). Minors acotados: S2-A-03 (ventana cross-source rechazada antes de cualquier llamada), S2-D-01 (decoders exigen un único documento JSON), S2-J-03 (L2 fingerprint liga adapter/model), S2-K-01 (readbacks cubren provenance/reasons; corrupción de fila commiteada falla el resume cerrado), S2-T-03 (loader de proyecciones distingue EOF de corrupción). No-mandatorios preservados según adjudicación (D-02, H-01, K-02, M-01, T-02 y NOTES sin fix). Acceptance adversarial independiente: PASS con poder de detección demostrado (17 ataques propios fallan en baseline y pasan en `cc13a12`), `NEW_DEFECTS: NONE`. Suites: 20/20 paquetes ok, vet limpio. Certificación física sobre fuente real (episodio del owner, SHA `90ceeb9c…`, SPEC-01 420 frames/106 persistidos + SPEC-02 3 FRAME): `mke pipeline` COMPLETE 7 supported/0 non-supported, replay ×2 byte-idéntico en 9 artefactos, resume físico byte-idéntico, RequestJSON verificado en las 5 clases contractuales, provenance harness `TestV2PhysicalProvenanceTraceResolvesToSourceSHA` PASS (SKO→claims→evidencia→source→SHA). Limitación real: adapter recorded (sin credencial VLM por-corrida); smoke live queda como única deuda operacional, heredera del estándar V1. Artefactos: `~/mke/v2-shot3-cert-20260930/`.
- **2026-10-01 — Clutifx Chapter 01, primera extracción full real live (V2):** `CLUTIFX_CH01_EXTRACTION = BLOCKED`. Fuente `~/mke/course/ep01-intro.mp4` ("Episodio 1 - Introducción", SHA `4de8f12d4841c63022a03e7450e0b54c4947ed9c8fc8c408606dde79dd3d289b`, 34:03.9, 136.6 MB); MKE `cc13a121` intacto (`PRODUCT_CODE_CHANGED = NO`); provider live `openrouter`/`stealth/space-bunny-alpha` (probe 6/7). L0 COMPLETE del capítulo completo: ASR faster-whisper large-v3 (323 seg, es p=1.00, 97% habla, ligado al SHA), media 2044 frames inspeccionados/531 persistidos/0 unobserved, plan+acquire 1040/1040, 130 ventanas ×8 frames. L1 live FATAL determinista (exit 5) al commit de w0003: el contrato congelado S2-B-01 detectó `cl-chart-instrument-eurusd@1` propuesto por w0002 y w0003 con contenido divergente (statement + evidence_ids window-locales) — bloqueo estructural para escala full-chapter: la igualdad de contenido incluye evidencia local de ventana y los claim ids son slugs del modelo, por lo que todo hecho visual persistente re-proposto diverge ⇒ ClassFatal. 0 claims/relations/SKOs publicados; 56 claims + 4 relations quedaron como proposals no committeados en el journal (en ~19 claims/ventana ⇒ proyección ~2.600 provider calls para 130 ventanas, sobre el techo de budget 2400). Replay recorded del fatal: mismo error byte-idéntico. `REPLAY_CHECK` de outputs canónicos = NOT_AVAILABLE (nunca existieron). Finding adicional observado: statements mayoritariamente en inglés sobre fuente en español (el prompt congelado no fija idioma). Review Bundle persistido en `evaluations/clutifx/chapter-01/`; runtime local en `~/mke/clutifx-ch01-20260930/`. Espera decisión Owner + Primary Manager sobre el contrato de identidad L1 antes de cualquier reintento full-chapter.
- **2026-10-01 — identity remediation implementada + adversarial review FINDINGS:** sobre `cc13a121` se congeló el design `docs/v2/remediation/CLUTIFX-LONG-SOURCE-CLAIM-IDENTITY-REMEDIATION.md` (`ebe8cc7`, ladder de equivalencia: evidencia=soporte no contenido, normalización conservativa sin fusionar separadores interiores, adjudicador bounded `claims.equivalence_review` via `invokeV2`, ventana como unidad atómica, rechazo window-scoped no fatal, relations acumulan soporte sin adjudicar, regla idioma fuente con `mke.claims-recon.v1→v2`), implementación (`6914022`) y suite de regresión §14 (17 tests, `71b5a21`; ambos pusheados FF). Independent adversarial review (fresh context, 20 frentes A–T, worktree detached `~/mke/multimodal-knowledge-engine/wt`, harness propio de 19 tests scratch sin commit): baseline verificado (HEAD=origin=`71b5a21`, tree limpio, merge-base `cc13a121`), suites 20/20 ok + vet + build. Veredicto `IDENTITY_ADVERSARIAL_REVIEW = FINDINGS`: 0 CRITICAL / 0 MAJOR / 1 MINOR / 4 NOTE. MINOR (confirmado físicamente con probe): el contador `divergentCollisions` del run summary se incrementa dos veces por ventana rechazada (`resolveIdentityCollision` y `commitClaimCandidates` — `internal/pipeline/v2_stages.go`), sesgando 2× la métrica "divergent collisions" del live gate §15. NOTEs: false-positive EQUIVALENT mergea proposiciones distintas (autoridad dentro del contrato aprobado, con guardas deterministas kind/epistemic/relaciones y veredicto durable auditable); el parser acepta claves JSON duplicadas (last-wins de Go, pinned); `EVIDENCE_ACCUMULATED` se estampa también cuando la evidencia entrante es subconjunto del unión (auditoría cosmica); `equivalenceReviews` cuenta replays del journal, no sólo llamadas live. Propiedad fundamental probada: same proposition + soporte adicional ⇒ ACCUMULATE; proposición distinta ⇒ nunca merge (incl. reviewer deliberadamente equivocado: `EURUSD 20/30 pips` mergea por diseño aceptado). Atomicidad whole-window sin residuo en stages/records/edges con invocaciones de equivalencia durables, re-collision desde journal sin nueva llamada, crash/resume byte-idénticos, corrupción durable (payload y provenance) FATAL, scope limpio (sin go.mod/L0/L2/V1/D4). Test quality: 1 assertion vacua en el test de fingerprints (L1 sensitivity sólo indirecta) y 3 gaps de suite permanente (correctivo válido, budget-refused en correctivo, crash post-DIVERGENT) — todos cubiertos por el harness del review. `READY_FOR_MANAGER_ADJUDICATION = YES`; recomendación `READY_FOR_CLUTIFX_10_WINDOW_LIVE = YES` (corregir el contador antes de leer métricas del gate). Sin product fixes, sin live, sin cambios de diseño.

## 🧭 Decisiones

- `Course Intelligence Engine` solo alias histórico; nombre MKE generalista, POC video trading sin types de trading en core.
- ADR-001 A antes de C y C opcional, B no implementada por puntos ciegos visuales. No vender C por el trabajo invertido; recuperar conocimiento correcto incremental es la medida.
- GLM tras VLMProvider, Whisper tras ASRProvider; Qwen/M4/Kronos no bloquean M0 con backend aceptado. Modelo/endpoint/compatibilidad reales no presumidos.
- Product-first 00A, SQLite+FS cuando necesario 02; nada de infraestructura por anticipación.
- QA no auto-certificado, golden blind, replay ≠ live, no afirmaciones falsas de verdad humana/externa, JSONL canónico.
- Historial sintético anterior NO_GO conservado; recovery PASS sobre tres casos y holdout 6/6 no son certificación M0. Gate definitivo físico/spec basado en evidencia.
- Roadmap de oportunidades diferido y ya persistido, sin scope creep M0.
- V2: L0 reutiliza source/media/evidence; L1 son Grounded Claims atómicos; L2 son SKOs con provenance transitiva. `D4 = DEFERRED_TO_V3`; intent/questions, RAG/search, cross-source composition y SKO nesting quedan fuera.
- Para M0-R1, el golden existente se preserva hash-identical; corregir evaluación cross-language NO autoriza traducir/regenerar golden ni relajar valores/condiciones/negaciones/excepciones.
- Whisper/local ASR es ahora requisito operacional del Owner para cerrar M0-R1, pero sigue detrás de `ASRProvider`; este refinement no autoriza acoplar media/pipeline a Whisper ni crear routing/infra adicional.

## 🔗 Docs / Links

- **Punto de entrada para nuevo agente:** [[MKE — Handoff técnico y certificación M0]].
- **Historial V1/M0:** [[M0 Execution]].
- **V2 Design Pack:** repo `xKoRx/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, `docs/v2/` @ `618043e`.
- [Rama de código de continuidad](https://github.com/xKoRx/multimodal-knowledge-engine/tree/fix/m0-live-readiness) y [commit verificable `974f748`](https://github.com/xKoRx/multimodal-knowledge-engine/commit/974f74818d1a298497fff77e297f64b1dd327f61).
- [Arquitectura congelada](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/architecture/architecture.md); [SPEC-00A](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-00A-product-spike.md); [SPEC-04](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-04-integration-benchmark.md).
- [Runbook físico (leer erratas en recurso antes de usar)](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/runbooks/m0-live-certification.md).
- [Roadmap posterior](https://github.com/xKoRx/multimodal-knowledge-engine/blob/master/docs/roadmap/post-m0-opportunities.md).
- [[agents-os]], [[agents-os-bootstrap]], [[agents-os-agent-project-workflow]], [[agents-os-session-close]].

## 💡 Ideas diferidas

- Video-use, MarkItDown, Agent Reach, WeKnora, OpenMAIC/HyperFrames: solo experimentos futuros; ver roadmap. Postgres/MinIO/vector DB/cluster/Argus/otros modelos solo por evidencia de necesidad; sin desviar M0.
