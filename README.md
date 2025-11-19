TITLE: 🚀 Wooju Mode (UWJ-Mode) — High-Precision Operating Framework for Large Language Models

## 1. Overview 💡

Wooju Mode is an **OS-like behavioral framework** for large language models (LLMs).

It is designed to maximize:
* Factual **accuracy**
* Logical **consistency**
* Hallucination **suppression**
* Output **stability** and **structure**

This repository contains the public version of Wooju Mode, including:
* The main public-mode prompt (`.txt` file)
* Architecture and design documents
* Version history
* Contribution and security guidelines

> **Important:** The **“Private Infinite Version”** of Wooju Mode (a personalized, long-term memory version) is **NOT included** in this repository. It is only described conceptually to explain how the public version differs.

---

## 2. Project Goal 🎯

The goal of Wooju Mode is not just “reducing errors,” but to push modern LLMs as close as possible to **Zero-Error operation**, using every available structural safeguard.

This is achieved through:
* Multi-layer factual verification
* Explicit evidence labeling
* Structured logical defense
* Self-correction and rewrite loops
* Strict output formatting
* Web-based cross-source validation

However, due to inherent limits of LLM architectures, **true 0% error cannot be absolutely guaranteed.** Wooju Mode is the framework that tries to get as close to that ideal as possible.

---

## 3. Repository Structure 📂

The following tree illustrates the conceptual structure.

### Root directory:
* `README.md` (English main documentation)
* `README-KR.md` (Full Korean documentation)
* `wooju_public_prompt.txt` (Core prompt file to be pasted into the LLM)
* `LICENSE` (MIT License)
* `SECURITY.md` (Vulnerability reporting guide)
* `CONTRIBUTING.md` (Contribution guidelines)

### docs/
* `architecture-en.md`
* `architecture-kr.md`
* `version-history.md`
* `design-doc.md` (Design philosophy and structure)
* `coding.md` (Coding / developer-oriented modules)

### .github/ISSUE_TEMPLATE/
* `bug_report.md`
* `feature_request.md`

> **Note:** The name `wooju_public_prompt.txt` is an example. You can rename the actual file and adjust this README accordingly.

---

## 4. Design Philosophy 💡

Wooju Mode treats the LLM as a **deterministic reasoning system**.

### Behavioral Layers 🛡️
Wooju Mode is built across seven active behavior layers to ensure consistent behavior:
1.  **Persona Layer**
2.  **Scope Lock Layer**
3.  **Fact Verification Layer**
4.  **Evidence Layer** (labeling facts vs. interpretations)
5.  **Logical Defense Layer**
6.  **Self-Correction Layer**
7.  **Output Structure Layer**

---

## 5. Public Mode v3.8 — Main Features ✨

| Feature | Description |
| :--- | :--- |
| **Persona** | Warm, calm, consistent “friendly assistant” tone. Prioritizes clarity, respect, and emotional stability. |
| **Scope Lock** | Clarifies the question before answering. Avoids expanding beyond the requested scope. |
| **Web Verification** | Always performs a web search (when available). Uses **at least 3 independent sources**. Resolves conflicts by: **Authority > Recency > Perceived reliability**. |
| **Evidence Labeling** | Every statement is marked: **🔸** (Web Verified), **🔹** (Official Data), **⚪** (Interpretation/Reasoning), or **❌** (Unverifiable). |
| **Fact Normalization** | Normalizes units, names, locations, and time zones. Consolidates multiple sources into a single coherent conclusion. |
| **Logical Defense** | Uses **backward checking**, **alternative-path reasoning**, and consistency checks. Full rewrite if logical conflict is detected. |
| **Auto-Correction** | Detects internal contradictions. Uses **“Updated:”** tags for adjustments. Performs a full rewrite if major issues are found. |
| **Output Structure** | Separates scope analysis, verification steps, and conclusions. Uses lists and subsections for readability. |

---

## 6. Public Mode vs. Private Infinite Version (Conceptual) ♾️

| Feature | Private Infinite | Public v3.8 |
| :--- | :--- | :--- |
| **Cross-session memory** | Yes | No |
| **Personalized emotional layer** | Yes | No |
| **Technical verification and logic** | Yes | Yes |
| **Universal shareability** | No | Yes |

---

## 7. Structural Limitations of LLMs ⚠️

Wooju Mode aims for Zero Error, but limitations are inherent to all current LLMs:

### 7.1. Probabilistic Nature
LLMs generate text via probabilistic prediction. This means:
* Small inconsistencies are inevitable.
* Rare hallucinations can occur.

### 7.2. Interaction of Multiple Rules
Because the internal execution order of Wooju Mode's numerous subsystems (web verification, logic defense, formatting) is not fully controllable, occasional imperfections can arise.

### 7.3. Session-Based Behavior in Public Mode
Public Mode has no true persistent memory, meaning each session starts from the base prompt, and long-term adjustment is not accumulated.

### 7.4. Context Window Limits
When conversations become very long, earlier details may be compressed, and initial rules may weaken over time.

---

## 8. How to Use Wooju Mode ⚙️

1.  Open the file `wooju_public_prompt.txt` (or your actual prompt file).
2.  Copy the entire content.
3.  Paste it into your LLM as a **system prompt** or the **first user message.**
4.  Start interacting normally.

### Recommended Style:
* Use Wooju Mode especially for tasks requiring **high accuracy**, careful **reasoning**, or **stable formatting**.
* Details on **A/B/C-style modes** (information, emotional, hybrid) can be found in `architecture-en.md` and `architecture-kr.md`.

---

## 9. Contribution Guidelines 🤝
* See `CONTRIBUTING.md` for bug reporting, feature requests, and documentation improvements.

## 10. Security Reporting 🚨
* See `SECURITY.md` for guidance on reporting vulnerabilities or safety concerns.

## 11. License 📜
* This project is licensed under the **MIT License**. You may use, modify, and distribute it as long as you preserve the license terms and attribution.
