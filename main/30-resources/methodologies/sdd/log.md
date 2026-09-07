# SDD — Bitácora (Resource Wiki)

Append-only, cronológico. Formato: `## [YYYY-MM-DD] <op> | <detalle>` con
`<op>` ∈ `ingest | query | lint`.

## [2026-08-08] ingest | Bootstrap incremental del dominio SDD

- Fuentes activas: GitHub Spec Kit, Kiro Specs, Symphony runtime governance y
  manual SDD local.
- Fuente histórica `docs/sdd/` clasificada `superseded`: su README declara el
  bootstrap pendiente, pero el runtime actual ya contiene constitution, rules,
  skills y specs.
- Creadas seis páginas reusables. No se copiaron specs concretas del repo.
- La metodología separa núcleo portable de políticas locales estrictas; los
  thresholds numéricos de Symphony no se promueven a regla global.

## [2026-08-08] query | Lifecycle brownfield y retorno de gaps

- Retrieval entró por `00-index.md` y seleccionó `lifecycle.md`.
- Graphify recuperó lifecycle, índice y fuentes GitHub/Kiro entre los primeros
  resultados; la respuesta verificable enruta gaps de outcome a SPECIFY,
  impacto a PLAN, granularidad a TASKS y defectos a IMPLEMENT.
- No se creó una página nueva: la respuesta ya está contenida en el canon.

## [2026-08-08] lint | Gate G4

- Metadata SDD: `ERROR=0 WARN=0` sobre 13 notas seleccionadas.
- Cero specs concretas copiadas; provenance resuelve a cinco notas source.
- Logs y `_sources/` están excluidos de Graphify; doctor estricto verde.

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4

- Cobertura del índice completa; provenance y exclusiones conservadas; Graphify limpio y actualizado.
