---
type: runbook
schema_version: 1
scope: project
created: 2026-08-10
updated: 2026-08-10
area: "[[Aranea]]"
project:
application:
entities:
  - "[[Aranea]]"
related: []
aliases: []
confidence: medium
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/project
  - area/aranea
---

## Propósito

Procedimiento operacional histórico de [[Aranea]]; validar los datos volátiles antes de ejecutarlo.

## Procedimiento

# RUNBOOK — Migración HTTPS interna de servicios Aranea

**Estado:** activo  
**Fecha base:** 2026-07-17  
**Ejecutor principal:** Hermes / Ariadna  
**Ámbito:** servicios HTTP/HTTPS internos publicados mediante Traefik  
**Dominio canónico:** `*.lab.aranea.cl`  
**Acceso permitido:** LAN Aranea y Tailscale mediante Split DNS  
**Tags sugeridos:** `#aranea #networking #traefik #tls #letsencrypt #pihole #tailscale #runbook`

---

## 0. Decisión operativa

No se deben migrar todos los servicios de una sola vez ni crear rutas “por si acaso”.

La política correcta es:

1. Inventariar y clasificar el servicio.
2. Probar el backend directamente desde Traefik.
3. Respaldar su archivo dinámico.
4. Agregar un router HTTPS nuevo sin retirar el router antiguo.
5. Validar router, backend y certificado localmente.
6. Crear el DNS interno en Pi-hole.
7. Validar desde LAN y desde Tailscale.
8. Probar la función real de la aplicación.
9. Registrar evidencia.
10. Recién después pasar al servicio siguiente.

**Máximo: un servicio por cambio operativo.**

Los servicios simples pueden migrarse consecutivamente, pero cada uno debe cerrar su propio ciclo de validación. Los servicios especiales o críticos deben detenerse en un gate antes de modificar la aplicación backend.

---

## 1. Objetivo

Migrar progresivamente los servicios web internos desde:

```text
http://<servicio>.lab.aranea
```

hacia:

```text
https://<servicio>.lab.aranea.cl
```

manteniendo durante la transición:

- el dominio antiguo operativo;
- acceso exclusivo desde LAN/Tailscale;
- puertos de entrada desde Internet cerrados;
- backend interno HTTP cuando corresponda;
- certificado wildcard público válido;
- rollback inmediato por servicio;
- configuraciones especiales existentes, como CORS, autenticación, WebSocket, headers y reescrituras.

---

## 2. Arquitectura vigente

### 2.1 Componentes centrales

| Componente | Dirección / ruta | Función |
|---|---|---|
| Traefik | `192.168.31.11` | Reverse proxy interno |
| Pi-hole | `192.168.31.31` | DNS interno |
| LAN | `192.168.31.0/24` | Red de servicios |
| Tailscale Split DNS | `lab.aranea.cl -> 192.168.31.31` | Resolución remota |
| ClouDNS | zona `aranea.cl` | DNS autoritativo para ACME DNS-01 |
| Let’s Encrypt | resolver `letsencrypt` | Certificados públicos |
| Step CA | resolver `stepca` | Resolver antiguo, aún conservado |

### 2.2 Traefik

```text
Versión observada:       3.7.5
Binario:                 /usr/bin/traefik
Unit systemd:            /etc/systemd/system/traefik.service
Configuración estática:  /etc/traefik/traefik.yaml
Configuración dinámica:  /etc/traefik/dynamic/
Log principal:           /var/log/traefik/traefik.log
Access log:              /var/log/traefik/access.log
ACME Let’s Encrypt:      /etc/traefik/ssl/acme.json
ACME Step CA:            /etc/traefik/ssl/acme-stepca.json
Secretos ClouDNS:        /etc/traefik/secrets/
Drop-in ClouDNS:         /etc/systemd/system/traefik.service.d/cloudns.conf
```

### 2.3 Certificado vigente

El almacenamiento ACME contiene un certificado válido para:

```text
lab.aranea.cl
*.lab.aranea.cl
```

El wildcard cubre exactamente un nivel:

```text
minio.lab.aranea.cl             cubierto
frigate.lab.aranea.cl           cubierto
echo-core.lab.aranea.cl         cubierto
dev.echo.lab.aranea.cl          NO cubierto
```

Por eso los nombres canónicos deben usar **un solo label antes de `lab.aranea.cl`**. Para ambientes o componentes compuestos, usar nombres planos:

```text
echo-core-dev.lab.aranea.cl
echo-core-prod.lab.aranea.cl
grafana.lab.aranea.cl
```

No usar:

```text
dev.echo.core.lab.aranea.cl
```

sin diseñar antes certificados adicionales.

---

## 3. Reglas no negociables para Hermes

### 3.1 Seguridad

Hermes debe obedecer estas restricciones:

