import streamlit as st
import pandas as pd
import sys
import os

# ================= FINAL IMPORT FIX (CLOUD SAFE) =================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from system.decision_engine import (
    risk_score,
    risk_insight,
    risk_recommendation,
    risk_profile,
    smart_insight,
    data_confidence,
    risk_volatility,
    decision_confidence
)

# ================= CONFIG =================
st.set_page_config(page_title="GDSN-X™ PRO", layout="centered")

st.title("🧠 GDSN-X™ PRO Decision Intelligence")
st.caption("Production-Grade Risk Engine v2 PRO")

# ================= SIDEBAR =================
st.sidebar.header("Client Setup")

client_name = st.sidebar.text_input("Client Name")
project_name = st.sidebar.text_input("Project Name")

use_case = st.sidebar.selectbox(
    "Use Case",
    ["Business Expansion", "Investment Decision", "Policy Analysis"]
)

scenario_type = st.sidebar.selectbox(
    "Scenario Type",
    ["Stable Market", "Emerging Market", "High Risk Zone"]
)

pro_mode = st.sidebar.checkbox("Enable Pro Mode")

# ================= DATA =================
df = pd.read_csv("data/country_risk.csv")

country = st.selectbox(
    "Select Country",
    sorted(df["country"].dropna().unique())
)

row = df[df["country"] == country].iloc[0]

economic = float(row["economic"])
political = float(row["political"])
social = float(row["social"])

# ================= SCENARIO ADJUSTMENT =================
if scenario_type == "High Risk Zone":
    economic = min(economic + 10, 100)
    political = min(political + 10, 100)
elif scenario_type == "Emerging Market":
    economic = min(economic + 5, 100)

# ================= VALIDATION =================
if not client_name or not project_name:
    st.warning("Please fill client details")
    st.stop()

# ================= RUN =================
if st.button("Run Analysis"):

    score, level = risk_score(economic, political, social)

    st.metric("Risk Score", score)
    st.metric("Risk Level", level)

    st.progress(economic / 100)
    st.progress(political / 100)
    st.progress(social / 100)

    st.info(risk_insight(economic, political, social))
    st.info(smart_insight(score, level, economic, political, social))

    st.info(f"Profile: {risk_profile(economic, political, social)}")
    st.info(f"Volatility: {risk_volatility(economic, political, social)}")
    st.info(f"Data Confidence: {data_confidence(economic, political, social)}")
    st.info(f"Decision Confidence: {decision_confidence(score)}")

    st.success(
        risk_recommendation(level, economic, political, social)
    )

    report = f"""
Client: {client_name}
Project: {project_name}
Score: {score}
Level: {level}
"""

    st.download_button(
        "Download Report",
        report,
        file_name="gdsn_x_report.txt"
    )

    if pro_mode:
        st.code(report)
