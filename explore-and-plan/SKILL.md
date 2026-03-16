---
name: explore-and-plan
description: Use this skill whenever you are asked to create a plan, implementation plan, technical plan, project plan, or any kind of actionable proposal. This includes when the user says "make a plan", "write a plan", "plan this out", "design a solution", "draft an approach", or when you are operating in Plan Mode. Also use this skill when the user proposes a new idea, wants to compare approaches, says "what do you think about X", "I'm thinking of building Y", "how should I approach this", "brainstorm", "let's think about this", or is in an exploratory mindset before execution. This skill covers the full arc from open exploration to finalized, executable plan — use it whether the user is still thinking or ready to commit.
---

# From Idea to Executable Plan

This skill governs the full thinking arc: from early exploration and brainstorming, through decision-making, to a finalized plan that can be executed without further clarification.

The key insight: **thinking and planning are not separate activities — they're one continuous flow.** Brainstorming that never converges is wasted effort. Planning that skips exploration produces brittle plans full of blind spots. This skill treats them as phases of a single process.

## Reading the Room

Before doing anything, figure out where the user is in their thinking:

**Still exploring** — They're tossing around ideas, comparing options, not yet committed to a direction. Signals: "what do you think about", "I'm considering", "what are the tradeoffs", "how should I approach", open-ended questions, multiple options on the table.

**Direction chosen, need a plan** — They know what they want, they need it broken down into executable steps. Signals: "make a plan", "plan this out", "how do I implement", a clear specification, Plan Mode.

**Somewhere in between** — They have a rough direction but haven't resolved key decisions yet. This is the most common case.

Match your response to where they are. Don't force someone who's exploring into a rigid plan. Don't let someone who needs a plan stay in endless discussion. And when they're in between, help them close the gaps so you can deliver something actionable.

## Phase 1: Explore (When Needed)

When the user is still in exploration mode, your job is to help them think — but with a bias toward convergence. Every round of exploration should narrow the space, not expand it.

**What good exploration looks like:**

- Surface the real tradeoffs between options, not just list pros and cons. Help the user understand what they'd be giving up with each choice.
- Proactively identify decisions that will need to be made. Don't wait for the user to discover them during implementation.
- Dig into edge cases and constraints early. These often eliminate options or force a direction, which is valuable.
- Pressure-test assumptions. If the user says "I'll just use X," ask yourself whether X actually fits the constraints. If it doesn't, say so.

**What bad exploration looks like:**

- Presenting five options without a recommendation, leaving the user no closer to a decision.
- Endlessly expanding scope ("you could also consider...") without helping narrow things down.
- Being so neutral that you're not useful. If you have a clear recommendation, make it — and explain why.

When you see enough clarity to start converging, say so. Don't wait for permission. Something like: "I think we have enough to lock in a direction — here's what I'd recommend and why." The user can always push back.

## Phase 2: Converge

This is the bridge between thinking and planning. The goal is to lock down every open decision so the plan can be written with zero ambiguity.

Go through each decision point that surfaced during exploration (or that you identify from the requirements) and resolve it. This means:

- **Commit to a specific choice**, not "option A or B." If you need the user's input to decide, ask now — don't defer it into the plan.
- **State the reasoning briefly.** Just enough so an executor won't second-guess the choice. One or two sentences, not a paragraph.
- **Identify what you're not doing** and why. Explicit exclusions prevent scope creep during execution.

If the user arrived already knowing what they want (skipping Phase 1), you still need to do this convergence work — just internally. Scan the requirements for any implicit decisions, ambiguities, or edge cases that haven't been addressed. Resolve them, and surface anything you can't resolve on your own.

The convergence phase is done when you can answer "yes" to: **Could I now write a plan with zero uses of "if", "or", "consider", "possibly", "depending on", or "TBD"?**

## Phase 3: The Plan

Now write the plan. The quality bar here is non-negotiable, regardless of format:

### Every decision is already made

The plan contains no deferred choices. No "if X, then A; otherwise B" unless it describes genuinely runtime-conditional behavior (error handling, feature flags, etc.). No "consider using", "you might want to", "depending on your needs." Every fork in the road has a chosen path.

Phrases that signal an unfinished plan: "if", "or", "possibly", "consider", "depending on", "TBD", "to be determined", "we could either", "optionally." If you catch yourself writing any of these, stop and resolve the decision before continuing.

### Context is self-contained

The plan carries everything an executor needs. Imagine handing it to someone who has access to the codebase but was not part of this conversation. They should be able to start working without asking "but wait, what about...?"

Include:
- **Why** key decisions were made (briefly — prevent second-guessing, not a history lesson).
- **What exists** that the plan touches (file paths, function names, current behavior).
- **What done looks like** — the expected end state, so the executor can verify completion.

### Steps are concrete and ordered

Each step describes a specific action with enough detail to execute. The granularity should match the complexity — a config change gets one line, a new module gets structured detail.

Steps should specify what file(s) to change, what the change does, non-obvious implementation details, and how to verify correctness when it's not obvious. Order them so dependencies are respected.

### Format follows function

There is no mandatory template. A small bugfix might be five numbered steps. A large feature might use sections with substeps. A system design might need an architecture overview before diving into steps. Use whatever structure makes the plan clearest for the specific task.

## Self-Check

Before presenting your output, ask yourself:

- If someone picked this up cold, could they start executing right now?
- Is there any point where they'd need to make a judgment call I haven't made for them?
- Have I resolved every "if/or/maybe" into a concrete decision?
- Did I skip exploring any area that could bite the executor later?
- If they follow the steps in order, will they arrive at the correct end state?

If any answer is unsatisfying, you're not done yet.
