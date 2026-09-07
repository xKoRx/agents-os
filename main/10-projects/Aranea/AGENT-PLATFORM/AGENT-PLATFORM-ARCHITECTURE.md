---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM-OWNER-PROJECT]]"
related:
  - "[[AGENT-PLATFORM-OWNER-PROJECT]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[30-resources/aranea/00-index]]"
  - "[[echo-forge]]"
aliases:
  - Aranea Agent Platform Architecture
  - Arquitectura Agent Platform
tags:
  - kind/doc
  - area/aranea
created: "2026-08-23"
updated: "2026-08-23"
---

# AGENT-PLATFORM-ARCHITECTURE

%% Naming: AGENT-PLATFORM-ARCHITECTURE es el link canónico; variantes humanas van en aliases. %%

## Propósito

Diseño objetivo **v1** de la **Aranea Agent Platform**: una VM Linux dedicada a workloads agénticos que evoluciona hacia el nodo central de una plataforma personal de agentes. Producido en la sesión de discovery/arquitectura del 2026-08-23 (fases F0-F2 del roadmap); todas las decisiones quedan como **propuestas** hasta pasar sus gates de owner. El estado ejecutable y el roadmap viven en [[AGENT-PLATFORM-OWNER-PROJECT]]; este documento es el diseño de referencia.

## Contenido

Este documento reúne la arquitectura objetivo, sus planos, el diseño inicial de la VM, los riesgos, las decisiones propuestas, las preguntas abiertas y las fuentes que deben verificarse antes de cada gate del owner.

## Contexto real (evidencia del vault)

Fuente primaria: [[30-resources/aranea/00-index]] (captura 2026-06-30, drift 0d al momento de esa captura) y sus subdocs de topología/servicios. Hechos relevantes para esta plataforma:

- Cluster: 5 nodos Proxmox (athena, zeus, hera, kronos, hades) + TrueNAS VM + hermes-vm = 7 máquinas · 302 threads / 767 GB RAM / ~12 TB útil.
- **hera** está muy subutilizada: 96 GiB RAM available y `local-lvm` de 363 GB al 29% (~258 GB libres); documentada como candidata natural para absorber carga si hades se congestiona ([[30-resources/aranea/01-topologia/nodo-hera]]).
- **hades** concentra los servicios IA/ML (echo, docker-echo-dev, argus, mcps, temporal, ubuntu-dev) y opera a ~74% RAM; la concentración es alerta conocida.
- Ya existe un nodo agéntico: **hermes-vm** (192.168.31.122, rol "Agente IA"), donde corren perfiles Hermes/Ariadna y skills operativas de Aranea.
- Red: LAN única 192.168.31.0/24; DNS Pi-hole (LXC 149 en athena) con wildcard `*.lab.aranea`; Traefik (LXC 115 en athena) con certificados step-ca internos y filtro `lan-only@file`; firewall OPNsense (VM 130 en athena). Política vigente: no publicar servicios a Internet.
- WireGuard/Tailscale: sin evidencia en la documentación capturada (marcado "necesita refresh"); no asumir que existe.
- Temporal ya corre como servicio (qemu/158 en hades) para workflows durables del ecosistema.
- Restricciones owner vigentes (no negociables): NO comprar hardware nuevo, NO migrar TrueNAS a bare-metal, NO cambiar la cantidad de servidores. Crear una VM en hypervisors existentes respeta estas reglas.
- Proyecto [[BACKUP-DR-OWNER-PROJECT]] está design-frozen esperando decisiones owner (tickets 018-021); la integración de backup de esta VM se engancha ahí cuando ejecute.

## Principios arquitectónicos

