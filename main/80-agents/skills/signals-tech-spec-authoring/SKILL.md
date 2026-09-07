---
type: skill
schema_version: 1
name: signals-tech-spec-authoring
scope: project
description: Escribir, estructurar, corregir o revisar specs TÉCNICAS (type=technical) del equipo Signals/Ads en Spellbook (proyecto SIG) y, en general, cualquier design doc de backend RIO/Meli. Usar al redactar la técnica que deriva de un funcional — rio-playmaker, rio-sdk-events, rio-controlplane-*, ads-signals-* — o cuando el usuario nombre una spec SIG-#### técnica y pida escribirla, arreglarla, acortarla o revisarla. Cubre qué definiciones entran y desde qué perspectiva, la forma real del equipo (DD-N, diagrama con marcadores de cambio, Files Changed), la calibración de largo y la regla de atemporalidad. Para el FUNCIONAL usar signals-func-spec-authoring.
created: 2026-08-24
updated: 2026-08-24
entities:
  - "[[Onboarding Signals]]"
related:
  - "[[signals-func-spec-authoring]]"
aliases:
  - spec tecnica signals
  - spec técnica SIG
  - technical spec signals
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/authoring
  - project/signals
---

# signals-tech-spec-authoring — Specs técnicas del equipo Signals (SIG)

Hermana de `signals-func-spec-authoring`, que dueña el **funcional**. Ésta dueña la **técnica**: qué se construye, dónde, y por qué así.

Derivada de las 33 specs técnicas reales del proyecto SIG (fecaputo, vmilesi, frsalazar, wvenera, dochoa, eolopes, dilimaa, jupereira). No es un template inventado: es lo que el equipo efectivamente escribe.

---

## 0. La regla que manda sobre todas las demás

**Una spec describe un estado objetivo, no su propia historia de edición.** El documento se lee como si el diseño hubiera sido siempre así. No tiene memoria de sí mismo.

Cuando te pidan cambiar algo de A a B, el entregable es una spec donde B es la única respuesta que existió jamás: **A desaparece por completo**, incluidas las decisiones, las alternativas descartadas y cualquier nota. Nada de "ya no es A", "se cambió porque", "antes decía", "a pedido del owner". El historial ya lo tiene Spellbook (`spellbook specs versions`); duplicarlo adentro del documento no agrega trazabilidad, agrega ruido.

Regla completa, con la distinción entre *alternativa descartada* (legítima, va) y *versión anterior del documento* (ruido, se borra): [`../signals-func-spec-authoring/references/que-es-una-spec.md`](../signals-func-spec-authoring/references/que-es-una-spec.md). **Léela antes de tocar una spec existente.**

---

## 1. Qué es una spec técnica

Es el diseño ejecutable de un funcional ya escrito. Responde tres preguntas y nada más:

1. **¿Qué se construye y dónde?** — clases, contratos, endpoints, queries, archivos, por repo.
2. **¿Por qué así y no de la forma obvia?** — las decisiones que un reviewer podría discutir, con la alternativa que cerraron.
3. **¿Qué queda afuera?** — el límite del cambio.

**Prueba ácida:** un dev que no participó del diseño lo implementa sin volver a preguntar, y un reviewer puede estar en desacuerdo **con una decisión puntual, citándola por su id**. Si el reviewer solo puede decir "no me convence en general", la spec no decidió nada: describió código.

**Funcional vs técnica.** El funcional dice *qué tiene que ser verdad* y **es el dueño de `RF-N` / `CA-N` / `E2E-N`**. La técnica los **referencia**, nunca los redefine ni los repite. Si estás reescribiendo requisitos, estás escribiendo el funcional otra vez.

---

## 2. Qué definiciones entran, y desde qué perspectiva

La perspectiva es **la del dev que va a implementar y la del reviewer que va a aprobarlo**. No la del autor, no la del proceso, no la de la conversación que originó el documento.

### Entra

