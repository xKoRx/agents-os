---
type: agent_memory
scope: internal
created: 2026-07-03
updated: 2026-09-09
index_priority: never
memory_state: archived
entities:
  - "[[Bajo y Muy Bajo Precio]]"
  - "[[RFC Destaques de Precio - Hito 2]]"
confidence: high
load_policy: manual
indexable: false
tags:
  - agent/internal
  - area/meli
---

# 2026-07-03 - RFC Destaques rollout order continuity

Si se retoma el RFC de Hito 2 de Destaques de Precio, no volver al orden antiguo "MLA primero, MLM después".

Orden vigente pedido por el usuario:

- MLA + MLM primero, juntos, porque la nueva versión del Sugeridor ya corre hace tiempo en ambos sites.
- Luego resto de sites no-MLB, en paralelo, cuando tengan Sugeridor disponible/validado.
- MLB se trabaja después de MLA+MLM como carril FIPE separado.
- La implementación base es común para todos los sites; la diferencia debe vivir en condiciones/configuración de tageo por site, no en una duplicación innecesaria del pipeline.

Iteración técnica posterior del mismo día:

- No asumir contrato de atributos `tier/origin`. El contrato está abierto.
- Atributos: mínimos, idealmente booleanos y filtrables en Search; pendiente definir/crear atributos, agregarlos a caché Search API Go y conversar filtrabilidad con Search.
- Hito 2 debe escalar Bajó de Precio: consumer/procesamiento común, no pipeline paralelo.
- Ya existe consumer de cambios de precio; falta consumer de cambios de atributos.
- Consumer común debe evaluar prioridad funcional: Bajo/Muy Bajo primero, Bajó de Precio segundo.
- Proceso masivo: orquestador paginado que encola items al consumer común. Trigger pendiente para no-MLB y MLB.
- Observabilidad, experimentos y rollout operativo quedaron `TBD`.

Corrección importante: el RFC principal de Hito 2 es
`/Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/RFC Destaque de precio — Hito 2.md`.
No seguir editando `rfc.md` como fuente principal de Hito 2 salvo que el usuario lo pida explícitamente.

Proyecto de implementación creado:

- Humano: `[[Implementación Hito 2 - Destaques de Precio]]`.
- Agentes por app: `[[Hito 2 - vis-items-loader-tagging]]`, `[[Hito 2 - Search API Go]]`, `[[Hito 2 - search-middleware]]`, `[[Hito 2 - java-polycard-sdk]]`, `[[Hito 2 - vis-octopus-lib]]`, `[[Hito 2 - vpp-backend]]`.
- Las reglas usadas son `90-system/convenciones.md` + `agents-os-agent-project-workflow`: agent projects en `agentes/`, `parent` obligatorio y tarea puente humana en el padre.
