---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Meli]]"
parent:
sprint:
start:
due:
progress: 80
repo:
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/meli
created: "2026-10-22"
updated: "2026-10-23"
---

# Sunsets backends RIO

## 🎯 Objetivo

Atender todos los sunsets de los backends y control planes RIO, excluyendo frontends, por ampliación explícita de Rodrigo el 2026-10-22. Horizonte: todos los abiertos, incluidos vencidos. Preservar cambios locales ajenos y entregar evidencia por aplicación.

## 📊 Estado actual

Discovery agregado completo de 13 apps: 35 dependencias con sunset; 7 vencidas repartidas en Playmaker (4) y Signals (3). Observability, Infra, Storage, Vector y rio-sdk-events sin sunsets. Catálogos paginados y conteos coincidentes por app; versiones desplegadas inspeccionadas para obtener los objetivos de `issues[].upgrade_to`. La mayoría de los fixes ya existe en develop; se confirma resolución efectiva antes de clasificar redeploy.

Materializer: PR #738, NoSQL y tres pins Jackson/Vert.x aprobados; lote final pasa Gradle build/jacocoTestReport. PR actualizado: head d2d0f8b3, build 202610.9.0-feat-rio-sunset-u.1 FINISHED y gate SHA aceptado; catálogo nuevo cero sunsets/349 dependencias. Rodrigo eligió test y api-test; ambos inactivos, presentes en el formulario de deploy. Pendientes gate de scopes y confirmación inmediata.

Los siete builds nuevos están FINISHED, con gates de SHA aceptados y catálogos completos sin sunsets. Esto verifica los artefactos; los scopes antiguos siguen pendientes de rollout. KMS requiere acción humana sobre prod. El Mac bloqueado impide guardar la evidencia original para el gate de scopes mediante la UI disponible.

## 🧱 Entrega de desarrollo

| App | Base develop | Pendiente real del catálogo | Ruta inicial |
| --- | --- | --- | --- |
| [[rio-materializer]] | 216c0e54 | Jackson, NoSQL, Vert.x; LZ4 stale | PR #738 + test |
| [[rio-controlplane-flink]] | 920a7075 | Jackson 2.21.5; Guava 33.6.0-android | Jackson ya efectivo 2.21.7; pin Guava 33.7.2-jre en feature/rio-sunset-update-rio-controlplane-flink |
| [[rio-controlplane-clickhouse]] | 126633f0 | LZ4 1.10.2 | develop declara 1.11.4; verificar redeploy |
| [[rio-controlplane-kafka]] | f4b5701e | Jackson 2.21.5 y LZ4 1.10.1 | Pins efectivos 2.21.7/1.11.4; checkout original sucio preservado |
| [[rio-playmaker]] | 4011c077 | 15 dependencias, cuatro vencidas | Las 15 ya resueltas en develop; afectan solo test4-nonprod |
| [[rio-controlplane-fury]] | b0fb7af1 | LZ4 1.10.1 | develop ya fija 1.11.4 |
| [[rio-controlplane-kms]] | 1168240a | Jackson 2.21.5 | Solo prod conserva 2.21.5; otros scopes ya 2.21.7; acción humana productiva |
| [[rio-controlplane-signals]] | 10a98bc0 | BOM/Streams/commons vencidos; Jackson | Efectivos BOM/Streams 4.0.7, commons 3.0.1, Jackson 2.21.7; redeploy |
| [[rio-controlplane-observability]] | — | Ninguno | NOTHING_ELIGIBLE |
| [[rio-sdk-events]] | — | Ninguno | NOTHING_ELIGIBLE |

SPEC funcional: este objetivo y la solicitud explícita del usuario. SPEC técnica: ejecutar [[30-resources/agents/skills/rio-sunset-update/SKILL|rio-sunset-update]] por app; un único PR si hace falta código, o build ligado al SHA base y redeploy de test si el código ya cumple. No cambiar gestores mayores ni tocar producción/stage sin intervención humana.

### SPEC técnica — Flink

Base develop @ 920a7075. Rama feature/rio-sunset-update-rio-controlplane-flink. Único cambio nuevo: pin de Guava a 33.7.2-jre en eachDependency existente; objetivo verificado en issues[].upgrade_to y Maven Fury. Jackson ya efectivo 2.21.7, no duplicar cambios. Validar runtimeClasspath, build/tests, pre-commit y PR único.

## ✅ Tareas

