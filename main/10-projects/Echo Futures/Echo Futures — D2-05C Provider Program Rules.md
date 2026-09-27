---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX]]"
aliases:
  - Echo Futures D2-05C
  - EF D2-05C Provider Program Rules
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-05C Provider / Program / RuleSet

> [!info]+ Workstream D2-05C
> Diseño técnico V1 del modelo `Provider / ProviderProgram / Phase / ProviderRuleSet`, su binding a la execution Account y su enforcement en runtime. Respeta sin reabrir D2-01 (snapshot + contract pinning), D2-02 (fan-out + single Operation), D2-03 (Signal + Strategy/MM boundary) y el artefacto cerrado [[Echo Futures — D2-04 Operation Order Fill Position]]. Responde el diseño de Q10 (Provider model) a nivel child. No implementa código productivo, no cierra D2-05 y no avanza a D2-06. Los drafts D2-05\* previos autoescritos fueron declarados inválidos por el mandato y NO se usaron como autoridad; este archivo los REEMPLAZA. Baseline físico verificada: `xKoRx/echo HEAD = 372af59a7b83604781346613da01e3d510ea1360` (worktree limpio en `~/aranea/work/d3-shot3-correction-20260924/echo`, verificación vía `git show 372af59a:<path>`).

## 1. Verdict

- `STATUS: D2-05C_READY_FOR_SUBMANAGER_REVIEW`. El modelo cierra Provider → ProviderProgram → fase → ProviderRuleSet versionado, el binding Account↔(Provider, Program, fase, transporte, DayBoundary) fuera de AccountStrategy, y un enforcement dividido exactamente donde el ciclo congelado de D2-04 lo permite: admisión pre-materialización (ALLOW / DENY_NEW_RISK, antes de crear Operation), gate por Order (cantidad/exposición, después de MM y antes del egreso físico) y plano safety asíncrono que actúa sobre Operations vivas mediante intents de terminación, nunca mediante terminalización instantánea (R3 de D2-04).
- Decisión central de dominio: **la autoridad de reglas es `ProviderRuleSet` versionado por `(provider, programa, fase)` y el Account la resuelve como autoridad corriente mediante un binding explícito**; Provider es business/policy owner y nunca un platform transport (ProjectX/NinjaTrader/Tradovate/Rithmic/CQG son capability de transporte, con entitlement separado y UNKNOWN jamás interpretado como permitido).
- Decisión central de enforcement: **la Operation se materializa sólo si la admisión del provider lo permite** (reconciliado con "Operation existe antes de MM/Orders" de D2-04: la admisión es un guard de materialización, igual que `valid_until` o el pin de contrato); **el gate de cantidad/exposición vive entre la decisión MM y el egreso transaccional de comandos** (una Order denegada nunca se emite al venue, sin tocar M1/M2); **las salidas (REDUCE/EXIT/CLOSE) jamás son bloqueadas por reglas de provider** (ninguna familia V1 exige impedir reducir riesgo).
- Decisión central de reglas: **familias tipadas compartidas + parámetros provider/program + excepciones provider-specific registradas**; sin DSL, sin generic if/then, sin normalizar nombres de negocio en enums artificiales. Sólo familias runtime-materiales entran al hot path; restricciones administrativas (payout, elegibilidad, consistencia, copy entre cuentas) quedan como configuración/eligibilidad u operativo del owner.
- Hot updates: el RuleSet vigente es dinámico y aplica prospectivamente en la próxima evaluación/decisión; jamás muta el `contract_id` pineado ni el snapshot MM de una Operation viva; la autoridad safety del provider sí actúa en vivo pero sólo vía intents (R3).
- Provenance: toda decisión material produce un `ProviderDecision` dur durable con `{programa, fase, rule_set_id/version, familia, reason, timestamps}`; la Operation sólo referencia por ID la decisión que la admitió; sin history engine genérico (patrón Kafka/OTel + facts de R14).
- `OWNER DECISIONS REQUIRED: NONE`. Quedan ratificaciones técnicas ordinarias para el manager (nombres de functions/topics/tablas, enum de razones, un campo additivo de provenance en Operation); ver §17.

## 2. Provider

- Definición: identidad canónica de la firma prop como **owner de negocio/policy**. Es la raíz de la jerarquía de autoridad de reglas; no ejecuta, no transporta, no posee cuentas físicas de Echo.
- Campos mínimos V1: `provider_id` (identidad canónica estable, slug de negocio, ej. `topstep`), `display_name`, `status` (`ACTIVE` | `ARCHIVED`; archived preserva historia sin permitir bindings nuevos), `created_at`/`updated_at`. Sin metadata ornamental (sitio web, logos, notas de marketing quedan fuera).
- Identidad: `provider_id` es la única identidad de negocio; nombres, marcas y renombres de firms (ej. TopstepTrader→Topstep) son datos display, nunca identidad (regla de continuidad: nombres/paths/timestamps son señales de routing, no identidad). No se crean aliases en V1 (YAGNI).
- Cardinalidad: `Provider 1 → 0..N ProviderProgram`. Un Provider soporta múltiples programas por diseño (Topstep Combine/Express/Live Funded son productos distintos del mismo provider).
- No es, explícitamente: ProjectX, NinjaTrader, Tradovate, Rithmic, CQG ni ninguna plataforma/transport. Esas familias pertenecen al concern de execution transport/capability (binding de cuenta + adapters D6); la coincidencia casual de que una firma sea dueña de una plataforma (TopstepX/ProjectX) no fusiona los dos concerns.
- No asume nomenclatura común entre firms: el modelo no exige que todas tengan "evaluation" o "funded"; esos conceptos existen sólo donde el RuleSet del programa los declara.
- Evidencia aceptada (corpus Front C corregido por manager en [[Echo Futures]] 2026-09-26): Topstep, Lucid, MFFU, TradeDay, FundedNext, Tradeify, Alpha Futures, TakeProfitTrader con automatización ALLOWED/CONDITIONAL/FORBIDDEN por programa y fase; esa matriz es el universo de diseño de V1, no la cohorte comercial (la cohorte es decisión posterior del owner).

## 3. ProviderProgram

- Definición: producto/programa real de la firma (ej. "Trading Combine", "Express Funded", "Core Challenge", "LucidDaily"). Es la unidad comercial a la que una cuenta pertenece y a la que el RuleSet se ancla.
- Campos mínimos V1: `program_id` (identidad canónica), `provider_id` (FK), `display_name` (nombre real del producto, texto libre), `status` (`ACTIVE` | `ARCHIVED`), timestamps. Nada más.
- Las diferencias de reglas entre programas NO viven en columnas del programa: viven en el RuleSet versionado ligado a `(provider, programa, fase)` (§5). El programa no normaliza nada; su función es ser el punto de anclaje estable de la autoridad de reglas y del binding de cuentas.
- Prohibido: enums artificiales de tipo de programa (`EVAL|FUNDED|...`) que no aporten enforcement. El corpus demuestra que las semánticas no son comparables entre firms (el "funded" de Topstep simulado tiene API prohibida; el "funded live" de TradeDay mantiene las mismas reglas de trading que su eval, cambiando sólo payout) — normalizar esos nombres destruiría información material. Si una familia de reglas necesita distinguir fases, lo declara su propia config tipada (§6), no un enum global.
- Antecedente legacy verificado: `echo.prop_rulesets` (V1/V2) ya intentó este modelo con `prop_firm text` + `phase_type text` como enums de texto (`CHALLENGE/VERIFICATION/FUNDED`) — es exactamente el anti-patrón que D2-05C corrige (§13, REUSE del concepto / REPLACE del shape).

