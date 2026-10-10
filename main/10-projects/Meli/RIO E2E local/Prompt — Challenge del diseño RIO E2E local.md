---
type: prompt
schema_version: 1
status: active
area: "[[Meli]]"
target: "IA revisora de arquitectura con acceso de lectura al workspace"
prompt_version: 1
inputs: ["Propuesta RIO E2E local", "Código vigente de cinco aplicaciones", "Contratos y evidencias heredadas"]
outputs: ["Challenge con evidencia", "Diseño revisado", "Matriz de viabilidad y E2E", "Plan mínimo por repo y expansión"]
application:
project: "[[RIO E2E local]]"
aliases: ["Challenge RIO E2E local", "Prompt diseño RIO Kafka local"]
related: ["[[Kafka — Ambiente local con servicios reales]]"]
tags:
  - kind/prompt
  - area/meli
  - project/rio-e2e-local
created: "2026-10-08"
updated: "2026-10-09"
---

# Prompt — Challenge del diseño RIO E2E local

## Propósito

Encargar a una IA un challenge crítico, basado en código vigente, que mejore la propuesta antes de implementar. Kafka producers/consumers dentro de las aplicaciones es la base; no se propone un bridge. Primer alcance: cinco aplicaciones; crecimiento posterior al ecosistema.

## Contrato de entrada

- Proyecto [[RIO E2E local]], propuesta y límites en esta nota; repos locales si están disponibles.
- Antecedentes [[Kafka — Ambiente local con servicios reales]] y worktrees históricos, como consulta, no como base completa.
- Acceso sólo de lectura a repos y documentación. Si no hay acceso, declarar supuestos y fuentes faltantes; no inventar contratos.

## Contrato de salida

- Diseño revisado con flujo/contratos, matriz de challenge con evidencia y cambios mínimos por repo.
- Matriz de capacidades/seams, fronteras locales, riesgos, bloqueos y validación física/browser.
- Plan incremental para las cinco apps y extensión posterior, sin implementar ni operar infraestructura.

## Prompt

