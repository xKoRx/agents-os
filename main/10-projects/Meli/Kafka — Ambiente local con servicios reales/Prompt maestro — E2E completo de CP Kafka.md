---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
sources: ["[[Kafka — Ambiente local con servicios reales]]", "[[Kafka local — Historia y prueba de arranque (2026-10-01)]]", "[[Ambientes locales RIO — Comparativa de implementaciones]]"]
last_verified: "2026-10-01"
confidence: high
aliases: ["Prompt Kafka E2E", "Prompt maestro CP Kafka"]
tags:
  - kind/resource
  - area/meli
  - app/rio-controlplane-kafka
created: "2026-10-01"
updated: "2026-10-01"
---

# Prompt maestro — E2E completo de CP Kafka

## Síntesis vigente

Prompt de ejecución para desarrollar y verificar la cobertura E2E completa de Kafka CP, con subagentes, servicios reales, casos reproducibles y actualización trazable de la knowledge library. Copiar el bloque siguiente al agente ejecutor.

## Prompt maestro — copiar completo

```text
Actúa como responsable técnico de construir un sistema E2E completo para rio-controlplane-kafka. Debes convertirte en experto del CP, implementar el ambiente y las pruebas, ejecutarlas con servicios reales y completar la documentación correspondiente. La prioridad es cubrir y verificar toda su funcionalidad. El tiempo necesario no es una razón para recortar el alcance. Optimiza tokens y coordinación conservando toda la evidencia necesaria.

1. OBJETIVO Y REPOSITORIOS

Trabaja sobre rio-controlplane-kafka. Investiga rio-playmaker, rio-sdk-events y los otros control planes RIO para reutilizar sus patrones de desarrollo local y testing. Decide con evidencia si conviene un módulo dentro del CP, un módulo E2E independiente o extender un harness existente. Explica la elección por cobertura, mantenimiento, aislamiento, reproducibilidad y alineamiento con RIO; después impleméntala.

Incluye obligatoriamente ads-signals-knowledge-library: audita toda la documentación relacionada con Kafka CP y sus fronteras relevantes, contrástala con código vigente y con lo que observes ejecutando, y corrige/incorpora las brechas verificadas. Entrega cambios concretos en la biblioteca.

Al comenzar, lee AGENTS.md y las skills aplicables de cada workspace. Resuelve rutas/repos desde el entorno; los repos suelen estar bajo ~/fuentes. Registra ramas, commits y estado de trabajo. Preserva modificaciones existentes y usa checkouts/worktrees limpios cuando corresponda. Actualiza las bases de forma segura. Respeta el flujo de SPEC funcional → SPEC técnica → tareas → implementación que aplique y deja cada repo/base/rama/SPEC identificado.

Distingue master canónico, develop y ramas de trabajo. La biblioteca exige evidencia del master canónico de GitHub para describir comportamiento vigente. Cita otras ramas como evidencia de implementación pendiente o histórica. No conviertas una propuesta en una afirmación de producción.

2. CONTEXTO INICIAL QUE DEBES REVALIDAR

El ensayo del 2026-10-01 usó develop@c9355395ef4b2bf438f0eb44528e24fa76ca498c. El repo traía Compose de un broker apache/kafka:3.9.0. En un Mac ARM el broker falló con SIGILL; con JAVA_TOOL_OPTIONS=-XX:UseSVE=0 funcionó. El CP compiló con Java 25, pero faltaba profiles/local/cloud-provider.json. Con routing AWS hacia localhost:9092 arrancó y PEEK devolvió cinco mensajes realmente publicados. Sólo quedaron comprobados arranque, ping y PEEK directo. Esos ajustes fueron temporales y no se incorporaron al repo.

El modo local observado usa LocalFileBigQueueClient para resultados y NoOpKvsClient para idempotencia. Eso no acredita el ambiente completo que debes entregar. El warmup GCP sin credenciales fue una advertencia no fatal; no se probaron operaciones GCP.

El backend de persistencia elegido por el owner es KVS real de Fury Sandbox, usando el cliente productivo. La dependencia de conectividad corporativa está aceptada. Debes demostrar compatibilidad del cliente Toolkit actual, creación exclusiva, versión asignada por servidor, CAS, incremento de versión y TTL. Usa recursos propios; no copies nombres ni configuración del sandbox de KMS.

Fury documenta comandos BigQueue mock para entrega local y un reenvío de mensajes de un consumer real de test. Ese reenvío requiere preparación que pausa el consumer de test. No asumas que existe un broker BigQueue sandbox provisionable equivalente al KVS. Verifica soporte vigente y emplea servicios BigQueue reales no productivos cuando pruebes ese transporte. Nunca pauses un consumer compartido ni uses las herramientas mock como evidencia de un E2E real.

3. ORGANIZACIÓN OBLIGATORIA CON SUBAGENTES

Usa múltiples subagentes con responsabilidades acotadas y coordinación explícita. Como mínimo, distribuye:
- Dominio: inventario exhaustivo del CP, contratos, estados, routing, handlers/provisioners, entradas/salidas y cobertura existente.
- Infraestructura: precedentes RIO/Playmaker, Kafka real, KVS sandbox, transportes, launchers, runner de CI y fallas reproducibles.
- Knowledge: auditoría de ads-signals-knowledge-library contra los mismos commits, gaps y actualizaciones documentales.
- Implementación de escenarios y revisión independiente: después de acordar los contratos, divide código/tests por archivos y asigna a un agente distinto la revisión/reproducción final.

Respeta la capacidad concurrente del entorno; ejecuta roles por tandas cuando haga falta. El coordinador integra hallazgos, verifica evidencia crítica y sigue siendo responsable de la entrega completa. Cada archivo tiene un solo escritor por fase. Evita tareas duplicadas y cambios concurrentes de build/configuración. Un autor no certifica solo su propio resultado.

Comparte un brief compacto con objetivo, commits, decisiones, archivos asignados y criterio de entrega. Usa contexto acotado para los hijos, artefactos comunes y resultados breves con referencias. No copies la conversación completa ni todo el repo a cada subagente. Reutiliza agentes cuando ayude a conservar conocimiento pertinente.

4. CONVIÉRTETE EN EXPERTO Y CONSTRUYE LA MATRIZ DE COBERTURA

Antes de diseñar escenarios, traza desde cada entrada hasta validación, routing, procesador, efecto Kafka, claim/finalización KVS y publicación del resultado. Inventaría endpoints, tipos de trigger/acción, DTO, estados, opciones, límites, defaults, ramas de proveedor, perfiles y errores. Revisa también código sin cobertura, features documentadas y diferencias entre SDKs de CP y Playmaker.

Produce una matriz versionada con: capacidad/feature ID, contrato, código y SHA, precondiciones, escenario OK, escenario de falla, efecto físico esperado, evento/estado esperado, evidencia, limpieza y estado de cobertura. La lista siguiente es mínima: amplíala con toda capacidad encontrada.

- Arranque y configuración: routing, perfiles, dependencia KVS real, brokers, health/readiness, restart, configuración ausente/inválida y selección correcta de adapters.
- PROVISION: nombres, particiones, replicación, configuración, defaults, routing/provider, topic existente, duplicación y parámetros inválidos.
- UPDATE: cambios permitidos de particiones/config/replicación, campos omitidos, valores inválidos, topic inexistente y errores de Kafka.
- DEPROVISION: borrado efectivo, repetición, topic inexistente y fallas según el contrato vigente.
- PEEK directo y por acción: mensajes/keys reales, offsets/particiones, EARLIEST/LATEST y opciones soportadas, límites, validación, topic ausente, timeout y broker inaccesible. Demuestra que no altera offsets comprometidos de un consumer existente.
- Triggers y resultados: parseo/envelopes, allowlists, correlación, payload inválido, entradas ignoradas/rechazadas, estados exitosos/fallidos, límites de resultado, publicación fallida, reintentos y DLT donde estén implementados.
- Idempotencia: create exclusivo, versión inicial leída del servidor, CAS válido y obsoleto, TTL, duplicación, dos workers, ownership/takeover, finalización y ventanas de fallo antes/después de publicar. No prometas exactly-once si el contrato no lo garantiza.
- Recuperación: reinicio del CP, persistencia, broker caído, KVS inaccesible, publicación fallida y redelivery; verifica la política productiva de degradación y su observabilidad.
- Integración Playmaker: solicitud → trigger → CP → efecto Kafka → resultado → estado final, incluyendo errores y compatibilidad real de DTO/versiones.
- Fronteras de autenticación/autorización y proveedores: prueba el contrato comprobable en el ambiente aislado y registra lo que dependa de gateway, OAuth o servicios externos. No inventes políticas de producto a partir de expectativas del test.

5. IMPLEMENTACIÓN DEL AMBIENTE Y DEL SISTEMA E2E

Usa Kafka real. El cluster debe cubrir los factores de replicación admitidos; la base analizada de GCP tenía default 2 y rango 1–3, por lo que un solo broker no basta. Fija imágenes/configuración, verifica ARM y el runner de CI, listeners, readiness, volúmenes y puertos. Empaqueta el routing y los requisitos de runtime para un arranque reproducible.

Usa el CP real y sus validadores, handlers, procesadores, provisioners y guard de idempotencia. Las adaptaciones de conexión/transporte deben conservar esa lógica y sus contratos. Los fixtures sintéticos de entrada están permitidos; mocks del negocio, resultados sintéticos, almacenamiento en memoria, KVS no-op y resultados a archivos no acreditan las suites reales.

Conecta resultados a un transporte real observable y la integración con Playmaker cuando corresponda. Un HTTP 200 de recepción asíncrona no demuestra éxito del deployment. Verifica efectos mediante clientes Kafka reales, resultados correlacionados, estado KVS y estado final de Playmaker.

Separa con nombres inequívocos dos alcances: E2E funcional local contra Kafka/KVS reales y pruebas de integración del proveedor/transporte administrado contra ambientes reales no productivos. Ejecutar negocio GCP sobre Kafka local no certifica OAuth GCP; Kafka como transporte local no certifica BigQueue. La entrega debe informar la evidencia y las brechas de cada familia, y la validación completa no puede declararse por una suite parcial.

Reutiliza JUnit, Testcontainers, Awaitility y Gradle si la inspección vigente confirma que siguen siendo el mejor encaje. Usa espera por condiciones con deadlines, recursos/IDs/namespaces por corrida, fixtures deterministas, cleanup en éxito y falla, logs redacted y reportes JUnit/Gradle. Automatiza startup, prueba y teardown con comandos documentados. Las tareas nuevas deben existir y funcionar, no quedar sólo propuestas.

Construye casos de falla reproducibles mediante entradas controladas y fallas de procesos/red de recursos propios. No perturbes servicios compartidos. Si descubres bugs del CP que impiden cumplir su contrato, deja regresiones y corrígelos con cambios acotados. No acomodes expectativas para convertir un defecto en éxito.

Integra las suites en CI con un runner que tenga Docker y acceso al sandbox/servicios requeridos. Demuestra la ejecución real del job o identifica el bloqueo externo preciso. Si falta una dependencia obligatoria, la suite/pipeline debe fallar claramente; no ocultes el problema con skip y un resultado verde.

6. ACTUALIZA ADS-SIGNALS-KNOWLEDGE-LIBRARY

Sigue su AGENTS.md y lectura progresiva: README → intent en docs/06-skills/context-packs.md → flujo/runbook → ficha del CP → feature IDs y contratos relevantes. Inspecciona sólo las fronteras necesarias del upstream/downstream ledger y su manifiesto de fuentes.

Audita responsabilidades, endpoints, schemas, estados, routing AWS/GCP, idempotencia, publishing, perfiles locales, límites de pruebas, troubleshooting, cobertura E2E y relación con Playmaker. Contrasta cada afirmación con fuente canónica o evidencia runtime identificada. Detecta ausencias, contradicciones, contenido stale y helpers presentados como escenarios completos.

Incorpora las correcciones verificadas, instrucciones reproducibles del nuevo sistema y un mapa capacidad→escenario→evidencia. Usa templates, links por SHA, last_verified y los índices/ledgers/runbooks/manifiesto que corresponda. Las nuevas capacidades aún en una rama de trabajo deben quedar identificadas con ese estado hasta su integración canónica. Ejecuta los validadores de la biblioteca. Entrega cambios concretos y un resumen de qué gaps quedaron resueltos o dependen de una decisión externa.

7. OPTIMIZACIÓN DE TOKENS SIN RECORTAR VERIFICACIÓN

Haz búsquedas dirigidas: primero rg --files/rg -l, después lee archivos/secciones seleccionadas. Excluye .git, build, caches, graphify-out y artefactos generados. Agrupa lecturas independientes; mantén secuenciales las decisiones y cambios dependientes. No vuelques dumps, classpaths, logs masivos ni árboles completos al contexto.

Mantén un único control del proyecto y artefactos de evidencia reutilizables. Guarda avances, decisiones, commits, pruebas y siguiente paso concreto antes de compactar/cambiar de fase. No repitas discovery ya resuelto. Reporta uso de tokens y coste sólo si la plataforma los expone; si no, declara desconocido. Optimiza la coordinación y las lecturas, conservando cobertura, reproducibilidad, razonamiento necesario y ejecución física de las pruebas.

8. CRITERIOS DE TERMINADO Y ENTREGA

Entrega:
- Decisión de arquitectura y matriz exhaustiva de cobertura.
- Ambiente reproducible y comandos efectivos de inicio/prueba/limpieza.
- Suites completas OK/falla, aislamiento por corrida y regresiones de bugs corregidos.
- Integración CI y evidencia de ejecución por escenario: commits, IDs mínimos, efecto Kafka, resultado y estado KVS/Playmaker cuando aplique.
- Cambios implementados en los repos necesarios y actualizaciones verificadas de la knowledge library; diffs/PRs de borrador según el workflow del entorno.
- Informe final con PASS, FAIL, BLOCKED y NOT_EXECUTED por capacidad, límites del alcance local/proveedor y comandos de reproducción.

Exige una revisión independiente que reproduzca desde un checkout limpio al menos la ruta completa y los casos críticos de falla; ejecuta también la suite completa y demuestra que detecta las fallas esperadas. Verifica aislamiento, limpieza y repetibilidad.

No cierres como completado con sólo ping, PEEK, un topic creado, código sin ejecutar o escenarios salteados. Cada capacidad requerida necesita evidencia. Si algo externo bloquea un gate, prepara todo el trabajo independiente, informa el bloqueo y la acción exacta necesaria, y deja la continuidad lista sin declarar éxito total.

Avanza autónomamente en lo autorizado. Resuelve decisiones técnicas mediante evidencia y revisiones. Pide una aclaración puntual sólo si falta una definición de negocio, una credencial/permiso imprescindible o autorización para una acción externa irreversible. Conserva trabajo existente y opera sobre recursos propios de sandbox/no producción. Mantén al owner informado con avances concretos y brechas reales.

Empieza por baseline y por distribuir discovery a los subagentes. Sigue hasta entregar el sistema implementado, probado y documentado.
```

## Evidencia y provenance

- Encargo explícito del owner: prompt maestro de ejecución con funcionalidad completa, casos OK/falla, expertise de Kafka CP, múltiples subagentes y uso eficiente de tokens.
- [[Kafka — Ambiente local con servicios reales]], [[Kafka local — Historia y prueba de arranque (2026-10-01)]] y [[Ambientes locales RIO — Comparativa de implementaciones]].
- `ads-signals-knowledge-library`, AGENTS.md consultado en `master@de7cde85f7dd83a673c918e22ae9f08a0f7e05bd`: lectura progresiva, fuente canónica y actualizaciones por SHA. El catálogo/context pack distingue helpers Kafka de escenarios E2E.

## Límites y contradicciones

- Este artefacto es un encargo para un agente futuro. La implementación E2E y las modificaciones de la knowledge library no se ejecutaron durante su preparación.
- Los hechos del ensayo inicial son un baseline fechado que el ejecutor debe revalidar. No sustituyen una verificación del código canónico actual ni una prueba completa.
