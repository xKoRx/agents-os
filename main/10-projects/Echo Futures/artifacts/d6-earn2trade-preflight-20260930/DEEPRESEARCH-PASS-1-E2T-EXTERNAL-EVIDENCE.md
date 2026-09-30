# Echo Futures — D6 Earn2Trade External Evidence Corpus — DeepResearch Pass 1

**Fecha de retrieval:** 2026-09-30
**Role:** DEEPRESEARCH external evidence specialist
**Scope:** Earn2Trade current first-party rules, automation policy, platform/transport capability, stage/account entitlement
**Internal baseline:** Echo Futures D5 CLOSED_BY_OWNER; xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d; ATP 113 PASS / 0 FAIL / 0 INCOMPLETE / 2 DEFERRED_TO_D6; S12 13/13; provider-first target Earn2Trade; one Earn2Trade account active at a time.
**Research boundary:** This artifact does not select an Echo architecture or execution adapter, does not reopen D5, and does not emit a D6 gate.

## 1. Baseline / Context Capsule

The frozen internal context is treated as authority and is not re-researched here: Strategy remains provider-agnostic; GerardMM remains provider-agnostic; ProviderRuleSet contains the complete read-only provider policy consumed by MM; provider_rules(account_id) is the final account-wide authority; only one Earn2Trade account is active at a time for this MVP; Echo Futures is not a leader/follower trade copier; no provider-specific Strategy, Earn2TradeGerardMM, generic rule DSL, or generic broker/plugin framework is introduced; D5 is not redesigned.

Owner economics SL USD 2000 and TP USD 1500 are internal configuration and are explicitly excluded from Earn2Trade policy classification.

## 2. Source freshness register

| Authority | Source | Source date/update shown | Retrieved | Current-use classification |
| --- | --- | --- | --- | --- |
| Earn2Trade | Home / program landing | current site | 2026-09-30 | CURRENT |
| Earn2Trade | Terms and Conditions | current legal page | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | What Are the Evaluation Rules? | 2026-07-06 | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | What Happens When I Complete My Evaluation? | 2026-07-06 | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | Drawdown types | 2026-08-10 | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | Maintain Consistency | 2026-05-07 | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | Platforms for GM/TCP | 2026-08-13 | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | NinjaTrader Access at Earn2Trade | 2026-06-05 | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | Live/LiveSim fee structure | 2026-07-06 | 2026-09-30 | CURRENT |
| Earn2Trade Help Center | Reset pricing | 2025-05-08 | 2026-09-30 | CURRENT unless checkout conflicts |
| Tradovate | Official API docs | current API docs | 2026-09-30 | CURRENT |
| NinjaTrader | Official NinjaScript developer docs | current docs | 2026-09-30 | CURRENT |
| Rithmic | Official API suite / Exchange Simulator | current product docs | 2026-09-30 | CURRENT |
| Earn2Trade | Older TCP explainer / old data-feed help | older than newer Help Center authorities | 2026-09-30 | SUPERSEDED where contradicted |

All dynamic prices, promotion terms, account availability and platform availability below are stamped with retrieval date 2026-09-30.

## 3. Current Earn2Trade program inventory

### Trader Career Path®

Current first-party inventory exposes TCP25, TCP50 and TCP100. Base monthly evaluation prices exposed by the current first-party checkout are USD 150, USD 190 and USD 350 respectively. Earn2Trade currently advertises a Labor Day promotion of 50% off plus one free reset with every evaluation using code 50PLUSRESET. The home page advertises TCP “From USD 75”, directly confirming the discounted floor. The exact TCP50 and TCP100 discounted amounts are arithmetic implications of the advertised 50% discount, not separately rendered in the retrieved neutral checkout, so USD 95 and USD 175 are SUPPORTED_INTERPRETATION rather than independent price FACTs. No explicit promotion expiration timestamp was found.

TCP funded progression is current first-party: TCP25 can progress through 25K funded → 50K → 100K → 200K; TCP50 can progress to 100K → 200K → 400K; TCP100 can progress to 150K → 200K → 400K. The top TCP 200K/400K funded stages use fixed drawdown rather than trailing drawdown.

TCP includes one free reset after each successful monthly rebill while the subscription remains active. The current site-wide promotion additionally advertises one free reset with every evaluation; public evidence does not explicitly explain whether that promotional reset is additive to the post-rebill TCP reset.

### The Gauntlet Mini™

Current first-party inventory exposes GAU50, GAU100, GAU150 and GAU200. Current base prices from first-party checkout are USD 170, USD 315, USD 375 and USD 550. A current first-party checkout carrying the active 50% banner rendered promotional prices USD 85, USD 157.50, USD 187.50 and USD 275, and GAU50 reset price USD 75.

Current reset help states fixed reset prices for GAU100 USD 100, GAU150 USD 130 and GAU200 USD 155. GAU50 reset pricing is dynamic with active promotions. Exact current GAU50 public checkout evidence is USD 75 on the 50% promotion.

The current program page fully exposes the GAU50 Evaluation, LiveSim and Live rule rows. The current page proves GAU100/150/200 are offered, but this pass did not obtain complete per-stage rule rows for those three dynamic tabs. Their existence and prices are FACT; any per-size rule value not directly captured remains UNKNOWN in this corpus rather than inferred from historical tables.

## 4. Candidate account matrix

No candidate is ranked or selected here.

| Program | Size | Current offer | Base price | Current promo | Evidence completeness for stage rules | Material notes |
| --- | ---: | --- | ---: | ---: | --- | --- |
| TCP | 25K | YES | USD 150/mo | USD 75 floor directly advertised | HIGH | Eval, LiveSim, Live and growth stages captured |
| TCP | 50K | YES | USD 190/mo | USD 95 derived from current 50% offer | MEDIUM | Current existence/growth/base risk values supported; complete selected-tab stage row not independently captured |
| TCP | 100K | YES | USD 350/mo | USD 175 derived from current 50% offer | MEDIUM | Current existence/growth/base risk values supported; complete selected-tab stage row not independently captured |
| Gauntlet Mini | 50K | YES | USD 170/mo | USD 85 directly rendered | HIGH | Eval, LiveSim and Live rows captured |
| Gauntlet Mini | 100K | YES | USD 315/mo | USD 157.50 directly rendered | LOW-MEDIUM | Offered/current price proven; exact current stage-rule row still needs direct tab capture |
| Gauntlet Mini | 150K | YES | USD 375/mo | USD 187.50 directly rendered | LOW-MEDIUM | Offered/current price proven; exact current stage-rule row still needs direct tab capture |
| Gauntlet Mini | 200K | YES | USD 550/mo | USD 275 directly rendered | LOW-MEDIUM | Offered/current price proven; exact current stage-rule row still needs direct tab capture |

