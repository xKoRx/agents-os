---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Futures]]"
sprint: 2026-09-24--2026-09-30
start: 2026-09-24
due: 2026-09-30
progress: 10
repo: "xKoRx/echo-futures"
jira:
prs:
aliases:
  - Echo Futures D5 Prop Economics
tags:
  - kind/project
  - area/echo
  - echo-futures
  - prop-economics
created: "2026-09-24"
updated: "2026-09-24"
---

# Echo Futures — D5 Prop Economics

## 🎯 Objetivo

- Validar cuantitativamente la hipótesis económica de Echo Futures sobre las **principales futures prop firms**, midiendo desde `evaluation comprada` hasta `primer retiro real de cash`.
- Determinar, por prop/plan y política simulada, `q_withdraw`, evaluations esperadas por retiro, cash burn, activaciones, probabilidad de retiro dentro de N attempts y EV neto.
- Consumir el simulator v0 certificado de D4 sin reabrir su matemática.

## 📊 Estado actual

- **D5.1 RESEARCH COMPLETE / GATE IN REVIEW.** Universe actual contrastado contra fuentes oficiales al 2026-09-24; falta aceptación del owner para `D5_RULE_UNIVERSE_PASS`.
- D4 cerrado con `G4C accepted` sobre simulator v0 `d4f42a41946f12231b75e4eb65b90d132731be0d`.
- KPI primario: `q_withdraw = P(evaluation comprada → primer retiro real recibido)`.
- Pass/funded son estados diagnósticos, no éxito final.
- Universo Tier-1 propuesto para freeze: Topstep, Apex Trader Funding, MyFundedFutures, Tradeify y Take Profit Trader. Las cinco mantienen hoy un lifecycle oficial evaluation→funded/sim-funded→payout.
- Productos concretos propuestos: Topstep 50K Trading Combine Standard Path → XFA Standard; Apex 50K EOD Evaluation → EOD PA; MyFundedFutures 50K Builder Default; Tradeify 50K Growth Evaluation → Growth Sim Funded; Take Profit Trader 50K Test → PRO.
- FTMO Futures: KEEP_WATCHLIST. Producto lanzado oficialmente el 2026-09-17; Growth/Pro 50K ya tienen reglas y payout lifecycle públicos, pero sólo llevan 7 días en mercado al corte D5 y no reemplazan todavía una Tier-1 madura.
- Lucid/Alpha Futures/TradeDay/etc.: fuera del primer corte salvo evidencia que justifique reemplazar una Tier-1.
- No existe todavía evidencia de `q_withdraw` real para ninguna prop. El `q=10%` de D4 es fixture matemático, no benchmark.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo-futures | master | `d4f42a41946f12231b75e4eb65b90d132731be0d` | TBD D5 after rules research | TBD D5 after rules normalization | RESEARCH/PLANNING |

## ✅ Tareas

> - [r] D5.1 validar universo Tier-1 y congelar planes concretos por firma #owner/agent #type/research #area/echo
> - [ ] D5.2 extraer rules oficiales versionadas hasta cash withdrawal #owner/agent #type/research #area/echo
> - [ ] D5.3 normalizar rule contract común sin perder excepciones materiales #owner/agent #type/research #area/echo
> - [ ] D5.4 definir experiments null + conditional-edge + recovery sobre cada ruleset #owner/agent #type/research #area/echo
> - [ ] D5.5 congelar SPEC técnica mínima de adapters/rules simulator #owner/agent #type/dev #area/echo
> - [ ] D5.6 implementar/ejecutar simulaciones sólo después de SPEC freeze #owner/agent #type/dev #area/echo #blocked
> - [ ] D5.7 emitir comparación factual por `q_withdraw`, attempts/withdrawal, cash burn y EV #owner/agent #type/research #area/echo #blocked

## 📆 Bitácora

- **2026-09-24 — D5.1 manager start.** Bootstrap y skill `technical-project-manager` cargados; D4 confirmado documentalmente CLOSED/G4C accepted @ `d4f42a41946f12231b75e4eb65b90d132731be0d`. Checkout local reportado en D4 no está montado en esta sesión, por lo que no se reejecutó Git/tests físicos; no existe contradicción material y el baseline certificado se conserva. Web oficial actual valida las cinco Tier-1 propuestas. Freeze propuesto: Topstep 50K Trading Combine Standard→XFA Standard; Apex 50K EOD→EOD PA; MFFU 50K Builder Default; Tradeify 50K Growth→Growth Sim Funded; TPT 50K Test→PRO. FTMO Futures KEEP_WATCHLIST por lanzamiento 2026-09-17. D5.1 queda en REVIEW a aceptación del owner.
- **2026-09-24** — D5 creado tras cierre/certificación de D4. Scope corregido: success = primer retiro real, no funded. Primer corte Tier-1 = Topstep, Apex, MyFundedFutures, Tradeify y Take Profit Trader; FTMO Futures watchlist por lanzamiento reciente.

## 🧭 Decisiones

- `q_withdraw` es el KPI principal.
- No asumir 10%, 20% ni ninguna tasa de retiro.
- No usar pass/funded como proxy de éxito.
- Reglas deben venir de fuentes oficiales y quedar date/version stamped.
- El manager no implementa antes de congelar un contract común y resolver ambigüedades materiales.
- No reabrir D4 salvo contradicción reproducible.
- Para D5.1 se prefieren paths de ~50K con lifecycle único hasta primer payout; variantes con bifurcaciones materiales se difieren salvo necesidad.
- Topstep: modelar purchase path Standard ($49/mes + $149 activation al aprobar) y XFA payout path Standard; la variante No Activation Fee queda sensitivity posterior, no segundo producto base.
- Apex: EOD 50K, no Intraday Trailing, para mantener una barrera EOD representable y comparable.
- MFFU: Builder 50K Default, no Add-On, para evitar duplicar MLL variants.
- Tradeify: Growth 50K, no Select, porque Growth tiene funded payout path fijo; Select introduce elección Flex/Daily después del pass.
- TPT: Test 50K → PRO; PRO+ live es transición posterior y no requisito para first withdrawal.
- FTMO Futures no entra al Tier-1 D5 inicial hasta tener más madurez del producto futures.

