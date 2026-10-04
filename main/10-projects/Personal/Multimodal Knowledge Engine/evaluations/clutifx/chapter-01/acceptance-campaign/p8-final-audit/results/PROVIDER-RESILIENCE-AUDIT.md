# PROVIDER RESILIENCE AUDIT — P8 Final Audit

- **Run**: clutifx-ch01 rerun @ `19b44c1` (fix R-B02/F-1), runtime `~/mke/clutifx-ch01-rerun-20261003/`, run terminal `run-rerun/`
- **Journal**: `run-rerun/run.db` (provider_invocations 1618 filas, budget_ledger 4266 filas, pipeline_state, record_outcomes 1189, status_reasons 102 entradas); log `logs/run-rerun.log` (3 líneas, terminal INCOMPLETE exit 4)
- **Fecha de auditoría**: 2026-10-04 · Auditor: provider-resilience (P8)
- **Veredicto resumido**: **MANUAL_RESUMES_REQUIRED: 0 · RUN_FATALS (run-killing): 0**

---

## 1. Declaraciones contractuales

| Declaración | Valor |
|---|---|
| MANUAL_RESUMES_REQUIRED | **0** — el capítulo completo corrió sin intervención humana |
| RUN_FATALS (run-killing) | **0** — ningún evento de provider mató el proceso; el término fue el estado diseñado (exit 4 INCOMPLETE por 64 records non-supported) |
| Terminal | `mke: error [incomplete]: v2 pipeline is incomplete: 1125 supported, 64 non-supported records`, `EXIT_CODE=4`, escrito 2026-10-04T16:33:06Z |

## 2. Empty-content events (clase R-B01)

**Eventos en este run: 0.** Sweep exhaustivo (LIKE `%empty%`, `is empty`, `blank`) sobre TODAS las columnas de texto de TODAS las tablas del journal: **cero coincidencias**. No hubo ni un solo 200-con-contenido-vacío del backend en 1618 invocaciones.

- **R-B01 verificado en el build**: commit `6dec7e5` ("fix(providers): classify empty assistant content as retryable (R-B01)") es **ancestro de `19b44c1`** (verificado con `git merge-base --is-ancestor`). En `internal/providers/openrouter/openrouter.go` el contenido vacío se clasifica `ClassRetryable` (comentario in-source cita R-B01); tras agotar el presupuesto acotado emerge como `retry-exhausted` sin perder el run.
- **Advertencia honesta**: como la clase no ocurrió, el camino retryable de R-B01 **no se ejercitó en vivo** en este run. Su resiliencia queda probada por código + por la recurrencia documentada del run viejo (~1 fatal cada ~36–47 ventanas; este run tuvo 0 en 130 ventanas, consistente con transiencia), no por disparo en vivo.
- Verificación del contador: `vlm_call` ledger = 1618 filas; `vlm_token` = 1613 filas (las 5 fatals no generan usage); sin calls fantasma.

## 3. Parse-structured fatals — 5 records REVIEW_UNAVAILABLE

Los 5 con `error_class=fatal`, `error_detail = "vlm provider parse-structured [fatal]: assistant content is not a valid JSON object"`. **En los 5, `response_json` está VACÍO (0 bytes), `usage_json`/`model`/`response_id` vacíos: NO hay respuesta persistida** — se declara explícitamente. La adquisición de budget de cada fatal quedó `state=released` en `budget_ledger` (8 filas released = 5 calls + 6 image-units).

| # | Target | Intentos | at_utc (fatal) | Causa visible | Destino final |
|---|---|---|---|---|---|
| 1 | cl-eurusd-candle-gains-lower-wick | 1 | 13:59:16.504Z | no persistida | UNSUPPORTED_REVIEW_UNAVAILABLE (16:29:13Z) |
| 2 | cl-intraturtlesoup-open-pnl-label | 2 | 14:33:34.916Z | intento 1 = verdicto malformed addresses `@1@1` (14:33:34.837Z) → reissue correctivo → fatal | UNSUPPORTED_REVIEW_UNAVAILABLE (16:29:54Z), reasons: reviewer_unavailable + reviewer_malformed_output |
| 3 | cl-los-rangos-son-importantes-para-encontrar-entradas | 1 | 14:41:51.847Z | no persistida | UNSUPPORTED_REVIEW_UNAVAILABLE (16:30:06Z) |
| 4 | cl-marco-temporal-alternativo-30 | 1 | 14:46:59.482Z | no persistida | UNSUPPORTED_REVIEW_UNAVAILABLE (16:30:09Z) |
| 5 | cl-right-chart-switch-to-gbpusd | 1 | 15:33:12.806Z | no persistida | UNSUPPORTED_REVIEW_UNAVAILABLE (16:31:50Z) |

