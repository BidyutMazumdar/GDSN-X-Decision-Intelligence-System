# ==========================================
# GDSN-X™ SCORING ENGINE — v1.0.4 FINAL LOCK 🔒
# ==========================================

import pandas as pd
import numpy as np
import logging
import hashlib
import json
from copy import deepcopy

# -------------------------
# GLOBAL DETERMINISM LOCK
# -------------------------
np.random.seed(42)

# -------------------------
# LOGGER (ISOLATED)
# -------------------------
logger = logging.getLogger("GDSN-X")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# -------------------------
# CONFIG
# -------------------------
WEIGHTS = {
    "GDP": 0.20,
    "POL": 0.20,
    "AI": 0.20,
    "EPI": 0.20,
    "LAW": 0.20,
}

DIRECTION = {k: 1 for k in WEIGHTS}

EXPECTED_OUTPUT_COLUMNS = {"SCORE", "RANK", "TIER"}
OUTPUT_ORDER = ["country", "SCORE", "RANK", "TIER", "VERSION"]
VERSION = "GDSN-X_SCORING_v1.0.4_FINAL_LOCK"

# -------------------------
# VALIDATION
# -------------------------
def _validate_inputs(df):
    missing = [c for c in WEIGHTS if c not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}")

    if not np.isclose(sum(WEIGHTS.values()), 1.0):
        raise ValueError("❌ WEIGHTS must sum to 1")

# -------------------------
# NORMALIZATION
# -------------------------
def _normalize(series):
    s = pd.to_numeric(series, errors="coerce")

    s = s.clip(s.quantile(0.01), s.quantile(0.99))

    if s.min() == s.max() or pd.isna(s.min()):
        return pd.Series(0, index=s.index)

    return (s - s.min()) / (s.max() - s.min()) * 100

# -------------------------
# FEATURE ENGINEERING
# -------------------------
def _prepare(df):
    df = df.copy()

    for c in WEIGHTS:
        norm = _normalize(df[c])
        if DIRECTION[c] == -1:
            norm = 100 - norm
        df[f"{c}_N"] = norm

    return df

# -------------------------
# MISSING CONTROL
# -------------------------
def _clean(df):
    before = len(df)
    df = df.dropna(subset=[f"{c}_N" for c in WEIGHTS])
    if len(df) != before:
        logger.warning(f"⚠️ Dropped {before - len(df)} rows")
    return df

# -------------------------
# SCORE
# -------------------------
def compute_score(df):
    _validate_inputs(df)
    df = _prepare(df)
    df = _clean(df)

    df["SCORE"] = sum(df[f"{c}_N"] * w for c, w in WEIGHTS.items())

    for c, w in WEIGHTS.items():
        df[f"{c}_CONTRIB"] = (df[f"{c}_N"] * w).round(6)

    df["SCORE"] = df["SCORE"].round(6)

    return df

# -------------------------
# RANKING
# -------------------------
def apply_ranking(df):
    df = df.sort_values(by=["SCORE", "country"] if "country" in df else ["SCORE"],
                        ascending=[False, True] if "country" in df else [False])

    df["RANK"] = df["SCORE"].rank(method="first", ascending=False).astype(int)
    return df

# -------------------------
# TIER (HYBRID)
# -------------------------
def assign_tiers(df):
    q = df["SCORE"].quantile

    def tier(x):
        if x >= max(q(0.90), 85): return "A+"
        if x >= max(q(0.75), 70): return "A"
        if x >= max(q(0.50), 55): return "B"
        if x >= max(q(0.25), 40): return "C"
        return "D"

    df["TIER"] = df["SCORE"].apply(tier)
    return df

# -------------------------
# METADATA
# -------------------------
def add_metadata(df):
    df.attrs["config"] = {
        "weights": deepcopy(WEIGHTS),
        "direction": deepcopy(DIRECTION),
        "normalization": "winsorized_minmax_0_100",
        "tier_method": "hybrid",
        "precision": "6_decimal",
        "version": VERSION,
    }
    return df

# -------------------------
# FINGERPRINT (CORE ONLY)
# -------------------------
def add_fingerprint(df):
    core = ["country", "SCORE", "RANK", "TIER"] if "country" in df else ["SCORE", "RANK", "TIER"]

    df_core = df[core].sort_values(by=core, kind="mergesort")
    data_str = df_core.to_csv(index=False)

    config = json.dumps(df.attrs["config"], sort_keys=True)

    df.attrs["fingerprint"] = hashlib.sha256((config + data_str).encode()).hexdigest()
    return df

# -------------------------
# FINALIZE
# -------------------------
def finalize(df):
    df["VERSION"] = VERSION

    ordered = [c for c in OUTPUT_ORDER if c in df]
    remaining = [c for c in df.columns if c not in ordered]

    return df[ordered + remaining]

# -------------------------
# PIPELINE
# -------------------------
def run_scoring(df):
    logger.info("⚙️ Running GDSN-X™ Engine")

    df = compute_score(df)
    df = apply_ranking(df)
    df = assign_tiers(df)
    df = add_metadata(df)
    df = add_fingerprint(df)
    df = finalize(df)

    if not EXPECTED_OUTPUT_COLUMNS.issubset(df.columns):
        raise ValueError("❌ Output schema violation")

    logger.info(f"✅ Completed: {len(df)} entities")

    return df

# -------------------------
# EXPORT
# -------------------------
def export_csv(df, path="dataset/processed/gdsn_index.csv"):
    df.to_csv(path, index=False)
    logger.info(f"📁 Exported → {path}")
