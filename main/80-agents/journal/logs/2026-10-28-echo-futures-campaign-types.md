---
type: change_log
schema_version: 1
scope: session
created: "2026-10-28"
updated: "2026-10-28"
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
application:
entities:
  - "[[Echo I+D — Futures]]"
related:
  - "[[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]"
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
  - area/trading
  - project/echo-rnd
---

# Echo Futures — tipos de campaña y mandato económico

## Cambio

- Fuente: último mandato Owner del 28-10-2026, America/Santiago. Integra CHALLENGE/FUNDED/SIMULATION como capacidad funcional de I+D, con entrega en planner técnico existente.
- Sustituye retiro fijo USD 3.000 por política evaluable, confirma USD 4.000 para compras y 100% reinversión de cash recibido. Challenge persigue pase/pérdida rápidos permitidos por reglas, sin caps prudenciales añadidos; 1/3 umbral Owner para futuras campañas, sin promedio empírico inventado.
- Actualiza PAUSED_OWNER a integración S04/variantes IN_PROGRESS_OWNER_REPORTED. No se certifica merge, build, tests, aceptación ni deploy.
- Nuevo [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]: requisitos aceptados, KPI/casos propuestos, reutilización, secuencia incremental y prompts C01/manager/C02/delta B. Frente C separado del antiguo I01-C read-only.
- Reconcilia planner Futures, parent, mapa de capacidades, planner lab, plan de integración, puente producto, índice y continuidad I01. A/B permanecen pendientes de retorno.
- No modifica fuentes/retornos DR/RV, skills, runbooks, G0–G5 ni evidencia histórica. Señala expresamente decisión pendiente FUNDED_ONLY frente a gate G4 challenge por identidad.

## Validación

- Lectura inicial Agents-OS master 837db281b78bc3d5f28834cf5e6ad539217696d5; reconciliar HEAD antes de publicación.
- Snapshot Echo master 347eee8bdab7f7628629af6383d1e45520815abd: revisión read-only de reutilización, no baseline certificado.
- Dos apoyos acotados revisaron KPI y baseline técnico; un tercer TOP revisó el mandato. Se repararon dos hallazgos materiales: activación contabilizada una sola vez y unidad compra/intento/reset explícita antes de aplicar 1/3. Sin escritura, código, tests, motores ni certificación propios; root integró y verificó el delta.
- Fuentes oficiales focales de payout/programa contrastadas; sin selección de prop ni perfil comercial completo.
- Artefactos nuevos materializados desde plantilla canónica; lint estricto de las 10 notas: ERROR=0, WARN=0. Reconciliación de HEAD y lectura remota requeridas antes de declarar publicación verificada.
- Agent-run omitido por alcance documental/lookup conforme a su skill. Consumo Pro no verificable: UNKNOWN, sin delta inventado. Graphify/replica física no ejecutados.

## Impacto y continuidad

- Autoridad funcional: [[Echo I+D — Futures]]; entrega técnica: [[Echo Futures — Optimización de Campañas]]; arquitectura/gates producto existentes preservados.
- Siguiente: Owner retorna A/B y coordina C01 con manager S04 existente; diseño puede avanzar mientras se integra. Nueva implementación requiere paquete aceptado y autorización pertinente.
- Sin código de producto, campañas, compras, operaciones, hosts, contactos a terceros ni cierre formal del manager por esta entrega.


## Motivo

El Owner modificó las decisiones económicas y el alcance de capacidades: la continuidad anterior mantenía una pausa y preguntas ya resueltas. El delta evita que futuros agentes implementen otro objetivo o reconstruyan el laboratorio.

## Fuentes usadas

Último mensaje Owner; planners/skills vigentes en Agents-OS; snapshot remoto Echo y dos páginas oficiales. Referencias exactas en el nuevo mandato.

## Resolución aplicada

Decisiones de negocio en el planner Futures; detalle técnico futuro en el planner del laboratorio. Los requisitos/ONE-SHOT quedan en un artefacto, con enlaces de entrada para agentes de I+D y producto. No se crean nuevas entidades de manager.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin credenciales, secretos, logs de cuentas ni datos financieros ajenos al mandato Owner.

## Rollback

Revertir únicamente este delta documental mediante un commit nuevo reconciliado sobre master. Conservar evidencia/decisiones posteriores y archivos originales DR/RV; no resetear el repositorio ni tocar código Echo.
