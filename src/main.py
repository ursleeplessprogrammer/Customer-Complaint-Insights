import argparse
from pathlib import Path

from src.analysis import (
    normalize_complaints,
    summarize_complaints,
    summarize_narratives,
)
from src.cfpb_client import fetch_complaints
from src.config import DEFAULT_DAYS, DEFAULT_LIMIT, OUTPUT_DIR
from src.visualization import (
    save_monthly_chart,
    save_top_products_chart,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze complaints from the CFPB Consumer Complaint Database."
    )
    parser.add_argument(
        "--product",
        default=None,
        help="Optional CFPB product filter, for example: 'Credit card'.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_DAYS,
        help=f"Number of recent days to request (default: {DEFAULT_DAYS}).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Maximum complaints to request (default: {DEFAULT_LIMIT}).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory for CSV reports, charts, and the downloaded data.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching complaints from the CFPB API...")
    raw_data = fetch_complaints(
        days=args.days,
        limit=args.limit,
        product=args.product,
    )

    raw_path = args.output_dir / "complaints_raw.csv"
    raw_data.to_csv(raw_path, index=False)

    complaints = normalize_complaints(raw_data)
    summaries = summarize_complaints(complaints)
    narrative_terms = summarize_narratives(complaints)

    complaints.to_csv(
        args.output_dir / "complaints_clean.csv",
        index=False,
    )

    for name, summary in summaries.items():
        summary.to_csv(
            args.output_dir / f"{name}.csv",
            index=False,
        )

    narrative_terms.to_csv(
        args.output_dir / "narrative_terms.csv",
        index=False,
    )

    save_monthly_chart(
        summaries["monthly"],
        args.output_dir / "monthly_complaints.png",
    )
    save_top_products_chart(
        summaries["by_product"],
        args.output_dir / "top_products.png",
    )

    print("\nAnalysis complete.")
    print(f"Complaints retrieved: {len(raw_data):,}")
    print(f"Clean complaints:     {len(complaints):,}")
    print(f"Output directory:     {args.output_dir.resolve()}")

    print("\nTop products:")
    print(summaries["by_product"].head(10).to_string(index=False))

    print("\nTop issues:")
    print(summaries["by_issue"].head(10).to_string(index=False))

    if not narrative_terms.empty:
        print("\nFrequent narrative terms:")
        print(narrative_terms.head(15).to_string(index=False))

    print(
        "\nInterpretation note: CFPB complaint records are not a statistical "
        "sample of all consumers' experiences. Complaint counts alone do not "
        "measure company performance or establish a trend in the broader market."
    )


if __name__ == "__main__":
    main()
