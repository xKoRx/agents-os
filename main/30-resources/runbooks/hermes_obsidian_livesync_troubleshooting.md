---
type: runbook
scope: service
created: 2026-06-29
updated: 2026-06-29
area: "[[Personal]]"
entities: []
related: []
aliases:
  - Troubleshooting de Obsidian LiveSync en Hermes
  - Hermes Obsidian LiveSync Setup
confidence: verified
source_session: "368404ab-3fb1-430d-890b-818e5b654c67"
load_policy: manual
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/runbook
  - scope/service
  - tech/couchdb
  - tech/linux
  - tech/obsidian
  - tool/hermes
---
qwasd
asd
asdasdas
# Hermes + Obsidian LiveSync — Setup y Troubleshooting

> Documento operativo para recordar qué se hizo, cómo conectarse al Obsidian headless de Hermes y cómo diagnosticar problemas futuros.

## 1. Estado final esperado

### Host

```txt
VM Hermes / Agent: 192.168.31.122
Usuario operativo: hermes
Vault local: /home/hermes/obsidian/SecondBrain/main
Backend LiveSync / CouchDB: 192.168.31.32
DB LiveSync: main_vault
```

### Storage

La VM quedó con dos discos separados:

```txt
/dev/sda 32 GB  → sistema operativo Ubuntu
/dev/sdb 50 GB  → datos de Hermes
```

El disco de Hermes quedó montado como `/home/hermes`:

```txt
/dev/sdb1 → /home/hermes
FSTYPE: ext4
LABEL: HERMES_DATA
UUID: a26bd76f-be2f-44e4-901a-9d9e34523526
```

Línea agregada a `/etc/fstab`:

```fstab
UUID=a26bd76f-be2f-44e4-901a-9d9e34523526 /home/hermes ext4 defaults,noatime 0 2
```

Validación final reportada:

```txt
/home/hermes está montado en /dev/sdb1
Tamaño: 49 GB
Usado después de migración: ~2.9 GB
Libre: ~44 GB
Vault sincronizado: ~62 MB
```

### Servicios relevantes

```txt
xvfb-obsidian.service       → display virtual :99
fluxbox-obsidian.service    → window manager mínimo
obsidian-headless.service   → Obsidian corriendo contra :99
x11vnc-obsidian.service     → VNC local en 127.0.0.1:5900
novnc-obsidian.service      → noVNC local en 127.0.0.1:6080
```

Servicios que deben quedar vivos para LiveSync sin pantalla remota:

```txt
xvfb-obsidian.service
fluxbox-obsidian.service
obsidian-headless.service
```

Servicios opcionales, solo para abrir UI remota:

```txt
x11vnc-obsidian.service
novnc-obsidian.service
```

---

## 2. Qué se hizo

### 2.1 Problema inicial

La VM tenía Obsidian, Xvfb y VNC parcialmente configurados, pero había varios problemas:

- El usuario `hermes` no tenía acceso SSH directo estable.
- Se estaba peleando con Apple Screen Sharing y VNC por contraseña.
- El vault local tenía riesgo de placeholders creados antes del initial sync.
- `/home/hermes` estaba usando el disco raíz de 32 GB.
- El disco de 50 GB existía, pero estaba vacío, sin formato y sin montar.
- Había confusión entre password Linux/SSH, password VNC, passphrase de LiveSync y Setup URI.

### 2.2 Decisión importante

Se decidió resetear solo la capa Obsidian/LiveSync, manteniendo lo útil:

```txt
Mantener:
- Ubuntu
- usuario hermes
- paquetes instalados
- Obsidian AppImage / squashfs-root
- scripts operativos
- servicios re-creables

Resetear:
- estado local de Obsidian
- vault local previo
- VNC roto
- configuración local contaminada
```

### 2.3 Reset de Obsidian/LiveSync

Se detuvieron servicios:

```bash
sudo systemctl stop novnc-obsidian.service || true
sudo systemctl stop x11vnc-obsidian.service || true
sudo systemctl stop obsidian-headless.service || true
sudo systemctl stop fluxbox-obsidian.service || true
sudo systemctl stop xvfb-obsidian.service || true
```

