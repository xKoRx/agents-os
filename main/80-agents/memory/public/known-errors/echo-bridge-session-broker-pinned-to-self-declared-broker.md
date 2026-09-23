---
type: known_error
schema_version: 1
scope: area
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Aranea]]"
project: "[[Echo]]"
application:
entities:
  - "[[Echo]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[echo-production-operational-audit]]"
aliases:
  - wsfmarkets-pinned-broker
  - echo-bridge-broker-not-available-999
confidence: high
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - area/aranea
  - area/echo
---

# echo-bridge-session-broker-pinned-to-self-declared-broker

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Una cuenta de ejecución no recibe copias y no deja ninguna fila en `echo.trade_journal` (ni siquiera `FAILED`): falla en silencio total.
- WARN en Loki `{service_name="echo-core", level="WARN"}`: `execution_store [OPEN_FAILED] error_code=999 "Symbol not available"` (símbolo canónico plano llega al terminal), y para índices `mm_engine MM_CALCULATION_ERROR "FIXED_RISK requires InstrumentSnapshot nil"`.
- La misma señal sí abre tickets en las demás cuentas del mismo fan-out.

## Causa

- El EA MT5 se autodeclara el broker en `POST /api/v1/register` (`GetBrokerName()`): si aún no recibió ClientConfig, cae a `NormalizeBrokerName(GetAccountCompany())` (ej: "WSF Markets" → `WSFMARKETS`).
- El bridge arma la sesión con ese string y el handshake la cementa (`if clientConfig.Broker == ""` rellena con el declarado cuando la cuenta aún no existe en Echo/kache).
- `echo.symbol_mappings` no tiene filas para el nombre autodeclarado → `Detransform` cae a identidad → el EA recibe el símbolo canónico plano → `SymbolInfoDouble(SYMBOL_POINT)==0` → 999.
- La sesión nunca reconciliaba: `GetOrCreateSession` hace resume sin actualizar Broker.
- Corregido en `c99aee06` (master): `resolveAccountBroker` prefiere el kache; re-registro repara pipes in-place; `BroadcastConfigUpdate` reconcilia sesión antes del gate de estado.

## Impacto

- La cuenta afectada queda operativamente muerta en silencio (cero copias, cero filas de error en DB) mientras las demás copian normalmente.

## Detección

- Loki ventana corta: `{service_name="echo-bridge"} |= "detransformed"` muestra el broker de la sesión y el símbolo enviado por `command_id` — discriminador directo entre config de sesión y Market Watch.
- DB: cero legs EXECUTION de la cuenta + `accounts.updated_at` fresco (EA conectado) + whitelist/`allowed_symbols` correctos.

## Mitigación

- Desplegar bridge ≥ `c99aee06` y reiniciarlo: el EA re-registra y la sesión/pipe se reconcilian con el broker canónico del kache.
- Sin deploy: alias del broker autodeclarado en `echo.symbol_mappings` (4 filas canonical→broker) — se propaga por `echo.symbol-mappings.v1` sin tocar el terminal.

## Evidencia

- Incidente WSF NEW! `183623` (2026-09-21..23, mt4-real): registrado `WSFMARKETS`, comandos USDJPY fallaban con 999; fix verificado E2E en dev-win (registro sin config → config llega → reconciliación automática → `broker=WSF broker_symbol=USDJPYc`).
