---
type: prompt
schema_version: 1
status: active
area: "[[Echo]]"
target: "TOP LOCAL IMPLEMENTATION LEAD — BTG-S03"
prompt_version: 1
inputs:
  - "BTG-S02-DESIGN reparado en master (d8ec80927307f27378bd6dd76c6a1d0478f6fee6)"
  - "Evidencia S01 (codex/btg-s01-evidence @ e4a177eb) y workspace Aranea reutilizable"
  - "Repo producto xKoRx/echo carril codex/btg-s01-real-diagnostics @ 77e188bc"
outputs:
  - "BTG-S03-IMPLEMENTATION"
  - "CANDIDATE_READY_FOR_PRIMARY_REVIEW"
application:
project: "[[Echo Futures]]"
aliases: []
related:
  - "[[BTG-PLAN]]"
  - "[[BTG-S02-DESIGN]]"
tags:
  - kind/prompt
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S03-OWNER-MANDATE-20261006

Mandato Owner recibido el 2026-10-06 (America/Santiago), preservado verbatim como autoridad del shot S03. Toda decisión de S03 se adjudica contra este texto; en conflicto con instrucciones supersedidas del diseño/BTG-PLAN, prevalece este mandato.

## Mandato — sección /goal verbatim; las demás secciones son RESUMEN ESTRUCTURADO del original (rotulación corregida por delta 2026-10-07; el original completo vive en el hilo Owner del 2026-10-06)

# ECHO FUTURES — BTG-S03
# IMPLEMENTACIÓN: MOTOR FIEL, STRATEGY/MM INTERCAMBIABLES, BASIC + CAMPAIGN

ROLE: TOP / GPT-6 Sol, o identificador equivalente realmente disponible en el harness, sin falsear modelo.
SURFACE: LOCAL.
WORK FUNCTION: implementation lead.
EXECUTION: ONE-SHOT fresh-context. Puedes delegar especialistas LOCAL ONE-SHOT con ownership disjunto; sigues siendo ejecutor, no Primary Manager ni submanager permanente. No aceptas tu propio gate.

## /goal

Entregar un candidato ejecutable de los DOS modos del mismo backtester: BASIC de USD100.000 continuos y CAMPAIGN de caja USD5.000, compra USD120, una cuenta operando, hasta cuatro cobros por cuenta y reinversión. Ejecutar histórico auténtico con Strategy/MM compartidos y preparar evidencia suficiente para S04 adversarial LOCAL y S05 corrección/resultados.

Prioridad Owner vigente: «No quiero una estrategia ganadora: quiero que el motor ejecute la estrategia como en real. Strategy y MM deben poder cambiar sin modificar el motor. KISS/YAGNI. No perder tiempo mejorando ROI».

El programa conserva cinco shots; éste es S03. Fecha límite Owner: 7 de octubre de 2026, America/Santiago. No planificar S06, nueva fase de diseño o una plataforma adicional. No comprar tiempo reduciendo la fidelidad o declarando pruebas inexistentes.

## /frozen (RESUMEN ESTRUCTURADO — no verbatim; rotulación corregida 2026-10-07)

1. Entregar motor, no optimizar estrategia: S2/Gerard como configuración de prueba (SL2000/TP1500, NO_ADDS y CONFIGURED explícitos); sin barrido de rentabilidad, ranking, holdout ni tuning; T30 = SUPERSEDED_BY_OWNER_SCOPE; T38 acotada a propagación de configuración; resultado negativo aceptable.
2. Strategy y MM intercambiables: el núcleo consume contratos; el conocimiento de ModuleS2/timeframes (ohlc_driver/requireNativeWarmup) migra al módulo/contrato compartido; MM entra por el contrato MoneyManager compartido; sin switches por strategy_id, reflect, DSL ni plugins; sustitución probada por los mismos seams del runtime.
3. Paridad y causalidad: runtime/backtester mismos inputs → iguales decisiones; OHLC1m sin ticks funciona; forming sin fuga de extremos futuros; SL-first, reservas, q_exec_max intactos; separar equivalencia de dominio de corrección de venue.
4. KISS y costo: generador intrabar lazy, buffers acotados, streaming; benchmark real pequeño antes de corridas extensas; sin -race en backtest largo; atajos sólo con T35/T36.
5. Dos modos, no dos engines: BASIC 100k continuo sin lifecycle prop; CAMPAIGN caja 5000, compra ON_DEMAND 120, 5000→4880 tras compra, burn no re-debita caja, payout acredita sólo al cobrar, sin quinta cobranza, retiro al cuarto cobro; perfil funcional S02 como FUNCTIONAL_ASSUMPTIONS; F1 continuidad total durante pausa/burn/reemplazo (sólo cambia el compartimento de cuenta; sin rewarmup ni traslado de estado).

