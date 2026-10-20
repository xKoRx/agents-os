---
type: feedback
schema_version: 1
scope: session
created: 2026-10-20
updated: 2026-10-20
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
entities:
  - "[[Echo Futures — Runtime Pools]]"
related:
  - "[[2026-10-20-zcode-glm53-echo-runtime-pools-resume05-timeout-fix]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
agent_run: "[[2026-10-20-zcode-glm53-echo-runtime-pools-resume05-timeout-fix]]"
session_goal: RESUME-05 CERT-NT-01 — perfilar, corregir y demostrar estabilidad del timeout StateFun→Core
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
---

# Session Feedback — 2026-10-20 — cert-nt-01-resume05

## Context

Mandato RESUME-05 (Primary Manager GPT-6): perfilar y corregir el timeout StateFun→Core con demostración, no estimación aritmética. Run: [[2026-10-20-zcode-glm53-echo-runtime-pools-resume05-timeout-fix]].

## Hallazgos operativos

- **Contar salidas canónicas ≠ medir capacidad del handler.** El RCA RESUME-04 derivó ~150 ms/envelope de un promedio global (4460 canónicos / 720 s). La medición directa con perfil CPU mostró que el costo era serde JSON del bundle completo por envelope (`store()` 59% + `load()` 40%; spec `sequencer` 2,1 MB), con engine ≈1%. El criterio de éxito debe incluir frescura y progreso, no sólo ausencia de excepciones: el fix eliminó los timeouts (estabilidad PASS 31,7 min) pero la edad del evento siguió creciendo (MITIGACION_INSUFICIENTE) porque el throughput del mailbox serializado (20,5 rec/s reales) no alcanza el ingress (46,1 rec/s). Ambos números deben reportarse por separado, siempre.
- **Overhead de transporte no trivial:** servicio real 20,5 rec/s vs 28,1 in-proc (−27%). Benchmarks in-proc subestiman el deficit; validar la pendiente con medición en el runtime real antes de prometer paridad.
- **Subagentes one-shot y supervisor:** el harness mata al subagente tras 10 min sin llamada a herramienta; las pruebas largas (suites 30 m, sustained 13 min) deben correrse en background con sondeo cada 30-60 s. Un worker dekillizado deja artefactos aprovechables: auditarlos y cerrar sólo los gaps (B→B') en vez de re-ejecutar todo.
- **Sesiones MCP SSH expiran entre llamadas largas:** para monitoreos prolongados usar re-init por llamada (helper `mcp_ssh_call.sh` con initialize+session-id) o superficies HTTP publicadas (Flink REST :8082 alcanzable sin SSH).
- **ETCD gRPC-gateway:** claves/range_end SIEMPRE en base64 (no hex); el range key-only devuelve vacío. Gotcha repetido dos veces en este proyecto — la forma correcta está en RESUME03-RUNBOOK-C.md.
- **Canal Owner que nadie había usado:** el evidence-log del relay de feed (`~/opt/echo-dev/var/nt-feed/evidence.jsonl`) publica en vivo el descubrimiento de cuentas del AddOn D6 con `Account.Id` — cerró el dato "ID de plataforma de Sim101" sin GUI ni AddOn nuevo, verificado contra el source de ambos AddOns (mismo `Account.Id` que el drift-check).
- **Parser real sin NT:** la lógica de parseo del AddOn C# (`ParseBindings`/`ExtractJsonString`) es reducible a un harness csc .NET 4.8 sin assemblies NT (clase no-AddOnBase + JSON por argv) — permite validar configs Owner con el parser REAL + test negativo fail-closed antes del ciclo del Owner.

## Mejoras propuestas

- Modelar el estado del sequencer shardado/incremental (ValueSpecs múltiples o codificación compacta O(1) por envelope) en un shot futuro: es la única palanca que alcanza paridad de ingress con este protocolo ValueSpec de bundle completo.
- Registrar en runbooks de deploy la regla "estabilidad y frescura se reportan por separado" con la tabla de DefaultFreshnessBounds como cota explícita.
