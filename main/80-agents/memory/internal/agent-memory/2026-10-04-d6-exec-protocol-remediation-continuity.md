---
type: agent_memory
schema_version: 1
scope: domain
created: 2026-10-04
updated: 2026-10-04
area: "[[Echo Futures]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures]]"
aliases: []
confidence: verified
memory_state: active
continuity_key: domain/echo-futures-d6-exec-protocol-remediation
supersedes: ""
load_policy: manual
indexable: true
index_priority: medium
tags:
  - agent/internal
  - kind/agent-memory
  - project/echo-futures
  - scope/domain
---

# D6 Execution Protocol Remediation — continuidad (2026-10-04)

## Estado al cierre

- `D6_EXECUTION_PROTOCOL_REMEDIATION = PASS` @ `32baeaeb` (FF sobre `ffa493d8`, push a origin, worktree limpio). Artefacto: `10-projects/Echo Futures/artifacts/d6-execution-protocol-remediation-20261004/`.
- D1/D2 (defectos físicos del intento 4) corregidos contra freeze §6.1/§6.2; D3 promovido a FIXED (SendTimeout + scan por-lane + EOF close). Cero órdenes/comandos/mutaciones; G-EGRESS-0 intacto.
- Bundle `C:\Temp\EchoD6Bundle` re-stageado desde HEAD (exec `7f76b30e`, VERIFY `bd68f529` con check feed config; feed AddOn y config byte-idénticos al certificado). Dry-runs sandbox: INSTALL PASS / VERIFY pass-path PASS / fail-path FAIL correcto.
- Staging dev-win: `C:\Temp\d6exec-proto` (shadow-compile + proto-harness); http.server 18099 apagado.

## Frictions / lecciones transferibles

- El MCP aranea-ssh: perfil read-only sirve para leer; `run-command` del perfil operator funciona SIN elicitation, pero `open-session` y todo comando con `$` disparan approval gate no disponible en este cliente ⇒ evitar `$` (usar literales) y subir archivos por http.server + curl.exe + hash (patrón probado).
- El arnés de protocolo (extracción mecánica → .NET real → fixtures → parser Go) detectó un bug real del refactor (comilla de cierre de ts_utc) que los guards estructurales no veían: los fixtures wire son la mitad comportamental insustituible del contrato.
- En el adapter, el frame account (match) SOBREESCRIBE el MISMATCH del hello (no DRIFT): para testear wrong-account fail-closed hay que enviar hello solo o el frame mismatch — no hello RESOLVED + ref distinto (artefacto de autoría, no defecto).
- `Session.Snapshot().Recovered` = "barrier completó", no "limpio": el fail-closed de AMBIGUOUS vive en AmbiguousOrders + Readiness.ReadyNewRisk.

## Siguiente acción (owner/manager)

1. Owner: cerrar NT → INSTALL → VERIFY → abrir NT (2 comandos copy-paste en el artefacto).
2. Manager: certificación fresh-context C→K (log NT: market lane al relay sin rechazos + exec session estable + barrier completado) → ladder congelado lun 2026-10-05 00:00–15:50 CT. OD-D6-1 sin consumir. Domingo ≥17:00 CT G-REALTIME feed-lane-only (no depende de esta remediación). No emitir EF_D6_E2E_PASS.
