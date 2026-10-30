---
type: skill
schema_version: 1
name: sdd-shot-2-verify
description: Verifica adversarialmente un candidato SDD en contexto independiente; deriva probes desde requisitos y entrega findings reproducibles sin corregir producto ni aceptar la entrega.
scope: global
created: '2026-10-30'
updated: '2026-10-30'
entities: []
related:
  - '[[sdd-developer]]'
aliases:
  - shot2
  - sdd-verifier
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/sdd
---

# SDD Shot 2 — falsación independiente

## Purpose

Intentar refutar que el candidato cumple los requisitos y preserva invariantes, con hallazgos reproducibles o evidencia positiva limitada al alcance probado. Aplicar a `delivery_role: shot-2-verify` sobre un candidato identificado; no implementar fixes, rediseñar ni aceptar la entrega. Ejecutar en contexto nuevo independiente de quien implementó.

## Minimal Read

- `../sdd-developer/role-contract.md`.
- Requisitos/AC congelados, baseline y candidate identity, reglas del repo y entorno de pruebas autorizado.
- Diff, código/tests relevantes y evidencia de Shot 1. Derivar primero obligaciones y riesgos desde las autoridades; después contrastar el reporte del implementador, no heredar su narrativa como prueba.

## Procedure

1. Verificar identidad, independencia de contexto y estabilidad del candidato. Si el código cambió durante la revisión, delimitar la evidencia válida y retornar el gap. No revisar un checkout distinto asumiendo que equivale al commit reportado.
2. Construir una matriz AC/invariante -> posible fallo -> prueba que lo detectaría. Priorizar por impacto y plausibilidad: estado, idempotencia/reintentos, concurrencia/orden, precisión/tiempo, persistencia, autorización/tenancy, errores, compatibilidad y efectos laterales sólo donde apliquen. No ejecutar una lista universal sin relación con el cambio.
3. Buscar contraejemplos: ¿puede pasar el happy path incumpliendo el AC?, ¿el test usa el mismo helper defectuoso como resultado esperado?, ¿un mock elimina la frontera que afirma probar?, ¿un retry duplica un efecto? Para valores críticos, usar un oráculo independiente o cálculo explícito externo al camino verificado.
4. Ejecutar probes en el espacio autorizado sin editar producto. Comprobar que los tests se seleccionaron y sus aserciones se ejecutaron. Cuando sea pertinente, usar un control negativo seguro; alterar una expectativa prueba selección/aserción, no resistencia a una mutación del código productivo.
5. Comparar una regresión sospechada contra baseline bajo condiciones equivalentes cuando sea seguro. Separar defecto introducido, deuda previa, restricción de entorno y sospecha sin reproducir. Un fallo previo no absuelve un AC nuevo incumplido; una limitación de herramientas no demuestra que el producto falle.
6. Emitir findings con ID estable, severidad por impacto real, fuente del requisito, escenario mínimo, esperado/observado, candidate identity y evidencia. Indicar el comportamiento que necesita corregirse, no imponer una arquitectura. No convertir estilo personal en hallazgo bloqueante ni inventar problemas para parecer adversarial.
7. Disponer cada reproducer según `sdd-developer`; entregar matriz, riesgos residuales y feedback. La ausencia de findings no prueba lo que quedó NOT_RUN. El principal adjudica los hallazgos antes de Shot 3.

## Output

Envelope común más:

```text
status: VERIFICATION_PASS | VERIFICATION_FINDINGS | VERIFICATION_INCOMPLETE | SDD_NOT_READY | SDD_BLOCKED_EXTERNAL
reviewed_identity: baseline/candidate y entorno
independence: sesión/contexto, contribución previa al candidato y límites
matrix: AC/invariante -> probe/oráculo -> evidencia -> PASS/FAIL/NOT_RUN
findings: ID, impacto, requisito, reproducción, esperado/observado, atribución baseline
assets: reproducer durable + clasificación; sin modificar producto
residual_risks: límites de cobertura y evidencia aún requerida
```

`VERIFICATION_PASS` exige las obligaciones de esta revisión satisfechas; no equivale a aceptación de producto, release ni deploy.

## Hard Rules

- No arreglar producto, modificar AC ni cambiar la expectativa contractual. Probes/tests nuevos viven en el espacio de verificación autorizado; su promoción la realiza Shot 3 tras adjudicación.
- Si sólo existe el contexto del implementador, marcar verificación no independiente y bloquear esa certificación; cambiar el nombre del rol no crea independencia.
- No confiar en autoevaluaciones, conteos de tests o coverage como sustituto de evidencia funcional.
- No ejecutar sobre datos sellados ni servicios reales por inferencia de que «es un test».
- Ownership de mejora: esta skill; feedback de falsos positivos y defectos escapados se incorpora mediante el runbook de mejora, sin reescribir el criterio durante esta revisión.
