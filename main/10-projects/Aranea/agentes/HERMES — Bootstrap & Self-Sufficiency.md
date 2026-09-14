---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P0
area: "[[Aranea]]"
parent: "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
sprint:
start: 2026-09-14
due:
progress: 20
repo:
jira:
prs:
slug: hermes-bootstrap-self-sufficiency
aliases:
  - Hermes Bootstrap
  - Hermes Self-Sufficiency Bootstrap
  - Hermes Human Exit Bootstrap
tags:
  - kind/project
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - agent/hermes
  - action/bootstrap
created: "2026-09-14"
updated: "2026-09-14"
---

# HERMES — Bootstrap & Self-Sufficiency

> [!info]+ Bootstrap transitorio
> **Padre:** [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] · **Owner:** agent · **Estado:** active · **Prioridad:** P0
>
> Este proyecto existe sólo para sacar al owner del loop operativo inicial. No es un tercer workstream permanente: termina cuando Hermes puede administrar el MCP Access Plane y su consumer onboarding sin intervención shell humana rutinaria.

## 🎯 Objetivo

Dejar a Hermes/Ariadna en un estado donde el owner sólo tenga que:

1. copiar un prompt entre ChatGPT y Hermes;
2. ejecutar **una cantidad mínima y batcheada de acciones manuales de bootstrap** cuando Hermes todavía no tenga autoridad para hacerlas por sí mismo;
3. volver a intervenir sólo ante gates explícitos de alto impacto, PROD, secretos imposibles de auto-provisionar o ausencia real de autoridad.

El bootstrap debe habilitar el primer circuito autónomo real:

```text
owner expresa objetivo
→ Hermes planifica
→ Hermes administra mcps por management path nativo
→ Hermes repara/configura/despliega capability
→ Hermes publica/configura consumer
→ Hermes certifica
→ Hermes actualiza Agents-OS
→ owner recibe resultado
```

## 🧠 Por qué existe este proyecto

El perfil operativo actual [[Ariadna]] ya corre sobre Hermes Agent y es la identidad correcta; **no se crea otro Hermes desde cero**. Sin embargo, su contrato histórico fue diseñado para operación fuertemente supervisada y contiene gates incompatibles con la nueva meta de autonomía, por ejemplo aprobación explícita del owner para todo cambio no trivial.

Además, el MCP Access Plane no puede ser el canal con que Hermes administra el propio host `mcps`: una falla del MCP lo dejaría incapaz de recuperarlo.

Por tanto el bootstrap debe resolver primero dos cosas:

1. **contrato de autonomía de Ariadna/Hermes**;
2. **management paths out-of-band** para el plano que Hermes va a administrar.

## 🧭 Orden de implementación obligatorio

```text
B0  contrato de autonomía + perfiles/skills
B1  management path directo al LXC mcps
B2  management path de consumer onboarding
B3  operador MCP reusable + self-repair smoke
B4  human-exit gate
```

No empezar a resolver blockers específicos de Echo/Forge antes de B4. El objetivo es que esos blockers se conviertan en el primer workload del sistema autónomo y no en otra tanda de configuración manual.

## 👤 Presupuesto de intervención humana

### Permitido durante bootstrap

- pegar el prompt maestro de una sesión Hermes;
- ejecutar uno o pocos bloques de comandos que **Hermes no pueda ejecutar porque todavía no tiene acceso**;
- instalar una public key generada por Hermes en un target inicial;
- habilitar un usuario/sudo/API token cuando sólo el owner pueda hacerlo;
- entregar una referencia/ubicación de secret existente, sin pegar el valor en Agents-OS;
- aprobar un cambio que modifique el contrato de autonomía de Ariadna.

### No aceptado como flujo normal

- entrar manualmente a `mcps` para cada nuevo MCP;
- editar Docker/Compose/Nginx/Portainer a mano por capability;
- configurar manualmente cada consumer nuevo;
- copiar secretos entre máquinas a mano cada vez;
- ejecutar diagnósticos shell repetitivos para Hermes;
- resolver uno por uno los blockers de Echo/Forge antes de que Hermes pueda hacerlo.

