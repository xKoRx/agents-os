---
type: feedback
scope: session
created: "2026-07-22"
updated: "2026-07-22T20:10Z"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
application: "[[StrategyQuant X]]"
entities:
  - "[[Symphony]]"
  - "[[StrategyQuant X]]"
related: []
aliases: []
confidence: medium
source_session: "0bd267d6-a6bb-43ff-af9e-32d1472b91e9"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
  - app/strategyquant-x
---
# Session Feedback - 2026-07-22 - Symphony Kronos fixes

> [!warning]+ Addendum 2026-07-22 ~20:10
> El usuario reportó "volvió a fallar" tras los fixes y, tras nueva ronda
> de investigación, **rebotó la Causa #1** ("Existing portfolio ausente").
> El usuario decidió cancelar antes de hipotetizar una causa raíz para la
> diferencia. Por lo tanto este feedback refleja el ciclo completo.

## Qué complicó más la sesión y cómo se mejoraría

- **Confundir un efecto con la causa raíz**: el databank `Existing portfolio`
  en disco era un síntoma **observable** pero no causal. La diferencia real
  Hera vs Kronos (workspace state) es invisible a ssh directo y solo
  aparece al comparar temporalmente logs de ambos workers. Una validación
  más profunda con la doble comparación `retester_test.cfx` MinIO vs
  workers (mismo SHA) desde el minuto 0 habría revelado que el problema
  no era el CFX.
- **No probar el fix end-to-end**: los fixes al JAR + cache son técnicamente
  válidos pero quedaron sin un wf fresco de prueba. Mejor: tras el fix,
  disparar el mismo wf `sqx-main-00_configs-v1-NDX-H1-L-1784762810` para
  validar que el comportamiento del worker coincide.
- **El CFX `databank="null"` en `CustomAnalysis-Task1.xml:38`** es un bug
  upstream real pero **no es la causa del fallo en Kronos** porque Hera
  usa el mismo XML y arranca. Confundir esto con "el problema" habría
  generado un PR innecesario.

- **Iteración masiva de scripts de extracción** sobre el wf Temporal. Tuve
  que escribir `scratch/extract_payloads.go` y `scratch/extract_raw_logs.go`
  antes de poder siquiera comparar logs lado a lado. La extracción de
  `sqx_raw_log` desde eventos de Temporal debería ser un script
  reutilizable en `30-resources/tools/symphony/` o como sub-comando
  de `.agents/skills/echo-forge-testing`.
- Descubrir la "no-caché" del JAR requirió verificar manualmente el SHA256
  del byte-code entre el JAR y la carpeta `internal/tmp/compiled/`. Una
  verificación de este tipo debería estar documentada en
  `80-agents/learning/symphony/` y consultada vía `agents-os-context-retrieval`
  en futuras investigaciones similares.

## Qué parte de Sistema 1 fue más útil

- **agents-os-bootstrap** y los skills `symphony-worker-ssh` /
  `symphony-worker-troubleshooting`. Iterar sobre los 3 workers vía SSH
  con disciplina (sin tocar Zeus o Hera) hizo la investigación fluida.
- **graphify-personal** orientó rápido al ecosistema de la skill y al
  agente a cargo (`artesano` para fixes, `auditor-critico` para revisar).

## Qué parte fue menos útil, redundante o ruidosa

- El cache de grep en `internal/tmp/compiled/` creó una falsa idea de
  "compilación" cuando en realidad es una **copia del classpath**. La
  nota L3 que se creó deja esto explícito para no perder tiempo en
  sesiones similares.

## Qué problema apareció que Sistema 1 no resuelve pero podría ayudar a resolver

- **Falta de un tooling de validación post-deploy de worker**: un skill
  `symphony-worker-bootstrap` (o `worker-bootstrap-validator`) que dado un
  host, verifique:
  - Permisos del JAR `EchoForgeAutomator.jar` (`0664`)
  - Existencia y contenido de `internal/tmp/compiled/SQ/CustomAnalysis/`
  - SHA256 del `EchoForgeOverviewExporter.class`
  - Presencia de databanks sueltos esperados (`Existing portfolio`, ...)
- **Falta de un test de regresión** para los `builder_test.cfx` versionados:
  alguien versionó un CFX en MinIO que tiene un mismatch config.xml ↔
  Build-Task1.xml. Un linter del CFX al hacer push evitaría futuras
  regresiones.

## Qué feedback deja sobre retrieval, skills y templates

- El retrieval ayudó a encontrar rápidamente notas relacionadas
  (`sqcli-databanks-not-found.md`, `sqcli-project-does-not-exist.md`),
  confirmando que la sesión anterior documentó bien el fenómeno de
  CFX mal formado. Sin embargo, **ninguna nota existente mencionaba
  el fenómeno `Existing portfolio` específico** ni el doble factor
  "permisos + cache compilado" — y por eso lo creé como dos L3 nuevos
  con nombres específicos.

## Qué dolor parece repetible y debería evaluarse para promoción a L3

- **Recurrencia esperada**: cada nuevo worker que se suma al cluster va
  a tropezar con esta misma doble falla (permisos + cache) hasta que
  haya un bootstrap automático. Ambos L3 ya están en
  `80-agents/memory/public/known-error/symphony/`. El siguiente paso
  debería ser:
  1. Promover la "mitigación recomendada" a `30-resources/runbooks/symphony/symphony-worker-bootstrap.md`.
  2. Crear el skill `80-agents/skills/symphony-worker-bootstrap/SKILL.md`
     que ejecute los comandos en lote y reporte el estado.
