---
type: project
schema_version: 1
owner: "me"
root: true
status: "active"
priority: "P2"
area: "[[Meli]]"
parent:
sprint:
start: "2026-09-30"
due:
progress: 0
repo: "https://github.com/melisource/fury_rio-controlplane-kafka"
jira:
prs:
aliases: ["Kafka local real", "Ambiente local Kafka", "Control plane Kafka — Desarrollo local"]
tags: ["kind/project", "area/meli", "app/rio-controlplane-kafka"]
created: "2026-09-30"
updated: "2026-10-01"
---

# Kafka — Ambiente local con servicios reales

> [!info]+ Kafka — Ambiente local con servicios reales
> **Área:** [[Meli]] · **Estado:** active · **Owner:** Rodrigo · **Fase:** propuesta lista para iterar; implementación pendiente.

## 🎯 Objetivo

Levantar [[rio-controlplane-kafka]] y [[rio-playmaker]] en un ambiente de desarrollo que ejecute PROVISION, UPDATE, DEPROVISION y PEEK contra Kafka real, use KVS real de Fury Sandbox y muestre el resultado real en Playmaker. Automatizar la comprobación de esas capacidades para desarrollo y CI. Mantener los contratos y la lógica de negocio utilizados por las aplicaciones, con una matriz verificable de cobertura y de dependencias externas.

El resultado esperado es un comando de inicio documentado, configuración reproducible, servicios saludables y escenarios que demuestren el efecto físico sobre topics, mensajes y estado de orquestación. La comparación de implementaciones ya terminó y vive en [[Ambientes locales RIO — Comparativa de implementaciones]]; este proyecto conduce el cambio que se desprende de esa evidencia.

## 📊 Estado actual

- **Investigación terminada el 2026-09-30:** se contrastaron los siete control planes, Playmaker, Materializer y SDK Events con commits identificados. Fuentes y límites en [[Repositorios RIO — Ambientes locales (2026-09-30)]].
- **Base encontrada:** Playmaker ya tiene MySQL real y transporte Kafka real en `local,local-integration`. Su propia arquitectura declara pendiente un control plane real conectado. Kafka ya tiene Compose con un broker, pero su publicación local usa archivos y su KVS sin configuración funciona en modo degradado.
- **Recomendación:** extender esa base con tres brokers Apache Kafka en KRaft, el control plane real y KVS real de Fury en sandbox. Usar adaptadores locales de transporte y conexión que deleguen a los procesadores productivos. La configuración del SDK Toolkit con el sandbox debe demostrarse antes de dar por cubierta la idempotencia.
- **Alcance confirmado por el owner:** el CP debe funcionar completo localmente, incluido KVS, con pruebas automáticas. KVS real de Fury Sandbox está aceptado; el ambiente puede depender de conectividad corporativa. El backend KVS queda definido, y su configuración con el cliente Toolkit actual sigue por comprobar.
- **Estado de entrega:** propuesta documental lista; código, SPEC funcional, SPEC técnica y ramas de implementación todavía pendientes. Progreso de implementación: 0%.
- **Actualización de repos:** diez bases locales actualizadas con `git pull`: siete control planes, Playmaker, Materializer y SDK Events. Kafka y Playmaker se actualizaron desde worktrees limpios de sus ramas `develop` existentes, preservando ramas y cambios de los checkouts originales. ClickHouse volvió a su rama original después de actualizar su base. Las fuentes remotas examinadas coincidieron con los SHAs finales de esas bases.
- **Validación realizada:** investigación estática el 2026-09-30; prueba runtime parcial el 2026-10-01. La copia limpia falla en este Mac ARM por SIGILL del broker y falta de routing del CP. Con `JAVA_TOOL_OPTIONS=-XX:UseSVE=0` en el broker y routing AWS a localhost, ambos arrancan: `/ping` responde y PEEK devuelve cinco mensajes reales. Los resultados siguen a archivos y KVS sigue no-op. No se probaron deployments ni integración con Playmaker. Evidencia: [[Kafka local — Historia y prueba de arranque (2026-10-01)]].

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-controlplane-kafka]] · `melisource/fury_rio-controlplane-kafka` | Pendiente; todavía no creada | `develop@c9355395ef4b2bf438f0eb44528e24fa76ca498c` al investigar; refrescar antes de implementar | Pendiente | Pendiente | Propuesta; implementación no iniciada |
| [[rio-playmaker]] · `melisource/fury_rio-playmaker` | Pendiente; todavía no creada | `develop@f087e4b7cc185d93618de4bdeaeb76b53486ac47` al investigar; refrescar antes de implementar | Pendiente | Pendiente | Extensión del perfil existente; implementación no iniciada |

