---
type: project
schema_version: 1
owner: me
root: true
cssclasses:
  - wide
status: active
priority: P0
area: "[[Echo]]"
parent:
sprint:
start: 2026-09-23
due:
progress: 5
repo: xKoRx/symphony
jira:
prs:
aliases:
  - Echo Forge Primera Campaña Real
  - Echo Forge Campaign 001
  - Echo Forge Real Operations
tags:
  - kind/project
  - area/echo
  - priority/p0
created: "2026-09-23"
updated: "2026-09-23"
---

# Echo Forge — Operación Real V2

> [!info]+ Echo Forge — Operación Real V2
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P0
> Proyecto sucesor de [[Echo Forge]]. Su primer horizonte es ejecutar y certificar la **Primera Campaña Real** con estrategias auténticas, iterar el funnel con revisión humana y cerrar con la nueva Integration V2 Forge→Echo compatible con el nuevo The Lab.

## 🎯 Objetivo

- Pasar Echo Forge desde “fábrica construida y certificada técnicamente” a **fábrica operada y validada con estrategias reales**.
- Certificar por separado lo que el owner necesita confiar personalmente: ingestión/import, evidencia extraída desde SQX, Classification, Ranking, Selection y validación profunda SQX/MT5.
- Tratar la revisión humana del owner como evidencia formal de producto: si técnicamente PASS pero el ranking/selection no representa estrategias que Rodrigo considera razonables, el gate es **STAGE_ITERATE**, no PASS.
- Versionar cualquier cambio de algoritmo/config para poder comparar cohorte, inputs, ranking, selection y resultados entre versiones.
- Construir **Integration V2 Forge→Echo** recién cuando la campaña real haya demostrado qué información necesita realmente Echo/The Lab.
- Cerrar este proyecto cuando una campaña real complete Forge → Echo → The Lab con linaje, evidencia y resultados inspeccionables.

## 📊 Estado actual

- **Foundation cerrada:** [[Echo Forge]] = completed / FOUNDATION COMPLETE.
- **Import cerrado:** [[Echo Forge — Import Task V1]] = G7 físico PASS, integrado a master.
- **Campaña B integrada:** resolver `selection_cohort` y pipeline SelectionSnapshot→SQX/MT5 ya están en master; [[Echo Forge — Campaña B]] deja de ser planner activo y se absorbe como gate C6.
- **Baseline operativo vigente:** **CONSOLIDACIÓN FINAL DEL REPO COMPLETA (2026-09-23): `master` = `origin/master` = `d9032ff8c5ee0f5f5d68d70994a9f4dc660e33aa`.** Repo con una única rama local y remota, sin worktrees residuales, sin tags `archive/*`, sin PRs, sin material preservado pendiente y con todo desarrollo vigente/aceptado contenido en master (cero pendientes). El gate integró el delta post-cert A1 (`archive/f05-post-cert-delta`: fix F-INT-04 de handoff, pin de contracts a `5dd998f`, refresh de release matrix, stdout puro en flowkit vía sdk `c7f11496`) y resolvió con evidencia las líneas archivadas restantes: atestación E-06 y magic-width R3 = SUPERSEDED (refutadas como comportamiento V1 por los artefactos certificados de V2: XML `<type>int</type>` + `input int` con magics >int32, 0 errores MetaEditor, cadena CERT-F04-01/02), Forge Explorer v0 = SUPERSEDED_BY_FLOWKIT, material `preserved/` = resuelto y eliminado. Campaign 001 queda desbloqueada: C0 debe usar `d9032ff8` como baseline exacto y revalidar el runtime desplegado antes de iniciar (el RC 0.2.106 actual fue construido desde `d07cc69`, sin este delta).
- **Integración histórica superseded:** el boundary Forge→Echo V1 no se termina por inercia. The Lab cambió y también cambió la forma de inyectar/consumir datos. Integration V2 se especifica en C8 usando necesidades reales observadas.
- **Modo de trabajo:** desde este proyecto, bugs/findings de campaña se corrigen en branches cortas y vuelven rápido a master tras test + review; no se acumulan nuevas ramas históricas largas.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | branch corta por finding/stage; master como baseline aceptado | master verificado al iniciar cada stage | este proyecto + SPEC del stage | contrato/spec técnica vigente de Forge | **C0 pendiente: fijar baseline operacional exacto** |
| xKoRx/echo | se abre en C8 | master vigente al iniciar C8 | Integration V2 derivada de Campaign 001 | nueva SPEC Forge→Echo→The Lab | **DEFERRED hasta C8** |

## 🧭 Horizonte de certificación — Primera Campaña Real

