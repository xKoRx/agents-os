---
title: "Backup/DR — Diff conceptual previo (pre-implementación)"
type: doc
schema_version: 1
status: active
status_detail: "Diff conceptual antes de generar los 16 archivos del refactor §12. Owner debe aprobar antes de cualquier implementación."
icon: 🔍
slug: backup-dr-diff-conceptual
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
tags:
  - kind/doc
  - area/personal
  - project/agents-os
  - domain/backup-dr
  - doc/design-proposal
  - workflow/pre-approval
related:
  - "[[DESIGN-PROPOSAL]]"
  - "[[PROPUESTA-COMPLETA-ITER4]]"
  - "[[../05-tickets/2026-06-30-013-storage-redesign-backup-design]]"
cssclasses:
  - wide
---

# 🔍 Backup/DR — Diff conceptual (pre-implementación)

## Propósito

Documentar el diff conceptual presentado al owner antes del refactor Backup/DR, manteniendo su estado histórico de espera de aprobación en `status_detail` y en el cuerpo.

## Contenido

> **Propósito**: antes de generar los 16 archivos del refactor (BACKUP-DR-DESIGN, OWNER-PROJECT, 9 agent-projects, runbook, checklist, policy YAML, inventory JSON, REQUEST-CHANGES), mostrar al owner exactamente qué cambiaría, qué se elimina, qué se mantiene, qué riesgos se corrigen y qué decisiones quedan congeladas.
>
> **Modo de trabajo (§0 del prompt maestro)**: este doc es la SALIDA 1. Una vez aprobado, se procede a generar el resto.

---

## 1. Contradicciones detectadas en la propuesta actual

### 1.1 Recursos "disponibles" que en realidad no lo están

| # | Contradicción | Ubicación | Estado real |
|---|---|---|---|
| C-01 | TL;DR dice "Reusar `local-sqx-hera` (931 GB libres, vm 123 stopped)" | §0 TL;DR punto 3 | **Descartado** por decisión 5 del §12. Iter 4 dice NO TOCAR. TL;DR desactualizado. |
| C-02 | §3.1 dice "hera — destino secundario de `zfs recv`" con detalles operativos | §3.1 | **Descartado**. Aún describe cómo destruir el VG `local-sqx-hera`. |
| C-03 | §4.4 Plan C propone crear `pool1` sobre `local-sqx-hera` | §4.4 | **Descartado** por sagrado SQX. |
| C-04 | §7 Topología objetivo muestra "hera + ZFS recv (931 GB libre)" | §7 diagrama | **Mentira visual**. No existe esa fase. |
| C-05 | §6.3 sanoid policy referencia `[pool1/recv]` y `[pool0/proxmox_storage]` | §6.3 | pool1/recv no existe. proxmox_storage sí existe pero no tiene sanoid declarado. |
| C-06 | §6.2 Gantt menciona "pool1 (sanoid)" como hourly job | §6.2 | pool1 no existe. |

### 1.2 Restos de iteraciones anteriores que quedaron vivos

| # | Iteración descartada | Resto visible |
|---|---|---|
| R-01 | Iter 1 (capex ~$650) | §0 todavía menciona "5 puntos" que incluyen comprar HW. NO comprar. |
| R-02 | Iter 2 (asumía `sdf` spare) | §0 menciona `sdf1` y Plan A mirror. `sdf` está en pool0 mirror-0. |
| R-03 | Iter 3 (Plan B) | §4.5 dice "NO crear pool1 por ahora" pero §4.4 Plan C sigue existiendo con detalles. |
| R-04 | Iter 4 (sagrados SQX, Fase 2 descartada) | §3.1 hera dice "destino secundario de zfs recv" — sigue activo, contradice Fase 2 rechazada. |

### 1.3 Decisiones del owner que faltan en el cuerpo

