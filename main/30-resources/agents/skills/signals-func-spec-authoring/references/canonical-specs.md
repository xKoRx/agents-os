# Canonical SIG specs — patrón → ejemplo vivo

La fuente de verdad de "cómo se ve un spec funcional de Signals" es el **spec real en Spellbook**, no un template copiado. Lee el ejemplo vivo antes de escribir (`spellbook specs view <specId>`; el markdown está en `.content`). Mecánica completa en [`spellbook-access-runbook.md`](spellbook-access-runbook.md).

Los números `SIG-####` son estables; los UUID son lo que toman `view`/`edit`. Si un UUID deja de resolver, re-lista con `spellbook specs list SIG` y matchea por `specNumber` — nunca asumas que un spec desapareció por un ID cambiado.

> Estos ejemplos son de los referentes del equipo (dmuena, cmontecinos, fecaputo). Se mantiene re-listando, no copiando contenido: cuando el estilo evoluciona, el spec más nuevo de buena calidad de cada tipo pasa a ser la referencia — actualiza los IDs aquí en vez de editar prosa en la skill.

| Patrón que estás escribiendo | Lee este | specNumber | UUID |
|------------------------------|----------|:----------:|------|
| **Feature spec / fix conciso (ES)** — root cause + tabla RF-N con Prioridad + CA-N. El molde canónico y testeable | Fix de idempotencia en config de componentes | SIG-543 | `de42936b-424c-4e4a-96f2-9a679875cc01` |
| **Feature spec con E2E (ES)** — US-N + Business Rules en prosa + E2E-N en Gherkin (Dado/Cuando/Entonces) | Migración Kafka Express | SIG-263 | `074d3ff3-662f-4404-b5fe-296362a66b5b` |
| **Doc de diseño interno / plomería (EN)** — Problem → Scope → Handler flow con pasos `[1]…[4]` → Idempotency; sin US/CA | Component Runtime State Change | SIG-448 | `8c547334-e986-47c5-bd09-63f090a87bcd` |
| **Cambio de contrato chico (ES)** — un RF, un payload de ejemplo, impacto por app | Entity Relations — Deploy al Control Plane | SIG-541 | `ed67e9ff-4402-4301-bd1d-d54471e5c7a9` |
| **Plan de ejecución por fases (ES)** — secciones numeradas 1-6, Decisiones tomadas, Rollback, mermaid | Update / Force Deploy de componentes en RIO | SIG-582 | `839aaba4-1358-4a6b-83e6-69e3c2406344` |
| **Spec chico por fases + decisiones (ES)** — Objetivo/Contexto → Decisiones → Fase 1-3 por release → Rollback | rio-sdk-events: módulo de idempotency | SIG-210 | `345a5065-d4cf-4f63-8958-6de20a6ee719` |
| **Epic / RFC arquitectónico (EN)** — Summary→Context→Goals/Non-Goals→Proposed Design→Alternatives→Risks→Milestones; YAML front matter con related_sigs | EPIC - ClickHouse Connectors for RIO | SIG-527 | `fe30d869-70a6-4ac9-b8de-c046ba6c87fb` |
| **Epic-como-template (EN)** — Part 1 (problema+reglas arquitectónicas) + Part 2 (template de spec hijo) + Appendix con decision tree | External Configuration Consolidation | SIG-364 | `b5e946f7-ba44-4059-bc23-41ae37764357` |
| **Epic de planificación / OKR (EN)** — O1/O2/O3 con Key Results + KPIs semanales + out-of-scope del quarter | Playmaker + ControlPlanes OKR Q3 | SIG-323 | `ac79602f-76d8-4370-98b0-61285c9cfa69` |
| **Epic de migración multi-fase (EN)** — Phase 0…6 con semanas, Key file paths, Rollback | Migración Materializer → Playmaker | SIG-117 | `dadc0bdf-1d01-4288-b771-286e73ad9d2c` |

## Qué tomar de cada uno

- **SIG-543 (dmuena)** — el feature/fix como debe leerse: front-matter en negritas (`**Estado:** / **Fecha:** / **Dueño:**`), un párrafo de root cause que nombra el código (`isSameAsLatestConfig`), una tabla `| # | Requisito | Prioridad |` con `RF-N` (Debe/Podría), `CA-N`, y `## Fuera de Alcance`. Mínima ceremonia, alta señal. **Es el molde por defecto para un feature.**
- **SIG-263 (dmuena)** — cómo sumar escenarios verificables: `### US-N` con Como/quiero/para + Acceptance Criteria, y `### E2E-N` en Gherkin español (`**Dado** / **Cuando** / **Entonces**`). Las reglas de negocio van como sección en prosa, **no** como `BR-N`.
- **SIG-448 (dmuena)** — cuando el spec es plomería interna (no cara a usuario): baja a Problem → Scope → Handler Flow con pasos numerados → Idempotency → New Components, sin US/CA. Diseño técnico funcional, conciso.
- **SIG-541** — prueba de que chico está bien: un RF, un payload, impacto por app. Para cambios de contrato, no features.
- **SIG-582 / SIG-210 (cmontecinos)** — el plan de ejecución: sección firma **`## Decisiones tomadas`** (decisiones no-negociables con trade-offs), plan **por fases** (`Fase 1 — … (release X)`), y **`## Rollback`** explícito. SIG-582 además usa secciones numeradas jerárquicas (`## 4. Diseño V1` → `### 4.3.1`) y **mermaid**.
- **SIG-527 (fecaputo)** — el RFC canónico: YAML front matter con `related_sigs`/`related_source`, y `Summary → Context → Problem/Motivation → Goals → Non-Goals → Proposed Design → Alternatives Considered → Open Questions → Risks → Success Metrics → Milestones`.
- **SIG-364 (fecaputo)** — el epic que **genera specs hijos**: Part 1 (problema + reglas arquitectónicas + naming) y Part 2 (template de spec hijo con instrucciones de generación) + Appendix con decision tree.
- **SIG-323 (fecaputo)** — planificación por objetivos: `## O1/O2/O3` con `### Key Results` + `### KPIs to track weekly` + `## What's explicitly out of Q3 scope`.
- **SIG-117 (cmontecinos)** — migración multi-fase: `Phase 0…6` con semanas, `## Key file paths (single source of truth)` anclando al código real, y Rollback.

## Notas de convención (de estos 9 specs reales)

- Identificadores del equipo: **`US-N`, `RF-N`, `CA-N`, `E2E-N`**. Nadie numera `BR-N` ni `SEC-N`; "Business Rules" aparece como sección en prosa. `RF-N` va en tabla con columna **Prioridad** (`Debe`/`Podría`).
- Idioma: **ES para feature specs**, **EN para epics/RFCs y design docs**. Prosa ES con headings EN es común y aceptado.
- Longitud correlaciona con el **tipo, no la calidad**: feature specs buenos = cortos (3-14k); epics = largos por naturaleza (20-24k). No infles un feature para que parezca riguroso.
