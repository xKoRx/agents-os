---
created: "2026-09-20"
updated: "2026-09-20"
tags:
  - area/personal
  - kind/roadmap
---

# Loom — Continuidad y próximos pasos

**Proyecto padre:** [[Loom]]  
**Decisión del owner (2026-09-20):** pausar el desarrollo de Loom durante un período indeterminado. Esta nota conserva la continuidad para retomar sin repetir research ni confundir una POC certificada con una función habilitada en producción. **No asignar fecha de reanudación ni iniciar agentes automáticamente.**

> [!important] Punto de reentrada
> **Primero, integrar F3 en una RC de producto sobre fixtures; no empezar por G4 ni por nuevas funcionalidades.** Cuando se retome, recuperar el HEAD remoto real, el estado de los worktrees, la documentación y las autorizaciones vigentes. La existencia de esta nota NO autoriza escritura sobre el vault real, merge a `master`, cierre de Reviews humanas ni uso corporativo.

## 1. Estado congelado al pausar

| Entrega | Estado conocido | Referencia |
| --- | --- | --- |
| Loom v0.6 | Rama publicada, aplicación normal **read-only**, sin merge a `master` | `xKoRx/loom` · `feature/loom-v06 @ 36c760cc9d124ef8522aa10ab91852e1fcac334b` |
| F3 writer endurecido | POC de filesystem y recuperación, aislada del binario productivo | `feature/f3-writer-poc @ 593f656d97b09a8e1b68279ecca9c76f6c4c153d` |
| F3 G1/G2 | Watcher real y API de operaciones, en laboratorio aislado | `feature/f3-integration-lab @ 62943d46fe97612043111a72524b91251c3bb68c` |
| F3 G3 | Today interactivo sobre vault **sintético**; 5 operaciones y E2E reportados | `feature/f3-ux-lab @ 47cbadb8e3e46cda85ccac776fc6de767338bc44` |
| F3 idempotencia | Ledger de request IDs lado servidor, L01–L21 y auditoría reportados; laboratorio, **no producto** | `feature/f3-idempotency-gate @ 04a3ae80b9eaacd4165e1989a21246c9bc2d8898` |
| F3 Product Integration | **Mandato definido, no implementado ni certificado a esta fecha** | Rama propuesta `feature/f3-product-integration` (comprobar su existencia cuando se retome) |

**Autoridades de implementación:** `specs/FEAT-F3-HARDENING/RESULTS.md`, `specs/FEAT-F3-INTEGRATION/{INTEGRATION-CONTRACT,RESULTS}.md`, `specs/FEAT-F3-UX-LAB/RESULTS.md`, `specs/FEAT-F3-IDEMPOTENCY/RESULTS.md` en las ramas correspondientes de `xKoRx/loom`. Los PASS y las mediciones de los agentes son evidencia de esas entregas: la integración productiva todavía requiere gates propios sobre su SHA definitivo.

**Restricciones vigentes:** Markdown/Agents-OS es la autoridad; índice derivado; binario normal sin endpoints POST de F3 ni `--allow-write-plan`; v0.6 y `master` sin merge; las Reviews humanas de versiones anteriores no se cierran automáticamente. La política de MELI y la separación de vaults personal/corporativo son una decisión aparte: no inferir aprobación corporativa por tener una aplicación propia.

## 2. NEXT STEP ejecutable — F3 Product Integration RC

**Prioridad de reanudación: primera. Estado: pendiente; NO iniciado.** Recuperar la rama idempotente como baseline, inspeccionar commits remotos reales y construir `feature/f3-product-integration` en worktree aislado. Reutilizar writer, ledger, adaptador de watcher, API y Today ya implementados; no reconstruirlos. Entregar un producto integrado que **arranque read-only por defecto** y cuya certificación de escritura se ejecute exclusivamente sobre un vault sintético registrado. No permitir que esta RC escriba en el vault real.

