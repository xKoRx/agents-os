---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Forge — Forge Explorer v0]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
tags:
  - kind/doc
  - area/echo
  - area/forge
  - action/handoff
created: "2026-09-21"
updated: "2026-09-21"
---

# Forge Explorer v0 — decisión de diferimiento y handoff

**Decisión del owner, 2026-09-21: DEFERRED / NOT PRIORITY.** La idea es útil y necesaria a futuro, pero no corresponde ejecutarla ahora. Fue introducida como propuesta nueva por el manager del carril Echo, NO proviene del roadmap original Echo ni del alcance congelado F-01…F-05 de Factory V2. El ownership exclusivo de la eventual implementación pertenece al **manager de Forge**; el manager de Echo NO despacha agentes, revisa código ni certifica Explorer. El parent no debe incluirla en el critical path de Factory V2 ni F-05-C.

## Qué conservar (trabajo ya realizado)

- Repo: `xKoRx/symphony`; branch `codex/forge-explorer-v0`; baseline exacto `codex/f05-release-prep @ 745bc8b94e1f6148ddc16c02eb86a755088c2666` (release 0.2.105 en fecha de planificación); commit exclusivo de planificación `cc36c39845235476761cb12836e433e9f890278d`. El estado de HEAD debe comprobarse nuevamente el día de reactivación; NO asumir que los refs permanecen inmóviles.
- Paquete persistido: `specs/FEAT-FORGE-EXPLORER-V0/SPEC.md`, `PLAN.md`, `NORMAL-PROMPT.md`. Contienen decisiones, contratos, allowed files, EX0…EX6, pruebas, gates y STOP conditions. Worktree registrado al planificar: `/home/kor/aranea/work/forge-explorer-20260921/symphony`; su existencia/estado futuro NO están garantizados.
- Nota de proyecto: [[Echo Forge — Forge Explorer v0]]. La read surface reutilizada es F-05-I: `docs/echo-forge/f05-read-surface.md` y seis comandos de lectura (`campaign get|list`, `run get|stages`, `strategy get`, `release-matrix`). No replicar SQL ni recomputar finalist membership, rankings, funnel o certificaciones.
- Solución planeada, NO implementada: visor local read-only, Go stdlib, `sqx/cmd/forge-explorer`, HTML server-rendered en loopback, invocación de `sqx-flowkit` exclusivamente con allowlist; vistas HOME, CAMPAIGN, RUN, STRATEGY, RELEASE. No incluye viewer SQX GUI, selección/materialización de pools, reejecución ni escrituras. El usuario había planteado por separado explorar estrategias en SQX GUI: no fingir que este v0 cubre esa capacidad.
- No se ejecutó implementación EX0…EX6, no hubo tests de producto, release, deploy ni certificación del Explorer. `PHYSICAL CERTIFICATION NOT RUN`.

## Política hasta reactivación

**NO DISPATCH.** No enviar `NORMAL-PROMPT.md` a un coding agent, no abrir PR/merge, no desarrollar, no certificar ni desplegar. No modificar los contratos F-05-I ni tocar la campaña F-05-02 como parte de este proyecto. Su tarea del tablero se considera *diferida*, no WIP, ni bloqueo de Factory V2. Conservar el commit docs-only y los artefactos sin borrarlos; toda acción de continuidad queda en el carril Forge. Echo únicamente coordina fronteras de integración cuando Forge lo solicite.

## Gate de reactivación (decisión exclusiva del manager Forge + owner)

1. Confirmación explícita del owner de que Explorer entra en la prioridad de desarrollo.
2. Comprobación de que Forge no tiene ya un frontend/viewer equivalente ni otro agente implementando la misma funcionalidad; aclarar integración con front existente si aplica.
3. Revalidar la rama actual F-05-I, baseline SHA y evolución de los seis contratos CLI; comparar con SPEC/PLAN preparados. Si hubo drift, actualizar el paquete por delta, no rediseñar desde cero ni aplicar `BASELINE_MOVED` como bloqueo perpetuo.
4. Asegurar worktree/branch exclusivos y ausencia de colisiones con trabajo activo de certificación o desarrollo Forge.
5. Sólo entonces aprobar explicitamente prioridad y despachar NORMAL con el mandato conservado; tests, fixtures y smoke serán evidencia de desarrollo, no certificación física.

## Contexto de alcance y orden

F-01/F-02/F-03 y F-05-I tienen sus estados propios; Forge Explorer es una capacidad posterior y opcional desde el punto de vista del DAG de Factory V2. La release 0.2.105 y CERT-F05-01 PASS son contexto histórico, no criterios de aceptación del Explorer. El estado de CERT-F05-02/CERT-F05-03 debe consultarse al reactivar, jamás inferirse de esta nota. No bloquear desarrollo Echo por Explorer y no consumir sesiones de TOP/NORMAL adicionales hasta aprobación.

**NEXT EXACT:** mantener este handoff diferido; el carril Echo continúa con E-08/E-09. El manager Forge es el único que puede proponer reactivación.