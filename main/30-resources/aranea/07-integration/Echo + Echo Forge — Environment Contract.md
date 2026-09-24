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
  - "[[Echo Forge — Operación Real V2]]"
aliases:
  - Echo Forge environment contract
  - Echo DEV PROD contract
  - Ambientes Echo y Forge
tags:
  - kind/doc
  - area/echo
  - tech/environment
created: "2026-09-20"
updated: "2026-09-24"
---

# Echo + Echo Forge — Environment Contract

## Propósito

Fuente canónica **de los modelos de ambiente de Echo y Echo Forge** en Aranea: Echo mantiene separación `DEV / PROD`; Echo Forge tiene **un solo ambiente operacional** (§0). Lectura obligatoria al iniciar una sesión de cualquiera de los dos proyectos a través de [[aranea-agent-dev]], antes de acceder a infraestructura. También aplica a sesiones de investigación/review que puedan producir instrucciones de operación o despliegue. No es una SPEC de producto, un inventario general de Aranea, un runbook ni una autorización de ejecución.

**Corte de este documento: 2026-09-24** (corrección del owner: modelos de ambiente por producto, §0; secciones con conclusiones derivadas del modelo anterior marcadas `SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION`). Corte previo 2026-09-21T03:38Z (AS-BUILT Core/Gateway DEV + recertificación + recovery source + **deploy Gateway `2360369c` e ingestión DEV funcional**; el corte 2026-09-20 sigue siendo la base de las secciones no tocadas). Las asignaciones de destino expresan decisiones del owner; los estados físicos solo expresan evidencia identificada, con su propia fecha. **No se ha recibido ni validado aquí el reporte AS-BUILT de Hermes.** Nunca convertir una decisión TARGET, configuración escrita, servicio healthy, release o acceso MCP en `PHYSICALLY_VERIFIED` sin su smoke material. Frente a un runtime más reciente, reconciliar y actualizar este contrato antes de apoyarse en un dato desmentido; ninguna nota histórica autoriza una mutación.

## Contenido

### 0. Modelo de ambientes por producto — decisión del owner (2026-09-24, rige sobre todo lo precedente)

**Echo y Echo Forge NO comparten el mismo modelo de ambientes.** Esta decisión del owner corrige el modelo conceptual anterior y tiene autoridad sobre cualquier conclusión de este documento (incluidas §1, §2, §4, §5 y §7) que derivara de proyectar la separación DEV/PROD de Echo sobre Forge. Donde un texto anterior exija para Forge un DEV (SQX DEV, worker Forge DEV, `dev-win`), ese requisito queda `SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION`.

- **Echo = `DEV / PROD`.** Conserva su separación y todas sus reglas de aislamiento (§2–§4, lado Echo) salvo contradicción material. Para Echo, DEV es el ambiente de desarrollo y pruebas y PROD nunca es fallback.
- **Echo Forge = un solo ambiente operacional.** Toda prueba física, campaña, certificación y validación real de Forge se ejecuta sobre su infraestructura operacional existente, actualmente tratada/configurada como `production`. No se construye una separación DEV/PROD artificial para Forge.
- **Runtime operacional Forge (AS-BUILT desde fuentes existentes):** SQX instalaciones/workers en **Zeus** (`sqx-zeus`, `192.168.31.101`), **Hera** (`sqx-hera`, `192.168.31.111`) y **Kronos** (`sqx-kronos`, `192.168.31.121`, VM 111); worker Windows **worker-kronos** (VM 135, perfiles `mt5-kronos` / `mt5-kronos-operator`) para las capacidades Windows/MT5; y las dependencias persistentes del runtime real: prefijos ETCD production de flota (`/sqx-worker/production/`, `/sqx-watcher/production/`, seleccionados por `ENV=production`), Temporal de flota (namespaces `sqx`/`sqx-prop`, cola `sqx-main-queue`), MinIO `192.168.31.92:9000`, PG `192.168.31.220` (`trading_systems`/`trading_systems_test`), Mongo `forge`. Fuentes: [[aranea-ssh-mcp]], [[echo-forge-workers-shared-access]], [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]], bitácoras de [[Echo Forge — Import Task V1]] y de [[Echo Forge — Operación Real V2]]. No se inventan hosts ni procesos no respaldados; los estados físicos se revalidan en ventana antes de operar.
- **Para Forge NO existe:** obligación de construir `SQX DEV` en Daedalus, de crear un worker Forge aislado en Daedalus, de habilitar `dev-win` para certificar Forge, ni bloqueo de Campaign 001 por falta de licencia SQX en Daedalus. **Daedalus** sigue siendo workspace, host de coding agents, host de builds y herramientas auxiliares (incluido el screen `deployer`, `ENV=production` desde 2026-09-17); NO es el runtime SQX/MT5 canónico de Forge.
- **`ENV=production` de Forge es el ambiente operacional esperado**, no un error, fallback, leak, defecto ni `unsafe PROD mutation` automático. La seguridad se determina por el scope de Forge y el ownership del recurso, no exigiendo un `development` paralelo por aplicación.
- **Aislamiento dentro del ambiente único:** los candidatos de campaña se aíslan por cola/prefijo/instancia candidate-local sin tocar la flota activa — patrón certificado en el G7 físico de [[Echo Forge — Import Task V1]] (cola exclusiva en `sqx-dev`, prefijos ETCD propios, copia SQX candidate-local, negativos de no-interferencia sobre flota y ETCD production). El ownership de jobs y la ventana sobre recursos de flota compartida se siguen respetando.
- **Dinero real (inalterable):** que Forge opere en su ambiente `production` NO autoriza trading live, cuentas reales, órdenes económicas ni cambios destructivos; esas autorizaciones siguen siendo gates owner independientes. Forge fabrica y valida estrategias; “Forge production” no es permiso financiero.

### 1. Orden de autoridad y selección obligatoria

1. Resolver entidad/tarea: `Echo`, `Echo Forge` o ambas; no crear un tercer proyecto de integración. El padre es [[Echo — Producto Integrado]] y la ejecución pertenece a sus dos tracks.
2. Resolver ambiente **antes** de seleccionar host, credencial, capability MCP o comando, según el modelo de §0: para **Echo**, el ambiente predeterminado para desarrollo y pruebas es **DEV** y nunca se infiere PROD por falta de DEV; para **Echo Forge**, el ambiente es su **operacional único** (production) y la resolución obligatoria es de target, scope y ownership dentro de ese ambiente, no de elección DEV-vs-PROD.
3. Identificar target exacto, instancia, identidad OS, rol/capability, recursos lógicos, ownership de jobs y alcance de la operación. Validar el estado físico actual mediante mecanismo autorizado.
4. Cargar [[aranea-mcps-expert]] y el runbook específico **solo si la tarea necesita MCP u operación**. Esta nota no concede poderes adicionales.
5. Si ambiente, target, credenciales, separación de colas, licencia, configuración o datos contradicen la fuente o no se demuestran: **bloquear únicamente la mutación afectada** (`ENVIRONMENT_UNRESOLVED` / `BLOCKED_DEV_INFRA`), registrar evidencia y continuar trabajo independiente. En Echo no se recurre a PROD ni se amplían privilegios para sortearlo; en Forge el bloqueo se resuelve dentro del ambiente operacional único (capacidad existente de Zeus/Hera/Kronos y worker-kronos según el stage), nunca construyendo un ambiente DEV paralelo ni tocando flota activa sin ownership.