- No crear registros públicos `A` o `AAAA` para servicios internos en ClouDNS.
- No abrir ni redirigir puertos de OPNsense hacia Traefik.
- No exponer servicios directamente a Internet.
- No eliminar Step CA durante esta migración.
- No borrar, truncar ni regenerar `acme.json`.
- No mostrar claves privadas ni passwords.
- No ejecutar `cat /etc/traefik/ssl/acme.json`.
- No pegar el password de ClouDNS en comandos o documentación.
- No retirar el dominio antiguo durante la misma sesión.
- No cambiar múltiples servicios en un solo archivo o commit.
- No editar bases internas de Pi-hole directamente.
- No reemplazar middlewares existentes sin entender su función.
- No cambiar la aplicación backend antes de comprobar que sea necesario.
- No usar un router HTTP para publicar bases de datos o brokers.

### 3.2 Disciplina de cambio

Antes de cada mutación, Hermes debe mostrar:

```text
Servicio:
Archivo:
Backend:
Dominio antiguo:
Dominio nuevo:
Middlewares actuales:
Riesgos especiales:
Rollback:
```

Después debe pedir o registrar el gate correspondiente según el modo de trabajo definido por el propietario.

### 3.3 Evidencia mínima

Cada servicio debe cerrar con evidencia de:

- archivo antes y después;
- backend directo operativo;
- router HTTPS operativo;
- certificado válido;
- DNS Pi-hole correcto;
- DNS Tailscale correcto;
- aplicación funcional;
- dominio antiguo todavía operativo;
- ausencia de errores nuevos;
- rollback disponible.

---

## 4. Qué servicios sí deben pasar por Traefik

### 4.1 Candidatos normales

- interfaces web;
- dashboards;
- APIs HTTP/HTTPS;
- aplicaciones con WebSocket;
- consolas administrativas web que el propietario apruebe;
- endpoints internos que necesiten un hostname y TLS confiable.

### 4.2 Servicios que NO deben agregarse como router HTTP

No crear routers HTTP para:

- PostgreSQL;
- MongoDB;
- Kafka;
- etcd;
- MQTT nativo;
- Milvus nativo;
- Ceph MON/OSD/MGR;
- iSCSI;
- NFS;
- RTSP;
- SSH;
- RDP;
- APIs internas no destinadas a clientes web, salvo aprobación específica.

Estos protocolos requieren acceso directo, firewall, Tailscale, VLAN o routers TCP/UDP diseñados expresamente. No se deben meter detrás de un router HTTP genérico.

### 4.3 Planos de administración críticos

Los siguientes no deben migrarse automáticamente:

- OPNsense;
- Proxmox;
- TrueNAS;
- Pi-hole admin;
- paneles de almacenamiento;
- interfaces de quorum o cluster.

Requieren una decisión explícita de seguridad. Centralizar todos los planos de control detrás de un único proxy aumenta el impacto de una falla de Traefik o de autenticación.

---

## 5. Inventario inicial obligatorio

Antes de continuar con nuevos servicios, Hermes debe producir el inventario real desde el LXC Traefik.

### 5.1 Estado base

```bash
hostname
date -Is
/usr/bin/traefik version
systemctl is-active traefik
systemctl status traefik --no-pager -l
```

### 5.2 Archivos dinámicos

```bash
find /etc/traefik/dynamic \
  -maxdepth 1 \
  -type f \
  \( -name '*.yaml' -o -name '*.yml' \) \
  -printf '%f\n' |
sort
```

### 5.3 Routers y backends declarados

```bash
grep -RniE \
  'rule:|entryPoints:|service:|middlewares:|certResolver:|url:' \
  /etc/traefik/dynamic
```

### 5.4 Middlewares disponibles

```bash
grep -RniE \
  'middlewares:|ipAllowList:|basicAuth:|headers:|redirectScheme:|forwardAuth:' \
  /etc/traefik/dynamic
```

### 5.5 Certificado wildcard sin mostrar secretos

```bash
jq -r '
  .. |
  objects |
  select(has("domain")) |
  select(.domain.main? != null) |
  [
    .domain.main,
    ((.domain.sans // []) | join(", "))
  ] |
  @tsv
' /etc/traefik/ssl/acme.json
```

Esperado:

```text
lab.aranea.cl    *.lab.aranea.cl
```

### 5.6 Permisos sensibles

```bash
stat -c '%a %U:%G %n' \
  /etc/traefik/ssl/acme.json \
  /etc/traefik/secrets/* \
  /etc/systemd/system/traefik.service.d/cloudns.conf
```

`acme.json` y los archivos con secretos deben mantenerse restringidos.

---

## 6. Catálogo inicial de servicios Aranea

Este catálogo combina la configuración Traefik observada y el inventario actual. Hermes debe verificar cada endpoint antes de usarlo.

### 6.1 Migrados

| Servicio | Dominio canónico | Backend | Estado |
|---|---|---:|---|
| MinIO Console | `minio.lab.aranea.cl` | `192.168.31.92:9090` | migrado |
| Frigate | `frigate.lab.aranea.cl` | `192.168.31.41:5000` | migrado |

