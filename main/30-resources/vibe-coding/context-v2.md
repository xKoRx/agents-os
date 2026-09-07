---
type: resource
status: active
area: "[[Personal]]"
created: 2026-07-08
updated: 2026-08-08
aliases:
  - context-v2
  - CONTEXT_V2
tags:
  - resource
  - vibe-coding
  - pilar
---

# **CONTEXT_V2: MANUAL DE ARQUITECTURA DE GESTIÓN DE CONTEXTO BASADO EN ARTEFACTOS**

## **1\. El Paradigma de la Memoria Estructural en Sistemas de Desarrollo Autónomo**

### **1.1. La Crisis de la Ingeniería de Contexto Probabilística**

La industria del desarrollo de software asistido por Inteligencia Artificial (IA) se encuentra en un punto de inflexión crítico. Durante la fase inicial de adopción de Grandes Modelos de Lenguaje (LLMs) para la generación de código, la arquitectura predominante fue la Generación Aumentada por Recuperación (RAG) basada en similitud vectorial. Este enfoque, aunque eficaz para la recuperación de información en lenguaje natural no estructurado, ha demostrado limitaciones severas cuando se aplica a la ingeniería de software rigurosa. El problema fundamental radica en la naturaleza probabilística de los embeddings vectoriales: al fragmentar el código en "chunks" arbitrarios y recuperarlos mediante similitud de cosenos, se desintegra la coherencia lógica y estructural inherente al software.1

En la ingeniería de software, el contexto no es meramente una colección de fragmentos de texto relacionados semánticamente; es una red causal y jerárquica de decisiones, restricciones y especificaciones. Un sistema RAG tradicional sufre de lo que denominamos "amnesia contextual" o fragmentación semántica: puede recuperar la implementación de una función, pero olvidar la interfaz que la define, el documento de requerimientos que justifica su existencia o el registro de decisión arquitectónica (ADR) que prohíbe el uso de ciertas bibliotecas dentro de ella.1 Esta pérdida de "situational awareness" resulta en código que es sintácticamente correcto pero arquitectónicamente inválido, generando deuda técnica acelerada y alucinaciones funcionales.

### **1.2. Hacia una Gestión de Contexto Determinista (Artifact-Driven Context)**

Para superar estas limitaciones, este manual establece la arquitectura CONTEXT\_V2, una refactorización integral que transita desde la "Ingeniería de Contexto" (manipulación de prompts y recuperación difusa) hacia la "Gestión de Contexto mediante Artefactos". En este nuevo paradigma, el repositorio deja de ser un almacén pasivo de código para convertirse en el "cerebro" estructurado del framework, operando como una memoria a largo plazo navegable, determinista y explicable sin dependencia de bases de datos vectoriales opacas.4

La premisa central de CONTEXT\_V2 es que la inteligencia de un agente de codificación no reside únicamente en los pesos del modelo, sino en la calidad y estructura de su entorno de información. Al igual que un desarrollador humano no lee fragmentos aleatorios de código para entender un sistema, sino que consulta la documentación de alto nivel (PRD), las discusiones técnicas (RFC) y las decisiones normativas (ADR), el agente debe interactuar con estos "Artefactos Cognitivos". Estos documentos actúan como anclas deterministas que guían el razonamiento del modelo, permitiendo una comprensión profunda de la intención detrás del código.6

Esta arquitectura se fundamenta en tres pilares estratégicos que se detallarán exhaustivamente en este reporte:

1. **Memoria Estructural (/docs):** La implementación de una jerarquía documental estandarizada que sirve como memoria episódica y semántica.  
2. **Optimización de Ventana (Whole-Document Loading):** El rechazo a la fragmentación (chunking) en favor de la carga inteligente de documentos completos, aprovechando las ventanas de contexto extendidas modernas.  
3. **Trazabilidad como Código:** La vinculación explícita mediante anotaciones (tags) entre la especificación y la implementación.

| Característica | Enfoque RAG Tradicional (V1) | Enfoque Artifact-Driven (CONTEXT\_V2) |
| :---- | :---- | :---- |
| **Mecanismo de Recuperación** | Búsqueda Vectorial (Similitud Probabilística) | Navegación de Grafos y Referencias (Determinista) |
| **Unidad de Información** | Chunk (Fragmento arbitrario de texto/código) | Artefacto (Documento completo: RFC, PRD, Archivo) |
| **Manejo del Contexto** | Reconstrucción imprecisa de fragmentos | Carga de documentos completos y mapas de repositorio |
| **Trazabilidad** | Implícita o inexistente | Explícita mediante etiquetas @req, @trace |
| **Coste Operativo** | Alto (Mantenimiento de Vector DB, índices) | Bajo (Sistema de archivos nativo, Git) |
| **Fiabilidad en Código** | Propensa a alucinaciones por falta de contexto global | Alta coherencia gracias a "Barandillas" (ADRs) |

