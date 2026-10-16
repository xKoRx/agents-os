---
type: change_log
schema_version: 1
scope: session
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
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

# Echo Futures — candidato runtime creado

## Cambio

Creación documental de `10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` por mandato Owner del 2026-10-16. Estado CANDIDATO_INICIAL / NO_ACEPTADO. No cambia la aceptación del proyecto, el código ni los controles del carril local. Escritura solicitada sobre master, sin rama ni PR.

## Motivo

Conservar AS-IS localizado, hipótesis delimitadas, modelo inicial y tres decisiones de producto pendientes en una nota separada del control de TradesGerard. No duplicar catálogo de cuentas ni estado de campañas.

## Fuentes usadas

Mandato Owner PROMPT_VERSION 1; source Echo fijado y revalidado en `0c4aae552176fda005c44766e24dd70e8c48e589`; autoridades y fuentes first-party enlazadas en la nota. Las páginas oficiales de Earn2Trade sobre múltiples cuentas, trade copiers y términos fueron abiertas y leídas el 2026-10-16. Su lectura no aporta autorización específica para la automatización de Echo.

## Resolución aplicada

Se reutilizan entidades y owners existentes en el candidato. Se distinguen evidencia de código, reportes de fixture, evidencia física fechada, propuestas y desconocidos. No se presume permiso LIVE ni ejecución física completa.

## Validación

Creación efectuada mediante el conector GitHub, no mediante ejecución del materializador canónico. Se leyeron la skill de entity-update, el contrato de schema, los templates doc/change_log y el source de materialize_schema_note.py y validate_schema_contract.py. Leer esos scripts no equivale a ejecutarlos: materialización canónica, gate por tipo y lint automatizado = NOT_RUN. La conformidad procedimental de creación queda pendiente; no hay una comparación byte a byte contra una nota materializada localmente ni una reconstrucción local ejecutada del contrato.

Readback efectuado del encabezado y estado candidato del diseño en master: commit de creación `b9eb613dcb5cb6c33408bff5e72f4dfa2c295f9e`, blob remoto `015e02a29ee96d88f8c907da2772ad1060411d92`. Readback completo de la primera versión de este registro: commit de creación `9b0839c2ed22167daeb0429ddf9f63ad2f7c5276`, blob `e70598bdce6a68283f82350b930ef7c65dd5557c`.

Corrección de evidencia en esta misma sesión: la primera versión del registro atribuía por error materialización, validaciones y equivalencia byte-identical no realizadas. Se sustituyen aquí por los pasos efectivamente observados. No se ejecutó código de producto, campañas ni tests de trading. La publicación documental no certifica comportamiento físico ni acepta el diseño.

## Compartibilidad

Scope local. Sin credenciales, tokens ni endpoints operativos. Alias de cuenta y sufijo no credencial; identidad completa permanece en la autoridad D6 existente. Sin memoria interna privada ni transcript de razonamiento.

## Rollback

Revertir sólo la creación de esta nota y este registro, preservando cualquier cambio concurrente posterior. No afecta producto ni los controles de TradesGerard. No cerrar sesión ni generar feedback automáticamente.
