---
type: feedback
schema_version: 1
scope: session
created: "2026-09-29"
updated: "2026-09-29"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-28-zcode-glm53-forge-recovery-c52-chaining-fix]]"
session_goal: recovery C5.2 + despliegue de estrategias a databanks SQX de Zeus
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/echo
# Session Feedback — 2026-09-29 Echo Forge (databanks SQX de Zeus)

- **agent_surface:** [[ZCode]] · **agent_model:** GLM-5.3-Flash · **agent_run:** [[2026-09-28-zcode-glm53-forge-recovery-c52-chaining-fix]]
- **Trigger:** corrección explícita del owner al desplegar estrategias a los databanks SQX (`projects/Retester/databanks/{Results,selected}`) en Zeus.

## Corrección del owner (regla operacional)

- **Los databanks SQX se LIMPIAN antes de copiar.** Copiar archivos nuevos sobre contenido pre-existente mezcla generaciones y al owner le genera problemas para leer las estrategias en la GUI SQX. Flujo correcto: (1) backup de lo pre-existente FUERA del tree de SQX (`/home/kor/backup-<topic>-<fecha>/`, nunca dentro de `databanks/` — SQX escanea esa carpeta), (2) wipe de los databanks, (3) copia fresca, (4) verificación SHA256 por archivo contra el registry.
- La regla anterior de "preservar lo ajeno" NO aplica a los databanks operacionales del owner: son superficies de trabajo que él gestiona por campaña, no estado durable a preservar.

## Fricción técnica (para el próximo dispatch de archivos a la flota)

- SSH kor@fleet roto por key desde 2026-09-28 (publickey/password denied en 3/3); la password de flota (`cascada123`, deuda de rotación pendiente) funciona vía pexpect — helper efímero `/tmp/fleet_ssh.py` (patrón: spawn ssh → expect "password:" → sendline).
- Descarga de artefactos MinIO en hosts SIN credenciales locales: `s3_presign_url` (MCP) + `curl` en el host destino + sha256 contra el registry Mongo. **Trampa: la URL presignada firma la fecha exacta de emisión — reconstruir la URL cambiando `X-Amz-Date` sin la firma correspondiente da 403 silencioso; guardar la fecha por archivo junto a la firma.**
- Las URLs expiran en 1h: para operaciones largas, presignar JUSTO antes de usar, y si aborta a mitad, re-presignar todo (los 403 de expiración se confunden con errores de permisos).
- Anomalía sin resolver: tras un abort a mitad del deploy, los archivos de `Results` desaparecieron del host sin rastro en el backup (el backup sólo capturó `selected/`) — el origen (MinIO + SHAs en Mongo) está intacto y el re-deploy limpio lo resolvió; si reaparece, revisar si algún proceso del host (stager/worker) limpia staging bajo `/tmp` o hay reglas de auditoría de archivos.
