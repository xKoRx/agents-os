---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P0
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
created: "2026-09-21"
updated: "2026-09-21"
tags:
  - kind/project
  - area/echo
---

# Echo — Branch Consolidation 2026-09-21

## Mandato vigente del owner

**Prioridad antes de cualquier cobertura E-08/E-09, E-10 o nueva implementación:** reducir xKoRx/echo a `master` como línea estable y **una sola `feature/*` de desarrollo activa**. No perder commits, no forzar pushes, no confundir `SOURCE_VERIFIED` con release/physical; no integrar features inmaduras a master para simplemente borrar ramas. Este documento es plan/ownership, NO un informe de limpieza ejecutada. Owner del trabajo: manager Echo, agente TOP de integración; demás agentes congelan sus ramas hasta cierre.

## Inventario remoto observado (GitHub, 2026-09-21)

`master = 5dd998f16aea7b2821f460188718d7a6d279829c`; 16 ramas totales, 15 adicionales; cero PR abiertas en la consulta.

- Ancestros exactos de master, **ahead=0**: `feature/deprecated-sl-offset@02fa35d8`, `feature/e02-control-safety-journal-recovery@92d0ec2e`, `feature/e04-forge-ingestion-e1@2f8db345`, `feature/i8ab@fd63a2b8`, `feature/13a@e53c1da2`, `fix/e03-verification-correction-1@fac48051`, `fix/s0-metric-formula-identity-erratum@7e628bf5`. `feature/e05-analytics-convergence-a0@5dd998f1` idéntica a master. Candidatas a borrado SOLO tras inspección de worktrees, consumidores, PRs y refs.
- Línea acumulativa sin merge en master: `feature/e06-reference-enrollment-binding@b66dc5ff` (master +38) → `feature/e07-raw-facts-deal-lifecycle@3765f2ba` (E06 +12) → E08/E09. `feature/e08-routing-economic-command-risk-reservation@28db61b2` (master +82); `feature/e09-execution-copy-reconciliation-fidelity@0798ce4a` (master +99). E08 y E09 divergen desde `c2e88a0d`: E08 tiene 3 commits C3 no contenidos en E09; E09 tiene 20 commits en su lado. NO borrar E08 hasta integración demostrada.
- Línea separada: `feature/e04-dev-ingest-recovery@4aad647b` (master +5); incluye DEV Gateway certificado y migración 068, seguridad ETCD y modificaciones históricas de 061. Requiere merge selectivo compatible con 064–067, test hermético, y mantener el runtime DEV trazable. NO borrar hasta integrar y comprobar todos sus commits/efectos.
- Rescates divergentes: `rescue/e01-dirty-20260911-175139@dc0348c2` (1 commit único, S0 identity/tests); `rescue/e03-uncommitted-20260911-175842@ce9ee11d` (1 commit único, identidad/persistencia/migración 061). NO borrar ni fusionar sin reconciliar contenido y autoridad frozen. Conservar refs y SHAs en un registro si se opta por archivar.

## Estrategia operativa congelada

1. STOP nuevos desarrollos NORMAL y mandato coverage; comprobar worktrees locales/remotos, estado dirty/untracked, agente dueño y despliegues anclados a SHA. Inventario de preimages Git y del source no publicado. No tocar usuarios ni infraestructura PROD/SHARED.
2. Elegir **`feature/e09-execution-copy-reconciliation-fidelity` como rama activa/canónica** porque contiene históricamente E06→E07→E08 anterior a C3 y E09. Congelar el resto. NO crear otra rama remota de desarrollo. Usar worktree de integración aislado y rama **local temporal** desde SHA 0798ce4a.
3. Integrar E08 C3 `28db61b2` conservando ascendencia, resolver conflictos selectivos, comparar árbol/semántica y correr tests focalizados; no reescribir historia de ramas ajenas.
4. Integrar E04 recovery `4aad647b` sobre resultado, resolver 061/068 vs 064–067 y fail-closed ETCD source/tests, revisar `go.work`, DEV Gateway y E04/E06/E07/E08/E09 contratos. No aplicar migraciones ni deploy en esta sesión. No debilitar tests ni esconder fallas.
5. Suites de build/vet y regresiones por paquete con PG efímero único/dedicado; nunca lanzar `go test ./...` sobre infra compartida, ni correr tests peligrosos ETCD. Confirmar cobertura/status como deuda sin fingir cierre. Comparar failing set al baseline en condiciones equivalentes. Si bloqueado, conservar rama y entregar el defecto específico; no eliminar refs.
6. Tras integración verificada, publicar por **fast-forward normal** la rama E09 existente, read-back; comprobar `git merge-base --is-ancestor` para cada fuente, más equivalencia por contenido para cualquier cambio resuelto/cherry-pick y registro de diferencias. Si todo PASS, retirar solo ramas antiguas con cero commits únicos demostrados y worktrees desocupados; los rescates NO son descartables automáticamente. Cero force-push. Nunca modificar master en esta misión.
7. Resultado objetivo: master intacto y una sola feature activa; idealmente dos ramas visibles después de archivar las dos rescates de modo recuperable, pero NO prometer dos refs remotas mientras queden rescates divergentes o trabajo no integrado. La seguridad del código precede a la estética del listado. Mantener Agents-OS/roadmap/continuidad consistentes y cierre de sesión.

## Gates y estado

- INVENTORY + OWNERSHIP: GitHub confirmado; worktrees y consumo remoto aún NO VERIFICADOS.
- E08_INTEGRATED: PENDING.
- E04_INTEGRATED: PENDING.
- RESCUES_RECONCILED: PENDING.
- TESTS/BUILD/PG/SECURITY: PENDING sobre árbol consolidado.
- MASTER_UNCHANGED: obligatorio.
- SINGLE_ACTIVE_FEATURE: PENDING, no declarar completado hasta read-back de ramas y agentes.

**NEXT EXACT:** despachar un solo agente TOP para consolidar refs y limpiar de forma segura; no despachar cobertura E08/E09 en paralelo.