---
type: known_error
scope: global
created: 2026-07-17
updated: 2026-07-17
area: "[[Meli]]"
project: "[[Bajo y Muy Bajo Precio]]"
application: "[[vpp-backend]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Meli]]"
  - "[[vpp-backend]]"
related:
  - "[[preserve-legacy-semantics-when-extending-feature]]"
  - "[[diff-audit-diagnostic-leftovers]]"
aliases:
  - review finding heredado
  - finding sin regresion de branch
  - over-edit por review
confidence: verified
source_session: "codex-vpp-backend-2026-07-17-review-findings"
load_policy: when_error_matches
indexable: true
index_priority: critical
tags:
  - kind/known-error
  - workflow/code-review
  - workflow/git
  - area/meli
  - scope/global
---

# Confundir finding heredado con regresión de la branch

## Síntoma

- Un review señala una condición cuestionable en un archivo compartido y el agente la corrige sin demostrar primero que la branch la introdujo.
- Se modifican archivos para “alinear” comportamientos aunque el diff funcional contra la base no contenga esa regresión.

## Causa

- Se inspecciona el código actual y la intención del comentario, pero no se separan primero: comportamiento de `develop`, delta real de la branch y cambios locales sin commit.
- Se confunde una inconsistencia legacy válida como scope de la iniciativa con un bug introducido por el PR.

## Impacto

- Cambios innecesarios, churn en archivos compartidos, riesgo de alterar contratos legacy y pérdida de tiempo del desarrollador.

## Detección

- Antes de editar: ejecutar `git diff <base>...HEAD -- <archivo>` y `git diff <base> -- <archivo>`; luego usar `git log -S`/`git blame` para fechar la condición.
- Clasificar cada finding como: introducido por la branch, heredado sin cambio, o cambio local no autorizado.

## Mitigación

- Si el finding es heredado y el usuario exige preservar `develop`, no editar código: informar la evidencia y dejar el finding explícitamente fuera de scope.
- Si la feature es multi-vertical, aislar la lógica nueva en la vertical objetivo; no crear abstracciones compartidas que modifiquen la vertical legacy solo por simetría.
- Antes de cerrar, verificar `git diff HEAD --exit-code` para confirmar que no quedaron ediciones accidentales.

## Evidencia

- En la sesión `codex-vpp-backend-2026-07-17-review-findings`, los comentarios sobre RES describían condiciones presentes desde `develop`; no correspondía editar RES ni sus tests.