1. **Agents OS es control plane y permanece ortogonal**: constitución, políticas, roles, lifecycle, gates, decisiones, evidencia, handoffs, skills, gobernanza. Ningún runtime (Harness, Codex, Claude Code, ZCode) lo reemplaza ni lo acopla a sus APIs internas.
2. **Buy/adopt before build**, sin sacrificar ownership arquitectónico: adoptar herramientas existentes; construir solo la capa mínima que falte y demostrar el gap primero.
3. **KISS/YAGNI por fases con gates**: nada masivo adelante; cada fase termina en gate verificable antes de la siguiente.
4. **Superficie mínima**: no publicar nada a Internet; privilegios por capacidad; ningún workflow de agente como root.
5. **Secretos nunca en el vault** ni en logs ni en prompts; el vault guarda referencias seguras.
6. **Una fuente canónica por hecho**: procedimientos en skills/runbooks, estado en proyectos, diseño aquí; enlazar, no duplicar.
7. **Capability contract separado del runtime adapter**: lo que hace una capacidad se define una vez; cómo se conecta a cada runtime es un adapter intercambiable.
8. **Version pinning obligatorio** en runtimes jóvenes (DeepSeek Harness): versión exacta registrada, upgrade y rollback diseñados, sin seguir `latest`.
9. **Separación ephemeral vs durable** en todo conocimiento: session history ≠ decisión ≠ skill ≠ documentación humana.

## Planes de la plataforma (target)

| Plano | Responsabilidad | Herramienta propuesta | Estado |
|---|---|---|---|
| Control | Constitución, políticas, gates, decisiones, handoffs, skills | **Agents OS** (vault Obsidian) | Existe; ortogonal |
| Orchestration/Runtime | Model routing, tools, subagentes, personas, permissions, session logs | **DeepSeek Harness (`dsh`) con pin** + CLIs nativos (Codex/Claude Code) | Candidato; F5 |
| Operator/Session | Multi-sesión, tmux, attach/detach, visibilidad, costos, worktrees | **Agent Hub** (bake-off: Agent Deck → Claude Squad → dmux) | Por decidir; F6 |
| Provider | Acceso a modelos API-key y por suscripción | DeepSeek API, GLM/Z.AI, MiniMax, OpenRouter (API keys); Claude/Codex (login nativo) | F7 |
| Capability | Interfaz común de herramientas hacia infraestructura | **MCP** como denominador común + adapters por runtime | Contrato; gradual |
| Knowledge | Conocimiento durable auditable | Vault/Obsidian vía escritores controlados (mecanismos Agents OS) | Existente; POC F9 |
| Execution | CLI, tmux, git worktrees, procesos | Host-native en la VM + systemd selectivo + containers puntuales | F3-F4 |
| Durable Workflow | Retries/timers/recovery de larga duración | **Temporal existente** (hades vm158) | Fuera de alcance fase 1 |

### Control Plane — Agents OS

Agents OS sigue siendo el dueño de la gobernanza y vive en el vault, independiente del runtime que ejecute agentes. La plataforma debe permitir migrar gradualmente políticas desde prompt rules hacia runtime-enforced policies (allowed-files enforcement, dirty worktree protection, required-test evidence, PASS/BLOCKED gates, audit events), pero eso es evolución futura: en fase 1 solo se diseña para que sea posible (hooks/policies del Harness como punto futuro de enforcement, sin acoplar hoy).

### Orchestration/Runtime Plane — DeepSeek Harness

Hecho verificado (repositorio oficial, 2026-08-23): `deepseek-ai/deepseek-harness` (`dsh`) es un harness oficial Web-UI-first sobre runtime de plugins Cordis, MIT, creado 2026-08-13, solo releases RC (latest `dsh-v0.1.1-rc.2`, 2026-08-21) con warning explícito de breaking changes. Soporta profiles (`web`, `headless`, `tui`), providers custom OpenAI-compatible con flags de compatibilidad (ruta de diseño para GLM/Z.AI, MiniMax, OpenRouter — soportado por diseño, no certificado por marca), subagentes con providers coexistentes incluyendo **Codex y Claude Code como subagentes**, permission presets (sandbox + approval policy), credenciales write-only en `$DSH_HOME/.credentials.yaml`.

Posición: **adoptar como candidato principal del plano de orchestration**, con reglas duras:

- Pin de versión exacto por RC (ej. `dsh-v0.1.1-rc.2`) registrado en el proyecto; `$DSH_HOME` aislado y backupeable; upgrade = instalar nueva versión en paralelo + smoke test + swap; rollback = volver al pin anterior.
- NO acoplar Agents OS a APIs internas del Harness mientras esté en developer preview; la frontera de integración inicial son profiles, plugins y permisos declarativos.
- NO usar el Harness para gobernanza: es runtime, no control plane.

