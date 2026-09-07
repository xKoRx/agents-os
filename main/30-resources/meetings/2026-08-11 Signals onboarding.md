---
type: meeting
date: 2026-08-11
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
attendees:
  - Rodrigo Arturo Jara Castro
  - Alonso
tags:
  - area/meli
  - kind/meeting
created: 2026-08-11
updated: 2026-08-11
---

🗂️ **Contexto / Agenda**

- **Objetivo:** Sesión de alineación y transferencia de conocimiento entre Rodrigo Jara y Alonso sobre la plataforma de datos ("Signals").
- **Foco:** Discusión sobre la transición desde una arquitectura y _frontend_ heredados (_legacy_) hacia una plataforma modernizada. El objetivo central es mejorar la mantenibilidad, la escalabilidad y la gobernanza de los datos mediante un enfoque de _Data Mesh_, asegurando una colaboración estrecha entre los equipos de _Frontend_ y _Backend_.

📝 **Notas**

- **Desafíos del Sistema Heredado:** La arquitectura anterior presenta una deuda técnica alta, con colas internas mal diseñadas (difíciles de mantener) y falta de aislamiento entre ambientes (modificaciones en _staging_ afectaban a producción).
- **Arquitectura y Flujo de Datos:**
    - El flujo base consiste en **Signals** (inicio lógico) -> **Collector** (asincronía/resiliencia) -> **Kafka/Destinos**.
    - Se busca optimizar saltos de red mediante el uso de una SDK que permita a las aplicaciones conectarse directamente a Kafka, ahorrando pasos innecesarios por el colector.
    - Se requiere mejor observabilidad y control sobre los recursos (instancias, memoria, red), ya que errores en _streaming_ (como ventanas de tiempo mal configuradas) impactan directamente en el costo y estabilidad.
- **Usabilidad y Configuración:** El nuevo _frontend_ mejora la experiencia (similar a herramientas como n8n), pero existe un desconocimiento técnico en los usuarios sobre la configuración de paralelismo, particiones y réplicas. El sistema actualmente permite configuraciones arbitrarias que pueden generar desperdicio de recursos.
- **Migración:** Se realizará en "olas" (fases) y no como un _big bang_ para minimizar riesgos operativos.

🧭 **Decisiones**

- **Estrategia de Despliegue:** Se priorizará la estabilidad operativa antes de habilitar nuevas funciones masivas. Se moverá a los usuarios al nuevo _frontend_ de forma gradual.
- **Cultura de Trabajo:** Se abandona el modelo de trabajo en silos. A partir de ahora, los equipos de _Backend_ y _Frontend_ trabajarán con _backlogs_ alineados para asegurar que los plazos y objetivos se cumplan coordinadamente.
- **Observabilidad:** Se definirá como prioridad futura agregar métricas de uso y costo directamente en la interfaz para guiar a los usuarios en la toma de decisiones (ej. recomendaciones automáticas de particiones según el _throughput_).

✅ **Action items**

- **Rodrigo & Alonso:** Coordinar los _backlogs_ de Frontend y Backend de manera conjunta para avanzar alineados.
- **Alonso:** Analizar la usabilidad del nuevo _frontend_ desde una perspectiva crítica para identificar fricciones antes de la migración masiva de usuarios.
- **Ambos:** Colaborar en la creación de guías o recomendaciones dentro de la herramienta para ayudar a los usuarios a configurar correctamente los recursos (particiones/réplicas) y evitar el sobre-dimensionamiento.
- **Rodrigo:** Programar futuras sesiones de trabajo para profundizar en las explicaciones de la arquitectura de bajo nivel (Collector, Flink, Kafka) y ayudar a Alonso a resolver dudas técnicas de los usuarios.

---

**Referencias:**

- Front actual (Legacy): [https://rio.adminml.com/](https://rio.adminml.com)
- Front nuevo: [https://signals.adminml.com/](https://signals.adminml.com/)