Gates imprescindibles:

1. **Seguridad HTTP local:** bind loopback, validación de Host/Origin, protección CSRF en mutaciones, Content-Type estricto, CORS no permisivo, errores sin rutas sensibles. Un sitio remoto no puede activar ni accionar la escritura por apuntar a localhost.
2. **Autorización y aislamiento:** activación explícita en laboratorio, máquina+vault registrados, default OFF, rechazo de cualquier vault no autorizado; no basta con un parámetro de URL. Mantener separadas identidad del vault, identidad del servidor y scope de las cinco operaciones permitidas.
3. **Estado transaccional:** ledger durable, requestId estable, confirmación por snapshot y post-hash, pending/conflict/recovery visibles, reinicios y reintentos sin doble aplicación. Política de `LedgerRetention` que cubra toda la ventana de retries admitida.
4. **Threat model del StateDir:** el auditor demostró que JSON válido falsificado por un actor que puede escribir el StateDir permite éxito ficticio. Definir adversarios y permisos efectivos; si se requiere defenderse de ese actor, incorporar una raíz de confianza realmente independiente o declarar BLOCKED. Un MAC con clave accesible al mismo adversario no resuelve el problema.
5. **Certificación sobre binario integrado:** matrices F3, G1–G3 y L01–L21, crash/recovery, race, ataques de origen hostil, E2E Chromium, integridad en tres capas (archivo/snapshot/journal), dark/light y validación de rechazo en modo OFF. Auditor independiente sobre el SHA FINAL, no transferir mecánicamente un PASS de laboratorio.

**Resultado requerido:** `PRODUCT_RC_READY / PARTIAL / BLOCKED`, SHA y rama remota, matriz de gates y evidencia, riesgos residuales, comando para probar contra fixtures, sin merge ni modificación del vault real. Conservar la separación de permisos: integrar código y autorizar escritura en documentos reales son decisiones distintas.

### Después de la RC, en este orden

- **Aceptación UX real read-only:** probar v0.6/RC en el vault personal sin escrituras: Home, Actions, Projects, Collections, Resume y Today; comprobar utilidad, densidad, enlaces y evidencia. Conservar las tareas puente humanas en Review hasta aceptación explícita.
- **Ensayo en copia independiente del vault:** si el owner lo autoriza, usar copia aislada con backup externo verificable, hashes, rollback y re-certificación de filesystem/índice/API/UI en el binario real. No presentar una copia como si fuera el vault productivo.
- **G4 — ensayo sobre vault real:** únicamente mediante una autorización nueva, específica y explícita del owner, después de cerrar la integración y los hallazgos bloqueantes, con backup externo comprobado, ventana de reversión, política de conflictos y monitoreo. Esta nota **no** otorga esa autorización; G5 tampoco es automático.

## 3. Roadmap de producto posterior a F3

La investigación de producto compartida el 2026-09-20 estudiaba Loom **v0.4**, de modo que su backlog se reconcilia con el estado posterior antes de planificar. **Ya implementados:** Human Action Center, Project Command Center y Resume Context en v0.5; cuatro Smart Collections (Architecture, Runbooks, Decisions, Project Knowledge) en v0.6. Today con escritura funciona por ahora **solo en laboratorio**. No abrir tickets para rehacer estas funciones.

### v0.7 — Knowledge & Portfolio (propuesta, no aprobada para ejecución)

- **Knowledge Explorer:** panel contextual por nota/proyecto con backlinks, relaciones verificadas, ADR/decisiones, recursos y documentos pertinentes; reutilizar índice, grafo y Smart Collections. Resolver ambigüedades explícitamente y enlazar al Markdown fuente. No crear otro Graphify, vector DB, LLM ni segunda autoridad.
- **Portfolio Insights:** visión transversal de proyectos en foco con progreso *documentado*, blockers, tareas puente humanas en Review y proyectos sin próxima acción explícita. Indicadores calculados diferenciados de estado documental, con denominador y procedencia visibles; no inventar estados de ejecución ni puntajes arbitrarios.
- **Continuidad de sesiones:** extender Resume Context con la última ejecución **documentada** (mandato, SHA, entrega, evidencia, gates y residuales) relacionada con el proyecto; no confundirla con proceso agente activo ni inventar actividad. Reutilizar notas `agent_run`/bitácora existentes, sin nuevo orquestador.

