Empezaré resolviendo el bootstrap canónico de Agents-OS y localizando la documentación del proyecto Polymarket Engine, para luego crear el repositorio Go e implementar el slice M2-S01.

Bootstrap: arranque en frío. Go 1.27.1 ya está instalado, y existe un checkout en `~/go/src/github.com/xKoRx/polymarket-engine`. Cargaré el stack de arranque mínimo y examinaré el estado actual del repositorio.

La constitución está cargada. Continuando el bootstrap: perfil global, nota de continuidad y registro de habilidades; después, el documento del proyecto.

Bootstrap listo. Entity: [[Polymarket Engine]] · Goal: implementar M2-S01 Foundation · Ahora leo el documento de proyecto (2134 líneas) — primero localizo la estructura para leer sólo lo requerido.

Ahora leo el plan M2 completo (líneas 1593–2134), que es la autoridad directa del slice.

Plan M2 leído. Puntos clave: gates S01 = G-01 + base mecánica G-15b; el plan propone `go 1.23` (el mandato ordena corregirlo a 1.27); el repo ya existe con commit inicial. Ahora leo las secciones M1 congeladas que S01 cita como contratos (M1.1 capacidades, M1.3 dominio/unidades/tiempo, M1.8 modos, M1.14 import gate).

Tengo los contratos principales. Reviso M1.14 (base confiable Go / import gate) y la sección de tareas/bitácora donde luego actualizaré el estado.

Bootstrap y lectura de contratos completos. Tengo el alcance congelado claro. Antes de escribir código, registro el plan de trabajo y verifico el entorno de módulos Go.

**Entity:** [[Polymarket Engine]] · **Goal:** implementar M2-S01 Foundation · **Gates S01 según plan:** G-01 + base mecánica de G-15b

Red disponible y proxy funcional; `BurntSushi/toml` parcialmente cacheado. Ahora bootstrapeo el repo existente (`~/go/src/github.com/xKoRx/polymarket-engine`, commit inicial con README) y fijo el baseline Go.

Dependencias listas: `decimal v1.4.0`, `toml v1.6.0`, `rapid v1.3.0`. Verifico la API de shopspring v1.4.0 que usaré y luego escribo foundation.

API confirmada (`Coefficient()` devuelve `*big.Int` — haré copia defensiva). Escribo ahora el paquete `internal/foundation`, empezando por errores, decimal y protocol identity.

Ahora los IDs nominales (validadores compartidos + tipos congelados de M1.3):

Ahora time primitives (Clock, SourceTime, VirtualTime) y el capability registry fail-closed:

Ahora `internal/config` (TOML estricto versionado con hash de revisión determinista):

Ahora `internal/archtest` — mecanismo AST (sin dependencias pesadas) + fixtures del probe:

Corrijo un error de tipos: `findCycle` recibe un tipo anónimo que no coincide con `*pkg` local — muevo `pkg` a nivel de paquete.

Ahora los fixtures del probe (bajo `testdata/`, ignorados por el build) y `cmd/engine`:

Primer build de verificación antes de escribir los tests:

Build, vet y gofmt limpios. Ahora escribo los tests obligatorios — empiezo con foundation (IDs, decimal+property, unidades, revisiones, tiempo, errores, capabilities, lease) y el runner de evidencia G-01:

Ahora el fixture G-01 y el runner con emisión de evidencia física:

Simplifico: uso `errors.Is` estándar (nuestros tipos implementan `Is`/`Unwrap`) y completo el campo `generated_at`:

El clásico: literal compuesto en condición de `if` necesita paréntesis. Corrijo:

Ahora config, archtest y cmd tests:

Dos bugs reales: (1) `ParseDecimal` exige parte fraccional aunque no haya punto; (2) el validador de IDs opacos permite espacios internos — lo Endurezco para fail-closed:

Varios hallazgos buenos del test suite. Reviso primero el `Neg()` de shopspring (posible mutación in-place):

`Neg` es seguro. Hago una sonda rápida para entender el fallo de `Neg` antes de arreglar todo:

`Neg` está bien ahora. El caso raro es `0 + 1e4096`. Reviso `Coefficient()` de shopspring v1.4.0:

Encontrado: `RescalePair` de shopspring alinea exponentes hacia abajo, de modo que `0 + 1e4096` produce `10^4096` con exponente 0 (4097 dígitos) antes de la canonicalización. La corrección correcta: canonicalizar primero y verificar el límite después. Aplico todas las correcciones:

Ahora corrijo los tests: expectativas de escala canónica, decisión ALLOWED y generadores rapid con `SampledFrom`:

Todo verde salvo la evidencia pendiente. Emito la evidencia física G-01:

Evidencia G-01 emitida (62 casos). Ahora agrego la emisión de evidencia G-15b (base mecánica del gate de imports) en archtest:

Todo verde con -race. Ahora coverage, tidy y verificación física:

foundation 86.2% y cmd 74.2% — bajo el piso de 95%. Identifico las líneas descubiertas:

Añado un archivo de tests que cubre las ramas restantes (accesores, stringers, rutas de error) y simplifico una rama muerta en `Decimal.String` según la regla del perfil (rama inalcanzable → se borra):

`huge - tiny` genera genuinamente 8193 dígitos significativos (10^8192−1) — el rechazo es correcto; corrijo la expectativa del test y cubro las indirecciones de os:

foundation 95.0% y config 97.8% ✓. Levanto archtest (93.5%) cubriendo lo que falta:

Coverage total 95.1% (foundation 95.0, config 97.8, archtest 97.1; cmd 83.9 por el seam `os.Exit` de `main`, no testeable sin matar el binario). Ejecuto la batería de calidad completa y la verificación física:

Verificación física del binario y revisión final del árbol:

Verificación física completa (el binario compilado estampa el commit). Ahora actualizo el documento de proyecto — primero las correcciones ordenadas del plan M2 (`go 1.23` → baseline 1.27 y registro del path del repo):

Las menciones restantes de `go 1.23` son las notas históricas que documentan la corrección (correcto), y los `REQUIRES_OWNER` restantes son historial preservado de M1/FABLE o texto procedimental. Ahora actualizo estado, tareas, encabezado M2 y bitácora:

Proyecto actualizado. Ahora registro la ejecución de código según el contrato `agents-os-agent-run-register` (requerido por el perfil y M2.6):

No hay precedente de change-log para actualizaciones de este proyecto (M0/M1/M2 se registraron en bitácora del propio proyecto, y M2.6 lo prescribe así). Paso final del repo: commit único checkpoint del DoD en `main` sin push:

El commit arrastró un artefacto obsoleto de rapid (`.fail` de la corrida con el generador roto, ya corregido). Lo elimino y enmiendo el checkpoint (sin push, es mi propio commit recién creado):

Commit final `0912d39` con árbol limpio y suite verde post-commit. Cierro todos y entrego el reporte:

STATUS: M2-S01_PASS

REPO:
- path: `~/go/src/github.com/xKoRx/polymarket-engine` (checkout existente registrado; commit checkpoint `0912d39` en `main`, sin push ni tags)
- module: `github.com/xKoRx/polymarket-engine`
- Go: `1.27.0`
- toolchain: `1.27.1`

