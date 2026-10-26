---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# D — GLM Handoff Packages

## Propósito

Prompts maestros para contexto fresco. B es la SPEC única; estos prompts recuperan autoridad y definen ejecución sin duplicarla ni autorizar despliegue.

## Contenido

### D1. Despacho

Cada bloque D2/D3/D4 es un prompt completo utilizable por separado. Modelo obligatorio **GLM-5.3-Flash Max LOCAL** para todos los especialistas posteriores. Verificar modelo/entorno antes de ejecución; si se lanzó otro, reportar discrepancia. Guardar este documento no inicia ningún shot.

### D2. Prompt maestro — Shot 2 implementación e integración temprana

~~~text
ECHO INGESTION V2 — SHOT 2. Actúa con GLM-5.3-Flash Max LOCAL como implementador responsable. Es el segundo de exactamente cuatro shots; no nuevos shots ni rediseño GOD por defecto.

Arranca Agents-OS leyendo AGENTS.md canónico y ejecutando una vez 80-agents/skills/agents-os-bootstrap/SKILL.md. VAULT_ROOT contiene 80-agents/agents-os/agents-os.md. En warm reutiliza contexto. Proyecto existente: 10-projects/Echo/Echo — Producto Integrado.md. Documentación xKoRx/agents-os sólo master, sin PR ni ramas de trabajo. No cierres Agents-OS.

Recupera autoridad:
1. 10-projects/Echo/The Lab/F — Decision Register.md D25/D26 y decisiones compatibles D09/D10/D11/D16–D22. D25/D26 sustituyen sólo partes indicadas de D23/D24.
2. 10-projects/Echo/Ingestion V2 — Operational Integration/A — Source Baseline and Branch Integration.md.
3. Misma carpeta/B — Frozen Architecture.md (SPEC única), C — Implementation Shots and Acceptance Gates.md y E — Executable Contract Examples.md.
4. 10-projects/Echo/The Lab/V4 — Runtime Integration/H — Test Matrix Independent Oracles.md, SHOT4_FINAL_HANDOFF.md, SHOT4_FINAL_COVERAGE_MATRIX.md, SHOT4_INDEPENDENT_FINAL_REVIEW.md. Consulta A–J V4 según delta; preserva matemática/contratos compatibles.
5. 30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md y skills de implementación/testing/ambiente resueltos por bootstrap.

Baseline: xKoRx/echo lab-v4/shot4-integration@b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce. Nueva rama propuesta feature/lab-v4-ingestion-v2 DEBE salir del HEAD remoto actualizado de esa rama. Comprueba disponibilidad/ownership y registra SHAs. NO master, feature/ef-runtime-pools, feature/lab-v4-shot4 ni backtester. Runtime@0e17c4d3f1179cde709f923c8dd28e8cd853afc9 es referencia, no destino autorizado. Divergencia125/64 y colisión SQL081 prohíben trasplante ciego. Symphony candidato lab-v4/shot4-symphony@a0c68d154b733049c97bf46e69c4629078d40c05: refresca y usa hija candidate-local si lo modificas, sin deploy/campaña.

PRIMER trabajo obligatorio: incremento E de C2, endpoint V2. Reutiliza Gateway/router/harness/SDK/PG/registry/history. Resuelve B2–B4, ejemplos E. E01–E12 requieren router HTTP real, PG/store reales aislados, readback independiente, restart/replay/conflictos/rollback/migraciones/regresiones. No handler/mocks/200 como sustituto. Analytics detenido no impide aceptación;0órdenes. Mientras provisioning no esté completo, PROVISION_REFERENCE devuelve503 explícito sin efectos, nunca falso PROVISIONING.

Al obtener ECHO_INGESTION_V2_ENDPOINT_INTEGRATION_PASS integra INMEDIATAMENTE ese incremento autocontenido en lab-v4/shot4-integration siguiendo A4. No esperar readiness/copy/curvas/frontend ni fin del shot. No incluir funcionalidades posteriores parciales. Refresca destino, incorpora commits ajenos y revalida si avanzó; push normal sin force. Registra BASE_SHA, ENDPOINT_SHA, destino antes/después, evidence digest y RESUME_BASE_SHA. Si baseline ya pasa físicamente todo, registra PASS sin fabricar delta/merge. Sincroniza rama y sólo entonces continúa O/J/L/F.

B5/B6: profile autorizado/config completa/CAS, consumer propio aplica y confirma lookup/checkpoint antes de ACK, incarnation/epoch/lease/renewal. No installer nil ni targets libres. OBSERVE_MASTER sin execution ficticia. NEW OPEN exige readiness actual en planner y último envío; management seguro conserva ciclo original.

