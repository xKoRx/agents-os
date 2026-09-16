# change_log 2026-09-16 — E-02 physical certification + Access Plane P1

Sesión Ariadna (Hermes, TUI). Objetivo del owner: ejecutar y cerrar los physical gates E-02 con capabilities ya certificadas; sin PROD mutation, sin MT4/MT5, sin GAP-ECHO-005.

## Resultado

`E02_PHYSICAL_CERTIFICATION_PASS` — 3/3 gates físicos PASS (Hasura DEV roles/hook, Kafka PublishSync/redelivery, Flink restart/recovery). E-02 NO se declara CLOSED (falta AC-11 outage PG real, AC-12 kill -9 del binario core Go, AC-01 bundle, verifier independiente).

## Cambios de estado (Sistema 2)

1. `10-projects/Echo/agentes/Echo — E-02 Control Safety, Auth and Journal Recovery.md` — bitácora 2026-09-16 con los 3 gates, clasificación KEEP/REMOVE, deuda y residuales.
2. `10-projects/Echo/agentes/Echo — Access & Physical Capability Matrix.md` — gates E-02 Hasura/Kafka/Flink → PASS con evidencia; E-02 result → PASS con residuales; E-05 T19 → parcialmente resuelto.
3. `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/ACCESS-CERTIFICATION.md` — run 2026-09-16 + GAP-ECHO-010 (P1, defecto async-202 en proxies; workaround = restart backend proxy; NO era el quirk pool-64 en el caso ssh-mcp).

## Cambios de infraestructura (todos DEV, con rollback verificado)

- Hasura DEV (.75): metadata roles `readonly`/`config_operator` aplicados (estado contractual KEEP, AC-05); 44 permisos `admin` legacy inconsistentes excluidos; compose del stack 2 restaurado byte-identical tras fixture de hook (backup `/tmp/docker-compose.yml.pre-e02hook`); fila fixture `e02cert-8795936d9a51` DELETE 1. Drift check PASS (0 roles legacy reales, consistency OK, 0 fixture rows).
- Kafka DEV (.44): topics fixture `e02cert-gate2-*` creados/destruidos (post-condición: 0 particiones).
- Flink DEV (.75): `docker restart statefun-worker` (control mínimo para recovery); job RUNNING, `restored=1`; master untouched.
- mcps: `docker restart hasura-mcp-dev-admin` ×2 y `docker restart ssh-mcp` ×1 (recovery del defecto async-202; workaround certificado).
- Daedalus: fixture gateway E-02 @ `f7ddea18` compilado/corrido y luego eliminado con todo el toolchain/tokens/scripts (`/home/hermes-ops/e02-fixture`, `/tmp/etcdread`, `/tmp/e02-*`).

## Credenciales

- Tokens fixture (4×48-hex, openssl rand server-side) creados, usados por file-ref y BORRADOS; 0 valores en vault/DB/history (verificado por patrón de valor; 89 refs = nombres/paths en transcript).
- Bearers MCP siempre por stdin entre hosts; nunca argv/env/file/vault.

## Hallazgos

- GAP-ECHO-010 (P1, Access Plane): proxies nginx-wrapped → modo async-202 sin sid tras churn; workaround = restart backend proxy; causa raíz pendiente.
- Runtime Hasura DEV sin roles/hook E-02 antes de esta sesión (defecto D-04 vivo en runtime hasta el apply de hoy).
- Helper único de sesión (`e02-hermes-mcp.py`) reemplaza el patrón de scripts one-shot por probe (regla reusable registrada).

## Follow-ups

1. AC-11/AC-12/AC-01 restantes + verifier independiente → E-02 DONE (lanes futuros).
2. GAP-ECHO-010: diagnóstico durable del pool/leak de sesiones en mcp-proxy (P1 Access Plane).
3. Hook `HASURA_GRAPHQL_AUTH_HOOK` + headers de webhooks = steps del deploy real del Gateway E-02 (PLAN §3).

No se tocó: PROD, trading, MT4/MT5, etcd, firewall, branches ajenas, master.
