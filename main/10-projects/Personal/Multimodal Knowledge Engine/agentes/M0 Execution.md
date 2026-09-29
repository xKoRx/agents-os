---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Multimodal Knowledge Engine]]"
sprint:
start: 2026-09-17
due:
progress: 100
repo: xKoRx/multimodal-knowledge-engine
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/personal
created: "2026-09-17"
updated: "2026-09-29"
---

# M0 Execution

> [!important]+ Planificador único · cierre 2026-09-28
> **CERTIFICACIÓN FÍSICA ORIGINAL EJECUTADA: `M0_NO_GO`. WORKSTREAM ACTIVO: `M0-R1`.** La implementación base no se reabre. El pipeline real quedó probado; la remediación se concentra en grounding/evaluación y en completar ASR local con Whisper detrás de `ASRProvider`.
>
> Último HEAD remoto verificado del repo: `fix/m0-live-readiness @ 974f74818d1a298497fff77e297f64b1dd327f61`. El ejecutor anterior reportó cambios locales no commiteados (OpenRouter/runbook); inspeccionar HEAD/worktree reales antes de escribir. `progress: 100` sigue representando la campaña de implementación histórica, NO certificación M0 terminada.
>
> **Nuevo agente:** este archivo vuelve a ser el planificador único. No abras otro proyecto M0. Ejecuta M0-R1 con IMPLEMENT→TEST→QA, preserva source/golden/baseline, deja Whisper local operativo y termina sólo con `M0_R1_PASS | M0_R1_NO_GO | M0_R1_BLOCKED`.

## 🎯 Objetivo

Entregar M0: fuente original autorizada → adquisición audiovisual independiente y trazable → conocimiento estructurado revisado → Markdown técnico útil + benchmark A/C, con SPEC-00A E2E live y SPEC-04 G0–G9 sobre video REAL. Arquitectura/SPECs del repo son autoridad técnica; [[Multimodal Knowledge Engine]] autoridad de producto; esta nota es fuente ÚNICA de tareas y estado de ejecución. Los reports de recorded-provider son evidencia parcial, no final.

## 📊 Estado actual — lo más reciente prevalece

**2026-09-29 — M0-R1 SHOT 3 (REMEDIATION + ACCEPTANCE) COMPLETADO: `M0_R1_REMEDIATION_PASS_D4_DECISION_REQUIRED`, `SHOT3_REMEDIATION_ACCEPTANCE = PASS`.** Branch `fix/m0-live-readiness` @ `640d000` (8 commits sobre `dad3891`, pusheada; worktree limpio; 17/17 paquetes `go test ./... -count=1` + vet limpio; golden intacto `91c3dd57…` verificado). Remediación completa de los 8 MAJOR + 13 MINOR + NOTES mandatorios de Shot 2: C-01 (resume completa filas transport-failed, committed jamás reescrito), A-01/A-02/A-03 (statement como data de una línea; colisión transcript/evidence y blank text fallan cerrados en el índice), B-03 (parsers exigen exactamente un JSON), **cluster semántico**: MGR-01 cerrado por decisión owner del mandato (notes FUERA del juez; directivas any_of DENTRO como data), B-01 veredicto estructurado v2 `mke.semantic.v2`/`mke.sem02.v1` (7 componentes, aceptación = match AND todos; guard de negación determinista), B-02 description-value guard (números del Description ligan con variantes decimales), F-07 usage del evaluator en quality.json, F-08 matches canónicos, B-04 anchor por segmentos, B-05 truncation honesta, E-05 G8 computado (cost.json `within_declared_limits`), E-07 validación pre-gasto, E-01 firewall recursivo, E-02 escenario reviewer real vía seam `grounding_prompt_version`, E-04/F-10 runbook (`run_suites: true`, elección semantic explícita), D-01..D-06 ASR (validación deadlines, re-hash post-ASR, prechecks baratos, drop tras EOF, no-habla=exit 3 único). Acceptance adversarial independiente: 18 superficies atacadas, todas CLOSED, cero regresiones; 2 hardenings aplicados (`640d000`). 86 tests Shot 2 integrados (0 borrados). **D4_CHECKPOINT = CONTRACT_DECISION_REQUIRED**: 7/7 críticos sin single-record (evidencia en `~/mke/m0-shot3-20260929/D4-EVIDENCE.md`; probe `_d4probe`); el owner debe elegir: acreditar composición en el evaluador / consolidar reglas en el engine / aceptar limitación (G2 honesta en falla). **Recertificación G0–G9 NO ejecutada** (estado autorizante no alcanzado) — pendiente: (1) decisión D4 del owner, (2) `MKE_OPENROUTER_API_KEY` por-corrida + smoke semántico live (procedimiento en `~/mke/m0-shot3-20260929/SEMANTIC-LIVE-SMOKE.md`), (3) rerun completo (~5.2M tokens ref). Reporte: `~/mke/m0-shot3-20260929/SHOT3-REPORT.md`.

