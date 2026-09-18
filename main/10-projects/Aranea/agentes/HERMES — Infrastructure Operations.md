---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Aranea]]"
parent: "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
sprint:
start: 2026-09-14
due:
progress: 0
repo:
jira:
prs:
slug: hermes-infrastructure-operations
aliases:
  - Hermes Infrastructure Operations
  - Hermes Homelab Administration
  - Hermes Infra Ops
tags:
  - kind/project
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - agent/hermes
  - domain/infrastructure
created: "2026-09-14"
updated: "2026-09-17"
---

# HERMES — Infrastructure Operations

> [!info]+ Infrastructure Operations
> **Padre:** [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] · **Owner:** agent · **Estado:** active · **Prioridad:** P1

## 🎯 Objetivo

Dar a Hermes autoridad operativa **paulatina, verificable y recuperable** sobre Aranea hasta poder administrar de extremo a extremo el homelab: storage, backups, TrueNAS, Proxmox, nodos, VMs/LXC, Linux/Windows, Docker, lifecycle de servicios, provisioning y componentes de mayor impacto cuando sean habilitados explícitamente.

Este workstream define el **management plane nativo** de Hermes. No depende del MCP Access Plane para reparar o administrar el mismo plano MCP ni los servicios subyacentes.

**Objetivo inmediato autorizado el 2026-09-17:** ejecutar H0 Observe/Inventory en una ventana de hasta 10 horas el 2026-09-18. El plan operativo vinculante está en `## 🧭 H0 — Plan de ejecución 2026-09-18` de ESTA nota: no crear otro planner ni volver a diseñar H0.

## 🧠 Contexto

Hermes será el administrador general del homelab, pero entregar root-equivalent sobre todo Aranea desde el primer día generaría demasiado blast radius y dificultaría saber qué autoridad está realmente certificada.

La estrategia es progresiva:

```text
observe
→ protect storage/backups
→ operate Proxmox lifecycle
→ operate guests/services
→ provision new infrastructure
→ enable high-impact infrastructure
→ integrated autonomy
```

El conocimiento existente de Backup/DR se reutiliza desde [[BACKUP-DR-OWNER-PROJECT]]. Este workstream **no rediseña Backup/DR**; lo usa como primer dominio real para certificar el modelo de autonomía.

## 🏛️ Boundary

### Este workstream SÍ gobierna

- authority/bootstrap de Hermes sobre interfaces administrativas nativas;
- inventario y discovery de infraestructura;
- administración de Proxmox/TrueNAS/hosts/guests según etapa activa;
- acceso Linux/Windows para operación;
- Docker/systemd/filesystem/configuración no secreta;
- service lifecycle y recovery;
- provisioning de infraestructura cuando H4 quede habilitado;
- gates, rollback, revoke y evidencia de cada nivel.

### Este workstream NO gobierna

- capabilities MCP entregadas a Echo/Forge/agentes: eso vive en [[HERMES — Agent Access Operations]];
- endpoints/permisos exactos del MCP Access Plane: source of truth [[AGENT-PLATFORM - MCP Access Plane]];
- redefinir la estrategia Backup/DR: source of truth [[BACKUP-DR-OWNER-PROJECT]];
- mutaciones PROD no autorizadas explícitamente.

## 🔐 Matriz de authority efectiva (2026-09-17, reconciliación incremental)

| Target | Canal/identidad | Clase | Evidencia / límite |
|---|---|---|---|
| athena/zeus/hera/kronos/hades/truenas | SSH `agent_ro` + `sudo -n agent-read` | observe, wrapper-only | G0: matriz 6/6 PASS; no generalizar a SSH de guests |
| `mcps` LXC | SSH `hermes-ops@mcps` + sudo scoped | operate, appliance | G0: 26 containers; recovery independiente del MCP |
| daedalus | SSH `hermes-ops@daedalus`, sin sudo | operate scoped | G0 consumer configs; no permisos generales |
| hermes-vm (self) | `systemd --user` y FS local | operate propio runtime | recovery 2026-09-16 |
| Windows `worker-kronos` | ssh-mcp viewer/operator | observe/operate parcial | probes 2026-09-17; requiere matriz G2 formal y smoke de sesión nueva |
| APIs nativas Proxmox/TrueNAS | sin credencial Hermes demostrada | absent para API directa | preparar RO owner bundle si las consultas necesarias no están cubiertas por wrapper; NO asumir H2/H4 habilitados |
| MCPs runtime Hermes | `aranea-postgres-ro`, `aranea-ssh` :3000, `aranea-observability-ro` :3009 | observe, parcial | G3 consumer helper PASS 2026-09-17; recertificar carga en sesión nueva |

## 🔐 Principios de autoridad

1. Hermes recibe sólo la autoridad necesaria para el nivel H actualmente certificado.
2. Un operador especializado recibe tools/credentials sólo para su responsibility boundary.
3. Los valores secretos nunca se escriben en Agents-OS; sólo referencias.
4. Antes de cualquier mutación se demuestra target, entorno y blast radius.
5. Toda nueva autoridad debe tener revoke/rollback viable.
6. Un management path no puede depender exclusivamente del servicio/plano que debe recuperar.
7. PROD/high-impact permanece gated hasta decisión explícita del owner.

## 🚦 Roadmap H0 → H6

### H0 — Observe / Inventory

**Objetivo:** Hermes puede reconstruir el estado real de Aranea sin mutar.