Cada gate termina en uno de estos estados:

- **STAGE_PASS** — capacidad aceptada y su salida puede ser baseline del siguiente stage.
- **STAGE_ITERATE** — el sistema funciona pero el resultado de producto no es aceptable; se formula hipótesis, se versiona el cambio y se re-ejecuta.
- **STAGE_BLOCKED** — falta evidencia, entorno o una decisión material.

| Gate | Capacidad a certificar | Evidencia mínima |
|---|---|---|
| **C0 — Operational Baseline** | master/runtime contienen todo lo necesario para operar la campaña | SHA master + release/runtime + build/regresión + branches/worktrees saneados |
| **C1 — Import Real** | Watcher Import introduce una cohorte auténtica sin pérdida ni drift de identidad | N/N artifacts, hashes, refs, FlowRun, replay/idempotencia, inspección owner |
| **C2 — SQX Evidence Trust** | los datos que Forge extrae de SQX representan realmente la estrategia | muestra comparada contra SQX GUI/report: métricas, trades y campos críticos |
| **C3 — Classification** | las clases/tipos producidos tienen significado útil en estrategias reales | distribución + ejemplos por clase + casos frontera + revisión owner |
| **C4 — Ranking** | ranking por tipo/global ordena estrategias de forma útil y explicable | top/bottom/fronteras + métricas/pesos/versiones + revisión owner |
| **C5 — Selection** | la política selecciona un cohort que merece validación cara | selected vs rejected + falsos positivos/negativos + SelectionSnapshot aceptado |
| **C6 — Deep Validation / Campaña B** | los seleccionados sobreviven validación OOS + MT5 física | SelectionSnapshot→SQX Tick Retest→MT5 export/compile/real-tick backtest→reconcile/fidelity |
| **C7 — Funnel Iteration** | Classification/Ranking/Selection convergen a un baseline aceptado | comparación vN→vN+1 sobre cohortes comparables + owner acceptance |
| **C8 — Integration V2 Forge→Echo** | Forge entrega exactamente la evidencia que Echo/The Lab requiere | nuevo contrato congelado + ingest/normalización + QA E2E |
| **C9 — First Integrated Campaign** | una campaña real completa Forge→Echo→The Lab | linaje completo, evidence refs, resultados inspeccionables y aceptación owner |

## 🔬 Protocolo obligatorio por gate

1. **Freeze:** cohorte, config, algoritmos/versiones, baseline de código y objetivo del gate.
2. **Execute:** correr sólo la capacidad que se está evaluando.
3. **Evidence packet:** entregar artifacts, números, ejemplos y discrepancias; no sólo “PASS”.
4. **Owner review:** C2–C7 requieren revisión explícita de Rodrigo sobre casos reales.
5. **Verdict:** STAGE_PASS / STAGE_ITERATE / STAGE_BLOCKED.
6. **Iteration:** un desacuerdo no se racionaliza para pasar; se convierte en hipótesis falsable, cambio versionado y re-ejecución comparable.
7. **Promote:** sólo una salida aceptada se usa como input durable del siguiente gate.

## 🎯 Qué revisar personalmente en cada etapa

### C2 — SQX Evidence Trust

- ¿las métricas que Forge persiste coinciden con lo que ves en SQX?
- ¿las listas de trades y períodos corresponden a la estrategia correcta?
- ¿hay campos críticos ausentes, transformados o ambiguos?
- ¿qué datos de SQX resultan realmente útiles para juzgar calidad?

C2 debe producir una lista explícita de **campos confiables**, **campos dudosos** y **campos faltantes**.

### C3 — Classification

- distribución por tipos;
- estrategias representativas de cada clase;
- casos que parecen mal clasificados;
- si la clasificación ayuda realmente al ranking o sólo agrega complejidad.

Una clasificación técnicamente consistente pero inútil para decidir estrategias = STAGE_ITERATE.

### C4 — Ranking

Para cada logical type y global:

- Top N;
- Bottom N;
- casos alrededor del cutoff;
- métricas que explican su posición;
- pesos/normalización;
- sensibilidad ante cambios razonables.

Registrar explícitamente **AGREE / DISAGREE / UNCERTAIN**. Los DISAGREE alimentan hipótesis para vN+1.

### C5 — Selection

- revisar seleccionados;
- revisar rechazados cercanos al cutoff;
- registrar falsos positivos/negativos;
- aceptar sólo un SelectionSnapshot que el owner esté dispuesto a someter a Campaña B.

### C6 — Deep Validation / Campaña B

SelectionSnapshot → SQX Tick Retest OOS → MT5 Export → Compile → Real-Tick Backtest → Reconcile/Fidelity → resultado durable.

