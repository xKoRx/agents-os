#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DISTRIBUTION_DIR="$VAULT_ROOT/30-resources/agents-os/distribution"
ZIP_PATH="$DISTRIBUTION_DIR/agents-os-chatgpt.zip"
SOURCES_LIST="$SCRIPT_DIR/sources.list"
BASE_LIST="$SCRIPT_DIR/base-components.list"

hash_file() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    sha256sum "$1" | awk '{print $1}'
  fi
}

file_size() {
  wc -c < "$1" | tr -d ' '
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
OUTPUT_DIR="$tmp_dir/agents-os-chatgpt"
worklist="$tmp_dir/worklist.tsv"
deduped="$tmp_dir/worklist-deduped.tsv"
: > "$worklist"

add_file() {
  local category="$1"
  local rel="$2"
  local source="$VAULT_ROOT/$rel"
  if [[ ! -f "$source" ]]; then
    echo "Missing required source: $rel" >&2
    exit 1
  fi
  printf '%s\t%s\n' "$category" "$rel" >> "$worklist"
}

add_tree() {
  local category="$1"
  local root="$2"
  local source
  while IFS= read -r -d '' source; do
    [[ "$(basename "$source")" == ".DS_Store" ]] && continue
    printf '%s\t%s\n' "$category" "${source#"$VAULT_ROOT/"}" >> "$worklist"
  done < <(find "$root" -type f -print0 | sort -z)
}

while IFS='|' read -r mode category rel; do
  [[ -z "${mode:-}" || "$mode" == \#* ]] && continue
  case "$mode" in
    file)
      add_file "$category" "$rel"
      ;;
    tree)
      [[ -d "$VAULT_ROOT/$rel" ]] || { echo "Missing source tree: $rel" >&2; exit 1; }
      add_tree "$category" "$VAULT_ROOT/$rel"
      ;;
    globtree)
      matched=0
      for root in "$VAULT_ROOT"/${rel}; do
        [[ -d "$root" ]] || continue
        matched=1
        add_tree "$category" "$root"
      done
      [[ "$matched" -eq 1 ]] || { echo "Source glob matched nothing: $rel" >&2; exit 1; }
      ;;
    *)
      echo "Unknown selection mode: $mode" >&2
      exit 1
      ;;
  esac
done < "$SOURCES_LIST"

awk -F '\t' '!seen[$2]++' "$worklist" | sort -t $'\t' -k2,2 > "$deduped"

mkdir -p "$DISTRIBUTION_DIR"
mkdir -p "$OUTPUT_DIR/sources"
cp "$SCRIPT_DIR/README.md" "$OUTPUT_DIR/README.md"
cp "$SCRIPT_DIR/PROJECT-STATE.md" "$OUTPUT_DIR/PROJECT-STATE.md"
cp "$SCRIPT_DIR/ITERATION-PROMPT.md" "$OUTPUT_DIR/ITERATION-PROMPT.md"

manifest="$OUTPUT_DIR/MANIFEST.md"
{
  echo "# AGENTS OS ChatGPT Pack — Manifest"
  echo
  echo "- **Generated:** $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "- **Vault:** source vault at build time"
  echo "- **Authority:** generated snapshot; canonical paths are listed below."
  echo
  echo "| Category | Canonical source | Packaged copy | Bytes | SHA-256 |"
  echo "|---|---|---|---:|---|"
} > "$manifest"

count=0
total_bytes=0
while IFS=$'\t' read -r category rel; do
  source="$VAULT_ROOT/$rel"
  dest="$OUTPUT_DIR/sources/$rel"
  mkdir -p "$(dirname "$dest")"
  cp -p "$source" "$dest"
  source_hash="$(hash_file "$source")"
  dest_hash="$(hash_file "$dest")"
  [[ "$source_hash" == "$dest_hash" ]] || { echo "Hash mismatch: $rel" >&2; exit 1; }
  bytes="$(file_size "$source")"
  printf '| %s | `%s` | `sources/%s` | %s | `%s` |\n' \
    "$category" "$rel" "$rel" "$bytes" "$source_hash" >> "$manifest"
  count=$((count + 1))
  total_bytes=$((total_bytes + bytes))
done < "$deduped"

base_bundle="$OUTPUT_DIR/AGENTS-OS-BASE-COMPONENTS.md"
{
  echo "# AGENTS OS — Componentes base verbatim"
  echo
  echo "> Archivo generado. Cada bloque conserva el contenido exacto de su fuente"
  echo "> canónica al momento del snapshot. Los delimitadores no forman parte de la fuente."
  echo
  while IFS= read -r rel; do
    [[ -z "$rel" || "$rel" == \#* ]] && continue
    source="$VAULT_ROOT/$rel"
    [[ -f "$source" ]] || { echo "Missing base component: $rel" >&2; exit 1; }
    echo
    echo "<!-- ===== BEGIN CANONICAL FILE: $rel ===== -->"
    echo
    cat "$source"
    echo
    echo "<!-- ===== END CANONICAL FILE: $rel ===== -->"
  done < "$BASE_LIST"
} > "$base_bundle"

if grep -R -n -E 'sources/80-agents/(memory/internal|journal)/' "$manifest" >/dev/null; then
  echo "Private/internal or journal content leaked into pack" >&2
  exit 1
fi

{
  echo
  echo "## Build summary"
  echo
  echo "- Files copied: $count"
  echo "- Canonical source bytes: $total_bytes"
  echo "- Consolidated base bytes: $(file_size "$base_bundle")"
  echo "- Internal memory included: no"
  echo "- Journal included: no"
  echo "- Hash validation: passed"
} >> "$manifest"

build_info="$OUTPUT_DIR/BUILD-INFO.md"
{
  echo "# Build information"
  echo
  echo "- Generated: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "- Files: $count"
  echo "- Source bytes: $total_bytes"
  echo "- Builder: \`30-resources/agents-os/chatgpt-pack/build-pack.sh\`"
  echo "- Selection: \`30-resources/agents-os/chatgpt-pack/sources.list\`"
  echo "- Validation: source/copy SHA-256 equality for every file"
} > "$build_info"

rm -f "$ZIP_PATH"
(
  cd "$tmp_dir"
  zip -qry "$ZIP_PATH" "$(basename "$OUTPUT_DIR")"
)
unzip -tq "$ZIP_PATH" >/dev/null

echo "Pack staging:   temporary (removed after validation)"
echo "Pack archive:   $ZIP_PATH"
echo "Files copied:   $count"
echo "Validation:     passed"
