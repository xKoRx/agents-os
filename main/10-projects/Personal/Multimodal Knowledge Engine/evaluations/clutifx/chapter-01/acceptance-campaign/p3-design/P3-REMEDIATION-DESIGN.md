# P3 — BOUNDED REMEDIATION DESIGN

**Entrada:** P2 adjudication (`../p2-adjudication/P2-ADJUDICATION.md`). Regla: corrección más pequeña que cierra el finding; KISS/YAGNI; cero arquitectura nueva (sin vector DB, RAG, graph DB, queue, event sourcing, ontology, semantic layer). Todas las superficies verificadas contra el código @ `ef53530`.

## Contrato de la remediación

- Branch: `feature/v2-layered-knowledge-model` (continuidad), FF sobre `ef53530`, commits pequeños con tests.
- Prompts: bump de versión contractual (`mke.claims-recon.v2 → v3`, `mke.claims-ground.v1 → v2`); los fingerprints ligados a adapter/model siguen automáticamente (S2-J-03).
- Guardas frozen intactas: ladder determinista (kind/epistemic/estructura), fail-closed DIVERGENT, atomicidad whole-window, exit codes, budget semantics. Ninguna política cambia.
- Suite completa verde + `go vet` + build antes de terminar. Tests primero sobre lo crítico (semántica de clasificación y reintentos), coverage ≥95% en paquetes tocados.

## R-B01 — Empty content retryable (BLOCKER)

**Archivo:** `internal/providers/openrouter/openrouter.go` (`parseChatResponse`).
**Cambio:** antes de `extractJSONObject`, si `strings.TrimSpace(content) == ""` → `providers.Error{Class: ClassRetryable, Op: "parse", Detail: "assistant content is empty"}` con el mismo rationale del caso hermano (200 sin choices: anomalía transiente del backend, repetible como misma operación lógica). El contenido PRESENTE pero no-JSON sigue **fatal** (malformed real, `extractJSONObject` intacto).
**Tests:** unit con fake transport: (1) vacío → 2º intento exitoso = VALIDATED con 1 retry; (2) vacío persistente → retry-exhausted (no fatal); (3) contenido malformado → fatal (regresión); (4) sin choices → retryable (regresión existente).

## R-B02 — Composition timeout por intento (BLOCKER)

**Archivos:** `internal/pipeline/v2.go` (config), `internal/pipeline/v2_sko_stages.go:70`.
**Cambio:** nuevo campo `CompositionTimeoutSeconds int64 json:"composition_timeout_seconds,omitempty"` en la config v2 (validación ≥0; omitempty ⇒ configs viejas válidas). Nuevo helper `compositionTimeoutSecondsV2()`: `Config.CompositionTimeoutSeconds` si >0, si no `ex.opts.Timeout` (el timeout del pipeline, 600s en el run canónico). Sólo la llamada de COMPOSITION (`v2_sko_stages.go:70`) usa el nuevo valor; composition review (`:296`), equivalence (`v2_stages.go:609`) y grounding review (`:1081`) siguen en `ReviewTimeoutSeconds` (120s es correcto para payloads chicos: 1048/1048 grounding OK).
**Tests:** decode de config con/sin campo; selección de timeout (field vs fallback); suite v2_sko existente verde. El reason durable `composition_unavailable` NO cambia.

## R-M03 — Bad evidence refs: prompt + validación (MAJOR)

**Archivo:** prompt de reconstruction en `internal/pipeline/v2_stages.go` (~831, se convierte en `mke.claims-recon.v3`).
**Cambio (hardening):** regla nueva: «`evidence_ids` debe contener ids exactos copiados de las listas de evidencia de esta ventana — nunca el formato con rango (`asr-NNNNN [start-end]`), nunca prefijos (`transcript asr-...`), nunca ids de otras ventanas». Motivo: el request muestra transcript como `transcript asr-00003 [34850-49400]: ...` y el modelo imitó ese formato.
**Corrective reissue (opcional-si-trivial):** si el patrón de correctivos de grounding se reutiliza con ≤~40 líneas en el loop de ventana: ante rechazo por unknown evidence ref, 1 reissue con el error de validación. Si no es trivial, queda sólo el hardening (P1 probó que el contenido semántico era correcto 4/4). Gate de P6: las 4 ventanas bad-ref (w0003, w0005, w0043, w0110) replayadas deben VALIDATED con refs válidas.

