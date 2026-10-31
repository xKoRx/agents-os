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

- Cerrar el paso documental de fee abierto por [[Research — Target Fee Inventory W1-o 2026-10-31]]: con fuentes oficiales públicas y fechadas, fijar fórmula, unidades, precisión, base de coste, cobro y vigencias de la fee de Polymarket, y determinar qué significa el campo WS `fee_rate_bps` frente a los límites maker/taker `1000` y al `fd` crudo `{e:1, r:0.05, to:true}` del mercado `5784455`, con as-of `2026-10-29`.

## Contexto cargado

- Bootstrap agents-os (cold start) con constitución, perfil global, nota interna global, índice de skills y registry de routers: entidad [[Polymarket Engine — MVP]], área [[Personal]] → DEFAULT sin router de dominio.
- Pack W1-o reutilizado tal como lo verificó el parent (no reextraído): 9236 registros, 0 errores, 102 observaciones fee, `mbf`/`tbf` 1000, `fd {e:1,r:0.05,to:true}`, `fees_enabled` true, 78/78 `last_trade_price` con `fee_rate_bps="0"`, settlement NOT_CERTIFIED, `REAL_FEE_READY=false`.

## Trabajo realizado

- Code scout en modo `inline-fallback` (no hay delegación Agent/Task en esta superficie), `dispatch_id=w1p-fee-docs`, foco en el mapa de implementaciones y versiones de fees oficiales, con metodología canónica de `agents-os-code-scout` y su runbook.
- 78 llamadas WebFetch en la ventana medida por el supervisor vía SQLite (`2026-10-31T11:35:38.606Z`–`2026-10-31T11:44:35.301Z`): 34 fuentes únicas con éxito (docs oficiales, API reference, AsyncAPI, changelog y código oficial de `polymarket-v2-external`, `ctf-exchange-v2`, `ctf-exchange`, `clob-client`, `ts-sdk`, más metadatos/árboles/historial de commits por la API pública de GitHub), 3 rutas denegadas por el hook, 4 HTTP 404 y 1 URL oficial fuera de allowlist no intentada. Cero lecturas del episodio W1-j.
- Hallazgo: la documentación oficial entrega **una única** fórmula, `fee = C × feeRate × p × (1 - p)` (5 decimales, mínimo `0.00001`, **modo de redondeo no adjudicado**, sólo taker, cobro en matching time; BUY paga collateral adicional, SELL recibe proceeds netos) y el código oficial muestra que la curva se calcula off-chain y que el contrato sólo acota un techo en bps por familia/versión; en cambio **no** existe fuente consultada que defina el sujeto de `fee_rate_bps`, ni que ligue `mbf`/`tbf` al `MAX_FEE_RATE`, ni que demuestre la implementación desplegada el 29-10-2026.
- Separación explícita: evidencia directa / inferencia / hipótesis marcada / claim no resuelto, con matriz actual vs. histórico donde el changelog aporta **anuncios documentales con fecha** y lo observado del target sólo se declara **compatible**.

## Pasada de corrección (findings del supervisor)

- Aplicados 5 findings concretos y **rehechas las afirmaciones fuertes** en todos los documentos W1-p (no sólo disclaimers añadidos al final): (1) eliminada la generalización con exponente —el modelo se restringe a la fórmula documentada con elegibilidad `e = 1` y para `e ≠ 1` no hay modelo—; (2) la historia pasa a "anuncio documental previo + parámetros compatibles + modelo retrospectivo condicional", con el coeficiente del 10-07-2026 acotado a Sports, el destino deportivo tomado como dado y el SDK descrito como el recomendado por las docs de hoy con código preexistente al corte; (3) sin modo de redondeo exacto, con BUY/SELL diferenciados, `fee ≤ proceeds` limitado al camino demostrado, caps por familia/versión y USDC/pUSD como etiquetas distintas; (4) prereg reescrito como **incremento offline de conformidad del modelo** (sin micro-trade, sin cuenta, sin gates nuevos, sin umbrales); (5) ventana de consultas corregida a la medida y tres rutas denegadas registradas sin afirmar la existencia de los archivos.
- Cero consultas web nuevas en esta pasada; no se reintentó ni se eludió ninguna ruta denegada.

## Artifacts creados o modificados

- `validated-baseline/w1-p-fee-documentary-20261031/`: `source-ledger.json`, `research.md`, `prereg-draft.md` (DRAFT_NOT_APPROVED), `run-receipt.json`, `capability.json`, `scout-pack.json`.
- Vault: `10-projects/Personal/Polymarket Engine/Research — Fee Formula Documentary W1-p 2026-10-31.md` (nuevo); delta W1-p en `Polymarket Engine — MVP.md` y en `Polymarket Engine — Continuidad Five-POC 2026-09-20.md`; `2026-10-31-polymarket-w1p-fee-documentary-summary.md`, feedback general, feedback de scout `2026-10-31-code-scout-w1p-fee-docs-feedback.md`, agent run `2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md` y change_log del 31-10-2026.

## Memoria propuesta o creada

- No se creó L3: el conocimiento es evidencia de proyecto y queda en el informe W1-p; no hay regla reusable nueva que promover. No se tocó memoria interna.

## Decisiones

- **Modelado futuro:** sí, con la fórmula documentada y elegibilidad `e = 1`, versión CLOB V2, unidades declaradas (USDC/pUSD como etiquetas distintas), precisión con banda conservadora declarada como hipótesis, base y lados diferenciados, límites por familia/versión y `rate`/`exponent` leídos del `feeSchedule` capturado antes del timestamp de decisión.
- **Episodio histórico:** sólo acotado y condicional — anuncio documental previo + parámetros observados compatibles + modelo retrospectivo condicional; sin comisión cobrada ni implementación vigente demostradas; `fee_rate_bps="0"` no interpretable como ausencia de cobro.
- Sin cambio de estrategia, parámetros, escenarios congelados A/S ni regla de L; sin re-score, capturas o piloto; `REAL_FEE_READY=false`.

## Pendiente

- Owner: decidir el **incremento offline de conformidad del modelo** del `prereg-draft.md` (DRAFT_NOT_APPROVED): autorizar/rechazar la conformidad matemática/contable del modelo documentado con `e = 1` (sin captura, sin re-score, sin cuenta ni fondos), confirmar el uso de los parámetros capturados como ejemplo condicional y confirmar que `REAL_FEE_READY` sigue en `false` sin definición global. La regla de L sigue pendiente y no bloquea documentación ni cálculo de fee; cambiar gate, estrategia o piloto requiere decisión y preregistro aparte.
- Si el Owner puede aportar la definición oficial del sujeto de `fee_rate_bps`, la etiqueta de fee-category/`rebateRate` del mercado `5784455` o la prueba de despliegue con su `MAX_FEE_RATE`, se cerrarían los claims no resueltos que esta sesión no pudo resolver con la superficie autorizada; en particular, el contenido de los tres helpers del SDK (`packages/client/src/actions/orders/{estimate.ts,market.ts,settlement.ts}`) cuya existencia y contenido **no** quedaron establecidos por los intentos denegados, o bien adjudicar el filtro de alcance `/actions` en un encargo posterior.
