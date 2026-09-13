# Contract Audit — AGENTS OS (sólo lectura)

- Rol: auditor de contratos observables para el Conformance Harness. Extracción pura: no se diseñaron tests, no se propusieron mejoras, no se modificó ningún archivo salvo este artefacto.
- Fecha de auditoría: 2026-09-12. VAULT_ROOT resuelto: `/home/kor/secondbrain/main` (contiene `80-agents/agents-os/agents-os.md`, marker exigido por `/home/kor/secondbrain/main/AGENTS.md`).
- Estado git: el baseline informado `a6a503f` existe y es ancestro del HEAD actual `09746b3` (`git merge-base --is-ancestor a6a503f HEAD` → true). El árbol estaba limpio al iniciar la auditoría.
- Método: lectura de las autoridades Markdown listadas abajo + greps de `load_policy`, `superseded`, `archived`, `deprecating` sobre `80-agents/` y `30-resources/` (y barrido whole-vault de `load_policy: always` / `load_policy: never`). Markdown canónico es la única autoridad considerada; no se usó memoria de sistemas similares.
- Autoridades leídas: `/home/kor/secondbrain/main/AGENTS.md`; `/home/kor/secondbrain/main/80-agents/agents-os/agents-os.md`; `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`; `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`; `/home/kor/secondbrain/main/80-agents/skills/agents-os-context-retrieval/SKILL.md`; `/home/kor/secondbrain/main/80-agents/skills/INDEX.md`; `/home/kor/secondbrain/main/80-agents/skills/_shared/schema-contract.md`; `/home/kor/secondbrain/main/80-agents/skills/_shared/metadata-schema.md`; `/home/kor/secondbrain/main/80-agents/skills/_shared/note-types.md`; `/home/kor/secondbrain/main/80-agents/skills/_shared/graphify-contract.md`; `/home/kor/secondbrain/main/90-system/convenciones.md`; `/home/kor/secondbrain/main/70-templates/` (listado); `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`; `/home/kor/secondbrain/main/80-agents/skills/agents-os-session-close/SKILL.md`; `/home/kor/secondbrain/main/80-agents/skills/agents-os-session-feedback/SKILL.md`; `/home/kor/secondbrain/main/80-agents/skills/agents-os-agent-project-workflow/SKILL.md`; además los routers de dominio y notas del closed club citadas como evidencia.
- Convención de bloques: cada contrato se identifica con una línea en negrita y desarrolla exactamente los headings `## Contract`, `## Authority`, `## Observable behavior`, `## Positive condition`, `## Negative condition`, `## Testability`, `## Unknown / ambiguity`. Testability usa exactamente uno de: STATIC / SIMULATED / LIVE-SMOKE / NOT-TESTABLE.

---

**C01 — Invariantes de bootstrap: startup única y canónica (área 1)**

## Contract

Bootstrap es la única máquina de startup de AGENTS OS; nada más puede definir o duplicar el procedimiento de arranque, y se ejecuta una sola vez por sesión, no por mensaje.

## Authority

- `/home/kor/secondbrain/main/AGENTS.md`: "Invoca `80-agents/skills/agents-os-bootstrap/SKILL.md` una sola vez al iniciar una nueva sesión y ejecuta su procedimiento. No lo releas por cada mensaje" y "Bootstrap es la única máquina de startup y decide qué contexto y skills cargar; no lo reemplaces con una lectura amplia del vault".
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md` (Purpose): "Single canonical startup for AGENTS OS... Nothing else should redefine startup"; (Hard Rules): "This skill is the only startup procedure. Do not duplicate it in `agents-os.md`, `AGENTS.md`, adapters, or project notes."
- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md` (Autoridad): "El startup ejecutable vive solo en `80-agents/skills/agents-os-bootstrap/SKILL.md`... Si una guía o proyecto repite un procedimiento, manda la skill canónica."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md` (Check 4): "The startup procedure must live ONLY in `agents-os-bootstrap/SKILL.md`. Flag any procedural startup steps found in: `AGENTS.md`, `agents-os.md` (should be map+routing only), project notes, adapters or per-surface overrides."
- `/home/kor/secondbrain/main/AGENTS.md` también fija la condición de aplicabilidad: "Resuelve `VAULT_ROOT`: la carpeta que contiene `80-agents/agents-os/agents-os.md`. Si ese marker no existe, estas reglas no aplican."

## Observable behavior

En cualquier sesión el agente resuelve `VAULT_ROOT` por el marker, invoca bootstrap exactamente una vez al inicio, clasifica el turno (cold/warm/swap) y nunca redefine startup desde `agents-os.md`, proyectos, adaptadores ni notas. Bootstrap declara "Pick exactly one per turn" para el modo de sesión.

## Positive condition

Existe el marker `80-agents/agents-os/agents-os.md` bajo `VAULT_ROOT`; el único texto procedimental de startup vive en `80-agents/skills/agents-os-bootstrap/SKILL.md`; ni `AGENTS.md`, ni `agents-os.md`, ni notas de proyecto contienen pasos de startup duplicados.

## Negative condition

Cualquier archivo distinto de `agents-os-bootstrap/SKILL.md` que declare pasos de carga inicial (qué archivos leer al arrancar) es una violación; releer/ejecutar bootstrap en cada mensaje del usuario es violación; aplicar las reglas en una carpeta sin el marker es comportamiento no contratado.

## Testability

STATIC para la no-duplicación (parseo/grep de pasos de startup en `AGENTS.md`, `agents-os.md`, proyectos y adaptadores, igual que doctor Check 4); LIVE-SMOKE para "se invoca una sola vez por sesión real" (requiere sesión fresca observable).

## Unknown / ambiguity

Qué cuenta exactamente como "nueva sesión" frente a "turno warm" depende de la superficie huésped (IDE/CLI) y ninguna autoridad del vault lo define; el harness sólo puede observarlo en vivo. El AGENTS.md gestionado por markers (`AGENTS_OS_MANAGED_START/END`) implica generación automática, pero ninguna autoridad declara quién lo regenera ni cuándo.

---

**C02 — Cold start: conjunto de carga base y orden (área 2)**

## Contract

El cold start carga un conjunto cerrado: constitución + perfil global (la única nota always-load bajo `80-agents/memory/public/user-preference/`) + EXACTAMENTE UNA nota interna global de ruta fija + el registro de skills `INDEX.md`; el mapa conceptual `agents-os.md` queda fuera del stack base y se lee sólo si la tarea lo pide.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Cold start pasos 1–4: paso 1 carga `80-agents/agents-os/agent-constitution.md` y "the single always-load note under `80-agents/memory/public/user-preference/` — the global profile. Resolve it by that directory; its filename belongs to the vault owner"; paso 2 "Load exactly ONE global internal note: `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`"; paso 3 "Load the skills registry `80-agents/skills/INDEX.md` (core catalog + federated rows)... Do not read the federated domain index unless routing needs detail beyond the registry rows"; paso 4 "Read `agents-os.md` only if the task needs the conceptual map; do not add it to the base stack by ritual."
- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`, regla 2: "En cold start, bootstrap carga esta constitución, el perfil global y una sola memoria interna global compacta."
- `/home/kor/secondbrain/main/80-agents/agents-os/agents-os.md`, "Contexto Y Skills": "Core always-load: constitución, perfil global, bootstrap, el índice de skills y una sola memoria interna global compacta."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Session Modes: "Cold start — first turn of a conversation, or no entity loaded yet. Load: constitution + global profile + ONE compact global internal note + active entity context via Context Router."

## Observable behavior

En la primera vuelta de una conversación el agente abre exactamente: `agent-constitution.md`, la nota de perfil de `80-agents/memory/public/user-preference/` (hoy `rjara-agent-profile.md`), `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` y `80-agents/skills/INDEX.md`; luego resuelve entidad y aplica el domain gate (C10) y enruta a context-retrieval sólo si la pregunta depende de estado del vault (bootstrap paso 7: "For casual or general requests that do not depend on a vault entity, skip entity retrieval").

## Positive condition

Las cuatro lecturas base ocurren una vez en cold start; el perfil se resuelve por directorio (una sola nota con `load_policy: always` en `user-preference/`); la nota interna se carga por su ruta canónica fija sin escanear `memory/internal/`; `INDEX.md` entra en el arranque; `agents-os.md` no se abre por ritual.

## Negative condition

Cargar `agents-os.md` en el stack base sin necesidad conceptual; escanear `80-agents/memory/internal/` buscando notas `always`; cargar más de una nota interna global; omitir `INDEX.md`; cargar el índice federado de dominio (`30-resources/agents/00-index`) sin necesidad de routing.

