---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
  - "[[BTG-S04-GOD-ADVERSARIAL]]"
  - "[[BTG-S02-DESIGN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-07"
updated: "2026-10-07"
---
## Propósito

Cerrar dentro de BTG-S05 los 16 hallazgos materiales de S04 y entregar un candidato reproducible para revisión del Primary y aceptación posterior del Owner. Este documento concentra la matriz, decisiones S05, evidencia, límites y próxima acción; los logs, manifests y fuentes completas permanecen fuera del vault.

## Contenido

### 1. Estado, autoridad y baseline

`BTG_S05 = IN_PROGRESS`; `PROGRAM_STATE = REMEDIATION_IN_PROGRESS`; `PRODUCT_NOT_CERTIFIED`; `READY_FOR_PRIMARY_FINAL_REVIEW = false`; `GATE_ACCEPTED = false`; `PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED`. Este estado describe avance documental/evidencia inicial, no cierre de ningún finding ni aprobación de producto.

Autoridad: mandato Owner BTG-S05 vigente (PROMPT_VERSION 2, 2026-10-07) > requisitos aplicables y decisiones S05 explícitas > informe S04 y evidencia reproducida > claims históricos S03. BTG-S05 es el último shot del programa: no crear S06 ni rebajar requisitos. ROI/tuning queda fuera de alcance. No órdenes físicas, compras reales, despliegue, PROD/ETCD ni revalidación física D6 fueron ejecutados por este segmento.

Producto auditado: `xKoRx/echo`, `codex/btg-s03-remediation@1bf45050780554c1135edc619bf01a8a4b04ba08`. Test overlay independiente exacto: commit local `d5b16049bbee7295063e88d8d8f7fa0a4bbe34fe`, padre exacto el SHA auditado, siete archivos de tests nuevos. El checkout S05 fue preparado sobre ese baseline con las pruebas S04 preservadas; su SHA inicial observado fue `3d4e9cd20a964e42ab39f789170f6d40073b506e`, antes de cambios S05. La integración de código y todos los fixes corresponden a workers Echo; este escritor no modificó código de producto ni asserts.

El informe S04 fue publicado en Agents-OS master por `8e32c2430ec8baa1d96cc69d7d1b52d91e513e4d`. El blob actual de `BTG-S04-GOD-ADVERSARIAL.md` en master `ddcd6a248560ef46d1ba74fd07825461d907952c` coincide con el blob publicado (`d26564e8dda26af2330de54aed3fe870b3911cd7`); no se inventa una actualización bootstrap. S04 clasificó hallazgos según evidencia y límites del auditor; sus PASS_BOUND y observaciones no son certificación S05.

### 2. Evidencia inicial y su alcance

Manifest S04: SHA256 `beef01ef8b2f3e115120160eac2c7837adfcec89e4aae53355c5ad70826adc53`, 226 entradas; `sha256sum -c` verificó todas. Bundle de 39,078,645 bytes: SHA256 `1de87cb240a217b79cd192d3663a04cfb2daa4ed4bacc77090838a0ae171897f`. Patch preservado: SHA256 `5f6d730a2ade1a9e29d9826e47f239dcd94901c60b08443999009caf7d759c2c`.

La reproducción final ejecutó cuatro grupos cortos sin modificar tests, bajo `unshare --user --map-root-user --net`, `GOPROXY=off`, `GOSUMDB=off`, `GOMAXPROCS=2`, `-p 2` y `timeout 180s`. Los cuatro grupos devolvieron exit 1 por las aserciones RED preservadas: backtester causal 3 PASS/9 FAIL; venue 0/2; campaña 5/5; runtime 2/2. Los PASS son controles o sondas de límites; no transforman el comportamiento faltante en requisito satisfecho. Logs definitivos y hashes: `work/btg-s05-20261007/evidence/initial/causality-network-ns.log` (SHA256 `94a850854bb63830830a3229ae02a5234403bc5e4acfe0ea27d96c91cfe01c04`), `venue-network-ns.log` (`1efb262cbfa0525ee635ce9f0c31f459b6f26aa215d0a341575aa1364e169332`), `campaign-network-ns.log` (`ae85e1da74c654008b107203a9a0696b57aac7da2250a4de63b7a4720300f725`) y `runtime-network-ns.log` (`6579d4959f96f19a7db538cb3eb85d84c95b00214195895bd79ac6fcd2022be4`). El primer intento directo con proxies Go apagados no probaba aislamiento; se repitió bajo el namespace de red documentado y esa segunda corrida es la autoridad de RED inicial.

