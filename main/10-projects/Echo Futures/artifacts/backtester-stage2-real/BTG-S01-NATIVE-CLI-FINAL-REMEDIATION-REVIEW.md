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

# BTG-S01-NATIVE-CLI-FINAL-REMEDIATION-REVIEW

## Propósito

Revisión TOP LOCAL independiente ONE-SHOT del candidato CLI congelado `e63254875b84b9ebe91b26ca138bb5c19843113a`, parent `6ef303f57739f0b2a44288f387b377d145eeceac` (docs sobre source `198f29f44bc6e58dd445c9a9b5ee1adfdade2ae9`). Bootstrap AgentsOS cold una vez, routing Echo/Aranea y autoridades reales Echo/SDD leídas. Producto sólo lectura, sin modificaciones de producción ni tests existentes. Documentación en rama aislada `codex/btg-s01-native-cli-final-remediation-review-record` desde master `07ea7468`.

## Contenido

### Veredicto congelado

`REMEDIATION_REQUIRED_EXACT_ONCE_GATE` para `e6325487`: F09 y F10 pasan sus regresiones independientes; nuevo `BT2-F11 LOW` incumple cierre único en un retorno temprano de re-admisión después de EOF. No se emite `READY_LOCAL_NATIVE_BASELINE_REVIEW_ONLY` mientras Root no resuelva ese gate. Separadamente `BLOCKED_EXTERNAL`: no existen originales NT transferidos ni corpus autenticado/digests completos; `REAL_SMOKE`, `LONGITUDINAL` y `REAL_RERUN` permanecen `NOT_RUN`, sin cierre de findings históricos ni aceptación Owner. Toda evidencia actual es `SYNTHETIC_REFERENCE_ONLY`.

### F09 / F10 — comprobación independiente

- Mismo probe público F09 con GC desactivado: baseline198f RED conserva error spool y snapshots FD `0→1→2`; correccióne632 PASS mantiene `0→0→0`, sin archivos snapshot nombrados persistentes. Tests permanentes de run/reproduce pasan. Error original preservado por `errors.Is(ENOTDIR)` y `errors.As(*os.PathError)`; con fallo secundario Close, ambas causas siguen encontrables. Spy sobre fuente native real confirma `Close1 / Peek0 / Next0` en los cuatro casos de spool run/reproduce con/sin error secundario; ninguna reserva, avance, admisión o cálculo económico de cleanup.
- Normal Finish y reproducción sin script cierran una vez y generan bytes iguales. Scope contiene autenticidad no adjudicada, NO_ADDS, warmup/horizonte aportado por caller, AvailableAt y ausencia BBO/LIVE parity; Fidelity sigue `OHLC_1M_MODEL_V1`. Guard serialización year0000→year-1 sigue siendo error alcanzable, no bug ni exclusión.

### BT2-F11 LOW — doble llamada Close después de EOF y rechazo de re-admisión

Dataset reproducible: dos filas de `writeNTFixture`, misma fuente NT native real del adapter, UTC end1m; no mock de parser ni modificación de producción. Se crea y verifica un artefacto CALLER_CONTROLLED válido con cashflow admitido en `warmup+30s`, efectivo en EndExclusive y pendiente sellado. El comando público `reproduce --result <sealed> --spec <valid AUTO spec> --nt-source-config <same descriptor>` alcanza el rechazo original `EnqueueControl requires CALLER_CONTROLLED mode`. `readBaseline` devuelve el script verificado y el mismo seam ejecutado con wrapper contador registra `Close2 / Peek3 / Next1`.

Primer divergence: driver EOF ya llamó `sequenceCursor.Close`, pero `sequenceSource.cursor` conserva la propiedad; defer ante el error re-admission vuelve a llamar `closeCursor`. Esperado Close1, observado Close2 en `TestReviewerOwnershipPublicValidSealedScriptOverride`. El native adapter Close es idempotente: no se observó segunda operación FD, fuga, cambio económico ni pérdida del error original. Severity LOW refleja ese límite; la regla solicitada de exactamente una llamada todavía falla. Owner del arreglo: wrapper CLI, sin justificación para alterar NewRun, ResultWriter, APIs SDK o motor. Regresión pendiente de Root; este reviewer no repara producto.

### Gates y cobertura

Todos los Go checks dentro de `unshare --user --map-root-user --net`; loopback DOWN, `GOPROXY=off`, `GOSUMDB=off`, `GOFLAGS=-mod=readonly`. `GOGC=off` sólo para prueba FD inmediata; dominio y fresh subprocesses `GOGC=100`. Compiler observado `go1.27.1 linux/amd64`, módulos `go1.25.5`.

