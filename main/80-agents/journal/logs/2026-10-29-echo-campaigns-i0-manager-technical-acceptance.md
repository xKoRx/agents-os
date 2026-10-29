---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures — Optimización de Campañas]]", "[[EF-CAMPAIGN-MODES-DESIGN]]", "[[EF-CAMPAIGN-MODES-I0-LOCAL]]", "[[EF-CAMPAIGN-MODES-I0-S3R2-RETURN]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---

# Echo Futures — I0 manager technical acceptance

> Registro histórico de la aceptación técnica I0. **La vía de entrega/merge Python de este registro queda revocada por la decisión Owner C06 GO-ONLY del mismo día**, documentada al final. El código Echo no se modifica por este log.

## Motivo
Cerrar la secuencia I0-S1/S2/S3/S3R1/S3R2 sin otra revisión amplia, recuperar retorno S3R2 y decidir preparación para integración controlada del reporter económico opt-in.

## Verificación manager
GitHub confirmó branch SHA 01a38c13b0a1b280eefb9d18f6d2b167e3cd8739, base echo master 2baf319d, 7 commits/7 paths en diff I0 total, corrección M1–M4 y errata de recuento 10/14 falsificadores contra base. Inspección source de mapping ResearchFundingSummary, condiciones Q y cash corroborado, STOW/PLATFORM por kind, y attempt provenance/request sellado no mostró bloqueo de código para el alcance I0. 69/69 reporter, 124/124 legacy, 25/25 frozen, R03 E2E y 442/442 statements son recibos del ejecutor local, no reejecutados CLOUD.

## Decisión histórica
MANAGER_TECHNICAL_VERDICT=APPROVED_FOR_CONTROLLED_MERGE_GATE; I0_MERGE=NOT_EXECUTED, OWNER_RELEASE_ACCEPTANCE=PENDING. Un único gate LOCAL para repetición sobre SHA y diff, deliver MERGE_READY_FOR_OWNER; no mover master sin aprobación Owner. S04-F01 y S04-F02 aún bloqueados por alcance separado, PROD congelada, I1–I4/GOD sin despacho. Sólo reporter opt-in, sin cambios Go/SDK/Strategy/MM, sin simulación causal/producción.

## Continuidad histórica
Actualizados planner único, diseño C05 por estado y paquete I0 con mandato de integración. Manager y programa abiertos. PRO_CHAT_POOL_DELTA UNKNOWN.

## Delta Owner 2026-10-29 — C06 GO-ONLY

### Solicitud y autoridad
Owner ordena deprecar Python S04 como parte de la solución oficial, diseñar toda la capacidad en Go, documentar plan detallado en Agents-OS y entregar tres shots: implementación GLM-5.3-Flash orquestada, review GOD LOCAL con workers Luna/Sol, corrección GLM LOCAL TOP. Esta orden supersede la propuesta de merge I0 Python, no borra los receipts históricos ni autoriza producción.

### Evidencia recuperada
Source remoto Echo master sigue `2baf319ddcba622d9557bc9f23a13787b44c58a7`. Se inspeccionaron entrada AGENTS, README del backtester, CLI main/experiment, platform_search, compose_account y ConfigSnapshot. Hay owners Go, runner, factories, pools/compartimentos y lifecycle reutilizables; composeAccount aún exige una cuenta y los comandos Python siguen en legado S04. No se asegura que la composición simultánea sea simple configuración: C06 asigna la adaptación del routing/RuleSets/mercado común al implementador y pruebas de paridad.

### Resolución documental
1. Reemplazar el diseño vigente por C06 GO-ONLY: mismos owners Go, tres modalidades, caja única, eventos/KPI y CLI Go, migración por identidad y retiro de dependencias Python. No puerto línea por línea del reporter ni nuevo motor/scheduler/framework.
2. Actualizar y compactar el planner existente con W0–W6 de implementación, R01–R12 de requisitos y A01–A16 de aceptación; matrices separadas de migración, ejecución física y resultados económicos. La entrega no termina en tooling/reporting.
3. Reemplazar el contenido operativo del paquete histórico I0-LOCAL por GO-S02/S03/S04; no crear otro planner/manager. S01 es el diseño actual. Los roles/modelos reales se registran; TOP para corrector GLM es instrucción Owner explícita.
4. Conservar copias byte-idénticas de los tres documentos anteriores como snapshots `.txt` bajo artifacts/backtester/history, no notas canónicas activas. Preservan toda la historia/estados previos sin múltiples cabeceras vigentes; las fuentes actuales conservan sus paths. Son derivados mecánicos, no un segundo diseño.
5. I0 Python pasa a REFERENCE_ONLY / SUPERSEDED_FOR_DELIVERY y su merge a CANCELLED_BY_OWNER_DIRECTION. El código Python S04 queda DESIGN_DEPRECATED; eliminación/migración física corresponde a GO-S02 y no se finge ejecutada desde CLOUD.

### Verificación y límites
Se publican blobs/cambios documentales con base tree reconciliado, optimistic HEAD guard y readback de master. No se programó producto Echo ni se ejecutaron builds/tests/campañas/compras/trading/merge/deploy. Validadores de notas/plan y Graphify del host no se ejecutaron en esta superficie; GO-S02 debe aplicar materialización/lint del SDD/retornos en el entorno real. No afirmar lint canónico PASS. Los archivos canónicos editados ya existían; no se crea plantilla/policy global.

### Pendientes y continuidad
S04-F01 equivalencia V1, S04-F02 admisión Go y D05 para investigación funded-only permanecen explícitos; no bloquean pruebas funcionales sintéticas ni autorizan G5. Ningún estudio A/B ni workstream vecino se redefine. SOURCE/BUILD/TEST/E2E/QUALIFICATION/MERGE/DEPLOY siguen separados. La siguiente acción es GO-S02 del paquete vigente; reviews sólo contra el SHA retornado. Manager y programa abiertos; PRO_CHAT_POOL_DELTA UNKNOWN. Rollback documental mediante nuevo commit reconciliado, nunca reset/force, conservando snapshots.
