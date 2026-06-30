# Anti-Patterns

Use this as a review checklist before delivery or when a deck starts getting
hard to modify.

## Starting From A Vague Prompt

If the user gives only a short idea, do not begin by creating files. First align
on purpose, audience, density, source material, visual direction, and delivery
context. A fast wrong deck costs more than one good clarification.

## Forcing A Framework

This skill is not a framework recommendation. Do not force React, Vite,
Tailwind, Playwright, or any other stack when the user has an existing project or
clear preference. Implement the harness mechanisms in the chosen stack.

## Using Harness For Tiny One-Off Slides

For a tiny static deck with no expected iteration, no animation states, and no
regression risk, a single HTML file may be enough. The harness is worth it when
future edits, visual review, or stateful frames matter.

## Rendering A Whole Static Slide In Canvas

Canvas text is hard to inspect, copy, search, translate, and audit. Use DOM or
SVG for static text and labels. Reserve canvas for genuinely graphical regions,
and expose equivalent labels when the content matters.

## Treating Beats As Decorative Fades

A beat should represent story progress: a new argument, reveal, comparison,
chart state, or demo state. Do not create a new beat for every decorative text
fade. Excess beats multiply review work and visual baselines without improving
the talk.

## Responsive Breakpoints Inside The Stage

The slide stage should scale as a whole. Viewport breakpoints inside the stage
can make the same slide render differently on laptop, phone, projector, and CI.
Use fixed stage geometry for slide content; keep responsive UI outside the
stage.

## Embedding Live Demos Inside Critical Frames

Cross-origin iframes, remote sandboxes, videos, and live widgets often make
screenshots flaky. Prefer an external demo link plus a stable screenshot unless
the live region is central to the slide and has a deterministic test mode.

## Casual Stable Id Renames

Stable ids are part of links, baselines, and review history. Rename ids only when
the identity of the scene has truly changed, and clean up stale baselines or
links intentionally.

## Masking The Main Content

Visual masks are for nondeterministic regions, not for hiding broken layout. If a
mask covers the user's actual message, the visual check no longer protects the
deck.

## Skipping Checks After Visual Changes

A build can pass while the rendered deck is wrong. Run the relevant structural or
visual check after changes to layout, animation, fonts, assets, shared visual
code, or frame navigation.
