# MAGIC-NUMBER-VERIFICATION — identidad 64-bit (2026-10-18)

## Veredicto

**64BIT_VERIFIED** — el EA exportado declara `input long MagicNumber` y el valor que MT5 ejecutó realmente (Inputs del HTM) es IGUAL a la mágica durable de `sqx.strategy_magic` en **22/22 estrategias** del E2E w10. El truncamiento int32 del defecto forense (26100091079 → 330287303) quedó eliminado en la cadena completa.

## Reparación en la autoridad real

- El generador físico del MQ5 es el `SourceCode.generate` de SQX (JAR propietario Build 144, no parcheable — "no parchear binarios"). La costura propia es el plugin `EchoForgeMT5Exporter`: `enforceMagicWidth()` reescribe EXACTAMENTE la declaración `input int MagicNumber = <durable>;` → `input long MagicNumber = <durable>;` antes de publicar el .mq5 durable. No es sustitución textual ciega: patrón anclado al input MagicNumber, exactamente 1 declaración exigida (0 o >1 → excepción, no se publica), idempotente, no toca el allocator ni reduce mágicas.
- Precedencia de runtime descubierta y certificada: en Build 144 headless, `sqcli` RECOMPILA el snippet `user/extend/Snippets/.../EchoForgeMT5Exporter.java` por corrida y pisa la clase del JAR en `internal/tmp/compiled`. El deploy correcto actualiza snippet + JAR (hecho 3/3 con backups).

## Regresiones añadidas (contrato del mandato)

| Requisito | Regresión | Resultado |
|---|---|---|
| Magic > int32 | simulador `widensIntMagicToLong` con 26100091079; Go `TestFromMQ5_LongDeclarationBeyondInt32` (Int64() sin error) | PASS |
| Valor declarado en MQ5 | `magicreadback.FromMQ5` acepta `long` (patrón `(?:int|long)`); canario físico Zeus/Hera/Kronos | PASS 3/3 |
| EX5 compilado | MetaEditor compiló 22/22 MQ5 con `input long` — 0 errores (stage rows mt5_compiler COMPLETED) | PASS |
| Inputs efectivos del Strategy Tester | `magicreadback.FromHTMInputs` lee MagicNumber del bloque Inputs del HTM (unit tests: presente/ausente/ambiguo/título) | PASS |
| HTM de readback | gate `verifyEffectiveMagic` en `mt5_reconcile_v1`, corre ANTES de cualquier escritura durable | PASS |
| Coincidencia exacta con sqx.strategy_magic | mismatch/missing → `CONTRACT_CONFLICT` non-retryable; comparación NUMÉRICA (el literal de un truncado int32 nunca iguala el decimal de 11 dígitos) | PASS |

## Evidencia física del E2E w10 (FlowRun 79385c32)

- **Canario focalizado PRE-dispatch 3/3**: .sqx control con mágica 26100091079 → MQ5 exportado declara `input long MagicNumber = 26100091079;` en Zeus, Hera y Kronos (0 declaraciones `int`). Evidencia: `/tmp/canary-evidence/canary_magic64.mq5` por host.
- **Gate de reconcile 22/22**: logs de workers con "Mágica efectiva MT5 verificada contra sqx.strategy_magic" — Zeus 7, Hera 8, Kronos 7 = 22 (mágicas p.ej. 26100091085/087/102).
- **Round-trip exacto**: `sqx.strategy_magic` para final-c842ce88 = `26100091085`; el MQ5 durable de esa estrategia declara `input long MagicNumber = 26100091085` (fetch MinIO `durable/mt5-export/v1/79385c32/.../final-c842ce88….mq5`). Rango completo de la cohorte: 26100091082..26100091103 (22 asignaciones, todas >int32).
- El gate que el mandato exigía ("comparar el valor realmente utilizado por MT5, no solamente el literal del fuente") es exactamente el nuevo `verifyEffectiveMagic`: pasó 22/22 en producción.

## Negativos

- Un HTM con mágica truncada (330287303) contra durable 26100091079 produce `CONTRACT_CONFLICT` non-retryable sin persistir nada (test `TestMT5ReconcileActivity_EffectiveMagicMismatchFailsClosed` — el error reporta ambos valores).
- Asignación durable ausente → fail-closed (test dedicado).
