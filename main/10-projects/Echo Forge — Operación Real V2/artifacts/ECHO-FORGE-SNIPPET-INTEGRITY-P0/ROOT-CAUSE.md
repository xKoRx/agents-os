# ROOT-CAUSE — Snippet Integrity P0 (2026-10-19)

## Veredicto

`SNIPPET_INTEGRITY_ROOT_CAUSE_CONFIRMED` — **no existió ningún proceso restaurador**. El snippet viejo nunca fue "restaurado": **nunca llegó a instalarse**. El swap silencioso de `deploy-plugin-s02.sh` (línea 95) falló por permisos y el script siguió como si nada, reportando `DEPLOY OK`.

## Mecanismo causal demostrado

1. En Zeus el directorio de snippets `user/extend/Snippets/SQ/CustomAnalysis` es `echo-dev:echo-dev` modo `775`. El usuario `kor` (identidad de todo el rollout) **no pertenece al grupo `echo-dev`** → no puede crear archivos ahí.
2. La línea 95 del script original era `cp -a "${SRC}" "${SNIPPET}.new" && mv -f "${SNIPPET}.new" "${SNIPPET}"`. Bajo `set -e`, **un `cp` que falla en posición no-final de una lista `&&` NO aborta el script** (regla de errexit de bash: el fallo de un comando no-final de una lista `&&`/`||` no dispara la salida; verificado empíricamente y en la reproducción FASE B). El `mv` nunca se ejecuta, el script continúa, sella y reporta éxito.
3. Las líneas 93/94 (JARs `user/libs` e `internal/libs`) SÍ se aplicaron: ambos directorios son escribibles por `kor`. Resultado: **estado mixto** — JARs con bytecode S02 nuevo + snippet fuente con la versión antigua (`03106b81`, mtime 2026-09-06 10:13:10, nunca modificado desde su instalación inicial).
4. En Build 144 headless la **fuente es la autoridad efectiva**: sqcli recompila por corrida desde el snippet y esa compilación prevalece sobre JARs (precedencia certificada 2026-10-18; re-demonstrada hoy). Por eso los canaries 1 y 2 ejecutaron el exporter **v1.2** (sin marker `Parallel workers:`), recompilando el fuente viejo que siempre estuvo en disco.

## Evidencia determinante

- Sello del propio deploy fallido `SHA256SUMS.after` (Zeus `backup/plugin-s02-20261019T180331Z/`, mtime 18:03:34.439Z): línea 1 = src del bundle `b5f85c4e…` (nuevo), **línea 2 = snippet live `03106b81…` (viejo)**. El script registró, sin darse cuenta, que el archivo live siguió siendo el viejo.
- `stat` del directorio `CustomAnalysis`: `ctime == mtime == 2026-10-19 18:22:43.495992274Z` — el único cambio de metadata del dir es la creación del archivo en la corrección de 18:22Z. **Nunca hubo `chmod`** que hubiera hecho el dir escribible por `kor` en 18:03Z.
- `test -w` como `kor` sobre el dir: `KOR-NOT-WRITABLE` (verificado en vivo).
- No hay watcher vivo ni histórico: único proceso con inotify en Zeus es systemd/dbus (escaneo completo de `/proc/*/fdinfo` como root); `stager.timer` corre como usuario `stager` con `ProtectSystem=full` (no puede escribir en `/home/kor`); sin cron/timer que toque `sqx/144`; `journalctl` 17:45–18:35Z sin sudo ni sesiones relevantes.
- Canario 1 (18:03:57Z) y canario 2 (18:09:24Z): 0 ocurrencias de `Parallel workers`, header `EchoForgeOverviewExporter v1.2 DATABANK`. Canario 3 (18:23:02Z, tras la instalación real de 18:22:43Z): `Parallel workers: 3`.
- Reproducción exacta candidate-local (FASE B): mismo script, dir 555 → "swap aplicado… DEPLOY OK" con sello `src=nuevo / live=viejo`, snippet intocado con su mtime original. Sin ningún otro actor.

## Correcciones al relato del rollout (PLUGIN-ROLLOUT-3OF3.md)

- "El snippet fuente reapareció con contenido y mtime del 14 de octubre": **incorrecto**. El contenido viejo tiene mtime **2026-09-06 10:13:10** (instalación inicial del plugin) y nunca salió de disco. No existe copia alguna con mtime 14-oct en el host.
- "Un proceso no identificado restauró el snippet viejo una vez": **falso** — no hubo restauración; hubo instalación que nunca ocurrió más reporte de éxito falso.
- La corrección de 18:22:43Z (instalación `echo-dev:echo-dev` 664 del fuente S02) fue la primera escritura real del snippet ese día y permaneció estable a través de canary 3, E2E w11, 10 runs del cert CPU (proyecto `custom`, 19:35–19:49Z) y runs del proyecto `EchoForgeMT5Exporter`.

## Por qué afectó a S02 en Zeus y no a Kronos/Hera

Único factor diferencial: **ownership del directorio de snippets**. Kronos y Hera lo tienen `kor:kor`; el mismo script con el mismo bug completó allí el swap del fuente (sus sellos `SHA256SUMS.after` muestran `live = b5f85c4e…` en ambas líneas). Ver `KRONOS-COMPARISON.md`.

## Prevención

`fix/snippet-integrity-p0` @ `xKoRx/symphony` (`fe77854c`): deploy fail-closed (preflight de escritura sobre el DIRECTORIO, verificación por superficie con `cmp`, snippet primero, gate final source→bytecode) + gate read-only pre-dispatch `verify-plugin-integrity.sh`. Detalle y estado de adopción en `REMEDIATION-AND-ROLLBACK.md`.

## Fuentes crudas

`/home/kor/aranea/work/snippet-integrity-p0-20261019/evidence/` (fuera del vault): `zeus-SHA256SUMS.before` / `zeus-SHA256SUMS.after` (sellos del deploy 18:03Z), `zeus-canary1-databank.log` (header v1.2), `zeus-original-deploy.sh` (SHA256 `b52addbe38767fad2b1dabf34e23579435a44b7db7c08a702c2a5e689069ee9e`, idéntico byte a byte al local del workspace y al ejecutado).
