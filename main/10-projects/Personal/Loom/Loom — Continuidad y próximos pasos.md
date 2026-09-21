---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Loom]]"
  - "[[Loom — Banco de ideas de producto]]"
aliases: []
tags:
  - kind/doc
  - area/personal
created: "2026-09-20"
updated: "2026-09-20"
---

# Loom — Continuidad y próximos pasos

## Propósito

**Proyecto padre:** [[Loom]]. **Decisión del owner (2026-09-20): pausar desarrollo por un período indeterminado.** Conservar punto de reentrada, restricciones, SHAs y roadmap sin repetir research ni confundir POC certificada con producto habilitado. No asignar fecha de reanudación ni iniciar agentes automáticamente.

> [!important] Punto de reentrada
> **Primero, integrar F3 en una RC de producto sobre fixtures; no empezar por G4 ni por nuevas funcionalidades.** Al retomar: descubrir HEAD remoto y worktrees reales, cotejar documentos y confirmar permisos. Esta nota NO autoriza escritura sobre vault real, merge a `master`, cierre de Reviews humanas ni uso corporativo.

**Ideas de producto preservadas sin pérdida:** [[Loom — Banco de ideas de producto]] (inventario de las 13 propuestas originales, estado implementado/propuesto/diferido, v0.7/v0.8, criterios y dependencias). **Feedback del cierre:** `80-agents/journal/feedback/system-1/2026-09-20-loom-continuity-session-feedback.md`. Este documento es la puerta de entrada operativa; el banco es el detalle de producto y ninguno sustituye a [[Loom]] como proyecto canónico.

## Contenido

### 1. Estado congelado al pausar

| Entrega | Estado conocido | Referencia |
| --- | --- | --- |
| Loom v0.6 | Rama publicada, aplicación normal **read-only**, sin merge a `master` | `xKoRx/loom` · `feature/loom-v06 @ 36c760cc9d124ef8522aa10ab91852e1fcac334b` |
| F3 writer endurecido | POC de filesystem/recuperación, aislada del binario productivo | `feature/f3-writer-poc @ 593f656d97b09a8e1b68279ecca9c76f6c4c153d` |
| F3 G1/G2 | Watcher real y API de operaciones en laboratorio aislado | `feature/f3-integration-lab @ 62943d46fe97612043111a72524b91251c3bb68c` |
| F3 G3 | Today interactivo sobre vault **sintético**; cinco operaciones/E2E reportados | `feature/f3-ux-lab @ 47cbadb8e3e46cda85ccac776fc6de767338bc44` |
| F3 idempotencia | Ledger servidor de request IDs, L01–L21/auditoría reportados; laboratorio, **no producto** | `feature/f3-idempotency-gate @ 04a3ae80b9eaacd4165e1989a21246c9bc2d8898` |
| F3 Product Integration | **Mandato definido; NO implementado ni certificado a la fecha de pausa** | Rama propuesta `feature/f3-product-integration` (verificar si existe al retomar) |

**Autoridades:** `specs/FEAT-F3-HARDENING/RESULTS.md`, `specs/FEAT-F3-INTEGRATION/{INTEGRATION-CONTRACT,RESULTS}.md`, `specs/FEAT-F3-UX-LAB/RESULTS.md` y `specs/FEAT-F3-IDEMPOTENCY/RESULTS.md`, cada archivo en la rama correspondiente de `xKoRx/loom`. Los PASS de los agentes son evidencia de laboratorio; la integración requiere gates propios sobre su SHA FINAL.

**Restricciones vigentes:** Markdown/Agents-OS autoridad, índice derivado, binario normal sin endpoints POST F3 ni `--allow-write-plan`; v0.6 y `master` sin merge; Reviews humanas anteriores no se cierran por entrega técnica. Política MELI y separación de vaults personal/corporativo requieren verificación independiente.

### 2. NEXT STEP ejecutable — F3 Product Integration RC

**Primero al reanudar; pendiente, NO iniciado.** Recuperar la rama idempotente como baseline, inspeccionar commits remotos y crear `feature/f3-product-integration` en worktree aislado. Reutilizar writer, ledger, watcher, API y Today existentes; no reconstruir POC. Entregar binario integrado que arranque **read-only por defecto**, cuya certificación de escritura se haga exclusivamente sobre vault sintético registrado. Esta RC NO puede escribir en el vault real.

Gates:

1. **Seguridad HTTP local:** bind loopback, Host/Origin validados, protección CSRF, Content-Type estricto, CORS no permisivo y errores sin rutas sensibles; una web remota no puede accionar localhost por sí misma.
2. **Autorización y aislamiento:** activación explícita solo en laboratorio, máquina+vault registrados, default OFF, rechazo de cualquier vault no autorizado y scope limitado a cinco operaciones; URL/parámetro no concede permisos.
3. **Transacciones:** ledger durable/requestId estable, confirmación por snapshot + post-hash, pending/conflict/recovery visibles; reinicio/retry no duplica, `LedgerRetention` ≥ ventana de retries admitida.
4. **Threat model de StateDir:** auditor demostró éxito ficticio mediante JSON válido forjado por actor con escritura en StateDir. Definir adversarios y permisos; si ese actor está dentro del modelo, raíz de confianza independiente o `BLOCKED`. MAC cuya clave posee el mismo adversario no protege.
5. **Certificación productiva:** matrices F3, G1–G3, L01–L21, crash/recovery, race, origen hostil, E2E Chromium, tres capas archivo/snapshot/journal, dark/light y modo OFF. Auditor independiente sobre SHA integrado; no transferir PASS de POC automáticamente.

