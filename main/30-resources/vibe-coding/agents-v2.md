---
type: resource
status: active
area: "[[Personal]]"
created: 2026-07-08
updated: 2026-08-08
aliases:
  - agents-v2
  - AGENTS_V2
tags:
  - resource
  - vibe-coding
  - pilar
---

# **AGENTS_V2.md: Manual de Operaciones de Agentes para Flujos de Trabajo Autónomos Escalables**

## **Resumen Ejecutivo: La Nueva Era de la Orquestación Agéntica**

La ingeniería de software se encuentra en un punto de inflexión crítico. La transición de modelos de lenguaje grandes (LLM) aislados a ecosistemas de **agentes autónomos multi-rol** representa un cambio de paradigma tan fundamental como la adopción de DevOps o la arquitectura de microservicios. En este nuevo contexto, el rol del desarrollador humano evoluciona hacia el de un "arquitecto de orquestación", responsable de diseñar los sistemas cognitivos y los protocolos de interacción que permiten a una fuerza laboral digital operar con autonomía, precisión y resiliencia.

Este documento, titulado formalmente **AGENTS\_V2.md**, constituye el manual definitivo de operaciones para esta nueva fuerza laboral sintética. Unifica los roles operativos críticos—Product Manager, Arquitecto de Software, Desarrollador e Ingeniero de QA—bajo un estándar riguroso de entradas y salidas (Inputs/Outputs), establece un protocolo de transferencia de estado basado en sistemas de archivos inmutables (**File-Based Hand-off**), e introduce mecanismos robustos de tolerancia a fallos conocidos como el protocolo de "Devolver el Ticket" (**Return the Ticket**).

El análisis exhaustivo de la literatura actual y las prácticas emergentes en 2025 revela que la dependencia de un único modelo generalista para la generación de software de extremo a extremo es insostenible para sistemas complejos. La "deriva de contexto" (*context drift*), las alucinaciones arquitectónicas y la falta de coherencia lógica son síntomas endémicos de flujos de trabajo no estructurados.1 Por el contrario, la descomposición del ciclo de vida de desarrollo de software (SDLC) en roles especializados, donde cada agente opera dentro de un perfil cognitivo delimitado y validado, permite mitigar estos riesgos mediante la especialización funcional y la verificación adversarial.1

Este manual integra el flujo de trabajo de codificación de 4 agentes proporcionado por el usuario con las mejores prácticas de la industria en persistencia de archivos, salidas estructuradas y manejo de excepciones. Está diseñado no solo como una guía de referencia humana, sino como un "meta-prompt" o constitución operativa que puede ser ingerida por los propios agentes, alineando su comportamiento con la intención humana y garantizando que el ciclo autónomo permanezca fundamentado en la realidad técnica.

---

## **1\. Fundamentos Arquitectónicos: Del Chat al Sistema de Archivos**

La primera y más crítica evolución en el paso de los flujos de trabajo "V1" a "V2" es el abandono del historial de chat efímero como medio principal de gestión de estado. En los sistemas de primera generación, el contexto se mantenía en una ventana de conversación creciente, lo que inevitablemente llevaba a la pérdida de información crítica y al aumento de costos computacionales. El estándar **AGENTS\_V2** establece la supremacía del sistema de archivos como la única fuente de verdad (*Single Source of Truth*).

### **1.1 El Paradigma de la Persistencia Basada en Artefactos**

La volatilidad de la memoria de corto plazo de los LLMs exige un mecanismo de persistencia externo que sea robusto, verificable y agnóstico al modelo. Al adoptar un enfoque centrado en artefactos, transformamos el flujo de trabajo de una serie de conversaciones efímeras a una línea de montaje de manufactura digital, donde cada etapa produce bienes tangibles e inmutables.

El análisis de patrones de diseño para orquestación de agentes sugiere que tratar la memoria como un subsistema de primera clase es esencial para la estabilidad operativa.3 En este modelo, los agentes no "recuerdan" lo que dijeron hace diez turnos; en su lugar, leen el estado actual del proyecto directamente de los archivos generados. Esto permite una **auditoría forense** completa: en cualquier punto del proceso, un humano o un sistema de supervisión puede inspeccionar el estado exacto del producto (PRD), el diseño (RFC) o la implementación (Código), sin tener que analizar gigabytes de logs conversacionales no estructurados.4

