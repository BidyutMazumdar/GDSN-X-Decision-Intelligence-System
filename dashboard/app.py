# =========================
# 🧠 GDSN-X™ DASHBOARD (ENTERPRISE v3 - ABSOLUTE FINAL LOCK)
# =========================

import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import os

# =========================
# ⚙️ CONFIG
# =========================
st.set_page_config(page_title="GDSN-X™ SaaS", layout="wide")

# 🔥 PRODUCTION SAFE (ENV SUPPORT)
API_BASE = os.getenv("API_BASE", "http://localhost:8000/api/v3")
TIMEOUT = 15

# =========================
# 🔐 MAIN LOGIN SCREEN
# =========================
if "token" not in st.session_state:

    st.title("🔐 GDSN-X Login")
    st.markdown("Enter your credentials to access the platform")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            res = requests.post(
                f"{API_BASE.replace('/api/v3','')}/login",
                json={"username": username, "password": password},
                timeout=TIMEOUT
            )

            if res.status_code == 200:
                st.session_state["token"] = res.json()["access_token"]
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

        except:
            st.error("❌ Server not reachable")

    st.stop()

# =========================
# 🔓 LOGOUT (SAFE)
# =========================
if "token" in st.session_state:
    if st.sidebar.button("Logout"):
        del st.session_state["token"]
        st.session_state.pop("result", None)  # clear old result
        st.rerun()

# =========================
# 🧾 HEADER
# =========================
st.title("🧠 GDSN-X™ Decision Intelligence Platform")
st.caption("Enterprise SaaS • API v3 • Secure • Scalable")

# =========================
# 🧾 CONFIGURATION
# =========================
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

# =========================
# 📊 LOAD DATA
# =========================
DATA_PATH = os.path.join("data", "country_risk.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

country = st.selectbox("🌍 Select Country", sorted(df["country"].dropna().unique()))
row = df[df["country"] == country].iloc[0]

# =========================
# 🎯 SAFE INPUT
# =========================
def safe(x):
    try:
        return max(0, min(float(x), 100))
    except:
        return 0.0

economic = safe(row["economic"])
political = safe(row["political"])
social = safe(row["social"])

# =========================
# ⚙️ ADVANCED INPUT
# =========================
st.subheader("⚙️ Advanced Risk Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    tech = st.slider("Technological Risk", 0, 100, 50)

with col2:
    env = st.slider("Environmental Risk", 0, 100, 50)

with col3:
    legal = st.slider("Legal Risk", 0, 100, 50)

# =========================
# 🔁 SCENARIO
# =========================
def apply_scenario(values):
    if scenario_type == "Best Case":
        return [max(v - 10, 0) for v in values]
    elif scenario_type == "Worst Case":
        return [min(v + 10, 100) for v in values]
    return values

economic, political, social, tech, env, legal = apply_scenario(
    [economic, political, social, tech, env, legal]
)

# =========================
# ⚠️ VALIDATION
# =========================
if not client_name or not project_name:
    st.warning("⚠️ Fill Client & Project details")
    st.stop()

# =========================
# 📊 RADAR CHART
# =========================
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

# =========================
# 🚀 RUN ANALYSIS
# =========================
if st.button("🚀 Run Analysis", use_container_width=True):

    headers = {
        "Authorization": f"Bearer {st.session_state['token']}"
    }

    payload = {
        "economic": economic,
        "political": political,
        "social": social,
        "tech": tech,
        "env": env,
        "legal": legal,
        "use_case": use_case,
        "strategy_mode": strategy_mode,
        "country": country
    }

    try:
        res = requests.post(
            f"{API_BASE}/risk",
            json=payload,
            headers=headers,
            timeout=TIMEOUT
        )

        if res.status_code != 200:
            st.error(f"❌ API Error: {res.text}")
            st.stop()

        st.session_state["result"] = res.json()

    except requests.exceptions.Timeout:
        st.error("❌ Request timeout")
        st.stop()

    except requests.exceptions.RequestException:
        st.error("❌ API connection failed")
        st.stop()

# =========================
# 📊 PERSISTENT RESULT
# =========================
if "result" in st.session_state:

    data = st.session_state["result"]

    st.divider()

    colA, colB, colC = st.columns(3)

    colA.metric("Risk Score", data["core"]["score"])
    colB.metric("Risk Level", data["core"]["level"])
    colC.metric("Decision Confidence", data["core"]["decision_conf"])

    st.subheader("📌 Insights")

    st.info(data["explainability"]["explanation"])
    st.info(data["explainability"]["analysis"])
    st.success(data["recommendation"])

# =========================
# 📊 HISTORY
# =========================
st.sidebar.markdown("### 📊 User History")

if st.sidebar.button("Load History"):

    headers = {
        "Authorization": f"Bearer {st.session_state['token']}"
    }

    try:
        res = requests.get(
            f"{API_BASE}/history",
            headers=headers,
            timeout=TIMEOUT
        )

        if res.status_code == 200:
            history = res.json()

            for item in history:
                st.sidebar.write(
                    f"{item['country']} → {item['score']} ({item['level']})"
                )
        else:
            st.sidebar.warning("No history found")

    except:
        st.sidebar.error("Failed to load history")
