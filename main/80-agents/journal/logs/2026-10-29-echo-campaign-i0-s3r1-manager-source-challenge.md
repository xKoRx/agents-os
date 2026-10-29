---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures — Optimización de Campañas]]", "[[EF-CAMPAIGN-MODES-DESIGN]]", "[[EF-CAMPAIGN-MODES-I0-LOCAL]]", "[[EF-CAMPAIGN-MODES-I0-S3R1-RETURN]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---

# Echo Futures — manager source challenge I0-S3R1

Se recuperaron en remoto SHA/diff/return del worker `xKoRx/echo@bab3bef1` (62 reporter, 124 legacy, E2E R03, cobertura, no-spawn reportados localmente, no reejecutados CLOUD). Revisión SOURCE contra Go real halló cuatro gaps: M1 P1 `ResearchFundingSummary.other_spend/total_spend` mal mapeado a RESET_PAID/EVAL_COST; M2 P1 Q puede probar con pago net<=0, reverso o cash post-cutoff/unrelated; M3 P2 setup STOW/PLATFORM no atribuible a cuenta pero conocido por kind; M4 P2 revision attempt_id+indices sin compatibilidad del request. R03 no ejerce fees no cero. M1/G4 contradice oráculo positivo sintético. Decisión manager: I0 gate no aceptado; un único microfix I0-S3R2 en reporter/tests/SDD y gate local completo, sin Go, campañas, gastos, trading, merge o deploy. S04-F01/F02 abiertos; manager y programa OPEN; PRO_CHAT_POOL_DELTA UNKNOWN.