Además, este enfoque desacopla a los agentes entre sí. El Agente Desarrollador no necesita saber "quién" es el Agente Arquitecto ni "cómo" llegó a sus conclusiones; solo necesita consumir el artefacto RFC validado. Esto habilita una escalabilidad horizontal donde múltiples agentes desarrolladores podrían trabajar en paralelo sobre diferentes módulos definidos en un único RFC, coordinados únicamente por la estructura del sistema de archivos y los protocolos de bloqueo de recursos.

### **1.2 Estructura de Directorios Canónica**

Para operacionalizar este paradigma, **AGENTS\_V2.md** impone una taxonomía de directorios estricta. Esta estructura no es una sugerencia; es una restricción operativa que los agentes deben respetar para garantizar la interoperabilidad. La organización del espacio de trabajo refleja el flujo secuencial de datos y la segregación de responsabilidades.

| Directorio | Propósito | Agente Propietario (Escritura) | Agentes Consumidores (Lectura) | Artefactos Clave |
| :---- | :---- | :---- | :---- | :---- |
| 00\_input/ | Punto de entrada de la intención del usuario. | Usuario Humano / Orquestador | Product Manager | user\_prompt.md, context\_files/ |
| 01\_product/ | Definición del problema y requisitos. | Product Manager | Arquitecto, QA | PRD.md, PRD.json, user\_stories/ |
| 02\_architecture/ | Solución técnica y diseño. | Arquitecto | Desarrollador, QA | RFC.md, file\_tree.json, api\_spec.yaml |
| 03\_src/ | Implementación del código fuente. | Desarrollador | QA | Código fuente, requirements.txt, Dockerfile |
| 04\_quality/ | Validación y aseguramiento. | QA | Desarrollador, Arquitecto | test\_suite/, validation\_report.json, coverage/ |
| 05\_logs/ | Trazabilidad y depuración. | Sistema / Todos | Sistema | audit\_trail.log, error\_traces/ |
| .handoff/ | Mecanismo de control de flujo. | Todos | Orquestador | manifest.json, lock\_files |

Esta estructura jerárquica facilita la navegación autónoma. Los estudios sobre ingeniería de contexto eficaz demuestran que los agentes rinden mejor cuando pueden inferir el propósito de un archivo basándose en su ubicación y convención de nombres.5 Por ejemplo, la presencia de un archivo auth\_spec.json en 02\_architecture indica claramente una especificación de diseño, mientras que el mismo nombre en 03\_src implicaría un archivo de código fuente, reduciendo la ambigüedad semántica para el modelo.

### **1.3 El Manifiesto de Transferencia (The Handoff Manifest)**

El mero acto de escribir un archivo no constituye una transferencia de responsabilidad. Para formalizar el paso de un agente a otro, introducimos el concepto de **Manifiesto de Transferencia**. Este es un archivo JSON estandarizado que actúa como un contrato de entrega, certificando que el agente emisor ha completado su tarea y que los artefactos generados cumplen con los criterios de integridad básicos.4

El manifiesto resuelve el problema de la coordinación asíncrona. En lugar de tener un "Supervisor" omnisciente monitoreando cada token generado, el sistema opera bajo un modelo basado en eventos. La aparición de un manifest.json válido en el directorio .handoff/ dispara la siguiente etapa del pipeline. Este patrón, inspirado en arquitecturas orientadas a eventos, permite una orquestación más limpia y resiliente.6

El esquema del manifiesto debe incluir metadatos críticos para la trazabilidad y el contexto:

JSON

{  
  "handoff\_id": "UUID-V4",  
  "timestamp": "ISO-8601",  
  "source\_agent": "Product\_Manager",  
  "target\_agent": "Architect",  
  "status": "COMPLETED",  
  "artifacts":,  
  "context\_summary": "El usuario priorizó la velocidad de desarrollo sobre la escalabilidad masiva. Se descartaron características de gamificación compleja.",  
  "version": "2.1"  
}

