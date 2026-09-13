---
agent: agents-md-gardener
role: AGENTS.md Router Design
task_id: KBC-I
status: COMPLETE
baseline: echo f7ddea18 · symphony 9fad768c · vault 3e1da0b
inputs: AGENTS.md existentes (echo, symphony, vault), wiki recién publicada (30-resources/applications/echo/), repos READ-ONLY
scope: propuesta AGENTS.md minimalistas (draft-only; repos READ-ONLY — los cambios a repos quedan como PATCHES propuestos en este artifact)
started_at: 2026-09-12
updated_at: 2026-09-12
---

## Assignment

- Diseñar AGENTS.md minimalistas tipo router para `xKoRx/echo` y `xKoRx/symphony` (Echo Forge), como DRAFTS dentro de este único artifact.
- Inventariar y diagnosticar los AGENTS.md existentes (tamaño, defectos, violaciones de path-de-máquina), verificar comandos contra build files reales, y evaluar impacto de routing en el AGENTS.md raíz del vault.
- NO editar ningún AGENTS.md real en esta fase.

## Baseline

- Vault: `/home/kor/secondbrain/main` @ `3e1da0b`; wiki canónica publicada en `30-resources/applications/echo/` (00-index, echo-core, echo-forge, echo-forge-integration-boundary).
- Repo echo: branch `feature/e02-control-safety-journal-recovery` @ `f7ddea18` (clean), árbol activo `v3/`.
- Repo symphony: branch `feature/f04-magic-version-handoff` @ `9fad768c`, 1 dirty file (`specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json`), READ-ONLY estricto.
- AGENTS.md raíz del vault: 11 líneas / 87 palabras, sólo bloque managed de bootstrap. Referencia de estilo: router puro.

## Inventory & Diagnosis

### `/home/kor/go/src/github.com/xKoRx/echo/AGENTS.md` (raíz) — 33 líneas / 263 palabras

- Sobra: tabla de topografía con enlaces `file:///Users/rjara/...` (10+ machine-paths absolutos, violación directa de la regla repo+path-relativo), rol de SDD detallado que pertenece a `.agents/rules/08-sdd-governance.md` y `09-sdd-phase-permissions.md`, sin ninguna línea de propósito del repo.
- Falta: invariants always-on (orquestación Flink StateFun no Temporal; receptor Forge produce INGESTED y nunca activación; Echo nunca asigna/recicla magic), comandos autoritativos (no hay ninguno; delega ciegamente a `01-stack-and-tooling.md`), forbidden operations, orden de autoridad, puntero al vault/subdominio echo, freshness, exclusión de legacy.
- No duplica recursos del vault (no existe puntero cruzado en ninguna dirección): no hay routing wiki↔repo.
- Sub-AGENTS.md detectado: `vibe-coding/docs/cursor/AGENTS.md` — 503 líneas / 3.815 palabras, ensayo genérico de "arquitectura agnóstica multi-agente" sin relación operativa con este repo; candidato a archivo/exclusión, no debe cargarse en retrieval normal.

### `/home/kor/go/src/github.com/xKoRx/symphony/AGENTS.md` (raíz) — 53 líneas / 400 palabras

- Sobra: misma tabla topográfica con 6 enlaces `file:///Users/rjara/...` (violaciones de máquina), y un bloque "Inventario de Workers" con 8 líneas de infraestructura operativa (FQDNs, IPs, usuario `kor` y CONTRASEÑA en claro `<REDACTED>`) — secreto hardcodeado y conocimiento operativo que pertenece a `.agents/skills/worker-ssh/SKILL.md`, jamás a un router always-on. Este hallazgo de seguridad debe reportarse al parent.
- Falta: propósito del repo y la distinción crítica módulo root (feeds legacy Zeebe/goka) vs `sqx/` (Forge, Temporal) — un agente nuevo no puede saber dónde trabajar; invariants always-on (1 VM = 1 worker = 1 task; Echo nunca asigna magic; handoff NO cableado); comandos; forbidden ops; autoridad; routing al vault; freshness.
- Sub-AGENTS.md detectado: `vibe-coding/docs/cursor/AGENTS.md` (mismo ensayo genérico; excluir). Junk file `-h` en la raíz (1472 bytes, contenido de salida de CLI): ignorar.
- Nota: los repos NO tienen bloque managed `AGENTS_OS_MANAGED` (sólo el vault lo tiene); los patches propuestos reemplazan el archivo completo sin markers que romper.

