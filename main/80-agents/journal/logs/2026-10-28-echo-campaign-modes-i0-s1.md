# Change Log — 2026-10-28 — Echo campañas I0-S1 (implementación del reporting económico)

## Motivo

Ejecutar el despacho I0-S1 confirmado por el Owner sobre el paquete [[EF-CAMPAIGN-MODES-I0-LOCAL]] (C04): entregar el candidato de contrato/reporting económico opt-in y la reconciliación focal S04-F01/F02, sin campañas ni cambios de runtime, como paso previo a la verificación adversarial I0-S2.

## Fuentes usadas

- Mandato completo I0-S1 y estado vigente C04 en [[EF-CAMPAIGN-MODES-I0-LOCAL]]; planner único [[Echo Futures — Optimización de Campañas]] (bloque vigente, no escrito por este worker).
- [[EF-CAMPAIGN-MODES-DESIGN]] C04 (§§4.2, 5–7, 8, 14.1–14.4, 17) y [[EF-S04-INTEGRATION-RECONCILIATION]] (hallazgos F01/F02, evidencias A–D).
- Código real `xKoRx/echo@2baf319d` (read-only): `platform_campaign.go`/`platform_research.go` (cash events, payments, researchCharge/tickPayment), `research_lab.py`, reglas SDD 08/09, FEAT-CHALLENGE-HISTORY.
- Planes efectivos sellados en Hefesto: `~/echo-work/runs/challenge-history-20261018-{r4,r5,hefesto}/plans/`, `R01-HIST-20261021/lab/LAB-NATIVE-*`, artefacto E2E `R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750`.

## Resolución aplicada

- Rama `feature/ef-campaign-modes-i0` creada desde `2baf319d` en worktree propio (`echo-i0`); candidato `b964e13d` (implementación `a324fda9`), push con readback `origin == HEAD`. Sin merges/resets; trabajo ajeno intacto.
- CREATE módulo puro `economics_report.py` + 34 tests; MODIFY mínimo de `research_lab.py` (subcomando opt-in `economics`); SDD del change bajo `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-*` (SPEC/PLAN/TASKS/VERIFICATION del slice, sin segunda SPEC contradictoria).
- S04-F01 → DEMONSTRATED_AT_PLAN_LEVEL con censo de planes sellados (r4 52/52, r5 15/15, hefesto 5/5, R01 26/26, todos V1; SG desparejadas): refuta «policy vacío»; equivalencia de intérprete abierta; fixture Go registrado fuera de alcance I0.
- S04-F02 → CONFIRMED (guard ausente; seam `_run_one`/`resume --execute` declarado, no portado).
- Retorno canónico create: [[EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN]]; agent-run: `80-agents/journal/agent-runs/2026-10-28-zcode-glm-5.3-flash-echo-campaign-modes-i0-s1.md`.

## Validación

- Tests de contrato 34/34; suites del lab 124/124 sin regresión; coverage del módulo nuevo 99,8% (sys.settrace, piso 95).
- E2E real doble corrida byte-idéntica con conciliación (residual 0 USD; cost_per_pass 804 USD == declarado; q NOT_OBSERVED); inputs sellados byte-intactos por sha256; sentinel no-spawn/egress PASS.
- Sin ejecución de I0-S2/S3/GOD-COMPOSITION, sin suites Go, sin campañas/compras/trading/deploy; PROD congelado; umbral 1/3 THRESHOLD_NOT_ADJUDICATED.

## Compartibilidad

- Scope: local (Hefesto) + push de la rama de candidato a origin (`xKoRx/echo`) con readback.
- Sin secretos; importes citados pertenecen a receipts ya sellados del proyecto.

## Rollback

- Producto: revertir sólo los commits de `feature/ef-campaign-modes-i0` (`a324fda9`, `b964e13d`); ninguna otra rama afectada; dejar de consumir el reporte opt-in.
- Vault: revertir este delta documental con nuevo commit reconciliado sobre master, sin reset ni force.

## Continuidad

- Siguiente paso: I0-S2 (TOP LOCAL fresco, ≤90 min) sobre el SHA candidato exacto `b964e13d`, retorno `EF-CAMPAIGN-MODES-I0-VERIFY-RETURN.md`; luego adjudicación del manager y, si corresponde, I0-S3.
- Aceptación semántica S04 sigue ABIERTA; F01 resuelto a nivel de planes efectivos, fixture de frontera Go pendiente de adjudicación; PRO_CHAT_POOL_DELTA UNKNOWN.
- Este worker queda CERRADO; el manager de Optimización de Campañas y el programa Echo Futures permanecen abiertos.
