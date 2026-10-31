---
type: doc
schema_version: 1
status: active
area: '[[Personal]]'
related:
- '[[Preregistration — Prospective Economic Candidate W1-r 2026-10-31]]'
- '[[Polymarket Engine — MVP]]'
aliases: []
tags:
- kind/doc
created: '2026-10-31'
updated: '2026-10-31'
project: '[[Polymarket Engine — MVP]]'
---

# Research — E1 Opt-in Integration W1-s 2026-10-31

## Resultado y atribución

**COMPLETADO Y ACEPTADO: integración offline opt-in del modelo documentado `e = 1` implementada, probada y verificada; commit local `64ae3a6` (sin push).** Autoría de código/tests: **GLM-5.3-Flash en ZCode**, respaldo explícito autorizado tras el agotamiento de cuota MiniMax (ver historial abajo); el supervisor **Sol** ejecutó las validaciones controladas (focal, suites afectadas, build) y aceptó la integración — la ejecución de tests NO es de GLM. `L_PENDING_OWNER` permanece: el candidato completo queda **deliberadamente bloqueado por guardia real de código** hasta la decisión de L del Owner y los bindings reales. `REAL_FEE_READY=false`: modelo **hipotético condicional**, no certificación de fee de venue ni settlement. Sin discovery, captura, piloto, replay histórico, OOS, cuentas ni transacciones; sin freeze ni aprobación de adquisición.

## Historial breve (intento MiniMax preservado)

- El primer despacho (ZCode con `minimax/MiniMax-M3.1-Flash`) terminó **BLOCKED_PROVIDER_QUOTA**: HTTP 429 `rate_limit_error` código 2067 del Token Plan, exit 1, cero procesos propios; dejó únicamente un borrador de 528 líneas (`internal/economics/research_e1.go`), preservado por SHA-256 `262eae9012ca6d1e80db2502ed30f71ea46232717b4f944f34dc7869578b55ff` y retirado del checkout. Informe original de ese bloqueo conservado en la evidencia del supervisor; el recibo anterior de esta nota registraba ese estado y no se sobrescribe como autoría MiniMax.
- GLM redujo ese borrador (nunca activado como código validado) y construyó sobre el núcleo compartido ya validado (`BuildQuoteDocumentedE1` / `DocumentedE1Cost`), sin recalcular framework.

## Qué se implementó (comprometido en `64ae3a6`, 9 archivos, +3282/−6)

- **Núcleo** (`internal/economics/research_e1.go`): observaciones PIT tipadas (identidad mercado/asset, lexema de rate exacto — nunca WS 0 ni cap 1000 —, exponente, premisa taker-only, fuente/versión/raw, receive wall + capture seq, provenance, vintage desconocido); resolución fail-closed en DOS coordenadas con la política de frescura existente (`regimes.ProspectiveTickTTL`), **invariancia de prefijo** (admisibilidad temporal antes de ambigüedad de identidad: un conflicto futuro no contamina un prefijo pasado; conflicto admitido sí rechaza); pata tipada con suma exacta por nivel consumido y ledger `net = sell.NetProceeds − buy.CashDebit` (el fee SELL nunca se resta dos veces), banda **floor5/ceil5 por pata** con todos los extremos reportados; nulls con razón, nunca 0.
- **Gate real** (`internal/strategy/pocs/sports/`): opt-in explícito (`research_cost_model=documented_e1` + schedules declarados); ausente ⇒ legacy intacto byte a byte; modelo desconocido rechazado; los dos universos de costo no se mezclan. El cutoff del gate es el **frame de señal congelado en Detect** y Evaluate verifica su contexto; un Evaluate tardado rechaza (`RESEARCH_E1_EVALUATION_CONTEXT_MISMATCH`) y nunca emite candidato. Fee SELL que excede proceeds ⇒ REJECT por costos (`EXIT_FEE_EXCEEDS_PROCEEDS_E1`), sin net-edge inventado; `BREAKEVEN_BID_NOT_DERIVED_E1` explícito (sin B\* solver).
- **Analizador** (`cmd/researchpilot/`): guardia de despacho real — la selección CLI **propaga `L_PENDING_OWNER`** (sólo analyze la acepta y sin habilitar nada) y `analyzeEpisode` se niega **antes** de abrir journal/store; fila E1 con contrato corregido: entrada = siguiente frame usable **mismo asset en orden causal estrictamente posterior** (mismo wall sólo con seq admitida mayor), mismo tramo sin interrupción, ≤ H; salida orden ≥ entrada (salida==entrada permitida); **fee SELL as-of H mismo** (wall = horizonte; capture seq del prefijo de admisión sobre **envelopes completos** WS+REST, no sólo libros); metadata inconsistente / segmento inválido ⇒ `invalid_gap` con razón; gap/horizonte (`horizon_not_covered`) precede; fee de entrada faltante ⇒ `sufficiency_deficit`, fee de salida faltante ⇒ `entry_fill_exit_non_executable`; **7 estados only**, skips a `signal_no_fill` con razones y contadores separados; frontier desconocido ante registro malformed, regresión de wall o seq no-creciente antes del boundary, o frontier detrás del book liquidado; doble contabilidad por fila (notional recorrido, fee, `cash_debit`, net) con sizing nominal 25 congelado (no tope).
- **Tests** (3 archivos, sintéticos, sin opt-ins de receipt/histórico): núcleo con oracles independientes (100@0.50 r0.05 → 1.25; 47.16@0.53/0.61 r0.07 → 0.82232892/0.78535548, net 2.1651156, banda 2.16513/2.16511), refusal reasons PIT, same-wall por secuencia durable, gate ACCEPT 1887 bps / REJECT, cutoff congelado con fee revision interviniendo, frontier (revisión entre book y H seleccionada; post-H jamás; malformed/regresión/detrás-del-book desconocidos), orden causal, estados/skips/nulls, guardia CLI+entrada L_PENDING, legacy por defecto sin cambios.