El flujo de entrega sigue Spellbook: SPEC funcional → SPEC técnica → tasks → implementación. Completar ramas y ambas SPEC antes de modificar código. Incluir otro repositorio en esta tabla sólo si el diseño demuestra que necesita un cambio.

## 🧩 Alcance propuesto

1. **Infraestructura compartida:** reutilizar el Compose de Playmaker y agregar un perfil o archivo para tres brokers, volúmenes, healthchecks y listeners internos/externos. Un comando levanta infraestructura y arranca las dos aplicaciones con versiones y puertos explícitos.
2. **Control plane real:** consumir los triggers locales con los DTO y validadores vigentes; delegar a los procesadores existentes; crear, actualizar y borrar topics mediante `AdminClient` real; publicar resultados a Kafka local con confirmación del broker.
3. **Conexión de datos:** habilitar una configuración local explícita hacia los brokers del Compose. El flujo GCP necesita desacoplar la obtención de `AdminClient` de la autenticación OAuth para ejecutar su provisioner real contra el cluster local. AWS ya tiene una fábrica plaintext. El perfil de integración debe evitar exigir una SA GCP sólo para administrar Kafka local.
4. **Acciones y PEEK:** extender el transporte local de Playmaker para acciones y conectar su cliente HTTP de PEEK al control plane. En `local` hoy siguen seleccionándose un productor de acciones no-op y un cliente PEEK que devuelve un mensaje sintético.
5. **Idempotencia real:** configurar un contenedor aislado de KVS Fury Sandbox con el SDK actual y probar create/CAS, versión, TTL, redelivery y reinicios. Validar primero la versión asignada por el servidor después de create, el conflicto de versiones y el incremento tras un update válido: el guard depende de esos comportamientos. No copiar identificadores de sandbox de KMS.
6. **Verificación automática:** escenarios de ciclo de vida, datos, replicación, routing y errores con evidencia en Kafka, KVS y MySQL, ejecutables mediante Gradle y en CI. Reservar una validación de integración con servicios reales no productivos para OAuth de GCP, transporte BigQueue y otras dependencias que Compose no reproduce.
7. **Disponibilidad verificable:** el launcher del perfil de integración debe comprobar Kafka y KVS real, rechazar wiring no-op/archivos y explicar qué configuración falta. Una dependencia corporativa ausente debe producir un fallo visible en las suites que la requieren. Las pruebas de caída posterior de un KVS real verificarán la política de degradación vigente del producto.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] Confirmar KVS real de Fury Sandbox y permitir la dependencia de conectividad corporativa #owner/me #type/research #area/meli
> - [ ] Comprobar el cliente Toolkit contra un sandbox propio y verificar create/CAS, versiones y TTL #owner/me #type/dev #area/meli
> - [ ] Identificar un runner de CI con Docker y acceso al KVS sandbox; documentar configuración y aislamiento por corrida #owner/me #type/dev #area/meli
> - [ ] Crear la SPEC funcional en Spellbook con la matriz de capacidades y los criterios de aceptación de esta nota #owner/me #type/dev #area/meli
> - [ ] Crear la SPEC técnica y verificar compatibilidad serializada entre `rio-sdk-events:1.5.0` de Playmaker y `1.3.1` de Kafka #owner/me #type/dev #area/meli
> - [ ] Definir las ramas y completar la tabla de entrega antes de implementar #owner/me #type/dev #area/meli
> - [ ] Implementar arranque compartido y configuración del control plane con Kafka real #owner/me #type/dev #area/meli
> - [ ] Conectar deployments completos y comprobar estado físico y resultado en Playmaker #owner/me #type/dev #area/meli
> - [ ] Conectar acciones/PEEK e idempotencia con KVS real #owner/me #type/dev #area/meli
> - [ ] Implementar suites Gradle de integración y E2E con servicios reales, reportes y cleanup #owner/me #type/dev #area/meli
> - [ ] Integrar la ejecución automática en PRs y verificar que una dependencia ausente produce fallo visible #owner/me #type/dev #area/meli
> - [ ] Ejecutar la matriz de aceptación, documentar brechas y entregar el comando reproducible #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-09-30** — Búsqueda y contraste de implementaciones vigentes completados; diez bases actualizadas; los checkouts originales de Kafka y Playmaker se preservaron usando worktrees limpios. Se creó esta iniciativa con la recomendación de extender `local-integration`, tres brokers y KVS sandbox real. Implementación pendiente de las SPEC y ramas.
- **2026-10-01** — Historia verificada: Compose creado el 25 de febrero y mergeado a develop el 2 de marzo de 2026. Arranque y PEEK reales comprobados con dos ajustes temporales de configuración. El warmup GCP sin credenciales avisa y permite arrancar; operaciones GCP pendientes. La prueba se hizo sin modificar los repos y sus procesos se retiraron. El ambiente completo sin mocks continúa pendiente.
- **2026-10-01** — El owner confirmó el requisito de CP completo localmente, incluido KVS y automatización, y eligió KVS real de Fury Sandbox. Se concretó una propuesta de suites JUnit/Testcontainers/Awaitility, cobertura y fases de entrega; configuración del SDK y disponibilidad del runner quedan como primeras comprobaciones técnicas.

