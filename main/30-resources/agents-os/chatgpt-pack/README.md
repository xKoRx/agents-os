# AGENTS OS — Pack para iteración en ChatGPT

Este bundle transporta los componentes base de AGENTS OS **tal como existen en
el vault**, acompañados por una capa breve de orientación. No reemplaza ni
reescribe las fuentes canónicas.

## Qué subir a ChatGPT

### Opción recomendada: Proyecto de ChatGPT

1. Descomprime `agents-os-chatgpt.zip`.
2. Sube `README.md`, `PROJECT-STATE.md` e `ITERATION-PROMPT.md`.
3. Sube la carpeta `sources/` completa si quieres iterar cualquier componente.
4. Usa `MANIFEST.md` para comprobar procedencia y hashes.

### Opción liviana

Sube solamente:

- `PROJECT-STATE.md`;
- `ITERATION-PROMPT.md`;
- `AGENTS-OS-BASE-COMPONENTS.md`.

Luego agrega desde `sources/` la skill, template o memoria pública concreta que
quieras modificar. Este modo reduce el universo documental inicial.

## Jerarquía de autoridad

1. Constitución y decisiones/ADRs vigentes.
2. Contratos compartidos.
3. Skills para comportamiento ejecutable.
4. Guía operativa y documentos conceptuales.
5. Notas canónicas de proyecto para estado actual.
6. `PROJECT-STATE.md` como orientación derivada.
7. Evaluaciones, reportes y presentaciones como evidencia, no como regla.

Ante una contradicción, ChatGPT debe identificarla y proponer una resolución;
no debe fusionar silenciosamente las afirmaciones.

## Qué contiene

- Guía `agents-os.md`, Context Router, constitución y perfil del usuario.
- Contratos de metadata, tipos, skills y Graphify.
- Skills AGENTS OS completas, incluyendo archivos auxiliares disponibles.
- Templates de Sistema 1 y Sistema 2.
- ADRs, learnings, known errors y runbooks públicos de AGENTS OS.
- Estado del proyecto, planificador activo Fase 3, topología Resources/agents, Economía de Tokens y evaluación de adopción.
- Un Markdown consolidado de los componentes base.

## Qué se excluye deliberadamente

- `80-agents/memory/internal/`;
- raw sessions, summaries, logs y feedbacks individuales;
- drafts archivados;
- outputs de Graphify;
- secretos, credenciales y evidencia pesada;
- proyectos no relacionados con AGENTS OS.

## Regeneración

Desde la raíz del vault:

```bash
bash "30-resources/agents-os/chatgpt-pack/build-pack.sh"
```

La ejecución ensambla el bundle en un directorio temporal, genera hashes
SHA-256, verifica que las copias sean idénticas y conserva sólo
`30-resources/agents-os/distribution/agents-os-chatgpt.zip` en el vault.

Las copias son snapshots derivados: nunca se editan para devolver cambios al
vault. Los cambios propuestos por ChatGPT deben aplicarse sobre las rutas
canónicas indicadas en `MANIFEST.md`.
