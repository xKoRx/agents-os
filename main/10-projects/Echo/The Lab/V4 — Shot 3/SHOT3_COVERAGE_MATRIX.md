---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[0 — Submanager State]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-21"
updated: "2026-10-21"
---

# SHOT3_COVERAGE_MATRIX

## Propósito

Trazar G1–G11, T01–T45 y C01–C06 al candidato `61ac1f720d07513e48b0310b84b5b415b80ff48f`. Ejecutor GPT-6.1-Sol / reasoning high. Esta matriz distingue capacidad ausente, defecto ejecutado y caso excluido; no es certificación de I1.

## Contenido

**AUDIT BLOCKED; PRODUCT INCOMPLETE.** Axx/Mxx son repros de `outputs/SHOT3_AUDIT_EVIDENCE/repros/`, Oxx son oráculos independientes de aritmética, y «Source» significa inspección del SHA, no prueba conductual. Estados PASS_EXECUTED sólo cubren la superficie nombrada. Un gate parcial con un test verde no queda aprobado. Casos dinámicos de seguridad: NOT_RUN — harness safety restriction.

### Gates

| ID | Implementación | Prueba/evidencia | Estado observado |
|---|---|---|---|
| G1 | Parcial: contrato/servicio, sin handler real | 7 tests; A01/A02/A14/A16 | FAIL_EXECUTED + MISSING_IMPLEMENTATION; seguridad NOT_RUN harness safety restriction |
| G2 | Tablas/grano; sin adapters por Operation | A01/A02/A07/A08/A18; O01–O03/O09 | FAIL_EXECUTED + MISSING_IMPLEMENTATION |
| G3 | Sin perfiles V4/métricas | Oráculos O04/O05; no implementación que ejercitar | MISSING_IMPLEMENTATION |
| G4 | Metadata parcial; sin selección/etapas | A05/A12; source servicio | FAIL_EXECUTED + MISSING_IMPLEMENTATION |
| G5 | CAS/receipts parciales; sin worker | A09/A13/A14/A15/A17/A21 | FAIL_EXECUTED + MISSING_IMPLEMENTATION |
| G6 | Sin front/metadata V4 | Delta Git y búsqueda consumidores | MISSING_IMPLEMENTATION |
| G7 | Sólo DDL portfolios | Oráculos O07/O08; source070 | MISSING_IMPLEMENTATION |
| G8 | Sin adapter/copia V4 | Búsqueda source; no fixture auténtico | MISSING_IMPLEMENTATION |
| G9 | 071 ledger; legacy consumidores vivos | TestLabV4RetirementSafeByDefault; M02/M03 | Parcial PASS_EXECUTED; gate MISSING_IMPLEMENTATION |
| G10 | Sin worker/capacidad | Source y evidencia de ejecución | MISSING_IMPLEMENTATION + EVIDENCE_GAP |
| G11 | Sin recorrido Forge V2 | Sin artefacto auténtico v2 ejecutable | MISSING_IMPLEMENTATION; NOT_RUN integración física |

### Casos T

