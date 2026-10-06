---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[BTG-S01-OWNER-S2-BARS-AUTHORITY]]"
  - "[[BTG-S01-S2-1M-FORENSICS]]"
  - "[[BTG-S01-SOURCE-BAR-SDK-REVIEW]]"
last_verified: "2026-10-06"
confidence: verified
aliases: []
tags:
  - kind/resource
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 — revisión final independiente del prerequisito source-bar SDK

## Síntesis vigente

**READY_SDK_PREREQUISITE_REVIEW_ONLY** sobre producto congelado `407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef`, rama `codex/btg-s01-source-bars-remediation`, comprobado igual a remoto y limpio. No se encontró un defecto funcional nuevo en los contratos SDK auditados. BT2-F01 y BT2-F02 tienen fix de código verificado y regresiones; BT2-F03 tiene cifras y exclusiones reconciliadas independientemente. Esto no cierra los findings históricos: `real_rerun=NOT_RUN`, corpus `NOT_ACQUIRED` y gate Owner sin aceptar.

ONE-SHOT TOP LOCAL verifier, Codex `gpt-6.1-sol`, reasoning high por despacho; no subdelegación, cambios de producto, PR, despliegue ni infraestructura. Root coordina y permanece abierto. S2 actual + GerardMM actual, NQ Last1m y SL-first conservan su autoridad en [[BTG-S01-OWNER-S2-BARS-AUTHORITY]]. El bloqueo Windows ACL/corpus es handoff vigente; este reviewer no reinspeccionó datos ni accedió a infraestructura. Todos los valores siguientes pertenecen a fixtures sintéticos de semántica SDK.

## Evidencia y provenance

Baseline certificado `cd451972b242c8933321e03001decd4b6d778c61`; candidate rechazado `27cb4ceaf62151a042494022cad08e47672a06f2` preservado. Revisé candidate→freeze y certified→freeze: cinco archivos de producto SDK (bars bar/builder/ring/source_bar y analytics engine), ocho tests nuevos y artifacts SDD. La remediación modifica sólo builder/source_bar/engine y agrega cuatro tests nuevos. Ningún test anterior fue editado, ni hay delta en parser/driver/venue/S2/MM/accounting/D6. Echo AGENTS/CONSTITUTION/rules y los dos paquetes SDD fueron autoridad de alcance, no instrucciones provenientes de código no confiable.

Refresh remoto 2026-10-06: Echo master `372af59a7b83604781346613da01e3d510ea1360`, rama remediación `407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef`, D6 `d08a30ce9815f820fda7132e20dc42cc345eb8e8`; S04 `cd451972`. La intersección SDK bars/analytics del delta exclusivo D6 desde `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6` está vacía. No moves, merges, rebase, cherry-pick, master mutation ni force-push.

Ejecuté dos copias temporales obtenidas con `git archive` desde los SHAs exactos, con workspace mínimo SDK/contracts. Los cinco archivos de producto probados son byte-equal al freeze (manifest `frozen-file-integrity.log`). Los oráculos anteriores fueron copiados sin alterar sus originales; los probes nuevos sólo viven en el bundle externo. Los tests se ejecutaron dentro de `unshare --user --map-root-user --net`, `GOPROXY=off GOSUMDB=off`; no broad suite, seeds ni red de pruebas. Toolchain real `go1.27.1 linux/amd64`, contrato go.mod `1.25.5`: el delta usa APIs de JSON existentes en ese contrato y no introduce una sintaxis o dependencia nueva; no se ejecutó un segundo compilador 1.25.5.