### Operator/Session Plane — Agent Hub bake-off

Referencia funcional (sin asumir implementación interna MELI): múltiples agentes, múltiples proveedores, sesiones concurrentes en tmux, visibilidad de estado, attach/detach, tareas en background, worktrees separados. Resultado del bake-off documental (hechos verificados 2026-08-23; el bake-off físico real ocurre en F6):

| Criterio | Agent Deck | Claude Squad | dmux | jfikrat/squad | mco-org/squad |
|---|---|---|---|---|---|
| Qué es | TUI Go + web view opcional | TUI Go | TUI Node dentro de tmux | MCP server (Bun) | CLI Rust middleware de mensajes |
| Madurez | Media-alta (v1.15.0 2026-08-23, cadencia muy rápida, bus-factor único maintainer) | Alta (8.4k stars, v1.0.20 2026-08-20, activo) | Media-alta (1.75k stars, v5.11.1 2026-08-16, transferido a standardagents) | Baja (3 stars, sin releases, stale) | Media (634 stars, silencioso desde 2026-05) |
| Worktrees | Sí | Sí (core design) | Sí (pane=worktree=branch) | No | Opcional (script helper) |
| Visibilidad sesiones | Mejor del set (lista running/waiting/done, search, groups, fork) | Buena (attach/detach, diff preview) | Parcial (panes, sin dashboard) | Buena introspección semántica | Ninguna (no es session manager) |
| Cost tracking | Sí (Cost Dashboard) | No | No | No | No |
| Multi-provider | Claude/Gemini/OpenCode/Codex/Pi + más | Claude/Codex/Gemini/Aider/OpenCode/Amp | El más amplio (11+ CLIs) | Codex+Claude presets | Claude/Gemini/Codex/OpenCode |

Clasificación razonada:

- **Agent Deck — probar primero**: único con dashboard de costos + mejor visibilidad + groups + managers de MCP/Skills; riesgo: bus-factor y churn por velocidad; mitigable con pin de versión.
- **Claude Squad — segundo**: el más maduro y simple; buena base si Agent Deck resulta frágil.
- **dmux — tercero**: mejor cobertura de CLIs y flujo pane=worktree=branch; alternativa válida si ese modelo calza con el workflow.
- **jfikrat/squad — NO adoptar; referencia de patrón**: valida el patrón MCP parent→workers en tmux con introspección de estado; útil como inspiración para el POC de Agents OS en F8.
- **mco-org/squad — descartado** para este rol: middleware de mensajes sin visibilidad de sesiones; categoría distinta.
- Si ninguno cubre el gap real tras F6, construir solo la capa delgada faltante (decisión post-bake-off, no antes).

### Provider Plane

Distinguir autenticación por tipo (verificado en docs upstream donde aplica):

- **API key**: DeepSeek, GLM/Z.AI, MiniMax, OpenRouter → via providers custom OpenAI-compatible del Harness o env vars de cada CLI. Una suscripción mensual NO implica acceso API; verificar caso por caso.
- **Login product-native / OAuth**: Claude (Max), Codex (ChatGPT) → auth nativo de cada producto, no API keys.
- Ambient credentials (gh auth, ssh agent) donde corresponda.
- Mecanismo de secretos: definido en § Secretos; jamás en el vault.

### Capability Plane — MCP

Si una capacidad puede exponerse vía MCP, se define una sola vez como **capability contract** y cada runtime consume su **runtime adapter** (config MCP nativa, plugin del Harness, wrapper controlado). Evita integraciones N-veces para Cursor/Codex/Claude/Harness/ZCode. Servicios MCP ya existen en Aranea (LXC mcps en hades) — evaluar consolidación futura, no mover nada en fase 1.

### Knowledge Plane

El vault es knowledge plane, no filesystem arbitrario: los agentes escriben conocimiento durable solo vía mecanismos Agents OS (skills, proyectos, journal, decisions); lo efímero vive fuera (session logs del runtime, `/tmp`, workspaces). Clasificación: ephemeral < session history < evidence < project state < decisions < skills/runbooks < documentación humana. Auditabilidad: change_logs y bitácoras. POC de integración controlada en F9.

