---
type: evidence_doc
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence
  - area/echo
  - tech/deployment
---

# DEPLOYMENT-MECHANISM — cómo ejecuta SQX 144 el plugin Forge (hallazgo operativo)

Refina el hallazgo de precedencia de la 21.ª sesión ("snippet > jar en Build 144") con el mecanismo exacto, demostrado físicamente en esta sesión con 5 runs trampa.

## Mecanismo demostrado

1. **La autoridad de ejecución es `internal/libs/Snippets.jar`**, no `user/libs/EchoForgeAutomator.jar`. Evidencia: reemplazar el jar de `user/libs` por el candidato produjo 5 runs con timing y firma JFR de baseline (5/5 runs con `norm WITH-compile=237–262`, idéntico a baseline); actualizar las clases DENTRO de Snippets.jar produjo el run del candidato (`norm WITH-compile=0`, timing 7–9 s).
2. **`user/settings/snippets.txt` es el manifiesto cache-keyed**: línea por fuente `<ruta>|<md5>`. En boot, SQX recompila un snippet SOLO si el md5 listado difiere del md5 de la fuente en disco; si coincide, confía en la clase ya compilada del Snippets.jar.
3. **Consecuencia práctica (trampa demostrada): actualizar fuente + hash a la vez NO recompila** — el manifiesto queda "fresco" y el jar stale sigue ejecutándose silenciosamente (fue exactamente lo que pasó en los primeros 5 "candidate runs" de esta sesión; la paridad pasaba porque el código ejecutado era el mismo baseline). Vía de deploy manual correcta: (a) reemplazar SOLO la fuente (dejar el hash viejo) y dejar que el boot recompile, o (b) actualizar fuente+hash+jar en el mismo cambio (lo que hace el pipeline deployer en cada release — Snippets.jar con mtime de release).
4. **Un CustomAnalysisMethod nuevo NO se descubre por el jar de user/libs**: una sonda no-op empaquetada solo allí falló con "Class with name 'EchoForgeNoopProbe' doesn't exist!" en la carga de settings de la tarea; la clase debe existir en el sistema de snippets.

## Implicancia de integración para el candidato

Ninguna acción manual de flota: el pipeline release estándar de Forge ya reconstruye snippet+JAR+Snippets.jar (así se desplegó 0.3.1). La revisión de integración del candidato puede apoyarse además en el canario de firma JFR usado aquí (`0 Pattern.compile` bajo métodos del exporter en el primer run post-deploy) como verificación de que el código nuevo está realmente en ejecución.

## Estado final de la copia candidate-local (Kronos)

`Snippets.jar` y `user/libs/EchoForgeAutomator.jar` restaurados a los SHA de 0.3.1 (`aac0e8f2…` / `3b0063e4…`); backups del jar con el candidato en `bench/Snippets.jar.candidate-perf-s01`. La instalación de flota `/home/kor/sqx/144` permaneció read-only toda la sesión. Sin workers reiniciados, sin colas ni ETCD tocados, sin campañas afectadas (los 25+ runs corrieron como proceso sqcli independiente de la copia, flota ociosa).
