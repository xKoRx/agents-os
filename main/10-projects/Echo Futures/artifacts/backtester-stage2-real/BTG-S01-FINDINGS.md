---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-S01-REAL-GERARD-RESULT]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-FINDINGS

## Propósito

Registrar las divergencias materiales verificadas del carril BTG-S01 sin convertir pruebas sintéticas del prerequisito SDK en evidencia histórica. Ningún finding se cierra por PASS de paquetes; el cierre requerido sigue siendo FIXED_WITH_REGRESSION_AND_REAL_RERUN o DISPROVED_WITH_EVIDENCE.

## Contenido

### Corte y procedencia

Corte final2026-10-06: trece exports reales legibles y hasheados; smoke RAW y longitudinal DERIVED con código posterior a los fixes terminan COMPLETE y fresh reproduce IDENTICAL. BT2-F01–F11 conservan abajo su reproducción/regresión específica y review independiente anterior. Su rerun histórico ahora es bt-b9676b4b…e4d44 y bt-bd627d8a…029f sobre el candidato integrado que contiene los fixes; no se dice que el mercado haya disparado cada error artificial de compatibilidad, control o cleanup.

El diff producción fb210ac4→d69d03ec sólo cambia atribución FAILED en driver/finish, resumen/residual en finish y getter accounting readonly: conserva los fixes F01–F11 previamente revisados. Cada cierre usa la regresión específica más este rerun auténtico del producto integrado; no convierte fixtures legacy TRADE, aliases, mutation ni control intrabar en ticks observados. Cobertura full13/rollover y recuperación de gaps quedan como frontera de contrato/datos, no finding de bug cerrado por un slice único.

| Finding | Prueba específica preservada | Evidencia real posterior al fix | Cierre |
| --- | --- | --- | --- |
| F01 | Once oráculos legacy bytes fresh BYTE_EQUAL / golden permanentes | Código SDK407 conservado; OHLC prepare/run/reproduce correcto | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F02 | Preflight mixed mode atómico RED→GREEN | Modo OHLC consistente en toda agregación5m/H4 del run | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F03 | Coverage raw/aplicable con guards demostrados en407 | Misma lógica SDK sobre38909barras auténticas | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F04 | Mutable head/tail/append/short horizon RED→GREENe44 | Receipt/snapshot de archivos auténticos y freshsamehash | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F05 | SameFile symlink/hardlink/relative aliases; distinctfiles permitido | Binding físicoNQ12-23 con original/derivedmanifest explícito; no multi-stream claim | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F06 | Firedstorage bound/causal trace regression | 38909barras completas en6m47.02, no timeout ni historial timer bloqueante | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F07 | Latecontrols+30s/intervalend/horizon guards race | Trayectoria histórica normal sin caller cashflow; guard conserva regresión específica | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F08 | Reset17h/before/at/after/DST RED→GREEN171 | WarmupOct15→Nov23 cruza resets y ChicagoDSTNov5 sin colisión | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F09 | FD cleanup public run/reproduce error RED→GREEN | Ambos CLI reales terminan/seallan/cierra proceso; no error-outdir artificial observado | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F10 | Scope authenticity/NO_ADDS/preparation assertions | Manifestreal declara explícitamente noadjudicarautenticidad/modelodeejecución | FIXED_WITH_REGRESSION_AND_REAL_RERUN |
| F11 | EOF/readmission closeexactonce RED→GREEN15422 | CLI histórico run/reproduce native completo con mismo producto integrado | FIXED_WITH_REGRESSION_AND_REAL_RERUN |

Rerun común identificado para cada fila: long RunID bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f; code d69d03eceeac1495522473a95baf08087f5c28b3; result/repro SHA256 b11bd4e7776762523f29c9dda8e264c98818f5e209c7b051e72e6e671222a637, 270781records/113ops/78fills. No blanket claim de todos los modos/controlbranches con datos de mercado. BT2-F12–F14 tienen además reproducciones reales específicas antes/después descritas abajo. Esta adjudicación Root no sustituye aceptación Owner ni adversarial S04.

### BT2-F01 — serialización legacy modificada