```text
Actúa como arquitecto revisor de RIO. Haz un challenge crítico y mejora el diseño de RIO E2E local antes de escribir código. No busco que confirmes la propuesta: intenta falsar sus supuestos, identifica fallos concretos y entrega una solución menor, clara y verificable.

ENCARGO Y BASE OBLIGATORIA

Primero debemos levantar cinco aplicaciones reales en paralelo: Playmaker, un front RIO vigente y los CP de Kafka, ClickHouse y Flink. Después ampliaremos al resto del ecosistema. Las cinco aplicaciones necesitarán también sus motores y almacenamiento locales; no asumas que son sólo cinco contenedores.

El transporte local debe usar producers y consumers Kafka embebidos en Playmaker y en los CP. La base es rio-deployment-trigger-local y rio-deployment-result-local. No uses un bridge Kafka→HTTP, ni externo ni embebido, ni un proceso relay/sidecar que entregue los eventos a controllers por HTTP. El front y Postman sí usan las APIs HTTP normales de Playmaker. Kafka sustituye el transporte BigQueue; los resultados los construye el negocio real.

En la medida de lo posible no tocar código productivo: reutiliza interfaces, DI y seams locales existentes. Conserva endpoints, DTOs, validaciones, routing, defaults, handlers, estados, errores, publishers, idempotencia y capacidades productivas. No dupliques reglas en listeners ni añadas ramas if local al negocio. Si no existe seam limpio, demuestra el impedimento y compara el refactor estructural mínimo con sus costes y pruebas de paridad. No asumas de entrada que hay que extraer handlers o crear interfaces nuevas. Sin un seam viable dentro de estas condiciones, declara BLOCKED; no cambies silenciosamente la arquitectura a bridge.

Usa Clean, SOLID, KISS y YAGNI como criterios concretos: responsabilidad de cada pieza, dependencias, necesidad demostrada y coste operativo. No construyas un framework, emulador Fury, librería común, registry de plugins ni abstracciones para CP futuros que aún no las requieren. Diseña una expansión sencilla después de validar los cinco.

CONTEXTO Y FUENTES

Si tienes acceso al workspace, resuelve VAULT_ROOT con AGENTS OS, ejecuta bootstrap una sola vez en cold start y recupera sólo el delta de RIO E2E local. Lee el proyecto /Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/RIO E2E local/RIO E2E local.md. No cierres la sesión.

Repos candidatos locales, rutas de consulta y remotos a verificar:
- /Users/rjara/fuentes/rio-playmaker → melisource/fury_rio-playmaker.
- /Users/rjara/fuentes/rio-controlplane-kafka → melisource/fury_rio-controlplane-kafka.
- /Users/rjara/fuentes/rio-controlplane-clickhouse → melisource/fury_rio-controlplane-clickhouse.
- /Users/rjara/fuentes/rio-controlplane-flink → melisource/fury_rio-controlplane-flink.
- Front: /Users/rjara/fuentes/ads-signals-frontend → melisource/fury_ads-signals-frontend; /Users/rjara/fuentes/rio-frontend → melisource/fury_rio-frontend. El vault marca rio-frontend deprecated y ads-signals-frontend como reemplazo. Verifica cuál corresponde a los journeys requeridos y elige uno; si sigue ambiguo, plantea esa definición concreta al owner. No levantes ambos sin motivo.

Hay cambios ajenos en los repos originales: preserva todo. Resuelve realpaths, remotes, common-dir, rama, HEAD/status y versiones Java/Node/SDK. Lee AGENTS.md, testing/docs y sólo los flujos relevantes. No copies APIs de memoria. Los SHAs son referencias observadas el 08/10, no garantía de vigencia: PM develop44c290591a104e1471f43f132007fb6d13169684; Kafka develop6a91937c0664d83f907dec222af8a96b4042c6ae; CH developc8b20b6531a73348314587fc14f43e0ad8ce76ae; Flink develop7c645ea92f86650744a3c5ee1bad0012633ef0e9. Verifica referencias remotas sólo mediante lectura si resulta necesario; no sincronices/modifiques checkouts en esta fase.

Playmaker develop ya contiene LocalKafkaDeploymentTriggerProducer y LocalKafkaDeploymentResultListener en localintegration y el perfil local,local-integration. Su launcher inicia MySQL/Kafka/PM, no el CP. CP Kafka PR85 ya fue merged y conserva LocalKafkaBigQueueClient y standalone25. Historical PM /Users/rjara/fuentes/rio-playmaker-kafka-e2e es un worktree del mismo repo, feature/kafka-real-e2e@acbda2f, con adapters actions y gate Sandbox. Historical CP /Users/rjara/fuentes/rio-controlplane-kafka-e2e tiene KafkaTriggerHttpBridge y KafkaResultBigQueueClient: consulta contratos, no copies el bridge ni gates remotos. Preserva /Users/rjara/fuentes/rio-controlplane-kafka-memory-e2e; contiene capacidades GCP ausentes en producción. No usar mavenLocal, publicar SDKs de prueba ni bajar Java por comodidad.

Existe además una entrega HTTP local verificada en /Users/rjara/fuentes/rio-playmaker-kafka-http-lifecycle y /Users/rjara/fuentes/rio-controlplane-kafka-http-lifecycle. Ocho E2E HTTP pasaron y se corrigió un lifecycle DEPROVISION PM; esa evidencia no certifica el nuevo transporte Kafka ni los otros CP ni el front. Consulta selectivamente y conserva sus ramas/diffs. El CP local usa Java21 y PM histórico declara25: verifica cada base y no homogeneices versiones arbitrariamente.

PROPUESTA QUE DEBES CHALLENGEAR

Front/Postman → API Playmaker → producer Kafka → trigger local → consumer CP correspondiente → lógica/provisioner real → efecto físico → publisher CP real con transporte Kafka → resultado local → consumer PM real → estado persistido observable.

Inicialmente un broker compartido, dueño Compose CP Kafka, red rio-local, endpoint interno rio-kafka:19092. PM39080/CP Kafka39081/broker host39092/MySQL33306 son valores previos propuestos/implementados para dos apps; define los de front/CH/Flink tras comprobar colisiones. Un CP nuevo no implica otro broker. ClickHouse real y runtime Flink real son motores adicionales; averigua sus requisitos, no asumas que una imagen Flink reemplaza el Cloud Controller usado por el CP.

La VM acordada rio/colima-rio tiene4CPU/8GiB/40GiB: calcula si alcanza para cinco apps+motores. No operes la VM. Conserva el runbook colima-rio-grpc-port-forwarder: no colima stop ni cambios a default; si luego se autoriza operación, no reiniciar una VM que ya corre.

CHALLENGE OBLIGATORIO

1. Viabilidad por aplicación: quién produce/consume hoy, interfaz/qualifier/profile y wire format/SDK resuelto; filtros de component_type/template/schema/context/routing y estados finales. Identifica el seam menor, archivos que cambiarían y dependencia externa que impediría una ejecución local real. CP Kafka tiene guards/routing en controllers: llamar sólo al processor puede saltarlos. No generalices ese diagnóstico a CH/Flink sin leerlos.
2. Topología: compartir trigger/result entre CP, aislamiento por ambiente y groups diferentes por CP. Si comparten group, Kafka puede repartir a un CP equivocado; demuestra cómo evitarlo conservando filtros/contratos. Keys, particiones, orden por correlación, versiones SDK, campos desconocidos y envoltura: Kafka existente usa payload SDK crudo, BigQueue HTTP usa envelope; evitar doble wrapping y pérdidas de campos. Observer E2E independiente que no robe mensajes.
3. Fiabilidad: estado PM visible antes de publish, transacciones/AFTER_COMMIT aplicables, ACK producer y timeouts; aceptación frente a fin de procesamiento; offsets, executor async, rebalance, shutdown, replay y orden STARTED→terminal según contrato. Separar FAILED de negocio, payload inválido y fallo de transporte. Proponer política explícita de retry/DLT sustentada en contratos, sin nuevas políticas de negocio ni prometer exactly-once/atomicidad Kafka-MySQL-KVS.
4. Gap conocido CP Kafka: DeploymentResultPublisher absorbe fallos de publicación y el guard puede finalizar antes de enviar. Replay puede descartarse sin recuperar resultado. Kafka no lo resuelve solo. Conserva evidencia y distingue conservación productiva de cualquier cambio de fiabilidad que necesite otro alcance. GCP PEEK actual es FAILED/INVALID_PARAMS/unmapped sin STARTED: no copiar factories locales que lo conviertan artificialmente en COMPLETED.
5. Motores reales: CH SQL/DDL/grants/context/lifecycle; Flink deploy/job/status/cancel y datos, según lo que el código soporte. Qué depende de Cloud Controller, cloud/Kubernetes/storage y qué se puede conectar localmente mediante seams existentes. No simular provisioners, SQL o jobs para declarar E2E. Si falta seam, declarar BLOCKED y el cambio mínimo requerido.
6. Fronteras: MySQL, KVS, auth/Entity/metadata y otras dependencias mínimas. Mapas por JVM sólo si satisfacen contratos CAS/TTL/atomicidad/locks requeridos; declarar límites de restart/coordination. Mecanismos locales explícitos manteniendo validaciones; no certificar ACME/Entity/OAuth/Fury como integrados. No-op de idempotencia, permisos universales o fixtures que construyan el estado esperado no acreditan el flujo.
7. Front: verificar repo, versiones, BFF/env/auth/CORS/rutas y polling/eventos reales. Proponer al menos un journey disponible por CP; si la UI no lo expone, separar el gap UI del caso API. Un E2E backend no prueba el front.
8. Operación: Compose/Dockerfiles pequeños, imágenes fijadas compatibles, jar copiado/no bind mount, healthchecks, readiness/grupos y recursos. Comandos arranque/test/cleanup desde cualquier ruta con espacios; owner labels/names únicos; limpiar sólo recursos propios, detener consumers antes de retirar broker/red. No supervisor ni CLI/framework extenso. Dimensionamiento/arranque paralelo realistas, no delays para esconder carreras.
9. Verificación y expansión: matriz caso→API/journey→trigger→CP resultado→PM estado→efecto físico, errores/replays y gaps por los tres CP. JUnit/Gradle y dependencias actuales, gates/impact de cada repo y pruebas browser del front. Conservar standalone25 Kafka. Dos suites seguidas sobre mismo ambiente vivo, recreación limpia y reproducción independiente desde clones; sin suites concurrentes. Proponer fases que terminen con las cinco apps y sólo después extender a otros CP, materializer y ecosistema; limitar generalización a necesidades demostradas.

ENTREGA

- Veredicto de viabilidad y tabla por las cinco apps: capacidad/seam, frontera sustituida, cambio mínimo, riesgo y PASS/FAIL/BLOCKED/NO_EJECUTADO según evidencia real.
- Challenge priorizado: supuesto → evidencia archivo/símbolo/versión → fallo/impacto → mantener/cambiar/descartar → corrección menor. Distingue observación de inferencia; no inventes ejecución o paridad.
- Arquitectura revisada con diagrama, responsabilidades, contratos/tópicos/groups/keys y secuencias incluyendo ACK, commit, error y replay.
- Alternativas sin bridge: cero cambio productivo frente a refactor estructural mínimo. Justifica la elegida con Clean/SOLID/KISS/YAGNI y coste de mantenimiento; enumera lo que eliminarías de la propuesta.
- Inventario exacto de cambios/dependencias por repo, pruebas de paridad y límites productivos.
- Plan gradual y criterios de aceptación para cinco apps, matriz E2E físico/browser y expansión posterior.
- Lista breve de decisiones imprescindibles del owner y bloqueos concretos. No pedir permiso para leer/discutir ni usar preguntas como sustituto de discovery.

Entrega un diseño proporcional, no un aparato documental. Puedes actualizar sólo documentos de RIO E2E local por delta y usando templates AGENTS OS. No implementes código, no crees ramas/worktrees ni repos nuevos, no arranques Docker, no uses recursos Fury/remotos ni publiques PR/merge. No ejecutes la integración en esta fase. Conserva límites y fallos actuales; no declares terminado el E2E por compilar, ping, HTTP200 o ACK Kafka.
```

## Límites

- Diseño/challenge, no implementación ni autorización para operar infraestructura o publicar.
- Kafka producers/consumers sin bridge es requisito del owner; alternativas/refactors deben respetarlo o declarar bloqueo.
- Cinco aplicaciones iniciales; un front a resolver y sus motores reales. Evidencias históricas no se transfieren al nuevo alcance.
