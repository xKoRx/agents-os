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
updated: "2026-10-24"
---

# Import de Refreshable Materialized Views externas

## 🎯 Objetivo

Entregar SIG-700 con un PR draft por repo, tres shots independientes y E2E físico conjunto. Rodrigo Jara cierra los gates; el manager solo prepara evidencia para revisión. Se completaron los nueve shots de código; las continuaciones por manifest y por E2E permanecieron dentro de sus shots originales. No hubo Shot 4 ni release productiva.

## 📊 Estado actual

**2026-10-24 — Auditoría corregida, E2E local PASS y tres ramas publicadas; Playmaker bloqueado por el gate Cleric.** CP, front y Lore están pusheados con versiones de prueba `0.0.2-import-ref-view-ch` (CP y front). Playmaker quedó local: el pre-push pasa el contrato completo (64 selectores y 2 checks L0) y el gate Cleric responde BLOCKED por escenarios bajo `.lore/scenarios/`; la versión de prueba vigente de Playmaker sigue siendo `0.0.1-import-ref-view-ch`, que ya contiene el único cambio de runtime. Rollout: CP y Playmaker antes del front.

| Repo | Rama | HEAD | Estado |
|---|---|---|---|
| rio-controlplane-clickhouse | `feature/refreshable-view-import` | `852628c0` | Pusheado. 4783 tests, 1 skip. Versión `0.0.2-import-ref-view-ch` |
| ads-signals-frontend | `feature/refreshable-view-import` | `36749c94b` | Pusheado, sincronizado con develop. 122 suites/3390 tests, lint 385 warnings, typecheck 123 heredados (rojo). Versión `0.0.2-import-ref-view-ch` |
| lore | `feature/rio-ecosystem-drag-and-drop` | `edb5fc0` | Pusheado. Runner 277 tests, typecheck y lint 0 errores |
| rio-playmaker | `feature/refreshable-view-import` | `e8fa4230d` (remoto `0cec5e7c5`) | Push bloqueado por gate Cleric. 5194 tests/3 skips, localTest 64 |

E2E local final `run_mvmmx1oa2d7d9a404d` (corrida 8/8): smoke, import y guardado, primer deploy, reprovisión y solo lectura tras el deploy PASS, con 8/8 oráculos y teardown verificado por identidad. La corrida 7 encontró que la externa desplegada mostraba una nota contradictoria; el front la corrigió antes de la 8. Descripciones: [[Descripción PR — rio-controlplane-clickhouse]], [[Descripción PR — ads-signals-frontend]], [[Descripción PR — lore]] y [[Descripción PR — rio-playmaker]]. Registro: [[2026-10-24-refreshable-audit-fixes-entity-updated]].

Gate de Playmaker preparado hasta donde depende de la rama (HEAD local `9af30184d`): sincronizada con #1332 `dcabdc55a`, escenario nativo `junit-evidence/at-100-s11` regenerado (suite nativa 237/237, `CLEANUP_CERTIFIED`). El bloqueo restante es el tooling de `build.gradle` heredado de #1332; se libera al mergear #1332 a develop. Luego: sync con develop, `./local/test-lore.sh --gate`, perfil readonly + `.sdd/config.json`, push normal.

### Estado anterior — 2026-10-23

**2026-10-23 — Hallazgos corregidos y certificación E2E local PASS; entrega pendiente del push de Playmaker.** La base E2E `9045e81fa6195c612171cb59f624aa50c7854be9` quedó integrada por merge en la rama de import, conservando su ledger, teardown por EXIT con propagación de errores, productor Kafka fail-closed, instalación limitada a clones/checkouts administrados, correlación posterior al seed y naming con doble guion. Los cuatro drafts tienen evidencia nueva arriba y enlaces hermanos; CP, front y Lore están pusheados. El único hilo existente (CodeQL del front) fue respondido con el commit que introdujo el allowlist y el HEAD donde sus 61 tests HTTP pasan.