Material MVP candidates with the strongest complete current rule evidence in this pass are TCP25 and GAU50. This is an evidence-completeness statement, not an architectural or purchase recommendation.

## 5. Stage/rule matrix

| Rule | Evaluation | LiveSim® | Live |
| --- | --- | --- | --- |
| Environment | Simulated/virtual evaluation with real market data | Simulated account with live market data | Real funded/live account |
| Drawdown type | End-of-Day drawdown | End-of-Day drawdown | Trailing drawdown |
| TCP top growth exception | N/A | N/A | TCP 200K/400K fixed drawdown |
| Daily Loss Limit | YES | YES | YES |
| Daily loss PnL | Open/unrealized + closed + commissions; 5pm–5pm CT | Funded rules state DLL applies | Funded rules state DLL applies |
| Progression / max size | Applies; exceeding max is hard fail | Applies; hard fail | Applies; hard fail |
| Consistency | 30%; must be below 30% of total PnL for any single day | NO | NO |
| Minimum trading days | NONE | NONE | NONE |
| News trading | Allowed | Allowed | Allowed |
| Overnight | Positions and working orders must be flat during restricted close window | Flat 15:50–17:00 CT | Flat 15:50–17:00 CT |
| General close window | Current evaluation timing rules include exchange-specific windows; general flatten by 15:50 CT | 15:50–17:00 CT | 15:50–17:00 CT |
| Funded simultaneous accounts | N/A | Up to 3 program accounts by published funded rules | Only 1 Live account |
| Trade copiers | PROHIBITED | PROHIBITED | PROHIBITED |
| Monthly E2T subscription | Evaluation renews on subscription cadence until pass/cancel | No E2T monthly subscription | No E2T monthly subscription |
| Data/activation | Non-pro evaluation data included | Non-pro USD 139 activation deducted from first profitable withdrawal; pro USD 140/mo/exchange | Data USD 140/mo/exchange Rithmic or USD 156/mo/exchange NinjaTrader; calendar-month, not prorated |
| Funded partner | N/A | Partner such as Helios Trading Partners or Appius Trading Limited | Partner such as Helios Trading Partners or Appius Trading Limited |

### Concrete current rows captured

TCP25 Evaluation: start USD 25,000; profit target USD 1,750; EOD drawdown USD 1,500; daily loss USD 550; progression up to 3 contracts; 30% consistency; general approved time through 15:50 CT; max concurrent evaluations 5; no minimum days; news allowed.

TCP25 LiveSim: start USD 25,000; profit target to advance USD 1,750; EOD drawdown USD 1,500; daily loss USD 550; up to 3 contracts; profit split 50% below USD 1,500 and 80% above USD 1,500; max concurrent funded accounts shown 3; no consistency/minimum-days/buffer requirement; weekly payouts; news allowed.

TCP25 Live: start USD 25,000; profit target to advance USD 1,750; trailing drawdown USD 1,500; daily loss USD 550; up to 3 contracts; same split; max concurrent Live 1; no consistency/minimum-days/buffer requirement; weekly payouts; news allowed.

GAU50 Evaluation: start USD 50,000; profit target USD 3,000; EOD drawdown USD 2,000; daily loss USD 1,100; progression up to 6 contracts; 30% consistency; general approved time through 15:50 CT; max concurrent evaluations 5; no minimum days; news allowed.

GAU50 LiveSim: start USD 50,000; EOD drawdown USD 2,000; daily loss USD 1,100; up to 6 contracts; split 50% below USD 2,250 and 80% above USD 2,250; max concurrent funded accounts shown 3; no consistency/minimum-days/buffer requirement; weekly payouts; news allowed.

GAU50 Live: start USD 50,000; trailing drawdown USD 2,000; daily loss USD 1,100; up to 6 contracts; same split; max concurrent Live 1; no consistency/minimum-days/buffer requirement; weekly payouts; news allowed.

### Instruments and trading windows

Evaluation participants may trade futures listed on CME, COMEX, NYMEX and CBOT. Earn2Trade states stocks, options, Forex, cryptocurrency and CFDs are not permitted/available in the evaluation program/platforms. Current funded rules separately prohibit Forex, Bitcoin futures and Ether futures.

The current evaluation-hours article establishes a general 15:50 CT flattening window and additional exchange/product windows, including earlier livestock and grain windows. Therefore runtime policy cannot be reduced to a single generic “15:50 CT” close for every instrument without instrument/session-specific evidence.

## 6. Exact drawdown semantics

### Evaluation / LiveSim — End-of-Day Drawdown

Classification: FACT.

The minimum balance starts at starting balance minus the drawdown amount. Positive end-of-day account balance performance ratchets that minimum balance upward dollar-for-dollar, but only when the EOD watermark is processed after market close. A lower later EOD balance does not lower the watermark. The threshold stops rising once the minimum balance reaches the original starting balance.

Open equity still matters intraday for rule enforcement: if unrealized/open losses take account equity to or below the already-established minimum account balance, the account fails even though the watermark itself is only advanced at EOD.

Rithmic processing of the uploaded minimum balance normally occurs during the 4–5pm CT market-close interval, so dashboard and R Trader Pro Auto Liquidate Threshold may temporarily diverge.

Operational classification: balance/EOD-watermark based for ratchet calculation; open equity participates in breach detection; threshold moves only upward; never retreats; stops at starting balance.

### Live — Trailing Drawdown

Classification: FACT.

The threshold is pegged to positive performance intraday and advances dollar-for-dollar as positive account performance increases. Earn2Trade explicitly says trailing rules use both closed and open equity intraday. The threshold can therefore advance from unrealized gains before the position closes. It never retreats on later losses and stops advancing once it reaches the original starting balance; it does not trail above starting balance.

Operational classification: intraday trailing; open and closed equity included; positive unrealized PnL can advance the threshold; monotonic upward only; cap at starting balance.

### TCP top growth stages — Fixed Drawdown

Classification: FACT.

Fixed drawdown is a static minimum balance that does not change. It applies exclusively to TCP funded 200K/400K top stages. Current TCP25 growth page explicitly shows 200K minimum fixed at USD 194,000. Current Help Center identifies 400K top stages for TCP50/TCP100 as fixed.

## 7. Automation-policy evidence

Central question: Can a trader execute a proprietary automated algorithmic strategy on exactly one Earn2Trade account, without copying/mirroring trades between accounts?

Result: UNKNOWN under public first-party policy; worker synthesis status AMBIGUOUS.

Evidence supporting technical/educational compatibility: Earn2Trade first-party educational material discusses more advanced traders using automated trading systems to execute predefined criteria. Earn2Trade currently supports automation-capable platforms/transports including NinjaTrader, Tradovate and Rithmic-based platforms. Tradovate vendor API explicitly distinguishes automated orders. NinjaTrader officially supports automated NinjaScript Strategies. Rithmic explicitly markets its APIs for algorithmic trading systems.

