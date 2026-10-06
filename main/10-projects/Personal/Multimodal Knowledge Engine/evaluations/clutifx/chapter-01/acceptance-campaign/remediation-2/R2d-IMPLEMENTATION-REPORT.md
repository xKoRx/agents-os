# R2d — IMPLEMENTATION REPORT (MKE V2 · Clutifx Ch01)

**Rol:** implementador R2d · remediation loop · micro-fix R3c MAJOR-1.
**Repo:** `/home/kor/mke/multimodal-knowledge-engine` · branch `feature/v2-layered-knowledge-model`.
**Base:** `1d06ce8` (verificado con `git fetch origin` + `git log`; sin commits nuevos del track paralelo, no hizo falta rebasar). **No pusheado.**

## Cambio

`internal/claims/review.go` — `groundingRelationsCalibrationV4` (calibración relations de be240f9), 2 bullets negativos nuevos tras el bullet de co-ocurrencia, v4.1:

1. **Two consequences of one shared cause** — A causa B y A causa C enacts B←A y C←A, nunca B←C. Pin: `rel-eliminacion-rango-requiere-invalidez` («y ya se puede eliminar, ya no se consideraría más un rango», asr-00161/62): dos consecuencias del cierre fuera, sin enlace entre ellas → GROUNDING_INSUFFICIENT.
2. **Narrative adjacency** — mencionar X y luego Y no enacts X←Y. Pin: `rel-falso-turtle-soup-depende-de-reaccion-real` (regla Turtle Soup + escenario «te confundas viendo que es un tartle sub y quizá no lo es», asr-00132/33) → INSUFFICIENT, con cláusula de frontera que lo distingue del few-shot positivo #3 (ahí el veredicto y la reacción ausente están enactuados dentro de un único escenario), neutralizando el vector de volcado few-shot #3 + regla de consistencia que R3c señaló.

Doc comment del bloque actualizado a v4.1 (R-M10/R3c). **Intacto:** rama claims, los 6 few-shots positivos, constantes de versión (`PromptVersionGrounding = mke.claims-ground.v4`; el bump a v4.1 es de etiqueta de calibración en comentario, no de fingerprint — el encargo no pedía bump y tocarlo habría cambiado la superficie de invalidación).

## Test

`internal/claims/review_relations_v4_test.go` — nuevo `TestRelationsBranchV41PinsNegativeDependencyPatternsFromR3c`, prompt-only (los 2 fixtures del encargo):

- Fixture 1: `rel-eliminacion-rango-requiere-invalidez` — patrón "two consequences of one shared cause" presente en el system prompt.
- Fixture 2: `rel-falso-turtle-soup-depende-de-reaccion-real` — patrón "narrative adjacency" presente.
- Comentario en el test anota que el veredicto lo da el modelo en vivo (ambos esperados GROUNDING_INSUFFICIENT en R6); la superficie determinista verificable en-repo es exactamente este pin de prompt.
- Guardas incluidas en el mismo test: no-leak de las 2 reglas nuevas a la rama claims, y few-shot #3 intacto (frontera explícita).

## Verificación

- `go vet ./internal/claims/...` — limpio.
- `go test ./internal/claims/... -count=1` — `ok mke/internal/claims`.
- `go build ./...` — OK. `gofmt -l internal/claims/` — vacío.

## Commit

`20ad4de` — `fix(claims): pin negative dependency patterns in relations calibration v4.1 (R-M10/R3c)` (2 files, +57/−1).

## FEEDBACK (Agents-OS)

- **Bootstrap correcto y barato en routing:** el marker de VAULT_ROOT resolvió a la primera y el bootstrap cargó constitution + perfil (`rjara-agent-profile.md`) + nota de continuidad global sin escaneos de carpetas. El contrato de warm-turn es la parte mejor diseñada: nada tentó a releer la base.
- **Fricción real:** el cold-start completo (constitution + perfil + continuidad + INDEX de skills) pesa más que la tarea para one-shots de implementación en repo EXTERNO al vault (todo el trabajo vivió en `~/mke`; del vault solo salió el path del reporte). Sugerencia: una regla de "cold start degrgado para tareas externas acotadas" (marker + continuidad + orientación de una línea) reservando la base completa para trabajo dentro del vault.
- **Registro implícito, no explícito:** el bootstrap prohíbe crear memory notes durante el startup pero no dice dónde registrar el cierre de una sesión one-shot de subagente; en este loop lo resuelve el reporte en `acceptance-campaign/`, que es fuera del esquema de AGENTS OS. Un puntero del bootstrap a "cierra con el artefacto que el encargo pida" eliminaría la ambigüedad.
- **Positivo:** la disciplina "carga mínima + routing perezoso" evitó exactamente el failure mode de leer el vault entero en una sesión de 10 minutos. El dominio (skill de proyecto MKE) no existía como router y el fail-closed a DEFAULT funcionó sin fricción.
