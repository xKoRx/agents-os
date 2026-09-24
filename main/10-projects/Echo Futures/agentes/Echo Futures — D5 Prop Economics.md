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
- **D5.2A/D5.2B capturadas 2026-09-24 (REVIEW).** Paquetes oficiales reutilizados. En D5.3 el mandato owner resuelve TS-1 a cap $2,000 y TPT-1 a 60 trading days; TS-3 y TPT-2 ya estaban resueltos. TS-2 queda histórico fuera del scope sin recovery. Contrato y gap matrix anteriores son drafts parcialmente superseded por §D5.3 Session Model Review; allí están los bloqueos vigentes. Sin código; D4 intacto; Tier-2 no investigado.

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
| TS-1 | Topstep | cap por tamaño frente a headline genérico de XFA | help.topstep.com/en/articles/8284233 | help.topstep.com/en/articles/8284215 · topstep.com/express-funded-account-rules | RESUELTO por mandato owner D5.3: $2,000 para 50K XFA Standard sin DLL add-on; no hay conflicto material del path congelado. |
| TS-2 | Topstep | ventana de decisión Back2Funded: 30 días calendario (Help Center 12060405, actualizado 2026-08-14, ampliado desde 2026-05-29) vs 7 días (topstep.com/express-funded-account-rules, actualizado 2025-06-26) | help.topstep.com/en/articles/12060405 | topstep.com/express-funded-account-rules | RULE_CONFLICT ABIERTO (página marketing stale) — Help Center más nuevo gana por jerarquía §regla comercial 8; no material para first withdrawal (recuperación post-failure). |
| TS-3 | Topstep | consistencia en XFA Standard: frase del artículo de consistency ("choose Standard or Consistency as your Payout path") vs tabla de Parameters (Standard: ❌) | help.topstep.com/en/articles/8284208 | help.topstep.com/en/articles/8284215 | RESUELTO — Standard no tiene consistency target (tabla + eligibility del Payout Policy sin consistencia). |
| TPT-1 | TPT | reloj inside-buffer, tabla abreviada frente a nota explícita de trading days | zendesk 15172219527581 (tabla) | zendesk 15172219527581 (nota) | RESUELTO por mandato owner D5.3: trading days; ≤60 split 50%, >60 split 80%. No reabrir como días calendario. |
| TPT-2 | TPT | Test drawdown: "calculated only at the end of the trading day" vs liquidación inmediata intradía incl. unrealized (mismo artículo) | zendesk 15170265979165 | zendesk 15170265979165 | RESUELTO como semántica normalizada: el trailing se ACTUALIZA EOD; el breach se ENFORCEA intradía incl. unrealized. |

SECONDARY_FLAGS: ninguno que contradiga fuente oficial (secundarias Topstep consultadas corroboran $3,000/$2,000/EOD-lock; TPT no usó secundarias).

## D5 — Unknowns consolidados (captured_at 2026-09-24)

Topstep: status list-vs-promo del precio $49; inactividad en Combine; deadline de activación XFA; si el día de trading requiere ≥1 trade (implícito); tabla completa de scaling tiers (imagen no textual); frequency cap de payouts (ninguno declarado); población exacta del legacy "100% primeros $10K"; schedule de comisiones por trade (no capturado en ninguna página oficial).
TPT: list price $170 no impreso directamente (derivado triple-consistente); deadline de activación PRO; destino del $130 si el PRO falla después; mínimo PRO→wallet; "no daily loss" explícito en PRO; frase textual del efecto del retiro sobre el drawdown lockeado; inactividad Test; número de reintentos de pago; cutoff horario fijo de payout request.

## D5.3 draft histórico — Contrato normalizado candidato (PropRuleSet)

**Superseded parcialmente por §D5.3 Session Model Review.** Los importes de compra/activación/renovación pertenecen a `PricingSnapshot`; el momento y monto elegido de retiro pertenecen a `WithdrawalPolicy`. El draft se conserva como antecedente, no como contrato implementable. Cap Topstep congelado = $2,000; reloj inside-buffer TPT = trading days. No implementar desde este bloque.

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

**Delta D5.3:** sesiones/flatten obligatorio y compatibility TPT ya no son DEFER: se diseñan en §D5.3 Session Model Review. Trading fees quedan excluidos explícitamente del structural null; pricing sale de PropRuleSet. La matriz siguiente conserva el diagnóstico inicial, no autoriza implementación desde sus simplificaciones.

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

## D5.3 Session Model Review — 2026-09-24

### Mandato, autoridad y decisiones que prevalecen

Diseño matemático, no Functional/Technical SPEC. Baseline certificado: `d4f42a41946f12231b75e4eb65b90d132731be0d`; [[D4 — Simulator v0 Functional SPEC]], [[D4 — Simulator v0 Technical SPEC]] y [[echo-futures-astra-math-review]] permanecen CLOSED/intactos. Esta sección sustituye los drafts D5.3/D5.4 sólo donde afectan sesiones, trailing, contadores/consistencia, retiro, precios y compatibilidad TPT. Los paquetes D5.2 se reutilizan; no se repite research de firmas ni se amplía Tier-1.

| Decisión | Resultado de este diseño |
|---|---|
| Modelo v1 recomendado | `CLOCKED_BROWNIAN_SESSION_KERNEL`: Brownian continuo sin drift, reloj de varianza explícito, kernel conjunto de primer evento/supervivencia a fin de intervalo; máximo intradía para TPT PRO |
| Costes de ejecución M1 estructural | `execution_cost_model = ZERO_STRUCTURAL_NULL`, explícito y separado de cash fees; no representa ejecución neta real |
| Synthetic edge en sesiones | Sólo `delta=0`; rechazar `delta≠0` en este modelo. D4 legacy retiene su contrato synthetic y T7/T8 |
| TS-1 | RESUELTO por mandato owner: Topstep 50K XFA Standard sin DLL add-on, cap bruto $2,000/request |
| TPT-1 | RESUELTO por mandato owner: ≤60 trading days → 50%; >60 trading days → 80% al cerrar dentro del buffer |
| TPT para el target Echo automatizado | `ECONOMICS_ONLY`; permanece comparación económica Tier-1, no candidato aprobado para ejecutar bots |
| Éxito | `WITHDRAWAL_RECEIVED` con cash externo neto positivo; request, aprobación y wallet son estados intermedios |
| Gate / próximo paso | `D5_SESSION_MODEL_PASS = REVIEW` / `MATH_REVIEW`; sólo el owner acepta |

### A1 — Qué información falta y por qué contadores no bastan

D4 entrega `P(τ_U<τ_L)=(x−L)/(U−L)` sin modelar `τ`. La misma probabilidad corresponde a cualquier volatilidad positiva constante, pero cambiar la volatilidad cambia radicalmente cuántos eventos ocurren antes del cierre. No se puede inferir de D4 una distribución de PnL diario, cantidad de días, coste de renovaciones ni winning days. Tampoco se puede muestrear una duración independiente del lado de salida: ambos están correlacionados.

En cada tramo de posición constante se necesita la ley conjunta de `(τ, tipo_de_evento, estado_en_τ)` si un evento ocurre antes del próximo límite temporal, o `(estado_al_límite | ningún_evento_previo)` y su probabilidad de supervivencia. El endpoint sin condicionar puede pertenecer a un path que ya quebró. En TPT PRO, además hace falta el running maximum y el orden temporal de sus incrementos y descensos: un máximo y un mínimo de sesión sin orden no determinan si hubo drawdown. Se requiere kernel con absorción continua, no reconstruir un camino ficticio desde el retorno diario.

### A2 — Alternativas examinadas

| Candidato | Compatibilidad con D4 y adds | Sesgo / auditoría null | Complejidad / reproducibilidad | Decisión |
|---|---|---|---|---|
| A. Brownian continuo, horizonte finito, implementado con pasos Euler/retornos Gaussianos | Mismo proceso en el límite; una malla finita pierde primeros cruces y orden de adds | Ignora cruces entre nodos, típicamente sobreestima supervivencia y subestima ratchet. Media gaussiana cero no demuestra null para el proceso detenido implementado | Media; reproducible con seed+malla, pero resultados dependen de malla y correcciones | Rechazado como motor de referencia v1; útil sólo como contraste con convergencia |
| B. Kernel Brownian conjunto de sesión/primer evento, extendido a `(equity, máximo)` cuando corresponde | D4 es su marginal de salida sin deadline. Conserva precios de adds y bookkeeping, tiempo correlacionado y censura correcta | Cero sesgo estructural de discretización temporal en la ley matemática; aproximación numérica exige error declarado. Martingala auditable | Media para barreras fijas; alta pero acotada para PRO antes del lock. Seed + versión de kernel/tolerancias/calendario determinan resultado | **SELECCIONADO**: una ley continua con dos estados mínimos de kernel según fase |
| C. Una distribución de retorno diario encima de los wins/losses D4 | Generalmente incompatible: dobla fuentes de PnL o pierde la relación entre exposición, adds y duración | Puede forzar media cero diaria y aun así sesgar ruina, consistencia y q. Calibrar varianza no recupera el orden del path | Baja y reproducible, pero la reproducción no valida la ley | Rechazado. Si la distribución incluye exactamente todos los eventos y máximos condicionados, ya es B |
| D. CTMC/random walk en retícula o reloj de número fijo de trades por día | Admite adds sólo con estados alineados; las duraciones implícitas dependen de política. Retícula no preserva Brownian/D4 salvo límites controlados | Overshoot, redondeo de barreras y muestreo artificial de EOD cambian la probabilidad. Puede ser martingala de otro modelo | Media; excelente como oráculo independiente de refinamiento | Rechazado para producción v1; aceptado como oráculo numérico con límites y refinamiento |

Un Brownian bridge es una forma de realizar B, no una licencia para muestrear endpoint, máximo y cruces independientemente. Una bridge bajo dos barreras debe condicionarse a supervivencia y respetar el primer evento; PRO requiere también el máximo continuo y su dependencia con la absorción. El contrato elegido fija esa ley aunque la futura revisión técnica elija una representación numérica equivalente.

### A3 — Proceso, tiempo y política de exposición mínimos

Usar unidades normalizadas de precio de D4: `dS_t = σ_z(t) dW_t`, drift cero, con reloj `v(t)=∫σ_z(u)²du`. `σ_z(t)` es determinista, piecewise constant y positivo en ventanas activas; fuera de ellas no hay posición ni exposición. Para referencia puede expresarse `ν_session=∫session σ_z²dt`, pero no se debe identificar un día calendario con una unidad Brownian sin declarar esa escala. Una sesión más corta reduce `ν` bajo la misma tasa por hora; no se renormaliza silenciosamente a un día completo.

`σ`, `G`, `L`, `h0`, lista finita de adds y `hMax` son inputs hipotéticos identificados en cada escenario. No hay estimación empírica, cifra base de q ni escala de volatilidad inferible de D4. La familia `q_withdraw(ν, TradePolicy, WithdrawalPolicy, calendario, settlement)` es la salida correcta hasta congelar escenarios; variar ν es sensibilidad estructural, no edge. Los límites de posición y unidades de contrato deben validarse en el escenario; no introducir scaling ficticio. Una v1 puede usar exposición siempre dentro del mínimo límite permitido y dejar scaling variable fuera.

Política de trading de referencia propuesta: abrir al inicio de cada ventana activa; cerrar por TP/SL o breach; reabrir inmediatamente tras TP/SL mientras la ventana siga abierta; ningún límite artificial de trades/día. Usar el último evento antes de cada corte determinista y liquidar la posición superviviente a su precio condicionado. No llevar posición ni add pendiente a la sesión siguiente. Cortes de noticias/early close son ventanas exógenas versionadas, con flat obligatorio y reapertura posterior; no crean trading days adicionales. No se impone un profit stop diario implícito ni se deja de operar por tocar $3,000 intradía. Las decisiones de pass/retiro de esta v1 se evalúan sobre el snapshot diario completo; es una política EOD explícita, no afirmación de que la firma prohíba terminar antes.

La política EOD puede perder ganancias logradas intradía antes de que se reconozca pass/eligibility; esa diferencia frente a una política de flatten temprano es real y debe etiquetarse. Optimizar stopping intradía sería otro escenario, no un arreglo que pueda inventar el coding agent. El modelo continuo tiene tiempos de decisión discretos para retiros: evita la política patológica «cerrar en el primer instante con ganancia >0», cuyo ínfimo en Brownian puede ser cero sin un primer beneficio positivo bien definido.