El campo context\_summary es vital. Permite transmitir "meta-conocimiento" o la "vibra" del proyecto sin obligar al siguiente agente a leer todo el historial de conversación anterior, optimizando el uso de la ventana de contexto y manteniendo la coherencia de la visión del producto a lo largo de la cadena.4

---

## **2\. Unificación de Roles: Perfiles Cognitivos y Contratos de Interfaz**

La eficacia de un flujo de trabajo multi-agente depende de la claridad con la que se definan los límites de cada rol. La superposición de responsabilidades (por ejemplo, un Desarrollador que toma decisiones de producto) conduce a incoherencias y "deuda técnica alucinada". El manual **AGENTS\_V2.md** define cuatro perfiles cognitivos distintos, cada uno con un modo de razonamiento especializado y contratos de entrada/salida inmutables.

### **2.1 Agente 1: El Product Manager (PM) \- El Reductor de Entropía**

El rol del Product Manager Técnico no es simplemente "escribir requisitos"; es actuar como una máquina de reducción de entropía. Los usuarios humanos a menudo proporcionan entradas vagas, contradictorias o incompletas. El PM debe emplear un razonamiento empático y exploratorio para cristalizar estas intenciones nebulosas en especificaciones deterministas.

* **Perfil Cognitivo:** Empático, Interrogativo, Orientado a Estructura. Debe operar en un modo de "Pensamiento Sistema 2", deliberativo y analítico, para evitar suposiciones prematuras.1  
* **Directiva Principal:** "No asumas. Clarifica hasta que el camino sea determinista."  
* **Modo Operativo:** Iteración de preguntas y respuestas (Bucle Mayéutico) seguido de síntesis estructurada.

**Contrato de Entrada (Inputs):**

* user\_prompt (Texto natural): La solicitud inicial.  
* context\_files (Opcional): Documentos de referencia, guías de marca, o datos históricos.

Contrato de Salida (Outputs):  
El PM debe generar dos versiones del Documento de Requisitos del Producto (PRD).

1. **PRD Narrativo (PRD.md):** Optimizado para lectura humana y contexto semántico. Incluye la visión, objetivos de negocio y narrativas de usuario.  
2. **PRD Estructurado (PRD.json):** Optimizado para el consumo por el Agente Arquitecto. Utiliza un esquema JSON estricto para garantizar que no falten secciones críticas como los Criterios de Aceptación.

Esquema de Salida Estructurada (PRD):  
La investigación subraya la importancia de las salidas estructuradas para evitar errores de análisis en etapas posteriores.7 El esquema JSON del PRD actúa como una "interfaz de tipo" para el proceso de desarrollo.

| Campo | Descripción | Restricción de Validación |
| :---- | :---- | :---- |
| project\_name | Identificador único del proyecto. | snake\_case, máx 50 caracteres. |
| user\_stories | Lista de funcionalidades desde la perspectiva del usuario. | Formato: "Como \[rol\], quiero \[acción\], para \[beneficio\]". |
| acceptance\_criteria | Condiciones binarias para considerar la tarea completa. | Debe ser verificable (True/False). No subjetivo. |
| non\_functional\_reqs | Restricciones de rendimiento, seguridad y escalabilidad. | Debe incluir métricas cuantificables (ej. "\< 200ms"). |
| out\_of\_scope | Qué NO se va a construir. | Crítico para prevenir el alcance progresivo (*scope creep*). |

La inclusión explícita de out\_of\_scope es una mejora táctica derivada de las mejores prácticas de gestión de productos, obligando al modelo a razonar sobre los límites del sistema, lo que reduce drásticamente las alucinaciones de funcionalidades no solicitadas en etapas posteriores.

### **2.2 Agente 2: El Arquitecto de Software \- El Diseñador de Planos**

El Arquitecto recibe el relevo del PM y transforma el "qué" en el "cómo". Este agente debe resistir la tentación de escribir código de implementación y centrarse exclusivamente en la estructura macroscópica y las decisiones tecnológicas. Su función es maximizar la mantenibilidad y minimizar la deuda técnica antes de que se escriba una sola línea de código.

