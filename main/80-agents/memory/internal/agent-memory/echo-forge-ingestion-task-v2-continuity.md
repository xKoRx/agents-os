---
type: agent_memory
schema_version: 1
scope: project
created: '2026-10-27'
updated: '2026-10-28'
area: '[[Echo]]'
project: '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
application: null
entities: []
related:
- '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
- '[[Echo — Producto Integrado]]'
aliases: []
confidence: verified
memory_state: active
continuity_key: project/echo-forge/ingestion-task-v2
supersedes: null
superseded_by: null
load_policy: Cargar al continuar la task nativa Forge Echo Ingestion V2 o revisar sus shots y gates.
indexable: true
index_priority: high
tags:
- kind/agent-memory
- scope/project
---

# Echo Forge Ingestion Task V2 — continuidad activa

## Continuidad

**SHOT4_READY_WITH_ADJUDICATED_FINDINGS.** Shot 3 recibido el 2026-10-28 con hallazgos y alcance parcial. Orden Owner: exactamente cuatro shots; no otra vuelta Shot 2/3 ni Shot 5. Shot 4 contiene correcciones completas y después otro GLM LOCAL fresco sin autoría que verifica el candidato final. El Manager adjudica contra evidencia, sin PASS forzado.

Programa `forge-echo-ingestion-task-v2`, task `echo_ingestion_v2`, dentro de Echo Forge. La antigua clasificación stale/duplicado fue rectificada: es distinto de Ingestion V2 cerrado, que permanece como dependencia. Diseño B/addendum congelados; no reiniciar arquitectura ni requerir ZIP.

## Candidato y evidencia

Refs remotas comprobadas intactas: Symphony `feature/forge-echo-ingestion-task-v2@7731cb844446062f861f04d19dea60a34d425373`; Echo `feature/forge-task-contract-v2@24af786232fa362cc1599df1b9d90b1c8347b557`. SDK esperado `c7f11496b6f681687c9e1e41a773a13295640351` por replace ../../sdk; comprobar resolución efectiva local. Contracts .2 objeto `7496b05b6932517e1d51b757c42cf72dad2cc1bd` → Echo candidato, subtree `cb88aece4f04b648fd724568de3823604dc064ab`; tags .1/.2 inmutables. Si contracts cambia, nueva versión disponible y pins/cold builds; no mover tags.

E recibido en Agents-OS `124430da4deb8eb95e3121f970ea366adcffd289`, blob `a56a34865f3ccccb8a80a8c28e0c58e01641df7e`. Adjudicación vigente en [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]]: nueve findings obligatorios. 05/06/08 P1 de migración/bootstrap, Decision y lifecycle; 02/07 P1 de integridad; 03/04 P2 funcional/contrato; 01/09 P2 test/cobertura. La corroboración CLOUD fue acotada a fuente/evidencia; repros y runtime son del auditor LOCAL, no reejecutados aquí.

A INCOMPLETE; B/C E2E NOT_RUN; D BLOCKED_EXTERNAL con observaciones auténticas parciales reportadas, dataset aún pendiente; E release NOT_AUTHORIZED. 47,1%/80,4% de E quedan reportados pendientes de perfiles/scope/unión; ≥95% rige código nuevo incluida funcionalidad añadida a archivos existentes. M04 sólo oráculos TradeList ejecutados; M08 sólo contratos/servicio probados, Lab pendiente.

## Autoridades y límites

Despacho vigente: [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]]. B/addendum son la SPEC; C conserva cuatro shots; D/E mantienen historia y evidencia. QA-S3-05 exige boot normal data_only y upgrade desde 018 antigua registrada mediante ruta aditiva; el ledger no tiene checksums. QA-S3-08 exige Generic y Group completos, no sólo un span. QA-S3-07/04 exige versión/key por item y los tres modos, antes de devolver work-item refs. Preservar tests QA/hashes y promover expected correcto; un test FINDING verde puede confirmar el defecto.

Gate D requiere dataset PG/Mongo/artifacts con lineage; ETCD legacy o ausencia de tablas V2 sólo describen despliegue. Reconexión RO soportada permitida; falta concreta queda documentada y no bloquea A/B/C con fixtures. No PROD/flota/campañas/trading/migraciones shared, sin Forge DEV inventado ni merge general Runtime/Dynamic Groups.

## Incidente reportado

Template compartido `lab-v4-shot4-20261021/pgdata` excluido de pruebas, cleanup, stop y restauración. E afirma ninguna conexión/escritura de QA a ese PG; el Manager no certifica su impacto/restauración. Reutilizar harness2/qa-stack sólo tras verificar ownership y targets actuales. Garage es sustituto S3 documentado, no MinIO real.

## Señales de carga

Cargar al ejecutar/revisar Shot 4, sus findings y gates. No sustituye continuidad de campañas ni otros workstreams. Agents-OS master directo con protección de concurrencia; autorización documental pública persiste.

## Próxima acción

Ejecutar [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]] con GLM-5.3-Flash Max LOCAL/ZCode corrector. Crear F — Final Certification con candidato, fixes/tests/hashes/coverage/gates y handoff al verificador fresco dentro de Shot 4. Esta superficie no dispone de despacho ZCode directo; entregar launcher exacto al Owner. Si el cierre sigue bloqueado, informar alcance/causa concreta sin inventar PASS ni otro shot. Agents-OS abierto, sin feedback/L0/L1 ni cierre.
