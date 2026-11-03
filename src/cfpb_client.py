from datetime import date, timedelta

import pandas as pd
import requests

from src.config import (
    API_URL,
    DEFAULT_DAYS,
    DEFAULT_LIMIT,
    PAGE_SIZE,
    REQUEST_TIMEOUT,
)


def _extract_records(payload):
    """Extract complaint records from common API response structures."""
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ("hits", "results", "data"):
            value = payload.get(key)

            if isinstance(value, list):
                return value

            if isinstance(value, dict):
                nested = value.get("hits")
                if isinstance(nested, list):
                    return nested

    return []


def _flatten_record(record):
    """Flatten common API hit wrappers into a plain record dictionary."""
    if not isinstance(record, dict):
        return {}

    # Search APIs may wrap the actual fields in "_source".
    if isinstance(record.get("_source"), dict):
        return record["_source"]

    return record


def fetch_complaints(
    days=DEFAULT_DAYS,
    limit=DEFAULT_LIMIT,
    product=None,
):
    """
    Retrieve recent complaints through the CFPB API.

    The API's query format can evolve. If the response format changes,
    review the CFPB API documentation and update _extract_records().
    """
    if days < 1:
        raise ValueError("days must be at least 1.")

    if limit < 1:
        raise ValueError("limit must be at least 1.")

    today = date.today()
    start_date = today - timedelta(days=days)

    session = requests.Session()
    records = []
    offset = 0

    while len(records) < limit:
        page_limit = min(PAGE_SIZE, limit - len(records))

        params = {
            "date_received_min": start_date.isoformat(),
            "date_received_max": today.isoformat(),
            "size": page_limit,
            "from": offset,
            "format": "json",
        }

        if product:
            params["product"] = product

        response = session.get(
            API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        payload = response.json()
        page = _extract_records(payload)

        if not page:
            break

        records.extend(_flatten_record(item) for item in page)
        offset += len(page)

        if len(page) < page_limit:
            break

    if not records:
        raise RuntimeError(
            "The API returned no complaint records. Check the filters, "
            "network connection, API documentation, and response format."
        )

    return pd.DataFrame(records[:limit])
