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

## /authorities

En cold start, cargar Agents-OS vigente por su bootstrap; en warm, sólo deltas. Autoridades de xKoRx/agents-os:
- main/80-agents/agents-os/agents-os.md
- main/30-resources/agents/skills/technical-project-manager/SKILL.md
- main/10-projects/Echo Futures/Echo Futures.md
- main/10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTG-S02-DESIGN.md
- main/10-projects/Echo Futures/artifacts/backtester-stage2-real/BTG-S01-REAL-GERARD-RESULT.md y BTG-S01-REAL-GAP-FORENSICS.md
- Contrato de ambientes Echo y router Aranea aplicables, antes de acceder a infraestructura.

Diseño reparado publicado en master: d8ec80927307f27378bd6dd76c6a1d0478f6fee6; cierre documental posterior: 920012e3239765d876f7611ab4f3363eff97fa5e. Su existencia NO demuestra tests ni implementación.

Orden de autoridad: mandato Owner actual y este despacho > instrucciones supersedidas del diseño/BTG-PLAN > cortes históricos. F1 continuidad y F2 generación lazy se conservan. F3 deja de exigir búsqueda de rentabilidad: configuración sigue, optimización NO.

## /baseline

Producto: xKoRx/echo, carril codex/btg-s01-real-diagnostics, tip 77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626; source ejecutado d69d03eceeac1495522473a95baf08087f5c28b3. Incluye dependencias S01; no volver a cd451972 perdiendo soporte OHLC. Refrescar HEAD, dirty state y deltas materiales antes de mutar.

Evidencia S01: e4a177ebca60c95062fbc30bc8a97ceb3be31c04, codex/btg-s01-evidence. Baseline NQZ3, trading 2023-10-29→2023-11-23 UTC; 113 operaciones materializadas, 39 con fills, 78 fills, neto −USD34.293,32, fresh reproduce IDENTICAL. Perfil NO_ADDS; no demuestra scaling ni trece contratos continuos.

Originales YA ENTREGADOS: daedalus:/home/hermes-ops/echo-dev/history/nq/, 13 archivos NQ *-*.Last.txt. Hay inventario y derivados con provenance: reutilizarlos, originales intactos. No volver a pedir exportación Windows ni ZIP.

CURRENT_TASK_STATE = IMPLEMENTATION_NOT_STARTED_UNLESS_NEW_EVIDENCE.
ACCEPTED_INPUT = diseño reparado con las precisiones de este mandato + evidencia S01 acotada.
OPEN = implementación, desacoplamiento, paridad física, ambos modos y cobertura/rollover.

## /frozen

### 1. Entregar motor, no optimizar estrategia

No cambiar entradas/salidas, indicadores, filtros, SL/TP o scaling para aumentar ROI. Mantener S2/Gerard como configuración de prueba: SL2000/TP1500; NO_ADDS y CONFIGURED explícitos según diseño. Parámetros configurables; defaults funcionales no son reglas de una prop ni autorización LIVE.

NO implementar ni ejecutar barrido1000/1500/2000, ranking, selección de ganador, holdout de rentabilidad, optimizer ni tuning. Marcar esa parte de F3/§11/T30 como SUPERSEDED_BY_OWNER_SCOPE, no PASS. T38 queda como prueba focalizada de propagación de configuración, no tres campañas para elegir ganancias. Resultado negativo es aceptable si la ejecución es correcta.

### 2. Strategy y MM intercambiables

El núcleo consume contratos de datos, triggers, readiness, señales, decisiones MM, órdenes/fills y estados; NO interpreta internals de S2 ni fórmulas Gerard. La composición puede conocer módulos para registrarlos/injectarlos. Cambiar de módulo o parámetros sólo modifica módulo/configuración/composición, no driver, venue, reloj, accounting ni campaign.

