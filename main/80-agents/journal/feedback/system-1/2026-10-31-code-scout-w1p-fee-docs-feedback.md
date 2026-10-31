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
- Agent run: `2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md` (mismo run; esta nota recoge los findings de la revisión y su corrección).
- Session goal: code-scout `dispatch_id=w1p-fee-docs`, `scout_role=code-scout`, `execution=inline-fallback` (sin delegación Agent/Task en esta superficie); foco: mapa de implementaciones y versiones de fees oficiales (fórmula, caller, cobro, versiones), sin diseño ni producto.
- Main entity: [[Polymarket Engine — MVP]] (área [[Personal]]; routing DEFAULT).
- Skills used: `agents-os-code-scout` + `80-agents/skills/_shared/scout-contract.md` + runbook `80-agents/memory/public/runbook/agents-os-code-scout.md`, aplicados en modo scout.
- Retrieval mode: WebFetch dirigido — índice oficial `docs.polymarket.com/llms.txt` como ruta de descubrimiento, luego páginas de docs/API reference/changelog, luego código oficial vía `raw.githubusercontent.com/Polymarket/*` y metadatos/árboles/historial vía `api.github.com/repos/Polymarket/*` (sin token); 78 llamadas en la ventana medida `2026-10-31T11:35:38.606Z`–`2026-10-31T11:44:35.301Z`.
- Artifacts changed: sólo documentos y notas (`validated-baseline/w1-p-fee-documentary-20261031/` y notas del vault). Sin cambios en código, skills ni runbooks.

## Scout sampling (modo scout)

- **Request / revisiones:** `dispatch_id=w1p-fee-docs`, `scout_role=code-scout`; revisiones usadas: `scout-contract.md`, `agents-os-code-scout/SKILL.md`, `80-agents/memory/public/runbook/agents-os-code-scout.md` (leídos en esta sesión). Pregunta: fórmula/unidades/precisión/cobro de la fee oficial y vigencia frente al 29-10-2026.
- **Ruta de recuperación:** índice oficial → docs (fees, market details, WS, API reference) → changelog fechado → contratos (`polymarket-v2-external`, `ctf-exchange-v2`, `ctf-exchange`) → SDK (`clob-client`, `ts-sdk`, `py-clob-client`, `rs-clob-client`) → historial de commits por path vía API pública.
- **Rangos realmente leídos:** `trading/fees.md` (fórmula, tabla de categorías, precisión), `market-data/market-details.md` (semántica de `feeSchedule`), `api-reference/markets/get-clob-market-info.md` (`mbf`/`tbf`/`fd`), `api-reference/markets/get-market-by-id.md` (Gamma), `api-reference/wss/market.md` y `asyncapi.json` (`fee_rate_bps`), `api-reference/market-data/get-fee-rate*.md` (`base_fee` bps), `changelog/predictions.md` (entradas 05-01, 11-02, 30-03, 31-03, 17-04, 28-04, 10-07-2026 y ventana 11-07→29-10-2026), `programs/maker-rebates.md`, `programs/taker-rebates.md`, `trading/place-orders.md`, `migrate/polymarket-v2/api-integrations.md`, `resources/contracts.md`; `Exchange.sol`, `OrderStructs.sol`, `MATCH_ORDERS_LIFECYCLE.md`, `certora/specs/Exchange-FeeCap01b.spec`, `ctf-exchange-v2/{mixins/Fees.sol,mixins/Trading.sol,interfaces/IFees.sol}`, `ctf-exchange/{mixins/Fees.sol,interfaces/IFees.sol}`, `clob-client/src/order-builder/helpers.ts`, `ts-sdk/packages/bindings/src/clob/builder.ts`.
- **Utilidad observada:** alta. El mapa separa la fórmula contractual documentada, el techo on-chain en bps por familia/versión, el hecho de que la curva se calcula off-chain en matching time y —sobre todo— que el sujeto de `fee_rate_bps` no está documentado en ninguna fuente, lo que impide certificar la fee histórica. Utilidad para el consumidor: `unknown` hasta su reporte.
- **Gaps / truncado / degradación / relecturas:** truncado en el árbol recursivo de `ts-sdk`; **tres** rutas del SDK denegadas por el hook (`packages/client/src/actions/orders/{estimate.ts,market.ts,settlement.ts}`, error literal `Outside immutable W1-p scope`, motivo verificado por el supervisor: filtro por substring `/actions`), **sin que esos intentos establezcan la existencia ni el contenido** de esos archivos; visualización oficial de la curva fuera de allowlist; 4 repos inexistentes (404). Sin relecturas: cada fuente se leyó una vez y las preguntas se dirigieron por índice, no por memoria.
- **Causa:** `permissions` (cadena y endpoints de mercado fuera de la superficie) y `tooling` (alcance del hook) para los bloqueos; `retrieval` (interpretación propia no soportada) para los findings de la revisión.
- **Decisión de mantenimiento:** `NO_FINDING` sobre `agents-os-code-scout/SKILL.md` y su runbook — la fricción de la revisión es de **mis propios artefactos** (sobreafirmación de la fórmula, rótulo histórico demasiado fuerte, afirmaciones no respaldadas y ventana de consultas no medida), no del procedimiento canónico, que se aplicó completo. Corregir mis documentos no habilita editar la skill ni el runbook, que además son de solo lectura en este encargo.
- **Máxima mejora accionable (1):** en el runbook de code-scout, para repos remotos consultados sin clonación, sustituir el paso "ref/commit y dirty" por "rama consultada + ausencia de hash de contenido + estado de truncado del árbol", y declarar el truncado como límite de cobertura en el retorno.

