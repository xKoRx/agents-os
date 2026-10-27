---
type: project
schema_version: 1
owner: me
root: false
status: active
priority: P1
area: '[[Trading]]'
parent: '[[Echo — I+D de Estrategias]]'
start: '2026-10-27'
progress: 0
repo: xKoRx/echo
aliases:
  - Echo Futures I+D
  - Investigación continua Futures
tags:
  - kind/project
  - area/trading
  - project/echo-rnd
  - tech/futures
created: '2026-10-28'
updated: '2026-10-27'
related:
  - '[[Echo Futures]]'
  - '[[Echo I+D — Cobertura Futures]]'
---

# Echo I+D — Futures

## 🎯 Objetivo

Conducir la división Futures de [[Echo — I+D de Estrategias]]: descubrir, especificar, desarrollar mediante los owners técnicos, cualificar y evaluar estrategias que puedan pasar challenges y producir retiros funded con economía completa verificable.

Prioridad inmediata: **NQ**, aprovechando el trabajo existente y reduciendo incertidumbre útil para la futura salida a producción. La investigación no declara listo el runtime ni autoriza operaciones. La metodología admite otras familias, instrumentos y fuentes cuando el Owner amplíe el alcance.

## 📊 Estado actual

**2026-10-27 — línea de gestión organizada; FUT-R01 listo para asumir, sin campaña nueva.**

- Existen motor, laboratorio, identidades, recibos y metodología técnica. [[Echo Futures — Optimización de Campañas]] sigue siendo planner de su entrega acotada y del laboratorio; no se duplica.
- [[30-resources/agents/skills/echo-retester-master/SKILL|echo-retester-master]] posee desarrollo/corrección y cualificación G0–G5. Se usa antes de desarrollar y antes de campañas.
- La matriz [[Echo I+D — Cobertura Futures]] propone celdas y mapea implementación conocida. Ninguna fila representa alpha validado o candidato aceptado.
- **Proveedor/programa actual: pendiente de decisión Owner.** E2T/GAU50 es escenario histórico versionado. El Owner aclaró que esas cuentas ya no sirven y nunca fueron operadas.
- Último ClutiFX consultado: [[10-projects/Echo Futures/artifacts/clutifx-strategy-research/e05r1/CLF-E05R1-STATUS|E05R1]], en REVIEW, sin elegibles G5. K05/E05R1 superseden partes de Q04; no reutilizar “sin defecto técnico” o “catálogo ausente” como estado actual.
- Datos NQ y capacidad física deben revalidarse cuando se despache ejecución. La organización actual no prueba disponibilidad on-host.

`progress: 0` corresponde al arranque de esta línea, no a la investigación total ni al avance de sus componentes históricos.

## 🧱 Entrega de desarrollo

_No aplica a este planner de investigación. El trabajo Go, fixtures ejecutables, cambios del Backtester o configuración ejecutable se prepara y ejecuta en Hefesto dentro del proyecto técnico autorizado, con branch/base y SPECs. La gestión Cloud puede leer y discutir evidencia, pero no simula una certificación física._

## 🧩 Iniciativas y autoridades

| Trabajo | Autoridad y relación |
|---|---|
| Laboratorio y búsqueda acotada de geometría/MM | [[Echo Futures — Optimización de Campañas]], subproyecto de esta línea. Sus objetivos históricos de cinco candidatas/25% pertenecen a ese encargo; no son cuotas universales del programa. |
| TG/FBC/ORB/MR y campañas anteriores | [[TRADESGERARD-CONTROL]] y catálogo/recibos del lab; evidencia existente que debe mapearse a celdas, no reejecutarse por defecto. |
| ClutiFX | [[CLUTIFX-STRATEGIES-MASTER]], biblioteca MKE, K05 y E05R1; línea secundaria y fuente de aprendizaje. No bloquea nuevas familias. |
| Universo de props | [[Echo Futures — Futures Prop Universe]], resultado histórico de D1 y punto de partida para actualización first-party cuando corresponda. |
| Economía de ciclo completo | [[Echo Futures — Prop Economics Experiment]], evidencia histórica reutilizable; no autoridad del producto actual. |
| Producto y runtime | [[Echo Futures]], [[Echo Futures — Runtime Pools]] y owners técnicos: dependencias para integración/promoción, con sus gates propios. |

