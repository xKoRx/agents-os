---
type: decision
schema_version: 1
scope: application
created: 2026-07-31
updated: 2026-07-31
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[CleanProjectDatabanks]]"
  - "[[GetSQXPaths]]"
related:
  - "[[2026-07-31-temporal-activity-contract-remote-only]]"
  - "[[2026-07-31-storage-path-deterministic-by-logical-identity]]"
  - "[[2026-08-14-echo-forge-one-vm-one-worker-one-task]]"
aliases:
  - databanks-input-output-only
  - task-local-dir-contract
confidence: verified
source_session: cursor-2026-07-31-trade-list-remote-contract-design
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - tech/sqx
  - priority/high
---

# Decision: el disco local de una task son `databanks/input` y `databanks/output`

## Contexto

Cada task del pipeline EchoForge que ejecuta `sqcli` necesita disco local:
el motor SQX y sus plugins Java leen de un databank de entrada y escriben
artefactos de salida. Ese disco es **compartido entre tasks**: los 5
proyectos EchoForge viven bajo `user/projects/<project>/` y se reutilizan
wave tras wave.

El trade list exporter había introducido un tercer directorio
(`user/projects/<project>/tradelist`), hermano de `databanks/`, imitando
la convención de `overview/`. Consecuencias observadas:

- Nadie lo limpiaba. `runtime.CleanProjectDatabanks` cubre
  `databanks/input`, `databanks/output` y `overview`, pero no un
  directorio arbitrario. Los artefactos de corridas viejas se acumulaban.
- El descubrimiento de artefactos (`_SUCCESS` walk) podía encontrar
  residuos de una wave anterior y publicarlos como si fueran de la actual.
- Nacieron **dos** convenciones de ruta para lo mismo: el step legacy
  `collect_trade_list` leía `databanks/output/tradelist` mientras la
  activity escribía en `<project>/tradelist`. Nunca se encontraban.

## Decisión

**El contrato local de una task es: leo de `databanks/input`, escribo en
`databanks/output`, y limpio ambos antes y después de usarlos.**

1. El directorio de salida del exporter es `databanks/output`
   (`runtime.GetSQXPaths`). No se crean directorios hermanos nuevos.
2. La activity llama `runtime.CleanProjectDatabanks` **al empezar**
   (garantía de no heredar contaminación) y **al terminar con éxito**
   (higiene). Ante fallo **no** limpia: los archivos quedan para RCA y la
   siguiente ejecución los borra.
3. Todo directorio local que un exporter escriba debe estar cubierto por
   la primitiva de limpieza. `overview/` lo está y por eso Overview y WFM
   siguen siendo válidos; cualquier ruta nueva fuera de esa cobertura no.
4. Los nombres de archivo **dentro** de `databanks/output` los decide el
   plugin y no son contrato con nadie: ese directorio es efímero. El
   nombre canónico se aplica al publicar en storage remoto.
5. Una sola fuente de verdad para la base path: el worker fija
   `runtime.SetSQXExecBasePath(filepath.Dir(cfg.SQCLIBinaryPath))` al
   arrancar. Antes, `runtime.*` usaba el default `/home/kor/sqx` mientras
   las activities derivaban de ETCD; coincidían por convención, y una
   activity que **borra** directorios no puede depender de eso.

## Alternativas descartadas

1. **Mantener el tercer directorio y no limpiarlo** (statu quo): es la
   fuente de contaminación entre tasks que motivó la decisión.
2. **Mantenerlo y ampliar `CleanProjectDatabanks` para cubrirlo**:
   resuelve la limpieza pero deja dos rutas para lo mismo y obliga a
   registrar cada directorio nuevo en la primitiva. Más superficie, cero
   beneficio.
3. **Limpiar con locks o mutex por proyecto**: innecesario por la invariante
   vinculante [[2026-08-14-echo-forge-one-vm-one-worker-one-task]]. El worker
   corre con `MaxConcurrentActivityExecutionSize: 1`, así que las activities
   se serializan por host aunque el workflow lance N estrategias en paralelo.

## Consecuencias

- Un `tradelist/` remanente en los workers desplegados queda huérfano:
  borrarlo a mano una vez tras el despliegue.
- El walk de descubrimiento pasa a tener como root `databanks/output`; el
  guard `if info.Name() == "output" && path != root → SkipDir` sigue
  siendo válido y protege de un `output/` anidado que cree SQX.
- Los tests que ejercitan estos paths **deben** redirigir la base con
  `SetSQXExecBasePath(t.TempDir())` y restaurarla con `defer`: la limpieza
  borra archivos de verdad.

## Trazabilidad

- Proyecto de implementación: [[Echo Forge - Trade List Export Contrato Remoto]] (D10, tareas T2c/T3).
- Gap: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.9 (EF-G32).
