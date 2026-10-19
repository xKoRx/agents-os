# REMEDIATION-AND-ROLLBACK — Snippet Integrity P0 (2026-10-19)

## Veredicto

`READY_FOR_OWNER_APPROVAL` — el mecanismo demostrado está corregido y validado candidate-local + en modo read-only sobre producción; **la adopción operacional en producción (usar estos scripts como procedimiento de rollout y gate pre-dispatch) requiere aprobación del Owner**. No se declaró producción remediada por decreto: hoy producción está ÍNTEGRA (gates PASS 3/3) y el bug latente vive en el script de rollout, no en los hosts.

## Cambio mínimo (source authority · runtime integrity · KISS · YAGNI)

Rama `fix/snippet-integrity-p0` @ `xKoRx/symphony` commit `fe77854c` (sobre master `619c3b6f`, push verificado), dos archivos nuevos junto a `build.sh`:

### 1. `sqx/exporter-plugin/deploy-plugin.sh` (reemplaza al script de workspace)

- **Preflight fail-closed**: exigencia de escritura sobre el **directorio** del snippet (el swap crea `<file>.new` ahí) con mensaje accionable que incluye ownership/modo del dir; verificación opcional `EXPECTED_SRC_SHA256` para trazabilidad bundle↔commit; guard sqcli/StrategyQuant intacto.
- **`swap_file()`**: `cp` || die → `mv` || die → `cmp` staged vs live || die. Eliminado el patrón `cp -a A B && mv B C` (silent-skip).
- **Orden de swap**: snippet PRIMERO (autoridad runtime); si un fallo residual abortara después, el estado mixto residual sería source-nuevo + JARs-viejos, que el runtime autocorrige al recompilar — nunca lo inverso.
- **Gate final**: `cmp` live-vs-src y clase extraída de ambos JARs vs clases compiladas antes de declarar `DEPLOY OK`; sello `SHA256SUMS.after` refleja el estado **live** real.
- Rollback ejecutable por backup (guard sqcli), igual que el original.

### 2. `sqx/exporter-plugin/verify-plugin-integrity.sh` (NUEVO — gate pre-dispatch)

Read-only, seguro con sqcli activo, nunca muta/reinicia/cancela. Par **atómico** de hashes esperados del manifest de la release (src + clase main). Verifica: source == esperado; clase main extraída de `user/libs/EchoForgeAutomator.jar`, `internal/libs/Snippets.jar` y cache `internal/tmp/compiled` (si existen) == esperada y mutuamente iguales. Emite tabla efectiva y `PASS/FAIL` con diagnóstico (runtime recompilaría OTRA versión / JAR stale / cache stale). Exit 0/1.

## Impacto

- Código de producto: **cero cambios** (no toca exporter, worker, flows, manifest). `RELEASE_CHANGED: NO`.
- Producción: **cero mutaciones** realizadas por esta investigación (matriz `RUNTIME-IDENTITY-MATRIX.csv`; los permisos/ownership quedaron tal cual; los caches intactos).
- Uso esperado: (a) todo deploy futuro de plugin usa `deploy-plugin.sh`; (b) el operador/dispatcher corre `verify-plugin-integrity.sh` antes de despachar nuevas actividades SQX por host (barato: 4 sha256 + 2 extracciones jar).
- Riesgo de adopción: bajo — el script nuevo es un sobconjunto estricto del viejo con verificaciones; probado en los 4 tests de `REPRODUCTION-RESULTS.md` §4.

## Ventana y procedimiento de adopción (al aprobar Owner)

1. `git checkout fix/snippet-integrity-p0` (o merge a master — es documentación/scripts operacionales, no release de binarios).
2. Sustituir el script de workspace por `sqx/exporter-plugin/deploy-plugin.sh` como procedimiento canónico (no hay nada instalado en los hosts que haya que cambiar: los scripts viven en el workspace/repo y se suben por deploy).
3. Opcional (hardening, no requerido para este incidente): normalizar el ownership del dir de snippets de Zeus a `kor:kor` para uniformidad de flota — decisión del Owner; NO es condición del fix.

## Rollback

- Del cambio de scripts: `git checkout master -- sqx/exporter-plugin/` (los scripts no tienen estado en hosts).
- De un deploy con el script nuevo: `backup/plugin-<TS>/rollback.sh` por host (idéntico contrato al original, con guard sqcli).
- De un estado mixto detectado por el gate en producción: NO tocar nada en caliente; correr el deploy corregido como el dueño del dir (o elevar explícitamente), verificación de sello, canario. El gate nunca cancela campañas.

## Pendiente explícito (no certificado por anticipado)

- Adopción en producción del script corregido y del gate → `OWNER_APPROVAL_REQUIRED`.
- La observación de un ciclo completo deploy→run productivo con el script nuevo (procedimiento pasivo en `LONG-RUN-INTEGRITY-ACCEPTANCE.md`).