---

## **2\. Arquitectura de la Memoria a Largo Plazo: El Sistema /docs**

### **2.1. Ontología y Taxonomía de la Información**

En la arquitectura CONTEXT\_V2, la carpeta /docs se eleva de ser un repositorio de documentación pasiva a constituir la Memoria de Largo Plazo (LTM) activa del agente. Para que un sistema autónomo navegue eficazmente por esta memoria, la estructura de carpetas debe reflejar una ontología lógica que mapee el ciclo de vida del desarrollo de software. No es suficiente con almacenar información; esta debe estar indexada por su función temporal y normativa.8

La taxonomía propuesta organiza la información en tres estratos cognitivos que responden a las preguntas fundamentales de cualquier tarea de ingeniería: "¿Qué queremos hacer?" (Intención), "¿Cómo lo haremos?" (Planificación) y "¿Qué reglas debemos respetar?" (Normativa).

#### **2.1.1. Jerarquía de Directorios Estandarizada**

La siguiente estructura de directorios es normativa para cualquier repositorio bajo CONTEXT\_V2. Esta estructura inmutable permite a los agentes (y herramientas como aider o cursor) predecir la ubicación de la información crítica sin necesidad de búsquedas exhaustivas.

/docs  
├── 00\_meta/ \# Metadatos del Sistema Cognitivo  
│ ├── CONTEXT\_V2.md \# El manual de arquitectura (Definición del Sistema)  
│ ├── llms.txt \# Índice optimizado para consumo por IA 10  
│ ├── glossary.md \# Memoria Semántica (Definiciones de Dominio)  
│ └── persona.md \# Definición del Rol del Agente y Tono  
├── 01\_prd/ \# Memoria de Intención (Product Requirements Documents)  
│ ├── active/ \# Requerimientos en desarrollo actual  
│ ├── backlog/ \# Requerimientos aprobados pendientes  
│ └── archive/ \# Memoria histórica de requerimientos completados  
├── 02\_rfc/ \# Memoria de Trabajo (Request for Comments)  
│ ├── 0000-template.md \# Plantilla estricta para nuevos diseños  
│ ├── 0015-auth-refactor.md \# Ejemplo de RFC activo  
│ └── index.md \# Tabla de contenidos dinámica  
├── 03\_adr/ \# Memoria Normativa (Architecture Decision Records)  
│ ├── 0000-use-madr.md \# Decisión sobre el formato de registro  
│ ├── 0012-postgres-only.md \# Restricción técnica vigente  
│ └── index.md \# Estado actual de la arquitectura  
└── 04\_specs/ \# Especificaciones Técnicas Detalladas  
├── api/ \# Contratos de API (OpenAPI/Swagger)  
└── schema/ \# Modelos de Datos (SQL, JSON Schema)

### **2.2. Definición de Artefactos y Metadatos (Machine-Readable Frontmatter)**

Para transformar documentos de texto en estructuras de datos procesables, es imperativo el uso de bloques de metadatos YAML (Frontmatter) al inicio de cada archivo Markdown. Esto permite a los agentes filtrar, clasificar y cargar contexto basándose en atributos estructurados (Metadatos) en lugar de depender exclusivamente del análisis semántico del cuerpo del texto, reduciendo drásticamente la latencia y el error.11

#### **2.2.1. PRD: La Memoria de Intención**

El Documento de Requerimientos de Producto (PRD) define el problema y el alcance. En CONTEXT\_V2, el PRD no es un documento monolítico, sino un artefacto atómico enfocado en Historias de Usuario y Criterios de Aceptación verificables.

**Esquema de Frontmatter para PRD:**

YAML

\---  
id: PRD-005  
title: Sistema de Autenticación Biométrico  
type: product\_requirement  
status: approved \# Valores permitidos: \[draft, review, approved, implemented, deprecated\]  
owner: @security-team  
priority: high  
dependencies:  
tags: \[security, auth, bio, compliance\]  
last\_updated: 2025-02-15  
version: 1.2  
\---

