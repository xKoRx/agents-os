---
type: change_log
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
confidence: verified
source_session:
source_feedbacks:
  - "[[80-agents/journal/feedback/system-1/2026-10-31-polymarket-w1p-fee-documentary-feedback.md]]"
  - "[[80-agents/journal/feedback/system-1/2026-10-31-code-scout-w1p-fee-docs-feedback.md]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-31-polymarket-w1p-fee-documentary-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - created `10-projects/Personal/Polymarket Engine/Research — Fee Formula Documentary W1-p 2026-10-31.md` (informe del encargo W1-p, tipo `doc`, materializado con `materialize_schema_note.py`).
  - updated `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` — nueva sección `### W1-p — investigación documental de la fórmula de fee (2026-10-31)` con seis ítems cerrados y un ítem de Owner pendiente; nueva entrada de bitácora W1-p; el ítem de Owner de W1-o sobre el paso documental pasa a `[x]` con la nota de que fue decidido y ejecutado en W1-p y de que las fuentes **no** prueban la aplicación; `updated: 2026-10-31` en el frontmatter.
  - updated `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` — nueva sección `### Cierre W1-p — investigación documental de la fórmula de fee (2026-10-31, ZCode × minimax/MiniMax-M3.1-Flash)` al final, sin tocar ni reescribir el cierre W1-o ni ninguna sección previa.

## Motivo

- W1-p cerró el paso documental que W1-o dejó abierto (decisión del Owner ya tomada): dejar constancia en el estado actual del proyecto de **qué quedó demostrado y qué no**, separando evidencia directa de inferencia y de claims no resueltos. El cambio es "current truth" del proyecto porque el Owner necesita un punto de partida para decidir el siguiente paso y porque cualquier re-score o piloto futuro debe heredar la conclusión correcta sobre el campo WS `fee_rate_bps` y sobre los límites de la evidencia histórica.

## Fuentes usadas

- Fuentes oficiales públicas consultadas el 2026-10-31 (34 entradas con URL, estado, fecha de consulta, fecha propia de fuente y fecha de vigencia cuando existe): `docs.polymarket.com/llms.txt`, `/trading/fees.md`, `/market-data/market-details.md`, `/market-data/realtime-data.md`, `/market-data/prices-order-books.md`, `/api-reference/markets/get-clob-market-info.md`, `/api-reference/markets/get-market-by-id.md`, `/api-reference/wss/market.md`, `/asyncapi.json`, `/api-reference/market-data/get-fee-rate.md`, `/api-reference/market-data/get-fee-rate-by-path-parameter.md`, `/api-reference/trade/post-a-new-order.md`, `/changelog/predictions.md`, `/programs/maker-rebates.md`, `/programs/taker-rebates.md`, `/trading/place-orders.md`, `/concepts/order-lifecycle.md`, `/concepts/markets-events.md`, `/migrate/polymarket-v2/api-integrations.md`, `/migrate/polymarket-v2/overview.md`, `/migrate/data-api-v1-to-v2.md`, `/resources/contracts.md`, `/getting-started/typescript.md`; código oficial `Polymarket/polymarket-v2-external` (BUSL-1.1), `Polymarket/ctf-exchange-v2`, `Polymarket/ctf-exchange`, `Polymarket/clob-client`, `Polymarket/ts-sdk`; API pública de GitHub (metadatos, árboles, commits por path).
- Ledger completo: `validated-baseline/w1-p-fee-documentary-20261031/source-ledger.json` (S01–S34, `denied_or_unavailable`, `claims_unresolved`).
- Informe: `validated-baseline/w1-p-fee-documentary-20261031/research.md`; propuesta de siguiente paso: `.../prereg-draft.md` (DRAFT_NOT_APPROVED).

## Resolución aplicada

- Se registró en las notas del proyecto sólo lo que la evidencia sostiene: (a) la fórmula y unidades documentadas (`fee = C × feeRate × p × (1 - p)`, USDC, 5 decimales, mínimo `0.00001`, sólo taker, cobro en matching time sobre el valor de collateral) y los parámetros por mercado (`feeSchedule`/`fd`, `mbf`/`tbf` en bps); (b) la arquitectura de cobro: la curva se calcula **off-chain** y el contrato sólo acota un techo en bps sobre el cash value más `fee ≤ proceeds`; (c) la cronología fechada previa al 29-10-2026 del changelog; (d) el límite explícito: **el sujeto de `fee_rate_bps` no está documentado** en ninguna fuente consultada y no hay prueba de despliegue, por lo que `fee_rate_bps="0"` no equivale a "no se cobró fee", la fee histórica sigue sin certificar, el gap U-02 queda acotado pero abierto y `REAL_FEE_READY` sigue en `false`.
- No se borró ni reescribió historia previa; el cierre W1-o y el resto de la bitácora quedan intactos y el delta W1-p es aditivo.
- No se autoaprobó ninguna decisión del Owner: la regla de L sigue marcada pendiente y el siguiente paso queda como ítem de Owner en el MVP y como `prereg-draft.md` con estado **DRAFT_NOT_APPROVED**.

## Validación

- Readback después de la última edición de cada archivo modificado (informe nuevo, MVP en el rango del delta W1-p y su bitácora, continuidad en el rango del cierre W1-p, y las cinco notas de journal).
- Verificación de que el checkout del proyecto sigue con HEAD `7c9adaea59251b39ac1559db1ed63d4566996206` y árbol limpio, sin push: **no corresponde a esta sesión** la medición de los 90 hashes sellados, del estado de sincronización remota del vault ni de la integridad del episodio W1-j (verifican el supervisor y el parent); esta sesión no puede autocertificarlos.
- Límite de validación declarado en el propio informe: WebFetch devuelve cuerpo convertido y resumido por un modelo de sesión, sin hash de origen de ninguna fuente; una fecha de commit no es fecha de despliegue.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los tres archivos de Sistema 2 (`Research — Fee Formula Documentary W1-p 2026-10-31.md` se puede eliminar; MVP y Continuidad se restauran quitando la sección W1-p y la entrada de bitácora y volviendo `updated: 2026-10-30` en el MVP) y las notas de journal del 31-10-2026 con prefijo `polymarket-w1p-fee-documentary` y `code-scout-w1p-fee-docs`. Los artefactos del shot son derivados y read-only para el vault.
