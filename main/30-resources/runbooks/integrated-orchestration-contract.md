---
type: runbook
schema_version: 1
scope: area
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[Aranea]]"
  - "[[HERMES — Infrastructure Operations]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[provisioning-operator-contract]]"
  - "[[proxmox-lifecycle-operator-contract]]"
  - "[[linux-container-operator-contract]]"
  - "[[windows-operator-contract]]"
  - "[[service-lifecycle-operator-contract]]"
  - "[[high-impact-networking-dns-contract]]"
  - "[[cluster-node-maintenance-contract]]"
  - "[[ceph-storage-operations-contract]]"
aliases:
  - integrated orchestration contract
  - contrato orquestacion integrada
  - H6 orchestration contract
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - action/orchestration
  - project/hermes-aranea-autonomous-operations
---

# integrated-orchestration-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato de coordinación H6: define cómo Ariadna/Hermes procesa una solicitud operativa de infraestructura de Aranea de principio a fin **dentro del alcance certificado** (H0–H5), la enruta al proyecto ejecutor responsable, aplica los gates y produce un handoff completo y reproducible. **Enablement-only:** este contrato NO autoriza ni ejecuta operaciones; los pasos mutantes pertenecen al proyecto ejecutor con sus propios gates. REUSE > EXTEND > CREATE: reutiliza las matrices de autoridad H1–H5 (en [[HERMES — Infrastructure Operations]]), los contratos de operador existentes y el catálogo/matriz de [[30-resources/aranea/07-integration/00-index|07-integration]]; no crea un segundo orquestador paralelo a Hermes ni una base de datos de estados.

## Precondiciones

- Bootstrap Agents-OS cargado; dominio `aranea` activo ([[aranea-agent-dev]] router); preferencias scoped leídas.
- Catálogo de capacidades y matriz de routing vigentes: [[30-resources/aranea/07-integration/00-index|07-integration — Catálogo integrado y routing H6]].
- Fuentes de estado vigente (no fotografías antiguas): matrices de autoridad H1–H5 en [[HERMES — Infrastructure Operations]] para autoridad/identidades; [[BACKUP-DR-OWNER-PROJECT]] bitácora para el estado actual de Backup/DR; [[30-resources/aranea/06-high-impact/00-index|índice high-impact]] para blast radius y NO_GO vigentes; `30-resources/aranea/01-topologia/fechas-captura.md` para la fecha de cada captura.
- Regla de frescura: si un dato crítico para la decisión tiene captura > 7 días o existe contradicción entre fuentes, revalidarlo read-only en vivo antes de decidir (CONFLICT/STALE → revalidar; nunca adivinar).

## Cadena obligatoria (REQUEST → AGENTS-OS UPDATE)

`REQUEST → INTENT CLASSIFICATION → PROJECT OWNERSHIP → TARGET RESOLUTION → BASELINE → AUTHORITY CHECK → DEPENDENCY CHECK → RISK CLASSIFICATION → GO/NO_GO → EXECUTOR HANDOFF → EXECUTOR EVIDENCE → ACCEPTANCE → AGENTS-OS UPDATE`

Separación de responsabilidad por paso (quién puede avanzar cada estado):

| Tramo | Pasos | Estados alcanzables | Quién |
|---|---|---|---|
| Preparación (Ariadna) | intent, ownership, target, baseline, authority, dependencies, risk, GO/NO_GO | REQUESTED, DISCOVERED, SCOPED, GATED, BLOCKED, READY_FOR_EXECUTOR | Ariadna (este contrato) |
| Ejecución (proyecto ejecutor) | handoff→evidencia→aceptación | EXECUTING, PARTIAL, FAILED, VERIFIED, CLOSED | Proyecto ejecutor con sus gates |

La cadena completa vive en la sección § Cadena de [[30-resources/aranea/07-integration/00-index|07-integration]]; este runbook añade la mecánica operativa por letra A–S del mandato H6:

1. **A — Entradas obligatorias:** solicitud (texto owner o proyectado), consumer/proyecto origen, environment (DEV/test/PROD), need funcional. Una solicitud sin environment o sin need clasificable = AMBIGUOUS (negativo N1): no ejecutar, pedir precisión.
2. **B — Identificación del owner:** resolver el proyecto ejecutor desde la matriz NEED→EXECUTING PROJECT (07-integration § Routing). Si no existe proyecto para la operación: `EXECUTOR_NOT_DEFINED` — NO asignar silenciosamente la ejecución a Infrastructure Operations; preparar ficha de proyecto propuesta y detenerse.
3. **C — Resolución de targets:** desde el inventario H0 (identidad estable `node+VMID`, no nombres efímeros) + verificación viva read-only cuando la decisión dependa del estado (target proof: estado vivo, IP viva/DNS consistente, quorum). VMID/IP históricos no son reservas.
4. **D — Selección de capacidades:** del catálogo integrado (07-integration § Catálogo), por Capability ID; usar el estado de enablement/certificación registrado, nunca inferir certificación de la identidad.
5. **E — Identidad y canal:** de la matriz de autoridad vigente (H1–H5). Canal nativo primero; MCP sólo como consumer plane; jamás token `ariadna@pve!backup-dr` para gestión (sólo `VM.Audit`+`VM.Backup` en `/vms`).
6. **F — Gates de autorización:** CLASS 1 → ejecutor decide dentro de su contrato; CLASS 2 → ejecutor + ventana + evidencia reforzada; CLASS 3 → owner gate explícito por acción, sin excepción. `AUTHORITY AVAILABLE != EXECUTION AUTHORIZED != OPERATION EXECUTED != RESULT VERIFIED`.
7. **G — Dependencias:** consultar el grafo (07-integration § Dependencias) + checks read-only de la propia cadena (¿el canal de administración sobrevive a la operación? ¿el backup/protección del target está demostrado?).
8. **H — Orden de ejecución futuro:** lo propone Ariadna en el handoff (fases, puntos de verificación); lo ejecuta y ajusta el ejecutor.
9. **I — Concurrencia:** una sola escritura por recurso; dos operaciones sobre el mismo target/nodo/storage = serializar o GATED (declarar en el handoff el lock lógico asumido).
10. **J — Idempotencia:** el handoff exige precondiciones verificables y pasos re-ejecutables; el ejecutor detecta estado existente antes de cada mutación (ej.: template ya clonado, key ya instalada).
11. **K — Timeouts:** toda operación mutante del handoff declara timeout y criterio de abort; ante timeout NO reintentar a ciegas: leer estado durable y reconciliar (lección global de continuidad).
12. **L — Resultados parciales:** clasificar PARTIAL con evidencia exacta de lo completado/pendiente; el ejecutor registra delta, no estado inventado.
13. **M — Abort:** condiciones de abort pre-escritas en el handoff (NO_GO material, quorum <5/5, Ceph nearfull agravado, secretos expuestos, target proof falla) con acción de detención segura.
14. **N — Rollback:** ruta de reversión por operación (snapshot/restore previo cuando exista, restauración de config, disable de timer); una mutación sin rollback identificable = CLASS 3 por definición.
15. **O — Recovery:** si la operación falla dejando el sistema degradado, aplicar el decision tree de recovery (07-integration § Dependencias) antes de reintentar; nunca recuperarse usando exclusivamente la superficie caída.
16. **P — Evidencia:** cruda fuera del vault (`~/aranea/work/<run>/`), con timestamps UTC, sin secretos; referencia canónica relativa en el vault; el ejecutor entrega la evidencia de EXECUTING→VERIFIED.
17. **Q — Handoff:** paquete reproducible (ver § Handoff abajo) entregado a la nota del proyecto ejecutor + change log; el estado queda `READY_FOR_EXECUTOR`.
18. **R — Criterio de aceptación:** definido por el proyecto ejecutor (su DoD); Ariadna NO certifica VERIFIED por cuenta propia; acepta/rechaza la evidencia como orquestador y registra.
19. **S — Actualización de Agents-OS:** al cierre, actualizar la nota del proyecto ejecutor (bitácora/estado), change log consolidado, y si correspondiera el índice 07-integration; cero secretos.

## Máquina de estados (contrato de routing y handoffs)

Estados que Ariadna puede alcanzar en preparación: `REQUESTED → DISCOVERED → SCOPED → {GATED | BLOCKED | READY_FOR_EXECUTOR}`.
Estados que exigen evidencia del proyecto ejecutor: `EXECUTING → {PARTIAL | FAILED | VERIFIED} → CLOSED`.
Convenciones: `REQUESTED` (solicitud recibida) → `DISCOVERED` (target/estado vivo leídos) → `SCOPED` (capacidades, riesgos y plan esbozados) → `GATED` (requiere owner gate, p.ej. CLASS 3) o `BLOCKED` (NO_GO material: capacidad, protección, autoridad ausente) o `READY_FOR_EXECUTOR` (handoff emitido). El ejecutor mueve los estados de ejecución; Ariadna los registra, nunca los fabrica. No existe base de datos de estados: los estados se escriben en el change log / bitácora de la operación usando estas etiquetas.

## Handoff — paquete mínimo reproducible

Todo handoff READY_FOR_EXECUTOR contiene: (1) necesidad y environment; (2) proyecto ejecutor y contrato aplicable (wikilink); (3) targets con identidad estable + estado vivo leído + timestamp; (4) capacidades/identidades/canales autorizados (referencias, sin secretos); (5) gates aplicables y owner decisions pendientes; (6) plan de ejecución propuesto con orden, precondiciones verificables, timeouts, abort; (7) rollback por paso; (8) criterio de aceptación sugerido (el ejecutor lo confirma); (9) evidencia de la preparación (probes, rutas `~/aranea/work/...`); (10) estado final REQUEST→READY_FOR_EXECUTOR con timestamps.

## Validación

- Una solicitud representativa resuelta con este contrato produce un handoff que un agente fresco puede ejecutar sin leer el chat original (golden G9 de H6; ver bitácora del proyecto).
- Negativos N1–N10 clasificados sin ejecutar operaciones (07-integration § Negativos H6).
- `AUTHORITY AVAILABLE ≠ EXECUTION AUTHORIZED` verificado en cada decisión; cero mutaciones en preparación.

## Rollback / recuperación

- Documental: revertir los archivos canónicos tocados (vault es canónico; el productor GitHub conserva historial).
- Operacional: si una preparación deja probes/sesiones abiertas, cerrarlas; ninguna preparación deja mutaciones (si las dejara, es una violación de este contrato y se registra como incidente del propio carril).

## Evidencia

- Golden H6 (G7) y continuidad (G9): `~/aranea/work/h6-integration-20260919/` (fuera del vault).
- Change log H6: `80-agents/journal/logs/2026-09-19-h6-integrated-autonomy-enablement.md`.
- Matriz de autoridad por nivel: [[HERMES — Infrastructure Operations]] § matrices H1–H5.
