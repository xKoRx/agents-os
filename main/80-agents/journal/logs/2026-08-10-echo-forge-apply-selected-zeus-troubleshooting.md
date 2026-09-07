---
type: change_log
scope: system
created: 2026-08-10
updated: 2026-08-10
entities:
  - "[[Echo Forge]]"
  - "[[Stager]]"
  - "[[Symphony]]"
tags:
  - kind/changelog
  - project/echo-forge
---

# 2026-08-10 — Echo Forge apply_selected_run / Zeus troubleshooting

- Nuevo known-error: [[stager-go-noop-pending-sync-thrash]] (PENDING en noop reinicia worker).
- Nuevo known-error: [[apply-selected-run-metadata-run-id-mismatch]] (metadata cross-run en wave test).
- Evidencia workflows: `1786323448` (flow_75, mismatch run_id) y `1786366035` (flow_1, thrash stager).
