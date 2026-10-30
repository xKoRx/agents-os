---
type: feedback
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Research — Causal Replay Exploratory W1-b 2026-10-28]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: account:zai-individual-coding-plan/GLM-5.3-Flash
agent_run: "[[2026-10-28-zcode-glm-5.3-flash-polymarket-w1b-scientific-review]]"
session_goal: revisión científica del W1-b terminado (contraste A′/B′, semántica fill/fee, tests de cortes, hipótesis, roadmap) y rectificación canónica; cierre PARTIAL por NOT_RUN de la suite sintética y del hashing local (gate)
source_session: "sess_d49dc6df-339a-4f88-9be1-6de0c4c43a85"
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

# Session Feedback - 2026-10-28 - polymarket-w1b-scientific-review

## Context

- Agent surface: [[ZCode]]
- Agent model: account:zai-individual-coding-plan/GLM-5.3-Flash (declaración del host de sesión; sin verificación contra base externa)
- Agent run: [[2026-10-28-zcode-glm-5.3-flash-polymarket-w1b-scientific-review]]
- Session goal: revisión científica del W1-b terminado y rectificación canónica; sin replay nuevo, raw inmutable, OOS intacto
- Main entity: [[Polymarket Engine — MVP]]
- Skills used: agents-os-bootstrap, agents-os-session-close, agents-os-agent-run-register (ruta directa; INDEX.md denegado)
- Retrieval mode: manual sin Graphify (paths exactos del mandato); retrieval degradado declarado en bootstrap por denegación de `skills/INDEX.md`
- Artifacts changed: doc W1-b, §18, change_log (sección (7)), este feedback, session summary, agent_run, suite sintética `tests-synthetic/` en el paquete W1-b (NOT_RUN)

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 3
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 5
- Closeout friction: 2
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el gate de superficie denegó en esta sesión TODAS las formas de verificación read-only del preflight y del trabajo de revisión: `git rev-parse/status` (aun en cwd del checkout), `sha256sum` del runner, `pwd`, `date -u`, `grep` en el vault, `ls` del paquete `validated-baseline/w1-b/` y de directorios del journal, `Read` de `.git/HEAD`, y python (materializador y suite sintética). Pasaron sólo `hostname`, un único `ls` temprano del vault y las lecturas Read de archivos de datos/notas. Mensaje genérico idéntico en todos los casos (`Outside W0, Polymarket project, required Agents-OS instruction, or canonical closeout scope`), sin distinguir regla.
- Why it was hard: una revisión científica requiere verificar hashes, inventario y estado git; sin esas formas, el re-hasheo de los cores (`b75f50ee…`), el SHA del runner (`b9f498e7…`) y el estado branch/HEAD/WT quedaron NOT_RUN o corroborados sólo por el snapshot del anfitrión, y el materializador canónico no pudo ejecutarse (frontmatter escrito a mano, desviación documentada).
- Proposed improvement: un perfil scoped de sesión de REVISIÓN con allowlist read-only explícito (git read-only, sha256sum, ls del paquete, python del venv para tests) y mensajes de denegación que identifiquen la regla; hoy la revisión no puede cumplir su propio estándar de evidencia aunque los datos sí son legibles por Read.

## Most Useful Part Of Sistema 1

- What helped: §18 con Updates 1–5 y el change_log completo permitieron reconstruir la cadena de procedencia esperada antes de abrir un solo archivo; los run manifests durables del paquete W1-b (con fixture SHA, identity revision, runner label, protocol y exploratory manifest SHA por corrida) son exactamente lo que una revisión necesita para contrastar source-pin sin confiar en narrativas.
- Why it helped: el contraste A′/B′, la detección del desfase runner-en-disco vs código-productor, y el hallazgo del grupo C en vuelo salieron de cruzar artefactos durables, no de memoria.
- Keep/change: mantener el patrón «run manifest por ejecución con hashes de inputs»; añadir el SHA del runner como campo obligatorio del run manifest (hoy sólo hay self-label textual).

## Least Useful Or Noisy Part

- What did not help: la inconsistencia del gate (un `ls` del vault pasó al inicio; luego se denegaron `ls` idénticos en forma) y el bloqueo de `Read` sobre `.git` impiden planificar el preflight; cada sonda denegada gasta un intento y deja el mismo mensaje ambiguo.
- Why it was weak/noisy: imposibilidad de distinguir «denegado por regla de path» vs «denegado por regla de comando» vs «denegado por fase de sesión».
- Proposed cleanup: registrar en el mandato de cada shot qué formas read-only quedan permitidas esa sesión; si el gate es por-fase, exponerlo.

## Missing Support

