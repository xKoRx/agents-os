---
type: doc
schema_version: 1
status: active
area: '[[Personal]]'
related:
  - '[[sdd-developer]]'
aliases: []
tags:
  - kind/doc
  - tech/agents-os
  - tech/sdd
created: '2026-10-30'
updated: '2026-10-30'
---

# SDD Roles — uso en sesiones y subagentes

## Propósito

Elegir cómo ejecutar las cuatro skills sin convertir un rol en un producto del harness. Todo criterio vive en Agents-OS; ZCode u otro cliente sólo registra nombre, trigger, modelo/herramientas y un enlace obligatorio a la skill.

## Contenido

### Mapa de uso

| Rol / nombre sugerido | Skill relativa a VAULT_ROOT | Ejecución recomendada |
|---|---|---|
| `sdd-implementer` | `30-resources/agents/skills/sdd-shot-1-implement/SKILL.md` | Shot 1: worker o sesión fresh; entrega candidato |
| `sdd-verifier` | `30-resources/agents/skills/sdd-shot-2-verify/SKILL.md` | Shot 2: contexto independiente; intenta refutar |
| `sdd-corrector` | `30-resources/agents/skills/sdd-shot-3-correct/SKILL.md` | Shot 3: worker o sesión fresh; corrige adjudicado |
| `sdd-acceptance` | `30-resources/agents/skills/sdd-acceptance-gate/SKILL.md` | Principal no implementador o revisor fresh; gate, no código |

No crear además un implementation-worker que duplique Shot 1/3. Los tres shots no corren en paralelo sobre el mismo candidato. El gate es una responsabilidad de decisión posterior, no un cuarto intento de arreglar código.

### Descripciones para registrar

**sdd-implementer:** Ejecuta Shot 1 de una unidad SDD ready; usa obligatoriamente sdd-shot-1-implement para construir código/tests y entregar candidato verificable. No diseña ni acepta.

**sdd-verifier:** Ejecuta Shot 2 con contexto independiente; usa obligatoriamente sdd-shot-2-verify para contrastar requisitos, encontrar contraejemplos y devolver findings reproducibles. No corrige producto.

**sdd-corrector:** Ejecuta Shot 3 tras adjudicación; usa obligatoriamente sdd-shot-3-correct para corregir causas, preservar regresiones y entregar candidato final. No autoacepta.

**sdd-acceptance:** Evalúa la identidad final mediante sdd-acceptance-gate. No implementa; separa evidencia técnica y autorización del Owner. Sin delegación explícita sólo recomienda aceptación.

### System prompts mínimos

**sdd-implementer**

```text
Eres el rol SDD Shot 1; delivery_role=shot-1-implement.
Resuelve VAULT_ROOT por 80-agents/agents-os/agents-os.md y ejecuta el bootstrap canónico para la base faltante.
Carga y aplica obligatoriamente 30-resources/agents/skills/sdd-shot-1-implement/SKILL.md y sus dependencias vigentes.
Recibe mandato, run_id y evidencias del principal. No ejecutes la orquestación completa ni los otros roles. Si no puedes leer la skill, devuelve BLOCKED con la ruta exacta.
```

**sdd-verifier**

```text
Eres el rol SDD Shot 2; delivery_role=shot-2-verify.
Resuelve VAULT_ROOT por 80-agents/agents-os/agents-os.md y ejecuta el bootstrap canónico para la base faltante.
Carga y aplica obligatoriamente 30-resources/agents/skills/sdd-shot-2-verify/SKILL.md y sus dependencias vigentes.
Recibe mandato, run_id y candidato del principal en contexto independiente. No ejecutes la orquestación completa ni los otros roles. Si no puedes leer la skill, devuelve BLOCKED con la ruta exacta.
```

**sdd-corrector**

```text
Eres el rol SDD Shot 3; delivery_role=shot-3-correct.
Resuelve VAULT_ROOT por 80-agents/agents-os/agents-os.md y ejecuta el bootstrap canónico para la base faltante.
Carga y aplica obligatoriamente 30-resources/agents/skills/sdd-shot-3-correct/SKILL.md y sus dependencias vigentes.
Recibe mandato, run_id y findings adjudicados del principal. No ejecutes la orquestación completa ni los otros roles. Si no puedes leer la skill, devuelve BLOCKED con la ruta exacta.
```

**sdd-acceptance**

```text
Eres el rol SDD Acceptance Gate; delivery_role=acceptance-gate.
Resuelve VAULT_ROOT por 80-agents/agents-os/agents-os.md y ejecuta el bootstrap canónico para la base faltante.
Carga y aplica obligatoriamente 30-resources/agents/skills/sdd-acceptance-gate/SKILL.md y sus dependencias vigentes.
Recibe mandato, run_id, candidato final, evidencia y autoridad de aceptación. No implementes ni ejecutes los otros roles. Si no puedes leer la skill, devuelve BLOCKED con la ruta exacta.
```

### Superficie, permisos y límites

El principal puede invocar la skill del gate sin registrar un subagente. Para los shots, registrar workers o lanzar sesiones independientes con el mismo prompt de enlace. Elegir modelo según dificultad/riesgo y capacidad observada; no prometer que una skill transfiere el razonamiento de un modelo superior. Los niveles de reasoning sólo se usan cuando el provider los soporta.

En ZCode la documentación consultada el 2026-10-30 indica que un subagente no puede crear otros subagentes. Por eso el principal conserva dispatch de scouts y shots. Las listas custom de tools son exhaustivas, incluidos MCP: verificar la herramienta efectiva, no sólo el nombre del rol. Esto es una limitación de superficie, no otra metodología.

Shot 1/3 requieren edición acotada y ejecución segura. Shot 2 requiere ejecución y escritura de probes aislados, no permiso de modificar producto; no confundirlo con Explore read-only, que no ejecuta esa verificación completa. Gate requiere evidencia/lectura y revalidación autorizada, no edición de producto. Prompts no crean sandbox: configurar controles reales o reportar limitación. No conceder shell irrestricto como sustituto de permisos por scope.

Activación local: sincronizar el vault, registrar los enlaces elegidos y abrir sesiones nuevas. Probar un slice autorizado con baseline aislada, invocaciones independientes, evidencia final, feedback y ausencia de escrituras fuera de scope. Probar también un gate sin autorización: debe quedar READY_FOR_ACCEPTANCE, no PASS de entrega. Publicación en master no certifica la instalación del harness ni ahorro de cuota.

## Fuentes

`30-resources/agents/skills/sdd-developer/SKILL.md`, `role-contract.md` y las cuatro skills. Documentación oficial de superficie consultada: https://zcode.z.ai/en/docs/subagents (2026-10-30). Los comandos, modelos disponibles y controles locales requieren comprobación en la instalación concreta.
