---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[BTG-S01-OWNER-S2-BARS-AUTHORITY]]"
  - "[[BTG-S01-S2-1M-FORENSICS]]"
last_verified: "2026-10-06"
confidence: verified
aliases: []
tags:
  - kind/resource
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 — revisión adversarial del source-bar SDK

## Síntesis vigente

REJECT_FOR_CORRECTION sobre `27cb4ceaf62151a042494022cad08e47672a06f2`: F1/F2 son defectos MAY reproducidos y F3 es un gap MAY de evidencia del gate de cobertura. El seam agrega OHLCV correctamente y los fixes provisionales de replay/cause/ownership funcionan, pero este freeze no satisface todos los invariantes. No se acepta ningún gate Owner.

ONE-SHOT TOP LOCAL, función verifier, superficie Codex, identificador exacto de despacho `gpt-6.1-sol`, reasoning_effort high. Baseline `cd451972b242c8933321e03001decd4b6d778c61`. Sólo SDK bars/analytics y regresión S2: sin parser, driver, venue, estrategia/MM, infraestructura, D6 ni real-run. S2 + GerardMM, corpus NQ Last1m y SL-first vienen de [[BTG-S01-OWNER-S2-BARS-AUTHORITY]] y [[BTG-S01-S2-1M-FORENSICS]]. Corpus NOT_ACQUIRED es handoff del Manager al iniciar este shot; el reviewer no inspeccionó adquisición ni recibió bytes. Todos los valores de las pruebas son fixtures sintéticos de semántica SDK.

## Hallazgos

| ID | Severidad | Contrato / origen | Evidencia y oracle | Ownership / siguiente paso |
|---|---|---|---|---|
| F1 | MAY | Regresión de serialización TRADE frente a SPEC frozen: exige conservar serialized bytes sin limitarlo a BarRecord. `bars/builder.go:35-36,134` agrega y fija `InputMode=TRADE`. | `TestReviewerLegacyBytes` y `TestReviewerLegacyOwnerBytes` sobre baseline y frozen, más `compare_legacy.py`: BarRecord JSON y Version son BYTE_EQUAL; Builder agrega `/input_mode="TRADE"`; OwnerState agrega `/Builders/5m/input_mode="TRADE"`. Eliminar sólo ese campo devuelve igualdad estructural. | SDK Builder / NORMAL remedial: conservar bytes TRADE y el fence durable; Manager conserva autoridad de contrato. Root confirmó corrección sin Ownerdelta. |
| F2 | MAY | Nuevo rechazo TRADE/OHLC sin preflight global: `analytics/engine.go:416-452` admite owner/guard antes de `feedBuilders`; `feedBuilders` aplica en orden y `Builder.ApplyTrade` rechaza modo tarde. | `TestReviewerCanonicalMixedModePreflightAtomic`: aplicar SourceBar a5mOHLC, agregar1m vacío con misma grid, enviar TRADE canónico válido con clock causal. Error `SOURCE_MODE_CONFLICT` en5m, pero1m ya está FORMING TRADE, owner_seq1→2, guard_seq0→1 y se retornan3 effects. Oracle no-partial-mutation FAIL. | SDK analytics / NORMAL remedial: preflight del nuevo fence antes de guard/admit y antes de mutar cualquier builder. No refactor general de TRADE. |
| F3 | MAY de verificación | Gate95 de nueva lógica no demostrado con la evidencia entregada; exclusiones declaradas como inalcanzables incluyen caminos alcanzables y deben reconciliarse. | Original source_bar.go122/130=93.846%; applySourceBar37/41=90.244%; resolver7/8=87.5%. `source_bar.go:93` se alcanza con SourceBar shape válido, ordinal3 y región vieja tras cerrar dos regiones: ocurre antes del high-water guard98. `engine.go:408` se alcanza con calendario válido sin sesión dentro de7 días. `engine.go:218` también es rechazo real de OHLC malformado. | NORMAL / verifier fresco: mantener regresiones reales y publicar rangos/denominador exactos; eliminar ramas verdaderamente imposibles según policy aplicable o justificar el contrato, sin etiquetar rechazos de caller como defensas inalcanzables. |

F3 distingue comportamiento de evidencia: los guards93/218/408 rechazan correctamente y sin mutación; son gaps de cobertura/justificación, no tres errores funcionales adicionales. El número47/52 del implementer puede agrupar admisión y transición;37/41 aquí identifica sólo la función applySourceBar. No se acusa error aritmético sin un range idéntico.

## Pruebas ejecutadas

Ejecución en copias temporales aisladas desde los dos SHAs; el producto original permaneció limpio. Desde `v3/`, siempre `unshare --user --map-root-user --net env GOPROXY=off GOSUMDB=off`; sin broad suite ni conexión de infraestructura.

