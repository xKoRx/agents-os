# PLUGIN-ROLLOUT-3OF3 — Plugin Java real S02 (2026-10-19)

## Veredicto

PLUGIN_EFFECTIVE_3OF3_PASS — cadena Source Git → compilación SQX 144 por host → clases → Snippets.jar/JAR/snippet → JVM → output demostrada en Kronos, Hera y Zeus, en ese orden, con canary semántico y marker runtime `Parallel workers: N` (imposible en bytecode anterior). SQX 142 no tocado. Una sola instancia SQX por VM en todo momento (preflight fail-closed por host).

## Origen y compilación

- Fuente canónica: `EchoForgeOverviewExporter.java` @ `619c3b6f`, SHA256 `b5f85c4ed0b37a8551f017210a29da2f36611c0bf52739f31008887dceffb0c8` (transferido por bundle + SHA verificado por host).
- Compilación EN CADA HOST con su propio JDK (`<SQX>/j64/bin/javac`, Zulu 22) contra el SDK local 144 (`build.sh` modo producción) — sin reutilizar bytecode entre hosts.
- Compilación determinista: las 8 clases `EchoForgeOverviewExporter*` tienen SHAs idénticos 3/3 (main `3ec6e112dc771e0f6170f11df97154ffc02559df9828f9b5e498421737d08bc0`).
- `javap` verifica `processDatabankParallel` presente 3/3; `cmp` byte-exacto de cada entrada re-extraída del JAR staged vs clase compilada.

## Superficies actualizadas por host (uniformes)

- Snippet fuente `/home/kor/sqx/144/user/extend/Snippets/SQ/CustomAnalysis/EchoForgeOverviewExporter.java` → `b5f85c4e…` — **autoridad efectiva en Build 144 headless** (precedencia certificada 2026-10-18; sqcli recompila por corrida sobre el cache/JAR).
- `/home/kor/sqx/144/user/libs/EchoForgeAutomator.jar` (update quirúrgico `jar uf` de las 8 clases): Kronos `cb5d53c2…`, Hera `d7017429…`, Zeus `91ed5c2f…` (las bases diferían por host; las entradas actualizadas son idénticas).
- `/home/kor/sqx/144/internal/libs/Snippets.jar` (mismo update quirúrgico, escribible 3/3): Kronos `8e39242c…`, Hera `b43cc6a5…`, Zeus `5efcc876…`.
- Cache de snippets `internal/tmp/compiled/SQ/CustomAnalysis/`: sincronizada SOLO con las 8 clases objetivo donde existe (Zeus) — sin vaciar el cache completo (contrato de la skill).

## Backups y rollback

- Backup por host en `/home/kor/backup/plugin-s02-<TS>/` (snippet + ambos JARs + estado previo del cache + sellos SHA256SUMS before/after).
- `rollback.sh` ejecutable por host (falla cerrado si hay sqcli activo). Rollbacks NO ejecutados (no hubo fallo que los requiera).

## Canary semántico (proyecto scratch `ef-canary-s02-*`, 2–3 estrategias copiadas read-only de la flota)

- Kronos 18:57Z: rc=0, marker `Parallel workers: 2` (acotado por estrategias), processed 2/2 con trades reales (9278), overview.ndjson 2/2, monthly 92, `_SUCCESS`, 0 procesos residuales.
- Hera 18:59Z: rc=0, marker `Parallel workers: 2`, 2/2 filas, monthly 92, `_SUCCESS`, 0 residuales.
- Zeus 18:23Z (tras corrección, ver abajo): rc=0, marker `Parallel workers: 3`, 3/3 filas, monthly 138, `seen=3 written=3 errors=0`, 0 residuales.
- El marker runtime prueba el bytecode efectivo ejecutado (la cadena `Parallel workers` sólo existe en S02).

## Incidente Zeus (resuelto y documentado)

- Primer y segundo canary en Zeus ejecutaron código ANTIGUO (sin marker). Causa raíz operativa: (1) el directorio de snippets de Zeus es `echo-dev:echo-dev` (propiedad distinta a Kronos/Hera, kor-owned) y el swap inicial como kor no persistió como se esperaba; (2) Zeus tiene cache de snippets en `internal/tmp/compiled` (Kronos/Hera no) y el recompilado por-corrida desde el snippet viejo pisa los JARs actualizados.
- Resolución: instalación del snippet por vía privilegiada (`sudo install -o echo-dev -g echo-dev -m 664`, preservando propiedad/permisos originales — mismo patrón que el rollout del 18-oct para el MT5 snippet) + resincronización del cache + canary PASS con marker. El snippet permaneció estable (`b5f85c4e…`) a través del canary y del E2E completo posterior.
- Residuo forense no explicado: entre el swap inicial (15:03Z, SHA leído correcto) y el canary 1 el archivo reapareció con contenido/mtime del 14-oct; no se identificó el proceso restaurador. El estado final es estable y fue re-verificado post-E2E.

## Evidencia en el E2E real

- CustomAnalysis del builder w11: TASK `Custom analysis` 18:47:45→18:49:55Z (2m10s para 846 estrategias — sólo explicable por la ruta paralela; detalle en `E2E-CPU-PERFORMANCE.md`).
- Proyectos canary scratch `ef-canary-s02-*` dejados en los 3 hosts como evidencia (sin impacto: proyectos inertes fuera del pipeline).
