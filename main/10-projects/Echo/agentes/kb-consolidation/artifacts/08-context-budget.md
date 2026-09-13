---
agent: context-budget-auditor
role: Context Budget & Leak Audit
task_id: KBC-J
status: COMPLETE
baseline: vault e3e34ab2 · echo f7ddea18 · symphony 9fad768c
inputs: wiki publicada (30-resources/applications/echo/), índices (applications/00-index, runbooks/00-index, skills/INDEX), memory (80-agents/memory), skills, repos RO
scope: auditoría read-only de context budget y leakage
started_at: 2026-09-13T02:41-03:00
updated_at: 2026-09-13T02:50-03:00
---

# 08 — Context Budget & Leak Audit (KBC-J)

## Assignment

Auditar la economía de contexto tras la publicación del subdominio `30-resources/applications/echo/`: duplicación Echo/Forge, stale docs aún discoverable, deprecated en hot path, costo AGENTS.md de repos, hechos globales repetidos, routing cost, project state en resources, frontera skill/runbook/resource, y leakage MELI/ARANEA/DEFAULT. Output único: este artifact. READ-ONLY salvo este archivo; sin subagentes; sin cambios a skills ni permisos.

## Baseline

- Vault `e3e34ab2` (sync posterior a publicación KBC, commits 01:56–02:08); echo `f7ddea18` (branch e02, master a99f9a63); symphony `9fad768c` (branch f04, master 0b9742b0, dirty → sólo lectura).
- Hot path cold start medido (líneas): AGENTS.md 11 · constitución 119 · perfil global 74 · continuidad global 45 · skills INDEX 112 · bootstrap 166 → ~527 líneas ≈ 4.5–5.5k tokens, dentro del target 3–6k.
- Always-load real en frontmatter: exactamente 3 (constitución, rjara-agent-profile, agents-os-operating-continuity) + SKILL.md de bootstrap. Los matches `load_policy: always` en journal/logs son citas de texto, no policies. Club cerrado verificado.
- Wiki Echo: 20 notas, 4,985 líneas totales; canónicas activas (echo-core 69, echo-forge 84, boundary 69, índice 79) están livianas; el peso (≈4,300 líneas) vive en 6 contratos frozen + 5 históricos en retención, no enlaces en hot path.

## Findings

### F1 — Perfil always-load duplicado y snapshot de distribución indexables dentro del árbol vivo
- Evidencia: `30-resources/agents-os/core-export/dist-files/80-agents/memory/public/user-preference/agent-profile.md` (declara `load_policy: always`, `indexable: true`, `index_priority: critical`, perfil genérico 2026-09-09 distinto del real) y `30-resources/agents-os/core-export/dist-files/` (11 archivos que replican AGENTS.md, índices y notas); `30-resources/agents-os/chatgpt-pack/PROJECT-STATE.md` (context_pack del proyecto AGENTS OS, snapshot 2026-08-10, `source_of_truth: false`).
- Impacto: un segundo perfil "always" en superficie indexable; retrieval/Graphify no distingue dist de vida; riesgo de que una query de perfil entregue el genérico stale en vez del real (~1–2k tokens de lectura incorrecta antes de detectar el error). PROJECT-STATE es estado de proyecto viviendo en resources.
- Autoridad: bootstrap Hard Rules (un solo perfil always bajo `user-preference/`); constitución regla 5 (una fuente por hecho) y frontera Sistema 1/2 (estado en proyectos).
- Consolidación recomendada: los dir `core-export/dist-files/` y `chatgpt-pack/` son artefactos de distribución, no recursos canónicos; deben ser no-indexables (y el estado del pack, referenciado desde el proyecto AGENTS OS, no duplicado en resources).
- Acción segura: fase K marca `indexable: false` + `load_policy: manual` en los dist-files (o mueve el pack fuera de `30-resources/`); verificar con `agents-os-doctor`. No borrar (pertenecen al pipeline de distribución).

