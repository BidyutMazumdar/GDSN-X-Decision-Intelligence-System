import streamlit as st
import pandas as pd
import sys
import os
import plotly.graph_objects as go
import plotly.express as px

# ================= PATH CONFIG =================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ================= ENGINE IMPORT =================
try:
    from system.decision_engine import (
        risk_score,
        risk_insight,
        risk_recommendation,
        risk_profile,
        smart_insight,
        data_confidence,
        risk_volatility,
        decision_confidence,
        explain_score
    )
    from system.report_engine import generate_pdf
    from system.simulation import run_simulation  # ✅ NEW
except Exception as e:
    st.error(f"❌ System import failed: {e}")
    st.stop()

# ================= CONFIG =================
st.set_page_config(
    page_title="GDSN-X™ v2.4 ELITE",
    layout="wide"
)

# ================= HEADER =================
st.title("🧠 GDSN-X™ Decision Intelligence Platform")
st.caption("v2.4 ELITE • Probabilistic • Explainable • Consulting-Grade Engine")
st.caption("⚠️ Deterministic + Monte Carlo Model. Not financial advice.")

# ================= SIDEBAR =================
st.sidebar.header("🧾 Configuration")

client_name = st.sidebar.text_input("Client Name")
project_name = st.sidebar.text_input("Project Name")

use_case = st.sidebar.selectbox(
    "Use Case",
    ["Business Expansion", "Investment Decision", "Policy Analysis"]
)

strategy_mode = st.sidebar.selectbox(
    "Strategy Mode",
    ["Balanced", "Conservative", "Aggressive"]
)

scenario_type = st.sidebar.selectbox(
    "Scenario",
    ["Base Case", "Best Case", "Worst Case"]
)

st.caption(f"Use Case: {use_case} | Strategy: {strategy_mode}")

# ================= DATA =================
DATA_PATH = os.path.join(ROOT_DIR, "data", "country_risk.csv")

if not os.path.exists(DATA_PATH):
    st.error("❌ Dataset not found")
    st.stop()

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)

country = st.selectbox("🌍 Select Country", sorted(df["country"].dropna().unique()))
row = df[df["country"] == country].iloc[0]

# ================= SAFE INPUT =================
def safe(x):
    try:
        return max(0, min(float(x), 100))
    except:
        return 0.0

economic = safe(row["economic"])
political = safe(row["political"])
social = safe(row["social"])

# ================= ADVANCED INPUT =================
st.subheader("⚙️ Advanced Risk Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    tech = st.slider("Technological Risk", 0, 100, 50)

with col2:
    env = st.slider("Environmental Risk", 0, 100, 50)

with col3:
    legal = st.slider("Legal Risk", 0, 100, 50)

# ================= SCENARIO =================
def apply_scenario(values):
    if scenario_type == "Best Case":
        return [max(v - 10, 0) for v in values]
    elif scenario_type == "Worst Case":
        return [min(v + 10, 100) for v in values]
    return values

economic, political, social, tech, env, legal = apply_scenario(
    [economic, political, social, tech, env, legal]
)

# ================= VALIDATION =================
if not client_name or not project_name:
    st.warning("⚠️ Fill Client & Project details")
    st.stop()

# ================= RADAR =================
st.subheader("📊 Risk Radar")

categories = ["Economic", "Political", "Social", "Tech", "Env", "Legal"]
values = [economic, political, social, tech, env, legal]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=values + [values[0]],
    theta=categories + [categories[0]],
    fill='toself'
))
fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])))

st.plotly_chart(fig, use_container_width=True)

# ================= ALERT =================
if any(v > 80 for v in values):
    st.warning("⚠️ Extreme Risk Detected (Non-linear penalty applied)")

# ================= FORECAST =================
forecast = round(sum(values) / len(values), 2)
st.info(f"📈 Estimated Trend Risk: {forecast}")

