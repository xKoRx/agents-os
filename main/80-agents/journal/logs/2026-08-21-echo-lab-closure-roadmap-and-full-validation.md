---
type: change_log
schema_version: 1
scope: session
created: "2026-08-21"
updated: "2026-08-21"
area: "[[Echo]]"
project: "[[Echo - Cierre del Lab y Limpieza del Journal]]"
application: "[[echo-core]]"
entities:
  - "[[Echo]]"
  - "[[echo-core]]"
  - "[[Echo - Discovery y Estado]]"
  - "[[Echo - Cierre del Lab y Limpieza del Journal]]"
related:
  - "[[2026-08-21-echo-north-documented-and-stage0-reaudit]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
---

# Echo: roadmap de cierre del Lab + validación completa de estado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created (2 notas nuevas) + updated (Discovery con correcciones mayores)
- **Archivo(s) nuevos:**
  - `10-projects/Echo/Echo - Cierre del Lab y Limpieza del Journal.md` — proyecto de ejecución (owner: me, P1): roadmap en 6 fases (D decisiones / G gate GO / E Etapa 10 / N calidad nativos / C contrato-robustez / S seguridad-ops) con 20 tareas.
  - `10-projects/Echo/Echo - Reporte de Estado Lab y Journal 2026-08-21.md` — reporte autocontenido (para evaluar con otra IA): contexto, historia de 3 generaciones, contrato vigente + extensiones no ratificadas, estado validado con evidencia, inventario de problemas (2 blockers, 8 warns/parciales), tensiones de diseño, roadmap y 6 preguntas para el evaluador.
- **Archivo(s) actualizados:**
  - `10-projects/Echo/Echo - Discovery y Estado.md` — correcciones validadas: `origin` fue reintroducido a propósito por 056 (la lee `mv_daily_operations`); universo de cuentas = 48 (el "2186 INACTIVE" era falso); vacío de Daily Ops explicado (ventana HWM 22:00–23:00 UTC + filtro ACTIVE que oculta 102/124 trades del día); gate script roto = **4** CTEs tipados (líneas 13/57/194/389), no 2; HEAD = `e25165ba`; 51 filas FAILED (migración 060 no registrada en el vault) y migraciones 058-060 incorporadas a la deuda; 052 dropeó solo 4 `lab_out_*`; tareas de ejecución redirigidas al proyecto nuevo; deuda conocida re-indexada a las tareas del roadmap.

## Motivo

- Pedido explícito del owner: "arma un proyecto con una serie de tareas para construir un roadmap para terminar de limpiar trade_journal y terminar lab tal como teníamos pensado; valida estado de producción y toda la mierda. Sin modificaciones de features — solo documentación, problemas, warnings, estados parciales. Reporte completo en el vault para evaluarlo con otra IA."

## Fuentes usadas

- Doble validación read-only 2026-08-21 (subagentes independientes): (a) prod — servicios/systemd/journalctl en `192.168.31.71`, psql en `192.168.31.220` (schema journal, gate original + corregido `summary|1|1|NO_GO`, pipeline lab, policies, matview/pg_cron, queries de ventana HWM), Hasura healthz; (b) repo — git/stash, migraciones 042-060 leídas, grep `origin`/`source_type`, consumidores front, writers legacy, RFCs, lab-worker, EAs, scripts deploy/build.
- Verificación directa del agente primario de los hechos load-bearing: CTEs tipados del gate (leído el archivo: `WITH required(name text)` en líneas 13/57/194/389), migración 056 (ADD COLUMN origin + matview que la lee), lista de prohibidas del gate (`comment` NO está), fechas git de migraciones clave (043+057 recién el 31-may — restructure final del pivot).

## Resolución aplicada

- Estado reconciliado con evidencia fresca; discrepancias entre fuentes resueltas a favor de la verificación directa (p.ej. un subagente reportó que el bug de CTEs no existía; la lectura del archivo primaria confirmó que sí, y la ejecución del script original en prod capturó el error exacto).
- Roadmap consolidado en un proyecto de ejecución separado del discovery (regla de no mezclar comprensión/cambio), con camino crítico G1→D1→G2→G4 para el GO del gate.

## Validación

- Gate corrido en prod (copia corregida en /tmp): `summary|1|1|NO_GO` — blocker `origin` FAIL_PRESENT único, warn policy_row_coverage 0% único, resto verde (38/38 columnas, GENERATED, constraints 11/11, event/recorded 100%).
- Script original corrido con ON_ERROR_STOP: `syntax error at or near "text"` (evidencia del blocker de tooling).
- Queries de cierre de la causa Daily Ops: trades de hoy por status de cuenta (22 ACTIVE / 102 INACTIVE), elegibilidad matview = 0, `daily_hwm_reset_at` de las ACTIVE = hoy 22:00–23:00 UTC.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos (IPs privadas del homelab mantenidas por consistencia con el resto del proyecto Echo)

## Rollback

- Borrar las dos notas nuevas, revertir las ediciones del Discovery y borrar este log.
