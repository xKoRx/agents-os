---
type: skill
schema_version: 1
name: sdd-shot-3-correct
description: Corrige sólo findings SDD adjudicados, preserva regresiones fuertes y entrega candidato final con evidencia; no reabre diseño ni autoacepta sus correcciones.
scope: global
created: '2026-10-30'
updated: '2026-10-30'
entities: []
related:
  - '[[sdd-developer]]'
aliases:
  - shot3
  - sdd-corrector
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/sdd
---

# SDD Shot 3 — corrección causal y evidencia final

## Purpose

Resolver hallazgos adjudicados sin reabrir decisiones congeladas, preservar regresiones útiles y entregar un candidato final verificable. Aplicar a `delivery_role: shot-3-correct` tras Shot 2; no diseñar, realizar la revisión independiente ni aceptar el propio fix. Un resultado sin correcciones necesarias permite un delta vacío, no una mejora inventada.

## Minimal Read

- `../sdd-developer/role-contract.md`.
- Autoridades congeladas, baseline, candidato Shot 1, reporte y reproducers de Shot 2, adjudicación del principal/Owner y alcance de corrección.
- Sólo fuentes y pruebas afectadas; consultar evidencia original cuando un hallazgo o expectativa sea ambiguo.

## Procedure

1. Verificar identidades y la disposición de cada finding: accepted, refuted con evidencia, deferred con autoridad o pendiente. No tratar silencio como rechazo. Un finding material pendiente de adjudicación impide declarar cerrado el ciclo.
2. Reproducir cada defecto aceptado cuando sea seguro; describir la causa, el invariante violado y el mecanismo del fix de forma breve. Corregir en el dueño del comportamiento, no mediante condiciones ad hoc que sólo reconozcan la fixture.
3. Elegir el menor cambio coherente que elimine la causa y respete PLAN. Reutilizar componentes existentes; no convertir un parche en rediseño. Si la evidencia contradice el finding o exige otra semántica, retornar el conflicto con prueba al principal, sin descartarlo unilateralmente.
4. Promover reproducers valiosos a regresiones permanentes en los módulos canónicos definidos por `sdd-developer`. Conservar el oráculo independiente y fuerza de assertions; deduplicar cobertura equivalente sin perder el caso que detectó el fallo.
5. Ejecutar la reproducción corregida, límites vecinos pertinentes y suite afectada exigida. Comparar baseline -> candidato inicial -> candidato final; verificar efectos laterales e integridad. Si aparece un defecto ordinario del delta dentro del scope, corregir/reprobar en este shot y registrarlo; si cambia requisitos, riesgos o alcance, retornar al principal.
6. Preparar la matriz final AC/finding -> fix/test -> evidencia -> identidad exacta. Registrar lo que sigue NOT_RUN. Si no hay hallazgos aceptados, validar la evidencia y conservar el candidato sin tocar producto; no saltar obligaciones de este rol.
7. Retornar `FINAL_CANDIDATE_READY` sólo con correcciones/gates propios completos y trazabilidad, más feedback y agent_run aplicable. La comprobación independiente del fix y la aceptación pertenecen al gate; un verde del corrector no certifica su propio cambio.

## Output

Envelope común más:

```text
status: FINAL_CANDIDATE_READY | CORRECTION_INCOMPLETE | SDD_NOT_READY | SDD_BLOCKED_EXTERNAL
identity: baseline, candidato inicial y final; dirty/diff y evidencia vinculada
findings_disposition: ID -> autoridad/adjudicación -> causa -> fix -> regresión -> resultado
acceptance_matrix: AC -> test -> evidencia -> PASS/FAIL/NOT_RUN
assets_disposition: promovido, unificado o descartado con razón
remaining: defectos, conflictos, dependencias o ninguno demostrado
next: acceptance gate sobre la identidad final
```

## Hard Rules

- No corregir findings refutados ni ocultar deuda/risks material con un cambio de severidad propio. Un waiver no vuelve PASS a un AC fallido.
- No eliminar pruebas del verificador por incomodidad, cambiar resultados esperados para copiar la implementación ni generalizar el workaround más allá del contrato.
- No emitir `SDD_DELIVERY_PASS`, certificar producción ni promover una release; el retorno es candidato final.
- No planear un cuarto shot correctivo. Si el ciclo no alcanza el criterio, retornar estado honesto; el principal decide explícitamente un nuevo ciclo, no un bucle autónomo.
- Ownership de mejora: esta skill. Aprender del retrabajo y de los fallos del fix por el runbook compartido, después del resultado, nunca alterando los gates actuales.