Se mataron procesos residuales:

```bash
sudo pkill -u hermes -f obsidian || true
sudo pkill -u hermes -f x11vnc || true
sudo pkill -u hermes -f Xvfb || true
sudo pkill -u hermes -f fluxbox || true
sudo pkill -f websockify || true
```

Se dejó el vault local vacío antes del initial sync:

```txt
/home/hermes/obsidian/SecondBrain/main
```

Regla crítica:

```txt
No crear placeholders antes de LiveSync.
No crear AGENTS.md local.
No crear estructura base local.
El vault real viene desde CouchDB / main_vault.
```

### 2.4 Migración de storage

Hermes hizo discovery read-only y detectó:

```txt
/dev/sda 32 GB → root disk
/dev/sdb 50 GB → raw disk, vacío, sin filesystem
```

Se autorizó:

1. Crear tabla GPT en `/dev/sdb`.
2. Crear partición única `/dev/sdb1`.
3. Formatear `/dev/sdb1` como ext4 con label `HERMES_DATA`.
4. Montar temporalmente en `/mnt/hermes-new`.
5. Copiar `/home/hermes` actual con `rsync -aAXH`.
6. Respaldar el home anterior como:

```txt
/home/hermes.before-disk-move-20260630-021546
```

7. Montar `/dev/sdb1` permanentemente en `/home/hermes` por UUID.
8. Validar permisos.

Permisos finales:

```txt
/home/hermes                       755  hermes:hermes
/home/hermes/.ssh                  700  hermes:hermes
/home/hermes/.ssh/authorized_keys  600  hermes:hermes
```

Carpetas operativas creadas/preservadas:

```txt
/home/hermes/apps
/home/hermes/bin
/home/hermes/obsidian/SecondBrain/main
/home/hermes/skills
/home/hermes/workspaces
/home/hermes/docs
/home/hermes/logs
/home/hermes/tmp
/home/hermes/reset-backups
```

### 2.5 Separación correcta de responsabilidades

El disco de 32 GB queda para sistema:

```txt
/usr/bin
/etc
systemd units
paquetes apt
logs de sistema
xvfb
x11vnc
novnc
fluxbox
websockify
curl
jq
git
```

El disco Hermes de 50 GB queda para usuario/agente:

```txt
/home/hermes/apps                 → apps portables, Obsidian AppImage, squashfs-root
/home/hermes/bin                  → wrappers propios
/home/hermes/obsidian             → vault local
/home/hermes/skills               → skills propias del agente
/home/hermes/workspaces           → repos/proyectos de trabajo del agente
/home/hermes/docs                 → documentación operativa local si no corresponde al vault
/home/hermes/logs                 → logs propios de Hermes
/home/hermes/tmp                  → temporales/cache propios del agente
```

Regla:

```txt
Apps de sistema van por apt y viven fuera de /home/hermes.
Apps portables o propias de Hermes pueden vivir en /home/hermes/apps.
```

### 2.6 noVNC funcionando

Se dejó noVNC en lugar de Apple Screen Sharing directo.

Puertos internos:

```txt
x11vnc: 127.0.0.1:5900
noVNC:  127.0.0.1:6080
```

Ambos quedan solo en localhost dentro de la VM. Para acceder desde Mac se usa túnel SSH.

### 2.7 LiveSync configurado

Desde noVNC se abrió Obsidian en:

```txt
/home/hermes/obsidian/SecondBrain/main
```

Luego:

1. Se instaló `Self-hosted LiveSync`.
2. Se pegó la Setup URI generada desde el vault bueno en Mac.
3. Se ingresó la passphrase de LiveSync.
4. Se ejecutó initial sync.
5. El vault local quedó sincronizado y pesó ~62 MB.

Nota:

```txt
El plugin reportó cerca de 1 GB transferido, pero el vault final pesó 62 MB.
Esto probablemente fue transferencia acumulada, metadata, revisiones, cache o historial interno, no tamaño final en disco.
```

