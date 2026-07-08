# Building a Claude Code Agent — and the Tools It Uses

A behind-the-scenes explanation of how a Claude Code (sub)agent is actually
built, what its tools do, and how it decides which tool to use. Written for
someone with a Unix background who has never built an agent.

---

## Part 1 — What "an agent" actually is

**An agent is a Markdown file, not a deployed service.** You are not standing up
a server, a daemon, or a long-running process. An agent definition is a file
with some YAML settings at the top and a body of prose beneath. When you are not
using it, it sits on disk doing nothing.

When the file is *invoked*, the harness spins up a **fresh instance of Claude** —
a brand-new, blank context window — hands it that file's prose as its system
prompt plus a specific task, lets it work on its own with whatever tools you
granted it, and when it finishes it returns **one final message**. That final
message is the entire deliverable. Everything it did along the way (its tool
calls, its intermediate reasoning) stays in *its* context and never enters the
caller's context. That isolation is the point: it is what gives a reviewer agent
"fresh eyes," and what lets a worker agent chew through a large, noisy blob and
hand back only the conclusion.

### Anatomy of the definition file

An agent lives at `.claude/agents/<name>.md` (project-scoped) or
`~/.claude/agents/` (available in every project). Two parts:

**1. Frontmatter — the YAML settings:**

```yaml
---
name: rigor-reviewer
description: When to use this agent — the caller reads this to decide to call it
tools: Read, Grep, Glob, Skill      # optional; omit = inherit all tools
model: fable                         # optional; omit = inherit the caller's model
---
```

- **`name`** — the identifier you call it by.
- **`description`** — *when* to use it. The orchestrator matches against this to
  decide to dispatch the agent. This is the most important field for getting the
  agent used at the right moment.
- **`tools`** — which tools it is allowed to use. A **least-privilege** decision
  (see Part 3); not boilerplate.
- **`model`** — which model it runs on.

**2. The body — everything after the frontmatter:** free-form prose that becomes
the agent's **system prompt** — its role, exactly what it does, and how to
report. This is where the agent's behavior is actually defined.

### The lifecycle

1. **Author** — write the `.md` file once; reuse it forever.
2. **Invoke** — the caller uses the Agent tool with `subagent_type: "<name>"`
   plus a **task prompt** (the specific job this time).
3. **Execute** — a fresh Claude boots with the file's body as its system prompt,
   sees only what the task prompt tells it (not the caller's conversation), uses
   only its granted tools, and runs autonomously to completion.
4. **Return** — its final message becomes the caller's tool result. The agent
   then evaporates; it keeps no memory for next time (unless kept alive and
   continued mid-run).

**There are two prompts in play:** the *system prompt* (the file body — stable,
the role) and the *task prompt* (passed at invocation — variable, the specific
job). The file defines *what kind of agent it is*; the call defines *what it
does this time*.

### The four design levers

Designing an agent is really setting four things:

1. **The system prompt (the body).** The role and the standard it works to.
2. **Tool access (least privilege).** Grant only what the job needs — this is a
   security boundary, not a convenience setting (Part 3).
3. **The model.** Match the model tier to how much reasoning the job needs.
4. **Context isolation — fresh vs. fork.** A normal spawn gets a **blank**
   context (independence). A "fork" *inherits the caller's whole conversation* —
   the opposite of what an independent reviewer wants, because it would see all
   of the caller's reasoning and lose its fresh-eyes value.

---

## Part 2 — The tools, and why narrow tools exist alongside Bash

Five tools, and the purpose of each:

- **Read** — reads one file. Like `cat -n` (returns numbered lines), but also
  renders images visually, reads PDFs by page range, and parses notebooks.
- **Grep** — content search built on **ripgrep**. Regex, file-type/glob filters,
  context lines, and output modes (matching lines / filenames / counts).
  Essentially `rg` with structured output.
- **Glob** — filename matching by pattern (`**/*.html`), returns paths sorted by
  modification time. Like `find -name`, faster and consistent.
- **Bash** — the actual shell. Runs any command, including `grep`, `find`,
  `cat`, and `rm`. The general-purpose escape hatch.
- **Skill** — *not a file tool.* It loads a skill's playbook (e.g.
  `/rigorous-explainer`) into the agent's context, so the agent knows a standard
  or procedure to follow.

### The natural question: why Read/Grep/Glob when Bash can do all of it?

Bash *can* run `cat`/`grep`/`find`. The dedicated tools exist for five reasons:

