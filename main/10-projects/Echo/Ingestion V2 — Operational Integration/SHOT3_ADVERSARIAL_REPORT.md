---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
  - "[[SHOT2_IMPLEMENTATION_REPORT]]"
  - "[[SHOT3_COVERAGE_MATRIX]]"
  - "[[SHOT4_FIX_PACKAGE]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-26"
updated: "2026-10-26"
---

# SHOT3_ADVERSARIAL_REPORT — Ingestion V2

## Propósito

Reporte de QA adversarial independiente (C4/D3) sobre el candidato Shot2: xKoRx/echo `lab-v4/shot4-integration@d223d9f816338a831f5cf4c1acdc1c1ea9145917` (rama candidate `feature/lab-v4-ingestion-v2` == `d223d9f8`). Modelo ejecutor: GLM-5.3-Flash Max LOCAL, sesión fresca, sin autoría de implementación (no participé en Shot2). Ningún PASS del reporte Shot2 ni del Shot4 V4 se heredó: todo estado propio se re-derivó con expected propio desde fuente/recetas reimplementadas. Sin fixes de producto; paquete Shot4 en [[SHOT4_FIX_PACKAGE]].

## Contenido

### R1. Verificación de SHAs, integración temprana y artefacto

| Verificación | Resultado | Evidencia |
|---|---|---|
| Remoto `lab-v4/shot4-integration` | `d223d9f8` (ls-remote; el destino NO avanzó tras Shot2) | `git ls-remote origin` en worktree |
| Candidate == remoto | worktree `feature/lab-v4-ingestion-v2` limpio en `d223d9f8` | `git status` sin delta |
| Ancestry base→final | `b2b3ebfe` ancestro de `d223d9f8` (ANCESTRY_OK) | `git merge-base --is-ancestor` |
| Commits del delta | exactamente 5, lineales, sin commits ajenos: `613a0f16` (E) → `2cef162c` (E) → `0e45ebf4` (E, ENDPOINT_SHA) → `b085b8c0` (O) → `d223d9f8` (O) | `git log --format='%h %p %an' b2b3ebfe..d223d9f8` |
| Early merge E antes de O | los 3 commits E preceden a los 2 commits O en la cadena parental del destino; orden consistente con ff-only `b2b3ebfe..0e45ebf4` | mismo log |
| Provenance de rama | base desciende de `lab-v4/shot4-final@055cd69c` (SHOT4_FINAL_IS_ANCESTOR_OK); `merge-base(candidate, feature/ef-runtime-pools) = ac0621a1` = ancestro común de A1: cero commits runtime trasplantados | merge-base checks |
| Build auditado propio | rebuild desde el árbol limpio: `vcs.revision=d223d9f8`, `vcs.modified=false`, go1.27.1 `-trimpath -buildvcs=true`, SHA256 `dd67b942cc0e589f637f762f7449285dacce89e9ce0caef552859c692d882567` | `go version -m` |
| Binario del implementador | `harness/gateway-harness-bin` SHA256 `9e01ded4…` coincide con el reporte Shot2 y sus stamps (`vcs.revision=d223d9f8`, `vcs.modified=false`) | sha256sum + go version -m |
| Migraciones | sólo `084`/`085` nuevas; `067–083` byte-idénticas; `v3/front` y `v3/hasura` sin cambios; pin `shared-analytics v0.0.1-lab-v4-shot2.1` intacto (bridge go.sum) | `git diff --name-only b2b3ebfe..d223d9f8` |

Observación (no defecto): rebuild propio produce bytes distintos (`dd67b942…`) con stamps idénticos al reportado (`9e01ded4…`); Go no fue byte-reproducible entre corridas de build en este host. Identidad recomendada por buildinfo (`vcs.revision` + `vcs.modified`), no por SHA de bytes.

### R2. Hallazgos (formato C4)

