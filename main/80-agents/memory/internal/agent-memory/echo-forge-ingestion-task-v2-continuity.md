---
type: agent_memory
schema_version: 1
scope: project
created: '2026-10-27'
updated: '2026-10-27'
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

Programa `forge-echo-ingestion-task-v2`, task `echo_ingestion_v2`, en Echo Forge. Exactamente cuatro shots: GOD diseño; GLM-5.3-Flash Max LOCAL/ZCode implementación; GLM LOCAL fresco QA; GLM correcciones y otro verificador fresco dentro Shot 4. El manager adjudica. No cierre Agents-OS ni feedback/L0/L1 sin orden explícita.

**Estado actual: SHOT2_INCOMPLETE.** Shot 1 sigue DESIGN_FROZEN. Se recibió el candidato Symphony `07c914251760a938293b7fa7fe4e6d7b4d330640` y Echo `2c66e9402ba96ff354681552587c895ec92f4a28`; refs y ancestry verificados por API. No se adjudicó FORGE_ECHO_TASK_IMPLEMENTED_LOCAL. La revisión de fuente encontró defectos implementables M01–M09, descritos en [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]]; no fue QA runtime. Próximo ejecutor: el mismo GLM LOCAL termina Shot 2, después se decide admisión a Shot 3. No repetir arquitectura ni crear otro shot.

Bases intencionales permanecen Symphony `22f337ca434549c492b2d402fd158e23ac4758a8` y Echo `f93cd4f80085e328f9176c1215e42e6c8e0b2404`. Continuar desde los candidatos, sin reset ni vuelta a una base anterior. Contracts `v3/sdk/contracts/v0.0.1-forge-ingestion-task.1` apunta a Echo `2c66e940…`, subtree `0c727f10288cac24bdd2f9d367eeb218d5315006`; es inmutable. Correcciones del contrato exigen nueva versión de prueba y pins/cold builds efectivos. SDK dedicado `c7f11496b6f681687c9e1e41a773a13295640351` es dato declarado por GLM, no checkout inspeccionado desde CLOUD.

A INCOMPLETE; B/C/D NOT_RUN según D. Coverage nuevo ≥95% y goldens pendientes. D exige intento read-only auténtico; no declarar bloqueo externo por tiempo consumido. E NOT_AUTHORIZED. Source/runtime/QA independientes conservan sus fronteras.

## Autoridades y límites

TARGET: [[B — Frozen Design]] y [[Forge Task — Contract Addendum]]. A/Contract Source Review describen la base investigada; C gobierna los cuatro shots. [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT2 — Local Implementation Mandate|SHOT2 — Local Implementation Mandate]] contiene la continuación vigente de Shot 2 y el mandato original. [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]] conserva la entrega inicial del ejecutor y la adjudicación posterior; no confundir su texto histórico de entrada a QA con el siguiente paso vigente.

Folder opaco; PG identidad/control, Mongo evidencia, MinIO bytes; selección exacta sin latest. REGISTER_ONLY; REQUIRED/IF_AVAILABLE/NONE. Definiciones/identidades acreditadas, source metrics separadas de Lab, historia real por operación y scope. Recovery desde manifest PG, receipt completo/refs atómicos, resultado Foundation durable y data_only sin SQCLI. No reinterpretar datos para acomodar el candidato.

Runtime/Lab paralelo y Dynamic Groups son otros workstreams, sin merge global. Sólo ports mínimos/colisiones ya previstos. No PROD, flota, campañas, trading ni migraciones compartidas.

## Incidente reportado y rectificación histórica

GLM reportó DROP/repoblado parcial del template compartido `lab-v4-shot4-20261021/pgdata`, DB `echo_labv4_s4`. Alcance/restauración no verificados desde CLOUD. El siguiente ejecutor acredita ownership/paths/PIDs/DB y aislamiento efectivo de su harness2. No queda autorizado a reconstruir/borrar el template compartido; prepara recuperación preservadora y devuelve sólo la acción fuera de alcance si exige autorización. No cerrar el incidente por considerarlo desechable.

La antigua clasificación stale/duplicado se rectificó; GLM reporta haber corregido su memoria local conservando la traza. El programa anterior Ingestion V2 sigue como dependencia. El Owner autorizó explícitamente la publicación íntegra de este paquete en Agents-OS público. El despacho se carga desde commit remoto exacto, sin ZIP. Agents-OS siempre master directo con protección de concurrencia.

## Señales de carga

Cargar para continuar/revisar esta task y sus gates. No sustituye la continuidad de campañas, Runtime ni Dynamic Groups.

## Próxima acción

Ejecutar la continuación vigente de [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT2 — Local Implementation Mandate|SHOT2 — Local Implementation Mandate]] con el mismo implementador LOCAL, cerrar M01–M09 y devolver un candidato completo con evidencia. No avanzar a Shot 3 con wiring/mapper/harness pendiente. Esta superficie no expone despacho directo ZCode/GLM. Mantener el bootstrap de la sesión; no cierre ni feedback.
