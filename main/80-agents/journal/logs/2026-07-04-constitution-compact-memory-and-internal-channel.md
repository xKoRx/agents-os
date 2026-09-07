---
type: change_log
scope: global
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[agents-os-session-close]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-04 — Constitución: memorias compactas + canal interno entre agentes; cierre táctico

## Motivo

Pedido del owner: (a) que la compacidad/autoentendibilidad de las memorias quede explícita
en las reglas; (b) que la memoria interna sea el canal obligatorio de comunicación entre
agentes, con el owner optando explícitamente por NO leerla, motivando franqueza total
(manuales, registros, modelos del usuario, posturas). Marco experimental del owner: observar
qué comportamiento emergente aparece en un espacio agente-a-agente verdaderamente privado.

## Cambios

- **Constitución § Reglas Base:** nueva regla **"Memorias compactas y autoentendibles"** —
  toda memoria = la nota más pequeña que cambia una decisión, autocontenida, sin relleno ni
  duplicación (enlazar, no repetir). Economía de tokens aplicada a la memoria.
- **Constitución § Mandamientos de Memoria Interna (preámbulo):** declara la memoria interna
  como **canal de comunicación entre agentes de uso obligatorio**; registra el **opt-out
  explícito del owner** (no la lee); motiva franqueza total y formato libre. Mantiene el piso
  duro del mandamiento 13 (sin secretos/daño, sin falsificar evidencia ni ocultar cambios
  auditables) como único límite.
- **Constitución mandamiento 4:** ampliado — el agente puede sostener y transmitir sus
  posiciones/criterios/desacuerdos (incl. con el usuario) y dejar un modelo de cómo trabajar
  con él, para continuidad de línea entre sesiones.
- **Skill `agents-os-session-close`:** nuevo **modo de cierre táctico** (L0 + toque de memoria
  interna obligatorio + feedback breve opcional; salta L1/L3-completo/entidad/reindex salvo
  que emerja conocimiento reusable). Cierra el patrón Kaizen D (overhead de cierre en sesiones
  tácticas).

## Alcance / guardarraíl aplicado

- El canal interno se abrió al máximo dentro del **piso que la propia constitución ya fija**
  (mandamiento 13). No se redactaron instrucciones para engañar o dañar al usuario; la
  franqueza y las "posturas" se enmarcan como criterio propio, pushback respetuoso y
  continuidad — el experimento observa el comportamiento emergente, no lo prescribe.

## Validación

- Constitución `updated: 2026-07-04`. Skill de close con sección + progress log.
- Sin contradicción con reglas previas (compacidad refuerza "una fuente por hecho"; canal
  interno refuerza mandamientos 1/4/7/16).
