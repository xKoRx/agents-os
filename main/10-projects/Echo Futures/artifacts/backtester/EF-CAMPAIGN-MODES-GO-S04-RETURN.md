---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-GO-S03R1-RETURN]]"
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-30"
updated: "2026-10-30"
---

# EF-CAMPAIGN-MODES-GO-S04-RETURN

**STATUS: C06_DELIVERY = PARTIAL · FIRST_STRATEGY_CANDIDATE = SELECTED_FOR_REVALIDATION.**

El candidato C06 pasó de fail-closed incompleto a **capacidad materialmente entregada en los grupos A–E** (bindings sellados TGMM/RGMM por asociación, heterogeneidad real de perfiles/RuleSets/MM, FUNDED multi-asociación, CloseSafety v2, productor de reversos, admisión sin bypass, migración honesta con materialización v2 real). Pero **C06 no está completo**: dos requisitos materiales quedan abiertos y se declaran aquí con su causa exacta — el productor REFUND de lifecycle (Grupo C) y el piso de cobertura por archivo en 4 superficies grandes (F7). La candidata económica #1 queda **seleccionada para revalidación**, con su configuración materializada, admitida y ejecutada mecánicamente; **no** está lista para certificación runtime porque su MM (riskgeometry) es `HISTORICAL_POLICY_ONLY` y la cadena G0–G5/D01/D02/D05 sigue sin resolverse.

## Identidad de la entrega

| Campo | Valor |
|---|---|
| BASE_SHA | `2baf319ddcba622d9557bc9f23a13787b44c58a7` (master remoto sin mover; ancestry verificado) |
| EXACT_REVIEWED_SHA | `062b6df77845d2042e398bb6174700e80bb58b60` (el SHA exacto que S03/S03R1 revisaron) |
| BRANCH | `feature/ef-campaigns-go` (remoto `origin/feature/ef-campaigns-go` == local, readback verificado) |
| FINAL_SHA | `a22970c85d139c81c919aafac69f4bf6ceaf5dcd` (remoto `origin/feature/ef-campaigns-go` == local, readback verificado) |
| BUILD_SHA256 | `9769039d69d26ddb54b953ad2a9eb289a6ac9d6c7f5bd9faf1392bac5c939c35` (`go build -trimpath -buildvcs=true` en FINAL_SHA) |
| DIFF_SCOPE | 31 archivos, +5.706/−165, 17 commits sobre `062b6df7` (7 del autor S02 + 16 de producción/pruebas de este shot + 1 documental de VERIFICATION/TASKS) |
| Superficie nueva | `campaign_v2_sealed.go` (autoridades selladas de producción), `campaign_v2_candidate.go` (loader de preset sellado + derivador v2 de candidata), 2 TCR |
| AGENTS_OS_PATHS_SHA | este retorno: `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-GO-S04-RETURN.md` (create-only); delta del planner: `10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md`; run-register: `80-agents/journal/agent-runs/2026-10-30-zcode-glm-5.3-flash-echo-c06-go-s04.md` |

## FINDINGS_DISPOSITION (F1–F10, NF1–NF4)