- severity: MEDIUM.
- dataset/rango: traza TRADE local idéntica sobre baseline y candidate; SYNTHETIC_REFERENCE_ONLY, sin rango NQ histórico.
- expected: bytes JSON de BarRecord, Builder y OwnerState TRADE y Version legacy iguales al contrato previo.
- actual: BarRecord JSON/Version BYTE_EQUAL; Builder añade `input_mode:"TRADE"`; OwnerState añade `Builders/5m/input_mode:"TRADE"`. Al retirar sólo ese campo hay igualdad estructural, que no sustituye la igualdad de bytes exigida.
- first_divergence: serialización del primer Builder TRADE, candidate `27cb4cea`; `TestReviewerLegacyBytes` y `TestReviewerLegacyOwnerBytes` frente a `cd451972`.
- owner: SDK bars/mode serialization; raíz coordina, NORMAL implementa en carril correctivo.
- fix: `407e03dd`; Marshal omite sólo modo TRADE redundante, restore recupera evidencia durable; OHLC modo/high-water explícitos. Once salidas legacy BYTE_EQUAL contra fresh baseline.
- regression: golden hashes independientes en source_serialization_test.go; oráculos fresh de once estados/fronteras y restore eviction/discard PASS. PERMANENT_REGRESSION en producto, probes externos retenidos.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F02 — rechazo de modo tras mutación parcial

- severity: HIGH.
- dataset/rango: probe local con builder 1m vacío, 5m OHLC y TRADE canónico válido; SYNTHETIC_REFERENCE_ONLY, sin rango NQ histórico.
- expected: SOURCE_MODE_CONFLICT antes de admission/guard/efectos o mutación de cualquier builder.
- actual: rechazo en 5m después de tres efectos, apertura 1m TRADE, OwnerInputSeq 1→2 y Guard.LastAppliedSeq 0→1; retry consume un guard ya avanzado.
- first_divergence: `Engine.applyCanonicalEvent` admite/aplica guard y primer builder antes de verificar el modo de todos; `TestReviewerCanonicalMixedModePreflightAtomic` sobre `27cb4cea`.
- owner: SDK analytics preflight del nuevo modo, sin refactor de validación canónica legacy.
- fix: `407e03dd`; preflight de modo de todos los builders antes de admission/guard/grid/aggregation.
- regression: source_contract_regression_test.go y oracle independiente PASS; cero efectos y estado/owner_seq/guard inalterados. TOP nuevo verifica también hidden mode, hot discard y fence inverso.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F03 — gate de cobertura no demostrado

- severity: MEDIUM.
- dataset/rango: perfiles y probes unitarios offline del candidate; SYNTHETIC_REFERENCE_ONLY, sin rango NQ histórico.
- expected: >=95% de lógica nueva aplicable, rangos/denominadores explícitos y exclusiones de ramas realmente inalcanzables demostradas.
- actual: source_bar.go bruto 122/130=93.846%; applySourceBar puro 37/41=90.244%; resolver 7/8=87.5%. La cifra 47/52 publicada puede agregar once statements de admission y no se trata como error aritmético sin delimitar el rango. El guard de región antigua, el error de resolver con tres holidays y el rechazo de SourceBar malformado son alcanzables; no justifican declarar 100% aplicable excluyéndolos. La unión con oráculos cubre source 123/130=94.615% y resolver 8/8, aún sin demostrar el gate completo.
- first_divergence: exclusión publicada de source_bar.go:93 contradicha por `TestReviewerOlderClosedRegionErrorIsReachable`; calendario válido con tres miércoles holidays alcanza engine.go:408; engine.go:218 rechaza un input malformado legítimo.
- owner: evidencia/VERIFICATION del implementer, revisada independientemente.
- fix: evidencia de `407e03dd` supersede claims del candidate, que se conserva. source_bar.go129/135 bruto95.56%; serialization19/19; admission11/11; resolver8/8; preflight4/4; applySourceBar38/41 bruto y38/38 aplicable tras proof independiente de tres guards serialmente redundantes. Errores reales no excluidos.
- regression: casos permanentes older-region, holidays y malformedSource PASS; nuevo TOP ejecutó perfiles raw y audita rangos/denominadores/exclusiones en final-all.cover + coverage_audit.py. No coverage filtrado del source.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F04 — filas mutables expuestas bajo manifiesto congelado