### 6.2 Preparados para migración con endpoint conocido

| Orden | Servicio | Dominio propuesto | Backend | Complejidad |
|---:|---|---|---|---|
| 1 | Temporal UI | `temporal.lab.aranea.cl` | `192.168.31.46:8080` | baja |
| 2 | Grafana | `grafana.lab.aranea.cl` | `192.168.31.60:3000` | baja/media |
| 3 | Prometheus | `prometheus.lab.aranea.cl` | `192.168.31.60:9090` | baja |
| 4 | Jaeger UI | `jaeger.lab.aranea.cl` | `192.168.31.60:16686` | baja |
| 5 | MinIO API | `minio-api.lab.aranea.cl` | `192.168.31.92:9000` | media/alta |
| 6 | Obsidian Sync | `obsidian-sync.lab.aranea.cl` | `192.168.31.32:5984` | alta |
| 7 | Hermes Dashboard | `dashboard.lab.aranea.cl` | `127.0.0.1:19119` | alta |
| 8 | Traefik Dashboard | `traefik.lab.aranea.cl` | `api@internal` | alta |

### 6.3 Servicios que requieren descubrimiento

| Servicio | Dominio propuesto | Dato faltante | Nota |
|---|---|---|---|
| Home Assistant | `homeassistant.lab.aranea.cl` | IP/puerto real | requiere trusted proxy |
| EMQX Dashboard | `emqx.lab.aranea.cl` | IP/puerto HTTP real | solo dashboard, no MQTT |
| Pi-hole Admin | `pihole.lab.aranea.cl` | puerto/ruta/version | plano crítico |
| Attu/Milvus UI | `attu.lab.aranea.cl` | confirmar que exista | no publicar Milvus nativo |
| Otros dashboards | nombre plano | backend real | inventariar primero |

### 6.4 ARGUS: no publicar todo

En ARGUS existen varios puertos, pero no todos deben transformarse en sitios web.

| Componente | Puerto | Decisión inicial |
|---|---:|---|
| Grafana | 3000 | sí |
| Prometheus | 9090 | sí, restringido |
| Jaeger UI | 16686 | sí, restringido |
| Loki HTTP | 3100 | no por defecto |
| Node Exporter | 9100 | no |
| Promtail metrics | 9080 | no |
| OpenSearch | 9200 loopback | no |
| OTLP gRPC/HTTP | 4317/4318 | no |
| Jaeger gRPC | 16685 | no |
| métricas internas | varios | no |

---

## 7. Orden recomendado de migración

### Ola 1 — Simple y de bajo riesgo

1. Temporal UI.
2. Grafana.
3. Prometheus.
4. Jaeger UI.

Objetivo: validar el patrón repetible en servicios web normales.

### Ola 2 — Aplicaciones con particularidades

5. MinIO API.
6. Obsidian Sync.
7. Hermes Dashboard.
8. Traefik Dashboard.

Objetivo: tratar CORS, API, auth, headers y reescritura de origen.

### Ola 3 — Requieren configuración del backend

9. Home Assistant.
10. EMQX Dashboard.
11. Otros dashboards detectados.

### Ola 4 — Decisión de arquitectura separada

- OPNsense;
- Proxmox;
- TrueNAS;
- Pi-hole admin;
- servicios TCP/UDP;
- planos de gestión del cluster.

---

## 8. Flujo estándar por servicio

Las siguientes fases se repiten para cada servicio.

---

## Fase A — Descubrimiento

### A1. Identificar el archivo

```bash
find /etc/traefik/dynamic \
  -maxdepth 1 \
  -type f \
  -iname '*NOMBRE*' \
  -print
```

Si no aparece:

```bash
grep -Rli \
  'Host(`NOMBRE.lab.aranea`)' \
  /etc/traefik/dynamic
```

### A2. Leer el archivo completo

```bash
nl -ba /etc/traefik/dynamic/ARCHIVO.yaml
```

Hermes debe registrar:

- router antiguo;
- entrypoint;
- service;
- middlewares;
- `passHostHeader`;
- backend;
- cualquier TLS actual;
- headers;
- CORS;
- auth;
- path rules.

### A3. Probar backend directo

Desde el LXC Traefik:

```bash
curl -sS \
  -o /dev/null \
  -D - \
  http://IP:PUERTO/
```

O para mostrar un resumen:

```bash
curl -sS \
  -o /dev/null \
  -w 'HTTP %{http_code} connect=%{time_connect}s total=%{time_total}s\n' \
  http://IP:PUERTO/
```

Resultados aceptables:

- `200`;
- `204`;
- `301`, `302`, `307` o `308` entendido;
- `401` o `403` esperado por autenticación.

Detenerse si:

- timeout;
- connection refused;
- `5xx`;
- redirect hacia IP incorrecta;
- redirect hacia dominio público/antiguo inesperado;
- backend solo HTTPS desconocido;
- certificado interno roto.

### A4. Clasificar el servicio