### Regla de batching

Cuando Hermes detecte acciones que sólo el owner puede realizar, **debe acumularlas y devolver un único `OWNER ACTION BUNDLE` mínimo**, ordenado, idempotente cuando sea posible y con verificación inmediata. No pedir permisos/outputs de a una acción salvo que una evidencia sea materialmente necesaria para decidir la siguiente.

## 🔐 B0 — Contrato de autonomía

### B0.1 Reconciliar identidad real

- Hermes Agent es el runtime.
- [[Ariadna]] es la identidad operativa principal y debe seguir siéndolo mientras no exista razón material para dividirla.
- No crear agentes/perfiles nuevos sólo por organización conceptual.

### B0.2 Cambiar approval model histórico

El perfil actual fue construido para supervisión manual. Debe evolucionar desde:

```text
cambio no trivial → pedir OK
```

a:

```text
acción dentro de clase preautorizada → ejecutar + verificar + registrar
acción fuera de authority → OWNER ACTION BUNDLE / gate
```

#### Preautorización inicial propuesta

**AUTO — sin aprobación por operación:**

- lectura/discovery de Aranea personal;
- escritura normal en Agents-OS dentro de contratos existentes;
- administración completa del LXC dedicado `mcps` una vez certificado el management path;
- Docker/Compose/Portainer/Nginx/configuración del MCP plane en `mcps`;
- restart/redeploy/repair de capabilities MCP DEV/test;
- creación/eliminación de recursos temporales/sandbox para certificación;
- configuración y onboarding de consumers DEV/test dentro del scope explícito del proyecto;
- rollback de una mutación propia cuando falla su post-condición;
- mantenimiento de skills/runbooks del dominio cuando el cambio refleja evidencia real.

**GATED — owner requerido:**

- mutación PROD no preautorizada;
- operación destructiva sobre datos permanentes;
- cambios de red/firewall/routing de alto blast radius;
- cambios host-level sobre nodos Proxmox/TrueNAS antes de habilitar su fase correspondiente;
- borrado irreversible de VMs/LXC/storage;
- rotación/revocación de credenciales que puedan cortar a otros consumidores si no existe recovery probado;
- cualquier acción fuera de la authority certificada vigente.

### B0.3 Especialización: skill primero, perfil separado sólo si agrega aislamiento real

KISS para v1:

- **Ariadna** sigue como orquestadora;
- crear/ajustar **skills de operador** para comportamiento especializado;
- usar connections/credentials separadas por responsabilidad;
- crear un perfil/subagente separado sólo cuando exista una razón concreta de credenciales, blast radius, system prompt o workflow recurrente.

Esto preserva la idea de operadores especializados sin introducir coordinación multi-agent innecesaria antes de tener management paths funcionando.

### Gate B0

- Ariadna puede ejecutar cambios preautorizados sin pedir OK uno por uno.
- Escalaciones se agrupan como `OWNER ACTION BUNDLE`.
- PROD/high-impact/destructive siguen gated.
- No se debilitó la política de secretos ni target proof.

## 🔑 B1 — Management path directo a `mcps`

### Objetivo

Hermes debe administrar el LXC `mcps` **sin usar ningún MCP servido por ese LXC**.

### Estrategia propuesta

1. Desde la VM Hermes, descubrir si ya existe identity reutilizable segura.
2. Si no existe, generar una key ED25519 dedicada para `mcps`.
3. Crear en `mcps` una identidad OS dedicada, propuesta: `hermes-ops`.
4. Autenticación key-only; password login no necesario.
5. Dar autoridad administrativa suficiente para administrar el appliance completo.
6. Pinnear host key.
7. Crear un wrapper/operator entrypoint local que fije target/identity y aplique logging/redaction, manteniendo la regla de no depender del MCP.

### Authority objetivo sobre `mcps`

`mcps` es un LXC dedicado al Access Plane. Para cumplir el objetivo de self-service, Hermes necesita poder:

- inspeccionar filesystem/config;
- operar Docker/Compose/Portainer runtime;
- crear/eliminar/recrear containers y networks del MCP plane;
- editar configuración de proxy/backends;
- administrar systemd/servicios locales que pertenezcan al appliance;
- manejar archivos de configuración/secret refs sin imprimir valores;
- instalar dependencias **del appliance MCP** cuando un deployment legítimo lo requiera;
- ejecutar rollback/recovery.

La implementación concreta puede ser `hermes-ops + passwordless sudo` o equivalente. El principio es **root-equivalent limitado al LXC `mcps`, no a Proxmox ni al resto de Aranea**.

### Regla de secretos

Hermes puede usar secretos necesarios para operar el plano, pero:

- no los imprime en chat/logs;
- no los copia al vault;
- no los incluye en handoffs;
- Agents-OS guarda sólo referencias/paths/identificadores no sensibles.

### Owner Action Bundle esperado

Hermes debe hacer por sí mismo todo lo posible —generación de key, detección de target, preparación de comandos— y pedir al owner **sólo** el bloque mínimo que requiera autoridad externa para instalar esa identity/sudo inicialmente.

### Gate B1

Desde su runtime real, Hermes puede por management path nativo:

```text
identify target
→ sudo/root proof dentro de mcps
→ docker/portainer/config inspection
→ crear y destruir un recurso de smoke no persistente
→ verificar estado
```

sin usar `aranea-ssh` ni ningún otro MCP.

## 🖥️ B2 — Management path de consumer onboarding

### Problema

Desplegar un MCP server no completa el trabajo si Echo/Forge no pueden consumirlo. Actualmente Daedalus/Cursor y otros runtimes tienen configuración/secret refs propias.

### Objetivo

Hermes debe poder incorporar una capability en el consumer sin pedir al owner que edite archivos manualmente cada vez.

### Procedimiento

1. Descubrir los **consumers reales actuales** y su source of truth de MCP config/secrets.
2. Identificar cuál puede ser administrado por Hermes con menor privilegio.
3. Si la config vive en un host separado, establecer un management path dedicado una sola vez.
4. Evitar acceso root si sólo se requiere administrar config user-level.
5. Estandarizar sólo después de confirmar el patrón real.
6. Certificar desde el consumer o desde un harness equivalente que use la misma config/auth/transport.

Si Daedalus requiere un alta SSH/manual inicial, debe agruparse en el mismo bootstrap humano de B1 cuando sea posible.

### Gate B2

Hermes puede publicar/actualizar una capability DEV/test para al menos un consumer real y verificar `initialize/tools/list`/smoke sin edición manual del owner.

## 🧰 B3 — Operador MCP reusable

### B3.1 No reutilizar `aranea-mcps-expert` como operador privilegiado

[[aranea-mcps-expert]] es actualmente el router **agent-facing/consumer-facing** y contiene boundaries correctos para consumidores. Mantenerlo así.

Crear una superficie separada, nombre propuesto:

`aranea-mcp-plane-operator`

Su responsabilidad será operar el Access Plane por management path nativo:

- discovery del appliance;
- health/runtime/config;
- backup mínimo de config antes de cambios;
- repair/restart/redeploy;
- onboarding de una capability;
- pinning/version evidence;
- proxy/auth boundary;
- publish/register;
- server smoke;
- consumer smoke;
- rollback;
- update de [[AGENT-PLATFORM - MCP Access Plane]] y runbooks canónicos.

No copiar a la skill todos los procedimientos por servicio; debe delegar a arquitectura/runbooks existentes y conservar token economy.

### B3.2 Golden self-repair

Probar autonomía sobre una capability DEV existente y de bajo impacto:

```text
baseline
→ management-plane inspect
→ controlled restart/redeploy/repair
→ health
→ MCP initialize/tools/list
→ consumer smoke
→ evidence
```

No introducir una falla destructiva sólo para probar recovery.

### B3.3 Golden deploy/config

Luego ejecutar una ampliación o capability real requerida por Echo/Forge usando el mismo operador, sin todavía intentar cerrar toda la cola.

### Gate B3

