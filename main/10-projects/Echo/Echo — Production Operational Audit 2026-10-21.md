---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Production Operational Audit 2026-10-14]]"
  - "[[Echo — Production Operational Audit 2026-10-13]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
aliases:
  - Echo PROD operational audit 2026-10-21
  - auditoria operacional Echo PROD 21-oct
tags:
  - kind/doc
  - area/echo
  - action/audit
created: "2026-10-21"
updated: "2026-10-21"
---

# Echo — Production Operational Audit 2026-10-21

## Propósito

Auditoría de regresión read-only solicitada por el owner ("necesito que hagas una auditoría completa a echo prod. está funcionando todo bien?"). Ejecutada 2026-10-21 ~11:49–11:58 UTC (miércoles, mercados abiertos). Ventana auditada: desde la auditoría del 14-oct ~23:30 UTC (~7 días). Regresión contra [[Echo — Production Operational Audit 2026-10-14]] (`OPERATIONAL_DEGRADED` por AUD-24 latente). Capacidades usadas: `aranea-ssh` (`echo-runtime-prod`, profile explícito desde la primera llamada), `aranea-postgres-ro`, `aranea-hasura-prod-ro`, `aranea-etcd-ro`, Loki/Prometheus (`aranea-observability-ro`).

**Veredicto: `OPERATIONAL_DEGRADED`.** El sistema opera correctamente end-to-end y la ventana trajo dos eventos de infraestructura (reboot del host `.71` el 20-oct y reinicio de PostgreSQL `.220` el 21-oct 09:24 UTC) que el sistema absorbió solo, con recuperación automática demostrada y sin impacto de datos visible. La copia E2E sigue funcionando con tickets reales en segundos, 17/17 terminales conectadas, 0 duplicados, config-flow entregando. La degradación es la misma de siempre, latente y sin causa: **AUD-24 sigue demostrado (TTP G5 `504079710` con 0 filas en `trade_journal` en toda la historia)** y su gate de regresión volvió a quedar sin ejercitar porque en la ventana no se copió ningún trade a G5.

## Respuesta directa: "¿está funcionando todo bien?"

Casi todo. Lo que el sistema hizo esta semana lo hizo bien: ciclos completos de copia con tickets y PnL journalizados, latidos de terminales al segundo, entregas de configuración tras el reboot, y ni un solo error de aplicación fuera de los 11 ERRORs transitorios del reinicio de PG de esta mañana (recuperados solos en minutos). Lo que no está bien es lo conocido: AUD-24 (journal de cuentas TTP 504xxxxx) sigue sin reparar ni diagnosticar, AUD-25 (triggers Hasura sólo en metadata viva) sigue latente, y las decisiones owner AUD-26/27/29 siguen abiertas. Ningún hallazgo nuevo de producto; los hallazgos nuevos de esta auditoría son de infraestructura y ambos cerraron solos (AUD-30).

## Eventos físicos de la ventana (nuevos vs baseline)

- **Reboot del host `.71` el 2026-10-20 (~18:1x UTC, evidenciado por boot del gateway 18:11 UTC):** PID 1 y todos los procesos con START `oct20`; los PIDs del 14-oct (core `441462`, gateway `442685`, functions `441170`, arranques 25-sep) desaparecieron. Los tres servicios Echo (`echo-core` PID 705, `echo-functions` PID 706, `echo-gateway` PID 707), nginx y promtail volvieron solos al boot ⇒ **resiliencia de arranque demostrada por primera vez con evidencia física** (las unidades quedaron habilitadas para boot, pero hasta hoy no había un reboot observado). No fue deploy: los binarios son los mismos paths `/home/kor/echo/*` y no hay despliegue registrado en la ventana.
- **Reinicio de PostgreSQL PROD `.220` el 2026-10-21 09:24:33 UTC** (`pg_postmaster_start_time`): el core registró 11 ERRORs entre ~09:21 y ~09:24 UTC (`position_sync: failed to delete closed positions` / `account_sync: bulk update failed` con "database system is shutting down" → connection refused → connection reset). Reconexión automática inmediata: legs REF journalizadas a las 09:23, 09:32 y 11:00 UTC, latidos de cuentas al segundo, 7 backends app y `xact_commit` 6,05M al momento de la auditoría. Sin FAILED nuevos, sin huecos visibles en el journal. Causa del reinicio desconocida desde este perfil (ver AUD-30).
- **Delta de listeners:** el efímero conocido `:45021` (AUD-23) desapareció con el reboot y apareció otro efímero sin dueño visible `*:36387` (misma clase: procesos de `kor` no atribuibles por `ss` como `echo-dev`; benigno-sospechado, no demostrado).

