---
title: "Backup/DR — Formulario Mínimo Owner (4 tickets)"
type: doc
schema_version: 1
status: active
icon: ⚡
slug: backup-dr-formulario-minimo
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-07-02
updated: 2026-08-10
aliases:
  - Formulario mínimo Backup/DR
  - Owner decisions minimal form
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - doc/form
  - workflow/owner-decision
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[BACKUP-DR-DESIGN]]"
  - "[[2026-07-02-018-owner-task-critical-vms]]"
  - "[[2026-07-02-019-owner-task-maint-window]]"
  - "[[2026-07-02-020-owner-task-secret-zero]]"
  - "[[2026-07-02-021-owner-task-oauth-scope]]"
  - "[[FORMULARIO-DECISIONES]]"
---

# ⚡ Formulario Mínimo — Backup/DR (4 tickets)

## Propósito

Recopilar en formato breve las cuatro decisiones del owner necesarias para destrabar los tickets 018–021 de Backup/DR.

## Contenido

> [!info] Cómo usar este formulario
> Este es el **formulario corto** para destrabar los 4 tickets 018-021. A diferencia del [[FORMULARIO-DECISIONES]] (largo, con templates completos), este es para que respondas **en una línea por ticket** y arranquemos implementación lo antes posible.
>
> **Workflow**:
> 1. Lee cada bloque abajo.
> 2. Responde en la sección `✍️ Tu respuesta`.
> 3. Avísame por Telegram: **"formulario mínimo listo"**.
> 4. Yo cierro los 4 tickets y armo gate técnico de implementación PBS.

---

## 🎫 Ticket 018 — Tier 0 VMs

### Lista sugerida (del inventario 2026-07-02 + docs vigentes)

| VMID | Nombre | Nodo | Razón | Tier 0 sugerido |
|---|---|---|---|---|
| 130 | opnsense | athena | gateway/firewall — control plane absoluto | ✅ Sí |
| 149 | pi-hole | athena | DNS (recursivo y sinkhole) | ✅ Sí |
| 115 | traefik | athena | reverse proxy HTTPS interno | ✅ Sí |
| 200 | ca (step-ca) | athena | cert authority raíz (R-11 step-ca pierde claves) | ✅ Sí |
| 145 | truenas | hades | storage — single point of data | ✅ Sí |
| 152 | postgresql | hades | DB prod — alimenta echo | ✅ Sí |
| 153 | mongodb | hades | DB prod — alimenta echo | ✅ Sí |
| 116 | obsidian-sync | hades | CouchDB — vault del Second Brain | ✅ Sí |
| 157 | minio | hades | object storage S3-compatible | ✅ Sí |
| 124 | mt4-real | hades | trading real | ✅ Sí |
| 133 | mt4-ftmo | hades | trading prop firm | ✅ Sí |
| 134 | mt4-ttp | hades | trading trend following | ✅ Sí |
| 144 | mt4-demo | hades | trading demo (parte del sistema echo) | ✅ Sí |
| 140 | echo | hades | orquestador del sistema echo | ✅ Sí |
| 160 | argus | hades | observabilidad general | ✅ Sí |

> **Nota**: la lista sugerida incluye **15 VMs tier 0** (las que sostienen el sistema echo + control plane). Esto es más que los 12 originales del ticket 018 — incluye también **echo (140)**, **mt4-demo (144)** y **argus (160)** que el owner mencionó como parte del core echo.

### Tu respuesta esperada

- ✅ **Aceptar la lista completa** (15 VMs tier 0)
- ✂️ **Sacar algunas** (indica VMID)
- ➕ **Agregar otras** (indica VMID + razón)

### ✍️ Tu respuesta

```
[ej: "acepto todo", o "saco 144 y 157, agrego 158 temporal", o "lista completa OK"]
```

---

## 🎫 Ticket 019 — Ventana de mantenimiento

### Opciones recomendadas

| Opción | Día | Hora | Duración | Owner presente | Notas |
|---|---|---|---|---|---|
| **A** | Sábado | 02:00-04:00 | 2h | NO (durmiendo) | Mínimo impacto laboral. Si falla, agente aborta y avisa por Telegram. |
| **B** | Domingo | 23:00-01:00 | 2h | NO (durmiendo) | Similar a A pero domingo. |
| **C** | Miércoles | 22:00-00:00 | 2h | NO | Mitad de semana. Útil si A o B no aplican. |
| **D** | A coordinar | A coordinar | 2h | SÍ | Owner presente. Mayor control pero requiere coordinación activa. |

### Duración mínima realista

**2 horas** para crear VM PBS (vmid 180) en kronos + install interactivo PBS via noVNC + config datastore + register storage en 5 nodos. **90 min es el mínimo absoluto** si todo va bien; **4h con margen** si hay troubleshooting.

### Impacto esperado

- **Kronos**: interrupción breve durante `qm create` (~1 min de I/O en LVM). NO toca Ceph quorum directamente.
- **Otros 4 nodos**: `pvesm add aranea-pbs` requiere escribir en `/etc/pve/storage.cfg` (replicado automáticamente por PVE cluster). Sin downtime.
- **VMs corriendo en kronos**: cero impacto (la VM PBS usa disco nuevo en local-lvm, no compite con VMs existentes).
- **Truenas / hades / athena / zeus / hera**: cero impacto directo. Solo se registra el storage remotamente.