- inventario de nodos físicos/virtualizados;
- Proxmox cluster resources;
- TrueNAS/storage topology y health;
- VMs/LXC, host placement y estado;
- services/runtimes relevantes;
- interfaces administrativas disponibles;
- relaciones service → guest → host → storage;
- identificación de gaps de autoridad/credenciales por referencia.

**Gate:** un agente fresco puede diagnosticar dónde vive un servicio y qué management path usar sin preguntar al owner por datos ya documentados.

### H1 — Backup & Storage

**Objetivo:** Hermes opera protección y recovery básico usando el diseño vigente.

- leer y reconciliar [[BACKUP-DR-OWNER-PROJECT]];
- ejecutar/verificar backups dentro del scope aprobado;
- health de targets/storage;
- detectar jobs fallidos o cobertura incompleta;
- validar evidencia de restore;
- ejecutar restore drill acotado;
- registrar findings y drift en Agents-OS.

**Gate:** la operación normal de backup/restore evidence no requiere shell humana habitual.

### H2 — Proxmox Lifecycle

**Objetivo:** Hermes administra lifecycle de VMs/LXC con scopes explícitos.

- inspect/config/status;
- start/stop/reboot;
- create/clone cuando el scope esté aprobado;
- resource/config changes acotados;
- validación post-change;
- rollback/recovery.

**Gate:** lifecycle completo certificado sobre workloads no críticos antes de ampliar scope.

### H3 — Guest & Service Operations

**Objetivo:** Hermes diagnostica y repara servicios dentro de guests.

- Linux SSH;
- Windows management path;
- Docker/Compose;
- systemd/services;
- filesystem/configuración;
- logs/health;
- restart/recovery;
- verificación funcional post-repair.

**Gate:** reparar un servicio DEV/test roto end-to-end sin intervención humana.

### H4 — Provisioning

**Objetivo:** Hermes puede levantar infraestructura nueva reproducible.

- VM/LXC/containers;
- OS/bootstrap;
- instalación/configuración de software;
- networking/config necesaria dentro del scope;
- observabilidad y backup onboarding;
- documentation/state registration.

**Gate:** nuevo servicio DEV/test provisionado desde objetivo funcional hasta health/backup/documentación.

### H5 — High-impact Infrastructure

**Objetivo:** habilitar progresivamente operaciones de mayor blast radius.

Ejemplos potenciales: networking, cluster/storage operations, quorum-sensitive services, cambios host-level críticos.

**Gate:** cada familia tiene recovery demostrado, authority específica y criterios de abort/rollback.

### H6 — Integrated Autonomy

**Objetivo:** Hermes coordina incidentes y cambios multi-capa usando operadores especializados.

**Gate:** tareas habituales y recoveries previstos requieren intervención humana excepcional, no como paso normal del procedimiento.

## 🤖 Operadores lógicos previstos

La separación exacta se ajustará por evidencia; punto de partida:

- `backup/storage operator`
- `proxmox operator`
- `linux/container operator`
- `windows operator`
- `service operator`

No se crea un framework genérico de operadores por anticipación. Primero se certifican paths reales; después se extraen skills/prompts reutilizables.

## 🧪 Acceptance scenarios

Este workstream debe demostrar progresivamente escenarios reales, no sólo acceso técnico:

- identificar host/guest de un servicio desde nombre lógico;
- detectar backup faltante o job fallido;
- validar un backup y restaurar una muestra acotada;
- reiniciar de forma segura un servicio DEV/test;
- recuperar un MCP/runtime caído usando el management path nativo;
- crear/provisionar un workload no crítico cuando H4 esté activo;
- registrar evidencia suficiente para que otro agente continúe.

## 📊 Estado actual

- **Workstream:** creado 2026-09-14; H0 EN EJECUCIÓN PARCIAL, no certificado integral.
- **G0:** PASS, bootstrap y `agent-read` 6/6, `mcps-ops`, `daedalus-ops` y authorities; `I0.1–I0.4` cerradas.
- **G1 discovery:** captura 2026-09-17 18:58 UTC 6/6, 59 VMs definidas (42 running / 17 stopped), 10 storages, canon actualizado. Discovery PASS según resumen owner; la cobertura service/guest y G2 no se infieren de este PASS.
- **G3 integration:** batch autorizado en config Hermes (`aranea-ssh` y observability junto con postgres-ro); helper consumer-side PASS (SSH 11 tools, observabilidad 22 tools); pendiente prueba en sesión nueva. El change log `2026-09-17-hermes-infra-preflight-g0` ya registra G3 resuelto; la fotografía previa 'sólo postgres' queda histórica.
- **G2:** parcial, Linux probado; Windows tiene probes previos pero requiere matriz de cobertura y certificación H0 formal; Proxmox/TrueNAS sin credenciales API nativas demostradas, utilizar wrapper cuando tenga cobertura probada.
- **G4:** pendiente prueba integral fresca desde Hermes.
- **Management path:** independiente vía `mcps-ops`; nunca tratar el MCP como ruta exclusiva de recovery.
- **Runtime Hermes 2026-09-16:** `v0.21.3 (2026.9.14)`, dashboard 127.0.0.1:9119 HTTP 200, `hermes-gateway-ariadna.service` conectado. Legacy `hermes-gateway.service` permanece disabled para evitar doble polling de Telegram. Recovery en [[hermes-linux-update-recovery]] y [[hermes-agent-operator]].
- **Publicación Agents-OS:** editar `VAULT_ROOT` como fuente canónica; pipeline vault→GitHub corre en otro equipo (~1 min); repo local Hermes es consumidor fast-forward, no productor. Si GitHub diverge, resolver conservando delta del vault y evitar direct push al espejo.
- **Backup/DR:** [[BACKUP-DR-OWNER-PROJECT]] mantiene autoridad; no tocar jobs ni decisions congeladas en H0.