## Cadena de evidencia (traza 2026-10-20 14:27 UTC, trade_id `01a15a5a-70d8…`)

1. **Señal viva:** master `2089125533` REF NDX BUY 1.10, ticket `270643013`, creada 14:27:20 (opened_at 17:27 hora broker UTC+3).
2. **Copia física:** leg EXECUTION `80577453` NDX BUY 1.96, ticket real `64164304`, creada 14:27:21 (**1 s** después del master).
3. **Cierres con PnL:** copia cerrada 15:34:42 (−216.19); master cerrado hoy 21-oct 08:07:39 (+466.38) — ciclo completo journalizado.
4. **Volumen de la ventana (14→21 oct):** 67 legs EXECUTION CLOSED + 130 REF CLOSED + 1 EXECUTION FAILED; hoy 21-oct ya hay 5 REF abiertas (masters GDAXI/NDX) y el flujo de ingesta post-reinicio-PG demostrado.
5. **Copias por cuenta en la ventana:** 11 cuentas recibieron legs EXECUTION, todas con ticket≠0 salvo el FAILED 4109 aislado (ver G8). **G5 (`504079710`): 0 copias en la ventana.**
6. **Latidos:** 17 cuentas ACTIVE con `updated_at` al segundo (última 11:52:51 UTC); `lab_job_runs` última corrida 11:50:50 UTC (lab-worker vivo post-reboot); Prometheus `echo_bridge_executions_connected=1` en las 17 terminales (mt4-ttp ×5, mt4-ftmo ×2, mt4-real ×10).

## Gates

