---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
aliases:
  - CERT-NT-01 owner checklist
tags:
  - kind/doc
  - area/echo
created: "2026-10-19"
updated: "2026-10-19"
---

# OWNER CHECKLIST — CERT-NT-01 (desbloqueo de gates C2/C3/C4)

Estado de la certificación al 2026-10-19: release `feature/ef-runtime-pools@b13ef43d` desplegado y probado en el entorno canónico DEV (ledger «Certificación operativa CERT-NT-01» del planner). Quedan bloqueadas las fronteras físicas de NinjaTrader por dos dependencias que sólo el Owner puede ejecutar (ACL del terminal y market data de NT). Ninguna de las dos acciones arma ejecución: la sesión SIM se arma aparte, con el submanager, después.

## Acción 1 — Reconectar market data de NinjaTrader (desbloquea C2 completo)

Síntoma verificado: el AddOn de feed reporta `market_events` congelado (15.451.883) desde ≤10:00Z; heartbeats y eventos de cuenta/órdenes sí fluyen. Es el mismo modo de fallo certificado en D6: la conexión **"Simulación"** de NT no se resuscribió tras el cierre de fin de semana y NT no reconecta solo.

1. En NinjaTrader (dev-win .132, sesión `KoR`): Control Center → Connections → reconectar **"Simulación"** (o botón derecho sobre la conexión → Connect).
2. Confirmar datos de **NQ 12-26** vivos (ventana de mercado cotizando).
3. Señal observable sin tocar nada más: en ~1 minuto, `journalctl --user -u echo-nt-feed-relay -f | grep market_events` (en Daedalus) vuelve a avanzar, y el offset de `echo.futures.market-feed-candidates.v1` (grupo `echo-statefun-futures-market-feed`) avanza con datos frescos. Con eso, el pipeline desplegado (feed → barras → analytics → Strategy) entra en observación con datos utilizables por sí solo; no se requiere ninguna otra acción del Owner.

## Acción 2 — Cargar el AddOn de ejecución (desbloquea C3-ready)

El release trae `EchoExecutionAddOn.cs` (multi-binding, ya compilado sin errores contra las assemblies reales de NT 8.1.8.3; evidencia en el ledger). El sandbox del agente NO puede escribir en `C:\Users\KoR\Documents` (verificado `WRITE_DENIED`), por lo que la copia y el reinicio de NT son del Owner.

1. Verificar antes de reiniciar NT (terminal compartido): sin posiciones ni órdenes activas del Owner en las cuentas RJARA del terminal. El reinicio de NT no toca los bridges MT4/MT5 (procesos separados) y el relay de feed tolera la reconexión (~segundos).
2. Copiar `C:\Users\TEMP\certnt01\EchoExecutionAddOn.cs` → `C:\Users\KoR\Documents\NinjaTrader 8\bin\Custom\AddOns\EchoExecution\EchoExecutionAddOn.cs` (crear la carpeta `EchoExecution`).
3. (Opcional ahora, obligatorio antes de armar SIM) Copiar también `C:\Users\TEMP\certnt01\echo-execution-addon.json` → `C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json`. El archivo entregado por el submanager llevará el token real y el binding SIM (`Sim101` → lane `192.168.31.161:9771`). Mientras no exista el puente escuchando, el AddOn queda con sus lanes caídas y sin efecto (sólo reintentos en log).
4. Reiniciar NinjaTrader. NT compila el `Custom` folder al arrancar e instancia el AddOn (sin ventana ni interacción). Si algo fallara al compilar, NT arranca igual y lo reporta en su log — avisar al submanager con ese log.

## Qué queda PROHIBIDO para cualquiera (vigente)

- Habilitar `futures-bridge/accounts` (clave de armado), iniciar `futures-bridge`, o poner `enabled=true` en la asociación `certnt01-a1` sin un despacho explícito del Manager (eso ES armar ejecución).
- Ejecutar/cancelar órdenes en cuentas RJARA\*/E2T del Owner. SIM autorizada para esta certificación: **Sim101** exclusivamente.
- Mergear `feature/ef-runtime-pools` a master o tocar Echo PROD.

## Reanudación de la certificación

Con las dos acciones hechas, el submanager retoma el mandato CERT-NT-01: verifica feed vivo → completa C2 (barras/indicadores/señales naturales) → arma la sesión SIM con el puente (token + binding + `futures-bridge/accounts` apuntando SOLO a la cuenta de certificación) → smoke del gateway y recorrido Strategy→MM→NT/SIM (C3) → rotación/recuperación/economía (C4) → verificación independiente (C5) → estado final seguro (ejecución automática deshabilitada).
