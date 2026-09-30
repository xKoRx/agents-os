# Echo Futures — D6 Earn2Trade Entitlement + Rules Gap Repair — Research Pass 2

**Fecha de retrieval:** 2026-09-30
**Role:** RESEARCHER external evidence specialist
**Scope:** gap repair first-party sobre own-algorithm policy, automation/API entitlement, funded transport continuity, rule-row completeness y commercial gaps
**Accepted input:** `DEEPRESEARCH-PASS-1-E2T-EXTERNAL-EVIDENCE.md` @ Agents-OS `0f6c20fca2ebb57bc87df37870b14bc29940ec70`
**Boundary:** este artifact no selecciona arquitectura, transport, programa ni tamaño de cuenta; no reabre D5; no emite gate D6.

## 1. Resultado delta

Pass 2 no encontró evidencia pública first-party que autorice o prohíba explícitamente el caso exacto de una estrategia algorítmica propia ejecutando automáticamente sobre una sola cuenta Earn2Trade, separada de copying/mirroring. Por lo tanto, `OWN_ALGORITHMIC_TRADING` permanece `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION` en Evaluation, LiveSim® y Live.

NinjaTrader/NinjaScript, Tradovate REST/WebSocket y Rithmic R|API+/R|Protocol siguen demostrando capacidad técnica del vendor y/o disponibilidad de plataforma, pero la documentación pública no prueba el entitlement de una cuenta Earn2Trade para custom automation/direct API por stage. Los tres caminos permanecen `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION` como entitlement.

Funded continuity quedó parcialmente reparado: el partner decide si ofrece LiveSim® o Live; para NinjaTrader Live, Earn2Trade documenta que la prop crea la cuenta y entrega nuevas credenciales. No existe una garantía pública de conservar el transport de Evaluation, ni un contrato público de reprovisioning para LiveSim®, ni diferencias operativas públicas Helios/Appius suficientes para cerrar automation/API entitlement post-pass.

Las cinco filas pedidas permanecen `STILL_INCOMPLETE` como filas completas stage-by-stage. TCP50 sí obtuvo evidencia current seleccionada para Evaluation. La UI pública dinámica continúa exponiendo sólo el tab activo/default en los crawls obtenidos para TCP100 y GAU100/150/200, y no corresponde transplantar valores desde tabs vecinos, growth stages o páginas históricas.

El checkout first-party muestra `USD 100` como “Current Reset Price” para TCP25 y TCP50, pero la política oficial de reset de 2025 dice que ambos son dinámicos, ajustados por promociones y siempre inferiores al precio vigente de una nueva suscripción. Con `50PLUSRESET` activo al 2026-09-30, ambas fuentes no pueden reconciliarse públicamente; el valor mostrado es FACT, pero el precio efectivo promo-adjusted permanece `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`.

## 2. Own algorithm policy — exact separation

| Concepto | Clasificación | Evidencia pública actual | Resultado |
| --- | --- | --- | --- |
| OWN_ALGORITHMIC_TRADING | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | No existe texto first-party público encontrado que diga explícitamente “allowed” o “not allowed” para software propio que genera y envía órdenes en una sola cuenta | Evaluation UNKNOWN; LiveSim UNKNOWN; Live UNKNOWN |
| TRADE_COPYING | FACT | Earn2Trade prohíbe trade copiers en Evaluation y funded accounts | Prohibido; no se usa como proxy de own-algorithm |
| LEADER_FOLLOWER | FACT | Earn2Trade indica que las prop firms no proveen leader-follower/trade-copy y NinjaTrader Live ya no usa el antiguo leader-follower | Distinto de own-algorithm |
| ACCOUNT_MIRRORING / MULTI-ACCOUNT COORDINATION | FACT | Prohibited Conduct prohíbe colaboración/manipulación, hedging/pooling entre cuentas conectadas y trade copiers | Distinto de una sola cuenta |
| UNFAIR_ADVANTAGE_OR_MANIPULATION | FACT | Prohibited Conduct incluye software/AI/ultra-fast entry cuando podría manipular el entorno o dar ventaja injusta | No es una prohibición textual de software per se |
| AUTOMATION_OF_E2T_WEB_SERVICE | FACT | Terms prohíben programas/bots/routines para automáticamente acceder o manipular “the Service” | El Terms no explica públicamente si ese clause alcanza order automation mediante una interfaz de trading soportada |

### Stage classification

