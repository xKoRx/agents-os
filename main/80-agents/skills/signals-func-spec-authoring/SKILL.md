---
type: skill
schema_version: 1
name: signals-func-spec-authoring
scope: project
description: >-
  Escribir, estructurar o revisar specs FUNCIONALES del equipo Signals/Ads en
  Spellbook (proyecto SIG). Usar al redactar o planificar un "spec funcional" de
  Signals — epic, feature, fix chico o bug/incidente — o al tocar apps
  ads-signals-* (catalog, collector, sdk-go/node/java) o RIO/playmaker/
  control-plane. Cubre qué es un funcional, epic vs spec, los esqueletos de
  secciones, las convenciones del equipo (US-N / RF-N / CA-N / E2E-N) y la regla
  de atemporalidad. La creación del spec se hace con Grimoire (/grimoire.arcanist).
  Para la spec TÉCNICA usar signals-tech-spec-authoring. La mecánica de Spellbook
  (listar, leer, crear, editar, el gotcha de backticks) vive en
  references/spellbook-access-runbook.md.
created: 2026-08-12
updated: 2026-08-24
entities:
  - "[[Onboarding Signals]]"
related:
  - "[[signals-tech-spec-authoring]]"
aliases:
  - spec funcional signals
  - escribir spec SIG
  - spellbook SIG spec
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/authoring
  - project/signals
---

# Authoring Functional Specs for Signals (Spellbook / SIG)

This skill encodes how the **Signals/Ads** team writes functional specs in Spellbook (project `SIG`), so you don't rediscover the conventions each session. Scope: the **content and shape** of a good functional spec — the judgment of *what to write*. The mechanical *how to reach and publish* a spec (CLI commands, the backtick gotcha) is a runbook: [`references/spellbook-access-runbook.md`](references/spellbook-access-runbook.md).

---

## 0. Dos reglas antes de escribir una sola línea

**A — El documento no habla de sí mismo.** Una spec describe un estado objetivo, no su propia historia de edición. Se lee como si el diseño hubiera sido siempre así. Cuando te pidan cambiar algo de A a B, el entregable es una spec donde B es la única respuesta que existió jamás: **A desaparece por completo**, incluidas decisiones, alternativas y notas al pie. Nada de "ya no es A", "se cambió porque", "antes decía", "a pedido del owner". El historial ya lo tiene Spellbook (`spellbook specs versions`). Regla completa, y la distinción entre *alternativa descartada* (legítima) y *versión anterior del documento* (ruido): [`references/que-es-una-spec.md`](references/que-es-una-spec.md) — **léela antes de tocar una spec existente.**

**B — El funcional se crea con Grimoire.** El camino es `/grimoire.arcanist`: brainstorm socrático, diagramas, y el gate de aprobación antes de publicar. No arranques a redactar a mano ni improvises el flujo. Esta skill dice **qué tiene que decir** el documento y cómo se ve un buen funcional del equipo; Grimoire es **cómo se produce y se publica**. Si el usuario ya viene con un funcional escrito y pide corregirlo, no hace falta rehacer el flujo de Grimoire: aplicá la regla A y las convenciones de acá.

---

## ¿Qué es un spec funcional? (definición)

Un **spec funcional** define, **desde afuera**, **QUÉ** tiene que pasar y **POR QUÉ** — nunca el **CÓMO** (el cómo es el spec técnico). Es un **contrato con el equipo**, no un diseño de implementación.

Responde tres preguntas, y nada más:

1. **¿Qué problema resuelve?** — con el *root cause* nombrado, no un síntoma vago.
2. **¿Qué tiene que ser verdad cuando esté listo?** — requisitos (`RF-N`) y criterios de aceptación (`CA-N`) **verificables**.
3. **¿Qué queda explícitamente fuera?** — la sección de alcance es la que evita el scope creep.

**Prueba ácida:** un buen spec funcional le alcanza a un reviewer para aprobar y a un dev para estimar **sin leer código**. Si para entenderlo hay que abrir el repo, le falta problema o le sobra implementación.

