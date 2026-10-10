---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Kafka — Ambiente local con servicios reales]]"
  - "[[rio-controlplane-kafka]]"
  - "[[rio-playmaker]]"
aliases: []
tags:
  - kind/doc
  - project/kafka-local-real
created: "2026-10-08"
updated: "2026-10-08"
---

# Prompt maestro — Playmaker y CP Kafka local

## Propósito

Prompt listo para copiar a una sesión nueva. Encarga implementar y verificar la integración local; esta sesión sólo preparó la continuidad, no ejecutó la integración.

## Contenido

### Prompt maestro

Actúa como manager técnico local. Implementa una integración pequeña entre Playmaker real y el CP Kafka real, con Kafka y MySQL locales en Docker. Quiero levantar ambas aplicaciones en paralelo, enviar requests con Postman y ejecutar E2E que entren por Playmaker y comprueben efectos físicos y estado final en ambos sistemas. Conserva el comportamiento productivo. ClickHouse y el resto del ecosistema quedan fuera.

**1. Punto de partida y repositorios**

- CP aprobado: `/Users/rjara/fuentes/rio-controlplane-kafka-local-small`, rama `feature/kafka-local-small`, commit `aa198836c9a8c21b66e9ef5ac56afb965dc795ea`, base `develop@931893e00d26363c13bee35ca19ed0980b959b51`. PR https://github.com/melisource/fury_rio-controlplane-kafka/pull/85. Tiene Compose CP+Kafka+init, KVS mapa por proceso, resultados Kafka y25pruebas funcionales repetibles. Se verificaron691+6unitarios y el jar productivo excluye locales. El PR terminó con8checksPASS/2SKIPPED/0pendientes; aprobación de reviewers pendiente al cerrar.
- `/Users/rjara/fuentes/rio-playmaker-kafka-e2e` **ya existe y es un worktree del mismo repo Playmaker**, no un repo nuevo ni un módulo. Remote: `git@github.com:melisource/fury_rio-playmaker.git`; rama histórica `feature/kafka-real-e2e`, HEAD `acbda2f1e68ae7672de6f9571cd739da972ca07a`. Incluye `1b4b8e155` ("add real Kafka control-plane ecosystem gate"). Usa esa entrega como consulta y extracción selectiva, no como base completa.
- Playmaker develop remoto observado08/10: `44c290591a104e1471f43f132007fb6d13169684`. Verifica nuevamente el SHA antes de trabajar. El original `/Users/rjara/fuentes/rio-playmaker` está en release/202610.7.0 con cambios ajenos no trackeados: presérvalo. También preserva el CP original y `/Users/rjara/fuentes/rio-controlplane-kafka-memory-e2e`, desarrollo congelado.
- Resuelve realpaths y registra HEAD/rama/status antes de modificar. Crea un worktree limpio y rama nueva de integración desde Playmaker develop vigente. Si el repo no existe en otra máquina, clona el remote de Playmaker; no crees otro repositorio GitHub. No limpies ni reescribas el worktree histórico.
- No modifiques la rama ni el PR85. Si ya está merged, parte de CP develop vigente en otra rama limpia; si sigue abierto, usa aa19883 como dependencia explícita en otra rama de integración. No lo merges por tu cuenta.

**2. Discovery breve antes de código**

Lee AGENTS.md y skills aplicables; bootstrap AGENTS OS una sola vez y recupera sólo el delta de este proyecto. Cumple SPEC funcional→técnica→tareas si corresponde, con documentos proporcionales. Define una matriz caso→endpoint→trigger→resultado→estado Playmaker→efecto Kafka desde el código vigente, sin inventar URLs ni contratos.

Consulta en Playmaker AGENTS.md, testing.md, testing-scenarios.md, `.testing/impact.json`, scripts de testing, producers de deployments/actions y consumidores de resultados. El gate histórico `local/02-real-e2e.sh` exige Sandbox, caller real y `CP/e2e/run.sh`; no arrastres ese requisito al alcance local. Conserva los gates administrados existentes y añade sólo el wiring/gate local necesario, actualizando las reglas que describan esta nueva familia. El encargo autoriza infraestructura local propia y efímera; no autoriza Fury ni recursos remotos.

