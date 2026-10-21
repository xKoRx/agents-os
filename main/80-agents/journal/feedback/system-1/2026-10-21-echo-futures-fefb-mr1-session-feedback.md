---
type: session_feedback
schema_version: 1
scope: project
created: "2026-10-21"
updated: "2026-10-21"
area: "[[Echo]]"
project: "[[Echo Futures — Execution Client y Feed Batching]]"
entities:
  - "[[Echo Futures — Execution Client y Feed Batching]]"
related: []
aliases: []
confidence: verified
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/session-feedback
  - area/echo
---

# Feedback — FEFB S01 MR1 (orquestación de reparación con especialistas ONE-SHOT)

- **Pain pattern candidate (ownership por paths vs defecto que cruza la frontera):** el pin de los tests de `adapters/ntfeed` fijaba el comportamiento exacto que la reparación ordenada sustituía, pero `adapters/**` quedó fuera del ownership del especialista dueño del fix → round-trip por el submanager. En reparaciones, declarar explícitamente "tests-pins del comportamiento a sustituir" como parte del ownership del especialista que ejecuta el cambio de contrato (el diff del pin se revisa igual).
- **Campaña de capacidad:** `TestFEFBW4CapacityCampaign` con config 1800s aborta silenciosamente con el timeout default de `go test` (600s) — exigir `-timeout` explícito en el runbook de campaña (recurrente con [[echo-go-zcode-harness-quirks]]).
- **Hallazgo útil transferible:** sin toolchain C# en el host, `dotnet-install.sh` user-local (~/.dotnet, SDK 8.0.426) permitió tests ejecutables REALES del motor puro (`EchoFeedV1.cs` linkeado, sin assemblies NT) — sustituye al guard estático como evidencia conductual (reparación-02); declarar el patrón en los runbooks de cliente.