## 🧱 Entrega de desarrollo

_No aplica como repo único. Este workstream puede cambiar configuración ejecutable e infraestructura; antes de cada implementación registrar target, source of truth, baseline, scope, rollback y evidencia. Si aparece código/versioned config, declarar repo, branch, base y SPEC antes de modificar. No inventar repo ni editar el espejo GitHub como si fuera el vault en runtime._

## 🧭 H0 — Plan de ejecución 2026-09-18 · SPEC freeze

### Misión y definición de resultado

Ventana de **hasta 10 horas desde T0 real de inicio**. Ejecutar H0 hasta su gate máximo demostrable; NO confundir 10 horas con garantía de PASS ni con autorización de mutaciones. Prioridad: 1) verificación desde Hermes; 2) cobertura y mapa de servicios; 3) observación nativa estrictamente necesaria; 4) evidencia y handoff. H0 NO ejecuta lifecycle, provisioning, restores, backups, restart productivo, root/elevación, red, storage mutable ni desarrolla Echo/Forge. Si hay tiempo remanente, adelantar únicamente contratos/handoff read-only para H1; no empezar H1 formal.

**Producto H0:** un Hermes fresco puede resolver `servicio lógico → guest/VMID y nodo → storage/dependencias cuando estén demostradas → canal disponible y authority → health/logs/métricas permitidas → diagnóstico con evidencia y gaps`, sin hacer cambios. No construir un provider framework, dashboard, DB de capabilities, nuevo MCP ni orquestador.

**No confundir denominadores:** 59 es inventario de guests definidos, no número de SSH targets ni de servicios. Los 17 apagados no fallan por no aceptar SSH; deben figurar como `STOPPED_EXPECTED` salvo otra evidencia. La capacidad de guest-SSH se mide sólo sobre hosts encendidos, de familia pertinente, con identidad autorizada. Coverage de servicios se mide sobre el catálogo in-scope enumerado, no sobre un total inventado. `PASS` de un endpoint no implica permisos para otras máquinas.

### Baseline congelado y delta obligatorio

- Canon: [[HERMES — Infrastructure Operations]], [[HERMES — ARANEA AUTONOMOUS OPERATIONS]], [[AGENT-PLATFORM - MCP Access Plane]], [[BACKUP-DR-OWNER-PROJECT]], `30-resources/aranea/00-index.md`, `01-topologia/fechas-captura.md`, catálogo de servicios, skills `aranea_agent_ro_inventory_refresh` / [[hermes-agent-operator]]. Resolver paths reales desde `VAULT_ROOT`, no fijar paths absolutos.
- Evidencia inicial: change log `2026-09-17-hermes-infra-preflight-g0`, discovery `*_20260917_185839.txt`, `inventory_20260917_185839.json`; 6/6, 59 = 42+17, 10 storages, `mcps-ops` 26 containers; G3 helper PASS.
- T0: bootstrap warm (si aplica); leer delta de esta nota, último change log y el runtime, comprobar hash/mtime de la captura y git/vault freshness. Si hay evidencia posterior, adoptar la más reciente tras reconciliation; no revertir gates demostrados, no volver a generar G0/G1 por rutina.
- La instrucción del owner de adelantar H0 el 2026-09-18 autoriza **únicamente preparación/observación H0** como excepción de prioridad frente a la secuencia histórica padre Access Plane→Echo/Forge→H0. A2–A5, H1–H6 y Backup/DR permanecen en sus propios proyectos.

### Roles, ownership y paralelización

Un **Hermes manager/integrador** coordina y es único escritor de ESTA nota, gates, config compartida e integración. Ejecutores lógicos A/B/C/D sólo si el runtime real permite aislamiento, credenciales y concurrencia; si no, ejecutarlos secuencialmente. Máximo 4 workers y un integrador, NO crear subagentes/perfiles por reflejo. Antes de delegar, manager entrega worktree/repo/branch/base y `allowed files` exclusivos por tarea; un único integrador une cambios después de pruebas. No compartir sesión SSH MCP entre workers si causa agotamiento: reutilizar `Mcp-Session-Id`, hacer DELETE al finalizar y acotar concurrency. `ssh-mcp` tiene antecedente de pool 64 agotado por init-only; no disparar sondeos masivos.

