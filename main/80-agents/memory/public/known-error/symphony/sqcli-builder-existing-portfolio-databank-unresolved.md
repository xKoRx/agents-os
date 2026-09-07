---
type: known_error
scope: application
created: "2026-07-22"
updated: "2026-07-22"
confidence: low
supersedes: false
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqcli-project-does-not-exist]]"
  - "[[sqcli-databanks-not-found]]"
aliases:
  - Project has unresolved resources en SQX
  - Builder CFX missing Existing portfolio databank
  - Mismatch config.xml vs Build-Task1.xml en EchoForge
confidence: high
source_session: "2026-07-22-symphony-kronos-builder-failures"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/knownerror
  - project/echo-forge
  - project/echoforge
  - scope/application
  - tool/strategyquant
---
# StrategyQuant CLI — Project has unresolved resources en builder

> **⚠️ NOTA — 2026-07-22 ~20:08:** esta nota fue creada durante la sesión de
> fix a Kronos. Una revisión posterior en vivo con wfs encolados reveló
> que la Causa #1 (databank `Existing portfolio` ausente en disco) **NO es
> la diferencia real entre Kronos y Hera/Zeus**. Hera tampoco tiene
> `Project has unresolved` aunque su `Existing portfolio` está vacío. La
> diferencia auténtica es **estado de la workspace persistente de SQX en
> `/home/kor/sqx/user/projects/custom/`** (databanks + caches internos que
> SQX regenera tras runs fallidos).
>
> Mantener esta nota como evidencia de la hipótesis descartada, **no**
> como diagnóstico operacional. Para la nota nueva sobre el cache
> compilado y permisos JAR (que SÍ es válida), ver
> [[sqcli-echoforge-class-not-found-fresh-worker]].

> Error que aborta la fase `01_builder` cuando el `project.cfx` (generado a
> partir de `builder_test.cfx` cargado en MinIO) tiene un mismatch entre
> `config.xml` (declara databanks) y el `Build-Task1.xml` (referencias).

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- En el log SQX del workflow se observa, justo después de cargar databanks:
  ```
  Syncing databank(s) from files
  Loaded 0 strategies to databank Results
  Loaded 0 strategies to databank Last generation
  Loaded 0 strategies to databank Initial population
  Loaded 0 strategies to databank Strategies to improve
  Loaded 0 strategies to databank Strategies to optimize
  Loaded 0 strategies to databank input
  Loaded 0 strategies to databank output
  Synchronization finished.
  ==================================================
  Cannot start project.
  Project has unresolved resources.
  ==================================================
  ```
- El flujo falla en la fase `01_builder`. Sin 0 strategies producidas.
- En el wf `sqx-main-00_configs-v1-NDX-H1-L-1784762810`, el siguiente paso
  (`overview_exporter`) pasó con status `success` pero con 0 datos, y
  `classify_and_rank` abortó con `metadata missing for wave`.

## Causa

- El `builder_test.cfx` versionado en MinIO bajo
  `wave_<W>/<INSTRUMENT>/<DIR>/<TF>/<STRATEGY>/<VERSION>/<CFG_ID>/00_configs/builder_test.cfx`
  es internamente inconsistente:
  - Su `config.xml` declara **7 databanks**: `Results`, `Last generation`,
    `Initial population`, `Strategies to improve`, `Strategies to optimize`,
    `input`, `output`.
  - Su `Build-Task1.xml` (1.24 MB) referencia un **octavo databank**,
    `Existing portfolio`, en la línea
    `<FitPortfolio active="false" databank="Existing portfolio">`.
- SQX, al arrancar el proyecto, parsea `config.xml`, descubre las 7 entries y
  las reconcilia contra los archivos en `~/sqx/user/projects/custom/databanks/`.
- Como `Existing portfolio` **no está declarado**, SQX intenta resolver la
  referencia huérfana de `Build-Task1.xml` y falla con
  `Project has unresolved resources.`

## Por qué Hera / Zeus "pasan" y Kronos no

- En Hera y Zeus la carpeta `~/sqx/user/projects/custom/databanks/Existing portfolio/`
  existe desde hace semanas (`Birth: 2026-06-03` en Hera, `2026-06-18` en Zeus).
  SQX, al sincronizar desde archivos, la encuentra y la añade implícitamente al
  estado del proyecto.
- En Kronos la carpeta es **nueva** (`Birth: 2026-07-22 10:22:46`, creada hoy)
  y además tiene permisos `0755` (vs `0775` en los otros dos workers, cuestión
  de un chmod más permisivo por SQX al sincronizar).
- Resultado: Kronos **resuelve 7 databanks y aborta**, mientras Hera/Zeus
  resuelven 8 (incluida `Existing portfolio`) y arrancan el builder.

## Impacto

- Falla del `01_builder` específica para workers "limpios" (instalaciones
  recién sincronizadas, worker recién provisionado, o un worker donde el
  estado de `custom/databanks/` se haya regenerado).
- En producción, **mientras el `custom/project.cfx` se reescriba desde MinIO
  en cada wf, cualquier worker que no conserve el databank pre-existente en
  disco va a fallar de forma intermitente** dependiendo del estado local.
- Probabilidad ~70% de fallo en builds iniciales de cada wave (kronos,
  workers recién desplegados).

## Detección

- Buscar en `sqx_raw_log` del wf: `Project has unresolved resources` o
  `Cannot start project` combinado con un databank que no se carga
  (`Existing portfolio` por defecto).
- Comparar el `custom/project.cfx` en disco con el de un worker que sí pasó.

## Mitigación (recomendada)

1. **Corregir el `builder_test.cfx` en MinIO** para alinear
   `config.xml` y `Build-Task1.xml`. Hay dos opciones equivalentes:
   - **a)** Agregar a `<Databanks>` del `config.xml`:
     ```xml
     <Databank name="Existing portfolio" view="Default" syncType="Auto-sync never" />
     ```
   - **b)** Quitar o cambiar el atributo `databank="Existing portfolio"` del
     `<FitPortfolio>` en `Build-Task1.xml` (SQX respeta `active="false"`).
   La opción **a** es la más segura porque mantiene la simetría con
   el resto del ecosistema (Hera y Zeus ya tienen este databank).
2. **Workaround de emergencia** (lo aplicado esta sesión en Kronos): poblar
   la carpeta manualmente antes del primer build:
   ```bash
   ssh kor@<worker> 'mkdir -p /home/kor/sqx/user/projects/custom/databanks/Existing\ portfolio && chmod 0775 "$_"'
   ```
   Esto no resuelve el bug del CFX pero permite al worker correr builds
   idénticos a los que corren en Hera/Zeus.

## Verificación

- Tras la mitigación, el log SQX debe mostrar:
  ```
  Loaded 0 strategies to databank Existing portfolio
  ==================================================
  =========== Project started ===========
  Build strategies : Initializing backtest data...
  ```
- Métricas de validación tras la mitigación: `Build finished because databank is full`
  debería aparecer antes del cierre del workflow.

## Evidencia

- Diagnóstico completo:
  [2026-07-22-symphony-kronos-builder-failures-and-fixes](../journal/sessions/2026-07-22-symphony-kronos-builder-failures-and-fixes.md)
- WorkID afectado: `sqx-main-00_configs-v1-NDX-H1-L-1784762810`
- Logs comparativos: `builder_log.txt` (Kronos) vs `hera_builder_log.txt`
  extraídos del `sqx_raw_log` de los eventos `ActivityTaskCompleted` (scheduled
  event ID 5) del wf.
