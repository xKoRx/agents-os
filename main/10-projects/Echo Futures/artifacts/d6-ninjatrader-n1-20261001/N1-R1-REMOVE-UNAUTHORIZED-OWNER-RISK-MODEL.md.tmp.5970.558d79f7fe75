# Echo Futures — D6 N1-R1 — Remove Unauthorized Owner-Risk Model

**Shot:** D6 N1-R1 — focused remediation (owner-ordered)
**Role:** Senior Remediation Implementer (no Manager, no Owner, no arquitecto)
**Date:** 2026-10-01 (evidencia UTC 14:0x–14:35Z / local -03)
**Project:** [[Echo Futures]]
**Mandato:** eliminar completamente del producto y la configuración el modelo no autorizado `OwnerRiskAcceptance` (C1-R1 F2 + amendment), preservando el trabajo válido N1. Sin rediseñar entitlement, sin inventar otra excepción, sin transformar `UNKNOWN`, sin tocar `FORBIDDEN`, sin adelantar N2.
**Echo baseline antes:** `xKoRx/echo@36a083a49b94e06a8d57a047f44fac720dda21b9` (`origin/feature/d6-n1-readonly-vertical`, FF sobre el baseline congelado `13e087a3bb762f65b060d3b3200fb00a67c6ff1d`)
**Echo baseline después:** `xKoRx/echo@7af6210ad635ecce6e06107ddc6af398d8f83330` (push FF `36a083a4..7af6210a` a `origin/feature/d6-n1-readonly-vertical`; master intocado)
**Verdict:** `D6_N1_R1_OWNER_RISK_REMOVAL = PASS` — el modelo rechazado no existe ya ni en source ni en config ni en el runtime Echo-side; el trabajo válido N1 queda intacto y byte-verificable contra el baseline congelado.

## 0. Hard safety

No se envió, modificó ni canceló orden alguna: `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`, estructural y re-verificado tras el remediation — el AddOn no contiene ninguna llamada `Account.Submit/Change/Cancel/Flatten` (el único match del grep es su comentario negativo en `EchoFeedAddOn.cs:20`), el protocolo `echo.ntfeed.v1` mantiene exactamente 8 familias de observación (`hello|session|account|positions|orders|executions|market|heartbeat`) sin familia de comandos, y el relay no escribe al AddOn (su único `Write` es el evidence file local 0600). No se arrancó el execution bridge. No se tocó PROD, no se tocó `FORBIDDEN`, no se seteó `entitlement` a `ALLOWED`, no se creó flag/override/bypass nuevo. No se instaló el AddOn ni se continuó certificación física (bundle owner-install en Daedalus intacto y limpio, ver §5).

## 1. Verificación de baseline y alcance del diff

HEAD real al iniciar = `36a083a` (idéntico a origin; worktree limpio en `~/aranea/work/d6-n1-readonly-20261001/echo`). Diff contra `13e087a3`: 29 archivos. El modelo rechazado vivía exactamente en 2 commits:

- `94d46708` — F2 dominio: `OwnerRiskAcceptance{DecisionRef,DecidedAt,PhysicalEgressApproved}`, campo `TransportSpec.OwnerRiskAccepted`, predicates `AutomationAuthorized()`/`PhysicalEgressAuthorized()`, `EntitlementDegradation()` → `ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED`, y `ProviderAccountBinding.Validate()` relajado para habilitar UNKNOWN+aceptación.
- `2df5ae18` — F2 wiring: loader compartido `internal/binding` leyendo keys `owner-risk-accepted-{ref,at,egress}`, readiness con dimensión `PhysicalEgressAuthorized` (`PHYSICAL_EGRESS_NOT_APPROVED`), `Status.EntitlementDegradation`, health log `echo.entitlement.degradation`.

Inventario completo por `git grep` de los 6 términos mandados: 13 archivos (ninguno de los componentes ntfeed puros los referenciaba salvo el surface de `BindingState`).

## 2. Cambios aplicados (15 archivos, +119/−597)

Revert exacto (byte-idéntico al baseline congelado, verificado por `git checkout 13e087a3 --` tras confirmar que cada archivo fue tocado sólo por commits F2):

| Archivo | Efecto |
|---|---|
| `v3/sdk/futures/domain/provider.go` | Sin `OwnerRiskAcceptance`; `Validate()` D5: `UNKNOWN|FORBIDDEN` no enableable, valores desconocidos fallan |
| `v3/sdk/futures/provider/admission.go` | Switch D5: `ALLOWED\|CONDITIONAL` pasan; `UNKNOWN\|FORBIDDEN` y valores desconocidos ⇒ `DenyReasonEntitlementRevoked` |
| `v3/futures-bridge/core/capabilities/readiness.go` + test | Sin dimensión `PhysicalEgressAuthorized`/`PHYSICAL_EGRESS_NOT_APPROVED` |
| `v3/futures-bridge/internal/session/session.go` + test | `staticEligible()` switch D5; sin `Status.EntitlementDegradation` |
| `v3/futures-bridge/core/bridge.go` | Health log sin attr `echo.entitlement.degradation` |
| `v3/futures-bridge/cmd/futures-bridge/main.go` | Delegación en loader compartido preservada; comportamiento D5 (default ALLOWED) intacto |
| `v3/sdk/futures/domain/provider_owner_risk_test.go`, `v3/sdk/futures/provider/admission_owner_risk_test.go` | Eliminados |

