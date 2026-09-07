# Knowledges — Bitácora (Resource Wiki)

Append-only, cronológico. Prefijo: `## [YYYY-MM-DD] <op> | <detalle>` con `<op>` ∈ `ingest | query | lint`. Últimas ops: `grep "^## \[" log.md | tail -5`.

## [2026-08-18] ingest | Bootstrap del dominio + alta de signals-knowledge
- Creado el dominio `knowledges/` (external-resources de tipo *knowledge bundle*): `00-index.md` (`type: index`) + este `log.md`.
- Materializada la página canónica [[signals-knowledge]] (`type: resource`) desde el repo `~/fuentes/signals-knowledge`: bundle OKF del equipo Signals que cubre RIO, catalog, collector, SDK-go, CLI, migrator y frontend. `confidence: high`, `last_verified: 2026-08-18`.
- Provenance vía nota [[signals-knowledge-repo]] (`type: source`, `repo`+`path` relativos a [[Fuentes — Workspace de repositorios]]).
- Asociado el dominio al proyecto de comprensión [[Onboarding Signals]] y a la iniciativa de cambio [[Signals Knowledge Harness]].
- Contradicciones anotadas en la página: bundle en versión inicial; solapamiento con `30-resources/applications` a reconciliar (no duplicar); `signals-collector` sin nota de app propia; taxonomía OKF ≠ tipos S2.

## [2026-09-01] ingest | ads-signals-knowledge-library reemplaza a signals-knowledge
- Materializada [[ads-signals-knowledge-library]] como único knowledge bundle activo del dominio, con provenance en [[ads-signals-knowledge-library-repo]] (`master@c2e83fdbd`).
- [[signals-knowledge]] quedó `deprecated` y [[signals-knowledge-repo]] quedó `superseded`; ambas notas se conservan por trazabilidad.
- Auditoría completa persistida en [[Revisión de ads-signals-knowledge-library]]: 148 archivos revisados, gate del repo rojo con 17 errores y drift material contra `origin/master`.
- Jerarquía vigente: código del servicio dueño > knowledge library > wikis secundarias. La librería es el punto de entrada canónico, no una exención de verificar fuentes frescas.

## [2026-09-01] lint | lifecycle, cobertura y provenance de knowledges
- Cobertura manual del `00-index.md`: 0 páginas raíz faltantes; una sola resource `active` y la anterior explícitamente `deprecated`.
- Provenance resoluble: resource nueva → source activa → `repo` + `path` + checksum; lifecycle cruzado `supersedes`/`superseded_by` consistente.
- Contratos `resource` y `source`: 0 errores. `graphify-obsidian update` no alcanzó a reindexar porque el gate global encontró 25 errores y 6 warnings preexistentes fuera de este dominio; no se modificó deuda ajena.
