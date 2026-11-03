# 🏦 Customer Complaint Insights

<p align="center">
      <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
      <img src="https://img.shields.io/badge/IDE-Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white" />
</p>

> **Explore consumer complaint data to understand reported issues, products, companies, and changes over time.**

## Overview

Customer Complaint Insights is a Python project that retrieves public complaint records from the **Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database**, analyzes selected fields, and creates summary reports and charts.

The project explores complaint counts by month, product, issue, company, response, and state. It also counts common words in available complaint narratives. This is exploratory data analysis—not a measure of overall company quality or a representative survey of all consumers.

## 🗺️ Contents

- [Project Goals](#-project-goals)
- [Data Source and Important Context](#-data-source-and-important-context)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Setup](#-setup)
- [Run the Project](#-run-the-project)
- [Command-Line Options](#️-command-line-options)
- [How It Works](#-how-it-works)
- [Generated Files](#-generated-files)
- [Sample Output](#-sample-output)
- [Understanding the Results](#-understanding-the-results)
- [Limitations](#️-limitations)
- [References](#-references)

## 🎯 Project Goals

This project aims to:

- Retrieve complaint records through the CFPB API.
- Clean and standardize selected fields.
- Summarize records by month, product, issue, company, response, and state.
- Explore frequently occurring terms in available complaint narratives.
- Save analysis results as CSV files and charts.
- Demonstrate a modular Python project structure.

## 📊 Data Source and Important Context

The project uses the **CFPB Consumer Complaint Database**, which provides public complaint data and an API for searching records. ([CFPB complaint API](https://cfpb.github.io/api/ccdb/))

Keep these limitations in mind:

- The database is **not a representative sample** of all consumers or all experiences.
- Not every complaint is published; publication depends on CFPB processes and applicable criteria.
- Narratives are available only for some complaints where consumers provide them and consent to publication.
- A complaint is a consumer report. Its presence alone does not establish that a company violated a law or acted improperly.
- Counts may be affected by publication practices, product definitions, company names, and submission patterns.

The CFPB cautions that the database is not a statistical sample of consumer experiences. Use it to describe the records returned by your query—not to make unsupported claims about all consumers or a company’s overall performance. ([CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/))

## 🧰 Technology Stack

- **Python** — project language
- **Pandas** — data loading, cleaning, and analysis
- **Requests** — API calls
- **Matplotlib** — charts

## 📁 Project Structure

```text
customer-complaint-insights/
├── output/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── cfpb_client.py
│   ├── analysis.py
│   ├── visualization.py
│   └── main.py
├── requirements.txt
└── README.md
```

- `src/config.py` stores API settings, defaults, and output paths.
- `src/cfpb_client.py` requests records from the CFPB API.
- `src/analysis.py` normalizes fields and creates summary tables.
- `src/visualization.py` creates charts.
- `src/main.py` connects the modules and runs the project.
- `src/__init__.py` marks `src` as a Python package.
- `output/` contains downloaded data, reports, and charts.

## ⚙️ Setup

Use Python 3 and create a virtual environment if desired:

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS or Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should contain:

```text
pandas
requests
matplotlib
```

## ▶️ Run the Project

From the project root, run:

```bash
python -m src.main
```

By default, the script requests up to 5,000 complaints from the most recent 365 days, then saves the data, summaries, and charts in `output/`.

The CFPB API and its parameters can change. If a request fails or the response structure differs, check the current API documentation and update `src/cfpb_client.py`. ([CFPB API documentation](https://cfpb.github.io/ccdb5-api/documentation/))

## 🏷️ Command-Line Options

### Filter by product

```bash
python -m src.main --product "Credit card"
```

The product value must match a product accepted by the CFPB API. Available names may change, so check the API or database documentation if a filter returns no data.

### Choose a date range

```bash
python -m src.main --days 180
```

### Limit the number of records

```bash
python -m src.main --limit 10000
```

### Choose an output directory

```bash
python -m src.main --output-dir results
```

### Combine options

```bash
python -m src.main \
  --product "Credit card" \
  --days 365 \
  --limit 5000 \
  --output-dir output
```

On Windows Command Prompt, enter the command on one line or use the appropriate line-continuation character.

## 🔄 How It Works

### 1. Fetch complaint records

`src/cfpb_client.py` sends requests to the CFPB complaint search API. It requests records in pages until it reaches the requested limit or no more records are returned.

The original downloaded records are saved before normalization so they can be inspected later.

### 2. Normalize selected fields

`src/analysis.py` finds commonly used fields even if capitalization or naming differs. It parses complaint dates and creates a month field for aggregation.

Date, product, issue, and company fields are required. If the API response does not include recognizable versions of them, the script stops and reports the available columns.

### 3. Create summary tables

The project counts records by:

- Month
- Product
- Product and issue
- Company
- Company response, when available
- Timely-response value, when available
- State, when available

These are raw counts, not normalized rates. For example, a company’s complaint count is not adjusted for its number of customers, transactions, or market share.

### 4. Explore complaint narratives

When narratives are available, the script converts the text to lowercase, extracts words, removes a small list of common terms, and counts the remaining words.

This is a basic exploratory summary. It is **not** sentiment analysis, a validated topic model, or a substitute for reading the narratives. Word counts can miss context, negation, sarcasm, and meaning.

### 5. Save charts and outputs

`src/visualization.py` creates a line chart of monthly complaint counts and a bar chart of the most frequently recorded products.

The charts summarize the downloaded records; they do not explain why a count changed.

## 📤 Generated Files

The default output folder contains:

```text
output/
├── complaints_raw.csv
├── complaints_clean.csv
├── monthly.csv
├── by_product.csv
├── by_issue.csv
├── by_company.csv
├── by_response.csv
├── by_timely_response.csv
├── by_state.csv
├── narrative_terms.csv
├── monthly_complaints.png
└── top_products.png
```

Some summary files are created only if the corresponding field exists in the API response.

- **`complaints_raw.csv`** — downloaded records before normalization.
- **`complaints_clean.csv`** — normalized records with parsed dates and a month field.
- **`monthly.csv`** — record counts by month.
- **`by_product.csv`** — counts by product.
- **`by_issue.csv`** — counts by product and issue.
- **`by_company.csv`** — counts by company.
- **`by_response.csv`** — counts by company-response category, when available.
- **`by_timely_response.csv`** — counts by timely-response value, when available.
- **`by_state.csv`** — counts by state, when available.
- **`narrative_terms.csv`** — frequent terms in available narratives.
- **`monthly_complaints.png`** — chart of monthly counts.
- **`top_products.png`** — chart of the most frequently recorded products.

## 🖥️ Sample Output

Console output will vary depending on the query date, filters, API response, and available records. It may look like this:

```text
Fetching complaints from the CFPB API...

Analysis complete.
Complaints retrieved: 5,000
Clean complaints:     4,9xx
Output directory:     .../output

Top products:
                         product  complaint_count
                   Credit report             1,420
                    Credit card             1,105
Checking or savings account                860
                         ...
```

`monthly.csv`:

```csv
month,complaint_count
2025-01,412
2025-02,389
2025-03,431
```

 `narrative_terms.csv`:

```csv
term,count
payment,638
account,521
called,407
```

These numbers are **illustrative examples only**, not actual results from a specific run. Complaint counts and frequent words depend on the records returned by the CFPB API.

## 📖 Understanding the Results

### Monthly counts

Monthly counts can show changes in the downloaded records. A change could reflect complaint activity, data coverage, publication timing, product mix, or submission patterns.

### Product and issue summaries

These tables show which categories appear most often in the retrieved records. Counts do not indicate the severity of an issue or the rate at which it affects customers.

### Company counts

Company counts are raw totals. Comparing companies without considering their customer bases, transaction volumes, product mix, and other context can be misleading.

### Response fields

Response categories and timely-response values describe fields in complaint records. Check CFPB documentation for their definitions before drawing conclusions.

### Narrative terms

Frequent words can suggest subjects for further exploration. They do not prove a trend, determine sentiment, or capture the full meaning of a complaint.

## ⚠️ Limitations

- The analysis covers only the records returned by the API query.
- The database is not a representative survey of all consumers.
- Complaint counts are not complaint rates unless appropriate denominators are available.
- Company comparisons do not account for customer or transaction volume.
- Available narratives may not represent complaints without narratives.
- Basic word counts cannot reliably interpret context or intent.
- API limits, field names, and response formats may change.
- Changes in complaint counts do not establish their causes.
- This project is for educational and exploratory analysis, not regulatory or legal conclusions.

## 🔗 References

- [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)
- [CFPB Consumer Complaint API](https://cfpb.github.io/api/ccdb/)
- [CFPB API Documentation](https://cfpb.github.io/ccdb5-api/documentation/)
- [CFPB API Field Definitions](https://cfpb.github.io/api/ccdb/fields.html)

---
## 📄 License

Please refer to the repository for applicable licensing information.

## 👨‍💻 Author

**ursleeplessprogrammer**

*This project summarizes public complaint records for learning and exploration. Its results describe the data retrieved—not every consumer’s experience, company conduct, or the overall quality of a financial product.*