### Tu respuesta esperada

- Día + hora local
- Duración máxima tolerable (en minutos)
- ¿Owner presente durante la ventana? (sí/no)
- Canal de notificación (default: Telegram "Home")

### ✍️ Tu respuesta

```yaml
maint_window:
  preferred_day: ""          # sábado | domingo | miércoles | otro
  preferred_time: ""         # formato HH:MM local
  duration_max_minutes: 0
  owner_present: false
  notify_telegram_channel: "Home"
```

---

## 🎫 Ticket 020 — Secret Zero

### Checklist mínimo para quedar operativo

- [ ] **Caja fuerte física** definida (descripción ubicación + cómo acceder)
- [ ] **USB cifrado LUKS** comprado/formateado y probado (read/write round-trip)
- [ ] **Bitwarden** cuenta owner creada y operativa
- [ ] **Recovery code de Bitwarden** impreso y guardado en caja fuerte (separado del USB)
- [ ] **Write-back procedure** documentado en `BACKUP-DR-RUNBOOK §8` (yo lo escribo si los 4 puntos anteriores están OK)

### Qué puedo tener listo ahora vs después

| Item | ¿Listo ahora? | Dependencia |
|---|---|---|
| Caja fuerte (decisión ubicación) | **Sí** — solo requiere decisión del owner, no comprar nada | ninguna |
| USB cifrado LUKS | **Depende** — si ya tienes uno, OK. Si no, requiere compra o reutilizar uno existente | opcional |
| Bitwarden | **Sí** — si tienes cuenta operativa | ninguna |
| Recovery code impreso | **Sí** — solo requiere acción física del owner | ninguna |
| Write-back procedure | **Sí** — yo lo documento una vez confirmados los 4 anteriores | ninguna |

> [!tip] Punto clave
> El **bloqueante real** para arrancar ap-02 (PBS) es solo el **passphrase del datastore PBS**, que debe vivir en Secret Zero. Los demás secretos (restic, rclone crypt, step-ca backup) son para ap-04/05 y pueden resolverse después.

### Tu respuesta esperada

Para cada item del checklist: `[x]` listo, `[ ]` pendiente.

### ✍️ Tu respuesta

```markdown
- [ ] Caja fuerte física: [ubicación breve]
- [ ] USB cifrado LUKS: [sí, modelo X / no, falta comprar / no necesito]
- [ ] Bitwarden operativo: [sí / no]
- [ ] Recovery code Bitwarden impreso: [sí / no]
- [ ] Write-back procedure: [lo documento yo / ya está en §8 / pendiente]
```

---

## 🎫 Ticket 021 — OAuth (pcloud + GDrive)

### Recomendación concreta

| Servicio | Recomendación | Método | Por qué |
|---|---|---|---|
| **pcloud** | **Opción A** — agent-driven con client_id/secret en Secret Zero | OAuth flow programático con scope `files.read` + `files.write` | pcloud OAuth es simple y el agent puede manejar el flow con tokens en Secret Zero. Refresh tokens rotan sin intervención. |
| **GDrive** | **Opción C** — service account JSON | Service account de Google Cloud project, scope `drive.file` (mínimo) | Más limpio: sin OAuth flow, sin refresh tokens, sin expiración. JSON key se guarda una vez en Secret Zero. |

### Riesgos de cada opción (en una línea)

**pcloud**:
- **A (agent)**: si refresh token expira o es revocado, agent no puede continuar sin intervención owner.
- **B (owner-driven)**: cada vez que un token expira (poco frecuente pero pasa), owner debe intervenir manualmente.
- **C (no aplica)**: pcloud no tiene service account equivalente.

**GDrive**:
- **A (agent)**: igual que pcloud — riesgo de refresh token expirado.
- **B (owner)**: igual — intervención manual por expiración.
- **C (service account)**: el JSON key es compromiso total de la cuenta-servicio (un solo archivo, una sola rotación anual).

### Tu respuesta esperada

Para cada servicio: `[A]`, `[B]` o `[C]`.

### ✍️ Tu respuesta

```yaml
oauth_decision:
  pcloud: ""    # A | B | C
  gdrive: ""    # A | B | C
```

---

## ✅ Cuando termines

1. Marca las 4 secciones con respuesta.
2. Avísame por Telegram: **"formulario mínimo listo"**.
3. Yo:
   - Cierro los 4 tickets (018-021) con tus respuestas.
   - Armo el **gate técnico de implementación PBS** con **comandos reales** (no placeholders), basados en tu ventana confirmada + tier 0 + Secret Zero + OAuth.
   - Te lo entrego para revisión **antes de ejecutar nada en infra**.

---

## 📚 Referencias

- [[BACKUP-DR-OWNER-PROJECT]] — proyecto owner (design-frozen)
- [[BACKUP-DR-DESIGN]] — diseño congelado
- [[FORMULARIO-DECISIONES]] — versión larga con templates (referencia, no usar)
- [[2026-07-02-018-owner-task-critical-vms]] — ticket 018
- [[2026-07-02-019-owner-task-maint-window]] — ticket 019
- [[2026-07-02-020-owner-task-secret-zero]] — ticket 020
- [[2026-07-02-021-owner-task-oauth-scope]] — ticket 021
