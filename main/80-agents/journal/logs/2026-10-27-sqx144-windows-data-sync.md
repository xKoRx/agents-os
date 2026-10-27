---
type: change_log
schema_version: 1
created: "2026-10-27"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/change-log
  - area/echo
---

# change_log — 2026-10-27 · SQX 144 data sync Windows → flota

- **Nuevo artefacto**: `10-projects/Echo Forge — Operación Real V2/artifacts/SQX144-WINDOWS-DATA-SYNC-20261027.md` — referencia compacta de la sincronización de `user/data` de SQX 144 desde Kronos Windows hacia zeus/hera/kronos/hefesto (veredicto PASS_4OF4 al reemplazo; delta post-arranque documentado en hefesto; backups y rollback en la skill).
- **Repo externo** `xKoRx/symphony`: commit `a4d7968` — skill nueva `.agents/skills/sqx-windows-data-sync/` (SKILL.md, RUNBOOK.md, script coordinador, generador de manifest PowerShell, selftest 30/30). La skill `sqx-instrument-sync` v3.0.0 (Zeus→Linux) queda intacta; la nueva es complementaria y enlaza la frontera de uso.
- **Sin cambios** a constitución, perfil, skills del vault ni entidades más allá del artefacto anterior.
