---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-PROD-PRD5-MANAGER-REVIEW-20261026]]"
  - "[[EF-PROD-PRD5-DEV-PREFLIGHT-AND-COVERAGE-20261026]]"
  - "[[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]"
  - "[[Echo Futures — Runtime Pools]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# EF-PROD PRD.6 — Final Recovery Migration Closure (2026-10-26)

## Propósito

Evidencia consolidada del cierre PRD.6 (mandato Owner 2026-10-26 sobre el dictamen [[EF-PROD-PRD5-MANAGER-REVIEW-20261026]]): corregir los tres P0 (G5A seal sintético, G5B backup no independiente, G5C migración legacy) y el QA, dejando el procedimiento seguro y ejecutable sobre el MISMO Flink DEV de .75. Sin deploy, sin reinicios del job compartido, sin PROD, sin topics nuevos en Kafka DEV. Ejecutado por Submanager GLM-5.3-Flash LOCAL; verificación independiente y dictamen Manager separados.

## Veredicto

```text
STATUS: READY_FOR_MANAGER_REVIEW (pendiente dictamen del verificador independiente y re-review del Primary Manager)
SOURCE_SHA: 1a5c6d8741d539fddc96eb2d1066b46dd2ea2707 (origin/feature/ef-runtime-pools, REMOTE_VERIFIED; delta c2d71357..1a5c6d87 = 4 commits producto + 1 merge de cobertura tests-only)
RELEASE: /home/kor/opt/echo-dev/releases/63f241c0… + 1a5c6d87 (BUILD.md con sha256 por binario; vcs.modified=false)
A (P0-G5A): seal reescrito — frontier REAL del checkpoint vía sonda Java (deserializador propio de Flink 1.14.3: MetadataV3Serializer + backend serialization proxy), join 1:1 checkpoint↔REST↔module.yaml desplegado; HWM prohibido para offsets (divergencia medida en lab: HWM 20 vs frontier 19); campos reales (JobGraphDigest del inventario unido, CompletedAt=REST, digests=sha256 de archivos, revision=ETCD mod_revision, DomainScope derivado); toda brecha ⇒ BLOCKED
B (P0-G5B): copia independiente COMPLETA (chk dir entero + dependencias referenciadas bajo el job dir) re-hasheada desde las copias + anexos (checkpoint-objects, job-graph); LAB S-R FULL PASS: restore DESDE LA COPIA con el original YA ROTADO por la cadencia (num-retained), latest.restored=chk-2602 en la copia, attest EXTERNAL CLEAN, contador 41→45 sin reset
C (P0-G5C): migración ONE-SHOT declarada EN EL MANIFEST (continuity_migration: MIGRATE_LEGACY_ONCE): guard RECOVER_MIGRATE estampa MIGRATED_LEGACY con provenance (checkpoint id + digest del corte) SOLO sobre keys roster-ACTIVE (jamás BIRTH, nada más se toca); sweep por el canal attest EXISTENTE (echo/recovery_attestor → probes → acks con el outcome del PROPIO barrier → reporte firmado → validación contra el roster → evidencia CAS en ETCD); LAB S-M FULL PASS: legacy (HARNESS sin markers) → restore → migración → checkpoint → seal gen2 STRICT → restore estricto con contador avanzando (46→48) y re-abertura REFUSED
D (QA): batería completa 101 paquetes — new-code 840/934=89.94%, diff-aware 220/266=82.71%: BAJO el piso GOD-03 ≥95%; NO PASS; excepción clasificada al Manager (gaps: broker/REST vivos y marshals defensivos; los caminos de integración real están demostrados FÍSICAMENTE en el lab)
LAB: /tmp/ef-prd6-lab loopback estricto (etcd :12382, kafka :28094, flink :28083, svc :28082); evidencia cruda en evidence/ y logs/
PROD_UNTOUCHED: SÍ — cero escrituras PROD; el Flink DEV compartido NO fue tocado (el lab es loopback aislado en daedalus)
VENTANA: tarjeta GO/NO-GO exacta lista (evidence/WINDOW-CARD-PRD6.md) — primer paso = corte completo verificado ANTES de detener nada; jamás arranque sin restore-args; rollback R1/R2
HALLAZGOS DE LAB CORREGIDOS EN SOURCE: (1) lectura del _metadata vivo por path validado contra la autoridad Flink (el containment del storage-root bloqueaba el seal in-container); (2) submit-intent create-once bloqueaba TODO restore posterior → retirement on CLEAN attest + rotación FORWARD por generación (lateral sigue prohibido); (3) one-shot de migración comparaba el manifest activo GLOBAL en vez del MISMO lineage
```

