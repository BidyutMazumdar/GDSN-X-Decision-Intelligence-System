# ==========================================
# GDSN-X™ DATA PIPELINE (ABSOLUTE FINAL LOCK)
# Production + Audit + Research Grade
# ==========================================

import pandas as pd
from pathlib import Path
import logging

# -------------------------
# CONFIG
# -------------------------
BASE_PATH = Path("dataset/raw")

FILES = {
    "gdp": BASE_PATH / "gdp_growth.csv",
    "political": BASE_PATH / "political_stability.csv",
    "ai": BASE_PATH / "ai_readiness.xlsx",
    "epi": BASE_PATH / "epi.csv",
    "law": BASE_PATH / "rule_of_law.csv",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# -------------------------
# HELPERS
# -------------------------
def _check_file(path):
    if not path.exists():
        raise FileNotFoundError(f"❌ Missing file: {path}")

def _clean_country(series):
    return series.astype(str).str.strip()

def _to_numeric(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def normalize(series):
    s = pd.to_numeric(series, errors="coerce")
    min_val = s.min()
    max_val = s.max()

    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series([0]*len(s), index=s.index)

    return (s - min_val) / (max_val - min_val) * 100

# -------------------------
# COUNTRY STANDARDIZATION
# -------------------------
COUNTRY_MAP = {
    "United States": "United States of America",
    "Korea, Rep.": "South Korea",
    "Russian Federation": "Russia",
    "Iran, Islamic Rep.": "Iran",
    "Egypt, Arab Rep.": "Egypt",
}

def _standardize(df):
    df["country"] = df["country"].replace(COUNTRY_MAP)
    df["country"] = df["country"].str.strip()
    return df

# -------------------------
# SAFE YEAR PICKER
# -------------------------
def _get_latest_year_column(df):
    year_cols = [c for c in df.columns if str(c).isdigit()]
    year_cols = sorted(year_cols)

    valid_cols = []
    for col in year_cols:
        if pd.to_numeric(df[col], errors="coerce").notna().sum() > 0:
            valid_cols.append(col)

    if not valid_cols:
        raise ValueError("❌ No valid numeric year columns found")

    return valid_cols[-1]

# -------------------------
# SAFE COLUMN FINDER
# -------------------------
def _find_column(df, keyword):
    cols = [c for c in df.columns if keyword in c.lower()]
    if not cols:
        raise ValueError(f"❌ Column not found: {keyword}")
    return cols[0]

# -------------------------
# DEDUPE
# -------------------------
def _dedupe(df):
    return df.drop_duplicates(subset=["country"], keep="last")

# -------------------------
# LOADERS
# -------------------------
def load_gdp():
    _check_file(FILES["gdp"])
    df = pd.read_csv(FILES["gdp"], low_memory=False)

    df = df.rename(columns={"Country Name": "country"})
    col = _get_latest_year_column(df)

    df = df[["country", col]]
    df.columns = ["country", "GDP_raw"]

    df = _standardize(df)
    return _dedupe(df).dropna()


def load_political():
    _check_file(FILES["political"])
    df = pd.read_csv(FILES["political"], low_memory=False)

    df = df.rename(columns={"Country Name": "country"})
    col = _get_latest_year_column(df)

    df = df[["country", col]]
    df.columns = ["country", "POL_raw"]

    df = _standardize(df)
    return _dedupe(df).dropna()


def load_ai():
    _check_file(FILES["ai"])
    df = pd.read_excel(FILES["ai"])

    country_col = _find_column(df, "country")
    score_col = _find_column(df, "score")

    df = df.rename(columns={country_col: "country", score_col: "AI_raw"})
    df = df[["country", "AI_raw"]]

    df = _standardize(df)
    return _dedupe(df).dropna()


def load_epi():
    _check_file(FILES["epi"])
    df = pd.read_csv(FILES["epi"], low_memory=False)

    country_col = _find_column(df, "country")
    epi_col = _find_column(df, "epi")

    df = df.rename(columns={country_col: "country", epi_col: "EPI_raw"})
    df = df[["country", "EPI_raw"]]

    df = _standardize(df)
    return _dedupe(df).dropna()


def load_rule_of_law():
    _check_file(FILES["law"])
    df = pd.read_csv(FILES["law"], low_memory=False)

    df = df[["country", "L_raw"]]

    df = _standardize(df)
    return _dedupe(df).dropna()

# -------------------------
# MERGE ENGINE
# -------------------------
def merge_all(normalize_all=True):
    logging.info("🔄 Merging datasets...")

    gdp = load_gdp()
    pol = load_political()
    ai = load_ai()
    epi = load_epi()
    law = load_rule_of_law()

    logging.info(f"GDP: {len(gdp)}, POL: {len(pol)}, AI: {len(ai)}, EPI: {len(epi)}, LAW: {len(law)}")

    df = gdp.merge(pol, on="country", how="inner")
    df = df.merge(ai, on="country", how="inner")
    df = df.merge(epi, on="country", how="inner")
    df = df.merge(law, on="country", how="inner")

    if df.empty:
        raise ValueError("❌ Merge failed — country mismatch")

    # -------------------------
    # TYPE SAFETY
    # -------------------------
    df = _to_numeric(df, ["GDP_raw", "POL_raw", "AI_raw", "EPI_raw", "L_raw"])
    df = df.dropna()

    # -------------------------
    # NORMALIZATION
    # -------------------------
    if normalize_all:
        df["GDP"] = normalize(df["GDP_raw"])
        df["POL"] = normalize(df["POL_raw"])
        df["AI"] = normalize(df["AI_raw"])
        df["EPI"] = normalize(df["EPI_raw"])
        df["LAW"] = normalize(df["L_raw"])

    # -------------------------
    # COVERAGE (AUDIT)
    # -------------------------
    coverage = len(df) / len(gdp) * 100
    logging.info(f"🌍 Coverage: {coverage:.2f}%")

    # -------------------------
    # SORT (READY FOR SCORING)
    # -------------------------
    df = df.reset_index(drop=True)

    logging.info(f"✅ Final dataset: {len(df)} countries")

    return df
