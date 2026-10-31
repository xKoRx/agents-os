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
user_rework: unknown
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

- **Objetivo:** W1-p — investigación documental de fuentes oficiales fechadas de Polymarket (fórmula de fee, unidades, redondeo, base de coste, cobro, techo contractual, significado del campo WS `fee_rate_bps` frente a `mbf`/`tbf` 1000 y `fd {e:1,r:0.05,to:true}`) con as-of `2026-10-29` para el mercado `5784455`.
- **Alcance atribuible a esta combinación superficie×modelo:** sólo investigación documental y redacción de evidencia. **No hubo desarrollo**: ningún archivo de código escrito, compilado, testeado ni depurado; ningún re-score, gate, extracción, captura, checkout ni push. El checkout del proyecto se verificó limpio con HEAD `7c9adaea59251b39ac1559db1ed63d4566996206` y no fue modificado.
- **Artefactos afectados:** en `validated-baseline/w1-p-fee-documentary-20261031/`: `source-ledger.json` (34 fuentes + denegaciones + claims no resueltos), `research.md`, `prereg-draft.md` (DRAFT_NOT_APPROVED), `run-receipt.json`, `capability.json`, `scout-pack.json`. En el vault: `Research — Fee Formula Documentary W1-p 2026-10-31` (nuevo), delta W1-p en `Polymarket Engine — MVP` y en `Polymarket Engine — Continuidad Five-POC 2026-09-20`, más notas de sesión, feedback (general y de scout), este run y el change_log del 31-10-2026.

## Evidencia

- **Validaciones ejecutadas:** ninguna de código (no aplican: no hay código). Verificaciones documentales: 41 intentos de fuente (34 con éxito, 2 denegaciones del hook, 4 HTTP 404, 1 fuera de allowlist no intentado), lectura de bodies de contrato (`Exchange.sol`, `OrderStructs.sol`, `MATCH_ORDERS_LIFECYCLE.md`, `Fees.sol` legacy y V2, `IFees.sol`, `Trading.sol`, spec Certora) e historial de commits por path vía API pública de GitHub sin token; readback de cada artefacto y documento del vault tras su última edición.
- **Resultado observable:** entregable producido con límites explícitos — la documentación oficial sí entrega fórmula/unidades/redondeo/base de cobro y el código oficial sí entrega el techo en bps y el hecho de que la curva se calcula off-chain en matching time; en cambio **ninguna fuente consultada define el sujeto de `fee_rate_bps`** ni prueba el despliegue ni el `MAX_FEE_RATE` vigente el 29-10-2026, por lo que el gap U-02 queda acotado pero abierto y `REAL_FEE_READY` sigue en `false`. El `0` de los 78 trades queda **no interpretable** (no equivale a "no se cobró fee").
- **Limitaciones de la evidencia:** WebFetch devuelve cuerpo convertido y resumido por un modelo de sesión, sin hash de origen: no hay hash de ninguna fuente. La documentación consultada es la vigente el 2026-10-31 y consultarla no prueba vigencia retrospectiva; las fechas de commit/committer no son fechas de despliegue. Dos archivos del SDK oficial con la lógica de fee (`.../actions/orders/estimate.ts` y `.../market.ts`) fueron denegados por el hook con `Outside immutable W1-p scope` y no se reintentaron; la visualización oficial de la curva de fee (`datawrapper.dwcdn.net/dJ74e/`) está fuera de la allowlist de dominio. La medición de los 90 hashes sellados, del estado de sincronización remota del vault y de la integridad del episodio W1-j corresponde al supervisor/parent: esta sesión no puede certificarlos.

## Evaluación

- **Correctness:** 4 — las afirmaciones del informe están ligadas a URL y fecha de fuente, y los claims no resueltos están declarados como tales; se pierden puntos por dos archivos de código relevantes que no se pudieron leer y por no existir hash de origen de las fuentes.
- **Autonomy:** 5 — el encargo se ejecutó de punta a punta sin requerir decisiones intermedias del Owner, con los límites de superficie respetados y sin ask bloqueante.
- **Efficiency:** 4 — el volumen de consultas fue el necesario para cerrar los claims principales; el intento de dos archivos denegados y los 404 de repos son costo residual de exploración dirigida.
- **Tool use:** 4 — uso correcto de WebFetch con rutas derivadas del índice oficial (sin adivinar variantes), Bash restringido a los comandos permitidos y materializador canónico para toda nota del vault; un `--dry-run` del materializador fue rechazado por el hook y se reintentó sólo con la forma exacta autorizada.
- **Overall:** 4

## Resultado

- **Outcome:** complete — investigación documental cerrada con matriz actual/histórico, ledger de fuentes y draft de preregistro prospectivo listo para revisión del Owner; sin desarrollo, sin tests, sin cambio de estado del gate de costes.
- **Rework posterior:** unknown (aún no hay feedback del Owner).
- **Aprendizaje para comparar herramientas:** en superficies con WebFetch mediado por modelo y sin acceso a cadena, la evidencia documental alcanza para **modelar costos futuros** con parámetros explícitos, pero **no** para certificar fees históricas: el límite no es de esfuerzo de búsqueda sino de naturaleza de la evidencia (sujeto del campo WS no documentado y ausencia de prueba de despliegue). Conviene que futuros encargos declaran esta distinción desde el inicio para evitar búsquedas infinitas.
