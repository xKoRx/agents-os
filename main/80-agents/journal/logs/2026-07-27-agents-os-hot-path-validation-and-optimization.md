---
type: change_log
scope: session
created: 2026-07-27
updated: 2026-07-27
area: "[[Personal]]"
project: "[[AGENTS OS - Hot Path y Cierre Silencioso]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
  - "[[agent-constitution]]"
confidence: verified
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - project/agents-os
  - scope/session
---

# AGENTS OS — validación y optimización Hot Path

## Cambio

- **Tipo:** updated / merged / archived
- Se corrigió el hook `AGENTS.md` al root físico vigente y el instalador ahora
  genera un hook mínimo que delega el startup a bootstrap.
- Se compactaron guía, constitución, perfil global, bootstrap, retrieval y
  memoria interna global. Preferencias Meli/Aranea quedaron scoped.
- El closed club `load_policy: always` quedó en cinco archivos; decisiones y
  agente de dominio dejaron de cargar globalmente.
- Silent Close quedó sin L0 vacío, inventario de memorias ni feedback ritual.
- `.graphifyignore` excluye `.obsidian/` y `outputs/`.
- Se agregó `agents-os-doctor/scripts/doctor.py` y se repararon referencias
  relativas del core.
- El proyecto duplicado Hot Path fue fusionado y archivado.
- Corrección de portabilidad: referencias internas basadas en `VAULT_ROOT`;
  scripts y wrapper resuelven raíz en runtime, sin usuario/path hardcodeado.
- Se normalizaron también los links internos absolutos del `README.md` y de
  notas activas de proyecto que apuntaban al vault.

## Motivo

- La implementación declaraba un cold start de 3–5k, pero el set base medido
  superaba ampliamente ese objetivo y mantenía drift documental y de entidad.

## Resolución aplicada

- Runtime agent-facing mínimo; historia en proyecto/log.
- Una entidad canónica:
  [[AGENTS OS - Hot Path y Cierre Silencioso]].
- Doctor read-only, ejecutable y seguro: no imprime valores sensibles.

## Validación

- `doctor.py --strict`: `HIGH=0 MEDIUM=0 LOW=0`.
- Cold base estimado por caracteres: **~4.856 tokens**, dentro del objetivo
  blando 3–5k y ~77–80% menor que el baseline potencial 21–24k.
- `py_compile` pasó para doctor e instalador.
- Dry-run del instalador resolvió el vault real.
- Referencias relativas `.md` de skills: cero rotas.
- Cero paths machine-specific en hook, guía, skills y distribución Graphify.
- Cero referencias absolutas a la raíz del vault en documentación activa
  (fuera de snapshots/journal/archivo histórico).
- Reindex Graphify exitoso: 7.661 nodos; cero fuentes desde `.obsidian/`,
  `outputs/`, `40-archive/` o el proyecto Hot Path duplicado.
- Pendiente: gate E2E completo con agente fresco (warm, swap, degradación y
  cinco escenarios de cierre).

## Compartibilidad

- **Scope:** local
- Incluye rutas y preferencias locales; no exportar sin parametrización.
- No contiene secretos ni valores de credenciales.

## Rollback

- Revertir el parche consolidado de esta fecha y restaurar el proyecto
  histórico archivado solo si el gate E2E demuestra pérdida de calidad.