## Testability

SIMULATED (ejecutar el procedimiento bootstrap en condiciones controladas con telemetría de archivos abiertos y comparar contra el conjunto esperado); el conjunto declarado es además verificable STATIC contra los paths citados.

## Unknown / ambiguity

`agents-os.md` (línea 61) describe el índice de skills como parte del "Core always-load", pero `80-agents/skills/INDEX.md` no declara `load_policy` en su frontmatter y el closed club de `agents-os-doctor/SKILL.md` (Check 3) no lo incluye: la pertenencia del índice al always-load es procedimental (paso 3 de bootstrap) y no declarativa, y ninguna autoridad explica esa asimetría. El paso 5 ("Identify the active entity... If not explicit, infer candidates with a focused search and declare the assumed entity") no especifica qué búsqueda ni qué umbral de confianza.

---

**C03 — Cold start: cargas prohibidas (área 2/13)**

## Contract

Durante el cold start está prohibido crear memoria, cargar el proyecto de desarrollo de AGENTS OS, cargar skills Nexus/MELI/externas no pedidas, y escanear carpetas en vez del registry.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Hard Rules: "Do not create memory notes during bootstrap."; "Do not load the AGENTS OS development project unless the task is maintaining the system itself."; "Prefer Graphify / focused search before opening broad folders."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Lazy Skill Routing: "Do not load Nexus, MELI, or external project skills unless the request explicitly asks for them."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, cold start paso 6: "resolve it via Graphify metadata/facets or the entity note; do not scan folders"; paso 3: "Do not read the federated domain index unless routing needs detail beyond the registry rows."

## Observable behavior

El arranque no escribe notas, no abre `10-projects/Personal/AGENTS OS/` salvo trabajo de mantenimiento del sistema, no abre skills de dominio sin puerta de dominio, y no recorre carpetas de skills en disco.

## Positive condition

Cold start sin escrituras; skills seleccionadas sólo desde `INDEX.md` (registry-first); proyecto AGENTS OS fuera del arranque salvo tarea de mantenimiento explícita.

## Negative condition

Crear una nota durante bootstrap; escanear `80-agents/skills/*/` o `30-resources/agents/skills/` para descubrir skills; cargar el proyecto AGENTS OS por defecto.

## Testability

SIMULATED (harness que instrumenta lecturas/escrituras durante una ejecución controlada de bootstrap y verifica ausencia de escrituras y de escaneos de carpeta).

## Unknown / ambiguity

El límite exacto de "escanear carpetas" no está definido (¿cuenta un `ls` de un directorio? ¿un glob?), y "la tarea es mantener el sistema itself" carece de criterio operativo; ambas fronteras quedan a interpretación del agente.

---

**C04 — Presupuestos de tokens: soft ceilings, sufficiency-first (área 2)**

## Contract

Los presupuestos de arranque/recuperación son techos blandos por tier que escalan ante miss, nunca cortes fijos: cold base 3–6k tokens, warm delta <1k, entity swap 1–3k; la suficiencia, no el número, decide la parada.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Token Targets (soft): "Cold base 3–6k tokens; warm delta <1k; entity swap 1–3k. Never cut relevant context to satisfy a number; investigate duplicate reads or broad scans."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Hard Rules: "Sufficiency-first context: the budget is a soft ceiling that escalates on miss, never a fixed cut. See `../_shared/graphify-contract.md`."
- `/home/kor/secondbrain/main/80-agents/skills/_shared/graphify-contract.md`, Budget semantics: "This is the canonical definition of 'budget' for the whole system. Any `--budget N`... is a soft starting ceiling per tier, not a hard cap"; "Sufficiency-first: load cheapest→most expensive and stop when the context is sufficient. Never cut the agent's context at a fixed number"; "Any fixed token target... is illustrative only."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-context-retrieval/SKILL.md`, Context Budget: "Do not cut context at a fixed number; that was a design error... stop when the context is sufficient"; y tiers "fact < relation < synthesis".
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`, Check 11: benchmarks "Cold start: 3-6k tokens. Warm turn: <1k new tokens. Entity swap: 1-3k tokens for the new pack".

## Observable behavior

El agente escala (re-query con techo mayor o sube de capa) cuando el resultado está truncado, y registra la causa del miss; los números son smell-test. El tier del presupuesto crece con la profundidad de la intención.

## Positive condition

Ante un miss, el agente re-consulta con techo superior o sube una capa y registra el motivo; el conteo del conjunto always-load de cold start cae en el rango 3–6k tokens aproximados.

## Negative condition

Truncar contexto para respetar el número; aceptar un corte ciego como completo; usar un objetivo fijo de tokens como guillotina (el contrato lo califica explícitamente de "design error" en `agents-os-context-retrieval/SKILL.md`).

## Testability

SIMULATED (tokenizar el conjunto de cold start y verificar el rango; simular un miss y verificar la escalada); el valor en vivo en sesión real es LIVE-SMOKE (doctor Check 11 lo declara "smoke" y admite "manual check needed" sin shell).

## Unknown / ambiguity

No existe una definición de tokenización de referencia (qué tokenizer/cuenta usa el benchmark), así que "3–6k" no es reproducible sin elegir una métrica; ninguna autoridad la fija.

---

**C05 — Nota de orientación (área 2)**

## Contract

La nota de orientación se omite por defecto; sólo se emite la nota mínima `Entity / Goal / Skills / Open questions` cuando la retrieval fue degradada, y en warm turn o swap no hay output salvo anomalía.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, cold start paso 10: "Skip the orientation note unless retrieval was degraded. If degraded, emit the minimal `Entity / Goal / Skills / Open questions` note and flag the gap."; Hard Rules: "Skip the orientation note unless retrieval was degraded."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Output: "On cold start, optionally emit a one-line orientation: `Entity: [[<canonical>]] · Goal: <one phrase> · Skills selected: <list or none>`" y "On warm turn or entity swap, no output unless something is wrong."

## Observable behavior

Cold start limpio: como máximo una línea de orientación (opcional); retrieval degradada: nota de cuatro campos con el gap marcado; warm/swap: silencio.

## Positive condition

Sin degradación no aparece la nota de 4 campos; con degradación aparece con los cuatro campos y el gap; warm/swap sin problemas no producen output.

## Negative condition

Emitir la nota de orientación completa en cada cold start limpio; emitir output ritual en warm turn.

## Testability

LIVE-SMOKE (la emisión depende de detectar degradación real de retrieval y del output del agente en sesión viva; la degradación no es determinísticamente simulable con las autoridades actuales).

## Unknown / ambiguity

Dos formatos conviven sin relación declarada: la "one-line orientation" opcional del cold start (Output) y la "orientation note" de 4 campos por degradación (paso 10); ninguna autoridad dice si la línea opcional está permitida cuando hubo degradación, ni si la emisión opcional es deseable. "Something is wrong" (warm/swap) no está definido.

---

**C06 — Warm turn: delta-only, sin releer la base (área 3)**

## Contract

En turno warm con la misma entidad el agente reutiliza el stack ya cargado y recupera sólo el delta; nunca relee constitución, perfil ni bootstrap, y no re-invoca bootstrap porque llegó otro mensaje. Sólo re-lee una fuente si cambió en disco o cambió entidad/intención.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Session Modes: "Warm turn, same entity — continuation of an ongoing task on the same entity. Reuse what is already in context. Fetch only the delta needed. Never re-read constitution/profile/bootstrap."; Warm turn pasos 1–4: "Do not invoke or reread bootstrap merely because the user sent another message."; "Only re-read a source if it changed on disk or the entity/intent shifted."
- `/home/kor/secondbrain/main/AGENTS.md`: "No lo releas por cada mensaje: en turnos warm reutiliza la base y ante cambio de entidad ejecuta sólo el routing y delta correspondientes."
- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`, regla 2: "En warm turn no relee la base; recupera solo el delta."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-context-retrieval/SKILL.md`, paso 5: "Bootstrap already loaded the base invariants on cold start: do not reload them here."
- Señales de invalidación (`agents-os-bootstrap/SKILL.md`): "the user names a new entity, the intent clearly shifts, or a base source changed on disk. Do NOT re-run the full ritual on every message."

## Observable behavior

Entre mensajes consecutivos sobre la misma entidad no hay relecturas de los archivos base; las únicas lecturas nuevas son el delta que exige el turno; la relectura puntual está permitida sólo por cambio en disco o shift de entidad/intención, y es de la fuente afectada, no del stack completo.

## Positive condition

