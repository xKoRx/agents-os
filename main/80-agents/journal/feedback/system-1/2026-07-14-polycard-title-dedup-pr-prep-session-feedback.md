---
type: session_feedback
scope: session
created: "2026-07-14"
area: "[[Meli]]"
application: "[[java-polycard-sdk]]"
related:
  - "[[2026-07-14-polycard-title-dedup-pr-prep-summary]]"
load_policy: manual
indexable: false
tags:
  - kind/feedback
  - scope/session
  - area/meli
---

# Feedback de sesión — polycard título dedup + prep PR

- **Qué complicó más:** dos errores propios de lectura. (1) Corrí tests filtrados y disparé `cleanTestFiles` borrando 283 archivos ajenos — no verifiqué `git status` post-gradle. (2) El usuario preguntó por la **caché de search-api-go (Go)** y respondí con BigQuery; confundí "queriable" con BQ. Ambos por no anclarme al pedido literal y al estado del working tree.
- **Qué de Sistema 1 fue más útil:** la nota de continuidad interna y el learning de `SHORT_VERSION` — evitaron re-explorar. El gotcha de Java 17 estaba y sirvió.
- **Qué faltó:** una señal fuerte, cargada temprano, de "revisar daño colateral tras correr build/gradle". Ya se promovió a memoria interna + base auto-memory ([[feedback-no-collateral-file-deletion]]).
- **Dolor repetible:** confundir la fuente de datos runtime (caché) con su mirror analítico (BQ). Registrado en [[reference-motors-catalog-bq-table]] y continuity.
- **Para el próximo agente:** antes de proponer "acceso a X", leer el código de X y separar runtime vs mirror; después de gradle, `git ls-files --deleted`.
