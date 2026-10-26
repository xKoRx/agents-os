---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# C — Implementation Shots and Acceptance Gates

## Propósito

Plan ejecutable de los tres shots restantes, gates y revisión del freeze. El proyecto padre Echo conserva la planificación; no se crea otro proyecto ni un quinto shot.

## Contenido

### C1. Gate obligatorio de integración temprana

**ECHO_INGESTION_V2_ENDPOINT_INTEGRATION_PASS** exige todas las filas E01–E12 PASS sobre un SHA concreto. Ejecución al diseñar: **NOT_RUN**. La lectura de A/B no certifica funcionamiento. Owner autoriza integración inmediata al cumplir este gate; la regla genérica de planning que reserva aceptación al owner no agrega otra confirmación al mandato explícito del 2026-10-26.

Harness: reutilizar v3/gateway/cmd/echo-gateway-harness con internal.NewServer, PG16 propio persistente entre reinicios y artifact root propio; auth/cursor/config explícitos, loopback reservado y manifest de ownership. No handler aislado como sustituto. Readback SQL desde conexión independiente read-only y oráculo que no invoque el servicio bajo prueba. Runner real de migraciones y ledger. Worker detenido durante POST prueba independencia analítica. Cero commands/órdenes. Ejemplos E generan requests, no certifican autenticidad.

| Caso | Estímulo y oráculo independiente | Evidencia mínima |
|---|---|---|
| E01 router | POST real202; ruta incorrecta404, método405; build corresponde al SHA | URL/puerto owner, request/response sanitizados, PID/build/config digest |
| E02 auth/scope | Sin token401, rol inválido403, ns/producer ajeno rechazado; GET id/key ajeno404 | Identidades propias A/B y SQL counts antes/después |
| E03 contrato | DTO válido y unknown/duplicate/invalid UTF8/recipe/hash/declared_ref incorrectos; límites/encoding | Recomputación independiente digest/version,400/422/413/415 y cero efectos |
| E04 registry | StrategyVersion paquete íntegro, crosswalk, StrategyDefinition/runtime links/instrumentos, Magic NULL | SELECT independiente con refs exactas y counts |
| E05 histories |1 y8 historias completas; error en última revierte todo | Digests/counts/source IDs/economía/coverage/heads contra manifest |
| E06 receipts | GET id y key después de reiniciar Gateway/PG sobre mismo volumen | Snapshot/ref/digest/accepted_at idénticos y artifact bytes recuperables |
| E07 replay | Paralelismo misma key/body; respuesta perdida después commit | Un receipt/heads/dirty, replay200 mismas refs |
| E08 conflictos | Key diferente body409, external identity incompatible409; misma versión nueva key reutiliza; paquete distinto409 | Race de crosswalk, cero mutación de versión/receipt original |
| E09 fallos | Crash antes/después commit; fallo último insert/artifact | Rollback completo o receipt íntegro; sin estado intermedio |
| E10 regresión | Suites afectadas API/contracts/PG/history/worker/readbundle; PUT CAS/metadata y roles cuando se tocan | SHA/casos/expected/actual; cero nuevas fallas |
| E11 SQL | Fresh+upgrade desde base; reapply; checksum alterado/fallo mitad migración | Ledger/schema/grants idénticos tras replay; error sin DDL parcial |
| E12 seguridad | Destino externo inválido, ownership ausente, cancelación/cleanup; analytics detenido | Guard rechaza antes de red, órdenes0, inventario y cero residuos propios |

No exigir READY, copy ni curvas terminadas. H45/QA01 históricos se informan con no-regresión, no se renombran PASS. AUTH_FORGE no es prerequisito de E; fixtures NUM/NEGATIVE etiquetados. Defecto nuevo atribuible al incremento bloquea merge. PROVISION_REFERENCE transitoriamente503 sin efectos hasta completar O.

Cada caso: {case_id,requirement,source_sha,build_sha256,vcs_modified,toolchain,migration_checksums,harness_manifest_sha256,fixture_kind,fixture_digest,request_digest,expected,actual,status,evidence_refs,elapsed,cleanup}. Logs/capturas/JSON fuera del vault, resumen con rutas relativas y digests dentro. Además diff/commits y destino antes/después/RESUME_BASE_SHA según A4.

