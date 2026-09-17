# Example: Senal de Problema Detectada (Validar)

## Contexto

El owner reporta que una nota creada en su Mac no aparece en la
VM. Hay senal concreta de problema: ausencia de archivo esperado.

## Procedimiento

1. Cargar la skill `operational-healthcheck-policy`
2. Validar el sync state
3. Reportar y decidir

```bash
# Verificar que el plugin LiveSync tenga data.json
VAULT_ROOT="${AGENTS_OS_VAULT:-$PWD}"
ls -la "$VAULT_ROOT/.obsidian/plugins/obsidian-livesync/"

# Tamano del vault
du -sh "$VAULT_ROOT"

# Conteo de archivos .md
find "$VAULT_ROOT" -type f -name "*.md" -not -path "*/.obsidian/*" | wc -l

# Ver logs de LiveSync (si hay)
ls "$HOME"/.config/obsidian/*/logs/ 2>/dev/null | head
```

4. Si todo OK: reportar "sync en buen estado, archivo probablemente
   en transito o con conflicto pendiente" y sugerir al owner
   reintentar
5. Si hay problema: abrir un ticket o notificar según severidad

## Anti-Pattern

- Decir "sync esta bien" sin validar (asumir)
- Repetir el check 3 veces "por si acaso"
- Intentar arreglar el problema directamente sin pedir OK

## Por Que Importa

Este es exactamente el caso para el cual la skill existe. Validar
una vez con evidencia, reportar, decidir. No es rutina.
