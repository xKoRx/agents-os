---
type: change_log
schema_version: 1
scope: global
created: 2026-08-25
entities:
  - "[[AGENTS OS]]"
related:
  - "[[rjara-agent-profile]]"
  - "[[Crear Context - Code Review Remediation]]"
tags:
  - kind/change-log
  - project/agentsos
  - scope/user
---

# 2026-08-25 — Regla de construcción de tests en el perfil global

## Qué cambió

`80-agents/memory/public/user-preference/rjara-agent-profile.md`: se agregó una preferencia `[DURA]` en "Preferencias de trabajo", inmediatamente después de la regla de `agents-os-agent-run-register`.

**Regla:** los tests aseguran primero las funcionalidades críticas de un desarrollo —lo que rompe producción, los bordes de seguridad y autorización, la degradación silenciosa— y recién después se complementa con casos hasta el piso de **90% de coverage**, obligatorio para todo desarrollo nuevo. Un 90% alcanzado sin cubrir lo crítico no cumple. Una rama inalcanzable por cualquier entrada real se borra en vez de testearse.

## Por qué

Pedido explícito del owner durante la remediación del code review de [[Crear Context - Code Review Remediation]]. El disparador fue concreto: en la implementación revisada convivían un 95% de branch coverage con una guarda de seguridad sin ningún test —la que impide leer outputs a través de una cadena de imports— y con dos tests que perseguían ramas inalcanzables de un presupuesto de bytes que terminó eliminado. El número no distinguía un caso de otro.

## Alcance

Aplica a todo repo y todo lenguaje. No reemplaza gates de cobertura propios de cada repo cuando son más exigentes.

## 2026-08-26 — Piso elevado a 95%

Por pedido explícito del owner, el piso global de coverage para desarrollo nuevo se elevó de 90% a 95%; se mantiene la prioridad de cubrir primero los caminos críticos y no crear tests para ramas inalcanzables.