Evidence preventing CONFIRMED status: Earn2Trade Terms prohibit programs/bots/routines used to automatically access or manipulate the E2T “Service”; the legal text does not explicitly carve supported trading-platform automation out of this clause. The same Terms also separately prohibit trade copiers and multiple forms of manipulation/unfair-advantage conduct. No current first-party Earn2Trade rule or Help Center article found in this pass says unambiguously: “you may run your own algorithmic strategy on one Earn2Trade Evaluation/LiveSim/Live account.”

Because platform technical automation capability is not provider policy entitlement, this corpus does not infer permission.

## 8. Algorithmic trading vs copying/prohibited-conduct matrix

| Behavior | Current public status | Classification | Evidence boundary |
| --- | --- | --- | --- |
| OWN_ALGORITHMIC_STRATEGY on one account | UNKNOWN | UNKNOWN | Vendor capability + E2T educational material exist, but no unambiguous E2T program permission |
| TRADE_COPYING across accounts | NOT ALLOWED | FACT | E2T Help Center 2026-06-22 and Terms explicitly prohibit trade copiers on all programs |
| LEADER_FOLLOWER copying | Not an authorized workaround | FACT / SUPPORTED_INTERPRETATION | Copying prohibition applies regardless of mechanism; current NinjaTrader Live page says old leader/follower mechanism is no longer used |
| ACCOUNT_MIRRORING | NOT ALLOWED when it is trade copying | FACT | Falls under explicit copier prohibition |
| Coordinated identical trading / pooling risk between multiple parties/accounts | Prohibited conduct where covered by Terms | FACT | Terms prohibit collaborative/manipulative conduct designed to evade rules or pool risk |
| Exploiting latency/platform errors | Prohibited | FACT | Terms prohibited conduct |
| Credential sharing / another person trading account | Prohibited | FACT | Account holder is sole authorized user |
| Software/AI/ultrafast techniques used to manipulate environment or obtain unfair advantage | Prohibited | FACT | Terms prohibited conduct |
| VPS/cloud/unattended own algo execution | No current explicit public rule found | UNKNOWN | Must not be inferred from API capability |

Trade copying and own-algorithm execution are materially different questions. Public E2T evidence conclusively answers copying, but not the central one-account own-algorithm question.

## 9. Current platform/transport inventory

Current Evaluation platforms listed by Earn2Trade: NinjaTrader, Finamark, R Trader/R Trader Pro, Tradovate, TradingView, BlackArrow One, Inside Edge Trader, Investor RT, Motive Wave, MultiCharts, Bookmap, Photon, QScalp, QSI, ScalpTool, Trade Navigator, Volfix, Jigsaw, ATAS, Sierra Chart and Quantower. NinjaTrader, Finamark, R Trader/R Trader Pro, Tradovate, TradingView and BlackArrow are explicitly listed free during evaluation; others generally require the user’s own license unless noted.

Current transport changes are material: for new subscriptions, Earn2Trade-provided NinjaTrader access is through the NinjaTrader–Tradovate unified API. Legacy Earn2Trade-provided NinjaTrader/Rithmic access was only honored through June 30, 2026. A user with a personal NinjaTrader license that includes Rithmic integration may still use Rithmic with NinjaTrader, but that is distinct from the current E2T-provided route.

Primary automation-capable transport candidates researched in depth, without selecting one: NinjaTrader Desktop over E2T’s NinjaTrader–Tradovate connection; direct Tradovate REST/WebSocket API; direct Rithmic R|API+/R|Protocol API. R Trader Pro is a supported frontend and operational failsafe, but is not itself treated here as Echo’s API.

## 10. Transport technical capability matrix

| Capability | NinjaTrader / NinjaScript | Tradovate REST + WebSocket | Rithmic R|API+ / R|Protocol |
| --- | --- | --- | --- |
| Vendor automation exists | YES | YES | YES |
| Relationship to E2T | Free Eval option; new E2T path via Tradovate | Free Eval platform/feed option | E2T Rithmic credentials/platform option |
| Auth model | NinjaTrader connection login; E2T current route uses Tradovate credentials | API key/access token or OAuth; Bearer/WebSocket authorization | Rithmic credentials after environment/FCM provisioning; dev kit + conformance process |
| Realtime market data | YES via connected provider | YES via market-data WebSocket/subscriptions, subject entitlement | YES; normalized live market data |
| Historical data | Platform facilities exist; exact transport-history entitlement varies | Chart/history endpoints exist | Tick history advertised back to Dec 2011, weekly 40GB/user |
| Account state | Account object/events expose account items | Account/cash/position/user sync entities | Platform exposes order/risk/account infrastructure; exact account API objects vendor-documented |
| Positions | YES | YES | YES |
| Working orders | YES | YES | YES |
| Order updates | YES OnOrderUpdate / Account events | YES WebSocket user sync | YES execution/order management callbacks/messages |
| Fills/executions | YES; partial fills explicitly produce multiple executions | YES fills/executions | YES execution reports |
| MARKET | YES | YES | YES |
| LIMIT | YES | YES | YES |
| STOP | YES | YES | YES |
| STOP LIMIT | YES in platform order model | YES StopLimit enum | API supports advanced/order primitives; exact API-specific method differs |
| Cancel | YES CancelOrder | YES cancelorder | YES |
| Modify/replace | YES ChangeOrder | YES modifyorder | YES order management |
| Bracket/OCO | YES | YES OCO/OSO/multibracket | YES server-side bracket/OCO |
| Partial fills | YES explicitly | YES via fills/executions | YES via execution reports |
| Client order identity | Strategy/order objects and order IDs; custom signal semantics available | clOrdId optional plus server orderId | API order identifiers/client correlation available; exact persistent-field contract must be frozen from chosen API spec |
| Fill identity | executionId + orderId | fill/execution entity IDs | execution report identity |
| Reconnect | Strategy ConnectionLossHandling/restart controls | Reconnect WebSocket + resync user state | Session/reconnect behavior API-specific; test/conformance needed |
| Recover open state | Account order/position collections/events | user/syncrequest and list/query endpoints | API order/account state mechanisms; exact recovery contract needs chosen API docs |
| Demo/sim | Sim101/Playback + E2T simulated Evaluation | demo.tradovateapi.com exists; E2T Evaluation is simulated but API entitlement separate | Rithmic Test and Exchange Simulator exist; E2T evaluation uses Rithmic Paper Trading credentials |
| Numeric rate limits | No relevant fixed local NinjaScript rate limit found | API can return throttling errors; exact numeric policy not captured | No current numeric throttling limit captured in public page |
| Certification | No separate NinjaScript vendor conformance identified | API access subscription/key prerequisites | Rithmic conformance mandatory before production systems, including Paper Trading, for custom API app |

