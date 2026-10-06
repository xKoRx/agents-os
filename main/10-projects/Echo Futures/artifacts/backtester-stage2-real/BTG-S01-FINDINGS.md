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

Candidate producto `27cb4ceaf62151a042494022cad08e47672a06f2`, baseline certificado `cd451972b242c8933321e03001decd4b6d778c61`. Revisor TOP LOCAL `gpt-6.1-sol` independiente. Corpus real NOT_ACQUIRED; todos los rangos siguientes son N/A para histórico real, y los probes son REFERENCE_ONLY. Remediación NORMAL fresh-context `407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef` en `codex/btg-s01-source-bars-remediation`, preservando el candidate anterior; nuevo TOP independiente confirma el gate SDK en [[BTG-S01-SOURCE-BAR-SDK-FINAL-REVIEW]]. Ningún finding cumple todavía el cierre histórico frozen.

### BT2-F01 — serialización legacy modificada

- severity: MEDIUM.
- dataset/rango: traza TRADE local idéntica sobre baseline y candidate; SYNTHETIC_REFERENCE_ONLY, sin rango NQ histórico.
- expected: bytes JSON de BarRecord, Builder y OwnerState TRADE y Version legacy iguales al contrato previo.
- actual: BarRecord JSON/Version BYTE_EQUAL; Builder añade `input_mode:"TRADE"`; OwnerState añade `Builders/5m/input_mode:"TRADE"`. Al retirar sólo ese campo hay igualdad estructural, que no sustituye la igualdad de bytes exigida.
- first_divergence: serialización del primer Builder TRADE, candidate `27cb4cea`; `TestReviewerLegacyBytes` y `TestReviewerLegacyOwnerBytes` frente a `cd451972`.
- owner: SDK bars/mode serialization; raíz coordina, NORMAL implementa en carril correctivo.
- fix: `407e03dd`; Marshal omite sólo modo TRADE redundante, restore recupera evidencia durable; OHLC modo/high-water explícitos. Once salidas legacy BYTE_EQUAL contra fresh baseline.
- regression: golden hashes independientes en source_serialization_test.go; oráculos fresh de once estados/fronteras y restore eviction/discard PASS. PERMANENT_REGRESSION en producto, probes externos retenidos.
- real_rerun: NOT_RUN, corpus no adquirido.
- state: OPEN_REAL_RERUN_REQUIRED; FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED. Esto no es un cierre permitido por el mandato.

### BT2-F02 — rechazo de modo tras mutación parcial

- severity: HIGH.
- dataset/rango: probe local con builder 1m vacío, 5m OHLC y TRADE canónico válido; SYNTHETIC_REFERENCE_ONLY, sin rango NQ histórico.
- expected: SOURCE_MODE_CONFLICT antes de admission/guard/efectos o mutación de cualquier builder.
- actual: rechazo en 5m después de tres efectos, apertura 1m TRADE, OwnerInputSeq 1→2 y Guard.LastAppliedSeq 0→1; retry consume un guard ya avanzado.
- first_divergence: `Engine.applyCanonicalEvent` admite/aplica guard y primer builder antes de verificar el modo de todos; `TestReviewerCanonicalMixedModePreflightAtomic` sobre `27cb4cea`.
- owner: SDK analytics preflight del nuevo modo, sin refactor de validación canónica legacy.
- fix: `407e03dd`; preflight de modo de todos los builders antes de admission/guard/grid/aggregation.
- regression: source_contract_regression_test.go y oracle independiente PASS; cero efectos y estado/owner_seq/guard inalterados. TOP nuevo verifica también hidden mode, hot discard y fence inverso.
- real_rerun: NOT_RUN, corpus no adquirido.
- state: OPEN_REAL_RERUN_REQUIRED; FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED. Esto no es un cierre permitido por el mandato.

### BT2-F03 — gate de cobertura no demostrado

