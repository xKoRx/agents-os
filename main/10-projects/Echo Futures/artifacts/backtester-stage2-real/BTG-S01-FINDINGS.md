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

### Retención y clasificación

Reproductores y logs del revisor viven fuera del vault en el carril Aranea `work/btg-s01-20261006/source-bar-review-evidence/`; sus digests/manifest quedan en el artifact del revisor. Golden legacy bytes y casos de atomicidad/orden/calendario que detectaron estos defectos son PERMANENT_REGRESSION candidates, sin framework nuevo. Probes usados sólo para auditoría comparativa o coverage son DISPOSABLE_REPRODUCER hasta clasificación final. No se afirma un rerun real ni el cierre de findings.

## Fuentes

[[BTG-S01-SOURCE-BAR-SDK-IMPLEMENTATION]], [[BTG-S01-SOURCE-BAR-SDK-REVIEW]], [[BTG-S01-SOURCE-BAR-SDK-REMEDIATION]], [[BTG-S01-SOURCE-BAR-SDK-FINAL-REVIEW]], [[BTG-S01-S2-1M-FORENSICS]], SDD producto `specs/btg-s01-source-bars/` y `specs/btg-s01-source-bars-remediation/`. Root recibió los findings confirmados del revisor y conserva continuidad hasta resolverlos con regresión y el histórico autorizado.
