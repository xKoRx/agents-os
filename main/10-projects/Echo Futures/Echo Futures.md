---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Echo]]"
parent:
sprint:
start: 2026-09-23
due:
progress: 2
repo:
jira:
prs:
aliases:
  - Futures Prop Automation
  - Echo Futures Trading
tags:
  - kind/project
  - area/echo
created: "2026-09-23"
updated: "2026-09-23"
---

# Echo Futures

%% Naming: Echo Futures es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Futures
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Echo Futures]] arrancar + seguimiento #owner/me #type/supervision #area/personal`

## 🎯 Objetivo

- Convertir la idea inicial de operar futuros fondeados con alta intensidad y alto volumen en un sistema cuantitativo, reproducible y escalable sobre Echo + NinjaTrader, comenzando por definir y validar la operativa, la gestión monetaria y la economía real de las prop firms antes de implementar automatización.
- North star inicial: maximizar **cash neto extraído por unidad de capital real arriesgado y tiempo**, no maximizar balance nominal, cantidad de cuentas ni tasa de aprobación aislada.
- Escala objetivo de largo plazo: operar decenas de cuentas en paralelo (orden de magnitud aspiracional: 40–80) sin que la estrategia, la gestión de riesgo o la reconciliación dependan de trabajo manual por cuenta.

## 📊 Estado actual

- **2026-09-23 — Proyecto creado.** La idea está en fase de discovery operativo; no existe todavía estrategia, gestión monetaria, prop firm, instrumento ni arquitectura de ejecución congelados.
- Hipótesis del owner: estrategias de **win rate alto**, timeframes muy bajos, entradas/salidas rápidas y señales simples que pueden incluir estocásticos u otros filtros; Gerard García, Tradesfera y Psicólogo del Trading son fuentes iniciales de investigación, no autoridades mecánicas todavía.
- Hipótesis de gestión: usar un perfil agresivo al inicio y estudiar el método de hardscalping/recovery atribuido a Gerard García: cuando una posición evoluciona en contra y se cumple un trigger aún por reconstruir, aumentar exposición buscando un rebote y recalcular el objetivo/salida sobre la posición agregada.
- Hipótesis económica: aceptar una tasa alta de cuentas quemadas si el ciclo completo challenge/evaluation → funded → retiro mantiene valor esperado neto positivo después de fees, activaciones, resets, comisiones, slippage y restricciones de payout.
- El sistema debe distinguir **pasar la evaluación**, **sobrevivir funded** y **retirar dinero**; optimizar una sola de esas etapas puede empeorar la economía total.
- El target de 40–80 cuentas es un objetivo de capacidad futura, **no scope del MVP**. El primer vertical slice será una estrategia, una prop/configuración, un instrumento, una Reference y una Execution.
- **Gate actual: RESEARCH_ONLY.** No desarrollar bots NinjaTrader ni integración Echo hasta cerrar G0 Operativa y G1 Economía.

## 🧠 Hipótesis operativa inicial

La idea no se congela como “martingala” ni como “promediar pérdidas” hasta reconstruir evidencia suficiente. El proyecto tratará el hardscalping como una **secuencia de recuperación con aumento de exposición** y deberá identificar exactamente el mecanismo causal y sus límites.

La ventaja que se quiere validar combina cuatro piezas: una entrada base de alta probabilidad, permanencia corta en mercado, capacidad de aumentar exposición bajo condiciones concretas cuando el trade va adverso y un modelo económico de prop donde el downside real por intento está acotado por el coste del challenge/cuenta y sus reglas. La fuerza bruta viene del volumen y de la repetición; no reemplaza la necesidad de demostrar valor esperado positivo.

El riesgo principal es de cola: una técnica con win rate muy alto puede esconder pérdidas raras pero suficientemente grandes para destruir la cuenta. Por eso el KPI principal no será win rate sino **distribución completa de resultados y cash extraído después de cuentas fallidas**.

## 🔬 M0 — Forense de operativa