Verifica SDKs y wire format resueltos de ambos proyectos, qualifiers, transacciones, estados, errores y orden de eventos. No uses mavenLocal ni publiques versiones de prueba para arreglar compatibilidad. Lee la versión Java vigente de cada repo: el CP corre en21; el worktree histórico de Playmaker declara25. No bajes la versión de Playmaker por comodidad.

**3. Arquitectura mínima**

Un broker, dueño: Compose del CP. Playmaker se une a `rio-local` como red external y usa `rio-kafka:19092`; no levantes `docker-compose.kafka.yaml` de Playmaker ni otro broker. Conserva aliases `rio-kafka` y `rio-cp-kafka`; usa `rio-playmaker` y un alias único para su MySQL. Puertos parametrizados sin colisiones: CP39081/Kafka39092 existentes; propone PM39080/MySQL33306 y documenta los valores realmente implementados.

Levanta CP y Playmaker como aplicaciones utilizables por Postman. Prefiere Compose y Dockerfiles pequeños con COPY del jar, imágenes fijadas compatibles y healthchecks; nada de bind mounts del jar, supervisor o CLI extenso. Playmaker usa MySQL real propio y efímero. Las necesidades locales de KVS se resuelven por adapters mapa por proceso que respeten el contrato; sin Sandbox, NoOp de idempotencia ni coordinación fingida entre JVMs.

Colima acordado `rio`:4CPU/8GiB/40GiB, contexto `colima-rio`. Si ya corre, no reinicies. Arranque: `LIMA_HOME="$HOME/.colima/_lima" LIMA_SSH_PORT_FORWARDER=false limactl start colima-rio`; parada de VM únicamente con `limactl stop` y sólo si el usuario lo pide. Nunca `colima stop` ni perturbes la VM default. Runbook en AGENTS OS: `colima-rio-grpc-port-forwarder`.

**4. Loop real de transporte, sin negocio simulado**

Implementa adapters HTTP locales a través de las interfaces existentes:

`API Playmaker → producer real → POST envelope al CP → processors/provisioners reales → Kafka real → publishers reales → POST envelope a Playmaker → consumers reales → estado persistido observable`.

Entradas existentes del CP: `/triggers/deployments` y `/triggers/actions`. Callbacks observados en Playmaker: `/events/deployment/result` y **`/events/actions/result` (plural)**; reconfirma en la base vigente. Conserva el envelope BigQueue, IDs de correlación, estados y payload reales; no construyas resultados COMPLETED en adapters ni uses el loopback como prueba integrada.

En el CP añade selección configurable del transporte local: Kafka conserva el standalone; HTTP permite el modo integrado. Puedes implementar `local.results.transport` y URLs configurables por tipo de resultado. **Son diseño de esta fase, no propiedades existentes hoy.** Usa qualifiers/wiring local; publishers intactos. Playmaker despacha sus triggers por HTTP mediante adapters locales, sin consumer/bridge Kafka nuevo si los endpoints bastan. No inventes políticas de retry de negocio; respeta ACK/errores de las interfaces y documenta timeouts y fallos del transporte. No uses delays para ocultar carreras de resultados antes del commit.

**5. Conservación de producción**

No cambies controllers, DTOs, validaciones, defaults, handlers, processors, provisioners, estados, errores, publicación ni idempotencia. Sin ramas "si local" dentro de los flujos. Reutiliza interfaces y DI; toda abstracción adicional debe ser estructural, justificar selección productiva sin cambios y pasar revisión independiente.

No registres providers que habiliten una capacidad ausente en producción. PEEK action GCP actualmente falla `FAILED/INVALID_PARAMS`, `reason=unmapped`, sin STARTED: preserva esa paridad y reporta el gap; no lo arregles en esta integración. No copies correcciones productivas del desarrollo congelado. Si aparece otra incompatibilidad o defecto, conserva el escenario/evidencia, declara FAIL/BLOCKED y continúa lo independiente. No cambies expectativas ni atribuyas éxito a HTTP200.

La autorización de usuarios y metadatos necesarios para fixtures debe usar mecanismos locales existentes conservando sus validaciones. Explicita qué fronteras externas se sustituyen; no certifiques ACME/Entity/OAuth/Fury como integrados. Si no existe seam compatible, reporta el bloqueo concreto.

**6. Pruebas obligatorias**

