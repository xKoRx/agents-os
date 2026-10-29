---
type: change_log
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: ["[[Echo Futures]]"]
related: ["[[EF-CAMPAIGN-MODES-DESIGN]]", "[[EF-CAMPAIGN-MODES-I0-LOCAL]]", "[[2026-10-28-chatgpt-astra-echo-campaigns-c04-source-review]]"]
aliases: []
confidence: verified
source_session: unknown
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-28 — Echo campañas C04 — reutilización, composición y migración

## Cambio

- Updated por delta: [[Echo Futures — Optimización de Campañas]], [[EF-CAMPAIGN-MODES-DESIGN]] y [[EF-CAMPAIGN-MODES-I0-LOCAL]]. Mismos planner/diseño/paquete; sin documento arquitectónico duplicado.
- Created: este change_log y [[2026-10-28-chatgpt-astra-echo-campaigns-c04-source-review]] para el segmento material de review de código.
- Producto y entorno LOCAL: read-only. No implementación, branch, merge, reset, tests/build/campañas, gastos, trading ni deploy de Echo. No cierre del manager.

## Motivo

Owner aclara la capacidad reusable: una lógica por modalidad, módulos Strategy/MM propios, GAU50/E2T como perfil/config con N cuentas y una activa por asociación; múltiples campañas independientes y SIMULATION genuina con mercado/reloj/bankroll conjunto son capacidades diferentes. Solicita dictamen antes de confirmar despacho, migración de campañas antiguas y conocimiento durable para siguientes agentes.

## Fuentes usadas

C03 previamente publicado en cb3495e8e510669ea9d84f70ce1f88ec87ec165a, sin cambios materiales en los tres archivos en HEAD recuperado 610ef5306648d234b026e92676f8d9d35ce51236. Echo master sigue 2baf319ddcba622d9557bc9f23a13787b44c58a7. Entrada/base/routing Agents-OS refrescados; autoridades de gestión/SDD/retester vigentes. Dos reviews SOURCE focales separados y corroboración del manager; referencias exactas en C04 §26.

## Resolución aplicada

1. Dictamen DESIGN_READY_WITH_MINOR_DELTAS limitado al contrato/I0; se conserva el mismo driver y factories SDK. Nuevos módulos pueden requerir registro/admisión/policy; no Campaign por Strategy.
2. Se registra explícitamente la generalidad todavía limitada: perfil E2T/GAU50, TGMM-specific objectiveCapacity, una funded seed, un Provider/ledger/venue instalado y RuleSet global. El test pool sellado no acredita driver simultáneo.
3. Se distingue rotación actual de simultaneidad multi-asociación; I4 requiere adaptación localizada por adjudicar, incluida trayectoria OHLC común, sin segunda autoridad ni refactor preventivo ahora.
4. I0 incorpora identidad de instancia/attempt/revisión/scope, eventos/linaje/tiempo y frontera Python/Go. Nuevos negativos V31–V36; tres mandatos del mismo paquete ajustados. Ningún layout físico I4 anticipado.
5. Migración incremental de Platform CHALLENGE/FUNDED/FULL_JOURNEY y CAMPAIGN legacy con mapa source→target, SAME_SEMANTICS/NEW_EXPERIMENT y preservación de recibos. S04-F01/F02 continúan abiertos en su alcance.
6. Cuatro shots propuestos: implementar/verificar/corregir I0; cuarto reservado para GOD de la primera decisión Go concreta, sin gate adicional previo al reporter. Estado actual NOT_DISPATCHED por la solicitud Owner de revisión previa. Prompt reservado incluido en el mismo paquete; no se crea un retorno vacío.

## Validación

Source inspeccionado y límites documentados; ninguna prueba de producto ejecutada. Review ONE-SHOT del delta: PASS_DOCUMENTAL, sin hallazgos materiales. Se incorporó su única precisión editorial: el mandato GOD limita los cambios aditivos al contrato/proyección I0, sin prohibir la adaptación Go posterior admitida. Lint canónico strict sobre cinco notas: ERROR=0, WARN=0; fences y templates verificados. Publicación sobre master reconciliado con expected_sha, sin force, y readback de blobs exigidos. C02, recibo C03 y reconciliación S04 anteriores no se reescriben ni se convierten en aceptación de C04 física.

## Compartibilidad

Scope local al repositorio autorizado del Owner; sin mensajes a terceros, publicación externa, secretos o cambios en cuotas Pro. Consumo UNKNOWN.

## Rollback

Revertir sólo este delta documental mediante commit inverso sobre master reconciliado, sin reset/force ni cambios ajenos. C03 y su mandato siguen recuperables por historial. No existe código nuevo de producto que revertir.

Manager/programa abiertos. Próxima actualización por despacho Owner o retorno verificable. I+D conserva decisiones económicas y su planner central.
