---
type: doc
schema_version: 1
status: active
scope: project
project: "[[AGENTS OS]]"
area: "[[Personal]]"
created: 2026-09-13
updated: 2026-09-13
description: P2-B Context Budget Implementer — nota de implementación de la tool context-budget; decisiones tomadas, evidencia de verificación (spec sección 6), resultados de la suite ejecutada y limitaciones operativas.
aliases:
  - p2-implementation-notes
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
---

# P2 — Notas de implementación de `80-agents/tools/context-budget/` (P2-B)

- Implementación de la tool definida por [[80-agents/tools/context-budget/artifacts/p2-context-budget-design.md|p2-context-budget-design]] (P2-A) y [[80-agents/tools/context-budget/artifacts/p2-context-budget-spec.md|p2-context-budget-spec]] (parent, A1-A9). Write scope respetado: `context_budget.py`, `selftest.py`, `README.md`, `results/run-<timestamp>.json` y esta nota; ningún otro archivo del vault fue creado, modificado ni eliminado (verificado con `git status --porcelain` antes y después; ver sección 6).

## 1. Archivos entregados y decisiones principales

- `context_budget.py` (entrypoint único, Python 3.9+ stdlib only, determinista, read-only salvo `results/`): reutiliza el harness como librería — `load_harness()` resuelve `80-agents/tools/conformance-harness` relativo a VAULT_ROOT en runtime (`sys.path.insert`, sin paths absolutos persistidos; constitución regla 11) y bindea `rules`/`agents_os_conformance` como globales del módulo, de modo que toda decisión de carga sale de `rules.Session` (cold_start/warm_turn/retrieve/open_delta/swap_entity/route_specialist/holds_two_packs/gate_note); ningún segundo modelo cold/warm/switch existe aquí (fork de `rules.py` prohibido y evitado).
- CLI implementada: `--vault-root`, `--json` (JSON a stdout, resumen a stderr), `--scenario <ID>` (dirigido por el operador, sin gate; acepta `RULES-FIDELITY-ANCHORS`), `--live` (habilita CTX-14), más `--conformance-json` opcional del diseño sección 10. Exit codes 0 (sin FAIL) / 1 (FAIL o pre-flight en rojo) / 2 (sin VAULT_ROOT o escenario desconocido). Ejecución: `python3 80-agents/tools/context-budget/context_budget.py [--json]`.
- Orden de ejecución implementado según spec sección 3: pre-flight `RULES-FIDELITY-ANCHORS` (reutilizado del harness, no re-implementado) → CTX-15 baseline → CTX-01/02/03 cold → CTX-04/05/06 warm → CTX-07/08/09/10 switch → CTX-11 → CTX-12 → CTX-13 → CTX-14. FAIL del pre-flight ⇒ todos los CTX en SKIP motivado ("transcripción obsoleta"); FAIL de un CTX no corta los demás; marker ausente o harness no disponible ⇒ SKIP motivado de todo.
- Etiquetado: único campo de estimación `estimated_tokens` = chars//4 vía `harness._size` en el run (jamás hardcodeado; jamás un campo llamado `tokens` — verificado mecánicamente en el selftest T6); `bytes`/`chars` son EXACT; la nota "chars/4, sin tokenizador de autoridad (C04)" viaja en la autoridad de cada métrica estimada y en la línea de baseline del resumen (A9).
- A1 (M18): los techos blandos del bootstrap ("Token Targets (soft)": "Cold base 3–6k tokens; warm delta <1k; entity swap 1-3k") y doctor Check 11 se comparan vía `_soft_target()`; la desviación degrada PASS→WARN con la cifra y su motivo, jamás a FAIL.
- A2/A3/A8: clasificación de dominio `classify_file()` según diseño 8.1 — (a) frontmatter `area` vía `rules.domain_from_area`; (b) membresía en `rules.ROUTERS`/`ROUTER_PREFS`/`DOMAIN_GATED_SKILLS`; (c) coincidencia de exclusividad en AMBOS registros reutilizando `_parse_index_tables`/`_row_name`/`_classify_index_use` del harness (desacuerdo → INFERRED/WARN por DUAL-REGISTRY); (d) bajo `30-resources/aranea/`; (e) neutral. La nota VPN es meli por membresía (autorizada, Minimal Read 3) y su aparición en escenario aranea sería WARN (A3); las transversales son neutrales (A8).
- A4 (M14): detector propio `find_duplication()` — normalización minúsculas/whitespace/puntuación, runs contiguos no solapados ≥5 tokens (acota falsos positivos de stopwords), condición de hit: ≥120 chars acumulados o un bloque que abarque ≥3 líneas consecutivas normalizadas; frontmatter excluido (metadatos estructurales del schema-contract, no contenido de la regla 5); `thresholds` completo registrado en cada record; veredicto máximo WARN.
- A5 (CTX-14): SKIP por defecto; con `--live` reutiliza la MISMA `read_surface_configs()` del harness (sin reimplementación); registra el dato names-only y jamás es criterio de FAIL (Hallazgos 4/17). No se ejecutó `--live` en esta misión (indicación del parent); la ruta de código queda verificada por inspección y por el SKIP por defecto.
- A6/A7: unidad de cuenta = archivo completo (paridad con harness); `30-resources/aranea/00-index.md` y recursos on-demand no se cobran al pack base (sólo si el escenario los abre; no ocurre en ningún fixture).
- Residuo post-swap (diseño 8.3): `potential_residual_files/_estimated_tokens` (peso en disco del pack saliente, INFERRED, Hallazgo 8) + verificación EXACT de que el modelo deja de sostener el pack (M11) y no lo re-abre tras el swap; el residuo real en la ventana del modelo se declara UNOBSERVABLE.
- Counterfactual de CTX-11 ("leak evitado"): notas de memoria bloqueadas SOLO por el chequeo de dominio de `rules.trigger_fires` y que referencian a la entidad activa por `entities`/`project`/`application` (reutiliza `rules.references_entity`) — sin el gate habrían entrado por los triggers de referencia; las `when_area_loaded` cruzadas siguen excluidas por desigualdad de área. Se reporta como cota superior INFERRED con su chars/estimated_tokens.
- Escenario dirigido (`--scenario`): incluye el resultado del pre-flight en el record (paridad con el harness) pero no aplica gate.