El proceso nominal self-financing sigue siendo `E_t = E_0 + ∫H_u dS_u`. Con `0<h0≤H≤hMax<∞` durante exposición, un número finito de adds por trade y horizontes acotados, `E[E_{t∧τ}]=E_0` y `E[(E_{t∧τ}−E_0)²]=E[∫_0^{t∧τ}H_u²σ_z(u)²du]`. Cierre/reapertura sin costes no cambia equity. Para un tiempo de éxito ilimitado, no basta invocar optional stopping: verificar absorción/integrabilidad o reportar censura y cotas; no asegurar media terminal cero sin esas condiciones.

Los adds mantienen exactamente `Y=b+h·s`, `h'=h+Δh`, `b'=b−Δh·s`, `Y'=Y`. Son acciones adaptadas al estado actual, nunca al futuro endpoint de una bridge; conservar orden y exclusión de adds fuera de barreras D4. **Lo que no se conserva como claim universal es la invariancia de p frente a sizing:** con sesiones, trailing y day gates, cambiar H cambia duración y distribución diaria aun sin drift. Tampoco se aplica `D/(T+D)` al ruleset real.

### A4 — Contrato matemático del kernel seleccionado

Para cada estado Z y tiempo de varianza restante V hasta el próximo corte exógeno, definir `τ = inf{v≥0: ocurre una barrera económica o un evento de trading}`. El kernel devuelve exactamente una de estas ramas, con su masa conjunta:

- `EVENT`: `(τ≤V, tipo, Z_τ)`, con tiempo, precio, equity y máximo si corresponde. Se consume τ del reloj; un trade nuevo no reinicia el tiempo restante.
- `SURVIVED_TO_BOUNDARY`: `(τ>V, Z_V)`. Se conserva toda la masa superviviente; no se sustituye `Z_V` por una normal incondicional ni por la barrera que se habría tocado después.

En Topstep y TPT Test el loss floor es constante dentro de cada sesión. Entre eventos, los niveles de precio son los de D4 reemplazando `−Drawdown` por el floor vigente; el phase upper absorbente está desactivado en modo prop EOD. `lowerEvent` es el siguiente add elegible o la barrera inferior terminal; `upperEvent` es TP. Con `a<x<b`, `ℓ=b−a` y varianza V, la densidad subprobabilidad de endpoint superviviente es:

`k_V(x,y) = (2/ℓ) Σ_{n≥1} sin[nπ(x−a)/ℓ] sin[nπ(y−a)/ℓ] exp[−n²π²V/(2ℓ²)]`, para `a<y<b`.

Su integral es supervivencia. Las densidades conjuntas de salida por unidad de varianza son `f_a(v|x)=½ ∂_y k_v(x,y)|_{a+}` y `f_b(v|x)=−½ ∂_y k_v(x,y)|_{b−}`. Integrar salidas hasta V más supervivencia da 1. La mezcla fija el evento y su duración; si sobrevive se usa `k_V/∫k_V`. Al integrar `f_b` hasta infinito se recupera exactamente `(x−a)/(b−a)`. El cambio de tiempo determinista convierte v en hora de calendario; no se muestrea una duración independiente. Esta formulación es derivación matemática del modelo propuesto y queda sujeta a revisión.

Para TPT PRO antes del lock usar equity `e` y máximo `m`, ambos relativos al inicio de fase, con `m≥max(0,e)` y `F(m)=min(0,m−D)`, D=$2,000. Entre acciones `de=h·dW_v`, `dm` sólo aumenta cuando e marca máximo; matar el proceso al tocar `e≤F(m)`. Los TP/SL/adds se mapean a niveles de e con el bookkeeping vigente y compiten con ese killing. La ley requerida es la distribución conjunta del primer evento `(τ,tipo,e_τ,m_τ)` o supervivencia `(e_V,m_V)`, nunca dos draws marginales independientes.

Caracterización suficiente para revisión/realización numérica: semigrupo detenido de `(e,m)` con generador interior `𝓛=(h²/2)∂²_e`, frontera absorbente `e=F(m)` y fronteras de trading etiquetadas según el primer evento. En la diagonal `e=m<D`, las funciones backward del dominio cumplen `∂_m u(e,m)|_{e=m}=0`; al alcanzar `m=D` se empalma al kernel 1D con floor fijo 0. Condición inicial de semigrupo identidad y datos de frontera de cada evento fijan la ley; las acciones add/close cambian coeficientes/estado sólo después del evento. El máximo no se resetea al cerrar trades ni al terminar días. Tras lock, almacenarlo completo deja de ser necesario para reglas de primera extracción: bastan `locked=true` y F=0.

La ley es exacta; una implementación de series/inversión/PDE puede ser aproximada. El gate no promete un sampler exacto de PRO aún construido ni una solución cerrada para q. No se admite anunciar «exacto» si el evaluador usa malla sin cota de error. La revisión matemática debe aceptar la realización y presupuesto de error antes de SPEC freeze; si no resulta viable, volver a REVIEW del diseño, no sustituirlo silenciosamente por retornos diarios.

### A5 — Estado de sesión y orden de eventos

Estado mínimo adicional al de D4: identificadores de fase/sesión; timestamp y tiempo de varianza restante; balance realizado relativo B; equity E; balance inicial del día `B_open`; PnL realizado del día y provisional; flag de entrada/round-trip; siguiente add; máximo EOD `H_EOD`; floor F y flag lock; máximo intradía M sólo para PRO no lockeado; trading days `N`; winning days `W`; best locked day `A`; snapshot publicado y su session_id; ledger de retiros/settlement; próxima fecha de renovación. Phase equity 0 representa 50,000 nominales en Combine/Test/PRO y 0 en XFA. La referencia nominal nunca es depósito personal.

| Boundary | Modelo y etiqueta |
|---|---|
| Topstep | Sesión abre 17:00 `America/Chicago`, flatten/lock del PnL diario 15:10 del siguiente día habilitado; winning-day publication 16:00. El intervalo 15:10–16:00 no añade PnL ni otra sesión |
| TPT | Trading day 18:00–17:00 `America/New_York`; hard flatten 16:55. Mantener plano hasta el corte. Snapshot de dashboard posterior, publicado en ventana 20:00–21:00 Eastern; no es una segunda sesión |
| Holidays / DST | Calendario de sesiones versionado, IANA timezone y versión tzdb; incluir early close y fines de semana. No usar UTC−5 fijo ni timezone de Chile |
| TPT publicación durante sesión siguiente | Si el snapshot previo aún no está publicado, la policy espera plana antes de request. No combinar balance de ayer con PnL abierto de hoy. Fijar latencia de publicación en el escenario; 21:00 Eastern es supuesto conservador posible, no SLA |
| Inactividad / edad | Días de actividad son por session_id con ejecución, no por fecha civil ni número de trades. PRO age se reinicia al activar; los días Test no cuentan. El contador PRO usa ≥1 round-trip; la liquidación EOD del trade abierto completa el round-trip |

Secuencia de cierre de sesión para sobrevivientes:

1. Resolver cualquier breach intradía, incluido tocar floor al límite: tiene prioridad absoluta y no puede ser rescatado por el endpoint final ni por un retiro. Conservar prioridad D4 phase-loss > trade-close > add; en empate con hard close, cerrar antes de ejecutar un add o reabrir. Un empate exacto tiene probabilidad cero en el modelo regular, pero las fixtures deben ser deterministas.
2. Liquidar posición superviviente a `S_close` condicionado, cancelar órdenes y fijar `B_close=E_close`. No generar precio ni PnL adicionales durante publication lag.
3. Calcular `d=B_close−B_open` en fases sin transferencias; en general excluir débitos de payout/deposit de d. Comisiones nominales entrarían aquí y en equity cuando se devenguen; M1 estructural usa 0. No mezclar fees personales de compra/activación con PnL del día.
4. Actualizar `N←N+1{actividad}`, `A←max(A,d,0)` y, sólo XFA, `W←W+1{actividad y d≥150}`. Cada session_id una vez; los contadores se publican cuando corresponde. Pérdidas no borran best day ni W. Sin actividad no hay winning day, aunque exista un crédito externo.
5. Aplicar ratchet EOD donde corresponda y volver a validar solvencia frente al nuevo floor. Registrar lock. En PRO no hacer un segundo ratchet EOD: ya se aplicó continuamente.
6. Evaluar pass EOD y transicionar sólo después de publicación/activación; reset de variables de fase y del historial diario, sin transferir profit de evaluación. Primer funded trade en una nueva ventana completa elegible de esta policy. Publicar eligibility XFA sólo a las 16:00; retirar usando snapshot autorizado y cuenta flat.

Para EOD trailing: `H_j=max(H_{j−1},B_close,j)`, `H_0=0`, `F_j=min(0,H_j−2000)`, `F_0=−2000`; dentro del día j se aplica `F_{j−1}`. Equivalente `F_j=max(F_{j−1},min(0,B_close,j−2000))`. Nunca decrece; lock permanente cuando H alcanza 2000. Para PRO: `M_t=max(0,sup_{u≤t}E_u)`, `F_t=min(0,M_t−2000)` continuamente, incluso ganancias no realizadas. Un add self-financing no produce nuevo máximo por sí mismo. Un retiro tampoco baja F/M. En XFA el primer payout fuerza F=0 aunque el ratchet no hubiese llegado allí.

### A6 — Consistencia y winning days

Definir `P=B_close` como net profit acumulado relativo de evaluación y `A=max(0,d_1,…,d_N)` con días cerrados. La evaluación permanece activa si falta consistencia; no quema la cuenta ni borra pérdidas.