| ID | Severidad | Atribución | Hallazgo |
|---|---|---|---|
| S3-A-01 | P2 | historical (pre-existente en `b2b3ebfe`, línea 695-696 + handler sin chequeo de path) | POST a `/api/v2/strategy-ingestions/{segmento-extra}` responde **202 y crea receipt**; B3 exige "matching exacto por segmentos… rechazar segmentos extra". El patrón mux subtree (`/api/v2/strategy-ingestions/`, `lab_v4_gateway.go:768`) despacha POST con sufijo arbitrario al mismo handler, cuyo `case POST` nunca compara `r.URL.Path` exacto. Repro: POST válido con Idempotency-Key `p5a` a `…/strategy-ingestions/extra-segment` → 202; `echo.strategy_ingestion_receipts` gana la fila (ns del actor). Riesgo: creación de recursos por rutas no documentadas y confusión de superficie; sin pérdida de datos ni duplicación de órdenes. Owner: gateway (`lab_v4_gateway.go`). Criterio de corrección: rechazo 404 (o 405) de POST con path ≠ exacto, cero efectos; repro pasa. |
| S3-A-02 | P3 | new_delta (`2cef162c`) | El chequeo B3 de Content-Type usa `strings.HasPrefix(ct, "application/json")`: acepta `application/json; charset=utf-8` y también `application/json-patch+json` (202). El contrato exige `Content-Type: application/json`. Impacto bajo (el body sigue validándose estricto; no hay bypass). Owner: gateway. Criterio: parse de media type y comparación exacta type/subtype; charset/param → 415 o decisión documentada. |
| S3-A-03 | P2 | new_delta (`b085b8c0` + `d223d9f8`) | El binario ELF `v3/core/echo-core` (40.284.194 bytes, debug_info, no stripped) fue **re-agregado a la rama producto**: ausente en `b2b3ebfe`, añadido en `b085b8c0` y re-commiteado en `d223d9f8`. Su build stamp es `vcs.revision=b085b8c0…` con **`vcs.modified=true`** (build sucio) ⇒ la punta de la rama versiona un binario stale y no reproducible del propio código. Impacto: higiene/integridad (~80 MB en historia tras dos commits) y riesgo de confusión de artefacto. Owner: higiene de repo Shot4. Criterio: `git rm` forward (sin rewrite), regla anti-binario, nada ejecuta ese path. |
| S3-A-04 | P2 | scope (declarado) | Incrementos **J/L/F sin implementar** (alcance restante de Shot2, declarado en reporte Shot2 §S4): `managed_context` y `reference_dispatch_outbox` ausentes del candidate, consumidor de `journal_change_outbox` ausente en lab-worker, sin worktree/entry point Symphony (`sqx/cmd/echo-ingest-v2` inexistente). Consecuencia: filas J01–J06, L01–L05, F01–F03 y 13+ filas H dependientes NOT_RUN. No es defecto oculto; bloquea la aceptación final del workstream hasta Shot2-residual/Shot4. |
| S3-A-05 | P3 | evidence (Shot2) | El implementador no publicó cobertura del delta (QA01): sólo rc=0 de suites. El auditor la midió (R4): lógica del delta 100% statements; adapters wiring/cmd 0% sin suites dedicadas (clase estructural ya adjudicada en V4). |
| S3-A-06 | P3 | observación | Build no byte-reproducible con stamps iguales (R1); sin consecuencia runtime. Verificar identidad por buildinfo. |

BLOCKED_EXTERNAL transversal (adjudicación vigente, sin cambios): **AUTH_FORGE** — falta copia autorizada e inmutable de artefacto Forge con trade list y lineage (`X_AUTH_ARTIFACT`). Recurso concreto requerido: copia autorizada existente; obtenerla mediante campaña nueva está prohibido por mandato. Afecta la porción auténtica de H01/H05; no convierte defectos en bloqueos ni limita gates funcionales con fixtures NUM/NEGATIVE etiquetados.

### R3. Ejecución adversarial (gates C1/C3 y probes propios)

Harness propio del auditor (manifest `harness_manifest.json` run `1040b1b1`): PG embebida 18.3 propia en 56327 con base 001–066 + protocolo V4 067–085 APPLIED con ledger (19/19), dos PGs E11 (56331/56333/56335), artifact roots propios, gateways del binario reconstruido por el auditor, loopback-only, sin ETCD/Kafka/Hasura/PROD, cero órdenes. Evidencia y drivers fuera del vault: `/srv/echo-work/ingestion-v2-shot3-20261026/harness/` (índice con SHA256 en `ev3/EVIDENCE_INDEX.sha256`).