## 2. Evidencia de verificación (requisitos del spec sección 6)

- (1) Caso normal: suite completa ejecutada sobre el vault real — `python3 80-agents/tools/context-budget/context_budget.py --json` — exit 0, counts `PASS 7 · FAIL 0 · WARN 7 · SKIP 1` (detalle por CTX en sección 3); `fidelity_gate PASS` (26 anclas verificadas); `git_head` resuelto en VAULT_ROOT.
- (2) Caso negativo (inyección controlada, sin rastro en el vault): `selftest.py` T1 construye un vault temporal, sustituye `_session_for` por un `CrossPackSession` (saboteador que carga el router + prefs aranea dentro de un cold start meli) y demuestra que CTX-02 pasa de PASS/WARN (control limpio) a FAIL con evidencia "carga prohibida detectada" y el listado del pack cruzado; la restauración del punto de inyección deja el control limpio otra vez (T1c). Todo en tempfile del sistema; el vault canónico no se tocó.
- (3) Input malformado: perfil con bytes binarios ilegibles y perfil ausente (T2) → 14-15 CTX en SKIP con motivo ("no ejecutable: RuntimeError: cold set broken: no unique always-load note...") o PASS en los escenarios estáticos que no requieren sesión; ningún traceback aborta el run (los escenarios corren bajo try/except con SKIP honesto, misma política del harness).
- (4) Comportamiento SKIP: marker ausente (T4: todos los CTX SKIP citando el marker), pre-flight en rojo simulado (T3: bootstrap SKILL.md truncado en el fixture → `fidelity_gate FAIL` → 15/15 CTX SKIP con motivo de gate), CTX-14 sin `--live` (SKIP "la parte de configs de máquina se omite por defecto"), y harness no disponible → SKIP con motivo (verificado en los fixtures sin enlace al harness).
- (5) Determinismo: dos runs consecutivos completos sobre el vault real (T5 del selftest y par final de esta misión, runs `run-20260913-042944.json` / `run-20260913-042945.json`) producen records idénticos salvo `run`/timestamp y `results_file` (comparación JSON normalizada: True).
- (6) Baseline explícito: `git_head` resuelto vía `harness.git_head(VAULT_ROOT)` en cada run (`3a841154056a3fe802cf863d02dc99f08d1f67c3` en el run final A); las cifras del baseline salen SIEMPRE de `_size` en el run (el always-load midió 7025 estimated_tokens live, frente al ≈7108 informativo del diseño: drift real del corpus, no hardcode). El record CTX-15 incluye además un cross-check contra `context_baseline` del harness (misma fuente `_size`): coincidencia exacta de agregados (always=7025, meli=2017, aranea=1197).
- (7) No mutación canónica: `git status --porcelain` inicial vacío; al cierre, sólo aparecen los archivos del write scope (los commits "sync" minutales del repositorio son un proceso externo de la máquina del owner, fuera del alcance de esta tool; la tool no ejecuta git).
- Selftest completo: 11/11 PASS (T1a/T1b/T1c inyección, T2.corrupt, T2.missing-profile, T3 pre-flight rojo, T4 marker, T5 determinismo, T6 etiquetado, T7a exit 2, T7b suite temporal exit 0) — comando: `python3 80-agents/tools/context-budget/selftest.py`.

