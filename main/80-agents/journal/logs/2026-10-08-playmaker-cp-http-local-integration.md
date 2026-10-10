---
type: change_log
schema_version: 1
scope: session
created: "2026-10-08"
updated: "2026-10-08"
area:
project: "[[Kafka — Ambiente local con servicios reales]]"
application:
entities: ["[[rio-playmaker]]", "[[rio-controlplane-kafka]]"]
related: []
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

# 2026-10-08-playmaker-cp-http-local-integration

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- Tipo: updated.
- Archivo: proyecto Kafka — Ambiente local con servicios reales; SPEC LOCAL-HTTP-1, tareas y checkpoint de implementación.

## Motivo

El owner encargó implementar la continuidad local Playmaker→CP→Kafka→Playmaker conservando producción, con MySQL propio y sin capacidades remotas.

## Fuentes usadas

- Prompt maestro del owner; bases Git verificadas Playmaker develop44c2905 y CP PR85 OPEN aa19883/develop931893e.
- Contratos SDK resueltos y documentación primaria Toolkit KVS0.7.4.
- Review cruzado de agentes, Gradle y primera ejecución física del stack Docker propio.

## Resolución aplicada — primer candidato histórico

Ramas nuevas de integración; HTTP por interfaces locales, sourceSets separados, broker dueño CP y MySQL propio. Fixture HTTP ACME fail-closed conserva cliente y autorización real. Modos KVS locales separados resultados-upsert y locks-create-only. No cambios de negocio ni providers GCP adicionales.

## Validación — primer candidato histórico

PM4787 productivos/0fails/0errors/2skips +7 locales PASS; CP691 productivos+12 locales PASS y standalone25/25 PASS. Seis selectores y3 checksL0 PASS; validadores documental/impact/diffPASS. PMD claro; Checkstyle PMPASS y CP únicamente namespace underscore heredado.

Cinco suites completas (dos mismo ambiente vivo, recreación vacía, clon independiente y certificación final por autor distinto):7tests/5PASS/2FAIL/0errors/skips cada una. Fuente final verifica ambos DEPROVISION CP COMPLETED/Kafkaausente antes de esperar PM; ambos quedan requested/is_active por terminal previo del mismo deployment DB ID. Lifecycle completo FAIL/BLOCKED, sin corrección productiva ni expectativas debilitadas. Modo DIRECT desde clon pasó PROVISION y PEEK físicos y reprodujo el mismo undeploy.

Clones limpios fuera de HOME/con espacios; jars productivos0 clases/recursos nuevos locales, Java25PM/21CP. Recorder restringido a loopback, alcanzable vía host.docker.internal corroborado desde CP. SO_REUSEADDR habilita puertos liberados y rechaza listener activo. Todas las limpiezas propias físicas certificadas; una etiqueta residual de imagen standalone se retiró explícitamente sin tocar imágenes ajenas. Originales/PR85 intactos, VM rioRunning4CPU/8GiB/40GiB y contexto global preservados.

Ramas staged sobre bases exactas, sin commits nuevos porque L1 rojo; sin push/PR/merge ni bypass de hooks. MeliAppSec MCP y aoc-management update-internal NOT_EXECUTED por capacidades ausentes; arquitectura local/documentos actualizados. Sesión activa. Guía operacional KAFKA_HTTP.md y evidencia JUnit/logs sanitizados fuera del diff.

## Compartibilidad

- Scope: local.
- Sin credenciales, prompts crudos, paths de máquina ni dumps.

## Rollback

Retirar delta de estas ramas nuevas y detener sólo sus proyectos Compose, Playmaker antes de red CP; no tocar originales ni VM. La sesión continúa activa.


## Delta LOCAL-HTTP-2 — entrega vigente

El owner autorizó corregir Playmaker y exigió PM desde develop sincronizado y CP con su desarrollo local actual. PM `44c2905` fue confirmado mediante fetch/ls-remote antes de crear la rama lifecycle. PR85 fue merged externamente el 08/10 a las 21:35:09 UTC; CP develop `6a91937` tiene el mismo árbol que el local aprobado `aa19883`. La nueva rama CP parte de ese develop y recibe sólo el overlay HTTP anterior. Originales y primeros candidatos se preservan.

Luna implementó guard de terminal UNDEPLOY por deployment + UUID, rotó ambas correlaciones y publicó AFTER_COMMIT. COMPLETED deja deployment inactivo y termina su service; componente global y ComponentRun previo se conservan. Un error postcommit usa REQUIRES_NEW sólo para la misma operación aún REQUESTED. Sol detectó el caso superseded: el fallo puede marcar la fila vieja FAILED, pero no el service reemplazante. Luna añadió ese guard y su test H2; otro agente Luna revisó los tres archivos sin findings concretos. Root certificó la suite escrita por Sol.

