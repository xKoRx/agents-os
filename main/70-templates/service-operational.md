---
type: service-doc
schema_version: 1
status: template
area: "[[Personal]]"
aliases:
  - "{{title}}"
tags:
  - kind/service-doc
  - area/personal
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

> [!warning] Template — completar antes de activar
> Materializar con `materialize_schema_note.py service-doc <destino.md>`,
> reemplazar placeholders con evidencia real y cambiar `status: template` a
> `draft`, `partial` o `active`. El dominio decide el destino, inventario,
> herramientas y runbooks; este template no presupone ninguno.

## 🎯 Propósito

- **Rol concreto del servicio:**
- **Qué deja de funcionar si cae:**
- **Límites de responsabilidad:**

## 🌐 Acceso

| Canal | Referencia segura |
|---|---|
| UI o endpoint | `<referencia>` |
| Shell o consola | `<referencia>` |
| API | `<referencia>` |

No guardar credenciales ni URLs con secretos embebidos. Enlazar el mecanismo
de secretos autorizado por el dominio.

## 💾 Estado y persistencia

- **Datos o volúmenes:**
- **Estado durable:**
- **Backup/restore:**
- **Dependencias:**

## 🔧 Operación

### Health check

```bash
<comando-read-only>
```

### Restart o recuperación

```bash
<comando-autorizado>
```

### Logs

- **Canal:**
- **Consulta:**

### Update

- **Método:**
- **Precondiciones:**
- **Rollback:**

## 📊 Observabilidad

- **Métricas:**
- **Alertas:**
- **Dashboards:**
- **Señal de salud primaria:**

## 🚨 Incidentes

- **Runbook:**
- **Known errors:**
- **Escalamiento:**

## 🔗 Relaciones

- **Owner:**
- **Servicios relacionados:**
- **Infraestructura o runtime:**

## 📌 Provenance

- **Fuentes verificadas:**
- **Fecha de verificación:** {{date:YYYY-MM-DD}}
- **Confidence:**

## ✅ Validación antes de activar

- [ ] El propósito describe el rol, no sólo el nombre.
- [ ] Los accesos son referencias seguras y no contienen secretos.
- [ ] Health check, recuperación y rollback son comandos autorizados.
- [ ] Persistencia, dependencias y observabilidad están documentadas.
- [ ] Runbooks y relaciones resuelven en el dominio activo.
- [ ] `area`, tags y destino corresponden al dominio real.
