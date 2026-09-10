# Prompt maestro de instalación de AGENTS OS

Reemplaza solamente `<RUTA_ABSOLUTA_DEL_VAULT>` por la ruta absoluta de esta carpeta y entrega el bloque completo a un agente con acceso local a ella.

El mismo prompt sirve para **Codex** y para **Claude Code**; el paso 8 configura cada superficie que elijas. Si vas a usar las dos, córrelo una vez y responde "ambas" cuando el agente pregunte.

## Cómo entregarlo

- **Codex** (`codex` en la terminal, o Codex Desktop): abre la carpeta del vault y pega el bloque como primer mensaje.
- **Claude Code** (`claude` en la terminal, la app de escritorio o la extensión de IDE): abre la carpeta del vault y pega el bloque como primer mensaje.
- **Cualquier otra superficie con acceso a archivos locales**: pégalo igual. El agente va a registrar lo que su superficie no puede hacer, en vez de fingir que lo hizo.

## El prompt

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
   - 80-agents/memory/public/user-preference/agent-profile.md
2. Lee completamente AGENTS.md, CLAUDE.md si existe, la guía operativa, la
   constitución, el perfil always-load, agents-os-install y el proyecto de
   instalación. Trátalos como fuentes canónicas; no improvises otro flujo.
3. Usa el proyecto Instalación de AGENTS OS como plan y registro de avance.
   Empieza con todos sus checks en el estado real encontrado y marca solo lo que
   valides en esta máquina.
4. Explica en lenguaje simple: constitución, perfil, Sistema 1, Sistema 2,
   LLM Wiki, retrieval por capas, Graphify, memoria interna y skills.
5. Entrevista al usuario para completar identidad, rol, equipo, idioma, estilo,
   autonomía, aprobaciones, privacidad, persistencia, agentes usados, mecanismo
   de sync y qué reglas semilla mantiene, modifica o elimina. Actualiza el perfil
   existente sin borrar reglas no discutidas y mantenlo pending hasta el final.
   Si renombras el archivo del perfil, asegúrate de que siga siendo la única nota
   always-load bajo 80-agents/memory/public/user-preference/.
6. Pregunta una o más rutas absolutas donde viven sus proyectos. Ejecuta el
   descubridor read-only, presenta los repos encontrados y pide confirmar cuáles
   son aplicaciones activas. No asumas que todos los repos lo son.
7. Por cada aplicación activa, busca duplicados por título, alias, slug, remote,
   repo y path. Lee primero las instrucciones locales del repo; luego solo el
   README y manifests necesarios. Crea la nota canónica desde el template de
   aplicación, completa su contexto para agentes y actualiza índice y log sin
   copiar secretos ni paths personales al log compartible. Los repositorios
   completos nunca se copian dentro del vault: viven en un workspace externo y el
   vault guarda repo + path relativo.
8. Pregunta qué superficies usa y configura solo esas:
   - Codex: AGENTS.md en la raíz del vault, apuntando a las skills canónicas.
   - Claude Code: CLAUDE.md importando @AGENTS.md, apuntando a las mismas skills.
   - Otra superficie: usa el mecanismo de reglas que esa superficie soporte y
     regístralo; si no soporta ninguno, déjalo como pendiente explícito en vez de
     inventar un adapter.
   Usa el script configure-agent-surfaces.py de agents-os-install. El bloque
   administrado debe resolver VAULT_ROOT como la carpeta que contiene
   80-agents/agents-os/agents-os.md y ordenar invocar agents-os-bootstrap una vez
   al iniciar una sesión nueva, no en cada mensaje. La única ubicación física
   válida de una skill es VAULT_PATH/80-agents/skills/: no copies, symlinks ni
   adapters en carpetas de Codex, Claude u otro cliente.
9. Pregunta si esta regla aplica solo dentro del vault o globalmente a todos los
   proyectos del usuario. Para alcance global, pide aprobación antes de editar
   la configuración global del cliente. Mantén una sola fuente física por skill
   dentro del vault.
10. Reinicia o abre un proceso realmente fresco —una sesión abierta puede
    conservar un catálogo de discovery antiguo— y verifica que cada superficie
    elegida carga las reglas y que, al pedir por nombre agents-os-bootstrap,
    agents-os-install, agents-os-doctor o agents-os-hygiene-cycle, encuentra y
    lee el SKILL.md correspondiente bajo 80-agents/skills/. Registra por separado
    si el discovery nativo por `$skill` o slash-command funciona sin registro
    adicional; déjalo pendiente si no está validado y no lo resuelvas duplicando
    skills.
11. Instala Graphify desde un wheel o checkout local a la máquina siguiendo
    agents-os-graphify-install, configura AGENTS_OS_VAULT con VAULT_PATH, instala
    el wrapper canónico desde
    80-agents/skills/agents-os-graphify-install/scripts/, ejecuta
    help/cache-path/status y valida explain sobre una aplicación activa. El índice
    nunca se guarda en el vault; Markdown sigue siendo la fuente de verdad. Si la
    superficie no puede escribir la caché, regístralo como limitación de
    superficie y sigue: el vault funciona sin Graphify, con búsqueda dirigida.
12. Define con el usuario una cadencia de higiene: semanal para uso activo,
    mensual para uso liviano u otra frecuencia explícita. Configura una
    automatización recurrente si la superficie lo permite y el usuario aprueba;
    si no, deja el prompt exacto y una tarea pendiente. Cada corrida debe invocar
    agents-os-hygiene-cycle para regularizar notas, procesar feedbacks con
    Kaizen, promover valor reusable, registrar changelog compartible cuando
    cambie el sistema y reindexar Graphify.
13. Corre los gates y deja su salida en el reporte final:
    - python3 80-agents/skills/agents-os-doctor/scripts/doctor.py
    - python3 80-agents/skills/_shared/scripts/validate_schema_contract.py
    - python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --gate
    doctor debe salir con HIGH=0 y el contrato con errors=0. Si el lint reporta
    findings nuevos, corrígelos; el baseline solo congela deuda preexistente.
14. Ejecuta bootstrap con un agente o contexto fresco y recupera una aplicación
    activa sin que el usuario tenga que reexplicarla. Abre la fuente Markdown
    para verificar los hechos recuperados.
15. Solo cuando perfil, workspace, aplicaciones, superficies elegidas, Graphify,
    higiene, gates y bootstrap hayan pasado, cambia installation_status a
    complete y marca los checks correspondientes.
16. Entrega un reporte final con: perfil, roots, aplicaciones, recursos tocados,
    superficies configuradas, skills, Graphify, higiene y cadencia, salida de los
    gates, checks aprobados y pendientes. Mantén la sesión abierta para revisión.

Reglas de honestidad, no negociables:
- Si un gate no se pudo ejecutar en esta superficie, dilo. No afirmes que corrió.
- Si un check no se validó en esta máquina, queda pendiente. La existencia del
  scaffolding no es evidencia.
- Si encuentras una contradicción, privilegia la constitución y las fuentes
  canónicas del vault, registra el conflicto y evita crear una segunda regla
  paralela.
```

## Después de instalar

- Trabaja normal. El agente carga bootstrap una vez por sesión nueva y recupera solo lo que la pregunta necesita.
- Pide `cierra sesión` cuando quieras que persista lo aprendido. El cierre completo nunca ocurre por inercia.
- Pide `corre el ciclo de higiene` según la cadencia que hayas elegido, o deja que la automatización lo haga.
- Pide `agents-os-doctor` cuando algo se sienta raro.
