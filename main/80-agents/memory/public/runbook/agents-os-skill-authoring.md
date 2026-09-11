---
type: runbook
schema_version: 1
scope: global
created: "2026-09-11"
updated: "2026-09-11"
area:
project:
application:
entities: []
related: []
aliases:
  - skill-authoring-runbook
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/global
  - tech/agents-os
  - action/skill-authoring
---

# agents-os-skill-authoring

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Ejecutar el lifecycle mecánico de una skill de AGENTS OS después de que `agents-os-skill-authoring` haya clasificado el artefacto y definido su contrato de comportamiento.

Este runbook posee materialización, cambios de archivos, checks de activación, validación, recuperación ante fallos y registro del `change_log`. No decide si un artefacto debe ser skill ni diseña su contrato semántico.

## Precondiciones

- `../../../skills/agents-os-skill-authoring/SKILL.md` clasificó el artefacto como `skill`.
- La capacidad, el trigger boundary y los handoffs están definidos.
- Están disponibles `../../../skills/_shared/note-types.md`, `../../../skills/_shared/skill-contract.md`, `../../../skills/_shared/schema-contract.md` y `../../../templates/skill.md`.
- Se inspeccionó el target y cualquier artefacto existente con responsabilidad solapada.
- La operación está definida: `create`, `refine` o `deprecate`.

Si falta una precondición semántica, detener y volver a `agents-os-skill-authoring`.

## Procedimiento

1. **Inspeccionar antes de escribir.**
   - Leer las fuentes canónicas vigentes requeridas para el cambio.
   - Inspeccionar el target antes de crear nada.
   - Buscar skill, runbook o memoria con responsabilidad solapada.
   - Si ya existe un artefacto canónico dueño de la responsabilidad, preferir refinar o enlazar; no duplicar.

2. **Materializar cuando la skill es nueva.**
   - Usar `../../../skills/_shared/scripts/materialize_schema_note.py` con `type: skill` y target vault-relative.
   - Consultar el contrato/`--help` vigente del script; no usar sintaxis recordada ni inventada.
   - No copiar a mano frontmatter canónico.
   - No continuar si la materialización queda parcial o falla el gate del contrato.

3. **Modificar preservando el contrato vigente.**
   - En `refine`, preservar metadata válida existente salvo que el cambio requiera actualizarla.
   - Completar las secciones exigidas por `skill-contract.md` y el schema ejecutable vigente.
   - Mantener Scope/Purpose enfocado en responsabilidad, no rationale.
   - Mantener `Minimal Read` realmente mínimo.
   - Dejar decisiones y orquestación en la skill; sacar procedimientos deterministas, failure-sensitive o rollbackable al runbook/tooling correspondiente.
   - Referenciar reglas canónicas en vez de copiarlas.

4. **Comprobar activación con tres casos mínimos.**
   - **Positivo:** caso inequívocamente propio → la skill debe aplicar.
   - **Negativo:** comparte vocabulario pero no responsabilidad → la skill no debe aplicar.
   - **Adyacente:** pertenece a otro artefacto → debe existir handoff explícito.
   - Revisar que `description`, Purpose y Procedure describan la misma capacidad y que no exista lenguaje catch-all.

5. **Validar Draft→Ready.**
   - Ejecutar los checks canónicos vigentes de `skill-contract.md` y schema contract sobre los paths explícitamente modificados.
   - Confirmar frontmatter/schema, secciones requeridas, boundary de activación, Minimal Read, Procedure, Hard Rules, Output, referencias y separación skill/runbook.
   - Un check obligatorio fallido mantiene el artefacto no listo.

6. **Registrar el lifecycle change.**
   - Materializar `type: change_log` mediante el flujo canónico vigente.
   - Registrar skill creada/refinada/deprecada y cualquier runbook relacionado creado o actualizado por la misma operación.
   - No reportar `READY` mientras skill y `change_log` no sean válidos.

7. **Deprecar sin borrar historia.**
   - Seguir el lifecycle y las reglas canónicas vigentes para deprecación.
   - Mantener enlaces/handoffs necesarios para no dejar referencias huérfanas.
   - Registrar la deprecación en el `change_log`.

## Validación

Success requiere, como mínimo:

```text
Classification:      PASS
Schema/frontmatter:  PASS
Skill contract:      PASS
Trigger positive:    PASS
Trigger negative:    PASS
Trigger adjacent:    PASS
No duplicated rule:  PASS
Runbook separation:  PASS
Change log:          PASS
```

Checklist:

- [ ] La clasificación sigue siendo `skill`.
- [ ] Frontmatter y schema cumplen el contrato ejecutable actual.
- [ ] Existen las secciones requeridas por el contrato actual.
- [ ] `description` y trigger boundary son específicos y coherentes.
- [ ] `Minimal Read` contiene sólo dependencias necesarias.
- [ ] `Procedure` puede ser ejecutado por un agente sin esconder un runbook dentro.
- [ ] `Hard Rules` previenen fallos reales y no duplican Procedure.
- [ ] `Output` es explícito.
- [ ] Las reglas canónicas están enlazadas, no copiadas.
- [ ] Rationale y explicación humana extensa están fuera de `SKILL.md`.
- [ ] Los tres casos de activación pasan.
- [ ] El `change_log` requerido existe y es válido.

Cualquier `FAIL` deja la operación `INCOMPLETE` o `ABORTED`; nunca `READY`.

## Rollback / recuperación

Abortar sin publicar un resultado `READY` cuando:

- la clasificación deja de ser `skill`;
- un artefacto canónico existente ya posee la responsabilidad;
- las fuentes canónicas entran en conflicto y resolverlo exige cambiar policy fuera del scope;
- falla la materialización/schema;
- falla un check Draft→Ready obligatorio;
- la única forma de hacer pasar el artefacto es duplicar o debilitar una regla canónica.

Ante fallo:

1. no debilitar validaciones para forzar `PASS`;
2. revertir sólo cambios introducidos por la operación actual cuando sea seguro;
3. preservar contenido válido preexistente;
4. reportar checkpoint fallido y handoff requerido;
5. no emitir éxito para un artefacto parcial;
6. registrar el intento si la constitución vigente exige evidencia del lifecycle change.

## Evidencia

Registrar al finalizar:

```text
Operation:             create | refine | deprecate
Skill:                 <path>
Runbook:               <path usado | no aplica>
Classification:        PASS | FAIL
Schema/frontmatter:    PASS | FAIL
Draft→Ready:           PASS | FAIL
Activation:
  positive:            PASS | FAIL — <caso>
  negative:            PASS | FAIL — <caso>
  adjacent:            PASS | FAIL — <caso>
Runbook separation:    PASS | FAIL
Validation:            <comando/checks y resultado>
Change log:            <path | NOT CREATED>
Result:                READY | INCOMPLETE | ABORTED
Failure checkpoint:    <checkpoint | none>
```
