# Z0 — PROVIDER PREFLIGHT (Z.AI / glm-5.3-flash)

Fecha: 2026-10-06 · Manager: Primary Manager (sesión migración) · Ejecutado con sondas directas mínimas desde `/tmp/z0_probe.py` (fuera de repo/vault), credencial leída de env protegido `~/.config/mke/zai.env` (chmod 600, fuera de repo/vault). **Ninguna sonda incluyó la key en argumentos de comandos, artifacts ni en este documento.** Todos los payloads usaron fixtures locales mínimos (PNG sólidos 4×4 generados en memoria), no Chapter 01.

```text
ZAI_PREFLIGHT = PASS
ZAI_GENERAL_API_ENTITLEMENT = OK   (api.z.ai/api/paas/v4 autenticó y sirvió completions; no se usó endpoint coding-only)
OWNER_DECISION_REQUIRED = NO
```

## Matriz de sondas (metadata sanitizada)

| Sonda | Request clave | Resultado | Evidencia (sanitizada) |
|---|---|---|---|
| Z0-1 auth | chat/completions mínimo | **PASS** HTTP 200 | `id` "2026100…", `model` "glm-5.3-flash" |
| Z0-2 text completion | "Reply OK" (max_tokens 16) | PASS HTTP 200 (2.3s) | contenido vacío porque reasoning consumió el budget mínimo — ver hallazgo H-1; no es defecto de la API |
| Z0-3 JSON estricto | `response_format {type: json_object}` | **PASS** | JSON válido devuelto con presupuesto realista (finish=stop, contenido `{"ok":true,"items":[1,2,3]}`) |
| Z0-3b json+thinking+temp0 | thinking enabled + temperature 0 | PASS HTTP 200 | aceptado sin error |
| Z0-3c reasoning_effort | `reasoning_effort: "max"` | PASS HTTP 200 | aceptado sin error |
| Z0-4 single image | 1 PNG data URL Base64 | PASS HTTP 200 | imagen aceptada; con budget mínimo el contenido fue consumido por reasoning (H-1) |
| Z0-5 multi image + orden | 2 PNG (rojo, azul) + JSON por orden | **PASS** | `{"first":"red","second":"light blue"}` — orden de imágenes respetado y colores identificados |
| Z0-6 usage accounting | presente en todas las respuestas | **PASS** | `prompt_tokens` / `completion_tokens` (+`reasoning_tokens` detail) / `total_tokens`; sin campo de costo (no inventar) |
| Z0-7 response shape | id/model/finish_reason | **PASS** | `id` string tipo "20261007…", `model` eco correcto, `finish_reason` stop/length presentes, `content` string |
| Z0-8 large structured | 30 ítems JSON (~650 completion tokens) | **PASS** HTTP 200 (12.7s) | 30/30 ítems, finish=stop |
| Z0-9 timeout | read timeout cliente 3s | **PASS (observado)** | `TimeoutError` transport → clase retryable según contrato; el adapter acota con timeout por intento |
| Extra: combo completo | system+user, thinking enabled + reasoning_effort max + temperature 0 + stream false | **PASS HTTP 200** | contenido "OK", reasoning_content presente |
| Extra: default budget | sin `max_tokens`, tarea 30 ítems JSON | **PASS** | finish=stop, 30/30 ítems — el default del endpoint alcanza; el adapter puede omitir max_tokens igual que openrouter |
| Extra: imagen+JSON combinado | 1 imagen + json_object | **PASS** | `{"color":"red","polygon_count":1}` — modalidad requerida por MKE (evidencia visual + JSON) funciona |

## Requisitos duros del gate

```text
AUTH = PASS
MODEL = glm-5.3-flash            (eco del provider, no el string solicitado a ciegas)
IMAGE_INPUT = PASS               (Base64 data URL)
MULTI_IMAGE = PASS               (orden preservado verificado con contenido real)
STRUCTURED_JSON = PASS           (response_format json_object aceptado y validado)
```

## Hallazgos para Z1/Z2 (adapter policy local)

- **H-1 thinking por defecto**: `glm-5.3-flash` emite `reasoning_content` incluso sin pedirlo; los reasoning tokens se contabilizan dentro de `completion_tokens` y consumen `max_tokens`. Con presupuestos pequeños el contenido final queda vacío (finish=length, 0 contenido). Consecuencias: (a) el adapter debe dejar thinking habilitado (mandato) pero NO recortar max_tokens por debajo del uso real (openrouter no envía max_tokens; el default del endpoint es suficiente — verificado); (b) las llamadas con `finish_reason=length` y contenido vacío deben caer en la clase retryable "empty content" existente; (c) `reasoning_content` NUNCA entra a Structured/Audit — sólo el `content` final es elegible para parsing.
- **H-2 temperature 0 aceptado**: se conserva la preferencia determinista de MKE (Temperature 0, igual que openrouter). Documentado en audit metadata.
- **H-3 json_object soportado**: se usa con `MKE_ZAI_JSON_MODE=true` (default); el parser MKE sigue siendo el dueño fail-closed de la validez. `reasoning_effort=max` + `thinking.type=enabled` aceptados juntos (sonda combo).
- **H-4 sin costo**: la respuesta no expone costo; Usage se puebla honesto y cost queda ausente (no inventar).
- **H-5 API general**: la credencial sirve en `https://api.z.ai/api/paas/v4` (knowledge workload); NO se redirigió a endpoint coding-only.

Raw sanitizado: `/tmp/z0_results.json` (sin key; transitorio de máquina).
