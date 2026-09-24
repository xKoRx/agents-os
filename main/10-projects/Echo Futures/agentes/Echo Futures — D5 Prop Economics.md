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
progress: 45
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

- **D5.3 SESSION MODEL REVIEW — 2026-09-24.** Diseño entregado en §D5.3 Session Model Review: Brownian sin drift con reloj de varianza y kernel conjunto de primer evento/supervivencia a horizonte finito; running maximum para TPT PRO. `WithdrawalPolicy` y `PricingSnapshot` separados de reglas. TPT = `ECONOMICS_ONLY` para el target automatizado. `D5_SESSION_MODEL_PASS = REVIEW`; siguiente acción `MATH_REVIEW`. No hay código, nuevas SPECs ni aceptación del owner. Esta sección D5.3 prevalece sobre drafts anteriores en los seis puntos del mandato; ver bloqueos precisos al final.

- **D5.1 CLOSED / D5_RULE_UNIVERSE_PASS ACCEPTED por owner.** Tiering congelado: Tier-1 = Topstep + Take Profit Trader; Tier-2 = Apex Trader Funding + MyFundedFutures + Tradeify.
- D4 cerrado con `G4C accepted` sobre simulator v0 `d4f42a41946f12231b75e4eb65b90d132731be0d`.
- KPI primario: `q_withdraw = P(evaluation comprada → primer retiro real recibido)`.
- Pass/funded son estados diagnósticos, no éxito final.
- Tier-1 congelado por owner: **Topstep** y **Take Profit Trader**. Estas dos props definen el primer vertical slice funcional D5.
- Tier-2 congelado por owner: **Apex Trader Funding**, **MyFundedFutures** y **Tradeify**. Se investigan/modelan después de certificar Tier-1, salvo conflicto que afecte el contract común.
- Productos concretos: Topstep 50K Trading Combine Standard Path → XFA Standard; Take Profit Trader 50K Test → PRO; Tier-2 mantiene provisionalmente Apex 50K EOD→EOD PA, MFFU 50K Builder Default y Tradeify 50K Growth.
- FTMO Futures: KEEP_WATCHLIST. Producto lanzado oficialmente el 2026-09-17; Growth/Pro 50K ya tienen reglas y payout lifecycle públicos, pero sólo llevan 7 días en mercado al corte D5 y no reemplazan todavía una Tier-1 madura.
- Lucid/Alpha Futures/TradeDay/etc.: fuera del primer corte salvo evidencia que justifique reemplazar una Tier-1.
- No existe todavía evidencia de `q_withdraw` real para ninguna prop. El `q=10%` de D4 es fixture matemático, no benchmark.
- **D5.2A/D5.2B capturadas 2026-09-24 (REVIEW).** Paquetes de reglas Topstep 50K Standard y TPT 50K Test→PRO completos con fuente oficial, capturados por agentes de research y verificados verbatim por el manager en las páginas load-bearing. 2 RULE_CONFLICT abiertos (TS-1 cap de payout 50K XFA Standard $2,000 vs "$5,000*"; TPT-1 reloj 60 días inside-buffer calendario vs trading days) + 2 tensiones resueltas documentalmente (TS-3 consistencia XFA Standard, TPT-2 semántica EOD-trailing/enforcement intradía). Contrato normalizado candidato y gap matrix de simulator como drafts en este planner. Sin código; D4 intacto; Tier-2 no investigado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo-futures | master | `d4f42a41946f12231b75e4eb65b90d132731be0d` | TBD D5 after rules research | TBD D5 after rules normalization | RESEARCH/PLANNING |

## ✅ Tareas

> - [x] D5.1 validar universo y tiering; congelar paths concretos #owner/agent #type/research #area/echo
> - [x] D5.2A extraer rules oficiales Topstep 50K hasta cash withdrawal (REVIEW a aceptación owner) #owner/agent #type/research #area/echo
> - [x] D5.2B extraer rules oficiales TPT 50K hasta cash withdrawal (REVIEW a aceptación owner) #owner/agent #type/research #area/echo
> - [ ] D5.2C capturar Tier-2 Apex/MFFU/Tradeify después del Tier-1 vertical slice #owner/agent #type/research #area/echo
> - [ ] D5.2 extraer rules oficiales versionadas hasta cash withdrawal #owner/agent #type/research #area/echo
> - [r] D5.3 diseñar session-aware null model, contratos de retiro/precios y clasificación TPT; diseño persistido, gate REVIEW a revisión matemática y aceptación owner #owner/agent #type/research #area/echo
> - [ ] D5.4 definir experiments null + conditional-edge + recovery sobre cada ruleset #owner/agent #type/research #area/echo
> - [ ] D5.5 congelar SPEC técnica mínima de adapters/rules simulator #owner/agent #type/dev #area/echo
> - [ ] D5.6 implementar/ejecutar simulaciones sólo después de SPEC freeze #owner/agent #type/dev #area/echo #blocked
> - [ ] D5.7 emitir comparación factual por `q_withdraw`, attempts/withdrawal, cash burn y EV #owner/agent #type/research #area/echo #blocked

## 📆 Bitácora

- **2026-09-24 — D5.3 diseño, change_log consolidado en el planner.** Seleccionado kernel Brownian conjunto con horizonte finito y máximo para PRO; definidas actualizaciones EOD, consistencia estricta TPT, winning days, políticas de retiro, tres snapshots de precios y pruebas analíticas/oráculo independiente. TS-1 resuelto a $2,000 y TPT-1 a 60 trading days por mandato owner. TPT permanece Tier-1 económica, sin permiso de automatización. Verificaciones documentales y fuentes oficiales focalizadas; no se ejecutó simulación ni se reabrió D4. Por instrucción expresa de editar sólo este archivo, no se modifica tarea puente, memoria, journal externo ni Agents-OS core; la continuidad queda aquí. `D5_SESSION_MODEL_PASS = REVIEW`, `Next action = MATH_REVIEW`.

- **2026-09-24 — D5-M1 Tier-1 rule capture (RESEARCH + CONTRACT DISCOVERY).** Bootstrap Agents-OS + autoridades (planner D5, SPECs D4, matemática MATH_GO, proyecto padre, contrato de ambientes) cargados; ninguna operación de infraestructura. Captura por dos agentes de research con contrato de evidencia (sólo fuentes oficiales topstep.com/help.topstep.com y takeprofittrader.com/try.takeprofittrader.com/zendesk oficial; secundarias sólo SECONDARY_FLAG) + verificación adversarial del manager con re-fetch verbatim de las 6 páginas load-bearing Topstep y 5 páginas load-bearing TPT (WebFetch 403 en Zendesk ⇒ reader MCP; el artículo de suscripciones TPT 15141145057053 no re-fetchable en sesión ⇒ cita del agente + doble corroboración cruzada). Resultado: paquetes D5.2A/D5.2B completos, economics ledger por prop (account balance ≠ personal cash), registro RULE_CONFLICT (TS-1, TS-2, TS-3 resuelto, TPT-1, TPT-2 resuelto), unknowns consolidados (8 Topstep + 9 TPT), contrato normalizado candidato `PropRuleSet` y gap matrix de simulator con 4 SUPPORTED, 7 SMALL_EXTENSION, 7 MATERIAL_EXTENSION, 8 DEFER. Hallazgo material para D5: ambos drawdowns Tier-1 son trailing (EOD Topstep/TPT-Test, intraday TPT-PRO) ⇒ la barrera estática de D4 sobreestimaría p_pass bajo null ⇒ MATERIAL_EXTENSION de capa de sesiones. Gate `D5_TIER1_RULES_CAPTURED` → REVIEW. Sin código; D4 intocado; Tier-2 no investigado.
- **2026-09-24 — Owner freeze D5.1.** Owner redefine tiers: Tier-1 = Topstep + Take Profit Trader; Tier-2 = Apex + MyFundedFutures + Tradeify. `D5_RULE_UNIVERSE_PASS` aceptado. Estrategia de entrega cambia a Tier-1-first: primer hito funcional = reglas reales Topstep/TPT + lifecycle purchase→WITHDRAWAL_RECEIVED + null-model economics reproducible; Tier-2 no bloquea este hito.
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
- **Tiering owner 2026-09-24:** Tier-1 = Topstep + Take Profit Trader. Tier-2 = Apex Trader Funding + MyFundedFutures + Tradeify.
- **Delivery strategy:** certificar primero un vertical slice Tier-1 completo; Tier-2 se monta sobre el contract/engine certificado sin ampliar arquitectura por adelantado.
- **Primer hito funcional D5-M1:** Topstep 50K y TPT 50K deben poder simular `PURCHASE_EVALUATION → ... → WITHDRAWAL_RECEIVED | BURNED` bajo null model, con reglas reales versionadas y outputs económicos obligatorios.