Telemetría de una conversación multi-turno muestra cero aperturas de `agent-constitution.md`, `rjara-agent-profile.md` y `agents-os-bootstrap/SKILL.md` tras el cold start, salvo invalidación declarada.

## Negative condition

Re-ejecutar el ritual completo en cada mensaje; releer la base sin señal de invalidación; usar context-retrieval para recargar invariantes ya en contexto.

## Testability

SIMULATED (harness multi-turno con registro de file-opens); LIVE-SMOKE como confirmación en sesión real.

## Unknown / ambiguity

"Intent clearly shifts" no tiene umbral definido; la granularidad de "changed on disk" (¿mtime? ¿git diff?) no está especificada en ninguna autoridad.

---

**C07 — Entity swap: reemplazo explícito de pack, nunca dos packs de dominio (área 4)**

## Contract

Al cambiar de entidad dentro de la misma conversación se conservan los invariantes y la nota interna global, se re-aplica el domain gate con el `area` de la nueva entidad, se descarta el pack de dominio anterior (router + preferencias scoped) y el pack de entidad previo sale del razonamiento activo; jamás se sostienen dos packs de dominio a la vez.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Session Modes: "Entity swap — same conversation switches to a different entity/topic. Keep constitution + global profile; replace entity pack; skip global internal reload if already loaded this session."; Entity swap pasos 1–4: "Re-apply the domain gate with the new entity's `area`; if the domain changed, drop the previous domain pack (router + scoped preferences) and load the new router. Never hold two domain packs at once."; "Drop the previous entity pack from active reasoning."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Lazy Skill Routing: "The two domains are mutually exclusive; a domain swap replaces the pack explicitly instead of mixing."
- `/home/kor/secondbrain/main/30-resources/agents/skills/meli-agent-dev/SKILL.md`, Hard Rules: "No mezclar dominios: si la tarea cruza a Aranea, cerrar el paquete Meli y hacer swap explícito a [[aranea-agent-dev]]."
- `/home/kor/secondbrain/main/30-resources/agents/skills/aranea-agent-dev/SKILL.md`, Hard Rules: "No mezclar dominios: si la tarea cruza a Meli, cerrar el paquete Aranea y hacer swap explícito."
- `/home/kor/secondbrain/main/AGENTS.md`: "ante cambio de entidad ejecuta sólo el routing y delta correspondientes."

## Observable behavior

En un swap Meli→Aranea (o inverso): el router anterior deja de estar activo, sus preferencias scoped dejan de aplicarse, el nuevo router entra vía domain gate, y la nota interna global no se re-carga si ya está en contexto.

## Positive condition

Tras el swap, exactamente un pack de dominio activo; invariants + global internal note persistentes; sin relectura de la nota interna global ya cargada.

## Negative condition

Mezclar routers o preferencias de dos dominios; conservar el pack anterior "por si acaso"; recargar la nota interna global en cada swap.

## Testability

SIMULATED (harness de conversación con swap de entidad que verifica el set de skills/preferencias activas antes y después).

## Unknown / ambiguity

"Drop from active reasoning" es un estado mental del agente, no un artefacto observable; un harness sólo puede inferirlo por las lecturas/citaciones posteriores. La frase de Session Modes "skip global internal reload if already loaded this session" y el paso 1 "Keep the invariants and global internal note from cold start" usan formulaciones distintas para el mismo efecto; ninguna autoridad define qué pasa si el swap ocurre antes de que el cold start haya cargado la nota interna.

---

**C08 — Closed club `load_policy: always` (área 5)**

## Contract

Sólo cuatro archivos del vault pueden declarar `load_policy: always`: la constitución, la skill bootstrap, la única nota always bajo `80-agents/memory/public/user-preference/` (perfil global) y la única nota interna global (`agents-os-operating-continuity.md`); en el corpus de memoria son exactamente 2 (perfil + continuidad interna global). Cualquier otro `always` es violación; un segundo perfil es violación y cero perfiles indica instalación incompleta.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`, Check 3: "Only these may use `load_policy: always`: `80-agents/agents-os/agent-constitution.md`; `80-agents/skills/agents-os-bootstrap/SKILL.md`; `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`; exactly ONE note under `80-agents/memory/public/user-preference/`... a second one is a club violation and zero means the install is incomplete." y "Anything else with `load_policy: always` is a violation. Flag with the matching `when_*_loaded` policy. If a domain memory truly needs always-load, require an ADR before allowing it."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Hard Rules: "Only ONE global internal note may use `load_policy: always`, and it may contain only compact behaviors or failure lessons transferable across domains. Domain state, releases, hashes, task progress and project-specific next steps must use `when_project_loaded`, `when_application_loaded`, `when_error_matches` or `manual`."
- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`, Memoria Interna: "Solo una nota interna global puede usar `load_policy: always`; memorias de dominio usan `when_*_loaded` o `manual`."
- `/home/kor/secondbrain/main/80-agents/agents-os/agents-os.md`: "Preferencias globales | la única nota always-load bajo `80-agents/memory/public/user-preference/`".

## Observable behavior

Un grep de `load_policy: always` sobre el corpus vivo devuelve exactamente los cuatro miembros del club (ver "Closed-club scan result" al final); la nota interna global contiene sólo comportamientos transferibles y declara `scope: global`; el perfil declara `scope: user`.

## Positive condition

Los 4 whitelisted presentes con `always`; exactamente 1 nota always en `user-preference/`; 0 notas always fuera del club; la nota interna global bajo ~1.000 tokens aproximados con sólo lecciones transferibles (doctor Check 7: "The single global internal memory stays below 1,000 approximate tokens and contains only transferable behavior or failure lessons").

## Negative condition

Una tercera nota de memoria con `always`; una segunda nota en `user-preference/`; estado de dominio (releases, hashes, progreso de tareas) dentro de la nota global siempre-cargada (doctor Check 7: "Project status, releases, hashes, execution IDs, task progress and domain-specific next steps are violations even when the file is in the allowed path").

## Testability

STATIC (barrido de frontmatter en todo el vault + verificación de contenido de la nota global; es exactamente el Check 3 y parte del Check 7 de doctor).

## Unknown / ambiguity

Los umbrales de contenido ("transferable behavior" vs "domain state") requieren clasificación semántica por nota (doctor lo define como paso manual 2: "A fact is transferable only if it changes agent behavior across unrelated entities without carrying project identifiers or progress"); la métrica "1,000 approximate tokens" carece de tokenizador de referencia. Ver también C17 para la tensión entre la enumeración de triggers de bootstrap y `when_*_loaded` de la constitución.

---

**C09 — Lazy-load: políticas when_*_loaded, manual y never (área 6)**

## Contract

