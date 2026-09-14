---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start:
due:
progress: 75
repo:
jira:
prs:
aliases:
  - Agents OS Context Hygiene
  - Context Hygiene and Canonical Integrity
tags:
  - kind/project
  - area/personal
  - project/agents-os
created: "2026-09-13"
updated: "2026-09-14"
---

# AGENTS OS - Context Hygiene and Canonical Integrity

%% Naming: AGENTS OS - Context Hygiene and Canonical Integrity es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ AGENTS OS - Context Hygiene and Canonical Integrity
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1
> Proyecto `owner: agent`: esta nota es el planificador durable; la evidencia pesada vive en los artifacts de cada tool. Link > copy.

## 🎯 Objetivo

Convertir la salud de Agents-OS en una superficie verificable y barata de operar, manteniendo una sola autoridad por comportamiento:

1. **Conformance Harness** — correctness / contratos observables.
2. **PHASE 2 — Context Budget + Domain Leak Auditor** — eficiencia de contexto, aislamiento DEFAULT/MELI/ARANEA y leakage.
3. **PHASE 3 — Canonical / Deprecation Linter** — higiene documental, canonicalidad, deprecación, archive, routing y hot-path.
4. **PHASE 4 — Unified `agents-os doctor`** — agregación delgada de los tres instrumentos anteriores más el Doctor estructural existente, sin duplicar business logic ni auto-corregir el sistema.

La meta final de PHASE 4 es que un operador o agente pueda ejecutar **un solo health check read-only** y obtener una fotografía honesta, acotada y machine-readable de:

```text
STRUCTURAL
CONFORMANCE
CONTEXT / DOMAIN ISOLATION
CANONICAL / DEPRECATION
```

## 📊 Estado actual

- **Conformance Harness — DONE / OWNER REVIEW.** Autoridad para cold/warm/switch/isolation y contracts observables. Sigue registrando defectos reales del sistema sin auto-corregirlos; su F1 conocido no debe ocultar diagnósticos independientes de otras herramientas.
- **PHASE 2 — DONE.** `python3 80-agents/tools/context-budget/context_budget.py`; selftest 21/21; suite estable PASS 7 · FAIL 0 · WARN 7 · SKIP 1. Baseline cold: DEFAULT ≈7025, MELI ≈9042, ARANEA ≈8222 `estimated_tokens` (`chars/4`, nunca precisión falsa). Warm deltas y ambos swaps cubiertos; 0 domain leaks; 0 deprecated hot-path; MCP surface SKIP salvo `--live`.
- **PHASE 3 — DONE.** `python3 80-agents/tools/canonical-linter/canonical_linter.py`; 20 checks CL-01..CL-20; selftest 9/9; real-vault PASS 6 · FAIL 5 · WARN 9 · SKIP 0 · 1004 findings. D1 de CL-14 corregido y verificado; findings reales preservados.
- **PHASE 3.5 — PLANNED / NOT IMPLEMENTED.** Slice correctivo atómico incorporado el 2026-09-14 tras el challenge de [[AGENTS OS - Desarrollo Agnóstico por Dominio]]. Cierra una migración federada incompleta y desacopla el dominio del hot path del core. Va **antes** de PHASE 4 porque su invariante termina como check del provider `Canonical`, y porque un Doctor unificado sobre un corpus con dos fuentes por hecho agrega verdes falsos. Ver [[doctor-verde-falso-por-duplicados-core-federado]].
- **PHASE 4 — PLANNED / NOT IMPLEMENTED.** La arquitectura está congelada en `80-agents/skills/agents-os-doctor/PHASE-4-AGGREGATION-SPEC.md`. No existe todavía un Doctor unificado: el `agents-os-doctor` executable actual sigue siendo el Doctor estructural existente.

## 🧭 Arquitectura PHASE 4

El Doctor unificado será **aggregation only**:

```text
                     agents-os doctor
                            │
                            ▼
                    thin orchestrator
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      structural       conformance          context
          │                                   │
          └─────────────────┬─────────────────┘
                            ▼
                        canonical
                            │
                            ▼
                   normalized envelope
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
             human summary           --json
```

### Providers y ownership

| Provider | Entrypoint actual | Ownership |
|---|---|---|
| Structural | `80-agents/skills/agents-os-doctor/scripts/doctor.py` | instalación/core hygiene existente |
| Conformance | `80-agents/tools/conformance-harness/agents_os_conformance.py` | correctness/contracts |
| Context | `80-agents/tools/context-budget/context_budget.py` | context footprint/domain leakage |
| Canonical | `80-agents/tools/canonical-linter/canonical_linter.py` | canonical/deprecation/routing hygiene |

Regla principal:

> **Provider owns semantics; Doctor aggregates.**

PHASE 4 no copia checks, no transcribe reglas, no inventa un segundo routing model y no reinterpreta findings para hacerlos calzar.

### Invariantes

- Un único entrypoint canónico de Doctor; preferir conservar `80-agents/skills/agents-os-doctor/scripts/doctor.py` si P4-A confirma que es seguro evolucionarlo.
- Ejecución secuencial por defecto; no consumir concurrencia por comodidad.
- Un `FAIL` de un provider **no corta** providers independientes posteriores.
- Separar `execution_status: OK|ERROR` de `verdict: PASS|FAIL|WARN|SKIP`.
- `UNKNOWN` o no observable jamás se convierte en `PASS`.
- `--strict` afecta exit policy; no muta records ni severidades.
- `estimated_tokens` sigue siendo estimado.
- El output humano es acotado; 1000+ findings no se imprimen completos.
- JSON conserva provenance (`provider`, `check_id`, evidence/confidence cuando exista).
- `--live` sólo habilita observación segura; jamás side effects.
- Doctor es read-only y no repara findings automáticamente.
- Capturar baseline Git al inicio/fin cuando exista Git; auto-sync no debe ocultarse.
- No fuzzy/LLM semantic dedup en V1; preservar provenance antes que “limpiar” demasiado el reporte.

### CLI objetivo

P4-A debe validar los contratos reales antes de implementar. El target mínimo, sólo si las interfaces actuales lo soportan legítimamente, es:

```text
--component structural|conformance|context|canonical|all
--json
--strict
--live
--vault-root PATH
```

No crear daemon, DB, dashboard, MCP, scheduler, framework de plugins ni CI remoto dentro de PHASE 4.

### Resultado objetivo

```text
AGENTS-OS DOCTOR
baseline: <start> → <end> (stable|moved)
mode: read-only / non-live

STRUCTURAL   PASS   ...
CONFORMANCE  FAIL   ...
CONTEXT      WARN   DEFAULT≈7.0k · MELI≈9.0k · ARANEA≈8.2k est
CANONICAL    FAIL   5 failing checks · 1004 findings

OVERALL      FAIL
```

Un provider que **ejecuta correctamente y encuentra un bug real** es `execution_status=OK, verdict=FAIL`. Un provider que se rompe es `execution_status=ERROR`; eso no se debe maquillar como un defecto demostrado de Agents-OS.

## ✅ Tareas

> [!note]+ Estado
> `[ ]` To Do · `[/]` WIP · `[r]` Review · `[x]` Done. El parent/orchestrator es el single writer del planning global; artifacts grandes viven junto a las tools.

### PHASE 2 — Context Budget + Domain Leak

- [x] P2-A — Context Budget Auditor/Designer → `80-agents/tools/context-budget/artifacts/p2-context-budget-design.md` #owner/agent #type/research #area/personal
- [x] PARENT GATE P2 — spec binding → `80-agents/tools/context-budget/artifacts/p2-context-budget-spec.md` #owner/agent #type/admin #area/personal
- [x] P2-B — Context Budget Implementer #owner/agent #type/dev #area/personal
- [x] P2-C — Adversarial Verifier → `80-agents/tools/context-budget/artifacts/p2-adversarial-verification.md` #owner/agent #type/research #area/personal
- [x] P2-D — Fixer ciclo 1/2; selftest 21/21 #owner/agent #type/dev #area/personal
- [x] PHASE 2 acceptance gate #owner/agent #type/admin #area/personal