### F2 — Credenciales en claro repetidas en 4 superficies (incluye private key SSH en el vault)
- Evidencia: `xKoRx/symphony: AGENTS.md:47` (password `cascada123` + inventario workers) · `xKoRx/symphony: .agents/skills/worker-troubleshooting/SKILL.md:21-41` (mismo password repetido ~10 veces) · `80-agents/tools/echo-forge-worker-access/credentials.env` (1,132 bytes) + `echo-forge-worker` (4,691 bytes, private key SSH) · `30-resources/APIs.md` (API keys z.ai y minimax en claro).
- Impacto: el password viaja como always-on en toda sesión de symphony (53 líneas de AGENTS.md) y queda expuesto en git history; la private key y las API keys viven dentro del vault sincronizado. Mayor blast radius de la auditoría (seguridad + economía: credenciales no aportan contexto, lo contaminan).
- Autoridad: constitución invariante 9 (no persistir secretos); planner ya lo flagueó al owner en fase I.
- Consolidación recomendada: secret store único; AGENTS.md y skills referencian "resolver credencial desde el gestor autorizado", nunca el valor.
- Acción segura: fase K sólo documenta y repite el flag al owner (rotación + remediación repo-side son patches del owner; repos y `credentials.env` READ-ONLY para la campaña).

### F3 — AGENTS.md de echo usa `file:///Users/rjara/...` (paths de máquina muertos)
- Evidencia: `xKoRx/echo: AGENTS.md` (33 líneas) — las 6 referencias de la tabla topográfica (CONSTITUTION.md, `.agents/rules/`, `.agents/skills/`, `.agents/workflows/`, `specs/`, `specs/SPECS.md`) son `file:///Users/rjara/go/...`; el repo corre en Linux (`/home/kor/...`). Idéntico patrón en `xKoRx/symphony: AGENTS.md`.
- Impacto: router roto en la máquina real: todo agente que siga el entry point debe re-derivar cada path (búsquedas extra por sesión). 33–53 líneas con costo de routing alto y valor de navegación nulo tal como está.
- Autoridad: constitución invariante 11 (para repos externos, `repo + path relativo`).
- Consolidación recomendada: los drafts de `artifacts/07-agents-md-plan.md` (~40 líneas c/u) ya corrigen esto con paths relativos; el costo se elimina aplicando el patch.
- Acción segura: fase K no toca repos; registra que el patch 07 es la remediación y que incluye este defecto.

### F4 — Ensayo de 503 líneas como AGENTS.md anidado en echo (`vibe-coding/docs/cursor/`)
- Evidencia: `xKoRx/echo: vibe-coding/docs/cursor/AGENTS.md` — ensayo genérico "Arquitectura de Sistemas Multi-Agente Agnósticos" con citas académicas; 3,815 palabras, cero relación operativa con el repo. `artifacts/07-agents-md-plan.md` ya lo detectó y excluye de retrieval.
- Impacto: ~4k tokens always-on para cualquier agente que trabaje bajo ese subtree (Cursor resuelve AGENTS.md anidados); es el mayor costo unitario de contexto en los repos auditados.
- Autoridad: un AGENTS.md es router operativo, no ensayo (convención AGENTS OS; planner objetivo "AGENTS.md reducidos a routers efectivos").
- Consolidación recomendada: renombrar a doc no-mágico (p.ej. `docs/agnostic-agents-essay.md`) o archivar; decidir con owner (07 anota la suposición de que nadie lo usa).
- Acción segura: fase K documenta; el cambio es patch repo-side del owner.

### F5 — Skills INDEX subdeclara app-owned: 3 filas vs 21 skills reales en symphony
- Evidencia: `80-agents/skills/INDEX.md` ("App-owned: 3", filas sqx-plugin-lifecycle, echo-forge-wfm-troubleshooting, sqx-temporal-failure-audit) vs `xKoRx/symphony/.agents/skills/` con 21 directorios (worker-ssh, worker-troubleshooting, sqx-deployer, sqx-watcher, echo-forge-testing, sdd-*, go-static-validation, graphify, anti-test-masking-guard, etc.).
- Impacto: el INDEX es la base de routing del cold start; si el agente necesita una skill no listada debe escanear carpetas del repo (over-read) o la pierde. Defecto de descubrimiento demostrado (declara 3, hay 21), ya anotado en el planner como riesgo de fase I/J.
- Autoridad: INDEX es el registro curado ("enlaza, no copia"); constitución regla 4 (explorar con índice, no scans).
- Consolidación recomendada: corregir el conteo y agregar filas link-only (`repo + path relativo`, una línea por skill) para las 18 faltantes; sin copiar contenido.
- Acción segura: fase K puede editar `80-agents/skills/INDEX.md` — es defecto demostrado, no rediseño; con change_log por constitución regla 6.