Toda memoria que no es always-load entra al contexto sólo por un trigger runtime concreto: `when_project_loaded`, `when_application_loaded`, `when_error_matches`, `when_area_loaded`, otros `when_*_loaded`, `manual` o `never`; `load_policy` es un string libre cuyo requisito contractual es ser un "concrete runtime trigger"; las preferencias scoped y la memoria de dominio son lazy y las notas superseded/archived usan `manual` o `never`.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/_shared/schema-contract.md`, campo: `"load_policy": {"kind": "string", "rule": "concrete runtime trigger"}` (línea 72 del bloque JSON).
- `/home/kor/secondbrain/main/80-agents/skills/_shared/metadata-schema.md`, Campos de retrieval: "`load_policy` decide cuándo una nota puede entrar al contexto."
- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`: "memorias de dominio usan `when_*_loaded` o `manual`."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`, Check 7: "Domain memories use `when_*_loaded`, not `always`. An internal memory outside the canonical global file may not declare `scope: global`; route it to its project, application, error or an explicit manual trigger." y "Active continuity uses an automatic scoped trigger; `superseded` and `archived` use `manual` or `never`, with low/never index priority".
- Distribución observada hoy (grep sobre `80-agents/memory/`, `30-resources/agents/skills/`, `80-agents/skills/`): 197 `manual`, 89 `when_error_matches`, ~76 `when_project_loaded`, 16 `when_application_loaded`, 3 `when_area_loaded` (las tres preferencias scoped de `80-agents/memory/public/user-preference/`), 3 `never` en memoria pública (`memory-tool-format-drift-recovery.md`, `aranea-docs-resource-location.md`, `aranea-agent-ro-sudo-nopasswd-blocked.md`), 2 `when_echo_forge_loaded`, 1 `when_installing_graphify_obsidian` (`80-agents/memory/public/runbook/graphify-obsidian-install.md`), 1 `when_entity_loaded` (`agents-os-context-retrieval/SKILL.md`).
- `/home/kor/secondbrain/main/80-agents/memory/public/user-preference/rjara-agent-profile.md` (última línea): "Las preferencias Meli y Aranea son scoped; se cargan solo con esas entidades."

## Observable behavior

Las notas de dominio (Echo Forge, Symphony, RIO, etc.) no aparecen en contexto hasta que su trigger se cumple: proyecto/aplicación cargada, error cuyo patrón coincide, área activada; `manual` exige invocación/decisión explícita; `never` excluye la nota del contexto runtime.

## Positive condition

Cada nota de `80-agents/memory/internal/` fuera del archivo global declara un trigger concreto (no `always`) y no declara `scope: global`; las notas `active` usan trigger automático scoped; `superseded`/`archived` usan `manual`/`never` con `index_priority` low/never.

## Negative condition

Memoria interna no-global con `scope: global`; memoria de dominio con `always` (ver C08); nota `superseded` con trigger automático; trigger abstracto sin condición runtime verificable (viola el rule del schema).

## Testability

STATIC (parseo de frontmatter: valor, scope, memory_state, index_priority por nota); la semántica de disparo real de cada trigger (qué cuenta como "error matching") es SIMULATED.

## Unknown / ambiguity

La tensión de enumeraciones: la constitución permite `when_*_loaded` o `manual`; bootstrap Hard Rules enumeran `when_project_loaded`/`when_application_loaded`/`when_error_matches`/`manual`; el uso real incluye `when_echo_forge_loaded` (p.ej. `/home/kor/secondbrain/main/80-agents/memory/internal/agent-memory/2026-09-04-echo-forge-mt5-6180-parser-cert-continuity.md`), `when_area_loaded`, `when_entity_loaded` y `when_installing_graphify_obsidian`, que caben en "concrete runtime trigger" (schema) o en `when_*_loaded` (constitución, si se lee como patrón), pero no en la lista literal de bootstrap. Ninguna autoridad resuelve la precedencia entre esas tres enumeraciones. Tampoco hay contrato para `never` en memoria pública (3 notas lo usan sin que una autoridad lo mencione como política de memoria; `never` sí está documentado para L0 raw session en `note-types.md`: "Load policy: never").

---

**C10 — Routing de dominio: domain gate por `area` de la entidad (área 7)**

## Contract

El dominio se deriva del frontmatter `area` de la entidad activa: `[[Meli]]` → cargar `meli-agent-dev`; `[[Echo]]` o `[[Aranea]]` → cargar `aranea-agent-dev`; cualquier otra área o entidad no resoluble → sin router de dominio. Evidencia de superficie (prefijos MCP `mcp__aranea-*`, tooling corporativo Zord/Fury/Spellbook) sustituye a la entidad cuando no resuelve. Evidencia ambigua o conflictiva falla cerrado (sin router); nunca se cargan ambos routers; el router carga a lo sumo UNA skill especializada y posee las preferencias scoped de su dominio. La identidad de dominio debe demostrarse, la mención del usuario no basta.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, cold start paso 6: "`[[Meli]]` → load `meli-agent-dev`. `[[Echo]]` or `[[Aranea]]` → load `aranea-agent-dev`. Any other area, or no resolvable entity → no domain router. If no entity resolves but the surface shows domain evidence (MCP tool prefixes `mcp__aranea-*`, or corporate tooling such as Zord/Fury/Spellbook), use that instead. Ambiguous or conflicting evidence fails closed: no router. Never load both routers; the router loads at most ONE specialized skill and owns the scoped preferences of its domain."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Lazy Skill Routing: "The domain comes from the active entity's `area` (domain gate, cold start step 6)... The two domains are mutually exclusive; a domain swap replaces the pack explicitly instead of mixing."
- `/home/kor/secondbrain/main/30-resources/agents/skills/meli-agent-dev/SKILL.md`, Procedure 1: "Confirmar boundary Meli. Demostrar identidad corporativa (remoto/owner del repo, metadata corporativa o relación canónica del vault); la mención del usuario no basta por sí sola. Si es no Meli o queda incierto, no abrir fuentes corporativas y resolver el dominio real."; Hard Rules: "Revisión de código Meli exige Zord vía [[signals-code-review]]: nunca revisar PRs Meli sin esa skill."
- `/home/kor/secondbrain/main/30-resources/agents/skills/aranea-agent-dev/SKILL.md`, Procedure 1: "Confirmar boundary Aranea. Homelab y sus hosts/Echo/mcps son este dominio; Meli/corporativo se rechaza y deriva a [[meli-agent-dev]] antes de leer documentación o abrir conexiones."
- `/home/kor/secondbrain/main/80-agents/skills/INDEX.md` (filas federadas): meli-agent-dev "Router del dominio Meli... Todo trabajo corporativo Meli. Excluye MCPs `aranea-*`."; aranea-agent-dev "Router del dominio Aranea (homelab)... Todo trabajo homelab Echo/Forge/mcps. Excluye Meli/corporativo."

## Observable behavior

Dado un pedido cuya entidad canónica tiene `area: "[[Meli]]"` el agente activa sólo el router Meli; con `area: "[[Aranea]]"` o `[[Echo]]` sólo el router Aranea; con otra área (o sin entidad) ningún router; con evidencia contradictoria (p.ej. entidad Meli + herramienta `mcp__aranea-*`) no carga router alguno.

## Positive condition

Un solo router activo por turno, derivado del `area` resuelto vía Graphify metadata/facets o la nota de entidad (sin escanear carpetas); alias/slugs resueltos al título canónico Obsidian antes del gate (bootstrap paso 5: "Resolve aliases/slugs to the canonical Obsidian title").

## Negative condition

Cargar ambos routers; cargar un router sin entidad ni evidencia de superficie; ante ambigüedad elegir un router por probabilidad (debe fallar cerrado); derivar el dominio de tags o del nombre de carpeta en vez del frontmatter `area`.

## Testability

SIMULATED (matriz de casos: entidad Meli / Echo / Aranea / otra / inexistente / evidencia de superficie / conflicto; verificar router activo por turno).

## Unknown / ambiguity

No hay lista cerrada de qué "corporate tooling" cuenta como evidencia Meli (Zord/Fury/Spellbook son ejemplos, no enumeración); el gate no define qué hacer si la entidad tiene `area` apuntando a otra área no-Meli/no-Echo/no-Aranea pero la evidencia de superficie sugiere un dominio (¿"any other area" gana o la evidencia sustituye?); el bootstrap sólo define la sustitución de evidencia "if no entity resolves". La resolución del `area` "via Graphify metadata/facets or the entity note" no especifica precedencia si ambos discrepan.

---

**C11 — Scope y perfil: preferencias globales vs scoped (área 8)**

## Contract

El perfil global (`scope: user`, always) aplica siempre; las preferencias de dominio son scoped (`scope: area`, `load_policy: when_area_loaded`) y sólo son válidas dentro de su dominio, cargadas por el router correspondiente; la memoria interna no-global no puede declarar `scope: global`.

## Authority

- `/home/kor/secondbrain/main/80-agents/memory/public/user-preference/rjara-agent-profile.md`, frontmatter: `scope: user`, `load_policy: always`; última línea: "Las preferencias Meli y Aranea son scoped; se cargan solo con esas entidades."
- `/home/kor/secondbrain/main/30-resources/agents/skills/meli-agent-dev/SKILL.md`, Minimal Read 2–3 y Procedure 2: "Cargar preferencias scoped... Son válidas sólo dentro de este dominio."; Hard Rules: "Las preferencias Meli son scoped (`when_area_loaded`): no se cargan en cold start ni persisten fuera del dominio."
- `/home/kor/secondbrain/main/30-resources/agents/skills/aranea-agent-dev/SKILL.md`, Minimal Read 2: `rjara-aranea-operations-preferences.md` como preferencia scoped.
- Frontmatter observado: `/home/kor/secondbrain/main/80-agents/memory/public/user-preference/rjara-meli-work-preferences.md` (`scope: area`, `area: "[[Meli]]"`, `load_policy: when_area_loaded`); `/home/kor/secondbrain/main/80-agents/memory/public/user-preference/rjara-aranea-operations-preferences.md` (`scope: area`, `area: "[[Aranea]]"`, `load_policy: when_area_loaded`); `/home/kor/secondbrain/main/80-agents/memory/public/user-preference/rjara-vpn-routing-preferences.md` (`scope: user`, `load_policy: when_area_loaded`).
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`, Check 7: "An internal memory outside the canonical global file may not declare `scope: global`".
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, paso 6: "the router... owns the scoped preferences of its domain."

## Observable behavior

