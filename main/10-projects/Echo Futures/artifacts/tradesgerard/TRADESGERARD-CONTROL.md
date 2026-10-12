---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-CONTROL

## Propósito

Fuente única de estado de la preparación TradesGerard, etapa A del mandato GOD LOCAL del Owner, recibido el 2026-10-12. Estado técnico inicial: IN_PROGRESS; no READY_FOR_GLM, aceptación final Owner pendiente. Etapa B corresponde a GLM-5.3-Flash y no se lanza automáticamente.

## Contenido

### Autoridad y límites

El mandato vigente autoriza diseño técnico ordinario, desarrollo offline por TOPs, verificación independiente y corrección. El manager coordina y documenta; no escribe ni integra código, scripts, indicadores ni tests. Sin merges productivos, deploy, servicios, egress trading, compras/resets reales ni reconstrucción de cuentas personales. La aceptación final pertenece al Owner. BTG-PLAN, BTX-PERF y D1–D6 conservan sus gates históricos.

Inputs inmutables: caja inicial USD 5.000; compra individual USD 120 a demanda; reinversión sólo de efectivo acreditado; una cuenta operando y un ciclo agregado; turno persistente hasta target/límite/fallo/bloqueo/sesión; target ordinario evaluación USD 870 netos; pausa interna −USD 1.000 sin reset; NY flat/cancelado al cierre; funded sin heredar 870 ni consistencia de evaluación. Retiros brutos candidatos 2.250/2.300/2.500/3.000.

### Trabajo y evidencia vigente

| Entrega | Estado | Responsable / siguiente acción |
|---|---|---|
| Inventario real y diseño acotado por propietarios | REVIEWED_FOR_IMPLEMENTATION | TOP inventory completo; mapa y decisiones en [[TRADESGERARD-CONTRACT]]. |
| Perfil GAU50 versionado con fuentes oficiales | RESEARCH_COMPLETE_SCENARIO_REQUIRED | [[TRADESGERARD-PROP-PROFILE]] distingue hechos, supuestos y UNKNOWN; no certificación comercial. |
| Catálogo finito con todos los IDs | DESIGN_VERIFIED_FOR_IMPLEMENTATION | design-2 preserva53 IDs; auditoría+corrección con59 checks PASS. Ver [[TRADESGERARD-CONTRACT]]; ninguna variante ejecutada. |
| Motor/composición/campaña/lote compacto | CANDIDATE_FOR_AUDIT | Fuente limpia congelada06ab6b12; no autorización de readiness. Integrador termina sólo recibo externo. |
| Verificación independiente del delta exacto | RUNNING | TOP verifier_a tiene el único carril de pruebas/build/campañas sobre el freeze exacto. |
| Cobertura nueva mínima95% | GAP_OPEN | Recibo del candidato1081/1425=75,86%; TOP coverage_prepare prepara tests externos sin medir ni modificar producto. |
| Manual actualizado, evidencia A y prompt GLM | IN_PROGRESS | [[TRADESGERARD-EVIDENCE-A]] y prompt preparados; manual/recetas/identidades finales pendientes, sin inventar flags ni rutas. |

Harness local: TOP inventory/prop_profile/catalog/contract_audit/catalog_repair completos; integrator_a implementa y verifier_a prepara casos en ámbito disjunto sin medir fuente mutable. Todos fresh-context ONE-SHOT, modelo solicitado `gpt-6.1-sol`; modelo servido UNKNOWN. No se asume GLM disponible en el mismo harness. No se consume CLOUD Pro.

Baseline de source inspeccionado por TOP inventory: repo `xKoRx/echo`, checkout relativo a workspace Aranea `work/btx-perf-last-20261010/integrator/echo`, rama `codex/btx-perf-last`, HEAD `873f5f1c7df25086271af1de1896095f1cade2a9`, limpio; origin apunta a clon local. Es identidad source, no build nuevo ni certificación actual. Inventario completo recibido; ningún componente no inspeccionado se considera ausente.

### Recursos y gates

Progreso del autor, todavía sin freeze ni auditoría independiente del producto: pruebas de registro preservado/relojes pausados y regresión ReplaceAccount PASS; perfil cuatro PAY/2250 inclusivo/ladder/DST+feriados PASS; Live intraday floor/withdrawal/equality/latch PASS. Ruta causal integrada de dos sesiones sintéticas COMPLETE con una compra120 y caja4880, una cuenta50000, HORIZON_CENSORED; cancelación FAILED/PLATFORM_CANCELLED conserva caja y drena Finish. Sellado/mutación de reglas por fase PASS. Prueba pública con nueva Strategy/MM determinista: entrada1/add1/salida física2, ledger flat, cancelación real de protecciones y BE200/TP250→500; corregido churn de cancelación del exit propio del fixture. Proyección del ciclo usa gross/costos del ledger autoritativo. Paridad detallado/compacto y batch resume/retry/tamper reportados PASS. Pase→funded→crédito sintético público PASS en el milestone descrito abajo. Estos resultados son reports del implementador y no acreditan READY_FOR_GLM ni rentabilidad.

