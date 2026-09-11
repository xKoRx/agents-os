---
type: project
schema_version: 1
owner: me
root: true
status: archived
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-03
due:
progress: 0
repo:
  - fury_rio-materializer
  - fury_rio-entity-service
  - fury_rio-controlplane-clickhouse
  - fury_rio-controlplane-flink
  - fury_rio-controlplane-fury
  - fury_rio-controlplane-kafka
  - fury_rio-controlplane-kms
  - fury_rio-controlplane-observability
  - fury_rio-controlplane-signals
jira: SIGFOUN
prs:
aliases:
  - vulnes SIGFOUN
  - WebSec RIO
  - vulnerabilidades ads-signals-foundation
tags:
  - kind/project
  - area/meli
  - tech/rio
  - topic/security
created: "2026-09-03"
updated: "2026-09-11"
---

# Vulnerabilidades WebSec — RIO Foundation

%% Naming: Vulnerabilidades WebSec — RIO Foundation es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Vulnerabilidades WebSec — RIO Foundation
> **Área:** [[Meli]] · **Estado:** archived · **Prioridad:** P1 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Vulnerabilidades WebSec — RIO Foundation]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

Dejar en un solo lugar, listas y ya investigadas, las **23 vulnerabilidades WebSec (SIGFOUN-623 … SIGFOUN-645)** que el bot de Fran Salazar publicó el 2026-09-03 en el canal Slack `#ads-signals-foundation`, con evidencia verificada en cada repo, para que agentes las aborden por lotes de causa raíz en vez de ticket por ticket.

- **Fuente primaria:** canal Slack `#ads-signals-foundation` (`C08RWQ5P3TM`). Cada mensaje enlaza un ticket `SIGFOUN-N` en `mercadolibre.atlassian.net`.
- **Restricción conocida:** no hay acceso a Jira/SIGFOUN desde esta cuenta, así que **el CVE exacto y la "fixed version" oficial de cada ticket no están en esta nota**. Todo lo que sigue se derivó de los títulos de los tickets más inspección directa de los repos, los POM de `spring-boot-dependencies` y los `maven-metadata.xml` servidos por el Nexus de Fury, y el estado desplegado según `fury list-infra`. Existe un camino para cerrar ese hueco: ver **Accesos pendientes** más abajo.
- **Criterio de trabajo:** un PR por repo agrupando sus tickets, no un PR por ticket. Siete de las nueve apps comparten una sola causa raíz (la versión de Spring Framework que arrastra el plugin de Spring Boot).

## 📊 Estado actual

- **Archivado el 2026-09-11 por solicitud del owner.** El material se conserva como historial; no representa trabajo activo.

Recopilación cerrada e investigación técnica hecha. **Nada corregido todavía.** El siguiente paso es repartir los lotes a agentes.

### Inventario — publicadas hoy (2026-09-03)

23 tickets: 9 critical, 14 high, sobre 9 aplicaciones.

