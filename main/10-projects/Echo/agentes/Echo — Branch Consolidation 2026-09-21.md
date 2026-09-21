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

**Prioridad antes de cualquier cobertura E-08/E-09, E-10 o nueva implementación:** reducir xKoRx/echo a `master` como línea estable y **una sola `feature/*` de desarrollo activa**. No perder commits, no forzar pushes, no confundir `SOURCE_VERIFIED` con release/physical; no integrar features inmaduras a master para simplemente borrar ramas. Owner del trabajo: manager Echo, agente TOP de integración. Ejecución 2026-09-21: integración publicada; cobertura sigue pendiente.

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

## Inventario verificado (Daedalus, 2026-09-21T16:48Z, antes de borrar refs)

Fetch `origin` sin prune destructivo de ramas de trabajo. Host `daedalus`, usuario `kor`. Clone principal `/home/kor/go/src/github.com/xKoRx/echo`. Cero PR abiertas. Workflows GitHub (`front-ci.yml`, `postgres-etapa0.yml`) disparan sólo `main`/`develop` o `workflow_dispatch`; ningún nombre `feature/*` ni `rescue/*` ni tag. Cero tags. Cero deployments GitHub. Runtime DEV no se tocó: Gateway `vcs.revision=3d260e81ee37dc80c3ff186b1a089e6aada07c1d`, Core `5dd998f16aea7b2821f460188718d7a6d279829c`. Esos binarios citan el nombre de rama sólo en `BUILD.md` histórico; el puntero de release es el SHA.

Worktrees del mismo repo, todos limpios salvo el de certificación (no se altera):

| Worktree | HEAD | Notas |
|---|---|---|
| clone principal | `feature/e02-control-safety-journal-recovery` @ `92d0ec2e0005464fcc85151754a33f34c044df42` | limpio, igual a origin; **ocupado** ⇒ la ref remota e02 se preserva |
| `/tmp/echo-e09-execution-copy-reconciliation-fidelity` | `0798ce4a8174c1a87745069da090df5d5e8ef011` | limpio, igual a origin; sin proceso; mtime = commit C2 |
| `/tmp/echo-e08-routing-economic-command-risk-reservation` | `28db61b2b1e6d0a266bcbf395c334d93dc8103bc` | limpio, igual a origin; sin proceso |
| `/tmp/echo-e07-raw-facts-deal-lifecycle` | `3765f2ba0d0d0ffdc3e07de91efdc8ded5c5e798` | limpio |
| `/tmp/echo-e06-reference-enrollment` | `b66dc5ffa3044ef91135014bfd0227ced31eff67` | limpio |
| `/home/kor/aranea/work/echo-dev-recovery-20260921/echo` | `4aad647bfdd31f6eb8599736922cf4f97c406827` | limpio, igual a origin |
| `/home/kor/aranea/work/cert-int-qa-20260920/repos/echo` | detached `5dd998f1` | **untracked** `zz_audit_h01_h02_h03_h07_test.go` y `zz_audit_h06_test.go`; no se toca |
| detached históricos e03/e06/dev-build | varios SHA ya en master o en E06 | sin delta; no se mueven |

Ningún agente tiene E09 sucio. E08/E09 no tienen commits locales sin publicar (`origin_ahead=0`, `local_ahead=0`). Exclusividad de esta sesión: sí para el merge; los worktrees ajenos no se reescriben.

Preimages `commit tree` (recuperables aunque se borre la ref, porque los ancestros de master siguen en `origin/master`):