- severity: HIGH (revisor R01/P1).
- dataset/rango: probe local independiente sobre code `933b40d6`, fila NT observada usada como REFERENCE_ONLY; corpus físico completo no adquirido.
- expected: ningún byte distinto al receipt validado puede entregarse bajo la identidad del constructor; consumidor que termina horizonte o cierra cursor antes de EOF conserva ese contrato.
- actual: tras NewSource, cambiar volume35→36 en el archivo y llamar Open/Peek entrega36 con el manifiesto anterior; ErrSourceChanged llega sólo al drenar EOF, que un consumidor corto puede no alcanzar.
- first_divergence: primera fila alterada entregada por Peek después de modificar fuente; probe TOP `reports/ntminute-ingress-review/adversarial.log`.
- owner: adapter ntminute immutable source/cursor; ROOT coordina, worker NORMAL fresco remedia.
- fix: e44b741e0a6c32d39326b46738dc70565db4759c; snapshot completo privado por cursor verificado contra receipt antes de exponer filas, backing inmutable; handles cerrados en error/Close y unlink best effort con error si OS deniega. Metadata/identity lógicos preservados.
- regression: PERMANENT_REGRESSION immutable_source_regression_test.go; TOP fresh final RED933→PASSe44 preOpen head/tail/append/truncate/missing, short horizon Close beforeEOF, dualcursor/postOpenimmutability, rawmetadata/oracle byteigual. Large tail >buffer:1500/2000 rows, RED933fila82→PASSfix. Rawadapter290/29897.315%, exclusiones0.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F05 — un archivo físico asignado dos veces mediante aliases

- severity: MEDIUM (revisor R02/P2).
- dataset/rango: probe local dos bindings de contratos físicos, paths aliases; REFERENCE_ONLY, sin rango histórico.
- expected: misma fuente física no puede vincularse a dos streams usando symlink/hardlink/alias de path; archivos distintos legítimos con bytes iguales son admisibles.
- actual: validación compara sólo strings Path; distintos aliases del mismo inode se aceptan como NQ12-23 y NQ03-24.
- first_divergence: constructor acepta dos streams y manifiesto tras resolver ambos paths al mismo archivo físico; probe TOP `reports/ntminute-ingress-review/adversarial.log`.
- owner: adapter ntminute physical-binding preflight.
- fix: e44b741e0a6c32d39326b46738dc70565db4759c; preflight SameFile de todos los bindings antes del scan/manifest; physical inode/path excluidos de identidad lógica.
- regression: PERMANENT_REGRESSION + TOP fresh final RED933→PASSe44 aliases symlink/hardlink/relative path, distinct byteequivalentfiles permitted; full adapter race/vet/NDJSON/oracle/TCR antimasking PASS.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F06 — coste cuadrático del historial de timers nativo

- severity: HIGH para viabilidad de horizonte histórico; no defecto de rentabilidad.
- dataset/rango: corpus minuto sintético completo51-H4 del worker C, REFERENCE_ONLY; ningún histórico original ejecutado. Source baseline933b40d6 con delta C todavía WIP, función nextTimer heredada sin cambiar.
- expected: scheduler nativo retiene y recorre obligaciones pendientes, coste acotado por timers activos; fulldomain smoke con calentamiento termina sin historial cuadrático.
- actual: cada minuto re-arms/replaces timers; driver conserva fired/replaced entries y nextTimer/pushTimer los recorren, O(minutes²). E2E race agota timeout600s; primer casoSL tardó≈9m, casoTP aún calentando, stack runnable nextTimer, sin deadlock/assertion failure.
- first_divergence: acumulación de timers fired tras cada re-arm; log/stack `reports/ohlc-driver/final-native-race.log`, antes del fix.
- owner: backtester native driver timer storage, no shared SDK/MM/Strategy.
- fix: C congelado e2e15a3559034a3ed08c04f247baf4919e20b2ff, stable native-only removal of Fired at nextRoot entry before any index selected; no new scheduler ni modificación legacy. Misma prueba nonrace40.48s→42.46s no demuestra speedup; storage live acotado y trace/result exactos. CPUprofileafter GC47.4%/Builder.findSource8.95%/completeNativeBar4.82%; timer scan deja de ser hotspot, atribución dominante no confirmada. No se aplicó optimización SDK/cache especulativa.
- regression: FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED — PERMANENT_REGRESSION compara48/1000min con5000fired, causal records/result/ref digests iguales y livepeak<=20; selección/generation/order/residual race PASS. Mismo fixture/flags beforeafter sin speedup. Domain cuatro long/short SL/TP ordinarios PASS, race completo pendiente.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F07 — control tardío aplicado dentro de vela expuesta no resuelta

