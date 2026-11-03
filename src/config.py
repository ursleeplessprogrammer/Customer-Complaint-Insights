from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "output"

# CFPB's current Consumer Complaint Database search API.
API_URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"

DEFAULT_DAYS = 365
DEFAULT_LIMIT = 5000
PAGE_SIZE = 1000
REQUEST_TIMEOUT = 30

# Used to generate optional narrative summaries.
NARRATIVE_COLUMN = "Consumer complaint narrative"
