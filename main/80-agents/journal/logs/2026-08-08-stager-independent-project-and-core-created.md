---
type: change_log
scope: public
tags:
  - kind/changelog
  - scope/public
  - area/echo
  - tech/deployment
created: 2026-08-08
updated: 2026-08-08
entities:
  - "[[Stager]]"
  - "[[stager-app]]"
  - "[[Echo Forge]]"
  - "[[Echo Forge - Cross-Platform Stager]]"
---

# Stager independent project and core created

## Cambio

- Se creó [[Stager]] como proyecto de agente y planificador único del nuevo repositorio independiente `github.com/xKoRx/stager`.
- Se creó el repositorio Git local con módulo Go, SDD mínimo, CLI, adapter MinIO, manifest tipado, staging verificado, lock cross-process Unix/Windows y protocolo recuperable `PENDING.next → CURRENT → PENDING`.
- [[Echo Forge]] recibió su única tarea puente y quedó en Review.
- [[Echo Forge - Cross-Platform Stager]] se marcó como precursor parcialmente supersedido donde proponía código dentro de Symphony y `ACTIVATION.json`.
- Se creó [[stager-app]] desde el template de application y se reconcilió el índice curado a sus 17 applications reales, incorporando dos entradas antiguas omitidas.
- La validación externa sin acceso al código aprobó continuar integración (~9/10). Se incorporaron su wording correcto de migración aditiva, el gate explícito de completitud multi-plataforma y el freno a nuevo diseño antes del E2E.

## Evidencia

- `go test ./...`: PASS.
- `go vet ./...`: PASS.
- Build `linux-amd64`: PASS.
- Build `windows-amd64`: PASS.
- Sin imports Go de Symphony y sin secretos hardcodeados detectados.
- Symphony no fue modificado; stager Bash y deployment legacy siguen disponibles.
- Lint canónico: 0 errores en proyecto, parent, precursor y change log.
- Graphify: 13.821 nodos, 13.836 aristas; query `Independent Stager` recupera el proyecto y sus slices.

## Decisiones

- MinIO es el único source productivo del MVP.
- El Stager sigue siendo one-shot y no supervisa workers.
- El estado local mínimo excluye DB, journal general, PREVIOUS y RUNNING.
- No se creó remote GitHub ni commit: visibilidad, ownership y publicación quedan para decisión explícita del owner.
- El repo ya está en el nivel solicitado, hermano de Symphony/Echo/SDK: `~/go/src/github.com/xKoRx/stager`.
