---
type: skill
schema_version: 1
name: agents-os-install
scope: global
created: 2026-07-14
updated: 2026-08-10
description: Install, explain, personalize, and validate a local AGENTS OS vault. Use for first-time onboarding, setting up another machine, completing a pending user profile, discovering a person's workspace and active repositories, reconciling application resources, routing agents to canonical AGENTS OS skills, installing Graphify, or repairing an incomplete installation.
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/install
  - action/onboarding
  - tech/agents-os
  - scope/global
---

# agents-os-install

## Purpose

Dejar AGENTS OS configurado para una persona y su workspace sin asumir que el
usuario o el agente conocen previamente el sistema.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

1. `../../agents-os/agents-os.md`
2. `../../agents-os/agent-constitution.md`
3. El perfil always-load resuelto bajo `../../memory/public/user-preference/`
4. Proyecto de instalación resuelto: usar
   `../../../10-projects/Personal/AGENTS OS/AGENTS OS.md` en este vault. En una
   distribución nueva, usar un proyecto dedicado de instalación solo si
   existe; no asumir una ruta inexistente.
5. `../../../70-templates/application.md`
6. `../../../30-resources/applications/00-index.md`
7. `../agents-os-resource-wiki/SKILL.md`
8. `../agents-os-entity-lifecycle/SKILL.md`
9. `../agents-os-graphify-install/SKILL.md`
10. `../agents-os-hygiene-cycle/SKILL.md`

## Procedure

1. Detectar la raíz por `80-agents/agents-os/agents-os.md`, resolver el
   proyecto de seguimiento según Minimal Read y explicar en cinco líneas o
   menos: constitución, perfil, Sistema 1, Sistema 2 y Graphify.
2. Auditar escritura en el vault, shell, sistema operativo, Python 3.10+, PATH
   y fuente local de instalación de Graphify; el vault no contiene wheels.
3. Resolver y abrir el perfil always-load:
   - preferir `user-profile.md` si existe;
   - si no, usar la única nota con `type: user_preference` y
     `load_policy: always`;
   - si hay varias candidatas, pedir al usuario elegir antes de editar;
   - si ninguna existe, materializar `type: user_preference` como
     `user-profile.md` con `materialize_schema_note.py` y mantenerlo `pending`;
   - si declara `installation_status: pending`, tratarlo como seed editable;
   - si declara `complete`, preguntar si se desea reparar o reconfigurar.
4. Entrevistar en bloques cortos y esperar respuesta:
   - identidad, rol, equipo, idioma, tono y nivel de detalle;
   - reglas existentes a mantener, modificar o eliminar;
   - autonomía, aprobaciones, checkpoints y validaciones;
   - privacidad, memoria, sesiones, sync, agentes e IDEs;
   - alcance de reglas (`project` o `global`) y superficies Codex/Claude;
   - cadencia de higiene y mecanismo de automatización;
   - una o más rutas raíz donde viven proyectos o repositorios locales.
5. Actualizar el mismo perfil resuelto con respuestas confirmadas. Mantener
   `installation_status: pending`; no inventar valores ni borrar reglas no
   discutidas.
6. Validar cada raíz de workspace y ejecutar descubrimiento read-only:

   ```bash
   python3 80-agents/skills/agents-os-install/scripts/discover-workspace-apps.py \
     --root <ruta> [--root <ruta>]
   ```

7. Presentar nombre, path, remote, stack e instrucciones detectadas. Si aparecen
   muchos repos, pedir al usuario que seleccione los activos; no ingerir todos
   por defecto.
8. Por cada repo activo, reconciliar `30-resources/applications/`:
   - buscar duplicados por título, aliases, slug, remote, repo y path;
   - leer instrucciones del repo (`AGENTS.md`, `CLAUDE.md` u otras) antes de
     inspeccionar contenido;
   - leer solo README y manifests suficientes para determinar rol y stack;
   - actualizar la nota existente o crear una desde
     `70-templates/application.md` mediante `agents-os-entity-lifecycle`;
   - completar al menos título canónico, aliases, área, lenguaje/stack, remote,
     path local, descripción e instrucciones relevantes;
   - actualizar `30-resources/applications/00-index.md` y append a `log.md` sin
     copiar secretos ni rutas personales al log;
   - agregar la aplicación como wikilink canónico en el perfil.
9. Registrar en el perfil las raíces de workspace y aplicaciones activas. Usar
   `ninguno` en campos opcionales decididos, no dejar placeholders ambiguos.