Acoplamiento observado en la autoridad S01: ohlc_driver.go/requireNativeWarmup discrimina ModuleS2, decodifica s2.State y fija51H4/20M5. Llevar ese conocimiento al módulo/contrato compartido de requisitos/readiness. Preservar la semántica de S2 y su elegibilidad temporal; no quitar el guard para esconder falta de datos. Reutilizar interfaces existentes. Sólo extender una interfaz pequeña si falta una necesidad concreta.

MM entra por el contrato MoneyManager compartido de Operation. No crear GerardMMBacktest, switches por strategy_id en ejecución, reflect/serialización de estados privados para decidir, DSL, carga dinámica de plugins o framework de dependencias.

Probar sustitución independiente de Strategy y MM mediante los mismos seams del runtime, con módulos existentes o fixtures mínimos de prueba. No desarrollar otra estrategia comercial. Corridas independientes de estrategias distintas bastan; no agregar ahora portfolio simultáneo, combinador ni asignador de capital.

La ampliación de datos/capacidades genuinamente nuevos puede requerir un adapter/contrato nuevo; eso debe ser explícito y reusable, nunca duplicar decisiones ni prometer soporte silencioso para una capacidad ausente.

### 3. Paridad y causalidad

Mismos inputs normalizados, estado, configuración, calendario, orden causal y fills autoritativos deben producir iguales decisiones por los caminos runtime y backtester. Usar el harness existente por ambos adapters; no limitarse a invocar dos veces Evaluate.

OHLC1m sin ticks debe funcionar. S2 conserva señales5m/tendenciaH4 cerradas. Ticks completos aportan secuencia observada; fallback por minuto completo según manifest, sin dobles eventos/volumen ni QUOTE falsa. LIVE missing/stale nunca genera eventos de mercado sintéticos.

El modelo intrabar es del simulador, no una trayectoria histórica observada. Forming sólo expone el prefijo disponible; sin extremos futuros ni fills retrospectivos. Mantener protección, callbacks entre fills, reservas, q_exec_max y revalidación Provider. Versionar el cambio y conservar reproducción/identidad de V1 según su contrato.

Separar dos pruebas: equivalencia del dominio con los mismos fills inyectados, y corrección del venue con oráculos independientes de fills/precios/costes. La primera no demuestra por sí sola realismo del matching.

### 4. KISS y costo

Generador intrabar siempre lazy, buffers/rings acotados y resultados streaming. Primero medir referencia correcta. Si cabe en el presupuesto disponible, NO construir una optimización adicional sólo para satisfacer un nombre del diseño. Omitir pasos únicamente cuando sea necesario y la inercia/equivalencia esté demostrada; T35/T36 aplican a todo atajo implementado. Sin atajo, declararlo NOT_APPLICABLE con motivo, no afirmar que se probó.

Benchmark real pequeño antes de corridas extensas; medir tiempo, memoria, pasos y volumen de salida. Sin -race en el backtest largo. Corregir cuellos demostrados dentro del shot; no acumular timeouts a ciegas ni duplicar fórmulas MM para saltarse trabajo.

### 5. Dos modos, no dos engines

BASIC: saldo100000 continuo, sin lifecycle de prop, compras, retiros o reset por día/contrato. Procesar todas las oportunidades admitidas por Strategy/MM/seguridad. Distinguir señales, operaciones sin fills y trades ejecutados.

CAMPAIGN: mismo dominio; añade lifecycle secuencial y caja. Compra ON_DEMAND120; caja5000→4880. Perder2000 dentro de la cuenta NO cambia nuevamente caja. Payout sólo acredita al cobrar; no quinta cobranza. Mantener idempotencia, costos exactos, pendientes y residuales.

Usar el perfil funcional configurable propuesto en S02 para arrancar, bajo la delegación Owner de reglas consistentes: evaluación→funded, piso98000, pass3000/mínimo2 días con fills, payout bruto1500/split100%/fee0, settlement posterior y retiro de cuenta al cuarto cobro. Etiquetarlo FUNCTIONAL_ASSUMPTIONS; no investigar empresas ni atribuirlo a Earn2Trade. No cobrar extras escondidos. El Owner ajustará esos datos después.

