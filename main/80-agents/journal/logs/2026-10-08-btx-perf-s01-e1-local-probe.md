---
type: agent_run_log
schema_version: 1
created: "2026-10-08"
area: "[[Echo Futures]]"
project: "[[Echo Futures]]"
tags: [kind/log, project/echo-futures]
---

# BTX-PERF-S01-E1 — TOP LOCAL probe (baseline + causalidad), 2026-10-08

- **Rol:** TOP/GPT-6.1 Sol ejecutor LOCAL ONE-SHOT; superficie LOCAL Daedalus; sin subdelegación.
- **Baseline:** echo @ `50250a2b0df6106943108bf6bfe57552409f3d13` (codex/btg-s05-id-invariance, clean), binario `66657a99384ff6e622da15cd6953ea34621edc35100b536f118d1ff3918a89fb` (reutilizado del workspace s06, identidad verificada), go1.27.1.
- **Ejecutado:** R BASIC NQU6 prefijo (warmup 2026-07-05T22:01Z→end_exclusive 2026-07-19T23:00Z, bloque con exposición+SL demostrado): COMPLETE 89,6s wall / 163,5s CPU / maxRSS 73,3 MiB. CAMPAIGN mismo horizonte: COMPLETE 90,0s wall / 167,9s CPU / 73,5 MiB, caja 4880 reconciliada. Prefijo común vs artefacto original NQU6: verificación canónica ejecutada (ver cápsula). Causalidad NQZ5 y replay resueltas desde artefactos íntegros sin rerun.
- **Omitido por presupuesto de sesión (no de proceso):** repeticiones R, perfil CPU/allocs (PROFILE_UNAVAILABLE), control fuente blob 7afb8ca verificado pero no ejecutado, H NOT_MEASURED.
- **Artefactos:** `/home/kor/aranea/work/btx-perf-s01-e1-20261008/` (BTX-PERF-E1-EVIDENCE.md + BTX-PERF-INPUT-CAPSULE/ con manifest.json SHA256).
- **Producto:** cero modificaciones; sólo inputs derivados fuera del repo por preparador público (runspec digest `bfa43e5b…` idéntico al original; sólo cambió end_exclusive).
