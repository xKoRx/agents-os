---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
progress: 0
area: "[[Meli]]"
parent:
sprint:
start: "2026-10-21"
due:
repo:
jira:
prs: ["https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/362", "https://github.com/melisource/fury_rio-playmaker/pull/1328", "https://github.com/melisource/fury_ads-signals-frontend/pull/816"]
aliases: []
tags:
  - kind/project
  - area/meli
created: "2026-10-21"
updated: "2026-10-22"
---

# Import de Refreshable Materialized Views externas

## 🎯 Objetivo

Entregar SIG-700 con un PR draft por repo, tres shots independientes y E2E físico conjunto. Rodrigo Jara cierra los gates; el manager solo prepara evidencia para revisión. Se completaron los nueve shots de código; las continuaciones por manifest y por E2E permanecieron dentro de sus shots originales. No hubo Shot 4 ni release productiva.

## 📊 Estado actual

**BLOCKED.** Hay tres drafts publicados, pero no se acredita el E2E completo ni se aceptan gates rojos. Bloqueos: typecheck heredado del front, capacidades locales KVS/CKAAS/KMS ausentes para el import y preservación del baseline de volúmenes todavía no acreditada. La auditoría terminó UNVERIFIED y Docker/VM siguen sin nuevas mutaciones. Zord completó 8/8 tras autorización explícita; FRONT-ZORD-1 fue corregido y rechecado independientemente, sin aceptar gates del owner.

Todos los Shot 1/2/3 y el worker físico usaron el modelo exacto **gpt-6-sol, LOCAL**, con contextos nuevos por shot y agent-runs separados. El auditor de limpieza independiente también usa gpt-6-sol LOCAL. El identificador exacto del modelo del manager no fue expuesto y se registra como unknown, sin inferirlo.

## 🧱 Entrega de desarrollo