- **Gate E re-ejecutado (edriver contra mi harness y mi build): E01–E10 + E12 = 11/11 PASS** (run `25cbba1d`); **E11 protocolo separado PASS** (abajo). Regresión de superficies afectadas en el SHA: contracts rc=0, sdk/postgres rc=0 (108 s), gateway/internal rc=0 — ejecutadas por mí contra mi PG (mi `regression.txt`; el del implementador no fue reutilizado).
- **Gate O re-ejecutado (odriver, supervisores/installers reales del SDK): O01–O05 = 5/5 PASS** (run `966db9ad`).
- **Probes adversariales propios del auditor (expected desde receta reimplementada en Python, sin importar SDK):**
  - P1–P10: 9 PASS + P5 FAIL = hallazgo S3-A-01. Destacados: `version_ref` y `strategy_definition_sha256` **bit-exactos** contra oráculo propio (H/D receta fuente); request_digest estable ante reorden de claves (canónico); PUT CAS 1 ganador + 412 + 428 + If-Match 400/412 con una sola revisión nueva; 401/403/404/415/400/429 con cero efectos laterales; binding sin grant 403 fail-closed (productor y operador); snapshot receipt inmutable GET-id×2/by-key byte-idénticos; PROVISION_REFERENCE dentro del envelope 503 sin efectos; artifact bytes verificados sha256 en store.
  - P11/P12: 12 POST paralelos misma key ⇒ 1×202 + 11×429 Retry-After (cap bulk=1/ns por diseño C-12/H46), retry converge a 200 replay, `receipts=1`; 9 historias ⇒ 413 sin receipt (run `867c3d86`).
  - P13: corrección N+1 (40→30) y retracción N+2 (operación ausente) con **`previous_record_digest` calculado por mi oráculo Python aceptado bit-exacto** por el producto (`sha256:9f321aaa…`); `previous` ajeno → 422 CHANGE_EVIDENCE_MISMATCH; readback rev1 net=40 / rev2 net=30 / rev3 sin operación; `history_change_entries`=2; replay del ganador tras N+2 devuelve el receipt original (rev 2).
  - P14: FK de `runtime_binding_mutation_receipts` (085) enforced contra binding inexistente.
- **Probes Q propios (timing real, driver Go propio): 4/4 PASS** (run final `416ffe32`): lease real 15 s expira → readiness **DEGRADED medido por HTTP (~17 s)** y persiste sin re-ACK; renewal con lookup exacto (store del consumidor) vuelve READY y con digest ajeno rechaza; 4 ACKs forjados (digest ajeno, applied_at regresivo, binding ajeno, revisión ajena) todos rechazados sin falsar READY; restart de encarnación invalida ACK previo (PROVISIONING) y el re-ACK desde store durable recupera.
- **E11 (protocolo F, PGs frescas propias): PASS** — fresh+upgrade 19/19 APPLIED con ledger; reapply 085 → `ALREADY_APPLIED` con fingerprint de schema idéntico; tamper 085 (bytes ≠ ledger) → `MIGRATION_CHECKSUM_CONFLICT` **antes de DDL**; mid-fail 068 (`SELECT 1/0` válido al cierre, manifest re-sellado) → `V4_FAILURE division by zero`, ledger=1 (sólo 067), sin DDL parcial (objetos de 068 ausentes; `strategy_definitions` proviene de 001/061 de la base, no de 068). Nota honesta: con manifest re-sellado y ledger vacío, el runner aplica el tamper (el re-sello es operación legítima del protocolo); la protección real es ledger-vs-bytes, demostrada en la PG con 085 original.

### R4. QA01 — cobertura del delta (medición propia del auditor)

- Paquetes del delta con suites: contracts (4 archivos nuevos/cambiados: 71+273+321+23 stmts), sdk/postgres (7 archivos), gateway/internal (3 archivos) ⇒ **100.0% statements** en todos los archivos lógicos del delta E+O (2484 stmts en postgres+gateway; contracts completo por archivo). Perfiles: `ev3/cov_{contracts,postgres,gateway}.out`.
- Wiring/cmd del delta sin suites dedicadas: `v3/bridge/internal/runtime_config_installer.go` 0% (3 stmts), `v3/core/cmd/echo-core/runtime_config_installer.go` 0% (3 stmts), `gateway/cmd/echo-gateway-harness/main.go` y `toolkit/cmd/apply-migration/main.go` sin medir — delegadores de la lógica SDK ya cubierta y ejercitados físicamente por los gates O/Q, pero clase estructural idéntica al residuo QA-01 de V4.
- QA01 transversal: **FAIL se mantiene** (V4 85,8/85,2 < 95 es histórico y sigue vigente para el candidato; el delta E+O queda verde en lógica y con residuo estructural en wiring). Hallazgo S3-A-05 registra el hueco de reporte del implementador.

