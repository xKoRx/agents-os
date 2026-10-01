# Echo Futures — D6 N1 Shot 1 — NinjaTrader Read-Only Vertical Implementation

**Shot:** D6 N1 Shot 1 — read-only NinjaTrader ↔ Echo vertical (no orders)
**Role:** Senior Implementation Agent (IMPLEMENTER; no Manager, no Owner, no verifier independiente)
**Date:** 2026-10-01 (evidencia UTC 13:0x–13:46Z)
**Project:** [[Echo Futures]]
**Echo frozen baseline antes:** `xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d`
**Branch de trabajo:** `origin/feature/d6-n1-readonly-vertical` @ `36a083a49b94e06a8d57a047f44fac720dda21b9` (FF sobre el baseline congelado; 5 commits)
**Authorities:** C0 + C1 + C1-R1 (Manager QA `ACCEPTED_WITH_AMENDMENT`, 2026-10-01); D4/D5 frozen (Architecture Candidate V2, Functional/Technical SPEC V1, ATP V1, Performance Budgets V1, D5 shots)
**Verdict:** `D6_N1_SHOT1 = BLOCKED` — bloqueo único y accionable: la instalación física del AddOn y el restart de NinjaTrader viven en la sesión interactiva del owner en `dev-win` (ACL de lectura Y escritura denegadas para `dev-win\echo-dev` sobre el perfil KoR, demostrado hoy; sin admin sobre `Program Files`; NT corre en sesión SI=2 ajena). Todo el lado Echo del vertical está implementado, desplegado en DEV y **físicamente verificado end-to-end** (protocolo, relay, Kafka ingress). Bundle de instalación owner listo con checklist de ~5 min; con él, un shot corto de re-verificación reclasifica los ítems NT-side.

## 0. Hard safety

No se envió, modificó ni canceló orden alguna. `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`, estructuralmente: el AddOn no contiene ninguna llamada a `Account.Submit/Change/Cancel/Flatten`; el protocolo `echo.ntfeed.v1` no tiene familia de comandos; el relay nunca escribe al AddOn (conexión de datos unidireccional AddOn→bridge) y su única superficie Kafka es el topic de market ingress; no se arrancó el execution bridge (ningún consumidor de `echo.order-commands.*`). Ningún otro transporte (PROJECTX/RITHMIC/CQG) fue tocado. No se cambió ninguna ACL ni identidad en `dev-win` (mandato C0/C1 vigente). El token del canal vive sólo en ETCD DEV (`futures-bridge/nt-feed/auth-token`) y en un archivo 0600 en Daedalus; este artifact no lo contiene.

## 1. Alcance cubierto vs mandato

| Ítem /scope | Estado |
|---|---|
| 1. NinjaScript AddOn (`AddOnBase`) | IMPLEMENTADO (`EchoFeedAddOn.cs`), instalación pendiente owner |
| 2. Account identity (Id+Name, fail-closed, defence-in-depth) | IMPLEMENTADO en los 3 planos (AddOn resolve / relay hello-match / ETCD binding) |
| 3. Owner-risk/entitlement F2 + amend Manager | IMPLEMENTADO + tests; config ETCD registrada (UNKNOWN + aceptación + `PhysicalEgressApproved=false`) |
| 4. Canal read-only AddOn↔bridge | IMPLEMENTADO + desplegado + smoke físico OK |
| 5. Market data NQ → ingress canónico | IMPLEMENTADO + verificado con envelopes QUOTE/TRADE reales en el topic |
| 6. Observabilidad | ECHO-SIDE verificada; NT-side pendiente de la instalación |
| 7. Protective STOP (compatibilidad F1) | Cumplido: N1 no introduce ni asume `protective == LIMIT`; ninguna superficie compartida tocada |

## 2. Implementación (branch `feature/d6-n1-readonly-vertical`, 5 commits sobre 13e087a3)