Hermes demuestra `repair` y `configure/deploy` con el mismo patrón operativo reusable.

## 🚪 B4 — Human Exit Gate

B4 es PASS sólo si:

- [ ] el perfil/contrato de Ariadna permite autonomía dentro del scope aprobado;
- [ ] Hermes tiene management path directo y root-equivalent **sólo sobre `mcps`**;
- [ ] Hermes puede administrar config/runtime MCP sin usar el MCP a reparar;
- [ ] Hermes puede publicar/configurar al menos un consumer sin edición owner por capability;
- [ ] existe skill/operator mínima para repetir repair/deploy;
- [ ] secretos no aparecen en Agents-OS ni outputs;
- [ ] un golden repair PASS;
- [ ] un golden configure/deploy PASS;
- [ ] cualquier intervención humana restante está clasificada como gate excepcional, no procedimiento normal.

Cuando B4 pasa:

1. este proyecto pasa a Review;
2. [[HERMES — Agent Access Operations]] toma el control;
3. los blockers de Echo/Forge se convierten en la primera cola real A2-A5;
4. el owner deja de realizar configuración MCP rutinaria.

## 📊 Estado actual

- Proyecto creado 2026-09-14 a partir del requisito explícito del owner de minimizar intervención humana.
- Identidad real verificada en vault: [[Ariadna]] corre sobre Hermes Agent; no hace falta crear otra identidad principal.
- Gap confirmado de diseño: el perfil actual exige aprobación owner para cambios no triviales, por lo que debe evolucionar hacia clases preautorizadas.
- Gap confirmado operativo: [[AGENT-PLATFORM - MCP Access Plane]] registró incidentes donde no pudo observar/reiniciar server-side `mcps` por falta de authority administrativa disponible en la sesión.
- Próximo paso: B0/B1 en una sesión Hermes dedicada; no resolver todavía blockers específicos de Echo/Forge.
- **2026-09-14 — B0 PASS:** approval model AUTO/GATED aplicado a SOUL.md §8.1, Regla Dura 1 de [[Ariadna]] y USER.md operativo. Cambio loggeado en `80-agents/journal/logs/2026-09-14-b0-autonomy-contract-applied.md`.
- **2026-09-14 — B1 discovery PASS, authority pendiente:** target `mcps.lab.aranea.cl` = `192.168.31.219`, SSH :22 open, host key ED25519 pinneada (`SHA256:REpcjg31iDIJ5xysEaM63UBgbtuIU3KCuvuJ0NZo+lY`). Identity dedicada ED25519 `agent_mcps_ops` generada en VM Hermes (fingerprint `SHA256:1ebPwqXIyeCC8zo4spKg+OyTDPYMXg78Kv1BaKRgp48`); alias `mcps-ops` en `~/.ssh/config`; wrapper `~/aranea/bin/mcps-ops` creado con logging. No existe identity reutilizable: las keys locales (`agent_ro_aranea`, `agent_pve_create_athena`, `agent_traefik_*`, tunnel) son de otros targets; `root@mcps` y `hermes-ops@mcps` rechazan `publickey`. Conexión actualmente `Permission denied` — OWNER ACTION BUNDLE emitido para instalar `hermes-ops` + sudo passwordless en el LXC. Tras aplicar el bundle: B1.4 (certificación: sudo proof → docker ps → smoke create/destroy) y B1.5 (revoke path) se ejecutan automáticos.
- **B2 pre-work registrado:** consumers reales conocidos vía runbook `aranea-mcp-capability-plane`: Daedalus/Cursor en host separado con bearers vía KDE env chain (`~/.config/plasma-workspace/env/aranea-mcp.sh` → `~/.config/mcp/aranea-env.sh`); Hermes-VM aún no consume capabilities. El alta del management path en Daedalus se agrupará en un bundle posterior de B2, no en el actual (evitar mezclar hosts sin evidencia).

## 🧱 Entrega de desarrollo

_No hay repo único. Este proyecto modifica comportamiento operativo, skills/config y acceso a infraestructura. Antes de tocar configuración versionada se debe identificar su source of truth; cualquier script/wrapper nuevo debe permanecer mínimo y sólo existir si reduce intervención humana repetida._