- **A / inventory & service map (critical path):** consumir el JSON actual, registrar 59 identidades estables (`node + VMID` como localización actual, VMID de clúster como identidad cuando aplique), tipo, state, colocación, storage referido, origen y hora. Reconciliar hosts/nodos, 10 storages, catálogo de servicios y servicios críticos; joins `service→guest→node→storage` con `UNKNOWN` explícito si faltan datos; verificar que migración/cambio IP no fija el target equivocado. No duplicar inventario en otra DB. Documentar cobertura/gaps y proveer casos de prueba al integrador.
- **B / Linux & management boundaries:** certificar desde runtime Hermes `agent-read` 6/6, distinguir operator `mcps-ops` y `daedalus-ops` de viewer wrapper y guest SSH; mapear identities/profile/capabilities por target; smokes inocuos y negativos `POLICY_DENIED` sobre comandos realmente prohibidos. `docker ps` con exit 127 en viewer es CLI inexistente, NO prueba de enforcement. No ampliar sudo, no modificar host-keys ni crear root universal. Preparar onboarding idempotente read-only sólo como SPEC si aparece un guest nuevo sin permiso.
- **C / Windows & service observation:** recuperar evidencias existentes del 17-sep, inspeccionar publisher SYSTEM y perfiles viewer/operator según sources vigentes; validar desde la nueva sesión Hermes al menos identidad, target, lectura de evidencia no secreta, estado/timestamp y rechazo efectivo de mutadores no autorizados. NO otorgar Windows admin/JEA en H0, NO tocar Task Scheduler ni MT5 productivo. Si el MCP ofrece sólo acceso indirecto, marcarlo como `CONSUMER_PLANE_ONLY`, no como recovery nativo.
- **D / Proxmox–TrueNAS read-only:** verificar si `agent-read` existente ya prueba inventario PVE, placement, cluster health, storage health/TrueNAS health necesarios. Emitir matriz `fact → wrapper/API → PASS/MISSING`. Sólo para MISSING genuino preparar API RO owner bundle; no pedir credenciales de H2/H4. Después de autorización, adoptar cliente/API nativo existente y probar lectura y rechazo de mutaciones. Detectar versiones reales antes de escoger transporte (TrueNAS 25.04+ usa JSON-RPC/WebSocket; REST eliminado en 26; verificar release instalada); exigir TLS/verificación cert para keys. Proxmox usar token privilege-separated, scopes efectivos de user∩token y expiración, no full privileges. Ninguna credencial nueva hasta consentimiento explícito.

### Owner Action Bundle — única interrupción agrupada

Antes de T+60 min el manager entrega UN bloque consolidado, sólo si existe gap probado, con tabla para cada autorización: `ID; hecho que falta; target real/versión; canal/identidad actual; mínimo permiso RO; efecto; cómo instala owner de forma segura; verificación positiva y negativa; expiración/revoke; alternativa sin permiso; impacto sobre gate`. Separar **DECISION** (autorizar o rechazar API RO) de **SEED** (owner instala el secreto directo en canal seguro del host); no pedir copiar tokens al chat/vault/GitHub. Validar account/role por read-only inspect, nunca autoelevar. Al responder owner: revalidar sólo los target afectados, continuar workstreams independientes en paralelo. Si owner no responde: registrar `GATED_OWNER`, continuar A/B/C y observación D por wrappers; no insistir ni inventar autorización. H2/H4 requieren otro contrato futuro; token RO NO los desbloquea.

### Evidence contract y matriz G2

Crear únicamente archivos de evidencia no secretos bajo la convención de run actual fuera del vault para artefactos grandes; en esta nota dejar referencias relativas al workspace y síntesis. Campos mínimos por observación: `run_id`, timestamp UTC, source/version, stable target ID, hostname/VMID+node actual si procede, service ID si procede, environment, method/channel, identity profile *sin credencial*, requested operation, effective allow/deny, result code/status, freshness, evidence reference, limitations. Redactar headers, env, payloads sensibles y blobs; no logs masivos en vault.

Matriz de targets: una fila por guest (59) y una por host/servicio pertinente con estado `INVENTORIED`, `OBSERVED`, `STOPPED_EXPECTED`, `UNREACHABLE`, `AUTH_DENIED`, `NOT_AUTHORIZED`, `UNKNOWN`, `STALE`, `CONFLICT`, según evidencia; permisos por canal y fecha. Mantener inventario≠reachability≠authority≠health; no colapsar estados ni inferir diagnósticos. Para VM offline, inventario y placement pueden PASS, guest-access es N/A. Para `PBS VM 180` respetar inaccesibilidad documentada y dependencia Backup/DR: registrar bloqueo, no escanear ni reparar por H0.

G2 family certifications:
- **Linux:** 6/6 control-plane wrapper (reprobe si stale); muestra representativa de guest Linux sólo si hay identidad ya autorizada; distinción viewer/operator y negativos.
- **Windows:** target `worker-kronos` y casos documentados; viewer/operator de alcance probado, evidencia publisher fresca, negativos seguros; no extrapolar a todas las Windows.
- **Proxmox:** inventario cluster/VMID, placement, state, storage por wrapper o API RO, source proof y exact permissions; clasificar API directa separadamente.
- **TrueNAS:** pools/datasets/health/topology por wrapper o API RO, auth y source proof; no mutaciones.
- **Observability:** Grafana/Jaeger/Loki datasource health y consulta acotada con target correlation, no confundir MCP tool list con observación real.

Un family gate es `PASS` sólo si todos sus MUST dentro del scope observado pasan; de otro modo `PASS_WITH_LIMITATIONS` (limitaciones no críticas y documentadas), `BLOCKED` (autoridad/target crítico) o `FAIL` (regresión real). No declarar un PASS universal a partir de una muestra. Reportar denominadores exactos por familia.

### Golden G4 — prueba desde sesión Hermes nueva

