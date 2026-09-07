---
type: action
status: done
created: 2026-06-30T18:34:00Z
owner: ariadna
ticket: 2026-06-30-012
priority: low
---

# Dashboard stale-note cleanup

Verificación final 2026-06-30 18:34 UTC:

- ✅ Dashboard bind LAN `192.168.31.122:9119` responde 302→/login
- ✅ Tunnel reverso contra `agent_traefik_tunnel@192.168.31.11` vivo
- ✅ MEMORY.md nota stale eliminada (no había bug, era nota obsoleta)
- ⏳ Pendiente owner: ejecutar `bash /home/hermes/aranea-ops/pending-config-cleanup.sh`

Decisión arquitectónica confirmada: dashboard queda en bind LAN +
tunnel reverso (no se vuelve a 127.0.0.1). Script de cleanup preparado
en `/home/hermes/aranea-ops/pending-config-cleanup.sh` con backup
automático en `~/.hermes/config.yaml.before-cleanup-dashboard-comment-20260630-183446`.

Ref: [[2026-06-30-012-dashboard-bug-cleanup-stale-note]]