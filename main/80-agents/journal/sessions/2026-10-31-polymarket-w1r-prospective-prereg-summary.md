---
type: session
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Preregistration — Prospective Economic Candidate W1-r 2026-10-31]]"
aliases: []
confidence: high
source_session: w1r-prospective-prereg-20261031
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# Preregistration — Prospective Economic Candidate W1-r 2026-10-31

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Consolidar **UN** preregistro candidato (**DRAFT_NOT_APPROVED**) para la próxima prueba exploratoria **económica** de PE-005-R1, reutilizando el draft de W1-q y los planes vigentes, **sin ejecutar nada** de lo propuesto.

## Contexto cargado

- Bootstrap AGENTS OS en cold start (constitución, perfil global, memoria interna global única, índice de skills, registro de routers, skill de retrieval); entidad `[[Polymarket Engine — MVP]]`, área `[[Personal]]` ⇒ DEFAULT sin router de dominio.
- Fuentes canónicas: prereg v1 (W1-g), prereg v2 (W1-h), plan v3 (W1-i), plan ejecutable (W1-j), plan de instrumentación (W1-l), research W1-p y W1-q, MVP y continuidad.
- Lectura dirigida de código en HEAD `dee7a977cdf67ad6aabdff374abecc9b0d0cdd0d` (árbol limpio): `internal/regimes/schedule.go`, `internal/economics/scheduled.go`, `internal/strategy/pocs/sports/sports.go`, `cmd/researchpilot/{main,economics,discovery}.go`.
- Context scout en modo `inline-fallback` (`dispatch_id=w1r-prereg`): no se repitió code-scout porque el pack W1-q estaba fresco y los helpers nuevos no conectan con el piloto.

## Trabajo realizado

- Redactado el candidato con §0–§10: autoridad y delta congelado, parámetros PIT, mapeo explícito del modelo de costos, entrada/salida y contabilidad, ventana futura y requisitos de datos, número/selección/independencia/muestra, evidencia faltante y gate de admisión, instrucciones listas con dependencias, decisión `L_PENDING_OWNER`, y qué NO hace.
- Aplicadas las correcciones obligatorias al draft de W1-q: sólo adquisición **futura** pre-declarada (los datos del 29-10-2026 son retrospectivos/exploratorio-causales), PIT por orden del observador y no por "as-of conocido", y L con recomendación única, sin implementarla ni elegirla por resultados.
- Nombradas las dependencias técnicas reales sin inventar comandos: el modelo documentado `e = 1` no es operativo hoy (y su delta exige wiring de gate real **y** réplica/analizador), y la regla de L elegida requeriría cambio de código.
- **Revisión documental de Sol aplicada en el mismo shot** (nueve correcciones mínimas, sin ejecución): frescura anclada en la última observación admitida (W1-i §4 FINAL); cohorte única coherente con `e = 1` como delta aritmético propuesto con aprobación del manager y wiring de gate real **y** réplica; selección de mercado determinista por `(K, id de mercado numérico)`; PIT en dos coordenadas; presupuesto nominal de dimensionamiento vs débito de caja reportados por separado; sensibilidad de redondeo bilateral por pata sin redondeo inventado por fill; horizonte con cobertura real y `PnL` nulo; comandos sin duplicado con precondiciones antes de cualquier discovery; recibos bajo opt-in explícito de W1-nR; y eliminación de la afirmación de "cero recursos" con la aclaración de comparabilidad de los artefactos previos.
- Cero código, tests, build, auditorías SDK/web/mercados, capturas, re-score, piloto, gate, L ni modelos alternativos; cero escrituras en el checkout; ninguna adquisición ni operación de producto adicional.

## Artifacts creados o modificados

- `10-projects/Personal/Polymarket Engine/Preregistration — Prospective Economic Candidate W1-r 2026-10-31.md` (**creado**, autoritativo).
- `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` (delta W1-r en tareas y bitácora).
- `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (nuevo bloque «Cierre W1-r»).
- `validated-baseline/w1-r-prospective-prereg-20261031/`: `source-map.json`, `manager-review.md`, `run-receipt.json`, `scout-pack.json`.
- Journal: este resumen, el feedback de sesión, el feedback de scout (`context-scout`), el agent run y la bitácora de entidad del 31 de octubre.

## Memoria propuesta o creada

- Ninguna nota L3 nueva: el delta es de estado y decisión de proyecto, ya registrado en las notas canónicas de Sistema 2. No se tocó memoria interna.

## Decisiones

- El candidato es **DRAFT_NOT_APPROVED**: no autoriza ejecución, captura, piloto, gate ni decisión.
- `L_PENDING_OWNER` con **recomendación única**: excluir el frame de señal del nivel `L` (coherente con el literal de la v1 §4 y con referencias sólo anteriores); la referencia de detección sigue excluyendo el frame actual en cualquier escenario. **Sin cambios** tras la revisión documental.
- **Cohorte única coherente** con el modelo documentado `e = 1` desde la admisión por referencia hasta BUY/SELL a `H`, con el umbral `net_bps >= 50` sin cambio; es un **delta aritmético propuesto** que exige aprobación del manager y wiring de gate real **y** réplica/analizador, no una nota.
- Los escenarios A/S lineales quedan como historia: no son coste de venue ni compiten con el modelo documentado `e = 1`; el resultado del episodio del 29-10-2026 sigue válido bajo su convención registrada, pero no comparable como la misma especificación.
- La identidad del experimento es de **mercado único**, con selección determinista por `(K, id de mercado numérico)`; compartir el mismo `K` no es identidad.
- `REAL_FEE_READY=false` y el gap U-02 siguen abiertos.

## Pendiente

- `L_PENDING_OWNER` (Owner): bloquea el siguiente piloto económico, no las matemáticas ya cerradas de W1-q.
- **Aprobación del delta aritmético** (manager) y revisión/aprobación del candidato; el shot queda detenido **sólo aquí**, sin cancelar el proyecto ni freeze global.
- Dependencias D-1 a D-7 antes de cualquier ejecución futura: wiring del modelo documentado en gate real y réplica, wiring de L, recepción PIT de `feeSchedule`, permisos por shot, binding de preregistro **y de selección/deadlines**, recibos bajo opt-in explícito y doble contabilidad notional/caja.