---

## 3. Cómo conectarse al Obsidian de Hermes más adelante

### 3.1 Conexión normal por noVNC

En tu Mac, abre un túnel SSH:

```bash
ssh -N -L 127.0.0.1:6080:127.0.0.1:6080 agent@192.168.31.122
```

Deja esa terminal abierta.

Luego abre en navegador:

```txt
http://127.0.0.1:6080/vnc.html?autoconnect=true&resize=scale
```

Eso abre la UI web de noVNC y muestra el escritorio virtual donde corre Obsidian.

### 3.2 Cerrar conexión

Cuando termines:

1. Cierra la pestaña del navegador.
2. En la terminal del túnel, presiona:

```txt
Ctrl + C
```

Esto solo cierra tu acceso visual. No apaga Obsidian si el servicio sigue activo.

### 3.3 Apagar la pantalla remota, dejando LiveSync funcionando

Si ya no necesitas UI remota, puedes detener noVNC y x11vnc:

```bash
ssh hermes@192.168.31.122

sudo systemctl stop novnc-obsidian.service
sudo systemctl stop x11vnc-obsidian.service
```

Validar:

```bash
systemctl is-active xvfb-obsidian.service
systemctl is-active fluxbox-obsidian.service
systemctl is-active obsidian-headless.service
systemctl is-active x11vnc-obsidian.service || true
systemctl is-active novnc-obsidian.service || true
```

Esperado:

```txt
active
active
active
inactive
inactive
```

### 3.4 Volver a abrir pantalla remota

Si necesitas volver a ver Obsidian:

```bash
ssh hermes@192.168.31.122

sudo systemctl start x11vnc-obsidian.service
sudo systemctl start novnc-obsidian.service
```

En tu Mac:

```bash
ssh -N -L 127.0.0.1:6080:127.0.0.1:6080 hermes@192.168.31.122
```

Abrir:

```txt
http://127.0.0.1:6080/vnc.html?autoconnect=true&resize=scale
```

---

## 4. Comandos de validación rápida

### 4.1 Estado de servicios

```bash
systemctl status xvfb-obsidian.service --no-pager
systemctl status fluxbox-obsidian.service --no-pager
systemctl status obsidian-headless.service --no-pager
systemctl status x11vnc-obsidian.service --no-pager
systemctl status novnc-obsidian.service --no-pager
```

Resumen rápido:

```bash
systemctl is-active xvfb-obsidian.service
systemctl is-active fluxbox-obsidian.service
systemctl is-active obsidian-headless.service
systemctl is-active x11vnc-obsidian.service || true
systemctl is-active novnc-obsidian.service || true
```

### 4.2 Procesos

```bash
pgrep -a Xvfb || true
pgrep -a fluxbox || true
pgrep -a obsidian || true
pgrep -a x11vnc || true
pgrep -a websockify || true
```

### 4.3 Puertos

```bash
ss -ltnp | grep -E '5900|6080' || true
```

Esperado si UI remota está activa:

```txt
127.0.0.1:5900  x11vnc
127.0.0.1:6080  websockify/noVNC
```

### 4.4 Storage

```bash
findmnt /home/hermes
df -hT /home/hermes
lsblk -f
```

Esperado:

```txt
/home/hermes → /dev/sdb1 ext4
```

### 4.5 Tamaño del vault

```bash
du -sh /home/hermes/obsidian/SecondBrain/main
du -h -d 1 /home/hermes/obsidian/SecondBrain/main | sort -h
```

### 4.6 Cantidad de notas Markdown

```bash
find /home/hermes/obsidian/SecondBrain/main -type f -name '*.md' | wc -l
```

### 4.7 Carpetas principales del vault

```bash
find /home/hermes/obsidian/SecondBrain/main -maxdepth 2 -type d | sort | head -100
```

### 4.8 Cache/config de Obsidian

```bash
du -sh \
  /home/hermes/.config/obsidian \
  /home/hermes/.cache \
  /home/hermes/.local/share \
  2>/dev/null
```

---

## 5. Qué NO hacer

