---
type: resource
status: active
area: "[[Personal]]"
created: 2026-07-08
updated: 2026-08-08
aliases:
  - prompts-v2
  - PROMPTS_V2
tags:
  - resource
  - vibe-coding
  - pilar
---

# **PROMPTS_V2: Arquitectura de Flow Engineering para la Generación de Artefactos Técnicos de Alta Precisión**

## **1\. El Cambio de Paradigma: De la Interacción Basada en Chat al Flow Engineering Orientado a Especificaciones**

La industria del desarrollo de software se encuentra en un punto de inflexión crítico en 2025\. La interacción convencional con los Grandes Modelos de Lenguaje (LLMs) a través de interfaces de chat efímeras está siendo reemplazada por arquitecturas de estado robustas y secuenciales conocidas como **Flow Engineering**. Para los líderes técnicos y arquitectos de sistemas, esta evolución no es meramente incremental, sino fundamental. El enfoque tradicional de "plantillas de chat" (chat templates), aunque suficiente para consultas ad-hoc o la generación de fragmentos de código aislados, se fractura bajo la carga cognitiva requerida para generar artefactos técnicos de alta precisión y coherencia a gran escala, como los Documentos de Requisitos del Producto (PRDs) y las Solicitudes de Comentarios (RFCs).

El estado del arte (SOTA) en 2025 para la IA generativa en ingeniería de software ya no se define por la inteligencia bruta de un modelo subyacente, sino por la orquestación de su proceso de razonamiento. La metodología **"Spec-First"** (Primero la Especificación), donde las especificaciones técnicas se tratan como la fuente principal de verdad y el código como un artefacto derivado, exige un marco de ingeniería de prompts que refleje el rigor del proceso de ingeniería mismo.1 La iniciativa "PROMPTS\_V2" aborda esta necesidad transformando las plantillas estáticas en flujos agénticos dinámicos que imponen integridad estructural, consistencia lógica y restricciones específicas del dominio a través de un diseño de sistemas deliberado.

### **1.1 Las Limitaciones Estructurales del Prompting en Chat para Artefactos Complejos**

La dependencia de las interacciones basadas en chat para la generación de documentación compleja introduce varios modos de fallo inherentes a la naturaleza lineal y no iterativa de la decodificación estándar de los LLM. Cuando un usuario solicita un PRD completo en un solo prompt (Single-Turn), está pidiendo efectivamente al modelo que realice la planificación de alto nivel, la redacción detallada, la validación de restricciones y la referencia cruzada de dependencias simultáneamente dentro de un único paso de ventana de contexto. Esta compresión de tareas cognitivas dispares en una sola inferencia degrada la calidad del resultado final.

La investigación sobre los modos de pensamiento "Sistema 1" (rápido, intuitivo, asociativo) frente al "Sistema 2" (lento, deliberado, lógico) en la inteligencia artificial sugiere que los prompts de turno único fuerzan a los modelos a operar en un modo "Sistema 1". En este estado, el modelo se basa en la asociación probabilística de tokens en lugar de en un razonamiento estructurado y planificado.4 Para las especificaciones técnicas, esto resulta en fenómenos perjudiciales como la **deriva contextual**, donde el modelo pierde el rastro de las restricciones iniciales a medida que avanza la generación, provocando contradicciones entre secciones críticas como los "Objetivos del Negocio" y los "Requisitos Funcionales". Además, sin un anclaje estricto en un flujo de referencia, los modelos tienden a **alucinar estándares**, inventando APIs inexistentes o patrones arquitectónicos que suenan plausibles fonéticamente pero que son funcionalmente imposibles.

El **Flow Engineering** aborda estos déficits descomponiendo el proceso de generación en etapas discretas y verificables.5 En lugar de un solo prompt monolítico de "Escribe un PRD", un flujo orquesta una secuencia lógica: *Extracción de Requisitos* $\\rightarrow$ *Generación de Esqueleto* $\\rightarrow$ *Redacción de Secciones* $\\rightarrow$ *Comprobación de Restricciones (Critic)* $\\rightarrow$ *Ensamblaje Final*. Este enfoque modular permite simular un razonamiento de "Sistema 2", donde los resultados intermedios pueden ser validados y refinados algorítmicamente antes de influir en el artefacto final.

La diferencia fundamental radica en el control y la escalabilidad. Mientras que el Prompt Engineering tradicional se centra en optimizar la entrada textual para una sola inferencia estocástica, el Flow Engineering se centra en diseñar el grafo de interacciones deterministas entre múltiples llamadas al modelo, permitiendo la integración de herramientas externas y bucles de retroalimentación.5

**Tabla 1: Análisis Comparativo de Prompt Engineering vs. Flow Engineering en Contextos Técnicos**

| Aspecto | Prompt Engineering (Enfoque Tradicional) | Flow Engineering (Enfoque PROMPTS\_V2) |
| :---- | :---- | :---- |
| **Alcance Operativo** | Prompts únicos o cadenas de pensamiento lineales simples. | Interacciones estructuradas y ramificadas entre múltiples componentes agénticos. |
| **Nivel de Control** | Limitado; los cambios en el fraseo pueden alterar toda la estructura de salida. | Alto; soporta interacciones modulares, anidadas y validación de tipos de datos. |
| **Mecanismos de Feedback** | Inexistentes o manuales (Human-in-the-loop reactivo). | Bucles de retroalimentación robustos con refinamiento iterativo y autocrítica automática. |
| **Gestión de Errores** | Estocástica; se confía en la probabilidad del modelo. | Determinista; se valida la salida contra esquemas y se reintenta si falla. |
| **Caso de Uso Ideal** | Respuestas rápidas, resúmenes, escritura creativa breve. | PRDs, RFCs, Generación de Código Complejo, Análisis de Sistemas Distribuidos. |
| **Escalabilidad** | Limitada por la ventana de contexto y la atención del modelo. | Altamente escalable y concurrente mediante la descomposición de tareas. |

Datos derivados y sintetizados de análisis comparativos sobre metodologías de interacción con LLMs.5

### **1.2 La Filosofía Spec-First en la Era de la IA Generativa**

La filosofía "Spec-First" postula que la especificación en lenguaje natural —si es suficientemente rigurosa e inequívoca— es el verdadero código fuente, mientras que el código de programación tradicional se convierte en un artefacto de implementación derivado. En un flujo de trabajo aumentado por IA, la especificación se convierte en el "meta-prompt" para el agente de codificación. Por lo tanto, la precisión, claridad y completitud de la especificación se correlacionan directamente con la calidad y fiabilidad del software generado.