### Fuentes iniciales

- **Gerard García:** cursos y videos que posee el owner + material público pertinente.
- **Tradesfera:** operativa pública, sesiones, explicaciones y ejemplos relevantes.
- **Psicólogo del Trading:** material público y cualquier contenido del owner que se incorpore explícitamente.
- Cada regla derivada debe guardar fuente, timestamp/lección, evidencia, nivel de confianza y si es suficientemente determinista para automatizar.

### Contrato mínimo a reconstruir por operador/estrategia

- Instrumento(s), sesión y horario efectivo.
- Timeframe de decisión y, si existe, timeframe de contexto.
- Setup completo de entrada: indicadores, parámetros, cruces/niveles, filtros, contexto y condiciones de no-trade.
- Tipo de orden y timing real de entrada.
- Tamaño inicial y unidad de sizing.
- SL y TP iniciales: distancia, fórmula y autoridad para modificarlos.
- **Trigger exacto de aumento de posición:** distancia adversa, estructura, indicador, tiempo, volatilidad u otra condición; no aceptar “cuando se da vuelta” como regla.
- Secuencia de tamaños: cantidad máxima de adds, multiplicador o escalera exacta y exposición total máxima.
- Precio medio ponderado después de cada add.
- Regla exacta de recálculo de SL/TP después de agregar exposición.
- Condición de scratch/breakeven, salida parcial y cierre forzado.
- Qué ocurre si continúa en contra después del último add.
- Stop diario, stop por sesión y número máximo de secuencias fallidas.
- Reglas de noticias, rollover, baja liquidez y desconexión.
- Evidencia de trades ganadores **y perdedores**; no inferir el modelo desde highlights.

### Output G0

G0 queda PASS únicamente cuando exista al menos una estrategia candidata expresable como una máquina de estados sin decisiones humanas ambiguas y con ejemplos que cubran entrada normal, recovery/add, salida ganadora y pérdida completa. Si una regla material sigue siendo “a ojo”, el bot queda bloqueado.

## 💰 M1 — Gestión monetaria y economía de prop

El proyecto modelará la cuenta por **capital económico realmente arriesgable**, no por el balance publicitado de 50K/100K. Cada programa de prop debe normalizar como mínimo: coste de evaluación, activación, resets, profit target, drawdown y su modalidad, daily loss, límites de contratos, consistency, días mínimos, restricciones de scaling/DCA/copier/automatización, reglas de payout, máximo de cuentas y cualquier condición capaz de invalidar esta operativa.

### Estados económicos mínimos

- **EVALUATION_AGGRESSIVE:** perfil orientado a maximizar la probabilidad/velocidad de llegar a funded bajo un presupuesto de intentos explícito.
- **FUNDED_PRE_PAYOUT:** política posiblemente distinta; optimiza probabilidad de llegar al primer retiro.
- **PAYOUT_PROTECTED:** después de retirar, estudiar si conviene reducir riesgo, reciclar beneficio o mantener agresividad.
- Estos nombres son estados de investigación, no reglas congeladas; el análisis puede demostrar que dos o los tres deben usar la misma política.

### Variables de la secuencia hardscalping

- Riesgo inicial (R_0).
- Número máximo de adds (N).
- Tamaño por escalón (q_i).
- Distancia/trigger de cada add.
- Precio medio ponderado de la posición agregada.
- SL/TP agregado y pérdida máxima si falla toda la secuencia.
- MAE/MFE, tiempo expuesto y coste real de comisión/slippage por secuencia.
- Riesgo acumulado por cuenta, por sesión y por conjunto de cuentas correlacionadas.

### Métricas económicas obligatorias

