#!/usr/bin/env sh
# Copy the single source of truth (shared/) into every skill folder.
set -e
cd "$(dirname "$0")"
for s in planificador-calendario calendar-planner; do
  cp shared/build_ics.py "skills/$s/scripts/"
done
for s in planificador-calendario-secciones calendar-planner-sections; do
  cp shared/build_ics.py shared/build_sections.py "skills/$s/scripts/"
done
echo "scripts synced"
