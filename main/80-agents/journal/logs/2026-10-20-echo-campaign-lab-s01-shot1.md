# change_log — 2026-10-20 — Echo Futures campaign-lab S01 (SHOT1)

- **Entidad**: [[Echo Futures — Optimización de Campañas]] (proyecto de agente, planificador único).
- **Cambio**: ejecución del despacho SHOT1 (T1.1–T1.5) sobre `xKoRx/echo`, rama nueva `experiment/campaign-lab-s01` creada desde `20c73fd4` (descendiente verificado del corte aceptado `07cca9d3`, preservado). Commit `e5af38eb` pusheado con readback. Sin merge a master, sin PR, sin despliegue.
- **Contenido**: kernel puro `v3/sdk/futures/riskgeometry` (SizingProfile/Input/Proposal V1; consumidor de observaciones ATR14-Wilder/stdev20 causal; sizing decimal exacto, rechazos nombrados; coverage 96.7%) y tooling `v3/backtester/tools/tradesgerard/campaign-lab/` (catalog26 nativo exacto + descriptores STANDARDIZED_GEOMETRY declarados, perfiles, experiment DECLARATION_ONLY, validador/materializador stdlib fail-closed; 18 tests Python).
- **Vault**: planner actualizado por delta (estado S01, tareas T1.1–T1.5 `[x]`, bitácora, progress 0→28); tarea puente única creada en el padre `Echo Futures` y movida a `[r]` (Review). Agentes-OS master directo, sin ramas/PRs.
- **No cambiado**: TGMM, Signal, Provider, ledger, presets legacy, `feature/ef-runtime-pools` (sólo lectura), infraestructura. Cero campañas ejecutadas; sin cifras de aprobaciones.
- **Estado**: `IMPLEMENTATION_COMPLETE / G1=review`. Pendiente Owner: aceptar G1 (recibos S01) para habilitar S02 (Analytics causal + MM opt-in + ≤6 ensayos).
