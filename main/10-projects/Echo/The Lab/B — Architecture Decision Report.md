---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[D — Revised Roadmap]]"
  - "[[F — Decision Register]]"
tags: [kind/doc, area/echo]
created: "2026-09-22"
updated: "2026-09-22"
---
# B — Architecture Decision Report — V3 simplified

**Decisión de arquitectura objetivo propuesta por TL el 22-09-2026; owner ratificó el modelo conceptual simple y la eliminación de deuda legacy, NO un DDL concreto.** Reemplaza recomendaciones de este documento anteriores que trataban HistoryRevision, HistoryPublication y TradeSet como tres entidades obligatorias adicionales. Documentación de evidencia, no certificación: [[C — Reality and Gap Matrix]].

## Grafo de autoridad
```
Forge SQX originals + Forge MT5 originals       Echo trade_journal (operacional, intocable)
                  \                                 /
              adapters de frontera, validación, idempotencia
                                  |
                           lab_operations
                      UNA base canónica activa
                                  |
                     CurveAlgorithm en Go (N)
                                  |
                 lab_curves + puntos + métricas
                                  |
               dashboard / calendar / screener
                                  |
            políticas monetarias / portfolio research
                                  |
             portfolio apply autorizado en Echo
```

## Modelo mínimo, no abstraer por anticipación
1. Configuración Lab por StrategyVersion: fechas A/B, timezone y pruebas, estado. Puede alojarse en tabla mínima o metadata existing si sus invariantes lo permiten. Fecha A desde dataset Forge, B opcional hasta puesta en marcha. No crear una entidad histórica genérica sólo para almacenar dos cortes.
2. `lab_operations`: una operación por identidad económica estable dentro de fuente y versión; llave/source ID, StrategyVersion, open/close event con provenance, instrumento y espec, señal entrada/SL/TP, economics y costos, riesgo y valores ausentes, import/batch/original digest. Período se resuelve por apertura; columna materializada si útil sólo como proyección de A/B versionada/reconstruible. PG authority activa.
3. `lab_curves` con resultado de ejecución algorítmica identificado por StrategyVersion, fingerprint de operaciones+límites, algorithm id/version/config/basis, status, generación y fecha; `lab_curve_points` como tabla física subordinada o payload según tamaño/consulta; `MetricSet` semánticamente explícito asociado. NO crear un modelo alternativo de trades por cada curva.
4. `lab_job_runs` existente y checkpoint operacional del worker son infraestructura, no nuevas entidades de dominio. Screener y calendario son queries/proyecciones sobre operaciones/curvas, no write masters.

### Relación con S0/E05 — decisión explícita anti-doble autoridad
El SDK S0 `NormalizedOperationV1` puede servir como DTO/validador; E05 calculator, identity/digests y parte del writer se reutilizan sólo si sirven a la autoridad única. La persistencia `canonical_trade_sets` PG063 es write-once y hoy actúa como autoridad E05: NO introducir `lab_operations` paralelas y declarar ambas canonical sin migrar contratos. La SPEC del miércoles debe escoger y ejecutar convergencia: nuevo `lab_operations` = autoridad analítica Lab; E05 cambia su entrada/calculator/writer por adaptación versionada; los TradeSets históricos de E05 se consideran fuente legada transitoria/contrato wire si siguen siendo necesarios para E10. Confirmar consumidores E10 y fuentes antes de eliminar 063; NO perpetuar dual-write o tener dos maestros en PROD. Si un contrato frozen requiere TradeSet wire, puede construirse desde operaciones con procedencia declarada, no persistirse como segundo write master activo. No borrar datos que sean la única copia verificable del input actual; migrar o conservar fuente original hasta demostrar reconstrucción. Decisión final de estructuras a concretar en SPEC diaria, no reescritura ciega.

### Ingestión Forge y reemplazo histórico
Handoff F04/E04 existente se extiende para dos listas por trade: SQX TRAINING y MT5 PRE_REAL, IDs/StrategyVersion/rangos/zonas/specs/format/parser/hash/report sums. Verificar un candidato verdadero; un HTM agregado no equivale a trade list. Forge entrega solamente base original, Echo normaliza y calcula. Intake E04 sigue único, receipt operativo != historia analítica lista. Import/reimport idempotente por fuente/digest; si owner reemplaza dataset, staging validado y transacción corta swap/cambio de conjunto visible+marca de curvas dirty; lectores no ven media importación, job nunca borra journal. Sin historial perpetuo de revisions, conservar archivos originales, manifiesto y trazabilidad mínima del último import y job; el efecto de sustitución se registra sin duplicar datasets obsoletos.