### R5. Límites y estados

- Sin AUTH_FORGE: ninguna certificación de autenticidad Forge; los fixtures usados son NUM/NEGATIVE etiquetados en namespaces `labv4qa3*` propios.
- H45 (prepare p95 ≤ 2 s a 20k) y QA-01 V4 no se re-ejecutaron por presupuesto del shot: el delta no toca sus superficies (0 archivos compartidos con lab-worker/bundles/front); se reportan como **excepción histórica sin prueba de remisión** (H45 FAIL, QA01 FAIL).
- Las filas de superficies J/L/F y de matemática V4 no afectada por el delta quedan NOT_RUN (34 filas): NOT_RUN no equivale a ausencia de defecto; su plan de cierre está en [[SHOT4_FIX_PACKAGE]].
- PG del harness 18.3 (igual que Shot2; contrato decía PG16; mismo protocolo DDL, versión registrada honesta).

### R6. Evidencia, ownership y cleanup

- Manifest del harness: run `1040b1b1`, namespace `labv4qa3*`, hosts permitidos loopback, puertos prohibidos del Shot2 excluidos (56127/56229/56231/56233/56241…). Evidencia completa: `/srv/echo-work/ingestion-v2-shot3-20261026/harness/ev3/` (gates E/O/Q, probes P, E11, coberturas, regresión, logs de gateways) con `EVIDENCE_INDEX.sha256` (28 artefactos hasheados).
- Oráculos propios: `harness/oracle/wire_oracle.py` (perfil `echo-wire-json.v1`, H/D, version_ref, definition digest, `OperationDigestV2` completo — verificado bit-exacto contra el producto en P1 y P13), `probes.py`, `probes_parallel.py`, `probes_history.py`, `qdriver/` (driver Go propio con replace al worktree del candidate).
- Cleanup verificado: postmasters de mis 4 PGs terminados por PID dueño del puerto; gateways propios terminados (incluidos 3 huérfanos míos detectados y eliminados individualmente — lección de ownership registrada); sin `killall` ni borrado ajeno; los pgboot de otros workspaces (`lab-v4-shot4-20261023`) quedaron intactos; puertos 56327/31/33/35 libres; cero residuos de procesos propios.

### R7. Veredicto

`SHOT3_ADVERSARIAL_COMPLETE_WITH_FINDINGS` sobre `d223d9f8`. El artefacto integrado resiste la falsificación en las superficies E+O con oráculos independientes (12 H PASS propios, gates E 11/11 + E11 + O 5/5 + probes). Defectos: S3-A-01 (P2, histórico, superficie V2), S3-A-02/S3-A-03 (delta), S3-A-04 (alcance J/L/F pendiente), S3-A-05/S3-A-06 (P3). Sin P0. H45/QA01 históricos se mantienen FAIL por excepción histórica sin remisión. Matriz completa y conteos disjuntos: [[SHOT3_COVERAGE_MATRIX]]. Entrada de Shot4: [[SHOT4_FIX_PACKAGE]]. No se inició Shot4 ni se modificó producto.

## Fuentes

- Mandato Owner 2026-10-26 (D3); [[F — Decision Register]] D25–D27; [[B — Frozen Architecture]]; [[C — Implementation Shots and Acceptance Gates]]; [[A — Source Baseline and Branch Integration]]; [[E — Executable Contract Examples]]; [[SHOT2_IMPLEMENTATION_REPORT]]; [[H — Test Matrix Independent Oracles]]; [[Echo + Echo Forge — Environment Contract]].
- Evidencia externa: `/srv/echo-work/ingestion-v2-shot3-20261026/harness/` (manifest `1040b1b1`, `ev3/EVIDENCE_INDEX.sha256`).
