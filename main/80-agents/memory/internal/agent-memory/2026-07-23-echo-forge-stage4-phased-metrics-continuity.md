---
type: agent_memory
scope: project
created: 2026-07-23
updated: 2026-07-23
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge]]"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - project/echo-forge
---

# Echo Forge Stage 4 phased metrics continuity

La fuente única del cierre es `Echo Forge - Cierre de Etapa 4`, plan v0.9. SQX sigue siendo autoridad para métricas nativas y Go solo calcula validaciones derivadas/métricas custom rjara. Las Fases 0–6 tienen paquetes autónomos §8.1.1–§8.7, carga relativa 9–11, tareas atómicas, referencias exactas, `No tocar`, spikes permitidos, gates y bloques de despacho separados. Cada fase usa un agente/contexto nuevo, recibe solamente su bloque §15.1 y se detiene con su gate en review. No redistribuir responsabilidades entre fases.

## Continuidad 2026-07-23 — orientación de pendientes

- El owner puede despachar F0 a Minimax M3 usando el prompt maestro + bloque F0 de §15.1.
- El orden correcto es: F0 → G0 review → aceptación owner → F1, y repetir el mismo ciclo hasta F6/G6.
- No confundir “plan v0.9 corregido” con “G0 aceptado”: T0.1/T0.2/T0.4 están reabiertas por delta arquitectónica; falta validar el registro objetivo de cinco proyectos, la composición dinámica y el contrato standalone de TradeList.
- Confirmado: R:R = máxima ganancia / máxima pérdida neta en ventana móvil de 12 meses anclada en la última operación; mejor mes de todo el histórico vs peor año calendario completo; PnL después de comisión/swap.
- Confirmado: recovery de la racha negativa más larga con `recovery_months < streak_months` como `ACCEPTABLE` (ideal/`FAST`: un mes), `SLOW` si demora igual o más y `UNRECOVERED` si no recupera.
- Confirmado: comparador pluggable `risk_adjusted_delta.v1` (Ret/DD 25, PF 20, Sharpe 20, SQN 15, DD 15, Net Profit 5).
- Confirmado: `deep_warnings_shadow_v1` sin warning score, penalties ni efecto en selector. Regla de curva se habilita solo después de G0 y calibración del parameter set en shadow.
- Portfolio/período futuro no son preguntas de métricas: quedaron como restricciones técnicas de integridad/exportación originadas en el prompt inicial.

## Cierre 2026-07-23

- Plan v0.9 listo para revalidación: conserva 7 paquetes, 7 gates y 7 dispatches; `OD-A01/OD-A02` congelan cinco proyectos independientes y composición dinámica.
- Procedimiento reusable promovido a `80-agents/skills/agents-os-implementation-planning/`; este proyecto es su caso de referencia.
- Próximo agente: recibir prompt §15 + bloque F0 únicamente; detenerse con G0 en review. No reabrir M03/M05/M10 sin `PLAN_CONFLICT` respaldado por evidencia ejecutable.

## Gate G0 accepted 2026-07-23 22:50 CLT — pase arquitectónico v0.9

- **T0.1 inventario arquitectónico**: §1.6 del capability report v0.9 con whitelist efectiva (4 proyectos), clases Java (`src/SQ/CustomAnalysis/`), cadena runtime (`executor.ExecuteAndWait(projectName)`), contrato dinámico exacto y matriz TradeList por contexto. `EchoForgeAutomator` confirmado `dead runtime` (7 sitios con vestigios clasificados).
- **T0.2 SPECs alineadas**: las 3 SPECs (`FEAT-SQX-JAVA-EXPORTER-PLUGIN`, `FEAT-SQX-METRICS-CONTRACT`, `FEAT-SQX-STRATEGY-EVALUATION`) congelan el registro de 5 proyectos y el contrato dinámico `{project, source/input, output, stage/context}`.
- **T0.3 spike SQX real contra Zeus Build 142**: `javap` sobre `SQTradingLib.jar` + `SQDataLib.jar`. Confirmado `ResultsGroup.orders()` → `OrdersList`; `Order` (no `stockchart.Trade`) como tipo TradeList; `OrdersList.filter(field, direction, sampleType)` segrega FULL/IS/OOS; `SampleTypes` no incluye `FUTURE`; `OrdersList.identifier` da portfolio identity. 8 campos financieros promovidos de `unsupported/not_tested` a `supported` con firma SQX nativa.
- **T0.4 cierre G0 + handoff**: 7 `.cfx` firmados (4 EchoForge + `builder_test`/`retester_test`/`optimizer_test`) con smoke semántico (versión `142.2399`, símbolo `XAUUSD_darwinex` periodo `2016-01-04 → 2026-06-04`, fitness `NetProfit + ComputeFromStrategyResult`). G0 → `accepted`.
- **Artefactos firmados** (auditoría): `specs/FEAT-SQX-METRICS-CONTRACT/phase0/{SHA256SUMS.txt, G0_HANDOFF.md, PHASE-0-CAPABILITY-REPORT.md, spike_javap/, fixtures/cfx/}`.
- **Próximo agente F1**: contrato `signed_pnl` + reemplazo extractor heurístico Overview → nativo `Order`-based.
- **Próximo agente F2**: crear `EchoForgeTradeListExporter` (whitelist + `.cfx` + plugin class); renombrar 7 sitios con vestigios `EchoForgeAutomator*`; extender `core/runtime/config.go::ResolveLocalProjectNameByType` con `trade_list_exporter`.

## Validación owner 2026-07-23 22:55 CLT — auditoría G0

- El owner (vía Cursor) validó en dos pasadas los reportes del agente implementador de F0: T0.2 Contratos (CONFORME, 2 hallazgos menores) y pase arquitectónico v0.9 (CIERRE APROBADO).
- Los 11 SHA256 firmados (`phase0/SHA256SUMS.txt`) y el capability report (738 líneas, SHA `0a0e2cde…`) cotejados bit a bit contra `shasum -a 256`. Checklist G0: 13/14 ✅.
- `git status` confirmó cero cambios productivos: solo 3 SPECs modificados + `phase0/` y `PHASE-0-CAPABILITY-REPORT.md` no trackeados.
- El owner ejecutó el `sed` de aceptación: `G0_HANDOFF.md` y `PHASE-0-CAPABILITY-REPORT.md` pasaron `review → accepted`. F1 habilitada.
- Patrón reutilizable: para validar un reporte de cierre de gate, cotejar `git status`, `git diff --stat`, SHA256 de artefactos firmados, y grep puntual de cada claim del reporte contra los diffs. Aplica a futuras revisiones G1–G6.

## Corrección final 2026-07-23 — cinco piezas dinámicas

- El owner corrigió explícitamente la interpretación v0.8: `EchoForgeTradeListExporter` sí debe ser el quinto proyecto fijo independiente.
- Registro objetivo: `EchoForgeOverviewExporter`, `EchoForgeWFMExporter`, `EchoForgeTradeListExporter`, `EchoForgeMT5Exporter`, `EchoForgeRobustRunExporter`.
- La definición dinámica del flujo elige qué proyecto usar y cuándo; compartir `TradeExtractionService` no autoriza alojar TradeList en WFM/RobustRun ni crear mappings estáticos por tipo.
- `EchoForgeAutomator` continúa deprecado. El nombre histórico `EchoForgeAutomator.jar` puede aparecer como packaging, pero no implica responsabilidad runtime vigente.
- F0 se repite solo en delta: reutilizar baseline/métricas, reabrir contrato/registry/matriz de inputs y mantener G0 pending hasta evidencia.
