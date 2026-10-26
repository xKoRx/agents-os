---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[SHOT3_ADVERSARIAL_REPORT]]"
  - "[[SHOT4_FIX_PACKAGE]]"
  - "[[SHOT2_IMPLEMENTATION_REPORT]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-26"
updated: "2026-10-26"
---

# SHOT3_COVERAGE_MATRIX — Ingestion V2

## Propósito

Exactamente H01–H49 con un veredicto por ID del Shot 3 (QA adversarial independiente), más QA01 transversal separado. Artefacto auditado: xKoRx/echo `lab-v4/shot4-integration@d223d9f816338a831f5cf4c1acdc1c1ea9145917` (candidate `feature/lab-v4-ingestion-v2` == destino). Oráculos: propios del auditor (receta wire/OperationDigestV2 reimplementada desde fuente en `wire_oracle.py`; readback SQL por conexión independiente; timing real en Q). Ningún PASS de Shot2/Shot4 heredado: las filas no re-ejecutadas quedan NOT_RUN con su evidencia histórica anotada, sin convertirlas en PASS.

## Contenido

**Conteo disjunto de los 49 casos principales: 12 PASS / 1 FAIL / 2 BLOCKED_EXTERNAL / 34 NOT_RUN.** QA01 (transversal, aparte): **FAIL** — V4 histórico 85,8/85,2 < 95 vigente; delta E+O medido por el auditor: lógica 100% statements, wiring/cmd 0% sin suites (hallazgo S3-A-05). Cero NOT_RUN convertidos en PASS por inferencia; cero defectos convertidos en bloqueos externos.

| Caso | Estado Shot3 | Oráculo/evidencia del auditor (síntesis) |
|---|---|---|
| H01 | BLOCKED_EXTERNAL | Porción auténtica requiere AUTH_FORGE (X_AUTH_ARTIFACT, recurso concreto no generable por mandato). Porción NUM re-verificada con oráculo propio: version_ref/definition sha bit-exactos (P1), crosswalk/registry/definitions/links/instruments + Magic NULL en readback SQL (E04). |
| H02 | **PASS** | E07 + P8 + P11: 12 paralelos misma key ⇒ 1×202 + 11×429 Retry-After (cap bulk 1/ns), retry converge 200 replay, receipts=1; respuesta perdida → GET-by-key mismo receipt; snapshot inmutable GET-id×2/by-key byte-idénticos. |
| H03 | **PASS** | E08 + P3: 2 PUT mismo expected ⇒ 1 gana + 412; falta precondición 428; If-Match divergente 400/412; una sola revisión nueva; replay del ganador tras N+2 devuelve receipt original (P13). |
| H04 | **PASS** | E05 + P12 + E09: 8 historias completas OK; 9ª ⇒ 413 sin receipt; última inválida revierte todo (cero receipts/heads parciales); SIGKILL antes de commit sin estado intermedio. Nota: límite de body probado con el máximo configurado del harness (8 MiB), no el literal 128 MiB. |
| H05 | BLOCKED_EXTERNAL | Porción auténtica (AUTH_FORGE) bloqueada; porción funcional PASS: O01 — targets cliente alterados 422 ASSERTION_MISMATCH, cuentas jamás creadas por producto (runtime_accounts sin crecimiento), CAS dos writers 1×202+1×412, key conflict 409. |
| H06 | **PASS** | O02 + O05 + Q: consumidor detenido ⇒ PROVISIONING (outbox sin ACK); apply→lookup→proof→ACK exactos ⇒ ECHO_OPERATIONAL_READY con expected/applied por consumidor; lookup real en stores; OBSERVE_MASTER 0 órdenes (trade_journal intacto); dos bindings sin cross-talk. |
| H07 | NOT_RUN | Master t+60s vía ingress real requiere el camino J (managed_context/JournalObservationServiceV2): no implementado en el candidate (S3-A-04). Alcance declarado en Shot2 §S4. |
| H08 | NOT_RUN | OPEN pre-ready/bulk es superficie J: no implementada (S3-A-04). |
| H09 | **PASS** | O03 + O04 + Q1–Q4 con timing real: lease 15 s expira ⇒ DEGRADED medido por HTTP (~17 s) y persiste sin re-ACK; restart de encarnación invalida ACK; ACKs forjados (digest ajeno/applied_at regresivo/binding ajeno/revisión ajena) rechazados; renewal sólo con lookup exacto; REVOKED deniega el gate nativo real. |
| H10 | **PASS** | E09 + O03: crash antes/después de commit del endpoint sin estado intermedio; crash apply/ACK/delivered con recovery idempotente desde durable. Puntos tras intake/journal (J) y tras journal/LAB (L) NO_RUN por alcance. |
| H11 | NOT_RUN | Source ownership dos versiones/cuentas vía ingress real (J): no implementado. La porción registry (crosswalk race, 409) sí verificada en E08/P1. |
| H12 | NOT_RUN | Execution facts/dedupe (J): no implementado. |
| H13 | NOT_RUN | Continuidad Forge/Echo con crosswalk (J/L): no implementado. |
| H14 | **PASS** | P13 con oráculo bit-exacto: 40→30→0 (CORRECTION + RETRACTION, operación ausente en N+1), `previous_record_digest` propio aceptado (`sha256:9f321aaa…`), previous ajeno 422 CHANGE_EVIDENCE_MISMATCH, readback rev1/rev2/rev3 (net 40/30/—), change_entries=2, replay ganador tras N+2 ⇒ receipt original. |
| H15–H26 | NOT_RUN (12) | Economía/precisión (worker real, curvas, monedas, temporalidad, estático, wire numérico): superficie no tocada por el delta E/O (0 archivos compartidos); evidencia previa V4 @ `b2b3ebfe` PASS (no heredada como estado; sólo anotada). |
| H27–H33 | NOT_RUN (7) | Rankings/cohorte/kernel compartido: superficie no tocada; pin `v0.0.1-lab-v4-shot2.1` verificado intacto en bridge go.sum; evidencia previa V4 anotada. |
| H34 | NOT_RUN | Relay/lease del worker V4: superficie no tocada. La porción claim/fence del binding (mismo patrón B6) sí verificada en O03/Q. |
| H35 | **PASS** (delta) | E11 en PGs frescas propias: 067–085 APPLIED con ledger (19/19); reapply ALREADY_APPLIED con fingerprint idéntico; tamper ⇒ MIGRATION_CHECKSUM_CONFLICT pre-DDL; mid-fail 068 ⇒ rollback sin DDL parcial y ledger=1; FK append-only de 085 enforced (P14); 067–083 byte-idénticas. |
| H36–H42 | NOT_RUN (7) | Read bundles/cursors/screener/detalle/estados/roles: front/Hasura sin cambios en el delta; sin browser en este shot; evidencia previa V4 anotada. |
| H43 | **PASS** | E02 + E03 + E12 + P4 + P6 + P7: 401 sin/inválido token; 403 rol/sin grant; 404 cross-ns; 415 media type; 400 JSON roto/dup key/Idempotency-Key inválida; 413; 429 Retry-After; errores sin token/SQL/stack; cero efectos laterales. Defecto de tolerancia Content-Type registrado (S3-A-02). |
| H44 | NOT_RUN | Capacidad SCALE 132805: superficie no tocada; evidencia previa V4 (dos auditores) anotada. |
| H45 | **FAIL** (histórico) | Presupuesto prepare p95 ≤ 2 s a 20k: no re-ejecutado en este shot y sin prueba suficiente de remisión (el delta no toca prepare/bundles); se mantiene FAIL por excepción histórica, sin cambiar presupuesto (C3). Los otros 22 invariantes del oráculo H45 permanecen en su estado V4, no re-verificados aquí. |
| H46 | **PASS** (parcial) | P11: 429 Retry-After 2 s ANTES de sobre-admisión con receipts=1 y convergencia por retry; sin starving del POST único. Clases compute/outbox (V4, no tocadas) no re-ejecutadas. |
| H47 | **PASS** | E12 + disciplina del manifest propio: loopback-only verificado por `ss` por PID, 0 workers levantados, 0 órdenes, sin ETCD/Kafka/Hasura/PROD, guard de puertos prohibidos del Shot2 respetado; 3 huérfanos propios detectados y eliminados individualmente (ownership exacto). |
| H48 | **PASS** | Teardown final verificado: 4 postmasters propios terminados por PID dueño de puerto; puertos 56327/31/33/35 libres; pgboot de otros workspaces intactos; sin killall/wildcard; residuo propio cero. |
| H49 | NOT_RUN | Fanout nativo completo (Strategy→Signal→Operation→MM): superficie V4 no tocada. El gate nativo real sí fue re-ejercitado por O04/O05 (READY pasa, REVOKED/DEGRADED deniegan, sin LIMIT1). |
| QA01 (transversal) | **FAIL** | V4 histórico 85,8/85,2 < 95 vigente en el candidato. Delta E+O medido por el auditor: lógica (contracts 4 / postgres 7 / gateway 3 archivos) 100.0% statements; wiring/cmd del delta 0% sin suites (bridge 3 stmts, core 3 stmts, harness main, toolkit) — clase estructural del residuo V4; S3-A-05 registra que el implementador no publicó cobertura del delta. Perfiles: `ev3/cov_*.out`. |