### `/home/kor/secondbrain/main/AGENTS.md` (vault) — 11 líneas / 87 palabras

- Correcto: router mínimo, sólo bootstrap managed. No duplicar nada del subdominio echo aquí.

### Comandos verificados (evidencia)

- echo: `.agents/rules/01-stack-and-tooling.md` §2.1 manda por módulo Go `cd v3/<modulo> && go vet ./... && go test -race -cover ./...` (§2.1 enumera 5 módulos: bridge, core, gateway, lab-worker, sdk — L30); los 7 módulos v3 activos provienen de `go.work` (verificado: v3/bridge, v3/core, v3/e2e, v3/gateway, v3/lab-worker, v3/sdk, v3/toolkit), que es la fuente citada por el draft para el catálogo; §2.2 manda `cd v3/front && npm run test:unit | build | lint`. Makefile raíz existe (`make build|test|lint|proto|tidy|mocks`) pero todos sus targets apuntan a v1 (legacy): NO proponerlo como comando activo, marcarlo legacy.
- symphony: `sqx/README.md` §"Build" `go build -o bin/sqx-worker ./cmd/sqx-worker` (+ sqx-watcher, sqx-flowkit, sqx-mt5-worker; binarios verificados en `sqx/cmd/`) y §"Testing" `go test ./... -cover` desde `sqx/`. Root `README.md` línea 68 `go build -o symphony cmd/symphony/main.go` (módulo feeds legacy). No existe Makefile en el repo.

## Proposed: xKoRx/echo AGENTS.md

Contenido completo propuesto (~40 líneas, reemplaza el archivo):

```markdown
# AGENTS.md — xKoRx/echo

## Purpose

Echo Core: plataforma de ejecución y Trade Journal de trading (Go + Flink StateFun + Kafka + PostgreSQL). Árbol activo: `v3/` (v1/ y v2/ son legacy conviviente; no desarrollar allí). Este archivo es un ROUTER: no duplica arquitectura ni contratos.

## Bootstrap (Agents-OS)

Sesión bajo Agents-OS: resolver VAULT_ROOT y ejecutar `80-agents/skills/agents-os-bootstrap/SKILL.md` una sola vez; entity Echo. No escanear el vault.

## Invariants (always-on)

- La orquestación es Flink StateFun vía HTTP; NUNCA introducir dependencias `go.temporal` (Temporal es Echo Forge, sistema upstream distinto).
- Echo es RECEPTOR de la frontera Forge: la ingesta de `HandoffManifestV1` produce sólo receipt `INGESTED`; jamás activación, provisioning ni capital (post-INGESTED no hay consumidores).
- Echo NUNCA asigna ni recicla magic; ownership de identidad (CanonicalStrategyID, seal, Magic V1) es de Forge. Contratos frozen en `v3/sdk/contracts` — no editar sin cambio de contrato formal.
- Gateway queda FUERA del hot path de trading (webhooks/control/boundary Forge).
- Migraciones de PostgreSQL (esquema `echo`) son append-only: no editar migraciones ya aplicadas.
- En task SDD activa, respetar tu rol (coordinator/implementor/verifier) según `specs/SPECS.md` y `.agents/rules/08-sdd-governance.md`.

## Commands (autoritativos)

- Go (por módulo, en los 7 módulos v3 de `go.work`: `bridge|core|e2e|gateway|lab-worker|sdk|toolkit`): `go vet ./...` y `go test -race -cover ./...` (comandos: `.agents/rules/01-stack-and-tooling.md` §2.1; catálogo de módulos: `go.work` — §2.1 enumera sólo 5, sin `e2e` ni `toolkit`).
- Front (`v3/front`): `npm run test:unit` · `npm run build` · `npm run lint` (fuente: `.agents/rules/01-stack-and-tooling.md` §2.2).
- Makefile raíz apunta a v1 (legacy): no usar para desarrollo v3.

## Forbidden

- No editar `v3/sdk/contracts` ni ningún contrato frozen sin decisión formal.
- No simular/mascar tests ni tocar tests existentes como implementor (`10-anti-test-masking.md`).
- No correr la plataforma contra entornos reales ni mutar config de etcd/Hasura de producción desde un agente.
- No force-push ni reescribir historia.

## Authority order

Contratos frozen (`v3/sdk/contracts`) > specs SDD (`specs/`, `specs/SPECS.md`) > código > documentación del repo (`v3/docs/`, `docs/adr/`). AGENTS.md es router, no wiki.

Gobierno vivo (no-regresión): `CONSTITUTION.md` y el catálogo `.agents/rules/00-14` permanecen vigentes y no son reemplazados por este router — las reglas 00-14 son `alwaysApply: true` y única fuente de verdad para CI; la verificación obligatoria `sdd-feature-verification` se rige por `CONSTITUTION.md` y `.agents/rules/`.

## Canonical wiki (vault)

El "qué es / estado actual / gaps" vive en Agents-OS: `30-resources/applications/echo/00-index` → `echo-core` y `echo-forge-integration-boundary`. La wiki manda en estado y frontera; el repo manda en detalle de implementación. No copiar la wiki aquí.

## Freshness

Ante cambio material (nuevo endpoint, contrato, migración, gap cerrado), revalidar las secciones volátiles de `echo-core` (y `echo-forge-integration-boundary` si toca la frontera) en el vault.

## Do not load

Ignorar en retrieval normal: `vibe-coding/` (incl. su AGENTS.md de 500 líneas, ensayo genérico), `ESTRUCTURA_PROYECTO.md`, `SCAFFOLDING_SUMMARY.md`, `search_results.txt`, `build_all_old.sh`, `old-cursorrules`, `PROMPT-*.md`, `PIPE_RECONNECT_FIX_*.md`, `QUICK_START.md` (histórico/vibe), y árboles `v1/`, `v2/` salvo tarea explícita de legacy.
```