## 🔗 Docs / Links

- [[Echo Futures]]
- [[Echo Futures — Simulator v0]]
- [[D4 — Simulator v0 Functional SPEC]]
- [[D4 — Simulator v0 Technical SPEC]]
- [[echo-futures-astra-math-review]]


## D5.1 — Universe freeze package (ACCEPTED)

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
| D5_RULE_UNIVERSE_PASS | **ACCEPTED** | Owner froze Tier-1=Topstep/TPT and Tier-2=Apex/MFFU/Tradeify |
| D5_TIER1_RULES_CAPTURED | **REVIEW** | Complete official Topstep + TPT rule packets through actual cash receipt (paquetes D5.2A/D5.2B + conflictos + unknowns en este planner, captured_at 2026-09-24) |
| D5_TIER1_RULE_CONTRACT_PASS | BLOCKED | Normalize only Tier-1 first, preserving prop-specific exceptions |
| D5_TIER1_SIM_GAP_PASS | BLOCKED | Classify every Tier-1 rule as SUPPORTED/SMALL_EXTENSION/MATERIAL_EXTENSION/DEFER |
| D5_TIER1_SPEC_PASS | BLOCKED | Freeze minimum functional+technical extension for Tier-1 lifecycle |
| D5_TIER1_IMPL_PASS | BLOCKED | Three-shot implementation/audit/correction on exact certified baseline |
| D5_TIER1_ECON_PASS | BLOCKED | Null-model Monte Carlo produces required q_withdraw/cash/burn/tail metrics |
| D5_TIER2_EXPANSION | BLOCKED | Only after Tier-1 engine/spec is certified |


## D5.2A — Topstep 50K Standard rule packet (captured_at 2026-09-24)

Producto congelado: **50K Trading Combine — Standard purchase path** ($49/mes + $149 activación) → **50K Express Funded Account (XFA) — Standard payout path**. Variantes excluidas y NO investigadas como producto: No Activation Fee, Consistency XFA, DLL add-on en checkout (offer que dobla caps — registrada sólo como ambigüedad, sensibilidad posterior). Fuentes oficiales: `help.topstep.com` + `topstep.com`. Confianza: HIGH = declaración oficial explícita; MISSING = no encontrado en páginas oficiales.

### Fase 1 — Trading Combine 50K (Standard)

| campo | valor normalizado | evidencia oficial (cita) | fuente | conf |
|---|---|---|---|---|
| purchase_cost | 49 USD por ciclo de 30 días (base; impuestos aparte) | "Standard Path: '$49/month'" · "Listed prices are base costs only." | help.topstep.com/en/articles/14289835 | HIGH (status list-vs-promo = unknown) |
| recurring | 49 USD cada 30 días, auto-renew; cancel manual irreversible (sin resubscribe); pago fallido: 2 reintentos y baja; resets deshabilitados durante retry | "It Rebills every 30 days from your original sign-up date." · "attempt to process the charge two more times before the subscription is canceled." | help.topstep.com/en/articles/8284121 | HIGH |
| reset_cost | 49 USD; reset total (balance, MLL, consistency, días → day one); empuja rebill +30d; máx 2/día; 1 Reset Credit gratis por rebill (emitidos ≥2025-12-11 expiran en 1 año) | "A Reset returns your Trading Combine® to its original starting balance" · "Limit: 2 Resets per account each day." · "Resetting your account pushes your Rebill date out 30 days" | help.topstep.com/en/articles/8284128 · /10370307 · /14289835 | HIGH |
| expiration | sin límite de tiempo para pasar; activo hasta pasar o cancelar | "Active until you pass and earn an Express Funded Account® (XFA) — or until you cancel. No time limit for passing." | help.topstep.com/en/articles/8284121 | HIGH |
| inactivity | MISSING para Combine (sólo XFA tiene cláusula 30 días) | — | — | MISSING |
| profit_target | 3,000 USD (tabla oficial del artículo de consistency) | "$3,000 Profit Target" · "$50K → <$1,650" (ejemplo 55%) | help.topstep.com/en/articles/8284208 | HIGH |
| MLL | 2,000 USD; trailing sobre balance END-OF-DAY, nunca baja; monitoreado en tiempo real intradía; lock permanente en balance inicial (50,000); base = Net P&L realizado+no realizado; breach → liquidación resto del día + inelegible para funding hasta Reset (la suscripción sigue corriendo) | "It rises as your end-of-day balance grows, but never moves down." · "Once it reaches your starting balance, it locks permanently." · "monitored in real time throughout the session" · "liquidated for the rest of the trading day and becomes ineligible for funding until you Reset." | help.topstep.com/en/articles/8284204 | HIGH |
| daily_loss | none por defecto; add-on opcional 1,000 USD (50K) fijado en checkout; trigger = flatten hasta próxima sesión 5PM CT, NO es violación | "The Daily Loss Limit (DLL) is optional" · "$50K Account: $1,000" · "it's a forced break for the rest of that session." | help.topstep.com/en/articles/10490293 | HIGH |
| consistency | 55% Consistency Target: mejor día ≤ 55% del Profit Target; línea dura sin redondeo; si se excede el target sube dinámicamente a Best Day ÷ 0.55 (corregir sólo con ganancia de días posteriores) | "Your single best day of profit must stay at or below 55% of your Profit Target." · "55% is a hard line." · "new target = 'Best Day ÷ 0.55'" | help.topstep.com/en/articles/8284208 | HIGH |
| minimum_days | 2 días de trading; día de trading = 5:00 PM CT → 3:10 PM CT del día calendario siguiente | "You can pass in as few as 2 days." · "The trading day runs from 5:00 PM CT through 3:10 PM CT the next calendar day." | help.topstep.com/en/articles/8284208 · /8284197 | HIGH (si el día requiere ≥1 trade: implícito) |
| max_position | 5 minis / 50 micros; micros:minis 10:1; sólo futuros de lista permitida (sin forex/spot) | "$50K | 5 | 50" · "Micros and minis count at a 10:1 ratio." | help.topstep.com/en/articles/8284197 · /8284206 | HIGH |
| scaling_evaluación | none (límites flat; el Scaling Plan es objetivo de XFA) | ver /8284223 y límites flat en /8284197 | help.topstep.com/en/articles/8284223 | HIGH |
| sesión/overnight | cierre obligatorio 3:10 PM CT días hábiles; reanuda 5:00 PM CT; sin overnight ni fin de semana; feriados: cerrar 15 min antes del early close, si no auto-liquidación | "All positions must be closed by 3:10 PM CT every weekday." · "Topstep does not permit holding positions from one session to the next." | help.topstep.com/en/articles/8284206 · /13350348 | HIGH |
| news | sin flatten obligatorio; full-size contra news programada = estrategia prohibida; trades afectados por releases sin excepciones ni Reset credits | "Topstep doesn't require you to flatten positions during economic releases" · "Purposefully trading your full Maximum Position Size directly into a scheduled major news event" (prohibido) | help.topstep.com/en/articles/8284211 · /10305426 | HIGH |
| conducta_prohibida | spoofing; off-market; posiciones opuestas entre cuentas propias; trading coordinado/copiado que pooling riesgo; ventaja técnica/AI/HFT; account stacking multi-perfil; VPN/proxy/geo-evasión; posición a <2% del price limit; trading para terceros; disputas de pago; abuso de SIM | "holding opposite positions across multiple accounts simultaneously" · "using software, AI, ultra-high speed systems... to gain an unfair advantage" · "VPNs, proxy services, TOR... are not permitted." | help.topstep.com/en/articles/10296582 · /10305426 | HIGH |
| account_limits | Combines simultáneos ilimitados bajo un perfil; Practice 150K gratis (1) con suscripción activa | "There's no limit to the number of Trading Combines you can have" | help.topstep.com/en/articles/8284197 · /8284134 | HIGH |
| failure_rules[] | MLL breach → liquidación + inelegible hasta Reset; conducta prohibida → warning/delección de día/reset/cierre/denial de payout; consistencia no falla la cuenta (sólo bloquea pass hasta corregir); DLL no es violación; refund 28 días sólo compra nueva sin actividad | ver filas MLL/DLL/consistency | /8284204 · /10490293 · /8284208 · /8284197 | HIGH |