### NinjaTrader identity/recovery notes

OnExecutionUpdate provides executionId, orderId, fill quantity/price and supports multiple executions for partial fills. CancelOrder is explicitly asynchronous: an order can fill or partial-fill after cancel request and before exchange cancellation. ChangeOrder amends working orders. Strategies expose ConnectionLossHandling and restart controls. These are technical capabilities only and do not prove E2T permission for custom NinjaScript automation.

### Tradovate identity/recovery notes

The official API exposes user synchronization over WebSocket so a client can receive initial and subsequent account/user-related state. Order placement accepts client correlation fields and returns server order identity. The API exposes order, fill/execution, position and account entities. Access tokens authorize HTTP/WebSocket sessions. Exact stable-ID guarantees across all reconnect edge cases should be verified against the selected API endpoints during implementation; no stronger provider-specific guarantee is inferred here.

### Rithmic identity/recovery notes

Rithmic advertises normalized order management and execution reporting across its API suite, server-side OCO/bracket/trailing behavior and production-like test environments. Production use of a custom API application requires conformance. Exact message/identifier and recovery contracts depend on which API flavor is chosen and are not frozen by this research.

## 11. API/automation entitlement matrix

The fields below intentionally separate platform support, API existence and actual Earn2Trade account entitlement.

| Transport | PLATFORM_SUPPORTED | API_EXISTS | API_AUTOMATION_ENTITLEMENT_CONFIRMED | Evaluation | LiveSim | Live | Main gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NinjaTrader Desktop + NinjaScript via E2T NinjaTrader–Tradovate | YES | YES, in-platform NinjaScript automation mechanism | UNKNOWN | Platform/account access YES; custom automation entitlement UNKNOWN | UNKNOWN | NinjaTrader Live may be provisioned; custom automation entitlement UNKNOWN | E2T never explicitly authorizes custom NinjaScript strategy on account |
| Direct Tradovate REST/WebSocket | YES as platform/feed | YES | UNKNOWN | E2T Tradovate credentials YES; direct API key entitlement UNKNOWN | UNKNOWN | UNKNOWN | Tradovate’s published developer access prerequisites are not shown as satisfied by E2T accounts |
| Direct Rithmic R|API+ / R|Protocol | YES as Rithmic transport/platform family | YES | UNKNOWN | E2T Rithmic Paper Trading credentials YES for supported frontends; direct custom API entitlement UNKNOWN | UNKNOWN | Rithmic is an E2T Live data path; direct API entitlement UNKNOWN | Rithmic conformance + FCM/broker credentials + E2T permission not publicly proven |
| R Trader / R Trader Pro | YES | N/A as Echo API surface in this research | N/A | YES | stage-specific frontend entitlement not fully enumerated | Rithmic-funded path exists | Frontend support is not direct API entitlement |

### Tradovate entitlement gap

The Tradovate developer documentation captured in this pass describes developer API access as requiring the appropriate Tradovate account/API-access setup and API key. Earn2Trade proves that Evaluation customers can receive Tradovate data credentials and use a simulated account, but public E2T evidence does not prove that those credentials include developer API access or API-key creation rights. Therefore API_AUTOMATION_ENTITLEMENT_CONFIRMED remains UNKNOWN.

### Rithmic entitlement gap

Rithmic proves that its APIs exist and that a custom application must pass conformance before connecting to production systems, including Rithmic Paper Trading, then obtain applicable broker/FCM credentials. Earn2Trade proves that Evaluation users can receive Rithmic Paper Trading credentials for supported platforms. Neither side’s public documentation found here proves that the E2T-issued credentials are enabled for a customer’s conformed direct API application. Therefore entitlement remains UNKNOWN.

### NinjaTrader entitlement gap

NinjaTrader proves that custom strategies can automatically submit, modify and cancel orders and consume order/execution/account updates. Earn2Trade proves NinjaTrader is a current supported platform through its Tradovate route. No E2T page found here explicitly grants use of a custom automated NinjaScript Strategy/AddOn. Therefore entitlement remains UNKNOWN.

## 12. Demo/evaluation/sim/live environment matrix

| Layer | Environment | Evidence | Entitlement status |
| --- | --- | --- | --- |
| Earn2Trade | Evaluation | Virtual/simulated account with real market data | CONFIRMED |
| Earn2Trade | LiveSim® | Simulated capital with live market data and withdrawals | CONFIRMED |
| Earn2Trade | Live | Real funded/live account | CONFIRMED, but offered by funding partner and not guaranteed to be the user-selected stage |
| NinjaTrader | Sim101 / simulated mode | Vendor supports simulation; E2T NinjaTrader Evaluation instructs simulated mode | CONFIRMED platform capability |
| Tradovate | demo.tradovateapi.com | Vendor API simulation environment | CONFIRMED vendor capability; E2T direct API entitlement UNKNOWN |
| Rithmic | Rithmic Test | Development/test environment, no conformance required to develop | CONFIRMED vendor capability |
| Rithmic | Exchange Simulator / Paper Trading | Production-like simulated environment | CONFIRMED vendor capability; custom API requires conformance for production systems |
| E2T + Rithmic | Rithmic Paper Trading Chicago Area Non-Aggregated | E2T Evaluation credentials/current onboarding | CONFIRMED frontend/account connection |
| E2T funded | LiveSim/Live transport selection | Partner may offer LiveSim or Live | CONFIRMED stages; exact transport continuity/choice UNKNOWN |

## 13. Authentication/onboarding requirements

### Earn2Trade Tradovate / NinjaTrader route

After purchase, Earn2Trade provisions “Tradovate Data Credentials”. The user must accept Tradovate exchange agreements. For NinjaTrader Desktop, those Tradovate credentials are used to log in/connect, and during Evaluation the user selects simulated account mode. Since June 2, 2026, new E2T NinjaTrader access uses the NinjaTrader–Tradovate unified route; new subscriptions must select that option during signup.

### Earn2Trade Rithmic route

Earn2Trade sends “Rithmic Data Feed Credentials Created”; the user accepts Rithmic exchange agreements and connects to the designated Rithmic Paper Trading Chicago-area non-aggregated server. E2T onboarding exposes both the evaluation account and a separate sim/practice account in R Trader Pro.

### Tradovate direct API

Vendor API uses access tokens/API-key or OAuth flows and WebSocket authorization. Session renewal/re-authentication is part of the API lifecycle. E2T’s ordinary Tradovate data credentials are not sufficient proof of API-key entitlement.

### Rithmic direct API

Developer must obtain a dev kit, develop on Rithmic Test, pass conformance for production/Paper systems and then obtain the necessary live/FCM/broker credentials and fees. The exact mapping from an E2T account to a conformed client is UNKNOWN.

No real secrets, credentials or tokens are stored in this artifact.

