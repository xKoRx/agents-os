---
type: skill
schema_version: 1
name: human-first-technical-writing
description: Redacta o reestructura documentos técnicos para minimizar el esfuerzo cognitivo necesario para entender correctamente un problema, cambio o decisión. Prioriza la construcción progresiva del modelo mental del lector sobre el orden de investigación o implementación del agente. Usar especialmente en PRs, specs, propuestas, incidentes, reportes y guías destinadas a personas.
scope: global
created: "2026-08-26"
updated: "2026-08-26"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-skill-authoring]]"
aliases:
  - human-first-document-authoring
  - escritura para humanos
  - human-readable document authoring
  - cognitive technical writing
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/document-authoring
---

# Human-First Technical Writing

## Purpose

Hacer que el lector gaste su capacidad mental entendiendo el sistema, no descifrando el documento.

Preservar la complejidad técnica necesaria, pero eliminar carga cognitiva accidental causada por mal orden, contexto tardío, conceptos prematuros, ruido o falta de relaciones causales.

## Minimal Read

Leer sólo:

1. El contrato o template del artefacto destino.
2. Las fuentes autoritativas necesarias para sostener sus afirmaciones.
3. El documento existente, sólo si debe reestructurarse.

No consumir historial de investigación innecesario cuando los hechos autoritativos ya están disponibles.

## Procedure

1. **Definir al lector.** Determinar qué sabe probablemente, qué necesita entender o decidir y qué artefacto está leyendo. Si no existe información suficiente, asumir un lector técnico competente pero sin el contexto inmediato del autor.

2. **Extraer el modelo esencial.** Identificar problema o propósito, causa relevante, cambio o decisión, efecto observable, límites, riesgos, evidencia y —cuando corresponda— feedback esperado. Separar hechos confirmados, inferencias y pendientes.

3. **Ordenar por preguntas del lector, no por historia del agente.** Presentar cada pieza cuando responde una pregunta que surge naturalmente de la anterior. Como heurística para PRs:
   `qué ocurre → por qué ocurre → qué cambia → cómo cambia el comportamiento → límites/riesgos → validación/feedback`.
   Esto no es un template obligatorio; el contrato del artefacto tiene precedencia.

4. **Dar orientación antes de detalle.** El título, primer bloque y headings deben permitir reconocer rápidamente el propósito y el cambio principal. No introducir implementación antes de que exista una razón mental donde ubicarla.

5. **Construir comprensión causal.** Preferir `causa → mecanismo → consecuencia` sobre inventarios de hechos. Introducir conceptos antes de depender de ellos y mantener pequeño el conjunto de conceptos que el lector debe recordar simultáneamente. Cerrar una relación antes de abrir varias nuevas.

6. **Favorecer reconocimiento sobre memoria.** Mantener cerca la información necesaria para interpretar una afirmación. Repetir brevemente contexto cuando evita backtracking; no usar referencias vagas como “lo anterior”, “este caso” o “dicho comportamiento” si el referente puede nombrarse de forma barata.

7. **Aplicar profundidad progresiva.** Mantener propósito, comportamiento, decisión y riesgo material en el camino principal. Mover configuración, evidencia extensa, casos borde y detalle interno después de que el modelo principal ya sea comprensible. Usar diagramas sólo cuando reduzcan el esfuerzo de entender relaciones, flujo o cambio.

8. **Editar por carga cognitiva.** Eliminar meta-narrativa, orden de investigación, detalles que no alteran comprensión o decisión, repetición sin función y headings genéricos. Si una sección necesita demasiadas explicaciones para entenderse, reordenarla antes de agregar texto.

9. **Validar desde el lector.**
   - **Scan test:** título, headings y primeras frases permiten reconocer propósito, cambio y zonas relevantes.
   - **Backtracking test:** el camino principal puede leerse sin volver atrás repetidamente para recuperar contexto.
   - **Mental-model test:** el lector puede explicar qué pasa, por qué y qué efecto produce sin inventar conexiones.
   - Para PRs, el lector debería llegar al diff sabiendo qué comportamiento espera encontrar y dónde merece concentrar la review.

## Output

Entregar el artefacto en el formato requerido por su template o contexto.

Si falta evidencia o una decisión material, declararlo separadamente sin inventarla ni esconderla dentro de una narrativa fluida.

## Hard Rules

- Fuentes autoritativas y contrato del artefacto tienen precedencia sobre esta skill.
- No publicar el orden de investigación, implementación ni razonamiento interno del agente.
- No introducir una solución antes de establecer el problema o necesidad que le da sentido, salvo que el artefacto exija otra estructura.
- No simplificar eliminando complejidad necesaria para revisar, operar o decidir.
- No convertir incertidumbre en certeza para mejorar la fluidez narrativa.
- No obligar al lector a recordar información que puede mantenerse visible o reiterarse brevemente.
- No repetir información sin una nueva función cognitiva; contexto mínimo repetido para evitar backtracking sí es válido.
- No usar listas largas como sustituto de estructura, ni convertir información inherentemente enumerativa en prosa artificial.
- No usar diagramas decorativos ni duplicar en ellos lo que la prosa ya hace igual de bien.
- No rescatar una estructura fallida agregando explicación: reordenar primero.
- No inflar el alcance actual con trabajo futuro; separar explícitamente lo que cambia ahora de lo que podría seguir.
