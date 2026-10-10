---
name: calendar-planner
description: Designs optimized schedules (daily, weekly, short or long periods, quarterly) and delivers them as .ics files to import into Google Calendar, Apple Calendar or Outlook, plus a separate calendar of recurring reminders (bills, cleaning, maintenance). Use it ALWAYS when the person wants to get organized, plan their week or month, spread tasks or to-dos over time, build or stick to a routine, set reminders that repeat (every N days, on day X of each month) or asks for a file to import into their calendar, even if they never mention ".ics" or "skill". Also for updating or rebalancing a plan already delivered. This version delivers the plan as a single calendar (one color).
---

# Calendar planner

Turns a person's to-dos, routine and commitments into a realistic, optimized schedule and
delivers it as files they import into their calendar.

There are two products and they almost always go in separate files, because they do
different jobs:

| File | Contains | Why separate |
|---|---|---|
| `plan_<period>.ics` | Fixed routine + tasks spread into blocks | Replaced every time the plan is updated |
| `reminders.ics` | Bills, cleaning, maintenance that repeat | Permanent; sits on top of the normal calendar and is not touched when the plan changes |

Modes:
- **Full plan**: routine + to-dos (+ reminders if any).
- **Reminders only**: the person just wants recurring alerts (e.g. "clean the fridge every 30 days", "pay the electricity bill on the 3rd of each month").
- **Update a plan**: a plan was already delivered and needs rebalancing (see "Updates").

## Workflow

### 1. Gather what you already know
Before asking anything, check the conversation and any available memory: sleep hours, work
hours, commutes, children, pets, planning preferences. Do not ask again for what you already
know; confirm it in one line ("I'll use your usual routine: you sleep 11:00 pm–7:00 am, work
Mon–Fri 9–6 and pick up the kids at 3:30… still the same?"). Asking again for something the
person already said tells them they were not listened to.

### 2. Interview in blocks
If information is missing, ask **in blocks as a numbered list**, one block per message, so
the person can answer quickly by number. The blocks and their questions are in
`references/questionnaire.md`; read it before asking.

- Skip blocks that do not apply ("reminders only" → blocks 1 and 4).
- If the person already gave everything in one message, ask only for what is missing, in a single block.
- Accept partial answers: estimate what they do not know (durations, energy levels) and say so.
- No more than 3–4 rounds. With the essentials (period, sleep, fixed commitments, to-dos) you can already design; the rest gets adjusted later.

### 3. Design the schedule
Apply the principles in the next section. Work in this order:
1. **Fixed anchors**: sleep, work, commutes, meals, childcare and pet care, commitments with a set time.
2. **Tasks with a deadline or that need business hours** (banks, calls, offices, paperwork).
3. **Big projects** split into blocks.
4. **Small tasks** grouped into short gaps.
5. **Flexible slots** and free time.

### 4. Generate and validate the files
Write a JSON spec and run the script (full format in `references/spec_format.md`). Always
include `"lang": "en"` so the script reports in English:

```bash
python <skill-path>/scripts/build_ics.py <working-folder>/spec_plan.json
```

The script validates the JSON (if there are errors, it lists them all and writes nothing),
writes the .ics, detects **clashes** between events (expanding recurring ones) and prints
**hours per category**. Fix every unintended clash before delivering, and use the hours
summary to confirm that the priorities get the time the person asked for. If it warns that
`python-dateutil` is missing, install it (`pip install python-dateutil`) and run again:
without it, recurring events are not checked.

Save the files in the environment's output folder (on claude.ai: `/mnt/user-data/outputs/`;
the script creates the folder if needed) and deliver them with the environment's file-sharing
tool (on claude.ai: `present_files`).

### 5. Deliver
A short message in the person's language:
- A short table with the daily routine (time → activity).
- In prose, the 3–6 key decisions (what was prioritized, where the errands landed, which days are lighter).
- Any assumption you made ("I gave Toby 30 minutes because I assumed he's a dog; tell me if not").
- Import instructions (see `references/importing.md`): **always into a new calendar, never the main one**.

## Design principles

Each principle has a reason; apply them with judgment, not as blind rules.