**PROD (Echo):** observación únicamente bajo perfiles RO vigentes. Cualquier mutación, release, despliegue, reinicio, campaña, configuración, activación económica u orden requiere el gate del owner y el runbook/contrato específico. Una `approvalPolicy=auto` del MCP no es autorización humana. DEV no da permiso sobre infraestructura compartida activa. El paso a dinero real siempre tiene autorización owner independiente.

**Operacional (Forge):** ejecutar campañas, certificaciones y validaciones físicas de Forge sobre su ambiente operacional único (§0) es el uso normal del sistema, no una mutación PROD a justificar. Lo que sigue gated: intervenir recursos de flota activa (reinicios, drenes, reemplazo de releases/instalaciones compartidas, keys y datasets de flota) exige ownership/ventana propia; y trading live, cuentas reales u órdenes económicas exigen autorización owner independiente (§0).

### 2. Topología objetivo DEV (track Echo y workspace/builds) — decisiones del owner; no certificación AS-BUILT; el runtime operacional de Forge se rige por §0

| Componente | Destino objetivo | Estado físico de esta decisión |
|---|---|---|
| Workspace, coding agents, builds, Echo Core y Gateway DEV, componentes auxiliares requeridos, Forge Go | **Daedalus** | **AS-BUILT completo 2026-09-21** (ver §5.1): Core y Gateway DEV `RUNNING / PHYSICALLY_VERIFIED` (health, restart, kill-recovery; PG DEV conectada tras rotación de credencial por owner); sin unidades de sistema (sin root interactivo) se usó `systemd --user` de `kor` con linger demostrado. |
| SQX DEV y plugins/worker de investigación rápida | ~~**Daedalus**, preferencia por instalación nativa~~ → **SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION (2026-09-24, §0)** | La premisa “SQX DEV en Daedalus” quedó sin efecto: no hay requisito de SQX, licencia ni worker Forge DEV en Daedalus; Forge ejecuta sus validaciones sobre su flota operacional (§0). El prework de 2026-09-24 (§5.8) se realizó bajo la premisa corregida y se conserva como evidencia histórica del runtime candidato, no como requisito. |
| MT4/MT5, MetaEditor, Strategy Tester y MT5 worker DEV | **Windows `192.168.31.132`**, nombre lógico `dev-win`; clon designado de `mt5-win` | **Vigente sólo como decisión del track Echo.** Para Forge NO es requisito (SUPERSEDED como requisito Forge): la validación MT5 de Forge corre en el worker Windows **worker-kronos** del ambiente operacional (§0), hoy asociada al stage C6. Para Echo sigue `OWNER_DESIGNATED / ISOLATION_AND_AS_BUILT_PENDING`: no asumir SSH, perfiles MCP, worker, cuenta demo ni backtest habilitados hasta smoke real. |
| PostgreSQL, Hasura, Kafka, Flink/StateFun, MongoDB y dependencias efectivas | Instancias **DEV ya existentes** en Aranea, no duplicarlas en Daedalus | Inventario y capacidades documentadas; cada consumidor debe demostrar endpoint/recurso DEV y conectividad actual. |
| Workers SQX/MT5 de Zeus, Hera y Kronos | **Runtime operacional de Echo Forge** (ambiente único, §0); para Echo permanecen fuera de DEV | Operables y certificados ([[aranea-ssh-mcp]]: operator 2026-09-13; releases Stager 0.2.98 observadas 2026-09-13; worker 0.2.105 con PID 1400507 en Kronos al 2026-09-22; G7 físico PASS 2026-09-23 en Kronos VM 111). Preservar jobs activos, releases, locks y procesos; no reiniciar, drenar, actualizar ni intervenir sin ownership/ventana propia. |

La topología define objetivos, **no** autoriza que un clon Windows arranque automáticamente tareas heredadas. Verificar y neutralizar en `dev-win`, sin tocar la VM original, cualquier identidad, host key, tarea, servicio, Stager, worker, terminal, conexión, credencial de broker o autostart productivo antes de habilitarlo. Cuenta real y órdenes reales prohibidas en DEV; cuenta demo solo si autorizada y verificada. Credenciales/llaves privadas únicamente en stores autorizados, nunca en el vault.

### 3. Estado histórico conocido PROD — verificar antes de actuar

| Superficie | Evidencia documental y fecha | Límite |
|---|---|---|
| Echo Core / Gateway | Matriz [[Echo — Access & Physical Capability Matrix]]: procesos PROD observados en host `.71` al **2026-09-15**. | **Snapshot histórico**; no afirmar que siguen ejecutándose hoy sin lectura nueva. Perfil `echo-runtime-prod` viewer RO; no restart/deploy. |
| Echo Bridge | La misma matriz registra `NOT_DEPLOYED` al **2026-09-15**. | No inferir su estado presente ni arrancarlo en PROD. |
| SQX Linux y MT5 workers Zeus/Hera/Kronos | [[aranea-ssh-mcp]] describe perfiles y permisos de esa flota; para Forge son su runtime operacional (§0). | Para Echo no equivalen a workers DEV (no se usan como atajo de desarrollo). La autoridad del profile y del SO se verifica por separado. |
| PostgreSQL/Mongo/Hasura PROD | [[aranea-mcps-expert]] y sus runbooks definen perfiles RO y alcance. | Sin DML/DDL, credenciales RW, mutaciones indirectas o fallback desde DEV. |
| Kafka/Flink PROD y otras capacidades | Revisar inventario actual de [[aranea-mcps-expert]]; nombres planeados no prueban capabilities desplegadas. | No reutilizar capacidades DEV para operar PROD. |

El mapa PROD detallado de hosts, releases, datasets, terminales y cuentas se completa exclusivamente a partir de despliegues/runtime y evidencias verificadas. `UNKNOWN` no significa ausente ni autoriza descubrirlo mediante una mutación.

### 4. Matriz de aislamiento por recurso

Alcance: esta matriz expresa exigencias del lado **Echo DEV** y de recursos compartidos. Para **Echo Forge** el modelo es el de §0 (ambiente operacional único con aislamiento de candidatos por cola/prefijo/instancia candidate-local), no la exigencia de un entorno DEV por recurso.

