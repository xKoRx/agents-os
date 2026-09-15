---
type: skill
schema_version: 1
name: agents-os-doctor
scope: global
created: 2026-07-25
updated: 2026-09-14
description: Audita salud estructural, conformance, presupuesto/aislamiento de contexto y canonicalidad de AGENTS OS desde un único comando read-only. Usar ante "agents-os-doctor", "doctor", "health check AGENTS OS", cierres de fase o fallas de bootstrap/retrieval; no usar para reparar automáticamente.
aliases:
  - agents-os-doctor
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - action/doctor
  - action/lint
  - tech/agents-os
---

# agents-os-doctor — AGENTS OS Health Check

## Purpose

Obtener una fotografía única, acotada y reproducible de AGENTS OS sin mutar el
vault. El Doctor agrega providers existentes; no copia sus reglas ni repara sus
findings.

## Lectura mínima

Para ejecutar un diagnóstico ordinario no leas documentación adicional: corre
el entrypoint y usa su JSON si necesitas detalle. Sólo al modificar el Doctor:

1. Lee `PHASE-4-AGGREGATION-SPEC.md` para el contrato del agregador.
2. Lee `P4-PROVIDER-CONTRACT-AUDIT.md` para schemas, flags y ownership reales.
3. Inspecciona únicamente el provider afectado.

## Ejecución

Desde `VAULT_ROOT`:

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py
```

Opciones:

- `--json`: envelope machine-readable completo.
- `--component structural|conformance|context|canonical|all`: ejecución dirigida.
- `--strict`: conserva los veredictos, pero retorna no-cero ante `WARN` o `SKIP`.
- `--live`: habilita sólo observaciones live read-only propiedad de cada provider.
- `--vault-root <path>`: diagnostica otra instalación que contenga el marker.

El modo normal y `--live` pasan `--no-write` a todos los providers externos. El
Doctor nunca crea resultados ni modifica Markdown canónico.

## Modelo de salud

Los cuatro componentes tienen una sola autoridad:

| Componente | Autoridad |
|---|---|
| Structural | checks existentes dentro de `scripts/doctor.py` |
| Conformance | `80-agents/tools/conformance-harness/agents_os_conformance.py` |
| Context | `80-agents/tools/context-budget/context_budget.py` |
| Canonical | `80-agents/tools/canonical-linter/canonical_linter.py` |

Structural conserva el club cerrado de `load_policy: always`: exactamente estos
tres paths fijos más el perfil global resuelto por directorio:

- `80-agents/agents-os/agent-constitution.md`
- `80-agents/skills/agents-os-bootstrap/SKILL.md`
- `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
- exactly ONE note under `80-agents/memory/public/user-preference/` — the global profile.

Una segunda nota always en ese directorio es inválida: a second one is a club violation and zero means the install is incomplete.

El envelope separa dos ejes:

- `execution_status`: `OK` o `ERROR`; dice si el provider pudo ejecutarse e
  interpretarse.
- `verdict`: `PASS`, `WARN`, `FAIL` o `SKIP`; dice qué observó sobre AGENTS OS.

Un provider con findings `FAIL` sigue teniendo `execution_status: OK`. Timeout,
entrypoint ausente, JSON inválido, exit code contradictorio o crash producen
`execution_status: ERROR` y exit global `2`; no se maquillan como un defecto del
vault. Los providers posteriores se ejecutan igualmente.

Los findings estructurales `LOW` se proyectan como `status: INFO`: siguen
visibles en JSON y en el contador humano `low`, pero no alteran el verdict ni
`--strict`. Ésa es la política retrocompatible del Doctor estructural; nunca se
etiquetan como `PASS`.

Exit codes:

- `0`: ejecución correcta sin `FAIL`; en modo normal `WARN`/`SKIP` son visibles
  pero no bloquean.
- `1`: hay `FAIL`, o `--strict` encontró `WARN`/`SKIP`.
- `2`: al menos un provider terminó en `ERROR` o el `VAULT_ROOT` es inválido.

## Instalaciones por dominio

El registro `30-resources/agents/domain-router-registry.md` es opcional. Un core
DEFAULT con registro vacío es válido:

- baseline y escenarios DEFAULT siguen corriendo;
- `scope_pack` enumera sólo dominios realmente registrados;
- escenarios que requieren fixtures Meli/Aranea quedan `SKIP` con causa;
- la ausencia de paquetes federados nunca debe causar `ERROR` ni justificar
  exportarlos dentro del core.

## Procedure

1. Ejecuta el Doctor completo, salvo que el usuario pida un componente.
2. Si necesitas automatizar o comparar, repite con `--json`; no parsees el
   resumen humano.
3. Distingue findings del sistema (`verdict`) de fallas del instrumento
   (`execution_status`) antes de proponer una acción.
4. Consume los records/counts que cada provider emite. Context es dueño de su
   record `RULES-FIDELITY-ANCHORS`; el agregador no lo fabrica ni lo recuenta.
5. Reporta primero los findings accionables. El resumen humano ya limita la
   muestra a cinco y distribuye espacio entre providers; usa el JSON para el
   inventario completo.
6. No interpretes `estimated_tokens` como conteo exacto: es `chars/4`, baseline
   aproximado y nunca criterio único de aceptación.
7. Si se autoriza una reparación, modifica la autoridad dueña del finding, no
   el agregador. Repite Doctor y los selftests del provider afectado.

## Verificación de cambios al Doctor

```bash
python3 80-agents/skills/agents-os-doctor/scripts/selftest.py
python3 80-agents/tools/conformance-harness/registry_selftest.py
python3 80-agents/tools/context-budget/selftest.py
python3 80-agents/tools/canonical-linter/selftest.py
```

Además, construye el core exportable y ejecuta el Doctor dentro del artefacto.
Una prueba sólo sobre el vault fuente no demuestra compatibilidad DEFAULT.

## Hard Rules

- Read-only siempre; nunca auto-aplicar fixes.
- No duplicar business logic de providers en `aggregate.py`.
- No detener providers independientes después de un `FAIL` o `ERROR`.
- No convertir `SKIP` o ausencia de evidencia en `PASS`.
- No imprimir valores de secretos.
- No agregar dominios al core para hacer pasar escenarios scoped.
- Baseline Git desconocido se reporta `null`; no inventar estabilidad.