| # | Decisión tomada | Falta en |
|---|---|---|
| M-01 | Iter 4: pcloud=critical, GDrive=bulk | §5.1 dice "Tier caliente semanal" / "Tier archivo mensual" — no segrega explícitamente. |
| M-02 | Iter 4: Optimización = Opción A | §3e dice "Pendiente discutir con owner" pero §12.7 dice "✅ Opción A". Inconsistencia. |
| M-03 | Iter 4: 8 GB RAM para PBS | §3.1 kronos dice "16 GB RAM". |
| M-04 | Iter 4: PBS datastore = `local-kronos` | §3.1 dice "sobre `local-kronos` o `pool-kronos`" — no fija. |
| M-05 | Iter 4: Pool1 (Ceph) sin backup externo | §6.1 política incluye "Ceph RBD → export → PBS weekly" — contradice. |
| M-06 | Iter 4: `pool0_backup` no migrar | §4.3 política dice "migrar a kronos pool1 cuando exista". Contradice. |

### 1.4 Riesgos no cubiertos por la propuesta

| # | Riesgo | Estado actual |
|---|---|---|
| X-01 | Sin **Secret Zero / escrow offline** documentado | Solo mención: "bitwarden offline + USB cifrado". Sin procedure, sin responsables. |
| X-02 | Sin **observabilidad / alertas** explícitas | Solo "rclone logs + PBS verify". No hay alertas, thresholds, runbooks asociados. |
| X-03 | Sin **restore drills** calendarizados con criterios PASS/FAIL | §9 Fase 5 lo menciona pero sin métricas ni responsables. |
| X-04 | Sin **inventario de secretos** | No lista qué secrets existen ni dónde se registran. |
| X-05 | Sin **clasificacion tier 0/1/2/3** para VMs | §6 dice "critical" pero no define qué es critical. |
| X-06 | Sin **request change workflow** | Cambios futuros al diseño no tienen template. |
| X-07 | Sin **definición de terminado** por fase | §9 lista tareas pero no AC por fase. |
| X-08 | Sin **ventanas de mantenimiento** declaradas | Fases no indican cuándo se ejecutan. |
| X-09 | Sin **rollback explícito** por fase | Solo "rollback" mencionado de pasada. |
| X-10 | Sin **owner tasks vs agent tasks** separadas | Mezcladas en §9. |
| X-11 | Sin **gate de seguridad** por fase | DANGEROUS no marcado en comandos. |
| X-12 | Sin **diferencia policy vs runbook vs skill vs memory** | Todo mezclado en el mismo doc. |
| X-13 | Confusión **pool0_backup** vs **pool0 backup** | §4.3 menciona "pool0_backup" como dataset dentro de pool2. §6 dice "ZFS pool0 truenas sanoid". El lector no entiende cuál es cuál. |

---

## 2. Lo que CAMBIARÍA (refactor positivo)

### 2.1 Nuevos archivos a crear

| Archivo | Propósito | Tamaño estimado |
|---|---|---|
| `BACKUP-DR-DESIGN.md` | Diseño final corregido. Una sola verdad activa. Capas A-G. Decisiones congeladas. | ~30 KB |
| `BACKUP-DR-OWNER-PROJECT.md` | Proyecto owner. Mapa subproyectos. Calendario. DoD. | ~15 KB |
| `agent-project-00-policy-and-doc-cleanup.md` | Limpiar DESIGN-PROPOSAL, mover histórico, cerrar gaps de docs. | ~6 KB |
| `agent-project-01-critical-config-backup.md` | /etc/pve, Traefik, OPNsense, step-ca, etcd, manifests, runbooks. | ~12 KB |
| `agent-project-02-pbs-on-backup-node.md` | Crear VM PBS en kronos. Datastore `local-kronos`. 8 GB RAM. | ~14 KB |
| `agent-project-03-app-consistent-data-backups.md` | PostgreSQL, MongoDB, CouchDB, minio, ZFS pool0 sanoid. | ~14 KB |
| `agent-project-04-cloud-critical-tier.md` | pcloud + rclone crypt + Restic/Borg. Tier caliente. | ~10 KB |
| `agent-project-05-cloud-bulk-archive-tier.md` | GDrive + rclone crypt + chunking. Tier bulk. | ~10 KB |
| `agent-project-06-observability-and-alerting.md` | Stack observabilidad. Alertas mínimas. Thresholds. | ~10 KB |
| `agent-project-07-restore-drills.md` | Calendario drills. Criterios PASS/FAIL. Evidencia. | ~10 KB |
| `agent-project-08-session-closeout-and-learning-loop.md` | Cierre sesión, lecciones, memoria, skills. | ~8 KB |
| `BACKUP-DR-RUNBOOK.md` | Comandos operativos. Backup manual. Restore manual. Troubleshooting. | ~15 KB |
| `BACKUP-DR-CHECKLIST.md` | Pre/post ejecución, mensual, restore drill. | ~6 KB |
| `backup-policy.yaml` | Tiers, frecuencia, retención, exclusiones, verificación, restore drill. | ~5 KB |
| `backup-inventory-template.json` | Nodos, VMs, servicios, datasets, destinos, jobs, secretos, owners. | ~3 KB |
| `REQUEST-CHANGES.md` | Cambios propuestos a policies/runbooks/skills/memoria. | ~5 KB |