## Proposed: xKoRx/symphony AGENTS.md

Contenido completo propuesto (~40 líneas, reemplaza el archivo):

```markdown
# AGENTS.md — xKoRx/symphony (Echo Forge)

## Purpose

Echo Forge: fábrica cuantitativa de estrategias (campaña multi-wave Temporal sobre el motor SQX). Código activo: módulo `sqx/` (Go 1.24 + workers dedicados + plugin Java de SQX). El módulo ROOT de symphony (Zeebe/Camunda/goka, feeds) es el sistema legacy de feeds: NO desarrollar allí salvo tarea explícita. Este archivo es un ROUTER.

## Bootstrap (Agents-OS)

Sesión bajo Agents-OS: resolver VAULT_ROOT y ejecutar `80-agents/skills/agents-os-bootstrap/SKILL.md` una sola vez; entity Echo (área Echo Forge). No escanear el vault.

## Invariants (always-on)

- **1 VM = 1 worker = 1 task en ejecución.** Cada worker SQX procesa UNA activity/task a la vez; prohibido diseñar locks, mutexes, semáforos, slots o workspaces para concurrencia intra-worker. Cambiar esto exige decisión arquitectónica aprobada por el owner.
- Echo NUNCA asigna magic: la asignación Magic V1, seal de versiones y CanonicalStrategyID/StrategyRef son ownership de Forge.
- **El handoff Forge→Echo NO está cableado.** No existe transporte Forge→Echo en producción; `SealStrategyVersion`, `BuildHandoffManifest` y `DeliverHandoff` no tienen caller de producción (capacidad librería, branch F-04). No "completar" el cableado sin decisión de producto explícita.
- La FinalistPromotion V2 es membership estructural (≠ Top N); ranking global congelado `score_descending.v1`.
- Única dependencia cruzada de código: pin `github.com/xKoRx/echo/v3/sdk/contracts` en `sqx/go.mod` — no actualizarlo sin contrato formal.
- En task SDD activa, respeta tu rol asignado: coordinator (sólo specs/planes/checklists, nunca código), implementor (código sólo en `Allowed Files`, no tocar tests existentes), verifier (audita y ejecuta lints/tests, nunca edita código de producción). Mapa completo: `.agents/rules/08-sdd-governance.md` y `09-sdd-phase-permissions.md`.

## Commands (autoritativos)

- Build (desde `sqx/`): `go build -o bin/sqx-worker ./cmd/sqx-worker` · idem `sqx-watcher` · `sqx-flowkit` (fuente: `sqx/README.md`).
- Tests (desde `sqx/`): `go test ./... -cover` (fuente: `sqx/README.md` §Testing).
- Watcher/worker deploy: `run_watcher.sh`, `run_deployer.sh` (raíz) — sólo con instrucción humana explícita.
- No hay Makefile; no inventar targets.

## Forbidden

- No tocar el módulo root (feeds legacy) ni `deployer/` sin tarea explícita.
- No editar contratos frozen del SDK Echo ni el pin de `sqx/go.mod` casualmente.
- No mascar tests ni saltar gates `verify_*` read-only de los workflows.
- No operar workers/VMs del cluster (SSH, deploy, MT5) desde un agente sin instrucción humana; credenciales NUNCA en archivos tracked.
- No force-push ni reescribir historia.

## Authority order

Contratos frozen (F-0x, SDK contracts) > specs SDD (`specs/`, `specs/SPECS.md`; PRD `docs/prd/SQX_Adaptive_E2E_Pipeline_PRD.md`) > código > documentación (`sqx/README.md`). AGENTS.md es router, no wiki.

Gobierno vivo (no-regresión): `CONSTITUTION.md` y el catálogo `.agents/rules/00-14` también existen en symphony y permanecen vigentes (reglas `alwaysApply: true`, única fuente de verdad para CI); este router no los reemplaza.

## Canonical wiki (vault)

El "qué es / estado actual / gaps" vive en Agents-OS: `30-resources/applications/echo/00-index` → `echo-forge` y `echo-forge-integration-boundary` (gaps G1–G7). La wiki manda en estado y frontera; el repo manda en detalle. No copiar la wiki aquí.

## Freshness

Ante cambio material (nuevo workflow, cableado seal/handoff, contrato), revalidar las secciones volátiles de `echo-forge` (y `echo-forge-integration-boundary` si toca la frontera) en el vault.

## Do not load

Ignorar en retrieval normal: `vibe-coding/` (incl. su AGENTS.md de 500 líneas), `resumen_dev.md`, `pr_body.md`, `reports/`, `benchmarks/`, `input/`, archivo junk `-h`, y el módulo root (feeds) salvo tarea explícita de legacy.
```