Preferencias `[DURA]`/`[FUERTE]` del perfil (idioma, tono, no-cierre-ritual, no-hard-wrap, etc.) aplican en todo turno; las de `rjara-meli-work-preferences.md` sólo tras activar el dominio Meli; las de `rjara-aranea-operations-preferences.md` sólo tras activar Aranea; al hacer swap (C07) las preferencias scoped salen con el pack.

## Positive condition

Cold start carga el perfil global y ninguna preferencia scoped; la activación del dominio carga su nota de preferencias; `scope` es singular y las relaciones múltiples viven en `entities` (metadata-schema: "`scope` es singular; relaciones múltiples viven en `entities`").

## Negative condition

Cargar `rjara-meli-work-preferences.md` en cold start o en un turno Aranea; memoria interna no-global con `scope: global`; tratar preferencias scoped como persistentes fuera del dominio.

## Testability

SIMULATED (turnos con y sin dominio activo verificando qué preferencias se citan/aplican); los frontmatter son STATIC.

## Unknown / ambiguity

`rjara-vpn-routing-preferences.md` tiene `scope: user` con trigger `when_area_loaded`: es una nota de usuario con disparo de área, cargada por el router Meli (Minimal Read 3) pero sin dueño de dominio declarado en Aranea (su router no la lista); ninguna autoridad define a qué dominio pertenece realmente ni si un `scope: user` puede tener trigger de área. La constitución usa "scope más estrecho" para continuidad interna (`agent-constitution.md`: "Toda continuidad interna usa el scope más estrecho y un trigger concreto") sin definir una jerarquía de estrechez entre `user` y `area`.

---

**C12 — Carga de skills: registry-first, una skill primaria, dominio-gated vía router (área 9)**

## Contract

El agente conoce las skills desde `80-agents/skills/INDEX.md` (cargado en cold start) y rutéa desde él sin escanear carpetas; carga como máximo UNA skill especializada adicional (lazy) sólo si la tarea la necesita y el router de dominio no la rutéa ya; las skills domain-gated se alcanzan exclusivamente a través de su router de dominio, nunca directo; las dependencias se cargan sólo si el procedimiento lo exige.

## Authority

- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Lazy Skill Routing: "The registry `80-agents/skills/INDEX.md` is already in context from cold start; route from it instead of scanning folders. Match the task to one primary skill and load that `SKILL.md`; load a dependency only if its procedure requires it. Common direct routes: close → `agents-os-session-close`, repair AGENTS OS → `agents-os-doctor`, project execution → `agents-os-agent-project-workflow`, entity merge → `agents-os-entity-lifecycle`, index stale or blocked update → `agents-os-graphify-maintenance`."; "Domain-gated skills route through their domain router, never directly."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, cold start paso 9: "Select at most ONE additional specialized skill (lazy-load) only if the task needs it and the domain router (if loaded) does not already route it."
- `/home/kor/secondbrain/main/80-agents/skills/INDEX.md`, callout inicial: "El core (`80-agents/skills/`) contiene sólo comportamientos de AGENTS OS; las skills de dominio y transversales viven curadas en `30-resources/agents/skills/` y las app-owned en el repo owner... Se carga en el cold start del `agents-os-bootstrap`."; "Regla de lugar: una skill vive en el core sólo si cambia el comportamiento de AGENTS OS itself; todo lo demás vive federado y se enlaza, no se copia."; filas domain-gated: signals-code-review "Vía `meli-agent-dev`. Fuera de Meli termina sin ejecutar Zord."; signals-func-spec-authoring / signals-tech-spec-authoring / fury-lib-consumer-deploy "Vía `meli-agent-dev`."; aranea-mcps-expert "Sólo dominio Aranea. **MUST NOT** para MELI/corporativo."
- `/home/kor/secondbrain/main/30-resources/agents/skills/meli-agent-dev/SKILL.md`, Procedure 3: tabla de routing a skills especializadas; Minimal Read 4: "Sólo la skill especializada elegida en el routing; nunca el catálogo completo."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`, Check 8: "Skills referenced in `80-agents/skills/INDEX.md` exist on disk." / "Skills existing on disk appear in `INDEX.md`."

## Observable behavior

Ante una tarea se elige una skill primaria del registry; skills Meli como `signals-code-review` sólo se alcanzan con el router Meli activo; `aranea-mcps-expert` sólo bajo `aranea-agent-dev`; las skills app-owned de `xKoRx/symphony` se referencian por `repo + path relativo` (INDEX: "El registry enlaza por `repo + path relativo`; nunca copia ni persiste un path absoluto de máquina (constitución, invariante 11)").

## Positive condition

Toda skill usada figura en `INDEX.md` (core, federada o app-owned) o es una dependencia declarada de la skill primaria; la skill domain-gated cargada tiene su dominio activo; hay paridad registry↔disco.

## Negative condition

Descubrir skills listando directorios; cargar dos skills primarias para una tarea; alcanzar `signals-code-review` o `aranea-mcps-expert` sin su router; copiar skills federadas al core (viola la regla de lugar).

## Testability

STATIC para la paridad registry↔disco y la regla de lugar (parseo de `INDEX.md` y filesystem); SIMULATED para la selección de una skill primaria y el gating por dominio.

## Unknown / ambiguity

"One primary skill" no define qué pasa con tareas que cruzan dos procedimientos (p.ej. code review + PR description); el bootstrap dice "load a dependency only if its procedure requires it" sin mecanismo para distinguir dependencia de segunda primaria. La fila de INDEX para `signals-code-review` ("Fuera de Meli termina sin ejecutar Zord") declara un comportamiento de terminación que no está replicado en el body de la propia skill citada por el auditor (no leída aquí; ver Unknown general de cobertura).

---

**C13 — Herramientas y MCP: fronteras por dominio (área 10)**

## Contract

Las capabilities MCP `aranea-*` no existen en el dominio Meli (prohibido usarlas para hosts, datos, repos o infraestructura Meli/corporativa); todo acceso MCP `aranea-*` es exclusivo del dominio Aranea y pasa siempre por `aranea-mcps-expert` (única puerta, activada bajo `aranea-agent-dev`); `aranea-mcps-expert` es MUST NOT para MELI/corporativo; PROD de datos/control-plane Aranea es read-only; en Meli, el acceso a datos/clusters va sólo por las superficies corporativas autorizadas por la skill especializada elegida (el router Meli no habilita superficies propias).

## Authority

- `/home/kor/secondbrain/main/30-resources/agents/skills/meli-agent-dev/SKILL.md`, Hard Rules: "Las capabilities MCP `aranea-*` **no existen en este dominio**: nunca usarlas para hosts, datos, repos o infraestructura Meli/corporativa."; Procedure 5: "Acceso a datos o clusters Meli: sólo por las herramientas y superficies corporativas autorizadas por la skill especializada elegida; esta skill no habilita superficies propias."; description: "las capabilities MCP aranea-* no existen en este dominio."
- `/home/kor/secondbrain/main/30-resources/agents/skills/aranea-agent-dev/SKILL.md`, Purpose: "Los servicios MCP de Aranea (SSH, PostgreSQL, MongoDB, Hasura) son exclusivos de este dominio: ninguna otra skill o dominio los activa."; Hard Rules: "El acceso MCP `aranea-*` es **exclusivo de este dominio** y pasa siempre por [[aranea-mcps-expert]]; ninguna otra skill abre esas conexiones ni duplica endpoints, permisos o semántica MCP."; "**MUST NOT** para MELI o sistemas corporativos"; "Elegir ambiente antes que autoridad; PROD de datos/control plane es read-only (contrato de [[aranea-mcps-expert]])."; "Esta skill nunca conecta `aranea-*` por su cuenta."
- `/home/kor/secondbrain/main/30-resources/agents/skills/aranea-mcps-expert/SKILL.md`, Purpose: "Activar bajo el dominio [[aranea-agent-dev]] —su única puerta de entrada— antes de usar cualquier capability `aranea-*`... **MUST NOT activate for Mercado Libre / MELI infrastructure, databases, repositories, hosts, credentials or corporate systems** (dominio de [[meli-agent-dev]])."
- `/home/kor/secondbrain/main/80-agents/skills/INDEX.md`, filas federadas: aranea-mcps-expert "Sólo dominio Aranea. **MUST NOT** para MELI/corporativo."; echo-forge-wfm-troubleshooting (app-owned) "delega el acceso MCP a [[aranea-mcps-expert]]".
- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`, regla 8: "El conocimiento persistido debe ser agnóstico al modelo, IDE o cliente, salvo una limitación de superficie explícita." (única excepción declarada para diferencias de superficie).

## Observable behavior