| Repo | Rama | HEAD local verificado | Publicación y gates |
|---|---|---|---|
| rio-playmaker | `feature/refreshable-view-import` | `d02c4a5ef538de8754b2cd606fb71eac229bcf8c` | Push pendiente: instalación y hooks PASS; gate Cleric BLOCKED por integración de escenarios. `test`: 5191 tests, 0 fallas/errores, 3 skips; `localTest`: 64 PASS; contrato staged: 55 selectores y 2 checks L0 PASS; contrato committed contra origin/develop: 64 selectores y 2 checks L0 PASS; Python: 11 PASS; lifecycle de procesos PASS |
| rio-controlplane-clickhouse | `feature/refreshable-view-import` | `b05fd16404d2cd876d107dfb1c2cd980729fd89c` | Pusheada. 4781 tests, 0 fallas/errores, 1 skip; tres archivos ajenos de graphify-out preservados |
| ads-signals-frontend | `feature/refreshable-view-import` | `3bf2e828fa5f7643614b08b257f1893714894729` | Pusheada. 121 suites/3323 tests vecinos y 61 tests HTTP PASS; lint 0 errores/385 warnings; typecheck conserva exactamente los 123 diagnósticos previos |
| lore | `feature/rio-ecosystem-drag-and-drop` | `32310661157b008bc92d79999e6bfc455ad086d8` | Pusheada. Runner 18 suites/274 tests PASS; typecheck PASS; lint 0 errores/437 warnings |

| Caso | Corrida Lore | Escenarios | Oráculos |
|---|---|---|---|
| clickhouse-refreshable-view-import | `run_mvlg5rjk8450459643` | 4/4 PASS | 8/8 PASS |
| clickhouse-refreshable-view | `run_mvlg99hc42c8a86ca6` | 2/2 PASS | 4/4 PASS |
| clickhouse-mv | `run_mvlgadyh9b4603e8a0` | 3/3 PASS | 6/6 PASS |
| clickhouse-mergetree | `run_mvlgcyn22e98704696` | 2/2 PASS | 2/2 PASS |
| clickhouse-run-query | `run_mvlgeb496448751bd9` | 2/2 PASS | 3/3 PASS |

Certificación desde limpio con `RIO_ECOSYSTEM_CONFIG` apuntando a `refview.env` y `RIO_ECOSYSTEM_HOME="$HOME/.rio-ecosystem/state-refview"`: 5/8 corridas utilizadas, 13 escenarios al 100 %, 23 oráculos PASS y costo observado US$3.2105. El comando terminó con exit 0. El teardown físico dejó cero contenedores/redes RIO, screens y procesos rastreados; se comprobaron los 16 IDs del ledger y las 24 identidades de proceso capturadas, sin archivos de tracking remanentes. Los puertos de frontend y Lore se acreditaron por PID/cwd contra los checkouts de esta ronda antes del recorrido.

La extracción SQL usa el AS superior y valida el COMMENT literal opcional; la marca clásica vuelve a ser best-effort y sólo la refreshable exige persistencia. El front conserva predicados WHERE y el copy clásico, permite el primer save de revisión y bloquea la externa después del primer deploy exitoso; el primer deploy fallido conserva su comportamiento. PA-2 sólo se fijó por test, sin cambiar la reconciliación vigente.

**Bloqueo restante — actualizado tras autorización:** el owner autorizó la instalación exacta de Grimorio 27.2.1 (`0c21cb41279fdbc991a4b0edee458a9f2bd852f9`), incluidos assets globales, registro y hooks. El bootstrap y `grimoire-hooks verify` terminaron PASS. El gate obligatorio se ejecutó sobre `d02c4a5ef538de8754b2cd606fb71eac229bcf8c` y terminó BLOCKED: exige escenarios Markdown añadidos/modificados en `.lore/scenarios/`; los escenarios certificados están en `.lore/ecosystem/cases/`. El contrato de la base además usa `origin/develop`, entorno `local` y un binding del proceso anterior a la corrida, mientras el ecosistema usa `ecosystem` y ya completó teardown. No se debilitó la política ni se modificó la base. Candidato para la base E2E: integrar explícitamente ambos contratos de evidencia, o preparar una suite nativa adicional bajo el contrato Cleric; requiere resolver ese alcance antes del push. El HEAD remoto sigue en `0cec5e7c5e3d352387b4284b63620bb0e91b6a18`; la definición de terminado permanece incompleta.