**2026-09-29 — M0-R1 SHOT 2 (REVISIÓN ADVERSARIAL INDEPENDIENTE) COMPLETADO: `M0_R1_SHOT2_REVIEW_PASS`, `READY_FOR_SHOT_3 = YES`.** Candidato `dad3891` revisado de cero por 6 superficies adversariales independientes (worktrees aislados, ~140 tests nuevos, evidencia física en vivo; golden intacto `91c3dd57…`; baseline 17/17 paquetes ok; sin cambios a código productivo). Resultado: **8 MAJOR + 13 MINOR + 12 NOTE, cero CRITICAL** — candidato NO derrocado. MAJOR: C-01 (resume tras transport-failure = fatal permanente; preexistente, prioridad 1), A-01 (inyección estructural vía statement multi-línea), A-02 (shadowing de evidencia por colisión de ids), E-04/E-05 (runbook no cierra G7 con su propio config; G8 PASS constante), B-01/B-02/MGR-01 (cluster evaluación semántica: 17 superficies FP con un solo voto del juez; `gold-entrada-miercoles-las-2` crítico sin pin numérico; **MGR-01 CONFIRMED** — Authoring.Notes verbatim al juez, flips demostrados en ambas direcciones, `any_of` nunca llega al juez: decisión owner de contrato). **D4 = CONTRACT_GAP**: 4/7 críticos pueden seguir sin acreditar (single-record semantics) ⇒ G2 puede mantenerse en falla ⇒ escalar a owner ANTES del rerun completo de Shot 3. Remediation set ordenado por dependencia en el reporte. Artefactos: `~/mke/m0-shot2-20260929/`. Whisper truth: user unit de `hermes-ops`, linger ON, loopback healthy (contradicción Ariadna/Shot 1 = contexto, no defecto).

**2026-09-29 — M0-R1 SHOT 1 (IMPLEMENTATION) COMPLETADO: `M0_R1_SHOT1_IMPLEMENTATION_PASS`.** Branch `fix/m0-live-readiness` @ `dad38913` (6 commits sobre la baseline de certificación `f522cbe`, worktree limpio, suites verdes, golden intacto — content hash `91c3dd57…` verificado antes/después). R1-01: el reviewer de grounding recibe el texto real de los segmentos citados (`mke.ground04.v1`). R1-03: un corrective reissue bounded con identidad defect-independiente, fail-closed preservado. R1-02: pase semántico cross-language opt-in del benchmark (`"semantic"` en config; determinista idéntico si se omite; valores con dígitos pineados a nivel plumbing; fail-closed por elemento). ASR: ruta operacional `mke media --asr whisper` vía `ASRProvider` con fixture canónico `<run>/transcript.json`, deadline policy (60s + 4x duración, single-attempt) y clamping errata-7; smoke físico PASS contra el runtime real (evidencia `~/mke/asr-smoke-20260929/`). R1-04: runbook con revisión 2026-09-29. Review adversarial independiente ejecutado: 3 MAJOR + menores corregidos en `dad38913`. PENDIENTE: Shot 2 (adversarial) y Shot 3 (recertificación G0–G9); la recertificación requiere rerun del engine completo (el cambio de prompt invalida grounding/consolidación/publicación); D4 (descomposición atómica) sigue FUERA de scope y puede mantener G2 en falla — decisión owner.