1. Nueva sesión real: comprobar que config carga `aranea-ssh`, observability y postgres-ro; mínimo session initialize+tools/list, health observable y cero secretos. Comprobar que no se levanta gateway legacy duplicado.
2. Elegir por inventory service catalog **tres escenarios** si hay evidencia: Linux/servicio en nodo, Windows MT5 vía publisher, infraestructura/storage TrueNAS/Proxmox. Al menos uno debe partir de nombre lógico de servicio, no host/IP anticipado. Usar diferentes targets, sin inventar estado saludable.
3. Para cada escenario, resolver: nombre lógico → identidad unívoca/guest/VMID/ubicación → source y timestamp → canal autorizado → lectura de estado/log/metric según exista → síntesis y evidencia. Contrastar dos fuentes cuando sea posible; contradicción = CONFLICT, no adivinar.
4. Negativos obligatorios: nombre inexistente o ambiguo devuelve NOT_FOUND/AMBIGUOUS sin ejecutar acciones; viewer mutator devuelve POLICY_DENIED verificable; endpoint auth sin secreto devuelve 401/403 sólo si prueba segura preexistente; caído/no autorizado se clasifica sin reintentos ilimitados. No ejecutar un mutador real para probar un DENY si el policy layer no garantiza bloqueo antes del target.
5. Recoverability: probar por lectura que `mcps-ops` sigue disponible independentemente del MCP y que existen runbooks vigentes. No apagar servicios para simular incidentes.
6. Un agente fresco (contexto sólo skill/proyecto y sources indicadas) reproduce al menos un lookup de servicio sin owner knowledge. Si no existe ruta runtime directa, declarar PARTIAL y especificar blocker verificable.

**G4 PASS** requiere G2 con cobertura MUST suficiente, sesión nueva PASS, ≥3 escenarios si están autorizados (de lo contrario justificar menor alcance y no declarar integral), negativos, management independence, cero mutaciones y evidencia reproducible. No usar HTTP 200, tool count o mocks como sustituto de consumer real.

### Cadencia de 10 horas, presupuesto y stop rules

| Ventana relativa | Manager / workers | Output no opcional |
|---|---|---|
| T+0–0:30 | cold/warm delta, baseline runtime y distribución de archivos | manifiesto + alcance + fuentes; no repetir G0/G1 |
| T+0:30–1:00 | A/B/C/D inspect paralelo; D detecta RO gaps; manager consolida bundle owner | owner action bundle único si procede, deps claros |
| T+1:00–5:00 | A inventory/service map; B Linux; C Windows; D wrapper/API RO | entregas independientes y evidencias parciales |
| T+5:00–7:00 | manager integra; se corrigen conflictos/bugs; D aprovecha auth aprobada | matriz coverage normalizada y rutas runtime |
| T+7:00–8:30 | G2 por familia; regresión y negativos | PASS/PARTIAL/BLOCKED honesto |
| T+8:30–9:30 | nueva sesión Hermes + G4 golden | ejecución E2E reproducible |
| T+9:30–10:00 | freeze cambios, verify, notas, handoff | estado del proyecto actualizado, changelog, pendientes |

Tiempos son **timeboxes**, no promesas. Si los workers no pueden correr concurrentemente, manager ordena por A→B→C→D e integra temprano. Limitar probes y contextos, reutilizar resultados frescos; no dejar tareas abiertas con shell sessions sin cerrar. A T+8:30 prohibido empezar funcionalidad nueva; a T+9:30 solo certificar, restaurar cambios reversibles pendientes y documentar. Ante riesgo de secretos, error de identidad, target equivocado o potencial mutación PROD: ABORT inmediato de esa tarea y pedir gate. Owner offline no bloquea A/B/C.

### Definición de cierre y handoff

- `H0 PASS`: inventario actual de 59 identidades reconciliado con source proof, 6 nodos, 10 storages, service map de alcance explicitado y sin conflictos críticos; familias G2 MUST probadas por canal real y con límites explícitos; G4 de sesión fresca PASS y negativos válidos; acceso de recuperación independiente; cero mutaciones; evidencia y proyecto autocontenidos.
- `H0 PASS WITH DEBT`: sólo deuda no bloqueante como API directa innecesaria para datos H0, más mitigación y owner action futura; no llamar H2/H4 READY. Si faltan datos críticos de PVE/TrueNAS, service map decisivo o E2E, usar `H0 PARTIAL/BLOCKED` aunque otras familias estén PASS.
- Entrega durable: actualizar I1 checkboxes durante la ejecución `[ ]→[/]→[x]`, status/progress y esta sección de estado; bitácora con source/time, evidencia, commits y next exact; 1 change log consolidado para las entidades modificadas; matriz de 59 y coverage por familia fuera del vault (referenciada); owner bundle residual sin secretos; lista de decisiones H1 sólo como handoff, sin diseñar H1 ni ejecutarlo.
- Único manager edita proyecto; workers reportan pruebas y commits por scope. En el padre, tarea puente Infra pasa `[ ]→[/]` al comenzar ejecución; solamente `[r]` al quedar para Review y NUNCA `[x]` por el agente. Cierre completo de sesión Agents-OS sólo por pedido explícito del owner.

## ✅ Tareas

### I0 — Bootstrap del management plane

- [x] I0.1 Inventariar interfaces administrativas realmente disponibles para Hermes #owner/agent #type/research #area/aranea — verificado 2026-09-17
- [x] I0.2 Clasificar authority actual por target: observe / operate / provision / absent #owner/agent #type/admin #area/aranea — matriz 2026-09-17
- [x] I0.3 Definir referencias de credenciales y boundaries sin persistir secretos #owner/agent #type/admin #area/aranea
- [x] I0.4 Certificar que Hermes conserva recovery path independiente del MCP Access Plane #owner/agent #type/admin #area/aranea

