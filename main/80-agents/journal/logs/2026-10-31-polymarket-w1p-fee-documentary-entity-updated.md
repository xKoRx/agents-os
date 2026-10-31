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

- **Tipo:** created + updated (creación y posterior pasada de corrección por revisión de supervisión, en la misma sesión)
- **Archivo(s):**
  - created `10-projects/Personal/Polymarket Engine/Research — Fee Formula Documentary W1-p 2026-10-31.md` (informe del encargo W1-p, tipo `doc`, materializado con `materialize_schema_note.py`).
  - updated `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` — sección `### W1-p — investigación documental de la fórmula de fee (2026-10-31)` con seis ítems cerrados y un ítem de Owner pendiente; entrada de bitácora W1-p; el ítem de Owner de W1-o sobre el paso documental pasa a `[x]` con la nota de que fue decidido y ejecutado en W1-p y de que las fuentes prueban **anuncios y compatibilidad**, no la aplicación; `updated: 2026-10-31` en el frontmatter.
  - updated `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` — sección `### Cierre W1-p — investigación documental de la fórmula de fee (2026-10-31, ZCode × minimax/MiniMax-M3.1-Flash)` al final, sin tocar ni reescribir el cierre W1-o ni ninguna sección previa.
  - updated `80-agents/journal/sessions/2026-10-31-polymarket-w1p-fee-documentary-summary.md`, `.../feedback/system-1/2026-10-31-polymarket-w1p-fee-documentary-feedback.md`, `.../feedback/system-1/2026-10-31-code-scout-w1p-fee-docs-feedback.md`, `.../agent-runs/2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md` (mismo agent run) y este change_log: ampliados con los findings de la revisión y su corrección, **sin crear notas nuevas**.

## Motivo

- W1-p cerró el paso documental que W1-o dejó abierto (decisión del Owner ya tomada): dejar constancia en el estado actual del proyecto de **qué quedó demostrado y qué no**, separando evidencia directa de inferencia, hipótesis marcada y claims no resueltos.
- La pasada de corrección responde a cinco findings del supervisor que detectaron sobreafirmación material en la primera entrega: una generalización de la fórmula sin respaldo que además rompía la simetría citada, un rótulo histórico más fuerte que la evidencia, afirmaciones de precisión y lados no sustentadas, un siguiente paso mal focalizado y un recibo con ventana horaria inventada y bloqueos incompletos. Corregir estas afirmaciones es **current truth** del proyecto: cualquier re-score o piloto futuro debe heredar la conclusión correcta sobre el campo WS `fee_rate_bps`, sobre los límites de la evidencia histórica y sobre el alcance de `REAL_FEE_READY`.

## Fuentes usadas

- Fuentes oficiales públicas consultadas el 2026-10-31 (34 entradas con URL, estado, fecha de consulta, fecha propia de fuente y fecha de vigencia cuando existe): `docs.polymarket.com/llms.txt`, `/trading/fees.md`, `/market-data/market-details.md`, `/market-data/realtime-data.md`, `/market-data/prices-order-books.md`, `/api-reference/markets/get-clob-market-info.md`, `/api-reference/markets/get-market-by-id.md`, `/api-reference/wss/market.md`, `/asyncapi.json`, `/api-reference/market-data/get-fee-rate.md`, `/api-reference/market-data/get-fee-rate-by-path-parameter.md`, `/api-reference/trade/post-a-new-order.md`, `/changelog/predictions.md`, `/programs/maker-rebates.md`, `/programs/taker-rebates.md`, `/trading/place-orders.md`, `/concepts/order-lifecycle.md`, `/concepts/markets-events.md`, `/migrate/polymarket-v2/api-integrations.md`, `/migrate/polymarket-v2/overview.md`, `/migrate/data-api-v1-to-v2.md`, `/resources/contracts.md`, `/getting-started/typescript.md`; código oficial `Polymarket/polymarket-v2-external` (BUSL-1.1), `Polymarket/ctf-exchange-v2`, `Polymarket/ctf-exchange`, `Polymarket/clob-client`, `Polymarket/ts-sdk`; API pública de GitHub (metadatos, árboles, commits por path).
- 78 llamadas WebFetch en la ventana medida por el supervisor vía SQLite (`2026-10-31T11:35:38.606Z`–`2026-10-31T11:44:35.301Z`); 3 rutas denegadas por el hook con motivo verificado (filtro por substring `/actions`), sin establecer existencia ni contenido de esos archivos.
- Ledger con las correcciones aplicadas por hallazgo: `validated-baseline/w1-p-fee-documentary-20261031/source-ledger.json` (S01–S34, `denied_or_unavailable`, `claims_unresolved`, `corrections_applied`).
- Informe y propuesta: `validated-baseline/w1-p-fee-documentary-20261031/research.md` y `prereg-draft.md` (DRAFT_NOT_APPROVED).