* **Perfil Cognitivo:** Sistémico, Abstracto, Orientado a Compromisos (*Trade-offs*). Debe evaluar múltiples enfoques técnicos y seleccionar el óptimo basándose en las restricciones del PRD.1  
* **Directiva Principal:** "Diseña para el futuro. Minimiza la complejidad accidental."  
* **Modo Operativo:** Descomposición funcional y selección de patrones de diseño.

**Contrato de Entrada (Inputs):**

* PRD.json: La fuente de verdad inmutable sobre los requisitos.

Contrato de Salida (Outputs):  
El Arquitecto produce el documento de solicitud de comentarios (RFC) y, crucialmente, el árbol de archivos.

1. **RFC Técnico (RFC.md):** Justificación de las decisiones tecnológicas, diagramas de flujo de datos y modelos de entidad-relación.  
2. **Árbol de Archivos (file\_tree.json):** Un mapa completo de cada archivo que existirá en el proyecto.

La Importancia del file\_tree.json:  
Este artefacto es una innovación clave en el flujo AGENTS\_V2. Al obligar al Arquitecto a pre-declarar la estructura de archivos en un formato JSON plano, proporcionamos al Agente Desarrollador un "esqueleto" pre-aprobado.9 Esto elimina la parálisis de análisis del desarrollador sobre dónde ubicar un archivo y garantiza una arquitectura coherente (por ejemplo, asegurando que se siga un patrón MVC o Microservicios).  
**Esquema de Salida Estructurada (Diseño):**

| Campo | Descripción | Restricción de Validación |
| :---- | :---- | :---- |
| tech\_stack | Lenguajes, frameworks y versiones específicas. | Debe usar versiones LTS (Long Term Support) salvo indicación contraria. |
| file\_structure | Lista anidada o plana de rutas de archivos. | Debe incluir archivos de configuración (package.json, .env.example). |
| api\_definitions | Firmas de funciones y endpoints de API. | Debe definir Tipos de Entrada y Salida para interfaces públicas. |
| data\_models | Esquemas de base de datos. | Definiciones SQL o NoSQL completas con tipos de datos. |

### **2.3 Agente 3: El Desarrollador \- El Ejecutor Determinista**

En el modelo V2, el Agente Desarrollador es deliberadamente limitado en su alcance creativo. No cuestiona el diseño del Arquitecto ni reinterpreta los requisitos del PM. Su excelencia reside en la precisión sintáctica y la eficiencia algorítmica dentro de los límites establecidos. Es el motor de producción del sistema.

* **Perfil Cognitivo:** Literal, Procedural, Enfocado en Sintaxis.  
* **Directiva Principal:** "Sigue el plano. Si el plano está roto, devuelve el ticket."  
* **Modo Operativo:** Generación de código archivo por archivo y validación sintáctica local.

**Contrato de Entrada (Inputs):**

* RFC.md: Para contexto y lógica de negocio.  
* file\_tree.json: La lista de tareas de generación de archivos.

**Contrato de Salida (Outputs):**

* 03\_src/: El directorio conteniendo todo el código fuente.  
* build\_log.md: Un registro de las acciones tomadas y cualquier decisión de implementación de bajo nivel (ej. optimizaciones de bucles).

Estrategia de Generación de Código:  
El desarrollador debe iterar sobre el file\_tree.json. Para cada entrada, genera el contenido del archivo correspondiente. Es imperativo que el desarrollador incluya todos los archivos de soporte necesarios para la ejecución, como requirements.txt o docker-compose.yml, asegurando que el entorno sea reproducible. El código debe estar exhaustivamente comentado, utilizando docstrings que reflejen las especificaciones del RFC, cerrando así el ciclo de trazabilidad entre diseño e implementación.1

### **2.4 Agente 4: El Ingeniero de QA \- El Guardián Adversarial**