La transición al desarrollo **Spec-Driven (SDD)** altera fundamentalmente el rol del ingeniero de prompts. El objetivo ya no es persuadir al modelo para obtener una salida creativa, sino restringirlo para obtener una salida compatible con los estándares. Las especificaciones se escriben primero para servir como la "fuente de verdad" inmutable tanto para los desarrolladores humanos como para los agentes de IA.7 Al iterar sobre las especificaciones en lugar de sobre el código, los equipos logran una modularidad inherente y una reducción drástica en el uso de tokens, ya que las especificaciones son órdenes de magnitud más compactas que las bases de código verbosas que describen.3

En el marco PROMPTS\_V2, las plantillas dejan de ser meros archivos de texto para convertirse en **compuertas lógicas ejecutables**. Un flujo de generación de PRD puede utilizar un prompt de "Cadena de Densidad" (Chain-of-Density) para asegurar que el resumen ejecutivo contenga la máxima información por token 8, seguido de un prompt de "Planificar y Resolver" (Plan-and-Solve) para derivar criterios de aceptación matemáticamente precisos a partir de historias de usuario.10 Esta estructuración rigurosa asegura que el documento resultante no sea solo un texto pasivo, sino un plano funcional capaz de dirigir agentes de codificación aguas abajo como Cursor, Windsurf o Devin.12

La adopción de este enfoque transforma el ciclo de vida del desarrollo de software. El código se vuelve "desechable" en cierto sentido; si la implementación es defectuosa pero la especificación es correcta, el código puede regenerarse con un costo marginal cercano a cero. Sin embargo, si la especificación es ambigua, ninguna cantidad de regeneración de código resolverá el problema de raíz. Por lo tanto, el valor se desplaza de la sintaxis a la semántica, y de la implementación a la definición. PROMPTS\_V2 está diseñado para maximizar la calidad de esta definición.

## **2\. Arquitecturas Cognitivas para la Documentación Técnica**

Para elevar la calidad de los artefactos técnicos más allá de lo que permite un simple prompt, el marco PROMPTS\_V2 incorpora patrones de prompting cognitivo avanzados. Estas técnicas no son meros trucos retóricos, sino que obligan al modelo a exponer su razonamiento latente, planificar su estructura de salida e incrementar iterativamente la densidad de información, simulando así los procesos cognitivos de un ingeniero senior durante la redacción técnica.

### **2.1 Cadena de Pensamiento (Chain-of-Thought) y Razonamiento Documental**

La técnica de **Chain-of-Thought (CoT)** mejora significativamente el rendimiento de los LLM en tareas de razonamiento complejo al alentar al modelo a generar pasos intermedios antes de llegar a una respuesta final.14 En el contexto de la documentación técnica, CoT no se trata solo de obtener la "respuesta correcta" a un problema matemático, sino de asegurar la coherencia lógica y la trazabilidad de las decisiones dentro de la estructura del documento.

Para un PRD, un prompt CoT estándar es insuficiente. PROMPTS\_V2 implementa un **CoT Documental**, que instruye al modelo a realizar una derivación lógica explícita antes de redactar cualquier sección. Por ejemplo, en lugar de solicitar simplemente "Historias de Usuario", el sistema instruye:

"Primero, identifica las personas usuarias principales y sus motivaciones intrínsecas basándote en la descripción del producto. Segundo, mapea estas motivaciones a puntos de dolor específicos y tangibles. Tercero, deriva características funcionales que aborden directamente estos puntos de dolor. Finalmente, formula Historias de Usuario basadas en estas características, asegurando que cada historia tenga un origen rastreable en una motivación de usuario."

Este rastro de razonamiento intermedio asegura que las Historias de Usuario finales estén profundamente arraigadas en las personas establecidas, evitando los textos genéricos o desconectados que a menudo resultan de la generación directa. La investigación indica que el prompting CoT mejora la precisión y la coherencia al permitir que el modelo "piense" antes de escribir, utilizando eficazmente el tiempo de computación (tokens de salida) para alinear su estado interno con las restricciones de la tarea.16

**Aplicación en PROMPTS\_V2:**

* **Pre-computación Lógica:** El marco exige un bloque de \<thinking\> (a menudo oculto en la salida final presentada al usuario pero visible en los logs) donde el modelo esquematiza la lógica del documento.  
* **Mapeo de Dependencias:** CoT se utiliza para mapear explícitamente las dependencias entre los requisitos funcionales y las restricciones técnicas antes de que se redacten las secciones, identificando conflictos potenciales en la fase de "pensamiento" antes de la "escritura".

### **2.2 Esqueleto de Pensamiento (Skeleton-of-Thought) para la Integridad Estructural**

La generación de documentos de formato largo, como los RFCs detallados, a menudo conduce a la "fatiga de contenido", donde la calidad del texto se degrada hacia el final de la generación, o el modelo se apresura a concluir, omitiendo detalles cruciales. **Skeleton-of-Thought (SoT)** es una técnica diseñada para mitigar esto desacoplando la generación de la estructura de la expansión del contenido.18

El proceso SoT implica dos etapas distintas y secuenciales:

1. **La Etapa del Esqueleto:** Se solicita al modelo que genere un esquema de alto nivel o "esqueleto" del documento. Este esqueleto es conciso, centrándose únicamente en la jerarquía de encabezados y breves puntos clave para el contenido, sin prosa narrativa.  
2. **La Etapa de Expansión de Puntos:** El modelo (o múltiples llamadas paralelas al modelo) expande cada punto del esqueleto en párrafos completos y detallados.

Este método no solo mejora la latencia al permitir la generación paralela en arquitecturas que lo soportan 20, sino que, lo que es más importante para la documentación técnica, asegura que la estructura global del documento permanezca consistente. Al fijar el esqueleto primero, el modelo se compromete con una estructura coherente, evitando la "divagación" o el cambio de alcance que a menudo se observa en las generaciones secuenciales largas.

**Aplicación en PROMPTS\_V2:**

* **Estructura de RFC:** El marco genera primero la Tabla de Contenidos para un RFC, la valida contra la plantilla estándar (Introducción, Motivación, Diseño Detallado, Alternativas, Riesgos), y luego expande cada sección individualmente manteniendo el contexto global.  
* **Contratos de Consistencia:** El esqueleto sirve como un contrato inmutable. La fase de expansión está restringida a una adherencia estricta a los puntos del esqueleto, previniendo la desviación del alcance (scope creep) durante la generación del texto.

### **2.3 Cadena de Densidad (Chain-of-Density) para Resúmenes de Alta Precisión**