## 1. Delta y piezas por mandato

| Mandato | Implementación | Tests |
|---|---|---|
| A | `seal.go` reescrito (join `joinFrontier` + copia `copyCheckpointComplete` + campos reales), sonda `v3/core/tools/flink-checkpoint-probe/` (Java, compila contra flink-dist 1.14.3), `checkpoint_probe.go` (reglas de fusión fail-closed), `readiness.go` (+JobVertices/+completion time), `module_ingress.go` (parser de ingresses), `seal_auth.go` (fuentes reales) | `seal_blocks_test.go`, `seal_gaps_test.go`, `seal_g5_blocks_test.go` (worker), `checkpoint_probe_integration_test.go` (bytes reales del lab), `module_ingress_gaps_test.go`, `prdd6_gaps_test.go` |
| B | copia completa + anexos + restore-args a la COPIA; tarjeta P1/P2 (savepoint relocatable + off-host a .161:/srv/echo-work) | happy path de copia + `copyCheckpointComplete` unit + LAB S-R físico |
| C | `migration_protocol.go` (probe/ack/sweep/report firmados), `owner_continuity.go` (RECOVER_MIGRATE + provenance + tally por tipo + HandleContinuityProbe en los 7 owners), `sweep.go` (tally), `recovery_attestor_wiring.go` (fan-out/acks/reporte), `migrate.go` (CLI `continuity-migrate`), `manifest.go` (+continuity_migration), `continuity.go` (+MIGRATED_LEGACY +provenance), `recovery_gate.go` (wiring por manifest) | `prdd6_migration_guard_test.go`, `sweep_test.go`, `migration_protocol_gaps_test.go`, `migrate_test.go`, `restore_lifecycle_test.go` + LAB S-M físico |
| D | cierre de cobertura propio + worker `wrk-prd6/cov` (tests-only) integrado | QA-REPORT.md |

## 2. Sin alteración de Strategy/MM, FEFB o Ninja

`git diff c2d71357..1a5c6d87 --stat`: cero toques a kernels económicos (strategy engine/money manager/sizing), adapters NT, AddOn C#, relay/feed. Los owners futures sólo ganaron el bloque de probe (respuesta del barrier, sin ruta económica). gofmt ajeno: cero (un gofmt masivo temprano fue revertido del historial antes del push).

## 3. Flink StateFun 3.2 y Kafka compatibles

- La sonda compila y corre contra el flink-dist 1.14.3 de la MISMA imagen del master DEV (`apache/flink-statefun:3.2.0-java11`); fixture de bytes reales en el repo (`testdata/flink114-chk-metadata`) con test de integración.
- El manifest es ADDITIVE (campos nuevos `omitempty`); wire types ValueSpec sin cambios; los únicos topics usados son los ya declarados del release PRD.5 (recovery-attest.v1); CERO topics nuevos.
- 17 ingresses: el seal certifica EXACTAMENTE los operadores del checkpoint (17 en el job DEV vigente); ingress nuevo del release (attest) entra con la PRÓXIMA generación, no en el corte sellado.

## 4. Rollback sin pérdida

R1 (pre-efecto): restore desde el ORIGINAL intacto (P1 nunca lo borra ni mueve) o desde la copia verificada; R2 (post-efecto): forward-fix, jamás snapshot anterior. Ambos con attest obligatorio post-boot. Detalle exacto en WINDOW-CARD-PRD6.md.

## 5. Estado y siguientes pasos

1. Verificador independiente ONE-SHOT: en curso (intentos previos caídos por red del proveedor; este es el 3.º) → VERIFIER-REPORT.md.
2. Re-review del Primary Manager (esta evidencia + verificador) → G-IMPL.
3. Sólo entonces, ventana Owner con la tarjeta (orden 0-10; el desarme FX/Futures vigente se mantiene; Ninja feed sigue NOT_INICIADO).

## Fuentes

- Workspace externo `~/aranea/work/ef-prd6-20261026/`: `briefs/{PRD6-DESIGN,LAB-BRIEF,VERIFIER-BRIEF,COV-BRIEF}.md`, `evidence/{LAB-REPORT,QA-REPORT,WINDOW-CARD-PRD6,VERIFIER-REPORT}.md`, `evidence/lab/` (logs crudos), wt-main/wt-cov.
- Lab físico `/tmp/ef-prd6-lab/` (loopback; conserva directorios y evidencia; procesos apagados al cierre).
- Repo `xKoRx/echo` `origin/feature/ef-runtime-pools@1a5c6d87` (REMOTE_VERIFIED); release local `/home/kor/opt/echo-dev/releases/`.
