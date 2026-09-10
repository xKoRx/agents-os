---
type: known_error
scope: project
created: 2026-07-28
updated: 2026-08-06
area: "[[Echo Forge]]"
project: "[[Echo Forge - Trade List Export Contrato Remoto]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
  - "[[sqx-temporal-failure-audit]]"
aliases:
  - echo-forge-snippets-stale-jar
  - sqx-runtime-recompile-shadows-jar
  - tradelist-java-snippets-stale
confidence: verified
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/known-error
  - area/echoforge
  - tech/sqx
  - tech/echo-forge
  - scope/public
---

# Echo Forge trade_list — bug latente descubierto en `user/extend/Snippets/`

**Fecha:** 2026-07-28
**Sesión:** fix TradeExtractionService reordered.isEmpty() y deploy plugin 0.2.5
**Severidad:** bloqueante — el fix Java no llegó a ejecutarse aunque estaba "desplegado"

## Síntoma

Después de:
1. Compilar `EchoForgeAutomator.jar` con el fix `reordered.isEmpty()` en `TradeExtractionService.java`.
2. Copiar el `.jar` a `/home/kor/sqx/user/libs/` en Zeus/Hera/Kronos.
3. Redesplegar `example_flow_41`.

El plugin Java **volvió a fallar** con el mismo `IndexOutOfBoundsException` en `TradeExtractionService.java:181`, exactamente el bug que el `.jar` ya tenía parcheado.

```
ERROR NDX_L_H1_example_flow_41_v1_Strategy_5.1.22.k0_robust:
  IndexOutOfBoundsException - Index 0 out of bounds for length 0
  at SQ.CustomAnalysis.trades.TradeExtractionService.extract(TradeExtractionService.java:181)
```

## Causa raíz

**SQX NO carga el plugin desde `user/libs/EchoForgeAutomator.jar`.** Hay un **segundo classpath de fuentes Java sin compilar** en:

```
/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/
  ├── EchoForgeTradeListExporter.java
  └── trades/
      ├── TradeExtractionService.java
      ├── TradeListArtifactWriter.java
      ├── ProductionSQXTradeSource.java
      └── ... (17 archivos en total)
```

StrategyQuant escanea `user/extend/Snippets/` y **compila en runtime esos `.java` para construir el plugin en memoria**. Los fuentes de `Snippets/` no se actualizaron junto con el `.jar`. En `Snippets/`, la línea 181 de `TradeExtractionService.java` sigue siendo:

```java
Instant periodStart = reordered.get(0).entryTimeUtc();
```

(es decir, el `get(0)` original sin el `reordered.isEmpty()` check). SQX recompiló ese fuente, no el del `.jar` y la excepción reapareció aunque el `.jar` ya tenía el fix.

## Falsos positivos generados

Al decompilar el `.class` que **sí** se ejecutó (proveniente de `Snippets/`), el `LineNumberTable` referenciaba líneas 180/181 que coincidían con el `throw new TradeExtractionException(Code.CONTRACT, ...)` del fuente actual. Eso llevó a creer inicialmente que el `.jar` "nuevo" aún no estaba cargado, cuando en realidad ni siquiera era ese `.class` el que corría. El byteoffset 690 en el .class correspondía a `new TradeExtractionException`, no a `get(0)`, pero el stack trace decía `IndexOutOfBoundsException` en `TradeExtractionService.java:181` porque esa línea del FUENTE de Snippets (el cargado realmente) sí es el `get(0)`.

## Lección operativa

- **Nunca** confiar en que desplegar el `.jar` en `user/libs/` alcanza. Si `user/extend/Snippets/` contiene fuentes Java, SQX recompilará en runtime desde allí y el `.jar` queda como espejismo.
- Cualquier fix al plugin Java debe replicarse en **ambas** rutas antes de reejecutar el flow.
- La causa raíz solo se hizo evidente al inspeccionar el **fuente** que SQX estaba usando para recompilar (`user/extend/Snippets/SQ/CustomAnalysis/trades/TradeExtractionService.java`), no el `.class` del `.jar`.
- `classpath` tiene **dos entradas** con la misma lógica de carga; ambas deben mantenerse sincronizadas.

## Fix aplicado

Sincronizar vía `rsync --delete` desde el repo local a `user/extend/Snippets/` y recompilar el `.jar` para mantener ambos paths consistentes. Confirmado en los 3 workers:

```
SHA source:  faa829681f098604496d4aa5108c9d9473a707b981025ef5fe59d9c37b3ac640
             /home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/trades/TradeExtractionService.java

SHA jar:     6e2a8223102c7187bcb2b67e4c02aaafd2986989046e77c42b26a3f8374dd9ea
             /home/kor/sqx/user/libs/EchoForgeAutomator.jar
```

Workflow `sqx-main-00_configs-v1-NDX-H1-L-1785288415` cancelado. Listo para reejecutar `example_flow_41` cuando se relance.
