# SQX144 — Certificación integral de campaña E2E NDX (5 finalistas por grupo, frontera pre-Echo)

**Fecha:** 2026-10-16 · **Sesión:** ZCode/GLM-5.3-Flash one-shot (LOCAL EXECUTION & REMEDIATION LEAD) · **Primary Technical Manager:** ChatGPT · **Owner:** KoR

**Veredicto:** `SQX144_FULL_CAMPAIGN_IN_PROGRESS` — la campaña integral está despachada y ejecutándose físicamente en la flota 144; la certificación técnica del arranque completo (flota alineada, CFX operativos, cadena de despacho, reposición armada) está demostrada con evidencia; el funnel completo y las cuotas por grupo quedan pendientes de la corrida (24–48 h estimadas de flota).

---

## 1. Resumen ejecutivo

El mandato pedía ejecutar una campaña nueva desde las etapas iniciales de Forge hasta finalistas locales sobre SQX 144, NDX H1 Long, Robust V2 y MT5, con cinco finalistas por cada grupo real de resultados y cero entrega a Echo. Esta sesión recuperó la configuración E2E histórica realmente ejecutada, la adaptó a 144 + NDX + Robust V2, sanó la flota para que los CFX del owner funcionen en las instalaciones 144, probó físicamente las capacidades críticas por host y despachó la campaña como **ForgeCampaign V2** con reposición canónica de candidatos.

Estado al cierre de la sesión: **wave 1 en ejecución** (builder corriendo en Kronos bajo el worker 0.2.144), flota 3/3 sana, matriz de capacidades críticas 3/3 con probes físicos, y todos los artefactos de la campaña congelados por SHA256 con lineage verificable.

## 2. Configuración E2E histórica recuperada

La configuración de prueba E2E anterior a la campaña de múltiples runs (wave2b y sus continuaciones wave3p–t) es la **ForgeCampaign `0ce72173-b629-4ca4-bf4c-e7e586792e72`** (CERT-F05-01, 2026-09-21): `COMPLETED / TARGET_REACHED` con wave única `forge-0ce72173-…-w000001` (FlowRun `9d1b41ac-7f3f-4dd2-ac4c-e0938bd8dcaa`), 3 finalistas, ranking global `mt5-final-fidelity-ranking` y promoción de la era CERT.

- **Fuente durable:** PG de flow, tabla `sqx.configs`, id `55b2d998-563a-4015-b38a-f3fc77963d52`, `config_id=XAUUSD_cert-f05-02_v1_wcert-f05-02` (extraída con helper RO efímero; snapshot completo en `HISTORICAL-E2E-BASE-SPEC-cert-f05-02.json`).
- **Cadena ejecutada por esa config:** `builder → overview_exporter → group(retester → optimizer) → evaluate_wfm → select_robust_run → apply_selected_run → final_reretester → trade_list_exporter → mt5_exporter → mt5_compiler → mt5_backtesting`, con classification `indicator_signature.v1`, early ranking `weighted_combination_minmax` per-logical-type, score `mt5_fidelity_shadow.v1`, ranking `score_descending.v1` y promotion `finalist_promotion`.
- **No es** el ejemplo `input/example/config.json` tal cual: el ejemplo es el mismo esqueleto con fixture XAUUSD; la config ejecutada recuperada tiene su propia identidad, wave y promotion 2.0.0 (era CERT con ingest Echo, hoy prohibida por este mandato → la nueva campaña usa promotion **1.0.0** local).
- **Mecanismo de reposición:** el controlador **ForgeCampaign V2** (`sqx-forge-campaign.v2`, `forge-campaign-intent.v2`) con `target_finalists`, `max_waves` y `max_builder_candidates_per_wave` (waves NEW_BUILDER_SUPPLY con `BuilderSupplyBatchRef` y dedupe insert-once por producer authority). Este es el mecanismo canónico existente y es el que usa la nueva campaña.

## 3. Delta aplicado (NDX + SQX 144 + Robust V2 + MT5 + grupos)

