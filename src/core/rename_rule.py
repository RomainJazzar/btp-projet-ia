# path: src/core/rename_rule.py
import re
import unicodedata
from datetime import datetime
from typing import Dict, Optional


def _strip_accents(s: str) -> str:
    """Remove accents safely."""
    if not isinstance(s, str):
        return ""
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def _slug_type(s: Optional[str]) -> str:
    """TYPE part: keep only A-Z0-9, collapse everything else, UPPERCASE."""
    if not s:
        return ""
    s = _strip_accents(s).upper()
    s = re.sub(r"[^A-Z0-9]+", "", s)
    return s


def _slug_entity_no_spaces(s: Optional[str]) -> str:
    """
    ENTITY part: remove accents and ALL non-alphanumerics (including spaces),
    then uppercase. e.g. 'Entreprise X' -> 'ENTREPRISEX'
    """
    if not s:
        return ""
    s = _strip_accents(s)
    s = re.sub(r"[^A-Za-z0-9]+", "", s)  # remove all non-alphanumerics
    return s.upper()


def _norm_number(s: Optional[str]) -> str:
    """
    Number part: remove accents, replace non-alphanumerics by underscores,
    trim, uppercase. (F2024-001 -> F2024_001)
    """
    if not s:
        return ""
    s = _strip_accents(s).upper()
    s = re.sub(r"[^A-Z0-9]+", "_", s)
    s = s.strip("_")
    return s


def _norm_date(date_str: Optional[str]) -> str:
    """
    Accept several FR-ish formats and return YYYY-MM-DD.
    If already YYYY-MM-DD, keep it. Raise ValueError if not parseable.
    """
    if not date_str:
        raise ValueError("date manquante")

    ds = date_str.strip()
    # Already ISO-like?
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", ds):
        return ds

    # Try common formats
    formats = [
        "%d/%m/%Y", "%d-%m-%Y",
        "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d",
        "%d.%m.%Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(ds, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Fallback: try to pick 8 consecutive digits as yyyymmdd
    m = re.search(r"(\d{4})[^\d]?(\d{2})[^\d]?(\d{2})", ds)
    if m:
        y, mo, d = m.groups()
        return f"{y}-{mo}-{d}"

    raise ValueError(f"Date non reconnue: {date_str!r}")


def format_name(meta: Dict, basename: str) -> str:
    """
    Build: YYYY-MM-DD_TYPE_ENTITE_NUM.pdf
    Required: date, doc_type
    entity and number optional.
    """
    if not isinstance(meta, dict):
        raise ValueError("meta doit être un dict.")

    # Required
    date_iso = _norm_date(meta.get("date"))
    doc_type = meta.get("doc_type") or meta.get("type") or ""
    doc_type_slug = _slug_type(doc_type)
    if not doc_type_slug:
        raise ValueError("doc_type manquant")

    # Optional
    entity = meta.get("entity") or ""
    entity_slug = _slug_entity_no_spaces(entity)
    number = meta.get("doc_number") or meta.get("number") or ""
    number_norm = _norm_number(number)

    parts = [date_iso, doc_type_slug]
    if entity_slug:
        parts.append(entity_slug)
    if number_norm:
        parts.append(number_norm)

    filename = "_".join(parts) + ".pdf"
    return filename
