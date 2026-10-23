# Frame Reconciliation — 2026-10-22 (CLUTIFX FINAL REGULARIZATION, Fase A)

Manifiesto de reconciliación física de frames, antes/después, con causa raíz del
mecanismo que restauraba los archivos retirados. Ejecutado sobre HEAD `a05186a7`.

## Antes → Después

| Capítulo | PNG físicos (antes) | Huérfanos retirados | PNG físicos (después) | Clasificación de los retirados |
|---|---|---|---|---|
| ch02-time | 69 | 4 | 65 | 3 OUT_OF_DURATION (f-004800/f-004806/f-004823) + 1 OUT_OF_DURATION/INVÁLIDO (f-170903, 61743 s) |
| ch03-bias | 162 | 41 | 121 | 41 INVALID_NAME (concatenación manual `minuto+'059'`: f-00059…f-40059) |
| ch07-setups | 132 | 6 | 126 | 6 INVALID_NAME (f-000071 segundos 71>59; f-00321935 y 4 análogos de 8 dígitos) |
| ch08-proceso | 96 | 3 | 93 | 1 INVALID_NAME (f-000075, s=75>59) + 2 HISTORICAL_RESIDUE (f-000801, f-000814) |
| ch10-noticias | 106 | 1 | 105 | 1 HISTORICAL_RESIDUE (f-002148, residuo del naming del frame final) |
| **Total** | **565** | **55** | **510** | 48 INVALID_NAME + 4 OUT_OF_DURATION + 3 HISTORICAL_RESIDUE |

## Evidencia por archivo (los 55)

- Los 55 estaban **borrados previamente** en Git (los retiros originales de los QA
  de ch02/ch03/ch07/ch08/ch10) y fueron **restaurados en disco** después.
- Los 55 son **byte-idénticos** (SHA-256) a su frame canónico ya indexado en
  FRAMES.md (mismo instante, misma extracción ffmpeg): su retirada no pierde
  ninguna evidencia visual única.
- 0 referencias vivas en claims.jsonl/documentation/rules/concepts/examples:
  las únicas menciones de texto (ch02 f-170903 en review-notes y repair/REPAIR-LOG)
  son registros de auditoría históricos, no citas vigentes.
- 0 casos VALID_UNINDEXED, 0 UNRESOLVED. No se eliminó ningún frame único.
- Detalle completo por archivo: `orphan_audit.json` del run (fuera del vault).
- Manifiestos `.deprecated_frame_names`: ch02/ch07/ch08/ch10 ya los declaraban;
  **ch03 se crea en esta operación** con sus 41 nombres (contrato v1.1 §3).

## Causa raíz de la resurrección (A1)

Dos sistemas de sincronización independientes sobre el mismo árbol, sin
protocolo de tumbas compartido:

1. **git autosync** (`~/secondbrain/sync.sh` vía cron, cada minuto): `git add -A`
   + commit + push. Nunca crea archivos: sólo commitea lo que hay en disco.
2. **Obsidian Self-hosted LiveSync** (app abierta 24/7 sobre el vault,
   `liveSync=true`, replicación periódica, CouchDB remoto E2EE): los archivos
   borrados por shell mientras el watcher del plugin no registró la tumba
   seguían en su base remota; la replicación los **re-descargó**.

Evidencia: los archivos restaurados tienen **inodo nuevo** (birth time
2026-10-22 07:00:10–15, creación secuencial = descarga) con **mtime original
preservado** y blob idéntico — patrón de restauración mtime-preserving, no de
re-extracción. Los commits de resurrección (`sync 15:53` 2026-10-20, `sync 06:48`
2026-10-21, `sync 07:01` 2026-10-22) son locales: el cron commiteó lo que
LiveSync había vuelto a poner en disco. El conjunto restaurado incluía también
residuos `.tmp.*` de escrituras atómicas de agentes, que LiveSync sincroniza
igualmente (sincroniza todo archivo del vault).

## Operación de retiro (A3)

- `git rm` de los 55 (reversible: los blobs quedan en el historial; los retiros
  originales ya los habían adjudicado).
- Validadores re-ejecutados por capítulo con `--duration-seconds` exacta.
- Verificación de persistencia: quedó PENDIENTE al cierre de la misión anterior
  (historia preservada en esta sección; el documento COMPILATION-READINESS de
  entonces la daba por verificada con observación pasiva — drift documental que
  la auditoría GOD 2026-10-22 corrigió).

## Verificación de persistencia — CERRADA (auditoría GOD, 2026-10-22 22:2x)

El gate pendiente se cerró con un FIX EN LA CAUSA, no con observación pasiva:

1. **Exclusión soportada del árbol**: `syncIgnoreRegEx = "knowledge-library/clutifx/"`
   en `.obsidian/plugins/obsidian-livesync/data.json` (plugin obsidian-livesync
   v1.0.26; el predicado de sync-target del plugin excluye los paths que
   matchean de propagación Y de reflexión — verificado en `main.js` del plugin:
   `if(syncIgnore.some(e3=>e3.test(file)))return!1`). Se descartó
   `useIgnoreFiles/.gitignore` porque habría excluido el árbol también de git
   (autosync), rompiendo el pipeline de publicación.
2. **Aplicación verificable**: edición de `data.json` con Obsidian activo +
   reinicio controlado de Obsidian (systemd --user, TERM + relanzamiento
   21:53); la config sobrevivió apagado y arranque (re-leída del disco) y el
   proceso quedó vivo con el vault cargado. LiveSync NO se desactivó ni se
   tocaron CouchDB/datos E2EE; la base remota conserva docs Clutifx obsoletos
   (inofensivos: el filtro impide su reflexión local).
3. **Convergencia observada post-fix** (21:53→22:2x, ~30 min): 0/55 nombres
   retirados presentes; 1.033 PNG en 12/12 capítulos = conteo esperado exacto;
   0 adds de frames en git desde el arranque (≈15 ciclos de autosync + ciclos
   continuos de replicación LiveSync); 0 borrados nuevos de frames válidos.
   Adicionalmente, la observación pasiva previa al fix ya acumulaba ~3 h sin
   huérfanos (16:35→19:5x) y el evento inverso (borrado de 6 frames, repuesto)
   está documentado en review-notes de ch01.
4. **Residual honesto**: (a) otros dispositivos con LiveSync sobre el mismo
   CouchDB remoto NO quedan protegidos por este filtro (alcance local a este
   vault — decisión del Owner si aplica); (b) si el Owner revierte la config,
   vuelve el riesgo — la recomendación original queda sustituida por este fix;
   (c) los validadores W06/V11/V04/V05 siguen como red de detección.

`SYNC_INTEGRITY` (gate GOD fase C): evidencia acumulándose desde el fix; el
veredicto final del gate vive en el HANDOFF de la misión GOD.
