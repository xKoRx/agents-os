---
title: Backup/DR — Formulario de Decisiones del Owner
type: doc
schema_version: 1
status: active
icon: 📝
slug: backup-dr-formulario-decisiones
area: "[[Aranea]]"
created: 2026-07-02
updated: 2026-08-10
aliases:
  - Formulario Backup/DR
  - Owner decisions form
  - backup-dr-form
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
cssclasses:
  - wide
---

# 📝 Formulario de Decisiones — Backup/DR Aranea

## Propósito

Recopilar en Obsidian las cuatro decisiones del owner que bloquean la implementación Backup/DR.

## Contenido

> [!info] Cómo usar este formulario
> Este archivo existe para que **respondas en Obsidian** a las 4 decisiones que bloquean la implementación del proyecto Backup/DR.
>
> **Workflow:**
> 1. Abre este archivo en Obsidian en cualquier dispositivo.
> 2. Para cada ticket, edita el bloque `✍️ Tu respuesta` debajo de cada pregunta.
> 3. Marca el checkbox `[ ]` → `[x]` cuando termines una sección.
> 4. Cuando las 4 secciones estén completas, **avísame por Telegram** y yo proceso el archivo, cierro los tickets 018-021 y arranco con la Fase 0.
>
> **Tip:** No necesitas escribir mucho. Respuestas de una línea bastan en la mayoría de los casos. Si algo te bloquea, marca `❓ Bloqueado — necesito input del agente` y conversamos.

---

## Resumen ejecutivo

