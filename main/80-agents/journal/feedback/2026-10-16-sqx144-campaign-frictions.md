---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-16"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Aranea]]"
related: []
aliases: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# Feedback — 2026-10-16 (campaña SQX 144)

- **Fricción (transporte MCP):** `aranea-ssh` expira la sesión del cliente ZCode y el re-initialize no ocurre en caliente; además el DNS `*.lab.aranea.cl` desde Daedalus es intermitente. Remedio aplicado: cliente HTTP directo contra la IP del appliance (192.168.31.219) con session-id persistido y helper pexpect (password + base64→bash) para kor. Sugerencia: endpoint IP directa en `config.json` o健康-check de sesión por llamada.
- **Fricción (SQX fail-open):** `sqcli` termina exit 0 con "Cannot start project. Project has unresolved resources." (y con StopConfiguration inválida se va a background). El código de salida NO refleja el fallo; el criterio de éxito del worker es por markers, pero en probes manuales esto confunde. Sugerencia: en probes/cierres, grep explícito de "Error while running"/"Cannot start" además del exit code.
- **Fricción (estado de instalaciones 144):** los CFX del owner referencian datasets del árbol raíz 142; el árbol 144 tiene su propio `user/data` (divergente desde la importación dukascopy del 13-oct). El skill de sync cubre el árbol raíz, no los árboles por versión. Sugerencia: extender `sqx-instrument-sync` con un modo "root→versión" o registrar los datasets canónicos por versión.
- **Aprendizaje (resolución de recursos SQX):** el `<Chart symbol>` del Setup es la referencia operativa de datos; un bloque `<Resources><Symbols>` con entradas no resolubles envenena el proyecto completo ("unresolved resources", exit 0). La adaptación segura de CFX entre instalaciones = swap de Chart symbols + remoción del bloque Resources (SQX resuelve por catálogo). Registrado como patrón en ADAPTATION-REPORT.json.
