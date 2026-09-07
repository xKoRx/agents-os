---
type: skill
schema_version: 1
name: fury-lib-consumer-deploy
scope: global
created: 2026-06-30
updated: 2026-08-24
description: Orquesta despliegues FURY de versiones de prueba de librerias Java hacia aplicaciones consumidoras. Usar cuando el usuario pida publicar una version test de java-polycard-sdk para search-middleware, publicar vis-octopus-lib para vpp-backend, importar una lib en su consumidor, crear versiones X.Y.Z-nombre-rama-sin-feature, commitear/pushear cambios y desplegar a un scope de test mediante Fury CLI.
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/deploy
  - area/meli
  - tech/agents-os
  - tech/fury
  - tech/java
  - scope/global
---

# Fury Lib Consumer Deploy

## Purpose

Ejecutar el flujo end-to-end para probar una libreria publicada en FURY dentro de una aplicacion consumidora, sin tocar scopes productivos.

## Contrato de versionado FURY — obligatorio

Definir `version` en `build.gradle` **no crea una version en Meli/FURY**. Es sólo la declaracion que Fury leera al crear la version.

El orden obligatorio es:

1. **Libreria Java:** dejar la version de test en `build.gradle`, con todos los cambios commiteados (y pusheados), y ejecutar desde el repo de la libreria:

   ```bash
   fury create-version --no-tests
   ```

   En una libreria Java no pasar la version como argumento: Fury debe leer la version efectiva desde `build.gradle`.
2. **Esperar disponibilidad real:** no tocar ni importar la libreria en el consumidor hasta que FURY confirme que la version fue creada y esta disponible (`fury list-versions`).
3. **Consumidor:** importar exactamente esa version en `build.gradle`, commitear el cambio y, si corresponde crear una version de la aplicacion consumidora, usar una version explicita de rama:

   ```bash
   fury create-version 0.0.1-nombre-rama --no-tests
   ```

   El consumidor nunca debe crear/importar una version apuntando a la libreria antes de que la version de la libreria exista en FURY.

`--no-tests` es parte de este flujo de creacion de versiones y no debe reemplazarse por `--confirmed --watch`.

Pares soportados:

| Caso | Libreria | Consumidor | Version importada |
|---|---|---|---|
| Search + Polycard SDK | `~/fuentes/java-polycard-sdk` (`melisource/fury_java-polycard-sdk`) | `~/fuentes/search-middleware` (`melisource/fury_search-middleware`) | `polycardVersion` en `build.gradle` |
| VPP + Octopus | `~/fuentes/vis-octopus-lib` (`melisource/fury_vis-octopus-lib`) | `~/fuentes/vis-vpp-backend` (`melisource/fury_vis-vpp-backend`) | buscar `visLibVersion`, `vis-octopus-lib` u otra dependencia equivalente |

## Minimal Read

1. Leer la nota canonica de cada app involucrada si se necesita contexto: `30-resources/applications/{search-middleware,java-polycard-sdk,vis-octopus-lib,vpp-backend}.md`.
2. Consultar documentacion viva del CLI antes de ejecutar si hay duda:
   - `fury docs`
   - `fury create-version --help`
   - `fury list-versions --help`
   - `fury list-infra --help`
   - `fury stage --help`
   - `fury deployments list --help`
   - `fury deployments details --help`
   - `fury deployments create --help`
3. Usar Fury CLI como camino normal. Usar MCP de Fury solo si el flujo documentado falla, el CLI queda ambiguo, o el CLI pide una capacidad que no esta cubierta por esta skill.

## Inputs

- Caso: `search+polycard` o `vpp+octopus`.
- Scope de test exacto indicado por el usuario.
- Rama actual de la libreria y del consumidor.
- Estrategia de version del consumidor: crear una version nueva equivalente o reutilizar una version test existente.
- Version base `X.Y.Z` a usar en la libreria y en el consumidor. Para Java, la version efectiva debe quedar escrita en `build.gradle` antes de crear la version FURY.

## Procedure

