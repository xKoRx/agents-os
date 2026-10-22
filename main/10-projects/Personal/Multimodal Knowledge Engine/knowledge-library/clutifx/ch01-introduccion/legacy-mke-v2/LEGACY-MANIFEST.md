# LEGACY — MKE V2 run (ch01-introduccion)

Este directorio preserva INTACTO el resultado del run MKE V2 original sobre
`ep01-intro.mp4` (2026-10-14/16, abortado por costo: 44 h para 34 min de video),
publicado como biblioteca el 2026-10-17. NO es conocimiento activo V1.2: se
conserva como historia y material de contraste.

- Motor: MKE V2 completo (ventanas wNNNN, granularidad por ventana, revisión por
  claim — el contrato que la skill `course-knowledge-extraction` prohíbe).
- Registros totales en claims.jsonl: 1.894 (130 WINDOWS + 1.527 CLAIMS + 367
  RELATIONS). Grounding al abortar: 1.140 SUPPORTED / 38 INSUFFICIENT / 22
  CONTRADICTED / 694 UNREVIEWED (REVIEWED = 1.200/1.894).
- Los IDs `wNNNN`/`c-NNNN` de este archivo NO son IDs activos V1.2; la biblioteca
  activa usa su propio espacio de IDs.
- No convertir automáticamente los GROUNDING_SUPPORTED a SUPPORTED V1.2: los
  contratos de validación son distintos.

## SHA-256 de los archivos preservados (verificados al moverlos, 2026-10-22)

| Archivo | SHA-256 |
|---|---|
| README.md | `f6ec3b68517f61a73d5259a89bc75530b96dc64d9c42bb2a922e30b920b4b209` |
| claims.jsonl | `5bdcb6bca8bcfc41296817b723da7db52e62491e7ce82fc0d5e3f294745fb2db` |
| documentation.md | `8a2f732750f887a0ccc7154f572d6cb6289621d5b4c554847c591d35f2e5bfae` |

Enlaces entrantes verificados antes de mover: COURSE-INDEX.md y GLOSSARY.md del
curso (actualizados en la misma migración para apuntar aquí como legado),
ch02-time/README.md (mención histórica), skill course-knowledge-extraction
(mención histórica del run caro). Los dos primeros apuntan ahora a la biblioteca
activa V1.2; el legado se referencia como tal.
