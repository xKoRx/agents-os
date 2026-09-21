---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Aranea]]"
  - "[[Echo — Producto Integrado]]"
  - "[[Echo — Live Platform V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
  - "[[aranea-agent-dev]]"
  - "[[aranea-mcps-expert]]"
aliases:
  - Echo Forge environment contract
  - Echo DEV PROD contract
  - Ambientes Echo y Forge
tags:
  - kind/doc
  - area/echo
  - tech/environment
created: "2026-09-20"
updated: "2026-09-21"
---

# Echo + Echo Forge — Environment Contract

## Propósito

Fuente canónica **del límite DEV/PROD y del mapa de ambientes** de Echo y Echo Forge en Aranea. Lectura obligatoria al iniciar una sesión de cualquiera de los dos proyectos a través de [[aranea-agent-dev]], antes de acceder a infraestructura. También aplica a sesiones de investigación/review que puedan producir instrucciones de operación o despliegue. No es una SPEC de producto, un inventario general de Aranea, un runbook ni una autorización de ejecución.

**Corte de este documento: 2026-09-21** (reconciliación AS-BUILT Echo Core/Gateway DEV en Daedalus del 2026-09-21; el corte 2026-09-20 sigue siendo la base de las secciones no tocadas). Las asignaciones de destino expresan decisiones del owner; los estados físicos solo expresan evidencia identificada, con su propia fecha. **No se ha recibido ni validado aquí el reporte AS-BUILT de Hermes.** Nunca convertir una decisión TARGET, configuración escrita, servicio healthy, release o acceso MCP en `PHYSICALLY_VERIFIED` sin su smoke material. Frente a un runtime más reciente, reconciliar y actualizar este contrato antes de apoyarse en un dato desmentido; ninguna nota histórica autoriza una mutación.

## Contenido

### 1. Orden de autoridad y selección obligatoria

1. Resolver entidad/tarea: `Echo`, `Echo Forge` o ambas; no crear un tercer proyecto de integración. El padre es [[Echo — Producto Integrado]] y la ejecución pertenece a sus dos tracks.
2. Resolver ambiente **antes** de seleccionar host, credencial, capability MCP o comando. El ambiente predeterminado para desarrollo y pruebas es **DEV**; nunca inferir PROD por falta de DEV.
3. Identificar target exacto, instancia, identidad OS, rol/capability, recursos lógicos, ownership de jobs y alcance de la operación. Validar el estado físico actual mediante mecanismo autorizado.
4. Cargar [[aranea-mcps-expert]] y el runbook específico **solo si la tarea necesita MCP u operación**. Esta nota no concede poderes adicionales.
5. Si ambiente, target, credenciales, separación de colas, licencia, configuración o datos contradicen la fuente o no se demuestran: **bloquear únicamente la mutación afectada** (`ENVIRONMENT_UNRESOLVED` / `BLOCKED_DEV_INFRA`), registrar evidencia y continuar trabajo independiente. No recurrir a PROD ni ampliar privilegios para sortearlo.

**PROD:** observación únicamente bajo perfiles RO vigentes. Cualquier mutación, release, despliegue, reinicio, campaña, configuración, activación económica u orden requiere el gate del owner y el runbook/contrato específico. Una `approvalPolicy=auto` del MCP no es autorización humana. DEV no da permiso sobre infraestructura compartida activa. El paso a dinero real siempre tiene autorización owner independiente.

### 2. Topología objetivo DEV — decisiones del owner; no certificación AS-BUILT

| Componente | Destino objetivo | Estado físico de esta decisión |
|---|---|---|
| Workspace, coding agents, builds, Echo Core y Gateway DEV, componentes auxiliares requeridos, Forge Go | **Daedalus** | **AS-BUILT parcial 2026-09-21** (ver §5.1): Gateway DEV `RUNNING / PHYSICALLY_VERIFIED` (health, restart, kill-recovery); Core DEV `BLOCKED` por drift de credencial PostgreSQL DEV (owner); sin unidades de sistema (sin root interactivo) se usó `systemd --user` de `kor` con linger demostrado. |
| SQX DEV y plugins/worker de investigación rápida | **Daedalus**, preferencia por instalación nativa | `TARGET / FEASIBILITY_AND_AS_BUILT_PENDING`: licencia, recursos, plugin, proceso y job real pendientes de evidencia. Si resulta inviable, alternativa DEV autorizada y documentada; no nueva VM por inercia. |
| MT4/MT5, MetaEditor, Strategy Tester y MT5 worker DEV | **Windows `192.168.31.132`**, nombre lógico `dev-win`; clon designado de `mt5-win` | `OWNER_DESIGNATED / ISOLATION_AND_AS_BUILT_PENDING`: no asumir SSH, perfiles MCP, worker, cuenta demo ni backtest habilitados hasta smoke real. |
| PostgreSQL, Hasura, Kafka, Flink/StateFun, MongoDB y dependencias efectivas | Instancias **DEV ya existentes** en Aranea, no duplicarlas en Daedalus | Inventario y capacidades documentadas; cada consumidor debe demostrar endpoint/recurso DEV y conectividad actual. |
| Workers SQX/MT5 actuales de Zeus, Hera y Kronos | Recursos **compartidos actualmente entre DEV y PROD**, según owner | `SHARED / ISOLATION_NOT_INFERRED`: preservar jobs activos, releases, locks y procesos; no reiniciar, drenar, actualizar ni intervenir sin autoridad propia. |

