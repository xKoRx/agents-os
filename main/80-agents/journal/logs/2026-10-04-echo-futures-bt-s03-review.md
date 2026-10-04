---
type: change_log
schema_version: 1
scope: session
created: "2026-10-04"
updated: "2026-10-04"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
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

# Change log — Echo Futures BT-S03

## Cambio

Creado [[Echo Futures — BT-S03 Adversarial Review]], actualizada continuidad de [[Echo Futures]], registrados tres segmentos Codex×modelo y un feedback por incidente real. Repros publicados en `xKoRx/echo:codex/bt-s03-adversarial-review@13bb72bb`; sólo tests, sin fixes ni integración D6.

## Motivo

Persistir findings y contrato de remediación para revisión del Manager. Escalar escrituras ETCD no autorizadas ocurridas en una suite legacy; no certificar recuperación ni ocultar efectos externos.

## Fuentes usadas

BT-S01/BT-S02 completos, source f41da25c, cinco subagentes, repros y suites finales aisladas. D6 nuevo delta d08a30ce sin shared-domain conflict.

## Resolución aplicada

BT_S03_REMEDIATION_REQUIRED; F04 abierto. No iniciar BT-S04. No nueva memoria pública: hazard de seed ya documentado en contrato de ambientes.

## Validación

Suites explicitadas en artifact PASS;20 tests adversariales rojos esperados; checks de source-only/tests y lint focalizado. Valores de configuración/credenciales excluidos.

## Compartibilidad

Scope local. Referencias relativas al vault/repos; sin valores secretos ni dumps de herramientas.

## Rollback

Revertir únicamente artifact/control/registro de esta sesión si el Manager lo solicita. Eso no restaura el estado de ETCD: su recuperación requiere historial autorizado por separado.
