# Spec format (JSON)

`scripts/build_ics.py` reads a JSON file and writes an .ics. Write one JSON per output file
(one for the plan and another for the reminders).

Paths in the examples are the claude.ai ones (`/mnt/user-data/outputs/`). In any other
environment, use its output folder; the script creates the folder if it does not exist.

## Structure

```json
{
  "lang": "en",
  "calendar_name": "Plan Oct 3–11",
  "timezone": "America/New_York",
  "output": "/mnt/user-data/outputs/plan_oct_3-11.ics",
  "range_end": "2026-10-11",
  "color": "#33B679",
  "events": [ ... ]
}
```

| Field | Required | Notes |
|---|---|---|
| `lang` | no | Language of the script's messages: `en` or `es` (default `es`). Always use `en` in this version. |
| `calendar_name` | yes | Suggested calendar name on import. |
| `timezone` | yes | IANA zone (`America/New_York`, `Europe/London`, `Asia/Kolkata`…). The script writes the VTIMEZONE with the real clock changes and, for zones with daylight saving time, its yearly rule, so open-ended reminders stay correct in future years. |
| `output` | yes | Path of the .ics. |
| `range_end` | no | Last day of the plan; improves the clash check for recurring events. |
| `color` | no | Hex `#RRGGBB`. Apple uses it; Google ignores it (there, color is chosen per calendar). |

## Timed events

```json
{"title": "🎓 Thesis: slides (block 1)",
 "start": "2026-10-03T10:00", "end": "2026-10-03T12:30",
 "description": "Full structure and first sections.",
 "alarm_min": 10}
```

Times are **local, without a zone** (`2026-10-03T10:00`, no `Z` or `-04:00`): `timezone` sets
the zone. Use 24-hour times in the JSON even if the person uses am/pm. An event may cross
midnight (sleep, for example): `"start": "2026-10-02T23:00", "end": "2026-10-03T07:00"`.

## All-day events

```json
{"title": "💡 Pay electricity bill", "date": "2026-11-03"}
```
For several days add `"end_date": "2026-11-05"` (inclusive). They have no time, so they are
not part of the clash check.

## Repetition (`repeat`)

| Need | `repeat` |
|---|---|
| Every day until Oct 11 | `{"freq": "DAILY", "until": "2026-10-11"}` |
| Monday to Friday | `{"freq": "WEEKLY", "byday": ["MO","TU","WE","TH","FR"], "until": "2026-10-09"}` |
| Every 30 days | `{"freq": "DAILY", "interval": 30}` |
| The 3rd of each month | `{"freq": "MONTHLY", "bymonthday": 3}` |
| Last day of each month | `{"freq": "MONTHLY", "bymonthday": -1}` |
| Every other Saturday | `{"freq": "WEEKLY", "interval": 2, "byday": ["SA"]}` |
| Once a year (March 15) | `{"freq": "YEARLY", "bymonth": 3, "bymonthday": 15}` |
| 6 repetitions | add `"count": 6` |
| Free-form rule | `{"rrule": "FREQ=MONTHLY;BYDAY=1MO"}` (first Monday of the month) |

`until` is an **inclusive** local date. Without `until` or `count` the repetition is endless,
which is right for permanent reminders. The script writes `UNTIL` the way the standard
requires (a date for all-day events, a UTC time otherwise), including inside free-form rules.

## Other fields
- `alarm_min`: minutes of warning before the start.
- `location`: place.
- `allow_overlap: true`: the script does not report clashes for this event (useful for a heads-up event that overlaps on purpose).
- `uid`: optional; if missing, a stable one is generated from the title and date. If two events share title and start, the script warns and gives them different UIDs.

## Example: reminders

```json
{
  "lang": "en",
  "calendar_name": "🔔 Reminders",
  "timezone": "America/New_York",
  "output": "/mnt/user-data/outputs/reminders.ics",
  "events": [
    {"title": "💡 Pay electricity bill", "date": "2026-11-03", "repeat": {"freq": "MONTHLY", "bymonthday": 3}},
    {"title": "🔔 Tomorrow: pay electricity bill", "date": "2026-11-02", "repeat": {"freq": "MONTHLY", "bymonthday": 2}},
    {"title": "🧊 Clean the fridge", "start": "2026-10-10T10:00", "end": "2026-10-10T10:45",
     "repeat": {"freq": "DAILY", "interval": 30}, "alarm_min": 30}
  ]
}
```

## Script output
```
✅ No clashes between timed events.
Hours per category (repetitions included):
   🎓     20.0 h
   🖥     13.8 h
   ...
📄 /mnt/user-data/outputs/plan_oct_3-11.ics  (73 events)
```
- **Clashes**: fix them in the JSON and run again.
- **Format errors** (unknown zone, invalid date, end before start, misspelled `freq` or `byday`): the script lists them all at once and does not write the file.
- **python-dateutil missing**: the script says so; install it, because without it recurring events are not checked.

With `--check` it only validates, without writing the file.