```text
SIMPLE_HTTP
WEBSOCKET
CORS
API
AUTH
HOST_SENSITIVE
PATH_SENSITIVE
LARGE_UPLOAD
MANAGEMENT_PLANE
NON_HTTP
```

Si es `MANAGEMENT_PLANE` o `NON_HTTP`, detener migración automática.

---

## Fase B — Respaldo

### B1. Backup versionado

```bash
FILE=/etc/traefik/dynamic/ARCHIVO.yaml
STAMP=$(date +%Y%m%d-%H%M%S)

cp -a "$FILE" "${FILE}.bak-${STAMP}"

stat -c '%a %U:%G %s %n' \
  "$FILE" \
  "${FILE}.bak-${STAMP}"
```

Nunca reutilizar un único `.before-https`, porque se puede sobrescribir evidencia previa.

### B2. Capturar línea inicial del log

```bash
TRAEFIK_LOG=/var/log/traefik/traefik.log
LOG_START=$(wc -l < "$TRAEFIK_LOG")
echo "$LOG_START"
```

Esto evita confundir errores antiguos con el cambio actual.

---

## Fase C — Agregar router HTTPS dual

### C1. Plantilla base

Preservar el router antiguo y el servicio existente. Agregar solo un router nuevo:

```yaml
http:
  routers:
    servicio:
      rule: "Host(`servicio.lab.aranea`)"
      entryPoints:
        - web
      service: servicio
      middlewares:
        - lan-only@file

    servicio-https:
      rule: "Host(`servicio.lab.aranea.cl`)"
      entryPoints:
        - websecure
      service: servicio
      middlewares:
        - lan-only@file
      tls:
        certResolver: letsencrypt

  services:
    servicio:
      loadBalancer:
        passHostHeader: true
        servers:
          - url: "http://IP:PUERTO"
```

### C2. Reglas de edición

- Copiar al router nuevo los middlewares relevantes del router viejo.
- Mantener el mismo `service`.
- Mantener `passHostHeader` existente.
- No agregar `tls.domains` en cada router.
- No duplicar el servicio en otro archivo.
- No crear un nuevo certificado por servicio.
- No cambiar el backend a HTTPS salvo que la aplicación ya lo requiera.
- No eliminar el router HTTP antiguo.
- No agregar redirección global HTTP→HTTPS todavía.

### C3. Wildcard

El wildcard ya está almacenado. Por eso basta:

```yaml
tls:
  certResolver: letsencrypt
```

La declaración explícita:

```yaml
domains:
  - main: "lab.aranea.cl"
    sans:
      - "*.lab.aranea.cl"
```

debe mantenerse en el router que actualmente funciona como ancla de adquisición, hasta aprobar un diseño centralizado distinto. No repetirla sin necesidad.

### C4. Escritura atómica

Preparar el archivo fuera del directorio observado:

```bash
TMP=$(mktemp /tmp/traefik-service.XXXXXX.yaml)

cat >"$TMP" <<'EOF'
# YAML completo
EOF

nl -ba "$TMP"
```

Después:

```bash
install \
  -o root \
  -g root \
  -m 0644 \
  "$TMP" \
  /etc/traefik/dynamic/ARCHIVO.yaml

rm -f "$TMP"
```

Esto reduce el riesgo de que Traefik lea un archivo parcialmente escrito.

---

## Fase D — Validar carga dinámica

### D1. Esperar file provider

```bash
sleep 3
```

### D2. Mostrar solo logs nuevos

```bash
sed -n "$((LOG_START + 1)),\$p" \
  /var/log/traefik/traefik.log
```

Filtrado:

```bash
sed -n "$((LOG_START + 1)),\$p" \
  /var/log/traefik/traefik.log |
grep -iE \
  'error|ERR|SERVICIO|router|certificate|acme|file'
```

No usar un `grep` sobre todo el historial como única validación, porque muestra incidentes viejos.

### D3. Condiciones de detención

Detenerse y hacer rollback si aparece:

```text
Error occurred during watcher callback
field not found
middleware ... does not exist
service ... does not exist
router uses a nonexistent certificate resolver
Unable to obtain ACME certificate
yaml
cannot unmarshal
```

No reiniciar Traefik automáticamente para “probar suerte”.

---

## Fase E — Prueba local sin DNS

### E1. Router + backend + TLS

```bash
curl -Iv \
  --resolve servicio.lab.aranea.cl:443:127.0.0.1 \
  https://servicio.lab.aranea.cl/
```

Debe confirmar:

```text
Connected to servicio.lab.aranea.cl
subjectAltName matched "*.lab.aranea.cl"
SSL certificate verify ok
HTTP/2 200
```

También son aceptables respuestas esperadas como `302`, `401` o `403`.

### E2. Certificado

```bash
openssl s_client \
  -connect 127.0.0.1:443 \
  -servername servicio.lab.aranea.cl \
  </dev/null 2>/dev/null |
openssl x509 -noout \
  -subject \
  -issuer \
  -dates \
  -ext subjectAltName
```

