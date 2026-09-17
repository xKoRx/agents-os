---
type: project-note
schema_version: 1
status: active
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-17
updated: 2026-09-17
tags:
  - tech/polymarket
  - status/m0
---

# Research — Technical Platform Map M0

**Proyecto canónico:** [[Polymarket Engine — MVP]]. Esta nota es sólo un enlace/handoff para M0; las decisiones de arquitectura, diseño y plan TOP/NORMAL permanecen en el archivo raíz del proyecto. No crear aquí un diseño paralelo.

**Recurso técnico canónico de M0:** [[Polymarket — Technical Platform Map — synced 2026-09-17]] en `main/30-resources/polymarket/Polymarket — Technical Platform Map — synced 2026-09-17.md`.

**Original completo preservado:** Biblioteca de ChatGPT `/Polymarket Engine/Resources/Polymarket — Technical Platform Map — synced 2026-09-17.md` (160165 bytes, 1177 líneas, SHA-256 `78e6506fa67aa12843ba4acb0e4c8271a83c1841432a4a53777c73c4c723c11f`). Si el recurso canónico todavía no está materializado en GitHub al iniciar una sesión, el primer paso es importar **ese archivo exacto**, validar SHA-256 y commit antes de cualquier edición. No reconstruirlo desde memoria, chat ni notas de ingesta.

**Estado M0:** documento técnico amplio y útil, pero `M0 DESIGN READY` todavía debe ser certificado por un agente nuevo trabajando directamente sobre el archivo. El documento declara RG-01–RG-07 en §24 y mantiene `NO LIVE CONVERSION UNTIL ROUTE VERIFIED` para NegRisk Protocol-v2. El objetivo inmediato NO es obtener perfección enciclopédica: es cerrar los contratos y gaps necesarios para que Astra y Fable puedan diseñar el Engine MVP sin navegar documentación oficial para descubrir facts básicos o contratos críticos.

**Necesidades del Engine MVP que deben quedar cubiertas en el recurso:** modelo de dominio/IDs; market discovery; CLOB REST y WS; books/reconnect/recovery; recorder/replay y límites históricos; auth/wallets/session/signing; órdenes/estados/fills/reconciliation; positions/split/merge/redeem; resolution; fees/rebates/rewards; rate limits; contratos/addresses/version boundaries; observabilidad y datos necesarios para strategy POCs; NegRisk con cualquier capability no verificada explícitamente bloqueada.

**Flujo autorizado:** importar/abrir recurso canónico → verificar repo y fuentes → trabajar in-place → ejecutar scripts/descargas/parsers/read-only probes necesarios → patch por secciones → commit frecuente → actualizar §24/gates → cerrar cuando `M0 DESIGN READY` sea demostrable. No generar otro Technical Platform Map paralelo ni devolver el documento completo por chat.

**Después de M0:** Astra diseña el Engine sobre `Polymarket Engine — MVP.md` usando este recurso + Edge Research; Fable challengea; Astra reconcilia; owner revisa; TOP produce plan de implementación; NORMAL implementa. Astra/Fable no deben gastar ventanas descubriendo endpoints o contratos que M0 debía dejar resueltos.
