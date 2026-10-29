---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Optimización de Campañas]]"
  - "[[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]]"
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---


# EF-S04-INTEGRATION-RECONCILIATION

## Propósito

Reconciliar el retorno de integración pre-ClutiFX con GitHub y preservar la evidencia exacta que falta para aceptar S04. Inspección CLOUD read-only del manager y apoyo ONE-SHOT; ninguna ejecución física ni cambio de producto. Fecha local: 2026-10-28 America/Santiago.

## Contenido

**SOURCE_RECONCILED_WITH_MATERIAL_FINDINGS. S04_SEMANTIC_ACCEPTANCE: BLOCKED_EVIDENCE.** La existencia del merge se acepta como hecho; la equivalencia de sus 89 identidades no se acepta aún. I0 contractual/reporting puede usar este source para una salida descriptiva aislada y conservadora, sin habilitar campañas.

El informe de integración y su verificador no se reescriben. S04-F01 y S04-F02 se adjudican contra el alcance que realmente acreditan: contradicción de una afirmación del retorno y ausencia del guard en el corte, respectivamente. No se infiere que todas las campañas históricas cambiaron ni que ocurrió ejecución indebida.

## 1. Corte observado

- Echo master observado: `2baf319ddcba622d9557bc9f23a13787b44c58a7`.
- Master base informado y comprobado como ancestro: `347eee8bdab7f7628629af6383d1e45520815abd`.
- Linaje integrado: `ae1b09bc10370806f7648f076c5fa0825c9efa4e`; compare confirma merge-base exacto y behind_by=0.
- Merge: `2188ac3e23d4e4a73ca0edb9aad952029deec951`, padres exactos 347eee8b + ae1b09bc.
- Árboles recursivos completos: base 4466 entradas, master 4877; ambos truncated=false.
- Diferencia completa por SHA de blobs: 421 archivos; 369 añadidos, 52 modificados, 0 borrados.
- Fuera de v3/backtester, v3/sdk y v3/core: únicamente PLAN.md, SPEC.md, TASKS.md y VERIFICATION.md de specs/FEAT-CHALLENGE-HISTORY.
- El endpoint compare devolvió sólo 300 archivos; se reemplazó ese inventario incompleto con el delta de árboles completos. No usar el compare como censo exhaustivo.

## 2. Estado por capa

| Capa | Estado observado | Alcance |
|---|---|---|
| SOURCE | DEMOSTRADO | Ref, ancestry, merge, catálogo y superficie completa verificados vía GitHub |
| BUILD | OWNER/EXECUTOR_REPORTED | Agent-run declara build frío 11 módulos en retorno del Owner; no receipt binario sellado de este merge recuperado |
| TEST | EXECUTOR_REPORTED_WITH_LIMITATIONS | Agent-run resume igualdad de failure sets y 2 regresiones corregidas; faltan logs/manifiesto de nombres+causas+inputs para recomprobar. Race NOT_EXECUTED sin gcc |
| INDEPENDENT_REVIEW | REPORTED, FULL_RETURN_NOT_RECOVERED | Agent-run afirma CANDIDATE_APPROVED read-only; no informe independiente completo de este merge recuperado en remoto |
| ACCEPTANCE | UNKNOWN / OWNER_REVIEW | Presencia en master no cierra gate; nueva discrepancia semántica exige adjudicación |
| DEPLOY | NONE_REPORTED / PROD_FROZEN_BY_OWNER | Sin despliegue o trading nuevo autorizado; no inspección física de producción en este worker |

Agent-run persistido: `main/80-agents/journal/agent-runs/2026-10-28-zcode-glm-5.3-flash-echo-backtest-runtime-integration.md`, blob `64b157b32c84baed88a0d002f20889114bd615cb`.
Control persistido: `main/10-projects/Echo Futures/artifacts/runtime/EF-BACKTEST-RUNTIME-INTEGRATION-PLAN.md`, blob `18a03ba33d63b38572d8d10d8ff275caa930a5a2`.
El planner único aún contenía IN_PROGRESS_OWNER_REPORTED en su cabecera observada; el control de integración ya dice ejecutada. Resolver por delta, sin otro planner.

## 3. Catálogo exacto y preservación de bytes

