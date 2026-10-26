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
updated: 2026-10-26
---
# Echo — Producto Integrado

## 📊 Estado actual

### Dirección actual del LAB — V4 (Owner ratificó 2026-10-20)

**The LAB V4 sustituye el diseño V3 para la plataforma analítica de Echo**, sin crear otro proyecto/producto. El motor nacido bajo Echo Futures es el motor genérico de operaciones de Echo; los conceptos compartidos no conservarán nombres `futures_` por inercia. LAB es consumidor analítico con su propio modelo de historia, curvas, métricas y composición; preserva los hechos originales, la identidad del runtime y la integración operativa Forge, y retira progresivamente el LAB exclusivo V1–V3, sin alterar silenciosamente PROD.

**Dirección vigente Owner, 2026-10-26 (D25/D26):** nuevo workstream Ingestion V2 parte de lab-v4/shot4-integration; endpoint validado se integra temprano al mismo branch antes del resto de Shot2. Runtime paralelo es referencia, convergencia fuera del programa. Cuatro shots: GOD diseña, GLM-5.3-Flash Max LOCAL implementa, GLM independiente audita, GLM corrige con verificador independiente. D24 conserva restricciones de extracción/migración futura, pero su autoridad de rama está sustituida. Ver [[F — Decision Register]] D25–D27.

**Decisiones Owner V4 ratificadas:** D09 capital virtual inicial 10.000 + preset 1% configurable con presupuesto al abrir; D10 R sobre presupuesto certificado del ciclo sellado al abrir; D11 portfolio estático con capital separado, pesos fijos y comienzo flat; D16 corte pre/post por `construction_at` real y `construction_data_cutoff` como metadata distinta. Autoridad detallada: [[F — Decision Register]]; handoff completo GOD: [[THE_LAB_V4_Diseno_para_revision]].

**Antecedente al 2026-10-22 (superado por cierre V4 y nuevo freeze):** `SHOT1_DESIGN_COMPLETE / SHOT2_IMPLEMENTATION_READY` para `THE_LAB_V4_RUNTIME_FORGE_INTEGRATION`. Diseño ejecutable sobre `feature/ef-runtime-pools@2ee61791deb3139be23e1c9be3708b1d41da8d6b`, ocho especialistas Sol ONE-SHOT y revisión crítica GOD. Autoridad y diez entregables: [[0 — Shot 1 Gate and Baseline]]; siguiente GLM LOCAL Shot2: [[J — Shot 2 Implementation Package]]. D17–D24 también ratificadas; las condiciones/preflights de 2026-10-20 son antecedentes superados para el gate de diseño actual, sin nuevo freeze. Implementación/E2E de este paquete NOT_RUN, sin deploy, migración destructiva ni activación compartida. Exactamente cuatro shots; sesión Agents-OS y proyecto abiertos.

**Continuidad 2026-10-23:** `SHOT3_ADVERSARIAL_COMPLETE / SHOT4_FIX_PACKAGE_READY` para THE_LAB_V4_RUNTIME_FORGE_INTEGRATION, candidato Echo `3b3ae81e` / Symphony `dd4af7d`. 53 findings adjudicados: 22 P0, 30 P1 y 1 P2. H01–H49: 1 PASS, 41 FAIL, 7 NOT_RUN, 0 BLOCKED_EXTERNAL principales. Dictamen y límites: [[10-projects/Echo/The Lab/V4 — Runtime Integration/SHOT3_ADVERSARIAL_REPORT|SHOT3_ADVERSARIAL_REPORT]]. Entrega única a GLM LOCAL: [[10-projects/Echo/The Lab/V4 — Runtime Integration/SHOT4_FIX_PACKAGE|SHOT4_FIX_PACKAGE]]. Sin fixes ni inicio Shot4. Cero conexiones externas no certificado en primer browser E; sin mutaciones compartidas observadas/ejecutadas. Sesión abierta.