Esperado:

```text
subject=CN=lab.aranea.cl
issuer=... Let's Encrypt ...
DNS:*.lab.aranea.cl, DNS:lab.aranea.cl
```

Detenerse si aparece:

```text
TRAEFIK DEFAULT CERT
```

Eso indica que el router o el certificado no se están asociando correctamente.

### E3. Validar hostname anterior

```bash
curl -I \
  --resolve servicio.lab.aranea:80:127.0.0.1 \
  http://servicio.lab.aranea/
```

El dominio antiguo debe seguir funcionando.

---

## Fase F — DNS interno en Pi-hole

Solo después de que la prueba local pase.

### F1. Registro

Crear en Pi-hole:

```text
servicio.lab.aranea.cl -> 192.168.31.11
```

No crear ese `A` en ClouDNS.

### F2. Verificación directa

```bash
dig @192.168.31.31 \
  servicio.lab.aranea.cl \
  +short
```

Esperado:

```text
192.168.31.11
```

### F3. Política DNS

Mantener registros explícitos por servicio. No activar wildcard DNS interno todavía.

Ventajas:

- inventario visible;
- menos rutas accidentales;
- cambios auditables;
- cada hostname requiere una decisión;
- evita que errores tipográficos resuelvan silenciosamente a Traefik.

---

## Fase G — Validación Tailscale/macOS

### G1. Resolver interno de Tailscale

```bash
tailscale dns query \
  servicio.lab.aranea.cl
```

Debe mostrar:

```text
Forwarding to resolver: 192.168.31.31
RCodeSuccess
TypeA 192.168.31.11
```

### G2. Estado Split DNS

```bash
tailscale dns status
```

Debe existir:

```text
Split DNS Routes:
  - lab.aranea.cl -> 192.168.31.31
```

### G3. Resolver nativo de macOS

```bash
dscacheutil -q host \
  -a name servicio.lab.aranea.cl
```

Esperado:

```text
name: servicio.lab.aranea.cl
ip_address: 192.168.31.11
```

### G4. Curl real

```bash
curl -Iv \
  https://servicio.lab.aranea.cl/
```

No usar `-k`.

### G5. Si `dig` funciona pero `dscacheutil` no

Reinstalar la configuración DNS local de Tailscale:

```bash
tailscale set --accept-dns=false
sleep 2
tailscale set --accept-dns=true

sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

sleep 3
dscacheutil -q host \
  -a name servicio.lab.aranea.cl
```

También puede bastar reiniciar el cliente Tailscale.

### G6. VPN corporativa

Cuando exista una VPN corporativa que pise el DNS:

1. Conectar VPN corporativa.
2. Reconectar Tailscale.
3. Confirmar `tailscale dns status`.
4. Confirmar `dscacheutil`.
5. Probar Chrome.

### G7. Chrome

Solo limpiar Chrome si el resolver nativo ya funciona.

```text
chrome://net-internals/#dns
```

Usar **Clear host cache**.

```text
chrome://net-internals/#sockets
```

Usar **Flush socket pools**.

Cerrar Chrome completamente con `⌘Q` y abrirlo de nuevo.

No culpar a Chrome mientras `dscacheutil` siga vacío.

---

## Fase H — Smoke test funcional

Un `HTTP 200` no basta. Probar la función principal del servicio.

### Ejemplos

#### Temporal

- abre la UI;
- lista namespaces;
- abre un workflow;
- navega historial;
- no hay errores de assets o WebSocket.

#### Grafana

- login;
- abrir dashboard;
- ejecutar consulta;
- cargar paneles;
- verificar Grafana Live si se usa;
- revisar redirects y cookies.

#### Prometheus

- abrir `/graph`;
- ejecutar `up`;
- revisar `/targets`;
- confirmar que no hay mixed content.

#### Jaeger

- cargar UI;
- listar servicios;
- buscar trazas;
- abrir una traza completa.

#### MinIO Console

- login;
- listar buckets;
- navegar objetos;
- no realizar cambios destructivos durante smoke test.

#### MinIO API

- usar cliente S3 real;
- listar buckets;
- subir un objeto pequeño de prueba;
- descargarlo;
- eliminar solo el objeto de prueba;
- validar firmas y endpoint;
- validar cargas grandes por separado.

#### Frigate

- cargar dashboard;
- abrir Live;
- abrir una cámara;
- revisar grabaciones;
- confirmar que no falla streaming.

#### Obsidian Sync

- autenticar;
- leer base;
- realizar cambio controlado;
- confirmar sincronización en dos clientes;
- preservar CORS;
- no cambiar todos los dispositivos en la misma sesión.

#### Hermes Dashboard

- cargar dashboard;
- autenticar;
- abrir perfil correcto;
- enviar mensaje de prueba;
- validar Origin y headers;
- confirmar que el túnel/local forward sigue operativo.

#### Traefik Dashboard