### F6 — Inventario de workers SQX triplicado (AGENTS.md symphony ↔ runbook ↔ aranea)
- Evidencia: tabla Zeus/Hera/Kronos (FQDN, IPs) en `xKoRx/symphony: AGENTS.md:43-53` · `30-resources/runbooks/symphony-zeus-troubleshooting.md:44-75` · `30-resources/aranea/02-servicios/ml-ia.md:35-52` (+ topologia por nodo). Tres fuentes para el mismo hecho de infraestructura.
- Impacto: riesgo de drift (IP/FQDN cambiado en un lugar y no en otros); el AGENTS.md arrastra ~11 líneas de infra Aranea en toda sesión symphony.
- Autoridad: la infra cluster es conocimiento del dominio Aranea → `30-resources/aranea/` es la fuente canónica; runbooks y AGENTS.md deberían linkear.
- Consolidación recomendada: AGENTS.md symphony (tras patch 07) apunta a la página aranea; runbook symphony-zeus-troubleshooting mantiene su tabla operativa mínima o linkea.
- Acción segura: vault-side nada urgente (runbook es fuente válida de operación); repo-side via patch; fase K documenta la autoridad.

### F7 — Objetivos de proyecto con claim de integración Forge→Echo sin link a la frontera
- Evidencia: `10-projects/Echo Forge/Echo Forge.md` ("hasta el despliegue automático... e ingesta de finalistas en Echo Core vía API") y `10-projects/Echo Forge/agentes/Echo Forge - Etapas 8-10.md` ("API-first con Echo Core... mock server si los contratos reales no están cerrados" — superseded de facto por los contratos frozen). Ninguno enlaza `echo-forge-integration-boundary`.
- Impacto: un agente que lea el proyecto puede inferir integración vigente; las notas no afirman entrega en tiempo presente (el claim falso fue eliminado de la wiki), pero el routing queda stale. Bajo costo, riesgo de verdad.
- Autoridad: boundary page es el estado implementado; specs conceptuales FEAT-SQX-ECHO-INGESTION superseded de facto (G6).
- Acción segura: fase K agrega UNA línea con link a [[echo-forge-integration-boundary]] en el objetivo de `Echo Forge.md`; no reescribir bitácoras ni Etapas 8-10 (historia).

### F8 — Machine paths (`/home/kor`, `/Users/rjara`, `file://`) en ~40 notas históricas de memoria interna
- Evidencia: `80-agents/memory/internal/agent-memory/2026-07-15-sqx-watcher-remote-deployment.md`, `2026-07-07-sqx-robust-run-magic-mt5-flow.md`, `2026-07-06-sqx-sequential-logical-type-chunking.md`, `2026-07-17-vpp-review-overedit-continuity.md`, `2026-07-09-polycard-new-title-motors-continuity.md`, entre otras; también `30-resources/aranea/02-servicios/ml-ia.md:169` (source files históricos `/home/hermes/...`).
- Impacto: ~0 en hot path (notes `load_policy: manual`, sólo retrieval histórico); riesgo de que un path de máquina muerto entre por retrieval y cueste un read fallido. Pool: 114 notas en `agent-memory/`, 73 echo/forge-relacionadas.
- Autoridad: constitución invariante 11.
- Acción segura: NO retrolimpiar (historia; KISS). Regla vigente aplicada a notas nuevas; fase K no toca.

### F9 — Positivos verificados (sin acción)
- Club always cerrado: 3 notas + bootstrap; continuidad global compacta (45 líneas, sólo comportamientos); archive con `memory_state: superseded` correcto.
- Frontera cross-boundary sin duplicación: echo-core y echo-forge resumen en ≤1 sección y linkean la página boundary canónica; contratos linked, no copiados.
- Deprecated fuera del hot path: `30-resources/runbooks/signals-code-review.md` (superseded → `signals-code-review-runbook`) NO aparece en runbooks/00-index; preferencias Meli/Aranea/VPN con `when_area_loaded` (correctamente scoped).
- Índice applications: puntero único al subdominio (1 fila Echo + nota de delegación), 0 filas residuales duplicadas.
- Perfil global: mención Meli es identidad del usuario (1 línea, "Signals dueño de RIO"), no procedimiento de dominio; links a preferencias scoped. Neutral-aceptable.

## Priority Ranking

