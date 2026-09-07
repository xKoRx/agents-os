---
type: agent_memory
scope: agent
created: 2026-07-15
updated: 2026-07-15
tags:
  - agent/internal
  - project/agentsos
  - area/meli
---

# Continuidad — sincronización local de ramas

- El usuario exige Git local por defecto: no fetch, no ramas creadas desde remoto, no rebase, no reset, no force-push.
- Skill canónica: `30-resources/agents/skills/sync-local-branch/SKILL.md`.
- En `/Users/rjara/fuentes/java-polycard-sdk`, `feature/new-title-motors` existe localmente, `master` existe y `develop` no existe localmente.
- La sincronización solicitada quedó bloqueada antes de cambiar ramas porque faltaba `develop` local. Los no trackeados `.agents/`, `.codex/`, `descripcion_pr.md` y `graphify-out/` no deben bloquear por sí solos una sincronización si no colisionan con archivos funcionales; deben preservarse sin staging.
- No modificar la rama objetivo hasta que exista `develop` local o el usuario indique otra base.

## 2026-07-15 — nueva solicitud

- La solicitud actual confirma `master` como base para `feature/new-title-motors`.
- Ambas ramas existen localmente, pero el working tree tiene archivos no trackeados (`.agents/`, `.codex/`, `descripcion_pr.md`, `graphify-out/`); detenerse antes de `switch`, `pull`, `merge` o `push` y pedir dirección.

## 2026-07-15 — versión propuesta y cierre

- `build.gradle` y `polycard-decorator/src/main/resources/version.properties` quedaron en `8.191.0`; la entrada de Motors se movió a una sección superior `8.191.0` en `CHANGELOG.md`.
- La solicitud posterior no pidió commit ni push; preservar esos cambios locales junto con los artefactos no trackeados.
- Cierre táctico ejecutado: se creó el L0 `2026-07-15-polycard-title-version-sync-raw.md`; no hubo nuevo aprendizaje reusable ni feedback que persistir.
