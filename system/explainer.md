# GDSN-X™ Risk Model — Technical Explainer

## Overview

The GDSN-X™ Decision Intelligence System applies a structured, multi-factor risk evaluation model to quantify uncertainty in strategic decision-making.

The model integrates three core dimensions:

- Economic Risk (E)
- Political Risk (P)
- Social Risk (S)

These dimensions represent the primary drivers of systemic instability across business, policy, and global environments.

---

## Mathematical Formalization

Let:

E, P, S ∈ [0,100]

Define the risk function:

R(E, P, S) = w₁E + w₂P + w₃S

Where:

w₁ = 0.40  
w₂ = 0.35  
w₃ = 0.25  

Subject to:

w₁ + w₂ + w₃ = 1

Thus:

R(E, P, S) ∈ [0,100]

---

## Risk Model Formula

Risk Score = (0.40 × E) + (0.35 × P) + (0.25 × S)

Where:

- E = Economic Risk (0–100)
- P = Political Risk (0–100)
- S = Social Risk (0–100)

The output is normalized to a 0–100 scale.

---

## Rationale for Weighting (40 / 35 / 25)

The weighting scheme reflects real-world impact hierarchy observed across economic, political, and societal systems.

### Economic Risk — 40%

Economic factors are the most immediate drivers of decision outcomes.

They directly impact:

- Capital flow  
- Market viability  
- Cost structures  
- Investment sustainability  

Due to their direct and measurable effect, economic risk carries the highest weight.

---

### Political Risk — 35%

Political conditions define the operational and regulatory environment.

They influence:

- Policy stability  
- Legal frameworks  
- Government intervention  
- Geopolitical tensions  

Political instability can significantly disrupt economic systems, justifying a near-equal weight.

---

### Social Risk — 25%

Social dynamics reflect population-level stability.

They include:

- Public sentiment  
- Social unrest  
- Labor conditions  
- Demographic pressures  

Social risk typically evolves more gradually but remains critical for long-term stability.

---

## Risk Level Classification

The aggregated score is categorized as:

- 0 – 39 → Low Risk  
- 40 – 69 → Medium Risk  
- 70 – 100 → High Risk  

This enables fast and actionable interpretation.

---

## Interpretation of Scores

The risk score should be interpreted as follows:

- 0–39 → Operationally stable environment with low disruption probability  
- 40–69 → Moderate uncertainty requiring controlled execution  
- 70–100 → High instability with significant risk exposure  

The score reflects **relative risk intensity**, not absolute certainty.

---

## Multi-Factor Insight Layer

The system identifies:

- Primary Risk Driver (highest factor)  
- Secondary Risk Driver (second-highest factor)  

### Purpose

This layer provides diagnostic clarity:

- Identifies the dominant risk source  
- Guides targeted intervention  
- Improves decision transparency  

---

## Risk Profile Tagging

The system assigns qualitative profiles:

- High Political Exposure  
- Economic Dominant Risk  
- Social Instability Risk  
- Balanced Risk Profile  

### Function

Transforms numerical output into **strategic, human-readable interpretation**.

---

## Recommendation Engine Logic

Recommendations are generated based on:

- Overall risk level  
- Dominant risk factor  

### Examples:

- High Political Risk → Delay or limit exposure  
- High Economic Risk → Reduce investment scale  
- Medium Balanced Risk → Controlled execution  

---

## Model Characteristics

### Deterministic
Same inputs always produce the same output

### Interpretable
Fully transparent and explainable logic

### Scalable
Extendable with additional variables, dynamic weighting, or AI integration

---

## Model Limitations & Scope

- The model evaluates structured risk, not future certainty  
- Outputs are dependent on input quality and contextual accuracy  
- External shocks and non-linear systemic events are not explicitly modeled  
- The system is intended for decision support, not autonomous decision-making  

Users should apply domain-specific judgment when interpreting results.

---

## Positioning

GDSN-X™ is a:

- Decision Support System (DSS)  
- Not a predictive system  
- Not a replacement for human judgment  

Its value lies in:

- Structured clarity  
- Quantified uncertainty  
- Actionable insight  

---

## Conclusion

The GDSN-X™ model bridges qualitative judgment and quantitative analysis.

It enables decision-makers to transition from intuition-based decisions to **data-informed strategic intelligence**.