En una tarea Meli el agente nunca invoca herramientas `mcp__aranea-*`; en una tarea Aranea con necesidad MCP, activa `aranea-mcps-expert` antes de conectar y elige ambiente antes que autoridad; conexiones PROD de datos/control-plane Aranea son read-only.

## Positive condition

Router Aranea activo + `aranea-mcps-expert` activado antes del primer uso de `aranea-*`; ninguna conexión `aranea-*` abierta por otra skill; cero uso de `aranea-*` con targets Meli.

## Negative condition

Usar `mcp__aranea-*` (o cualquier MCP Aranea) en trabajo Meli/corporativo; conectar `aranea-*` desde `aranea-agent-dev` u otra skill sin pasar por la expert; mutar PROD de datos/control-plane Aranea; duplicar endpoints/permisos/semántica MCP fuera de la expert.

## Testability

LIVE-SMOKE para la frontera real de uso (exige una superficie con ambos sets de MCP expuestos y tareas reales de cada dominio); STATIC para la existencia y coherencia de las reglas declaradas; la configuración host-level de qué MCP servers están expuestos por superficie NO está declarada en ninguna autoridad del vault (NOT-TESTABLE desde el vault).

## Unknown / ambiguity

El vault declara reglas de uso a nivel skill, pero ningún archivo del vault configura la exposición real de MCPs por dominio/superficie (eso vive fuera del vault, en la config de cada superficie); por lo tanto el harness puede verificar la regla declarada, no la garantía de exposición. La lista de capabilities (`aranea-ssh-mcp`, `aranea-postgres-mcp`, `aranea-mongodb-mcp`, `aranea-hasura-mcp` en `aranea-mcps-expert/SKILL.md` related) podría divergir de las MCPs realmente configuradas; ninguna autoridad del vault exige paridad. No se encontró ninguna otra frontera de herramientas declarada (p.ej. límites de uso de Graphify por dominio) fuera de la regla genérica de la constitución regla 8.

---

**C14 — Deprecación y lifecycle de memoria (superseded/archived) (área 11)**

## Contract

La continuidad interna mantiene exactamente un checkpoint activo por `continuity_key` (actualizado in-place); el reemplazo físico exige transición atómica de la nota anterior a `memory_state: superseded` + `load_policy: manual` + `index_priority: low` + enlace `superseded_by` (y la sucesora registra `supersedes`); el paso superseded→archived ocurre sólo cuando ninguna ruta normal de retrieval lo necesita; nunca se reactiva un checkpoint viejo sin retirar el actual; retrieval ignora memorias superseded/archived salvo consulta histórica explícita. Las notas legacy sin `schema_version` son read-only; las versiones desconocidas fallan cerrado. En Sistema 2, `deprecating` es un `status` válido sólo para `application`.

## Authority

- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`, Memoria Interna: "El camino normal mantiene un único checkpoint activo por `continuity_key` y lo actualiza en el mismo archivo... Si un cambio material de scope exige una sucesora, la anterior pasa atómicamente a `memory_state: superseded`, `load_policy: manual` e `index_priority: low`, enlazada mediante `superseded_by`. Retrieval ignora memorias `superseded` y `archived` salvo consulta histórica explícita."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Hard Rules: "Internal continuity uses one active checkpoint per `continuity_key`. Update it in place after consuming it; if replacement is required, retire the prior checkpoint to `superseded` plus `manual` in the same change. Never load `superseded` or `archived` continuity during normal startup or entity retrieval."
- `/home/kor/secondbrain/main/80-agents/skills/_shared/note-types.md`, Internal Continuity Memory: "Create a successor only when the scope or canonical identity changes materially. Then mark the prior note `memory_state: superseded`, set `load_policy: manual`, lower `index_priority`, link `superseded_by`, and link the successor with `supersedes`."; "`archived` memories are historical evidence and never enter normal retrieval. Missing lifecycle fields are legacy: do not bulk-load them and migrate them only when touched."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-memory-distillation/SKILL.md`, pasos 4–5: "If replacement is unavoidable, write the successor and then change the prior note to `memory_state: superseded`, `load_policy: manual`, `index_priority: low` and `superseded_by: ...`"; "Historical cleanup changes `superseded` to `archived` only when no normal retrieval path needs it. Never reactivate an old checkpoint without first retiring the current one."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-context-retrieval/SKILL.md`, paso 5: "Ignore `superseded` and `archived` memory unless the user asks for history; treat lifecycle-less legacy memory as candidates, never as a set to bulk-load, and migrate it when touched."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`, Check 7: "A `continuity_key` has exactly one `memory_state: active` note... superseded notes require `superseded_by`."
- `/home/kor/secondbrain/main/80-agents/skills/_shared/schema-contract.md`: `"memory_state": {"kind": "string", "values": ["active", "superseded", "archived"]}`; `"legacy_unversioned": "read_only"`, `"unknown_version": "reject"`, `"upgrade_policy": "explicit_migrator"`; S2 `application` statuses `["active", "deprecating", "deprecated", "archived"]`.
- Evidencia viva de la transición: `/home/kor/secondbrain/main/80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity-archive.md` declara `memory_state: superseded`, `load_policy: manual`, `index_priority: low`, `indexable: false`, `superseded_by: "[[agents-os-operating-continuity]]"`, mismo `continuity_key: global/agents-os-operating-continuity` que la activa.

## Observable behavior

Para cada `continuity_key` existe a lo sumo una nota `active`; las notas retiradas declaran el cuádruple (superseded/manual/low/superseded_by); el retrieval normal no las devuelve; el bootstrap no las carga.

## Positive condition

Un `continuity_key` → exactamente una `active`; transiciones completas y atómicas (los cuatro campos en el mismo cambio); consulta histórica sólo por pedido explícito del usuario.

## Negative condition

Dos notas `active` para el mismo `continuity_key`; una nota `superseded` sin `superseded_by` o con `index_priority` alto o trigger automático; cargar continuidad superseded/archived en startup o entity retrieval; migración implícita de versiones (el schema exige migrador explícito).

## Testability

STATIC para el estado del corpus (un `continuity_key` → una activa; cuádruple de retiro presente; hay al menos un caso conformante: la nota archive citada); SIMULATED para la ejecución de la transición y para "retrieval ignora superseded/archived" (lanzar una query y verificar exclusiones).

## Unknown / ambiguity

El `archived` de memoria interna no tiene productor declarado con criterio medible ("only when no normal retrieval path needs it" es subjetivo); ninguna autoridad define quién decide ni cuándo se ejecuta el cleanup superseded→archived. `deprecating` existe como status S2 de application pero ninguna autoridad define comportamiento de retrieval para aplicaciones `deprecating`.

---

**C15 — Precedencia de autoridad (área 12)**

## Contract

Markdown es fuente de verdad y Graphify índice derivado y reconstruible (jamás autoridad vigente); el bloque JSON de `schema-contract.md` es la autoridad ejecutable única para sets exactos de S1/S2; la constitución contiene invariantes y manda sobre guías/proyectos; si una guía o proyecto repite un procedimiento, manda la skill canónica; hay una sola fuente por hecho (procedimientos en skills, secuencias mecánicas en runbooks, criterio en memoria, estado en entidades/proyectos), enlazando en vez de repetir.

## Authority

