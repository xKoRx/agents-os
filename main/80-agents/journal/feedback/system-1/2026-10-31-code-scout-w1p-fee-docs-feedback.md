---
type: feedback
schema_version: 1
scope: session
created: 2026-10-31
updated: 2026-10-31
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[ZCode]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
agent_run: "[[80-agents/journal/agent-runs/2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md]]"
session_goal: code-scout inline-fallback, dispatch_id w1p-fee-docs — mapa de implementaciones y versiones de fees oficiales de Polymarket
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-10-31 - code-scout-w1p-fee-docs

## Context

- Agent surface: [[ZCode]] (host `sqx-ulab-hefesto-0`).
- Agent model: `minimax/MiniMax-M3.1-Flash` (reportado por el host).
- Agent run: `2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md`.
- Session goal: code-scout `dispatch_id=w1p-fee-docs`, `scout_role=code-scout`, `execution=inline-fallback` (sin delegación Agent/Task en esta superficie); foco: mapa de implementaciones y versiones de fees oficiales (fórmula contractual, caller, cobro, versiones), sin diseño ni producto.
- Main entity: [[Polymarket Engine — MVP]] (área [[Personal]]; routing DEFAULT).
- Skills used: `agents-os-code-scout` + `80-agents/skills/_shared/scout-contract.md` + runbook `80-agents/memory/public/runbook/agents-os-code-scout.md`, aplicados en modo scout.
- Retrieval mode: WebFetch dirigido — índice oficial `docs.polymarket.com/llms.txt` como ruta de descubrimiento, luego páginas de docs/API reference/changelog, luego código oficial vía `raw.githubusercontent.com/Polymarket/*` y metadatos/árboles/historial vía `api.github.com/repos/Polymarket/*` (sin token).
- Artifacts changed: sólo documentos y notas (`validated-baseline/w1-p-fee-documentary-20261031/scout-pack.json`, `source-ledger.json`, `research.md` y notas del vault). Sin cambios en código, skills ni runbooks.

## Scout sampling (modo scout)

- **Request / revisiones:** `dispatch_id=w1p-fee-docs`, `scout_role=code-scout`; revisiones usadas: `scout-contract.md`, `agents-os-code-scout/SKILL.md`, `80-agents/memory/public/runbook/agents-os-code-scout.md` (leídos en esta sesión). Pregunta: fórmula/unidades/rounding/cobro de la fee oficial y vigencia frente al 29-10-2026.
- **Ruta de recuperación:** índice oficial → docs (fees, market details, WS, API reference) → changelog fechado → contratos (`polymarket-v2-external`, `ctf-exchange-v2`, `ctf-exchange`) → SDK (`clob-client`, `ts-sdk`, `py-clob-client`, `rs-clob-client`) → historial de commits por path vía API pública.
- **Rangos realmente leídos:** `trading/fees.md` (fórmula, tabla de categorías, precisión), `market-data/market-details.md` (semántica de `feeSchedule`), `api-reference/markets/get-clob-market-info.md` (`mbf`/`tbf`/`fd`), `api-reference/markets/get-market-by-id.md` (Gamma), `api-reference/wss/market.md` y `asyncapi.json` (`fee_rate_bps`), `api-reference/market-data/get-fee-rate*.md` (`base_fee` bps), `changelog/predictions.md` (entradas 05-01, 11-02, 30-03, 31-03, 17-04, 28-04, 10-07-2026 y ventana 11-07→29-10-2026), `programs/maker-rebates.md`, `programs/taker-rebates.md`, `trading/place-orders.md`, `migrate/polymarket-v2/api-integrations.md`, `resources/contracts.md`; `Exchange.sol`, `OrderStructs.sol`, `MATCH_ORDERS_LIFECYCLE.md`, `certora/specs/Exchange-FeeCap01b.spec`, `ctf-exchange-v2/{mixins/Fees.sol,mixins/Trading.sol,interfaces/IFees.sol}`, `ctf-exchange/{mixins/Fees.sol,interfaces/IFees.sol}`, `clob-client/src/order-builder/helpers.ts`, `ts-sdk/packages/bindings/src/clob/builder.ts`.
- **Utilidad observada:** alta. El mapa cambia la conclusión del encargo: separa la fórmula contractual documentada, el techo on-chain en bps, el hecho de que la curva se calcula off-chain en matching time, y —sobre todo— que el sujeto de `fee_rate_bps` no está documentado en ninguna fuente, lo que impide certificar la fee histórica. Utilidad para el consumidor: `unknown` hasta su reporte.
- **Gaps / truncado / degradación / relecturas:** truncado en el árbol recursivo de `ts-sdk` (cobertura de "fee" incompleta en ese repo); dos archivos del SDK (`.../actions/orders/estimate.ts`, `.../market.ts`) denegados por el hook con `Outside immutable W1-p scope` (sin reintento ni variante); visualización oficial de la curva fuera de allowlist; 4 repos inexistentes (404). Sin relecturas: cada fuente se leyó una vez y las preguntas se dirigieron por índice, no por memoria.
- **Causa:** `tooling` (alcance del hook) + `permissions` (cadena y endpoints de mercado fuera de la superficie), no `retrieval`.
- **Decisión de mantenimiento:** `NO_FINDING` sobre `agents-os-code-scout/SKILL.md` y su runbook — la metodología canónica se aplicó completa y sin fricción estructural; la fricción fue de superficie, no de la skill, y en este encargo skills y runbooks son de solo lectura.
- **Máxima mejora accionable (1):** en el runbook de code-scout, para repos remotos consultados sin clonación, sustituir el paso "ref/commit y dirty" por "rama consultada + ausencia de hash de contenido + estado de truncado del árbol", y declarar el truncado como límite de cobertura en el retorno.

## Notas de modo

- Las secciones de scores de sesión, memoria interna y nota Graphify separada no aplican a esta invocación en modo scout (muestreo permanente del Owner para scouts); no se crea nota Graphify porque Graphify no se usó.
- Feedback persistido en esta misma invocación, con el mismo `dispatch_id` (`w1p-fee-docs`), sin duplicarlo.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: low
- Candidate owner: responsable del hook de alcance
- Promote to L3 memory? defer

## One Next Improvement

- Exponer en el error del hook qué URLs del allowlist de dominio quedan fuera del alcance, para que el principal pueda aportarlas en vez de dejar gaps no recuperables por búsqueda.