| Ref | Commit | Tree | vs master | Exclusivos |
|---|---|---|---|---|
| `master` | `5dd998f16aea7b2821f460188718d7a6d279829c` | `81efb2bff973e3fbd6d70143a70eadd0c5d9e2b1` | — | — |
| `feature/deprecated-sl-offset` | `02fa35d843db82fb6160cc8e7633279f8d02c204` | `53c18f52768cfc02c26a3c533595873baedd4a01` | ahead 0, ancestor | 0 |
| `feature/e02-control-safety-journal-recovery` | `92d0ec2e0005464fcc85151754a33f34c044df42` | `0364b382d8f66ee8195032837f02dc023272b74f` | ahead 0, ancestor | 0; **PRESERVE** worktree ocupado |
| `feature/e04-forge-ingestion-e1` | `2f8db34560e9804c24287ecad9bdd5c8d3d41d03` | `3f382a386b5002e2b1648f0aa68917109961556a` | ahead 0, ancestor | 0 |
| `feature/e05-analytics-convergence-a0` | `5dd998f16aea7b2821f460188718d7a6d279829c` | `81efb2bff973e3fbd6d70143a70eadd0c5d9e2b1` | idéntica a master | 0 |
| `feature/i8ab` | `fd63a2b817a6adae4c133f9d7f626ae1cb499389` | `1c6a7f2a071afd80c3741257e9473178f5e391ca` | ahead 0, ancestor | 0 |
| `feature/13a` | `e53c1da2ca6a1517fbd62ac6928cfef7848e9fbf` | `06bebd7b6f69a6edefe0c11e1d0da45625d22c7d` | ahead 0, ancestor | 0 |
| `fix/e03-verification-correction-1` | `fac4805185eb586bb73c3df0c0ccc20d1377099c` | `4b3683979ad1c5e0ee0746cd9b1d2917a23e79be` | ahead 0, ancestor | 0 |
| `fix/s0-metric-formula-identity-erratum` | `7e628bf5fcadd92dc5398663d9b99a239a95ef7a` | `645b0d204a1a2047e69cd74b8384409dbae97e88` | ahead 0, ancestor | 0; local `da469d50` detrás 1, sin commits propios |
| `feature/e06-reference-enrollment-binding` | `b66dc5ffa3044ef91135014bfd0227ced31eff67` | `042f8447029f02265d3e80b43ecda932af1ae6e6` | ahead 38 | ancestro de E09 |
| `feature/e07-raw-facts-deal-lifecycle` | `3765f2ba0d0d0ffdc3e07de91efdc8ded5c5e798` | `e65e9c94767a557525d0bf7f919ce3cb79ab66ba` | ahead 50 | ancestro de E09; +12 sobre E06 |
| `feature/e08-routing-economic-command-risk-reservation` | `28db61b2b1e6d0a266bcbf395c334d93dc8103bc` | `69853c7abf867b9c875c304eb7659a423878eb0f` | ahead 82 | diverge de E09 en `c2e88a0d0d44160f2dc1b88f2a4886fdfb637d4f`; exclusivos `8fe7e5b2` C3-A, `b7c9adbe` C3-B, `28db61b2` docs |
| `feature/e09-execution-copy-reconciliation-fidelity` | `0798ce4a8174c1a87745069da090df5d5e8ef011` | `34f986daaf6d59dc3935e715324f778fb310d863` | ahead 99 | 20 commits desde `c2e88a0d`; contiene E06 y E07 |
| `feature/e04-dev-ingest-recovery` | `4aad647bfdd31f6eb8599736922cf4f97c406827` | `0d510275c8517666c76a560fc4b9ce4b6ce266eb` | ahead 5, behind 0 | `2360369c` `2498042f` `3d260e81` `988e0ae6` `4aad647b` |
| `rescue/e01-dirty-20260911-175139` | `dc0348c2d3f5fbf5ddba77df20a99332fc4dc862` | `630cc6b3231d9e65725303a3f78949b2f787121c` | ahead 1, behind 67 | no descartable |
| `rescue/e03-uncommitted-20260911-175842` | `ce9ee11ddb4196e20b68efaf0a96056224497634` | `92c7fda720e337525c74bb29f864487b98d8a0a2` | ahead 1, behind 61 | no descartable |

Local-only `impl/e04-forge-ingestion-e1-normal` @ `4aef2958ea444002b3ddb2d53f909f42b0c79921` es ancestro de master y de `feature/e04-forge-ingestion-e1`. Sin commits exclusivos. No es ref remota.

Preview `git merge-tree` (sin checkout): E09+E08 limpio, árbol `d61e8ebb1f27bd127f3ed19ac5988b09e51ace74`, delta = los 7 archivos C3. E08-merge+E04 limpio. `061` de E09 es idéntica a master; la de E04 se conserva byte a byte (guardas de ownership, no un segundo rewrite de esta sesión). `068` entra desde E04. `064`–`067` permanecen de E06–E09. `main.go` y `server.go` combinan el consumer E-06 con el ArtifactSource E-04. Objetos de preview `99d88762` y `4837a05f` no están en ninguna rama y no se publican.

## Ejecución (2026-09-21T17:0xZ)

Worktree aislado `/tmp/echo-consolidate-20260921`, rama local `integrate/e09-e08-e04-20260921` desde `0798ce4a8174c1a87745069da090df5d5e8ef011`. No se movieron los worktrees previos.