**Continuidad 2026-10-26 — cierre de sesión The Lab V4 y próximo workstream de ingesta operacional (Owner).** Shot 4 terminó como **candidato cerrado con excepciones, NO release certificado**: Echo `lab-v4/shot4-integration@b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce`, Symphony `lab-v4/shot4-symphony@a0c68d154b733049c97bf46e69c4629078d40c05`. [[SHOT4_FINAL_COVERAGE_MATRIX]] contiene H01–H49 **48 PASS, H45 FAIL** (prepare 20k no alcanza ≤2s), más **QA-01 transversal FAIL** (~85,8/85,2% vs 95%); la cabecera histórica «47/49» agrupa indebidamente QA-01 con los casos H. AUTH_FORGE auténtico sigue sin artefacto autorizado. `feature/ef-runtime-pools@0e17c4d3f1179cde709f923c8dd28e8cd853afc9` divergió del candidato; no existe integración/cutover/deploy demostrado. El `RuntimeConfigSupervisor` del candidato requiere un `ConfigInstaller` efectivo en Core/Bridge/StateFun; sin instalador permanece fail-closed (NO-READY), no está certificado provisioning real. No abrir Shot 5 ni reabrir los cuatro shots.

**Estado 2026-10-26 — ECHO_INGESTION_V2_GOD_DESIGN_READY_FOR_GLM.** Diseño completado, separado del programa V4 cerrado y dentro de Echo. Baseline remoto/local: Echo lab-v4/shot4-integration@b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce; referencia runtime feature/ef-runtime-pools@0e17c4d3f1179cde709f923c8dd28e8cd853afc9; Symphony lab-v4/shot4-symphony@a0c68d154b733049c97bf46e69c4629078d40c05. Forensics confirma reutilización del endpoint/registry/historias/worker/UI y deltas de validación/store, binding/installer/ACK, correlación/dispatch/projector. Ningún test producto, implementación, deploy ni integración de ramas ejecutado en Shot1.

**NEXT exacto:** GLM-5.3-Flash Max LOCAL toma [[D — GLM Handoff Packages]] §D2. Crea hija desde HEAD refrescado de lab-v4/shot4-integration, implementa/valida endpoint, obtiene ECHO_INGESTION_V2_ENDPOINT_INTEGRATION_PASS y lo integra inmediatamente al mismo branch con SHAs/evidencia/base sincronizada antes de O/J/L/F. No reconciliar runtime como prerequisito. SPEC [[B — Frozen Architecture]], baseline/merge [[A — Source Baseline and Branch Integration]], gates [[C — Implementation Shots and Acceptance Gates]], ejemplos [[E — Executable Contract Examples]]. Carpeta 10-projects/Echo/Ingestion V2 — Operational Integration/. Sin blocker de diseño; AUTH_FORGE limita sólo autenticidad futura, H45/QA01 históricos explícitos. Shot2 NO iniciado, Agents-OS abierto; cierre anterior V4 no cierra esta sesión.

## Backlog de producto — funcionalidades futuras (fuera de LAB V4)

**Registro del Owner (2026-10-22).** Son capacidades futuras de Echo, no tareas del programa actual ni compromisos de fecha. The Lab continúa dentro de [[Echo — Producto Integrado]]: no se crea un proyecto paralelo.

- **The Lab — evolución analítica:** explotar las historias preconstrucción, postconstrucción/pre-Echo y Echo según sus cortes reales para evaluar estabilidad y deriva de métricas, curvas configurables, rankings y comparativas por ventana, preservando identidad, provenance y revisiones. El alcance actual de integración Forge → Echo → LAB, curvas, rankings, screener y dashboard continúa bajo [[F — Decision Register]] y el programa V4 de cuatro shots.
- **Portfolios dinámicos (I2, futuro):** selección y rotación de estrategias por rankings, filtros, curvas y ventanas; políticas Top N, pesos, correlación, riesgo y MM; membresía temporal y cadencias configurables (hora, día, semana, mes, año), con evaluación y seguimiento. No implementar ni diseñar ahora scheduler, rebalanceador, políticas de selección ni nuevas tablas de I2.
- **Backtester histórico de campañas desde The Lab (futuro):** reutilizar el motor de backtesting existente de Echo, no crear otro motor, para recorrer los históricos de estrategias y eventualmente portfolios y simular campañas de distintas duraciones, ventanas y tipos de cuenta **Forex y/o Futuros**. Permitir definir reglas de evaluación/fondeo según el tipo de cuenta (fases, objetivos, límites de pérdida diaria/total, trailing EOD cuando corresponda, capital y costes), MM y escenarios; devolver cronología de decisiones, curvas, métricas y resultados reproducibles. Usar sólo datos disponibles en cada instante, sin look-ahead y distinguiendo historia observada de resultados simulados. Estas reglas son ejemplos de parámetros futuros, no defaults congelados.
- **Compatibilidad futura sin trabajo especulativo hoy:** cuando se implementen estas capacidades, deben evolucionar de forma predominantemente aditiva sobre identidades StrategyVersion/History/Operation, versiones y revisiones, provenance, ventanas y disponibilidad temporal, contexto MM, curvas, métricas y scores versionados que V4 ya necesita. Evitar una reingesta completa de Forge o refactorizar medio Echo; **cero tiempo de implementación actual** para portfolios y backtesting de campañas, y sin añadir endpoints, tablas, colas o workers por anticipación.

