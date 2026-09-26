
### Rollover

Owner manual V1.

Hot update.

Debes congelar:

```text
resolve Contract at Operation creation
Operation pins result
mapping update applies to new Operations
existing Operation keeps old Contract
```

Exact behavior de cierre de una Operation pinneada al contrato viejo.

No auto-migration.

No automatic rollover.

Si el venue ya no permite operar/cerrar el contrato viejo:

fail-visible / execution edge; no inventar remapping.

### Units

Eliminar pips como universal unit.

Modelo mínimo cross-market para que MM pueda trabajar con:

```text
price
ticks
points
contract quantity
tick value
contract multiplier
currency
```

sin diseñar equities ahora.

### Persistence / hot config

Decidir:

- fuente de config;
    
- Kafka compacted/config pattern;
    
- cache/resolver;
    
- identity/persistence.
    

Reutilizar patrón existente cuando encaje.

---

# 6. D2-05B — TOP: SESSION / CALENDAR

El TOP B debe cerrar:

```text
ExchangeSession
Calendar
Provider trading-window overlays
Account DayBoundary separation
```

## Autoridades separadas

No mezclar:

```text
ExchangeSession
ProviderProgram trading window
Account DayBoundary
```

Son tres cosas distintas.

Ejemplo ya probado:

```text
CME NQ market available hasta 16:00 CT
Topstep forced flat 15:10 CT
Account daily reset = otra autoridad
```

---

## Resolver

### Time authority

Usar timezone semántica real:

```text
IANA timezone
```

no fixed UTC offset.

Debe soportar DST.

### Exchange calendar

Modelo mínimo para:

- regular open/close;
    
- maintenance breaks;
    
- session/trade date;
    
- holidays;
    
- early closes;
    
- product/session overrides cuando sean necesarias.
    

No hardcodear una fórmula universal CME.

### Session date

Resolver conceptualmente:

```text
event timestamp
    ↓
exchange/calendar
    ↓
trade/session date
```

incluyendo sesiones que empiezan el día civil anterior.

### Named Strategy sessions

Una Strategy debe poder configurar:

```text
NY
London
CME ETH/RTH
custom trading window
```

sin offsets hardcodeados.

Define si son:

- named windows sobre un ExchangeCalendar;
    
- o equivalente KISS.
    

No conviertas esto en otro calendar engine.

### Bars

D2-05 no diseña Market Runtime completo, pero debe dejar contrato suficiente para D2-06:

- bar bucket necesita consultar Session/Calendar;
    
- forming/closed semantics deben poder respetar breaks/open/close;
    
- LIVE/REPLAY/BACKTEST deben usar la misma autoridad.
    

No diseñar todavía bar builder interno.

### Provider overlay

Provider allowed-time/forced-flat debe aplicar sobre exchange session sin modificarla.

Ejemplo:

```text
Exchange says OPEN
Provider says NO_NEW_RISK
```

debe ser representable.

---

# 7. D2-05C — TOP: PROVIDER / PROGRAM / RULESET

El TOP C debe cerrar el modelo:

```text
Provider
    ↓
ProviderProgram
    ↓
Phase
    ↓
ProviderRuleSet
```

sin DSL.

---

## Provider

Entidad de firma/venue/business provider.

Ejemplos conceptuales:

```text
Topstep
Lucid
...
```

No mezclar Provider con transport tecnológico.

Una prop puede usar diferentes:

```text
ProjectX
NinjaTrader
Tradovate
Rithmic
```

Transport entitlement es otro concern.

---

## Program

Representa el producto/programa real de la prop.

Ejemplo conceptual:

```text
evaluation 50k
funded 50k
live
```

No asumir que todos los providers usan los mismos nombres.

---

## Phase

Resolver si Phase necesita entidad/config propia o si basta como atributo dentro del Program/Account binding.

KISS.

No crear entidad sólo porque el nombre suena correcto.

La prueba es:

> ¿cambian reglas operativas de manera material según la fase?

Si sí, modelarlo limpiamente.

---

## ProviderRuleSet

Éste es el **único lugar de D2 donde version/provenance explícita ya tiene justificación aceptada**.

No convertir esto en generic version framework.

Resolver:

```text
rule_set_id
version/provenance
effective config
source/evidence metadata mínima
```

cuando sea útil.

### Rule families

Usar el corpus aceptado.

Normalizar familias comunes sólo cuando haya semántica real compartida.

Considerar como mínimo:

- allowed trading window;
    