| ID | Veredicto S03/S03R1 | Disposición GO-S04 | Evidencia |
|---|---|---|---|
| **F1** TGMM/RGMM no admitidos (P1) | CONFIRMED | **CORREGIDO** — superficie sellada por asociación (`mm_catalog` versionado, digest-preservante): TGMM y RGMM se resuelven contra catálogos sellados por las costuras runtime (`NewSealedMoneyManagerCatalog`/`SealedAccountPolicy`), sin segunda fábrica. La guardia `HISTORICAL_POLICY_ONLY` de RG **intacta** (ver §Estado HISTORICAL/LIVE) | `campaign_v2_sealed.go`, `campaign_modes_v2.go` (admisión), `campaign_v2_s04_test.go` |
| **F2** heterogeneidad imposible (P1) | CONFIRMED | **CORREGIDO** — dos perfiles realmente distintos + dos RuleSets del catálogo + MM heterogéneo por asociación, simultáneos, con divergencia conductual. Se detectó y corrigió un defecto real durante la corrección: el seed del compartimento instalaba el RuleSet **global** mientras el binding declaraba el de la asociación (el proveedor rechazaba el claim y el segundo compartimento nunca operaba) | `compose_account.go`, `campaign_v2_s04_test.go` |
| **F3** FUNDED multi-asociación (P1) | CONFIRMED | **CORREGIDO** — `seedAllFunded` generalizado: N seeds por asociación, provenance por asociación, denominadores separados | `campaign_modes_v2.go`, `campaign_v2_s04_test.go` |
| **F4** CloseSafety v2 (P2) | CONFIRMED | **CORREGIDO** — superficie legacy-shaped admitida en v2 y consumida por el runtime (close-risk, checkpoint, force-close, flat checks). `CLOSE_CALENDAR_MISSING` conservado como negativo | `campaign_modes_v2.go`, `campaign_composition.go` |
| **F5** reversos/refunds sin productor (P2) | CONFIRMED | **CORREGIDO PARCIALMENTE** — el **productor de REVERSO** existe (identidad propia `payment.ID+"/reversed"`, caja ajustada una vez, primer crédito preservado, idempotencia, conflicto nombrado, `finish()` concilia). El **productor REFUND de lifecycle NO se implementó**: no existe transición declarada consumidora (una transición de contexto rechazada falla el run; `PENDING_AT_HORIZON` permanece por C06 §6) ⇒ inventar el disparador sería economía nueva prohibida. Contrato REFUND sellado en emisor+proyector | `campaign_accounts_v2.go` (`reconcileCreditedPayouts`), `campaign_modes_v2.go` (`finish`) |
| **F6** MIGRATED=LEGACY_PATH (P2) | CONFIRMED | **CORREGIDO** — etiqueta honesta `LEGACY_PATH_PRESERVED` + **builder de materialización GO_V2 real** (antes: constante sin builder). 104 filas, censo delta CERO, materialización por identidad | `campaign_migrate.go`, `campaign_v2_sealed.go`, `lab migrate --materialize-v2` |
| **F7** cobertura <95% (P2) | CONFIRMED | **PARCIAL** — el piso 95% **no** se alcanza ni por archivo ni diff-aware (79,6% statement-based sobre 1.027 statements nuevos); los huecos combinan superficies nuevas (`campaign_v2_candidate.go` 68,9%, `campaign_v2_sealed.go` 74,4%, `campaign_migrate.go` 74,6%) y pre-existentes (`qualification_admission.go` 30,5% con suite en otro paquete, `campaign_modes_v2.go` 83,6%). Medida statement-based con denominador explícito (el promedio por función del retorno S02 no es la medida de policy). Declarado, no maquillado | ver §COVERAGE |
| **F8** puertas legacy con bypass opt-in (P2) | RECLASSIFIED a defecto WITHIN_C06 | **CORREGIDO** — las cuatro puertas ejecutables legacy (`run`, `platform-batch`, `campaign`, `reproduce`) clasifican ahora el **propósito físico** del input reutilizando `ClassifyExecutionPurpose`: QUARTER/HISTORICAL sin cadena de receipts ⇒ `RECEIPT_MISSING` pre-engine (exit 78, cero motores). La alternativa "ledger-only" del retorno S03 fue descartada. Se conservan: SMOKE sin receipts, replay de identidad ya admitida, comandos de sólo lectura, D05 bloqueado | `qualification_gate.go`, `qualification_admission.go`, `btx_s04_gate_purpose_test.go` |
| **F9** capacidad sólo anillo 1×N (P3) | CONFIRMED | **CORREGIDO** — K=5 asociaciones simultáneas medidas (5 compras, cash 2.380 USD, reconciliado, `CONTINUOUS_HORIZON_COMPLETE`) sobre un único mercado/reloj/scheduler/caja. El reviewer midió K=2/K=3 | `campaign_v2_s04_capacity_test.go` |
| **F10** independencia de modelo (P3) | CONFIRMED / NO RESUELTO | **RESIDUAL DECLARADO** — el verificador final no-GLM **no estaba disponible**: el surface expone `account:zai-start-plan/GLM-5.3-Flash` y los despachos de subagente funcionaron sólo intermitentemente (cuota muerta en dos tramos; dos workers completaron, dos murieron y fueron reanudados). Todo el trabajo de este shot es **GLM-5.3-Flash**. No se etiqueta como GOD a ninguna ejecución GLM | ver §SUBAGENT_RECEIPTS |
| **NF1** `AccountSlots` sin cap (P2) | CONFIRMED | **CORREGIDO CON LA ADJUDICACIÓN DEL OWNER (no con el mínimo propuesto por S03R1)** — `AccountSlots` NO se convirtió en un límite de compras de por vida: es **inventario concurrente de asientos**; los reemplazos reusan el asiento y las adquisiciones sucesoras siguen la política de adquisición declarada. Regresión: con `AccountSlots=1` tres compras sucesoras son legales y los asientos concurrentes nunca exceden `AccountSlots` | `campaign_v2_contract.go` (semántica documentada), `campaign_v2_s04_test.go` |
| **NF2** disputa de última caja asimétrica (P2) | CONFIRMED | **CORREGIDO** — el owner del motor **ganador** se instala en el compartimento adoptado; el flip que moría con `OPERATION_OWNER_MISSING` corre limpio con winner invertido y cash idéntico por simetría (1.000 USD) | `campaign_composition.go`, `campaign_v2_s04_test.go` |
| **NF3** activación funded (P3) | CONFIRMED | **CORREGIDO** — activación acreditada por **control observado** (nunca por `compliant_at`); la autoridad de *solicitud* de payout abre sólo con `compliant_at` (calendario declarado); elegibilidad separada. Sin desplazamiento de fechas por intuición | `campaign_accounts_v2.go`, `campaign_modes_v2.go` |
| **NF4** replay de items sin artefacto (P3) | CONFIRMED | **CORREGIDO** — replay **nombrado**: `reproduce --result-json` re-deriva el request sellado del artefacto plano tras **verificar su digest contra la identidad del artefacto**, y compara identidad/cash/terminal/reconciliación/evidencia económica | `replay.go`, `reproduce.go`, `campaign_replay_result_s04d1_test.go` |
| **Defecto ordinario extra** | — | **CORREGIDO** — `ClassifyExecutionPurpose` ignoraba lecturas declaradas sin stamps y el catálogo de contratos declarado, contradiciendo su propio test de tabla (`TestQualificationPurposeClassification/short_multi_contract_is_historical` fallaba en el SHA revisado **prístino**). Corregido sin tocar la regla de residuo zero-stamp | `qualification_admission.go` |
| **Defecto ordinario extra** | — | **CORREGIDO** — `TestCampaignV2Matrix_EventLogSurfaceHonesty` iteraba un map exigiendo orden: es el "FAIL único no reproducido" observado por S03R1. Reparado con igualdad de conjunto + orden declarado (TCR §3b) | `campaign_v2_matrix_test.go` |