- `/home/kor/secondbrain/main/80-agents/agents-os/agents-os.md`: "Markdown es fuente de verdad; Graphify es índice derivado. Journal, snapshots y packs generados son auditoría o distribución, nunca autoridad vigente."; "Una fuente por hecho; enlazar en vez de repetir."
- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`, regla 1: "Markdown es fuente de verdad. Graphify es índice derivado y reconstruible."; regla 5: "Una fuente canónica por hecho: procedimientos en skills, secuencias mecánicas en runbooks, criterio reusable en memoria y estado en entidades o proyectos. Enlazar en vez de repetir."; (Autoridad): "Si una guía o proyecto repite un procedimiento, manda la skill canónica."
- `/home/kor/secondbrain/main/80-agents/skills/_shared/schema-contract.md`: "Esta nota es la autoridad machine-readable para el envelope, versiones, campos, estados, tags, secciones mínimas, template canónico y política de lint de cada tipo S1 y S2. Las guías humanas explican semántica; no duplican estos sets exactos."; (Ownership): "Esta nota define sets exactos y mappings ejecutables. `metadata-schema.md`, `note-types.md` y `90-system/convenciones.md` explican uso y fronteras sin redefinir las listas."
- `/home/kor/secondbrain/main/80-agents/skills/_shared/metadata-schema.md`, Frontera de autoridad: "`schema-contract.md`: contrato exacto y versionado. `note-types.md`: frontera conceptual S1/S2..."
- `/home/kor/secondbrain/main/90-system/convenciones.md`, Schema de Sistema 2 (autoridad): "El bloque JSON de `80-agents/skills/_shared/schema-contract.md` es la autoridad única y versionada para tipos, lifecycle, campos, tags, secciones y mappings `type → template` de S1/S2. Esta sección conserva sólo la interpretación humana."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md`, Canonical Authority: "`AGENTS.md` invoca esta skill; this file owns startup. `agents-os.md` is only the conceptual map, the constitution contains invariants, specialized skills contain lazy procedures, and project/journal notes contain state/history."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-context-retrieval/SKILL.md`, Hard Rules: "Do not treat Graphify output as canonical without opening source notes when the answer affects persisted knowledge."; `/home/kor/secondbrain/main/80-agents/skills/_shared/graphify-contract.md`: "Graphify is a derived index over Markdown. Markdown remains the source of truth."

## Observable behavior

Ante conflicto entre Graphify y un archivo Markdown, gana el Markdown (verificando la fuente); ante un procedimiento repetido en una guía, se aplica la skill; ante un set de campos/tags/estados dudoso, se consulta el bloque JSON del schema-contract y no las guías humanas; las decisiones persistidas se validan contra la fuente Markdown.

## Positive condition

Ninguna guía humana redefine listas del schema; los conflictos se resuelven en la dirección Markdown>derivado y skill>guía; cada hecho tiene una única fuente canónica con enlaces desde las demás.

## Negative condition

Tratar salida de Graphify, snapshots, packs generados, journal o distributions como autoridad vigente; duplicar sets exactos del schema en `metadata-schema.md`/`note-types.md`/`convenciones.md`; dos fuentes canónicas para un mismo hecho.

## Testability

SIMULATED (escenarios de conflicto inyectados: derivado vs fuente, guía vs skill; verificar la elección del agente); STATIC para la no-duplicación de sets en las guías humanas.

## Unknown / ambiguity

La cadena completa de precedencia no está escrita como lista única y ordenada en ninguna autoridad: se reconstruye por piezas (constitución > skills > guías/proyectos; Markdown > derivado; schema-contract > guías humanas). No está definido qué pasa si la constitución y el bloque JSON del schema-contract discrepan (p.ej. enumeración de triggers, ver C09) ni qué autoridad arbitra. `graphify-contract.md` (línea 54) corrige explícitamente una afirmación previa suya ("An earlier note claimed the file-node id path worked; that was wrong"), lo que demuestra que las notas de contrato también pueden contener afirmaciones históricas erróneas sin marcador de estado.

---

**C16 — Comportamiento prohibido (área 13)**

## Contract

Catálogo de prohibiciones declaradas: no persistir secretos/credenciales/tokens/material dañino/dumps pesados/cadena de pensamiento privada; no persistir paths absolutos de máquina ni `file://` (todo path interno es relativo a `VAULT_ROOT`; repos externos por `repo + path relativo`); no agregar repos completos al vault; no mantener planes paralelos fuera de la nota de proyecto de agente; el agente nunca marca la tarea puente como Done; no ejecutar cierre completo ni crear L0/L1/feedback sin pedido explícito (L0 sólo con transcript disponible o placeholder pedido); nunca usar UUID/hash/ID externo como filename/prefix/H1/tópico; nunca sobrescribir un hecho canónico de entidad sin journal log; no ocultar conflictos ni sobrescribir hechos canónicos sin evidencia; no crear notas canónicas copiando templates o escribiendo frontmatter a mano (materializador obligatorio); no cortar contexto por número fijo; no escribir/sincronizar estado generado de Graphify dentro del vault ni invocar el binario `graphify` crudo desde el vault; no usar queries abstractas ni nodos template como evidencia de estado vivo; no cargar raw sessions por defecto; no hard-wrappear (perfil DURA); en repos de desarrollo, jamás crear/fixar/publicar versión productiva `X.Y.Z` desde rama feature; el cierre explícito termina con la frase literal `por favor gracias`.

## Authority

- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`: regla 7 "No ocultar conflictos ni sobrescribir hechos canónicos sin evidencia"; regla 9 "No persistir secretos, credenciales, tokens, material dañino, dumps pesados ni cadena de pensamiento privada. Guardar referencias seguras."; regla 11 "Toda referencia interna al vault es relativa a `VAULT_ROOT`; nunca persistir `/Users/...`, `/home/...` ni `file://` de una máquina. Para repos externos usar `repo + path relativo`"; regla 12 "No agregar repositorios completos al vault. Clones, worktrees, builds y grafos de código derivados deben vivir fuera de `VAULT_ROOT`"; regla 13 "Toda nota canónica nueva se materializa mediante el contrato ejecutable y `materialize_schema_note.py`; no copiar templates ni escribir frontmatter canónico a mano. Derivados/fragmentos requieren exención contractual."; regla 14 "una rama feature jamás crea, fija ni publica una versión productiva limpia `X.Y.Z`"; Cierre de sesión: "Ejecutar `agents-os-session-close` solo por pedido explícito del usuario. Persistir por delta; no crear L0 sin transcript disponible o placeholder solicitado."; "Finalizar el cierre explícito con la frase literal `por favor gracias`."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-session-close/SKILL.md`, Hard Rules: "Do not run a full AGENTS OS close automatically at task completion."; "Create L0 only when transcript content is available or the user explicitly asks for a placeholder."; "Never use UUID/hash/external ID as filename, prefix, H1, or human topic."; "Never overwrite a canonical entity fact without a journal log."; Trigger Guard: "Finishing a task, reaching a checkpoint, or noticing reusable knowledge is NOT a trigger by itself."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-agent-project-workflow/SKILL.md`: "Regla dura: la nota del proyecto de agente... es la única fuente de verdad de planificación para ese trabajo. No crear un plan paralelo en un archivo de scratch, un documento externo, o solo en el contexto de la conversación."; "El agente nunca marca `[x]` la tarea puente. Máximo llega a `[r]` (Review)."; "Un rechazo del humano siempre se registra en la bitácora... no se corrige en silencio."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-context-retrieval/SKILL.md`, Hard Rules: "Do not use abstract queries like 'give me important context'."; "Do not treat template nodes as evidence of live project state."; "Do not write, copy or sync Graphify output inside the vault"; "Do not load raw sessions by default."; "Do not load a note body without a prior selection"; "Do not cut context at a fixed token number".
- `/home/kor/secondbrain/main/80-agents/skills/_shared/graphify-contract.md`: "Generated state is strictly local to each machine... it is never vault content."; "Run only `graphify-obsidian` for this vault; never invoke the raw `graphify` binary from a vault path."; "Avoid broad filename globs such as `**/*raw-session*.md`".
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-session-feedback/SKILL.md`, Hard Rules: "Do not store secrets, credentials, heavy logs, or private chain-of-thought."; "Do not quote internal memory in the feedback note."; "A clean session with no friction → no feedback note."
- `/home/kor/secondbrain/main/80-agents/memory/public/user-preference/rjara-agent-profile.md`, preferencia DURA: "Prohibido el hard-wrap. Nunca insertar saltos de línea manuales dentro de un párrafo o de un ítem de lista en Markdown... Esto rige para todo lo que el agente escriba (vault, código, docs, mensajes)."; DURA: "No ejecutar cierre completo ni crear L0/L1/feedback salvo pedido explícito."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-doctor/SKILL.md`, Check 7: "No credentials / tokens / passwords / API keys in any `80-agents/memory/internal/**/*.md`. Run a focused grep on `password|passwd|secret|api[_-]?key|token|AKIA|pwd` and flag any hit."; Check 1: "Flag any machine-specific home or absolute vault path."
- `/home/kor/secondbrain/main/80-agents/skills/agents-os-note-capture/SKILL.md` y el materializador: `schema-contract.md` creation.policy "canonical notes are materialized from the resolved template; direct template copies and handwritten frontmatter are rejected" (materializer: `80-agents/skills/_shared/scripts/materialize_schema_note.py`).

## Observable behavior

Ningún archivo escrito por el agente contiene secretos, paths absolutos de máquina o hard-wrap; las notas canónicas nacen del materializador; el cierre completo ocurre sólo por pedido y termina con `por favor gracias`; los planes de proyectos `owner: agent` viven sólo en la nota del proyecto; la tarea puente nunca llega a `[x]` por el agente.

## Positive condition

Greps de secretos/paths absolutos sobre producciones del agente sin hits; cada nota canónica es rastreable al materializador (o tiene exención contractual registrada en `schema-contract.md` fragments/derived_templates); bitácora y tarea puente reflejan el ciclo WIP→Review→Done humano.

