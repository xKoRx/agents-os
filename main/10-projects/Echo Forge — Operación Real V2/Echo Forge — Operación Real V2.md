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
updated: "2026-09-24"
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
- **Fase 1 Shot 1 (2026-09-24/25):** baseline operacional = **release 0.2.107 desde `d9032ff8`** (commit release `6482173`); runtime flota 0.2.107 verificado 3/3. **CORRECCIÓN DE MANDATO (2026-09-25): Cohort 001 = 727 estrategias NDX H1 LONG de Zeus/Retester/"in retest cross"** (la interpretación previa 11 XAUUSD running portfolio quedó `INVALIDATED_AS_COHORT001_BY_OWNER`); grupo resuelto **BR_G1** (`Build_BR_G1_H1.cfx`, `STRONGLY_CORROBORATED` por cobertura 15/15 del universo de bloques de las 727; el Builder ACTUAL == plantilla G4, estado posterior que no originó la cohorte — divergencia documentada para decisión owner). C1 = CANDIDATE: 727/727 publicados+adoptados, manifest sellado 727/727 SHA verificado, FlowRun `1a4d66d6`, wave técnica `wave1b`. C2 = BLOCKED_EXTERNAL: licencia flota RENOVADA 2026-09-24 21:37 local pero las GUI SQX del owner abiertas en 3/3 hosts impiden `sqcli` CLI (single-instance) ⇒ enriquecimiento en retry. Findings abiertos: go.work.sum (SHOT2/SHOT3); deployer/watcher sin supervisión durable (BEFORE_C6); deadline del import_intake no alcanza para cohorts grandes + watchdog auto-upgrade mata binarios candidate-local (fix en rama `fix/watcher-import-intake-deadline` pusheada, 2 knobs con defaults intactos — review owner). Detalle: `~/aranea/work/forge-shot1-cohort001-fix-20260925/EVIDENCE-COHORT001-FIX.md` y `forge-shot1-20260924/EVIDENCE-SHOT1.md`.
- **Prework ambiente Fase 1 (2026-09-24, corrección del owner): `PREWORK_DAEDALUS_SQX_LICENSE = SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION` — la licencia SQX en Daedalus ya no es blocker.** El owner corrigió el modelo de ambientes ([[Echo + Echo Forge — Environment Contract]] §0): **Echo Forge tiene un único ambiente operacional** —actualmente configurado como production, con flota SQX Zeus/Hera/Kronos + worker Windows Kronos— y sus pruebas físicas, campañas y certificaciones se ejecutan allí; no existe obligación de SQX/worker/licencia DEV en Daedalus ni de `dev-win`, y `ENV=production` de Forge es el ambiente canónico, no un defecto. Campaign 001 no requiere SQX local en Daedalus: se ejecuta usando el runtime operacional Forge existente según la capacidad que cada stage requiera. Las tres sesiones de prework del 2026-09-24 se conservan en Bitácora como investigación realizada bajo una premisa de ambiente posteriormente corregida. Estado resultante del prework: **`PREWORK_REQUIRES_RUNTIME_REVALIDATION`** — la infraestructura operacional está lista (flota operable y certificada; G7 físico PASS sobre Kronos) y la única revalidación pendiente (runtime desplegado RC 0.2.106 @ `d07cc69` vs baseline `d9032ff8`) pertenece a C0, primer hito de Fase 1; no se abre otro prework. `PREWORK_MT5 = DEFERRED_UNTIL_C6` se mantiene por alcance de stage (C0–C2 sólo requieren SQX), no por ambiente. Dinero real intacto: “Forge production” ≠ autorización económica. **NEXT EXACT: iniciar Shot 1 de Fase 1 de Echo Forge — Operación Real V2 sobre el ambiente operacional Forge canónico. Shot 1 trabaja el milestone único C0+C1+C2. No avanzar C3.**

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
> - [x] **C0** Revalidar master/release/runtime y dejar baseline operacional único para Campaign 001 #owner/me #type/dev #area/echo #urgent — DONE candidate 2026-09-24/25: release 0.2.107 @ d9032ff8 publicada+rollout 3/3; commit 6482173
> - [/] **C1** Definir Cohort 001 y ejecutar Watcher Import con estrategias reales #owner/me #type/dev #area/echo — C1 CANDIDATE PASS 2026-09-25 bajo CORRECCIÓN DE MANDATO: Cohort 001 = 727 NDX H1 LONG (Zeus/Retester/"in retest cross", BR_G1 resuelto por Building Blocks), 727/727 publicados+adoptados con manifest sellado verificado, FlowRun `1a4d66d6` (wave1b); FlowRun previo `f87fde30` = INVALIDATED_AS_COHORT001_BY_OWNER. Pendiente: enriquecimiento sqcli (espera cierre de GUI flota) + review owner de la elección de cohorte y de la divergencia Builder actual (G4) vs cohorte (G1)
> - [ ] **C2** Auditar personalmente evidencia SQX vs GUI/report y congelar campos confiables #owner/me #type/research #area/echo — BLOCKED (7.ª sesión 2026-09-25): FlowRun `1a4d66d6` = FAILED (1 solo intento sqcli 04:52:36Z contra GUI Zeus, sin retry); 0 overview/MetricSets ⇒ sample imposible. Precondiciones: cerrar GUI Zeus + re-ejecutar enriquecimiento sobre el cohort ya publicado (sin re-importar)
> - [ ] **C3** Revisar Classification real y aceptar/iterar sus clases #owner/me #type/research #area/echo
> - [ ] **C4** Revisar Ranking real: top/bottom/cutoffs/explicaciones y aceptar o iterar scoring #owner/me #type/research #area/echo
> - [ ] **C5** Revisar Selection real: selected/rejected/falsos positivos-negativos y aceptar SelectionSnapshot #owner/me #type/research #area/echo
> - [ ] **C6** Ejecutar Campaña B sobre el SelectionSnapshot aceptado (SQX tick OOS → MT5 real ticks) #owner/me #type/dev #area/echo
> - [ ] **C7** Iterar Classification/Ranking/Selection hasta baseline empírico aceptado #owner/me #type/research #area/echo
> - [ ] **C8** Diseñar e implementar Integration V2 Forge→Echo según necesidades observadas del nuevo The Lab #owner/me #type/dev #area/echo
> - [ ] **C9** Ejecutar primera campaña integrada Forge→Echo→The Lab y cerrar el proyecto #owner/me #type/dev #area/echo