B7/B8: managed_context exacto, event/cycle IDs durables, source-instance/account/ns/version/run/binding, un journal owner, no Signal nativa externa. OPEN pre-ready se conserva pero nunca se copia retroactivamente. Copy por policies/MM existentes por cuenta, provider simulado, command key durable; UNKNOWN_OUTCOME exige lookup.

B9/B10: projector asíncrono por snapshots/grupo exacto, N+1 acumulativo y delivered sólo procesados; writer Echo no remapea Forge. Worker/cuatro curvas/dos rankings/cohortes/readbundle/UI V4 existentes. No inventar Q/FX/fills/costes/fechas. Adapter Forge usa store durable existente y valida receipt; artefacto auténtico sólo copia autorizada existente.

Gates C3 y H afectados. H01–H49 separados de QA01; H45/QA01 históricos no se resuelven por inferencia. AUTH_FORGE ausente limita sólo autenticidad. Falta de implementación es FAIL, no bloqueo externo. Commits/integraciones posteriores completos con evidencia; sin runtime merge/deploy/cutover.

Harness propio, guard de efectos externos, PG/ETCD/Kafka/StateFun/Hasura propios cuando necesarios, brokers simulados. PROD read-only, ninguna orden real, flota/cuentas/infra compartida ni restart Forge/extracción. No secretos/logs grandes/binarios en vault, no sync.sh/.sync, force-push ni borrado ajeno.

Termina persistiendo reporte Shot2 en el workstream: SHAs integrados/candidate, early-merge proof, matrices/casos, source/build/SQL/module/front/metadata digests, evidencia relativa externa, limitaciones y cleanup. Actualiza proyecto/continuidad y change_log consolidado directamente master, commit/push/readback. Entrega paquete fresco para Shot3 independiente; no auto-certificación, no inicio automático de Shot3 ni cierre Agents-OS.
~~~

### D3. Prompt maestro — Shot 3 QA adversarial independiente

~~~text
ECHO INGESTION V2 — SHOT 3. Eres GLM-5.3-Flash Max LOCAL en sesión fresca sin autoría de implementación. Si participaste en Shot2, no puedes ser auditor independiente. No modifiques producto para hacer verdes pruebas.

Bootstrap una vez desde AGENTS.md y 80-agents/skills/agents-os-bootstrap/SKILL.md; VAULT_ROOT por marker agents-os.md. Proyecto 10-projects/Echo/Echo — Producto Integrado.md. Documentación xKoRx/agents-os sólo master, sin PR/ramas ni cierre.

Lee 10-projects/Echo/The Lab/F — Decision Register.md D25/D26. Dentro de 10-projects/Echo/Ingestion V2 — Operational Integration/ lee A — Source Baseline and Branch Integration.md, B — Frozen Architecture.md, C — Implementation Shots and Acceptance Gates.md, E — Executable Contract Examples.md y reporte/manifest Shot2 enlazado en proyecto. Lee The Lab/V4 — Runtime Integration/H — Test Matrix Independent Oracles.md y SHOT4_FINAL_HANDOFF.md, SHOT4_FINAL_COVERAGE_MATRIX.md, SHOT4_INDEPENDENT_FINAL_REVIEW.md. Consulta contratos V4 según caso. Lee 30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md y skills QA/ambiente que determine bootstrap.

Verifica SHAs reales remotos/candidate y que endpoint se integró temprano a lab-v4/shot4-integration antes de O/J/L/F. Origen b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce o descendiente revisado, nunca runtime/master. Inspecciona diff, module sums, build vcs_revision/modified, migraciones/metadata/frontend del artefacto auditado. No heredes PASS Shot2/Shot4 histórico.

Ejecuta C4/C3: falsifica auth/scopes/grants, replay/key conflict, CAS/races, crash antes/después commit/apply/ACK/worker; config publicada sin aplicar; lease/incarnation inválidos; multi-source/multi-version; OPEN pre-ready; duplicate journal; UNKNOWN_OUTCOME/copy duplicada; N/N+1/batches; moneda/costes/Q insuficientes; cohort parcial; UI N/N+1/Hasura. Expected propio desde fuentes/oráculos independientes, sin helpers del producto bajo prueba.

E/O/J/L/F pertinentes y49 filas H con estados individuales. QA01 coverage aparte, H45 SLO histórico FAIL salvo prueba suficiente; separar regresión nueva/excepción histórica. Fixture sintético no certifica AUTH_FORGE. BLOCKED_EXTERNAL requiere recurso/permiso concreto e intento, nunca defecto implementable. Continuar independientes.

