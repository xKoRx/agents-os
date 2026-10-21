# V4 Shot 2 — Submanager State (durable)

**Role:** Implementation Submanager / Technical Integration Lead (mandato maestro 2026-10-20). **Engine:** GLM-5.3-Flash Max LOCAL. **Estado global:** ver [[F — Decision Register]] §V4 y [[Echo — Producto Integrado]].

## Gate vigente — aceptación del Primary Manager, 2026-10-21

**TECHNICAL_FREEZE_ACCEPTED_V3 — IMPLEMENTATION_AUTHORIZED.** Metis, Primary Manager, acepta el paquete revisión 3 para implementación en respuesta al Owner, quien exige terminar las revisiones preparatorias y continuar el programa original de cuatro shots. D09/D10/D11/D16 permanecen ratificadas, sin nuevas preguntas de producto.

**Corte aceptado:** `xKoRx/agents-os@eb9ad25e`, archivo `main/10-projects/Echo/The Lab/V4 — Shot 2/1 — TECHNICAL_FREEZE_PACKET.md`, blob `cee739a8f8ae7c0bfe2d7e30bc473c88ab608c78` (paquete publicado también en commit `5d6cae71`). El diseño GOD más las ratificaciones y esta concreción V3 forman el contrato de implementación. La etiqueta histórica READY del paquete no es un gate pendiente adicional.

Esta aceptación sustituye los dictámenes `TECHNICAL_FREEZE_REPAIR_REQUIRED` / `TECHNICAL_FREEZE_REPAIR_REQUIRED_V2` y las esperas de aceptación V2/V3 para este corte. También satisface la condición de aceptación técnica pendiente consignada el 20-10 en el registro y el proyecto padre; no modifica decisiones de producto ni declara resultados de implementación todavía inexistentes.

**Alcance del GO:** código, integración en la rama de trabajo, archivos de migración y pruebas locales/descartables dentro de I1 y del presupuesto autorizado. **No autoriza** deploy/reinicio en servicios compartidos, mutaciones de bases compartidas, PROD, trading, campañas, merge a master de producto ni retiro destructivo sin sus permisos específicos. Agents-OS sí continúa directamente en master.

**Estado honesto de entrega:** implementación autorizada; no demostrada aún por este registro. El freeze acepta contratos para construir, NO certifica las garantías, el rendimiento, la integración física ni la ausencia de defectos.

### Ejecución sin otra ronda de aprobación de diseño

- No preparar revisión 4, otro discovery, otro preflight general ni volver a pedir aceptación de D09/D10/D11/D16 o de este freeze.
- Las precisiones de ingeniería, bugs, comportamiento SQL, orden de migraciones, límites de memoria, publicación coherente y casos económicos se resuelven implementando y probando dentro de Shot 2. Registrar el delta y evidencia; no convertir cada decisión técnica ordinaria en un nuevo gate humano.
- Se mantienen los invariantes y G1–G11/T01–T45 más los casos añadidos C01–C06. Ningún input fijado por un resultado puede cambiar silenciosamente: un append debe conservar su identidad reproducible mediante el contrato de revisión/snapshot. No se aprueba degradar requisitos o cambiar oráculos para conseguir verde.
- Escalar sólo una nueva decisión real de producto, contradicción irresoluble con lo ratificado, riesgo de pérdida de datos o acción fuera de los permisos disponibles. Un fallo de tests normalmente se corrige dentro del shot. Un bloqueo de entorno detiene la acción dependiente; no todo el trabajo independiente.
- **Excepción de ejecución autorizada por el Primary Manager, limitada a Shot 2:** preferir workers secuenciales con GLM-5.3-Flash Max. Si el harness vuelve a cancelar despachos, el submanager puede asumir explícitamente el rol de implementador/integrador y ejecutar en serie con ese mismo motor, registrando trabajo propio y ownership. No requiere otro permiso de diseño ni cambio de modelo/proveedor/cuota; no presentarlo como verificación independiente. Esta excepción sustituye únicamente el fallback restrictivo de §7/§10 del paquete. Shot 3 conserva auditor/contexto independiente de la implementación.
- La próxima entrega sustantiva debe ser implementación integrada con pruebas y evidencia, o un bloqueo real con el alcance afectado; no otro paquete de freeze. Las actualizaciones de progreso siguen siendo breves y basadas en trabajo real.

**Programa invariable:** Shot 1 diseño; Shot 2 implementación e integración; Shot 3 adversarial independiente; Shot 4 correcciones y gate final. Los hitos internos de implementación no son nuevos shots ni nuevas autorizaciones generales.

## Baselines verificados por el submanager (2026-10-21, daedalus)