Preflight disco del workspace: filesystem 146G, usado 127G, disponible aproximadamente 12G (2026-10-12). Antes de ejecutar: reservar al menos 8 GiB libres, un escritor de producto y una campaña a la vez; TOP debe fijar límites medibles de temporales, outputs y logs según preflight de su ruta real. No limpieza de corpus/caches/releases/trabajo ajeno. Sin barrido de investigación completo en A.

El gate READY_FOR_GLM exige demostrar cada fila de §10 del mandato, no sólo interfaces o pruebas unitarias del autor. Fixtures deterministas deben etiquetarse; smoke real sólo con corpus válido y ventanas explícitas. Cobros pendientes no son caja, datos truncados no son checkpoints, hashes no reemplazan replay detallado. El coverage nuevo mínimo es 95% sin cambiar denominadores heredados.

### Siguiente acción

Hallazgo de implementación en ruta sintética de22sesiones: el run llegó COMPLETE/reconciled pero el objetivo de aceptación falló (sin cobro acreditado; caja4760/dos compras). Primera causa identificada: applyContextTransition actualiza binding del Provider y deja liveConfig.Accounts con faseEVALUATION al transitar aLIVESIM; MM/admission leen fase desactualizada. Corrección en run.go y regresión en curso, log propio conservado. COMPLETE de ejecución no sustituye aprobación del contrato. Ninguna inferencia de rentabilidad desde este fixture.

Repetición sintética con calendario NY declarado: mismo fallo de aceptación (cobros0/caja4760); primera cuenta observada FAILED_RULE/LIVESIM/saldo50000. Manager solicitó primera causa reglamentaria y piso exactos; investigación del integrador en curso, sin atribuir causa no probada ni aceptar COMPLETE como resultado financiero correcto. Evidencia relativa al workspace Aranea: `work/tradesgerard-platform-a-20261012/evidence/integrator/lifecycle-ny-test.log`.

Corte posterior del autor: corregido inicio funded con baseline diario propio y piso48000; `lifecycle-credit-test.log` demuestra en el pipeline un retiro bruto2250/neto1611, solicitado30sep, aprobado1oct, procesado7oct y acreditado8oct, caja conciliada. La prueba encontró otro defecto: el débito de retiro afectaba indebidamente la pérdida diaria oficial (base anterior51475,2 contra saldo posterior50325,2). Se corrige el cómputo DLL para separar cashflow no comercial del PnL de trading conservando piso de drawdown y defaults legacy. También se fija min-days0 explícito en términos de cada compra nueva (nil estaba bloqueando pase). Gate completo aún abierto; ningún resultado de rentabilidad atribuido al fixture.

Corte del autor posterior: PASS focalizado de `TestProgression_ExactBandsAndRealCandidateDenial`, `TestRisk_DailyWithdrawalsExcludePerformancePreserveAbsoluteDrawdown` y pruebas quiet/public proof del backtester (~4,1s). Lifecycle de23sesiones en ejecución con asserts permanentes: ningún DAILY_LOSS por inicio funded/retiro, min-days0 explícito en cada compra y evaluación con progreso suficiente entra a revisión. Pendientes matriz completa, cobertura, freeze y verificación independiente; estos PASS no los sustituyen.

Último milestone autor: `lifecycle-final-dll-test.log`, PASS27,027s. Dos evaluaciones (incluida compra posterior) pasan con3090,24netos/6días y llegan aLiveSim; primer pago2250→1611CREDITED; saldo funded50325,2 sin breach DAILY_LOSS/TRAILING. Tres cuentas preservadas, una ejecutando. Asserts permanentes para los defectos precedentes. Fixture sintético público, no evidencia de rentabilidad. Fuente mutable; restantes cap/turno/terminalidad/recursos/coverage/smoke pendientes.

TOP verifier_a solicitado gpt-6.1-sol, servido UNKNOWN, fresh-context: preparación disjunta en evidencia externa mediante mandato/canon y baseline estable. No compila ni ejecuta ni audita el source mutable antes del freeze; la prueba independiente del producto continúa NOT_RUN. Su matriz preparatoria no acredita aceptación.