## 4. Decisión de Phase

- Pregunta del mandato: ¿cambian materialmente las reglas operativas por fase? **Respuesta: sí, con evidencia first-party aceptada.** Topstep: automatización/API permitida en Combine/Express simulados y FORBIDDEN vía ProjectX API en Live Funded (cambio material de entitlement por fase). TradeDay: drawdown y mecánica de evaluación vs funded difieren por fase. Lucid: news trading prohibido en LucidDaily y permitido en Flex/Pro (cambio por plan/programa). Drawdown EOD vs intraday varía por programa/fase en el corpus. Por tanto la fase es material y debe ser parte de la autoridad de reglas.
- Decisión (KISS): **la fase NO es un aggregate ni una entidad global; es un atributo tipado del binding Account↔Programa y una dimensión del catálogo de RuleSets.** Concretamente: (1) cada `ProviderRuleSet` declara la tupla `(provider_id, program_id, phase)` que gobierna; (2) el binding de la cuenta declara `(provider_id, program_id, phase)` vigente; (3) la resolución de autoridad une ambas (§5/§7). Los valores válidos de `phase` por programa quedan declarados de facto por el catálogo de RuleSets (lo que existe en el catálogo es lo que se puede bindear); no hay tabla ni enum central de fases.
- Cardinalidad congelada: `Account 1 → 0..1 binding activo`; `binding N → 1 ProviderProgram`; `(programa, fase) 1 → 0..N versiones de RuleSet` con **a lo sumo una** versión efectiva a la vez; cero versiones efectivas ⇒ fail-closed (la cuenta sin autoridad de reglas no admite nuevo riesgo, §8).
- Transiciones de fase (eval → funded → breached): en V1 son **operación manual del owner** sobre el binding (config); Echo no integra APIs de status de firmas ni detecta la transición automáticamente (no hay evidencia de API de lifecycle de fase en el corpus aceptado; la política de research prohíbe inferirla). El cambio de fase publica el binding actualizado y dispara la reevaluación de admisión (§11, caso entitlement revocado).

## 5. ProviderRuleSet

- Definición: conjunto versionado y con provenance explícita de las reglas efectivas de un `(provider, programa, fase)`. Es la ÚNICA autoridad de enforcement de provider en runtime y la única entidad del modelo provider donde version/provenance es obligatoria (D2-01: sin framework universal de versionado para Strategy/MM/AccountStrategy).
- Campos: `rule_set_id` (identidad); `provider_id` + `program_id` + `phase` (alcance); `version` (entero monotónico por `rule_set_id`); `status` (`ACTIVE` | `SUPERSEDED`); `effective_at` (no-antes-de; la versión efectiva es la ACTIVE con mayor `effective_at ≤ now`); `source_refs` (provenance mínima obligatoria: lista de `{claim/referencia, url o fuente first-party, retrieved_at}` — sin esto la versión no puede activarse); `rules` (payload tipado de familias, §6); `reset_semantics` (anclaje de acumuladores diarios, §4 caso F); `updated_at`.
- Resolución de autoridad corriente: para un binding `(provider, programa, fase)` vigente, la autoridad es la versión `ACTIVE` efectiva con `version` máxima; el binding publica el par `(rule_set_id, rule_set_version)` resuelto y se recalcula en caliente cuando el catálogo cambia. **Si no existe versión efectiva, el estado de admisión es DENY_NEW_RISK con razón `NO_RULESET_AUTHORITY`** — fail-closed: un account sin reglas conocidas jamás opera (alignado con "UNKNOWN jamás se interpreta como permitido").
- Scope de enforcement (declaración honesta de límites): V1 sólo puede enforcear en runtime reglas **ACCOUNT-scoped** (lo observable dentro de una cuenta Echo). Los scopes TRADER/HOUSEHOLD/CROSS_ACCOUNT/CROSS_PROVIDER del corpus (copy prohibido, same-IP, group trading, uso exclusivo cross-firm) son **CONFIG/ELIGIBILITY ONLY**: se registran en el RuleSet como restricciones declaradas con provenance, condicionan la habilitación del binding por el owner, y producen superficie de advertencia; Echo no tiene observabilidad para enforcearlas y no finge lo contrario.
- Hot update: el catálogo viaja por topic Kafka compactado (patrón `echo.automation-profiles.v1` / `echo.account-configs.v1`): nueva versión activada ⇒ binding resuelve nueva autoridad ⇒ reevaluación de admisión y safety (§11).
- Valores de reglas: este artefacto congela familias y parámetros tipados, **no valores comerciales** (dólares, porcentajes, horarios por firma). Los valores se cargan como config onboarding por programa con su provenance; un programa sin valores verificados no puede activarse (fail-closed). FACT (automatización por programa/fase) vs valor numérico concreto (config onboarding) queda explícito.

## 6. Familias de reglas tipadas

Clasificación sobre el corpus aceptado (matriz corregida por manager + forensics V2 como apoyo). Cada familia es un struct de config tipado + un evaluador tipado registrado; **no existe evaluador genérico if/then ni DSL**. Las diferencias entre firms son valores de parámetros dentro de la familia tipada; lo que no calza en ninguna familia es una **excepción provider-specific**: un evaluador tipado nuevo, registrado explícitamente, que sólo se implementa cuando un programa concreto lo exige y vive identificado en el RuleSet (nunca lógica ad-hoc embebida en el runtime).

