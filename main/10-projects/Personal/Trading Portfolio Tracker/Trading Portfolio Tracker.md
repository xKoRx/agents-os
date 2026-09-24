---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Personal]]"
parent:
sprint:
start: 2026-09-23
due:
progress: 5
repo:
jira:
prs:
aliases:
  - Trading Tracker
  - Prop Tracker
  - Trading P&L Tracker
  - Trading Portfolio
tags:
  - kind/project
  - area/personal
  - domain/trading
  - topic/prop-firms
  - topic/portfolio-tracking
created: 2026-09-23
updated: 2026-09-23
---

# Trading Portfolio Tracker

%% Naming: Trading Portfolio Tracker es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Trading Portfolio Tracker
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Fase:** F0 Inventario · **Cuentas conocidas:** 17 · **Expansión prevista:** ~10 cuentas adicionales
> Registro económico y operativo personal del ecosistema de trading: cuánto capital salió, cuánto cash volvió, qué cuentas/activos existen hoy, cuál es su estado y qué capacidad económica potencial representan.

## 🎯 Objetivo

Construir una fuente de verdad personal para responder, sin sacar cuentas a mano, cinco preguntas:

1. **¿Cuánto he gastado realmente en trading?**
2. **¿Cuánto he retirado/cobrado realmente?**
3. **¿Cuál es mi P&L realizado neto y cuánto capital sigo teniendo comprometido?**
4. **¿Qué activos/cuentas tengo, en qué estado están y cuáles siguen teniendo valor económico?**
5. **¿Qué potencial de monetización tiene el portfolio actual bajo escenarios explícitos y no fantasiosos?**

El alcance inicial son las cuentas de fondeo/prop y broker asociadas al ecosistema actual, incluyendo **Axi Select, FTMO, The Trading Pit (TTP), Orion y WeGetFunded/WSF**, más cualquier firma futura que se incorpore.

La primera entrega es deliberadamente KISS: **Markdown canónico en Agents-OS, actualizado manualmente con evidencia suficiente**. Una integración posterior en [[Loom]] puede consumir este modelo cuando la información ya esté limpia y estable.

## 📊 Estado actual

> [!summary]+ Snapshot inicial — 2026-09-23
> **17 cuentas conocidas** entre Axi Select, FTMO, TTP, Orion y WSF.
> **Inventario detallado:** parcial — Orion 6 cuentas históricas / 5 activas; TTP 2 cuentas funded de 50k; The5ers 1 cuenta High Growth 10k perdida; resto pendiente.
> **Gastos históricos:** evidencia parcial cargada — facturas TTP/contexto US$2.237,35 + WSF US$717,50 + Orion estimado conservador US$2.614,01; FTMO/Axi y otros gastos aún faltan.
> **Cash recibido acreditado en evidencia:** Axi Select US$2.178,87 + TTP/contexto US$1.619,58 + Orion real US$1.782,26 + FTMO pagos visibles US$2.290,15 = **US$7.870,86**. La clasificación payout vs refund sigue parcial.
> **P&L realizado neto:** todavía no calculable de forma fiable porque faltan gastos históricos completos y separar refunds de trading payouts.
> **Expansión:** posible compra de aproximadamente 10 cuentas adicionales; se registra como pipeline, **no como activo existente**.

> [!warning]+ Regla contable clave
> El balance nominal de una cuenta prop **no es patrimonio líquido ni ganancia**. Se registra como **capacidad financiada / notional gestionable**. Un payout sólo se convierte en profit realizado cuando fue efectivamente cobrado. Una cuenta activa puede tener valor económico operacional, pero no se suma como cash.

### Dashboard económico