- [x] Sincronizar skill y validar input por app. #owner/agent #type/dev #area/meli
- [x] Barrer catálogos, scopes, issues y trabajo en curso de las apps conocidas. #owner/agent #type/research #area/meli
- [x] Confirmar inventario de CPs en Fury y resolución efectiva desde bases limpias. #owner/agent #type/research #area/meli
- [x] Completar PR y build final de [[Sunsets rio-materializer]]. #owner/agent #type/dev #area/meli
- [x] Resolver cambios nuevos y verificar nativamente; no duplicar fixes ya merged. #owner/agent #type/dev #area/meli
- [x] Crear/reusar builds inmutables ligados al SHA correcto. #owner/agent #type/dev #area/meli
- [ ] Elegir y confirmar scopes de test, luego verificar deploy/Finish. #owner/me #type/dev #area/meli
- [ ] Entregar matriz final con pendientes productivos/stage y evidencia. #owner/agent #type/dev #area/meli

## 📆 Bitácora

- **2026-10-23** — Auditoría read-only solicitada por Rodrigo; despliegues pausados por instrucción humana. Inventario corregido: ocho versiones en siete apps, incluyendo Materializer .0 intermedia y .1 final. Únicos PRs creados: Materializer #738 y Flink #217, ambos OPEN/draft, no merged, checks relevantes SUCCESS. Comparación contra develop remoto actual confirma que NoSQL/Jackson/Vert.x de #738 y Guava de #217 aún faltan; no son duplicados del develop actual. LZ4 de Materializer y Jackson de Flink ya existían y no se duplicaron. Las otras cinco apps ya tenían los fixes. CI de develop actual SUCCESS para ClickHouse/Kafka/Playmaker/Fury/Signals; ClickHouse, Playmaker y Fury avanzaron de SHA pero mantienen idéntico manifest respecto al build auditado. No se recompiló ni creó otra versión durante esta auditoría.

- **2026-10-22** — Flink api-nonprod completado: pipeline 533792 completed/100%, deploy/wait/finish completed; deployment 38932155 finished/active=false. Signals también completado (533791/38932153). Finish automático observado en ambas; no se duplicó. Validación runtime de los dos destinos cerrada, con artefactos sin sunsets; otros scopes pendientes de rollout.

- **2026-10-22** — Signals test-nonprod completado: pipeline 533791 completed/100%, todos los pasos completed; deployment 38932153 finished/active=false. Finish fue automático en este flujo y se verificó sin duplicarlo. Artifact 202608.21.1-develop.0 @10a98bc0 sin sunsets; prod/stage pendientes humanos. Flink alcanzó deploy completed y wait running.

- **2026-10-22** — Confirmación final recibida para Signals test-nonprod y Flink api-nonprod. Ejecutados pipelines 533791 (deployment 38932153) y 533792 (deployment 38932155), respectivamente. Ambos running al inicio, sin conflictos. No se ejecutará Finish antes de revisar estado y secuencia del pipeline.

- **2026-10-22** — Rodrigo autorizó test-nonprod o el equivalente principal. Signals test-nonprod y Flink api-nonprod (único web de prueba en el inventario de Flink) aceptados por gate con respuestas originales completas. Builds ligados a 10a98bc0 y 884c1326; PR #217 conserva SHA. Ambas configuraciones Review Deployment listas, sin conflictos activos. Confirmación final solicitada, sin ejecutar. Fury carece de test-nonprod y tiene roles separados, principal no determinado. Cambios automáticos mostrados: OTel 0.1.9→0.1.10 en ambas, Config Service sidecar 1.23.0→1.24.0 en Signals.

- **2026-10-22** — Test desplegó la versión corregida: pipeline 533333 / deployment 38929535. Deployment alcanzó effective, application_up=1, containers_started=1, failed_instances=0, swappedIn=100. Se ejecutó Finish y su confirmación autorizada; deployment pasó a finishing. Pipeline observado alerted, completion=33: deploy step 1977521 alerted/target FAILED (sin razón adicional expuesta), wait completado, finish del pipeline pendiente. No se reintentó, ignoró, abortó, hizo rollback ni Instant termination. api-test no iniciado; requiere atención humana antes de continuar según skill.

- **2026-10-22** — Activación finalizada: test y api-test en finished sobre versión previa 202609.18.1. Gates de scopes aceptados nuevamente con respuesta completa. Preparados dos formularios Review Deployment separados para 202610.9.0-feat-rio-sunset-u.1 @d2d0f8b3, inicio inmediato, un destino cada uno; no se presionó Execute Pipeline. Sin despliegues activos. Solicitada confirmación final conjunta para ejecutar secuencialmente test y api-test y cerrar con Finish.

- **2026-10-22** — Rodrigo autorizó explícitamente activar test y api-test. Se ejecutó Activate → Apply conservando la versión previa 202609.18.1. API confirma ambos en activating. La versión corregida 202610.9.0-feat-rio-sunset-u.1 todavía no fue desplegada; pendiente activación estable y confirmación final.

