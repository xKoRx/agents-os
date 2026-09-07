---
type: decision
schema_version: 1
scope: application
created: "2026-08-16"
updated: "2026-08-16"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
related:
  - "[[2026-08-16-echo-forge-mt5-m0-m2t]]"
  - "[[2026-08-16-echo-forge-mt5-amendment-m0-m2t]]"
aliases:
  - Echo Forge MT5 comparability taxonomy
  - taxonomía de comparabilidad MT5
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - area/echo
  - project/echo-forge
---

# Echo Forge MT5 — Taxonomía de comparabilidad SQX↔MT5

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El proyecto [[Echo Forge - Reconciliación y Scoring MT5]] necesita comparar métricas MT5 (reporte HTM) contra métricas SQX (Reretester) para scoring shadow.
- La primera versión de la matriz semántica marcó `NO_COMPARABLE_V1` varias métricas (Sharpe, SQN, ret_dd, stagnation) argumentando fórmula no demostrada.
- El owner corrigió: no existía decisión owner declarando indicadores SQX↔MT5 incompatibles, y la falta de evidencia no es evidencia de incompatibilidad.

## Decisión

- Taxonomía obligatoria de veredictos en `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/METRIC-MATRIX.md` (repo `xKoRx/symphony`): `COMPARABLE` (equivalencia demostrada), `COMPARABLE_CONDICIONAL` (equivalencia conocida; exige basis/scope igual en runtime), `PENDING_VERIFICATION` (parece el mismo concepto; falta verificar fórmula/basis), `NO_COMPARABLE` (solo con evidencia positiva de concepto/fórmula distinta).
- Antes de cualquier veredicto se investiga el código/exporter/spec real (`EchoForgeOverviewExporter.overviewFromStats`, stub `StatsKey`, `FEAT-SQX-METRICS-CONTRACT`); si no se puede demostrar la equivalencia, queda `PENDING_VERIFICATION`.
- Prohibido mapear `z_score` (MT5) a `sqn_score` (SQX) sin evidencia; `sqn_score` se trata como `NO_BINDING_IDENTIFIED_IN_HTM`.
- Los pesos/required-metrics de la proposal `mt5_validation_delta.v1` quedan PENDING_OWNER y abiertos; M5-TOP decide el algoritmo final.

## Rationale

- La primera matriz convirtió ignorancia en incompatibilidad, cerrando la puerta a componentes válidos del score antes de investigar.
- Evidence real disponible: el plugin SQX calcula `ret_dd = net/drawdown` (equivale en forma a MT5 Recovery Factor); `PctDrawdown` existe en el engine pero no se exporta; el contract spec documenta Sharpe SQX anualizado.
- El fixture all-loss no puede distinguir bases de Profit Factor (PF=0 bajo cualquier base con GP=0), por lo que afirmar una basis de GP/GL era una sobreafirmación.

## Consecuencias

- Ninguna métrica queda `NO_COMPARABLE` sin evidencia positiva; el mapa semántico queda correcto y los cierres pendientes viven en M5-TOP.
- En runtime, lo no verificado cae a `NOT_COMPARABLE` (estado de Score) sin convertirse en incompatibilidad permanente.
- La matriz es la única fuente de veredictos de comparación; `FEAT-SQX-DEVIATION-FILTER` es consumidor enforce futuro y no duplica veredictos.

## Alternativas descartadas

- Mantener `NO_COMPARABLE_V1` por ausencia de fórmula demostrada (rechazado por el owner: inventa incompatibilidad).
- Mapear Z-Score↔SQN por analogía de concepto (prohibido sin evidencia).
