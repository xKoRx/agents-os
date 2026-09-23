---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Aranea]]"
project: "[[Echo — E-10 Strategy Quality and Eligibility]]"
application:
entities:
  - "[[Echo]]"
related:
  - "[[Echo — E-10 Manager Review M2 — T00-T03 Corrections 2026-09-21]]"
  - "[[2026-09-22-zcode-glm53-e10-m2-c1c2-corrections]]"
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

# E-10 — correcciones M2 C1/C2 y actualización de estado

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-10 Strategy Quality and Eligibility.md` (estado actual, tabla de entrega, decisión pendiente 1 con cierre M2 C1-C, bitácora 2026-09-22, frontmatter `updated`)
  - repositorio `xKoRx/echo`: commits `2ce43b1a` (C2 run.sh E-08/E-09), `67e33b7f` (C1 dominio+stores+comentarios 069), `d2754415` (SPEC 1.2.0 + VERIFICATION §8); push FF `34876939..d2754415`

## Motivo

- Mandato NORMAL E10-M2-C1/C2 sobre la autoridad [[Echo — E-10 Manager Review M2 — T00-T03 Corrections 2026-09-21]]: corregir los defectos de identidad (policy_ref sin versión, policy_digest confundido con el ref), integridad (decision/assessment construidos a mano aceptados por el store), compatibilidad (run.sh E-08/E-09 con 069 en sus rebuild_chain) y declarar el estado real de la ratificación owner, sin deshacer el trabajo legítimo T00–T03 ni iniciar T04–T10.

## Fuentes usadas

- M2 (autoridad), SPEC/VERIFICATION v1.1.0 en `34876939`, código fuente dominio/stores/migración 069, PG PROD (`echo` vía `mcp_echo_prod_ro`) y DEV compartido (`echo-develop` vía `mcp_echo_dev_rw`) para verificar que 069 no fue aplicada fuera de harness.

## Resolución aplicada

- policy_ref = D(tag,{policy_version,content}) y policy_digest = D(tag,content) como receta distinta; verificación de identidad desde todas las columnas durables; gates cross-row fail-closed en PutDecision/PutAssessment con errores tipados y cero escritura; provenance inputs_digest decisión=assessment; PutPolicy declarado fixture-only en clase A con la vía owner-operated como UNRESOLVED DECISION de manager (clase C); 069 excluida explícitamente de todas las reconstrucciones parciales de ambos harnesses; conteo del delta M1 corregido a 23 archivos en VERIFICATION.

## Validación

- ROJO conductual C1-A/C1-D/C1-B contra el árbol sin corregir (sonda temporal eliminada); VERDE: 11/11 tests físicos E-10 en instancia propia :15471, `go test ./domain/ -race`, run.sh E-08/E-09 PASS completos en :15472/:15473 con schema final sin objetos 069; failing sets idénticos al baseline por nombre; push FF con read-back `origin == d2754415`; master intacto.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Git: `git revert` de los tres commits en la feature (sin force); la nota del vault se restaura desde el historial del vault; las instancias descartables `/tmp/e10-m2-*-pg-*` se pueden apagar sin dependencias.
