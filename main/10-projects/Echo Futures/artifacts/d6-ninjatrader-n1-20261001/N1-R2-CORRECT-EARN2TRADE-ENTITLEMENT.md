# Echo Futures — D6 N1-R2 Correct False Earn2Trade Entitlement Blocker

**Fecha:** 2026-10-01
**Mandato:** focused remediation — corregir el blocker falso `entitlement=UNKNOWN` del binding Earn2Trade/GAU50 bajo la corrección owner («Earn2Trade permite automatización/estrategia propia»), sin owner-risk model, sin bypass, sin nuevo enum, sin nueva policy layer; usar el contrato D5 existente.
**Baseline:** `xKoRx/echo@7af6210ad635ecce6e06107ddc6af398d8f83330` (`feature/d6-n1-readonly-vertical`, worktree limpio antes y después; cero cambios de código en este remediation).
**Naturaleza del cambio:** `wrong provider-policy state → correct provider-policy state`. Un solo valor de config ETCD DEV.

## 1. Owner correction (autoridad)

- Premisa corregida por el owner (2026-10-01, mandato N1-R2): **Earn2Trade SÍ permite ejecutar automatización/estrategia propia** (`Earn2Trade != UNKNOWN`). Esto es exactamente la confirmación externa que N1-R1 declaró pendiente como OD-1.
- La corrección resuelve el estado factual del firm: el grant existe (no `UNKNOWN`, no `FORBIDDEN`). No selecciona por sí sola entre `ALLOWED` y `CONDITIONAL`; esa clasificación se resolvió desde autoridades existentes (§2).

## 2. Determinación ALLOWED vs CONDITIONAL (autoridad demostrada, no inventada)

Clasificación vigente correcta: **`ALLOWED`**. Cadena de autoridad:

1. **Contrato D5 congelado** (`v3/sdk/futures/domain/provider.go`, D2-05C §7): `TransportEntitlement` es «the automation entitlement the firm grants for a program/phase»; `TransportSpec.Conditions` es el portador opcional de condiciones. `ALLOWED|CONDITIONAL → enableable`; `UNKNOWN|FORBIDDEN → fail-closed` (`ProviderAccountBinding.Validate`).
2. **Criterio canónico del proyecto** (project note, Front C authoritative matrix, revisión manager 2026-09-26): `CONDITIONAL` queda reservado para grants con condiciones explícitas adjuntas al permiso de automatización — precedentes: Tradeify («sólo con sole ownership, exclusive use, no-HFT»), Topstep sim (restricciones API/no-VPS; Live vía ProjectX API `FORBIDDEN`), TradeDay («mediante plataformas soportadas», API directa prohibida), MFFU (con condiciones HFT/fill-simulation). En contraste, permiso plano con sólo prohibiciones de conducta general se clasifica `ALLOWED` — precedentes: FundedNext (permite EAs/bots; prohíbe latency abuse/order flooding → `ALLOWED`), Lucid (`ALLOWED`).
3. **Evidencia Earn2Trade existente** (artifacts `d6-earn2trade-preflight-20260930/`, Pass 1 + Pass 2 2026-09-30): ninguna autoridad documenta condición alguna adjunta al grant de automatización propia. La prohibición de trade copiers/mirroring está explícitamente separada de la pregunta own-algorithm («trade copying prohibition is not logically equivalent to own-algorithm prohibition»); Prohibited Conduct es lenguaje de conducta general (manipulación/ventaja injusta); la cláusula «Service» de los Terms queda resuelta por la afirmación owner. Las preguntas abiertas (restricciones stage-specific, VPS/unattended) nunca recibieron respuesta documentada que las convierta en condiciones — ausencia de restricción documentada no puede transmutarse en condición.
4. **Semántica interna del proyecto**: `CONDITIONAL` exige «a concrete condition» declarada (`v3/futures-bridge/core/capabilities/capabilities.go`, comentario ExactSubmissionReady). No existe ninguna condición que declarar: escribir `CONDITIONAL` sin condiciones sería fabricar un hecho sin evidencia — exactamente la falsificación que C1-R1 rechazó.
5. Aplicado el criterio canónico: grant afirmado por autoridad owner + cero condiciones documentadas ⇒ **`ALLOWED`**, con `TransportSpec.Conditions` vacío. Las reglas generales del programa (consistencia 30%, DLL, horario, flat 15:50–17:00 CT, no-copiers) viven en el `ProviderRuleSet` (`GAU50-EVAL` v1) y aplican a todo trading con o sin automatización; no son condiciones del entitlement.

