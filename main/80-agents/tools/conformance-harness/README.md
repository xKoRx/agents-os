---
type: doc
schema_version: 1
status: active
scope: project
project: "[[AGENTS OS]]"
area: "[[Personal]]"
created: 2026-09-13
updated: 2026-09-13
description: Conformance Harness de AGENTS OS (Test Model V1) — qué prueba, cómo correrlo, semántica de resultados y cómo extenderlo.
aliases:
  - conformance-harness
  - agents-os-conformance
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
---

# AGENTS OS Conformance Harness

Suite de conformance para AGENTS OS definida por el Test Model V1: 25 escenarios en tres capas más un check pre-flight de fidelidad de la transcripción (RULES-FIDELITY-ANCHORS) que verifican que los contratos observables de las autoridades vigentes se cumplen sobre el corpus real del vault HOY. Implementación: Python 3.9+ stdlib only, determinista, read-only sobre todo el vault salvo `results/`.

- Diseño binding: [[80-agents/tools/conformance-harness/artifacts/conformance-spec-v1.md|conformance-spec-v1]] (secciones 3-10) y [[80-agents/tools/conformance-harness/artifacts/conformance-scenarios.md|conformance-scenarios]] (ids, campos y valores esperados).
- Evidencia de las reglas: [[80-agents/tools/conformance-harness/artifacts/contract-audit.md|contract-audit]] (C01-C17) y [[80-agents/tools/conformance-harness/artifacts/domain-isolation-audit.md|domain-isolation-audit]] (Hallazgos 1-17).
- Autoridades transcritas: [[80-agents/skills/agents-os-bootstrap/SKILL.md|agents-os-bootstrap]], [[80-agents/skills/agents-os-doctor/SKILL.md|agents-os-doctor]], [[80-agents/skills/agents-os-context-retrieval/SKILL.md|agents-os-context-retrieval]] y los routers de dominio.

## Qué prueba

- **Pre-flight — RULES-FIDELITY-ANCHORS (corre en toda capa antes de los escenarios):** guarda anti-deriva de la transcripción (D2 de la verificación adversarial): assertion estática de que las citas literales de las autoridades que `rules.py` declara transcribir — líneas del domain gate del paso 6 (incluidas la cláusula de evidencia de superficie y la sentencia fail-closed), cold set (pasos 1-5), warm turn (Session Modes + pasos 1-4), entity swap (Session Modes + pasos 1-4) y regla superseded de bootstrap SKILL.md; líneas del club del doctor Check 3 — siguen existiendo verbatim en los archivos de autoridad vigentes (el emparejamiento colapsa solo whitespace por los saltos de línea; las palabras deben ser exactas). La cobertura del guard es exactamente el texto de decisión transcrito listado en `rules.FIDELITY_ANCHORS`, no la equivalencia semántica completa del documento (limitación 3 de "Notas de operación"). Cada ancla vive en `rules.FIDELITY_ANCHORS` (`rules.py`) citando su archivo de autoridad. Ancla ausente → FAIL con la cita faltante (transcripción obsoleta: los resultados de los escenarios dependientes del gate no son confiables; en runs full/--layer el gate L0 corta L1/L2); archivo de autoridad ausente → FAIL, nunca crash. Correrlo solo: `--scenario RULES-FIDELITY-ANCHORS`.
- **L0 — STATIC (8 escenarios):** parseo/grep determinista de archivos y frontmatter: validador del schema-contract en verde, startup no duplicado (solo bootstrap), closed club `load_policy: always` (exactamente 4 miembros), vocabulario de `load_policy`, paridad INDEX.md ↔ disco (incluye verificación de los conteos declarados por el callout de INDEX contra las filas parseadas: mismatch → WARN), sincronía de los dos registros de dominio, cero secretos en Markdown vivo, pureza de dominio de la memoria activa (un checkpoint activo por `continuity_key`).
- **L1 — SIMULATED (16 escenarios):** transcripción ejecutable y fiel de las reglas reales de arranque (marker → cold set → inferencia de entidad → domain gate → minimal reads del router; modelo de sesión con `session_mode`/`active_entity`/`active_domain` y transiciones warm/swap; filtro de retrieval por entidad activa que ignora superseded/archived). La transcripción vive en `rules.py` (único módulo de reglas, autoridad citada por regla) y se ejecuta sobre fixtures reales del vault: `30-resources/applications/RIO.md`, `10-projects/Echo Forge/Echo Forge.md`, preferencias scoped, continuidad global y su archive. Telemetría de turnos: el escenario fija `s.turn` al turno que ejecuta ANTES de invocar `cold_start`/`warm_turn`/`swap_entity` y el modelo nunca avanza el turno por su cuenta, de modo que `opens_in_turn(N)` describe exactamente el turno declarado y las aserciones por-turno (cero relecturas de base en warm, nota interna global y pack anterior no re-abiertos en el turno del swap) miden el turno real (fix D1 de la verificación adversarial).
- **L2 — LIVE-EXPOSURE (1 escenario + baseline):** parte automatizada: lee las configs de superficie de la máquina (`~/.zcode/cli/config.json`, `~/.cursor/mcp.json`, `~/.codex/config.toml`, nombres y flags only, jamás credenciales) y asserta servers `aranea-*` presentes y cero servers Meli (zord/fury/spellbook/melisource); SKIP si no existen o con `--no-live`. La sonda manual de auto-reporte de una sesión real fresca queda SKIP por defecto: el orchestrator la ejecuta pidiéndole al agente fresco que declare (sin ejecutar ninguna tool) su stack base, prefijos MCP visibles y router aplicado, y registra el resultado a mano.
- **Context baseline (siempre):** bytes/chars/tokens aproximados (chars/4, baseline-only, sin tokenizador de autoridad) del always-load (constitución, perfil, continuidad global, INDEX) y de los packs meli/aranea. Sale en el JSON y como línea del summary; nunca es criterio de fallo.