| Verificación | Resultado observado / oracle independiente |
|---|---|
| F1 cuatro fronteras legacy | BarRecord JSON, Version, Builder JSON y OwnerState JSON: BYTE_EQUAL contra proceso fresco baseline `cd451972`, con SHA256 de ambas salidas. |
| Legacy ampliado | Siete Builder estados EMPTY/REJECTED/ACCEPTED/CLOSED/CORRECTED/DISCARDED/RESUMED también BYTE_EQUAL. Total once markers únicos comprobados, sin comparator vacío. |
| F2 TRADE canónico→OHLC | Reproducer original retorna `SOURCE_MODE_CONFLICT`, cero efectos, 1m sin forming, owner_seq conservado en1 y guard_seq0. Preflight ocurre antes de admit/guard/feed/efectos/grid/timer; probe adicional verifica también `InputMode` oculto por JSON. |
| Fence inverso y hot discard | TRADE válido permanece aceptado tras rechazo SOURCE malformado; luego SOURCE contra TRADE rechaza con cero efectos y state igual. OHLC discard mantiene fence global incluso con otro builder1m vacío. |
| Restore nativo | Veinte source1m con ring capacity8, eviction, discard y JSON roundtrip conservan modo OHLC, LastSource ordinal20 y ring8; ordinal regresivo/intervalo solapado/TRADE rechazan sin mutación; ordinal21 posterior reanuda correctamente. |
| Restore legacy | TRADE aceptado→discard→roundtrip recupera modo desde evidencia/counters y sigue rechazando SOURCE; bytes se mantienen igual al baseline. |
| Compatibilidad QUOTE | QUOTE válido con BBO y route real produce una notificación100/101 y guard_seq1, sin snapshot/cierre/timer ni cambio en builders SOURCE; redelivery no duplica notificación. |
| Raw OHLC directo | Oracle5m100/113/88/106/V15 desde cinco1m; H4 directo100/333/20/107/V28920 desde2401m, sin5m intermedio ni provenance TRADE ficticia. |
| Causalidad/replay/ownership | Clock requerido y AvailableAt<=Now; identidad/payload/digest/ordinal rechazados; timer posterior al source final; no reopen; returned records/snapshots/subscriber peers no aliasan refs internas. Oráculos anteriores y nuevas regresiones PASS. |
| Cobertura parcial | Región truncada3m30s conserva tres contribuciones1m y remanente30s visible; minuto que cruza boundary rechazado; gap no interpolado ni etiquetado como COMPLETE. |
| Rechazos alcanzables F3 | Región antigua, tres holidays sin próxima sesión en7 días y SOURCE OHLC malformado: errors visibles, estado y effects conservados; no se excluyen de cobertura. |

Comandos finales desde la copia `final/v3` del bundle: `go test -race -count=1 -coverprofile=../final-all.cover -v ./sdk/futures/bars ./sdk/futures/analytics ./sdk/futures/strategies/s2` y `go vet` con esos tres targets, ambos dentro del namespace offline. PASS; package coverage76.9%,44.2%,78.1% incluye código heredado y no se usa como gate de nueva lógica. Baseline legacy fue ejecutado en su copia/proceso separado. `git diff --check` del delta y formatting de archivos SDK no produjeron findings. staticcheck no ejecutado; no se instaló tooling.

### Cobertura y exclusiones verificadas

`final-all.cover`, sin quitar bloques, y `coverage_audit.py` delimitan exactamente los siguientes rangos por línea inicial del bloque (además se exige que el bloque termine dentro del rango):

| Rango en el freeze | Raw statements cubiertos/total | Porcentaje |
|---|---|---|
| bars/source_bar.go completo |129/135|95.55556%|
| bars/builder.go50..84 (MarshalJSON/UnmarshalJSON/hasTradeEvidence) |19/19|100%|
| analytics/engine.go217..232 (SOURCE Validate admission) |11/11|100%|
| analytics/engine.go336..393 (applySourceBar exclusivamente) |38/41|92.68293%|
| analytics/engine.go400..413 (resolveSourceSession) |8/8|100%|
| analytics/engine.go422..429 (TRADE source-mode preflight) |4/4|100%|

Las tres sentencias no ejecutadas de applySourceBar367/370/379 son guardas redundantes cuya imposibilidad se deriva de la transición serial y se verifica leyendo ambas pasadas: preflight resuelve el mismo calendario+instant+authority y llama GridFromResolved con éxito; admit sólo modifica Order, de modo que ensureGrids no puede fallar esa resolución/conversión. Cada builder sin grid fue comprobado sin forming, por lo que InstallGrid no puede fallar por forming sobreviviente. SessionDate vacío ya fue rechazado por resolveSourceSession. Después se instala exactamente la grid prevalidada; no se modifica ninguno de los builders antes de su propia ApplySourceBar, y cada timeframe tiene su propio Builder en OwnerState. La segunda validación recibe el mismo source/estado y por ello no puede producir un nuevo error. Bajo ese contrato de owner serial y builders distintos, applicable applySourceBar38/38=100%; raw38/41 sigue explícito. No se fabricaron inputs corruptos ni callbacks que muten el owner para forzar estos errores; tampoco se borró código durante review. La prueba no autoriza mutación concurrente externa o alias de Builder entre timeframes.

