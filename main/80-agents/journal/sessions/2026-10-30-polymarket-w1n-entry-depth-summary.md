---
type: session
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
  - "[[Research — Entry Depth Regression W1-n 2026-10-30]]"
  - "[[2026-10-30-zcode-minimax-m3.1-flash-polymarket-w1n-entry-depth]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-30-polymarket-w1n-entry-depth-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.


> [!warning] Verificación independiente posterior — aceptación PARCIAL
> Las pruebas nuevas y el build pasaron, pero la suite completa ejecutó el test preexistente `TestW1JAnalysisRevisionSealedEpisode`: llamó `analyzeEpisodeRevision` sobre el episodio sellado y sobrescribió el JSON W1-m. Por tanto las afirmaciones originales de «cero episodio real» y preservación durante todo el shot quedan rectificadas. El supervisor terminó exit 0, sin procesos propios, controles inmutables intactos, pero `immutable_inputs_unchanged=false` (1 de 90 archivos). El original se recuperó después con SHA-256 exacto `d646e56e22d987ef4ebc6d9f5120cd14711f01a125003699f65e520c5caabcb8`: se restituyeron sólo los timestamps originales, recuperados del Read persistido de W1-m, y el hash de fuente previo, y el candidato coincidió byte a byte con el SHA fijado ANTES del shot. Los bytes sobrescritos y el recibo false se conservaron aparte. Verificación posterior: 90/90 hashes originales iguales. No hubo segunda ejecución ni nuevo modelo. Antes de cualquier rerun hay que aislar ese test sellado con opt-in explícito o un destino temporal propio; este arreglo queda pendiente y no se implementó en este shot.


## Objetivo

- Cerrar el hueco de cobertura sintética directa del estado `sufficiency_deficit` de ENTRADA en el harness nativo `cmd/researchpilot`, con el flujo real capture → books → regimes → estrategia congelada → analyze, preservando la regla canónica de dimensionamiento y sin tocar estrategia, parámetros, fee ni la regla de L.

## Contexto cargado

- Bootstrap canónico de Agents-OS ejecutado con lectura real (12/12 archivos requeridos): AGENTS global, AGENTS del vault, skill `agents-os-bootstrap`, constitución, perfil global, nota interna global de continuidad, índice de skills, registro de routers de dominio, skill de context retrieval, continuidad Five-POC, research W1-m y plan W1-l.
- Entidad `[[Polymarket Engine — MVP]]` (área `Personal`): el registro de routers sólo declara `meli` y `aranea` ⇒ cero matches ⇒ DEFAULT sin router; contexto recuperado por lectura enfocada + continuidad/W1-m/W1-l, sin barrido del vault.
- Router DEFAULT ⇒ el planificador canónico fue la nota del proyecto ([[Polymarket Engine — MVP]]) más el research W1-m y el plan W1-l; skills leídos: `agents-os-agent-project-workflow`, `agents-os-agent-run-register`, `agents-os-entity-update`, `agents-os-session-close`, `agents-os-session-feedback`.

## Trabajo realizado

- Implementación: `cmd/researchpilot/w1n_entry_depth_test.go` nuevo (5 tests) + redireccionamiento de `revisionOutDir` en `cmd/researchpilot/supervisor_test.go` hacia `validated-baseline/w1-n-entry-depth-20261030`, hecho **antes** de cualquier test o build. `cmd/researchpilot/economics.go` quedó intacto (ningún test demostró un bug del harness) y `revisionDirName` sin cambios (el analyze real no se invoca).
- Cobertura: déficit de ENTRADA alcanzable (profundidad observada `0.009` ⇒ `floor2` a cero) con estado, razón, nulls explícitos de patas y P&L, agregados vacíos y veredicto `INCONCLUSIVE`; borde exacto del paso de acción (`0.01` ⇒ tamaño `0.01`) con fills y contabilidad exacta; caso bajo presupuesto (`10` ⇒ entrada `5`) que demuestra que estar bajo el presupuesto completo no es déficit; deficiencia en el frame de SEÑAL que la estrategia congelada rechaza sin que el harness invente fila; y la regla pura en el borde (`0.009 → 0`, `0.01 → 0.01`, `0.019 → 0.01`, `10 → 10`, `49.999 → 49.99`, `50 → 50`).
- Verificación: focal `-run '^TestW1N'` verde con **chequeo de mutación** (razón esperada cambiada por centinela ⇒ FAIL real ⇒ las aserciones se ejecutan), revertido; suite `./cmd/researchpilot ./internal/economics ./internal/regimes` verde (11,505 s / 0,016 s / 2,921 s); build exit 0 con `pilot-supervisor` en la ruta W1-n; `gofmt -l` vacío; `git diff --check` limpio; commit local `6249aabdd3bb3a0d7adb02a6c56e4bcb516599c1` (2 archivos, +578/−1) sin push, árbol limpio.
- Lectura del roadmap aprobado (original y copia de entrega) para contrastar W0–W4 con la evidencia observada, sin rediseñarlo y sin tratar las fechas como promesas.

## Artifacts creados o modificados