- forced-flat cutoff;
    
- permitted instruments;
    
- contract/max quantity;
    
- daily loss / trailing drawdown inputs si deben estar disponibles al enforcement;
    
- automation/copy restrictions cuando tengan efecto runtime;
    
- consistency/news/overnight/weekend rules sólo si son runtime enforceable/materiales para V1.
    

No meter reglas administrativas que Echo no puede/shouldn't enforce en hot path.

### No DSL

Modelo esperado:

```text
typed common rule families
+
provider/program parameters
+
explicit provider-specific exceptions
```

No:

```text
if/then arbitrary expression language
```

---

# 8. ACCOUNT BINDING

Los tres TOPs deben converger sobre esto.

Una execution Account debe poder determinar:

```text
Provider
ProviderProgram
current phase/state if needed
RuleSet authority
execution venue/transport capability
```

sin meter todo dentro de `AccountStrategy`.

`AccountStrategy` sigue siendo:

```text
Account
+
Strategy
+
MoneyManagement
```

No transformarlo en ProviderProgramConfigMegaObject.

Determinar la relación limpia:

```text
Account -> ProviderProgram / rules
AccountStrategy -> Strategy + MM binding
```

---

# 9. RULE ENFORCEMENT — INTEGRACIÓN OBLIGATORIA

El Submanager debe integrar qué componente aplica qué regla.

Diseñar al menos estos boundaries:

### Antes de abrir riesgo

```text
Signal
  ↓
fan-out
  ↓
AccountStrategy eligibility
  ↓
ProviderProgram/Account rule gate
```

Puede resultar:

```text
ALLOW
DENY_NEW_RISK
```

sin crear Operation si el OPEN es rechazado antes de materialización.

Debes reconciliar esto con D2-04.

### Operation viva

Una regla vigente puede cambiar mientras existe una Operation.

Ejemplo:

```text
forced-flat cutoff reached
```

Debe producir:

```text
safety/provider termination intent
```

hacia la Operation existente.

NO mutar el snapshot de Operation.

NO esperar la próxima Signal de Strategy.

### Rule hot update

Debes resolver qué pasa si RuleSet cambia live.

Reglas de seguridad vigentes NO deben quedar congeladas en una Operation antigua sólo porque D2-01 snapshottea MM config.

Provider safety authority es dinámica.

### Provenance

Una decisión importante debería poder registrar qué:

```text
ProviderProgram
RuleSet version
```

la produjo, sin convertir Operation en generic history framework.

Decide el punto mínimo donde guardar provenance.

---

# 10. CONTRATO + SESSION + PROVIDER — CASOS INTEGRADOS

El Submanager debe demostrar estos casos.

## A — rollover manual

```text
NQ -> NQZ6

Operation A created
contract_id = NQZ6

owner hot updates:
NQ -> NQH7

Operation A stays NQZ6
next Operation B -> NQH7
```

## B — feed/execution identifiers differ

Strategy recibe market semantics de NQ.

Feed usa identifier X.

Execution Account usa provider contract identifier Y.

Strategy sigue agnóstica.

## C — CME open, provider blocks

ExchangeSession:

```text
OPEN
```

ProviderProgram:

```text
NO_NEW_RISK
```

OPEN Signal no materializa nueva Operation para esa AccountStrategy.

## D — forced flat

Operation ACTIVE.

Provider cutoff.

Safety/provider plane entrega termination intent.

Operation sigue lifecycle D2-04 hasta exposure 0 + no live Orders.

## E — early close

Holiday override cambia session boundary.

LIVE y REPLAY deben resolver la misma session/trade date.

## F — account day reset

Account DayBoundary ocurre en un horario que no coincide con exchange close.

No modifica ExchangeSession.

No cambia Contract.

## G — rule update live

RuleSet hot update endurece cutoff o max exposure.

Nuevas decisiones usan regla vigente.

Operation existente no cambia Contract/MM snapshot, pero safety constraints vigentes pueden actuar sobre ella.

## H — old contract edge

Operation pinneada a Contract viejo.

Mapping ya apunta al siguiente contrato.

Close/REDUCE de esa Operation sigue dirigiéndose a su Contract pinneado.

Nunca al Contract nuevo silenciosamente.

---

# 11. ECHO V3 — CONTRASTE FÍSICO

Cada TOP inspecciona sólo source relevante.

Como mínimo revisar precursors/patterns:

```text
InstrumentSnapshot
inst_snapshot
symbol mapping / hot update
AccountSnapshot
ExecutionPolicy
StrategyConfig
DayBoundary / DayBoundaryCache
ClientConfig / account state
automation evaluator / CloseHandler safety patterns
kache/config topics
Gateway handlers relevantes
```

No recorrer repo completo.

Para cada pieza clasificar:

```text
REUSE
EXTEND
ADAPT
REPLACE
DEFERRED_DEBT
```

Dejar repo/path/símbolo/blob SHA cuando sea material.

No confiar ciegamente en D1.

---

# 12. RESEARCH POLICY

D1 ya entregó evidencia suficiente.

NO hacer web research general.

Sólo investigar externamente si aparece una pregunta concreta que:

```text
cambia identity
cambia lifecycle
cambia enforcement
o bloquea el diseño
```

En ese caso:

- first-party sources;
    
- scope estrecho;
    
- artifact durable;
    
- distinguir FACT / INFERENCE.
    

No abrir otra investigación de props.

---

# 13. CHILD ARTIFACTS

Cada TOP debe dejar un artefacto durable corto y técnico:

```text
main/10-projects/Echo Futures/
Echo Futures — D2-05A Instrument Contract.md

main/10-projects/Echo Futures/
Echo Futures — D2-05B Session Calendar.md

main/10-projects/Echo Futures/
Echo Futures — D2-05C Provider Program Rules.md
```

Estos son evidence/design inputs.

El Submanager debe luego crear el único artefacto integrado authority candidate:

```text
main/10-projects/Echo Futures/
Echo Futures — D2-05 Instrument Session Provider.md
```

No pedir al Primary Manager que lea tres handoffs para integrar.

Esa responsabilidad es del SUBMANAGER.

---

# 14. INTEGRATED ARTIFACT — CONTENIDO MÍNIMO

Debe contener:

```text
1. Executive verdict
2. Minimal entity model
3. identities + cardinalities
4. Instrument / Contract / identifier mapping
5. hot rollover resolver semantics
6. economic unit semantics
7. ExchangeSession / Calendar
8. trade/session date semantics
9. provider window overlays
10. Provider / Program / Phase / RuleSet
11. Account binding
12. enforcement ownership matrix
13. hot-update semantics
14. interaction with D2-04 Operation lifecycle
15. LIVE / REPLAY / BACKTEST contract
16. Echo V3 REUSE/EXTEND/ADAPT/REPLACE map
17. migration implications
18. risks/debts
19. owner decisions genuinely required
20. acceptance cases A-H
```

No rellenar con pseudocódigo ornamental.

---

# 15. OWNER DECISIONS

El Submanager puede cerrar decisiones técnicas ordinarias.

Escalar sólo si aparece una decisión real de producto/domain authority que las decisiones existentes no determinen.

No preguntar por:

- nombres de structs;
    
- nombres de topics;
    
- exact persistence table names;
    
- Go layout;
    
- cache implementation;
    
- enum spelling;
    
- whether to use one or two structs when semantics are equivalent.
    

Sí escalar si existe, por ejemplo:

```text
una regla owner ambigua sobre cuándo una prop puede forzar cierre
una contradicción material sobre quién gobierna un live Operation
una exigencia productiva nueva de auto-rollover
```

No inventar blockers.

---

# 16. GATE

El Submanager NO puede marcar D2-05 cerrado.

Estados permitidos:

```text
D2-05 STATUS:
READY_FOR_MANAGER_REVIEW
BLOCKED_OWNER_DECISION
BLOCKED_EVIDENCE
```

Nunca:

```text
PASS
CLOSED
EF_D2_DESIGN_PASS
```

Eso pertenece al Primary Manager + Owner.

---

# 17. HANDOFF FINAL

Entrega únicamente un handoff corto:

```text
D2-05 STATUS:
READY_FOR_MANAGER_REVIEW
| BLOCKED_OWNER_DECISION
| BLOCKED_EVIDENCE

INTEGRATED ARTIFACT:
<path>

CHILD ARTIFACTS:
<3 paths>

AGENTS-OS SHA:
<sha>

ECHO BASELINE:
<sha>

INTEGRATED MODEL:
<10-15 líneas máximo>

KEY REUSE/ADAPT:
<5-10 líneas>

OWNER DECISIONS REQUIRED:
<NONE o sólo las reales>

MATERIAL RISKS:
<sólo riesgos reales>

NEXT:
Primary Manager review only.
```

NO avances a D2-06.

Termina después del handoff.