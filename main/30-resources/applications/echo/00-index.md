---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: echo-index
area: "[[Echo]]"
project:
created: "2026-09-13"
updated: "2026-09-13"
reviewed: "2026-09-13"
aliases:
  - "echo index"
  - "índice de Echo"
cssclasses:
  - wide
tags:
  - kind/index
  - area/echo
---

# 📂 Echo — Índice

> [!info] Subdominio de [[30-resources/applications/00-index|Applications]]
> Páginas canónicas de Echo (plataforma) y Echo Forge (fábrica), sus contratos vigentes y la frontera compartida. Reglas: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] · Bitácora compartida: `../log.md`.

## 📊 De un vistazo

- **Páginas:** 14 (2 apps + frontera + changelog + 6 contratos + 4 provenance) + 5 históricas en retención
- **Última ingesta:** 2026-09-13 (protocolo de mantenimiento incremental + checkpoints de código documentado)
- **Estado:** active

## Aplicaciones

| Página | Una línea | Baseline citado |
|---|---|---|
| [[echo-core]] | Plataforma de ejecución y Trade Journal de Echo (Bridge/Core Flink StateFun/Gateway); receptor de la frontera Forge. | echo `f7ddea18` |
| [[echo-forge]] | Fábrica cuantitativa sobre SQX (Temporal): campaña multi-wave → WFM → ranking → FinalistPromotion V2 + Apply; handoff NO cableado. | symphony `9fad768c` |

## 🔄 Mantenimiento incremental

La consolidación KBC es el **snapshot completo inicial**. Desde este punto la documentación se mantiene por **delta de Git**, no repitiendo una auditoría global de Echo/Echo Forge.

### Checkpoints de código documentado

| Fuente | Superficie cubierta | `documented_sha` | Ref al verificar | Verificado | Páginas principales afectadas |
|---|---|---|---|---|---|
| `xKoRx/echo` | `v3/` + contratos compartidos relevantes | `f7ddea18cab51db72c9765aa74381328134d7ce7` | `feature/e02-control-safety-journal-recovery` | 2026-09-13 | [[echo-core]], [[echo-forge-integration-boundary]] |
| `xKoRx/symphony` | `sqx/` + contracts/specs Forge relevantes | `9fad768ccd1f9d25ebb535a2d26edb3d74556c10` | `feature/f04-magic-version-handoff` | 2026-09-13 | [[echo-forge]], [[echo-forge-integration-boundary]] |

`documented_sha` es un **cursor documental**, no un release pointer ni “último commit del repo”. Sólo avanza cuando el delta hasta el target fue inspeccionado y toda página afectada quedó reconciliada y verificada. El nombre de branch/ref es contexto; la autoridad del cursor es el SHA exacto.

### Protocolo de refresh

1. Resolver el `documented_sha` de cada repo desde esta tabla y el target a documentar (normalmente el HEAD/merge/release que corresponda).
2. Verificar ancestry. Si `documented_sha` es ancestro del target, revisar únicamente `documented_sha..target`. Si hubo rebase/divergencia, usar el merge-base y **no fingir** un delta lineal.
3. Clasificar los cambios antes de abrir documentación:
   - `NO_DOC_IMPACT`: refactor/tests/tooling/formato sin cambio durable observable.
   - `IMPLEMENTATION_DOC_IMPACT`: runtime, lifecycle, persistence, API, wiring, failure/retry, observability, dependencias relevantes.
   - `CONTRACT_IMPACT`: contratos, wire schema, identidad, ownership o semántica frozen.
   - `BOUNDARY_IMPACT`: Forge↔Echo, handoff, ingestion, artifacts, magic/version y ownership cruzado.
4. Abrir **sólo** las páginas canónicas afectadas. No releer el subdominio completo por defecto.
5. Contrastar los claims modificados contra source/tests/config/contratos. Los contratos frozen no se reescriben para hacerlos coincidir con una implementación divergente: la divergencia se documenta como gap hasta una decisión explícita de contrato.
6. Actualizar páginas afectadas y su provenance. `last_verified` sólo cambia para superficies realmente verificadas; editar formato o backlinks no cuenta.
7. Actualizar este índice si cambió routing/resumen/checkpoint y append a `../log.md` con la operación `ingest`.
8. Avanzar `documented_sha` al target **sólo después de PASS**. Si la reconciliación queda parcial o bloqueada, mantener el cursor anterior y registrar el gap.

### Resultado esperado de un refresh

```text
repo: <echo|symphony>
from: <documented_sha>
to: <target_sha>
ancestry: LINEAR | DIVERGED
changed_paths: <n>
doc_impact: NONE | IMPLEMENTATION | CONTRACT | BOUNDARY | MIXED
pages_touched: <wikilinks>
verification: PASS | PARTIAL | BLOCKED
new_documented_sha: <sha anterior si no PASS; target si PASS>
```

Este protocolo es la especialización Echo/Echo Forge del contrato general [[30-resources/00-RESOURCE-WIKI|Resource Wiki]]: índice primero, evidencia dirigida, freshness event-driven y una fuente canónica por hecho.

## Frontera

| Página | Una línea |
|---|---|
| [[echo-forge-integration-boundary]] | Frontera Forge→Echo: contrato frozen vigente, estado implementado por lado (con baseline), gaps G1–G7 y lo que la wiki no afirma. |

## Bitácora

| Página | Una línea |
|---|---|
| [[echo-core-changelog]] | Bitácora de cambios de [[echo-core]]. |

## Contratos vigentes (source-of-record, frozen — no re-derivar)

| Contrato | Una línea |
|---|---|
| [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] | Contrato compartido SDK/analytics/handoff; autoridad congelada del lado Echo. |
| [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] | Ingestión, identidad runtime y Live Authority; autoridad del SPEC E-04. |
| [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] | CanonicalStrategyID puro + `ExecutionIntentKey` como discriminator de publication. |
| [[Echo Forge — F-02 Finalist Model V2 Contract]] | Membership estructural ≠ Top N; Promotion 2.0.0. |
| [[Echo Forge — F-03 SQX Long-Running Contract]] | elapsed ≠ failure; ceiling `MaxInt64ns−1s`; cancel de process-tree. |
| [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | Magic V1, seal write-once, HandoffManifestV1; C4/C5 verificados 2026-09-12. |

## Provenance (notas source)

| Nota | Cubre |
|---|---|
| [[Echo — Fuentes de implementación 2026-09-12 (f7ddea18)]] | Baseline Echo de campaña (fase B). |
| [[Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c)]] | Baseline Symphony de campaña (fase C). |
| [[Echo — Fuentes de arquitectura y producto 2026-09-06]] | Provenance histórica Echo master 04c16bd. |
| [[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]] | Provenance histórica Symphony a10c26c. |

## Histórico (retención; autoridad vigente en las páginas de arriba tras verificación)

[[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] · [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] · [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]] · [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]] · [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]
- `../log.md` — bitácora cronológica compartida del dominio `applications/`