## 🧭 Decisiones

- **Propuesta D1:** usar Docker Compose con Apache Kafka, MySQL y aplicaciones reales, extendiendo la integración ya existente de Playmaker. El código de negocio sigue siendo el de los control planes.
- **Propuesta D2:** tres brokers para cubrir RF 1–3, incluidos el default RF=2 de GCP y los cambios de replicación. Un broker puede ser una modalidad liviana posterior con cobertura declarada como parcial.
- **Decisión D3 — KVS confirmado:** usar KVS real de Fury Sandbox, con un contenedor propio para este ambiente. Mantener el cliente Toolkit usado por el CP. La compatibilidad concreta y el contrato de versiones/CAS/TTL quedan como comprobación técnica inicial. El owner acepta la dependencia de conectividad corporativa.
- **Propuesta D4:** separar la certificación funcional local de la validación de autenticación GCP y entrega BigQueue en un ambiente real no productivo. El transporte Kafka local conserva contratos de aplicación, pero tiene semántica distinta de BigQueue.
- **Propuesta D5:** automatizar con JUnit, Testcontainers y Awaitility, ya declarados en el CP, y tasks Gradle distintas para integración y E2E. Usar las mismas versiones, DTO y configuración de servicios que el ambiente de desarrollo. Mantener la suite unitaria existente.

## 🧪 Criterios de aceptación propuestos

| Capacidad | Evidencia requerida |
|---|---|
| Arranque | Un comando reproducible inicia las aplicaciones e infraestructura, espera disponibilidad y expone healthchecks útiles; reinicio conserva datos según la política elegida. |
| PROVISION | El topic aparece en Kafka con particiones, replicación y configuración solicitadas; Playmaker recibe el resultado correspondiente al mismo deployment. |
| UPDATE | Cambian particiones/configuración y replicación permitida; los campos omitidos se conservan; errores inválidos se reflejan como fallas reales. |
| DEPROVISION | El topic desaparece; repetir la operación conserva la semántica del handler vigente. |
| PEEK | Lee mensajes producidos realmente, por REST y por acción cuando corresponda; no altera offsets de un consumer group existente. |
| Redelivery y concurrencia | KVS real demuestra claim/CAS y deduplicación, incluido redelivery tras reinicio; no hay éxito sintético. |
| Routing y contratos | Se ejercitan los templates AWS/GCP y reglas vigentes de selección de cluster, usando fixtures locales explícitas; los DTO serializados de ambos repos son compatibles. |
| Fallas | Se ejercitan broker caído, publicación fallida, timeout, payload inválido y DLT; las brechas heredadas de ACK/asíncrono se documentan con resultado observable. |
| Automatización | Suites ejecutables localmente y en un runner de CI habilitado; cada corrida usa IDs/recursos aislados, espera condiciones observables, genera reportes y limpia sus recursos. La ausencia de Kafka o KVS requerido produce fallo explícito. |
| Autenticación/transporte administrados | OAuth GCP y BigQueue se validan contra servicios reales no productivos; la prueba local por sí sola no los certifica. |

### Automatización propuesta

| Suite | Servicios y cobertura | Momento de ejecución |
|---|---|---|
| Unitarias existentes | Reglas y casos aislados en JUnit; conservar la ejecución rápida actual | Desarrollo y cada PR |
| `realIntegrationTest` — task por crear | Kafka real administrado por Testcontainers y KVS Fury Sandbox; CP real, PROVISION/UPDATE/DEPROVISION, PEEK REST/acción, RF 1–3, create/CAS/TTL, redelivery, concurrencia, errores y resultados publicados al broker | Comando local y cada PR en runner con Docker y acceso al sandbox |
| `e2eTest` — task por crear | Playmaker + MySQL + CP + cluster Kafka real + KVS sandbox; request de deployment, efecto físico, evento de resultado y estado final de Playmaker; reinicios y fallas de integración | Comando local y cambios que afecten esos contratos; gate automático antes de entrega |