**Estado:** backlog diferido, sin estimación ni asignación. No modifica requisitos, gates ni responsabilidades de los cuatro shots de LAB V4.

### Antecedentes de producto V3 (históricos; no authority de V4)

> **Dirección histórica V3, owner 22-09-2026; superseded para LAB V4 por las decisiones ratificadas el 20-10-2026.** Exactamente dos tracks de implementación: [[Echo Forge — Factory V2 Completion]] y [[Echo — Live Platform V1]]. The Lab pertenece a Echo, no es un tercer proyecto. La planificación vigente de Lab está en [[D — Revised Roadmap]]; el contrato en [[A — Product Contract — The Lab]], diseño en [[B — Architecture Decision Report]], primer flujo en [[E — First Usable Vertical Slice]] y decisiones en [[F — Decision Register]]. [[C — Reality and Gap Matrix]] conserva evidencia con fecha de corte, NO prueba implementación nueva.

## 🎯 Objetivo

### Objetivo de producto
Forge fabrica y entrega finalistas junto con operaciones SQX y MT5. Echo ingiere estrategias; su `trade_journal` continúa siendo exclusivamente autoridad operacional de Echo. The Lab V3 conserva una única base analítica de operaciones normalizadas, ofrece tres períodos, N curvas algorítmicas, métricas, calendario, dashboard y screener. Luego permite probar múltiples gestiones monetarias, portfolios y asignaciones controladas a cuentas. North star: TIME_TO_USABLE_TRADING_SYSTEM, KISS, integridad y crecimiento sin duplicar autoridades.

## Decisiones de producto ratificadas por owner 22-09
- Dos cortes configurables en el import: A = fin efectivo del dataset Forge de entrenamiento, B = inicio de operativa/observación; pertenencia de operación exclusivamente por instante de APERTURA, punto de resultado al CIERRE. Convención exacta de input date/time y UTC debe fijarse en SPEC diaria; si A se expresa como último día completo, primer instante siguiente es límite exclusivo.
- Una historia seleccionada: `TRAINING_DATA` desde SQX antes de A; `PRE_REAL` desde MT5 entre A y B; `REAL` desde Echo Reference/journal a partir de B. IS/OOS son metadatos del training. Originales SQX/MT5 aportados por Forge, Echo calcula todo Lab. Fuera de período se corta, no concatena otra historia.
- Única base durable activa en Lab = operaciones normalizadas. Curvas, puntos, métricas, screener y portfolios research son derivados. No exigir HistoryRevision/HistoryPublication ni mantener ediciones históricas de datasets: reemplazo manual validado y atómico con fuente original reconstruible.
- `trade_journal`, broker facts, runtime, copying, controles de riesgo y posiciones no se modifican ni se eliminan como parte de limpieza Lab. Un job periódico de Lab lee journal de modo read-only, normaliza operaciones Reference, actualiza base analítica idempotentemente y recalcula derivados afectados.
- N algoritmos de curvas, R_PIPS/R_MONEY y otras bases, configuración/versionado; separar comportamiento de estrategia de lotaje/gestión monetaria. No simular stops/entradas alternativas sin futuros datos de velas.
- Reemplazar Lab V1/V2 sin obligación de compatibilidad visual ni fórmulas legacy. Eliminar tablas, jobs, código, vistas y front exclusivos de Lab antiguo tras inventario de consumidores y prueba de que no tocan Echo operacional; no convertir paridad legacy en gate. Limpieza explícita del roadmap, no backlog eterno.
- Entregar primero dashboard auténtico durante 23–27 septiembre. Cada día inicia con planificación técnica de su hito, luego implementación, pruebas, corrección y evidencia; no terminar una jornada por mera entrega de código. Owner mantiene gates de trading/PROD separados.