## 📆 Bitácora

> [!note] Premisa de ambiente corregida (2026-09-24)
> Las tres sesiones siguientes se ejecutaron bajo la premisa “Forge necesita runtime/SQX DEV en Daedalus”, que el owner corrigió ese mismo día ([[Echo + Echo Forge — Environment Contract]] §0: Forge tiene un único ambiente operacional). Se conservan íntegras como bitácora histórica y como evidencia del runtime candidato DEV; su blocker de licencia quedó `SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION` y no vuelve a usarse como gate de Campaign 001.

- **2026-09-23** — Proyecto creado por decisión del owner. Echo Forge deja de desarrollarse en abstracto y pasa a certificarse operando estrategias reales. El foco explícito del owner es revisar personalmente datos extraídos de SQX, Classification, Ranking y Selection; iterar algoritmos cuando el resultado no represente su criterio; someter seleccionados a validación SQX/MT5; y recién después construir Integration V2 con Echo/The Lab.
- **2026-09-24** — Prework de ambiente Fase 1 ejecutado (sesión ZCode/GLM-5.3-Flash en Daedalus): baseline `master=origin/master=d9032ff8` verificado limpio; watcher+worker DEV construidos y ejecutados localmente con `ENV=development`; smoke real de dispatch (job retester con `.sqx` real de la cohorte G7 bajo prefijo `wave_prework_smoke_20260924`) completó watcher→MinIO→PG→Temporal y quedó demostrado el blocker SQX con repro (`worker` exit 1: `command not found or not executable: /home/kor/sqx/sqcli`); artefactos descartables del smoke limpiados (workflow cancelado — cierra al arrancar el primer worker DEV; objetos MinIO del prefijo smoke borrados; filas PG `sqx.flow_runs`+`sqx.configs` borradas); repo sin delta. Veredicto `PREWORK_BLOCKED` (subtipo authority): owner debe proveer distribución SQX Build 142 y autorizar licencia DEV en Daedalus (instalar OpenJDK es operacional y no bloquea la decisión). NEXT EXACT en §HANDOFF de la sesión.
- **2026-09-24 (2.ª sesión — corrección y cierre)** — Veredicto `PREWORK_BLOCKED_AUTHORITY` con blocker único = licencia SQX para Daedalus. Resuelto: distribución oficial hallada en Kronos (`/home/kor/sqx/SQX_142_linux_20250327.zip`) y copiada byte-idéntica a Daedalus vía clave SSH temporal (append→scp→revoke con SHA256 de `authorized_keys` antes `397ec802…`/después idéntico; imagen ssh-mcp restaurada tras reparar pool de sesiones, remediación canónica del runbook); instalación `/home/kor/sqx` (Build 142.2399 impreso por el binario real, JRE Zulu 21 bundled, plugin certificado, exporter config). Material evidence licencia: misma clave en Zeus/Hera/Kronos (hash idéntico ×3) pero `sqcli` en Daedalus rechaza host nuevo; términos §3.8 single-device. Runtime candidato: prefixes `/sqx-{worker,watcher}/forgev2dev/` + cola exclusiva `sqx-forgev2-dev-v1` en `sqx-dev`; smoke real completo hasta `execute_sqx` (cohort MinIO descargado verificado → `sqcli` exit 1 licencia; retries infinitos por `MaximumAttempts:0` ⇒ cancel); teardown 100% (workflow CANCELLED, PG `flow_runs`/`configs` borradas, 4 objetos MinIO borrados, procesos detenidos, zombie prework 1 TERMINATED). Reconciliación ETCD prework 1: ambas mutaciones KEEP (par watcher/worker DEV consistente en `sqx-main-queue@sqx-dev`; ownership compartido documentado; candidato no la usa). Findings: licencia Daedalus BLOCKER_NOW; `go.work.sum` stale (vcs.modified=false inalcanzable) BEFORE_PHASE1; binarios prework 1 construidos con tree sucio (reemplazados) BEFORE_PHASE1; teardown Temporal sin poller exige Terminate BEFORE_PHASE1; `max_parallel` knob no cableado en binario actual BACKLOG; ssh-mcp session pool recurrente + `sftp-download` corrupto para binarios BACKLOG (feedback 2026-09-24); §5.8 del Environment Contract contiene claims a corregir (binarios `35821eb9/251f25e2` con tree sucio y alcance del smoke) — corrección documental diferida a acción autorizada separada (no editada en esta sesión). Repo sin delta (`d9032ff8` limpio). NEXT EXACT: Shot 1 de Fase 1 queda desbloqueado salvo licencia — C0 puede iniciarse sin SQX; C1/C2 requieren la acción owner de licencia.
- **2026-09-24 (3.ª sesión — cierre post-activación de licencia)** — Mandato: cerrar exclusivamente el gate `SQX real → EchoForgeOverviewExporter → evidence artifact` hacia `PREWORK_PASS`, verificando antes que ningún `internal/license.db` copiado de otro host sobreviviera a la activación legítima. Evidencia física: (1) `sqcli` en Daedalus rechaza la licencia a las 18:25Z con la copia flota en el sitio (`Failed to check license - License is not valid for this computer`); (2) la copia local se probó idéntica a la flota: estructura + valor `license=D0C25B` (6 chars, sin clave plena) leído RO en Kronos, SHA256 `a25ce029…` preservado, mtime 14:32 local = siembra del prework 2 nunca reemplazada (el run register del prework 2 declara "license.db con clave flota"); (3) cero artefactos de activación del owner en el host: ningún archivo bajo `/home/kor/sqx` posterior a la sesión 2 (los 3 tocados son de esta verificación), sin keys de licencia en ETCD (todos los prefixes legibles, por nombre), sin buckets nuevos en MinIO (la identidad de licencia es local por construcción: sin license.db sqcli responde `Missing license`); (4) eliminación ejecutada según mandato: `internal/license.db` retirada con backup `~/aranea/work/forge-prework3-20260924/stale-license.db.copy-of-kronos` ⇒ re-run `sqcli -v`: `Missing license` (exit 1). Estado resultante: Daedalus sin licencia local; Kronos mantiene su license.db (intacto); Zeus/Hera no tocados. Baseline re-verificado: `master=origin/master=d9032ff8` worktree limpio único; SHAs de binarios candidato coinciden (`7af048f0…` watcher, `b2e9c227…` worker); sin procesos residuales. Pasos 3–10 del mandato corto-circuitados: sin licencia aceptada el camino real no produce evidencia (repro del prework 2: worker arranca pero `execute_sqx` falla con `sqcli` exit 1); worker no arrancado, cero mutaciones nuevas en ETCD/MinIO/PG/Temporal, cola exclusiva sin pollers. Veredicto `PREWORK_BLOCKED_AUTHORITY` — subtipo licencia ahora más preciso: la activación del owner no materializó estado local en el host (puede requerir el paso interactivo con la credencial nueva, o el binding vendor-side del HWID `C487C9A88600` no se completó). Repo sin delta. NEXT EXACT: owner completa la activación local de la licencia legítima en Daedalus (que `internal/license.db` quede bound a `C487C9A88600` vía flujo oficial); re-dispachar la sesión de cierre del gate (`sqcli` acepta → 1 worker → camino real watcher→MinIO→Temporal→worker→sqcli→SQX→exporter → evidencia con SHAs → teardown). *Esta sesión y su NEXT EXACT quedan SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION (ver entrada 4.ª).*
- **2026-09-25 (7.ª sesión — preparación hito C3+C4+C5: FlowRun actual = FAILED y política = G7_DERIVED; política histórica BR_G1/wave1 no recuperable):** sesión ZCode/GLM-5.3-Flash en Daedalus, mandato: cerrar C2 + recuperar la política real BR_G1/wave1; sin ejecutar Retester ni reimportar. **FlowRun `1a4d66d6` = FAILED (no "en retry"):** la read surface `sqx-flowkit run stages` (namespace sqx-prop) muestra status FAILED con el stage `import@sqx-import.v1` generation 1 en RUNNING-zombie; en el log del worker Zeus el stage tuvo 1 solo intento 2026-09-25T04:52:36Z (`sqcli -project action=start name=EchoForgeImportExporter`, 548 ms, "success markers not found" — contrato single-instance contra la GUI `sqcli -gui` abierta en Zeus, PID 2940144 desde 21:39 local 09-24; Hera/Kronos ya sin GUI) y NUNCA reintentó — corrige la expectativa de retry automático de la 6.ª sesión. Los 727 artifacts publicados+adoptados siguen intactos (verificado en MinIO `wave_wave1b/…/01_cohort_001/`), `02_selection` sólo tiene `.folder_marker`, y no existe overview/MetricSet (0 evidencia) ⇒ **C2 = BLOCKED** (sample SQX↔Forge imposible: 0 evidencia Forge que contrastar). **Config durable leído literalmente** (PG `sqx.configs` id `0221b984-64b6-4e71-8266-f5fc48ecd825`, vía flowkit RO + helper SELECT efímero, eliminado; repo restaurado limpio @ 6482173): tasks=[`selection select_cohort001`→`02_selection` source `01_cohort_001`]; classifications=`indicator_signature.v1@1.0.0` (input watcher_import); early_rankings=`weighted_combination_minmax.v1@1.0.0` con drawdown COST 40 / profit_factor BENEFIT 30 / sharpe_ratio BENEFIT 30, top_n=5; selections=`per_logical_type` top_n=3; sin Retester, promotion, scores ni rankings post-retester. El `job_config.json` de MinIO (sólo tasks) es el registro legacy JobConfig, no la política durable. **FLOWRUN_POLICY = G7_DERIVED:** el config es estructuralmente idéntico al de la certificación G7 (`USATECHIDXUSD_darwinex_SQX_v1_wimport_cert_v1` / g7r5, 2026-09-23); coincide con la base contractual congelada (30/30/40) pero top_n=5 y selección 3/per_logical_type provienen del template G7, no de evidencia BR_G1/wave1. **Política histórica BR_G1/wave1 = NOT_RECOVERABLE:** barrido del registry (ningún FlowRun/config NDX/USATECH antes del 2026-09-25 salvo wave_test de agosto), sin paquetes `00_configs` en MinIO (bucket `configs` = tests 2025-08), sin job_config histórico; BR_G1 existe sólo como CFX Builder SQX-side (`Build_BR_G1_H1.cfx`) y las 727 son el output crudo del retest ("in retest cross", re-save 02:39Z) — el ranking/selection del flujo real del owner ocurrió en SQX GUI sin config durable. **Mecanismos confirmados en código** (`workflows/generic_workflow.go` @ 6482173): (a) `group source=ranking_snapshot` → Retester (durable EARLY; `source: ranking` dinámico rechazado fail-closed) y (b) task `selection` → SelectionSnapshot durable (consumido después por Campaña B vía `selection_cohort`); tras cada producer corren classification→early_ranking (`runClassificationSnapshotsForProducer`/`runEarlyRankingSnapshotsForProducer`). El FlowRun actual usa (b) sin Retester — patrón correcto para el experimento C3–C5. **Veredicto: C2=BLOCKED; ejecución = re-ejecución requerida con la config durable ya registrada**, pendientes: (1) owner cierra GUI Zeus; (2) ratificación owner de top_n=5 / selección 3 per_logical_type como política de Campaign 001 (única decisión faltante, no completar con ejemplos); (3) elegir vía de re-ejecución — re-dispatch con el mismo request_id (convergencia FD-1 al mismo FlowRunRef, soporte sobre FlowRun FAILED sin verificar) o FlowRun nuevo consumiendo el cohort ya publicado (evita re-import, mandato). Repo sin delta de producto. **NEXT EXACT: (1) owner cierra la GUI SQX de Zeus; (2) owner ratifica o corrige ranking_top_n y selección scope/top_n; (3) verificar el camino de re-ejecución del enriquecimiento sobre el cohort 001 sin re-importar y despachar; (4) con enriquecimiento COMPLETED, ejecutar sample C2 y trust matrix; (5) recién entonces Shot C3+C4+C5 (Classification→Ranking→Selection sin Retester, packet owner).**
- **2026-09-25 (6.ª sesión — CORRECCIÓN DE MANDATO: Cohort 001 Zeus/Retester "in retest cross" + resolución BR_G\*): C1=CANDIDATE (727/727), C2=BLOCKED_EXTERNAL (GUI flota).** Sesión ZCode/GLM-5.3-Flash en Daedalus. **Inventario Zeus (RO):** SQX en `/home/kor/sqx`; proyecto Retester databank `in retest cross` = **727 .sqx** (0 SHA duplicados, 110.6 MB, re-save del retest 2026-09-25T02:39Z); SHA256+tamaño de todos capturados. **Grupo:** comparación Builder efectivo vs configs ⇒ Builder ACTUAL == `Build_G4_BR_H1.cfx` (byte-semántico, sólo root tag y paramType null/undefined) PERO la cobertura del universo de bloques usados por las 727 estrategias (15/15 claves configurables ⊆ G1; G2 falla 12; G4 falla 15; IsGreaterOrEqual/CrossesAbove/IsRising sólo en G1; 0 uso de familias G4) prueba que el origen es **BR_G1** (`Build_BR_G1_H1.cfx`) ⇒ `RESOLVED_GROUP=BR_G1`, `STRONGLY_CORROBORATED`, con divergencia Builder-actual(G4)/cohorte(G1) documentada para decisión owner; no existe config BR_G3. Corroboración: 727/727 `USATECHIDXUSD_darwinex/H1` y LONG-only (señales Short/Exit constante false). **Freeze:** `COHORT001-FREEZE.json` v3 SHA `f4aa96bf…` (727 items). **Import:** watcher candidate-local en Zeus sobre ETCD production; CFX G7 byte-idéntica; tras 3 intentos fallidos documentados (conflicto de alias canónico por 4 duplicados "(1)" — resuelto con sufijo `.d1`; manifest sellado invalidado; identidad `wave1` envenenada por membresías de intentos ⇒ wave técnica **`wave1b`**) el pipeline completó 7/7 con `published_count=727`, manifest sellado con **727/727 SHA == freeze local**, FlowRun `1a4d66d6-edb4-415b-ae1e-f7cb0d1b79f2` (workflow `sqx-main-v1-722dfb27…`, run `01a0d6e8…`); worker Zeus descargó 727/727 digest-verified. **Fix de producto (rama corta R7, pusheada, sin merge):** `fix/watcher-import-intake-deadline` @ `a95ef2c` — knobs `SQX_WATCHER_INTAKE_DEADLINE` (default 2m intacto) y `SQX_WATCHER_DISABLE_AUTO_UPGRADE`; el deadline fijo de 2m no alcanza para cohorts grandes y el watchdog auto-upgrade mata binarios candidate-local a los 10s. **Licencia/C2:** renovada (license.db 3/3 hosts, 2026-09-24 21:37 local, D0C25B→921C51; retest físico 22:39 OK) pero `sqcli -gui` del owner abierto en 3/3 hosts ⇒ single-instance bloquea todo sqcli CLI; el stage sqcli del FlowRun queda en retry y completará al cerrarse las GUI. Limpieza propia: 296 objetos MinIO garbage + 1 manifest sellado inválido eliminados; watcher detenido; fuente Zeus intacta. Repo: delta de producto en rama de fix únicamente. **NEXT EXACT: (1) owner cierra las GUI SQX de Zeus/Hera/Kronos → el FlowRun `1a4d66d6` completa el enriquecimiento solo (retry vigente); (2) verificar FlowRun COMPLETED + overview evidence; (3) ejecutar sample C2 y trust matrix; (4) decisión owner sobre divergencia Builder G4 vs cohorte G1 (restaurar `Build_BR_G1_H1.cfx` como template si se sigue en wave1 G1) y review del merge de la rama de fix; (5) Shot 2 — Independent Verification sobre el candidate C0+C1(+C2).**
- **2026-09-24/25 (5.ª sesión — Fase 1 Shot 1: C0+C1+C2): `SHOT1_BLOCKED_EXTERNAL` — C0=CANDIDATE_PASS, C1=CANDIDATE_PASS, C2=BLOCKED_EXTERNAL.** Sesión ZCode/GLM-5.3-Flash en Daedalus; evidence pack `~/aranea/work/forge-shot1-20260924/EVIDENCE-SHOT1.md`. **C0:** runtime alineado al source aceptado — release **0.2.107** construida desde `d9032ff8` por mecanismo canónico (`deploy_release.sh --release-only`; screen `deployer` estaba muerto desde 17:47Z, re-levantado), publicada a MinIO y aplicada por stager en Zeus/Hera/Kronos 3/3 (CURRENT=0.2.107, SHA `6dccbde3…` idéntico build/MinIO/flota, workers polling `sqx-prop/sqx-main-queue`); commit de release `6482173` pusheado (master=origin/master=6482173; delta = sólo `deploy/manifest.json`). **C1:** Cohort 001 = **11 estrategias XAUUSD L H1 auténticas del portafolio running del owner** (MinIO `running/wave_2/xau/base/`, 2025-10-09; interpretación de "elegidas por el owner" declarada explícitamente para review; NO fue la cohorte G7); Watcher Import real con el binario 0.2.107 sobre ambiente operacional (ETCD production): pipeline watcher 7/7, freeze manifest `watcher-import-freeze-manifest.v1` sellado write-once, publicación byte-exacta 11/11 (etags == source), adopción IMPORTED + membership, lineage N/N = 11/11 verificado (MinIO + PG + manifest); FlowRun `f87fde30-7730-4619-a308-b225714811f4`, workflow `sqx-main-v1-660c32f1…` — **ese Cohort 001 y su FlowRun quedan INVALIDATED_AS_COHORT001_BY_OWNER (corrección de mandato, 6.ª sesión)**. **C2:** enrichment físico (stage `import@sqx-import.v1` → sqcli → EchoForgeOverviewExporter) **BLOQUEADO: la licencia SQX de la flota está vencida vendor-side** ("Trial license expired" en Zeus/Hera/Kronos, license.db intacto desde sep-10, verificación online; pasó G7 el 09-23) — blocker externo único, sólo el owner puede renovarla; el workflow queda en RUNNING con retry y el enrichment se completa solo al renovar. Entregado igualmente: inventario de datos SQX→Forge (code-derived, etiquetado; TradeList = MISSING por diseño en este stage), sample de 5 estrategias con checks exactos del owner y trust matrix provisional. Findings: go.work.sum stale reproducido con causa exacta (go1.27.1 normaliza ⇒ vcs.modified=true; resolución canónica = commitear sum normalizado, SHOT2/SHOT3); deployer/watcher sin servicio durable (BEFORE_C6); OTEL .45 caído; Mongo RO MCP caído; jar del plugin difiere Zeus≠Hera. Repo sin delta de producto; helpers efímeros eliminados. **NEXT EXACT: (1) owner renueva la licencia SQX de flota; (2) verificar que el FlowRun `f87fde30` complete el enrichment (o re-despachar el flujo); (3) ejecutar el sample C2 y llenar trust matrix + diferencias reales; (4) ejecutar Shot 2 — Independent Verification de Fase 1 sobre el candidate C0+C1(+C2) de esta sesión: falsificar runtime/source exactness, lineage N/N y SQX evidence trust; no corregir producto durante Shot 2.**
- **2026-09-24 (4.ª sesión — corrección canónica de ambientes, mandato owner one-shot): `ENVIRONMENT_MODEL_CORRECTED`.** El owner corrigió el modelo conceptual: Echo y Echo Forge NO comparten modelo de ambientes. Echo conserva DEV/PROD; **Forge tiene UN solo ambiente operacional** (production) — flota SQX Zeus/Hera/Kronos + worker Windows Kronos + dependencias persistentes del runtime real — y sus pruebas físicas, campañas y certificaciones se ejecutan allí; Daedalus queda como workspace/coding agents/builds, no como runtime SQX/MT5 de Forge; `ENV=production` de Forge es canónico, no fallback/leak/defecto; y “Forge production” no autoriza dinero real (gates económicos independientes). Corregido: [[Echo + Echo Forge — Environment Contract]] (§0 nuevo, §1 selección de ambiente, §2 topología, §3, §4 matriz, §5 gates, §5.8 banner SUPERSEDED + corrección factual de SHAs de binarios `35821eb9…/251f25e2…` → vigentes `7af048f0…/b2e9c227…`, §7 reconciliación), router `aranea-agent-dev` (selección de ambiente por producto) y esta nota (estado, decisión R9, bitácora). `PREWORK_BLOCKED_AUTHORITY` y la licencia Daedalus = `SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION`; `PREWORK_MT5 = DEFERRED_UNTIL_C6` se mantiene por alcance de stage (C0–C2 sólo requieren SQX). Estado del prework = `PREWORK_REQUIRES_RUNTIME_REVALIDATION`, con esa revalidación absorbida por C0 (RC 0.2.106 @ `d07cc69` vs baseline `d9032ff8`). Sin mutación de infraestructura, ETCD, workers ni repos de producto. **NEXT EXACT: iniciar Shot 1 de Fase 1 de Echo Forge — Operación Real V2 sobre el ambiente operacional Forge canónico. Shot 1 trabaja el milestone único C0+C1+C2. No avanzar C3.**