| Recurso | Exigencia DEV |
|---|---|
| PostgreSQL / Hasura | Base, esquema, metadata, roles y migraciones autorizados para DEV; nunca ejecutar DDL de aplicación con un perfil que no lo permite. |
| MongoDB Forge | Target/DB/colecciones e identidad RW DEV autorizadas; no escribir en Mongo Forge PROD. |
| Kafka | Brokers/topics, consumer groups, productores y políticas DEV identificados; prohibido registrar un consumidor en grupo productivo. |
| Flink/StateFun | Jobs, endpoints y configuración DEV; usar capability Flink DEV para control y autoridad SSH de host DEV para Docker cuando corresponda. |
| Temporal | Namespace `sqx-dev` existente en inventario documentado; verificar al ejecutar el namespace real, task queues exclusivas, workflow IDs y workers antes de registrar consumidores o iniciar jobs. `aranea-temporal-ro` no autoriza start/cancel. |
| MinIO | Buckets o prefijos DEV concretos y autorización específica; nunca usar amplitud de una capability RW como permiso para tocar objetos PROD o backups. |
| etcd | Prefijos, leases, locks y owner DEV exclusivos; nunca competir con lock productivo ni saltar el access plane. |
| MT4/MT5 | Terminal portable/data directory/worker/artifacts/cuenta demo DEV separados. Una VM clonada no demuestra separación. (Echo DEV; Forge usa el worker-kronos operacional, §0.) |
| SQX | Instalación, licencia, plugins, datasets, worker identity y artefactos DEV verificables; no reemplazar JAR en flota compartida para probar desarrollo local. (Echo DEV. Para Forge: la instalación/licencia/plugins/datasets de la flota operacional son los canónicos; candidatos con copia candidate-local y prefijos propios — patrón G7 —, nunca mutando flota.) |
| Runtime integrado | Worktrees por agente; un único owner/lock operativo para cambios al runtime DEV compartido y pruebas físicas en curso. |
| Secrets | Solo referencias a stores/identidades/perfiles; ninguna contraseña, bearer, token o llave privada en este documento ni en `AGENTS.md`. |

Los nombres exactos de endpoints, colas, topics, buckets y rutas operativas deben registrarse tras inspección en el inventario AS-BUILT o el runbook propietario, **no inventarse en esta matriz**. Los mecanismos existentes prevalecen sobre wrappers nuevos; no instalar infraestructura duplicada.

### 5. Certificación del ambiente, no del producto

Estados por componente: `TARGET` (decisión), `CONFIGURED` (configuración aplicada), `RUNNING` (proceso/servicio observado), `PHYSICALLY_VERIFIED` (smoke real con fecha y evidencia), `UNKNOWN` (sin evidencia vigente), `BLOCKED` (impedimento demostrado). No comparar estos estados con la taxonomía de implementación/release/certificación del producto.

**Gates mínimos del AS-BUILT de Hermes:**

- Identidad del clon, separación de la VM original y negativos de PROD; clave SSH de host propia y perfiles `dev-win`/`dev-win-operator` comprobados desde el consumidor real.
- Echo Core y Gateway DEV compilados, arrancados y capaces de acceder a las dependencias DEV; puertos, logs, health, arranque y recuperación evidenciados.
- ~~Forge Go y SQX DEV (o alternativa explícita) con build/plugin/worker, fixture y resultado real.~~ **SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION (2026-09-24, §0):** Forge no requiere SQX DEV; sus capacidades se demuestran sobre el ambiente operacional único (build/plugin/worker/fixture con resultado real en flota, como el G7 de [[Echo Forge — Import Task V1]]).
- MT5 DEV con compilación MQ5→EX5, Strategy Tester, HTM, SHA256 y destino de resultados DEV.
- Smoke de conectividad/handoff de infraestructura; no declarar F-04/E-04/E-06 ni cross-lane `CERTIFIED` por una prueba de infraestructura.
- Evidencia de que los workers compartidos y PROD quedaron intactos; todo componente no verificado permanece pendiente.

El resultado físico de cada gate debe incluir fecha UTC, target, caller/superficie, commit y SHA de binario cuando apliquen, configuración sanitizada, operación ejecutada, salida y negativo/rollback pertinente. `IMPLEMENTED != CERTIFIED`; la certificación funcional pertenece a [[Echo + Echo Forge — Deferred Certification Backlog]].

### 5.1 AS-BUILT Daedalus — Echo Core/Gateway DEV (2026-09-21, gate operativo de infraestructura; NO certifica producto ni join Forge→Echo)

Ejecutado por sesión ZCode/GLM sobre el host Daedalus (192.168.31.161, Ubuntu, usuario `kor` del grupo sudo sin root interactivo). No existía instalación Echo previa de Ariadna ni de nadie en Daedalus al comenzar (verificado: cero unidades systemd, cero binarios, cero procesos Echo); el único runtime Forge pre-existente es el screen `deployer` (`run_deployer.sh` con `ENV=production`, desde 2026-09-17) que quedó intacto. El gate entregado es de **ambiente**, no de producto: `RUNNING/PHYSICALLY_VERIFIED` aquí no implica `IMPLEMENTED/CERTIFIED` de ninguna feature.