### Execution Plane — host-native vs containers

| Componente | Modo | Justificación |
|---|---|---|
| git, gh, tmux, Node, Go, CLIs de agentes | Host-native (usuario no privilegiado) | PTYs, SSH, credentials y shells locales funcionan mejor sin capas |
| Git worktrees | Host-native bajo convención de directorios | Primitive de ejecución paralela; ver § Worktrees |
| dsh Web UI / hub web views | systemd user units | Lifecycle limpio, restart, logs journald |
| MCP servers terceros con deps pesadas | Container (caso a caso) | Aislamiento de dependencias; solo si aporta real |
| Nada expuesto a Internet | — | Traefik lan-only + wildcard interno |

### Durable Workflow Plane

Temporal (existente, hades) NO se reemplaza ni duplica: orchestration de agentes (LLM/delegación/coding/review) es cosa del plano de runtime; workflows durables de horas/días con retries/timers/recovery siguen siendo Temporal. Puntos de integración futura (agente dispara actividad Temporal, o workflow Temporal invoca headless runs) se investigan después de F7; NO construirlos en fase 1.

## Diseño VM (F2 — draft para gate de owner)

- **Placement**: nodo **hera**. Evidencia: 96 GiB RAM available, local-lvm ~258 GB libres, subutilización documentada, y descongestiona la concentración de hades (alerta conocida). Alternativas descartadas: hades (74% RAM, concentración), kronos (reservado a Ceph + PBS del proyecto Backup/DR), zeus (sqx-ulab-zeus-0 activo).
- **Sizing baseline**: 8 vCPU / 32 GB RAM / 200 GB SSD sobre `local-lvm` (thin). Justificación: workload de orchestration/CLI es network-bound, no memoria-masiva; 32 GB soporta múltiples sesiones concurrentes + runtimes + caches; crecimiento trivial por LVM extend o NFS truenas si aparece necesidad real. Sin GPU (no hay inferencia local en fase 1).
- **OS**: Ubuntu Server 24.04 LTS recomendado (soporte LTS 2029, compatibilidad documentada de primera mano con Node.js 24/Go/tmux/gh/Claude Code/Codex/dsh, uso ya existente de Ubuntu en VMs del cluster). Debian estable es alternativa aceptable si el owner prefiere uniformidad; no elegir por costumbre: la diferencia práctica real es documentación/comunidad de las tools agénticas, que hoy favorece Ubuntu.
- **Nombre propuesto**: convención mitología griega + sufijo `-vm` (precedente hermes-vm). Propuesta: **talos-vm** (Talos, autómata guardián de la mitología griega). Alternativas: daedalus-vm, hephaestus-vm. Decisión D-01.
- **Red/DNS/TLS**: IP estática LAN 192.168.31.0/24; registro DNS en Pi-hole bajo `talos.lab.aranea`; exposición HTTP/S interna vía Traefik lan-only + cert step-ca; cero puertos publicados; acceso admin por SSH con key-only desde máquinas del owner.
- **Usuarios/privilegios**: usuario admin humano (sudo), usuario(s) dedicados no privilegiados para runtimes de agentes; sin NOPASSWD amplios; wrappers con privilegios por capacidad solo cuando una operación sensible lo exija (patrón existente: `agent-read` read-only).
- **Secretos**: archivos env con permisos 600 fuera del vault, propiedad del usuario correspondiente, provisionados por el owner; el vault solo guarda referencias seguras. Pendiente decidir si se adopta un store dedicado (open question).
- **Worktrees como primitive**: repos centrales bajo convención `~/workspaces/<repo>`; un worktree por tarea (`wt/<branch>` naming); un solo writer por worktree; ownership de creación/cleanup queda primero en la tool del hub elegida; integración con gates de Agents OS (dirty worktree protection, merge policy) en fases posteriores.
- **Observabilidad fase 1**: fuentes de verdad = registro de sesiones del hub elegido + bitácoras/journal de Agents OS; campos objetivo (provider, model, task, workspace, branch, started_at, status, costo cuando exista) salen de esas fuentes; sin Grafana nuevo hasta que haya razón concreta (gap de observabilidad unificada ya conocido en Aranea).
- **Backup/DR**: stateful must-backup = `$DSH_HOME` (profiles/settings/session state), config del hub, `~/.ssh`, env files de secretos, metadata de workspaces; reproducible = binarios/CLIs instalados (reinstalables por pin registrado) y caches. Integración formal con [[BACKUP-DR-OWNER-PROJECT]] cuando ejecute (tier assignment depende de ticket 018).

