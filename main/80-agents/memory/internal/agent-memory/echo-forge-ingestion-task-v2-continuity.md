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

**SHOT4_BLOCKED; cierre final e integración E2E autorizados como candidato.** Owner 2026-10-28 pidió evaluar el retorno, terminar pendientes y entregar un prompt maestro para una última prueba con correcciones e incorporación a master o al Forge en pruebas. Se elige primero la combinación con el linaje E2E actual, con recursos propios. Continuar MISMO Shot 4: corrector/integrador completa; después verificador fresco sin autoría. Sin Shot 2/3/5 adicional, autocertificación ni cierre Agents-OS/feedback/L0/L1.

Programa forge-echo-ingestion-task-v2, task echo_ingestion_v2; distinto del anterior Ingestion V2 cerrado. Autoridad inmediata: [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]], sección «Cierre final e integración E2E»; B/addendum funcionales congelados. [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/F — Final Certification|F — Final Certification]] separa relato del corrector y adjudicación gerencial.

## Candidato y evidencia

Remote verificado: Symphony shot4/forge-echo-ingestion-task-v2@0417330a9d1ab9c8639d8f449f6d65548382f0e1, descendiente de d760dc3/7731cb8; SDK shot4/telemetry-optional-metrics@be85d144b7dfcc8e82941c2ee0de26082de60b85. Echo24af786232fa362cc1599df1b9d90b1c8347b557 y contracts .2 inmutables. La publicación ya no está bloqueada. F recibida en Agents-OS032095c6, blob1183723d5f0763f0414ef91af672b7ba12ecb931; runtime s4c y coverage siguen atribuidos al corrector, no re-ejecutados CLOUD.

El Owner dice verificador en background; F aún dice NO despachado, sin veredicto publicado en el corte. Recuperar ejecución antes de duplicar. Si escribió los tests/fixes de cierre, esa parte es corrector; mantener revisión posterior sin autoría.

## Pendientes y decisiones resueltas

QA-S3-09 abierta: 1499/1871=80,12% declarado por statements en Symphony; piso ≥95%, scope completo del código nuevo por repo, wiring/adiciones/SDK/Echo/integración visibles, legado ajeno separado. No promedio de funciones/bloques ni waiver por os.Exit. Con denominador fijo son279 statements adicionales hasta95%, pero recalcular tras cambios.

QA-S3-02 reabierta por source_instance_ref: wiring no carga instancia configurada; helper la fabrica por selector (task_output:<task> o FlowRun). B§6.1/8.3 exige config sellada. Corregir y probar identidad estable con misma evidencia en cuatro modos. RunRef=FlowRunRef universal requiere autoridad específica de productor, no cambio del fixture a conveniencia.

SDK require c7 y replace local no sellan fixbe85; resolver versiones/layout/bootstrap reproducibles y cold build. GateC positivo exige cuatro perfiles y dos rankings con evidencia suficiente: cero targets no cierra. Preservar insuficiencias/zero-history/coverage/timestamps honestos. Corrector completa esto antes del auditor.

## Destino E2E e integración

Remoto acreditado: cert-replay codex/forge-cert-replay-oneshot@36071d819b1532cade14ce06ad691d0d33856772, config w12R/dynamic-groups.v1; Symphony masterdd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19. Ingesta y cert divergen desde master. Refrescar/readback LOCAL antes de elegir target; commits/config no prueban runtime actual. Dispatcher compartido task_dispatch.go carece de echo_ingestion_v2; integrar raíz/grupo/anidado, sin perder legacy/carriers/accounting.

Migraciones de ambos linajes reutilizan prefijos017/018 con nombres distintos; ledger usa filename completo. No renumerar nombres ya aplicados ni borrar ledger; reconciliar ordered y probar fresh/upgrades/concurrencia en PG propias.

Echo master347eee8bdab7f7628629af6383d1e45520815abd ya contiene24af+118commits; no downgrade/remerge. SDK masterc8559444 es ancestro de c7 y be85 en la topología remota actual. Sellar tuple efectiva final; runtime/Go replace se comprueban LOCAL.

## Recursos y límites

Pila s4c previa declarada propia: PG56439, Mongo27418, Garage8345, ETCD7445/7446, Kafka19096/19097, Temporal7234/s4c, Gateway8125. Revalidar ownership/config antes de reutilizar; no intervenir otra sesión ni PG incidente lab-v4-shot4-20261021/pgdata. Nunca ejecutar teardown histórico/PIDs de cert-replay sin readback vigente.

Contacto Kafka DEV previo permanece atribuido; -1001 sólo acredita ausencia observable de offset en la consulta, no historial sin commits/efectos. No nuevas operaciones compartidas ni auditoría general.

Participar consumiendo outputs auténticos COMPLETED/sellados del E2E mediante lectura autorizada y nueva ejecución opt-in con recursos propios. No alterar specs en vuelo ni elegir latest. Si Mongo sigue inaccesible, D=BLOCKED_EXTERNAL concreto; no FULL_CERTIFIED con fixtures. E release/mutaciones compartidas NOT_AUTHORIZED.

## Señales de carga

Cargar para continuar cierre Shot 4, integrar al linaje E2E o revisar el candidato final. No sustituir otros workstreams. Agents-OS master directo, con concurrencia/readback y autorización documental pública vigente.

## Próxima acción

Ejecutar [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]], sección «Cierre final e integración E2E». Preparar candidato combinado y dejar terminadas correcciones, tests, coverage y evidencia; después verificar sin autoría. Publicar/participar en pruebas de forma opt-in. Promoción con efecto en master/release/infraestructura compartida sólo si esa acción concreta está autorizada; preparar primero el resultado revisable y dejar únicamente ese paso pendiente si corresponde.