- severity: HIGH, causal accounting/control ownership.
- dataset/rango: probe C sintético minute interval con orden protectiva working, CALLER_CONTROLLED; REFERENCE_ONLY. Source C WIP, ningún rango histórico original.
- expected: control admitido después del modeledOpen con EffectiveAt dentro de una vela expuesta/working pendiente se diagnostica OHLC_BOUNDARY_AMBIGUOUS antes de aplicar cualquier cashflow/context/settlement, usando sólo intervalbounds y timestamp/control conocidos; diagnosticAt>=caller completedfrontier.
- actual: el preflight inicial de Open desconocía un control admitido luego; rootControl aplicaba cashflowUSD1 a los30s antes del preflight en SourceClose.
- first_divergence: ledger.Cashflows0→1 al procesar control tardío, probe `TestOHLCDriver_LateAdmittedControlCannotAlterExposedInterval` del worker C y logs late-control-before/after.
- owner: native backtester root/control preflight, sin fórmulas MM/Strategy ni sharedSDK.
- fix: C congelado e2e15a3559034a3ed08c04f247baf4919e20b2ff, preflight de todos nativePending antes de seleccionar root; Coordinator clarificó horizon: control exactamente intervalEnd dentro horizonte diagnostica; control at/after EndExclusive permanece PENDING_BEYOND_HORIZON y no invalida soleterminal SourceClose, preservando S04.
- regression: FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED — PERMANENT_REGRESSION late+30s/intervalEnd dentrohorizonte, single/multistream pendingpinned; control atEndExclusive sellado pending sincashflow/ambiguity, soleterminal SourceClose consumido; diagnostic no backdate/cero mutación anteserror. Suite native rápida race31.642s PASS.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F08 — día inicial parcial colisiona con el reset de cuenta

- severity: HIGH; bloquea un horizonte válido del perfil funcional.
- dataset/rango: reproducción E2E nativa sintética independiente sobre e2e15a3559034a3ed08c04f247baf4919e20b2ff. Warmup2026-10-05T20:59Z (Chicago15:59); fuentes20:59→21:00 y22:00→22:01 respetan break16–17; TradeStart22:00:59.999999999Z/End22:01Z. REFERENCE_ONLY, sin histórico físico ejecutado.
- expected: día inicial es el intervalo account-day que contiene WarmupStart bajo reset17h; al boundary17h abrir un intervalo distinto, con economics/MM selector coherentes y sin consumir ordinal durante warmup.
- actual: openInitialAccountDay usa accountDayID(civilDate(WarmupStart)); naturalboundary17h de la misma fecha usa igual ID ad-20261005, Ledger rechaza ACCOUNT_DAY_FAILED porque ese día ya está abierto.
- first_divergence: ACCOUNT_DAY_FAILED a2026-10-05T22:00Z antes del segundo SourceClose; logs independent-fast.log del TOP revisor, source run.go684/driver.go496.
- owner: backtester composición/identidad del intervalo account-day; defecto heredado expuesto por reset17h funcional, no fórmulas SDK/accounting/MM ni Strategy.
- fix: congelado171fc712e56d731493befeef5c54a2620f25d31a; inicializa el intervalo contenedor con civilDateOf/boundaryOf/AddDate existente, conserva reset natural, WarmupStart caller e IDs naturales. Integración CLI byteexacta comprobada independientemente en198f29f4.
- regression: PERMANENT_REGRESSION + TOP independiente RED e2e15a35→PASS171fc712; mismo break nativo y legacy, antes/at/después17h, año y Chicago23/25h DST, EndExclusive/timezonefailure. Oráculos legacy UTC00/after17 result+records byteiguales (678137/678131 bytes). Race7.477s, S04/Plan/native10.509s y vet PASS aislados; coverage10/10 bruto sin exclusiones. Evidencia externa reports/native-integrated-final-review/f08-proof.json; [[BTG-S01-ACCOUNT-DAY-REMEDIATION]].
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F09 — cursor nativo sin liberar ante fallo de salida CLI

