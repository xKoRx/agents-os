# Prompt maestro de instalación de AGENTS OS

Reemplaza solamente `<RUTA_ABSOLUTA_DEL_VAULT>` y entrega el bloque completo a
un agente con acceso local a la carpeta.

```text
Instala y configura completamente AGENTS OS en este vault:

VAULT_PATH=<RUTA_ABSOLUTA_DEL_VAULT>

Actúa como responsable del onboarding de punta a punta. El usuario no conoce el
sistema y no habrá una sesión hands-on, así que debes explicar brevemente cada
decisión, hacer las preguntas necesarias en bloques cortos, ejecutar todo lo que
puedas y dejar pendientes explícitos solo cuando necesites una autorización o
una capacidad que no exista en esta superficie.

Autorización y límites:
- Puedes leer y modificar archivos dentro de VAULT_PATH y ejecutar validaciones
  locales necesarias para la instalación.
- Antes de escribir fuera de VAULT_PATH, instalar herramientas globales, editar
  configuración del usuario o crear automatizaciones, explica la acción y pide
  aprobación.
- No leas ni persistas secretos, tokens, llaveros, credenciales o archivos .env.
- No borres ni reemplaces contenido preexistente del usuario sin reconciliarlo.
- No cierres la sesión al terminar la instalación.

Procedimiento obligatorio:
1. Verifica que VAULT_PATH sea absoluto y que existan:
   - AGENTS.md
   - 80-agents/agents-os/agents-os.md
   - 80-agents/agents-os/agent-constitution.md
   - 80-agents/skills/agents-os-install/SKILL.md
   - 10-projects/Instalación de AGENTS OS/Instalación de AGENTS OS.md
2. Lee completamente AGENTS.md, CLAUDE.md si existe, la guía operativa, la
   constitución, el perfil always-load, agents-os-install y el proyecto de
   instalación. Trátalos como fuentes canónicas; no improvises otro flujo.
3. Usa el proyecto Instalación de AGENTS OS como plan y registro de avance.
   Empieza con todos sus checks en el estado real encontrado y marca solo lo que
   valides en esta máquina.
4. Explica en lenguaje simple: constitución, perfil, Sistema 1, Sistema 2,
   LLM Wiki, Context Router, Graphify, memoria interna y skills.
5. Entrevista al usuario para completar identidad, rol, equipo, idioma, estilo,
   autonomía, aprobaciones, privacidad, persistencia, agentes usados, mecanismo
   de sync y reglas seed que mantiene, modifica o elimina. Actualiza el perfil
   existente sin borrar reglas no discutidas y mantenlo pending hasta el final.
6. Pregunta una o más rutas absolutas donde viven sus proyectos. Ejecuta el
   descubridor read-only, presenta los repos encontrados y pide confirmar cuáles
   son aplicaciones activas. No asumas que todos los repos lo son.
7. Por cada aplicación activa, busca duplicados por título, alias, slug, remote,
   repo y path. Lee primero las instrucciones locales del repo; luego solo el
   README y manifests necesarios. Actualiza o crea la nota canónica desde el
   template de aplicación, completa su contexto para agentes y actualiza índice
   y log sin copiar secretos ni paths personales al log compartible.
8. Configura reglas duras para las superficies elegidas:
   - Codex: AGENTS.md apuntando a las skills canónicas del vault.
   - Claude Code: CLAUDE.md importando @AGENTS.md y apuntando a las mismas
     skills canónicas.
   Usa el script configure-agent-surfaces.py de agents-os-install. El bloque
   administrado debe usar la ruta absoluta de VAULT_PATH y ordenar, en cada
   turno, cargar 80-agents/agents-os/agents-os.md, la constitución, el perfil y
   bootstrap antes del trabajo sustantivo. La única ubicación física válida es
   VAULT_PATH/80-agents/skills/: no copies, symlinks ni adapters en carpetas de
   Codex o Claude.
9. Pregunta si esta regla aplica solo dentro del vault o globalmente a todos los
   proyectos del usuario. Para alcance global, pide aprobación antes de editar
   ~/.codex/AGENTS.md o ~/.claude/CLAUDE.md. Mantén una sola fuente física por
   skill dentro del vault.
10. Reinicia o abre un proceso realmente fresco —una sesión abierta puede
    conservar un catálogo de discovery antiguo— y verifica que Codex y Claude
    cargan las reglas y que,
    al pedir por nombre agents-os-bootstrap, agents-os-install o
    agents-os-hygiene-cycle, encuentran y leen el SKILL.md correspondiente bajo
    80-agents/skills/. Registra por separado si el discovery nativo por
    `$skill` o slash-command funciona sin registro adicional; déjalo pendiente
    si no está validado y no lo resuelvas duplicando skills.
11. Instala Graphify desde un wheel o checkout local a la máquina, configura
    AGENTS_OS_VAULT con VAULT_PATH, instala el wrapper canónico desde
    80-agents/skills/agents-os-graphify-install/scripts/, ejecuta help/cache-path/status
    y valida explain sobre AGENTS OS y una aplicación activa. El índice nunca se
    guarda en el vault; Markdown sigue siendo la fuente de verdad.
12. Define con el usuario una cadencia de higiene: semanal para uso activo,
    mensual para uso liviano u otra frecuencia explícita. Configura una
    automatización recurrente si la superficie lo permite y el usuario aprueba;
    si no, deja el prompt exacto y una tarea pendiente. Cada corrida debe invocar
    agents-os-hygiene-cycle para regularizar notas, procesar feedbacks con
    Kaizen, promover valor reusable, registrar changelog compartible cuando
    cambie el sistema y reindexar Graphify.
13. Ejecuta bootstrap con un agente/contexto fresco y recupera una aplicación
    activa sin que el usuario tenga que reexplicarla. Abre la fuente Markdown
    para verificar los hechos recuperados.
14. Solo cuando perfil, workspace, aplicaciones, Codex/Claude elegidos,
    Graphify, higiene y bootstrap hayan pasado, cambia installation_status a
    complete y marca los checks correspondientes.
15. Entrega un reporte final con: perfil, roots, aplicaciones, recursos tocados,
    Codex, Claude, skills, Graphify, higiene/cadencia, checks aprobados y
    pendientes. Mantén la sesión abierta para revisión.

Si encuentras una contradicción, privilegia la constitución y las fuentes
canónicas del vault, registra el conflicto y evita crear una segunda regla
paralela.
```