| Familia | Clasificación V1 | Superficie de enforcement | Params tipados (no valores) | Evidencia corpus |
|---|---|---|---|---|
| allowed new-risk window | V1 HOT-PATH ENFORCEABLE | Gate pre-materialización (DENY_NEW_RISK fuera de ventana) | ventanas por exchange/instrumento/global, timezone del provider clock (input de B), días habilitados | Topstep trading times; Lucid allowed trading times |
| forced-flat cutoff | V1 HOT-PATH ENFORCEABLE | Plano safety asíncrono → ForceClose intents (R3) | cutoff por programa, offsets por early-close/holiday (input B), flatten opcional por instrumento | Topstep 3:10 PM CT vs cierre CME 4:00 PM CT; Lucid 4:45 PM ET |
| permitted instruments | V1 HOT-PATH ENFORCEABLE | Gate pre-materialización (instrumento/contract no permitido ⇒ DENY_NEW_RISK); complementa (no reemplaza) la `TradingWhitelist` operacional de cuenta | allowlist de instrument_id/exchange/product_group; fail-closed ante instrumento desconocido | allowed instruments/exchanges en programas; resticciones de producto por fase |
| max contracts/order | V1 HOT-PATH ENFORCEABLE | Gate por Order (después de MM, antes del egreso) | cap por orden, por clase de instrumento (full/micro) | max contracts por programa (corpus general) |
| max exposure/instrument/account | V1 HOT-PATH ENFORCEABLE | Gate por Order (qty propuesta + exposición corriente agregada por cuenta/contrato) | caps por cuenta, por contract/instrument, por product group; margen de headroom | position/contract limits por programa (corpus general) |
| daily loss | V1 SAFETY INPUT | Estado de riesgo del provider → DENY_NEW_RISK al disparar + ForceClose opcional declarado por la regla | límite, tipo PERCENT/ABSOLUTE, basis (initial_balance / prev_day_close / daily HWM — bases ya tipadas en V3), acción (deny / deny+flatten) | daily loss en todas las firms; bases DAY_HIGH/PREV_CLOSE ya presentes en `prop_rulesets` legacy |
| trailing drawdown | V1 SAFETY INPUT | Igual que daily loss; el estado trailing es máquina de estado del account, no del order gate | variante tipada: EOD-trailing / intraday-trailing / static-lock; basis; lock | EOD vs intraday trailing en Topstep/TradeDay/Lucid |
| automation restrictions | CONFIG/ELIGIBILITY ONLY | Binding: entitlement de automatización por (programa, fase); UNKNOWN/FORBIDDEN ⇒ binding no habilitable / revocable en caliente | entitlement ALLOWED_CONDITIONAL/FORBIDDEN/UNKNOWN + condiciones tipadas (ownership exclusivo, no cross-firm, no-VPS) | Topstep sim ALLOWED/Live FORBIDDEN; TradeDay vía plataformas; Tradeify conditional; Alpha/TPT FORBIDDEN |
| copy/multi-account | CONFIG/ELIGIBILITY ONLY | Declaración en RuleSet + advertencia al configurar AccountStrategies; sin gate runtime | scope declarado (mismo-owner-only / prohibido / desconocido) | TradeDay no-duplicación; FundedNext copy sólo cuentas propias; Tradeify exclusividad |
| overnight/weekend | V1 HOT-PATH ENFORCEABLE | Plano safety con trigger programado por calendario (input B) + gate de nueva exposición en ventanas prohibidas | prohibido pernoctar / fin de semana; trigger = pre-cutoff programado | overnight/weekend_allowed ya tipados en `prop_rulesets` legacy; corpus de fases |
| news | V1 SAFETY INPUT | Ventana activa → DENY_NEW_RISK (pre-materialización) + acciones opcionales declaradas (block symbols / flatten) | ventanas before/after por impacto/evento; acción tipada | MFFU news policy; LucidDaily news restriction; `NEWS_BLACKOUT` RFC-007 ya existe en V3 |
| consistency | CONFIG/ELIGIBILITY ONLY (warn) | Cálculo warn-only sobre días cerrados; jamás bloquea una orden (no es prevenible por orden) | % máximo de contribución diaria | Alpha 40% consistency; variantes en corpus |
| payout/min days/inactivity/account-count | NOT ECHO-RUNTIME RESPONSIBILITY | Fuera del runtime; datos de RuleSet para contexto del owner | — | payout eligibility en todas las firms |
| HFT/microscalping/order-frequency | CONFIG/ELIGIBILITY ONLY (+ DEFER runtime) | Declaración + warn; un limitador runtime de frecuencia es YAGNI V1 salvo que la cohorte lo exija (DEFER explícito) | umbral de frecuencia si se activa el DEFER | HFT prohibido (Topstep, Alpha, MFFU, FundedNext); min-hold en corpus |
| hedging/correlated | CONFIG/ELIGIBILITY ONLY | Validador de configuración: cuenta con restricción no-declarada para estrategias opuestas ⇒ advertencia; Echo no auto-corrige configuración (regla del proyecto) | hedging_allowed bool + productos correlacionados | hedging prohibido (TradeDay, Alpha, MFFU); D2-04 caso 7 (dos estrategias opuestas netean físicamente) |

Principios transversales congelados: (1) **las salidas jamás se bloquean** — ninguna familia puede impedir REDUCE/EXIT/CLOSE; el gate sólo toca nueva exposición; (2) **sin liquidación inventada** — el runtime no fuerza reducción de exposición existente salvo que la regla tipada declare explícitamente flatten (ninguna familia del corpus aceptado lo exige por defecto); (3) los caps de exposición son preventivos para órdenes nuevas; un cruce de cap por movimiento adverso de mercado es fail-visible (telemetría), no violación auto-inventada ni liquidación automática.

## 7. Account binding

- Nueva entidad: `ProviderAccountBinding` (config de la execution Account, 1:1 con ella). **AccountStrategy permanece exactamente `Account + Strategy + MoneyManagement`** (D2-01/02/03); el binding es propiedad de la Account, no del AccountStrategy, y todas las AccountStrategies de la cuenta comparten la misma autoridad de provider (las reglas ACCOUNT-scoped no varían por estrategia).
- Campos: `account_id` (FK, identidad del binding activo); `provider_id` + `program_id` + `phase` (autoridad de negocio); `rule_set_id` + `rule_set_version` (autoridad corriente resuelta, hot-updatable); `transport` (`{transport_id: PROJECTX | NINJATRADER_BRIDGE | TRADOVATE_API | RITHMIC | CQG | SIM_EXECUTION, entitlement: ALLOWED | CONDITIONAL | FORBIDDEN | UNKNOWN, conditions[]: strings}`); `day_boundary` (referencia a la autoridad de DayBoundary de la cuenta — timezone + hora de reset, que ya existe en schema V3 vía `accounts.prop_ruleset_id → prop_rulesets.daily_reset_timezone/daily_reset_time` y `DayBoundaryCache`; C la consume, no la re-diseña); `enabled`; timestamps.
- Cardinalidades congeladas: Account 1 → 0..1 binding activo (re-binding = evento de ciclo de vida, histórico por versiones del binding; consistente con "cuenta nueva = account_id nuevo" del DayBoundaryCache); binding N → 1 programa; programa N → 1 provider; `(programa, fase)` → ≤1 RuleSet efectivo; transporte 0..N adapters físicos por transport_id (capability D6), pero el entitlement es dato del binding.
- Authority boundaries: (1) `AccountState` de Echo (`ACTIVE/CLOSE_ONLY/INACTIVE/ARCHIVED` en `ClientConfig`) sigue siendo autoridad operacional Echo; la admisión efectiva es `AccountState.AcceptsOpens() AND provider_admission == ALLOW` — dos autoridades independientes que se conjuncionan, sin fusionarse. (2) El **entitlement de transporte es separado del platform support**: el binding declara lo que la firma otorga por programa/fase (dato policy, con provenance); la capacidad técnica de un adapter es un asunto D6 (qué se puede construir). Lucid soporta NinjaTrader/CQG/Rithmic (platform support) sin entitlement direct-API conocido (entitlement UNKNOWN) — la separación es material y verificada en el corpus. (3) **UNKNOWN entitlement jamás se interpreta como permitido**: binding con entitlement UNKNOWN/FORBIDDEN no puede habilitarse para trading automatizado; si un binding habilitado deviene UNKNOWN/FORBIDDEN, §11 caso 4 aplica.
- Persistencia propuesta: tabla `echo.provider_account_bindings` (+ catálogos `echo.providers`, `echo.provider_programs`, `echo.provider_rule_sets`), propagadas en caliente por topics compactados (patrón webhook Hasura → handler → topic, igual que `account_strategy_risk_policy` hoy); el runtime lee por kache, sin I/O en hot path.

