# AGENTS.md

<INSTRUCTIONS>
<!-- AGENTS_OS_MANAGED_START -->
Resuelve `VAULT_ROOT`: la carpeta que contiene
`80-agents/agents-os/agents-os.md`. Si ese marker no existe, estas reglas no
aplican.

Invoca `80-agents/skills/agents-os-bootstrap/SKILL.md` una sola vez al iniciar una nueva sesión y ejecuta su procedimiento. No lo releas por cada mensaje: en turnos warm reutiliza la base y ante cambio de entidad ejecuta sólo el routing y delta correspondientes. Bootstrap es la única máquina de startup y decide qué contexto y skills cargar; no lo reemplaces con una lectura amplia del vault.
<!-- AGENTS_OS_MANAGED_END -->
</INSTRUCTIONS>