- **2026-10-22** — Mac desbloqueado. Respuesta completa de scopes guardada sin editar; gates aceptan Materializer test y api-test. Fury impide seleccionarlos por estado inactive y exige Activate en Scopes. Revisión automática rechazó Activate por falta de autorización explícita de esa mutación operativa; solicitada a Rodrigo. No se activó ni desplegó. Sin despliegues activos en Materializer. Rodrigo indicó test para el resto: gates aceptan ClickHouse/Kafka/Playmaker y rechazan Flink/Signals/Fury porque no existe scope literal test.

- **2026-10-22** — Ampliación autorizada desde Materializer a todos los CPs/backends RIO excepto frontends. Checkouts ClickHouse y Kafka tienen cambios funcionales ajenos; Playmaker tiene probes sin trackear. Se preservan íntegros. Las inspecciones sobre sus bases usan Git read-only o checkout aislado, nunca stash/reset de cambios ajenos.
- **2026-10-22** — Plugin meli-security-expert 1.14.0 instalado por autorización explícita; activación local verificada en .codex/config.toml. Los catálogos de Infra/Storage/Vector confirman cero sunsets. Playmaker tiene las 15 dependencias resueltas en develop; todos los avisos vienen de test4-nonprod.
- **2026-10-22** — Flink: PR [#217](https://github.com/melisource/fury_rio-controlplane-flink/pull/217), head `884c132609ebf5762b16a5457c7ff49d5031ea8d`, build local + 1.966 tests + pre-commit pasan. Materializer: PR #738, build final FINISHED, catálogo cero sunsets.
- **2026-10-22** — Builds de redeploy creados desde develop limpio: ClickHouse `0.0.2-mergetree-component-im.2` @126633f0; Kafka `202609.22.1-rc1.0` @f4b5701e; Playmaker `202608.13.1-develop.3` @4011c077; Fury `202610.5.0-logs-tag.0` @b0fb7af1; Signals `202608.21.1-develop.0` @10a98bc0. CLI devolvió exit 1 en los tres clones de /private/tmp tras crear las versiones, pero API confirmó creación durable; no se repitieron.
- **2026-10-22** — ClickHouse, Kafka, Playmaker y Signals: builds FINISHED, gates SHA aceptados y catálogos nuevos completos con cero sunsets (198/197/303/202 dependencias). Materializer también FINISHED/gate/catálogo cero. Flink FINISHED/gate SHA/catálogo cero sobre 339 dependencias; Fury también FINISHED, gate aceptado y catálogo completo sin sunsets sobre 167 dependencias. Materializer scopes pedidos por Rodrigo: test y api-test; ambos inactivos en Fury, pendiente gate de scopes y revisión de disponibilidad. Mac bloqueado durante preparación visual; se pidió desbloqueo manual, sin iniciar login.
- **2026-10-22** — Scopes explícitos solicitados a Rodrigo para Flink, ClickHouse, Kafka, Playmaker y Signals después de gates verdes. No se infirieron nombres ni se retuvieron defaults. El updater AOC no está disponible en este runtime; no se afirmó ejecución de update-internal.


## 🧭 Decisiones

- No confundir sunset de un artefacto viejo con defecto actual del manifest. El catálogo agregado manda para discovery; Gradle/catálogo del build nuevo manda para afirmar resolución.
- No crear una release productiva limpia desde una rama de trabajo. Test requiere build con sufijo, gate SHA, gate scope y confirmación inmediata.

## Reportes

- [[rio-sunset-update-rio-materializer-20261022-1331]] — rio-materializer
- [[rio-sunset-update-rio-controlplane-flink-20261022-1331]] — rio-controlplane-flink
- [[rio-sunset-update-rio-controlplane-clickhouse-20261022-1331]] — rio-controlplane-clickhouse
- [[rio-sunset-update-rio-controlplane-kafka-20261022-1331]] — rio-controlplane-kafka
- [[rio-sunset-update-rio-playmaker-20261022-1331]] — rio-playmaker
- [[rio-sunset-update-rio-controlplane-fury-20261022-1331]] — rio-controlplane-fury
- [[rio-sunset-update-rio-controlplane-kms-20261022-1331]] — rio-controlplane-kms
- [[rio-sunset-update-rio-controlplane-signals-20261022-1331]] — rio-controlplane-signals

## 🔗 Docs / Links

- [[Sunsets rio-materializer]] · [[30-resources/agents/skills/rio-sunset-update/SKILL|rio-sunset-update]].




