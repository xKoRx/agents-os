# SHOT4_FINAL_HANDOFF (borrador — consolidar al cierre de revalidación)

**Para:** KoR (Owner) · **De:** Primary Implementation Submanager, THE LAB V4 Shot 4 · **Fecha:** 2026-10-25
**Producto:** THE_LAB_V4_RUNTIME_FORGE_INTEGRATION · **Gate:** SHOT4 cerrado SIN aceptación total — 47/49 H PASS en el cierre; QA-01 y presupuesto H45 quedan abiertos con causa medida; decisión al Owner (ver §5)

## 1. Qué se entrega

- **Echo** `xKoRx/echo`, rama `lab-v4/shot4-final` @ `055cd69c8babf2e4dd4744b264ba34dd0aa6aebb` (rama autorizada `feature/ef-runtime-pools` + Shot 4 completo: W1–W5, wperf r1/r2, corrección r1/r2 de cobertura QA-01, corrección r2 de los defectos adjudicados por la auditoría W6, W6b-F6 del integrador). Congelado auditado W6: `757b927a`. Base Shot 3: `3b3ae81e`; commit ajeno preservado: `ac0621a1` (reloj LIVE, cert-nt-01-f1).
- **Symphony** `xKoRx/symphony`, rama `lab-v4/shot4-symphony` @ `a0c68d1` (base `dd4af7d0`): D-08 módulo sqx + paridad de bits H27.
- **Harness seguro** (fuera del árbol, `/srv/echo-work/lab-v4-shot4-20261023/harness/`): guard F-01 con prueba de identidad (ambas convenciones de cwd) + `rebase.sh` stop/purge/reset ownership-safe + launcher QA `qalaunch` (fail-closed ante destinos fuera del manifest).
- **Migraciones aditivas** 076–082 (067–075 con bytes intactos; downs de 077/080 reparados en r2).
- **Evidencia completa**: `evidence/{w0..w5,wperf*,fix-cov*,fix2-*,w6,reval}` + `SHOT4_FINAL_COVERAGE_MATRIX.json`.

## 2. Gates funcionales

- CIERRE (b2b3ebfe): **47 PASS / 2 FAIL** en H01–H49 principales; QA-01 transversal FAIL documentado. H13 cerrado con el oráculo del auditor (tokens cruzados mutuos); H39 cerrado (front compila); H45 FAIL sólo en prepare p95 ≤2s (piso contractual medido ~3s; los otros 22 checks del oráculo pasan); QA-01 en 85,8/85,2% vs 95% con críticos cubiertos y residuos estructurales documentados.

- Certificación W6 (auditoría adversarial sobre congelado 757b927a): 49 IDs principales = 32 PASS / 17 FAIL; los 7 NOT_RUN de Shot3 ejecutados íntegros; 0 BLOCKED_EXTERNAL principales.
- Corrección r2: 25/26 findings FIXED + W6b-F6 por el integrador → revalidación independiente sobre 055cd69c: **46 PASS / 3 FAIL (H13, H39, H45)** con oráculos de contrato completo; sin regresiones en los casos que pasaban con archivos tocados.
- Cierre r3 (en curso al redactar): W6C-08 dedupe mutuo (H13), import del screener YA corregido por el integrador (front vite build OK; re-verificación H39 pendiente), presupuesto prepare ≤2s (H45), cobertura QA-01 r3.

## 3. Gates físicos

- H44 re-medido PASS dos veces por auditores independientes (ingest 88,4–95,2s ≤120s; compute 61,5–68,8s ≤300s; VmHWM 1,34–1,37GiB ≤2GiB con monitor externo; conciliación económica exacta en ambas revisiones; replay bit-idéntico).
- Hasura físico en recurso propio (engine v2.50.5 loopback, apply aditivo 0 inconsistencias, action end-to-end, WS/GraphQL, dos principals mismo ns + cross-ns invisible + DML denegado).
- Browser real (playwright/chromium) con guard preflight; journey screener→detalle→día→operaciones→movimientos capturado.
- H45: los otros 22 invariantes del oráculo pasan 1:1 (cohortes ≤30s, read p95 12ms con 10 lectores durante corrección 1%, membership completa 20001); único FAIL = prepare p95 (×5 sobre presupuesto; r3 lo ataca).
- AUTH_FORGE: BLOCKED_EXTERNAL/X_AUTH_ARTIFACT (sin copia autorizada; fixtures NUM/SCALE/NEGATIVE etiquetados; nunca campañas lanzadas).

