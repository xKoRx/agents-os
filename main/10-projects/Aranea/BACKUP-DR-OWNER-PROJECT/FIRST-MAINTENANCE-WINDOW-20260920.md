---
type: doc
schema_version: 1
status: active
icon: 🗓️
slug: aranea-first-maintenance-window-20260920
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[OPERATING-STATE-20260920]]"
  - "[[PLACEMENT-DECISIONS-20260920]]"
  - "[[ROADMAP-WP-BACKUP-DR]]"
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
aliases:
  - First Maintenance Window 2026-09
  - Ventana 26-09 P0
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
created: "2026-09-20"
updated: "2026-09-21"
---

# 🗓️ FIRST-MAINTENANCE-WINDOW — 2026-09-20

## Propósito

- Primera ola de mantenimiento concreta tras el cierre de mercado. **Cierre operativo REAL de Echo, medido desde sus datos** (echo.trade_journal, PG 152 vía RO, 20sep): último trade **cerrado vie 18sep 17:59 -03**; el dom 20sep (hoy) se abrieron 2 operaciones en la sesión vespertina (última apertura dom 21:36 -03). El mercado NO equivale a ventana disponible: la primera ventana segura es **sábado 26-09 02:00-07:00 -03** (fuera de sesiones abiertas, antes del run del domingo-noche, después del último ciclo R2 del viernes 25sep), **siempre que no queden posiciones abiertas sosteniendo el fin de semana** (el mercado siempre cierra viernes; lo que importa es la ausencia de posiciones vivas — el precheck lo verifica sin filtro temporal). Ventana de respaldo: dom 27-09 madrugada SOLO para acciones que no toquen guests de trading.

> [!warning] Errata y dependencias (2026-09-21, cierre documental — el cuerpo original del 20sep se conserva)
> 1. **W1/W2 a pool2 son PROPUESTAS con ficha, no destinos aprobados**: pool2 es single-disk (F-14) y comparte chasis con pool0; su valor es separar el dominio de falla del SO edge, NO redundancia. Ejecución = gates del §Bloqueantes (alta `nfs-pool2` + ventana 019); W3/W4/W5 igualmente no aprobadas en bloque.
> 2. **Dependencia D↔R2 resuelta explícitamente**: el run R2 del 21sep 06:05 no ocurrió (hermes apagada 01:09-07:36) → la serie es 3/7 NO consecutiva y el criterio "7/7 con verify ok" es inalcanzable. La decisión D de P0-1 se toma con el criterio alternativo ya definido en MANDATO-P0: **6/7 runs OK + OK owner con CAPACITY-METRICS re-medidas 25-26sep**. Si el owner no acepta el criterio alternativo, P0-1 se difiere a su decisión (la ventana continúa con K2/K1/P0-2 según gates).
> 3. **VM125**: encendida el 20-09 18:54:44 en hades (el uptime ≥42d era del nodo, no del guest); es el escritor identificado por K2. Cualquier referencia de uptime de la matriz/Operating State para 125 queda corregida en [[K2-CEPH-RISK-20260920]] (errata 21sep).
> 4. **Cierre operativo de Echo (vie 25) = comprobación + prevención**, no supuesto: query sin filtro temporal `SELECT count(*) FROM echo.trade_journal WHERE closed_at IS NULL;` = 0 + prevención de nuevas entradas (decisión del owner sobre su plataforma; el agente verifica y registra en el preflight GO/NO_GO).
> 5. `pct move-volume` elimina el volumen origen; la conservación del origen de cada CT es el **vzdump previo verificado del paso 1** (ningún `--delete` ni borrado autorizado por defecto).

## Contenido

---
### 8.2 Plan de ejecución consolidado post-redirección D-NEW (21sep noche — vigente; el P0 del 20sep queda como registro histórico, su P0-2 CANCELADO)

**DAG de organización** (autoridad: [[STORAGE-ORGANIZATION-FREEZE]]): 1. Decisiones placement ([[PLACEMENT-DECISIONS-20260920]] §F) → 2. Reservas y capacidad ([[CAPACITY-AND-RESERVATIONS]]; re-medición en cada preflight) → 3. Preparación de destinos (payloads réplica, diff nfs-vmbackup, W-01 PBS) → 4. Protección previa por operación (fixture G-REP-0 / vzdump verificado) → 5. Operaciones justificadas → 6. Validación de servicios → 7. Certificación ([[MANDATO-CERTIFICACION-SPEC]]) → 8. `STORAGE_ORGANIZATION_COMPLETE` CIERRA la optimización de storage (corrección noche-5: los jobs Backup/DR corren por sus propios gates G-B1/G-NFSVM/G-REP-0..5 y NO esperan este paso; las migraciones exigen BACKUP_BASELINE_VERIFIED por unidad).

