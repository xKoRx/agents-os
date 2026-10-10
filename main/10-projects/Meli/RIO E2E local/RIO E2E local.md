---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Meli]]"
parent:
sprint:
start: "2026-10-08"
due:
progress: 40
repo:
jira:
prs: ["https://github.com/melisource/fury_rio-playmaker/pull/1286", "https://github.com/melisource/fury_rio-controlplane-kafka/pull/86"]
aliases: ["rio-e2e-local", "RIO local E2E", "Ecosistema RIO E2E local"]
tags:
  - kind/project
  - area/meli
  - project/rio-e2e-local
created: "2026-10-08"
updated: "2026-10-09"
slug: rio-e2e-local
entities: ["[[rio-playmaker]]", "[[rio-controlplane-kafka]]", "[[rio-controlplane-clickhouse]]", "[[rio-controlplane-flink]]"]
related: ["[[ads-signals-frontend]]", "[[rio-frontend]]", "[[Kafka — Ambiente local con servicios reales]]", "[[Ambientes locales RIO — Comparativa de implementaciones]]"]
---

# RIO E2E local

> [!info]+ RIO E2E local
> **Área:** [[Meli]] · **Owner:** Rodrigo · **Estado:** active · **Fase:** F1 integrada con develop vigente y publicada en dos PRs; Kafka verde, Playmaker con CodeQL pendiente; aceptación calificada al contexto Docker saludable. VM original offline con limpieza pendiente explícita. ClickHouse backend integrado y reproducido; Flink/front quedan fuera de esta certificación.

## 🎯 Objetivo

Diseñar y luego implementar un entorno local reproducible con cinco aplicaciones reales: Playmaker, un front RIO vigente y los CP de Kafka, ClickHouse y Flink. Front/Postman entran por las APIs Playmaker; triggers y resultados viajan por Kafka mediante producers/consumers embebidos en cada aplicación. Verificar efectos físicos en motores y estado final de Playmaker/CP. Posteriormente ampliar al resto del ecosistema, sin construir hoy un framework general.

Base fijada por el owner: `rio-deployment-trigger-local` y `rio-deployment-result-local`, sin bridge Kafka→HTTP externo ni embebido. Minimizar cambios productivos, conservar contratos y usar Clean, SOLID, KISS y YAGNI para justificar cada pieza nueva. El challenge y el consenso están completos; F1 Playmaker + CP Kafka está implementada y certificada dentro del alcance autorizado. El alcance posterior conserva CH/Flink/front.

## 📊 Estado actual

- **F2 backend vigente — E2E físico del alcance soportado PASS:** MergeTree PROVISION/reconcile/ALTER/DEPROVISION e inactivate, MV PROVISION/reconcile/DEPROVISION, list-warehouse/list-database y negativos/aislamiento con Kafka. Reproducción independiente desde clones exactos/rutas con espacios: cuatro normales×23 y cuatro gaps×3 en cuatro stacks frescos, 104 ejecuciones/0FES. Cleanup certificado y baseline completo preservado. C6 PM UPDATE literal sigue BLOCKED_no_API, CP devuelve FAILED de negocio esperado; gates externos/CodeQL/F4 no certificados por este PASS. Ramas y evidencia vigentes en tabla F2.
- **Historia de correcciones F2, sustituida por el candidato vigente — SPEC/PLAN/TASKS READY y código implementado:** CP N1-T/COV-M2 VERIFY independiente `d218c35a` PASS, CH2705+88/Kafka691+64/0F/E/skips y MAIN/LOCAL>=95L+B con CRCs exactos. PM-N2 VERIFY4bdfde79 PASS: full4862product(2skips heredados)+23local, categorías95 y ambos jars cambian sólo2entries existingdecoder. PM11-L3 FULL156GREEN/whole95 es histórico válido, pero VERIFY05c29a53 cerró **FAIL D01**: señalOS real→handlerInterruptedError→PollSelector lo consume; ps/supervisor siguen vivos. Review67artefactos auditados y80PID/54PGID originales ausentes/root525e7194/0SIG; recovery no subsanaFAIL. **PM11-L4 funcional→PLAN→TASKS READY antesfuente, código implementado** sólo R.run/interrupted ContextVar+carrier privado y tests canónicos; mismo objeto InterruptedError exterior, máscaras/handlers/budgets/drain/helper/Java protegidos. Fresh FULL160RED/107.983s/0F/3E/0skip: único nestedmethod y dos cleanups; nuevo twoPIPE/selector youter PASSparciales. Snapshot5e38e1b7/2951files6179173bytes auditado root+independiente, causa interna NO_AISLADA (sin traceback/returncode supervisor). Recovery original grupos9810/9818/9826 PASS después validación íntegra, no convierte RED enverde. H1 THIRD condicionado acredita snapshot219 despuésACK/application-exit0 yantes stop-request; los dosERROR_PROBE anteriores quedan preservados y la causa retrospectiva FULL160/33306 sigueNO_AISLADA. ALL1062PID/6PGID actuales ausentes, retornoPopen1060/1061limitado; rootfinalizer39754ed240d2a. PM11-L5 funcional→PLAN→TASKS READY antes IMPLEMENT exclusivo: branchfreeze-first, nativepostACKcompletion regression yprependPYTHONPATHtest-only. L5 full161/108.501s/0F/E/skips y wholehelper99.12L/96.96B,R96.85L/95.39B sinexcludes; freeze9db5506f3805files11,502,982B auditroot815a5270+finalizer54415ausente. VERIFY17/PS pendiente: primerD01ERROR_PROBE cerrado38artefactos/roota40efe74/finalizer63786ausente, sinfindingproducto. PM12estático3a7f54f0 confirma gapCHtipo300prevalecesobredefault15; funcional→PLAN→TASKS READY antesIMPLEMENTargvsólo10–30, normal300yJavajarsconservados. PM12full165/107.910s/0F/E/skips, wholeR97.81L/96.41B helper98.60L/96.09B0excludes; freezee08f76493155files12,038,362B y finalizer79072 rootfa5f595c auditados. VERIFYbudget independiente activo,17/PSpendiente ySOURCE_RELEASE=false. Runtimeoffline exclusivoF2/F3offline, runidNone; no Docker/SQL/VM/Gradle de agentes. Contrato23selectors+5caps, normal/gapdosvecesvivos+recreados, Kafka25currentjar, commits/clones/reproducciónfísica ycleanup final pendientes. C1–C5/C6CPFAILED+PMPROVISIONreconcile/A1positivo/X/F1/native52 previos son candidatos/históricos; A1AUTH/gapactionfixes nuevos aúnNO_EJ. C6literalUPDATEAPI PMBLOCKED, CodeScanningPMstartup_failure, externalausentes/F4NO_EJ/original36868NO_CERT yCPUoldermissingidentities preservados. [Matriz vigente](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/4-implementation/VERIFICATION.md).

