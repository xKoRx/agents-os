---
type: feedback
schema_version: 1
created: 2026-10-18
area: "[[Personal]]"
project: "[[Multimodal Knowledge Engine]]"
entities:
  - "[[Multimodal Knowledge Engine]]"
related:
  - "[[agents-os-bootstrap]]"
aliases: []
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
---

# 2026-10-18 — Clutifx ch02 (course-knowledge-extraction) · fricciones de sesión

## Hallazgos

1. **Subagente `documentation-verifier` no arranca en esta cuenta** — `Cannot start subagent: Provider unavailable (provider-not-found; selection=account:zai-start-plan/GLM-5.3-Flash)`. El agente especializado queda anclado a un proveedor que la sesión actual no tiene; el fallback a `general-purpose` con el mismo prompt adversarial funcionó equivalente (encontró 15 defectos reales, 1 MATERIAL). Gap: los agent types especializados del vault deberían resolver modelo desde la sesión o declarar fallback.
2. **Sync cron (1 min) convive bien con trabajo activo**: la biblioteca de 71 archivos quedó commiteada y pusheada incrementalmente por el cron sin conflicto con el trabajo en curso; el commit explícito final solo tuvo que cubrir el delta tardío. Sin fricción; solo tener presente que `git status` durante la sesión muestra casi siempre tree limpio.
3. **MEMORY.md por encima del límite** (50,9 KB vs 24,4): el índice de memoria auto carga parcial. Registrado aquí; la compactación del índice es tarea propia del sistema de memoria, no del vault.

## Qué funcionó

- Bootstrap → skill canónica → entidad: la cadena cargó exactamente lo necesario (constitución + continuidad + skill + proyecto) sin lecturas anchas del vault.
- `COURSE_KNOWLEDGE_EXTRACTION = DONE` con throughput en objetivo (99 min cómputo-subagentes por hora de video) usando revisión POR MINUTO.