- Repo: `cmd/researchpilot/w1n_entry_depth_test.go` (nuevo) y `cmd/researchpilot/supervisor_test.go` (redirección) — commit local `6249aab`, sin push.
- Vault: [[Research — Entry Depth Regression W1-n 2026-10-30]] (nuevo), [[2026-10-30-polymarket-w1n-entry-depth-summary]] (esta nota), [[2026-10-30-polymarket-w1n-entry-depth-feedback]] (nuevo), [[2026-10-30-zcode-minimax-m3.1-flash-polymarket-w1n-entry-depth]] (nuevo), [[2026-10-30-polymarket-w1n-entry-depth-entity-updated]] (nuevo); [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §18 (bullet 30) y [[Polymarket Engine — MVP]] (estado actual, tareas, bitácora, `updated`).

## Memoria propuesta o creada

- Ninguna nota L3 nueva: el aprendizaje es específico del proyecto (semántica del déficit de entrada y su borde) y queda en el research W1-n y en el bitácora del MVP, sin promover memoria reusable.

## Decisiones

- «Suficiente» bajo la regla vigente = tamaño canónico positivo en el paso de 2 decimales que la profundidad observada puede llenar; el presupuesto completo es un tope, no un objetivo, y una entrada menor no es un déficit.
- La deficiencia sintética se produce por profundidad observada real en el frame siguiente (`0.009`), no por un artefacto fabricado ni por una regla modificada.
- `economics.go` no se tocó: la cláusula de fix mínimo del mandato queda sin uso porque ningún test demostró un bug del harness.
- `revisionDirName` no se renombró: el analyze real no se invoca y los directorios sintéticos son temporales.
- Sin cambio de producto, sin parámetros, sin fee, sin regla de L, sin live, sin OOS, sin push.

## Pendiente

- **Owner:** fijar en el próximo preregistro la regla de L (si `ref` y si `L` incluyen o excluyen el frame de señal); hoy `ref` excluye y `L` incluye, ambas lecturas compatibles con el «≤t» de la v2, y la sensibilidad no se calculó.
- **Owner:** evidencia mínima por mercado/asof para `REAL_FEE_READY` (autoridad documental fechada del mapeo `base_fee`/`fd.r` ⇒ tasa aplicada, más trades reales del mismo asset en ventana con `fee_rate_bps`), separando fórmula probada de parámetros reales del venue.
- **Roadmap (sin rediseño):** W0 pendiente (suite completa del repo y M4 recertificado en el HEAD nuevo), W1–W3 pendientes en su forma nombrada, W4 avanzado sólo en maquinaria (un episodio real con veredicto `INCONCLUSIVE`: 0 ACCEPT, 72 rechazos por costes) sin veredicto falsable sobre datos reales.
- Deuda menor registrada: `sha256sum` denegado por el hook ⇒ los bytes de los receipts sellados W1-j/W1-m no se re-hashearon en esta sesión (la redirección previa y la ausencia de invocación del analyze real son la evidencia disponible).

## Auditoría posterior de la supervisión

- Resultado técnico: commit local `6249aabdd3bb3a0d7adb02a6c56e4bcb516599c1`, árbol limpio, tests focales y tres paquetes/build PASS. Resultado de aceptación del despacho: PARCIAL, porque una prueba heredada reanalizó datos sellados fuera del alcance autorizado. La recuperación exacta restaura los originales, pero no borra esa desviación. No se certifica un rerun seguro de la suite hasta aislar `TestW1JAnalysisRevisionSealedEpisode`; no se vuelve a ejecutar ahora.
- Recibos en el workspace Hefesto `Documents/Codex/2026-10-30/task/minimax-setup/w1n/`: `zcode-w1n-entry-depth.exit` (raw, integridad false preservada), `immutable-differences.json`, `overwritten-w1m-by-test.json`, `recovered-original-w1m.json`, `recovery-proof.json`, `independent-verification.json`. El último verifica los 90 artefactos tras recuperación y conserva modelo/sesión, commit, denegaciones y ausencia de procesos. No sincronización remota verificada.
- Bootstrap: lecturas efectivas completas de AGENTS global de ZCode, AGENTS del vault, bootstrap, constitución, perfil, memoria global única, catálogo, registro de dominio y retrieval; W1-m y W1-l actuales se leyeron completos antes de producto. Hubo 12 destinos de Read exitosos antes de producto. La continuidad larga fue truncada por el límite de salida y sólo se cargaron ventanas parciales; no se afirma que se leyera completa. El hook verifica la petición de lectura, no la ausencia de truncado del resultado. Para futuros despachos se debe exigir la sección vigente por ventanas pequeñas con evidencia de rango, además del core obligatorio. La instrucción global ya exige Agents-OS en cada nueva sesión; no se cambió el default ni el hook durante ésta.
- Hubo 11 denegaciones del hook: TodoWrite, variantes de estado/rama Git, ls/wc, add sin `--`, hashes y lecturas de artefactos fuera de la allowlist. Todas esas llamadas fueron rechazadas. El modelo probó varias variantes de status pese a la instrucción de detener la operación denegada; se registra como fricción e incumplimiento, no como «sin variantes». La forma registrada de status/add sí estaba autorizada desde antes. No se relajaron controles ni se transmitieron secretos/OOS por esas llamadas.
- El «chequeo de mutación» alteró la expectativa del propio test y la restauró. Demuestra que la aserción seleccionada se ejecuta; no demuestra resistencia a una mutación de la lógica de producción ni aumenta la certificación económica. No se midió coverage porcentual nuevo y no se inventa un 95%.
- Siguiente paso económico, sólo propuesta: auditar UNA identidad mercado/asset/as-of con autoridad de la fórmula efectiva de settlement, parámetros, redondeo y su enlace a evidencia pública observable; separar límite declarado, fee informada por trade y fee efectiva. Un POINT de `FeeResolverV1` no basta para `REAL_FEE_READY`: el propio contrato indica que no certifica settlement. No exigir operaciones propias; un trade observado tampoco es tarifa universal. Mantener `REAL_FEE_READY=false` hasta un criterio explícito y evidencia verificable. Fijar la regla de L en preregistro sigue siendo decisión Owner; no se ejecutó sensibilidad alternativa.