- severity: MEDIUM.
- dataset/rango: perfiles y probes unitarios offline del candidate; SYNTHETIC_REFERENCE_ONLY, sin rango NQ histórico.
- expected: >=95% de lógica nueva aplicable, rangos/denominadores explícitos y exclusiones de ramas realmente inalcanzables demostradas.
- actual: source_bar.go bruto 122/130=93.846%; applySourceBar puro 37/41=90.244%; resolver 7/8=87.5%. La cifra 47/52 publicada puede agregar once statements de admission y no se trata como error aritmético sin delimitar el rango. El guard de región antigua, el error de resolver con tres holidays y el rechazo de SourceBar malformado son alcanzables; no justifican declarar 100% aplicable excluyéndolos. La unión con oráculos cubre source 123/130=94.615% y resolver 8/8, aún sin demostrar el gate completo.
- first_divergence: exclusión publicada de source_bar.go:93 contradicha por `TestReviewerOlderClosedRegionErrorIsReachable`; calendario válido con tres miércoles holidays alcanza engine.go:408; engine.go:218 rechaza un input malformado legítimo.
- owner: evidencia/VERIFICATION del implementer, revisada independientemente.
- fix: evidencia de `407e03dd` supersede claims del candidate, que se conserva. source_bar.go129/135 bruto95.56%; serialization19/19; admission11/11; resolver8/8; preflight4/4; applySourceBar38/41 bruto y38/38 aplicable tras proof independiente de tres guards serialmente redundantes. Errores reales no excluidos.
- regression: casos permanentes older-region, holidays y malformedSource PASS; nuevo TOP ejecutó perfiles raw y audita rangos/denominadores/exclusiones en final-all.cover + coverage_audit.py. No coverage filtrado del source.
- real_rerun: NOT_RUN, corpus no adquirido.
- state: OPEN_REAL_RERUN_REQUIRED; FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED. Esto no es un cierre permitido por el mandato.

### BT2-F04 — filas mutables expuestas bajo manifiesto congelado

- severity: HIGH (revisor R01/P1).
- dataset/rango: probe local independiente sobre code `933b40d6`, fila NT observada usada como REFERENCE_ONLY; corpus físico completo no adquirido.
- expected: ningún byte distinto al receipt validado puede entregarse bajo la identidad del constructor; consumidor que termina horizonte o cierra cursor antes de EOF conserva ese contrato.
- actual: tras NewSource, cambiar volume35→36 en el archivo y llamar Open/Peek entrega36 con el manifiesto anterior; ErrSourceChanged llega sólo al drenar EOF, que un consumidor corto puede no alcanzar.
- first_divergence: primera fila alterada entregada por Peek después de modificar fuente; probe TOP `reports/ntminute-ingress-review/adversarial.log`.
- owner: adapter ntminute immutable source/cursor; ROOT coordina, worker NORMAL fresco remedia.
- fix: e44b741e0a6c32d39326b46738dc70565db4759c; snapshot completo privado por cursor verificado contra receipt antes de exponer filas, backing inmutable; handles cerrados en error/Close y unlink best effort con error si OS deniega. Metadata/identity lógicos preservados.
- regression: PERMANENT_REGRESSION immutable_source_regression_test.go; TOP fresh final RED933→PASSe44 preOpen head/tail/append/truncate/missing, short horizon Close beforeEOF, dualcursor/postOpenimmutability, rawmetadata/oracle byteigual. Large tail >buffer:1500/2000 rows, RED933fila82→PASSfix. Rawadapter290/29897.315%, exclusiones0.
- real_rerun: NOT_RUN; transferencia completa pendiente.
- state: OPEN_REAL_RERUN_REQUIRED; FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED. No cierre histórico.

### BT2-F05 — un archivo físico asignado dos veces mediante aliases

