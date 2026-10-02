# Change Log — 2026-10-02 — D6 Shot 2 adversarial review (REMEDIATION_REQUIRED)

- **Fecha:** 2026-10-02
- **Entidad:** [[Echo Futures]]
- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/d6-shot2-20261002/D6-SHOT2-ADVERSARIAL-REVIEW.md` (nuevo: artefacto canónico del review adversarial Shot 2 — matriz A–Q, findings F-S2-01..10, evidencia, handoff)
  - `10-projects/Echo Futures/Echo Futures.md` (nueva entrada de bitácora D6 Shot 2 + estado del proyecto actualizado)

## Motivo

- Encargo Shot 2 del plan D6: review adversarial independiente (fresh context, one-shot, read-only) del candidato Shot 1 `0e9741a56afe6911e52480fb9f2fe86a47aae427` antes de permitir Shot 3.

## Resolución aplicada

- `D6_SHOT2_ADVERSARIAL = REMEDIATION_REQUIRED` — 0 BLOCKER / 2 HIGH / 8 MEDIUM. Sin cambios de código, sin mutaciones de ETCD/deployment/configs; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`.
- Pasan los frentes críticos (wrong-account, double-submit, M1/M2, STOP_MARKET, reconciliation, GAU50 rules con ==30% ⇒ BREACHED verificado contra fuente, egress STRUCTURALLY_DISABLED 4 barreras, coverage reproducido 98.4% ajustado). HIGH: seq-rewind del AddOn ejecución staged en reconnect (lane muerto fail-closed) y feed muerto-silencioso que queda FRESH congelado (liveness off). MEDIUM incluye binding ETCD real `day-boundary-tz=America/New_York` (16:00 CT vs 5pm CT del programa).

## Validación

- HEAD y FF range verificados; suites `-race` reproducidas (bridge 13 pkgs exit 0; sdk/core vía reproducción de cobertura del frente N con 0 FAIL); cobertura changed-logic reproducida independientemente (raw 94.0% / ajustado 98.4% ≥ 95%); ETCD leído por existencia exacta de claves (gotcha fuzzy del MCP neutralizado).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de secretos, memoria interna ni credenciales.

## Rollback

- Revert de la entrada de bitácora en el project note y borrado del artefacto `d6-shot2-20261002/`; el candidato Shot 1 y su estado no dependen del review.
