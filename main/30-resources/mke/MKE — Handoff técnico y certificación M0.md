---
type: doc
schema_version: 1
status: active
project: "[[Multimodal Knowledge Engine]]"
related:
  - "[[M0 Execution]]"
tags:
  - kind/doc
  - area/personal
  - topic/mke
created: 2026-09-20
updated: 2026-09-20
---

# MKE — Handoff técnico y certificación M0

> [!important] LEER PRIMERO EN LA PRÓXIMA SESIÓN
> Fecha de corte: **2026-09-20**. El proyecto está **LIVE_READY_WITH_LIMITATIONS**; **M0 = BLOCKED físico / certificación real NO ejecutada**. Los reportes del agente hablan de tests sintéticos y HTTP simulado; NO hay evidencia de inferencia GLM real, comprensión multimodal de un video autorizado completo, ni aprobación de G0–G9. La frase del owner «listoooo» es petición de documentar/pausar, NO prueba de disponibilidad de video, transcript o credenciales. Reconfirmar recursos al retomar.
>
> **Autoridad de ejecución:** [[M0 Execution]] (planificador único de tareas). **Producto/decisiones:** [[Multimodal Knowledge Engine]]. **Contratos inmutables M0:** SPECs y arquitectura del repo. Esta nota es mapa de continuidad y evidencia, NO segundo planificador ni autorización para implementar M1/M2.

## 1. Identidad, misión y alcance

- Proyecto canónico: [[Multimodal Knowledge Engine]], alias histórico `Course Intelligence Engine`.
- Repo privado: `xKoRx/multimodal-knowledge-engine`. Repo de vault: `xKoRx/agents-os`, branch `master`.
- M0: video autorizado de curso de trading como PRIMER caso, fragmento de 5–10 min y después video entero de 1–2 h. Objetivo verdadero: `source → evidence → knowledge.jsonl → documentation.md` técnico, trazable, con procedimientos por paso, reglas, excepciones, valores y conflictos visibles. Curso, trading y video NO son dominio permanente del motor.
- M1, solo tras M0 PASS: varias fuentes/corpus → documentación incremental, cobertura, duplicados y procedencia. M2, después: inteligencia transversal y relaciones, no promesas de rentabilidad.
- Stack decidido M0: Go CLI monolítico, FFmpeg/ffprobe, SQLite + FS desde SPEC-02, `VLMProvider` y `ASRProvider` como fronteras externas, JSONL canónico y Markdown proyección. GLM-5.3-Flash es adaptador inicial de desarrollo; Qwen por Ollama/LM Studio y Whisper son candidatos locales NO certificados. M4 de noche / Kronos CPU como fallback son posibilidades operacionales, no contrato del core.

## 2. Baselines Git — NO CONFUNDIR

| Hito | Ref / SHA | Evidencia y sentido |
|---|---|---|
| Freeze M0 | `master` @ `e5f9e9757d0e42b00c831e57920174428397d3b5` al momento del freeze | arquitectura y seis SPECs congeladas. `master` puede haber avanzado; verificar HEAD real. |
| Implementación inicial | `m0-implementation` @ `77b8d6f21ca3496457c523840d62c9eb105f158e` | siete etapas implementadas, fallo sintético material y bloqueo físico. |
| Recovery sintético | `fix/m0-synthetic-recovery` @ `b48822d5a2be1c805bc8eff52457cea71a7d708e` | selección determinista, interpretación, hints de conflicto, evaluador v2; 3/3 benchmarks ejecutables con A PASS después de corregir respuestas grabadas. |
| Último handoff dev | `fix/m0-live-readiness` @ `974f74818d1a298497fff77e297f64b1dd327f61` | **último commit verificado vía GitHub**; seis commits sobre recovery, `mke windows`, E2E ruta integrada, holdout, HTTP simulado, runbook. No merge a `master` confirmado. |

**Reanudación obligatoria:** localizar repo real (workspace anterior reportado `~/mke/multimodal-knowledge-engine`, no asumir que existe semanas después); `git fetch`, verificar branch, HEAD, worktree, remotos y divergencia. Partir desde la rama de live readiness o de un merge posterior expresamente comprobado, NO desde `master` asumido ni desde el freeze original. No force-push, no merge automático ni overwrite de cambios ajenos.

## 3. Estado por fase — qué está y qué NO

