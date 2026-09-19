---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[agent-project-02-pbs-on-backup-node]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "R2 ejecución mandato fail-closed + driver medición"
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
  - area/aranea
---

# 2026-09-18-r2-mandato-ejecucion

%% Ejecución del mandato owner one-shot "BACKUP/DR R2 / OPERACIÓN CONTROLADA" (18sep noche): acciones 1 y 2 del bundle v3 aprobadas; acción 3 (reboot PBS) NO aprobada. %%

## Cambio

- **Tipo:** updated + infra-mutation-autorizada
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-02-pbs-on-backup-node.md` (bitácora; tareas 02-8/02-9; `status_detail`)
  - `30-resources/aranea/03-storage/backup-dr/00-index.md` ("De un vistazo")
  - `80-agents/journal/logs/2026-09-18-r2-mandato-ejecucion.md` (este log)
  - `~/aranea/work/r2-pbs-20260918/measurement/` (FUERA del vault): driver `r2-measure-day.sh` + `r2-helper.sh` + `README-ACTIVACION.md` + `state/` + `logs/`
- **Mutaciones en infra (autorizadas por este mandato):** PBS 192.168.31.123 — 2 archivos NUEVOS `/etc/systemd/system/proxmox-backup.service.d/10-require-pbs-data.conf` y `/etc/systemd/system/proxmox-backup-proxy.service.d/10-require-pbs-data.conf` + `daemon-reload`. Nada más. Rollback: `rm` de ambos + `daemon-reload`.

## Motivo

- Mandato owner one-shot (mensaje directo 2026-09-18 ~21:00): APRUEBA acciones 1 y 2 del bundle v3; NO aprueba acción 3 (reboot PBS/pruebas físicas); ejecución autónoma en una sola intervención; corrección de ventana obligatoria; caducidad 7 días; fail-closed sólo se declara con protección EFECTIVA demostrada.

## Fuentes usadas

- Mandato + `owner-action-bundle-v3.md` + `2026-09-18-r2-closeout.md` + bitácora ap-02 + `r2-closeout-analysis.md` + log piloto.
- OBSERVADO live (read-only pre-mutación, 18sep 21:05–21:15 -03): **baseline sin drift** — storage.cfg sha256 `87482f91…` == v3; jobs.cfg AUSENTE; `qm config 180` md5 `1815e259…`; lvs md5 `ec23b35b…`; fstab md5 `b4e8dd0f…`; df 1G/279G; du 731M; 429 chunks; snapshot única `ct/155/2026-09-18T22:15:24Z`; servicios `active/active`; proxy corre como usuario `backup` con sólo `Wants=proxmox-backup.service` y SIN dependencia del mount; cero drop-ins previos; cero timers PBS 05:00-08:00 (sólo daily-update 05:33); cero crontabs de usuarios.
- Timers hermes (ventana): `aranea-backup-r1` 04:00 (duró 6s el 18sep), `aranea-etcd-snapshot` 05:00 (18s), `aranea-pve-config` SÁB 08:30. Nodos 05:00-08:00: sólo `apt-daily*`/`man-db` (host-level, sin recursos compartidos con vzdump/LVM/PBS).
- Ceph pool1 (kronos): 87.18% texto / 87.21% via JSON al cierre — nearfull pre-existente.

## Resolución aplicada

### Acción 1 — Fail-closed: INSTALADO + VALIDADO, PENDING ACTIVATION (PASS no declarado)

- **Extensión justificada del diff de v3:** el mandato exige cubrir "todas las unidades… incluidos los caminos de ingreso de backups". Observado: `proxmox-backup-proxy` (ingreso de backups, corre como `backup`, dueño de `/mnt/pbs-data` 755) sólo tenía `Wants=` sobre el API server y cero dependencia del mount ⇒ el drop-in sólo en `proxmox-backup.service` dejaba el ingreso de backups sin protección. Se instalaron **2 drop-ins idénticos** (hash común sha256 `56eefebf…`): `.service.d/10-require-pbs-data.conf` con `Requires/After=mnt-pbs\x2ddata.mount` + `[Install] RequiredBy=`.
- **Verificación positiva:** `daemon-reload` limpio (sin warnings en journal); `DropInPaths` carga el archivo en AMBOS servicios; `show -p Requires/-p After` contiene `mnt-pbs\x2ddata.mount` en ambos; la mount unit declara `RequiredBy=proxmox-backup.service proxmox-backup-proxy.service` (enlaces inversos resueltos por el manager); `list-dependencies` muestra la mount en el árbol de ambos; servicios `active/active` sin interrupción; datastore `main` intacto; `is-enabled` sin cambios (systemv symlink no reescrito).
- **Pruebas negativas/positivas seguras (sin desmontar nada):** unidades temporales en `/run/systemd/system` con la MISMA sintaxis: `Requires=mnt-nonexistent\x2ddata.mount` → `Failed to start … Unit mnt-nonexistent\x2ddata.mount not found`, exit 5 (el manager FALLA la unidad por la dependencia ausente = mecanismo fail-closed demostrado a nivel manager); contraprueba con el mount real → exit 0. Cleanup completo. Servicios productivos NUNCA tocados.
- **`systemd-analyze verify`**: no soporta drop-ins ni unidades generadas por fstab-generator (artefacto de la herramienta, registrado); la validación de carga real se hizo contra el manager vivo (DropInPaths/Requires/RequiredBy).
- **CLASIFICACIÓN (cláusula CRÍTICA del mandato): PENDING ACTIVATION.** Ambos servicios arrancaron ANTES de instalar el drop-in; `daemon-reload` no protege instancias ya running; la dependencia liga en el próximo arranque. La activación efectiva requiere reiniciar servicios o reboot PBS — ambos prohibidos por el mandato (§4) / no aprobados (Acción 3). **FAIL-CLOSED PASS NO declarado; backups desatendidos NO habilitados.** No se simuló ninguna prueba como exitosa.

### Acción 2 — Medición 7 días: DRIVER PREPARADO Y VALIDADO, NO ACTIVADO (gate insatisfecho)

- El mandato condiciona la activación del piloto a que el gate de protección (§1) esté satisfecho. No lo está (PENDING ACTIVATION) ⇒ plan B del mandato aplicado: **driver preparado, validado, SIN activar; blocker exacto registrado; sin segunda ronda de diseño.**
- **Driver:** `~/aranea/work/r2-pbs-20260918/measurement/r2-measure-day.sh` (serializado, 7 CTs en orden v3, preflight montaje/capacidad/salud, re-chequeo entre jobs, verify `main` post-ciclo, métricas JSONL por evento, dryrun integrado, caducidad: primera ejecución FULL +6 días con `deadline_date`, deshabilitación automática del timer al expirar/abortar, ventana acotada 06:00–07:25). `r2-helper.sh`: tamaños/racha de fallos/resumen. `README-ACTIVACION.md`: activación = 2 comandos (instalar timer + primer run) cuándo el gate esté demostrado; desactivación = `systemctl disable --now aranea-r2-measure.timer`. Cero estado en PVE/PBS (sólo `vzdump` dirigido).
- **Validación del driver (dryrun ×3 con correcciones):** exit 0; 6 prechecks con identidad/placement/unprivileged/uptime verificados por SSH al nodo residente; bugs capturados y corregidos en caliente: array `GUESTS_ORDER` vs `GUEST_ORDER` (loop mudo — hallado leyendo el archivo, no desde memoria), `note()` unbound var, parse `ceph df` textual → JSON `percent_used` ×100 (0.87 era fracción), helper fusionado. Smoke del helper con estado aislado y limpieza.
- **Ventana definitiva: 06:00–07:25 America/Santiago** (dentro de 06:00–07:30 evaluada por el mandato). Reconciliación con timers REALES medidos: R1 termina 04:00:06, etcd 05:00:18, pve-config sáb 08:30 ⇒ sin solapamiento demostrado con 05:30–08:00 libre de trabajos que compartan LVM thin/PBS/SSH. No se modificó ningún horario congelado de R1.
- **CORRECCIÓN material al inventario v3 (placement): CT 148 etcd-keeper tiene `rootfs: pool1:vm-148-disk-0` (Ceph RBD), NO local-lvm como declara v3.** Con pool1 87.21% nearfull, se le aplica el MISMO gate que kafka (política explícita del bundle v3: raíz en pool1 nearfull ⇒ GATED). El driver lo excluye automáticamente mientras `pool1 ≥ 85%` y lo reincorpora solo si baja. **Set activo efectivo hoy: 6 CTs** (155, 156, 154, 101, 147, 115) — decisión documentada, no silenciosa; si el owner quiere forzar 148 contra el gate, es decisión explícita post-gate.
- Exclusiones v3 respetadas (mp0 etcd de facto; 152/153; kafka; mt4; truenas; resto Tier 0). Umbrales: warn 70% / ABORT 85% / <30G libres / proyección×1.5 sin margen / thin hera >90% / verify ≠ TASK OK / vzdump FAIL ×2 días → exclusión del guest.

### Integridad y cobertura (§3 del mandato)

- Sin cambios: evidencias separadas se mantienen (backup estructural PASS; restore estructural PASS; restore lógico etcd offline PASS; **restore funcional NO demostrado**; **reincorporación al quorum NO demostrada**). No se tocó ningún CT; no se activó `backup=1` en mp0; **NO se declara cobertura integral de datos** (sólo rootfs entra por PBS; datos etcd = R1 lógico).

## Validación

- Baseline pre-mutación == bundle v3 §0 en las 5 huellas + capacidad (drift cero ⇒ sin ABORT).
- Post-mutación: storage.cfg/jobs.cfg/qm 180/fstab/df/du/chunks/snapshot única SIN drift; `/etc/systemd/system` sin otras referencias a pbs-data; servicios y datastore íntegros; cero unidades transitorias residuales.
- Prueba semántica negativa/positiva con evidencia de exit codes y mensaje del manager (no simulada).
- Driver: dryrun exit 0 reproducible; eventos JSONL completos por guest; 148 gateado con medición fresca de pool1 (87.21%).
- Sin secretos en logs ni evidencias (sólo huellas criptográficas de configs).

## Compartibilidad

- Scope local; sin identidad, paths sensibles ni secretos.

## Rollback

- Infra (Acción 1): `sudo rm /etc/systemd/system/proxmox-backup.service.d/10-require-pbs-data.conf /etc/systemd/system/proxmox-backup-proxy.service.d/10-require-pbs-data.conf && sudo systemctl daemon-reload` → `show -p Requires` sin mnt-pbs. Servicios nunca reiniciados durante la sesión.
- Documental: revertir bitácora/tasks/status_detail en ap-02, índice, borrar este log y `~/aranea/work/r2-pbs-20260918/measurement/` (dir entero, 700, fuera del vault).
- Acción 2: nada que revertir en infra (cero estado persistente creado); el timer NUNCA llegó a instalarse.

## Gates residuales (estado al cierre)

1. **PENDING ACTIVATION del fail-closed** → requiere reinicio de servicios PBS o reboot (GATED: Acción 3 NO aprobada). Recién con eso se declara FAIL-CLOSED PASS y se habilita la activación del piloto.
2. **Reboot de persistencia** (fstab + drop-in en ciclo real de boot): Acción 3, GATED ventana owner.
3. Prueba negativa física (disco des-adjuntado): diferida, procedimiento documentado en v3.
4. Retención/prune/GC, jobs.cfg, Tier 0 completo: decisión D post-medición (fuera de este mandato).
5. R1.6 PAUSADO; Ceph nearfull = carril Infrastructure Ops.
6. **R2 permanece IN-PROGRESS** (DoD incompleto por diseño del mandato). Sin session close.
