---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
  - "[[Echo Forge]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[aranea-minio-mcp]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change Log — 2026-09-18 — E-06 T21: objeto SQX real identificado, sondas vivas y solicitud owner

Sesión ZCode/GLM-5.3-Flash (continuación E-06, baseline echo `1f59b19b`, lane Forge `a1f62a6`). Mandato: desbloquear `READ_ONLY_ARTIFACT_FETCH_REQUIRED` y avanzar T21 al límite de las autorizaciones existentes. Cero cambios IAM/ACL/credenciales; cero rutas no autorizadas; cero órdenes.

## Cambios

1. **`xKoRx/echo` @ `9f3ccc2b` (push FF `1f59b19b..9f3ccc2b`, docs-only, branch `feature/e06-reference-enrollment-binding`):** `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/VERIFICATION.md` — encabezado corregido (MQL_COMPILE_C2=**PASS** como estado vigente; las menciones NOT_RUN en bloques históricos T09b C1/C2, T10 C1/C2 y T11–T20 se conservan como evidencia del estado al momento de cada entrega) + sección nueva «T21 PRERREQUISITO — OBJETO SQX REAL IDENTIFICADO + SONDAS VIVAS + SOLICITUD OWNER LISTA (2026-09-18)»; `TASKS.md` — T21 con estado acotado del blocker (objeto, RequestIDs, rutas agotadas, solicitud owner).
2. **Solicitud owner creada (fuera del vault, espacio operacional):** `~/aranea/work/e06-t21-owner-action/owner-action-e06-t21-minio-getobject.md` — statement `s3:GetObject` puntual (cubre HeadObject) sobre el ARN del MQ5 real de RERUN-3 y, opcionalmente, el ARN del `strategy.sqx` del apply-selected-run, en la policy embedded del principal `aranea-minio-ro`; alternativa equivalente = copia byte-exacta del owner verificable contra SHA256 (precedente C6). Responsable: owner del Access Plane.
3. **Registro en vault:** nueva entrada en «Estado actual» de [[Echo — E-06 Reference Enrollment and Binding]] con el objeto identificado (key/size/SHA256/provenance durable), las sondas 403 frescas y las rutas autorizadas agotadas; fila Forge de la tabla de entrega sin cambios (lane R2 `a1f62a6` intacta).
4. **Agent-run:** [[2026-09-18-zcode-glm-5.3-flash-e06-t21-sqx-object-owner-action]].
5. **Feedback (gap de provenance):** [[2026-09-18-e06-t21-sqx-provenance-digest-session-feedback]] — los registros C5/vault citaban el digest del MQ5 desde el segmento `sha256:f8968dba…` del key; el record durable del uploader (`mt5_exporter`) registra SHA256 de bytes `6c598d79…`; corregido en el registro vigente (VERIFICATION/E-06/solicitud); el fetch resuelve la identidad byte definitiva.

## Hallazgos de esta sesión (nuevo conocimiento operativo)

- **Objeto requerido por T21:** `s3://sqx-strategies/durable/mt5-export/v1/b6a1edea-ba20-4a23-8cde-0201ee22e8f0/b94f1400-e495-4636-8587-516db1cb8cb7/sha256:f8968dba…/final-b94f1400-e495-4636-8587-516db1cb8cb7.mq5` — 282575 B; producido por `mt5_exporter` del funnel RERUN-3 (child `sqx-main-v1-dfa8750c-…`, campaña `sqx-forge-campaign-v1-76aefcec-…`, `EXPORTED` 2026-09-17T23:38:14Z); fue el `source_key` del compile físico Windows (EX5 `6d667d70…`); cadena HTM→EX5 certificada en C6.
- **Permiso vigente de `aranea-minio-ro` re-verificado en vivo:** buckets visibles `deploy`+`examples`; HeadObject/GetObject sobre el objeto exacto → 403 (RequestIDs `18D6879427801BF6`/`18D6879730EAF460`); la concesión C5A/C5B sigue sin aplicar.
- **Rutas autorizadas agotadas:** deploy (sólo releases), examples (fixtures), SSH RO zeus/hera (sin copia residual), scratch Temporal (metadata, no bytes), Mongo Forge RO (réplica vacía), copia C6 (sólo HTM), fixtures `/tmp` (CONTRACT, no física).

## Gates vigentes

- MQL_COMPILE_C2=**PASS** (encabezado corregido). PHYSICAL=**PENDING** (GAP-ECHO-006) con causa única `READ_ONLY_ARTIFACT_FETCH_REQUIRED` (owner-gated, solicitud lista) + matriz §22 con terminal collector real (E2E del gate T21). T21 **NO PASS**. CONTRACT/SOURCE T11–T20 y lane Forge R2 intactos. E-06 NO CLOSED. Nueva StrategyVersion + ingestion E-04 PENDING de la misma única capacidad.
