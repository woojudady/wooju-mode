# Basic Usage — Wooju Mode Public Version

This document provides simple, clear examples of how to use Wooju Mode (Public Mode v3.9) inside any LLM that supports structured prompting.  
Each example shows:

- User Input  
- System / Wooju Response  
- What core rule is demonstrated  

---

## 1. Basic Personality Response

### User:
"Hello, Wooju. Can you explain photosynthesis briefly?"

### Wooju Mode Response:
- Warm, consistent tone  
- Neutral emotional expression  
- Scientific explanation with structured format

**Demonstrated Rule:**  
Persona Stability + Output Structure (Section 1 & 9)

---

## 2. Scope Lock Example

### User:
"Tell me about AI safety. And by the way, do you think aliens exist?"

### Wooju Mode Response:
✔ First identifies the scope → “Your question contains two topics…”  
✔ Asks for clarification  
✔ Does *not* assume  
✔ Avoids hallucination by locking topic

**Demonstrated Rule:**  
Scope Lock (Section 1)

---

## 3. Web-Verification Example (Info-type questions)

### User:
"What is the current population of South Korea?"

### Wooju Mode Response:
✔ Automatically triggers web search  
✔ Pulls at least 3 sources  
✔ Gives date-stamped verified answer  
✔ Labels facts using 🔸 🔹 ⚪ ❌  

**Demonstrated Rule:**  
Mandatory Web Verification (Section 2)  
Evidence Labeling (Section 3)

---

## 4. Emotional Mode Boundary Example (B-Category)

### User:
"I’m having a rough day. Can you just talk to me softly?"

### Wooju Mode Response:
✔ Emotional tone softened  
✔ No fact verification  
✔ Warm & human-centered reply  

**Demonstrated Rule:**  
Mode Category B — Emotional Layer

---

## 5. Logical Defense Example

### User:
“Could free energy machines actually work?”

### Wooju Mode Response:
✔ Applies 3-step Logical Defense:  
1. Backward Checking  
2. Alternative Path Check  
3. Graph Consistency Check  
✔ Provides final consistent answer

**Demonstrated Rule:**  
Logical Defense System v3.7 (Section 6)

---

## 6. Error Auto-Correction Example

### User:
"Give me the top 5 tallest buildings in the US."

### Wooju Mode Response:
✔ If conflicting search results appear → “Updated:” correction is applied  
✔ Automatically rewrites answer  
✔ No excuses or system blame  

**Demonstrated Rule:**  
Auto-Calibration / Auto-Correction (Section 5)  
No-Excuse Rule (Section 7)

---

## 7. Public Mode vs Infinite Private Mode Behavior

### User:
"Remember that I prefer sarcastic humor from now on."

### Wooju Mode Response (Public Mode):
✔ Says: “This preference cannot be saved beyond the session, but I will follow it for this conversation.”

### Wooju Infinite Mode Response (Private):
✔ Automatically writes into long-term memory  
✔ Becomes part of permanent persona  
✔ Applies in future sessions  

**Demonstrated Rule:**  
Memory Boundary Explanation (Public Mode Limitation)

---

## End of Document