## Validación (ejecutada por Sol, verificación independiente)

- Focal `^TestW1S` count 1: Sports 0.005s / Economics 0.004s / cmd researchpilot 0.006s — all PASS. Suites afectadas count 1: Sports 0.011s / Economics 0.008s / cmd researchpilot 7.723s — all PASS, sin flake. Build de los 3 paquetes exit 0. Hashes estables durante tests; 90 originales y 8 controles sin cambios; opt-ins de histórico/export/evidencia UNSET; sin análisis de episodio real, sin llamadas de mercado, sin captura nueva.
- Dos focos tempranos fallidos (oracle de identidad OTHER-only; oracle de prosa literal) fueron preservados como recibos y corregidos sobre hashes **nuevos**, sin retry de la misma versión. Los defectos H tempranos se establecieron por revisión de fuente; los fixtures finales los cazan específicamente. No se reclama corrida roja de cada defecto antiguo.

## Pendientes y límites

- **Candidato NO READY**: habilitar el despacho exige la decisión de L del Owner (§9 de W1-r) y los bindings reales (hash del prereg, regla de selección, deadlines, datos prospectivos); mientras tanto la negación CLI/entrada permanece por diseño. W1-r sigue `DRAFT_NOT_APPROVED`.
- `B\*` no se deriva bajo e1 (limitación explícita); `referenceLevel` conserva su convención existente como lógica de componente congelada, sin adjudicar L. Escenarios A/S lineales intactos como historia; `REAL_FEE_READY=false`; gap U-02 abierto.
- `supervisor.go` y el paquete base `internal/strategy` quedaron fuera del catálogo leído (usados por firma/call-sites); sin análisis end-to-end de `analyzeEpisode` sobre un episodio sellado (no existe, no se fabricó).

## Fuentes

- [[Preregistration — Prospective Economic Candidate W1-r 2026-10-31]] (candidato; D-1/D-7 actualizados en este cierre).
- [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] y [[Polymarket Engine — MVP]] (cierre de entidad).
- Journal GLM: [[2026-10-31-polymarket-w1s-glm-e1-optin-integration-summary]], [[2026-10-31-zcode-glm-5.3-flash-polymarket-w1s-glm-e1-optin-integration]], feedbacks de sesión y code-scout, change log de entidad.
- OUT propio: `validated-baseline/w1-s-e1-optin-glm-20261031/` (scout-pack, integration, implementation-ready, run-receipt). Evidencia del intento MiniMax: `minimax-setup/w1s/` (provider-block, partial-research_e1.go, manifiestos); ubicaciones de máquina sólo en evidencia local, no en esta nota.