| Gate | Estado | Justificación |
|---|---|---|
| G1 runtime | PASS | Host `echo`, uid `echo-dev`; core (705), functions (706), gateway (707), nginx, promtail vivos con arranque oct-20 (reboot); listeners 80/8080/8090/9080/9090 + efímero `:36387` (clase AUD-23, dueño no visible); 0 `echo-bridge` en `.71` (normal, corren en Windows) |
| G2 identidad | PASS | Binarios `/home/kor/echo/*` re-arrancados por systemd al boot (no deploy); `service.version=2.0.0` y `deployment.environment=production` en logs de hoy; SHA exacto UNKNOWN declarado (viewer no lee `/home/kor/echo`) |
| G3 config | PASS | ETCD `/echo/production/` = 37 keys (idéntico al baseline 14-oct); Kafka `.247-.249`, gateway core `localhost:9090`; sin filtración DEV observada |
| G4 servicios | PASS | PG `echo` con 7 backends app y 6,05M commits; Hasura v2.38.0 con metadata consistente (0 inconsistentes); Loki/Prometheus/etcd consultados OK; PG mismo se reinició hoy 09:24 UTC (AUD-30, recuperado) |
| G5 transporte | PASS | Traza REF→EXEC en 1 s con tickets reales (20-oct); cierres con PnL journalizados; 17/17 terminales conectadas post-reboot; ingesta viva después del reinicio de PG (legs 09:23/09:32/11:00 UTC); lag de consumer groups = EVIDENCE_GAP (sin Kafka PROD) |
| G6 datos | PASS | Journal al segundo del evento; 0 duplicados `(trade_id, account_id)`; 1 FAILED en 7 días (4109, ticket 0, 15-oct — patrón benigno AUD-17, acotado) |
| G7 consistencia | PASS | 0 `active_positions` vs 7 legs OPEN en journal: 5 REF vivas de hoy (masters, patrón conocido: los masters INACTIVE no snapshot-ean posiciones) + 2 reliquia jun-04 (AUD-28 pendiente). Sin divergencias nuevas |
| G8 trading | PASS | E2E completo en la ventana con tickets y PnL; WARNs del planner trazan 1:1 a Slaves ARCHIVED (GDAXI `2089126183`/`2089126186`, exclusión correcta); cierre REF sin copias = "no open executions found" benigno por diseño de whitelist; FAILED 4109 aislado y acotado |
| G9 observabilidad | PASS | Core 3 h: 11 ERRORs (todos del reinicio PG de hoy, AUD-30) + 23 WARNs (todas exclusiones/cierres benignos, verificadas por label `level`); bridge 6 h: 0 WARN + 0 ERROR; gateway en silencio event-driven normal (30 líneas/24 h = bootstrap de arranque) |
| G10 cambios | PASS | `origin/master` avanzó `372af59a`→`d74b6525` (16-oct, docs tradesgerard; sin deploy PROD — el rollout vigente sigue siendo el del 25-sep); trabajo posterior en ramas feature (futures-pools/fefb-s01/challenge-history, producto DEV/backtest); ETCD sin mutación observable; deltas físicos = reboot `.71` + restart PG `.220`, ambos con recuperación automática. Nota de higiene: `master` local divergido (tip `3596fc48` del 22-sep sin push vs origin `d74b6525`) |
| G11 config-flow | PASS (con gaps estructurales) | Post-reboot el gateway re-bootstrappeó los 6 automation profiles a Kafka (18:11 UTC 20-oct, `AutomationWebhook: bootstrap complete`); terminales conectadas y operando con símbolos transformados; `hdb_catalog.event_log` sin permiso RO = EVIDENCE_GAP estructural; AUD-25 re-verificado VIGENTE |
| G12 estado | PASS (con hallazgos conocidos) | 17/17 ACTIVE con latido de segundos; cobertura `client_allowed_symbols`→`symbol_mappings` = 0 gaps; 1 cuenta ciega re-confirmada (3094610, AUD-29); 305 policies muertas hacia ARCHIVED/INACTIVE (idéntico al baseline, peso muerto conocido); zombies de topic sin verificación directa = EVIDENCE_GAP (sin Kafka PROD) |

## Hallazgos

