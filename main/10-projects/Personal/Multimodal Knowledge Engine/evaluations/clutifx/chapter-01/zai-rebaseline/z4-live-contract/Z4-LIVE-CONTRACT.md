# Z4 — LIVE CONTRACT CERTIFICATION: BLOCKED_EXTERNAL_QUOTA

> [!important]+ RESOLUCIÓN OWNER (2026-10-07) — CAMPAÑA PARADA
> El Owner resolvió el bloqueo: **PARAR la migración** — "el plan zai no permite usar glm5.3flash para otras cosas... esperaremos un modelo free de openrouter". No se autoriza el endpoint coding ni el cambio de modelo. Watcher solo-sonda muerto (1ª ventana 96/96 probes 429; 2ª ventana cortada por el owner al cierre). El adapter `zai` queda pusheado @ `bd2edc1d` como capacidad disponible **sin certificación live**. Si la campaña se retoma con un modelo free de OpenRouter: `--vlm openrouter` existe y está intacto; NO se reutiliza el run-z4 (fingerprint distinto); nuevo preflight + Z4 con el modelo elegido. `CHAPTER_01_ACCEPTED = NO`, `READY_TO_SCALE_CORPUS = NO`.

Fecha: 2026-10-06 · Worker: manager-adoption tras muerte del subagent (run ejecutado y adoptado por Primary Manager; ver "Desviación de proceso") · Binario: `bd2edc1d` (`go version -m` vcs.revision verificado; `vcs.modified=true` por dir no-trackeado `wt/`, sin cambio de código) · Runtime local: `~/mke/zai-live-contract-20261006/`.

```text
ZAI_LIVE_CONTRACT = BLOCKED_EXTERNAL_QUOTA
ZAI_GENERAL_API_ENTITLEMENT = BLOCKED   (para el modelo objetivo glm-5.3-flash)
OWNER_DECISION_REQUIRED = YES
PROGRESO_DURABLE_PRESERVADO = YES   (run INCOMPLETE ordenado, 0 corrupción, run.db íntegro)
DEFECTO_DE_PRODUCTO = NO            (el adapter behave per contract ante el bloqueo)
```

## Evidencia del bloqueo

1. **Preflight Z0 (más temprano)**: sondas pequeñas en `api.z.ai/api/paas/v4` con `glm-5.3-flash` → HTTP 200 repetido (auth OK). Ver `z0-preflight/Z0-PREFLIGHT.md`.
2. **Corrida Z4 (8 ventanas: w0002-o1..o4 solapadas + w0001..w0005, config `configs/config.zai-contract.v2.json`)**: las 8 ventanas fallaron claims reconstruction con `retry-exhausted` (budget 2, backoff openrouter-paridad) y causa raíz `429: Insufficient balance or no resource package. Please recharge.` (código 1113). Terminal `INCOMPLETE` ordenado; `L2 composition skipped: no supported claims to compose`; 8 invocaciones registradas; presupuesto reservado liberado sin fuga. `pipeline_state`: fingerprints nuevos generados (config `b323ba48…`, L1 `05d66d16…`, L2 `23313dd7…`) — consistentes con re-baseline.
3. **Clasificación post-mortem (sondas mínimas)**:
   - `glm-5.3-flash` en API general → `429 {"code":"1113","message":"Insufficient balance or no resource package. Please recharge."}`
   - `glm-4.7-flash` → 200 OK · `glm-4.5-flash` → 200 OK · `glm-4.5-air` → 429 1113 (la key está viva; el bloqueo es de paquete/saldo por modelo)
   - `glm-5.3-flash` en endpoint **coding-only** (`api.z.ai/api/coding/paas/v4`) → **200 OK** (sonda de entitlement de 1 token, permitida por el mandato "You may probe entitlement safely"; NUNCA se corrió MKE ahí)
   - Patrón exacto pre-registrado por el mandato: `general API = unauthorized/no entitlement, coding-only = authenticated` → NO se bypassed; se retorna `ZAI_GENERAL_API_ENTITLEMENT = BLOCKED`.

## Gates del contrato

| Gate | Estado |
|---|---|
| IMAGE | NOT_EXERCISED (bloqueo de quota antes de cualquier 200 de reconstruction) |
| STRUCTURED_OUTPUT | NOT_EXERCISED |
| GROUNDING | NOT_EXERCISED |
| EQUIVALENCE | NOT_EXERCISED |
| L2 | NOT_EXERCISED (skipped: sin claims supported) |
| NO_SECRET_LEAK | PASS parcial (grep -F sobre run.db/logs sin matches; no hubo outputs de éxito que auditar) |
| Error-path live del adapter | PASS observacional (429→retryable→retry-exhausted, terminal honesto, sin crash) |

Probe runtime de capacidades (`probe-zai/report.md`): `zai 6/7, NO_GO` con el **inconclusivo conocido de campaña** (`vlm.malformed_output_rejected` = inconclusive: el backend con JSON mode responde JSON válido en vez de prosa malformada — path de rechazo no ejercitable live; mismo 6/7 documentado con openrouter/stealth en gates previos).

## Consumo

Las llamadas de reconstruction fallaron con 429 (no facturables). Consumo previo del día en la cuenta: sondas Z0 + probe runtime (~20 llamadas pequeñas, ≪ 50k tokens). Hipótesis de causa: grant de prueba mínimo de `glm-5.3-flash` consumido, o el modelo nunca tuvo paquete gratis y las primeras 200 fueron trial — en cualquier caso la cuenta HOY no tiene saldo/paquete que cubra `glm-5.3-flash` en API general.

## Desviación de proceso

El worker ONE-SHOT Z4 fue muerto por el harness (inactivo 600s durante la corrida larga) y dejó el run a medio nacer; el Manager adoptó la ejecución mecánica (binario verificado @ bd2edc1d, config derivada por el worker, run lanzado y diagnosticado directo). El juicio de certificación sigue siendo del Manager; el gate queda BLOCKED de todos modos, sin certificación emitida.

## Reanudación (cuando el Owner resuelva)

Relanzar `run-z4` FRESCO (mismo binario bd2edc1d, mismo config; el run bloqueado queda como evidencia): `bin/mke pipeline … --vlm zai --out run-z4b --timeout 600`. Con 429 por saldo persistente → `BLOCKED_EXTERNAL_QUOTA` de nuevo; NO cambiar provider/model mid-run sin decisión Owner.