- **Persistencia:** unidades `systemd --user` (`~/.config/systemd/user/echo-core-dev.service`, `echo-gateway-dev.service`), habilitadas en `default.target.wants`; `Linger=yes` para `kor` (loginctl + flag en `/var/lib/systemd/linger/`) ⇒ arranque al boot sin sesión SSH demostrado por mecanismo; **reboot físico NO ejecutado**. `sudo` sin contraseña no disponible ⇒ unidades de sistema quedan como mejora futura del owner.
- **Release layout:** `/home/kor/opt/echo-dev/releases/<sha>/` + symlink `current` + `/home/kor/opt/echo-dev/etc/*.env` (mode 600, sin secretos) + `BUILD.md` por release. Rollback = repoint de `current` + `systemctl --user restart` de ambas unidades; primer release ⇒ `ROLLBACK_DOCUMENTED`, no `ROLLBACK_TESTED`.
- **Baseline:** `xKoRx/echo` origin/master `5dd998f16aea7b2821f460188718d7a6d279829c` (worktree limpio, build workspace vía `go.work`), go1.27.1 linux/amd64, 2026-09-21T01:04Z. SHA256: echo-core `34f10782f406678a0593b2000dfd50f61f1ad854400781ed61100ed0df53f883`, echo-gateway `4022bcf45188f42cb730d02d1c4674149f9c23e44ada4efaa0ef98075942c757`.
- **Configuración DEV efectiva (sanitizada, fuente ETCD namespace `/echo/development/` leído por los binarios en runtime):** `ENV=development`; `ETCD_ENDPOINTS=http://192.168.31.250..254:2379` (explícito en EnvironmentFile); Core HTTP `:9090` (`HTTP_PORT`); Gateway `:8090` (`gateway/port`); `gateway/core_internal_url=http://localhost:9090`; PG DEV `192.168.31.220:5432/echo-develop` usuario `echo_user` schema `echo` (password vive en ETCD, nunca en unidades/vault); Kafka DEV `192.168.31.44:19091-19096`; OTEL DEV `192.168.31.45:4317`. El grupo `echo-core-v3` del source quedó demostrado como no-competitivo: los brokers del namespace DEV son el clúster Kafka DEV certificado y el namespace PROD apunta a `192.168.31.247-249:9092`; el grupo en DEV estaba `DEAD` con 0 miembros antes del arranque.
- **Core DEV:** `RUNNING / PHYSICALLY_VERIFIED` — ciclo completo reproducido (ETCD/Kafka/telemetría OK, `postgresql connected` a `192.168.31.220/echo-develop`, kache consumiendo `echo.account-configs.v1`, automation_evaluator con 5 perfiles, HTTP `:9090` optimizado, `started successfully`); `/health` 200 local y LAN; restart controlado y recuperación ante `SIGKILL` al MainPID verificadas (PG reconecta, health 200). El grupo `echo-core-v3` pasó a `STABLE` con **un único miembro** (`echo-core-kache-daedalus` desde `.161`, 5 particiones de `echo.account-configs.v1`) ⇒ sin competencia. `ENV=development` efectivo demostrado en journal (`etcd_prefix /echo/development/`).
- **Bloqueo previo y causa raíz (resuelto 2026-09-21 ~02:07Z):** el arranque inicial falló con `pq: password authentication failed for user "echo_user"` porque el valor de `/echo/development/postgres/password` en ETCD estaba sobrescrito con la credencial de prueba `test-postgres-password`. Causa raíz identificada en el repo: los **seed tests escriben a ETCD real sin guardas** — `v3/sdk/etcd/echo_seed_test.go` (`TestSeedEchoConfig_Development` línea 115 y `TestSeedEchoConfig_Production` línea 167) y el mismo patrón en `v1` (línea 97, dev) y `v2` (líneas 129/182, dev+prod) hacen `SetVar` del mapa completo, incluida `postgres/password`, sobre los namespaces `/echo/development/` y `/echo/production/` del clúster real; cualquier `go test ./v3/sdk/etcd/...` o `go test ./...` desde la raíz re-clobberiza **ambos ambientes**. Además `v3/sdk/postgres/scratch_query_test.go` mantiene la credencial versionada en un connStr. Owner rotó la credencial (misma en DEV y PROD) y corrigió ETCD; Core y Gateway reconectaron. **Pendiente owner/manager:** blindar o eliminar los seed tests (guard `testing.Short`/env gate o mover el seeding a script owner-only con password por env) y retirar credenciales versionadas del repo; mientras no se corrija, cualquier suite completa vuelve a romper la credencial de ambos ambientes.
- **Gateway DEV:** `active (running)`, `/health` HTTP 200, listeners `*:8090`; restart controlado y recuperación ante `SIGKILL` al MainPID verificados (nuevo PID, health 200, 1 scheduled restart en journal); `NRestarts` estable; journal sin fatales. Tras la rotación de credencial, el restart del Gateway mostró `PostgreSQL connected` y habilitó por diseño `automation handler` + `job scheduler` (antes degradados con warning). El boundary Forge ingest sigue `forge_ingest_misconfigured=true` ⇒ `/api/v1/forge/promotions` en fail-closed 503, tal como anticipa el contrato.
- **Dependencias verificadas desde Daedalus:** ETCD DEV PASS; Kafka DEV PASS (producer/consumers inician); PG DEV FAIL auth (ver bloqueo); OTEL providers inicializados con endpoint DEV (salud de export no afirmada). Puertos sólo en LAN 192.168.31.0/24 y overlay tailscale (sin IP pública; UFW disabled pero sin borde a Internet en el host). Cliente LAN: `http://192.168.31.161:8090/health` 200.
- **Wiring Flink/StateFun DEV:** `module.yaml` de `v3/core/deploy/flink-statefun/develop` apunta las functions a `http://dev.echo.core.lab.aranea:9090/statefun` y ese nombre resuelve a 192.168.31.161 ⇒ el diseño DEV ya espera el Core en Daedalus; ingress/egress del job son el clúster Kafka DEV. Con Core DEV arriba el job `StatefulFunctions` dejó el patrón de re-emisión cada ~75–80 s y sostuvo un mismo intento (mismo jid) con 28/28 tasks por >12 min; correlación fuerte con la disponibilidad del endpoint, confirmación final de estabilidad pendiente de observación más larga. No se tocó infra Flink.
- **Forge en Daedalus (inventario, sin iniciar nada):** binarios/CLIs del repo `xKoRx/symphony` (`cmd/symphony`, `sqx/cmd`, `deployer/cmd`); namespaces ETCD `/symphony/development/` (38 keys, sin `echo/ingest/*` ⇒ handoff DEV hacia Echo sin sembrar), `/deployer-watcher/development/` (watcher con config MinIO) y `/deployer/`. Ningún componente Forge fue autorizado con aislamiento demostrado para instalarse como servicio en Daedalus ⇒ `FORGE_RUNTIME_SCOPE_BLOCKED` para watcher DEV, worker Temporal sqx y workers SQX/MT5 (compartidos Zeus/Hera/Kronos, NO TOUCH). No se lanzaron campañas ni backtests.
- **Ownership del runtime DEV compartido en Daedalus:** esta sesión instaló y es dueña de `echo-core-dev`/`echo-gateway-dev` + release layout `/home/kor/opt/echo-dev`; cualquier otra sesión debe reconciliar contra esta sección antes de mutar. El screen `deployer` tiene owner separado (sesión 2026-09-17) y NO debe reiniciarse.

### 5.2 Recertificación join Forge→Echo (2026-09-21T02:30Z) — evidencia AS-BUILT de certificación; NO cierra producto

Sesión Cursor/Composer sobre el mismo host Daedalus; **sin redeploy**, sin restart de Core/Gateway, sin tocar workers/PROD/`.132`. Informe: workdir externo `~/aranea/work/cert-int-qa-20260921/FINDINGS-CERT-INT-QA-20260921.md` (fuera del vault).

- **Runtime health reconfirmado:** ambos `systemctl --user is-active` = active; `/health` Core `:9090` y Gateway `:8090` = 200; binarios SHA idénticos al §5.1; source HEAD desplegado = `5dd998f1…` (sin fix posterior).
- **Ingest real:** `forge_ingest_misconfigured=true` vigente; POST live `/api/v1/forge/promotions` → HTTP 503 `UNAVAILABLE` retryable. Keys ETCD `/echo/development/gateway/forge_ingest/*` **ausentes** (`etcd_get_value` found=false para `artifact_root`/`namespace`). Path de código sigue cableando `unavailableArtifactSource` cuando no hay source inyectado.
- **Schema DEV:** `echo-develop` tiene `canonical_scopes`/`journal_quarantine` pero **no** `promotion_records` / `strategy_versions` / `strategy_identity_mappings` ⇒ migración 061 identity/E-04 **no aplicada** al PG DEV compartido.
- **Forge consumer DEV:** `/symphony/development/echo/ingest/base_url` (y bearer) **ausentes**; `FORGE_RUNTIME_SCOPE_BLOCKED` sin cambio (no se arrancó worker).
- **Golden:** corpus F04-02 revalidado (`validate.py` PASS; `goldenrecompute` 5/5); bodies/payload_digest siguen **GOLDEN_AUTHORITY_BLOCKED** (owner action 1 pendiente).
- **Defectos código:** E-INT-01…08 y F-INT-01…05 **STILL_REPRODUCIBLE** sobre el mismo SHA + E-INT-09 (Store reutiliza archivo corrupto). Suites herméticas contracts/Corpus/CertPack PASS contra PG descartable `127.0.0.1:15433/cert_int_qa`; **no equivalen** a CERT-E04-01/CERT-F04-03.
- **Veredicto certificación producto:** `CERT_E04_01=BLOCKED`, `CERT_F04_03=BLOCKED`, G6 cross-lane **NOT_EXECUTED**. `/health` ≠ ingest funcional ≠ join certificado.

### 5.3 Recovery DEV 2026-09-21T03:15Z — código, ETCD y schema; runtime todavía en baseline

