---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - SQCLI 144 - Primera carga de GUI y proyecto sin terminar]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/sqx-144-abrir-la-gui-de-sqcli-puede-dejar-un-proyecto-ejecutandose-indefinidamente"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - SQCLI 144 - Primera carga de GUI y proyecto sin terminar

## Síntesis vigente

Reporte reproducido por el autor: la primera carga de la interfaz web de un proceso sqcli puede alterar el estado del proyecto y dejarlo trabajando indefinidamente si ya tiene estrategias.

## Conocimiento extraído

**Disparador:** SQX 144 con `sqcli -gui`, primera apertura web del proceso cuando el proyecto activo ya tiene estrategias en un databank. El autor atribuye el fallo a una recarga de bancos que marca el proyecto como parado sin comprobar la ejecución.

**Síntomas:** Start activo y Stop/Pause grises con CPU/log activos; Build ignora tiempo límite y sigue Evolving generation; retests no cierran; StopAndStart no avanza. Que el proceso exista no prueba progreso.

**Prueba descrita:** mismo Build limitado a diez minutos; abrir GUI al minuto siete con 15 estrategias produjo bloqueo, no abrirla terminó a los diez minutos.

**Prevención propuesta:** no usar `-gui`, o completar la primera carga antes de que el proyecto produzca estrategias. Precarga automática: barrera `-waitfor` antes de start, ruta entre comillas idéntica en ambos lados y archivo anterior eliminado; esperar a que SQCLI confirme Waiting for file antes de solicitar carga, y después a quietud del log. Cada reinicio de proceso requiere repetirlo, no cada proyecto encadenado.

El script del autor espera diez minutos y puede liberar el proyecto sin precarga si no detecta la barrera: en ese caso no es una prueba de precarga completada. Solicitar carga mientras SQCLI aún carga proyectos puede dañar bancos, según el reporte.

**Recuperación declarada:** terminar el proceso colgado y relanzar con prevención; se reinicia el proyecto desde la primera tarea, conservando lo exportado previamente mediante SaveToFiles. No se ejecutó esta recuperación.

## Comentarios y matices

El autor aclara que no aplica a usar solo la GUI de escritorio. El motor no se hace más rápido por usar CLI: la ventaja es automatizar ejecución, encadenado y recuperación.

## Adjuntos y cobertura

Sin adjuntos de contenido adicional identificados.

## Interés para Forge

Prioridad de consulta: **Alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/sqx-144-abrir-la-gui-de-sqcli-puede-dejar-un-proyecto-ejecutandose-indefinidamente).
- Autor: Xavi Lorente. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - SQCLI 144 - Primera carga de GUI y proyecto sin terminar]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

Reporte específico de 144; no se reprodujo localmente ni se extrapola a otras versiones. El código PowerShell completo del post no se copió ni ejecutó; antes de usarlo debe revisarse contra la instalación real.