| Métrica | Valor actual | Regla |
|---|---:|---|
| Cash gastado bruto identificado | **US$6.068,86 parcial** | TTP/contexto US$2.237,35 + WSF US$717,50 + Orion estimado US$2.614,01 + The5ers estimado US$500; falta FTMO y otros gastos |
| Capital desplegado recuperable | **~US$2.200 Axi Select** | Se trata como inversión/activo recuperable, no como costo hundido mientras mantenga recuperabilidad |
| Cash desplegado total conocido | **~US$8.268,86 + FTMO pendiente** | Costos identificados + capital Axi recuperable |
| Cash recibido acreditado | **US$7.870,86** | Incluye payouts/rewards y refunds; se descompone antes de calcular trading profit |
| Refunds acreditados | **2 eventos TTP, monto pendiente** | Reducen costo económico, no cuentan como trading profit |
| Trading payouts confirmados | **≥ US$3.961,13** | Axi US$2.178,87 + Orion US$1.782,26; TTP/FTMO requieren clasificación por tipo |
| **P&L realizado neto** | Pendiente | retiros − gastos |
| Capital propio comprometido | Pendiente | dinero propio aún expuesto/no recuperado |
| Cuentas existentes | **17** | inventario físico, cualquier estado |
| Cuentas productivas | Pendiente | funded/live y habilitadas para generar payout |
| Cuentas en evaluación | Pendiente | challenge/evaluation en curso |
| Cuentas perdidas/cerradas | Pendiente | historial; no cuentan como capacidad actual |
| Notional financiado activo | Pendiente | suma de tamaño nominal de cuentas productivas |
| Potencial de payout | Pendiente | escenarios, nunca valor patrimonial |
| Break-even histórico | Pendiente | gastos acumulados − retiros acumulados |

### Firmas conocidas

| Firma / venue | Cuentas | Estado del inventario | Notas |
|---|---:|---|---|
| Axi Select | Pendiente | Parcial | Aproximadamente US$2.200 de capital desplegado recuperable; no clasificar como gasto hundido |
| FTMO | Pendiente | Por levantar | Prop |
| TTP | **2 funded de 50k** | Parcial | Ambas cuentas han generado refund; montos exactos por asociar a movimientos |
| Orion | **6 históricas / 5 activas** | Parcial | 2×100k + 3×50k + 1×25k Flash; 1×50k lost por inactividad; payouts reales informados US$1.782,26 |
| WSF | Pendiente | Parcial | Compras visibles por US$717,50; estados actuales por levantar |
| The5ers | **1 histórica / 0 activa** | Parcial | High Growth 10k perdida; costo recordado US$400–500, se registra US$500 conservador |
| **Total conocido** | **17** | Parcial | El total 17 original debe reconciliarse para confirmar si incluía esta cuenta histórica perdida |

## 🧮 Modelo económico

El tracker mantiene cuatro capas separadas. No se mezclan aunque una misma cuenta participe en varias.

### 1. Cash out — dinero efectivamente gastado

Registrar cada movimiento pagado con dinero propio:

- compra de challenge/evaluation;
- activation fee;
- reset/retry;
- mensualidad o fee recurrente;
- fee de payout/retiro si aplica;
- conversión, comisión o cargo relevante;
- tooling directamente atribuible al portfolio, sólo si se decide incluirlo.

**Costo histórico acumulado** = suma de todos los cash-out confirmados.

### 2. Cash in — dinero efectivamente recibido

Registrar sólo cash que efectivamente llegó:

- payouts;
- revenue share;
- devoluciones/refunds;
- créditos realizados que reduzcan costo, separados de payouts.

**Retiros acumulados** = suma de payouts efectivamente cobrados.

### 3. Inventario de activos operacionales

Una cuenta se trata como un **activo operacional**, no como cash. Cada cuenta debe tener identidad estable y estado trazable.

Estados base propuestos:

| Estado | Significado económico |
|---|---|
| `planned` | Compra considerada; aún no existe |
| `evaluation` | Challenge/evaluación activa |
| `passed` | Evaluación aprobada; falta activación o transición |
| `funded` | Cuenta financiada y utilizable |
| `payout_eligible` | Cumple condiciones para solicitar payout |
| `paused` | Existe, pero no se está operando |
| `lost` | Cuenta fallada/perdida |
| `closed` | Terminada administrativamente |
| `unknown` | Falta evidencia; no asumir estado |

### 4. Potencial económico

> [!important]+ Potencial ≠ profit
> El potencial sirve para planificación. No debe sumarse al P&L ni al patrimonio.

Se medirán, como mínimo:

- **notional financiado activo:** tamaño nominal de cuentas funded/payout-eligible;
- **capacidad de payout elegible:** cuánto podría retirarse hoy bajo reglas vigentes, cuando sea calculable;
- **run-rate conservador:** escenario basado en payouts históricos reales cuando exista muestra suficiente;
- **run-rate objetivo:** escenario de planificación, etiquetado explícitamente como hipótesis;
- **capital efficiency:** payouts acumulados / cash gastado acumulado;
- **recovery ratio:** porcentaje del gasto histórico ya recuperado;
- **break-even restante:** max(0, gastos − cash-in económico reconocido).

## 🗃️ F0 — Inventario maestro

### Cuentas

Cada cuenta tendrá un ID interno estable aunque cambie su nombre visible.

| ID | Firma | Tipo | Tamaño nominal | Moneda | Fecha compra | Costo inicial | Costos extra | Estado | Balance/equity | Payout eligible | Payout acumulado | Último evento | Evidencia / nota |
|---|---|---|---:|---|---|---:|---:|---|---:|---|---:|---|---|
| ACC-001 | Orion | Evaluación/programa histórico | 100.000 | USD | — | Est. 569,00 | — | funded | — | — | — | — | Costo estimado con promedio conservador de precios actuales comparables |
| ACC-002 | Orion | Evaluación/programa histórico | 100.000 | USD | — | Est. 569,00 | — | funded | — | — | — | — | Costo estimado |
| ACC-003 | Orion | Evaluación/programa histórico | 50.000 | USD | — | Est. 325,67 | — | funded | — | — | — | — | Costo estimado |
| ACC-004 | Orion | Evaluación/programa histórico | 50.000 | USD | — | Est. 325,67 | — | funded | — | — | — | — | Costo estimado |
| ACC-005 | Orion | Evaluación/programa histórico | 50.000 | USD | — | Est. 325,67 | — | lost | — | no | — | Inactividad | Cuenta perdida por inactividad; costo se conserva históricamente |
| ACC-006 | Orion | Flash / proxy actual Zero | 25.000 | USD | — | Est. 499,00 | — | funded | — | — | — | — | Flash no existe como programa actual comparable; se usa Orion Zero 25k como proxy pesimista |
| ACC-007 | TTP | Funded | 50.000 | USD | — | Pendiente | — | funded | — | — | — | — | Refund recibido; monto por asociar |
| ACC-008 | TTP | Funded | 50.000 | USD | — | Pendiente | — | funded | — | — | — | — | Refund recibido; monto por asociar |
| ACC-009 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-010 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-011 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-012 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-013 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-014 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-015 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-016 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-017 | The5ers | High Growth | 10.000 | USD | — | Est. 500,00 | — | lost | — | no | — | Perdida | Owner recuerda costo entre US$400–500; se usa US$500 por criterio pesimista |

### Ledger de gastos

