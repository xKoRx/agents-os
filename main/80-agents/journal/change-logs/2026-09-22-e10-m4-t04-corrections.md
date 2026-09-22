---
type: change_log
schema_version: 1
created: "2026-09-22"
area: "[[Aranea]]"
project: "[[Echo — E-10 Strategy Quality and Eligibility]]"
entities:
  - "[[Echo]]"
related:
  - "[[Echo — E-10 Strategy Quality and Eligibility]]"
  - "[[Echo — E-10 Manager Review M4 — T04 Coverage Safety Corrections 2026-09-22]]"
tags:
  - kind/change-log
  - area/echo
---

# Change Log — 2026-09-22 E-10 M4: correcciones de coverage T04 (M4-R1/M4-R2)

- **Disparo:** mandato NORMAL del Manager Review M4 (`Echo — E-10 Manager Review M4 — T04 Coverage Safety Corrections 2026-09-22`): corregir exclusivamente M4-R1 y M4-R2 sobre el baseline exacto `bea4c099`, preservando M3-P1 y T04 legítimo; STOP tras R2 (el manager revisa antes de liberar T05).
- **Repo `xKoRx/echo` (branch única `feature/e09-execution-copy-reconciliation-fidelity`, push FF `bea4c099..a861e73b`, read-back exacto `origin == a861e73b`, master `5dd998f1` intacto):** commit `bf243307` fix(e10) M4-R1 — un trade CANONICAL verificado dentro del intervalo de un claim VALID_NO_SIGNAL ahora marca la contradicción a nivel de claim (half-open) antes del barrido: el tramo contradicho se degrada a UNKNOWN sin límites (jamás componente VNS ni denominador), el conflicto `TRADE_INSIDE_VALID_NO_SIGNAL` conserva provenance, los tramos no contradichos permanecen y múltiples trades en el mismo claim no duplican conflictos ni duraciones; incluye la corrección del test físico `TestE10CoverageAssemblerPG_ShadowForeignVersionWrongBinding` que esperaba erróneamente 1h de VNS con trade 09:30 dentro de `[09:00,10:00)`. Commit `9c3f347f` fix(e10) M4-R2 — el lector READ ONLY escanea `open_event_time_basis` con `sql.NullString` y `LifecycleTradeSnapshot.OpenTimeBasis` pasa a `*string` donde nil ES la ausencia real (SQL NULL de 065, jamás interpretada como UTC ni como valor probado): el trade queda en `TradesUnverifiableTime` fuera de `TradesObserved` y el digest de inputs conserva la distinción con representación canónica inequívoca (JSON null vs string probado); DDL 065 sin cambios. Commit `a861e73b` docs(e10) — SPEC 1.4.0 (erratum M4 + §3.5 corregido), TASKS sección M4, VERIFICATION §10. Migraciones 001–069 byte-intactas (`git diff bea4c099 -- v3/sdk/postgres/migrations/` vacío); cero cambios S0; `go.mod`/`go.work` delta 0.
- **Vault:** nota `[[Echo — E-10 Strategy Quality and Eligibility]]` — nuevo estado en 📊 Estado actual, tabla de entrega actualizada (HEAD `a861e73b`, SPEC v1.4.0) y entrada en 📆 Bitácora (M4 ejecutado y publicado; `POLICY_RATIFICATION=UNACCREDITED`; `PHYSICAL/INTEGRATION=PENDING`; T05–T10 NOT AUTHORIZED; DETENIDO TRAS R2). Agent run: `[[2026-09-22-zcode-glm53-e10-m4-t04-corrections]]`.
- **Evidencia:** ROJOs capturados contra el árbol sin corregir (R1: 4/4 herméticos conservaban exposición VNS + test físico FAIL con `ValidNoSignal:1h0m0s` pese al trade interno; R2: FAIL con el error exacto `converting NULL to string is unsupported` en la columna 5); VERDE con worktree aislado `/home/kor/aranea/work/e10-m4-t04r1r2-20260922/echo` (detached `bea4c099`, sin reset/rebase/force) y instancia descartable EXCLUSIVA E-10 :15467 (marcador físico + tabla de identidad del arnés; run.sh cadena 001–069 PASS antes y después); domain `-race` PASS, `TestE10*` postgres `-race` PASS; failing set 121/121 idéntico por nombre al baseline (apples-to-apples); M3-P1 policy pin PASS sin drift; E-08/E-09 no re-ejecutados (fuera del delta, arneses exclusivos propios; no-efectos demostrado por el failing set completo).