1. **Safety and blast radius (the big one).** Read/Grep/Glob are structurally
   **read-only** — no argument to Read can delete a file. Bash is a firehose: one
   grant potentially allows `rm -rf`, network calls, anything. So the read-only
   tools can be allowed freely with few prompts, while Bash is gated harder.
   **This is the basis of least-privilege agent design:** an agent given only
   Read/Grep/Glob *cannot* mutate files, no matter what goes wrong.
2. **Structured output the harness relies on.** Read returns line-numbered
   content *and registers that the agent has seen the file's exact current
   bytes.* **Edit depends on this contract** — it refuses to edit a file the
   agent has not Read, and detects if the file changed underneath. A `cat`
   through Bash establishes none of that. Grep returns clickable `file:line`
   links; raw `grep` stdout is just text.
3. **Portability.** These tools behave identically on Windows, macOS, and Linux.
   (On Windows, `grep`/`find` are not native — they exist only via Git Bash,
   with differences.) ripgrep-backed Grep and Glob work the same everywhere.
4. **Context-budget guardrails.** Grep has head-limits and output modes; Read
   caps lines. A runaway `grep -r` in Bash can dump tens of thousands of lines
   into a finite context window. The dedicated tools are shaped for that limit.
5. **Non-text rendering.** Read shows a PNG or PDF page as an image; `cat` on a
   PNG gives binary garbage.

### The mental model

**Narrow tools vs. the escape hatch:**

- **Read / Grep / Glob** = narrow, read-only, structured, portable, safe. Reach
  for these by default.
- **Bash** = the escape hatch for real shell work with no dedicated tool —
  running scripts, `git`, Python, build tools.

Use the narrow tool when one fits; drop to Bash only when you genuinely need the
shell. It is the Unix principle of least privilege applied to an agent's
toolbox: you *could* do everything as root with a shell, but you don't, because
the narrow, unprivileged path is safer and its output is cleaner.

---

## Part 3 — How the agent decides which tool to use

There are **two layers**, and only one is a guarantee.

### The soft layer — bias, not enforcement

Most of the time the agent picks the narrow tool because it is *steered* to,
three ways:

1. **The tool descriptions tell it to.** Instructions travel *with* each tool.
   The Bash tool's own description says to avoid using it for `find`/`grep`/
   `cat`/`head`/`tail`/`sed` and to use the dedicated tool instead; Grep's
   description says to prefer it over `grep`/`rg` via Bash. The model reads these
   each time and is trained to follow tool and system instructions.
2. **Training instilled the habit.** The model was post-trained to reach for
   Read/Grep/Glob by default.
3. **The narrow tools are genuinely easier.** Structured, parseable output and
   fewer permission prompts (being read-only, they are often auto-allowed). The
   path of least resistance *is* the narrow tool.

But all three are **probabilistic**. They make "Bash for everything" unlikely,
not impossible. An LLM is not a deterministic program; nothing at the moment of
choosing forces its hand.

### The hard layer — the only guarantee

The one non-probabilistic fact: **if a tool is not in the agent's granted
`tools` list, it does not exist for that agent and cannot be chosen.** An agent
given only `Read, Grep, Glob` has no Bash in its toolbox — the question "will it
pick Bash?" never arises, exactly like a Unix process without a capability
simply cannot invoke it.

### The through-line

**Safety comes from removing the tool, not from trusting behavior.** If you want
the guarantee "this agent provably cannot mutate my files," you do not achieve
it by writing "please don't edit" in the prompt (soft) — you achieve it by not
granting Write, Edit, or Bash (hard). The absence of the tool *is* the
enforcement. The agent usually picks the right tool because it is instructed and
trained to; but when the stakes are safety rather than tidiness, you never rely
on "usually" — you remove the tool and turn a tendency into a certainty.

---

## Applying all of this to the reviewer agent

- **It is one file:** `.claude/agents/rigor-reviewer.md`.
- **`description`:** dispatch after a section's hardening scripts pass, to judge
  the things scripts cannot (rigor parity, read-aloud prose, K-problem depth,
  self-containment).
- **`tools`:** `Read, Grep, Glob, Skill` — deliberately **no Write, Edit, or
  Bash**, so it is provably read-only. It judges; it does not rewrite. (Bash was
  considered, only so it could re-run the scripts itself; dropped because that
  re-widens the blast radius, and the scripts already run in the caller's loop
  before the reviewer is dispatched.)
- **`model`:** `fable` — judging rigor is reasoning.
- **Context:** fresh, never a fork — independence is the whole point.
- **Body:** the four judgment checks, the acceptance standard (loaded via `Skill`
  from `/rigorous-explainer`), and a structured findings format.

The reviewer's independence and safety are not hopes about good behavior — they
are consequences of a fresh context and a deliberately narrow tool list.
