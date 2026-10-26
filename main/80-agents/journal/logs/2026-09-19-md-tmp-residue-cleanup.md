---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-10-24"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-hygiene-cycle]]"
aliases:
  - "md.tmp residue cleanup"
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
tags:
  - kind/change-log
  - action/hygiene
  - project/agentsos
---

# Limpieza de residuos `*.md.tmp.*`

## Qué

Eliminación de 36 archivos residuales `*.md.tmp.<pid>.<hash>` en el vault (escrituras atómicas interrumpidas del writer de notas; auditoría M4 previa reportaba cuatro, la inspección física encontró 36 en `30-resources/`, `10-projects/Echo|Loom|Polymarket Engine/` y `80-agents/journal/`).

## Prueba por archivo (cero eliminaciones a ciegas)

- Writer PIDs (4627, 464097, 153247, 740422, 488609): todos muertos — sin writer activo.
- Ningún archivo tmp trackeado por git (invisible para el repo; la limpieza no altera el historial).
- 29 eliminados por **supersesión temporal**: mtime del tmp anterior al mtime del archivo real ⇒ el writer completó una escritura posterior exitosa que lo reemplazó.
- 7 eliminados por **igualdad de contenido byte a byte** con su archivo real vigente ⇒ cero trabajo único.
- 0 inciertos: ningún tmp divergió de su real sin estar superseded por tiempo.
- Muestra inspeccionada en contenido (`Polymarket Engine — MVP.md.tmp.153247.*` vs real): intermedio antiguo (`progress: 0`, texto M2 superseded) contra real evolucionado (`progress: 25`) — patrón consistente con residuo.
- Ninguna nota del vault referencia rutas `.md.tmp.` (patrón interno del writer, sin inbound links).

## Efecto

- Vault: 36 archivos menos, sin cambio de contenido canónico.
- Separación de commits: esta entrada vive en el vault; los commits del engine (`polymarket-engine`) quedan intactos y separados.

## 2026-10-24 — Segunda pasada

El residuo se re-acumuló desde el 17-sep (el writer sigue muriendo a medias). Escaneo físico completo del vault: 227 tmp con el patrón `*.tmp.<pid>.<hash>`.

- **211 tmp eliminados (~7,0 MB)** con el mismo criterio de la primera pasada: 16 en 0 bytes (sin trabajo único por definición) y 195 superseded (mtime del tmp anterior al mtime del archivo real vigente). 0 huérfanos (ningún tmp sin su archivo base), 0 inciertos (ningún tmp más nuevo que su real), 0 recientes (<2 h). Ninguno bajo git.
- **3 notas vacías eliminadas**: `Sin título.md` en la raíz y en `30-resources/futures/` (0 bytes), y la memoria interna `80-agents/memory/internal/agent-memory/2026-07-25-echo-forge-fase1-g1-validation-continuity.md` (0 bytes desde el 14-ago; contenido ya perdido, memoria interna del agente sin log público).
- Verificado intacto: los 5.302 `.md` (UTF-8 válido, sin bytes nulos), 1.132 imágenes y PDFs íntegros, y las notas reales junto a cada tmp borrado. Los `.cfx` son ZIPs válidos de NinjaTrader (no residuo). Los logs/`.jsonl` vacíos restantes son evidencia legítima (salida vacía real) y se conservan.
- Verificación post-limpieza: 0 tmp, 0 `Sin título` vacíos; las menciones a `.tmp.` en notas son históricas (feedbacks y este log), no enlaces.
- **Pendiente estructural**: el writer de notas del agente sigue dejando residuo en cada ejecución interrumpida; la limpieza es sintomática. Si vuelve a acumular, atacar el writer (eliminación del tmp en exit/kill), no otra pasada manual. El aviso de "archivos corruptos" de Obsidian se atribuye a la base local de Self-hosted LiveSync (cifrado E2E activo); su cura es rebuild de la DB local, no de este vault.
