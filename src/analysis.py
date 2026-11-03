import pandas as pd


COLUMN_CANDIDATES = {
    "date": ["Date received", "date_received"],
    "product": ["Product", "product"],
    "issue": ["Issue", "issue"],
    "company": ["Company", "company"],
    "state": ["State", "state"],
    "response": [
        "Company response to consumer",
        "company_response",
        "Company public response",
    ],
    "timely": ["Timely response?", "timely"],
    "narrative": [
        "Consumer complaint narrative",
        "complaint_what_happened",
    ],
}


def find_column(data, candidates):
    """Return the first matching column name, ignoring case and whitespace."""
    lookup = {str(column).strip().lower(): column for column in data.columns}

    for candidate in candidates:
        matched = lookup.get(candidate.lower())
        if matched is not None:
            return matched

    return None


def normalize_complaints(data):
    """Normalize important columns while preserving source fields."""
    result = data.copy()

    selected = {
        field: find_column(result, candidates)
        for field, candidates in COLUMN_CANDIDATES.items()
    }

    required = ["date", "product", "issue", "company"]
    missing = [field for field in required if selected[field] is None]

    if missing:
        raise ValueError(
            "Could not find required fields: "
            + ", ".join(missing)
            + ". Available columns: "
            + ", ".join(map(str, result.columns))
        )

    rename_map = {
        original: normalized
        for normalized, original in selected.items()
        if original is not None
    }

    result = result.rename(columns=rename_map)
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    result = result.dropna(subset=["date"])

    for column in ("product", "issue", "company", "state", "response", "timely"):
        if column in result.columns:
            result[column] = (
                result[column]
                .astype("string")
                .str.strip()
                .replace("", pd.NA)
            )

    result["month"] = result["date"].dt.to_period("M").astype(str)

    return result


def summarize_complaints(data):
    """Create monthly, product, issue, company, and response summaries."""
    summaries = {}

    summaries["monthly"] = (
        data.groupby("month")
        .size()
        .rename("complaint_count")
        .reset_index()
        .sort_values("month")
    )

    summaries["by_product"] = (
        data.groupby("product", dropna=False)
        .size()
        .rename("complaint_count")
        .reset_index()
        .sort_values("complaint_count", ascending=False)
    )

    summaries["by_issue"] = (
        data.groupby(["product", "issue"], dropna=False)
        .size()
        .rename("complaint_count")
        .reset_index()
        .sort_values("complaint_count", ascending=False)
    )

    summaries["by_company"] = (
        data.groupby("company", dropna=False)
        .size()
        .rename("complaint_count")
        .reset_index()
        .sort_values("complaint_count", ascending=False)
    )

    if "response" in data.columns:
        summaries["by_response"] = (
            data.groupby("response", dropna=False)
            .size()
            .rename("complaint_count")
            .reset_index()
            .sort_values("complaint_count", ascending=False)
        )

    if "timely" in data.columns:
        summaries["by_timely_response"] = (
            data.groupby("timely", dropna=False)
            .size()
            .rename("complaint_count")
            .reset_index()
            .sort_values("complaint_count", ascending=False)
        )

    if "state" in data.columns:
        summaries["by_state"] = (
            data.groupby("state", dropna=False)
            .size()
            .rename("complaint_count")
            .reset_index()
            .sort_values("complaint_count", ascending=False)
        )

    return summaries


def summarize_narratives(data, top_n=20):
    """
    Return frequent non-stopword terms from narratives.

    This is a lightweight exploratory summary, not sentiment analysis
    or a validated topic model.
    """
    if "narrative" not in data.columns:
        return pd.DataFrame(columns=["term", "count"])

    stopwords = {
        "about", "after", "again", "against", "also", "because", "been",
        "before", "being", "between", "both", "could", "customer", "did",
        "does", "doing", "down", "during", "each", "from", "further",
        "have", "having", "here", "into", "just", "more", "most", "other",
        "over", "same", "should", "some", "such", "than", "that", "their",
        "them", "then", "there", "these", "they", "this", "through", "under",
        "until", "very", "what", "when", "where", "which", "while", "with",
        "would", "your", "account", "company", "complaint", "consumer",
        "credit", "card",
    }

    text = (
        data["narrative"]
        .dropna()
        .astype(str)
        .str.lower()
        .str.findall(r"[a-z]{3,}")
    )

    counts = {}
    for words in text:
        for word in words:
            if word not in stopwords:
                counts[word] = counts.get(word, 0) + 1

    return (
        pd.DataFrame(
            [{"term": term, "count": count} for term, count in counts.items()]
        )
        .sort_values("count", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
