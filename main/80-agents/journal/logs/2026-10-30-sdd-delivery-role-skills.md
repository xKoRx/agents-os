---
type: change_log
schema_version: 1
scope: session
created: '2026-10-30'
updated: '2026-10-30'
entities: []
related: []
aliases: []
confidence: verified
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - tech/agents-os
area: '[[Personal]]'
project: '[[AGENTS OS]]'
---

# SDD — cuatro roles portables y mejora basada en evidencia

## Cambio

Crear cuatro skills federadas: `sdd-shot-1-implement`, `sdd-shot-2-verify`, `sdd-shot-3-correct` y `sdd-acceptance-gate`. Refactorizar `sdd-developer` como orquestador que enlaza sus procedimientos; añadir contrato común, runbook de mejora y adaptadores mínimos. Registrar los roles en INDEX e integrar `delivery_role` en bootstrap sin ampliar el always-load.

## Motivo

Mandato explícito del Owner del 2026-10-30: definir objetivos, criterio de actuación y evolución de los cuatro roles. Se distingue rol/skill/sesión/subagente/modelo y se conserva la autoridad principal para arquitectura y aceptación. No se promete transferir capacidad intrínseca de un modelo mediante instrucciones.

## Fuentes usadas

- Baseline leída: `xKoRx/agents-os master@c81b4e78acf3c9eabbcbcfd2f860aad030b6511d`; `sdd-developer`, `sdd-workflow`, bootstrap, índices y contratos de authoring/schema vigentes. Canonical blobs de helpers y templates verificados en la copia local.
- Contrato de scouts ya publicado y feedbacks recuperados en esta conversación: RIO Bus 2026-10-29 (bitácora/diagnóstico), CLF-Q03 2026-10-26 (identidad/evidencia), W1-n y W1-nR 2026-10-30 (efectos laterales de tests, lecturas truncadas, inventario y pruebas no equivalentes a integridad). Son antecedentes, no una auditoría nueva de esos productos.
- Documentación oficial ZCode Subagents consultada el 2026-10-30: subagentes sin subdelegación; herramientas custom exhaustivas; configuración de rol no sustituye permisos reales. Restricción registrada en el adaptador, no en la semántica portable.

## Resolución aplicada

Shot 1 entrega candidato, Shot 2 verifica independientemente sin reparar, Shot 3 corrige hallazgos adjudicados sin autoaceptarse y gate evalúa evidencia de la identidad final. `SDD_READY_FOR_ACCEPTANCE` es estado intermedio cuando falta autoridad de aceptación; no se convierte en PASS por confianza. El gate no es un cuarto shot correctivo ni autoriza producción.

Cada rol registra feedback por invocación con NO_FINDING válido y ownership limitado a su propia skill. Promoción en mantenimiento separado con evidencia, validación y revisión independiente; no hot-reload ni cambios retroactivos de criterios. Orquestador/contratos/runbook comunes siguen siendo responsabilidad del principal. Se reutilizan materialización, agent_run y authoring existentes; no se crea otro framework, plugin ni memoria paralela.

## Validación

- Ocho notas nuevas materializadas mediante `materialize_schema_note.py`; tres notas existentes actualizadas. No se publican scripts, templates ni schemas locales.
- Helpers sin modificaciones, cotejados por Git blob SHA: materializador `067dbef8…`, validador `7f6e9227…`, lint `d9c23424…`. Templates skill/runbook/doc/change_log cotejados contra los blobs canónicos recuperados.
- Lint `--strict` por los 11 paths del delta en workspace parcial; ERROR=0 / WARN=0; 11 notas escaneadas. Usa proyección semánticamente exacta del envelope/field_types/tipos afectados del schema canónico `27e59b8…`, no un schema alternativo publicado ni gate all-vault. Parse YAML estricto con rechazo de claves duplicadas.
- 68 comprobaciones automáticas estáticas PASS: estructura, referencias nuevas, routing, permisos, independencia, evidencia final, autoridad, feedback, mantenimiento y límites de scope. Son checks documentales, no ejecuciones de los agentes.
- Forward-test documental manual: 18 casos, incluyendo positivo/negativo/adyacente por rol y seis bordes (contexto no independiente, evidencia vieja, delta vacío, autorización ausente, autoedición y restauración posterior). Caso real histórico W1-n recorrido desde el feedback: verde técnico no prueba ausencia de escritura sellada; no se ejecutó ni inspeccionó nuevamente su código.
- Diagnóstico `quick_validate.py` NOT_RUN: no localizado bajo `/home/oai/skills`; además su perfil portable no es el gate aplicable al frontmatter local, según `skill-contract.md`. No se quitaron keys para fabricar compatibilidad.
- NOT_RUN: invocación de estos roles por modelos, ZCode en Hefesto/Daedalus, aislamiento real de permisos, Graphify/E2E y suites de producto. NOT_MEASURED: mejora de calidad, ahorro de tokens/cuota o latencia. El smoke local definido en role-adapters queda pendiente; publicación documental no lo certifica.

## Paths del delta

- Nuevos: cuatro `SKILL.md` federados, `sdd-developer/role-contract.md`, `sdd-developer/role-adapters.md`, `30-resources/runbooks/sdd-role-improvement.md` y este log.
- Modificados: `30-resources/agents/skills/sdd-developer/SKILL.md`, `80-agents/skills/INDEX.md`, `80-agents/skills/agents-os-bootstrap/SKILL.md`.
- Intactos: producto, skills de scouts, constitución, perfil, schema, templates, runtime local y credenciales. No se ejecuta cierre de sesión del Owner.

## Compartibilidad

Scope local; sin secretos, transcripts, dumps ni rutas privadas de máquinas en las nuevas instrucciones. Los adaptadores son enlaces de rol, no procedimientos duplicados.

## Rollback

Revertir sólo el delta de estos 11 paths preservando commits concurrentes y posteriores. Restaurar orquestador/routing/índice junto con las cuatro skills, contrato y adaptadores para no dejar enlaces rotos. No resetear master ni tocar producto. Publicación directa en master, sin ramas ni PRs, con verificación posterior del diff y los blobs.