| Fecha | Firma | Cuenta / grupo | Categoría | Moneda original | Monto original | Monto base | Medio | Evidencia | Nota |
|---|---|---|---|---|---:|---:|---|---|---|
| 2025-10-13 | TTP/contexto | Factura 275046 | challenge/fee | USD | 314,10 | 314,10 | Pendiente | Captura factura Paid | Firma inferida por contexto de esta tanda; confirmar |
| 2025-11-02 | TTP/contexto | Factura 290910 | challenge/fee | USD | 261,75 | 261,75 | Pendiente | Captura factura Paid | Confirmar cuenta asociada |
| 2025-11-02 | TTP/contexto | Factura 290911 | challenge/fee | USD | 261,75 | 261,75 | Pendiente | Captura factura Paid | Confirmar cuenta asociada |
| 2025-11-02 | TTP/contexto | Factura 290913 | challenge/fee | USD | 261,75 | 261,75 | Pendiente | Captura factura Paid | Confirmar cuenta asociada |
| 2025-12-01 | TTP/contexto | Factura 313946 | challenge/fee | USD | 398,30 | 398,30 | Pendiente | Captura factura Paid | Confirmar cuenta asociada |
| 2025-12-01 | TTP/contexto | Factura 313948 | challenge/fee | USD | 398,30 | 398,30 | Pendiente | Captura factura Paid | Confirmar cuenta asociada |
| 2025-12-14 | TTP/contexto | Factura 324210 | challenge/fee | USD | 341,40 | 341,40 | Pendiente | Captura factura Paid | Confirmar cuenta asociada |
| 2026-04-01 | WSF | Ultra Two Phase 100K Step-1 #190343 | challenge | USD | 264,50 | 264,50 | Bridgerpay/WSFunded | Captura Paid | |
| 2026-05-03 | WSF | Elite Two Phase 100K Step-1 #205523 | challenge | USD | 377,40 | 377,40 | Bridgerpay/WSFunded | Captura Paid | |
| 2026-09-19 | WSF | Ultra Two Phase 25K Step-1 #282609 | challenge | USD | 75,60 | 75,60 | Bridgerpay | Captura Paid | |
| 2026-09-21 | WSF | Ultra Two Phase 100K Step-2 #283675 | phase_transition | USD | 0,00 | 0,00 | No payment required | Captura Paid | Sin cash-out |
| Estimación 2026-09-23 | Orion | 2×100k | estimated_challenge_cost | USD | 1.138,00 | 1.138,00 | — | Precios actuales consultados | 2 × promedio Standard/Select/Nova 100k = US$569,00 |
| Estimación 2026-09-23 | Orion | 3×50k | estimated_challenge_cost | USD | 977,01 | 977,01 | — | Precios actuales consultados | 3 × promedio Standard/Select/Nova 50k = US$325,67 |
| Estimación 2026-09-23 | Orion | 1×25k Flash | estimated_challenge_cost | USD | 499,00 | 499,00 | — | Precio actual Orion Zero 25k como proxy | Estimación pesimista; no es gasto histórico probado |
| Estimación 2026-09-23 | The5ers | High Growth 10k | estimated_challenge_cost | USD | 500,00 | 500,00 | — | Memoria directa del owner | Rango recordado US$400–500; se usa techo US$500 por criterio pesimista |

Categorías iniciales: `challenge`, `activation`, `reset`, `subscription`, `commission`, `tooling`, `other`.

### Ledger de ingresos / retiros

| Fecha | Firma | Cuenta / grupo | Tipo | Moneda original | Bruto | Fees | Neto recibido | Medio | Evidencia | Nota |
|---|---|---|---|---|---:|---:|---:|---|---|---|
| 2026-01 | Axi Select | Pendiente | payout | USD | 1.038,72 | Pendiente | 1.038,72* | Pendiente | Captura "Tus pagos" Axi Select | Fecha disponible sólo a nivel mes; *monto visible tratado como neto provisional |
| 2026-02 | Axi Select | Pendiente | payout | USD | 43,90 | Pendiente | 43,90* | Pendiente | Captura "Tus pagos" Axi Select | Fecha disponible sólo a nivel mes; *neto provisional |
| 2026-03 | Axi Select | Pendiente | payout | USD | 592,30 | Pendiente | 592,30* | Pendiente | Captura "Tus pagos" Axi Select | Fecha disponible sólo a nivel mes; *neto provisional |
| 2026-04 | Axi Select | Pendiente | payout | USD | 436,79 | Pendiente | 436,79* | Pendiente | Captura "Tus pagos" Axi Select | Fecha disponible sólo a nivel mes; *neto provisional |
| 2026-07 | Axi Select | Pendiente | payout | USD | 63,56 | Pendiente | 63,56* | Pendiente | Captura "Tus pagos" Axi Select | Fecha disponible sólo a nivel mes; *neto provisional |
| 2026-08 | Axi Select | Pendiente | payout | USD | 3,60 | Pendiente | 3,60* | Pendiente | Captura "Tus pagos" Axi Select | Fecha disponible sólo a nivel mes; *neto provisional |
| 2026-04-01 | TTP/contexto | Pago 132082 | cash_in_pending_classification | USD | 80,92 | Pendiente | 80,92* | Pendiente | Captura listado de pagos, estado Completed | Firma asignada por contexto; determinar si corresponde a refund o payout |
| 2026-05-11 | TTP/contexto | Pago 133971 | cash_in_pending_classification | USD | 652,60 | Pendiente | 652,60* | Pendiente | Captura listado de pagos, estado Completed | Determinar refund vs payout |
| 2026-08-24 | TTP/contexto | Pago 136965 | cash_in_pending_classification | USD | 571,22 | Pendiente | 571,22* | Pendiente | Captura listado de pagos, estado Completed | Determinar refund vs payout |
| 2026-09-16 | TTP/contexto | Pago 137652 | cash_in_pending_classification | USD | 314,84 | Pendiente | 314,84* | Pendiente | Captura listado de pagos, estado Completed | Existen 2 refunds TTP según owner; asociar IDs exactos |
| 2025-10-04 | FTMO | Cuenta 22170650 | cash_in_pending_classification | USD | 520,59 | Pendiente | 520,59* | Pendiente | Captura estado Pagado | Puede ser reward o refund; clasificar |
| 2025-11-02 | FTMO | Cuenta 22353341 | cash_in_pending_classification | USD | 632,63 | Pendiente | 632,63* | Pendiente | Captura estado Pagado | Puede ser reward o refund; clasificar |
| 2025-11-02 | FTMO | Cuenta 22353358 | cash_in_pending_classification | USD | 632,63 | Pendiente | 632,63* | Pendiente | Captura estado Pagado | Puede ser reward o refund; clasificar |
| 2025-11-26 | FTMO | Cuenta 22501235 | cash_in_pending_classification | USD | 504,30 | Pendiente | 504,30* | Pendiente | Captura estado Pagado | Puede ser reward o refund; clasificar |
| Fecha pendiente | Orion | Retiro informado por owner | payout | USD | 1.365,82 | Pendiente | 1.365,82 | Pendiente | Declaración directa owner | Cash realmente retirado |
| Fecha pendiente | Orion | Retiro informado por owner | payout | USD | 416,44 | Pendiente | 416,44 | Pendiente | Declaración directa owner | Cash realmente retirado |

