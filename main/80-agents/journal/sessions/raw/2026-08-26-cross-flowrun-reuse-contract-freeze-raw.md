---
type: raw_session
schema_version: 1
scope: session
created: "2026-08-26"
updated: "2026-08-26"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-REUSE-AND-OUTPUT-OWNERSHIP-FREEZE-TOP
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

# 2026-08-26-cross-flowrun-reuse-contract-freeze-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: ZCode (GLM-5.3, host-reported) + 3 subagentes mm-scout read-only.
- Proyecto o entidad: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] / repo `xKoRx/symphony`.
- Objetivo de la sesión: congelar en el repo el contrato de negocio de cross-FlowRun reuse y output ownership (sesión TOP documental, sin código productivo), auditar el gap real y reclasificar tracks anteriores.

## Transcript

Misión del owner (TOP `SQX-CROSS-FLOWRUN-REUSE-AND-OUTPUT-OWNERSHIP-FREEZE-TOP`, verbatim esencial; el contenido normativo completo quedó congelado canónicamente en `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE/SPEC.md` del repo):

```text
MODELO: TOP
Repo: xKoRx/symphony. Baseline esperado: 1bb5fdb... o HEAD==origin/master con sólo commits documentales.
MISIÓN: Corregir formalmente la dirección arquitectónica y congelar en el REPO el contrato de negocio real para: reutilización de estrategias entre FlowRuns; composición de flujos independientes; reprocesamiento; ownership de outputs/carpetas MinIO; continuidad de Strategy identity; Builder usando estrategias históricas como templates. NO implementar comportamiento productivo todavía. El resultado debe convertirse en FUENTE CANÓNICA para futuros agentes.
CORRECCIÓN DEL OWNER: el feature principal NO es "volver a entrar mediante Temporal Reset a la misma StageExecution COMPLETED y recuperar sus outputs". El feature real es "crear NUEVOS FlowRuns que puedan reutilizar libremente outputs históricos de otros FlowRuns como inputs para nuevas ejecuciones".
10 FROZEN DECISIONS: FD-1 FlowRun nueva ejecución de negocio; FD-2 Strategy continuity; FD-3 new execution/new evidence; FD-4 historical outputs are readable inputs; FD-5 output namespace single producer owner fail-fast pre-SQX; FD-6 sealed output ⇒ namespace nuevo; FD-7 technical retry plano separado; FD-8 metadata/pool no es identidad ni ownership (sin StrategyPool); FD-9 Builder templates producen refs nuevos; FD-10 path is not business identity.
Casos obligatorios A (branch desde Builder), B (branch desde Optimizer), C (Builder templates), D (overwrite inválido FAIL PRE-EXECUTION).
Auditar 14 desarrollos previos con clasificación KEEP_CORE / KEEP_AS_TECHNICAL_RELIABILITY / DEFER / SUPERSEDED_BY_THIS_CONTRACT / CONTRADICTS_AND_MUST_AMEND.
Auditar gap real: input reuse, strategy continuity, output ownership, output collision, provenance, builder template.
No sobremodelar (sin StrategyPool/ArtifactNamespace/StrategyDefinition/StrategyVariant/Branch/Fork). Ownership design analizar sin implementar (ATOMIC/DURABLE/PRE-SQX).
Tracks anteriores: RESUMABILITY-CERTIFICATION SECONDARY/PAUSED; RETESTER-RESUMABILITY PAUSED_PENDING_BUSINESS_CONTRACT_ALIGNMENT; SDK-MINIO-ATOMIC-CREATE DEFERRED.
Commit autorizado sin confirmación: docs(sqx): freeze cross-flow run reuse contract. Push origin/master. Preservar foreign dirty.
```

Instrucción final del usuario: «cuando termines cierra sesión y deja feedback» / «cerrar sesión con Agents OS».

## Evidencia externa

- Proceso: bootstrap Agents OS (cold start) → verificación baseline `1bb5fdb` == `origin/master`, foreign dirty preservado → 3 scouts read-only paralelos (inputs/paths, identidad, ownership/schema/builder) con evidencia file:line → spot-check directo de evidencia load-bearing (`paths.go:8-73`, `adopt_strategy.go:271-291`, migración 001) → redacción SPEC/TOP-DECISIONS/fila SPECS.md → validación (links, grep contradicciones en specs durables: ninguna material, `git diff --check` limpio) → commit `9517f92d00a5be63fb74ce5279991164e957ea1d` push origin/master, HEAD == origin/master confirmado.
- Veredictos de auditoría: CROSS_FLOWRUN_HISTORICAL_READ PARTIAL; CROSS_FLOWRUN_STRATEGY_CONTINUITY SUPPORTED; NEW_FLOWRUN_NEW_EVALUATION SUPPORTED; OUTPUT_NAMESPACE_OWNERSHIP MISSING; PRE_SQX_COLLISION_GUARD MISSING; BUILDER_TEMPLATE_REUSE MISSING. BUSINESS_CONTRACT FROZEN.
- Archivos repo: `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE/SPEC.md` (nuevo), `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE/TOP-DECISIONS.md` (nuevo), `specs/SPECS.md` (fila índice, +1 línea).
- Vault: checkpoint del proyecto (append), delta de continuidad, agent-run, feedback, este L0, change log. Sin L1 (el checkpoint cubre la navegación).
