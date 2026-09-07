---
type: agent_memory
scope: agent
created: 2026-07-16
updated: 2026-07-22
tags:
  - agent/internal
  - area/meli
  - app/vpp-backend
  - feature/bajo-de-precio
---

# VPP — sincronización local con develop

- Repositorio: `/Users/rjara/fuentes/vpp-backend`.
- `develop` local se actualizó con `git pull` hasta `0629adca9ac`.
- `feature/bajo-de-precio-motors` local se dejó en merge pendiente, sin commit ni push.
- Conflictos resueltos en `build.gradle` y `PriceDeprecatedComponentTask.java`:
  preservar `visLibVersion=3.4.1`, la funcionalidad de cupones de develop y el cálculo vertical-first de previous price para RES/Motors.
- Validación 2026-07-16: `compileJava`, suites focales de precio/tracking/marshaller, `test`, `archTest` y `pmdMain` en verde.
- `pr_descripcion.md` permanece no trackeado y no se incorporó al merge.

## Rollback preservando la iniciativa — 2026-07-22

- La rama `feature/bajo-de-precio-motors` fue rebobinada a `b4c7639196242166fd05944cf63ae946b8a6ad03`.
- Se creó el merge commit `85b7549b13d` con `origin/develop` actualizado (`e555ed123d3`), preservando desde el commit objetivo el task, modelo, marshaller, layouts y pruebas de bajó de precio.
- El worktree quedó limpio; el remoto de la feature sigue apuntando al historial anterior y requiere `push --force-with-lease` explícito para sincronizarlo.

## Revisión vpp-review

- Se corrigió `vpp_tests_07` moviendo las variaciones de RES/Motors a los argumentos de los `@MethodSource`, eliminando los `if/else` de los tests parametrizados.
- Se extrajo `vis/item-dropprice-motors` a una constante `UPPER_CASE` y se reemplazaron los mocks de `PriceDropMotorsModel` por builders de datos en `VipMotorsViewTrackingInfoTaskTest`.
- `vpp-review --mode manual --base origin/develop`: `PASS` en los seis agentes; quedaron solo warnings no bloqueantes.
- Validación posterior: `test`, `archTest` y `pmdMain` en verde. No se hizo commit ni push.
