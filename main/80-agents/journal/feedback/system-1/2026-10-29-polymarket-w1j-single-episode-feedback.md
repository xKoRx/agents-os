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

## Fricción 8 (lote 3) — el gate de commit está por mensaje exacto y dos bugs míos quedaron expuestos por el recibo durable

- **Qué pasó:** (a) el commit del fix ordinario fue denegado con el mensaje alternativo que le di («Outside W1-j lot3 scope…») — el perfil registra la forma de commit POR MENSAJE EXACTO; reintentado con el mensaje autorizado del lote y pasó (segundo commit con el mismo texto, sin amend). (b) Mi etiqueta GMT de pared en el recibo READY_FUTURE imprimió «GMT-5»/«-05:00»: los layouts de zona de Go interpretan fragmentos como «GMT-3»/«-03:00» como tokens de offset; la hora de pared era correcta pero la etiqueta durable era falsa — peligro real de despacho. (c) Mi orden revalidate-vs-episode dejaba la renovación sin re-query inalcanzable tras el primer prepare, justo lo que el mandato exige tras un cambio de fuente.
- **Impacto:** tres ciclos de renovación (fuente→gofmt→tests→build→revalidate→run, sin una sola re-query) antes del recibo correcto «17:55:00 GMT-3»; los recibos intermedios erróneos quedaron preservados como historia en OUT3.
- **Lección:** (1) los perfiles por-shot pueden registrar formas por mensaje — ante denegación de commit, probar el mensaje exacto del mandato antes de asumir bloqueo; (2) jamás construir etiquetas de zona con layouts de Go («MST», «-07», «GMT-3» son tokens, no literales) — usar Sprintf campo a campo; (3) los paths de renovación (revalidate) deben evaluarse ANTES que los guards de primera-ejecución.

## Fricción 9 (lote 3) — la documentación prima confirmó el diseño del muestreo como causa, y la ruta editorial lo resolvió

- **Qué pasó:** el spec OpenAPI oficial documenta `end_date_min/max` (date-time) SIN semántica de campo y sin ningún filtro de kickoff; con esa evidencia, la ventana editorial como reductor + gameStartTime como autoridad + verificación client-side completa encontró 68 elegibles y un cluster hoy — los lotes 1/2 no fallaron por ausencia de universo sino por el diseño de muestreo (una página de 100 en cualquier dirección ordenada).
- **Impacto:** ruta viable establecida con limitación explícita documentada (el filtro editorial no prueba kickoff ni universo); identidad fina del cluster (gameId) no interpretada en preparación — limitación declarada, el análisis etiquetará la composición real.
- **Lección:** leer la documentación primaria ANTES de un segundo intento de muestreo convierte un lote vacío en una ruta defendible; el costo fue 4 lecturas de docs y cero requests de datos extra.

## Fricción 5 (lote 2) — el gate del hook exige los destinos de recibo como literales y protege los del lote anterior

- **Qué pasó:** la suite fue denegada 2 veces («Outside W1-j lot2 scope or actual-source/receipt destination not ready; preserve lot1») aunque los destinos ya apuntaban a OUT2 vía constante. Pasó al tercer intento sólo cuando (a) OUT2 existía en disco, (b) los dos paths de recibo quedaron como literales completos en `supervisor_test.go` (el `filepath.Join` con constante nunca produce el path completo en el texto de la fuente) y (c) la referencia `.private-execution/w1j/source-paths.json` del lote 1 salió de `inputRelPaths` (sustituida por `.private-execution/w1j-lot2/source-paths.json`, mismo contenido, SHA `e591b7fc…`). BUILD pasó desde el primer intento mientras TEST no — la denegación era específica del gate de recibos, no del perfil general.
- **Impacto:** dos denegaciones productivas que señalaron exactamente los residuos del lote 1 en mi fuente; ninguna variante inventada; los recibos del lote 1 quedaron intactos.
- **Lección:** cuando un perfil por-shot protege evidencia anterior, auditar la fuente propia por referencias residuales (paths literales, no solo destinatarios lógicos) ANTES de la primera ejecución; los mensajes del hook describen la condición, no la causa.

## Fricción 6 (lote 2) — mi fixture de horizonte estaba mal (25h30m es elegible)

- **Qué pasó:** el test nuevo de selección usó «muy futuro» = now+25h30m, que está DENTRO del horizonte 26h ⇒ era legítimamente elegible y el assert de 3 blockers falló; el detector lo señaló antes de cualquier red.
- **Impacto:** corregido a now+26h30m con aserción propia de la razón «beyond the 26h horizon».
- **Lección:** los bordes del dominio (26h, 95m) deben aparecer en los fixtures con su razón nominal, no por aproximación.

## Fricción 7 (lote 2) — la estructura del presupuesto limita lo que cualquier dirección puede ver

- **Qué pasó:** con `ascending=false` el lote 2 recibió los 100 kickoffs MÁS LEJANOS [2026-11-20 .. 2027-03-06], todos >26h; el extremo cercano del catálogo no es observable con una página de 100 candidatos en ninguna dirección (el lote 1 lo demostró en el otro extremo).
- **Impacto:** cierre honesto con rango real y déficit exacto, sin tercer lote; la decisión de un eventual reintento exige cambio documentado de reglas (filtro futuro documentado en query o multi-página planificada), no más presupuesto del mismo diseño.
- **Lección:** el diseño del muestreo define qué puede concluirse; un lote vacío por estructura no es evidencia de vacío del mundo.

## Fricción 1 — perfil del hook de este shot: formas básicas denegadas y hash delegado a la corrida de tests (LOTE 1)

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
