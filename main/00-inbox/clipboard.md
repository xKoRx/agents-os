Voy a empezar resolviendo el bootstrap canónico de Agents-OS y leyendo las fuentes autorizadas del proyecto.

Bootstrap cold start: cargo la base (constitución, perfil global, continuidad, registro de skills y router de dominio) en paralelo.

Bootstrap: entidad = [[Polymarket Engine]] (área Personal → sin router de dominio, DEFAULT). Cargo el perfil global y la skill de project workflow, y localizo el documento del proyecto.

Bootstrap resuelto. Entidad: [[Polymarket Engine]] · Objetivo: plan M2 TOP sobre diseño frozen · Skill: agents-os-agent-project-workflow · Router de dominio: ninguno (DEFAULT). Ahora leo completo el documento del proyecto (1590 líneas).

He leído la primera mitad del proyecto (foundation, M1.0–M1.6). Continúo con el resto del documento.

Continúo con M1.12 en adelante (auth, observabilidad, gates, cierre ASTRA-3).

He leído el proyecto completo (M1.0–M1.17, F.1–F.9, cierre ASTRA-3). Ahora leo el índice del Technical Platform Map para referenciar las partes TPM en los slices.

He leído todas las fuentes autorizadas: proyecto completo (M1.0–M1.17, FABLE F.1–F.9, cierre ASTRA-3), índice del TPM y su notación de partes. Ahora redacto la sección `## M2 — TOP Implementation Plan` dentro del documento del proyecto. Empiezo con baseline, paquetes Go y orden de dependencia.

Base del plan escrita (M2.0–M2.2). Ahora agrego los slices M2-S01 a M2-S05.

Slices S01–S05 agregados. Continúo con S06–S10 (market data, frames, replay, strategy runtime, economics/simulator).

Continúo con S11–S13 (account/risk, supervisor/backup, experiments/shadow) y la sección de paralelismo.

Último bloque del plan: estrategia de tests/mapa de gates, política de entrega a NORMAL, hitos, frontera M4, decisiones operativas y checklist de calidad.

Plan completo en el documento. Ahora actualizo el estado del proyecto: Estado actual, tarea TOP y Bitácora.

Verificación final de integridad del documento antes de reportar.

STATUS: `M2_PLAN_READY_FOR_MANAGER_REVIEW`

PLAN:
- major slices: 13 (M2-S01 Foundation → S02 Protocol/fixtures → S03 Capture+Persist → S04 Catalog → S05 Regimes → S06 WS+Books → S07 Frames → S08 Replay → S09 Strategy/SCREEN → S10 Economics+Simulator → S11 Account+Risk → S12 Supervisor/Obs/Backup-Restore → S13 Experiments/Shadow/Certificación), cada uno con plantilla completa (scope, contratos, persistencia, concurrencia, fallos, tests, gates, DoD, handoff)
- milestones: M3-A Protocol & Durable Data Foundation · M3-B Market Data + Recorder + Replay · M3-C Runtime + Simulator + Account + Ops · M3-D Shadow Research Engine · M3-E Certification readiness
- parallel groups: A = S02 ∥ S03; barrera; B1 = S06→S10 (cadena) ∥ B2 = S11; barrera de integración B1×B2; final secuencial S12→S13, con rangos de migraciones disjuntos por slice
- critical path estimado: 11 slices

COVERAGE:
- FOUNDATIONAL NOW: 100% mapeado a slices (verificación ítem por ítem en M2.10 del plan)
- deferred: todo lo de la columna IMPLEMENT LATER queda como contrato + stub `DISABLED` deny-all verificado por G-15/G-12b; sin fake implementations
- gates mapped: G-01…G-15 y G-02b/05b/06b/07b/09b/10b/10c/11b/12b/13b/15b con fixture/acción/esperado/FAIL/evidencia en M2.5; G-16…G-19 y G-14b quedan explícitos NOT_RUN / IMPLEMENT LATER

OWNER:
- repo/path decision: nombre `xKoRx/polymarket-engine` ya acordado; falta `REQUIRES_OWNER — REPO LOCATION ONLY` (path local del clone; propuesta `~/code/xKoRx/polymarket-engine`, fuera del vault). Única decisión previa a S01
- other decisions required: ninguna bloqueante; decisiones operativas de TOP (driver `modernc.org/sqlite`, `shopspring/decimal`, `pgregory.net/rapid`, `gorilla/websocket`, TOML, toolchain pin) reversibles y objetables en la revisión

RISKS:
- implementation risks identificados: rendimiento del driver pure-Go SQLite y fsync tail (se mide en G-09b/G-13; reemplazo encapsulado sin rediseño); S11 (account) es el slice más denso — su contraste con B1 lo protege; `REQUIRES_OWNER` del path puede demorar el arranque si no se resuelve antes de la primera asignación NORMAL
- `BLOCKED — DESIGN ISSUE`: ninguno. No encontré contradicción arquitectónica material entre el mandato y M1 frozen

NEXT: manager review del plan en el proyecto → M2 freeze → asignaciones NORMAL por slice según M2.4/M2.6. Editado únicamente `Polymarket Engine — MVP.md` (estado, tarea TOP y bitácora incluidos); sin código, sin SPECs, gates físicos `NOT_RUN`, live deshabilitado.s