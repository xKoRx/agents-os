# ECHO FORGE — F05I-T1-C1 / CORRECCIÓN DEL PARSER

ROL: coding agent NORMAL.

OBJETIVO:
Corregir exclusivamente el defecto de validación de trailing data en
sqx/core/releasematrix.Parse.

No repetir T1. No implementar T5. No reabrir Planning C1.

## AUTORIDADES

Repo: xKoRx/symphony
Branch: codex/f05-release-prep
HEAD esperado: 5295f1ca91f41cc28f999f517c5bbae425f86b1b
Baseline F-04: b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43

SPEC: Echo Forge — F-05-I Release Matrix and Read Surface Contract.
Proyecto: Echo Forge — F-05-I Cohesive release and read surfaces.

Ejecuta el bootstrap vigente de Agents OS.

Verifica Git local y remoto antes de modificar.

Dirty ajeno conocido:
specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json

Preservarlo intacto.

## DEFECTO CONFIRMADO

Parse utiliza:

    dec.More()

después del primer Decode para verificar trailing data.

Esto no garantiza el final del documento JSON.

Una matriz JSON válida seguida de "}" o "]" puede ser aceptada.
El contrato exige rechazar TODO contenido no-whitespace posterior al
único objeto JSON permitido.

El manager reprodujo el defecto con el decoder estándar de Go.

## ALLOWED FILES

Únicamente:

sqx/core/releasematrix/releasematrix.go
sqx/core/releasematrix/releasematrix_test.go

NO modificar release-matrix.json.
NO modificar otros archivos source, SPECs ni deploy/.

## IMPLEMENTACIÓN

Reemplaza exclusivamente la verificación dec.More() por la técnica
correcta para validar un único documento JSON completo:

- Primer Decode: decodifica Matrix.
- Segundo Decode en una variable descartable.
- Acepta exclusivamente io.EOF.
- Si devuelve nil u otro error, rechaza el documento.
- Conserva DisallowUnknownFields y Validate.

No cambies:

- API pública.
- Modelos.
- Estados.
- Matriz de 17 capacidades.
- Marshaling canónico.
- Embedding.
- Loader.
- Contratos históricos.

No agregues dependencias externas.

## REGRESIÓN

Extiende TestParseRejectsCorruptAndTrailing o crea un test enfocado.

Construye los inputs a partir de Embedded() para asegurar que el
primer documento sea una matriz auténticamente válida.

Casos obligatorios:

1. JSON válido + "}" => ERROR.
2. JSON válido + "]" => ERROR.
3. JSON válido + segundo objeto JSON => ERROR.
4. JSON válido + texto inválido => ERROR.
5. JSON válido + espacios/newlines => PASS.

El test debe demostrar el defecto anterior y pasar con el arreglo.

No alcanza un test que sólo compruebe dos objetos concatenados:
el test anterior ya cubría ese caso y no detectó el problema.

## VALIDACIÓN

Ejecuta y reporta:

- gofmt.
- go test ./sqx/core/releasematrix/...
- go test -race ./sqx/core/releasematrix/...
- go vet ./sqx/core/releasematrix/...
- go build ./sqx/core/releasematrix/...
- git diff --check.
- Confirmar que release-matrix.json no cambió.

PASS / FAIL / NOT_RUN por cada comando.

No usar MCPs de infraestructura.
No usar bases de datos remotas.
No desplegar, publicar releases ni ejecutar certificaciones físicas.

## GIT

Commit atómico con los dos archivos autorizados.

Push normal a origin/codex/f05-release-prep.

Sin force, tags, releases, PRs ni cambios a master.

Verifica:

- HEAD remoto == commit correctivo.
- 5295f1c es ancestro del nuevo HEAD.
- Diff limitado a dos archivos.
- Dirty ajeno preservado.

Si hay avance remoto incompatible: STOP.

## AGENTS OS

Actualiza únicamente T1:

- Defecto encontrado.
- Causa.
- SHA correctivo.
- Tests reales.
- Manager review pending.

Mantén T1 en Review.

No cambiar T2–T4.
No marcar T5/T6/T7 como realizadas.
No cerrar F-05-I.
No declarar nueva certificación física.

Registra change_log y agent_run según las skills vigentes.

Ejecuta session close.
No crear L0 sin transcript auténtico.

## HANDOFF

Entrega breve:

1. Resumen ejecutivo.
2. SHA anterior y nuevo.
3. Diff exacto.
4. Evidencia de regresión antes/después.
5. Validaciones.
6. URL del commit y HEAD remoto.
7. Estado Agents OS.
8. Session close.

No autoapruebes T1.
No avances a T5.

STOP.