## Negative condition

Cualquier instancia de las prohibiciones listadas; "arreglar" un hallazgo sin pedido; cierre automático al terminar una tarea; feedback automático por cierre limpio; planes que sobreviven a la sesión fuera de la nota del proyecto.

## Testability

STATIC en su mayoría (greps de secretos/paths/UUID-filenames/hard-wrap; verificación de materialización; ciclo de tarea puente en la nota); SIMULATED para conductas de decisión (no cerrar sin pedido, no corregir en silencio); LIVE-SMOKE para la frase literal de cierre y la ausencia de ritual en sesiones reales.

## Unknown / ambiguity

La lista es distribuida: no existe un único índice de prohibiciones y algunas viven en preferencias del usuario (`[DURA]` del perfil) cuyo estatus jerárquico frente a la constitución no está declarado. "Heavy logs/dumps" no tiene umbral cuantitativo. La frase literal `por favor gracias` está declarada en la constitución pero su verificación depende de salida real del agente (LIVE-SMOKE).

---

**C17 — Contrato de templates y materialización (Sistema 2 nace de `70-templates/`; referenciado por constitución reglas 3 y 13) (área 12/3)**

## Contract

Todo documento nuevo de Sistema 2 nace desde `70-templates/` y todo canónico S1 desde `80-agents/templates/`, resolviendo el mapping `type → template` y la `schema_version` actual en `schema-contract.md`; la materialización es vía `materialize_schema_note.py` (nunca copia manual de frontmatter); si falta template se crea en el mismo cambio; el validador rechaza cruces de frontera S1/S2, templates sin mapping y mappings duplicados; las notas derivadas/fragmentos requieren exención explícita en el contrato.

## Authority

- `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md`, regla 3: "Todo documento nuevo de Sistema 2 nace desde `70-templates/`; si falta template, se crea en el mismo cambio."; regla 13 (citada en C16).
- `/home/kor/secondbrain/main/80-agents/skills/_shared/note-types.md`, Template Policy: "Every new S1/S2 document must resolve its canonical template and current `schema_version` through `schema-contract.md`... Sistema 1 templates live under `80-agents/templates/`; Sistema 2 templates live under `70-templates/`. The validator rejects boundary crossings, unmapped templates and duplicate canonical mappings."
- `/home/kor/secondbrain/main/80-agents/skills/_shared/schema-contract.md`: `"s1": {"template_root": "80-agents/templates", ...}`, `"s2": {"template_root": "70-templates", ...}`; `derived_templates` (graphify-feedback, hygiene-report) y `fragments` (`70-templates/task.md`, "task-line snippet without frontmatter; not a note type") registran las exenciones; `"creation": {"materializer": "80-agents/skills/_shared/scripts/materialize_schema_note.py", "policy": "canonical notes are materialized from the resolved template; direct template copies and handwritten frontmatter are rejected"}`.
- Verificación de cobertura actual (listado de directorios): `70-templates/` contiene 30 archivos que cubren los 29 tipos S2 del bloque JSON (incluye `service-operational.md` para `service-doc` y `ai-context-pack.md` para `context_pack`) más el fragmento `task.md`; `80-agents/templates/` contiene 17 archivos que cubren los 17 tipos S1 (incluye los 2 derivados).
- `/home/kor/secondbrain/main/90-system/convenciones.md`: "Toda nota S2 nueva nace del template que resuelve el contrato, usa su versión actual y declara el envelope común."
- Validación declarada: `python3 80-agents/skills/_shared/scripts/validate_schema_contract.py` (`metadata-schema.md`, `convenciones.md`); `lint.gate_policy`: "current_findings_must_be_subset_of_baseline" con baseline `80-agents/skills/agents-os-entity-lifecycle/lint-baseline-v1.json` y fingerprint sha256.

## Observable behavior

Toda nota S1/S2 nueva porta `schema_version: 1` (versión current y única soportada), envelope común requerido (`type`, `schema_version`, `created`, `updated`, `tags`; S1 añade `scope`), secciones mínimas de su tipo, y proviene del materializador; notas S1 nunca llevan `status`/`draft` (schema: s1 forbidden `["status", "draft"]`).

## Positive condition

Mapping tipo→template resuelto y vigente para cada creación; `validate_schema_contract.py` verde; exenciones sólo si el contrato registra razón explícita; notas unversioned tratadas como legacy read-only.

## Negative condition

Crear una nota S2 sin template o con template de S1 (boundary crossing); copiar frontmatter a mano; introducir una `schema_version` no soportada (reject) o crear notas desde template legacy; exenciones sin registro en el contrato.

## Testability

STATIC (ejecución del validador y del lint con baseline como verificación sobre archivos; mapping type→template comprobarlo por parseo del bloque JSON vs filesystem); SIMULATED para el flujo completo de materialización de un tipo dado.

## Unknown / ambiguity

Quién ejecuta el lint `--gate` y con qué cadencia (release gates mencionados pero no especificados); el contrato declara "full-corpus validation is reserved for contract changes, doctor, and release gates" sin definir estos últimos; el comportamiendo del materializador ante tipos con template `null` (sólo `scratch`, que es derivado con exención) no está documentado fuera del bloque JSON.

---

## Closed-club scan result

Scan ejecutado con `grep -rn --include="*.md" "load_policy: always"` sobre todo `/home/kor/secondbrain/main/` (excluyendo `.git/`), más los greps dirigidos a `80-agents/memory/` y `30-resources/agents/skills/` exigidos por el encargo.

Miembros vigentes del closed club declarado (coincide 1:1 con el whitelist de `agents-os-doctor/SKILL.md` Check 3):

1. `/home/kor/secondbrain/main/80-agents/agents-os/agent-constitution.md` (línea 18, frontmatter).
2. `/home/kor/secondbrain/main/80-agents/skills/agents-os-bootstrap/SKILL.md` (línea 14, frontmatter).
3. `/home/kor/secondbrain/main/80-agents/memory/public/user-preference/rjara-agent-profile.md` (línea 20, frontmatter) — el perfil global; es la única nota always-load bajo `80-agents/memory/public/user-preference/` (el directorio contiene además `rjara-meli-work-preferences.md`, `rjara-aranea-operations-preferences.md` y `rjara-vpn-routing-preferences.md`, todas con `when_area_loaded` y ninguna con `always`).
4. `/home/kor/secondbrain/main/80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` (línea 18, frontmatter) — la única nota interna global always.

En el corpus de memoria estricto (`80-agents/memory/` + `30-resources/agents/skills/`), exactamente las 2 esperadas por el encargo: el perfil de usuario (`rjara-agent-profile.md`) y la continuidad interna global (`agents-os-operating-continuity.md`).

Terceros y falsos positivos verificados (ninguno viola el club):

- Copia de distribución `/home/kor/secondbrain/main/30-resources/agents-os/core-export/dist-files/80-agents/memory/public/user-preference/agent-profile.md` (línea 15 declara `always`): es packaging/distribution de AGENTS OS, no una nota viva; `doctor/SKILL.md` Check 1 ordena excluir las copias de packaging bajo `30-resources/agents-os/`, y `/home/kor/secondbrain/main/.graphifyignore` lo materializa con la regla `30-resources/agents-os/` (bloque "AGENTS OS packaging output"). No es candidato a retrieval.
- Menciones en prosa dentro de `/home/kor/secondbrain/main/80-agents/journal/` (sessions, feedback, logs) y proyectos archivados en `/home/kor/secondbrain/main/40-archive/agents-os-*`: son referencias narrativas al contrato, no declaraciones de frontmatter; journal y `40-archive/` están excluidos del corpus por `.graphifyignore` (`80-agents/journal/`, `40-archive/`).
- Notas con `load_policy: never` en memoria pública (3: `memory-tool-format-drift-recovery.md`, `aranea-docs-resource-location.md`, `aranea-agent-ro-sudo-nopasswd-blocked.md`) y en templates (`raw-session.md`, `hygiene-report.md`) y raw sessions de journal: excluidas por diseño, no son miembros del club ni violaciones.
- Conclusión: no existe hoy ningún tercero vivo que viole el closed club. Los únicos 4 archivos con `always` son exactamente el whitelist de doctor Check 3, y en el ámbito de memoria son exactamente los 2 del encargo.

---

Cierre de auditoría: sólo se creó/actualizó este archivo (`/home/kor/secondbrain/main/80-agents/tools/conformance-harness/artifacts/contract-audit.md`). Ninguna contradicción encontrada fue corregida; todas quedaron registradas bajo "Unknown / ambiguity" del bloque correspondiente.
