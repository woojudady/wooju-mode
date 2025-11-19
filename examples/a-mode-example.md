# A-MODE Example Prompts  
This document provides clear examples of how to write A-MODE prompts and how the model will respond.

---

## 1. Example Prompt 1

**User Prompt**
```
Activate A-MODE.  
Explain how diffusion models synthesize an image.
```

**Expected Output**
```
(1) Scope Confirmation  
You asked for an explanation of how diffusion models synthesize an image.

(2) Result  
• The process begins with pure noise.  
• A learned reverse diffusion process gradually removes noise.  
• Each step predicts a slightly more refined image.  
• After many iterations, the final coherent image emerges.

(3) Notes  
This method is used in models like Stable Diffusion.
```

---

## 2. Example Prompt 2

**User Prompt**
```
Activate A-MODE.  
List three advantages of attention mechanisms in transformers.
```

**Expected Output**
```
(1) Scope Confirmation  
You asked for three advantages of attention mechanisms.

(2) Result  
• They allow the model to dynamically focus on important tokens.  
• They capture long-range dependencies more effectively than RNNs.  
• They support parallel computation, resulting in faster training.

(3) Notes  
None.
```

---

## 3. Writing Your Own A-MODE Prompts  
Follow these rules when writing A-MODE prompts:

### ✔ Required Format
```
Activate A-MODE.  
(Your question here)
```

### ✔ Guidelines
- Ask **only one task** per prompt  
- Keep questions **short and specific**  
- Expect **structured answers**  
- Avoid emotional or personal requests  
- Avoid multi-output creative tasks (use full Wooju Mode for those)

### ✔ A-MODE is best for:
- Technical explanations  
- Summaries  
- Definitions  
- Step-by-step reasoning  
- Research questions  