| Gate | Resultado observado |
| --- | --- |
| Directed race ownership/Scope/native routing/legacy folds/prepare + probes | PASS, 6.470s package time; el nuevo F11 se ejecutó después y falla por separado. |
| F08 selected account-day regression race | PASS, 1.260s; Chicago17, DST/civil/year, EndExclusive y legacy cubiertos. |
| vet / build CLI offline | PASS, exit0 ambos. |
| Fresh short sealed SOURCE_COVERAGE_INCOMPLETE / integrity / sin sibling spec / fresh reproduce | PASS, IDENTICAL; un SourceClose y input_sequence `sha256:4edc67cfa29899e4eda363895b7846c6c92dd070907ebdbf3ac5ecd487db903b`. |
| Legacy NDJSON same bytes198f→e632 | PASS artifact SHA256 `d5325ae6cf99725a9e7e23dab1951b1e8fb60468f29a41179a636f5b504c5ad7`; mismo RunID/InputSHA/state. |
| Exact changed production blocks all3files | Independiente raw42/42 =100%; applicable42/42=100%; exclusiones0. Package67.5% informado aparte. |
| Public verified sealed re-admission EOF ownership | FAIL Close2 esperado1; F11 pendiente. |
| Source proof | HEAD exacto/clean inicio y fin; sólo3 production Go files + nuevo test Linux, SDD/docs; ningún test existente modificado; SDK, ntminute y F08 bytepaths sin delta. |

No nueva corrida larga S2/MM en paralelo al productor: la evidencia independiente anterior198f de COMPLETE con operación S2/MM real + SL_FIRST + fresh IDENTICAL (129.517s) conserva esa procedencia previa; la lectura del diff demuestra ausencia de delta domain/SDK/parser. El productor informó timeout10m de su E2E con GOGCoff y rerun GOGC100 en curso al freeze: no se considera PASS ni se presume causalidad ambiental. Tampoco se convierte el race previo de suite amplia cancelado/timeout624.35s en PASS. No se tocaron D6, infraestructura, funded/campaign/Optimizer, economics o risk.

### Evidencia durable y cierre del worker

Raíz externa resoluble desde workspace Aranea: `work/btg-s01-20261006/reports/native-cli-final-remediation-review/`. Pesados/probes quedan ahí; vault sólo conserva esta referencia. `artifact-digests.json` enumera SHA256 de logs, probes, raw coverprofile y source proof. Capsule `findings-capsule.json` SHA256 `74fe84bdca5709a250d9668756f8daed9e77b74b4ac70ca574076dfb896073d7`; `coverage-independent.json` SHA256 `016d2969f18dbfb7b02dec773561a757686a9bcd88acb4da90b9825087721214`; profile SHA256 `9bf94b382c8439feffbf197c6a2065f788ca703f7bf51b66f97261bef40b2f7d`; probe ownership SHA256 `fb53453e0c06c4ed4f748cbd2c3509dc0691991dec7218e811afb21a502d4859`; public F11 log SHA256 `855ed6bd8b283af9164b636b97155027e4dcc54d3bec5c2d51afd32c921c7274`. Capsule previa F09/F10 verificada SHA256 `4d8d01c67dc27ee0a26e86f20fdf1fbed3d399520fca5107896e38f04dcbadda` en sibling `native-integrated-final-review/`.

Run-register atribuible Codex, modelo host exacto no expuesto → unknown, model_source unknown; Root informa requested/configured `gpt-6.1-sol` con reasoning high, sin receipt runtime independiente; ProChat0, sin receipt falso. Feedback `NONE`: no fricción durable AgentsOS nueva; un comando inicial apuntó al cwd distinto al go.work y fue corregido antes de obtener evidencia, no se usó ese setup failure como RED. Reusable candidates `NONE` válidos: finding específico queda en cápsula/control, sin memoria genérica artificial. Cierre autorizado sólo de este worker; Root permanece abierto y no se cierra el programa. Root confirmó gate F11 y despachará corrección NORMAL fresh acotada al wrapper desdee632, seguida de nuevo TOP independiente; este worker no reabre ni rerunea otro candidato. Luego corpus original antes de gates REAL.

## Fuentes

- Repo Echo: `AGENTS.md`, `CONSTITUTION.md`, reglas reales00–10; `specs/btg-s01-native-cli-final-remediation/{SPEC,PLAN,TASKS}.md` frozen y `specs/btg-s01-nt-cli/{SPEC,PLAN,TASKS,VERIFICATION}.md`.
- Autoridad perfil functional recuperada desde carril evidence: BTG-S01-FUNCTIONAL-BASELINE-PROFILE; sharedS2 + GerardMM reales, SIM/GENERIC100K100000USD, FIXED2000/1500 todo account-day, Chicago17, NO_ADDS, costes2.49/lado+1tick+offsets1/1, modelo SL_FIRST_NEXT_OPEN y LastNQ1m; sin atribución a perfil económico físico.
- Evidencia externa `source-proof.json`, `baseline-red.log`, `fd-pass.log`, `directed-race.log`, `independent-f08-race.log`, `independent-vet.log`, `independent-build.log`, `readmission-eof.log`, `public-readmission-eof.log`, `coverage-independent.json` y probes reproducibles. Ningún original histórico adquirido.
