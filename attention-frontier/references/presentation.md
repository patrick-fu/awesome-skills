# Workbench presentation

**Re-entry, progressive disclosure, plain language.** Let the reader quickly
find where a matter stands, what changed, and what they can do next. Use the
user's language and familiar terms. State facts, recommendations, and unknowns
at their actual strength. If available, explain and deslop can support
orientation and prose editing; neither is required to use this skill.

**Engineering whiteboard, modern hand-drawn, lively emoji, restrained motion.**
Use these as visual direction, adjustable to the user's preferences. Pair
stable emoji meanings with text, keep hierarchy clear, and use motion to signal
changes or support navigation. Respect reduced-motion preferences.

## Current view

Use compact tables or short labeled units for comparison and scanning. Make
current user actions prominent, with active work, external waits, and unresolved
evidence easy to inspect. Emphasis follows actual priority; choose the amount
of detail for the workload, with every unfinished matter still reachable.

Lead with a stable business-matter title. Put temporary activity in current
progress, and retain each conversation's verified title as its source link.

Keep **Main task** and **Background and context** visible for each matter,
each in one or two sentences. Main task explains the owning conversation's
intended outcome and scope. Background explains why the work exists and the
prior decisions or constraints that led to the current situation. Explain
enough terminology for someone who has forgotten the matter to recognize it.
Keep the latest progress distinct from this orientation.

Show unfinished side tasks and parallel work together under related work,
including branches within the same conversation. Briefly state each branch's
purpose, current state, and relationship to the main task, with its owner or
source link. Highlight the branch needing the person's attention and relevant
dependencies. Completed branches that still explain the situation belong in
the background or supporting history.

Let the reader move from the business title through main task, background,
related work, and current progress to the recommended next move and prompt.
Combine overlapping explanations of the reason, action, and recommendation
so adding context does not multiply repeated text.

Keep two fields visible for each matter: **Next step** and **Suggested prompt**.
Put the reason, next owner, and source link beside them. Make the prompt a short,
copyable instruction addressed to the linked owning conversation. Reuse that
conversation's context and name the concrete action or desired outcome; omit
defensive boilerplate. For example: “跑一遍移动端验收，把结果和截图给我。”
Match the recommendation's scope. Label any prerequisite physical action the
person must complete before sending a prompt that reports it as done.

For work already progressing or waiting on an external event, show the actual
next step and its owner or trigger. When a message would not advance it, mark
the prompt field “No message needed now.” If nothing needs the person, say so
in the opening recommendation.

Put supporting history and evidence behind details where useful. Distinguish
the person's completed action from the project's completion; keep observed
work visible and restore it to the action area when needed again.

If search or filters are provided, cover the full unfinished queue, including
main tasks, background, and related work across its sections.

## Stable entry

Update the same entry rather than issuing a new dashboard per run. Choose a
lightweight refresh mechanism supported by the host, preserving scroll position
and expanded details along with active search and filters. Display the last
successful check and source-specific gaps or older verification times. Describe
the actual update cadence.

Verify from the reader's side: leave the page open, publish another update, and
confirm that the same tab shows it while preserving reading position. Check
the links and the full queue's reachability. If automatic refresh is unavailable,
make the refresh requirement explicit instead of implying a live view.

The workbench is a view of source-backed state. Keep decisions and completion
in their authoritative work context so local viewing does not create competing
task records.

## Polling reply

Report meaningful deltas: newly actionable work, changed priority or risk,
released blockers, and completed user actions. Include the stable entry link.
A changed check timestamp or cosmetic edit alone is not a notification.

Unchanged open actions remain marked in the HTML. Their continued presence
does not require another polling reply.
