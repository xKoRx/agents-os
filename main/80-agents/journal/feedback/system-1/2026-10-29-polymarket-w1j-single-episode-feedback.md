---
type: session_feedback
schema_version: 1
status: captured
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: "2026-10-29"
updated: "2026-10-29"
source_session: sess_no-legible-desde-superficie-w1j
surface: "[[ZCode]]"
model: "account:zai-individual-coding-plan/GLM-5.3-Flash"
related:
  - "[[2026-10-29-polymarket-w1j-single-episode-summary]]"
  - "[[2026-10-29-zcode-glm-5.3-flash-polymarket-w1j-single-episode]]"
  - "[[2026-10-29-polymarket-engine-entity-updated]]"
aliases: []
tags:
  - kind/feedback
  - topic/research-ops
---

# 2026-10-29-polymarket-w1j-single-episode-feedback

## Fricción 1 — perfil del hook de este shot: formas básicas denegadas y hash delegado a la corrida de tests

- **Qué pasó:** `sha256sum`, `gofmt` (también full-path), `go fmt`, `date`, `ls`, `grep`, `go test -run`, las formas `git diff --check/--stat` (con y sin `--cached`), la forma combinada `git status && git rev-parse` y toda invocación manual del binario engine (incluso `journal verify` read-only) fueron denegadas 1 vez cada una con el mensaje genérico «Outside W1-j exact scope…». Las únicas formas de ejecución que pasaron fueron los sufijos exactos de test/build y `pilot-supervisor prepare/run/analyze` con flags exactos.
- **Impacto:** los hashes exigidos (preflight de fuentes, 12 inputs) y los recibos del gate se produjeron con la única máquina permitida — `TestMain` tras PASS completo — que además es la regla del mandato («el recibo lo produce la prueba»); el formateo se verificó por compilación limpia sin poder correr gofmt; el SHA del binario `pilot-supervisor` tras el rebuild post-prepare quedó sin medir (preservado el previo en `execution-identity.json`).
- **Lección:** para shots con perfiles por-forma tan estrictos, diseñar los recibos desde el inicio como productos de la corrida de tests (no de comandos de shell) elimina la fricción completa; pedir al lanzador el registro de las formas diff/gofmt si se quiere revisión de diff por comando.

## Fricción 2 — lectura de recibos del lanzador en `.private-execution/w1j/`

- **Qué pasó:** `supervise.py` y `workspace-preflight.json` fueron legibles, pero `immutable-inputs.json` (la lista canónica de los 12 inputs del lanzador) y `zcode-w1j-*.meta`/`.log` resultaron denegados.
- **Impacto:** la lista exacta de los «12 inputs» previos no pudo replicarse; `inputs.json` se definió con los 12 archivos que ESTE shot consume realmente (módulo + fuentes del engine reutilizadas + contrato del shot), con SHAs medidos que además corroboran los valores publicados en W1-i (go.mod `b3a5f56b…`, reducer `23814a47…`, service `8b5fad8c…`).
- **Lección:** cuando el insumo canónico no es legible, declarar el criterio de sustitución y corroborar contra registros históricos es la vía honesta; no inventar que «son los mismos 12».

## Fricción 3 — mi error de dirección de descubrimiento (aprendizaje de investigación)

- **Qué pasó:** elegí `order=gameStartTime&ascending=true` para servir la regla «primer partido por kickoff ascendente»; el presupuesto de candidatos (100 TOTAL del shot, no por página) se agotó con kickoffs antiguos (pasados aún activos) y el lote cerró `NO_ELIGIBLES_EN_LOTE`. El preregistro v2 §3 ya había fijado `ascending=false` como priorización hacia kickoffs futuros poblados (y W1-d pasada 8 lo había demostrado con 100/100 elegibles).
- **Impacto:** el shot termina sin captura; la corrección es una línea (+ test + rerun de gate) pero exige decisión nueva de Metis/lanzador porque el presupuesto es durable y total.
- **Lección:** cuando una regla de SELECCIÓN (ascendente sobre lo recibido) y una regla de PRIORIZACIÓN de presupuesto (descending hacia el futuro) conviven, separarlas explícitamente en el congelado de reglas y re-leer el preregistro de priorización antes de elegir el parámetro del query; el «primero ascendente» se aplica client-side sobre la página, no en el parámetro del servidor.

## Fricción 4 — bugs propios detectados por los tests (sin salir a producción)

- `protocol.Surface` es enum uint8 (comparar con `.String()`, no con `string(const)`); ring continuo de la estrategia cruza segmentos ⇒ señales duplicadas/espurias de frontera en el fixture; estado de posiciones virtuales por escenario (unHold de A no bloquea a S); `bash -c 'cmd # ruta'` pierde el cmdline por exec implícito (holder con comando compuesto); orden del corte NO_ELIGIBLES vs schedule vacío en `run`. Todas corregidas con causa leída y suite verde antes de `prepare`.

## Señal positiva

- El patrón «recibos producidos por la corrida de tests + formas CLI exactas» cerró el gate de source real sin una sola fabricación: `offline-preflight.json`, `inputs.json`, manifiesto, presupuesto durable y recibo terminal son verificables byte a byte; el desenlace honesto (`NO_ELIGIBLES_EN_LOTE`) se selló con la misma naturalidad que un PASS.
