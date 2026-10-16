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

# Echo Futures — candidato runtime creado y actualizado

## Cambio

Creación y actualización documental de `10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` por mandato Owner del 2026-10-16. Estado inicial CANDIDATO_INICIAL / NO_ACEPTADO; estado vigente CANDIDATO_R2 / DISEÑO_NO_ACEPTADO. No cambia la aceptación del proyecto, el código ni los controles del carril local. Escrituras sobre master, sin rama ni PR.

## Motivo

Conservar AS-IS localizado y decisiones progresivas en una nota separada del control de TradesGerard. No duplicar catálogo de cuentas ni estado de campañas. El segundo turno corrige el alcance de exclusión y elimina asignaciones manuales de Strategy/MM por cuenta consumible.

## Fuentes usadas

Mandato Owner PROMPT_VERSION 1 y segundo turno explícito del 2026-10-16; source Echo fijado y revalidado sin delta en `0c4aae552176fda005c44766e24dd70e8c48e589`. Lectura R2 acotada de `v3/backtester/platform_campaign.go` (blob `1bdbd20f4abf9aa89d4044fa77332d2a9801d04f`) y del inicio de `TG-FLOW.md`. Documentación primaria de Apache sobre direcciones/estado y serialización de invocaciones de StateFun; no certifica wiring de Echo. La investigación comercial R1 se retira del alcance vigente por instrucción explícita del Owner; no se repitió en R2.

## Resolución aplicada

R2 establece configuración pool–Strategy–MM, una cuenta por asociación y varias asociaciones concurrentes dentro del mismo pool, turno persistente, selección por creación, contexto de fase para MM/elegibilidad y NinjaTrader gateway-only. AccountStrategy se propone como binding efectivo automático, no alta manual por cuenta. Se reemplazan las recomendaciones R1 contradichas, conservando AS-IS y referencias de source.

Afinidad persistente entre turnos se identifica como interpretación propuesta de la prohibición de cambiar de Strategy a una cuenta ya operada; no se presenta como aprobación adicional del Owner. Arbitraje determinista, generación de claim y aislamiento de estado por asociación son propuestas técnicas. La entrega útil objetivo incluye pool compartido/rotación/múltiples módulos; probar una cuenta primero no sustituye esa entrega. Parámetros/Strategies finales siguen por decisión del Owner. No hay prompt de implementación, dispatch de agentes ni cierre.

## Validación

Creación R1 efectuada mediante el conector GitHub, no mediante ejecución del materializador canónico. Se leyeron la skill de entity-update, el contrato de schema, los templates doc/change_log y el source de materialize_schema_note.py y validate_schema_contract.py. Leer esos scripts no equivale a ejecutarlos: materialización canónica, gate por tipo y lint automatizado = NOT_RUN. La conformidad procedimental de creación queda pendiente; no hay una comparación byte a byte contra una nota materializada localmente ni una reconstrucción local ejecutada del contrato.

Readback R1 del encabezado y estado candidato del diseño en master: commit de creación `b9eb613dcb5cb6c33408bff5e72f4dfa2c295f9e`, blob remoto `015e02a29ee96d88f8c907da2772ad1060411d92`. Readback completo de la primera versión de este registro: commit de creación `9b0839c2ed22167daeb0429ddf9f63ad2f7c5276`, blob `e70598bdce6a68283f82350b930ef7c65dd5557c`.

Corrección de evidencia R1 conservada: la primera versión del registro atribuía por error materialización, validaciones y equivalencia byte-identical no realizadas. Esas afirmaciones fueron sustituidas por los pasos efectivamente observados; R2 no cambia ese límite.

Actualización R2 del documento existente mediante SHA de concurrencia leído; commit `e076fdeb5231f50ce74481cf1459191ac94ff50c`, blob `09f66b257d9d176960af8d8a0e04a4df3c4dfa7d`. Readback de las líneas 1–85 en master confirma encabezado R2, decisiones Owner, AS-IS y modelo compartido; SHA devuelto coincide con el de la actualización. No se afirma comparación local byte a byte ni lint automatizado. Este registro existente se actualiza por delta y conserva la trazabilidad anterior; su respuesta de escritura y readback posterior identificarán la revisión.

No se ejecutó código de producto, scripts, campañas ni tests de trading. La publicación documental no certifica comportamiento físico ni acepta el diseño.

## Compartibilidad

Scope local. Sin credenciales, tokens ni endpoints operativos. Sin memoria interna privada ni transcript de razonamiento.

## Rollback

Para R2, restaurar sólo el contenido anterior de la nota/registro mediante una actualización conservadora que preserve cambios concurrentes. Para la creación R1, revertir únicamente las dos notas correspondientes. No afecta producto ni los controles de TradesGerard. No cerrar sesión ni generar feedback automáticamente.
