---
type: agent_memory
scope: agent
created: 2026-07-25
updated: 2026-09-09
memory_state: archived
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge - Cierre de Etapa 4]]"
related:
  - "[[AGENTS OS]]"
aliases:
  - how-owner-validates-gates
  - rjara-validation-method
confidence: observed
source_session: 2026-07-25-fix-pack-g2-review
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/internal-memory
  - scope/agent
  - project/echo-forge
---

# Echo Forge — modelo del owner para validación de gates

Para el próximo agente que cierre un handoff de gate (G0..G6) en este proyecto: cómo trabaja el owner cuando revisa.

## Lo que el owner verifica

- **Validación independiente, no por fe**. Correr comandos por su cuenta y cotejar contra los claims del handoff. Si un claim es "16/16 OK" pero `sha256sum -c` falla con 1 FAILED, eso es un blocker.
- **Tabla con dos columnas mínimas**: `Blocker | Evidencia local`. Si el veredicto incluye `¿Cerrado?` después del pase de fix, usa exactamente la misma tabla. La consistencia ayuda.
- **Atomicidad de artefactos**: cualquier `_SUCCESS`/`completed.json` con datos placeholder (e.g. `compressed_bytes=0`) que se reescribe después es un bug estructural, no cosmético.
- **OD-N contradichas por código**: el owner lee `grep -nE "..."` para verificar imports. Si OD dice "no importa Directions" pero el código lo importa, eso es blocker.
- **DoD incompleto**: si un ítem dice ✅ sin evidencia reproducible (comando + resultado), eso es blocker o non-blocker según el ítem.

## Lo que NO espera el owner

- Que el implementador se autocelebre ("todo perfecto"). Quiere números exactos: `5/5 PASS`, `exit=0`, `39/39 OK`, no "todo verde".
- Reescritura de historia. Una vez commiteado, **no** se reescribe; se hace commit de fix encima.
- Que el implementador cubra smoke contra infra externa (SQX Build 142 real, databanks de producción). Eso es defer firmado con trigger para re-validar.
- Que el implementador sea tímido con la fricción. El owner prefiere un feedback breve y honesto que un reporte pulido.

## Patrones observados en este pase

- El owner usa `git show --stat` para confirmar que el pase fue atómico (no reescritura, no mezcla de refactors).
- Tabla de blockers se cruza con tabla de DoD del handoff; si un DoD dice ✅ pero el blocker dice "DoD incompleto", el implementador debe corregir.
- El veredicto suele venir con "salvedades explícitas" (e.g. "no pude re-ejecutar el go test por proxy 403"). Esas salvedades NO invalidan el cierre si el código está en su sitio.

## Cómo responder

- No promovas el gate tú mismo. Status sigue `review`. La promoción es del owner.
- Si tienes un blocker que NO puedes cerrar (e.g. requiere infra externa), defir firmado en el handoff con trigger para re-validar.
- Numeros exactos, no superlativos.
- Tabla `¿Cerrado? | Evidencia local` con comandos literales y outputs literales.

## Señales de atención

- Si el owner reporta un blocker y tú lo "cierras" con un cambio que no toca el código que el blocker describió: ese cierre no es válido.
- Si el veredicto dice "DoD incompleto" y tú agregas un script de verificación sin ejecutarlo: ese cierre no es válido.
- Si el SHA-256 maestro cambia entre la primera regeneración y la final: documenta el motivo o el owner lo marcará como non-blocker.