Quirúrgico (archivos N1 válidos que exhibían surface F2):

- `v3/futures-bridge/internal/binding/loader.go` (+test): el loader compartido se **conserva** (fuente única de binding para bridge main + relay; sin él habría que inventar otro seam, prohibido por mandato) pero sin las keys `owner-risk-accepted-*` ni su documentación. D5 semantics: sólo `ALLOWED|CONDITIONAL` cargan binding enabled.
- `v3/futures-bridge/adapters/ntfeed/relay.go` (+test): `BindingState` sin `Degradation`/`PhysicalEgressApproved`; `Loaded/ExecutionAccountID/ProviderExternalAccountID/Entitlement/Err` intactos — la verificación defence-in-depth hello↔binding queda operativa.
- `v3/futures-bridge/cmd/nt-feed-relay/main.go`: sin surface owner-risk (attrs `echo.entitlement.degradation` y `physical_egress_approved` eliminados); fail-closed del binding lane visible.

Resultado neto vs baseline congelado: el árbol contiene exactamente el trabajo N1 válido (canal ntfeed, relay, AddOn C#, publisher JSON crudo, tests) + el loader compartido de binding sin owner-risk — 19 archivos, +3602 líneas, 0 referencias al modelo eliminado.

## 3. Verificación /verify

- `git grep -n -e OwnerRiskAcceptance -e OwnerRiskAccepted -e PhysicalEgressApproved -e AutomationAuthorized -e PhysicalEgressAuthorized -e ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED` → **0 matches** en todo el repo (única mención histórica: los artifacts/journal del vault, marcados superseded).
- Tests (`go test -race -count=1`): `v3/sdk/futures` 13/13 pkgs ok (incluye domain, provider admission); `v3/futures-bridge` 11/11 pkgs con tests ok (`core/ntfeed`, `adapters/ntfeed`, `internal/binding`, `internal/session`, `core/capabilities`, `core`); regresión `v3/core`: `internal/futuresvertical` (27.5s), `internal/futuresruntime`, `internal/functions` ok. Sin `go test ./...` global (guarda seed tests).
- `go vet` limpio en los paquetes tocados; `gofmt` aplicado sólo a `cmd/nt-feed-relay/main.go` (los demás archivos no-formateados ya estaban así en `36a083a`/master — deuda de estilo preexistente, fuera de alcance).

## 4. ETCD DEV cleanup y redeploy relay

- Eliminadas (herramienta efímera SDK `DeleteVar` + read-back, luego borrada del worktree; nunca `SetVar`): `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/owner-risk-accepted-{ref,at,egress}` (36/20/5 bytes). Verificación doble: read-back del writer (3× `DELETED_AND_VERIFIED`) + listado plano MCP ETCD RO (8 keys restantes, 0 owner-risk). Sobreviven intactas: `entitlement=UNKNOWN`, `provider-id=EARN2TRADE`, `program-id=GAU50`, `enabled=true`, day-boundary, rule-set.
- Relay read-only redesplegado desde el HEAD nuevo: release `/home/kor/opt/echo-dev/releases/7af6210a…/nt-feed-relay` (`vcs.revision=7af6210a…`, `vcs.modified=false`, go1.27.1, SHA256 `db04ee78…42998f1`); unidad `systemd --user echo-nt-feed-relay` activa, MainPID 579561, `/proc/PID/exe` y SHA verificados, listener `*:9770`. Journal del proceso nuevo: **0 attrs** `entitlement.degradation`/`physical_egress_approved`; binding fail-closed visible (`binding_loaded=false`, `domain: binding for account E2T-GAU50-01 cannot be enabled with UNKNOWN automation entitlement`); lane de mercado operativa (stream-level). Rollback documentado en BUILD.md (repoint ExecStart a release `36a083a`).

## 5. Preservación N1 verificada

Diff total vs `13e087a3` = sólo los archivos N1 válidos: `core/ntfeed/*` (frame, market, tracker + tests), `adapters/ntfeed/*` (relay, kafka, server + tests), `cmd/nt-feed-relay`, `internal/binding/*`, `addon-ninjatrader/*` (EchoFeedAddOn.cs, README, example config). El AddOn del bundle owner-install en Daedalus (`/home/kor/opt/echo-dev/var/nt-feed/owner-install/EchoFeedAddOn.cs`) es byte-idéntico al repo (SHA256 `799bdf8e…737d8b` en ambos lados) y el bundle completo no contiene ninguna referencia owner-risk/acceptance/entitlement/egress. Topic `echo.futures.market-feed-candidates.v1` y su ingress no fueron tocados.

## 6. Consecuencia bloqueante (declarada, NO resuelta)

Con la semántica D5 restaurada, el binding `E2T-GAU50-01` con `entitlement=UNKNOWN` **no es enableable ni carga sesión** (`ProviderAccountBinding.Validate` fail-closed). El lane de cuenta del relay queda degradado fail-closed (hello defence-in-depth no resuelve) y una sesión de ejecución del bridge no puede cargar ese binding bajo D5. Esto es exactamente el estado previo a C1-R1: la confirmación externa del entitlement Earn2Trade (hacia `ALLOWED|CONDITIONAL` en el binding ETCD) es una decisión del owner. No se tocó `FORBIDDEN`, no se amplió la semántica, no se creó reemplazo.

## 7. Handoff

```text
D6_N1_R1_OWNER_RISK_REMOVAL = PASS

ECHO_BRANCH:
origin/feature/d6-n1-readonly-vertical @ 7af6210ad635ecce6e06107ddc6af398d8f83330 (push FF 36a083a4..7af6210a; master intocado)

BASELINE_BEFORE:
36a083a49b94e06a8d57a047f44fac720dda21b9

BASELINE_AFTER:
7af6210ad635ecce6e06107ddc6af398d8f83330 (árbol vs 13e087a3 = sólo N1 válido + binding loader sin owner-risk; domain/admission/readiness/session/bridge-main byte-idénticos al baseline congelado)

REMOVED:
OwnerRiskAcceptance{DecisionRef,DecidedAt,PhysicalEgressApproved}; TransportSpec.OwnerRiskAccepted; predicates AutomationAuthorized/PhysicalEgressAuthorized; EntitlementDegradation/ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED; readiness PHYSICAL_EGRESS_NOT_APPROVED; Status.EntitlementDegradation; attrs log echo.entitlement.degradation y physical_egress_approved; keys ETCD owner-risk-accepted-{ref,at,egress}; 2 test files F2

PRESERVED_N1:
Canal ntfeed echo.ntfeed.v1 (8 familias observación, framing 64KB, auth constant-time, seq monótona), relay nt-feed-relay, AddOn EchoFeedAddOn.cs read-only (byte-idéntico al bundle owner), publisher JSON crudo (fix 36a083a), topic ingress echo.futures.market-feed-candidates.v1, defence-in-depth hello↔binding, tests ntfeed (core 96.1% / adapters 96.2% invariantes), loader compartido internal/binding (sin owner-risk)

ETCD_OWNER_RISK_KEYS_REMOVED:
YES (3 keys, read-back doble writer+MCP RO; entitlement=UNKNOWN intacto; cero SetVar)

ENTITLEMENT_SEMANTICS:
RESTORED_TO_D5 (ALLOWED|CONDITIONAL permitido; UNKNOWN|FORBIDDEN y valores desconocidos fail-closed en Validate/staticEligible/admission; FORBIDDEN jamás override)

ACTIVE_OWNER_RISK_REFERENCES:
0 (git grep de los 6 términos = 0 matches; menciones históricas sólo en artifacts/journal del vault marcados superseded/rejected)

TESTS:
go test -race -count=1: v3/sdk/futures 13/13 ok; v3/futures-bridge 11/11 ok (ntfeed/binding/session/capabilities incluidos); regresión v3/core futuresvertical+futuresruntime+functions ok; go vet limpio

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

RUNTIME_ECHO_SIDE:
relay release 7af6210a (vcs.revision=7af6210a, vcs.modified=false, SHA256 db04ee78…42998f1) activo en Daedalus :9770; journal sin surface owner-risk; binding E2T-GAU50-01 fail-closed visible; lane de mercado operativa

NEW_BLOCKERS_AFTER_REMOVAL:
B-R1: binding E2T-GAU50-01 con entitlement=UNKNOWN no es enableable bajo semántica D5 restaurada (Validate fail-closed) — el lane de cuenta del relay queda degradado fail-closed y ninguna sesión de ejecución puede cargar ese binding; el lane de mercado (stream-level) continúa

OWNER_DECISIONS_REQUIRED:
OD-1: confirmar externamente el entitlement Earn2Trade del binding E2T-GAU50-01 y fijarlo a ALLOWED|CONDITIONAL en ETCD DEV si corresponde (no hacerlo aquí por mandato). OD-2 (preexistente N1): instalación del AddOn + restart NT en sesión owner dev-win (checklist ~5 min, bundle intacto y limpio)

NEXT_MANAGER_ACTION:
Comunicar al owner OD-1/OD-2; tras resolverlas, re-verificación corta N1 (reclasa ítems NT-side) y recién entonces evaluar N1 PASS. Este remediation no emite N1 PASS ni D6 PASS.
```
