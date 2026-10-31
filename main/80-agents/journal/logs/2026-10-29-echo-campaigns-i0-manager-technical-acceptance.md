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
updated: "2026-10-30"
---

# Echo Futures — I0 manager technical acceptance

> Registro histórico de la aceptación técnica I0. La vía de entrega/merge Python de este registro fue revocada por la decisión Owner C06 GO-ONLY. El delta del30-10 al final registra la entrega final GLM+MiniMax. Ninguno de estos registros ejecuta por sí solo operaciones de producto.

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

## Delta Owner 2026-10-30 — EF-CAMPAIGNS-FINAL

### Mandato
El Owner solicita una última sesión local integral: GLM-5.3-Flash sólo coordinador y todos los workers MiniMax M3.1 Flash; completar C06/migración de todos los canónicos, determinismo runtime/backtest, comparación con versión anterior y validación de señales/operaciones en último contrato físico NQ2–3meses; entregar histórico completo listo al siguiente agente sin ejecutarlo aquí. Primera candidata real objetivo domingo1-11-2026, America/Santiago. El objetivo de calendario no constituye permiso de operar.

### Baseline documental y producto comprobados
Se leyeron bootstrap actualizado30-10, guía Agents-OS, planner actual, paquete, retester y skill manager por alcance. Se verificaron GitHub refs: Echo feature/ef-campaigns-go `a22970c85d139c81c919aafac69f4bf6ceaf5dcd`; master `2baf319ddcba622d9557bc9f23a13787b44c58a7`. Corte Agents-OS de lectura `bb51f2ecd228047abd31c63edf94c11517d65e8e`. Los hechos físicos del S04 siguen executor-reported; no se reejecutaron desde CLOUD.

### Decisiones de ejecución publicadas
Se compacta el planner existente, preservando la versión previa en Git; se reemplaza el paquete de tres shots del path I0-LOCAL por un mandato final autosuficiente. C06 sigue siendo la arquitectura, sin nuevo manager/diseño. Requisitos precisados: P0 determinismo, P1 legacy/nuevo, P2 runtime fact replay con mismos inputs/estado/fills y comparación de decisiones antes de aplicar respuestas; controles CloseSafety efectivos; Strategy real y no fixture; manifest de policies extraído de fuentes selladas, sin transcripción manual Owner ni defaults; refund aplicado sólo como devolución comercial confirmada; catálogo entero y clasificación independiente de rentabilidad; cola G5 sólo preparada. Los porcentajes de reutilización no son un gate técnico: se reutilizan owners por contrato y evidencia, sin objetivo porcentual artificial.

Los procesos de implementación y verificación son MiniMax reales, con preflight provider y receipts, sin fallback de implementación GLM. La ausencia de subagentes debe resolverse mediante una ruta existente/autorizada MiniMax o reportarse como bloqueo proveedor; no fingir modelos ni agregar otra plataforma de agentes. La revisión independiente será de autor/contexto; no se afirma independencia de modelo entre dos workers MiniMax.

### Escritura y verificación
Cambios exclusivamente documentales en los archivos ya existentes: planner, paquete de mandatos y este change_log. La primera propuesta extensa de blob para el planner fue rechazada por la herramienta; se revisó y publicó una versión resumida del estado/plan con `update_file`, commit `c5ea6303fd06dabff8059973a3e9b1670c4b9c64`. No se da por publicado un blob sólo por haberlo creado: se exige commit/ref y readback del paquete y del log. No hay escritura de producto Echo, ejecución de pruebas o campañas, merge/deploy/gasto/trading. No se declara lint/Graphify ejecutado.

### Continuidad
El próximo agente carga EF-CAMPAIGNS-FINAL y completa los fixes/retests ordinarios en esa misma sesión; no entrega otra cadena de prompts de desarrollo. El histórico completo pertenece al siguiente agente, con manifests/gates elegibles y binario preparados. Live y merge requieren permisos correspondientes. El manager de conversación y el programa permanecen abiertos; el coordinador local cierra sólo su encargo. Consumo Pro UNKNOWN.