**Subtotal Axi Select visible:** **US$2.178,87**.

**Subtotal TTP/contexto visible:** **US$1.619,58**. El owner confirma que existen **2 refunds** asociados a sus dos cuentas funded de 50k; falta identificar cuáles movimientos son refunds y cuáles payouts.

**Subtotal FTMO visible:** **US$2.290,15** en cuatro movimientos con estado Pagado; tipo económico exacto pendiente de clasificar.

**Orion cash realmente retirado:** **US$1.782,26** = US$1.365,82 + US$416,44.

> [!warning]+ Certificado Orion ≠ cash retirado
> El certificado Orion `Overall Rewards = US$2.417,58` se conserva sólo como evidencia de rewards/acumulado de plataforma. **No se usa como cash-in**. La autoridad para retiros reales es la corrección del owner: **US$1.782,26**.

### Reconciliaciones de cash-in

| Firma / fuente | Corte | Total acreditado | Tratamiento actual | Pendiente |
|---|---|---:|---|---|
| Axi Select | 2026-08 | **US$2.178,87** | Payouts visibles; trading cash-in provisional | Asociar a cuentas y confirmar fees/neto |
| Orion | 2026-09-23 | **US$1.782,26** | Dos retiros reales informados por owner | Fechas/fees |
| TTP/contexto | 2026-09-16 | **US$1.619,58** | Cash-in real; mezcla de al menos 2 refunds y posibles payouts | Clasificar IDs |
| FTMO | 2025-11-26 | **US$2.290,15** | Cash-in visible con estado Pagado | Clasificar reward vs refund |

**Cash recibido total acreditado actualmente:** **US$7.870,86**.

**Trading payouts confirmados mínimos:** **US$3.961,13** = Axi US$2.178,87 + Orion US$1.782,26. TTP y FTMO quedan fuera del trading-profit hasta separar refunds/rewards.

### Pipeline de compras

| Oportunidad | Firma | Cantidad | Tamaño | Costo estimado | Motivo | Estado |
|---|---|---:|---:|---:|---|---|
| Expansión próxima | Por definir | ~10 | Por definir | Por definir | Aumentar capacidad del portfolio | planned |

## 🧾 Reglas de verdad

1. **No estimar datos históricos que puedan recuperarse.** Si falta precio, payout o fecha, queda `Pendiente`.
2. **Una compra = un evento del ledger**, incluso si cubre varias cuentas.
3. **Un payout = un evento de ingreso**, asociado a la cuenta o grupo correspondiente.
4. Refunds no se confunden con payouts; reducen costo económico pero no son trading profit.
5. Moneda original siempre se conserva. Si se convierte a USD/CLP para dashboard, guardar además el criterio/tipo de cambio usado.
6. No contar una cuenta `lost` o `closed` dentro del notional activo.
7. No contar cuentas `planned` como inventario adquirido.
8. No sumar balance/equity de una prop al patrimonio personal.
9. Toda métrica estimada o potencial debe declarar su fórmula y supuestos.
10. Ante contradicción entre recuerdo y evidencia, queda `unknown` hasta resolverla.

