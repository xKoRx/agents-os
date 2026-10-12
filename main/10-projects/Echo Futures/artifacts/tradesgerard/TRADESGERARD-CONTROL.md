---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-CONTROL

## Propósito

Fuente única de estado de la etapa A del mandato GOD LOCAL del Owner, recibido el 2026-10-12. Estado técnico: **IN_PROGRESS / CORRECTION_RUNNING**. No READY_FOR_GLM; aceptación final del Owner pendiente. La etapa B corresponde a GLM-5.3-Flash y no se lanza automáticamente.

## Contenido

### Autoridad y límites

[[TRADESGERARD-MANDATE-SNAPSHOT]] autoriza diseño ordinario, desarrollo offline por TOPs, verificación independiente y correcciones. El manager coordina y documenta; no escribe ni integra código, scripts, indicadores ni tests. Sin merges productivos, deploy, servicios, egress de trading, compras/resets reales ni reconstrucción de cuentas personales. BTG-PLAN, BTX-PERF y D1–D6 conservan sus gates históricos. Manager y proyecto permanecen abiertos; el cierre de un shot no los cierra.

Inputs inmutables: caja inicial USD 5.000; compra individual USD 120 a demanda; reinversión sólo de efectivo acreditado; una cuenta operando y un ciclo agregado; turno persistente hasta target/límite/fallo/bloqueo/sesión; target ordinario de evaluación USD 870 netos; pausa interna −USD 1.000 sin reset; NY flat/cancelado al cierre; funded sin heredar 870 ni consistencia de evaluación. Retiros brutos candidatos 2.250/2.300/2.500/3.000. Sin límite artificial de 41 cuentas durante toda la campaña ni horizonte fijo de dos semanas.

### Entregas y responsables

| Entrega | Estado | Evidencia o siguiente acción |
|---|---|---|
| Inventario y diseño por propietarios | REVIEWED_FOR_IMPLEMENTATION | [[TRADESGERARD-CONTRACT]]; inventario completo recibido. |
| Perfil GAU50 versionado | RESEARCH_COMPLETE_SCENARIO_REQUIRED | [[TRADESGERARD-PROP-PROFILE]] separa hechos oficiales, supuestos y UNKNOWN; no certificación comercial. |
| Catálogo finito | DESIGN_VERIFIED_FOR_IMPLEMENTATION | `catalog.json` único, design-2: 53 IDs, 15.168 combinaciones únicas compatibles; auditoría y reparación con 59 checks PASS. |
| Motor, composición, campaña y lote compacto | CORRECTION_RUNNING | TOP corrector_a es el único escritor y ejecutor sobre la rama de desarrollo. |
| Verificación independiente | INTERIM_FINDINGS | Auditoría de 06ab6b12 terminada; tres hallazgos y filas pendientes requieren nuevo freeze y recheck. |
| Cobertura nueva ≥95% | GAP_OPEN | Candidato auditado: 1081/1425 = 75,86%. Seis propuestas de tests ya integradas por el corrector; medición nueva pendiente. |
| Manual, recibo y prompt GLM | IN_PROGRESS | [[TRADESGERARD-EVIDENCE-A]] conserva identidades y resultados; manual/recetas finales pendientes. [[TRADESGERARD-GLM-MASTER]] preparado, sin lanzamiento. |

Harness local verificado. TOPs inventory, prop_profile, catalog, contract_audit, catalog_repair, integrator_a, verifier_a y coverage_prepare terminaron sus shots. corrector_a recibió RELEASE_LANE tras liberación expresa del auditor. Todos solicitados `gpt-6.1-sol`; servido UNKNOWN. No se consume CLOUD Pro ni se presupone GLM disponible en este harness.

### Identidad y evidencia aceptada para corrección

Repo `xKoRx/echo`; baseline source `873f5f1c7df25086271af1de1896095f1cade2a9`. Desarrollo: rama `codex/tradesgerard-platform-a`, checkout relativo al workspace Aranea `work/tradesgerard-platform-a-20261012/echo`. SDD: `specs/FEAT-TRADESGERARD-PLATFORM-A/`.

Último freeze auditado: `06ab6b12d2e4701d21ee8506238a481c5c47af5e`; binario `work/tradesgerard-platform-a-20261012/evidence/integrator/bin/echo-backtest`, SHA256 `7afb11bc32b5d5e3a0330589aa9f0b75310eb2c11193d64204fb5a7ee56951ba`, Go1.27.1, VCS embebido idéntico y modified=false. Manager corroboró HEAD limpio/hash/metadata; no ejecutó campañas. La fuente está ahora autorizada a cambiar por el corrector: estas identidades no certifican su delta.

