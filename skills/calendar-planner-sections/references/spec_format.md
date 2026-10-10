# Spec formats

Paths in the examples are the claude.ai ones (`/mnt/user-data/outputs`). In any other
environment, use its output folder; the script creates the folder if it does not exist.

## Mode 1: new plan by sections (`build_sections.py spec.json`)

```json
{
  "lang": "en",
  "calendar_name": "Plan Oct 3–11",
  "timezone": "America/New_York",
  "output_dir": "/mnt/user-data/outputs",
  "range_end": "2026-10-11",
  "combined": false,
  "sections": [
    {"id": "thesis",   "name": "🎓 Thesis",                "color": "#D50000", "color_name": "Tomato"},
    {"id": "tech",     "name": "🖥️ Server · AI tools",      "color": "#8E24AA", "color_name": "Grape"},
    {"id": "errands",  "name": "🏦 Banks and errands",      "color": "#F4511E", "color_name": "Tangerine"},
    {"id": "routine",  "name": "🏡 Routine and home",       "color": "#33B679", "color_name": "Sage"},
    {"id": "flexible", "name": "🔄 Flexible slots",         "color": "#616161", "color_name": "Graphite"}
  ],
  "events": [
    {"section": "routine", "title": "😴 Sleep", "start": "2026-10-02T23:00", "end": "2026-10-03T07:00",
     "repeat": {"freq": "DAILY", "until": "2026-10-11"}},
    {"section": "thesis", "title": "🎓 Thesis: slides (block 1)",
     "start": "2026-10-03T10:00", "end": "2026-10-03T12:30", "description": "Full structure."},
    {"section": "flexible", "title": "🔄 Flexible slot",
     "start": "2026-10-03T18:15", "end": "2026-10-03T19:30"}
  ]
}
```

| Field | Notes |
|---|---|
| `lang` | Language of the script's messages and of the combined file name: `en` or `es` (default `es`). Always use `en` in this version. |
| `sections` | In the order the files are numbered (`1_thesis.ics`, `2_tech.ics`…). Keep the same order and `id` in updates. |
| `id` | Lowercase, no spaces or accents (`a-z`, `0-9`, `_`, `-`): it is part of the file name. |
| `name` | Calendar name, with emoji. |
| `color` / `color_name` | Hex `#RRGGBB` and palette name (see `sections.md`). |
| `combined` | `true` → also writes `all_in_one.ics`, for anyone who wants everything in one calendar. |
| `events[].section` | Required; must match an `id`. |

The other event fields (`start`/`end` in local time without a zone and in 24-hour format,
`date`/`end_date` for all-day events, `repeat`, `alarm_min`, `description`, `location`,
`allow_overlap`) work the same as in the single-calendar planner:

| Need | `repeat` |
|---|---|
| Every day until Oct 11 | `{"freq": "DAILY", "until": "2026-10-11"}` |
| Monday to Friday | `{"freq": "WEEKLY", "byday": ["MO","TU","WE","TH","FR"], "until": "2026-10-09"}` |
| Every 30 days | `{"freq": "DAILY", "interval": 30}` |
| The 3rd of each month | `{"freq": "MONTHLY", "bymonthday": 3}` |
| Last day of each month | `{"freq": "MONTHLY", "bymonthday": -1}` |
| Once a year (March 15) | `{"freq": "YEARLY", "bymonth": 3, "bymonthday": 15}` |
| Free-form rule | `{"rrule": "FREQ=MONTHLY;BYDAY=1MO"}` |

`until` is an inclusive local date. Without `until` or `count` the repetition is endless,
which is right for reminders.

### Reminders
Use a second JSON with the same format and its own sections, for example:

```json
{"lang": "en", "timezone": "America/New_York", "output_dir": "/mnt/user-data/outputs/reminders",
 "sections": [
   {"id": "bills", "name": "💳 Bills", "color": "#E67C73", "color_name": "Flamingo"},
   {"id": "maintenance", "name": "🧽 Maintenance", "color": "#0B8043", "color_name": "Basil"}],
 "events": [
   {"section": "bills", "title": "💡 Pay electricity bill", "date": "2026-11-03", "repeat": {"freq": "MONTHLY", "bymonthday": 3}},
   {"section": "maintenance", "title": "🧊 Clean the fridge", "start": "2026-10-10T10:00",
    "end": "2026-10-10T10:45", "repeat": {"freq": "DAILY", "interval": 30}}]}
```
So that reminder files do not clash with the plan's numbering, use another output folder
(as in the example) or different `id`s. A JSON with only all-day events is valid.

### Validation
Before writing, the script checks the JSON and lists **every** problem at once (unknown zone,
invalid date, end before start, `id` with spaces or repeated, color that is not hex, an event
whose `section` does not exist). If there is any, no files are written: fix and run again.
With `--check` it only validates and shows the table.

## Mode 2: split an existing .ics (`--split plan.ics rules.json`)

```json
{
  "lang": "en",
  "output_dir": "/mnt/user-data/outputs",
  "default": "routine",
  "sections": [
    {"id": "thesis",   "name": "🎓 Thesis",           "color": "#D50000", "color_name": "Tomato",
     "emojis": ["🎓", "🎤"], "keywords": ["thesis", "committee"]},
    {"id": "errands",  "name": "🏦 Banks and errands", "color": "#F4511E", "color_name": "Tangerine",
     "emojis": ["🏦", "💳", "📄", "🚗", "📞"], "keywords": ["bank", "payment", "appointment"]},
    {"id": "flexible", "name": "🔄 Flexible slots",    "color": "#616161", "color_name": "Graphite",
     "emojis": ["🔄"]},
    {"id": "routine",  "name": "🏡 Routine and home",  "color": "#33B679", "color_name": "Sage"}
  ]
}
```

Classification: first the title's **leading emoji** (in `sections` order), then the
**keywords** (case-insensitive), and if nothing matches, the `default` section (must be one
of the `id`s). Emojis are compared with and without the variation selector, so `🖥` and `🖥️`
count as the same. Files with CRLF or LF line endings are accepted.
Events are kept as they are, including time zone and repetitions; each calendar provides the
color. Before delivering, review the list of events that fell into `default`.