- severity: MEDIUM; ownership/cleanup del CLI.
- dataset/rango: reproducción pública sintética nativa sobre198f29f44bc6e58dd445c9a9b5ee1adfdade2ae9, REFERENCE_ONLY; source real no ejecutado.
- expected: tras NewRun exitoso, cerrar cursor poseído antes de cada return de error; conservar el primer error y Finish normal una sola vez.
- actual: cmdRun y cmdReproduce con un archivo regular bloqueando out/<RunID> retornan spool-create error pero conservan un FD adicional del snapshot ya desvinculado, observado inmediatamente con GOGC=off. No archivo privado nombrado persistente; exit del proceso/GC puede liberarlo después.
- first_divergence: error SpoolDir después de NewRun; FDs0→1 run,1→2 reproduce en reports/native-integrated-final-review/cli-f09-capsule.log. Constructor leak DISPROVED acotado: validaciones antes de Open y fallo de Open limpia el adapter.
- owner: cmd/echo-backtest executeRunSource/executeReproductionSource; no NewRun/ResultWriter/SDK cambios justificados.
- fix: fresh NORMAL codex/btg-s01-native-cli-final-remediation desde6ef303f5, SDD Root congelado; limpieza mínima de paths de error preservando artefactos exitosos.
- regression: PERMANENT_REGRESSION + TOP independiente RED198f FD0→1→2 / PASSe632 FD0→0→0, GOGCoff sólo prueba FD; close1/peek0/next0, errors.Is ENOTDIR/errors.As PathError y sentinel secundario preservados; race6.470s/F081.260s/vet/build, freshfailuresealed/repro IDENTICAL y legacy198f→e632 byteiguales. Coverage42/42 bruto/aplicable, ceroexclusiones. [[BTG-S01-NATIVE-CLI-FINAL-REMEDIATION-REVIEW]].
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F10 — preparación no declara límite de autenticidad

- severity: LOW; metadata no conforme a SPEC.
- dataset/rango: manifest preparado sintético sobre198f29f4; REFERENCE_ONLY.
- expected: Scope declara que la preparación no adjudica autenticidad de la fuente junto a NO_ADDS/horizonte caller/AvailableAt/no BBO o LIVE parity; Fidelity OHLC_1M_MODEL_V1.
- actual: Scope omite esa frontera explícita. No se infiere flag auto-REAL ni claim histórico falso.
- first_divergence: prepare_nt.go112, manifest Scope contra aclaración Coordinator de specs/btg-s01-nt-cli/SPEC.md.
- owner: CLI preparación metadata.
- fix: fresh NORMAL del mismo carril F09, una aclaración Scope sin cambiar reglas/fidelidad.
- regression: TOP independiente Scope authenticity PASS e632, Fidelity/NO_ADDS/callerhorizon/AvailableAt/BBOlimits preservados; mismo gate42/42 sin exclusiones.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F11 — segundo Close tras EOF y error de re-admisión

