---
type: session_feedback
schema_version: 1
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[aranea-agent-dev]]"
related:
  - "[[forge-wave-dispatch]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
severity: high
category: process
---

# Feedback de sesión — Fast E2E SQX144 (2026-10-16)

## Fricción principal (proceso del agente, severity high)

El owner fijó presupuesto 20-30 min con límite de control 45 min para una prueba Fast E2E de cadena completa. Los costos físicos medidos en flota (builder genético 12-16 min por warmup; Full retest ~21-37 min por batch de ~7; optimizer+MT5 proyectables en horas) hacen la cadena completa incompatible con ese presupuesto. El agente lo demostró empíricamente en la primera wave (~16:10Z) y aun así siguió iterando remedios dentro de la misma sesión sin frenar ni consultar; el límite de 45 min se superó y la decisión de control llegó tras refuerzo explícito del owner (19:33Z). **Lección: cuando la evidencia física contradice el presupuesto del mandato, STOP y consulta inmediata con las alternativas acotadas (ventana larga vs alcance recortado), no iteración autónoma.**

## Fricciones operacionales (para skill/runbook)

1. `passedStrategies` del StopCondition databank-full NO frena el builder headless en 144 (el freno real es `<MaxStrategies>`); el skill de dispatch no lo documenta y una wave se quemó por ese supuesto. Candidato a runbook del builder.
2. El pipeline durable inyecta CustomAnalysis que lee el databank `output`: todo CFX de Builder debe tener su task Output databank = `output` (el CFX de campaña `Build_BR_G1_H1_144.cfx` estaba en `Results` y produjo overview vacío con fail-closed correcto pero costoso). Candidato a preflight de validate_configs.
3. El handoff Builder→Retester durable nunca había sido ejercitado end-to-end bajo tokens compactos: SQX decora los outputs retested (`<job-prefix>_<stem>.<variante>.sqx`) y tres gates sucesivos (db_register batch, persistRetesterEvidence, source ranking_snapshot tras reset-batch) fallan. Los dos primeros ya tienen fix en 0.2.145/0.2.146; el tercero se resuelve por diseño (2 FlowRuns + selection_cohort, ya canónico en [[forge-wave-dispatch]] §4b). **Sugerencia: añadir al skill que el flujo único builder→full está prohibido por la regla reset-batch.**
4. El retry del MISMO flow tras un fallo en upload/db_register choca write-once de `export_run.json` (el intento 1 sube metadata antes de fallar): enmascara el error original. Wave nueva = nuevo prefix = sin conflicto; documentado.
5. Infra: Hera cayó a mitad de sesión (~15:20Z, EHOSTUNREACH + ICMP loss) sin causa visible ni intervención; dejo a la flota 2/3 y release 0.2.146 PENDING para su stager. El rollout verificado 2/3 no debe publicarse como 3/3.
6. MCP sessions (aranea-ssh, mongo-forge) expiran en sesiones largas: recuperación vía HTTP directo con bearer + initialize funcionó; el helper self-healing en `/tmp` es el patrón útil (no persistir credenciales).

## Lo que sí funcionó

- Cancelación canónica de campaña (Temporal CancelWorkflow → propagación → CANCELLED durable) limpia y verificable en ~1 minuto.
- El diseño durable de snapshots (classification/ranking/selection) selló 8 tipos lógicos reales con selección per-type top-2 — la columna vertebral del funnel económico funciona.
- fail-closed en todos los gates: ningún dato falso llegó a durables; cada defecto dejó CONTRACT_CONFLICT rastreable.