- Módulos Strategy: s1, s2, tg, fbc, orb, mr; fixture sólo BACKTEST/EXACT_REPLAY.
- MM: gerardmm, tgmm, riskgeometry.
- Nativos: 26 (TG 4; FBC 4; ORB CH300 3; MR 10; ORB NATIVE C01..C05 5).
- SG ejecutables censales: 63, con perfiles ATR14 bruto 250/500/750 USD, 1:1.
- Total manifiesto: 89 = 26 NATIVO + 63 SG; 15 alias excluidos de la ejecución.
- Lista exacta derivada de catálogo/manifiesto en `EF-S04-CATALOG-RECONCILIATION.json`, sólo snapshot de evidencia; los catálogos originales de Echo conservan autoridad.
- `catalog-v1.json` blob `b2abed68214c96f913d3266a02d887e7fc15cb74` idéntico en ae1b09bc y 2baf319d.
- `R02-HISTORICAL-MANIFEST.json` blob `0a2aa46ccc005df50aedf18543fefd1cf2335dad` idéntico en ambos.
- Esta igualdad NO demuestra equivalencia del intérprete/ejecución.

### Addendum I0-S1 — evidencia de planes sellados (recuperación LOCAL reportada)

Retorno I0-S1 en Agents-OS `8414341b3eb3818b39ae7966f646338a8cefca5f`: censo de planes nativos r4 **52/52** (FULL/CANARY), r5 **15/15**, hefesto **5/5** y R01 **26/26**, todos con `entry_budget_policy=STRATEGIC_ENTRY_BUDGET_V1`. Las SG observadas carecen del campo. Localizadores en `EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN.md`; censo con hashes reportado en `/tmp/s04-f01-census.json` (ruta LOCAL, existencia remota no comprobada por manager). **EXECUTOR_REPORTED_WITH_PLAN_CENSUS**. Esto refuta «policy vacío» para los planes observados, pero no prueba que cada resultado histórico haya cambiado. No sumar raíces como identidades distintas. Pendiente prueba Go focal del comportamiento V1 antiguo/nuevo en R>headroom positivo, igualdad y floor; no renombrar políticas ni reejecutar 89 campañas automáticamente. **S04_SEMANTIC_ACCEPTANCE=BLOCKED_EVIDENCE**.

## 4. S04-F01 — contradicción material del recibo: nativos y EntryBudgetV1

**Confirmado estáticamente:** el retorno afirma «nativos = shrink legacy con entry_budget_policy vacío» para descartar efecto de la colisión V1. El catálogo actual y del linaje declara **STRATEGIC_ENTRY_BUDGET_V1 en los 26 nativos**, y el materializador transmite ese valor. La semántica V1 difiere entre el source ae1b09bc y master integrado.

No se afirma que todos los planes efectivos de R03 usaran V1, porque esos bytes sellados están fuera de Git y no fueron recuperados. Esa es la dependencia exacta. Si los planes efectivos usaron vacío, la afirmación de esa corrida podría acreditarse; no convierte al catálogo/materializador actual en equivalente.

### Evidencia A — catálogo

Archivo `v3/backtester/tools/tradesgerard/campaign-lab/catalog-v1.json`, blob `b2abed68214c96f913d3266a02d887e7fc15cb74`, igual ambos refs:

```json
{
  "candidate_id": "TG-CH300-F0",
  "family": "TG",
  "version": 1,
  "strategy_module": "tg",
  "strategy_id": "tg-main",
  "signal_timeframe": null,
  "filters": [
    {
      "kind": "TG_FILTER",
      "filter": "F0"
    }
  ],
  "params": {
    "stop_rho_num": 1,
    "stop_rho_den": 1,
    "tick_size": "0.25",
    "filter": "F0"
  },
  "mm": {
    "module": "tgmm",
    "scaling_mode": "NO_ADDS",
    "risk_ref": "300",
    "target_ref": "300",
    "budget_semantics": "NET_TARGET_LEGACY_V1",
    "economic_minimum_policy": "ECONOMIC_MINIMUM_V2",
    "entry_budget_policy": "STRATEGIC_ENTRY_BUDGET_V1",
    "eval_daily_goal": "900",
    "eval_pass_target": "3000",
    "internal_pause_loss": "1000",
    "fee_per_side_per_contract": "2.49",
    "slippage_ticks": 1,
    "minimum_spread_ticks": 2
  },
  "phase": "NATIVE_REPLAY",
  "campaign_policy": "CONTINUOUS_V1",
  "purchase_window_scenario": "NY_1000_OBS_V1",
  "provenance": {
    "source": "v3/backtester/tools/tradesgerard/challenge-first/generate.py ROWS",
    "repo": "xKoRx/echo",
    "commit": "20c73fd4b02c5747ff87346407210f389280033d",
    "verified_remote_cut": "07cca9d399f3a4045aadb151dfcec612f192db96"
  }
}
```

### Evidencia B — materializador

