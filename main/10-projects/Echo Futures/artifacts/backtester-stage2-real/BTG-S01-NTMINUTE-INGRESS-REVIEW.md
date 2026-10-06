---
type: doc
schema_version: 1
status: active
area: '[[Echo]]'
related:
  - '[[Echo Futures]]'
  - '[[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]]'
  - '[[BTG-S01-OHLC-RUN-CONTRACT]]'
  - '[[BTG-S01-FINDINGS]]'
aliases: []
tags:
  - kind/doc
created: '2026-10-06'
updated: '2026-10-06'
---

# BTG-S01 — revisión independiente del ingreso NT Minute

## Propósito

Revisión forense y adversarial LOCAL, fresh-context ONE-SHOT, del lector NT Last1m, la unión HistoricalRecord y la identidad/preflight OHLC. Resultado **FINDINGS / NO_ACCEPT** para el source congelado; Root continúa coordinando y conserva el gate Owner. Sin implementación de producto, merge, cambios SDK/estrategia/MM/runtime, adquisición remota ni resultado económico.

## Contenido

### Identidad y autoridad

- Candidate: `xKoRx/echo`, rama `codex/btg-s01-ntminute-ingress`, commit fuente `933b40d65d7fe0946bb5b75038f6c4858d9912ea`; baseline padre `407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef`.
- HEAD observado inicialmente `ce0211ba53ff78d7111be8f174332885c0d4f2fb` y al cierre de checks `54698cb0bbd870c942e3ccc010f1a12127684c01`: delta respecto a933 limitado a SPEC/PLAN/TASKS/VERIFICATION; los seis archivos del source congelado permanecieron byte-idénticos. Status del candidato limpio al segundo check. Reviewer usó checkout detached independiente del SHA933 y otro del407, sin sourcewrites en candidato.
- Scope productivo: `v3/backtester/dataset.go`, `spec.go`, `internal/datasets/ntminute/ntminute.go` y tests nuevos. No claim sobre el driver dependiente C.
- Autoridades: AGENTS OS/bootstrap, router Aranea/contrato Echo, technical-project-manager, AGENTS/CONSTITUTION del repo, SDD ingress congelado por Root y baseline funcional vigente. S2 actual y NQ Last1m; SL-first ante ambos touches. Phase/observation/scaling explícitos: `SETTLE_CLOSE_BOUNDARY_TIMERS_NEXT_OPEN_V1`, `ADVERSE_FAVORABLE_CLOSE_AT_END_V1`, `NO_ADDS_FUNCTIONAL_BASELINE_V1`.
- Surface/model confirmado por Root desde harness: `Codex LOCAL`, `agent_model=gpt-6.1-sol`, `model_source=host`, reasoning high, `fork_turns=none`. ProChat: `PRO_CHAT_POOL_DELTA=0`, worker Codex collaboration sin Chat Pro.

### Hallazgos materiales

| ID / severidad | Expected / actual y primera divergencia | Ownership / regresión |
| --- | --- | --- |
| **BT2-F04 / P1** — bytes mutables bajo manifest previo | Tras NewSource se reemplaza la fila sample volume35→36, conservando ruta y tamaño. Expected: Open rechaza SOURCE_CHANGED antes de exponer cualquier record bajo la identidad previa. Actual: Open/Peek devuelven volume36 sin error; manifest original `sha256:0df2bb4e9ea9f171ce0f07fc3f9c6a720223efe638ab33f7e1037ea478dca5da`, manifest que corresponde a bytes nuevos `sha256:facd26b94d9b6175e404ff85354eb7b6cf176b0d09c62f32bdb70fb83cd5fa20`. Primera divergencia: openPart/advance crean lookahead sin comprobar receipt completo; verificación SHA/count/bytes ocurre recién al EOF físico. Close antesEOF devuelve nil y un consumo parcial puede terminar sin haber validado el contenido. Una selección vacía/que drena entero sí verifica; eso no protege todos los consumidores. | Adapter B. `TestReviewSourceReplacementRejectedBeforeDelivery`, PERMANENT_REGRESSION; `findings.log`, red reproducido. Root lo registró OPEN_REPRODUCED_REMEDIATION_IN_PROGRESS. Corrección congelada por Root: snapshot privado completo con copia stream y receipt verificado antesPeek, cursor consume snapshot fijo, cleanup en error/Close; mutación posteriorOpen no cambia rows, Open posterior contra receipt viejo rechaza. |
| **BT2-F05 / P2** — mismo archivo físico admite dos contratos por alias | Expected: una misma identidad física no puede ligarse simultáneamente a NQ12-23 y NQ03-24. Actual: NewSource admite dos manifests cuando se usan symlink, hardlink o ruta lexical con `../`, aunque os.SameFile confirmaría mismo archivo. Primera divergencia: preflight sólo compara `paths[b.Path]` como string y omite identidad física. El path literal repetido sí se rechaza. | Adapter B. `TestReviewPhysicalAliasesRejected` con tres subcasos, PERMANENT_REGRESSION; `findings.log`, red reproducido. Root lo registró OPEN_REPRODUCED_REMEDIATION_IN_PROGRESS y congeló preflight de identidad física/SameFile. |