## 8. Enforcement pre-materialización

- Colocación exacta: es un **guard de materialización dentro de `echo/operation`**, al mismo nivel que los guards ya congelados en D2-04 §3.1 (`valid_until`, compatibilidad Strategy↔MM, resolución/pin de `contract_id`, sello de `direction`). La semántica D2-04 queda intacta: un OPEN **aceptado** materializa la Operation antes de MM/Orders; la admisión provider es parte de la **aceptación**. Sin Operation, sin MM, sin Orders (caso C del mandato: exchange abierto + provider bloquea ⇒ no hay Operation).
- Autoridad de evaluación: nueva función StateFun `echo/provider_rules` **keyeada por `account_id`**, dueña del estado de reglas del provider por cuenta: versión de RuleSet vigente, **estado de admisión** (`ALLOW` / `DENY_NEW_RISK` + razones tipadas + provenance de la regla que lo causa), estado de riesgo provider (daily loss / trailing / ventanas activas de news), exposición agregada corriente por contrato (§9), entitlement y flags de safety disparados. Patrón idéntico al chain RFC-005: ingiere `echo.account-snapshots.v1` + inputs de calendario/clock (seam B) + actualizaciones de RuleSet/binding (kache/topics compactados) + mensajes internos de las Operations (§9); publica el **admission snapshot** a un topic compactado `echo.provider-admission.v1` (kache) y decisiones a `echo.provider-decisions.v1` (egreso transaccional exactly-once, R14).
- Defensa en profundidad: (1) `echo/signal_fanout` pre-filtra OPENs de cuentas con `DENY_NEW_RISK` leyendo kache (patrón RFC-007 whitelist/account-state que D2-04 ya reutiliza) — optimización temprana; (2) el guard de materialización en `echo/operation` es la **verificación autoritativa** (mismo contexto serializado que los demás guards), leyendo el admission snapshot de kache con `version`/`evaluated_at`; snapshot ausente o stale más allá del umbral de configuración ⇒ `DENY_NEW_RISK` con razón `ADMISSION_STATE_STALE` (fail-closed). Signals REDUCE/CLOSE/CLOSE_ALL **no son filtradas** por admisión (§6 principio 1).
- Reglas evaluadas en este gate (todas account-scoped, ninguna dependiente de una Order inexistente): Account active/close-only (AccountState); ProviderProgram/fase eligibility (binding habilitado, fase vigente, RuleSet efectivo existente); automation entitlement (UNKNOWN/FORBIDDEN ⇒ deny); permitted instruments (+ resolvabilidad del Contract — seam de A ya existente como guard de D2-04); allowed new-risk window (ventana provider, con clock/session de B); estado de riesgo provider disparado (daily loss / trailing / news window ⇒ deny mientras esté activo). Retorna únicamente `ALLOW` o `DENY_NEW_RISK` (no existen resultados intermedios: cualquier duda es deny con razón tipada).
- Resultado DENY_NEW_RISK en materialización: la OPEN no se acepta; se emite `ProviderDecision{kind: DENY_NEW_RISK}` dur durable con razón + regla; telemetría al operador; la Strategy queda sin Operation (su estado lógico canónico no cambia — no hubo materialización). La estrategias siguen pudiendo emitir CLOSE/REDUCE no-ops (`NO_ACTIVE_OPERATION` de D2-04) y nuevas OPENs cuando la admisión revierta.

## 9. Enforcement por Order

- Colocación exacta: dentro de `echo/operation`, **después de que MM resuelve la decisión y produce 0..N Order requests y antes del egreso transaccional de comandos** (`echo.order-commands.{account_id}.v1`, §5.6 D2-04). Una Order denegada nunca entra al topic: no hay comando físico, no hay journal de adapter, no hay pregunta de idempotencia M2 — el gate está aguas arriba de ambos boundaries M1/M2.
- Reglas evaluadas (todas dependen de qty propuesta + exposición, imposibles antes de MM — por eso este gate existe): `max contracts/order` (qty ≤ cap por clase); `max exposure/account` (exposición lógica firme de la cuenta + qty propuesta ≤ cap); `max exposure/instrument|contract|product_group` (idem por agrupador). La exposición de la **propia key** (`account:strategy`) es exacta (el aggregate la conoce); la exposición de **otras keys de la misma cuenta** llega como **agregado por cuenta** que `echo/provider_rules` mantiene a partir de mensajes internos checkpoint-atómicos: cada `echo/operation` envía a `echo/provider_rules` (key `account_id`) un delta de exposición/cambio de estado al materializar, al cambiar exposición (fills) y al terminar; `echo/provider_rules` responde con el agregado actualizado de la cuenta cuando cambia (push por key a las Operations vivas de esa cuenta). Todo el flujo es mensajería interna StateFun capturada por el checkpoint (sin I/O externo, sin topic nuevo para este flujo).
- Consistencia declarada (riesgo asumido, no oculto): el agregado cross-key es **eventualmente consistente** con una ventana acotada por la latencia interna (mensaje→checkpoint), no atómico global. La exactitud plena exigiría serializar todas las Orders de una cuenta en una sola key, lo que violaría el ownership por `account:strategy` congelado en D2-04 — rechazado. Mitigaciones congeladas: los caps se configuran con margen de headroom (owner), el gate usa el agregado con su `as_of`/versión, y una brecha detectada (agregado vs comparación periódica) es telemetría fail-visible `PROVIDER_EXPOSURE_STATE_DIVERGENCE`, sin auto-corrección.
- Resultado `DENY_ORDER`: la Order no se emite; se emite `ProviderDecision{kind: DENY_ORDER}` con razón + regla + estado de exposición usado; MM recibe el rechazo como evento en su stream serializado y decide (reintentar con qty menor, reduce, o desistir). **Una Operation recién creada con TODAS sus entry orders denegadas no se borra ni silencia**: si MM desiste, registra intent de terminación y la Operation termina `TERMINAL(ENTRY_REJECTED)` — razón ya existente en D2-04 §3.3 reutilizada (la causa provider queda en la provenance del decision y del intent, no en un estado nuevo). Una Operation con exposición ya obtenida (adds denegados) continúa viva con su exposición; MM gestiona según su política. El lifecycle de D2-04 no cambia.
- Las Orders de salida (REDUCE/EXIT y las close-orders emitidas por el plano safety) **bypassan el gate** (§6 principio 1) pero pasan por los boundaries de idempotencia M1/M2 intactos.