La topología define objetivos, **no** autoriza que un clon Windows arranque automáticamente tareas heredadas. Verificar y neutralizar en `dev-win`, sin tocar la VM original, cualquier identidad, host key, tarea, servicio, Stager, worker, terminal, conexión, credencial de broker o autostart productivo antes de habilitarlo. Cuenta real y órdenes reales prohibidas en DEV; cuenta demo solo si autorizada y verificada. Credenciales/llaves privadas únicamente en stores autorizados, nunca en el vault.

### 3. Estado histórico conocido PROD — verificar antes de actuar

| Superficie | Evidencia documental y fecha | Límite |
|---|---|---|
| Echo Core / Gateway | Matriz [[Echo — Access & Physical Capability Matrix]]: procesos PROD observados en host `.71` al **2026-09-15**. | **Snapshot histórico**; no afirmar que siguen ejecutándose hoy sin lectura nueva. Perfil `echo-runtime-prod` viewer RO; no restart/deploy. |
| Echo Bridge | La misma matriz registra `NOT_DEPLOYED` al **2026-09-15**. | No inferir su estado presente ni arrancarlo en PROD. |
| SQX Linux y MT5 workers Zeus/Hera/Kronos | [[aranea-ssh-mcp]] describe perfiles y permisos de esa flota, y el owner indica uso compartido actual. | No equivalen a workers exclusivos DEV. La autoridad del profile y del SO se verifica por separado. |
| PostgreSQL/Mongo/Hasura PROD | [[aranea-mcps-expert]] y sus runbooks definen perfiles RO y alcance. | Sin DML/DDL, credenciales RW, mutaciones indirectas o fallback desde DEV. |
| Kafka/Flink PROD y otras capacidades | Revisar inventario actual de [[aranea-mcps-expert]]; nombres planeados no prueban capabilities desplegadas. | No reutilizar capacidades DEV para operar PROD. |

El mapa PROD detallado de hosts, releases, datasets, terminales y cuentas se completa exclusivamente a partir de despliegues/runtime y evidencias verificadas. `UNKNOWN` no significa ausente ni autoriza descubrirlo mediante una mutación.

### 4. Matriz de aislamiento por recurso

| Recurso | Exigencia DEV |
|---|---|
| PostgreSQL / Hasura | Base, esquema, metadata, roles y migraciones autorizados para DEV; nunca ejecutar DDL de aplicación con un perfil que no lo permite. |
| MongoDB Forge | Target/DB/colecciones e identidad RW DEV autorizadas; no escribir en Mongo Forge PROD. |
| Kafka | Brokers/topics, consumer groups, productores y políticas DEV identificados; prohibido registrar un consumidor en grupo productivo. |
| Flink/StateFun | Jobs, endpoints y configuración DEV; usar capability Flink DEV para control y autoridad SSH de host DEV para Docker cuando corresponda. |
| Temporal | Namespace `sqx-dev` existente en inventario documentado; verificar al ejecutar el namespace real, task queues exclusivas, workflow IDs y workers antes de registrar consumidores o iniciar jobs. `aranea-temporal-ro` no autoriza start/cancel. |
| MinIO | Buckets o prefijos DEV concretos y autorización específica; nunca usar amplitud de una capability RW como permiso para tocar objetos PROD o backups. |
| etcd | Prefijos, leases, locks y owner DEV exclusivos; nunca competir con lock productivo ni saltar el access plane. |
| MT4/MT5 | Terminal portable/data directory/worker/artifacts/cuenta demo DEV separados. Una VM clonada no demuestra separación. |
| SQX | Instalación, licencia, plugins, datasets, worker identity y artefactos DEV verificables; no reemplazar JAR en flota compartida para probar desarrollo local. |
| Runtime integrado | Worktrees por agente; un único owner/lock operativo para cambios al runtime DEV compartido y pruebas físicas en curso. |
| Secrets | Solo referencias a stores/identidades/perfiles; ninguna contraseña, bearer, token o llave privada en este documento ni en `AGENTS.md`. |