**Criterio de cierre v0.7:** navegación útil desde Home → proyecto → conocimiento/última entrega → fuente en ≤2–3 interacciones habituales; fixtures de relaciones ambiguas, datos faltantes y eventos desactualizados; pruebas funcionales y visuales. Ajustar el alcance antes de rebajar gates.

### v0.8 — Temporal & Review (posterior; requiere contratos de historial)

- **Change Feed + Weekly Review como un mismo sistema:** qué cambió, qué se cerró, bloqueos nuevos, decisiones, compromisos arrastrados y vínculos a la evidencia.
- **Precondición:** definir origen, persistencia, identidad y límites del historial de snapshots/eventos. `mtime`, orden textual de bitácora o último commit por sí solos NO demuestran un cambio semántico, una ejecución activa ni un hito. No presentar datos históricos incompletos como exhaustivos.

### Backlog diferido (sin compromiso)

- Agent Run Explorer más completo: historial documental de mandatos, entregas, SHAs y gates; puede partir de la continuidad v0.7. Nunca representar tareas `[/]` como presencia o actividad real de un agente.
- Focus Reading y Saved Workspaces: mejoras pequeñas de UX, preferencia local, sin nueva arquitectura. Foco entre máquinas (F1) permanece diferido.
- Decision Explorer específico solo si el explorador de conocimiento y Decisions existente no cubren casos reales.
- Safe Capture/editor general: **otro proyecto/contrato de escritura**, no extensión tácita de F3; autorización, allowlist, concurrencia, recuperación y pruebas propias. F2 `daily_plan` sigue siendo propuesta de esquema, sin migración automática; F4 de tipos de tarea sigue diferido.

## 4. Decisiones y antiobjetivos

- Visión: **Notion para presentación, Obsidian para conocimiento y Agents-OS para continuidad/supervisión**, sin replicar sus plataformas completas.
- Home debe responder rápidamente: **qué requiere mi intervención, dónde quedaron los proyectos y cómo retomo**; no convertirla en inventario de todas las notas ni en 20 widgets.
- No reabrir F3 POC ni encargar nuevas funcionalidades antes de la RC; no paralelizar v0.7 con integración F3 si todavía hay bloqueos de seguridad o pruebas pendientes.
- No usar esta nota para cerrar automáticamente tareas puente `[r]`, cambiar el estado del padre a `done`, iniciar tareas programadas ni reservar tiempo de desarrollo.

## 5. Checklist de recuperación futura

- [ ] **Al retomar:** verificar `origin`/HEAD/worktrees en `xKoRx/loom` y comparar con el baseline `04a3ae8`; confirmar si existe ya la rama de integración. #owner/me #type/planning #area/personal
- [ ] Revisar la SPEC y las evidencias del laboratorio y registrar los riesgos que sigan abiertos antes de iniciar Product Integration. #owner/me #type/review #area/personal
- [ ] Autorizar por separado, si corresponde, el desarrollo de la RC y luego cualquier ensayo de escritura sobre copia/vault real. No inferir autorización de esta nota. #owner/me #type/decision #area/personal
- [ ] Tras Product RC y aceptación humana, abrir un subproyecto ejecutable para v0.7; solo entonces congelar SPEC, fixtures y work packages. #owner/me #type/planning #area/personal

**Última decisión:** proyecto en pausa, continuidad documentada; próximo trabajo técnico = F3 Product Integration RC sobre fixtures, NO G4 real ni v0.7 todavía.