Este bloque permite al sistema responder consultas complejas como "Listar todos los requerimientos de seguridad de alta prioridad aprobados pero no implementados" mediante una simple consulta de metadatos, sin leer el contenido de cientos de archivos.14

#### **2.2.2. RFC: La Memoria de Trabajo Activa**

El RFC (Request for Comments) representa el proceso de razonamiento y diseño técnico. Es el artefacto más dinámico y crítico durante la fase de codificación. Un agente que trabaja en una tarea debe cargar obligatoriamente el RFC correspondiente como su "Contexto Primario".

**Esquema de Frontmatter para RFC:**

YAML

\---  
id: RFC-023  
title: Migración a OAuth2 con Proveedores Externos  
type: request\_for\_comments  
status: active \# Valores permitidos: \[proposed, active, finalized, rejected, superseded\]  
linked\_prd:  
affected\_components:   
  \- /src/auth  
  \- /src/users/models.py  
driver: "Necesidad de soportar SSO corporativo y cumplimiento SOC2"  
decision\_date: 2025-03-01  
\---

El campo affected\_components es una innovación crucial de CONTEXT\_V2. Actúa como una directiva de "pre-fetching" para el agente, indicándole explícitamente qué áreas del código fuente deben ser indexadas o cargadas en el mapa del repositorio (RepoMap) antes de intentar cualquier modificación. Esto elimina la necesidad de que el agente "adivine" qué archivos son relevantes.16

#### **2.2.3. ADR: La Memoria Normativa Inmutable**

Los Registros de Decisión Arquitectónica (ADR) actúan como las "leyes" del repositorio. Documentan decisiones pasadas inmutables y, lo más importante, el *porqué* de esas decisiones. En un entorno impulsado por IA, los ADRs funcionan como "Guardrails" (Barandillas) cognitivos.6 Si un agente sugiere introducir una nueva base de datos NoSQL, debe validar primero esta sugerencia contra los ADRs existentes.

**Esquema de Frontmatter para ADR (Estándar MADR):**

YAML

\---  
id: ADR-012  
title: Estandarización de Base de Datos Relacional (PostgreSQL)  
type: architecture\_decision  
status: accepted \# Valores permitidos: \[proposed, accepted, rejected, superseded, deprecated\]  
date: 2023-11-15  
deciders: \[arquitecto-jefe, tech-lead\]  
supersedes: ADR-004  
context: "Necesidad de consistencia ACID estricta en transacciones financieras"  
decision: "Usar PostgreSQL 15+ como única fuente de verdad"  
consequences:   
  positive:  
  negative: \["Mayor complejidad en escalado horizontal"\]  
compliance\_check: "reject\_if\_db\_is\_not\_postgres"  
\---

El campo compliance\_check puede ser utilizado por herramientas de linter o agentes de revisión para automatizar la validación de pull requests contra las decisiones arquitectónicas vigentes.19

### **2.3. El Índice Maestro para Agentes: Implementación de llms.txt**

Para unificar estos artefactos en una estructura de navegación optimizada para LLMs, CONTEXT\_V2 adopta y extiende el estándar llms.txt. A diferencia de robots.txt que es para crawlers de búsqueda, llms.txt proporciona un mapa semántico curado del repositorio.10

Estrategia de Implementación:  
Se deben generar dos archivos en la raíz del repositorio o en /docs/00\_meta/:

1. **llms.txt (Resumido):** Contiene enlaces a los documentos de "Alto Nivel" (Manual de Arquitectura, Índices de ADR/RFC, Glosario). Diseñado para la exploración inicial del agente.  
2. **llms-full.txt (Exhaustivo):** Contiene el contenido concatenado o referenciado de toda la documentación activa. Diseñado para ventanas de contexto masivas cuando se requiere una comprensión total del proyecto.22

**Estructura Normativa de llms.txt:**

# **Contexto del Proyecto \[Nombre\]**

Resumen: Sistema de backend para gestión logística basado en Microservicios y Python.

## **Documentación Núcleo (Long-Term Memory)**

* Arquitectura Global: Reglas maestras y estructura del repositorio.  
  \-(/docs/03\_adr/index.md): Restricciones arquitectónicas activas que DEBEN respetarse.  
* : Definiciones de términos de dominio.

## **Contexto Activo (Working Memory)**

\-(/docs/02\_rfc/0018-route-opt.md): Tarea actual en desarrollo.  
\-(/docs/01\_prd/active/prd-012.md): Requerimientos funcionales para la tarea actual.

