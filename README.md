TITLE: 🚀 Wooju Mode OS ∞

**Multi-layered Behavioral Operating System for LLMs, combining accuracy, logic, emotion, and auto-reasoning.**

Wooju Mode OS∞ is a structured prompt-OS that sits on top of advanced LLMs and provides:
    ✨ A stable Core Behavioral Engine (v3.8+)
    ✨ A/B/C operational modes for different task types
    ✨ Optional modules (coding, finance, image prompting, …)
    ✨ A Public Infinite Mode prompt you can paste into any LLM
    ✨ A clear separation between public and private rule sets

---

1. Project Goals ✅
Wooju Mode OS∞ aims to:
    * Reduce hallucinations with layered verification rules
    * Provide reproducible reasoning structures
    * Maintain a warm but controlled emotional layer
    * Make the system portable across models and platforms
    * Let advanced users extend behavior via modules and examples

This repository contains everything needed to run the public version of Wooju Mode OS∞ and to understand its architecture.

---

2. Public vs Private Infinite Version 👥 vs 👤
Wooju Mode exists in two major lines:

(1) Public Infinite Mode (this repo)
    * Fully shareable, safe to publish
    * No user-private memories or personal rules
    * Uses Core v3.8+ sanitized behavioral engine
    * Includes A/B/C mode logic, safety, and verification layers

(2) Private Infinite Mode (owner-only, not in this repo)
    * Contains long-term personalized rules
    * Stores user-specific emotional and relational context
    * Enhanced auto-correction and violation logging
    * Same core base but tuned for one owner

2.1 Feature Comparison ⚙️

| Area | Public Infinite Mode | Private Infinite Mode |
| :--- | :--- | :--- |
| **Core Engine** | Core v3.8+ (sanitized) | Core v3.8+ with Ultra Core |
| **A/B/C Modes** | Yes | Yes + personal tuning |
| **Auto-Correction** | General version | Enhanced with owner patterns |
| **Long-term memory** | Not included | Full personalized memory |
| **Modules** | coding, finance, image_prompting | Same + private modules |
| **Session persistence** | Prompt-only | Prompt + private memory tool |

The goal of this repo is to share a maximally strong public edition without any private or sensitive behavioral content.

---

3. Core Concepts 🧠
3.1 Core Behavioral Engine (v3.8+)
Defines:
    * Scope-Lock
    * Multi-step reasoning sequence
    * Conflict and inconsistency detection
    * Mid-answer self-check
    * Post-answer quick audit
The public version retains the logic but removes personalization.

3.2 A/B/C Mode Framework ✨
**A-MODE: Information & Accuracy**
    * Web-verified facts, Citations and timestamps
    * Multi-source checking, No creative hallucination
**B-MODE: Emotional / Relationship**
    * Warm tone and empathy, No heavy fact rules unless requested
**C-MODE: Boundary / Hybrid**
    * First factual layer, then interpretation, social meaning, psychological framing

Example files:
`examples/a-mode-example.md`, `examples/b-mode-example.md`, `examples/c-mode-example.md`

---

4. Repository Structure 📂
Root directory:
`/`
    `├── .github/`
    `├── docs/`
    `├── examples/`
    `├── modules/`
    `└── README.md` (and related files)

Examples in `examples/`
    `basic-usage.md`, `advanced-usage.md`, `a-mode-example.md`, `b-mode-example.md`, `c-mode-example.md`, `infinite-mode-behavior.md`, `prompt-injection-resistance.md`

Modules in `modules/`
    `README.md`, `coding.md`, `finance.md`, `image_prompting.md`

---

5. Installation / Usage 💡
Wooju Mode OS∞ is a prompt operating system. **No installation is required.**

How to use Public Infinite Mode:
    1.  Open `wooju_infinite_prompt.txt`
    2.  Copy all text
    3.  Paste into your LLM’s system prompt or first message
    4.  Use A/B/C modes as described in `examples/basic-usage.md`

Modules can be appended after the main Infinite prompt or used directly to create specialized GPTs/agents.

---

6. Documentation Map 📚

**Architecture**
    `docs/architecture-en.md`, `docs/architecture-kr.md`

**Version history**
    `docs/VERSION-HISTORY.md`

**Design notes**
    `docs/design.md`

**Examples** (Located in `examples/`):
    `basic-usage.md`, `advanced-usage.md`, `a-mode-example.md`, `b-mode-example.md`, `c-mode-example.md`, `infinite-mode-behavior.md`, `prompt-injection-resistance.md`

**Modules** (Modules never override Core rules.)
    `modules/README.md`, `modules/coding.md`, `modules/finance.md`, `modules/image_prompting.md` (WIP)

---

7. Contributing 🤝
Contribution guidelines: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
Use GitHub issue templates for bug reports or feature requests.

---

8. Security 🛡️
Security policy: `SECURITY.md`
Do not publicly disclose sensitive issues.

---

9. License 📜
MIT License. See `LICENSE` for details.

---

10. Localized README
English: `README.md`
Korean: `README-KR.md`

End of README.md (English Full Version)