> **2026-07-02 — nota de migración**: el proyecto owner y los 9 subproyectos de agente migraron de `30-resources/aranea/03-storage/backup-dr/` a `10-projects/Aranea/` (proyecto) y `10-projects/Aranea/agentes/` (subproyectos) por convención PARA (proyectos con plazo y tareas → `10-projects/`, documentación evergreen → `30-resources/`). Los archivos en sí no cambiaron de contenido; solo de ubicación. Ver `10-projects/Aranea/README.md` y log `80-agents/journal/logs/2026-07-02-aranea-backup-dr-migration-to-10-projects.md`.

### 2.2 Cambios al doc actual `DESIGN-PROPOSAL.md`

| Cambio | Tipo | Por qué |
|---|---|---|
| Marcar como **deprecated** y dejar link al nuevo `BACKUP-DR-DESIGN.md` | Refactor | El nuevo doc es la verdad activa. |
| Mover toda la sección §4.4 Plan C y §4.5 Plan B/C a una sección "Diseños descartados / histórico" con motivo, fecha y riesgo que evita. | Limpieza | Sin restos vivos. |
| Reescribir §0 TL;DR para reflejar SOLO el estado vigente (PBS + cloud dual, sin zfs recv on-cluster) | Corrección | TL;DR ≠ body. |
| Actualizar §3.1 hera: NO destino `zfs recv`, mantener Ceph OSD.0 + compute. | Corrección | Confunde Sagrados SQX. |
| Actualizar §3.1 kronos: VM PBS con 8 GB RAM sobre `local-kronos` (NO 16 GB, NO sobre `local-sqx-*`). | Corrección | Decisión 2 del §12. |
| Reescribir §5 con segregación dura pcloud=critical, GDrive=bulk. | Refuerzo | Decisión 3 del §12. |
| Eliminar §6 referencias a `pool1/recv` (no existe), Ceph RBD → PBS weekly (contradice 8), `pool0_backup` migration (contradice 4). | Limpieza | Decisiones 4, 5, 6, 8 del §12. |
| Cerrar §3e "Pendiente discutir con owner" → "✅ Opción A aplicada". | Cierre | Decisión 7 del §12. |
| Actualizar §10 riesgos: hades SPOF se mantiene, sdf ya verificado, agregar riesgo sobre pool0_backup vs pool2 confusion. | Refuerzo | Claridad. |

### 2.3 Cambios al ticket `2026-06-30-013`

| Cambio | Tipo |
|---|---|
| Marcar ticket como `superseded-by-backup-dr-design`. | Metadata |
| Linkear a `BACKUP-DR-DESIGN.md` como nuevo contenedor. | Link |
| Las 6 decisiones resueltas pasan a `Decisiones congeladas` en el nuevo design. | Migración |
| Las 2 decisiones nuevas pendientes (Fase 2 reactivable, optimización) — la de optimización ya resuelta. | Update |

### 2.4 Cambios al `00-index.md` de aranea

