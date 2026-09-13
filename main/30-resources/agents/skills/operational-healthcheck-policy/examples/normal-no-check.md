# Example: Trigger Normal (Sin Check)

## Contexto

Ariadna va a registrar el cierre de una sesión en el vault, crear
un learning, o escribir una decisión. No hay señal de problema.

## Procedimiento

Proceder sin check de LiveSync, sin healthcheck, sin pedir OK al
owner. Escribir la nota directamente.

## Anti-Pattern

- Hacer `curl localhost:5984/_up` antes de escribir
- Verificar `.obsidian/plugins/obsidian-livesync/data.json` antes
  de registrar
- Pedir OK al owner para registrar un cierre de sesión

## Por Que Es OK

- Obsidian/LiveSync maneja el sync automaticamente
- El registro de notas operativas es parte del trabajo de Ariadna
- El owner corrigió explicitamente: "Ariadna no debe validar
  LiveSync o el estado del vault en cada escritura normal del
  vault"
