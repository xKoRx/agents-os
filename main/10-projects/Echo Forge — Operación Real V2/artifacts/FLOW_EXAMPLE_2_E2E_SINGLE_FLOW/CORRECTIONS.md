# CORRECTIONS — FLOW_EXAMPLE_2 E2E SINGLE FLOW (2026-10-16/17)

## 1. Corrección arquitectónica del Owner (entrada de esta ejecución)

El mandato original pedía dos FlowRuns (A producer + B consumer `selection_cohort`). La corrección del Owner revoca ese diseño: **UN `config.json`, UN `GenericSQXWorkflow` raíz, GROUP interno con `source.type=ranking_snapshot`**, prohibido invocar `resetBatchKeepBindings` como justificación de separación. Esta ejecución se realizó bajo la corrección.

## 2. Investigación del "defecto" resetBatchKeepBindings — NO EXISTE en la topología del Owner

Verificación en código (`generic_workflow.go`): el reset tras un group hermano deja `Keys=[]` con carriers vivos; `exactEarlyRankingArtifacts` exige `artifact.Key ∈ current.Keys` ⇒ un GROUP con source `ranking_snapshot` colocado DESPUÉS de otro group falla cerrado (eso fue el fallo wave-6 de la mañana, cuya spec tenía precision-group antes del GROUP con source). En la topología del Owner (builder→overview→selection→GROUP inmediato) **no hay reset previo**: `runSelectionTask` preserva el cohort completo (777/760 keys + artifacts + bindings) y añade solo el binding del SelectionSnapshot; el route sale de los ranking snapshots durables y matchea contra las keys exactas. **Cero cambios de código para el encadenamiento.** El flujo único se validó SPEC_VALID y corrió física end-to-end dos veces (w8 y w9), recorriendo GROUP→children por 6-7 particiones lógicas.

## 3. Defecto REAL #1 — alias canónico faltante del dataset dukascopy (FIXED)

- **Síntoma**: w8 falló no-retryable en `mt5_score_shadow_v1` (fidelidad) con `decode durable TradeSet: normalized trade scope mismatch: contract_conflict` después de MT5 30/30 COMPLETED.
- **Causa raíz**: `sqx/core/evaluation/canonical_scope.go` — tabla explícita de alias sin `usatechidxusd_dukascopy_utc02` (dataset del Owner `USATECHIDXUSD_dukascopy_UTC02`). Cada trade del TradeSet durable resolvía a símbolo canónico vacío → mismatch fail-closed contra el scope. El exporter cumplía el diseño (símbolo raw en trades); faltaba el alias.
- **Fix**: `b77af11` — alias exacto `"usatechidxusd_dukascopy_utc02": "ndx"` + filas de regresión (UTC02→ndx, UTC03→"" para preservar el boundary fail-closed). Tests: `TestCanonicalSymbol_ExistingCatalogAndAliases` + suites evaluation/MT5-score green.
- **Release**: 0.2.147 (`deploy_release.sh --release-only`), binario linux `0e4c9908fe428b65…`, manifest `69a6cd7`. Rollout: el verificador SSH-directo del script falla (`kor@host` sin llaves desde Daedalus — limitación conocida); verificación sustituta por SSH MCP: proceso `/opt/stager/releases/0.2.147/bin/symphony` + SHA byte-exacto 3/3 hosts.
- **Evidencia de eficacia**: reset Temporal del workflow w8 re-ejecutó el score con 0.2.147 → 30 scores mt5-score.v1 COMPUTED en el primer intento.

## 4. Hallazgo #2 — el reset Temporal no puede completar un FlowRun ya sellado FAILED (NO fix; contrato correcto)

Tras el fix, un reset al `WorkflowTaskFinishEventId` previo al fallo re-ejecutó TODO el tramo final (scores/ranking/promoción) pero `flow_run_seal` rechazó FAILED→COMPLETED (`invalid FlowRun transition`, `domain/control_plane.go` — FAILED es terminal por diseño). Decisión: NO debilitar el contrato ni editar el estado durable; el "continuar" del §7 se ejecutó como re-despacho del MISMO flujo único con identidad nueva (w9). Lección operacional: **un FlowRun sellado FAILED no llega nunca a COMPLETED vía reset; los reintentos post-fix requieren identidad nueva.**

## 5. Observación #3 — mágica solicitada vs autoridad durable

El spec pidió magic 888111; `runDurableApplySelectedRun` usa exclusivamente la asignación de Magic Number V1 (26100091054..26100091083). Comportamiento contractual existente (la TaskSpec magic confirma, nunca overridea; el mismatch gestionado por la autoridad no bloqueó el apply 30/30). Registrado para transparencia; sin cambio.

## 6. Errores transitorios del operador y de la sesión

- `pgrep -f` vía wrapper SSH MCP se auto-machea (la línea de comando del wrapper contiene el patrón) → varios "EXPORTER_ALIVE" falsos positivos entre 23:44-00:28Z; corregido con `ps aux | grep "patrón [-]x"`.
- Lecturas de CPU por `%CPU` de `ps` (promedio de vida) indujeron al error "392% CPU" durante la fase single-thread del export; corregido con `top -H` + delta de `TIME`. La consulta del owner ("1.8%, 1 core, 44 min") era correcta: la exportación del overview es single-thread por diseño.
- Sesiones MCP (aranea-ssh, aranea-mongo) expiraron repetidamente; recovery certificado vía `initialize` HTTP + driver curl con `Mcp-Session-Id` (helpers `sshrpc.sh`/`mongorpc.sh` con auto-reinit).
- El export del overview de 745-847 estrategias × ~20k trades tarda 25-60 min single-thread según host/densidad (Zeus 25 min con 760; Hera 59 min con 847). Costo documentado para planificación futura.

## 7. Lección del intento anterior (mandato §10.5)

La cancelación de Run B por tiempo (T+40, 2026-10-16 21:52Z) **fue incorrecta**: el workflow estaba sano (optimizer 18/30 avanzando a ritmo normal para 30 optimizadores genéticos WF) y la cadena completa jamás cupo en 40 min. Esta sesión lo confirma empíricamente: el mismo funnel completo tardó 2h09m30s (w9). Registrado como feedback en Agents-OS.