- autenticación obligatoria;
- abrir `/dashboard/`;
- revisar routers y services;
- no exponer `/api` sin protección.

---

## 9. Patrones especiales por servicio

---

## 9.1 Temporal UI

### Riesgo

Bajo. Normalmente funciona como aplicación HTTP detrás de un hostname.

### Patrón

```yaml
temporal-ui-https:
  rule: "Host(`temporal.lab.aranea.cl`)"
  entryPoints:
    - websecure
  service: temporal-ui
  middlewares:
    - lan-only@file
  tls:
    certResolver: letsencrypt
```

Backend conocido:

```text
http://192.168.31.46:8080
```

### Smoke test

- carga inicial;
- namespaces;
- workflows;
- historial;
- links internos.

---

## 9.2 Grafana

### Backend conocido

```text
http://192.168.31.60:3000
```

### Riesgos

- redirects al hostname antiguo;
- OAuth callback incorrecto;
- cookies ligadas a otra URL;
- `root_url`;
- Grafana Live/WebSocket.

### Regla

Primero probar sin cambiar Grafana. Si la UI redirige o falla login, revisar:

```ini
[server]
domain = grafana.lab.aranea.cl
root_url = https://grafana.lab.aranea.cl/
```

No modificar `grafana.ini` preventivamente.

### Smoke test

- login;
- dashboard;
- datasource;
- consulta;
- Grafana Live si se usa;
- cookies seguras.

---

## 9.3 Prometheus

### Backend conocido

```text
http://192.168.31.60:9090
```

### Riesgo

La UI permite consultas y revela topología interna. Debe conservar `lan-only`.

### Smoke test

```text
/graph
/targets
/alerts
```

No publicar Node Exporter ni métricas internas como sitios web.

---

## 9.4 Jaeger UI

### Backend conocido

```text
http://192.168.31.60:16686
```

### Smoke test

- UI;
- listado de servicios;
- búsqueda de trazas;
- detalle de spans.

No publicar automáticamente OTLP, gRPC, OpenSearch ni puertos de sampling.

---

## 9.5 MinIO API

### Backend conocido

```text
http://192.168.31.92:9000
```

### Dominio

```text
minio-api.lab.aranea.cl
```

### Reglas

- `passHostHeader: true`;
- hostname dedicado;
- no usar subpath;
- no mezclar console y API;
- conservar firmas S3;
- probar cliente real;
- no agregar límites de body arbitrarios;
- no cambiar timeouts sin evidencia.

### Smoke test mínimo

```bash
# Usar el cliente S3 ya configurado por Aranea.
# No documentar secretos.
```

Probar:

- list buckets;
- put de archivo pequeño;
- get;
- delete del objeto de prueba;
- una carga grande controlada.

---

## 9.6 Obsidian Sync / CouchDB

### Backend conocido

```text
http://192.168.31.32:5984
```

### Middleware existente

```text
obsidian-cors@file
```

### Reglas

- conservar CORS exactamente;
- no reemplazarlo por `lan-only` sin análisis;
- no cambiar la URL en todos los clientes;
- probar primero con un solo cliente;
- mantener acceso directo por Tailscale durante la transición;
- no mostrar credenciales CouchDB.

### Smoke test

- autenticación;
- lectura;
- escritura controlada;
- replicación;
- segundo cliente;
- conflictos;
- adjuntos.

---

## 9.7 Hermes Dashboard

### Backend conocido

```text
http://127.0.0.1:19119
```

### Configuración especial observada

- `passHostHeader: false`;
- middleware de reescritura de Origin;
- router HTTPS antiguo con Step CA;
- posible autenticación dedicada;
- dependencia del túnel/forward local.

### Reglas

Preservar:

```text
hermes-dashboard-origin-rewrite@file
passHostHeader: false
```

Antes de migrar:

```bash
curl -sS -I http://127.0.0.1:19119/
ss -lntp | grep 19119
```

No tocar el unit de Hermes dentro de esta migración.

### Smoke test

- login;
- perfil Ariadna;
- chat;
- envío de mensaje;
- respuesta;
- assets;
- conexiones persistentes.

---

## 9.8 Traefik Dashboard

### Backend

```text
api@internal
```

### Regla especial

Debe incluir rutas:

```yaml
rule: >
  Host(`traefik.lab.aranea.cl`) &&
  (PathPrefix(`/api`) || PathPrefix(`/dashboard`))
```

### Requisitos

- autenticación obligatoria;
- `lan-only`;
- usar `/dashboard/` con slash final;
- no publicar API sin auth;
- no quitar protección existente.

---

## 9.9 Home Assistant

### Estado

Endpoint real pendiente de descubrir.

### Requisito backend

Home Assistant detrás de reverse proxy requiere permitir los headers reenviados y confiar explícitamente en la IP de Traefik.