IMPLEMENTED:
- foundation: IDs nominales por namespace no intercambiables (`GammaEventID`, `GammaMarketID`, `IntentID`, `RunID`, `StrategyID`, `ExperimentID`, `VenueTradeID`, `FillKey`), `AssetKey{chain_id, protocol, token_contract?, wire_asset_id}`, `ConditionRef{protocol, raw_id}` (bytes32 para CTF), unión cerrada `ProtocolIdentity` (CTF/PROTOCOL_V2/UNKNOWN sin conversiones), decimal exacto coefficient+scale parseado desde lexema JSON con shopspring encapsulado (sin `float64`, sin `*big.Int` expuesto, overflow y `-0` rechazados/normalizados, forma canónica y serialización determinista), unidades `Price/Shares/CollateralAmount/BasisPoints/FeeCoefficient` con política de signo y conversión exacta bps→coeficiente, `RevisionRef{owner, namespace, entity_id, generation, revision, schema_version, content_hash}` con 9 owners cerrados, `Clock` (wall+mono por boot, `FakeClock` determinista, `SystemClock` como único `time.Now`), `SourceTime` con unknown explícito y precisión declarada, `VirtualTime` tipo distinto, error taxonomy tipada de 11 kinds estable bajo wrapping (`errors.Is`/`errors.As`), capability registry v1 fail-closed (8 capabilities frozen no habilitables: LIVE_EXECUTION, NEGRISK_CTF/V2_CONVERSION, L2_HISTORICAL_BACKFILL, DEFER_EXEC, BUILDER_OPTIONAL, COMBO, RFQ; unknown/missing/disabled → DENIED; sin `defaultAllow`), `ExecutionMode` (default `LIVE_DISABLED`) y `ActivationLease` como value contract (`RequestActivationLease` → `DISABLED`; sin emisor, sin secretos).
- config: TOML estricto versionado (`BurntSushi/toml`, schema v1 obligatorio, unknown fields rechazados con nombre exacto, defaults inequívocos, `LIVE_ENABLED` → FAIL `DISABLED` porque el registry v1 niega `LIVE_EXECUTION`, hash de revisión determinista sobre config normalizada, sin campos de secretos verificado por test reflect).
- archtest: mecanismo AST (`go/parser`, sin herramientas externas): dirección de imports (foundation no importa internos; config sólo foundation), sin `utils`/`common`, detección de ciclos, y gate de imports de estrategias reusable para S09/G-15b (unsafe/reflect/os/os-exec/net/syscall/plugin/cgo, goroutines propias, `time.Now`, `math/rand`) con fixtures probe en rojo (unsafe, net/http, goroutine, clock, random) y fixture neutral en verde.
- cmd: `cmd/engine` mínimo con subcomando `version` (module/commit/toolchain/config schema; commit estampado en build compilado), sin networking, sin SQLite, sin lógica de negocio.

QUALITY:
- go test: PASS (unit + property rapid + fixtures G-01)
- race: PASS (`go test -race ./...`; property con seed fija 20260917 verde, registrada en bitácora)
- vet: PASS; `go mod tidy` con sólo 3 dependencias directas (decimal, toml, rapid; cero transitivas inesperadas)
- coverage: 95.1% total (foundation 95.0%, config 97.8%, archtest 97.1%; cmd 83.9% — única excepción: `main`/`exitWith`, seam `os.Exit` no testeable sin matar el binario)

GATES:
- PASS: G-01 porción S01 (62 vectores IDs/decimal/unidades/fills; evidencia física en `testdata/foundation/evidence/g01.json` con hash de fixture `f6c2796f…`, expected/actual y build) · G-15b base mecánica (evidencia `evidence/g15b-base.json`; cierre con fixtures de redacción queda en S09/S12). Semilla de G-15 cubierta por la matriz fail-closed de capabilities en tests.
- NOT_RUN: G-02 (asignado a S10/S11), G-03 en adelante — no declarados.
- evidence: regenerable con `PM_ENGINE_EMIT_EVIDENCE=1 go test ./...`; integridad de evidencia re-verificada en cada corrida normal.

SCOPE:
- files/packages created: `go.mod`, `cmd/engine`, `internal/foundation`, `internal/config`, `internal/archtest` (+fixtures `testdata/`), `testdata/foundation` (vectores + evidencia). Sin paquetes futuros vacíos, sin migraciones, sin SQLite.
- explicit deferred work: tabla de ticks/redondeos P03 §5 → porción S05 de G-01 (el mandato ordering las rounding rules de órdenes a S02/protocol); el plan M2 corregido puntualmente (`go 1.23` → baseline 1.27, repo location resuelto) sin otras modificaciones; proyecto Agents-OS actualizado (estado `M2_FROZEN — S01 DONE`, tareas, bitácora) y run registrado en `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-pm-engine-m2-s01-foundation.md`.

BLOCKERS:
- none

NEXT:
- M2-S02 + M2-S03 barriers