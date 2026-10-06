---
type: change_log
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities: []
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

# rio-playmaker — PR del hotfix de ownership opcional

## Cambio

- **Tipo:** created / updated / conflict-resolution.
- **Archivos:** descripción del hotfix y nota del proyecto SIG-616; agent run de autorización opcional.

## Motivo

- El owner pidió crear un PR de hotfix hacia master y dejar sus checks verdes.

## Fuentes usadas

- Pedido del owner, contrato y template de rio-playmaker, diff confirmado y evidencia de Gradle/contratos/cleanup.

## Resolución aplicada

- Integración conservadora de master@5e4e2089b en hotfix/optional-dp-owner-permissions@d0135ae67; unión de escenarios del manifiesto sin perder ninguna prueba. PR #1273 creado hacia master y adjunto al chat; descripción materializada junto al proyecto.

## Validación

- Once selectores y MySQL aislado PASS; 4.453 tests, cero fallas/errores, dos skips; cobertura global de líneas 97,21% y ActionAuthorizationService 100% de líneas y ramas. Contratos y diff check PASS, worktree limpio, cleanup de containers/red/volumen confirmado. CI #5924 terminó con cinco checks obligatorios PASS; Fury reporta 202610.5.2-hotfix-1 FINISHED para el mismo HEAD. Code Scanning #5944 falló al arrancar por la policy corporativa que bloquea github-script@v7, idéntico a master. Aprobación humana pendiente; no hubo merge ni deploy.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos ni dumps; evidencia técnica de la entrega.

## Rollback

- Revertir el commit funcional mediante el workflow autorizado; merge y release no ejecutados.

## Rework por inactivación bloqueada en test3

- El reporte del usuario mostró un DP con team presente y project vacío. El guard local de inactivación rechazaba cualquiera de los dos campos ausentes antes del autorizador. Se corrigió la condición común y su precheck, incluyendo borrado por nombre; se probaron separadamente los campos faltantes y la ausencia de ambos.
- Commit funcional c6831d4a3 y merge de master@3600effbf en 916106355 publicados en el mismo PR #1273 hacia master. El conflicto del manifiesto se resolvió conservando las pruebas de ambos lados.
- 224 pruebas críticas y 96 selectores PASS; MySQL y loopback PASS; Kafka PASS tras reintentar el runner oficial en puerto local 39093, luego del primer fallo de metadata/offset. 4.607 tests completos, cero fallas/errores, dos skips; 97,24% de cobertura de líneas y 100% de líneas/ramas en los autorizadores modificados. Cleanup de cuatro runs verificado.
- GitHub confirmó MERGEABLE sobre 916106355; CI #5931 SUCCESS y cinco checks obligatorios PASS. Fury 202610.5.2-hotfix-3 FINISHED para el mismo HEAD. Review humano pendiente; sin deploy ni smoke F1 del agente. No se editó la descripción del PR durante este rework.
