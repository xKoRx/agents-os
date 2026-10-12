---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-CONTROL]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-PROP-PROFILE

## Propósito

Perfil de simulación versionado, con verificación dirigida de fuentes oficiales y supuestos separados. No certifica todas las condiciones comerciales ni ejecución LIVE. La investigación TOP se incorpora abajo como evidencia; el código futuro debe declarar la versión y los supuestos efectivos.

## Contenido

Decisión manager para el escenario de desarrollo A: aceptar los hechos contrastados del perfil de compras desde 2026-07-06. Los valores de latencia, igualdad, centavos del ladder, ordering de fees y terminalidad LiveSim se mantienen explícitos como DESIGN_SCENARIO. No hay una afirmación de rentabilidad ni de condiciones particulares del Owner. La versión exacta del perfil ejecutable y sus campos deben quedar vinculados a source/build en la evidencia A antes de declarar readiness.

Política inicial: no profesional LiveSim, proveedor hipotético Rise non-US USD 50/retiro, activación USD 139 desde el primer retiro después del split. Los USD 120 iniciales son compra Owner, nunca la tarifa pública. Cualquier renovación, plataforma, stow o latencia no acreditada requiere campo explícito y etiqueta de supuesto, sin defaults silenciosos. La simulación detiene LiveSim al límite declarado y conserva transición pendiente; no crea retiros infinitos. Live requiere parámetros propios y pruebas de su regla distinta.

## Fuentes

Devolución TOP prop_profile, solicitado `gpt-6.1-sol`, servido UNKNOWN, 2026-10-12. Spot-check del manager: anuncio oficial de julio y política de retiros. No se atribuyen hechos a documentos históricos incompatibles. Detalle y URLs a continuación.

## Evidencia incorporada
# Earn2Trade GAU50 — targeted profile research

Retrieval: 2026-10-12. ROLE TOP; SURFACE LOCAL; requested model gpt-6.1-sol; served model UNKNOWN. Research only; no implementation, account access, purchases or LIVE. This scratch document is evidence for manager materialization, not canonical policy or commercial certification. Bootstrap/constitution/global profile/index read. No vault mutation.

## Version and material delta

Candidate identity: `E2T_GAU50_PURCHASE_GE_20260706_OBS_20261012_SCENARIO_V1`. Synthetic evaluations have an explicit purchase-rule version independent of historical market-data dates. Official announcement effective July 6, 2026 (updated July 10) applies new rules to purchases on/after that date and their successor funded accounts. Older accounts retain their purchase-date conditions; never migrate an account by calendar rollover.

The supplied references are mostly confirmed: 3000 evaluation profit, 2000 drawdown, 1100 daily loss, strict best-day fraction <0.30, EOD evaluation/LiveSim versus intraday trailing Live, 5 evaluations/3 funded/1 Live, inclusive2250 threshold and80% whole-request split, Friday14CT/Wednesday processing. Material delta against historical ten-day descriptions: the applicable new profile has NO minimum evaluation trading-day count; strict consistency entails at least four profitable days arithmetically. No funded minimum days or consistency. Commercial public pricing is not used to replace Owner inputs: bankroll5000, purchase120 per new synthetic account, evaluation ordinary daily target870, internal pause1000.

## First-party source ledger

All sources retrieved 2026-10-12; dates below are source dates, not guarantees of complete contractual terms. Each quote is <=25 words/source. Paraphrases are intentionally compact.

