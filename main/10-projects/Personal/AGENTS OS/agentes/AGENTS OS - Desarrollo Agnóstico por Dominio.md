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
start: "2026-09-14"
due:
progress: 0
repo:
jira:
prs:
aliases:
  - AGENTS OS Domain-Scoped Development
  - Desarrollo transversal por dominio
related:
  - "[[AGENTS OS - Conformance Harness]]"
  - "[[meli-agent-dev]]"
  - "[[aranea-agent-dev]]"
  - "[[sdd-workflow]]"
tags:
  - kind/project
  - area/personal
  - project/agents-os
  - tech/agents-os
created: "2026-09-14"
updated: "2026-09-14"
---

# AGENTS OS - Desarrollo Agnóstico por Dominio

> [!info]+ Planificador único
> **Padre:** [[AGENTS OS]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1 · **Progreso:** 0%
> Plan listo para challenge arquitectónico. No hay implementación iniciada ni cambios runtime autorizados antes de G0.

## 🎯 Objetivo

- Incorporar las capacidades valiosas observadas en un developer harness externo —perímetro de autonomía, lifecycle de implementación, gates derivados del riesgo y evidencia fresca— sin importar su tooling ni sus reglas Meli.
- Establecer una conducta transversal de desarrollo agnóstica al dominio; delegar políticas, runbooks y herramientas a los routers scoped existentes de Meli y Aranea; y mantener un fallback DEFAULT estrictamente repo-native.
- Demostrar que eliminar todo el paquete Meli no afecta el núcleo transversal, Aranea ni DEFAULT.

## 📊 Estado actual

- **Planificación completada:** alcance, arquitectura objetivo, decisiones del owner, fases, gates, tareas, prompts y pruebas de aislamiento quedaron documentados; el siguiente paso exacto es F0, challenge adversarial por un agente fresco.
- **Baseline vigente:** bootstrap selecciona explícitamente `meli-agent-dev`, `aranea-agent-dev` o ningún router; ambos routers ya aíslan preferencias y herramientas; Conformance Harness y Context Budget prueban exclusión MELI/ARANEA/DEFAULT, pero la tabla del dominio sigue hardcodeada en bootstrap y tooling.
- **Gap transversal:** no existe una skill genérica que gobierne el ciclo material de desarrollo y una evidencia de delivery ligada al HEAD; `sdd-workflow`, `agents-os-agent-project-workflow` y `agents-os-agent-run-register` cubren responsabilidades vecinas que no deben reemplazarse.
- **Fuente externa:** el bundle `meli-developer` entregado por el owner se considera input de investigación no canónico. Solo se retienen aquí patrones agnósticos; Grimoire, Spellbook, Fury, O11y y cualquier tooling corporativo permanecen exclusivamente en el dominio Meli.
- **Repositorio:** no aplica; esta iteración modifica fuentes canónicas y tooling dentro del vault. El baseline es el estado verificado de los archivos citados, no un commit inexistente.

## 🧠 Síntesis del input externo

| Patrón observado | Decisión para AGENTS OS |
|---|---|
| Autonomía concedida por scope | Adoptar como `autonomy envelope` transversal |
| Lifecycle de implementación y bloqueos tipados | Adoptar reducido; no copiar roles ni estados Grimoire |
| Gates seleccionados por diff/riesgo | Adoptar como contrato abstracto; resolver comandos por dominio/repo |
| Evidencia asociada a base/head SHA | Adoptar como `delivery checkpoint` mutable |
| Consumidores observados y breaking declaration | Reservar para adapter/runbook Meli; no convertir en regla global |
| Mutation testing y thresholds fijos | No adoptar globalmente; solo si el repo o dominio lo exige |
| Routing por Captain/Warrior/Cleric | Descartar; el routing canónico usa intención, entidad, área y capability |
| Spellbook/Grimoire/Fury/O11y/Zord | Prohibidos en la skill transversal, Aranea y DEFAULT |

## 📐 Requerimientos y evidencia

| ID | Requerimiento | Estado | Evidencia vigente / gap |
|---|---|---|---|
| R1 | Una conducta transversal para desarrollo material | `partial` | `VAULT_ROOT/30-resources/agents/skills/sdd-workflow/SKILL.md` y `VAULT_ROOT/80-agents/skills/agents-os-agent-project-workflow/SKILL.md` cubren fases/continuidad, no el ciclo integrado |
| R2 | Exactamente un dominio activo y cero leakage | `done` | `VAULT_ROOT/80-agents/tools/conformance-harness/artifacts/domain-isolation-audit.md`; falta extenderlo al nuevo workflow |
| R3 | Meli y Aranea eligen runbooks/tooling sin contaminar core | `partial` | `VAULT_ROOT/30-resources/agents/skills/meli-agent-dev/SKILL.md` y `VAULT_ROOT/30-resources/agents/skills/aranea-agent-dev/SKILL.md`; falta protocolo abstracto común |
| R4 | DEFAULT funciona sin router ni herramientas de dominio | `done` | `VAULT_ROOT/80-agents/skills/agents-os-bootstrap/SKILL.md`; debe preservarse al agregar desarrollo transversal |
| R5 | Eliminar Meli sin impacto residual | `missing` | Bootstrap y harness nombran Meli explícitamente; falta registry/discovery y deletion test |
| R6 | Evidencia de delivery fresca y ligada al código evaluado | `partial` | La nota de proyecto admite evidencia; `agent_run` mide superficie×modelo y no debe absorber gates |
| R7 | Tooling mecánico vive en runbooks/adapters | `partial` | La frontera skill/runbook existe; los routers actuales rutean principalmente a skills |
| R8 | Ningún aumento del system prompt/always-load | `done` | `VAULT_ROOT/80-agents/agents-os/agent-constitution.md` y bootstrap exigen lazy/scoped; la solución no los amplía con policy de desarrollo |

## 🎯 Scope y non-scope

**Scope:** contrato transversal de desarrollo; `autonomy envelope`; `delivery checkpoint`; resolución de capacidades por router activo; DEFAULT repo-native; evolución metadata-driven del domain gate; alineación mínima de los routers actuales; conformance de aislamiento, fallback y eliminación de un dominio.

**Non-scope:** copiar el harness externo; imponer herramientas o thresholds globales; rediseñar SDD; reemplazar project workflow o `agent_run`; crear tooling Meli dentro del core; modificar repos de aplicaciones; ejecutar PRs, pushes o releases; resolver findings ajenos de Conformance/Doctor; generalizar MCPs de Aranea.

## 🏗️ Arquitectura actual

```text
bootstrap
  ├─ area=Meli   → meli-agent-dev   → una skill Meli
  ├─ area=Aranea/Echo → aranea-agent-dev → una skill/runbook Aranea
  └─ otra/ninguna → sin router       → skill transversal directa

sdd-workflow                  → fases SDD
agent-project-workflow        → continuidad durable
agent-run-register            → telemetría superficie×modelo
repo/CI                       → validación técnica efectiva
```

## 🧭 Arquitectura objetivo

```text
bootstrap → resolver dominio por metadata/registro, sin nombres de dominios en core
  → domain router scoped (0..1; cero significa DEFAULT)
  → agent-development-workflow cuando la intención es implementación material
       → comportamiento transversal: scope, lifecycle, riesgos, gates, evidencia, handoff
       → capability abstracta: validate | security | contract-impact | pre-push | review | release
            → router activo mapea capability a skill/runbook/tooling del dominio
            → DEFAULT usa AGENTS.md + comandos y policy del repo
       → delivery checkpoint ligado a base/head o evidencia equivalente
```

### Dirección de dependencias

```text
core transversal → protocolo abstracto
domain router     → protocolo abstracto + referencias a sus propios runbooks
runbook/adapter   → herramientas concretas
```

El core no referencia `Meli`, `Aranea`, `Spellbook`, `Grimoire`, `Fury`, `O11y`, `Zord`, hosts, MCPs ni paths de dominio. Los routers pueden referenciar el protocolo transversal; el protocolo nunca referencia routers concretos. DEFAULT es ausencia de router, no un tercer pack always-load.

## 🔌 Contratos objetivo

- **Workflow:** recibe `authority`, `scope`, `risk_flags`, `active_domain` y `delivery_state`; opera solo `baseline → implementing → verifying → blocked|review`.
- **Autonomy envelope:** `allowed_repositories`, `allowed_change_types`, `protected_surfaces`, `forbidden_actions`, `approved_exceptions`.
- **Delivery checkpoint:** `base_revision`, `head_revision`, `changed_surfaces`, `validations`, `evidence_status`, `blocking_reasons`, `verified_at`. Un cambio de revisión invalida evidencia; sin VCS se usa identidad verificable equivalente. Vive in-place en el proyecto; logs pesados quedan fuera del vault.
- **Capabilities:** la skill solicita `validate|security|contract-impact|pre-push|review|release`; el router activo responde `skill|runbook|not_available|human_gate`; DEFAULT usa `AGENTS.md` y policy del repo. Una operación estrecha con skill propia puede omitir el workflow.

## 🧱 Decisiones cerradas

| ID | Estado | Resolución | Fuente/evidencia | Fase |
|---|---|---|---|---|
| D1 | `CONFIRMED` | Conducta transversal agnóstica; policy y tooling separados por dominio | Instrucción owner 2026-09-14 | F1 |
| D2 | `CONFIRMED` | Herramientas concretas viven en runbooks/adapters de dominio o repo | Instrucción owner 2026-09-14 | F1-F3 |
| D3 | `CONFIRMED` | Grimoire/Spellbook/Fury/O11y/Zord nunca entran a Aranea, DEFAULT ni core | Instrucción owner 2026-09-14 | F3-F4 |
| D4 | `TECHNICAL_RESOLUTION` | Reutilizar y alinear `meli-agent-dev`/`aranea-agent-dev`; no crear routers paralelos | Baseline verificado | F2-F3 |
| D5 | `TECHNICAL_RESOLUTION` | DEFAULT permanece sin router; el workflow aplica fallback repo-native | Economía de contexto + contrato vigente | F1-F4 |
| D6 | `TECHNICAL_RESOLUTION` | Reemplazar mapping hardcodeado del core por discovery/registro metadata-driven y fail-closed | Invariante de eliminación limpia | F2 |
| D7 | `CONFIRMED` | No agregar policy de desarrollo al system prompt ni always-load | Instrucción owner + constitución | Todas |
| D8 | `CONFIRMED` | Borrar el paquete Meli en el futuro no debe romper core, Aranea ni DEFAULT | Instrucción owner 2026-09-14 | F2-F4 |

## 🧪 Invariantes de aislamiento y escalabilidad

- Exactamente cero o un router de dominio; más de uno falla cerrado.
- El workflow transversal contiene cero identificadores de herramientas o dominios.
- Un adapter de dominio no puede activar skills/runbooks de otro dominio.
- DEFAULT no carga preferencias, skills ni herramientas scoped.
- Eliminar un dominio registrado deja referencias rotas igual a cero y preserva los escenarios restantes.
- Agregar un nuevo dominio requiere adapter + metadata + tests, sin editar la semántica del workflow transversal.
- Capability ausente produce `not_available` o `human_gate`, nunca fallback silencioso a otra herramienta.
- Las reglas del repo pueden endurecer defaults; ninguna capa reduce una regla superior sin decisión auditable.

## 🛠️ Paquetes autónomos

### Paquete autónomo Fase 0 — Challenge adversarial y freeze contractual

**Misión exacta:** intentar refutar DEFAULT sin router, discovery metadata-driven, dependencias y remove-Meli. **Precondiciones verificables:** planner creado, runtime intacto, G0 `pending`. **Lectura obligatoria:** este proyecto; `VAULT_ROOT/80-agents/skills/agents-os-bootstrap/SKILL.md`; routers; domain audit; note types. **Decisiones cerradas:** D1-D8 son baseline desafiable con evidencia.
**Implementación paso a paso:** threat model; verificar selector workflow/router/runbook; simular add/remove domain; revisar SDD/project workflow/agent run; registrar `ACCEPT|AMEND|REJECT`. **Archivos esperados:** solo este planner y artifact opcional. **No tocar:** runtime, memoria, repos. **Spikes permitidos:** Graphify/read-only/`--no-live`. **Tests y asserts:** refs y validator verdes, cero tooling cruzado. **Entregables/Gate G0:** challenge + contrato reconciliado en `review`. **Handoff a Fase 1:** decisiones/file map tras aceptación owner.

### Paquete autónomo Fase 1 — Workflow transversal y checkpoint

**Misión exacta:** skill lean + autonomy/checkpoint sin tooling de dominio. **Precondiciones verificables:** G0 `accepted`. **Lectura obligatoria:** este contrato; `VAULT_ROOT/80-agents/skills/agents-os-skill-authoring/SKILL.md`; project workflow; agent run. **Decisiones cerradas:** D1-D3/D5/D7; agent run no absorbe delivery.
**Implementación paso a paso:** materializar workflow; definir lifecycle/capabilities; agregar checkpoint retrocompatible; actualizar índice/log. **Archivos esperados:** `create: 80-agents/skills/agent-development-workflow/SKILL.md`; modificar workflow/template/registros mínimos. **No tocar:** bootstrap, routers, SDD, repos. **Spikes permitidos:** fixture legacy; nuevo note type exige volver a G0. **Tests y asserts:** schema/lint/Doctor, skill lean, legacy válido, cero términos de dominio. **Entregables/Gate G1:** workflow/checkpoint en `review`. **Handoff a Fase 2:** contrato y evidencia.

### Paquete autónomo Fase 2 — Domain gate extensible

**Misión exacta:** resolver 0..1 router por metadata/registro sin nombres de dominio en core. **Precondiciones verificables:** G1 `accepted`. **Lectura obligatoria:** `VAULT_ROOT/80-agents/skills/agents-os-bootstrap/SKILL.md`; conformance rules; context budget; D4-D6/D8. **Decisiones cerradas:** cero=DEFAULT, múltiples=fail-closed, cero markers específicos.
**Implementación paso a paso:** definir metadata; migrar routers; reemplazar tabla/markers hardcodeados; preservar cold/warm/swap. **Archivos esperados:** bootstrap, contrato metadata autorizado, routers y transcripciones de tests. **No tocar:** runbooks/prefs/workflow semantics. **Spikes permitidos:** registry vs Graphify con fallback determinista. **Tests y asserts:** paridad de tres rutas y ambigüedad cerrada. **Entregables/Gate G2:** gate extensible + compatibility matrix en `review`. **Handoff a Fase 3:** protocolo/fixtures.

### Paquete autónomo Fase 3 — Adapters y runbooks por dominio

**Misión exacta:** routers scoped mapean capabilities a skills/runbooks propios. **Precondiciones verificables:** G2 `accepted`. **Lectura obligatoria:** `VAULT_ROOT/30-resources/agents/skills/meli-agent-dev/SKILL.md`; `VAULT_ROOT/30-resources/agents/skills/aranea-agent-dev/SKILL.md`; prefs y contrato F1. **Decisiones cerradas:** D2-D5; no duplicar core ni llenar vacíos.
**Implementación paso a paso:** inventariar; mapear `skill|runbook|not_available|human_gate`; extraer solo comandos mecánicos; documentar DEFAULT repo-native. **Archivos esperados:** routers, runbooks mínimos e índices. **No tocar:** core salvo conflicto; cero tooling Meli en Aranea/DEFAULT y cero MCP Aranea en Meli/DEFAULT. **Spikes permitidos:** unknown=`not_available`, sin sustitución cross-domain. **Tests y asserts:** resolución exclusiva y carga mínima. **Entregables/Gate G3:** adapters/matriz en `review`. **Handoff a Fase 4:** fixtures negativos.

### Paquete autónomo Fase 4 — Conformance, eliminación y entrega

**Misión exacta:** demostrar aislamiento, add-domain y remove-Meli. **Precondiciones verificables:** G3 `accepted`. **Lectura obligatoria:** `VAULT_ROOT/80-agents/tools/conformance-harness/artifacts/conformance-spec-v1.md`; providers e invariantes. **Decisiones cerradas:** D3/D5/D7/D8 son gates físicos.
**Implementación paso a paso:** escenarios workflow/profile; adapter ficticio; eliminación Meli en copia temporal; Doctor/providers/context delta. **Archivos esperados:** providers/tests/docs mínimos. **No tocar:** Meli real, proyecto Conformance entregado, findings ajenos. **Spikes permitidos:** temp deletion; live solo autorizado. **Tests y asserts:** core sin términos de dominio, 0 leaks, add sin core edit, remove preserva Aranea/DEFAULT, cero deuda nueva. **Entregables/Gate G4:** evidencia/rollback en `review`. **Handoff final:** owner acepta/rechaza.

## 🚦 Gate control

| Gate | Estado | Responsabilidad del agente | Evidencia de aceptación owner | Habilita |
|---|---|---|---|---|
| G0 | `pending` | Challenge adversarial y freeze | Owner acepta decisiones reconciliadas | F1 |
| G1 | `pending` | Workflow/checkpoint en `review` | Owner acepta contrato transversal | F2 |
| G2 | `pending` | Domain gate extensible en `review` | Owner acepta paridad y registry | F3 |
| G3 | `pending` | Adapters/runbooks en `review` | Owner acepta matriz y aislamiento | F4 |
| G4 | `pending` | Conformance final en `review` | Owner acepta entrega | Cierre |

## ✅ Tareas

- [ ] T0.1 Ejecutar challenge de arquitectura, leakage, fallback DEFAULT y eliminación Meli #owner/agent #type/research #area/personal
- [ ] T0.2 Reconciliar findings, decisiones y file map; dejar G0 Review #owner/agent #type/admin #area/personal
- [ ] T1.1 Materializar la skill transversal lean y sus aliases/capabilities #owner/agent #type/dev #area/personal
- [ ] T1.2 Implementar autonomy envelope y delivery checkpoint retrocompatibles #owner/agent #type/dev #area/personal
- [ ] T1.3 Validar schema/lint/Doctor/legacy y dejar G1 Review #owner/agent #type/testing #area/personal
- [ ] T2.1 Resolver contrato metadata/registry para domain routers #owner/agent #type/dev #area/personal
- [ ] T2.2 Reemplazar hardcode core preservando cold/warm/swap/default #owner/agent #type/dev #area/personal
- [ ] T2.3 Actualizar fixtures/providers y dejar G2 Review #owner/agent #type/testing #area/personal
- [ ] T3.1 Mapear capabilities reales de Meli sin mover tooling al core #owner/agent #type/dev #area/personal
- [ ] T3.2 Mapear capabilities reales de Aranea y DEFAULT sin sustitución cross-domain #owner/agent #type/dev #area/personal
- [ ] T3.3 Extraer solo runbooks mecánicos necesarios y dejar G3 Review #owner/agent #type/dev #area/personal
- [ ] T4.1 Agregar conformance de workflow/profile y dominio ficticio #owner/agent #type/testing #area/personal
- [ ] T4.2 Ejecutar simulación remove-Meli y medir aislamiento/contexto #owner/agent #type/testing #area/personal
- [ ] T4.3 Consolidar rollback/evidencia y dejar G4 Review #owner/agent #type/admin #area/personal

## 🤖 Prompt común del executor

Trabaja solo la fase asignada de `[[AGENTS OS - Desarrollo Agnóstico por Dominio]]`. La nota es el planificador único. Lee únicamente su paquete, las fuentes obligatorias y el delta necesario. Preserva cambios ajenos. No mezcles dominios, no inventes capabilities ni herramientas, no cargues dos routers y no agregues policy al startup. Actualiza tareas/estado/bitácora durante el trabajo. Un executor deja su gate en `review`; solo el owner lo acepta. Ante contradicción ejecutable, registra `PLAN_CONFLICT` y detente.

**Despacho Fase 0**
`FASE_ASIGNADA=0 · PAQUETE_CANONICO=Fase 0 — Challenge adversarial y freeze contractual · GATE_REQUERIDO=none · TAREAS=T0.1-T0.2 · SALIDA=challenge + decisiones reconciliadas · STOP=G0 review; no runtime edits`

**Despacho Fase 1**
`FASE_ASIGNADA=1 · PAQUETE_CANONICO=Fase 1 — Workflow transversal y checkpoint · GATE_REQUERIDO=G0 accepted · TAREAS=T1.1-T1.3 · SALIDA=skill + checkpoint + validación · STOP=G1 review`

**Despacho Fase 2**
`FASE_ASIGNADA=2 · PAQUETE_CANONICO=Fase 2 — Domain gate extensible · GATE_REQUERIDO=G1 accepted · TAREAS=T2.1-T2.3 · SALIDA=registry/domain gate + paridad · STOP=G2 review`

**Despacho Fase 3**
`FASE_ASIGNADA=3 · PAQUETE_CANONICO=Fase 3 — Adapters y runbooks por dominio · GATE_REQUERIDO=G2 accepted · TAREAS=T3.1-T3.3 · SALIDA=capability maps + runbooks mínimos · STOP=G3 review`

**Despacho Fase 4**
`FASE_ASIGNADA=4 · PAQUETE_CANONICO=Fase 4 — Conformance, eliminación y entrega · GATE_REQUERIDO=G3 accepted · TAREAS=T4.1-T4.3 · SALIDA=evidencia isolation/add/remove + rollback · STOP=G4 review`

## 📆 Bitácora

- **2026-09-14 — Validación:** `validate_plan.py` PASS (`phases=5/gates=5/dispatches=5/refs=10/errors=0/warnings=0`); lint strict de los tres archivos tocados `ERROR=0/WARN=0`; schema `project` y `change_log` verdes; Graphify reindexó y resolvió el nodo exacto. Doctor global reportó `HIGH=0/MEDIUM=13/LOW=0` por skills ausentes de `INDEX.md`; el gate global de Graphify mantiene deuda ajena `ERROR=64/WARN=27`; no se corrigieron por scope.
- **2026-09-14** — Proyecto creado desde el harness externo y corregido por el owner: la intención no es importar una policy Meli, sino extraer capacidades agnósticas. Se verificó que AGENTS OS ya posee routers exclusivos `meli-agent-dev` y `aranea-agent-dev`, DEFAULT sin router y conformance de aislamiento. El plan propone una skill transversal, mappings de capabilities en routers scoped, herramientas solo en runbooks/adapters y domain discovery sin nombres hardcodeados para que Meli pueda eliminarse sin impacto. Queda listo para F0 challenge por un agente fresco; cero runtime modificado.

## 🔗 Fuentes

- `VAULT_ROOT/80-agents/skills/agents-os-bootstrap/SKILL.md` — startup y domain gate vigente.
- `VAULT_ROOT/30-resources/agents/skills/meli-agent-dev/SKILL.md` — router Meli vigente.
- `VAULT_ROOT/30-resources/agents/skills/aranea-agent-dev/SKILL.md` — router Aranea vigente.
- `VAULT_ROOT/80-agents/tools/conformance-harness/artifacts/domain-isolation-audit.md` — evidencia de aislamiento y gaps.
- `VAULT_ROOT/80-agents/skills/agents-os-agent-project-workflow/SKILL.md` — continuidad durable.
- `VAULT_ROOT/30-resources/agents/skills/sdd-workflow/SKILL.md` — fases SDD existentes.
- `VAULT_ROOT/80-agents/skills/agents-os-agent-run-register/SKILL.md` — telemetría que no debe mezclarse con delivery.
- Source bundle `meli-developer` — input externo no canónico entregado por el owner; sus mecanismos reutilizables están sintetizados en este planner.

## ⚠️ Riesgos y rollback

- **Riesgos:** crear un segundo router; inflar startup; usar metadata no resoluble sin Graphify; romper DEFAULT; duplicar SDD; mezclar delivery y performance; dejar referencias Meli en core; convertir runbooks en policy; falsa eliminación basada solo en grep.
- **Rollback:** cada fase es independiente y requiere gate owner. Revertir solo archivos de la fase; preservar el router/domain gate previo hasta G2; mantener proyectos legacy sin checkpoint; ejecutar conformance antes y después; no borrar adapters reales durante pruebas.

## ✅ Definition of Done

- Skill transversal lean, lazy y sin nombres/herramientas de dominio.
- Routers scoped resuelven capabilities hacia runbooks propios sin duplicar conducta transversal.
- DEFAULT opera con reglas y herramientas del repo sin cargar paquetes Meli/Aranea.
- Evidencia de delivery se invalida al cambiar la identidad del código evaluado.
- Agregar un dominio no cambia el core; retirar Meli no rompe core, Aranea ni DEFAULT.
- Conformance, context budget, schema, lint y Doctor quedan sin deuda nueva.
- Todos los gates G0-G4 son aceptados por el owner y la tarea puente queda lista para cierre humano.
