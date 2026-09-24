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
> **Inventario detallado:** pendiente de levantar.
> **Gastos históricos:** pendiente de consolidar.
> **Retiros / payouts:** evidencia parcial cargada — Axi Select US$2.178,87 + lote no identificado US$1.619,58 + certificado acumulado Orion US$2.417,58.
> **Cash-in confirmado sin doble conteo:** **US$4.596,45 mínimo**; **US$6.216,03 máximo provisional** si el lote de 4 pagos no pertenece a Orion.
> **P&L realizado neto:** no calculable todavía porque faltan gastos históricos y resolver el origen del lote no identificado.
> **Expansión:** posible compra de aproximadamente 10 cuentas adicionales; se registra como pipeline, **no como activo existente**.

> [!warning]+ Regla contable clave
> El balance nominal de una cuenta prop **no es patrimonio líquido ni ganancia**. Se registra como **capacidad financiada / notional gestionable**. Un payout sólo se convierte en profit realizado cuando fue efectivamente cobrado. Una cuenta activa puede tener valor económico operacional, pero no se suma como cash.

### Dashboard económico

| Métrica | Valor actual | Regla |
|---|---:|---|
| Cash gastado acumulado | Pendiente | Compras + resets + activaciones + fees + tooling atribuible |
| Cash retirado acumulado | **US$4.596,45 mínimo confirmado** | Axi US$2.178,87 + Orion acumulado US$2.417,58; lote no identificado de US$1.619,58 no se suma hasta descartar solapamiento |
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
| Axi Select | Pendiente | Por levantar | Broker/programa |
| FTMO | Pendiente | Por levantar | Prop |
| TTP | Pendiente | Por levantar | The Trading Pit |
| Orion | Pendiente | Payout acumulado acreditado | Certificado Overall Rewards: **US$2.417,58** al 2026-09-23; falta desglose por pago |
| WSF | Pendiente | Por levantar | Nombre/entidad exacta a normalizar al inventariar |
| **Total conocido** | **17** | Parcial | Distribución por firma pendiente |

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
| ACC-001 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-002 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-003 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-004 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-005 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-006 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-007 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-008 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-009 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-010 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-011 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-012 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-013 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-014 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-015 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-016 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |
| ACC-017 | Pendiente | Pendiente | — | — | — | — | — | unknown | — | — | — | — | — |

### Ledger de gastos

| Fecha | Firma | Cuenta / grupo | Categoría | Moneda original | Monto original | Monto base | Medio | Evidencia | Nota |
|---|---|---|---|---|---:|---:|---|---|---|
| — | — | — | — | — | — | — | — | — | Pendiente de carga |

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
| 2026-04-01 | **Firma pendiente** | Pago 132082 | payout | USD | 80,92 | Pendiente | 80,92* | Pendiente | Captura listado de pagos, estado Completed | ID 132082; firma no visible en la evidencia |
| 2026-05-11 | **Firma pendiente** | Pago 133971 | payout | USD | 652,60 | Pendiente | 652,60* | Pendiente | Captura listado de pagos, estado Completed | ID 133971; firma no visible en la evidencia |
| 2026-08-24 | **Firma pendiente** | Pago 136965 | payout | USD | 571,22 | Pendiente | 571,22* | Pendiente | Captura listado de pagos, estado Completed | ID 136965; firma no visible en la evidencia |
| 2026-09-16 | **Firma pendiente** | Pago 137652 | payout | USD | 314,84 | Pendiente | 314,84* | Pendiente | Captura listado de pagos, estado Completed | ID 137652; firma no visible en la evidencia |

**Subtotal Axi Select visible:** **US$2.178,87**.

**Subtotal lote de 4 pagos con firma pendiente:** **US$1.619,58**.

> [!warning]+ Control de doble conteo — Orion
> El certificado de Orion del 2026-09-23 acredita **Overall Rewards = US$2.417,58**. Se registra como **total acumulado reconciliable**, no como una quinta transacción del ledger, porque todavía no sabemos si los cuatro pagos con IDs 132082/133971/136965/137652 pertenecen a Orion y están incluidos en ese acumulado.

### Reconciliaciones de payouts

| Firma / fuente | Corte | Total acreditado | Tratamiento actual | Pendiente |
|---|---|---:|---|---|
| Axi Select | 2026-08 | **US$2.178,87** | Suma de 6 pagos visibles; aditivo | Asociar a cuentas y confirmar fees/neto |
| Orion | 2026-09-23 | **US$2.417,58** | Total acumulado certificado; aditivo respecto de Axi, no desglosado | Obtener eventos individuales |
| Firma pendiente — pagos 132082/133971/136965/137652 | 2026-09-16 | **US$1.619,58** | **No aditivo todavía** por posible solapamiento con Orion | Identificar firma |

**Cash-in confirmado conservador sin doble conteo:** **US$4.596,45** = Axi US$2.178,87 + Orion US$2.417,58.

**Cash-in provisional máximo si el lote pendiente es de otra firma:** **US$6.216,03**.

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
- [ ] Identificar la firma de los pagos 132082, 133971, 136965 y 137652 y descartar/confirmar solapamiento con Orion #owner/me #type/admin #area/personal
- [ ] Reconciliar gastos e ingresos y calcular P&L realizado + break-even #owner/me #type/admin #area/personal
- [ ] Clasificar cuentas por estado y separar capacidad nominal de valor líquido #owner/me #type/admin #area/personal
- [ ] Definir moneda base del dashboard y política de conversión histórica #owner/me #type/admin #area/personal
- [ ] Construir primera vista de potencial económico con escenarios explícitos #owner/me #type/admin #area/personal
- [ ] Evaluar integración del tracker en [[Loom]] después de estabilizar el modelo #owner/me #type/supervision #area/personal

## 📆 Bitácora

- **2026-09-23** — Primera evidencia de payouts cargada: 6 pagos Axi Select por US$2.178,87; 4 pagos Completed por US$1.619,58 con firma aún no visible; certificado Orion Overall Rewards por US$2.417,58. Para no inflar resultados, Orion se mantiene como acumulado reconciliable y el lote no identificado no se suma hasta resolver posible solapamiento. Cash-in conservador confirmado: US$4.596,45; máximo provisional si el lote es independiente: US$6.216,03.
- **2026-09-23** — Proyecto creado. Se conoce un universo inicial de 17 cuentas repartidas entre Axi Select, FTMO, TTP, Orion y WSF; detalle por cuenta, gastos y payouts pendiente de inventario. Se deja pipeline separado para una posible expansión de ~10 cuentas.

## 🧭 Decisiones

- **Agents-OS primero, Loom después.** No construir UI hasta que el modelo de datos haya sobrevivido el inventario real.
- **Ledger sobre memoria.** Cash-in y cash-out se reconstruyen como eventos; los totales son derivados.
- **Nominal prop separado del patrimonio.** El tamaño financiado mide capacidad operativa, no riqueza.
- **Realizado separado de potencial.** Los payouts cobrados pertenecen al P&L; escenarios futuros pertenecen a planificación.
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