### Pass / Activation

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| pass_transition | target + ≥2 días de trading + best day ≤55%; estado refleja ≤30 min; el Combine CIERRA y su suscripción auto-cancela; ganancias NO se transfieren; activación desde el Trade Report (elección de tipo/size de XFA, locked después) | "The subscription tied to the passed Trading Combine will auto-cancel, and the account will close." · "you activate your Express Funded Account® (XFA) directly from your Trade Report." | help.topstep.com/en/articles/8284208 · /8284197 · /8284217 | HIGH |
| activation_deadline | MISSING — sin plazo documentado | — | /8284217 | MISSING |
| activation_cost | 149 USD one-time por XFA ganado (Standard path); no reembolsable; XFA sin mensualidad | "Standard Path — $149, charged once per XFA earned." · "No refunds on Activation Fee purchases" | /14289835 · /8284217 · /8284117 | HIGH |
| failed_activation | estado de pérdida sin refund; recuperación paga: Back2Funded 599 USD (≤2 reactivaciones por XFA, 30 días calendario desde cierre, sólo cierre por violación PRE-primer-payout; tras Back2Funded todo resetea a cero) o nuevo Combine | "$50K XFA — $599" · "Up to 2 Reactivations per Express Funded Account." · "Once a Payout is taken from an XFA, it is no longer eligible for Back2Funded." | /12060405 · /8284117 · /14289835 | HIGH (ventana: ver RULE_CONFLICT TS-2) |

### Fase 2 — XFA 50K Standard (payout path Standard)

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| starting_reference | buying power 50K; BALANCE nominal inicia en 0; MLL arranca en −2,000 | "Your balance starts at $0 and grows from your trading profits." · "your MLL starts at -$2,000" | /8284215 · /8284204 | HIGH |
| MLL_funded | 2,000 USD; trailing sobre MÁXIMO balance EOD, nunca baja; lock en 0 cuando el balance alcanza 2,000 (= buffer/safety net: la cuenta no puede caer bajo 0); breach → liquidación y cierre permanente al fin del día | "Once your balance reaches $2,000, the MLL locks at $0 permanently." · "Your account is permanently closed." | /8284204 · /8284215 | HIGH |
| daily_loss_funded | add-on opcional 1,000 (si se eligió en Combine permanece de por vida de la cuenta; requerido en plataformas ≠ TopstepX); trigger = temporary violation, flatten hasta próxima sesión | "The DLL stays with the account for its full lifetime." · "A Daily Loss Limit applies to accounts on platforms other than TopstepX." | /10490293 · topstep.com/express-funded-account-rules | HIGH |
| max_position_funded | Scaling Plan por niveles de balance (ejemplo textual 50K: 2 minis / 20 micros); nunca sube intradía; >10 s en exceso = review; tabla completa de tiers es imagen (parcial) | "Follow the Scaling Plan — the max contracts you can hold at one time — based on your current account balance." · "Your max contracts do not increase mid-session." | /8284223 · /8284215 | HIGH concepto / MEDIUM tiers |
| consistency_funded | NONE en Standard (tabla Parameters: "❌"); la 40% es del path Consistency (excluido) y se resetea tras cada payout | "Consistency target: ❌" (columna Standard) | /8284215 · /8284208 | HIGH (ver TS-3) |
| winning_days | 5 winning days de ≥150 USD Net P&L; no consecutivos; el día lockea 4:00 PM CT; el día del request no cuenta para el próximo ciclo | "5 winning days of $150+ Net P&L. Days don't need to be consecutive." · "your 5-day count restarts" (tras cada payout) | /8284233 | HIGH |
| buffer_safety_net | MLL lock en 0 = piso absoluto; policy recomienda construir balance hasta MLL=0 antes del primer payout | "trails upward, locking at $0 once the balance reaches $2,000" | /8284204 · /8284233 | HIGH |
| payout_eligibility | 5 winning days $150+ + ganancia neta ≥0.01 desde el último payout (PRIMER payout exento) + compliance limpio + ventana de request Sun 5 PM – Fri 5 PM CT (feriados fuera) | "Positive net profit since your last Payout... at least $0.01... Your first Payout is exempt." · "Available during CME market hours: Sunday 5 PM CT – Friday 5 PM CT" | /8284233 | HIGH |
| payout_cap | por request: min(50% del balance, cap por tamaño); 50K Standard cap = 2,000 USD; mínimo de request 125 USD; caps completos: 50K 2,000/3,000 (Std/Consistency), 100K 3,000/4,000, 150K 5,000/6,000 | "Max Payout per request: 50% of your account balance up to the cap below." · "$50K | Standard | $2,000" · "Minimum Payout: $125" | /8284233 | HIGH (ver RULE_CONFLICT TS-1) |
| payout_split | 90/10 (trader 90%) en payouts XFA; regla legacy: 100% de los primeros 10,000 USD de profits vitalicios para dashboards pre-2026-01-12 (población MEDIUM) | "90/10 profit split — you keep 90%" · "You receive 100% of your first $10,000 in lifetime profits." (contexto legacy) | /8284233 | HIGH / MEDIUM legacy |
| payout_processing | aprobación interna 1–3 días hábiles; métodos: Aeropay (US) instantáneo fee 0; Prop-to-Brokerage (US) mismo día fee 0 si request ≤12 PM CT; Wise 1–3 días fee 0; ACH 1–3 días fee 30; Wire/SWIFT 5–10 días fee 30; no payouts en feriados | "Internal approval can take 1-3 business days" · "ACH (US): 1-3 business days, $30 fee." | /8284233 · /13350348 | HIGH |
| payout_invalidation | review de compliance/conducta/ToU; sólo bancos a nombre propio; W-9/W-8BEN obligatorio; DLL temp-violation posterga; MLL post-request NO clawback de payout aprobado; copy trading auto-disabled durante procesamiento; inelegibilidad por felony/disciplina NFA-CFTC/deuda de clearing/chargeback | "payouts only to bank accounts in your own name; tax forms (W-9/W-8BEN) required." · "Hitting MLL after a request doesn't affect an already-deducted payout." | /8284233 · topstep.com/express-funded-account-rules | HIGH |
| balance_effect | el monto se deduce del balance al aprobarse; la XFA sigue operable de inmediato | "Payout amounts are subtracted from the balance once approved." · "Funds transfer immediately on request (XFA can resume trading)" | /8284233 · topstep.com/express-funded-account-rules | HIGH |
| drawdown_effect | MLL seteado a 0 PERMANENTE tras el primer payout (queda en 0); balance restante = piso efectivo de pérdida | "Your MLL is set to $0 after your first Payout... The remaining balance becomes your effective loss floor." | /8284233 | HIGH |
| continuation_state | misma XFA sigue tradendose; conteo de 5 winning days reinicia; regla ≥0.01 aplica al próximo payout; Back2Funded perde elegibilidad tras cualquier payout | "After each Payout: ... your 5-day count restarts." | /8284233 | HIGH |
| closure_conditions | MLL breach = cierre permanente; inactividad >30 días puede cerrar (sin holds); cierre voluntario de XFA elegible paga ≤50% del Reward Balance cap 5,000 (resto se pierde); Topstep puede cerrar en cualquier momento; máx 5 XFA activos (Shoulder Tap: 1) | "XFAs with no trading activity for more than 30 days may be closed." · "up to 50% of your current Reward Balance, capped at $5,000" · "You can hold up to 5 active XFAs at a time." | /8284215 · topstep.com/express-funded-account-rules | HIGH |

