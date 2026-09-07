---
type: session
schema_version: 1
scope: session
created: "2026-07-22"
updated: "2026-08-11"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
application: "[[StrategyQuant X]]"
entities:
  - "[[Symphony]]"
  - "[[StrategyQuant X]]"
  - "[[sqcli-builder-existing-portfolio-databank-unresolved]]"
  - "[[sqcli-echoforge-class-not-found-fresh-worker]]"
related:
  - "[[sqcli-project-does-not-exist]]"
  - "[[sqcli-databanks-not-found]]"
aliases:
  - Kronos builders fallando
  - Symphony worker Zeus Hera Kronos divergence 2026-07
confidence: high
source_session: "0bd267d6-a6bb-43ff-af9e-32d1472b91e9"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/strategyquant-x
  - app/strategyquantx
  - area/symphony-portal
  - area/symphonyportal
  - kind/session
  - project/symphony
  - scope/session
---
# Session Summary - 2026-07-22 - Symphony Kronos builder failures (EchoForge)

> [!info]+ Session summary L1
> Diagnóstico y resolución de fallo de `01_builder` en Kronos en el wf
> `sqx-main-00_configs-v1-NDX-H1-L-1784762810` mientras Zeus y Hera sí
> procesan el mismo flow. Dos errores raíz independientes:

## Objetivo

- Diagnosticar y resolver por qué Kronos fallaba en `01_builder` para el wf
  `sqx-main-00_configs-v1-NDX-H1-L-1784762810` cuando Zeus y Hera procesaban
  el mismo flow sin inconvenientes.
- Garantizar que la información (causas, evidencia, mitigación) no se
  pierda tras el cierre de la sesión.

## Contexto cargado

- `80-agents/skills/symphony-worker-ssh` y `symphony-worker-troubleshooting`
  para introspección remota de los 3 workers (Zeus, Hera, Kronos).
- Historia completa del wf vía cliente Temporal
  (`host=192.168.31.46:7233, namespace=sqx-prop`). El wf corre el flow
  `example_flow_22` cargado en MinIO.
- Inspección local del `input/example/config.json` (no era el config real del wf,
  que vino desde MinIO; estrategia `example_flow_24`, no `example_flow_22`).

## Trabajo realizado

### 1. Diagnóstico del wf

- `extract_payloads.go` para decodificar `sqx_raw_log` de cada
  `ActivityTaskCompleted` con payloads base64 del event `ActivityTaskCompleted`.
- `extract_raw_logs.go` para filtrar solo las líneas relevantes (`Project has
  unresolved resources`, `Cannot start project`, `Loaded 0 strategies to
  databank…`, etc.).
- Comparación de logs lado a lado: `builder_log.txt` (Kronos) vs
  `hera_builder_log.txt` (Hera, `identity: @sqx-ulab-hera-0@`).

### 2. Causa raíz n.° 1 — `Project has unresolved resources` en Kronos

- **`builder_test.cfx`** descargado desde MinIO a `/tmp/builder_test_from_minio.cfx`,
  descomprimido con `unzip`. Inspección del `Build-Task1.xml` (1.24 MB):
  - `<FitPortfolio active="false" databank="Existing portfolio">`.
- **`config.xml`** del mismo CFX declara 7 databanks (Results, Last generation,
  Initial population, Strategies to improve, Strategies to optimize, input, output).
- **No contiene** una entry para `Existing portfolio`.
- **Hera y Zeus** tienen `~/sqx/user/projects/custom/databanks/Existing portfolio/`
  con `Birth: 2026-06-03` y `2026-06-18` respectivamente. SQX carga implícitamente
  databanks sueltos en disco si están en `databanks/` aunque no estén declarados
  en `config.xml`. Resultado: Hera y Zeus resuelven 8 databanks y arrancan el
  build, mientras Kronos resuelve 7 y aborta con `unresolved resources`.
- Resultado: `01_builder` falla inmediatamente. `02_optimize_wfm > import_metadata`
  sigue y procesa, pero `classify_and_rank` falla en el siguiente paso con
  `metadata missing for wave`.

### 3. Causa raíz n.° 2 — `Class with name 'EchoForgeOverviewExporter' doesn't exist` (worker fresco)