Los nombres exactos de endpoints, colas, topics, buckets y rutas operativas deben registrarse tras inspección en el inventario AS-BUILT o el runbook propietario, **no inventarse en esta matriz**. Los mecanismos existentes prevalecen sobre wrappers nuevos; no instalar infraestructura duplicada.

### 5. Certificación del ambiente, no del producto

Estados por componente: `TARGET` (decisión), `CONFIGURED` (configuración aplicada), `RUNNING` (proceso/servicio observado), `PHYSICALLY_VERIFIED` (smoke real con fecha y evidencia), `UNKNOWN` (sin evidencia vigente), `BLOCKED` (impedimento demostrado). No comparar estos estados con la taxonomía de implementación/release/certificación del producto.

**Gates mínimos del AS-BUILT de Hermes:**

- Identidad del clon, separación de la VM original y negativos de PROD; clave SSH de host propia y perfiles `dev-win`/`dev-win-operator` comprobados desde el consumidor real.
- Echo Core y Gateway DEV compilados, arrancados y capaces de acceder a las dependencias DEV; puertos, logs, health, arranque y recuperación evidenciados.
- Forge Go y SQX DEV (o alternativa explícita) con build/plugin/worker, fixture y resultado real.
- MT5 DEV con compilación MQ5→EX5, Strategy Tester, HTM, SHA256 y destino de resultados DEV.
- Smoke de conectividad/handoff de infraestructura; no declarar F-04/E-04/E-06 ni cross-lane `CERTIFIED` por una prueba de infraestructura.
- Evidencia de que los workers compartidos y PROD quedaron intactos; todo componente no verificado permanece pendiente.

El resultado físico de cada gate debe incluir fecha UTC, target, caller/superficie, commit y SHA de binario cuando apliquen, configuración sanitizada, operación ejecutada, salida y negativo/rollback pertinente. `IMPLEMENTED != CERTIFIED`; la certificación funcional pertenece a [[Echo + Echo Forge — Deferred Certification Backlog]].

### 6. Lectura y operación para cada sesión

- **Cold start o cambio de entidad a Echo/Forge:** `agents-os-bootstrap` → router `aranea-agent-dev` → leer este contrato **antes de elegir ambiente o actuar**. No añadirlo al stack global ni cambiar el bootstrap.
- **Warm turn de la misma sesión:** reutilizarlo; leer solo el delta cuando cambió la fuente, cambió el ambiente o existe evidencia de drift.
- **Entrada directa por `AGENTS.md` de repositorio:** debe remitir a este contrato; la federación en los repos es un cambio separado de la presente edición Agents-OS.
- **Operaciones:** seguir [[aranea-mcps-expert]] y el runbook del recurso; verificar permisos reales, preflight, blast radius, rollback y postcondición. No convertir este contrato en manual de comandos.
- **Si el contrato no está disponible:** lectura/investigación local permitida; mutaciones de infraestructura bloqueadas hasta recuperar ambiente y autoridad.

### 7. Reconciliación pendiente

| Punto | Estado a este corte | Acción de actualización |
|---|---|---|
| Reporte final Hermes `dev-win` | No recibido aquí | Incorporar host/identidad, claves host sanitizadas, profiles, smokes y fecha. |
| Core/Gateway/Forge sobre Daedalus | Target owner; no certificado aquí | Registrar source, servicios reales, endpoints DEV, health y resultados. |
| SQX local / Windows MT5 | Target owner; no certificado aquí | Registrar instalación/licencia permitida, worker, tests, HTM y aislación. |
| Mapa PROD actual | Snapshot parcial de 2026-09-15 | Leer deployment/runtime actual RO antes de cualquier decisión operacional. |
| Repositorios Echo y Symphony `AGENTS.md` | Fuera del alcance de esta escritura | Añadir puntero breve al contrato en cambio independiente; retirar credenciales versionadas mediante gestión segura y rotación correspondiente. |

## Fuentes

- [[Echo — Producto Integrado]] — ownership de dos tracks y semántica de certificación.
- [[Echo — Access & Physical Capability Matrix]] — estado histórico Echo, reconciliación 2026-09-15.
- [[Daedalus — Development Agents MCP Access & Gaps]] — capacidades MCP y fecha de sus certificaciones, no runtime Echo/Forge.
- [[aranea-agent-dev]], [[aranea-mcps-expert]], [[aranea-ssh-mcp]] — router, selección y límites de acceso.
- [[Echo + Echo Forge — Deferred Certification Backlog]] — gates funcionales pendientes; no es un inventario de ambientes.
- `xKoRx/echo:AGENTS.md` y `xKoRx/symphony:AGENTS.md` — portales de repositorio (sin copiar credenciales).
- Decisiones expresas del owner en esta conversación, 2026-09-20: Daedalus DEV, Windows `192.168.31.132`, workers compartidos y documentación AS-BUILT posterior a Hermes.
