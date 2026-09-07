#!/usr/bin/env bash
# Sistema de sincronización automática del repo agents-os.
# Corre cada 1 minuto vía cron y está diseñado para el peor caso:
# cambios locales y cambios remotos al mismo tiempo.
#
# Política de colisiones:
#   1. commit local primero (sync HH:MM)
#   2. rebase sobre origin/master
#   3. si hay conflicto de contenido: merge -X ours (gana lo local,
#      los archivos nuevos del remoto entran igual)
#   4. último recurso: respaldar el remoto en un branch conflict-<fecha>
#      y avanzar con lo local (nunca se pierde nada, nunca force-push)
set -u
cd "$(dirname "$0")" || exit 1

BRANCH="master"
LOG=".sync/sync.log"
LOCK=".sync/sync.lock"

mkdir -p .sync
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

if [ ! -d .git ]; then
  log "ERROR: no hay .git en $(pwd)"
  exit 1
fi

# un solo sync a la vez; si hay otro corriendo, este ciclo no hace nada
exec 9>>"$LOCK"
flock -n 9 || exit 0

git fetch origin "$BRANCH" --quiet 2>>"$LOG" || {
  log "fetch falló (¿sin red?); se reintenta el próximo ciclo"
  exit 0
}

commit_local() {
  git add -A
  git diff --cached --quiet && return 1
  local msg="sync $(date +%H:%M)"
  git commit -m "$msg" --quiet 2>>"$LOG" || return 1
  log "commit local: $msg"
  return 0
}

integrate_remote() {
  # solo atrás: fast-forward limpio, sin conflictos posibles
  if git merge-base --is-ancestor HEAD "origin/$BRANCH" 2>/dev/null; then
    if git merge --ff-only "origin/$BRANCH" --quiet 2>>"$LOG"; then
      log "fast-forward a origin/$BRANCH"
      return 0
    fi
  fi

  # divergido: rebase primero
  if git rebase "origin/$BRANCH" --quiet 2>>"$LOG"; then
    log "rebase sobre origin/$BRANCH ok"
    return 0
  fi
  git rebase --abort 2>/dev/null

  # conflicto de contenido: merge con preferencia local
  if git merge -X ours --no-edit -m "sync-merge $(date +%H:%M) (conflicto: gana local)" "origin/$BRANCH" 2>>"$LOG"; then
    log "merge -X ours tras conflicto de rebase"
    return 0
  fi
  git merge --abort 2>/dev/null

  # último recurso: preservar el remoto en un branch y avanzar con lo local
  local stamp remote_sha
  stamp="$(date +%Y%m%d-%H%M%S)"
  remote_sha="$(git rev-parse "origin/$BRANCH" 2>/dev/null || true)"
  if [ -n "$remote_sha" ] && git push origin "$remote_sha:refs/heads/conflict-$stamp" --quiet 2>>"$LOG" \
    && git merge -s ours --no-edit -m "sync-merge $(date +%H:%M) (conflicto duro: remoto preservado en conflict-$stamp)" "origin/$BRANCH" 2>>"$LOG"; then
    log "conflicto duro: remoto respaldado en conflict-$stamp; se avanza con lo local"
    return 0
  fi
  git merge --abort 2>/dev/null
  log "ERROR: no se pudo integrar origin/$BRANCH"
  return 1
}

push_remote() {
  local i
  for i in 1 2 3; do
    if git push origin "$BRANCH" --quiet 2>>"$LOG"; then
      log "push ok"
      return 0
    fi
    log "push rechazado (intento $i); re-integrando"
    git fetch origin "$BRANCH" --quiet 2>>"$LOG" || return 1
    if ! git merge-base --is-ancestor "origin/$BRANCH" HEAD 2>/dev/null; then
      integrate_remote || return 1
    fi
    sleep 2
  done
  log "ERROR: push no pudo completarse"
  return 1
}

commit_local

REMOTE_SHA="$(git rev-parse "origin/$BRANCH" 2>/dev/null || true)"
LOCAL_SHA="$(git rev-parse HEAD 2>/dev/null || true)"

if [ -n "$REMOTE_SHA" ] && [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
  integrate_remote || exit 1
fi

# pushear solo si hay algo que pushear (o si el remoto aún no existe)
if [ -z "$REMOTE_SHA" ] || [ -n "$(git log "origin/$BRANCH..HEAD" --oneline 2>/dev/null)" ]; then
  push_remote
fi