Archivo `v3/backtester/tools/tradesgerard/campaign-lab/research_lab.py`, blob `4ab19ae18b8705ff57beda0c0ab7137b4de48b0f`, función native_mm_block, líneas 320–345:

```python
def native_mm_block(candidate):
    """The candidate's OWN native TGMM money-manager block (300/300 or
    500/250 net targets, policy, ADD) — the economy of THIS strategy, never
    the base plan's leftover block. Modeled spread offsets carry the sealed
    native constant (challenge-history builder)."""
    mm = candidate["mm"]
    if mm.get("module") != "tgmm" or mm.get("budget_semantics") != "NET_TARGET_LEGACY_V1":
        fail(f"candidate {candidate['candidate_id']} has no native TGMM block")
    tg = {
        "economic_minimum_policy": mm["economic_minimum_policy"],
        "entry_budget_policy": mm["entry_budget_policy"],
        "minimum_spread_ticks": mm["minimum_spread_ticks"],
        "modeled_bid_offset_ticks": 1,
        "modeled_ask_offset_ticks": 1,
        "risk_ref": canonical_decimal(mm["risk_ref"], "risk_ref"),
        "target_ref": canonical_decimal(mm["target_ref"], "target_ref"),
        "eval_daily_goal": canonical_decimal(mm["eval_daily_goal"], "goal"),
        "eval_pass_target": canonical_decimal(mm["eval_pass_target"], "pass_target"),
        "internal_pause_loss": canonical_decimal(mm["internal_pause_loss"], "pause_loss"),
        "fee_per_side_per_contract": canonical_decimal(mm["fee_per_side_per_contract"], "fee"),
        "slippage_ticks": mm["slippage_ticks"],
    }
    if "add_policy" in mm:
        tg["add_policy"] = dict(mm["add_policy"])
    return {"currency": "USD", "plans": None, "scaling_mode": mm["scaling_mode"],
            "mm_module": "tgmm", "tg_mm": tg}
```

### Evidencia C — intérprete source ae1b09bc

Archivo `v3/sdk/futures/strategies/tgmm/tgmm.go`, blob `59437bb851422d26461600438319fbcb872ec679`, líneas 252–270:

```go
	risk, target := m.requestedBudget(phase, pend)
	origin := "ref"
	if targetRef.Cmp(pend) > 0 {
		origin = "remanente"
	}
	head := m.headroom(in)
	// Role separation (mandate THREE STRATEGIES V2.1 §2): under the
	// strategic entry-budget policy the remaining daily/EOD room is the
	// RiskFinalizer's authority over the real proposal, never a
	// manager-side pre-veto — the headroom only stays as decision evidence
	// (tg_headroom). The legacy configuration keeps its historical shrink.
	if m.cfg.EntryBudgetPolicy != EntryBudgetV1 && risk.Cmp(head) > 0 {
		risk.Set(head)
		target.Quo(risk, new(big.Rat).Quo(riskRef, targetRef))
		origin = "headroom"
	}
	if target.Sign() <= 0 || risk.Sign() <= 0 {
		out.DiagnosticReason = "TG_NO_RISK_HEADROOM"
		return out, nil
```

### Evidencia D — intérprete master 2baf319d

Mismo archivo, blob `d6aae6dbecf41490f15752cb34db8c7a367ccb69`, líneas 260–297:

```go
	risk, target := m.requestedBudget(phase, pend)
	origin := "ref"
	if targetRef.Cmp(pend) > 0 {
		origin = "remanente"
	}
	head := m.headroom(in)
	if risk.Cmp(head) > 0 {
		switch m.cfg.EntryBudgetPolicy {
		case EntryBudgetV1:
			// The entry budget is never shrunk to the leftover headroom:
			// declining is the only legal response. The platform authority
			// owns the pause/permanent decision from the same R_ref.
			out.DiagnosticReason = "TG_ENTRY_BUDGET_EXCEEDS_HEADROOM"
			out.MMState["tg_entry_budget_policy"] = EntryBudgetV1
			out.MMState["tg_headroom"] = head.RatString()
			return out, nil
		case EntryBudgetUnclippedV1:
			// R6 §12F (OQ(1) adopted): a POSITIVE floor remainder never
			// clips, rejects or retires the entry — requestedBudget(pending)
			// keeps determining R/T. A NON-positive headroom is a REAL
			// crossed floor (internal pause / daily loss / provider floor):
			// its own decline treatment is conserved (breach real SÍ
			// bloquea). EconomicMinimumV2 below stays the admission
			// constraint of the integer quantity.
			if head.Sign() <= 0 {
				out.DiagnosticReason = "TG_NO_RISK_HEADROOM"
				out.MMState["tg_headroom"] = head.RatString()
				return out, nil
			}
		default:
			risk.Set(head)
			target.Quo(risk, new(big.Rat).Quo(m.cfg.RiskRef, m.cfg.TargetRef))
			origin = "headroom"
		}
	}
	if target.Sign() <= 0 || risk.Sign() <= 0 {
		out.DiagnosticReason = "TG_NO_RISK_HEADROOM"
		return out, nil
```