| Repo | Rama / base real | SHA final | SPEC | Draft / diffstat real verificado por manager |
|---|---|---|---|---|
| [[rio-controlplane-clickhouse]] | feature/refreshable-view-import ← origin/develop@4b16f7c2721e0e3c30cd5e020f627cad78040d7f | b23862238960773fa965681e95180ad44754ae3c | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700), [SIG-701](https://spellbook.adminml.com/projects/SIG/specs/SIG-701) | [#362](https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/362), 9 archivos +179/-15, presupuesto10 |
| [[rio-playmaker]] | feature/refreshable-view-import ← origin/develop@f1a4b246d74e679dd81718513b50b56818bd1deb | 74bcdde08a1dce9ec3000db1588ad464f439d5c3 | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700), [SIG-702](https://spellbook.adminml.com/projects/SIG/specs/SIG-702) | [#1328](https://github.com/melisource/fury_rio-playmaker/pull/1328), 5 archivos +92/-28, excepción owner5 |
| [[ads-signals-frontend]] | feature/refreshable-view-import ← origin/develop@9a70723c96ebd7f7a8e6564988ed4f8e630ea58a | 027d9f10c83b1962ea463c905f17d2de58b291bf (candidato, no certificación completa) | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700), [SIG-703](https://spellbook.adminml.com/projects/SIG/specs/SIG-703) | [#816](https://github.com/melisource/fury_ads-signals-frontend/pull/816), 20 archivos +1309/-276, presupuesto20 |

El manager contrastó HEAD, merge-base, git diff --stat contra origin/develop y head/draft/base remotos de cada PR. CP conserva tres derivados graphify-out modificados por el hook de checkout fuera de los commits; PM/front están limpios. No checkout, stash, reset ni commit en originales. Fetch y worktree add se ejecutaron una vez por repo según autorización.

## Gates locales y descripción de PR

| Repo | Gate final observado | Coverage informado | Recurso vault |
|---|---|---|---|
| CP | ./gradlew test jacocoTestReport PASS: 3949 tests, 0 fallas/errores, 1 skip; cinco probes críticos PASS y Zord completo | 26/26 líneas ejecutables nuevas | [[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — rio-controlplane-clickhouse]] |
| Playmaker | ./gradlew test jacocoTestReport PASS: 4933 tests, 0 fallas/errores, 2 skips; contrato testing y 236 focalizados +4 probes PASS | No Java productivo nuevo; ratio delta no aplica | [[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — rio-playmaker]] |
| Front | npm run typecheck exit2; npm run lint PASS0errores/385warnings; npm run test:unit PASS502suites/11710tests; diff check PASS | 142/144 sentencias cambiadas, 98,61% | [[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — ads-signals-frontend]] |

En 027d9f10c, typecheck final conserva 123 diagnósticos heredados con los mismos códigos y ubicaciones que origin/develop, sin errores nuevos. Un texto abreviado cambia de «31 more» a «32 more» por la propiedad opcional del adapter; ya no se afirma igualdad literal del log. Incluye CanvasControls.spec.tsx(325,7): TS2345, incompatibilidad de MiniMapProps. La deuda es heredada, pero el gate sigue rojo; no se autorizó waiver ni cambios fuera de alcance para ocultarla. Los hilos existentes se respondieron con el SHA vigente: CP/PM ninguno; front único hilo CodeQL actualizado en [respuesta final](https://github.com/melisource/fury_ads-signals-frontend/pull/816#discussion_r4347520487).

## Triage y ciclo de shots

### CP

Shot1 e689f6af43bab9c27136ee51575aee93883bd8dd: candidato8archivos +161/-10. Shot2 independiente encontró RF17 roto pese a tests y coverage verdes. Shot3 b23862238960773fa965681e95180ad44754ae3c corrigió y dejó9archivos.

| ID | Hallazgo | Decisión / resultado |
|---|---|---|
| CP-1 HIGH | El guard buscaba parameters.external_reference; mapper real produce externalReference plano. Probe real llamó CREATE para vista externa ausente. | Aceptado y corregido; regresión permanente trigger→mapper→comando. D físico confirmó ausencia de recreación. |
| CP-2 LOW | markImportedByRio quedó sin callers productivos. | Aceptado y eliminado sin retirar helpers utilizados. |
| CP-R1 HIGH | Falla posterior al marker puede perder outputs y el siguiente PROVISION no recuperar credenciales. | Rechazado como corrección de esta entrega: secuencia heredada de SIG475 y publisher/persistencia no modificados; recuperación durable requiere lifecycle/storage fuera de técnica congelada. Riesgo real conservado para owner, no declarado resuelto ni aceptado. |
| CP-R2 | Exigir external_reference para todo import. | Rechazado: contradice rollout explícito para componentes manuales sin flag y paridad congelada. |
| CP-R3 | Params tipados y rechazo de valores no booleanos. | Rechazado: contradice DD3 (true boolean/string exacto; otrosfalse). |
| CP-R4 | Enum, helper, factory y deduplicación de returns. | Rechazado: diseño DD2 congelado y estilo sin defecto observable. |
| CP-R5 | Assert/import style y firma de metadata. | Rechazado: mejoras opcionales sin defecto material; conservar reglas enforced. |
| CP-R6 | Confirmar flag, outputs, step, marker y endpoint. | Flag duplica CP-1; otros contratos explícitos y patrón MV vigente contrastado. Sin incompatibilidad reproducida. |

### Playmaker

Shot1 2899d805261cbd65a29688a394b97ff293dc5cd8, Shot2 sin defecto material introducido, Shot3 74bcdde08a1dce9ec3000db1588ad464f439d5c3 promovió prueba permanente de YAML real + autorización + dispatch. Owner autorizó exclusivamente .testing/impact.json como quinto archivo tras error `testing-contract: .testing/impact.json must be added or updated with the affected changes`.

| ID | Observación Zord | Decisión manager |
|---|---|---|
| PM-Z1 | Fixture mutable compartido | Rechazado: BeforeEach recrea repositorio/datos por invocación. |
| PM-Z2 | Strings YAML frente a enums | Rechazado: patrón vigente; abstracción fuera de alcance. |
| PM-Z3 | Confirmar acción de lectura | Rechazado como pendiente: DescribeMatViewAction/ActionDispatcher contrastados. |
| PM-Z4 | Repositorio podría devolver copia | Rechazado: hipótesis contradice implementación in-memory y caso observado. |
| PM-Z5 | CsvSource frente a MethodSource | Rechazado: estilo válido, sin fallo. |
| PM-Z6 | Negativa repetida por fila | Rechazado: redundancia menor sin gap funcional. |
| PM-Z7 | Confirmar consumidor/front | Rechazado como pendiente: extremos y par exacto contrastados con probe. |
| PM-Z8 | Helper para setup de una línea | Rechazado: wrapper sin beneficio demostrado. |
| PM-Z9 | Constante adicional en test | Rechazado: opcional, sin defecto material. |

### Front

Shot1 96c9509fe2cec4dd2835cb298145be8b49929bd8. Shot2 local sin defecto material reproducible: 161 focalizados y probes independientes de SQL/ownership/header/eligibilidad/adapter/relaciones, más dobles comillas + SQL SECURITY NONE y cancel→reopen sin mutación. La corrida inicial de Zord fue rechazada automáticamente; tras autorización específica del owner el 2026-10-22 se completó 8/8 sobre d49225f y encontró FRONT-ZORD-1 HIGH reproducible. Shot3 inicial0f3339d71394fd39e9dc7f58305f9aaba676dbdc promovió Cancel; continuación del mismo Shot3 corrigió PT2 en d49225f0c24f44885c8c4ada022bea0a96c8db15, sin cuarto shot.

FRONT-E2E-PT2 aceptado: ClickHouse25.8.33.6 emite SELECTwindow sin backticks aunque lista de columnas declara `window`. Oráculo válido: result.ddl de acción Playmaker f358ecb0-53c9-4aa8-bda0-d01ae7123c19, JSONdecoded10LF/0backslash-n, SHA25658ff04c5401c2993357ea63e15b4bc60e234bc87a52626105f745f03fe890fa2. Fuente original extraída por git show falló; final fuente fijada por hash pasa. Normalizador cita proyección declarada, conserva literales/comentarios y referencias calificadas; WINDOW clause real sigue prohibida. Validator estricto y PA3 no se relajaron. Test permanente usa el payload real byte por byte en archivo existente.

Primer ensayo PT2 con TSV escapado: rechazado como oráculo inválido del harness y conservado como historia; nunca se usa para certificar la corrección. Nordic propio se detuvo antes de editar fuentes, evitando watch/reload entre SHA. Corrección habilitada solo después del oráculo válido.

## E2E físico y límites

Worker gpt-6-sol LOCAL, corrida rio-refreshable-20261021234729-372852, CPb238622 yPM74bcdde yfront0f3339d7; ClickHouse25.8.33.6. Se comprobaron jars/hashes dentro de containers y procesos supervisados. Recheck acotado rio-refreshable-pt2-20261022-c4cZWo fijó frontd49225f por blobs git show y bundleNode24.19.0, usando el mismoDDLreal. Este segundo check acredita comportamiento de fuente PT2, no nuevo recorrido UI ni E2E completo de tres apps.

| Gate | Resultado final | Evidencia y límite |
|---|---|---|
| E2E-A / CA1 | BLOCKED | Nordic401 y navegador net::ERR_CERT_AUTHORITY_INVALID; no modal journey. También faltan capacidades de credenciales. |
| E2E-B / CA6 | BLOCKED_INFRA | DeploymentFAILED genérico por KvsClient: Container name cannot be null or empty. Vista/target intactos; no acredita mensaje del endpoint. |
| E2E-C / CA7 | NOT_EXECUTED / BLOCKED | No primer import físico exitoso. |
| E2E-D / CA11 | PASS backend físico | Execution480da629-0cd8-4428-af74-7ad116d208da: FAILED explícito por vista externa borrada; vista ausente y sourceHash/targetRows1/targetHash/targetDdlHash/userCount3 invariantes. |
| Verificación1 / PT2 | PASS fuente sobre SHA final027d9f10c | DDL JSON real validado por worker independiente:11 comprobaciones; ownership eliminado, window citado, referencias/literales/comentarios intactos, WINDOW real rechazada. No acredita E2E conjunto. |
| Verificación2 | PASS semántico; drift literal | Kafka usa params.external_reference=true; CPmapper produce data.externalReference=true. No existe parameters en el cable capturado. El guard físico de D actuó. |

Stack local: KvsConfig crea FuryKvsClient sin container-name local para MatViewCredentialService; CkaasConfig no tiene alternativa local para mvImportCkaasKey; LocalEncryptCommand es mock, no KMS real. No se llamó KVS/CKAAS corporativo ni se inventó ciphertext para acreditar A/B/C. Suite auxiliar PMClickHouse4/5: fallo heredado de generador crud_user sin dígito, separado de nuevos tests.

## Teardown y auditoría

Observado al cierre: cero containers y cero procesos/listeners propios. **Preservación del baseline de volúmenes UNVERIFIED.** El preflight no persistió IDs antes de mutaciones y su primer conteo24 no pudo reconciliarse. Inventarios antes/después de teardown: 26IDs→18IDs, ocho retirados, cero agregados. El manager recalculó esa diferencia y hashes de ambos inventarios.

Se retiraron dos volúmenes nombrados de Compose y seis anónimos. Tres anónimos tienen mount de broker propio acreditado; faltan pruebas retenidas para la identidad de otros tres y de nueva creación frente a baseline de todos los recursos reutilizables. La relación con el init Kafka y sus imageVOLUME es hipótesis, no certificación. No se afirma pérdida de datos ajenos, pero tampoco cleanupPASS. Artefactos privados fuera repo conservados; ninguna nueva mutación Docker/VM, restore o prune autorizada. Auditor independiente cleanup_audit gpt-6-sol LOCAL completado: preservaciónUNVERIFIED. Los dos volúmenes nombrados son OWNED_NEW con prueba Creating/Created de logs; los seis anónimos son UNKNOWN respecto de nueva creación frente a baseline. Los18IDs posteriores siguen presentes; eso no acredita ausencia de escrituras ni procedencia de los retirados. Auditor no realizó mutaciones. Evidencia: [[2026-10-22-codex-gpt-6-sol-refreshable-cleanup-audit]].

## ✅ Tareas

- [r] Revisar tres drafts y matrices RF/CA; ningún gate owner aceptado. #owner/me #type/pr-review #area/meli
- [ ] Resolver typecheck heredado sin waiver implícito. #owner/me #type/dev #area/meli
- [x] Corregir FRONT-ZORD-1 HIGH en el mismo Shot3 y verificar integración:027d9f10c, recheck independiente4/4 y PT2fuente11/11; Zord8/8 completado sobre d49225f. #owner/me #type/pr-review #area/meli
- [ ] Resolver capacidades locales KVS/CKAAS/cifrado y acceso al modal antes de repetir A/B/C. #owner/me #type/dev #area/meli
- [ ] Revisar auditoría de volúmenes y decidir pasos forenses antes de mutar Docker/VM. #owner/me #type/admin #area/meli

## Reusable behavior candidates

- Probar flags y claves después del mapper real, no solo con mapas construidos directamente.
- Probar el contenedor real que consume el adapter: modal y formulario pueden discrepar sobre readOnly aunque las pruebas aisladas pasen.
- Verificar manifests de testing antes de congelar el presupuesto de archivos.
- Declarar payload privado, CLI/proveedor y destinos del review antes del primer Shot2.
- Normalizar el DDL JSONdecoded del contrato real, sin confundir TSV escapado con SQL.
- Gate durable de inventario/ownership por ID antes de Compose y teardown; nunca borrar recursos ambiguos por prefijo o por estar montados en un contenedor propio.

## 🔗 Docs / Links

- [[RIO E2E local]] — entorno, iniciativa independiente.
- [[2026-10-21-codex-unknown-refreshable-import-manager]] — coordinación y validación real de SHA/diffstat.
- [[2026-10-21-codex-gpt-6-sol-rio-refreshable-import-physical-e2e]] — ambas corridas físicas/acotadas y límites.
- [[2026-10-22-codex-gpt-6-sol-refreshable-cleanup-audit]] — auditoría independiente de volúmenes, hashes de inventarios y clasificación de los ocho IDs.
- [[2026-10-21-codex-gpt-6-sol-cp-refreshable-import-shot1]], [[2026-10-21-codex-gpt-6-sol-cp-refreshable-import-shot2]], [[2026-10-21-codex-gpt-6-sol-cp-refreshable-import-shot3]].
- [[2026-10-21-codex-gpt-6-sol-pm-refreshable-import-shot1]], [[2026-10-21-codex-gpt-6-sol-pm-refreshable-import-shot2]], [[2026-10-21-codex-gpt-6-sol-pm-refreshable-import-shot3]].
- [[2026-10-21-codex-gpt-6-sol-front-refreshable-import-shot1]], [[2026-10-21-codex-gpt-6-sol-front-refreshable-import-shot2]], [[2026-10-21-codex-gpt-6-sol-front-refreshable-import-shot3]].

## 📆 Bitácora

- 2026-10-21: cold bootstrap, specs por SpellbookCLI y worktrees aislados desde origin/develop; tresShot1 en paralelo. Código vigente avanzó sobre bases de técnicas; no se editaron specs.
- 2026-10-21: owner autorizó exclusivamente manifest Playmaker como quinto archivo. CP yPM completaron shots y drafts; front mantuvo bloqueos heredados/automáticos explícitos.
- 2026-10-22: continuó misma sesión tras medianoche, sin nuevos shots por fecha. E2E encontró PT2; primer oráculoTSV descartado y campoJSONreal confirmó defecto. MismoShot3 corrigió y publicó d49225f; probe independiente posteriorPASS.
- 2026-10-22: E2EA/B/C bloqueados por entorno; D ypropagaciónPASS. Se retiró certificación de preservación de volúmenes, se congelaron mutaciones y se despachó auditor independiente de solo lectura. Auditoría final UNVERIFIED:2namedOWNED_NEW/6anonUNKNOWN, sin afirmar pérdida ajena nicleanupPASS. Sesión cerrada por pedido explícito del owner, proyectoactivo y estado globalBLOCKED; siguienteacción: owner revisa bloqueos/capacidades y auditoría antes de nuevas mutaciones.

- 2026-10-22: auditoría independiente terminó enUNVERIFIED, manager contrastó hashes de inventarios7853e811... y7647b144... y resta8IDs. Se conserva freezeDocker/VM. Feedback y cierre por delta: estado único en este proyecto, registros por worker/modelo, sinL0/L1 redundante ni cambios de skills.

- 2026-10-22: owner autorizó explícitamente enviar el diff privado del PR816 a los servicios configurados codex y claude mediante `zord assemble --scope branch --include rjara-rio-impact --output-json --quiet`. Reanudado el mismo worker Shot2 sobre SHA final d49225f, sin nuevo shot, publicación de comentarios ni mutaciones Docker/VM. Resto de bloqueos persiste.

- 2026-10-22: Zord COMPLETE 8/8 sin errores, 27 findings brutos en /tmp/front-shot2-zord-final.json. FRONT-ZORD-1 HIGH aceptado: NodeConfigModal activa readOnly al hidratar external flag y RefreshableTableForm retorna antes de onSubmit, aunque Save aparece habilitado. Probe real /tmp/front-shot2-probes/front-shot2-node-config-repro.spec.tsx: SHOT2_REPRO exit1/onSave0 frente esperado1; control sinflag exit0/onSave1. Reanudado MISMO front_shot3 para corrección typedoptin del adapter y regresión integrada, preservando permisos/CA12 y presupuesto20; detener antes de exceder y justificar extras si no puede consolidar sin perder comportamiento.

### Triage adicional Zord autorizado del front

Resultado de la continuación del mismo Shot2 sobre d49225f: COMPLETE, 8/8 revisores sin errores, 27 findings brutos. Manager acepta `rjara-rio-impact:1` (FRONT-ZORD-1 HIGH) como defecto reproducible del guardado integrado. Acepta `rjara-rio-impact:2-3` y `io-boundaries:2-3` exclusivamente como dos gates de rollout: soporte CP y permiso PM deben estar desplegados antes del front; son cuatro observaciones duplicadas, no cuatro defectos nuevos ni autorización de alternativas a las PA. `performance:1` se registra como backlog de fetch warehouse sin degradación medida, fuera del gate. Los otros21 se rechazan como correcciones por estilo, contratos ya comprobados, invariantes de callers o hipótesis sin reproducción; el motivo por ID está en [[2026-10-21-codex-gpt-6-sol-front-refreshable-import-shot2]].

Plan de corrección aceptado dentro20: capacidad tipada opt-in `managesExternalReferenceReadOnly` en adapter y consumo genérico en NodeConfigModal; solo refreshable la activa, sin omitir readOnly explícito ni !canSave. Integración permanente en suite ya modificada. Se consolidan hidratación con adapter y preview con evaluación compartida para compensar dos archivos genéricos nuevos; sin retirar comportamiento ni pruebas. Gates del owner permanecen abiertos.

### Cierre de la continuación autorizada

- Mismo Shot3 corrigió FRONT-ZORD-1 y publicó `027d9f10c83b1962ea463c905f17d2de58b291bf` en el mismo draft816. Manager comprobó HEAD y worktree limpio, diff20archivos +1309/-276 contra origin/develop y head remoto exacto, draft=true/base=develop. Consolidación de preview+evaluación e hidratación+adapter compensó los dos archivos genéricos tocados; sin ampliar presupuesto.
- Gates del implementador: unit502/502suites y11710/11710tests PASS; lint0errores/385warnings PASS; changed-statements142/144=98,61%; diffcheckPASS. Typecheckexit2 con123diagnósticos heredados, identidad+código igual a base, un cambio textual explicado31→32; no waiver.
- Verificador independiente del mismo Shot2 fijó027d9f10c y repitió el reproducer original más permisos/CA12:4/4PASS, externo onSave1 antes0, control1, readOnly explícito impideguardar, FAILED sin deployedconfig bloquea source/destination y cambiosSQL. Probe temporal DISPOSABLE_REPRODUCER, permanentes en suite existente. PT2 sobre DDLrealSHA25658ff04c5401c2993357ea63e15b4bc60e234bc87a52626105f745f03fe890fa2 pasó11 comprobaciones source-only con fuentes fijadas al SHAfinal; sin Docker.
- Zord completo correspondió a d49225f, no se atribuye su corrida al commit027d9f10c; el delta correctivo tuvo revisión/probe independiente. Persisten E2EA/B/C bloqueados, D físico previoPASS sobreCPfinal, propagaciónPASScon drift y baseline de volúmenesUNVERIFIED. Rollout exige CP/PMcompatibles antes del front. Estado globalBLOCKED; ningún gate del owner cerrado.

- Descripción vault/remota y único hilo CodeQL actualizados por Shot3 al SHA027d9f10c: https://github.com/melisource/fury_ads-signals-frontend/pull/816#discussion_r4347520487. Cierre de esta continuación por delta en los mismos registros de proyecto, feedback y agent-runs; globalBLOCKED sin nuevos gates aceptados.

## Versiones de prueba solicitadas el 22 de octubre

El owner autorizó crear `0.0.1-import-ref-view-ch` en rio-controlplane-clickhouse, rio-playmaker y ads-signals-frontend desde sus SHA finales b23862238960773fa965681e95180ad44754ae3c, 74bcdde08a1dce9ec3000db1588ad464f439d5c3 y 027d9f10c83b1962ea463c905f17d2de58b291bf. Es una operación de artefactos de testing, separada de los tres shots de código y sin aceptación de gates. No autoriza despliegues; el owner probará en testing. Un worker TOP LOCAL gpt-6-sol crea y sigue las versiones mediante Fury CLI, sin cambios de código ni publicación productiva. La CLI requirió renovar login; el flujo corporativo terminó correctamente. Las tres versiones fueron creadas y el manager consultó de forma independiente `fury versions -a <app> get 0.0.1-import-ref-view-ch --output json`: versión exacta y commit esperado en las tres. Tras el seguimiento, las tres quedaron FINISHED con ci.test_passed=true y registry_availability no vacío, verificados también por el manager. Tests de build habilitados; no despliegues.

| App | Versión de prueba | Commit fuente | Build observado | Estado final |
|---|---|---|---|---|
| rio-controlplane-clickhouse | [0.0.1-import-ref-view-ch](https://web.furycloud.io/rio-controlplane-clickhouse/versions/detail/0.0.1-import-ref-view-ch) | b23862238960773fa965681e95180ad44754ae3c | [503](https://rp-builds.furycloud.io/blue/organizations/jenkins/rio-controlplane-clickhouse/detail/rio-controlplane-clickhouse/503/pipeline/) | FINISHED; CI PASS; registry disponible |
| rio-playmaker | [0.0.1-import-ref-view-ch](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.1-import-ref-view-ch) | 74bcdde08a1dce9ec3000db1588ad464f439d5c3 | [1859](https://rp-builds-java.furycloud.io/blue/organizations/jenkins/rio-playmaker/detail/rio-playmaker/1859/pipeline/) | FINISHED; CI PASS; registry disponible |
| ads-signals-frontend | [0.0.1-import-ref-view-ch](https://web.furycloud.io/ads-signals-frontend/versions/detail/0.0.1-import-ref-view-ch) | 027d9f10c83b1962ea463c905f17d2de58b291bf | [890](https://rp-builds.furycloud.io/blue/organizations/jenkins/ads-signals-frontend/detail/ads-signals-frontend/890/pipeline/) | FINISHED; CI PASS; registry disponible |

**Solicitud de versiones: COMPLETADA.** Las tres versiones de prueba `0.0.1-import-ref-view-ch` están disponibles en Fury desde los SHA autorizados. CP y front tienen registry_availability en us-east-1.aws y us-east4.gcp; PM además en ca-central-1.aws. El manager comprobó get y metadata de categorías ci/registry mediante consultas independientes; no se infiere una certificación binaria por hash ni un despliegue. El worker conservó HEAD/status de los worktrees, incluido el dirty no funcional previo del CP, que Fury excluyó explícitamente. No cambios de producto, branches, PRs adicionales, despliegues, F1 ni Docker/VM. Para testing, desplegar CP y PM antes del frontend. Los gates abiertos de la entrega original se mantienen. Evidencia de operación: [[2026-10-22-codex-gpt-6-sol-refreshable-testing-versions]].
