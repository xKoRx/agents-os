# Clasificación de fallos wave3q/r/s (21 children mt5_backtest por wave)
- 20/21 por wave: `mt5 artifact backtest: journal contract: mt5 logs: journal tester sin delta de la ejecución` — NO_RETRIABLE — INFRA-1 (terminal MT5 single-live; ver MD).
- 1/21 por wave: SUCCESS → reconcile StructuralIdentityMatch → baseline materialize → score COMPUTED.
- wave3s además: 95 min de los compile children pendientes porque el worker MT5 quedó colgado con mt5/slot_count=1 (segundo defecto de producto, revertido a 4). Worker sano verificado tras rollback.
- Journals MT5 del éxito (wave3s, f8719ecf): durable/mt5-export/v1/cd697133-.../07_mt5_backtest/ (terminal.log, tester.log, agent.log en MinIO; htm + tradeset + tester.ini en el mismo prefijo).