1. Exigir scope al inicio.
   - Si el usuario no dio un scope, preguntar `Que scope de test uso?` y detener el flujo.
   - No inferir scope por historial, lista de infra, rama ni preferencia.
   - Validar el scope en el consumidor con `fury list-infra`; debe existir y tener `Environment` igual a `Test`.

2. Preparar preflight.
   - Confirmar VPN y login FURY. Si `fury list-infra` o `fury list-versions` falla por auth/red, pedir al usuario reconectar VPN o correr `fury login`.
   - Revisar `git status --short` en libreria y consumidor. No mezclar cambios ajenos; si hay cambios no relacionados, avisar y trabajar solo con los archivos necesarios.
   - Detectar rama con `git branch --show-current` en ambos repos.
   - Construir `branch_slug` desde la rama de trabajo: quitar prefijos `feature/`, `feat/`, `fix/`, `bugfix/`, `hotfix/`; pasar a minusculas; reemplazar cualquier caracter no `[a-z0-9]` por `-`; colapsar guiones.

3. Elegir version de prueba.
   - Usar formato obligatorio `X.Y.Z-branch-slug`.
   - `branch_slug` debe salir de la rama sin prefijo: `feature/nombre-rama` -> `nombre-rama`.
   - Nunca crear, fijar ni publicar versiones productivas desde ramas test: prohibido `X.Y.Z` sin sufijo, `X.Y.Z-rc-N`, `X.Y.Z-hotfix-N`, `X.Y.Z-rc`, `X.Y.Z-hotfix` u otras preposiciones productivas. La versión productiva limpia sólo se prepara desde `master` después del merge.
   - Iterar cambiando el patch/base cuando haga falta: `X.Y.Z-branch-slug`, luego `X.Y.(Z+1)-branch-slug`, etc., o seguir la version test existente si el usuario lo pide y esta verificada.
   - Verificar existencia con `fury list-versions --limit 50` antes de elegir. Si la version ya existe, no sobrescribirla.

4. Publicar version FURY de la libreria Java.
   - Actualizar primero la version declarada de la libreria en `build.gradle`, por ejemplo `version = 'X.Y.Z-branch-slug'`.
   - Ejecutar validacion local razonable en la libreria antes de commitear.
   - Hacer commit y push de la libreria antes de crear la version FURY.
   - Solo despues del push, mostrar al usuario libreria, rama, version y comando de creacion.
   - Usar exactamente `fury create-version --no-tests` desde el repo de la libreria, dejando que Fury lea la version commiteada del proyecto Java.
   - No pasar la version como argumento en la libreria Java.
   - Consultar `fury list-versions --limit 20` hasta que la version aparezca creada/disponible o falle.
   - Esperar al menos unos minutos y no importar la version hasta que FURY confirme que esta creada/publicada.
   - Si la version falla, detener el flujo y no tocar el consumidor.

5. Importar la libreria en el consumidor.
   - Search: editar `polycardVersion = "..."` en `~/fuentes/search-middleware/build.gradle`.
   - VPP: primero localizar el punto real con `rg -n "visLibVersion|vis-octopus|octopus|previous-price"`. Si no existe un import claro en el checkout actual, detenerse y pedir confirmacion del archivo/propiedad antes de editar.
   - VPP + Octopus: antes de pushear un bump de `visLibVersion`, correr `./gradlew compileJava compileTestJava`. Si se acaba de mergear `develop`, validar que la version test importada contenga tanto las clases del feature como las clases que ya consume `develop`. Caso conocido: `3.3.0-previous-price-motors` contenia `PriceDropMotorsModel`/`VisPriceDropMotorsTask`, pero no `SellerGoodAttentionDomainModel`/`SellerReputationMotorsTask`; `0.0.21-previous-price-motors` contenia ambos sets y compilo contra el merge local.
   - Ejecutar la validacion local razonable del consumidor (`./gradlew test`, `./gradlew compileJava`, o el comando acotado que el repo use para ese cambio).
   - Corregir fallas obvias solo si pertenecen al bump/import; no abrir refactors.

