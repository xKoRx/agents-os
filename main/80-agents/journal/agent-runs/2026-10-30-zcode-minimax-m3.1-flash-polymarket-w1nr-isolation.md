---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Default Suite Isolation W1-nR 2026-10-30]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
model_source: host
task_type: coding
task_complexity: medium
outcome: success
verification: passed
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
  - project/polymarket-engine
---

# Agent Run — 2026-10-30-zcode-minimax-m3.1-flash-polymarket-w1nr-isolation

## Trabajo

- **Objetivo:** aislar la suite por defecto de `cmd/researchpilot` para que no pueda reanalizar el episodio sellado ni sobrescribir artefactos de evidencia: opt-in explícito en el test histórico con salida a `t.TempDir()`, y opt-in explícito en la exportación de recibos de `TestMain` con raíz nueva y directorios propios únicos.
- **Alcance atribuible a esta combinación superficie×modelo:** los tres archivos de test del paquete `cmd/researchpilot` (`economics_test.go`, `supervisor_test.go` y el nuevo `w1nr_isolation_test.go`); dos commits locales sobre `w0/offline-causal-replay-20261027`, sin push: `4acf954407ede3e5bb42d057f35d7b2c7f02c913` (aislamiento de la suite) y `e4d201a391bf97b5f43c5287366deda57242e258` (restauración de la garantía de corrida verde en la exportación de recibos, tras la revisión de la supervisión). Sin cambios en código de producción, estrategia, dimensionamiento, fees, parámetros ni en la regla de L.
- **Artefactos afectados:** repo `polymarket-engine` (3 archivos de test, +677/−70 en los dos commits); nota de research [[Research — Default Suite Isolation W1-nR 2026-10-30]]; binario `pilot-supervisor` construido en la ruta de salida del shot.

## Evidencia

- **Validaciones ejecutadas:** preflight de seguridad `safe: true` (sin problemas; `sealed_unchanged: true`), re-corrido después de cada edición de fuente y antes de cada corrida; focal `-run '^TestW1NR'` verde; histórico `-run '^TestW1JAnalysisRevisionSealedEpisode$' -v` con `--- SKIP` y sin variables de opt-in presentes; suite `./cmd/researchpilot ./internal/economics ./internal/regimes` (tres corridas registradas: dos con el flake de timing preexistente `TestStepSequenceWaitsForAbsoluteSlotStart` a 199.512005 ms y 199.026946 ms frente al umbral de 200 ms, tercera verde); build de `pilot-supervisor` exit 0; `gofmt -l` vacío; `git diff --check` limpio; árbol limpio tras el commit.
- **Comprobación de mordida de la regresión nueva:** con el guard `code != 0` temporalmente retirado, la suite focal **falló** en `TestW1NRReceiptExportRefusedAfterFailedSuite` y el hijo imprimió `offline-preflight and inputs receipts written: all required cases passed` sobre una suite fallida — el defecto exacto reportado por la supervisión. Restaurado el guard, la misma suite es verde.
- **Resultado observable:** la suite por defecto no escribe ninguna ruta de artefactos externa; el test histórico no alcanza el episodio real sin opt-in; y una suite **roja** ya no puede acuñar recibos `all_required_cases_passed`.
- **Limitaciones de la evidencia:** la medición de los 90 hashes sellados y de la lista final de archivos corresponde al supervisor, no a esta corrida; el preflight sólo informa `sealed_unchanged: true`. No se ejecutó análisis histórico ni se leyó un episodio real. La suite completa **no es fiablemente verde en este host**: el flake de timing preexistente incidió dos de tres corridas registradas, y el test que falla no fue tocado por esta corrección (el diff sobre `supervisor_test.go` son 8 líneas dentro de `TestMain`). No se midió coverage porcentual y no se produjeron cifras económicas.

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- **Correctness:** no se agrega score autoevaluado: la evidencia objetiva disponible es el resultado de los comandos (gate, focal, skip, suite, build) y no una medición independiente.
- **Autonomy:** no se agrega score autoevaluado.
- **Efficiency:** no se agrega score autoevaluado.
- **Tool use:** no se agrega score autoevaluado.
- **Overall:** no se agrega score autoevaluado.

## Resultado

- **Outcome:** partial — el defecto de aislamiento quedó corregido y verificado, pero la revisión de la supervisión encontró una regresión en la semántica de recibos (una suite roja podía acuñar `all_required_cases_passed`), corregida en un segundo commit con una regresión negativa que se demostró mordiendo. La suite completa **no es fiablemente verde en este host** por el flake de timing preexistente; la tercera corrida registrada fue verde.
- **Rework posterior:** la revisión de la supervisión rechazó la primera entrega por la regresión de la garantía de corrida verde; ese rework está en `e4d201a`. El Owner todavía no ha reaccionado a la corrección.
- **Aprendizaje para comparar herramientas:** en superficies con hook de alcance, el gate de seguridad previo es la fuente más barata de verdad sobre la forma exacta que debe tener el código (orden de sentencias y literales); implementarlo contra el gate evitó un ciclo de ensayo y error sobre el comportamiento correcto. Y una garantía semántica que se traslada a otro mecanismo (aquí, el opt-in de exportación) debe conservar **todas** sus precondiciones, no sólo la nueva: la Corrección del `if code == 0` se perdió al reescribir `TestMain` y sólo la revisión externa la detectó, porque las pruebas del shot no cubrían la ruta de suite roja.