### Prueba focal pendiente (NOT_EXECUTED)

LOCAL debe recuperar, sin reejecutar las 89 campañas, planes/configs efectivos sellados de las 26 nativas y publicar censo por campo entry_budget_policy y hash. Contrastar generador/materializador actual con lo realmente corrido.

Construir un fixture desde los journeys existentes con las demás precondiciones satisfechas, floor positivo suficiente para al menos un NQ, riesgo solicitado mayor que headroom positivo (ejemplo conceptual R=300 y headroom=250; ajustar geometría a los tipos/piso reales). Comparar explícitamente:
1. V1 source ae1b09bc no realiza ese veto de manager.
2. V1 master devuelve TG_ENTRY_BUDGET_EXCEEDS_HEADROOM antes de propuesta.
3. Unclipped master deja la resolución de sala positiva al finalizer.
4. Controles headroom=requestedRisk y headroom<=0.
No declarar igualdad de eventos cuando sólo la identidad o la política cambió; no cambiar runtime para recuperar resultados históricos.
No sustituir policy silenciosamente en 89 presets: una migración prospectiva necesita identidad/política propia y la evidencia histórica conserva su intérprete.

## 5. S04-F02 — guard de cualificación no está en el corte integrado

El tree master completo no contiene qualification_guard.py. research_lab.py::_run_one (líneas 716–727) invoca subprocess.run directamente; cmd_resume --execute llama ese mismo método. El guard de cualificación de ClutiFX posterior sigue siendo autoridad documental, pero no se debe presumir código presente en master pre-ClutiFX.

I0 estrictamente reporting/no-spawn puede avanzar con esta limitación expresa. Antes de cualquier ejecución nueva reconciliar/adaptar la admisión vigente de run y resume a este corte por trabajo explícito, sin merge global de ClutiFX ni bypass G4.

## 6. Mapping acotado para I0 (sin diseñar implementación)

| Superficie actual | Punto de extensión/reporting a inspeccionar | Contrato que protege |
|---|---|---|
| campaign-lab/campaign_lab.py | validación/materialización y digest | identidad y compatibilidad de schemas |
| campaign-lab/research_lab.py::_census | cuenta PURCHASE por account_id; hoy exige account record | F01 requiere distinguir compra pagada/provisión/intento; no tratar ausente como 0 |
| research_lab.py::characterize | reconciliación per-account desde fills, estado y ledger | alcance último RunState vs campaña; UNKNOWN granular |
| research_lab.py::row_from_char | adapta campos al selector legacy | contiene defaults 0: nuevo reporte no debe convertir desconocido en 0 ni alimentar adjudicación legacy como si fuese nueva |
| research_lab.py::adjudicate | piso histórico Fraction(1,4) | conservar 25% como identidad legacy; nuevo 1/3 opt-in explícito |
| campaign-lab/test_research_lab.py | tests L1–L5, negativos y CLI | preservar existentes; fixtures nuevos por vía SDD/TCR cuando toque |
| v3/backtester/platform_campaign.go y platform_research.go | lectura source de contrato/salidas | no mutar driver, fees, Strategy/MM/Provider en I0 |

No existe archivo research_campaign.py en el tree consultado. No inventarlo como existente ni usarlo como autoridad.
Tests actuales pertinentes: test_purchase_requires_a_backing_event; test_null_accounts_zero_purchases_is_a_valid_shape; test_pause_variants_count_pending; test_multi_account_reconciles_per_account_and_last_account_scope; test_gz_and_plain_traces_are_equivalent; test_run_refuses_non_reusable_and_reuses_terminated; test_resume_classifies_everything_and_execute_is_explicit; test_resume_execute_restarts_into_fresh_byte_intact_dirs; test_23p81_and_zero_and_truncated_and_engine; test_valid_confirmation_with_policy_accepts_and_without_is_unset.

## 7. Entrada y SDD del repo