Entrega S04 y capsule/logs son referencias de evidencia, no claims de fix. D6 canónico `artifacts/d6-final-physical-certification-20261005/D6-FINAL-PHYSICAL-CERTIFICATION.md` pertenece a `d08a30ce9815f820fda7132e20dc42cc345eb8e8`, no ancestro del producto auditado; el merge-base indicado por S04 es `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6`. El certificado no se transfiere al candidato ni a un build S05. Cualquier preparación física futura requiere autoridad y revalidación separadas; no se ejecutó aquí.

#### Matriz S04-01…16

`RED` apunta a la reproducción aislada de esta cápsula salvo donde se marca `OBSERVED_S04`; esas dos formas se conservan separadas. `FIX_SHA`, regresión de corrección, rerun independiente y rerun real permanecen `PENDING` para cada fila hasta contar con evidencia fresca atribuida al SHA final. No existe finding cerrado en este corte.

| ID / gravedad S04 | Requisito conservado | RED inicial / evidencia | Fix SHA | Regresión S05 | Rerun independiente final | Rerun real aplicable |
|---|---|---|---|---|---|---|
| S04-01 / P1 | Siguiente paso intrabar compite en scheduler común; no observar ni mover reloj más allá de `AdvanceUntil(t)`; preservar timers y streams. | `RED`: `causality-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-02 / P1 | Skip requiere demanda/obligaciones de consumidores estructurales y equivalencia; flat/net0 no demuestra inercia. | `RED`: `causality-network-ns.log`; primera divergencia estructural preservada en S04 | PENDING | PENDING | PENDING | PENDING |
| S04-03 / P1 | Publicar clock, mark y MarketContext del paso antes de entregar fill/callback. | `RED`: `causality-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-04 / P1 | No recorrer extremos ni coordenadas históricas ya consumidas por esa exposición. | `RED`: `causality-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-05 / P1 | Fases V2 Close/Open respetan orden causal congelado, incluso con igual UTC. | `RED`: `causality-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-06 / P1 | Venue da prioridad protectora y drena efectos de un fill antes de reevaluar el siguiente candidato. | `RED`: `venue-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-07 / P0 | ADD y parciales mantienen cobertura total; reconciliar cantidad aparte del tightening, claims/finality y caps; bloquear new-risk inseguro. | `RED`: `runtime-network-ns.log`, casos adverse/pyramid | PENDING | PENDING | PENDING | PENDING |
| S04-08 / P1 | Strategy y MoneyManager sustituibles por factories tipadas públicas compartidas antes de operar. | `RED`: `runtime-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-09 / P1 | Requirements del módulo sustituido gobiernan streams/readiness/MarketContext antes de construirlos. | `RED`: `campaign-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-10 / P1 | Cuenta nueva instala sus propios términos EVALUATION junto a las autoridades financieras. | `RED`: `campaign-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-11 / P1 | ON_DEMAND reemplaza en el próximo minuto negociable tras desenlace y quiescencia. | `RED`: `campaign-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-12 / P2 | Totales de campaña agregan cobros efectivos desde cero monetario exacto; caja y cobros conservan conciliación. | `RED`: `campaign-network-ns.log` | PENDING | PENDING | PENDING | PENDING |
| S04-13 / P1 | Última revisión O(1) en autoridad correcta; evitar copia completa por consulta sin alterar exactitud. | `OBSERVED_S04`: `btg-s04-god-20261007/evidence/performance/active600.log`, `active600.mem.pprof`, `profile-alloc.txt` | PENDING | PENDING | PENDING | PENDING |
| S04-14 / P2 | Revisiones/marks retienen sólo lo necesario; preservar risk, dedup y evidencia streaming sin límites arbitrarios. | `OBSERVED_S04`: `evidence/performance/summary.md` y `active120/300/600.log` | PENDING | PENDING | PENDING | PENDING |
| S04-15 / P1 | Implementar selección MIXED por disponibilidad/minuto; mantener ticks observados y no inventar BBO/fallback. | `RED` de capacidad: `causality-network-ns.log`; probe PASS significa capacidad ausente | PENDING | PENDING | PENDING | PENDING |
| S04-16 / P2 | Provenance vincula build/source/diff/untracked/inputs/outputs; compatibilidad semántica y byte identidad se reportan aparte. | `OBSERVED_S04`: `btg-s04-god-20261007/evidence/provenance.json`, `evidence/performance/golden-v1-comparison.json` | PENDING | PENDING | PENDING | PENDING |

### 3. Decisión S05

**S05-DEC-01 — protección lógica por precio con tramos limitados por caps.** El mandato Owner vigente S05 v2 prevalece para esta corrección frente a la cardinalidad de una sola `protective STOP Order` lógica indicada por D4-B2 §18. La protección conserva un precio/intent lógico; el venue la materializa mediante tramos no superpuestos de máximo 5 contratos por orden para cubrir exposición 7, dentro del máximo account-wide 10 del caso. La reconciliación de cantidad es independiente del tightening del precio: el nivel previamente alcanzado nunca se afloja; claims permanecen hasta finality; no puede existir cobertura ejecutable duplicada; ningún new-risk se admite si falta autoridad/protección exigible; salida/force-close cancela y reconcilia todos los tramos.

La aceptación de esa decisión exige pruebas LONG y SHORT y ambas familias de add; adverso/favorable; fills parciales/duplicados; cancel-replace y finality tardía; add pendiente durante CLOSE/force-close; transición por transición de exposición, cobertura, claims y admisión. Un stop único por 7 que exceda cap5, liberar claim antes de finality, cerrar dos veces o evaluar sólo el estado terminal no cumple. La decisión no autoriza cambiar Strategy, mejorar ROI ni rediseñar ejecución física.

**S05-DEC-02 — mantenimiento protector antes de admitir riesgo, `IN_PROGRESS`.** Si un ACK autoritativo indica `WORKING` para protección y ese hecho satisface un trigger material de mantenimiento, la protección/reconciliación requerida precede a cualquier nuevo riesgo; no se posterga tightening requerido para hacer pasar una prueba. El mandato Owner autoriza un cambio mínimo de mantenimiento MM desde Operation en `operation/engine.go` más su regresión: ACK protector con contexto y freshness actuales, deduplicación y precedencia de CLOSE/force-close. La causa se detectó porque la finality instala protección, pero el ACK no reactiva MM y el fixture S04 no ofrece otra quote. El contrato exacto del trigger sigue pendiente de adjudicación/evidencia del worker; todavía no hay fix ni aceptación. No generar quote sintética, polling ni bypass de authority/freshness.'

### 4. Alcance funcional congelado, orquestación y siguiente secuencia

BASIC sigue siendo una cuenta continua USD 100,000, con oportunidades admitidas por módulos y seguridad. CAMPAIGN conserva caja USD 5,000, compra ON_DEMAND USD 120, una cuenta operando, hasta cuatro cobros efectivos y reinversión; comprar deja USD 4,880, y pérdidas virtuales de la cuenta no se cargan otra vez a caja. Se mantiene el perfil funcional configurado y su piso estático explícito; no se atribuyen reglas a una prop real. S2 conserva decisiones de 5m/H4 cerradas y base 1m; el dominio compartido y SimExecution conserva sus límites congelados en el mandato Owner.

| Rol / función | Modelo solicitado | Modelo ejecutado | Estado / evidencia |
|---|---|---|---|
| GOD, SUBMANAGER: prioridad, decisiones materiales, revisión de evidencia; cero código | GPT-6 Astra | UNKNOWN | Activo; costes/tokens UNKNOWN |
| Evidencia y RED inicial, LOCAL ONE-SHOT | gpt-6-luna | UNKNOWN | Este registro; rerun aislado completado |
| Protección compartida y correcciones técnicas | gpt-6.1-sol | UNKNOWN | Workers TOP activos; fixes aún no acreditados aquí |
| Causalidad/venue/skip, corrección e integración coordinada | gpt-6.1-sol | UNKNOWN | Worker TOP activo; integración por un solo owner técnico |
| Campaña/composición/costo/MIXED según dependencias | gpt-6.1-sol para cambios delicados; gpt-6-luna para mediciones acotadas autorizadas | UNKNOWN | En espera de la secuencia definida; no reportar cierre |
| Revisión independiente final, ajena a fixes/integración | gpt-6.1-sol | UNKNOWN | Reservada, `NOT_DISPATCHED` |

Secuencia de aceptación: RED preservado → protección → causalidad/venue → skip → composición/campaña → costo/retención → MIXED/provenance e integración → pruebas críticas y corridas BASIC/CAMPAIGN sobre SHA/build congelados → fresh-context TOP independiente → revisión GOD → revisión Primary. Preparación disjunta puede avanzar en paralelo, pero la integración sigue esa dependencia. Ningún mismo autor revisa independientemente sus propios cambios. Todos los modelos ejecutados y costes permanecen `UNKNOWN` salvo evidencia del harness.

### 5. S01 cobertura y fuente de histórico

Las fuentes S01 importadas byte por byte desde `xKoRx/agents-os@e4a177eb` están en la cápsula externa. El índice focalizado `work/btg-s05-20261007/evidence/initial/source-docs/source-index.md` identifica secciones de corpus, cobertura y límites. S01 documenta un run derivado NQZ3 reproducible con warmup `2023-10-15T22:00Z`, trading `2023-10-29T22:00Z` hasta `2023-11-23T03:29Z`, resultado neto −USD 34,293.32 desde USD 100,000, antes de la auditoría de corrección S04. El horizonte se detiene ante un gap real; no prueba continuidad de los 13 exports, tres años, rollover completo ni aceptación S01.

El censo de 13 archivos reporta 1,096,336 filas y 24,831 minutos ausentes respecto del calendario semanal congelado sin overrides. El derivado elimina sólo 226 filas fuera de sesión y mantiene gaps intrasesión. Cada derivado contiene un segmento local con 51 H4, pero los segmentos no se pueden sumar como una cuenta continua. Causa del gap, calendario histórico, feriados y política de recuperación permanecen no adjudicados; no inventar datos o balances. La especificación de fuentes real/MIXED y cobertura permanece separada de los falsificadores sintéticos.

### 6. Próximo paso y cierre

Los 16 hallazgos siguen abiertos en este corte; las pruebas no ejecutadas, límites de ambiente/datos y requisitos de seguridad se conservan por separado. La tabla sólo cambia a `FIXED_WITH_REGRESSION_AND_RERUN` o `DISPROVED_WITH_EVIDENCE` con evidencia directa y revisión; no se autoproclama gate. El estado final sólo puede ser `READY_FOR_PRIMARY_FINAL_REVIEW` cuando requisitos materiales, evidencia final e independiente estén completos; de otro modo permanece `REMEDIATION_INCOMPLETE` con el gap exacto.

Acción inmediata: workers TOP cierran protección y causalidad según S05-DEC-01; el propietario de integración conserva secuencia y entrega logs frescos con SHA/hash. Después continúa skip, composición/campaña, costo, MIXED/provenance y verificación independiente según §4. El Primary evalúa; Owner conserva aceptación final. `GOD_PRODUCT_CODE_WRITES=0`. Este informe no cierra la sesión del Primary ni declara el runtime físico listo.

## Fuentes

- Mandato Owner BTG-S05 vigente, PROMPT_VERSION 2, conversación 2026-10-07; reglas Frozen y `/verify` de ese mandato.
- [[BTG-S04-GOD-ADVERSARIAL]], publicado por `8e32c2430ec8baa1d96cc69d7d1b52d91e513e4d`; contenido readback idéntico en master al preparar S05.
- [[BTG-S02-DESIGN]] y [[BTG-PLAN]] para invariantes congelados, dependencias y continuidad del programa.
- [[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]], §18; cardinalidad de order supersedida en el alcance indicado por S05-DEC-01.
- `xKoRx/agents-os@e4a177eb`: `BTG-S01-REAL-GERARD-RESULT.md` (SHA256 `d693d08555edfa035f17f1a641565fc3f56dfbb2e08672ed012584a3d3edf639`) y `BTG-S01-REAL-GAP-FORENSICS.md` (SHA256 `f9f8095a964acc381fc1fa12ddd436524af82e8c9bc08e76364f6705c89712e9`); selected index and full copies in `work/btg-s05-20261007/evidence/initial/source-docs/`.
- Baseline test source `xKoRx/echo@d5b16049bbee7295063e88d8d8f7fa0a4bbe34fe`, parent `1bf45050780554c1135edc619bf01a8a4b04ba08`; bundle, manifest and patch hashes in §2; network-isolated logs in `work/btg-s05-20261007/evidence/initial/`.
