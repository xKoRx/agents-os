---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
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

# 2026-09-18-f05c-cert-f04-01-c5a-acquisition-blocked

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-18 — Re-adquisición del HTM de RERUN-3 vía MinIO RO` con veredicto `ACQUISITION BLOCKED` + actualización de `Estado de entrada` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C, sin ejecutar gates posteriores, sin tocar symphony)
  - `80-agents/journal/agent-runs/2026-09-18-zcode-glm-5.3-flash-f05c-cert-f04-01-c5a-acquisition.md` (creado)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C5A`: recuperar exactamente un HTM auténtico del RERUN-3 (key/size/SHA256 de la provenance durable C5, sin re-descubrimiento) para continuar la certificación de compatibilidad del build 6182. Prohibiciones respetadas: sin campañas, sin backtests, sin tocar Windows ni hacer downgrade, sin publicar releases, sin RERUN-4, sin ampliar Access Plane, sin credenciales de ETCD/servicios, sin URL firmada persistida.

## Fuentes usadas

- Backlog deferred (deltas C5 y RERUN-3), SPEC-PARSER §3.3, CORPUS, runbook `aranea-minio-mcp`, matriz `aranea-mcps-expert`, contractos del Access Plane (`AGENT-PLATFORM - MCP Access Plane`), sondas vivas sobre `aranea-minio-ro` (registro completo en `~/aranea/work/f04-cert-f04-01-c5a/acquisition-record.md`).

## Resolución aplicada

- Distinción GET vs LIST cerrada con evidencia viva: la conexión preconfigurada de `aranea-minio-ro` apunta al MinIO correcto (`192.168.31.92:9000`); la identidad RO es válida (ListBuckets → `deploy`+`examples`); `HeadObject`, `GetObject` y GET presignado (120 s, curl local, URL no registrada) sobre el objeto exacto devuelven todos HTTP 403 `Forbidden` → denegación de política IAM, no de conector, endpoint, credenciales ni transporte; existencia del objeto no demostrable vía esta identidad y apoyada en la provenance durable C5.
- Vía B agotada contra la matriz certificada: ninguna capability del Access Plane cubre lectura de bytes de `sqx-strategies`; vías alternativas descartadas por mandato (SSH con credenciales de servicio, ETCD, ampliación de permisos por iniciativa propia).
- Blocker refinado y entregado: principal RO afectado (`aranea-minio-ro` service account, policy embedded), operación denegada (`s3:GetObject`, también `s3:ListBucket`), recurso S3 completo, error (403 + RequestIDs `18D66C70BAF0077A`/`18D66C9D9B5C9BAD`), cambio mínimo (statement `s3:GetObject` del objeto exacto en la policy embedded, sin Put/Delete/List ni acceso general) y responsable (owner del Access Plane); alternativa: copia byte-exacta del owner verificable contra el SHA256 durable.
- Sin bytes: la certificación de compatibilidad 6182 no es ejecutable; compatibilidad NO demostrada NI refutada; `CERT-F04-01 = BLOCKED` sin cambio; `MIGRATION: NONE`; allocations `26090011001–005` write-once permanecen; sin branch/commit/allow-list/corpus/SPEC-PARSER.

## Validación

- Cinco sondas ordenadas en una sola capability existente, sin operaciones destructivas, sin segunda auditoría del homelab; la denegación quedó demostrada en tres variantes independientes (HeadObject, GetObject, presign firmado por la misma identidad) y el conector quedó verificado correcto por runbook (S3 target `http://192.168.31.92:9000`).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (sin access keys, sin bearer, sin URL presignada)

## Rollback

- Revertir el delta C5A y las secciones actualizadas del backlog; el agent-run y este change_log son registro histórico (sin efectos laterales que revertir: ninguna mutación en infraestructura ni repos).
