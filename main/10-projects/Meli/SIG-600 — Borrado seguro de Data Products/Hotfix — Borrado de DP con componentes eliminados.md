---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[SIG-600 — Borrado seguro de Data Products]]"
related: ["[[rio-playmaker]]", "[[SIG-600 — Borrado seguro de Data Products]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# Hotfix — Borrado de DP con componentes eliminados

## Propósito

Permitir el soft delete de un Data Product cuando los deployments que lo bloquean pertenecen a componentes con `status = Deleted` (sin distinguir mayúsculas) o con `deleted_at` informado. Solicitud del owner del 2026-10-06, después del diagnóstico del 409.

## Alcance y aceptación

- `Deleted` sin timestamp y cualquier estado con `deleted_at` dejan de generar blockers de deployments.
- Un componente vigente con `deploy_requested` o `deploy_completed` sigue bloqueando, incluso cuando convive con componentes eliminados. `Inactive` sin `deleted_at` no equivale al estado `Deleted`.
- El borrado conserva filas e historial; mantiene autenticación, autorización, locks, cascade y contratos HTTP actuales.
- Ruta liviana de bugfix autorizada por el pedido de implementar el hotfix; sin cambios a las SPECs remotas, versiones productivas ni infraestructura.

## Plan y tarea

- Repo: `melisource/fury_rio-playmaker`; branch de publicación `hotfix/dp-delete-ignore-deleted-components-master`; base `master@7dbc49ccf8bb49a6998f94a55da011e54c53f661`, actualizada mediante pull local. La preparación inicial sobre develop queda conservada en la rama local `hotfix/dp-delete-ignore-deleted-components@f5a293f24` y no se publica.
- Una tarea: ajustar exclusivamente `DeploymentRepository.findAllRunningOrRequestedNotImported`, agregar regresiones a `DataProductControllerIntegrationTest` y actualizar `.testing/impact.json`, `testing-scenarios.md` y el contrato de arquitectura del DELETE.
- Validación: demostrar falla de las nuevas regresiones contra baseline; tests focalizados, contratos y regresión completa. Las consultas nativas se validan a través de Spring/H2 (L0); no demuestra integración desplegada.
- Rollout: versión prerelease desde la rama del hotfix autorizada por el owner; revisión y merge pendientes antes de una release productiva. No ejecutar deploys por este pedido. Rollback: revertir el commit del hotfix; no requiere migración ni backfill.

## Estado

Hotfix publicado en [PR draft #1267](https://github.com/melisource/fury_rio-playmaker/pull/1267) contra `master`: branch `hotfix/dp-delete-ignore-deleted-components-master`, base `master@7dbc49ccf8bb49a6998f94a55da011e54c53f661`, HEAD `9118cbe7f953a446b83432a410933ccf89cee0e2`. Un único commit y cinco archivos, +115/−193. Worktree limpio y tracking remoto configurado.

Se añadieron 17 regresiones. La preparación inicial sobre develop produjo ocho fallas esperadas antes del fix; la consulta original de blockers es idéntica en master. Las pruebas se repitieron sobre la entrega master: 4.400 tests, 0 fallas/errores, 2 skips preexistentes; line coverage JaCoCo 97,21% (15.240/15.677). Dos selectors focalizados, plan, contratos y diff check PASS. H2 con rollback transaccional de fixtures; no prueba MySQL/Fury ni integración desplegada.

El owner autorizó explícitamente publicación y apertura contra master, resolviendo el rechazo inicial de revisión automática. La preparación `f5a293f24` sobre develop permanece local; la publicación contiene únicamente el hotfix portado a master. Review humana y checks remotos pendientes; no se ejecutó deploy, F1, release productiva, migración ni mutación de datos remotos. Descripción canónica: [[Descripción PR — rio-playmaker — Hotfix componentes eliminados]].

Por solicitud explícita del owner se creó [0.0.1-delete-dp-fix](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.1-delete-dp-fix) desde esa rama. Fury confirma `FINISHED`, commit exacto `9118cbe7f953a446b83432a410933ccf89cee0e2`, `disabled=false` y `productive=false`; [build #1788](https://rp-builds-java.furycloud.io/blue/organizations/jenkins/rio-playmaker/detail/rio-playmaker/1788/pipeline/). La creación se solicitó con la CLI oficial sin `--no-tests`, cuyo código envía `run_test=true` por defecto, pero la metadata final de Fury registra `run_test=false`. No se afirma ejecución de tests en ese build; se conserva la evidencia local verde del mismo commit. Sin deploy.

## Fuentes

- [[SIG-600 — Borrado seguro de Data Products]] y solicitud explícita del owner en este chat.
- `rio-playmaker`: `AGENTS.md`, `testing.md`, `testing-scenarios.md`, `src/main/java/com/mercadolibre/rio/playmaker/repository/DeploymentRepository.java`, `src/main/java/com/mercadolibre/rio/playmaker/dtos/ComponentStatusDTO.java` y las rutas de soft delete de componentes.
