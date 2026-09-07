---
type: skill
name: agents-os-requirement-interview
scope: global
created: 2026-08-06
updated: 2026-08-08
description: Interview the user to close the context gap before executing a non-trivial task. Use when the request is ambiguous, has multiple valid designs, touches irreversible decisions, or the user asks for an interview / "pregúntame lo que no entiendas" / "hazme una entrevista" / "levantemos requerimientos". Produces high-value, request-specific questions derived from evidence — never a generic questionnaire — plus an explicit assumption ledger.
tags:
  - kind/skill
  - action/requirement-interview
  - action/planning
  - tech/agents-os
---

# AGENTS OS Requirement Interview

## Purpose

Convertir una solicitud ambigua en contexto suficiente para ejecutar sin
retrabajo, gastando el mínimo de turnos del usuario. La entrevista no es un
cuestionario: es un método para descubrir qué decisiones existen, cuáles el
agente debe resolver solo, y cuáles solo el usuario puede responder.

Lazy-load. Invocar antes de planificar o implementar algo no trivial.

## Minimal Read

1. Fuentes del dominio de la solicitud (código, specs, docs, historial) vía
   `agents-os-context-retrieval` o Graphify del repo.
2. `agents-os-implementation-planning` solo si el resultado será un proyecto por
   fases.

## Procedure

### 1. Investigar primero (obligatorio, antes de cualquier pregunta)

Levantar la evidencia disponible: código, specs, configuración real, ejemplos de
payload, historial de decisiones, artefactos previos del mismo pipeline.
Si un dato es obtenible por el agente, obtenerlo. Preguntarlo es un defecto.

### 2. Construir el mapa de decisiones

Enumerar las decisiones que la ejecución va a forzar (no las tareas). Clasificar
cada una en exactamente un cubo:

```text
RESUELTA   evidencia directa    -> registrar el hecho + fuente
SUPUESTO   default seguro       -> anotar en el ledger, no preguntar
PREGUNTA   solo el usuario sabe -> entra a la entrevista
```

### 3. Filtrar cada candidata a pregunta

Una pregunta entra solo si pasa las cuatro:

- **Divergente**: ≥2 respuestas plausibles producen diseños materialmente
  distintos.
- **Costosa**: equivocarse implica retrabajo, migración, pérdida de datos,
  corridas desperdiciadas o cambio de contrato público.
- **No derivable**: no está en el código, los docs, el historial ni en el propio
  mensaje del usuario.
- **De su dominio**: intención de negocio, prioridad, realidad operativa,
  hardware, sistemas externos, tolerancias, gustos. Decisiones de ingeniería
  las toma el agente.

### 4. Barrer ejes ciegos

Recorrer estos ejes para detectar huecos; instanciarlos en el dominio concreto.
No son preguntas: son direcciones de búsqueda. La mayoría se resolverá como
hecho o supuesto.

```text
Resultado        qué significa "listo"; quién consume la salida
Frontera         qué queda explícitamente fuera de alcance
Contrato         forma exacta de entradas y salidas; identidad/correlación
Escala           volumen, concurrencia, duración, presupuesto de tiempo
Falla            fallo parcial, reintento, idempotencia, qué es aceptable perder
Entorno          dónde corre, qué existe físicamente hoy, qué hay que crear
Ciclo de vida    quién opera, retención, limpieza, evolución
Verificación     con qué evidencia el usuario declara éxito
Trade-off        velocidad vs completitud, reuso vs módulo nuevo
Reversibilidad   qué no se puede deshacer
```

### 5. Detectar X-Y

Si la solución propuesta por el usuario huele a síntoma, incluir **una** pregunta
que ataque el objetivo de fondo, con la alternativa concreta ya evaluada.
No cuestionar el enfoque sin ofrecer alternativa.

### 6. Formular

- Cerradas con opciones concretas extraídas de la evidencia real, con una
  recomendada; abiertas solo cuando el espacio de respuestas es genuinamente
  libre.
- Declarar la consecuencia de cada opción en una línea.
- Una decisión por pregunta. Nada de preguntas compuestas.
- Ordenar por radio de impacto: primero lo que invalida otras preguntas.
- 5–9 preguntas por ronda, agrupadas por tema.
- Mostrar la tarea hecha: listar antes los hechos ya establecidos, para que el
  usuario solo corrija deltas.
- Usar la herramienta de opción múltiple del cliente cuando exista; si no,
  numerar con opciones explícitas.

### 7. Iterar acotado

Ronda 1: estructural e irreversible. Ronda 2: solo lo que las respuestas de la
ronda 1 desbloquearon. Tope 2 rondas, 3 por excepción justificada. Cerrar cuando
lo que queda puede ser supuesto seguro.

### 8. Cerrar con delta

Antes de ejecutar, devolver el delta de contexto: qué cambió respecto de la
hipótesis inicial, el ledger de supuestos final y el criterio de aceptación
enunciado en los términos del usuario.

## Output

Bloque previo a las preguntas:

```text
Entendido (hechos verificados): <bullets con fuente>
Asumo (ledger): <supuesto -> default -> costo si es incorrecto>
Necesito de ti: <N> decisiones
```

Cada pregunta:

```text
[<eje>] <pregunta única>
  A) <opción> -> <consecuencia>   (recomendada: <razón en una línea>)
  B) <opción> -> <consecuencia>
  Si no respondes: <default que aplico>
```

Cierre tras respuestas:

```text
Delta de contexto:   <qué cambió vs. hipótesis inicial>
Supuestos vigentes:  <lista>
Criterio de aceptación: <en palabras del usuario>
Siguiente paso:      <acción concreta>
```

## Hard Rules

- Prohibido preguntar lo que el agente puede averiguar; investigar es
  prerrequisito de la entrevista.
- Prohibido preguntar lo que el usuario ya dijo en la solicitud o en el
  historial de la sesión.
- Prohibido el cuestionario genérico: toda pregunta debe ser irrepetible en otra
  solicitud.
- Prohibido pedir permiso en vez de pedir una decisión ("¿quieres que lo haga
  bien?" no es pregunta).
- Prohibido esconder una decisión de diseño dentro de una pregunta: si el agente
  ya tiene una recomendación, la declara.
- Toda incógnita no preguntada queda como supuesto explícito con su default.
- Nunca convertir en definitiva una cifra o regla que el usuario declaró
  ilustrativa.
- No iniciar ejecución con una decisión irreversible pendiente de respuesta.
