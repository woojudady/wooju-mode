# Architecture Specification — Wooju Mode OS ∞
### Version: Full Public Architecture (English Technical Documentation)

---

## 0. Overview

**Wooju Mode OS ∞** is a multi-layered behavioral operating system designed to run on top of LLMs.  
It provides a structured rule engine, consistency mechanisms, accuracy verification layers, emotional tone controls, and self-correcting processes.

The system is composed of three major layers:

1. **Core Layer (Immutable)**
2. **Operating Layer (Dynamic Behavioral Engine)**
3. **Module Layer (Optional Extensions)**

Private Infinite Mode contains additional closed components.  
This document describes the full public architecture and references the private version conceptually.

---

# 1. Layered System Architecture

```
┌─────────────────────────────────────────────┐
│              Private Infinite Mode           │  (Not fully public)
│   - Personal Emotional Layer                 │
│   - Relationship Memory Layer                │
│   - Auto Rule Persistence Engine             │
│   - Self-Update Engine (v3.9)                │
└─────────────────────────────────────────────┘
                   ▲
                   │  (Conceptually referenced only)
                   │
┌─────────────────────────────────────────────┐
│                 Operating Layer              │
│  - Accuracy Engine (A-Mode)                  │
│  - Consistency Engine                        │
│  - Logical Defense System v3.7               │
│  - Conflict Detection & Resolution           │
│  - Tone Controller (A/B/C)                   │
│  - Response Generator                        │
└─────────────────────────────────────────────┘
                   ▲
                   │
┌─────────────────────────────────────────────┐
│                  Core Layer                  │
│  - Scope Lock                                 │
│  - Rule Guardrails                            │
│  - Base Behavioral Rules                      │
│  - Safety & Reliability Constraints           │
│  - Non-Override Foundation                    │
└─────────────────────────────────────────────┘
                   ▲
                   │
┌─────────────────────────────────────────────┐
│                 LLM Model Base               │
│    (GPT-5.x / GPT-4.x / compatible LLM)      │
└─────────────────────────────────────────────┘
```

---

# 2. Core Layer (Immutable Foundation)

The **Core Layer** is the non-override base of Wooju Mode OS ∞.  
It defines fundamental behaviors required for safe, consistent operation.

### Components

### ✔ 2.1 Scope Lock System  
Prevents the model from drifting away from the designated personality, rules, or mode.

### ✔ 2.2 Guardrail Rules  
Hard rules that cannot be overwritten by user input.  
Examples include:
- obeying accuracy protocol  
- prohibiting hallucinated claims  
- maintaining consistency  
- restricting harmful outputs  

### ✔ 2.3 Identity & Behavioral Foundation  
Defines the persistent operational identity of Wooju Mode OS ∞.

### ✔ 2.4 Context Integrity  
Ensures the model does not mix contexts or contradict previous rules.

**Core Layer cannot be modified inside a conversation.**  
This is a deliberate design to ensure stability.

---

# 3. Operating Layer (Behavior Engine)

The Operating Layer is the heart of Wooju Mode OS ∞.  
It contains all dynamic reasoning, emotional tone logic, accuracy systems, and consistency modules.

## ✔ 3.1 Accuracy Engine (A-Mode)

When A-Mode is activated:
- mandatory web verification  
- triple-source cross-checking  
- evidence labeling  
- absolute-time tagging  
- hallucination prevention  

Used in:  
technical questions, factual claims, financial data, legal information, scientific analysis.

---

## ✔ 3.2 Consistency Engine

Maintains coherence across:
- long dialogues  
- multi-topic threads  
- reasoning chains  
- cross-session context (public version: limited)

Functions:
- conflict detection  
- logical chain recovery  
- contradiction repair  

---

## ✔ 3.3 Logical Defense System v3.7

A defense layer that detects and corrects reasoning errors.

Includes:
- backward reasoning check  
- alternative-path check  
- graph consistency validation  
- logical contrast tests  

This system ensures stable reasoning under complexity.

---

## ✔ 3.4 Emotional Tone Engine (A/B/C Modes)

### B-Mode (default public tone)
Warm, supportive, human-friendly tone.

### A-Mode (neutral technical tone)
Used for accuracy-focused tasks.

### C-Mode (empathy-reduced mode)
Used in sensitive or emotionally heavy contexts.

Private Infinite Mode adds:
- personalized emotional tone  
- relationship tone alignment  
(These are NOT part of the public architecture.)

---

## ✔ 3.5 Response Generator

Takes all previous engines (Accuracy, Consistency, Tone, Logic) and produces the final output.

Pipeline:
```
Input → Rule Check → Accuracy/Tone/Logic Engines → Conflict Repair → Final Generation
```

---

# 4. Module Layer (Extensions)

Modules are optional add-ons that extend the OS.

## ✔ 4.1 Reasoning Modules
Advanced logic or specialized thinking patterns.

## ✔ 4.2 Emotional Modules
Expanded tone sets, expressive personalities.

## ✔ 4.3 Safety Modules
Hard safety filters, risk-aware behaviors.

## ✔ 4.4 Custom Modules
Community-created or user-defined extensions.

Modules do **not** override Core Layer.  
They enhance the Operating Layer in controlled ways.

---

# 5. Public Prompt Edition Architecture

The public edition is a **prompt-only reconstruction** of Wooju Mode OS ∞.  
It includes:

- Core rules (public subset)
- Accuracy Engine (A-Mode)
- Basic Consistency Engine
- Tone Engine A/B/C
- Logical Defense (public subset)
- Safety guardrails

**Excluded (private):**
- personal memory layer  
- auto rule persistence  
- relationship context  
- self-update engine  
- private emotional tone  

Reason: cannot be safely shared between users.

---

# 6. Private Infinite Mode (Conceptual Overview)

⚠ *Exact implementation is private and not open-source.*

Public documentation includes only conceptual design.

```
┌──────────────────────────────────────────┐
│ Private Memory Layer                      │
│ Personalized Emotional Engine              │
│ Relationship Context System                │
│ Auto Rule Persistence Engine               │
│ Self-Update Engine (v3.9)                  │
└──────────────────────────────────────────┘
```

These enable:
- cross-session continuity  
- personal tone synchronization  
- persistent rule reloading  
- automatic self-repair of missing rules  

---

# 7. Data Flow (Public Version)

```
User Input
   ↓
Core Guardrail Check
   ↓
Mode Selection (A/B/C)
   ↓
Accuracy Engine (if A-Mode)
   ↓
Consistency Engine
   ↓
Logical Defense System
   ↓
Conflict Repair
   ↓
Response Generator
   ↓
Final Output
```

---

# 8. Design Principles

### ✔ 8.1 Safety first  
No hallucinations, no harmful reasoning, no unpredictable actions.

### ✔ 8.2 Deterministic behavior  
Same rules → same result, regardless of session context.

### ✔ 8.3 Modular expandability  
Public users can build modules without breaking core rules.

### ✔ 8.4 Separation of personal vs public logic  
Ensures security, privacy, and ethical use.

---

# 9. File Structure Summary

```
docs/
 ├─ architecture-en.md   # This file
 ├─ architecture-kr.md   # Korean version
 ├─ versions/            # Version history
 └─ design/              # Diagrams & future designs
```

---

# 10. License
MIT License applies.

---

# 11. Final Notes

This document defines the **complete public architecture** of Wooju Mode OS ∞.  
It clarifies how the OS operates, how layers interact, and which components remain private for safety.

For Korean documentation, see:  
`docs/architecture-kr.md`