- severity: LOW; gate local de ownership exact-once.
- dataset/rango: dos minute records UTC sintéticos reales en el adapter, artefacto CALLER sellado válido + override --spec AUTO válido; e63254875b84b9ebe91b26ca138bb5c19843113a, REFERENCE_ONLY, sin histórico original.
- expected: un solo Close subyacente entre driver EOF/Finish y cleanup CLI; original admission-mode error preservado.
- actual: driver cierra sequenceCursor al EOF, sequenceSource retiene el wrapper y el cleanup CLI después de error de re-admisión vuelve a cerrar. Cursor native idempotente: sin fuga ni divergencia económica/error observada.
- first_divergence: pointer de ownership aún presente después de EOF; cmdReproduce reproduce el error público, seam equivalente instrumentado con DatasetSource nativo observa Close2/Peek3/Next1. Probe TestReviewerOwnershipPublicValidSealedScriptOverride/log public-readmission-eof.log, capsuleSHA74fe84bdca5709a250d9668756f8daed9e77b74b4ac70ca574076dfb896073d7.
- owner: CLI sequenceCursor/sequenceSource lifecycle run.go; no SDK/NewRun/ResultWriter cambio justificado.
- fix: source15422c2329164a33a76bf63912491168227660b7 desdee632, sequenceCursor.Close sync.Once cachea primer resultado; no otros productionfiles/API/domain changes. Docs-onlytip e320fef9 preserva F09Verification exacta.
- regression: PERMANENT_REGRESSION + freshTOP RED e632Close2/Peek3/Next1 → PASS15422 Close1/Peek3/Next1, mismo sealedscript/override/originalmodeerror. Concurrent128/sequential Closeerror cache errors.Is/As, F09publicFD []→[]→[], race8.070s/F081.171s/vet/build; shortsealedSOURCE_COVERAGE_INCOMPLETE/reproIDENTICAL y legacy e632→15422 byteigual SHAd5325ae6cf99725a9e7e23dab1951b1e8fb60468f29a41179a636f5b504c5ad7. Independent changedblocks3/3 bruto/aplicable, sinexclusiones. Evidence reports/cli-cursor-once-review.
- real_rerun: COMPLETE rawbt-b9676b4b…e4d44 + derivedbt-bd627d8a…029f, ambos freshIDENTICAL, code d69d03ec integra fix específico. Alcance/ramas reales delimitados en matriz anterior.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN; regresión específica y rerun integrado acotado, no equivalencia LIVE ni full13.

### BT2-F12 — fallo histórico reportado al caller frontier antiguo

- severity: MEDIUM; atribución temporal de evidencia real incorrecta, sin divergencia de scheduler probada.
- dataset/rango: NQ12-23 real, SHA256caead986337256d77011d58cb49d4d4b20393b1261c0f1ef4c494cd0397c6c94; warmupsOct1/Oct10 y fallosOct10/Oct13, artifacts externos de real-history-execution.
- expected: Summary.LastLogicalTime de FAILED refleja último clock alcanzado; causa de source inválido identifica ref e intervalo. La referencia de input rechazado y último prefix consumido son coordenadas diferentes.
- actual: summary queda en warmupOct1 aunque records/error gap alcanzaronOct10; nextRoot validation failure deOct13 se fecha al warmupOct10 y causa omite intervalo/ref en no-owning-session branch.
- first_divergence: Finish summary y AdvanceUntil nextRoot-error capsule usan r.frontier (caller-completed frontier) en lugar del último clock alcanzado. Mantener frontier es intencional para fases/timers: no se autoriza alterarlo per root.
- owner: backtester finish.go/driver.go; TOP LOCAL real_gap_forensics implementor, Root sólo SDD/specs/coordination.
- fix: 970f1d5238192a24aec8caca4a48d3da5b1d3280, sólo FAILED time/source attribution, no guard/calendar/Strategy/MM/risk/scheduler.
- regression: focused RED confirmado missing minute summary start vs start+2min y outside-source interval ausente; GREEN/race/vet PASS por TOP. PERMANENT_REGRESSION.
- real_rerun: source-gap bt-2b7e9fc2…d39f4 reachedOct10T00:16Z/52238records; outside-session bt-e036b4f0…6fd7 reachedOct13T20:59Z/rejected ntminute:c43f2f9c…0fab Oct15[04:32,04:33),33308records. AmbosfreshreproduceIDENTICAL, records/state/economics preservados.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN (F12 únicamente); evidencia TOP importada byteexacta desde9630c410 en BTG-S01-REAL-GAP-FORENSICS; no modifica guard ni scheduler.

### BT2-F13 — contadores de fills y operaciones reales en cero

