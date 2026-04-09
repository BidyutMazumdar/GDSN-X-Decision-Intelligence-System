import streamlit as st
import sys
import os
import pandas as pd

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from system.decision_engine import risk_score, risk_insight, risk_recommendation

# Page config
st.set_page_config(page_title="GDSN-X™ Dashboard", layout="centered")

# Header
st.title("GDSN-X™ Decision Intelligence")
st.caption("Advanced Risk Evaluation Dashboard")

# =========================
# 🔹 SINGLE ANALYSIS
# =========================
st.markdown("### Risk Input Panel")

economic = st.slider("Economic Risk", 0, 100, 50)
political = st.slider("Political Risk", 0, 100, 50)
social = st.slider("Social Risk", 0, 100, 50)

# History init
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Run Analysis"):
    score, level = risk_score(economic, political, social)
    insight = risk_insight(economic, political, social)
    recommendation = risk_recommendation(level)

    st.markdown("---")
    st.subheader("Analysis Result")

    st.metric("Risk Score", score)
    st.write(f"**Risk Level:** {level}")

    if level == "High Risk":
        st.markdown("### 🔴 High Risk Zone")
    elif level == "Medium Risk":
        st.markdown("### 🟠 Medium Risk Zone")
    else:
        st.markdown("### 🟢 Low Risk Zone")

    st.info(insight)

    if level == "High Risk":
        st.error(f"🚫 {recommendation}")
    elif level == "Medium Risk":
        st.warning(f"⚠️ {recommendation}")
    else:
        st.success(f"✅ {recommendation}")

    # Save structured history
    st.session_state.history.append({
        "score": score,
        "level": level
    })

    # Report
    report = f"""
GDSN-X™ Decision Intelligence Report

------------------------------------
Risk Score: {score}
Risk Level: {level}
{insight}

Recommendation:
{recommendation}
------------------------------------
"""

    st.download_button("📥 Download Report", report, "GDSN-X_Report.txt")

    st.markdown("### Full Report Preview")
    st.code(report)

# =========================
# 🔹 SCENARIO COMPARISON
# =========================
st.markdown("---")
st.markdown("## 🔄 Scenario Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Scenario A")
    econ_a = st.slider("Economic A", 0, 100, 50, key="econ_a")
    pol_a = st.slider("Political A", 0, 100, 50, key="pol_a")
    soc_a = st.slider("Social A", 0, 100, 50, key="soc_a")

with col2:
    st.markdown("### Scenario B")
    econ_b = st.slider("Economic B", 0, 100, 50, key="econ_b")
    pol_b = st.slider("Political B", 0, 100, 50, key="pol_b")
    soc_b = st.slider("Social B", 0, 100, 50, key="soc_b")

if st.button("Compare Scenarios"):
    score_a, level_a = risk_score(econ_a, pol_a, soc_a)
    score_b, level_b = risk_score(econ_b, pol_b, soc_b)

    st.subheader("Comparison Result")

    st.metric("Scenario A Score", score_a)
    st.metric("Scenario B Score", score_b)

    # Professional chart
    chart_data = pd.DataFrame({
        "Scenario": ["A", "B"],
        "Risk Score": [score_a, score_b]
    })

    st.bar_chart(chart_data.set_index("Scenario"))

    # Decision
    if score_a < score_b:
        st.success("✅ Scenario A is safer")
    elif score_b < score_a:
        st.success("✅ Scenario B is safer")
    else:
        st.info("Both scenarios are equal risk")

# =========================
# 🔹 HISTORY
# =========================
st.markdown("---")
st.markdown("## 📊 Previous Scores")

if st.session_state.history:
    scores = [item["score"] for item in st.session_state.history]
    st.line_chart(scores)
    st.write(st.session_state.history)
else:
    st.write("No history yet.")

# =========================
# 🔹 BRANDING
# =========================
st.markdown("---")
st.caption("GDSN-X™ | Decision Intelligence System")