**Viernes 25sep (cierre operativo Echo + preflight)**: 10 checks W-04 (fail-closed, GO/NO_GO por intervención) + **MIGRATIONS_NOT_READY declarado** (ninguna migración preparada pasa al sábado; no se inventan operaciones para el calendario) + cierre real de Echo (query trade_journal sin filtro temporal = 0 + prevención de nuevas entradas, acción del owner) + re-medición CAPACITY-METRICS + `ceph osd df` (K2) + verify PBS.

**Sábado 26sep (ventana 02:00-07:00 si gates)**: prechecks → K2 (RO) → K1 (ARGUS, AUTO-with-diff, **PENDIENTE_GO owner** — muta Prometheus 160: sin OK, la ventana continúa) → P0-1 (W-01 PBS growth, gates D1+P1-1+019) — **sin P0-2** (cancelado). Sin W1/W2, sin réplica-full ese día (la 1ª transferencia 2,35T va en ventana EXCLUSIVA propia, G-REP-3: madrugada sáb-dom propuesta, Echo cerrado, sin B1-fulls/G1B/migraciones sobre TrueNAS).

**Dependencias duras**: Echo/PG/Mongo/MinIO conservan condiciones propias de disponibilidad y recuperación (dumps G1A ya diarios, G1B certificado) — ninguna depende de esta ventana. Ceph: separar K1/K2 (lecturas) de S2 (compact/mClock, carril Ceph, otra ventana). I/O TrueNAS jamás compartido: réplica-full ∥ B1-fulls ∥ G1B ∥ migraciones = PROHIBIDO simultáneo (regla MANDATO 2/4/5).

**Paralelizables sin riesgo**: carril documental/prep ∥ diagnóstico kafka P1-4 (RO) ∥ operación Echo. Nunca simultáneo: TrueNAS/pool0 (réplica ∥ vm-backup-full ∥ scrub), Ceph (W5 ∥ S2), edge (una intervención a la vez).

---

### Reglas de la ventana

1. Una sola operación mutante a la vez en componentes que comparten recuperación: nunca simultáneo sobre TrueNAS/pool0 (A6-full ∥ W1), nunca sobre Ceph (W5 ∥ S2), nunca sobre el edge (W2 aislado).
2. ABORT de cada intervención con su condición explícita; ABORT global si HEALTH_ERR de Ceph, si un restore falla dos veces, o si Echo no valida post-cambio.
3. Duración total objetivo 5h (02:00-07:00). Presupuesto realista: prechecks 15 min + K2 20 min + K1 30 min + P0-1 40 min + P0-2 hasta 3,5h (extrapolación conservadora: los vzdumps del piloto midieron CTs chicos, 13-39 s; obsidian-sync ~64G puede tomar 20-40 min de restore) ≈ 4h45-5h: margen corto — si P0-2 no alcanza, se corta por CT completo (cada CT es independiente) y el resto va a la ventana 2.
4. Todo lo GATED exige el OK owner de la semana (bloqueantes §Bloqueantes); sin OK, esa intervención no arranca y la ventana continúa con las AUTO.
5. Vuelta a operación normal: validar Echo vivo (freshness de métricas ARGUS <60s o, si hay sesión abierta, intents fluyendo) + verify PBS TASK OK + timers R1/R1.5/A1 armados + **R2 exceptuado por expiración natural el 26sep (validar su último run 06:05 OK y el retiro del timer, no que siga armado)**.
6. Coexistencia de timers dentro de la ventana (declarado, no accidental): A1 dumps 03:00/03:20 con ingesta a PBS y el último ciclo R2 06:05 corren DURANTE la ventana. Son operaciones congeladas y no-mutantes para P0; P0-1 (resize PBS) se ejecuta después de 03:45 para no solapar con la ingesta A1; el run R2 06:05 corre sobre el datastore ya crecido y su OK es parte de la validación de P0-1.
7. Canal de validación independiente del plano migrado: las verificaciones de cierre (Prometheus/ARGUS) se hacen por curl directo a 160 desde hermes/athena, NO por los MCPs servidos en 113 (que estará recién movido).
8. Orden de ejecución: **K2 → K1 → P0-1 → P0-2** (K2 es RO puro y consume telemetría que K1 aún no reinició; K1 activa instrumentación que P0-1/P0-2 usarán para validar).

### Clasificación