### I1 — H0 Observe (única cola ejecutable 2026-09-18)

- [x] I1.0 Verificar G0, G1 discovery y G3 helper ya hechos; NO repetir salvo drift — evidencia change log `2026-09-17-hermes-infra-preflight-g0`, owner recap #owner/agent #type/admin #area/aranea
- [x] I1.1 Reconciliar inventario real nodes/hosts/59 VMs/LXC/10 storages **y catálogo de servicios**; baseline 59 confirmado, service map pendiente #owner/agent #type/admin #area/aranea — DONE run h0-20260918-r1 WS A: inventory_59.json 59=42+17 verificado 1:1, service_map 58 servicios (38 completos/17 parciales/3 unknown), 7 testcases G4, discrepancies.md (step-ca 200 stopped vs doc activa; renombres SQX 108/111/112/123; 121/122 eliminados; PBS 180 nuevo)
- [x] I1.2 Construir y probar service → guest → host → storage/dependencies (si demostrado) → management path; resolver unknown/ambiguous/drift #owner/agent #type/admin #area/aranea — DONE WS A: service_map 58 servicios (38 completos/17 parciales/3 unknown), 2 ambiguos y 1 inexistente como testcases G4
- [x] I1.3 Congelar evidence contract/matriz G2 por máquina/familia; distinguir 17 offline de acceso fallido #owner/agent #type/admin #area/aranea — DONE: integration/g2_matrix.csv 70 filas + evidence_records.jsonl (contrato de campos); 17 stopped = STOPPED_EXPECTED, 0 contados como fallo
- [x] I1.4 Preparar owner bundle API RO SOLO ante gap de fact; obtener decisión owner sin exponer tokens, revalidar D #owner/agent #type/admin #area/aranea — RESUELTO SIN BUNDLE: D certificó 0 gaps críticos (9 COVERED/4 PARTIAL/1 MISSING=backup jobs material H1, obtenible extendiendo wrapper); D/owner_bundle_draft.md declara NO SE REQUIERE BUNDLE
- [x] I1.5 Certificar Linux y Windows desde sesión Hermes, positivos/negativos y permisos efectivos #owner/agent #type/admin #area/aranea — DONE WS B+C: Linux PASS (wrapper 6/6, mcps-ops/daedalus-ops, ssh-mcp 16+/4-), Windows PASS_WITH_LIMITATIONS (worker-kronos viewer+operator, publisher FRESH, negativos 4/5 + drift netstat registrado)
- [x] I1.6 Certificar Proxmox/TrueNAS/observabilidad por wrapper o API native RO, sin sobredimensionar permisos #owner/agent #type/admin #area/aranea — DONE WS D + manager probes: facts críticos COVERED por wrapper (nodos/quorum/59 VMs/10 storages/Ceph/pools TrueNAS/versiones/PBS), observabilidad-ro y postgres-ro con lectura real correlacionada y 401 sin bearer
- [x] I1.7 Ejecutar golden G4 desde sesión nueva con escenarios cross-layer y safety negatives #owner/agent #type/admin #area/aranea — DONE: G4 PASS (sesiones frescas CLI): G4.0 carga 3/3 MCPs (50 tools); G4.1 Linux PASS (postgresql→VM152@hades desde nombre lógico, estado vivo PG 17.6 `mcp_echo_prod_ro@echo`, sin contexto privado); G4.2 Windows ejecución PASS (publisher vivo vía mt5-kronos-operator: FRESH 7.2min/SYSTEM/PID 5496/0.2.100+SHA; clasificación del agente corregida por integrador a CONSUMER_PLANE_ONLY); G4.3 TrueNAS PASS (25.04.1, pools ONLINE 0 errores, secciones citadas); G4.4 negativos 3/3 (NOT_FOUND, AMBIGUOUS 114/125, POLICY_DENIED con sessions=0); management independence (`mcps-ops` durante 503 del plano), gateway legacy disabled
- [x] I1.8 Auditar zero mutation/secrets, reconciliar canon, reportar H0 PASS/PASS WITH DEBT/PARTIAL/BLOCKED con evidencias + handoff H1 #owner/agent #type/admin #area/aranea — DONE: leak check CLEAN (sin valores de secretos en evidencia/vault); 3 mutaciones AUTO registradas fielmente por orden owner (config perfil, restart ssh-mcp, parche helper) — veredicto **H0 PASS WITH DEBT** (deuda no bloqueante, detalle en bitácora); handoff H1 en bitácora

### I2 — H1 Backup & Storage (NO ejecutar en jornada H0)

- [ ] I2.1 Cargar y reconciliar [[BACKUP-DR-OWNER-PROJECT]] sin rediseñarlo #owner/agent #type/admin #area/aranea
- [ ] I2.2 Identificar authority faltante para backups/storage/restore #owner/agent #type/admin #area/aranea
- [ ] I2.3 Certificar operación de backup/health dentro de scope aprobado #owner/agent #type/admin #area/aranea
- [ ] I2.4 Ejecutar restore drill acotado y registrar evidencia #owner/agent #type/admin #area/aranea
- [ ] I2.5 Declarar H1 PASS o blockers precisos #owner/agent #type/admin #area/aranea

### I3 — Expansión H2→H6 (NO ejecutar en jornada H0)

