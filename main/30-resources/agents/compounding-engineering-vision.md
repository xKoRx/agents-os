---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[technical-project-manager]]"
  - "[[sdd-workflow]]"
  - "[[sdd-developer]]"
  - "[[e2e-gated-validation]]"
  - "[[agents-os-hygiene-cycle]]"
  - "[[agents-os-kaizen-memory]]"
aliases:
  - AGENTS OS Engineering Vision
  - Compounding Engineering
  - Compounding Delivery Vision
  - visión de ingeniería de Agents OS
tags:
  - kind/doc
  - tech/agents-os
  - tech/sdd
  - action/engineering
  - action/continuous-improvement
created: "2026-09-23"
updated: "2026-09-23"
---

# AGENTS OS — Compounding Engineering Vision

## Propósito

Definir la visión de ingeniería que guía cómo AGENTS OS debe transformar trabajo técnico asistido por agentes en **progreso acumulativo, verificable y reutilizable**.

La meta no es producir más código por unidad de tiempo. La meta es construir un sistema donde cada iteración exitosa deje cuatro activos:

1. **producto mejorado**;
2. **evidencia ejecutable de que funciona**;
3. **tooling y tests que reducen riesgo futuro**;
4. **conocimiento operacional que evita que agentes futuros redescubran lo mismo**.

El resultado buscado es un sistema que compone conocimiento y capacidad con el tiempo.

> Cada iteración debe dejar el sistema más avanzado, más probado y más fácil de continuar que antes.

---

## Contenido

## 1. Visión

AGENTS OS debe comportarse como una organización de ingeniería capaz de entregar software mediante agentes autónomos sin convertir autonomía en improvisación.

La unidad de progreso no es:

- horas consumidas;
- número de archivos modificados;
- cantidad de prompts;
- cantidad de agentes;
- porcentaje subjetivo de avance.

La unidad de progreso es un **resultado observable y certificado**.

Un proyecto puede planificarse para varios días, pero cada día debe terminar idealmente con una capacidad que:

- tenga un objetivo concreto;
- pueda probarse dentro del mismo día;
- tenga un gate explícito;
- produzca un commit o baseline exacto;
- sea utilizable como base segura del siguiente paso;
- pueda promoverse a un entorno real cuando el riesgo y las dependencias lo permitan.

El roadmap largo expresa intención. El contrato operativo se congela **just-in-time**, al comenzar la iteración que realmente se ejecutará.

---

## 2. El efecto acumulativo

Una sesión de agentes no debería terminar sólo con código nuevo.

Debe alimentar un flywheel:

```text
                  ┌────────────────────┐
                  │   SPEC / objetivo  │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │     implementar    │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ intentar romperlo  │
                  │   independientemente│
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ corregir + certificar│
                  └─────────┬──────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
    executable knowledge           agent/process knowledge
 tests · E2E · harnesses           agent-run · feedback
 fixtures · toolkit                reusable candidates
             │                             │
             │                             ▼
             │                      Hygiene / Kaizen
             │                             │
             │                 skill · runbook · pattern
             │                 known-error · tooling
             │                             │
             └──────────────┬──────────────┘
                            ▼
                    siguiente iteración
                  redescubre menos cosas
```

El éxito acumulativo se manifiesta cuando una iteración futura:

- necesita menos discovery;
- reutiliza herramientas ya validadas;
- hereda invariantes ejecutables;
- encuentra defectos antes;
- formula prompts más precisos;
- puede dedicar más tiempo a capacidad nueva y menos a reconstruir contexto perdido.

---

## 3. Entrega diaria atómica

Una jornada técnica debe definirse por un **hito verificable**, no por una lista abierta de tareas.

Un buen hito diario es:

- observable;
- acotado;
- probado objetivamente;
- razonablemente reversible;
- suficientemente independiente para constituir nueva baseline;
- pequeño para dejar tiempo real de verificación y corrección;
- idealmente promovible sin depender de código incompleto del día siguiente.

Ejemplo débil:

> avanzar la ingesta de historia.

Ejemplo fuerte:

> una StrategyVersion acepta un snapshot TRAINING + PRE_REAL válido, lo persiste de forma atómica, lo expone por GET y un replay idéntico resulta UNCHANGED.

Si el hito no cabe junto con su verificación y corrección en la ventana disponible, el hito está mal dimensionado y debe dividirse **antes** de comenzar a desarrollar.

---

## 4. El ciclo de tres shots

Cuando una iteración SDD está lista para implementación, AGENTS OS favorece tres contextos de trabajo separados.

