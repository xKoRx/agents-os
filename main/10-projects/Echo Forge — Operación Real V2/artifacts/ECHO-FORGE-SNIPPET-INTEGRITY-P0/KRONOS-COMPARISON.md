# KRONOS-COMPARISON — Snippet Integrity P0 (2026-10-19)

## Veredicto Kronos

`NOT_AFFECTED_WITH_CAUSAL_EVIDENCE` — el mecanismo (bug del script de deploy) está presente en todos los hosts porque es el mismo script; el **trigger** (directorio de snippets no escribible por la identidad que ejecuta el deploy) no existe en Kronos ni Hera porque sus directorios son `kor:kor`. La diferencia es causal y demostrada, no observacional: sus sellos `SHA256SUMS.after` muestran `live = b5f85c4e…` (el swap del fuente SÍ persistió).

## Comparativa física (leída read-only el 2026-10-19 ~22:4xZ–23:0xZ)

| Dimensión | Zeus | Kronos | Hera |
|---|---|---|---|
| Source S02 (b5f85c4e, 87.157 B) | ✅ (desde 18:22:43Z, `echo-dev:echo-dev` 664) | ✅ (`kor:kor` 664, mtime 16:31:22Z por `cp -a`) | ✅ (`kor:kor` 664, mtime 16:31:22Z) |
| Ownership/permisos dir snippets | `echo-dev:echo-dev` 775 — kor sin w (trigger del incidente) | `kor:kor` — kor con w | `kor:kor` — kor con w |
| JAR efectivo `user/libs` (clase main `3ec6e112…`) | ✅ | ✅ | ✅ |
| `Snippets.jar` interno (clase main) | ✅ `3ec6e112…` | ✅ `3ec6e112…` | ✅ `3ec6e112…` |
| Cache compilado `internal/tmp/compiled` | Existe, clase main `3ec6e112…` (reescribo per-run; última 19:49:41Z) | Existe (creado por canary 17:56Z), clase main `3ec6e112…` | Existe (creado por canary 17:59Z), clase main `3ec6e112…` |
| Compilación por corrida | Sí (fuente = autoridad) | Sí | Sí |
| Scripts de deploy | Mismo `deploy.sh` `b52addbe…` en los 3 (idéntico byte a byte) | idem | idem |
| Stager/mantenimiento | `stager.timer` 30 s, `ProtectSystem=full`, no toca SQX | ídem (no auditado a fondo — sin evidencia de intervención) | ídem |
| Trigger del problema (dir no escribible por kor) | PRESENTE | AUSENTE | AUSENTE |
| Seal del deploy: live = src | ❌ NO (src `b5f85c4e` / live `03106b81`) → bug disparado | ✅ SÍ (ambas líneas `b5f85c4e`) | ✅ SÍ (ambas líneas `b5f85c4e`) |
| Hash estable post-fix | ✅ PASS gate 3 verificaciones | ✅ PASS gate | ✅ PASS gate |

Nota: la nota de rollout "Kronos/Hera no tienen cache" quedó desactualizada: hoy los 3 hosts tienen `internal/tmp/compiled` (lo crea el primer sqcli run); el gate lo verifica y está coherente en los 3.

## Historial de deploy por host (backups `plugin-s02-*`)

- **Kronos: 4 corridas** — `174014Z`, `174313Z`, `174914Z` (3 aborts sin `SHA256SUMS.after`: el guard `pgrep sqcli` detuvo el deploy con la flota activa; los 3 backups quedaron como estado previo) y `175624Z` (completo: backup, compilación, swaps, sello con `live=b5f85c4e`, rollback). Canary `ef-canary-s02-175647` con marker `Parallel workers: 2`.
- **Hera: 1 corrida** — `175925Z` completa con sello `live=b5f85c4e`. Canary `ef-canary-s02-175952` con marker `Parallel workers: 2`.
- **Zeus: 1 corrida** — `180331Z` con el sello mixto (incidente). Canary 3 tras corrección manual.

El guard anti-SQX-activo del script FUNCIONÓ en Kronos (3 aborts limpios) — el único defecto era el swap silencioso, disparado sólo por la combinación Zeus + identidad kor.

## Respuestas exigidas (§6)

1. ¿Existe el mismo proceso o mecanismo restaurador? **No existe proceso restaurador en ningún host**; el mecanismo es el bug del script (presente en los 3).
2. ¿Puede escribir sobre el source de S02? En Kronos/Hera el deploy como `kor` puede; en Zeus no sin identidad `echo-dev`/elevación.
3. ¿Se ejecuta bajo las mismas condiciones? Sí (mismo script, misma identidad kor) — con ownership distinto del dir.
4. ¿La diferencia de permisos evita el problema o sólo lo oculta? **Evita** este trigger concreto (kor puede escribir); no oculta el bug: con cualquier futuro dir no-escribible fallaría igual — por eso el fix es el script, no los permisos.
5. ¿Ruta de bytecode antiguo? La misma en los 3: fuente viejo → recompilación per-run → cache+`Snippets.jar` re-escritos con bytecode viejo. Requiere fuente divergente, que el gate pre-dispatch ahora detecta.
6. ¿El mismo trigger produce el mismo efecto? Reproducido físicamente en Zeus candidate-local (FASE B) con dir 555; en Kronos/Hera el trigger no existe (causa demostrada).
7. ¿Un trabajo SQX real puede activarlo? No — el trabajo SQX sólo compila; el trigger es del deploy, no del runtime.
8. ¿Qué cambia entre Zeus y Kronos? Exclusivamente el ownership del directorio de snippets.

## Hera (control RO)

Sin hallazgos propios: estado íntegro, mismo mecanismo latente, sin trigger. Sin auditoría general de flota (fuera de alcance).

## Corolario para futuros hosts

Cualquier host nuevo con dir de snippets no-escribible por la identidad de deploy repetirá el incidente si se usa el script viejo. El gate pre-dispatch (`verify-plugin-integrity.sh`) es el detector universal independiente del ownership.
