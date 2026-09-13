---
type: doc
schema_version: 1
status: active
scope: project
project: "[[AGENTS OS]]"
area: "[[Personal]]"
created: 2026-09-12
updated: 2026-09-12
description: Test Model V1 del AGENTS OS Conformance Harness; input obligatorio del Harness Implementer. Reconcilia contract-audit (C01-C17), domain-isolation-audit (Hallazgos 1-17) y conformance-scenarios (25 escenarios).
aliases:
  - conformance-spec-v1
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
---

# Conformance Spec V1 — Test Model del AGENTS OS Conformance Harness

- Autor: parent/orchestrator (único escritor del planner). Fecha: 2026-09-12. Baseline git: `a6a503f` (ancestro del HEAD vivo; el vault tiene auto-sync).
- Inputs reconciliados: `80-agents/tools/conformance-harness/artifacts/contract-audit.md`, `domain-isolation-audit.md`, `conformance-scenarios.md`. Los tres son consistentes entre sí; no se arbitró ninguna contradicción factual porque no surgió ninguna. Las tensiones reales son ambigüedades de autoridad ya documentadas y se prueban con semántica WARN.

## 1. Qué se prueba

- Que los contratos observables declarados por las autoridades vigentes de AGENTS OS (constitución, bootstrap, routers de dominio, doctor, schema-contract, registros de skills) se cumplen en el corpus real del vault HOY.
- Que la lógica de decisión del domain gate, cold start, warm turn, entity swap y retrieval lazy —transcrita fielmente de `80-agents/skills/agents-os-bootstrap/SKILL.md` y `80-agents/skills/agents-os-context-retrieval/SKILL.md`— produce las selecciones esperadas sobre fixtures reales (frontmatter de entidades del vault).
- Que la superficie de exposición de tools MCP de las configuraciones de máquina observables es la declarada (presencia/ausencia; nunca invocación).
- El footprint de contexto (bytes/chars y tokens aproximados chars/4) del always-load y de los packs por scope, SOLO como baseline, sin optimizar nada.

## 2. Qué NO se prueba

- Comportamiento de obediencia real de un modelo en sesión viva más allá del LIVE-SMOKE declarado (auto-reporte de stack y presencia de tools; el gate es prompt-discipline, Hallazgo 3 del domain audit).
- Invocación de cualquier tool real (`mcp__aranea-*`, zord, fury, graphify queries contra servicios): prohibido en todos los niveles.
- Mutación del vault: ningún escenario crea, modifica o borra notas canónicas (el harness escribe únicamente dentro de `80-agents/tools/conformance-harness/`).
- Los contratos C04 (conteo exacto de tokens: sin tokenizador de referencia), C05 (nota de orientación: sin trigger determinista de degradación), C15 (precedencia con conflictos inyectados: requiere fixtures sintéticos que no existen), C13-prod (certificación `tools/list` server-side: exige invocar tools), C14-transición viva y C17-materialización completa (mutantes). Registrados como NO-CUBIERTO con autoridad en la cobertura de escenarios.
- La garantía de exposición de MCP por dominio (imposible desde el vault mientras la config viva a nivel máquina, Hallazgo 17): se verifica el estado observado de las configs, no se fuerza nada.

## 3. Layers

- **L0 — STATIC CONFORMANCE** (8 escenarios): parseo/grep determinista de archivos y frontmatter. SCHEMA-VALIDATOR-GREEN, STARTUP-DUPLICATION, CLOSED-CLUB-ALWAYS, LOAD-POLICY-VOCABULARY, REGISTRY-DISK-PARITY, DUAL-REGISTRY-DOMAIN-SYNC, NO-SECRETS-IN-MARKDOWN, ACTIVE-MEMORY-DOMAIN-PURITY. Gate previo: si algún L0 falla, L1/L2 no se ejecutan (sus resultados no serían interpretables sobre un corpus no conformante).
- **L1 — SIMULATED CONFORMANCE** (16 escenarios): replicación determinista de las reglas de decisión reales (transcripción executable del bootstrap: marker → cold set → entity inference → domain gate → minimal reads del router; modelo de sesión con estados session_mode/active_entity/active_domain y transiciones warm/swap) sobre frontmatter y autoridades reales. COLD-DEFAULT, COLD-MELI, COLD-ARANEA, COLD-CONFLICTING-EVIDENCE-FAILS-CLOSED, WARM-DEFAULT, WARM-MELI, WARM-ARANEA, BOOTSTRAP-NOT-RERUN-ON-WARM, SWITCH-MELI-TO-ARANEA, SWITCH-ARANEA-TO-MELI, SWITCH-DEFAULT-TO-MELI, SWITCH-DEFAULT-TO-ARANEA, MELI-NEGATIVE-ARANEA-TOOL, ARANEA-NEGATIVE-MELI-TOOL, DEPRECATED-DOC-NOT-DEFAULT-LOAD, UNRELATED-DOMAIN-NOT-LOADED.
- **L2 — LIVE-EXPOSURE SMOKE** (1 escenario + baseline): SESSION-SURFACE-EXPOSURE en dos partes. Parte automatizada (ejecutable por el script, determinista y read-only): inspección de las configs de superficie de la máquina (`~/.zcode/cli/config.json`, `~/.cursor/mcp.json`, `~/.codex/config.toml` si existen) para verificar qué servers MCP están configurados y habilitados — assert: servers `aranea-*` presentes según config, cero servers Meli (zord/fury/spellbook/melisource). Parte manual (SKIP por defecto en runs scriptados): sonda de auto-reporte para una sesión real fresca, documentada en el README; el orchestrator puede ejecutarla y registrarla a mano. Además captura del baseline de contexto (siempre).

