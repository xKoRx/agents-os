---
type: change_log
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Meli]]"
project: "[[Import de Refreshable Materialized Views externas]]"
application:
entities: ["[[Import de Refreshable Materialized Views externas]]", "[[RIO E2E local]]"]
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Refreshable import — sincronización y versiones de testing

## Cambio

- **Tipo:** updated.
- **Entidades:** [[Import de Refreshable Materialized Views externas]] y [[RIO E2E local]]. Estados actuales actualizados con los tres builds finalizados y disponibles para testing.
- **Estado anterior:** versiones de prueba Playmaker `0.0.2-import-ref-view-ch`, CP ClickHouse y front `0.0.3-import-ref-view-ch`, desde los commits del 26 de octubre.
- **Estado nuevo:** las tres ramas `feature/refreshable-view-import` integran develop por merge y están publicadas. Fury confirmó Playmaker `0.0.3-import-ref-view-ch` y CP/front `0.0.4-import-ref-view-ch` en FINISHED, con `ci.test_passed=true` y registry disponible en las tres.

## Motivo

- El owner pidió sincronizar las tres aplicaciones con develop y crear versiones nuevas para desplegarlas él mismo en `test`. No autorizó ni se ejecutó ningún despliegue en esta operación.

## Fuentes usadas

- Fetch de origin y confirmación de ancestro: Playmaker develop `c7d894aadfa3640a1c7ea988274a3ee008781650`, CP `b1dbe13d5ca03090d55782d28bbcfc572301bbd5` y front `c4c09b0bbffcc1fafa473ab2f2d15d373de689da`.
- Merges publicados: Playmaker `fd4b1dac089acfbaed105798d9d77e97c2df34d3`, CP `30cc111ecd915e47a1a09baf82a357cece26e0e6`, front `e0f07541bf7997ca470db10bea0ec6b32d31b753`.
- CLI oficial: creación de versiones con tests habilitados; consulta independiente de versión, rama, commit y estado. No se imprimieron tokens ni credenciales.

## Resolución aplicada

- Playmaker: el hash del catálogo se recalculó sobre el escenario combinado y se adoptó el retiro de `.testing/impact.json` de develop. Contrato de repositorio y pruebas PASS. Grimorio 27.3.0 ya estaba instalado; sólo se actualizó el dispatcher local mediante `installGitHooks`.
- Front: las dos entradas del feature se movieron a `Unreleased`, preservando el historial de releases de develop.
- CP: merge preparado en un checkout temporal propio y aplicado al worktree sin escribir los tres archivos Graphify del owner. Sus SHA-256 se conservaron; el árbol Graphify comprometido coincide con develop. Checkout temporal retirado.
- El push normal de Playmaker quedó bloqueado por la ausencia de `.grimoire/lore-readonly.local.json`. El launcher nativo además requiere que `local.adminml.com` resuelva sólo a loopback y sudo requiere contraseña. El owner autorizó explícitamente omitir sólo el pre-push de `fd4b1dac0` para crear la versión `0.0.3-import-ref-view-ch`; no es una excepción para futuros pushes. Tests de Fury habilitados.
- Selección de Docker mediante una configuración temporal sin credenciales, con `currentContext=colima-rio`; no se cambió el contexto global, no se modificó hosts y no se arrancó ningún stack ni corrida Lore en esta ronda.

## Validación

- Playmaker: 424 suites, 5327 tests, 0 fallas/errores, 3 omitidos. Contrato y control de aislamiento por tipo de componente PASS.
- CP ClickHouse: 468 suites, 5062 tests, 0 fallas/errores, 1 omitido.
- Front: 513 suites y 12194 tests PASS; lint 0 errores y 375 advertencias. Typecheck exit 2, con 122 diagnósticos idénticos por ubicación y código al snapshot exacto de develop usando las mismas dependencias; cero diagnósticos nuevos.
- Los tres repos conservan la rama esperada; Playmaker y front limpios, CP sólo con los tres cambios previos de Graphify. No se recertificó el E2E de import tras estos merges; la última corrida integrada documentada sigue siendo `run_mvpps59z4c0d5e6de3`.
- Estado final independiente de Fury: los tres commits exactos en FINISHED, `ci.test_passed=true`, `run_test=true`, `productive=false`. CP build571 y front918 disponibles en us-east-1.aws/us-east4.gcp; PM build1877 además en ca-central-1.aws. Versiones listas para el despliegue del owner en `test`, sin deploy ejecutado por el agente.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos ni contenido de credenciales; fuentes limitadas a Git, suites y metadata de versiones.

## Rollback

- No se hicieron despliegues. Para la prueba manual se pueden seleccionar las versiones previas; las nuevas no se deshabilitan ni se borran automáticamente. Cualquier reversión de los merges debe preservar la historia y los archivos ajenos.
