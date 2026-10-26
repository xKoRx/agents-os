---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
  - "[[EF-PROD-PRD6-RECOVERY-MIGRATION-CLOSURE-20261026]]"
  - "[[EF-PROD-PRD5-MANAGER-REVIEW-20261026]]"
  - "[[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-26"
updated: "2026-10-26"
---

# EF-PROD PRD.6 — Primary Manager adjudicación (2026-10-26)

## Propósito

Adjudicar el cierre PRD.6 para **seguir a certificación DEV sobre el deployment Flink/StateFun ya existente en Aranea .75**, sin un tercer Flink, sin nuevos clústeres ni otro rediseño. Revisión documental + source remoto de `xKoRx/echo@4a041e6cf17b27a023a1a693a48be1034c35e7dd`; verificador ONE-SHOT del Submanager reporta 10/10 CONFIRMED, cero P0/P1, con evidencia L3 aislada. Primary Manager no ejecutó laboratorio ni inspección física .75 en esta revisión.

## Contenido

### Decisión vinculante

**PRD.6 SOURCE/INTEGRATION = ACCEPTED_WITH_LIMITED_DEV_EXCEPTIONS.** P0-G5A (frontier de TODOS los ingress por metadata real; join Flink REST/module, no HWM), P0-G5B (inventario + copia y hash de dependencias), P0-G5C (migración ONE-SHOT legacy→strict con sweep y provenance) **aceptados en su capa de implementación y laboratorio**. Los 14 commits frente a `c2d71357` y la eliminación final del binario commiteado se verificaron; SHA final coincide con origin `feature/ef-runtime-pools`. Esta es aprobación para iniciar **certificación operacional DEV observation-only**, NO una declaración de migración ya realizada ni de producción lista.

**G-IMPL_SOURCE = ACCEPTED_FOR_DEV_OBSERVATION_WITH_EXCEPTIONS; G-IMPL_FULL/PROD = NOT_ACCEPTED.**
**OWNER_MAINTENANCE_WINDOW = PENDING_EXPLICIT_OWNER_APPROVAL; G-REC_PHYSICAL = PENDING; G-FEED_NT = PENDING; G-SIM = BLOCKED; G-PROD = NO_GO.**

### Excepciones adjudicadas

**EX-QA P2 — cobertura.** Evidencia reportada PRD.6: nuevos `840/934 = 89.94%` y diff-aware `220/266 = 82.71%`; son universos distintos, **ninguno cumple el piso ≥95% de GOD-03**. Manager acepta excepcionalmente esta deuda ÚNICAMENTE para el despliegue/certificación **DEV sin órdenes** porque los riesgos económicos y de recuperación siguen fail-closed, la verificación adversarial no encontró P0/P1 y las fronteras P0 disponen de pruebas L3 reales. Esto NO cambia GOD-03 para PROD: la deuda debe resolverse o obtener autorización de excepción con evidencia específica antes de promoción a cuentas comerciales. No hacer otra campaña de tests genérica ahora.

**EX-STORAGE P2 en implementación, gate OPERACIONAL bloqueante para el corte DEV.** El ensayo L3 demostró restauración desde copia de un checkpoint en ese laboratorio, pero **NO cubrió incremental RocksDB** y el preflight PRD.5 verificó que **DEV existente tiene RocksDB incremental con checkpoints host-local y sin savepoints**. En source `seal.go::copyCheckpointComplete` copia/hashes los archivos referidos bajo `<copyDir>/dependencies/`, pero **NO reescribe las rutas absolutas de los handles incrustados en `_metadata`**. Por ello esa copia no acredita portabilidad/independencia para checkpoint incremental: si se rotan/eliminan los ficheros originales, un restore puede fallar aun teniendo hashes válidos de la copia. La doc Flink 1.14 distingue checkpoints no generalmente móviles de savepoints normalmente relocatables: https://nightlies.apache.org/flink/flink-docs-release-1.14/docs/ops/state/savepoints/ . `G-REC` queda NO-GO hasta demostrar un backup/restore efectivo de la forma real del checkpoint o, preferentemente, **un savepoint completo y portable** del Job DEV (mismo deployment), respaldado fuera del host y accesible en el runtime real. **No se acepta renombrar este residual como P2 no-bloqueante para un reinicio de FX.** No requiere otro Flink: usar mecanismo nativo de savepoint y almacenamiento existente Aranea.

