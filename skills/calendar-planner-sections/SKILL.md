---
name: calendar-planner-sections
description: Designs optimized schedules (daily, weekly, short or long periods, quarterly) and delivers them as SEVERAL .ics calendars, one per section (thesis, work, errands, routine, etc.), each with its own color, to import into Google Calendar, Apple or Outlook; recurring reminders (bills, cleaning) go in their own calendar. Use it ALWAYS when the person wants their plan or calendar split by categories, sections, areas or colors, wants it to "look more distinctive", wants to hide or show topics, or asks to split an existing .ics or plan by color. If they ask for a plan without mentioning sections or colors, the single-calendar version (calendar-planner) is enough when it is available.
---

# Calendar planner by sections

Does the same as a regular planner (interview, optimized design, importable files), but
delivers **one calendar per section, each with its own color**. Each topic is recognizable
at a glance, and a section can be hidden or shown with one click.

Why one file per section: Google Calendar ignores the per-event color an .ics carries; the
color comes from the calendar. One calendar per section is the only way for colors to show
up in Google. Apple does use the color the file carries.

Modes:
- **New plan by sections**: interview, design, one .ics per section.
- **Split an existing plan**: the person brings an .ics (for example, one made with the single-color version) and wants it split by color. Go straight to step 3 (propose sections) and use `--split` mode.
- **Reminders only, by sections**: for example "💳 Bills" and "🧽 Maintenance" as separate calendars.
- **Update**: see "Updates".

## Workflow

### 1. Gather what you already know
Check the conversation and memory (routine, sleep, work, planning preferences, sections or
colors the person chose before). Do not ask for what you know: confirm it in one line. If
the person already has sections and colors from an earlier plan, **reuse them**: they already
created those calendars in their app, and changing them forces them to redo the work.

### 2. Interview in blocks
Read `references/questionnaire.md` and ask one block per message, as a numbered list, only
for what is missing (period, fixed routine, to-dos, reminders, preferences). No more than
3–4 rounds; estimate whatever the person does not know and say so.

### 3. Propose the sections (extra block, always)
With the to-dos known, propose the sections in a table (emoji + name, color, what it
includes) and ask for confirmation or changes in a single message. Guidance in
`references/sections.md`. In short:
- **4–8 sections.** Fewer does not distinguish; more clutters the calendar list and the import work.
- Group by **kind of attention**, not by single task: "Server · AI tools · Courses" together (technical), "Banks and errands" together (business hours).
- Always: a **routine and home** section and a **flexible slots** section (gray). **Priorities** get strong, distinct colors.
- Recurring reminders go in their own section(s) and separate files.

### 4. Design the schedule
Apply `references/principles.md` (visible sleep, deep work in high-energy hours, errands in
business hours, 60–150 min blocks, daily variety, option A/B for uncertain dates, one flexible
slot a day, weekly review, long horizons detailed only for the first 1–2 weeks). Assign each
event to a section.

### 5. Generate and validate
Write the JSON (format in `references/spec_format.md`, always with `"lang": "en"`) and run:

```bash
# new plan
python <skill-path>/scripts/build_sections.py <working-folder>/spec.json
# split an existing .ics
python <skill-path>/scripts/build_sections.py --split <path>/plan.ics <working-folder>/rules.json
```

The script validates the JSON (if there are errors, it lists them all and writes nothing),
checks clashes across the whole plan, writes one .ics per section (`1_thesis.ics`,
`2_tech.ics`…) and shows the table section → color → events → hours. Fix unintended
clashes. If it warns that `python-dateutil` is missing, install it
(`pip install python-dateutil`) and run again. In `--split` mode, review the list of events
that fell into the default section: if any is wrong, adjust the rules and run again.
For reminders use a separate JSON (also by sections if there are several).
Save the files in the environment's output folder (on claude.ai: `/mnt/user-data/outputs/`;
the script creates the folder if needed) and deliver them together, in numbered order, with
the environment's file-sharing tool (on claude.ai: a single `present_files` call).

### 6. Deliver
A short message in the person's language:
- **Legend**: table with file, calendar name, color (name + hex) and what it includes.
- 3–6 key decisions in prose and the assumptions you made.
- Import steps from `references/importing.md` for their app. The essentials: create one calendar per section with the name in the table, import each file into its calendar and give it its color. Never import into the main calendar.
- Creating the calendars is done once; updates reuse them.

## Updates
- Keep **the same sections, names, file numbers and colors**: the person already created those calendars.
- Change only what was asked and rebalance as little as needed. If they asked "give X more time", show a before/after table of hours per section.
- Deliver **only the files of the sections that changed** and say which ones. For each: delete that calendar and recreate it with the same name and color before importing, because Google does not reliably replace events already imported and they would be duplicated. Unchanged sections are not touched.
- Reminders are only regenerated if they changed.
- If the person says they liked something, apply it to future plans too.

## Reference files
- `references/questionnaire.md`: interview question blocks.
- `references/sections.md`: how to build sections, color palette and suggested sections.
- `references/principles.md`: principles for designing the schedule and event format.
- `references/spec_format.md`: JSON for the sectioned plan and for the `--split` rules.
- `references/importing.md`: create calendars, import, color and delete in Google, Apple and Outlook.
