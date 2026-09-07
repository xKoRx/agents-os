---
type: agent_memory
scope: agent
created: 2026-07-17
updated: 2026-07-17
tags:
  - agent/internal
  - area/meli
  - app/vpp-backend
  - feature/bajo-de-precio
  - attention/review-diff-first
---

# VPP review: no editar findings heredados

- En `/Users/rjara/fuentes/vpp-backend`, branch `feature/bajo-de-precio-motors`, el usuario confirmó que la rama estaba lista y que RES debía permanecer tal cual `develop`.
- Error operativo de esta sesión: tratar comentarios válidos sobre lógica legacy como regresiones de la branch y modificar archivos sin necesidad.
- Regla para futuros agentes: antes de cualquier edición por review, comparar `git diff <base>...HEAD` y el diff del archivo; si la condición no fue introducida por la branch, no tocarla.
- En features multi-verticales, aislar el cambio en la vertical nueva y no forzar alineación estructural si altera una vertical existente.
- Estado final del repo: `git diff HEAD` vacío; `pr_descripcion.md` preexistente sin tocar.