Auditoría independiente cerrada en `evidence/verifier/{CANDIDATE-AUDIT.md,COMMANDS.md,AUDIT-METADATA.json}` bajo ese workspace. Demostró pase exacto y negativo del 30%, pérdida intermedia, turno y pausa preservados, parciales/rechazo/fill tardío, precios SL/TP y BE, paridad compacta/detallada, fallos/cancelación/cleanup/resume, smoke real con fills y BASIC replay idéntico de 94.798 registros. El recibo detalla alcance y límites; no acredita el total de §10 ni rentabilidad.

| Hallazgo | Evidencia del freeze | Avance del corrector, aún sin recheck independiente |
|---|---|---|
| F01: renovación impaga y ruina | Caja 80, única cuenta RENEWAL_UNPAID, sin pagos pendientes; devuelve censura en vez de ruina. | Reproducer confirmado; prueba pública pasa tras clasificar recuperación por costos vigentes de renovación/setup y compra admisible, conservando historia y cupos. |
| F02: frontera temporal incompleta | Campaña de 35 sesiones falla ANALYTICS_SOURCE_FAILED; control equivalente sin campaña completa. | Regresión antes del fix demuestra SESSION_END pendiente con Deadline igual al frontier publicado. Tras completar todas las fases del instante, campaña de 35 sesiones completa; aún no alcanza el cap 5000 y sigue censurada. |
| F03: cierre de seguridad no convergente | MM público sin SL entra, sufre breach y deja exposición residual con DRAIN_NOT_CONVERGENT. | Reproducido. Corrección/repetición pendientes. Debe permitir reducción real sin habilitar reversión o expansión. |

### Gates y recursos

READY_FOR_GLM exige demostrar todas las filas materiales de §10, regresiones relevantes y cobertura nueva ≥95% con baseline separado y denominador completo. Fixtures sintéticos se identifican como tales; no son resultados de rentabilidad. COMPLETE no sustituye aceptación económica, pending no es caja, hashes no sustituyen replay, y una capacidad estructural pendiente no se traslada a B.

Pendientes explícitos de auditoría: compra y fondos/cupos extremos; independencia del estado de MM por cuenta y ausencia de solapamiento; relojes inactivos/calendario; cuatro targets y cap completo; terminalidad con cuenta utilizable o crédito pendiente; causalidad representada; pico temporal continuo y fallos posteriores de escritura/readback; identidad completa de lote; regresiones restantes. El corrector debe aportar casos reproducibles y un nuevo freeze; un TOP independiente comprobará el conjunto.

Un carril de compilación/prueba/campaña y un escritor de producto. Límites: reserva libre ≥8 GiB, scratch propio ≤2 GiB, durable ≤256 MiB, logs ≤16 MiB, GOMAXPROCS=4 y paquetes seriales. Cada nuevo scratch tiene propietario/manifest; no borrar corpus, caches ni temporales anteriores sin atribución. Auditor anterior liberó sus procesos y registró aproximadamente 11,02 GB libres y 38,85 MB durables; no hubo muestreo continuo del pico temporal. No se ejecuta el barrido de investigación de B.

### Siguiente acción

corrector_a reproduce/corrige F01–F03, integra pruebas revisadas y completa los gaps de §10 y cobertura. La ampliación del fixture sintético para llegar al cap no cambia las ventanas reales ni convierte el resultado anterior en PASS del cap. Luego debe entregar commit limpio, binario/hash/VCS, configuración, comandos, cobertura y recursos para una nueva auditoría independiente. No se reutilizará el binario de tests compilado contra 06ab como verificación del siguiente commit.

Agents-OS se mantiene en master con autosync observado; no se atribuyen sus commits al manager ni se afirma push. Código, corpus y logs pesados permanecen fuera del vault. El handoff final consolidará recetas físicas, evidencia y alcance legítimo de B, dejando abierto el gate del Owner.

## Fuentes

- [[TRADESGERARD-MANDATE-SNAPSHOT]], §§10–12; [[TRADESGERARD-CONTRACT]]; [[TRADESGERARD-EVIDENCE-A]].
- [[Echo Futures]] y `xKoRx/echo:v3/backtester/README.md`.
- `30-resources/agents/skills/technical-project-manager/SKILL.md`; el mandato actual prevalece en modelo Sol 6.1, autonomía interna, alcance y ausencia de cuota de shots.
