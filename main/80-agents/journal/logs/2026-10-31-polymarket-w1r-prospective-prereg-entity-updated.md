---
type: change_log
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
confidence: verified
source_session: w1r-prospective-prereg-20261031
source_feedbacks:
  - "[[2026-10-31-polymarket-w1r-prospective-prereg-feedback]]"
  - "[[2026-10-31-context-scout-w1r-prereg-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-31-polymarket-w1r-prospective-prereg-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Preregistration — Prospective Economic Candidate W1-r 2026-10-31.md` (creado; doc de Sistema 2, `DRAFT_NOT_APPROVED`).
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` (actualizado: bloque de tareas W1-r y entrada de bitácora W1-r).
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (actualizado: bloque «Cierre W1-r» y `updated` de frontmatter).

## Motivo

- El proyecto tiene un paso pendiente y explícito: la próxima prueba exploratoria económica de PE-005-R1 requiere un candidato de preregistro escrito **antes** de que exista cualquier dato prospectivo, con `L` decidido por el Owner y no derivado de resultados. Este shot consolida **ese** candidato como estado actual de Sistema 2, sin ejecutar nada y sin abrir decisiones que corresponden al Owner o al manager.

## Fuentes usadas

- `Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29.md` (valores congelados de la hipótesis).
- `Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29.md` (endpoint a horizonte fijo, taxonomía, descriptividad, presupuesto).
- `Plan — Single Episode Pilot v3 W1-i 2026-10-29.md` (deadlines absolutos, wiring **FINAL** de renovación causal `62a819d` — ancla de la vigencia en la última observación admitida), `Plan — Executable Single Episode Pilot W1-j 2026-10-29.md` (formas de comando, `H` ≤ fin real del tramo, cobertura real del horizonte), `Plan — Minimal Economic Instrumentation W1-l 2026-10-30.md` (P0-1 de L; bloqueo real de superficie por shot).
- `Research — Fee Formula Documentary W1-p 2026-10-31.md` y `Research — E1 Fee Model Conformance W1-q 2026-10-31.md` (fórmula, unidades, redondeo no adjudicado, roles, conformidad del modelo `e = 1`).
- `validated-baseline/w1-q-e1-conformance-20261031/prereg-draft.md` (draft consolidado y sustituido en alcance).
- Código en HEAD `dee7a977cdf67ad6aabdff374abecc9b0d0cdd0d`: `internal/regimes/schedule.go`, `internal/economics/scheduled.go`, `internal/strategy/pocs/sports/sports.go`, `cmd/researchpilot/{main,economics,discovery}.go`.

## Resolución aplicada

- **Un** entregable autoritativo: el candidato W1-r. No se creó un segundo preregistro, proyecto, framework, plantilla ni hipótesis; los artefactos `source-map.json`, `manager-review.md`, `run-receipt.json` y `scout-pack.json` son evidencia y resumen con enlaces al candidato, no otro plan.
- Delta único del experimento nuevo: el modelo de costo pasa a ser el **documentado `e = 1`** (W1-q) en **una sola cohorte coherente** (admisión por referencia y ambas patas a `H`), con el umbral `net_bps >= 50` sin cambio, etiquetado como **delta aritmético propuesto** que exige aprobación del manager y wiring de gate real **y** réplica/analizador; y `L` queda como `L_PENDING_OWNER` con recomendación única (excluir el frame de señal del nivel `L`), sin implementarla y sin elegirla por resultados; la referencia de detección siempre excluye el frame actual.
- Los escenarios A/S lineales quedan como historia y **no** se reetiquetan como coste de venue; el resultado del episodio del 29-10-2026 sigue válido bajo su convención registrada, aunque no comparable como la misma especificación; `REAL_FEE_READY=false` y el gap U-02 permanecen abiertos.
- Se declara que el único candidato es una **adquisición futura pre-declarada**: los datos del 29-10-2026 son retrospectivos y exploratorio/causales.
- Identidad corregida: la unidad es mercado único (`conditionId` + 2 `clobTokenIds`); compartir el mismo `K` no es identidad; la selección queda adjudicada de forma determinista por `(K, id de mercado numérico)` ascendente dentro de la página adquirida y acotada, como regla propia y más estrecha que la vigente de ≤4 mercados.
- Las dependencias técnicas se nombran (D-1…D-7) sin inventar comandos: el modelo documentado no es operativo y su delta exige wiring de gate y réplica; la regla de L elegida requeriría cambio de código; falta el binding de selección/deadlines al plan; falta el preflight de superficie; los recibos exigen opt-in explícito (W1-nR); y falta la doble contabilidad notional/caja.
- **Revisión documental del supervisor aplicada en el mismo shot** (nueve correcciones mínimas, sin ejecución): frescura anclada en la última observación admitida (W1-i §4 FINAL) corrigiendo dos afirmaciones contradictorias; cohorte/gate coherente con el delta aritmético etiquetado y sin afirmar el gate intacto; selección de mercado determinista; PIT en dos coordenadas; presupuesto nominal vs débito de caja; sensibilidad de redondeo bilateral por pata sin redondeo inventado por fill; horizonte con cobertura real y `PnL` nulo; comandos sin duplicado con precondiciones antes de cualquier discovery; eliminación de la afirmación de "cero recursos"; y aclaración de la validez y comparabilidad de los artefactos previos. Sin cambios en la recomendación de L, en A/S, en `REAL_FEE_READY` ni en el gap U-02.

## Validación

- Validación documental: readback de los tres archivos de Sistema 2 tras la última edición y materialización canónica de las seis notas de journal vía `materialize_schema_note.py` (tipos `doc`, `session`, `feedback`, `agent_run`, `change_log`).
- Validación de repo (sólo lectura): `git -C REPO status --short` vacío y `git -C REPO rev-parse HEAD` = `dee7a977cdf67ad6aabdff374abecc9b0d0cdd0d`; el checkout no fue modificado.
- **Gap de validación declarado:** los 90 hashes sellados, la sincronización remota del vault, la integridad del episodio sellado y los procesos externos los verifica el Root **después** del cierre de esta sesión, no de forma prospectiva; esta sesión **no** los midió. La escritura local **no** prueba publicación remota (W1-q ya fue verificado remotamente por el parent; el candidato W1-r es local). Ningún archivo denegado por el hook se leyó por otra vía.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir las tres ediciones de Sistema 2 listadas arriba y eliminar el doc `Preregistration — Prospective Economic Candidate W1-r 2026-10-31.md` y la carpeta de artefactos `validated-baseline/w1-r-prospective-prereg-20261031/`. El checkout del repo no requiere rollback: no fue modificado.
