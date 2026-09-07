---
type: methodology
status: active
area: "[[Personal]]"
sources:
  - "[[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]"
  - "[[kiro-specs-structured-development|Kiro Specs — Structured Development]]"
  - "[[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]"
  - "[[symphony-sdd-manual|Symphony SDD Manual]]"
last_verified: 2026-08-08
confidence: verified
aliases:
  - SDD artifact model
  - artefactos SDD
tags:
  - kind/methodology
  - tech/sdd
created: 2026-08-08
updated: 2026-08-08
---

# SDD — Artifact Model

## Modelo mínimo

```text
repo policy/constitution
└── feature catalog
    └── feature/change
        ├── specification or requirements
        ├── design or plan
        ├── tasks
        ├── changes/ and rca/ (cuando aplica)
        └── verification
```

## Autoridad por artefacto

| Artefacto | Autoridad | Evitar |
|---|---|---|
| Constitution/policy | invariantes del repositorio | detalles de una feature |
| Catalog | identidad, ubicación y lifecycle de capacidades | duplicar la spec |
| Spec/requirements | outcomes, alcance, reglas, aceptación | mapa exhaustivo de archivos |
| Design/plan | solución, impacto, riesgos, rollout/rollback | escribir código |
| Tasks | slices, dependencias, archivos permitidos, gates | decisiones nuevas sin subir al plan |
| Change spec | delta durable sobre una capacidad | reescribir baseline como historial |
| RCA | causa y evidencia histórica de una falla | contaminar la spec vigente |
| Verification | comandos, resultados, findings y veredicto | autoaprobar sin evidencia |

## Identidad y lifecycle

- Una capacidad tiene ID estable y una baseline canónica.
- Una nueva versión de una fuente no crea automáticamente una feature `-v2`.
- Cambios con identidad propia se modelan como delta; la baseline se actualiza
  cuando cambia el comportamiento durable.
- El catálogo refleja estados reales definidos por el repositorio.
- Archived conserva historia y deja de ser autoridad vigente.

## Instancias concretas

Las carpetas `specs/<feature>/` pertenecen al repo/proyecto. Este dominio sólo
describe el patrón y enlaza fuentes; nunca copia specs reales dentro del vault.

## Fuentes y provenance

- [[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]
- [[kiro-specs-structured-development|Kiro Specs — Structured Development]]
- [[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]
- [[symphony-sdd-manual|Symphony SDD Manual]]

## Límites

- Los nombres `SPEC.md`, `requirements.md`, `design.md` o `PLAN.md` son adapters
  de herramientas/repos; la responsabilidad semántica es la parte portable.