## 📆 Bitácora

### Estado y realidad
- **Auditoría operacional PROD (14-10): `OPERATIONAL_DEGRADED` — sistema limpio E2E, AUD-24 sigue latente.** Todo lo que corrió hoy corrió bien: traza E2E completa (trade `01a13a80` del master scalpa copiado en 1–2 s a 3 cuentas con tickets reales, cierres con PnL journalizados, master +93.43), 17/17 terminales conectadas, 0 FAILED/96 h, core 0 ERROR (4 WARN = exclusiones correctas), bridge 0 WARN/0 ERROR, config-flow entregando (ola ClientConfig hoy 13:31 UTC), ETCD/repo sin cambios (PIDs del 25-sep intactos). La única degradación es la misma de ayer, ahora sin exposición viva: **AUD-24 sigue demostrado (G5 `504079710` con 0 filas en journal all-time, causa en hipótesis) y su gate de regresión no se ejercitó (0 copias a G5 en la ventana)**. Las 3 posiciones huérfanas del 13-oct cerraron en broker fuera de Echo (equity=balance con latido fresco). Nuevos/extendidos: AUD-27 extendido (la estrategia XAU `magic_250901015` tiene su trade de 22:01 OPEN sin copiar: policies sólo hacia Slaves ARCHIVED), AUD-29 re-confirmado (Axi `3094610` = cuenta ciega, ya listada como pendiente owner en el change_log del 12-oct). AUD-25/26/28 vigentes sin cambio. Evidencia: [[Echo — Production Operational Audit 2026-10-14]].
- **Auditoría operacional PROD (13-10): `OPERATIONAL_DEGRADED` — los fixes del 12-oct quedaron finos.** Triggers entregando de nuevo (ola ClientConfig post-fix 23:21 UTC del 12-oct vía `accounts_config`), flota migrada 17/17 (3 MT4 + 14 MT5) latiendo, E2E con tickets reales y 0 FAILED/72 h. Las "pocas operaciones abiertas" son config vigente, no efecto de los fixes: master con 4 señales copiables; `magic_260104001` sin policies (AUD-26) y GDAXI con policies hacia cuentas ARCHIVED (AUD-27, 0 legs históricos). Único defecto nuevo AUD-24 (P1): **TTP G5 `504079710` no journaliza** — 3 USTEC vivas sin legs en `trade_journal`; el próximo cierre del master NDX las dejaría sin gestión activa (quedarían al TP/SL estático del broker) — tratar hoy. AUD-25: repo `v3/hasura/` sigue sin triggers ni header Authorization (apply directo reproduciría el incidente). Evidencia: [[Echo — Production Operational Audit 2026-10-13]].
- **Auditoría operacional PROD (04-10): `OPERATIONAL_PASS`.** Primera auditoría con SSH al runtime: core/gateway/functions en `.71` sin reinicio desde el rollout 25-sep (`master@372af59a`, cero drift), ETCD íntegro (incluida la recuperación del incidente del día), E2E persistiendo al segundo en la apertura dominical, 0 ERROR/24 h y 1 WARN esperado. **AUD-17 (4109) CERRADO** con gate cumplido; copia activa en ~15 cuentas y ~14 estrategias (AUD-18 mejorado). Pendientes P3/P4: volumen de logs del core (knob WARN no reduce export), higiene métrica de cuenta archivada, listener extra :45021 por identificar. Evidencia: [[Echo — Production Operational Audit 2026-10-04]].
- **The Lab D3 (24-09): CLOSED / DAY_PASS.** Baseline certificado y promovido a `master@372af59a7b83604781346613da01e3d510ea1360`. Shot 2 adversarial encontró y Shot 3 corrigió F-D3-01..07; source/fixture PASS. Certificación física DEV posterior: schema D1+D3, Hasura readonly, Front Curve Lab V3, MONEY/R, períodos A/B, drill-down, stale→recalculate→publish y rollback PASS; PROD quedó intocado. `D3_AUTHENTIC_DATA_PASS` no se declara porque `FORGE_DUAL_HISTORY_INTEGRATION = PENDING`: el dataset DEV fue de verificación por la interfaz canónica, no historia Forge auténtica. Hallazgos de integración para el siguiente día: el `StrategyHistoryHandler` existe pero no está montado en el mux real del Gateway; metadata Hasura debe aplicar limpiamente sin permisos `admin` incompatibles; `--triggered-by` y polish de chart son menores. Autoridades: [[G — Correction Record D3 (Shot 3)]], [[E — F4 Handoff D3]].
- Forge F05-C FULL: tres finalistas certificados según notas del 21-09; **no demuestra** todavía dos listas individuales SQX/MT5 con las ventanas correctas. E04 join DEV certificado para handoff operativo, **no** para Lab. E05 S0 y PG063 existen, **no** constituyen Lab V3 usable. Evidencia: [[C — Reality and Gap Matrix]]. No se ejecutaron tests, cambios de source ni consultas PROD en esta actualización documental.
- La implementación puede conservar identidad/contratos S0 y piezas correctas del worker, pero el producto V3 tendrá UNA autoridad analítica activa: no coexistencia permanente de `canonical_trade_sets` como segundo write-master y `lab_operations`. Resolver consumidores E05/E10 mediante adaptación explícita antes del retiro de tablas.
- **Rollout PROD (25-09): owner autorizado; `PROD_ROLLOUT_PARTIAL_EXECUTED`.** En vivo y verificado: BD `echo` @ .220 migrada (061–065 + suplementos certificados MetaTrader5/GRANT UPDATE, postcheck PASS, backup 157.310 filas) y ETCD production sembrado (4 tokens auth Gateway + CORS, mod_rev 59077–59081). Empaquetado esperando ventana owner: binarios `372af59a` (core/functions/gateway/lab-worker, `vcs.modified=false`), front dist, metadata Hasura vía merge aditivo (**el repo `v3/hasura/` no contiene event_triggers ⇒ un `metadata apply` directo los borraría y rompería la propagación de config**). Paquete y runbooks: workspace externo `~/aranea/work/echo-prod-rollout-20260925/release/`. Deuda: merge `4aad647b` (seed tests siguen pudiendo clobberizar password ETCD PROD), AUD-10 GDAXI, alias WSFMARKETS, alertas silencio. Evidencia: resumen `2026-09-25-echo-prod-rollout-summary`.
- Echo E10 M7 pendiente revisión/ratificación sample policy: no bloquear historia/curvas ni avanzar elegibilidad por inercia. E06/E07 son fuentes para REAL; E08/E09 controlan seguridad/fidelidad económica, no son prerequisito de curvas históricas. No asumir que master=PROD.