1. `94d46708` — **F2 dominio** (`v3/sdk/futures/domain/provider.go`): `OwnerRiskAcceptance{DecisionRef, DecidedAt, PhysicalEgressApproved}` como campo separado de `TransportEntitlement` (jamás reclasifica el grant del firm); predicado compartido `AutomationAuthorized()` (ALLOWED/CONDITIONAL ⇒ true; UNKNOWN ⇒ sólo con aceptación con provenancia; FORBIDDEN y valores desconocidos ⇒ siempre false) y `PhysicalEgressAuthorized()` (idem + egress explícito para UNKNOWN); degradación permanente `ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED`; `ProviderAccountBinding.Validate()` habilita bajo UNKNOWN+aceptación y falla cerrado con FORBIDDEN/provenancia ausente. Manager amendment literal: la aceptación read-only jamás autoriza egress físico.
2. `2df5ae18` — **F2 wiring bridge** (`v3/futures-bridge`): `internal/binding.Load` = fuente única del binding (bridge main + relay) con claves ETCD `owner-risk-accepted-{ref,at,egress}`; `staticEligible` usa `AutomationAuthorized()`; readiness gana dimensión `PHYSICAL_EGRESS_NOT_APPROVED` (read-only observable, jamás `ReadyNewRisk`); `Status` + health log exponen la degradación permanente; `cmd/futures-bridge/main.go` delega en el loader (comportamiento SIM/dev intacto: default ALLOWED preserved).
3. `2eabc1f2` — **Canal ntfeed** (`core/ntfeed` + `adapters/ntfeed` + `cmd/nt-feed-relay`): framing newline-JSON `echo.ntfeed.v1` con familias `hello|session|account|positions|orders|executions|market|heartbeat` (no existe familia de comandos — kill-switch estructural del egress); auth token con `subtle.ConstantTimeCompare` + hello obligatorio en deadline; límite de frame 64KB; disciplina de seq estrictamente monótona por sesión (duplicado/rewind ⇒ rechazo contado, jamás dato); mapping de market frames a `MarketCandidateEnvelope` congelado (clase C: `log_identity = ninjatrader-addon/<session>`, `offset = seq` — re-publicar el mismo frame resuelve a la misma identidad canónica; identificadores distintos jamás colisionan); payload canónico construido con `units.Price/Quantity` y auto-chequeado contra `bars.ParseTradePayload/ParseQuotePayload` (los bytes que produce el relay son exactamente los que el side Echo parsea); publicación sync a `echo.futures.market-feed-candidates.v1` con key = `stream_id` y value **JSON crudo** (`json.RawMessage` — el `SerializeValue` del SDK hace `json.Marshal` y un `[]byte` plano viaja base64, defecto encontrado y corregido en `36a083a`); evidencia estructurada con account ids enmascarados (`****últimos4`) + evidence sink opcional full-fidelity 0600 para operación local; binding verificado defence-in-depth contra la autoridad ETCD (hello `expected_account` vs binding `provider-external-account-id`; `MISMATCH`/binding no cargado = fail-closed, el lane de mercado —nivel stream, read-only— continúa).
4. `4126b877` — **EchoFeedAddOn** (`v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs`, C# 5-compatible): AddOn `AddOnBase` observation-only; config local `Documents\NinjaTrader 8\echo\echo-feed-addon.json` (reintento ~60 s sin restart si falta); escaneo de `Connection.Connections` + publicaciones de estado; descubrimiento `Account.All` (todas las GAU50 visibles) con resolución de la cuenta activa por `Id` (Int64) + cross-check `Name` — jamás por selector GUI ni posición de colección; `match = RESOLVED | MISMATCH | DISCOVERY_ONLY` publicado fail-closed; snapshots periódicos de balances (`GetAccountItem`, ítems ausentes degradan visiblemente), positions, orders y executions nuevas (dedup por `ExecutionId`, historia previa primada sin publicarse); market data por eventos `Instrument.MarketData.Update` (TRADE `Last` tick-a-tick; QUOTE = par BBO mantenido por el AddOn — NT entrega Bid/Ask como eventos separados; resets como evidencia de barrier); heartbeat con contadores; writer thread con cola acotada + reconnect exponencial; una sola conexión outbound; sin loop de lectura (no puede recibir comandos).
5. `36a083a` — fix record crudo (arriba).

**Reuse compliance:** journal M2, readiness, barrier, gate de sesión, families de eventos, topic routing, provider plane, envelopes de mercado,EXACT_REPLAY/BACKTEST: intactos (ningún cambio). El transport branch SIM-only de `buildSession` queda para N2 tal como lo clasificó C1 (SMALL_D6_ADAPTER_WORK). No se construyó plugin framework, IPC genérico, UI, copier ni multi-provider.

## 3. Tests y verificación software

Comando canónico por regla 01 (`go test -race -cover`), suites acotadas (sin `go test ./...` global por la guarda de seed tests conocida):

- `v3/sdk/futures` (race): 12/12 paquetes ok, incluyendo nuevos: matriz completa de `AutomationAuthorized`/`PhysicalEgressAuthorized`/degradación, `Validate` de binding con aceptación (UNKNOWN sin aceptación falla; read-only carga; FORBIDDEN jamás; valor desconocido jamás; provenancia obligatoria), y admission: UNKNOWN+aceptación+egress=false ⇒ `DENY_NEW_RISK` con `ENTITLEMENT_REVOKED`; egress=true ⇒ ALLOW; FORBIDDEN+aceptación ⇒ deny; UNKNOWN sin aceptación ⇒ deny.
- `v3/futures-bridge` (race): 100% ok — `core/ntfeed` **96.1%**, `adapters/ntfeed` **96.2%**, `internal/binding` **100%**; readiness table actualizada (bloqueo `PHYSICAL_EGRESS_NOT_APPROVED`), sesión bajo aceptación read-only: `StaticEligible` elegible, `ReadyNewRisk=false`, degradación visible; sesiones ALLOWED sin degradación fantasma (regresión D5).
- Regresión `v3/core`: `internal/functions` (futures) + `internal/futuresvertical` (25 s) + `internal/futuresruntime` ok.
- Cobertura nueva ≥ 95% en toda la lógica nueva razonablemente testeable; las ramas restantes son inalcanzables por diseño (marshal infalible) o paths de acept TCP no-deterministas, y se declararon como tales.

## 4. Despliegue DEV y verificación física Echo-side (2026-10-01)

| # | Evidencia | Método | Timestamp UTC |
|---|---|---|---|
| E1 | Release `36a083a49b94…` en `/home/kor/opt/echo-dev/releases/36a083a…/nt-feed-relay`, `vcs.revision=36a083a… vcs.modified=false`, go1.27.1 linux/amd64, SHA256 `6d720dac…e0bd26ca` | build local + `go version -m` + sha256sum | 13:26Z |
| E2 | Unidad `systemd --user` `echo-nt-feed-relay.service` enabled+active (linger Daedalus ya certificado §5.1 contrato ambientes); `/proc/PID/exe` = release E1; listener `*:9770` | systemctl + ss + readlink | 13:34Z |
| E3 | Config ETCD `/echo/development/futures-bridge/nt-feed/*` + binding `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/*` con `entitlement=UNKNOWN`, `owner-risk-accepted-ref=EF-D6-OWNER-RISK-ACCEPTED-2026-09-30`, `owner-risk-accepted-at=2026-09-30T00:00:00Z`, `owner-risk-accepted-egress=false`; read-back doble (writer con verificación + plano MCP ETCD RO) | ETCD DEV | 13:2xZ |
| E4 | F2 mecanismo demostrado en runtime: relay carga el binding con UNKNOWN+aceptación (read-only) y expone `echo.entitlement.degradation`/`physical_egress_approved=false`; con `provider-external-account-id` aún ausente (se fija tras el discovery del AddOn) el estado de binding queda fail-closed visible (`binding_loaded=false`, error declarado) — el lane de mercado sigue operativo por ser stream-level | journalctl del relay | 13:30Z |
| E5 | Smoke de protocolo real (cliente efímero reutilizando el contrato `core/ntfeed` por TCP real): hello autenticado + 7 familias + 2 market frames; `ntfeed.published=2/2`, `malformed=0`, `rejected=0`; ids de cuenta enmascarados en logs (`"id":"****1111"`); evidence file 0600 con registros de familias de evidencia | TCP + journalctl + evidence.jsonl | 13:31–13:41Z |
| E6 | Topic `echo.futures.market-feed-candidates.v1` creado en clúster Kafka DEV (5 particiones, RF=3, retention 1d — alineado al ingress declarado del module.yaml DEV congelado; no existía: el clúster DEV no tiene ningún topic `echo.futures.*` ni el grupo del ingress — el job StatefulFunctions DEV desplegado es pre-D5 y no incluye las ingresses futures) | kafka MCP DEV | 13:2x–13:37Z |
| E7 | Ingress recibiendo: 2 registros físicos en el topic (`offset 0 QUOTE`, `offset 1 TRADE`, key `NQ:NQZ6`) con el envelope JSON crudo exacto (`stream_id`, `source_id=NINJATRADER_ADDON`, `ingress_ref{log_identity:"ninjatrader-addon/smoke-final", partition:0, offset:6|7}`, `payload` base64 del shape canónico `{"bid_price":"21845","bid_qty":5,"ask_price":"21845.25","ask_qty":3}` / `{"price":"21845.25","qty":2}`, `receive_ts` presente) — decodificado y verificado contra `market.MarketCandidateEnvelope` | consume MCP + decode | 13:37Z |

Nota E6/E7: el procesamiento canónico downstream (`echo/market_stream` en StateFun) requiere redeploy del job DEV core con el module.yaml D5 — fuera del alcance N1 (runtime core DEV es propiedad de otra sesión según contrato §5.1) y no bloquea N1 (la obligación de este shot es la publicación al ingress). Queda registrado como input de N2/N3.

## 5. Verificación física dev-win y bloqueo

| # | Evidencia | Método (perfil dev-win-operator) | Timestamp UTC |
|---|---|---|---|
| E8 | NinjaTrader 8.1.8.3 vivo: PID **3464**, sesión **2** (owner), `ProductVersion 8.1.8.3` | PowerShell `Get-Process` + `Get-Item …VersionInfo` | 13:4xZ |
| E9 | Sesión Tradovate continua: mismas conexiones de C0 con puertos locales idénticos (`49960→34.117.68.229:443` ×2 = demo.tradovateapi.com, `53464→3.133.196.229:31655` MD gateway, accelerator) ⇒ continuidad ≥ 12 h desde la certificación C0 (01:52Z), sin reconnect | `netstat -ano` filtrado PID 3464 | 13:4xZ |
| E10 | ACL `dev-win\echo-dev`: `Test-Path Documents\NinjaTrader 8\bin\Custom\AddOns` ⇒ **PermissionDenied** (lectura); `New-Item … AddOns\EchoFeed` ⇒ **Access denied** (escritura); `New-Item … Documents\NinjaTrader 8\echo` ⇒ **Access denied**; `New-Item Program Files\NinjaTrader 8\bin\Custom\AddOns\EchoFeed` ⇒ **Access denied** (sin admin). `read-command` del perfil viewer se niega entero (`POLICY_DENIED: read-only`), `tasklist` por cmd ⇒ Access denied (Get-Process sí funciona) | EncodedCommand probes | 13:4xZ |
| E11 | NT corre en sesión interactiva ajena (SI=2): el restart requerido para compilar el `Custom` folder (carga de AddOns ocurre sólo al arranque) es operación del owner — idéntico boundary B2 de C0 | Get-Process SessionId + límites de identidad | 13:4xZ |

**Consecuencia:** la instalación del AddOn y su primera carga son un paso one-time asistido por owner, tal como anticipó C1 §G. Bundle completo entregado en `kor@daedalus:/home/kor/opt/echo-dev/var/nt-feed/owner-install/` (`EchoFeedAddOn.cs` SHA256 `799bdf8e…737d8b`, `echo-feed-addon.json` con token real modo 600, `OWNER-CHECKLIST.md` con los 4 pasos exactos). El config viene `account_id: ""` (discovery-only) para que el primer restart ya rinda evidencia completa; la cuenta activa se activa editando ese campo (elección owner, C1 inputs).

## 6. Contradicciones / hallazgos

1. **`SerializeValue` base64 (corregido en este shot):** el `messaging.Producer` serializa `Message.Value` con `json.Marshal`; un `[]byte` plano viaja como string base64, con lo que el ingress raw-string de StateFun no puede parsearlo. `PublishCandidate` usa `json.RawMessage`. Los offsets 0–3 originales del topic (smoke-0001/0002, defectuosos) se eliminaron recreando el topic (sin consumidores registrados en ese momento); el estado físico final del topic son los 2 registros limpios de E7. **Input para N2:** el publisher de execution-events del bridge D5 publica `[]byte` plano por el mismo path — cuando ese vertical se despliegue físicamente necesitará el mismo ajuste o un wrapper.
2. Ninguna contradicción con el diseño congelado. El mandate F2+amend se implementó literal; N1 no tocó F1 (STOP_MARKET queda precondición N2).

## 7. Handoff

```text
D6_N1_SHOT1 = BLOCKED

ARTIFACT:
main/10-projects/Echo Futures/artifacts/d6-ninjatrader-n1-20261001/N1-SHOT1-READONLY-VERTICAL.md

AGENTS_OS_SHA:
05409356860ca8a99c1a0c9ff533c30aa9a75c5e

ECHO_BASELINE_BEFORE:
13e087a3bb762f65b060d3b3200fb00a67c6ff1d

ECHO_BASELINE_AFTER:
36a083a49b94e06a8d57a047f44fac720dda21b9 (origin/feature/d6-n1-readonly-vertical, FF sobre baseline; master intocado)

NINJATRADER_VERSION:
8.1.8.3 (dev-win 192.168.31.132, PID 3464 sesión owner, Tradovate vivo ≥12h)

ADDON:
BLOCKED (implementado y commitado; instalación bloqueada por ACL/sesión owner — bundle + checklist entregados)

BRIDGE_CHANNEL:
PASS (relay release 36a083a activo en Daedalus :9770; smoke TCP real con auth + 8 familias)

GAU50_ACCOUNTS_DISCOVERED:
0 (pendiente primera carga del AddOn; el canal demuestra descubrimiento enmascarado del protocolo con cuentas sintéticas)

ACTIVE_ACCOUNT_BINDING:
BLOCKED (binding ETCD E2T-GAU50-01 cargado por el relay con UNKNOWN+aceptación y fail-closed visible; provider-external-account-id se fija tras el discovery; defence-in-depth hello↔binding implementada y testeada)

ENTITLEMENT:
UNKNOWN

OWNER_RISK_ACCEPTANCE:
PASS (config ETCD con DecisionRef=EF-D6-OWNER-RISK-ACCEPTED-2026-09-30, DecidedAt=2026-09-30, egress=false; mecanismo F2 con amend Manager implementado y demostrado en runtime)

PHYSICAL_EGRESS_APPROVED:
false

EGRESS_HARD_DISABLED:
PASS (sin familia de comandos en el protocolo; AddOn sin llamadas de órdenes y sin lectura del canal; relay sin superficie de comandos; execution bridge no arrancado; admission/readiness fail-closed bajo UNKNOWN+egress=false — tests)

NQ_MARKET_DATA:
NOT_TESTED (pendiente AddOn en NT)

QUOTE_STREAM:
PASS como contrato y pipeline (envelope QUOTE canónico físico en el ingress vía smoke; ticks NT reales pendientes del AddOn)

TRADE_STREAM:
PASS como contrato y pipeline (idem)

ACCOUNT_STATE:
NOT_TESTED (pendiente AddOn)

POSITIONS:
NOT_TESTED (pendiente AddOn)

ORDERS:
NOT_TESTED (pendiente AddOn)

ECHO_MARKET_INGRESS:
PASS (topic canónico DEV creado según module.yaml congelado; 2 registros QUOTE/TRADE físicos verificados byte-level)

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

TESTS:
go test -race: v3/sdk/futures 12/12 ok; v3/futures-bridge 100% ok; regresión v3/core functions+futuresvertical+futuresruntime ok. Nuevos: matriz F2 completa, admission egress gate, readiness PHYSICAL_EGRESS_NOT_APPROVED, protocolo/masking/clase-C/tracker/server/relay/kafka.

COVERAGE:
core/ntfeed 96.1% · adapters/ntfeed 96.2% · internal/binding 100%; resto de lógica nueva razonablemente testeable ≥95%; ramas sin cobertura declaradas inalcanzables (marshal total, accept errors TCP no-deterministas).

FILES_CHANGED:
v3/sdk/futures/domain/provider.go; v3/sdk/futures/provider/admission.go (+2 test files nuevos); v3/futures-bridge/{internal/binding,internal/session,core/capabilities,core/bridge.go,cmd/futures-bridge/main.go}; v3/futures-bridge/core/ntfeed/* (nuevo); v3/futures-bridge/adapters/ntfeed/* (nuevo); v3/futures-bridge/cmd/nt-feed-relay/main.go (nuevo); v3/futures-bridge/addon-ninjatrader/* (nuevo)

CONTRADICTIONS:
NONE con el diseño congelado. Hallazgo de plataforma corregido: SerializeValue base64 para []byte (input N2 para execution-events del bridge).

BLOCKERS:
B1: instalación del AddOn + restart NT requieren la sesión interactiva del owner en dev-win (ACL lectura+escritura denegadas al perfil KoR para dev-win\echo-dev, demostrado hoy E10; Program Files sin admin; NT SI=2). Resolución: checklist owner (~5 min) en kor@daedalus:/home/kor/opt/echo-dev/var/nt-feed/owner-install/OWNER-CHECKLIST.md. Nada más bloquea.

SHOT2_INPUTS:
(1) Tras checklist owner: shot corto de re-verificación N1 (reclasa ADDON/ACCOUNT_STATE/POSITIONS/ORDERS/NQ a PASS|FAIL, fija provider-external-account-id en ETCD y activa account_id en la config del AddOn — elección owner de la GAU50 activa). (2) N2 requiere: F1 STOP_MARKET completo, gate stop nativo venue-held, re-affirm owner de egress, transport branch en buildSession + adapter NINJATRADER_BRIDGE, y el ajuste SerializeValue en el publisher execution-events. (3) Procesamiento canónico downstream exige redeploy del job Flink DEV core con module.yaml D5 (otra sesión/owner). (4) Hardening pendiente N2: canal LAN+token → mTLS/ACL si se exige.

NEXT_MANAGER_ACTION:
Comunicar al owner la checklist (owner-install en Daedalus, 4 pasos, ~5 min) y despachar el shot de re-verificación N1 al confirmar el restart; después, secuenciar N2 según SHOT2_INPUTS. No emitir D6_N1=PASS ni EF_D6_E2E_PASS desde este shot.
```
