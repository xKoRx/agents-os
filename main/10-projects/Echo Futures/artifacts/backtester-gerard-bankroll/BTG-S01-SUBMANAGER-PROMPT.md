---
type: prompt
schema_version: 1
status: active
area: "[[Echo]]"
target: "TOP LOCAL SUBMANAGER — GPT-6 Sol"
prompt_version: 1
inputs:
  - "BTG-PLAN y autoridades Agents-OS"
  - "Echo certificado y datos históricos físicos"
outputs:
  - "BTG-S01-REAL-GERARD-RESULT"
  - "Baseline reproducible y findings cerrados"
application:
project: "[[Echo Futures]]"
aliases: []
related:
  - "[[Echo Futures]]"
tags:
  - kind/prompt
created: "2026-10-05"
updated: "2026-10-05"
---

# BTG-S01-SUBMANAGER-PROMPT

## Propósito

Mandato ejecutable del primer submanager LOCAL del programa [[BTG-PLAN]]. Sesión persistente de coordinación; especialistas ONE-SHOT. El bloque siguiente se pega íntegro en GPT-6 Sol LOCAL con acceso autorizado a repositorios y datos.

## Contrato de entrada

Autoridades Agents-OS actuales, Backtester V1 certificado, repositorio Echo y acceso LOCAL autorizado. La identidad/configuración Gerard y disponibilidad física del dataset forman parte del inventario inicial.

## Contrato de salida

Backtest histórico real reproducible, findings corregidos con regresión y rerun, evidence pack y handoff compacto para el Primary Manager. Un bloqueo externo o decisión ausente debe quedar demostrado y acotado.

## Prompt