## Roadmap de la línea

| Tramo | Pregunta y salida | Condición de avance |
|---|---|---|
| **FUT-R01 — Baseline NQ, cobertura efectiva y mandato económico** | Qué existe realmente, qué se reutiliza, qué perfil actual evaluar y cuál es la siguiente investigación que aporta información. | Inventario por identidad/celda, vigencia de evidencia, alternativas y decisión Owner preparada. |
| Especificación del experimento elegido | Qué comportamiento esperamos y qué resultado lo refutaría; fuente, operacionalización y MM separados. | Spec determinista revisable, datos/versiones, presupuesto y autorización de ejecución. |
| Implementación y cualificación | ¿El código y las operaciones se comportan como la teoría operacionalizada? | G0–G4 propios según retester; corregir o bloquear donde falte evidencia. |
| Histórico y economía completa | ¿El candidato conserva utilidad después de selección/costes y en challenge/funded? | G5 sólo cuando corresponda; receipts de fase, sensibilidad y limitaciones; revisión Owner. |
| Adopción o cierre de investigación | ¿Continuar, corregir, aparcar, rechazar o proponer adopción? | Evidencia conservada, cobertura actualizada, próxima celda definida. La adopción se remite al owner runtime. |

Cada vuelta puede terminar antes del histórico si refuta una regla, demuestra duplicidad, falta de datos o incompatibilidad. No saltar G2C/G4 cambiando el nombre del trabajo a “research”. No optimizar reiteradamente sobre datos ya vistos como si fueran holdout.

## Primer trabajo: FUT-R01

**Estado:** READY_FOR_MANAGER; no motores ni código. **Responsable:** manager Futures con el Owner. **Celdas:** transversal a las celdas NQ de la matriz; habilita su selección sin pretender cubrirlas científicamente.

### Alcance

1. Recuperar los HEAD/branches, catálogos, recibos y datasets necesarios por lectura enfocada. Distinguir evidencia actual, superseded, incompleta y pendiente de aceptación.
2. Mapear TG/FBC/ORB/MR/ClutiFX a hipótesis, variantes, configuración y MM. FBC es NY FIRST CANDLE; no usar su nombre como evidencia de failed breakout.
3. Identificar duplicados de señal demostrados, solapamientos por investigar y huecos reales de mecanismo/contexto.
4. Preparar la selección del Provider/Program/RuleSet actual usando fuentes oficiales vigentes, restricciones de automatización/sesión y compatibilidad del simulador. No elegirlo por las antiguas cuentas E2T ni comprar cuentas.
5. Presentar un primer mandato candidato y una alternativa de mecanismo distinto, con hipótesis, refutador, evidencia previa, datos, coste de preparación, gates y presupuesto pendiente o autorizado.
6. Coordinar dependencia runtime y capacidad compartida sin reabrir sus implementaciones.

### Salida verificable

- Una tabla por identidad con fuente, celda, SHA/recibo, gates, estado económico y aceptación separados.
- Decisiones requeridas para un perfil comercial actual; desconocidos explícitos.
- Una recomendación de primera investigación y alternativa, sin candidatos falsamente validados.
- Mandato siguiente listo para aceptación del Owner y actualización de matriz/planner.

**No incluye:** ejecución Go, motores, adquisición de datos, mutación de cuentas, producción ni auditoría exhaustiva nueva de ClutiFX. Si falta una prueba física, emitir un encargo acotado y autorizado para Hefesto.

## Economía y evidencia