- SPEC-00A: walking skeleton y recorded E2E desarrollados; criterio 8 (GLM **live** con fragmento autorizado y evidencia real) sigue `BLOCKED` según último informe.
- SPEC-00B: contratos/probe + adapters implementados y testeados con fakes. Qwen/Ollama/LM Studio/Whisper/M4/Kronos estaban BLOCKED por target; GLM HTTP simulada ≠ servicio remoto validado. Fallo de un target local NO bloquea M0 con VLM aceptado.
- SPEC-01: media/PTS exacto, ASR normalizado o transcript supplied, cobertura visual independiente, hash e índice, reportado PASS sobre fixtures.
- SPEC-02: cinco tipos `FRAME|REGION|COMPARE|SEQUENCE|FIND_CHANGE`, presupuesto, dedupe, SQLite/FS y crash/resume, reportado PASS.
- SPEC-03-A: reconstruction → integrity → grounding → consolidation/revalidation → JSONL/Markdown, PASS de replay. Fijar determinismo a orquestación y replay, NUNCA prometer LLM live determinista.
- SPEC-03-C: adaptive investigator como sólo generador de preguntas y typed EvidenceRequest que reingresa por pipeline A. Implementado; no justificar C sin conocimiento correcto incremental.
- SPEC-04: harness, golden, A/C, recovery/invalidation y QA desarrollados. **No existe certificación definitiva sobre video real.** Resultado sintético original NO_GO → recovery sintético 3/3 A PASS → holdout recorded 6/6, no generalizar a comprensión live.

La implementación no equivale a aceptación del producto. Los gates físicos se mantienen abiertos; NO marcar M0 PASS, DONE ni 100% del producto.

## 4. Secuencia ejecutable demostrada y laguna cerrada

El recovery anterior usaba `requests.json` y listas de ventanas escritos manualmente; `mke plan` NO formaba parte del benchmark. Live readiness agregó `mke windows` y probó E2E desde mp4 original:

```text
mke media VIDEO --transcript TRANSCRIPT --out MEDIA
    ↓
mke plan --media-run MEDIA --out requests.json
    ↓
mke acquire MEDIA --video VIDEO --requests requests.json --budget BUDGET
    ↓
mke windows --media-run MEDIA --out config-a.json
mke windows --media-run MEDIA --out config-c.json --adaptive
    ↓
mke pipeline MEDIA --video VIDEO --transcript TRANSCRIPT --config config-a.json --vlm glm --budget BUDGET --out RUN
    ↓
knowledge.jsonl + documentation.md + interpretation.jsonl + auditoría
```

El benchmark A/C debe reutilizar mismos source bytes/hash, transcript, índice, selección/evidencia inicial, modelo compartido, reconstruct/review/publisher; única diferencia prevista: toggle adaptativo y requests adicionales propios de C. Trazabilidad persistida: `requests.payload_json`/policy → `created_by_request_id` → ventana → knowledge evidence ref → source real PTS/hash. El nuevo E2E comprueba esta cadena, pero con provider recorded. **No invocar benchmark directamente sobre insumos manuales legados como si probara planner integrado.**

## 5. Resultados y causas raíz con límites

### Primera campaña (`77b8d6f`)

- 16/16 paquetes Go reportados verdes, QA separado por SPEC y cobertura reportada ≥95% en perfiles relevantes.
- Tres benchmarks sintéticos A tenían omisiones/contradicción no reconstruida. Cinco de ocho goldens sin transcript ligado al hash no eran ejecutables autónomamente (NO contar como aprobados).
- C: cero conocimiento correcto incremental en 3/3, con llamadas extra; no conservar por complejidad invertida.

### Recovery (`b48822d`)

- `digit-change`: requests manuales omitían el segundo de frontera; no era simplemente defecto de score/detector. `mke plan` cubre selección inicial y el fixture publica con PTS 1.0s.
- `red-flash` + `intake`: el script recorded propuso `kind:"event"` fuera de taxonomía `claim|concept|rule|parameter|observation`; validador rechazó toda ventana. Script corregido; `interpretation.jsonl` hace visibles evidencias no citadas. NO afirmar que GLM live ya produce el tipo correcto.
- Contradicciones: motor puede publicar una relación `CONTRADICTS` si la reconstrucción la propone; hints de diferencias de valor NO son relaciones respaldadas ni deciden verdad. Recovery corregido propone relación explícita.
- Evaluador original tenía falso positivo con token `not`: errata E-1, comparación v1/v2 preserva golden y decisiones v1 originales; v2 exige relación soportada. No ajustar un golden y medir sobre él como prueba independiente.
- Resultado informado: los tres benchmarks ejecutables pasan G2/G2v2/G3 con A; C aporta 0/3 incremental y cuesta más. Es evaluación sobre entradas recorded corregidas, NO generalización.

### Live readiness (`974f748`)