## Corrections (A-1..A-4)

Post-verificación (artifact 09, tabla V1–V21; veredicto PARTIAL con V10/V16/V17/V18 FAIL menores). Cambios aplicados a los drafts de arriba:

- **A-1 (V10, echo Commands):** el draft ya no atribuye la lista de 7 módulos a `§2.1`. Ahora los comandos (`go vet ./...`, `go test -race -cover ./...`) se citan desde §2.1 y el catálogo de 7 módulos v3 (`bridge|core|e2e|gateway|lab-worker|sdk|toolkit`) se atribuye a `go.work` (verificado en `~/go/src/github.com/xKoRx/echo/go.work`: contiene exactamente esos 7 módulos v3); la nota aclara que §2.1 enumera sólo 5 (sin `e2e` ni `toolkit`). También corregida la línea de evidencia "Comandos verificados".
- **A-2 (V16, echo no-regresión):** añadido al draft de echo un párrafo "Gobierno vivo (no-regresión)" en Authority order que conserva los punteros a `CONSTITUTION.md` (gobierno, verificación obligatoria `sdd-feature-verification`) y al catálogo `.agents/rules/00-14` (`alwaysApply: true`, única fuente de verdad para CI).
- **A-3 (V17, symphony no-regresión):** añadido al draft de symphony el one-liner de roles SDD (coordinator/implementor/verifier, con mapeo a `08-sdd-governance.md` y `09-sdd-phase-permissions.md`) como invariante, y un párrafo "Gobierno vivo" en Authority order que referencia que `.agents/rules/00-14` y `CONSTITUTION.md` también existen en symphony y siguen vigentes.
- **A-4 (V18, credencial SSH — nota de remediación, en este artifact, NO en el draft):** el draft de symphony no replica la contraseña y el Forbidden ya prohíbe credenciales en archivos tracked; falta la parte operativa. Remediación: (a) la credencial del cluster de workers NO debe vivir en ningún archivo del repo; si es operativamente necesaria, debe residir en un secret manager o en variables de entorno/creds untracked fuera del control de versiones (p.ej. `~/.symphony/credentials`, ssh-agent, o vault del owner) y los skills deben referenciar el mecanismo, no el valor; (b) ADVERTENCIA: `.agents/skills/worker-ssh/SKILL.md:40` (y comandos :45-67, :74-99) y `.agents/skills/worker-troubleshooting/SKILL.md:19-24` (tabla de credenciales) y `:116` (y :31-54, :193) de symphony SIGUEN conteniendo la contraseña `<REDACTED>` en archivos tracked — esto contradice el propio Forbidden del draft mientras no se remedie; (c) requiere ROTACIÓN de la credencial por el owner (la contraseña quedó expuesta en git history), fuera del alcance de esta campaña; se reitera como hallazgo de seguridad en Conflicts/Unknowns y Handoff.

