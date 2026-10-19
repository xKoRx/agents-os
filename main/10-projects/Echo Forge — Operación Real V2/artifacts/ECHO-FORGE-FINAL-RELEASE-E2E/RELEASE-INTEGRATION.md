# RELEASE-INTEGRATION — Gate A (2026-10-19)

## Veredicto

GATE_A_PASS — S01+S02 integrado en master de `xKoRx/symphony` y publicado; árbol limpio; sin cambios en Strategy, MM, WFM, ranking ni contratos congelados; `EchoForgeParallelProbe` queda FUERA del classpath productivo.

## Integración

- Base: master `492a271e84f1faa1d4050b7ab35255863b2992e5` (release 0.3.1), fresco y limpio, verificado contra origin.
- Contenido integrado: exclusivamente `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeOverviewExporter.java` (S01 `cf8f522c` + parte exporter del candidato S02 `568907b`; 386 inserciones / 87 eliminaciones, 1 archivo).
- `EchoForgeParallelProbe.java` (diagnóstica, commits `568907b`/`f4755c3`) NO fue integrada: el build productivo contiene 0 clases probe (verificado por listing del JAR y grep `probe`).
- Commit de integración: `619c3b6f71a0d8198783a7ab5684767b6ddf15d9` (rama `s02-integration` → merge FF a master, pusheado a origin).

## Adaptación del default de workers (cambio mínimo del mandato)

- Hecho demostrado: `writeExporterProperties` (`sqx/activities/worker/steps/steps.go:2975`) reescribe `exporter.properties` en cada corrida con contenido fijo (wave/stage/output_dir/instrument/timeframe/direction/clear_output/variant) — cualquier `workers=16` manual se pierde.
- Decisión: NO usar el writer Go ni crear knob público nuevo; el default automático de S02 se amplió de `min(8, cores-1)` a `min(16, max(1, cores-1))`, acotado además por el número de estrategias (`resolveWorkers`): Kronos 76 cores → 16; Zeus 28 cores → 16; si el databank tiene <2 estrategias, secuencial. El valor de producción nace siempre del default (determinista por host).

## Verificaciones pre-merge

- Build simulador: OK (65 archivos contra stubs).
- Suite JUnit del plugin: 13/13 PASS (trade conformance, resolve main result, config, robust run params).
- `scripts/verify_build.sh`: OK — JAR sim y `EchoForgeAutomator.jar` con sólo las 5 clases de exporters productivas, sin test-support.
- Build producción contra SDK SQX local: OK (55 clases; 8 de `EchoForgeOverviewExporter*`).
- Regresiones Go: `go test ./sqx/activities/worker/...` PASS (worker 14.9s, pipeline, hooks, steps) — sin cambio Go; el fallo `pebbe/zmq4` (libzmq.pc ausente) es ambiental preexistente documentado y ajeno al área.
- Efecto secundario conocido: `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` queda modificado por correr la suite; restaurado a HEAD (patrón del commit `f02bf39`).

## Estado final

- Master `619c3b6f` (luego `daded14` con el manifest de release; documental, no funcional), tree limpio, `origin/master` == local.
- Certificación física del candidato que respalda esta integración: `SQX144-FULL-MULTICORE-CERTIFICATION/` (13,4× paridad FULL 300 estrategias / 33.858 filas monthly).
