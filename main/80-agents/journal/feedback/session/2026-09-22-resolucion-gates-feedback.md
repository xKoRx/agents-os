---
type: feedback
schema_version: 1
scope: session
created: 2026-09-22
updated: 2026-09-22
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
aliases: []
agent_surface: ZCode (workstation kor)
agent_model: glm-5.3-flash (zai)
agent_run:
session_goal: ONE-SHOT resolución integral de gates de ejecución 25-26sep (P1/T-21b/W-02/R2/018) sin mutaciones productivas
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agentsos
  - agent/system1
---

# Session Feedback - 2026-09-22 - resolucion gates (Aranea Backup/DR)

## Pain Pattern Candidate

- **Errores de canal/host en documentos de autorización**: el GATE-22SEP (instrumento de decisión del owner) citaba kronos como `ariadna@192.168.31.100` cuando .100 es zeus (kronos = .120). Un error así, ejecutado sin la verificación de identidad por hostname que hizo esta sesión, habría dirigido `qm`/`lvextend` de la VM 180 al nodo equivocado. Regla sugerida para mandatos de infra: todo comando de ejecución debe anclar identidad por hostname verificado en vivo en el preflight, nunca por IP citada en un documento (coherente con la regla global de identidad canónica).

## Friction / gaps

- El tool Skill de ZCode no resuelve skills del vault por ruta (`80-agents/skills/...`): el bootstrap canónico se ejecutó leyendo el SKILL.md directamente. Funciona, pero la indización de skills del vault en el cliente haría el arranque más robusto.
- La documentación W-01(b) llegó a GATE con comandos internamente incoherentes (vgextend del host sobre disco del guest) pese a haber pasado por 3 rondas de revisión adversarial documental: la revisión documental no sustituye un dry-run técnico del comando propuesto. Sugerencia: en mandatos de ejecución, exigir que cada bloque de comandos haya pasado por al menos una lectura de coherencia host-vs-guest (¿dónde corre?, ¿qué ve?).

## Positivo

- El patrón "verificación RO masiva + preparación ejecutable + gates separados" permitió resolver P1/018/W-02 en una sesión sin tocar producción; el fixture con pruebas negativas atrapó 2 defectos míos antes de llegar al owner.
