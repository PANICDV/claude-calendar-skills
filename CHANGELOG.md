# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
uses [Semantic Versioning](https://semver.org/).

## [1.0.0] - unreleased

### Added
- Four Claude skills: `planificador-calendario` and `planificador-calendario-secciones`
  (Spanish) and `calendar-planner` and `calendar-planner-sections` (English).
- Shared engine in `shared/` (`build_ics.py`, `build_sections.py`) with `sync_scripts.sh`
  to copy it into every skill.
- Clash detection across recurring events, hours per category, correct VTIMEZONE with
  daylight-saving rules, clear error messages, and Windows console support.
- `--split` mode to color-code an existing .ics by section.
- Test suite (pytest) and GitHub Actions on Linux and Windows.
- `examples/`: one fictional week as a single calendar, by sections, and split from an
  existing .ics, generated with `examples/make_examples.py`.