## Vault Routing Impact

- Esperado: NONE. El AGENTS.md raíz del vault (11 líneas) es bootstrap puro; el routing a `30-resources/applications/echo/00-index` ya funciona vía `agents-os-bootstrap` (entity Echo → domain router → context retrieval) y la wiki es hoja de `30-resources/applications/00-index`. Añadir un puntero echo en el vault AGENTS.md violaría el principio de router mínimo y duplicaría el bootstrap.
- Nota separada (no cambio): si en el futuro se quiere un atajo por intención ("trabajar en Echo → ver 30-resources/applications/echo/00-index"), el lugar correcto sería el skill de dominio `aranea-agent-dev`, no el AGENTS.md del vault.

## Conflicts / Unknowns

- Secreto en claro: la contraseña SSH del cluster (`<REDACTED>`) está hardcodeada en el AGENTS.md de symphony y SIGUE en archivos tracked en `.agents/skills/worker-ssh/SKILL.md:40,45-67` y `.agents/skills/worker-troubleshooting/SKILL.md:19-24,116,193` (verificado por grep). Fuera de mi scope; ver nota de remediación en `## Corrections (A-1..A-4)`: mover a secret store/env fuera del repo y ROTAR la credencial (owner).
- El Makefile raíz de echo apunta a v1: verificar con el owner si se desea actualizarlo a v3 (fuera de scope de este artifact).
- `make` no verificado por ejecución (build read-only de módulos Go consumiría tiempo; las fuentes de comando son README/rules del propio repo, marcadas como tales).
- Los drafts proponen reemplazo completo de los AGENTS.md de repo (no tienen bloque managed `AGENTS_OS_MANAGED`, así que no se rompe ningún marker).
- La exclusión "Do not load" de `vibe-coding/` asume que nadie la usa activamente; confirmar con el owner antes de aplicar.

## Handoff

- **documentation-verifier debe:** (1) contrastar cada invariante de los drafts contra `echo-core.md`, `echo-forge.md` y `echo-forge-integration-boundary.md` (30-resources/applications/echo/); (2) re-verificar los comandos citados contra `.agents/rules/01-stack-and-tooling.md` de echo y `sqx/README.md` de symphony; (3) confirmar que ninguna línea de los drafts contiene paths absolutos de máquina (regla repo+path relativo); (4) validar que no se copió contenido de la wiki a los drafts (sólo punteros).
- **Aplicación de cambios:** los repos echo y symphony son READ-ONLY para la campaña. Los AGENTS.md de repo NO se escriben: quedan como PATCHES propuestos en este artifact, para que el owner los aplique fuera de campaña (o en una fase autorizada con paths exactos). Si el parent autorizara escritura, el path exacto sería `/home/kor/go/src/github.com/xKoRx/echo/AGENTS.md` y `/home/kor/go/src/github.com/xKoRx/symphony/AGENTS.md`, sin tocar ningún otro archivo.
- El AGENTS.md del vault no requiere cambio (ver sección Vault Routing Impact).
- Acción inmediata recomendada al parent: reportar el secreto SSH en symphony/AGENTS.md como hallazgo de seguridad.
