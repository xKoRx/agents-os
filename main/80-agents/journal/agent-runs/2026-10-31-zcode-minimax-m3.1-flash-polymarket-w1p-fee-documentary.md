---
type: agent_run
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
  - "[[MiniMax M3.1 Flash]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
model_source: host
task_type: research
task_complexity: medium
outcome: complete
verification: not_run
evaluator: agent
user_rework: "revisión de supervisión aplicada (5 findings concretos reconciliados en los artefactos y en los documentos del vault); sin cambios de Owner sobre estrategia, parámetros ni regla de L"
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary

## Trabajo

- **Objetivo:** W1-p — investigación documental de fuentes oficiales fechadas de Polymarket (fórmula de fee, unidades, precisión, base de coste, cobro, techo contractual y significado del campo WS `fee_rate_bps` frente a `mbf`/`tbf` 1000 y `fd {e:1,r:0.05,to:true}`) con as-of `2026-10-29` para el mercado `5784455`.
- **Alcance atribuible a esta combinación superficie×modelo:** sólo investigación documental y redacción de evidencia. **No hubo desarrollo**: ningún archivo de código escrito, compilado, testeado ni depurado; ningún re-score, gate, extracción, captura, checkout ni push. El checkout del proyecto se verificó limpio con HEAD `7c9adaea59251b39ac1559db1ed63d4566996206` y no fue modificado.
- **Artefactos afectados:** en `validated-baseline/w1-p-fee-documentary-20261031/`: `source-ledger.json` (34 fuentes + denegaciones + claims no resueltos + `corrections_applied`), `research.md`, `prereg-draft.md` (DRAFT_NOT_APPROVED, incremento offline de conformidad del modelo con `e = 1`), `run-receipt.json`, `capability.json`, `scout-pack.json`. En el vault: `Research — Fee Formula Documentary W1-p 2026-10-31` (nuevo), delta W1-p en `Polymarket Engine — MVP` y en `Polymarket Engine — Continuidad Five-POC 2026-09-20`, más notas de sesión, feedback (general y de scout), este run y el change_log del 31-10-2026.

## Evidencia

- **Validaciones ejecutadas:** ninguna de código (no aplican: no hay código). Verificaciones documentales: 78 llamadas WebFetch en la ventana medida por el supervisor vía SQLite (`2026-10-31T11:35:38.606Z`–`2026-10-31T11:44:35.301Z`), de las que el ledger registra 34 fuentes únicas con éxito, 3 rutas denegadas, 4 HTTP 404 y 1 URL oficial fuera de allowlist no intentada; lectura de bodies de contrato (`Exchange.sol`, `OrderStructs.sol`, `MATCH_ORDERS_LIFECYCLE.md`, `Fees.sol` legacy y V2, `IFees.sol`, `Trading.sol`, spec Certora) e historial de commits por path vía API pública de GitHub sin token; readback de cada artefacto y documento del vault tras su última edición.
- **Pasada de corrección:** cinco findings del supervisor aplicados y **reconciliadas las afirmaciones fuertes** en todos los documentos W1-p (no sólo disclaimers añadidos al final): (1) eliminada la generalización de la fórmula con exponente —el modelo queda en la fórmula documentada con elegibilidad `e = 1` y, para `e ≠ 1`, no hay modelo—; (2) historia reetiquetada como anuncio documental previo + compatibilidad + modelo retrospectivo condicional, con el coeficiente del 10-07-2026 acotado a Sports, el destino deportivo tomado como dado y el SDK descrito como el recomendado por las docs de hoy; (3) sin modo de redondeo exacto, con BUY/SELL diferenciados, `fee ≤ proceeds` limitado al camino demostrado, caps por familia/versión y USDC/pUSD como etiquetas distintas; (4) prereg reescrito como incremento offline de conformidad del modelo (sin micro-trade, cuenta, fondos, gates nuevos ni umbrales); (5) ventana corregida a la medida y tres rutas denegadas registradas sin afirmar la existencia de los archivos. Cero consultas web nuevas en esa pasada.
- **Resultado observable:** entregable producido con límites explícitos — la documentación oficial entrega **una única** fórmula (`fee = C × feeRate × p × (1 - p)`, 5 decimales, mínimo `0.00001`, modo de redondeo no adjudicado, sólo taker, base = valor de collateral) y el código oficial entrega el techo en bps por familia/versión y el hecho de que la curva se calcula off-chain en matching time; en cambio **ninguna fuente consultada define el sujeto de `fee_rate_bps`** ni demuestra la implementación desplegada ni el `MAX_FEE_RATE` vigente el 29-10-2026, por lo que el gap U-02 queda acotado pero abierto, `REAL_FEE_READY` sigue en `false` y el `0` de los 78 trades queda **no interpretable**. Para el episodio sólo se sostiene anuncio documental previo + parámetros observados compatibles + modelo retrospectivo condicional, sin comisión cobrada ni implementación vigente demostradas.
- **Limitaciones de la evidencia:** WebFetch devuelve resúmenes de IA, no el cuerpo crudo: no hay hash de origen ni de cuerpo de ninguna fuente. La documentación consultada es la vigente el 2026-10-31 y consultarla no prueba vigencia retrospectiva; las fechas de commit/committer no son fechas de despliegue. **Tres** rutas del SDK oficial (`packages/client/src/actions/orders/{estimate.ts,market.ts,settlement.ts}`) fueron denegadas por el hook con `Outside immutable W1-p scope` (motivo verificado por el supervisor: filtro por substring `/actions`); su **existencia y contenido no quedan establecidos** por esos intentos y no se reintentaron. La medición de los 90 hashes sellados, del estado de sincronización remota del vault y de la integridad del episodio W1-j corresponde al supervisor/parent: esta sesión no puede certificarlos.