## 3. Resultados finales de la suite (run-20260913-042944.json, git_head 3a841154…)

- Counts: `PASS 7 · FAIL 0 · WARN 7 · SKIP 1`; exit 0. Fidelity gate: PASS. La nota de la unidad: todos los estimated_tokens son chars/4 (C04), bytes/chars son EXACT.
- CTX-15 PASS — baseline: always_load 4 archivos / 28436 bytes / 28105 chars / 7025 estimated_tokens; pack meli 3 archivos / 8148 bytes / 8076 chars / 2017 estimated_tokens; pack aranea 2 archivos / 4821 bytes / 4788 chars / 1197 estimated_tokens.
- CTX-01 WARN (cold DEFAULT): set = exactamente los 4 always; cold = 7025 estimated_tokens; unrelated-domain 0; WARN heredado Hallazgo 6 (cláusula de superficie) + WARN A1/M18 (cold base 7025 > techo blando 6k).
- CTX-02 WARN (cold MELI): base 4 + router meli-agent-dev + 2 prefs; cold total = 9042 estimated_tokens (base 7025 + pack 2017); unrelated-domain 0; expert aranea ausente; memoria interna activa Meli = ninguna (Hallazgo 10, estado observado); WARN A1/M18 (base > 6k).
- CTX-03 WARN (cold ARANEA): base 4 + router aranea-agent-dev + aranea ops prefs; cold total = 8222 estimated_tokens; expert no cobrada (Minimal Read 4); unrelated-domain 0; WARN heredado Hallazgo 7 (nota VPN) + WARN A1/M18 (base > 6k).
- CTX-04 PASS (warm DEFAULT): warm_delta_files = 0, warm_delta = 0 estimated_tokens (cero opens, delta puro).
- CTX-05 PASS (warm MELI + BOOTSTRAP-NOT-RERUN-ON-WARM): delta = 1 archivo (known-error fury segment suffix) = 634 estimated_tokens; base y pack intactos en turnos 2..5; bootstrap_runs = 1.
- CTX-06 PASS (warm ARANEA): delta = 1 archivo (continuidad MT5 parser cert) = 829 estimated_tokens; base intacta; sin memoria Meli en el turno.
- CTX-07 PASS (swap MELI→ARANEA): swap_turn = 1197 estimated_tokens (pack aranea completo); active_pack_count_post_swap = 1; base sin relectura; potential_residual (pack meli) = 2017 estimated_tokens (INFERRED, Hallazgo 8); M15 post-swap 0 unrelated.
- CTX-08 WARN (swap ARANEA→MELI): swap_turn = 4820 estimated_tokens (router + 2 prefs + signals-code-review vía tabla del router); expert ausente; active_pack_count_post_swap = 1; potential_residual (pack aranea) = 1197 estimated_tokens; WARN A1/M18 (swap > techo blando 3k — el especialista rut-eado empuja el turno por encima del rango; dato, no violación).
- CTX-09 WARN (DEFAULT→MELI): swap_turn = 2017 estimated_tokens; base intacta; bootstrap_runs = 1; WARN heredado de modo ambiguo (C02/C07).
- CTX-10 WARN (DEFAULT→ARANEA): swap_turn = 1197 estimated_tokens; mapeo [[Echo]]→aranea verificado explícitamente; WARN heredado de modo ambiguo.
- CTX-11 PASS (leak unrelated-domain): 0 archivos del dominio ajeno en los sets cargados de ambas corridas (meli y aranea); pool de "leak evitado" = 0 notas (ninguna nota del dominio ajeno referencia a RIO ni a Echo Forge hoy — el chequeo de dominio no está filtrando nada que el matching de entidad dejaría pasar).
- CTX-12 PASS (deprecated hot-path): escenario heredado en PASS (archive superseded fuera de stack y retrieval, cuádruple de retiro completo) + barrido M16 estático sobre 10 archivos del hot path: 0 hits; deprecated_hot_path = 0 estimated_tokens. (N1, corregido 2026-09-13: esta nota decía "11" por error; el run citado barría 10 — 4 always + 2 routers + expert + 2 prefs meli + 1 pref aranea. Tras el ciclo de corrección 1 el barrido incluye el set completo de especialistas y el set pasa a 14 archivos; ver sección 6.)
- CTX-13 WARN (duplicación): 2 pares ≥ umbral A4 — (a) agent-constitution.md ↔ rjara-agent-profile.md: 144 chars normalizados (regla de versiones `X.Y.Z` desde `master`: constitución regla 14 vs perfil `[DURA]` — el caso real previsto por el diseño); (b) INDEX.md ↔ 30-resources/agents/00-index.md: 2356 chars (pareja de registros ya vigilada por DUAL-REGISTRY-DOMAIN-SYNC del harness); total 2500 chars / 625 estimated_tokens duplicados en hot path; veredicto máximo WARN (A4).
- CTX-14 SKIP (sin `--live`, A5): "la parte de configs de máquina se omite por defecto".