### Economics ledger Topstep (PERSONAL CASH; balances = nominales simulados)

- PURCHASE: −49 USD (ciclo 1 Combine 50K Standard, +impuestos).
- SUBSCRIPTION_RENEWAL: −49 cada 30 días mientras el Combine esté activo; sigue tras MLL breach; auto-cancela al pasar.
- RESET_REBUY: −49 por reset (económicamente = nuevo attempt con F; conserva suscripción y corre rebill +30 días); Reset Credit gratis por rebill.
- ACTIVATION: −149 al activar XFA (una vez por XFA ganado).
- FUNDED_FEE: 0 (XFA sin mensualidad).
- OTHER_REQUIRED_COST: L2 DOM 38 USD/mes (opcional); comisiones por trade auto-deductadas del nominal (SCHEDULE NO CAPTURADO — unknown); Back2Funded 599 USD (condicional, ≤2×, pre-payout).
- WITHDRAWAL_RECEIVED: +0.90 × min(0.50 × balance, 2000) − fee método (0 Aeropay/Brokerage, 30 ACH/Wire); request mínimo 125. Ejemplo cap: request 2,000 → 1,800 netos (Aeropay) / 1,770 (ACH).

## D5.2B — TPT 50K Test→PRO rule packet (captured_at 2026-09-24)

Producto congelado: **50K Test** (evaluación) → **50K PRO** (sim-funded con payout day-one). PRO+ sólo como continuation_state posterior al primer retiro (no requisito de éxito). Fuentes oficiales: `takeprofittrader.com`, `try.takeprofittrader.com/TPT-FAQs-nf40-4-0725`, `takeprofittraderhelp.zendesk.com` (help desk oficial), `/terms`.

### Fase 1 — 50K Test

| campo | valor normalizado | evidencia oficial (cita) | fuente | conf |
|---|---|---|---|---|
| purchase_cost | LIST 170 USD/mes (MEDIUM — derivado de 3 promos oficiales consistentes: 40%→102, 30%→119, 50%→85); promo vigente NOFEE40 = 102 USD/mes con 40% lifetime discount y activación 130 waived de por vida | "you'd be getting a $50k account for just $102 flat" · "$119 flat" (NOFEE30) · "$85 flat" (NOFEE50) | zendesk 29660646764445 · 36337706971677 · 35985020984605 | HIGH promo / MEDIUM list |
| recurring | mensual, mismo día calendario; NO auto-cancela por breach (cancelar manualmente); intento final de pago fallido → expira sin reactivación | "You will be charged a subscription fee each month on the same calendar day" · "if the final payment attempt fails, your account will expire." | zendesk 15141145057053 | HIGH (re-fetch directo falló 403/reader; corroborado por 15140989806493 y FAQ) |
| refund | 72 h sólo si cuenta sin usar/sin tradear, menos 75 USD | "we will refund you within 72 hours... minus a $75 fee" | takeprofittrader.com/terms | HIGH |
| reset_cost | 99 USD (50K Test); resets ilimitados; NO cambia la fecha de renewal | "50K $99" · "there are no limits to test resets" · "this will not change the subscription renewal date" | zendesk 15140989806493 · FAQ | HIGH |
| expiration | sin time limit para pasar; expira sólo por renewal fallido; sin política de inactividad documentada | "there is no time limit to reach your profit target" | zendesk 15141145057053 | HIGH |
| profit_target | 3,000 USD (tabla oficial) | "$50,000 | 6 Contracts | $3,000 | $2,000" | zendesk 15170265979165 | HIGH |
| drawdown | 2,000 USD EOD TRAILING: el floor sigue el MÁXIMO balance EOD hacia arriba y lockea en el balance inicial (50,000); el breach se ENFORCEA intradía incl. no realizado → liquidación inmediata | "the drawdown for test accounts is calculated only at the end of the trading day" · "the minimum account balance follows your highest end-of-day balance upward... until it reaches the original starting balance... it stops trailing and remains fixed." · "If your account drops to the Minimum Account Balance at any time — through realized or unrealized losses — the account is immediately liquidated" | zendesk 15170265979165 | HIGH (semántica EOD vs intradía: ver TPT-2) |
| daily_loss | none en Test | "no daily loss limits" | FAQ | HIGH |
| consistency | best day < 50% del net profit total al momento del pass; breach NO falla la cuenta: el profit goal sube a 2 × best day | "your best trading day must be below 50% of your total net profits" · "Updated Profit Goal > High Profit Day's Net P/L × 2" · "you have not failed the test account" | zendesk 15170316538013 | HIGH |
| minimum_days | 3 días de trading con ≥1 trade (cuentas compradas antes del 2026-08-17: 5 días — cambio versionado, no conflicto) | "you must trade for a minimum of 3 trading days. A trading day is defined as any day in which you place at least one trade." | zendesk 15170316538013 | HIGH |
| max_position | 6 minis / 60 micros (micros 10×); sólo productos CME/CBOT/NYMEX/COMEX aprobados | "you can trade up to 60 micro contracts" | zendesk 15169066911133 · 15172629238301 | HIGH |
| sesión/overnight | sin overnight; ventana 6 PM–5 PM ET; auto-close 4:55 PM ET; feriados: perder el close ajustado = liquidación | "Positions cannot be carried from one trading day into the next" · "TPT will automatically close any open position at 4:55 PM Eastern" | zendesk 15170347090461 | HIGH |
| news | permitido en Test | "You're allowed to trade the news." | FAQ | HIGH |
| copy/limits | copy trading entre cuentas propias permitido (copiers aprobados: Tradesyncer, TradeCopia, Affordable Indicators, Replikanto Compliance, nativo); Tests simultáneos ilimitados; máx 5 funded activos; máx 10 activaciones de test aprobado por 30 días rolling; counter-positions entre cuentas propias prohibidas (liquidación de ambas); Cooldown 60 días por tocar rolling adjusted loss limit (bloquea compras/resets/activaciones) | "you can trade as many accounts simultaneously as you'd like" · "The limit is 5 active funded accounts per person" · "activate up to 10 successfully passed tests within a span of 30 calendar days" | FAQ · zendesk 15172695563933 · 34431176505245 | HIGH límites / MEDIUM Cooldown |
| failure_rules[] | tocar MAB (realizado o no realizado) = liquidación inmediata; exceder posición; productos/horarios no aprobados o_hold past close; counter-positions; bots/algos; consistencia NO falla | "If your account drops to the Minimum Account Balance at any time... immediately liquidated" · UTP: "may result in profit forfeiture, account reset, account closure, or removal" | zendesk 15170265979165 · 34431153546397 | HIGH |