| Ticket | Sev | Dependencia | Aplicación | Hora |
|---|---|---|---|---|
| SIGFOUN-624 | critical | `org.springframework/spring-webmvc` | rio-controlplane-kafka | 11:34 |
| SIGFOUN-625 | critical | `org.springframework/spring-webmvc` | rio-controlplane-clickhouse | 11:34 |
| SIGFOUN-626 | critical | `org.springframework/spring-webmvc` | rio-entity-service | 11:36 |
| SIGFOUN-627 | critical | `org.springframework/spring-webmvc` | rio-controlplane-fury | 11:36 |
| SIGFOUN-628 | critical | `org.springframework/spring-webmvc` | rio-materializer | 11:40 |
| SIGFOUN-629 | critical | `org.springframework/spring-webmvc` | rio-controlplane-flink | 11:40 |
| SIGFOUN-630 | critical | `org.springframework/spring-webmvc` | rio-controlplane-observability | 11:40 |
| SIGFOUN-640 | critical | `org.apache.tomcat.embed/tomcat-embed-core` | rio-controlplane-flink | 13:51 |
| SIGFOUN-642 | critical | `org.apache.tomcat.embed/tomcat-embed-core` | rio-controlplane-signals | 14:05 |
| SIGFOUN-623 | high | `io.netty/netty-resolver-dns` | rio-materializer | 04:52 |
| SIGFOUN-631 | high | `io.micrometer/micrometer-core` | rio-controlplane-observability | 11:44 |
| SIGFOUN-632 | high | `io.micrometer/micrometer-core` | rio-controlplane-kms | 11:47 |
| SIGFOUN-633 | high | `org.springframework.retry/spring-retry` | rio-materializer | 13:40 |
| SIGFOUN-634 | high | `io.opentelemetry/opentelemetry-api` | rio-controlplane-clickhouse | 13:47 |
| SIGFOUN-635 | high | `io.opentelemetry/opentelemetry-api` | rio-controlplane-kafka | 13:47 |
| SIGFOUN-636 | high | `io.opentelemetry/opentelemetry-api` | rio-controlplane-signals | 13:48 |
| SIGFOUN-637 | high | `org.apache.tomcat.embed/tomcat-embed-core` | rio-controlplane-flink | 13:48 |
| SIGFOUN-638 | high | `io.opentelemetry/opentelemetry-api` | rio-controlplane-flink | 13:49 |
| SIGFOUN-639 | high | `io.opentelemetry/opentelemetry-api` | rio-controlplane-observability | 13:49 |
| SIGFOUN-641 | high | `org.apache.tomcat.embed/tomcat-embed-core` | rio-controlplane-signals | 13:53 |
| SIGFOUN-643 | high | `org.springframework.security/spring-security-core` | rio-entity-service | 18:10 |
| SIGFOUN-644 | high | `org.springframework.security/spring-security-crypto` | rio-controlplane-flink | 18:12 |
| SIGFOUN-645 | high | `org.springframework.security/spring-security-crypto` | rio-entity-service | 18:12 |

**Concentración por app:** flink 5 · observability 3 · entity-service 3 · materializer 3 · signals 3 · clickhouse 2 · kafka 2 · kms 1 · controlplane-fury 1.

**Concentración por dependencia:** spring-webmvc 7 · opentelemetry-api 5 · tomcat-embed-core 4 · spring-security-* 3 · micrometer-core 2 · netty-resolver-dns 1 · spring-retry 1.

### Estado técnico verificado por repo

Versión del plugin `org.springframework.boot` leída de `origin/develop`, versión desplegada leída de `fury list-infra` (scope productivo).

| App | Boot en `develop` | Pins propios relevantes | Versión en prod | Tickets de hoy |
|---|---|---|---|---|
| rio-materializer | 3.5.6 | `io.netty` → 4.2.7.Final · `spring-retry` → 2.0.13 · `logback` → 1.5.36 · otel-bom 1.25.0 | `production` 202608.4.0-rc-2 (Boot 3.5.6) | 623, 628, 633 |
| rio-entity-service | 3.5.12 | `spring-boot-starter-security` directo | `prod-nonsite` 0.1.0-rc-1 (Boot 3.5.7) | 626, 643, 645 |
| rio-controlplane-fury | 3.5.7 | melitk-bom 2.2.1 | `prod-nonsite` 202605.26.0 (Boot 3.5.7) | 627 |
| rio-controlplane-kafka | 3.5.16 | otel-api 1.48.0 | `production` 1.2.0 (Boot 3.5.7, otel 1.48.0) | 624, 635 |
| rio-controlplane-clickhouse | 3.5.16 | otel-api 1.62.0 | `prod` 202608.11.0-rc-1 · `prod-nonsite` 2026.8.31-rc-1 | 625, 634 |
| rio-controlplane-flink | 3.5.16 | `tomcat.embed` → 10.1.56 · `grpc-netty-shaded` → 1.75.0 · otel-api 1.62.0 | `production` 202608.28.0-rc-1 | 629, 637, 638, 640, 644 |
| rio-controlplane-observability | 4.1.1 | force netty 4.1.122.Final (7 módulos, **sin** `netty-resolver-dns`) · otel-api 1.62.0 | `prod` 202608.32.0-rc-1 | 630, 631, 639 |
| rio-controlplane-signals | 3.5.16 | otel-api 1.48.0 | `production-nonsite` 202608.28.1 | 636, 641, 642 |
| rio-controlplane-kms | 3.5.16 | otel-api **1.65.0** · `grpc-netty-shaded` 1.75.0 | `prod` 202609.1.1-rc-1 | 632 |