El objetivo es el recorrido **challenge → funded → retiro**, incluyendo supervivencia y costes. Registrar fase y modo efectivo; `CHALLENGE_PASSED` no demuestra retiro y una cuenta funded inicializada para estudio debe tener origen/supuestos explícitos.

Las métricas vigentes y los contratos viven en el lab y en el perfil versionado: todas las compras en el denominador, pases/pérdidas/pendientes separados, comisiones/slippage, fees/renovaciones, tiempo, sequías y sensibilidad. No reinterpretar los resultados históricos con reglas comerciales nuevas sin una nueva identidad de experimento.

Los perfiles Strategy, MM y Provider se mantienen separados. El resultado cambia si cambia uno de ellos; un candidato no hereda PASS ni rentabilidad de otra combinación. El gate trimestral es filtro de cómputo, no validación estadística suficiente. Un diagnóstico de imposibilidad con los trades observados no prueba imposibilidad universal de la fuente.

## ✅ Tareas

- [ ] FUT-R01: asumir baseline, vigencia de evidencia, cobertura NQ y preparar decisiones de perfil/primer mandato. #owner/me #type/research #area/trading
- [r] [[Echo Futures — Optimización de Campañas]] implementar y revisar el laboratorio por shots. Puente transferido desde Echo Futures, conservando REVIEW; no se acepta la entrega por la reorganización. #owner/me #type/supervision #area/echo
- [ ] Decidir perfil económico y presupuesto inicial de Futures con las alternativas de FUT-R01. #owner/me #type/research #area/trading
- [ ] Elegir el primer experimento y una siguiente pregunta de mecanismo diferente; luego despachar sólo el alcance autorizado. #owner/me #type/research #area/trading

Futures Prop Universe es una entrega histórica cerrada, normalizada de `complete` a `completed`; Prop Economics ya estaba cerrado. Enlazarlos no reactiva sus tareas ni equivale a certificar reglas actuales.

## 📆 Bitácora

- **2026-10-27** — Línea incorporada al programa único por mandato Owner. NQ inmediato, economía challenge+retiros, perfil comercial actual por seleccionar. Puente de Optimización transferido conservando REVIEW. Retester y runbook alineados con conformidad teoría→regla→código y sin excepciones de rareza que omitan G2C. No se ejecutaron campañas ni se aceptaron gates.

## 🧭 Decisiones y pendientes

Aceptadas: dos mercados dentro del mismo programa; Futures por Echo Backtester; NQ inmediato; prioridad económica challenge+funded; Owner decide lo material. La ampliación a otros instrumentos y SQX como generación adicional quedan aparcadas, sin ejecutar ni integrar.

Pendientes: Provider/Program/RuleSet actual, primer experimento, riesgos/MM/presupuesto, y decisiones ClutiFX que sólo afecten su propia línea. La propuesta de cobertura y orden dentro de mecanismos no son una shortlist aceptada.

## 🔗 Docs / Links

- [[Echo — I+D de Estrategias]] · [[Echo I+D — Cobertura Futures]] · [[Echo I+D — Mapa de capacidades]].
- [[30-resources/agents/skills/echo-futures-research-manager/SKILL|Manager Futures]].
- [[30-resources/runbooks/echo-rnd-cycle-runbook|Ciclo de investigación y mejora]].
- [[30-resources/runbooks/echo-futures-strategy-qualification-runbook|Cualificación técnica Futures]].

## Entrada del próximo chat

> Actúa como manager de la línea Futures del programa Echo I+D. Repositorio `xKoRx/agents-os`, vault `main/`: ejecuta el bootstrap si es una sesión nueva y carga `echo-futures-research-manager`. Lee [[Echo — I+D de Estrategias]] y esta nota. Retoma **FUT-R01**, conserva NQ como alcance inmediato y la separación Strategy/MM/Provider. Organiza el primer mandato conmigo, verifica el estado vigente y distingue propuestas de decisiones aceptadas. Este arranque no autoriza motores, código, cuentas ni producción; prepara el siguiente paso con evidencia y límites concretos.