Cada escenario debe comprobar el efecto físico y el resultado correlacionado por IDs de la corrida. Un HTTP 200 de recepción asíncrona no basta para aprobar un deployment. Las suites reales deben ejecutar los handlers/provisioners de la aplicación, sin reemplazarlos por Mockito ni usar resultados sintéticos. Awaitility espera estados reales con timeout; se conservan logs y reportes JUnit/Gradle al fallar.

El sandbox se aísla por contenedor dedicado al ambiente y claves/IDs por corrida, según lo que soporte Fury. La limpieza se limita a los recursos creados por esa corrida. Ningún test debe borrar contenedores globales o datos de otro desarrollador. En CI, validar acceso a Docker y al sandbox antes de ejecutar; no marcar la suite como aprobada por un skip de infraestructura.

**Comandos objetivo, todavía no implementados:** `make local-up` inicia el ambiente y comprueba dependencias; `make local-test` delega a las suites Gradle; `make local-down` retira sólo recursos del ambiente. Los nombres y el launcher se fijarán en la SPEC técnica.

### BigQueue para desarrollo local

La documentación oficial de Sandbox Services lista BigQueue mediante comandos mock de Fury CLI. `fury services bigq mock send-msg` entrega un mensaje con formato BigQueue a un endpoint local; no demuestra una cola sandbox real con topics, consumers y redelivery. No cumple por sí solo el requisito de transporte real.

También está documentado `fury services bigq mock send-msg-consumer`, que reenvía mensajes desde un consumer BigQueue real de test hacia un endpoint local. Su paso `init` pausa el consumer de test. Es una alternativa por evaluar para usar el transporte real en pruebas; no se ejecutó ni se modificó ningún consumer durante esta consulta. La documentación revisada no demuestra un BigQueue sandbox provisionable equivalente a KVS.

Fuentes oficiales verificadas el 2026-10-01: [Sandbox Services, servicios soportados](https://github.com/melisource/fury_sandbox-services-docs/blob/961c80339f0b12cd0a88610f5af9edf79d58385f/docs/guide/sandbox_service.md) y [BigQueue CLI, Mock Message](https://github.com/melisource/fury_cli-services-docs/blob/2ae4d44d8750497cb36e1fa6f85aff62b03fa583/docs/guide/services/bigq.md#bigqueue-mock-message). Se contrastó el comando `send-msg` con la ayuda del CLI instalado.

### Orden de entrega propuesto

1. **Dependencias comprobadas:** configurar KVS sandbox con el Toolkit actual, demostrar su contrato y confirmar el runner de CI. La falta de acceso/configuración deja la suite real como no ejecutada y el pipeline falla con diagnóstico.
2. **CP local completo:** resolver arranque/routing/compatibilidad ARM, conexión real de ambos flujos Kafka, resultados al broker, acciones e idempotencia. Entregar el launcher y `realIntegrationTest` juntos.
3. **Playmaker y CI:** conectar el flujo completo con MySQL, crear `e2eTest`, comprobar contratos entre SDK 1.3.1/1.5.0 y automatizar los gates.
4. **Fallas y reinicios:** completar la matriz de recuperación, redelivery, concurrencia y persistencia, y documentar la validación adicional de OAuth/BigQueue en servicios no productivos.

## 🔗 Docs / Links

- [[Ambientes locales RIO — Comparativa de implementaciones]] — evidencia comparada, herramientas comunes, alternativas y recomendación.
- [[Repositorios RIO — Ambientes locales (2026-09-30)]] — commits y archivos fuente verificables.
- [[Kafka local — Historia y prueba de arranque (2026-10-01)]] — fecha de incorporación, fallas originales y prueba real de arranque/PEEK con configuración temporal.
- [Testcontainers — Kafka](https://java.testcontainers.org/modules/kafka/) — soporte oficial de contenedores Apache Kafka y listeners adicionales.
- [Gradle — Testing](https://docs.gradle.org/current/userguide/java_testing.html) — suites separadas y reportes de ejecución.
- [[RIO]] · [[rio-controlplane-kafka]] · [[rio-playmaker]] · [[rio-controlplane-kms]] · [[rio-sdk-events]].

## 💡 Ideas

- Si la operación diaria requiere trabajar sin VPN, evaluar después un backend local real para persistencia y locks, con su propio contrato de CAS/TTL. Esa alternativa requiere diseño adicional y no certifica las semánticas de Fury KVS.
