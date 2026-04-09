import streamlit as st
import sys
import os
import pandas as pd

# =========================
# 🔹 PATH CONFIG
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from system.decision_engine import risk_score, risk_insight, risk_recommendation

# =========================
# 🔹 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="GDSN-X™ Platform",
    layout="centered"
)

# =========================
# 🔹 HEADER
# =========================
st.markdown("""
# 🧠 GDSN-X™ Decision Intelligence Platform
### Quantifying Risk. Powering Decisions.
---
""")

# =========================
# 🔹 SIDEBAR
# =========================
menu = st.sidebar.radio(
    "Navigation",
    ["Single Analysis", "Scenario Comparison", "History"]
)

st.sidebar.markdown("## Client Details")
client_name = st.sidebar.text_input("Client Name")
project_name = st.sidebar.text_input("Project Name")

# =========================
# 🔹 SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# 🔹 SINGLE ANALYSIS
# =========================
if menu == "Single Analysis":

    st.markdown("## Risk Input Panel")

    economic = st.slider("Economic Risk", 0, 100, 50)
    political = st.slider("Political Risk", 0, 100, 50)
    social = st.slider("Social Risk", 0, 100, 50)

    st.markdown("### Risk Breakdown")
    st.bar_chart({
        "Economic": economic,
        "Political": political,
        "Social": social
    })

    if st.button("Run Analysis", use_container_width=True):

        if not client_name:
            st.warning("Please enter Client Name for report")
        else:
            score, level = risk_score(economic, political, social)
            insight = risk_insight(economic, political, social)
            recommendation = risk_recommendation(level)

            st.markdown("---")
            st.markdown("## 📊 Analysis Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Risk Score", score)

            with col2:
                st.metric("Risk Level", level)

            if level == "High Risk":
                st.error("🔴 High Risk Detected")
            elif level == "Medium Risk":
                st.warning("🟠 Moderate Risk")
            else:
                st.success("🟢 Low Risk")

            st.info(insight)

            if level == "High Risk":
                st.error(f"🚫 {recommendation}")
            elif level == "Medium Risk":
                st.warning(f"⚠️ {recommendation}")
            else:
                st.success(f"✅ {recommendation}")

            st.session_state.history.append({
                "score": score,
                "level": level,
                "client": client_name,
                "project": project_name
            })

            report = f"""
GDSN-X™ Decision Intelligence Report
------------------------------------
Client: {client_name}
Project: {project_name}

Risk Score: {score}
Risk Level: {level}

{insight}

Recommendation:
{recommendation}
------------------------------------
"""

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name="GDSN-X_Report.txt",
                mime="text/plain"
            )

            st.markdown("### Report Preview")
            st.code(report)

# =========================
# 🔹 SCENARIO COMPARISON
# =========================
elif menu == "Scenario Comparison":

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

    if st.button("Compare Scenarios", use_container_width=True):

        score_a, _ = risk_score(econ_a, pol_a, soc_a)
        score_b, _ = risk_score(econ_b, pol_b, soc_b)

        st.subheader("Comparison Result")

        st.metric("Scenario A Score", score_a)
        st.metric("Scenario B Score", score_b)

        chart_data = pd.DataFrame({
            "Scenario": ["A", "B"],
            "Risk Score": [score_a, score_b]
        })

        st.bar_chart(chart_data.set_index("Scenario"))

        if score_a < score_b:
            st.success("✅ Scenario A is safer")
        elif score_b < score_a:
            st.success("✅ Scenario B is safer")
        else:
            st.info("Both scenarios are equal risk")

# =========================
# 🔹 HISTORY
# =========================
elif menu == "History":

    st.markdown("## 📊 Previous Scores")

    if st.session_state.history:
        scores = [item["score"] for item in st.session_state.history]
        st.line_chart(scores)
        st.dataframe(pd.DataFrame(st.session_state.history))
    else:
        st.write("No history yet.")

# =========================
# 🔹 FOOTER
# =========================
st.markdown("---")
st.caption("© GDSN-X™ | Decision Intelligence Platform v1.0")