- Ruta planner integrada, `mke windows`, trace E2E y pruebas de contratos engine-side. `kind:event` ⇒ REJECTED auditable, INCOMPLETE, terminal inmutable; `Procedure` ordenado con evidencia por paso.
- Holdout de video sintético de 8 s con golden agente separado: 6 elementos, hash golden reportado `64446e4e…`, A 6/6. Responses recorded predeterminan semántica: prueba harness, NO comprensión de video por GLM.
- HTTP local simulado: imagen, auth 401/403 sin retry, 429/5xx, timeout, ausencia/redacción de secreto. NO prueba endpoint/modelo vivo.
- 16/16 paquetes verdes reportados; coverage específica del último sprint fue mixta (p. ej. `DeriveAndRenderConfig` 81.8% individual, carga DB cubierta vía E2E); no prometer 95% de cada función ni nueva certificación de toda cobertura sin medir.

## 6. Dependencias físicas y seguridad: única intervención owner real

- Video original **autorizado** y accesible al runtime (1–2 h ideal; primero fragmento de 5–10 min). Permisos/derechos suficientes, sin publicar el contenido privado.
- Transcript `mke.transcript.v1` con `source_sha256` EXACTO, texto y tiempos válidos; o ASR autorizado aceptado, comprobado contra fuente. Un video silencioso NO autoriza inventar narración; falta de transcript viable es bloqueo formal del contrato vigente.
- `MKE_GLM_API_KEY` configurada en entorno/secret store autorizado sin valor en vault/repo/log. Endpoint y model id reales verificados; la API de GLM debe demostrar soporte de imagen + structured output mediante llamada LIVE.
- `ffmpeg`, `ffprobe`, Go, espacio libre, rutas, permisos y presupuestos aptos para video completo.
- El owner puede decidir backend local Qwen/M4/Kronos/Whisper después, pero NO es un gate obligatorio del M0 si GLM funciona.

**Disponibilidad actual:** NO comprobada en este handoff. El usuario afirmó «listoooo» al pedir documentación; no entregó video, ruta, transcript, API key ni un run físico. Los nuevos agentes deben comprobarlo, sin solicitar información que ya se pueda descubrir de forma legítima en su entorno. Si falta algo, una petición única mínima, sin exponer secretos.

## 7. Runbook y cuatro erratas operativas abiertas

Runbook técnico publicado en repo: `docs/runbooks/m0-live-certification.md` en rama `fix/m0-live-readiness`. Fue verificado principalmente con `--help` + suites/fixtures, **NO ejecutado sobre video real**. Antes de invocarlo literalmente:

1. Verificar transcript real ligado al SHA o ruta ASR aceptada; el archivo `path/to/transcript.json` es PLACEHOLDER, no credencial/procedencia real.
2. Crear y validar `budget-a.json` y `budget-c.json` ANTES de `acquire`/`pipeline`. El runbook inicial menciona `path/to/budget.json` antes de crear sus ejemplos. A/C deben compartir una política de techo comparable; registrar costos reales aparte. C necesita límites de rondas/preguntas explícitos y puede no participar si 03-C no es viable.
3. Convertir probes de credencial/endpoints/espacio en fallos **fail-closed** (exit nonzero), no simples `echo MISSING`; comprobar códigos de salida de cada fase. `mkdir` de salida antes de terminar todo el preflight puede producir artefactos vacíos: reservar temporal y marcar preflight incompleto, nunca confundir con run iniciado.
4. Golden evaluator separado prepara y congela golden desde ORIGINAL **sin acceso a resultados de 00A, A o C**; aunque el runbook enumera 00A primero, ejecutar en contextos aislados o reordenar congelación primero. Verificar hash y timestamps de freeze antes de benchmark; no contaminar golden ni introducirlo en prompts.

Registrar estas erratas en la próxima sesión, repararlas como documentación/procedimiento con QA antes del primer run real; no reabrir arquitectura ni rediseñar motor. La secuencia de certificación completa debe cerrar SPEC-00A criterio 8 y SPEC-04 G0–G9 sobre VIDEO REAL. Si A falla G0–G9 ⇒ M0 no PASS aunque C acierte; C se descarta si agrega error/regresiones o no justifica costo. Preservar variantes y outputs.

## 8. Evidence map: qué persiste dónde y qué NO está archivado