**2026-09-28 OVERRIDE CANÓNICO.** La pausa/BLOCKED físico de 2026-09-20 quedó superseded por ejecución real.

La certificación formal procesó el source autorizado completo y reportó 26/26 ventanas, 348 llamadas de modelo y ~5.2M tokens. Resultado: `M0_NO_GO`.

**Gates físicamente favorables:** G1 temporal integrity, G3 critical value correctness, G4 reference integrity y G8 budget semantics. QA reportó 10/10 afirmaciones soportadas honestas y cero alucinaciones publicadas como soportadas en la muestra; la multimodalidad visual se probó con información existente sólo en píxeles.

**Gates fallidos:** G2 con 7/7 reglas críticas del golden sin acreditar y G5 con 6 excepciones materiales ocultas. QA posterior encontró 0/7 realmente ausentes del material recuperado; al menos una estaba incluso soportada. Por tanto, no reabrir media/evidence acquisition como primera hipótesis.

**Findings M0-R1 aceptados:**
- R1-01: grounding reviewer no recibe suficiente texto de transcript; 0/147 audio-only soportados vs 65/176 con imagen.
- R1-02: golden español vs publicación mayormente inglesa rompe equivalencia lexical; preservar golden intacto y corregir evaluación semántica con checks estrictos de valores/condiciones/negaciones/excepciones.
- R1-03: ~15.7% verdicts de grounding malformados; mantener fail-closed y mejorar robustez sólo de forma bounded/auditable.
- R1-04: runbook/budget mostró erratas físicas; validar cada comando real, sin documentación teórica.

**Requirement nuevo del Owner:** Whisper/local ASR es obligatorio para cerrar M0-R1. Debe operar a través de `ASRProvider`, target primario Daedalus, sin acoplar dominio, sin routing framework y sin abrir infraestructura innecesaria.

**Evidencia local reportada:** certificación y QA bajo `~/mke/m0-20260928/`, course bajo `~/mke/course/`, wrappers SMB bajo `~/mke/smb/`. Revalidar existencia en host; no copiar secretos/material privado al vault.

## 🧱 Entrega de desarrollo

| Repo | Branch y HEAD de continuidad | Baseline/origen | SPEC funcional | SPEC técnica | Gate |
|---|---|---|---|---|---|
| `xKoRx/multimodal-knowledge-engine` | `fix/m0-live-readiness` @ `dad38913` (Shot 1 M0-R1 implementado y pusheado 2026-09-29, HEAD remoto verificado) | freeze `e5f9e9757d0e42b00c831e57920174428397d3b5` → implementación `77b8d6f21ca3496457c523840d62c9eb105f158e` → recovery `b48822d5a2be1c805bc8eff52457cea71a7d708e` → readiness `974f748` | padre + este planificador | `docs/architecture/architecture.md`, `docs/specs/SPEC-00A…04`, `docs/runbooks/m0-live-certification.md` | cert física `M0_NO_GO`; M0-R1 + Whisper local pendientes |

## ✅ Tareas

> [!note]+ Ownership
> La única tarea puente humana está en [[Multimodal Knowledge Engine]] con `[r]` Review, nunca Done por agente. Este bloque es planificador único del agente. **Las tareas históricas marcadas [x] significan implementación/QA sintética, no certificación del M0 físico.** Las tareas de certificación abiertas NO pueden ser cerradas por reports previos.

### Campaña de desarrollo y recovery — completada