**Funcional vs técnico:** para escribir la **técnica** hay skill propia: `signals-tech-spec-authoring` (regla de evidencia `archivo:línea` contra un commit base, convenciones `DT-N`/`PT-N`, y los modos de falla). Este skill no la cubre. El funcional dice "el CP debe recibir el I/O tipado del componente"; el técnico dice "se agrega la clase `ContextBuilder` que lee `component_relations` y…". No mezclar: el detalle de implementación va al spec técnico o a un doc referenciado.

### Enfoca en la entidad/capacidad, NO en el primer caso de uso

Un spec que crea una entidad o capacidad nueva es **sobre esa entidad**, no sobre lo primero que se hace con ella. El primer caso de uso es **alcance de la v1** (un milestone), no la tesis del spec. Confundirlos encajona el diseño y hace que el spec envejezca mal cuando llega el segundo caso de uso.

- El **título y el Problema** nombran la **entidad/capacidad** (p.ej. "la entidad Context por componente"), no el detalle (p.ej. "el contrato de I/O").
- El primer caso de uso va en su propia sección (**"Primer caso de uso (v1)"**) o como el primer ítem del alcance — presentado como *lo primero que se implementa sobre la entidad*, no como el propósito.
- Los siguientes casos de uso van a **Fuera de alcance / futuros**, explícitamente "sobre la misma entidad".
- Señal de que lo tienes al revés: el título describe un detalle técnico y la entidad aparece recién a mitad del texto. Dalo vuelta.

---

## Principio rector: conciso, no verboso (regla #1)

Un buen spec **explica el problema y la solución de forma simple, deja un diagrama, y para.** La verbosidad es un defecto, no rigor: un spec largo que nadie termina de leer no sirve. Este principio **manda sobre** cualquier "igualar la profundidad del ejemplo canónico" — usa las secciones canónicas como checklist de *qué cubrir*, no como licencia para inflar el texto.

- **Estructura mínima que sirve:** Problema (con root cause) → Objetivo/Solución (en simple) → **Diagrama** si ayuda → Requisitos/Criterios → **Fuera de Alcance**. Todo lo demás se agrega **solo si aporta**.
- **El diagrama hace el trabajo pesado:** si algo se entiende mejor en un diagrama, va al diagrama y NO se re-narra en prosa.
- **Una idea por bullet, sin relleno.** Prefiere tablas y listas a párrafos largos. Corta adjetivos, repeticiones y contexto que ya vive en un spec/doc linkeado (enlázalo, no lo copies).
- **Longitud según tipo, no según calidad:** los buenos feature specs del equipo son **cortos** (SIG-543 ~5.7k, SIG-448 ~6.3k, SIG-210 ~3.6k chars). La verbosidad (20-24k) se reserva para **epics** arquitectónicos y planes de migración multi-fase — no para un feature.
- **Prueba de humo:** si un bullet no cambia una decisión de build ni un criterio de aceptación, sobra.

Al iterar un spec verboso: **condensa, no agregues** — que quede más corto y más claro que antes.

### No inventes documentos ni referencias fantasma

El spec debe leerse **solo**, sin presuponer contexto que el lector no tiene.

- **Nunca** escribas "reemplaza el borrador verboso", "versión condensada", "la versión anterior decía…" ni notas de proceso. El spec ES el documento, no un changelog de sí mismo. Arranca directo en el Problema.
- **Nunca** cites un documento/sección que no exista o que el lector no pueda abrir. Si citas algo (un spec hermano `SIG-N`, un Grid), tiene que existir y estar linkeado.

### Formato

- **No hard-wrapear la prosa:** cada párrafo y bullet en **una sola línea continua**; el render hace el soft-wrap. Los saltos de línea solo separan bloques (párrafos, ítems, filas de tabla). Excepción: bloques de código, tablas y arte ASCII conservan sus saltos.

---

## Cómo llegar a los specs y publicarlos → runbook

Es mecánico (CLI, no browser — el browser choca con SSO). Está separado a propósito, en [`references/spellbook-access-runbook.md`](references/spellbook-access-runbook.md): listar/leer/crear/editar, el **gotcha de backticks** en `specs edit` y el workaround por API, paginación, y ciclo de review. Cárgalo cuando vayas a tocar Spellbook; no lo repitas acá.