- **Topstep Combine:** `N≥2`, `P≥3000` y `A≤0.55·P`. Target efectivo `T_TS=max(3000,A/0.55)` sin redondeo de elegibilidad. El provisional intradía usa `max(A_locked,d_current,0)`; se congela al cierre, no se sustituye por máximo intradía de equity. Más profit en el mismo día eleva también ese día y puede elevar el target. El diseño EOD no adelanta el pass por haber tocado el target viejo. Fuente focal: [Consistency at Topstep](https://help.topstep.com/en/articles/8284208-consistency-at-topstep).
- **TPT Test:** `N≥3`, `P≥3000` y `A<0.50·P`, estrictamente. Registrar frontera `P>2A`; `max(3000,2A)` solo no basta porque admitiría igualdad cuando `P=2A`. Comparar mediante productos cruzados con reglas numéricas explícitas; no reemplazar `<` por `≤` ni por un epsilon favorable. Fuente focal: [Rule 5: Be Consistent](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15170316538013-Rule-5-Be-Consistent).
- **Topstep XFA Standard:** no consistency gate. W cuenta días con PnL neto final ≥150; cinco días no consecutivos habilitan el componente de días. Una ganancia intradía de 150 que termina en 149.99 no cuenta. El primer request está exento de profit positivo desde un payout previo; no está exento de balance suficiente, mínimo, cap ni receipt.

### A7 — Compatibilidad exacta y límites de D4

Preservado: proceso null sin drift, bookkeeping self-financing, barreras continuas sin overshoot, adds finitos adversos, prioridad de eventos de D4, aislamiento cash/nominal, seed explícita y fixtures legacy. Superseded sólo para el modo D5: ausencia de tiempo, phase-upper como pass instantáneo, resultados terminales siempre ±target/stop, cash W constante y fees C deterministas. Un cierre por horario produce un PnL interior; los fees recurrentes y el cash retirado son variables del path.

La compatibilidad de barreras estáticas se exige al desactivar gates y trailing **y también** quitar liquidaciones forzadas/reset de trade por sesión, o llevar el primer horizonte a infinito. Entonces el marginal de eventos es D4 y la probabilidad de evaluación +3000/−2000 es 0.4. Mantener un cierre finito puede alterar el trade win rate y no tiene por qué recuperar T1–T3; exigirlo ocultaría una contradicción.

Un intervalo matemático de duración cero es identidad de kernel (`K_0=I`), no un trade instantáneo ni un día ganado. Una sesión configurada con duración cero se rechaza; la fixture K0 no ejecuta business events. Desactivar `EOD_update` congela el floor, pero no elimina automáticamente flatten, day gates o reloj. Separar boundaries de mera observación de cierres económicos permite verificar `K_{u+v}=K_uK_v` sin introducir resets. El modo legacy D4 sigue accesible y no necesita simular días para sus T1–T8.

`delta` de D4 perturba un lado terminal sin definir tiempos ni paths condicionados. No existe una extensión única a sesiones: censurar una salida alterada antes de EOD puede crear sesgo inadvertido. Por eso D5 v1 acepta sólo null; `delta≠0` en sesiones es configuración inválida. Un futuro modelo de edge necesitará una ley temporal propia y revisión independiente; no reinterpretar delta como drift físico.

Reproducibilidad: seed + configuración normalizada + IDs/versiones de RuleSet, TradePolicy, WithdrawalPolicy, PricingSnapshot, calendario/tzdb, kernel y tolerancias. Determinismo de orden RNG y serialización. D5 debe repetir sus propios bytes en el mismo entorno soportado; no se promete igualdad bit a bit de muestras D4 vs D5, pues muestrear tiempos consume RNG adicional. La igualdad requerida entre motores es de ley; D4 legacy conserva su contrato original.

### B1 — WithdrawalPolicy separada de reglas

`PropRuleSet` determina una correspondencia legal `AllowedRequests(state)`, mínimos/caps/split/buffer, flatness, ventanas y efectos en cuenta. `WithdrawalPolicy` elige dentro de ella. El contrato conceptual mínimo es: `policy_id/version`; `decision_schedule`; `eligibility_state`; `requested_amount_policy(state, allowed_set)`; `close_account_if_required`; `continuation_policy`; `minimum_positive_external_cash`; `settlement_profile_id`. Estado de elegibilidad distingue `NOT_ELIGIBLE`, `ELIGIBLE_ABOVE_BUFFER`, `ELIGIBLE_CLOSE_REQUIRED`, `AWAITING_DAY_LOCK`, `AWAITING_PUBLICATION`, `PENDING_REQUEST`, `PENDING_RECEIPT` y `UNKNOWN_RULE`. Un campo material desconocido invalida el escenario de reglas completas; nunca se interpreta como permitido.

Convención monetaria: R es débito **bruto** de profit nominal autorizado por la firma; `w=s·R` es entitlement del trader tras split; `c=w−f(w,method)−external_fees` es cash recibido. Seleccionar sólo requests que dejan `c>0`, respetan unidad monetaria de retiro y mínimos oficiales; `minimum_positive_external_cash=0.01 USD` es decisión de policy, no mínimo de firma. Redondear R hacia abajo a centavos para requests; no redondear el proceso Brownian ni los gates de consistencia. Los tests analíticos de martingala preceden el redondeo de retiro.

| Policy | Trigger y requested_amount_policy | close_account_if_required / continuación |
|---|---|---|
| Topstep `MAX_ELIGIBLE` | Primer snapshot/ventana permitida con W≥5, R=`floor_cent(min(0.5·B,2000))`≥125 y cash externo positivo. B es balance XFA relativo, no 50,000+profit | false; flat mientras se procesa. Al aprobar: B←B−R, F←0, reset del ciclo de winning days; cuenta sigue abierta. Absorber experimento sólo en receipt |
| TPT `WAIT_FOR_BUFFER` | Primer snapshot con profit retirable sobre buffer y cash positivo; en escenario `RETAIN_BUFFER`, R=`floor_cent(max(B−2000,0))`, s=0.8. B=2000 exacto da R=0 y **no** éxito | false; conservar buffer, flat mientras request/settlement; registrar cuenta abierta al receipt |
| TPT `CLOSE_INSIDE_BUFFER` | Primer snapshot de PRO con 0<B≤2000 y R=`floor_cent(B)` que produce cash positivo; split s=0.5 si N_PRO≤60, s=0.8 si N_PRO>60. No esperar al día 61 de forma implícita. Si el primer snapshot disponible ya tiene B>2000, usar la misma extracción sobre buffer de WAIT para totalizar la policy, sin cierre | true sólo cuando la ruta lo exige; confirmar cierre total antes de request inside-buffer. Cuenta `CLOSED_FOR_WITHDRAWAL`, nunca confundir con BURNED. Sin reapertura/reset; receipt aún puede ser éxito |

Estas son políticas de decisión en snapshots EOD, no máximos globales de EV ni claims de óptimo. En `CLOSE_INSIDE_BUFFER`, si el neto es cero/negativo por fees, continuar al siguiente día; no fabricar success por un retiro de $1 que no llega como cash. La ruta conservadora sobre buffer es una hipótesis explícita `RETAIN_BUFFER` pendiente de precisión documental del monto máximo, como se indica en B4; no convierte una interpretación en regla permanente.

### B2 — Request no equivale a cash

Lifecycle mínimo: `PURCHASE_EVALUATION → EVALUATION → PASSED → FUNDED → ELIGIBLE → WITHDRAWAL_REQUESTED → APPROVED/DEBITED → WALLET_CREDITED (TPT) → WITHDRAWAL_RECEIVED`. Ramas: `BURNED`, `CLOSED_FOR_WITHDRAWAL`, `RETRYABLE_OPERATIONAL_FAILURE`, `DENIED`, `INCOMPLETE`. El estado económico terminal de cuenta y el estado de liquidación del cobro son ejes distintos: cerrar PRO para retirar no quema el entitlement; un cash pendiente no se contabiliza como recibido. No sumar a K una cuenta de prop ni saldo wallet aún no remitido.

Policy v1: permanecer flat desde decisión hasta receipt; no reutilizar wallet para comprar otra evaluación. Reintentar errores transitorios sin recrear el débito ni recontar el retiro; un rejection definitivo no se convierte en burn matemático. `SettlementProfile=IDEAL_COMPLIANT` puede fijar aprobación/remesa eventual cierta, compliance/KYC satisfechos y latencia explícita, pero resultados se etiquetan **condicionales a settlement ideal**, no probabilidades empíricas de recibir dinero. Latencias/fallos operativos alternativos deben ser inputs, sin porcentajes inventados. Nunca inferir probabilidad 1 real por documentación de plazo típico.

Para TPT, `w≤250` incurre fee de wallet 50; `w>250`, fee de firma 0, más posibles costes del método. El test aplica al monto wallet→externo, no a R antes del split. Sin cartera previa y primera remesa completa, w es el importe de esa remesa. Ejemplos aritméticos, sin calibración: R=200 y s=.5 ⇒ w=100, c=50; R=300 y s=.8 ⇒ w=240, c=190; R=400 y s=.8 ⇒ w=320, c=320, todos con external_fees=0. [Withdrawal Fees](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15172354954525-Withdrawal-Fees) y [PRO→Wallet](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15172253980061-How-to-Withdraw-from-PRO-Account-to-the-Wallet) respaldan separar split, wallet y remesa.

### B3 — Efecto económico que sí puede afirmarse sin simular

Sea `J=1{receipt externo positivo}`, I=activación pagada y `C_path` todos los costes personales del attempt. Entonces `q_π=P(J=1)`, `W_π=E[c|J=1]`, `EV_attempt,π=E[Jc−C_path]=q_πW_π−E[C_path]`; J≤I. La factorización de fases usa probabilidades **condicionales**, no presume independencia entre ellas. Registrar por separado `P(account_open_at_receipt|J=1)`; no equivale a survival indefinida.

| Policy | q y expected attempts | Cash condicional / survival / EV |
|---|---|---|
| MAX_ELIGIBLE | El monto máximo no crea eligibility; bajo mismos tiempos y settlement flat, cambiar R dentro del allowed set no cambia q antes del primer receipt | Mayor R aumenta cash en ese mismo estado si fees netos son monótonos; deja menos colchón y el payout fuerza F=0. No deducir de esto optimalidad global ante otros tiempos/policies |
| WAIT_FOR_BUFFER | Expone más tiempo a ruina antes de retirar; un threshold de buffer no es payout por sí mismo | Busca split 80% y continuidad; cash condicional depende del exceso observado al decision time y fees. Survival al receipt bajo flat/sin fallos operativos se conserva; survival posterior no modelada |
| CLOSE_INSIDE_BUFFER | Puede convertir caminos que fallarían antes de buffer en éxitos. Sólo bajo mismo path acoplado, mismos decision times y settlement ideal, con fallback sobre buffer idéntico, el evento de éxito de WAIT está contenido en el de CLOSE | En rutas de cierre, survival de cuenta =0 aunque haya cash; split 50%/80% y fees pueden producir menos cash condicional. La selección de paths cambia W; no hay ranking general de EV |

Con attempts IID y q>0, `E[N_attempts]=1/q`, `E[failures_before_success]=(1−q)/q`, `P(no withdrawal in n)=(1−q)^n`. Con costes de duración aleatoria, no reemplazar `E[C_path]` por F+A constantes. Si rewards/costs por attempt son integrables y los attempts son IID hasta éxito, `E[cash acumulado hasta éxito]=EV_attempt/q`; incluye el coste del intento exitoso. q=0 ⇒ espera infinita, no dividir por cero. Cohortes con fechas progresivas, promociones que expiran, distintos calendarios o presupuesto limitado no son IID; reportar simulación/recursión por calendario y no usar geometric por defecto.

### B4 — Límite documental del buffer

La fuente oficial fija buffer 52,000 y cierre obligatorio para retirar dentro de él, pero la frase sobre 80% del total no da una ecuación inequívoca del monto máximo conservando cuenta. El draft anterior tampoco aportaba una frase explícita del balance/floor post-retiro. Por eso `R=B−2000` queda como escenario conservador `RETAIN_BUFFER`, no certificación de todo `AllowedRequests`. [Profit Split & Withdrawal Rules](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15172219527581-PRO-Account-Profit-Split-Withdrawal-Rules).

Pregunta concreta antes de certificar la fila TPT de reglas completas: **«En un PRO 50K con balance $52,500 y MAB ya fijo en $50,000, ¿cuál es el máximo débito bruto retirable manteniendo el PRO abierto: $500 o más? ¿Qué balance y MAB quedan después? Con balance exactamente $52,000, ¿hay algún monto positivo retirable sin cerrar? Confirmen también el mínimo PRO→wallet y que las tablas ≤60/>60 cuentan días con trading efectivo desde activación PRO».** No se contactó al vendor. La unidad trading days y el corte 60/61 ya están congelados por owner; se pide definición operativa fina, no reabrir ese freeze.

### C — PricingSnapshot y contabilidad temporal

Contrato conceptual separado: `snapshot_id/version`, provider/product, `captured_at=2026-09-24`, currency USD, source_refs, confidence, evaluation_initial, renewal_amount, renewal_calendar, activation_amount, taxes/other_personal_costs, promo_code, purchase_eligibility_window, entitlement_scope, evidence_status. `PropRuleSet` referencia eventos de cobro/cancelación y entitlement; no contiene precios promocionales como semántica permanente. Una compra conserva su snapshot/entitlement; nuevos attempts no heredan descuentos salvo que el escenario lo declare elegible.

| Snapshot requerido | Compra | Renovación mientras evaluación siga activa | Activación | Semántica |
|---|---:|---|---:|---|
| `TOPSTEP_STANDARD_CURRENT` | 49 | 49 cada 30 días desde compra | 149 | Snapshot actual del path Standard; no afirmar tarifa eterna ni plan sin activation. No DLL add-on |
| `TPT_LIST` | 170 | 170 cada mes calendario | 130 | Escenario list congelado; evidencia original MEDIUM, derivado de promos oficiales, no promover a captura directa |
| `TPT_NOFEE40_SNAPSHOT` | 102 | 102 cada mes calendario para compra elegible | 0 | NOFEE40, descuento y waiver ligados al entitlement comprado; no extender automáticamente a futuras compras |

Fuentes reutilizadas de D5.2: [Topstep pricing](https://help.topstep.com/en/articles/14289835-topstep-pricing-and-payment-questions) y [NOFEE40 FAQ](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/29660646764445). No se vuelve a validar todo el pricing de firmas; estos son escenarios al corte, no cotizaciones futuras. Reset/recovery queda fuera del attempt base: después de burn, cancelar evaluación y comprar un attempt nuevo. La firma no siempre cancela por burn; la cancelación es una acción de policy que evita renovaciones posteriores, no un hecho de RuleSet.

`C_path = F_initial + Σ_{r∈renewals_before_cancellation}F_r + I·A + other_personal_costs`. La activación sólo se cobra cuando ocurre; PnL nominal no paga fees personales. El reloj de renovación es calendario, aunque no se haya operado ese día. Declarar timestamps, cancelación por pass y por burn, timezone de billing y convención de aniversarios de meses cortos. Si la fuente no fija simultaneidad exacta entre pass/cancel y rebill, el escenario debe fijar `billing_tie_order` y reportar sensibilidad de un cargo; no decidirlo por orden accidental del event loop.

Identidad de control en el mismo path TPT y misma policy, con n renovaciones, activación I y misma remesa: `K_NOFEE40−K_LIST=68·(1+n)+130·I`. Cambiar sólo pricing conserva todos los estados nominales, días y q cuando no hay restricción de presupuesto y las policies no dependen de cash personal. Si cambia q, hay acoplamiento indebido o un budget rule que debe declararse. No restar los $130 waived otra vez como rebate. Fees de payout pertenecen al settlement/fee schedule referenciado; no son comisiones de trading.

El structural null v1 **excluye comisiones/slippage nominales en ambas firmas** para preservar la auditoría de martingala y comparabilidad, como permite R6 del manager. Se conservan fees personales de compra, renovación, activación y remesa. Resultado se etiqueta `STRUCTURAL_NULL_ZERO_EXECUTION_COST`; no llamarlo cash EV real neto de ejecución. Un futuro coste nominal convierte la martingala gross en supermartingala neta y requiere schedule comparable, cuándo se cobra por fill/add/close y test de contabilización única.

### D — TPT operational compatibility gate

**Clasificación para el target actual Echo Futures: `ECONOMICS_ONLY`.** El proyecto busca ejecución automatizada y escalable; las reglas PRO prohíben bots/algos y requieren ejecución manual. Una autorización limitada de copia entre cuentas propias mediante herramientas aprobadas no aprueba señales ejecutadas automáticamente, adds algorítmicos ni un copier custom de Echo. Evidencia oficial reconsultada el 2026-09-24: [PRO Account Rules](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15171769361053-PRO-Account-Rules), actualizado 2026-09-22, y [Trade Copier Policy](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/34431176505245-Trade-Copier-Policy).

No se elige `DROP_TIER1`: la comparación económica solicitada sigue siendo útil. `MANUAL_REFERENCE_ONLY` requeriría que el owner adopte un objetivo manual y una herramienta aprobada concreta; no se asume ese cambio. `AUTOMATION_COMPATIBLE` carece de respaldo. Esta clasificación económica es final para el scope actual y no necesita inventar permiso ni esperar al vendor. Para una futura propuesta de integración, el gate de esa **variante** será `BLOCKED_VENDOR_CLARIFICATION` hasta respuesta escrita: **«¿Permiten en PRO 50K que Echo/NinjaTrader genere y ejecute automáticamente entradas, adds, exits y gestión de órdenes? Si sólo admiten referencia manual, ¿qué acciones de gestión pueden automatizarse y está aprobado explícitamente nuestro copier custom/versionado, o debemos usar uno de su lista?»** Sin respuesta afirmativa específica se mantiene exclusión de automatización; no se envió la pregunta.

### E — Acceptance tests nuevos, evidencia y oráculo

Son requisitos propuestos; **ninguno se declara ejecutado** en este mandato sin código. Mantener T1–T8 sobre D4 legacy; añadir los siguientes sin cambiar sus resultados certificados.

| ID | Caso / oracle | Aceptación esperada |
|---|---|---|
| S01 static-barrier limit | Sesiones/gates/trailing/flatten off o primer V→∞; conservar política D4 | Integral de flujo upper = `(x−a)/(b−a)`; media de tiempo de salida Brownian en varianza `(x−a)(b−x)`; T1–T4 recuperados, eval +3000/−2000 =0.4 |
| S02 zero/no-update | K0; boundaries sólo de observación; floor-update off | K0 identidad, sin contador ni RNG/acción de negocio; `K_{u+v}=K_uK_v`; floor fijo. No exigir equivalencia D4 si todavía hay liquidación forzada |
| S03 finite-horizon mass | Kernel 1D serie/flujo, varios x y V | `∫k_V+∫_0^V(f_a+f_b)=1`, no masa negativa, endpoints condicionados interiores. Validar ley conjunta tiempo/lado, no sólo win rate |
| S04 EOD monotonic | B EOD: 0→800→300→2200→1000, sin breach previo | F: −2000→−1200→−1200→0→0. Ganancia unrealized que se pierde antes de EOD no eleva floor EOD |
| S05 locked trail | Alcanzar lock en EOD o PRO y luego subir/bajar equity sin breach | F=0 permanentemente; trades/días/payout no lo bajan. XFA payout fuerza 0 aun si antes era negativo |
| S06 Topstep consistency | Días [1650,1350]; [1800,1200]; luego +300; fixture provisional de día aún abierto | Primer caso pass por igualdad 55%; segundo no pass con P=3000; tercero P=3300, A=1800 sí. Pérdidas no reducen A; target ≥3000 y fórmula A/.55 sin redondeo |
| S07 TPT consistency | Días [1500,1000,500] vs [1500,1000,500.01]; [1400,900,700] | 50% exacto no pass; >3000 en segundo sí; tercero P=3000 y best<1500 sí. Dos días nunca bastan; target no es absorción intradía |
| S08 activity/winning | XFA días netos [150,−50,149.99,200,150,150,150] | W=5 tras siete días; una sesión con 100 trades sólo incrementa una vez. Pico intradía≥150 y EOD<150 no cuenta; quinto día no elegible antes de publication. Día sin actividad/transferencia no cuenta |
| S09 PRO intraday max | Path E:0→1000 unrealized→500 realizado→−1000; otro path llega a 2000 | F:−2000→−1000→−1000 y breach en −1000, aunque EOD posterior hipotético recupere. En segundo lock0 al tocar 2000, sin esperar EOD. Add/close preservan M |
| S10 drawdown analytical | Equity Brownian constante, sin EOD/fees ni controles intermedios, M0=E0=0 | Antes de drawdown D, `P(M_τ≥m)=exp(−m/D)`; llegar al lock m=D tiene prob. e⁻¹. Con target T≥D y lock floor0, `P(hit T before burn)=e⁻¹·D/T`. No confundir con q del ruleset |
| S11 self-financing/null | Adds de T2/T3 con cierres finitos; comparar balance antes/después y martingala detenida a horizonte fijo | Y_before=Y_after; `E[E_{t∧τ}]=E0`; segundo momento igual a varianza integrada esperada. No exigir p_trade=.5 si terminal ahora incluye EOD interior |
| S12 cash identity | TS B=5000 ⇒ R=2000, split .9 y fee0; TPT ejemplos B2; dos callbacks del mismo request | TS B'=3000, c=1800, F'=0. En todos `K=−C_path+Jc`, sin 50K como cash; un solo débito y crédito. Request/aprobación/wallet con J=0; receipt externo positivo J=1 |
| S13 closure/age | PRO age 60 vs61, profit positivo, misma petición inside-buffer; fines de semana y días Test | Split .5 vs .8, PRO cerrado para siempre, cash puede recibirse; días calendario, Test e inactividad no inflan edad. Ningún cierre se etiqueta éxito antes del receipt |
| S14 pricing identity | TPT list vs promo, paths y stream emparejados, n renovaciones | `ΔK=68(1+n)+130I`; q, equity y días idénticos sin budget. TS 30d ≠ TPT mes calendario; burn cancela por policy, no por cancelación ficticia de firma |
| S15 chronology | DST, early close, news cut, carry a publicación en sesión siguiente, snapshot repetido | Flat en cortes, sin eventos fantasma ni día duplicado; tiempos RNG conservados; nunca operar con snapshot obsoleto al solicitar |
| S16 isolation/reproducibility | Mismo seed+versiones; delta0 vs null; delta≠0 con session model | D5 idéntico consigo mismo; delta0 misma ruta null; delta≠0 rechazado. D4 legacy T7/T8 intactos |
| S17 policy coupling | Mismos paths/decision schedule/settlement ideal para WAIT y CLOSE con fallback idéntico | Cada path exitoso WAIT también exitoso CLOSE, salvo fallo de implementación del coupling. No imponer orden a W ni EV; supervivencia de rutas cerradas=0 |
| S18 incomplete/IID | Guard de tiempo antes de terminar; cohortes IID fixture q=.1 y calendario progresivo distinto | No convertir alive/pending en BURNED ni excluirlos del denominador. Para N intentos, S recibidos y U sin resolver: q∈[S/N,(S+U)/N]. Geometric sólo en modo IID; q=.1 exclusivamente fixture |

S10 se deriva de la distribución del máximo antes de drawdown Brownian y del hitting estático después de lock; referencia primaria de control: Landriault, Li y Zhang, [On the Frequency of Drawdowns for Brownian Motion Processes, §2](https://arxiv.org/abs/1403.1183). La composición `e⁻¹D/T` es derivación de este diseño, no cifra de la firma. Hace falsable el tratamiento del máximo incluso cuando los endpoints de sesión parezcan razonables.

**Límite de validación analítica:** las piezas 1D, martingala a horizonte fijo, ratchets deterministas, contadores/consistencia, ledger y límite S10 son analíticamente comprobables. No se dispone aquí de fórmula cerrada para el q completo de sesiones + adds + trailing + políticas + calendario. Una comprobación del ledger y de media cero no certifica ese q.

**Oráculo numérico independiente propuesto:** resolver la ecuación backward de difusión mediante cadena Markov/finite-volume en retícula de `(e,m)` para PRO, y 1D para EOD, con operadores explícitos de add/close/fin de día y backward induction sobre los estados diarios discretos. No reutilizar el sampler ni su función de crossing probability. Comparar primero sin adds, luego un add y finalmente ciclos cortos de 2–7 sesiones con consistencia/withdrawal. Las ventanas deterministas y estados de políticas son los mismos; la representación del proceso y RNG deben ser independientes. Alternativa de contraste adicional: Brownian bridges condicionadas en malla refinada, conservando orden y máximos; un Euler de pasos más pequeños solo no certifica ausencia de cruces omitidos.

Para cada oracle usar mallas Δ, Δ/2, Δ/4 y ampliar dominios truncados; imponer barreras absorbentes desplazadas hacia dentro/fuera para acotar sensibilidad a no alineación. Si no se demuestra una cota rigurosa, etiquetar la estimación de error como empírica, no exacta. Las políticas sobre regiones abiertas (consistencia `<`) requieren ensayos de ambos lados. Congelar presupuesto propuesto `ε_num≤10⁻⁴` para probabilidades y `≤$0.01` para medias cash de fixtures acotadas; validar que el resultado sea estable dentro de él antes de usarlo. Para comparación Monte Carlo analítica aceptar `|p_hat−p|≤5√[p(1−p)/N]+ε_num`; con oracle usar incertidumbre del oracle más MC, sin absorber un sesgo sistemático aumentando sólo N. La revisión puede ajustar presupuestos por justificación, pero el coding agent no puede eliminarlos.

A horizonte no acotado, reportar masa pendiente y extender horizonte hasta cota declarada, o dejar `INCOMPLETE`. Un technical guard de D4 no se transforma en timeout económico. Si el experimento introduce un plazo de abandono, es otra policy con outcome `ABANDONED` y costes explícitos. No publicar `1/q`, cash hasta primer retiro ni EV infinito-horizonte desde runs censurados como si todos hubieran terminado.

### F — Bloqueos remanentes y handoff sin matemática implícita

| Pendiente | Impacto y responsable de resolución |
|---|---|
| Revisión del kernel conjunto, frontera de máximo, sampler/evaluador y presupuesto de error | `MATH_REVIEW` antes de freeze; diseño propuesto, no certificación numérica. Elegir método técnico que realice la ley ya definida; si no viable, devolver al diseño |
| Aceptación owner de v1 | Gate sigue REVIEW; incluye policy de trading/retiro EOD, structural null con coste nominal0 y TPT economics-only. Ninguna SPEC ni implementación autorizada por este gate |
| Escenarios concretos de ν/TradePolicy/calendario | Inputs obligatorios sin defaults inferidos del hitting kernel D4; congelar matriz de sensibilidad y calendario/tzdb antes de ejecutar resultados. No requiere suponer edge |
| `AllowedRequests` TPT sobre/en buffer y mínimo PRO→wallet | Pregunta B4 pendiente; puede estudiarse `RETAIN_BUFFER` como escenario declarado, pero no certificar como regla completa ni elegir policy económicamente superior |
| Billing y publicación/settlement | Fijar timestamps/perfil, convención meses cortos y empates rebill/cancel; snapshot TPT usa balance publicado. Latencias/fallos no medidos sólo pueden ser escenarios condicionados, no «q real» |
| Schedules de ejecución comparables / scaling completo | No bloquean structural null explícito con exposición conservadora; sí bloquean proclamar economics neta real o implementar scaling no capturado |
| Integración TPT automatizada | Excluida por `ECONOMICS_ONLY`; no bloquea research matemático. Una variante manual o custom necesita gate propio y permiso vendor explícito donde no esté documentado |

R1–R6 del review anterior: R1 resuelto por freeze; R2 clasificado ECONOMICS_ONLY; R3 contratos y policies propuestos con B4 abierto; R4 snapshots definidos; R5 diseño entregado, revisión matemática pendiente; R6 structural null zero execution cost propuesto explícitamente. Ningún resultado económico ni ranking de policies fue calculado. Permanece el estado del gate de captura D5.2 hasta aceptación owner; este trabajo no lo acepta por sustitución.

**Handoff autorizado ahora:** revisar matemáticamente esta sección y resolver los inputs/fuentes materiales listados. **No iniciar Functional/Technical SPEC, código ni experimentos en este mandato.** `D5_SESSION_MODEL_PASS = REVIEW`. `Next action = MATH_REVIEW`. Agents-OS actualizado: **sí, continuidad y change_log dentro del planner único; core/journal externo/tarea puente intactos por alcance expreso**.


## Manager Decision — D5.3 ready for GOD math review — 2026-09-24

**Verdict:** READY_FOR_GOD_MATH_REVIEW. No implementation authorized.

### Manager assessment

- The selected 1D finite-horizon killed-Brownian kernel is the correct class of model to preserve first-event/survival semantics at EOD; counters layered on D4 would be invalid.
- The technically dangerous surface is the TPT PRO process `(equity, running_max)` with intraday trailing floor and the diagonal/max boundary condition. This must be independently validated before any SPEC freeze.
- D5 introduces a new sensitivity input absent from D4: session variance `ν`. Under finite horizons, q and day-count outcomes depend on `ν`; D4 cannot identify it. D5 results must therefore be reported as `q_withdraw(ν, TradePolicy, WithdrawalPolicy, calendar, settlement)` until a calibration source is explicitly introduced.
- The proposed always-in-market/reopen-until-session-close policy is a **scenario trading policy**, not a prop rule. It may be used for structural null experiments only if frozen and labeled as such.
- TPT remains `ECONOMICS_ONLY` for the automated Echo target; this does not block mathematical comparison but forbids interpreting TPT as an integration candidate.
- `AllowedRequests` TPT and vendor settlement details do not block the kernel review; they do block final rules completeness / cash-EV certification for TPT.
- No code, Functional SPEC or Technical SPEC is authorized before math review.

### GOD review must decide

1. correctness/normalization of the finite-horizon 1D killed Brownian kernel and boundary flux formulas;
2. whether the proposed event-time + surviving-endpoint sampling contract is sufficient and unbiased;
3. correctness of the `(e,m)` running-maximum formulation for TPT PRO, including the diagonal boundary condition and lock transition;
4. validity of analytical test S10 and other claimed invariants;
5. optional-stopping/martingale claims under finite sessions + adaptive bounded adds + forced EOD liquidation;
6. whether the proposed independent numerical oracle can falsify the production sampler with a defensible error budget;
7. whether the model is implementable with bounded complexity or should be simplified before SPEC freeze.

### Gate

`D5_SESSION_MODEL_PASS` remains **REVIEW**.
Next action: **GOD_MATH_REVIEW**.

## GOD Mathematical Review — D5.3

### Baseline, alcance y decisión — 2026-09-24

**Verdict: MATH_REVISE. Recommended next action: CORRECT_AND_REVIEW. `D5_SESSION_MODEL_PASS = REVIEW`.** La clase de modelo es viable. El kernel 1D, la condición diagonal del máximo y la composición analítica de S10 son correctos bajo las condiciones precisadas abajo. No hay contradicción material que reabra D4. Sí hay correcciones obligatorias en el contrato del oráculo multisesión, el presupuesto de error global, las cotas con censura y la definición del indicador de activación. No congelar SPEC hasta incorporar y revisar estas correcciones.

Autoridades leídas: [[Echo Futures]], este planner —especialmente §D5.3 y §Manager Decision—, [[Echo Futures — Simulator v0]], ambas SPECs D4 y [[echo-futures-astra-math-review]]. Baseline D4 `d4f42a41946f12231b75e4eb65b90d132731be0d` comprobado por `git rev-parse HEAD` en su checkout, sin cambios locales. Baseline documental del planner antes de esta revisión: commit `0ddb83ce`. Esta sección es la disposición vigente de la revisión; los bloques anteriores se conservan como propuesta e historia, no como aceptación posterior.

Método: derivaciones independientes de flujo, Itô, problemas backward y cambio de tiempo; contraejemplos deterministas y pequeñas evaluaciones numéricas de fórmulas, sin implementar ni ejecutar un simulador. La única consulta externa fue la referencia matemática primaria ya citada para S10; no se investigaron firmas, precios ni marketing. Ningún resultado de implementación, convergencia PDE o Monte Carlo nuevo se declara certificado.

### Blocking findings

No se encontró un BLOCKER de inviabilidad de la difusión elegida. **G53-01 a G53-04 son MAJOR y bloquean SPEC freeze** porque todavía permiten contratos de validación o identidades falsas. No son defectos que autoricen sustituir el modelo por retornos diarios. Las condiciones técnicas de G53-06 y los teoremas de las secciones siguientes deben quedar explícitos en el handoff.

### Major findings

**G53-01 — Dimensión real del oráculo de consistencia. Severity: MAJOR.**

- **Claim audited:** §E propone PDE/cadena 1D para EOD o 2D `(e,m)` para PRO, con backward induction sobre «estados diarios discretos», para comparar ciclos de 2–7 sesiones con consistencia/retiros.
- **Expected mathematics:** 1D/2D describe la difusión local entre acciones, condicionada a los demás estados. El valor económico multisesión depende también de variables continuas de historia, además de los contadores discretos.
- **Problem found:** el contrato no especifica la representación ni el error del best day A, máximo EOD H, balance inicial diario y estado de trade/policy. No son todos discretos. Contraejemplo: días `[1700,700,600]` y `[1400,900,700]` producen igual P=3000, N=3, H_EOD=3000 y F=0, pero A=1700 frente a 1400. El primero falla ambas consistencias; el segundo las satisface. Sus vecindades contienen el mismo desacuerdo, no es sólo una igualdad de probabilidad cero.
- **Corrected formulation:** declarar por separado el semigrupo local condicionado y el estado suficiente de la recursión de valor. Conservar/integrar las variables continuas de historia, mediante cuadratura, mallas adicionales o condicionamiento que mantenga su ley conjunta; refinar también esas dimensiones. No sumar P como estado independiente de e cuando son idénticos en el snapshot, pero tampoco omitir A. Un oráculo 1D/2D sin esa extensión sólo certifica fixtures locales o sin consistencia.
- **Impact on D5:** evitar que dos motores compartan una reducción de estado incorrecta y coincidan en un q sesgado; reconocer la complejidad adicional sin exigir una PDE monolítica de todas las dimensiones.
- **Blocks SPEC freeze:** sí; cerrar el alcance de validación y la representación matemática de la historia antes del freeze. No se exige implementarla en esta revisión.

**G53-02 — Error numérico local, global y de cash no son intercambiables. Severity: MAJOR.**

- **Claim audited:** §E propone `ε_num≤10⁻⁴` para probabilidades y `≤$0.01` para medias cash, comparando sampler y oráculo mediante tolerancia MC adicional.
- **Expected mathematics:** cada tolerancia debe identificar observable, horizonte, norma, acumulación por composición y fuentes de error separadas; un presupuesto por probabilidad no determina el error de una expectativa monetaria.
- **Problem found:** no se fija si 10⁻⁴ corresponde a una llamada, una sesión o al resultado completo. Con reaperturas ilimitadas no hay un número determinista fijo de llamadas. Tampoco 10⁻⁴ implica un centavo: aun disponiendo de una cota de distancia de variación total de 10⁻⁴, un payoff de rango $2,000 admite error de $0.20. Controlar sólo una probabilidad escalar es todavía más débil. Renovaciones sin horizonte acotado dan costes no acotados.
- **Corrected formulation:** fijar presupuestos globales por fixture/observable y separar `ε_prod`, `ε_oracle`, `ε_trunc`, `ε_history`, `ε_tail` y error estadístico. Con K llamadas y cotas uniformes δ_i de variación total, el error de ley se acota por `Σ_i δ_i`; con número aleatorio, justificar una cota esperada equivalente o truncar K y conservar explícitamente su masa residual. Para payoff g en `[g_min,g_max]`, `|E_P g−E_Q g|≤(g_max−g_min)·TV(P,Q)`; para costes no acotados se necesita además una cota de momento/cola monetaria. Alternativamente, controlar directamente el error débil del observable de cash.
- **Impact on D5:** un kernel preciso o una coincidencia MC no certifican automáticamente q ni el centavo prometido. Mantener las metas para fixtures acotadas es razonable; prometerlas para toda economía infinita sin una cota adicional no lo es.
- **Blocks SPEC freeze:** sí; adoptar el contrato de aceptación desglosado de §Numerical oracle verdict. El trabajo numérico posterior deberá demostrarlo.

**G53-03 — S18 confunde censura de la muestra con incertidumbre sobre q. Severity: MAJOR.**

- **Claim audited:** para N intentos simulados, S recibidos y U sin resolver, `q∈[S/N,(S+U)/N]`.
- **Expected mathematics:** ese intervalo encierra la proporción final de esa muestra, no necesariamente el parámetro poblacional q. La incertidumbre de Monte Carlo permanece cuando U=0.
- **Problem found:** con N=1, S=1, U=0 se publicaría `q=1`, aunque un modelo con q=1/2 produce exactamente esa observación con probabilidad 1/2. Es una falsificación directa de la afirmación literal.
- **Corrected formulation:** escribir `q_hat_completed∈[S/N,(S+U)/N]`. Para N fijo de attempts IID, un intervalo conservador de confianza `1−α` para q es `[max(0,S/N−η), min(1,(S+U)/N+η)]`, `η=sqrt(log(2/α)/(2N))`; también sirve la envolvente de límites binomiales exactos para todos los conteos finales entre S y S+U. Añadir incertidumbre numérica por separado. Si S y U son masas exactas de un solver, entonces sí `q∈[p_received,p_received+p_unresolved]` es una cota poblacional determinista. Tamaño muestral elegido adaptativamente exige una confidence sequence o diseño equivalente, no reutilizar sin más el intervalo de N fijo.
- **Impact on D5:** no sobrecertificar q, `1/q` ni probabilidades de no retiro. No se asume censura independiente para la envolvente pathwise; sí se requiere el muestreo declarado para su capa estadística.
- **Blocks SPEC freeze:** sí; reemplazar S18 y el contrato de reporting correspondiente.

**G53-04 — Activación ocurrida ≠ fee positivo pagado. Severity: MAJOR.**

- **Claim audited:** §B3 define I como «activación pagada» y exige `J≤I`; §C/S14 usa I en la identidad promo/lista.
- **Expected mathematics:** todo retiro implica una activación/funding anterior, aunque la tarifa de activación sea cero. El indicador de lifecycle debe ser independiente del precio.
- **Problem found:** en `TPT_NOFEE40_SNAPSHOT`, fee de activación=0. Si «pagada» significa desembolso positivo, un retiro produce J=1 e I=0; `J≤I` es falso y `ΔK=68(1+n)+130I` pierde el ahorro de activación. Si se pretendía «activación ocurrida», la definición escrita debe corregirse.
- **Corrected formulation:** `I_act=1{activación completada}`, `J≤I_act`; `C_path=F_initial+ΣF_renewal+I_act·a_snapshot+C_other`. El cash pagado por activación es `I_act·a_snapshot`, no el indicador. Para mismos paths sin restricciones de presupuesto: `K_NOFEE40−K_LIST=68(1+n)+130 I_act`. Usar otro símbolo para la tarifa evita colisión con A=best day.
- **Impact on D5:** conservar separación nominal/cash y comparaciones de pricing; ninguna modificación a D4 ni al modelo de difusión.
- **Blocks SPEC freeze:** sí; corregir definición y fixtures S12/S14. Es una corrección contractual, no investigación de pricing.

### Minor / informational findings

**G53-05 — Los empates no son universalmente de probabilidad cero. Severity: MINOR.** **Claim audited:** §A5 dice que «un empate exacto tiene probabilidad cero en el modelo regular». **Expected mathematics:** el tiempo de hitting de una barrera separada de un punto inicial interior no tiene átomo en un deadline determinista positivo; barreras coincidentes sí se alcanzan juntas con probabilidad positiva. **Problem found:** una barrera de SL puede coincidir exactamente con el floor; TP con lock también. La frase es demasiado amplia, aunque la prioridad ya propuesta es correcta. **Corrected formulation:** limitar el argumento de probabilidad cero al empate tiempo aleatorio/deadline bajo no degeneración; definir todos los empates geométricos y los estados iniciales sobre frontera mediante operadores deterministas. **Impact on D5:** conservar phase-loss > close > add; en hard close no add ni reapertura; lock se actualiza aunque coincida con TP. **Blocks SPEC freeze:** no por sí solo; incorporar la precisión sin relajar prioridades.

**G53-06 — Máximo correcto, pero ley conjunta potencialmente mixta. Severity: INFO.** **Claim audited:** §A4 usa `(e,m)`, `L=(h²/2)∂ee` y `∂m u=0` en diagonal. **Expected mathematics:** son correctos para h constante entre eventos y estado de policy condicionado; el kernel es una medida, no necesariamente una densidad 2D ordinaria. **Problem found:** ninguno en esas fórmulas. Hay una trampa de implementación: partiendo de e<m, sobrevivir sin volver a m tiene probabilidad positiva y deja masa en `m_final=m_initial`. Con h=0 aparece además una masa puntual de identidad. **Corrected formulation:** preservar explícitamente esas componentes, fronteras de evento y transición al lock; no normalizar sólo una densidad respecto de `de dm`. **Impact on D5:** requisito del sampler/oráculo, detallado abajo. **Blocks SPEC freeze:** no es una refutación del modelo; el contrato de realización debe incluirlo.

**G53-07 — S10 es exacto con dos tiempos de muerte diferentes. Severity: INFO.** **Claim audited:** cola exponencial del máximo y `e⁻¹D/T` tras lock. **Expected mathematics:** la exponencial para todo m pertenece al drawdown sin cap; el proceso con floor bloqueado cambia esa cola después de D. **Problem found:** la composición propuesta para T≥D es correcta; no debe convertir la primera expresión en un test del proceso capped para m>D. **Corrected formulation:** usar `τ_D` para drawdown sin lock y `ζ` para muerte con lock; fórmulas y extensión a T<D abajo. **Impact on D5:** conservar S10 como control independiente, con nombres y condiciones explícitos. **Blocks SPEC freeze:** no por sí solo.

**G53-08 — Martingala nominal local, no identidad de lifecycle con resets/retiros. Severity: INFO.** **Claim audited:** media nominal cero con adds, sesiones y flatten. **Expected mathematics:** verdadera para la integral de trading detenida; evaluar condicionalmente desde el inicio de cada fase o llevar ganancias acumuladas sin borrar historia. **Problem found:** ninguno para el proceso declarado; sería falso aplicarlo al saldo que se reinicia al activar o se debita al retirar, o al subconjunto de sobrevivientes. **Corrected formulation:** exposición predecible, acotada y sin anticipación; transferencias/reset separados de `∫H dS`; condiciones de stopping explicadas abajo. **Impact on D5:** sizing puede cambiar q sin crear drift. **Blocks SPEC freeze:** no.

**G53-09 — Consistencia determinista válida; igualdad exige contrato explícito. Severity: INFO.** **Claim audited:** Topstep `P≥3000,N≥2,A≤.55P`; TPT `P≥3000,N≥3,A<.50P`. **Expected mathematics:** predicados válidos sobre snapshot cerrado. **Problem found:** ninguno en los predicados. Brownian continuo no garantiza que toda variable derivada carezca de átomos: killing, stopping por policy, redondeo de requests y días sin exposición pueden crearlos. **Corrected formulation:** conservar exactamente `<` frente a `≤`; no usar probabilidad cero ni epsilon favorable para borrar la diferencia. **Impact on D5:** S06–S08 siguen obligatorios, incluida igualdad exacta. **Blocks SPEC freeze:** no.

**G53-10 — ν es familia de relojes, no calibración implícita. Severity: MINOR.** **Claim audited:** `q_withdraw(ν,TradePolicy,WithdrawalPolicy,calendar,settlement)`. **Expected mathematics:** depende de la varianza por ventana y su correspondencia con decisiones de calendario; un único escalar basta sólo bajo una forma temporal y asignación entre ventanas ya congeladas. **Problem found:** la notación abreviada puede ocultar grados de libertad que §A3 sí admite al definir σ piecewise constant. **Corrected formulation:** interpretar ν como vector/perfil de varianzas de ventanas, o como multiplicador de un perfil determinista versionado. **Impact on D5:** sensibilidad reproducible sin inventar volatilidad; matriz mínima abajo. **Blocks SPEC freeze:** no como fórmula abreviada; sí deben declararse los inputs de cualquier experimento concreto.

### 1D kernel verdict

**Aceptado.** Sea `ℓ=b−a`, `r=(x−a)/ℓ`, `λ_n=n²π²/(2ℓ²)`. En reloj de varianza de PRECIO, el generador es `½∂yy` y:

`k_V(x,y)=(2/ℓ) Σ_{n≥1} sin(nπr) sin[nπ(y−a)/ℓ] exp(−λ_n V)`.

Es una densidad subprobabilidad, no una densidad ya normalizada a 1. La ortogonalidad de los senos produce la identidad inicial en sentido débil. Para V>0 la serie resuelve la ecuación de calor con Dirichlet en a,b. Su masa es:

`Q_x(V)=∫_a^b k_V(x,y)dy=(2/π) Σ_{n≥1} [(1−(−1)^n)/n] sin(nπr) exp(−λ_n V)`.

Los flujos propuestos tienen signos y factores correctos. En forma explícita, por unidad de varianza:

`f_a(v|x)=+(1/2)∂_y k_v(x,a+)=(π/ℓ²) Σ_{n≥1} n sin(nπr) exp(−λ_n v)`.

`f_b(v|x)=−(1/2)∂_y k_v(x,b−)=(π/ℓ²) Σ_{n≥1} (−1)^(n+1) n sin(nπr) exp(−λ_n v)`.

Aunque los sumandos cambien de signo, las funciones completas son no negativas. `Q'_x(v)=−f_a(v|x)−f_b(v|x)`; por tanto `Q_x(V)+∫_0^V(f_a+f_b)dv=1`. La normalización incluye ambas masas de salida, no sólo el endpoint.

Las probabilidades acumuladas, útiles para evitar integrar una serie mal condicionada en v=0, son:

`U_x(V)=P(τ≤V,exit=b)=r−(2/π)Σ_{n≥1}[(−1)^(n+1)/n]sin(nπr)exp(−λ_n V)`.

`L_x(V)=P(τ≤V,exit=a)=1−r−(2/π)Σ_{n≥1}[1/n]sin(nπr)exp(−λ_n V)`.

Así `U_x(∞)=r` y `L_x(∞)=1−r`, recuperando D4. La integración término a término hasta v=0 requiere límite/regularización; no justificarla por convergencia absoluta allí. El tiempo medio de salida es `(x−a)(b−x)` en varianza de precio. En coordenadas de EQUITY con `de=h dW_v`, usar `h²V` en el kernel unitario o coeficiente `h²/2`; en calendario, el flujo se multiplica por `σ²(t)`. No multiplicar dos veces por h² ni confundir varianza de precio con varianza de equity.

**Ley conjunta suficiente:** es una mezcla disjunta de `f_a(v)dv δ_a`, `f_b(v)dv δ_b`, para `0<v≤V`, y `k_V(x,y)dy` con etiqueta `τ>V`. No existe un endpoint superviviente que haya que muestrear también en la rama de salida. Muestrear primero esas tres masas y luego tiempo condicionado al lado, o primero tiempo condicionado a salida y lado según `f_b(v)/(f_a(v)+f_b(v))`, da la ley correcta. En la rama superviviente usar `k_V/Q_x(V)`. No usar r para elegir el lado independientemente de la duración finita.

**Límites:** V↓0 desde x interior da Q→1 y `k_V dy⇒δ_x`; las masas de salida tienden a 0. V→∞ da Q→0 y salida eventual cierta con masas r,1−r; el endpoint condicionado a supervivencia rara converge a `(π/(2ℓ))sin[π(y−a)/ℓ]dy`. Para V>0 fijo y x↓a, salida lower→1, tiempo→0, Q→0; x↑b es simétrico. Exactamente en una frontera, absorber a tiempo 0 antes de llamar al kernel interior. Los límites conjuntos x→frontera y V→0 no son uniformes: no sustituirlos por una tolerancia de empate.

**Evidencia aritmética independiente, no certificación de sampler:** a=0,b=1,x=.25,V=.1 da Q=.553175891850086, L=.429195269138053 y U=.0176288390118612; suman 1 a precisión de máquina. La masa upper eventual es .25, muy distinta de su masa antes de V. Con V=1, Q=.0064749699291492, L=.746762514183855, U=.246762515886996. Evaluaciones de las series con 1,000 términos; no prueban estabilidad uniforme para V pequeño o puntos casi absorbidos. La realización deberá cambiar de representación, por ejemplo imágenes para tiempos cortos y espectral para largos, con cotas de truncación y sin clipping silencioso.

### Session composition / event semantics verdict

**Aceptado con estado aumentado.** Brownian tiene strong Markov en los tiempos de hitting. En cada tramo se congela h y el estado que determina barreras; al ocurrir un evento se aplica la acción no anticipativa, se consume su τ de varianza y se vuelve a condicionar desde el estado alcanzado. El calendario, fase, trade/add index, floor, historial diario y policy tienen que formar parte del estado de control. `(e,m)` solo no vuelve Markov a cualquier estrategia adaptada con memoria omitida.

Los resets de precio relativo `s←0` al reabrir son cambios de coordenadas; no resetean equity de fase, máximo, reloj ni historial de días. Al hard close, una supervivencia se liquida en su endpoint condicionado. En una frontera meramente observacional se aplica Chapman–Kolmogorov; al liquidar y reiniciar trade/adds se compone semigrupo con un operador económico, y no se exige la misma igualdad que sin esa acción.

La política de referencia de G,L positivos fijos, h acotado, lista finita de adds y cortes exógenos localmente finitos no explota en una sesión: cada trade completo mueve la equity continua desde su apertura por G o −L. La continuidad uniforme en un horizonte compacto impide infinitos movimientos consecutivos de tamaño al menos `min(G,L)>0`; hay sólo finitos adds por cada trade. Una futura política con targets decrecientes a cero no hereda esta prueba y necesita una condición de no explosión propia. Un guard informático no puede etiquetar el resto como burn.

En EOD, breach frente al floor vigente se resuelve antes de flatten/snapshot. El ratchet `F_new=max(F_old,min(0,B_close−D))` no crea PnL. Para un sobreviviente con D>0 tampoco lo quema por sí solo: si el candidato nuevo es B_close−D está debajo del saldo; si llega a 0, B_close≥D; si no sube, el sobreviviente ya estaba sobre F_old. La revalidación sigue siendo útil como invariante y para transferencias separadas. PRO no recibe un segundo ratchet EOD.

### TPT PRO running-max verdict

**Aceptado; no corregir la diagonal a reflexión normal.** Antes de lock, `Ω={(e,m):0≤m<D, m−D<e≤m}`. Con coeficiente h fijo entre eventos:

`dE_v=h dW_v`, `M_v=max(m,sup_{s≤v}E_s)`, `dM_v≥0`, `1{E_v<M_v}dM_v=0`.

El par es strong Markov para el segmento condicionado. Para u suave, Itô da `du=h u_e dW_v+(h²/2)u_ee dv+u_m dM_v`. Puesto que dM vive en E=M, el dominio backward tiene `u_m(m,m)=0`. **No** es `u_e=0`, ni `u_e+u_m=0`, ni una condición de flujo forward que pueda copiarse sin derivación. Para valor terminal g y tiempo restante v, la ecuación interior es `∂_v u=(h²/2)u_ee`, con dato inicial g, dato absorbente/cemetery en `e=m−D` y datos de evento/continuación donde corresponda. En formulación por tiempo calendario hacia delante del contrato, es `∂_t u+(h²σ²(t)/2)u_ee=0`.

Control de coordenadas: para gap `d=m−e` y `w(d,m)=u(m−d,m)`, la condición es `w_d(0,m)+w_m(0,m)=0`; imponer `w_d=0` salvo que w sea independiente de m cambiaría el proceso. Esta identidad es útil para auditar una formulación alternativa del oráculo.

Al llegar por primera vez a m=D, la continuidad exige E=D. Desde `(D,D)` el floor queda en 0. El valor se empalma con la solución locked 1D; para límites desde estados `(e,m)` con m↑D y e<D, la traza compatible es el valor locked iniciado en e. No se absorbe el path como éxito salvo que un target analítico independiente lo mande. El máximo puede descartarse para reglas de primera extracción sólo si ninguna policy retenida lo consulta; floor/locked y demás historia relevante permanecen.

Adds y close/reopen conservan E, por tanto M. Cambiar h cambia la velocidad de varianza futura, no el máximo ya recorrido. Un reset de fase sí inicializa una cuenta/fase nueva según contrato; no confundirlo con cerrar un trade. En flat, E y M quedan constantes. Retiros son saltos de débito separados y no reducen el floor histórico.

**Competencia de eventos:** detener en el primer hit del conjunto drawdown ∪ SL ∪ TP ∪ add ∪ lock, o integrar lock como transición interna equivalente. Evaluar el máximo hasta ese instante, no el máximo hipotético posterior de toda la sesión. El floor móvil puede interceptar un descenso antes del add que era elegible al inicio; no basta calcular un floor estático al abrir el segmento. En un empate de pérdida con SL/add, domina pérdida. En TP=lock, conservar lock además de cerrar; en el deadline no reabrir. Las condiciones de boundary rewards se ponen sólo en las fronteras alcanzables antes de otras absorciones.

**Realización viable sin tiny Euler:** resolver/invertir el semigrupo o resolvente con esas fronteras y sus medidas de salida, o usar una construcción de excursiones/bridges con control del primer cruce. El dominio pre-lock está acotado (`−D<e<D`, `0≤m<D`), aunque la PDE es degenerada. Eso hace viable el problema local; no prueba un coste uniforme para todos los ν, policies o todos los estados diarios. Una malla PDE determinista puede aproximar la ley continua sin pasos Euler de paths, siempre declarando su error.

**Componente singular que debe preservarse:** si e0<m0, los paths que no vuelven a m0 mantienen M=m0. Sin otras barreras intermedias, la masa superviviente en esa línea a tiempo V es `k^{(m0−D,m0)}_{h²V}(e0,y)dy δ_{m0}(dm)`. Se añade la componente que sí actualizó el máximo y las medidas de salida. Ignorar la línea elimina probabilidad real. Desde e0=m0 y h≠0, en tiempo positivo el máximo aumenta inmediatamente casi seguramente; ello no permite ignorar la línea después de un add o una caída que deja e<m. Para h=0 el operador es identidad mientras no haya un evento determinista.

### S10 analytical oracle verdict

**Aceptado como igualdad exacta, no aproximación.** Definir por separado `τ_D=inf{v:M_v−E_v=D}` para Brownian sin cap y `ζ=inf{v:E_v≤min(0,M_v−D)}` para el proceso con lock. Sin otros stops ni horizonte finito, empezando E=M=0:

`P(M_{τ_D}≥z)=exp(−z/D)`, z≥0.

La cola del máximo al primer drawdown en Brownian sin drift está corroborada por [Landriault, Li y Zhang, §2, ecuaciones (2.6)–(2.7)](https://arxiv.org/html/1403.1183v1#S2). La siguiente derivación y el empalme capped se verifican aquí de forma independiente.

Para alcanzar un nivel c antes de drawdown, desde `m−D<e≤m<c`, la solución armónica es `u_c(e,m)=((e−m+D)/D) exp(−(c−m)/D)`. Es lineal en e, vale 0 en el floor, 1 en `(c,c)`, y cumple `u_m(m,m)=0`. En `(0,0)` da `exp(−c/D)`. Para c=D coincide con el proceso capped hasta lock, de modo que `P(lock before burn)=e⁻¹`.

Para target intradía T≥D, la continuidad obliga a pasar primero por `(D,D)`. Strong Markov da la probabilidad condicional locked `P_D(hit T before 0)=D/T`. Por tanto:

`P_0(hit T before ζ)=e⁻¹ D/T`, T≥D.

El caso T=D incluye el factor 1. Para `0<T<D`, el target puede ganar antes del lock y la fórmula correcta es `exp(−T/D)`. Para el máximo del proceso capped al morir:

`P(M_ζ≥z)=exp(−z/D)` si `0≤z≤D`; `P(M_ζ≥z)=e⁻¹D/z` si `z≥D`.

No exigir la cola exponencial más allá de D al motor capped. Con D=2000,T=3000, la probabilidad analítica de este fixture es `.24525296078096157`; la probabilidad de lock es `.36787944117144233`. Ninguna es q_withdraw del ruleset EOD.

**Condiciones:** equity continua, drift y costes nominales cero, ningún reset del máximo, target observado continuamente, sin retiro/cancelación anticipada ni gates de día. El target T≥D no puede ocurrir antes del lock; un target EOD, cambiante o condicionado a consistencia sí invalida ese argumento. Con h constante no nulo el resultado no depende de h. Con exposición predecible variable, se conserva por cambio de tiempo de martingala continua si el reloj cuadrático tiene suficiente recorrido para alcanzar la absorción —por ejemplo, exposición total en varianza infinita en paths no terminados— y no hay interrupciones de policy que eliminen outcomes. Acotación superior sola no basta: exposición apagada para siempre puede dejar paths sin resolver. h=0, deadline finito y calendario con oportunidad finita no satisfacen el fixture. Pure equity hitting/drawdown sin relojes ni otras reglas conserva esa invariancia; no atribuir un efecto de sizing a cualquier regla de path indistintamente.

**Oracle adicional sensible al tiempo, derivado del mismo boundary-value problem:** para h constante, `κ=sqrt(2λ)/|h|`, T≥D y λ>0, en reloj v de varianza de precio:

`E_0[exp(−λτ_T);τ_T<ζ]=exp[−κD coth(κD)]·sinh(κD)/sinh(κT)`.

La parte pre-lock se obtiene con `u(e,m)=[sinh(κ(e−m+D))/sinh(κD)] exp[−κ coth(κD)(D−m)]`, que satisface `Lu=λu`, kill y diagonal; la parte locked es el resolvente de hitting en (0,T). Su límite λ↓0 recupera S10. Este control sí detecta algunas leyes de duración incorrectas que el mero pass rate no detectaría. No es una fórmula directa de probabilidad antes de una sesión: obtener esa CDF requeriría inversión adicional validada. Para D=h=1,T=1.5, los valores son `.21477390832873927` en λ=.125 y `.14846893086020618` en λ=.5; calculados por evaluación de la fórmula, sin paths.

### Martingale / optional-stopping verdict

**Aceptado a horizonte finito.** Escribir la riqueza nominal de trading como `X_t=X_0+∫_0^t H_s σ(s)dW_s`. Para `|H_s|≤hMax`, exposición predecible y `∫_0^Tσ²(s)ds<∞`, la integral es una martingala cuadrado-integrable. Para cualquier stopping time τ:

`E[X_{T∧τ}]=X_0`, `E[(X_{T∧τ}−X_0)²]=E[∫_0^{T∧τ}H_s²σ²(s)ds]≤hMax²ν_[0,T]`.

«Adaptado» solo no es el contrato completo del integrando. Las decisiones de add en hitting times continuos se ejecutan con información actual y el nuevo h actúa después del evento; una exposición simple `H=Σh_i·1_(τ_i,τ_{i+1}]`, con h_i medible en `F_{τ_i}`, cumple el contrato. No usar el endpoint futuro de una bridge para decidir el add pasado.

`b'=b−Δh s`, `h'=h+Δh` da algebraicamente `b'+h's=b+hs`. El flatten sin coste cambia holdings/cash interno de trading a igual mark y desde entonces H=0. No crea drift. Reapertura self-financing conserva esa propiedad, incluida exposición adaptativa y simetría short si se habilitase. Se puede alterar la distribución y el promedio condicionado a sobrevivir; eso no es drift de la población completa.

D4 conserva la invariancia de hitting con sólo dos valores terminales fijos y stopping válido. D5 ya tiene valores interiores al EOD, trailing, gates y transferencias, de modo que `P(win)=L/(G+L)` no se obtiene de media cero para todo experimento. El sizing puede cambiar varianza realizada por sesión, distribución diaria y q_withdraw sin producir edge en la integral nominal.

No extrapolar `E[X_{T∧τ}]=X_0` a T=∞ sólo porque τ sea finito casi seguramente. Hace falta UI, stopping acotado u otra condición suficiente. Contraejemplo pertinente: una vez lockeado, Brownian desde D y floor 0, sin target ni retiro, toca 0 a.s. pero `E[X_ζ]=0≠D`; el tiempo medio de hitting es infinito y no hay UI. La familia detenida a cada horizonte finito sí tiene media D. Fees personales, resets de fase y débitos de payout son operaciones distintas y no satisfacen por sí mismos esa identidad nominal.

### Consistency / day-state verdict

**Aceptados los predicados propuestos.** En evaluación sin transferencias, `P=Σd_j`, `A=max(0,d_1,…,d_N)` con días finalizados; N cuenta sólo sesiones con actividad. Topstep permite `[1650,1350]`; TPT rechaza `[1500,1000,500]` y admite `[1400,900,700]`. `P≥max(3000,2A)` es incorrecto para TPT: se requieren separadamente `P≥3000` y `P>2A`.

No hay patología de definición al reentrar sin costes: el número de trades completos es finito a.s. bajo la política fija y la ganancia del día es la suma del realizado más el flatten final. Cien trades de un día siguen contando como un día. No se puede obtener N≥3 subdividiendo artificialmente una ventana, ni definir una sesión por el número de cierres. N cuenta actividad, no rentabilidad.

Para una política fija no degenerada y observaciones a tiempos deterministas, las distribuciones vivas de profit suelen tener densidad, lo que puede hacer nula la masa en la igualdad relevante. Ese argumento no es una licencia universal: stopping diario en un profit exacto crea un átomo, flat crea ganancia 0, los burns crean masas de frontera y las fixtures fuerzan igualdades. El contrato debe resolverlas aun cuando sean nulas en una subfamilia. No redondear equity/consistencia a centavos; el redondeo explícito de requests pertenece a otra operación.

### ν / scaling verdict

**Aceptada la familia de escenarios; rechazado un q null universal.** Dependen materialmente del reloj: exits por sesión, supervivencia/kill antes de cada close, adds ejecutados, PnL y best day, hitting del máximo/lock, winning days, p_pass, q_withdraw, duración, renovaciones y distribución de cash. El costo de compra fijo o una identidad aritmética de ledger no dependen por sí mismos de ν; el número de veces que se cobra sí puede depender.

Sea D una escala de equity y h_ref una exposición de referencia legal. Usar `ẽ=e/D`, `m̃=m/D`, `ṽ=h_ref²v/D²`, `h̃=h/h_ref`. Por ventana i, `ρ_i=h_ref²ν_i/D²` es adimensional. Permanecen ratios `G/D`, `L/D`, distancias de add `h_ref Δs/D`, profit target/D, winning-day threshold/D, buffer/D, caps/D y ratios de size. Por sí sola, `ν/D²` sería dimensionalmente incorrecta si ν está en unidades de precio² y h no se ha normalizado.

Escalar todos los niveles monetarios nominales por c y las distancias de precio por c con h fijo exige escalar ν por c²; entonces se conserva la ley de estados normalizados en las mismas sesiones. Escalar h por c y ν por 1/c² con barreras monetarias fijas también conserva la ley equivalente si se reescalan los add levels en precio y se conserva la policy normalizada. Los límites de contratos, enteros de size, tick/centavo, fees y umbrales que no se escalen rompen la invariancia. Los fees personales fijos no alteran q si las policies no consultan presupuesto, pero sí alteran cash normalizado/EV; mantener barreras y ν equivalentes no convierte snapshots económicos diferentes en idénticos.

**Grid mínimo propuesto, puramente adimensional:** para cada policy/exposición frozen, `sqrt(ρ_full)∈{0.1,0.25,0.5,1,2,4}` —equivalentemente `ρ_full∈{.01,.0625,.25,1,4,16}`— con la misma forma temporal declarada. Comparar no-add y cada política de adds requerida, y WAIT/CLOSE donde corresponda. Añadir el control h=0 sólo como fixture matemática de no exposición, no como default válido del scenario. Refinar donde cambien q o las colas de días; seis puntos no certifican monotonicidad, y q no tiene por qué ser monótono en ν bajo consistencia/ratchet.

Para early close usar el ν de la ventana realmente operable, sin renormalizar. Con noticias o publication waits, mantener un vector de ventanas y sus varianzas: igual varianza total repartida distinto entre dos ventanas con flatten/reset intermedio puede cambiar resultados. Un σ(t) distinto dentro de una única ventana sin decisiones temporales internas da la misma ley de outcomes en varianza, pero cambia el mapa a timestamps de eventos; éste importa cuando compite con billing o settlement. El grid no inventa una volatilidad empírica ni una escala de mercado.

### Numerical oracle verdict

**Independencia potencial, no certificación ya conseguida.** Un finite-volume/CTMC implementado independientemente puede falsificar un sampler espectral/semigrupo. Si producción también usa la misma PDE, stencil, interpolación o crossing routine, llamarlo «otro solver» no garantiza independencia; necesitan otra representación y controles analíticos separados. Compartir las reglas escritas es necesario; compartir un operador de transición incorrecto como única evidencia deja un fallo común. Los fixtures deterministas de ledger/consistencia y S10 deben impedirlo.

El oráculo local PRO puede construirse con saltos simétricos de equity y actualización `m←max(m,e_new)`, killing al floor y lock correcto, sin reutilizar probabilities del production kernel. Su límite debe reproducir la condición backward demostrada. No modelar el máximo mediante un Brownian independiente ni reflexión normal de un proceso 2D ordinario. Su resolución de historia multisesión es la obligación G53-01.

**Contrato de convergencia obligatorio:**

1. Refinar espacio Δ,Δ/2,Δ/4; refinar independientemente paso temporal/cuadratura/inversión y las dimensiones continuas de historia. Mostrar estimaciones y diferencias; añadir nivel si no hay régimen estable. Richardson sólo con orden observado y justificado, no asumido en esquinas/discontinuidades.
2. Alinear floor, diagonal, lock, TP/SL/add y umbrales del fixture. Cuando no sea posible, desplazar ambas direcciones y medir sensibilidad. Las barreras de supervivencia anidadas dan cotas por inclusión; mover una frontera de policy/consistencia puede no ordenar q y no debe presentarse automáticamente como bracket riguroso.
3. Pre-lock tiene dominio acotado. Para el locked/EOD no acotado, aumentar el dominio truncado y llevar masa de escape como desconocida o acotarla. No convertir un borde artificial superior en retiro ni reflejarlo sin control. Repetir con dominio ampliado y separar cola monetaria de probabilidad de escape.
4. Verificar conservación/positividad, medidas de frontera y masa singular `M=m0`; identidad a tiempo 0; semigrupo sin acciones; first-event ordering; empalme locked. Una renormalización o clipping de probabilidad no sustituye una cota.
5. Comparar distribución conjunta: sub-CDF `P(τ≤v,side=a/b)`, supervivencia/endpoint, ley de M y dependencia con E, además de q final. El mean-zero no detecta todos los errores de killing.
6. Llevar un presupuesto global de error de composición, historia, truncación y horizonte. Tres mallas estables son evidencia empírica; sin enclosure/error theorem no decir «cota rigurosa» ni «sampler exacto».

**Aceptación numérica:** conservar `ε_num_global≤10⁻⁴` en probabilidades de los fixtures locales/finito-horizonte expresamente definidos. Para cash de fixtures acotadas, `≤$0.01` es una meta separada: exigir control directo de la expectativa o distancia de ley compatible con su rango. Identidades de ledger y casos deterministas deben coincidir a la precisión aritmética del contrato, no consumir una tolerancia MC de un centavo. Una tolerancia exploratoria mayor para q completo, por ejemplo 10⁻³ absoluto, puede declararse antes de correr como screening; no satisface por sustitución el gate 10⁻⁴ ni autoriza un ranking cuya diferencia esté dentro de incertidumbre. El presupuesto de un resultado completo debe congelarse según su uso, no heredarse de un kernel.

Con referencia analítica p, usar test binomial exacto o intervalo con cobertura declarada; la regla 5σ es una aproximación aceptable cuando Np y N(1−p) son suficientemente grandes. Para p cercano a 0/1 no usar una banda degenerada de plug-in. Si el oráculo entrega `[p_o−ε_o,p_o+ε_o]`, exigir compatibilidad con el intervalo MC ampliado por el presupuesto del production sampler, manteniendo además las anchuras máximas predefinidas. Reportar por separado sesgo numérico y SE; elegir niveles/ajuste por múltiples fixtures antes de inspeccionar resultados. Para medias cash, usar SE sólo con varianza finita y un régimen estadístico defendible, o intervalos conservadores para payoffs acotados; no imponer normalidad de colas pesadas.

El 10⁻⁴ numérico NO exige SE Monte Carlo de 10⁻⁴. A modo de coste, `5 sqrt(.25/N)≤10⁻⁴` requeriría N≥625,000,000 en el peor p; MC de tamaño menor puede validar con su incertidumbre explícita, pero no demostrar por sí solo ausencia de sesgo 10⁻⁴. El presupuesto pequeño se sustenta en análisis/convergencia/control independiente, no en aceptar una banda 5σ ancha.

### Censoring / infinite attempt horizons verdict

**Aceptados pending/live separados de BURNED y el requisito IID; corregir G53-03.** Un receipt pendiente después de cerrar cuenta no es burn, ni success antes de cash. Si un settlement ideal asegura receipt eventual, puede contarse como éxito eventual lógicamente probado para un observable de horizonte infinito, pero sigue pendiente para cash recibido antes de un deadline. No mezclar esos dos observables.

Para usar geometric en ejecuciones secuenciales, cada attempt debe terminar/resolverse a.s., tener probabilidad de éxito común q>0, ser independiente de los anteriores y no depender de presupuesto/entitlements/calendario heredados. El lifecycle completo, incluidas renovaciones y settlement, forma parte del attempt. Un intento que permanece vivo para siempre puede impedir iniciar el siguiente: una sucesión hipotética de Bernoulli independientes no representa entonces la operación secuencial.

Si `N*=inf{i:J_i=1}` y los pares `(J_i,K_i)` son IID, donde `K_i=J_i c_i−C_i` incluye el intento exitoso, `E[N*]=1/q`, `P(N*>n)=(1−q)^n` y, si `E|K_i|<∞`, `E[Σ_{i=1}^{N*}K_i]=E[K_i]/q`. No hace falta independencia entre coste y éxito dentro del mismo attempt. La prueba usa que `{N*≥i}` depende sólo de attempts anteriores. Sin presupuesto suficiente para comprar indefinidamente o con purchase times dependientes de duración, no trasladar estas expresiones automáticamente al calendario real.

Para hazards de éxito variables, `P(no success through n)=∏_{i=1}^n(1−q_i^cond)`, donde `q_i^cond=P(J_i=1 | J_1=…=J_{i−1}=0)` corresponde al experimento de attempts realmente iniciables. No usar probabilidades marginales ni asumir que renovación/mes/promo preserve q. Cohortes simultáneas/copiadas requieren su dependencia conjunta.

Tiempo finito casi seguro no garantiza duración media, número medio de renovaciones ni cash medio finitos. Para cash acumulado hasta retiro se requieren integrabilidad absoluta de los costes/rewards y control de colas, además de eventual receipt y reinicio. Una pequeña masa pendiente no da un pequeño error monetario si puede seguir pagando renovaciones ilimitadas. `q_L=0` impide una cota superior finita de `1/q`; con `0<q_L≤q≤q_U`, el intervalo transformado es `[1/q_U,1/q_L]`. Para cuantiles cash con censura se necesitan bounds de CDF o masa residual suficiente; no reportar cuantiles sólo entre paths resueltos como si fueran incondicionales.

### Required corrections before SPEC

1. **G53-01:** separar dimensión de difusión local de historia multisesión; fijar estado suficiente y dimensiones/cuadraturas que el oráculo debe validar. Incluir el par de historiales con igual P,N,H,F y distinto A como negativo obligatorio.
2. **G53-02:** definir presupuestos globales de probabilidad y cash por fixture/observable; límites de composición y colas, cobertura MC, fuentes de incertidumbre separadas y qué evidencia será empírica frente a rigurosa. No exigir un sampler ya implementado para aprobar la matemática, pero sí un contrato verificable.
3. **G53-03:** reemplazar la cota literal de q en S18 por cota de completación muestral más intervalo estadístico; preservar la alternativa de masas exactas del solver.
4. **G53-04:** definir I_act por activación ocurrida independientemente de la tarifa; propagar a ledger, S12 y S14.
5. Incorporar G53-05/06: empates geométricos, componentes singulares del máximo, h=0, fronteras iniciales y endpoint condicionado. Conservar la diagonal `u_m=0`; cambiarla a Neumann normal sería un error.
6. Separar τ_D de ζ en S10; conservar condiciones de cambio de tiempo y añadir al menos un control de duración conjunta. Mantener el límite D4 sólo al desactivar efectivamente deadlines/flatten/gates pertinentes.

### Accepted analytical tests

- **S01–S03:** correctos con reloj/unidades explícitos, supervivencia más ambos flujos, y semigrupo sólo sin acción económica en el corte. Añadir sub-CDF por lado para detectar coupling incorrecto, puntos próximos a cada frontera y régimen V pequeño/grande.
- **S04–S09:** ratchets, lock, consistency, winning days y máximo continuo aceptados. Igualdades, estados iniciales de frontera y prioridades siguen siendo fixtures deterministas aunque una subfamilia tenga densidad.
- **S10:** aceptado para drawdown sin cap y composición capped tal como se distingue arriba; añadir T<D y T=D, y resolvente con λ>0. No es un oracle del q EOD completo.
- **S11:** aceptado para trading nominal de una fase o ganancias acumuladas sin resets, con exposición predecible acotada, horizonte fijo y todos los paths detenidos incluidos.
- **S12–S14:** identidades y cronología monetarias aceptadas después de corregir I_act; fixture adicional obligatoria: activación exenta, receipt positivo, `J=I_act=1`, fee de activación=0.
- **S15–S16:** cronología/determinismo y aislamiento delta aceptados. Calendario/tolerancias son inputs versionados, no una fuente de drift.
- **S17:** inclusión de éxitos WAIT dentro de CLOSE aceptada con mismo path hasta divergencia, decision schedule idéntico, fallback idéntico y settlement ideal que asegura cash positivo en cada cierre elegido. No implica dominancia de importe/EV ni sigue siendo universal con denegaciones dependientes de ruta.
- **S18:** separación de outcomes y geometric IID aceptados después de corregir el intervalo y exigir terminación/resolución de cada attempt.
- **Controles nuevos:** oráculo del máximo no actualizado, prueba de coordenadas de diagonal, invariancia de escala adimensional y negativo de estado A omitido. Son contratos analíticos para implementación futura, no tests ejecutados en esta revisión.

### Rejected/replaced analytical tests

- Rechazado `q∈[S/N,(S+U)/N]` como garantía poblacional de una muestra MC. Reemplazo: G53-03.
- Rechazado `J≤1{fee_activation>0}`. Reemplazo: `J≤I_act` incluso con waiver.
- Rechazada cualquier certificación de q con consistencia basada sólo en e o `(e,m)` y contadores enteros omitiendo historia continua. Reemplazo: semigrupos locales condicionados más recursión de estado suficiente.
- Rechazado inferir error global/cash del 10⁻⁴ de una llamada o de un pass rate; sustituir por presupuestos observables y control de composición/cola.
- Rechazados como ampliaciones indebidas, no como fórmulas realmente demostradas por el draft: cola exponencial capped para m>D; `e⁻¹D/T` a deadline EOD; invariancia general de q frente a sizing; martingala de saldos reiniciados o cash; igualdad de ley diaria inferida de mean-zero; normal incondicional en supervivencia; tiempos y lado independientes.

### Exact residual blockers / handoff

**Bloqueos matemáticos residuales de freeze:** incorporar G53-01 a G53-04 en el contrato propuesto y revisar su cierre; incluir las condiciones de realización y tests precisados. Esta revisión aporta las fórmulas corregidas, pero no marca la propuesta anterior como corregida/aceptada automáticamente. No se encontró necesidad de rediseñar la clase de proceso ni de reabrir D4.

**Inputs de escenario aún requeridos:** perfil/vector ν y grid, TradePolicy/WithdrawalPolicy, calendario de ventanas/publicación/billing/settlement y criterio de horizonte/tail. `AllowedRequests` TPT y mínimos/settlement siguen bloqueando certificación de reglas completas/cash real; no invalidan los kernels ni impiden estudiar un escenario hipotético etiquetado `RETAIN_BUFFER`/`IDEAL_COMPLIANT`. Integración TPT permanece `ECONOMICS_ONLY` y fuera de esta revisión.

**Owner gate:** no aceptado. **Gate:** `D5_SESSION_MODEL_PASS = REVIEW`. **Recommended next action:** `CORRECT_AND_REVIEW`. No Functional SPEC, Technical SPEC ni código autorizados o creados.

**Agents-OS actualizado: sí.** Change_log de esta revisión y continuidad quedan exclusivamente en esta sección del planner por mandato de alcance: dictamen, evidencia, correcciones y blockers persistidos; core, journal externo, tarea puente y baseline D4 intactos. **STOP.**
