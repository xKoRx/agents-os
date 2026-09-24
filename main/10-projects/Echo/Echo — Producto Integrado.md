---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Echo]]"
parent:
sprint: 2026-09-23--2026-09-27
start: 2026-09-07
due:
progress: 5
repo:
jira:
prs:
aliases:
  - Echo Producto Integrado
  - Echo + Echo Forge
  - Echo as product
tags:
  - kind/project
  - area/echo
created: 2026-09-07
updated: 2026-09-22
---
# Echo — Producto Integrado

> **Dirección de producto vigente, owner 22-09-2026, planificación solamente.** Exactamente dos tracks de implementación: [[Echo Forge — Factory V2 Completion]] y [[Echo — Live Platform V1]]. The Lab pertenece a Echo, no es un tercer proyecto. La planificación vigente de Lab está en [[D — Revised Roadmap]]; el contrato en [[A — Product Contract — The Lab]], diseño en [[B — Architecture Decision Report]], primer flujo en [[E — First Usable Vertical Slice]] y decisiones en [[F — Decision Register]]. [[C — Reality and Gap Matrix]] conserva evidencia con fecha de corte, NO prueba implementación nueva.

## Objetivo de producto
Forge fabrica y entrega finalistas junto con operaciones SQX y MT5. Echo ingiere estrategias; su `trade_journal` continúa siendo exclusivamente autoridad operacional de Echo. The Lab V3 conserva una única base analítica de operaciones normalizadas, ofrece tres períodos, N curvas algorítmicas, métricas, calendario, dashboard y screener. Luego permite probar múltiples gestiones monetarias, portfolios y asignaciones controladas a cuentas. North star: TIME_TO_USABLE_TRADING_SYSTEM, KISS, integridad y crecimiento sin duplicar autoridades.

## Decisiones de producto ratificadas por owner 22-09
- Dos cortes configurables en el import: A = fin efectivo del dataset Forge de entrenamiento, B = inicio de operativa/observación; pertenencia de operación exclusivamente por instante de APERTURA, punto de resultado al CIERRE. Convención exacta de input date/time y UTC debe fijarse en SPEC diaria; si A se expresa como último día completo, primer instante siguiente es límite exclusivo.
- Una historia seleccionada: `TRAINING_DATA` desde SQX antes de A; `PRE_REAL` desde MT5 entre A y B; `REAL` desde Echo Reference/journal a partir de B. IS/OOS son metadatos del training. Originales SQX/MT5 aportados por Forge, Echo calcula todo Lab. Fuera de período se corta, no concatena otra historia.
- Única base durable activa en Lab = operaciones normalizadas. Curvas, puntos, métricas, screener y portfolios research son derivados. No exigir HistoryRevision/HistoryPublication ni mantener ediciones históricas de datasets: reemplazo manual validado y atómico con fuente original reconstruible.
- `trade_journal`, broker facts, runtime, copying, controles de riesgo y posiciones no se modifican ni se eliminan como parte de limpieza Lab. Un job periódico de Lab lee journal de modo read-only, normaliza operaciones Reference, actualiza base analítica idempotentemente y recalcula derivados afectados.
- N algoritmos de curvas, R_PIPS/R_MONEY y otras bases, configuración/versionado; separar comportamiento de estrategia de lotaje/gestión monetaria. No simular stops/entradas alternativas sin futuros datos de velas.
- Reemplazar Lab V1/V2 sin obligación de compatibilidad visual ni fórmulas legacy. Eliminar tablas, jobs, código, vistas y front exclusivos de Lab antiguo tras inventario de consumidores y prueba de que no tocan Echo operacional; no convertir paridad legacy en gate. Limpieza explícita del roadmap, no backlog eterno.
- Entregar primero dashboard auténtico durante 23–27 septiembre. Cada día inicia con planificación técnica de su hito, luego implementación, pruebas, corrección y evidencia; no terminar una jornada por mera entrega de código. Owner mantiene gates de trading/PROD separados.

## Estado y realidad
- **The Lab D3 Shot 1 (24-09): CANDIDATE implementado — NO certificado.** Vertical analítico completo sobre la autoridad D1 (engine `v3/sdk/analytics/curve`, migración 065 derivados, servicio F4 `RecalculateStrategyVersion`, CLI, Hasura source artifacts, tab front Curve Lab V3). Candidate `6a111c9e` en `origin/feature/d3-lab-v3-first-analytical` (baseline `8adce7ec`); fixture determinista, sin historia auténtica (Forge pendiente); verificación independiente (Shot 2) y gate final (Shot 3) pendientes. Paquete: [[A — Technical SPEC D3]], evidencia [[C — Evidence D3 (Shot 1)]], handoff [[E — F4 Handoff D3]]. `FORGE_DUAL_HISTORY_INTEGRATION = PENDING`.
- Forge F05-C FULL: tres finalistas certificados según notas del 21-09; **no demuestra** todavía dos listas individuales SQX/MT5 con las ventanas correctas. E04 join DEV certificado para handoff operativo, **no** para Lab. E05 S0 y PG063 existen, **no** constituyen Lab V3 usable. Evidencia: [[C — Reality and Gap Matrix]]. No se ejecutaron tests, cambios de source ni consultas PROD en esta actualización documental.
- La implementación puede conservar identidad/contratos S0 y piezas correctas del worker, pero el producto V3 tendrá UNA autoridad analítica activa: no coexistencia permanente de `canonical_trade_sets` como segundo write-master y `lab_operations`. Resolver consumidores E05/E10 mediante adaptación explícita antes del retiro de tablas.
- Echo E10 M7 pendiente revisión/ratificación sample policy: no bloquear historia/curvas ni avanzar elegibilidad por inercia. E06/E07 son fuentes para REAL; E08/E09 controlan seguridad/fidelidad económica, no son prerequisito de curvas históricas. No asumir que master=PROD.

## Plan y supervisión
- **23/09:** modelo SQL/contrato Forge+Echo congelado con evidencia de operación auténtica.
- **24/09:** dos históricos ingeridos, tres períodos definidos, base única consultable.
- **25/09:** curva auténtica visible en dashboard DEV con algoritmo versionado y métricas mínimas.
- **26/09:** job journal→Lab idempotente + calendario/detalle y curvas actualizadas.
- **27/09:** screener, pruebas E2E, diagnóstico de brechas y primera aceptación de producto; limpieza legacy inventariada y priorizada.
- **Inmediatamente después de V3 usable:** limpieza Lab V1/V2 de código/SQL/jobs/front con prueba de cero consumidores; luego múltiples gestiones de riesgo, portfolio research, portfolio allocation/apply, dashboards portfolio y backtesting futuro con velas según [[D — Revised Roadmap]]. No afirmar limpieza ejecutada aún.

## Gobernanza
La decisión de alcance es del owner; las opciones técnicas exactas quedan en SPEC al inicio de cada día. Los cambios frozen se reabren sólo para eliminar deuda demostrada y habilitar V3, con revisión cruzada SDK/Forge/Echo. DEV integrado y PROD autorizado son gates distintos. El trabajo viejo no se preserva por antigüedad, los hechos operativos sí. Proyecto padre coordina los dos tracks; no crear Integration como tercer producto.
