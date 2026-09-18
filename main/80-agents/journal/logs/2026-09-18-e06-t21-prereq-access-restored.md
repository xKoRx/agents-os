---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
application: "[[xKoRx/echo]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
  - "[[Echo Forge]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[aranea-ssh-mcp]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-18-e06-t21-prereq-access-restored

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` (nuevo bullet de estado `E06_T21_PREREQ_ACCESS_RESTORED_MQL_COMPILE_C2_PASS` + errata en bullets R2 y T09b C2 + erratum en fila Forge de la tabla de entrega + fila echo actualizada a `1f59b19b` + nueva entrada de Bitácora)
  - `80-agents/journal/logs/2026-09-17-e06-t09b-c2-correction-freshness.md` (sección «Corrección de acceso (2026-09-18)» appended; texto histórico intacto)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-e06-t09b-c2-correction-freshness.md` (sección «Corrección (2026-09-18)» appended)
  - `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-e06-attestation-exporter-r2.md` (sección «Corrección (2026-09-18, misma fecha)» appended)
  - `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-e06-t21-prereq-access-restored.md` (creado)
  - `80-agents/journal/feedback/system-1/2026-09-18-e06-access-diagnosis-gap-feedback.md` (creado)
  - Repo `xKoRx/echo`: branch `feature/e06-reference-enrollment-binding` @ `1f59b19b` (push FF `cab31f4d..1f59b19b`, docs-only) — `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/VERIFICATION.md` (nueva sección «ACCESO REAL CORREGIDO + MQL_COMPILE_C2 CERRADO (2026-09-18)» + puntero en Status; evidencia histórica intacta)

## Motivo

- Mandato Manager: un Permission denied por SSH directo NO demuestra que mt5-kronos, MetaEditor o el acceso autorizado no existan; no solicitar reprovisionamiento por defecto. Corregir las afirmaciones contradictorias en entidades y handoffs conservando historial, diferenciar existencia/autorización/acceso, y avanzar el prerrequisito físico de T21 con el acceso autorizado y funcional, sin operaciones económicas y respetando los gates del SPEC.

## Fuentes usadas

- Runbooks `aranea-ssh-mcp` y `aranea-mcp-capability-plane`, skills `aranea-mcps-expert`/`aranea-mcp-plane-operator`/`aranea-agent-dev`/`hermes-agent-operator`
- Estado vivo del plano: `GET /status` ssh-mcp, initialize, `tools/list`, probes de auth (bearer por stdin, jamás impreso)
- Log C1 `2026-09-17-e06-t09b-c1-correction-mql-compile.md` (receta de compilación y workspaces)
- Backlog `Echo + Echo Forge — Deferred Certification Backlog` (blocker READ_ONLY_ARTIFACT_FETCH_REQUIRED vigente)
- SPEC v1.2.3 y VERIFICATION/TASKS @ `cab31f4d` (intactos; VERIFICATION extendido docs-only)

## Resolución aplicada

- **Erratum documental:** «sin capability MCP del host Windows» (T09b C2), «falta exacta: terminal/host con MetaEditor autorizado» (R2) y «PHYSICAL NOT_RUN: BLOCKED» quedaron refutados como diagnóstico de capacidad, con errata in situ y preservación del texto histórico.
- **Acceso real:** `aranea-ssh` con perfiles `mt5-kronos`/`mt5-kronos-operator` vigentes y funcionales; única incidencia real = pool de 64 sesiones agotado (503 session-limit con `connections:[]`), resuelta con el recovery documentado (`docker restart ssh-mcp` por `mcps-ops`, baseline + drift cero) y smoke PASS (11 tools).
- **MQL_COMPILE_C2=PASS:** workspaces `C:\MT{5,4}\e06-t09b-c2\`; MT5 0 errors/1 warning (w43 preexistente; ex5 204736 B sha256 `49e95cfb71adbc4e6956a8b6c098b448ddbff38bb03aa8b6c5f1bb7a77e13cdf`), MT4 0 errors/1 warning (w60 preexistente; ex4 198014 B sha256 `179404a01c4e9e6f529133423df82049586438f52e6b51e4f801a05fbff83fc5`).
- **Gap exacto restante (único):** fetch RO owner-gated de un export SQX real (`s3://sqx-strategies/...`) para Version instrumentado §7.2a → nueva StrategyVersion → ingestion E-04 → matriz §22. PHYSICAL sigue PENDING (GAP-ECHO-006) por esa causa, no por ausencia de infraestructura.

## Validación

- Server smoke negativo+positivo (401 unauth / 200+11 tools auth) post-restart; drift cero verificado por `docker inspect` (imagen/contenedor/mounts/puerto).
- 15/15 SHA256 remotos == locales en `mt5-kronos`; logs MetaEditor leídos con `Result:` explícito; artefactos ex5/ex4 hasheados en host.
- `git diff --check` limpio; commit docs-only `1f59b19b` (VERIFICATION.md único archivo); push FF verificado `cab31f4d..1f59b19b`; worktree limpio.
- SPEC v1.2.3, TASKS y código MQL sin cambios (0 bytes de producto en este cambio de vault+docs).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin bearers, sin rutas de vault absolutas; los paths del host de compilación son evidencia del proyecto

## Rollback

- Repo: `git revert 1f59b19b` (docs-only sobre feature branch; master intocado). Vault: revertir los deltas listados (las errata son aditivas y los textos históricos permanecen). Plane: ninguno — el restart de ssh-mcp es estado operacional sin cambio de configuración.
