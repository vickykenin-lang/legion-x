# MoneyPrinterTurbo — Curated Useful Material

This folder preserves only the reusable engineering ideas found during a live
MoneyPrinterTurbo v1.3.4 evaluation. It is not a vendored copy of the project and
must not be treated as LEGION-X's video-quality solution.

## Decision

MoneyPrinterTurbo was rejected as a creative video engine for LEGION-X. The live
outputs were not publishable: generic visuals, basic zoom motion, weak scene
direction, no character continuity, and unreliable online voice synthesis in the
test environment.

## What was worth keeping

- A provider-independent video-job contract.
- A strict approval-before-publishing state machine.
- A reusable vertical render profile.
- Notes on task queues, status persistence, subtitles, local assets, social
  metadata, and publishing adapters.

## What must not be imported

- Stock-footage-led creative direction.
- Automatic publishing immediately after rendering.
- Default background music.
- In-memory-only production state.
- Unauthenticated public API configuration.
- Claims that topic-to-video output is production quality without independent QA.

## Intended LEGION-X placement

`Scripter -> Forge -> Guardian -> Human Approval -> Flash -> Vision`

The files here support the boundaries between those agents. Forge may use any
future renderer, but Guardian and Human Approval remain mandatory before Flash
can publish.