| Cambio | Tipo |
|---|---|
| Agregar entrada en § Mapa de documentación: `BACKUP-DR-DESIGN.md` y los 9 agent-projects. | Adición |
| Marcar `DESIGN-PROPOSAL.md` como `historical → ver BACKUP-DR-DESIGN.md`. | Advertencia |

---

## 3. Lo que ELIMINARÍA

| # | Eliminación | Justificación |
|---|---|---|
| E-01 | §0 TL;DR punto "Reusar `local-sqx-hera` (931 GB libres)" | Sagrados SQX. |
| E-02 | §3.1 hera "destino secundario de `zfs recv`" | Sagrados SQX. |
| E-03 | §4.4 Plan C entero | Ya descartado, contradice sagrados. |
| E-04 | §4.2 "❌ Plan A descartado — `sdf` NO es spare" | Mantener como histórico breve, NO como acción. |
| E-05 | §6.3 sanoid policy referencia `[pool1/recv]` | pool1 no existe. |
| E-06 | §6.1 política "Ceph RBD → export → PBS weekly" | Decisión 8: NO agregar backup externo Ceph. |
| E-07 | §6.1 política "`ZFS pool1 truenas`" | pool1 no existe. |
| E-08 | §6.1 política "`ZFS pool1 kronos` (recv)" | zfs recv descartado. |
| E-09 | §4.3 política "migrar pool2/pool0_backup a kronos pool1 cuando exista" | Decisión 4: no migrar. |
| E-10 | §3e "Pendiente discutir con owner" | Ya resuelto = Opción A. |
| E-11 | §7 topología "hera + ZFS recv" | No existe. |
| E-12 | §6.2 Gantt "ZFS snap pool1 (sanoid)" | pool1 no existe. |
| E-13 | §9 Fase 1 paso "Liberar `local-kronos` o `pool-kronos` (migrar vms stopped si necesario; `sqx-ulab-kron-0` vmid 111 stopped" | Implica mover VM SQX stopped. NO TOCAR sagrados. |
| E-14 | §6 política "Traefik config" y "OPNsense config" mencionados sin owner task | Sin responsable asignado. |

---

## 4. Lo que MANTENDRÍA

| # | Mantener | Por qué |
|---|---|---|
| K-01 | Estructura general por capas (recursos, asignación, pools, cloud, política, topología, antes/después, roadmap, riesgos, refs, decisiones) | Esqueleto útil. |
| K-02 | Inventario de recursos por nodo (athena/zeus/hera/kronos/hades/truenas) | Real, validado. |
| K-03 | Decisión `local-sqx-*` sagrados | Regla owner vigente. |
| K-04 | Decisión `pool0_backup` no migrar | Vigente. |
| K-05 | Decisión `pool2` single disk aceptado | Vigente. |
| K-06 | Decisión hades SPOF aceptado | Vigente. |
| K-07 | Decisión PBS = 8 GB, datastore = `local-kronos` | Vigente. |
| K-08 | Decisión cloud dual segregado (pcloud=critical, GDrive=bulk) | Vigente. |
| K-09 | Decisión Opción A para optimización | Vigente. |
| K-10 | Decisión NO backup externo Ceph | Vigente. |
| K-11 | Tabla de riesgos §10 (la idea, no los detalles contradictorios) | Válida. |
| K-12 | Política §6.1 base: vzdump daily critical + weekly all, ZFS sanoid hourly/daily/weekly/monthly | Válida. |
| K-13 | Inventario completo de VMs en `02-servicios/ml-ia.md` | Independiente, válido. |
| K-14 | Skill `aranea_agent_ro_inventory_refresh` | Independiente, válido. |
| K-15 | Tickets 014-017 (dashboard, etc.) | Independientes. |

---

## 5. Riesgos que se CORRIGEN con el refactor