- [x] SPEC-00A walking skeleton y recorded E2E, excepto criterio live 8 aún pendiente. #owner/agent #type/dev #area/personal ✅2026-09-17
- [x] SPEC-00B adapters y suite neutral de contratos; targets locales se documentaron BLOCKED por target. #owner/agent #type/dev #area/personal ✅2026-09-17
- [x] SPEC-01 media, SourceID/PTS/visual coverage/transcript en fixtures y QA. #owner/agent #type/dev #area/personal ✅2026-09-17
- [x] SPEC-02 requests tipadas, SQLite/FS, budgets, dedupe/resume/crash tests. #owner/agent #type/dev #area/personal ✅2026-09-17
- [x] SPEC-03-A baseline, grounding/consolidación/publicación reproducible mediante replay. #owner/agent #type/dev #area/personal ✅2026-09-17
- [x] SPEC-03-C investigador opcional; decisiones sobre valor real reservadas a SPEC-04. #owner/agent #type/dev #area/personal ✅2026-09-18
- [x] SPEC-04 harness y benchmark sintético, identificado NO_GO inicial y bloqueo físico (NO certificación). #owner/agent #type/dev #area/personal ✅2026-09-20
- [x] Recovery sintético: `mke plan`, `interpretation.jsonl`, conflict hints, evaluador v2; 3/3 A PASS con scripts corrected y QA reportado. #owner/agent #type/dev #area/personal ✅2026-09-20
- [x] Live-readiness: `mke windows`, integración E2E planner, holdout 6/6 recorded, HTTP fake, runbook; `LIVE_READY_WITH_LIMITATIONS`. #owner/agent #type/dev #area/personal ✅2026-09-20
- [x] Pausa documentada: padre, planificador, recursos y mapa de evidencia actualizados; ninguna certificación física fabricada. #owner/agent #type/admin #area/personal ✅2026-09-20

### M0-R1 — remediation + local runtime (workstream vigente)

- [x] Preflight: inspeccionar branch/HEAD/worktree/remotos y preservar cambios locales válidos antes de modificar. #owner/agent #type/admin #area/personal ✅2026-09-29 (HEAD limpio en `f522cbe`; commits posteriores a `974f748` eran trabajo legítimo publicado)
- [x] R1-01: corregir grounding audio-only para que el reviewer reciba la evidencia textual realmente citada; regression positiva/negativa + QA adversarial. #owner/agent #type/dev #area/personal ✅2026-09-29 (`3320221`)
- [x] R1-02: corregir evaluación cross-language sin tocar/regenerar el golden; equivalencia semántica estricta con números/condiciones/negaciones/excepciones protegidos. #owner/agent #type/dev #area/personal ✅2026-09-29 (`f0cbaee` + guardas `dad38913`)
- [x] R1-03: reducir verdicts malformados con mecanismo bounded/auditable, preservando fail-closed y sin normalización semántica silenciosa. #owner/agent #type/dev #area/personal ✅2026-09-29 (`b8a7df2` + identidad determinista `dad38913`)
- [x] R1-04: reconciliar runbook/budget contra ejecución real y dejar comandos físicamente verificados. #owner/agent #type/dev #area/personal ✅2026-09-29 (`ed4499a`; `mke media --asr whisper` y health endpoint verificados físicamente)
- [x] Whisper local: elegir backend mínimo correcto para Daedalus, exponerlo tras `ASRProvider`, probar fixture + audio real + timestamps/error/cancel, documentar exact model/runtime. #owner/agent #type/dev #area/personal ✅2026-09-29 (`6f9eeae`; prework Ariadna `WHISPER_DAEDALUS_PASS` + smoke físico del Shot sobre fragmento del source certificado, evidencia `~/mke/asr-smoke-20260929/`)
- [ ] Reusar/invalidate sólo etapas dependientes; preservar source identity, golden frozen y baseline anterior para comparación. #owner/agent #type/testing #area/personal
- [ ] Shot 2 adversarial sobre la candidate implementation y luego recertificación completa del mismo source bajo G0–G9, A primero; C sólo según ADR-001 y reglas SPEC-04. #owner/agent #type/testing #area/personal → Shot 2 ✅2026-09-29 (`M0_R1_SHOT2_REVIEW_PASS`); Shot 3 ✅2026-09-29 (remediación aplicada `640d000`, acceptance PASS; recert NO ejecutada: D4 + credencial pendientes)
- [ ] **DECISIÓN OWNER D4 (única decisión antes de la recert):** 7/7 críticos del golden son multi-cláusula y ningún record individual concentra su regla (evidencia `~/mke/m0-shot3-20260929/D4-EVIDENCE.md`). Elegir: (1) acreditar composición multi-record en el evaluador (con la misma disciplina de gates por record), (2) consolidar reglas en records únicos (cambio de engine), o (3) aceptar la limitación documentada (G2 termina en falla honesta). MGR-01 ya resuelto en Shot 3 (notes fuera del juez, decisión owner del mandato). #owner/me #type/supervision #area/personal
- [ ] Recertificación G0–G9 tras decisión D4: requiere `MKE_OPENROUTER_API_KEY` por-corrida + smoke semántico live primero (`~/mke/m0-shot3-20260929/SEMANTIC-LIVE-SMOKE.md`); rerun completo A-first (~5.2M tokens ref), invalidación grounding→evaluación por fingerprint, G7 vía `run_suites: true`, G8 computado. #owner/agent #type/testing #area/personal #blocked
- [ ] Persistir resultado `M0_R1_PASS|M0_R1_NO_GO|M0_R1_BLOCKED`, exact HEAD, delta de calidad/costo y estado Whisper; actualizar padre/Agents-OS. #owner/agent #type/admin #area/personal