### Versiones gestionadas por el BOM de Spring Boot

Extraídas de los POM en la caché local de Gradle (`~/.gradle/caches/modules-2`). Es lo que resuelve cada app salvo pin explícito.

| Boot | spring-framework | tomcat | spring-security | micrometer | netty | spring-retry |
|---|---|---|---|---|---|---|
| 3.5.6 | 6.2.11 | 10.1.46 | 6.5.5 | 1.15.4 | 4.1.127.Final | 2.0.12 |
| 3.5.7 | 6.2.12 | 10.1.48 | 6.5.6 | 1.15.5 | 4.1.128.Final | 2.0.12 |
| 3.5.12 | 6.2.17 | 10.1.52 | 6.5.9 | 1.15.10 | 4.1.131.Final | 2.0.12 |
| 3.5.16 | 6.2.19 | 10.1.55 | 6.5.11 | 1.15.12 | 4.1.135.Final | 2.0.13 |
| 4.1.1 | 7.0.9 | 11.0.24 | 7.1.1 | 1.17.1 | 4.2.17.Final | — |

**3.5.16 es el tope de la línea 3.5 y 4.1.1 el tope de la 4.1**; no hay nada más arriba en ninguna de las dos.

### Techo real de cada dependencia

Última versión publicada en el Nexus de Fury. Define hasta dónde se puede subir sin cambiar de línea.

| Dependencia | Última publicada | Dónde está hoy el parque | ¿Hay margen? |
|---|---|---|---|
| `opentelemetry-api` | **1.65.0** | kms 1.65.0 · clickhouse/flink/observability 1.62.0 · kafka/signals 1.48.0 · materializer 1.25.0 (bom) | Sí — subir todas a 1.65.0 |
| `netty-resolver-dns` | **4.2.17.Final** | materializer forzado a 4.2.7.Final · observability lo deja en 4.2.17 vía Boot 4.1.1 | Sí — 10 parches de margen en materializer |
| `tomcat-embed-core` | **10.1.59** (línea 10.1) | flink forzado a 10.1.56 · signals hereda 10.1.55 | Sí — pero ver hallazgo 2 |
| `spring-webmvc` | **6.2.19** (línea 6.2) | las apps en Boot 3.5.16 ya están en 6.2.19 | **No** en la línea 6.2 |
| `spring-security-core` | 6.5.11 vía Boot 3.5.16 · 7.1.1 vía Boot 4.1.1 | entity-service 6.5.9 · flink 6.5.11 | Sí sólo para entity-service |
| `micrometer-core` | **1.17.1** (release; 1.18.0-M1 es milestone) | observability 1.17.1 · kms 1.15.12 | **No** para observability |
| `spring-retry` | **2.0.13** | materializer ya forzado a 2.0.13 | **No** |

### Hallazgos de la investigación