- **P0 (26-09 02:00-07:00)**: K2, K1, P0-1, P0-2 (en ese orden; ver regla 8).
- **P1 (siguientes ventanas / semana, sin ventana)**: P1-1..P1-5.
- **P2 (diferido)**: P2-1..P2-4.

### P0 — Sábado 26-09 02:00-07:00

| ID | Servicio | Problema | Preflight | Operaciones exactas (orden) | Duración y fundamento | Riesgo | Downtime | Rollback | Validación | Gate owner | DoD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | ARGUS 160 | 865 series de plataforma sin muestras: sin visibilidad Ceph/kafka/pve | MCP observability RO lista datasources (OK hoy); identidad del exporter en 160 via management path RO existente | (1) identificar exporters declarados vs scraping en Prom; (2) activar scrape faltante en la config de Prometheus (160); (3) refresh targets; (4) confirmar `ceph_*`/`kafka_*` con muestras | 30 min (edición config conocida + restart del stack de recolección; NO toca 127) | bajo: capa de recolección, no datos | 0 (sólo ARGUS recolección, breves gaps de ingest) | revert config Prometheus (diff guardado) | series con samples en Prom + series Ceph visibles | ninguno — AUTO (master plan §4 observabilidad); **NO es RO**: muta config de recolección en 160 y reinicia el recolector | instrumentación Ceph/kafka/pve visible en ARGUS |
| K2 | Identificación escritor pool1 | growth ~+17G/OSD/día con nearfull 87,8%: sin causante identificado | evidencia diskwrite por guest ya capturada 20sep (`pve-live.txt`); ceph osd df antes/después | (1) snapshot métrico pre (`ceph osd df` + /cluster/resources); (2) correlacionar diskwrite guest vs growth RBD por imagen (`rbd du` desde hera con `cluster addr` correcto o stats OSD); (3) emitir lista ordenada de escritores | 20 min (sólo lectura) | cero (RO) | 0 | n/a | lista de escritores con GB/día estimado | ninguno | informe de escritores pool1 en el workspace de la ventana |
| P0-1 | PBS datastore | piloto R2 día 7/7: sin decisión D formal = sin producción vzdump (riesgo: seguir sin imagen-level T0) | CAPACITY-METRICS re-medidas 25-26sep (regla D3.1); verify 6/7 TASK OK al precheck (el 7º run dispara 06:05 en ventana y se valida en cierre; criterio alternativo: 6/7 + OK owner con métricas 25sep); datastore 17% | (1) owner decide D con las métricas frescas; (2) si GO: retención final definida + grow disk scsi1 180 +300G (vg local-kronos 567G libres) + resize2fs en PBS (online) + umbral 70% documentado; (3) ejecutar DESPUÉS de 03:45 (fin ingesta A1) y dejar el run R2 06:05 correr sobre el datastore crecido; (4) timer R2 se retira por expiración natural (26sep) | 40 min (grow + resize online; PBS sigue arriba) | medio-bajo: resize filesystem en vivo, mecanismo estándar | 0 (PBS activo) | restaurar tamaño no es posible sin volver a crear el disco → mitigación: la operación es aditiva; rollback = desactivar jobs nuevos, no revertir disco | df 595G + verify TASK OK post-resize + run R2 06:05 OK + timer A1/R1 intactos | OWNER (decisión D-piloto, bloqueante #5) | PBS 595G con retención final y decisión D documentada |
| P0-2 | edge storage (W1) | rootfs de 4 CTs edge (113/103/116/137) + ISOs + discos ide0 MT4/labs comparten el export pool0 (mismo dominio de falla que los datos T0) | vzdump fresco VERIFICADO de los 4 CTs — **103, 116, 137 Y 113 (ninguno está en el piloto R2)**; dataset+export pool2 creados en TrueNAS (canal DDP); alta de storage NUEVO preparada con owner ANTES de la ventana | (1) crear dataset+export NFS pool2; (2) alta del storage `nfs-pool2` en storage.cfg (pmxcfs: UNA edición, replicada 5/5); probar mount; (3) stop CT 103 → `pct move-volume 103 rootfs nfs-pool2` (vzdump previo verificado; fallback vzdump+`pct restore`) → start → validar servicio; (4) repetir 116, 137, 113 (mcps al final: es el plano de acceso del agente y las validaciones usan canal alterno); (5) **`nfs-storage` NO se toca** — verifica al cierre que MT4 (ide0), labs e ISOs siguen intactos en pool0 | 3-3,5h para 4 CTs escalonados (15-25 min/CT; obsidian-sync ~64G hasta 40 min de restore; fundamento: piloto midió vzdump CT chico 13-39s, restore domina) | medio: toca rootfs de 4 CTs edge; ISOs/MT4/labs NO se mueven | por CT: 15-25 min (emqx/vault/frigate/mcps) | re-restore desde el vzdump previo al backend original (<10 min/CT chicos; 116 hasta 40 min) | servicio de cada CT vivo post-arranque (5984 vault, UI frigate, MQTT 1883, mcps containers vía management path) + `nfs-storage` intacto (MT4 ide0 + ISOs visibles) | OWNER: alta storage nuevo en storage.cfg + ventana 019 (bloqueantes #1/#2) | 4 CTs con rootfs en nfs-pool2, servicios validados, `nfs-storage` sin cambios |

- **Prohibiciones P0**: no tocar Echo/MT4/kafka guests (las migraciones W2-W5 van a la ventana 2 con sus gates); no ejecutar A6-REPL full (I/O TrueNAS compartido con W1); no compact/mClock (carril Ceph, ventana separada).

### P1 — siguientes ventanas (26-09 tarde / semana del 28-09)

| ID | Servicio | Problema | Operaciones | Dependencias | Gate | Duración |
|---|---|---|---|---|---|---|
| P1-1 | Echo 140 SO → hades local-lvm (W5 fase 1) | SO reconstruible en pool1 nearfull | vzdump offline 140 → restore a local-lvm hades → arranque → verificación app completa (arranque limpio + sesiones reconectadas + freshness de métricas; NO se exige intent de mercado con el mercado cerrado) | D-piloto GO + 018 + B1 mecanismo + ventana con Echo cerrado | OWNER | 30-40 min |
| P1-2 | W2 traefik 115 → nfs-pool2 | SPOF edge en athena | mismo mecanismo P0-2 aplicado a 115 + prueba arranque nodo alterno | W1 hecho (P0-2) | OWNER | 30 min |
| P1-3 | W4 kafka 128 hera→athena | broker del pipeline Echo en host Ceph | diagnóstico previo del brote (ver P1-4) + vzdump 128 + migración offline 5 min | diagnóstico del brote sin causa abierta | OWNER | 15 min |
| P1-4 | Diagnóstico brote kafka bridges | +147 err/h en bridges 20sep | correlación logs kafka 128 vs errores métricas; verificar ISR de kafka-hera/kronos/zeus (canal a definir) | canal RO a 128/guests kafka | ninguno si hay canal | 1h |
| P1-5 | W5 fases 2-3 (MT4s, SOs PG/Mongo/MinIO) | resto de down-tier pool1 | igual que P1-1, escalonado | P1-1 exitoso + espacio PBS post-P0-1 | OWNER | 2-3 ventanas |

### P2 — diferido (sin urgencia operacional)

| ID | Tema | Nota |
|---|---|---|
| P2-1 | W3 pi-hole | depende de decisión retiro/reactivación (WP-B2); si retiro → decomisión formal |
| P2-2 | A6-REPL full + scrub pool2 | ventana propia con I/O TrueNAS exclusivo (post-W1); gates 018/019 |
| P2-3 | S2 mClock+compact | carril Ceph, ventana dedicada, tras K2 (necesita línea base de escritores) |
| P2-4 | mcps docker prune + 132/125 regularización | mutaciones menores gated; oportuno en cualquier ventana corta |

### Bloqueantes owner estrictamente necesarios para P0

1. **OK D-piloto** con métricas del 25-26sep (habilita P0-1) — ya está calendarizado como decisión del 28sep; adelantarla a la ventana o ejecutar P0-1 cuando el owner decida.
2. **Alta del storage `nfs-pool2` aprobada** (dataset+export pool2 y una edición pmxcfs; `nfs-storage` NO se toca) + **ventana 019 declarada** (sáb 26sep 02:00-07:00) — habilita P0-2.
3. K1/K2 no requieren gates.

### Mandato de ejecución P0

- Preparado y NO ejecutado en: `~/aranea/work/first-window-20260926/MANDATO-P0.md` (autosuficiente: authorities, preflights fail-closed, operaciones en orden, ABORT, validación por paso, rollback, cierre). Estado: BORRADOR esperando los gates del owner; el mandato NO se ejecuta sin ventana 019 formal.

## Fuentes

- [[OPERATING-STATE-20260920]] (hallazgos: kafka brote, Ceph growth, mcps 83%), [[PLACEMENT-DECISIONS-20260920]] (fichas W1-W5), [[ROADMAP-WP-BACKUP-DR]] (D-piloto, A6, B1), [[MASTER-PLAN-STORAGE-BACKUP-DR]] (§4 ventana, §5 bloqueantes), `~/aranea/work/first-window-20260926/`.