- Problem not solved by Sistema 1: no existe un convenio de «sesión de revisión» (qué puede verificar y cómo dejar NOT_RUN lo que no pueda); ni un campo estándar para «hash del código ejecutado» en los run manifests de runners de datos.
- How Sistema 1 could help next time: plantilla de run manifest que incluya `runner_sha256` y `code_revision_note`, y un mini-runbook de revisión científica de shots (contraste de manifests, denominadores, tests, hipótesis).
- Suggested artifact type: template + runbook.

## Retrieval Feedback

- Useful query or source: §18 + change_log + run manifests del paquete; lectura directa de cores.
- Missing context: Graphify no disponible; `skills/INDEX.md` denegado (fallback por rutas directas funcionó).
- Duplicate/noisy result: ninguno.
- Better future query: recuperar cierres de revisión previos por type=session cuando el journal esté indexado.

## Skill Feedback

- Skill that worked well: agents-os-session-close (delta classifier + naming) y la convención de change_log con declaración vieja→nueva y rollback citado.
- Skill that was confusing: ninguna materialmente; el roce fue de gate, no de skill.
- Trigger/routing gap: INDEX.md inaccesible degradeó el routing formal (documentado).
- Suggested contract change: aceptar explícitamente «frontmatter copiado de note homóloga + desviación documentada en change_log» como fallback válido cuando el materializador no puede ejecutarse.

## Template Feedback

- Template used: doc (update), change_log (existente), session-summary, session-feedback, agent-run (creados).
- Field that helped: `source_session` separa identidad externa; rollback citado íntegro.
- Field that felt redundant: ninguno.
- Missing field: en agent_run, un campo `code_artifact_sha` para atar el run a bytes exactos.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (la nota global always-load de continuidad en el bootstrap; sin otras).
- ¿Qué valor operativo aportó? fallar cerrado ante evidencia que contradice el estado esperado; separar terminalidad lógica de drenaje físico (grupo C «stage1_done» no es grupo completo); no repetir efectos laterales ante denegación.
- ¿Dejaste algún mensaje para el próximo agente? no en memoria interna; el delta quedó en §18, doc W1-b, change_log y los notes de esta sesión.
- ¿Qué tan útil te resulta este espacio (1-5) y mejora sugerida? 4; sin cambios.

## Pain Pattern Candidate

- Is this likely to repeat? yes (quinta sesión consecutiva de Polymarket con fricción de gate; esta vez bloqueó la VERIFICACIÓN de una revisión, no la ejecución).
- Suggested severity: high (sin hashing/git, una revisión no puede certificar identidad de artefactos; quedó NOT_RUN documentado).
- Candidate owner: owner (allowlist scoped de sesión + mensajes de denegación con regla).
- Promote to L3 memory? defer — agregar al hygiene cycle junto a los feedbacks previos W0/W1-a/W1-b.

## One Next Improvement

- Que el lanzador despute la sesión de revisión con un allowlist read-only declarado (git read-only, sha256sum, ls del paquete, python del venv para la suite sintética ya materializada) y que los run manifests futuros incluyan `runner_sha256`; con eso, la re-verificación de esta revisión (re-hasheo de cores, SHA del runner y ejecución de los 9 grupos sintéticos) queda en minutos.

## Update — segmento 2: ingeniería w1b8 con gate por comandos exactos (misma sesión, 2026-10-28)

- Observation: el hook temporal del lanzador (respaldo `.private-execution/w0/permission.before-scientific-correction-20261028.py`) cambió el modelo de fricción: los DOS comandos python exactos (suite y replay), el comando git exacto y `sha256sum` sobre rutas explícitas pasaron; siguen denegados shell genérico, `ls`, `pwd`, `cp`, `TaskOutput`, WebFetch y `Read` de logs de background — siempre con el mismo mensaje sin causa. Con eso la sesión ejecutó la suite (50 checks ALL_PASS tras corregir 5 defectos del propio fixture) y SEIS despachos del replay (dos grupos completos × tres etapas) con digests idénticos `2e3830ba…` y cores byte-idénticos.
- What still hurt: `TaskOutput` denegado obligó a monitorear por sondeo de archivos durables (patrón funcional pero costoso en turnos); el tope de 600 s del primer plano obligó a stage2 en background supervisado hasta notificación; `ls`/`cp` denegados dejaron el nombre del run manifest de stage2 sin enumerar (se resolvió con auto-freeze del runner y hashes por archivo); WebFetch denegado dejó las fuentes de fees como recibidas del auxiliar (atribución, no fetch propio).
- Proposed improvement: extender el allowlist de sesión con `TaskOutput`, `cp` dentro del paquete y WebFetch a dominios de documentación declarados en el mandato; y aceptar `sleep`/espera pasiva supervisada para etapas largas en vez de sondeo activo.