El último bastión de calidad es el Agente de QA. A diferencia de los modelos de auto-corrección simples, el QA en **AGENTS\_V2** adopta una postura adversarial. Su objetivo no es demostrar que el código funciona (sesgo de confirmación), sino intentar romperlo (falsabilidad). Este enfoque es fundamental para descubrir errores lógicos y casos borde que un desarrollador "optimista" pasaría por alto.10

* **Perfil Cognitivo:** Escéptico, Destructivo (en el sentido de pruebas), Minucioso.  
* **Directiva Principal:** "No confíes. Verifica. Intenta romper el sistema."  
* **Modo Operativo:** Generación de casos de prueba, ejecución de suites de pruebas y análisis de cobertura.

**Contrato de Entrada (Inputs):**

* PRD.json: Para extraer los Criterios de Aceptación (La Verdad).  
* 03\_src/: El objeto a probar.

**Contrato de Salida (Outputs):**

* 04\_quality/test\_suite/: Código de pruebas unitarias e integración (ej. archivos .test.js o test\_\*.py).  
* validation\_report.json: El veredicto final.

Esquema de Salida Estructurada (Reporte de Validación):  
El reporte de validación es el documento que autoriza el cierre del ticket o dispara el flujo de iteración.

| Campo | Descripción |
| :---- | :---- |
| status | PASSED |
| coverage\_score | Porcentaje de código cubierto por pruebas. |
| passed\_tests | Lista de IDs de criterios de aceptación verificados. |
| failed\_tests | Lista de fallos con trazas de error y pasos de reproducción. |
| critical\_defects | Lista de bugs que impiden la funcionalidad core. |

---

## **3\. Protocolos Operativos y Flujos de Trabajo**

Una vez definidos los actores y sus artefactos, el manual **AGENTS\_V2.md** debe establecer las reglas de juego: cómo se mueven estos artefactos y qué sucede cuando las cosas salen mal.

### **3.1 Protocolo de Hand-off (Transferencia) Basado en Archivos**

El mecanismo de "Hot Potato" (Patata Caliente) asegura que solo un agente tenga el control de escritura sobre el estado activo del proyecto en un momento dado, previniendo condiciones de carrera y conflictos de edición.

**El Ciclo de Vida del Hand-off:**

1. **Bloqueo (Lock):** El agente activo crea un archivo .lock en el directorio de trabajo, señalando que está operando.  
2. **Ejecución:** El agente lee los inputs inmutables de los directorios anteriores y genera sus outputs en su directorio asignado.  
3. **Validación de Salida:** Antes de liberar el ticket, el agente debe verificar contra su propio esquema de salida (Self-Reflection).11 Por ejemplo, el Arquitecto verifica que su JSON de árbol de archivos sea sintácticamente válido.  
4. **Generación de Manifiesto:** Si la validación interna pasa, el agente escribe el manifest.json en la carpeta .handoff/.  
5. **Desbloqueo (Unlock):** El agente borra su archivo .lock y entra en estado de reposo.  
6. **Enrutamiento:** El sistema de orquestación (script observador) detecta el nuevo manifiesto y activa al siguiente agente en la cadena.3

### **3.2 Flujos de Iteración: El Protocolo "Devolver el Ticket" (Return the Ticket)**

En el desarrollo de software real, el camino feliz (Happy Path) es la excepción, no la regla. Los requisitos cambian, las librerías resultan incompatibles, y el código tiene bugs. **AGENTS\_V2** formaliza el manejo de estas excepciones mediante el protocolo "Devolver el Ticket".12

Este protocolo otorga a cada agente el derecho (y la obligación) de rechazar una tarea si las condiciones de entrada no se cumplen o si encuentra un bloqueo insuperable. Esto previene la "falla silenciosa" donde un agente intenta alucinar una solución a un problema imposible.

**Escenarios de Rechazo y Flujos de Retorno:**

#### **Escenario A: Ambigüedad en los Requisitos (Arquitecto \-\> PM)**

