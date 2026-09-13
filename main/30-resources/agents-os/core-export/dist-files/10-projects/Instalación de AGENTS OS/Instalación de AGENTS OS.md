---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Personal]]"
parent:
sprint:
start:
due:
progress: 0
repo:
jira:
prs:
aliases:
  - instalación de agents os
  - onboarding de AGENTS OS
  - setup de AGENTS OS
tags:
  - kind/project
  - project/agents-os
  - action/install
created: 2026-09-09
updated: 2026-09-09
---
indexable: false
index_priority: never

# Instalación de AGENTS OS

> [!info]+ Tu instalación local
> No necesitas conocer AGENTS OS antes de empezar. Pega el bloque de `INSTALL-PROMPT.md` en tu agente, o pídele directamente: `usa agents-os-install para instalar AGENTS OS en esta máquina`. La skill hace las preguntas, explica cada etapa y actualiza este proyecto.

## 🎯 Objetivo

Dejar esta copia de AGENTS OS configurada para la persona que usa la máquina: perfil, reglas de trabajo, workspace, aplicaciones, superficies de agente, skills, Graphify, higiene periódica y retrieval.

Al terminar, un agente nuevo debe poder entender quién es el usuario, dónde están sus repositorios, con qué aplicaciones trabaja y qué contexto cargar, sin que la persona lo explique de nuevo.

## 📊 Estado actual

- Instalación no iniciada.
- `80-agents/memory/public/user-preference/agent-profile.md` trae la semilla estándar de reglas y declara `installation_status: pending`; todavía no representa a nadie.
- `30-resources/applications/` está vacío a propósito: el catálogo se construye desde los repositorios reales de esta máquina.
- Ningún check se considera aprobado hasta que el agente lo valide localmente. Que el scaffolding exista no prueba nada.

## Qué hará el agente instalador

1. Explicar en lenguaje simple qué son la constitución, el perfil, Sistema 1, Sistema 2, LLM Wiki, retrieval por capas, memoria interna y skills.
2. Entrevistar al usuario y modificar el perfil existente sin borrar reglas que no se discutieron.
3. Pedir una o más rutas absolutas donde viven los proyectos o repositorios locales.
4. Descubrir los repositorios dentro de esas rutas y pedir al usuario que confirme con cuáles trabaja activamente. No todos los repos encontrados son aplicaciones activas.
5. Crear la nota canónica de cada aplicación activa desde `70-templates/application.md`, buscando antes duplicados por título, alias, slug, remote, repo y path.
6. Actualizar `30-resources/applications/00-index.md` y su `log.md` sin copiar secretos ni paths personales al log compartible.
7. Configurar las reglas duras de las superficies elegidas y validar que las skills se lean desde `80-agents/skills/`.
8. Definir la cadencia de higiene y, cuando la superficie lo permita y el usuario apruebe, automatizarla.
9. Instalar Graphify por máquina, reindexar y probar retrieval con una aplicación real del usuario.
10. Cambiar `installation_status` a `complete` sólo cuando cada criterio obligatorio esté comprobado.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Ver [[convenciones]]. %%
> - [ ] Leer guía, constitución y perfil semilla #owner/agent #type/admin #project/agents-os
> - [ ] Entrevistar al usuario y confirmar reglas del perfil #owner/agent #type/admin #project/agents-os
> - [ ] Registrar raíces de workspace y aplicaciones activas #owner/agent #type/research #project/agents-os
> - [ ] Descubrir y reconciliar repositorios con la Resource Wiki #owner/agent #type/research #project/agents-os
> - [ ] Crear los recursos canónicos de las aplicaciones activas #owner/agent #type/admin #project/agents-os
> - [ ] Configurar y validar las reglas duras de cada superficie elegida #owner/agent #type/admin #project/agents-os
> - [ ] Validar carga de skills canónicas en cada superficie #owner/agent #type/admin #project/agents-os
> - [ ] Definir cadencia y automatización de higiene #owner/agent #type/admin #project/agents-os
> - [ ] Instalar y validar Graphify #owner/agent #type/dev #project/agents-os
> - [ ] Ejecutar bootstrap y retrieval con una aplicación real #owner/agent #type/research #project/agents-os
> - [ ] Revisar el reporte de instalación #owner/me #type/supervision #project/agents-os

## Criterios de aceptación