- severity: MEDIUM.
- dataset/rango: smoke NQZ3Oct29→Nov3 real COMPLETE `bt-0049ea…ad5fb0`.
- expected: lifetime unique fills accounting y operaciones materializadas compartidas, distinguiendo filled/never-filled; no capped FIFO ni copia de historial de marks.
- actual: summary fills0/operations0 frente24unique(account,provider_execution_id),30CREATED/12con fills.
- first_divergence: Finish cuenta colección legacy sin el ciclo nativo compartido.
- owner: finish.go + SDK accounting thin read-only FillCount getter. D6 refreshsinintersección antes sharedchange.
- fix: d69d03eceeac1495522473a95baf08087f5c28b3; Ledger.FillCount O(1) sobre dedup económico permanente y sum IssuedOperationIDs; sin cambio monetario.
- regression: RED real_result_counts_test.go con2unique fills/1materialized/duplicateredelivery; ledger getter zero/qty≠count/duplicate/conflict/daycontext/revision-readonly. GREEN full-warmup86.666s, race focalizado1.151s/1.026s y vet PASS. Oráculo inicial flat⇒TERMINAL incorrecto corregido en test nuevo; race full-warmup timeout10min preservado como FAIL.
- real_rerun: rawbt-b9676b4b…e4d44 COMPLETE/136932records/24fills/30ops/−9970.70USD y freshIDENTICAL; derivedbt-bd627d8a…029f COMPLETE/270781records/78fills/113ops/−34293.32USD y freshIDENTICAL. F14 rawsinresidualterminal; derivedACTIVEflat declarado legítimo, no garantía de terminar todaslasops.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN.

### BT2-F14 — operación terminal como residual abierto

- severity: MEDIUM.
- dataset/rango: mismo COMPLETE real5accountdays;30latestoperationsTERMINAL,posición0/unrealized0.
- expected: residual working/live operation sólo si lifecycle compartido activo; account_day/stage abiertos sí se conservan.
- actual: residual fop239b… peseTERMINAL/MM_NO_ACTION Nov3T19:50Z; CurrentOperationID retenido intencional no prueba actividad.
- first_divergence: finish.residuals trata anyCurrentOperationID como abierto.
- owner: finish.go, sin modificación del actor/runtimeOperation.
- fix: d69d03ec; consulta status canónico para residual, excluye sólo TERMINAL, conserva nil/ACTIVE; sin borrar IDs ni mutar lifecycle.
- regression: RED terminal residual y caso materializado no-fill working conserva residual; GREEN full-warmup86.666s, race focalizado1.151s/1.026s y vet PASS. Oráculo inicial flat⇒TERMINAL incorrecto corregido en test nuevo; race full-warmup timeout10min preservado como FAIL.
- real_rerun: rawbt-b9676b4b…e4d44 COMPLETE/136932records/24fills/30ops/−9970.70USD y freshIDENTICAL; derivedbt-bd627d8a…029f COMPLETE/270781records/78fills/113ops/−34293.32USD y freshIDENTICAL. F14 rawsinresidualterminal; derivedACTIVEflat declarado legítimo, no garantía de terminar todaslasops.
- state: FIXED_WITH_REGRESSION_AND_REAL_RERUN.

### Retención y clasificación

Reproductores y logs del revisor viven fuera del vault en el carril Aranea `work/btg-s01-20261006/source-bar-review-evidence/`; sus digests/manifest quedan en el artifact del revisor. Golden legacy bytes y casos de atomicidad/orden/calendario que detectaron estos defectos son PERMANENT_REGRESSION candidates, sin framework nuevo. Probes usados sólo para auditoría comparativa o coverage son DISPOSABLE_REPRODUCER hasta clasificación final. Los reproductores sintéticos conservan su clase y no sustituyen los reruns históricos ahora identificados. Findings F01–F14 cerrados por regresión+rerun acotado; no gate Owner ni cobertura full13.

## Fuentes

[[BTG-S01-SOURCE-BAR-SDK-IMPLEMENTATION]], [[BTG-S01-SOURCE-BAR-SDK-REVIEW]], [[BTG-S01-SOURCE-BAR-SDK-REMEDIATION]], [[BTG-S01-SOURCE-BAR-SDK-FINAL-REVIEW]], [[BTG-S01-S2-1M-FORENSICS]], SDD producto `specs/btg-s01-source-bars/` y `specs/btg-s01-source-bars-remediation/`. Root recibió los findings confirmados del revisor y conserva continuidad hasta resolverlos con regresión y el histórico autorizado.