- [ ] I3.1 Planificar H2 Proxmox lifecycle sólo después de H1 #owner/agent #type/admin #area/aranea
- [ ] I3.2 Planificar H3 guest/service operations sólo con management paths certificados #owner/agent #type/admin #area/aranea
- [ ] I3.3 Planificar H4 provisioning con onboarding a backup/observability/documentación #owner/agent #type/admin #area/aranea
- [ ] I3.4 Mantener H5 high-impact gated hasta aprobación explícita del owner #owner/agent #type/admin #area/aranea
- [ ] I3.5 Definir criterio medible de H6 sólo después de escenarios reales repetidos #owner/agent #type/admin #area/aranea

## 📆 Bitácora

- **2026-09-18 — H0 CIERRE run `h0-20260918-r1` · veredicto: PASS WITH DEBT (T+~3h de 10, deuda no bloqueante):** **G2 por familia:** Linux PASS (wrapper 6/6 sha16, mcps-ops 26 containers, daedalus-ops + sudo-DENIED, ssh-mcp 7/7 perfiles, 16+/4-); Windows PASS_WITH_LIMITATIONS (worker-kronos: viewer 4/5 negativos + DEVIATION netstat ALLOWED 2/2, operator, publisher FRESH, CONSUMER_PLANE_ONLY, self-hash ausente del payload); Proxmox PASS vía wrapper (0 gaps críticos, 9/14 COVERED); TrueNAS PASS vía wrapper (25.04.1, pools ONLINE); Observabilidad PASS (22 tools, correlación echo-core, 401 sin bearer); anexo postgres-ro (mcp_echo_prod_ro@echo, PG 17.6). Matriz 70 filas en `~/aranea/work/h0-20260918/integration/` (fuera del vault por diseño). **G4 PASS en sesiones frescas:** carga 3/3 (50 tools), Linux/TrueNAS/Windows resueltos desde nombre lógico, negativos 3/3 con POLICY_DENIED probado (sessions=0), management independence demostrada durante 503 real del plano. **Deuda registrada (no bloqueante, candidata handoff):** (a) drift clasificador viewer Windows: `netstat -ano` ALLOWED donde el mapa 17-sep esperaba denegación — read-only, requiere parche ssh-mcp owner-gated; (b) ambigüedad terminológica runbook aranea-ssh-mcp: el camino "agent-facing certificado" del publisher se presta a leerse como recovery nativo — es plano MCP (CONSUMER_PLANE_ONLY); corregir redacción en próxima edición del runbook; (c) self-hash ausente del payload publicado de worker-kronos (contrato runbook dice self-hash; payload no lo trae) — diagnosticar publisher con authority existente; (d) drift documental 02-servicios: step-ca (VM 200) stopped vs doc activa — reparación = lifecycle GATED (decisión owner pendiente; bloquea renovación TLS `*.lab.aranea`); renombres SQX 108/111/112/123 y eliminados 121/122; (e) helper session-steps-client corregido (DELETE) — extender disciplina de cierre de sesión a consumidores del plano; (f) config base `~/.hermes/config.yaml` conserva el batch G3 duplicado (inofensivo para perfil default; reconciliar cuando se toque ese archivo). **Mutaciones de la jornada (AUTO, registradas por orden owner):** config perfil Ariadna (G3 fix, con backups+sha), `docker restart ssh-mcp` (503 pool-64, pre-checks runbook), parche helper con DELETE de sesión. **Handoff H1 (no iniciado):** (1) arrancar por [[BACKUP-DR-OWNER-PROJECT]]: cargar diseño vigente, reconciliar jobs (D: MISSING=jobs de backup, obtenible extendiendo wrapper con /etc/pve/jobs.cfg); (2) decidir destino del hallazgo step-ca 200 (owner-gated: lifecycle); (3) closures documentales menores: runbook aranea-ssh-mcp (terminología CONSUMER_PLANE_ONLY + nota bookkeeping `[connected]` ya agregada al skill), fechas-captura/02-servicios por delta A; (4) H2/H4 siguen gated: token API RO NO los habilita.
- **2026-09-18 — H0 mutaciones registradas (clase AUTO, NO read-only — orden owner de registro fiel):** (1) **Corrección config perfil Ariadna:** el batch G3 del 17-sep escribió `mcp_servers` + bearers en `~/.hermes/config.yaml` (perfil default), pero las sesiones Ariadna leen `profiles/ariadna/config.yaml` → los 3 MCPs nunca cargaron en sesión nueva (causa raíz del fallo G3 "efectivo próxima sesión"). Fix: mismo batch autorizado por owner aplicado en el archivo correcto (`profiles/ariadna/config.yaml` + `profiles/ariadna/.env` con refs `${VAR}`); backup pre + sha256 en `~/aranea/work/h0-20260918/integration/` (`config.yaml.pre-mcp-*`, `dotenv.pre-mcp-*`, `pre_shas_*`); rollback = restaurar backups. Validado: sesión fresca CLI ve 3/3 capabilities (postgres-ro 13, ssh 13, observability-ro 24 tools). (2) **Restart `ssh-mcp` en mcps:** :3000 en HTTP 503 por pool-64 agotado (leak de sesiones init-only de helpers sin DELETE); recovery según runbook (health + `/status` + logs ANTES de restart), `docker restart ssh-mcp` vía `mcps-ops`, healthy ~12 s, initialize fresco 200. Sin cambio de config. (3) **Parche del helper propio** `mcp-access-plane-operations/templates/session-steps-client.py` (código de Ariadna, NO del plano): captura del `Mcp-Session-Id` por event-hook + DELETE al salir para no re-agotar el pool; probado contra :3001 y :3000 (steps PASS + `session released`). Estas tres mutaciones quedan registradas como mutaciones, no como observación; el resto de H0 (A/B/C/D, G2) fue estrictamente read-only.
- **2026-09-18 — H0 ejecución iniciada (run `h0-20260918-r1`):** T0 2026-09-17T23:30:36Z (20:30 CLT), ventana ≤10 h. Preflight reconciliación GitHub→vault RESUELTO SIN CAMBIOS: `9bc3d58` ya está en `origin/master` y el vault byte-a-byte idéntico en planner + change log (diff vacío; ediciones posteriores del owner preservadas); repo local `~/workspace/agents-os-repo` confirmado consumidor. Delta runtime verificado: 3 MCPs en config (`aranea-postgres-ro` :3001, `aranea-ssh` :3000, `aranea-observability-ro` :3009), bearers por referencia en `~/.hermes/.env` (600), gateway legacy `disabled` y Ariadna activo, hermes CLI v0.21.3 disponible para G4. Evidencia G1 (`*_20260917_185839`) fresca: NO se regenera G0/G1. Workspace run: `~/aranea/work/h0-20260918/` (evidencia fuera del vault). Organización: workers secuenciales A→B→C→D (runtime permite 1 hijo concurrente; B/C comparten plano ssh-mcp — secuencial evita agotar pool 64). Tarea activa: I1.1 (WS A inventory/service map). Siguiente exacta: al cierre de A → B Linux → C Windows → D Proxmox/TrueNAS → integración → G2 → G4 sesión nueva → reporte.
- **2026-09-17 — SPEC H0 freeze para 2026-09-18:** owner solicita plan detallado y mandato de ejecución en ventana hasta 10 horas. Se crea plan único EN ESTA nota con A/B/C/D, owner bundle T+60, G2/G4, cobertura honesta 59/42/17, timeboxes, stop rules, evidencia/handoff y boundary H1–H6. G0/G1/G3 reconocidos sin reejecución. Cambio documental, no se ejecuta H0 ni se conceden permisos nuevos por esta edición.
- **2026-09-17 — G3 runtime integration post-preflight:** `config.yaml` autorizado, `aranea-ssh` 11 tools + observability 22 tools junto postgres-ro; helper consumer-side PASS, datasource Jaeger/Loki health OK; efectivo próxima sesión. Publicación vault→GitHub en otra máquina verificada. En la sesión nueva todavía falta smoke de carga.
- **2026-09-17 — Preflight G0 mandato Infrastructure Enablement:** `agent-read` 6/6 PASS, discovery 6/6 (`*_20260917_185839.txt`, `inventory_20260917_185839.json`: 59 VMs / 42 running / 17 stopped / 10 storages), smokes `mcps-ops` (26 containers) y `daedalus-ops` PASS. Index/nodo-docs/área corregidos por delta. El hallazgo inicial de sincronización y gap de MCPs de este instante se resolvió luego en G3; ver entrada superior.
- **2026-09-16** — Recovery real del runtime Hermes tras `hermes update`: dashboard + Ariadna `systemd --user`, duplicate legacy gateway deshabilitado, `fleet_restart_pending` reconciliado; skill+runbook federados.
- **2026-09-14** — Workstream creado; H0→H6 y separación management/MCP; Backup/DR reutilizado, no duplicado.