- **Lo que cambia, nombrado con el nombre real del código**: clases, métodos, tablas, columnas, topics, endpoints, claves de configuración. `MetricsTickPublisher`, `component_relations`, `POST /events/metrics/tick`, `rio.context.outputs.enabled`.
- **Los contratos, pegados, no descritos**: el JSON que sale al wire, el DTO, el `SHOW CREATE TABLE`, la migración SQL, la firma del record. Un contrato en prosa obliga a adivinar el tipo.
- **Las decisiones discutibles (`DD-N`)**: las que tienen más de una respuesta razonable.
- **El estado actual, solo donde condiciona el diseño**: si el índice es non-unique, si el listener corre post-commit, si la columna es nullable. Un hecho del código que no cambia una decisión sobra.
- **Lo que NO cambia**, cuando puede haber duda. El equipo lo marca explícito (`[UNCHANGED]`, "Lo que NO cambia", "Componentes existentes — sin cambios"), y evita el diff imaginario.
- **El límite**: fuera de alcance, y las preguntas abiertas que todavía no tienen dueño.

### No entra

- **Nada sobre el documento**: cómo se escribió, qué versión reemplaza, qué se corrigió, quién lo pidió, si fue verificado. (§0)
- **Los `RF-N`/`CA-N` copiados del funcional.** Se referencian.
- **La clase entera pegada.** Va el fragmento que la prosa no puede decir con precisión: una query JPQL, la firma de un record, el `catch` que no puede lanzar.
- **Un `DD-N` que no cierra ninguna alternativa.** Si no hay una segunda opción razonable, no es una decisión: es una descripción. Bajala a prosa y liberá el número.
- **Una pregunta sin responder disfrazada de decisión cerrada.** Si no está decidido, va a preguntas abiertas.
- **Baselines que caducan sin avisar** (conteos de tests, listas de servicios, "los seis CP"). Escribí el predicado —"todo consumidor del topic"— y anclá los números al commit que los produjo.

---

## 3. Calibración de largo — la falla más común

Mediana real de una técnica del equipo: **~10k caracteres**. De 23 specs técnicas con contenido, **18 están por debajo de 16k**. Las cinco que pasan de 30k son plataforma multi-repo o multi-fase (SIG-342 GCP Flink, SIG-564 SDK Python, SIG-368 refactor de transporte, SIG-576 y SIG-137).

**Un feature de un repo, o dos, se escribe en 6k–15k.** Si vas por 40k para un feature, no tenés rigor: tenés un chorizo, y un chorizo no se revisa — se aprueba sin leer, que es lo mismo que no tener spec.

Qué lo infla, en orden de frecuencia:

- Repetir en prosa lo que ya dice el diagrama o la tabla.
- Justificar decisiones obvias con un `DD-N` cada una.
- Volcar el inventario del código existente en vez de los hechos que condicionan el diseño.
- Explicar el mismo riesgo en tres secciones (decisión, seguridad, riesgos).
- Contar la historia del documento (§0).

Al iterar una spec larga: **condensá, no agregues.** Que quede más corta y más clara que antes.

---

## 4. La forma del equipo

### Frontmatter en negritas, no YAML

```
# Technical Specification — <título>            (o "Spec Técnica: <título>")

**Feature**: <slug o id>
**Owner**: <nombre>
**Project**: Signals (<repo principal>)
**Status**: DRAFT | Pending approval | ready_to_code
**Deriva de**: SIG-N — <título del funcional>
```

### Diagrama ASCII con marcadores de cambio — el patrón más distintivo

El equipo no describe la arquitectura en prosa: la dibuja, y **anota cada caja con su estado de cambio**. Es lo que hace que se entienda el alcance de un vistazo.

```
  JobController [MODIFIED]
    │ capture requestedAt = Instant.now()
    ├──▶ BigQueue Topic: rio-clickhouse-metrics-tick [NEW]
    └──▶ returns 202 Accepted

  PublishMetricsCommand [UNCHANGED]
```

