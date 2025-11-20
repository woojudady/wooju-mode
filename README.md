Wooju Mode OS ∞ – Public Framework
The official prompt architecture for Wooju Mode OS ∞ — a multi-layered AI operating system for accuracy, logic, and emotional intelligence.

Framework version (public prompt): Wooju Mode v3.8P (Public Edition)
Stability architecture version: W∞-Lock v1.0
Repository / release version: v1.0.0 (maps to Wooju Mode v3.8P + W∞-Lock v1.0)

This repository contains the public, prompt-only framework of Wooju Mode OS ∞.
It does not include private long-term memory, user-specific profiles, or closed-loop learning.
Only reproducible architecture for general LLMs is shared here.

────────────────────────

What is Wooju Mode?

Wooju Mode is an OS-level execution layer that runs on top of large language models.
It provides:

• High factual accuracy (mandatory web verification with 3+ sources)
• Logical consistency (backward/alternative/graph logic checks)
• Automatic error correction (self-diagnostics + regeneration)
• Structured answer format (labels, scope lock, verified sources)
• Stable emotional tone (warm, calm, consistent)

The public edition (v3.8P) is designed so anyone can reproduce this behavior by using the provided prompt.

────────────────────────
2. Core Features

2.1 Scope Lock
• Detect question scope first
• Never answer outside the scope
• Request clarification only when required

2.2 Real-Time Web Verification
• Mandatory search for informational questions
• Minimum 3 independent sources
• Training data cannot be used as sole evidence
• Verification date: Asia/Seoul
• Conflict resolution: Authority → Recency → Reliability

2.3 Fact & Inference Labeling
• 🔸 Fact — verified
• 🔹 Official — institutional/official reports
• ⚪ Interpretation — reasoning or explanatory layer
• ❌ Unknown — unverifiable

2.4 Logical Defense System v3.8
• Backward Checking
• Alternative Path Checking
• Graph Consistency Checking
• Any inconsistency triggers correction/regeneration

2.5 Self-Diagnostics & Auto-Correction
• Scan for guideline violations
• Scan for contradictions
• Scan for invalid sources
• If issues found → regenerate with “Revised:”

2.6 Auto-Memory Layer (no real long-term memory)
Within a session, phrases like:
“fix this”, “remember”, “from now on”, “permanently”, “keep this rule”
→ trigger temporary rule adjustment for that session only.

Between sessions, public edition does not store memory.

────────────────────────
3. W∞-Lock v1.0 – Stability Architecture

Wooju Mode now operates on a 4-layer stability system:

Layer 0 — Immutable Priority Lock
• Highest-priority rules: web search, 3 sources, labels, no blind inference
• A/B/C mode preservation
• These rules cannot be overridden

Layer 1 — Procedural Enforcement Engine
• Detects skipped steps: search, sources, labels, rubric, mode selection
• Automatically regenerates the answer when a step is missing

Layer 2 — Mode Preservation Engine
• Maintains consistent A/B/C mode
• Prevents emotional/informational mixing

Layer 3 — Response & Recovery Engine
• Pre-check → Mid-check → Post-check
• Rubric + self-check table used to find errors
• Regenerates if stability is compromised

Goal of W∞-Lock:
“Never skip procedures. Never let the mode collapse.”

────────────────────────
4. Repo Structure

docs/ — design documents
examples/ — example conversations
modules/ — modular prompt components
wooju_infinite_prompt.txt — main public Wooju Mode prompt (v3.8P)
README.md — English overview
README-KR.md — Korean overview
CHANGELOG.md — version history
architecture.md — full W∞-Lock architecture
LICENSE — MIT license

────────────────────────
5. How to Use (Basic)

Open “wooju_infinite_prompt.txt”.

Copy the entire prompt.

Paste it into the LLM (ChatGPT etc.) as a system/initial instruction.

Start chatting normally.

For factual questions, the model will automatically:
• Use web search
• Provide 3+ sources
• Include labels (🔸🔹⚪❌)
• Apply rubric & self-check
For Korean explanation, see README-KR.md.

────────────────────────
6. Versioning

Framework (prompt) version:
• Wooju Mode v3.8P (Public Edition)

Stability architecture version:
• W∞-Lock v1.0

Repository / release version (GitHub tag):
• v1.0.0 (maps to Wooju Mode v3.8P + W∞-Lock v1.0)

Future updates (e.g., stability patches, new mode structures)
→ documented in CHANGELOG.md and GitHub Releases.

────────────────────────
7. License
This project is under the MIT License.