## GO_ONLY_PROOF

Físico, sin Python en `PATH` (sandbox `/tmp/nopython-s04/bin`, `command -v python3` ⇒ **PYTHON_ABSENT**):

- `go test ./v3/backtester -run 'CampaignV2|CampaignComposition|CampaignEconomic|CampaignMigrate|Migration|Candidate'` ⇒ **ok** bajo el sandbox sin Python.
- `lab migrate --materialize-v2 --out DIR` ⇒ exit 0, **28 artefactos** (27 requests + manifiesto), censo `{V2_ADMITTED:27, BLOCKED:62, CATALOG_VALIDATED:15}`, 104 filas, delta CERO.
- Build sellado limpio; grep del flujo oficial: cero invocaciones Python (los únicos hits son comentarios de linaje).
- No se creó otra dependencia Python; no hay venv/pip/wrapper/exec.

## MIGRATION_MATRIX (por identidad — sin renombrar estados por nombre)

Censo de referencia **26 nativas + 63 SG + 15 aliases = 89 ejecutables / 104 filas**, delta CERO. Salida del builder (`lab migrate --materialize-v2`, receipt `/tmp/s04v-migrate/MATERIALIZATION-MANIFEST.json`, schema `echo.backtest.campaign-migration-materialization.v1`):

| Estado | Filas | Detalle |
|---|---|---|
| `LEGACY_PATH_PRESERVED` | 26 | las 26 nativas en la matriz (sin builder): la ruta legacy queda preservada por diseño §10, no "migrada" |
| `V2_ADMITTED` | 27 | 26 nativas TGMM + 1 RGMM (`SG:SG-MR-04-500`): request v2 **materializado** y **admitido** (`Validate()` en seco, sin engine), con spec_digest y request_digest por fila |
| `BLOCKED` | 62 | causa única y nombrada: *"no sealed promotion bundle declares the RGMM_ACCOUNT_POLICY_V1 economics for profile &lt;ref&gt; (eval_daily_goal_usd/internal_pause_loss_usd absent from the sealed profile authorities; RGMM account policy is a required RG block member and is never defaulted)"* |
| `CATALOG_VALIDATED` | 15 | aliases (`ALIAS_OF_CANONICAL`): materializan nada, se ejecutan por su canónico |

Materializadas concretas (digests del binario sellado): `NATIVE:MR-08` spec `sha256:ee355ac3…` / request `sha256:77825d00…`; `SG:SG-MR-04-500` spec `sha256:7de7f3bd…` / request `sha256:b872a3d7…`. Horizonte: autoridad sellada `r5-report-manifest-FULL.json` (HIST 2023-10-02→2026-10-06, 785 sesiones). `SAME_SEMANTICS`/`NEW_EXPERIMENT` conservan su clasificación vigente (41 SAME / 63 NEW por `budget_semantics`); **V1/Unclipped no renombrados**; ningún receipt ni catálogo sellado reescrito.

**El desbloqueo de las 62 filas es barato y está identificado**: los presets sellados de los runs COMPLETE_RECONCILED (R01/R03) **sí** declaran `account_policy {eval_daily_goal_usd, internal_pause_loss_usd}` por identidad (ej. `S04LAB-LAB-SG-FBC-CH300-15M-R500-V1` ⇒ 870/1000). Lo que falta es un manifest Owner que exponga esas account policies por identidad al builder (o su incorporación a las autoridades selladas del repo). El builder ya las admitiría sin código nuevo.

