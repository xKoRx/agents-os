---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[CP Flink local]]"
  - "[[RIO E2E local]]"
  - "[[rio-controlplane-flink]]"
  - "[[Descripción PR — rio-controlplane-flink (E2E local)]]"
aliases: []
tags:
  - kind/doc
  - project/rio-e2e-local
created: "2026-10-13"
updated: "2026-10-14"
---

# Descripción PR — rio-controlplane-flink (E2E local PR 2)

Repo fury_rio-controlplane-flink · rama feature/rio-e2e-local-flink-pr2 @ 39937680c49622fb5f839d237ab29111081719bf · base feature/rio-e2e-local-flink-kiss @ c0cabe7213461793bf1382c4e2816dea258361fd (#209) · 11 commits sobre la base, incluidos dos merges normales · diff vs base: 15 archivos/+1150/−144; vs develop: 29 archivos/+3280/−0 · Java 1937/local 19/hooks PASS; recertificación física del último fix pendiente, 2026-10-14.

## Propósito

Recurso del proyecto con el cuerpo del PR 2. El repo no tiene template de pull request; se usan las secciones mínimas de pr-description.

## Contenido

Entrega apilada sobre PR 1, con aislamiento productivo y límites de validación explícitos.

---

**Pendiente:** recertificar físicamente el último fix de limpieza de adjuntos en `39937680`. El E2E completo pasó en `278b4a1a`; se alcanzó el máximo de tres iteraciones físicas de esta sesión.

PR 2 de 3 del CP Flink local, apilado sobre [#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209). Extiende el runtime para probar SQL UPDATE, CRUD y JAVA/JAR sin cambiar código productivo. Python/ZIP queda para el PR 3; GCP y Playmaker están fuera de alcance.

## Qué cambia

El perfil local agrega SQL UPDATE, CRUD HTTP de `/flink/sql-code` y JAVA/JAR usando los controllers, handlers y pollers de develop. UPDATE prepara el reemplazo antes de cerrar la sesión anterior: si falla la validación o la apertura del Gateway, la aplicación original sigue utilizable. Después del reemplazo elimina los adjuntos anteriores sin referencias; DEPROVISION usa la misma limpieza y conserva archivos compartidos.

El stub Nexus con nginx sirve `TopSpeedWindowing.jar` de la imagen Flink y ejercita la descarga multipart existente. La excepción HTTP se limita a `nexus-local`, conservando la validación de paths. El launcher registra el job JAR antes de limpiar el upload para mantenerlo alcanzable por stop si falla la limpieza.

La rama incorpora la base actual del #209: comandos serializados, cierre de operaciones SQL incluso ante error, registro de cada job antes de la siguiente sentencia y cancelación del lote ante fallas. SQL y JAR comparten actividad para acciones/eliminación y salud con prioridad FAILED para el monitor. Las pruebas de la base permanecen en `LocalFlinkRuntimeTest`. El README conserva la guía vigente de la base.

## Cómo se probó

- `./gradlew test`: PASS, 1937 tests productivos, sin fallas, errores ni skips.
- `./gradlew --offline localBootJar localTest`: PASS, 19 tests locales, sin fallas, errores ni skips; incluye cambios de adjuntos SQL/JAR, retención de archivos compartidos y fallos de preparación de UPDATE.
- Pre-commit: PASS, incluidos formato, Checkstyle y PMD.
- `src/main` y `src/test`: diff vacío contra `origin/develop` y contra `origin/feature/rio-e2e-local-flink-kiss`.
- E2E completo PASS en `278b4a1a`: SQL con dos INSERT y comentarios, SQL inválido tras dos jobs, stop con FAILED+RUNNING, SQL UPDATE con transformación nueva, CRUD HTTP con datos reales, JAR PROVISION/RUNNING, stop/start, UPDATE con job nuevo y file-sink, DEPROVISION y descarga nueva desde Nexus que acredita el borrado del artefacto.
- Tres iteraciones físicas: primera completa PASS en `f3cb6f8b`; segunda interrumpida intencionalmente al actualizar la base (exit 143, con SQL/UPDATE/regresiones/CRUD PASS); tercera completa PASS en `278b4a1a`. Cleanup final: cero contenedores y redes `rio-*`. El último fix `39937680` tiene validación Java/local y queda pendiente de otra corrida física.

## Proyecto

RIO E2E local / CP Flink local · rama `feature/rio-e2e-local-flink-pr2` · base `feature/rio-e2e-local-flink-kiss` @ `c0cabe72`.

---

## Notas internas — NO van al PR

- Commits propios de implementación, sin merges heredados: −564/+544 líneas. Sin el fix JAR inicial: −563/+527; la simplificación cumple el presupuesto también incluyendo los fixes restantes.
- El último comentario llegó después de la tercera corrida. Se corrigió y cubrió localmente sin exceder el límite físico. Próximo paso: recertificar 39937680.