| Dónde | Qué | Estado/limitación |
|---|---|---|
| GitHub code | repo `xKoRx/multimodal-knowledge-engine`, branch `fix/m0-live-readiness` `974f748...`, docs/specs frozen, README y `docs/runbooks/` | Commits/archivos verificables. Re-fetch SHA al retomar. |
| GitHub vault | [[Multimodal Knowledge Engine]], [[M0 Execution]], esta nota y el roadmap del repo `docs/roadmap/post-m0-opportunities.md` | Fuente de planes, producto y handoff; no acredita runtime. |
| Workstation anterior | `~/mke/evidence/04/`, `~/mke/evidence/live-readiness/`, `~/mke/multimodal-knowledge-engine/artifacts/` (rutas reportadas por el agente) | **NO archivadas/verificadas por esta sesión**. Artifacts gitignored; no asumir que están en clones futuros. |
| Repo fixtures | `testdata/holdout/`, fixtures versionados pertinentes | Comprobar `git ls-files`, hashes y existencia. Goldens/corridas en `artifacts/` pueden ser locales exclusivamente. |

Si el host o artifacts faltan en la nueva sesión, regenerar sólo con runbooks/fixtures versionados cuando sea posible; etiquetar los artefactos no recuperables como ausencia, nunca reconstruir hashes o resultados de memoria. El plan durable NO depende de que sobrevivan directorios temporales. No respaldar material privado ni secrets automáticamente en Git.

## 9. Protocolo exacto de reinicio para agentes nuevos

1. Bootstrap Agents-OS canónico. Leer en este orden: proyecto padre → [[M0 Execution]] (estado, tareas, última bitácora) → esta nota → repo `architecture.md`, SPEC-00A/04, runbook y roadmap. Solo después cargar otras SPECs según problema. No reconstruir arquitectura desde el chat.
2. Confirmar branch/HEAD/worktree remoto/local y todos los insumos; actualizar tabla de entrega en [[M0 Execution]] si cambió. Branch preferida `fix/m0-live-readiness @ 974f748...`; no asumir master al día.
3. Corregir las cuatro erratas **de runbook** de §7, ejecutar `go test ./... -count=1`, `go vet ./...`, preflight fail-closed (pruebas no ejecutadas aquí).
4. Si recursos siguen inaccesibles: `BLOCKED` físico con una sola petición agrupada; no ampliar M0, no ejecutar código aleatorio ni degradar objetivos.
5. Si recursos existen: obtener fuente/hash, transcript válido y límites; agente golden aislado desde ORIGINAL congelado antes de cualquier output visible; LIVE 00A; planner `media→plan→acquire→windows`; A y C según reglas; QA independiente G0–G9; reporte final source/commit/config/hash/tiempo/calidad/costo/artefactos.
6. Resultados permitidos: `M0_PASS`, `M0_NO_GO`, `M0_BLOCKED`, con razón y evidencia. Sólo `M0_PASS` autoriza planificar M1. QA separado y `AGENT_GOLDEN/AGENT_REVIEWED` no equivalen a verificación humana.
7. Actualizar planificador único y padre, historial, decisiones, pruebas, permisos, errores y fuente de evidencia. No cerrar automáticamente puente humano ni hacer merge no autorizado.

## 10. Continuación posterior — sin adelantar scope

Roadmap de exploración registrado en repo `docs/roadmap/post-m0-opportunities.md` (documento candidato, no SPEC): R0 certificación → R0-FIX basado en evidencia → R1 `video-use` VU-01 planning context compacto y VU-02 evidence timeline QA → M1 corpus y opcionales MarkItDown (documentos) y Agent Reach (fuentes autorizadas) → WeKnora consulta derivada → M2 inteligencia transversal → OpenMAIC/HyperFrames publicación opcional. No incorporar código/servicios por inspiración ni alterar JSONL como fuente de verdad.

## 11. Cierre de esta sesión

Se documentó handoff a petición del owner; **NO se ejecutó certificación real, QA físico nuevo ni merge**. La tarea puente de owner permanece abierta para revisar/retomar, y el subproyecto de agente conserva su historial. Esta pausa no es `project Done` ni borrado de blockers. Antes de afirmar que algo está listo para correr, ejecutar los preflights de §7 en un entorno efectivo.

### Enlaces directos

- [Código MKE](https://github.com/xKoRx/multimodal-knowledge-engine/tree/fix/m0-live-readiness)
- [Commit último dev](https://github.com/xKoRx/multimodal-knowledge-engine/commit/974f74818d1a298497fff77e297f64b1dd327f61)
- [Arquitectura](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/architecture/architecture.md)
- [SPEC-00A](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-00A-product-spike.md)
- [SPEC-04](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/specs/SPEC-04-integration-benchmark.md)
- [Runbook](https://github.com/xKoRx/multimodal-knowledge-engine/blob/fix/m0-live-readiness/docs/runbooks/m0-live-certification.md)
- [Roadmap oportunidades](https://github.com/xKoRx/multimodal-knowledge-engine/blob/master/docs/roadmap/post-m0-opportunities.md)