## 14. Rejected/superseded evidence

- SUPERSEDED: older Earn2Trade TCP explanatory material stating a minimum of 10 trading days. Current July 6, 2026 Evaluation Rules and current program pages explicitly state no minimum trading days.
- SUPERSEDED_FOR_CURRENT_TRANSPORT: older Help Center material stating evaluations are Rithmic-only. Current 2026 Earn2Trade platform/onboarding documentation proves Tradovate and NinjaTrader–Tradovate availability.
- SUPERSEDED: legacy Earn2Trade-provided NinjaTrader/Rithmic route for new subscriptions. Current Help Center says legacy connection was honored only through June 30, 2026; new E2T NinjaTrader access is NinjaTrader–Tradovate.
- REJECTED_FOR_GENERAL_PROMO: affiliate-specific first-party checkout pages showing discounts other than the current site-wide 50% promotion. They prove base prices but do not override current public 50PLUSRESET terms.
- REFERENCE_ONLY: historical funding-partner names or platform defaults that conflict with the July 2026 current completion article naming partners such as Helios Trading Partners or Appius Trading Limited.

## 15. Contradictions

### C1 — E2T bot clause vs automation-capable trading ecosystem

Current Terms prohibit bots/routines used to automatically access or manipulate the E2T Service. E2T first-party educational material discusses automated trading systems, and E2T supports platforms whose vendors explicitly support algorithms. The public corpus does not resolve whether the Terms clause targets automation of the E2T website/service layer or also a customer’s supported trading-interface automation. Classification: UNRESOLVED; central support question required.

### C2 — Dynamic reset help vs checkout reset display

Current reset-help policy says TCP25/TCP50/GAU50 reset prices are dynamic with promotions and always below the current subscription price. A neutral TCP25 checkout parser displayed USD 100 while the site-wide discounted TCP25 floor is USD 75, which cannot both satisfy “reset below current subscription” at face value. A current 50%-promo GAU50 checkout displayed reset USD 75. Classification: current TCP25/TCP50 exact reset price UNKNOWN until checkout/support clarification.

### C3 — LiveSim “option” language vs partner assignment

LiveSim article calls LiveSim an optional intermediary but also says the prop firm may decide to provide Live instead; the current completion article says the partner will offer either LiveSim or Live. Classification: not a technical contradiction after normalization; stage outcome is partner-controlled/not guaranteed to be user choice.

### C4 — Old 10-day rule vs current no-minimum-days rule

Resolved as superseded. Current July/August 2026 authorities control.

### C5 — Old Rithmic-only evaluation feed vs current Tradovate rollout

Resolved as superseded. Current 2026 platform/onboarding authorities control.

## 16. UNKNOWNs

- Whether E2T explicitly permits a user’s own automated algorithmic strategy on exactly one Evaluation account.
- Whether that permission differs for LiveSim and Live.
- Whether unattended/self-hosted/VPS execution is permitted when only the account holder controls the strategy.
- Whether an E2T NinjaTrader–Tradovate account may run a custom NinjaScript Strategy or AddOn.
- Whether E2T-issued Tradovate credentials include direct REST/WebSocket developer API entitlement and API-key creation.
- Whether E2T-issued Rithmic credentials may be used by a conformed R|API+/R|Protocol client rather than only supported frontends.
- Exact funded transport availability/continuity for each partner and whether Evaluation transport can be retained in LiveSim/Live.
- Exact 50PLUSRESET expiration timestamp/date.
- Exact TCP25/TCP50 reset price under the current active promotion due help/checkout conflict.
- Whether the promotional free reset is additive to the TCP reset earned after monthly rebill.
- Exact current complete stage-rule rows for GAU100/GAU150/GAU200 were not captured from the dynamic tabs in this pass.
- Numeric rate/throttle limits for the specific candidate runtime path remain unproven where vendors do not expose a public fixed number.
- Exact API identifier/recovery semantics for the ultimately selected Rithmic API flavor remain to be documented if that path survives entitlement review.

## 17. Exact support questions

1. I will trade exactly one Earn2Trade account at a time with my own algorithmic strategy, under my own control, and I will not copy, mirror, leader/follow, hedge, or coordinate trades with any other account. Is automated order generation and execution by my own software permitted on (a) Evaluation, (b) LiveSim®, and (c) Live? Please confirm in writing and identify any stage-specific restrictions.
2. How should the Terms clause prohibiting programs/bots that automatically access or manipulate the Service be interpreted for a user’s own automated trading strategy running through an Earn2Trade-supported trading platform or API? Does it prohibit algorithmic order execution itself, or only automation that accesses/manipulates Earn2Trade’s site/service outside supported trading interfaces?
3. For an Earn2Trade Evaluation using the NinjaTrader–Tradovate option, may I run a custom NinjaScript Strategy or NinjaScript AddOn that automatically places, modifies and cancels orders on that one evaluation account?
4. Do the Tradovate credentials provisioned by Earn2Trade permit direct use of Tradovate’s REST/WebSocket developer API? If yes, how is API Access/API-key entitlement provisioned for the Earn2Trade Evaluation account when the normal Tradovate developer-access prerequisites may differ from an evaluation account?
5. Do the Rithmic credentials provisioned by Earn2Trade permit direct R|API+ or R|Protocol API access after Rithmic conformance, or are they limited to approved front-end trading platforms? If API access is allowed, what additional approval, fee, FCM mapping or permission is required for Evaluation, LiveSim® and Live?
6. After passing, which execution/data transports can the proprietary trading partner provision for LiveSim® and for Live? Can the trader retain the same transport selected during Evaluation, and does this differ between Helios Trading Partners and Appius Trading Limited?
7. Are unattended/self-hosted execution, VPS/cloud execution or remote sessions permitted for a user’s own algorithmic strategy, provided credentials remain private and only the account holder controls the strategy?
8. What is the expiration date/time and eligibility scope of promotion code 50PLUSRESET, and is the advertised free reset on each purchased evaluation additional to the TCP free reset earned after each monthly rebill?
9. Under the current 50PLUSRESET promotion, what are the exact current reset prices for TCP25 and TCP50?
10. Please confirm the current Evaluation, LiveSim and Live rule rows for GAU100, GAU150 and GAU200, including profit target where applicable, drawdown amount/type, daily loss limit and maximum contracts.

## 18. Purchase-affecting findings

### P0 — Automation policy ambiguity

The core MVP usage pattern is not publicly authorized with enough precision to classify as CONFIRMED. Trade copying is explicitly prohibited, but own-algorithm single-account execution is not equivalently documented. This is a purchase-affecting blocker if algorithmic automation is mandatory.

### P0 — Direct API entitlement not demonstrated

