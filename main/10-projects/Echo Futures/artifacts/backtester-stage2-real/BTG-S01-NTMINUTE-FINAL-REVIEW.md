---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 — revisión final independiente del fix NTminute

## Propósito

Revisar el fix BT2-F04/F05 sobre source congelado mediante probes independientes, comprobación de identidad y cobertura bruta sin exclusiones. **PASS_BOUNDED_LOCAL** del adapter; correcciones documentales explícitas abajo. No aceptación Owner, cierre histórico ni certificación del driver C.

## Contenido

### Identidad y límites de autoridad

- Producto `xKoRx/echo`, rama `codex/btg-s01-ntminute-remediation`, SHA congelado **e44b741e0a6c32d39326b46738dc70565db4759c**. HEAD y status del candidato comprobados antes y después: SHA igual, limpio; source del candidato readonly. Baseline código933b40d65d7fe0946bb5b75038f6c4858d9912ea, docs54698cb0. Reviewer usó dos checkouts detached externos y no editó producción ni tests existentes.
- Artefactos SDD leídos: `specs/btg-s01-ntminute-remediation/{SPEC,PLAN,TASKS,TEST_CHANGE_REQUEST,VERIFICATION}.md`; AGENTS/CONSTITUTION y reglas vigentes, bootstrap/router Aranea/contrato Echo, revisión NT ingress independiente y FINDINGS/perfil funcional del carril Root. Scope local Linux/amd64 Go1.27.1, offline, sin infra, runtime, seeds, SDK/dominio, fixtures existentes ni `go test ./...`.
- Surface/model confirmado por el host mediante Root: Codex LOCAL, **agent_model=gpt-6.1-sol**, **model_source=host**. PRO_CHAT_POOL_DELTA=0, worker Codex collaboration sin Chat Pro. Root sigue coordinando; cierre ONE-SHOT de este reviewer no cierra programa ni consume el gate Owner.
- Hashes del source candidato: ntminute.go `dac91a8eb58afba50b2f49452eeda276f5aa0962802f0543514173d50748773a`; ntminute_test.go `48aade0d24445d6475d69a4ab1e35ee3cbd2b977ee6cadbee257916aa03f4c88`; immutable_source_regression_test.go `be54d3cf62d484348584111cd5b8428e4bf02d53c1aaad3090035904af64022c`.

### Resultado funcional independiente

| Contrato | Resultado / evidencia |
| --- | --- |
| BT2-F04: original distinto al receipt antes de Open | **RED933 / PASS e44**. Head/tail con mismo tamaño, append, truncate y missing rechazan desde Open con cursor nil y ErrSourceChanged. Selección de un solo minuto no puede admitir un prefix cuyo tail cambió. Probe previo independiente también reproduce volume36 bajo manifest viejo en933. |
| BT2-F04: original mutado después de Open | **RED933 / PASS e44**. Corpus sintético de2000 filas, cursor consume1500 y cierra antesEOF; en933 la primera fila afectada aparece en ordinal82, una vez agotado el buffer. En e44 las1500 filas conservan volume35. Dos cursores conservan ownership separado; cerrar uno no altera el otro; Open posterior rechaza bytes nuevos; manifest/receipt/gaps permanecen inmutables. |
| BT2-F05: aliases | **RED933 / PASS e44**. Symlink/hardlink/path lexical se rechazan; con bytes malformed el rechazo de alias precede al scan. La matriz previa prueba aceptación indebida de dos contratos sobre mismo inode en933. Archivos físicos distintos con bytes iguales siguen admitidos por la regresión producto; inode/path no entra al manifest. |
| Merge/selection/parse/identity | **PASS**. Matriz independiente de merge intercalado/empates y rangos half-open, decimales canónicos, malformed/orden y extremos observados. Receipt comparado contra SHA/count de bytes calculados por el probe. Peek defensivo; Next/EOF/Close y guards cerrados conservados. |
| Cleanup / fallos multi-stream | **PASS**. Original eliminado en segundo stream tras snapshot válido del primero: Open rechaza y no deja handles/nombres temporales. Error real de lectura de un snapshot durante Next cierra ambos parts y el cursor; Close posterior idempotente, FD count restaurado. |
| Compatibilidad legacy/root | **PASS byte-exacto933→e44**. Root dataset.go/spec.go, NDJSON y SDK source-idénticos según git diff. Oracle legacy JSON/digests/runID igual, SHA256 `17d598692c372efbc30099369e9191bcc28d878e7a41013f6ff1ca6d6856e23f`. Oracle adapter con path físico normalizado conserva manifest/receipt/record, SHA256 `b29543d35fe8ae6731982a12e5fae8e5a7d9441fe7269fa7e707123b11017093`. Root union causal/model policies/identidad probados explícitamente; taggedS03 no se cuenta como ejecutado. |

