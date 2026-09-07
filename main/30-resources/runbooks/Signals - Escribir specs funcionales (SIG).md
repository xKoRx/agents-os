---
type: runbook
schema_version: 1
scope: project
created: "2026-08-12"
updated: "2026-08-12"
area:
project: "[[Onboarding Signals]]"
application:
entities:
  - "[[Onboarding Signals]]"
related:
  - "[[signals-func-spec-authoring]]"
aliases:
  - runbook specs funcionales signals
  - como escribir spec SIG
confidence: high
source_session: 2026-08-12
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/project
  - tech/spellbook
  - tech/signals
  - tech/ads
---

# Signals — Escribir specs funcionales (SIG)

%% Cara humana (el *por qué*) de la skill [[signals-func-spec-authoring]]. El procedimiento imperativo vive en el SKILL.md; acá el racional y el onboarding. Una fuente canónica por hecho: no duplicar la procedura. %%

## Propósito

Guía para humanos del equipo Signals/Ads sobre cómo pensar un spec funcional en
Spellbook (proyecto SIG). La contraparte para agentes es la skill
[[signals-func-spec-authoring]]: ese SKILL.md es la versión ejecutable; esta nota es el
"por qué" y el onboarding. **No copia templates**: los moldes vivos son los specs
reales, que se leen con `spellbook specs view <id>`.

## Precondiciones

- Spellbook CLI autenticada por token (ver `/spellbook.auth`). Verificar con
  `spellbook specs list SIG`.
- **No** intentar entrar por el navegador: `spellbook.adminml.com` está tras el SSO
  `auth-meli.adminml.com` y las herramientas de browser de un agente quedan
  atrapadas ahí. La web es para personas; la puerta operativa es la CLI.

## Procedimiento

Ver la skill [[signals-func-spec-authoring]] para el paso a paso imperativo. En corto:

1. `spellbook specs list SIG` → ver qué existe, evitar duplicar.
2. Elegir la forma según el trabajo:
   - **Epic** (toca 3+ apps o tiene fases de rollout) — dueño del big picture, el
     desglose por app, el plan por fases y las decisiones abiertas; tiene hijas.
     Ej. vivo: SIG-492.
   - **Spec de feature** (1–2 apps: endpoint/comportamiento nuevo). Ej. SIG-462.
   - **Spec chico / fix** (arreglo puntual o cambio de contrato, tabla RF-N).
     Ej. SIG-543, SIG-541.
   - **Epic de bug** (incidente de producción con root cause). Ej. SIG-547.
3. Abrir el spec canónico que más se parece (catálogo en las references de la skill)
   y leerlo entero antes de escribir. De ahí sale la estructura y la profundidad.
4. Redactar respetando las convenciones (idioma, `US/BR/E2E/RF`, métricas
   `advertising.signals.*`, disciplina de alcance).
5. Pasar el checklist pre-review y mover a `review`.

## Por Qué (lo que este runbook previene)

Errores que, sin esto, cada persona/agente nuevo vuelve a cometer:

- Perder tiempo peleando con el SSO en el navegador en vez de usar la CLL.
- Inventar `--project` en `specs list` (es posicional: `specs list SIG`).
- Escribir un spec sin sección **Fuera de alcance** → scope creep en review.
- Mezclar **Decisiones cerradas** con **Gaps pendientes** → en el sprint aparece una
  decisión que nadie tomó.
- Meter valores de payload en métricas → problema de privacidad y cardinalidad.
- Copiar un template viejo que ya no refleja cómo escribe hoy el equipo, en vez de
  leer el spec canónico vivo.

## Validación

- La skill [[signals-func-spec-authoring]] resuelve correctamente el acceso (CLI) y la
  elección de forma sin abrir el navegador.
- Base de specs revisados: SIG-462, SIG-492, SIG-518, SIG-541, SIG-543, SIG-547,
  SIG-551 (2026-08-12).

## Mantención

Se mantiene **re-listando, no copiando**. Si el estilo del equipo evoluciona, el spec
de mejor calidad de cada tipo pasa a ser el nuevo referente: actualizar los IDs en las
references de la skill, no reescribir prosa. Así la documentación no se pudre.