6. Commit y push del consumidor.
   - Revisar diff acotado.
   - Commit sugerido: `chore: test <lib> <version>`.
   - Ejecutar `git push` a la rama actual del consumidor.
   - Si el usuario pidio tambien commitear la libreria por el cambio de version, hacer commit separado en el repo de la libreria; no mezclarlo con el consumidor.

7. Crear o reutilizar version test del consumidor.
   - Por defecto crear una version nueva con el mismo `branch_slug` y el siguiente `X.Y.Z-branch-slug` disponible para el consumidor, iterando patch/base si la version ya existe.
   - Si el usuario pide continuar con una version test existente, verificar que esa version existe con `fury list-versions --limit 50` y que corresponde a la rama/cambio esperado.
   - La version del consumidor tambien debe cumplir `X.Y.Z-branch-slug`; no usar `rc`, `hotfix`, ni version semver productiva limpia para pruebas de rama.
   - Crear la version del consumidor con `fury create-version "$APP_VERSION" --no-tests`.
   - Sólo después de que esa version exista, desplegar con `fury deployments create "$APP_VERSION" "$SCOPE" BLUE_GREEN --no-confirmation --output json`.
   - `fury stage` es un atajo de despliegue para una version ya creada; no reemplaza la creación explícita de la version del consumidor.

8. Esperar el despliegue.
   - Si el comando devuelve deployment id, usar `fury deployments details "$DEPLOYMENT_ID" --watch --interval 30 --timeout 120`.
   - Si no devuelve id, buscar activo con `fury deployments list --scope "$SCOPE" --active --output json` y luego mirar detalles.
   - Al finalizar, confirmar con `fury list-infra` que el scope de test quedo en la version esperada.
   - Si el deploy falla, devolver estado, id de deployment, scope, version y siguiente accion recomendada.

9. Evolucionar la skill despues del uso.
   - Al terminar un flujo real, revisar si hubo friccion, comando corregido, espera distinta, formato de version nuevo, archivo de version distinto o paso manual no documentado.
   - Si el aprendizaje mejora el proximo despliegue, actualizar este `SKILL.md` en el mismo cierre o dejar una tarea explicita para hacerlo.
   - Guardar memoria solo para contexto o decisiones alrededor del flujo. La instruccion operativa estable debe quedar en la skill, no solo en memoria.
   - Objetivo: que el proximo agente pueda desplegar correctamente con Fury CLI sin llamar al MCP de Fury salvo fallback.

## Output

Al cerrar, reportar:

- Caso ejecutado.
- Scope de test usado.
- Version de libreria creada.
- Archivo y propiedad actualizados en el consumidor.
- Commit y rama pusheada.
- Version del consumidor creada o reutilizada.
- Deployment id, estado final y version activa segun `fury list-infra`.
- Tests/validaciones ejecutadas.
- Mejora aplicada o pendiente para evolucionar esta skill.

## Hard Rules

- No continuar sin scope explicito del usuario.
- No desplegar a scopes productivos; solo `Environment Test`.
- No crear versiones productivas desde ramas test: siempre usar `X.Y.Z-branch-slug`.
- Una versión productiva limpia `X.Y.Z` sólo se crea, fija y publica desde `master` después del merge; esta skill no autoriza ese release productivo.
- No usar versiones `rc`, `hotfix`, `release`, ni semver limpia `X.Y.Z` para pruebas de rama.
- En librerias Java, no ejecutar `fury create-version` antes de que la version correcta este en `build.gradle`, commiteada y pusheada.
- No inventar comandos FURY: si cambia el CLI, consultar `fury docs` o `--help`.
- No usar MCP de Fury como camino normal; usarlo solo como fallback cuando el flujo con CLI documentado falle o sea insuficiente.
- No importar una version de libreria hasta que FURY confirme que fue creada.
- No reutilizar versiones test ambiguas; la version debe existir y corresponder al cambio.
- No commitear cambios ajenos ni formateos masivos no relacionados.
- En este flujo, usar `--no-tests` en la creacion FURY de la libreria y del consumidor; es parte del contrato operativo.
- No asumir que `actopus` es entidad canonica; en este vault el par confirmado es `vis-octopus-lib` + `vpp-backend`.