Tradovate and Rithmic expose strong technical APIs, and NinjaTrader exposes a strong in-platform automation surface. None of those vendor capabilities proves that an E2T Evaluation/LiveSim/Live user receives the necessary direct API/automation entitlement. This is a purchase-affecting blocker until the intended transport has stage-specific entitlement proof.

### P1 — Funded transport continuity unknown

After passing, a funding partner offers LiveSim or Live and may provision different credentials/data paths. Public documentation does not guarantee that the evaluation transport remains available unchanged through funded stages.

### P1 — Promotion expiration unknown

The current 50% + free reset offer is first-party current on 2026-09-30, but no public expiration timestamp was found. This is a commercial timing risk, not an Echo design finding.

### P2 — Reset-price ambiguity

TCP25/TCP50 exact dynamic reset price under the current promotion and the interaction between promotional reset and rebill reset are unresolved. This affects economics but not runtime feasibility.

## 19. Source index

### Earn2Trade current program/rules

- https://www.earn2trade.com/
- https://www.earn2trade.com/trader-career-path
- https://www.earn2trade.com/gauntlet-mini
- https://www.earn2trade.com/non-us/purchase
- https://www.earn2trade.com/terms-and-conditions
- https://help.earn2trade.com/en/articles/5941958-what-are-the-evaluation-rules
- https://help.earn2trade.com/en/articles/6877364-what-happens-when-i-complete-my-evaluation
- https://help.earn2trade.com/en/articles/8117088-drawdown-types
- https://help.earn2trade.com/en/articles/5372687-how-does-end-of-day-drawdown-work
- https://help.earn2trade.com/en/articles/3292356-what-is-a-trailing-drawdown
- https://help.earn2trade.com/en/articles/3849975-what-is-the-maintain-consistency-rule
- https://help.earn2trade.com/en/articles/3395926-how-is-my-daily-loss-calculated
- https://help.earn2trade.com/en/articles/11183609-reset-pricing-for-earn2trade-accounts
- https://help.earn2trade.com/en/articles/6863801-do-you-provide-free-resets
- https://help.earn2trade.com/en/articles/2280137-what-is-the-fee-structure-on-the-live-or-livesim-accounts
- https://help.earn2trade.com/en/articles/3313030-what-is-the-livesim
- https://help.earn2trade.com/en/articles/12034590-am-i-allowed-to-copy-trades-across-multiple-accounts
- https://help.earn2trade.com/en/articles/2090521-what-platforms-can-i-use-for-the-gauntlet-mini-trader-career-path
- https://help.earn2trade.com/en/articles/15359154-ninjatrader-access-at-earn2trade
- https://help.earn2trade.com/en/articles/4473826-how-to-connect-tradovate-to-ninjatrader
- https://help.earn2trade.com/en/articles/6863807-what-is-the-difference-between-the-tcp25-tcp50-and-tcp100

### Vendor transport docs

- https://api.tradovate.com/
- https://docs.ninjatrader.com/ninjascript/strategy
- https://docs.ninjatrader.com/ninjascript/onexecutionupdate
- https://docs.ninjatrader.com/ninjascript/cancelorder
- https://docs.ninjatrader.com/ninjascript/changeorder
- https://docs.ninjatrader.com/ninjascript/advanced_order_handling
- https://www.rithmic.com/apis
- https://www.rithmic.com/products
- https://www.rithmic.com/products/exchange-simulator

## Material claim register