Usa JUnit/Gradle y dependencias existentes; unitarios de adapters/serialización/errores como complemento, nunca como acreditación E2E. Las pruebas integradas deben iniciar por APIs existentes de Playmaker, no enviar directamente al CP y llamarlo integración.

- PROVISION: request Playmaker, trigger real, STARTED→terminal según contrato, estado persistido Playmaker y tópico físico con nombre/particiones/RF1/configs explícitos.
- UPDATE: tópico creado por el flujo, cambio permitido, resultado procesado por Playmaker y cambio físico.
- DEPROVISION: eliminación solicitada desde Playmaker, resultado final y ausencia física; usa la entrada real de su lifecycle.
- ACTIONS/PEEK: mensajes Kafka deterministas con keys, action desde Playmaker y payload final observable con keys/mensajes/límite. Incluye cualquier otra action soportada por ambos repos que el código identifique; no supongas nombres.
- Al menos un error contractual por flujo; distingue rechazo inicial Playmaker de error CP propagado. Casos existentes/ausentes e idempotencia según código. Replays de trigger y callback deben usar IDs capturados de flujos reales, no resultados fabricados. Verifica que no duplican efectos ni estados terminales.
- Conserva la suite standalone25 del CP en modo Kafka y verifica su regresión después del cambio. No agregues otro CP simultáneo sólo para correr ambas suites.

HTTP200 es recepción: espera condiciones con deadlines y comprueba estado final Playmaker + resultado CP + Kafka físico. Sin sleeps fijos, expectaciones debilitadas ni SQL que construya el estado esperado. Los fixtures pueden preparar referencia local mínima; no pueden sustituir el procesamiento de negocio. Documenta matriz y exclusiones verdaderas.

**7. Repetibilidad, propiedad y limpieza**

Un comando documentado arranca ambos desde un clon/ruta cualquiera, incluso fuera de HOME y con espacios; otro prueba y otro elimina sólo recursos propios. Descubre recursos existentes antes de borrar. Usa nombres/IDs únicos por corrida y fixtures aislados. Limpia ante fallas y confirma eliminación física; detén consumidores antes de retirar la red del CP. Preserva estado/recursos ajenos y la VM.

Ejecuta la suite integrada completa dos veces seguidas contra el mismo ambiente vivo sin down, después destruye/recrea vacío y repítela. Otro agente reproduce desde clones limpios. Nunca ejecutes suites concurrentes contra el mismo ambiente. Guarda JUnit y logs necesarios fuera del diff, redactados; no framework de evidencia ni dumps masivos.

**8. Coordinación y criterio de terminado**

Manager integra build/config, mantiene un único registro corto de base/ramas/decisiones/archivos-responsables/comandos-resultados/bloqueos. Usa GPT-6 Luna inicialmente para generación acotada; Sol sólo para arquitectura/diagnóstico/revisión justificados. Si no están disponibles, informa el modelo real. Brief por agente: objetivo/exclusiones, rutas/SHAs, decisiones, archivos exclusivos, contrato y comando de entrega. Un escritor por archivo; no dupliques discovery; autor distinto del certificador.

Cumple los gates Playmaker vigentes de selección AT/impact, tests afectados, regresión y validación documental. Revisión final elimina lo que no sea necesario para estos dos procesos. No añadas CI nueva, ClickHouse, integraciones administradas ni aparato histórico. Avanza autónomamente hasta terminar; pregunta sólo por una definición imprescindible o permiso externo.

Entrega: rutas/ramas/SHAs y diff explicado, comandos simples, matriz PASS/FAIL/BLOCKED con evidencia final y física, corridas repetidas y reproducción independiente, limpieza y limitaciones. Deja ramas listas para revisión; no publiques otro PR ni merges sin autorización. No declares terminada la integración por compilar, ping o recepciónHTTP. Actualiza AGENTS OS por delta y cierra sólo cuando el usuario lo solicite.

## Fuentes

- Identidad Git/common-dir/remotes y estado de ambos worktrees leídos08/10; referencias remotas verificadas por `git ls-remote`.
- CP PR85 y su entrega aa19883; README local y suite funcional.
- Playmaker histórico acbda2f: AGENTS.md, local/02-real-e2e.sh, Compose, application-local-integration.yml, RealE2ePlaymakerConfiguration y controllers de resultados. Son pistas de extracción, no prueba de compatibilidad de develop44c2905.
