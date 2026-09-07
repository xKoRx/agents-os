---
type: meeting
date: 2026-08-10
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
attendees:
  - Rodrigo Arturo Jara Castro
  - David Ismael Muena Henriquez
tags:
  - area/meli
  - kind/meeting
created: 2026-08-10
updated: 2026-08-10
---

🗂️ Contexto / Agenda

- Discusión sobre la estabilización de la plataforma, los desafíos actuales de la infraestructura y la transición arquitectónica hacia el uso de un atributo de "contexto" en los componentes para gestionar las relaciones de flujo de datos y configuraciones.

📝 Notas

- El equipo está priorizando la estabilización de la plataforma, lo que incluye la limpieza de tópicos, particiones y réplicas innecesarias para mejorar la observabilidad y reducir costos operativos.
- Existe una dependencia crítica de conocimientos técnicos específicos (ej. Wagner) y una falta de "ownership" clara en los componentes de infraestructura, situación que se busca corregir para descentralizar el conocimiento.
- Se está implementando una estrategia para agregar un campo de "contexto" a los componentes. Esto permitirá definir explícitamente las fuentes (orígenes) y destinos de cada componente, en lugar de depender de propiedades genéricas o variables de entorno actuales.
- El manejo de datos actual es ineficiente; se explorará el uso de formatos más óptimos (como Avro) a futuro para reducir el volumen de datos en tránsito.

🧭 Decisiones

- Se priorizará la estabilización técnica de la plataforma mediante la limpieza de configuraciones obsoletas y la optimización de los tópicos existentes.
- Se adoptará el uso del atributo de "contexto" en todos los componentes para estandarizar la gestión de entradas/salidas y configuración, desplazando la lógica de propiedades genéricas.

✅ Action items

- Rodrigo: Analizar el código actual (ControlPlane, PlayMaker, SDK events) para comprender cómo se extraen las propiedades y cómo viajan los mensajes, con el fin de proponer una especificación para la implementación del "contexto".
- Rodrigo: Coordinar con Alonso (líder del equipo Front-end) para entender cómo la interfaz define las relaciones entre componentes.
- Rodrigo: Documentar hallazgos, áreas de mejora en la base de datos y proponer un plan de acción para la limpieza de infraestructura.

Extra
[https://rio.adminml.com/](https://rio.adminml.com/) front actual
[https://signals.adminml.com/](https://signals.adminml.com/) front nuevo