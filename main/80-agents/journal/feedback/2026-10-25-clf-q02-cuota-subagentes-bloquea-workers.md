---
type: feedback
schema_version: 1
scope: session
created: "2026-10-25"
updated: "2026-10-25"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: []
related: []
aliases: []
severity: medium
category: capability-gap
status: open
source_run: "[[2026-10-25-zcode-glm53-flash-clf-q02-catalog-completion]]"
load_policy: manual
indexable: false
index_priority: never
tags: [kind/feedback, scope/session]
---

# Cuota de subagentes agotada deja sin ejecutar el frente de estrategias de sesión (STR-001/003/004)

Durante CLF-Q02 el despacho del worker `clf-flash` para implementar STR-001/003/004 falló con `exceed quota limit`. El frente quedó declarado NOT_IMPLEMENTED con detectores listos en vez de entregado. Fricción operativa real: los mandatos ONE-SHOT de varias horas que combinan implementación Go + campañas largas se benefician de delegar el segundo frente paralelo; sin cuota disponible, el camino alternativo (implementar en serie en el mismo checkout) habría retrasado las olas de motores ya en curso. Sugerencia: presupuestar cuota de subagentes para misiones ONE-SHOT largas o documentar de antemano el frente que se sacrifica.