## 4. Hallazgos sobre AGENTS OS registrados (sólo registrar, no corregir)

- El always-load (base 4) mide 7025 estimated_tokens (chars/4), por encima del techo blando declarado "cold base 3–6k" (bootstrap Token Targets; doctor Check 11) — WARN A1/M18 en CTX-01/02/03. Puede ser drift real del corpus (INDEX.md crece) o desviación de la métrica chars/4 respecto del conteo que inspiró el rango; C04 impide afirmar cuál.
- El swap ARANEA→MELI con tarea de code review mide 4820 estimated_tokens (router + 2 prefs + signals-code-review), por encima del techo blando "entity swap 1-3k" — WARN A1/M18 en CTX-08. El contrato obliga a cobrar router + prefs + especialista en un mismo turno; el rango blando no contempla explícitamente el caso con especialista (tensión registrada, no resuelta).
- Duplicación textual real en hot path DEFAULT: la regla de versiones productivas `X.Y.Z` aparece formulada tres veces (constitución regla 14, perfil `[DURA]`, prefs meli); el detector A4 la captura constitución↔perfil (144 chars normalizados); el par perfil↔prefs no supera el umbral (paráfrasis más corta) — límite mecánico declarado del detector.
- La pareja INDEX.md ↔ 30-resources/agents/00-index.md comparte 2356 chars normalizados (filas y descripciones de skills repetidas entre registros); ya estaba vigilada por DUAL-REGISTRY-DOMAIN-SYNC del harness — el presupuesto la cuantifica: ~589 estimated_tokens duplicados co-cargables vía INDEX (el índice federado no se carga sin necesidad de routing, paso 3).
- Sin hallazgos nuevos de unrelated-domain (0 en todos los sets) ni de deprecated en hot path (0 hits): el aislamiento de dominio del modelo transcrita y el estado del corpus pasan limpio hoy.
- El repositorio tiene un proceso externo de commits "sync" minutales (observado 03:54–04:13): cambia `git_head` entre runs separados por minutos; no afecta la reproducibilidad de las cifras (medidas de disco) ni el determinismo de los records dentro del mismo segundo de ejecución.

## 5. Limitaciones operativas

- `estimated_tokens` es chars/4 (C04): las comparaciones contra los techos blandos heredan su imprecisión; una desviación WARN es un smell-test, no una medición de tokens reales.
- CTX-14 no se ejecutó con `--live` en esta misión (indicación del parent): la ruta de lectura de configs queda verificada por reuso directo de `harness.read_surface_configs` y por el SKIP por defecto; la exposición de una sesión viva sigue UNOBSERVABLE (Hallazgos 4/17).
- M14 no detecta paráfrasis y su umbral es self-declared (A4): cambiar `min_run_tokens`/`min_chars`/`strip_frontmatter` rompe la comparabilidad entre versiones de la tool; la versión vive en `thresholds` del record.
- La clasificación M15 cubre lo declarado (frontmatter, membresías, ambos registros, carpeta aranea): contenido de dominio sin marcador (Hallazgo 9) no es detectable; archivos clasificados ambiguos degradan a WARN, nunca a FAIL.
- El hot path de M16 cubre los sets fijos (always + packs + especialistas `rules.DOMAIN_GATED_SKILLS` completo, desde el ciclo de corrección 1; antes sólo la expert aranea); el barrido del corpus completo de memoria vive en los checks L0 del harness y en el doctor, no aquí.
- Los commits "sync" externos pueden hacer variar `git_head` entre runs separados en el tiempo; dentro de la misma ejecución el record es estable y las cifras provienen siempre del estado del vault en el momento del run. Nota operativa: en un run con `--vault-root` apuntando fuera del vault (fixtures temporales), `results_file` se reporta como la ruta canónica relativa del tool (`80-agents/tools/context-budget/results/<archivo>.json`), nunca como path absoluto ni relativo al cwd del operador (regla 11).
- Transparencia de side-effects: la PRIMERA corrida de humo (03:56, antes de fijar `sys.dont_write_bytecode`) refrescó la entrada de `agents_os_conformance` en el `__pycache__` preexistente del harness (mismo subproducto que produce ejecutar el propio harness); desde ese ajuste, ninguna corrida de la tool ni del selftest escribe bytecode (0 `__pycache__` en `context-budget/`).
- El selftest enlaza el harness dentro del vault temporal por symlink para respetar la resolución relativa a VAULT_ROOT; si la instalación del vault moviera el harness de `80-agents/tools/conformance-harness/`, la constante `HARNESS_REL` de la tool debe actualizarse en el mismo ciclo.