- SQX no carga el JAR directamente; **extrae los `.class` a
  `~/sqx/internal/tmp/compiled/`** y los referencia desde ese classpath.
  Verificación: comparación de SHA256 del
  `EchoForgeOverviewExporter.class` en JAR (3 workers mismos bytes
  `4138c3e2...`) y en el `compiled/` de Hera (idénticos).
- **Dos factores necesarios para que el cache exista**:
  - (a) Permisos del JAR: `0664` para que SQX pueda ejecutar la fase de copy
    de classpath sin restricciones. Hera/Zeus `0664`, Kronos `0644`.
  - (b) Carpeta `internal/tmp/compiled/` poblada al menos una vez en el
    arranque. Hera la tiene desde 2026-07-22 16:59. Zeus la tiene vacía desde
    2026-07-18 (pero su JAR escribible re-puebla en cada arranque
    exitoso: por eso sigue corriendo). Kronos no la tiene.

### 4. Mitigación aplicada en Kronos (`192.168.31.121`)

```bash
JAR=/home/kor/sqx/user/libs/EchoForgeAutomator.jar
chmod 0664 "$JAR"
mkdir -p /home/kor/sqx/internal/tmp/compiled
cd /home/kor/sqx/internal/tmp/compiled
unzip -oq "$JAR"
sha256sum SQ/CustomAnalysis/EchoForgeOverviewExporter.class
# 4138c3e2b058ecae5a7aff0dcae7cb2ae3e66b5a203aaed1bdf8a9b6ce6e2aa7 ✓
```

- Backup defensivo: `/home/kor/sqx/user/libs/EchoForgeAutomator.jar.bak-20260722_195108`
- Magic bytes del `.class` extraído confirmados: `0xCAFEBABE` (Java class válido).
- El cómputo de `sha256` es idéntico al de Hera.

## Artifacts creados o modificados

- `scratch/extract_payloads.go` — decodifica payloads base64 del wf Temporal.
- `scratch/extract_raw_logs.go` — filtra líneas relevantes del `sqx_raw_log`.
- Notas de memoria (L3 Known Errors):
  - [[sqcli-builder-existing-portfolio-databank-unresolved]]
  - [[sqcli-echoforge-class-not-found-fresh-worker]]

## Memoria propuesta o creada

- **L3 Known Error #1** — `sqcli-builder-existing-portfolio-databank-unresolved`
  documenta el mismatch config.xml ↔ Build-Task1.xml en `builder_test.cfx`
  versionado en MinIO y propone corregir el CFX upstream.
- **L3 Known Error #2** — `sqcli-echoforge-class-not-found-fresh-worker`
  documenta los dos factores (permisos JAR + cache compilado) y propone
  automatizar la regularización del worker como `systemd unit` o skill
  `symphony-worker-bootstrap`.

## Decisiones

- **No tocamos el `builder_test.cfx` en MinIO** en esta sesión. El usuario
  pidió "regularizar Kronos" (estado local), no un cambio upstream. La
  decisión queda documentada en el L3 Known Error #1 como mitigación
  pendiente para un PR posterior contra `SYMPHONY/exporter-plugin` o
  el artefacto de la wave 13.
- **Solución a escala**: añadir un post-install del binario `symphony-worker`
  que haga los 3 comandos arriba. Pendiente de extracción como
  skill (`symphony-worker-bootstrap`) y runbook en `30-resources/runbooks/symphony/`.

## Pendiente

- Corregir el `builder_test.cfx` en el artefacto upstream
  (`sqx/exporter-plugin/`, `${HUB}/input/wave*/.../builder_test.cfx`,
  o el equivalente en MinIO según el flujo de release) para alinear
  `config.xml` con `Build-Task1.xml` (opción a — agregar
  `<Databank name="Existing portfolio" />`). Esto elimina el problema
  para todos los workers, no solo Kronos.
- Investigar el pipeline de packaging del worker
  (`./scripts/build-worker.sh` o `Makefile` equivalente) para entender
  por qué el JAR sale con `0644` en vez de `0664`.
- Repetir el smoke test de `01_builder` en Kronos tras la regularización,
  idealmente lanzando un wf nuevo con el mismo config que disparó esta
  sesión para validar end-to-end.

## Operación efectiva

