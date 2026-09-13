---
type: feedback
schema_version: 1
scope: session
created: 2026-09-13
updated: 2026-09-13
area: "[[Echo]]"
project: "[[Echo — E-01 Canonical SDK Foundation S0]]"
entities:
  - "[[Echo]]"
related:
  - "[[Echo — E-05 Analytics Convergence A0]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: builtin:zai-coding-plan/GLM-5.3
agent_run: "[[2026-09-13-zcode-glms0-erratum-verifier]]"
session_goal: "Verificación independiente one-shot del erratum S0 V3-006."
source_session: 2026-09-13-echo-s0-erratum-independent-verification
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-09-13 - S0 erratum independent verification (V3-006)

## Context

- Agent surface: `[[ZCode]]`; model `builtin:zai-coding-plan/GLM-5.3` (host).
- Agent run: `[[2026-09-13-zcode-glms0-erratum-verifier]]`.
- Session goal: Independent Verifier one-shot del erratum S0; evidencia y cierre sin integración.
- Main entity: `[[Echo — E-01 Canonical SDK Foundation S0]]`.
- Skills used: Agents OS bootstrap, aranea-agent-dev router, agent-run register; sdd-workflow fase verification como marco.
- Retrieval mode: focused (notas E-01/E-05, SPEC/VERIFICATION, source S0); cero scans amplios.
- Artifacts changed: `VERIFICATION.md` del repo (sólo evidencia), notas E-01/E-05, run/log/feedback del vault.

## Hallazgos de proceso (pedidos por el mandato de verificación)

- **Por qué el corpus S0 original no detectó versiones/digests distintos:** G01–G36 son fixtures de conjuntos *válidos bajo el tuple truncado*: ninguno contiene dos métricas que empaten en `key+basis+formula.id` y difieran en `formula.version`/`definition_digest`, porque el validator certificado rechazaba exactamente esa forma. El corpus valida comportamiento observable de casos existentes; no explora el espacio de sets que la implementación rechazaba erróneamente (negative space). Un gap estructural de todo corpus golden: certifica lo que existe, no lo que debió existir.
- **Calidad del BWC proof del implementor:** correcta pero de un solo fixture golden (ref/digest/bytes hardcoded de `testMetricSet`). El verificador la extendió a 21 casos (17 derivados de corpus + 4 construidos) calculando cada lado con binarios de su respectivo commit, cerrando el riesgo de un "before" recalculado con el fix. Recomendación: mantener el golden in-repo de un caso y documentar el método dual-binario como patrón para futuros errata.
- **¿La regresión debe quedar permanente?:** sí. `TestMetricSetFormulaIdentityErratum` y `TestSortMetricsUsesFrozenIdentityOrder` codifican invariantes del contrato frozen (FR-2), no detalles del fix; eliminarlas reabre la puerta al mismo truncamiento. El test de identidad por campo (`TestMetricIdentityUsesAllFrozenFields`) es la barrera más barata contra futuros campos descartados; conviene replicar ese patrón si algún día se agrega una séptima dimensión al contrato (lo que hoy está prohibido).
- **Fragilidad del comparator/identity:** baja tras el fix. La primitive compartida elimina la divergencia validator/canonicalizer, y el orden lexicográfico de strings es total y estable. Fragilidad residual: (a) `unit` en la identidad es redundante con el catálogo para sets válidos, así que un futuro catálogo con dos units por `(key,basis)` cambiaría silenciosamente qué sets son distintos; (b) `compare` opera sobre strings crudos sin normalización — correcto por contrato, pero dependiente de que nadie "semantice" versiones (p.ej. `1` vs `01` son legítimamente distintas).
- **¿El erratum fue realmente implementation-only?:** sí, verificado por tres vías: `SPEC.md` diff 0 en el delta; la semántica de seis campos ya estaba en FR-2 (`FORMULA = {id, version, definition_digest}` + métrica `key+basis+unit+formula`, prohibición de duplicar `(key, basis, formula)`); y el BWC demuestra que ningún observable de sets previamente válidos cambió. Los únicos textos que cambiaron son comentarios/doc y el mensaje de error de duplicados exactos (inputs ya inválidos bajo el pin).

## Fricción / mejoras

- El mandato de verificación es largo y parcialmente redundante (gates repetidos entre secciones); una checklist de gates únicos con referencias reduciría el costo de sesión sin perder cobertura.
- El patrón dual-binario (módulo externo con `replace` a pin y target) debería ser una skill/runbook reutilizable de verificación de contratos; se reimplementó desde cero esta sesión.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Workflow clarity: 5
- Bootstrap/retrieval: 5
- Tooling friction: 4
- Overall: 5
