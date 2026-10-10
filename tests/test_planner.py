"""Tests for build_ics.py and build_sections.py.

Run from the repository root:  python -m pytest -q
Needs: pytest, icalendar, python-dateutil (see requirements-dev.txt).
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import icalendar
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
SKILLS_DIR = ROOT / "skills"
BUILD_ICS = SHARED / "build_ics.py"
BUILD_SECTIONS = SHARED / "build_sections.py"
SKILLS = ["planificador-calendario", "planificador-calendario-secciones",
          "calendar-planner", "calendar-planner-sections"]


def run(script, *args, cwd=None, pre=""):
    """Run a script in a fresh interpreter; `pre` is Python code run first."""
    code = (f"import sys; sys.argv = {[str(script), *map(str, args)]!r}; {pre}\n"
            f"sys.path.insert(0, {str(script.parent)!r})\n"
            f"import runpy; runpy.run_path({str(script)!r}, run_name='__main__')")
    return subprocess.run([sys.executable, "-c", code], capture_output=True,
                          text=True, encoding="utf-8", cwd=cwd)


def write_spec(tmp_path, spec, name="spec.json"):
    p = tmp_path / name
    p.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    return p


def parse(path):
    return icalendar.Calendar.from_ical(pathlib.Path(path).read_bytes())


# --------------------------------------------------------------- time zones
ZONES = ["America/New_York", "Europe/Madrid", "America/Santiago", "Australia/Sydney",
         "Pacific/Auckland", "Australia/Lord_Howe", "America/Lima",
         "America/Mexico_City", "Asia/Tehran", "America/Asuncion"]


@pytest.mark.parametrize("zone", ZONES)
def test_vtimezone_matches_tz_database_for_years(tmp_path, zone):
    spec = {"calendar_name": "t", "timezone": zone, "output": str(tmp_path / "t.ics"),
            "events": [
                {"title": "🎓 Block", "start": "2026-10-12T10:00", "end": "2026-10-12T11:00"},
                {"title": "💡 Bill", "date": "2026-11-03",
                 "repeat": {"freq": "MONTHLY", "bymonthday": 3}}]}
    r = run(BUILD_ICS, write_spec(tmp_path, spec))
    assert r.returncode == 0, r.stdout + r.stderr
    vtz = [c for c in parse(tmp_path / "t.ics").walk("VTIMEZONE")][0]
    from_file, real = vtz.to_tz(), ZoneInfo(zone)
    t = datetime(2025, 1, 1, tzinfo=timezone.utc)
    while t < datetime(2036, 12, 31, tzinfo=timezone.utc):
        assert t.astimezone(from_file).utcoffset() == t.astimezone(real).utcoffset(), (zone, t)
        t += timedelta(hours=11)


def test_dst_zone_uses_yearly_rules(tmp_path):
    spec = {"calendar_name": "t", "timezone": "Europe/Madrid", "output": str(tmp_path / "t.ics"),
            "events": [{"title": "x", "start": "2026-10-12T10:00", "end": "2026-10-12T11:00"}]}
    run(BUILD_ICS, write_spec(tmp_path, spec))
    text = (tmp_path / "t.ics").read_text(encoding="utf-8")
    assert "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU" in text
    assert "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU" in text


def test_clash_detected_across_dst_change(tmp_path):
    spec = {"calendar_name": "t", "timezone": "America/New_York", "output": str(tmp_path / "t.ics"),
            "range_end": "2026-11-05",
            "events": [
                {"title": "😴 Sleep", "start": "2026-10-28T23:00", "end": "2026-10-29T07:00",
                 "repeat": {"freq": "DAILY", "until": "2026-11-05"}},
                {"title": "🏃 Run", "start": "2026-11-02T06:30", "end": "2026-11-02T07:30"}]}
    r = run(BUILD_ICS, write_spec(tmp_path, spec), "--check")
    assert "1 choque" in r.stdout and "dom 01/11 23:00" in r.stdout


# ------------------------------------------------------- the 3 Phase-1 bugs
def test_sections_with_only_all_day_events(tmp_path):
    spec = {"timezone": "Europe/Madrid", "output_dir": str(tmp_path / "out"),
            "sections": [{"id": "pagos", "name": "💳 Pagos", "color": "#E67C73"}],
            "events": [{"section": "pagos", "title": "💡 Pagar la luz", "date": "2026-11-03",
                        "repeat": {"freq": "MONTHLY", "bymonthday": 3}}]}
    r = run(BUILD_SECTIONS, write_spec(tmp_path, spec))
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "out" / "1_pagos.ics").exists()


def test_missing_dateutil_is_reported(tmp_path):
    spec = {"calendar_name": "c", "timezone": "America/Lima", "output": str(tmp_path / "c.ics"),
            "range_end": "2026-10-12",
            "events": [
                {"title": "😴 Dormir", "start": "2026-10-09T23:00", "end": "2026-10-10T07:00",
                 "repeat": {"freq": "DAILY", "until": "2026-10-12"}},
                {"title": "🎓 Tesis", "start": "2026-10-11T06:00", "end": "2026-10-11T08:00"}]}
    p = write_spec(tmp_path, spec)
    assert "1 choque" in run(BUILD_ICS, p, "--check").stdout
    r = run(BUILD_ICS, p, "--check",
            pre="sys.modules['dateutil'] = None; sys.modules['dateutil.rrule'] = None")
    assert "python-dateutil" in r.stdout


def test_until_types_follow_rfc5545(tmp_path):
    spec = {"calendar_name": "u", "timezone": "America/New_York", "output": str(tmp_path / "u.ics"),
            "events": [
                {"title": "all-day", "date": "2026-11-03",
                 "repeat": {"freq": "MONTHLY", "bymonthday": 3, "until": "2027-03-03"}},
                {"title": "timed", "start": "2026-11-03T09:00", "end": "2026-11-03T10:00",
                 "repeat": {"freq": "DAILY", "until": "2026-11-10"}},
                {"title": "raw", "start": "2026-11-03T09:00", "end": "2026-11-03T10:00",
                 "repeat": {"rrule": "FREQ=WEEKLY;UNTIL=20261201"}}]}
    assert run(BUILD_ICS, write_spec(tmp_path, spec)).returncode == 0
    rules = {str(e["SUMMARY"]): e.content_line("RRULE", e["RRULE"])
             for e in parse(tmp_path / "u.ics").walk("VEVENT")}
    assert "UNTIL=20270303" in rules["all-day"] and "UNTIL=20270303T" not in rules["all-day"]
    assert re.search(r"UNTIL=20261111T045959Z", rules["timed"])
    assert re.search(r"UNTIL=20261202T045959Z", rules["raw"])


# ------------------------------------------------- portability and checks
def test_output_folder_is_created(tmp_path):
    out = tmp_path / "a" / "b" / "plan.ics"
    spec = {"calendar_name": "p", "timezone": "America/Lima", "output": str(out),
            "events": [{"title": "x", "start": "2026-10-12T10:00", "end": "2026-10-12T11:00"}]}
    assert run(BUILD_ICS, write_spec(tmp_path, spec)).returncode == 0
    assert out.exists()


def test_all_problems_reported_at_once(tmp_path):
    spec = {"calendar_name": "p", "timezone": "Mars/Olympus", "output": str(tmp_path / "p.ics"),
            "events": [{"title": "a", "start": "2026-10-12T11:00", "end": "2026-10-12T10:00"},
                       {"title": "b", "date": "2026-13-01"},
                       {"title": "c", "start": "2026-10-12T10:00", "end": "2026-10-12T11:00",
                        "repeat": {"freq": "HOURLY", "byday": ["XX"]}}]}
    r = run(BUILD_ICS, write_spec(tmp_path, spec))
    assert r.returncode == 1 and not (tmp_path / "p.ics").exists()
    for needle in ("Mars/Olympus", "posterior", "2026-13-01", "DAILY", "XX"):
        assert needle in r.stdout


def test_english_messages(tmp_path):
    spec = {"lang": "en", "calendar_name": "p", "timezone": "Europe/London",
            "output": str(tmp_path / "p.ics"),
            "events": [{"title": "📚 Study", "start": "2026-10-12T10:00", "end": "2026-10-12T11:00"}]}
    r = run(BUILD_ICS, write_spec(tmp_path, spec))
    assert "No clashes" in r.stdout and "Hours per category" in r.stdout


def test_duplicate_events_get_distinct_uids(tmp_path):
    ev = {"title": "x", "start": "2026-10-12T10:00", "end": "2026-10-12T11:00", "allow_overlap": True}
    spec = {"calendar_name": "d", "timezone": "America/Lima", "output": str(tmp_path / "d.ics"),
            "events": [ev, dict(ev)]}
    r = run(BUILD_ICS, write_spec(tmp_path, spec))
    uids = [str(e["UID"]) for e in parse(tmp_path / "d.ics").walk("VEVENT")]
    assert len(set(uids)) == 2 and "⚠️" in r.stdout


def test_no_per_event_hex_color(tmp_path):
    spec = {"timezone": "America/Lima", "output_dir": str(tmp_path),
            "sections": [{"id": "a", "name": "A", "color": "#D50000"}],
            "events": [{"section": "a", "title": "x", "start": "2026-10-12T10:00",
                        "end": "2026-10-12T11:00"}]}
    run(BUILD_SECTIONS, write_spec(tmp_path, spec))
    text = (tmp_path / "1_a.ics").read_text(encoding="utf-8")
    assert "X-APPLE-CALENDAR-COLOR:#D50000" in text and "\nCOLOR:" not in text


# ------------------------------------------------------------- split mode
def test_split_handles_lf_variation_selector_and_commas(tmp_path):
    ics = ("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//x//EN\nX-WR-TIMEZONE:Europe/Madrid\n"
           "BEGIN:VEVENT\nUID:1\nDTSTAMP:20261001T000000Z\nDTSTART:20261012T080000Z\n"
           "DTEND:20261012T090000Z\nSUMMARY:\U0001F5A5 Server setup\\, part 1\nEND:VEVENT\n"
           "BEGIN:VEVENT\nUID:2\nDTSTAMP:20261001T000000Z\nDTSTART:20261012T100000Z\n"
           "DTEND:20261012T110000Z\nSUMMARY:Call the bank\nEND:VEVENT\nEND:VCALENDAR\n")
    src = tmp_path / "plan.ics"
    src.write_text(ics, encoding="utf-8", newline="\n")
    rules = {"lang": "en", "output_dir": str(tmp_path / "out"), "default": "home",
             "sections": [
                 {"id": "tech", "name": "🖥️ Tech, tools", "color": "#8E24AA", "emojis": ["🖥️"]},
                 {"id": "errands", "name": "🏦 Errands", "color": "#F4511E", "keywords": ["bank"]},
                 {"id": "home", "name": "🏡 Home", "color": "#33B679"}]}
    r = run(BUILD_SECTIONS, "--split", src, write_spec(tmp_path, rules, "rules.json"))
    assert r.returncode == 0, r.stdout + r.stderr
    tech = parse(tmp_path / "out" / "1_tech.ics")
    raw = (tmp_path / "out" / "1_tech.ics").read_text(encoding="utf-8")
    assert "X-WR-CALNAME:🖥️ Tech\\, tools" in raw  # TEXT value, comma escaped
    assert str(tech["X-WR-TIMEZONE"]) == "Europe/Madrid"
    assert len(list(tech.walk("VEVENT"))) == 1
    assert (tmp_path / "out" / "2_errands.ics").exists()
    assert not (tmp_path / "out" / "3_home.ics").exists()


def test_split_rejects_unknown_default(tmp_path):
    rules = {"output_dir": str(tmp_path), "default": "nope",
             "sections": [{"id": "a", "name": "A", "color": "#D50000"}]}
    src = tmp_path / "p.ics"
    src.write_text("BEGIN:VCALENDAR\nEND:VCALENDAR\n", encoding="utf-8")
    r = run(BUILD_SECTIONS, "--split", src, write_spec(tmp_path, rules, "r.json"))
    assert r.returncode == 1 and "nope" in r.stdout


# --------------------------------------------------------- repository hygiene
def test_skill_copies_match_shared_scripts():
    def digest(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()
    for skill in SKILLS:
        assert digest(SKILLS_DIR / skill / "scripts" / "build_ics.py") == digest(BUILD_ICS), skill
    for skill in ("planificador-calendario-secciones", "calendar-planner-sections"):
        assert digest(SKILLS_DIR / skill / "scripts" / "build_sections.py") == digest(BUILD_SECTIONS)


# Local, git-ignored list of regexes (one per line, "#" for comments) that must
# never appear in the skills. Kept out of the repo because it holds personal data.
PRIVATE_WORDS = ROOT / "tests" / "private_words.txt"


def load_private_words():
    lines = PRIVATE_WORDS.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]


def test_no_personal_data_in_skills():
    if not PRIVATE_WORDS.exists():
        pytest.skip(f"{PRIVATE_WORDS.relative_to(ROOT)} not found; personal-data check skipped")
    FORBIDDEN = load_private_words()
    for skill in SKILLS:
        for f in (SKILLS_DIR / skill).rglob("*"):
            if f.is_file():
                text = f.read_text(encoding="utf-8")
                for pat in FORBIDDEN:
                    assert not re.search(pat, text, re.I), (f, pat)
