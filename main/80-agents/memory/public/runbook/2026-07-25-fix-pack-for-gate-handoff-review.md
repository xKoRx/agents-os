---
type: runbook
scope: public
created: 2026-07-25
updated: 2026-07-25
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge - Cierre de Etapa 4]]"
related:
  - "[[Echo Forge]]"
aliases:
  - gate-review-fix-pack
  - handoff-rejected-fix-pass
confidence: verified
source_session: 2026-07-25-fix-pack-g2-review
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - tech/gate-review
  - tech/sdd
  - scope/public
---

# Pase de fix para handoffs de gate rechazados en review

## Propósito

Recuperar un handoff de gate (`G<n>`) cuyo veredicto de revisión del owner fue "no aceptar" — específicamente cuando el veredicto enumera blockers verificables y non-blockers reales. **No** se reescribe historia, **no** se hace reset, **no** se mezclan refactors.

## Precondiciones

- Branch actual limpia salvo los cambios del pase original (sin `git reset`, sin `checkout --`).
- Handoff del gate (`<feature>/phase<n>/G<n>_HANDOFF.md`) accesible.
- Veredicto del owner con tabla `Blocker` / `Evidencia` / (opcional) `No bloqueantes`.
- Toolchain verificada: build del proyecto, JUnit (si aplica), Go test (si aplica).

## Procedimiento

1. **Clasificar blockers** del veredicto en 4 buckets:
   - **B1 — Manifest/file integrity**: hashes, manifests, listas, conteos firmados.
   - **B2 — Atomicidad/contract**: comportamiento no-determinista, leaks, orden de operaciones.
   - **B3 — Decisión contradicha**: ADR/OD en handoff no coincide con el código (imports, firmas, defaults).
   - **B4 — DoD incompleto**: items declarados ✅ pero sin evidencia reproducible.
2. **Por cada blocker**:
   - Reproducir el fallo con el comando exacto del veredicto (no de memoria).
   - Aplicar el mínimo cambio que cierra el bloque sin tocar áreas no relacionadas.
   - Añadir/coberturar test que falle antes y pase después.
3. **Non-blockers del veredicto**: anotar en la nota del proyecto y en el handoff; resolver los que sean baratos; defer firmado los que requieran infra externa (e.g. SQX Build 142 real).
4. **Actualizar el handoff**: reescribir la sección DoD con la verdad verificada (sin sobredeclaraciones). Cambiar claims medibles a números exactos: `39/39 OK`, `5/5 PASS`, `exit=0`. Mover ítems sin evidencia a una sección explícita **DEFER firmado** con trigger para re-validar.
5. **Regenerar artefactos de integridad**: SHA-256 maestro, listado de JARs, scripts de verificación reproducibles. Un script "regenerate + self-check" debe detectar su propio bug (e.g. `cd` relativo mal resuelto).
6. **Validación reproducible end-to-end**: ejecutar todos los comandos del handoff y comparar contra los números declarados. Si un número no cierra, NO aceptar el pase.
7. **Commit consolidado único** con mensaje que mapee cada blocker a su fix y la evidencia correspondiente. No múltiples commits chicos para un fix-pack (rompe trazabilidad).
8. **Status del gate sigue `review`**: el pase cierra blockers, no promueve. La promoción es responsabilidad del owner.

## Validación

- `git diff --stat` muestra sólo cambios del fix-pack + docs/handoffs.
- Working tree sin archivos untracked ajenos al fix (los ajenos se documentan pero no se commitean).
- El handoff actualizado tiene sección **DEFER firmado** para los ítems que el implementador no puede cerrar.
- El veredicto del owner, leído de nuevo, debe quedar sin blockers abiertos.

## Rollback / recuperación

- Si un comando del handoff actualizado no cierra: revertir el último cambio del fix (`git checkout -- <archivo>` o `git revert HEAD`), no destructivo sobre el pase original (`b2848d7` en este caso).
- Si se descubre que un cambio del fix-pack es incorrecto, NO se reescribe historia; se hace commit correctivo adicional referenciando el pase.
- Si el veredicto rechaza el pase de fix: el handoff queda `review`, se inicia un nuevo ciclo con el siguiente veredicto.

## Evidencia

- Pase aplicado: commit `5c186a3` sobre `b2848d7` (Fase 2 — EchoForgeTradeListExporter).
- Handoff: `specs/FEAT-SQX-METRICS-CONTRACT/phase2/G2_HANDOFF.md`.
- Proyecto: [[Echo Forge - Cierre de Etapa 4]] (nota actualizada con Bitácora F2 — pase de fix).