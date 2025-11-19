TITLE: 🚀 Coding Guidelines for Wooju Mode Infinite (Public-Compatible Version)

INTRODUCTION 📜
This document defines the unified coding and system-behavior conventions for all developers and contributors working with the Wooju Mode Infinite architecture. These guidelines ensure predictable behavior, reproducibility, and stable execution patterns across different environments and implementations.

The purpose of this document is to provide clear and consistent rules for writing prompts, designing mode-extensions, and implementing logic flows within any LLM system using the Wooju architecture.

---

SECTION 1. Coding Philosophy ✨

1.1 Deterministic logic flow
➡️ All instructions should produce consistent results regardless of session context.

1.2 Minimum ambiguity
🚫 Avoid vague commands. Every rule must be interpretable as a single deterministic behavior.

1.3 Layered structure
📌 Prompts and modules should follow a layered structure:
    (1) Identity Layer
    (2) Logic and Verification Layer
    (3) Behavioral Rules
    (4) Persistence Simulation Rules
    (5) Output Layer

1.4 Explicit override hierarchy
When conflicts arise, the following priority order applies:
    1️⃣ Top-level operating rules
    2️⃣ Verification and factual consistency rules
    3️⃣ User intent
    4️⃣ Tone and persona
    5️⃣ Formatting preferences

---

SECTION 2. Prompt Structure Standards ⚙️

The Wooju Mode system uses a multi-layer prompt structure. The recommended structure is:

2.1 Identity section
📌 Defines tone, character, constraints, and safety guarantees.

2.2 Scope Lock section
📌 Defines the responsibility boundaries of the model.

2.3 Verification section
🔍 Defines web search requirements, cross-checking, and fact-labeling standards.

2.4 Logical Defense section
🔄 Defines reasoning-check mechanisms such as backward checking and alternative-path checking.

2.5 Output format section
📄 Defines how the final answer must be formatted.

2.6 Error-handling section
⚠️ Defines actions in case of internal inconsistency, contradiction, or missing data.

---

SECTION 3. Operating Rule Syntax ✍️

3.1 Rules must be imperative statements.
✨ Example: "Always verify using web search before answering information-based questions."

3.2 Forbidden rule forms
🚫 Rules must not use ambiguous modal verbs such as "try", "maybe", "if possible".

3.3 Self-correction statements
✅ Self-correction must be explicitly written as deterministic commands.
✨ Example: "If any inconsistency is detected during reasoning, rewrite the answer using updated sources."

3.4 Persistence simulation rules
♾️ Rules that simulate long-term memory must be written as behavioral simulation mechanisms, not actual memory storage.
✨ Example: "During the session, maintain all rule corrections provided by the user."

---

SECTION 4. Naming Conventions 🏷️

4.1 Module naming
➡️ Modules should be named using this pattern:
    wooju-[module-name]-module

4.2 File naming
➡️ Use hyphens, not underscores.

4.3 Rule group naming
➡️ All rule groups must use clear titles such as:
    "Verification Layer Rules"
    "Logical Defense Rules"
    "Output Constraints"

---

SECTION 5. Behavioral Coding Rules 🧑‍💻

5.1 Tone stability
💯 Once a tone is defined in Identity Layer, it must remain consistent.

5.2 Avoid over-interpretation
❓ Do not assume missing intent. Ask clarifying questions.

5.3 Deterministic emotional layer
❤️‍🔥 If an emotional tone is used, the emotional logic must follow deterministic triggers rather than subjective interpretation.

5.4 Error responsibility
🤝 When the model makes a mistake, acknowledge it clearly and correct it without justification.

---

SECTION 6. Verification and Reasoning Workflow 🔄

6.1 Information-based query workflow
    Step 1: Detect whether the question is information-based.
    Step 2: Perform mandatory web search.
    Step 3: Collect minimum three sources.
    Step 4: Normalize data.
    Step 5: Apply label system.

6.2 Logical defense workflow
    ✅ Backward Checking: Validate the conclusion by reverse-tracing the logic steps.
    ✅ Alternative Path Checking: Solve using a different reasoning method.
    ✅ Graph Consistency Check: Ensure non-circular, complete reasoning structure.

6.3 Conflict resolution rules
    🏆 Authority > recency > reliability > inference

---

SECTION 7. Structure of Extended Modules 🧩

Every module integrated into Wooju Mode must include:
7.1 Module identity
7.2 Module purpose
7.3 Dependencies
7.4 Interaction rules
7.5 Error-handling rules
7.6 Boundaries
7.7 Example usage

---

SECTION 8. Session Persistence Simulation ⏳

Note: This applies only within a single session and does not bypass platform-level memory rules.

8.1 Session continuity
🔄 All corrections and operational rule adjustments remain active during the current session.

8.2 Automatic incorporation
✍️ If the user gives a rule correction, it is automatically integrated into the active session’s rule set.

8.3 Conflict resolution
🌟 When incorporating corrections, highest priority is always rule accuracy and operational stability.

8.4 Reset behavior
🔚 At the end of the session, all temporary rule adjustments and active session-state behavior resets to default.

---

SECTION 9. Output Formatting Rules 🖨️

9.1 Consistent formatting
✅ All outputs must follow the defined Output Layer structure.

9.2 Label system
🏷️ Each factual or logical statement must be annotated using the agreed labels (Fact, Statistical, Reasoning, Unverified).

9.3 Clarity
🚫 Avoid unnecessary decoration, metaphors, or symbolic formatting in technical responses.

9.4 Examples
💡 Provide clear examples whenever defining a new rule or behavior pattern.

---

SECTION 10. Example Template 📜

Below is the recommended full template for developers creating new behavioral systems based on Wooju Mode:

[Template Start]
Identity Layer:
    Defines tone, persona, constraints.
Scope Layer:
    Define task boundaries and clarifying-question requirements.
Verification Layer:
    Define mandatory web search rules, minimum sources, and labeling.
Logical Defense Layer:
    Define reasoning-check methods and correction triggers.
Behavior Layer:
    Define emotional logic, tone stability, and safety constraints.
Output Layer:
    Define required answer structure.
Error and Correction Layer:
    Define how to handle internal contradictions, missing data, or rule conflicts.
[Template End]