- claim: Earn2Trade currently offers TCP25/TCP50/TCP100 and GAU50/GAU100/GAU150/GAU200; classification: FACT; source_owner: Earn2Trade; source_title: Home, Trader Career Path, Gauntlet Mini, Purchase; source_url: https://www.earn2trade.com/; retrieved_at: 2026-09-30; source_type: official_program_page; evidence_summary: current product selectors and purchase pages expose the seven sizes; applies_to: current Evaluation inventory; limitations: dynamic UI did not expose every larger-size rule row; conflicts_with: none.
- claim: Current public promotion is 50% off plus one free reset with every evaluation using code 50PLUSRESET; classification: FACT; source_owner: Earn2Trade; source_title: Home; source_url: https://www.earn2trade.com/; retrieved_at: 2026-09-30; source_type: official_program_page; evidence_summary: site-wide Labor Day banner; applies_to: current evaluation purchase; limitations: public expiration timestamp not found; conflicts_with: affiliate-specific checkout discounts.
- claim: TCP base prices are USD150/USD190/USD350; classification: FACT; source_owner: Earn2Trade; source_title: Purchase; source_url: https://www.earn2trade.com/es/purchase?discount=50PLUSRESET; retrieved_at: 2026-09-30; source_type: official_program_page; evidence_summary: current checkout exposes undiscounted base prices; applies_to: TCP25/50/100; limitations: discounted TCP50/100 values not separately rendered by retrieved neutral parser; conflicts_with: none.
- claim: GAU base prices are USD170/USD315/USD375/USD550 and a current first-party 50% checkout renders USD85/USD157.50/USD187.50/USD275; classification: FACT; source_owner: Earn2Trade; source_title: Purchase; source_url: https://www.earn2trade.com/fr/non-us/purchase?a_pid=snowtrading&plan=GAU50; retrieved_at: 2026-09-30; source_type: official_program_page; evidence_summary: checkout renders base and current 50% promotional values; applies_to: GAU50/100/150/200; limitations: affiliate URL parameter exists but rendered banner matches active site-wide 50% offer; conflicts_with: affiliate-specific 20% pages rejected for general promotion.
- claim: Evaluations and LiveSim use EOD drawdown, Live uses trailing drawdown, TCP top 200K/400K funded stages use fixed drawdown; classification: FACT; source_owner: Earn2Trade; source_title: Drawdown types; source_url: https://help.earn2trade.com/en/articles/8117088-drawdown-types; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: current help explicitly maps drawdown type to stage; applies_to: current programs; limitations: drawdown amount is program/size-specific; conflicts_with: none.
- claim: EOD drawdown ratchets from positive EOD balance only, never retreats, caps at starting balance, while open equity losses can breach the current threshold intraday; classification: FACT; source_owner: Earn2Trade; source_title: How Does End of Day Drawdown Work?; source_url: https://help.earn2trade.com/en/articles/5372687-how-does-end-of-day-drawdown-work; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: operational behavior is explicitly documented; applies_to: Evaluation and LiveSim; limitations: provider threshold synchronization can lag; conflicts_with: none.
- claim: Live trailing drawdown advances intraday dollar-for-dollar with positive performance using open and closed equity, never retreats, and stops at starting balance; classification: FACT; source_owner: Earn2Trade; source_title: What is a Trailing Drawdown?; source_url: https://help.earn2trade.com/en/articles/3292356-what-is-a-trailing-drawdown; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: current help explicitly defines open/closed equity intraday trailing semantics; applies_to: Live; limitations: amount varies by account; conflicts_with: none.
- claim: Current Evaluation has no minimum trading-day requirement; classification: FACT; source_owner: Earn2Trade; source_title: What Are the Evaluation Rules?; source_url: https://help.earn2trade.com/en/articles/5941958-what-are-the-evaluation-rules; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: July 2026 authority says no minimum days; applies_to: TCP/GM Evaluation; limitations: 30% consistency mathematically requires at least four profitable days; conflicts_with: older 10-day explainer, marked SUPERSEDED.
- claim: 30% consistency applies only during Evaluation and does not apply to LiveSim/Live; classification: FACT; source_owner: Earn2Trade; source_title: Maintain Consistency Rule; source_url: https://help.earn2trade.com/en/articles/3849975-what-is-the-maintain-consistency-rule; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: no single day may be 30% or more of total PnL at passing; applies_to: Evaluation; limitations: exceeding temporarily does not immediately fail; conflicts_with: none.
- claim: Daily loss uses unrealized/open PnL, closed PnL and commissions and is measured 5pm-to-5pm CT; classification: FACT; source_owner: Earn2Trade; source_title: How is My Daily Loss Calculated?; source_url: https://help.earn2trade.com/en/articles/3395926-how-is-my-daily-loss-calculated; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: exact calculation inputs/timing documented; applies_to: Evaluation and funded rules carrying DLL; limitations: limit amount program-specific; conflicts_with: none.
- claim: Trade copiers are prohibited on every E2T program, both before and after passing; classification: FACT; source_owner: Earn2Trade; source_title: Am I Allowed to Copy Trades Across Multiple Accounts?; source_url: https://help.earn2trade.com/en/articles/12034590-am-i-allowed-to-copy-trades-across-multiple-accounts; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: explicit prohibition on evaluation and LiveSim/Live; applies_to: all stages; limitations: does not answer own single-account algorithm; conflicts_with: none.
- claim: Public E2T evidence unambiguously permits a proprietary automated strategy on one account; classification: UNKNOWN; source_owner: Earn2Trade; source_title: Terms and Conditions + public educational content; source_url: https://www.earn2trade.com/terms-and-conditions; retrieved_at: 2026-09-30; source_type: official_terms; evidence_summary: automation-capable ecosystem exists but Terms bot clause lacks a program-automation carveout; applies_to: central MVP usage; limitations: support clarification required; conflicts_with: official educational mention of automated systems creates ambiguity, not a resolved entitlement.
- claim: Current E2T Evaluation supports NinjaTrader, Tradovate and Rithmic-family frontends among many listed platforms; classification: FACT; source_owner: Earn2Trade; source_title: What Platforms can I use?; source_url: https://help.earn2trade.com/en/articles/2090521-what-platforms-can-i-use-for-the-gauntlet-mini-trader-career-path; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: current platform list; applies_to: Evaluation; limitations: platform support is not API entitlement; conflicts_with: older Rithmic-only help, marked SUPERSEDED.
- claim: New E2T-provided NinjaTrader subscriptions use NinjaTrader–Tradovate rather than legacy Rithmic; classification: FACT; source_owner: Earn2Trade; source_title: NinjaTrader Access at Earn2Trade; source_url: https://help.earn2trade.com/en/articles/15359154-ninjatrader-access-at-earn2trade; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: current route and June 30 legacy cutoff documented; applies_to: new subscriptions; limitations: personal NT licenses with Rithmic are a separate case; conflicts_with: old E2T NinjaTrader/Rithmic path, superseded.
- claim: NinjaTrader supports automated strategies with order/update/execution events, partial fills, cancel and modify; classification: FACT; source_owner: NinjaTrader; source_title: NinjaScript Strategy / OnExecutionUpdate / CancelOrder / ChangeOrder; source_url: https://docs.ninjatrader.com/ninjascript/strategy; retrieved_at: 2026-09-30; source_type: official_transport_docs; evidence_summary: official developer docs expose automation and lifecycle primitives; applies_to: NinjaTrader technical capability; limitations: does not establish E2T account permission; conflicts_with: none.
- claim: Tradovate exposes REST/WebSocket trading/account/order APIs and realtime user-state synchronization; classification: FACT; source_owner: Tradovate; source_title: Tradovate API; source_url: https://api.tradovate.com/; retrieved_at: 2026-09-30; source_type: official_transport_docs; evidence_summary: WebSocket authorization and user/syncrequest state flow documented; applies_to: Tradovate technical capability; limitations: E2T direct API entitlement unproven; conflicts_with: none.
- claim: Rithmic offers APIs for algorithmic trading with order management/execution reports and requires conformance before production access; classification: FACT; source_owner: Rithmic; source_title: R|API+ / API Suite; source_url: https://www.rithmic.com/apis; retrieved_at: 2026-09-30; source_type: official_transport_docs; evidence_summary: R|API+, Protocol API and conformance workflow documented; applies_to: Rithmic technical capability; limitations: E2T credentials/direct API entitlement unproven; conflicts_with: none.
- claim: Rithmic provides a production-like simulator/test surface for API integration; classification: FACT; source_owner: Rithmic; source_title: Exchange Simulator; source_url: https://www.rithmic.com/products/exchange-simulator; retrieved_at: 2026-09-30; source_type: official_transport_docs; evidence_summary: market/limit/stop/bracket/OCO and API test use documented; applies_to: transport development/testing; limitations: not proof of E2T account entitlement; conflicts_with: none.
- claim: API_AUTOMATION_ENTITLEMENT_CONFIRMED is YES for any researched E2T transport; classification: UNKNOWN; source_owner: Earn2Trade + vendors; source_title: combined entitlement review; source_url: https://help.earn2trade.com/en/articles/2090521-what-platforms-can-i-use-for-the-gauntlet-mini-trader-career-path; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: platform access and vendor APIs are proven separately, but no public source closes account/stage entitlement; applies_to: NinjaTrader custom automation, Tradovate direct API, Rithmic direct API; limitations: support response could resolve; conflicts_with: none.
- claim: LiveSim is simulated capital with live market data and can pay withdrawals; classification: FACT; source_owner: Earn2Trade; source_title: What is the LiveSim?; source_url: https://help.earn2trade.com/en/articles/3313030-what-is-the-livesim; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: stage semantics explicit; applies_to: post-evaluation funded stage; limitations: partner may offer Live instead; conflicts_with: “option” wording normalized with current completion article.
- claim: Post-pass funding partner may offer either LiveSim or Live; classification: FACT; source_owner: Earn2Trade; source_title: What Happens When I Complete My Evaluation?; source_url: https://help.earn2trade.com/en/articles/6877364-what-happens-when-i-complete-my-evaluation; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: current partner handoff and stage offer documented; applies_to: funded transition; limitations: exact partner/transport not guaranteed publicly; conflicts_with: none.
- claim: Current LiveSim/Live fees include non-pro LiveSim activation USD139 on first profitable withdrawal and Live data USD140/exchange Rithmic or USD156/exchange NinjaTrader; classification: FACT; source_owner: Earn2Trade; source_title: Fee Structure on Live or LiveSim Accounts; source_url: https://help.earn2trade.com/en/articles/2280137-what-is-the-fee-structure-on-the-live-or-livesim-accounts; retrieved_at: 2026-09-30; source_type: official_help_center; evidence_summary: current fee schedule; applies_to: funded accounts; limitations: professional classification differs; conflicts_with: none.
- claim: An inactive E2T subscriber account may be disabled after more than 120 days and reactivated by correspondence; classification: FACT; source_owner: Earn2Trade; source_title: Terms and Conditions; source_url: https://www.earn2trade.com/terms-and-conditions; retrieved_at: 2026-09-30; source_type: official_terms; evidence_summary: dormancy clause; applies_to: service/subscriber account; limitations: this is not a separately documented “must place a trade every X days” funded rule; conflicts_with: none.