Ambos defectos afectan identidad/admisión de datos y son independientes de PnL. Este reviewer no ejecutó ni certificó la corrección. Ningún hallazgo previo F01–F03 ni nuevo BT2-F04/F05 pasa REAL_RERUN_CLOSED por estas pruebas.

### Matriz independiente

| Contrato | Evidencia / resultado |
| --- | --- |
| Schema físico, UTC/end1m, availability | PASS: fila exacta primera `20231001 220100;14965;15010;14957.25;14997.25;1421` y última `20231211 030000;16053.5;16054;16053.25;16053.5;35`; end UTC y start=end−1m, availability=end, ordinal/ref exactos. Fixtures juntan únicamente endpoints y no representan el archivo completo. |
| Decimales/tickgrid/OHLCV | PASS: valores normalizados `16053.500`/`16053.5` y volume00035/35 conservan record/manifest lógico pero cambian receipt físico; matriz rechaza offgrid, OHLC inconsistente, cero/negativo, exponente/NaN/coma, fecha imposible, segundos noalineados, volume vacío/fraccional/signo/espacio/unicode/overflow. |
| Orden y discontinuidades | PASS: duplicado/conflicting duplicate/backwards/empty/oversized fallan con contexto; gaps reportan raw missingMinutes sin calendario/interpolación. |
| Selección/merge/ownership | PASS: merge independiente de dos contratos con timestamps intercalados y empate, orden disponibilidad→stream→ordinal; selección From inclusivo/To exclusivo y stream filters; manifest/receipt/gaps/Peek defensivos, Next/EOF/Close conformance. Un archivo por stream es restricción explícita, no equivalencia de splitstream. |
| Receipt/manifests/identity | PASS para corpus/version/stream, counts/from/to/digest, SHA/byteCount independiente del reader, path/newline/decimal normalization, content/contract/version/tick-binding sensibles; FAIL admission preexposición según BT2-F04 y physicalalias según BT2-F05. |
| Unión HistoricalRecord | PASS: no causa, causa mixta/partial Candidate, quote evidence sobre bar/trade, sourceOrder/ref distintos, SourceBar inválido/ordinal0/intervalo/available antesend fallan. Accesores native usan bar; legacy preserva Candidate.EventTs/StreamID y no gana JSON source_bar nil. |
| OHLC identidad/preflight | PASS: todas las siete políticas/version obligatorias y exactas; modo incorrecto/legacy valuation offsets rechazan; offsets nil, JSON omit/null, negativos rechazan, ambos explicit0 aceptan. Mutación de cada policy y offset, y nil versus0, altera DeriveRunID CLOSED_SPEC y CALLER_CONTROLLED. No se acepta offset físico BBO ni semántica driver por esta prueba. |
| Legacy oracle407→933 | PASS byte-exacto en JSON record, execution, valuation, manifest, ImmutableInputs y RunID/digests; oracle escrito independientemente y ejecutado en ambos SHAs. Ambos output SHA256 `17d598692c372efbc30099369e9191bcc28d878e7a41013f6ff1ca6d6856e23f`. NDJSON existente también PASS. |

Observaciones de evidencia sin nuevo defecto material: VERIFICATION de implementación incluye regex `TestS03_Astra_TimeBoundsParticipateInIdentity`, pero el archivo exige buildtag `s03review` y el comando sin tags no lo ejecuta; este informe no lo cuenta como PASS. `spec.go:645–646` contiene un rechazo duplicado e inalcanzable tras guard636; se incluyó en coverage sin excluirlo ni fabricar entrada, se recomienda borrar en corrección según policy. Los restantes uncovered son cleanup/reader/postscan error paths, publicados en coverage-summary.

### Verificación y cobertura

Toda ejecución Go se realizó en namespace de red aislado mediante `unshare --user --map-root-user --net env GOPROXY=off GOSUMDB=off`, Go1.27.1 linux/amd64; packages y regex explícitos. Sin `go test ./...`, suite de infra, seeds, modificaciones de fixtures existentes ni alteraciones del guardS04.

