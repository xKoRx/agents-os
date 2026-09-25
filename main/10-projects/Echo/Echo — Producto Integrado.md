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
updated: 2026-09-24
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
- **The Lab D3 (24-09): CLOSED / DAY_PASS.** Baseline certificado y promovido a `master@372af59a7b83604781346613da01e3d510ea1360`. Shot 2 adversarial encontró y Shot 3 corrigió F-D3-01..07; source/fixture PASS. Certificación física DEV posterior: schema D1+D3, Hasura readonly, Front Curve Lab V3, MONEY/R, períodos A/B, drill-down, stale→recalculate→publish y rollback PASS; PROD quedó intocado. `D3_AUTHENTIC_DATA_PASS` no se declara porque `FORGE_DUAL_HISTORY_INTEGRATION = PENDING`: el dataset DEV fue de verificación por la interfaz canónica, no historia Forge auténtica. Hallazgos de integración para el siguiente día: el `StrategyHistoryHandler` existe pero no está montado en el mux real del Gateway; metadata Hasura debe aplicar limpiamente sin permisos `admin` incompatibles; `--triggered-by` y polish de chart son menores. Autoridades: [[G — Correction Record D3 (Shot 3)]], [[E — F4 Handoff D3]].
- Forge F05-C FULL: tres finalistas certificados según notas del 21-09; **no demuestra** todavía dos listas individuales SQX/MT5 con las ventanas correctas. E04 join DEV certificado para handoff operativo, **no** para Lab. E05 S0 y PG063 existen, **no** constituyen Lab V3 usable. Evidencia: [[C — Reality and Gap Matrix]]. No se ejecutaron tests, cambios de source ni consultas PROD en esta actualización documental.
- La implementación puede conservar identidad/contratos S0 y piezas correctas del worker, pero el producto V3 tendrá UNA autoridad analítica activa: no coexistencia permanente de `canonical_trade_sets` como segundo write-master y `lab_operations`. Resolver consumidores E05/E10 mediante adaptación explícita antes del retiro de tablas.
- **Rollout PROD (25-09): owner autorizado; `PROD_ROLLOUT_PARTIAL_EXECUTED`.** En vivo y verificado: BD `echo` @ .220 migrada (061–065 + suplementos certificados MetaTrader5/GRANT UPDATE, postcheck PASS, backup 157.310 filas) y ETCD production sembrado (4 tokens auth Gateway + CORS, mod_rev 59077–59081). Empaquetado esperando ventana owner: binarios `372af59a` (core/functions/gateway/lab-worker, `vcs.modified=false`), front dist, metadata Hasura vía merge aditivo (**el repo `v3/hasura/` no contiene event_triggers ⇒ un `metadata apply` directo los borraría y rompería la propagación de config**). Paquete y runbooks: workspace externo `~/aranea/work/echo-prod-rollout-20260925/release/`. Deuda: merge `4aad647b` (seed tests siguen pudiendo clobberizar password ETCD PROD), AUD-10 GDAXI, alias WSFMARKETS, alertas silencio. Evidencia: resumen `2026-09-25-echo-prod-rollout-summary`.
- Echo E10 M7 pendiente revisión/ratificación sample policy: no bloquear historia/curvas ni avanzar elegibilidad por inercia. E06/E07 son fuentes para REAL; E08/E09 controlan seguridad/fidelidad económica, no son prerequisito de curvas históricas. No asumir que master=PROD.

## Plan y supervisión
- **23/09:** modelo SQL/contrato Forge+Echo congelado con evidencia de operación auténtica.
- **24/09:** D3 cerrado: primera experiencia analítica certificada en source/fixture y físicamente en Echo DEV; baseline `master@372af59a`. Historia Forge auténtica sigue como gate externo separado.
- **25/09:** D4 — Live Analytical Refresh. Primero cerrar wiring físico del endpoint de history y metadata Hasura reproducible; luego `history changed → dirty → automatic recalculate → atomic publish → UI refreshed` sin CLI manual.
- **26/09:** gate de historia auténtica Forge cuando el producer esté disponible + calendario/detalle, sin bloquear D4 interno por dependencia externa.
- **27/09:** screener, pruebas E2E, diagnóstico de brechas y primera aceptación de producto; limpieza legacy inventariada y priorizada.
- **Inmediatamente después de V3 usable:** limpieza Lab V1/V2 de código/SQL/jobs/front con prueba de cero consumidores; luego múltiples gestiones de riesgo, portfolio research, portfolio allocation/apply, dashboards portfolio y backtesting futuro con velas según [[D — Revised Roadmap]]. No afirmar limpieza ejecutada aún.

## Gobernanza
La decisión de alcance es del owner; las opciones técnicas exactas quedan en SPEC al inicio de cada día. Los cambios frozen se reabren sólo para eliminar deuda demostrada y habilitar V3, con revisión cruzada SDK/Forge/Echo. DEV integrado y PROD autorizado son gates distintos. El trabajo viejo no se preserva por antigüedad, los hechos operativos sí. Proyecto padre coordina los dos tracks; no crear Integration como tercer producto.