| # | Riesgo original | Corrección en refactor |
|---|---|---|
| Z-01 | TL;DR desactualizado podría inducir a error de implementación | TL;DR nuevo coincide con diseño final. |
| Z-02 | Restos de iteraciones hacen que un implementador toque recursos prohibidos | Histórico separado y explícito. |
| Z-03 | Sin owner tasks separadas, owner podría esperar que agente haga cosas que no puede | Owner tasks explícitas en cada agent-project. |
| Z-04 | Sin Secret Zero, pérdida de passphrase = pérdida total de cloud tier | Sección obligatoria + escrow. |
| Z-05 | Sin alertas, fallos silenciosos | Observabilidad con thresholds + runbooks asociados. |
| Z-06 | Sin restore drill formal, "creemos que funciona" hasta el día del disaster | Calendario + AC + evidencia. |
| Z-07 | Acciones `DANGEROUS` no marcadas, agente podría ejecutar `zpool attach` o `vm destroy` por error | Marcadas explícitamente + gate de aprobación. |
| Z-08 | Cambios futuros al diseño/edit silenciosos, memory drift | Request Change workflow obligatorio. |
| Z-09 | Pool1/recv en sanoid policy = config corrupta si se aplica literal | Eliminado del policy. |
| Z-10 | Confusión pool0_backup (dataset en pool2) vs pool0 backup (sanoid de pool0) | Glosario en §0 nuevo design. |

---

## 6. Decisiones CONGELADAS (no se pueden cambiar sin Request Change)

| # | Decisión | Estado | Motivo | Evidencia | Fecha | Impacto |
|---|---|---|---|---|---|---|
| F-01 | Cero capex | FROZEN | Owner restricción hard | Mensaje 2026-06-30 | 2026-06-30 | Sin comprar HW. |
| F-02 | No migrar TrueNAS a bare-metal | FROZEN | Owner restricción hard | Mensaje 2026-06-30 | 2026-06-30 | hades sigue como hypervisor. |
| F-03 | No agregar ni sacar servidores | FROZEN | Owner restricción hard | Mensaje 2026-06-30 | 2026-06-30 | 5 Proxmox + truenas-vm + hermes-vm. |
| F-04 | `local-sqx-{zeus,hera,kronos}` son sagrados | FROZEN | Owner declaración explícita | Mensaje 2026-07-01 | 2026-07-01 | NO se tocan para nada que no sea SQX. |
| F-05 | `sdf` está en `pool0 mirror-0` (NO spare) | FROZEN | Validado `zpool status -v` | Discovery truenas 2026-06-30 | 2026-06-30 | No hay disco libre hades para mirror pool2. |
| F-06 | PBS datastore = `local-kronos` (680 GB libre) | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | SSD Samsung 870 QVO en kronos. |
| F-07 | PBS RAM = 8 GB | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Default mínimo. Ajustar si métricas lo piden. |
| F-08 | Cloud segregado: pcloud=critical, GDrive=bulk | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Tier aislado por criticidad. |
| F-09 | `pool0_backup` (dataset en pool2) no se migra | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Se queda donde está. |
| F-10 | Sin backup externo Ceph (RBD export) | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | 3× replication + vzdump PBS cubren. |
| F-11 | Optimización = Opción A (PBS dedup + ZFS raw/compressed + excluir caches) | FROZEN | Owner decisión | Mensaje 2026-07-01 | 2026-07-01 | Conservadora, simple. |
| F-12 | Fase 2 (zfs recv on-cluster) DESCARTADA | FROZEN | Sagrados SQX, sin SSD libre alternativo | Mensaje 2026-07-01 | 2026-07-01 | PBS + cloud reemplazan. |
| F-13 | hades SPOF aceptado | FROZEN | Owner decisión | Mensaje 2026-06-30 | 2026-06-30 | PBS off-host en kronos sobrevive. |
| F-14 | pool2 single disk aceptado, scrub mensual | FROZEN | Sin disco libre para mirror | Iter 3 + validado | 2026-06-30 | Mitigado con cloud tier. |

---

## 7. Decisiones PENDIENTES (no congeladas, pueden cerrarse en próxima sesión)