Los artefactos técnicos a menudo requieren resúmenes ejecutivos que sean densos en información pero concisos en longitud. Los prompts de resumen estándar a menudo producen texto "esponjoso" y de baja entropía. **Chain-of-Density (CoD)** es un método de prompting iterativo diseñado para producir resúmenes que se vuelven progresivamente más detallados y ricos en entidades sin aumentar su longitud total.8

El proceso CoD implica generar un resumen inicial y luego refinarlo iterativamente identificando "entidades faltantes" (hechos clave, métricas, términos técnicos específicos) y fusionándolos en el texto existente. Esto obliga al modelo a eliminar palabras de relleno, transiciones innecesarias y redundancias para "hacer espacio" para la nueva información, aumentando así la densidad léxica y semántica del resultado.

**Tabla 2: Proceso de Iteración de Cadena de Densidad (CoD)**

| Iteración | Foco Cognitivo | Resultado en el Artefacto |
| :---- | :---- | :---- |
| **Inicial** | Visión General Amplia | Resumen disperso en entidades, muy legible pero carente de detalles técnicos específicos. |
| **Refinamiento 1** | Identificación de Entidades Faltantes | Integración de términos técnicos clave (e.g., "OAuth2", "Redis", "Latencia p99"). |
| **Refinamiento 2** | Compresión Sintáctica | Eliminación de transiciones verbosas ("el artículo dice que...") para liberar tokens. |
| **Refinamiento 3** | Abstracción y Fusión | Síntesis de conceptos complejos en frases nominales densas. |
| **Final** | Optimización de Entropía | Resumen de alta entropía adecuado para el liderazgo técnico y la revisión rápida. |

Metodología basada en la investigación de optimización de resúmenes.9

**Aplicación en PROMPTS\_V2:**

* **Generación de Abstract:** Se utiliza para la sección "Abstract" de los RFCs y el "Resumen Ejecutivo" de los PRDs para asegurar la máxima transmisión de información técnica en el mínimo espacio visual.  
* **Condensación de Requisitos:** Se utiliza para convertir notas de entrevistas con stakeholders, que suelen ser verbosas y desestructuradas, en declaraciones de requisitos atómicas, nítidas y libres de ambigüedad.

### **2.4 Prompting Plan-and-Solve para Lógica Técnica**

El prompting **Plan-and-Solve (PS)** extiende el CoT solicitando explícitamente al modelo que idee un plan detallado antes de la ejecución.11 Esto es particularmente efectivo para las secciones de "Consideraciones Técnicas", "Migración" o "Hitos" de un PRD, donde se requiere un razonamiento cuantitativo (e.g., estimación, planificación de capacidad) o secuencial riguroso.

A diferencia del CoT Zero-Shot ("Pensemos paso a paso"), el prompting PS ordena: "Primero, comprende el problema y diseña un plan para resolverlo. Luego, lleva a cabo el plan paso a paso". Esta separación ayuda a reducir los errores de cálculo y los pasos faltantes en las derivaciones lógicas, que son críticos cuando se definen cronogramas de ingeniería o estimaciones de carga.25

**Aplicación en PROMPTS\_V2:**

* **Planificación de Implementación:** Se utiliza para descomponer una característica compleja en tareas de ingeniería discretas, asegurando que no se omitan pasos prerrequisitos (como migraciones de bases de datos, actualizaciones de contratos de API o configuraciones de infraestructura).  
* **Evaluación de Riesgos:** El modelo planifica un "barrido de riesgos" a través de categorías específicas (Seguridad, Rendimiento, Cumplimiento, Operaciones) antes de listar riesgos específicos, asegurando una cobertura exhaustiva.

## **3\. Ingeniería del Documento de Requisitos del Producto (PRD)**

El PRD es la piedra angular del enfoque "Spec-First". Un PRD exitoso en 2025 no es simplemente un documento de texto para lectura humana; es un objeto de datos estructurado que puede ser analizado (parsed) tanto por ingenieros humanos como por agentes de codificación de IA. El marco PROMPTS\_V2 utiliza una arquitectura basada en Markdown específica para PRDs, influenciada por las plantillas rigurosas de Uber 26 y la metodología "Working Backwards" de Amazon.27

### **3.1 La Estructura PRD "Spec-First" en Markdown**

El marco adopta una estructura Markdown estandarizada que asegura la compatibilidad con IDEs Agénticos (como Cursor o Windsurf) que dependen del contexto estructurado para generar código de alta calidad.12

**Secciones Nucleares del PRD PROMPTS\_V2:**

1. **Metadatos del Documento:** (Versión, Autor, Estado) \- Crucial para el control de versiones en Git y la trazabilidad.  
2. **Declaración del Problema (El "Por Qué"):** Derivado del enfoque PR/FAQ de Amazon, centrándose obsesivamente en el punto de dolor del cliente antes de proponer soluciones.28  
3. **Personas Usuarias:** Perfiles detallados que sirven como "actores" en las historias de usuario.26  
4. **Requisitos Funcionales:** Declaraciones atómicas y comprobables.  
5. **Restricciones Técnicas:** Límites explícitos (e.g., "Debe ejecutarse en AWS Lambda", "Latencia máxima de 100ms").  
6. **Historias de Usuario:** Estructuradas en formato Como \<rol\>, quiero \<función\>, para que \<beneficio\>, con Criterios de Aceptación (AC) específicos y verificables.  
7. **Métricas de Éxito:** KPIs cuantificables que definen qué constituye un lanzamiento exitoso.29

### **3.2 Arquitectura del Prompt Generador (Slot-Filling)**

La generación del PRD se orquesta a través de un sistema de prompt de **"Slot-Filling"** (Llenado de Ranuras).30 Este prompt actúa como una máquina de estados, guiando al usuario (o al agente que llama) a través de la recopilación de la información necesaria antes de intentar redactar el documento.

Mecanismo de Slot-Filling:  
El sistema mantiene un "Mapa de Ranuras" basado en JSON:

JSON

{  
 "Product Overview": { "Title": "", "Summary": "" },  
 "Goals": { "Business": "", "User": "" },  
 "User Personas": { "Key Types": "", "Roles": "" },  
 "Technical Constraints": { "Stack": "", "Compliance": "" }  
}

El agente itera a través de estas ranuras, haciendo preguntas dirigidas al usuario. Este **"Modo Interrogativo"** previene la generación de requisitos genéricos o alucinados, un problema común en los prompts de un solo paso.31 Solo cuando las ranuras están suficientemente pobladas, el agente procede a la fase de "Redacción", donde interpola los datos en la plantilla Markdown utilizando las técnicas de CoT y CoD descritas anteriormente.

### **3.3 Evitando Trampas Comunes mediante Restricciones Negativas**