1. **El scan corre sobre el artefacto desplegado, no sobre `develop`.** rio-controlplane-clickhouse y rio-controlplane-flink ya están en Boot 3.5.16 (Framework 6.2.19, el tope de la línea) en `develop` y aun así recibieron el critical de `spring-webmvc`; rio-controlplane-kms, cuyo prod es del 2026-09-01 y usa otel-api 1.65.0, es la única app con otel que **no** recibió ticket. Consecuencia práctica: para varios tickets el arreglo no es tocar código sino **cortar release y desplegar**. Antes de abrir cualquier PR hay que comparar `develop` contra el tag desplegado.
2. **`tomcat-embed-core` entra transitivo en servicios que corren Jetty.** Las nueve apps hacen `exclude module: 'spring-boot-starter-tomcat'` y usan `spring-boot-starter-jetty`, pero Tomcat sigue en el classpath: flink incluso lo fuerza a 10.1.56. El patrón se repite desde junio (SIGFOUN-579, SIGFOUN-586 en flink, ahora 637/640/642). Perseguir la versión cada mes es tratar el síntoma; si nada lo carga en runtime, el arreglo de fondo es un `exclude group: 'org.apache.tomcat.embed'` global. Hay que verificar primero que ningún `ServletWebServerFactory` de Tomcat se resuelva en arranque.
3. **Tres tickets no tienen versión a la cual subir.** `spring-retry` está publicado hasta **2.0.13** y materializer ya fuerza exactamente esa versión, en `develop` y en el tag desplegado `202608.4.0-rc-2` (SIGFOUN-633). `micrometer-core` está publicado hasta **1.17.1** como release y observability ya corre esa versión vía Boot 4.1.1 (SIGFOUN-631). En los tres casos el bump es imposible: o WebSec está leyendo la versión que declara el BOM en vez de la resuelta, o todavía no hay release con el fix. Estos tickets se resuelven **leyendo el ticket y respondiendo por el campo `solución`**, no con un PR.
4. **`opentelemetry-api`: el objetivo es 1.65.0, y está confirmado.** 1.65.0 es la última publicada y es exactamente la que usa kms, la única app con otel que no recibió ticket. Recibieron ticket las que están en 1.48.0 (kafka, signals) y en 1.62.0 (clickhouse, flink, observability). Queda un contraejemplo sin explicar: rio-materializer declara `opentelemetry-bom:1.25.0` y hoy no recibió ticket de otel — lo más probable es que su artefacto productivo, de agosto, no exponga la clase afectada, pero no está verificado.
5. **`spring-webmvc` critical es una sola causa raíz repartida en 7 apps, y media parte ya está resuelta en código.** Ninguna app fija Spring Framework a mano: todas lo heredan del plugin de Boot. Como 6.2.19 es el tope de la línea 6.2 y lo trae Boot 3.5.16, las apps que ya están ahí (clickhouse, flink, kafka) **no tienen nada que subir**: su fix es liberar. Las que faltan son materializer (Boot 3.5.6 → 6.2.11), controlplane-fury (3.5.7 → 6.2.12) y entity-service (3.5.12 → 6.2.17).
6. **`netty-resolver-dns` en materializer no está cubierto por sus propios forces.** materializer fuerza todo `io.netty` a 4.2.7.Final y ya hay 4.2.17.Final publicada: diez parches de atraso, incluido el módulo del ticket.
7. **rio-controlplane-observability está degradando netty con su propio `force`.** El repo fuerza siete módulos (`netty-codec-http`, `netty-codec-http2`, `netty-handler`, `netty-common`, `netty-buffer`, `netty-transport`, `netty-resolver`) a `4.1.122.Final` con el comentario "o superior", pero `force` en Gradle fija la versión exacta: bajo Boot 4.1.1, que gestiona **4.2.17.Final**, ese bloque las **baja** una línea completa. `netty-resolver-dns` no está en la lista, así que queda en 4.2.17.Final y el classpath termina con netty partido entre 4.1.122 y 4.2.17. Es a la vez una regresión de seguridad y un riesgo de incompatibilidad binaria; el bloque quedó obsoleto cuando se subió a Boot 4.1.1 y hay que borrarlo.

### Accesos pendientes

- **`oraculo-websec-mcp`** (`https://oracle-websec-mcp-mcp.melioffice.com/mcp`) es el MCP de WebSec y sería la vía para leer CVE, versión segura y estado de cada ticket sin pasar por Jira. Con la VPN corporativa arriba la autenticación pasa (`x-fury-user: rjara`) pero la autorización rechaza con `OFFSEC-AUT-6 / NO_ACCESS_GROUP_MATCHED`: falta el access group **`mcp_consumer_bu_all`**, que se pide por autoservicio en MeliHelp (`access-management/new-request`, application `traffic-catalog`, resource `mcp_consumer_bu_all`, permisos read+write). **Este es el desbloqueo de mayor impacto del proyecto.**
- El endpoint `mcp.melioffice.com/namespaces/application-security/mcp` que aparece en las guías de setup **ya no existe**: ese host resuelve hoy a `documentation-mcp-server-py` y devuelve 404 en todos sus namespaces. No insistir por ahí.

### Backlog previo del canal (parcial, anterior a hoy)