- **Hosts**: Zeus (101), Hera (111), Kronos (121).
- **Username SSH**: `kor`; usar el wrapper canónico `echo-forge-worker` para resolver la credencial compartida.
- **Cliente Temporal**: `192.168.31.46:7233`, namespace `sqx-prop`.
- **WID afectado**: `sqx-main-00_configs-v1-NDX-H1-L-1784762810`.

---

## ⚠️ Addendum — 2026-07-22 ~20:08 (revisión tras volver a fallar)

Después de aplicar los dos fixes de esta sesión, el usuario reportó
**"volvió a fallar"**. Una revisión más profunda en vivo (con wfs nuevos
todavía encolados) reveló datos que **refutan parcialmente la Causa #1**.

### Lo que SÍ se confirmó del fix original

- Permisos del JAR `EchoForgeAutomator.jar` en Kronos pasaron de `0644` →
  `0664` (idéntico a Zeus/Hera).
- El cache `internal/tmp/compiled/SQ/CustomAnalysis/` se pobló en Kronos
  con los 18 `.class` extraídos del JAR; SHA256 de
  `EchoForgeOverviewExporter.class = 4138c3e2...` (idéntico al de Hera).
- **`Class with name 'EchoForgeOverviewExporter' doesn't exist`**: ya no
  aparece en el log desde 13:00 UTC (≈ 11:00 -04). El último en línea
  395220 / 683430 = ~58%. **Causa #2 RESUELTA en producción.**
- `Existing portfolio` ahora se carga y aparece en los logs recientes
  (`Loaded 0 strategies to databank Existing portfolio`) en wfs que sí
  llegan a la fase Builder.

### Lo que se REBUTIÓ de la Causa #1

- **Hera NO tiene "Project has unresolved resources" en ningún momento** del
  día (verificación `grep -c "Project has unresolved" /var/log/.../symphony-worker.log = 0`).
- **No es `Existing portfolio` la diferencia**: ambos CFX (`builder` con
  `databank="Existing portfolio"` y `retester` con `databank="null"`)
  funcionan en Hera sin tocar esa carpeta databank.
- El repo Symphony trae en `input/example/builder_test.cfx` línea 153 un
  `<FitPortfolio active="false" databank="Existing portfolio">` (correcto).
  `input/example/retester_test.cfx` y el original exportado de SQX
  (`scratch/retest_test/Retest-Task1.xml:99`) también lo traen bien. Sin
  embargo, el
  `sqx/exporter-plugin/test-support/custom_project_config/CustomAnalysis-Task1.xml:38`
  está mutado a `databank="null"` (literal string "null").

### Por qué Kronos sigue fallando

El fenómeno auténtico probablemente es un **estado persistente de la
workspace de SQX en `/home/kor/sqx/user/projects/custom/`** (bases
internas de SQX que viven en disco y se regeneran tras `sqcli -project
action=start` fallidos). El fix local de esta sesión **restauró la base
del plugin y los permisos del JAR**, lo cual atacó una de las dos
condiciones necesarias para que la workspace arrancara limpio. La otra
condición (workspace limpia de cualquier estado intermedio corrupto) **no
se tocó en esta sesión** y queda como misterio abierto.

El usuario **canceló el resto de la investigación**. Decisión textual:

> "nah cancela, los cfx no son el problema porque funcionan perfectamente
> en zeus y hera. así que cierra sesión, seguiré con otra IA"

### Lo que significa para los L3 Known Errors

- [[sqcli-echoforge-class-not-found-fresh-worker]]: **se mantiene
  íntegramente**. La causa raíz del error de plugin loading es real, los
  fixes aplicados funcionan, y la receta `chmod 0664` + `unzip` al cache
  son válidos para cualquier worker recién provisionado.
- [[sqcli-builder-existing-portfolio-databank-unresolved]]: **queda
  obsoleto como causa raíz**. Mantenerlo puede confundir a futuras
  sesiones. Se recomienda reescribirlo con foco en:
  - la mutación del template en
    `sqx/exporter-plugin/test-support/custom_project_config/CustomAnalysis-Task1.xml:38`
    (sustituir `"null"` por `"Existing portfolio"`),
  - la nota explícita de que la diferencia Hera vs Kronos es workspace
    state, **no** la presencia del databank en disco.

Esta rectificación queda pendiente para la siguiente sesión que tome el
caso.
