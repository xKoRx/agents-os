---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Meli]]"
project: "[[Vulnerabilidades WebSec — RIO Foundation]]"
application:
entities:
  - "[[RIO]]"
related:
  - "[[Onboarding Signals]]"
  - "[[2026-09-03-vulnes-signals-no-salen-por-fury-cli]]"
  - "[[resolver-versiones-java-sin-construir-via-fury-nexus]]"
  - "[[gradle-force-fija-exacto-y-puede-degradar]]"
  - "[[2026-09-03-websec-vuln-intake-session-feedback]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-03-sigfoun-websec-vuln-intake-rio-foundation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - [[Vulnerabilidades WebSec — RIO Foundation]] (proyecto nuevo bajo `10-projects/Meli/`)
  - [[2026-09-03-vulnes-signals-no-salen-por-fury-cli]], [[resolver-versiones-java-sin-construir-via-fury-nexus]] y [[gradle-force-fija-exacto-y-puede-degradar]] (memoria pública nueva)
  - Clon nuevo de `fury_rio-entity-service` en el workspace externo de repos (fuera de `VAULT_ROOT`)

## Motivo

- El 2026-09-03 el bot de WebSec publicó 23 vulnerabilidades nuevas (SIGFOUN-623…645) sobre 9 aplicaciones de RIO en el canal Slack del equipo. Sin acceso a Jira no había forma de verlas juntas ni de repartirlas, y el volumen hace inviable atacarlas ticket por ticket.

## Fuentes usadas

- Nexus de Fury (`maven.artifacts.furycloud.io/repository/all`), accesible con la VPN corporativa: POM de `spring-boot-dependencies` 3.5.12 y 4.1.1, y `maven-metadata.xml` de cada dependencia reportada para conocer el techo publicado.
- Canal Slack `#ads-signals-foundation` (`C08RWQ5P3TM`): un mensaje por ticket creado, con dependencia, severidad, aplicación y enlace a `SIGFOUN-N`. Histórico del canal para el backlog anterior (primera página de resultados, incompleto).
- Fury CLI 5.21.0: `fury -a <app> list-infra` para la versión desplegada por scope en las 9 aplicaciones.
- `origin/develop` y tags de release de los 9 repos: versión del plugin `org.springframework.boot`, `java-melitk-bom`, pins de `opentelemetry-api` y bloques `resolutionStrategy`.
- POM de `spring-boot-dependencies` 3.5.6, 3.5.7 y 3.5.16 desde la caché local de Gradle, para las versiones gestionadas de framework, tomcat, security, micrometer, netty y retry.

## Resolución aplicada

- Se identificó que `ads-signals-foundation` no es una aplicación ni un proyecto de Fury sino el canal Slack del equipo, y que las vulnes son tickets Jira del proyecto `SIGFOUN`. Ni `fury actionables`, ni GitHub Code Scanning, ni Dependabot exponen estos hallazgos: los actionables de Fury son rightsizing y migraciones, code scanning devuelve vacío y Dependabot está deshabilitado en los repos.
- Se creó el proyecto con el inventario completo de los 23 tickets del día (9 critical, 14 high), la concentración por aplicación y por dependencia, y el backlog previo rescatado del canal marcado explícitamente como parcial y de estado desconocido.
- Se contrastó cada ticket contra el estado real del repo: versión de Boot en `develop`, pins propios, versión desplegada en el scope productivo y versiones que gestiona el BOM correspondiente.
- Los 23 tickets se colapsaron en 6 lotes por causa raíz. Siete de los nueve critical son la misma versión de Spring Framework heredada del plugin de Boot.
- Segunda pasada con la VPN corporativa conectada: se completaron las versiones gestionadas de Boot 3.5.12 y 4.1.1 y se levantó el techo publicado de cada dependencia reportada. Tres conclusiones cambiaron el plan de remediación: `spring-webmvc` no tiene margen sobre la línea 6.2 porque 6.2.19 ya es el tope y lo trae Boot 3.5.16, de modo que la mitad del lote crítico se resuelve liberando; `spring-retry` (2.0.13) y `micrometer-core` (1.17.1) ya están en su última versión publicada en las apps que los reportan, así que SIGFOUN-633 y SIGFOUN-631 no admiten PR y se cierran respondiendo el ticket; y rio-controlplane-observability degrada siete módulos de netty de 4.2.17.Final a 4.1.122.Final con un bloque de forces que quedó obsoleto al subir a Boot 4.1.1.
- Se documentó el desbloqueo pendiente: `oraculo-websec-mcp` responde con la VPN arriba y autentica correctamente al usuario, pero rechaza por falta del access group `mcp_consumer_bu_all`, que se pide por autoservicio. El endpoint `mcp.melioffice.com/namespaces/application-security` de las guías de setup está obsoleto: ese host resuelve a `documentation-mcp-server-py` y devuelve 404 en todos sus namespaces.
- Tercera pasada: el reparto de trabajo se reorganizó por aplicación en vez de por lote. Quedaron 12 tareas — nueve de desarrollo, una por repo, con sus vulnes como puntos internos, más tres de acceso e investigación — y los 23 tickets están cubiertos sin quedar ninguno suelto. La tabla de lotes por causa raíz se conservó degradada a lectura transversal, para ver qué se repite sin volver a ser el reparto.
- Se destiló la sesión en tres notas de memoria pública: el known error de dónde viven realmente las vulnerabilidades del equipo, el runbook para resolver versiones Java sin construir el proyecto, y el aprendizaje sobre `force` de Gradle fijando exacto y degradando.
- Se dejó registrado que el scan corre sobre el artefacto desplegado y no sobre `develop`, con la evidencia que lo sostiene, porque cambia la acción esperada: para varias apps el arreglo es cortar release, no modificar dependencias.

## Validación

- `materialize_schema_note.py` creó la nota desde `70-templates/project.md`; `validate_schema_contract.py --type project` devuelve `errors=0`.
- Inventario cuadrado por doble conteo: 9 critical + 14 high = 23, y la suma por aplicación (5+3+3+3+3+2+2+1+1) da los mismos 23.
- Versiones gestionadas del BOM leídas directamente de los POM en caché, no de memoria. Boot 3.5.12 y 4.1.1 no estaban en caché y quedaron marcados como pendientes de confirmar en vez de completados por inferencia.
- Techos de versión leídos de `maven-metadata.xml` en el Nexus, no de memoria; las versiones gestionadas de Boot 3.5.12 y 4.1.1 salieron de sus POM y confirman el comentario que ya existía en `build.gradle` de observability.
- Lint dirigido PASS sobre las cinco notas escritas en esta sesión. El rebuild global de Graphify quedó bloqueado por 28 errores y 6 warnings de frontmatter **preexistentes en notas ajenas** (concentrados en `memory/public/decision/symphony/` y en las skills `signals-*-spec-authoring`); se conserva el último índice válido y el índice queda `stale`. No se tocó esa deuda por estar fuera de alcance; queda registrada en [[2026-09-03-websec-vuln-intake-session-feedback]].
- Sin acceso a Jira ni al MCP de WebSec: el CVE y la versión segura oficial de cada ticket **no** están en la nota y quedan como bloqueo declarado, ahora con una ruta concreta para levantarlo.
- Trabajo read-only sobre los repos salvo `git fetch` y el clon nuevo de `fury_rio-entity-service`; ningún archivo de trabajo del usuario fue alterado.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar la carpeta del proyecto en `10-projects/Meli/` y este log. El clon de `fury_rio-entity-service` puede eliminarse del workspace de repos sin efecto sobre nada más.