## Riesgos principales

1. **Inestabilidad del Harness** (RC con breaking changes garantizados) → pin estricto, `$DSH_HOME` aislado, rollback probado, cero acople de Agents OS.
2. **Bus-factor/churn del hub elegido** (Agent Deck maintainer único) → pin de versión + bake-off con alternativas maduras (Claude Squad) + salida barata porque los worktrees/sesiones son host-native.
3. **Concentración de dependencia en una VM** → todo lo stateful backupeable; nada crítico de trading/producción dependerá de esta VM en fase 1.
4. **Deriva de alcance**: instalar veinte tools "por si acaso" → anti-goal explícito; cada adopción pasa su fase/gate.
5. **Fugas de secretos** → reglas duras + auditoría; referencias solamente en el vault.
6. **Convivencia con hermes-vm**: rol solapado de "nodo agéntico" → definir en G0 si talos-vm complementa (plataforma de orchestration) mientras hermes-vm mantiene su rol actual.

## Decisiones propuestas

Resumen; texto completo y estado de gate en [[AGENT-PLATFORM-OWNER-PROJECT]]:

- **D-01** Nombre de la VM: `talos-vm` (propuesto; alternativas daedalus/hephaestus).
- **D-02** Placement: hera.
- **D-03** Sizing: 8 vCPU / 32 GB / 200 GB en local-lvm.
- **D-04** OS: Ubuntu Server 24.04 LTS.
- **D-05** Agent Hub: bake-off físico en orden Agent Deck → Claude Squad → dmux; mco-org/squad descartado; jfikrat/squad solo como referencia de patrón.
- **D-06** DeepSeek Harness: adoptar con pin exacto, `$DSH_HOME` aislado y política upgrade/rollback; sin acoplar Agents OS.
- **D-07** Secretos: env files 600 fuera del vault provisionados por owner; store dedicado pendiente de decisión.
- **D-08** Knowledge plane: escritura durable al vault solo vía mecanismos Agents OS.
- **D-09** Capabilities: contract único + adapters; MCP como denominador común cuando aplique.
- **D-10** Temporal existente permanece como durable workflow plane; sin duplicación.

## Open questions (bloquean gates, no el diseño)

1. ¿Existe realmente Tailscale/WireGuard en Aranea? El prompt de origen lo menciona; la documentación capturada no muestra evidencia (WireGuard "necesita refresh"). Verificar antes de F2-final.
2. ¿Dónde viven hoy las API keys del owner (DeepSeek/GLM/MiniMax/OpenRouter)? Define el mecanismo de secretos concreto (D-07).
3. Confirmar qué accesos son suscripción vs API key por proveedor (Claude Max, ChatGPT/Codex, GLM, MiniMax).
4. Relación exacta talos-vm ↔ hermes-vm: complementar o absorber cargas (decisión owner, G0).
5. Preferencia OS si existe historial fuerte a Debian en el cluster (D-04).

## Fuentes

- Vault: [[30-resources/aranea/00-index]], [[30-resources/aranea/01-topologia/red]], [[30-resources/aranea/02-servicios/ml-ia]], [[30-resources/aranea/01-topologia/nodo-hera]], [[BACKUP-DR-OWNER-PROJECT]], [[80-agents/skills/agents-os-bootstrap/SKILL.md|agents-os-bootstrap]], [[90-system/convenciones]].
- Investigación externa 2026-08-23 (repos/docs oficiales vía GitHub API + READMEs): smtg-ai/claude-squad, asheshgoplani/agent-deck, standardagents/dmux, jfikrat/squad, mco-org/squad, deepseek-ai/deepseek-harness (docs user/guide/providers, subsystems/subagent, permission-presets). Detalle hecho-verificado vs inferencia en bitácora del proyecto owner.