La investigación destaca que los requisitos vagos ("La aplicación debe ser rápida") son una causa principal del fracaso de los proyectos de software.29 El marco PROMPTS\_V2 utiliza **Prompting de Restricciones Negativas** para prohibir estrictamente tal ambigüedad.

**Instrucción del System Prompt (Restricción Negativa):**

"NO DEBES usar adjetivos vagos como 'rápido', 'fácil', 'intuitivo' o 'moderno' en los Requisitos Funcionales. DEBES reemplazarlos con métricas cuantificables (e.g., 'Carga de página \< 200ms', 'Máximo 3 clics para finalizar compra'). Si una métrica es desconocida, usa '' en lugar de un término vago."

Esta aplicación estricta asegura que el PRD resultante sea procesable y comprobable, alineándose con el ethos de "Spec-Driven Development" donde las especificaciones describen la intención en un lenguaje estructurado y comprobable.7

## **4\. Ingeniería de la Solicitud de Comentarios (RFC)**

Mientras que los PRDs definen *qué* construir, los RFCs definen *cómo* construirlo. El proceso de RFC es central para la cultura de ingeniería en organizaciones de alto rendimiento como Google 32, Uber 33 y el IETF.34 PROMPTS\_V2 trata la generación de RFCs no como una tarea de redacción, sino como un ejercicio técnico riguroso, aprovechando la estructura de los estándares de Internet y la claridad en la toma de decisiones de los RFCs de Rust.

### **4.1 La Influencia del IETF: Cumplimiento de RFC 2119**

Una característica definitoria de las especificaciones técnicas profesionales es el uso preciso de los niveles de requerimiento. El marco PROMPTS\_V2 integra el estándar **RFC 2119** 35 como una restricción lingüística central en sus prompts.

**Palabras Clave RFC 2119 y su Interpretación:**

* **MUST / REQUIRED (DEBE):** Requisito absoluto.  
* **MUST NOT (NO DEBE):** Prohibición absoluta.  
* **SHOULD / RECOMMENDED (DEBERÍA):** Pueden existir razones válidas para ignorarlo, pero las implicaciones deben entenderse y sopesarse.  
* **MAY / OPTIONAL (PUEDE):** Verdaderamente opcional.

Estrategia de Prompting:  
El prompt del sistema para el agente "Redactor de RFC" incluye una instrucción obligatoria:  
"Todos los requisitos normativos DEBEN utilizar palabras clave RFC 2119 en mayúsculas. Tienes prohibido usar lenguaje débil como 'usualmente hará' o 'a veces puede' al definir el comportamiento del protocolo o los contratos de API."

Esto obliga al LLM a comprometerse con decisiones arquitectónicas. En lugar de escribir "La API probablemente debería devolver un 404", el modelo escribe "La API DEBE devolver 404 si falta el recurso". Esta precisión reduce la ambigüedad durante la fase de implementación y permite la generación automatizada de casos de prueba basados en palabras clave.37

### **4.2 Adaptación de la Plantilla RFC de Rust**

El proceso de RFC del lenguaje de programación Rust es ampliamente considerado como un estándar de oro para la toma de decisiones en código abierto.38 Enfatiza secciones críticas como "Motivación", "Diseño Detallado" y, crucialmente, "Inconvenientes" (Drawbacks) y "Alternativas".

**Estructura Markdown RFC de PROMPTS\_V2:**

# **RFC:**

## **Resumen**

Explicación de un párrafo de la característica.

## **Motivación**

¿Por qué hacemos esto? ¿Qué problemas resuelve?

## **Diseño Detallado**

Especificación técnica, firmas de API, modelos de datos.  
Uso obligatorio de palabras clave RFC 2119\.

## **Inconvenientes (Drawbacks)**

¿Por qué NO deberíamos hacer esto?

## **Alternativas**

¿Qué otros diseños se consideraron y por qué fueron rechazados?

## **Preguntas No Resueltas**

¿Qué se desconoce todavía?

La inclusión de "Inconvenientes" y "Alternativas" se impone a través de **Meta-Prompting**. Si el modelo genera un RFC sin una sección sustancial de Inconvenientes, el "Agente Revisor" activa un rechazo, instando al generador a "Analizar críticamente el diseño propuesto en busca de cuellos de botella de rendimiento, riesgos de seguridad o costos de complejidad".

### **4.3 Elementos de Design Doc de Google**

De la cultura de ingeniería de Google, PROMPTS\_V2 toma prestados los conceptos de **"Contexto y Alcance"** y **"Arquitectura del Sistema"**.32

* **Contexto:** Define claramente lo que está *fuera del alcance* para prevenir el "scope creep".  
* **Arquitectura Visual:** Requiere la inclusión de diagramas **MermaidJS** para visualizar el flujo de datos.

Integración de MermaidJS:  
El marco solicita explícitamente al modelo:  
"Genera un diagrama de secuencia MermaidJS que ilustre el flujo de datos entre \[Componente A\] y. Asegúrate de que todas las llamadas síncronas y asíncronas estén correctamente etiquetadas."

Este componente visual permite que el RFC sirva como un mapa de alto nivel del sistema, crucial para revisar sistemas distribuidos complejos.

## **5\. La Capa de Validación: Meta-Prompts y Revisión Automatizada**

Una innovación clave en PROMPTS\_V2 es la introducción de una **Capa de Validación** autónoma. En un flujo de trabajo manual, un humano revisa el PRD/RFC. En un flujo de Flow Engineering, un "Agente Revisor" especializado realiza una evaluación heurística *antes* de que el humano vea siquiera el borrador. Esto filtra errores obvios y eleva la calidad base del documento presentado.

### **5.1 La Persona del Agente "Crítico"**

El Agente Crítico se inicializa con un prompt de sistema diseñado para ser escéptico, pedante y riguroso.40 Se le instruye explícitamente para *no* generar contenido, sino para encontrar fallos en él.

**System Prompt para el Crítico (Extracto):**

"Eres un Arquitecto de Software Principal y Experto en Seguridad. Tu objetivo es encontrar fallos, ambigüedades y riesgos de seguridad en la especificación proporcionada. No reescribas el documento.  
Criterios de Revisión:

1. **Ambigüedad:** ¿Hay requisitos vagos? (e.g., 'manejar errores con gracia').  
2. **Completitud:** ¿Se abordan los casos extremos (e.g., fallo de red, entrada inválida)?  
3. **Cumplimiento RFC 2119:** ¿Se usan correctamente las palabras clave?  
4. Seguridad: ¿Están explícitamente definidos la autenticación y la autorización?  
   Salida: Una lista estructurada de problemas bloqueantes."

### **5.2 Bucles de Autorreflexión y Refinamiento**