### C2. Shot 2 — implementación e integración incremental

Modelo de ejecución: **GLM-5.3-Flash Max LOCAL**, nunca GLM-5.3 normal ni fallback GOD. E/O/J/L/F son incrementos internos, no nuevos shots.

| Orden | Trabajo y ownership de fuentes efectivas | Gate / condición de avance |
|---|---|---|
| 1 · E endpoint | Gateway server/lab_v4_gateway/v2_wire; SDK contracts/registry/history/store y runner SQL si necesario. B2–B4/E. | E01–E12 PASS → integrar INMEDIATAMENTE a The Lab con A4. Registrar y sincronizar base antes de O. |
| 2 · O operacional | SDK runtime_binding_repository/runtime_config_supervisor/runtime_ack_repository/runtime_readiness_gate; Core main/kache/StrategyConfigFn; Bridge pipe_handler/cliente config; resolver profile LabV4. B5/B6. | O01–O05. OBSERVE sin execution, SIMULATED con aplicación real en consumidores. |
| 3 · J reference/copy | MasterObservationFn/module.yaml, JournalObservationServiceV2/TradeJournalRepository, legacy journal discriminator, ExecutionPlannerFn/MM seam/Bridge. B7/B8. | J01–J06. Owner único, gates OPEN/management, simulador y recovery. |
| 4 · L proyección/LAB | SDK journal outbox/history tx helper; labv4-worker; front/composable/Hasura sólo delta demostrado. B9. | L01–L05. Historia acumulada,4curvas/2rankings/cohortes/UI pinneados. |
| 5 · F producer/E2E | Symphony echo-handoff/registry-postgres/entry point candidate-local desde lab-v4/shot4-symphony actualizado, hija propuesta feature/lab-v4-ingestion-v2. B10. | F01–F03. Adapter durable; AUTH separado. Sin campaña ni merge/deploy Symphony compartido inferido. |
| 6 · entrega | Candidate y evidence index por capacidad; integración normal de incrementos completos al destino The Lab con A4. | SHAs Echo/Symphony/SDK/module/front/SQL/metadata, diff integrado/no integrado, gates y cleanup; handoff fresco a QA. |

No código O/J/L parcial dentro de early merge E. Cada integración posterior preserva E y commits ajenos; si un incremento está bloqueado, entregar exacto diff no integrado. Ownership exclusivo por archivos durante incremento. Una contradicción nueva de fuente produce PLAN_CONFLICT concreto y corrección mínima técnica compatible, no rediseño entero; decisión de producto incompatible requiere Owner con evidencia exacta. No nuevo proyecto.

### C3. Matriz de deltas y falsificación

Estado de todas estas pruebas en Shot1: **NOT_RUN**. Mocks sirven unitarios, jamás acreditan apply/journal/copy. Broker/provider sólo simulados.