- severity: MEDIUM (revisor R02/P2).
- dataset/rango: probe local dos bindings de contratos físicos, paths aliases; REFERENCE_ONLY, sin rango histórico.
- expected: misma fuente física no puede vincularse a dos streams usando symlink/hardlink/alias de path; archivos distintos legítimos con bytes iguales son admisibles.
- actual: validación compara sólo strings Path; distintos aliases del mismo inode se aceptan como NQ12-23 y NQ03-24.
- first_divergence: constructor acepta dos streams y manifiesto tras resolver ambos paths al mismo archivo físico; probe TOP `reports/ntminute-ingress-review/adversarial.log`.
- owner: adapter ntminute physical-binding preflight.
- fix: e44b741e0a6c32d39326b46738dc70565db4759c; preflight SameFile de todos los bindings antes del scan/manifest; physical inode/path excluidos de identidad lógica.
- regression: PERMANENT_REGRESSION + TOP fresh final RED933→PASSe44 aliases symlink/hardlink/relative path, distinct byteequivalentfiles permitted; full adapter race/vet/NDJSON/oracle/TCR antimasking PASS.
- real_rerun: NOT_RUN; transferencia completa pendiente.
- state: OPEN_REAL_RERUN_REQUIRED; FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED. No cierre histórico.

### BT2-F06 — coste cuadrático del historial de timers nativo

- severity: HIGH para viabilidad de horizonte histórico; no defecto de rentabilidad.
- dataset/rango: corpus minuto sintético completo51-H4 del worker C, REFERENCE_ONLY; ningún histórico original ejecutado. Source baseline933b40d6 con delta C todavía WIP, función nextTimer heredada sin cambiar.
- expected: scheduler nativo retiene y recorre obligaciones pendientes, coste acotado por timers activos; fulldomain smoke con calentamiento termina sin historial cuadrático.
- actual: cada minuto re-arms/replaces timers; driver conserva fired/replaced entries y nextTimer/pushTimer los recorren, O(minutes²). E2E race agota timeout600s; primer casoSL tardó≈9m, casoTP aún calentando, stack runnable nextTimer, sin deadlock/assertion failure.
- first_divergence: acumulación de timers fired tras cada re-arm; log/stack `reports/ohlc-driver/final-native-race.log`, antes del fix.
- owner: backtester native driver timer storage, no shared SDK/MM/Strategy.
- fix: C congelado e2e15a3559034a3ed08c04f247baf4919e20b2ff, stable native-only removal of Fired at nextRoot entry before any index selected; no new scheduler ni modificación legacy. Misma prueba nonrace40.48s→42.46s no demuestra speedup; storage live acotado y trace/result exactos. CPUprofileafter GC47.4%/Builder.findSource8.95%/completeNativeBar4.82%; timer scan deja de ser hotspot, atribución dominante no confirmada. No se aplicó optimización SDK/cache especulativa.
- regression: IMPLEMENTER_VERIFIED, INDEPENDENT_REVIEW_PENDING — PERMANENT_REGRESSION compara48/1000min con5000fired, causal records/result/ref digests iguales y livepeak<=20; selección/generation/order/residual race PASS. Mismo fixture/flags beforeafter sin speedup. Domain cuatro long/short SL/TP ordinarios PASS, race completo pendiente.
- real_rerun: NOT_RUN; corpus físico completo pendiente.
- state: OPEN_REPRODUCED_REMEDIATION_IN_PROGRESS.

### BT2-F07 — control tardío aplicado dentro de vela expuesta no resuelta

- severity: HIGH, causal accounting/control ownership.
- dataset/rango: probe C sintético minute interval con orden protectiva working, CALLER_CONTROLLED; REFERENCE_ONLY. Source C WIP, ningún rango histórico original.
- expected: control admitido después del modeledOpen con EffectiveAt dentro de una vela expuesta/working pendiente se diagnostica OHLC_BOUNDARY_AMBIGUOUS antes de aplicar cualquier cashflow/context/settlement, usando sólo intervalbounds y timestamp/control conocidos; diagnosticAt>=caller completedfrontier.
- actual: el preflight inicial de Open desconocía un control admitido luego; rootControl aplicaba cashflowUSD1 a los30s antes del preflight en SourceClose.
- first_divergence: ledger.Cashflows0→1 al procesar control tardío, probe `TestOHLCDriver_LateAdmittedControlCannotAlterExposedInterval` del worker C y logs late-control-before/after.
- owner: native backtester root/control preflight, sin fórmulas MM/Strategy ni sharedSDK.
- fix: C congelado e2e15a3559034a3ed08c04f247baf4919e20b2ff, preflight de todos nativePending antes de seleccionar root; Coordinator clarificó horizon: control exactamente intervalEnd dentro horizonte diagnostica; control at/after EndExclusive permanece PENDING_BEYOND_HORIZON y no invalida soleterminal SourceClose, preservando S04.
- regression: IMPLEMENTER_VERIFIED, INDEPENDENT_REVIEW_PENDING — PERMANENT_REGRESSION late+30s/intervalEnd dentrohorizonte, single/multistream pendingpinned; control atEndExclusive sellado pending sincashflow/ambiguity, soleterminal SourceClose consumido; diagnostic no backdate/cero mutación anteserror. Suite native rápida race31.642s PASS.
- real_rerun: NOT_RUN; corpus físico completo pendiente.
- state: OPEN_REPRODUCED_REMEDIATION_IN_PROGRESS.

