# REPRODUCTION-RESULTS — Snippet Integrity P0 (2026-10-19)

## Alcance

Reproducción candidate-local sobre Zeus (192.168.31.101), SIN sqcli (el host tenía actividad productiva: proyecto `EchoForgeMT5Exporter`; el experimento no requiere JVM SQX). Todo bajo `/tmp/repro-sip0` y `/tmp/fixval*`, limpiado al terminar. Datos: copies read-only de los respaldos reales del deploy del incidente. El script es el byte-idéntico al del incidente (`b52addbe…`); único delta declarado: `BACKUP_DIR` reubicado a `/tmp` (higiene de auditoría, no toca la lógica del swap).

## 1. Reproducción del incidente (script ORIGINAL) — `REPRODUCIDA`

Setup: candidate SQX con layout mínimo (`user/extend/Snippets/SQ/CustomAnalysis` con el fuente viejo `03106b81` y dir modo `555` — equivalente funcional de `echo-dev:echo-dev 775` para kor; `user/libs` + `internal/libs` kor-escribibles con los JARs viejos; `j64` + 10 SDK jars por symlink).

Resultado (bash `/tmp/s02-rollout/deploy.sh <cand> <workdir>`):

- `preflight OK`, backup, compilación OK (8 clases), stage OK, `javap: processDatabankParallel presente`
- **`swap aplicado (snippet + user/libs jar + Snippets.jar interno)`** ← falso
- Sello `SHA256SUMS.after`: línea 1 `b5f85c4e…` (src) / **línea 2 `03106b81…` (live)** — idéntico al sello real del incidente
- `DEPLOY OK — pendiente canary semántico`
- Post: snippet intocado (`03106b81`, mtime sep-6 preservado), JARs nuevos

El patrón completo de Zeus (éxito reportado + snippet viejo + JARs nuevos) se reproduce **sin ningún proceso externo**: causa suficiente y necesaria demostrada.

## 2. Precedencia fuente→bytecode (por qué JARs nuevos no alcanzan) — `DEMONSTRADA EN PRODUCCIÓN`

No se re-ejecutó canary candidate (requisito: una sola actividad SQX por host; había campañas activas). La precedencia quedó demostrada por el experimento natural del propio incidente en producción real, con 3 puntos:

- canary 1 y 2 (18:03:57Z / 18:09:24Z): JARs S02 en disco + fuente sep-6 → ejecutaron **v1.2** (header del databank, 0 markers).
- canary 3 (18:23:02Z): fuente S02 instalado → marker `Parallel workers: 3`.

Más la precedencia certificada 2026-10-18 (autoridad del fuente en Build 144 headless). El mecanismo runtime no requiere reproducción adicional.

## 3. Semántica bash del silent-skip — `DEMONSTRADA`

`bash -c 'set -euo pipefail; cp -a /nonexistent x.new && mv x.new y; echo SURVIVED'` → imprime `SURVIVED` (rc 0 del script). Regla errexit: el fallo de un comando no-final de una lista `&&` no aborta. Raíz del reporte de éxito falso.

## 4. Validación de la remediación (scripts NUEVOS, candidate-local) — `PASS`

| Test | Setup | Resultado |
|---|---|---|
| A — fail-closed | dir 555 + script nuevo + SHA esperado | **PASS**: aborta EN PREFLIGHT (`sin permiso de escritura sobre el directorio del snippet kor:kor 555 …`), ANTES de backup/compilación/swap; cero mutaciones (JAR intacto, snippet intacto, sin sello) |
| B — éxito completo | dir kor-escribible + script nuevo | **PASS**: `swap aplicado y verificado`, `gate final OK`, sello `live = src = b5f85c4e…`, verificación `cmp` por superficie |
| C — gate en producción real | `verify-plugin-integrity.sh /home/kor/sqx/144 <src> <class>` | **PASS**: source `b5f85c4e`, user/libs/Snippets.jar/cache todos `3ec6e112` (3 hosts) |
| D — detector del estado incidente | candidate con JARs nuevos + fuente viejo + gate con par esperado de la release | **PASS**: `FAIL: source 03106b81… != esperado b5f85c4e… — el runtime recompilaría OTRA versión` (rc 1) |

## Límites de la reproducción

1. La equivalencia `555` vs `echo-dev:echo-dev 775` es funcional (mismo efecto para kor: no-w en dir); el ownership real no se alteró en producción (contrato).
2. No se ejecutó canary candidate-local con sqcli (ventana ocupada); la ejecución de bytecode viejo quedó demostrada en producción durante el incidente. Si se deseara reproducibilidad end-to-end con JVM: procedimiento pasivo listo en `LONG-RUN-INTEGRITY-ACCEPTANCE.md` §Observación.
3. La reproducción usa el layout mínimo del plugin (no un clon completo de la instalación 144): los pasos ejercitados (preflight, backup, compile SDK, stage, swap, seal, gate) son idénticos por construcción del script.