## 10. Safety asíncrono

- Las reglas que actúan sin esperar una nueva Strategy Signal (forced-flat cutoff, flatten de news, daily-loss con flatten declarado, revocación de entitlement, holiday/weekend) viven en `echo/provider_rules` y producen **intents hacia Operations**, nunca mutaciones directas de estado ni terminalizaciones.
- Path de ForceClose provider: `echo/provider_rules` detecta el disparo ⇒ emite `ProviderForceClose{account_id, reason tipada, rule_ref, decision_id}` hacia **cada key `account:strategy` viva de esa cuenta** (conoce las keys por los mensajes de §9) ⇒ cada `echo/operation` lo trata como **intent de terminación `requested_by=SAFETY_PLANE`** con la provenance provider (R3 de D2-04): cancela Orders vivas, emite Orders de cierre por el path normal de comandos (gate de admisión no aplica a salidas), espera partial fills/reconciliación, y la Operation llega a `TERMINAL(SAFETY_FLATTEN)` **sólo cuando los guards de D2-04 se satisfacen** (`exposure==0 ∧ 0 live orders ∧ intent`). `ForceClose != TERMINAL` se preserva literalmente.
- El análogo account-wide legacy (`CloseHandlerFn`/`CloseBatchCommand`/`CloseAllAccountCommand`, emitidos por egress exactly-once a topics dinámicos por cuenta) es el patrón REUSE de este path; el nuevo path apunta al aggregate nuevo en vez del Edge MT y añade la trazabilidad `rule_ref`. El plano safety de owner (automations RFC-005, emergency close) sigue operando en paralelo sin cambios.
- No se inventa liquidación: si la semántica del provider no exige flatten (ej. instrumento recién prohibido), el runtime sólo deniega nueva exposición y alarma; la reducción queda a MM/owner (§11 caso 3).

## 11. Hot update de reglas

Regla general congelada: el RuleSet/bindings son dinámicos y su vigencia aplica **prospectivamente en la próxima evaluación o decisión**; jamás mutan `contract_id` pineado ni snapshot MM de una Operation viva (D2-01); la autoridad safety del provider es la parte explícitamente dinámica sobre Operations vivas y actúa sólo vía intents (R3). Cada cambio dispara reevaluación inmediata de `echo/provider_rules` (nuevo admission snapshot + eventos safety si corresponde).

- **Cutoff se adelanta y ya pasó:** la reevaluación con la versión nueva encuentra "now fuera de ventana" ⇒ `DENY_NEW_RISK` inmediato + ForceClose provider si la familia forced-flat lo declara; el horizonte del nuevo cutoff aplica desde la evaluación, sin efecto retroactivo sobre decisiones ya tomadas (las Orders ya en el venue siguen su curso físico; el intent cancela las vivas que pueda).
- **Max exposure baja bajo exposición actual:** regla prospectiva: se deniega cualquier Order que empuje más allá del cap nuevo (adds denegados, `DENY_ORDER`); la exposición existente NO se liquida automáticamente (ninguna familia del corpus aceptado exige reducción forzada por breach pasivo) — se emite telemetría fail-visible `PROVIDER_EXPOSURE_OVER_LIMIT` y sólo se flatten si la regla tipada declara `flatten=true` (default false, YAGNI).
- **Instrument pasa a forbidden:** `DENY_NEW_RISK` para ese instrumento de inmediato (nuevas OPENs y adds); posiciones existentes no se liquidan por defecto (idem anterior); las reducciones/cierres de ese instrumento siempre pasan.
- **Automation entitlement revocado** (ej. fase cambia a una donde la API/automatización está prohibida): binding deviene no-habilitable ⇒ `DENY_NEW_RISK` permanente (`ENTITLEMENT_REVOKED`) + ForceClose provider sobre todas las Operations vivas de la cuenta (Echo debe dejar de operar la cuenta, no dejarla medio viva) + alerta de operador y binding requiere re-habilitación manual. La fase detectada al cambiar el binding publicado; no se auto-detecta desde la firma (§4).
- **Daily-loss rule cambia** (límite/basis/tipo): los acumuladores de estado provider recalculan bajo la regla nueva prospectivamente; si la regla nueva ya está breached al evaluarse (ej. trailing más agresivo), dispara en el momento de la reevaluación (deny + flatten declarado), sin reconstructar historia.

## 12. Provenance

- Registro mínimo: `ProviderDecision{decision_id UUIDv7; account_id; account_strategy_id?; operation_id?; kind: ADMIT_OPERATION | DENY_NEW_RISK | ADMIT_ORDER | DENY_ORDER | SAFETY_FORCE_CLOSE; provider_id; program_id; phase; rule_set_id; rule_set_version; rule_family; reason (enum tipado + detalle); evaluated_at; exposure_state_as_of?}`. Una decisión material siempre puede responder programa/fase/versión/regla/razón/timestamp sin history engine genérico.
- Persistencia: (1) las decisiones originadas en `echo/provider_rules` salen por su propio egreso Kafka transaccional exactly-once a `echo.provider-decisions.v1` (event topic; projector PG eventual para queries/UI; no es recovery authority); (2) las decisiones tomadas dentro de `echo/operation` (admisión de materialización y DENY_ORDER) se emiten como record `PROVIDER_DECISION` por el **mismo egreso transaccional de proyecciones/facts de R14** (`echo.operation-projections.v1`), checkpoint-atómico con el estado que gatean — sin writer fuera de la frontera (misma disciplina que R14). (3) OTel complementa (métricas/logs), no sustituye el fact durable.
- Lo que guarda Operation: **sólo referencia**. Campo additivo propuesto `admission_decision_id` (nullable) en Operation = el `decision_id` que la admitió; `termination` conserva su shape de D2-04 (`requested_by=SAFETY_PLANE` + razón) y el intent de ForceClose porta el `decision_id` provider para trazabilidad; las Orders denegadas no existen como Orders (sólo decision). Sin log de decisiones embebido en el aggregate, sin tablas de eventos (R9 intacto). El campo additivo y el enum de `reason` requieren ratificación técnica del manager (§17).

## 13. Disposición Echo V3 (source audit acotado)