| ID | Prueba y expected a falsificar | H reutilizados |
|---|---|---|
| O01 | Profile/grants/cuentas existentes; targets cliente alterados rechazados, sin account fake; CASN dos writers uno gana/otro412; key conflict409 | H05,H35,H43 |
| O02 | Publicación con consumidor detenido no READY; lookup tras apply y todos ACK exactos sí; OBSERVE produce0órdenes | H05,H06 |
| O03 | Crash apply/ACK/delivered; restart nuevo epoch; ACK viejo con timestamp mayor rechazado; renewal5s/expiry15s medidos | H06,H09,H10 |
| O04 | Lease/grant/head cambia entre admission/planner/Bridge, OPEN denegado; CLOSE reduce ciclo viejo; MODIFY aumenta riesgo bloqueado | H08,H09,H11 |
| O05 | Native gate con2runs/cuentas/versions no elige LIMIT1; engine snapshot y StateFun post-commit lookup reales | H06,H49 |
| J01 | Namespaces/cuentas/source instances comparten Magic/trade_id; sólo tuple exacta journaliza, ambigüedad unresolved | H01,H08,H11,H35 |
| J02 | Duplicate/payload cambiado/out-of-order/reconnect/close-before-open/gaps/correction; un journal hecho/seq y economía única | H10,H12,H14 |
| J03 | OPEN durante bulk/provision→journal al resolver, NOT_DISPATCHED_PRE_READY permanente; OPEN nuevo sí pasa policies | H07,H08 |
| J04 | LAB apagado, reference t_first_byte+60s, journal/copy funcionan; readiness≤45s desde commit con prerequisites propios | H07,H11,H46 |
| J05 |2execution con MM distinto y una policy denegada; sizing por cuenta, links exactos, P&L no sumado a reference | H11,H25,H49 |
| J06 | Broker aceptó/respuesta perdida, command key/lookup; UNKNOWN_OUTCOME sin segundo OPEN; legacy no duplica managed | H10,H12,H47 |
| L01 |2estrategias/cuentas/roles intercaladas, batch pequeño, una inválida; delivered sólo procesados, N+1 contiene N | H03,H10,H14,H34 |
| L02 | Summary/movements/costes desconocidos/multidivisa/Q ausente; no fills/FX/riesgo inventados | H15–H19,H21–H23,H26 |
| L03 | Forge previo+Echo posterior/carry; overlap sin crosswalk no unión; pre/post y AS_KNOWN correctos | H13,H20,H24 |
| L04 | N+1 durante compute/cohort; token viejo; cohort completo, bundleN sigue N en todos sus endpoints | H27–H34,H36,H42 |
| L05 | Browser real, selectores independientes, GraphQL/actions aislados, errores/cursors/cancel; sin latest fallback | H36–H43 |
| F01 | PG store real, producer restart persist/POST/receipt; digest común, key mismatch conflicto; error update propagado | H01,H02,H10,H26 |
| F02 | Artefacto autorizado+lineage→DTO→HTTP→journal simulador→history→UI; counts/digests fuente conciliados | H01,H05–H07,H11,H13,H36–H41 |
| F03 | Cold build ambos consumers mismo shared-analytics pin/sum; golden independiente, wrappers sin fórmulas duplicadas | H27–H33 |

Mantener49 filas H individuales: H01–H14 identidad/operación/evidencia; H15–H26 economía/precisión; H27–H33 ranking/shared; H34–H35 worker/SQL; H36–H43 lectura/UI/auth; H44 historia larga; H45 catálogo20k/prepare; H46 backpressure; H47 guard; H48 cleanup; H49 nativo. QA-01 coverage separado, nunca H50/denominador50. Código nuevo/cambiado≥95% por paquete y agregado ponderado, rutas críticas completas, race tests pertinentes. Cobertura heredada se informa aparte.

H45 mantiene prepare p95≤2s: ~8.4–10s histórico y floorCOPY~3–3.5s son FAIL histórico, no presupuesto relajado. No abrir optimización aparte; toda degradación atribuible se corrige en Shot4. H44 budgets y H completo original siguen vigentes en superficies afectadas. No ejecutar suites no afectadas por cada commit; sí regresión completa de superficies afectadas antes de certificación.

### C4. Shot 3 — QA adversarial independiente

GLM-5.3-Flash Max LOCAL en sesión fresca, sin autoría de implementación. Verifica SHA integrado/candidate, árbol/build/SQL/modules/front/metadata. No acepta resultados de Shot2 como expected: deriva oráculos desde source artifacts/raw facts, sin importar fórmulas/helpers bajo prueba. No modifica producto para pasar; tests/fixtures propios aislados permitidos.

Intenta falsificar auth/grants, replay, CAS/races/crashes, published-not-applied, incarnation/lease, source confusion, pre-ready, duplicate journal/P&L, insuficiencia económica, N/N+1, cohort parcial y UI drift. Finding: {id,severity P0..P3,requirement,source_sha,owner_module,repro,fixture_digest,expected,actual,first_divergence,evidence_refs,fix_acceptance,attribution new_delta|historical|regression}. P0 riesgo nuevo/crossscope/duplicación órdenes; P1 pérdida de historia/receipt/config falsa/economía incorrecta; demás por impacto concreto.

