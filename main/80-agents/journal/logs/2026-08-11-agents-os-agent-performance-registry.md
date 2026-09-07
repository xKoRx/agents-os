---
type: change_log
schema_version: 1
scope: session
created: "2026-08-11"
updated: "2026-08-11"
area:
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Codex]]"
  - "[[Claude Code]]"
  - "[[Cursor]]"
  - "[[Antigravity]]"
related:
  - "[[agents-os-agent-run-register]]"
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

# AGENTS OS — Registro de performance por superficie y modelo

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `80-agents/templates/agent-run.md` y fixture contractual asociado.
  - `80-agents/skills/agents-os-agent-run-register/SKILL.md`, registry de skills, session close y session feedback.
  - `80-agents/crew/INDEX.md` y perfiles `Codex.md`, `Claude Code.md`, `Cursor.md`, `Antigravity.md`.
  - Contrato/schema, note types, templates de feedback, template de perfil, preferencia global y cockpit [[AGENTS OS]].

## Motivo

- Los feedbacks históricos mezclaban IDE/superficie y modelo en texto libre, mientras el feedback event-driven registraba principalmente sesiones con fricción. Esa evidencia no permite comparar confiablemente herramientas ni modelos.

## Fuentes usadas

- [[AGENTS OS]], feedbacks legacy con valores `agent`/`agent_surface`, [[Antigravity]], `70-templates/agent-profile.md`, `session-feedback.md`, `agents-os-session-feedback` y el contrato ejecutable v1.

## Resolución aplicada

- Se creó `type: agent_run` como evidencia compacta en journal, una skill de registro por segmento atribuible, cuatro perfiles canónicos de superficie y dashboards por superficie×modelo. El modelo se conserva como identificador exacto reportado; switches y handoffs crean runs separados; el historial ambiguo no se migra por inferencia.

## Validación

- Contrato `45` tipos / `44` templates / `5` fixtures con `errors=0`; lint strict de fuentes del cambio `0 ERROR / 0 WARN`; materializer `agent_run` resuelto en dry-run; skill de 68 líneas con YAML válido y rechazo esperado del validator portable por metadata federada; Doctor `0/0/0` con startup≈6000; Context Router `14/14`, 0 misses y precisión proxy 100%. El gate all-vault quedó NO-GO por `status: deprecating` en `rio-materializer.md` y `rio-frontend.md`, cambios ajenos a este alcance; no se alteraron ni baselinaron y el reindex quedó deliberadamente bloqueado.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** configuración personal de superficies; sin secretos, paths locales persistidos ni memoria interna.

## Rollback

- Revertir el commit conceptual completo: retirar `agent_run` del contrato/template/fixture, eliminar la skill y los tres perfiles nuevos, restaurar Antigravity/template/dashboard y remover el wiring en perfil, feedback y cierre. No hay runs históricos migrados que deshacer.