### Certificación física original — completada 2026-09-28

- [x] Source autorizado + credencial VLM disponibles y corrida física completa ejecutada. ✅2026-09-28
- [x] Golden real congelado y benchmark/QA ejecutados; resultado formal `M0_NO_GO`. ✅2026-09-28
- [x] Root-cause refinement identificó R1-01..04; media/evidence foundation no se reabre sin nueva evidencia. ✅2026-09-28

## 📆 Bitácora

- **2026-09-17 — inicio/freeze:** Agents-OS bootstrap, subproyecto materializado y baseline `e5f9e97`, SPECs congeladas. Implementación 00A→04 con manager/implementer/QA separado. En historia Git figuran checkpoints SPEC (00A `e1cfdc6`, 00B `d33dd98`, 01 `b628ced`, 02 `1737e0a`, 03-A `97fa0e0`, 03-C `0479b3a`, 04 `77b8d6f`). El detalle histórico original de esta nota está disponible en Git; no confundir sus diagnósticos tentativos con causas raíz adjudicadas en recovery.
- **2026-09-20 — primer benchmark:** tres ejecutables de ocho goldens; event-2s y late-exception con omisiones críticas; contradicción con falso positivo evaluador; 5 goldens sin transcript auténtico. M0 NO_GO sintético inicial + BLOCKED físico, nunca PASS. Evidence local reportado `~/mke/evidence/04/`.
- **2026-09-20 — recovery:** `fix/m0-synthetic-recovery` @ `b48822d`, causas reales documentadas: requests de selección manuales omitían frontera, y script recorded inválido `kind:event` rechazaba ventana; correcciones `mke plan`, interpretation coverage, hints, errata E-1. 3/3 A PASS sintético con recorded responses corregidas; C 0/3 incremental. QA independiente reportó 8/8 PASS sintético, no físico.
- **2026-09-20 — live readiness:** `fix/m0-live-readiness` @ `974f748`, seis commits. Descubrió segunda laguna: `mke plan` no participaba en la ruta benchmark; añadido `mke windows` y E2E cadena integrada. Holdout nuevo golden separado 6/6 A recorded; HTTP fake sin GLM real; 16/16 paquetes reportados verdes. Runbook `docs/runbooks/m0-live-certification.md` publicado con erratas operativas posteriormente identificadas. Entrega `LIVE_READY_WITH_LIMITATIONS`, M0 BLOCKED físico; último QA de readiness fue adversarial durante sprint, no cert física.
- **2026-09-20 — pausa owner / HANDOFF COMPLETO DOCUMENTAL:** se documentan padre actualizado, este planificador, resource [[MKE — Handoff técnico y certificación M0]], tareas de certificación y no-go de scope. Owner retomará potencialmente en semanas sin fecha fija; `listoooo` no verificó recursos. No se ejecutó video real, no se constató existencia de artefactos locales fuera de Git ni se efectuó merge. Tarea puente debe seguir Review hasta decisión humana.