| Caso | Implementación | Prueba/evidencia | Estado observado |
|---|---|---|---|
| T01 | Summary viable; terminal movements roto | A01 y TestLabV4IngestionPostReplayConflictCAS | FAIL_EXECUTED parcial |
| T02 | Falta adapter económico multi-entrada | A02; O01–O03=11/10/2R | FAIL_EXECUTED + MISSING_IMPLEMENTATION |
| T03 | Falta adapter fills correlacionados | Source runtime sin delta | MISSING_IMPLEMENTATION |
| T04 | OPEN un movimiento válido; curva ausente | A09/A18; sin worker | FAIL_EXECUTED + MISSING_IMPLEMENTATION |
| T05 | Falta adapter de ciclo/reentrada | Source runtime sin delta | MISSING_IMPLEMENTATION |
| T06 | Falta muestra/cobertura y adapter rechazo | Source + M02/M03 | MISSING_IMPLEMENTATION |
| T07 | Falta atribución correlacionada; FIFO antiguo | O09=5/O10=15, sólo oráculo | MISSING_IMPLEMENTATION |
| T08 | Falta Forge auténtico v2 | M01; no fixture genuino ejecutado | MISSING_IMPLEMENTATION / NOT_RUN |
| T09 | run_mode persistido, adapter ausente | TestLabV4IngestionMovementsAndAnalytic EXACT_REPLAY | Parcial PASS_EXECUTED; MISSING_IMPLEMENTATION |
| T10 | Receipt secuencial sí; carrera/UNCHANGED no | A14/A15, suite entregada | FAIL_EXECUTED |
| T11 | Conflicto secuencial sí; scope recurso incorrecto | Suite entregada y A21 | FAIL_EXECUTED parcial |
| T12 | CAS concurrente sí | A13 y concurrency-race.json | PASS_EXECUTED servicio; sin HTTP v2 |
| T13 | PUT snapshot sí; inmutabilidad rota | A05/A09/A17 | FAIL_EXECUTED |
| T14 | No publicación worker V4 | Source lab-worker | MISSING_IMPLEMENTATION |
| T15 | No claim/lease/fencing V4 | Sólo DDL070 | MISSING_IMPLEMENTATION |
| T16 | Historias separadas; no selección/derivados | Servicio y DDL069 | MISSING_IMPLEMENTATION; NOT_RUN recorrido completo |
| T17 | No selección segmentos/continuidad | Source | MISSING_IMPLEMENTATION |
| T18 | Sin consulta cohorte/temporal/as_of | Source | MISSING_IMPLEMENTATION |
| T19 | Fechas separadas en DTO; PUT roto | A05 | FAIL_EXECUTED + MISSING_IMPLEMENTATION |
| T20 | Riesgo ausente aceptable en summary; perfil inexistente | Suite entregada; M03 | Parcial PASS_EXECUTED; MISSING_IMPLEMENTATION |
| T21 | Sin algoritmo causal V4 | O04=10100, sólo oráculo | MISSING_IMPLEMENTATION |
| T22 | Sin algoritmo causal V4 | O05=10098, sólo oráculo | MISSING_IMPLEMENTATION |
| T23 | Sin perfil/DD V4 | Source worker/analytics | MISSING_IMPLEMENTATION |
| T24 | Sin perfil/estado capital agotado calculado | Sólo enum DDL070 | MISSING_IMPLEMENTATION |
| T25 | Sin catálogo métricas V4 | Source | MISSING_IMPLEMENTATION |
| T26 | SQL suma monedas distintas | A08 | FAIL_EXECUTED |
| T27 | Sin adapter y comparación copia | Source | MISSING_IMPLEMENTATION |
| T28 | Sin adapter/contexto comparable/calculador | A06; Source | FAIL_EXECUTED + MISSING_IMPLEMENTATION |
| T29 | Estado historia RETIRED en DDL; sin lifecycle usable | Source | MISSING_IMPLEMENTATION |
| T30 | Sólo DDL portfolio | O07/O08=6000/4000, sólo oráculos | MISSING_IMPLEMENTATION |
| T31 | Sin composición/UI retrospectiva | Source | MISSING_IMPLEMENTATION |
| T32 | Coverage JSON sin análisis/lectura V4 | A05; Source | MISSING_IMPLEMENTATION |
| T33 | Controles source leídos; sin verificación dinámica | Restricción explícita del harness | NOT_RUN — harness safety restriction |
| T34 | Upgrade preserva historia; sin migración proyección/adapters | M01–M03 PASS; M04 FAIL | FAIL_EXECUTED parcial + MISSING_IMPLEMENTATION |
| T35 | POST tras PUT queda en conflicto y conserva head | TestLabV4IngestionPostReplayConflictCAS | PASS_EXECUTED servicio |
| T36 | Sin prueba dinámica writer ajeno | Restricción explícita del harness | NOT_RUN — harness safety restriction |
| T37 | No publicador/manifiesto selección+portfolio | Source | MISSING_IMPLEMENTATION |
| T38 | No coalescing/dirty jobs | Servicio sin enqueue ni worker | MISSING_IMPLEMENTATION |
| T39 | Exactitud SQL correcta; servicio terminal roto | A18=114; A01 | FAIL_EXECUTED servicio; PASS_EXECUTED SQL |
| T40 | Sin curva R por parciales | O11=0.4R, sólo oráculo | MISSING_IMPLEMENTATION |
| T41 | Sin start flat de portfolio | Source | MISSING_IMPLEMENTATION |
| T42 | PUT revisiona; artefactos/metadata incompletos | A05/A17 | FAIL_EXECUTED |
| T43 | Sin métricas window_local/curve_running | Sólo enum/columnas070 | MISSING_IMPLEMENTATION |
| T44 | Sin selección/segmento e indicador discontinuidad | A06; Source | MISSING_IMPLEMENTATION |
| T45 | Sin paneles rendimiento/copia V4 | Source | MISSING_IMPLEMENTATION |

