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
updated: "2026-09-20"
---

# 🗓️ FIRST-MAINTENANCE-WINDOW — 2026-09-20

## Propósito

- Primera ola de mantenimiento concreta tras el cierre de mercado. **Cierre operativo REAL de Echo, medido desde sus datos** (echo.trade_journal, PG 152 vía RO, 20sep): último trade **cerrado vie 18sep 17:59 -03**; el dom 20sep (hoy) se abrieron 2 operaciones en la sesión vespertina (última apertura dom 21:36 -03). El mercado NO equivale a ventana disponible: la primera ventana segura es **sábado 26-09 02:00-07:00 -03** (fuera de sesiones abiertas, antes del run del domingo-noche, después del último ciclo R2 del viernes 25sep). Ventanas de respaldo: dom 27-09 madrugada SOLO para acciones sin tocar guests de trading; si el mercado cierra viernes, reconfirmar con este mismo query.

## Contenido

### Reglas de la ventana

1. Una sola operación mutante a la vez en componentes que comparten recuperación: nunca simultáneo sobre TrueNAS/pool0 (A6-full ∥ W1), nunca sobre Ceph (W5 ∥ S2), nunca sobre el edge (W2 aislado).
2. ABORT de cada intervención con su condición explícita; ABORT global si HEALTH_ERR de Ceph, si un restore falla dos veces, o si Echo no valida post-cambio.
3. Duración total objetivo 5h (02:00-07:00); las intervenciones P0 caben con holgura; P1/P2 NO entran.
4. Todo lo GATED exige el OK owner de la semana (bloqueantes §Bloqueantes); sin OK, esa intervención no arranca y la ventana continúa con las AUTO.
5. Vuelta a operación normal: validar Echo vivo (sesiones + 1 intent de mercado o freshness de métricas) + verify PBS TASK OK + timers R1/R1.5/R2 intactos.

### Clasificación

- **P0 (26-09 02:00-07:00)**: K1, K2, P0-1, P0-2.
- **P1 (siguientes ventanas / semana, sin ventana)**: P1-1..P1-5.
- **P2 (diferido)**: P2-1..P2-4.

### P0 — Sábado 26-09 02:00-07:00