- **Evaluation:** `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`. Searched: Terms, Prohibited Conduct, Evaluation rules, platform/onboarding docs, trade-copy policy. Evidence exists for account-holder exclusivity, prohibited manipulative software and copier prohibition, but no exact authorization/denial of own automated order execution. Minimal closing question: confirm in writing whether one-account proprietary algorithmic order execution is allowed in Evaluation and how the Service bot clause applies to supported trading interfaces.
- **LiveSim®:** `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`. Searched: same corpus plus funded rules. Funded rules enumerate drawdown, DLL, position size, hours, prohibited assets and trade copiers but do not state own-algorithm permission. Minimal closing question: same, explicitly for LiveSim®.
- **Live:** `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`. Searched: same corpus plus NinjaTrader Live account access/funding docs. Live provisioning is documented, but automation policy is not. Minimal closing question: same, explicitly for Live.

A reasonable reading that the conduct rule targets manipulative/unfair uses of software rather than every use of software is only a `SUPPORTED_INTERPRETATION`; it is not promoted into an authorization.

## 3. NinjaTrader / NinjaScript entitlement

### Proven independently

- `NINJATRADER_PLATFORM_AVAILABLE = FACT` for current Earn2Trade offering. New Earn2Trade-provided NinjaTrader access uses the NinjaTrader–Tradovate unified route rather than legacy E2T-provided Rithmic.
- `NINJASCRIPT_TECHNICALLY_CAPABLE = FACT` from NinjaTrader vendor documentation already accepted in Pass 1.
- Earn2Trade Evaluation onboarding instructs the trader to log in with the Tradovate credentials and select simulated mode.

### Not proven

No public Earn2Trade source found explicitly grants a custom NinjaScript Strategy or AddOn permission to automatically place/modify/cancel orders, nor unattended/VPS/cloud execution, on an Earn2Trade account.

| Stage | E2T_NINJASCRIPT_ENTITLEMENT | Classification | Why public evidence is insufficient |
| --- | --- | --- | --- |
| Evaluation | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | Platform access and simulated login are documented; custom automation permission is not |
| LiveSim® | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | Funded platform availability is broad but custom NinjaScript entitlement is not stated |
| Live | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | NinjaTrader Live can be provisioned, but custom NinjaScript/unattended entitlement is not stated |

Minimal closing question: may the account holder run a custom NinjaScript Strategy or AddOn that automatically places/modifies/cancels orders on exactly one account, and may it run unattended/VPS/cloud, separately for Evaluation, LiveSim® and Live?

## 4. Tradovate direct REST/WebSocket entitlement

### Proven independently

- `VENDOR_CAPABILITY = FACT`: Tradovate documents direct REST/WebSocket access and automated orders; automated orders must carry `isAutomated=true`.
- Tradovate’s public retail API prerequisites say a user needs a Live account with more than USD 1,000 equity, an API Access subscription and an API key.
- `E2T_PLATFORM_SUPPORT = FACT`: Earn2Trade provisions “Tradovate Data Credentials” for Evaluation and lets the trader connect the feed to a supported platform.

### Entitlement result

| Stage | ACCOUNT/STAGE_ENTITLEMENT | Classification | Why public evidence is insufficient |
| --- | --- | --- | --- |
| Evaluation | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | E2T data credentials do not prove API Access subscription, API-key rights or an exception to Tradovate’s normal retail prerequisites |
| LiveSim® | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | No public E2T source maps LiveSim® credentials to direct developer API entitlement |
| Live | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | Tradovate vendor capability is clear; the prop-provisioned account/API-key entitlement is not publicly guaranteed |

Do not classify Evaluation as NO from the retail prerequisites: partner/B2B provisioning could differ, and no first-party E2T source publicly resolves that mapping.

Minimal closing question: do E2T-provisioned Tradovate credentials permit direct REST/WebSocket use, API-key creation/API Access, and automated orders for Evaluation, LiveSim® and Live; if Evaluation/LiveSim® are exceptions to standard Tradovate API prerequisites, how is that entitlement provisioned?

## 5. Rithmic direct R|API+ / R|Protocol entitlement

### Proven independently

- `VENDOR_CAPABILITY = FACT`: Rithmic documents R|API+, R|Protocol and R|Diamond for custom/algorithmic systems.
- Rithmic requires conformance before connecting an application to production systems including Rithmic 01 and Rithmic Paper Trading; after conformance the developer must work with an FCM/broker for live credentials and fees.
- `E2T_PLATFORM_SUPPORT = FACT`: Earn2Trade provisions Rithmic data-feed credentials for Evaluation and instructs use of Rithmic Paper Trading on supported frontends.