## 🧭 Decisiones

- **R1 — Real campaign = product authority.** Los tests certifican contratos y regresiones; no certifican por sí solos la utilidad del algoritmo.
- **R2 — Human review es gate formal.** C2–C7 requieren aceptación explícita del owner; técnicamente verde puede terminar en STAGE_ITERATE.
- **R3 — Versionar el funnel.** Cambios de métricas, pesos, thresholds, clasificación, ranking o selection quedan versionados junto con cohort/config/output.
- **R4 — Campaña B deja de ser proyecto independiente.** Su capacidad `selection_cohort` y pipeline SQX/MT5 viven en C6.
- **R5 — Integration V1 superseded.** C8 construye Integration V2 desde necesidades reales observadas.
- **R6 — Límites de autoridad.** Forge produce y valida estrategias/evidencia; Echo ingiere y normaliza; The Lab construye análisis/curvas/portfolios según su contrato vigente.
- **R7 — Branches cortas.** Findings de campañas reales → branch acotada → implementación → verificación independiente → master. No acumular ramas largas.
- **R8 — No optimizar antes de observar.** No crear dashboards, feedback automation o nuevos scores antes de que C2–C5 demuestren una necesidad concreta.
- **R9 — Modelo de ambientes Forge (decisión owner 2026-09-24).** Forge tiene un único ambiente operacional (production) y sus pruebas físicas se ejecutan allí: flota SQX Zeus/Hera/Kronos + worker Windows Kronos, según la capacidad que el stage requiera. No se construye una separación DEV/PROD para Forge; no hay requisito de SQX, licencia ni worker DEV en Daedalus ni de `dev-win`; `ENV=production` es el ambiente canónico, no un defecto. La seguridad la determinan el scope y el ownership del recurso (aislamiento de candidatos por cola/prefijo/instancia candidate-local, flota activa intacta — patrón G7), y el dinero real sigue siendo gate owner independiente. Detalle canónico: [[Echo + Echo Forge — Environment Contract]] §0.

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