| ID | Servicio | Problema | Preflight | Operaciones exactas (orden) | Duración y fundamento | Riesgo | Downtime | Rollback | Validación | Gate owner | DoD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | ARGUS 160 | 865 series de plataforma sin muestras: sin visibilidad Ceph/kafka/pve | MCP observability RO lista datasources (OK hoy); identidad del exporter en 160 via management path RO existente | (1) identificar exporters declarados vs scraping en Prom; (2) activar scrape faltante en la config de Prometheus (160); (3) refresh targets; (4) confirmar `ceph_*`/`kafka_*` con muestras | 30 min (edición config conocida + restart del stack de recolección; NO toca 127) | bajo: capa de recolección, no datos | 0 (sólo ARGUS recolección, breves gaps de ingest) | revert config Prometheus (diff guardado) | series con samples en Prom + 1 query `ceph_osd_utilization` visible | ninguno (WP-S4 READY, RO-safe) | instrumentación Ceph/kafka/pve visible en ARGUS |
| K2 | Identificación escritor pool1 | growth +19G/OSD/día con nearfull 87,8%: sin causante identificado | evidencia diskwrite por guest ya capturada 20sep (`pve-live.txt`); ceph osd df antes/después | (1) snapshot métrico pre (`ceph osd df` + /cluster/resources); (2) correlacionar diskwrite guest vs growth RBD por imagen (`rbd du` desde hera con `cluster addr` correcto o stats OSD); (3) emitir lista ordenada de escritores | 20 min (sólo lectura) | cero (RO) | 0 | n/a | lista de escritores con GB/día estimado | ninguno | informe de escritores pool1 en el workspace de la ventana |
| P0-1 | PBS datastore | piloto R2 día 7/7: sin decisión D formal = sin producción vzdump (riesgo: seguir sin imagen-level T0) | CAPACITY-METRICS re-medidas 25-26sep (regla D3.1); verify 7/7 TASK OK; datastore 17% | (1) owner decide D con las métricas frescas; (2) si GO: retención final definida + grow disk scsi1 180 +300G (vg local-kronos 567G libres) + resize2fs en PBS + umbral 70% documentado; (3) timer R2 se retira por expiración natural (26sep) | 40 min (grow + resize online; PBS sigue arriba) | medio-bajo: resize filesystem en vivo, mecanismo estándar | 0 (PBS activo) | restaurar tamaño no es posible sin volver a crear el disco → mitigación: la operación es aditiva; rollback = desactivar jobs nuevos, no revertir disco | df 595G + verify TASK OK post-resize + timer A1/R1 intactos | OWNER (decisión D-piloto, bloqueante #5) | PBS 595G con retención final y decisión D documentada |
| P0-2 | edge storage (W1) | rootfs de 4 CTs T0-edge + ISOs en pool0 (mismo dominio de falla que los datos) | vzdump fresco de 103/116/137 (113 ya cubierto); export pool2 creado en TrueNAS (canal DDP); diff storage.cfg preparado con owner ANTES de la ventana | (1) crear dataset+export NFS pool2; (2) probar mount desde un nodo; (3) stop CT 103 → pvesm move-volume o vzdump+restore al nuevo backend → start → validar servicio; (4) repetir 116, 137, 113 (mcps al final: es el plano de acceso del agente); (5) redefinir nfs-storage en 5 nodos apuntando a pool2; (6) verificar ISOs visibles | 3h para 4 CTs escalonados (15-25 min/CT + margen; fundamento: piloto R2 midió vzdump CT 13-39s; restore rootfs pequeño domina) | medio: toca rootfs de 4 CTs edge; ISOs de labs no afectan producción | por CT: 15-25 min (emqx/vault/frigate/mcps) | redefinir nfs-storage de vuelta (diff guardado) + restore rootfs original; <10 min/CT | servicio de cada CT vivo post-arranque (health por protocolo: 5984 vault, S3 de frigate UI, MQTT 1883, mcps containers) + ISOs listables | OWNER: cambio storage.cfg 5 nodos + ventana 019 (bloqueantes #1/#2) | 4 CTs T0-edge con rootfs en pool2, servicios validados, storage.cfg consistente 5/5 |

- **Prohibiciones P0**: no tocar Echo/MT4/kafka guests (las migraciones W2-W5 van a la ventana 2 con sus gates); no ejecutar A6-REPL full (I/O TrueNAS compartido con W1); no compact/mClock (carril Ceph, ventana separada).

### P1 — siguientes ventanas (26-09 tarde / semana del 28-09)

| ID | Servicio | Problema | Operaciones | Dependencias | Gate | Duración |
|---|---|---|---|---|---|---|
| P1-1 | Echo 140 SO → hades local-lvm (W5 fase 1) | SO reconstruible en pool1 nearfull | vzdump offline 140 → restore a local-lvm hades → arranque → verificación app completa (sesiones + intent) | D-piloto GO + 018 + B1 mecanismo + ventana con Echo cerrado | OWNER | 30-40 min |
| P1-2 | W2 traefik 115 → nfs-storage nuevo | SPOF edge en athena | mismo mecanismo P0-2 aplicado a 115 + prueba arranque nodo alterno | W1 hecho (P0-2) | OWNER | 30 min |
| P1-3 | W4 kafka 128 hera→hades | broker del pipeline Echo en host Ceph | diagnóstico previo del brote (ver P1-4) + vzdump 128 + migración offline 5 min | diagnóstico del brote sin causa abierta | OWNER | 15 min |
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
2. **Diff storage.cfg W1 aprobado** (export pool2 + redefine nfs-storage, 5 nodos) + **ventana 019 declarada** (sáb 26sep 02:00-07:00) — habilita P0-2.
3. K1/K2 no requieren gates.

### Mandato de ejecución P0

- Preparado y NO ejecutado en: `~/aranea/work/first-window-20260926/MANDATO-P0.md` (autosuficiente: authorities, preflights fail-closed, operaciones en orden, ABORT, validación por paso, rollback, cierre). Estado: BORRADOR esperando los gates del owner; el mandato NO se ejecuta sin ventana 019 formal.

## Fuentes

- [[OPERATING-STATE-20260920]] (hallazgos: kafka brote, Ceph growth, mcps 83%), [[PLACEMENT-DECISIONS-20260920]] (fichas W1-W5), [[ROADMAP-WP-BACKUP-DR]] (D-piloto, A6, B1), [[MASTER-PLAN-STORAGE-BACKUP-DR]] (§4 ventana, §5 bloqueantes), `~/aranea/work/first-window-20260926/`.
