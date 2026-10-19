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

Actualizado 2026-10-19 noche (RESUME-02): el AddOn de ejecución está **cargado y activo** (demostrado por comportamiento: dial continuo hacia `192.168.31.161:9771`, PID 8556) y **el JSON de configuración YA EXISTE en el perfil KoR** (corrección de RESUME-01, ver sección JSON abajo). Quedan: UN bloqueo del Manager (defecto P1 del release), UNA confirmación Owner del CONTENIDO del JSON antes del armado, y la reconexión recurrente del feed («Simulación» volvió a caer ~21:00Z, segunda vez hoy). Ninguna acción pendiente arma ejecución: la sesión SIM se arma aparte, con el submanager, después.

## Estado de las acciones originales (2026-10-19 RESUME-01)

- **Acción 1 (reconectar «Simulación»): HECHA dos veces y VOLVIÓ A CAER** — frames NQ 12-26 QUOTE/TRADE frescos llegaron a Kafka tras la reconexión (18:53–21:00Z); a las **21:00:00Z el feed volvió a detenerse** (HWM congelado verificado en tres muestras 21:33–21:40Z) — mismo patrón D6 («Simulación» sin auto-reconexión). La reconexión GUI del Owner es una acción RECURRENTE: re-verificar frescura del feed justo antes de cada ventana de certificación. El primer dato vivo reveló el **defecto P1 del release** (typename de market_stream rechazado por StateFun → crash-loop del job); el submanager ejecutó el rollback documentado del module (FX-only, estable). **El pipeline futures NO enruta market data hasta que el Manager corrija el typename y re-despliegue el module** (`module.yaml.certnt01` preservado en dev .75). Esta corrección es del Manager, NO del Owner.
- **Acción 2 (cargar AddOn de ejecución): HECHA por el Owner** — NT reiniciado (PID 8556), el Custom assembly está vivo tras el restart (el AddOn de feed sigue publicando) y el Owner reporta compilación exitosa tras resolver los duplicados. Matiz técnico (UNKNOWN V8): desde los canales del agente NO es demostrable QUÉ versión quedó instalada (NT conserva el último ensamblado bueno si la compilación fallara); si el Owner quiere cerrarlo, basta ejecutar UNA vez en su sesión: `Get-FileHash "C:\Users\KoR\Documents\NinjaTrader 8\bin\Custom\AddOns\**\EchoExecutionAddOn.cs"` y compartir el/los hash(es) con el submanager (esperado `a93a6a1e…` del release, una sola copia).

## JSON de configuración del AddOn — PRESENTE; pendiente confirmar su CONTENIDO (RESUME-02)

**Corrección de RESUME-01:** el archivo `echo-execution-addon.json` **SÍ existe** en el perfil KoR (`C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json`) y fue cargado por NT al arranque del PID 8556. Evidencia (source byte-exacto `a93a6a1e…`, sin `9771` hardcodeado): sin JSON el AddOn no diala (Warning + lanes caídas); con JSON inválido limpia los bindings y tampoco diala; **sólo un JSON válido produce el dial** a `192.168.31.161:9771` que el especialista B y el verificador C observaron en `netstat` (SYN_SENT transitorio, ~1 intento cada 10 s). La conclusión previa «nunca fue entregado» era una inferencia del staging borrado, refutada por este comportamiento. El AddOn relee el JSON sólo al arrancar: si se corrige el archivo, hace falta reiniciar NT.

**Única acción Owner pendiente antes del armado:** confirmar el CONTENIDO del JSON (sin exponer el token): lista de bindings (debe ser **Sim101 exclusivamente**, con host `192.168.31.161` puerto `9771`) y decirle al submanager qué `auth_token` contiene (el bridge debe validar el mismo token; si no coincide, se corrige en el armado). Verificación opcional que cierra V8: `Get-FileHash "C:\Users\KoR\Documents\NinjaTrader 8\bin\Custom\AddOns\**\EchoExecutionAddOn.cs"` (esperado `a93a6a1e…`). Estado SEGURO actual: sin listener en 9771 la conexión nunca completa y sin routing futures no existe productor de órdenes — cero capacidad de orden.

## Qué queda PROHIBIDO para cualquiera (vigente)

- Habilitar `futures-bridge/accounts` (clave de armado), iniciar `futures-bridge`, o poner `enabled=true` en la asociación `certnt01-a1` sin un despacho explícito del Manager (eso ES armar ejecución).
- Ejecutar/cancelar órdenes en cuentas RJARA\*/E2T del Owner. SIM autorizada para esta certificación: **Sim101** exclusivamente.
- Mergear `feature/ef-runtime-pools` a master o tocar Echo PROD.

## Reanudación de la certificación

Orden de desbloqueo: (1) Manager corrige el typename de `market_stream` (+ test de gramática de typename) y re-despliega el module verbatim, decidiendo la política del backlog del grupo `echo-statefun-futures-market-feed` (lag ~1,3M sobre committed 21.848.991; cambiar offsets requiere autorización); (2) Owner reconecta «Simulación» y confirma contenido del JSON (bindings = Sim101; token); (3) submanager arma la sesión SIM: token + binding + `futures-bridge/accounts` SOLO con la cuenta de certificación, verificación de binding Sim101; (4) smoke del gateway y recorrido Strategy→MM→NT/SIM (C3); (5) rotación/recuperación/economía (C4, con `MULTIACCOUNT_NT_NOT_EXECUTED` si no hay más cuentas NT SIM autorizadas); (6) verificación independiente (C5) y estado final seguro (ejecución automática deshabilitada).