### Shot 1 — IMPLEMENT

Un agente senior recibe un mandato one-shot completo y construye la capacidad.

Debe:

- trabajar contra decisiones congeladas;
- resolver autónomamente obstáculos técnicos normales;
- crear tests normales de unidad/integración;
- entregar un commit candidato;
- registrar evidencia;
- no autoaceptar el resultado final.

Su output es una **implementation candidate**, no un PASS definitivo.

### Shot 2 — VERIFY adversarially

Un contexto fresco inspecciona el commit candidato sin confiar en Shot 1.

Su misión no es confirmar que todo parece correcto. Es intentar falsificar el gate.

Debe buscar, cuando aplique:

- inputs inválidos;
- límites y precisión;
- concurrencia;
- atomicidad;
- idempotencia;
- rollback;
- timestamps;
- autenticación y tenancy;
- clasificación de errores;
- persistencia;
- side effects;
- compatibilidad;
- regresiones respecto del baseline.

Cuando una propiedad crítica deriva de un algoritmo del producto, la prueba independiente debe evitar la tautología. Si se verifica un digest, una transformación o un cálculo, el verifier debe preferir una implementación independiente de la receta cuando reutilizar el mismo helper productivo haría trivial la comparación.

Shot 2 **no corrige product code**. Produce findings reproducibles y evidencia independiente.

### Shot 3 — CORRECT + FINAL GATE

Un tercer contexto:

- corrige los findings aceptados;
- no reabre decisiones congeladas;
- convierte reproducers valiosos en regresiones permanentes;
- vuelve a correr el gate completo;
- revisa el diff final;
- entrega el commit certificado.

No se planifica un Shot 4 para defectos técnicos ordinarios. Shot 3 debe corregir y revalidar dentro de su propia ejecución. Sólo una contradicción real que requiera decisión humana rompe el ciclo.

---

## 5. SDD como sistema de autoridad

La separación SDD se conserva:

```text
SPECIFY → PLAN → TASKS → IMPLEMENT → VERIFY
```

La SPEC define **qué debe ser verdad**.

El PLAN define **cómo impactar el sistema sin improvisar arquitectura**.

TASKS define **slices ejecutables y sus gates**.

La implementación produce código.

La verificación determina si el resultado satisface realmente la SPEC.

Cuando SPEC/PLAN/TASKS están ready, `sdd-developer` puede ejecutar el ciclo:

```text
Shot 1 IMPLEMENT
      ↓
Shot 2 VERIFY adversarial
      ↓
Shot 3 CORRECT + FINAL GATE
      ↓
certified commit
```

Si durante implementación aparece una pregunta de producto o arquitectura que no estaba resuelta, no se debe ocultar inventando comportamiento en código. El gap retorna al artefacto SDD que posee esa decisión.

---

## 6. Cada SPEC posee su verificación

Cada SPEC debe poder responder:

> ¿qué evidencia ejecutable demuestra que cada acceptance criterion sigue siendo cierto?

La propiedad es lógica, no necesariamente física.

`VERIFICATION.md` actúa como mapa:

```text
AC / invariant
  → executable test path
  → scenario/test name
  → evidence/status
```

Ejemplo:

```text
AC-03 — replay idéntico no produce writes
→ v3/e2e/specs/FEAT-HISTORY-INGESTION/replay_test.go
→ TestReplayUnchanged
→ PASS @ <commit>
```

La SPEC posee el contrato de comportamiento; el código de test vive donde corresponde técnicamente.

---

## 7. No todo test es E2E

“E2E” describe un boundary de comportamiento, no una carpeta donde guardar tests importantes.

Placement esperado:

- invariante local de paquete → `*_test.go` junto al owner;
- persistencia/HTTP/component integration → paquete de integración owner;
- comportamiento estable cross-component → módulo E2E canónico;
- helpers reutilizables, launchers, validadores, seeders → toolkit/test-support owner;
- evidencia temporal para reproducir un defecto → puede permanecer como reproducer sólo si conserva valor de auditoría.

Cuando un repositorio adopta ownership por SPEC, los E2E cross-component pueden agruparse como:

```text
<e2e-root>/specs/<SPEC-ID>/
```

Esto permite localizar pruebas por comportamiento sin esconder código ejecutable dentro de carpetas documentales.

---

## 8. El trabajo del verifier no se pierde

Todo artifact de verificación nuevo se clasifica:

- `PERMANENT_REGRESSION`
- `E2E_CANDIDATE`
- `HARNESS_TOOLKIT_CANDIDATE`
- `DISPOSABLE_REPRODUCER`

Una prueba independiente que encontró un defecto real tiene presunción fuerte de valor futuro.

Shot 3 debe normalmente convertirla en un asset permanente, salvo razón concreta para rechazarla.

El objetivo es que una futura migración, refactor o reimplementación pueda ejecutar nuevamente las invariantes importantes sin tener que reconstruir la estrategia de verificación.

---

## 9. Dos tipos de conocimiento reusable

AGENTS OS separa deliberadamente dos clases de aprendizaje.

### Conocimiento del producto

Pregunta:

> ¿qué debe seguir siendo verdad en el software?

Se preserva como:

- tests;
- E2E;
- fixtures;
- harnesses;
- simuladores;
- toolkit;
- validadores ejecutables.

Ejemplo:

> un replacement que falla después del DELETE debe conservar intacta la historia anterior.

Eso pertenece a un test ejecutable, no a una skill.

### Conocimiento del agente/proceso

Pregunta:

> ¿cómo debería trabajar un agente futuro para resolver mejor esta clase de problema?

Se preserva como candidatos de:

- skill;
- runbook;
- pattern;
- known error;
- tooling;
- test harness methodology.

Ejemplo:

> para verificar digests, el verifier debe implementar independientemente la receta en vez de usar el helper productivo bajo prueba.

Eso puede convertirse en patrón o skill reusable.

Las dos clases no se sustituyen mutuamente.

---

## 10. Aprender sin contaminar Agents OS

No toda observación útil merece una skill.

Crear reglas compartidas inmediatamente después de una sola sesión produciría:

- skills duplicadas;
- reglas demasiado específicas;
- contradicciones;
- ruido de retrieval;
- comportamiento basado en anécdotas.

Por eso cada one-shot debe **evaluar** mejoras, pero no necesariamente promoverlas.

El loop es:

```text
one-shot
  ↓
agent_run + feedback concreto
  ↓
Hygiene / Kaizen
  ↓
evidencia repetida / blocker fuerte / forward-test convincente
  ↓
skill | runbook | pattern | known_error | tooling
```

`NONE` es un resultado válido para una sesión sin aprendizaje reusable.

La mejora continua requiere filtro, no volumen.

---

## 11. Contrato de Prompt Maestro

Todo Prompt Maestro despachado por el manager o por el desarrollador SDD usa secciones semánticas explícitas:

```text
/goal
/authorities
/baseline
/frozen
/scope
/execute
/verify
/reuse
/improve
/close
```

No son comandos específicos de una herramienta; son el contrato mental del one-shot.

### /goal

Define únicamente el estado observable que debe existir al terminar.

No debe contaminarse con objetivos meta de aprendizaje.

Ejemplo:

```text
/goal

Una StrategyVersion real puede importar TRAINING + PRE_REAL,
persistirlo de forma atómica y leerlo nuevamente por el contrato Echo.

PASS exige...
```

### /reuse

Pregunta qué activos técnicos generó la sesión y dónde deben vivir.

### /improve

Pregunta qué comportamiento repetible podría evitar rediscovery futuro.

Puede responder:

```text
REUSABLE_BEHAVIOR_CANDIDATES: NONE
```

La evaluación es obligatoria. La generación artificial de feedback está prohibida.

### /close

Exige persistencia, agent-run, feedback cuando corresponda, evidencia y continuidad suficiente para que otro contexto pueda retomar sin reconstruir la sesión.

---

## 12. One-shot significa autonomía con límites

Un shot no debe depender de una conversación interactiva de micro-prompts.

El mandato debe incluir:

- objetivo;
- autoridades;
- baseline exacto;
- decisiones congeladas;
- scope y non-goals;
- libertad técnica;
- blocker policy;
- verificación requerida;
- reuse harvest;
- mejora de sesión;
- closeout.

Un agente senior resuelve obstáculos técnicos ordinarios dentro del shot.

Sólo retorna al owner cuando:

- falta una decisión de producto;
- existe contradicción material entre autoridades;
- una acción externa no autorizada es necesaria;
- continuar exigiría romper un frozen decision.

La autonomía reduce overhead sólo cuando los límites están explícitos.

---

## 13. Capability PASS no es Production PASS

Los estados no se colapsan.

Una capacidad puede estar:

```text
implemented
→ verified
→ merged
→ released
→ deployed
→ physically validated
```

Cada transición requiere evidencia distinta.