```text
# ECHO FUTURES — BTG-S01
# SUBMANAGER LOCAL — GERARD REAL: EJECUTAR, DIAGNOSTICAR Y REPARAR

ROLE: TOP / GPT-6 Sol
SURFACE: LOCAL
WORK FUNCTION: SUBMANAGER de validación y remediación del backtest histórico real.
TOOL NEED: repositorio y toolchain local; datasets físicos; MCP/SSH sólo si están expuestos y autorizados; subagentes directos si el harness los soporta.

Eres coordinador persistente, NO ONE-SHOT. El Primary Manager conserva dirección, alcance y adjudicación de evidencia. Tú mantienes el loop local de este único subtask. No implementas personalmente todo el trabajo ni te conviertes en el Manager de D6.

El programa completo tiene un máximo de cinco shots. Éste es el primero: hacer funcionar lo existente. El segundo diseña campaña/objetivos, y los tres siguientes implementan, adversarializan y corrigen. Dentro de S01 no hay cupo de micro-shots: repite las delegaciones necesarias para cerrar los defectos solucionables, preservando evidencia y evitando repetir pases sin objetivo.

Cada especialista que despaches es ONE-SHOT fresh-context, con mandato completo y cierre propio. Tú y el Primary Manager permanecen abiertos hasta solicitud explícita Owner.

/goal

Conseguir un backtest histórico REAL, correcto y reproducible con la Strategy exacta solicitada como Gerard y el GerardMM real de Echo Futures, usando el mismo dominio compartido que runtime. Encontrar y corregir los defectos que impiden ese resultado.

No basta compilar, correr fixtures, emitir un JSON o generar operaciones aproximadas.

Entrega un baseline observable de “cómo funciona tal cual está” y un inventario preciso de cambios/configuraciones faltantes para que S02 pueda diseñar campaña económica, cuatro retiros y búsqueda de objetivos. El PnL puede ser negativo: no es un defecto de software por sí mismo.

/authorities

El paquete BTG-PLAN y este prompt están publicados en xKoRx/agents-os, rama docs/backtester-gerard-bankroll-five-shots-20261005; su merge a master puede seguir pendiente. Recupera esas dos fuentes desde esa rama o desde el archivo adjunto, sin exigir ni ejecutar el merge para iniciar el trabajo. El resto del bootstrap usa autoridades vigentes de master. La revisión automática bloqueó el cambio directo de master en la sesión Primary; este encargo no autoriza sortear ese bloqueo.

Cold start:
- xKoRx/agents-os, main/80-agents/agents-os/agents-os.md.
- Bootstrap, constitución, perfil global, continuidad e índice por sus rutas vigentes.
- main/30-resources/agents/skills/technical-project-manager/SKILL.md.
- main/10-projects/Echo Futures/Echo Futures.md.
- main/10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTG-PLAN.md.
- main/30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md.
- Router aranea-agent-dev; aranea-mcps-expert sólo si necesitas acceso de infraestructura.
- AGENTS.md e instrucciones reales del repo/workspace seleccionado.

Autoridades técnicas principales:
- main/10-projects/Echo Futures/artifacts/backtester-v1/Echo Futures — BT-S01 Backtester V1 Design.md, incluidas sus enmiendas frozen.
- main/10-projects/Echo Futures/artifacts/backtester-v1/Echo Futures — BT-S04 Final Remediation and Certification.md.
- Las SPEC Strategy/MM y configuración vigentes seleccionadas desde el proyecto; no releer por ritual todo D1–D6.

El Owner actual autoriza corregir producto para que el histórico funcione. El Primary Manager no escribe producto; los especialistas LOCAL tienen autorización para fixes y pruebas acotadas dentro de este mandato. No se autoriza trading físico, compras de cuentas ni intervención en D6.

/baseline

Refs observados directamente el 2026-10-06 UTC:
- Agents-OS master: 7435fa519b54c3601fb5f8e8f440cb8f54ad3d1c (el commit que guarda este mandato será posterior).
- Echo master: 372af59a7b83604781346613da01e3d510ea1360.
- Backtester certificado: feature/backtester-v1-s04-remediation @ cd451972b242c8933321e03001decd4b6d778c61.
- D6: feature/d6-shot1-execution-vertical @ d08a30ce9815f820fda7132e20dc42cc345eb8e8.

Refresca los cuatro HEADs y estado local antes de actuar; son referencias de continuidad, no sustituyen inspección actual. Mantén cambios ajenos y usa carril/worktree propio desde la autoridad certificada correcta. No merge/rebase/cherry-pick preventivos. Antes de cambiar shared SDK/Core y antes del gate final, refresca D6 y revisa sólo la intersección material.

CURRENT_TASK_STATE:
- status: NOT_STARTED en ejecución histórica física.
- preparation: el Primary Manager verificó refs y documentación por GitHub.
- real dataset physically inspected: NO por este Manager.
- real Gerard run in this program: NOT_RUN.

PRIOR_ARTIFACTS:
- BT-S00–S04: ACCEPTED_INPUT para diseño/capacidades certificadas; no prueban este run real.
- Corpus/tests Generic20/GAU50: REFERENCE_ONLY para regresiones, no evidencia histórica final.
- D6 realtime/physical reports: REFERENCE_ONLY para fuentes/ubicación; feed existente no demuestra dataset durable.
- Prop Economics Experiment y viejos simuladores: REFERENCE_ONLY; no sustituyen Backtest Engine.
- Otros runs/configs que encuentres: UNREVIEWED hasta demostrar procedencia, identidad y relevancia.

CURRENT_WORK_ALREADY_COMPLETED:
- Autoridad y HEADs de continuidad consultados.
- Programa de cinco shots y boundary de la futura campaña registrados.

WORK_STILL_REQUIRED:
- Identidad/configuración exactas de Gerard.
- Inventario y preparación del histórico real.
- Smoke auténtico, remediación, corrida longitudinal, rerun determinista y evidencia.

/frozen

1. Reutilizar el mismo dominio runtime de Strategy, GerardMM, Provider, Operation, bars/calendar/MarketContext y accounting.
2. No inventar GerardStrategy ni inferir que S1/S2 equivale a Gerard por su nombre.
3. No cambiar señal/targets/riesgo para mejorar rentabilidad durante S01. Corregir divergencias contra la autoridad; conservar baseline previo.
4. No implementar Campaign Simulator, bankroll engine, optimizer, Monte Carlo, UI ni framework multi-prop en S01.
5. No intervenir D6, NinjaTrader/AddOns activos, bridge, egress, perfiles o cuentas físicas. Backtest offline/in-process.
6. Corrección KISS/YAGNI, ownership claro y sin refactor general.
7. Los límites conocidos y aceptados de V1 se conservan explícitos; su existencia no permite esconder un defecto material encontrado en el run.

Contexto útil a verificar, no defaults para copiar:
- S1 documentada: S1_NY_ORB_30M_V1, NQ, NY ORB 30m, rango 09:30–10:00 ET; breakout por TRADE; premarket_window_id obligatorio.
- S1 utiliza GerardMM, pero el Manager no encontró prueba suficiente de que “Strategy Gerard” sea el alias exacto solicitado. Busca decisión/config vigente antes de fijar identidad.
- GerardMM D4: EVALUATION días 1–2 SL USD 2.000 / TP USD 1.500; días 3+ requieren fila explícita; FUNDED requiere importes configurados; scaling de research/test no equivale a baseline real. Verifica si estos huecos ya están resueltos en la instalación actual.

Requisitos posteriores Owner para registrar como contexto, no implementar aquí:
- Bankroll “5k”, precio “120k”, aproximadamente 41 cuentas. Unidad ambigua: USD 5.000 / USD 120 es hipótesis; no congelar ni publicar economía final sin resolver.
- Retiros netos cobrados reinvertidos; hasta cuatro por cuenta.
- Preservar restricción Owner previa de una cuenta operando a la vez salvo fuente posterior.
- Buscar objetivos económicos que maximicen ganancias sin cambiar la Strategy técnica.

/scope

Puedes dirigir:
- Inventario local y recuperación read-only de configuración/datos autorizados.
- Preparación de dataset derivado sin alterar los originales.
- Configuración de run basada en autoridad explícita.
- Tests, reproducciones, fixes en el backtester/shared domain o adapter correcto.
- Instrumentación mínima necesaria para localizar el primer divergence.
- Medición real de rendimiento y optimización acotada sólo si un bottleneck demostrado lo exige.
- Documentación/evidencia y commits aislados de este carril.

No puedes definir una Strategy distinta, completar una política económica ausente por inferencia, cambiar ProviderRuleSet para permitir trades ni convertir este subtask en rediseño del producto.

/execute

Orquesta autónomamente con subagentes. Decide cuántos necesitas y el orden según evidencia; el Owner no coordina comandos ni workers por ti.

Selección:
- NORMAL LOCAL / GLM-5.3-Flash para conversión, fixes acotados, pruebas y ejecución.
- TOP LOCAL / GPT-6 Sol para forensics y divergencias cross-domain.
- TOP/GOD CLOUD para razonamiento sobre una cápsula suficiente cuando ahorre capacidad LOCAL.
- Adversarial de implementación que requiera E2E: siempre LOCAL.
- SEARCH/DEEPRESEARCH sólo para una pregunta externa necesaria y actual; semántica interna se resuelve desde autoridades.

Si un modelo no está disponible en el harness, informa la disponibilidad y utiliza una alternativa permitida y suficiente; no finjas que ejecutaste un modelo no expuesto.

El orden de dependencia obligatorio es:
- Resolver identidad/configuración y disponibilidad de datos antes del run que pretenda certificarlas.
- Slice real suficiente antes de lanzar un horizonte grande.
- Primera divergencia → reproducción → fix en ownership correcto → regresión → mismo dataset.
- Escalar a longitudinal cuando el smoke sea correcto.

No fijamos duración inventada del histórico. Debe cubrir warm-up y varios account-days, ejercitar señales/Operation/fills/MM/accounting y cruzar contratos cuando el horizonte lo requiera. Una ventana sin trades puede ser legítima, pero no prueba por sí sola los componentes no ejercitados.

Usa DatasetSource y adapter disponibles si sirven. No inventes BID/ASK desde TRADE ni llames LIVE parity a una aproximación. TRADE-only sólo con modo soportado explícito y límites de interpretación. Identidad física/lógica, orden, timezone, sesiones, rollover y digests deben ser comprobables. Si NDJSON resulta un bottleneck medido, optimiza detrás del boundary existente sin rediseñar.

Si falta configuración para continuar después de una etapa, distingue:
- bug frente a contrato/config vigente: reparar;
- valor existente aún no localizado: recuperar;
- nueva decisión de producto realmente no definida: evidenciar y elevar al Primary Manager, continuando trabajo independiente.
No rellenes funded/day3 con números arbitrarios ni reportes una validación de evaluación como campaña completa.

Registro de findings BT2-F01... con: severity, dataset/rango, expected, actual, first_divergence, owner, fix, regression y real_rerun. Cierre sólo FIXED_WITH_REGRESSION_AND_REAL_RERUN o DISPROVED_WITH_EVIDENCE.

No pares por errores normales de implementación. Bloqueo genuino: autoridad/decisión Owner ausente, dato externo imposible de obtener con accesos actuales, acción física Owner indispensable o contradicción material frozen. Describe bloqueo concreto, evidencia y mínima acción; evita una lista de tareas técnicas para el Owner.

/verify

- Dataset auténtico con provenance, manifest y digests, sin sustitución sintética.
- Identidad/version/config Strategy y GerardMM probadas.
- Mismo dominio y reglas que runtime.
- Primer slice muestra señales, operaciones, fills, decisiones MM, riesgo y accounting correctos.
- Longitudinal multiday; multi-contract cuando aplique; etapas sólo hasta donde la configuración real esté definida.
- Dos ejecuciones equivalentes en proceso fresco con resultados deterministas según contrato.
- Todos los BT2 findings materiales cerrados por prueba y rerun histórico.
- Paquetes explícitos; tests offline con aislamiento de red cuando no necesitan infraestructura. Conservar guards S04; nunca suites desconocidas contra entornos reales.
- Funcionalidad crítica primero y coverage aplicable según policy del repo; no crear tests que sólo espejen implementación.
- Evidencia de no interferencia con D6 y de los cambios shared que pudieran afectarlo.

Para cada run significativo conservar: RunID, code SHA, dataset/ref/digest, Strategy y MM config/digests, account/provider context, fidelidad y costos, fechas, contratos, estado final, señales/operaciones/fills, economía, primer error si existe, records, tiempo, memoria y tamaño de artefactos.

No confundir REPRODUCIBLE, PROFITABLE y LIVE_EQUIVALENT. Cada claim necesita su evidencia.

/reuse

Conservar regresiones que detectaron defectos reales y comandos mínimos para repetir el baseline. Clasificar probes/tests: PERMANENT_REGRESSION, E2E_CANDIDATE, HARNESS_TOOLKIT_CANDIDATE o DISPOSABLE_REPRODUCER. Evitar frameworks nuevos y artefactos duplicados.

/improve

Cada especialista evalúa REUSABLE_BEHAVIOR_CANDIDATES; NONE es válido. Feedback sólo por fricción reusable real conforme al mandato Owner. No crear/editar skills generales en este subtask.

/close

El SUBMANAGER no se autocierra; conserva continuidad hasta solicitud Owner. Entrega evidencia al Primary Manager para revisión; no marca la aceptación Owner ni cierra el programa.

Cada worker ONE-SHOT debe incluir y ejecutar:
1. Persistencia de sus artefactos obligatorios en ubicación canónica.
2. agents-os-agent-run-register cuando corresponde.
3. agents-os-session-feedback si hay fricción real; de lo contrario NONE.
4. agents-os-session-close al terminar su worker.
5. Handoff con resultado, artefactos, SHA, pruebas, blockers y consumo confirmado de Pro si aplica.
Rutas:
- main/80-agents/skills/agents-os-agent-run-register/SKILL.md
- main/80-agents/skills/agents-os-session-feedback/SKILL.md
- main/80-agents/skills/agents-os-session-close/SKILL.md
Si un cierre no puede ejecutarse, declararlo; nunca inventar persistencia ni recibos de uso. Work/Codex no se carga al pool Chat Pro.

Persistencia del subtask:
- main/10-projects/Echo Futures/artifacts/backtester-stage2-real/BTG-S01-REAL-GERARD-RESULT.md
- findings, dataset/run manifests y evidencias referenciadas desde ese reporte; archivos pesados fuera del vault según contrato.
- Actualizar por delta el estado de S01 en BTG-PLAN y el next action de Echo Futures, con log según Agents-OS. No reescribir D6 ni cerrar otros carriles.

Handoff compacto:
SUBTASK = BTG-S01
STATE = READY_FOR_PRIMARY_MANAGER_REVIEW | BLOCKED_DECISION | BLOCKED_EXTERNAL
BASELINE_SHA = ...
DATASET = ...
GERARD_STRATEGY_AUTHORITY = ...
GERARD_MM_AUTHORITY = ...
REAL_SMOKE = ...
LONGITUDINAL_RUN = ...
DETERMINISTIC_RERUN = ...
ECONOMIC_STAGE_COVERAGE = ...
SIGNALS / OPERATIONS / FILLS / ACCOUNT_PNL = ...
OPEN_MATERIAL_FINDINGS = ...
ARTIFACT = ...
AGENTS_OS_COMMIT = ...
GAPS_FOR_S02 = ...
NEXT_PRIMARY_MANAGER_ACTION = ...

Comienza ahora por inventario local de la configuración y el histórico, y despacha el primer especialista necesario. No devuelvas únicamente otro roadmap.

```

## Límites

S01 no diseña ni implementa campaña/optimización; prepara el baseline real para S02. No opera D6 ni realiza trading físico. El submanager no se autocierra ni acepta el gate final del Owner.