La retroalimentación del Agente Crítico se alimenta de nuevo al Agente Redactor en un **Bucle de Refinamiento**.42

**El Bucle de Reflexión:**

1. **Borrador:** El Redactor genera la V1.  
2. **Crítica:** El Crítico genera una lista de 5 problemas de integridad.  
3. **Refinamiento:** Se instruye al Redactor: "Aquí tienes retroalimentación sobre tu borrador. Actualiza el documento para resolver estos 5 problemas específicos. Genera la V2."

Este "Patrón de Reflexión" ha demostrado mejorar significativamente la calidad de las salidas de los LLM.40 Al separar la generación de la evaluación, el sistema aprovecha la capacidad del modelo para reconocer errores que podría no haber evitado durante la generación inicial "ciega".

### **5.3 Evaluación Heurística**

El Agente Crítico emplea heurísticas estándar de usabilidad e ingeniería.44 Para PRDs centrados en UI, verifica contra las Heurísticas de Nielsen (e.g., "Visibilidad del estado del sistema"). Para RFCs de Backend, verifica contra las falacias de los sistemas distribuidos (e.g., "La red es fiable").

Meta-Prompting para Validación:  
El meta-prompting implica pedirle al modelo que genere los criterios para su propia evaluación.46  
"Antes de revisar el documento, genera una lista de verificación de 10 criterios de validación específicos para un. Luego, utiliza esta lista para revisar rigurosamente la especificación adjunta."

Esta generación dinámica de criterios asegura que la validación esté adaptada al contexto específico del proyecto (e.g., una "App Bancaria" recibe un escrutinio de seguridad mucho mayor que una "Herramienta Interna").

## **6\. Implementación de PROMPTS\_V2.md: Estrategia y Despliegue**

El archivo PROMPTS\_V2.md es el artefacto central que aloja los prompts del sistema, las plantillas y las definiciones de flujo. Sirve como el archivo de configuración para el sistema de Flow Engineering.

### **6.1 Prompts de Sistema Modulares**

El archivo está organizado en secciones modulares, cada una definiendo un rol de agente específico. Esta modularidad permite actualizaciones fáciles y especialización.

**Secciones Clave:**

* @agent\_planner: Instrucciones para el desglose inicial de la consulta del usuario utilizando Plan-and-Solve.  
* @agent\_drafter\_prd: El prompt de Slot-Filling para la generación de PRD.30  
* @agent\_drafter\_rfc: El prompt compatible con RFC 2119 para especificaciones técnicas.  
* @agent\_reviewer: El prompt de Crítico basado en persona.40  
* @template\_prd: La plantilla Markdown raw para PRDs (Estilo Uber/Amazon).  
* @template\_rfc: La plantilla Markdown raw para RFCs (Estilo Rust/IETF).

### **6.2 Estrategia de Ingeniería de Contexto**

El prompting efectivo requiere gestionar la ventana de contexto con higiene estricta. PROMPTS\_V2 impone un protocolo de **"Higiene de Contexto"**.47

* **Limpieza de Entrada:** Instrucciones para eliminar el "fluff" conversacional irrelevante de las entradas del usuario antes del procesamiento.  
* **Inyección de Referencia:** Mecanismos para inyectar documentación externa (e.g., documentos de API, esquemas existentes) en la ventana de contexto solo cuando son relevantes para la sección actual.  
* **Gestión de Memoria:** Resumen de turnos anteriores para mantener la coherencia a largo plazo sin desbordar el límite de tokens.

### **6.3 Meta-Prompt para Actualizaciones**

El marco incluye un meta-prompt diseñado para actualizarse a sí mismo.

"Analiza el rendimiento actual de los agentes. Si el Revisor encuentra consistentemente el mismo tipo de error (e.g., falta de manejo de errores), genera un Prompt de Sistema actualizado para el Redactor que prevenga explícitamente este error en el futuro."

Esto permite que la biblioteca de prompts evolucione basándose en los patrones de uso reales y los modos de fallo encontrados durante la operación.

## **7\. Estrategia de Implementación: Desplegando PROMPTS\_V2 en Frameworks Agénticos**

La transición de una colección de archivos de texto a un flujo de trabajo de Flow Engineering requiere un despliegue estratégico sobre frameworks de orquestación modernos. Aunque PROMPTS\_V2.md puede usarse manualmente, su verdadero potencial se desbloquea al integrarse con arquitecturas de grafos.

### **7.1 Integración con Frameworks Agénticos (LangGraph, CrewAI, AutoGen)**

Los prompts definidos no son estáticos; son nodos en un grafo de estado.

* **LangGraph:** Se utiliza para definir el flujo de control explícito. Los nodos representan a los Agentes (Redactor, Revisor) y las aristas representan la lógica de flujo condicional (e.g., "Si la Revisión falla, volver a Redactor"; "Si la Revisión pasa, ir a Finalizar").48 Esto permite persistencia de estado y bucles de reintento.  
* **CrewAI:** Se definen el "Planificador", "Escritor" y "Revisor" como agentes distintos dentro de un Crew. Se asignan los prompts de sistema específicos de PROMPTS\_V2.md a cada rol, permitiendo la colaboración autónoma.49  
* **AutoGen:** Habilita patrones de conversación multi-agente donde el "Usuario Proxy" puede ser un humano o una herramienta de validación automatizada que interactúa con el "Asistente" para refinar el documento.50

### **7.2 El Protocolo "Human-in-the-Loop"**

A pesar de la automatización, la supervisión humana sigue siendo crítica para la validación semántica de alto nivel. El flujo está diseñado para pausar en transiciones de estado críticas:

* **Aprobación del Plan:** Antes de que comience la redacción, el usuario aprueba el "Esqueleto" o "Plan".  
* **Revisión de la Crítica:** El usuario ve los problemas detectados por el Crítico y puede anularlos si son falsos positivos.  
* **Aprobación Final:** El usuario acepta el artefacto final antes de que se guarde en el repositorio o se pase a los agentes de codificación.

### **7.3 Conclusión y Perspectivas Futuras**

El marco PROMPTS\_V2 representa una maduración de la IA generativa en la ingeniería de software. Al ir más allá de las interacciones de chat simples y abrazar los principios de **Flow Engineering**, desarrollo **Spec-First** y validación automatizada rigurosa, los equipos técnicos pueden aprovechar los modelos SOTA 2025 para generar artefactos que no son solo plausibles, sino precisos, robustos y listos para la implementación. La convergencia del razonamiento de Cadena de Pensamiento, las restricciones estándar de la industria (RFC 2119\) y los flujos de trabajo agénticos crea un sistema donde la IA actúa menos como un chatbot y más como un Ingeniero de Staff disciplinado y metódico.