Método: `git show 372af59a:<path>` sobre clon verificado (worktree limpio, HEAD = baseline). Blob SHAs verificados en ventana salvo indicación.

| Pieza V3 | Disposición | Evidencia física (path · símbolo · blob) |
|---|---|---|
| ExecutionPolicy | **ADAPT** | `v3/sdk/domain/execution_policy.go` · `ExecutionPolicy/ExecutionPolicyEvent` · `295f7ea2c605`. Binding+riesgo+knobs mezclados; se separa en AccountStrategy (binding) / config MM / knobs; el patrón tabla→webhook→topic compactado (`echo.execution-policies.v1`, `POLICY_UPDATE/DELETE`) es el transporte canónico para los nuevos catálogos provider. |
| StrategyConfigFn | **REUSE (patrón)** | `v3/core/internal/functions/strategy_config.go` · KVS por key sobre topic compactado · `b89a9a1a61f7`. La función de config de RuleSets/bindings sigue este patrón exacto. |
| AccountSnapshot / Account state | **REUSE** | `v3/sdk/domain/client_config.go` · `AccountState` (ACTIVE/CLOSE_ONLY/INACTIVE/ARCHIVED) + `AcceptsOpens/AcceptsCloses` + `TradingWhitelist(Mode)` · `587eb5c4db63`; `v3/sdk/domain/snapshots.go` · Topics · `d319d0a3`. `AccountState` es ya el input "account active/close-only" del gate de admisión; la whitelist operacional de cuenta complementa (no se sustituye por) permitted-instruments. |
| DayBoundaryCache | **REUSE (patrón) / EXTEND** | `v3/core/internal/functions/account_sync.go` · `DayBoundaryCache/DayBoundaryEntry` · `b0f8f1ce426c`. Cache por cuenta con timezone + reset desde `prop_rulesets` y acumuladores daily HWM/prev-day-close con cruce de día — es el anclaje de reset del estado provider (caso F). Deuda registrada D1: su fallback UTC 23:00 no se propaga a Futures; la autoridad DayBoundary formal es del workstream de cuenta/sesión (seam B). |
| AutomationEvaluatorFn | **REUSE (patrón)** | `v3/core/internal/functions/automation_evaluator.go` · `AutomationEvaluatorFn` · `9503410ef0af`. Chain snapshot-enriquecido → evaluación sin I/O → egress exactly-once; `echo/provider_rules` replica la forma para reglas provider. |
| Typed automation evaluators/registry | **REUSE/EXTEND** | `v3/core/internal/automation/evaluator.go` · `RuleEvaluator/EvaluatorRegistry/TargetCloseEvaluator/DailyLossCloseEvaluator` · `bf97b13ae0df`; `v3/core/internal/automation/automation.go` · `AutomationEvaluator` · `25dcfbdc0b31`; `trigger_cache.go` · `TriggerCache` (cooldown) · `8ddb8b14dd84`. El Strategy Pattern con configs tipadas (`TriggerConfig` PERCENT/ABSOLUTE × bases) es exactamente la forma "familias tipadas sin if/then genérico"; las familias provider se registran como evaluadores tipados adicionales, separados de los AutomationProfiles owner-configurados (autoridad distinta). |
| AutomationCache | **REUSE (patrón)** | `v3/core/internal/automation/cache.go` · `AutomationCache` · `39a461e3f740`; topic `echo.automation-profiles.v1` (compacted) en `v3/sdk/domain/snapshots.go` `d319d0a3`. Mismo patrón para el catálogo de RuleSets (`echo.provider-rulesets.v1`). |
| CloseHandler safety patterns | **REUSE (patrón)** | `v3/core/internal/functions/close_handler.go` · `CloseHandlerFn/emitCloseCommands` (egress exactly-once, topic dinámico por cuenta) · `8dba9731bbce`; `v3/sdk/domain/trade_close.go` · `CloseCommand/CloseBatchCommand/CloseAllAccountCommand` · `3ffe13e69d99` (SHA de D1 pack). Flatten account-wide es el precursor directo del path `ProviderForceClose`; el nuevo path apunta al aggregate `echo/operation` con intents R3. |
| ClientConfig state/whitelist | **REUSE** | `v3/sdk/domain/client_config.go` · `ClientConfig` (entrega hot al Edge, `echo.account-configs.v1`) · `587eb5c4db63`. El binding provider se propaga con este mismo mecanismo; el Edge/adapter futuro recibe lo mínimo operativo (estado, whitelist), no el RuleSet completo. |
| Gateway automation/config handlers | **REUSE/ADAPT** | `v3/gateway/internal/automation/handler.go` · `5f0a99e24842`; `executor.go` · `ActionExecutor/ExecutorRegistry/CloseAllExecutor` · `593d70b1`; `news_blackout_evaluator.go` · `4bda7e10` (ventanas de news con SET/RESTORE state + whitelist — precedentes directos de la familia news); `execution_policy_handler.go` · webhook Hasura → topic · `42048c05fa34`; `evaluator_registry.go` · `63ac50d7`. Los executors se extienden con acciones provider-safety; el pipeline webhook→Kafka es el transporte de los catálogos nuevos. |
| kache / config topics | **REUSE** | `v3/sdk/kache/README.md` · `faf0f7e9d48f`; `v3/sdk/statefun/constants.go` · Topics/Egress IDs · `2f8ab57e3f35`. Lectura in-process de configs compactadas en hot path — el mecanismo del admission snapshot. |
| `echo.prop_rulesets` + `accounts.prop_ruleset_id` | **REUSE (concepto) / REPLACE (shape)** | `v3/sdk/postgres/migrations/001_schema_baseline.up.sql` (líneas ~626-666) · `a186be357e9a`. Precursor legacy: ya tipa daily loss (pct + basis + DAY_HIGH/PREV_CLOSE), total loss static/trailing, news windows, overnight/weekend/hedging, reset timezone/time — valida las familias; pero identity por `prop_firm text`, `phase_type` enum artificial, reglas en columnas planas sin version/provenance/effective_at y sin programa — exactamente los defectos que D2-05C corrige. No se extiende; se migra a los catálogos nuevos (su FK alimenta el DayBoundary existente durante la transición). |
| Concepto Provider | **NEW** | `git grep -i provider` sobre `v3/{sdk,core,gateway}` @ baseline: sin concepto de prop firm como policy owner (sólo `prop_rulesets` legacy y ruido). Provider/ProviderProgram/ProviderRuleSet/ProviderAccountBinding + `echo/provider_rules` + admission/order gates + decisiones son dominio nuevo, coherente con la matriz D1 (Provider/Program/RuleSet = NEW/ADAPT). |

## 14. Cross-TOP seams