Recursos actualizados: [[Descripción PR — rio-playmaker]], [[Descripción PR — rio-controlplane-clickhouse]], [[Descripción PR — ads-signals-frontend]] y [[Descripción PR — lore]]. Evidencia y cierre por delta: [[2026-10-23-refreshable-review-fixes-entity-updated]]. No se trasladaron estas correcciones a la base E2E. PA-1 a PA-5 siguen abiertas; la certificación local no acredita KVS/CKAAS/KMS corporativos ni despliegues Fury.

### Preguntas abiertas contrastadas con las specs

- PA-1: el código acepta un DEFINER existente, sin exigir usuario dedicado. Fixture con owner dedicado; recomendar dedicado para testing y decidir ownership/deprovisión antes de generalizar usuarios compartidos.
- PA-2: la paridad vigente reconcilia antes del ownership; no se cambió la decisión de rechazar diferencias frente a reconciliar. Recomendar rechazo explícito si se quiere garantizar adopción sin alteraciones no previstas.
- PA-3: validación SQL estricta de una fuente, sin joins/subqueries/agregaciones, se conserva. Recomendar mantenerla hasta definir soporte adicional.
- PA-4: no se agregó validación remota de la credencial precargada; la paridad existente no la exige. Recomendar definir una verificación segura antes de cambiar ese contrato.
- PA-5: la credencial permanece en KVS tras el import; no se decidió consumirla ni cambiar TTL. Recomendar una política explícita de reintento/retención antes de eliminarla.
- RF-4 permite importar sin tablas origen/destino en el pipeline; el caso comienza vacío y verifica cero relaciones. El guard del modal clásico no se trasladó a refreshable. Guardar y desplegar son acciones distintas, verificadas en escenarios separados.

### Preflight inicial, superado por la autorización posterior

Las entradas siguientes conservan historia. La autorización posterior resolvió acceso y recreación E2E; la deuda de typecheck y la incertidumbre forense histórica no se convierten en gates aprobados por esta certificación.

**2026-10-23 — BLOCKED en F0 del E2E local.** El preflight detectó `node` PID 62677 escuchando en 8443 y 8080, con cwd en el checkout original del repo `lore`, ajeno al runner de esta tarea. Se aplicó la restricción explícita de detenerse sin matar el proceso. No se ejecutaron fetch, merges, setup, suites, corridas Lore, commits, push ni edición de PRs. El intento no acredita que el feature esté listo para testing. Registro: [[2026-10-23-refreshable-import-e2e-preflight-entity-updated]].

Estado local verificado: los tres worktrees siguen en `feature/refreshable-view-import`; Playmaker `74bcdde08a1dce9ec3000db1588ad464f439d5c3` y front `027d9f10c83b1962ea463c905f17d2de58b291bf` limpios; CP ClickHouse `b23862238960773fa965681e95180ad44754ae3c` conserva únicamente los tres cambios previos en `graphify-out/`, intactos. Inventario Docker no acreditado: la consulta read-only al socket de `colima-rio` fue rechazada por el sandbox. Presupuesto Lore usado en este intento: 0/12, costo US$0. PA-1 a PA-5 no investigadas ni resueltas. Una vez libre 8443, repetir F0 y continuar F1 antes de setup; siguen pendientes la integración de la base E2E, el caso nuevo, la certificación conjunta y los gates finales.

**BLOCKED.** Hay tres drafts publicados, pero no se acredita el E2E completo ni se aceptan gates rojos. Bloqueos: typecheck heredado del front, capacidades locales KVS/CKAAS/KMS ausentes para el import y preservación del baseline de volúmenes todavía no acreditada. La auditoría terminó UNVERIFIED y Docker/VM siguen sin nuevas mutaciones. Zord completó 8/8 tras autorización explícita; FRONT-ZORD-1 fue corregido y rechecado independientemente, sin aceptar gates del owner.

Todos los Shot 1/2/3 y el worker físico usaron el modelo exacto **gpt-6-sol, LOCAL**, con contextos nuevos por shot y agent-runs separados. El auditor de limpieza independiente también usa gpt-6-sol LOCAL. El identificador exacto del modelo del manager no fue expuesto y se registra como unknown, sin inferirlo.

