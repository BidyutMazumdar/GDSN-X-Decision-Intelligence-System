import streamlit as st
from system.decision_engine import risk_score, risk_insight, risk_recommendation

# Page config
st.set_page_config(page_title="GDSN-X™ Dashboard", layout="centered")

# Header
st.title("GDSN-X™ Decision Intelligence")
st.caption("Advanced Risk Evaluation Dashboard")

st.markdown("### Risk Input Panel")

# Inputs
economic = st.slider("Economic Risk", 0, 100, 50)
political = st.slider("Political Risk", 0, 100, 50)
social = st.slider("Social Risk", 0, 100, 50)

# Action
if st.button("Run Analysis"):
    score, level = risk_score(economic, political, social)
    insight = risk_insight(economic, political, social)
    recommendation = risk_recommendation(level)

    st.markdown("---")
    st.subheader("Analysis Result")

    # KPI Metric
    st.metric(label="Risk Score", value=score)

    # Risk Level
    st.write(f"**Risk Level:** {level}")

    # Color Zone Indicator
    if level == "High Risk":
        st.markdown("### 🔴 High Risk Zone")
    elif level == "Medium Risk":
        st.markdown("### 🟠 Medium Risk Zone")
    else:
        st.markdown("### 🟢 Low Risk Zone")

    # Insight Box
    st.info(insight)

    # Recommendation Box
    if level == "High Risk":
        st.error(f"🚫 {recommendation}")
    elif level == "Medium Risk":
        st.warning(f"⚠️ {recommendation}")
    else:
        st.success(f"✅ {recommendation}")

    # -----------------------------
    # 📄 REPORT GENERATION (NEW)
    # -----------------------------
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

    # 📥 Download Button
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="GDSN-X_Report.txt",
        mime="text/plain"
    )

    # 🧾 Report Preview
    st.markdown("### Full Report Preview")
    st.code(report)
