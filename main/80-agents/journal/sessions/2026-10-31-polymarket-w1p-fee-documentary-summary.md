---
type: session
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[ZCode]]"
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-10-31-polymarket-w1p-fee-documentary-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Cerrar el paso documental de fee abierto por [[Research — Target Fee Inventory W1-o 2026-10-31]]: con fuentes oficiales públicas y fechadas, fijar fórmula, unidades, redondeo, base de coste, cobro y vigencias de la fee de Polymarket, y determinar qué significa el campo WS `fee_rate_bps` frente a los límites maker/taker `1000` y al `fd` crudo `{e:1, r:0.05, to:true}` del mercado `5784455`, con as-of `2026-10-29`.

## Contexto cargado

- Bootstrap agents-os (cold start) con constitución, perfil global, nota interna global, índice de skills y registry de routers: entidad [[Polymarket Engine — MVP]], área [[Personal]] → DEFAULT sin router de dominio.
- Pack W1-o reutilizado tal como lo verificó el parent (no reextraído): 9236 registros, 0 errores, 102 observaciones fee, `mbf`/`tbf` 1000, `fd {e:1,r:0.05,to:true}`, `fees_enabled` true, 78/78 `last_trade_price` con `fee_rate_bps="0"`, settlement NOT_CERTIFIED, `REAL_FEE_READY=false`.

## Trabajo realizado

- Code scout en modo `inline-fallback` (no hay delegación Agent/Task en esta superficie), `dispatch_id=w1p-fee-docs`, foco en el mapa de implementaciones y versiones de fees oficiales, con metodología canónica de `agents-os-code-scout` y su runbook.
- 41 intentos de fuente: 34 con éxito (docs oficiales, API reference, AsyncAPI, changelog, y código oficial de `polymarket-v2-external`, `ctf-exchange-v2`, `ctf-exchange`, `clob-client`, `ts-sdk`, más metadatos/árboles/historial de commits por la API pública de GitHub), 2 denegaciones del hook, 4 HTTP 404 y 1 URL oficial fuera de allowlist no intentada.
- Hallazgo: la fórmula y las unidades **sí** están documentadas (`fee = C × feeRate × p × (1 - p)`, USDC, 5 decimales, mínimo `0.00001`, sólo taker, cobro en matching time sobre el valor de collateral) y el código oficial **sí** muestra que la curva se calcula off-chain y que el contrato sólo acota un techo en bps sobre el cash value y los proceeds; en cambio **no** existe fuente consultada que defina el sujeto de `fee_rate_bps`, ni que ligue `mbf`/`tbf` al `MAX_FEE_RATE`, ni que pruebe el despliegue vigente el 29-10-2026.
- Separación explícita: evidencia directa / inferencia / claim no resuelto, con matriz actual vs. histórico y fechas de vigencia separadas de fechas de commit.

## Artifacts creados o modificados

- `validated-baseline/w1-p-fee-documentary-20261031/`: `source-ledger.json`, `research.md`, `prereg-draft.md` (DRAFT_NOT_APPROVED), `run-receipt.json`, `capability.json`, `scout-pack.json`.
- Vault: `10-projects/Personal/Polymarket Engine/Research — Fee Formula Documentary W1-p 2026-10-31.md` (nuevo); delta W1-p en `Polymarket Engine — MVP.md` y en `Polymarket Engine — Continuidad Five-POC 2026-09-20.md`; `2026-10-31-polymarket-w1p-fee-documentary-summary.md`, feedback general, feedback de scout `2026-10-31-code-scout-w1p-fee-docs-feedback.md`, agent run `2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md` y change_log del 31-10-2026.

## Memoria propuesta o creada

- No se creó L3: el conocimiento es evidencia de proyecto y queda en el informe W1-p; no hay regla reusable nueva que promover. No se tocó memoria interna (no hubo delta durable que la justifique).

## Decisiones

- **Modelado futuro:** sí se puede modelar costo de forma defendible con versión (CLOB V2), fórmula (`C × rate × p^e × (1 - p)`, con la forma con exponente marcada como inferencia), unidades/redondeo y límites exactos (techo on-chain en bps sobre collateral, `fee ≤ proceeds`, maker paga 0 y recibe rebate diario).
- **Episodio histórico:** conclusión acotada — el régimen y los parámetros declarados del 29-10-2026 están documentados y fechados, pero la fee cobrada en los 78 trades **no** es certificable; `fee_rate_bps="0"` **no** equivale a "no se cobró fee"; `REAL_FEE_READY` sigue en `false` y el gap U-02 sigue abierto.
- Sin cambio de estrategia, parámetros, escenarios congelados A/S ni regla de L; sin re-score, capturas o piloto.

## Pendiente

- Owner: decidir el protocolo prospectivo del `prereg-draft.md` (§2–§6), incluido `ε`, `N` y rango de precios, y por separado si autoriza la fase opcional con micro-trade controlado; decidir la regla de L (sigue pendiente); y fijar el alcance textual de una futura afirmación `REAL_FEE_READY`.
- Si el Owner puede aportar la definición oficial del sujeto de `fee_rate_bps`, la categoría/`rebateRate` del mercado `5784455` o la prueba de despliegue del Exchange v2 con su `MAX_FEE_RATE`, se cerrarían los tres claims no resueltos que esta sesión no pudo resolver con la superficie autorizada.
