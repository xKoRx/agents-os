---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-CLI-CURSOR-ONCE-FINAL-REVIEW

## Propósito

Review TOP LOCAL independiente del fix F11. **READY_LOCAL_NATIVE_BASELINE_REVIEW_ONLY**; F11 CONFIRMED_FIXED_WITH_PERMANENT_REGRESSION, cero findings nuevos. Root/S01 siguen abiertos; ninguna aceptación histórica ni S02.

## Contenido

- Source15422c2329164a33a76bf63912491168227660b7 parente63254875b84b9ebe91b26ca138bb5c19843113a; tip revisado limpioe320fef9e98c514309505771331d831bfda4c4d1. Sólo run.go cambia el producto: sync.Once cachea el primer Close. Existingtests y SDK/driver/reproduce/ntminute inmutables. Nuevo SDD VERIFICATION docs-only fb210ac4afeab2315aaa3c424f287c2d9db5a7b3, branchcodex/btg-s01-cli-cursor-once-reviewed; Go bytes permanecen exactos15422.
- Mismo probe público de artefacto CALLER sellado+override AUTO: REDbaseClose2/Peek3/Next1 → PASScandidatoClose1/Peek3/Next1, error original retenido. Spool fail preserva ENOTDIR/PathError y causa secundaria sin Advance; Finish normal/reproduceClose1, bytes iguales. PrimerClose nil/error tipado cacheado, errors.Is/As y128concurrent callers racePASS.
- Directed CLI racePASS8.070s, F08racePASS1.171s, vet/buildexit0; Go1.27.1. FDgateGOGCoff público run/reproduce antesGC []→[]→[] sin snapshots nombrados. Cobertura independiente raw/applicable3/3=100%, cero exclusiones; package59.7% separado. Guard canónico anti-test-masking exactnewregression PASS. Todo en netnamespace aislado, GOPROXYoff/GOSUMDBoff/modreadonly y workspace externo explícito; GC100 en gates normales.
- Fresh failureSOURCE_COVERAGE_INCOMPLETE sellado/integrity con SOURCE_CLOSEcount1; replay sin sidecarsIDENTICAL. Legacy e632→15422 byteequal artefacto SHAd5325ae6cf99725a9e7e23dab1951b1e8fb60468f29a41179a636f5b504c5ad7. OPEN reservado no pliega closed source ni publica OHLC futuro. F09VERIFICATION previa integradaexactSHA91a9c52d95d6c0565fa44b98a9f13c51e9d8eba28e128a498c68ccf642ca1b8b.
- Autoridades refreshed locales: AgentsOSmaster07ea74689eeb56988653cce61cc836be32c0effe; Echoremote-master372af59a7b83604781346613da01e3d510ea1360; S04cd451972b242c8933321e03001decd4b6d778c61; D6d08a30ce9815f820fda7132e20dc42cc345eb8e8 limpio. No network/infra/trading ni nuevo SDK change.
- Artefactos: nueva native_cli_cursor_once_regression_test.go PERMANENT_REGRESSION; copias/probes externos DISPOSABLE_REVIEW_PROBE; capsule/logs/digests VERIFICATION_EVIDENCE fuera del vault. External BTG-S01 workspace reports/cli-cursor-once-review, capsuleSHAd67c84152821c973e0a8176a9f23c08cdb4f37b150a78533be8423dd99facfd1; coverage/source-proof/artifact-digests y logs dirigidos enlazan la evidencia reproducible. No framework/skill nueva.

Todo **SYNTHETIC_REFERENCE_ONLY**. Originales NT completos/digests no adquiridos; REAL_SMOKE/LONGITUDINAL/REAL_RERUN NOT_RUN. Perfil funcional compartido S2+GerardMM/NO_ADDS/Chicago17/SL-firstnextOpen/costes sin cambios; no cierre de finding histórico ni resultado económico. Prior full S2 fresh domain+sealedIDENTICAL129.517s pertenece198f; producer e632 heavyE2E parcial FAILED_HARNESS y anterior timeoutGCoff no son PASS. No se repitieron warmups pesados para este wrapper.

Codex/Work fueraChatPro0 es clasificación, no recibo. Root reporta configuracióngpt-6.1-sol/high; actual runtimeID/usage no expuestos: unknown, sin fabricar. FeedbackNONE, reusableCandidatesNONE; cierre autorizado sólo del worker, sin L0/L1 ni mutación de continuidad Root.

## Fuentes

- Repo xKoRx/echo: specs/btg-s01-cli-cursor-once/{SPEC,PLAN,TASKS,VERIFICATION}.md y deltae632→15422; nuevo SDDVERIFICATION docs-only citado arriba.
- [[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]] y [[BTG-S01-NATIVE-CLI-FINAL-REMEDIATION-REVIEW]]; capsule previa F11SHA74fe84bdca5709a250d9668756f8daed9e77b74b4ac70ca574076dfb896073d7, probe originalfb53453e0c06c4ed4f748cbd2c3509dc0691991dec7218e811afb21a502d4859.