## 🧱 Entrega de desarrollo original — 21 y 22 de octubre

| Repo | Rama / base real | SHA final | SPEC | Draft / diffstat real verificado por manager |
|---|---|---|---|---|
| [[rio-controlplane-clickhouse]] | feature/refreshable-view-import ← origin/develop@4b16f7c2721e0e3c30cd5e020f627cad78040d7f | b23862238960773fa965681e95180ad44754ae3c | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700), [SIG-701](https://spellbook.adminml.com/projects/SIG/specs/SIG-701) | [#362](https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/362), 9 archivos +179/-15, presupuesto10 |
| [[rio-playmaker]] | feature/refreshable-view-import ← origin/develop@f1a4b246d74e679dd81718513b50b56818bd1deb | 74bcdde08a1dce9ec3000db1588ad464f439d5c3 | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700), [SIG-702](https://spellbook.adminml.com/projects/SIG/specs/SIG-702) | [#1328](https://github.com/melisource/fury_rio-playmaker/pull/1328), 5 archivos +92/-28, excepción owner5 |
| [[ads-signals-frontend]] | feature/refreshable-view-import ← origin/develop@9a70723c96ebd7f7a8e6564988ed4f8e630ea58a | 027d9f10c83b1962ea463c905f17d2de58b291bf (candidato, no certificación completa) | [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700), [SIG-703](https://spellbook.adminml.com/projects/SIG/specs/SIG-703) | [#816](https://github.com/melisource/fury_ads-signals-frontend/pull/816), 20 archivos +1309/-276, presupuesto20 |

El manager contrastó HEAD, merge-base, git diff --stat contra origin/develop y head/draft/base remotos de cada PR. CP conserva tres derivados graphify-out modificados por el hook de checkout fuera de los commits; PM/front están limpios. No checkout, stash, reset ni commit en originales. Fetch y worktree add se ejecutaron una vez por repo según autorización.

## Gates originales y descripción de PR — 21 y 22 de octubre

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
- [x] Resolver capacidades locales KVS/CKAAS/cifrado y acceso al modal: proveedores locales probados, Lore drag y certificación conjunta PASS. #owner/me #type/dev #area/meli
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

- **2026-10-26 — PRs actualizados:** #1332 entró a develop (squash) y #1328 quedó retargeteado a develop (`49328ca8b`, diff de 23 archivos sólo del feature). Conflictos con develop resueltos en CP (`377e3dcc`), front (`f599fa78b`) y Playmaker. Review de marellanoqui: ALTO del CP (credenciales tras marker con respuesta perdida) corregido devolviendo las credenciales del import en el reprovision `ALTER_MV`; MEDIO de Playmaker (arranque parcial) corregido registrando recursos por procedencia. Hilos de bots respondidos; el de PA-2 en CP queda abierto para el owner. E2E integrada `run_mvpps59z4c0d5e6de3` PASS 5/5 y 8/8. Versiones de prueba: CP y front `0.0.3-import-ref-view-ch`, Playmaker `0.0.2-import-ref-view-ch` (push con `--no-verify` autorizado por el owner).

- **2026-10-24 — Lore #21 en ready:** la CI fallaba porque `dragAndDrop.node.spec.ts` lanzaba Chromium sin el guard `skipIf` que usan los demás specs; corregido en `1381004`, CI verde. El check `dependencies` sigue rojo por vulnerabilidades heredadas de develop (`simple-git` 3.36.0 requiere 4.0.1; #20 cubre `sharp` y `source-map-js`, no `simple-git`).

- **2026-10-24 — Publicación:** Playmaker pusheado con `--no-verify` autorizado por el owner (sólo el pre-push del gate Cleric; contrato de testing PASS sobre el HEAD), integrado el lock por contexto Docker de #1332 (`f9862eff0`); HEAD `15c359560`, CI verde. #362, #816 y #1328 en ready for review; #21 de Lore en draft con CI de Jenkins roja sin log accesible.

- **2026-10-24 — Gate Cleric preparado:** merge de la base #1332 `dcabdc55a`, escenario nativo `at-100-s11` ampliado con los tests del permiso describe y declarado en `.testing/impact.json`; gate directo ahora bloquea sólo por tooling heredado de #1332.

- **2026-10-24 — Auditoría y correcciones:** auditoría independiente con controles negativos; correcciones vía subagentes en los cuatro repos, run Lore colgado cancelado, E2E 8/8 PASS, CP/front/Lore pusheados, versiones `0.0.2-import-ref-view-ch` de CP y front, descripciones reescritas. Playmaker sin push por el gate Cleric. [[2026-10-24-refreshable-audit-fixes-entity-updated]].

- **2026-10-23 — Continuación autorizada:** instalado Grimorio 27.2.1 en la revisión exacta aprobada, ambos proveedores y hooks verificados PASS. El gate de Playmaker terminó BLOCKED por inventario de escenarios: `.lore/scenarios/` frente a `.lore/ecosystem/cases/`; queda como integración candidata para la base, sin alterar su rama/política. Contrato committed contra `origin/develop`: 64 selectores y los dos checks L0 PASS, exit 0 y cleanup completado. No se consumieron nuevas corridas Lore.
- **2026-10-23 — Fixes del code review:** PM `d02c4a5ef` integrado con base `9045e81fa`, CP `b05fd1640`, front `3bf2e828f` y Lore `323106611`. Suites y certificación nueva PASS: 5 corridas/13 escenarios/23 oráculos; teardown físico cero, 16 recursos y 24 identidades comprobados. Tres ramas pusheadas y cuatro drafts actualizados; push/gate de PM pendientes de autorización del instalador global fijado. El hilo del front fue respondido; PA-1..PA-5 no se decidieron. [[2026-10-23-refreshable-review-fixes-entity-updated]].

- **2026-10-23 — Code review de la implementación (Claude Code, 4 revisores independientes + verificación).** Veredicto: APROBADO CON RESERVAS para pasar a testing; antes del merge: CP #362 extracción `AS (SELECT` toma el cuerpo de un CTE y oculta drift, y el import clásico de MV pasa a fallar si no se escribe la marca (decisión no tomada por el owner); front #816 `normalizeExternalRefreshableSql` borra `definer = x` dentro del query, la refreshable externa queda editable después del primer deploy, copy de MV cambiado sin tests y código muerto; Playmaker #1328 oráculos del caso nuevo cuentan corridas previas, 3 conflictos con la base E2E (16 commits atrás), naming `--` pendiente y estado/screens compartidos entre corridas (causa del teardown cruzado); Lore #21 sin bloqueantes (CHANGELOG, prompt y README).
- **2026-10-23 — certificación local cerrada:** PM `0cec5e7c5`, CP `1a39e420`, front `cdcb115e6` y Lore `78090f60`. Cinco casos/13 escenarios/23 oráculos PASS, teardown cero; 12/12 corridas y US$7.7875. Bugs HTTP camelCase, callback SQL obsoleto y SELECT canónico del segundo PROVISION corregidos con regresiones. Tres drafts actualizados, Lore #21 de apoyo; typecheck heredado continúa rojo. [[2026-10-23-refreshable-import-e2e-alignment]].


- **2026-10-23 — continuación con screens:** merges y suites de los tres repos publicados; PM `85f5bad67`, CP `686d8f7a8`, front `8eaa15827`. #1328 retargeteado y los tres drafts actualizados con evidencia real. Helper genérico de screens y apagado del grupo corregido con RED/GREEN; candidatos a #1332. Autenticación Spellbook y autorización de borrado de volúmenes del stack concurrente pendientes; caso y certificación no ejecutados. [[2026-10-23-refreshable-import-e2e-alignment]].

- **2026-10-23 — certificación refview detenida en preflight:** bootstrap ejecutado una vez y HEAD/status comprobados; 8443 ocupado por Lore ajeno (PID 62677). Se respetó el hard stop sin tocar procesos, Docker/VM, repositorios ni PRs; ningún bug ni decisión de producto nueva. F1–F6 no ejecutadas y PA-1..PA-5 pendientes. Cierre AGENTS OS por delta, agent-run y feedback registrados en [[2026-10-23-refreshable-import-e2e-preflight-entity-updated]]. La skill de autoría app-owned no llegó a cargarse porque F1 no se ejecutó; no se declara un gap de autoría sin evidencia.

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