| ID | Official source/date | Evidence and limited quote |
|---|---|---|
| S1 | [GAU program](https://www.earn2trade.com/gauntlet-mini), no publication date | GAU50 balance50000; target3000; DD2000; DLL1100; six-contract ceiling; evaluation5, LiveSim3, Live1. Quote: “No Minimum Trading Days”. Cards for funded specify no consistency/buffer/monthly subscription and no upfront activation. Card wording “over $2,250” is resolved by explicit inclusive table in S2/S3. |
| S2 | [July rule update](https://www.earn2trade.com/blog/earn2trade-evaluation-rules-profit-split-update/), July6/updatedJuly10 2026 | Quote: “purchases made on or after July 6, 2026.” No separate minimum-day wait, evaluation consistency retained, funded limit violation loses account; split50% below2250/80% from2250 on full request. This date-versioned announcement overrides older blog10day/fixed80 descriptions. |
| S3 | [Withdrawal policy](https://help.earn2trade.com/en/articles/5452472-what-is-the-withdrawal-policy), July9 2026 | GM50:50% under2250/80%2250+, LiveSim max5000. Split based on individual request. Minimum NET100; Friday14CT submission for Wednesday processing. Fees Rise non-US50/US1.5%, Deel50, Bayzat5–40, direct crypto0.735%; provider chosen by firm, region constrained. Quote: “LiveSim Max Withdrawal”. Exact cap accumulator/gross-versus-net basis remains insufficiently defined. |
| S4 | [GAU ladder](https://help.earn2trade.com/en/articles/3292351-what-is-the-progression-ladder-in-the-gauntlet-mini), July6 2026 | Quote: “current account balance and profit levels (real-time).” Image attached to article shows GAU50 profit0–1500:2 contracts;1501–2000:4;2001+:6. Ten listed micros count as one standard. Exceeding aggregate position limit fails. Research asset inspected from HTML `prog_ladder_EN.png`; cents/negative-profit gaps are not specified. |
| S5 | [Consistency](https://help.earn2trade.com/en/articles/3849975-what-is-the-maintain-consistency-rule), May7 2026 | Quote: “no single trading day can account for 30% or more”. Equality blocks approval; overage extends evaluation, does not fail it. Includes days while balance below starting balance. Not funded. |
| S6 | [Daily loss calculation](https://help.earn2trade.com/en/articles/3395926-how-is-my-daily-loss-calculated), August27 2024 | Quote: “including both open (real-time/unrealized), closed trades and commissions.” Reset17:00America/Chicago to17:00 next day, measured from day-start balance. Hitting evaluation limit fails; article also uses “cannot go below”, so candidate adopts hit-inclusive fail. |
| S7 | [EOD mechanics](https://help.earn2trade.com/en/articles/5372687-how-does-end-of-day-drawdown-work), February1 2022 | Quote: “Open equity losses are taken into consideration”. Floor rises with highest EOD balance, never declines, locks at starting balance. Update market-close16–17CT may be delayed; intraday open equity can fail against current floor. |
| S8 | [Trailing](https://help.earn2trade.com/en/articles/3292356-what-is-a-trailing-drawdown), October30 2023; [types](https://help.earn2trade.com/en/articles/8117088-drawdown-types), August10 2026 | Quote from trailing: “All rules, including trailing, use closed and open equity intraday.” Live floor starts48000 and trails intraday high equity dollar-for-dollar to50000. Types confirms EOD evaluation/LiveSim and trailing Live. No GAU50 fixed floor exception. |
| S9 | [Multiple accounts](https://help.earn2trade.com/en/articles/5660666-can-i-have-multiple-trader-career-path-gauntlet-mini-and-live-livesim-accounts), June22 2026 | Quote: “up to five evaluation accounts concurrently.” Three active funded, maximum one Live; spare/stowed account requires agreed timeline and may incur setup costs paid before setup. Reservation timing and costs not quantified. |
| S10 | [Funded completion](https://help.earn2trade.com/en/articles/6877364-what-happens-when-i-complete-my-evaluation), July6 2026 | Quote: “No Minimum Trading Days”. Verification precedes offer. Funded DLL exists; funded ladder hard fail; flat/working-orders closed15:50–17CT. No funded subscription/consistency/buffer. DLL funded breach consequence is not specified clearly enough to assert daily pause versus loss. |
| S11 | [Funded fee structure](https://help.earn2trade.com/en/articles/2280137-what-is-the-fee-structure-on-the-live-or-livesim-accounts), July6 2026; [cost responsibility](https://help.earn2trade.com/en/articles/1795200-what-costs-am-i-responsible-for-once-i-become-funded-with-a-live-livesim-account), January7 2026 | Quote from fee structure: “deducted only from the trader's first profitable withdrawal.” Nonprofessional LiveSim139 one-time/account, no withdrawal means no139charge. Professional LiveSim140/month/exchange; Live Rithmic140 or NinjaTrader156/month/exchange, full calendar month not prorated. Commissions/exchange/NFA/FCM trade costs charged account balance; platform costs may apply, amount unknown. |
| S12 | [Faster onboarding](https://www.earn2trade.com/blog/faster-livesim-access/), March4 2026 | Quote: “Receiving credentials does not mean onboarding is complete”. Credentials permit trading after pass; required paperwork/compliance before first withdrawal. Exact verification/credential/compliance latency unknown. Live choice must precede LiveSim login; later transition at maximum LiveSim amount allowed. |
| S13 | [Older GAU explanation](https://www.earn2trade.com/blog/what-is-the-gauntlet-mini/), older article | Quote: “first $5,000 in profits (minus the 20% profit split).” Mentions subsequent Live transition but also stale10day/fixed80 terms. Cannot resolve modern cap gross/net/paid-total accumulator using this article alone. |

## Finite implementable candidate

FACT means supported above; OWNER means fixed mandate input; ASSUMPTION means named scenario choice; UNKNOWN means commercially unresolved, forbidden silent default.

| Field | Value/classification |
|---|---|
| owner_cash / new_eval_purchase / ordinary_eval_daily / internal_daily_pause |5000 /120 /870 /1000 OWNER |
| eval_start / goal / dd / dll |50000 /3000 /2000 /1100 FACT |
| eval_min_days / consistency |0 FACT; `10 * best_day_cents < 3 * total_net_profit_cents`, total>=300000 cents FACT; compare integer money, no float epsilon |
| funded_min_days / funded_consistency |0 /disabled FACT |
| account inventory admission |activeeval<=5; activefunded<=3; Live<=1 FACT; only1operating account/aggregate trade OWNER |
| ladder |real-time equity-profit basis FACT; qmax2 if profit<1501,4 if1501<=profit<2001,6 if>=2001 ASSUMPTION for cents gaps/negative profit; source integer bands FACT. Separate standard/micro exposure; listed micros10:1 FACT; mixed-symbol aggregation rounding conservative ceil(micro_count/10) ASSUMPTION |
| official DLL evaluation |`day_realized+open-liquidation-PnL-commissions <= -1100 => FAIL` hit semantics FACT fromS6; require closing-cost reserve internally ASSUMPTION conservative. No pause repairing valid balance or history |
| official DLL funded |1100 FACT; breach=>terminal FAIL ASSUMPTION conservative; cannot label verified commercial daily-pause semantics. Owner internal1000 pauses valid account before DLL when executable fills permit |
| EOD floor |initial48000; `F_next=min(50000,max(F_old,EOD_net_balance-2000))`; monotone FACT; failure at equity<=F ASSUMPTION conservative equality (sources vary below/at-threshold wording); check intraday against currentF |
| Live floor |initial48000; `F=min(50000,max(F_old,net_equity_intraday_high-2000))` FACT; same equality assumption; withdrawals never lower floor ASSUMPTION consistent monotone rule |
| phase balance reset |fresh funded50000 FACT starting card; eval PnL not transferred. LiveSim→Live fresh50000 and48000floor ASSUMPTION; reset/funded transfer treatment UNKNOWN commercially |
| withdrawal split |`s(g)=.50 if g<2250 else .80`, whole request FACT; no four-withdrawal cap |
| nonprofessional first payout |139 fee/account FACT, payable only from first profitable withdrawal; `net=s(g)*g-139_if_first-provider_fee` ASSUMPTION fee ordering (source lacks explicit order), require net>=100 FACT |
| provider baseline |Rise non-US fixed50 FACT conditional provider/status; assignment eligible/actual region UNKNOWN, baseline scenario explicitly selects it, does not infer personal jurisdiction |
| no buffer |no additional buffer FACT; available cash for request limited to realized unreserved profits and retained drawdown floor ASSUMPTION accounting; reserve request amount on submission to prevent duplicate withdrawals |
| schedule |America/Chicago zone; Friday14:00 cutoff FACT; exact equality accepted ASSUMPTION because English “by”/Spanish “before”; Wednesday processing FACT;09:00 processing hour ASSUMPTION |
| latency scenario |pass-review1businessday; credentials1businessday afterreview; paperwork2businessdays; approval1businessday fromrequest; credit1businessday afterprocessing ASSUMPTION illustrative, not certified SLA; finite configurable alternative required if used |
| reservation |PASSEVAL waits for funded slot; credentialed funded reserves slot; approved withdrawals remain pending cash untilcredit ASSUMPTION; spare timeline/cost explicit UNKNOWN |
| LiveSim finite terminal |gross cumulative authorized withdrawals capped5000 ASSUMPTION conservative candidate; final request can be smaller and use50% split if<2250; stop LiveSim atcap and markTRANSITION_PENDING. No further payout until explicit Live transition schedule/slot/model or terminal stop. Published5000cap FACT, accumulator UNKNOWN |
| Live transition baseline |terminate account at LiveSim cap rather than assign unverified transfer economics ASSUMPTION scenario; alternative Live enabled requires monthly exchange/platform/commission inputs plus transition delay/starting-state. Finite horizon OWNER-required |
| extra costs |LiveSim nonprofessional no recurring data fee FACT; platformfee/sparefee/renewal fee UNKNOWN. Require config with source or declared scenario value; rejected if absent, never hidden zero. Owner120 remains purchase input; any renewal is distinct scenario, never commercial170 substituted |

Illustrative gross→share→fees→credit: g2250, share1800, first139, Rise50, credit1611; later same request1750. This arithmetic applies fee-after-split scenario, not commercial confirmation of ordering. Trading commissions have already reduced available trading profit and must not be deducted again from cash payout. Campaign net economics deduct purchases and cash-paid extras exactly once; payout-withheld fees reduce credited cash, never also charge cash twice.

## Material unresolved consequences

1. LiveSim5000 accumulator and transition transfer balance/fees/latency: determines whether PAY2250 gets two full80% requests plus500 final50% request, or a different cap boundary. Must remain scenario, and cap must stop repeated payouts.
2. Funded DLL breach consequence and exact drawdown equality: affects account death versus daily suspension. Conservative scenario acceptable for synthetic engine evidence but not certification.
3. Ladder cents gaps, negative profit, mixed micro aggregation, balance changes after withdrawal: affects admissions and adds near thresholds. Conservative values above are explicit; tests need149999/150000/150001/150100 cents and199999/200000/200001/200100 cents.
4. Fee ordering, provider selection, platform/renewal/spare charges, verification/credit/compliance/Live transition latencies: materially affect ranking/time-to-cash and purchase funding. Require declared complete scenario to run; absence is configuration blocker, not zero.
5. Paperwork readiness versus funded trade permission: no withdrawal until compliant; funded phase cannot collapse pass/request/approval/processing/credit into one event.

## Worker lifecycle and manager handoff

/reuse: Date-version every account by purchase conditions; inclusive2250 applies full-request split; strict30% eval only; maintain phase-specific floors and separate processing from credited cash; finite LiveSim terminal. Canonical persistence pending manager at existing Echo Futures initiative artifact location; no duplicate research authority. Scratch is complete.

/improve: Candidate feedback: official article ladder numerical table is image-only and text retrieval silently omits it; source inspection must include linked assets before declaring absence. Also avoid relying on old generic GAU blog for postJuly6 rules. No Graphify feedback: not used. Tool friction: `python` absent, `python3` worked; no durable system change proposed. Requested model versus served remains UNKNOWN.

/close: Worker evidence persisted here; manager/project remain open. Agent-run skipped by explicit documentation-only/lookup-only rule. L0/L1 skipped: no raw transcript artifact requested/available. L3/entity/changelog/feedback canonical writes not performed because worker authorization forbids vault mutation; manager has exact research delta and improvement candidate above. Graphify validation pending only if manager materializes canon. No gate acceptance. Next step: freeze profile as scenario with visible unresolved fields, or verify additional partner terms before commercial certification. por favor gracias

## Minimal fully declared engine scenario supplement

Manager approved conservative ladder scenario: negative profit uses2contracts only while drawdown/DLL/session validity holds; profit1500 and2000 remain lower tiers according to image; cents gaps remain unverified. Frozen additional fee inputs for one hypothetical engine smoke profile: platform_cash_fee0, stowed_funded_setup_fee0, evaluation_renewal_fee120 every30calendar days from purchase while active, eval nonprofessional data0 as published, LiveSim nonprofessional recurring_data0 as published, provider Rise non-US50, first LiveSim139. The zeros for platform/stow are explicit ASSUMPTION hypothetical values, not verified absence of charges; outputs must carry them. Renewal120 is DESIGN_SCENARIO reusing Owner unit cost, not verified public rebill price or additional initial purchase charge. Preserve same latency values above; holiday calendar empty ASSUMPTION for synthetic fixture calendar, realistic campaign must supply exchange/provider holidays. Live phase disabled after cap in this minimal scenario, so no unknown Live monthly charges silently omitted. Positive-cost/longer-latency scenarios may be supplied later but no broad parameter sweep is requested. This completes finite smoke behavior and still cannot certify commercial economics.