Sólo harness propio con guard, simuladores y ownership/cleanup H47/H48. Ninguna orden real, deploy, migración compartida, campaña/restart Forge, runtime paralelo, cuenta real/extracción. No force-push/borrado ajeno. Tests adversariales propios/evidencia fuera vault, sin modificar rama producto.

Entrega findings C4: severidad, reproducción, SHA/build/fixture, expected/actual, evidencia, owner/atribución/criterio de corrección. Matriz completa/conteos disjuntos PASS/FAIL/NOT_RUN/BLOCKED_EXTERNAL y QA01; SHAs y cleanup. Persiste reporte/paquete Shot4 en workstream, actualiza continuidad/proyecto/change_log master, commit/push/verifica. No fixes producto, Shot4 automático, cierre Agents-OS ni Shot5.
~~~

### D4. Prompt maestro — Shot 4 fixes y certificación independiente

~~~text
ECHO INGESTION V2 — SHOT 4 FINAL. Modelo implementación/verificación GLM-5.3-Flash Max LOCAL. Cuarto y último shot; no Shot5, subshots indefinidos ni revisión GOD por defecto.

Bootstrap Agents-OS una vez desde AGENTS.md/80-agents/skills/agents-os-bootstrap/SKILL.md; VAULT_ROOT por marker, sesión permanece abierta. Proyecto 10-projects/Echo/Echo — Producto Integrado.md; Agents-OS sólo master sin PR/ramas. Lee 10-projects/Echo/The Lab/F — Decision Register.md D25/D26 y, en Ingestion V2 — Operational Integration/, A — Source Baseline and Branch Integration.md, B — Frozen Architecture.md, C — Implementation Shots and Acceptance Gates.md, E — Executable Contract Examples.md y reportes Shot2/Shot3 enlazados. Lee matriz H/reportes finales V4, Environment Contract en 30-resources/aranea/07-integration/ y skills pertinentes.

Verifica SHAs/diff/ownership y early merge. Trabajo desciende lab-v4/shot4-integration, jamás runtime por inferencia. Corrige findings atribuibles al programa y regresiones siguiendo B sin rehacer LAB ni alcance futuro. Preserva repros Shot3/criterios. Gate E permanece válido. Commits autocontenidos, SQL forward aditivo, no borrar datos. Integra sólo incrementos completos con A4/SHAs/revalidación si destino avanzó; no deploy/cutover.

Repite repros/gates afectados/regresiones completas de esas superficies: crash/races/readiness/last-hop/journal/history/cohort/UI. Registra source/build/module/front/metadata/migration hashes y evidence manifest. Sólo provider simulado/harness propio; PROD read-only, ninguna cuenta/config/infra compartida, extracción ni worker Forge tocados.

Después de fixes y SHA final fijo, despacha otra instancia GLM-5.3-Flash Max LOCAL independiente, fresca y sin autoría de producto/fixes. Verifica dentro de Shot4, no un nuevo shot. Instrucción del verificador: leer las mismas autoridades/findings, comprobar SHA final integrado/árbol/build, repetir repros y regresiones con expected propio, rechazar claims falsos de apply/READY/autenticidad, reportar identidad de sesión/modelo y evidencia. No aceptar sólo el reporte implementador. Sin instancia independiente no declarar certificación independiente.

Estados PASS/FAIL/NOT_RUN/BLOCKED_EXTERNAL explícitos;49H y QA01 aparte. H45/QA01 históricos con no-regresión probada; AUTH_FORGE ausente limita autenticidad. Defecto producto no es externo. Sin P0/P1 nuevo abierto para certificación funcional. Si no logra cierre, entregar FAIL/pendientes dentro de Shot4, sin verde ficticio ni otro shot.

Persiste correction log y reporte independiente final con findings/SHAs/matrices/evidencia relativa externa/gates/limitaciones/cleanup. Actualiza proyecto/continuidad/change_log consolidado master, commit/push/readback. No cerrar Agents-OS sin orden Owner ni interpretar certificación local como release/deploy/runtime merge autorizado.
~~~


## Fuentes

- Mandato Owner 2026-10-26; [[F — Decision Register]] D25/D26.
- [[A — Source Baseline and Branch Integration]] contiene los SHAs y localizadores efectivos.
- Contratos compatibles de `10-projects/Echo/The Lab/V4 — Runtime Integration/` y [[Echo + Echo Forge — Environment Contract]].