### Precauciones adicionales de integración

- **No reutilizar binarios de un SHA intermedio sin comprobar su buildvcs:** el commit final `4a041e6c` incluye higiene `.gitignore` y eliminación de un binario, por lo que el bundle release para DEV deberá tener build reproducible/hashes y source SHA explícitos, sin `vcs.modified` ni confusión `63f241c0`/`1a5c6d87`/`4a041e6c`. No se requiere rebuild de código para la revisión documental.
- La tarjeta WINDOW-CARD-PRD6 actual es un artefacto del workspace local. **Materializar su versión final y hashes en el vault antes de solicitar consentimiento de corte**, no depender de una ruta local inaccesible para el Owner.
- El primer corte debe verificar en runtime efectivo TODOS los 17 ingresses originales y su frontier, topic IDs, roster FX/Futures, JobGraph/ValueSpecs, config revision, checkpoint/savepoint, propietarios y separación PROD. No inventar un campo faltante ni cambiar earliest/latest.
- El manifest de migración legacy debe declarar la ONE-SHOT, sellarse desde estado preexistente, certificar sweep completo de keys ACTIVE antes de sellar nueva generación strict y mantener counters/timers/offsets; sólo después del segundo checkpoint/attestation se considera recuperable.
- Todos los ensayos de capacidad, M1 commit-at-checkpoint real, PG projector, NT FEFB batched, FX Journal y venue/Sim101 siguen sujetos a sus gates separados: no se colapsan en `G-IMPL_SOURCE`.

### Ejecución operacional autorizada y STOP

**AUTORIZADO AHORA, SIN RESTART:** Staging/preflight final read-only del mismo `flink` DEV .75; sellado de artefacto de release exacto, revisión de backup/restore strategy, preparación del savepoint target en almacenamiento existente Aranea y verificación de paths/permisos, revalidación cinco capas de desarme y estado FX. Toda mutación necesaria para generar un savepoint real, cambiar módulo o reiniciar/recrear contenedores compartidos requiere **aprobación explícita de la ventana Owner**. PROD no se toca.

**CON VENTANA OWNER AUTORIZADA EN UN TURNO POSTERIOR:** (0) recertificar preflight/propietarios FX desarmados, (1) obtener savepoint COMPLETO y verificado y respaldo fuera del host ANTES de detener; junto con último checkpoint y metadata; (2) ejecutar `seal` sobre cut auténtico, 17 ingress coincidentes, copia/restore compatible con la URI elegida, (3) si cualquier condición falta, ABORT SIN RESTART, (4) corte coordinado SOLO sobre el proyecto Compose `flink` existente; runtime master/worker sin crear otros; (5) restore + legacy migration + proof checkpoint STRICT + attest CLEAN; (6) FX continuity/offsets/Journal y futures OBSERVATION sin nueva exposición; (7) capacity/M1/freshness/feed Ninja físico, con autorización terminal independiente; (8) aceptar DEV sólo si estable, con rollback conservador; no volver a snapshot viejo tras efectos económicos sin reconciliación.

**Si el código `seal` vigente no puede aceptar el artefacto de snapshot/savepoint seguro, resolver únicamente la compatibilidad mínima en el MISMO despliegue/mandato de comisionamiento**, documentar el bloqueo y NO arrancar de cero; no convocar GOD, no tercer Flink, no iniciar otra secuencia de microshots.

### Resultado

- PRD6_CLOSED_AS_SOURCE: YES
- DEV_OBSERVATION_CANDIDATE: YES, CONDITIONAL
- DEV_SHARED_RESTART: **NO — todavía necesita snapshot portable + aprobación ventana Owner**
- COVERAGE_WAIVER: ONLY DEV OBSERVATION, NOT PROD
- INCREMENTAL_ROCKSDB_WAIVER: SOURCE ONLY, **NOT PHYSICAL RESTORE**
- NO_PROD, NO_ORDERS, NO_SIM, NO_NEW_FLINK.