- Probabilidad de pasar evaluation antes de quemarla.
- Probabilidad de primer payout dado que se llegó a funded.
- Probabilidad y coste de ruina por etapa.
- Intentos esperados y coste esperado hasta primer payout.
- Cash neto esperado por intento y por cohorte de cuentas.
- Expected payout / challenge+activation+reset cost.
- Tiempo esperado hasta cashflow y capital lock.
- Distribución P5/P50/P95 y drawdowns; no evaluar solo promedio.
- Efecto de comisiones, slippage, fills parciales y latencia.
- Sensibilidad a rachas: una estrategia 90% WR debe demostrar qué ocurre con la cola del 10%, incluyendo secuencias consecutivas.
- Correlación entre 40–80 cuentas cuando todas siguen la misma Reference; multiplicar cuentas no multiplica independencia.

### Gate G1

No se compra escala ni se construye fan-out multi-account hasta que exista una región de parámetros con EV neto positivo bajo supuestos conservadores y sin depender de una única combinación extremadamente frágil.

## 🧪 M2 — Estrategias candidatas y simulación

- Partir con pocas estrategias mecánicas de alta frecuencia operativa y alto win rate potencial; estocásticos en TF bajos son **candidato**, no decisión.
- Elegir un solo mercado inicial después de evaluar liquidez, tick value, comisiones, horario y compatibilidad con las reglas de la prop.
- Para una lógica de adds y salidas rápidas, exigir resolución de datos suficiente para reconstruir el path intratrade; una barra OHLC que no resuelva el orden de eventos no puede certificar la estrategia.
- El simulador debe reproducir también la prop: challenge/funded/payout, no solo una curva PnL.
- Separar edge de entrada, lógica de recovery y money management para poder medir cuánto aporta y cuánto riesgo agrega cada componente.

## 🏗️ M3+ — Automatización después de validar la operativa

- **M3 — Vertical slice NinjaTrader:** una Reference + una Execution + SIM + un instrumento + una estrategia.
- **M4 — Integración Echo:** identidad, comandos idempotentes, fills, reconciliación, position truth, límites y observabilidad.
- **M5 — Primera evaluation real:** una cuenta/plan con autorización explícita del owner y presupuesto máximo conocido.
- **M6 — Primer payout y aprendizaje:** comparar simulación versus ejecución real, recalibrar slippage/fills/rules.
- **M7 — Scale-out:** fan-out controlado hacia múltiples cuentas solo después de evidencia de retiro; crecer por cohortes y no saltar directo a 40–80.

## 🚦 Gates del proyecto

| Gate | Condición | Estado |
|---|---|---|
| G0 — Operativa | Estrategia + hardscalping completamente mecánicos, incluidos casos de pérdida | **WIP** |
| G1 — Economía | EV de challenge→primer payout positivo con costes y rules reales | BLOCKED by G0 |
| G2 — Simulación | Replay/path intratrade y simulador de prop reproducibles | BLOCKED by G1 |
| G3 — Execution | Reference→Echo→Execution reconciliado en SIM | BLOCKED by G2 |
| G4 — Real pilot | Primera evaluation real dentro de presupuesto explícito | BLOCKED by G3 + owner |
| G5 — Withdrawal | Primer retiro y discrepancias sim/live entendidas | BLOCKED by G4 |
| G6 — Scale | Cohortes multi-account con límites, observabilidad y kill-switch | BLOCKED by G5 |


## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Echo Futures runtime (repo por definir) | TBD tras G0/G1 | TBD | BLOCKED — congelar después de G0/G1 | BLOCKED — congelar después de G0/G1 | NOT STARTED |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [/] Inventariar y organizar corpus de Gerard García: cursos/videos disponibles + material público relevante #owner/me #type/research #area/echo
> - [ ] Reconstruir una estrategia Gerard completa con evidencia y reglas mecánicas, incluyendo add/recovery y pérdida total #owner/me #type/research #area/echo
> - [ ] Investigar y mecanizar operativa relevante de Tradesfera #owner/me #type/research #area/echo
> - [ ] Investigar y mecanizar operativa relevante de Psicólogo del Trading #owner/me #type/research #area/echo
> - [ ] Comparar setups y seleccionar 1–3 candidatos de alto win rate / TF bajo para validación #owner/me #type/research #area/echo
> - [ ] Definir modelo matemático del hardscalping: triggers, escalera de contratos, promedio, SL/TP agregado y pérdida máxima #owner/me #type/research #area/echo
> - [ ] Construir shortlist inicial de prop firms/planes y normalizar rules que afectan la operativa #owner/me #type/research #area/echo
> - [ ] Modelar challenge→funded→primer payout con fees, resets, drawdown, consistency, slippage y comisiones #owner/me #type/research #area/echo
> - [ ] Elegir primer instrumento solo después de cruzar microestructura + estrategia + rules de prop #owner/me #type/research #area/echo
> - [ ] Cerrar G0 y G1 antes de autorizar SPEC/implementación NinjaTrader/Echo #owner/me #type/supervision #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-23** — Proyecto creado y alcance corregido hacia operativa-first. Se registran como hipótesis: estrategias de alto win rate y TF bajo, hardscalping/recovery con aumento de exposición, gestión agresiva orientada a challenge/funded/payout y escalado futuro a decenas de cuentas. G0/G1 bloquean desarrollo hasta demostrar reglas mecánicas y economía positiva.

## 🧭 Decisiones

- **2026-09-23 — Echo Futures es una iniciativa raíz bajo [[Echo]], relacionada con [[Trading]], y no un tercer track de [[Echo — Producto Integrado]].**
- **2026-09-23 — Operativa-first:** estrategia, hardscalping, money management y prop economics se definen antes de arquitectura o desarrollo.
- **2026-09-23 — “Quemar cuentas hasta retirar” se modela como hipótesis económica falsable:** el criterio es cash neto y distribución de resultados, no pass rate ni win rate aislados.
- **2026-09-23 — No etiquetar la técnica de Gerard como martingala sin evidencia:** reconstruir trigger, sizing, límites y salida exactos.
- **2026-09-23 — Escala 40–80 cuentas es target de capacidad, no MVP:** el sistema escala por cohortes después de obtener evidencia real de payout.
- **2026-09-23 — Reference/Execution de Echo se conserva como dirección arquitectónica, pero su SPEC queda bloqueada hasta G0/G1.**

## 🔗 Docs / Links

- [[Echo]] — área de producto y automatización.
- [[Trading]] — área relacionada para operativa, prop firms y riesgo.
- [[Echo — Producto Integrado]] — producto vigente; Echo Futures se mantiene independiente para no alterar sus dos tracks congelados.
- [[Echo + Echo Forge — Environment Contract]] — será autoridad de ambiente si Echo Futures reutiliza infraestructura Echo/Aranea; no concede autorización de ejecución.

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- Cohortes de cuentas con perfiles de agresividad distintos para estimar experimentalmente la frontera pass-rate / payout-rate / burn-rate.
- Risk profile dinámico por estado económico de la cuenta en vez de una gestión única.
- Reference única con fan-out a muchas Executions y límites locales por cuenta.
- Simulador Monte Carlo sobre secuencias de trades reales para estimar costo hasta payout y riesgo de cola.
- Clasificar cuentas como inventario económico: evaluation, funded pre-payout, payout-protected, burned, retired.

### Motivos / principios

- **Operativa antes que software.**
- **Cash retirado > balance nominal > win rate.**
- **High win rate no elimina tail risk.**
- **Force brute solo sirve si el EV neto después de quemas es positivo.**
- **KISS:** una prop, un instrumento y una estrategia antes de multiplicar cuentas.
- **YAGNI:** no construir multi-prop, multi-market ni 80-account fan-out antes de demostrar primer payout.
- **Separación SOLID:** signal/strategy, recovery logic, money management, prop rules y execution deben ser medibles y reemplazables por separado.

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** por definir cuando G0/G1 produzcan reglas reutilizables verificadas.
- **Memoria interna:** no requerida para crear el proyecto; continuidad vive en esta nota hasta que exista delta durable específico.
- **Motivo:** evitar convertir hipótesis tempranas en memoria canónica.