## Evaluación

- **Correctness:** 3 — la revisión de supervisión detectó sobreafirmación material en la primera entrega (una generalización de fórmula sin respaldo que además rompía la simetría citada, un rótulo histórico más fuerte que la evidencia y opciones que nada probaban); tras la corrección, las afirmaciones quedan ligadas a URL y fecha de fuente, los claims no resueltos están declarados como tales y la inferencia está etiquetada. Se pierde un punto por los tres archivos de código no leídos y por la ausencia de hash de origen.
- **Autonomy:** 4 — el encargo se ejecutó de punta a punta sin decisiones intermedias del Owner y con los límites de superficie respetados; la corrección derivada de la revisión se aplicó sin bloquear al usuario.
- **Efficiency:** 4 — el volumen de consultas fue el necesario para cerrar los claims principales; el costo residual fue la exploración dirigida fallida (tres rutas denegadas, cuatro 404) y la primera versión del prereg, que hubo que reescribir por estar mal focalizada.
- **Tool use:** 4 — uso correcto de WebFetch con rutas derivadas del índice oficial, Bash restringido a los comandos permitidos y materializador canónico para toda nota del vault; un `--dry-run` del materializador fue rechazado por el hook y se reintentó sólo con la forma exacta autorizada.
- **Overall:** 3

## Resultado

- **Outcome:** complete tras rework — investigación documental cerrada con matriz actual/histórico, ledger de fuentes y draft de incremento offline listo para revisión del Owner; sin desarrollo, sin tests, sin cambio de estado del gate de costes, con `REAL_FEE_READY=false` y la regla de L intacta.
- **Rework posterior:** findings del supervisor aplicados en la misma sesión y en el mismo agent run (5 puntos, con reconciliación de todos los documentos W1-p); sin cambios de Owner sobre estrategia, parámetros ni L.
- **Aprendizaje para comparar herramientas:** en superficies con WebFetch mediado por modelo, sin acceso a cadena y con hooks de alcance por substring, la evidencia documental alcanza para **modelar costos futuros** con la fórmula sustentada por la fuente, pero **no** para certificar fees históricas. El límite principal de esta sesión no fue de esfuerzo de búsqueda sino de **disciplina de evidencia**: generalizar una fórmula que la fuente sólo nombra, o rotular como "probado" lo que la fuente sólo anuncia, produce afirmaciones que la revisión tiene que desmontar. Conviene que futuros encargos declaren desde el inicio las tres etiquetas —declarado / inferido / no establecido— y la fecha propia de la fuente separada de la fecha de consulta.