Sesión Cursor/Grok sobre Hermes (no sobre Daedalus). **No se tocó PROD, workers SQX/MT5, Windows `.132`, ni el screen `deployer`.** Health LAN reconfirmado: Core `:9090` y Gateway `:8090` = 200; POST live `/api/v1/forge/promotions` sigue 503 porque el proceso Gateway **no se reinició** (este agente no tiene SSH a `kor@192.168.31.161`).

- **Source Echo:** worktree `feature/e04-dev-ingest-recovery` commit `2360369c3ba406a8bf575f2169993028978f48da` publicado en origin (baseline previo `5dd998f1`). Seed tests ya no escriben ETCD; CLI `echo-etcd-bootstrap` es el operador explícito DEV. ArtifactSource real = filesystem bajo `gateway/forge_ingest/source_root`. GetByID acotado a namespace. Store reemplaza artefactos corruptos.
- **Source Symphony:** worktree `feature/f04-handoff-ingress-fixes` commit `a2321cc14e0236b393af2503eff35748005d9bc6` publicado en origin (baseline `25a5122`). Receipt `contract_version`/`receipt_id` fail-closed; 201 truncado reconcilia por GET-by-key.
- **ETCD DEV aplicado (read-back MCP RO, sin secretos):** `/echo/development/gateway/forge_ingest/{artifact_root,namespace,source_root,store_allowlist}` presentes; `artifact_root=/home/kor/opt/echo-dev/var/forge-artifacts`; `namespace=forge-live`; token creado y no impreso; `postgres/password` existente no sobrescrito. `/symphony/development/echo/ingest/base_url=http://192.168.31.161:8090`; bearer creado y no impreso. Count no-secreto forge_ingest = 4 (+ token secreto no listado).
- **Schema `echo-develop`:** creadas `strategy_identity_mappings`, `strategy_versions`, `promotion_records`, `strategy_identity_aliases` + triggers write-once; `echo_user` INSERT=true UPDATE=false sobre `promotion_records`. `strategy_definitions.id` **sigue** `varchar(64)` porque `v_lab_strategy_screener` es owned by `admin` y bloquea ALTER; no se reescribió `trade_journal` (242 651 filas). Backups `mig061_backup_*` creados. `v_trade_execution_delta` y `mv_daily_operations` recreados.
- **Golden:** `trading_systems_test` confirmado como autoridad de bodies; MCP postgres-rw está ligado a `echo-develop` ⇒ **GOLDEN_AUTHORITY_BLOCKED** intacto.
- **Runtime desplegado:** sigue binarios §5.1 SHA `5dd998f1`. Ingest live no recertificado.

### 5.4 Deploy Gateway + ingestión DEV (2026-09-21T03:38Z) — `ECHO_DEV_INGEST_FUNCTIONAL_PASS`; CERT formal no cerrado

Sesión Cursor/Grok **sobre Daedalus** (`hostname=daedalus`, usuario `kor`). **No se tocó PROD, workers SQX/MT5, Windows `.132`, Core DEV, ni el screen `deployer`.** Informe: `~/aranea/work/echo-dev-ingest-close-20260921/FINDINGS-INGEST-CLOSE-20260921.md`.

- **Access:** `DAEDALUS_EXECUTION_ACCESS_PASS` por ejecución local (no SSH). `systemctl --user` operativo; write en `/home/kor/opt/echo-dev`.
- **Release Gateway:** publicado `/home/kor/opt/echo-dev/releases/2360369c3ba406a8bf575f2169993028978f48da/echo-gateway` SHA256 `ef56fff6b1b4afcfeafee33971d44706eaf30083bab51f68f34e47201eb96f80`; `vcs.revision=2360369c…` `vcs.modified=false`; go1.27.1 linux/amd64 `-trimpath -buildvcs=true`. Core binario copiado sin rebuild (`34f10782…`). Symlink `current` atómico al SHA nuevo. Rollback documentado al release `5dd998f1`.
- **Unidad:** restart exclusivo `echo-gateway-dev.service`. MainPID 2478768→2521367; `NRestarts=0`; ExecStart `%h/opt/echo-dev/current/echo-gateway`. Core MainPID **2479388 intacto** (sin restart). `/health` Gateway+Core 200. Journal: `forge_ingest_misconfigured=false`.
- **Schema DEV (delta sobre §5.3):** GRANT UPDATE a `echo_user` sobre `strategy_identity_mappings` / `strategy_versions` / `promotion_records` / aliases. Causa: RI PostgreSQL exige UPDATE para `SELECT … FOR KEY SHARE`; los triggers write-once siguen bloqueando UPDATE/DELETE reales. Migración 061 **no marcada completa**; `strategy_definitions.id` sigue `varchar(64)`.
- **Ingestión física:** HTTPIngress Symphony `a2321cc` → POST `/api/v1/forge/promotions`. 401 sin Bearer; 201 receipt `338bd937-95ad-4389-9278-89285908b0a6` `INGESTED`; replay 200 mismo id; GET by-key 200; same-key different digest 409 `CONTRACT_CONFLICT`/`sealed_digest`. PG read-back: `registry_namespace=forge-live`, key `sha256:0feb7f41…`, digest `sha256:be73cf7f…`, canonical `dev-daedalus-ingest-daedalus-dev-ingest-20260921T033545Z`. Artefactos materializados bajo `var/forge-source/minio/forge/…` con store `var/forge-artifacts/sha256/1ab88438…`. **No es el golden RERUN-6.**
- **Golden:** `GOLDEN_AUTHORITY_BLOCKED` intacto (bodies en `trading_systems_test.sqx.handoff_manifests`; owner action 1 sin entrega).
- **Veredicto:** `ECHO_DEV_INGEST_FUNCTIONAL_PASS`. `CERT_E04_01=BLOCKED`, `CERT_F04_03=BLOCKED`. `/health` ≠ ingest funcional ≠ join certificado con golden.

### 5.5 CERT-E04-01 / CERT-F04-03 PASS (2026-09-21T04:18Z) — golden auténtico ingerido en Gateway DEV

Sesión Cursor/Grok sobre Daedalus. **No se tocó PROD, workers SQX/MT5, Windows `.132`, Core DEV (PID 2479388), ni el screen `deployer`.** Evidencia: `~/aranea/work/cert-e04-01/`.