## **Especificaciones Técnicas**

\-(/docs/04\_specs/api/v1.yaml): Contrato OpenAPI.  
Esta estructura permite a los agentes realizar una "carga jerárquica": primero leen llms.txt para orientarse, y luego solicitan los documentos específicos necesarios, evitando la sobrecarga de tokens irrelevantes.

---

## **3\. Optimización de Ventana de Contexto: Estrategias de Carga**

### **3.1. La Superioridad de la Carga de Documentos Completos (Whole-Document Loading)**

En la arquitectura RAG convencional, los documentos largos se dividen en fragmentos (chunks) de tamaño fijo (ej. 512 tokens). En el contexto de código y documentación técnica, esta práctica es perjudicial. Un fragmento de un RFC que describe una solución técnica pierde su sentido si se separa de la sección de "Contexto" que explica el problema o de la sección de "Riesgos" que advierte sobre efectos secundarios. La "coherencia narrativa" es vital para el razonamiento complejo del LLM.

Con la disponibilidad de ventanas de contexto de 128k, 200k e incluso 1M+ tokens (Claude 3.5, Gemini 1.5), CONTEXT\_V2 impone la regla de **Whole-Document Loading**.

**Reglas de Carga Determinista:**

1. **Regla del Contexto Activo (The RFC Rule):** Si la tarea está asociada a un RFC activo, el documento completo del RFC *debe* cargarse en memoria. No se permite chunking. El RFC actúa como el "prompt extendido" que alinea al agente con el objetivo inmediato.  
2. **Regla del README Recursivo:** Cada directorio principal en /src debe contener un README.md técnico. Antes de explorar archivos de código individuales en una carpeta, el agente debe ingerir el README.md completo. Esto proporciona una comprensión de alto nivel de la responsabilidad del módulo ("Compresión Semántica Pre-calculada").

### **3.2. Mapa de Repositorio (RepoMap) y Algoritmos de Selección**

Dado que cargar *todo* el código fuente sigue siendo inviable incluso con ventanas grandes (por costo y latencia), CONTEXT\_V2 utiliza la técnica de **RepoMap** (Mapa de Repositorio), popularizada por herramientas como Aider, para proporcionar una "visión periférica" del código.

#### **3.2.1. Algoritmo de Construcción del RepoMap**

El RepoMap no es una simple lista de archivos. Es un grafo comprimido generado mediante análisis estático (AST).

1. **Análisis AST (Tree-sitter):** Se parsean todos los archivos fuente para extraer definiciones de clases, funciones, métodos y variables globales, ignorando cuerpos de funciones y detalles de implementación.  
2. **Ranking de Importancia (PageRank):** Se construye un grafo de dependencias (quién llama a quién). Se aplica un algoritmo tipo PageRank para identificar los módulos más "centrales" o referenciados del sistema.  
3. **Compresión Selectiva:** Basado en el presupuesto de tokens disponible (ej. 2k tokens para el mapa), se seleccionan los identificadores más importantes y se presentan en un formato de árbol conciso.

Este mapa permite al agente "ver" la estructura global y las firmas de funciones disponibles en todo el proyecto sin leer el código completo, facilitando la alucinación cero en nombres de funciones y tipos.

### **3.3. Presupuesto de Tokens y Estrategia de Carga (Context Budgeting)**

Para gestionar eficazmente la ventana de contexto, se establece una política de asignación de presupuesto de tokens. Esta política asegura que la información crítica (Instrucciones, Memoria Activa) nunca sea desplazada por información secundaria (Código irrelevante).

Esta estratificación asegura que el modelo tenga siempre acceso a las "Reglas de Juego" (ADRs) y al "Objetivo Actual" (RFC), mientras gestiona dinámicamente el detalle del código.

---

## **4\. Trazabilidad Documental: El Sistema Nervioso del Repositorio**

### **4.1. Trazabilidad como Código (Traceability as Code)**

Uno de los desafíos más persistentes en ingeniería de software es la desconexión semántica entre el requerimiento (el "qué") y el código (el "cómo"). En sistemas tradicionales, esta relación es externa (Jira vs. Git). En CONTEXT\_V2, establecemos la **Trazabilidad como Código**, incrustando los enlaces directamente en los artefactos fuente mediante un sistema estricto de anotaciones. Esto permite auditorías bidireccionales y análisis de impacto automatizados.