El HARD RULE del mandato no dispara: las autoridades existentes SÍ permiten distinguir inequívocamente (`ALLOWED`), mediante los criterios canónicos del manager aplicados a la evidencia existente + la corrección owner.

## 3. Source truth (intacta, no modificada)

- `v3/sdk/futures/domain/provider.go` leído en el baseline `7af6210a`: semántica D5 intacta — `ALLOWED|CONDITIONAL → binding enableable`; `UNKNOWN|FORBIDDEN` ⇒ error `cannot be enabled with %s automation entitlement`. El mismo predicado en `session.staticEligible()` y en los dos switches de admission (`DenyReasonEntitlementRevoked`). Sin modificaciones (worktree `git status` = 0 entradas antes y después del remediation).

## 4. ETCD DEV (única mutación)

- Clave: `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/entitlement`, `UNKNOWN` (7 bytes) → `ALLOWED` (7 bytes). Ninguna otra clave tocada.
- Herramienta efímera SDK (`v3/futures-bridge/cmd/n1r2-entitlement-fix`, cliente `etcd.New(WithApp("echo"), WithEnv("development"))` = namespace `/echo/development/` idéntico al del relay), con guardas: pre-lectura exige `UNKNOWN` (aborta sin escribir ante cualquier otro valor), `SetVar`, read-back exige `ALLOWED`. Salida: `before: UNKNOWN → after: ALLOWED → WRITE_VERIFIED`. Herramienta y binario eliminados del worktree tras la ejecución (nunca commiteados).
- Claves hermanas verificadas intactas tras la escritura (dump del writer): `enabled=true`, `provider-id=EARN2TRADE`, `program-id=GAU50`, `rule-set-id=GAU50-EVAL`, `rule-set-version=1`, `day-boundary-tz=America/New_York`, `day-boundary-reset=17:00`, `transport-id=NINJATRADER_BRIDGE`, `external-contract-identifier=NQ 12-26`.
- Read-back doble independiente: MCP ETCD RO devuelve `ALLOWED` (7 bytes) en la clave absoluta; conteo del prefijo de la cuenta = 10 keys (igual que antes; cero claves creadas o eliminadas).

## 5. Runtime (reload mínimo)

- Único proceso que relee el binding en N1: `systemd --user echo-nt-feed-relay` (Daedalus, release `7af6210a` sin rebuild — `vcs.revision=7af6210a`, `vcs.modified=false`). `systemctl --user restart` a las 13:16 -03; unidad activa, listener `*:9770`, lane de mercado operativa.
- **El error objetivo desapareció**: 0 ocurrencias de `cannot be enabled with UNKNOWN automation entitlement` en el journal del PID nuevo (1083756). El binding pasa `ProviderAccountBinding.Validate` (gate de entitlement superado en runtime).
- Estado residual de la lane de cuenta, preexistente y declarado en N1 (N1-SHOT1 E4), NO tocado por alcance: `binding_loaded=false` con `binding provider-external-account-id is empty` — la clave `futures-bridge/accounts/E2T-GAU50-01/provider-external-account-id` (identidad NT que el AddOn debe matchear) nunca existió en ETCD (10 keys antes y después) y se fija tras el discovery del AddOn en la sesión owner dev-win (OD-2). El error UNKNOWN la enmascaraba por orden de validación; ahora queda visible, que es su estado N1 declarado. Defence-in-depth hello↔binding sigue operativa (fail-closed mientras tanto; lane de mercado stream-level continúa).
- No se arrancó el execution bridge. No se instaló el AddOn. No se avanzó hacia envío de órdenes; N1 sigue read-only.