### Entitlement result

| Stage | ACCOUNT/STAGE_ENTITLEMENT | Classification | Why public evidence is insufficient |
| --- | --- | --- | --- |
| Evaluation | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | E2T data-feed credentials for a supported frontend do not prove authorization for a custom conformed R|API+/R|Protocol client or application ID |
| LiveSim® | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | Public E2T docs do not state custom API entitlement, FCM mapping or fees for LiveSim® |
| Live | UNKNOWN | UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION | Rithmic says live credentials/fees come through FCM/broker after conformance; no E2T stage mapping is public |

Minimal closing question: after Rithmic conformance, may an E2T account use a custom R|API+ or R|Protocol application, and what additional E2T/partner/FCM approval, application identity, credentials and fees apply in Evaluation, LiveSim® and Live?

## 6. Funded transport continuity

### FACT

- After passing, Earn2Trade verifies the evaluation and forwards it to a proprietary trading partner such as Helios Trading Partners or Appius Trading Limited; the partner offers either LiveSim® or Live.
- Current funded rules apply independently of the Evaluation rule profile.
- For NinjaTrader Live specifically, Earn2Trade says the live account is created by the prop firm and the trader receives live trading credentials directly from the prop firm. This proves reprovisioning/new credentials for that documented Live path.
- Current Earn2Trade material supports multiple platform/data paths in the broader offering; that does not create a guarantee of retaining the Evaluation binding.

### UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION

- Whether the transport chosen in Evaluation can be retained in LiveSim®.
- Whether the transport chosen in Evaluation can be retained in Live.
- Exact LiveSim® credential reprovisioning and data-provider behavior.
- Whether automation/API entitlement must be re-approved after passing.
- Partner-specific transport differences between Helios and Appius.
- Whether a direct Tradovate or direct Rithmic API entitlement, if approved during Evaluation, carries into funded stages.

Minimal closing question: for each funded stage and partner, what execution/data transports are provisioned, are credentials new, can the Evaluation transport be retained, and must custom automation/direct API permission be approved again?

The 2024 “Can I Use My Own Data Feed?” article is not promoted into a 2026 universal transport rule because it describes an older Rithmic/Helios setup that predates the current NinjaTrader–Tradovate rollout.

## 7. Program-rule gap repair

Current generic rules repaired/confirmed across the corpus: Evaluation has no minimum trading days, Evaluation uses 30% consistency, consistency does not apply to LiveSim®/Live, Evaluation and LiveSim® use EOD drawdown, Live uses trailing drawdown except TCP 200K/400K fixed drawdown, funded accounts carry DLL/progression/trading-hours rules, and all working orders/positions must be closed between 15:50 and 17:00 CT.

### TCP50

**Status: STILL_INCOMPLETE.**

Current selected-plan first-party purchase evidence repairs the Evaluation row:

| Field | TCP50 Evaluation current evidence |
| --- | --- |
| Starting balance | USD 50,000 |
| Profit target | USD 3,000 |
| EOD drawdown | USD 2,000 |
| Daily loss limit | USD 1,100 |
| Max contracts / progression | Up to 6 |
| Consistency | 30% |
| Trading hours | Trade until 15:50 CT |
| Minimum trading days | None |
| Current reset display | USD 100 |
| Max concurrent Evaluation accounts | 5 |

The current TCP product/help material proves TCP50’s growth direction to 100K, 200K and 400K, but this Pass did not obtain one current selected TCP50 LiveSim/Live rule row that supplies every requested stage-specific cell without borrowing values from another tab/stage. Therefore the complete row remains incomplete.

### TCP100

**Status: STILL_INCOMPLETE.**

Current product inventory and help prove the program exists and its growth direction to 150K, 200K and 400K. The public dynamic pages retrieved in this Pass did not expose a selected TCP100 Evaluation + LiveSim + Live row with all requested numeric cells. No values are inferred from neighboring TCP sizes or TCP growth stages.

### GAU100

**Status: STILL_INCOMPLETE.**

Current first-party pages prove GAU100 exists. Generic Evaluation/LiveSim/Live rule semantics are current. The current dynamic Gauntlet Mini page retrieved publicly exposed the selected/default GAU50 row, not a complete selected GAU100 row. Historical or neighboring values are not used.

### GAU150