| Eje | Histórico | Campaña nueva |
|---|---|---|
| Instrumento | XAUUSD | **NDX** (dataset ejecutor `USATECHIDXUSD_dukascopy_UTC02`, decisión owner en vivo) |
| Builder | fixture builder_test (XAUUSD) | **Build_BR_G1_H1_144.cfx** (familia del cohort real BR_G1, NDX H1 Long) |
| Funnel económico | builder → Full directo | + **Precision global → ranking per-logical-type top_n=5 → selección TopProjection** (freeze owner R10) |
| Robustez | WFM V1 defaults | **`robust_run_selection_v2` 0.35 / 0.01 / 0.01** (contrato congelado §8) |
| Final reretester + MT5 | XAUUSD | **reretesterfull.cfx (a51c1cc3, intacto)** + MT5 **NDX_SQX** H1 2025.07.01→2026.10.09 model 4 (contrato wave3t; períodos comparables por diseño) |
| Ranking final | global top_n=5 | global **top_n=40** (todos los elegibles ordenados); finalistas por grupo = prefijo por grupo del snapshot durable, con ClassificationSnapshot como autoridad de membresía |
| Promotion | 2.0.0 (entrega Echo) | **1.0.0 local** (cero Echo: sin seal/handoff, sin ingress, sin deployments) |
| Paralelismo | secuencial | **fan-out 3 hosts**: Precision batch 90 / Full batch 10 / Optimizer batch 1, todos `max_parallel: 3` (R12) |

## 4. Grupos esperados (autoridad y pertenencia)

Origen de la agrupación: **ClassificationSnapshot** de la campaña (`indicator_signature.v1` sobre la evidence del producer Precision), precedido por el precedente wave1c (FlowRun `254977a0`): 8 tipos lógicos con distribución 431/232/28/16/11/5/2/2. Los 8 grupos esperados y su criterio de pertenencia (firma de indicadores) están volcados en `SQX144-CAMPAIGN-FUNNEL-BY-GROUP.csv`; la autoridad definitiva de cada grupo es el snapshot que selle la campaña al cierre del group Precision (`ClassificationSnapshotRef` durable). Objetivo por grupo: **5 finalistas elegibles**; los grupos sin oferta real aparecerán con déficit legítimo, sin relleno cruzado ni filtros relajados.

Nota de alcance: el ranking final del runtime vigente es GLOBAL por contrato (`RankingSpec` frozen v1; promotion resuelve exactamente un ranking). La semántica por grupo se obtiene aplicando el mismo contrato `score_descending` al subconjunto del grupo dentro del snapshot durable — sin algoritmo nuevo ni framework de cuotas — y quedará explícito en los CSV de finalistas.

## 5. Correcciones y remediaciones ejecutadas

1. **Datasets ausentes en las instalaciones 144 (3/3 hosts):** los CFX del funnel del owner referencian `USATECHIDXUSD_darwinex` (M1 2016→2026-04), presente solo en los árboles raíz 142. Remediación: porté los datasets `USATECHIDXUSD{,_darwinex}` del árbol raíz al árbol 144 de cada host + filas `DATA` (IDs 213/214) en `data.db` (backup `data.db.bak-20261016-precfix`), sin sqcli activo.
2. **Diagnóstico del fallo "Project has unresolved resources":** el `<Chart symbol>` del Setup es la referencia que resuelve datos; el bloque `<Resources><Symbols>` del CFX original declara una entrada (darwinex, source=2) que ya no resuelve en 144 y **envenena el proyecto entero**. Controles físicos que lo demuestran: swap de Chart sobre recurso NDX intacto ⇒ corre; remoción de Resources + swap de Chart ⇒ corre; cualquier variante con el bloque Resources darwinex ⇒ falla.
3. **Adaptación owner-dirigida de CFX (en vivo):** el owner instruyó rehacer los CFX para `USATECHIDXUSD_dukascopy_UTC02`. Adaptación mínima aplicada a 4 CFX (swap de Chart symbols + remoción del bloque Resources; economía, períodos, spread, comisiones y swap intactos): `RetestPrecision_144` (99eaf5a2→2cd587f0), `RetestFull_144` (91ca1ac0→14d55e98), `Optimizer_144` (4b282d8b→d4d9c0aa), `Build_BR_G1_H1_144` (786cdaea→507507c5). `reretesterfull.cfx` (a51c1cc3) queda **intacto** (su dataset NDXm tick UTC02 resuelve nativamente en 144). Detalle y SHAs: `ADAPTATION-REPORT.json`.
4. **StopCondition del Builder:** el build del owner está en `type="never"` (válido solo en GUI; sqcli headless lo rechaza: "Build task is configured to never stop"). Adaptación headless registrada: `databank-full passedStrategies=750`. El `MaxStrategies=1000` del owner se conserva y es el límite real observado (la probe generó exactamente 1000 en ~30 min a 2500% CPU).
5. **Caché de datos no escribible (`internal/testfiles`):** causa del `FileNotFoundException` → `NPE loadedData null`. Fix con sudo kor: `chmod -R a+rwX` (misma clase del fix sancionado del 2026-10-14). Tras el fix, la probe de Precision completa en 10.14 s.
6. **CFX faltante en Kronos:** `Build_BR_G1_H1.cfx` no existía en Kronos (había `Build_BR_G1.cfx`); propagado desde Zeus (SHA verificado; el archivo local de Kronos quedó intacto).

