---
type: prompt
schema_version: 1
status: active
area: "[[Meli]]"
target: "Agente de desarrollo del CP Flink"
prompt_version: 1
inputs: ["Implementación standalone de CP Kafka", "Implementación standalone de CP ClickHouse", "Código y contratos vigentes de CP Flink"]
outputs: ["SPEC funcional y técnica", "Stack Flink Docker standalone", "Suite E2E física reproducible", "Evidencia y guía operativa"]
application: "[[rio-controlplane-flink]]"
project: "[[RIO E2E local]]"
aliases: []
related: ["[[rio-controlplane-kafka]]", "[[rio-controlplane-clickhouse]]", "[[RIO E2E local — Diseño revisado]]", "[[Prompt maestro — CP Flink E2E local]]"]
tags:
  - kind/prompt
  - project/rio-e2e-local
created: "2026-10-09"
updated: "2026-10-09"
---

# Prompt maestro CP Flink standalone E2E local

Implementar y certificar el control plane Flink contra un Flink real en Docker, siguiendo las implementaciones locales de Kafka y ClickHouse. Esta fase se ejecuta por sí sola. La integración con Playmaker corresponde a una fase posterior.

## Prompt para el agente

```text
Implementa Flink local standalone en rio-controlplane-flink y déjalo funcionando con pruebas E2E contra un Flink real en Docker. Debes basarte explícitamente en las implementaciones locales existentes de rio-controlplane-kafka y rio-controlplane-clickhouse: inspecciona sus archivos y reutiliza sus patrones antes de diseñar una solución nueva.

El objetivo es levantar el CP Flink y el motor Flink, enviar solicitudes a las APIs reales del CP, observar resultados correlacionados y comprobar directamente los jobs y sus efectos en Flink. Esta entrega debe funcionar sin Playmaker, frontend, CP Kafka ni CP ClickHouse ejecutándose. La integración con Playmaker y el transporte Kafka de triggers quedan para después.

1. Autoridad y forma de trabajo

Este pedido autoriza discovery, fetch de los repos necesarios, un checkout/worktree aislado, implementación, builds, pruebas y recursos Docker propios para completar esta fase local. Resuelve decisiones rutinarias y continúa hasta obtener una entrega ejecutable y verificada. La ejecución cloud, publicación de ramas/PRs y merges requieren un pedido posterior.

Respeta AGENTS.md y las reglas de seguridad/calidad de cada repo. En una sesión fría de AGENTS OS, resuelve VAULT_ROOT y ejecuta una sola vez 80-agents/skills/agents-os-bootstrap/SKILL.md; en una sesión warm usa routing y delta. Las skills canónicas se resuelven desde 80-agents/skills. Markdown es la fuente de verdad; Graphify es un índice. Conserva la sesión abierta.

Antes de editar, registra origin, rama, HEAD, base remota y cambios ajenos. Preserva los originales y usa un checkout aislado para Flink. Las referencias pueden tener trabajo sin commit: inspecciona ese contenido, registra su identidad y no lo descartes ni lo traslades en bloque. Verifica las refs actuales; los SHAs históricos de las notas no son una base vigente por defecto.

Sigue discovery → SPEC funcional → SPEC técnica/PLAN → tareas listas → implementación → verificación → correcciones. Documenta dentro del módulo canónico del repo que indiquen sus instrucciones. El objetivo incluye código y ejecución física; un diagnóstico, un PLAN o un spike por sí solos no completan esta tarea. Si aparece un bloqueo real, conserva evidencia, intenta alternativas dentro del alcance y explica exactamente qué acceso o cambio falta.

2. Referencias obligatorias

Repo objetivo:
/Users/rjara/fuentes/rio-controlplane-flink

Referencia Kafka:
/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-local

Lee al menos local/README.md, docker-compose.yml, Dockerfile.local, build.gradle y el código de src/local, src/localTest y src/localFunctionalTest. En particular:
- src/local/java/com/mercadolibre/rio_controlplane_kafka/local/LocalFunctionalAdaptersConfiguration.java
- src/local/java/com/mercadolibre/rio_controlplane_kafka/local/LocalInMemoryKvsClient.java
- src/local/java/com/mercadolibre/rio_controlplane_kafka/local/LocalKafkaBigQueueClient.java
- src/localFunctionalTest/java/com/mercadolibre/rio_controlplane_kafka/local/LocalKafkaFlowsTest.java

Extrae el patrón standalone: Compose con motor y CP, readiness, source sets locales, localBootJar/localTest/localFunctionalTest, sustitución de clientes externos bajo los publishers reales, IDs únicos, resultados correlacionados y comprobación física. Este checkout también contiene integración Kafka con Playmaker; selecciona lo necesario para el standalone, sin arrastrar el orquestador ni implementar listeners Kafka en esta fase.

Referencia ClickHouse:
/Users/rjara/fuentes/rio-controlplane-clickhouse

Lee README.md, local/README.md, local/VALIDATION.md, local/clickhouse_e2e.py, docker-compose.yml y las implementaciones BigQueueClientFactory, LocalFileBigQueueClient y KvsOwnershipService. Extrae el patrón API real del CP → resultado terminal correlacionado → efecto físico comprobado en el motor, además de fixtures y limpieza acotada. No copies límites accidentales del harness, nombres globales de containers ni dependencias entre tests.

Contexto del proyecto:
/Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/RIO E2E local/RIO E2E local.md
/Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/RIO E2E local/RIO E2E local — Diseño revisado.md

Lee únicamente el delta pertinente. El prompt histórico “Prompt maestro — CP Flink E2E local” describe una integración posterior con Playmaker; este pedido fija el alcance standalone actual.

En el discovery entrega una tabla breve: patrón observado en Kafka/ClickHouse, archivo de evidencia y adaptación elegida para Flink. “Me basé en ellos” sin inspección concreta no cumple esta exigencia. Si una ruta cambió, resuélvela desde la entidad/repos reales y registra la ruta vigente.

3. Resolver cómo el CP alcanzará el Flink local

Traza el flujo vigente completo: controller y DTO/SDK → guards/routing → processor → provisioning → artefacto/SQL → submit/start → monitor → resultado → cancel/deprovision. Inspecciona los processors AWS/GCP, handlers, factories KDA, GcpProvisioningStrategy, FlinkCloudAdapter, publishers reales/locales, KVS/idempotencia y la obtención de artefactos.

El antecedente observado es que el CP provisiona por AWS KDA o Fury Cloud Controller/Dataproc, y su publisher local solo registra logs. Revalida esto contra el código vigente. Esos clientes no empiezan a controlar un Flink Docker por cambiar una URL.

Diseña el seam mínimo que permita al flujo real del CP someter, observar y cancelar jobs en el runtime local. Puedes usar APIs nativas de Flink REST y SQL Gateway si corresponden a la versión/artefacto, con un adapter de provisioning seleccionado exclusivamente por el perfil local. Evalúa reutilizar el runner/artefacto rio-flink-sql y su contrato antes de crear otro ejecutor. Si requiere inspeccionar su repo, identifica la fuente y ref reales.

Conserva las APIs de entrada, DTOs, validaciones, correlación, idempotencia y construcción de resultados. Reutiliza código productivo hasta la frontera sustituida. Si necesitas extraer una interfaz o selector en src/main, justifica ese cambio pequeño y prueba que AWS/GCP conservan su comportamiento. Un adapter local puede sustituir infraestructura cloud; la ejecución del job y sus resultados deben provenir del Flink real.

Define tipos de componente y operaciones locales soportados. Como mínimo, resuelve un flujo flink-sql físicamente ejecutable y su DEPROVISION usando el contrato existente. Descubre la semántica de UPDATE/redeploy y de los estados antes de prometerlos. No fuerces equivalencias entre AWS y GCP; documenta qué caminos cloud siguen sin certificarse.

Fija versiones compatibles de Flink, Java del motor, Java del CP, runner SQL y conectores según el código y documentación primaria. Las JVM del CP y del motor pueden requerir versiones distintas. Registra tags/digests; evita latest. Demuestra temprano con un spike físico que el seam puede ejecutar y cancelar un job, y conviértelo después en implementación y regresión permanentes.

4. Stack y adaptadores locales

Entrega un Compose autocontenido con CP, JobManager, TaskManager y únicamente los servicios adicionales que necesite el seam demostrado, como SQL Gateway. Usa puertos configurables ligados a loopback, nombres de proyecto únicos, límites de recursos razonables y healthchecks que acrediten disponibilidad del motor y capacidad de ejecutar jobs.

El runtime local debe arrancar sin credenciales Fury/AWS/GCP ni acceso cloud. El build puede usar los repos Maven autorizados habituales. Resuelve storage/config/artefactos locales mediante fixtures explícitos; impide que los defaults locales terminen invocando servicios remotos.

Sigue el aislamiento de Kafka: código, recursos y dependencias específicos del entorno local en source sets/perfiles locales y un artefacto local separado. Verifica que bootJar productivo conserve su composición y no incluya adapters, configuración, fixtures o dependencias locales. Preserva los pins productivos y los checks de seguridad.

Para resultados usa el publisher productivo con una sustitución de transporte local en la frontera apropiada. Un cliente que capture JSON en archivos, como ClickHouse, permite esta fase sin broker. Los payloads deben conservar el contrato real y guardarse de forma atómica para que el test pueda correlacionarlos. El logger actual no basta como oráculo y el harness nunca fabrica COMPLETED/FAILED.

Si sustituyes KVS/locks, conserva las operaciones create/CAS/claim/finalize/TTL que el flujo requiere, siguiendo la implementación Kafka. Declara persistencia y coordinación realmente disponibles. Reemplazar claims por un “siempre OK” invalida las pruebas de idempotencia. Los job IDs deben ser IDs reales de Flink y relacionarse con los componentes/deployments en el estado del CP.

5. Pruebas E2E físicas

Usa el framework y tareas canónicos del repo, preferentemente el patrón JUnit localFunctionalTest de Kafka. Ejecuta un CP real y un Flink real; HTTP 200 significa recepción y debe complementarse con resultado terminal y oráculos físicos. Cada test prepara sus propios IDs/datos/recursos y limpia únicamente lo suyo.

La matriz mínima debe cubrir:
- Readiness del CP y del clúster, TaskManager registrado y slots disponibles.
- Un SQL enviado por el CP que procese datos de entrada conocidos y produzca salida física verificable: contenido/transformación/cantidad. SELECT 1 aislado no basta como aceptación.
- Provision de un job de streaming que alcance RUNNING y muestre progreso real; correlación entre deployment_id, resultado del CP y job ID de Flink.
- DEPROVISION por el CP que cancele ese job; resultado terminal correcto y estado físico terminal comprobado en Flink.
- SQL/params inválidos: error real y resultado coherente, sin job activo huérfano.
- Replay del deployment conforme al guard vigente: ausencia de un segundo job y de resultados terminales extra dentro de una ventana acotada declarada.
- Guards de tipo/schema/operación y rutas no soportadas con el comportamiento productivo observado.
- UPDATE/redeploy, stop/start o actions únicamente donde el contrato realmente los soporte, con efectos físicos comprobados; lista explícitamente el alcance pendiente.
- Una falla controlada del runtime propio: resultado/error/timeout reales y cleanup de jobs/claims según el contrato.
- Reinicio/recreación: verifica el comportamiento real del estado local, declara sus límites y demuestra una ejecución nueva desde un stack vacío.

Usa polling por condición con deadlines explícitos y diagnósticos de CP/Flink. Un timeout debe hacer fallar la suite; evita sleeps de estabilización. Obtén oráculos del runtime y de la salida del job, además de los eventos del CP. Un test que envía directamente SQL a Flink puede validar el seam durante el spike, pero no sustituye el caso E2E que entra por la API del CP.

Agrega pruebas focalizadas significativas para adapter, traducción de errores, estado/cancelación, captura de resultados y KVS. Ejecuta regresión productiva y checks requeridos por el repo. Reutiliza los gates de cobertura pertinentes de Kafka para el código local crítico; conserva umbrales existentes y explica exclusiones. No ajustes tests o contratos para obtener un verde artificial.

6. Operación reproducible y ownership

Entrega comandos simples para start, test y stop, y un comando completo que construya, levante un stack propio, espere readiness, ejecute la suite y limpie aun cuando falle, propagando el exit code. Mantén la posibilidad de repetir test sobre un stack vivo para uso manual. El runner debe funcionar desde cwd arbitrario y rutas con espacios.

Registra proyecto Compose, Docker context, IDs/labels y recursos creados. Selecciona explícitamente el mismo contexto para startup y cleanup, comprueba colisiones y disponibilidad antes de comenzar, y mide RAM/CPU/disco del stack. Revalida cualquier contexto Colima citado en notas históricas. Opera únicamente recursos del run; conserva containers, redes, volúmenes, imágenes y procesos ajenos. No uses prune global ni reinicies/redimensiones VMs compartidas.

Demuestra dos suites consecutivas en el mismo stack y otra ejecución desde recreación vacía. Verifica limpieza de jobs, archivos/fixtures, containers y volúmenes propios, y compara con el baseline. Si hay un verificador independiente disponible y autorizado por las reglas de la sesión, úsalo sobre un candidato congelado; registra su ref y evidencia. Cambios posteriores requieren repetir los gates afectados.

7. Entrega y criterio de terminado

Entrega código revisable en el checkout/branch aislado; SPEC y decisiones; Compose/Dockerfile/config/adapters; suite permanente; local/README.md con comandos, ejemplo de API/Postman, recursos y limitaciones; y VERIFICATION.md con matriz por caso, comandos exactos, refs, hashes del jar/imágenes, eventos correlacionados, job IDs/estados, datos de salida y cleanup.

PASS requiere que otro desarrollador pueda levantar únicamente este stack y ejecutar la suite para demostrar API del CP → job Flink real → datos procesados → resultado correlacionado → DEPROVISION físico. Un clúster encendido, mocks de SDK cloud, logs de COMPLETED o tests unitarios solos no satisfacen ese criterio.

Mantén la solución preparada para conectar Playmaker después mediante contratos y puntos de sustitución claros. La integración Kafka de triggers, cambios en Playmaker, frontend y orquestador multirrepo corresponden a la fase posterior. Esta certificación cubre CP Flink + Flink Docker; documenta aparte las diferencias con KDA/Dataproc y las demás fronteras sustituidas.
```