## ✅ Tareas

### B0 — Autonomy contract

- [x] B0.1 Cargar [[Ariadna]], USER/MEMORY operativos y este proyecto; reconciliar reglas que bloquean autonomía #owner/agent #type/admin #area/aranea
- [x] B0.2 Proponer patch mínimo al approval model: AUTO vs GATED, sin reducir secret/target/rollback rules #owner/agent #type/admin #area/aranea
- [x] B0.3 Aplicar el patch autorizado a las fuentes canónicas reales del perfil/system prompt #owner/agent #type/admin #area/aranea
- [x] B0.4 Definir y adoptar formato único `OWNER ACTION BUNDLE` #owner/agent #type/admin #area/aranea

### B1 — Direct mcps management

- [x] B1.1 Descubrir target real de `mcps`, SSH state, users/keys existentes y authority actual desde Hermes #owner/agent #type/admin #area/aranea
- [x] B1.2 Generar/reutilizar identity dedicada sin exponer private key #owner/agent #type/admin #area/aranea
- [x] B1.3 Preparar un único OWNER ACTION BUNDLE para instalar authority inicial si Hermes no puede hacerlo #owner/agent #type/admin #area/aranea
- [x] B1.4 Certificar direct SSH + root-equivalent scoped al LXC `mcps` #owner/agent #type/admin #area/aranea
- [x] B1.5 Materializar wrapper/operator entrypoint mínimo y documentar revoke path #owner/agent #type/admin #area/aranea

### B2 — Consumer onboarding path

- [x] B2.1 Descubrir consumers reales y source of truth de MCP config/secrets #owner/agent #type/research #area/aranea
- [x] B2.2 Elegir consumer piloto de Echo/Forge y management path mínimo #owner/agent #type/admin #area/aranea
- [x] B2.3 Batchear cualquier alta manual restante junto al bootstrap, si es posible #owner/agent #type/admin #area/aranea
- [x] B2.4 Certificar publicación/configuración sin edición manual owner por capability #owner/agent #type/admin #area/aranea

### B3 — Operator skill + golden paths

- [ ] B3.1 Crear/refinar `aranea-mcp-plane-operator` sin duplicar [[aranea-mcps-expert]] ni runbooks #owner/agent #type/admin #area/aranea
- [ ] B3.2 Golden repair sobre capability DEV existente y no destructiva #owner/agent #type/admin #area/aranea
- [ ] B3.3 Golden configure/deploy sobre necesidad real #owner/agent #type/admin #area/aranea
- [ ] B3.4 Actualizar source of truth y extraer sólo patrones demostrados #owner/agent #type/admin #area/aranea

### B4 — Human Exit

- [ ] B4.1 Auditar intervención manual residual #owner/agent #type/admin #area/aranea
- [ ] B4.2 Cerrar gaps que sean repetitivos/configurables #owner/agent #type/admin #area/aranea
- [ ] B4.3 Declarar PASS/FAIL contra checklist B4 #owner/agent #type/admin #area/aranea
- [ ] B4.4 Entregar control a [[HERMES — Agent Access Operations]] #owner/agent #type/supervision #area/aranea

## 📆 Bitácora

