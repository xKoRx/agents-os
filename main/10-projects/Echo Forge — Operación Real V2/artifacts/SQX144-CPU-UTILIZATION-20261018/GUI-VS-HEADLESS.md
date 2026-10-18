---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# GUI-VS-HEADLESS — una sola configuración, demostrada con correlaciones en vivo

## Respuesta corta

`same_config: SÍ`. La GUI StrategyQuantX y el CLI sqcli de 144 leen el mismo archivo `/home/kor/sqx/144/user/settings/settings.xml` (con `appPath`/`userPath` absolutos dentro del propio `settings.xml`), y los valores que el owner configuró por GUI están persistidos en disco y **demostrados aplicándose en el CLI headless**.

## Configuración persistida (leída de disco, 2026-10-18)

- Zeus/Hera/Kronos `user/settings/settings.xml`: `<coreUsage>100%</coreUsage>`, `<highPriority>true</highPriority>`, `<threadAffinity>false</threadAffinity>`, `<GCType>ParallelGC</GCType>`; última escritura ~09:52–09:53 local (verificación/re-guardado del owner por GUI). Los `.config` de lanzamiento (`sqcli.config`, `StrategyQuantX.config`) contienen las mismas opciones JVM de arranque en ambos modos (ParallelGC + -Xms4g + proxies/TLS); `StrategyQuantX.config` fue reescrito hoy por la GUI con el mismo contenido efectivo.
- Valor previo en 144 (igual que 142 hoy): `coreUsage=-1`, `highPriority=false` (142 mantiene `-1`/`false`; referencia en SQX-142-VS-144.md).

## Correlaciones CLI↔settings.xml (prueba física de lectura, no supuesto)

| Run CLI (hora local) | Host | settings.xml vigente | Línea log SQX |
|---|---|---|---|
| 01:29 (04:29Z) | Kronos | '-1', prio OFF | "High priority: OFF" / "Using: 75 cores, core usage configuration: '-1'" / "Preparing thread executors: 75" |
| 02:11 (05:11Z, builder E2E) | Kronos | '100%', prio OFF | "Using: 76 cores, core usage configuration: '100%'" / "Preparing thread executors: 76" |
| 01:29 y 01:36 y 02:07 | Hera | '-1', prio OFF | "Using: 63 cores … '-1'" / 63 executors |
| 03:21 (06:21Z, retest post-E2E) | Hera | '100%', prio ON | "High priority: ON" / "Using: 60 cores … '100%'" / 60 executors |
| 14-oct (pre-cambio) | Zeus | '-1', prio OFF | "Using: 27 cores … '-1'" / 27 executors |

Dos hosts × dos valores distintos correlacionan 1:1 con el archivo: la dirección de causalidad es settings.xml → CLI.

## Semántica de reinicio

- **CLI headless**: cada actividad lanza una JVM nueva (`Starting StrategyQuant CLI` por run en launcher log; 58 arranques hoy en Hera) ⇒ **adopta settings.xml en el siguiente run sin reiniciar nada**; no existe proceso SQX residente que conservar (el "Server started on port 5050" de cada run muere con el run). El aviso de la GUI ("requiere reiniciar") aplica sólo a una instancia GUI abierta; al momento del diagnóstico no hay ningún proceso StrategyQuantX vivo en la flota (ps 3/3 hosts).
- **GUI**: si el owner dejara una GUI abierta de antes del cambio, esa instancia conserva valores viejos en memoria hasta reiniciarla; no afecta al CLI.

## Diferencia material restante GUI vs CLI

Ninguna en CPU. Única diferencia de entorno: el CLI hereda `JAVA_TOOL_OPTIONS` de la unidad systemd (heap `-Xmx55g`, ver JVM-LAUNCH-CONTRACT.md) y una GUI lanzada a mano no; efecto en paralelismo: nulo.