| Repo / superficie | Baseline | Verificación |
|---|---|---|
| `xKoRx/echo` origin/master | `d74b6525` (= baseline de diseño; re-verificado fetch 2026-10-21) | fetch + rev-list en clon Shot 2 |
| `xKoRx/echo` rama e04 | `feature/e04-dev-ingest-recovery` @ `4aad647b`: 5 commits exclusivos (seeds+wiring, policy_id, platform+migración 068, guard DeleteVar, renumber); 305 detrás de master | git log/cherry/diff en clon Shot 2 (EV-E01) |
| `xKoRx/echo` stream concurrente | `feature/ef-runtime-pools` @ `112ccccd` (FEFB S01) — dueña del grammar Java; renombres coordinados | NO integrar |
| `xKoRx/symphony` origin/master | `daded14` (release 0.3.2) | clone limpio existente |
| Workspace Shot 2 | `~/aranea/work/lab-v4-shot2-20261020/echo` rama `feature/lab-v4-shot2` @ `d74b6525`, limpio en el preflight | verificado por el submanager 2026-10-21; refrescar deltas antes de cambios dependientes |
| PG DEV `echo-develop` @ .220 | sin `schema_migrations`; efectos reportados 001→065 + CHECK 4 tokens aplicados a mano; `futures_*` ausente; 5 objetos lab legacy admin-owned; REFERENCE 137.276 filas (64,7% risk_money) | SELECT-only del submanager 2026-10-21 (EV-E05..E11); no reejecutado por Metis en esta aceptación |

## Correcciones históricas del preflight

065 SÍ presenta su schema en DEV; distribución del journal medida por el submanager p50=19/p75=33/p95=59/p99=24.682/max=56.884 por strategy+symbol. Los tamaños serializados V1 son referencia, no certificación del envelope V2. Ausencia de actividad del proyector en logs NO demuestra ausencia de consumidores.

El toolkit de migración real ejecuta `db.Exec` por archivo; no demuestra golang-migrate ni tracking histórico. No registrar 066 como aplicada ficticiamente. Creación aditiva V4 y retiro legacy tienen acciones/permisos separados.

## Restricciones activas

- Sin mutaciones PROD, trading o campañas. Deploys/reinicios DEV y migraciones en la compartida requieren ownership y autorización específicos; pruebas en recursos locales/descartables autorizados no quedan bloqueadas por ello.
- Preservar cambios ajenos, protecciones de seeds, event triggers/metadata compartidos e identidades selladas; no integrar indiscriminadamente E-04 o FEFB.
- Horario Owner: 08:00–02:30 CLST; al parar, estado durable y procesos propios seguros; sin presuponer reanudación automática.
- Agents-OS sobre master, cambios pequeños + change_log. No cerrar sesión del submanager ni generar feedback de cierre sin pedido del Owner.

## Siguiente acción

**Implementar I1 ahora bajo el mandato maestro vigente, sin nueva aceptación.** Preparar contratos/Allowed Files de ejecución y despachar o ejecutar el primer paquete implementable en el workspace aislado: protocolo de migración probado en descartable y adopción selectiva E-04; fundación e ingesta; recorrido motor/backtester → historia → curvas/UI; portfolios estáticos; integración y retiro autorizado del legacy. Respetar dependencias reales y coordinar el traslape de source con FEFB.

Entrega de Shot 2: commits exactos, matriz de gates/casos, conciliación económica, evidencia de UI/integración, rendimiento medido, migración/rollback, legacy retirado o bloqueado por entorno y paquete reproducible para Shot 3. Si faltan gates, informar PARTIAL/BLOCKED, no COMPLETE. No iniciar Shot 3 ni declarar producción certificada.

## Log de avance

- 2026-10-20: bootstrap; 4 autoridades; baselines; workspace; preflight U01–U06 por el submanager; paquete rev 1 (`TECHNICAL_FREEZE_READY`).
- 2026-10-21: dictamen Manager R01–R06 y paquete rev 2; investigación read-only y evidencia publicadas. Sin edición de producto.
- 2026-10-21: dictamen Manager C01–C06 y paquete rev 3 (`TECHNICAL_FREEZE_READY_V3`), entrega `eb9ad25e`; correcciones de identidad, riesgo, atribución económica, retención, transporte y migraciones documentadas. Sin edición de producto.
- 2026-10-21: Primary Manager acepta corte V3 `cee739a8f8ae7c0bfe2d7e30bc473c88ab608c78`: `TECHNICAL_FREEZE_ACCEPTED_V3 / IMPLEMENTATION_AUTHORIZED`. Termina el ciclo de revisión preparatoria; mantiene cuatro shots. Excepción explícita de ejecución serial propia dentro de Shot 2 ante fallo de workers, con atribución honesta e independencia de Shot 3 preservada. Esta actualización es documental, no evidencia de código implementado.
