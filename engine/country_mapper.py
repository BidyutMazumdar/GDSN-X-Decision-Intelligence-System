# ==========================================
# GDSN-X™ COUNTRY MAPPER (ABSOLUTE FINAL LOCK ∞)
# ISO3 Standardization Engine (Audit + Production + Scalable)
# ==========================================

import pandas as pd
import re
import unicodedata
import logging

# -------------------------
# LOGGING (AUDIT-GRADE)
# -------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# -------------------------
# OPTIONAL: pycountry
# -------------------------
try:
    import pycountry
    PYCOUNTRY_AVAILABLE = True
except ImportError:
    PYCOUNTRY_AVAILABLE = False

# -------------------------
# OPTIONAL: fuzzy matching
# -------------------------
try:
    from rapidfuzz import process
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False

# -------------------------
# NORMALIZATION CORE
# -------------------------
def _normalize_text(text):
    if pd.isna(text):
        return None

    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().strip()

    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


# -------------------------
# OVERRIDE MAP
# -------------------------
RAW_OVERRIDE = {
    "United States": "USA",
    "United States of America": "USA",
    "US": "USA",
    "USA": "USA",

    "United Kingdom": "GBR",
    "UK": "GBR",
    "Britain": "GBR",

    "South Korea": "KOR",
    "Korea, Rep.": "KOR",

    "North Korea": "PRK",
    "Korea, Dem. Rep.": "PRK",

    "Iran": "IRN",
    "Iran, Islamic Rep.": "IRN",

    "Russia": "RUS",
    "Russian Federation": "RUS",

    "Egypt": "EGY",
    "Egypt, Arab Rep.": "EGY",

    "Turkey": "TUR",
    "Türkiye": "TUR",

    "Vietnam": "VNM",
    "Viet Nam": "VNM",

    "Czechia": "CZE",
    "Czech Republic": "CZE",

    "Slovakia": "SVK",
    "Slovak Republic": "SVK",

    "Côte d'Ivoire": "CIV",
    "Ivory Coast": "CIV",
}

COUNTRY_OVERRIDE = {
    _normalize_text(k): v for k, v in RAW_OVERRIDE.items()
}

# -------------------------
# PYCOUNTRY CACHE (PERFORMANCE FIX)
# -------------------------
if PYCOUNTRY_AVAILABLE:
    _PYCOUNTRY_CACHE = {}
    for c in pycountry.countries:
        _PYCOUNTRY_CACHE[_normalize_text(c.name)] = c.alpha_3
        if hasattr(c, "official_name"):
            _PYCOUNTRY_CACHE[_normalize_text(c.official_name)] = c.alpha_3
else:
    _PYCOUNTRY_CACHE = {}

# -------------------------
# FAST ISO LOOKUP
# -------------------------
def _auto_iso3(name):
    if not PYCOUNTRY_AVAILABLE:
        return None

    # fast cache lookup
    if name in _PYCOUNTRY_CACHE:
        return _PYCOUNTRY_CACHE[name]

    # fallback
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None


# -------------------------
# SAFE FUZZY MATCH (CONTROLLED)
# -------------------------
def _fuzzy_iso3(name):
    if not (PYCOUNTRY_AVAILABLE and FUZZY_AVAILABLE):
        return None

    countries = list(pycountry.countries)
    names = [_normalize_text(c.name) for c in countries]

    match, score, idx = process.extractOne(name, names)

    if score >= 93:
        return countries[idx].alpha_3

    return None


# -------------------------
# MAIN FUNCTION
# -------------------------
def to_iso3(country_name, allow_fuzzy=False):
    name = _normalize_text(country_name)

    if not name:
        return None

    # 1️⃣ override (highest priority)
    if name in COUNTRY_OVERRIDE:
        return COUNTRY_OVERRIDE[name]

    # 2️⃣ pycountry (cached)
    iso = _auto_iso3(name)
    if iso:
        return iso

    # 3️⃣ fuzzy (optional, controlled)
    if allow_fuzzy:
        iso = _fuzzy_iso3(name)
        if iso:
            return iso

    return None


# -------------------------
# VALIDATION (CRITICAL)
# -------------------------
def _validate_iso3(series):
    if not PYCOUNTRY_AVAILABLE:
        return series

    valid_codes = {c.alpha_3 for c in pycountry.countries}
    invalid = set(series.dropna()) - valid_codes

    if invalid:
        raise ValueError(f"❌ Invalid ISO3 detected: {list(invalid)[:5]}")

    return series


# -------------------------
# BULK APPLY (PIPELINE SAFE)
# -------------------------
def apply_iso3(df, country_col="country", allow_fuzzy=False):
    df = df.copy()

    df[country_col] = df[country_col].apply(_normalize_text)
    df["iso3"] = df[country_col].apply(lambda x: to_iso3(x, allow_fuzzy))

    # validation
    df["iso3"] = _validate_iso3(df["iso3"])

    # audit logging
    total = len(df)
    mapped = df["iso3"].notna().sum()
    coverage = (mapped / total) * 100

    logging.info(f"🌍 ISO3 Coverage: {mapped}/{total} ({coverage:.2f}%)")

    missing = df[df["iso3"].isna()][country_col].unique()

    if len(missing) > 0:
        logging.warning(f"Missing ISO3 mapping: {len(missing)} countries")
        logging.warning(list(missing[:10]))

    return df


# -------------------------
# STRICT MODE (AUDIT LOCK)
# -------------------------
def apply_iso3_strict(df, country_col="country"):
    df = apply_iso3(df, country_col, allow_fuzzy=False)

    if df["iso3"].isna().any():
        missing = df[df["iso3"].isna()][country_col].unique()
        raise ValueError(f"❌ ISO3 mapping incomplete: {len(missing)} missing")

    return df