- **Inicio F2 autorizado 09/10:** discovery/fetch reales completados, PM PR1286 HEAD`c3ecf8c`, CP Kafka PR86 HEAD`90710a5`; bases remotas PM`1ba12db`, CPK`6a91937` y CH`cf17797e`. CH trae82 archivos de delta; snapshot C1/C6/actions requiere ajuste contractual. **Bloqueo histórico previo al steering posterior del owner**, por discrepancia entre raíz canónica SDD exigida`80-agents/skills/` (skills ausentes) y catálogo federado vigente`30-resources/agents/skills/`; resuelto por la instrucción posterior de continuar de inmediato usando catálogo vigente. Ese checkpoint precede a las ramas/SPEC/implementación F2 actuales y no certifica F2. Contexto sano responde vacío, RAM5,77GiB, host8,2GiB libre; revalidar presupuesto/exclusividad antes de runtime. PM Code Reviewer NEUTRAL y Code Scanning conserva startup_failure en dos runs sobre el mismo HEAD. Evidencia y continuación: [[RIO E2E local — F2 discovery y bloqueo SDD]].

- **F3 primera entrega HTTP→CP→Flink Docker, BLOCKED/no entregada:** Todos los flujos antesPM. Commitsmainfix `4fc9fe12` ylocal/docs `eb65824a` enfeature/rio-e2e-local-flink/base579a6ce; hooks realesALLPASS. Sourcefull1912producto+403local/0F/E/skips,50critical≥95L+B/IDs,jars49a6e794/f51abc0d/major69/aislamientoPASS. VERIFY27(8terminal13SQL6ACK)/0findings,522inputs665outputsintactos,12JVMreaped/10puertosprivadosfree,Java devuelto root; source≠E2E. HTTP físicoALL/repeats/recreate/restart/cleanclone NO_EJ;JARcache-hitviable sinimplementación,NexusZIP/Python/params/CheckToCreate pendientes. GCP fuentes reales CC45a5825e/SQL6ad9532+a9cf34d/SDKaba06861recuperadas: PigDONE/controlID≠FlinkjobRUNNING, JARvivo/driver5.0.0 sinprovenance BLOCKED. Módulo externo/runner reusa toolkitF2actualCP-only/NCP, CP Kafkaúnicoownerbroker/red; noframeworknuevo. F2runtimeexclusivo/nohandoff,disco808488960Bsinpresupuestoclon+reserva; VMoriginal/ledger36868NO_CERTintocados. SecurityMCP/AOCausentesBLOCKED/CodeQLPMFAILpublishedpreservado. [Informe actual](/private/tmp/rio-controlplane-flink-rio-e2e-local/meli/features/20261009-rio-e2e-local-flink/4-implementation/DD29_DD31_VERIFICATION.md); continuidad [[F3 Flink — Discovery y gates bloqueados]]. NoPR/push/merge/deploy/cierreAGENTSOS.