- **AUD-24 (P1 — VIGENTE, latente): TTP G5 MT5 (`504079710`) sigue sin journalizar.** Re-verificado hoy 11:52 UTC: 0 filas all-time; la cuenta late fresco (11:52:51), está `ACTIVE`, conectada en Prometheus (`mt4-ttp`), equity=balance 50.471,74 (sin PnL flotante, sin posiciones). En 7 días no recibió ninguna copia (0 legs EXECUTION), así que el gate de regresión (próxima copia ⇒ fila con ticket≠0) volvió a quedar sin ejercitar, igual que el 14-oct. Causa sigue en hipótesis (wiring del path de journal para cuentas 504xxxxx). **Owner:** diagnosticar/repair antes de que el master vuelva a copiar a G5; cada copia mientras tanto nace huérfana (sin gestión activa ni PnL auditable).
- **AUD-25 (P2 — VIGENTE, re-verificado hoy): el fix de triggers vive sólo en metadata viva.** `v3/hasura/` del repo sigue sin `event_triggers` ni header `Authorization` (grep 0 matches hoy). Riesgo agravado por la divergencia del `master` local (tip `3596fc48` sin push): un apply desde este repo seguiría reproducindo el incidente del 12-oct. **Owner:** persistir triggers+header en el repo o blindar el runbook de apply; de paso resolver el destino del commit local `3596fc48` (push o revert).
- **AUD-26 (P3 — VIGENTE, re-verificado hoy): `magic_260104001` sigue con 0 policies** y su última señal fue el 19-oct 10:15 UTC — sigue señalizando y sigue reference-only por defecto de config, no por decisión demostrada.
- **AUD-27 (P3 — VIGENTE, re-evidenciado hoy): estrategias con camino de copia muerto.** Las 4 REF GDAXI abiertas hoy en el master `2089125371` generaron WARNs "intent rejected by account state (ARCHIVED)" hacia `2089126183`/`2089126186` — el motor excluye correctamente, pero la estrategia no copia a nadie. Mismo tratamiento owner que el 14-oct: dar targets o aceptar reference-only explícito.
- **AUD-28 (P4 — VIGENTE): legs reliquia jun-04** (`802591` ticket `26790904` USDJPY y `442688` ticket `26790522` NDX) siguen OPEN en journal en cuentas hoy ARCHIVED; residuo contable, limpieza owner pendiente.
- **AUD-29 (P3 — RE-CONFIRMADO): Axi Select (`3094610`) sigue ciego** (ACTIVE execution_agent, 0 filas en `account_strategy_risk_policy`) y sigue operando nativo: sus 5 legs de la ventana journalizan con ticket≠0 y PnL. Requiere decisión owner explícita (policies o archivar).
- **AUD-30 (P4 — NUEVO, cerrado por sí solo): reinicio de PostgreSQL PROD `.220` hoy 09:24:33 UTC sin causa conocida.** Evidencia: `pg_postmaster_start_time` + 11 ERRORs del core durante la caída (shutting down → connection refused). Recuperación automática limpia del core en minutos, sin FAILED ni huecos de datos visibles. **Owner:** confirmar si fue mantención programada; si no lo fue, averiguar quién/cué reinició. **Gate de regresión:** el core reconecta solo tras un restart de PG (demostrado hoy — patrón ya certificado en DEV 2026-09-21).
- **AUD-23 (carry-over, actualizado): el efímero `:45021` desapareció con el reboot** y hoy hay otro efímero sin dueño visible `*:36387`. Misma clase benigna-sospechada; sin evidencia de riesgo.
- **Positivos de regresión:** AUD-17 (4109) se mantiene esencialmente cerrado (1 evento aislado en 7 días, patrón histórico conocido); el incidente de triggers sigue reparado en runtime (bootstrap post-reboot entregó a Kafka); AUD-19 (masters INACTIVE journalizando REF) persiste benigno; flota 17/17 estable; **resiliencia de boot demostrada** — primer reboot observado de `.71` con los tres servicios Echo levantándose solos.

## EVIDENCE_GAPS

`hdb_catalog.event_log`/`event_invocation_logs` sin permiso del perfil RO (la entrega se demostró funcionalmente por el bootstrap del gateway post-reboot y por terminales operando). Lectura directa del topic compactado, lag de consumer groups y zombies post-purga en Kafka PROD (sin capability). Causa raíz de AUD-24 (requiere inspección de código/config del core o logs del terminal TTP). SHA de binarios en `.71` (viewer). Causa del reinicio de PG `.220` (AUD-30) y del reboot de `.71` del 20-oct (fuera de alcance del perfil viewer; el owner conoce la mantención del 20-oct por la caída de grinds del host). Dueño del efímero `:36387` (procesos de `kor` no atribuibles desde `echo-dev`). Inspección directa de terminales Windows (nunca se ejecuta desde esta auditoría).

## Conclusión

Echo PROD está operando limpio de punta a punta y, dato nuevo de esta semana, demostró resiliencia ante dos eventos de infraestructura real: el reboot del host (20-oct, servicios de vuelta solos) y el reinicio de PostgreSQL (21-oct 09:24 UTC, reconexión automática sin pérdida visible). La copia E2E cierra su ciclo con tickets y PnL, las 17 terminales laten y el config-flow entrega. El veredicto sigue siendo `OPERATIONAL_DEGRADED` por la misma razón de siempre: AUD-24 permanece demostrado y sin causa, ahora con 7 días adicionales sin poder ejercitar su gate de regresión (G5 no recibió copias). La agenda owner no cambió: diagnosticar el journal de las cuentas 504xxxxx antes de la próxima copia a G5, persistir los triggers Hasura en el repo (AUD-25), y decidir AUD-26/27/29 (targets o reference-only explícito). Nueva acción menor: confirmar que el reinicio de PG de esta mañana fue intencional (AUD-30).
