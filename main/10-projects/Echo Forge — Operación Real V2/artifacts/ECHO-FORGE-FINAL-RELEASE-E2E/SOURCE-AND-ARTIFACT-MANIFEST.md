# SOURCE-AND-ARTIFACT-MANIFEST — Release 0.3.2 (2026-10-19)

## Provenance

- Versión resuelta por la autoridad real (`cmd/release-authority`, modo AUTO de `deploy_release.sh`): **0.3.2** (0.3.1 publicada e inmutable; no sobrescrita).
- Source: master `619c3b6f71a0d8198783a7ab5684767b6ddf15d9`, árbol limpio al compilar, checkout canónico `/home/kor/go/src/github.com/xKoRx/symphony`.
- Build: `deploy_sqx.sh` — linux symphony + sqx-watcher, windows sqx-mt5-worker.exe, `vcs.modified=false` verificado con `go version -m` en linux y windows (`vcs.revision=619c3b6f…`, `vcs.time=2026-10-19T16:35:53Z`).
- Manifest publicado en MinIO (`worker/sqx/manifest.json` v0.3.2) con confirmación del deployer-watcher; **modo `--release-only`**: sin bump de input, sin FlowRun, sin watcher de delivery.
- Commit de cierre: `daded14cbe0bc85f6fafda8d079e94036f715b47` (manifest 0.3.2, documental).

## SHA256 de artefactos (manifest == local, verificado byte-exacto)

- linux-amd64 `bin/symphony`: `6abfb00bb8e310cb54d6e673e7d1711eb09b25ffa5dfd7547a4504eb21613491`
- linux-amd64 `bin/sqx-watcher`: `491d3894a39153c28da302892acada82e1d850612eb088f18d99e5a2cad0c285`
- linux-amd64 `bin/start-symphony-worker.sh`: `9f95638441dcb1d60d5c9475f0f95755dd48a09528c326b2ce36063b7ff50849`
- linux-amd64 `bin/run-symphony`: `8f240eb20a17d70c22512a6f6f689591f7078c7a8ee23b210aaf766bc459c062`
- linux-amd64 `etc/promtail-worker.yaml`: `eaa4e1b21ace4d34202ff6185b9c76710a6ff48274d4d57ba752ea13e532cbd9`
- windows-amd64 `bin/sqx-mt5-worker.exe`: `c65e4f5d098bab29f9448a4423c5518e41219bc6c8570781b358209b30e6313c`

## Limitación del verificador automático

`scripts/verify_rollout.sh` (SSH BatchMode) falla desde Daedalus por claves — preexistente documentado desde 0.2.147 y repetido en 0.3.0/0.3.1. El script terminó `Release PUBLICADA; rollout NO VERIFICADO (0/3)`; la verificación física 4/4 se ejecutó por el canal autorizado con credencial (ver `PHYSICAL-ROLLOUT-4OF4.md`).

## Sin empaquetado de basura

Artefactos = los 6 archivos del manifest; sin temporales, credenciales ni outputs de campaña en el paquete. 0.3.0 permanece cuarentenada (bitácora), 0.3.1 inmutable.