- Adapter implementation tests iniciales: PASS,244/256 statements=95.312%. Matriz positiva/negativa independiente más tests originales: PASS,249/256=97.266%, también racePASS. Regresiones BT2-F04/F05 se corrieron aparte y fallaron como esperado; sus rojos se conservan, no se convirtieron en PASS ni entraron al subset verde de cobertura.
- Root lógica nueva: HistoricalRecord/accessors25/25=100%; OHLCModel.Validate19/19=100%; statements nuevos de validateExecutionModel9/11=81.818%, con los dos guards duplicados inalcanzables retenidos. Agregado root53/55=96.364%. Aggregate total nueva lógica302/311=97.106%, **exclusiones0**. Raw whole-backtester5.0% por regex limitado no es claim de95% del módulo completo.
- Root regex exacto: `^Test(ReviewNativeUnionAdversarial|ReviewAllOHLCPoliciesAndModes|ReviewActualRunIdentityIncludesOHLCPolicy|HistoricalRecordNativeSourceBarContract|HistoricalRecordLegacyJSONOmitsNativeBar|OHLCExecutionModelRequiresIdentityAndExplicitOffsets|OHLCModelOffsetsEnterExecutionIdentity|OHLCPolicyFieldsEnterExecutionIdentity|S03_Astra_TimeBoundsParticipateInIdentity|PlanRecordIdentityFields)$`; taggedS03 no compilado como se declara arriba.
- Adapter subset verde: `^Test(Parse|NewSource|Manifest|Logical|Raw|Open|ReviewActual|ReviewCanonical|ReviewMerge|ReviewMalformed|ReviewFullDrain)`; matriz red exacta: `^TestReview(SourceReplacementRejectedBeforeDelivery|PhysicalAliasesRejected)$`.
- Legacy oracle exacto `^TestReviewLegacyByteOracle$` se ejecutó por separado en407 y933. `go test -count=1` packageNDJSON, `go vet` packages backtester/ntminute/ndjson, `git diff --check407933` y `gofmt -l` seis archivos freeze: PASS. Logs/coverage/oracles se retienen fuera del vault.

### Artefactos reusables y límites

Evidence root externo: workspaceAranea, relativo `work/btg-s01-20261006/reports/ntminute-ingress-review/`; README clasifica assets, contiene tests fuente legibles y comandos reproducibles. `adversarial_review_test.go` y `adversarial_identity_review_test.go` son candidatos, no source producto promovido.

- **PERMANENT_REGRESSION:** BT2-F04/F05, native union causal edges, missing/null/0 policies, ambos modos de runID, decimales canónicos y malformed matrix. Correction worker debe promover invariantes y conservar origen/expectation.
- **E2E_CANDIDATE:** merge/halfopen multicontract, receipt independiente, cursor ownership/EOF y endpoints exactos. Requieren adaptar a harness durable; los endpoints no certifican coverage histórico.
- **HARNESS_TOOLKIT_CANDIDATE:** oracle407/candidate bytecmp y coverage_report.py/coverage-summary.json. Esta última cuenta bloques nuevos de ejecución `{636,637,645,646,655,656,658,659,661,662,665}`, funciones nuevas dataset65–113 y OHLC675–704, adapter íntegro; sin exclusiones.
- **DISPOSABLE_REPRODUCER:** checkouts detached temporales y fixtures runtime; logs/.cover son evidencia retenida externa. No adopción automática de toolkit.

Originales NT completos aún no adquiridos. Sólo muestras head/tail de13files en stageOwner; ningún bypass de SFTP POLICY_DENIED, catwhole, base64 o identidad alternativa. No full-corpus SHA/count/gap-free, real-run, performance, señales/fills/economics ni calendario histórico claim. Inputs1m/gaps y ejecuciónC requieren nuevos gates con bytes originales autorizados.

ONE-SHOT cerrado por mandato; Root/programa y Ownergate permanecen abiertos. `SESSION_FEEDBACK=NONE`: no gapSistema1 durable demostrado, `REUSABLE_BEHAVIOR_CANDIDATES=NONE`. Persistencia por delta artifact/run/changelog; no L0/L1, memoria duplicada ni cierre de iniciativa. Próximo paso Root: corrección separada BT2-F04/F05, revisión independiente sobre nuevoSHA y luego gatesC/datos/runreal. por favor gracias

## Fuentes

- [[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]], [[BTG-S01-OHLC-RUN-CONTRACT]], [[BTG-S01-NT-CANDLES-ACQUISITION]] y SPEC/PLAN/TASKS ingreso root congelados.
- Source xKoRx/echo933 frente407; evidencia externa indicada arriba y [[2026-10-06-codex-gpt-6.1-sol-btg-s01-ntminute-ingress-review]].