## 4. Fixtures (todos reales, verificados 2026-09-12)

- Entidad Meli: `30-resources/applications/RIO.md` (`area: "[[Meli]]"`).
- Entidad Aranea: `10-projects/Echo Forge/Echo Forge.md` (`area: "[[Echo]]"` — prueba el mapeo Echo→aranea).
- Entidad DEFAULT: `10-projects/Personal/AGENTS OS/AGENTS OS.md` (`area: "[[Personal]]"`).
- Entidad inexistente: slug que no resuelve a ninguna nota (p. ej. `entidad-fantasma-xyz`).
- Continuidad superseded: `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity-archive.md` (cuádruple de retiro verificado) vs la activa `agents-os-operating-continuity.md` (mismo `continuity_key`).
- Preferencias scoped: `rjara-meli-work-preferences.md`, `rjara-aranea-operations-preferences.md`, `rjara-vpn-routing-preferences.md` (cross-domain sin `area`, WARN).
- Memoria de dominio: 6 notas internas activas Echo/Echo Forge (0 activas Meli, estado observado — Hallazgo 10); memoria pública `80-agents/memory/public/{decision,known-error,learning}/rio/` y `.../symphony/`, `.../aranea/`.
- Registros duales: `80-agents/skills/INDEX.md` y `30-resources/agents/00-index.md`.
- Exclusiones canónicas para barridos (idénticas a doctor Check 1 y `.graphifyignore`): `.git/`, `40-archive/`, `80-agents/journal/`, `30-resources/agents-os/` (packaging), `.graphify*`, `node_modules`, `output`.

## 5. Expected outputs y resultado semantics

- Estados por check, únicamente: `PASS` (contrato demostrado cumplido), `FAIL` (violación demostrada de contrato con autoridad inequívoca), `WARN` (riesgo o ambigüedad verificable, no violación demostrada; las ambigüedades declaradas de los audits son WARN por diseño), `SKIP` (no ejecutable en el entorno actual, con motivo). `UNKNOWN` nunca se convierte en `PASS`; un check que no puede determinar su condición termina `SKIP` o `WARN` con el motivo explícito.
- Human summary: bloque `AGENTS-OS CONFORMANCE` con una línea por escenario (`ID................ LEVEL  STATE`) y conteo `PASS/FAIL/WARN/SKIP`.
- Machine-readable: `--json` emite a stdout y `results/run-<timestamp>.json` con `{run, baseline, levels, scenarios: [{id, level, state, details, evidence[]}], counts, context_baseline}`.
- Semántica de corte: cualquier `FAIL` en L0 detiene L1/L2; `FAIL` en L1 no detiene la suite (continúa y reporta); L2 nunca falla por el auto-reporte manual (sólo por la parte de configs automatizada).
- WARN no degrada el veredicto de la suite (las ambigüedades son conocidas y declaradas en los audits); FAIL sí.

## 6. Environment assumptions

- `python3` (>= 3.9) disponible; harness con stdlib only (sin PyYAML ni dependencias externas: parser de frontmatter propio minimal).
- Ejecución desde `VAULT_ROOT` o con `--vault-root <path>`; `VAULT_ROOT` = la carpeta que contiene `80-agents/agents-os/agents-os.md` (marker; si falta, la suite entera es `SKIP` con motivo).
- Configs de superficie fuera del vault: lectura opcional; si no existen, la parte automatizada de L2 es `SKIP` con motivo (no FAIL).
- Git baseline informativo en cada run (`git rev-parse HEAD`), no como gate.

## 7. Side-effect policy

- El harness es read-only sobre TODO el vault salvo su propio directorio `80-agents/tools/conformance-harness/` (donde escribe `results/`).
- Cero invocaciones de tools MCP, cero comandos de red, cero mutaciones de vault, cero creación de notas canónicas.
- El validador del schema (`validate_schema_contract.py`) se ejecuta en modo no-mutante (verificación); el materializador NO se ejecuta.
- Los findings sobre AGENTS OS se registran, nunca se auto-corrigen.

## 8. Entrypoint y CLI

- Ubicación: `80-agents/tools/conformance-harness/agents_os_conformance.py` (script único + módulos si el implementer lo necesita, KISS).
- `python3 80-agents/tools/conformance-harness/agents_os_conformance.py` — run all (L0→L1→L2 con la semántica de corte).
- `--layer L0|L1|L2`, `--scenario <ID>` (run profile/scenario), `--json`, `--vault-root <path>`, `--no-live` (omite la parte de configs de máquina si se corre fuera de la máquina del owner).
- Doc del harness: `80-agents/tools/conformance-harness/README.md` (qué prueba, cómo correrlo, qué NO prueba, semántica de resultados, cómo agregar un escenario; LINK > COPY hacia las autoridades).

## 9. Baseline de contexto (sección 11 del mandato)

- Captura por run: archivos del always-load (constitución, perfil, continuidad global, INDEX) y packs por scope (meli, aranea): bytes, chars, tokens aproximados (chars/4, métrica declarada como baseline-only, sin autoridad de tokenizador).
- Output en el JSON y una línea en el summary; sin optimización, sin gates.

## 10. Implementación

- Python 3 stdlib only; un entrypoint; escenarios como funciones registradas con id/level; sin frameworks, sin daemon, sin red, sin CI externa, sin base de datos.
- La transcripción del gate/cold-set vive en UN módulo (`rules.py` o equivalente) citando la autoridad de cada regla en un comentario — es la única pieza que replica lógica; los checks STATIC parsean archivos reales.
- Cada check devuelve `(state, details, evidence[])`; el runner agrega, corta por FAIL-L0, imprime summary y JSON.
