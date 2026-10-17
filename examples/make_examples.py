#!/usr/bin/env python3
"""
Builds the example calendars in this folder from ONE fictional week, so the
single-calendar and the by-sections versions show exactly the same plan.

Persona (fictional): works 9:00-18:00 Mon-Fri, studies a part-time master's
(online classes Tue/Thu evenings), lives in Bogota. Week: Mon 2 - Sun 8 Nov 2026.

Run from the repository root:
    python examples/make_examples.py
It writes the JSON specs and runs the real scripts in shared/.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EX = ROOT / "examples"
TZ = "America/Bogota"
END = "2026-11-08"
WEEKDAYS = ["MO", "TU", "WE", "TH", "FR"]

# (section, title, start, end, extra)
PLAN = [
    # --- routine & home
    ("routine", "😴 Sleep", "2026-11-01T23:00", "2026-11-02T07:00", {"repeat": {"freq": "DAILY", "until": "2026-11-07"}}),
    ("routine", "🍳 Breakfast & get ready", "2026-11-02T07:00", "2026-11-02T07:45", {"repeat": {"freq": "WEEKLY", "byday": WEEKDAYS, "until": END}}),
    ("routine", "🍽️ Lunch", "2026-11-02T13:00", "2026-11-02T14:00", {"repeat": {"freq": "WEEKLY", "byday": WEEKDAYS, "until": END}}),
    ("routine", "🏃 Gym", "2026-11-02T18:45", "2026-11-02T19:30", {}),
    ("routine", "🍽️ Dinner", "2026-11-02T19:30", "2026-11-02T20:15", {}),
    ("routine", "🍽️ Dinner", "2026-11-03T18:45", "2026-11-03T19:25", {"repeat": {"freq": "WEEKLY", "byday": ["TU", "WE", "TH"], "until": END}}),
    ("routine", "🏃 Morning run", "2026-11-07T08:00", "2026-11-07T08:45", {}),
    ("routine", "🍳 Breakfast", "2026-11-07T08:45", "2026-11-07T09:15", {}),
    ("routine", "🧹 House cleaning", "2026-11-07T14:00", "2026-11-07T15:00", {}),
    # --- work
    ("work", "🚌 Commute to office", "2026-11-02T08:15", "2026-11-02T09:00", {"repeat": {"freq": "WEEKLY", "byday": WEEKDAYS, "until": END}}),
    ("work", "💼 Work", "2026-11-02T09:00", "2026-11-02T13:00", {"repeat": {"freq": "WEEKLY", "byday": WEEKDAYS, "until": END}}),
    ("work", "💼 Work", "2026-11-02T14:00", "2026-11-02T18:00", {"repeat": {"freq": "WEEKLY", "byday": ["MO", "TU", "WE", "TH"], "until": END}}),
    ("work", "💼 Work (short Friday)", "2026-11-06T14:00", "2026-11-06T17:30", {}),
    ("work", "🚌 Commute home", "2026-11-02T18:00", "2026-11-02T18:45", {"repeat": {"freq": "WEEKLY", "byday": ["MO", "TU", "WE", "TH"], "until": END}}),
    ("work", "🚌 Commute home", "2026-11-06T18:30", "2026-11-06T19:15", {}),
    # --- master's (priority)
    ("masters", "🎓 Statistics assignment (block 1)", "2026-11-02T20:15", "2026-11-02T21:45", {"description": "Data cleaning and exploratory analysis. Assignment due Fri Nov 6, 23:59."}),
    ("masters", "🎓 Online class: Machine Learning", "2026-11-03T19:30", "2026-11-03T21:30", {"alarm_min": 10}),
    ("masters", "🎓 FINISH statistics assignment (block 2)", "2026-11-04T19:30", "2026-11-04T21:30", {"description": "Final model, write-up and submission. Two days of margin before the deadline.", "alarm_min": 10}),
    ("masters", "🎓 Online class: Research Methods", "2026-11-05T19:30", "2026-11-05T21:30", {"alarm_min": 10}),
    ("masters", "🎓 Readings for next week", "2026-11-07T10:30", "2026-11-07T12:30", {"description": "Chapters 4-5 + notes."}),
    ("masters", "🎓 Deep study: ML exercises", "2026-11-08T10:00", "2026-11-08T11:30", {}),
    # --- errands (uncertain date -> option A / option B)
    ("errands", "🏦 Bank: renew debit card (option A)", "2026-11-06T17:45", "2026-11-06T18:30",
     {"description": "Bring ID. If you go on Saturday instead, this slot becomes free time.", "location": "Bank branch near the office"}),
    ("errands", "🏦 Bank: renew debit card (option B)", "2026-11-07T09:30", "2026-11-07T10:15",
     {"description": "Only if option A did not happen. If it is not needed, use it for the master's readings."}),
    # --- organization
    ("organization", "📋 Weekly review", "2026-11-08T18:00", "2026-11-08T18:30", {"description": "What got done, what moves, ask Claude to adjust the plan."}),
    ("organization", "🗂️ Plan next week", "2026-11-08T18:30", "2026-11-08T19:00", {}),
    # --- flexible slots (about one per day; Friday and Sunday afternoon stay light)
    ("flexible", "🔄 Flexible slot", "2026-11-02T21:45", "2026-11-02T22:15", {}),
    ("flexible", "🔄 Flexible slot", "2026-11-03T21:30", "2026-11-03T22:00", {}),
    ("flexible", "🔄 Flexible slot", "2026-11-04T21:30", "2026-11-04T22:15", {}),
    ("flexible", "🔄 Flexible slot", "2026-11-05T21:30", "2026-11-05T22:00", {}),
    ("flexible", "🔄 Flexible slot", "2026-11-07T15:00", "2026-11-07T16:00", {}),
    ("flexible", "🔄 Flexible slot", "2026-11-08T11:30", "2026-11-08T12:15", {}),
]

REMINDERS = [
    ("payments", "🏠 Pay rent", None, None, {"date": "2026-11-01", "repeat": {"freq": "MONTHLY", "bymonthday": 1}}),
    ("payments", "🔔 Tomorrow: pay rent", None, None, {"date": "2026-11-30", "repeat": {"freq": "MONTHLY", "bymonthday": -1}}),
    ("payments", "💡 Pay electricity bill", None, None, {"date": "2026-11-05", "repeat": {"freq": "MONTHLY", "bymonthday": 5}}),
    ("maintenance", "🧊 Clean the fridge", "2026-11-07T15:00", "2026-11-07T15:45",
     {"repeat": {"freq": "DAILY", "interval": 30}, "allow_overlap": True}),
    ("maintenance", "🚰 Change water filter", None, None, {"date": "2026-11-14", "repeat": {"freq": "DAILY", "interval": 90}}),
]

SECTIONS = [
    {"id": "masters", "name": "🎓 Master's", "color": "#D50000", "color_name": "Tomato"},
    {"id": "work", "name": "💼 Work", "color": "#3F51B5", "color_name": "Blueberry"},
    {"id": "errands", "name": "🏦 Errands", "color": "#F4511E", "color_name": "Tangerine"},
    {"id": "organization", "name": "🗂️ Organization", "color": "#039BE5", "color_name": "Peacock"},
    {"id": "routine", "name": "🏡 Routine & home", "color": "#33B679", "color_name": "Sage"},
    {"id": "flexible", "name": "🔄 Flexible slots", "color": "#616161", "color_name": "Graphite"},
]
REMINDER_SECTIONS = [
    {"id": "payments", "name": "💳 Payments", "color": "#E67C73", "color_name": "Flamingo"},
    {"id": "maintenance", "name": "🧽 Maintenance", "color": "#0B8043", "color_name": "Basil"},
]


def events(rows, with_section):
    out = []
    for sec, title, start, end, extra in rows:
        ev = {"title": title}
        if with_section:
            ev["section"] = sec
        if start:
            ev.update(start=start, end=end)
        ev.update(extra)
        out.append(ev)
    return out


def write(path, spec):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def run(script, *args):
    print(f"\n$ python {script.relative_to(ROOT)} {' '.join(str(a) for a in args)}", flush=True)
    subprocess.run([sys.executable, str(script), *map(str, args)], cwd=ROOT, check=True)


def main():
    ics, sections = ROOT / "shared" / "build_ics.py", ROOT / "shared" / "build_sections.py"
    base = {"lang": "en", "timezone": TZ}

    single = EX / "single-calendar"
    run(ics, write(single / "spec_plan.json", {**base, "calendar_name": "Plan Nov 2-8",
        "output": "examples/single-calendar/plan_nov_2-8.ics", "range_end": END,
        "events": events(PLAN, False)}).relative_to(ROOT))
    run(ics, write(single / "spec_reminders.json", {**base, "calendar_name": "🔔 Reminders",
        "output": "examples/single-calendar/reminders.ics",
        "events": events(REMINDERS, False)}).relative_to(ROOT))

    by_sec = EX / "by-sections"
    run(sections, write(by_sec / "spec_plan.json", {**base, "calendar_name": "Plan Nov 2-8",
        "output_dir": "examples/by-sections/plan", "range_end": END, "sections": SECTIONS,
        "events": events(PLAN, True)}).relative_to(ROOT))
    run(sections, write(by_sec / "spec_reminders.json", {**base,
        "output_dir": "examples/by-sections/reminders", "sections": REMINDER_SECTIONS,
        "events": events(REMINDERS, True)}).relative_to(ROOT))

    split = EX / "split-existing"
    rules = {"lang": "en", "output_dir": "examples/split-existing/out", "default": "routine",
             "sections": [dict(s, emojis=e) for s, e in zip(SECTIONS, [
                 ["🎓"], ["💼", "🚌"], ["🏦"], ["📋", "🗂"], [], ["🔄"]])]}
    run(sections, "--split", "examples/single-calendar/plan_nov_2-8.ics",
        write(split / "rules.json", rules).relative_to(ROOT))


if __name__ == "__main__":
    main()