10. Crear una nota compacta de continuidad en `memory/internal/` y un
    `change_log` de instalación sin exponer valores personales del perfil.
11. Alinear Codex y Claude con reglas duras que apunten a las skills canónicas:

    ```bash
    python3 80-agents/skills/agents-os-install/scripts/configure-agent-surfaces.py \
      --vault . --surface both --scope project
    ```

    - Codex debe cargar `AGENTS.md`;
    - Claude Code debe cargar `CLAUDE.md` con `@AGENTS.md`;
    - usar `--scope global` solo si el usuario lo confirma y después de pedir
      aprobación para escribir fuera del vault;
    - en scope global, el instalador guarda la raíz en el pointer local
      `~/.config/agents-os/vault-root`; `AGENTS_OS_VAULT` puede sobrescribirlo
      por máquina. La regla compartida nunca contiene el valor absoluto;
    - `80-agents/skills/*/SKILL.md` es la única ubicación física de skills;
    - eliminar únicamente adapters antiguos generados por AGENTS OS;
    - no copiar, enlazar ni generar skills bajo `.agents/skills/`,
      `.claude/skills/` o carpetas globales de las superficies.
12. Ejecutar `agents-os-graphify-install` y definir `AGENTS_OS_VAULT` con la
    raíz detectada.
13. Definir la cadencia de `agents-os-hygiene-cycle` y registrarla en el perfil:
    - semanal para uso activo, mensual para uso liviano u otra explícita;
    - configurar una automatización si la superficie ofrece scheduler y el
      usuario autoriza;
    - si no existe scheduler, dejar una tarea pendiente con el prompt exacto;
    - la corrida debe regularizar notas, procesar feedbacks, escribir changelog
      `team` cuando cambie el sistema y reindexar Graphify.
14. Validar:
    - `graphify-obsidian --help`, `cache-path`, `status` y una query con auto-refresh;
    - `explain` para `AGENTS OS` y una aplicación activa;
    - reglas cargadas por Codex y Claude seleccionados;
    - reiniciar o abrir un proceso de agente realmente fresco después de
      configurar las reglas; el catálogo de una sesión ya abierta puede
      conservar rutas de discovery anteriores;
    - ese agente fresco invoca por nombre `agents-os-bootstrap`,
      `agents-os-install` y `agents-os-hygiene-cycle`, encuentra sus
      `SKILL.md` bajo `80-agents/skills/` y los lee desde ahí;
    - registrar por separado si la sintaxis nativa `$skill` o slash-command de
      cada superficie funciona sin registro adicional; ese discovery es una
      optimización pendiente, no autorización para duplicar skills;
    - bootstrap con constitución, perfil y retrieval de esa aplicación;
    - fuente Markdown abierta para confirmar los hechos recuperados.
15. Cambiar `installation_status` a `complete` solo si perfil, workspace,
    aplicaciones, superficies elegidas, skills, Graphify, higiene y bootstrap
    pasan. Marcar en el proyecto únicamente los checks realmente validados en
    esta máquina, sin resetear ni desmarcar el historial de un proyecto
    existente.
16. Entregar el reporte y dejar pendientes explícitos; no cerrar la sesión.

## Output

```text
Vault:
Perfil: pending | complete
Raíces de workspace:
Repos descubiertos:
Aplicaciones activas confirmadas:
Recursos creados/actualizados:
Índice de aplicaciones:
Superficie/skills:
Codex:
Claude:
Graphify:
Higiene/cadencia:
Bootstrap/retrieval:
Checks aprobados:
Pendientes:
```

## Hard Rules

- No copiar identidad, correo, rutas ni aplicaciones de otra persona.
- No asumir que una regla seed fue aceptada; confirmarla o dejarla pendiente.
- No marcar `complete` mientras queden campos obligatorios sin decidir.
- No considerar todo repo descubierto como aplicación activa.
- No crear una aplicación antes de buscar duplicados por repo, remote y alias.
- No leer `.env`, credenciales, llaveros, tokens ni archivos de secretos.
- No modificar configuración global de una superficie sin aprobación.
- No copiar, enlazar ni generar skills de AGENTS OS bajo carpetas de Codex,
  Claude u otra superficie.
- No declarar una superficie compatible solo porque carga reglas; validar que
  encuentre y ejecute el `SKILL.md` canónico ante una solicitud real.
- No instalar una automatización sin cadencia y aprobación explícitas.
- No modificar la constitución por una preferencia individual.
- No cerrar la sesión como parte del onboarding salvo pedido explícito.