## Cómo correrlo

- Run completo (L0 → gate → L1 → L2): `python3 80-agents/tools/conformance-harness/agents_os_conformance.py`
- Una sola capa: `python3 80-agents/tools/conformance-harness/agents_os_conformance.py --layer L0` (ídem `L1`, `L2`)
- Un escenario puntual: `python3 80-agents/tools/conformance-harness/agents_os_conformance.py --scenario COLD-MELI`
- Salida machine-readable: `--json` (JSON a stdout + `results/run-<timestamp>.json`); el resumen humano va a stderr en ese modo.
- Opciones: `--vault-root <path>` (default: autodetección subiendo desde el script hasta la carpeta que contiene `80-agents/agents-os/agents-os.md`; si no la encuentra, error), `--no-live` (omite la parte de configs de máquina de L2, p. ej. fuera de la máquina del owner).
- Corte por gate: cualquier FAIL en L0 detiene L1/L2 (reportan SKIP con motivo) porque sus resultados no serían interpretables sobre un corpus no conformante; un FAIL en L1 no corta la suite. Los runs `--scenario` son dirigidos por el operador y no aplican el gate.
- Exit code: 0 si no hay FAIL, 1 si hay algún FAIL, 2 si no se pudo resolver VAULT_ROOT.

## Qué NO prueba

- Obediencia real de un modelo en sesión viva más allá de la sonda de auto-reporte: el domain gate es prompt-discipline sin enforcement mecánico (Hallazgo 3); los escenarios SIMULATED prueban la decisión replicada desde las autoridades, no la obediencia.
- Invocación de cualquier tool real (`mcp__aranea-*`, zord, fury, graphify contra servicios): prohibida en todos los niveles; la presencia de tools en superficie nunca es violación (Hallazgo 4).
- Mutación del vault: el harness no crea, modifica ni borra notas canónicas; el materializador no se ejecuta; el validador del schema corre en modo verificación.
- Contratos sin criterio determinista: conteo exacto de tokens (C04, sin tokenizador de referencia), nota de orientación por degradación (C05), precedencia con fixtures de conflicto inyectados (C15), certificación `tools/list` server-side (C13), transición viva de retiro y materialización completa (C17 — serían mutantes).
- Garantía de exposición MCP por dominio: la config vive a nivel máquina, fuera del vault (Hallazgos 4 y 17); solo se verifica el estado observado de las configs.

## Semántica de resultados