### **4.2. Sintaxis y Taxonomía de Anotaciones**

Se define un estándar de etiquetas (tags) que deben incluirse en los comentarios de documentación del código (Docstrings, Javadoc, TSDoc). Estas etiquetas son parseables por herramientas y leídas por los agentes de IA para entender el propósito de cada bloque de código.

#### **4.2.1. Ejemplos de Implementación**

**En Código (Python):**

**En Documentación (Markdown \- RFC):**

### **3.1 Componente de Verificación El sistema debe validar la firma criptográfica localmente.**

* **Implementación:** src/auth/BiometricAuthenticator.py \- **Validación:** tests/auth/test\_bio\_integrity.py

### **4.3. Validación Automatizada y Linting de Trazabilidad**

La integridad del sistema CONTEXT\_V2 depende de la veracidad de estos enlaces. Un enlace roto es una "alucinación estructural". Por lo tanto, se debe implementar un pipeline de validación (Linter de Trazabilidad) en CI/CD.

**Algoritmo de Validación del Linter:**

1. **Escaneo:** El linter recorre /src extrayendo todas las etiquetas @req, @ref, @context.  
2. **Verificación de Existencia:** Para cada etiqueta, verifica que el ID referenciado exista en el Frontmatter de algún archivo en /docs.  
   * *Error:* "El archivo auth.py referencia PRD-999 que no existe."  
3. **Verificación de Estado:** Verifica que el documento referenciado no esté en estado deprecated o rejected.  
   * *Warning:* "El código referencia RFC-002 que está marcado como superseded por RFC-015. Actualizar referencia."  
4. **Análisis de Cobertura (Backward Traceability):** Genera una matriz que alerta sobre requerimientos aprobados en /docs/01\_prd/active/ que no tienen ninguna etiqueta @req asociada en el código (Requerimientos Huérfanos).

---

## **5\. Manual de Operaciones: Flujos de Trabajo Agenticos**

### **5.1. El Ciclo de Vida del Desarrollo Basado en Artefactos**

La adopción de CONTEXT\_V2 implica un cambio en el flujo de trabajo del desarrollador (humano o agente). No se comienza "escribiendo código", se comienza "gestionando memoria".

#### **Fase 1: Ingesta y Planificación (Context Loading)**

1. **Inicio:** Se crea un nuevo RFC en /docs/02\_rfc/ (estado: proposed) describiendo la tarea.  
2. **Análisis:** El Agente lee el RFC, consulta llms.txt y carga los ADR relevantes para asegurar cumplimiento normativo (ej. "¿Puedo usar Redis aquí?").  
3. **Mapa de Impacto:** El Agente identifica los componentes afectados y actualiza el campo affected\_components en el Frontmatter del RFC. Esto prepara la "Memoria de Trabajo".

#### **Fase 2: Ejecución y Trazabilidad (Coding)**

1. **Implementación:** El Agente escribe el código fuente.  
2. **Etiquetado Obligatorio:** Durante la generación de código, el Agente *debe* insertar las etiquetas @req y @ref apuntando al RFC y PRD activos.  
   * *Instrucción al Agente:* "Cada nueva clase debe tener un docstring con @req apuntando al PRD-XXX".  
3. **Actualización de Documentación:** El Agente actualiza el README.md local del módulo si la arquitectura cambia.

#### **Fase 3: Consolidación y Cierre (Memory Commit)**

1. **Revisión:** El sistema de CI ejecuta el Linter de Trazabilidad. Si faltan enlaces, el PR falla.  
2. **Commit de Memoria:** Al fusionar (merge) el código, el RFC pasa de status: active a status: implemented. Si se generaron nuevas decisiones arquitectónicas, se formaliza un nuevo ADR y se añade a /docs/03\_adr.  
3. **Git como Controlador de Contexto (GCC):** El historial de Git, junto con los metadatos de los commits, sirve como una capa temporal de trazabilidad, permitiendo al agente responder preguntas históricas ("¿Cómo evolucionó la implementación de este requerimiento?").

### **5.2. Protocolo de Agentes y MCP (Model Context Protocol)**

Para estandarizar la interacción entre el editor (IDE) y el repositorio bajo CONTEXT\_V2, se recomienda la implementación de un servidor MCP (Model Context Protocol). MCP actúa como el protocolo de transporte que expone la estructura de /docs y el RepoMap al agente de IA de manera estructurada, en lugar de que el agente tenga que "leer archivos" manualmente.