### PHASE 3 — Canonical / Deprecation Linter

- [x] P3-A — Canonical Integrity Designer → `80-agents/tools/canonical-linter/artifacts/p3-canonical-model.md` #owner/agent #type/research #area/personal
- [x] PARENT GATE P3 — spec binding → `80-agents/tools/canonical-linter/artifacts/p3-canonical-linter-spec.md` #owner/agent #type/admin #area/personal
- [x] P3-B — Canonical Linter Implementer #owner/agent #type/dev #area/personal
- [x] P3-C — Adversarial Verifier → `80-agents/tools/canonical-linter/artifacts/p3-adversarial-verification.md` #owner/agent #type/research #area/personal
- [x] P3-D — Fixer D1/CL-14; selftest 9/9 #owner/agent #type/dev #area/personal
- [x] PHASE 3 acceptance gate #owner/agent #type/admin #area/personal

### PHASE 3.5 — Canonical Dedup + Domain Decoupling

> [!warning]+ Slice atómico, un solo gate
> Los cinco pasos se aceptan juntos o se revierten juntos: deduplicar sin adaptar el builder deja la distribución sin índice, y adaptar el builder sin deduplicar deja dos fuentes escribibles. Sin adapter ficticio ni simulación E2E de un tercer dominio.

- [x] P35-A — **Dedup skills y runbooks**: completar la migración dejando `30-resources/` como autoridad y borrando la copia de `80-agents/`. Alcance verificado al 2026-09-14: 13 skills (12 idénticas, `signals-code-review` divergente en `updated` y rutas relativas) y 9 runbooks, con tres divergencias materiales — `aranea-mcp-capability-plane.md` (172 líneas), `aranea-ssh-mcp.md` (143 líneas) y `signals-code-review.md`, `superseded` en el federado y vigente en el core. #owner/agent #type/dev #area/personal
- [/] P35-B — **Builder y proyección del índice distribuido**: repuntar `core-export/sources.list` al path federado y adaptar `build-core.py` en el mismo cambio. `filter_skill_index()` matchea `80-agents/skills/([^/]+)/SKILL\.md` y descarta el bloque `## 🌐 Registro federado` completo; reapuntar sin tocarlo deja skills copiadas y cero filas descubribles. #owner/agent #type/dev #area/personal
- [ ] P35-C — **Registro de dominios externo**: sacar el mapping del paso 6 de `agents-os-bootstrap` hacia un registro externo y opcional, con resolución `0 → DEFAULT`, `1 → router`, `>1 → fail-closed`. Preservar cold/warm/swap. #owner/agent #type/dev #area/personal
- [ ] P35-D — **Desacoplar el hot path**: remover las referencias operativas a dominios y tooling del core always-load, incluida `agent-constitution.md` (reglas 12 y 14 nombran workspaces y convención de release de dominio y viajan al core compartido). Ajustar sólo los fixtures existentes necesarios. #owner/agent #type/dev #area/personal
- [ ] P35-E — **Check permanente de duplicados**: agregar la detección core↔federado como **check nuevo del provider `Canonical`**, no como quinto provider; PHASE 4 sólo lo agrega. Preserva `provider owns semantics; Doctor aggregates`. #owner/agent #type/dev #area/personal
- [ ] PHASE 3.5 acceptance gate — todos los gates observables verdes; luego OWNER REVIEW. #owner/agent #type/admin #area/personal

#### Gates observables PHASE 3.5