## Findings de la revisión de supervisión y corrección aplicada (mismo dispatch_id, sin duplicar)

- **Fórmula:** eliminada la generalización `C × rate × p^e × (1 − p)` (rompía la simetría `p ↔ 1 − p` que cita la fuente); el modelo queda restringido a la fórmula documentada con **elegibilidad `e = 1`** y, para `e ≠ 1`, **no hay modelo** ni forma alternativa propuesta.
- **Historia:** la matriz y el retorno rotulan **anuncio documental previo** y **compatibilidad con los parámetros observados** en lugar de "probada por régimen"; el coeficiente del 10-07-2026 queda acotado a **Sports**; el destino deportivo del episodio se toma como dado (encargo + metadata W1-j) y lo no capturado es la etiqueta de política/rebate/override; el SDK se describe como el **recomendado por las docs de hoy** con código preexistente al corte, sin certificar soporte, despliegue ni uso histórico.
- **Precisión y lados:** sin modo de redondeo exacto (5 decimales y mínimo `0.00001` no fijan floor/ceil/nearest); la división entera atribuida al **techo** contractual y no al redondeo de la fee cobrada; redondeo de importes separado del significado de un campo de tasa; BUY paga collateral adicional y SELL recibe proceeds netos; `fee ≤ proceeds` limitado al camino demostrado; caps por familia/versión sin asumir actividad histórica; USDC y pUSD conservados como etiquetas distintas, sin identidad ni conversión asumida.
- **Siguiente paso:** el draft pasó de un protocolo centrado en fee cobrada/settlement/micro-trade a un **incremento estrictamente offline de conformidad del modelo** (e = 1, sin captura, sin re-score, sin cuenta ni fondos), con fixtures sintéticos **declarados y no implementados**, sin taxonomía de gates nueva y sin umbrales; criterio de aceptación = **conformidad del modelo** con fuentes y supuestos declarados.
- **Recibo y bloqueos:** ventana corregida a la medida por el supervisor (78 llamadas, `11:35:38.606Z`–`11:44:35.301Z`); tres rutas denegadas registradas con el motivo verificado del filtro y **sin afirmar la existencia de los archivos**; se conserva la limitación de que WebFetch devuelve resúmenes de IA sin hashes de cuerpo.

## Notas de modo

- Las secciones de scores de sesión, memoria interna y nota Graphify separada no aplican a esta invocación en modo scout (muestreo permanente del Owner para scouts); no se crea nota Graphify porque Graphify no se usó.
- Feedback persistido en esta misma invocación, con el mismo `dispatch_id` (`w1p-fee-docs`), sin duplicarlo y ampliado con los findings.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: responsable del método de evidencia (agente)
- Promote to L3 memory? defer

## One Next Improvement

- En el retorno de un scout documental, distinguir explícitamente tres etiquetas por hecho: **declarado por la fuente**, **inferencia del scout** y **no establecido**; y adjuntar siempre la fecha propia de la fuente separada de la fecha de consulta, para que un anuncio fechado no se lea como prueba de vigencia.
