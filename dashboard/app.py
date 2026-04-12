import streamlit as st
import sys
import os
import pandas as pd
import datetime

# =========================
# 🔹 PATH CONFIG
# =========================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from system.decision_engine import (
    risk_score,
    risk_insight,
    risk_recommendation,
    risk_profile
)

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

use_case = st.sidebar.selectbox(
    "Use Case",
    ["Business Expansion", "Investment Decision", "Policy Analysis"]
)

# =========================
# 🔹 SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# 🔹 COUNTRY DATA
# =========================
country_data = {
    "India": {"economic": 60, "political": 55, "social": 50},
    "USA": {"economic": 40, "political": 45, "social": 50},
    "China": {"economic": 70, "political": 75, "social": 65}
}

# =========================
# 🔹 SINGLE ANALYSIS
# =========================
if menu == "Single Analysis":

    st.markdown("## Risk Input Panel")

    mode = st.radio("Input Mode", ["Manual", "Country Data"])

    if mode == "Manual":
        economic = st.slider("Economic Risk", 0, 100, 50)
        political = st.slider("Political Risk", 0, 100, 50)
        social = st.slider("Social Risk", 0, 100, 50)
    else:
        country = st.selectbox("Select Country", list(country_data.keys()))
        economic = country_data[country]["economic"]
        political = country_data[country]["political"]
        social = country_data[country]["social"]

        st.info(f"Using preset data for {country}")

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
            profile = risk_profile(economic, political, social)
            recommendation = risk_recommendation(level, economic, political, social)

            st.markdown("---")
            st.markdown("## 📊 Analysis Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Risk Score", score)

            with col2:
                st.metric("Risk Level", level)

            # Risk Display
            if level == "High Risk":
                st.error("🔴 High Risk Detected")
            elif level == "Medium Risk":
                st.warning("🟠 Moderate Risk")
            else:
                st.success("🟢 Low Risk")

            # Insight + Profile
            st.info(insight)
            st.info(profile)

            # Recommendation
            if level == "High Risk":
                st.error(f"🚫 {recommendation}")
            elif level == "Medium Risk":
                st.warning(f"⚠️ {recommendation}")
            else:
                st.success(f"✅ {recommendation}")

            # Save history (WITH TIMESTAMP)
            st.session_state.history.append({
                "score": score,
                "level": level,
                "client": client_name,
                "project": project_name,
                "use_case": use_case,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })

            # EXECUTIVE REPORT
            report = f"""
GDSN-X™ Decision Intelligence Report
------------------------------------
Client: {client_name}
Project: {project_name}
Use Case: {use_case}

Risk Score: {score}
Risk Level: {level}

Insight:
{insight}

Risk Profile:
{profile}

Strategic Recommendation:
{recommendation}

Conclusion:
This decision falls under {level} category and requires structured evaluation.

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

    name_a = st.text_input("Scenario A Name")
    name_b = st.text_input("Scenario B Name")

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

        st.metric(name_a or "Scenario A", score_a)
        st.metric(name_b or "Scenario B", score_b)

        chart_data = pd.DataFrame({
            "Scenario": [name_a or "A", name_b or "B"],
            "Risk Score": [score_a, score_b]
        })

        st.bar_chart(chart_data.set_index("Scenario"))

        if score_a < score_b:
            st.success(f"✅ {name_a or 'Scenario A'} is safer")
        elif score_b < score_a:
            st.success(f"✅ {name_b or 'Scenario B'} is safer")
        else:
            st.info("Both scenarios are equal risk")

# =========================
# 🔹 HISTORY
# =========================
elif menu == "History":

    st.markdown("## 📊 Previous Scores")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)

        # Line chart
        st.line_chart(df["score"])

        # Table
        st.markdown("### Detailed History Table")
        st.dataframe(df)

        # CSV DOWNLOAD (FINAL FIXED)
        st.download_button(
            label="📥 Download History CSV",
            data=df.to_csv(index=False),
            file_name="GDSN-X_History.csv",
            mime="text/csv"
        )
    else:
        st.write("No history yet.")

# =========================
# 🔹 FOOTER
# =========================
st.markdown("---")
st.caption("© GDSN-X™ | Decision Intelligence Platform v2.0")