---

## 1. Parte siempre de un ejemplo vivo — nunca de un template copiado

Los templates se pudren; los specs reales son la fuente de verdad. Antes de escribir, **abre el spec canónico que más se parezca y léelo entero**. El mapeo *patrón → spec real* está en [`references/canonical-specs.md`](references/canonical-specs.md). Elige el más cercano y espeja su estructura y profundidad (con el principio de concisión por encima).

---

## 2. Decide el tipo: epic vs spec

Elige la forma desde el trabajo, no al revés.

| Situación | Tipo | Ejemplo real |
|-----------|------|--------------|
| Feature con cara a usuario/CP: nuevo endpoint, comportamiento, contrato | **spec** (US-N/RF-N/CA-N) | SIG-543, SIG-263 |
| Fix acotado o cambio de contrato chico | **spec** chico (root cause + tabla RF-N + CA-N) | SIG-543, SIG-541 |
| Doc de diseño interno / plomería (sin cara a usuario) | **spec** (Problema → Scope → pasos numerados) | SIG-448 |
| Plan de ejecución por fases + decisiones cerradas | **spec** grande (secciones numeradas, fases) | SIG-582, SIG-210 |
| Cambio arquitectónico multi-app, con goals/non-goals y milestones | **epic / RFC** | SIG-527, SIG-364 |
| Planificación por objetivos (OKR trimestral) | **epic** (O1/O2/O3 + KR/KPI) | SIG-323 |

Un epic dueña el panorama, las decisiones y la secuencia de ejecución; a veces genera specs hijos (SIG-364). Un spec dueña un cambio verificable.

---

## 3. Esqueletos por tipo (headings — lee el ejemplo vivo para la forma)

No pegues un template completo. Usa esto como checklist, con concisión por encima.

**Feature spec** (molde canónico del equipo — dmuena; ver SIG-543 / SIG-263):

```
# Spec Funcional: <título>
**Estado:** … · **Fecha:** … · **Dueño:** …        (front-matter en negritas, no YAML)
---
## Problema                     (narrativo + root cause nombrado)
## Objetivo                     (opcional, si el problema es amplio)
## Historias de Usuario         (US-N: Como <rol>, quiero…, para…)
## Requisitos Funcionales       (tabla | # | Requisito | Prioridad | con RF-N; Prioridad = Debe/Podría)
## Criterios de Aceptación      (CA-N)
## Escenarios E2E               (opcional; E2E-N en Gherkin ES: Dado/Cuando/Entonces)
## Fuera de Alcance
## Dependencias / Impacto Cross-App
## Preguntas Abiertas           (opcional)
```

**Epic / RFC** (fecaputo + fases de cmontecinos; ver SIG-527 / SIG-364):

```
---
title / status / kind: epic|epic-rfc / owner / date / related_sigs: [...]   (YAML solo para epics grandes)
---
# Epic: <título>
## Summary / Resumen
## Context / Contexto            (Current State + The Problem)
## Goals / Non-Goals             (pareja obligada)
## Decisions / Architectural Rules   (decisiones no-negociables, con trade-offs)
## Proposed Design / Diseño      (subsecciones numeradas; mermaid solo si ayuda)
## Phased Plan / Milestones      (Fase/Phase N con releases o semanas)
## Risks / Rollback              (Rollback si hay riesgo de infra)
## Success Metrics
## Open Questions
## Out of Scope
## References / Specs hijas
```

---

## 4. Convenciones que hacen que "se vea del equipo"

Detalle completo en [`references/conventions.md`](references/conventions.md). Lo de alto valor:

- **Identificadores del equipo (los reales):** `US-N` (historias), `RF-N` (requisitos funcionales, en **tabla con columna Prioridad `Debe`/`Podría`**), `CA-N` (criterios de aceptación), `E2E-N` (escenarios). **NO uses `BR-N` ni `SEC-N`** — ningún spec del equipo los numera; si hay reglas de negocio van como sección en prosa, no como `BR-N`.
- **Gherkin en español:** `**Dado** / **Cuando** / **Entonces**`. Historias: `**Como** <rol>, **quiero** …, **para** …`.
- **Idioma:** default **español** para la prosa de feature specs; **inglés** para epics/RFCs y design docs técnicos. Es común y aceptado prosa ES con headings EN. Nombres de apps, endpoints y métricas siempre en inglés.
- **Título H1 prefijado por tipo:** `Spec Funcional:` / `Spec:` / `Epic:` / `RFC:`.
- **Ancla al código real:** referencia clases/endpoints/repos concretos (`isSameAsLatestConfig`, `PATCH …/config`, `component_type_registry`) — patrón fuerte en dmuena y cmontecinos. Da credibilidad y baja ambigüedad.
- **Disciplina de alcance:** una sección explícita de **Fuera de Alcance** es la más universal del equipo (aparece en los 9 specs revisados) — es como frenan el scope creep. Cuando aplique, separa **Decisiones cerradas** (no se debaten aquí) de **Gaps/Preguntas abiertas** (hay que decidirlas antes/durante el build).
- **Rollback** cuando el cambio toca infra riesgosa (patrón de cmontecinos). **Success Metrics/KPIs** en migraciones y epics.
- **Métricas** (si toca data path): `advertising.signals.{component}.{name}{tag:value}`; distinguir motivos de falla por tag; nunca meter valores de payload ni IDs de alta cardinalidad en métricas (van a logs/spans).
- **Linking:** referencia specs hermanos como `SIG-N` en prosa, con URL completa en Referencias. Enlaza Grid cuando tiene el detalle de escenarios.

---

## 5. Workflow para producir un spec

**El camino es Grimoire** (`/grimoire.arcanist`): hace el brainstorm socrático, detecta specs solapados, genera los diagramas y corre el gate de aprobación antes de publicar. Esta skill es el criterio de contenido que Grimoire aplica, no un flujo alternativo.

1. Invoca `/grimoire.arcanist`. Antes de responderle, carga el ejemplo canónico más cercano (`references/canonical-specs.md`) para saber qué forma buscas.
2. Durante el brainstorm, sostén el §0 y la concisión: cada respuesta tuya tiene que cerrar una ambigüedad real, no agregar texto.
3. Redacta el contenido siguiendo el esqueleto (§3) y las convenciones (§4).
4. Corre el **checklist pre-review** (§6) antes del gate de aprobación de Grimoire.
5. Publica y muévelo a `review` (Grimoire lo hace; la mecánica cruda está en el runbook, ojo backticks).

**Si el funcional ya existe y hay que corregirlo**, no rehagas el flujo de Grimoire: aplica el §0 —el resultado es el documento vigente, sin rastro de lo que pediste cambiar— más las convenciones de §4, y publica por el runbook.

---

## 6. Checklist pre-review

Antes de mover un spec a `review`:

- [ ] El Problema responde *por qué existe este spec*, con **root cause** nombrado (no síntoma).
- [ ] Apps impactadas listadas (y, en epic, prioridad de implementación + fases).
- [ ] ≥2 historias de usuario (`US-N`) con criterios de aceptación verificables.
- [ ] `RF-N` en tabla con **Prioridad** (`Debe`/`Podría`); `CA-N` testeables.
- [ ] Escenarios (`E2E-N`, si aplica) cubren el happy path **y** los errores principales.
- [ ] Sección **Fuera de Alcance** explícita.
- [ ] Decisiones cerradas separadas de Gaps/Preguntas abiertas.
- [ ] **Rollback** si toca infra; **Success Metrics** si es migración/epic.
- [ ] **Regla del lector cero:** ni una frase que solo se entienda conociendo una versión anterior del documento. Corre el `grep` de [`references/que-es-una-spec.md`](references/que-es-una-spec.md).
- [ ] Concisión: sin párrafos de relleno; el diagrama no re-narrado en prosa; nada de referencias fantasma.
- [ ] Specs hermanos cross-linkeados (`SIG-N` + URL); hijos de epic linkeados; Grid/refs incluidos.

---

Para la versión narrativa (onboarding, filosofía, el "por qué" de las convenciones), ver [`runbook.md`](runbook.md).
