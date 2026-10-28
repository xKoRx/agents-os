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

**SHOT3_READY_WITH_KNOWN_GAPS.** Orden explícita del Owner del 2026-10-27: pasar a pruebas adversariales independientes, sin más iteraciones de Shot 2. Se congela la segunda entrega como candidato para QA. La instrucción anterior de continuar Shot 2 está supersedida en secuencia; sus requisitos y findings históricos siguen como expected/antecedentes. No se concede PASS a los gates ni al 95% por esta admisión.

Programa `forge-echo-ingestion-task-v2`, task `echo_ingestion_v2`, dentro de Echo Forge. Exactamente cuatro shots: 1 diseño (completado/frozen); 2 entrega de implementación (recibida/congelada con brechas); 3 GLM-5.3-Flash Max LOCAL/ZCode fresco QA sin autoría; 4 correcciones y otro verificador fresco dentro del mismo shot. No Shot 5, no nueva vuelta Shot 2. El manager adjudica; no cierre Agents-OS ni feedback/L0/L1 sin orden.

## Candidato y evidencia

Refs remotas comprobadas: Symphony `feature/forge-echo-ingestion-task-v2@7731cb844446062f861f04d19dea60a34d425373`, tres commits sobre `07c914251760a938293b7fa7fe4e6d7b4d330640`; Echo `feature/forge-task-contract-v2@24af786232fa362cc1599df1b9d90b1c8347b557`, uno sobre `2c66e9402ba96ff354681552587c895ec92f4a28`; sin divergencia. Las bases históricas intencionales siguen siendo `22f337ca434549c492b2d402fd158e23ac4758a8`/`f93cd4f80085e328f9176c1215e42e6c8e0b2404`.

Contracts `.2`: tag objeto `7496b05b6932517e1d51b757c42cf72dad2cc1bd` → Echo `24af7862…`, subtree `cb88aece4f04b648fd724568de3823604dc064ab`, go.sum `h1:t60eoyOjwkkgDNxzkPwLvXYLgf/dFW4xwLuazfvx3u8=`. .1 no se movió. Ambos tags son inmutables. SDK esperado `c7f11496b6f681687c9e1e41a773a13295640351` por replace ../../sdk; QA confirma resolución/cold builds reales.

M01–M08 corregidos es claim de GLM a confirmar/falsificar, no PASS del manager. Coverage reportado 68,0% como promedio de 85 funciones no es cobertura ponderada validada; el piso de 95% sigue vigente. B/C con Temporal/worker/Lab reales y goldens pendientes. D: MCP expirado reportado, fuente auténtica no leída; 515 receipts de harness no la acreditan. E NOT_AUTHORIZED. La migración 018 cambió: QA debe probar Fresh y Upgrade desde la 018 original aplicada, sin reescribir ledger/checksums. No se realizó una nueva auditoría exhaustiva ni runtime desde CLOUD en esta admisión.

## Autoridades y límites

[[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT3 — Independent Adversarial QA Mandate|SHOT3 — Independent Adversarial QA Mandate]] es el despacho vigente; [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]] conserva ambas entregas, revisión histórica y decisión Owner nueva. [[B — Frozen Design]] y [[Forge Task — Contract Addendum]] mantienen la SPEC; [[C — Four Shot Delivery Plan]] mantiene exactamente cuatro shots. Cargar autoridades por commit remoto exacto, sin ZIP; bootstrap una vez por sesión.

La clasificación antigua de este despacho como stale/duplicado fue rectificada. Esta task nativa es un programa distinto de la integración Ingestion V2 cerrada, que permanece como dependencia; no volver a cancelar la task confundiendo esos linajes.

QA puede crear tests/fixtures/harness y levantar Temporal real en recursos propios; no modificar producto para producir PASS. Confirmar los oráculos O01–O24 y EC-01…08 con expected independiente. Findings van a Shot 4. Sólo riesgo grave concreto de ejecución insegura detiene el escenario afectado; los otros continúan.

No PROD/flota/trading/campañas/migraciones shared ni Forge DEV inventado. Runtime y Dynamic Groups son workstreams distintos, sin merge general. Owner autorizó publicar este paquete en Agents-OS público; cambios de docs master directo preservando concurrencia, sin secretos.

## Incidente reportado

GLM reporta que el template `lab-v4-shot4-20261021/pgdata` (puerto 56437) conserva siete bases y sólo `echo_labv4_s4` fue afectada; su harness2/pgdata (56438) sería propio. Esa acreditación es del ejecutor; CLOUD no certifica impacto/restauración. QA verifica ownership/targets antes de escribir y excluye el template de pruebas/cleanup. No se autorizó restaurar/borrar/detener recursos ajenos; no bloquear la auditoría en recursos propios por una restauración fuera de alcance.

## Señales de carga

Cargar al continuar esta task, despachar/revisar QA o preparar Shot 4. No sustituye continuidad de campañas, Runtime ni Dynamic Groups.

## Próxima acción

Ejecutar [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT3 — Independent Adversarial QA Mandate|SHOT3 — Independent Adversarial QA Mandate]] en GLM LOCAL fresco. Entregar E — Independent Adversarial Report con matriz de oráculos, evidencia, coverage/goldens y findings reproducibles para Shot 4. Esta superficie no expone despacho directo ZCode/GLM; el Owner inicia la sesión fresca con el launcher. No devolver el candidato a otra vuelta de Shot 2. Agents-OS sigue abierto.
