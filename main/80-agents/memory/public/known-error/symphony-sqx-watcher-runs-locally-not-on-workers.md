---
type: known_error
scope: project
created: 2026-07-29
updated: 2026-07-29
area:
project: "[[Symphony]]"
application: "[[sqx-worker]]"
entities:
  - "[[Symphony]]"
  - "[[sqx-worker]]"
  - "[[sqx-watcher]]"
  - "[[symphony-stager]]"
related:
  - "[[sqx-deployer]]"
aliases:
  - sqx-watcher local vs remote
  - confundir watcher con stager
  - watcher no va en workers
confidence: high
source_session: "[[2026-07-29-deploy-0.2.6-flow-44]]"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - project/symphony
  - application/sqx-worker
  - scope/project
---

# sqx-watcher corre SOLO en local, NO en los workers remotos

## Síntoma

- En un despliegue de SQX Worker, un agente afirma que un subconjunto de workers
  remotos (Zeus/Hera/Kronos) corre `sqx-watcher` mientras los otros no, y que
  eso es "correcto por diseño".
- El usuario responde: "el watcher se corre en local en el mismo proyecto
  symphony".
- Se confunde el rol del `sqx-watcher` (input feeder) con el rol del
  `symphony-stager` (auto-updater desde MinIO).

## Causa

- El `sqx-watcher` vigila `./input/` para despachar workflows a Temporal.
- Por diseño corre en la **máquina de desarrollo local** (donde se editan
  configs), NO en los workers remotos.
- El `symphony-stager` (systemd timer en cada worker) es el único proceso que
  sí debe correr en los 3 workers — descarga binarios desde MinIO cuando el
  `manifest.json` cambia.
- El agente vio un proceso `sqx-watcher` corriendo en Zeus (probablemente
  heredado de un setup previo) e inventó la justificación de que "Zeus es el
  primario y los otros son secundarios", en vez de leer la skill
  `sqx-watcher` que ya tenía cargada y que dice explícitamente: *"Levantar el
  watcher en segundo plano utilizando una sesión de `screen` llamada `watcher`
  y vigilando la carpeta `./input`"*.

## Impacto

- Información arquitectural incorrecta entregada al usuario.
- Si el agente hubiera decidido instalar el watcher en Hera/Kronos por su
  cuenta, habría duplicado inputs: el mismo `config.json` se procesaría 3
  veces y se despacharían 3 workflows idénticos a Temporal.

## Detección

- Antes de afirmar asimetrías entre workers, **leer la skill oficial** del
  binario/servicio en cuestión.
- Si la skill dice "local", es local. No reinterpretar como "remoto por
  extensión".
- Distinguir claramente:
  - **Local (developer machine):** `sqx-watcher`, `deployer-watcher`,
    `deploy_sqx.sh`, edición de configs en `input/`.
  - **Remoto (workers Zeus/Hera/Kronos):** `symphony-worker`,
    `symphony-stager`, agentes que ejecutan actividades de Temporal.

## Mitigación

- Cuando el inventario de procesos muestre un proceso extra en uno de los
  nodos, tratarlo como **anomalía a explicar**, no como "diseño".
- Si el watcher aparece corriendo en un worker remoto, es residuo de un
  setup anterior — NO propagarlo a los otros workers.
- Verificar siempre con la skill antes de tocar systemd units en workers.

## Evidencia

- Sesión 2026-07-29: deploy de SQX Worker 0.2.6 y ejecución de flujo
  `example_flow_44`. El agente copió `config.json` y `.cfx` a
  `/var/lib/symphony/input/` en Zeus por SSH porque vio el watcher ahí,
  sin cuestionar si esa era la topología correcta.
- El usuario corrigió: "ctm esa wea debería correr solo en local".
- Verificación posterior:
  - Zeus (192.168.31.101): `symphony-watcher.service` enabled, proceso
    corriendo (PID 2633008, en `/var/lib/symphony/input`).
  - Hera (192.168.31.111): unit `not-found`, proceso ausente.
  - Kronos (192.168.31.121): unit `not-found`, proceso ausente.
  - Los 3 tienen `symphony-stager.service` (eso sí es correcto).