- **Sleep is a visible event.** If it is not on the calendar, the plan eats it. Respect the hours the person gives and leave ~30 min between waking up and the first demanding activity.
- **Deep work in high-energy hours.** Ask which they are; if the person does not know, use the morning. Mechanical work (email, short errands) goes into lower-energy hours.
- **Errands in business hours.** Banks, calls, clinics and offices: roughly Mon–Fri 9 am–6 pm, Saturday mornings. Add a document-prep block beforehand if the errand needs it.
- **Useful block sizes.** Deep work: 60–150 min. Small tasks: 15–45 min, grouped. Under 45 min is not enough to focus on something complex; more than 2.5 h in a row pays off poorly.
- **Daily variety.** No day devoted to a single topic; at most ~2 blocks of the same topic per day, separated by something else. Alternate demanding and light work.
- **Big projects in numbered blocks.** "Thesis: slides (block 3)". Put the concrete goal of the block in the description. Schedule the closing block ("FINISH …") with margin before the deadline.
- **Uncertain dates → option A / option B.** If an errand could fall on either of two days, book a block on each and write in the description that whichever is not used becomes time for the priority topic. No time is lost and the plan is not overloaded.
- **Flexible slots 🔄.** About one per day (10–15 % of the available time), to move whatever did not get done. A plan without slack breaks at the first surprise and the person abandons it.
- **Margins after variable events.** If lunch sometimes runs 15 min over, the next block starts 15 min later.
- **Do not fill up to bedtime.** Leave free or family time at the end of the day, and lighter days (for example, Friday evening and part of Sunday).
- **Weekly review.** A short block to review progress and ask for the plan to be adjusted, and another to plan the next week.
- **Explicit priorities win.** If the person says "give X more time", take time from the least urgent topics and show a before/after table of hours per topic.
- **Alarms only on what is critical.** Appointments, errands with a set time, bills, elections, school pick-ups. If everything rings, nothing rings.

### By horizon
| Type | How to plan |
|---|---|
| Daily | Detailed blocks for the whole day. |
| Weekly / short period (≤ 3 weeks) | Full day-by-day detail. |
| Long period / quarterly | Fine detail only for the first 1–2 weeks. After that: recurring routine + weekly milestones per project ("Week 5: report done") + weekly reviews. Detailed long-term plans go stale fast, so it is better to review and adjust them every week. |

## Event format

- **Routine as recurring events** (`repeat`), not as copies: cleaner and easier to delete.
- **Title**: emoji + topic + detail. The emoji identifies the category and makes it searchable (to delete or filter) in the calendar. Use the same emoji for the same topic for the whole plan.

| Emoji | Typical use |
|---|---|
| 😴 🏃 🍳 🍽️ | Sleep, exercise, meals |
| 🐕 🎒 🧹 | Pets, kids/school, cleaning |
| 🎓 🎤 | Studies, thesis, rehearsals/presentations |
| 🖥️ 🤖 🧩 | Technology, technical projects, tools |
| 🏦 💳 📄 🚗 📞 | Banks, payments, documents, car, calls |
| 🗂️ 📧 🎨 📋 | Organization, email, design, review or planning |
| 📈 💾 | Investing/markets, sales |
| 🔄 | Flexible slot |

- **Description**: the concrete goal, the alternative if there is one, and useful details (the doctor's name, which documents to bring).

## Recurring reminders

They go in `reminders.ics`, with their own `calendar_name` (for example "🔔 Reminders").
- Bills: an all-day event on the due date. If the person wants a heads-up, add a second event the day before, because all-day alarms behave differently from app to app.
- "Every N days": `freq DAILY` + `interval N`. "Day X of each month": `freq MONTHLY` + `bymonthday X`. For the end of the month use `bymonthday -1`. If X is 29–31, warn that short months skip that day and offer the last day of the month instead.
- No end date unless the person gives one: reminders are permanent.
- Maintenance tasks (cleaning the fridge) can get a suggested time in a typical gap of the person's routine.

## Updates

When the person asks for changes ("give X more time", "I can't on Tuesday"):
- Keep everything they did not ask to change: routine, earlier decisions, emojis.
- Change only what was asked and rebalance as little as needed.
- Version the file (`plan_…_v2.ics`) and remind them: **delete the old plan's calendar and create a new one before importing**, because Google Calendar does not reliably replace events that were already imported and they would be duplicated.
- The reminders calendar is not touched, unless the changes are about reminders.
- If the person says they liked something in your plan, apply it to future plans too.

## Reference files
- `references/questionnaire.md`: question blocks for the interview. Read it before asking.
- `references/spec_format.md`: format of the JSON the script reads, with examples.
- `references/importing.md`: how to import and delete in Google, Apple and Outlook.
