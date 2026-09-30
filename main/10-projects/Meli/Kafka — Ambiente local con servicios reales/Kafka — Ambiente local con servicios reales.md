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
updated: "2026-09-30"
---

# Kafka — Ambiente local con servicios reales

> [!info]+ Kafka — Ambiente local con servicios reales
> **Área:** [[Meli]] · **Estado:** active · **Owner:** Rodrigo · **Fase:** propuesta lista para iterar; implementación pendiente.

## 🎯 Objetivo

Levantar [[rio-controlplane-kafka]] y [[rio-playmaker]] en un ambiente de desarrollo que ejecute PROVISION, UPDATE, DEPROVISION y PEEK contra Kafka real y muestre el resultado real en Playmaker. Mantener los contratos y la lógica de negocio utilizados por las aplicaciones, con una matriz verificable de cobertura y de dependencias externas.

El resultado esperado es un comando de inicio documentado, configuración reproducible, servicios saludables y escenarios que demuestren el efecto físico sobre topics, mensajes y estado de orquestación. La comparación de implementaciones ya terminó y vive en [[Ambientes locales RIO — Comparativa de implementaciones]]; este proyecto conduce el cambio que se desprende de esa evidencia.

## 📊 Estado actual

- **Investigación terminada el 2026-09-30:** se contrastaron los siete control planes, Playmaker, Materializer y SDK Events con commits identificados. Fuentes y límites en [[Repositorios RIO — Ambientes locales (2026-09-30)]].
- **Base encontrada:** Playmaker ya tiene MySQL real y transporte Kafka real en `local,local-integration`. Su propia arquitectura declara pendiente un control plane real conectado. Kafka ya tiene Compose con un broker, pero su publicación local usa archivos y su KVS sin configuración funciona en modo degradado.
- **Recomendación:** extender esa base con tres brokers Apache Kafka en KRaft, el control plane real y KVS real de Fury en sandbox. Usar adaptadores locales de transporte y conexión que deleguen a los procesadores productivos. La configuración del SDK Toolkit con el sandbox debe demostrarse antes de dar por cubierta la idempotencia.
- **Estado de entrega:** propuesta documental lista; código, SPEC funcional, SPEC técnica y ramas de implementación todavía pendientes. Progreso de implementación: 0%.
- **Actualización de repos:** diez bases locales actualizadas con `git pull`: siete control planes, Playmaker, Materializer y SDK Events. Kafka y Playmaker se actualizaron desde worktrees limpios de sus ramas `develop` existentes, preservando ramas y cambios de los checkouts originales. ClickHouse volvió a su rama original después de actualizar su base. Las fuentes remotas examinadas coincidieron con los SHAs finales de esas bases.
- **Validación realizada:** inspección de código/configuración y contraste con documentación primaria. No se levantó el stack ni se ejecutaron pruebas de integración durante esta investigación. El lint estricto de las cinco notas versionadas tocadas pasó con 0 errores y 0 advertencias; Graphify recuperó el proyecto por título.

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
5. **Idempotencia real:** configurar un contenedor aislado de KVS Fury sandbox con el SDK actual y probar create/CAS, versión, TTL, redelivery y reinicios. Un fallback no-op o en memoria no satisface este criterio. No copiar identificadores de sandbox de KMS.
6. **Verificación:** escenarios de ciclo de vida, datos, replicación, routing y errores con evidencia en Kafka, KVS y MySQL. Reservar una validación de integración con servicios reales no productivos para OAuth de GCP, transporte BigQueue y otras dependencias que Compose no reproduce.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [r] Iterar la recomendación y acordar el alcance inicial, incluido KVS sandbox y las dependencias que requieren conexión corporativa #owner/me #type/research #area/meli
> - [ ] Crear la SPEC funcional en Spellbook con la matriz de capacidades y los criterios de aceptación de esta nota #owner/me #type/dev #area/meli
> - [ ] Crear la SPEC técnica y verificar compatibilidad serializada entre `rio-sdk-events:1.5.0` de Playmaker y `1.3.1` de Kafka #owner/me #type/dev #area/meli
> - [ ] Definir las ramas y completar la tabla de entrega antes de implementar #owner/me #type/dev #area/meli
> - [ ] Implementar arranque compartido y configuración del control plane con Kafka real #owner/me #type/dev #area/meli
> - [ ] Conectar deployments completos y comprobar estado físico y resultado en Playmaker #owner/me #type/dev #area/meli
> - [ ] Conectar acciones/PEEK e idempotencia con KVS real #owner/me #type/dev #area/meli
> - [ ] Ejecutar la matriz de aceptación, documentar brechas y entregar el comando reproducible #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-09-30** — Búsqueda y contraste de implementaciones vigentes completados; diez bases actualizadas; los checkouts originales de Kafka y Playmaker se preservaron usando worktrees limpios. Se creó esta iniciativa con la recomendación de extender `local-integration`, tres brokers y KVS sandbox real. Implementación pendiente de las SPEC y ramas.

## 🧭 Decisiones

- **Propuesta D1:** usar Docker Compose con Apache Kafka, MySQL y aplicaciones reales, extendiendo la integración ya existente de Playmaker. El código de negocio sigue siendo el de los control planes.
- **Propuesta D2:** tres brokers para cubrir RF 1–3, incluidos el default RF=2 de GCP y los cambios de replicación. Un broker puede ser una modalidad liviana posterior con cobertura declarada como parcial.
- **Propuesta D3:** usar el precedente híbrido de KMS para KVS Fury sandbox. Su compatibilidad concreta con Toolkit KVS queda como gate técnico; no hay evidencia de un servidor KVS Fury autocontenido en los repos revisados.
- **Propuesta D4:** separar la certificación funcional local de la validación de autenticación GCP y entrega BigQueue en un ambiente real no productivo. El transporte Kafka local conserva contratos de aplicación, pero tiene semántica distinta de BigQueue.

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
| Autenticación/transporte administrados | OAuth GCP y BigQueue se validan contra servicios reales no productivos; la prueba local por sí sola no los certifica. |

## 🔗 Docs / Links

- [[Ambientes locales RIO — Comparativa de implementaciones]] — evidencia comparada, herramientas comunes, alternativas y recomendación.
- [[Repositorios RIO — Ambientes locales (2026-09-30)]] — commits y archivos fuente verificables.
- [[RIO]] · [[rio-controlplane-kafka]] · [[rio-playmaker]] · [[rio-controlplane-kms]] · [[rio-sdk-events]].

## 💡 Ideas

- Si la operación diaria requiere trabajar sin VPN, evaluar después un backend local real para persistencia y locks, con su propio contrato de CAS/TTL. Esa alternativa requiere diseño adicional y no certifica las semánticas de Fury KVS.