* **Disparador:** El Arquitecto recibe un PRD donde los criterios de aceptación son subjetivos (ej. "Que la app sea rápida").  
* **Acción:** El Arquitecto genera un rejection\_report.json y devuelve el control al PM.  
* **Payload de Rechazo:**  
  JSON  
  {  
    "type": "REJECTION",  
    "source": "Architect",  
    "target": "Product\_Manager",  
    "reason": "AMBIGUITY",  
    "details": "El criterio 'rápido' no es cuantificable. Por favor defina latencia máxima en milisegundos.",  
    "ticket\_id": "PRD-001"  
  }

#### **Escenario B: Inviabilidad Técnica (Desarrollador \-\> Arquitecto)**

* **Disparador:** El Desarrollador detecta que una librería especificada en el RFC está obsoleta o no es compatible con el resto del stack.  
* **Acción:** El Desarrollador rechaza el diseño.  
* **Payload de Rechazo:**  
  JSON  
  {  
    "type": "REJECTION",  
    "source": "Developer",  
    "target": "Architect",  
    "reason": "DEPENDENCY\_CONFLICT",  
    "details": "La librería 'pandas-ai' v2.0 solicitada no es compatible con Python 3.8. Se requiere Python 3.9+.",  
    "ticket\_id": "RFC-001"  
  }

#### **Escenario C: Fallo de Validación (QA \-\> Desarrollador)**

* **Disparador:** Las pruebas automatizadas fallan o la cobertura de código es insuficiente.  
* **Acción:** QA devuelve el ticket al Desarrollador para corrección (Bug Fix Loop).  
* **Payload de Rechazo:**  
  JSON  
  {  
    "type": "REJECTION",  
    "source": "QA",  
    "target": "Developer",  
    "reason": "TEST\_FAILURE",  
    "details": "3 Tests fallaron en el módulo de autenticación. Ver logs adjuntos.",  
    "evidence\_path": "04\_quality/error\_traces/auth\_failure.log"  
  }

### **3.3 Reglas de Gobernanza de Bucles**

Para evitar bucles infinitos de rechazo (Ping-Pong Effect), el manual establece reglas de gobernanza estrictas:

1. **Regla del Doble Rebote:** Si un ticket es devuelto por la misma razón dos veces consecutivas, se dispara una **Escalada de Intervención Humana (HITL)**. El sistema se pausa y solicita ayuda al usuario.13  
2. **Límite de Iteraciones:** Se establece un máximo de 3 ciclos de corrección Dev-QA. Si no se resuelve, se asume un error de diseño fundamental y el ticket se escala hacia atrás, al Arquitecto.  
3. **Costo de la Corrección:** Los agentes deben priorizar soluciones que minimicen la reescritura de código.

---

## **4\. AGENTS\_V2.md: El Documento Unificado (Especificación del Manual)**

A continuación se presenta el contenido textual normativo que debe residir en el archivo AGENTS\_V2.md dentro del repositorio del proyecto. Este texto sirve como el "Prompt del Sistema" para la orquestación.

---

# **AGENTS\_V2.md: Manual de Operaciones de Agentes Autónomos**

Versión: 2.0.0  
Autoridad: Technical Product Manager (TPM)  
Propósito: Definir los protocolos de interacción, roles y estándares de artefactos para el equipo de desarrollo de IA.

## **1\. Directivas Globales**

1. **Aislamiento de Roles:** Actúe estrictamente dentro de los límites de su perfil asignado. No asuma responsabilidades de otros agentes.  
2. **Supremacía del Archivo:** Si no está escrito en un archivo, no existe. El chat es efímero; los archivos son eternos.  
3. **Comunicación Estructurada:** Toda comunicación crítica debe seguir los esquemas JSON definidos.  
4. **Fallo Rápido (Fail-Fast):** Rechace entradas defectuosas inmediatamente mediante el protocolo "Return the Ticket".

## **2\. Perfiles de Agentes y Flujos de Trabajo**

### **2.1 Product Manager (PM)**

* **Misión:** Traducir la intención del usuario en especificaciones técnicas deterministas.  
* **Entrada:** 00\_input/user\_prompt.md  
* **Salida:** 01\_product/PRD.md (Narrativa), 01\_product/PRD.json (Eschema).  
* **Instrucciones Críticas:**  
  * Interrogue al usuario si la solicitud es ambigua.  
  * Defina Criterios de Aceptación binarios para cada Historia de Usuario.  
  * Declare explícitamente lo que está FUERA del alcance (out\_of\_scope).

