# Controller handoff

Read for a new continuing owner, direct takeover, or degraded recovery of either
controller role. A second opinion can stay within the existing task; transfer
responsibility when a successor is needed.

## Establish the assignment

In predecessor-led handoff, continue an eligible successor by formal
`(hostId, threadId)`, or create one when the user requests a new task. Send a
concise transfer summary naming the role and scope so the successor can recover
its responsibility from history. In direct takeover, the user designates the
current session and it recovers the same facts itself.

The predecessor remains owner until acceptance. Existing authorized work can
continue while the successor prepares; coordinate writers of shared working
state so preparation does not produce competing execution.

## Recover current facts

Start with the current summary, linked artifacts, and relevant user decisions.
Use the [control index](../SKILL.md#current-facts) to locate responsibilities,
direct owners, follow-up choices, pending waits, and resource holds. For repository
work, check the actual working state, integration target, and available test or
review evidence. Preserve authorization limits, verified failed approaches that
affect the next step, and unresolved delivery or evidence gaps.

Verify facts that affect the transfer against current sources, including recent
user steering in directly owned tasks. Use [task selection](return.md#check)
where needed. For a missing or conflicting fact, read the relevant history;
use [delivery recovery](delivery.md) when the task read is incomplete or
suspicious. Preserve the question behind a terse answer and link supporting
records. Valid current evidence can settle the transfer without replaying the
whole history or repeating completed technical verification.

A gap in identity, access, authority, or responsibility needed for the transfer
keeps the predecessor in charge and the affected ownership, title, and routing
unchanged. Record other unknowns for follow-up within the selected mode.
Independent authorized work continues; an unresolved outcome or resource hold
keeps its existing dependency even when the successor can accept responsibility
for managing it.

## Accept responsibility

The successor needs a formal identity, the assigned host/project and usable
access, and a verified understanding of the material responsibilities it is
taking on. It then states in normal language that it accepts ownership and what
remains next. The predecessor verifies that statement; in user-authorized direct
takeover, the successor's evidence-backed acceptance establishes the transfer.

After acceptance, apply [handoff routing](return.md#handoff-routing) to the
relationships that need it. Notify only tasks whose next action or return path
changes. Preserve existing children; replacement is for confirmed failure or
unreachability, or the user's request.

Use `codex-session-naming` for the predecessor's outgoing handoff and the
successor's continuing role. Archive the predecessor once required routing
changes permit retirement, unless the user wants it kept visible. Retain history.
For a project handoff, record the successor in the project task for the global
controller's next check; notify immediately only under a user-selected Callback
on that project-to-global relationship. A global handoff preserves project owners
and their internal relationships.
