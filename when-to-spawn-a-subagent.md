---
name: when-to-spawn-a-subagent
description: Framework for deciding when a subagent is justified vs. keeping work in the main loop — derived from redesigning the biomechanics-course agent team.
metadata: 
  node_type: memory
  type: reference
  originSessionId: c2a0bb1b-e525-4eb4-ad10-e77647a9cf09
---

# When to spawn a subagent (and when not to)

Distilled from redesigning an agent team for the biomechanics course. The
original proposal was **orchestrator + writer + verifier (with cheap models to
save cost)**. Reasoning through it collapsed it to **the section loop (main
context + Bash + hardening scripts) + one reviewer agent.** The framework below
is why, and it generalizes.

## The core test — a subagent is justified only if it passes ONE of these

1. **Separation itself is the value.** The agent must structurally lack
   something the main context has, and *that lack is the point*. The canonical
   case is **independent review**: a reviewer that did NOT write the thing
   catches what the author is blind to. You cannot replicate this by re-reading
   your own work harder — the blindness is structural, so only separation
   creates the value.
2. **Something must reason over large throwaway output.** An agent chews through
   a big blob and returns only a conclusion, so the blob never floods the main
   context. Key word is *reason* — not merely *produce*.

If a task passes neither, **keep it in the main loop.**

## Three traps that make you over-spawn

**Trap A — treating "context isolation" as a symmetric benefit.** Isolation only
helps if you *don't have to re-ingest the output*. When the subagent's output
**is the deliverable you must understand anyway** (e.g. writing prose you then
review, harden, and commit), isolation saves nothing — and it *costs* quality,
because a cold-start agent lacks the accumulated context that makes the work
good (in this project: which symbols are already used so you don't collide
W/k/g/E, the exact wording of prior sections, the style sign-off, the user's
last review). Delegating the hardest reasoning to a cold agent produces *worse*
output than doing it in the context that already holds everything.

**Trap B — confusing "run a script that writes to a file" with "delegate to an
agent."** A Bash command's noisy stdout goes to a *file*, never your context —
so you already get isolation *for free*, no agent needed. You only need an agent
when something must **reason over** that output. And if a *deterministic script*
does the reasoning (here: `check_overlap.py`, `verify_dom.py`, `checktex.py`),
you don't need an agent at all. Figure-compute is exactly this: `gen9.py →
svg9.json` runs in the background, you `Read` only the small JSON — no agent.

**Trap C — cheap models on the wrong role.** Put the strong model where
reasoning and correctness live (writing math, proofs, judging rigor). Use cheap
models only on mechanical, script-verified, throwaway work. Economizing on the
reasoning step pays the tokens back with interest when a weaker model emits
plausible-but-wrong math and subtle rendering bugs that then round-trip through
review.

## Worked decision table (this project)

| Piece of work | Agent? | Why |
|---|---|---|
| Orchestration / the section loop | No | It *is* the main context holding conventions + prior sections. |
| Writing prose, derivations, proofs, problems | No — main loop | Fails both tests; output is the deliverable, and cold-start hurts quality (Trap A). |
| Figure-compute (Python → JSON) | No — Bash call | Output goes to a file; deterministic scripts check it (Trap B). |
| Mechanical verification | No — the hardening scripts | Already deterministic; an LLM verifier duplicates and is less reliable. |
| Independent review (rigor parity, read-aloud prose, K-problem depth, anatomy) | **Yes — one agent** | Passes test #1: value is that it *didn't* write the section. |

## The general rule

> Spawn a subagent only when **separation is the value** (independent review) or
> when an agent must **reason over a large throwaway blob**. Otherwise keep it in
> the main loop. "Noisy work" is not a reason — pipe it to a file. "It's a big
> chunk of work" is not a reason — if you must understand the output anyway,
> in-context is both cleaner and higher-quality.

## Caveat that survived (course-specific)

Even the minimal loop is not *fully* autonomous: the figure-style sign-off (one
representative figure approved before mass-producing) and the final anatomy
eyeball are judgment gates the repo reserves for the human — no reviewer agent
reliably replaces "does this SVG read as a knee." Automate everything between
those gates. Related: [[publish-modules-while-incomplete]].
