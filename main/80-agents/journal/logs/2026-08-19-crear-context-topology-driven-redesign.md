---
type: change_log
schema_version: 1
scope: session
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
related:
  - "[[signals-context-flow]]"
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

# 2026-08-19-crear-context-topology-driven-redesign

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/Crear Context/Crear Context.md` — cambio de foco a derivación topológica, hallazgo del origen de outputs, dependencia de orden, tareas y bitácora.
  - `10-projects/Meli/Crear Context/SPEC Funcional — Context IO.md` — creada.
  - `10-projects/Meli/Crear Context/SPEC Tecnica — Context IO.md` — creada, con contrato por tipo de componente y apps afectadas.
  - `rio-sdk-events` → `src/main/java/com/mercadolibre/rio/sdk/events/context/ComponentContext.java` — `Endpoint` pasa a `RelatedComponent`, se agregan `Origin` y códigos de issue; versión local `1.5.0-SIG573-LOCAL`.
  - `rio-playmaker` → `src/main/java/com/mercadolibre/rio/playmaker/service/ComponentContextBuilder.java` — derivación topológica.
  - `rio-playmaker` → `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/DispatchRequest.java` y `.../pipeline/impl/BatchDispatchServiceImpl.java` — transporte interno del Context.

## Segunda pasada — corrección de foco y envío en el mensaje

- El spec funcional se había encajonado en el contrato I/O. El Problema real es que **los control planes no tienen información**: el mensaje de deployment lleva `params` opaco, sin procedencia ni entorno. La entidad Context es el vehículo de información hacia los CP; el I/O es su primer caso de uso.
- Alcance v1 corregido: **crear el Context y enviarlo en el mensaje**. `DeploymentTriggerMessage` gana un campo `context` nullable con constructor de compatibilidad, y el adapter del pipeline lo publica.
- Resuelta la aparente contradicción con el ADR: éste posterga *cambios en los CP* y su *adopción*, no el envío. El contrato del mensaje ignora campos desconocidos, así que agregarlo es aditivo. La primera implementación había ido más allá del ADR dejando el Context fuera del wire y afirmándolo en un test.
- Verificado y corregido un error propio de análisis: enviar el Context **no** abre un canal nuevo para valores sensibles. El resolver ya sustituye placeholders por texto plano que se publica en `params`, y el cliente KMS con operación de cifrado **no tiene llamadores**. El delta real del Context es ensanchar el conjunto de outputs que viajan, no el canal. Decidido por el owner: se mantiene el tratamiento vigente, sin cifrado adicional.

## Motivo

El equipo corrigió el alcance: el Context no puede construirse leyendo lo que el front escribió; el backend debe replicar la pega del front. La derivación referencial del prototipo quedaba vacía si el front dejaba de emitir placeholders `${...}`, porque los pares sin outputs referenciados se filtraban antes de entrar al contrato.

## Fuentes usadas

- `30-resources/rio-atlas/architecture/signals-context-flow.md` — matriz canónica de tipos, contratos por tipo y mismatches priorizados.
- `80-agents/memory/public/decision/2026-08-19-crear-context-ephemeral-create-only.md` — alcance efímero y create-only, que se conserva.
- Conversaciones del equipo (dmuena, flor) sobre componentes importados, origen de los outputs y la rama base.
- Código verificado en `rio-playmaker`, `rio-sdk-events` y `ads-signals-frontend`.

## Resolución aplicada

- Separación de evidencia: los **outputs** pasan a ser topológicos porque leer el `service` de un par es leer lo que el control plane escribió, no una inferencia. Los **mappings** siguen siendo referenciales, de modo que la regla anti-invención del discovery se conserva intacta.
- Un par sin outputs se reporta con issue en vez de descartarse.
- Componentes importados resuelven outputs contra el componente original, validando el estado importado.
- Los outputs de ClickHouse se filtran por dirección de la relación, como control de seguridad.
- Se mantiene `sources`/`destinations` como nomenclatura, por decisión explícita del owner.
- Trabajo montado sobre la rama de parámetros de flor, que garantiza que los outputs del batch anterior estén commiteados.

## Validación

- `rio-sdk-events`: compilación y suite completa en verde.
- `rio-playmaker`: compilación de main y test, 14 tests nuevos del builder en verde, suite completa en verde.
- Verificado que ningún adapter serializa el Context: el wire sigue llevando solo `parameters`.
- Restaurado un cambio colateral no determinista en el swagger generado, ajeno al cambio.
- Segunda pasada: suites completas de ambos repos en verde tras el cambio de contrato del mensaje; dos tests nuevos verifican que el Context viaja con `params` intacto y que un request sin Context publica el campo nulo.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

El Context es efímero, aditivo y no consumido por los control planes: no hay estado que revertir. Rollback = revertir los commits en ambas ramas y devolver la dependencia del SDK a la versión publicada. El prototipo referencial anterior quedó preservado en un commit propio antes del rediseño.