| Gate | Evidencia |
|---|---|
| Dedup completo | Cero nombres duplicados entre core y federado, en skills **y** runbooks |
| Doctor limpio | `HIGH=0 / MEDIUM=0` sin suprimir findings |
| Distribución sana | Export reproducible y sus skills descubribles desde el índice distribuido |
| Core agnóstico | Cero literales operativos de dominio no allowlisted **en el artefacto construido**, distinguiendo por allowlist los ejemplos históricos y fixtures de las dependencias operativas |
| Routing | `0 / 1 / >1` probado, con `>1` cerrado |
| Paridad | Meli, Aranea y DEFAULT se comportan igual que antes del cambio |
| Eliminación | Quitar una entrada del registro y su paquete no deja referencias ejecutables rotas |

### PHASE 4 — Unified Agents-OS Doctor

- [x] P4-0 — Freeze de arquitectura/spec → `80-agents/skills/agents-os-doctor/PHASE-4-AGGREGATION-SPEC.md` #owner/agent #type/admin #area/personal
- [ ] P4-A — **Provider Contract Audit**: inspeccionar los cuatro providers reales; fijar flags, JSON disponible, exit codes, runtime requirements, timeouts, overlaps y adapters mínimos. NO implementar antes de este gate. #owner/agent #type/research #area/personal
- [ ] P4-B — **Thin Aggregator**: ejecución secuencial, failure isolation, normalized envelope, concise human renderer + JSON; cero business logic duplicado. #owner/agent #type/dev #area/personal
- [ ] P4-C — **Integration Selftests**: PASS/WARN/SKIP/FAIL, provider ERROR, strict sin mutación de verdict, component filtering, JSON envelope, moving baseline, no canonical mutation. #owner/agent #type/dev #area/personal
- [ ] P4-D — **Fresh Adversarial Verification**: intentar demostrar lógica duplicada, fail-fast indebido, false PASS, ERROR→FAIL, precisión falsa, output flooding, side effects, pérdida de structural checks o exit codes inconsistentes. #owner/agent #type/research #area/personal
- [ ] P4-E — **Skill/Docs/Acceptance**: actualizar `agents-os-doctor/SKILL.md` sólo después de que runtime exista, ejecutar selftests de todos los providers + real-vault smoke, actualizar proyecto/handoff. #owner/agent #type/admin #area/personal
- [ ] PHASE 4 acceptance gate — Doctor unificado read-only, truthful y reproducible; luego OWNER REVIEW. #owner/agent #type/admin #area/personal

## 🚦 Acceptance gate PHASE 4

No declarar DONE hasta demostrar:

```text
[ ] provider contracts reales auditados
[ ] zero duplicated provider business logic
[ ] structural Doctor existente preservado o ownership re-asignado explícitamente
[ ] un solo Doctor entrypoint
[ ] ejecución secuencial demostrada
[ ] provider FAIL no suprime providers independientes
[ ] provider ERROR distinguible de Agents-OS FAIL
[ ] PASS/FAIL/WARN/SKIP preservados
[ ] concise human summary
[ ] machine-readable JSON
[ ] DEFAULT/MELI/ARANEA visibles sin precisión falsa
[ ] grandes finding sets acotados en output humano
[ ] --strict verificado
[ ] component filtering verificado
[ ] --live sigue read-only
[ ] baseline start/end capturado cuando Git está disponible
[ ] no canonical mutation
[ ] integration tests green
[ ] provider selftests siguen green
[ ] real-vault smoke
[ ] fresh adversarial verifier
[ ] SKILL.md describe implementación real, no intención futura
```

## ⛔ Non-goals PHASE 4

PHASE 4 NO:

- corrige F1 del Conformance Harness;
- limpia los 1004 findings del corpus;
- optimiza automáticamente los budgets de contexto;
- redefine DEFAULT/MELI/ARANEA;
- auto-repara documentación;
- crea dashboard/daemon/MCP/scheduler;
- rediseña Agents-OS.

La remediación de findings es un carril posterior. Primero se construye una superficie única y confiable para medir antes/después.