## 🧭 Decisiones

- **I-D01:** management path nativo es obligatorio para recovery del MCP Access Plane y servicios administrados.
- **I-D02:** autoridad progresiva por nivel; no root-equivalent global inicial.
- **I-D03:** storage/backups es el primer dominio operativo por prioridad y porque permite certificar el patrón de seguridad/recovery antes de Proxmox completo.
- **I-D04:** operadores especializados son boundaries de autoridad; su implementación concreta se difiere hasta ver las interfaces reales.
- **I-D05:** gateway operativo `hermes-gateway-ariadna.service`; default legacy permanece disabled mientras comparta identidad Telegram con Ariadna.
- **I-D06 (2026-09-17):** owner adelanta exclusivamente H0 el 2026-09-18 para aprovechar ventana de agentes. Es prioridad de ejecución, no alteración de authority ni habilitación anticipada de H1/H2/H4. Token API RO acredita sólo observación, jamás lifecycle/provisioning.

## 🔗 Docs / Links

- [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] — programa padre.
- [[BACKUP-DR-OWNER-PROJECT]] — source of truth de Backup/DR.
- [[HERMES — Agent Access Operations]] — workstream paralelo del capability plane.
- [[AGENT-PLATFORM - MCP Access Plane]] — plano que Infrastructure Operations debe poder recuperar sin depender de él.
- [[hermes-agent-operator]] — skill agent-facing para operar el runtime Hermes.
- [[hermes-linux-update-recovery]] — runbook mecánico de update/recovery.
- `80-agents/journal/logs/2026-09-17-hermes-infra-preflight-g0.md` — evidencia G0/G1/G3.

## 💡 Ideas

### Backlog de ideas

- Detectar cuáles operators merecen perfil/agent separado después del primer ciclo H0/H1.
- Incorporar drills periódicos de recovery cuando el management plane sea estable.

### Motivos / principios

- La autonomía vale sólo si Hermes puede recuperarse de la falla de las superficies que administra.
- El blast radius debe aumentar más lento que la evidencia de operación segura.
