# main.py
from getter.aws_status_getter import collect_aws_dashboard
from getter.gcp_status_europe_north2 import collect_gcp_dashboard
from getter.dashboard_generator import generate_landing_html, generate_region_html

from pathlib import Path

if __name__ == "__main__":
    input_files = {
        "aws-eu-north-1": "input/rss-eu-north-1.txt",
        "aws-eu-central-1": "input/rss-eu-central-1.txt"
    }

    region_dashboards = {}
    region_statuses = {}

    # AWS Regions
    for region_key, path in input_files.items():
        dashboard, status = collect_aws_dashboard(path)
        region_dashboards[region_key] = dashboard
        region_statuses[region_key] = status

    # GCP Region (hardcoded for now)
    gcp_region = "gcp-europe-north2"
    dashboard, status = collect_gcp_dashboard()
    region_dashboards[gcp_region] = dashboard
    region_statuses[gcp_region] = status

    # Output
    Path("docs").mkdir(exist_ok=True)

    generate_landing_html(region_statuses, "docs/index.html")

    for region, dashboard in region_dashboards.items():
        output_file = f"docs/{region}.html"

        if region.startswith("aws-"):
            clean_region = region[len("aws-"):]
            provider = "AWS"
        elif region.startswith("gcp-"):
            clean_region = region[len("gcp-"):]
            provider = "GCP"
        else:
            clean_region = region
            provider = "Cloud"

        generate_region_html(clean_region, dashboard, output_file, provider=provider)

    print("✅ All dashboards generated.")