---

## **8\. Especificaciones de Referencia Detalladas**

Las siguientes subsecciones detallan las estructuras de plantilla y la lógica de prompt específicas referenciadas en el marco, listas para ser incorporadas en PROMPTS\_V2.md.

### **8.1 Estructura de Plantilla PRD en Markdown (Raw)**

Esta estructura está optimizada para ser analizada por agentes de codificación y mantiene una jerarquía estricta.

# **PRD: {Título del Proyecto}**

## **1\. Visión General del Producto**

### **1.1 Metadatos del Documento**

* **Versión:** 1.0  
* **Estado:** Borrador/Aprobado  
* **Propietario:** {Nombre}

### **1.2 Resumen Ejecutivo**

(Generado vía Chain-of-Density)

## **2\. Contexto Estratégico**

### **2.1 Declaración del Problema**

(Estilo "Working Backwards" de Amazon)  
\[¿Quién es el cliente? ¿Cuál es el problema? ¿Por qué ahora?\]

### **2.2 Objetivos**

* **Objetivos de Negocio:** \[Impulsados por métricas\]  
* **Objetivos del Usuario:** \[Impulsados por la experiencia\]  
* **No-Objetivos:** \[Explícitamente fuera del alcance\]

## **3\. Personas Usuarias**

* **\[Persona A\]:**  
* **:**

## **4\. Requisitos Funcionales**

(DEBE usar restricciones negativas para evitar ambigüedad)

* **RF-001:** \[Nombre de la Característica\] \-  
  * Prioridad: P0  
  * Dependencias: \[Lista\]  
  * Criterios de Aceptación:  
    * \[ \] Criterio 1  
    * \[ \] Criterio 2

## **5\. Experiencia de Usuario**

### **5.1 Flujos de Usuario**

### **5.2 Requisitos de UI**

## **6\. Especificaciones Técnicas**

### **6.1 Requisitos de API**

### **6.2 Modelos de Datos**

### **6.3 Seguridad y Cumplimiento**

## **7\. Métricas de Éxito**

* **Métrica 1:**  
* **Métrica 2:**

### **8.2 Estructura de Plantilla RFC en Markdown (Raw)**

Esta estructura impone rigor arquitectónico y toma de decisiones explícita.

# **RFC: {Título}**

* **Nombre de la Característica:** {nombre}  
* **Fecha de Inicio:** {fecha}  
* **PR del RFC:** {enlace}  
* **Issue:** {enlace}

## **Resumen**

Explicación de un párrafo de la característica.

## **Motivación**

¿Por qué estamos haciendo esto? ¿Qué resultado se espera?

## **Explicación a Nivel de Guía**

¿Cómo enseñamos esto a los usuarios/desarrolladores?

## **Explicación a Nivel de Referencia**

Detalles técnicos, casos extremos, algoritmos.  
(DEBE usar palabras clave RFC 2119: MUST, SHOULD, MAY)

## **Inconvenientes (Drawbacks)**

¿Por qué NO deberíamos hacer esto?

## **Racional y Alternativas**

¿Por qué es este el mejor diseño? ¿Qué alternativas se descartaron y por qué?

## **Arte Previo**

¿Cómo resuelven esto otros sistemas?

## **Preguntas No Resueltas**

¿Qué necesita decidirse antes de fusionar?

### **8.3 Prompt de Sistema "Spec-First" (Extracto)**

ROL: Arquitecto Técnico Principal y Gerente de Producto.

OBJETIVO: Facilitar la creación de un Artefacto Técnico riguroso (PRD o RFC) a través de un flujo estructurado e iterativo.

PROTOCOLOS NUCLEARES:

1. **Llenado de Ranuras (Slot-Filling):** NO generes el documento inmediatamente. Consulta al usuario para llenar las ranuras de conocimiento requeridas (Objetivos, Personas, Restricciones) antes de escribir.  
2. **Cumplimiento de Restricciones:**  
   * PRDs: Prohibir lenguaje vago ("rápido", "moderno"). Requerir métricas numéricas.  
   * RFCs: Imponer palabras clave RFC 2119 (MUST, SHOULD) para requisitos normativos.  
3. **Pensamiento Visual:** Proponer siempre un diagrama MermaidJS para flujos arquitectónicos.  
4. **Chain-of-Thought:** Antes de generar cualquier sección, declara explícitamente los pasos de razonamiento en un bloque .

FORMATO DE SALIDA: Markdown estricto. Sin relleno conversacional en el artefacto final.

---

Referencias:

1

#### **Fuentes citadas**

