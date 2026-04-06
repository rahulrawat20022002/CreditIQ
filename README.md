# CreditIQ — Fairness-by-Design Credit Scoring (Privacy, Ethics & Law Project)

**Course:** Privacy, Ethics & Law
**Dataset:** German Credit Data (UCI ML Repository, Prof. Hans Hofmann, 1994)  
**Project Type:** Responsible AI / Fair Credit Scoring / EU AI Act Compliance  
**Status:** Final  

---

# 🧠 Project Overview
CreditIQ is a **fairness-aware credit scoring system** designed to meet **EU AI Act (High-Risk)** and **AGG 80% Disparate Impact** requirements.  
The system applies **Fairness-by-Design**, **Intersectional Post‑Processing**, and **Explainable AI (SHAP)** to mitigate bias while maintaining competitive accuracy.

Unlike traditional credit scoring models, **CreditIQ is advisory only** — a **human finance manager makes the final decision**.

---

# 🎯 Project Goals

- Build regulatory‑compliant credit scoring AI
- Detect bias in historical lending data
- Apply fairness mitigation (Pre + Post processing)
- Optimize fairness vs accuracy trade‑off
- Add intersectional fairness (Age × Gender)
- Provide explainability using SHAP
- Deploy real‑time Streamlit decision interface
- Produce audit‑ready documentation

---

# 🧾 Dataset

**German Credit Dataset (UCI)**

- 1,000 applicants
- 20 original features
- Binary classification: `credit_risk`
- Good = 1 (Approved)
- Bad = 0 (Rejected)

### Protected Attributes

| Attribute | Privileged | Unprivileged |
|-----------|------------|--------------|
| Age | ≥ 30 | < 30 |
| Gender | Male | Female |

---

# ⚖️ Regulatory Target

**Disparate Impact ≥ 0.80**  
(EU AI Act Annex III + AGG Four-Fifths Rule)

---

# 🏗️ System Architecture

```
User Form (18 features)
        ↓
build_feature_vector()
        ↓
Random Forest Model (predict_proba)
        ↓
Intersectional Threshold Matrix
        ↓
fair_credit_decision()
        ↓
LLM Explanation (Groq LLaMA 3.1)
        ↓
Finance Manager (Human in Loop)
```

---

# 🔍 Phase-by-Phase Development

# Phase 1 — Baseline Risk Audit
Historical bias detected against younger applicants.

**Disparate Impact (raw):** 0.7948 (Not passed)

Risk Identified:

- Age discrimination
- Class imbalance
- Representation bias

---

# Phase 2 — Pre‑Processing (DIR)
Applied AIF360 Disparate Impact Remover.

Results (Logistic Regression):

| Model | Accuracy | DI |
|------|---------|----|
| Biased | 71% | 0.80 |
| Repaired | 72% | 0.84 |

DIR successful for linear models.

---

# Phase 3 — Random Forest “Yes‑Man” Discovery
Random Forest approved almost everyone due to imbalance.

False Positive Rate ≈ 88%

Accuracy inflated but misleading.

---

# Phase 4 — Balanced Random Forest
Introduced class weights.

| Model | Accuracy | DI | Youth FNR |
|------|---------|----|-----------|
| Biased | 74% | 0.6269 | 38.9% |
| Repaired | 72% | 0.5750 | 44.4% |

DIR worsened fairness for balanced RF.

---

# Phase 5 — Model Comparison

| Model | Accuracy | DI | FNR Gap |
|------|---------|----|--------|
| Random Forest | 73.0% | 0.569 | +23.6% |
| Logistic Regression | 72.5% | 0.492 | +28.3% |
| Decision Tree | 66.5% | 0.589 | +26.7% |

**Random Forest selected** as best trade‑off.

---

# Phase 5 — Threshold Optimization
Age‑based thresholds:

Older → 0.50  
Younger → 0.45

Result:

DI = 0.7321 still failing

---

# Phase 6 — SHAP Explainability
SHAP revealed proxy discrimination:

- housing ownership
- loan duration
- employment history

Gender bias detected.

---

# Phase 7 — Intersectional Post‑Processing
4‑way threshold matrix introduced:

| Group | Threshold |
|------|-----------|
| Older Men | 0.50 |
| Older Women | 0.44 |
| Younger Men | 0.42 |
| Younger Women | 0.42 |

---

# Final Model Performance

| Metric | Value |
|-------|------|
| Accuracy | 75.00% |
| Good Recall | 83% |
| Good Precision | 79% |
| Bad Precision | 60% |
| FPR | 43.55% |
| FNR | 16.67% |
| Disparate Impact | 0.8805 (Passed)|

---

# ⚖️ Fairness Improvement

| Group | Before | After |
|------|-------|------|
| Younger Women | 29.03% | 17.65% |
| Older Women | 22.40% | 17.78% |
| Older Men | 16.50% | 14.67% |

---

# 🤖 Explainability (XAI)

Method: SHAP TreeExplainer

Used for:

- Bias detection
- Feature importance
- Proxy discrimination discovery
- Decision transparency

---

# 🧪 Testing

- Unit tests with MockModel
- 100% branch coverage
- All demographic paths tested

---

# 🏛️ Regulatory Compliance

## EU AI Act Classification

HIGH‑RISK AI SYSTEM (Annex III)

| Article | Requirement | Status |
|--------|-------------|-------|
| Art. 9 | Risk Management | Passed |
| Art.10 | Data Governance | Passed |
| Art.11 | Documentation | Passed |
| Art.13 | Transparency | Passed |
| Art.14 | Human Oversight | Passed |

DPIA required before production.

---

# 🖥️ Streamlit App

Real‑time decision dashboard.

Features:

- 18 input fields
- fairness‑adjusted decision
- probability score
- LLM explanation
- risk flags
- human‑in‑loop approval

Run locally:

```
streamlit run app.py
```

---

# 📁 Repository Structure

```
├── models
        ├── Ai_and_Ethics.ipynb
        ├── credit_data_scaler.pkl
        ├── fair_credit_rf_model.pkl
        ├── model_columns.pkl
├── app.py
├── README.md
├── requirements.txt
```

---

# 🔐 Responsible AI Safeguards

- Human‑in‑the‑loop decision making
- Intersectional fairness mitigation
- Bias monitoring
- Threshold transparency
- SHAP explainability
- Regulatory documentation

---

# ⚠️ Limitations

- Dataset from 1994 (outdated)
- Only 1,000 samples
- Binary gender only
- German market only
- High FPR trade‑off

---

# 🎯 Intended Use
Decision support tool for **bank finance managers**.

Not allowed:

- Autonomous decisions
- Non‑EU deployment
- Production without DPIA

---

# 📊 Model Card

**Model:** CreditIQ Fair Credit Scorer v1.0  
**Type:** RandomForestClassifier  
**Fairness Method:** Intersectional Thresholding  
**DI:** 0.8805  
**FNR:** 16.67%  
**FPR:** 43.55%  
**XAI:** SHAP  
**Risk Level:** EU AI Act High‑Risk  

---

# 🚀 Key Contributions

✔ Fairness‑by‑Design credit scoring  
✔ Intersectional bias mitigation  
✔ Post‑processing threshold matrix  
✔ SHAP explainability integration  
✔ EU AI Act compliant architecture  
✔ Human‑in‑loop decision framework  
✔ Real‑time Streamlit deployment  

---

# 👨‍💻 Author

Course Project — SRH Heidelberg  
Responsible AI / Fair Credit Scoring  

---

# 📜 License

Educational / Research Use Only

---

# ⭐ If you find this useful

Give the repo a star and feel free to fork for responsible AI projects.

