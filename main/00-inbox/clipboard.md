
## /execute

1. Limpieza administrativa concreta solicitada por Owner, antes de trabajo documental nuevo:
   - Rama a retirar, exclusivamente en xKoRx/agents-os: codex/btg-s02-design-cloud-20261006. Último tip leído00514fe65d0b4a06975096de17a3c2246d573c92.
   - El Manager verificó diseño reparado en master920012e, rama antigua aún existente y ningún PR asociado a ese head. El feedback original main/80-agents/journal/feedback/system-1/2026-10-06-echo-futures-btg-s02-session-feedback.md NO apareció en master; recuperar desde00514fe antes de eliminar la rama.
   - Refrescar y comparar los cambios exclusivos de esa rama. Preservar en master cualquier evidencia documental única necesaria, incluido feedback original, sin sobrescribir el diseño reparado ni feedback posterior. La versión inicial queda como historia explícitamente supersedida cuando sea necesario; no otra autoridad activa.
   - Publicar sólo el delta documental en master con protección frente a cambios concurrentes y readback. Después eliminar la ref remota nombrada verificando que siga en el tip revisado; si avanzó, revisar ese delta antes. Cerrar sólo un PR que efectivamente pertenezca a ese head si apareció. No tocar PR/branches de Echo ni otras ramas ajenas.
   - Verificar ausencia de la ref. Limpiar la ref local únicamente si no contiene trabajo nuevo/no es un checkout activo; no borrar worktrees ajenos. Sin force global, reset duro, merge de toda la rama, cambios de ACL ni nuevos backups en branches/tags.
   - El Manager CLOUD no pudo ejecutar la eliminación: no expone ese write. No asumir que ya ocurrió. Si tu autorización técnica tampoco permite hacerlo, devolver estado preciso y continuar trabajo de producto independiente.
2. Registrar este delta Owner en el documento de control/diseño vigente: objetivo engine correctness, módulos intercambiables y ROI fuera de alcance. Un único change log; sin otra ronda de arquitectura. Guardar este mandato por el contrato prompt de Agents-OS si corresponde.
3. Implementar la mínima separación de composición y configuración compartida; sustituibilidad y continuidad antes de ensamblar campañas.
4. Completar fuentes/ejecución causal existentes, ambos modos y exports; ejecutar pruebas focalizadas y los primeros BASIC/CAMPAIGN reales. No devolver sólo READY_TO_RUN.
5. Medir y corregir; entregar candidato a revisión del Primary para S04. No ejecutar ni autoadjudicar el adversarial independiente que corresponde al siguiente shot.

Cada especialista tiene tarea y archivos de ownership claros, ONE-SHOT, pruebas y cierre. No despachar un ejército de reviews repetidos por cada microparche. El lead integra dependencias y resultados; no confundir actividad de agentes con capacidad entregada.

## /verify

Mantener la matriz S02 aplicable: T01–T29, T31–T34, T37; T35/T36 sólo para atajos implementados; T38 acotada a parametrización. T30/holdout/ranking no pertenecen al gate actual. Pruebas de sensibilidad de ejecución sirven para detectar dependencia del modelo, no para elegir el recorrido de mayor PnL.

Añadir dos comprobaciones pequeñas y decisivas:
- Sustituir Strategy sin cambiar código del motor, con requisitos/timeframes/readiness del módulo correctamente respetados; también sustituir MM independientemente. Comparar los caminos runtime/backtest, no duplicar una implementación de prueba dentro del engine.
- Cambiar parámetros declarados de los módulos conserva engine idéntico y cambia la configuración efectivamente consumida; no basta editar un JSON que nadie lee.

Probar causalidad, fills/costos, adds adversos/pyramiding, no-adds explícito común, continuidad tras reemplazo, caja5000→4880, no quinto payout, gaps/DST/rollover y reproducción. Verificar pathways críticos y policy de coverage del repo; no pruebas de relleno.

Usar escenarios controlados para demostrar lifecycle incluso si la estrategia real pierde o nunca retira. No alterar señales para producir un payout histórico. Histórico auténtico es obligatorio para el resultado real, y fixtures no lo sustituyen.

Resultado por modo: code/build/config/manifest, rango/contratos, fidelidad, señales/operaciones/fills, PnL/costes/DD, estado residual y tiempo/memoria. CAMPAIGN añade compras, burns, funded, retiros cobrados/pendientes y caja. Evidencia de prueba de paridad identifica su alcance; no LIVE_EQUIVALENT sin soporte.

## /reuse

Usar interfaces, adapters, parsers, materializers, harness y oráculos existentes. Conservar regresiones que atrapen fallos. Un CLI/config reutilizable; no UI ni diseñador visual. Ninguna abstracción sin necesidad concreta dentro de S03–S05.

## /improve

Capturar fricción real o NONE. No editar skills generales por una observación, no producir un documento por microfix ni modificar Strategy/MM para mejorar profit.

## /close

Persistir evidencia compacta en master de Agents-OS bajo main/10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTG-S03-IMPLEMENTATION.md, actualizando control por delta. Materializar notas nuevas y validar paths cambiados con los contratos vigentes; no reconstruir contratos/templates parciales ni ejecutar higiene global ajena.

Todo worker ONE-SHOT, incluido este lead: artefactos, agents-os-agent-run-register cuando corresponde, feedback y agents-os-session-close con handoff. Skills: main/80-agents/skills/agents-os-agent-run-register/SKILL.md; agents-os-session-feedback/SKILL.md; agents-os-session-close/SKILL.md. No afirmar pasos inaccesibles ni uso de modelo/cuota no expuesto. Primary Manager sigue abierto.

S03 devuelve CANDIDATE_READY_FOR_PRIMARY_REVIEW, no aceptación final. S04 LOCAL independiente crea/ejecuta E2E para falsificar; S05 corrige y completa ambos resultados, sin S06. Bugs ordinarios se reparan; sólo bloqueos reales o contradicciones Owner se elevan con evidencia.

Handoff máximo10líneas:
STATE / CODE_SHA / AGENTS_OS_SHA =
BASIC_REAL =
CAMPAIGN_REAL / CASH_RECONCILIATION =
STRATEGY_AND_MM_SUBSTITUTION =
RUNTIME_PARITY_SCOPE =
SCALING / HISTORICAL_COVERAGE =
REPRODUCIBILITY / PERFORMANCE =
AGENTS_OS_OLD_BRANCH_CLEANUP = DELETED_VERIFIED | BLOCKED_WITH_REASON
MATERIAL_FINDINGS / ARTIFACT =
NEXT = S04_LOCAL_INDEPENDENT_ADVERSARIAL

Empieza por el estado real y ejecuta. No devuelvas otra propuesta de estrategia ni un plan de optimización de rentabilidad.
