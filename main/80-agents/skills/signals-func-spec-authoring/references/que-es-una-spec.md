# Qué es una spec (y por qué no se comenta a sí misma)

Regla compartida por `signals-func-spec-authoring` y `signals-tech-spec-authoring`. Es la que más se rompe y la que más caro sale.

---

## La definición

**Una spec describe un estado objetivo. No es un relato de cómo se llegó a él.**

El documento terminado tiene que leerse como si el diseño que describe hubiera sido siempre así. No tiene memoria de sí mismo: no sabe que existió un borrador, no sabe que alguien pidió un cambio, no sabe que ayer decía otra cosa. Un lector que la abre hoy por primera vez tiene que poder entenderla entera **sin conocer ninguna versión anterior**, porque para él ninguna existió.

Eso no es una preferencia de estilo. Es lo que hace que una spec sirva como contrato: si el texto mezcla el diseño con la historia del diseño, el lector no puede distinguir qué es vigente de qué es residuo, y tiene que reconstruir la conversación que no presenció para saber qué implementar.

---

## La regla del lector cero

Antes de escribir cualquier frase, preguntate: **¿esta frase tiene sentido para alguien que nunca vio otra versión de este documento?**

Si la respuesta es no, la frase es ruido y se borra. No se reformula, no se mueve a un apéndice, no se pone entre paréntesis: **se borra**.

Frases que siempre fallan la prueba:

- "ya no es A, ahora es B"
- "se cambió porque…", "se corrigió el punto 4"
- "antes decía…", "la versión anterior…", "reemplaza el borrador…"
- "según lo solicitado", "a pedido del owner", "por indicación de …"
- "esta versión es más concisa que la anterior"
- "originalmente se planteó A, pero…"
- una sección "Cambios respecto de la versión previa" o "Changelog"

Todas comparten el mismo defecto: **solo se entienden si conocés un documento que ya no existe.**

---

## Cuando te piden cambiar A por B

Este es el caso que más se rompe, porque el impulso de "documentar el cambio" se siente como rigor y es exactamente lo contrario.

Te piden: *"cambiá el punto 4 de A a B, porque B nos conviene."*

**El entregable correcto** es una spec donde el punto 4 dice B, con la fundamentación de B, y donde **A no aparece en ningún lado**. Ni en el punto 4, ni en decisiones, ni en alternativas descartadas, ni en una nota al pie. Para el lector, A nunca existió.

**El entregable incorrecto**, y es lo que sale por default si no te frenás:

> **Decisión 4.** El punto 4 ya no es A sino B. Se cambió porque a nosotros nos conviene B.

Eso deja al lector persiguiendo una A que no está definida en ninguna parte del documento, y convierte una decisión de diseño en un chisme sobre el proceso de edición.

**El historial ya existe y no es tu trabajo.** Spellbook versiona cada spec (`spellbook specs versions`). Quién cambió qué y cuándo vive ahí, que es donde se puede consultar, comparar y auditar. Duplicarlo dentro del documento no agrega trazabilidad: agrega ruido y una segunda fuente que se desincroniza.

---

## La distinción que sí importa: alternativa descartada vs versión anterior

Una sección de **alternativas descartadas** es legítima y el equipo la usa (`DD-N` → *Discarded alternatives*, tablas con ✅/❌). No la borres por confundirla con lo de arriba. La diferencia:

| | Alternativa descartada (va) | Versión anterior del documento (no va) |
|---|---|---|
| **Dónde existe** | En el espacio de soluciones. Cualquier lector competente la propondría al leer el diseño. | Solo en la historia de edición de este archivo. |
| **Prueba** | "¿Un reviewer que ve esto por primera vez preguntaría *por qué no hicieron X*?" → si sí, X va. | "¿Solo sé que esto existió porque estuve en la conversación?" → si sí, no va. |
| **Ejemplo** | "¿Por qué Strategy Pattern y no un `if/else` por `component_type`?" — el `if/else` es la opción obvia; hay que cerrarla. | "El punto 4 antes era A." — nadie lo habría propuesto ni lo extraña. |

Dicho corto: **se descarta una solución, no un párrafo.**

---

## El corolario sobre las justificaciones

Una fundamentación explica **por qué el diseño es correcto**, no **por qué el documento cambió**.

"Se eligió B porque el owner lo pidió" no es una fundamentación: es una atribución, y no le sirve a nadie que tenga que decidir si B está bien. Si la única razón que podés dar para una decisión es que alguien la pidió, entonces no tenés una decisión de diseño: tenés una instrucción. Escribí el diseño resultante y **no abras un `DD-N` para eso** — un `DD-N` sin fundamentación técnica es peso muerto que además invita a citar la conversación.

Si la razón real es buena pero venía del usuario, escribila como razón técnica: no "dmuena pidió que `params` no se toque", sino "`params` conserva la configuración propia del componente, que el Context no reemplaza".

---

## Chequeo antes de publicar

```bash
grep -nEi "ya no |antes (decía|era)|versión (anterior|previa)|se (cambió|corrigió|modificó|reemplaz)|originalmente|a pedido|según lo solicitado|changelog|borrador (anterior|previo)|reemplaza el" spec.md
```

Cero resultados, o cada resultado justificado y verificado a mano. Si hay uno solo que no puedas defender frente a la regla del lector cero, borralo antes de publicar.