- **Golden access (Caso A):** identity `sqx` de sqx-flowkit vía ETCD `/sqx-flowkit/development/postgres` (mismo canal que `strategy get`) contra `192.168.31.220/trading_systems_test.sqx.handoff_manifests`. SELECT RO por las 5 PKs `idempotency_key` del corpus F04-02. `canonical_body` es JSONB; POST usó `Encode()` canónico (`PERSISTED_JSONB_CANONICAL_REENCODE_VERIFIED`). MCP postgres-rw (`echo-develop`) no se usó para extraer.
- **Runtime:** Gateway `3d260e81ee37dc80c3ff186b1a089e6aada07c1d` (SHA256 `5f77d108…`, `vcs.modified=false`) unidad `echo-gateway-dev` PID 2543059; Core `5dd998f1` / `34f10782…` PID **2479388 intacto**; `forge_ingest_misconfigured=false`; HTTPIngress Symphony `a2321cc`.
- **Fixes Echo (local, branch `feature/e04-dev-ingest-recovery`):** `2498042f` acepta `policy_id=finalist_promotion@2.0.0`; `3d260e81` acepta `target_platform=MetaTrader5` + migración 064. CHECK DEV aplicado como `echo_user`.
- **ETCD DEV:** `/echo/development/postgres/password` estaba en seed `test-postgres-password` (22 B, ping fail). Restaurado el valor previo de historial (mod_rev 58426, ping OK). **No se escribió PROD** (`/echo/production/postgres/password` sigue siendo el seed de prueba).
- **Join:** 5×201 INGESTED + replay 200 mismo receipt + GET by-key 200 + 409 `CONTRACT_CONFLICT` + 404 foreign ns. Magics `26090011013/014/016/017/018`. Locators en `var/forge-artifacts/sha256/…`. Noneffects: accounts/positions/journal/raw/canonical invariantes; +5 promotions/versions/identities.
- **Veredicto:** `GOLDEN_AUTHORITY_PASS` · `CERT_E04_01_PASS` · `CERT_F04_03_PASS` (HTTPIngress aislado; `sqx.handoff_deliveries` no mutado; F-INT-03 fuera de receta).

### 5.6 Git recovery E-04 (2026-09-21T13:0xZ) — publicación de la feature; runtime intacto

Sesión TOP manager sobre Daedalus (`kor`, ejecución local). **Sin redeploy, sin restart, sin POST, sin tocar PROD/workers/screen `deployer`.** Veredicto `E04_RECOVERY_PUBLISHED`.

- **Git:** `origin/feature/e04-dev-ingest-recovery` FF `2360369c..4aad647b` (read-back `origin HEAD == local HEAD`; `origin/master` intacto `5dd998f1`). Commits certificados `2498042f`/`3d260e81` publicados intactos; encima `988e0ae6` (seguridad ETCD) y `4aad647b` (renumeración migración 064→068 por colisión con `064_reference_enrollment_binding` de E-06; DAG 065/066/067 ocupado por E-07/08/09, 068 libre verificado). **El commit desplegado (`3d260e81`) es el 2º commit de la branch publicada; la tip publicada añade 2 commits que no alteran el binario en ejecución.**
- **Runtime re-verificado:** Gateway `vcs.revision=3d260e81` `vcs.modified=false` SHA256 `5f77d108…` PID 2543059 health 200 `forge_ingest_misconfigured=false`; Core `5dd998f1`/`34f10782…` PID 2479388 intacto.
- **Seguridad ETCD (nuevo hallazgo, corregido en source):** `v1/sdk/etcd/example_test.go:TestEtcdDumpUtility` espejaba `/sqx-flowkit/development/` sobre `/sqx-flowkit/production/` del clúster real (defaults `192.168.31.250-254:2379`) vía `put()` interno que salta el guard de `SetVar`; corría en cualquier `go test ./v1/...` ordinario y fue ejecutada por esta sesión ~12:27Z durante suite routine (PASS 0.46s, sobrescribe sin cleanup). Fix `988e0ae6`: dump requiere aprobación explícita + endpoints explícitos + unlock dedicado para production (default SKIP); `DeleteVar` con guarda de tests en v1/v2. **Owner actions:** restaurar `/echo/production/postgres/password` (intacto de §5.5/§7) y verificar `mod_revision` de `/sqx-flowkit/production/` (> 2026-09-21T12:20Z ⇒ contaminación de esta corrida ⇒ reconciliar y evaluar impacto en workers flowkit).
- **Migraciones:** sin tabla de control en `echo-develop` (aplicación manual). Efecto de la migración E-04 (CHECK ampliado) ya aplicado manualmente como `echo_user`; renumerada a `068_strategy_version_forge_platform` en source. E-06 064 no aplicada en DEV; 061 parcial (`strategy_definitions.id` `varchar(64)`). **Merge/deploy de la migración sigue gated al flujo de release estándar.**
- **Regresiones:** suites `v3/sdk/postgres` + `v3/gateway/internal` PASS en PG descartable (schema hasta 064-forge); fallo preexistente `TestAutomationHandler_HandleMessage_ValidAction` demostrado idéntico en `2360369c` y `5dd998f1`. Golden: `validate.py` PASS; alcance `PERSISTED_JSONB_CANONICAL_REENCODE_VERIFIED` (no transport-bytes).

### 5.7 Front DEV en Daedalus (2026-09-21, ~03:00Z del 22) — ambiente de desarrollo; NO certifica producto

Sesión ZCode/GLM-5.3-Flash sobre Daedalus (ejecución local, `kor`). **Sin tocar PROD, workers SQX/MT5, Windows `.132`, ni el screen `deployer`.** Core MainPID 2479388 quedó intacto; Gateway reiniciado de forma controlada (única mutación de runtime, ver abajo).