`DAY_PASS` o `SDD_DELIVERY_PASS` significa que existe un commit certificado dentro del gate definido.

No implica automáticamente:

- merge a master;
- migration aplicada;
- runtime actualizado;
- datos reales;
- integración externa;
- PROD.

Cuando corresponda, el flujo continúa por:

```text
release-certification
→ deployment-proof
→ e2e-gated-validation
```

---

## 14. El baseline certificado es un activo

Cada iteración que pasa el gate produce una nueva referencia exacta.

La siguiente iteración debe comenzar desde ese baseline certificado o desde una reconciliación explícitamente revalidada.

No se debe continuar desde:

- una branch anterior;
- un commit “parecido”;
- el resultado de Shot 1 cuando Shot 2/3 produjeron una corrección posterior;
- un master que avanzó sin reconciliar.

El commit certificado convierte el progreso del día en un punto de continuidad reproducible.

---

## 15. Principios de diseño

### Outcome over activity

Medir capacidades terminadas, no movimiento.

### Independent verification over self-confirmation

El autor no es el único juez de su implementación.

### Evidence over narrative

Un PASS debe poder reproducirse.

### Atomic progress over long-lived partial work

Preferir slices que cierren completamente y produzcan una baseline nueva.

### Executable knowledge over rediscovery

Cuando una propiedad del producto es estable, expresarla en tests.

### Curated learning over skill proliferation

Capturar candidatos ampliamente; promover reglas compartidas selectivamente.

### Fresh context over inherited assumptions

La verificación independiente debe partir de autoridades y evidencia, no del razonamiento del implementador.

### Just-in-time design over speculative detail

Planificar el horizonte, pero diseñar en detalle sólo la iteración activa.

### Production readiness as a continuum

No confundir source correctness con runtime evidence.

### Compounding as the north star

Cada iteración debería hacer más poderosa la siguiente.

---

## 16. Cómo reconocer que funciona

AGENTS OS está cumpliendo esta visión si, con el tiempo:

- baja el porcentaje de sesiones dedicado a redescubrir setup y contratos;
- aumenta la cobertura de invariantes reales, no sólo coverage numérico;
- bugs encontrados por verificadores independientes se convierten en regresiones permanentes;
- migraciones pueden apoyarse en suites de comportamiento existentes;
- los prompts maestros son más breves porque skills/runbooks ya cargan métodos probados;
- los agentes preguntan menos por decisiones ya resueltas;
- los proyectos terminan hitos diarios con commits certificados;
- el número de skills crece más lento que el valor reusable que representan;
- la evidencia para promover a producción se vuelve rutinaria y reproducible.

La métrica cualitativa más importante es:

> **La siguiente iteración parte desde un sistema más capaz de construir y probar que la iteración anterior.**

---

## 17. Anti-patrones

Esta visión se degrada cuando:

- Shot 1 se autoacepta;
- Shot 2 sólo vuelve a ejecutar los mismos tests;
- los reproducers de un bug real mueren en una branch temporal;
- todo test grande se llama E2E;
- cada feedback crea una skill;
- la SPEC documenta aceptación sin apuntar a evidencia ejecutable;
- se usa “90% listo” como sustituto de un gate;
- una iteración consume todo el tiempo implementando y deja verificación para “mañana”;
- se continúa desde un commit no certificado;
- una dependencia externa bloquea innecesariamente una capacidad interna;
- un PASS de código se comunica como PASS de producción.

---

## 18. Declaración de misión

AGENTS OS existe para convertir agentes autónomos en una **capacidad de ingeniería acumulativa**.

No buscamos sesiones brillantes aisladas.

Buscamos un sistema donde:

- los objetivos se cierran;
- los resultados se prueban;
- los errores fortalecen la suite;
- los métodos útiles se destilan;
- los agentes futuros heredan evidencia y comportamiento probado;
- cada día deja una base más sólida que el anterior.

La dirección es simple:

```text
build
→ break
→ fix
→ certify
→ preserve
→ learn
→ compound
```

## Fuentes

Síntesis interna de:
- [[technical-project-manager]]
- [[sdd-workflow]]
- [[sdd-developer]]
- [[e2e-gated-validation]]
- [[agents-os-hygiene-cycle]]
- [[agents-os-kaizen-memory]]

La visión fue formalizada a partir del ciclo de entrega y verificación de The Lab D1 del 23 de septiembre de 2026, donde implementación, verificación adversarial y corrección final produjeron un baseline certificado y nuevas prácticas reutilizables.
