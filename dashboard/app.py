import streamlit as st
import pandas as pd
import datetime
import sys, os

# ================= PATH =================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
VERSION = "2.1 PRO"
st.set_page_config(page_title="GDSN-X™ PRO", layout="centered")

# ================= HEADER =================
st.title("🧠 GDSN-X™ PRO Decision Intelligence")
st.caption("Consulting-Grade Risk Intelligence Platform")

# ================= SIDEBAR =================
st.sidebar.markdown("## 🧾 Client Details")
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

pro_mode = st.sidebar.checkbox("🔒 Enable Pro Mode")

# Pricing
st.sidebar.markdown("## 💰 Pricing")
st.sidebar.info("""
Free → Demo Analysis  
₹999 → Standard Report  
₹5000 → Premium Consulting  
""")

# ================= DATA =================
try:
    df_country = pd.read_csv("data/country_risk.csv")
except Exception:
    st.error("❌ country_risk.csv not found in /data folder")
    st.stop()

# ✅ CSV VALIDATION
required_cols = {"country", "economic", "political", "social"}
if not required_cols.issubset(df_country.columns):
    st.error("❌ Invalid CSV format. Required columns missing.")
    st.stop()

# Country Selection
country = st.selectbox("🌍 Select Country", df_country["country"])

filtered = df_country[df_country["country"] == country]

# ✅ EMPTY SAFETY
if filtered.empty:
    st.error("❌ Country data not found")
    st.stop()

row = filtered.iloc[0]

economic = int(row["economic"])
political = int(row["political"])
social = int(row["social"])

# ================= SCENARIO IMPACT =================
if scenario_type == "High Risk Zone":
    economic = min(economic + 10, 100)
    political = min(political + 10, 100)
elif scenario_type == "Emerging Market":
    economic = min(economic + 5, 100)

# ================= UI =================
st.subheader("📊 Risk Breakdown")

st.progress(economic / 100)
st.progress(political / 100)
st.progress(social / 100)

st.bar_chart({
    "Economic": economic,
    "Political": political,
    "Social": social
})

# ================= VALIDATION =================
if not client_name or not project_name:
    st.warning("⚠️ Client Name and Project Name are required")
    st.stop()

# ================= ANALYSIS =================
if st.button("🚀 Run Analysis", use_container_width=True):

    score, level = risk_score(economic, political, social)

    insight = risk_insight(economic, political, social)
    profile = risk_profile(economic, political, social)
    recommendation = risk_recommendation(level, economic, political, social)

    # ================= USE CASE INTELLIGENCE =================
    if use_case == "Investment Decision":
        recommendation += " Focus on ROI, capital efficiency, and downside protection."
    elif use_case == "Policy Analysis":
        recommendation += " Evaluate long-term governance and societal impact."
    elif use_case == "Business Expansion":
        recommendation += " Assess market entry barriers and competitive positioning."

    # ================= ADVANCED METRICS =================
    volatility = risk_volatility(economic, political, social)
    decision_conf = decision_confidence(score)
    confidence = data_confidence(economic, political, social)

    # ================= DISPLAY =================
    st.markdown("## 📈 Analysis Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Risk Score", score)
    col2.metric("Risk Level", level)
    col3.metric("Volatility Index", volatility)

    # Risk Tag
    if score > 70:
        st.error("🔴 CRITICAL RISK")
    elif score > 50:
        st.warning("🟠 ELEVATED RISK")
    else:
        st.success("🟢 STABLE")

    # Insights
    st.info(insight)
    st.info(smart_insight(score, level, economic, political, social))

    # Confidence
    st.info(f"📌 Data Confidence: {confidence}")
    st.info(f"📊 Decision Confidence: {decision_conf}")

    # Recommendation
    st.success(recommendation)

    # ================= REPORT =================
    report = f"""
===== GDSN-X™ PRO INTELLIGENCE REPORT =====

Client: {client_name}
Project: {project_name}
Use Case: {use_case}
Scenario Type: {scenario_type}

Date: {datetime.datetime.now().strftime("%Y-%m-%d")}

--- EXECUTIVE SUMMARY ---
Risk Score: {score}
Risk Level: {level}
Decision Confidence: {decision_conf}

--- CORE ANALYSIS ---
{insight}

--- ADVANCED ANALYSIS ---
{smart_insight(score, level, economic, political, social)}

--- RISK PROFILE ---
{profile}

--- VOLATILITY ---
Risk Volatility Index: {volatility}

--- DATA CONFIDENCE ---
{confidence}

--- STRATEGIC RECOMMENDATION ---
{recommendation}

--- FINAL VERDICT ---
This scenario represents a {level} environment with {decision_conf}.

===== END REPORT =====
"""

    # ✅ ENCODING FIX
    st.download_button(
        label="📥 Download Report",
        data=report.encode("utf-8"),
        file_name="GDSN-X_PRO_Report.txt",
        mime="text/plain"
    )

    # ================= PRO MODE =================
    if not pro_mode:
        st.warning("🔒 Pro Mode required to view full report preview")
    else:
        st.success("🔒 PRO MODE ACTIVE")
        st.code(report)

# ================= FOOTER =================
st.divider()
st.caption(f"© GDSN-X™ | Version {VERSION} — Consulting Intelligence System")
