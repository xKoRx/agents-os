---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[Presentación deployments en RIO]]"
sources:
  - "[[ads-signals-knowledge-library-repo]]"
related:
  - "[[RIO]]"
  - "[[Presentación deployments en RIO]]"
  - "[[Signals Knowledge Harness]]"
  - "[[signals-knowledge]]"
last_verified: 2026-09-01
confidence: medium
aliases:
  - RIO Knowledge Library
  - ADS Signals Knowledge Library
  - knowledge de RIO
tags:
  - kind/resource
  - area/meli
  - app/rio
created: "2026-09-01"
updated: "2026-09-01"
---

# ads-signals-knowledge-library

## Síntesis vigente

- **Qué es:** knowledge library interna de RIO/Signals, construida como 129 documentos navegables bajo `docs/`, más templates, scripts de validación y evaluaciones reproducibles. Organiza el dominio por orientación, plataforma, flujos, servicios, troubleshooting, contratos, skills, wiki, gobierno, feature catalog y evaluaciones.
- **Rol en el vault:** es el puntero canónico vigente para conocimiento compartido de RIO y **reemplaza** a [[signals-knowledge]]. El repo vive fuera del vault; esta página registra identidad, lifecycle, confianza y contradicciones, sin duplicarlo.
- **Jerarquía de verdad:** para comportamiento operacional, el código `origin/master` del servicio dueño prevalece sobre esta librería; la librería prevalece sobre wikis secundarias. Su propio `AGENTS.md` exige esa regla.
- **Uso recomendado:** entrar por `README.md` o `docs/00-start-here`, bajar a flows/contracts/services y abrir evidencia L4 sólo cuando la pregunta lo requiera. Para decisiones sensibles, comprobar `docs/08-governance/source-manifest.md` contra los HEAD actuales.
- **Cobertura:** 16 apps de Spellbook más repos relacionados; arquitectura y journeys RIO, fichas de servicio, runbooks, contratos transversales, 516 feature IDs declarados y suites de evaluación.
- **Auditoría vigente:** [[Revisión de ads-signals-knowledge-library]] detectó buena arquitectura documental, pero 17 errores del validador y drift material en Signals, Fury, Observability, routing/order/logs de Playmaker. Por eso `confidence: medium` hasta refrescar fuentes y dejar el gate verde.

## Evidencia y provenance

- **Fuente:** [[ads-signals-knowledge-library-repo]] — `repo: ads-signals-knowledge-library` · `path: ads-signals-knowledge-library`, relativo a [[Fuentes — Workspace de repositorios]] (`~/fuentes`).
- **Snapshot revisado:** `master@c2e83fdbdc38cbc089328d0c67d7bf25e15f762a`, alineado con `origin/master` y worktree limpio al 2026-09-01.
- **Revisión completa:** superficie de 148 archivos inventariada y validada; lectura profunda de startup, arquitectura, flujos, servicios, troubleshooting, contratos, skills/context packs, gobierno, feature catalog, evaluaciones y scripts; contraste con `origin/master` de los repos del deployment path.
- **Gate reproducido:** `ruby scripts/validate_library.rb` → `LIBRARY_VALIDATION_FAIL errors=17`.

## Límites y contradicciones

- **Frescura:** el manifest fue verificado el 2026-08-28; desde entonces cambiaron repos materiales. No asumir que `last_verified` de una página representa el HEAD vigente.
- **Integridad:** tres freezes apuntan a un commit inexistente y una evaluación contiene dos links `.sdd` rotos.
- **Drift funcional:** la librería aún describe Signals como placeholder, omite capacidades Fury y Observability actuales y no refleja las 11 rutas BigQueue ni `FORCE_CONFIG_ORDER` de Playmaker.
- **Producción fuera del repo:** scopes, filtros BigQueue y overrides runtime no están probados por la librería ni por la auditoría local; deben verificarse operacionalmente.
- **Lifecycle anterior:** [[signals-knowledge]] y [[signals-knowledge-repo]] se conservan sólo como registro de la knowledge reemplazada.