- **Componente:** `echo-backoffice` (`v3/front`, Vue 3 + Vite + urql) del repo canónico `xKoRx/echo` @ master `5dd998f1` con worktree limpio. El `.env` trackeado no se modificó: los endpoints se inyectan por variable de proceso en `vite build`. El `dist` previo (2026-09-12) estaba horneado con endpoints PROD (Hasura `.48`, Gateway `.71`).
- **Build DEV efectivo:** `VITE_HASURA_ENDPOINT=http://192.168.31.75:8080/v1/graphql` (Hasura DEV según `v3/hasura/config.yaml`), `VITE_GATEWAY_ENDPOINT=http://192.168.31.161:8090` (Gateway DEV §5.5) y `VITE_HASURA_ADMIN_SECRET` (valor entregado por owner en la sesión, **nunca persistido en vault ni commit**). Build desde master local `5dd998f1 + 269fefc3` (commit **local sin push**: front usa `x-hasura-admin-secret` en HTTP y `connection_init.payload.headers` en WS cuando `VITE_HASURA_ADMIN_SECRET` está definida; sin ella conserva el flujo Bearer por token de operador; en este Hasura la secret top-level del protocolo `graphql-ws` se ignora — verificado por probe). El `dist` previo (2026-09-12) estaba horneado con endpoints PROD (Hasura `.48`, Gateway `.71`).
- **Servicio:** unidad `systemd --user` `echo-front-dev.service` (`~/.config/systemd/user/`), `vite preview --host --port 4173 --strictPort` con el binario node absoluto de mise, enabled en `default.target.wants`, RSS ~105–120 MB. Rebuild del front ⇒ `systemctl --user restart echo-front-dev`. `npm run dev` (vite `:3000`) queda como modo manual para editar el front (HMR), no como servicio.
- **CORS Gateway DEV:** key ETCD `/echo/development/gateway/cors_allowed_origins`; primer ajuste (rev 58912) allowlist de orígenes `:4173`/`:3000`, luego (rev 58913) `*` + `GATEWAY_ENV=develop` en `etc/echo-gateway.env` ⇒ `Access-Control-Allow-Origin: *` desde cualquier origen (sólo afecta CORS; la auth por endpoint del Gateway sigue exigida). Restarts controlados de `echo-gateway-dev` (MainPID 2543059→3056377→3067953): health 200, `forge_ingest_misconfigured=false` en journal; Core MainPID 2479388 intacto en todos los cortes.
- **Smoke con datos vivos (2026-09-22T03:34Z):** sin prompt de token; badge `ECHO: HEALTHY`; 5/5 cuentas, 14 trades en stream, equity/P&L reales sobre `echo_test`; suscripciones WS autenticadas vía secret en `payload.headers`. `:4173/` y `/watchtower` (fallback SPA) 200 por LAN.
- **Alcance de seguridad aceptado por owner (DEV):** la secret DEV queda horneada en el bundle servido por LAN (rol admin sobre el Hasura DEV para quien cargue el front). El auth webhook del Gateway (`/api/v1/auth/hasura`) sigue sin cablear en el Hasura DEV; cablearlo y volver al flujo Bearer es la mejora pendiente para endurecer (recomendado antes de cualquier exposición fuera del LAN de confianza).
- **Ownership:** esta sesión es dueña de `echo-front-dev.service`, del commit local `3596fc48` (sin push; amplía `269fefc3` con token de control opcional) y de la key `gateway/cors_allowed_origins` DEV; cualquier otra sesión reconcilia contra esta sección antes de mutar.
- **Delta 2026-09-22 ~08:05Z — plano de auth y propagación de configs reparado (ambos síntomas del owner: 503 en Republish Configs y bridge sin cuentas nuevas):** (1) provisionados en ETCD DEV `/echo/development/gateway/auth/{front_read,config_operator,control_operator,service_hasura_webhook}_token` (4 valores aleatorios distintos, archivo con mode 600 en `/home/kor/opt/echo-dev/etc/dev-auth-tokens.env`, nunca en vault) — sin ellos todo endpoint autenticado del Gateway respondía 503 `AUTH_MISCONFIG` fail-closed; (2) los 6 event triggers de Hasura DEV apuntaban al Gateway muerto `.211:8090` y no tenían header de Authorization — corregidos vía `replace_metadata` a `.161:8090` + `Authorization: Bearer <service_hasura_webhook_token>` (backup pre-fix en `/home/kor/opt/echo-dev/etc/backup/hasura-dev-metadata-20260922-pre-triggers.json`; metadata consistente; ojo: Hasura no emite evento si ninguna columna monitoreada cambia de valor, y los eventos muertos del corte viejo no reintentan por `num_retries=0`); (3) commit local del front ampliado: `VITE_GATEWAY_CONTROL_TOKEN` definido ⇒ operaciones de control (republish/close-positions) no solicitan token al operador. Verificación física: republish 200 con 10 cuentas/589 políticas/139 estrategias; trigger real `delivered=t` con mensaje en Kafka (p1:67); click del botón Republish Configs en browser ⇒ force-sync exitoso en journal sin prompt.

### 5.8 Prework Forge DEV en Daedalus (2026-09-24 ~16:00Z) — watcher/worker DEV operables; SQX DEV sigue sin distribución ni licencia; NO certifica producto

> [!warning] SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION (2026-09-24, §0)
> Este prework se ejecutó bajo la premisa “Forge necesita runtime/SQX DEV en Daedalus”, corregida por el owner: Forge tiene un único ambiente operacional y Campaign 001 NO requiere SQX, licencia ni worker DEV en Daedalus. La evidencia física de esta sección (corrección ETCD DEV del watcher, watcher/worker operables y aislados, repro fail-closed de `sqcli` ausente, smoke y teardown 100%) sigue siendo válida como evidencia del runtime candidato DEV, pero la conclusión “SQX DEV en Daedalus = BLOCKED por distribución/licencia” ya no es requisito ni blocker. Corrección factual adicional (bitácora 2.ª/3.ª sesión de [[Echo Forge — Operación Real V2]]): los SHA256 de binarios listados abajo (`35821eb9…` watcher, `251f25e2…` worker) corresponden a builds con tree sucio reemplazados después por los vigentes `7af048f0…` (watcher) y `b2e9c227…` (worker).

Sesión ZCode/GLM-5.3-Flash sobre Daedalus (`kor`, ejecución local). **Sin tocar PROD, workers SQX/MT5 compartidos (Zeus/Hera/Kronos), Windows `.132`, Core/Gateway/front DEV ni el screen `deployer` (intacto, sigue corriendo `ENV=production` desde 2026-09-17).** Baseline symphony `master=origin/master=d9032ff8` verificado limpio al iniciar y sin delta al terminar. Workspace externo: `~/aranea/work/forge-prework-20260924/` (binarios + logs del smoke).

- **Corrección ETCD DEV aplicada (con rollback):** `/sqx-watcher/development/temporal/namespace` `sqx`→`sqx-dev` (rev 58981) y `/sqx-watcher/development/sqx/task_queue` `sqx-dev-queue`→`sqx-main-queue` (rev 58982). Antes: el watcher DEV despachaba al namespace `sqx` (flota PROD) con cola distinta a la del worker DEV ⇒ inconsistencia latente con efecto PROD-fallback. Rollback = restaurar valores previos (namespace `sqx` mod_rev 54030, task_queue `sqx-dev-queue` mod_rev 58896).
- **Configuración efectiva DEV demostrada en runtime (logs `env=development`):** watcher y worker leen ETCD `192.168.31.250-254:2379`; Temporal `192.168.31.46:7233` namespace `sqx-dev` cola `sqx-main-queue`; MinIO `192.168.31.92:9000` buckets `sqx-configs`/`sqx-strategies` (misma instancia para DEV/PROD ⇒ aislamiento por prefijo, no por host); PG `192.168.31.220/trading_systems_test` (registry `sqx.configs`, `sqx.flow_runs`); telemetría `192.168.31.45:4317`; `sqcli/binary_path=/home/kor/sqx/sqcli` (inexistente en este host).
- **Watcher DEV:** `RUNNING / PHYSICALLY_VERIFIED` para pipeline de ingest (7/7 pasos reales: validate_spec → validate_configs → upload_artifacts → save_config → import_intake → dispatch_workflow → move_processed), binarios construidos desde `d9032ff8` (SHA256 watcher `35821eb9…`, worker `251f25e2…`). Proceso detenido al cierre; no quedó como servicio.
- **Worker DEV:** `BLOCKED / FAIL_CLOSED_VERIFIED` — arranca, carga config DEV y **exige `sqcli` ejecutable al inicio** (`Validación de sqcli falló: command not found or not executable: /home/kor/sqx/sqcli`, exit 1). Este es el repro exacto del blocker.
- **Aislamiento demostrado:** cola `sqx-main-queue` en namespace `sqx-dev` con **0 pollers** antes y después (flota compartida opera namespaces `sqx`/`sqx-prop` ⇒ aislamiento por namespace Temporal); sin mutación ETCD/MinIO/PG en prefijos production.
- **Smoke de ambiente (dispatch real, cancelado y limpiado):** job `prework_smoke_20260924_r2` (task `project` retester con `.sqx` real de la cohorte G7, SHA256 `8952a6c3cfa14072b862c03c858f336135871cb25e72803cb91b71062396d3e9`) ⇒ workflow `GenericSQXWorkflow` `sqx-main-v1-556c2aa4-be36-40ed-9123-c11c2b7a27bc` (run `01a0d431-f3f1-758e-bda6-15d38fd99bb2`, flow_run `6a0aea75-1b58-4c17-8929-ae206f5d49e9`) creado en `sqx-dev`; quedó pendiente sin poller y fue **cancelado** (la cancelación se cierra sola cuando el primer worker DEV arranque — residuo benigno). Limpieza verificada: 4 objetos MinIO `wave_prework_smoke_20260924/*` borrados; filas PG `sqx.flow_runs` y `sqx.configs` borradas (FK `flow_runs_config_id_fkey` exige borrar flow_run primero).
- **SQX DEV (cierra la parte feasible del AS-BUILT):** sin instalación en Daedalus (`/home/kor/sqx` no existe), sin `java`, sin `etcdctl`/`mc`; sin distribución de SQX Build 142 en MinIO (buckets revisados) ni acceso SSH a la flota desde esta sesión; el plugin de evidencia (`EchoForgeAutomator.jar` con `EchoForgeOverviewExporter`) requiere `SQX_DIR` para compilarse. Instalación+licencia = **decisión owner** (instalar OpenJDK es operacional y no bloquea la decisión). Formato C1 vigente confirmado en código: intake local `<watch_dir>/import/` vía `watcher.import` en el spec (config declarada sólo si classifications/early_rankings consumen `watcher_import`); hop import es bootstrap interno (`root/0`, plugin fijo `EchoForgeOverviewExporter`), no task declarada.
- **Herramientas desechables usadas (eliminadas; repo sin delta):** helpers Go efímeros dentro de `sqx/tools/` para escribir ETCD, subir/bajar MinIO, cancelar workflow y limpiar PG; `go.work.sum` restaurado tras `go run`.