## R-M02 — Estabilidad de kind/epistemic (MAJOR)

**Archivo:** mismo prompt v3.
**Cambios:**
1. Definiciones operativas de kind con el patrón observado: `parameter` = valor/ajuste/metadata mostrada del gráfico o herramienta (símbolo del instrumento, temporalidad, niveles numéricos en pantalla); `observation` = algo que el video muestra ocurriendo (movimiento de precio, acción de dibujo, cambio de estado); `claim` = aserción de contenido de trading; `rule` = regla condicional; `procedure_step` = paso de proceso.
2. Regla de estabilidad: «Asigna kind por el CONTENIDO de la proposición, nunca por el contexto de la ventana: la misma proposición recibe siempre el mismo kind (p.ej. 'el instrumento mostrado es EURUSD' es siempre parameter)».
3. Regla de epistemic (hoy ausente del prompt): «INSTRUCTOR_SAID cuando el instructor verbaliza la proposición (aunque también sea visible); VIDEO_OBSERVED sólo cuando la evidencia es puramente visual sin contraparte hablada».
**Guardas frozen intactas:** el ladder sigue rechazando divergencias kind/epistemic — el fix reduce el ruido upstream, no afloja el guard.
**Tests:** los tests de prompt existentes (contract probes) ajustados a v3; suite de identidad verde sin cambios semánticos.

## R-M01 — Calidad de grounding: citación adyacente + calibración reviewer (MAJOR)

**Archivos:** prompt v3 (reconstruction) + `internal/claims/review.go` (grounding reviewer, se convierte en `mke.claims-ground.v2`).
**Cambios:**
1. Reconstruction: «Cita cada segmento de transcript necesario para resolver el statement: si usa deixis ('esto', 'ahí', 'el rango') o un antecedente/causa/continuación de un segmento adyacente, cita también ese segmento». Ataca los 48 EVIDENCE_SELECTION_PROBLEM.
2. Reviewer: (a) «No rechaces por desajuste entre el garble de ASR y el término canónico cuando la evidencia citada (frame/rótulo) muestra que son lo mismo» (ataca Turtle Soup/GIP); (b) «Resuelve la deixis desde el contexto citado» ; (c) atómico-vs-COMPOSITE: «COMPOSITE sólo cuando se afirman 2+ proposiciones que pueden variar independientemente en verdad; una proposición con su razón enunciada ('porque...') es ATOMIC» (cierra MI-01).
**Tests:** contract probes de review prompt; casos unit de clasificación que ejercen las guías nuevas (garble-equivalence, deixis, causal-atomic).

## R-M04 — Lectura visual de niveles (MAJOR)

**Archivo:** prompt v3.
**Cambio:** «Los niveles/objetivos/entradas/stops mostrados en pantalla se transcriben exactamente como están rotulados; nunca asignes a una proposición un nivel que la evidencia no muestra o no enuncia para ella».
**Tests:** contract probe del prompt; P6 verificará con los 4 claims WRONG replayados.

## R-MI04 — rejection_category en resume (MINOR)

**Dónde:** escritor de coverage/window-coverage (localizar en `internal/publish/` o pipeline; la categoría contractual original se sobrescribe con «rejected in a previous attempt» al re-validar en resume).
**Cambio:** preservar la categoría original de rechazo (identity divergence / bad evidence ref) en la re-validación cross-attempt; la historia de attempts queda en el journal como hoy.
**Tests:** resume test con ventana rechazada en attempt previo → categoría original preservada.

## Fuera de alcance (deuda documentada, sin cambio de producto)

- MI-03 dedup por statement normalizado (requiere design change del contrato de identidad por record_id).
- N-03 enriquecimiento de relations (Turtle Soup bajista huérfano).
- Contador `equivalenceReviews` que cuenta re-veredictos del journal (NOTE ya adjudicado).
- Rediseño L2 (paginación/catálogo): prohibido por B-02 sin evidencia; el timeout resuelve la causa medida.

## Gates de salida P4→P5

1. Suite completa + vet + build verdes; coverage ≥95% en paquetes tocados.
2. Red-green demostrado para R-B01 y R-B02.
3. Ningún cambio fuera de los archivos/superficies listados (scope check con `git diff --stat`).
4. Config canónica del rerun (P7) extendida con `composition_timeout_seconds: 600` y validada contra el schema.