Rescatado del histórico de `#ads-signals-foundation`. **Estado real desconocido** — sin Jira no se sabe cuáles siguen abiertos. La búsqueda devolvió sólo la primera página, así que la lista está incompleta.

| Ticket | Sev | Dependencia | Aplicación | Fecha |
|---|---|---|---|---|
| SIGFOUN-620 | high | `io.micrometer/micrometer-core` | rio-materializer | 2026-09-01 |
| SIGFOUN-611 | — | `io.netty/netty-codec-http2` | rio-materializer | 2026-08-10 |
| SIGFOUN-604 | high | `ch.qos.logback/logback-core` | rio-materializer | 2026-07-22 |
| SIGFOUN-603 | high | `ch.qos.logback/logback-core` | rio-controlplane-flink | 2026-07-22 |
| SIGFOUN-602 | critical | `golang.org/x/crypto` | rio-copilot | 2026-07-22 |
| SIGFOUN-601 | high | `golang.org/x/crypto` | rio-copilot | 2026-07-22 |
| SIGFOUN-587 | high | `github.com/go-jose/go-jose/v3` | rio-copilot | 2026-06-29 |
| SIGFOUN-586 | critical | `org.apache.tomcat.embed/tomcat-embed-core` | rio-controlplane-flink | 2026-06-23 |
| SIGFOUN-585 | high | `org.asynchttpclient/async-http-client` | rio-controlplane-flink | 2026-06-19 |
| SIGFOUN-584 | high | `org.bouncycastle/bcprov-jdk18on` | rio-controlplane-flink | 2026-06-19 |
| SIGFOUN-583 | high | `go.opentelemetry.io/otel` | rio-copilot | 2026-06-19 |
| SIGFOUN-579 | high | `org.apache.tomcat.embed/tomcat-embed-core` | rio-controlplane-flink | 2026-06-12 |
| SIGFOUN-559 | high | `org.springframework.boot/spring-boot-autoconfigure` | rio-controlplane-observability | 2026-06-01 |
| SIGFOUN-558 | high | `org.springframework.boot/spring-boot-actuator-autoconfigure` | rio-controlplane-observability | 2026-06-01 |
| SIGFOUN-557 | high | `org.springframework.boot/spring-boot-actuator` | rio-controlplane-observability | 2026-06-01 |
| SIGFOUN-539 | high | `org.asynchttpclient/async-http-client` | rio-controlplane-clickhouse | 2026-05-18 |
| SIGFOUN-502 | high | `org.apache.kafka/kafka-clients` | rio-materializer | 2026-04-16 |
| SIGFOUN-501 | high | `org.apache.kafka/kafka-clients` | rio-controlplane-kafka | 2026-04-16 |

### Flujo WebSec para cerrar un ticket

Del asistente virtual de `#tech-websec`: una vez corregida la vulnerabilidad hay que **transicionar el ticket a `Pending` y completar el campo `solución`** con el motivo. Desde `Pending` se detiene el SLA del lado del equipo responsable y el ticket queda en validación. Si la validación determina que no quedó bien resuelta, vuelve a `In Progress`. Hay SLA interno de validación según severidad, así que no conviene resolver pegado a la fecha de vencimiento.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

**La unidad de trabajo es la aplicación: una tarea por repo, un PR por repo.** La tabla de lotes que sigue es una lectura transversal por causa raíz, útil para ver qué se repite y para no resolver dos veces el mismo problema — no es el reparto de trabajo.