## 6. Cobertura por host (matriz resumida; detalle en SQX144-WORKER-CAPABILITY-MATRIX.csv)

| Capacidad | Zeus | Hera | Kronos | Evidencia |
|---|---|---|---|---|
| Worker 0.2.144 (SHA == manifest) | PASS | PASS | PASS | sha256sum == `5bb27830…` 3/3 |
| sqcli 144 + licencia operativa | PASS | PASS | PASS | probes físicas de retest |
| Retest Precision sobre dukascopy_UTC02 (CFX adaptado) | PASS 10.14s | PASS 20.88s | PASS 30.54s | `probe-logs/precision-*.log` |
| Build headless (CFX adaptado + stop condition) | PASS (1000 generadas) | — | **wave1 en curso** | `probe-logs/builder-zeus.log` |
| MT5 worker + NDX_SQX data | n/a | n/a | PASS (0.2.144 ba4948d4; .hcc 2024-2026) | manifest + bases/Custom |
| Full/Optimizer/Reretester/MT5/fidelity/ranking/promotion | PENDING_CAMPAÑA | PENDING_CAMPAÑA | PENDING_CAMPAÑA | la wave1 ejercita cada etapa; réplicas de probe para hosts que no las ejecuten quedan como pendiente de cierre |

## 7. Campaña despachada (refs durables)

- **CampaignRef:** `569c152c-322d-404a-92c1-0ee3ae1d8afc` · intent token `2fab2660-e194-49cd-a4e1-593cfb65c2cd` · workflow `sqx-forge-campaign-v1-2fab2660-…` (run `01a1451a-cef7-721b-9e99-ded192c11831`, namespace `sqx-prop`).
- **Wave 1:** FlowRun `34b95fd6-930a-462a-8479-38fe132e50f7` RUNNING (desde 2026-10-16T14:25:47Z), builder ejecutándose en Kronos (`sqcli 144 -project custom`, staging con CustomAnalysis del productor overview inyectado).
- **Límites declarados antes del dispatch:** `target_finalists=40` (5×8 grupos), `max_waves=2` (reposición con supply nuevo de builder), `max_builder_candidates_per_wave=1000` (= MaxStrategies del builder del owner), Precision batch 90 / Full batch 10 / Optimizer batch 1, `max_parallel 3`.
- **Spec congelado:** `flow-camp-ndx144.json` SHA `8335d72a…` (SPEC_VALID + WAVE1_VALID por `runtime.ValidateWorkflowSpec` + materialización de campaña), paquete y watcher congelados en `SHA256SUMS-freeze-20261016.txt`.
- **Promoción:** `finalist_promotion@1.0.0` local. Cero `forge_seal_handoff`, cero ingress Echo, cero deployments.

## 8. Comandos exactos de consulta (monitoreo)

```bash
# Estado de campaña y waves
cd /home/kor/go/src/github.com/xKoRx/symphony && ENV=production go run ./sqx/cmd/sqx-flowkit campaign get 569c152c-322d-404a-92c1-0ee3ae1d8afc
ENV=production go run ./sqx/cmd/sqx-flowkit run stages 34b95fd6-930a-462a-8479-38fe132e50f7
# Actividad por host
python3 /tmp/korsh.py kronos 'pgrep -af sqcli | grep -v pgrep | head -3; tail -3 /var/log/symphony/symphony-worker.log | cut -c1-200'
```

## 9. Pendientes al cierre de esta sesión

- **Funnel completo y cuotas por grupo:** la wave 1 sigue corriendo (builder → precision → selección → full → optimizer → apply → reretester → MT5 → fidelity → ranking → promotion). Veredicto definitivo A/B cuando la campaña termine; `SQX144-CAMPAIGN-FUNNEL-BY-GROUP.csv` y `SQX144-FINALISTS-BY-GROUP.csv` se llenan con los snapshots durables.
- **Probes de réplicas** para hosts que no ejecuten físicamente Full/Optimizer/Reretester/MT5 dentro de la wave (cierre de matriz 3/3 por capacidad).
- **Limpieza menor:** 3 CFX sobrantes en `watcher/input/` del paquete despachado (no referenciados por el spec; sin efecto) y restaurar `custom/project.cfx.preprobe-sqx144-20261016` si se desea el estado previo en Zeus.

## 10. Frontera pre-Echo

Cero llamadas Echo: el spec no contiene stages de seal/handoff; promotion V1 local; sin escrituras a `echo.*` (el boundary quedó probado físicamente en el cierre wave3t y esta campaña no toca ese camino).
