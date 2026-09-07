# agents-os

Segundo cerebro (vault de Obsidian + AGENTS OS) de Rodrigo, sincronizado
automáticamente con GitHub: [`xKoRx/agents-os`](https://github.com/xKoRx/agents-os).

## Estructura

```
.
├── main/          ← el vault completo (fuente de verdad, vive como carpeta dentro del repo)
├── AGENTS.md      ← instrucciones de entrada para agentes (leer primero)
├── README.md      ← este archivo
├── sync.sh        ← sistema de sincronización automática
└── .sync/         ← lock y log del sync (estado local, ignorado por git)
```

El contenido real vive en `main/`. La carpeta `main/` es el vault completo y
debe seguir siendo una carpeta dentro de este repo. Este README y `AGENTS.md`
viven al lado del vault, no dentro.

## Sincronización automática

`sync.sh` corre cada 1 minuto vía cron sobre esta carpeta y hace, en orden:

1. `fetch` de `origin/master`. Si no hay red, corta en silencio y reintenta el
   próximo ciclo.
2. Si hay cambios locales (incluidos archivos nuevos), los commitea con
   mensaje `sync HH:MM`.
3. Si el remoto también avanzó, integra con `git rebase`. Si hay conflicto de
   contenido, reintegra con `git merge -X ours`: ganan los cambios locales y
   los archivos nuevos del remoto entran igual. Como último recurso respalda
   el estado remoto en un branch `conflict-<fecha>` y avanza con lo local,
   así nunca se pierde nada de ningún lado.
4. `push` con reintentos. **Nunca hace force-push.**

Un lock (`flock`) evita que dos corridas se pisen. El log queda en
`.sync/sync.log`.

## Para agentes externos (ChatGPT, Codex, etc.)

- Empuja directo a `master`. Nunca hagas force-push.
- Archivos nuevos: créalos y commitealos normalmente; el sync local los
  integra solo en el siguiente ciclo.
- Escribe los archivos de forma atómica cuando sea posible (escribir a un
  temporal y renombrar) para que el cron no capture un archivo a medio escribir.
- Antes de trabajar, lee [`AGENTS.md`](AGENTS.md) y sigue sus instrucciones.