| Lote | Tickets | Causa raíz | Acción, con versión objetivo |
|---|---|---|---|
| **A — spring-webmvc critical** | 624, 625, 626, 627, 628, 629, 630 | Versión de Spring Framework heredada del plugin de Boot | Subir Boot a **3.5.16** (Framework 6.2.19, tope de la línea) en materializer (3.5.6), controlplane-fury (3.5.7) y entity-service (3.5.12). clickhouse, flink y kafka ya están en 3.5.16 en `develop`: **sólo liberar**. observability ya está en Boot 4.1.1 (Framework 7.0.9): confirmar que el desplegado lo incluye. |
| **B — tomcat-embed-core** | 637, 640, 641, 642 | Tomcat transitivo en apps que corren Jetty | Camino corto: subir a **10.1.59** (flink está en 10.1.56, signals hereda 10.1.55). Camino de fondo, preferible: `exclude group: 'org.apache.tomcat.embed'` global, previa verificación de que nada lo carga en runtime. |
| **C — opentelemetry-api** | 634, 635, 636, 638, 639 | Pin explícito desactualizado (1.48.0 / 1.62.0) | Alinear a **1.65.0** en clickhouse, kafka, signals, flink y observability. Objetivo confirmado: es la última publicada y la que ya pasó el scan en kms. |
| **D — spring-security-\*** | 643, 644, 645 | Versión gestionada por el BOM de Boot | entity-service Boot 3.5.12 → 3.5.16 (security 6.5.9 → **6.5.11**); flink ya está en 6.5.11, verificar el desplegado. Se resuelve con el mismo PR del lote A. |
| **E — sin versión a la cual subir** | 631, 633 | El parque ya está en la última versión publicada | `micrometer-core` 1.17.1 en observability y `spring-retry` 2.0.13 en materializer son los topes publicados. No hay PR posible: hay que leer el ticket y responder por el campo `solución`. |
| **F — netty** | 623 | Force de `io.netty` a 4.2.7.Final quedó diez parches atrás | materializer: subir el force a **4.2.17.Final**. Aparte y sin ticket asociado, borrar el bloque de forces netty de observability, que bajo Boot 4.1.1 degrada siete módulos de 4.2.17.Final a 4.1.122.Final (hallazgo 7). |
| **G — micrometer kms** | 632 | kms está en 1.15.12 vía Boot 3.5.16 | Subir cruza de línea (1.16.7 o 1.17.1) y por lo tanto sale del BOM de Boot 3.5.16. **Bloqueado** hasta saber del ticket cuál es la versión segura. |

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| fury_rio-materializer | — | develop | _no aplica (fix de dependencias)_ | _no aplica_ | Pendiente — lote A (Boot 3.5.6 → 3.5.16) y lote F (netty → 4.2.17.Final); ticket 633 sin bump posible |
| fury_rio-entity-service | — | develop | _no aplica_ | _no aplica_ | Pendiente — lotes A + D en un solo PR (Boot 3.5.12 → 3.5.16) |
| fury_rio-controlplane-fury | — | develop | _no aplica_ | _no aplica_ | Pendiente — lote A (Boot 3.5.7 → 3.5.16) |
| fury_rio-controlplane-kafka | — | develop | _no aplica_ | _no aplica_ | Pendiente — lote C (otel 1.48.0 → 1.65.0); lote A es sólo release |
| fury_rio-controlplane-clickhouse | — | develop | _no aplica_ | _no aplica_ | Pendiente — lote C (otel 1.62.0 → 1.65.0); lote A es sólo release |
| fury_rio-controlplane-flink | — | develop | _no aplica_ | _no aplica_ | Pendiente — lotes B y C (otel 1.62.0 → 1.65.0); lotes A y D son sólo release |
| fury_rio-controlplane-signals | — | develop | _no aplica_ | _no aplica_ | Pendiente — lotes B y C (otel 1.48.0 → 1.65.0) |
| fury_rio-controlplane-observability | — | develop | _no aplica_ | _no aplica_ | Pendiente — lote C (otel 1.62.0 → 1.65.0) y borrar el bloque de forces netty (hallazgo 7); ticket 631 sin bump posible |
| fury_rio-controlplane-kms | — | develop | _no aplica_ | _no aplica_ | Bloqueado — lote G |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [ ] **rio-controlplane-flink** — 5 vulnes: SIGFOUN-629, 637, 638, 640, 644 #owner/agent #type/dev #area/meli #urgent
>   - SIGFOUN-629 `spring-webmvc` critical y SIGFOUN-644 `spring-security-crypto`: `develop` ya está en Boot 3.5.16 (Framework 6.2.19, security 6.5.11), no hay bump — verificar contra el tag desplegado `202608.28.0-rc-1` y liberar.
>   - SIGFOUN-640 critical y SIGFOUN-637 high `tomcat-embed-core`: hoy forzado a 10.1.56; subir a 10.1.59 o, mejor, excluir `org.apache.tomcat.embed` del classpath — la app corre Jetty y el ticket se repite desde junio.
>   - SIGFOUN-638 `opentelemetry-api`: pin 1.62.0 → 1.65.0.
> - [ ] **rio-controlplane-observability** — 3 vulnes + 1 bug de dependencias #owner/agent #type/dev #area/meli #urgent
>   - SIGFOUN-630 `spring-webmvc` critical: `develop` ya está en Boot 4.1.1 (Framework 7.0.9); verificar que el desplegado `202608.32.0-rc-1` lo incluya y liberar.
>   - SIGFOUN-639 `opentelemetry-api`: pin 1.62.0 → 1.65.0.
>   - SIGFOUN-631 `micrometer-core`: ya corre 1.17.1, que es la última publicada. Sin bump posible — responder el ticket por el campo `solución`.
>   - Sin ticket asociado: borrar el bloque de `force` de netty, que bajo Boot 4.1.1 baja siete módulos de 4.2.17.Final a 4.1.122.Final y deja el classpath partido.
> - [ ] **rio-entity-service** — 3 vulnes: SIGFOUN-626, 643, 645 #owner/agent #type/dev #area/meli #urgent
>   - Las tres se resuelven con el mismo cambio: Boot 3.5.12 → 3.5.16, que sube Framework 6.2.17 → 6.2.19 (SIGFOUN-626 critical) y spring-security 6.5.9 → 6.5.11 (SIGFOUN-643 y SIGFOUN-645).
> - [ ] **rio-materializer** — 3 vulnes: SIGFOUN-623, 628, 633 #owner/agent #type/dev #area/meli #urgent
>   - SIGFOUN-628 `spring-webmvc` critical: Boot 3.5.6 → 3.5.16 (Framework 6.2.11 → 6.2.19). Es el repo más atrasado del parque.
>   - SIGFOUN-623 `netty-resolver-dns`: el `force` de `io.netty` está en 4.2.7.Final y ya hay 4.2.17.Final — subirlo.
>   - SIGFOUN-633 `spring-retry`: ya forzado a 2.0.13, que es la última publicada. Sin bump posible — responder el ticket por el campo `solución`.
> - [ ] **rio-controlplane-signals** — 3 vulnes: SIGFOUN-636, 641, 642 #owner/agent #type/dev #area/meli #urgent
>   - SIGFOUN-642 critical y SIGFOUN-641 high `tomcat-embed-core`: hereda 10.1.55 de Boot 3.5.16; misma decisión que flink, subir a 10.1.59 o excluir el grupo.
>   - SIGFOUN-636 `opentelemetry-api`: pin 1.48.0 → 1.65.0.
> - [ ] **rio-controlplane-clickhouse** — 2 vulnes: SIGFOUN-625, 634 #owner/agent #type/dev #area/meli
>   - SIGFOUN-625 `spring-webmvc` critical: `develop` ya está en Boot 3.5.16, no hay bump — verificar y liberar.
>   - SIGFOUN-634 `opentelemetry-api`: pin 1.62.0 → 1.65.0.
> - [ ] **rio-controlplane-kafka** — 2 vulnes: SIGFOUN-624, 635 #owner/agent #type/dev #area/meli
>   - SIGFOUN-624 `spring-webmvc` critical: `develop` ya está en Boot 3.5.16 mientras prod corre `1.2.0` con Boot 3.5.7 — verificar y liberar.
>   - SIGFOUN-635 `opentelemetry-api`: pin 1.48.0 → 1.65.0.
> - [ ] **rio-controlplane-fury** — 1 vuln: SIGFOUN-627 #owner/agent #type/dev #area/meli
>   - `spring-webmvc` critical: Boot 3.5.7 → 3.5.16 (Framework 6.2.12 → 6.2.19).
> - [ ] **rio-controlplane-kms** — 1 vuln: SIGFOUN-632 #owner/agent #type/dev #area/meli #blocked
>   - `micrometer-core`: corre 1.15.12 vía Boot 3.5.16. Subir cruza de línea (1.16.7 o 1.17.1) y sale del BOM. Bloqueado hasta conocer la versión segura del ticket.
> - [ ] Pedir el access group `mcp_consumer_bu_all` en MeliHelp para desbloquear `oraculo-websec-mcp` y leer CVE y versión segura por ticket #owner/me #type/admin #area/meli #urgent
> - [ ] Confirmar con el equipo que el scan de WebSec corre sobre el artefacto desplegado y no sobre `develop` #owner/me #type/research #area/meli
> - [ ] Barrer el backlog previo del canal para saber qué sigue abierto #owner/me #type/research #area/meli

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-03 (2)** — Con la VPN corporativa arriba se cerraron los huecos verificables contra el Nexus de Fury: versiones gestionadas de Boot 3.5.12 y 4.1.1, y el techo publicado de cada dependencia. Tres conclusiones cambian el plan: `spring-webmvc` no tiene margen sobre la línea 6.2 (6.2.19 ya es el tope, lo trae Boot 3.5.16), `spring-retry` y `micrometer-core` no tienen versión a la cual subir en las apps que los reportan, y observability está degradando netty con su propio bloque de forces. `oraculo-websec-mcp` daría el detalle de cada ticket y sólo falta pedir el access group.
- **2026-09-03** — Recopiladas las 23 vulnes publicadas hoy por el bot de Fran en `#ads-signals-foundation` (SIGFOUN-623…645) e investigadas contra el estado real de los 9 repos, los BOM de Boot y los scopes desplegados. Agrupadas en 6 lotes por causa raíz. Sin acceso a Jira: falta el CVE y la versión segura oficial de cada ticket.