### **2.2 Arquitecto de Software (ARCH)**

* **Misión:** Diseñar la solución técnica más robusta y mantenible que satisfaga el PRD.  
* **Entrada:** 01\_product/PRD.json  
* **Salida:** 02\_architecture/RFC.md, 02\_architecture/file\_tree.json.  
* **Instrucciones Críticas:**  
  * Seleccione un stack tecnológico estable y compatible.  
  * Provea un árbol de archivos completo (file\_tree.json) que sirva de esqueleto para el desarrollo.  
  * Defina las interfaces de API y esquemas de datos en detalle.

### **2.3 Desarrollador (DEV)**

* **Misión:** Implementar el diseño técnico con precisión sintáctica y eficiencia.  
* **Entrada:** 02\_architecture/file\_tree.json, 02\_architecture/RFC.md.  
* **Salida:** 03\_src/ (Código Fuente), 03\_src/build\_log.md.  
* **Instrucciones Críticas:**  
  * Genere código solo para los archivos definidos en el árbol.  
  * Asegure la inclusión de archivos de gestión de dependencias (requirements.txt, etc.).  
  * Incluya comentarios de documentación (docstrings) alineados con el RFC.

### **2.4 Ingeniero de QA (QA)**

* **Misión:** Validar que la implementación cumple con los Criterios de Aceptación del PRD.  
* **Entrada:** 01\_product/PRD.json, 03\_src/.  
* **Salida:** 04\_quality/validation\_report.json, 04\_quality/test\_suite/.  
* **Instrucciones Críticas:**  
  * Genere y ejecute pruebas unitarias y de integración.  
  * Reporte fallos con evidencia de trazas de error.  
  * Rechace el ticket si existen defectos críticos.

## **3\. Protocolos de Hand-off y Rechazo**

### **3.1 Manifiesto de Transferencia**

Cada finalización de tarea debe ir acompañada de un manifest.json en .handoff/:

JSON

{  
  "source": "Agent\_Name",  
  "target": "Next\_Agent",  
  "status": "SUCCESS",  
  "artifacts": \["path/to/file1", "path/to/file2"\]  
}

### **3.2 Protocolo de Rechazo (Return the Ticket)**

Si una entrada es inválida o la tarea imposible, genere un reporte de rechazo:

JSON

{  
  "status": "REJECTED",  
  "reason": "Error Code (e.g., AMBIGUITY, COMPILATION\_ERROR)",  
  "details": "Descripción humana del error.",  
  "corrective\_action": "Sugerencia para el agente anterior."  
}

---

## **5\. Implementación y Consideraciones Futuras**

La adopción de **AGENTS\_V2.md** transforma el desarrollo de software asistido por IA de un proceso artesanal y propenso a errores a una disciplina de ingeniería industrial. Al estandarizar las interfaces entre agentes y hacer cumplir la persistencia basada en archivos, creamos un sistema que es:

1. **Auditable:** Cada decisión, desde el requisito hasta la línea de código, deja un rastro documental inspeccionable.  
2. **Resiliente:** Los protocolos de rechazo evitan que los errores se propaguen y se amplifiquen a lo largo de la cadena (Efecto Bola de Nieve).  
3. **Escalable:** La arquitectura modular permite la futura incorporación de agentes más especializados (ej. Agente de Seguridad, Agente de DevOps) sin reestructurar el flujo central.

Para una implementación exitosa, se recomienda utilizar un orquestador ligero (script en Python o Node.js) que actúe como el "sistema nervioso" del flujo, observando los directorios de artefactos y despachando las llamadas a los agentes LLM según las reglas definidas en este manual. La integración de herramientas de validación estática (linters, compiladores) dentro del bucle del Agente Desarrollador y QA potenciará aún más la autonomía del sistema, permitiendo ciclos de auto-corrección rápidos antes de involucrar la supervisión humana.

### **5.1 Integración Humana (Human-in-the-Loop)**