**Status: STILL_INCOMPLETE.**

Current first-party pages prove GAU150 exists. Generic stage semantics are current. No complete selected GAU150 Evaluation/LiveSim/Live row was obtained from a current public tab, and historical values are not promoted.

### GAU200

**Status: STILL_INCOMPLETE.**

Current first-party pages prove GAU200 exists. Generic stage semantics are current. No complete selected GAU200 Evaluation/LiveSim/Live row was obtained from a current public tab, and historical values are not promoted.

### Rule-row closure question

Please provide/confirm the current selected Evaluation, LiveSim® and Live rows for TCP50, TCP100, GAU100, GAU150 and GAU200, including starting balance, profit/progression target, drawdown amount/type, DLL, max contracts/progression, consistency, trading hours, minimum days, payout/progression target and every stage-specific material rule.

## 8. Commercial repair

### Promotion `50PLUSRESET`

- **Promotion existence:** `FACT`. Earn2Trade’s current public site on 2026-09-30 advertises “50% OFF + a FREE Reset With Every Evaluation” with code `50PLUSRESET`.
- **Expiration date/time:** `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`. No public first-party expiration timestamp/date was found.
- **Eligibility/geography specific to the code:** `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`. General Terms eligibility exists, but no public code-specific geographic scope was found.
- **Promo free reset vs TCP rebill reset stacking:** `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION`. TCP’s normal policy grants one free reset after every monthly rebill; the promo promises a free reset “with every evaluation”; no public source says whether both entitlements stack on the same subscription.

### Reset pricing

- **TCP25:** current first-party purchase UI displays `USD 100` as “Current Reset Price” — `FACT` about the displayed value. Effective price under the active 50% promotion: `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION` because the official reset-pricing policy says TCP25 is dynamic, promotion-adjusted and always below the current new-subscription price.
- **TCP50:** current first-party selected-plan purchase UI displays `USD 100` as “Current Reset Price” — `FACT` about the displayed value. Effective price under the active 50% promotion: `UNKNOWN_REQUIRES_PROVIDER_CONFIRMATION` for the same policy conflict.
- **Source conflict:** active public promotion makes new TCP25 start at USD 75 and implies a TCP50 new-subscription price below USD 100 under a literal 50% discount, while the UI still displays USD 100 reset. The sources do not explain whether the reset display is pre-promo, whether the discount excludes resets despite the 2025 dynamic-policy wording, or whether checkout applies an adjustment later. No value is invented.

Minimal closing question: what is the promotion expiration/eligibility, is the promo free reset additional to TCP’s post-rebill free reset, and what amount is actually charged today for a TCP25/TCP50 reset while `50PLUSRESET` is active?

## 9. Pass 1 contradiction check

`PASS_1_CONTRADICTIONS = NONE`.

No accepted Pass 1 FACT is contradicted by the current Pass 2 evidence. The reset-price conflict was already explicitly tracked as unresolved in Pass 1 and remains a source-level contradiction, not a contradiction with a frozen Pass 1 fact.

Pass 1’s supersession decisions remain valid: the old ten-day minimum rule is superseded by current no-minimum-days guidance, and older Rithmic-only Evaluation transport text is not authority over the 2026 Tradovate/NinjaTrader rollout.

## 10. Minimal provider-confirmation set

1. For exactly one account at a time, with no copying/mirroring/leader-follower/hedging/synchronization, is a trader-owned algorithm that automatically generates and sends orders allowed on Evaluation, LiveSim® and Live, and how does the Terms bot/service clause apply to supported trading interfaces? Are unattended/VPS/cloud sessions allowed for that same use case?
2. For NinjaTrader–Tradovate accounts, may a custom NinjaScript Strategy or AddOn automatically place/modify/cancel orders on Evaluation, LiveSim® and Live?
3. Do E2T-provisioned Tradovate credentials permit direct REST/WebSocket access and API-key/API Access entitlement on Evaluation, LiveSim® and Live; if standard Tradovate retail prerequisites differ, how is the E2T entitlement provisioned?
4. After Rithmic conformance, may E2T credentials be used from a custom R|API+ or R|Protocol client on Evaluation, LiveSim® and Live, and what additional E2T/partner/FCM approval, application identity and fees apply?
5. After passing, which execution/data transports can each current funding partner provision for LiveSim® and Live, are credentials reprovisioned, can the Evaluation transport be retained, and must automation/API entitlement be approved again?
6. What is the expiration date/time and eligibility scope of `50PLUSRESET`, and is its free reset additional to the TCP free reset earned after a monthly rebill? While the code is active, what amount is actually charged for TCP25 and TCP50 resets?
7. Please confirm the complete current stage rows for TCP50, TCP100, GAU100, GAU150 and GAU200 using the requested rule fields.

