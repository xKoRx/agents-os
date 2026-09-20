---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-01-critical-config-backup]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "MP-01 A5 hallazgo compose 2026-09-20"
confidence: high
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
---

# 2026-09-20-mp01-a5-hallazgo-compose

%% Mandato MP-01 WP-A5: validación scratch del DoD exigía "restore scratch de 1 compose". Hallazgo material que cambia el criterio. %%

## Cambio

- **Tipo:** documentation (hallazgo; cero mutaciones)

## Resultado

- Los 9 targets de A5 NO tienen docker-compose.yml en rutas estándar (/opt /srv /root /home /etc, profundidad ≤4): verificado por inventario dentro del bundle capturado (0 hits en los 9 tgz). Los stacks docker de los CTs operan como servicios systemd (docker.service + containerd.service, units capturados) — composición de stacks posiblemente en exec manual o rutas no estándar.
- El criterio "restore scratch de 1 compose" del DoD es INAPLICABLE tal cual: se ejecutó validación scratch equivalente (descifrado del bundle + extracción + verificación de integridad de miembros) y queda registrado el gap: si existen stacks compose, viven en rutas no estándar → validar ubicación real con owner (posible deuda para ampliar las rutas de captura en el ciclo semanal A5).
- Implicancia positiva: el mecanismo de re-deploy de un CT docker es units + imágenes, no compose — el bundle cubre la parte crítica.

## Evidencia

`~/aranea/work/mp01-20260920/a5/raw/SHA256SUMS` (9 targets) · scratch de extracción verificado en a5.log 17:51.