## 20. Worker synthesis

PROGRAM_CANDIDATES:
- TCP25, TCP50, TCP100
- GAU50, GAU100, GAU150, GAU200
- Strongest complete current rule evidence in this pass: TCP25 and GAU50; this is not a recommendation.

AUTOMATION_POLICY:
- status: AMBIGUOUS
- evidence: Trade copying is explicitly prohibited. Vendor/platform technical automation is explicit. E2T public material does not unambiguously authorize the specific use case of a user-owned algorithm executing one account without copying, and the Terms bot clause introduces an unresolved policy boundary.

TRANSPORTS:
- name: NinjaTrader Desktop / NinjaScript over current E2T NinjaTrader–Tradovate route
  PLATFORM_SUPPORTED: YES
  API_EXISTS: YES, native automation mechanism
  API_AUTOMATION_ENTITLEMENT_CONFIRMED: UNKNOWN
  EVALUATION_AVAILABLE: YES as platform/simulated account
  FUNDED_AVAILABLE: YES for current NinjaTrader Live path in principle; LiveSim-specific custom-automation entitlement UNKNOWN
  blockers: E2T own-algorithm policy and custom NinjaScript entitlement unconfirmed
  unknowns: stage-specific permission and funded continuity
- name: Tradovate REST/WebSocket
  PLATFORM_SUPPORTED: YES
  API_EXISTS: YES
  API_AUTOMATION_ENTITLEMENT_CONFIRMED: UNKNOWN
  EVALUATION_AVAILABLE: YES as Tradovate platform credentials; direct API entitlement UNKNOWN
  FUNDED_AVAILABLE: UNKNOWN for direct API
  blockers: developer API entitlement/API-key rights not shown for E2T accounts
  unknowns: Evaluation/LiveSim/Live API entitlement
- name: Rithmic R|API+ / R|Protocol
  PLATFORM_SUPPORTED: YES as E2T Rithmic family
  API_EXISTS: YES
  API_AUTOMATION_ENTITLEMENT_CONFIRMED: UNKNOWN
  EVALUATION_AVAILABLE: YES as Rithmic Paper Trading frontend credentials; direct custom API use UNKNOWN
  FUNDED_AVAILABLE: Rithmic Live data path exists; direct API entitlement UNKNOWN
  blockers: conformance plus FCM/broker/E2T credential entitlement
  unknowns: stage-specific direct API authorization

PURCHASE_BLOCKERS:
- Written E2T confirmation for one-account proprietary algorithmic automation is missing.
- No researched direct/custom transport has current first-party E2T account entitlement proven for the required automation surface.
- Funded-stage transport continuity and partner-specific provisioning are not publicly guaranteed.

SUPPORT_REQUIRED_BEFORE_PURCHASE:
YES

SUPPORT_QUESTIONS:
- Use questions 1–9 in section 17 before buying for an automation-dependent MVP; question 10 closes larger-GM rule-table evidence if those sizes are under consideration.

UNKNOWNS:
- Own-algorithm permission by stage.
- NinjaScript custom automation entitlement.
- Tradovate direct API entitlement for E2T credentials.
- Rithmic direct API entitlement for E2T credentials after conformance.
- VPS/unattended execution policy.
- Funded transport continuity by partner/stage.
- Promotion expiration.
- TCP25/TCP50 current reset prices and promotional-vs-rebill reset interaction.
- Full current GAU100/150/200 stage rows.

## Reuse

REUSABLE_ASSETS:
- Provider-rule provenance matrix separating stage, rule, classification, authority and freshness.
- Transport entitlement checklist separating PLATFORM_SUPPORTED, API_EXISTS and API_AUTOMATION_ENTITLEMENT_CONFIRMED.
- Stage-rule comparison schema that models Evaluation, LiveSim and Live independently.
- Support-question template that separates own-algorithm automation from copying/mirroring policy.

## Improve

REUSABLE_BEHAVIOR_CANDIDATES:
- First-party entitlement triad: always prove vendor technical capability, provider offering and account/stage entitlement as three independent claims; never promote API existence or platform support into entitlement.

## Adversarial self-check

- Current prices/promotions use first-party current pages: PASS, with promotion expiry UNKNOWN.
- Account sizes use first-party current pages: PASS.
- Evaluation rules use current Help Center/program pages: PASS.
- Funded/LiveSim rules use current Help Center/program pages: PASS for current generic stage semantics and captured TCP25/GAU50 rows; larger dynamic program rows explicitly UNKNOWN where not captured.
- Live rules are documented or UNKNOWN: PASS.
- Drawdown semantics are not inferred: PASS.
- Automation policy has its own evidence and remains AMBIGUOUS: PASS.
- Copying policy is separate from automation: PASS.
- Platforms are tied to current E2T evidence: PASS.
- Vendor APIs use official vendor docs: PASS.
- Account API entitlement is not deduced from API existence: PASS.
- Stage-specific entitlement gaps are explicit: PASS.
- Demo/sim environments are separated from E2T entitlement: PASS.
- Support gaps have exact questions: PASS.
- No Reddit/blog affiliate/review source is used as final authority for a material claim: PASS. Earn2Trade-owned educational material is first-party but not elevated over Terms.
- Dynamic claims have retrieval date: PASS.

## Closeout

agents-os-agent-run-register: SKIPPED because this was documentation/web research only and produced no code/debug/review/test segment covered by the run-register trigger.
agents-os-session-feedback: SKIPPED because no qualifying session-friction/degradation event warrants a feedback note; reusable behavior candidate is retained in this worker artifact for later Kaizen review.
agents-os-session-close: REQUIRED by the one-shot mandate and completed by this worker after persistence verification.
No secrets or chain-of-thought are persisted.
No D6 gate is emitted.
