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

Actualizado 2026-10-19 tarde (RESUME-01): las dos acciones Owner originales YA FUERON EJECUTADAS y verificadas por canales del agente (feed vivo real; AddOn instalado y NT reiniciado). Quedan UN bloqueo del Manager (defecto P1 del release, abajo) y UNA única acción Owner puntual para C3 (el JSON de configuración del AddOn). Ninguna acción pendiente arma ejecución: la sesión SIM se arma aparte, con el submanager, después.

## Estado de las acciones originales (2026-10-19 RESUME-01)

- **Acción 1 (reconectar «Simulación»): HECHA y verificada** — frames NQ 12-26 QUOTE/TRADE frescos llegan a Kafka (~90–234 msg/s, event_ts <2 min). El primer dato vivo reveló el **defecto P1 del release** (typename de market_stream rechazado por StateFun → crash-loop del job); el submanager ejecutó el rollback documentado del module (FX-only, estable). **El pipeline futures NO enruta market data hasta que el Manager corrija el typename y re-despliegue el module** (`module.yaml.certnt01` preservado en dev .75). Esta corrección es del Manager, NO del Owner.
- **Acción 2 (cargar AddOn de ejecución): HECHA por el Owner** — NT reiniciado (PID 8556), el Custom assembly está vivo tras el restart (el AddOn de feed sigue publicando) y el Owner reporta compilación exitosa tras resolver los duplicados. Matiz técnico (UNKNOWN V8): desde los canales del agente NO es demostrable QUÉ versión quedó instalada (NT conserva el último ensamblado bueno si la compilación fallara); si el Owner quiere cerrarlo, basta ejecutar UNA vez en su sesión: `Get-FileHash "C:\Users\KoR\Documents\NinjaTrader 8\bin\Custom\AddOns\**\EchoExecutionAddOn.cs"` y compartir el/los hash(es) con el submanager (esperado `a93a6a1e…` del release, una sola copia).

## Única acción Owner pendiente para C3 — JSON de configuración del AddOn

El archivo `echo-execution-addon.json` **nunca fue entregado** (el staging `C:\Users\TEMP\certnt01` ya no existe). Sin ese archivo el AddOn de ejecución queda fail-closed con sus lanes caídas (estado SEGURO actual: cero capacidad de orden). El submanager preparará el JSON (con token real y binding `Sim101 → 192.168.31.161:9771`) al momento de armar la sesión SIM, y en ese momento pedirá al Owner la copia puntual a `C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json` + un reinicio de NT. NO entregar ni copiar JSONs con tokens por canales no acordados.

## Qué queda PROHIBIDO para cualquiera (vigente)

- Habilitar `futures-bridge/accounts` (clave de armado), iniciar `futures-bridge`, o poner `enabled=true` en la asociación `certnt01-a1` sin un despacho explícito del Manager (eso ES armar ejecución).
- Ejecutar/cancelar órdenes en cuentas RJARA\*/E2T del Owner. SIM autorizada para esta certificación: **Sim101** exclusivamente.
- Mergear `feature/ef-runtime-pools` a master o tocar Echo PROD.

## Reanudación de la certificación

Orden de desbloqueo: (1) Manager corrige el typename de `market_stream` (+ test de gramática de typename) y re-despliega el module verbatim; (2) submanager arma la sesión SIM: token + binding + `futures-bridge/accounts` SOLO con la cuenta de certificación, entrega del JSON al Owner, verificación de binding Sim101; (3) smoke del gateway y recorrido Strategy→MM→NT/SIM (C3); (4) rotación/recuperación/economía (C4, con `MULTIACCOUNT_NT_NOT_EXECUTED` si no hay más cuentas NT SIM autorizadas); (5) verificación independiente (C5) y estado final seguro (ejecución automática deshabilitada).