F1 obligatorio: mercado, analítica, clock, fanout y Strategy OwnerState COMPLETO continúan durante pausa, rechazo, burn y reemplazo. Sólo cambia el compartimento de cuenta. Ningún rewarmup, ARMED administrativo, entrega retrospectiva o traslado de exposure/PnL/órdenes/MMState entre cuentas. Campaign no decodifica ModuleState.

Gaps/calendario/rollover preservan identidad y estado. No fabricar datos/fills ni sumar cuentas reseteadas como continuidad. Intentar el horizonte solicitado, reportando por separado cobertura verificable y segmentos rechazados. Un bloqueo de datos no es un burn económico ni desaparece por reiniciar dinero.

## /scope

Cambios de producto limitados a los componentes existentes necesarios para estos contratos, pruebas, perfiles y exports. Libertad técnica para resolver integración y errores ordinarios; no nueva arquitectura general. No trading, compras reales, deploy, D6 físico, PROD, ETCD, secretos ni ampliación de permisos. Refrescar D6 antes de shared changes y al cierre; preservar sus cambios.

Agents-OS: TODO sobre master. Cero ramas, PR, worktrees de ramas documentales o tags de respaldo nuevos. La policy del repo de producto Echo es distinta y se respeta por separado.

## /execute

1. Limpieza administrativa concreta solicitada por Owner, antes de trabajo documental nuevo:
   - Rama a retirar, exclusivamente en xKoRx/agents-os: codex/btg-s02-design-cloud-20261006. Último tip leído00514fe65d0b4a06975096de17a3c2246d573c92.
   - El Manager verificó diseño reparado en master920012e, rama antigua aún existente y ningún PR asociado a ese head. El feedback original main/80-agents/journal/feedback/system-1/2026-10-06-echo-futures-btg-s02-session-feedback.md NO apareció en master; recuperar desde00514fe antes de eliminar la rama.
   - Refrescar y comparar los cambios exclusivos de esa rama. Preservar en master cualquier evidencia documental única necesaria, incluido feedback original, sin sobrescribir el diseño reparado ni feedback posterior. La versión inicial queda como historia explícitamente supersedida cuando sea necesario; no otra autoridad activa.
   - Publicar sólo el delta documental en master con protección frente a cambios concurrentes y readback. Después eliminar la ref remota nombrada verificando que siga en el tip revisado; si avanzó, revisar ese delta antes. Cerrar sólo un PR que efectivamente pertenezca a ese head si apareció. No tocar PR/branches de Echo ni otras ramas ajenas.
   - Verificar ausencia de la ref. Limpiar la ref local únicamente si no contiene trabajo nuevo/no es un checkout activo; no borrar worktrees ajenos. Sin force global, reset duro, merge de toda la rama, cambios de ACL ni nuevos backups en branches/tags.
   - El Manager CLOUD no pudo ejecutar la eliminación: no expone ese write. No asumir que ya ocurrió. Si tu autorización técnica tampoco permite hacerlo, devolver estado preciso y continuar trabajo de producto independiente.
2. Registrar este delta Owner en el documento de control/diseño vigente: objetivo engine correctness, módulos intercambiables y ROI fuera de alcance. Un único change log; sin otra ronda de arquitectura. Guardar este mandato por el contrato prompt de Agents-OS si corresponde.
3. Implementar la mínima separación de composición y configuración compartida; sustituibilidad y continuidad antes de ensamblar campañas.
4. Completar fuentes/ejecución causal existentes, ambos modos y exports; ejecutar pruebas focalizadas y los primeros BASIC/CAMPAIGN reales. No devolver sólo READY_TO_RUN.
5. Medir y corregir; entregar candidato a revisión del Primary para S04. No ejecutar ni autoadjudicar el adversarial independiente que corresponde al siguiente shot.

Cada especialista tiene tarea y archivos de ownership claros, ONE-SHOT, pruebas y cierre. No despachar un ejército de reviews repetidos por cada microparche. El lead integra dependencias y resultados; no confundir actividad de agentes con capacidad entregada.