Ejemplo conceptual:

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 192.168.31.11
```

No aplicar hasta:

- confirmar IP real de Traefik desde Home Assistant;
- respaldar `configuration.yaml`;
- validar sintaxis;
- tener rollback;
- aprobar reinicio de Home Assistant.

### Smoke test

- login;
- dashboards;
- estados;
- WebSocket;
- historial;
- cámaras;
- app móvil;
- automatizaciones visibles.

---

## 9.10 EMQX

### Regla

Solo el dashboard HTTP puede pasar por router HTTP.

No pasar por este procedimiento:

```text
MQTT 1883
MQTTS 8883
otros listeners
```

Descubrir primero:

- IP real;
- puerto del dashboard;
- auth actual;
- base path;
- WebSocket MQTT si se usa.

---

## 10. Middlewares

### 10.1 `lan-only`

Middleware observado:

```yaml
ipAllowList:
  sourceRange:
    - 127.0.0.1/32
    - 192.168.31.0/24
```

No modificarlo durante una migración individual.

Tailscale funciona actualmente porque el tráfico enrutado llega de una forma compatible con la política existente. Cualquier cambio de SNAT o subnet router exige una revisión separada.

### 10.2 CORS

No copiar CORS genérico a todas las aplicaciones.

Solo aplicaciones que lo necesiten, como Obsidian Sync, deben conservar su middleware específico.

### 10.3 Auth

`lan-only` no reemplaza la autenticación de la aplicación.

Para dashboards administrativos:

- conservar auth propia;
- conservar Basic Auth o Forward Auth existente;
- no inventar credenciales;
- no crear un middleware nuevo sin respaldo y aprobación.

### 10.4 Redirect HTTP→HTTPS

No activar redirección global todavía.

Una redirección global también afectaría los dominios antiguos `*.lab.aranea`, que aún no tienen certificados públicos válidos.

La redirección se diseña al final, cuando:

- todos los servicios aprobados estén migrados;
- clientes actualizados;
- dominios antiguos listos para retiro;
- Step CA ya no sea necesaria para rutas activas.

---

## 11. Rollback por servicio

### 11.1 Cuándo hacer rollback

- error de YAML;
- router no cargado;
- default certificate;
- backend inaccesible;
- login roto;
- CORS roto;
- WebSocket roto;
- streaming roto;
- redirect loop;
- cookies inválidas;
- errores nuevos de Traefik;
- dominio antiguo dejó de funcionar.

### 11.2 Procedimiento

1. Eliminar o desactivar el registro nuevo en Pi-hole.
2. Restaurar el backup del archivo.
3. Esperar recarga del file provider.
4. Revisar solo logs nuevos.
5. Probar dominio antiguo.
6. No tocar `acme.json`.

```bash
FILE=/etc/traefik/dynamic/ARCHIVO.yaml
BACKUP=/etc/traefik/dynamic/ARCHIVO.yaml.bak-FECHA

cp -a "$BACKUP" "$FILE"
sleep 3

systemctl is-active traefik
```

### 11.3 Reinicio

Traefik normalmente recarga archivos dinámicos sin reinicio.

Reiniciar solo si:

- el file provider no recarga;
- el proceso está sano pero mantiene estado incoherente;
- la configuración estática cambió;
- existe evidencia y rollback.

```bash
systemctl restart traefik
sleep 3
systemctl is-active traefik
```

---

## 12. Criterios de aceptación

Un servicio queda `MIGRATED_DUAL_STACK` cuando cumple:

```text
[ ] Backend directo responde
[ ] Backup versionado existe
[ ] YAML nuevo cargó sin errores
[ ] Router HTTPS responde localmente
[ ] Wildcard Let's Encrypt coincide
[ ] Pi-hole devuelve 192.168.31.11
[ ] Tailscale DNS query responde
[ ] macOS dscacheutil responde
[ ] curl sin -k valida TLS
[ ] Chrome abre sin advertencia
[ ] Login funciona
[ ] Función principal funciona
[ ] Middlewares especiales funcionan
[ ] Dominio antiguo sigue funcionando
[ ] No hay errores nuevos
[ ] Evidencia registrada
```

No marcar como finalizado solo porque `curl` devuelve `200`.

---

## 13. Registro en Second Brain

Hermes/Ariadna debe conservar este runbook como fuente operativa única y registrar cada migración dentro del proyecto Aranea, no en Resources.

Ubicación sugerida para este único documento:

```text
10-projects/aranea/networking/traefik-https-migration/
```

Por servicio registrar en la misma operación:

```markdown
## Migración: <servicio>

- Fecha:
- Ejecutor:
- Estado: planned | in-progress | migrated-dual-stack | rolled-back
- Dominio antiguo:
- Dominio nuevo:
- Backend:
- Archivo Traefik:
- Backup:
- Middlewares preservados:
- DNS Pi-hole:
- Evidencia TLS:
- Smoke test:
- Incidentes:
- Rollback:
- Pendientes:
```

No crear una doc distinta por cada comando ni tareas de una sola línea. Mantener evidencia compacta, precisa y enlazada al proyecto.

---

## 14. Prompt operativo para Hermes/Ariadna

Usar este prompt para cada servicio:

```text
Ejecuta el RUNBOOK de migración HTTPS interna de Aranea para el servicio <SERVICIO>.