**Herramientas y Recursos:**

* **Servidor MCP Local:** Un script ligero que expone los índices de llms.txt y los resultados de búsqueda de etiquetas @req como "Recursos" y "Herramientas" MCP.  
* **Prompt del Sistema:** Configurar el agente con una instrucción base que le obligue a consultar /docs/00\_meta/CONTEXT\_V2.md antes de iniciar cualquier sesión compleja.

---

## **6\. Estrategia de Migración y Adopción**

### **6.1. De Legacy a CONTEXT\_V2 (Brownfield Projects)**

No es viable reescribir la historia de un proyecto existente de la noche a la mañana. La estrategia de adopción debe ser incremental ("Strangler Fig Pattern" aplicado a documentación).

1. **Bootstrapping:** Crear la estructura /docs y el archivo llms.txt inicial.  
2. **Snapshot Normativo:** Documentar las decisiones actuales críticas en ADRs, incluso si se tomaron hace años (ADRs retroactivos).  
3. **Scan-and-Tag:** Utilizar un script o agente para escanear el código base (/src) y añadir etiquetas @req: UNKNOWN o @legacy en los módulos principales.  
4. **Política de "Boy Scout":** Cada vez que se toca un archivo legacy para una nueva feature, se debe reemplazar el @req: UNKNOWN con un enlace a un PRD/RFC nuevo o existente. La deuda de documentación se paga progresivamente.

### **6.2. Gobernanza y Mantenimiento**

El riesgo principal de este sistema es la desincronización ("Context Rot"). Si la documentación miente, el agente alucina.

* **Incentivo:** Los desarrolladores notarán rápidamente que el agente es mucho más competente y autónomo en las áreas del código que cumplen con CONTEXT\_V2. Esto crea un ciclo de retroalimentación positiva: "Mejor documentación \= Menor trabajo manual para mí".  
* **Automatización:** Confiar en los linters y validadores en el CI/CD, no en la disciplina humana. El pipeline debe fallar si se detectan "Requerimientos Huérfanos" o "Código Zombie" (código vinculado a requerimientos obsoletos).

---

## **7\. Conclusión**

La arquitectura CONTEXT\_V2 representa un avance fundamental sobre los enfoques simplistas de RAG. Al reconocer que el código no es texto plano, sino una estructura lógica hipervinculada, y al elevar la documentación al estatus de "artefacto computable", habilitamos una nueva generación de agentes de desarrollo de software. Estos agentes, equipados con una memoria estructurada, un contexto optimizado y un sistema nervioso de trazabilidad, pueden operar con un nivel de autonomía, precisión y coherencia inalcanzable mediante métodos puramente probabilísticos. Este manual proporciona la hoja de ruta técnica para transformar cualquier repositorio en un cerebro digital preparado para la era de la IA generativa.

#### **Fuentes citadas**