## Resolución aplicada

- En todos los documentos W1-p se **rehicieron las afirmaciones fuertes**, no se añadieron disclaimers al final: (1) el modelo usa **la única fórmula documentada** `fee = C × feeRate × p × (1 - p)` con **elegibilidad `e = 1`**; para `e ≠ 1` no hay modelo y no se propone forma alternativa; la correspondencia `fd`/`feeSchedule` y la unidad decimal de `rate` quedan como inferencia e hipótesis marcada. (2) La historia se enuncia como **anuncio documental previo + parámetros observados compatibles + modelo retrospectivo condicional**, sin comisión cobrada ni implementación vigente demostradas; el coeficiente del 10-07-2026 queda acotado a **Sports**; el destino deportivo del episodio se toma como dado (encargo y metadata W1-j) y lo no capturado es la etiqueta de política/rebate/override; el SDK se describe como el recomendado por la documentación de hoy, con código preexistente al corte y sin certificar soporte, despliegue ni uso histórico. (3) Se quitan las afirmaciones de modo de redondeo exacto, se atribuye la división entera al **techo** contractual y no al redondeo de la fee cobrada, se separan el redondeo de importes y el significado de un campo de tasa, se diferencian BUY (collateral adicional) y SELL (proceeds netos), se limita `fee ≤ proceeds` al camino demostrado, se separan los caps por familia/versión y se conservan USDC y pUSD como etiquetas distintas. (4) El `prereg-draft.md` pasa a un **incremento estrictamente offline de conformidad del modelo** (sin captura, sin re-score, sin cuenta ni fondos, sin micro-trade, sin taxonomía de gates ni umbrales; fixtures sintéticos declarados y no implementados; criterio de aceptación = conformidad del modelo con fuentes y supuestos declarados; `REAL_FEE_READY` sigue `false` sin definición global). (5) El recibo usa la ventana medida, registra las tres rutas denegadas con el motivo verificado y **no** afirma la existencia de los archivos intentados.
- No se borró ni reescribió historia previa: el cierre W1-o y el resto de la bitácora quedan intactos y el delta W1-p es aditivo.
- No se autoaprobó ninguna decisión del Owner: la regla de L sigue marcada pendiente (y no bloquea documentación ni cálculo de fee), y el siguiente paso queda como ítem de Owner en el MVP y como `prereg-draft.md` con estado **DRAFT_NOT_APPROVED**.

## Validación

- Readback después de la última edición de cada archivo modificado (los seis artefactos del shot, el informe nuevo, el MVP y la Continuidad en el rango del delta W1-p, y las cinco notas de journal).
- Verificación de que el checkout del proyecto sigue con HEAD `7c9adaea59251b39ac1559db1ed63d4566996206` y árbol limpio, sin push: **no corresponde a esta sesión** la medición de los 90 hashes sellados, del estado de sincronización remota del vault ni de la integridad del episodio W1-j (verifican el supervisor y el parent; la primera fase terminal fue verificada por el supervisor con exit0, 90/90 y controles intactos).
- Límite de validación declarado en el propio informe: WebFetch devuelve resúmenes de IA sin hash de cuerpo; una fecha de commit no es fecha de despliegue; las tres rutas denegadas no prueban existencia de archivo.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los tres archivos de Sistema 2 (`Research — Fee Formula Documentary W1-p 2026-10-31.md` se puede eliminar; MVP y Continuidad se restauran quitando la sección W1-p y la entrada de bitácora y volviendo `updated: 2026-10-30` en el MVP) y las notas de journal del 31-10-2026 con prefijo `polymarket-w1p-fee-documentary` y `code-scout-w1p-fee-docs`. Los artefactos del shot son derivados y read-only para el vault.