Se necesita de TOP A (sin rediseñarlo): (1) `instrument_id` canónico y `contract_id` físico pineado (ya congelados en D2-01/D2-04) — permitted-instruments y caps operan sobre instrument/contract, nunca sobre símbolos de plataforma; (2) el execution binding / contract resolver (canonical → physical + venue ids) ya existe como guard de materialización de D2-04 — C lo consume; (3) **input requerido**: que el `Instrument` de A exponga `exchange` y `product_group` (ej. grupo equity-index CME) porque los caps por grupo y permitted-instruments por exchange del corpus se declaran a ese nivel; si A no lo congeló, escalar al SUBMANAGER: o A añade el atributo, o V1 degrada esos caps a nivel contract/instrument con pérdida de fidelidad documentada. Sin contradicción detectada con D2-05A en lo ya integrado; este es el único requisito nuevo.
Se necesita de TOP B (sin modificar Calendar): (1) `exchange open/closed` y `session/trade date` por instrumento/exchange; (2) **provider-clock/timezone inputs**: las ventanas y cutoffs del provider se evalúan en el clock del programa (ej. America/Chicago para Topstep), que no es el clock del exchange ni el civil — B debe exponer la resolución de ese clock (config por binding + holiday/early-close calendar) como input de C; (3) holiday/early-close feeds para triggers programados de forced-flat/weekend.
Contradicciones a resolver por el SUBMANAGER: (1) la autoridad "ProviderProgram trading overlay" (ventanas/cutoffs provider) debe permanecer **distinta** de `ExchangeSession` en el modelo de B — D2-04/Front E y la integración D2-05 ya declaran tres autoridades (ExchangeCalendar/ExchangeSession, overlay de ProviderProgram, DayBoundary de Account); C consume las tres y confirma que su enforcement no requiere fusionarlas — si B las modeló fusionadas, es contradicción material. (2) La autoridad de **Account DayBoundary** (timezone+reset) aparece referida por §9 del mandato pero su diseño formal vive en el workstream de cuenta/sesión (D2-05B/lado cuenta): C sólo declara la dependencia (el reset diario del estado provider se ancla a ella, caso F) y la deuda del fallback UTC heredado. (3) El assignment de quién publica el calendar/holiday feed que C consume (B vs owner config) queda para la integración D2-05.

## 15. Casos obligatorios

- **Caso C — exchange abierto, provider bloquea:** Signal OPEN llega a `echo/operation`; guard de materialización consulta admission snapshot: `DENY_NEW_RISK` (razón p.ej. `WINDOW_CLOSED` con `rule_set_version` v<ref>) ⇒ la OPEN no se acepta: **no hay Operation, ni MM, ni Orders**; se emite `ProviderDecision{DENY_NEW_RISK}` dur durable + telemetría. El exchange pudo estar abierto (input B OK) y `AccountState ACTIVE`: la conjunción de autoridades falla sólo por provider. Cierres/REDUCEs de otras Operations de la cuenta siguen fluyendo.
- **Caso D — forced flat:** RuleSet declara cutoff 3:10 PM CT; `echo/provider_rules` dispara en el trigger ⇒ `ProviderForceClose` hacia cada key viva de la cuenta ⇒ cada `echo/operation` registra `termination{SAFETY_PLANE, SAFETY_FLATTEN}` (R3), cancela Orders working, emite close orders (gate de admisión no aplica a salidas), espera fills parciales/tardíos; la Operation llega a `TERMINAL(SAFETY_FLATTEN)` sólo al satisfacer guards (exposición 0 + 0 Orders vivas + intent). **No es terminal instantáneo.** Un fill tardío post-terminal sigue el path R13 (`POST_TERMINAL_EXECUTION_BREACH`) sin revivir nada.
- **Caso F — reset de Account DayBoundary:** al cruzar el day boundary de la cuenta (timezone+reset del binding/DayBoundary authority, ej. 16:00 CT), `echo/provider_rules` resetea los acumuladores provider diarios (daily HWM, ancla prev-day-close, deny por daily-loss expira) bajo autoridad de cuenta, **sin tocar ExchangeSession/trade-date de B** (que puede seguir en el trade date anterior para bar semantics). Las familias con semántica de no-reset (trailing lock, total loss) no se resetean — su reset_semantics es tipado por familia. El reset re-habilita new risk si la única causa de deny era el estado diario.
- **Caso G — RuleSet update live:** nueva versión `ACTIVE` publicada ⇒ binding resuelve autoridad nueva ⇒ reevaluación inmediata; toda decisión nueva porta la `rule_set_version` nueva en su provenance; las Operations vivas conservan contract pineado y snapshot MM; la autoridad safety nueva actúa vía intents si algún caso de §11 aplica (cutoff adelantado ya pasado, cap bajo exposición, instrumento prohibido, entitlement revocado, daily-loss más agresiva ya breached).

## 16. Riesgos y unknowns

- **Consistencia eventual del agregado cross-key (order gate):** brechas acotadas por latencia interna checkpoint; mitigado con headroom de configuración, `as_of` y divergencia fail-visible; riesgo aceptado porque la alternativa (serialización por cuenta) rompe D2-04. Si la cohorte real tiene varias estrategias concurrentes por cuenta con caps ajustados, reevaluar margen.
- **Fidelidad de valores por programa:** las familias están congeladas, los valores no; onboarding de un programa exige config verificada con provenance (owner); valores UNKNOWN ⇒ programa no activable (fail-closed), no defaults. El corpus V1 cubre 8 firms; los semánticamente raros (ej. scaling plans tipo Topstep ladder por balance) requieren excepción provider-specific registrada, no deformación de familias.
- **Dependencia del news feed:** la familia news hereda la dependencia de eventos externos del RFC-007 existente (cobertura/latencia del feed); sin feed el estado de news es UNKNOWN ⇒ si la regla está declarada, fail-closed a deny durante la duda.
- **Fases y entitlement son datos policy que las firmas cambian unilateralmente:** Echo depende del refresh de provenance del catálogo (procedimiento owner); drift entre política real y RuleSet es riesgo operacional del owner, no detectable en runtime.
- **Transiciones de fase manuales en V1:** un cambio real de fase de la firma no se auto-detecta; el owner debe publicar el binding nuevo (§4). Riesgo de binding stale operado con reglas de fase incorrecta — mitigado por alertas de reconciliación y fail-closed ante inconsistencias de admisión.
- **Consistency/copy warn-only:** Echo advierte pero no impide configuraciones que violen reglas de consistencia o copy entre cuentas del owner (ej. misma Strategy en N cuentas del mismo programa); es tensión real de cohorte que el owner debe resolver operativamente (no owner-blocker de diseño).
- **DayBoundary heredado:** el fallback UTC 23:00 del DayBoundaryCache actual no debe alimentar el estado provider (deuda D1); el binding debe exigir day boundary explícito para cuentas futures (fail-closed si falta).

## 17. Decisiones owner