## 🧭 Roadmap

### F0 — Inventario y reconstrucción histórica · **ACTIVA**

**Objetivo:** saber exactamente qué existe y reconstruir cash-in/cash-out.

Entregables:

- inventario de las 17 cuentas;
- detalle por firma y estado;
- ledger de todos los gastos;
- ledger de todos los payouts/retiros;
- normalización de monedas;
- cálculo de P&L realizado y break-even;
- trazabilidad mínima a evidencia cuando esté disponible.

**Gate F0:** 17/17 cuentas clasificadas + gastos e ingresos históricos razonablemente reconciliados + cero duplicados conocidos.

### F1 — Dashboard financiero y operacional

- KPIs consolidados;
- vistas por firma, estado y cohorte;
- costos por cuenta/firma;
- payout por cuenta/firma;
- recovery ratio;
- capital efficiency;
- aging de cuentas;
- historial de cambios de estado.

### F2 — Potencial y planificación

- escenarios conservador/base/objetivo;
- payout capacity;
- run-rate mensual observado;
- costo y payback de nuevas cuentas;
- comparación de expansión vs capacidad ya ociosa;
- evitar usar nominal financiado como proxy de riqueza.

### F3 — Integración en Loom

Sólo después de estabilizar F0–F2:

- vista dashboard dentro de Loom;
- filtros y drill-down por firma/cuenta;
- actualización simple del estado;
- gráficos de cashflow/P&L;
- fuente Markdown o dataset derivado manteniendo Agents-OS como autoridad mientras siga siendo suficiente.

## 🧱 Entrega de desarrollo

_No aplica por ahora — la primera etapa es inventario/documentación manual en Agents-OS. Si F3 se convierte en desarrollo de Loom, deberá abrirse la entrega técnica correspondiente con repo, branch, base y SPEC antes de implementar._

## 🧩 Subproyectos

No hay subproyectos todavía. Si la integración en Loom crece lo suficiente, debe separarse como entrega de desarrollo y enlazarse desde aquí.

## ✅ Tareas

- [/] Levantar inventario de las 17 cuentas actuales #owner/me #type/admin #area/personal
- [ ] Cargar compras, activaciones, resets y otros gastos históricos #owner/me #type/admin #area/personal
- [/] Cargar payouts/retiros históricos con monto neto efectivamente recibido #owner/me #type/admin #area/personal
- [ ] Clasificar los pagos TTP/contexto 132082, 133971, 136965 y 137652: identificar exactamente los 2 refunds y los posibles payouts #owner/me #type/admin #area/personal
- [ ] Clasificar los 4 movimientos FTMO pagados: reward vs refund #owner/me #type/admin #area/personal
- [ ] Confirmar costo histórico real de The5ers High Growth 10k si aparece factura/cargo #owner/me #type/admin #area/personal
- [ ] Reconciliar gastos e ingresos y calcular P&L realizado + break-even #owner/me #type/admin #area/personal
- [ ] Clasificar cuentas por estado y separar capacidad nominal de valor líquido #owner/me #type/admin #area/personal
- [ ] Definir moneda base del dashboard y política de conversión histórica #owner/me #type/admin #area/personal
- [ ] Construir primera vista de potencial económico con escenarios explícitos #owner/me #type/admin #area/personal
- [ ] Evaluar integración del tracker en [[Loom]] después de estabilizar el modelo #owner/me #type/supervision #area/personal

## 📆 Bitácora