| Comando dentro del namespace | Resultado | Log externo |
|---|---|---|
| `go test -race -count=1 -coverprofile=<external>/frozen-original.cover ./sdk/futures/bars ./sdk/futures/analytics ./sdk/futures/strategies/s2` | PASS; package coverage74.7/32.6/78.1%, respectivamente; cifras incluyen código heredado. | frozen-original-tests.log |
| `go vet ./sdk/futures/bars ./sdk/futures/analytics ./sdk/futures/strategies/s2` | PASS | frozen-vet.log |
| `go test -race -count=1 -run '^TestReviewer' -coverprofile=<external>/frozen-adversarial.cover -v ./sdk/futures/bars ./sdk/futures/analytics` |20 top-level PASS,1 FAIL(F2),9 subtests PASS. | frozen-adversarial-final.log |
| Baseline `go test -count=1 -run '^TestReviewerLegacy' -v ./sdk/futures/bars ./sdk/futures/analytics` | Captura baseline PASS; comparator de cuatro salidas FAIL por F1. | baseline-legacy.log; legacy-serialization-comparison.log |
| `go tool cover -func=<external>/frozen-original.cover` | Funciones/rangos auditados; no exclusiones en profile. | frozen-original-functions.log; coverage-audit.log |

`gofmt -l` de los siete archivos SDK y `git diff --check` del delta frozen no produjeron findings. staticcheck no estaba disponible y no se instaló. Ningún test existente fue modificado; sólo cuatro archivos de oráculos nuevos se copiaron a los checkouts desechables.

## Oráculos y clasificación

PERMANENT_REGRESSION: F2 atomicidad del rechazo canonical, F1 compatibilidad bytes/Version de BarRecord+Builder+OwnerState, payload cambiado con mismo digest, ordinal reutilizado, fences directos, orden/mode tras discard, ownership de timer-return/Last/Find/Recent/snapshots/subscribers, causa mixta, preflight entre targets, input malformado y TRADE/canonical rechazado antes de latch. Son candidatos para promoción al producto por el carril autorizado; aquí sólo existen fuera del producto.

PERMANENT_REGRESSION: oracle5m explícito100/113/88/106/V15; H4 directo desde240 filas100/333/20/107/V28920, sin5m intermedio. Ring1m capacity8 retiene exactamente8 cerradas+1forming tras20 fuentes; eviction y session roll no permiten ordinal regresivo. Región truncada3m30s retiene3m de cobertura y remanente30s visible, rechaza minuto que cruza cierre. No se encontró cálculo floor(duration/1m) ni etiqueta falsa de100% completeness en este freeze. Región vieja y calendario con holidays prueban las rutas alcanzables de F3.

E2E_CANDIDATE: en el futuro driver, source1m terminada debe entrar antes del timer del agregado y antes de cualquier decisión que dependa de HLC; este shot no prueba causalidad driver→S2/MM/venue. DISPOSABLE: generación del golden legacy, checkouts de comparación y harness de ejecución; resultados y SHA256 de oráculos quedan retenidos.

## Cobertura y costo

La unión por max hit de los mismos bloques del profile original y de los oráculos, sin excluir líneas, produce source_bar.go123/130=94.615%, applySourceBar37/41=90.244% y resolver8/8=100%. Un oracle FAIL puede ejecutar ramas y aportar cobertura, pero no aporta aceptación. Raw profiles y rangos permanecen disponibles para el verifier fresco.

El guard durable LastSource retiene una sola ref; el resto de las refs se limita a forming y al ring dimensionado por demanda. No hay cache del corpus completo. Inspección estática: findSource recorre las refs retenidas y los clones copian slices; su costo crece con la ventana retenida. El oracle de eviction prueba el bound estructural pequeño; no se midió throughput ni se extrapola rendimiento histórico.

## Evidencia y provenance

Repositorio externo Echo, workspace Aranea relativo `work/btg-s01-20261006/source-bar-review-evidence/`: reviewer_test.go, analytics_reviewer_test.go, legacy_reviewer_test.go, legacy_analytics_reviewer_test.go, compare_legacy.py, oracle-sha256.log y logs/profiles listados. Fuente SHA256 de cada reproducer se conserva en oracle-sha256.log; no se copian dumps ni repos al vault. Fixtures/oráculos fueron escritos antes del freeze y ampliados sólo por nuevos riesgos; ningún producto fue reparado por este reviewer.

Refresh final: Echo master `372af59a7b83604781346613da01e3d510ea1360`, S04 `cd451972b242c8933321e03001decd4b6d778c61`, D6 `d08a30ce9815f820fda7132e20dc42cc345eb8e8`. Exclusive D6 desde `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6` → SDK vacío. No merges/cherry-picks/rebase; worktree D6 intacto. Diff frozen: siete archivos SDK autorizados y cuatro artifacts SDD; cero cambios en tests existentes y cero delta Backtester/S2/MM.

## Cierre ONE-SHOT

Review atribuible en [[80-agents/journal/agent-runs/2026-10-06-codex-gpt-6.1-sol-btg-s01-source-bar-review]]. Change log [[80-agents/journal/logs/2026-10-06-btg-s01-source-bar-review]]. Feedback NONE: no gap de Sistema1 que amerite nueva nota; no feedback global especulativo. Sin L0/L1 ni memoria duplicada. PRO_CHAT_POOL_DELTA:0; sólo Codex LOCAL, sin receipts CLOUD inventados.

Worker cerrado por mandato explícito del Manager; root permanece abierto. El siguiente paso es corrección NORMAL y un verifier TOP fresco sobre un nuevo freeze; este worker no re-revisa ese futuro fix ni acepta gate Owner.