Resultado final: PM **4795 tests, 0 fallos/errores, 2 skips existentes**, más 7 locales; lifecycle 131/131 y H2 consumer 9/9. CP **691 +12 locales**, y standalone físico **25/25** en modo Kafka. Jars productivos excluyen locales. Gate de 12 selectores, tres L0 existentes y L1 PASS. Fuente final: dos E2E vivos **8/8** (13.416/12.069 s), mismos IDs/timestamps de contenedores; después down/recreación **8/8** (13.207 s); clon independiente **8/8** (13.425 s), sin fallos/errores/skips. El primer oracle nuevo usó un campo action que el DTO slim no expone; se corrigió usando legacy GET real, conservando los checks slim/físicos y la evidencia fallida.

Sol reprodujo desde clones Git limpios fuera de HOME/con espacios. CP check y packaging, PM locales y packaging PASS. El modo DIRECT separado pasó PROVISION físico, PEEK con keys/values/límite y DEPROVISION completed/inactive, slot terminated/sin activo y Kafka ausente. Fixtures API borrados. Tras la guía final, **42 archivos PM y 8 CP idénticos** a clones; validators repository 7/11/8 y testing 12/4 PASS. Schema de proyecto/change_log/agent_run PASS. Cero findings estáticos nuevos; se conservaron 2 Checkstyle +1 PMD de Undeploy y namespace CP heredado.

Auditoría: cero contenedores, red, volúmenes o imágenes propios; contexto global colima y VM rio Running, 4 CPU/8 GiB/40 GiB. Identidad/status Git de originales/historia/base aprobada/primer candidato: 7/7 intactos. La lectura VM inicial usó un LIMA_HOME vacío; se corrigió al del runbook sin operar la VM. Evidencia JUnit/logs redactados y patches fuera del diff; clones temporales conservados para auditoría.

Alcance local completo, proyecto progress 100 y status active; sesión sin cierre. Ramas staged sin commit/push/PR/merge propio, listas para revisión humana. GCP PEEK exitoso sigue BLOCKED; pérdida de callback conserva ausencia de watchdog. MeliAppSec/AOC NOT_EXECUTED por herramientas ausentes. Agent runs actualizados por delta: Luna código/adapters; Sol tests/revisión/reproducción; manager modelo desconocido. Tokens/coste desconocidos.


**Sincronización solicitada — 08/10, 22:22:44 UTC:** fetch y merge --ff-only de origin/develop en ambas ramas finales. PM44c2905 y CP6a91937 ya coincidían con sus develop remotos (0 ahead/0 behind); CP incluye PR85 local merged. Sin conflictos ni cambios de código. Los diffs staged de 42PM/8CP quedaron byte-idénticos; no se repiten tests al no cambiar fuentes/bases. Sesión activa; sin push/PR/merge remoto.

**Discovery solicitado — transporte Kafka/BigQueue:** revisión de código, sin modificar repos ni arrancar infraestructura. PM develop44c ya contiene `local-integration`, producer/listener Kafka de deployments y launcher MySQL+Kafka; ese launcher no inicia CP y su check L0 inyecta un resultado sin correlación real. El worktree histórico PM `rio-playmaker-kafka-e2e` (misma raíz Git/remote Playmaker, `feature/kafka-real-e2e@acbda2f`) añade actions y gate `local/02-real-e2e.sh`. CP histórico `rio-controlplane-kafka-e2e@7f1720d` contiene `KafkaTriggerHttpBridge`: consume triggers Kafka, envuelve `{msg:...}` y POST a los controllers del propio CP; `KafkaResultBigQueueClient` lleva los resultados productivos a Kafka, donde PM consume. HTTP en ese bridge simula la entrega push de BigQueue; difiere del transporte HTTP directo recién certificado. Runner histórico exige Sandbox/caller reales y cinco brokers; no constituye una integración puramente local certificada. CP develop local aprobado ya dispone de `LocalKafkaBigQueueClient`, pero no de ese bridge. El desarrollo congelado registra además factory GCP ausente en producción: no copiarla ni acreditar PEEK GCP por esa vía. Búsqueda GitHub accesible de repos Playmaker sólo devolvió `melisource/fury_rio-playmaker`; SDK events histórico contiene un adapter de archivos, no un broker BigQueue autónomo. Pendiente adaptar selectivamente transporte Kafka al broker único CP si el usuario encarga esa fase; la evidencia HTTP previa no acredita ese recorrido.

**Diseño solicitado — LOCAL-KAFKA-1:** owner adopta tópicos locales deployment y pide diseñar antes de implementar. Propuesta registrada en proyecto: adapters Kafka dentro de PM/CP, un broker CP, sin bridge HTTP; entrada CP compartida para conservar filtros/schema/routing/métricas hoy ubicados en controllers. Propuesta de refactor estructural aún no implementada. JSON SDK crudo y keys correlacionadas; estado visible antes de publish, ACK broker, commit consumidor controlado y política de errores explícita. Gap observado: CP finaliza idempotencia antes de publish y DeploymentResultPublisher absorbe errores; Kafka no garantiza recuperar resultados perdidos por replay. No se promete exactly-once ni atomicidad MySQL/KVS/Kafka. HTTP8/8 sigue histórico; nueva fase implementación pendiente, proyecto0%. Read-only repos/Docker/VM; sólo delta AGENTS OS, sesión abierta.