### Pass / PRO activation

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| pass_transition | target + ≥3 días + consistencia; la suscripción del Test AUTO-CANCELA al pasar; activación manual en dashboard (fee/contrato/POA firmado); sin deadline documentada | "Once you successfully pass your trading test, your subscription will be automatically canceled." · "you must still manually complete the activation steps in your dashboard" | FAQ · zendesk 15141145057053 · 17239170507805 | HIGH (deadline MISSING) |
| activation_cost | 130 USD one-time al activar PRO (0 con NOFEE credit); sin mensualidad PRO | "Pay a one time $130 PRO Account setup fee, and ZERO monthly fees after that" · "no ongoing monthly fees with a PRO or PRO+ Account" | takeprofittrader.com · zendesk 28923632631581 | HIGH |
| starting_reference | 50,000 nominal (mismo buying power que el Test; sin scaling) | "you're at the exact same buying power in your PRO Account that you had in your test account. No gimmicks or 'scaling'" | takeprofittrader.com · zendesk 15171769361053 | HIGH |
| failed_pro | PRO reset 649 USD (50K), hasta 3×, conservando retiros day-one; si el estado de suscripción PRO queda disabled → cierre permanente sin reset; si no → nuevo Test | "50k PRO Reset: $649" · "we allow you to reset your PRO Account up to three times per account" · "if the PRO subscription status is disabled, the PRO account is completely closed" | zendesk 15171895352733 | HIGH |