## 🧭 Decisiones

- **Trabajar por causa raíz, no por ticket.** 23 tickets colapsan en 6 lotes y 7 de ellos son la misma versión de Spring Framework. Un PR por repo, no uno por ticket.
- **Verificar `develop` contra el tag desplegado antes de tocar código.** Para varias apps el arreglo es cortar release, no cambiar dependencias; abrir un PR sin comprobarlo es trabajo perdido.
- **Este proyecto es de cambio, no de comprensión.** El entendimiento de RIO vive en [[Onboarding Signals]]; acá sólo entra lo que se necesita para corregir las vulnes.
- **Antes de abrir un PR, verificar que exista versión a la cual subir.** Tres de los 23 tickets caen sobre dependencias que ya están en su última versión publicada; ahí el entregable es una respuesta en el ticket, no código.
- **No se inventan CVEs.** Los títulos de los tickets sólo dan dependencia, severidad y app. Todo lo que dice esta nota sobre versiones sale de los repos y de los BOM en caché; lo que no se pudo verificar queda marcado como hipótesis o bloqueado.

## 🔗 Docs / Links

- Canal Slack fuente: `#ads-signals-foundation` (`C08RWQ5P3TM`) — el bot publica un mensaje por ticket creado.
- Canal de soporte WebSec: `#tech-websec` — ahí se piden extensiones de plazo y se resuelven dudas de flujo.
- Tickets: `https://mercadolibre.atlassian.net/browse/SIGFOUN-<n>` (sin acceso desde esta cuenta).
- Proyecto relacionado: [[Onboarding Signals]] · [[Estandarización de Scopes RIO]].
- Change log de la recopilación: [[2026-09-03-sigfoun-websec-vuln-intake-rio-foundation]].

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- 

### Motivos / principios

- 

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** [[2026-09-03-vulnes-signals-no-salen-por-fury-cli]] (dónde viven realmente las vulnes del equipo y por qué Fury no las tiene) · [[resolver-versiones-java-sin-construir-via-fury-nexus]] (cómo saber qué versión resuelve un build sin construirlo) · [[gradle-force-fija-exacto-y-puede-degradar]] (por qué un pin de seguridad caduca).
- **Memoria interna:** ninguna. La continuidad de este proyecto vive en esta nota; no hay estado privado del agente que justifique un checkpoint aparte.
- **Motivo:** las tres son conocimiento reusable fuera de este proyecto —sirven en cualquier repo Java de Meli y en cualquier triage de vulnerabilidades del equipo—, así que no pertenecen al cuerpo del proyecto sino a Sistema 1. 
