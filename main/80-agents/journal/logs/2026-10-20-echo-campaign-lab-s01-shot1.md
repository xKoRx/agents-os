# change_log — 2026-10-20 — Echo Futures campaign-lab S01 (SHOT1)

- **Entidad**: [[Echo Futures — Optimización de Campañas]] (proyecto de agente, planificador único).
- **Cambio**: ejecución del despacho SHOT1 (T1.1–T1.5) sobre `xKoRx/echo`, rama nueva `experiment/campaign-lab-s01` creada desde `20c73fd4` (descendiente verificado del corte aceptado `07cca9d3`, preservado). Commit `e5af38eb` pusheado con readback. Sin merge a master, sin PR, sin despliegue.
- **Contenido**: kernel puro `v3/sdk/futures/riskgeometry` (SizingProfile/Input/Proposal V1; consumidor de observaciones ATR14-Wilder/stdev20 causal; sizing decimal exacto, rechazos nombrados; coverage 96.7%) y tooling `v3/backtester/tools/tradesgerard/campaign-lab/` (catalog26 nativo exacto + descriptores STANDARDIZED_GEOMETRY declarados, perfiles, experiment DECLARATION_ONLY, validador/materializador stdlib fail-closed; 18 tests Python).
- **Vault**: planner actualizado por delta (estado S01, tareas T1.1–T1.5 `[x]`, bitácora, progress 0→28); tarea puente única creada en el padre `Echo Futures` y movida a `[r]` (Review). Agentes-OS master directo, sin ramas/PRs.
- **No cambiado**: TGMM, Signal, Provider, ledger, presets legacy, `feature/ef-runtime-pools` (sólo lectura), infraestructura. Cero campañas ejecutadas; sin cifras de aprobaciones.
- **Estado**: `IMPLEMENTATION_COMPLETE / G1=review`. Pendiente Owner: aceptar G1 (recibos S01) para habilitar S02 (Analytics causal + MM opt-in + ≤6 ensayos).

## Delta S01-R1 (2026-10-20, corrección antes de G1)

- **Cambio**: commit `8f2a8252` en `experiment/campaign-lab-s01` (sobre `e5af38eb`), push con readback. Alcance: `v3/sdk/futures/riskgeometry/` + `campaign-lab/` + delta documental.
- **R1**: validación de perfiles por valor alineada con `SizingProfileV1.Validate` (decimales finitos, positividad, identificadores, versiones ≥1, `profile_id` único) y canonicalización decimal antes del digest (`"500"`≡`"500.00"`); 8 regresiones negativas nuevas (26 tests Python totales).
- **R2**: contraste de instrumento canónico perfil↔recibido en `Evaluate` (`INSTRUMENT_MISMATCH`); identidad transportada verbatim desde `domain.Instrument.InstrumentID` sólo en la envoltura nueva; serialización la preserva.
- **R3**: `ceilDiv`/`floorDiv` con guard `IsInt64` ⇒ fuera de rango es rechazo explícito (repro 2^63 ticks: antes wrap→clamp a 1). Reward/quantity overflow cubiertos.
- **Evidencia**: Go coverage 97,7% (piso 95); Python 26/26 (18 originales preservados); `validate`/`materialize` deterministas con manifest `489a7c06…` sin cambios.
- **Planner**: fila G1 ahora `delivered: S01+S01-R1 en review @ 8f2a8252` (sin aceptación del ejecutor); estado y bitácora por delta. Auditoría pre-research en `20c73fd4` registrada, conclusiones intactas.
- **Estado**: `S01-R1 COMPLETE / G1=review`. STOP sin S02 ni campañas.