| # | Pregunta | Bloquea | Completado |
|---|---|---|---|
| 1 | [Ticket 018](https://github.com) — ¿Qué VMs son tier 0? | ap-02 (PBS schedule) | [ ] |
| 2 | [Ticket 019](https://github.com) — ¿Cuándo puedo tocar VMs/hosts? | ap-02 (crear VM PBS) | [ ] |
| 3 | [Ticket 020](https://github.com) — ¿Dónde viven los secretos raíz? | ap-04 / ap-05 (cloud tier) | [ ] |
| 4 | [Ticket 021](https://github.com) — ¿Quién corre los OAuth? | ap-04 / ap-05 (cloud tier) | [ ] |

---

## 🎫 Pregunta 1 — ¿Qué VMs son tier 0?

> [!question] Contexto
> El tier 0 define qué VMs reciben **backup diario con retención agresiva** y **restore drills mensuales**.
> Sin esta lista, ap-02 puede arrancar pero `vzdump` correría contra **todas** las VMs, saturando PBS con VMs de lab.

### Criterio sugerido (puedes ajustar)

> Tier 0 = cualquier VM cuya pérdida cause **outage material** (servicio productivo, control plane, identity, datos únicos).

### Candidatos pre-seleccionados del inventario 2026-07-02

| vmid | nombre        | nodo   | rol candidato                             | ¿Tier 0?        |
| ---- | ------------- | ------ | ----------------------------------------- | --------------- |
| 130  | opnsense      | athena | gateway/firewall (control plane absoluto) | [x] Sí / [ ] No |
| 149  | pi-hole       | athena | DNS                                       | [x] Sí / [ ] No |
| 115  | traefik       | athena | reverse proxy                             | [x] Sí / [ ] No |
| 200  | ca (step-ca)  | athena | identity / certs                          | [ ] Sí / [ ] No |
| 145  | truenas       | hades  | storage (single point of data)            | [x] Sí / [ ] No |
| 152  | postgresql    | hades  | DB prod                                   | [x] Sí / [ ] No |
| 153  | mongodb       | hades  | DB prod                                   | [x] Sí / [ ] No |
| 116  | obsidian-sync | hades  | knowledge base                            | [ ] Sí / [ ] No |
| 157  | minio         | hades  | object storage                            | [x] Sí / [ ] No |
| 124  | mt4-real      | hades  | trading real                              | [x] Sí / [ ] No |
| 134  | mt4-ttp       | hades  | trading real                              | [x] Sí / [ ] No |
| 133  | mt4-ftmo      | hades  | trading real                              | [x] Sí / [ ] No |

mt4-real 

> [!warning] VMs adicionales
> Si quieres sumar VMs que **no están en la lista**, agrégalas aquí abajo con el mismo formato.

```markdown
| vmid | nombre | nodo | rol | tier |
|------|--------|------|-----|------|
| XXX  | XXXX   | XXXX | XXX | 0    |
```

### ✍️ Tu respuesta

<!-- Responde acá. Ejemplos válidos:
  - "tier 0 = 130, 145, 152, 153, 200" (mínimo viable)
  - "tier 0 = 130, 145, 152, 153, 200" (mínimo viable)
  - "tier 0 = todo lo de la tabla; tier 1 = mt4 + obsidian; tier 2 = el resto"
  - "tier 0 = todo lo de la tabla; tier 1 = mt4 + obsidian; tier 2 = el resto"
  - "tier 0 = solo control plane (130 + 200 + 145), todo lo demás tier 1"
  - "tier 0 = solo control plane (130 + 200 + 145), todo lo demás tier 1"
-->

```
existen distintos tipos de vms...  dentro de tier 0. 

las fundamentales podrían ser (sin estas mierdas ningún servicio funciona):

opnsense
phihole
traefik

sobre esta capa hay otro servicio muy importante que es truenas, que se usa como storage para todos los servicios.

aranea no es solo un homelab tipo hobby, es también un datacenter para un sistema de trading algorítmico. sin esto no hay homelab al final.

el sistema se llama echo y utiliza primero el servicio de etcd (menos keeper), los lxc con etcd en cada nodo forman un cluster de etcd, de aquí todos los sistemas obtienen las configuraciones de infra y otros datos más, por lo que es importante mantener el cluster con al menos 3 nodos (esto es un warning feo) y siempre con 5. el cluster de kafka (en 3 nodos) también es importante, hay 3 vms.

los servicios que luego usa echo son:

mt4-demo
mt4-real 
mt4-ftmo
mt4-ttp
echo
docker-flink
docker-hasura
postgres
mongo
y finalmente argus, una vm para observabilidad general. puedes mirar las notas y verás todos los servicios que tiene, aquí podemos construir paneles y monitores de todo.

todo lo demás puede estar abajo, no es la idea, pero puede, los fundamentales son los tier 0
```

---

## 🎫 Pregunta 2 — ¿Cuándo puedo tocar VMs/hosts?

> [!question] Contexto
> `agent-project-02` necesita crear una **VM PBS** en kronos (vmid 180), descargar ISO, instalar PBS, registrar storage en 5 PVE nodes. Esto interrumpe brevemente kronos (Ceph quorum + storage PVE). El agente solo ejecuta dentro de una ventana confirmada por ti.

### Lo que necesito de ti

| Campo                                   | Ejemplo                               | Tu respuesta                              |
| --------------------------------------- | ------------------------------------- | ----------------------------------------- |
| **Día preferido**                       | "sábado" / "domingo" / "miércoles AM" | para PBS a penas tengas la tarea comienza |
| **Hora local**                          | "02:00" / "23:00"                     |                                           |
| **Duración máxima tolerable** (minutos) | 120                                   |                                           |
| **¿Owner presente durante la ventana?** | sí / no                               |                                           |
| **Contacto de emergencia**              | "telegram @rodrigo"                   |                                           |
| **Canal de notificación**               | "Home"                                |                                           |

### ✍️ Tu respuesta

```yaml
maint_window:
  preferred_day: ""
  preferred_time: ""
  duration_max_minutes: 0
  owner_present: false
  emergency_contact: ""
  notify_telegram_channel: "Home"
```

> [!tip] Sugerencia
> Si tienes claro "los sábados a las 02 AM estoy durmiendo, no me molestes salvo emergencia", eso es suficiente. El agente puede trabajar solo con supervisión async vía Telegram.

---

## 🎫 Pregunta 3 — ¿Dónde viven los secretos raíz (Secret Zero)?

> [!warning] Severidad: **high**
> Sin Secret Zero resuelto, los passphrases de rclone crypt, restic, PBS, step-ca quedan en plaintext en filesystem. Esto bloquea todos los tier cloud (ap-04 + ap-05) y el cifrado del backup de step-ca.

### Lo que necesito de ti

Marca con `[x]` lo que ya tienes listo, con `[ ]` lo pendiente:

- [ ] **Caja fuerte física** definida (con descripción de ubicación)
- [ ] **USB cifrado** (LUKS) comprado/formateado y probado
- [ ] **Bitwarden** cuenta owner creada y operativa
- [ ] **Recovery code de Bitwarden** impreso y guardado en la caja fuerte (separado del USB)
- [ ] **Write-back procedure** documentado en `BACKUP-DR-RUNBOOK.md §8` (yo lo escribo si me confirmas los puntos anteriores)
- [x] No tengo servicio de secrets, solo uso un cluster de etcd para guardar claves y configs... ✅ 2026-07-02

### ✍️ Tu respuesta

Describe brevemente cada punto:

```markdown
### Caja fuerte
- Ubicación física: [ej: "cajón del escritorio, segundo piso"]
- Combinación / llave: [NO escribir la combinación acá, solo si está sellada en sobre]

### USB cifrado
- Modelo: [ej: "Kingston DataTraveler 8GB"]
- Cifrado: [LUKS / VeraCrypt / BitLocker / otro]
- Etiqueta: [ej: "aranea-secret-zero-v1"]
- Probado: [sí/no, fecha]

### Bitwarden
- Cuenta: [email owner]
- Organización: [ej: "aranea-personal"]
- 2FA: [TOTP / Yubikey / otro]

### Write-back procedure
- ¿Quieres que yo lo documente en RUNBOOK §8? [sí/no]
```

---

## 🎫 Pregunta 4 — ¿Quién corre los flujos OAuth (pcloud + GDrive)?

> [!warning] Severidad: **high**
> OAuth apps son credenciales sensibles. Decidir el alcance del agente en OAuth flows.

### Opciones (elige una por servicio)

#### pcloud

- [x] **Opción A — Agent con scope limitado (recomendado)**: tú creas la OAuth app una vez en consola pcloud, guardas client_id + client_secret en Secret Zero. Agent ejecuta OAuth flow programáticamente con scope mínimo. ✅ 2026-07-02
- [ ] **Opción B — Owner-driven completo**: tú creas la app, ejecutas el OAuth flow, entregas tokens al agent vía Secret Zero.
- [ ] **Opción C — No aplica / otro proveedor**: [describe]

#### Google Drive

- [ ] **Opción A — OAuth flow agent-driven**: igual que pcloud opción A.
- [x] **Opción C — Service account (recomendado)**: tú creas service account en Google Cloud Console, descargas JSON key, guardas en Secret Zero. Agent usa la key directamente sin OAuth flow. Más limpio y reproducible. ✅ 2026-07-02
- [ ] **Opción D — No aplica / otro método**: [describe]

### ✍️ Tu respuesta

```yaml
oauth_scope_decision:
  pcloud:
    operator: ""          # "agent-with-scope" | "owner-driven" | "n/a"
    scopes: ["files.read", "files.write"]
    client_credentials_storage: "secret-zero"
  gdrive:
    method: ""            # "oauth-flow" | "service-account" | "n/a"
    scopes: ["drive.file"]
    service_account_key_storage: "secret-zero"
```

> [!tip] Si no tienes claro
> Mi recomendación: **Opción A para pcloud** + **Opción C (service account) para GDrive**. Es el balance entre seguridad, automatización y reproducibilidad. Si prefieres opción B en ambos por simplicidad, también funciona — solo que cada vez que un token expire, te toca intervenir.

---

## ✅ Cuando termines

1. Revisa que las 4 secciones estén completas.
2. Marca todos los checkboxes de la tabla resumen al inicio como `[x]`.
3. Avísame por Telegram: **"formulario Backup/DR listo"**.
4. Yo voy a:
   - Leer este archivo
   - Cerrar los tickets 018-021 con tu decisión
   - Actualizar el `BACKUP-DR-DESIGN` con los parámetros
   - Generar el runbook de Fase 0 listo para que ejecutes (o que yo ejecute si la ventana de mantenimiento está abierta)

---

## 📚 Referencias

- [[BACKUP-DR-OWNER-PROJECT]] — proyecto owner raíz
- [[BACKUP-DR-DESIGN]] — diseño congelado, 34 KB, capas A-G
- [[BACKUP-DR-RUNBOOK]] — runbook operativo (se actualizará tras tus respuestas)
- [[00-index]] — índice de docs Backup/DR
- [[RESTORE-DRILL-TEMPLATE]] — template para drills mensuales

## 📝 Convention

- **Formularios** del proyecto → `30-resources/aranea/03-storage/backup-dr/` (junto al diseño y runbook).
- **Tickets formales** → `10-projects/Aranea/05-tickets/` (uno por owner-task o blocker).
- Las respuestas del formulario se vuelcan a los tickets y actualizan el `BACKUP-DR-DESIGN` por referencia, no se duplica contenido.
