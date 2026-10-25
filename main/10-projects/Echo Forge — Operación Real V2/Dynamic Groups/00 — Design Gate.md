---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-25"
updated: "2026-10-25"
---

# 00 — Design Gate

## Propósito

Congelar Shot 1 de **Dynamic Group Execution, Target Top X & Runtime Task Bindings**, iniciativa dentro de [[Echo Forge — Operación Real V2]]. No es un proyecto nuevo. Mandato del owner del 2026-10-25; Forge → Echo → The Lab conserva su visión permanente, pero este paquete modifica únicamente el diseño de Forge.

## Contenido

**Estado: revisión final del diseño en curso.** Todas las APIs nuevas se etiquetan PROPUESTO. Implementación, deploy y certificación física: NOT_RUN. Las pruebas de baseline no certifican las capacidades propuestas.

### Autoridad y corte

- **HEAD remoto verificado:** `xKoRx/symphony@dd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19`, `git ls-remote origin refs/heads/master`, 2026-10-25. Checkout local limpio `master@daded14cbe0bc85f6fafda8d079e94036f715b47`; no se movió. Auditoría desde exportación exacta `git archive` del HEAD remoto.
- **Dependencia de pruebas:** SDK exportado del commit requerido `c7f11496b6f681687c9e1e41a773a13295640351`; no se usó el checkout SDK local atrasado `c8559444`. `-mod=mod` sólo actualizó los archivos de dependencias de la copia desechable auditada, no los repos originales.
- **Runtime documentado, no reobservado hoy:** 0.3.2, source `619c3b6f`, manifest `daded14c`, w11 `561267ed-224b-48b5-a803-9f7665927998`, certificado histórico `ECHO_FORGE_FINAL_E2E_PASS`, 105/105 children y flota 4/4 según proyecto al 2026-10-19. No afirmar que dd4af7d esté desplegado.
- **Otras lanes:** existen worktrees de LAB Shot4 en `a0c68d1`; no son baseline master ni se tocaron. Los cambios remotos desde daded14c incluyen el kernel compartido de ranking y HTTP ingress V2; el segundo queda fuera del alcance.
- **IMOX:** se encontró la referencia técnica del 2026-10-24, pero no una nota canónica titulada exactamente `Estrategias IMOX — Forex y CFD con Echo Forge` en este vault. No se creó una entidad sustituta ni se inventarió un corpus no entregado.

### Índice de entregables

| Requisito de entrega | Autoridad |
|---|---|
| A Executive Architecture Report | [[01 — Executive Architecture Report]] |
| B Capability Inventory | [[02 — Capability Inventory]] |
| C Target Architecture + ADRs | [[03 — Target Architecture and Decisions]] |
| D Functional Specification | [[04 — Functional Specification]] |
| E Technical Specification | [[05 — Technical Specification]] + `group-target.schema.json`, `examples/` |
| F Implementation Plan | [[06 — Implementation Plan]] |
| G Adversarial Plan | [[07 — Adversarial Plan]] |
| H Fix & Certification Plan | [[08 — Fix and Certification Plan]] |
| I Traceability Matrix | [[09 — Traceability Matrix]] |

El proyecto padre conserva el estado y la secuencia de shots. Los documentos son contratos y paquetes referenciados; no crean un segundo planificador.

### Evidencia ejecutada

`GOWORK=off go test -mod=mod ./core/domain ./core/runtime ./adapters/wfm/binding ./adapters/apply-selected-run/binding -run 'Test(Build.*Ranking|.*SelectionSnapshot|.*StageExecution|.*ConfiguredPeriod|.*TaskName|.*Score|.*Parse|.*Period|.*Config)' -count=1 -timeout=120s`, desde el módulo `sqx` de la copia. Resultado: PASS en los cuatro paquetes (0.076s, 0.076s, 0.093s, 0.053s). Es una selección dirigida, no suite completa ni coverage del cambio propuesto. El primer intento sin `-mod=mod` pidió actualizar go.mod; se conservó el repo original intacto.

Inspeccionados: configuración/validadores; root/group; fuentes/rankings/selección; Campaign; identidad/StageExecution; WFM parser/evidence/exporters; Apply; CFX parser/worker; MT5 config/INI/fidelity; pruebas asociadas; reportes y contratos seleccionados. No inspeccionados físicamente: flota actual, data feeds, CFX del owner, MT5 interactivo, DBs/ETCD/MinIO vivos. No se ejecutaron campañas, backtests, releases, migraciones ni conexiones operativas.

### Hallazgos que acompañan el freeze

F01: group source actual toma TopProjection previamente recortado; no demuestra agotamiento del universo original. F02: despachadores raíz/group difieren. F03: Apply Java toma `periods[size-1]` sin contrato de período común. F04: fechas CFX/MT5 son date-only y no prueban equivalencia DST por sí mismas. F05: snapshots V1 tienen fuentes y campos Builder específicos. F06: watcher antiguo puede descartar campos JSON nuevos. F07: `evaluate_strategy` es shadow y su handler descarta el resultado; requiere publicación durable para la muestra sin motores físicos. Todos tienen dueño y pruebas en el plan; ninguno se disfraza de capacidad implementada.

## Fuentes

[[Echo Forge — Operación Real V2]], [[Echo — Producto Integrado]], [[Echo + Echo Forge — Environment Contract]], [[SQX — BR H1 LONG — Grupos, Builders y continuidad Forge-Echo]]. Código y símbolos en [[02 — Capability Inventory]].
