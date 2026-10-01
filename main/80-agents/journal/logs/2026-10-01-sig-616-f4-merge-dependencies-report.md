---
type: change_log
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities: []
related:
  - "[[2026-09-30-codex-unknown-playmaker-pr1181-finalize]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-10-01-sig-616-f4-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# SIG-616 F4 — merge de develop y reporte de dependencias — 2026-10-01

## Cambio

- **Tipo:** conflict-resolution + diagnóstico.
- **Código:** PR [#1181](https://github.com/melisource/fury_rio-playmaker/pull/1181), rama `feature/operation-authorization-by-team-f4`. Integra `develop@f087e4b7cc185d93618de4bdeaeb76b53486ac47` conservando la autorización F4 y la nueva herencia de entidades signal→Kafka.
- **Publicación:** merge `372af0bacc0b577debbde3fc693e9bdbac7e1d2f`, push normal verificado; padres `99c51fe8b` y `f087e4b7cc`. GitHub `MERGEABLE`, worktree limpio. CI [#5696](https://rp-ci-java.furycloud.io/job/rio-playmaker/5696/) iniciada para ese SHA, todavía en curso; aprobación humana pendiente.

## Motivo

Resolver los conflictos posteriores a #1219 y explicar el nodo `dependencies` rojo con evidencia de la ejecución correspondiente. El owner autorizó lectura con su sesión MeLi y pidió cierre y feedback de AGENTS OS al terminar.

## Fuentes usadas

- [Fury: ejecución ad710ac9](https://web.furycloud.io/engineering/applications/rio-playmaker/executions/ad710ac9-ce4f-4886-86ed-d6c25ce66528), PR #1181, HEAD `99c51fe8bd3da2e73ede96ae717a1ab1fae723c7`.
- [Fury: ejecución del merge 084e256d](https://web.furycloud.io/engineering/applications/rio-playmaker/executions/084e256d-8b96-48a2-b713-a41143fcb2c6), HEAD `372af0bacc0b577debbde3fc693e9bdbac7e1d2f`; confirma las mismas nueve alertas low no bloqueantes.
- [Jenkins #5696: consoleFull](https://rp-ci-java.furycloud.io/job/rio-playmaker/5696/consoleFull), mismo SHA del merge: reproduce a las 10:16:41 del 2026-10-01 `report.json` ausente, BOM subido y post de flags fallido con `unexpected end of JSON input`.
- [Jenkins #5629: consoleFull](https://rp-ci-java.furycloud.io/job/rio-playmaker/5629/consoleFull), mismo HEAD; lectura autenticada autorizada, extracto sanitizado conservado como evidencia local.
- [Dependency Catalog: Troubleshooting](https://furydocs.io/dependencies-catalog-api/latest/guide/#/lang-en/Troubleshooting), canal oficial Fury Support → Build & Deploy → Dependency Catalog.
- [MeLi Toolkits: versiones no oficiales](https://furydocs.io/meli-toolkits-docs/0.6.0/guide/#/lang-en/unofficial_versions), límites de soporte de Early Access.
- Git local y remoto, contrato staged, catálogo de escenarios, tests y regresión del árbol integrado.

## Resolución aplicada

El guard configurado sigue usando el username autenticado que pasa el controller y ocurre antes de guardar relaciones, incrementar versiones o propagar/desconectar entidades. La herencia incorporada desde develop usa la misma identidad para auditoría. Tests verifican allow en orden y deny para conectar y desconectar sin efectos. El HTTP test nuevo atraviesa el filtro real de seguridad.

Se conservan la excepción de DPs sin equipo aceptada por el owner y el borrado de relaciones cross-DP históricas. No se regularizan DPs ni se cambia el comportamiento de create/update. El escenario F4 pasa de `AT-090-S17` a `AT-090-S21` para evitar colisionar con el GET topology nuevo de develop.

El check MySQL detectó dos ejecuciones de timeout compitiendo: el scheduler local corre cada segundo y el test lo invoca manualmente. La frecuencia se sobrescribe a una hora exclusivamente en ese test; se mantienen las verificaciones de idempotencia, logs y no-republicación. El mismo check pasó después de la corrección.

### Reporte: qué falla en dependencias

**Confirmado en Jenkins #5629:** el build finaliza `SUCCESS`. La etapa de catálogo ejecuta cdxgen; `rp_client` busca `/app/boms/report.json` y no lo encuentra. Registra `can't find bom flags`, sube exitosamente `/boms/rio-playmaker/prs/1181/bom.json`, y luego falla publicando flags con `unexpected end of JSON input`. La instalación termina con éxito pese a ese error; el check separado de GitHub/Fury queda `FAILURE` sin anotaciones útiles.

**Confirmado en Fury tanto en la ejecución anterior como en el nuevo HEAD:** declara “9 vulnerabilities and none of them is blocker”. Todas tienen estado `low` y ninguna informa un CVE. Son ocho advertencias de deprecación y una versión no oficial:

| Dependencia | Versión observada | Mínimo sugerido por catálogo | Sunset |
|---|---|---|---|
| `java-melitk-config` | `0.5.0` | `2.0.0` | 2026-10-28 |
| `rate-limiter` | `3.1.5` | `4.0.1` | 2026-12-11 |
| `routing` | `3.1.3` | `4.0.2` | 2026-12-11 |
| `threading` | `1.2.2` | `3.0.0` | 2026-12-11 |
| `java-melitk-secrets` | `1.3.5` | `2.0.0` | 2026-12-11 |
| `meli-restclient-context` | `3.1.2` | `4.0.0` | 2026-12-11 |
| `meli-restclient-core` | `3.1.2` | `4.0.0` | 2026-12-11 |
| `meli-restclient-default` | `3.1.2` | `4.0.0` | 2026-12-11 |
| `java-melitk-autobulk-lib` | `0.1.0-rc-2` | Consultar una release oficial; sin mínimo publicado | Sin fecha |

Las versiones pueden ser transitivas. `build.gradle`, settings, propiedades, locks, wrapper, `.fury` y Docker no cambiaron entre el HEAD previo que había pasado el gate y `99c51fe8b`; el merge de #1219 tampoco cambia esas superficies. No hay una nueva dependencia de F4 que explique este fallo.

**Inferencia más sustentada:** el rojo es consistente con un fallo de producción/lectura/publicación de flags del SBOM o de su consumo por el Release Process. No está probada la causa interna exacta: falta el HTTP status/body del envío y el diagnóstico downstream. El warning de cdxgen sobre root no demuestra causalidad. Las nueve alertas existen, pero esta ejecución no las identifica como bloqueantes.

**Acción recomendada:** revisar con Fury Support (Build & Deploy → Dependency Catalog) por qué falta `report.json`, cuál fue la respuesta al post de flags y por qué el consumidor marca el nodo fallido aunque el catálogo informa cero bloqueantes. Incluir ejecución, PR y SHA arriba. No se envió ningún mensaje o ticket externo. Planificar las actualizaciones de libs por sus sunsets como trabajo separado, con validación de compatibilidad, sin usar un upgrade especulativo para tapar el error del pipeline.

## Validación

- 61 selectores focalizados del árbol integrado: PASS.
- Health local: PASS; loopback MySQL y Kafka: PASS con cleanup certificado tras sincronizar el scheduler del test.
- `./gradlew check jacocoTestReport --offline --no-daemon`: PASS; 4.195 tests / 377 suites, cero fallas/errores y dos skips preexistentes de TopologicalSortServiceImplTest. Líneas 15.043/15.474 cubiertas, 97,21%.
- Contratos staged y plan final: PASS. Los 61 selectores pasaron antes del fallo de carrera del check MySQL; se reejecutó ese runner corregido y el check Kafka restante, ambos PASS. No se presenta esa primera ejecución interrumpida como un run limpio completo.
- SHA remoto, mergeabilidad y limpieza comprobados después del push; descripción en español actualizada y verificada por readback exacto. Nueva CI en curso, reproduciendo el error de flags en #5696; Fury del mismo SHA informa nueve avisos low no bloqueantes.
- No se ejecutó Zord por instrucción del owner. Sin deploy, merge del PR o autorización de excepciones de catálogo.

## Compartibilidad

- **Scope:** local. El diagnóstico técnico puede copiarse al canal interno de soporte indicado.
- **Redacción revisada:** sin credenciales, tokens, dumps de sesión ni datos personales; los enlaces apuntan a fuentes internas del mismo proyecto.

## Rollback

- Si el merge ya publicado requiere revertirse, usar un commit de revert convencional del merge tras revisar los padres; no reescribir historia remota ni omitir los guards F4.
- Los avisos y el error del pipeline son diagnóstico; no se cambiaron librerías ni políticas de seguridad para alterar el gate.

### Estado al cierre de sesión

- SHA remoto `372af0bacc0b577debbde3fc693e9bdbac7e1d2f`, base `f087e4b7cc185d93618de4bdeaeb76b53486ac47`; MERGEABLE / BLOCKED / REVIEW_REQUIRED. Worktree limpio, sin procesos locales de validación o espera pendientes.
- Checks observados del nuevo HEAD: continuous-integration=IN_PROGRESS, workflow=SUCCESS. La CI remota continúa por su cuenta; el informe no afirma que ya terminó ni que el PR está verde.
- AGENTS OS: continuidad del proyecto, SPEC, copia de descripción y agent_run actualizados; feedback [[2026-10-01-sig-616-f4-session-feedback]]. Lint estricto de las cinco notas canónicas editadas: cero errores/warnings.
- Consulta Graphify focalizada recuperó el archivo exacto del proyecto y actualizó el índice local. Advirtió deuda global fuera del delta; no bloqueó el refresh ni se modificaron notas ajenas a esta sesión.
- Sesión cerrada por petición explícita del owner; sin crear checkpoint privado duplicado ni promover la hipótesis del pipeline a un error conocido L3.
