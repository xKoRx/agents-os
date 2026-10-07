# Z1 — ADAPTER DESIGN (zai sibling)

Fecha: 2026-10-06 · Decidido por: Primary Manager (adjudicación de diseño, pre-implementación) · Baseline de producto: `feature/v2-layered-knowledge-model @ 20ad4de` · Implementado en: `bd2edc1d` (Z2).

## Frontera

`providers.VLMProvider` (internal/providers/providers.go) queda intacto y CONGELADO. El adapter `zai` es un sibling de `openrouter` en `internal/providers/zai/`. Sin framework genérico "openai-compat": mecánicas (retries/backoff/timeout/scrubbing/httptest style) copiadas de openrouter. Prohibido renombrar o re-apuntar OpenRouter.

## Identidad honesta

```text
VLMAdapter = zai
VLMModel   = glm-5.3-flash (default; eco del provider en Response.Model)
```

Adapter y modelo participan de los fingerprints (full/L1/L2) → nuevo baseline semántico esperado. Prohibido adoptar/resumir runs con fingerprint openrouter/stealth.

## Env contract

| Variable | Default | Notas |
|---|---|---|
| `MKE_ZAI_API_KEY` | (requerida) | Falta → invalid input pre-red (exit 2). Jamás en argv/artifacts/journal. |
| `MKE_ZAI_BASE_URL` | `https://api.z.ai/api/paas/v4` | API general (knowledge workload), no coding-only. |
| `MKE_ZAI_MODEL` | `glm-5.3-flash` | Multimodal; `glm-5.3` text-only NO sirve para Chapter 01. |
| `MKE_ZAI_JSON_MODE` | `true` | `response_format {type: json_object}` en todas las llamadas Infer. Parser MKE sigue siendo dueño fail-closed. |
| `MKE_ZAI_REASONING_EFFORT` | `max` | Junto con `thinking {type: enabled}` (siempre). Aceptado junto (sonda combo Z0). |

## Request mapping (OpenAI-compatible Chat Completions)

- `model`, `temperature: 0` (preferencia determinista de MKE, aceptada por Z0), `stream: false`, SIN `max_tokens` (default del endpoint suficiente, verificado en Z0 con tarea de 30 ítems finish=stop; igual que openrouter).
- System prompt separado cuando existe. Text parts + images como bloques ordenados del mensaje user; imagen → `{"type":"image_url","image_url":{"url":"data:<MediaType>;base64,<b64>"}}`; orden preservado; identidad de evidencia intacta (misma semántica de mapping que openrouter).

## Error mapping (clases congeladas)

429→retryable · 5xx→retryable · timeout transporte→retryable · empty choices/content→retryable · 404 modelo/endpoint→unsupported · capability gap→unsupported · 401/403→fatal · JSON malformado del contenido final→fatal (parser dueño) · bounded retries con backoff (constantes openrouter), nunca infinito.

## Response / provenance

`RequestID=RequestIdentity(req)`, `ResponseID=id`, `Model=eco del provider (fallback config)`, `OutputSchemaID=req.OutputSchemaID`, `Structured=content final crudo`, `Usage` (completion ya incluye reasoning_tokens del backend), cost ausente (no inventar). Audit exclusivamente `zai.*` sanitizado (http_status, finish_reason, json_mode, temperature, reasoning_effort, thinking, model_requested, content_bytes). `reasoning_content` NUNCA entra a Structured/Audit/docs — solo el content final es elegible para parsing. Scrubbing de la key configurada sobre todo texto del provider (incluidos Structured y audit, un paso más estricto que openrouter).

## Evidencia de soporte (Z0)

AUTH PASS en API general · multi-imagen con orden verificado por contenido (red→blue) · JSON mode + imagen combinados OK · thinking ON por defecto con reasoning_tokens contabilizados en completion (H-1: presupuestos chicos dejan content vacío → clase retryable existente; MKE no envía max_tokens, sin riesgo) · timeout de transporte observable → retryable.
