# Modos de falla de un spec técnica

Catálogo de lo que hace que una técnica envejezca mal o mienta.

Cada entrada trae un caso real. **Los ejemplos citados son de borradores que ya no existen** —la mayoría de un draft de SIG-590 que fue reescrito— y están acá como material de enseñanza, no como descripción de ninguna spec vigente. No vayas a buscar estas frases en Spellbook: no están, y ése es justamente el punto.

---

## 1. Meta-narrativa: la spec cuenta cómo fue escrita

**Síntoma.** Bloques que hablan del proceso de autoría en vez del diseño:

> Escrita **desde cero** sobre `develop` de `rio-playmaker` y `master` de `rio-sdk-events`. No reutiliza diseño ni código de ninguna rama anterior.

> ## 2. Punto de partida verificado

**Por qué está mal.** Nada de eso le sirve al lector. "Desde cero" y "no reutiliza el diseño anterior" son la defensa del autor frente a un intento descartado que el lector no conoce: es contexto de la conversación, no del documento. "Verificado" es peor, porque además **caduca**: el día que alguien mergea a `develop`, la sección sigue diciendo "verificado" y ya no lo está.

**Regla.** Los hechos de una técnica son hechos; anunciarlos como verificados no los hace más ciertos, los hace más frágiles. La confianza la da la **cita** (`archivo:línea` contra un commit base declarado), no el adjetivo.

**Corrección.** Borrá el bloque. La información que sí importaba —repos, ramas, commits base— ya vive en la tabla de §1. Renombrá la sección por lo que realmente contiene: `## 2. Restricciones del código existente`.

---

## 2. Punteros cruzados podridos

**Síntoma.** Los `DD-N` se renumeran mientras se edita y las referencias viejas quedan. El §2 de ese draft tenía **cuatro** referencias apuntando a la decisión equivocada:

| Decía | Debía decir | Tema real |
|---|---|---|
| `(§5.5, DD-13)` | `DD-20` | el resolver no puede usar `Casting` |
| `(DD-9, DD-10)` | `DD-16, DD-17` | `service` sin unique ⇒ 0, 1 o N filas |
| `(DD-15)` | `DD-23` | el gate cuelga del data product |
| `` `{}` (DD-14) `` | `DD-13` | `LastDeployedVersion` de un solo row |

Más un `PT-6` que debía ser `PT-10`.

**Por qué está mal.** Nada falla: la numeración es contigua, sin huecos ni duplicados, y un chequeo automático la da por buena. El daño es en el lector, que sigue el puntero, aterriza en una decisión sin relación, y a partir de ahí desconfía de **todas** las citas del documento.

**Regla.** El chequeo automático detecta referencias no definidas y huecos; **no** detecta una referencia bien formada que apunta al lugar equivocado. Después de cualquier renumeración, releé a ojo cada referencia que quedó dentro de una tabla — es donde se esconden.

---

## 3. Cobertura optimista

**Síntoma.** Un draft declaraba en §1:

> Cobertura: RF-1 a RF-7, CA-1 a CA-8 y E2E-1 a E2E-3 de SIG-573.

y §13, al final del documento, admitía:

> RF-4 asume que los valores viajan siempre, lo que PT-1 pone en duda para v1.

**Por qué está mal.** Las dos no pueden ser verdad. El gate de seguridad dejaba los valores de `outputs` detrás de un flag apagado por default, así que lo que se despliega entrega **topología sin valores**: RF-4 y CA-6 quedan inertes, y CA-4, E2E-2 y E2E-3 pasan **trivialmente** porque todos los `outputs` van vacíos — dejan de discriminar, que es peor que fallar.

**Regla.** La cobertura se declara sobre **la configuración que se despliega**, no sobre el código escrito. Si un flag, una fase o un gate dejan un requisito inerte, se dice arriba, en la línea de cobertura, con los ids exactos. Un test que pasa con el flag encendido no cubre un requisito que se despliega con el flag apagado.

---

## 4. Una decisión del autor disfrazada de decisión del equipo

**Síntoma.** El diseño contradice el funcional y la contradicción se resuelve sola, dentro de la técnica, y se reporta como un párrafo suelto al final de las preguntas abiertas.

