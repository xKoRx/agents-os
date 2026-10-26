---
type: project
schema_version: 1
owner: me
root: false
status: active
priority: P2
area: "[[Meli]]"
parent: "[[Sunsets backends RIO]]"
sprint:
start:
due:
progress: 80
repo: https://github.com/melisource/fury_rio-materializer
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/meli
created: "2026-10-22"
updated: "2026-10-22"
---

# Sunsets rio-materializer

## 🎯 Objetivo

Atender las cinco dependencias informadas por Rodrigo el 2026-10-22 usando [[30-resources/agents/skills/rio-sunset-update/SKILL|rio-sunset-update]]. Horizonte explícito: todos los sunsets abiertos informados, hasta el 2026-11-19 local (2026-11-20T00:00:00Z). Zona: America/Santiago (UTC−03).

## 📊 Estado actual

Código completo en PR [#738](https://github.com/melisource/fury_rio-materializer/pull/738), head d2d0f8b3dfa607fecc1743129e63e449cc7c7749. 1.825 tests pasan; build 202610.9.0-feat-rio-sunset-u.1 FINISHED, gate SHA aceptado y catálogo completo de 349 dependencias sin sunsets. Scopes test/api-test activados por autorización humana; gates aceptados. Test llegó a effective y se solicitó Finish, pero pipeline 533333 quedó alerted al 33%, deployment 38929535 en finishing al último chequeo. api-test no iniciado. Resultado STOPPED, requiere revisión humana de la alerta antes de continuar.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-materializer]] | feature/rio-sunset-update-rio-materializer | develop @ 216c0e54 | [[Sunsets rio-materializer#SPEC funcional]] | [[Sunsets rio-materializer#SPEC técnica]] | Build FINISHED; catálogo sin sunsets; deploy pendiente |

## SPEC funcional

Resolver los sunsets de Jackson core/databind (31/10 local), NoSQL (02/11 local), LZ4 (06/11 local) y Vert.x (19/11 local). Entregar un único PR con cambios seguros y validación efectiva. Deploy exclusivo a test tras selección de scope y confirmación; producción y stage requieren intervención humana.

## SPEC técnica

Actualizar `java-toolkit-nosql:0.2.1` a `0.2.6`. Proponer pins exactos de `jackson-core`/`jackson-databind:2.21.7` y `vertx-core:4.5.35` mediante el idioma existente `resolutionStrategy.eachDependency`, sin cambiar Spring Boot 4.0.8 ni java-melitk-bom 2.2.2. Conservar el pin existente `lz4-java:1.11.4`. Confirmar con dependencyInsight/runtimeClasspath, ejecutar build/tests del wrapper Gradle 9.4.0 con Java 21, y crear un build Fury de prueba ligado al SHA del PR.

## ✅ Tareas

- [x] Sincronizar skill y verificar sus tests. #owner/agent #type/dev #area/meli
- [x] Discovery paginado, contraste de conteos, PRs/builds en curso y existencia de objetivos. #owner/agent #type/research #area/meli
- [x] Validar resolución y aplicar NoSQL 0.2.6. #owner/agent #type/dev #area/meli
- [x] Validar build/tests y versiones efectivas de NoSQL/LZ4. #owner/agent #type/dev #area/meli
- [x] PR #738 actualizado y build Fury final ligado al SHA aceptado. #owner/agent #type/dev #area/meli
- [ ] Seleccionar/confirmar scope, desplegar test y Finish; reportar pendientes productivos/stage. #owner/me #type/dev #area/meli

- [x] Pins Jackson/Vert.x aprobados, aplicados y verificados en el catálogo nuevo. #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-10-22** — Test desplegó la versión corregida: pipeline 533333 / deployment 38929535. Deployment alcanzó effective, application_up=1, containers_started=1, failed_instances=0, swappedIn=100. Se ejecutó Finish y su confirmación autorizada; deployment pasó a finishing. Pipeline observado alerted, completion=33: deploy step 1977521 alerted/target FAILED (sin razón adicional expuesta), wait completado, finish del pipeline pendiente. No se reintentó, ignoró, abortó, hizo rollback ni Instant termination. api-test no iniciado; requiere atención humana antes de continuar según skill.

- **2026-10-22** — Confirmación final recibida para ambos deploys. Iniciado test: pipeline 533333, deployment 38929535, build 202610.9.0-feat-rio-sunset-u.1. Create Infrastructure completado; Boot Application en curso. api-test se ejecutará después del éxito terminal de test.

- **2026-10-22** — Activación finalizada: test y api-test en finished sobre versión previa 202609.18.1. Gates de scopes aceptados nuevamente con respuesta completa. Preparados dos formularios Review Deployment separados para 202610.9.0-feat-rio-sunset-u.1 @d2d0f8b3, inicio inmediato, un destino cada uno; no se presionó Execute Pipeline. Sin despliegues activos. Solicitada confirmación final conjunta para ejecutar secuencialmente test y api-test y cerrar con Finish.

- **2026-10-22** — Rodrigo autorizó explícitamente activar test y api-test. Se ejecutó Activate → Apply conservando la versión previa 202609.18.1. API confirma ambos en activating. La versión corregida 202610.9.0-feat-rio-sunset-u.1 todavía no fue desplegada; pendiente activación estable y confirmación final.

- **2026-10-22** — Mac desbloqueado. Respuesta completa de scopes guardada sin editar; gates aceptan Materializer test y api-test. Fury impide seleccionarlos por estado inactive y exige Activate en Scopes. Revisión automática rechazó Activate por falta de autorización explícita de esa mutación operativa; solicitada a Rodrigo. No se activó ni desplegó. Sin despliegues activos en Materializer. Rodrigo indicó test para el resto: gates aceptan ClickHouse/Kafka/Playmaker y rechazan Flink/Signals/Fury porque no existe scope literal test.

- **2026-10-22** — Solicitud autorizada para las cinco dependencias. Repos Materializer y Zord ya presentes en fuentes/vault. Zord contiene cambios ajenos y no se alteró. Actualizada referencia remota de la skill, sincronizada adaptación canónica y actualizada develop por fast-forward conservando graphify-out.
- **2026-10-22** — PR #738 abierto desde `feature/rio-sunset-update-rio-materializer`, head `05006e37`, base develop. Build local y 1.825 tests pasan; iniciado `fury create-version`.
- **2026-10-22** — Rodrigo aprobó todos los pins y amplió alcance a [[Sunsets backends RIO]]. Lote completo de Materializer pasa build local; no se han hecho deploys.
- **2026-10-22** — Catálogo de `202610.9.0-feat-rio-sunset-u.1`: cero sunsets sobre 349 dependencias. Gate `validate-build.mjs` acepta `d2d0f8b3dfa607fecc1743129e63e449cc7c7749`. Scopes test y api-test seleccionados; gate y confirmación inmediata pendientes.


## 🧭 Decisiones

- NoSQL usa `issues[].upgrade_to = "0.2.6"` (valor estructurado sin purl); coincide con objetivo literal del usuario y existe en registry. No se derivó del texto `suggested`.
- Los deadlines UTC se conservan como evidencia; la UI muestra el día anterior en America/Santiago.

## 🔗 Docs / Links

- [[rio-materializer]] · [[local-agents-pipeline-cli]] · [[ads-signals-skills-marketplace]].



