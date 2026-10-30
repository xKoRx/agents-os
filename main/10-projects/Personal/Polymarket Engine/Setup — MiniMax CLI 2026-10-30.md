---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-10-30"
updated: "2026-10-30"
---

# Setup — MiniMax CLI 2026-10-30

## Propósito

Conectar Polymarket al provider MiniMax existente mediante ZCode CLI, sin copiar claves ni cambiar el modelo global. Rodrigo autorizó retomar usando MiniMax M3.1 Flash sin horario; GLM-5.3-Flash sólo como respaldo y fuera de lunes a viernes 02:00–08:00 GMT−3. Esta etapa completó setup y probe; no ejecutó desarrollo del producto ni reactivó automatizaciones.

## Resultado verificado

- Hefesto: hostname corroborado. Desktop 3.17.1, CLI 3.16.3-40. Comparten el registro personal de providers. Aunque el catálogo empaquetado CLI es revisión 33, el activo ya es revisión 43 y contiene `minimax/MiniMax-M3.1-Flash` habilitado.
- El provider `minimax` tiene acceso configurado y endpoint `https://api.minimax.io/anthropic`. No se copiaron credenciales ni se cambió el default global GLM. La selección de MiniMax es explícita por ejecución.
- Probe: 2026-10-30T20:29:35Z–20:29:43Z; exit 0, respuesta exacta `MINIMAX_OK`, sesión `sess_0fd5f52b-b761-4616-b675-de13b32125a8`. `model_usage` registra provider `minimax`, modelo `MiniMax-M3.1-Flash`, una petición, cero tool calls y cero filas `tool_usage`; 7895 tokens de entrada y 252 de salida. La identidad está respaldada por metadata del cliente y su petición, no por una autoafirmación del modelo ni una atestación independiente del servidor.
- CWD vacío, sin contexto del proyecto; skills, MCP, plugins, memoria y subagentes desactivados; hook deny-all para herramientas. Sin fallback. El primer intento falló en startup por filesystem read-only al crear locks; terminó exit 1 antes de la llamada. El reintento usó la integración con acceso normal aprobado y produjo el resultado anterior.
- Guard horario: tres tests PASS; matriz de 7×1440 minutos, GMT−3 y UTC, MiniMax/GLM/modelo no autorizado, bordes y rollover de fin de semana. Ningún modelo invocado en estos tests. MiniMax no tiene cutoff horario; GLM exige flag explícito y recibe cutoff antes de la próxima ventana prohibida.

## Evidencia y controles

- Workspace Hefesto `Documents/Codex/2026-10-30/task`, subdirectorio `minimax-setup/`: `verified-probe.json`, `probe-result.json`, `probe-result-2.json`, `guard-tests.json`, logs y SQLite locales. No se llevan dumps al vault.
- Nuevo supervisor: `minimax-setup/product-supervisor/supervise.py`, con `setup-manifest.json`, settings idénticos a W1-m, referencia al hook anterior sin cambios e inputs inmutables preservados. Conserva lock, integridad, baseline limpio, control de memoria/disco y seguimiento/drenaje de descendientes. El próximo prompt aún no existe: fail-closed hasta que el despacho apruebe el alcance y revise el hook. No reutilizar ni sobrescribir los recibos W1-m.
- Checkout `polymarket-engine`, rama `w0/offline-causal-replay-20261027`, commit local `9f6caaac654a7dd8cef078ca4a7f71a3ef9d928d`, limpio. Ningún cambio al producto. `REAL_FEE_READY=false`, fees `UNRESOLVED`, resultado científico `INCONCLUSIVE`.

## Próximo incremento propuesto — no ejecutado

Añadir una regresión sintética directa para `sufficiency_deficit` de ENTRADA: fixture aceptado que carezca de asks suficientes para el notional objetivo; pin de estado, profundidad/importe faltante y nulls de salida/P&L. Añadir el caso límite de profundidad exactamente suficiente para detectar un rechazo incorrecto. Reutilizar el harness sintético existente, sin captura, red, estrategia, tuning, fee certificada, OOS ni cambio de L. La sensibilidad alternativa de L permanece NOT_RUN y requiere definir la regla antes de cambiarla.

Verificación propuesta: tests focalizados del nuevo caso y suite `go test -p 1 -count=1 -timeout 15m ./cmd/researchpilot ./internal/economics ./internal/regimes`. El despacho debe revisar los destinos de TestMain y preparar hook/prompt propios de la etapa para preservar los artefactos W1-j/W1-m; todavía no se autorizó ni ejecutó ese shot en este setup.

Comando de despacho preparado desde el workspace indicado: `python3 minimax-setup/product-supervisor/supervise.py --preflight`; ejecución posterior: `python3 minimax-setup/product-supervisor/supervise.py --execute`. Requiere antes el nuevo `master-prompt.md` y revisión scoped del hook; hoy el preflight debe fallar por ese archivo ausente. GLM sólo mediante `--fallback-glm`, nunca automático.

## Fuentes

- [[Polymarket Engine — Continuidad Five-POC 2026-09-20]], § Cierre W1-m.
- [[Research — Economic Instrumentation W1-m 2026-10-30]].
- Documentación local del CLI: `docs/PROVIDER_CONFIG.md`, `docs/CONFIGURATION.md` y código del launcher; sesión y usage del probe.
