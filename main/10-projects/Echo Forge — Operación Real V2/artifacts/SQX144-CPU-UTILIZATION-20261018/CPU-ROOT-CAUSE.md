---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e84f1faa1d4050b7ab35255863b2992e5 (release 0.3.1)"
verdict: "SQX144_CPU_EXPECTED_BEHAVIOR"
related:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# CPU-ROOT-CAUSE — SQX 144 utilización de CPU en la flota Forge

## Veredicto

`SQX144_CPU_EXPECTED_BEHAVIOR` — no se demostró ninguna restricción accidental de recursos o configuración; la baja utilización de CPU observada durante "Builder" queda explicada por la estructura de fases del proceso `sqcli`, medida con evidencia física (sar, logs SQX, logs worker), y la configuración Max Performance del owner está persistida y demostrada aplicándose en el CLI headless.

## Causa raíz de la percepción "Builder apenas usa CPU"

Un run de builder de Forge (`sqcli -project action=start name=custom`) no es una sola fase genética: es un proyecto SQX con dos tareas, y el 96% del wall time ocurre en la segunda, que es secuencial por diseño del API CustomAnalysis de SQX y del snippet Forge. Medición física del builder real del E2E w10 en Kronos (FlowRun 79385c32, task 01_builder, 2026-10-18 05:11:27Z→06:20:42Z, `duration_ms=4154640` = 69,2 min, log worker Kronos):

| Subfase del run sqcli | Duración | % wall | CPU medida | Fuente |
|---|---|---|---|---|
| Boot JVM + licencia + carga datos/proyecto | ~24 s | 0,6% | 1 core | launcher + log SQX 02:11:30–02:11:52 local |
| Build genético (4 islas, pop 20, corta a 1000 estrategias) | 126 s (02:11:52→02:13:58) | 3% | multihilo disponible, trabajo corto | log SQX "Build finished because totally 1000 strategies were generated" |
| **CustomAnalysis inyectada por Forge (overview producer) + escritura 649 archivos output** | **~60 min (02:14:00→03:14:10)** | **87%** | **~1,05 core sostenido** | log SQX; sar Kronos %user 1,39% de 76 cores |
| Sync databank output (649 archivos) | 145,5 s | 3,5% | ~1 core, I/O | log SQX "saved 649 … in 145.50 s" |
| Teardown + sync Results | ~8 s | 0,2% | — | log SQX 03:20:36–03:20:41 |

sar Kronos durante toda la ventana del builder (`sar -f /var/log/sysstat/sa18 -s 02:00:00 -e 04:00:00`, hora local): `%user 1,39–1,71`, `%idle 98,3–98,6`, load average ~1,0 — es decir ~1,05 núcleos activos de 76, mientras SQX tenía preparados 76 thread executors (`Preparing thread executors: 76`, log SQX 02:11:35 local). El patrón se repite en Hera pre-incidente (builder 04:36:25Z→05:05Z, sar %user 1,6–6,6 de 64) y en las fases de retest de los tres hosts (2–3 cores por host).

## Hipótesis descartadas con evidencia

- **"Builder es single-core por diseño"**: falso como enunciado general. SQX 144 reconoce todos los cores del host y prepara un executor por core (27/28 Zeus, 63/64 Hera, 75–76/76 Kronos, logs SQX citados). La fase genética usó su paralelismo; simplemente representa el 3% del wall time en este proyecto.
- **Quota/cgroup restrictiva**: sin límite. `cpu.max` ausente en `/system.slice/stager-runtime.service/` (Zeus/Hera/Kronos), `cpuset.cpus.effective` 0–N completo, `cpu.stat` del servicio sin throttling, `%steal` 0–0,02% en sar de los 3 hosts. No hay `CPUQuota`/`CPUWeight` en la unidad.
- **Affinity/thread pinning**: no hay `taskset`/`sched_setaffinity` en la ruta de lanzamiento (`process_nonwindows.go` solo fija `Setpgid`); `<threadAffinity>false</threadAffinity>` en settings.xml 144.
- **JVM que no ve los cores**: Zulu OpenJDK 25.0.2 64-bit; sin `ActiveProcessorCount`; JVM cgroup-aware sin límites ⇒ `availableProcessors` = cores del host, confirmado por las líneas "Using: N cores" de SQX.
- **GUI vs CLI con distinta configuración**: ambos leen el mismo `user/settings/settings.xml` (correlaciones en vivo documento en GUI-VS-HEADLESS.md).
- **Heap/memoria**: pico RSS ~12 GB de 70/98/125 GB por host (sar -r), `MemoryMax=infinity`, sin swap; sin presión de memoria ni GC patológico.

## Configuración Max Performance del owner (confirmada + demostrada en CLI)

Persistida en `/home/kor/sqx/144/user/settings/settings.xml` en los 3 hosts: `<coreUsage>100%</coreUsage>` y `<highPriority>true</highPriority>` (última escritura 2026-10-18 ~09:52–09:53 local). El CLI headless lee ese mismo archivo en cada arranque (cada run sqcli es una JVM nueva) y se demostró físicamente la adopción: Hera 03:21:35 local (ventana retest 06:21Z) logró `High priority: ON` + `Using: 60 cores, core usage configuration: '100%'` → 60 executors; Kronos 02:11 local `Using: 76 cores, '100%'` → 76 executors. Durante el builder E2E el valor vigente ya era '100%' en Kronos; el `High priority: OFF` inicial se debía al valor persistido `false` de antes de la intervención del owner. Nota: no hubo aún ningún run CLI en Zeus con la configuración final (su último sqcli fue 14-oct); su settings.xml en disco ya contiene 100%+true y el mecanismo de lectura está demostrado en los otros dos hosts.

## Dónde NO hay palanca de configuración

Con Max Performance el paralelismo ya está ofrecido a SQX; el cuello real es software: (1) la CustomAnalysis del overview producer itera estrategias de a una (~5,5 s/estrategia × 649 = ~60 min en 1 core) y (2) cada actividad de retest paga ~10–15 s de boot fijo de JVM (licencia + datos + proyecto) sobre runs de 17–30 s. Ambos son cambios de producto/Forge, no de configuración de flota; quedan registrados en REMEDIATION-PLAN.md como oportunidades, fuera del alcance de este mandato ("no rediseñar Forge").

## Benchmark before/after

No aplica: la evidencia read-only (sar + logs) cierra las preguntas Q1–Q10 y no existe candidato de configuración que mejorar (no hay restricción que corregir); un benchmark sólo reproduciría la misma estructura de fases y cualquier candidato real exigiría modificar el snippet de Forge (fuera de alcance). Condiciones del mandato: "Primero agotar evidencia read-only" — agotada.
