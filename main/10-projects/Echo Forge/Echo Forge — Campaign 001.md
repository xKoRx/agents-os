---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P0
area: "[[Echo]]"
parent: "[[Echo Forge — Operación Real V2]]"
sprint:
start: 2026-09-23
due:
progress: 0
repo: xKoRx/symphony
jira:
prs:
aliases:
  - Echo Forge Campaign 001
  - Campana 001
tags:
  - kind/project
  - area/echo
created: "2026-09-23"
updated: "2026-09-23"
---

# Echo Forge — Campaign 001

%% Naming: Echo Forge — Campaign 001 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — Campaign 001
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P0 · **Repo:** `xKoRx/symphony`
> Primera campaña real de [[Echo Forge — Operación Real V2]]: ejecutar el primer cohort real de estrategias end-to-end. Subproyecto de agente — tarea puente en el padre.

## 🎯 Objetivo

- Ejecutar el primer cohort real de estrategias end-to-end: **Import → Classification → Ranking → Selection → revisión humana → Campaña B (SelectionSnapshot durable) → SQX Tick → MT5 → análisis del resultado.** Guardar como evidencia durable: cohort, configuración, algorithm versions, ranking, selection, revisión humana, resultado Campaña B, supervivencia SQX/MT5 y findings. NO automatizar feedback humano en esta primera campaña: la revisión del selection es una parada humana explícita.

## 📊 Estado actual

- **CREATED (2026-09-23, mandato manager).** Prerrequisitos verificados en la misma ventana: Watcher Import intake con G7 PASS físico integrado en master (`9a69243`); resolver `selection_cohort` de Campaña B (CB-G2 @ `dc151e4`) integrado a master con gate 4/4; master consolidado `d07cc69`; RC 0.2.106 publicada en MinIO con binarios `vcs.revision=d07cc69, vcs.modified=false`. Pendiente de owner antes de la etapa B: CB-G1 (review manager + NORMAL) y freeze §3 (período OOS, tick model, parámetros MT5, criterios A-vs-B) — la etapa Import→Selection NO está bloqueada por eso.
- **NEXT EXACT: procesar el primer cohort real mediante Watcher Import.** El owner deposita `flow.json` + `*.cfx` + `import/*.sqx` en el watch_dir; el watcher congela, publica el paquete bajo `watcher.import.folder` y dispara el FlowRun con `Origin: watcher_import`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `master` @ `d07cc69` (origin) | RC 0.2.106 desplegable | Este proyecto (campaña real 001; sin código nuevo previsto — operar lo certificado) | `specs/FEAT-SQX-IMPORT-TASK-V1/SPEC.md` (intake) · `specs/FEAT-SQX-IMPORT-CAMPAIGN-B/SPEC.md` (§2.1 selection_cohort) | **OPERACIÓN — sin feature branch; defectos materiales abren fix sobre master** |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. %%
> - [ ] C1: owner define y deposita el cohort real en el watch_dir (`flow.json` + `*.cfx` + `import/*.sqx`) #owner/me #type/dev #area/echo
> - [ ] C2: Watcher Import intake — freeze doble-hash, publicación MinIO, FlowRun `watcher_import` COMPLETED con cohort durable #owner/agent #type/dev #area/echo
> - [ ] C3: Classification → Ranking → Selection sobre el cohort real; snapshots por ref exacta #owner/agent #type/dev #area/echo
> - [ ] C4: revisión humana del selection (parada explícita; NO automatizar) — owner ratifica o rechaza finalists #owner/me #type/pr-review #area/echo
> - [ ] C5: Campaña B desde SelectionSnapshot durable (`selection_cohort.snapshot_ref`) — SQX Tick Retest OOS → MT5 Export → Compile → Real-Tick Backtest → Reconcile/Fidelity → Final Decision/Report #blocked (CB-G1 + freeze §3 del owner) #owner/agent #type/dev #area/echo
> - [ ] C6: análisis del resultado — supervivencia SQX/MT5, fidelity, findings; comparación contra evidencia de la campaña de origen por refs #owner/agent #type/research #area/echo
> - [ ] C7: guardar el paquete de evidencia completo: cohort, config, algorithm versions, ranking, selection, revisión humana, resultado Campaña B, supervivencia, findings (MinIO + refs en esta nota) #owner/agent #type/admin #area/echo
> - [ ] C8: reporte de campaña + cierre en Agents-OS; hallazgos alimentan Track B (FUNNEL QUALITY) de [[Echo Forge — Operación Real V2]] #owner/me #type/admin #area/echo

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-23** — Proyecto creado por mandato manager. Master consolidado @ `d07cc69`, RC 0.2.106 publicada (binario auténtico `d07cc69`), pipeline completo disponible en producción. Siguiente exacto: C1 (owner deposita cohort real) → C2 Watcher Import.

## 🧭 Decisiones

- **D-C1-1 (2026-09-23): operar sobre master, sin feature branch.** La campaña usa el producto certificado (RC 0.2.106); sólo un defecto material observado en operación abre fix sobre master.
- **D-C1-2 (2026-09-23): revisión humana entre Selection y Campaña B es obligatoria y manual** (mandato: no automatizar feedback humano en la primera campaña).
- **D-C1-3 (2026-09-23): la etapa B de esta campaña hereda los gates de [[Echo Forge — Campaña B]]** (CB-G1 review + freeze §3 owner); el resto del funnel (Import→Selection) no está bloqueado por ellos.

## 🔗 Docs / Links

- Parent: [[Echo Forge — Operación Real V2]] · Predecesores: [[Echo Forge — Import Task V1]] · [[Echo Forge — Campaña B]]
- Entidad: [[echo-forge]] · Intake: `watcher.import` (SPEC FEAT-SQX-IMPORT-TASK-V1) · Entrada B: `selection_cohort` (SPEC FEAT-SQX-IMPORT-CAMPAIGN-B §2.1)