- **2026-09-23** — Axi reclasificado por instrucción del owner: ~US$2.200 corresponden a capital desplegado recuperable, no a gasto hundido. Cash-out bruto consumido conocido se mantiene en US$6.068,86 + FTMO pendiente; cash desplegado total conocido pasa a ~US$8.268,86 + FTMO pendiente.
- **2026-09-23** — Inventario histórico ampliado con The5ers: 1 cuenta High Growth 10k perdida. Costo recordado por el owner entre US$400–500; se registra provisionalmente **US$500** bajo criterio pesimista. Cash-out bruto identificado sube a US$6.068,86. Pendiente reconciliar si esta cuenta estaba incluida o no dentro del universo inicial de 17.
- **2026-09-23** — Segunda carga F0: gastos visibles TTP/contexto US$2.237,35 y WSF US$717,50; Orion inventariado con 6 cuentas históricas, 5 activas y US$325k de notional activo. Se estimó costo Orion en US$2.614,01 con precios actuales y criterio conservador, marcado explícitamente como estimación. Orion cash real corregido a US$1.782,26; el certificado US$2.417,58 deja de contar como retiro. TTP: 2×50k funded con 2 refunds pendientes de asociación. FTMO: cuatro movimientos Pagado por US$2.290,15 pendientes de clasificar como reward/refund.
- **2026-09-23** — Primera evidencia de payouts cargada: 6 pagos Axi Select por US$2.178,87; 4 pagos Completed por US$1.619,58 con firma aún no visible; certificado Orion Overall Rewards por US$2.417,58. Para no inflar resultados, Orion se mantiene como acumulado reconciliable y el lote no identificado no se suma hasta resolver posible solapamiento. Cash-in conservador confirmado: US$4.596,45; máximo provisional si el lote es independiente: US$6.216,03.
- **2026-09-23** — Proyecto creado. Se conoce un universo inicial de 17 cuentas repartidas entre Axi Select, FTMO, TTP, Orion y WSF; detalle por cuenta, gastos y payouts pendiente de inventario. Se deja pipeline separado para una posible expansión de ~10 cuentas.

## 🧭 Decisiones

- **Agents-OS primero, Loom después.** No construir UI hasta que el modelo de datos haya sobrevivido el inventario real.
- **Ledger sobre memoria.** Cash-in y cash-out se reconstruyen como eventos; los totales son derivados.
- **Nominal prop separado del patrimonio.** El tamaño financiado mide capacidad operativa, no riqueza.
- **Realizado separado de potencial.** Los payouts cobrados pertenecen al P&L; escenarios futuros pertenecen a planificación.
- **Refund separado de payout.** Ambos son cash-in, pero refund reduce costo económico y no se contabiliza como trading profit.
- **Estimaciones nunca se disfrazan de gasto probado.** Orion usa por ahora precios actuales como proxy conservador por instrucción del owner; cuando aparezca evidencia histórica, reemplaza la estimación.
- **Capital recuperable separado del gasto.** Axi Select se registra como capital desplegado recuperable (~US$2.200), no como costo hundido mientras conserve esa recuperabilidad.
- **Identidad estable por cuenta.** Cada cuenta recibe `ACC-NNN` para poder seguir cambios de firma, nombre o estado sin perder historia.

## 🔗 Docs / Links

- [[Loom]] — destino posible para una futura visualización/interfaz del tracker.

## 💡 Ideas

### Backlog de ideas

- Importar movimientos desde correos/recibos cuando F0 ya tenga reglas estables.
- Adjuntar screenshots o referencias de dashboards de las props sólo como evidencia, no como fuente única de totales.
- Heatmap por firma: capital gastado vs payouts vs cuentas vivas.
- Curva acumulada cash-out vs cash-in para visualizar el punto de break-even.
- Cohortes por mes de compra para medir payback real.
- Registrar descuentos/cupones para medir costo real, no precio lista.
- Registrar motivo de pérdida de cuenta para detectar concentración de fallos operativos.
- Incorporar cuentas de futuros/Echo Futures cuando existan, sin mezclar reglas de prop CFD con futures.

### Motivos / principios

- **KISS:** primero inventario y ledger; automatización después.
- **YAGNI:** no crear base de datos ni servicio antes de demostrar que Markdown queda corto.
- **Auditabilidad:** todo total debe poder descomponerse en movimientos.
- **Decisiones con cash real:** optimizar por retorno sobre dinero invertido, no por tamaño nominal de cuentas.

### Memoria pública / interna

- **Memoria pública:** no requerida; el proyecto es la fuente canónica del estado.
- **Memoria interna:** no requerida en esta fase.
- **Motivo:** evitar duplicar cifras financieras en varias fuentes.
