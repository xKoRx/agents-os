---
type: known_error
schema_version: 1
scope: application
created: "2026-09-02"
updated: "2026-09-03"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-controlplane-clickhouse]]"
entities:
  - "[[rio-controlplane-clickhouse]]"
related:
  - "[[rio-playmaker]]"
  - "[[Crear Context]]"
aliases:
  - password en claro en output de clickhouse
  - forCreateMV plaintext password
confidence: high
source_session: 9c1f9d46-34d9-4921-809f-b823fb3343f1
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
---

# ClickHouse CP persiste una password en claro en el output de deployment

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El output de deployment de una materialized view del control plane de ClickHouse lleva una clave `password` de primer nivel con la password **en texto claro**. Ese output lo persiste Playmaker en `deployment._values` y `service._values`, de donde cualquier consumidor de esos valores lo puede leer.

## Causa

- `DeploymentCommandResult.forCreateMV` hace `data.put(KEY_PASSWORD, mv.password())` sin cifrar. El valor viene de `CreateMatViewCommand.Result.credential().password()`, que sale de `UserProvisioningService.createUserIfAbsent` — una password generada o provista, **nunca** cifrada.
- El cifrado KMS del CP existe pero está en otro camino: `EncryptionServiceImpl` sólo lo invoca `ProvisionAndGrantUsersCommand`, alcanzable únicamente desde `UserProvisioningController` (REST). **El camino de deployment no lo recorre.**
- En el mismo archivo, `toCredentialMap` **sí** omite la password a propósito y emite sólo `{username, created}`. O sea que el propio CP sabe que no debe emitirla, y `forCreateMV` es el agujero.

## Impacto

- Una credencial real queda persistida en claro en la base de Playmaker y viaja a cualquier consumidor de `_values`. Con el `ComponentContext` de [[Crear Context]] el radio se amplía: los valores de un vecino se difunden a un topic único por ambiente que consumen todos los control planes con filtro client-side. CWE-668/497 y CWE-311/522.
- **Es preexistente y de dueño ajeno**: existe sin el PR del Context, y el fix corresponde al equipo del CP de ClickHouse.

## Detección

- `grep -n "KEY_PASSWORD" DeploymentCommandResult.java` en `rio-controlplane-clickhouse`: si aparece en `forCreateMV`, sigue vigente.
- En producción, buscar claves `password` en `deployment._values` / `service._values` de componentes `clickhouse-mat-view` diría si la fuga ya está materializada o es todavía teórica. **No verificado**: requiere query a prod.

## Mitigación

- Reportar al equipo dueño del CP de ClickHouse. El fix natural es el mismo criterio que ya aplica `toCredentialMap`: no emitir la password en el output, o cifrarla con el `EncryptionService` que el repo ya tiene antes de devolverla.
- Del lado de Playmaker no hay mitigación para **este** camino, y el motivo es más preciso de lo que parece: el flag `sensitive` **sí tiene productor** —`ClickHouseGrantedTableCreator` en `rio-materializer` lo escribe en `true` sobre las passwords CRUD y readonly, **ya cifradas con KMS**—, pero `forCreateMV` no emite envelope ni flag en absoluto, así que no hay nada que filtrar. Y aunque lo hubiera, el flag se pierde por el tipo `Map<String,String>` del contrato antes de llegar al vecino. Un control server-side real sería una allowlist por tipo de componente: alcance de la iniciativa **discovery**.
- Auditoría previa del ecosistema que ya había marcado este mismo P1: `[[signals-context-flow]]`.
