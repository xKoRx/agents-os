---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
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

# 2026-09-19-f04-e06-recovery-exec-one-decision-fresh-run

## Cambio

- **Tipo:** updated / created
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` — nuevo bullet «E06_RECUPERACION_EJECUTADA_SOLICITUD_UNA_DECISION» al tope de Estado actual; corrección de la referencia a «las 3 decisiones» en el bullet previo (ahora apunta a la decisión única).
  - `10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md` — nuevo bullet «Ejecución del mandato maestro — solicitud owner a UNA decisión + prompt corrida nueva» al tope de Estado actual; corrección equivalente en el bullet de recuperación.
  - `10-projects/Echo Forge/Echo Forge.md` — entrada de bitácora «Ejecución del mandato maestro de recuperación».
  - `80-agents/journal/agent-runs/2026-09-19-zcode-glm-5.3-flash-f04-e06-operational-recovery-exec.md` (nuevo).
  - `80-agents/journal/logs/2026-09-19-f04-e06-recovery-exec-one-decision-fresh-run.md` (este change_log).
  - Fuera del vault: `~/aranea/work/f04-cert-f04-01-c9r/OWNER-REQUEST-0.2.103.md` (reestructurada: §9 colapsado de 3 decisiones a 1 go/no-go; header con re-verificación 22:49–22:53Z; §8 apunta al prompt nuevo) y `~/aranea/work/f04-cert-f04-01-c9r/NEW-RUN-FRESH-IDENTITY-PROMPT.md` (nuevo).

## Motivo

- Mandato maestro FORGE «recuperación operacional E-06» (sesión de ejecución): prohibido volver a solicitar tres decisiones abiertas al owner. La solicitud existente pedía (a)(b)(c); se colapsó a UNA go/no-go del paquete integrado porque el drain de RERUN-5 ya es política canónica (no decisión) y la corrida nueva es consecuencia condicionada del deploy PASS. Además el mandato exige preparar la corrida nueva con identidad fresca sin ejecutarla.

## Fuentes usadas

- Monitor durable RERUN-5 (`/tmp/rerun5mon/`, polls 43–45, 22:49–22:53Z); git fetch + `merge-base --is-ancestor` en `symphony-integ` (== origin `3f6cd110`; `origin/master` `0b9742b0` ancestro estricto); `sha256sum` re-computado sobre `release-build/` + `go version -m` (`vcs.revision=3f6cd110…` 3/3); `release-authority` read-back 22:53:37Z (`candidate=0.2.103 CONSISTENT AVAILABLE`); fixtures `090ca4d1…`/`21917e14…`; `RERUN5-NORMAL-PROMPT.md` (contrato heredado §1–§6); notas F-04/E-06/programa del día.

## Resolución aplicada

- Sin cambio de veredicto: `CERT-F04-01 = BLOCKED / OWNER_APPROVAL_REQUIRED`; RERUN-5 preservada viva (drain), lineage NO CERTIFICABLE PARA E-06 R3; cero acciones mutantes (sin autorización). La única acción de autorización queda en `OWNER-REQUEST-0.2.103.md` §9 (una decisión); corrida nueva pre-stageada en `NEW-RUN-FRESH-IDENTITY-PROMPT.md` con identidades write-once renovadas (`cert-f04-01-rerun6`) y blocklist de consumo verificada.

## Validación

- Cero comandos de escritura en repo/flota/SQX/MinIO/IAM; dirty operacional ajeno del checkout principal intacto; campaña viva intacta (0 cancel/terminate); RERUN-5 monitor sin `CAMPAIGN_TERMINAL` al cierre; cada afirmación clave con read-back en vivo (timestamps 22:49–22:53Z en el agent_run).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Revertir los 3 bullets/entradas de entidades Sistema 2; borrar agent_run y este change_log; restaurar `OWNER-REQUEST-0.2.103.md` desde git o backup del work dir y borrar `NEW-RUN-FRESH-IDENTITY-PROMPT.md` si el owner declara la sesión no válida.
