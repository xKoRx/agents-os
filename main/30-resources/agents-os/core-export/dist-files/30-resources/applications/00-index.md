---
type: index
schema_version: 1
status: active
area:
aliases:
  - aplicaciones
  - catálogo de aplicaciones
tags:
  - kind/index
created: 2026-09-09
updated: 2026-09-09
---

# 📦 Aplicaciones

Catálogo canónico de las aplicaciones con las que trabaja el owner de este vault. Una fila por aplicación activa; el detalle vive en su propia página, creada desde `70-templates/application.md`.

## 📊 De un vistazo

- **Aplicaciones activas:** 0. `agents-os-install` lo puebla durante el onboarding, a partir de los repositorios que el usuario confirme.

## 📂 Catálogo

| Aplicación | Rol | Repo | Estado |
|---|---|---|---|
| _vacío_ | — | — | pendiente de instalación |

## Convención

- Los repositorios completos **no** viven dentro del vault: viven en un workspace externo. La página guarda `repo` y un path relativo a esa raíz, nunca una ruta absoluta de máquina.
- Separar lo estable (responsabilidad, rol, contratos) de lo volátil (stack, librerías, versiones, con `last_verified`).
- Toda ingesta o consulta se registra en `log.md`.
