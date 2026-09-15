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
progress: 99
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
- **PHASE 3 — DONE.** `python3 80-agents/tools/canonical-linter/canonical_linter.py`; base CL-01..CL-20 entregada y extendida en PHASE 3.5 con CL-21; selftest 9/9. Los findings reales de otras clases se preservan.
- **PHASE 3.5 — DONE / OWNER ACCEPTED.** El owner aceptó el 2026-09-14 el slice completo y el trade-off de `[[Personal]]` como fallback portable. Autoridad federada, export, templates, materialización y CL-21 quedaron validados adversarialmente.
- **PHASE 4 — DONE / OWNER REVIEW.** P4-A/B/C/D/E están cerrados. El verifier externo reprodujo la evidencia final, desafió dos defectos semánticos ya corregidos y cerró con veredicto `READY`; sólo queda la aceptación del owner.
- **Entrega de desarrollo:** el vault no es un repositorio Git, por lo que branch/base no aplican. Spec funcional+técnica: `80-agents/skills/agents-os-doctor/PHASE-4-AGGREGATION-SPEC.md`. Runtime owner: `80-agents/skills/agents-os-doctor/scripts/doctor.py`.

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
- [x] P35-B — **Builder y proyección del índice distribuido**: `sources.list` consume la autoridad federada, proyecta las filas portables y permite exclusiones exactas verificadas para memoria scoped capturada por árboles amplios. #owner/agent #type/dev #area/personal
- [x] P35-C — **Registro de dominios externo**: mapping opcional fuera del core con resolución `0 → DEFAULT`, `1 → router`, `>1 → fail-closed`; cold/warm/swap preservados. #owner/agent #type/dev #area/personal
- [x] P35-D — **Desacoplar y probar el artefacto**: constitución, router, bootstrap, índice y templates quedaron sin dependencias operativas de dominio. El builder audita frontmatter, resolución de áreas y cuerpos ejecutables, y materializa cada tipo canónico en una instalación DEFAULT temporal antes de aceptar el export. #owner/agent #type/dev #area/personal
- [x] P35-E — **Check permanente de duplicados**: CL-21 vive en el provider `Canonical`; PHASE 4 sólo lo agregará. #owner/agent #type/dev #area/personal
- [x] PHASE 3.5 acceptance gate — gates observables verdes; owner aceptó incluido el fallback `[[Personal]]`. #owner/agent #type/admin #area/personal

#### Gates observables PHASE 3.5

| Gate | Evidencia |
|---|---|
| Dedup completo | Cero nombres duplicados entre core y federado, en skills **y** runbooks |
| Doctor limpio | `HIGH=0 / MEDIUM=0` sin suprimir findings |
| Distribución sana | Export reproducible y sus skills descubribles desde el índice distribuido |
| Core agnóstico | Cero literales operativos de dominio no allowlisted **en el artefacto construido**; seis memorias scoped excluidas completas; `area` distribuida resoluble; templates DEFAULT-neutral |
| Consecuencia materializada | Una entidad por cada tipo canónico se crea con el materializador distribuido en un vault DEFAULT temporal y vuelve a auditarse; 44/44 en verde |
| Routing | `0 / 1 / >1` probado, con `>1` cerrado |
| Paridad | El routing de entidades existentes preserva Meli, Aranea y DEFAULT; la creación cambia deliberadamente a `[[Personal]]` como fallback portable y exige ajuste scoped para entidades de dominio |
| Eliminación | Quitar una entrada del registro y su paquete no deja referencias ejecutables rotas |

### PHASE 4 — Unified Agents-OS Doctor

