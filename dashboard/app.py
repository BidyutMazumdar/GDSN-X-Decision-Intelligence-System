import streamlit as st import pandas as pd import sys import os import plotly.graph_objects as go

================= PATH CONFIG =================

CURRENT_DIR = os.path.dirname(os.path.abspath(file)) ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if ROOT_DIR not in sys.path: sys.path.insert(0, ROOT_DIR)

================= ENGINE IMPORT =================

try: from system.decision_engine import ( risk_score, risk_insight, risk_recommendation, risk_profile, smart_insight, data_confidence, risk_volatility, decision_confidence, explain_score ) except Exception as e: st.error(f"❌ Engine import failed: {e}") st.stop()

================= CONFIG =================

st.set_page_config(page_title="GDSN-X™ v2.3 ELITE", layout="wide")

================= HEADER =================

st.title("🧠 GDSN-X™ Decision Intelligence Platform") st.caption("v2.3 ELITE • Multi-Factor • Strategy-Driven • Explainable AI")

================= TRUST LAYER =================

st.caption("⚠️ Disclaimer: Deterministic model. Not financial advice.") st.caption("Version: GDSN-X™ v2.3 ELITE")

================= SIDEBAR =================

st.sidebar.header("🧾 Configuration")

client_name = st.sidebar.text_input("Client Name") project_name = st.sidebar.text_input("Project Name")

use_case = st.sidebar.selectbox( "Use Case", ["Business Expansion", "Investment Decision", "Policy Analysis"] )

strategy_mode = st.sidebar.selectbox( "Strategy Mode", ["Balanced", "Conservative", "Aggressive"] )

scenario_type = st.sidebar.selectbox( "Scenario", ["Base Case", "Best Case", "Worst Case"] )

================= DATA =================

DATA_PATH = os.path.join(ROOT_DIR, "data", "country_risk.csv")

if not os.path.exists(DATA_PATH): st.error("❌ Dataset not found") st.stop()

df = pd.read_csv(DATA_PATH)

country = st.selectbox("🌍 Select Country", sorted(df["country"].dropna().unique())) row = df[df["country"] == country].iloc[0]

def safe(x): try: return max(0, min(float(x), 100)) except: return 0.0

Base factors

economic = safe(row["economic"]) political = safe(row["political"]) social = safe(row["social"])

================= ADVANCED INPUT =================

st.subheader("⚙️ Advanced Risk Inputs") col1, col2, col3 = st.columns(3)

with col1: tech = st.slider("Technological Risk", 0, 100, 50) with col2: env = st.slider("Environmental Risk", 0, 100, 50) with col3: legal = st.slider("Legal Risk", 0, 100, 50)

================= SCENARIO =================

def apply_scenario(values): if scenario_type == "Best Case": return [max(v - 10, 0) for v in values] elif scenario_type == "Worst Case": return [min(v + 10, 100) for v in values] return values

values = apply_scenario([economic, political, social, tech, env, legal]) economic, political, social, tech, env, legal = values

================= VALIDATION =================

if not client_name or not project_name: st.warning("⚠️ Fill Client & Project details") st.stop()

================= RADAR CHART =================

st.subheader("📊 Risk Radar")

categories = ["Economic", "Political", "Social", "Tech", "Env", "Legal"] fig = go.Figure()

fig.add_trace(go.Scatterpolar( r=values + [values[0]], theta=categories + [categories[0]], fill='toself' ))

fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))

st.plotly_chart(fig, use_container_width=True)

================= WARNINGS =================

if any(v > 80 for v in values): st.warning("⚠️ Extreme Risk Detected")

================= RUN =================

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

st.divider()

# ================= METRICS =================
colA, colB, colC = st.columns(3)

colA.metric("Risk Score", score)
colB.metric("Risk Level", level)
colC.metric("Volatility", volatility)

# ================= INSIGHTS =================
st.subheader("📌 Key Insights")

st.info(insight)
st.info(explanation)
st.info(smart_insight(score, level, economic, political, social, tech, env, legal))

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

# ================= REPORT =================
report = f"""

===== GDSN-X™ v2.3 ELITE REPORT =====

Client: {client_name} Project: {project_name} Country: {country}

--- EXECUTIVE SUMMARY --- Risk Score: {score} Risk Level: {level} Decision Confidence: {decision_conf}%

--- KEY DRIVERS --- {insight} {explanation}

--- ANALYSIS --- {smart_insight(score, level, economic, political, social, tech, env, legal)}

--- PROFILE --- {profile}

--- VOLATILITY --- {volatility}

--- FINAL RECOMMENDATION --- {recommendation}

--- DATA CONFIDENCE --- {confidence['label']} ({confidence['score']}%)

--- DISCLAIMER --- Model-based estimation. Not financial or policy advice.

===== END ===== """

st.download_button(
    "📥 Download Report",
    report.encode("utf-8"),
    file_name="GDSN_X_v2_3_ELITE_Report.txt"
)

st.code(report)
