# SIG-616 — Slice 1: autorizador común de operaciones

## Metadatos

- Tipo: Technical SPEC
- Estado inicial: Draft
- Requerimiento de origen: [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- Aplicación: `rio-playmaker`
- Baseline revisada: `origin/develop@1a4caf093`
- Cambio funcional esperado: ninguno

## Objetivo

Extraer la validación ACME introducida por el PR 1126 a una implementación reutilizable y migrar sus dos consumidores actuales, delete e inactivate, sin alterar su matriz de permisos, su orden de locks ni sus efectos.

Este slice crea la base transversal que usarán Actions y futuras mutaciones. Debe ser deliberadamente pequeño: una clase concreta, un enum de niveles y ningún framework de policies.

## Decisiones

- Sólo Tiger autentica al caller. ACME no es middleware porque la consulta precisa necesita conocer el team dueño del recurso.
- Se crea `OperationAuthorizationService`, sin interfaz paralela ni implementaciones por nivel.
- Se crea `OperationAccessLevel` con sólo `DEV_AND_UP` y `DEPLOYER_AND_UP`. `READ` no pertenece a este autorizador.
- Delete e inactivate conservan `DEPLOYER_AND_UP`: `admin`, `maintainer` y `deployer`. `committer` continúa rechazado aunque la matriz general de SIG-616 sea dev-and-up.
- El autorizador usa `AcmeClient.getOwnerProjectGrants(username, teamName, headers)` y exige match exacto de `teamName + projectCode` persistidos.
- Username, team o project nulos/blancos fallan cerrado antes de consultar ACME.
- Los roles se comparan case-insensitive, como hoy.
- Cada `require` realiza una sola invocación lógica a `AcmeClient.getOwnerProjectGrants`. La paginación y sus HTTP GET internos permanecen encapsulados e intactos en el cliente. No se agrega cache.
- Rol insuficiente y ACME no verificable conservan el `403` observable actual. La causa se diferencia sólo en observabilidad interna.
- El requisito actual `systemId != null` de delete/inactivate se conserva como precondición de compatibilidad en esos consumidores; no se filtra al contrato transversal porque ACME no lo usa.

## Alcance

Incluye:

- Crear `OperationAuthorizationService` y `OperationAccessLevel`.
- Centralizar role sets, validación de scope, consulta ACME y match de grants.
- Migrar `PipelineComponentDeleteServiceImpl` y `ComponentInactivationServiceImpl` a `DEPLOYER_AND_UP`.
- Eliminar `PipelineAuthorizationService.assertAdminAccess` y `AuthorizationUtils.requireDeployerOrAbove` cuando queden sin consumidores.
- Ajustar pruebas unitarias y de los dos consumidores.

No incluye:

- Cambiar Tiger, `SecurityContext` o rutas HTTP.
- Autorizar Actions, deployments, relaciones, pipelines u otras mutaciones.
- Modificar `PipelineAuthorizationService.assertWriteAccess`.
- Modificar `AuthorizationUtils.requireTeamAdmin` ni sus consumidores.
- Cache, annotations, AOP, motor de reglas o interfaz de una sola implementación.
- Cambiar `403` por `5xx` ante indisponibilidad de ACME.

## Estado actual

```text
delete / inactivate
  -> PipelineAuthorizationService.assertAdminAccess
     -> valida systemId + teamName + projectCode
     -> AuthorizationUtils.requireDeployerOrAbove
        -> AcmeClient.getOwnerProjectGrants
        -> match team + project + role
```

Los únicos call sites productivos de `assertAdminAccess` en la baseline son `PipelineComponentDeleteServiceImpl` y `ComponentInactivationServiceImpl`.

## Diseño objetivo

```text
[MODIFIED] delete / inactivate
  -> conserva precondición systemId y orden actual
  -> OperationAuthorizationService.require(..., DEPLOYER_AND_UP)

[NEW] OperationAuthorizationService
  -> valida username + teamName + projectCode
  -> consulta una vez getOwnerProjectGrants(username, teamName, headers)
  -> exige grant con team + project exactos
  -> valida role mediante OperationAccessLevel

[UNCHANGED] AcmeClient
[UNCHANGED] assertWriteAccess / requireTeamAdmin
```

### Contrato

```java
operationAuthorizationService.require(
    username,
    dataProduct.getTeamName(),
    dataProduct.getProjectCode(),
    headers,
    OperationAccessLevel.DEPLOYER_AND_UP);
```

`OperationAccessLevel` encapsula los sets finitos:

| Nivel | Roles permitidos |
|---|---|
| `DEV_AND_UP` | `admin`, `maintainer`, `deployer`, `committer` |
| `DEPLOYER_AND_UP` | `admin`, `maintainer`, `deployer` |

No se acepta un string libre para el nivel ni se expone `AcmeClient` a los consumidores.

### Orden de ejecución

Delete conserva:

1. Resolver Data Product.
2. Extraer caller Tiger como hoy.
3. Verificar la precondición `systemId` ya existente.
4. Autorizar `DEPLOYER_AND_UP`.
5. Resolver componente y adquirir lock.
6. Ejecutar guards y soft delete.

Inactivate conserva:

1. Extraer caller Tiger y resolver Data Product.
2. Verificar la precondición `systemId` ya existente.
3. Autorizar `DEPLOYER_AND_UP`.
4. Resolver componente/environment y ejecutar guards.
5. Adquirir lock/crear ejecución/publicar según el flujo actual.

La extracción no moverá la consulta ACME después de un lock, escritura, creación de ejecución o publicación.

## Archivos previstos

| Cambio | Archivo |
|---|---|
| Nuevo | `src/main/java/com/mercadolibre/rio/playmaker/service/OperationAuthorizationService.java` |
| Nuevo | `src/main/java/com/mercadolibre/rio/playmaker/enums/OperationAccessLevel.java` |
| Modificado | `service/impl/PipelineComponentDeleteServiceImpl.java` |
| Modificado | `service/impl/ComponentInactivationServiceImpl.java` |
| Modificado | `service/PipelineAuthorizationService.java` |
| Modificado | `util/AuthorizationUtils.java` |
| Tests | Test nuevo del autorizador y adaptación de tests existentes de ambos consumidores/helpers |

Los nombres y packages pueden ajustarse durante la implementación si la estructura real lo exige, sin cambiar el contrato ni crear capas adicionales.

## Errores y observabilidad

| Condición | Resultado |
|---|---|
| username/team/project nulo o blanco | `SecurityException` → `403`; no llama ACME |
| grant de otro team o project | `403` |
| rol ausente, nulo o insuficiente | `403` |
| excepción/timeout/respuesta no verificable de ACME | `403` fail-closed |
| grant exacto con rol permitido | continúa el flujo |

Los mensajes HTTP serán genéricos y no expondrán grants, miembros del equipo ni tokens. Logs estructurados distinguirán al menos `invalid_scope`, `insufficient_role` y `acme_unavailable`, usando nivel y causa de baja cardinalidad; nunca incluirán el Tiger token.

## Pruebas

Pruebas críticas antes del refactor mecánico y cobertura mínima de 95% del código nuevo:

- Matriz completa de roles para ambos niveles, incluyendo casing y rol nulo.
- Match exacto de team y project; grants cruzados no habilitan.
- Contract test de `AcmeClientImpl` con un fixture representativo del payload real `owner-project`, cubriendo mapping de team/project/role y la paginación existente sin depender de ACME en CI.
- Argumentos nulos/blancos fallan antes del cliente.
- Excepción de ACME falla cerrado con `403` y una sola invocación al método del cliente.
- Delete e inactivate permiten admin/maintainer/deployer y rechazan committer.
- Con username, team y project válidos pero `systemId` ausente, cada consumidor rechaza antes de invocar `OperationAuthorizationService`. Este caso debe aislarse porque el test actual también deja `projectCode` nulo.
- La autorización ocurre antes de lock, mutación, ejecución o publish.
- `assertWriteAccess` y `requireTeamAdmin` conservan comportamiento y tests.

## Rollout y compatibilidad

- No requiere migración de datos ni feature flag porque no cambia la decisión funcional esperada.
- La revisión del diff debe demostrar que sólo cambió el dueño de la lógica, no su orden ni su matriz.
- Antes de cerrar el slice se ejecuta un smoke en ambiente no productivo con un Data Product y grant reales para confirmar la convención exacta de `projectCode`; su evidencia se registra fuera de la suite automatizada.
- Ante una regresión, el rollback es el revert del slice; no hay datos nuevos que recuperar.

## Tasks ejecutables

1. Crear `OperationAccessLevel` y sus tests de matriz de roles.
2. Crear `OperationAuthorizationService` con validación de inputs, llamada única a ACME, match exacto y error mapping compatible.
3. Migrar delete preservando precondición `systemId` y orden pre-lock.
4. Migrar inactivate preservando precondición `systemId` y orden pre-side-effect.
5. Retirar sólo `assertAdminAccess` y `requireDeployerOrAbove`; mantener helpers no relacionados.
6. Ejecutar suites afectadas, contract test con fixture ACME, smoke no productivo, cobertura y revisión de logs sensibles.

## Criterios de aceptación

- Existe una única implementación concreta reutilizable de autorización por operación.
- Delete e inactivate llaman directamente al autorizador con `DEPLOYER_AND_UP`.
- La matriz allow/deny y el `403` existente no cambian, incluido `systemId` faltante.
- Cada `require` invoca una vez `AcmeClient.getOwnerProjectGrants`, cuya paginación interna no cambia, y valida team + project exactos.
- Ningún deny/error alcanza locks, escrituras o publishers que antes ocurrían después del guard.
- No se introducen interfaces, cache, annotations ni migraciones ajenas al slice.