- **Steering de review 09/10:** owner pide iterar con challenge independiente y permite contra-challengear propuestas no aplicables. Se aceptan Spring Kafka CP, fallback de cluster, topología en orquestador, transporte PM compartido, separar K6 y dividir harness. Se mantienen bytes/DLT y ownership/drenaje por defectos reproducidos; no se construye aún framework de N CP. Registro fuente: [[2026-10-09-claude-code-claude-opus-5-5-rio-e2e-local-f1-review]]. Cambios aceptados implementados y recertificados con nuevas fuentes/artefactos; las seis suites anteriores quedan como historia de sus commits.
- **Steering 09/10:** owner autoriza implementar hasta funcionar Playmaker + CP Kafka siguiendo el diseño consensuado; descarta el camino HTTP anterior. Fetch/ramas/recursos locales quedan autorizados por este pedido. Fases CH/Flink/front permanecen posteriores, sin reducir su criterio final.
- **Precisión K2 verificada en código vigente:** PM no emite UPDATE; redeploy usa PROVISION y el CP reconcilia particiones/config. K2 verificó payload PROVISION real + efecto físico actualizado; UPDATE literal se conserva en standalone25. Sin cambio productivo para forzar el diseño histórico.
- **Ejecución F1:** bases verificadas por fetch y pull fast-forward: PM `44c290591a104e1471f43f132007fb6d13169684`, CPK `6a91937c0664d83f907dec222af8a96b4042c6ae`. Checkouts aislados permanentes fuera del vault, bajo `fuentes`: `rio-playmaker-rio-e2e-local` y `rio-controlplane-kafka-rio-e2e-local`. Se trasladaron con Git desde las rutas temporales sin modificar fuentes ni perder evidencia. Ramas `feature/rio-e2e-local-deprovision-fix` (PM dependencia), `feature/rio-e2e-local-kafka` (integración en ambos repos). SPEC funcional/técnica/tareas READY antes de código por repo en `meli/features/20261009-rio-e2e-local/`; tareas y verificación final completadas. Originales/HTTP intactos. Docker `colima-rio` estuvo disponible y vacío al iniciar; luego quedó offline por host ENOSPC/VM I/O. La recertificación nueva usa explícitamente el contexto existente y vacío `colima-rio-kafka-e2e-01a0f8e0`.

- **Certificación anterior de F1 (fuentes 2f4a0a2 / 581e234):** producers/consumers Kafka embebidos para deployments y actions, broker único CP, runner propio y APIs/handlers productivos. Fix DEPROVISION separado `b6030980501139723338390a70458f111e5d2a7f`, 287 focalizadas PASS. PM: 4809 pruebas de regresión, cero fallos/errores y dos skips ya presentes en baseline; 23 locales PASS, launcher 16/16 PASS; cobertura crítica líneas 97.84% y branches 96.23%. CP: 691 productivas/52 locales/25 standalone PASS, cero skips; cobertura líneas 99.61% y branches 95.45%. Aislamiento de ambos jars productivos PASS. Contrato obligatorio PM completo PASS: 12 selectors, tres capacidades L0 y la L1 Kafka real. Seis suites físicas 12/12 sin fallos/errores/skips en tres stacks: repetición viva `6c6ee9ea8f1a`, recreación vacía `3fbc16fafc45` y clones limpios independientes `91292b80f545`. Cada par fue serial; restart CP real, offsets y efectos físicos acreditados; limpieza certificada y recursos ajenos preservados.
- **Recertificación de la simplificación anterior a publicación (histórica para PM):** fuentes PM `90dfef733dc56138ccacdebe915c0e29ff81f4ac` / CP `b0d4587f0e0fc90180ddb5ceb05bdd96c3147dc8`; entregas Markdown PM `ccc43d0d5c83ec2d144d022db011ec98ea9ec038` / CP `90710a590794e8a35b39f420013b24e2367ea4c1`. CP listener Spring Kafka, readiness real, sin mapa artificial; topología del ecosistema en el runner; PM transporte compartido; once casos normales y K6 explícito, fixtures por método. PM 4810 regresión, cero fallos/errores y dos skips heredados,23 locales,16 focalizadas y24 launcher PASS; cobertura235/241 líneas97.5104%,94/98 branches95.9184%. CP691 productivas,50 locales,25 standalone PASS;164/164 líneas100%,49/50 branches98%. Aislamiento productivo y versiones locales/productivas PASS, IDs JaCoCo verificados independientemente. Contrato obligatorio12 selectors+3 L0 completados; L1 reanudada PASS en run`f4ec56bb0c47` con2×11 normal+2×1 gap. Otro agente reconstruyó jars idénticos y reprodujo2×11 con presupuestos productivos (run`d566b230fa3b`) y2×1 en stack nuevo15s (run`12e65ac4a701`), cwd arbitrario y paths con espacios. Ocho suites nuevas, cero fallos/errores/skips; no contar las seis históricas como evidencia actual.
- **Calificación operacional:** los stacks nuevos dejan baseline0 containers/0 volumes, mismas tres redes por ID e imágenes previas, grupos/estado propios ausentes y puertos reutilizables tras espera acotada. `colima-rio` original permanece offline: recuperación stop/start/force-stop fue una desviación explícita de la regla de no operar la VM; sin delete/prune. Run`36868d2dbe3d` tiene limpieza **NO CERTIFICADA**; podrían quedar4 containers/1 volume/2 redes en su disco inaccesible. Grupo PM del host ausente; ledger completo privado preservado reversiblemente en `fuentes + .rio-e2e-interrupted-state/36868d2dbe3d`, fuera de Git y Gradle clean. No mezclar ese estado con el contexto saludable ni declarar la VM reparada.
- **Veredicto acordado:** viable para Playmaker, CP Kafka y CP ClickHouse con cambio productivo cero o mínimo. Flink físico BLOCKED hasta demostrar el seam mínimo, pero se mantiene en el criterio final. La certificación final exige efectos reales en Kafka, ClickHouse y Flink más journeys browser, incluidas las actions que esos journeys usan.
- **Front elegido:** [[ads-signals-frontend]] (`origin/develop`). [[rio-frontend]] queda fuera: listado fijado a `environment = 'legacy'`, URL de Playmaker hardcodeada y modelo antiguo de deployments.
- **Snapshot de discovery 09/10 (`ls-remote`, anterior a publicación):** PM develop44c2905 y CP Kafka develop6a91937 sin cambios; CH ac4662a, Flink 579a6ce, ads-signals-frontend 01e19bc y rio-frontend d977028 avanzaron y no se leyeron sin fetch. `develop` local ≠ `origin/develop` en PM, CP Kafka y front.
- **Pendiente posterior a F1:** releer deltas CH/Flink/front, demostrar seam físico Flink e integrar las fases restantes. La revisión posterior quedó implementada y aceptada por otro agente para F1 en el contexto saludable, con deuda operacional de la VM original explícita. La inactivación está cubierta por regresiones transaccionales; el journey browser de inactivate pertenece a la fase de front. El proyecto raíz sigue activo porque conserva su alcance final de cinco apps.
- Repos originales con cambios ajenos intactos tras el discovery (conteos de status idénticos a los observados el 08/10).

