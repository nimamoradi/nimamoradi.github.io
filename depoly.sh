#!/usr/bin/env zsh

set -euo pipefail

PROJECT_DIR=${0:A:h}
OUTPUT_DIR="$PROJECT_DIR/output"
PELICAN_BIN="$PROJECT_DIR/venv/bin/pelican"
GHP_IMPORT_BIN="$PROJECT_DIR/venv/bin/ghp-import"

rm -rf "$OUTPUT_DIR"
"$PELICAN_BIN" -s "$PROJECT_DIR/pelicanconf.py"
cp "$PROJECT_DIR/CNAME" "$OUTPUT_DIR/"
cp "$PROJECT_DIR/content/images/favicon.jpg" "$OUTPUT_DIR/"
"$GHP_IMPORT_BIN" "$OUTPUT_DIR"
git -C "$PROJECT_DIR" push origin gh-pages --force
