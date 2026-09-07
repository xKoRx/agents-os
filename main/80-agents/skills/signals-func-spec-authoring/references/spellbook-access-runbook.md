# Runbook — acceder y publicar specs en Spellbook (SIG) por CLI

Operación mecánica y validada. Este archivo es un **runbook** (secuencia de comandos para una operación puntual), no la skill: la skill decide *qué escribir*; esto es *cómo llegar y publicar*. Cargarlo cuando vayas a tocar Spellbook.

## Regla 0 — nada de browser

No intentes navegar `spellbook.adminml.com` con herramientas de browser: el in-app browser y la extensión de Chrome chocan con el SSO de MercadoLibre (`auth-meli.adminml.com`) y no logean. La web UI es para humanos. El agente entra **solo por CLI**.

## Auth

La CLI `@spellbook/cli` (alias `spellbook`) ya suele estar autenticada por token. Si da "Session expired" o "Authentication failed", el usuario debe correr `spellbook login <token>` (token desde la web: menú lateral → CLI Token → Generate). No puedes generar el token tú. Ver `/spellbook.auth`.

Config del CLI (baseUrl + token) en macOS: `~/Library/Preferences/spellbook-nodejs/config.json`.

Usa siempre la CLI autenticada para crear, editar y verificar. No reconstruyas manualmente el header de autenticación con `curl`: el formato es responsabilidad de la CLI y un token válido para ésta puede devolver `401` si se envía con un esquema manual incorrecto.

## Comandos que de verdad usas

El output es JSON por default (pensado para agentes); parséalo con `python3`. El cuerpo Markdown de un spec está en el campo `.content`, posiblemente dentro de una envoltura `.data`.

```bash
spellbook specs list SIG --page 1 --limit 50
spellbook specs view <specId>
spellbook specs create SIG --title "…" --type functional
content="$(<ruta-al-markdown.md)"; spellbook specs edit <specId> --content "$content"
spellbook specs children add <parentId> --title "…"
spellbook specs children add <parentId> <childId>
spellbook specs summary SIG
spellbook search "SIG-573"
```

`list` es paginado; el default histórico es 20 y el proyecto tiene más de 100 specs. Recorre páginas hasta recibir menos elementos que el límite.

```bash
python3 - <<'PY'
import subprocess, json

all_specs = []
page = 1
while True:
    output = subprocess.run(
        ["spellbook", "specs", "list", "SIG", "--page", str(page), "--limit", "50"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    payload = json.loads(output)
    data = payload.get("data", payload)
    while isinstance(data, dict):
        next_data = next((data[key] for key in ("data", "items", "specs") if key in data), None)
        if next_data is None:
            break
        data = next_data
    if not isinstance(data, list):
        raise RuntimeError("Formato inesperado en specs list")
    all_specs.extend(data)
    if len(data) < 50:
        break
    page += 1
print("total:", len(all_specs))
PY
```

## Publicar contenido Markdown

La CLI vigente acepta Markdown completo, incluidos code spans y fences con backticks, mediante `specs edit --content`. Validado el 2026-08-31 con `@spellbook/cli 1.3.0` publicando y releyendo un documento de 14 kB.

```bash
SPEC_ID=<uuid>
FILE=<ruta-al-markdown.md>
content="$(<"$FILE")"
spellbook specs edit "$SPEC_ID" --content "$content"
spellbook specs view "$SPEC_ID"
```

Después de crear, verifica por UUID. Si la salida JSON de `create` no expone el UUID donde tu parser espera, **no repitas el create**: crear specs no es idempotente. Recorre `specs list SIG` y resuelve por título exacto; exige un único match antes de editar.

Al terminar, relee el spec y confirma título, estado y contenido exacto. Crear deja el spec en `draft`; sólo cambia el status si el usuario lo pidió explícitamente.

## Ownership / review

`spellbook specs take <id>` **solo funciona en specs `ready_to_code`/`approved`**; en `draft` da "Only ready_to_code/approved specs can be taken". Para editar un draft **no** hace falta `take`. El flujo del equipo es dejar el spec cerrado y moverlo a `review` para que el equipo apruebe. `spellbook specs approve <id>` / `approvals <id>` cubren el lado reviewer.

## NO crear proyectos por CLI

`spellbook projects create` crea el proyecto **sin team**; queda huérfano e inaccesible ("Project not found") y no se puede adjuntar team después. Los proyectos se crean en la **web UI**. Specs sí se crean por CLI dentro de un proyecto existente; SIG usa `bb929ff8-31cc-4c92-a117-e93ad29327e3`.