- **2026-09-28 — certificación real:** `M0_NO_GO` tras corrida completa. G1/G3/G4/G8 PASS; G2 7/7 critical omissions de acreditación y G5 6 excepciones ocultas. QA demostró que los 7 ítems estaban en el material recuperado.
- **2026-09-28 — M0-R1 autorizado:** Owner delega remediation acotada + local runtime completion. Whisper pasa a requisito operacional; golden/source/baseline deben preservarse y no se permite M1/M2 ni rediseño general.
- **2026-09-29 — M0-R1 Shot 1 implementado:** `fix/m0-live-readiness` @ `dad38913`, 6 commits (`3320221` R1-01 · `b8a7df2` R1-03 · `f0cbaee` R1-02 · `6f9eeae` ASR · `ed4499a` runbook · `dad38913` fixes del review adversarial). Golden verificado byte/hash-equivalente antes y después (`91c3dd57…` / file-SHA `ed3ba925…`). Suites completas verdes por paquete post-fix; go vet limpio. Smoke ASR físico: muestra 30.07s del source certificado (SHA derivado `38102ec7…`), 1 segmento `es` model `large-v3`, deadline policy impresa, fixture canónico válido, exit 0; evidencia en `~/mke/asr-smoke-20260929/`. Veredicto del Shot: `M0_R1_SHOT1_IMPLEMENTATION_PASS`, `READY_FOR_SHOT_2 = YES` (reporte completo en la sesión del agente). Limitaciones declaradas: D4 descomposición atómica fuera de scope; comportamiento live del modelo en el pase semántico pinado por prompt/contrato, prueba física en recertificación; runtime Whisper corre como proceso de `hermes-ops` (unit systemd inactive) — supervisión es asunto ops.

- **2026-09-29 — M0-R1 Shot 2 (revisión adversarial) completado:** `M0_R1_SHOT2_REVIEW_PASS`, `READY_FOR_SHOT_3 = YES` sobre `dad3891`. 6 superficies atacadas por subagentes independientes (worktrees aislados, ~140 tests adversariales, evidencia física en vivo): **8 MAJOR + 13 MINOR + 12 NOTE, cero CRITICAL**; candidato no derrocado. Top MAJOR: C-01 resume-tras-transport-failure fatal permanente (preexistente, prioridad 1), A-01 inyección estructural vía statement multi-línea, A-02 shadowing de evidencia por colisión de ids, E-04/E-05 runbook no cierra G7 con su propio config y G8 PASS constante, B-01/B-02/MGR-01 cluster semántico (17 FP con un solo voto del juez; `gold-entrada-miercoles-las-2` crítico sin pin numérico; MGR-01 CONFIRMED: Authoring.Notes verbatim al juez con flips demostrados, `any_of` nunca llega al juez — decisión owner). D4 = CONTRACT_GAP: 4/7 críticos pueden seguir sin acreditar y G2 en falla aun con todo corregido — escalar a owner ANTES del rerun. Golden intacto `91c3dd57…`; repo sin commits (tests = evidencia de Shot 3). Artefactos: `~/mke/m0-shot2-20260929/` (reporte consolidado + findings por superficie + tests + evidencia ASR). Whisper service truth: user unit de `hermes-ops`, linger ON, loopback healthy (contradicción Ariadna/Shot 1 cerrada como contexto).