**Resultado requerido:** `PRODUCT_RC_READY / PARTIAL / BLOCKED`, SHA/remoto, evidencia y riesgo residual, comando de fixtures, sin merge ni edición del vault real. Integrar código y autorizar escrituras reales son decisiones diferentes.

#### Después de RC, secuencia separada

- **Aceptación UX real read-only:** probar Home, Actions, Projects, Collections, Resume y Today sobre vault personal exclusivamente en lectura; comprobar utilidad, enlaces y procedencia; puentes humanos permanecen Review hasta aceptación explícita.
- **Ensayo sobre copia independiente:** solo con autorización del owner; copia aislada, backup externo verificable, hashes, rollback y re-certificación de filesystem/índice/API/UI sobre binario real. No es ensayo sobre el vault productivo.
- **G4 en vault REAL:** requiere nueva autorización específica y explícita, integración/seguridad certificadas, backup externo probado, ventana de reversión y política de conflictos. Esta nota no concede autorización; G5 tampoco es automático.

### 3. Roadmap posterior — resumido (detalle completo en [[Loom — Banco de ideas de producto]])

La investigación original partía de **v0.4**; reconciliar contra versión vigente. **Ya implementados:** Human Action Center, Project Command Center y Resume Context en v0.5; Smart Collections Architecture/Runbooks/Decisions/Project Knowledge en v0.6. Today de escritura, solo laboratorio. No programar duplicados.

**v0.7, propuesta (no autorizada): Knowledge & Portfolio.** Knowledge Explorer contextual por nota/proyecto, backlinks/decisiones/recursos desde índice y grafo existentes; Portfolio Insights transversal con evidencia, progreso documentado, bloqueos y acciones humanas; Resume Context ampliado con última ejecución documentada (mandato, SHA, gates, evidencia, siguiente paso), jamás procesos supuestamente activos. Navegación habitual Home→proyecto→documento/evidencia en 2–3 interacciones; pruebas de ambigüedad, stale, vacíos y dark/light; no inventar relaciones ni métricas.

**v0.8, propuesta posterior: Temporal & Review.** Change Feed + Weekly Review como un sistema; antes definir historial persistente de eventos/snapshots, identidad, temporalidad, retención y límites de cobertura. `mtime`, bitácora o último commit solos NO prueban cambio semántico. Habilitar `Recently Updated` solo con procedencia temporal fiable.

**Backlog diferido:** Agent Run Explorer completo (historial documental ≠ proceso vivo); Focus Reading y Saved Workspaces browser-local (F1 sincronización deferred); Decision Explorer si Knowledge Explorer + Decisions no bastan; Safe Capture/editor genérico como contrato de escritura separado de F3 y con autorización nueva; F2 `daily_plan` sin migración automática y F4 tipología diferidos. Inventario de las **13 ideas sin omisiones** en [[Loom — Banco de ideas de producto]].

### 4. Decisiones y antiobjetivos

- Visión: **Notion presentación, Obsidian conocimiento, Agents-OS continuidad y supervisión**, sin replicar plataformas completas.
- Home responde qué necesita intervención, dónde quedaron proyectos y cómo retomo; no 20 widgets ni inventario del vault.
- No reabrir F3 POC, paralelizar v0.7 con bloqueos de integración ni otorgar autoridad de escritura por inferencia.
- No cerrar puentes `[r]`, mover parent a Done, iniciar agentes programados ni reservar desarrollo automáticamente. Esta nota documenta pausa, no cierre del proyecto.

### 5. Checklist de recuperación futura

- [ ] Al retomar: comprobar `origin`/HEAD/worktrees reales y comparar con baseline `04a3ae8`; confirmar si Product Integration ya existe. #owner/me #type/planning #area/personal
- [ ] Releer SPEC y hallazgos abiertos, validar qué gates siguen pendientes; consulta [[Loom — Banco de ideas de producto]] para no perder ideas ni duplicar v0.5/v0.6. #owner/me #type/review #area/personal
- [ ] Autorizar separadamente, si corresponde, trabajo de RC, ensayo en copia y más tarde G4 real; no inferir permisos de esta nota. #owner/me #type/decision #area/personal
- [ ] Solo después de Product RC y aceptación humana, crear subproyecto de v0.7 con SPEC/fixtures/work packages; v0.8 después de contrato histórico. #owner/me #type/planning #area/personal

**Última decisión:** Loom en pausa; próxima tarea técnica = F3 Product Integration RC sobre fixtures; G4 en vault real y expansión v0.7 no autorizados. Véase [[Loom — Banco de ideas de producto]] para preservar la visión íntegra.