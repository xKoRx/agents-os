---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-02-pbs-on-backup-node]]"
  - "[[BACKUP-DR-DESIGN]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
  - "[[2026-09-16-R0-reconciliacion]]"
aliases:
  - "PBS identity conflict 123 vs 180"
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
  - area/aranea
  - project/backup-dr
---

# 2026-09-18 — PBS identity conflict: premisa VMID 123 refutada, identidad PBS=180 confirmada

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `80-agents/journal/logs/2026-09-18-pbs-identity-conflict.md` (este log; único archivo nuevo en el vault)
  - `80-agents/memory/internal/agent-memory/aranea/backup-dr/agent-internal.md` (delta interno: identidad PBS=180 cacheada, fuera del vault canónico)
- **Cero cambios** en artefactos operativos Backup/DR (índice, CONTRACT, DESIGN, RUNBOOK, CHECKLIST, ap-02, owner project, tickets, R0).

## Motivo

- Owner (2026-09-18) autorizó corrección documental partiendo de la premisa «PBS = VMID 123, la doc que dice 180 está errada», con condición explícita: si la infraestructura demostraba que 123 es SQX u otra identidad, registrar `IDENTITY_CONFLICT` y detener las modificaciones dependientes de PBS sin inventar resolución.

## Fuentes usadas

- **OBSERVADO (canal certificado `agent-read`, read-only, sin bypass):**
  - Live 14:22 y re-verificación 14:37 (-03, 2026-09-18), `agent-read proxmox` en kronos (vista cluster + `qm list` kronos) y hera (`qm list` hera):
    - **VMID 123 = `sqx-hera`**, qemu, nodo hera, running, 70 vCPU / 100 GiB RAM / 50 GB disco, uptime ~40 días.
    - **VMID 180 = `pbs`**, qemu, nodo kronos, running, 4 vCPU / 8 GiB RAM / 64 GB disco, uptime ~40 días.
  - Captura `~/aranea/topology/discovery/athena_20260917_185839.txt` (17sep): mismo mapeo, dos apariciones independientes del inventario cluster.
  - `~/aranea/work/h0-20260918/A/inventory_59.json` (H0): `guests[21]` vmid 123 sqx-hera; `guests[57]` vmid 180 pbs.
- **DOCUMENTADO:**
  - `~/aranea/work/h0-20260918/A/discrepancies.md` §A: «renombres SQX 108/111/112/123» — 123 figura como renombre SQX (`sqx-ulab-hera-0` → `sqx-hera`), no como PBS; §D: 180 = PBS nuevo tras 2026-07-02.
  - Vault: ~161 referencias a la identidad PBS/180 en 60 archivos, todas coherentes con PBS=180 (R0, owner project, ap-02, ticket 019, RUNBOOK `https://192.168.31.180:8007`).
  - `30-resources/tools/strategyquant-x.md`, `30-resources/aranea/01-topologia/nodo-hera.md`, `30-resources/aranea/03-storage/inventory.md`: 123 = sqx-hera (`local-sqx-hera`), coherente con lo observado.

## Resolución aplicada

- **Conflicto:** claim nuevo (owner: PBS=123) vs claim canónico demostrado (PBS=180). Clase: *stale/erroneous incoming claim* — la premisa de entrada es la refutada; el vault estaba correcto.
- **IDENTITY_CONFLICT registrado** según la condición del owner. **No se aplicó corrección documental alguna**: no existe referencia operativa errada que corregir; aplicar los reemplazos habría introducido el error (123 es una VM SQX de trading running en hera; renombrarla PBS o renumerarla habría falseado el catálogo y contaminado el carril SQX/Echo).
- **No se ejecutó** el procedimiento PBS anterior (adopción R2) ni se tocó infraestructura: 0 comandos de mutación, canal read-only únicamente. Sin `qm create/destroy`, sin reinstalaciones, sin cambios de discos/datastore; recursos SQX y Ceph intactos.
- **Interpretación probable de la premisa:** lectura apresurada de `discrepancies.md` §A/§B, donde «123» y «PBS 180» aparecen en tablas adyacentes (renombres SQX y alta de PBS). La línea exacta de H0 dice: «renombres SQX 108/111/112/123; … PBS 180 nuevo».
- **Identidad demostrada (par completo):**
  - PBS = VMID **180**, hostname de inventario `pbs`, nodo **kronos**; 192.168.31.180 es la IP planificada/documentada (UI :8007 en RUNBOOK; R0: sin respuesta ping/22/8007 desde Hermes — host-up solo para backends; estado de servicio interno sigue UNKNOWN hasta el gate de adopción).
  - VMID **123** = `sqx-hera`, SQX runtime en hera (70 vCPU / 100 GiB). NO PBS, NO renumerada, NO renombrada.

## Validación

- Mapeo consistente en 5 canales: kronos live ×2 (14:22 y 14:37), hera live, athena captura 17sep, inventario H0 (`inventory_59.json` + `discrepancies.md`).
- Búsquedas vault: 0 archivos donde 123 aparezca como PBS; ~161 refs PBS/180 coherentes; `sqx-hera`=123 coherente en topología, storage y tools.
- Evidencia histórica preservada sin alteración: 17sep y H0 no fueron editados; todas las referencias históricas (PBS=180) resultaron legítimas, no errores.
- Backups R1.5 y bundle R1.6 (preparado, NO ejecutado): intactos; ninguno depende de la identidad refutada.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar `80-agents/journal/logs/2026-09-18-pbs-identity-conflict.md` y revertir el delta interno en `agent-internal.md` (línea PBS=180 del 2026-09-18). Sin más efectos: ningún otro archivo fue modificado.