Usá `[NEW]` / `[MODIFIED]` / `[UNCHANGED]` (o `NUEVO` / `MODIFICADO` / `SIN CAMBIOS`). **Lo que está en el diagrama no se re-narra en prosa.**

### Decisiones: `DD-N`

Dos formas válidas según el peso de la decisión. **`DD-N`, no `DT-N`** — es el identificador del equipo.

Forma corta (vmilesi, SIG-576) — la default:

```
### DD-1: BigQueue HTTP push en vez de consumer del SDK

**Decisión**: Usar la subscription HTTP push de BigQueue en vez de implementar un consumer `mqclient`.

**Fundamentación**: Es el patrón ya establecido en este codebase — `ActionTriggerController` ya lo usa. Deja retry y DLQ configurados fuera de la aplicación, a nivel de topic, y no agrega dependencias nuevas.
```

Forma larga (fecaputo, SIG-342) — para decisiones estructurales:

```
### DD-1: Strategy Pattern para extensión multi-cloud

**Contexto**: … el estado actual relevante, en dos líneas.
**Problema**: ¿Cómo …?
**Decisión**: …
**Consecuencias**: … (bullets)
**Alternativas descartadas**: … (bullets, cada una con por qué se cae)
```

Cuando hay varias decisiones estructurales, arriba va una **tabla resumen**: `| Decisión | Elección | Alternativa descartada |`. Para comparar opciones con detalle, la tabla `| Alternativa | Pros | Contras | Decisión |` con `✅ Elegida` / `❌` (wvenera, SIG-231).

### Anclaje al código: nombres reales, líneas solo para señalar un defecto

El equipo cita **clases, métodos, tablas y endpoints por su nombre real**. `archivo.java:97-126` se usa cuando estás **señalando un bug o un comportamiento puntual** que el lector tiene que ir a ver (SIG-218). No conviertas la spec en un índice de números de línea: caducan al primer merge y no es lo que el equipo hace.

Cuando el diseño depende de un hecho no obvio del código o de la base, **mostralo**: el `SHOW CREATE TABLE`, el bloque de configuración, la firma actual. Mostrarlo vale más que afirmarlo.

### Archivos afectados

Tabla al final del bloque de implementación, separando nuevos de modificados:

```
### Archivos nuevos
| Archivo | Propósito |
### Archivos modificados
| Archivo | Cambio |
```

### Idioma

Español o inglés, **consistente dentro del documento**. El equipo usa los dos (fecaputo y wvenera en inglés; eolopes, dilimaa y frsalazar en español/portugués). Nombres de clases, endpoints, topics, métricas y claves de configuración **siempre en el idioma del código**.

---

## 5. Esqueleto

Checklist de qué cubrir, no template para pegar. Ninguna sección va por ritual: va la que cambia una decisión de implementación. Un fix chico son cuatro secciones (SIG-333, SIG-526: Contexto → Problema → Solución → Archivos a modificar → Verificación) y está bien así.

```
## Contexto / Overview          por qué existe esto, anclado al estado actual (1-3 párrafos)
## Arquitectura                 diagrama con marcadores de cambio
## Contrato                     payload/DTO/schema/migración reales
## Cambios por repo o por capa  qué se toca, con nombres reales
## Design Decisions             DD-N
## Archivos afectados           nuevos / modificados
## Manejo de errores            tabla escenario → comportamiento
## Observabilidad               métricas y logs, con tags de cardinalidad acotada
## Estrategia de tests          qué cubre cada nivel, mapeado a los CA-N del funcional
## Seguridad                    solo si hay superficie: authz, datos sensibles, límites
## Plan de rollout / migración   pasos, y rollback si toca infra o datos
## Fuera de alcance
## Preguntas abiertas
```

**Cobertura del funcional.** Si mapeás contra `RF-N`/`CA-N`, que sea verdad de **lo que se despliega**, no del código escrito. Un requisito que queda inerte detrás de un flag apagado se dice arriba, con su id, no en un pie de página.