## /baseline (resumen)

Producto xKoRx/echo carril codex/btg-s01-real-diagnostics @ 77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626; source ejecutado d69d03eceeac1495522473a95baf08087f5c28b3; incluye dependencias S01; no volver a cd451972 perdiendo soporte OHLC. Evidencia S01 @ e4a177eb (codex/btg-s01-evidence): NQZ3 trading 2023-10-29→2023-11-23 UTC, 113 operaciones materializadas, 39 con fills, 78 fills, neto −USD34.293,32, fresh reproduce IDENTICAL, perfil NO_ADDS; no demuestra scaling ni trece contratos continuos. Originales ya entregados en daedalus:/home/hermes-ops/echo-dev/history/nq/ (13 NQ *-*.Last.txt); reutilizar inventario y derivados con provenance, originales intactos. CURRENT_TASK_STATE = IMPLEMENTATION_NOT_STARTED_UNLESS_NEW_EVIDENCE.

## /verify (resumen)

Matriz S02 aplicable: T01–T29, T31–T34, T37; T35/T36 sólo para atajos implementados; T38 acotada a parametrización; T30/holdout/ranking fuera del gate. Dos comprobaciones nuevas pequeñas y decisivas: (a) sustituir Strategy sin cambiar código del motor, respetando requisitos/timeframes/readiness del módulo, y sustituir MM independientemente, comparando caminos runtime/backtest sin duplicar implementación de prueba dentro del engine; (b) cambiar parámetros declarados de los módulos conserva el engine idéntico y cambia la configuración efectivamente consumida (no basta editar un JSON que nadie lee). Probar causalidad, fills/costos, adds adversos/pyramiding, no-adds explícito común, continuidad tras reemplazo, caja5000→4880, no quinto payout, gaps/DST/rollover y reproducción; pathways críticos y policy de coverage del repo, sin pruebas de relleno. Lifecycle se demuestra con escenarios controlados aunque la estrategia real pierda o nunca retire; no alterar señales para producir payout histórico; histórico auténtico obligatorio para el resultado real, fixtures no lo sustituyen.

## /execute (orden del Owner)

1. Limpieza administrativa: retirar rama codex/btg-s02-design-cloud-20261006 de xKoRx/agents-os recuperando el feedback original desde 00514fe65d0b4a06975096de17a3c2246d573c92 antes de eliminar; publicar delta documental en master con control de concurrencia y readback; verificar ausencia de la ref.
2. Registrar este delta Owner en el documento de control/diseño vigente (único change log) y guardar este mandato por el contrato prompt.
3. Implementar separación mínima de composición y configuración compartida; sustituibilidad y continuidad antes de ensamblar campañas.
4. Completar fuentes/ejecución causal existentes, ambos modos y exports; ejecutar pruebas focalizadas y los primeros BASIC/CAMPAIGN reales. No devolver sólo READY_TO_RUN.
5. Medir y corregir; entregar candidato a revisión del Primary para S04. No ejecutar el adversarial independiente de S04.

## /close (resumen)

Evidencia compacta en master de Agents-OS bajo main/10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTG-S03-IMPLEMENTATION.md, actualizando control por delta. Workers ONE-SHOT con agent-run-register/feedback/session-close cuando corresponde. S03 devuelve CANDIDATE_READY_FOR_PRIMARY_REVIEW. Handoff máximo 10 líneas con los campos STATE/CODE_SHA/AGENTS_OS_SHA, BASIC_REAL, CAMPAIGN_REAL/CASH_RECONCILIATION, STRATEGY_AND_MM_SUBSTITUTION, RUNTIME_PARITY_SCOPE, SCALING/HISTORICAL_COVERAGE, REPRODUCIBILITY/PERFORMANCE, AGENTS_OS_OLD_BRANCH_CLEANUP, MATERIAL_FINDINGS/ARTIFACT, NEXT=S04_LOCAL_INDEPENDENT_ADVERSARIAL.