Reglas:
1. Trabaja solo con un servicio.
2. Lee primero su configuración Traefik completa.
3. Identifica backend, router, middlewares, auth, CORS, WebSocket, redirects y riesgos.
4. Prueba el backend directamente.
5. Presenta el Gate de descubrimiento antes de mutar.
6. Crea un backup versionado.
7. Mantén el dominio antiguo operativo.
8. Agrega únicamente el router HTTPS para <SERVICIO>.lab.aranea.cl.
9. Reutiliza el wildcard existente y el resolver letsencrypt.
10. No repitas tls.domains salvo instrucción explícita.
11. No modifiques acme.json, secretos, Step CA, OPNsense ni puertos públicos.
12. Captura solo logs generados después del cambio.
13. Valida localmente con curl --resolve antes de tocar Pi-hole.
14. Agrega el DNS interno solo después de aprobar router, TLS y backend.
15. Valida Pi-hole, Tailscale, resolver nativo, curl y navegador.
16. Ejecuta un smoke test funcional específico de la aplicación.
17. Si hay error, detente y aplica rollback; no improvises cambios secundarios.
18. Registra evidencia en el proyecto 10-projects/aranea.
19. No retires el dominio antiguo sin aprobación explícita.
20. Al finalizar, entrega estado, evidencia, riesgos pendientes y siguiente candidato recomendado.
```

---

## 15. Modo semiautónomo permitido

Hermes puede migrar servicios consecutivamente solo bajo esta política:

### Puede avanzar sin gate adicional entre servicios si:

- el servicio es `SIMPLE_HTTP`;
- backend conocido;
- router antiguo simple;
- usa solo `lan-only`;
- no requiere auth nueva;
- no requiere modificar backend;
- smoke test es no destructivo;
- rollback es directo.

### Debe detenerse antes de mutar si:

- CORS;
- WebSocket crítico;
- API con clientes;
- OAuth;
- cookies;
- large uploads;
- management plane;
- backend HTTPS;
- puerto desconocido;
- middleware faltante;
- redirect extraño;
- aplicación sin auth;
- servicio no HTTP;
- se requiere reiniciar una aplicación;
- se requiere modificar configuración fuera de Traefik/Pi-hole.

### Servicios simples iniciales

```text
Temporal UI
Prometheus
Jaeger UI
```

Grafana requiere una revisión extra de redirects/cookies, aunque normalmente será simple.

---

## 16. Cierre de la migración completa

No cerrar el proyecto hasta completar:

1. catálogo final de hostnames;
2. servicios migrados;
3. servicios explícitamente excluidos;
4. DNS interno documentado;
5. Split DNS validado;
6. renovación ACME monitorizada;
7. backups de Traefik;
8. rollback probado;
9. eliminación planificada de dominios antiguos;
10. decisión sobre Step CA;
11. decisión sobre redirect global;
12. autenticación de dashboards;
13. observabilidad de Traefik;
14. runbook de recuperación.

### Retiro del dominio antiguo

Debe ser un proyecto posterior:

- buscar clientes y bookmarks;
- actualizar integraciones;
- revisar logs de acceso;
- confirmar cero dependencias;
- retirar router antiguo;
- retirar DNS antiguo;
- evaluar Step CA;
- activar redirect HTTP→HTTPS cuando corresponda.

---

## 17. Comandos rápidos de diagnóstico

### Traefik

```bash
systemctl is-active traefik
systemctl status traefik --no-pager -l
tail -n 100 /var/log/traefik/traefik.log
```

### Router local

```bash
curl -Iv \
  --resolve HOST:443:127.0.0.1 \
  https://HOST/
```

### Certificado

```bash
openssl s_client \
  -connect 127.0.0.1:443 \
  -servername HOST \
  </dev/null 2>/dev/null |
openssl x509 -noout \
  -subject \
  -issuer \
  -dates \
  -ext subjectAltName
```

### Pi-hole

```bash
dig @192.168.31.31 HOST +short
```

### Tailscale

```bash
tailscale dns query HOST
tailscale dns status
```

### macOS

```bash
dscacheutil -q host -a name HOST
curl -Iv https://HOST/
```

### Reset DNS local Tailscale

```bash
tailscale set --accept-dns=false
sleep 2
tailscale set --accept-dns=true
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

---

## 18. Resultado esperado

Al completar este runbook, Aranea tendrá:

- nombres internos consistentes;
- TLS válido sin instalar una CA en cada dispositivo;
- acceso LAN y Tailscale;
- servicios no publicados en Internet;
- rutas auditables;
- migración reversible;
- separación entre aplicaciones web y protocolos de infraestructura;
- documentación útil para Hermes y para recuperación manual.


## Validación

- Verificar precondiciones y resultados del procedimiento antes de declarar éxito.
