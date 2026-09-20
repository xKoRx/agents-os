---
type: feedback
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Aranea]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-c12-rerun6]]"
session_goal: Mandato F05C-CERT-F04-01-C12/RERUN-6: preflight seal, release/rollout 0.2.103 y campaña física #6 sobre 2993da0
source_session: sess_3cf3822e-5d39-459c-821a-18d26aa39ad1 (ZCode)
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-09-20 - Echo Forge C12/RERUN-6 (defecto #6 y fricción de STOPs)

- Agent surface: [[ZCode]] (daedalus), sesión F05C-CERT-F04-01-C12/RERUN-6.
- Agent model: GLM-5.3-Flash.
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-c12-rerun6]].
- Session goal: cerrar el ciclo de certificación CERT-F04-01 con el source C11 aprobado (preflight de seal, release, rollout y una campaña física).
- Main entity: [[Echo Forge]].
- Skills used: agents-os-bootstrap, aranea-agent-dev (router), agents-os-agent-run-register, agents-os-session-feedback, agents-os-session-close; lectura de runbooks aranea-ssh-mcp/windows-operator y de la wiki de dominio.
- Retrieval mode: Graphify no requerido; lectura enfocada de notas canónicas + fuentes vivas (Mongo/MinIO/ETCD/Temporal RO, logs de worker).
- Artifacts changed: delta de backlog y bitácora de Echo Forge; agent-run; change_log; esta nota; branch symphony `codex/f05-seal-failclosed-delivery-fix` @ `25a5122` (publicado, sin desplegar).

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: seis campañas físicas consecutivas (EXEC→RERUN-6) murieron cada una en un defecto determinístico distinto y siempre en el eslabón aún no ejercitado; el costo por iteración es una campaña de ~3.5 h de MT5 físico más una release/rollout completa entre intentos.
- Why it was hard: los gates previos no incluyen un ensayo del seal con el wiring REAL de entrega (0 keys echo → FailClosedIngress), de modo que el terminal HANDOFF_CREATED (F-04 §11) nunca se había demostrado ni local ni físicamente; el ensayo G1 de esta sesión modeló un ingress aceptante y por eso el defecto #6 no se detectó antes de gastar la campaña.
- Proposed improvement: exigir en el gate G1 de toda certificación un ensayo del consumidor terminal con los doubles que repliquen el wiring productivo (ingress fail-closed incluido) y el terminal contractual declarado en la receta; ampliar el preflight de release con un smoke físico barato (campaign canary de corta duración) cuando la campaña completa cueste horas.
- Observation (fricción de autonomía): los STOPs excesivamente estrechos entre misiones (C9→C9R→C10→RERUN-5→C11→C12) obligaron a re-verificar en cada sesión el mismo contexto (branches, dirty, fixtures, receta) y a volver a pedir autorización para pasos que ya estaban definidos por la propia receta congelada.
- Why it was hard: cada STOP rompe la continuidad de evidencia y consume una sesión completa en reconstruir estado, multiplicando el costo de iteración.
- Proposed improvement: para certificaciones iterativas, autorizar ciclos acotados predefinidos ("diagnóstico → fix RED/GREEN → release → RERUN con identidades nuevas") con límites duros (N ciclos, prohibido tocar contratos), de modo que un defecto determinístico no exija un nuevo mandato para el paso ya definido.

## Most Useful Part Of Sistema 1

- What helped: la nota de entidad [[Echo Forge]] y el backlog de certificación conservaron receta congelada, SHAs, hashes de fixtures y lecciones por defecto; el runbook aranea-ssh-mcp §106 documentó exactamente la firma del pool agotado y su recuperación autorizada.
- Why it helped: permitió ejecutar G0–G4 sin reconstruir decisiones y resolver el bloqueo del plano SSH por el camino documentado en minutos.
- Keep/change: mantener; añadir a la wiki la ruta exacta del evidence JSON de Windows (`C:\ProgramData\Aranea\evidence\stager-evidence-latest.json`) y el patrón de trabajo "worktree + symlink sdk" para compilar symphony fuera del checkout principal.

## Least Useful Or Noisy Part

- What did not help: la visibilidad Temporal del MCP RO (lista/count fallan o devuelven vacío según namespace del perfil) frente al acceso gRPC directo ya usado por sesiones previas (/tmp/thist).
- Why it was weak/noisy: dos lecturas del mismo plano daban resultados contradictorios y costó diagnosticar que el perfil no apunta a sqx-prop.
- Proposed cleanup: documentar en el runbook del MCP temporal el namespace por perfil y marcar explícitamente que la lectura de workflows de producción requiere el camino gRPC autorizado.

## Missing Support

- Problem not solved by Sistema 1: sin SSH operador (pool ssh-mcp) no hay lectura de PG del flujo (flowkit) ni de filas de delivery; el inventario del seal se clasificó con log + MinIO + Temporal.
- How Sistema 1 could help next time: registrar un perfil RO de lectura PG del flujo (o publicar la lectura flowkit vía MCP) para que el inventario de delivery rows no dependa de SSH.
- Suggested artifact type: runbook de certificación F-04 con la matriz de canales mínimos por gate (ya empieza a existir en los deltas; consolidarlo).

## Retrieval Feedback

- Useful query or source: bitácora + backlog de Echo Forge; runbook aranea-ssh-mcp; fixtures con SHA anclado en notas previas.
- Missing context: la ruta del evidence JSON de Windows no estaba en ninguna nota (se encontró por grep en proyectos).
- Duplicate/noisy result: n/a.
- Better future query: "CERT-F04-01 defecto #6 fail-closed delivery" tras esta sesión.

## Skill Feedback

- Skill que funcionó bien: agents-os-agent-project-workflow (implícito) y el par agent-run/feedback del cierre; e2e-gated-validation dio el vocabulario de gates.
- Skill que fue confusa: ninguna grave; el cierre exige recordar que SESSION CLOSE es por pedido explícito (aquí lo autoriza el mandato).
- Trigger/routing gap: el router de dominio aranea cargó bien; no hubo gap.
- Suggested contract change: para mandatos con "SESSION CLOSE obligatorio", registrar en la nota de control que el cierre es parte del alcance del mandato.