**Enmiendas al funcional.** Si el diseño demuestra que el funcional dice algo falso, va en sección propia y **con el texto de reemplazo redactado**. Un reemplazo se aprueba en una reunión; una descripción del problema genera otra ronda.

---

## 6. Ejemplos vivos — leé uno antes de escribir

Nunca partas de un template. Abrí la spec real más parecida y espejá su forma y su profundidad.

| Necesitás | Leé | Por qué |
|---|---|---|
| Fix acotado, 1 repo | **SIG-333**, **SIG-526** | Contexto → Problema → Solución → Archivos → Verificación. 4-7k |
| Feature de 1 repo con contrato nuevo | **SIG-576** (parte técnica) | Diagrama con marcadores, `DD-N` corto, Files Changed. El molde default |
| Cambio de schema / constraint de base | **SIG-231** | Estado actual real, tabla de alternativas con ✅/❌, rollout manual y rollback |
| Feature multi-repo | **SIG-234** | Cambios por repo, cómo agregar el próximo tipo, migración |
| Plataforma multi-fase, multi-cloud | **SIG-342** | `DD-N` largo, fases con estado de implementación, cobertura de US |
| Adopción de un contrato en un CP | **SIG-259** | Contexto → gap → state machine → config por ambiente → checklist |
| Deuda técnica | **SIG-416** | `DEBT-N` con impacto y tabla de prioridad. 2.7k y alcanza |

---

## 7. Checklist pre-review

- [ ] **Regla del lector cero**: ni una frase que solo se entienda conociendo una versión anterior. Corré el `grep` de [`que-es-una-spec.md`](../signals-func-spec-authoring/references/que-es-una-spec.md).
- [ ] Largo dentro de la calibración de §3, o justificado por ser multi-repo/multi-fase.
- [ ] Diagrama con marcadores de cambio, y **nada del diagrama re-narrado** en prosa.
- [ ] Cada `DD-N` cierra una alternativa que un reviewer propondría. Los que no, bajaron a prosa.
- [ ] Ninguna fundamentación es una atribución ("lo pidió X"); todas son técnicas.
- [ ] Contratos pegados (payload, DTO, SQL), no descritos.
- [ ] Nombres reales del código. Números de línea solo donde señalan un defecto concreto.
- [ ] Tabla de archivos nuevos vs modificados.
- [ ] `RF-N`/`CA-N` referenciados, nunca redefinidos; cobertura verdadera de lo que se despliega.
- [ ] Fuera de alcance explícito. Rollback si toca infra o datos.
- [ ] Preguntas abiertas separadas de decisiones cerradas.
- [ ] Sin baselines que caduquen sin aviso; predicados en vez de enumeraciones.
- [ ] Sin hard-wraps: cada párrafo y bullet en una sola línea continua.

---

## 8. Publicar

Mecánica compartida con el funcional: [`../signals-func-spec-authoring/references/spellbook-access-runbook.md`](../signals-func-spec-authoring/references/spellbook-access-runbook.md).

Lo único propio de la técnica: está llena de backticks y el CLI **rechaza backticks en cualquier argumento**, así que el contenido se publica por **PUT** a `{baseUrl}/api/cli-api/specs/{id}` con `Authorization: Bearer`. **Verificá releyendo el contenido remoto, no el HTTP 200**: si el script que arma el body falla, `curl` publica el body anterior y devuelve 200 igual.

---

## Hard Rules

- El documento no habla de sí mismo. Nunca. (§0)
- `DD-N` para decisiones, no `DT-N`. `RF-N`/`CA-N`/`E2E-N` son del funcional y solo se referencian.
- Ningún `DD-N` sin alternativa cerrada; ninguna fundamentación que sea una atribución.
- Leé una spec viva de §6 antes de escribir; no copies un template.
- Condensar, nunca inflar: si la iteración la dejó más larga, revisá §3.
