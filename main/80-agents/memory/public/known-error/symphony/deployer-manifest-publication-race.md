---
type: known_error
scope: application
created: 2026-08-01
updated: 2026-08-01
area: "[[Echo Forge]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Symphony]]"
  - "[[echo-forge]]"
related: []
aliases:
  - deployer manifest publication race
  - release waits without manifest acknowledgement
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - app/echo-forge
  - tech/symphony
  - tech/minio
  - tech/deployer-watcher
  - priority/high
---

# Symphony — publicación de manifest puede dejar un release incompleto

## Síntoma

- `deploy_release.sh` prepara un release, pero espera sin reconocer que el manifest ya fue confirmado si el entorno no tiene `rg`.
- Con más de un `deployer-watcher` local, un proceso obsoleto puede publicar o confirmar el manifest fuera del ciclo que inició el release.

## Causa

- El manifest es la señal de activación de los stagers, pero el watcher no lo publicaba de manera explícita y ordenada después de los artefactos.
- El script dependía de `rg`, que no está garantizado dentro de la sesión `screen`; además, cerrar una sesión screen no necesariamente termina sus procesos hijos.

## Impacto

- Los workers pueden quedarse mirando una versión remota vieja, o recibir un manifest antes de que todos sus artefactos estén disponibles.
- El orquestador puede quedar esperando una confirmación que sí ocurrió, pero no fue detectada.

## Detección

- Buscar en el log del deployer `Manifest publicado` o `Manifest confirmado` con `key=worker/sqx/manifest.json` y la versión objetivo.
- Antes de un release, verificar que exista un solo proceso `deployer-watcher` de producción.

## Mitigación

- Publicar los artefactos primero y el manifest al final; no avanzar el snapshot local cuando una subida falla, para reintentarlo en el siguiente tick.
- Esperar la confirmación estructurada del manifest con herramientas POSIX (`grep`), no con `rg`.
- Reanudar una versión existente sólo si su layout coincide exactamente con el manifest local; nunca recompilar ni sobrescribir un release ya creado.
- Copiar `config.json` al final del flujo de entrada para que el watcher sólo lo vea cuando los `.cfx` ya estén presentes.

## Evidencia

- Release `0.2.21`: el manifest fue confirmado en MinIO y el workflow de entrada fue iniciado tras aplicar estas correcciones.
- `go test ./deployer/watcher ./deployer/core/planner ./deployer/adapters/pathing-staticlayout ./deployer/adapters/manifest-json` y `bash -n deploy_release.sh` pasaron el 2026-08-01.