- AGENTS.md blob 2e4b7ad1146d639e18d3eed6c270bd47fb9855de.
- v3/backtester/README.md blob 66267be80dfc3f63ec44f5e7327ce4c40cdc3813.
- CONSTITUTION.md blob fcf7f9f190e8f65ab844b8ba139357dc77b32da5.
- .agents/rules/08-sdd-governance.md blob 014abca162476bb680c409f7ab7379a049049e48.
- .agents/rules/09-sdd-phase-permissions.md blob b1c38ac454291121e345007fcfe11b29c925faf8.
- SPECIFY→PLAN→TASKS→IMPLEMENT→VERIFY con Allowed Files; coordinator no edita código; verifier no cambia producción; cambios a tests existentes mediante TEST_CHANGE_REQUEST adjudicado.

Branches remotos enumerados: 81 (<100, respuesta completa). No se observó branch de campaign-modes/I0. integration/backtest-runtime tampoco apareció entre remotas. Prefijo propuesto para futuro slice: feature/ef-campaign-modes-i0, **NO creado**. LOCAL debe primero censar trabajo/branches locales del ejecutor vigente y reutilizar el slice correcto si existe; si no existe, crear desde 2baf319d o descendiente reconciliado explícitamente. No usar un branch antiguo S04 como nueva base por inercia.

## 8. Handoff mínimo LOCAL

1. Recuperar receipts originales de integración: source/build identity, comandos y logs por suite, failure sets con causas, informe completo del verificador, checksums. No rehacer suites de infraestructura ajenas.
2. Resolver S04-F01 con planes sellados y fixture de frontera; resultado REPORTED/DEMONSTRATED/UNKNOWN por claim.
3. Acreditar guard de admisión o mantener ejecución bloqueada; I0 no spawnea motores.
4. Mapping exacto de artefactos legacy consumibles en I0; el reporte puede producir UNKNOWN y preservar inputs byte-intactos.
5. Devolver diff/propuesta de corrección focal, sin cambiar semántica de runtime ni criterios económicos.

## Fuentes

- https://api.github.com/repos/xKoRx/echo/branches/master
- https://github.com/xKoRx/echo/commit/2baf319ddcba622d9557bc9f23a13787b44c58a7
- https://github.com/xKoRx/echo/commit/2188ac3e23d4e4a73ca0edb9aad952029deec951
- https://github.com/xKoRx/echo/compare/ae1b09bc10370806f7648f076c5fa0825c9efa4e...2baf319ddcba622d9557bc9f23a13787b44c58a7
- https://api.github.com/repos/xKoRx/echo/git/trees/347eee8bdab7f7628629af6383d1e45520815abd?recursive=1
- https://api.github.com/repos/xKoRx/echo/git/trees/2baf319ddcba622d9557bc9f23a13787b44c58a7?recursive=1
- https://github.com/xKoRx/echo/blob/2baf319ddcba622d9557bc9f23a13787b44c58a7/v3/backtester/CATALOG.md
- https://github.com/xKoRx/echo/blob/2baf319ddcba622d9557bc9f23a13787b44c58a7/v3/backtester/tools/tradesgerard/campaign-lab/catalog-v1.json
- https://github.com/xKoRx/echo/blob/2baf319ddcba622d9557bc9f23a13787b44c58a7/v3/backtester/tools/tradesgerard/campaign-lab/research_lab.py
- https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/sdk/futures/strategies/tgmm/tgmm.go
- https://github.com/xKoRx/echo/blob/2baf319ddcba622d9557bc9f23a13787b44c58a7/v3/sdk/futures/strategies/tgmm/tgmm.go
- https://github.com/xKoRx/agents-os/blob/844e777f95e01e5268f8f7cd98de5299765ce0f2/main/80-agents/journal/agent-runs/2026-10-28-zcode-glm-5.3-flash-echo-backtest-runtime-integration.md

## Retorno del apoyo ONE-SHOT y disposición del manager

- OUTCOME: SOURCE_RECONCILED_WITH_MATERIAL_FINDINGS.
- PHYSICAL_VERIFICATION: NOT_EXECUTED.
- REUSABLE_ASSETS: this memo + s04-catalog-identities.json.
- AGENT_RUN: el apoyo retornó la inspección estática al único writer; registro atribuible en [[2026-10-28-chatgpt-astra-echo-s04-source-review]]. No prueba ejecución física.
- FEEDBACK: GitHub compare 300-file cap hides remainder; compare full Git trees (truncated=false) for surface proof. Broad fetch_commit payload was oversized; prefer metadata + exact file/blob reads. No policy update proposed from this alone.
- PRO_CHAT_POOL_DELTA: UNKNOWN (no confirmed pool accounting).
- OWN_WORKER: terminado, resultado persistido por el manager como único writer. Cierre restringido al apoyo de evidencia; no cierra coordinador/programa. El manager corroboró catálogo, native_mm_block, las dos versiones TGMM y el agent-run de integración.

