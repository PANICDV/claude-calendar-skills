# Examples

One fictional week (Mon 2 - Sun 8 Nov 2026, `America/Bogota`): a person who works
9:00-18:00 and studies a part-time master's with online classes on Tuesday and Thursday.
The same week is built three ways so you can compare them:

| Folder | What it shows | Import |
|---|---|---|
| `single-calendar/` | `planificador-calendario` / `calendar-planner`: the whole plan in one calendar, plus a reminders calendar | `plan_nov_2-8.ics`, `reminders.ics` |
| `by-sections/` | `...-secciones` / `...-sections`: one color-coded calendar per section | `plan/1_masters.ics` ... `plan/6_flexible.ics`, `reminders/*.ics` |
| `split-existing/` | `--split` mode: the single-calendar plan split by emoji into sections | `out/*.ics` |

Each folder keeps the JSON specs (`spec_*.json`, `rules.json`) that the skills write before
calling the scripts. To rebuild everything from the repository root:

```bash
python examples/make_examples.py
```

Always import into a **new** calendar, never into your main one (see the skills'
`references/importing.md`).
