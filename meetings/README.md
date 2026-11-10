# Public meeting intelligence — source-first, independent research

Started 2026-11-10. **This folder contains an index of official agenda listings, not verified accounts of what actually happened at meetings.**

## Official primary sources
- [Town of Dartmouth — Board of Public Works agendas and minutes](https://dartmouthma.gov/AgendaCenter/Board-of-Public-Works-35/)
- [Town of Dartmouth — Select Board agendas and minutes](https://www.dartmouthma.gov/AgendaCenter/Select-Board-25)
- [DCTV town media / broadcast channels](https://www.dartmouthma.gov/194/Channels-Schedules)
- [DCTV government channel live/on-demand](https://reflect-dctv-18.cablecast.tv/internetchannel/watch-now?channel=2&site=2)

No collaboration or access agreement with a third-party meeting aggregator is necessary for this project. Prefer links to original town recordings, published agendas, and official minutes. Respect providers' rights, platform terms, and bulk-access limits.

## Current datasets
- [`meeting-index.csv`](meeting-index.csv): 20 posted **2026 Board of Public Works / joint BPW–Select Board agenda entries**, drawn from the Town Agenda Center on November 10, 2026. An agenda listing **does not verify that a meeting occurred**, the attendance, minutes, decisions, or meeting content.
- [`issues-and-actions.csv`](issues-and-actions.csv): Evidence-linked issue/action ledger schema; **no findings have been asserted yet**.

## Intake & review workflow
1. Record date, body, meeting title, agenda URL, and original file retrieval date.
2. Find official approved minutes where available and the original DCTV recording; populate URL fields.
3. Review source material; identify statements, motions, votes, costs, accountable bodies and deadlines with page numbers or recording timestamps.
4. Extract **one row per distinct issue / decision / commitment**, not one row per meeting.
5. Normalize issue labels (e.g., staffing, overtime, highway maintenance, fleet, procurement, capital planning, water/sewer, solid waste, governance, software/process).
6. Reconcile follow-up meetings and official records; label **open / resolved / unclear**, and separate proposed action from actual completion.
7. Review any AI transcript against original recording before quoting or relying on specific claims.

## Confidence and fairness
- Source collected ≠ verified decision.
- Repeated agenda mentions ≠ repeated failure.
- A board discussion or resident complaint ≠ a verified fact.
- Absence of a progress update ≠ proof work was not done.
- Do not label staff lazy or allege improper conduct from anecdotes, parked trucks, or automated transcript text.
- Publish only verified, relevant professional information; avoid personal data and unsupported accusations.

## First pass
Start with the 2026 BPW agenda index. Review the joint meetings (July 13, August 3, October 5) and budget/capital-planning discussions before expanding into 2025 and 2024. Build a chart of issue recurrence and verified resolution lag only once a representative reviewed sample exists.