## Notas de conteo

- Los estados son de ejecución del Shot 3 sobre `d223d9f8`: PASS exige oráculo propio en este SHA; NOT_RUN = no ejecutado (jamás equivale a ausencia de defecto); BLOCKED_EXTERNAL sólo con recurso concreto (AUTH_FORGE en H01/H05) e intento documentado.
- Las 34 NOT_RUN se agrupan: 13 por alcance J/L/F no implementado (H07, H08, H11, H12, H13 + filas L/F de C3) y 21 por superficies V4 no afectadas por el delta (economía 12, rankings 7, worker H34, capacidad H44, nativo H49) con evidencia previa anotada sin heredarla.
- Hallazgos de este shot: S3-A-01 (P2, historical), S3-A-02 (P3, new_delta), S3-A-03 (P2, new_delta), S3-A-04 (P2, scope), S3-A-05 (P3, evidence), S3-A-06 (P3, observación). Detalle y repros en [[SHOT3_ADVERSARIAL_REPORT]].

## Fuentes

- [[H — Test Matrix Independent Oracles]] (contrato de oráculos y evidencia); [[C — Implementation Shots and Acceptance Gates]] C3/C4; [[SHOT2_IMPLEMENTATION_REPORT]]; [[SHOT3_ADVERSARIAL_REPORT]]; evidencia `/srv/echo-work/ingestion-v2-shot3-20261026/harness/ev3/` (`EVIDENCE_INDEX.sha256`, runs E `25cbba1d`, O `966db9ad`, Q `416ffe32`, probes `b0476ba2`/`867c3d86`/P13-P14, E11, cov_*.out).
