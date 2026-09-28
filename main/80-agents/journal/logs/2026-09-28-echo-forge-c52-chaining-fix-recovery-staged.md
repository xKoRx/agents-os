# Change Log — 2026-09-28 — Echo Forge C5.2: fix de chaining (0.2.130) + recovery wave2a staged

- **Actor:** ZCode (GLM-5.3-Flash), 17.ª sesión Shot Precision, mandato owner "RECOVERY C5.2".
- **Repo xKoRx/symphony (master `b2e321d` → `ca07f72`, pushed):**
  - `3765d14` fix(workflows): gate de cohort artifact-aware en `handleGroupTask` (A1 chained carriers / A2 truly empty / A3 CONTRACT_CONFLICT fail-closed) — defecto wave1z.
  - `dd6c4bb` docs(spec,skill): SPEC `FEAT-SQX-WORKFLOWS-GENERIC` §4.2 con el contrato de 3 estados.
  - `0a10612` style: gofmt del arnés (`sqx/workflows/group_chaining_test.go`, nuevo, T1–T7).
  - `af8f1ae` release: publish 0.2.130 (manifest; worker sha `98291e1c…`, watcher sha `d810bed2…`).
  - `ca07f72` docs(skill): canales de verificación de rollout sin SSH certificados (series de arranque Prometheus + pollers Temporal).
- **[[Echo Forge — Operación Real V2]]:** bitácora 17.ª + actualización de la tarea C5.2 (fix desplegado 2/3; recovery wave2a staged/blocked por Hera offline).
- **Agent run:** `80-agents/journal/agent-runs/2026-09-28-zcode-glm53-forge-recovery-c52-chaining-fix.md` (outcome partial: Parte A completa, Parte B blocked_runtime).
- **Fuera del vault:** paquete recovery + artefactos en `~/aranea/work/forge-recovery-c52-20260928/` (RCA, FIX-VERIFICATION, FULL-RECOVERY-INPUT.csv 34/34, RECOVERY-STATUS.md con runbook, SHA256SUMS).
- **No ejecutado:** despacho de wave2a (preflight flota 3/3 incumplido: Hera 192.168.31.111 offline a nivel de red; rollout 0.2.130 certificado 2/3 — Zeus/Kronos por Prometheus+pollers).