### Entrega PR vigente — 09/10

| Repo | PR / HEAD publicado | Fuente y base verificadas | Gates |
|---|---|---|---|
| Playmaker | [#1286](https://github.com/melisource/fury_rio-playmaker/pull/1286), ready; `c3ecf8cb78bf5f4a8df093e1a1a40488d6d91a7f` | Fuente `642aa53ab929fa89394a4421051a7567b0585651`; merge de develop `1ba12db957576db04eca686c16e6afac7564edd1`. Las tres notas posteriores sólo cambian Markdown. | Local PASS: 4818/0/0/2 skips heredados,23 locales,24 launcher; crítica235/241 líneas97.5104%,94/98 ramas95.9184%; aislamiento PASS. CI6144 sobre HEAD actual PASS, junto con cobertura/dependencias/static-analyzer/workflow. Code Reviewer en curso al registrar cierre. CodeQL37975496615 startup_failure sin jobs/checkruns. |
| CP Kafka | [#86](https://github.com/melisource/fury_rio-controlplane-kafka/pull/86), ready; `90710a590794e8a35b39f420013b24e2367ea4c1` | Fuente `b0d4587f0e0fc90180ddb5ceb05bdd96c3147dc8`; base develop `6a91937c0664d83f907dec222af8a96b4042c6ae`; sin cambios productivos. | CI551, cobertura, dependencias, static-analyzer, workflow y CodeQL PASS; Code Reviewer NEUTRAL, empty SARIF SKIPPED. Local691/50/25, cero fallos/errores/skips; crítica100% líneas/98% ramas; aislamiento PASS. |

Fetch para publicar detectó nuevos guards PM de actions/history: las15 superficies upstream se conservaron byte por byte, sin bypass. El contrato V2 completo pasó22 selectors+3 L0+L1 física, run`44941be9e81d`:2×11 normal y2×1 gap. Nueva reproducción independiente en clones limpios con paths con espacios: normal productivo`810238a329de`2×11 y gap nuevo15s`9444d48eba3d`2×1, todos cero fallos/errores/skips; CP restart real, efecto físico, offsets, poison/DLT y cleanup certificado. Puertos reutilizables a53.81/53.57s dentro del límite60s; no afirmar disponibilidad inmediata. Fuente/jars y405 hashes de evidencia completada verificados. CP product jar difiere con compiler JDK21/25 target21; ambas variantes se documentan, no se afirma igualdad entre compiladores.

**Límite de entrega:** no están ambos PRs verdes: CodeQL PM falla al iniciar, también observado en otras ramas; causa no demostrada. Se propuso cambiar sólo `file-limit` de ubuntu-latest a los labels corporativos `[self-hosted, linux, X64, websec]`. El patch de una línea está en `/private/tmp/rio-codeql-corporate-runners.patch`, revisado por otro agente sin aplicarlo. Auto-review rechazó el cambio por alterar entorno/límite de seguridad; aprobación explícita owner pendiente. No modificar runner/permisos/umbrales ni ocultar el check sin esa aprobación; una aprobación del patch tampoco demuestra que arregle la causa. Reprobar CodeQL sobre el HEAD exacto y conservar un resultado real.

Descripciones canónicas: [[Descripción PR — rio-playmaker]] y [[Descripción PR — rio-controlplane-kafka]]. Prompts listos: [[Prompt maestro — CP ClickHouse E2E local]] y [[Prompt maestro — CP Flink E2E local]]. F2/F3 no se ejecutaron por el pedido de redactarlos. Feedback: [[2026-10-09-rio-e2e-local-delivery-session-feedback]]. Registro de corrida: [[2026-10-09-codex-unknown-rio-e2e-local-pr-publication]]. Aprendizaje: [[kafka-local-spring-retry-ack-evidence|Kafka local — Reintentos y ACK se verifican en el container]].

### Continuidad al reanudar

1. Leer esta nota/diseño por delta, PRs/checks y heads vigentes; no usar90df ni44c como head/base actual de PM. Reutilizar checkouts permanentes `fuentes/rio-playmaker-rio-e2e-local` y `fuentes/rio-controlplane-kafka-rio-e2e-local`, rama`feature/rio-e2e-local-kafka`; guía PM`local/RIO_E2E.md`, SPECs/VERIFICATION en`meli/features/20261009-rio-e2e-local/`. Review actual PM`4-implementation/PR_INTEGRATION_REVIEW.md` y auth`PM_UPSTREAM_AUTH_MERGE_REVIEW.md`; SIMPLIFICATION_REVIEW e INDEPENDENT_REVIEW son históricos.
2. CodeQL PM conserva diagnóstico/aprobación pendiente; CI principal/local no sustituyen ese gate remoto. El owner autorizó iniciar F2 en una sesión separada: discovery/fetch actual recuperado y autoridad de catálogo vigente resuelta por la instrucción posterior del owner; SPEC/PLAN/TASKS READY por repo y IMPLEMENT en curso. El checkpoint [[RIO E2E local — F2 discovery y bloqueo SDD]] es antecedente histórico; continuar desde los artefactos F2 sin repetir bootstrap. Generalizar el mismo runner a N CPs con configuración pequeña y acreditar Kafka+CH; luego Flink con seam real submit/monitor/cancel. No duplicar runners, anticipar un framework general ni ejecutar ambas integraciones sobre el mismo runtime. Sin merge/deploy implícitos.
3. Preservar originales sucios y worktrees HTTP/históricos. Fix DEPROVISION`b6030980501139723338390a70458f111e5d2a7f` conserva rama propia y ya integra el PR PM: no tercer PR ni cherry-pick duplicado. Reinspeccionar antes de nueva extracción; no reset/clean/merge de cambios ajenos.
4. Runtime sano explícito`DOCKER_CONTEXT=colima-rio-kafka-e2e-01a0f8e0`; baseline0 containers/0 volumes, mismas3 redes y24 imágenes. Una autoridad de runtime, suites seriales y cleanup sólo propio. Run original offline36868 sigue **NO CERTIFICADO**, ledger privado en`/Users/rjara/fuentes/.rio-e2e-interrupted-state/36868d2dbe3d`: no leer/exportar credenciales, no operar VM/prune ni mezclarlo con contexto sano. Recuperar esa deuda sólo con alcance explícito al reparar el perfil original.
5. Conservar actions CH list-warehouse/list-database, física CH/Flink y journeys browser en aceptación final. Flink físico sigue BLOCKED hasta demostrar su seam; front F4 no se certifica por backend. Macroproyecto active40; el cierre de sesión no termina las fases pendientes.

Sesión AGENTS OS cerrada el09/10 por pedido explícito, con feedback, corrida y continuidad persistidos. Entrega parcial del verde remoto: CodeQL PM y aprobación del patch siguen pendientes; no se recibió autorización ni se aplicó. Macroproyecto active40, sin merge/deploy. Al reanudar recuperar este delta, no repetir bootstrap en warm ni declarar cumplido el gate pendiente.

## 🧱 Entrega de desarrollo

Entrega multirrepo por fases. F1 tiene ramas/bases y SPEC funcional→técnica→tareas antes de código; las otras aplicaciones conservan su estado de discovery. No trasladar cambios sucios.

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] · fury_rio-playmaker | feature/rio-e2e-local-kafka, apilada sobre feature/rio-e2e-local-deprovision-fix | 44c290591a104e1471f43f132007fb6d13169684; dependencia b603098 | repo + meli/features/20261009-rio-e2e-local/1-functional/spec.md | repo + meli/features/20261009-rio-e2e-local/2-technical/spec.md | fuente642aa53; HEADc3ecf8c; PR1286 ready:4818/23/24 PASS y2 skips heredados; matriz nueva root+independiente; CI6144 PASS y CodeQLstartup_failure; contexto sano y deuda original offline |
| [[ads-signals-frontend]] · fury_ads-signals-frontend | Integración no creada | origin/develop local a3f82abd8a4756d750b8d3ec86e9065df1fec9a4; remoto 01e19bc sin leer | Journeys B1–B3 en el diseño revisado | Sin código si D4 se resuelve por seed | BLOCKED (D4) |
| [[rio-controlplane-kafka]] · fury_rio-controlplane-kafka | feature/rio-e2e-local-kafka | 6a91937c0664d83f907dec222af8a96b4042c6ae | repo + meli/features/20261009-rio-e2e-local/1-functional/spec.md | repo + meli/features/20261009-rio-e2e-local/2-technical/spec.md | fuenteb0d4587; documental90710a5:691/50/25 PASS; Spring Kafka local; normal11/gap1 repetidas root+independiente; cero cambios src/main |
| [[rio-controlplane-clickhouse]] · fury_rio-controlplane-clickhouse | feature/rio-e2e-local-clickhouse, worktreeaislado | fetcheddevelop cf17797ef9bc1eb9b9bdb3329e6c70bfc8231386; originaldirty intacto | SPEC F2 C1–C6/A1/X1–X4 abajo | SharedintakeMVC mínimo/Kafkaembebido/motor25.8.33.6/SQLcliente físico | E2E backend soportado y cleanup PASS; C6 API PM/capabilities externas BLOCKED, F4 NO_EJECUTADO |
| [[rio-controlplane-flink]] · fury_rio-controlplane-flink | Integración no creada | origin/develop local7c645ea92f86650744a3c5ee1bad0012633ef0e9;1 cambio ajeno | Escenarios a descubrir | Cloud Controller/runtime a verificar | Seam local por demostrar |

### Entregables F2 ClickHouse vigentes

SPEC consolidada de revisión: [[RIO E2E local — SPEC F2 ClickHouse]]. Incluye referencias recuperadas, contrato por caso, PLAN técnico y TASKS READY por repo; las SPEC enlazadas en la tabla conservan la autoridad y deltas de implementación.

SDD funcional → técnica/PLAN → TASKS READY precedió la implementación en los tres repos. Estas SPEC concretas son la autoridad del alcance F2; el borrador posterior corresponde al macroproyecto de cinco apps.

| Repo | Rama / candidato | SPEC funcional | SPEC técnica y PLAN | TASKS |
|---|---|---|---|---|
| PM | feature/rio-e2e-local-clickhouse · HEADf0cac94f (fuente c5cc53e0; E2E/cleanup PASS) | [spec](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md) | [plan](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md) | [ready](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |
| ClickHouse | feature/rio-e2e-local-clickhouse · HEAD61b63808 (fuente 8ab2961d; E2E/cleanup PASS) | [spec](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md) | [plan](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md) | [ready](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |
| Kafka | feature/rio-e2e-local-clickhouse-regression · HEADf8fe7671 (fuente 28428ff4; F1+F2/standalone PASS) | [spec](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/1-functional/spec.md) | [plan](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/2-technical/spec.md) | [ready](/Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/3-tasks/tasks.md) |

Gates root: contrato canónico, ocho matrices físicas, fault9/native52/critical7 y Kafka standalone PASS; collectors privados con FAIL preservados y reconciliaciones independientes. Cleanup root y del primer clone bootstrap fallido conservan baseline exacto. Reproducción limpia660431b713e7: FAIL unhealthy antes de tests, causa NO_AISLADA. Corrección mínima8ab2961d incluye init público en imagen del motor (dos archivos CH, CPstage intacto); VERIFY estático PASS. Reproducción independiente del nuevo Compose PASS: cuatro normales y cuatro gaps en cuatro stacks nuevos, 104 ejecuciones exactas/0FES. Manifest ebb133f2 conserva3136files; matrices independientes56993045, motores/cleanup45fbb366, baseline actualfullmetadata6430d371 y externalsb151d252 PASS. 2808PID/1116PGID originales+observadores ausentes inclZ/0SIG;14IDs propios retirados/23rmi exactos,24baselineRootFS/3redes intactos,0containersvolumes/puertos libres/statecredsausentes. SOURCE_RELEASE es aditivo, resultado sellado intacto. Commits finales f0cac94f/61b63808/f8fe7671 sólo ocho archivos existentes; clones exactos limpios y fuentes/jars invariantes. [Reproducir](/Users/rjara/fuentes/rio-controlplane-clickhouse-rio-e2e-local/local/RIO_E2E.md); [matriz actual](/Users/rjara/fuentes/rio-playmaker-rio-e2e-clickhouse/meli/features/20261009-rio-e2e-local-clickhouse/4-implementation/VERIFICATION.md). C6 PM UPDATE literal BLOCKED_no_API, capabilities externas ausentes y Code Scanning remoto startup_failure conservados. No PR/merge/deploy ni certificación browser implícitos.

### SPEC funcional — borrador

1. Levantar simultáneamente las cinco aplicaciones y los motores/dependencias locales necesarios. Cinco aplicaciones no significa cinco contenedores: Kafka, MySQL, ClickHouse y runtime Flink son infraestructura adicional.
2. Requests desde APIs Playmaker y journeys del front elegido, con triggers SDK reales, procesamiento CP real y resultados reales. No fabricar COMPLETED ni sustituir provisioning/SQL/jobs/lifecycle por fixtures.
3. Matriz por CP/caso: endpoint vigente, tipo de componente, operación/action soportada, trigger, resultado CP, estado PM, efecto físico y fronteras sustituidas. No asumir que los tres CP soportan las mismas operaciones.
4. Errores iniciales/propagados, duplicados/replays/orden y deadlines según contratos. Separar PASS/FAIL/BLOCKED/NO_EJECUTADO y E2E backend de browser. HTTP200 y ACK Kafka son recepción, no estado terminal.
5. Comandos pequeños de arranque/pruebas/limpieza, rutas arbitrarias/con espacios, recursos propios identificados y aislamiento. Repetir dos veces sobre ambiente vivo, recrear vacío y reproducir desde clones limpios. No suites concurrentes contra el mismo ambiente.

### SPEC técnica — estado objetivo

Estado objetivo, contratos, inventario por repo, secuencias ACK/error/replay, matriz E2E y decisiones abiertas en [[RIO E2E local — Diseño revisado]]. Resumen:

- Un broker, dueño Compose CP Kafka, red `rio-local`; Playmaker y front en host (PM contra `127.0.0.1:39092` por `LocalKafkaBootstrapGuard`), CPs/ClickHouse/MySQL en la VM. Puertos: PM39080, CP Kafka39081, CP ClickHouse39082, CP Flink39083, broker39092, ClickHouse HTTP39123, MySQL33306, front8443.
- Tópicos `rio-deployment-trigger-local` y `rio-deployment-result-local`, una partición, key `deployment_id`, payload SDK crudo; un group por CP; DLT por CP con la política de reintento ya usada por PM; observer con `assign()` sin group.
- Entrada CP: adapter local A que invoca el handler del controller sólo si demuestra paridad HTTP↔Kafka, incluidos binding, validación, filtros y errores; B con refactor estructural mínimo donde A no los conserve limpiamente. Commit tras aceptación; no equivale a operación terminada. Salida CP: `BigQueueClient` Kafka bajo el publisher productivo.
- Se conservan contratos, guards, idempotencia y gaps productivos (publisher CP Kafka, GCP PEEK). Sin bridge, librería común ni broker de PM. Runtime Flink, seam y dimensionamiento por demostrar; Flink físico permanece en el criterio final.

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

No se crearon subproyectos persistentes de ejecución delegada. SDD delegó implementación y revisión independiente de F1 con bases/SPEC antes de código; la entrega y continuidad permanecen en este proyecto.

## ✅ Tareas

- [x] Publicar dos PRs con descripciones técnicas y nueva recertificación de auth upstream #owner/agent #type/dev #area/meli
- [ ] Resolver CodeQL Playmaker y acreditar ambos PRs verdes sin bypass #owner/agent #type/test #area/meli
- [x] Preparar dos prompts maestros alineados con F1 y decisión N CPs #owner/agent #type/dev #area/meli

- [x] Simplificar F1 según review Claude, documentar contra-challenges y verificar por otro agente #owner/agent #type/dev #area/meli
- [x] Recertificar fuentes simplificadas: regresiones/cobertura, normal con presupuesto productivo, matriz completa repetida y reproducción limpia independiente #owner/agent #type/test #area/meli

- [x] Implementar F1 Playmaker + CP Kafka con transporte Kafka embebido; conservar originales y extraer fix DEPROVISION en rama propia #owner/agent #type/dev #area/meli
- [x] Verificar K1–K6/X2–X4/A2, standalone25, regresiones y limpieza propia; repetir ambiente vivo y recreación vacía #owner/agent #type/test #area/meli
- [x] Verificación independiente y corrección/gate final de F1 #owner/agent #type/test #area/meli

- [x] Ejecutar [[Prompt — Challenge del diseño RIO E2E local]] y revisar findings #owner/me #type/research #area/meli
- [x] Acordar D1–D6 de [[RIO E2E local — Diseño revisado]] #owner/me #type/dev #area/meli
- [ ] Autorizar fetch y releer deltas remotos de CH, Flink y front #owner/me #type/research #area/meli
- [ ] Spike de sólo lectura del seam físico mínimo de Flink #owner/me #type/research #area/meli
- [x] Preparar rama propia del fix DEPROVISION como dependencia explícita de la integración #owner/me #type/dev #area/meli
- [x] Aprobar diseño revisado y registrar ramas/bases/SPEC/tareas por repo F1 #owner/me #type/dev #area/meli

```dataviewjs

const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📆 Bitácora

- **2026-10-09 — publicación solicitada:** PR Kafka86 verde y PM1286 publicado; fuente PM integrada con auth vigente, gates y nueva reproducción física independiente PASS. CodeQL PMstartup_failure pendiente de diagnóstico/aprobación de patch acotado. Dos prompts y feedback/continuidad persistidos; registro [[2026-10-09-codex-unknown-rio-e2e-local-pr-publication]].

- **2026-10-09 — iteración posterior:** review Claude challengeada, simplificación y regresiones permanentes implementadas; fuentes90df/b0 y nueva recertificación root+independiente completa en contexto saludable. Normal11/gap1 separadas, cada una cuatro corridas nuevas PASS; jars reconstruidos idénticos, cobertura independiente y limpieza de nuevos stacks PASS. VM original offline/cleanup36868 no certificado y ledger privado preservado explícitamente. Sesión y macroproyecto siguen activos. [[2026-10-09-rio-e2e-local-f1-implementation]] y [[2026-10-09-codex-unknown-rio-e2e-local-f1-simplification]].

- **2026-10-09** — F1 implementada y certificada siguiendo el diseño: transporte Kafka embebido reemplaza el camino HTTP; dependencia DEPROVISION separada, originales preservados. Gates productivos/locales/contrato y standalone25 PASS; seis suites físicas 12/12 en repetición, recreación vacía y reproducción independiente. Findings de ownership/interrupción/bytes/fixture corregidos y promovidos a regresiones. Fuentes PM 2f4a0a2 / CP 581e234; entregas Markdown PM c03b950 / CP 6832c70. Jars coinciden por hash; limpieza certificada sin afectar recursos ajenos ni filtrar credenciales. Checkouts permanentes en fuentes; sesión/proyecto activos para fases posteriores. [[2026-10-09-rio-e2e-local-f1-implementation]] y [[2026-10-09-codex-unknown-rio-e2e-local-f1]].

- **2026-10-09** — Review cruzada de F1 por Claude Code (Opus 5.5) y refactor de simplificación de Codex (PM `ccc43d0d5`, CPK `90710a5`): listener CP sobre Spring Kafka, `LocalClusterMapping` eliminado, tópicos desde el runner, transporte PM unificado, suite E2E dividida y caso K6 como `test-gap`. Claude aprueba F1. Para F4 (front) quedan pendientes: token `local-e2e`, team del fixture, entity-service y el payload `aws-msk-topic` del front. [[2026-10-09-claude-code-claude-opus-5-5-rio-e2e-local-f1-review]].
- **2026-10-08** — Proyecto y prompt creados desde templates canónicos. Identidad local de repos leída sin fetch. Challenge e implementación pendientes. [[2026-10-08-rio-e2e-local-created]].
- **2026-10-09** — Challenge ejecutado con discovery de sólo lectura sobre refs git de los cinco repos; diseño revisado entregado, front elegido y seis decisiones abiertas. Sin código, fetch, Docker ni VM. [[2026-10-09-rio-e2e-local-design-challenge]].
- **2026-10-09** — Segunda revisión cruzada aceptada: alcance final completo (Flink físico y journeys con actions), A condicionada a demostrar paridad por pruebas, timeout como detección y readiness explícita. Mismo change log.
- **2026-10-09** — Sesión cerrada por pedido explícito. Continuidad guardada en esta nota, feedback propio en [[2026-10-09-rio-e2e-local-consenso-session-feedback]] y revisión atribuible en [[2026-10-09-codex-unknown-rio-e2e-local-design-review]]. [[2026-10-09-rio-e2e-local-session-close]].

## 🧭 Decisiones

- Owner fija cinco apps iniciales y crecimiento posterior. Producers/consumers Kafka sin bridge es requisito; producción se toca sólo ante necesidad demostrada y mediante cambio mínimo que conserve contratos.
- Front del alcance: [[ads-signals-frontend]]; [[rio-frontend]] fuera por estar acotado a ambientes legacy.
- D1–D6 acordadas en [[RIO E2E local — Diseño revisado]]: A condicionada a paridad HTTP↔Kafka (B donde no alcance), Flink físico en el criterio final, actions de los journeys dentro del alcance, fixtures mínimos de referencia, extracción selectiva desde LOCAL-HTTP-2 y versión ClickHouse fijada por pruebas físicas. F1 autorizada por el pedido actual del owner; CH/Flink/front permanecen posteriores.
- Iniciativa raíz independiente de [[Kafka — Ambiente local con servicios reales]], que conserva evidencias y ramas específicas. El cierre anterior del 09/10 se conserva como antecedente; sesión actual activa y F1 certificada; fases posteriores conservadas.

- **2026-10-09 — Owner tras review cruzada Claude↔Codex de F1:** prioridad única = todo funcionando local para E2E desde el front, KISS/YAGNI y sin tocar código productivo en lo posible. La versión de librerías en classpath locales (p. ej. `kafka-clients` 4.2.1 del CP vs 3.9.2 productivo) es irrelevante mientras levante. Regla F2: el runner se generaliza a N CPs al sumar ClickHouse, no se copia.

## 🔗 Docs / Links

- [[RIO E2E local — Diseño revisado]] — estado objetivo, contratos, inventario, matriz E2E y decisiones abiertas.
- [[Prompt — Challenge del diseño RIO E2E local]] — prompt autocontenido, sólo diseño.
- [[Kafka — Ambiente local con servicios reales]] — antecedente técnico/evidencia de alcance anterior.
- [[Ambientes locales RIO — Comparativa de implementaciones]] — investigación histórica, no contratos vigentes sin reverificar.
- [[rio-playmaker]], [[ads-signals-frontend]], [[rio-frontend]], [[rio-controlplane-kafka]], [[rio-controlplane-clickhouse]], [[rio-controlplane-flink]].

## 💡 Ideas

### Backlog de ideas

- Incorporar otros CP/materializer/servicios después de demostrar el patrón con estas cinco apps; no construir ahora un framework E2E general.

### Motivos / principios

- Clean/SOLID para separar transporte y negocio; KISS para operación local; YAGNI para limitar dependencias/abstracciones. Cada pieza nueva debe resolver una necesidad comprobada.

### Memoria pública / interna

- **Memoria pública:** contratos y decisiones verificadas enlazados desde esta nota.
- **Memoria interna:** journal de creation/discovery, sin duplicar el estado operativo en memorias generales.
- **Motivo:** separar propuesta vigente, evidencia histórica e implementación futura.