## 🔗 Docs / Links

- [[Echo Futures]]
- [[Echo Futures — Simulator v0]]
- [[D4 — Simulator v0 Functional SPEC]]
- [[D4 — Simulator v0 Technical SPEC]]
- [[echo-futures-astra-math-review]]


## D5.1 — Universe freeze package (REVIEW)

Captured at: 2026-09-24.

| Provider | Concrete path | Why this path | Official evidence for D5.1 |
|---|---|---|---|
| Topstep | 50K Trading Combine — Standard purchase path → XFA Standard payout path | canonical 50K; purchase economics explicit; funded path explicit | https://help.topstep.com/en/articles/14289835-topstep-pricing-and-payment-questions · https://help.topstep.com/en/articles/8284197-trading-combine-parameters · https://help.topstep.com/en/articles/8284215-express-funded-account-parameters · https://help.topstep.com/en/articles/8284233-topstep-payout-policy |
| Apex Trader Funding | 50K EOD Evaluation → 50K EOD Performance Account | exact 50K EOD lifecycle; avoids intraday-trailing variant | https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-evaluations/ · https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-performance-accounts-pa/ |
| MyFundedFutures | 50K Builder — Default MLL → Sim Funded | one fixed plan; no activation fee; explicit first-payout buffer and 80/20 split | https://help.myfundedfutures.com/en/articles/14290805-builder-plan-50k-a-comprehensive-guide |
| Tradeify | 50K Growth Evaluation → Growth Sim Funded | fixed payout policy; avoids Select Flex/Daily branch | https://help.tradeify.co/en/articles/10495915-growth-evaluation-accounts · https://help.tradeify.co/en/articles/11083796-growth-funded-account-payout-policy · https://help.tradeify.co/en/articles/10495917-how-do-i-get-funded-after-passing-an-evaluation |
| Take Profit Trader | 50K Test → PRO | direct simulated-funded stage with day-one payout; PRO+ not needed for first withdrawal | https://takeprofittrader.com/ · https://try.takeprofittrader.com/TPT-FAQs-nf40-4-0725 |
| FTMO Futures | WATCHLIST: Growth/Pro 50K | launched 2026-09-17; rules exist but product is only 7 days old at capture | https://ftmo.com/en/press-release/ftmo-launches-ftmo-futures/ · https://ftmo.com/en/futures/comparison-table/ |

### Research dispatches for D5.2

These are rule-capture research one-shots, not the later three implementation shots.

Common output contract for every provider: exact product/path; every material rule from purchase through WITHDRAWAL_RECEIVED; official URL; captured_at=2026-09-24; phase; raw wording summary; normalized field candidate; confidence; RULE_CONFLICT entries; missing facts; simulator relevance. Secondary sources may only discover contradictions and never establish a rule.

1. **Topstep 50K** — extract only Trading Combine Standard purchase path + XFA Standard payout path. Include recurring fee/reset, activation, MLL/DLL/consistency/max contracts, funded scaling, winning-day eligibility, payout cap/split, post-withdrawal balance effects and copy/account limits. Do not research Consistency XFA or No Activation Fee except to record why excluded.
2. **Apex 50K EOD** — extract only EOD Evaluation→EOD PA. Include current evaluation purchase/renewal/reset economics, 30-day access/activation deadline, EOD threshold/DLL, PA activation cost, tier scaling/DLL, payout eligibility/caps/split, inactivity and account/copy restrictions. Do not research Intraday Trailing.
3. **MFFU 50K Builder Default** — extract only Builder Default. Include current non-promotional list price and renewal/reset behavior, no activation fee, EOD MLL/DLL, Sim Funded buffer, 50% payout consistency, qualifying days, first payout amount/cap, 80/20 split, inactivity and post-payout MLL behavior. Do not model Add-On.
4. **Tradeify 50K Growth** — extract only Growth Evaluation→Growth Sim Funded. Include current price/reset economics, EOD trailing/DLL, minimum days, activation fee, funded drawdown, payout minimum/balance threshold, first payout cap, payout split, payout cadence, inactivity/copy/account limits. Do not research Select except conflicts that affect Growth terminology.
5. **TPT 50K Test→PRO** — extract only 50K Test→PRO. Include current subscription/reset and PRO activation/tech fee if any, 3-day/consistency/EOD evaluation rules, PRO intraday drawdown/buffer/news restrictions, 80/20 split, day-one/daily payout semantics, inside-buffer withdrawal closure/50% split, processing path to actual cash, copy/account limits. PRO+ only as continuation_state after first payout, not success condition.

### Gate control

| Gate | State | Acceptance |
|---|---|---|
| D5_RULE_UNIVERSE_PASS | REVIEW | Owner accepts/rejects the five concrete paths + FTMO watchlist |
| D5_RULES_CAPTURED | BLOCKED | Requires D5_RULE_UNIVERSE_PASS |
| D5_RULE_CONTRACT_PASS | BLOCKED | Requires five complete official rule packets |
| D5_SIM_GAP_PASS | BLOCKED | Requires normalized contract |
| D5_SPEC_PASS | BLOCKED | Requires accepted simulator gap classification |