Snapshot de e44 se copia stream completo a disco, compara tamaño/hash antes de emitir una fila, reabre sólo lectura y desvincula el nombre; el cursor consume exclusivamente esa copia. No modifica los originales, no carga el corpus entero en RAM y no incorpora paths de snapshot a identidad. SameFile preflight recorre todos los bindings antes de construir el manifest.

### Cobertura y precisión de evidencia

Gate definido: >=95% del adapter nuevo completo contra407, sin exclusiones. No se inventa un gate adicional por helper. El perfil original producto alcanza **286/298=95.973%**, luego la suite completa producto más probes independientes alcanza **290/298=97.315%**, ambos race PASS y **exclusiones0**. Raw whole-backtester no se presenta como95% del módulo.

El diagnóstico de delta933→e44 toma todos los bloques instrumentados Go cuyo span intersecta líneas añadidas/reemplazadas: **48/53=90.566%** originalmente y **51/53=96.226%** tras probes, también exclusiones0. El algoritmo, líneas y bloques completos quedan en `coverage_audit.py`/`coverage-summary.json`; su rango es explícito y no se confunde con el gate del adapter entero. Funciones finales: NewSource41/41, preflight10/10, openPart7/7, snapshotBinding20/22, copyVerifiedSnapshot7/7, cleanupSnapshot1/1, removeSnapshot3/3, Next10/10. Los dos handlers close restantes no se indujeron ni se excluyeron.

**Corrección documental:** `VERIFICATION.md` worker declara56/56 aplicable excluyendo7 statements por no inducir fallos OS/scanner. No se acepta como prueba de inalcanzabilidad ni100% del delta: reapertura, unlink y remove fallan físicamente mediante FIFO/chmod con DAC override deshabilitado en namespace. Worker no define un mapping de bloques reproducible para56/63; este reporte publica sus propios rangos exactos y supersede el claim100%. El gate real pasa por raw adapter, sin depender de esa exclusión.

Cleanup es **best effort con error propagado ante denegación OS**. Probe real de reapertura EACCES rechaza y remueve el snapshot; probe de unlink EACCES rechaza y cierra su handle, pero el nombre permanece mientras el SO niega escritura al directorio. El harness restaura permisos y elimina su propio archivo. No se certifica la frase absoluta «sin snapshot en todos los paths» bajo revocación de permisos; no es pérdida de identidad ni admisión corrupta, y no justifica borrar el handler ni excluirlo de cobertura.

Corrección menor de benchmark: la fila de la función retenida tiene50 bytes y5000 filas suman**250000 bytes**, no255000 como describe worker VERIFICATION. Su tiempo/throughput previo no se reinterpreta como medida del corpus Owner; no se realizó benchmark histórico nuevo.

### Checks ejecutados