- **2026-09-29 — M0-R1 Shot 3 completado:** `M0_R1_REMEDIATION_PASS_D4_DECISION_REQUIRED` @ `640d000` (8 commits, pusheado). Remediación íntegra de Shot 2 (8 MAJOR + 13 MINOR + mandatorios), acceptance adversarial independiente PASS (18 superficies, 0 abiertas, 0 regresiones), golden intacto, 86 tests Shot 2 integrados. D4 = CONTRACT_DECISION_REQUIRED con evidencia (7/7 críticos multi-cláusula sin single-record). Recert G0–G9 pendiente de: decisión D4 del owner + credencial OpenRouter por-corrida + smoke live. Artefactos: `~/mke/m0-shot3-20260929/`.

## 🧭 Decisiones

- Arquitectura/SPECs congeladas y repo técnico son autoridad, no replanificar el sistema por perder el chat. `MKE` generalista, M0 caso video trading.
- Planificador único esta nota; tareas efímeras del harness no sustituyen esta lista. Prohibido mantener un segundo plan persistente del mismo workstream.
- A obligatorio antes de C; C solo typed requests reutilizando pipeline A, sin retenerlo por complejidad. Falta prueba comparativa live.
- GLM bajo `VLMProvider`, Whisper bajo `ASRProvider`; Qwen/Ollama/LM Studio/M4/Kronos targets opcionales. No inventar acceso ni gastar sin autorización.
- JSONL canónico; Markdown proyección; provenance exacta; PTS real; evidence inspect/acquisition/interpretation son fases distintas; prompts live no probados.
- Golden source-first y ciego; `AGENT_GOLDEN` nunca `HUMAN_VERIFIED`. Tests/replay/HTTP fake no equivalen a M0 PASS ni a calidad física.
- Evitar infra no autorizada, nuevo frontend/RAG/M1/M2, cambios Echo/Forge/Hermes y cualquier merge o force push no autorizado.
- M0-R1 no cambia ADR-001: A debe pasar obligatorio antes de que C pueda aportar valor; C no puede rescatar baseline roto.
- Golden real permanece congelado/hash-identical; la corrección cross-language actúa en evaluación, no en la verdad de referencia.
- Whisper/local ASR es requisito del workstream por decisión del Owner, pero únicamente detrás de `ASRProvider`; no justificar coupling ni provider-routing framework.

## 🔗 Docs / Links

- **Reinicio obligatorio:** [[MKE — Handoff técnico y certificación M0]] (recursos: historial, pruebas, erratas runbook, seguridad y evidencia).
- Padre: [[Multimodal Knowledge Engine]].
- [Código, branch de continuidad](https://github.com/xKoRx/multimodal-knowledge-engine/tree/fix/m0-live-readiness) · [SHA `974f748`](https://github.com/xKoRx/multimodal-knowledge-engine/commit/974f74818d1a298497fff77e297f64b1dd327f61).
- [Arquitectura](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/architecture/architecture.md), [SPEC-00A](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-00A-product-spike.md), [SPEC-04](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-04-integration-benchmark.md).
- [Runbook (NO ejecutar literalmente sin cuatro erratas)](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/runbooks/m0-live-certification.md) · [Roadmap oportunidades](https://github.com/xKoRx/multimodal-knowledge-engine/blob/master/docs/roadmap/post-m0-opportunities.md).
- [[agents-os-agent-project-workflow]], [[agents-os-agent-run-register]], [[agents-os-session-close]].

## 💡 Ideas

- Ideas futuras se remiten al roadmap: experimentos video-use VU-01/VU-02 y luego M1/M2 bajo nuevo scope. No adoptar código ni nueva infraestructura mientras M0 esté BLOCKED.
