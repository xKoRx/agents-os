**HISTORICAL_DATA_PARTIAL.** El piloto histórico de PE-005-R1 corrió sobre datos reales y quedó reproducible. No hay `BACKTEST_PASS`, `OOS_PASS` ni `HYPOTHESIS_VALIDATED`.

## 1. Sports Week

Quedó intacta. `sports-week-capture.service` sigue activo desde el 2026-09-21 14:15:20 −03, con el binario pinneado `engine-bfa6eafa57ae17aa92d7e112d41b87cae5b67990`. La campaña está `ARMED`, `started_at` null, modo `NO_GAMES_SCHEDULED`. El health de las 19:31Z seguía en ese estado, con disco libre 17,7 %. No se reinició el servicio, no se cambió el binario y no se escribió su dataset.

## 2. Fuentes

`archive.pmxt.dev` rechazó la conexión. El espejo PendulumFlow de PMXT v2 es CC BY 4.0 y termina el 2026-08-09, antes de la fecha MLB elegida. Gamma responde. `/prices-history` es historia de midpoint, insuficiente para el spread de PE-005. El `base_fee` 1000 del CLOB se consultó hoy: es posterior a la ventana. El dataset de DineshKumar8399 no se descargó: son cotizaciones, no un libro reconstruible, y el dump no cabe en el margen de disco.

PendulumFlow v3 sí cubre el 2026-09-01. Cada hora es el flujo de eventos de esa hora UTC, no un snapshot horario. Trae `book`, `price_change`, `best_bid_ask`, `last_trade_price` y `tick_size_change`. En las dos horas de la cohorte, los cuatro mercados exploratorios tienen cero `tick_size_change`.

## 3. Dataset

Cohorte congelada antes de mirar spreads: moneylines MLB con kickoff 2026-09-01T22:40:00Z, ventana de recepción [21:10Z, 22:40Z). SD 3901945, NYM 3901951, TOR 3901947 y SF 3901949. El kickoff coincide entre MLB statsapi y Gamma `gameStartTime`, ambos leídos el 2026-09-21: autoridad `SCHEDULE_CORROBORATED_POSTHOC`.

Las horas 21 y 22 se leyeron por predicado remoto, sin guardar los parquet (866 MB y 596 MB). El sha256 del publicador quedó en el manifiesto local y no se recalculó sobre el objeto completo. OOS sellado y no analizado: ATL y SEA, kickoff 22:45Z, 18488 líneas, sha256 `740badfbcfacf9c21d13b0ec47518760de188ce6096fb42e49ce21cf8b7e71ee`.

## 4. Engine

Se reutilizaron Capture, regimes, books, replay, screen, shadow y el certificado M4. El paquete nuevo `internal/histimport` admite NDJSON al journal existente y proyecta los regímenes que el archivo trae. No hay un segundo simulador. `engine historical describe` mide el spread con la misma definición de PE-005-R1 y se etiqueta `DESCRIPTIVE_NOT_STRATEGY`.

## 5. SHA y pruebas

Código `56195c945eae59feb8aeefe849d887ed81776494`. Recibo publicado `de33d7d4efbcb085cca46dc8f3e2fbe2b2335d97` en `master` y `main`. M4 no-live recertificado en ese código: 27 PASS, 0 FAIL, 5 live diferidos. `go test ./...` pasó. Race de `histimport` y de `cmd/engine` pasó. Cobertura de `histimport`: 87,8 %. `LIVE_DISABLED` y `REAL_FEE_READY=false` se mantienen. El binario del piloto tiene `vcs.modified=false`.

## 6. Piloto PE-005-R1

Parámetros congelados: `window_ms=300000`, `ref_frames=10`, `widen_min_bps=50`, `entry_budget=25`, `min_net_edge_bps=50`, `taker=true`, `cuts=30`, `fee_unresolved=true`.

| Mercado | Eventos | Tick | Calidad con régimen | Replay `{1}` = `{32,7,1}` | Ensanchamientos | Observaciones | Desajustes de reconstrucción |
|---|---:|---:|---|---|---:|---:|---:|
| SD 3901945 | 15487 | 0 | SYNCING | `67fdba7b…d22da5` | 0 | 15268 | 6 |
| NYM 3901951 | 13204 | 0 | SYNCING | `701d30b0…8f2a3e` | 0 | 12858 | 6 |
| TOR 3901947 | 13027 | 0 | SYNCING | `873d0fb2…db014e3` | 0 | 12854 | 2 |
| SF 3901949 | 9166 | 0 | SYNCING | `048bc960…f1ee6a2` | 0 | 8986 | 2 |

Los cuatro comparten el mismo kickoff: son una franja, no cuatro observaciones independientes. Los 36 controles por partido son la cadencia de 5 minutos por token a lo largo de 90 minutos, porque no hubo ensanchamiento que reiniciara la ventana.

SCREEN con `cuts=30` queda `SCREEN_BLOCKED_INBOX`: el lote supera `MaxInboxDepth` 128. Una grilla etiquetada `EXECUTION_GRID_NOT_FROZEN` (`cuts=400`, solo SD) entregó 400 frames, 0 oportunidades y 0 frames inelegibles. Shadow sobre el binario `56195c9`, mismo mercado: `INCONCLUSIVE`, 920 frames, 0 oportunidades, 0 fills, fee `UNRESOLVED`, digest `fc3927ce0797c5719e45e94322b70dec48e461d180fb1021a1b51c0b826f55a9;records=15420`.

## 7. Capas

La serie descriptiva, al umbral congelado de 50 bps contra la mediana propia, cuenta cero ensanchamientos en los cuatro partidos. La estrategia no emitió señales: Detect exige `OBSERVED_USABLE` y el régimen deja los libros en `SYNCING`. El replay sin fuente de tick los marca `OBSERVED_USABLE`; esa marca no es elegibilidad de screen. La simulación no produjo fills. La economía sigue `ECONOMICS_UNCERTIFIED`: las 256 trades de la ventana traen `fee_rate_bps` `"0"`, y el `base_fee` 1000 es de hoy. No hay alpha medido.

## 8. Límites

El kickoff no es un snapshot point-in-time. El tick de Gamma de hoy no se escribió. `best_bid_ask` se omitió porque no aporta profundidad. Dieciséis desajustes entre snapshot y libro reconstruido quedaron censurados, sin interpolar. El sha256 local del parquet completo no existe. La cohorte es el racimo de las 22:40Z, no los quince partidos del día. La cobertura de `histimport` está bajo el piso de 95 % en ramas de error.

## 9. Las otras cuatro POCs

El mismo adapter sirve cuando el flujo trae el hecho que el gate de cada POC exige. v3 tiene `new_market` y `market_resolved`. No trae, en esta muestra, un snapshot histórico de reglas, un vintage meteorológico ni un `first_known_at` de catálogo. NegRisk, combinatorial, weather y maturation siguen sin un backtest elegible por esa ausencia. No hace falta un motor por POC.

## 10. Decisión

Para un screen histórico con libros `OBSERVED_USABLE` hace falta un hecho de tick que haya existido en la ventana y que no sea el Gamma consultado hoy. Estas dos horas de v3 no lo contienen. Sin esa fuente, el proceso puede seguir describiendo spreads y replaying journals, y la estrategia permanece en `SYNCING`.ss