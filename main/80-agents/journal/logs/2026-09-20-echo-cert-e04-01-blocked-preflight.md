# change_log 2026-09-20 — CERT-E04-01 preflight BLOCKED (Echo T21)

## Contexto

Misión NORMAL CERT-E04-01 (Echo cross-lane golden / T21 / AC-37) con autonomía acotada. Ejecutó G0 (brecha de bytes del golden F04-02) y G2 (preflight runtime Echo) con verificaciones read-only; G3–G7 NO_RUN; veredicto fail-closed sin POST.

## Cambios

- `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md`: delta nuevo «Delta de preflight y bloqueo CERT-E04-01 — 2026-09-20» (G0 `GOLDEN_MANIFEST_BYTES_BLOCKED`, G2 `ECHO_RUNTIME_BLOCKED`, G8 `CERT_E04_01_BLOCKED`, owner actions 1–2) + intento anotado en la entrada CERT-E04-01 del backlog.
- `10-projects/Echo/agentes/Echo — E-04 Forge Ingestion E1.md`: bullet nuevo de estado (T21 preflight BLOCKED 2026-09-20) + bitácora 2026-09-20 + frontmatter `updated`.
- `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-cert-e04-01-blocked-preflight.md`: nuevo (outcome: blocked, verificación executed_suite).
- Workdir externo (fuera del vault): `~/aranea/work/cert-e04-01/` con `owner-action-01-sqx-ro-trading-systems-test.md`, `owner-action-02-echo-e04-runtime-deployment.md`, `PREFLIGHT-EVIDENCE.md`.

## No cambió

- Código de `xKoRx/echo` y `xKoRx/symphony`, contratos frozen, migrations, SPEC E-04, corpus golden (`~/aranea/work/f04-cert-f04-02/corpus` intacto y re-validado PASS), ETCD, IAM, despliegues; estados de CERT-F04-01/F04-02/F04-03/F05-*.

## Evidencia

`~/aranea/work/cert-e04-01/PREFLIGHT-EVIDENCE.md` (probes, SQL, ETCD, ancestry) + agent-run del mismo nombre.