- (a) Intentos: 4 targets con 1 intento (fail-first), 1 target con 2 (malformed→reissue→fatal).
- (b) response_json de los intentos: **vacío en los 5 fatals** — no hay contenido del backend persistido, por lo que la causa raíz REAL del contenido no es adjudicable desde el journal (ver F-2, §7). El único intento con respuesta persistida del target #2 fue el intento 1 (JSON válido de 361 bytes rechazado por addressing `@1@1`).
- (c) **El run NO murió**: tras cada fatal el run siguió invocando (siguiente evento provider en minutos) y los 5 records quedaron **fail-closed** `UNSUPPORTED_REVIEW_UNAVAILABLE` en `record_outcomes` + `pipeline_state.status_reasons` (entradas [20],[23],[24],[25],[32]) + materializados así en `claims.jsonl` (5 menciones REVIEW_UNAVAILABLE).
- (d) **No hubo retry contractual para esta clase**: parse-structured es `ClassFatal` por diseño (`extractJSONObject` → fatal; el reissue correctivo existe sólo para la clase malformed-verdict). Es fail-first; el único reissue (#2) fue por su primer fallo malformed, no por el fatal.

## 4. Malformed verdicts

**236 eventos de rechazo de formato** (227 primeros intentos + 9 reissues re-rechazados) sobre 227 targets de `claims.grounding_review`. Todos son JSON bien formado que viola el contrato de salida. Subcausas (primer intento, examen directo de `response_json`):

| Subcausa | Instancias 1er intento | Descripción |
|---|---|---|
| **B — addressing `@1@1`** | **206** (199 solas + 7 con A) | el modelo devuelve `record_id` CON sufijo `@1`; el validador lo compone con la versión → `cl-X@1@1` vs target `cl-X@1` |
| **A — schema-id v2 vs want v1** | **26** (19 solas + 7 con B) | el modelo etiqueta la salida con `mke.claims-ground.v2` (la versión del prompt) en vez del schema de salida `v1` |
| **C — record-id drift** | 2 | el modelo "corrige"/typografea el id (`cl-precio-cierra-fuera-de-rango` vs target `...-rango`; `rel-elimacion-...` sin la "in") |

**Destino de los 227 targets**: 217 **recuperados** por el reissue correctivo contractual (2º intento con marcador `CORRECTIVE REISSUE` y restricciones explícitas de `record_id`/`version` — presente en 227/227 segundos intentos); 9 **re-rechazados** → fail-closed `UNSUPPORTED_INSUFFICIENT` con `reviewer_malformed_output` en reasons; 1 → el fatal del §3.

**Cobertura del "11 records"**: 10 records terminan el run con reasons malformed visibles (los 9 INSUFFICIENT: cl-entrada-posicion-corta-114697, cl-fecha-24-06-2025, cl-informacion-curso-intermedio-no-relevante, cl-observar-rangos-diario-es-facil, cl-operar-solo-grafico-diario, cl-rango-actual-toma-low-vela-anterior, cl-rango-bajista-completa-ordenes, cl-seleccion-vela-blanca-pequena, cl-smt-convierte-esto-en-rango; + cl-intraturtlesoup-open-pnl-label que termina REVIEW_UNAVAILABLE tras malformed→fatal). El 11º record con malformed verdict es **cl-precio-cierra-fuera-rango** (subcausa C, recuperado en reissue, sin reasons en el outcome). Total: **11 records produjeron algún verdict malformed; 10 quedaron fail-closed por ello.**

- **Fail-closed por record**: sí — cada uno de los 10 con reasons lleva su reasons_json propio; ningún record malformed contaminó a otro.
- **¿Alguna ventana se rechazó por esto? NO.** Las 19 ventanas re-chazadas en `status_reasons` ([0]–[18]) son por identity collision / divergencia determinística / evidence ref desconocida / relation id inestable — cero menciones a malformed. `record_stages` confirma 1189 PARSED + 38 EVIDENCE_ACCUMULATED sin estados de fallo.

## 5. Retry topology

| Task | Targets | Invocaciones | Targets con retry | Reintentos |
|---|---|---|---|---|
| claims.reconstruction | 130 | 130 | 0 | 0 |
| claims.equivalence_review | 71 | 71 | 0 | 0 |
| claims.grounding_review | 1189 | 1416 | **227** (19.1 % de targets) | 227 (todos exactamente 1 extra intento) |
| sko.composition | 1 | 1 | 0 | 0 |
| **Total** | 1391 | **1618** | 227 | 227 |

- **Contractualidad**: los 227 reintentos son **corrective reissues contractuales** (marcador `CORRECTIVE REISSUE` en el request del 2º intento, 227/227), disparados por rechazo del verdicto — no son retries de transporte.
- **Ratio**: 227/1618 = 14.0 % de las invocaciones fueron reissues; ningún target necesitó >2 intentos.
- Retries de transporte: **0 eventos** (presupuesto existente, nunca ejercitado; el run viejo muestra budget=2 para read-body).
- Distribución de 2º intento: 217 VALIDATED / 9 REJECTED / 1 fatal.

## 6. Run fatals, manual resumes, transporte y timing

**MANUAL_RESUMES_REQUIRED = 0.** Evidencia de proceso único, sin resume:

1. `budget_ledger` ids 1→4266 estrictamente monótonos en tiempo (**0 inversiones**) y con **0 gaps** tipo restart (mayor gap: 25.6 min en fase reconstruction, cadencia normal inter-ventanas; un resume dejaría re-adquisiciones tras hueco + re-ejecución).
2. **0 `invocation_id` duplicados**; intentos por target ≤ 2 en todo el run (el run viejo tiene el patrón resume: w0057 con 2 filas por (task,target)).
3. `effects`, `effect_log`, `reconciliation_log` = **0 filas** (sin re-adopción de efectos, que es lo que hace `allocatePipelineRunDirV2` en un resume).
4. Fingerprints únicos (3/3) en `pipeline_state`; status escrito una vez.
5. Birth times en disco: `run.db` nace 2026-10-03 22:48:02 local (= 2026-10-04T01:48:02Z, exactamente la 1ª fila del ledger); `run-rerun.log` nace 22:44:14 local (= 01:44:14Z); mtime del log = 16:33:06Z (línea terminal + EXIT_CODE=4). Host en UTC-3 (verificado con `date`). El ps del coordinador (un solo PID 2437524) es consistente con un único arranque; el proceso ya no existe (terminal 16:33Z ordenado).
6. Histograma horario de invocaciones sin hueco muerto: 01h→16h continuo (3,16,13,22,26,11,16,11,21,13,20,19,293,446,527,161).

**Wall clock por fase** (medido del journal; host local = UTC-3):

| Fase | Inicio (UTC) | Fin (UTC) | Duración |
|---|---|---|---|
| Lanzamiento → 1ª adquisición | 01:44:14 (birth log) | 01:48:02 (1ª fila ledger) | 3m48s setup |
| Reconstruction + equivalence (L1/L2 interleave) | 01:51:07 (1ª invocación) | 13:27:55 | 11h36m49s |
| Grounding review | 13:31:49 | 16:24:33 | 2h52m44s |
| Composition (1 call) | 16:24:36 (adquisición) | 16:28:27 (journaled REJECTED) | 3m51s in-flight |
| Materialización | 16:28:27.9 | 16:33:06.0 (terminal exit 4) | 4m38s |
| **Total unattended** | 01:44:14 | 16:33:06 | **14h48m52s (~14h49m)** |

Nota: los boundaries de fase informados por el coordinador (13:16Z) difieren ~12 min de los medidos (reconstruction termina 13:27:55Z, grounding inicia 13:31:49Z); valen los medidos del journal.

**Transporte/timing**: 0 timeouts, 0 errores de conexión, 0 read-body failures (los matches de "429"/"rate" en `request_json` son texto del prompt, no errores; `error_detail` sólo contiene la clase parse-structured en 5 filas).

**Totales de consumo (budget_ledger)**: **1618 vlm_calls** (1613 consumidos + 5 released por fatals) sobre el modelo `stealth/space-bunny-alpha`; **2.756 image-units** (2750 consumidos + 6 released); **12.045.055 vlm_tokens (~12.05M)** en 1613 calls con usage. Coincide con lo esperado (~1618 calls, ~12.05M tokens).

**Fin del run**: la composición SKO fue RECHAZADA por integridad de referencias (`object sko-range-chain-strategy component 0 references claim cl-estrategy-chain-of-ranges@1 which does not exist at that exact version` — status_reasons [37]); materialización fail-closed: `skos.jsonl` queda header-only con `sko_count: 0`; `claims.jsonl` 1190 líneas (header + 1189 records); terminal INCOMPLETE exit 4 con 1125 supported / 64 non-supported (49 INSUFFICIENT + 10 CONTRADICTED + 5 REVIEW_UNAVAILABLE). Todo ello es **estado terminal diseñado**, no crash.

## 7. Adjudicación de la deuda array-content (F-2)

**Veredicto: UNKNOWN para los 5 fatals de este run — y con una exclusión positiva.**

- **No hay evidencia directa**: en los 5 fatals `response_json` está vacío (0 bytes) y no hay usage/model/response_id. El adapter clasifica parse-structured como fatal y **no persiste el contenido ofensivo** en el journal (verificado también en el run viejo: su fatal `cl-rango-rectangular-vertical` 2026-10-02T05:08Z también tiene `response_json` de 0 bytes). No se infiere la causa sin evidencia.
- **Exclusión positiva (por código)**: `extract.go`/`openrouter.go` deserializan `choices[0].message.content` en un campo Go **string**. Si el backend hubiera enviado `content` como array JSON de parts, `json.Unmarshal` fallaría ANTES, con `ClassFatal Op "parse"` y detail `"response is not valid JSON"`. Los 5 fatals observados son **Op "parse-structured"** → el content llegó como string no vacío que falló `json.Valid` tras el slice de llaves. Es decir, los 5 fatals **NO son el caso "campo content como array"**.
- **Compatible con**: (i) array-of-parts **serializado como string** (`[{...},{...}]` → el slice primera-llave/última-llave produce JSON inválido), (ii) JSON object truncado, (iii) prosa sin objeto válido. Indistinguibles entre sí desde el journal.
- **Recomendación (no bloqueante)**: persistir en el journal el contenido ofensivo (o un resumen de forma: empieza-con `[`/`{`/otro, longitud, hash) cuando parse-structured falla; sin eso, F-2 no será adjudicable nunca en runs futuros.

## 8. Comparación old-vs-new

| Métrica | Run viejo (full-live-20261001) | Run nuevo (rerun @19b44c1) |
|---|---|---|
| Empty-content events | 2 — **run-killing** (w0057, w0093; `ClassFatal contractual`, exit 5) | **0** (clase reclasificada retryable por R-B01; ni siquiera ocurrió) |
| Manual resumes | **2** (resume #1 2026-10-01T23:14:18Z, resume #2; `resume-start.utc`, `resume2-start.utc`, `run-resume*.log` en disco) | **0** |
| Transport fatales | 1 — composition `read-body [retry-exhausted]: retry budget of 2 exhausted` (2026-10-02T06:05:23Z), mató la composición | **0** eventos de transporte |
| Parse-structured fatals | 1 (cl-rango-rectangular-vertical, fail-closed por record) | 5 — todos fail-closed por record, 0 run-killing |
| Malformed verdicts fail-closed | — | 10 records (+1 recuperado) |
| Resultado | Requirió babysitting (2 resumes) | **14h49m unattended, 0 resumes, término diseñado** |

## 9. Veredicto para el gate de escala

**GATE: PASS.** «Normal transient provider failures no requieren babysitting» se cumple con evidencia directa:

- 14h48m52s de muro, 1618 calls, 3 tareas provider, **0 intervenciones humanas**, 0 procesos extra, término por diseño (exit 4 INCOMPLETE con salida durable parcial).
- Las fallas transientes de provider (empty-content, transporte) fueron eliminadas como clase run-killing: R-B01 retryable en el build (nunca ocurrió) y 0 eventos de transporte.
- La única clase de provider que aún pierde unidades es **parse-structured fatal (5/1189 = 0.42 % de los records)**: fail-closed por record, no mata la ventana ni el run. El mecanismo de reissue correctivo ya existente para malformed-verdict recuperó 217/227 targets; extender un reissue acotado a parse-fatal (con el contenido ofensivo persistido para adjudicar F-2) es la palanca siguiente si el gate exigiera 0 REVIEW_UNAVAILABLE. No es bloqueante para escalar.

Riesgos menores documentados: (i) el camino retryable de R-B01 no se ejercitó en vivo en este run (0 ocurrencias); (ii) el subcause A (schema v2/want v1) persiste en 26 primeros intentos y causó los 9 fail-closed dobles — un ajuste de prompt/parser (aceptar v2 o endurecer la instrucción) lo reduciría; (iii) el subcause B (206 primeros intentos) es ruido contractual dominante que el reissue absorbe, pero cuesta ~1 call extra por record.

---

## FEEDBACK (Agents-OS)

1. **Skill tool no disponible en subagentes**: el bootstrap obligatorio (`agents-os-bootstrap`) no pudo invocarse vía Skill tool desde este subagente ("Skill is not allowed for subagent"); se cumplió leyendo el SKILL.md directamente. Sugerencia: documentar en el bootstrap (o en la constitución, regla 2) un **modo degradado explícito para subagentes/sesiones automatizadas** (leer constitución + perfil + continuidad, saltar routing de entidad, declarar la omisión), en vez de dejar el cumplimiento a criterio del agente.
2. **El gate de dominio funcionó bien por defecto**: la tarea apunta a un proyecto externo (`~/mke/...`, fuera de VAULT_ROOT) y el DEFAULT sin router fue la ruta correcta; no hizo falta escanear `30-resources/agents/domain-router-registry.md` para saberlo. Sería útil una fila de orientación en el bootstrap: "tarea sobre runtime externo con path absoluto fuera del vault → DEFAULT, sin entity retrieval".
3. **Cierre de sesión**: la instrucción de la orquestación (ONE-SHOT, cerrar sesión al terminar, feedback al final del summary) coincide con el contrato de `agents-os-session-close`; no hubo que inventar nada. Sin conflictos detectados entre AGENTS.md y tareas de auditoría one-shot.