- `OWNER DECISIONS REQUIRED: NONE`. El diseño vive dentro de D2-01/02/03, D2-04 y los requisitos de producto del proyecto; ningún hallazgo requirió research nuevo (§17 del mandato: el corpus aceptado alcanzó; FACT vs valor-onboarding quedó separado en §5).
- Ratificaciones técnicas ordinarias para el manager (no owner, no cambian semántica): (1) nombres físicos nuevos: functions `echo/provider_rules`, topics `echo.provider-rulesets.v1` / `echo.provider-bindings.v1` / `echo.provider-admission.v1` / `echo.provider-decisions.v1`, tablas `echo.providers` / `echo.provider_programs` / `echo.provider_rule_sets` / `echo.provider_account_bindings` / `echo.provider_decisions` (numeración de migraciones a coordinar al implementar, como D2-04); (2) enum tipado de `reason` de admisión/deny (`NO_RULESET_AUTHORITY`, `ADMISSION_STATE_STALE`, `WINDOW_CLOSED`, `INSTRUMENT_FORBIDDEN`, `EXPOSURE_CAP`, `ENTITLEMENT_REVOKED`, `RISK_STATE_TRIGGERED`, `NEWS_WINDOW`, `BINDING_DISABLED`); (3) campo additivo `admission_decision_id` en Operation (provenance §12); (4) reutilización de `TERMINAL(ENTRY_REJECTED)` para entradas denegadas por provider con provenance en decision/intent (sin estado nuevo); (5) atributo `exchange`/`product_group` requerido a Instrument de TOP A (§14).

## Handoff

```text
D2-05C STATUS:
READY_FOR_SUBMANAGER_REVIEW

ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-05C Provider Program Rules.md

AGENTS-OS SHA:
4cd85d357e395eb36f62ef3123b8898d7b6844d9

ECHO BASELINE:
372af59a7b83604781346613da01e3d510ea1360 (HEAD verificado, worktree limpio)

PROVIDER MODEL:
Provider (policy owner, provider_id canónico, 1→0..N programas) → ProviderProgram (producto real,
nombre libre, sin enums de negocio) → fase (atributo del binding + dimensión del catálogo, NO
aggregate) → ProviderRuleSet versionado por (provider, programa, fase) con version/effective_at/
provenance obligatoria; ≤1 versión efectiva; cero autoridad ⇒ fail-closed. Account 1→0..1
ProviderAccountBinding (programa, fase, RuleSet resuelto, transport entitlement separado de
platform support, day_boundary por referencia); AccountStrategy intacta (Account+Strategy+MM).
Scope honesto: runtime enforcea sólo ACCOUNT-scoped; trader/household/cross = eligibility.
Legacy prop_rulesets = REUSE concepto / REPLACE shape (enums de fase y firmas-por-nombre son
los anti-patrones corregidos).

ENFORCEMENT MODEL:
Tres planos reconciliados con D2-04: (1) pre-materialización: guard de admisión dentro de
echo/operation (autoritativo, kache-fed, fail-closed stale) + pre-filtro en signal_fanout;
ALLOW | DENY_NEW_RISK antes de crear Operation (C: exchange abierto + provider bloquea ⇒ no
Operation); (2) order-level: entre decisión MM y egreso transaccional de comandos; max/order,
max exposure account/instrument/grupo usando exposición propia exacta + agregado cross-key
mantenido por echo/provider_rules vía Sends checkpoint-atómicos (eventualmente consistente,
fail-visible); DENY_ORDER ⇒ no egress, MM decide, entradas todas denegadas ⇒
TERMINAL(ENTRY_REJECTED) con provenance, nunca delete silencioso; salidas jamás bloqueadas;
(3) safety asíncrono: echo/provider_rules (keyed account_id, patrón RFC-005) emite
ProviderForceClose como intent SAFETY_PLANE a cada key viva; TERMINAL(SAFETY_FLATTEN) sólo por
guards R3. Familias tipadas + params + excepciones provider-specific registradas; sin DSL.

HOT UPDATE:
Regla general prospectiva: nueva versión ⇒ reevaluación inmediata; decisiones nuevas usan la
regla vigente con provenance de versión; contract pin y MM snapshot jamás mutan; safety es la
autoridad dinámica y actúa sólo vía intents. Casos: cutoff adelantado ya pasado ⇒ deny+flatten
inmediatos, sin retroactivo; cap bajo exposición ⇒ adds denegados, sin liquidación inventada
(sólo flatten si la regla tipada lo declara, default no); instrumento prohibido ⇒ deny new risk,
cierres siempre pasan; entitlement revocado ⇒ DENY_NEW_RISK permanente + ForceClose de vivas +
alerta + re-habilitación manual; daily-loss cambia ⇒ recálculo prospectivo, breach actual dispara
al evaluarse.

ECHO V3 REUSE/ADAPT:
Patrones REUSE: cadena RFC-005 (AutomationEvaluatorFn 9503410ef0af) para echo/provider_rules;
EvaluatorRegistry + configs tipadas (bf97b13ae0df/25dcfbdc0b31) como forma de las familias;
AutomationCache/kache + topics compactados (39a461e3f740, faf0f7e9d48f) para catálogos;
AccountState/TradingWhitelist (587eb5c4db63) como input del gate; CloseHandlerFn (8dba9731bbce)
como precursor del ForceClose path; webhook→topic (42048c05fa34) como transporte de catálogos.
ADAPT: ExecutionPolicy (295f7ea2c605) se separa; DayBoundaryCache (b0f8f1ce426c) ancla reset
provider (fallback UTC no propaga). REPLACE shape: prop_rulesets (a186be357e9a). NEW: dominio
provider + gates + decisiones; sin concepto Provider previo en V3 (grep verificado).

CONTRACTS FOR A/B:
A: consume instrument_id/contract_id/resolver (congelados); REQUIERE Instrument.exchange +
product_group para caps por grupo (si A no lo tiene, degradación documentada o escalado).
B: consume exchange open/closed, session/trade date, provider-clock/timezone por binding,
holiday/early-close; exigencia: provider overlay (ventanas/cutoffs) permanece autoridad DISTINTA
de ExchangeSession; Account DayBoundary es autoridad propia (C sólo la referencia; reset de
estado provider se ancla a ella, caso F). Escalados al SUBMANAGER: atributo exchange/product_group
en A; ownership del calendar/holiday feed; verificar que B no fusionó overlay con session.

OWNER DECISIONS REQUIRED:
NONE. Ratificaciones técnicas manager: nombres functions/topics/tablas; enum reason;
admission_decision_id en Operation; ENTRY_REJECTED con provenance para denegaciones provider;
atributo exchange/product_group de A.

MATERIAL RISKS:
Order gate cross-key eventualmente consistente (headroom + fail-visible; alternativa rompe
D2-04); valores por programa exigen onboarding verificado (UNKNOWN fail-closed); news depende
del feed RFC-007; fases/entitlement son policy unilateral de firms (procedimiento owner de
refresh); transiciones de fase manuales V1 (binding stale posible); consistency/copy warn-only.
```