- **P0:** F2 (credenciales en claro + private key en vault y git history; ya flaggeado al owner — rotación urgente).
- **P1:** F4 (503 líneas always-on en subtree cursor), F1 (perfil always duplicado indexable), F3 (AGENTS.md repos con file:/// paths muertos), F5 (skills INDEX 3 vs 21).
- **P2:** F6 (inventario workers triplicado), F7 (claims de integración sin link a frontera).
- **P3:** F8 (machine paths en historia de memoria — no retrolimpiar).

## Scope Leakage Assessment

- **DEFAULT (always-load):** constitución + perfil + continuidad no contienen procedimientos de dominio. La línea de employer Meli en el perfil es identidad, mínima. Preferencias de dominio correctamente `when_area_loaded`. Conceptual PASS.
- **MELI:** notas de aplicaciones Meli con `area: [[Meli]]`; skills signals-* declaradas "Vía meli-agent-dev; fuera de Meli termina sin ejecutar Zord". Routing conceptual excluyente. Enforcement real (que el router bloquee Zord fuera de dominio) no demostrable por lectura → NOT_VERIFIABLE.
- **ARANEA:** router `aranea-agent-dev` (77 líneas) y `aranea-mcps-expert` declaran exclusión mutua con MELI ("Excluye MCPs aranea-*" / "MUST NOT para MELI"); bootstrap aplica domain gate por `area` y falla cerrado. Conceptual PASS; enforcement no demostrable → NOT_VERIFIABLE.
- **Residual capability tras context switch:** las MCP tools `aranea-*` (y credenciales de `80-agents/tools/echo-forge-worker-access/`) están disponibles en la superficie global independiente del dominio activo; el gate es procedural (router), no técnico. Diseño aceptado por bootstrap (usa prefijos de tools como evidencia de dominio), pero el riesgo residual existe y `credentials.env` amplifica. NOT_VERIFIABLE (no se puede demostrar bloqueo técnico sin cambiar permisos, prohibido en esta tarea).
- **Echo↔Forge:** mismo dominio Aranea por diseño; sin leakage entre ambos (boundary canónica compartida). PASS.

## Conflicts / Unknowns

- Graphify reindex pendiente (CLI no disponible en campaña): no pude verificar qué entradas del índice derivado apuntan hoy a `dist-files/` o al perfil dist; F1 se afirma por frontmatter + estructura, no por estado del índice.
- `30-resources/vibe-coding/` existe como dominio de la wiki (RESOURCE-WIKI:107); no auditado a fondo (fuera de alcance Echo); puede contener material relacionado al ensayo de F4.
- Ownership del folder `30-resources/agents-os/` (distribución) no está definido en esta campaña: fase K debe confirmar con owner antes de mover/marcar no-indexable.

## Recommendations

1. Fase K (vault-side, KISS): marcar `core-export/dist-files/` + `chatgpt-pack/` como no-indexables (F1); corregir skills INDEX (F5); 1 línea de link a boundary en `Echo Forge.md` (F7); repetir flags de seguridad F2 al owner en el informe final (L).
2. Fase K (owner patches, documentar no ejecutar): aplicar drafts 07 a AGENTS.md de echo/symphony (resuelve F3, reduce F6, habilita quitar credenciales); renombrar/archivar el ensayo de `vibe-coding/docs/cursor/` (F4); secret store + rotación (F2).
3. No tocar: memoria histórica (F8), runbooks, contratos frozen, archivos de distribución (sólo metadata).

## Handoff

Veredicto general: el hot path del vault está sano (club always cerrado, cold base ~5k tokens, wiki Echo sin duplicación cross-boundary y con deprecated fuera de índices). El desperdicio real de contexto vive en (a) repos (AGENTS.md con paths muertos, ensayo de 503 líneas, credenciales always-on) y (b) dos cuerpos indexables que no son canónicos (distribución AGENTS OS dentro de resources, skills INDEX incompleto). Los 3 más cargantes: F4 (~4k tokens por sesión en subtree cursor), F2 (secreto como contexto + riesgo), F5 (descubrimiento roto → folder scans). Leakage: sin violaciones conceptuales; dos NOT_VERIFIABLE (enforcement de routers, residual capability MCP/credenciales). Fase K puede ejecutar los 4 ítems vault-side listados en Recommendations sin rediseñar bootstrap ni tocar skills salvo INDEX.md (defecto demostrado F5).
