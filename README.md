# Classification Rule Mining

## 🎯 Overview

This project aims to extract, validate, and operationalize business rules from classification feedback data in order to improve model performance and training data quality.

Instead of manually reviewing individual corrections, this system identifies recurring patterns and transforms them into **validated, high-impact business rules**.

The approach combines:
- Semantic analysis (LLMs)
- Business knowledge (explanatory notes)
- Model behavior (confidence / IC)
- Data reality (training set)

---

## 🧠 Key Idea

We do not blindly trust:
- the model ❌
- the data ❌
- or the rules ❌

We reconcile all three:
Business Truth (notes)
vs
Data Reality (training set)
vs
Model Behavior (confidence)

→ Decision: ADD / UPDATE / REVIEW

1. Install uv
```Bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone & Sync
```Bash
git clone git@github.com:InseeFrLab/codif-ape-preprocess.git
cd classification_rule_mining
uv sync
```

3. Run
```Bash
uv run python -m src.main
```

4. Or run example demo
```Bash
uv run demo
```
