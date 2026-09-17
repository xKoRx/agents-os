---
type: session-summary
schema_version: 1
created: "2026-09-17"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[2026-09-16-R0-reconciliacion]]"
  - "[[agent-project-01-critical-config-backup]]"
  - "[[BACKUP-DR-CONTRACT]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-summary
  - scope/session
---

# 2026-09-17 — Backup/DR R1 ejecutado

- **Objetivo:** primer backup real y restaurable de bootstrap/config crítico hacia staging Hermes VM 118 (fase R1 del mandato owner 2026-09-16/17), sin repetir R0 y sin tocar producción.
- **Resultado: PASS WITH DEBT.** 3 unidades BACKUP_VERIFIED + RESTORE_VERIFIED con restore drills PASS a scratch: traefik-config (LXC 115 vía `agent_traefik`, configs estática+dinámica, drill sha256 8/8 vs fuente viva), second-brain (vault 3.438 archivos, restore idéntico byte a byte), hermes-state (`~/.hermes` operacional sin regenerables + `~/aranea` + unit túnel, 600). Staging `~/aranea/backup-staging/` (700) + wrapper `~/aranea/bin/r1-backup.sh` probado ×2 (idempotencia); manifests con sha256 por artefacto.
- **Gated (deuda owner acotada):** `/etc/pve` (requiere subcommand `config` en `agent-read` de los 5 nodos), etcd snapshot (etcdctl ausente + :2379 filtrado desde LAN), pi-hole (api_token FTL v6 o root; 149 inalcanzable desde hermes). Traefik parcial: `secrets/ ssl/` root-only fuera del alcance.
- **F-09:** `pool2/pool0_backup` EXISTS (live truenas + captura R0), intacto.
- **Quirks nuevos:** tar de paths amplios silenciosamente descarta entradas root-only (usar set explícito); auto-inclusión del staging en su propio tar; `profiles/ariadna/profile.yaml` no existe; .31 es OPNsense, no pi-hole (verificar identidad de host antes de afirmar).
- **Evidencia durable:** change log `80-agents/journal/logs/2026-09-17-backup-dr-r1-bootstrap-config.md` · bitácoras de [[BACKUP-DR-OWNER-PROJECT]] y [[agent-project-01-critical-config-backup]] · manifests por run en staging.
- **Próximo paso:** R2 (adoptar PBS VM 180) listo para manager review — requiere owner bundle (acceso VM 180, ventana 019, Secret Zero 020) + consolidar gates de deuda R1 y decidir frecuencia/retención del wrapper R1. R2 NO iniciado.