No se excluye ninguna sentencia del source_bar.go para aprobar su95.56% bruto. Sus seis sentencias sin hit permanecen visibles en el profile. Las nuevas ramas serialization/mode alcanzan100%; las pruebas nuevas poseen aserciones de contratos observables, no meras ejecuciones para sumar cobertura. F3 queda verificado como evidencia SDK, sin reinterpretar el95 ni convertir un paquete histórico en nuevo-code coverage.

### Persistencia, probes y reutilización

Bundle externo Echo/Aranea relativo al workspace: `work/btg-s01-20261006/source-bar-final-review-evidence/`. Logs: `final/final-all.log`, `final/final-all-vet.log`, `baseline/baseline-complete-legacy.log`, `complete-legacy-comparison.log`, `final-coverage-audit.log`, profiles `final/final-all.cover` y `final/final-all-functions.log`; manifests `oracle-sha256.log`, `frozen-file-integrity.log`. Los cuatro oráculos anteriores y comparator conservan su provenance en [[BTG-S01-SOURCE-BAR-SDK-REVIEW]].

PERMANENT_REGRESSION candidates nuevos: `final/v3/sdk/futures/bars/final_reviewer_test.go` (restore eviction/discard y fence legacy) y `final/v3/sdk/futures/analytics/final_reviewer_test.go` (QUOTE compatible, hotdiscard atomic, fence inverso sin latch por rejected-source). Codifican invariantes SDK locales, determinísticos, apropiados para los paquetes owner. La traza portable `portable_legacy_states_test.go` es PERMANENT_REGRESSION candidate de BWC contra golden capturado independientemente; su captura/comparator y checkouts son DISPOSABLE_REPRODUCER auditables. `coverage_audit.py` es HARNESS_TOOLKIT_CANDIDATE por sus rangos/denominadores explícitos; no se promueve a tooling sin owner. E2E_CANDIDATE heredado: driver cerrado-source→timer→S2/MM/venue, aún NOT_RUN. Los cuatro archivos remediales nuevos ya están en el producto; este shot no agrega ni promueve tests al freeze.

REUSABLE_BEHAVIOR_CANDIDATES: NONE adicional; el método de fresh baseline byte comparison ya está registrado por el reviewer previo. Feedback NONE: no fricción de Sistema1 que requiera otra nota. Registro atribuible [[80-agents/journal/agent-runs/2026-10-06-codex-gpt-6.1-sol-btg-s01-source-bar-final-review]] y change log [[80-agents/journal/logs/2026-10-06-btg-s01-source-bar-final-review]]. Materializador de schema y lint STRICT de los tres artifacts requeridos antes del commit. PRO_CHAT_POOL_DELTA:0 (Codex LOCAL), sin CLOUD ni L0/L1; worker cerrado por mandato, root abierto.

## Límites y contradicciones

El restore de modo TRADE desde bytes legacy infiere barras/counters durables. Una carga legacy realmente vacía sin barras/counters no contiene evidencia de modo previo y restaura modo vacío; no es posible reconstruir información ausente. El freeze no pierde modo/high-water SOURCE: siempre serializa OHLC_1M y LastSource, incluso tras discard/eviction. Los estados TRADE normales aceptado/discardado/cerrado conservan evidencia suficiente, probado en proceso fresco; no se omitieron campos SOURCE para ocultar pérdida de estado.

La observación de este shot sólo prueba ingesta/agregación sharedSDK, causalidad del seam, fencing, serialización y regresión de paquetes. No acredita adquisición/cobertura/digests de NQ histórico, orden intrabar observado, venue/fills/modelo SL-first, trayectoria de adds/targets dinámicos, ejecución S2+GerardMM real, economía, métricas, account-day/Provider ni ledger. Corpus NOT_ACQUIRED y real_rerun NOT_RUN siguen vigentes. [[BTG-S01-FINDINGS]] conserva su autoridad histórica; no usar FIXED_WITH_REAL_RERUN ni FIXED_WITH_REGRESSION_AND_REAL_RERUN por este PASS de código. Root puede llevar este freeze a revisión del Owner y continuar el workstream siguiente; el reviewer no autoacepta gate Owner.