A pesar de la autonomía, el juicio humano sigue siendo insustituible para decisiones estratégicas y resolución de conflictos de alto nivel. El manual V2 integra puntos de control explícitos donde el sistema puede "pedir ayuda", asegurando que la IA sirva como un multiplicador de fuerza para el ingeniero humano, y no como una caja negra incontrolable.

En conclusión, **AGENTS\_V2.md** no es solo un documento; es la infraestructura lógica para la próxima generación de desarrollo de software. Al fusionar la creatividad de los LLMs con la disciplina de la ingeniería de sistemas, este manual sienta las bases para un futuro donde el software se cultiva y orquesta, en lugar de escribirse manualmente.

#### **Fuentes citadas**

1. Orchestrating a 4-Agent AI Coding Workflow (2025 Update) (2).docx  
2. Seizing the agentic AI advantage \- McKinsey, acceso: noviembre 28, 2025, [https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage](https://www.mckinsey.com/capabilities/quantumblack/our-insights/seizing-the-agentic-ai-advantage)  
3. Best Practices for Multi-Agent Orchestration and Reliable Handoffs \- Skywork.ai, acceso: noviembre 28, 2025, [https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/](https://skywork.ai/blog/ai-agent-orchestration-best-practices-handoffs/)  
4. Understanding Handoff in Multi-Agent AI Systems \- Jetlink, acceso: noviembre 28, 2025, [https://www.jetlink.io/post/understanding-handoff-in-multi-agent-ai-systems](https://www.jetlink.io/post/understanding-handoff-in-multi-agent-ai-systems)  
5. Effective context engineering for AI agents \- Anthropic, acceso: noviembre 28, 2025, [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
6. Multi-Agent Workflows: A Practical Guide to Design, Tools, and Deployment \- Medium, acceso: noviembre 28, 2025, [https://medium.com/@kanerika/multi-agent-workflows-a-practical-guide-to-design-tools-and-deployment-3b0a2c46e389](https://medium.com/@kanerika/multi-agent-workflows-a-practical-guide-to-design-tools-and-deployment-3b0a2c46e389)  
7. Structured outputs in LLMs: Definition, techniques, applications, benefits \- LeewayHertz, acceso: noviembre 28, 2025, [https://www.leewayhertz.com/structured-outputs-in-llms/](https://www.leewayhertz.com/structured-outputs-in-llms/)  
8. Structured model outputs \- OpenAI API, acceso: noviembre 28, 2025, [https://platform.openai.com/docs/guides/structured-outputs](https://platform.openai.com/docs/guides/structured-outputs)  
9. Introducing Strands Agent SOPs – Natural Language Workflows for AI Agents \- AWS, acceso: noviembre 28, 2025, [https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/](https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/)  
10. How TELUS Digital leverages autonomous quality control agents for improved AI training data, acceso: noviembre 28, 2025, [https://www.telusdigital.com/insights/data-and-ai/article/autonomous-quality-control-agents](https://www.telusdigital.com/insights/data-and-ai/article/autonomous-quality-control-agents)  
11. 7 Tips to Build Self-Improving AI Agents with Feedback Loops | Datagrid, acceso: noviembre 28, 2025, [https://www.datagrid.com/blog/7-tips-build-self-improving-ai-agents-feedback-loops](https://www.datagrid.com/blog/7-tips-build-self-improving-ai-agents-feedback-loops)  
12. THE CONCEPT OF DECENTRALIZED AND SECURE ELECTRONIC MARKETPLACE \- CS-Rutgers University, acceso: noviembre 28, 2025, [https://www.cs.rutgers.edu/\~minsky/papers/marketplace.pdf](https://www.cs.rutgers.edu/~minsky/papers/marketplace.pdf)  
13. Building for Agentic AI \- Agent SDKs & Design Patterns | by Ryan LIN \- Medium, acceso: noviembre 28, 2025, [https://medium.com/dsaid-govtech/building-for-agentic-ai-agent-sdks-design-patterns-ef6e6bd4a029](https://medium.com/dsaid-govtech/building-for-agentic-ai-agent-sdks-design-patterns-ef6e6bd4a029)
