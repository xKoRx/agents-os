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
  - `80-agents/memory/internal/agent-memory/2026-09-17-backup-dr-doc-consistency-continuity.md` (delta interno in-place en el checkpoint activo: identidad PBS=180 cacheada)
- **Cero cambios** en artefactos operativos Backup/DR al momento de escribir este log (mañana). [Corrección de la tarde]: RUNBOOK, ap-02, R0 (anotación inline) e ITER4 (banner) sí se corrigieron por la dimensión IP — ver «Resolución aplicada», último bullet.

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
  - PBS = VMID **180**, hostname de inventario `pbs`, nodo **kronos**. [CORREGIDO 18sep tarde]: 192.168.31.180 NO es ninguna IP efectiva — era la IP del plan julio y NO hay host en .180 (ARP INCOMPLETE). La IP efectiva de PBS es **192.168.31.123:8007** (UI «pbs - Proxmox Backup Server», PTR `pbs.lab.aranea`); el «sin ping/22/8007» de R0 sondeó la IP del plan. VMID e IP son identificadores independientes y en Aranea NO coinciden numéricamente.
  - VMID **123** = `sqx-hera`, SQX runtime en hera (70 vCPU / 100 GiB). NO PBS, NO renumerada, NO renombrada.

- **Corrección de la tarde (mismo día, mandato owner tras STOP):** este log registró «.180 = IP planificada», ambiguo y consistente con una lectura errada VMID=IP. Evidencia de red 18sep tarde: **.123 = PBS** (:8007 UI viva, PTR pbs.lab.aranea, ARP presente), **.111 = sqx-hera** (fib_trie interno del guest vía ssh-mcp `sqx-hera` + PTR worker.hera.lab.aranea + DNS sqx-hera.lab.aranea.cl), **.180 = sin host en la LAN**. GAP wrapper: network no expone MACs de taps ni vecinos (registrado, no rodeado). Corregidos: RUNBOOK (§1/§1.3/§4), ap-02 (status_detail/objetivo/pvesm/validation), R0 (anotación inline, preservada), ITER4 (nota en banner deprecated). DESIGN frozen: limpio, 0 refs IP. VMIDs/nodos/estados de la mañana: sin cambios, re-verificados.

## Validación

- Mapeo consistente en 5 canales: kronos live ×2 (14:22 y 14:37), hera live, athena captura 17sep, inventario H0 (`inventory_59.json` + `discrepancies.md`).
- Búsquedas vault (mañana): 0 archivos presentaban 123 como PBS; ~161 refs PBS/180 coherentes con el VMID; `sqx-hera`=123 coherente en topología, storage y tools. [Nota tarde: tras la corrección IP, los docs operativos citan 192.168.31.123 como IP de PBS — el número es ahora también una IP; la identidad VMID 123=sqx-hera sigue intacta.]
- Evidencia histórica preservada sin alteración: 17sep y H0 no fueron editados; todas las referencias históricas (PBS=180) resultaron legítimas, no errores.
- Backups R1.5 y bundle R1.6 (preparado, NO ejecutado): intactos; ninguno depende de la identidad refutada.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar `80-agents/journal/logs/2026-09-18-pbs-identity-conflict.md` y revertir el delta interno del checkpoint `2026-09-17-backup-dr-doc-consistency-continuity.md` (párrafo «PBS identity conflict resuelto (2026-09-18)» + `updated`). Sin más efectos: ningún otro archivo fue modificado.
