---
type: decision
scope: application
created: 2026-07-31
updated: 2026-07-31
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[BuildMinIOPath]]"
related:
  - "[[2026-07-31-minio-storage-path-must-be-deterministic-by-logical-identity]]"
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
aliases:
  - buildminiopath-rollback-flat-path
  - ef-g27-decision
confidence: verified
source_session: cursor-2026-07-31-trade-list-path-rollback
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - tech/minio
  - priority/high
---

# Decision: `BuildMinIOPath` plano, sin segmento de ejecución

## Contexto

El cierre de Etapa 4 de Echo Forge quedó bloqueado por un bug que mutó
a lo largo de 5+ releases (0.2.x). Cada parche atacaba un síntoma
downstream (plugin Java, discovery de `_SUCCESS`, naming de NDJSON) sin
tocar la causa generadora: `BuildMinIOPath` inyectaba un segmento
`requestID` que se resolvía de forma distinta según el productor.

## Decisión

**Rollback a la convención plana**. `BuildMinIOPath` deja de aceptar
`ctx` y `requestID`; el path es función pura de la identidad lógica del
contenido:

```
wave_<wave>/<instrument>/<dir_tf>/<strategy>/<version>/[folder]/[filename]
```

El `cfgID` (cuando existe) se conserva **sólo** como identificador de BD
(Registry), nunca como segmento de path de storage.

## Alternativas descartadas

1. **Unificar la resolución de `requestID`** (que watcher y worker
   generen el mismo ID): rechazada. Requiere propagar cfgID por todo el
   flujo Temporal, fragiliza con cualquier producto nuevo y es una
   Lösung-symptom, no raíz.
2. **Mantener `requestID` pero determinístico**: equivalente a quitarlo
   con más pasos. No aporta nada; al contrario, deja un parámetro muerto
   que confunde.

## Consecuencias

- Productor y consumidor siempre coinciden en el path. Se elimina toda
  la clase de bugs "path mismatch" entre etapas.
- Las carpetas huérfanas previas (con cfgID/RunID) quedan como residuo
  en el bucket; se purgan en una pasada de mantenimiento.
- `canonical_strategy_id.go` se mantiene intacto: normaliza filenames
  entrantes, no construye paths.
- Contrato con el Registry (BD) no cambia — `cfgID` sigue ahí.

## Extensión (2026-07-31, noche): el trade list se alinea

Al auditar `EF-G32` se encontró que el trade list **nunca** se alineó con
esta decisión: `remoteArtifactKey`
(`sqx/adapters/storage-minio/trade_lists.go`) y su gemelo muerto
`TradeArtifactKeyBuilderImpl` (`sqx/core/capabilities/trade_keys.go`)
construían su propia key con segmentos de ejecución:

```
waves/wave_<w>/requests/<request_id>/runs/<run_id>/strategies/<sid>/stages/<st>/variants/<v>/results/<rk>/cells/<c>/samples/<s>/trades.v1.ndjson.gz
```

Es exactamente el patrón que esta decisión eliminó, con el agravante de
que cada reintento de Temporal (nuevo `run_id`) estrenaba una key y
dejaba el objeto anterior huérfano.

**Se corrige** publicando el artefacto por el mecanismo único, en la
carpeta que declara el campo `folder` de la task y con el nombre de la
estrategia, igual que todas las demás etapas del pipeline:

```
wave_<w>/<instrument>/<dir_tf>/<strategy>/<version>/<folder>/<canonical_strategy_id>.trades.ndjson.gz
wave_<w>/<instrument>/<dir_tf>/<strategy>/<version>/<folder>/<canonical_strategy_id>.trades.manifest.json
```

Corolarios que se elevan a regla:

1. **Un adapter no construye rutas.** La key la calcula el caller, que es
   quien conoce la identidad lógica de la configuración; el adapter mueve
   bytes y garantiza idempotencia. Dos copias divergentes de
   `BuildMinIOPath` nacieron justamente por invertir esa
   responsabilidad.
2. **La etapa se distingue por carpeta; la estrategia, por filename.** La
   versión de schema va en el manifest y en la metadata del objeto, no en
   el nombre del archivo.
3. **Nada de marcadores `_SUCCESS` por carpeta** cuando la carpeta
   contiene N estrategias: un marcador compartido no puede afirmar nada
   sobre una estrategia en particular. La completitud se registra por
   scope en Mongo.
4. Los sufijos de desambiguación (muestra `IS`/`OOS`, celda WFM) van en el
   **filename**, no en segmentos de path nuevos.

## Trazabilidad

- Fix en código: 10 call sites en módulo `sqx`, commit pendiente.
- Documentación: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.3 (EF-G27) y §10.9 (EF-G32).
- Extensión del trade list: [[Echo Forge - Trade List Export Contrato Remoto]] (D4, D12, D13).
- Learning asociado: [[2026-07-31-minio-storage-path-must-be-deterministic-by-logical-identity]].