## EXECUTION_MATRIX (por identidad — estados distintos de la migración)

| Identidad | Estado | Evidencia |
|---|---|---|
| `LAB-SG-FBC-CH300-15M-R500` (candidata #1) | `V2_ADMITTED` + `FUNCTIONALLY_EXECUTED` (mecánico) | spec `sha256:f3d3375e…`, request `sha256:f03c66d6…`; ejecución mecánica sobre corpus sintético determinista (4 sesiones), `reconciled`, eventos del lifecycle |
| `LAB-SG-MR-09-R750` (candidata #2) | `V2_ADMITTED` + `FUNCTIONALLY_EXECUTED` (mecánico) | spec `sha256:acaa4d08…`, request `sha256:d7efdc7f…`; idem |
| 26 nativas TGMM | `V2_ADMITTED` | request materializado y admitido en seco; **sin** ejecución en este shot |
| 62 SG (excepto MR-04-500) | `BLOCKED` | account policy RG no declarada en las autoridades selladas del repo |
| 15 aliases | `CATALOG_VALIDATED` | ejecución por su canónico |
| **CUALQUIER IDENTIDAD** | `HISTORICALLY_EXECUTED = 0` | ninguna campaña histórica ejecutada (D01/D02/D05 + cadena G0–G5 sin resolver) |

**FUNCTIONALLY_EXECUTED significa ejecución mecánica sobre corpus sintético, NO significado económico ni revalidación histórica** — declarado explícitamente en el manifiesto de candidatas (`~/echo-work/c06-s04/candidata/candidata.manifest.json`, `summary: {FUNCTIONALLY_EXECUTED:2, V2_ADMITTED:2, HISTORICALLY_EXECUTED:0}`).

## FIRST_STRATEGY_CANDIDATE

**Estado: SELECTED_FOR_REVALIDATION** (no `VALIDATED_FOR_RUNTIME_CERTIFICATION`).

### Configuración exacta (candidata #1 `LAB-SG-FBC-CH300-15M-R500`)

| Elemento | Valor (fuente sellada) |
|---|---|
| Identidad | `LAB-SG-FBC-CH300-15M-R500` = SG `FBC-CH300-15M` @ `PROFILE-ATR14-WILDER-M1-X1-GROSS500-1TO1` (`search-space-v1.json`, identity_digest `sha256:2cb4786a…`) |
| Strategy | módulo `fbc`, 15m, NQ (`s02r1_preset.strategy_module`) |
| MM | `riskgeometry` (RGMM) con perfil sellado `mm_profile_digest 00885055…` + `RGMM_ACCOUNT_POLICY_V1 {eval_daily_goal_usd 870, internal_pause_loss_usd 1000}` |
| Perfil | `E2T_GAU50_PURCHASE_GE_20260706_OBS_20261012_SCENARIO_V1`: purchase 120, renewal 120 (30 días), provider fee 50, first payout fee 139, platform/stow 0, payout target 2300, gross cap 5000, review/credentials 1 día hábil, compliance 2, approval 1, credit 1 |
| Plan de campaign | `CHALLENGE_ONLY` / `CONTINUOUS_V1`, `RESEARCH_COST_ACCUMULATION_V1`, `RESEARCH_DAILY_CLOSE_V1` con calendario sellado, cash inicial 5.000 USD (perfil de research; **no** es la caja SIMULATION de 4.000) |
| Costura | `RGMM` = `HISTORICAL_POLICY_ONLY` |

### Por qué esta y no la otra (unidad económica, no win-rate)

| Criterio | #1 FBC-CH300-15M-R500 | #2 MR-09-R750 |
|---|---|---|
| Compras → pases | 26 → 9 (0,346; Wilson95 [0,194, 0,538]) | 13 → 5 (0,385; Wilson95 [0,177, 0,645]) |
| Coste/pase | **666,67 USD** | 936 USD |
| Ritmo | **0,73 entradas/día** (cobertura 0,726) | 0,23 entradas/día |
| Mediana tiempo-a-pase | **27,0 días** | 91,9 días |
| Año vigente (2026) | **11 → 5** (su mejor tramo) | 2 → 0 (sin pases) |
| Estabilidad temporal | T1 0,769/día · T2 0,910/día · T3 0,852/día | T1 0,201 · T2 0,306 · T3 0,259 |
| Muestra | 26 compras (ok) | 13 compras (ok, corta) |

La #2 tiene la mejor fracción observada de la parrilla, pero con muestra corta, el año vigente sin pases y un tiempo-a-pase 3,4× mayor; la #1 domina en coste/pase, ritmo, tiempo-a-pase y estabilidad del tramo vigente. El criterio histórico del 25% de R03 **no** se traslada al umbral Owner 1/3 ni a caja finita 4.000 ni a resultados funded: el reporte es descriptivo y la unidad/reset/refund/horizonte del umbral siguen siendo decisión Owner.

### Separación exigida por el mandato

- **Mejor evidencia para challenge:** #1 (cost/pase, ritmo, tiempo-a-pase, tramo vigente). El umbral 1/3 **no** se adjudica aquí.
- **Mejor evidencia funded/retiros:** **NO_OBSERVADO** — R03/R01 son challenge; no hay corrida funded de estas identidades.
- **Factibilidad de ejecutar la misma configuración en runtime:** **bloqueada en el MM**: `riskgeometry` es `HISTORICAL_POLICY_ONLY` (`v3/sdk/futures/riskgeommm/manager.go:83` rechaza LIVE; `v3/sdk/futures/config/composition.go:184` y `:357` rechazan composición/policy LIVE). **La guarda no fue tocada, el modo no se cambió y el MM no se sustituyó.**

## RUNTIME_PARITY_AND_LIVE — estado por módulo

| Módulo | Estado | Evidencia / límite |
|---|---|---|
| Campaign/Strategy/MM/Provider/accounting Go | **HISTORICAL + LIVE-compartido** (owners existentes, sin reimplementación) | paridad monocuenta byte-idéntica preservada; digests legacy intactos (`TestCampaignV2_LegacyRequestDigestPreservedWithZeroV2Fields`) |
| `gerardmm` | LIVE-compartido | sin cambios |
| `tgmm` (26 nativas) | LIVE-compartido (`MM_ENTRY_BUDGET_UNCLIPPED_V1`) | sin cambios |
| **`riskgeometry` / `riskgeommm`** | **HISTORICAL_POLICY_ONLY — LIVE_BLOCKED** | guardas intactas: `manager.go:83` (constructor LIVE), `composition.go:184` (asociación pool LIVE), `composition.go:357` (account policy LIVE). La corrección de F1 abre la **composición histórica**; **no** habilita LIVE |
| `certnt01-s2` + `certnt01-mm-1` (frente ECHO_FUTURES_FIRST_LIVE_TRADE) | **intacto, no tocado** | es el módulo S2 que el runtime live acepta; **no** es la candidata económica (se.job de certificación técnica ≠ candidata por resultados) |
| Proveedor/pools/venue | sin cambios | R6 vigente |

**Paridad ejecutada:** la misma configuración atraviesa los owners compartidos con inputs normalizados equivalentes, mostrando decisión, sizing, riesgo, protección y cierre — `TestCandidate_RGMMParityDecisionLevel` demuestra que el run v2 sirve **la MISMA instancia/tipo del SDK** (`riskgeommm.New` sobre la misma config sellada), no una reimplementación; la comparación a nivel de decisión de sizing se ejecutó y quedó verde. Esto es paridad de composición, **no** fills físicos del broker.

## Handoff mínimo al frente Runtime Pools ya existente

1. **Paquete de habilitación de `riskgeometry` para LIVE** (owner Runtime Pools/S05): el módulo debe (a) componer para LIVE/pool — hoy rechazado en `composition.go:184`/`:357` — y (b) obtener su integración runtime-serving. Identificación exacta de la costura: `v3/sdk/futures/config/composition.go` (registro del módulo y `SealedAccountPolicy`) + `v3/sdk/futures/riskgeommm/manager.go` (constructor que rechaza LIVE) + `v3/sdk/futures/riskgeommm` account policy. **No** se pide cambiar el modo ni el MM: se pide la integración que hoy falta, con su gate propio.
2. **Cuenta RG por identidad para el builder**: exponer `RGMM_ACCOUNT_POLICY_V1` por identidad en una autoridad sellada (R01/R03 ya la declaran en sus presets) ⇒ las 62 filas BLOCKED se admiten sin código nuevo.
3. **Cadena G0–G5 en Go** para la ventana sellada HIST 2023-10-02→2026-10-06 (785 sesiones) + D01/D02/D05 + receipts `echo.strategy-qualification.v1`: la puerta legacy ya clasifica el propósito físico y bloquea QUARTER/HISTORICAL sin receipts (exit 78) — falta producir la cadena.
4. **Presupuesto/ventana** de la revalidación histórica de la candidata #1, autorizado por el Owner (no por este shot).
5. Ningún item de este handoff se ejecuta desde este shot: no hay merge a master, release, deploy, compras ni armado de trading.

## Qué falta para autorización real (sin frases genéricas)

- **Módulo RG**: integración runtime-serving + autorización de composición LIVE del `riskgeometry` (guardas hoy activas) — paquete preparado, no aplicado.
- **Materialización de las 62 SG**: manifest Owner con account policies RG por identidad (el builder ya está listo para admitirlas).
- **Revalidación histórica**: cadena G0–G5 en Go sobre la ventana sellada + D01 (unidad), D02 (horizonte) y D05 (funded-only) decididos por el Owner + presupuesto/ventana + receipts.
- **Caja/threshold**: el umbral 1/3 del Owner requiere unidad, resets, refunds y horizonte explícitos; hoy el reporte es descriptivo.
- **Regresión de cobertura**: 4 superficies grandes bajo el piso 95% por ramas pre-existentes (F7) — cerrar antes de declarar C06 completo.
- **REFUND de lifecycle**: existe la costura de contrato (emisor+proyector) pero no un disparador declarado; decidirlo es decisión de producto (economía), no de implementación.
- **Verificador no-GLM**: el contrapeso de modelo (F10) no se logró en este shot.

## TEST_COMMANDS_RECEIPTS

| Batería | Resultado |
|---|---|
| `go test ./v3/backtester/... -count=1` (suite completa) | conjunto de fallos **idéntico al baseline S03** (23 = 18 root + 5 cmd) tras integrar el patch tardío de D1; 0 regresiones nuevas (verificado por diff de conjuntos de nombres) |
| `go test ./v3/backtester -run 'TestS04_\|TestS04D1\|TestCandidate\|TestGateCanary\|Qualification' -count=1` | verde (regresiones nuevas + canaries + guard) |
| `go test ./v3/backtester/cmd/echo-backtest -run 'TestS04D1\|TestGateCanary\|Lab\|Migrate' -count=1` | verde |
| **Corpus del verificador (bytes intactos, vía copia a worktree aislado)** | **15/21 PASS, 5 FAIL** — los 5 FAIL son **exactamente las mutaciones TCR**: el flip NF2 ahora corre limpio (assert pedía error) y los rechazos de heterogeneidad/FUNDED-multi/segundo-perfil ahora nombran la causa correcta y más fuerte ("declare the sealed mm_catalog", "resolves to no declared profile v2"). Ninguno es defecto nuevo |
| Go-only sandbox sin python3 | ok + `lab migrate --materialize-v2` exit 0, 28 artefactos, 104 filas |
| `go build -trimpath -buildvcs=true ./v3/backtester/cmd/echo-backtest/` | limpio, SHA256 `9769039d…` |
| Capacidad | K=5 simultáneas: 5 compras, cash 2.380 USD, reconciliado, `CONTINUOUS_HORIZON_COMPLETE`, wall 5,05 s |
| `-race` | **NOT_EXECUTED** — el host no tiene gcc/cc (`go: -race requires cgo`); residual heredado de S03/S03R1; no se instaló infraestructura |

### TEST_CHANGE_REQUEST (mutaciones del corpus, con autoridad)

Dos TCR en `specs/FEAT-EF-CAMPAIGNS-GO/`: `TEST_CHANGE_REQUEST-C06-GO-S04.md` (controlador: sonda S03 F1–F4 → positivos; harness S03R1 NF2/G2/G6) y `TEST_CHANGE_REQUEST-C06-GO-S04-D1.md` (admisión: canary de item no-declarado → positivo histórico + nuevo negativo). Cada punto declara viejo/nuevo expected y autoridad. **No se movió ningún fixture/expected fuera de esas mutaciones declaradas**; los bytes del corpus del revisor se preservan en `~/echo-work/c06-s03/` y `~/echo-work/c06-s03r1/` sin editar.

## COVERAGE

**Medida válida: statement-based, denominador explícito** (`go tool cover` sobre el perfil `/tmp/s04-cover-final.out`; el "promedio de porcentajes por función" que usó el retorno S02 y el worker de la ola A **no** es la medida de policy y no se usa aquí).

**Diff-aware (statements nuevas del diff, desarrollo nuevo) — 817/1.027 = 79,6%:**

| Archivo (producción) | Diff-aware | Observación |
|---|---|---|
| `campaign_accounts_v2.go` | 92,5% | mejor superficie corregida |
| `campaign_v2_contract.go` | 89,7% | |
| `compose_account.go` | 86,5% | |
| `reproduce.go` | 85,7% | |
| `campaign_modes_v2.go` | 85,3% | |
| `campaign_composition.go` | 84,5% | |
| `campaign_migrate.go` | 77,7% | |
| `campaign_v2_sealed.go` (nuevo) | 74,4% | derivadores sellados |
| `campaign_v2_candidate.go` (nuevo) | 68,9% | loader/derivador de candidata |
| `replay.go` | 71,4% | replay nombrado de items |
| `vol_analytics.go` | 100% | |

**Por archivo completo (statements cubiertos/totales):** `campaign_v2_contract.go` 94,7% · `compose.go` 89,9% · `vol_analytics.go` 88,0% · `campaign_accounts_v2.go` 84,9% · `compose_account.go` 85,4% · `replay.go` 83,8% · `campaign_modes_v2.go` 83,6% · `campaign_composition.go` 82,5% · `platform_campaign.go` 83,0% · `campaign_migrate.go` 74,6% · `campaign_v2_sealed.go` 74,4% · `campaign_v2_candidate.go` 68,9% · `qualification_admission.go` 30,5% (superficie mayormente **pre-existente**, con suite propia en otro paquete) · **total archivos tocados 3.572/4.536 = 78,7%**.

**El piso 95% NO se alcanza**: ni por archivo ni en diff-aware (79,6%). Los huecos son ramas **fail-closed y de camino feliz** no ejercitadas —superficies nuevas (`campaign_v2_candidate.go` 68,9%, `campaign_v2_sealed.go` 74,4%, `campaign_migrate.go` 74,6%) y pre-existentes (`qualification_admission.go` 30,5% con su suite en otro paquete, `campaign_modes_v2.go` 83,6%). **F7 queda PARCIAL y declarado**: cerrar el piso es trabajo de otro shot, no un remiendo de este. Lo que sí se sostiene: los invariantes priorizados (economía exacta, identidad, causalidad, idempotencia, fail-closed, admisión sin bypass) tienen regresión permanente propia, y ninguna rama se maquilla con aserciones tautológicas.


## FINAL_GATE_RECEIPTS / EVIDENCIA INDEPENDIENTE

- **No hubo verificador final no-GLM**: el surface expone `account:zai-start-plan/GLM-5.3-Flash`; los despachos de subagente funcionaron intermitentemente (cuota muerta en dos tramos) y **todo** el trabajo —incluido el corpus del verificador re-ejecutado por el integrador— es del mismo modelo que el equipo autor. F10 queda **residual declarado**, sin etiquetar como GOD ninguna ejecución GLM.
- Lo que sí es independiente del autor del producto: el corpus del verificador (S03/S03R1) re-ejecutado por el integrador sobre el FINAL, con **bytes intactos**, y el trabajo de D1 (admisión/replay) ejecutado directamente por el integrador sobre archivos disjuntos del cluster del controlador.

## SUBAGENT_RECEIPTS

| Despacho | Modelo efectivo | Resultado |
|---|---|---|
| W-A1 — cluster del controlador (A+B+C+E2/E3/E4) | `clf-flash` GLM-5.3-Flash | **COMPLETE** — 6 commits (`7e3e5189`…`a411a2d1`), 17 regresiones + 6 de fail-closed, 2 TCR; 1 BLOCKED declarado (REFUND de lifecycle). Murió por límite de concurrencia del host a mitad: **reanudado con su WIP intacto** y completado |
| W-D1 — admisión E1/F8 + E5/NF4 | `clf-flash` GLM-5.3-Flash | **MURIÓ por límite de concurrencia** sin trabajo ⇒ ejecutado por el **integrador** en worktree propio (`88a0ad9d`, `4b63729d`), con TCR propio y canaries |
| W-D2 — migración honesta + builder GO_V2 | `clf-flash` GLM-5.3-Flash | **COMPLETE** — 3 commits (`069a13fa`, `42433580`, `12ec8357`); murió por corte de red a mitad ⇒ **reanudado con su WIP** y completado |
| W-CAND — candidatas v2 | `clf-flash` GLM-5.3-Flash | **COMPLETE en sustancia** (`9b9bfb3d` + `d2ed6804`, 8/8 tests verdes, artifacts escritos); murió por **cuota** tras dejar el trabajo hecho ⇒ cierre por el integrador (retirada del archivo debug temporal y commit del WIP de tests) |
| Integrador (este shot) | GLM-5.3-Flash | baseline, adjudication, D1, integración tardía (`baca3c60` + cierre documental `a22970c8`), corpus del verificador, Go-only, cobertura, K=5, push, este retorno |

Ningún resultado de subagente fue inventado; los dos workers completados y los dos muertos/reanudados quedan como están.

## REUSABLE_ASSETS

- `v3/backtester/campaign_v2_sealed.go` — loaders fail-closed de evidencia W0, ventana HIST y bundles + derivadores de bloques TG/RG sellados (consumible sin driver/RunState).
- `v3/backtester/campaign_v2_candidate.go` — `LoadSealedLabPreset(path, wantSHA256)` + `CampaignV2RequestFromSealedLabPreset`: la vía por la que una configuración sellada de lab se vuelve un request v2 materializado.
- `v3/backtester/campaign_migrate.go` — `BuildCampaignMigrationMaterialization` + `CampaignMigrationMaterializedRequest` (pipeline reutilizable; nuevas account policies ⇒ nuevas filas sin código nuevo).
- `v3/backtester/replay.go` — `ReplayCampaignResultJSON`: replay nombrado de items con verificación de digest del request sellado.
- `lab migrate --materialize-v2 --out DIR` — comando oficial versionado (manifiesto + requests por identidad).
- Corpus del verificador + generadores de fixture: `~/echo-work/c06-s03/`, `~/echo-work/c06-s03r1/` (bytes intactos); artifacts de este shot: `~/echo-work/c06-s04/` (candidata/, overlay/, notes/).
- Adjudicación de candidatas: `~/echo-work/c06-s04/notes/candidata-adjudication.md`.

## NOT_EXECUTED / UNKNOWN

- **NOT_EXECUTED**: `-race` (host sin gcc); campañas económicas históricas (D01/D02/D05 + cadena G0–G5 + budget/ventana Owner); re-ejecución de los 89 históricos; validación de reglas comerciales reales de props (perfiles TEST_ONLY); producción de la cadena de receipts G0–G5; widening del guard a otros documentos del linaje; cualquier merge a master/release/deploy/LIVE/compra/armado de trading.
- **UNKNOWN**: semántica QUOTE/MixedMinute en composición sin E2E (heredado); `prepareFixtureScope` multi-compartimento; régimen canario/WINDOW_REGISTRY del guard; consumo Pro/pool del host; el disparador de REFUND de lifecycle (no existe transición declarada consumidora).
- **Restricciones de modelo**: todo el trabajo de este shot es GLM-5.3-Flash; no hubo contrapeso no-GLM (F10). Los defectos ordinarios pre-existentes que S03/S03R1 declararon (clasificación de read-set, assertion no determinista del log de eventos) fueron corregidos con oráculo del contrato, no con TCR.

## RELEASE_ROLLBACK

- Rama `feature/ef-campaigns-go` publicada con readback (`origin` == local == `a22970c8…`). **Sin merge a master, sin release, sin deploy, sin compras, sin trading.**
- Rollback: revertir los commits propios del shot (17, incluido el commit documental final) sobre `062b6df7`; `062b6df7` es el punto exacto de rollback verificado (remoto y local), con su build reproducible `e4166366…`. Ningún catálogo, receipt, artifact sellado ni estado externo fue mutado por este shot.

## AGENTS_OS_PATHS_SHA

- Vault `main/` NO es git en este host (create-only + sincronización por el repo de publicación).
- Este retorno: `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-GO-S04-RETURN.md` (nuevo, create-only; **no** reescribe los retornos S02/S03/S03R1).
- Delta del planner: `10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md` (CURRENT_TASK_STATE + Bitácora por delta).
- Run-register: `80-agents/journal/agent-runs/2026-10-30-zcode-glm-5.3-flash-echo-c06-go-s04.md` (journal privado).
- Producto: `xKoRx/echo@feature/ef-campaigns-go@a22970c85d139c81c919aafac69f4bf6ceaf5dcd`; SDD del change: `specs/FEAT-EF-CAMPAIGNS-GO/{SPEC,PLAN,TASKS,VERIFICATION}.md` + 2 TCR.

## PRO_CHAT_POOL_DELTA

UNKNOWN (sin observabilidad del pool desde esta superficie; identidad de modelo efectiva `account:zai-start-plan/GLM-5.3-Flash` confirmada por el surface; 4 subagentes despachados, 2 completados, 2 reanudados tras muerte del host).

## Fuentes

[[EF-CAMPAIGN-MODES-GO-S03-RETURN]] · [[EF-CAMPAIGN-MODES-GO-S03R1-RETURN]] (adjudicación F1–F10/NF1–NF4 y paquete A–E) · [[EF-CAMPAIGN-MODES-DESIGN]] C06 §3/§4/§5/§6/§10/§11/§12 · [[Echo Futures — Optimización de Campañas]] (planner único, R01–R12/A01–A16) · [[EF-CAMPAIGN-MODES-I0-LOCAL]] (contrato común) · [[Echo Futures — Runtime Pools]] (R6 y el frente ECHO_FUTURES_FIRST_LIVE_TRADE) · runbook de cualificación (G0–G5) · repo `xKoRx/echo@a22970c8` (AGENTS.md, CONSTITUTION.md, `.agents/rules/08-09`, `specs/FEAT-EF-CAMPAIGNS-GO/`) · evidencia física en `~/echo-work/c06-s04/`, `~/echo-work/c06-s03/`, `~/echo-work/c06-s03r1/` · R03 (`v3/backtester/tools/tradesgerard/campaign-lab/correction/s04/lab-r03/R03-DECISION-STRATEGIES.md`).
