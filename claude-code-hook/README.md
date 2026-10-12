# Wooju Mode v4.0 — Claude Code Hook Edition

Enforces the Wooju Mode v4.0 rules with **Claude Code hooks** instead of relying on the model to remember a prompt.
Full documentation (Korean): [README-KR.md](README-KR.md)

**Why:** a system prompt only works while the model remembers it. In long tool-heavy Claude Code sessions the rules
fade, and nothing checks whether labels (🔸🔹⚪❌) actually point at evidence that was opened. Hooks turn the
machine-checkable parts into gates the answer must pass.

**How:**

| Hook event | Command | Role |
|---|---|---|
| `UserPromptSubmit` | `wooju_mode.py inject` | Re-injects the rule summary every message |
| `MessageDisplay` | `wooju_mode.py display` | Holds the final answer, has a read-only Opus reviewer (`claude -p`) cross-check evidence before it is shown |
| `Stop` | `wooju_mode.py check --warn` | Format checks; blocks the first rejected answer so it is fully rewritten with `Revised:` (second rejection is shown with a warning) |

Install: copy both files to `~/.claude/hooks/`, run `python ~/.claude/hooks/wooju_mode.py install`,
then `python test_wooju.py` (offline, fake reviewer). Requires Python 3.12+ and the `claude` CLI on PATH.
