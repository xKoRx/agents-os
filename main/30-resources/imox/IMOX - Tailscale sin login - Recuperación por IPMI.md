---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Tailscale sin login - Recuperación por IPMI]]"]
last_verified: "2026-10-30"
confidence: "high"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-30"
updated: "2026-10-30"
related: ["[[IMOX]]"]
---

# IMOX - Tailscale sin login - Recuperación por IPMI

## Síntesis vigente

Relata pérdida de acceso a Windows tras reinicio y diagnóstico por consola IPMI: sistema encendido en pantalla de login, pero Tailscale no disponible antes de iniciar sesión. El autor dice resolverlo con Run unattended y ajuste de expiración del nodo. La lección de continuidad es verificar acceso previo al login y contar con una vía de recuperación independiente. Tres comentarios accesibles son de experiencia/agradecimiento, sin nueva prueba técnica.

## Evidencia y provenance

[[IMOX - Fuente - Tailscale sin login - Recuperación por IPMI]] · [Publicación](https://comunidad.imoxtrading.com/c/seguridad-y-sevidores-vds/perdi-el-acceso-a-mi-servidor-por-tailscale-y-como-lo-recupere-por-ipmi) · revisión 2026-10-30, por Chrome autenticado del owner. Fuente atribuida al autor, no verificación independiente.

## Límites y contradicciones

Lectura cerrada del texto y tres comentarios accesibles; no se identificó material técnico adjunto pendiente en este alcance. Se registra el relato sin ejecutar ni aprobar sus pasos. Sus propuestas de HTTP, excepciones de Java/certificado y cambio de reloj no se convierten en runbook validado ni se realizaron. Tampoco se generaliza la desactivación de expiración a toda red.
