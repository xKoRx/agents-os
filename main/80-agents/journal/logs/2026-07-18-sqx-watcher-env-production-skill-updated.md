---
type: change_log
scope: global
created: 2026-07-18
tags:
  - kind/change_log
  - project/symphony
  - area/sqx
  - topic/skills
---

# Change Log: Actualización de la Skill sqx-watcher con variables de entorno de producción

## Motivo
El SQX Watcher local, al ser levantado de manera predeterminada a través de la terminal, hereda el entorno del shell del host que comúnmente está configurado como `development` o queda sin definir. Al no forzar `ENV=production`, el watcher local no interactúa con la infraestructura de producción correcta (Temporal, MinIO, bases de datos), causando que los flujos de trabajo se inicien en colas sin workers activos.

## Qué Cambió
- Modificamos [sqx-watcher/SKILL.md](file:///Users/rjara/go/src/github.com/xKoRx/symphony/.agents/skills/sqx-watcher/SKILL.md) para agregar de forma explícita el prefijo `ENV=production` en los comandos canónicos de activación y ejecución en primer plano del watcher.
- Se detuvo la sesión de screen vieja (`watcher`) en local.
- Se reinició el watcher local con: `ENV=production screen -dmS watcher ./run_watcher.sh ./input`.

## Validación
- Verificación de sesiones de screen locales con `screen -list`, mostrando `watcher` en estado detached.
- Captura del output del screen de `watcher` (`screen -S watcher -p 0 -X hardcopy`), validando que inició correctamente conectándose con `"env":"production"` e inicializando la vigilancia en `./input`.