La comparación clave es qué predijo C4/C5, qué sobrevivió C6 y qué métricas tempranas anticipaban éxito/fracaso. Eso alimenta C7.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [/] **C0** Revalidar master/release/runtime y dejar baseline operacional único para Campaign 001 #owner/me #type/dev #area/echo #urgent
> - [ ] **C1** Definir Cohort 001 y ejecutar Watcher Import con estrategias reales #owner/me #type/dev #area/echo
> - [ ] **C2** Auditar personalmente evidencia SQX vs GUI/report y congelar campos confiables #owner/me #type/research #area/echo
> - [ ] **C3** Revisar Classification real y aceptar/iterar sus clases #owner/me #type/research #area/echo
> - [ ] **C4** Revisar Ranking real: top/bottom/cutoffs/explicaciones y aceptar o iterar scoring #owner/me #type/research #area/echo
> - [ ] **C5** Revisar Selection real: selected/rejected/falsos positivos-negativos y aceptar SelectionSnapshot #owner/me #type/research #area/echo
> - [ ] **C6** Ejecutar Campaña B sobre el SelectionSnapshot aceptado (SQX tick OOS → MT5 real ticks) #owner/me #type/dev #area/echo
> - [ ] **C7** Iterar Classification/Ranking/Selection hasta baseline empírico aceptado #owner/me #type/research #area/echo
> - [ ] **C8** Diseñar e implementar Integration V2 Forge→Echo según necesidades observadas del nuevo The Lab #owner/me #type/dev #area/echo
> - [ ] **C9** Ejecutar primera campaña integrada Forge→Echo→The Lab y cerrar el proyecto #owner/me #type/dev #area/echo

## 📆 Bitácora

- **2026-09-23** — Proyecto creado por decisión del owner. Echo Forge deja de desarrollarse en abstracto y pasa a certificarse operando estrategias reales. El foco explícito del owner es revisar personalmente datos extraídos de SQX, Classification, Ranking y Selection; iterar algoritmos cuando el resultado no represente su criterio; someter seleccionados a validación SQX/MT5; y recién después construir Integration V2 con Echo/The Lab.

## 🧭 Decisiones

- **R1 — Real campaign = product authority.** Los tests certifican contratos y regresiones; no certifican por sí solos la utilidad del algoritmo.
- **R2 — Human review es gate formal.** C2–C7 requieren aceptación explícita del owner; técnicamente verde puede terminar en STAGE_ITERATE.
- **R3 — Versionar el funnel.** Cambios de métricas, pesos, thresholds, clasificación, ranking o selection quedan versionados junto con cohort/config/output.
- **R4 — Campaña B deja de ser proyecto independiente.** Su capacidad `selection_cohort` y pipeline SQX/MT5 viven en C6.
- **R5 — Integration V1 superseded.** C8 construye Integration V2 desde necesidades reales observadas.
- **R6 — Límites de autoridad.** Forge produce y valida estrategias/evidencia; Echo ingiere y normaliza; The Lab construye análisis/curvas/portfolios según su contrato vigente.
- **R7 — Branches cortas.** Findings de campañas reales → branch acotada → implementación → verificación independiente → master. No acumular ramas largas.
- **R8 — No optimizar antes de observar.** No crear dashboards, feedback automation o nuevos scores antes de que C2–C5 demuestren una necesidad concreta.

## 🔗 Docs / Links

- Predecesor: [[Echo Forge]]
- Import certificado: [[Echo Forge — Import Task V1]]
- Capacidad Campaña B: [[Echo Forge — Campaña B]]
- Área: [[Echo]]
- Repos: `xKoRx/symphony` · `xKoRx/echo`
- Symphony specs: `FEAT-SQX-IMPORT-TASK-V1` · `FEAT-SQX-IMPORT-CAMPAIGN-B` · `FEAT-SQX-CROSS-FLOWRUN-REUSE`

## 💡 Ideas

### Backlog de ideas

- Dataset de evaluación “owner judgment vs Forge ranking/selection” sólo después de C4/C5, cuando sepamos qué información es útil.
- Reporte comparativo de versiones de scoring sobre la misma cohorte congelada.
- Métricas de precisión del funnel usando C6 como outcome posterior, una vez exista suficiente muestra.

### Motivos / principios

- El producto no está “certificado” porque un agente pueda extraer datos; está certificado cuando podemos confiar en esos datos y el funnel toma decisiones útiles sobre estrategias reales.
- La primera campaña debe producir casos de regresión, criterios de producto y evidencia para Integration V2.