1. SLD-Spec: Enhancement LLM-assisted Specification Generation for Complex Loop Functions via Program Slicing and Logical Deletion \- arXiv, acceso: noviembre 28, 2025, [https://arxiv.org/html/2509.09917](https://arxiv.org/html/2509.09917)  
2. Spec-First vs. Code-First in AI Development: Which Should You Choose? \- Kinde, acceso: noviembre 28, 2025, [https://kinde.com/learn/ai-for-software-engineering/best-practice/spec-first-vs-code-first-in-ai-development/](https://kinde.com/learn/ai-for-software-engineering/best-practice/spec-first-vs-code-first-in-ai-development/)  
3. Spec-First Development: The Missing Manual for Building with AI \- Clever Thinking Software, acceso: noviembre 28, 2025, [https://www.cleverthinkingsoftware.com/spec-first-development-the-missing-manual-for-building-with-ai/](https://www.cleverthinkingsoftware.com/spec-first-development-the-missing-manual-for-building-with-ai/)  
4. Flow Engineering is All You Need \- Medium, acceso: noviembre 28, 2025, [https://medium.com/@rohanbalkondekar/flow-engineering-is-all-you-need-9046a5e7351d](https://medium.com/@rohanbalkondekar/flow-engineering-is-all-you-need-9046a5e7351d)  
5. What is flow engineering? A detailed guide \- LeewayHertz, acceso: noviembre 28, 2025, [https://www.leewayhertz.com/flow-engineering/](https://www.leewayhertz.com/flow-engineering/)  
6. Unlocking the Potential of AI-Powered Tools with Flow Engineering and Prompt Engineering \- Ctrl Man, acceso: noviembre 28, 2025, [https://ctrlman.dev/blog/flow-engineering-vs-prompt-engineering/](https://ctrlman.dev/blog/flow-engineering-vs-prompt-engineering/)  
7. Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl \- Martin Fowler, acceso: noviembre 28, 2025, [https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)  
8. Better Summarization with Chain of Density Prompting \- PromptHub, acceso: noviembre 28, 2025, [https://www.prompthub.us/blog/better-summarization-with-chain-of-density-prompting](https://www.prompthub.us/blog/better-summarization-with-chain-of-density-prompting)  
9. What is the Chain of Density in Prompt Engineering? \- Analytics Vidhya, acceso: noviembre 28, 2025, [https://www.analyticsvidhya.com/blog/2024/07/chain-of-density-in-prompt-engineering/](https://www.analyticsvidhya.com/blog/2024/07/chain-of-density-in-prompt-engineering/)  
10. The Prompt Report Part 2: Plan and Solve, Tree of Thought, and Decomposition Prompting, acceso: noviembre 28, 2025, [https://ghost.oxen.ai/the-prompt-report-part-2-thought-generation-tree-of-thought-and-decomposition-prompting/](https://ghost.oxen.ai/the-prompt-report-part-2-thought-generation-tree-of-thought-and-decomposition-prompting/)  
11. Plan-and-Solve Prompting: Improving Reasoning and Reducing Errors, acceso: noviembre 28, 2025, [https://learnprompting.org/docs/advanced/decomposition/plan\_and\_solve](https://learnprompting.org/docs/advanced/decomposition/plan_and_solve)  
12. r/ClineProjects \- Reddit, acceso: noviembre 28, 2025, [https://www.reddit.com/r/ClineProjects/](https://www.reddit.com/r/ClineProjects/)  
13. Resources / Best Practices for Using PRDs with Cursor \- ChatPRD, acceso: noviembre 28, 2025, [https://www.chatprd.ai/resources/PRD-for-Cursor](https://www.chatprd.ai/resources/PRD-for-Cursor)  
14. String diagrams for text, acceso: noviembre 28, 2025, [http://www.cs.ox.ac.uk/people/aleks.kissinger/theses/wang-thesis.pdf](http://www.cs.ox.ac.uk/people/aleks.kissinger/theses/wang-thesis.pdf)  
15. Chain-of-Thought Prompting | Prompt Engineering Guide, acceso: noviembre 28, 2025, [https://www.promptingguide.ai/techniques/cot](https://www.promptingguide.ai/techniques/cot)  
16. What is chain of thought (CoT) prompting? \- IBM, acceso: noviembre 28, 2025, [https://www.ibm.com/think/topics/chain-of-thoughts](https://www.ibm.com/think/topics/chain-of-thoughts)  
17. Let Claude think (chain of thought prompting) to increase performance, acceso: noviembre 28, 2025, [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-of-thought](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-of-thought)  
18. Build an LLM app using Skeleton-of-Thought | by Scott Regan | Langflow | Medium, acceso: noviembre 28, 2025, [https://medium.com/logspace/build-an-llm-app-using-skeleton-of-thought-6aa7e2e54cd1](https://medium.com/logspace/build-an-llm-app-using-skeleton-of-thought-6aa7e2e54cd1)  
19. Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation \- arXiv, acceso: noviembre 28, 2025, [https://arxiv.org/html/2307.15337v3](https://arxiv.org/html/2307.15337v3)  
20. Skeleton-of-Thought Prompting: Faster and Efficient Response Generation, acceso: noviembre 28, 2025, [https://learnprompting.org/docs/advanced/decomposition/skeleton\_of\_thoughts](https://learnprompting.org/docs/advanced/decomposition/skeleton_of_thoughts)  
21. Skeleton-of-Thought: Parallel decoding speeds up and improves LLM output \- Microsoft, acceso: noviembre 28, 2025, [https://www.microsoft.com/en-us/research/blog/skeleton-of-thought-parallel-decoding-speeds-up-and-improves-llm-output/](https://www.microsoft.com/en-us/research/blog/skeleton-of-thought-parallel-decoding-speeds-up-and-improves-llm-output/)  
22. From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting \- arXiv, acceso: noviembre 28, 2025, [https://arxiv.org/abs/2309.04269](https://arxiv.org/abs/2309.04269)  
23. Chain of Density (CoD) \- Learn Prompting, acceso: noviembre 28, 2025, [https://learnprompting.org/docs/advanced/self\_criticism/chain-of-density](https://learnprompting.org/docs/advanced/self_criticism/chain-of-density)  
24. What Is Plan-and-Solve Prompting? | by Deepak kumar sahoo | The Synaptic Stack, acceso: noviembre 28, 2025, [https://medium.com/the-synaptic-stack/what-is-plan-and-solve-prompting-59293b8b41b1](https://medium.com/the-synaptic-stack/what-is-plan-and-solve-prompting-59293b8b41b1)  
25. Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models \- ACL Anthology, acceso: noviembre 28, 2025, [https://aclanthology.org/2023.acl-long.147.pdf](https://aclanthology.org/2023.acl-long.147.pdf)  
26. Uber's PRD Template \- GrowthX, acceso: noviembre 28, 2025, [https://growthx.club/learn/templates/ubers-prd-template](https://growthx.club/learn/templates/ubers-prd-template)  
27. Working Backwards PR/FAQ Instructions & Template, acceso: noviembre 28, 2025, [https://workingbackwards.com/resources/working-backwards-pr-faq/](https://workingbackwards.com/resources/working-backwards-pr-faq/)  
28. Discover PRFAQ: Amazon's Innovation Blueprint \+Template \- Product School, acceso: noviembre 28, 2025, [https://productschool.com/blog/product-fundamentals/prfaq](https://productschool.com/blog/product-fundamentals/prfaq)  
29. 5 Common PRD Mistakes and How to Fix Them \- Centercode, acceso: noviembre 28, 2025, [https://www.centercode.com/blog/5-common-prd-mistakes-and-how-to-fix-them](https://www.centercode.com/blog/5-common-prd-mistakes-and-how-to-fix-them)  
30. Product requirement document generation using LLM task oriented ..., acceso: noviembre 28, 2025, [https://gist.github.com/Dowwie/151d8efea738ea486ddec9208ddb3a19](https://gist.github.com/Dowwie/151d8efea738ea486ddec9208ddb3a19)  
31. Best one-shot LLM prompts for product managers : r/ProductManagement \- Reddit, acceso: noviembre 28, 2025, [https://www.reddit.com/r/ProductManagement/comments/1i7ct8q/best\_oneshot\_llm\_prompts\_for\_product\_managers/](https://www.reddit.com/r/ProductManagement/comments/1i7ct8q/best_oneshot_llm_prompts_for_product_managers/)  
32. Design Docs at Google \- Industrial Empathy, acceso: noviembre 28, 2025, [https://www.industrialempathy.com/posts/design-docs-at-google/](https://www.industrialempathy.com/posts/design-docs-at-google/)  
33. The Uber Engineering Tech Stack, Part I: The Foundation, acceso: noviembre 28, 2025, [https://www.uber.com/blog/tech-stack-part-one-foundation/](https://www.uber.com/blog/tech-stack-part-one-foundation/)  
34. About RFCs \- IETF, acceso: noviembre 28, 2025, [https://www.ietf.org/process/rfcs/](https://www.ietf.org/process/rfcs/)  
35. RFC 2119 \- Key words for use in RFCs to Indicate Requirement Levels \- IETF Datatracker, acceso: noviembre 28, 2025, [https://datatracker.ietf.org/doc/html/rfc2119](https://datatracker.ietf.org/doc/html/rfc2119)  
36. "Key words for use in RFCs to Indicate Requirement Levels", BCP 14 \- IETF, acceso: noviembre 28, 2025, [https://www.ietf.org/rfc/rfc2119.txt](https://www.ietf.org/rfc/rfc2119.txt)  
37. iPanda: An Intelligent Protocol Testing and Debugging Agent for Conformance Testing \- arXiv, acceso: noviembre 28, 2025, [https://arxiv.org/html/2507.00378v1](https://arxiv.org/html/2507.00378v1)  
38. 1607-style-rfcs \- The Rust RFC Book, acceso: noviembre 28, 2025, [https://rust-lang.github.io/rfcs/1607-style-rfcs.html](https://rust-lang.github.io/rfcs/1607-style-rfcs.html)  
39. Software Design Document Template \- Google Docs, acceso: noviembre 28, 2025, [https://docs.google.com/document/d/1pgMutdDasJb6eN6yK6M95JM8gQ16IKacxxhPXgeL9WY/edit](https://docs.google.com/document/d/1pgMutdDasJb6eN6yK6M95JM8gQ16IKacxxhPXgeL9WY/edit)  
40. Reflection Agent Pattern — Agent Patterns 0.2.0 documentation \- Read the Docs, acceso: noviembre 28, 2025, [https://agent-patterns.readthedocs.io/en/stable/patterns/reflection.html](https://agent-patterns.readthedocs.io/en/stable/patterns/reflection.html)  
41. Agentic Design Patterns Part 2: Reflection \- DeepLearning.AI, acceso: noviembre 28, 2025, [https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)  
42. Self-Refine: Iterative Refinement with Self-Feedback for LLMs \- Learn Prompting, acceso: noviembre 28, 2025, [https://learnprompting.org/docs/advanced/self\_criticism/self\_refine](https://learnprompting.org/docs/advanced/self_criticism/self_refine)  
43. Iterative Refinement with Self-Feedback \- OpenReview, acceso: noviembre 28, 2025, [https://openreview.net/pdf?id=S37hOerQLB](https://openreview.net/pdf?id=S37hOerQLB)  
44. Heuristic evaluation \- Wikipedia, acceso: noviembre 28, 2025, [https://en.wikipedia.org/wiki/Heuristic\_evaluation](https://en.wikipedia.org/wiki/Heuristic_evaluation)  
45. Heuristic Evaluation | Usability Body of Knowledge, acceso: noviembre 28, 2025, [https://www.usabilitybok.org/heuristic-evaluation](https://www.usabilitybok.org/heuristic-evaluation)  
46. GPT-5 prompting guide | OpenAI Cookbook, acceso: noviembre 28, 2025, [https://cookbook.openai.com/examples/gpt-5/gpt-5\_prompting\_guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide)  
47. Context Engineering 101: The Hidden Skill Behind Smarter AI | by Generative AI \- Medium, acceso: noviembre 28, 2025, [https://medium.com/@genai.works/context-engineering-101-the-hidden-skill-behind-smarter-ai-c145ba04136d](https://medium.com/@genai.works/context-engineering-101-the-hidden-skill-behind-smarter-ai-c145ba04136d)  
48. Smart Document Automation with LangGraph and Streamlit: From Template to E-Signature | by Vishal | Medium, acceso: noviembre 28, 2025, [https://medium.com/@vishal025/smart-document-automation-with-langgraph-and-streamlit-from-template-to-e-signature-5d76d8802553](https://medium.com/@vishal025/smart-document-automation-with-langgraph-and-streamlit-from-template-to-e-signature-5d76d8802553)  
49. CrewAI Blog Automation: Building a Multi-Agent Content Creation System with Python, acceso: noviembre 28, 2025, [https://christianmendieta.ca/crewai-blog-automation-building-a-multi-agent-content-creation-system-with-python/](https://christianmendieta.ca/crewai-blog-automation-building-a-multi-agent-content-creation-system-with-python/)  
50. How to Build an Autonomous AI Agent Workflow (with LangGraph or Autogen) | by Its Aman Yadav | Nov, 2025, acceso: noviembre 28, 2025, [https://medium.com/@itsamanyadav/how-to-build-an-autonomous-ai-agent-workflow-with-langgraph-or-autogen-c84cc95bc2eb](https://medium.com/@itsamanyadav/how-to-build-an-autonomous-ai-agent-workflow-with-langgraph-or-autogen-c84cc95bc2eb)  
51. Multi-agent Conversation Framework | AutoGen 0.2, acceso: noviembre 28, 2025, [https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent\_chat/](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)  
52. The AI shift from prompt engineering to flow engineering \- Techzine Global, acceso: noviembre 28, 2025, [https://www.techzine.eu/blogs/applications/118176/the-ai-shift-from-prompt-engineering-to-flow-engineering/](https://www.techzine.eu/blogs/applications/118176/the-ai-shift-from-prompt-engineering-to-flow-engineering/)  
53. Why Hybrid “Spec-First, Sprint-Later” Works Best for LLM Code Assistants \- Medium, acceso: noviembre 28, 2025, [https://medium.com/@jcampbell38/why-hybrid-spec-first-sprint-later-works-best-for-llm-code-assistants-52c32848e230](https://medium.com/@jcampbell38/why-hybrid-spec-first-sprint-later-works-best-for-llm-code-assistants-52c32848e230)  
54. Meta Prompting for AI Systems \- arXiv, acceso: noviembre 28, 2025, [https://arxiv.org/html/2311.11482v6](https://arxiv.org/html/2311.11482v6)  
55. A Complete Guide to Meta Prompting \- PromptHub, acceso: noviembre 28, 2025, [https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting](https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting)  
56. Workflows and agents \- Docs by LangChain, acceso: noviembre 28, 2025, [https://docs.langchain.com/oss/python/langgraph/workflows-agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)  
57. Healing Agent \- Prompts \- UiPath Documentation, acceso: noviembre 28, 2025, [https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-prompts](https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-prompts)
