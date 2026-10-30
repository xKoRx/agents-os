---
type: change_log
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities: []
related: []
aliases: []
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
---

# 2026-10-30-echo-feed-p0-recovery

## Cambio

Actualización de [[Echo Futures — Runtime Pools]] con mandato P0, baseline preservado, ownership Sol/Luna, gates pendientes y cuota confirmada. El proyecto sigue como único planificador.

## Evidencia y motivo

Mandato Owner 2026-10-30; lectura source de workers y estado local systemd/journal. Feed reconectado tras acción física Owner a las 13:58:42 Chile, sin certificación inferida. Se corrige la inferencia histórica que comparaba items del relay con records Kafka: no demuestra estancamiento por sí sola.

## Validación y límites

Rama fuente inicial limpia en 3eaed4d2; nueva rama de misión conserva baseline. Go freeze3 y S2 pasan suites focales/race/vet y revisión independiente. C#165+4asserts/0fallos tras cap pending; revisión independiente cap/drain/resume y crash→SOURCE_GAP PASS. Integrado87c85a5e en codex/echo-feed-p0; paquete Windows validado y staged C:\Temp\EchoFeedP0. Relay87c85a5e desplegado17:38:40Z PID149253 porhash23960992…b78c9, core/gateway yFlink intactos; S2guard solo staged. Instalación/compilaciónNT Owner pendiente. Baseline físico reproduce NACKED tras drain desde14:09:39 Chile; causa inicial de presión no demostrada. Solo relay DEV actualizado; certificaciones pendientes. Cuenta de cuota: 64% inicial y59% restante último corte; reserva5%. Sin secretos ni dumps persistidos.

## Rollback

Revertir únicamente el delta documental de este hito; conservar historia y cambios concurrentes.

## Corrección del instalador tras intento Owner

El paquete original confundió símbolo configurado con Instrument.FullName y falló antes de mutar addon/identity. El fixture inicial reflejaba esa misma suposición y no cubría el límite real. Reparación: preservar única clave durable existente y mantener validación de fingerprint productiva. Windows confirmó nombres distintos, helper positivo sobre copia temporal, fingerprint incompatible sin mutación, multistream/missing identity rechazados; paquete reemplazado (Install SHA791fc1b5…caf40f). Instalación física sigue pendiente del reintento Owner.
