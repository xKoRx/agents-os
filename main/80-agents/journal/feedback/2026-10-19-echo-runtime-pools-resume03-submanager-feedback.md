---
type: feedback
schema_version: 1
scope: session
created: 2026-10-19
updated: 2026-10-19
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
entities:
  - "[[Echo Futures — Runtime Pools]]"
related:
  - "[[2026-10-19-cert-nt-01-resume03-summary]]"
  - "[[2026-10-19-zcode-glm53-echo-runtime-pools-resume03-typename-fix]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
agent_run: "[[2026-10-19-zcode-glm53-echo-runtime-pools-resume03-typename-fix]]"
session_goal: RESUME-03 CERT-NT-01 — fix P1 typename, release, redeploy, retoma de certificación
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
---

# Session Feedback — 2026-10-19 — echo-runtime-pools-resume03

## Context

Mandato RESUME-03 (Primary Manager GPT-6): implementación correctiva local del P1 del typename con especialistas A→B→C, release, redeploy DEV y retoma de CERT-NT-01. Related run: [[2026-10-19-zcode-glm53-echo-runtime-pools-resume03-typename-fix]].

## Hallazgos operativos (lo aprendido)

- **«Falta que el Manager pushee» fue una dependencia falsa**: el fix era implementable localmente en ~20 min de especialista + verificación. Cuando un bloqueo se define como «dependencia del Manager» sin que el mandato lo prohíba, evaluar primero si el submanager local tiene la autoridad y el alcance para cerrarlo (el despacho RESUME-03 lo explicitó y cambió el resultado).
- **Pinnear la gramática contra el runtime REAL descompuso la ambigüedad**: extraer la clase `TypeName` del jar desplegado (md5) + source del tag exacto convirtió «debería funcionar» en oráculo verificable; el mirror en Go con casos adversarios (`a/b/` VÁLIDO por recorte trailing) atrapó un error de transcripción del PROPIO submanager en su tabla de evidencia — el especialista que verifica la evidencia del manager es parte del diseño.
- **El inventario mecánico de call sites del helper evitó el fallo en cadena**: A encontró 2 usos del helper en `strategy_engine` que ni RESUME-01 ni el grep inicial del submanager habían atribuido (11→21 call sites reales). «Arreglar el helper» sin inventario habría dejado el crash siguiente.
- **El gateway ETCD DEV (.250:2379) devuelve vacío en range key-only**: toda lectura exacta debe usar `{"key":K,"range_end":K+".0"}`. Probablemente explica lecturas «fuzzy» históricas atribuidas al MCP.
- **Actor externo borró claves ETCD de provisioning en vivo** (22:31Z, sin lease): el estado del entorno puede mutar bajo la sesión; re-verificar las precondiciones JUSTO antes de cada paso destructivo (C lo hizo y el runbook contemplaba STOP si reaparecía).
- **Timeout del transporte como clase de defecto distinta**: el fix correcto puede desplegar un defecto preexistente de capacidad (batch 1001×2,5 MB vs call-timeout/2048 MB del worker). El rollback de module con core nuevo PERMANECIENDO es la separación correcta: la fuente quedó verificada en vivo aunque la topología no soporte aún la carga.
- **Fricción**: el MCP SSH expira sesiones bajo uso prolongado (recuperación por HTTP directo con bearer, helper `mcp_ssh_call.sh` — funciona bien); `docker logs` con awk de rangos temporales excede el timeout de 30 s del canal (usar `--since/--until`).

## Sugerencias

- El próximo despacho (timeout de transporte) debería empezar por medir el coste real de procesamiento por envelope del core (el worker respondía sano; el batch de 1001 acumulados sugiere backpressure) antes de tocar configuración de Flink.
- Considerar publicar la gramática TypeName como recurso del vault (30-resources) si va a reusarse en futuros owners StateFun.