### 5.1 No escribir antes de LiveSync

Nunca hacer esto antes del initial sync:

```txt
crear AGENTS.md
crear carpetas base
crear placeholders
crear tests de escritura
crear estructura nueva
```

La regla es:

```txt
Primero sincronizar.
Después discovery read-only.
Después escribir solo si hay permiso.
```

### 5.2 No escribir directo a CouchDB

Hermes no debe escribir directamente en CouchDB.

Correcto:

```txt
Hermes escribe Markdown local → Obsidian/LiveSync sincroniza.
```

Incorrecto:

```txt
Hermes escribe directo a CouchDB.
```

### 5.3 No usar rsync con los Macs

No usar rsync bidireccional entre Mac y Hermes para el vault. Puede pisar cambios.

La fuente de sincronización es:

```txt
Self-hosted LiveSync + CouchDB main_vault
```

### 5.4 No tocar `.obsidian/` por shell

No modificar `.obsidian/` manualmente por terminal salvo troubleshooting explícito y con backup.

---

## 6. Flujo correcto para Hermes como agente

Hermes debe trabajar sobre el vault existente, no crear uno paralelo.

Reglas:

```txt
El vault Obsidian existente es la fuente de verdad.
Hermes no crea estructura base propia.
Hermes primero lee, entiende y respeta la estructura existente.
Hermes solo agrega contenido donde las reglas del vault lo permiten.
```

Flujo:

1. Discovery read-only.
2. Leer reglas del vault.
3. Identificar carpetas permitidas.
4. Reportar estado.
5. Esperar autorización para escribir.
6. Crear solo archivos nuevos cuando corresponda.
7. No modificar notas existentes sin permiso.

Prompt recomendado para discovery:

```txt
LiveSync ya quedó configurado.

Ahora haz discovery read-only del vault:

/home/hermes/obsidian/SecondBrain/main

Reglas:
- No crees archivos.
- No modifiques archivos.
- No borres archivos.
- No ejecutes healthchecks que escriban.
- No toques .obsidian/.
- No crees placeholders.
- No reorganices carpetas.

Reporta:
1. cantidad total de archivos .md
2. carpetas principales detectadas
3. existencia de 80-agents/AGENTS.md, conventions.md, write-policy.md
4. existencia de 90-graphify/INDEX.md
5. proyectos/sistemas relacionados con Hermes
6. dónde puedo escribir con seguridad según reglas existentes
7. riesgos o inconsistencias
8. próximo paso recomendado
```

---

## 7. Troubleshooting

### 7.1 No carga noVNC en el browser

Verificar túnel en Mac:

```bash
lsof -iTCP:6080 -sTCP:LISTEN
```

Debe aparecer un proceso `ssh`.

Verificar servicios en VM:

```bash
ssh hermes@192.168.31.122

systemctl is-active x11vnc-obsidian.service
systemctl is-active novnc-obsidian.service
ss -ltnp | grep -E '5900|6080' || true
```

Reiniciar UI remota:

```bash
sudo systemctl restart x11vnc-obsidian.service
sudo systemctl restart novnc-obsidian.service
```

### 7.2 Obsidian no aparece en noVNC

Verificar servicios:

```bash
systemctl status xvfb-obsidian.service --no-pager
systemctl status fluxbox-obsidian.service --no-pager
systemctl status obsidian-headless.service --no-pager
```

Ver logs:

```bash
journalctl -u obsidian-headless.service -n 100 --no-pager
```

Reiniciar stack gráfico:

```bash
sudo systemctl restart xvfb-obsidian.service
sudo systemctl restart fluxbox-obsidian.service
sudo systemctl restart obsidian-headless.service
sudo systemctl restart x11vnc-obsidian.service
sudo systemctl restart novnc-obsidian.service
```

### 7.3 El túnel SSH pide password

Eso es SSH, no VNC.

Validar que tu llave pública esté en:

```txt
/home/hermes/.ssh/authorized_keys
```

Permisos correctos:

```bash
ls -lah /home/hermes/.ssh
```

Esperado:

