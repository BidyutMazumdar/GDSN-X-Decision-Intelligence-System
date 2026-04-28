# ==========================================
# GDSN-X™ REPORT GENERATOR (v2.2 FINAL LOCK)
# Executive Intelligence + Audit + JSON + Deterministic Export
# ==========================================

import pandas as pd
import numpy as np
import logging
import json
import os
from datetime import datetime

# -------------------------
# LOGGER (ISOLATED)
# -------------------------
logger = logging.getLogger("GDSN-X-REPORT")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


# -------------------------
# INPUT VALIDATION (CRITICAL)
# -------------------------
def _validate_report_input(df):
    if df is None or len(df) == 0:
        raise ValueError("❌ Empty dataframe: cannot generate report")

    required = ["SCORE", "RANK", "TIER"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}")


# -------------------------
# SAFE JSON SERIALIZER
# -------------------------
def _safe_json(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    return str(obj)


# -------------------------
# GLOBAL SUMMARY
# -------------------------
def generate_global_summary(df):
    return {
        "total_countries": int(len(df)),
        "average_score": round(float(df["SCORE"].mean()), 4),
        "max_score": round(float(df["SCORE"].max()), 4),
        "min_score": round(float(df["SCORE"].min()), 4),
    }


# -------------------------
# EXECUTIVE SUMMARY
# -------------------------
def generate_executive_summary(df):
    df_sorted = df.sort_values("SCORE", ascending=False)

    top = df_sorted.iloc[0]
    bottom = df_sorted.iloc[-1]
    avg = df["SCORE"].mean()

    return f"""
GDSN-X Global Intelligence Report

Coverage: {len(df)} countries

Top Performer: {top.get('country', 'N/A')} (Score: {top['SCORE']})
Lowest Performer: {bottom.get('country', 'N/A')} (Score: {bottom['SCORE']})

Global Average Score: {avg:.2f}

Insight:
High-performing nations demonstrate balanced strength across governance,
AI capability, environmental sustainability, and legal robustness.
Lower-tier nations exhibit structural weaknesses in institutional capacity.
""".strip()


# -------------------------
# TOP / BOTTOM (SINGLE PASS)
# -------------------------
def get_top_bottom(df, n=10):
    df_sorted = df.sort_values("SCORE", ascending=False)

    top = df_sorted.head(n)
    bottom = df_sorted.tail(n).sort_values("SCORE", ascending=True)

    return (
        top.to_dict(orient="records"),
        bottom.to_dict(orient="records")
    )


# -------------------------
# TIER DISTRIBUTION
# -------------------------
def tier_distribution(df):
    dist = df["TIER"].value_counts().sort_index()
    percent = (dist / len(df) * 100).round(2)

    return {
        k: {
            "count": int(dist[k]),
            "percentage": float(percent[k])
        }
        for k in dist.index
    }


# -------------------------
# CONTRIBUTION ANALYSIS
# -------------------------
def contribution_analysis(df):
    cols = [c for c in df.columns if c.endswith("_CONTRIB")]
    means = df[cols].mean().sort_values(ascending=False)

    return {
        c.replace("_CONTRIB", ""): round(float(v), 4)
        for c, v in means.items()
    }


# -------------------------
# COUNTRY PROFILE
# -------------------------
def generate_country_profile(df, country):
    row = df[df["country"] == country]

    if row.empty:
        raise ValueError(f"❌ Country not found: {country}")

    row = row.iloc[0]

    contrib_cols = [c for c in df.columns if c.endswith("_CONTRIB")]
    contributions = {
        c.replace("_CONTRIB", ""): round(float(row[c]), 4)
        for c in contrib_cols
    }

    sorted_c = sorted(contributions.items(), key=lambda x: x[1], reverse=True)

    return {
        "country": country,
        "score": float(row["SCORE"]),
        "rank": int(row["RANK"]),
        "tier": row["TIER"],
        "strengths": [k for k, _ in sorted_c[:2]],
        "weaknesses": [k for k, _ in sorted_c[-2:]],
        "contributions": contributions
    }


# -------------------------
# COUNTRY COMPARISON
# -------------------------
def compare_countries(df, c1, c2):
    df_sorted = df.sort_values("SCORE", ascending=False)

    d1 = df_sorted[df_sorted["country"] == c1]
    d2 = df_sorted[df_sorted["country"] == c2]

    if d1.empty or d2.empty:
        raise ValueError("❌ One or both countries not found")

    d1 = d1.iloc[0]
    d2 = d2.iloc[0]

    return {
        "country_1": c1,
        "country_2": c2,
        "score_diff": round(float(d1["SCORE"] - d2["SCORE"]), 4),
        "rank_diff": int(d1["RANK"] - d2["RANK"])
    }


# -------------------------
# METADATA (AUDIT LINK)
# -------------------------
def add_report_metadata(df, report):
    report["metadata"] = {
        "version": df.attrs.get("config", {}).get("version"),
        "fingerprint": df.attrs.get("fingerprint"),
        "generated_at": datetime.utcnow().isoformat(),
        "records": int(len(df)),
        "columns": list(df.columns)
    }
    return report


# -------------------------
# FULL REPORT PIPELINE
# -------------------------
def generate_full_report(df):
    _validate_report_input(df)

    logger.info("📊 Generating report...")

    top, bottom = get_top_bottom(df)

    report = {
        "executive_summary": generate_executive_summary(df),
        "summary": generate_global_summary(df),
        "top_countries": top,
        "bottom_countries": bottom,
        "tier_distribution": tier_distribution(df),
        "contribution_analysis": contribution_analysis(df)
    }

    report = add_report_metadata(df, report)

    logger.info("✅ Report ready")

    return report


# -------------------------
# EXPORT (VERSIONED + SAFE)
# -------------------------
def export_report(df, report, path="reports/output"):
    os.makedirs(path, exist_ok=True)

    version = report.get("metadata", {}).get("version", "v1")

    logger.info("📁 Exporting...")

    df.to_csv(f"{path}/leaderboard_{version}.csv", index=False)

    with open(f"{path}/report_{version}.json", "w") as f:
        json.dump(report, f, indent=4, default=_safe_json)

    logger.info(f"✅ Export complete → {path}")