### BT2-F08 — día inicial parcial colisiona con el reset de cuenta

- severity: HIGH; bloquea un horizonte válido del perfil funcional.
- dataset/rango: reproducción E2E nativa sintética independiente sobre e2e15a3559034a3ed08c04f247baf4919e20b2ff. Warmup2026-10-05T20:59Z (Chicago15:59); fuentes20:59→21:00 y22:00→22:01 respetan break16–17; TradeStart22:00:59.999999999Z/End22:01Z. REFERENCE_ONLY, sin histórico físico ejecutado.
- expected: día inicial es el intervalo account-day que contiene WarmupStart bajo reset17h; al boundary17h abrir un intervalo distinto, con economics/MM selector coherentes y sin consumir ordinal durante warmup.
- actual: openInitialAccountDay usa accountDayID(civilDate(WarmupStart)); naturalboundary17h de la misma fecha usa igual ID ad-20261005, Ledger rechaza ACCOUNT_DAY_FAILED porque ese día ya está abierto.
- first_divergence: ACCOUNT_DAY_FAILED a2026-10-05T22:00Z antes del segundo SourceClose; logs independent-fast.log del TOP revisor, source run.go684/driver.go496.
- owner: backtester composición/identidad del intervalo account-day; defecto heredado expuesto por reset17h funcional, no fórmulas SDK/accounting/MM ni Strategy.
- fix: PENDING_FRESH_WORKER; reuse existing civil calendar boundary semantics from experiment_plan.go, preserve valid legacy UTC00 and naturalboundary behavior. No modificar horarios caller ni inventar IDs de otro día para esconder error.
- regression: PENDING_PERMANENT_REGRESSION; antes/después reset17h, partial-first-day/year/DST y misma reproducción break; ledger snapshots/selector/ordinal, no fictitious trades during warmup; explicit valid legacy oracles.
- real_rerun: NOT_RUN; transferencia completa pendiente.
- state: OPEN_REPRODUCED_REMEDIATION_PENDING.

### Retención y clasificación

Reproductores y logs del revisor viven fuera del vault en el carril Aranea `work/btg-s01-20261006/source-bar-review-evidence/`; sus digests/manifest quedan en el artifact del revisor. Golden legacy bytes y casos de atomicidad/orden/calendario que detectaron estos defectos son PERMANENT_REGRESSION candidates, sin framework nuevo. Probes usados sólo para auditoría comparativa o coverage son DISPOSABLE_REPRODUCER hasta clasificación final. No se afirma un rerun real ni el cierre de findings.

## Fuentes

[[BTG-S01-SOURCE-BAR-SDK-IMPLEMENTATION]], [[BTG-S01-SOURCE-BAR-SDK-REVIEW]], [[BTG-S01-SOURCE-BAR-SDK-REMEDIATION]], [[BTG-S01-SOURCE-BAR-SDK-FINAL-REVIEW]], [[BTG-S01-S2-1M-FORENSICS]], SDD producto `specs/btg-s01-source-bars/` y `specs/btg-s01-source-bars-remediation/`. Root recibió los findings confirmados del revisor y conserva continuidad hasta resolverlos con regresión y el histórico autorizado.