## 11. Purchase-affecting findings

- **P0 — own-algorithm policy:** mandatory MVP behavior remains unconfirmed by public first-party policy across all three stages.
- **P0 — automation/direct transport entitlement:** no candidate custom/direct path researched has stage entitlement proven publicly. NinjaTrader platform availability, Tradovate API capability and Rithmic API capability do not close this.
- **P1 — funded continuity:** post-pass stage and some provisioning semantics are documented, but transport retention and custom automation/API entitlement continuity are not.
- **P1 commercial timing risk — promotion:** the offer is public/current on 2026-09-30, but expiry and code-specific eligibility are not public.
- **P2 commercial economics — resets:** USD 100 is the current displayed reset value for TCP25/TCP50, but effective promo-adjusted charge and reset stacking remain unresolved because first-party sources conflict/omit the interaction.

## 12. First-party source register

### Earn2Trade policy and funded lifecycle

- https://www.earn2trade.com/terms-and-conditions
- https://help.earn2trade.com/en/articles/9286647-prohibited-conduct-in-earn2trade-evaluations-and-in-the-livesim-live-trading-environment
- https://help.earn2trade.com/en/articles/5660666-can-i-have-multiple-trader-career-path-gauntlet-mini-and-live-livesim-accounts
- https://help.earn2trade.com/en/articles/6877364-what-happens-when-i-complete-my-evaluation
- https://help.earn2trade.com/en/articles/13460913-ninjatrader-live-account-access

### Earn2Trade platform/onboarding

- https://help.earn2trade.com/en/articles/15359154-ninjatrader-access-at-earn2trade
- https://help.earn2trade.com/en/articles/4473826-how-to-connect-tradovate-to-ninjatrader
- https://help.earn2trade.com/en/articles/14196947-how-do-i-set-up-my-tradovate-evaluation
- https://help.earn2trade.com/en/articles/6911655-how-do-i-set-up-my-rithmic-evaluation

### Earn2Trade rules/commercial

- https://www.earn2trade.com/
- https://www.earn2trade.com/trader-career-path
- https://www.earn2trade.com/gauntlet-mini
- https://www.earn2trade.com/pt/india/purchase?plan=TCP50
- https://help.earn2trade.com/en/articles/5941958-what-are-the-evaluation-rules
- https://help.earn2trade.com/en/articles/11183609-reset-pricing-for-earn2trade-accounts
- https://help.earn2trade.com/en/articles/6863801-do-you-provide-free-resets
- https://help.earn2trade.com/en/articles/6863807-what-is-the-difference-between-the-tcp25-tcp50-and-tcp100

### Vendor entitlement boundaries

- https://api.tradovate.com/
- https://www.rithmic.com/apis
- https://www.rithmic.com/products/exchange-simulator
- NinjaTrader developer documentation already accepted as vendor-capability evidence in Pass 1; no vendor capability is promoted into E2T entitlement here.

## 13. Reuse delta

`REUSABLE_ASSETS_DELTA`: extend the provider-rule provenance matrix with the selected dynamic-UI state, at minimum `selected_plan` and `selected_stage`, so a crawl of the default tab cannot be mistaken for evidence about a neighboring size/stage.

`REUSABLE_BEHAVIOR_CANDIDATES`: for dynamic rule/pricing UIs, evidence is selection-scoped. A selector proving that a plan exists does not prove the row behind that plan, and values from the default tab, a growth stage or a historical crawl must not be transplanted into another plan/stage.

This is additional to the existing capability/offering/account-entitlement triad; it does not restate it.

## 14. Closeout discipline

- `agents-os-agent-run-register`: SKIPPED — this execution is documentation/web research only and contains no material coding/debug/review/testing segment covered by the trigger.
- `agents-os-session-feedback`: SKIPPED — no qualifying AGENTS OS friction, degraded retrieval or Sistema 1 gap occurred.
- `agents-os-session-close`: explicit close is required by the one-shot mandate. Delta classification is satisfied by this research artifact; no L0/L1, internal checkpoint or additional memory artifact is warranted.
- No secrets or chain-of-thought are persisted.
- No D6 gate is emitted.