## 6. Verificación (/verify)

- `OwnerRiskAcceptance` references = **0** y `PhysicalEgressApproved` references = **0**: `git grep -e OwnerRiskAcceptance -e OwnerRiskAccepted -e PhysicalEgressApproved` @ `7af6210a` = 0 matches (menciones históricas sólo en artifacts del vault, preservados).
- `E2T entitlement` = **`ALLOWED`**, autoridad demostrada (§2).
- Binding validation = **PASS** a nivel dominio: `ProviderAccountBinding.Validate` superado por el loader real en el runtime real (error UNKNOWN eliminado; test unitarios `go test ./internal/binding/...` y `./futures/domain/...` ok). La lane de cuenta permanece fail-closed visible por la causa N1 declarada (`provider-external-account-id` pendiente de discovery owner), fuera del alcance de este remediation.
- `ORDERS_SENT = 0`, `ORDERS_MODIFIED = 0`, `ORDERS_CANCELLED = 0` — estructural: cero cambios de código, protocolo `echo.ntfeed.v1` sin familia de comandos, relay sin escritura al AddOn, AddOn no instalado, execution bridge sin arrancar. No se utilizó orden alguna para verificar el entitlement.

## 7. Historia preservada

- Los artifacts de research (`d6-earn2trade-preflight-20260930/`) NO se modifican: en su fecha (2026-09-30) el estado factual era genuinamente `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`; quedan como historia válida, superseded por la decisión/evidencia owner del 2026-10-01 para el estado vigente.
- Project note: la consecuencia bloqueante declarada en N1-R1 queda marcada superseded por la sección D6 N1-R2 añadida al final de la nota; la historia N1-R1 se preserva íntegra.

## 8. Handoff

```text
D6_N1_R2_ENTITLEMENT_CORRECTION =
PASS

PREVIOUS:
UNKNOWN

CORRECT:
ALLOWED

AUTHORITY:
Owner correction 2026-10-01 («Earn2Trade permite automatización/estrategia propia»; resuelve OD-1 de N1-R1) + criterio canónico del proyecto (Front C authoritative matrix, manager 2026-09-26: CONDITIONAL exige condiciones explícitas adjuntas al grant — Tradeify/Topstep/TradeDay/MFFU; permiso plano con sólo conducta general = ALLOWED — FundedNext/Lucid) + evidencia E2T existente sin ninguna condición documentada adjunta al grant (preflight Pass 1/2, separación copiers≠own-algorithm) + semántica interna (CONDITIONAL exige condición concreta declarada; conditions vacío)

ETCD_UPDATED:
YES

BINDING_VALID:
PASS

OLD_UNKNOWN_BLOCKER:
REMOVED

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

OWNER_DECISION_REQUIRED:
NONE

NEXT_MANAGER_ACTION:
Comunicar cierre de OD-1 (entitlement E2T-GAU50-01 = ALLOWED en ETCD DEV, blocker UNKNOWN eliminado, semántica D5 intacta) y despachar la re-verificación corta N1 pendiente, que sigue requerida para reclasificar ADDON/ACCOUNT_STATE/POSITIONS/ORDERS/NQ y requiere el lado owner OD-2 (instalación AddOn + restart NT en dev-win, que además fija provider-external-account-id — única causa restante del binding_loaded=false, declarada y fuera del alcance N1-R2). N2 sigue NOT AUTHORIZED (F1 STOP_MARKET pendiente + re-affirm owner de egress físico). No emitir N1 PASS ni D6 PASS en este remediation.
```