| # | Decisión | Bloquea |
|---|---|---|
| P-01 | ¿Reactivar Fase 2 con `pool-kronos` (730 GB libre, NO SQX) como destino `zfs recv` secundario on-cluster? | Mejora opcional on-cluster, no bloqueante. |
| P-02 | ¿Cuál es la definición de "critical VMs" para tier 0? (sqx-ulab, mt4-*, postgresql, mongodb, etc.) | Política §6.1 / agent-project-02 PBS. |
| P-03 | ¿Ventana de mantenimiento preferida para acciones DANGEROUS? (¿sábado madrugada, domingo noche,平日?) | Calendario implementación. |
| P-04 | ¿Confirmar ubicación física del Secret Zero? (¿caja fuerte, USB cifrado en oficina, segunda casa?) | Sección §9 Secret Zero obligatoria. |
| P-05 | ¿OAuth tokens pcloud/GDrive los maneja el owner en persona o el agente puede hacerlo? | agent-project-04/05. |

---

## 8. Modelo conceptual que aplica el refactor

| Artefacto | Rol | Ejemplos en este refactor |
|---|---|---|
| **Policy** | Límites duros, invariantes, recursos protegidos, reglas de seguridad | `backup-policy.yaml` (tiers, retención, exclusiones, sacred resources). Section §2 "Decisiones congeladas". |
| **Runbook** | Verdad operacional humana, pasos, validaciones, rollback | `BACKUP-DR-RUNBOOK.md` (comandos operativos, restore manual). |
| **Skill** | Habilidad ejecutable por agentes que sigue políticas y runbooks | `aranea_agent_ro_inventory_refresh` (existente), futuras: `aranea_backup_pbs_add_storage`, `aranea_restore_pbs_drill`. |
| **Memory** | Decisiones, aprendizajes, errores previos, preferencias curadas | `~/.hermes/profiles/ariadna/memory/` (ya tiene entries sobre Aranea). Próxima: lecciones de este refactor. |
| **Inventory** | Estado real observado del sistema | `backup-inventory-template.json` + discovery outputs. |
| **Request Change** | Propuesta revisable para cambiar policy/runbook/skill/memory | `REQUEST-CHANGES.md` (template vivo). |

**Reglas de autoridad**:
```
La policy bloquea.
El runbook manda.
La skill ejecuta.
La memoria aconseja.
El inventario aterriza.
El owner aprueba cambios riesgosos.
```

---

## 9. Pendientes que NO son bloqueantes para este refactor

- Implementación real de cualquiera de los 9 agent-projects.
- Compra de HW (prohibido).
- Modificación de pools, VGs, LVs, o datasets existentes.
- Creación de VM PBS.
- Configuración de rclone.
- Modificación de sanoid en truenas.

**Este refactor SOLO escribe documentos.**

---

## 10. Riesgos que el refactor MISMO introduce

| # | Riesgo | Mitigación |
|---|---|---|
| Y-01 | 16 archivos nuevos crean ruido en el vault | Agrupados en `30-resources/aranea/03-storage/backup-dr/` con index. |
| Y-02 | Obsidian graph se ensucia con referencias circulares | Cada doc tiene frontmatter con `related:` explícito, no wikilinks implícitos. |
| Y-03 | Doc actual `DESIGN-PROPOSAL.md` queda huérfano | Marcar deprecated + link al nuevo + mantener como histórico. |
| Y-04 | Owner abrumado por volumen | Este diff conceptual es la ÚNICA cosa que requiere lectura completa del owner. Los 16 archivos son implementables por agente. |

---

## 11. Pregunta al owner antes de generar los 16 archivos

**¿Apruebas este diff conceptual para que proceda a generar los 16 archivos del refactor §12?**

Si apruebas:
- Procedo a crear los 16 archivos en `30-resources/aranea/03-storage/backup-dr/`.
- Marco `DESIGN-PROPOSAL.md` como deprecated.
- Actualizo ticket 013 + 00-index.
- NO ejecuto ningún cambio de infraestructura.

Si quieres ajustar algo del diff conceptual (renombrar archivo, agregar constraint, cambiar tier, etc.), dímelo antes.

---

**Status**: awaiting owner approval.
**No se han creado archivos aún.** Este doc es la entrega 1 de 17.