### REAL y funcionamiento de job
Lab-worker actual (`v3/lab-worker`) contiene CLI, DI/telemetría, `lab_job_runs`, recompute journal→lab_canonical_trades→outcomes, materialize-curves y materialize-snapshots. Import histórico aún stub. Recompute legacy destruye resultados por scope, usa recorded times y R AUTO; no reutilizar esa lógica como V3. `canonical_a0.go` etiqueta un set Reference derivado de Lab como BACKTEST/SQX/FULL: no usar ese mapping para realidad de Echo. Reutilizar sólo scheduler/timer, binario, observabilidad, job-run scaffold y funciones corretas demostradas; escribir un pipeline V3 `READ journal → map StrategyVersion+Reference → upsert/swap lab_operations → recalc dirty curves/metrics`, checkpoint sobre tiempo de modificación/ingesta e ID de desempate más reconciliación periódica acotada para backfills; manejar deletes/correcciones cuando journal registre evento versionado. Source de journal READ ONLY. No asumir que timer productivo está sano por existir; última auditoría Sep21 documentó silencio 66h, Sep22 documentó reanudación: verificar salud/freshness en DEV antes del gate del sábado.

### Algoritmos extensibles y escala KISS
Interfaz Go in-process pequeña `CurveAlgorithm { Describe/Validate/Calculate }`, registro por id/versión/config tipada; output puntos+contribuciones y metadatos de inputs. R_PIPS/R_MONEY y otras bases se seleccionan explícitamente; no bloquear arquitectura definiendo todas las fórmulas ahora. No DSL, plugins remotos, Kafka/Temporal extra ni otro servicio. Misma estrategia y nuevo config produce nueva curva reproducible; cambio dataset invalida curvas de esa estrategia. Recompute completo del sujeto afectado V3 es aceptable inicialmente, incremental se agrega después sólo ante benchmark. PG con índices por StrategyVersion/open-time/source ID y curve/run/point; no Mongo analytics duplicado, no partición anticipada. Persistir suficientes fingerprints de inputs para detectar stale, evitar recompute en cada render; batch y transacciones cortas. Calidad de estrategia no equivale a PnL real de cuenta. Sin velas no simular stop/TP alternativo ni fill contrafactual.

### Limpieza agresiva sin daño colateral
V1/V2 son producto descartable: no exigir paridad, no mantener front/rutas/cálculos antiguos. Trabajo explícito L-CLEAN: localizar tablas, vistas, workers, SQL, schemas, SDK packages, front, Hasura, timers, dependencias/rutas de imports; clasificar cada objeto `LAB_ONLY_REMOVE`, `SHARED_PRESERVE`, `REPLACE_AFTER_CONSUMER`, `UNKNOWN_BLOCK_DELETE`. Elegir DROP/delete cuando la nueva V3 pasa gates y los consumidores ya no referencian el objeto. No tocar `trade_journal`, operaciones broker, cuentas, posiciones, core/gateway operativo, seguridad, snapshots necesarios para trading; backup/export previo de tablas que contengan la única copia histórica. Migraciones forward-only reproducibles, DEV primero, PROD sólo autorización. No preservar legacy por compatibilidad, sí preservar datos y ejecución de Echo ajenos a Lab. Limpiar deuda demostrada AHORA al diseñar; ejecutar remoción final después de dashboard sin postergarla indefinidamente.

### Trazabilidad y autoridad
Fechas clasifican por apertura y resultados se grafican por cierre; crossing visible, sin dividir PnL. Una sola historia oficial derivada de dataset actual, no HistoryRevision/Publication. Contratos E04/S0 frozen pueden reabrirse acotadamente por defecto demostrable. E06/E07 Reference facts y E09 execution analysis no se mezclan como performance de estrategia. E10 no bloquea UI ni journal ingestion. `SOURCE_VERIFIED`, `DEV_E2E`, `PROD_DEPLOYED` son gates distintos. El miércoles concreta DDL y owner de migraciones/paths; documentos previos A–F del 22-09 fueron corregidos por esta ratificación posterior.
