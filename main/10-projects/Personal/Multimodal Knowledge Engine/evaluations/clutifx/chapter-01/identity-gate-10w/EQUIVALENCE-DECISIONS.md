# EQUIVALENCE-DECISIONS

**No hubo adjudicaciones semánticas en este gate.** El live gate de 10 ventanas cerró con:

```text
identity collisions (todas las clases)      = 0
semantic equivalence reviews (contador)     = 0
semantic equivalence live calls             = 0
verdicts EQUIVALENT                          = 0
verdicts DIVERGENT                           = 0
structural divergence                        = 0
deterministic equivalent accumulations       = 0
exact duplicates                             = 0
```

Por lo tanto la tabla requerida (una fila por collision semánticamente adjudicada) queda **vacía por ausencia de eventos**, no por omisión:

| Window | Claim | Canonical statement | Incoming statement | Verdict | Live/reused | Evidence before | Evidence after |
|---|---|---|---|---|---|---|---|
| (ninguna — 0 colisiones) | | | | | | | |

Contexto para el Primary Manager:

1. El incidente que motivó la remediation (w0002/w0003 proponiendo `cl-chart-instrument-eurusd@1` con contenido divergente) no se reprodujo: w0003 murió en la validación de su proposal (evidence ref inventada) sin llegar al ladder, y esta corrida produjo statements en español con un espacio de slugs diferente.
2. La máquina `claims.equivalence_review` quedó **sin ejercicio live en este gate**: no hay decisión alguna del reviewer semántico que certificar ni refutar. La única observación previa del reviewer con modelo real sigue siendo la del smoke sintético de Shot 3 y el harness adversarial (recorded).
3. Los únicos rechazos observados fueron 2 ventanas por proposals con evidence refs inventadas (validación deterministic fail-closed, sin provider call de adjudicación).