- Merge E08: `739238f09e928b7dc7cb64b3a4c6c464d6320f22` (padres `0798ce4a8174c1a87745069da090df5d5e8ef011` + `28db61b2b1e6d0a266bcbf395c334d93dc8103bc`). Sin conflictos. Delta = los 7 archivos C3. `8fe7e5b2` y `b7c9adbe` son ancestros.
- Merge E04: `5e0017e556b714cf26c3cdde4cbbe6725a1a09ef` (padres `739238f09e928b7dc7cb64b3a4c6c464d6320f22` + `4aad647bfdd31f6eb8599736922cf4f97c406827`). Auto-merge de `v3/gateway/cmd/echo-gateway/main.go` y `v3/gateway/internal/server.go`: quedan el consumer E-06 y el ArtifactSource de filesystem. `061` y `068` byte-idénticos a E04. `064`–`067` byte-idénticos a E09. `061` de E09 era idéntica a master; no hubo segundo rewrite. Las guardas de ownership de E04 se conservaron. No se aplicó nada en DEV ni PROD.
- Ajuste de harnesses: `865532078f2c1993e7a3a542a78a9db0fad1f015`. El rebuild E-08 salta 067/068; el de identidad se detiene en 060; el reset de fixtures de identidad suspende los triggers write-once de E-06 sólo en la base descartable y los reactiva.
- Publicación: FF normal `0798ce4a..86553207` a `origin/feature/e09-execution-copy-reconciliation-fidelity`. Read-back `origin` = local = `865532078f2c1993e7a3a542a78a9db0fad1f015`. `origin/master` sigue `5dd998f16aea7b2821f460188718d7a6d279829c`.

## Gates y estado

- INVENTORY + OWNERSHIP: VERIFICADO. E09 no tenía agente activo.
- REDUNDANT_DELETE: hecha en origin para `feature/deprecated-sl-offset` `02fa35d8`, `feature/e04-forge-ingestion-e1` `2f8db345`, `feature/i8ab` `fd63a2b8`, `feature/13a` `e53c1da2`, `fix/e03-verification-correction-1` `fac48051`, `fix/s0-metric-formula-identity-erratum` `7e628bf5`, `feature/e05-analytics-convergence-a0` `5dd998f1`. Todas ahead=0 y ancestros de master. `feature/e02-control-safety-journal-recovery` `92d0ec2e` PRESERVE: el clone principal está checkout en esa rama.
- E08_INTEGRATED: SÍ, ancestro de `86553207`.
- E04_INTEGRATED: SÍ, ancestro de `86553207`. Migración 061 certificada por `identity_bwc/run.sh` PASS en PG 17.11 descartable `127.0.0.1:15471/echo_identity_disposable`. En el schema consolidado, AC-13/AC-17 del test Go se saltan porque 064 ensancha `active_positions.strategy_id`; no es un fallo de 061.
- RESCUES: PRESERVE. E01 conserva `verification_findings_test.go` ausente en HEAD y un delta en `identity.go`. E03 tiene blobs divergentes (061, repos, MT4, pipe). No se fusionaron ni se borraron.
- TESTS: build core/gateway/echo-etcd-bootstrap PASS; vet PASS. Hermético sin `DATABASE_URL` ni `ETCD_ENDPOINTS`: etcd v1/v2/v3, econroute, execfid, gateway, postgres PASS (los de PG hacen skip). Con PG descartable `127.0.0.1:15471/echo_consolidate_disposable`, un paquete por vez y `-race`: econroute, execfid, tradefacts, gateway, postgres PASS. Harness `economic_commands_e8` PASS, `execution_fidelity_e9` PASS, `identity_bwc` PASS. Una corrida paralela de varios paquetes contra la misma base falló por truncate cruzado; no cuenta como regresión. Flags `ECHO_E8_DURABLE_ROUTING` y `ECHO_E9_EXEC_FIDELITY` siguen default OFF. No se corrió `go test ./...`. No se tocó ETCD ni PG compartido. Cluster descartable detenido al cierre.
- MASTER_UNCHANGED: `5dd998f16aea7b2821f460188718d7a6d279829c` inicial y final.
- SINGLE_ACTIVE_FEATURE: `feature/e09-execution-copy-reconciliation-fidelity` @ `865532078f2c1993e7a3a542a78a9db0fad1f015`. Origin además conserva `feature/e02-control-safety-journal-recovery` y las dos `rescue/*`. Refs remotas E04 recovery, E06, E07 y E08 retiradas; sus worktrees locales siguen en los SHA viejos y no se movieron.
- COVERAGE_GATE, PHYSICAL y ECONOMIC: siguen pendientes. No se declaran PASS.

**NEXT EXACT:** el siguiente agente trabaja sólo en `feature/e09-execution-copy-reconciliation-fidelity` @ `865532078f2c1993e7a3a542a78a9db0fad1f015` (worktree nuevo o fast-forward del existente). El cierre de `COVERAGE_GATE` de E-08 y después el de E-09 corre sobre ese SHA, sin reabrir las ramas retiradas y sin activar flags económicos.