- [x] P4-0 — Freeze de arquitectura/spec → `80-agents/skills/agents-os-doctor/PHASE-4-AGGREGATION-SPEC.md` #owner/agent #type/admin #area/personal
- [x] P4-A — **Provider Contract Audit**: contratos reales, adapters mínimos y ownership fijados en `80-agents/skills/agents-os-doctor/P4-PROVIDER-CONTRACT-AUDIT.md`. #owner/agent #type/research #area/personal
- [x] P4-B — **Thin Aggregator**: entrypoint único, ejecución secuencial/failure isolation, JSON normalizado, salida acotada, adapters `--no-write` y soporte de registro federado vacío implementados. #owner/agent #type/dev #area/personal
- [x] P4-C — **Integration Selftests**: 14/14 PASS, 91,0% line coverage de `aggregate.py`; source y built-artifact smoke, strict/component/live y no mutation verificados. #owner/agent #type/dev #area/personal
- [x] P4-D — **Fresh Adversarial Verification**: el verifier reprodujo fixes y evidencia completa, cerró sin findings abiertos y emitió `READY`; ver handoff durable en `80-agents/skills/agents-os-doctor/P4-ADVERSARIAL-HANDOFF.md`. #owner/agent #type/research #area/personal
- [x] P4-E — **Skill/Docs/Acceptance**: skill runtime, spec, benchmark, provider docs, change log, agent run, planner y export publicados; lint estricto `0/0`. #owner/agent #type/admin #area/personal
- [r] PHASE 4 acceptance gate — implementación y challenge externo completos; pendiente sólo aceptación del owner. #owner/agent #type/admin #area/personal

## 🚦 Acceptance gate PHASE 4

No declarar DONE hasta demostrar:

```text
[x] provider contracts reales auditados
[x] zero duplicated provider business logic
[x] structural Doctor existente preservado o ownership re-asignado explícitamente
[x] un solo Doctor entrypoint
[x] ejecución secuencial demostrada
[x] provider FAIL no suprime providers independientes
[x] provider ERROR distinguible de Agents-OS FAIL
[x] PASS/FAIL/WARN/SKIP preservados
[x] concise human summary
[x] machine-readable JSON
[x] DEFAULT y packs federados instalados visibles sin precisión falsa
[x] grandes finding sets acotados en output humano
[x] --strict verificado
[x] component filtering verificado
[x] --live sigue read-only
[x] baseline start/end capturado cuando Git está disponible
[x] no canonical mutation
[x] integration tests green
[x] provider selftests siguen green
[x] real-vault smoke
[x] fresh adversarial verifier
[x] SKILL.md describe implementación real, no intención futura
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

- **2026-09-14 — P4-D cerrado `READY`.** El verifier externo reprodujo los fixes de LOW (`INFO`, no bloqueante) y ownership del fidelity gate, los selftests Doctor 14/14, Context 21/21, Canonical 9/9 y registry 0/1/>1, el build `196/15/37/7/44`, los cuatro providers `execution_status: OK` en fuente y core DEFAULT y la garantía read-only por hash. No quedan findings adversariales abiertos; PHASE 4 pasa a aceptación del owner.
- **2026-09-14 — Challenge P4-D ronda 1 incorporado.** El verifier reprodujo toda la evidencia y devolvió `READY_WITH_FINDINGS`: (1) LOW estructural estaba mal etiquetado PASS; ahora es `INFO`, visible y no bloqueante por retrocompatibilidad; (2) el agregador reconstruía el fidelity gate de Context; ahora Context emite `RULES-FIDELITY-ANCHORS` como record/count provider-owned y Doctor sólo consume. Se añadieron pruebas de LOW-only y conteo único. P4-D continúa en Review hasta reproducción del verifier.
- **2026-09-14 — PHASE 4 implementada y enviada a revisión externa.** P4-B/C/E cerrados; P4-D pasa a Review con handoff adversarial. Doctor 14/14, Context 21/21, Canonical 9/9, registry 0/1/>1, `py_compile` y lint estricto de 13 notas `ERROR=0 WARN=0`. Cobertura final del agregador 91,0%. Smoke fuente y `--live`: `execution_status=OK/verdict=FAIL`, cinco findings humanos, Markdown y 189 records de providers sin cambios. Export publicado: 196 canónicos, 15 authored, 37 skills, 7 exclusiones, 44 tipos materializados; Doctor DEFAULT ejecuta cuatro providers en OK, Context muestra sólo DEFAULT y `scope_pack={}`. `quick_validate.py` quedó no ejecutable por PyYAML ausente; los validators canónicos del vault sí pasaron.
- **2026-09-14 — Corrección DEFAULT cerrada.** Se eliminó el acceso import-time a routers Meli/Aranea; `NOT_LOAD_DEFAULT` y baselines derivan del registro real, y los escenarios scoped declaran requirements de dominio. El test permanente reproduce registro vacío contra Conformance y Context. No se exportó ningún paquete de dominio para obtener verde.
- **2026-09-14 — P4-B/P4-C reabiertos por defecto portable.** El builder terminó verde, pero el Doctor del artefacto construido devolvió `execution_status=ERROR`: `agents_os_conformance.py` hacía acceso import-time a `ROUTERS["meli"]` y `ROUTERS["aranea"]`, inexistentes por diseño en una instalación DEFAULT. Se corrige en el provider: los escenarios scoped a dominios ausentes deben declarar `SKIP` con causa y los baselines sólo medir dominios registrados. No se exportarán routers ni preferencias Meli/Aranea para ocultar el defecto.
- **2026-09-14 — P4-C cerrado, P4-D iniciado.** Selftest del Doctor 13/13 y `trace` reportó 261/261 líneas ejecutables de `aggregate.py`. Context 21/21, Canonical 9/9 y registry 0/1/>1 siguen verdes. Corridas reales: full JSON `execution_status=OK/verdict=FAIL`; Context normal `WARN/exit 0`, strict conserva WARN y retorna 1; Structural `PASS/exit 0`; inventario de `results/` y hash del corpus canónico permanecieron idénticos.
- **2026-09-14 — P4-B cerrado, P4-C iniciado.** `doctor.py` conserva los checks estructurales y delega orchestration a `aggregate.py`; Conformance/Context/Canonical reciben `--json --no-write --vault-root`, con live sólo donde cada provider lo posee. Smoke real ejecutó los cuatro en orden y terminó OVERALL FAIL por findings reales, mientras providers posteriores siguieron corriendo. El output mostró cinco findings como máximo frente a 1295 del Canonical.
- **2026-09-14 — P4-A cerrado, P4-B iniciado.** Auditoría real: Structural sólo tenía salida humana; Conformance/Context/Canonical ya emitían JSON pero escribían resultados siempre. Adapter mínimo autorizado: structural runner in-process, `--no-write` en externos, subprocess secuencial, timeout 30 s, exit `1` como FAIL real y exit `2`/timeout/JSON inválido como ERROR de ejecución. Baseline Git ausente queda unknown, no stable inventado.
- **2026-09-14 — PHASE 3.5 aceptada y PHASE 4 autorizada.** El owner aceptó explícitamente el slice, incluido `[[Personal]]` como fallback portable, y pidió implementar PHASE 4 completa con handoff verificable para revisión de otro agente. P4-A pasa a WIP; no se modifica runtime antes de cerrar la auditoría de contratos reales.
- **2026-09-14 — Validación adversarial cerrada con un trade-off visible.** El reviewer reprodujo de forma independiente build, exclusiones, templates, Doctor y fallas negativas del gate. Se retiró una entrada innecesaria del allowlist para evitar que una excepción muerta oculte findings futuros. Queda para aceptación consciente del owner que `[[Personal]]` es el default portable: una entidad nueva de Meli/Aranea permanece en DEFAULT si su flujo scoped no corrige routing en el mismo cambio.
- **2026-09-14 — Gate del artefacto completado tras challenge adversarial.** La primera implementación reducía incorrectamente el gate acordado al hot path. La revisión encontró seis memorias Meli-scoped y 26 literales de dominio en templates distribuidos; no se maquilló su metadata. `sources.list` ahora excluye las seis notas completas con reglas exactas y verificables, los templates quedaron DEFAULT-neutral y `build-core.py` audita metadata/routing y cuerpos ejecutables de todo el artefacto. El build publicado materializó 44/44 tipos en un vault temporal. Prueba negativa: `area: "[[{{title}}]]"` pasó el análisis pre-render y el gate post-render la rechazó por área inexistente. Export publicado: 189 archivos canónicos, 37 skills, nueve federadas, seis exclusiones scoped y Doctor `0/0/0`.
- **2026-09-14 — PHASE 3.5 implementada y en OWNER REVIEW.** Cero nombres duplicados core↔federado en skills y runbooks; Doctor fuente y export construido `HIGH=0 MEDIUM=0 LOW=0`; export reproducible con 37 skills, incluidas nueve federadas y nueve filas proyectadas; hot path construido sin literales operativos de dominio; registry selftest `0/1/>1 PASS`; COLD DEFAULT/MELI, conflicto fail-closed y swaps cross-domain PASS, con WARN heredados en COLD ARANEA y swaps desde DEFAULT; context-budget selftest 21/21 y suite sin FAIL; canonical-linter selftest 9/9 y CL-21 real PASS. El L0 completo conserva dos FAIL preexistentes (`SCHEMA-VALIDATOR-GREEN`, `LOAD-POLICY-VOCABULARY`) fuera del slice; no se suprimieron.
- **2026-09-14 — Retrieval post-cambio validado con límite explícito.** `graphify-obsidian explain "doctor-verde-falso-por-duplicados-core-federado"` auto-refrescó el índice y resolvió la nota con su nueva sección `Resolución`. El refresh continuó en modo derivado porque el lint corpus-wide está `NO-GO` (`76` fingerprints nuevos frente al baseline 2026-09-09), deuda acumulada previa a este slice y visible para P4-A/higiene; las seis notas nuevas o modificadas que exigen contrato estricto pasaron `ERROR=0 WARN=0`.

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
- El gate de agnosticismo de dominio se ejecuta sobre el artefacto construido, no sólo sobre las fuentes: el export falla si contiene referencias operativas de dominio no allowlisted.
- `[[Personal]]` es el default de templates compartidos porque siempre resuelve en el core distribuido; no implica dominio personal definitivo. En instalaciones con routers, el flujo scoped que crea una entidad de dominio debe ajustar `area`, tags y destino en el mismo cambio o la entidad quedará legítima pero silenciosamente en DEFAULT.
- `agent-development-workflow`, capabilities abstractas, `autonomy envelope` y `delivery checkpoint` quedan fuera de este slice; los dos últimos vuelven sólo con un consumidor concreto.
- El primer Doctor de un core DEFAULT puede devolver OVERALL FAIL por `SCHEMA-VALIDATOR-GREEN`: es un finding real del artefacto distribuido, no un error del agregador. PHASE 4 lo preserva explícitamente; mejorar el onboarding o corregir esa deuda es un slice posterior, no motivo para silenciarla.

## 🔗 Docs / Links

- `80-agents/skills/agents-os-doctor/PHASE-4-AGGREGATION-SPEC.md` — contrato de implementación PHASE 4.
- `80-agents/skills/agents-os-doctor/SKILL.md` — superficie unificada implementada.
- `80-agents/skills/agents-os-doctor/P4-ADVERSARIAL-HANDOFF.md` — challenge externo y comandos de reproducción.
- `80-agents/tools/conformance-harness/` — provider de correctness/contracts.
- `80-agents/tools/context-budget/` — provider de context budget/domain leakage.
- `80-agents/tools/canonical-linter/` — provider de canonical/deprecation.

## ➡️ Next exact

**Owner:** aceptar o rechazar PHASE 4. La implementación y el challenge adversarial están cerrados con veredicto externo `READY` y sin findings abiertos.