Salida:49H + nuevos casos + QA01 separado, findings reproducibles y paquete Shot4. BLOCKED_EXTERNAL sólo caso dependiente y recurso concreto; nunca convierte casos restantes en PASS. Sin fixes/merge de producto en Shot3.

### C5. Shot 4 — fixes y certificación final

GLM-5.3-Flash Max LOCAL corrige findings atribuibles al delta y regresiones, conserva repros y prueba criterios. Integra sólo incrementos completos y registra SHA final real. Después otra instancia GLM-5.3-Flash Max LOCAL, fresca y sin autoría del producto/fixes, verifica SHA final y repros con expected propio. Es parte de Shot4, no Shot5.

Si persiste FAIL, corregir/reverificar dentro del mismo shot con alcance explícito; no certificado verde ni bucle indefinido. Si no logra terminar, entregar pendientes reales al finalizar los cuatro shots. Certificación funcional requiere cero P0/P1 nuevo abierto. Independencia no disponible se informa, no se suplanta con auto-revisión.

Estados por caso: PASS probado; FAIL producto; NOT_RUN no ejecutado; BLOCKED_EXTERNAL recurso/permiso concreto e intento sanitizado. Global distingue funcional harness, autenticidad, H45/QA01 históricos y toda falla nueva. Certificación local no autoriza deploy/cutover/runtime merge.

### C6. Recursos, seguridad y evidencia

Excepción externa conocida AUTH_FORGE: falta copia inmutable autorizada de trade list auténtica con lineage/exporter/build/digests. No campaña SQX/MT5 adicional, reinicio Forge ni extracción tocada para obtenerla. No Forge DEV inventado. Otros recursos sólo externos tras demostrar inaccesibilidad necesaria (módulo privado frío/permiso/browser/copia). Installer sin implementar, timeout producto, test omitido o harness mal configurado son FAIL/NOT_RUN, no externos. Continuar gates independientes.

Manifest delimita PG/ETCD/Kafka/StateFun/Hasura/store/providers simulados propios, endpoints/puertos/account namespaces, guard allowlist antes red y sin fallback DEV/PROD. H47/H48 pre/post inventarios, cancelación y teardown por ownership exacto, sin killall/delete amplio. Artefactos voluminosos fuera del vault, refs/digests/SHAs dentro; sin credenciales. PROD read-only no obliga consultarlo; Shot1 no lo hizo.

### C7. Revisión del design freeze

Revisión documental por autor Shot1, no QA independiente ni pruebas de ejecución. Se contrastaron símbolos/contratos en los SHAs A. Una hipótesis de divergencia del digest Forge se descartó al leer helpers equivalentes; se conserva la receta existente.

| Criterio Owner | Evidencia |
|---|---|
|1 baseline | A1/A2,3HEAD remotos/locales y limpieza |
|2 deltas reales | G01–G16 con fuente/owner/estado y B |
|3 rama/early merge | D25/A4, sin runtime deploy |
|4 endpoint | B2–B4/E/E01–E12 |
|5 readiness | B5/B6 consumers/apply/checkpoint/epoch/lease |
|6 reference/journal/copy | B7/B8/B11, último salto/recovery |
|7 reuse LAB | B9/G13/G14, matemática V4 intacta |
|8 fallos/idempotencia | B4/B6/B8/B9/B12 y C3 |
|9 cuatro shots | C2/C4/C5/D26 |
|10 paquetes GLM | D tres prompts completos y E ejemplos |
|11 persistencia master | Change_log consolidado, readback/validación/commit/push de documentos |

Veredicto: **ECHO_INGESTION_V2_GOD_DESIGN_READY_FOR_GLM**, sujeto a la verificación de persistencia master registrada en change_log. Sin blocker de diseño pendiente. AUTH_FORGE limita autenticidad futura, no freeze. Ningún gate funcional PASS por esta declaración. Siguiente acción: D2, Shot2; no iniciado en Shot1.


## Fuentes

- Mandato Owner 2026-10-26; [[F — Decision Register]] D25/D26.
- [[A — Source Baseline and Branch Integration]] contiene los SHAs y localizadores efectivos.
- Contratos compatibles de `10-projects/Echo/The Lab/V4 — Runtime Integration/` y [[Echo + Echo Forge — Environment Contract]].
