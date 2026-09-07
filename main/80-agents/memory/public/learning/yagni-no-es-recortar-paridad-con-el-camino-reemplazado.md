---
type: learning
schema_version: 1
scope: global
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-playmaker]]"
entities:
  - "[[rio-playmaker]]"
related:
  - "[[Crear Context]]"
aliases:
  - yagni no aplica a paridad
  - el piso de un reemplazo
confidence: high
source_session: 9c1f9d46-34d9-4921-809f-b823fb3343f1
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
---

# YAGNI no es recortar paridad con el camino que se reemplaza

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- YAGNI y KISS aplican a **funcionalidad que nadie usa todavía**, no a **paridad con lo que el sistema ya hace**. Cuando algo reemplaza a un mecanismo existente, el piso no es cero: es lo que el mecanismo viejo ya entrega. Un recorte por debajo de ese piso se ve como simplificación en el diff y es una regresión en producción.
- Antes de cortar una pieza por "especulativa, nadie la pidió", hay que **leer el camino que se reemplaza y listar qué resuelve**. Todo lo que resuelva es piso, no alcance opcional.
- Cuando la paridad se implemente, **reusar el mismo servicio** en vez de reescribir la lógica: así la semántica es idéntica por construcción y no por parecido.
- Corolario del mismo caso: **un control que no puede disparar es peor que ningún control**, porque su métrica clavada en cero se lee como "no hay problema". Vale igual para un flag sin productor y para un guard que quedó inalcanzable después de arreglar la causa raíz — hay que borrarlo, no dejarlo de adorno.

## Aplicabilidad

- **Cuándo cargarlo:** al decidir el alcance de algo que reemplaza, envuelve o duplica un camino existente; al recortar una implementación previa por sobre-ingeniería; al justificar un recorte con "ningún consumidor lo pidió".
- **Cuándo no cargarlo:** en features nuevas sin predecesor, donde YAGNI aplica sin matices.

## Entidades relacionadas

- [[rio-playmaker]], [[Crear Context]]

## Evidencia

- En el PR #1068 recorté del `ComponentContext` toda la resolución cross-data-product argumentando que era superficie de autorización nueva para un dato que ningún control plane había pedido. `params` —el camino que el Context viene a reemplazar— **ya resolvía componentes importados**: `ParameterParseServiceImpl` sigue `sourceComponentId` hasta el original, resuelve el ambiente por nombre con fallback staging↔test y lee el `_values` del original, **sin ninguna autorización**. El recorte dejó al Context estrictamente por debajo de `params`, que es lo contrario del objetivo declarado.
- La implementación anterior había ido al otro extremo: un gate de `import_authorization` con validación del par (copia, original), **más restrictivo que el camino existente**. La referencia correcta no era ni sacarlo ni endurecerlo, era hacer lo mismo que ya hace el código que se reemplaza.
- Criterio del dueño, textual: *"la idea es tener exactamente la misma data con `params` y contexto, pero en el contexto la data está estructurada"*.
- Dato que se repitió mal varias veces en el proceso: una copia importada vive **dentro** del data product que importa; lo que apunta afuera es `sourceComponentId`. Gatear por "el data product difiere" es un no-op.