```txt
drwx------ .ssh
-rw------- authorized_keys
```

Probar con llave explícita desde Mac:

```bash
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes hermes@192.168.31.122
```

### 7.4 LiveSync no baja datos

Validar conectividad a CouchDB desde Hermes:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://192.168.31.32:5984
```

Esperado:

```txt
401
```

`401` es correcto: CouchDB responde y pide credenciales.

Si sale `000`, hay problema de red/firewall/ruta.

### 7.5 El vault pesa raro

Medir recursivo real:

```bash
du -sh /home/hermes/obsidian/SecondBrain/main
du -h -d 1 /home/hermes/obsidian/SecondBrain/main | sort -h
```

Revisar cache/config fuera del vault:

```bash
du -sh \
  /home/hermes/.config/obsidian \
  /home/hermes/.cache \
  /home/hermes/.local/share \
  2>/dev/null
```

### 7.6 El disco root queda con poco espacio

Existe backup antiguo del home antes de moverlo:

```txt
/home/hermes.before-disk-move-20260630-021546
```

No borrarlo hasta confirmar durante varios días que:

- LiveSync funciona.
- Obsidian arranca.
- `/home/hermes` está bien en `/dev/sdb1`.
- SSH funciona.
- No falta nada de apps/scripts.

Cuando esté todo validado:

```bash
sudo du -sh /home/hermes.before-disk-move-20260630-021546
sudo rm -rf /home/hermes.before-disk-move-20260630-021546
```

---

## 8. Comandos rápidos útiles

### Conectarse por SSH

```bash
ssh hermes@192.168.31.122
```

### Abrir noVNC

```bash
ssh -N -L 127.0.0.1:6080:127.0.0.1:6080 hermes@192.168.31.122
```

```txt
http://127.0.0.1:6080/vnc.html?autoconnect=true&resize=scale
```

### Ver estado de Hermes

```bash
ssh hermes@192.168.31.122
hermes-vault-status
```

### Reiniciar solo Obsidian

```bash
sudo systemctl restart obsidian-headless.service
```

### Reiniciar stack completo UI + Obsidian

```bash
sudo systemctl restart xvfb-obsidian.service
sudo systemctl restart fluxbox-obsidian.service
sudo systemctl restart obsidian-headless.service
sudo systemctl restart x11vnc-obsidian.service
sudo systemctl restart novnc-obsidian.service
```

### Detener pantalla remota

```bash
sudo systemctl stop novnc-obsidian.service
sudo systemctl stop x11vnc-obsidian.service
```

### Iniciar pantalla remota

```bash
sudo systemctl start x11vnc-obsidian.service
sudo systemctl start novnc-obsidian.service
```

---

## 9. Checklist post-mantenimiento

Después de cualquier cambio importante:

```bash
findmnt /home/hermes
df -hT /home/hermes
systemctl is-active xvfb-obsidian.service
systemctl is-active fluxbox-obsidian.service
systemctl is-active obsidian-headless.service
find /home/hermes/obsidian/SecondBrain/main -type f -name '*.md' | wc -l
du -sh /home/hermes/obsidian/SecondBrain/main
```

Checklist lógico:

```txt
[ ] /home/hermes sigue montado en /dev/sdb1
[ ] Obsidian sigue activo
[ ] LiveSync sigue funcionando
[ ] noVNC solo se enciende cuando se necesita UI
[ ] Hermes no creó estructura paralela
[ ] Hermes no escribió antes de discovery
[ ] Vault local sigue siendo main_vault
```

---

## 10. Decisión final

La arquitectura elegida:

```txt
VM Hermes:
  /home/hermes en disco dedicado de 50 GB
  Obsidian corriendo semi-headless con Xvfb
  LiveSync sincronizando main_vault
  noVNC solo para mantenimiento visual
  Hermes/agentes leen y escriben Markdown local bajo reglas del vault
```

No usar:

```txt
rsync bidireccional
CouchDB directo desde agentes
vault paralelo para Hermes
Apple Screen Sharing directo
placeholders antes del sync
```