- Suite **completa** original adapter antes de incorporar probes: `unshare --user --map-root-user --net env GOPROXY=off GOSUMDB=off go test -race -count=1 -coverprofile=adapter-original.cover ./internal/datasets/ntminute` — PASS286/298.
- Suite **completa** producto+reviewer final: mismo namespace con `setpriv --bounding-set=-dac_override,-dac_read_search`, oracle-output local y `go test -race -count=1 -coverprofile=adapter-final.cover ./internal/datasets/ntminute` — PASS290/298. Dos tests fuente nuevos independientes, sin editar tests viejos; fixtures sintéticos sólo en TempDir.
- Probes RED sobre933: cinco funciones exactas de F04/F05 y prueba large-tail separada; se conservaron los fallos en `red-baseline*.log`. Reused ingress positives/negatives ejecutados aparte sobre e44; su test histórico de rechazo tardío EOF se preserva intacto fuera del producto y queda superseded por early rejection, no se inserta en la suite final. Ningún test producto fue omitido.
- `go test -count=1 ./internal/datasets/ndjson`; root regex `^TestReview(LegacyByteOracle|NativeUnionAdversarial|AllOHLCPoliciesAndModes|ActualRunIdentityIncludesOHLCPolicy)$` y oracle legacy sobre933; `go vet . ./internal/datasets/ntminute ./internal/datasets/ndjson`; cmp de ambos oracles — PASS.
- Guard anti-masking canónico corrió sobre diff real poblado en repo disposable con ambos tests producto. Sólo busca patrones, por lo que se complementó con auditoría exacta del TCR: errores import + bloque aprobado, selección anterior y Peek/Next/Close posteriores byte-idénticos; sin skips ni fixtures modificados. Git diff --check e identidad source — PASS. Staticcheck ausente, no se afirma ejecutado.

### Retención y próximos gates

Evidence externo en workspace Aranea, relativo `work/btg-s01-20261006/reports/ntminute-final-review/`, README/comandos, tests legibles, .cover, logs, oracles, hashes y coverage audit. Heavy reports fuera del vault.

- **PERMANENT_REGRESSION candidates:** F04/F05, early rejection head/tail/append/truncate/missing,2000-row postOpen mutation/shortClose, ownership/closed lifecycle y preflight-before-scan. Regresiones ya presentes en producto son permanentes; probes nuevos requieren promoción explícita posterior.
- **E2E_CANDIDATE:** merge/half-open/raw receipt y logical oracle, multistream fault ownership; requieren harness durable, no prueban un histórico.
- **HARNESS_TOOLKIT_CANDIDATE:** auditor de cobertura, oracle legacy/identity y diff guard poblado; no adopción automática.
- **DISPOSABLE_REPRODUCER:** FIFO/chmod OS-fault probes y checkouts/fixtures temporales; logs y perfiles se retienen como evidencia externa. REUSABLE_BEHAVIOR_CANDIDATES=NONE; SESSION_FEEDBACK=NONE.

Originales13files `C:/Temp/history` siguen **POLICY_DENIED / NOT_ACQUIRED**; sólo head/tail previos. No transferencia completa, bypass, full-corpus SHA/count/gap-free, historical replay ni resultado económico. BT2-F04/F05 quedan **FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED / OPEN_REAL_RERUN_REQUIRED**, no REAL_RERUN_CLOSED. Siguientes gates de Root: integrar source exacto tras aplicar precisiones documentales, verificar driver C/identity, obtener originales por canal autorizado y ejecutar el real rerun. Owner acceptance permanece pendiente.

ONE-SHOT cerrado por mandato. Registro attributable y change_log por delta; sin L0/L1, memoria duplicada o cierre de iniciativa. por favor gracias

## Fuentes

- [[Echo Futures]] y carril Root: vault `10-projects/Echo Futures/artifacts/backtester-stage2-real/BTG-S01-NTMINUTE-INGRESS-REVIEW.md`, `BTG-S01-FINDINGS.md` y `BTG-S01-FUNCTIONAL-BASELINE-PROFILE.md`, leídos desde worktree evidencia autorizado; esas notas no se duplican en esta rama.
- Repo xKoRx/echo, SDD y source933→e44; evidence externo relativo indicado arriba y [[2026-10-06-codex-gpt-6.1-sol-btg-s01-ntminute-final-review]].
