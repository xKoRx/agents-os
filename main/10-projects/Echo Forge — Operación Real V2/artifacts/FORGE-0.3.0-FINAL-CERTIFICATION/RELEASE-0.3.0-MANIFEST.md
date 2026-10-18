# RELEASE-0.3.0-MANIFEST — Echo Forge (2026-10-18)

## Resumen

La release **0.3.0 fue publicada en MinIO pero queda CUARENTENADA por defecto de provenance**; la release canónica de este ciclo es **0.3.1**, construida desde master limpio con `vcs.modified=false` y desplegada físicamente 4/4. La inmutabilidad de 0.3.0 se respetó: NO se re-publicaron sus objetos.

## 0.3.0 — PUBLICADA Y CUARENTENADA (bitácora)

- Manifest MinIO confirmado: `worker/sqx/manifest.json` version=0.3.0, source SHA `d67244bb334840b8e7fd4cc158a49a68fa49fc54` (contenido funcional correcto).
- **Defecto**: los 3 binarios salieron con `vcs.modified=true`. Causa raíz demostrada por repro: Go buildvcs cuenta archivos UNTRACKED como dirty; `sqx/exporter-plugin/target/` (salida del build del plugin, aún no gitignored en ese momento) ensuciaba el stamp. El source era exactamente d67244b; el delta es sólo el flag de provenance.
- **Decisión**: el gate §6 exige `vcs.modified=false` y 0.3.0 es inmutable (prohibido sobrescribir objetos publicados). Doctrina del repo ([[forge-wave-dispatch]] §5): "release con vcs.modified=true → corta una release nueva limpia; la sucia queda en la bitácora". Se cortó 0.3.1.
- SHAs de la 0.3.0 cuarentenada: linux symphony `1b0842476cd339f4755f3f63e08ee480a550ebf0a362d511b909aac7b10bf8ec`; windows sqx-mt5-worker.exe `84d9d6139e46a470b09c45304325398e60dba587a00066817ca5522b6cb9f9d0`; watcher `3cf08138dcd32c3f488b46e2a03f5c41c1f0bd3425cf0217a86d49831b0c36c1`.

## 0.3.1 — CANÓNICA (en uso)

- Source SHA: `66dd8cdbfc144e82553cf69cb79f438f4775eebe` (master; d67244b + gitignore).
- `vcs.modified=false` **verificado en los 3 binarios** con `go version -m`.
- linux-amd64/symphony: SHA256 `a4117aac3391fe6bc5615bc24771bd696ccc857bf73f94a2d37dc068f1212e28` (40.8 MB).
- linux-amd64/sqx-watcher: `c2b883e2f578d921a4de756b041e47e157680f07c0f3a4fdc9a711b90f56a4b3`.
- windows-amd64/sqx-mt5-worker.exe: `6c7b08f26e789dfd652fb9e3c6b23cb30e6826bf3b87664f90e2b52f71653bac` (37.5 MB).
- Manifest publicado en MinIO `worker/sqx/manifest.json` confirmado por el deployer-watcher ("MinIO confirmó manifest v0.3.1"); commit canónico del manifest `492a271` pusheado.
- Mecanismo oficial: `./deploy_release.sh --release-only 0.3.1` (sin dispatch de flujo). release-authority previo: published 0.2.147, CONSISTENT; 0.3.x estaba libre.
- Release-authority post: 0.3.1 es la published version vigente.

## Plugin SQX (fuera del manifest Go — deploy paralelo certificado)

- `EchoForgeAutomator.jar` nuevo (fuente `d67244b`): SHA256 `3b0063e43735f9457f71c0c4208f060777cc5a3828ec4145b261b38d37ad847c`, 52 clases, uniforme 3/3 hosts en `/home/kor/sqx/144/user/libs/` (backups `.bak-20261018`).
- Snippet fuente actualizado 3/3 (`/home/kor/sqx/144/user/extend/Snippets/SQ/CustomAnalysis/EchoForgeMT5Exporter.java`, SHA `1599f1bedffaca61deb6ad5106ce7607e8ed8b00499921c234c3a349b1b0d0cb`; **el snippet es la autoridad efectiva en Build 144 headless: sqcli lo recompila por corrida y pisa la clase del JAR** — hallazgo de precedencia de esta sesión).
- Backups: JAR previo `323d1cb8…` (Zeus) / per-host SHAs divergentes; snippet previo `c9710bd9…`.

## Nota de verificación de rollout

`scripts/verify_rollout.sh` (SSH keyless kor) falla desde Daedalus por claves (preexistente, documentado desde 0.2.147). La verificación física 4/4 se hizo por el canal MCP/SSH autorizado (perfil operator/admin): proceso + ruta + SHA256 byte-exacto por host. Limitación del verificador automático dejada explícita.