### 6. Lectura y operación para cada sesión

- **Cold start o cambio de entidad a Echo/Forge:** `agents-os-bootstrap` → router `aranea-agent-dev` → leer este contrato **antes de elegir ambiente o actuar**. No añadirlo al stack global ni cambiar el bootstrap.
- **Warm turn de la misma sesión:** reutilizarlo; leer solo el delta cuando cambió la fuente, cambió el ambiente o existe evidencia de drift.
- **Entrada directa por `AGENTS.md` de repositorio:** debe remitir a este contrato; la federación en los repos es un cambio separado de la presente edición Agents-OS.
- **Operaciones:** seguir [[aranea-mcps-expert]] y el runbook del recurso; verificar permisos reales, preflight, blast radius, rollback y postcondición. No convertir este contrato en manual de comandos.
- **Si el contrato no está disponible:** lectura/investigación local permitida; mutaciones de infraestructura bloqueadas hasta recuperar ambiente y autoridad.

### 7. Reconciliación pendiente

| Punto | Estado a este corte | Acción de actualización |
|---|---|---|
| Modelo de ambientes por producto | **Corregido por el owner 2026-09-24 (§0):** Echo = DEV/PROD; Echo Forge = un solo ambiente operacional (production, flota Zeus/Hera/Kronos + worker-kronos); Daedalus = workspace/builds, no runtime SQX/MT5 de Forge | Ninguna. Las conclusiones de este contrato que derivaban del modelo anterior están marcadas `SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION`; las decisiones TARGET de Echo quedan intactas. |
|---|---|---|
| Reporte final Hermes `dev-win` | No recibido aquí | Incorporar host/identidad, claves host sanitizadas, profiles, smokes y fecha. |
| Core/Gateway sobre Daedalus | **AS-BUILT completo 2026-09-21 en §5.1** — ambos `RUNNING/PHYSICALLY_VERIFIED`; credencial PG resuelta por owner; `systemd --user`+linger, unidades de sistema pendientes de owner con root | Owner opcional: migrar a unidades de sistema. |
| Seed tests que sobrescriben credenciales ETCD (v1/v2/v3 `echo_seed_test.go`, dev+prod, sin guardas) | Source v3 fail-closed; **recurrencia 2026-09-21** DEV restaurado desde historial ETCD; PROD sigue en seed de prueba | Owner: restaurar `/echo/production/postgres/password` desde historial (no hecho aquí). No ejecutar `go test ./...` contra ETCD real. |
| Forge DEV en Daedalus | HTTPIngress aislado `a2321cc` contra Gateway DEV; 5 golden INGESTED | Certificación de ingesta del lado Echo; el runtime operacional de Forge sigue siendo la flota (§0), no Daedalus. No arrancar worker Temporal en Daedalus. Siguiente frozen: CERT-F05-01. |
| Front DEV (echo-backoffice) en Daedalus | **AS-BUILT 2026-09-22 en §5.7** — `echo-front-dev` RUNNING (`vite preview :4173`), datos vivos vía `VITE_HASURA_ADMIN_SECRET`, control ops sin prompt vía `VITE_GATEWAY_CONTROL_TOKEN`, propagación de configs reparada (tokens auth ETCD + triggers Hasura a `.161`), commit local `3596fc48` sin push | Owner: revisar/decidir destino del commit local `3596fc48` (push o revert); rotar secret/tokens DEV si su exposición por LAN no se acepta. Rebuild ⇒ `vite build` con env override + restart de la unidad. |
| Gateway forge_ingest DEV + mig 061/064 en `echo-develop` | Gateway `3d260e81`; CHECK platform incluye `MetaTrader5`; identity tables + GRANT UPDATE vigentes; migración E-04 renumerada a 068 en source (`4aad647b`); sin tabla de control de migraciones | No forzar 061 completa. No revertir el CHECK con filas Forge. Merge/deploy de la migración por flujo de release. |
| CERT-E04-01 / CERT-F04-03 | **PASS 2026-09-21T04:18Z** sobre golden F04-02 + Gateway DEV | F-INT-03 sigue backlog propio. ~~Echo feature commits no pusheados.~~ **→ PUBLICADOS 2026-09-21T13:0xZ @ `4aad647b` (§5.6).** |
| SQX local / Windows MT5 | **SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION (2026-09-24, §0).** La conclusión anterior (“SQX DEV en Daedalus: BLOCKED por distribución/licencia”, §5.8) quedó sin efecto: no hay requisito de distribución/licencia SQX en Daedalus ni de `dev-win` para Forge. Forge usa su flota operacional Zeus/Hera/Kronos + worker-kronos (distribución SQX 142 y licencia de flota ya presentes). `PREWORK_MT5 = DEFERRED_UNTIL_C6` se mantiene **por alcance de stage** (C0–C2 sólo requieren SQX; MT5 es alcance de C6), no por ambiente | Ninguna owner action de licencia Daedalus. [[Echo Forge — Operación Real V2]]: C0 revalida el runtime desplegado (RC 0.2.106 @ `d07cc69` vs baseline `d9032ff8`) como primer hito de Fase 1. |
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
- **Decisión expresa del owner 2026-09-24 (§0):** Echo y Echo Forge no comparten modelo de ambientes; Forge tiene un único ambiente operacional (production) sobre SQX Zeus/Hera/Kronos y worker Windows Kronos, y sus pruebas físicas se ejecutan allí; Daedalus no es runtime SQX/MT5 de Forge. Rige sobre decisiones previas de esta nota.
- [[Echo Forge — Operación Real V2]] y [[Echo Forge — Import Task V1]] — runtime y validaciones físicas reales de Forge sobre la flota operacional.