Corte posterior del autor: pruebas focalizadas públicas de composición/perfil/paridad compacta/lote/resume/fallos PASS6,953s. Reporta stage/best-day/saldo/equity públicos para MM, pausa con costo de salida reservado, selección bloqueada por órdenes/claims pendientes, fees/renovación y conteos del lote. Gaps funcionales declarados: ruina explícita y revisión robusta de fallos tempranos/cleanup, más CLI/manual/build final. Manager prioriza cerrar esas capacidades y congelar CANDIDATE_FOR_AUDIT con tests/cobertura pendientes declarados si los hay; el verificador ejecutará su matriz propia y el integrador corregirá después. Esto no reduce el mínimo final95% ni §10 y no habilita GLM.

Avance posterior: caja/ruina y search/fault/batch PASS8,946s antes de cambios finales de durabilidad. Autor confirmó/corrigió riesgos señalados por manager: readback fallido degrada a FAILED con causa durable; temporales JSON usan creación exclusiva y borrado sólo de archivo propio. Repetición postcorrección pendiente. Siguiente hito del integrador: CLI prepare/manual, regresiones actuales, cobertura honesta y freeze de auditoría.

Preparación de freeze: TestPlatform/TestSearch actual PASS; TCR mínimo aplicado y provider completo PASS. Baseline/actual con la misma selección causal heredada y `-p1` PASS0,080s/0,087s; paquetes SDK focalizados del baseline PASS. Coverage nuevo provisional1050/1425=73,68%, gap explícito frente al95% exigido. La medición anterior multipaquete con paralelismo por defecto no se usa como comparación válida. Toolkit canónico integrado. Integrador prepara commit/build limpio y smoke CLI real de60min; manager no modifica SDD/source durante ese freeze. Candidato para auditar y corregir, sin readiness.

Recoger candidato del integrador y ejecutar source/build exactos mediante TOP independiente del producto. Corregir gaps materiales antes de readiness; si existe bloqueo real, conservar causa, evidencia y continuidad. SDD source: `xKoRx/echo:specs/FEAT-TRADESGERARD-PLATFORM-A/`; nuevo worktree relativo a Aranea `work/tradesgerard-platform-a-20261012/echo`. Documentación Agents-OS en master con sincronización automática observada; no atribuir commits sync al manager ni afirmar push sin verificar.

### Freeze vigente y siguiente gate

Commit `06ab6b12d2e4701d21ee8506238a481c5c47af5e`, árbol limpio verificado por manager. Binario `work/tradesgerard-platform-a-20261012/evidence/integrator/bin/echo-backtest`, SHA256 `7afb11bc32b5d5e3a0330589aa9f0b75310eb2c11193d64204fb5a7ee56951ba`; Go1.27.1, VCS embebido mismo commit, modified=false. Manager corroboró HEAD/status/hash/metadata, sin ejecutar campañas. Detalle en [[TRADESGERARD-EVIDENCE-A]].

Autor reporta smoke NQZ5 real2025-10-28T14:00Z→15:00Z: catálogo COMPLETE,15008/15008minutos requeridos y60/60trading; campaña COMPLETE/conciliada/caja4880/HORIZON_CENSORED. Entrada de30contratos rechazada por cap del proveedor,0fills: prueba de pipeline/rechazo, no de ejecución financiera real ni rentabilidad. Resume exacto skipped1; BASIC replay detallado IDENTICAL94798records. Configs persistentes en evidencia/smoke. Verificador autorizado a casos propios sobre este freeze, sin escrituras de producto; especialista de cobertura prepara tests externos disjuntos, sin ejecutar. Tras findings, único integrador corregirá y se verificará nueva identidad. No READY_FOR_GLM.

Recibo final del primer shot autor: `evidence/integrator/CANDIDATE-REPORT.md`, `commands-executed.md`, `coverage-delta-audit.json`, `resource-receipt.json` y `closeout-metadata.json`. Coverage1081/1425=75,85965% actualiza el provisional1050 anterior; incluye hits instrumentados parciales de suites no completadas, sin convertirlos en testPASS. Shot cerrado, fuente congelada y proyecto abierto. Primer hito independiente físico: pase exacto3×870+390, igualdad30% negativa, pérdida intermedia recuperada y8ciclos en misma cuenta hasta pase PASS. Auditoría restante en curso; hipótesis de ruina con renovación impaga pendiente de falsificación.

## Fuentes

- Mandato Owner: `ECHO FUTURES — GOD LOCAL: BACKTESTER PARA TRADESGERARD`, PROMPT_VERSION 1, snapshot de entrada adjunto a la conversación de 2026-10-12.
- [[Echo Futures]] y `xKoRx/echo:v3/backtester/README.md` (manual existente, inspección TOP).
- `80-agents/skills/technical-project-manager` se resuelve en `30-resources/agents/skills/technical-project-manager/SKILL.md`; el mandato actual prevalece en modelo Sol 6.1, autonomía interna, alcance y ausencia de cuota de shots.