## 4. Limitaciones residuales (declaradas, con evidencia)

1. **QA-01 cobertura del delta**: corrección honesta alcanzó ~85,7% file / ~86,5% hunk con caminos críticos 100% (auth/CAS/lease/retry/temporal/economía/atomicidad); residuo documentado con causa estructural (etcd real, interceptor de driver a volumen, entropía de proceso, main() de binarios). Adjudicación final: REVAL-h.
2. **Tag .2 del kernel compartido**: la defensa D-01/D-02 vive en la fuente congelada y en el adaptador del producto (verificado por dos auditorías), pero el módulo distribuido que resuelven los consumidores es el tag `v0.0.1-lab-v4-shot2.1` — publicar .2 exige push no autorizado en este shot (W6d-F1).
3. **W6b-F2**: no existe ConfigInstaller real en el producto; el supervisor quedó fail-closed (sin instalación real no hay ACK ni READY). Cablear el instalador del consumidor real es trabajo de dueño de `echo-core` (superficie no Shot 4).
4. **AUTH_FORGE**: sin copia autorizada local; fixtures NUM/SCALE/NEGATIVE etiquetados y separados (subgate X_AUTH_ARTIFACT documentado por W6a).
5. **Test rojo pre-existente** `TestEconomicMinimumCoreTypedConfigAndProtectionParity/LIVE` (idéntico en baseline y congelado; adjudicado QA-W6H-07, no es regresión).
6. 6. **H45 prepare ≤2s**: piso estructural medido — el COPY del payload contractual (~38MB/bundle) cuesta 3,0–3,5s en tabla desnuda a 4 vCPU; con índice 083 + plan query el mejor caso es 8,4–10,0s (antes 25–28s). Alcanzar 2s exigiría relajar invariantes prohibidas (recortar dataset, paginar el prepare, relajar pin/métricas E-03/E-04) o cambiar el contrato del payload.
7. **QA-01 <95%**: 85,8/85,2% al cierre; el gap restante son clases estructurales (fallo de DB a mitad de llamada exige interceptor de driver a volumen; etcd real inexistente en sandbox; entropía de proceso; wiring de cmds) + ~70 stmts cerrados por r3a.

## 5. Decisión técnica solicitada al Owner

**Estado declarado por el submanager:** el shot cierra SIN aceptación total y SIN defecto funcional o de seguridad abierto. Por la letra del mandato: SHOT4_IMPLEMENTATION_COMPLETE no procede (QA-01 —finding 53— y el sub-invariante de presupuesto de H45 quedan abiertos); SHOT4_NOT_ACCEPTED no procede (no persiste defecto funcional ni de seguridad: todas las invariantes funcionales/seguridad de H01–H49 pasan sus oráculos en el cierre); SHOT4_IMPLEMENTED_WITH_EXTERNAL_CERTIFICATION_BLOCKERS no procede (las causas no son recursos externos según §10 del paquete: coverage ausente y timeout/presupuesto no califican).

**Lo que se pide al Owner (decisión, no shot nuevo automático):** (a) aceptar o rechazar el piso medido de H45-prepare (3,0–3,5s contractual en 4 vCPU) o autorizar la relajación/rediseño del payload del bundle; (b) aceptar el 95% contractual como inviable para las clases estructurales documentadas (autorizando un criterio alternativo, p.ej. 95% de lo alcanzable) o financiar la construcción del interceptor de driver a volumen y el etcd de sandbox que cerrarían la mayor parte del gap; (c) resolver la publicación del tag .2 del kernel compartido (push autorizado) que completa la defensa D-01/D-02 en la distribución.