## 📆 Bitácora

- **2026-09-14 — PHASE 3.5 incorporada.** El challenge de [[AGENTS OS - Desarrollo Agnóstico por Dominio]] cerró `NOT_READY` y su único trabajo con valor verificado aterrizó acá por ownership: este proyecto ya posee canonicalidad y domain leak. Se descubrió que los 13 `MEDIUM` de Doctor no eran deuda de índice sino una migración federada incompleta, y que la duplicación alcanza también a 9 runbooks con tres divergencias materiales que Doctor no ve — por lo que `MEDIUM=0` por sí solo sería verde falso. Se sumó el desacoplamiento de dominio del hot path, incluida la constitución, y el gate sobre el artefacto construido. Runtime no modificado.

- **2026-09-13 — PHASE 4 preparada.** Se confirmó que ya existe un `agents-os-doctor` estructural y que la integración correcta es evolucionarlo a **thin aggregator**, no crear un segundo Doctor. Se congeló `PHASE-4-AGGREGATION-SPEC.md`: providers, status dual execution/verdict, failure isolation, JSON envelope, exit policy, output bounded, baseline stability, safety, P4-A..P4-E y acceptance gate. Runtime PHASE 4 todavía NO implementado.
- **2026-09-13 — PHASE 3 DONE.** Real-vault post-D1: PASS 6 · FAIL 5 · WARN 9 · SKIP 0 · 1004 findings. CL-14 revisa todos los wikilinks por fila; selftest 9/9; ningún finding real maquillado.
- **2026-09-13 — PHASE 2 DONE.** Auditor de contexto estabilizado tras verificación adversarial; selftest 21/21; 0 domain leaks y 0 deprecated hot-path observados en su baseline.
- **2026-09-13 — Proyecto creado.** Conformance Harness se trató como input y autoridad de contracts, no como trabajo a rehacer. Restricción operativa de la campaña original: máximo un subagent activo a la vez.

## 🧭 Decisiones

- Una fuente por hecho: providers poseen checks; Doctor sólo agrega.
- Conformance Harness sigue siendo autoridad para cold/warm/switch/isolation.
- El Doctor estructural existente no se elimina por reflejo; P4-A debe revisar overlaps y preservar capacidades sin duplicarlas.
- Findings de Agents-OS se registran y priorizan; diagnóstico ≠ remediación.
- Phase 4 usa KISS/YAGNI: thin orchestration, bounded output, JSON y nada más.
- Cuando el vault auto-sync mueva HEAD durante un run, reportar baseline moved en vez de congelar Git destructivamente.
- La detección de duplicados core↔federado es un check del provider `Canonical`, no un provider nuevo: el provider posee la semántica y Doctor sólo agrega.
- El gate de agnosticismo de dominio se ejecuta sobre el artefacto construido, no sólo sobre las fuentes: el export actual valida verde conteniendo referencias operativas de dominio.
- `agent-development-workflow`, capabilities abstractas, `autonomy envelope` y `delivery checkpoint` quedan fuera de este slice; los dos últimos vuelven sólo con un consumidor concreto.

## 🔗 Docs / Links

- `80-agents/skills/agents-os-doctor/PHASE-4-AGGREGATION-SPEC.md` — contrato de implementación PHASE 4.
- `80-agents/skills/agents-os-doctor/SKILL.md` — Doctor estructural actual; no afirmar que ya es el unificado.
- `80-agents/tools/conformance-harness/` — provider de correctness/contracts.
- `80-agents/tools/context-budget/` — provider de context budget/domain leakage.
- `80-agents/tools/canonical-linter/` — provider de canonical/deprecation.

## ➡️ Next exact

**P35-A..E — Canonical Dedup + Domain Decoupling.** Slice atómico, un solo gate, antes de PHASE 4. Después: **P4-A — Provider Contract Audit** con agente fresco, read-only para discovery; fijar el contrato REAL de los providers y recién ahí autorizar P4-B.