- [ ] El perfil identifica al usuario y no conserva placeholders sin decidir.
- [ ] Las reglas semilla fueron confirmadas, modificadas o eliminadas explícitamente.
- [ ] El perfil lista las raíces del workspace y las aplicaciones activas.
- [ ] Cada aplicación activa tiene una nota canónica con repo, path relativo, rol y stack.
- [ ] `30-resources/applications/00-index.md` incluye las aplicaciones activas y `log.md` registra la ingesta.
- [ ] Las instrucciones locales de cada repo fueron identificadas y respetadas.
- [ ] `AGENTS.md` es detectado por el agente en la superficie elegida.
- [ ] `CLAUDE.md` importa `@AGENTS.md` y Claude confirma su carga, si Claude es una de las superficies.
- [ ] No existen copias, symlinks ni adapters de AGENTS OS bajo `.agents/skills/`, `.claude/skills/` ni carpetas globales del cliente.
- [ ] Cada superficie elegida encuentra y lee las skills directamente desde `80-agents/skills/` ante una invocación por nombre.
- [ ] `agents-os-bootstrap`, `agents-os-install`, `agents-os-doctor` y `agents-os-hygiene-cycle` son ejecutables desde su fuente canónica.
- [ ] El discovery nativo por `$skill` o slash-command fue validado, o quedó como pendiente explícito con evidencia y sin duplicar skills.
- [ ] La cadencia de higiene fue elegida y quedó automatizada, o con pendiente explícito si la superficie no ofrece scheduler.
- [ ] El mecanismo de sync del vault fue elegido explícitamente.
- [ ] `graphify-obsidian --help`, `cache-path` y `status` responden, y el índice **no** quedó dentro del vault.
- [ ] `graphify-obsidian explain` recupera al menos una aplicación activa por su nombre canónico.
- [ ] `python3 80-agents/skills/agents-os-doctor/scripts/doctor.py` sale con `HIGH=0`.
- [ ] `python3 80-agents/skills/_shared/scripts/validate_schema_contract.py` sale con `errors=0`.
- [ ] Un agente fresco ejecuta bootstrap sin que el usuario reexplique su entorno.
- [ ] El perfil declara `installation_status: complete`.

## Preguntas iniciales

- ¿Cómo quieres que te llame y en qué idioma debo responder?
- ¿Cuál es tu rol, equipo, especialidad y stack habitual?
- ¿Qué reglas del perfil semilla quieres mantener, modificar o eliminar?
- ¿Qué acciones requieren tu aprobación y qué puede ejecutar el agente solo?
- ¿En qué ruta o rutas están tus proyectos locales?
- ¿Con cuáles de los repositorios encontrados trabajas activamente?
- ¿Qué puede persistirse y qué nunca debe guardarse?
- ¿Qué agentes, IDEs y mecanismos de sync utilizas?
- ¿Las reglas de AGENTS OS aplican sólo a este vault o globalmente a todos tus proyectos?
- ¿Prefieres higiene semanal, mensual u otra cadencia?
- ¿Autorizas crear la automatización recurrente en la superficie disponible?

## 🧭 Reglas de la instalación

- No inventar identidad, rutas, aplicaciones ni reglas faltantes.
- No considerar todos los repos descubiertos como activos sin confirmación.
- No crear una aplicación duplicada: buscar título, alias, repo, remote y path antes.
- No leer ni persistir secretos durante el descubrimiento del workspace.
- No marcar checks por existencia del scaffolding; validar esta máquina.
- No escribir configuración global del cliente sin aprobación.
- No declarar compatibilidad sin probar carga y ejecución de la skill canónica.
- No resolver el discovery creando copias, symlinks o adapters por superficie.
- No agregar repositorios completos dentro del vault: viven en un workspace externo y el vault sólo guarda la nota de referencia.
- No cerrar la sesión como parte de la instalación salvo pedido explícito.

## 📆 Bitácora

- **Pendiente** — la instalación no ha comenzado en esta máquina.

## 🔗 Fuentes

- `80-agents/agents-os/agents-os.md` — mapa del sistema.
- `80-agents/agents-os/agent-constitution.md` — invariantes.
- `80-agents/skills/agents-os-install/SKILL.md` — procedimiento de instalación.
- `80-agents/skills/agents-os-graphify-install/SKILL.md` — instalación de Graphify por máquina.
- `80-agents/memory/public/user-preference/agent-profile.md` — perfil a completar.
- `80-agents/memory/public/runbook/graphify-obsidian-install.md` — runbook de instalación del índice.
- `70-templates/application.md` — template de aplicación.
- `INSTALL-PROMPT.md` — prompt maestro para Codex y Claude.