### Fase 2 — 50K PRO

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| drawdown | 2,000 USD INTRADÍA trailing sobre PEAK balance (realizado + NO realizado, tiempo real); nunca excede el balance inicial; lock en 50,000; MAB tocado (realizado o no) = liquidación inmediata | "The Trailing Drawdown is calculated intraday using your peak balance, which includes realized gains and unrealized gains. The drawdown trails intraday" · "will never exceed your starting account balance" | zendesk 15171769361053 · 15171820366109 | HIGH |
| buffer | buffer = máximo drawdown; 50K → umbral 52,000 de balance para retirar al 80% | "your maximum drawdown or buffer zone is $2,000… you will need to reach a balance of $52,000 in order to start withdrawing at 80%" · tabla "50k $52,000" | zendesk 15172219527581 · FAQ | HIGH |
| daily_loss | none documentada en PRO (ausencia en el artículo de reglas PRO) | — | zendesk 15171769361053 | MEDIUM (ausencia) |
| max_position/scaling | sin scaling en ninguna cuenta; el límite de posición sigue aplicando (6/60 implícito por mismo buying power; UTP #2) | "No scaling plan on any account" | FAQ · zendesk 34431153546397 | HIGH / MEDIUM número |
| consistency | none en PRO | "No, there is no consistency rule in the PRO account." | FAQ | HIGH |
| payout_eligibility | day-one y DIARIO; split 80% sólo con balance ≥ buffer (52,000 en 50K) | "In a PRO account you can withdraw from day-one and daily" · "you must build a buffer on the account first" | FAQ · zendesk 15172219527581 | HIGH |
| min_max_withdrawal | sin máximo declarado; sin mínimo declarado PRO→wallet; wallet→bank ≤250 USD tiene fee 50 (>250 gratis) | "No, there is no maximum withdrawal amount." · "a withdrawal of $250 or less from your wallet... $50 withdrawal fee" | FAQ · zendesk 15172354954525 | HIGH |
| payout_split | 80/20 sobre retiros sobre buffer (20% se descuenta automáticamente al solicitar); 90/10 es sólo PRO+ (post-review) | "the profit split is 80/20, where the trader keeps 80%" · "commission is calculated and subtracted automatically" | zendesk 15172219527581 · 15172253980061 | HIGH |
| daily_payout | requests diarios; balance PRO se actualiza 8–9 PM EST; requiere FLAT (sin posiciones ni órdenes) al momento del request | "This is updated daily between 8PM - 9PM EST" · "traders must have no open positions or working orders at the exact moment" | zendesk 15172253980061 | HIGH |
| inside_buffer | permitido pero CIERRA el PRO permanentemente (sin reactivación ni reset); split de las ganancias tomadas: 50% si ≤60 días / 80% si >60 días (CONFLICTO de reloj: ver TPT-1) | "it'll close that account and those profits will be at a 50% profit split" · "once canceled, the PRO account cannot be reactivated or reset" | FAQ · zendesk 15172219527581 | HIGH mecánica / CONFLICTO reloj |
| withdrawal_effect | trailing lockea en 50,000 y deja de moverse; retiro sobre buffer deja la cuenta viva con el drawdown invariado (inferencia por lock + retiros diarios; sin frase textual explícita) | "The drawdown continues to trail profits until it reaches your starting balance; once it reaches that level, it no longer moves." | zendesk 15171769361053 · FAQ | MEDIUM |
| processing | PRO→wallet automatizado 5–10 segundos; wallet→bank: Plaid (US) real-time o ACH 1–2 días hábiles; PayPal/Wise (intl) ≤12 business hours; gates: KYC, tax form, contrato PRO+POA, AML name-match | "the account-to-wallet withdrawal process will take 5-10 seconds" · "payouts are processed through Plaid and are typically real-time" | zendesk 15172253980061 · 15172296875165 | HIGH |
| cash_semantics | cash real a banco/PayPal/Wise (wallet también gastable en TPT); denegación sólo por 4 causas: fondos insuficientes, posiciones/órdenes abiertas al pedir, mantenimiento Tradovate, API caída | "the funds are now in your Wallet and available to be paid out" · "denied, but only for one of four reasons" | zendesk 15172253980061 · 37697356049949 | HIGH |
| PRO+ continuation | upgrade por review (sin umbral fijo); al subir, el PRO se congela con 5,000 de ganancia retenida (share del trader retirable según split PRO; balance negativo de PRO+ se descuenta de ahí); PRO+ arranca en 0 con EOD drawdown −2,000, sin buffer, 90/10; todo trading/retiro posterior en PRO+; NO afecta el primer retiro (ocurre en PRO) | "$5,000 in profit... frozen" · "the PRO+ account would start at $0 with an EOD drawdown of -$2,000" · "all future trading and withdrawals must be done on the PRO+ account only." | zendesk 15171978600349 · 36337706971677 | HIGH |
| reglas_extra_PRO | sin bots/algos; salir antes de limit-up/down; ≥1 día de trading por semana calendario (Dom–Vie); sin posiciones 1 min antes/durante/1 min después de FOMC statement, NFP, CPI | "no positions 1 min before/during/1 min after" (FOMC statements, NFP, CPI) | zendesk 15171769361053 | HIGH |

### Economics ledger TPT (PERSONAL CASH; balances Test/PRO = nominales SIM)

- PURCHASE: −170/mes list (MEDIUM) o −102/mes NOFEE40 (HIGH) por 50K Test.
- SUBSCRIPTION_RENEWAL: mismo monto cada mes calendario mientras el Test esté activo; no auto-cancela al fallar una regla.
- RESET_REBUY: −99 reset Test (ilimitado, no mueve renewal); −649 reset PRO (≤3×, condicional post-failure).
- ACTIVATION: −130 al activar PRO (0 con NOFEE).
- FUNDED_FEE: 0 recurrente.
- OTHER_REQUIRED_COST: comisiones nominales 4.50 USD round-turn mini / 1.50 micro, descontadas del balance nominal en Test y PRO (afectan velocidad a target/buffer, no cash personal directo).
- WITHDRAWAL_RECEIVED: +0.80 × monto retirado sobre buffer (dentro de buffer: cierre + 50%/80% según reloj 60d; −50 fee si wallet→bank ≤250).

## D5 — RULE_CONFLICT register

| id | provider | tema | fuente A | fuente B | estado |
|---|---|---|---|---|---|
| TS-1 | Topstep | cap de payout por request en XFA 50K Standard: $2,000 (tabla por tamaño del Payout Policy; $5,000 coincide con el cap 150K) vs "$5,000*" sin calificar tamaño (headline de XFA Parameters) y "$5,000" (topstep.com/express-funded-account-rules) | help.topstep.com/en/articles/8284233 | help.topstep.com/en/articles/8284215 · topstep.com/express-funded-account-rules | RULE_CONFLICT ABIERTO — evidencia favorece $2,000 para 50K (tabla por tamaño + footnote de Parameters que remite al Payout Policy). Adjudica owner/manager. |
| TS-2 | Topstep | ventana de decisión Back2Funded: 30 días calendario (Help Center 12060405, actualizado 2026-08-14, ampliado desde 2026-05-29) vs 7 días (topstep.com/express-funded-account-rules, actualizado 2025-06-26) | help.topstep.com/en/articles/12060405 | topstep.com/express-funded-account-rules | RULE_CONFLICT ABIERTO (página marketing stale) — Help Center más nuevo gana por jerarquía §regla comercial 8; no material para first withdrawal (recuperación post-failure). |
| TS-3 | Topstep | consistencia en XFA Standard: frase del artículo de consistency ("choose Standard or Consistency as your Payout path") vs tabla de Parameters (Standard: ❌) | help.topstep.com/en/articles/8284208 | help.topstep.com/en/articles/8284215 | RESUELTO — Standard no tiene consistency target (tabla + eligibility del Payout Policy sin consistencia). |
| TPT-1 | TPT | reloj inside-buffer: tabla "≤ 60 días since account opening → 50%" (lectura calendario) vs nota inmediata "Please note it is 60 trading days" en el MISMO artículo | zendesk 15172219527581 (tabla) | zendesk 15172219527581 (nota) | RULE_CONFLICT ABIERTO (intrapágina) — decide el split 50/80 del cierre inside-buffer. Default propuesto: trading days (frase explícita). Adjudica owner/manager. |
| TPT-2 | TPT | Test drawdown: "calculated only at the end of the trading day" vs liquidación inmediata intradía incl. unrealized (mismo artículo) | zendesk 15170265979165 | zendesk 15170265979165 | RESUELTO como semántica normalizada: el trailing se ACTUALIZA EOD; el breach se ENFORCEA intradía incl. unrealized. |

SECONDARY_FLAGS: ninguno que contradiga fuente oficial (secundarias Topstep consultadas corroboran $3,000/$2,000/EOD-lock; TPT no usó secundarias).

## D5 — Unknowns consolidados (captured_at 2026-09-24)

Topstep: status list-vs-promo del precio $49; inactividad en Combine; deadline de activación XFA; si el día de trading requiere ≥1 trade (implícito); tabla completa de scaling tiers (imagen no textual); frequency cap de payouts (ninguno declarado); población exacta del legacy "100% primeros $10K"; schedule de comisiones por trade (no capturado en ninguna página oficial).
TPT: list price $170 no impreso directamente (derivado triple-consistente); deadline de activación PRO; destino del $130 si el PRO falla después; mínimo PRO→wallet; "no daily loss" explícito en PRO; frase textual del efecto del retiro sobre el drawdown lockeado; inactividad Test; número de reintentos de pago; cutoff horario fijo de payout request.

## D5.3 draft — Contrato normalizado candidato (PropRuleSet)

```text
PropRuleSet
  provider: enum {TOPSTEP, TPT}
  product: string                      # "50K Trading Combine → XFA Standard" | "50K Test → PRO"
  captured_at: date                    # 2026-09-24
  currency: USD
  reference_balance: money             # nominal de cuenta (50,000)

  evaluation:
    purchase_cost: money               # TS 49/30d | TPT 170 list (promo separado)
    recurring_cost: money|none
    recurring_calendar: enum {FIXED_30D, CALENDAR_MONTH}
    reset_cost: money                  # TS 49 | TPT 99
    target: money                      # 3,000 ambos
    drawdown: money                    # 2,000 ambos
    drawdown_mode: EOD_TRAILING_LOCK_AT_START        # ambos Tier-1 en evaluación
    breach_enforcement: REALTIME_INCL_UNREALIZED     # ambos (TS monitoreo real-time; TPT liquidación inmediata)
    daily_loss: money|none             # TS none base (add-on excluido) | TPT none
    minimum_days: int                  # TS 2 | TPT 3
    consistency:
      kind: enum {BEST_DAY_MAX_PCT_OF_TARGET, BEST_DAY_MAX_PCT_OF_NET_AT_PASS}
      pct: percent                     # TS 55 | TPT 50
      breach_behavior: enum {RAISE_TARGET_DYNAMIC, RAISE_GOAL_2X_BEST_DAY}
    max_position: {minis: int, micros: int}          # TS 5/50 | TPT 6/60
    failure_rules[]:                   # drawdown breach, conducta, productos/horarios

  funded:
    activation_cost: money             # TS 149 | TPT 130 (promo waives)
    balance_start: money               # TS 0 (nominal) | TPT 50,000 (nominal recentered)
    drawdown: money                    # 2,000 ambos
    drawdown_mode: enum {EOD_TRAILING_LOCK_AT_START, INTRADAY_TRAILING_LOCK_AT_START}
                                       # TS XFA = EOD | TPT PRO = INTRADAY (peak incl. unrealized)
    daily_loss: money|none
    min_winning_days: {count: int, threshold: money} | none    # TS 5×150 | TPT none
    consistency: none                                # ambos sin consistencia en funded
    max_position: fixed | balance_tiered             # TPT 6/60 fijo | TS scaling tiers
    scaling: enum {NONE, BALANCE_TIERS}
    buffer_threshold: money|derived    # TS lock MLL en 0 | TPT start+drawdown (52,000)
    payout_eligibility:
      TOPSTEP: winning_days 5×150 + net_since_last ≥ 0.01 (first exempt) + window Sun5PM–Fri5PM CT + compliance
      TPT: day_one + balance ≥ buffer_threshold + flat al solicitar
    payout_cap: {pct_of_balance, cap, min_request}   # TS {50%, 2000, 125} | TPT {none, none, none}
    payout_split: percent              # TS 90 | TPT 80 (primer retiro)
    failure_rules[]

  withdrawal:
    requested_amount: money            # política del trader (M1: primera elegible)
    trader_cash_received: money        # requested × split − fee(método)
    balance_effect: DEDUCT_ON_APPROVAL # TS explícito | TPT equivalente
    drawdown_effect: enum {MLL_LOCK_0_PERMANENT, TRAILING_LOCKED_UNCHANGED}
    continuation_state: enum {SAME_ACCOUNT, CLOSED_INSIDE_BUFFER_50_80}

  economics:
    purchase_cash_flow      = −purchase_cost
    recurring_cash_flows    = −recurring × ciclos_activos − resets × reset_cost
    activation_cash_flow    = −activation_cost (condicional al pass)
    withdrawal_cash_flow    = +trader_cash_received
    other_cash_flows[]      # TS: DOM 38/mes opcional, Back2Funded 599 ≤2×; TPT: PRO reset 649 ≤3×

topstep:                            # extensiones específicas
  reset_credit_por_rebill (1 gratis, expira 1a); rebill pushed +30d por reset
  micros:minis 10:1; ventana payout Sun5PM–Fri5PM CT; aprobación 1–3 días hábiles
  fees método {Aeropay 0, Brokerage 0 same-day ≤12PM CT, ACH 30, Wire 30}
  post-payout: MLL=0 permanente + conteo 5 winning days reinicia; mín request 125
  Back2Funded 599 (≤2×, 30d desde cierre, sólo pre-payout); límite 5 XFA
  inactividad 30d; cierre voluntario ≤50% cap 5000; XFA balance arranca en 0

tpt:                                # extensiones específicas
  promos lifetime (NOFEE40: 40% + waiver 130); renewal mismo día calendario
  comisiones nominales (4.50 RT mini / 1.50 micro) contra balance en Test y PRO
  inside-buffer withdrawal → cierre permanente + split 50/80 (reloj 60d en conflicto TPT-1)
  PRO reset 649 ≤3×; counter-positions prohibidas; máx 5 funded; 10 activaciones/30d rolling
  PRO extra: ≥1 día trading/semana; no bots; exit antes de limit-up/down; FOMC/NFP/CPI ±1 min
  PRO+ (continuation): freeze 5,000, EOD DD −2,000, sin buffer, 90/10
```

Regla de fidelidad: ningún campo común recibe semántica que no le corresponda; toda excepción material vive en `topstep:`/`tpt:`. Balances nominales y personal cash permanecen separados en todo el contrato.

## D5.4 draft — Simulator capability gap matrix (base: D4 certificado d4f42a4)

| capability requerida por Tier-1 | clasificación | detalle / consecuencia de simulador |
|---|---|---|
| barreras de fase + economics F/A/C/W + cohort IID | SUPPORTED | núcleo D4 intacto; reset/rebuy ≈ attempt IID con su fee |
| max_position (5/50, 6/60) | SUPPORTED | `hMax` ya existe como invariante; bajo política fija no cambia la matemática; ratio 10:1 irrelevante en dinero normalizado |
| re-centrado de referencia (XFA balance=0 vs PRO=50,000 nominal) | SUPPORTED | offset de referencia; la equity de fase B arranca en 0 relativo |
| comisiones contra equity nominal (TPT 4.50/1.50; Topstep schedule MISSING) | SMALL_EXTENSION | costo fijo por cierre de trade restado de E en el event loop; rompe la equivalencia exacta D/(T+D) — contabilizar, no ignorar; requiere schedule Topstep (unknown) |
| minimum trading days (TS 2 / TPT 3) | SMALL_EXTENSION | gate de pass sobre la capa de sesiones (condicionado al MATERIAL de sesiones) |
| renovaciones/calendario de suscripción (30d / mes calendario; rebill push por reset) | SMALL_EXTENSION | contabilidad de calendario sobre la duración del attempt; sin cambio matemático |
| payout request→receipt (estados + split + fee método + min request) | SMALL_EXTENSION | transición WITHDRAWAL_REQUESTED→RECEIVED; request→receipt sin riesgo de pérdida de la suma (TS sin clawback; TPT denials operativos) — no cambia el modelo central |
| payout caps/split como función de balance (TS min(50%,2000)/90-10 min 125; TPT 80-20) | SMALL_EXTENSION | función determinista de cash sobre el estado de balance en el primer retiro |
| buffer threshold TPT (52,000 → habilita 80%) | SMALL_EXTENSION | umbral que gatea split/withdrawal |
| capa de sesiones/días (día de trading, PnL diario, marca EOD, winning days, day locks 3:10/4:00 PM CT) | MATERIAL_EXTENSION | D4 no tiene dimensión temporal: se requiere grid de sesiones con PnL diario agregado; habilita min-días, winning days, consistencia y las marcas EOD del trailing |
| EOD trailing drawdown con lock en balance inicial (TS Combine MLL, TS XFA MLL, TPT Test) | MATERIAL_EXTENSION | estado de máximo balance EOD; bajo proceso null continuo, floor trailing ≥ floor estático ⇒ p_pass_trailing ≤ D/(T+D): la barrera estática de D4 SOBREESTIMARÍA p_pass |
| intraday trailing drawdown sobre peak incl. unrealized (TPT PRO) | MATERIAL_EXTENSION | estado path-dependent del running max con ratchet continuo; cambia la semántica de barreras/kernel |
| consistencia (TS 55% target dinámico Best Day÷0.55; TPT 50% gate al pass con goal 2× best day) | MATERIAL_EXTENSION | requiere distribución diaria del path (sesiones) y target/gate dinámicos → condición de pass path-dependent |
| payout eligibility por winning days (TS 5×150 + net≥0.01 + ventana) | MATERIAL_EXTENSION | condición de transición dependiente de sesiones |
| scaling funded por balance (TS XFA tiers, prohibición intradía) | MATERIAL_EXTENSION | límite de posición = función escalonada del balance |
| DLL add-on Topstep (1,000, flatten sin falla; dobla caps — offer excluida) | DEFER | opcional en el path base; no quema ni invalida; sensibilidad posterior |
| restricciones de sesión/overnight (flatten 3:10 PM CT / 4:55 PM ET / feriados) | DEFER | sin modelo de tiempo no existen posiciones overnight; simplificación estructural declarada |
| news restrictions (TS conducta; TPT PRO FOMC/NFP/CPI ±1 min) | DEFER | restricción conductual/ventanas puntuales; no barrera económica del null model |
| conducta prohibida / copy trading / account limits / Cooldown 60d | DEFER | exclusiones, no barreras económicas; multi-cuenta fuera de M1 |
| activation deadlines | DEFER | no existen en ninguna de las dos props (MISSING documental) |
| Back2Funded 599 ≤2× (TS) y PRO reset 649 ≤3× (TPT) | DEFER | recuperación paga condicional post-failure; capturada en ledger; entra como sensibilidad si el owner la pide |
| post-withdrawal continuation (TS MLL=0 + restart conteo; TPT cuenta sobrevive) y payouts #2+ | DEFER | éxito D5-M1 = primer WITHDRAWAL_RECEIVED; capturado como continuation_state |

Síntesis del gap: el núcleo matemático D4 (first-passage exacto, adds self-financing, lifecycle, cohort, economics) se conserva; la extensión dominante es UNA capa de sesiones/días (MATERIAL) que habilita trailing EOD, consistencia, min-días y winning days; el trailing intraday de TPT PRO es la segunda pieza MATERIAL; el resto son extensiones locales o diferimientos explícitos.

## D5 — Evidence register (captured_at 2026-09-24)

- Jerarquía aplicada: official current documentation > official FAQ/terms > official pricing/product page > secondary (sólo SECONDARY_FLAG). Secundarias jamás establecieron una regla.
- Re-verificación verbatim del manager (fetch directo en sesión): Topstep 14289835 (pricing), 8284204 (MLL), 8284208 (consistency, confirma target $3,000 explícito), 8284233 (payout policy, confirma tabla de caps por tamaño), 8284215 (XFA parameters), 8284197 (TC parameters); TPT 15170265979165 (Rule 3: tabla $50,000/6/$3,000/$2,000 + mecánica EOD completa), 15172219527581 (profit split + buffer + inside-buffer), 15172253980061 (PRO→wallet), 29660646764445 (NOFEE40: $102 plana + waiver $130).
- Captura de campo por agentes de research con cita verbatim por regla: resto de URLs listadas en D5.2A/D5.2B (Topstep: 18 artículos Help Center + express-funded-account-rules; TPT: 30 artículos zendesk + FAQ + homepage + terms). Freshness registrada por página (Topstep Help Center mayormente jun–ago 2026, varios "updated this week"; topstep.com/express-funded-account-rules stale 2025-06-26; TPT zendesk may–sep 2026, Rule 5 y PRO Rules 2026-09-22; FAQ TPT sin fecha visible).
- Re-fetch NO reverificable en sesión: TPT 15141145057053 (Test subscriptions) — WebFetch 403 + reader error ×2 ⇒ confidence apoyada en cita verbatim del agente + doble corroboración cruzada (reset article y NOFEE40 FAQ oficiales).
- /verify: 12/12 ítems del mandato cumplidos (fuente oficial por regla, capture date, contradicciones en RULE_CONFLICT, proveedor/producto/fase en toda regla, requested≠received separados, nominal≠personal cash separados, q=10% no usado, contratos reproducibles, gap completo, cero código, D4 intocado, Tier-2 no investigado).

## D5 — Reuse (artefactos autoridad D5)

Sobreviven como autoridad: paquete de reglas Topstep (§D5.2A), paquete TPT (§D5.2B), contrato normalizado candidato (§D5.3 draft), RULE_CONFLICT register (§D5), unknowns consolidados (§D5), simulator capability matrix (§D5.4 draft), evidence register (§D5). No se crearon abstracciones genéricas adicionales sin evidencia.

REUSABLE_BEHAVIOR_CANDIDATES (para rule-capture Tier-2 futuro): (1) capturar schedule de comisiones/data fees explícitamente — quedó MISSING en Topstep; (2) extraer precio list desde la tabla/API de pricing cuando el HTML es JS-rendered (caso TPT $170 derivado); (3) registrar `updated_at` de cada artículo vía API del help desk cuando la página no muestra fecha; (4) fetch cruzado marketing site + help desk siempre — las páginas marketing se desactualizan (causa de TS-2); (5) snapshot archive (p.ej. Wayback) de cada URL citada en captured_at para inmunidad ante ediciones futuras.


## Manager Review — D5.2 Tier-1 Rule Capture — 2026-09-24

Status: **REVIEW_WITH_FINDINGS**. El paquete de research es materialmente bueno y suficiente para continuar el diseño, pero NO está listo para `D5_TIER1_RULES_CAPTURED=ACCEPTED` todavía.

### Findings

1. **TS-1 no es un RULE_CONFLICT material.** La página XFA usa un headline genérico "up to $5,000*" y remite explícitamente al Payout Policy para el cap por account size. El Payout Policy vigente fija 50K XFA Standard = **$2,000**. Resolver TS-1 a `$2,000` para el path congelado sin DLL add-on.
2. **TPT automation compatibility = BLOCKER de producto, no DEFER.** PRO Rules prohíbe trading bots/algos y exige ejecución manual. La Trade Copier Policy sí permite copiar entre cuentas propias, pero sólo mediante copiers aprobados/platform-native; un copier custom no está aprobado por defecto. Antes de invertir en soporte TPT para Echo Futures debe determinarse si el target operativo será manual-reference + approved copier, o si TPT queda economics-only / NO_GO para automation.
3. **WithdrawalPolicy falta como contrato separado.** Las reglas no determinan por sí solas cash EV. Topstep permite elegir requested amount dentro de min/cap; TPT permite dos rutas materialmente distintas: esperar buffer y retirar 80%, o retirar dentro del buffer cerrando PRO con split 50%/80% según antigüedad. D5 debe modelar `WithdrawalPolicy` separada de `PropRuleSet`.
4. **TPT inside-buffer path es material para q_withdraw.** Como success = primer cash real, cerrar dentro del buffer puede lograr WITHDRAWAL_RECEIVED antes de alcanzar $52K. No se puede ignorar sin congelar explícitamente una policy.
5. **TPT pricing debe ser snapshot/scenario.** List price 50K = $170/month; homepage vigente muestra $102/month bajo 40% promo y promo docs indican activation $130 waived para cuentas elegibles. No mezclar precio promocional con regla estructural.
6. **Principal gap matemático: session boundary.** D4 no tiene tiempo/días. EOD trailing, consistency y winning-days necesitan una definición estocástica del estado al cierre de sesión; no basta agregar contadores. Antes de Shot A debe congelarse un session-aware null model o una abstracción equivalente validada matemáticamente.
7. **Commissions/costs:** no mezclar schedules incompletos. O capturar schedules comparables de ambas props o congelar explícitamente `execution_cost_model=0` para el primer structural-null result y correr sensibilidad después.

### Required resolutions before SPEC freeze

- R1: Topstep 50K Standard payout cap = $2,000 for the frozen path.
- R2: Decide TPT operational compatibility posture: `AUTOMATION_COMPATIBLE | MANUAL_REFERENCE_ONLY | ECONOMICS_ONLY | DROP_TIER1`.
- R3: Freeze first-withdrawal policies to simulate; minimum required: `MAX_ELIGIBLE` and TPT `CLOSE_INSIDE_BUFFER` vs `WAIT_FOR_BUFFER`.
- R4: Freeze pricing scenarios: list/base vs current promo snapshot.
- R5: Produce a mathematically reviewed session-aware extension design before implementation.
- R6: Resolve execution-cost posture for M1.

### Gate

`D5_TIER1_RULES_CAPTURED` remains **REVIEW_WITH_FINDINGS**.
Do not start implementation. Next action: resolve R1–R6, then freeze Functional/Technical SPEC.


## D5-M1 — Tier-1 Prop Economics Vertical Slice

### Observable outcome

Using the certified D4 simulator baseline, reproduce the complete real-rule lifecycle for:
- Topstep 50K Trading Combine Standard → XFA Standard;
- Take Profit Trader 50K Test → PRO;

from evaluation purchase until either:
- `WITHDRAWAL_RECEIVED`; or
- `BURNED`.

The first milestone is **not** “support prop rules generically”. It is a bounded research capability that answers, under the null model, for each Tier-1:
- `P(pass evaluation)`;
- `P(funded | pass)`;
- `P(payout eligible | funded)`;
- `P(first withdrawal | funded)`;
- `q_withdraw`;
- expected evaluations / first withdrawal;
- burn/activation counts;
- no-withdrawal probability after 5/10/20/50 evaluations;
- expected cash per evaluation;
- cumulative cash before first withdrawal;
- cash P5/P50/P95;
- net cash per 10 and 100 evaluations;
- minimum/trading-day path where the rules make time relevant.

### Delivery sequence

1. **Rules capture — Topstep and TPT only.**
   Official sources, exact 50K path, capture date, conflicts and ambiguities.
2. **Normalization.**
   Create a common lifecycle/rule contract plus explicit prop-specific exceptions.
3. **Simulator gap analysis.**
   Map every required rule to `SUPPORTED | SMALL_EXTENSION | MATERIAL_EXTENSION | DEFER`.
4. **SPEC freeze.**
   Functional + technical SPEC for the minimum D4 extension required by Topstep/TPT.
5. **Three development shots.**
   Shot A implementation; Shot B fresh independent falsification; Shot C accepted corrections + certification.
6. **Null experiments.**
   No synthetic edge first. Produce Tier-1 economics from real rules.
7. **Owner gate.**
   Only after M1 passes, expand to Tier-2 and conditional edge/hardscalping sensitivities.

### Explicit non-goals M1

- Apex/MFFU/Tradeify implementation.
- FTMO Futures.
- empirical strategy edge.
- NinjaTrader/Echo integration.
- historical futures backtest.
- multi-prop generic framework beyond what Topstep/TPT force.
- payout #2+ optimization unless a rule is required to compute first withdrawal correctly.
