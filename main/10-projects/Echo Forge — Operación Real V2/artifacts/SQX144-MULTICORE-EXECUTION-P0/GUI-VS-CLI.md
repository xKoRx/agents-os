---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# GUI-VS-CLI — estado de la comparación física y respuesta operativa

## Respuesta a la pregunta del mandato

"¿La ejecución CLI altera el paralelismo efectivo o solamente cambia la forma de iniciar el proceso?" → **No altera el paralelismo.** La evidencia es directa: TODAS las mediciones de esta sesión son ejecuciones CLI headless (`sqcli -project action=start`) y en ellas SQX usó hasta 74-77 cores de 76 (builder 68,5 sostenidos; retest N=450-600 pico 72,6-74,1; optimizer WFO pico 72,6). Si el arranque CLI degradara el paralelismo, esos números serían imposibles. La hipótesis del launcher queda además descartada mecánicamente: `sqcli` es un launcher Go que exec-reemplaza a la JVM en el mismo proceso (comm=sqcli con 258-273 threads; sin capa intermedia); `process_nonwindows.go` sólo fija `Setpgid`.

## Comparación física GUI-vs-CLI mismo proyecto/corpus: BLOCKED_INFRA (no esencial)

- Los tres hosts Linux de la flota no tienen X disponible para el agente: sin sockets `/tmp/.X11-unix`, sin Xvfb/xvfb-run, sin sudo (rol operator sin privileged). La GUI StrategyQuantX requiere display Swing; no hay forma de lanzarla sin ventana del owner.
- No existe wrapper en la ruta de producción que probar (el worker invoca `sqcli` directo; `run_sqcli.sh` es camino manual GUI-era, fuera del camino headless).
- La correlación de configuración GUI↔CLI ya está demostrada físicamente (SQX144-CPU-UTILIZATION-20261018/GUI-VS-HEADLESS.md): ambos modos leen el MISMO `user/settings/settings.xml`, con dos hosts × dos valores correlacionando 1:1 en logs de arranque ("Using: N cores, core usage configuration: 'X'"), incluyendo runs del owner por GUI la mañana del 2026-10-18.

## Procedimiento para cerrar el formalismo si el owner lo desea (ventana owner, ~15 min)

1. En Kronos con sesión gráfica: abrir GUI de 144 (flota o candidate), cargar un proyecto con retest de databank ≥300 estrategias (p.ej. importar `forge-multicore-p0/corpus/overview1117` a un databank), ejecutar con settings Max Performance.
2. En otra terminal: `sar -u 5` + `top -H` durante la fase de retest; comparar con `rec/retest144-n600-cpu.csv` (pico 74 cores).
3. Criterio: GUI alcanza el mismo orden de cores en fase caliente ⇒ launcher descartado también formalmente. Cualquier desviación >2× sería el único caso que reabriría la hipótesis GUI/CLI.

Este pendiente NO afecta el veredicto P0: la ruta de producción es CLI, y la ruta CLI está medida usando todos los cores.
