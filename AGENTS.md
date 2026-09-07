# AGENTS.md

Este repo contiene el segundo cerebro de Rodrigo. El vault vive en la carpeta
`main/`.

## Entrada obligatoria para todo agente

1. Lee `main/AGENTS.md` — es el AGENTS.md canónico del vault y define el
   arranque del sistema.
2. Ejecuta el bootstrap: `main/80-agents/skills/agents-os-bootstrap/SKILL.md`.
3. `VAULT_ROOT` = `main/` (la carpeta que contiene
   `80-agents/agents-os/agents-os.md`). Resuelve todas las rutas del vault
   desde ahí.

## Reglas del repo

- La rama canónica es `master`. Nunca hacer force-push.
- No modificar `sync.sh` ni `.sync/`.
- Los cambios se sincronizan solos (cron cada 1 minuto); solo asegúrate de
  commitear y pushear tus cambios.
