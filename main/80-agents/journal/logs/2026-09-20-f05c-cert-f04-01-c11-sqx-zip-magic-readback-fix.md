---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-20-f05c-cert-f04-01-c11-sqx-zip-magic-readback-fix

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `xKoRx/symphony` — commit `2993da07d453521d81589413edb344e16ac1a9c6` en `codex/f05-sqx-zip-magic-readback-fix` (parent `66faa42debba18cd0dd09de127ae1374ea2a07f0`, push normal, read-back origin verificado): `sqx/adapters/magic-readback/readback.go` (detección ZIP `PK\x03\x04` + `magicFromSQXZip` en memoria con entrada canónica exacta `strategy_Portfolio.xml`, límite documentado `MaxSQXZipEntryBytes` 16 MiB, sentinels `ErrSQXZipContainer`/`ErrSQXZipEntryMissing`/`ErrSQXZipEntryAmbiguous`/`ErrSQXZipEntryLimit`, parser XML extraído a `magicFromXML` compartido con la ruta histórica), `sqx/adapters/magic-readback/readback_test.go` (gate auténtico `SQX_AUTHENTIC_FIXTURE` fail-closed, ZIP controlado, matriz negativa, variantes XML), `sqx/activities/worker/forge_seal_handoff_test.go` (fixture del seal convertido a ZIP real + negativos mismatch/corrupto con cero efectos)
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta `2026-09-20 — Corrección source C11 (veredicto SOURCE_FIX_READY_FOR_MANAGER_REVIEW)` + actualización de `Estado de entrada` + cierre de `Próxima tarea única recomendada para NORMAL`; CERT-F04-01 = BLOCKED / READY TO RERUN-6)
  - `10-projects/Echo Forge/Echo Forge.md` (checkpoint `ECHO-FORGE-C11-SQX-ZIP-MAGIC-READBACK-FIX-NORMAL`)
  - `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-c11-sqx-zip-magic-readback-fix.md` (creado)

## Motivo

- Ejecución del mandato `F05C-CERT-F04-01-C11`: corregir el quinto defecto demostrado por RERUN-5 (`FromSQX` parsea como XML plano el `strategy.sqx` contenedor ZIP del producer Apply → `forge_seal_handoff_v1` CONTRACT_CONFLICT en el read-back), con corrección mínima probada y verificable, sin cerrar F04-01 ni ejecutar efectos físicos.

## Contenido

- **G0:** artefacto auténtico de RERUN-5 verificado (4506976 B, SHA256 `9ac377b9a2b459b28ecefcf2c8166d8d200b2c47d4a4b2351cb8344d5635120d` == durable; ZIP válido; `strategy_Portfolio.xml` 32618 B crc `9ec67337` con `<value>26090011010</value>`); copia de trabajo 600 fuera de repo y vault.
- **G1:** fix en `readback.go` sólo — apertura ZIP en memoria (`archive/zip`), entrada canónica exacta case-sensitive (ausente/duplicada fail-closed, sin búsqueda alternativa), lectura acotada y CRC-verified, parser XML existente intacto, ruta XML plano histórica explícita y nunca fallback, magic decimal sin coerción int32; `forge_seal_handoff.go`, exporter, allocator, Apply, reretester, promotion, SDK y Echo sin tocar.
- **G2 RED contra `66faa42`:** T1 auténtico, T2 ZIP controlado y T3 seal fallan con la firma exacta `sqx xml parse: XML syntax error on line 3: illegal character code U+0003` (exit 1, logs preservados); fixture auténtico exigido por env con verificación dura de size+SHA256 (ausente/incorrecto = FAIL, nunca SKIP).
- **G3/G4 GREEN:** `26090011010` byte-exacto desde los bytes reales, determinístico (2 replays + 2 procesos), ZIP no mutado; matriz negativa completa en adapter y consumer (mismatch → `magic_mismatch` CONTRACT_CONFLICT; corrupto/ausente/duplicada/decoy/malformado/inválido/sobre-límite fail-closed; XML histórico preservado); sólo el miembro 1 ejercitado — los `.sqx` de `26090011011`/`012` no disponibles y NO declarados.
- **G5:** gofmt/vet/`git diff --check` limpios; coverage 100% de `magic-readback`; seal 19/19; conjunto de fallo de suites byte-idéntico al baseline (16 preexistentes, 0 nuevos); anti-test-masking sin skips/debiliciones/eliminaciones; fixture de benchmark contaminado por tests históricos restaurado antes del commit.
- **G6/G7:** cero efectos físicos (sin RERUN-6, MT5, campañas, releases, IAM, POST a Echo); commit único `2993da0…` con los 3 archivos autorizados, push normal y read-back origin (HEAD/parent/archivos); `codex/f05-release-prep` NO avanzado.
- **Estado final:** `CERT-F04-01 = BLOCKED / READY TO RERUN-6` (pendiente review manager del source C11); `SOURCE_FIX_READY_FOR_MANAGER_REVIEW`; CERT-F04-02 sin cambio; join con Echo sin cerrar; allocations `26090011001–012` write-once intactas. `MIGRATION: NONE`.

## Impacto

- La mitad source del defecto #5 queda corregida y demostrada (RED/GREEN sobre bytes reales); el gate físico sigue bloqueado por diseño hasta la revisión del manager, la release C12 y el RERUN-6 con identidades todas nuevas. Sin cambios de contratos S0, sin releases y sin reescritura de evidencias históricas.