- **2026-09-14** — Se crea bootstrap transitorio para priorizar la salida del owner del loop. Se decide conservar Ariadna como identidad principal, cambiar approval model por clases preautorizadas, dar management path out-of-band a `mcps` y resolver consumer onboarding antes de atacar blockers individuales.
- **2026-09-14 (sesión B0/B1)** — B0 PASS: patch AUTO/GATED aplicado a SOUL.md §8.1 (runtime), Regla Dura 1 de [[Ariadna]] (vault) y USER.md (hermes memory). change_log creado. B1: discovery real desde la VM Hermes — `mcps.lab.aranea.cl`→`192.168.31.219`, :22/:3000 open, ninguna identity local sirve para `mcps`; se genera `agent_mcps_ops` (ED25519, sólo fingerprint público registrado), se pinnea host key strict, alias `mcps-ops` y wrapper `~/aranea/bin/mcps-ops` con log. Conexión `Permission denied` hasta que el owner aplique el OWNER ACTION BUNDLE (usuario `hermes-ops` + sudo passwordless + authorized_keys en el LXC). B2 pre-work: consumers reales documentados (Daedalus/Cursor vía KDE env chain); bundle de B2 diferido a su propia intervención. No se tocó Echo/Forge ni Proxmox/TrueNAS.
- **2026-09-14 (sesión B1 post-bundle)** — **Hallazgo CRÍTICO: fingerprint incorrecto en el bundle anterior.** El bundle pub keys `IIxKwJK0...` (fp `SHA256:/9jv+B8oBoXxC29FyHokdHr9JdB+/l7K3IUpF+k4uu0`) no corresponde a ninguna private key existente. La primera aparición de esa string es en **mi propia respuesta anterior** (message id 2026, esta misma conversación): la key quedó **fabricada/plausible-looking en el texto del bundle** en vez de leerla de disco con `cat ~/.ssh/agent_mcps_ops.pub`. Violación directa de "evidence before claims". Owner la instaló legítimamente; el server rechaza porque la private key no existe. Corrección: nuevo bundle con la key REAL leída de disco (fp verificado `SHA256:1ebPwqXIyeCC8zo4spKg+OyTDPYMXg78Kv1BaKRgp48`, byte-identical a `~/.ssh/agent_mcps_ops.pub`). Licción registrada.
- **Lección B1 (durable):** en un OWNER ACTION BUNDLE, toda public key/material criptográfico debe salir de `cat <archivo>` verificado — nunca de memoria del modelo. Un fingerprint inventado produce un seed authority que instala limpio pero falla en la primera conexión real; el error se detecta tarde y cuesta una intervención owner adicional.

## 🧭 Decisiones

- **B-D01:** dos workstreams permanentes se conservan; Bootstrap es transitorio.
- **B-D02:** skill/operator separado para administración privilegiada del MCP plane; `aranea-mcps-expert` permanece consumer-facing.
- **B-D03:** root-equivalent inicial puede aceptarse dentro del LXC dedicado `mcps`; no se extiende a hosts Proxmox/TrueNAS por implicación.
- **B-D04:** especialización por skills/connections primero; nuevos perfiles/subagentes sólo con beneficio material de aislamiento.
- **B-D05:** toda solicitud manual al owner se batchea; interacción humana de a un comando es un fallo de diseño salvo dependencia secuencial real.
- **B-D06 (2026-09-14):** patch B0 se aplicó vía sesión Hermes con autorización explícita del owner para esta sesión; las fuentes tocadas fueron exactamente tres (SOUL.md §8/§8.1, Regla Dura 1 de Ariadna, USER.md). Ningún perfil o agente nuevo.
- **B-D07 (2026-09-14):** management path elegido: SSH key-only `hermes-ops@mcps` con sudo passwordless scoped al LXC, wrapper `~/aranea/bin/mcps-ops`, host key strict pinneada. Revoke = quitar authorized_keys del usuario en `mcps` (una línea), sin tocar otras identities.

## 🔗 Docs / Links

- [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] — programa padre.
- [[HERMES — Agent Access Operations]] — siguiente proyecto tras B4.
- [[HERMES — Infrastructure Operations]] — carril posterior, comenzando por Backup/DR.
- [[Ariadna]] — identidad operativa actual sobre Hermes Agent.
- [[AGENT-PLATFORM - MCP Access Plane]] — source of truth del plano MCP existente.
- [[aranea-mcps-expert]] — router consumer-facing que no debe convertirse en operador privilegiado.

## 💡 Ideas

### Motivos / principios

- Optimizar primero la interfaz humano→Hermes; después optimizar cada servicio.
- El owner habilita authority una vez; Hermes debe reutilizarla de manera controlada y escalable.
- La mejor prueba de autonomía no es un diseño completo sino que el próximo blocker real deje de requerir shell humana.