**Por qué está mal.** El funcional es el contrato con el equipo. Una técnica puede **demostrar** que el contrato está mal —es una de las cosas más valiosas que hace— pero no puede reescribirlo por su cuenta.

**Regla.** Sección propia (`## N. Enmiendas que requiere <funcional>`), numeradas `E-N`, cada una con: el texto actual del funcional, por qué es falso con la cita que lo demuestra, y **el texto de reemplazo propuesto**. Un reemplazo redactado se puede aprobar en una reunión; una descripción del problema genera otra ronda.

---

## 5. La métrica que se cuenta dos veces

**Síntoma.** Un draft tenía un DD entero explicando por qué el counter `derivation` se emite desde el adapter post-commit y no desde el builder (una transacción que revierte inflaría el denominador)… y cerraba con:

> La única excepción es el `safeCount(FAILED)` del `catch` de `build`.

**Por qué está mal.** Esa excepción reintroduce los dos sesgos que el DT venía a evitar: cada fallo que sí se publicó se cuenta **dos veces** (builder + adapter), y los fallos de transacciones revertidas se cuentan igual. El DD se contradecía a sí mismo en su última oración, y la implementación copió la contradicción.

**Regla.** Cuando un DD establece un invariante ("se emite en un solo lugar, y es éste"), la excepción que se agrega después no es un detalle: o rompe el invariante, o el invariante estaba mal. Revisá las últimas oraciones de los DD largos — es donde se cuelan.

---

## 6. Un orden de entrega que no se puede ejecutar

**Síntoma.**

| # | Paso |
|---|---|
| 1 | rama feature en el SDK con `version = 1.4.0` |
| 3 | Publicar `rio-sdk-events` **1.4.0** real |
| 5 | …, PR de los dos repos |

**Por qué está mal.** El paso 3 publica una versión productiva **antes** de que exista el PR del paso 5: el release sale de la rama feature. Es exactamente lo que la regla de versionado prohíbe, y no se puede hacer.

**Regla.** El orden de entrega se lee como una secuencia ejecutable, paso por paso, preguntando en cada uno "¿desde qué rama?". Merge a `master` **antes** del release; el consumidor itera contra una versión de prueba `0.0.x-<descripcion>` mientras tanto. Y si hay un gate (de seguridad, de decisión), tiene que bloquear **un paso numerado**, no "el rollout" en abstracto: un gate sin paso identificado se pisa por inercia.

---

## 7. Un dato que decae disfrazado de invariante

**Síntoma.** "los **seis** CP (kafka, clickhouse, flink, signals, fury, observability) reciben y deserializan todos los mensajes".

**Por qué está mal.** El número es correcto hoy y falso el día que entra un CP nuevo — y el argumento de seguridad que lo usa (radio de exposición) es justamente el que no puede quedar desactualizado. Además el conjunto de suscriptores **no es un dato del contrato**: no hay dónde verificarlo.

**Regla.** Cuando el argumento depende de un conjunto que cambia, escribí el **predicado**, no la enumeración: "todo consumidor suscripto al topic", y citá dónde está declarado (`DeploymentTriggerMessage.java:16-17`). Vale para listas de servicios, de equipos y de consumidores. El mismo criterio aplica a los baselines numéricos (conteo de tests, cobertura): van anclados al commit base que los produjo.

---

## 8. Una convención presentada como control

**Síntoma.** "Los control planes reciben una **instrucción normativa** nueva en el javadoc del contrato".

**Por qué está mal.** Un javadoc documenta; no obliga a nadie, menos a apps de otros equipos, y no hay gate que lo verifique. Llamarlo normativo hace que un riesgo abierto se lea como mitigado. La propia spec lo admitía sin darse cuenta al decir que era "la única palanca que tenemos" — que es un argumento de que es **débil**, no de que es normativa.

**Regla.** Nombrá los controles por lo que hacen cumplir. Documentación es documentación; control es lo que falla el build, rechaza el request o suprime el dato. Si sólo tenés documentación, decilo y abrí un `PT-N` para convertirla en control. Mismo criterio para los controles que **no** se acreditan: un filtro cuyo flag no tiene productor da una métrica clavada en 0 que se lee como "no hay problema" — peor que no tener control, y hay que escribir por qué no cuenta.
