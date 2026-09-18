---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project:
application:
entities:
  - "[[nodo-truenas]]"
related:
  - "[[30-resources/aranea/05-tickets/2026-06-30-012-unlock-agent-ro-nopasswd]]"
aliases:
  - "TrueNAS Ariadna admin enablement"
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

# 2026-09-18 — Habilitación administrativa de Ariadna en TrueNAS (privilegio Local Administrator + API key certificada)

## Cambio

- **Tipo:** config-change
- **Objetivo:** dar a Ariadna administración efectiva de TrueNAS vía API oficial, sin login por contraseña y sin tocar otros grupos ni privilegios predefinidos.
- **Archivo(s) / artefactos:**
  - `30-resources/aranea/01-topologia/nodo-truenas.md` (sección nueva «Acceso administrativo Ariadna»).
  - `80-agents/journal/logs/2026-09-18-truenas-ariadna-admin-enablement.md` (este log).
  - Evidencia local (fuera del vault): `~/aranea/work/truenas-ariadna-20260918/` (privilege-before.json, privilege-update.out, api-key-metadata.json, cert_api.py, cert-api.json). Secreto: `~/aranea/secrets/truenas/` (dir 0700, ficheros 0600).
- **Mutación en TrueNAS (192.168.31.91, TrueNAS Scale 25.04.1):**
  1. `privilege.update` id=1 «Local Administrator» (builtin): `local_groups` de `[544, 3002]` → `[544, 3002, 3008]` (GIDs; 3008 = grupo local `ariadna`). Roles (`FULL_ADMIN`), `web_shell=true` y `ds_groups=[]` sin cambios.
  2. `api_key.create` → id=1, nombre `ariadna-admin-20260918`, username `ariadna` (secreto de 66 chars, nunca impreso en conversación ni logs).

## Baseline (antes)

- Privilegio 1: local_groups `[544 builtin_administrators (miembros 1 root, 69 admin), 3002 apps_admin (miembro 70 kor)]`, roles `[FULL_ADMIN]`. Privilegios 2 (Read-Only, gid 951) y 3 (Sharing, gids 952/3002) presentes.
- Usuario `ariadna` uid 3005 (id 76): grupo primario `ariadna` gid 3008 único, `groups=[]`, `roles=[]`, sin API keys, `password_disabled=true`.
- SSH `ariadna@.91` por clave `~/.ssh/ariadna_truenas` + `sudo -n` completo por línea 6 de `/etc/sudoers` (preexistente, no modificada).
- Huella SSH ed25519 verificada contra `SHA256:u73kODBpK6M2XI/7JZM53veVaaeai8L7CLM/BbBLej8` antes de conectar; host key fijada en known_hosts.

## Ejecución y errores corregidos (sin estado parcial)

- Intento 1 `privilege.update {"local_groups":[40,110,3008]}`: EINVAL atómico (usé ids de tabla en vez de GIDs; el docstring pide GIDs). Estado verificado intacto tras el rechazo.
- Intento 2 con GIDs `[544,3002,3008]`: OK.
- `api_key.create` posicionales: EFAULT «Too many arguments» → formato correcto: un único objeto `{"name":..., "username":...}`.
- Fracasos de verificación redundante (quoting de filtros en midclt) no afectaron estado; el chequeo se repitió con forma anidada correcta.

## Causa raíz del desvío del canal WS (lección operativa)

- TrueNAS 25.04 sirve en `wss://host/websocket` (nginx :443; :80 redirige 307 a https) el protocolo **DDP del GUI**, no JSON-RPC crudo: handler `apps/websocket_app.py::WebSocketApplication.on_message` hace `message["msg"]` en el hot path → un frame `{"jsonrpc":"2.0",...}` sin `msg` muere con cierre 1011 razón `'msg'`; JSON inválido cierra 1007 con el error crudo de `json.loads` (discriminador empírico del handler legacy).
- Protocolo correcto: handshake `{"msg":"connect","version":"1"}` → `{"msg":"connected"}`; llamadas `{"msg":"method","id":N,"method":...,"params":[...]}`; respuestas `{"msg":"result"|"error","id":N}`. Mismos métodos del middleware (`auth.login_with_api_key`, `auth.me`, `user.query`, `api_key.my_keys`, `privilege.query`, `privilege.update`, `auth.logout`).
- Con websockets 15.x conectar con `proxy=None` (autodetección de proxy del sistema reescribe URIs ws/wss a la del redirect).

## Validación (certificación vía API oficial, 7/7 PASS)

- `auth.login_with_api_key` = true; `auth.me` → `ariadna`/uid 3005; `auth.logout` = true.
- `user.query`: roles derivados `[FULL_ADMIN]`, `password_disabled=true`, `api_keys=[1]`.
- `api_key.my_keys`: id 1 `ariadna-admin-20260918` para `ariadna`.
- `privilege.query`: priv1 local_groups `[544,3002,3008]` roles `[FULL_ADMIN]`; privs 2 y 3 intactos.
- `privilege.update` idempotente (re-aplicación del mismo payload por canal API): ok, `mismo_estado=true`, FULL_ADMIN y web_shell preservados — escritura efectiva demostrada.
- Superficie sin cambios: membresías de grupos 544/3002/3008 idénticas al baseline; privilegios 2/3 intactos; sudoers intacto; sin login por contraseña nuevo (password_disabled=true).
- Evidencia JSON sin secretos: `~/aranea/work/truenas-ariadna-20260918/cert-api.json`.

## Compartibilidad

- **Scope:** local. Sin secretos: solo nombre/id de key y referencias de ubicación de secretos.

## Rollback

1. Borrar la key: `midclt call api_key.delete 1` (o `api_key.delete` por WS con sesión admin).
2. Revertir privilegio: `sudo -n midclt call privilege.update 1 '{"local_groups":[544,3002]}'`.
3. Limpiar: borrar `~/aranea/secrets/truenas/` y known_hosts (opcional); revertir sección en `nodo-truenas.md` y borrar este log.

## Follow-ups

- datasets/snapshots/replicación: explícitamente NO configurados (fuera de alcance por orden del owner).
- Nota de diseño: `ariadna` sigue con `password_disabled=true`; el acceso admin es API-key + SSH/sudo existente.