# ================= RUN ANALYSIS =================
if st.button("🚀 Run Full Analysis", use_container_width=True):

    score, level, meta = risk_score(
        economic, political, social,
        tech, env, legal,
        use_case,
        strategy_mode
    )

    insight = risk_insight(economic, political, social, tech, env, legal)
    explanation = explain_score(meta)

    profile = risk_profile(economic, political, social, tech, env, legal)
    recommendation = risk_recommendation(level, strategy_mode)

    volatility = risk_volatility(economic, political, social, tech, env, legal)
    confidence = data_confidence(economic, political, social, tech, env, legal)
    decision_conf = decision_confidence(score)

    # ✅ CLEAN ANALYSIS
    analysis = smart_insight(
        score, level,
        economic, political, social, tech, env, legal
    )

    # Save for PDF
    st.session_state["result"] = {
        "score": score,
        "level": level,
        "explanation": explanation,
        "analysis": analysis,
        "profile": profile,
        "recommendation": recommendation,
        "confidence": confidence,
        "decision_conf": decision_conf,
        "volatility": volatility
    }

    st.divider()

    # ================= METRICS =================
    colA, colB, colC = st.columns(3)
    colA.metric("Risk Score", score)
    colB.metric("Risk Level", level)
    colC.metric("Volatility", volatility)

    # ================= INSIGHTS =================
    st.subheader("📌 Key Insights")
    st.info(explanation)
    st.info(insight)
    st.info(analysis)

    # ================= CONFIDENCE =================
    st.info(f"📊 Data Confidence: {confidence['label']} ({confidence['score']}%)")
    st.info(f"🎯 Decision Confidence: {decision_conf}%")
    st.info(f"🧭 Profile: {profile}")

    # ================= TAG =================
    if score > 70:
        st.error("🔴 CRITICAL RISK")
    elif score > 50:
        st.warning("🟠 ELEVATED RISK")
    else:
        st.success("🟢 STABLE")

    st.success(recommendation)

    # ================= TXT REPORT =================
    report = f"""
===== GDSN-X™ ELITE REPORT =====

Client: {client_name}
Project: {project_name}
Country: {country}

--- EXECUTIVE SUMMARY ---
Risk Score: {score}
Risk Level: {level}
Decision Confidence: {decision_conf}%

--- KEY DRIVERS ---
{explanation}

--- ANALYSIS ---
{analysis}

--- PROFILE ---
{profile}

--- VOLATILITY ---
{volatility}

--- CONFIDENCE ---
{confidence['label']} ({confidence['score']}%)

--- FINAL RECOMMENDATION ---
{recommendation}

===== END =====
"""

    st.download_button(
        "📥 Download TXT Report",
        report.encode("utf-8"),
        file_name="GDSN_X_ELITE_Report.txt"
    )

    # ================= MONTE CARLO =================
    st.subheader("🎲 Monte Carlo Simulation")

    sim = run_simulation(
        economic, political, social,
        tech, env, legal,
        use_case,
        strategy_mode,
        iterations=1000
    )

    colX, colY, colZ = st.columns(3)
    colX.metric("Mean Risk", sim["mean"])
    colY.metric("Min Risk", sim["min"])
    colZ.metric("Max Risk", sim["max"])

    st.info(f"📊 Volatility (Std Dev): {sim['std_dev']}")
    st.warning(f"⚠️ High Risk Probability: {sim['high_risk_probability']}%")

    fig_sim = px.histogram(sim["distribution"], nbins=30)
    st.plotly_chart(fig_sim, use_container_width=True)

# ================= PDF REPORT =================
if "result" in st.session_state:

    if st.button("📄 Generate PDF Report"):

        r = st.session_state["result"]
        pdf_file = "GDSN_X_Report.pdf"

        generate_pdf(
            pdf_file,
            client_name,
            project_name,
            country,
            r["score"],
            r["level"],
            r["decision_conf"],
            r["explanation"],
            r["analysis"],
            r["profile"],
            r["volatility"],
            r["confidence"]["label"],
            r["confidence"]["score"],
            r["recommendation"]
        )

        with open(pdf_file, "rb") as f:
            st.download_button(
                "📥 Download PDF",
                f,
                file_name=pdf_file
            )
