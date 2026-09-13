---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Personal]]"
project: "[[AGENTS OS - Conformance Harness]]"
application:
entities:
  - "[[AGENTS OS - Conformance Harness]]"
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
  - "[[agent-constitution]]"
aliases: []
confidence: verified
source_session: sess_8c7d3b7a-0c03-407d-be50-724cf2b06d6e
source_feedbacks:
  - "[[2026-09-13-agents-os-conformance-harness-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
---

# 2026-09-13-agents-os-conformance-harness

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Conformance Harness.md` (creado vía materializador; planificador único del proyecto de agente, progress 100, tareas T1-T6 `[x]`, findings F1-F4)
  - `10-projects/Personal/AGENTS OS/AGENTS OS.md` (tarea puente `[/]`→`[r]` añadida; ninguna otra línea tocada)
  - `80-agents/tools/conformance-harness/agents_os_conformance.py` + `rules.py` + `README.md` (creados: harness L0/L1/L2)
  - `80-agents/tools/conformance-harness/artifacts/` (contract-audit, domain-isolation-audit, conformance-scenarios, conformance-spec-v1, adversarial-verification, adversarial-verification-r2)
  - `80-agents/tools/conformance-harness/results/` (runs JSON de verificación)
  - `80-agents/journal/agent-runs/2026-09-13-zcode-glm-5-3-flash-conformance-harness.md` (creado vía materializador)
  - `80-agents/journal/feedback/system-1/2026-09-13-agents-os-conformance-harness-session-feedback.md` (creado vía materializador)

## Motivo

- Mandato del owner: demostrar automáticamente que Agents-OS cumple sus contratos vigentes (bootstrap, cold/warm, switch, aislamiento MELI/ARANEA/DEFAULT, routing de skills, exclusión de deprecated/superseded, minimal loading) con un conformance harness, sin rediseñar el sistema y registrando findings sin auto-corregirlos.

## Fuentes usadas

- Autoridades vigentes citadas en los artifacts: `AGENTS.md`, `80-agents/agents-os/agents-os.md`, `agent-constitution.md`, `agents-os-bootstrap/SKILL.md`, `agents-os-doctor/SKILL.md`, routers de dominio, `INDEX.md`, `30-resources/agents/00-index.md`, corpus `80-agents/memory/`, `_shared/schema-contract.md`.

## Resolución aplicada

- Verificación adversarial en 2 rondas: ronda 1 demostró D1/D2/D3 (falsos positivos de telemetría, sin guarda de fidelidad, crash en vez de SKIP) → corregidos en ciclo 1; ronda 2 confirmó los fixes y halló N1 (cláusula de evidencia de superficie sin ancla) → corregido en ciclo 2 (26 anclas); N2/N3 resueltos; límite de 2 ciclos respetado; residuos documentados como limitaciones en README.
- Hallazgos del sistema NO corregidos (F1-F4 en la nota del proyecto): F1 validador de schema en rojo (entrypoint sin materializador en `agents-os-skill-authoring`), F2 ambigüedad DEFAULT/superficie, F3 vocabulario load_policy sin árbitro, F4 redacción ambigua "token" en memoria interna.

## Validación

- Suite gated: `PASS 4 · FAIL 1 · WARN 4 · SKIP 17` (FAIL = F1, hallazgo real); matriz por escenario: 16 PASS + 1 FAIL + 8 WARN (ambigüedades declaradas) + L2 PASS; pruebas de inyección en /tmp demostrando FAIL ante violaciones y FAIL del guard ante mutación de autoridades.
- Sin L0/L1 de sesión (sin transcript disponible ni pedido); continuidad en la nota del proyecto.
- Graphify: binario no disponible en esta máquina → sin validación de índice; los notes nuevos no requieren reindex por sí mismos (journal excluido; tools/ y projects/ se resuelven en la próxima sesión con Graphify activo).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert` de los commits de la sesión (el vault tiene auto-sync; los archivos son todos nuevos salvo la tarea puente del cockpit, reversible línea a línea). Ninguna autoridad canónica fue modificada.