### Casos C añadidos por freeze V3

| Caso | Implementación | Prueba/evidencia | Estado observado |
|---|---|---|---|
| C01 | 067–071 + tracking/ledger; sin retire real | Siete originales pertinentes; M01 rollback 069 real; M02 sin 066; M03 conserva datos; M04 pierde fills | FAIL_EXECUTED en down 067; otros subcasos PASS_EXECUTED; retiro pendiente |
| C02 | Recetas presentes; sin perfil/consumer real | TestLabV4PlatformKindsIdentityRecipes y analítica/PUT; Source | Parcial PASS_EXECUTED; prueba T end-to-end MISSING_IMPLEMENTATION; ataques de mutación NOT_RUN harness safety restriction |
| C03 | DTO/tag/evidence y columnas; sin captura MM | Rechazo tag sin evidencia original; Source MM sin delta | Parcial PASS_EXECUTED; sello causal/método acreditado y caso multi-entrada MISSING_IMPLEMENTATION |
| C04 | Grano dual parcial; no atribución por Operation | A01/A02/A07/A08/A18; O09/O10 | FAIL_EXECUTED; adapter/reconciliación MISSING_IMPLEMENTATION |
| C05 | Sink write-ahead, revisión mutable y metadata incompleta | A03–A05/A09/A17/A22; pinned-revision.json | FAIL_EXECUTED; crash físico y protocolo mantenimiento NOT_RUN; sin GC concurrente implementado |
| C06 | Caps semánticos en DTO; sin handler128MiB | Source contracts; insertion sort; sin benchmark real | MISSING_IMPLEMENTATION + EVIDENCE_GAP; NOT_RUN benchmark completo |

### Capacidad faltante consolidada y límites

M01: HTTP/Forge auténtico. M02: Q_i causal, economía por Operation y adapters journal/runtime/backtester/proyector. M03: worker/cuatro perfiles/métricas/publicación/cola. M04: selección/dashboard/metadata/read models/ejecución. M05: portfolio estático y capital. M06: sustitución legacy/cutover genérico. E01: capacidad/cobertura/bootstrap allowlist. E02: verificación dinámica de seguridad excluida. La ausencia se agrupa por causa, sin repetir supuestos resultados conductuales.

Las suites completas postgres/gateway y todo el monorepo son NOT_RUN bajo este alcance; se ejecutaron subconjuntos funcionales enumerados en el informe. Pruebas de seguridad E-04, filesystem traversal, namespace/writer ajenos y equivalentes no seleccionadas son NOT_RUN — harness safety restriction. Integración física Forge y benchmark no son PASS por fixture sintético ni por un DTO.

## Fuentes

[[SHOT3_ADVERSARIAL_REPORT]], [[SHOT4_EXECUTION_PACKAGE]], SPEC F.1/F.2, freeze tablas C01–C06; paquete externo `outputs/SHOT3_AUDIT_EVIDENCE/` con evidencia JSON y MANIFEST.sha256.