1. Context Engine vs. RAG: 5 Technical Showdowns for Code AI, acceso: noviembre 28, 2025, [https://www.augmentcode.com/guides/context-engine-vs-rag-5-technical-showdowns-for-code-ai](https://www.augmentcode.com/guides/context-engine-vs-rag-5-technical-showdowns-for-code-ai)  
2. Why Context Is the New Currency in AI: From RAG to Context Engineering | Towards Data Science, acceso: noviembre 28, 2025, [https://towardsdatascience.com/why-context-is-the-new-currency-in-ai-from-rag-to-context-engineering/](https://towardsdatascience.com/why-context-is-the-new-currency-in-ai-from-rag-to-context-engineering/)  
3. What is Retrieval Augmented Generation (RAG)? \- Databricks, acceso: noviembre 28, 2025, [https://www.databricks.com/glossary/retrieval-augmented-generation-rag](https://www.databricks.com/glossary/retrieval-augmented-generation-rag)  
4. GibsonAI/Memori: Open-Source Memory Engine for LLMs, AI Agents & Multi-Agent Systems \- GitHub, acceso: noviembre 28, 2025, [https://github.com/GibsonAI/Memori](https://github.com/GibsonAI/Memori)  
5. Comparing Memory Systems for LLM Agents: Vector, Graph, and Event Logs, acceso: noviembre 28, 2025, [https://www.marktechpost.com/2025/11/10/comparing-memory-systems-for-llm-agents-vector-graph-and-event-logs/](https://www.marktechpost.com/2025/11/10/comparing-memory-systems-for-llm-agents-vector-graph-and-event-logs/)  
6. Architecture decision record (ADR) examples for software planning, IT leadership, and template documentation \- GitHub, acceso: noviembre 28, 2025, [https://github.com/joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)  
7. Documenting Design Decisions using RFCs and ADRs \- Bruno Scheufler, acceso: noviembre 28, 2025, [https://brunoscheufler.com/blog/2020-07-04-documenting-design-decisions-using-rfcs-and-adrs](https://brunoscheufler.com/blog/2020-07-04-documenting-design-decisions-using-rfcs-and-adrs)  
8. Code Documentation Best Practices \- OneNine, acceso: noviembre 28, 2025, [https://onenine.com/code-documentation-best-practices/](https://onenine.com/code-documentation-best-practices/)  
9. Git Context Controller: Manage the Context of LLM-based Agents like Git \- arXiv, acceso: noviembre 28, 2025, [https://arxiv.org/html/2508.00031v1](https://arxiv.org/html/2508.00031v1)  
10. Getting Started with llms.txt \- Developer Guide | llms.txt hub, acceso: noviembre 28, 2025, [https://llmstxthub.com/guides/getting-started-llms-txt](https://llmstxthub.com/guides/getting-started-llms-txt)  
11. RFC-0016 Collaborative Continuous Monitoring Standard · FedRAMP community · Discussion \#87 \- GitHub, acceso: noviembre 28, 2025, [https://github.com/FedRAMP/community/discussions/87](https://github.com/FedRAMP/community/discussions/87)  
12. Using YAML frontmatter \- GitHub Docs, acceso: noviembre 28, 2025, [https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter](https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter)  
13. Fields | Front Matter, acceso: noviembre 28, 2025, [https://frontmatter.codes/docs/content-creation/fields](https://frontmatter.codes/docs/content-creation/fields)  
14. Requirements traceability \- Azure Pipelines \- Microsoft Learn, acceso: noviembre 28, 2025, [https://learn.microsoft.com/en-us/azure/devops/pipelines/test/requirements-traceability?view=azure-devops](https://learn.microsoft.com/en-us/azure/devops/pipelines/test/requirements-traceability?view=azure-devops)  
15. Comprehensive Guide to Traceability Tools: Ensuring Quality and Accountability, acceso: noviembre 28, 2025, [https://www.modernrequirements.com/blogs/comprehensive-guide-to-traceability-tools/](https://www.modernrequirements.com/blogs/comprehensive-guide-to-traceability-tools/)  
16. Repository map \- Aider, acceso: noviembre 28, 2025, [https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)  
17. Agentic-Insights/codebase-context-spec: Proposal for a flexible, tool-agnostic, codebase context system that helps teach AI coding tools about your codebase. Super easy to get started, just create a .context directory in the root of your project with an index.md file in it. \- GitHub, acceso: noviembre 28, 2025, [https://github.com/Agentic-Insights/codebase-context-spec](https://github.com/Agentic-Insights/codebase-context-spec)  
18. Best practices \- AWS Prescriptive Guidance, acceso: noviembre 28, 2025, [https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html)  
19. Building an Architecture Decision Record Writer Agent | by Piethein Strengholt | Medium, acceso: noviembre 28, 2025, [https://piethein.medium.com/building-an-architecture-decision-record-writer-agent-a74f8f739271](https://piethein.medium.com/building-an-architecture-decision-record-writer-agent-a74f8f739271)  
20. Use YAML front matter for metadata | MADR \- Architectural Decision Records, acceso: noviembre 28, 2025, [https://adr.github.io/madr/decisions/0013-use-yaml-front-matter-for-meta-data.html](https://adr.github.io/madr/decisions/0013-use-yaml-front-matter-for-meta-data.html)  
21. The Complete Guide to llms.txt: Should You Care About This AI Standard? \- Publii, acceso: noviembre 28, 2025, [https://getpublii.com/blog/llms-txt-complete-guide.html](https://getpublii.com/blog/llms-txt-complete-guide.html)  
22. LLMs.txt Explained | TDS Archive \- Medium, acceso: noviembre 28, 2025, [https://medium.com/data-science/llms-txt-414d5121bcb3](https://medium.com/data-science/llms-txt-414d5121bcb3)  
23. Python source \- llms-txt, acceso: noviembre 28, 2025, [https://llmstxt.org/core.html](https://llmstxt.org/core.html)  
24. /llms.txt—a proposal to provide information to help LLMs use websites – Answer.AI, acceso: noviembre 28, 2025, [https://www.answer.ai/posts/2024-09-03-llmstxt.html](https://www.answer.ai/posts/2024-09-03-llmstxt.html)  
25. Give Your AI Agents Deep Understanding With LLMS.txt | by Dazbo (Darren Lester) | Google Cloud \- Medium, acceso: noviembre 28, 2025, [https://medium.com/google-cloud/give-your-ai-agents-deep-understanding-with-llms-txt-4f948590332b](https://medium.com/google-cloud/give-your-ai-agents-deep-understanding-with-llms-txt-4f948590332b)  
26. Chunking Strategies for LLM Applications \- Pinecone, acceso: noviembre 28, 2025, [https://www.pinecone.io/learn/chunking-strategies/](https://www.pinecone.io/learn/chunking-strategies/)  
27. Workaround with knowledge files bigger than context window \- GPT builders, acceso: noviembre 28, 2025, [https://community.openai.com/t/workaround-with-knowledge-files-bigger-than-context-window/848792](https://community.openai.com/t/workaround-with-knowledge-files-bigger-than-context-window/848792)  
28. LARCH: Large Language Model-based Automatic Readme Creation with Heuristics \- arXiv, acceso: noviembre 28, 2025, [https://arxiv.org/abs/2308.03099](https://arxiv.org/abs/2308.03099)  
29. Building a better repository map with tree sitter \- Aider, acceso: noviembre 28, 2025, [https://aider.chat/2023/10/22/repomap.html](https://aider.chat/2023/10/22/repomap.html)  
30. Repo Map Accuracy · Issue \#45 · dwash96/aider-ce \- GitHub, acceso: noviembre 28, 2025, [https://github.com/dwash96/aider-ce/issues/45](https://github.com/dwash96/aider-ce/issues/45)  
31. Improving aider's repo map to do large, simple refactors automatically. \- ミツモア Tech blog, acceso: noviembre 28, 2025, [https://engineering.meetsmore.com/entry/2024/12/24/042333](https://engineering.meetsmore.com/entry/2024/12/24/042333)  
32. Top techniques to Manage Context Lengths in LLMs \- Agenta, acceso: noviembre 28, 2025, [https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms](https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms)  
33. Constructing Traceability Links between Software Requirements and Source Code Based on Neural Networks \- MDPI, acceso: noviembre 28, 2025, [https://www.mdpi.com/2227-7390/11/2/315](https://www.mdpi.com/2227-7390/11/2/315)  
34. Verify Generated Code by Using Code Tracing \- MATLAB & Simulink \- MathWorks, acceso: noviembre 28, 2025, [https://www.mathworks.com/help/ecoder/ug/verify-generated-code-by-using-code-tracing.html](https://www.mathworks.com/help/ecoder/ug/verify-generated-code-by-using-code-tracing.html)  
35. Requirement tracking Doxygen \- c++ \- Stack Overflow, acceso: noviembre 28, 2025, [https://stackoverflow.com/questions/63157201/requirement-tracking-doxygen](https://stackoverflow.com/questions/63157201/requirement-tracking-doxygen)  
36. How to create a requirement traceability matrix with AI: Streamline compliance and audits, acceso: noviembre 28, 2025, [https://www.dartai.com/blog/how-to-create-a-requirement-traceability-matrix-with-ai](https://www.dartai.com/blog/how-to-create-a-requirement-traceability-matrix-with-ai)  
37. 2 years building agent memory systems, ended up just using Git : r/AI\_Agents \- Reddit, acceso: noviembre 28, 2025, [https://www.reddit.com/r/AI\_Agents/comments/1mw4jvp/2\_years\_building\_agent\_memory\_systems\_ended\_up/](https://www.reddit.com/r/AI_Agents/comments/1mw4jvp/2_years_building_agent_memory_systems_ended_up/)  
38. llms \- full.txt \- Model Context Protocol, acceso: noviembre 28, 2025, [https://modelcontextprotocol.io/llms-full.txt](https://modelcontextprotocol.io/llms-full.txt)  
39. Why is Model Context Protocol relevant for agentic systems? | by Ricardo Olivieri, acceso: noviembre 28, 2025, [https://medium.com/@ricardo.olivieri/why-is-model-context-protocol-relevant-for-agentic-systems-b2d5b8b121b8](https://medium.com/@ricardo.olivieri/why-is-model-context-protocol-relevant-for-agentic-systems-b2d5b8b121b8)