## ✅ Tareas

### Plan y supervisión
- **23/09:** modelo SQL/contrato Forge+Echo congelado con evidencia de operación auténtica.
- **24/09:** D3 cerrado: primera experiencia analítica certificada en source/fixture y físicamente en Echo DEV; baseline `master@372af59a`. Historia Forge auténtica sigue como gate externo separado.
- **25/09:** D4 — Live Analytical Refresh. Primero cerrar wiring físico del endpoint de history y metadata Hasura reproducible; luego `history changed → dirty → automatic recalculate → atomic publish → UI refreshed` sin CLI manual.
- **26/09:** gate de historia auténtica Forge cuando el producer esté disponible + calendario/detalle, sin bloquear D4 interno por dependencia externa.
- **27/09:** screener, pruebas E2E, diagnóstico de brechas y primera aceptación de producto; limpieza legacy inventariada y priorizada.
- **Inmediatamente después de V3 usable:** limpieza Lab V1/V2 de código/SQL/jobs/front con prueba de cero consumidores; luego múltiples gestiones de riesgo, portfolio research, portfolio allocation/apply, dashboards portfolio y backtesting futuro con velas según [[D — Revised Roadmap]]. No afirmar limpieza ejecutada aún.

## Gobernanza
La decisión de alcance es del owner; las opciones técnicas exactas quedan en SPEC al inicio de cada día. Los cambios frozen se reabren sólo para eliminar deuda demostrada y habilitar V3, con revisión cruzada SDK/Forge/Echo. DEV integrado y PROD autorizado son gates distintos. El trabajo viejo no se preserva por antigüedad, los hechos operativos sí. Proyecto padre coordina los dos tracks; no crear Integration como tercer producto.
