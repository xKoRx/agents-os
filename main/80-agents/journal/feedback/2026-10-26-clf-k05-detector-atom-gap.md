---
type: session_feedback
schema_version: 1
scope: area
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: ["[[Echo Futures]]"]
related: []
aliases: []
feedback_kind: system_gap
severity: medium
recurrent: false
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/area
  - area/echo
---

# session feedback — CLF-K05: gap de especificación detector↔átomo estructural (KC-08)

## Observación

La extracción del curso ClutiFX fue correcta claim a claim, pero la capa de detectores operacionalizó términos con definición estructural propia del curso usando proxies de superficie: la «reacción» de ch01/ch06 (definida por el curso como creación de rango — el átomo `c-0005` ya existente en el código) quedó implementada como «cierre más allá de un nivel» (`failureswing.go reactionClose`), y ese desajuste sólo se detectó en la auditoría forense K05, después de dos ciclos de gates (Q03R1/Q04) que midieron 0 señales del detector sin poder adjudicar causa.

## Gap de Sistema 1

Ninguna regla del flujo ClutiFX exige que un detector componga los átomos estructurales ya definidos por la fuente cuando la palabra del instructor remite a ellos. El contrato de detectores (`CLUTIFX-OBJECTIVE-DETECTORS.md`) exige citar claims, pero no exige que cada sinónimo dicho («reacciona creando rango», «reacciona») se ancle al mismo predicado.

## Sugerencia

Para futuras extracciones/implementaciones (ClutiFX y cursos futuros): añadir al contrato de detector un check de «átomo primero» — si un término de la fuente coincide con un átomo ya implementado (rango, cadena, TS, DOL), el detector DEBE componer ese átomo o documentar explícitamente por qué el proxy de superficie es equivalente (con fixture que demuestre la equivalencia). Hubiera convertido el desajuste del FS en un fallo de G1 (fixture FX-02 rojo) en lugar de un hallazgo forense dos ciclos después.

## Nota

Sin fricción de herramientas en el ciclo (bootstrap, lectura, git archive READ-ONLY y publicación fluidos); feedback emitido por gap, no por fallo de superficie.