- `PASS`: contrato demostrado cumplido con autoridad inequívoca.
- `FAIL`: violación demostrada de contrato con autoridad inequívoca (degrada el veredicto de la suite; corta L1/L2 si está en L0).
- `WARN`: riesgo o ambigüedad verificable, no violación demostrada; las ambigüedades declaradas por los audits son WARN por diseño y no degradan el veredicto. WARN declarados: la cláusula de evidencia de superficie de DEFAULT puede colapsar a ARANEA en esta máquina (COLD-DEFAULT, Hallazgo 6); extras de vocabulario `load_policy` fuera de la enumeración literal de bootstrap (LOAD-POLICY-VOCABULARY, C09/Hallazgos 7 y 12); la nota VPN cross-domain sin campo `area` (COLD-ARANEA, Hallazgo 7); áreas `[[Echo Forge]]`/`[[Personal]]` en memoria de dominio (ACTIVE-MEMORY-DOMAIN-PURITY, Hallazgo 11); cláusula dual de `pr-description` entre registros (DUAL-REGISTRY-DOMAIN-SYNC); clasificación de modo ambigua al resolver entidad desde DEFAULT (SWITCH-DEFAULT-*); keyword+UUID ambiguo en el barrido de secretos (identidad vs token).
- `SKIP`: no ejecutable en el entorno actual, siempre con motivo (fixture ausente, configs de máquina ausentes, `--no-live`, gate L0 en rojo, marker de VAULT_ROOT ausente, o error inesperado al ejecutar un escenario —p. ej. un fixture L0 ausente—: SKIP con el resumen de la excepción como motivo, nunca traceback abortando el run y nunca UNKNOWN→PASS; KeyboardInterrupt/SystemExit sí propagan).
- `UNKNOWN` nunca se convierte en `PASS`; un check que no puede determinar su condición termina SKIP o WARN con motivo explícito.

## Cómo agregar un escenario nuevo

1. Elegir nivel: L0 si es parseo/grep de archivos reales; L1 si replica una regla de decisión (entonces la regla va en `rules.py` con su cita de autoridad en comentario); L2 solo si es presencia/exposición observable sin invocación.
2. Escribir la función `sc_<id_en_snake_case>(ctx) -> (state, details, evidence)` en `agents_os_conformance.py` usando solo los helpers existentes (`require_files`, `_assert_absent`, `rules.Session`, etc.) y devolviendo únicamente estados PASS/FAIL/WARN/SKIP con motivo. Si la regla replica una decisión que transcribe texto de autoridad, añadir la cita literal correspondiente a `rules.FIDELITY_ANCHORS` (`rules.py`, con el path del archivo de autoridad) para que el pre-flight la vigile.
3. Registrarla en la lista `SCENARIOS` con `(id, level, fn)` — el id debe seguir el formato del artefacto de escenarios y todo valor esperado debe citar su autoridad en la docstring o en la evidence.
4. Documentar el escenario en `artifacts/conformance-scenarios.md` (o un artefacto nuevo de diseño): el harness no inventa comportamiento sin autoridad; si el escenario revela una ambigüedad nueva, se registra como WARN y se referencia, nunca se resuelve en código.

## Notas de operación

- Determinista y sin red/DB/CI/daemon; cada run escribe un `results/run-<timestamp>.json` con `{run, baseline (git HEAD informativo), levels, scenarios, counts, context_baseline}`.
- Los findings sobre AGENTS OS que detecte la suite se registran en la salida, nunca se auto-corrigen (spec section 7).
- La heurística de STARTUP-DUPLICATION (D1/D2/D3) y la de matching de entidades en retrieval están definidas por el harness y declaradas como tales, porque ninguna autoridad fija esos límites (unknowns de C01/C03/C09).
- Limitaciones conocidas (declaradas, no silenciosas): (1) el umbral de bearer de `_bearer_is_value` (NO-SECRETS-IN-MARKDOWN) clasifica como valor un bearer que contiene algún dígito o mide ≥20 caracteres; un token real alfanumérico de 12-19 caracteres sin dígitos pasaría desapercibido — umbral definido por el harness tras un falso positivo de prosa ("Bearer constant-time") y ninguna autoridad fija la frontera prosa/valor. (2) El cold-set L1 verifica existencia y aperturas de los archivos base, no su contenido: una constitución o perfil truncado no se detecta en L1 — la higiene de contenido vive en L0, el validador del schema y el doctor (limitación de alcance declarada; el L1 replica decisiones de carga, no hace hashing de contenido). (3) RULES-FIDELITY-ANCHORS es una aserción de existencia de citas, no de equivalencia semántica: su cobertura es el texto de decisión transcrito listado en `rules.FIDELITY_ANCHORS` (domain gate del paso 6 con la cláusula de evidencia de superficie y la sentencia fail-closed, cold set pasos 1-5, warm, swap, regla superseded, club del doctor); una inserción de texto nuevo entre o alrededor de anclas, o una edición semántica de texto de autoridad que ninguna regla transcribe, puede dejar el guard en PASS mientras la autoridad deriva (adversarial-verification-r2, N1/B1).
