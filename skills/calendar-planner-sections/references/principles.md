# Schedule design principles

Read this before designing. Each principle has a reason: apply them with judgment.

## Principles

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

## By horizon
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

They go in separate files, in their own section ("🔔 Reminders"), or in several if the person prefers ("💳 Bills", "🧽 Maintenance").
- Bills: an all-day event on the due date. If the person wants a heads-up, add a second event the day before, because all-day alarms behave differently from app to app.
- "Every N days": `freq DAILY` + `interval N`. "Day X of each month": `freq MONTHLY` + `bymonthday X`. For the end of the month use `bymonthday -1`. If X is 29–31, warn that short months skip that day and offer the last day of the month instead.
- No end date unless the person gives one: reminders are permanent.
- Maintenance tasks (cleaning the fridge) can get a suggested time in a typical gap of the person's routine.