## /verify

Mantener la matriz S02 aplicable: T01–T29, T31–T34, T37; T35/T36 sólo para atajos implementados; T38 acotada a parametrización. T30/holdout/ranking no pertenecen al gate actual. Pruebas de sensibilidad de ejecución sirven para detectar dependencia del modelo, no para elegir el recorrido de mayor PnL.

Añadir dos comprobaciones pequeñas y decisivas:
- Sustituir Strategy sin cambiar código del motor, con requisitos/timeframes/readiness del módulo correctamente respetados; también sustituir MM independientemente. Comparar los caminos runtime/backtest, no duplicar una implementación de prueba dentro del engine.
- Cambiar parámetros declarados de los módulos conserva engine idéntico y cambia la configuración efectivamente consumida; no basta editar un JSON que nadie lee.

Probar causalidad, fills/costos, adds adversos/pyramiding, no-adds explícito común, continuidad tras reemplazo, caja5000→4880, no quinto payout, gaps/DST/rollover y reproducción. Verificar pathways críticos y policy de coverage del repo; no pruebas de relleno.

Usar escenarios controlados para demostrar lifecycle incluso si la estrategia real pierde o nunca retira. No alterar señales para producir un payout histórico. Histórico auténtico es obligatorio para el resultado real, y fixtures no lo sustituyen.

Resultado por modo: code/build/config/manifest, rango/contratos, fidelidad, señales/operaciones/fills, PnL/costes/DD, estado residual y tiempo/memoria. CAMPAIGN añade compras, burns, funded, retiros cobrados/pendientes y caja. Evidencia de prueba de paridad identifica su alcance; no LIVE_EQUIVALENT sin soporte.

## /reuse

Usar interfaces, adapters, parsers, materializers, harness y oráculos existentes. Conservar regresiones que atrapen fallos. Un CLI/config reutilizable; no UI ni diseñador visual. Ninguna abstracción sin necesidad concreta dentro de S03–S05.

## /improve

Capturar fricción real o NONE. No editar skills generales por una observación, no producir un documento por microfix ni modificar Strategy/MM para mejorar profit.

## /close

Persistir evidencia compacta en master de Agents-OS bajo main/10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTG-S03-IMPLEMENTATION.md, actualizando control por delta. Materializar notas nuevas y validar paths cambiados con los contratos vigentes; no reconstruir contratos/templates parciales ni ejecutar higiene global ajena.

Todo worker ONE-SHOT, incluido este lead: artefactos, agents-os-agent-run-register cuando corresponde, feedback y agents-os-session-close con handoff. Skills: main/80-agents/skills/agents-os-agent-run-register/SKILL.md; agents-os-session-feedback/SKILL.md; agents-os-session-close/SKILL.md. No afirmar pasos inaccesibles ni uso de modelo/cuota no expuesto. Primary Manager sigue abierto.

S03 devuelve CANDIDATE_READY_FOR_PRIMARY_REVIEW, no aceptación final. S04 LOCAL independiente crea/ejecuta E2E para falsificar; S05 corrige y completa ambos resultados, sin S06. Bugs ordinarios se reparan; sólo bloqueos reales o contradicciones Owner se elevan con evidencia.

Handoff máximo10líneas:
STATE / CODE_SHA / AGENTS_OS_SHA =
BASIC_REAL =
CAMPAIGN_REAL / CASH_RECONCILIATION =
STRATEGY_AND_MM_SUBSTITUTION =
RUNTIME_PARITY_SCOPE =
SCALING / HISTORICAL_COVERAGE =
REPRODUCIBILITY / PERFORMANCE =
AGENTS_OS_OLD_BRANCH_CLEANUP = DELETED_VERIFIED | BLOCKED_WITH_REASON
MATERIAL_FINDINGS / ARTIFACT =
NEXT = S04_LOCAL_INDEPENDENT_ADVERSARIAL

Empieza por el estado real y ejecuta. No devuelvas otra propuesta de estrategia ni un plan de optimización de rentabilidad.
